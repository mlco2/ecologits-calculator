import io
import json

import pandas as pd
import streamlit as st

from ecologits.tracers.utils import llm_impacts
from ecologits.utils.range_value import RangeValue
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

from src.core.formatting import format_adpe, format_gwp, format_pe, format_wcf
from src.core.latency_estimator import latency_estimator
from src.repositories.models import load_models
from src.ui.common import (
    COL_DIFF_ADPE,
    COL_DIFF_GWP,
    COL_DIFF_PE,
    COL_DIFF_WCF,
    COL_LOCATION,
    COL_MODEL,
    COL_NEW_LOCATION,
    COL_NEW_MODEL,
    COL_NEW_PROVIDER,
    COL_PROVIDER,
    COL_TOKENS,
    COMPARISON_EMPTY_ROW,
    DIFF_COLS,
    EMPTY_DIFFS,
    IMPACT_DIFF_CELL_STYLE,
    IMPACT_DIFF_TOOLTIP,
    INCOMPLETE_CELL_STYLE,
    LOCATION_LABEL_TO_CODE,
    LOCATION_LABELS,
    build_provider_models_map,
    is_empty,
)

DIFF_COL_ATTR = {
    COL_DIFF_GWP: ("gwp", format_gwp),
    COL_DIFF_ADPE: ("adpe", format_adpe),
    COL_DIFF_PE: ("pe", format_pe),
    COL_DIFF_WCF: ("wcf", format_wcf),
}

# Raw diff entry per row: {col: {"abs": str, "pct": str}}
_EMPTY_RAW_DIFFS = {col: {"abs": "", "pct": ""} for col in DIFF_COLS}


def _build_grid_options(df: pd.DataFrame) -> dict:
    providers = sorted(df["provider_clean"].unique().tolist())
    provider_models_map = build_provider_models_map(df)

    model_cell_editor_params = JsCode(
        f"""
function(params) {{
    var providerModelsMap = {json.dumps(provider_models_map)};
    var provider = params.data["{COL_PROVIDER}"];
    return {{ values: providerModelsMap[provider] || [] }};
}}
"""
    )
    new_model_cell_editor_params = JsCode(
        f"""
function(params) {{
    var providerModelsMap = {json.dumps(provider_models_map)};
    var provider = params.data["{COL_NEW_PROVIDER}"];
    return {{ values: providerModelsMap[provider] || [] }};
}}
"""
    )

    gb = GridOptionsBuilder.from_dataframe(
        pd.DataFrame([{**COMPARISON_EMPTY_ROW, **EMPTY_DIFFS}]),
        editable=True,
    )
    gb.configure_default_column(editable=True, resizable=True, cellStyle=INCOMPLETE_CELL_STYLE)

    gb.configure_column(
        COL_PROVIDER,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": providers},
        minWidth=140,
    )
    gb.configure_column(
        COL_MODEL,
        cellEditor="agSelectCellEditor",
        cellEditorParams=model_cell_editor_params,
        minWidth=200,
    )
    gb.configure_column(
        COL_LOCATION,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": LOCATION_LABELS},
        minWidth=180,
    )
    gb.configure_column(
        COL_TOKENS,
        type=["numericColumn"],
        cellEditor="agNumberCellEditor",
        cellEditorParams={"min": 1, "precision": 0},
        minWidth=140,
    )
    gb.configure_column(
        COL_NEW_PROVIDER,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": providers},
        minWidth=140,
    )
    gb.configure_column(
        COL_NEW_MODEL,
        cellEditor="agSelectCellEditor",
        cellEditorParams=new_model_cell_editor_params,
        minWidth=200,
    )
    gb.configure_column(
        COL_NEW_LOCATION,
        cellEditor="agSelectCellEditor",
        cellEditorParams={"values": LOCATION_LABELS},
        minWidth=180,
    )
    for diff_col in DIFF_COLS:
        gb.configure_column(
            diff_col,
            editable=False,
            cellStyle=IMPACT_DIFF_CELL_STYLE,
            tooltipValueGetter=IMPACT_DIFF_TOOLTIP,
            minWidth=140,
        )
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_grid_options(
        singleClickEdit=True,
        stopEditingWhenCellsLoseFocus=True,
        enableBrowserTooltips=True,
    )

    return gb.build()  # type: ignore[no-any-return]


def _row_is_complete(row: dict) -> bool:
    return all(not is_empty(row.get(col)) for col in COMPARISON_EMPTY_ROW)


def _extract_raw_value(impacts, attr: str) -> float:
    """Extract scalar float from an Impacts attribute, using mean for RangeValue."""
    val = getattr(impacts, attr).value
    return float(val.mean) if isinstance(val, RangeValue) else float(val)


def _run_llm_impacts(
    df_models: pd.DataFrame, provider_clean: str, model_clean: str, location_label: str, tokens: int
):
    """Run llm_impacts for a single configuration; returns Impacts or None."""
    mask = (df_models["provider_clean"] == provider_clean) & (
        df_models["name_clean"] == model_clean
    )
    match = df_models[mask]
    if match.empty:
        return None
    provider_raw = match["provider"].values[0]
    model_raw = match["name"].values[0]
    location_code = LOCATION_LABEL_TO_CODE.get(location_label, "WOR")
    latency = latency_estimator.estimate(
        provider=provider_raw,
        model_name=model_raw,
        output_tokens=tokens,
    )
    result = llm_impacts(
        provider=provider_raw,
        model_name=model_raw,
        output_token_count=tokens,
        request_latency=latency,
        electricity_mix_zone=location_code,
    )
    return None if result.has_errors else result


def _fmt_magnitude(x: float) -> str:
    """Format a number without scientific notation, with appropriate precision."""
    a = abs(x)
    if a >= 1000:
        return f"{x:,.0f}"
    if a >= 10:
        return f"{x:.1f}"
    if a >= 1:
        return f"{x:.2f}"
    if a >= 0.001:
        return f"{x:.3f}"
    return f"{x:.2e}"


def _compute_all_impact_diffs(df_models: pd.DataFrame, row: dict) -> dict[str, dict[str, str]]:
    """Compute abs and pct diff strings for all impact types for one complete row."""
    tokens = int(row[COL_TOKENS])
    orig = _run_llm_impacts(df_models, row[COL_PROVIDER], row[COL_MODEL], row[COL_LOCATION], tokens)
    new = _run_llm_impacts(
        df_models, row[COL_NEW_PROVIDER], row[COL_NEW_MODEL], row[COL_NEW_LOCATION], tokens
    )

    if orig is None or new is None:
        return dict(_EMPTY_RAW_DIFFS)

    result = {}
    for col, (attr, fmt_fn) in DIFF_COL_ATTR.items():
        orig_val = _extract_raw_value(orig, attr)
        new_val = _extract_raw_value(new, attr)
        diff = new_val - orig_val
        # Use abs(diff) so format_* functions pick the correct unit for positive values
        qty = fmt_fn(abs(diff))
        sign = ""
        if diff > 0:
            sign = "+"
        if diff < 0:
            sign = "-"
        abs_str = f"{sign}{_fmt_magnitude(qty.magnitude)} {qty.units}"
        if orig_val != 0:
            pct = diff / orig_val * 100
            pct_sign = "+" if pct > 0 else ""
            pct_str = f"{pct_sign}{pct:.1f}%"
        else:
            pct_str = ""
        result[col] = {"abs": abs_str, "pct": pct_str}
    return result


def _to_display_diffs(raw: dict[str, dict[str, str]], mode: str) -> dict[str, str]:
    """Convert raw diff entry to display strings based on selected mode."""
    key = "abs" if mode == "Absolute" else "pct"
    return {col: v[key] for col, v in raw.items()}


def _apply_autofill(rows: list[dict]) -> list[dict]:
    """Copy Provider/Model/Location into New counterparts when those are empty."""
    for row in rows:
        if is_empty(row.get(COL_NEW_PROVIDER)):
            row[COL_NEW_PROVIDER] = row.get(COL_PROVIDER)
        if is_empty(row.get(COL_NEW_MODEL)):
            row[COL_NEW_MODEL] = row.get(COL_MODEL)
        if is_empty(row.get(COL_NEW_LOCATION)):
            row[COL_NEW_LOCATION] = row.get(COL_LOCATION)
    return rows


def _strip_diffs(records: list[dict]) -> list[dict]:
    """Remove diff columns from a list of row dicts."""
    return [{k: v for k, v in r.items() if k not in DIFF_COLS} for r in records]


def model_comparison_mode():
    """Model Choice Impact: compare environmental impacts between two LLM configurations."""
    col_desc, col_mode = st.columns([3, 1])
    with col_desc:
        st.markdown(
            "Compare the environmental impact of switching from one LLM model configuration "
            "to another. Fill each row with the current and proposed configurations."
        )
    with col_mode:
        display_mode = st.pills(
            "Display mode",
            ["Absolute", "Relative"],
            default="Absolute",
            selection_mode="single",
        )

    df_models = load_models(filter_main=False)

    if "mc_grid_rows" not in st.session_state:
        st.session_state["mc_grid_rows"] = [dict(COMPARISON_EMPTY_ROW)]
    if "mc_grid_version" not in st.session_state:
        st.session_state["mc_grid_version"] = 0
    if "mc_diff_raw" not in st.session_state:
        st.session_state["mc_diff_raw"] = [dict(_EMPTY_RAW_DIFFS)]

    rows = st.session_state["mc_grid_rows"]

    # Realign stored diffs when row count changes (add/remove)
    if len(st.session_state["mc_diff_raw"]) != len(rows):
        st.session_state["mc_diff_raw"] = [dict(_EMPTY_RAW_DIFFS)] * len(rows)

    display_diffs = [
        _to_display_diffs(raw, display_mode) for raw in st.session_state["mc_diff_raw"]
    ]
    grid_df = pd.DataFrame(
        [{**row, **diffs} for row, diffs in zip(rows, display_diffs, strict=False)]
    )

    grid_options = _build_grid_options(df_models)

    grid_response = AgGrid(
        grid_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        height=min(200 + len(rows) * 42, 500),
        key=f"mc_aggrid_{st.session_state['mc_grid_version']}",
    )

    updated_df: pd.DataFrame = grid_response["data"]
    updated_rows = _apply_autofill(_strip_diffs(updated_df.to_dict("records")))
    st.session_state["mc_grid_rows"] = updated_rows

    selected_rows: pd.DataFrame = grid_response["selected_rows"]
    has_selection = isinstance(selected_rows, pd.DataFrame) and len(selected_rows) > 0

    # Pair each editable row with its raw diffs for aligned remove/duplicate operations
    current_pairs = list(
        zip(
            _strip_diffs(updated_df.to_dict("records")),
            st.session_state["mc_diff_raw"],
            strict=False,
        )
    )

    col_add, col_remove, col_dup, col_export, col_compute = st.columns([1, 1, 1, 1, 2])
    with col_add:
        if st.button("➕ Add row", width="stretch"):
            st.session_state["mc_grid_rows"] = [*updated_rows, dict(COMPARISON_EMPTY_ROW)]
            st.session_state["mc_diff_raw"] = [
                *st.session_state["mc_diff_raw"],
                dict(_EMPTY_RAW_DIFFS),
            ]
            st.session_state["mc_grid_version"] += 1
            st.rerun()

    with col_remove:
        if st.button("🗑 Remove selected", width="stretch", disabled=not has_selection):
            selected_no_diff = _strip_diffs(selected_rows.to_dict("records"))
            remaining = [(r, raw) for r, raw in current_pairs if r not in selected_no_diff]
            if not remaining:
                remaining = [(dict(COMPARISON_EMPTY_ROW), dict(_EMPTY_RAW_DIFFS))]
            rem_rows, rem_raw = zip(*remaining, strict=False)
            st.session_state["mc_grid_rows"] = _apply_autofill(list(rem_rows))
            st.session_state["mc_diff_raw"] = list(rem_raw)
            st.session_state["mc_grid_version"] += 1
            st.rerun()

    with col_dup:
        if st.button("📋 Duplicate selected", width="stretch", disabled=not has_selection):
            selected_no_diff = _strip_diffs(selected_rows.to_dict("records"))
            duped = [(r, raw) for r, raw in current_pairs if r in selected_no_diff]
            duped_rows = [r for r, _ in duped]
            duped_raw = [raw for _, raw in duped]
            st.session_state["mc_grid_rows"] = [*updated_rows, *duped_rows]
            st.session_state["mc_diff_raw"] = [*st.session_state["mc_diff_raw"], *duped_raw]
            st.session_state["mc_grid_version"] += 1
            st.rerun()

    with col_export:
        export_records = []
        for row, raw in zip(
            st.session_state["mc_grid_rows"], st.session_state["mc_diff_raw"], strict=False
        ):
            export_row = dict(row)
            for col in DIFF_COLS:
                abs_val = raw[col]["abs"]
                pct_val = raw[col]["pct"]
                export_row[col] = (
                    f"{abs_val} ({pct_val})" if abs_val and pct_val else abs_val or pct_val
                )
            export_records.append(export_row)
        df_export = pd.DataFrame(export_records)
        for col in [COL_LOCATION, COL_NEW_LOCATION]:
            if col in df_export.columns:
                df_export[col] = df_export[col].str.split(" ", n=1).str[1]
        excel_buf = io.BytesIO()
        with pd.ExcelWriter(excel_buf, engine="openpyxl") as writer:
            df_export.to_excel(writer, index=False, sheet_name="Model Comparison")
        st.download_button(
            label="⬇ Export to Excel",
            data=excel_buf.getvalue(),
            file_name="model_comparison.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch",
        )

    incomplete = [
        i + 1 for i, r in enumerate(st.session_state["mc_grid_rows"]) if not _row_is_complete(r)
    ]
    with col_compute:
        if st.button(
            "▶ Compute impact difference",
            type="primary",
            width="stretch",
            disabled=bool(incomplete) or not rows,
        ):
            st.session_state["mc_diff_raw"] = [
                _compute_all_impact_diffs(df_models, row)
                if _row_is_complete(row)
                else dict(_EMPTY_RAW_DIFFS)
                for row in st.session_state["mc_grid_rows"]
            ]
            st.session_state["mc_grid_version"] += 1
            st.rerun()

    if incomplete:
        st.warning(
            f"Row(s) {incomplete} have incomplete fields (highlighted in red). "
            "Fill all columns before computing.",
            icon="⚠️",
        )
