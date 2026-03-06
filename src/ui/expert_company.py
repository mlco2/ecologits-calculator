import io
import json
import math
import operator
from collections import defaultdict
from functools import reduce

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

from ecologits.tracers.utils import llm_impacts

from src.config.constants import COUNTRY_CODES, PROMPTS, TIME_HORIZONS, USAGE_INTENSITY
from src.core.formatting import (
    QImpacts,
    format_adpe,
    format_energy,
    format_gwp,
    format_impacts,
    format_pe,
    format_wcf,
)
from src.core.latency_estimator import latency_estimator
from src.repositories.models import load_models
from src.ui.impacts import display_impacts

_COL_PROVIDER = "Provider"
_COL_MODEL = "Model"
_COL_USAGE_TYPE = "Usage Type"
_COL_USAGE_INTENSITY = "Usage Intensity"
_COL_NUM_USERS = "Number of Users"
_COL_LOCATION = "Usage Location"

_LOCATION_LABELS = [label for label, _ in COUNTRY_CODES]
_LOCATION_LABEL_TO_CODE = dict(COUNTRY_CODES)
_DEFAULT_LOCATION = _LOCATION_LABELS[0]  # "🌎 World"

_EMPTY_ROW = {
    _COL_PROVIDER: None,
    _COL_MODEL: None,
    _COL_USAGE_TYPE: None,
    _COL_USAGE_INTENSITY: None,
    _COL_NUM_USERS: None,
    _COL_LOCATION: _DEFAULT_LOCATION,
}

_INCOMPLETE_CELL_STYLE = JsCode("""
function(params) {
    if (params.value === null || params.value === undefined || params.value === '') {
        return { backgroundColor: '#ffd6d6', border: '1px solid #ff4444' };
    }
    return {};
}
""")


def _build_provider_models_map(df: pd.DataFrame) -> dict[str, list[str]]:
    return {
        provider: sorted(group["name_clean"].unique().tolist())
        for provider, group in df.groupby("provider_clean")
    }


def _build_grid_options(df: pd.DataFrame) -> dict:
    providers = sorted(df["provider_clean"].unique().tolist())
    provider_models_map = _build_provider_models_map(df)
    prompt_labels = [p.label for p in PROMPTS]
    intensity_keys = list(USAGE_INTENSITY.keys())

    model_cell_editor_params = JsCode(
        f"""
function(params) {{
    var providerModelsMap = {json.dumps(provider_models_map)};
    var provider = params.data["{_COL_PROVIDER}"];
    return {{ values: providerModelsMap[provider] || [] }};
}}
"""
    )

    gb = GridOptionsBuilder.from_dataframe(
        pd.DataFrame([_EMPTY_ROW]),
        editable=True,
    )
    gb.configure_default_column(editable=True, resizable=True, cellStyle=_INCOMPLETE_CELL_STYLE)

    gb.configure_column(
        _COL_PROVIDER,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": providers},
        minWidth=150,
    )
    gb.configure_column(
        _COL_MODEL,
        cellEditor="agSelectCellEditor",
        cellEditorParams=model_cell_editor_params,
        minWidth=200,
    )
    gb.configure_column(
        _COL_USAGE_TYPE,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": prompt_labels},
        minWidth=280,
    )
    gb.configure_column(
        _COL_USAGE_INTENSITY,
        header_name="Usage Intensity (per time horizon)",
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": intensity_keys},
        minWidth=240,
    )
    gb.configure_column(
        _COL_NUM_USERS,
        type=["numericColumn"],
        cellEditor="agNumberCellEditor",
        cellEditorParams={"min": 1, "precision": 0},
        minWidth=160,
    )
    gb.configure_column(
        _COL_LOCATION,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": _LOCATION_LABELS},
        minWidth=200,
    )
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_grid_options(singleClickEdit=True, stopEditingWhenCellsLoseFocus=True)

    return gb.build()


def _is_empty(value: object) -> bool:
    """Return True for None, empty string, zero, or NaN."""
    if value is None or value == "":
        return True
    try:
        return math.isnan(float(value))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False


def _row_is_complete(row: dict) -> bool:
    return all(
        not _is_empty(row.get(col))
        for col in [_COL_PROVIDER, _COL_MODEL, _COL_USAGE_TYPE, _COL_USAGE_INTENSITY, _COL_NUM_USERS]
    )


def _compute_row_tokens(row: dict) -> dict[str, int]:
    """Compute daily token counts for a single filled row."""
    prompt = next(p for p in PROMPTS if p.label == row[_COL_USAGE_TYPE])
    daily_count = USAGE_INTENSITY[row[_COL_USAGE_INTENSITY]]
    num_users = int(row[_COL_NUM_USERS])

    multiplier = daily_count * num_users
    return {
        "output_tokens": prompt.output_tokens * multiplier,
        "input_tokens": prompt.input_tokens * multiplier,
        "cached_tokens": prompt.cached_tokens * multiplier,
        "total_tokens": (prompt.output_tokens + prompt.input_tokens + prompt.cached_tokens) * multiplier,
    }


def _run_impacts(df_models: pd.DataFrame, row: dict, output_token_count: int):
    """Run ecologits llm_impacts for a single row, returning formatted impacts or None."""
    mask = (df_models["provider_clean"] == row[_COL_PROVIDER]) & (
        df_models["name_clean"] == row[_COL_MODEL]
    )
    match = df_models[mask]
    if match.empty:
        return None

    provider_raw = match["provider"].values[0]
    model_raw = match["name"].values[0]
    location_code = _LOCATION_LABEL_TO_CODE.get(
        row.get(_COL_LOCATION, _DEFAULT_LOCATION), "WOR"
    )

    estimated_latency = latency_estimator.estimate(
        provider=provider_raw,
        model_name=model_raw,
        output_tokens=output_token_count,
    )
    result = llm_impacts(
        provider=provider_raw,
        model_name=model_raw,
        output_token_count=output_token_count,
        request_latency=estimated_latency,
        electricity_mix_zone=location_code,
    )
    if result.has_errors:
        return None

    impacts, _, _ = format_impacts(result)
    return impacts


def _aggregate_impacts(impacts_list: list[QImpacts]) -> QImpacts:
    """Sum a list of QImpacts using pint's unit-aware arithmetic, then re-normalise scale."""
    energy = reduce(operator.add, [i.energy for i in impacts_list])
    gwp = reduce(operator.add, [i.gwp for i in impacts_list])
    adpe = reduce(operator.add, [i.adpe for i in impacts_list])
    pe = reduce(operator.add, [i.pe for i in impacts_list])
    wcf = reduce(operator.add, [i.wcf for i in impacts_list])
    return QImpacts(
        energy=format_energy(energy.magnitude, str(energy.units)),
        gwp=format_gwp(gwp.magnitude, str(gwp.units)),
        adpe=format_adpe(adpe.magnitude, str(adpe.units)),
        pe=format_pe(pe.magnitude, str(pe.units)),
        wcf=format_wcf(wcf.magnitude, str(wcf.units)),
    )


def expert_company_mode():
    """Expert Company Mode: multi-model, multi-scenario environmental impact calculator."""
    st.markdown("### 👽 Expert Company Mode")

    col_subtitle, col_horizon = st.columns([3, 1])
    with col_subtitle:
        st.markdown(
            "Configure multiple LLM models with different usage scenarios and user counts "
            "to estimate combined token usage and environmental impacts."
        )
    with col_horizon:
        time_horizon_label = st.pills(
            label="Time horizon",
            options=list(TIME_HORIZONS.keys()),
            default="Monthly",
            selection_mode="single",
        )

    df_models = load_models(filter_main=False)

    if "ec_grid_rows" not in st.session_state:
        st.session_state["ec_grid_rows"] = [dict(_EMPTY_ROW)]
    if "ec_grid_version" not in st.session_state:
        st.session_state["ec_grid_version"] = 0

    grid_df = pd.DataFrame(st.session_state["ec_grid_rows"])
    grid_options = _build_grid_options(df_models)

    grid_response = AgGrid(
        grid_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        height=min(200 + len(st.session_state["ec_grid_rows"]) * 42, 500),
        key=f"ec_aggrid_{st.session_state['ec_grid_version']}",
    )

    updated_df: pd.DataFrame = grid_response["data"]
    st.session_state["ec_grid_rows"] = updated_df.to_dict("records")

    selected_rows: pd.DataFrame = grid_response["selected_rows"]
    has_selection = isinstance(selected_rows, pd.DataFrame) and not selected_rows.empty

    col_add, col_remove, col_run = st.columns([1, 1, 2])
    with col_add:
        if st.button("➕ Add row", width="stretch"):
            st.session_state["ec_grid_rows"] = updated_df.to_dict("records") + [dict(_EMPTY_ROW)]
            st.session_state["ec_grid_version"] += 1
            st.rerun()

    with col_remove:
        if st.button("🗑 Remove selected", width="stretch", disabled=not has_selection):
            keep_df = updated_df.merge(
                selected_rows[[c for c in selected_rows.columns if c in updated_df.columns]],
                how="left",
                indicator=True,
            ).query('_merge == "left_only"').drop(columns="_merge")
            remaining = keep_df.to_dict("records") or [dict(_EMPTY_ROW)]
            st.session_state["ec_grid_rows"] = remaining
            st.session_state["ec_grid_version"] += 1
            st.rerun()

    rows = st.session_state["ec_grid_rows"]
    incomplete = [i + 1 for i, r in enumerate(rows) if not _row_is_complete(r)]

    if incomplete:
        st.warning(
            f"Row(s) {incomplete} have incomplete fields (highlighted in red). "
            "Fill all columns before running calculations.",
            icon="⚠️",
        )

    with col_run:
        run = st.button(
            "▶ Run calculations",
            type="primary",
            width="stretch",
            disabled=bool(incomplete) or not rows,
        )

    if not run:
        return

    time_horizon_days = TIME_HORIZONS.get(time_horizon_label, TIME_HORIZONS["Monthly"])

    summary_records = []
    all_impacts = []

    for i, row in enumerate(rows):
        tokens = _compute_row_tokens(row)
        impacts = _run_impacts(df_models, row, tokens["output_tokens"])

        horizon_key = time_horizon_label.lower()
        summary_records.append(
            {
                "llm_provider": row[_COL_PROVIDER],
                "model_name": row[_COL_MODEL],
                "usage_location": row.get(_COL_LOCATION, _DEFAULT_LOCATION),
                f"{horizon_key}_input_tokens": tokens["input_tokens"] * time_horizon_days,
                f"{horizon_key}_output_tokens": tokens["output_tokens"] * time_horizon_days,
                f"{horizon_key}_cached_tokens": tokens["cached_tokens"] * time_horizon_days,
                "impacts_available": impacts is not None,
            }
        )
        if impacts is not None:
            all_impacts.append((i, row, impacts))

    horizon_key = time_horizon_label.lower()
    _TOKEN_COLS = [
        f"{horizon_key}_input_tokens",
        f"{horizon_key}_output_tokens",
        f"{horizon_key}_cached_tokens",
    ]
    _GROUP_COLS = ["llm_provider", "model_name", "usage_location"]
    _IMPACT_COLS = ["energy", "gwp", "adpe", "pe", "wcf"]

    df_summary = (
        pd.DataFrame(summary_records)
        .groupby(_GROUP_COLS, as_index=False)[_TOKEN_COLS]
        .sum()
    )[_GROUP_COLS + _TOKEN_COLS]

    group_impacts: dict[tuple, list[QImpacts]] = defaultdict(list)
    for _, row, imp in all_impacts:
        key = (row[_COL_PROVIDER], row[_COL_MODEL], row.get(_COL_LOCATION, _DEFAULT_LOCATION))
        group_impacts[key].append(imp)

    impact_records = []
    for (provider, model, location), imps in group_impacts.items():
        agg = _aggregate_impacts(imps)
        impact_records.append({
            "llm_provider": provider,
            "model_name": model,
            "usage_location": location,
            "energy": f"{agg.energy.magnitude:.3g} {agg.energy.units}",
            "gwp": f"{agg.gwp.magnitude:.3g} {agg.gwp.units}",
            "adpe": f"{agg.adpe.magnitude:.3g} {agg.adpe.units}",
            "pe": f"{agg.pe.magnitude:.3g} {agg.pe.units}",
            "wcf": f"{agg.wcf.magnitude:.3g} {agg.wcf.units}",
        })

    if impact_records:
        df_summary = df_summary.merge(
            pd.DataFrame(impact_records), on=_GROUP_COLS, how="left"
        )

    col_rename = {
        "llm_provider": "Provider",
        "model_name": "Model",
        "usage_location": _COL_LOCATION,
        f"{horizon_key}_input_tokens": f"{time_horizon_label} Input Tokens",
        f"{horizon_key}_output_tokens": f"{time_horizon_label} Output Tokens",
        f"{horizon_key}_cached_tokens": f"{time_horizon_label} Cached Tokens",
        "energy": "Energy",
        "gwp": "GWP",
        "adpe": "ADPe",
        "pe": "PE",
        "wcf": "WCF",
    }

    with st.container(border=True):
        col_title, col_download = st.columns([3, 1])
        col_title.markdown(f"#### {time_horizon_label} Token Summary (aggregated by model)")

        display_cols = _GROUP_COLS + _TOKEN_COLS + (_IMPACT_COLS if impact_records else [])
        df_display = df_summary[display_cols].rename(columns=col_rename)

        df_excel = df_display.copy()
        df_excel[_COL_LOCATION] = df_excel[_COL_LOCATION].str.split(" ", n=1).str[1]
        excel_buf = io.BytesIO()
        with pd.ExcelWriter(excel_buf, engine="openpyxl") as writer:
            df_excel.to_excel(writer, index=False, sheet_name=f"{time_horizon_label} Token Summary")
        col_download.download_button(
            label="⬇ Download Excel",
            data=excel_buf.getvalue(),
            file_name="expert_company_token_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch",
        )

        st.dataframe(df_display, width="stretch")

    if all_impacts:
        aggregated = _aggregate_impacts([imp for _, _, imp in all_impacts])
        with st.container(border=True):
            st.markdown(
                f"<h5 align='center'>Aggregated Environmental Impacts "
                f"(all rows · {time_horizon_label.lower()})</h5>",
                unsafe_allow_html=True,
            )
            display_impacts(aggregated)

    failed = [
        r["llm_provider"] + "/" + r["model_name"]
        for r in summary_records
        if not r["impacts_available"]
    ]
    if failed:
        st.warning(
            f"Could not compute impacts for: {', '.join(failed)}. "
            "These models may not be in the ecologits repository.",
            icon="⚠️",
        )
