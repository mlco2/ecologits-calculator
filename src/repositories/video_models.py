import pandas as pd
import streamlit as st

from src.repositories.models import clean_model_name

VIDEO_PROVIDERS_FORMAT = {
    "google": "Google",
    "klingai": "Kling AI",
    "openai": "OpenAI",
    "runway": "Runway",
}

_PROTOTYPE_VIDEO_MODELS = [
    {
        "provider": "google",
        "name": "google/veo-3.1",
        "resolutions": ["1280x720", "1920x1080", "3840x2160"],
    },
    {
        "provider": "google",
        "name": "google/veo-3.1-fast",
        "resolutions": ["1280x720", "1920x1080"],
    },
    {
        "provider": "klingai",
        "name": "klingai/kling-v3",
        "resolutions": ["1280x720"],
    },
    {
        "provider": "openai",
        "name": "openai/sora-2-pro",
        "resolutions": ["1280x720", "1920x1080", "3840x2160"],
    },
    {
        "provider": "runway",
        "name": "runway/gen-4.5",
        "resolutions": ["1280x720"],
    },
]


@st.cache_data
def load_video_models(resolution: str | None = None) -> pd.DataFrame:
    data = []
    for model in _PROTOTYPE_VIDEO_MODELS:
        if resolution is not None and resolution not in model["resolutions"]:
            continue

        provider = model["provider"]
        name = model["name"]
        short_name = name.split("/", 1)[1]
        data.append(
            {
                "provider": provider,
                "provider_clean": VIDEO_PROVIDERS_FORMAT.get(provider, provider),
                "name": name,
                "name_clean": clean_model_name(short_name),
                "resolutions": model["resolutions"],
            }
        )

    return pd.DataFrame(data)
