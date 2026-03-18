import streamlit as st

from src.core.equivalences import (
    EnergyProduction,
    PhysicalActivity,
    format_energy_eq_electric_vehicle,
    format_energy_eq_electricity_consumption_ireland,
    format_energy_eq_electricity_production,
    format_energy_eq_physical_activity,
    format_gwp_eq_airplane_paris_nyc,
    format_gwp_eq_streaming,
)
from src.ui.plotting import range_plot


def display_mono_impact(impact_lablel, values, icon):

    #st.markdown(f"""<p style='font-size:25px; text-align: left;margin-left: 0px'><strong>{icon} {impact_lablel}</strong></p>""", unsafe_allow_html=True)
    with st.container(border=True):

        col_impacts, col_mid, col_eq = st.columns([2, 1, 2])
        col_impacts.markdown(f"""<p style='font-size:25px; text-align: center;margin-left: 0px'>{icon}</p>""", unsafe_allow_html=True)
        col_impacts.markdown(f"""<p style='font-size:25px; text-align: center;margin-left: 0px'><strong>{impact_lablel}</strong></p>""", unsafe_allow_html=True)
        col_impacts.latex(rf"\Large {values.magnitude:.3g} \ \large {values.units}", help="Average value from a range compute. Min range : Max range : ")

        #col_mid.markdown("|")
        #col_mid.

        col_eq.markdown("<p align=center>Equivalent to</p>", unsafe_allow_html=True)


def display_impacts(impacts_output = None, impacts_to_display: list = ["Electricity", "Carbon Footprint", "Water"]):

    if len(impacts_to_display) == 0:
        st.warning("Select at least one impact to display")

    col_left, col_right = st.columns(2)

    if "Electricity" in impacts_to_display:
        with col_left.container():
            display_mono_impact(
                impact_lablel="Electricity consumption",
                values=impacts_output.energy,
                icon="⚡️"
            )

    if "Carbon Footprint" in impacts_to_display:
        with col_right.container():
            display_mono_impact(
                impact_lablel="Carbon Footprint",
                values=impacts_output.gwp,
                icon="🌍️"
            )

    if "Water" in impacts_to_display:
        with col_left.container():
            display_mono_impact(
                impact_lablel="Water",
                values=impacts_output.wcf,
                icon="🚰"
            )

    if "Metals & Minerals" in impacts_to_display:
        with col_right.container():
            display_mono_impact(
                impact_lablel="Metals & Minerals",
                values=impacts_output.adpe,
                icon="🪨"
            )

    if "Fossile Fuels" in impacts_to_display:
        with col_left.container():
            display_mono_impact(
                impact_lablel="Fossile fuels",
                values=impacts_output.pe,
                icon="⛽️"
            )


############################################################################################################


def display_equivalent_energy(impacts):
    st.markdown("<br>", unsafe_allow_html=True)

    ev_eq = format_energy_eq_electric_vehicle(impacts.energy)

    col1, col2, col3 = st.columns(3)

    with col2:
        physical_activity, distance = format_energy_eq_physical_activity(impacts.energy)
        if physical_activity == PhysicalActivity.WALKING:
            physical_activity = "🚶 " + physical_activity.capitalize()
        if physical_activity == PhysicalActivity.RUNNING:
            physical_activity = "🏃 " + physical_activity.capitalize()

        st.markdown(f'<h4 align="center">{physical_activity}</h4>', unsafe_allow_html=True)
        st.markdown(
            f"""<p style='font-size:35px;text-align: center'>≈  {distance.magnitude:.3g} <i>{distance.units} </p>""",
            unsafe_allow_html=True,
        )

    with col3:
        ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>🔋 Electric Vehicle</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<p style='font-size:35px;text-align: center'>≈ {ev_eq.magnitude:.3g} <i>{ev_eq.units} </p>""",
            unsafe_allow_html=True,
        )

    with col1:
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>⚡️Energy</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<p style='font-size:35px;text-align: center'> {impacts.energy.magnitude:.3g} {impacts.energy.units} </p>""",
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<h3 align="center">What if 1% of the planet does the same everyday for 1 year ?</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<p align="center"> {impacts.energy.magnitude:.3g} {impacts.energy.units} x 1% of 8 billion people x 365 days are ≈ equivalent to</p><br>""",
        unsafe_allow_html=True,
    )

    col4, col5, _ = st.columns(3)

    with col4:
        electricity_production, count = format_energy_eq_electricity_production(impacts.energy)
        if electricity_production == EnergyProduction.NUCLEAR:
            emoji = "☢️"
            name = "Nuclear power plants"
        if electricity_production == EnergyProduction.WIND:
            emoji = "💨️ "
            name = "Wind turbines"
        st.markdown(
            f'<h4 align="center">{emoji} {count.magnitude:.0f} {name} </h4>',
            unsafe_allow_html=True,
        )
        st.markdown('<p align="center">Energy produced yearly </p>', unsafe_allow_html=True)

    with col5:
        ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
        st.markdown(
            f'<h4 align="center">⚡️ 🇮🇪 {ireland_count.magnitude:.3f} x Ireland </h4>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p align="center">Yearly electricity consumption</p>',
            unsafe_allow_html=True,
        )


def display_equivalent_ghg(impacts):
    st.markdown("<br>", unsafe_allow_html=True)

    streaming_eq = format_gwp_eq_streaming(impacts.gwp)

    col1, col2, _ = st.columns(3)

    with col1:
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>🌍️GHG Emissions</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<p style='font-size:35px;text-align: center'> {impacts.gwp.magnitude:.3g} {impacts.gwp.units} </p>""",
            unsafe_allow_html=True,
        )

    with col2:
        streaming_eq = format_gwp_eq_streaming(impacts.gwp)
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>⏯️ Streaming</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""<p style='font-size:35px;text-align: center'>≈ {streaming_eq.magnitude:.3g} <i>{streaming_eq.units} </p>""",
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        '<h3 align="center">What if 1% of the planet does the same everyday for 1 year ?</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<p align="center"> {impacts.gwp.magnitude:.3g} {impacts.gwp.units} x 1% of 8 billion people x 365 days are ≈ equivalent to</p><br>""",
        unsafe_allow_html=True,
    )

    _col4, col5, _ = st.columns(3)

    with col5:
        paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc(impacts.gwp)
        st.markdown(
            f'<h4 align="center">✈️ {round(paris_nyc_airplane.magnitude):,} Paris ↔ NYC</h4>',
            unsafe_allow_html=True,
        )
        st.markdown('<p align="center"><i>Based on GHG emissions<i></p>', unsafe_allow_html=True)
