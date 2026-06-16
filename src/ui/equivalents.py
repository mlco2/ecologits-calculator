import streamlit as st

from src.core.equivalences import (
    EQ_KPIS,
    EnergyProduction,
    EquivalentType,
    PhysicalActivity,
    format_adpe_eq_iphone,
    format_adpe_eq_nvidia,
    format_energy_eq_electric_vehicle,
    format_energy_eq_electricity_consumption_ireland,
    format_energy_eq_electricity_production,
    format_energy_eq_physical_activity,
    format_gwp_eq_airplane_paris_nyc,
    format_gwp_eq_streaming,
    format_gwp_eq_vehicle,
    format_wue_eq_drops,
    format_wue_eq_pints,
    format_wue_eq_pools,
)
from src.ui.components import render_environment_card

EQUIVALENT_TITLES = {
    "at_scale": {
        "title": "What if 1% of the planet does the same everyday for 1 year?",
        "subtitle": "",
    },
    "unit": {
        "title": "Equivalents for the environment",
        "subtitle": "Even if these equivalents might look small, it's all about the scale!",
    },
    "company": {
        "title": "Equivalents for the environment",
        "subtitle": "",
    },
}


def render_equivalents_title(how="at_scale") -> None:
    title = EQUIVALENT_TITLES[how]["title"]
    subtitle = EQUIVALENT_TITLES[how]["subtitle"]
    description = EQ_KPIS[how]["help"]
    subtitle_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""

    st.markdown(
        f"""
        <h3 class="section-title section-title-equivalents">{title}</h3>
        <p class="section-description">{description}</p>
        {subtitle_html}
        """,
        unsafe_allow_html=True,
    )


def render_equivalent(value, unit="", emoji="", name="", text=""):
    render_environment_card(
        title=name,
        value=value,
        unit=unit,
        emoji=emoji,
        subtext=text,
    )


def display_equivalent_energy(impacts, type=EquivalentType.EV, how="unit"):
    if type == EquivalentType.EV:
        ev_eq = format_energy_eq_electric_vehicle(impacts.energy)
        render_equivalent(
            value=f"{ev_eq.magnitude:.1f}",
            unit=f"{ev_eq.units:~}",
            emoji="🔋",
            name="with an electric vehicle",
            text="based on electricity consumption",
        )

    elif type == EquivalentType.SPORT:
        physical_activity, distance = format_energy_eq_physical_activity(impacts.energy)
        if physical_activity == PhysicalActivity.WALKING:
            emoji = "🚶"
        elif physical_activity == PhysicalActivity.RUNNING:
            emoji = "🏃"
        else:
            emoji = ""
        render_equivalent(
            value=f"≈ {distance.magnitude:.3g}",
            unit=f"{distance.units:~}",
            emoji=emoji,
            name=physical_activity.capitalize(),
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
            text="yearly energy production",
        )

    elif type == EquivalentType.ECONS:
        ireland_count = format_energy_eq_electricity_consumption_ireland(impacts.energy)
        render_equivalent(
            value=f"{ireland_count.magnitude:.3f}",
            unit="x Ireland",
            emoji="⚡️ 🇮🇪",
            name="Yearly electricity consumption",
        )


def display_equivalent_ghg(impacts, type=EquivalentType.PLANE):
    if type == EquivalentType.STREAMING:
        streaming_eq = format_gwp_eq_streaming(impacts.gwp)
        render_equivalent(
            value=f"{streaming_eq.magnitude:.2f}",
            unit=f"{streaming_eq.units:~}",
            emoji="⏯️",
            name="streaming videos",
            text="based on GHG emissions",
        )
    elif type == EquivalentType.PLANE:
        paris_nyc_airplane = format_gwp_eq_airplane_paris_nyc(impacts.gwp)
        render_equivalent(
            value=f"{int(paris_nyc_airplane.magnitude):,}",
            emoji="✈️",
            name="Paris ↔ NYC",
            text="based on GHG emissions",
        )
    elif type == EquivalentType.THERMIC_VEHICLE:
        thermic_vehicle_eq = format_gwp_eq_vehicle(impacts.gwp)
        render_equivalent(
            value=f"{thermic_vehicle_eq.magnitude:.1f}",
            unit=f"{thermic_vehicle_eq.units:~}",
            emoji="🏎️",
            name="with a thermic vehicle",
            text="based on GHG emissions",
        )


def display_equivalent_adpe(impacts, type=EquivalentType.NVIDIA):
    if type == EquivalentType.NVIDIA:
        nvdia_eq = format_adpe_eq_nvidia(impacts.adpe)
        render_equivalent(
            value=f"{int(nvdia_eq.magnitude):,}",
            emoji="🕹️",
            name="NVIDIA H100",
            text="based on metals & minerals use",
        )

    elif type == EquivalentType.IPHONE:
        iphone_eq = format_adpe_eq_iphone(impacts.adpe)
        render_equivalent(
            value=f"{int(iphone_eq.magnitude):,}",
            emoji="📱",
            name="Iphones",
            text="based on metals & minerals use",
        )


def display_equivalent_wcf(impacts, type=EquivalentType.POOL):
    if type == EquivalentType.POOL:
        pool_eq = format_wue_eq_pools(impacts.wcf)
        render_equivalent(
            value=f"{int(pool_eq.magnitude):,}",
            emoji="🏊🏼‍♂️",
            name="Olympic pools",
            text="based on water use",
        )
    elif type == EquivalentType.DROP:
        drop_eq = format_wue_eq_drops(impacts.wcf)
        render_equivalent(
            value=f"{int(drop_eq.magnitude):,}",
            emoji="💦",
            name="Rain drops",
            text="based on water use",
        )
    elif type == EquivalentType.PINTS:
        pint_eq = format_wue_eq_pints(impacts.wcf)
        render_equivalent(
            value=f"{int(pint_eq.magnitude):,}",
            emoji="🍺",
            name="pints of content",
            text="based on water use",
        )


def display_equivalents(impacts, how="at_scale", show_title=True):
    if show_title:
        render_equivalents_title(how)

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
