import streamlit as st

from ecologits.tracers.utils import llm_impacts

from src.config.constants import PROMPTS
from src.config.content import (
    HOW_TO_TEXT,
)
from src.core.formatting import format_impacts
from src.core.latency_estimator import latency_estimator
from src.repositories.models import load_models
from src.ui.components import display_model_warnings, render_model_selector
from src.ui.impacts import display_impacts


def calculator_mode():
    st.expander("How to use this calculator?", expanded=False).markdown(HOW_TO_TEXT)

    with st.container(border=True):
        df = load_models(filter_main=True)

        col1, col2, col3 = st.columns(3)

        provider, model = render_model_selector(df, col1, col2, key_suffix="calc")

        with col3:
            output_tokens = st.selectbox(
                label="Example prompt", options=[p.label for p in PROMPTS], index=2
            )

        list_impacts = st.pills(
            label="Impacts to display",
            options=[
                "Electricity",
                "Carbon Footprint",
                "Water",
                "Metals & Minerals",
                "Fossile Fuels",
            ],
            selection_mode="multi",
            default=["Electricity", "Carbon Footprint", "Water"],
            width="stretch",
        )

        # WARNING DISPLAY
        provider_raw = df[(df["provider_clean"] == provider) & (df["name_clean"] == model)][
            "provider"
        ].values[0]
        model_raw = df[(df["provider_clean"] == provider) & (df["name_clean"] == model)][
            "name"
        ].values[0]

        output_tokens_count = next(p.output_tokens for p in PROMPTS if p.label == output_tokens)

        estimated_latency = latency_estimator.estimate(
            provider=provider_raw,
            model_name=model_raw,
            output_tokens=output_tokens_count,
        )
        impacts = llm_impacts(
            provider=provider_raw,
            model_name=model_raw,
            output_token_count=output_tokens_count,
            request_latency=estimated_latency,
        )

        display_model_warnings(impacts)

        impacts_formatted, _, _ = format_impacts(impacts)

        # st.write(impacts)

        st.markdown(
            '<h3 align = "center">Environmental impacts</h3>',
            unsafe_allow_html=True,
        )
        display_impacts(impacts_output=impacts_formatted, impacts_to_display=list_impacts)
