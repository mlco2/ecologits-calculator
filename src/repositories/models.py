import pandas as pd
import streamlit as st

from ecologits.model_repository import ArchitectureTypes
from ecologits.model_repository import models as model_repository
from ecologits.status_messages import (
    ModelArchMultimodalWarning,
    ModelArchNotReleasedWarning,
)
from ecologits.utils.range_value import RangeValue

from src.config.constants import MAIN_MODELS

PROVIDERS_FORMAT = {
    "anthropic": "Anthropic",
    "cohere": "Cohere",
    "google_genai": "Google",
    "mistralai": "Mistral AI",
    "openai": "OpenAI",
}


def clean_model_name(model_name: str) -> str:
    model_name = model_name.replace("latest", "")
    model_name = model_name.replace("-", " ")
    model_name = model_name.replace("_", " ")
    return model_name


@st.cache_data
def load_models(filter_main=True) -> pd.DataFrame:
    data = []
    for m in model_repository.list_models():
        if filter_main and m.name not in MAIN_MODELS:
            continue  # Ignore "not main" models when filter is enabled

        if m.architecture.type == ArchitectureTypes.DENSE:
            if isinstance(m.architecture.parameters, RangeValue):
                total_parameters = dict(m.architecture.parameters)
            else:
                total_parameters = m.architecture.parameters
            active_parameters = total_parameters

        elif m.architecture.type == ArchitectureTypes.MOE:
            if isinstance(m.architecture.parameters.total, RangeValue):
                total_parameters = dict(m.architecture.parameters.total)
            else:
                total_parameters = m.architecture.parameters.total

            if isinstance(m.architecture.parameters.active, RangeValue):
                active_parameters = dict(m.architecture.parameters.active)
            else:
                active_parameters = m.architecture.parameters.active

        else:
            continue  # Ignore model

        warning_arch = False
        warning_multi_modal = False
        for w in m.warnings:
            if isinstance(w, ModelArchNotReleasedWarning):
                warning_arch = True
            if isinstance(w, ModelArchMultimodalWarning):
                warning_multi_modal = True

        data.append(
            {
                "provider": m.provider.value,
                "provider_clean": PROVIDERS_FORMAT.get(m.provider.value, m.provider.value),
                "name": m.name,
                "name_clean": clean_model_name(m.name),
                "architecture_type": m.architecture.type.value,
                "total_parameters": total_parameters,
                "active_parameters": active_parameters,
                "tps": m.deployment.tps,
                "ttft": m.deployment.ttft,
                "warning_arch": warning_arch,
                "warning_multi_modal": warning_multi_modal,
            }
        )

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
