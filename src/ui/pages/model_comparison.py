import streamlit as st

from src.config.scenarios import SCENARIOS
from src.core.formatting import format_impacts
from src.core.impact_calculator import compute_scenario_impacts
from src.repositories.models import load_models
from src.repositories.video_models import load_video_models
from src.ui.components.impacts import display_impacts


def model_comparison_page() -> None:
    st.markdown(
        "Compare estimated environmental impacts for the same task across AI models."
    )

    scenario_label = st.selectbox(
        "Task", options=[scenario.label for scenario in SCENARIOS], key="compare_task"
    )
    scenario = next(s for s in SCENARIOS if s.label == scenario_label)

    if scenario.modality == "video":
        models = load_video_models(
            resolution=scenario.resolution,
            duration=scenario.duration,
            with_audio=scenario.with_audio,
            extrapolate_resolution=scenario.extrapolate_resolution,
        )
    else:
        models = load_models(filter_main=True)

    if models.empty:
        st.error("No compatible models are available for this task.")
        return

    model_options = {
        f"{row.provider_clean} — {row.name_clean}": (row.provider, row.name)
        for row in models.itertuples()
    }
    selected = st.multiselect(
        "Models to compare",
        options=list(model_options),
        default=list(model_options)[:2],
        max_selections=4,
        help="Select up to four models. Estimates use identical task settings.",
        key="compare_models",
    )

    if not selected:
        st.info("Select at least one model to see its estimated impacts.")
        return

    columns = st.columns(len(selected))
    for column, label in zip(columns, selected, strict=True):
        provider, model_name = model_options[label]
        with column:
            st.subheader(label)
            try:
                impacts, _, _ = format_impacts(
                    compute_scenario_impacts(scenario, provider, model_name)
                )
                display_impacts(
                    impacts_output=impacts,
                    impacts_to_display=[
                        "Electricity",
                        "Carbon Footprint",
                        "Water",
                        "Metals & Minerals",
                    ],
                    mode="basic",
                )
            except ValueError as error:
                st.error(str(error))
