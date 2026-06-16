import streamlit as st

from src.config.scenarios import SCENARIOS, Scenario
from src.core.formatting import format_impacts
from src.core.impact_calculator import compute_scenario_impacts
from src.repositories.models import get_raw_model_names, load_models
from src.repositories.video_models import load_video_models
from src.ui.components import display_model_warnings, render_model_selector
from src.ui.equivalents import (
    display_equivalents,
)
from src.ui.impacts import display_impacts


def _render_scenario_selector() -> Scenario:
    scenario_label = st.selectbox(
        label="Task",
        options=[scenario.label for scenario in SCENARIOS],
        index=0,
    )
    return next(scenario for scenario in SCENARIOS if scenario.label == scenario_label)


def _load_compatible_models(scenario: Scenario):
    if scenario.modality == "video":
        return load_video_models(resolution=scenario.resolution)
    return load_models(filter_main=True)


def _render_scenario_context(scenario: Scenario) -> None:
    if scenario.modality == "video":
        st.caption(
            f"{scenario.resolution}, {scenario.duration}s"
            + (" with audio" if scenario.with_audio else "")
        )
    elif scenario.output_token_count is not None:
        st.caption(f"{scenario.output_token_count:,} output tokens")


def calculator_mode():
    with st.container(border=True):
        # st.markdown('<h3 align="center">Calculator</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            scenario = _render_scenario_selector()
            _render_scenario_context(scenario)

        df = _load_compatible_models(scenario)

        provider, model = render_model_selector(df, col2, col3, key_suffix="calc")

        # Display only electricity, carbon footprint, water, and minerals
        list_impacts = ["Electricity", "Carbon Footprint", "Water", "Metals & Minerals"]

        # WARNING DISPLAY
        raw_names = get_raw_model_names(df, provider, model)
        if raw_names is None:
            st.error("Selected model not found. Please select a different model.")
            return
        provider_raw, model_raw = raw_names

        impacts = compute_scenario_impacts(
            scenario=scenario,
            provider=provider_raw,
            model_name=model_raw,
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
