from enum import StrEnum

from pint import Quantity
from src.config.constants import *
from src.core.units import q


class PhysicalActivity(StrEnum):
    RUNNING = "running"
    WALKING = "walking"


class EnergyProduction(StrEnum):
    NUCLEAR = "nuclear"
    WIND = "wind"


from enum import Enum

class EquivalentType(Enum):
    EV = "EV"
    SPORT = "SPORT"
    EPROD = "EPROD"
    ECONS = "ECONS"
    STREAMING = "STREAMING"
    PLANE = "PLANE"
    THERMIC_VEHICLE = "THERMIC_VEHICLE"
    NVIDIA = "NVIDIA"
    POOL = "POOL"
    DROP = "DROP"
    IPHONE = "IPHONE"
    PINTS = "PINTS"

EQ_KPIS = {
    "at_scale": {
        "title": "<h3 align='center'>What if 1% of the planet does the same everyday for 1 year ?</h3>",
        "help": "1% of 8 billion people x 365 days",
        "energy": EquivalentType.EPROD,
        "ghg": EquivalentType.PLANE,
        "wcf": EquivalentType.POOL,
        "adpe": EquivalentType.IPHONE,
    },
    "unit": {
        "title": "<h3 align='center'>Equivalents for the environment</h3><p align='center'>Even if these equivalents might look small, it's all about the scale !</p>",
        "help": "Unit equivalents only for the selected usage",
        "energy": EquivalentType.EV,
        "ghg": EquivalentType.THERMIC_VEHICLE,
        "wcf": EquivalentType.DROP,
        "adpe": EquivalentType.IPHONE,
    },
    "company": {
        "title": "<h4 align='center'>Equivalents for the environment</h4>",
        "help": "Unit equivalents only for the selected usage",
        "energy": EquivalentType.EV,
        "ghg": EquivalentType.THERMIC_VEHICLE,
        "wcf": EquivalentType.PINTS,
        "adpe": EquivalentType.IPHONE,
    },
}


def format_energy_eq_physical_activity(
    energy: Quantity,
) -> tuple[PhysicalActivity, Quantity]:
    energy = energy.to("kJ")
    running_eq = energy / RUNNING_ENERGY_EQ
    if running_eq > q("1 km"):
        return PhysicalActivity.RUNNING, running_eq

    walking_eq = energy / WALKING_ENERGY_EQ
    if walking_eq < q("1 km"):
        walking_eq = walking_eq.to("meter")
    return PhysicalActivity.WALKING, walking_eq


def format_energy_eq_electric_vehicle(energy: Quantity) -> Quantity:
    energy = energy.to("kWh")
    ev_eq = energy / EV_ENERGY_EQ
    if ev_eq < q("1 km"):
        ev_eq = ev_eq.to("meter")
    return ev_eq


def format_gwp_eq_streaming(gwp: Quantity) -> Quantity:
    gwp = gwp.to("kgCO2eq")
    streaming_eq = gwp * STREAMING_GWP_EQ
    if streaming_eq < q("1 h"):
        streaming_eq = streaming_eq.to("min")
    if streaming_eq < q("1 min"):
        streaming_eq = streaming_eq.to("s")
    return streaming_eq


def format_gwp_eq_vehicle(gwp: Quantity) -> Quantity:
    gwp = gwp.to("gCO2eq")
    thermic_vehicle_eq = gwp / THERMIC_VEHICLE_GHG_EQ
    if thermic_vehicle_eq < q("1 km"):
        thermic_vehicle_eq = thermic_vehicle_eq.to("meter")
    return thermic_vehicle_eq


def format_energy_eq_electricity_production(
    energy: Quantity
) -> tuple[EnergyProduction, Quantity]:
    electricity_eq = energy
    electricity_eq = electricity_eq * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    electricity_eq = electricity_eq.to("TWh")
    if electricity_eq > YEARLY_NUCLEAR_ENERGY_EQ:
        return EnergyProduction.NUCLEAR, electricity_eq / YEARLY_NUCLEAR_ENERGY_EQ
    electricity_eq = electricity_eq.to("GWh")
    return EnergyProduction.WIND, electricity_eq / YEARLY_WIND_ENERGY_EQ


def format_energy_eq_electricity_consumption_ireland(energy: Quantity) -> Quantity:
    electricity_eq = energy * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    electricity_eq = electricity_eq.to("TWh")
    return electricity_eq / YEARLY_IRELAND_ELECTRICITY_CONSUMPTION


def format_gwp_eq_airplane_paris_nyc(gwp: Quantity) -> Quantity:
    gwp_eq = gwp * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    gwp_eq = gwp_eq.to("kgCO2eq")
    return gwp_eq / AIRPLANE_PARIS_NYC_GWP_EQ


def format_adpe_eq_nvidia(adpe: Quantity) -> Quantity:
    adpe_eq = adpe * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    adpe_eq = adpe_eq.to("gSbeq")
    return adpe_eq / NVIDIA_H100


def format_adpe_eq_iphone(adpe: Quantity) -> Quantity:
    adpe_eq = adpe * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    adpe_eq = adpe_eq.to("gSbeq")
    return adpe_eq / IPHONE


def format_wue_eq_pools(wcf: Quantity) -> Quantity:
    wue_eq = wcf * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
    wue_eq = wue_eq.to("L")
    return wue_eq / OLYMPIC_POOL


def format_wue_eq_drops(wcf: Quantity) -> Quantity:
    wue_eq = wcf.to("mL")
    return wue_eq / WATER_DROP


def format_wue_eq_pints(wcf: Quantity) -> Quantity:
    wue_eq = wcf.to("L")
    return wue_eq / BEER_PINT