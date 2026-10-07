import io
import math
import operator

from collections import defaultdict
from functools import reduce

import pandas as pd
import streamlit as st

from ecologits.electricity_mix_repository import electricity_mixes
from ecologits.tracers.utils import llm_impacts

from src.config.constants import COUNTRY_CODES, TIME_HORIZONS
from src.core.formatting import (
    QImpacts,
    format_adpe,
    format_energy,
    format_gwp,
    format_impacts,
    format_pe,
    format_wcf,
)
from src.repositories.models import get_raw_model_names, load_models
from src.ui.components.impacts import display_impacts

_COL_MODEL = "Provider / Model"
_COL_TOKENS_PER_USER = "Tokens per User per Selected Unit of Time"
_COL_NUM_USERS = "Number of Users"
_COL_LOCATION = "Usage Location"

_LOCATION_LABELS = [label for label, _ in COUNTRY_CODES]
_LOCATION_LABEL_TO_CODE = dict(COUNTRY_CODES)
_DEFAULT_LOCATION = _LOCATION_LABELS[0]  # "🌎 World"

_EMPTY_ROW = {
    _COL_MODEL: None,
    _COL_TOKENS_PER_USER: None,
    _COL_NUM_USERS: None,
    _COL_LOCATION: _DEFAULT_LOCATION,
}


def _render_grid(df_models: pd.DataFrame) -> dict:
    """Render native Streamlit editor and return current rows."""
    models = sorted(
        f"{row.provider_clean} / {row.name_clean}"
        for row in df_models[["provider_clean", "name_clean"]].itertuples(index=False)
    )
    grid_df = st.session_state.setdefault(
        "ec_grid_base",
        pd.DataFrame([_EMPTY_ROW], columns=list(_EMPTY_ROW)),
    )
    edited_df = st.data_editor(
        grid_df,
        column_config={
            _COL_MODEL: st.column_config.SelectboxColumn(options=models, required=True),
            _COL_TOKENS_PER_USER: st.column_config.NumberColumn(
                min_value=0,
                step=1,
                required=True,
            ),
            _COL_NUM_USERS: st.column_config.NumberColumn(
                min_value=1,
                step=1,
                required=True,
            ),
            _COL_LOCATION: st.column_config.SelectboxColumn(
                options=_LOCATION_LABELS,
                required=True,
                default=_DEFAULT_LOCATION,
            ),
        },
        num_rows="dynamic",
        hide_index=True,
        width="stretch",
        key="ec_data_editor",
    )
    rows = edited_df.to_dict("records")

    incomplete = [i + 1 for i, r in enumerate(rows) if not _row_is_complete(r)]
    if incomplete:
        st.warning(
            f"Some row(s) {incomplete} have incomplete fields. Fill all columns before running calculations.",
            icon="⚠️",
        )

    return {
        "rows": rows,
        "incomplete": incomplete,
        "run": st.button(
            "▶ Run calculations",
            type="primary",
            width="stretch",
            disabled=bool(incomplete) or not rows,
        ),
    }


def _is_empty(value: object) -> bool:
    """Return True for None, empty string, or NaN."""
    if value is None or value == "":
        return True
    try:
        return math.isnan(float(value))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False


def _row_is_complete(row: dict) -> bool:
    return all(
        not _is_empty(row.get(col))
        for col in [
            _COL_MODEL,
            _COL_TOKENS_PER_USER,
            _COL_NUM_USERS,
        ]
    )


def _split_model_selection(value: str) -> tuple[str, str] | None:
    provider, separator, model = value.partition(" / ")
    return (provider, model) if separator else None


def _compute_row_tokens(row: dict) -> int:
    """Compute total output tokens from selected-period usage for one row."""
    tokens_per_user = row[_COL_TOKENS_PER_USER]
    if tokens_per_user is None or tokens_per_user == "":
        raise ValueError("Tokens per user cannot be empty or None")
    try:
        tokens_per_user = int(tokens_per_user)
        if tokens_per_user < 0:
            raise ValueError(f"Tokens per user must be non-negative, got {tokens_per_user}")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid tokens per user value '{row[_COL_TOKENS_PER_USER]}': {e}") from e

    num_users_str = row[_COL_NUM_USERS]
    if num_users_str is None or num_users_str == "":
        raise ValueError("Number of users cannot be empty or None")

    try:
        num_users = int(num_users_str)
        if num_users < 0:
            raise ValueError(f"Number of users must be non-negative, got {num_users}")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid number of users value '{num_users_str}': {e}") from e

    output_tokens = tokens_per_user * num_users
    return output_tokens


def _run_impacts(df_models: pd.DataFrame, row: dict, output_token_count: int):
    """Run ecologits llm_impacts for a single row, returning formatted impacts or None."""
    model_selection = _split_model_selection(row[_COL_MODEL])
    if model_selection is None:
        return None
    provider, model = model_selection
    raw_names = get_raw_model_names(df_models, provider, model)
    if raw_names is None:
        return None
    provider_raw, model_raw = raw_names
    location_code = _LOCATION_LABEL_TO_CODE.get(row.get(_COL_LOCATION, _DEFAULT_LOCATION), "WOR")

    result = llm_impacts(
        provider=provider_raw,
        model_name=model_raw,
        output_token_count=output_token_count,
        request_latency=float("inf"),
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


def _aggregate_and_display(df_models: pd.DataFrame, rows: list, time_horizon_label: str) -> None:
    """Compute impacts for all rows, aggregate by provider/model/location, and display results."""
    # Check for electricity mix warnings in selected locations
    selected_locations = {row.get(_COL_LOCATION, _DEFAULT_LOCATION) for row in rows}
    location_codes = [_LOCATION_LABEL_TO_CODE.get(loc, "WOR") for loc in selected_locations]

    has_electricity_warnings = any(
        electricity_mixes.find_electricity_mix(code).has_warnings
        for code in location_codes
        if electricity_mixes.find_electricity_mix(code) is not None
    )

    if has_electricity_warnings:
        st.info(
            "⚠️ Some selected locations use default electricity mix values, which may affect precision. "
            "Hover over location names in the results for more details.",
            icon="ℹ️",
        )

    summary_records = []
    all_impacts = []

    for i, row in enumerate(rows):
        output_tokens = _compute_row_tokens(row)
        impacts = _run_impacts(df_models, row, output_tokens)
        model_selection = _split_model_selection(row[_COL_MODEL])
        provider, model = model_selection or ("", row[_COL_MODEL])

        horizon_key = time_horizon_label.lower()
        summary_records.append(
            {
                "llm_provider": provider,
                "model_name": model,
                "usage_location": row.get(_COL_LOCATION, _DEFAULT_LOCATION),
                f"{horizon_key}_output_tokens": output_tokens,
                "impacts_available": impacts is not None,
            }
        )
        if impacts is not None:
            all_impacts.append((i, row, impacts))

    horizon_key = time_horizon_label.lower()
    _TOKEN_COLS = [
        f"{horizon_key}_output_tokens",
    ]
    _GROUP_COLS = ["llm_provider", "model_name", "usage_location"]
    _IMPACT_COLS = ["energy", "gwp", "adpe", "pe", "wcf"]

    df_summary = (
        pd.DataFrame(summary_records).groupby(_GROUP_COLS, as_index=False)[_TOKEN_COLS].sum()
    )[_GROUP_COLS + _TOKEN_COLS]

    group_impacts: dict[tuple, list[QImpacts]] = defaultdict(list)
    for _, row, imp in all_impacts:
        provider, model = _split_model_selection(row[_COL_MODEL])
        key = (provider, model, row.get(_COL_LOCATION, _DEFAULT_LOCATION))
        group_impacts[key].append(imp)

    impact_records = []
    for (provider, model, location), imps in group_impacts.items():
        agg = _aggregate_impacts(imps)
        impact_records.append(
            {
                "llm_provider": provider,
                "model_name": model,
                "usage_location": location,
                "energy": f"{agg.energy.magnitude:.3g} {agg.energy.units}",
                "gwp": f"{agg.gwp.magnitude:.3g} {agg.gwp.units}",
                "adpe": f"{agg.adpe.magnitude:.3g} {agg.adpe.units}",
                "pe": f"{agg.pe.magnitude:.3g} {agg.pe.units}",
                "wcf": f"{agg.wcf.magnitude:.3g} {agg.wcf.units}",
            }
        )

    if impact_records:
        df_summary = df_summary.merge(pd.DataFrame(impact_records), on=_GROUP_COLS, how="left")

    col_rename = {
        "llm_provider": "Provider",
        "model_name": "Model",
        "usage_location": _COL_LOCATION,
        f"{horizon_key}_output_tokens": f"{time_horizon_label} Output Tokens",
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
                f"<h5 align='center'>Aggregated {time_horizon_label.lower()} environmental impacts</h5>",
                unsafe_allow_html=True,
            )
            display_impacts(
                aggregated,
                impacts_to_display=[
                    "Electricity",
                    "Carbon Footprint",
                    "Water",
                    "Metals & Minerals",
                    "Fossile Fuels",
                ],
                mode="company",
            )

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


def expert_company_mode():
    """Expert Company Mode: multi-model, multi-scenario environmental impact calculator."""
    col_subtitle, col_horizon = st.columns([3, 1])
    with col_subtitle:
        st.markdown(
            "Configure token usage per user for multiple LLM models to estimate combined "
            "token usage and environmental impacts."
        )
    with col_horizon:
        time_horizon_label = st.pills(
            label="Time horizon",
            options=list(TIME_HORIZONS.keys()),
            default="Monthly",
            selection_mode="single",
            required=True,
        )

    df_models = load_models(filter_main=True)

    st.session_state.setdefault(
        "ec_grid_base",
        pd.DataFrame([_EMPTY_ROW], columns=list(_EMPTY_ROW)),
    )
    grid_state = _render_grid(df_models)

    if not grid_state["run"]:
        return

    with st.spinner("Computing impacts…"):
        _aggregate_and_display(df_models, grid_state["rows"], time_horizon_label)
