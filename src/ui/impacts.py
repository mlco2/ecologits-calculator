import streamlit as st


def display_mono_impact(impact_lablel, values, icon, values_min=None, values_max=None):

    with st.container(border=True):
        st.markdown(
            f"""<p style='font-size:25px; text-align: center;margin-left: 0px'>{icon}</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<p style='font-size:25px; text-align: center;margin-left: 0px'><strong>{impact_lablel}</strong></p>""",
            unsafe_allow_html=True,
        )

        if values_min is not None and values_max is not None:
            help_text = f"Min: {values_min.magnitude:.3g} {values_min.units} — Max: {values_max.magnitude:.3g} {values_max.units}"
        else:
            help_text = None
        st.latex(rf"\Large {values.magnitude:.3g} \ \large {values.units}", help=help_text)


def display_impacts(
    impacts_output=None,
    impacts_to_display: list | None = None,
    mode: str = "calculator",
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
            "Water",
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

    if mode == "calculator":
        cols = st.columns(len(selected))
        for i, (label, values, icon, vmin, vmax) in enumerate(selected):
            with cols[i].container():
                display_mono_impact(
                    impact_lablel=label, values=values, icon=icon, values_min=vmin, values_max=vmax
                )

    else:
        cols = st.columns(2)
        for i, (label, values, icon, vmin, vmax) in enumerate(selected):
            with cols[i % 2].container():
                display_mono_impact(
                    impact_lablel=label, values=values, icon=icon, values_min=vmin, values_max=vmax
                )
