from src.config.models import PromptTemplate

PROMPTS = [
    PromptTemplate("Write a tweet", 50, 50, 0),
    PromptTemplate("Write an email", 170, 170, 0),
    PromptTemplate("Write an article summary", 250, 2000, 0),
    PromptTemplate("Small conversation with a chatbot", 400, 400, 2000),
    PromptTemplate("Write a 5-page report", 5000, 10000, 100),
    PromptTemplate("Write the code for a simple app", 15000, 50000, 100000),
    PromptTemplate("Assist application development", 100000, 1000000, 10000000),
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

# Main models are loaded from models_recent.json by the model_config module

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
