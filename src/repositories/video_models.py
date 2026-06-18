import pandas as pd
import streamlit as st

from ecologits.estimations.video import _video_models_data, duration_to_frames

from src.repositories.models import clean_model_name

VIDEO_PROVIDERS_FORMAT = {
    "alibaba": "Alibaba",
    "bytedance": "ByteDance",
    "google": "Google",
    "klingai": "Kling AI",
    "lightricks": "Lightricks",
    "openai": "OpenAI",
    "runway": "Runway",
    "tencent": "Tencent",
}


def _resolution_to_string(resolution: list[int]) -> str:
    width, height = resolution
    return f"{width}x{height}"


@st.cache_data
def load_video_models(
    resolution: str | None = None,
    duration: float | None = None,
    with_audio: bool | None = None,
    extrapolate_resolution: bool = False,
) -> pd.DataFrame:
    data = []
    frames_count = duration_to_frames(duration) if duration is not None else None

    for model in _video_models_data["models"]:
        capabilities = model["capabilities"]
        resolutions = [
            _resolution_to_string(model_resolution)
            for model_resolution in capabilities["resolutions"]
        ]

        if (
            resolution is not None
            and resolution not in resolutions
            and not extrapolate_resolution
        ):
            continue
        if frames_count is not None and frames_count not in capabilities["frames_count"]:
            continue
        if with_audio and not capabilities["audio_generation"]:
            continue

        provider = model["provider"]
        name = model["model_name"]
        short_name = name.split("/", 1)[1]
        data.append(
            {
                "provider": provider,
                "provider_clean": VIDEO_PROVIDERS_FORMAT.get(provider, provider),
                "name": name,
                "name_clean": clean_model_name(short_name),
                "resolutions": resolutions,
                "frames_count": capabilities["frames_count"],
                "audio_generation": capabilities["audio_generation"],
            }
        )

    return pd.DataFrame(data)
