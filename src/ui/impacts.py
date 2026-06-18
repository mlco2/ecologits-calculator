import streamlit as st

from src.ui.components import render_environment_card, render_environment_card_html


def _format_quantity_value(value) -> str:
    return f"{value.magnitude:.3g}"


def _format_quantity_unit(value) -> str:
    return f"{value.units:~}"


def _format_impact_subtext(values_min, values_max) -> str:
    if values_min is None or values_max is None:
        return ""

    unit = _format_quantity_unit(values_min)
    return f"between {_format_quantity_value(values_min)}-{_format_quantity_value(values_max)} {unit}"


def display_mono_impact(impact_lablel, values, icon, values_min=None, values_max=None):

    with st.container(border=True):
        render_environment_card(
            title=impact_lablel,
            value=_format_quantity_value(values),
            unit=_format_quantity_unit(values),
            emoji=icon,
            subtext=_format_impact_subtext(values_min, values_max),
        )


def display_impacts(
    impacts_output=None,
    impacts_to_display: list | None = None,
    mode: str = "basic",
):

    if impacts_to_display is None:
        impacts_to_display = [
            "Electricity",
            "Carbon Footprint",
            "Water",
            "Metals & Minerals",
            "Fossile Fuels",
        ]

    if len(impacts_to_display) == 0:
        st.warning("Select at least one impact to display")
        return

    if impacts_output is None:
        return

    all_impacts = [
        (
            "Electricity",
            "Electricity consumption",
            impacts_output.energy,
            "⚡️",
            impacts_output.energy_min,
            impacts_output.energy_max,
        ),
        (
            "Carbon Footprint",
            "Carbon Footprint",
            impacts_output.gwp,
            "🌍️",
            impacts_output.gwp_min,
            impacts_output.gwp_max,
        ),
        (
            "Water",
            "Water consumption",
            impacts_output.wcf,
            "🚰",
            impacts_output.wcf_min,
            impacts_output.wcf_max,
        ),
        (
            "Metals & Minerals",
            "Metals & Minerals",
            impacts_output.adpe,
            "🪨",
            impacts_output.adpe_min,
            impacts_output.adpe_max,
        ),
        (
            "Fossile Fuels",
            "Fossile fuels",
            impacts_output.pe,
            "⛽️",
            impacts_output.pe_min,
            impacts_output.pe_max,
        ),
    ]

    selected = [
        (label, values, icon, vmin, vmax)
        for key, label, values, icon, vmin, vmax in all_impacts
        if key in impacts_to_display
    ]

    desktop_columns = len(selected) if mode == "basic" else 2
    cards_html = "\n".join(
        render_environment_card_html(
            title=label,
            value=_format_quantity_value(values),
            unit=_format_quantity_unit(values),
            emoji=icon,
            subtext=_format_impact_subtext(vmin, vmax),
        )
        for label, values, icon, vmin, vmax in selected
    )

    st.html(
        f"""
        <div
            class="environment-card-grid environment-card-grid-{mode}"
            style="--environment-card-desktop-columns: {desktop_columns};"
        >
            {cards_html}
        </div>
        """
    )
