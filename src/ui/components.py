import pandas as pd
import streamlit as st

from src.config.content import (
    WARNING_BOTH,
    WARNING_CLOSED_SOURCE,
    WARNING_MULTI_MODAL,
)


def render_model_selector(
    df: pd.DataFrame, col_provider, col_model, key_suffix: str = ""
) -> tuple[str, str]:
    with col_provider:
        providers_clean = sorted(df["provider_clean"].unique())
        # Default to OpenAI if available
        default_index = providers_clean.index("OpenAI") if "OpenAI" in providers_clean else 0

        provider = st.selectbox(
            label="Provider",
            options=providers_clean,
            index=default_index,
            key=f"provider_select_{key_suffix}",
        )

    with col_model:
        models_clean = sorted(
            [
                x
                for x in df["name_clean"].unique()
                if x in df[df["provider_clean"] == provider]["name_clean"].unique()
            ]
        )
        model = st.selectbox(label="Model", options=models_clean, key=f"model_select_{key_suffix}")

    return provider, model


def display_model_warnings(impacts) -> None:
    """Display warning messages based on model characteristics."""
    
    if len(impacts.warnings) == 1:
        st.warning(impacts.warnings[0].message, icon="⚠️")
    elif len(impacts.warnings) == 2:
        st.warning(
            f"{impacts.warnings[0].message.split(',')[0]} and {impacts.warnings[1].message.split(',')[0].lower()}, {impacts.warnings[0].message.split(',')[1]}",
            icon="⚠️"
        )