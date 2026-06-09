import streamlit as st

from ecologits.tracers.utils import llm_impacts

from src.config.constants import PROMPTS
from src.config.content import (
    HOW_TO_TEXT,
)
from src.core.formatting import format_impacts
from src.repositories.models import get_raw_model_names, load_models
from src.ui.components import display_model_warnings, render_model_selector
from src.ui.equivalents import (
    display_equivalents,
)
from src.ui.impacts import display_impacts


def calculator_mode():
    st.expander("How to use this calculator?", expanded=False).markdown(HOW_TO_TEXT)

    with st.container(border=True):
        # st.markdown('<h3 align="center">Calculator</h3>', unsafe_allow_html=True)
        df = load_models(filter_main=True)

        col1, col2, col3 = st.columns(3)

        provider, model = render_model_selector(df, col1, col2, key_suffix="calc")

        with col3:
            output_tokens = st.selectbox(
                label="Usage scenario", options=[p.label for p in PROMPTS], index=3
            )

        # Display only electricity, carbon footprint, water, and minerals
        list_impacts = ["Electricity", "Carbon Footprint", "Water", "Metals & Minerals"]

        # WARNING DISPLAY
        raw_names = get_raw_model_names(df, provider, model)
        if raw_names is None:
            st.error("Selected model not found. Please select a different model.")
            return
        provider_raw, model_raw = raw_names

        output_tokens_count = next(p.output_tokens for p in PROMPTS if p.label == output_tokens)

        # estimated_latency = latency_estimator.estimate(
        #     provider=provider_raw,
        #     model_name=model_raw,
        #     output_tokens=output_tokens_count,
        #
        impacts = llm_impacts(
            provider=provider_raw,
            model_name=model_raw,
            output_token_count=output_tokens_count,
            request_latency=float("inf"),
        )

        if impacts.warnings:
            display_model_warnings(impacts)

        impacts_formatted, _, _ = format_impacts(impacts)

        # st.write(impacts)

        st.markdown(
            '<h3 align = "center">Environmental impacts</h3>',
            unsafe_allow_html=True,
        )
        display_impacts(
            impacts_output=impacts_formatted, impacts_to_display=list_impacts, mode="basic"
        )

        with st.container(border=True):
            st.session_state.impacts_at_scale = True
            st.session_state.impacts_at_scale = st.toggle(
                label="Display impacts at scale",
                value=st.session_state.impacts_at_scale,
                help="The scale we implemented is a daily replication of the given usage by 1% of the world population.",
            )
            if st.session_state.impacts_at_scale:
                display_equivalents(impacts_formatted, how="at_scale")
            else:
                display_equivalents(impacts_formatted, how="unit")
