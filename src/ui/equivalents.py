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
    format_adpe_eq_nvidia,
    format_wue_eq_pools,
    format_wue_eq_drops
)

eq_kpis = {
    "at_scale":{
        "title": "<h3 align='center'>What if 1% of the planet does the same everyday for 1 year ?</h3>",
        "help": "1% of 8 billion people x 365 days",
        "energy": "EPROD",
        "ghg": "PLANE",
        "water": "POOL",
        "adpe": "NVIDIA"
    },
    "unit":{
        "title": "<h3 align='center'>Request Equivalents</h3><p align='center'>Even if these equivalents might look small, it's all about the scale !</p>",
        "help": "Unit equivalents only for the selected usage",
        "energy": "EV",
        "ghg": "STREAMING",
        "water": "DROP",
        "adpe": "IPHONE"
    },
}

def display_equivalents(impacts, how = "at_scale"):

    st.markdown(
        f'{eq_kpis[how]["title"]}',
        unsafe_allow_html=True,
        help=f"{eq_kpis[how]["help"]}",
        #width="content"
    )

    st.space()

    col_eq_energy, col_eq_ghg, col_eq_water, col_eq_adpe = st.columns(4)

    with col_eq_energy:
        display_equivalent_energy(impacts, type=eq_kpis[how]["energy"])
    with col_eq_ghg:
        display_equivalent_ghg(impacts, type=eq_kpis[how]["ghg"])
    with col_eq_water:
        display_equivalent_wue(impacts, type=eq_kpis[how]["water"])
    with col_eq_adpe:
        display_equivalent_adpe(impacts, type=eq_kpis[how]["adpe"])


def render_equivalent(value, emoji = "", name = "", text = ""):

    st.markdown(
        f'<h2 align="center">{value}</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h4 align="center">{emoji} {name}</h4>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p align="center">{text}</p>', unsafe_allow_html=True)


def display_equivalent_energy(impacts, type = "EV"):

    with st.container(border=True):

        if type == "EV":
            ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
            render_equivalent(
                value=f"{ev_eq.magnitude:.2f} {ev_eq.units}",
                emoji="🔋",
                name="with an electric vehicle",
                text="(based on electricity consumption)"
            )

        elif type == "SPORT":
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
                value=f"{distance.magnitude:.3g} <i>{distance.units} </p>",
                name = physical_activity,
            )

        elif type == "EPROD":
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
                text="(yearly energy production)"
            )

        elif type == "ECONS":
            ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
            st.markdown(
                f'<h4 align="center">⚡️ 🇮🇪 {ireland_count.magnitude:.3f} x Ireland </h4>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p align="center">Yearly electricity consumption</p>',
                unsafe_allow_html=True,
            )


def display_equivalent_ghg(impacts, type = "PLANE"):

    with st.container(border=True):

        if type == "STREAMING":
            streaming_eq = format_gwp_eq_streaming(impacts.gwp)
            render_equivalent(
                value=f"{streaming_eq.magnitude:.2f} {streaming_eq.units}",
                emoji="⏯️",
                name="streaming videos",
                text="(based on GHG emissions)"
            )

        elif type == "PLANE":
            paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc(impacts.gwp)
            render_equivalent(
                value=f"{int(paris_nyc_airplane.magnitude):,}",
                emoji="✈️",
                name="Paris ↔ NYC",
                text="(based on GHG emissions)"
            )


def display_equivalent_adpe(impacts, type = "NVIDIA"):

    with st.container(border=True):

        if type == "NVIDIA":
            nvdia_eq = format_adpe_eq_nvidia(impacts.adpe)
            render_equivalent(
                value=f"{int(nvdia_eq.magnitude):,}",
                emoji="🕹️",
                name="NVIDIA H100",
                text="(based on metals & minerals use)"
            )


def display_equivalent_wue(impacts, type = "POOL"):

    with st.container(border=True):

        if type == "POOL":
            pool_eq = format_wue_eq_pools(impacts.wcf)
            render_equivalent(
                value=f"{int(pool_eq.magnitude):,}",
                emoji="🏊🏼‍♂️",
                name="Olympic pools",
                text="(based on water use)"
            )

        if type == "DROP":
            pool_eq = format_wue_eq_drops(impacts.wcf)
            render_equivalent(
                value=f"{int(pool_eq.magnitude):,}",
                emoji="💦",
                name="Rain drops",
                text="(based on water use)"
            )
