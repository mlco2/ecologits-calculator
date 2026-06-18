import streamlit as st

from src.config.scenarios import SCENARIOS, Scenario
from src.core.formatting import format_impacts
from src.core.impact_calculator import compute_scenario_impacts
from src.repositories.models import get_raw_model_names, load_models
from src.repositories.video_models import load_video_models
from src.ui.components import render_model_selector
from src.ui.equivalents import (
    display_equivalents,
    render_equivalents_title,
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
        return load_video_models(
            resolution=scenario.resolution,
            duration=scenario.duration,
            with_audio=scenario.with_audio,
            extrapolate_resolution=scenario.extrapolate_resolution,
        )
    return load_models(filter_main=True)


def _scenario_context_text(scenario: Scenario) -> str | None:
    if scenario.modality == "video":
        return (
            f"{scenario.resolution}, {scenario.duration}s"
            + (" with audio" if scenario.with_audio else "")
        )
    if scenario.output_token_count is not None:
        return f"{scenario.output_token_count:,} output tokens"
    return None


def _combine_warnings(warnings) -> str | None:
    if not warnings:
        return None
    messages = [str(getattr(warning, "message", warning)) for warning in warnings]
    if not messages:
        return None
    if len(messages) == 1:
        return messages[0]
    if len(messages) == 2:
        head, separator, suffix = messages[0].partition(",")
        tail = messages[1].partition(",")[0].lower()
        if separator and tail:
            return f"{head} and {tail},{suffix}"
    return " ".join(messages)


def calculator_mode():
    with st.container(border=True):
        # st.markdown('<h3 align="center">Calculator</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            scenario = _render_scenario_selector()

        df = _load_compatible_models(scenario)
        if df.empty:
            st.error("No compatible model is available for this task.")
            return

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

        context_parts = []
        scenario_text = _scenario_context_text(scenario)
        if scenario_text:
            icon = "🎬" if scenario.modality == "video" else "✍️"
            context_parts.append(f"{icon} {scenario_text}")
        warning_text = _combine_warnings(impacts.warnings)
        if warning_text:
            context_parts.append(f"⚠️ {warning_text}")
        if context_parts:
            st.caption(" · ".join(context_parts))

        impacts_formatted, _, _ = format_impacts(impacts)

        # st.write(impacts)

        st.markdown(
            '<h3 class="section-title section-title-impacts">Environmental impacts</h3>',
            unsafe_allow_html=True,
        )
        display_impacts(
            impacts_output=impacts_formatted, impacts_to_display=list_impacts, mode="basic"
        )

        if "impacts_at_scale" not in st.session_state:
            st.session_state.impacts_at_scale = True

        equivalents_mode = "at_scale" if st.session_state.impacts_at_scale else "unit"
        render_equivalents_title(equivalents_mode)
        st.toggle(
            label="Display impacts at scale",
            key="impacts_at_scale",
            help="The scale we implemented is a daily replication of the given usage by 1% of the world population.",
        )
        display_equivalents(impacts_formatted, how=equivalents_mode, show_title=False)
