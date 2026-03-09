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


def display_impacts(impacts):
    st.space(5)
    _, col_energy, col_gwp, _ = st.columns([1, 2, 2, 1])

    with col_energy:
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'>⚡️</p><p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>Energy</p>""",
            unsafe_allow_html=True,
        )
        st.markdown('<p align="center">Electricity consumption</p>', unsafe_allow_html=True)
        st.latex(rf"\Large {impacts.energy.magnitude:.3g} \ \large {impacts.energy.units}")
        if impacts.ranges:
            range_plot(
                impacts.energy.magnitude,
                impacts.energy_min.magnitude,
                impacts.energy_max.magnitude,
                impacts.energy.units,
            )

    with col_gwp:
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'>🌍️</p><p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>GHG Emissions</p>""",
            unsafe_allow_html=True,
        )
        st.markdown('<p align="center">Effect on global warming</p>', unsafe_allow_html=True)
        st.latex(rf"\Large {impacts.gwp.magnitude:.3g} \ \large {impacts.gwp.units}")
        if impacts.ranges:
            range_plot(
                impacts.gwp.magnitude,
                impacts.gwp_min.magnitude,
                impacts.gwp_max.magnitude,
                impacts.gwp.units,
            )

    st.space(5)

    col_adpe, col_pe, col_wcf = st.columns(3)

    with col_adpe:
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'>🪨</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>Abiotic Resources</p>""",
            unsafe_allow_html=True,
        )
        st.markdown('<p align="center"> Use of metals and minerals</p>', unsafe_allow_html=True)
        st.latex(rf"\Large {impacts.adpe.magnitude:.3g} \ \large {impacts.adpe.units}")
        if impacts.ranges:
            range_plot(
                impacts.adpe.magnitude,
                impacts.adpe_min.magnitude,
                impacts.adpe_max.magnitude,
                impacts.adpe.units,
            )

    with col_pe:
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'>⛽️</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>Primary Energy</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p align="center">Use of natural energy resources</p>',
            unsafe_allow_html=True,
        )
        st.latex(rf"\Large {impacts.pe.magnitude:.3g} \ \large {impacts.pe.units}")
        if impacts.ranges:
            range_plot(
                impacts.pe.magnitude,
                impacts.pe_min.magnitude,
                impacts.pe_max.magnitude,
                impacts.pe.units,
            )

    with col_wcf:
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'>🚰</p>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<p style='font-size:30px;text-align: center;margin-bottom :2px'><strong>Water</p>""",
            unsafe_allow_html=True,
        )
        st.markdown('<p align="center">Water consumption</p>', unsafe_allow_html=True)
        st.latex(rf"\Large {impacts.wcf.magnitude:.3g} \ \large {impacts.wcf.units}")
        if impacts.ranges:
            range_plot(
                impacts.wcf.magnitude,
                impacts.wcf_min.magnitude,
                impacts.wcf_max.magnitude,
                impacts.wcf.units,
            )


############################################################################################################


def display_equivalent_energy(impacts):
    st.markdown("<br>", unsafe_allow_html=True)

    ev_eq = format_energy_eq_electric_vehicle(impacts.energy)

    col1, col2, col3 = st.columns(3)

    with col2:
        physical_activity, distance = format_energy_eq_physical_activity(impacts.energy)
        activity_label = str(physical_activity)
        if physical_activity == PhysicalActivity.WALKING:
            activity_label = "🚶 " + physical_activity.capitalize()
        if physical_activity == PhysicalActivity.RUNNING:
            activity_label = "🏃 " + physical_activity.capitalize()

        st.markdown(f'<h4 align="center">{activity_label}</h4>', unsafe_allow_html=True)
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
