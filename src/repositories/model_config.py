"""Model configuration and filtering."""

import json

from pathlib import Path


def _load_models_json() -> dict:
    """Load raw models_recent.json content."""
    json_path = Path(__file__).parent.parent / "config" / "models_recent.json"
    with json_path.open(encoding="utf-8") as f:
        return json.load(f)


def load_main_models() -> list[str]:
    """Load main models from models_recent.json file.

    Returns:
        List of model names that should be considered "main" models
        for the filtered UI modes.

    Raises:
        FileNotFoundError: If models_recent.json is missing.
        json.JSONDecodeError: If models_recent.json is not valid JSON.
        KeyError: If the expected keys are missing.
    """
    data = _load_models_json()

    # Extract model names from the JSON
    return [model["name"] for model in data["models"]]


def load_model_aliases() -> dict[str, str]:
    """Load display aliases from models_recent.json file.

    Each entry in models_recent.json may define an optional ``alias``
    used as the display name (``name_clean``) in all model dropdown
    selectors. Entries without an alias fall back to ``clean_model_name``.

    Returns:
        Mapping of raw model name -> display alias.

    Raises:
        FileNotFoundError: If models_recent.json is missing.
        json.JSONDecodeError: If models_recent.json is not valid JSON.
    """
    data = _load_models_json()
    aliases = {}
    for model in data.get("models", []):
        name = model.get("name")
        alias = model.get("alias")
        if name and isinstance(alias, str) and alias.strip():
            aliases[name] = alias.strip()
    return aliases
