# src/equivalents/display.py
import streamlit as st
from src.core.equivalences import (
    EnergyProduction,
    PhysicalActivity,
    format_adpe_eq_nvidia,
    format_energy_eq_electric_vehicle,
    format_energy_eq_electricity_consumption_ireland,
    format_energy_eq_electricity_production,
    format_energy_eq_physical_activity,
    format_gwp_eq_airplane_paris_nyc,
    format_gwp_eq_streaming,
    format_wue_eq_drops,
    format_wue_eq_pools,
    format_gwp_eq_vehicle,
    format_wue_eq_pints,
    format_adpe_eq_iphone
)
from src.core.equivalences import EQ_KPIS, EquivalentType


def render_equivalent(value, emoji="", name="", text=""):
    st.markdown(
        f'<h2 align="center">{value}</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h4 align="center">{emoji} {name}</h4>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p align="center">{text}</p>', unsafe_allow_html=True)


def display_equivalent_energy(impacts, type=EquivalentType.EV, how="unit"):

    with st.container(border=True):

        if type == EquivalentType.EV:
            ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
            render_equivalent(
                value=f"{ev_eq.magnitude:.1f} {ev_eq.units}",
                emoji="🔋",
                name="with an electric vehicle",
                text="(based on electricity consumption)",
            )

        elif type == EquivalentType.SPORT:
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
            render_equivalent(
                value=f"{distance.magnitude:.3g} <i>{distance.units}</p>",
                name=physical_activity,
            )

        elif type == EquivalentType.EPROD:
            electricity_production, count = format_energy_eq_electricity_production(impacts.energy)
            if electricity_production == EnergyProduction.NUCLEAR:
                emoji = "☢️"
                name = "Nuclear power plants"
            if electricity_production == EnergyProduction.WIND:
                emoji = "💨️ "
                name = "Wind turbines"
            render_equivalent(
                value=f"{int(count.magnitude):,}",
                emoji=emoji,
                name=name,
                text="(yearly energy production)",
            )

        elif type == EquivalentType.ECONS:
            ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
            st.markdown(
                f'<h4 align="center">⚡️ 🇮🇪 {ireland_count.magnitude:.3f} x Ireland </h4>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p align="center">Yearly electricity consumption</p>',
                unsafe_allow_html=True,
            )


def display_equivalent_ghg(impacts, type=EquivalentType.PLANE):
    with st.container(border=True):
        if type == EquivalentType.STREAMING:
            streaming_eq = format_gwp_eq_streaming(impacts.gwp)
            render_equivalent(
                value=f"{streaming_eq.magnitude:.2f} {streaming_eq.units}",
                emoji="⏯️",
                name="streaming videos",
                text="(based on GHG emissions)",
            )
        elif type == EquivalentType.PLANE:
            paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc(impacts.gwp)
            render_equivalent(
                value=f"{int(paris_nyc_airplane.magnitude):,}",
                emoji="✈️",
                name="Paris ↔ NYC",
                text="(based on GHG emissions)",
            )
        elif type == EquivalentType.THERMIC_VEHICLE:
            thermic_vehicle_eq = format_gwp_eq_vehicle(impacts.gwp)
            render_equivalent(
                value=f"{thermic_vehicle_eq.magnitude:.1f} {thermic_vehicle_eq.units}",
                emoji="🏎️",
                name="with a thermic vehicle",
                text="(based on GHG emissions)",
            )


def display_equivalent_adpe(impacts, type=EquivalentType.NVIDIA):
    with st.container(border=True):
        if type == EquivalentType.NVIDIA:
            nvdia_eq = format_adpe_eq_nvidia(impacts.adpe)
            render_equivalent(
                value=f"{int(nvdia_eq.magnitude):,}",
                emoji="🕹️",
                name="NVIDIA H100",
                text="(based on metals & minerals use)",
            )

        elif type == EquivalentType.IPHONE:
            iphone_eq = format_adpe_eq_iphone(impacts.adpe)
            render_equivalent(
                value=f"{int(iphone_eq.magnitude):,}",
                emoji="📱",
                name="Iphones",
                text="(based on metals & minerals use)",
            )


def display_equivalent_wcf(impacts, type=EquivalentType.POOL):
    with st.container(border=True):
        if type == EquivalentType.POOL:
            pool_eq = format_wue_eq_pools(impacts.wcf)
            render_equivalent(
                value=f"{int(pool_eq.magnitude):,}",
                emoji="🏊🏼‍♂️",
                name="Olympic pools",
                text="(based on water use)",
            )
        elif type == EquivalentType.DROP:
            drop_eq = format_wue_eq_drops(impacts.wcf)
            render_equivalent(
                value=f"{int(drop_eq.magnitude):,}",
                emoji="💦",
                name="Rain drops",
                text="(based on water use)",
            )
        elif type == EquivalentType.PINTS:
            pint_eq = format_wue_eq_pints(impacts.wcf)
            render_equivalent(
                value=f"{int(pint_eq.magnitude):,}",
                emoji="🍺",
                name="pints of content",
                text="(based on water use)",
            )


def display_equivalents(impacts, how="at_scale"):
    st.markdown(
        f"{EQ_KPIS[how]['title']}",
        unsafe_allow_html=True,
        help=f"{EQ_KPIS[how]['help']}",
    )
    st.space()

    if how == "at_scale":
        col_eq_energy, col_eq_ghg, col_eq_water, col_eq_adpe = st.columns(4)
        with col_eq_adpe:
            display_equivalent_adpe(impacts, type=EQ_KPIS[how]["adpe"])
    else:
        col_eq_energy, col_eq_ghg, col_eq_water = st.columns(3)

    with col_eq_energy:
        display_equivalent_energy(impacts, type=EQ_KPIS[how]["energy"])
    with col_eq_ghg:
        display_equivalent_ghg(impacts, type=EQ_KPIS[how]["ghg"])
    with col_eq_water:
        display_equivalent_wcf(impacts, type=EQ_KPIS[how]["wcf"])
