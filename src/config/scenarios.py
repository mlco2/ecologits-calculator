from dataclasses import dataclass
from typing import Literal

Modality = Literal["text", "video"]


@dataclass(frozen=True)
class Scenario:
    label: str
    modality: Modality
    output_token_count: int | None = None
    resolution: str | None = None
    duration: int | None = None
    with_audio: bool = False


TEXT_SCENARIOS = [
    Scenario(
        label="✍️ Write an email",
        modality="text",
        output_token_count=250,
    ),
    Scenario(
        label="✍️ Small conversation with a chatbot",
        modality="text",
        output_token_count=400,
    ),
    Scenario(
        label="✍️ Write a 5-page report",
        modality="text",
        output_token_count=5000,
    ),
    Scenario(
        label="✍️ Assist application development",
        modality="text",
        output_token_count=100000,
    ),
    Scenario(
        label="✍️ Re-write the Lord Of The Rings trilogy",
        modality="text",
        output_token_count=500000,
    ),
]

VIDEO_SCENARIOS = [
    Scenario(
        label="🎬 Generate a 720p video",
        modality="video",
        resolution="1280x720",
        duration=6,
        with_audio=True,
    ),
    Scenario(
        label="🎬 Generate a 1080p video",
        modality="video",
        resolution="1920x1080",
        duration=6,
        with_audio=True,
    ),
    Scenario(
        label="🎬 Generate a 4K video",
        modality="video",
        resolution="3840x2160",
        duration=6,
        with_audio=True,
    ),
]

SCENARIOS = TEXT_SCENARIOS + VIDEO_SCENARIOS
