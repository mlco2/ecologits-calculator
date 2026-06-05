"""Model configuration and filtering."""

import json
import os


def load_main_models() -> list[str]:
    """Load main models from models_recent.json file.

    Returns:
        List of model names that should be considered "main" models
        for the filtered UI modes.
    """
    try:
        # Try to load from the JSON file
        json_path = os.path.join(os.path.dirname(__file__), "..", "config", "models_recent.json")
        with open(json_path) as f:
            data = json.load(f)

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
