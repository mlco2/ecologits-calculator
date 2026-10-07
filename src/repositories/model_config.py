"""Model configuration and filtering."""

import json
import os


def _load_models_json() -> dict:
    """Load raw models_recent.json content."""
    json_path = os.path.join(os.path.dirname(__file__), "..", "config", "models_recent.json")
    with open(json_path) as f:
        return json.load(f)


def load_main_models() -> list[str]:
    """Load main models from models_recent.json file.

    Returns:
        List of model names that should be considered "main" models
        for the filtered UI modes.
    """
    try:
        # Try to load from the JSON file
        data = _load_models_json()

        # Extract model names from the JSON
        return [model["name"] for model in data["models"]]

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        # Fallback to a basic list if JSON loading fails
        print(f"Warning: Could not load models_recent.json, using basic fallback list: {e}")
        # Basic fallback with some common models
        return [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "claude-3-opus",
            "claude-3-sonnet",
            "claude-3-haiku",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "command-r",
            "command-r-plus",
            "mistral-large",
            "mistral-medium",
            "mistral-small",
        ]


def load_model_aliases() -> dict[str, str]:
    """Load display aliases from models_recent.json file.

    Each entry in models_recent.json may define an optional ``alias``
    used as the display name (``name_clean``) in all model dropdown
    selectors. Entries without an alias fall back to ``clean_model_name``.

    Returns:
        Mapping of raw model name -> display alias. Empty dict if the
        JSON cannot be loaded.
    """
    try:
        data = _load_models_json()
    except (FileNotFoundError, json.JSONDecodeError, KeyError, OSError) as e:
        print(f"Warning: Could not load model aliases from models_recent.json: {e}")
        return {}
    aliases = {}
    for model in data.get("models", []):
        name = model.get("name")
        alias = model.get("alias")
        if name and isinstance(alias, str) and alias.strip():
            aliases[name] = alias.strip()
    return aliases
