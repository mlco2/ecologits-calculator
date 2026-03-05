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
    "Heavy (x11-x25)": 18,
    "Silicon Valley Tech Bro (x26+)": 30,
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

main_models_openai = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "o1",
    "o1-mini",
    "o3-mini",
    "gpt-4.1-nano",
    "gpt-4.1-mini",
    "gpt-4.1",
    "o4-mini",
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-5",
]

main_models_anthropic = [
    "claude-3-5-haiku-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-7-sonnet-latest",
    "claude-opus-4-0",
    "claude-opus-4-1",
    "claude-sonnet-4-0",
    "claude-sonnet-4-5",
    "claude-haiku-4-5",
]

main_models_cohere = [
    "command-a-03-2025",
    "command-r",
    "command-r-08-2024",
    "command-r-plus-08-2024",
    "command-r7b-12-2024",
]

main_models_google = [
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

main_models_mistral = [
    "codestral-latest",
    "devstral-medium-latest",
    "devstral-small-latest",
    "magistral-medium-latest",
    "magistral-small-latest",
    "ministral-3b-latest",
    "ministral-8b-latest",
    "mistral-large-latest",
    "mistral-medium-latest",
    "mistral-small-latest",
    "mistral-tiny-latest",
    "open-mistral-7b",
    "open-mistral-nemo",
    "open-mixtral-8x22b",
    "open-mixtral-8x7b",
]

MAIN_MODELS = (
    main_models_openai
    + main_models_anthropic
    + main_models_cohere
    + main_models_mistral
    + main_models_google
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
