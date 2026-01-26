from __future__ import annotations

from src.config.constants import COUNTRY_CODES

PATH = "src/data/electricity_mix.csv"

CRITERIA = {
    "gwp": "GHG Emission (kg CO2 eq)",
    "adpe": "Abiotic Resources (kg Sb eq)",
    "pe": "Primary Energy (MJ)",
    "wue": "Water Usage Effectiveness (L/kWh)",
}


def format_country_name(code: str) -> str | None:
    for country_name, country_code in COUNTRY_CODES:
        if country_code == code:
            return country_name
    return None


def format_electricity_mix_criterion(criterion: str) -> str | None:
    return CRITERIA.get(criterion)
