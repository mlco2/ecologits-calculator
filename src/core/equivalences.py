from enum import Enum

from pint import Quantity

from src.core.units import q


class PhysicalActivity(str, Enum):
    RUNNING = "running"
    WALKING = "walking"


class EnergyProduction(str, Enum):
    NUCLEAR = "nuclear"
    WIND = "wind"


# From https://www.runningtools.com/energyusage.htm
RUNNING_ENERGY_EQ = q("294 kJ / km")  # running 1 km at 10 km/h with a weight of 70 kg
WALKING_ENERGY_EQ = q("196 kJ / km")  # walking 1 km at 3 km/h with a weight of 70 kg

# From https://selectra.info/energie/actualites/insolite/consommation-vehicules-electriques-france-2040
# and https://www.tesla.com/fr_fr/support/power-consumption
EV_ENERGY_EQ = q("0.17 kWh / km")

# From https://impactco2.fr/outils/comparateur?value=1&comparisons=streamingvideo
STREAMING_GWP_EQ = q("15.6 h / kgCO2eq")

# From https://ourworldindata.org/population-growth
ONE_PERCENT_WORLD_POPULATION = 80_000_000

DAYS_IN_YEAR = 365

# For a 900 MW nuclear plant -> 500 000 MWh / month
# From https://www.edf.fr/groupe-edf/espaces-dedies/jeunes-enseignants/pour-les-jeunes/lenergie-de-a-a-z/produire-de-lelectricite/le-nucleaire-en-chiffres
YEARLY_NUCLEAR_ENERGY_EQ = q("6 TWh")

# For a 2MW wind turbine
# https://www.ecologie.gouv.fr/eolien-terrestre
YEARLY_WIND_ENERGY_EQ = q("4.2 GWh")

# Ireland yearly electricity consumption
# From https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption
YEARLY_IRELAND_ELECTRICITY_CONSUMPTION = q("33 TWh")
IRELAND_POPULATION_MILLION = 5

# From https://impactco2.fr/outils/comparateur?value=1&comparisons=&equivalent=avion-pny
# 1.77t for one passenger (round-trip) x 100 passenger
AIRPLANE_PARIS_NYC_GWP_EQ = q("177000 kgCO2eq")


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


def format_energy_eq_electricity_production(
    energy: Quantity,
) -> tuple[EnergyProduction, Quantity]:
    electricity_eq = energy * ONE_PERCENT_WORLD_POPULATION * DAYS_IN_YEAR
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
