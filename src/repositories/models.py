import pandas as pd
import streamlit as st

from ecologits.model_repository import ArchitectureTypes
from ecologits.model_repository import models as model_repository
from ecologits.status_messages import (
    ModelArchMultimodalWarning,
    ModelArchNotReleasedWarning,
)
from ecologits.utils.range_value import RangeValue

from src.repositories.model_config import load_main_models

PROVIDERS_FORMAT = {
    "anthropic": "Anthropic",
    "cohere": "Cohere",
    "google_genai": "Google",
    "mistralai": "Mistral AI",
    "openai": "OpenAI",
}


def clean_model_name(model_name: str) -> str:
    # Define a mapping of characters to replace
    replacements = {
        "latest": "",
        "-": " ",
        "_": " ",
        "preview": "",
    }

    # Apply replacements using a loop
    for old, new in replacements.items():
        model_name = model_name.replace(old, new)

    # Join and split to handle multiple spaces
    return " ".join(model_name.split())


@st.cache_data
def load_models(filter_main=True) -> pd.DataFrame:
    data = []
    # Load main models list (will be cached)
    main_models = load_main_models() if filter_main else None

    for m in model_repository.list_models():
        if filter_main and m.name not in main_models:
            continue  # Ignore "not main" models when filter is enabled

        if m.architecture.type == ArchitectureTypes.DENSE:
            if isinstance(m.architecture.parameters, RangeValue):
                total_parameters = dict(m.architecture.parameters)
            else:
                total_parameters = m.architecture.parameters
            active_parameters = total_parameters

        elif m.architecture.type == ArchitectureTypes.MOE:
            # Handle ParametersMoE objects
            if hasattr(m.architecture.parameters, "total") and hasattr(
                m.architecture.parameters, "active"
            ):
                # This is a ParametersMoE object
                total_param = m.architecture.parameters.total
                active_param = m.architecture.parameters.active

                if isinstance(total_param, RangeValue):
                    total_parameters = dict(total_param)
                else:
                    total_parameters = total_param

                if isinstance(active_param, RangeValue):
                    active_parameters = dict(active_param)
                else:
                    active_parameters = active_param
            else:
                # This is a simple number (int/float)
                if isinstance(m.architecture.parameters, RangeValue):
                    total_parameters = dict(m.architecture.parameters)
                else:
                    total_parameters = m.architecture.parameters
                active_parameters = total_parameters

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
