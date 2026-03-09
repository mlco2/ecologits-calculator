import math

import pandas as pd

from src.config.constants import COUNTRY_CODES

COL_PROVIDER = "Provider"
COL_MODEL = "Model"
COL_LOCATION = "Usage Location"
COL_TOKENS = "Tokens Usage"
COL_NEW_PROVIDER = "New Provider"
COL_NEW_MODEL = "New Model"
COL_NEW_LOCATION = "New Usage Location"

COL_DIFF_GWP = "Δ GWP"
COL_DIFF_ADPE = "Δ ADPe"
COL_DIFF_PE = "Δ PE"
COL_DIFF_WCF = "Δ WCF"
DIFF_COLS = [COL_DIFF_GWP, COL_DIFF_ADPE, COL_DIFF_PE, COL_DIFF_WCF]

LOCATION_LABELS = [label for label, _ in COUNTRY_CODES]
LOCATION_LABEL_TO_CODE = dict(COUNTRY_CODES)
DEFAULT_LOCATION = LOCATION_LABELS[0]  # "🌎 World"

COMPARISON_EMPTY_ROW = {
    COL_PROVIDER: None,
    COL_MODEL: None,
    COL_LOCATION: None,
    COL_TOKENS: None,
    COL_NEW_PROVIDER: None,
    COL_NEW_MODEL: None,
    COL_NEW_LOCATION: None,
}
EMPTY_DIFFS: dict[str, str] = dict.fromkeys(DIFF_COLS, "")

def build_provider_models_map(df: pd.DataFrame) -> dict[str, list[str]]:
    """Build a mapping of provider → sorted list of model names."""
    return {
        provider: sorted(group["name_clean"].unique().tolist())
        for provider, group in df.groupby("provider_clean")
    }


def is_empty(value: object) -> bool:
    """Return True for None, empty string, zero, or NaN."""
    if value is None or value == "":
        return True
    try:
        return math.isnan(float(value))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False
