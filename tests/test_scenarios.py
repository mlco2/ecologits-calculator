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
        ("🎬 Generate a 4K video", None),
    ]
    assert [scenario.duration for scenario in SCENARIOS if scenario.modality == "video"] == [
        6,
        6,
        6,
    ]


def test_load_video_models_filters_by_resolution(streamlit_mock):
    models_1080p = load_video_models(resolution="1920x1080")

    assert not models_1080p.empty
    assert "Kling AI" not in set(models_1080p["provider_clean"])


def test_load_video_models_supports_4k(streamlit_mock):
    models_4k = load_video_models(resolution="3840x2160")

    assert set(models_4k["provider_clean"]) == {"Google", "OpenAI"}


def test_mock_video_impacts_use_standard_formatting():
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
