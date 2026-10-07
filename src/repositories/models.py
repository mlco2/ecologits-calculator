import re

import pandas as pd
import streamlit as st

from ecologits.model_repository import ArchitectureTypes
from ecologits.model_repository import models as model_repository
from ecologits.utils.range_value import RangeValue

from src.repositories.model_config import load_main_models, load_model_aliases

PROVIDERS_FORMAT = {
    "anthropic": "Anthropic",
    "cohere": "Cohere",
    "google_genai": "Google",
    "mistralai": "Mistral AI",
    "openai": "OpenAI",
}


def normalize_params(params):
    return dict(params) if isinstance(params, RangeValue) else params


def clean_model_name(model_name: str) -> str:
    # Define a mapping of characters to replace
    replacements = {
        "latest": "",
        "-": " ",
        "_": " ",
        "preview": "",
    }

    for old, new in replacements.items():
        model_name = model_name.replace(old, new)
    model_name = re.sub(r"\d{8}", "", model_name)
    # Strip trailing date-like version suffixes (e.g. Mistral 2512, 2604,
    # Cohere 03 2025): "MM YYYY" then standalone "YYYY"/"YYMM".
    model_name = re.sub(r"\s\d{2}\s\d{4}\s*$", "", model_name)
    model_name = re.sub(r"\s\d{4}\s*$", "", model_name)
    return " ".join(model_name.split())


@st.cache_data
def load_models(filter_main=True) -> pd.DataFrame:
    data = []
    # Load main models list (will be cached)
    main_models = load_main_models() if filter_main else None
    model_order = {name: index for index, name in enumerate(main_models or [])}
    # Display aliases from models_recent.json: raw name -> alias.
    # Applies in all modes so expert mode stays consistent.
    aliases = load_model_aliases()

    for m in model_repository.list_models():
        if filter_main and m.name not in main_models:
            continue  # Ignore "not main" models when filter is enabled

        if m.architecture.type == ArchitectureTypes.DENSE:
            total_parameters = normalize_params(m.architecture.parameters)
            active_parameters = total_parameters

        elif m.architecture.type == ArchitectureTypes.MOE:
            params = m.architecture.parameters
            if hasattr(params, "total") and hasattr(params, "active"):
                total_parameters = normalize_params(params.total)
                active_parameters = normalize_params(params.active)
            else:
                total_parameters = normalize_params(params)
                active_parameters = total_parameters

        else:
            continue  # Ignore model

        data.append(
            {
                "provider": m.provider.value,
                "provider_clean": PROVIDERS_FORMAT.get(m.provider.value, m.provider.value),
                "name": m.name,
                "name_clean": aliases.get(m.name, clean_model_name(m.name)),
                "total_parameters": total_parameters,
                "active_parameters": active_parameters,
                "tps": m.deployment.tps,
                "ttft": m.deployment.ttft,
            }
        )

    if filter_main:
        data.sort(key=lambda model: model_order[model["name"]])

    return pd.DataFrame(data)


def get_raw_model_names(
    df: pd.DataFrame, provider_clean: str, model_clean: str
) -> tuple[str, str] | None:
    """Extract raw provider and model names from filtered models dataframe.

    Args:
        df: DataFrame with model data containing 'provider_clean', 'name_clean',
            'provider', and 'name' columns.
        provider_clean: The cleaned provider name to search for.
        model_clean: The cleaned model name to search for.

    Returns:
        Tuple of (provider_raw, model_raw) if found, None otherwise.
    """
    df_filtered = df[(df["provider_clean"] == provider_clean) & (df["name_clean"] == model_clean)]
    if df_filtered.empty:
        return None
    return df_filtered["provider"].iloc[0], df_filtered["name"].iloc[0]
