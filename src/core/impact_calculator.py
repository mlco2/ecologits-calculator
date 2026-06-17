from ecologits.estimations.video import video_impacts
from ecologits.tracers.utils import ImpactsOutput, llm_impacts

from src.config.scenarios import Scenario


def compute_scenario_impacts(
    scenario: Scenario,
    provider: str,
    model_name: str,
) -> ImpactsOutput:
    if scenario.modality == "text":
        return llm_impacts(
            provider=provider,
            model_name=model_name,
            output_token_count=scenario.output_token_count or 0,
            request_latency=float("inf"),
        )

    return video_impacts(
        model_name=model_name,
        resolution=scenario.resolution or "1280x720",
        duration=scenario.duration or 5,
        with_audio=scenario.with_audio,
    )
