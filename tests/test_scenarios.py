from src.config.scenarios import SCENARIOS
from src.core.formatting import format_impacts
from src.core.impact_calculator import compute_scenario_impacts
from src.repositories.video_models import load_video_models


def test_scenarios_include_text_and_video():
    modalities = {scenario.modality for scenario in SCENARIOS}

    assert modalities == {"text", "video"}


def test_scenarios_match_supported_tasks():
    assert [(scenario.label, scenario.output_token_count) for scenario in SCENARIOS] == [
        ("✍️ Write an email", 250),
        ("✍️ Small conversation with a chatbot", 400),
        ("✍️ Write a 5-page report", 5000),
        ("✍️ Assist application development", 100000),
        ("✍️ Re-write the Lord Of The Rings trilogy", 500000),
        ("🎬 Generate a 720p video", None),
        ("🎬 Generate a 1080p video", None),
        ("🎬 Generate a 720p video without audio", None),
        ("🎬 Generate a 4K video", None),
    ]
    assert [scenario.duration for scenario in SCENARIOS if scenario.modality == "video"] == [
        8,
        8,
        8,
        8,
    ]


def test_load_video_models_filters_by_resolution_and_audio(streamlit_mock):
    models_1080p = load_video_models(resolution="1920x1080", duration=8, with_audio=True)

    assert not models_1080p.empty
    assert "Kling AI" not in set(models_1080p["provider_clean"])
    assert set(models_1080p["audio_generation"]) == {True}


def test_load_video_models_uses_real_compatibility_data(streamlit_mock):
    models_without_audio = load_video_models(
        resolution="1280x720",
        duration=8,
        with_audio=False,
    )

    assert not models_without_audio.empty
    assert "Runway" in set(models_without_audio["provider_clean"])


def test_load_video_models_can_extrapolate_4k_resolution(streamlit_mock):
    exact_models = load_video_models(
        resolution="3840x2160",
        duration=8,
        with_audio=True,
    )
    extrapolated_models = load_video_models(
        resolution="3840x2160",
        duration=8,
        with_audio=True,
        extrapolate_resolution=True,
    )

    assert exact_models.empty
    assert not extrapolated_models.empty
    assert set(extrapolated_models["audio_generation"]) == {True}


def test_video_impacts_use_standard_formatting():
    scenario = next(scenario for scenario in SCENARIOS if scenario.modality == "video")

    impacts = compute_scenario_impacts(
        scenario=scenario,
        provider="openai",
        model_name="openai/sora-2-pro",
    )
    formatted, usage, embodied = format_impacts(impacts)

    assert formatted.ranges
    assert formatted.energy.magnitude > 0
    assert usage is not None
    assert embodied is not None
