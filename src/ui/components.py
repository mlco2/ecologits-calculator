import streamlit as st
import pandas as pd


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
