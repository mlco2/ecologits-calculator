from src.config.models import PromptTemplate
from src.core.units import q

PROMPTS = [
    PromptTemplate("Write a tweet", 50, 50, 0),
    PromptTemplate("Write an email", 170, 170, 0),
    PromptTemplate("Write an article summary", 250, 2000, 0),
    PromptTemplate("Small conversation with a chatbot", 400, 400, 2000),
    PromptTemplate("Write a 5-page report", 5000, 10000, 100),
    PromptTemplate("Assist application development", 100000, 1000000, 10000000),
    PromptTemplate("Re-write the Lord Of The Rings trilogy", 500000, 500000, 500000),
]

USAGE_INTENSITY = {
    "Light (x1-x3)": 2,
    "Medium (x4-x10)": 7,
    "Large (x11-x25)": 18,
    "XLarge (x26+)": 30,
}

TIME_HORIZONS = {
    "Daily": 1,
    "Weekly": 5,
    "Monthly": 22,
    "Yearly": 260,
}

MODEL_REPOSITORY_URL = (
    "https://raw.githubusercontent.com/mlco2/ecologits/refs/heads/main/ecologits/data/models.json"
)


COUNTRY_CODES = [
    ("🌎 World", "WOR"),
    ("🇦🇺 Australia", "AUS"),
    ("🇦🇹 Austria", "AUT"),
    ("🇦🇷 Argentina", "ARG"),
    ("🇧🇪 Belgium", "BEL"),
    ("🇧🇬 Bulgaria", "BGR"),
    ("🇧🇷 Brazil", "BRA"),
    ("🇨🇦 Canada", "CAN"),
    ("🇨🇭 Switzerland", "CHE"),
    ("🇨🇱 Chile", "CHL"),
    ("🇨🇳 China", "CHN"),
    ("🇨🇾 Cyprus", "CYP"),
    ("🇨🇿 Czech Republic", "CZE"),
    ("🇩🇪 Germany", "DEU"),
    ("🇩🇰 Denmark", "DNK"),
    ("🇪🇸 Spain", "ESP"),
    ("🇪🇪 Estonia", "EST"),
    ("🇫🇮 Finland", "FIN"),
    ("🇫🇷 France", "FRA"),
    ("🇬🇧 United Kingdom", "GBR"),
    ("🇬🇷 Greece", "GRC"),
    ("🇭🇺 Hungary", "HUN"),
    ("🇮🇩 Indonesia", "IDN"),
    ("🇮🇳 India", "IND"),
    ("🇮🇪 Ireland", "IRL"),
    ("🇮🇸 Iceland", "ISL"),
    ("🇮🇹 Italy", "ITA"),
    ("🇯🇵 Japan", "JPN"),
    ("🇰🇷 South Korea", "KOR"),
    ("🇱🇹 Lithuania", "LTU"),
    ("🇱🇺 Luxembourg", "LUX"),
    ("🇱🇻 Latvia", "LVA"),
    ("🇲🇽 Mexico", "MEX"),
    ("🇲🇹 Malta", "MLT"),
    ("🇲🇾 Malaysia", "MYS"),
    ("🇳🇱 Netherlands", "NLD"),
    ("🇳🇴 Norway", "NOR"),
    ("🇳🇿 New Zealand", "NZL"),
    ("🇵🇱 Poland", "POL"),
    ("🇵🇹 Portugal", "PRT"),
    ("🇷🇴 Romania", "ROU"),
    ("🇷🇺 Russian Federation", "RUS"),
    ("🇸🇰 Slovak Republic", "SVK"),
    ("🇸🇮 Slovenia", "SVN"),
    ("🇸🇪 Sweden", "SWE"),
    ("🇺🇦 Ukraine", "UKR"),
    ("🇹🇭 Thailand", "THA"),
    ("🇹🇷 Turkey", "TUR"),
    ("🇹🇼 Taiwan", "TWN"),
    ("🇺🇸 United States", "USA"),
]

# From https://www.runningtools.com/energyusage.htm
RUNNING_ENERGY_EQ = q("294 kJ / km")  # running 1 km at 10 km/h with a weight of 70 kg
WALKING_ENERGY_EQ = q("196 kJ / km")  # walking 1 km at 3 km/h with a weight of 70 kg

# From https://selectra.info/energie/actualites/insolite/consommation-vehicules-electriques-france-2040
# and https://www.tesla.com/fr_fr/support/power-consumption
EV_ENERGY_EQ = q("0.17 kWh / km")

# from https://impactco2.fr/outils/transport/voiturethermique
THERMIC_VEHICLE_GHG_EQ = q("142 gCO2eq / km")

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

# From https://librairie.ademe.fr/economie-circulaire-et-dechets/9103-analyse-de-cycle-de-vie-de-gpu-cartes-graphiques-pour-l-intelligence-artificielle.html
# ADPE for building a NVIDIA H100 80GB = 0.00895 kgSbeq
NVIDIA_H100 = q("8.95 gSbeq")

# https://en.wikipedia.org/wiki/Olympic-size_swimming_pool
# Olympic pool liters
OLYMPIC_POOL = q("2500000 L")

# https://en.wikipedia.org/wiki/Drop_(unit)
# water drop volume
WATER_DROP = q("0.05 mL")

# source : everybody knows :)
BEER_PINT = q("0.5 L")

# source : https://www.mdpi.com/2078-1547/8/2/21
IPHONE = q("2 gSbeq")
