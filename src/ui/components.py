import streamlit as st
import pandas as pd
from src.config.content import (
    WARNING_CLOSED_SOURCE,
    WARNING_MULTI_MODAL,
    WARNING_BOTH,
)


def render_model_selector(
    df: pd.DataFrame, col_provider, col_model, key_suffix: str = ""
) -> tuple[str, str]:
    with col_provider:
        providers_clean = sorted([x for x in df["provider_clean"].unique()])
        # Default to OpenAI if available
        default_index = (
            providers_clean.index("OpenAI") if "OpenAI" in providers_clean else 0
        )

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
        model = st.selectbox(
            label="Model", options=models_clean, key=f"model_select_{key_suffix}"
        )

    return provider, model


def display_model_warnings(df: pd.DataFrame, provider: str, model: str) -> None:
    """Display warning messages based on model characteristics."""
    df_filtered = df[
        (df["provider_clean"] == provider) & (df["name_clean"] == model)
    ]

    if (
        df_filtered["warning_arch"].values[0]
        and not df_filtered["warning_multi_modal"].values[0]
    ):
        st.warning(WARNING_CLOSED_SOURCE, icon="⚠️")
    if (
        df_filtered["warning_multi_modal"].values[0]
        and not df_filtered["warning_arch"].values[0]
    ):
        st.warning(WARNING_MULTI_MODAL, icon="⚠️")
    if (
        df_filtered["warning_arch"].values[0]
        and df_filtered["warning_multi_modal"].values[0]
    ):
        st.warning(WARNING_BOTH, icon="⚠️")
