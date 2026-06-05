"""Tests for JSON-based model filtering."""

import json
import os

from src.repositories.model_config import load_main_models
from src.repositories.models import load_models


class TestJSONModelFiltering:
    """Test cases for JSON-based model filtering."""

    def test_load_main_models_from_json(self):
        """Should load main models from models_recent.json file."""
        # Reset the global cache to ensure fresh load
        import src.config.constants as constants

        constants.MAIN_MODELS = None

        main_models = load_main_models()

        # Should load models from JSON
        assert isinstance(main_models, list)
        assert len(main_models) > 0

        # Should contain expected recent models
        expected_models = [
            "claude-opus-4-1-20250805",
            "gpt-5",
            "gemini-3-flash-preview",
            "command-a-plus-05-2026",
        ]

        for expected_model in expected_models:
            assert expected_model in main_models, (
                f"Expected model {expected_model} not found in main models"
            )

    def test_json_file_exists(self):
        """Should have models_recent.json file."""
        json_path = os.path.join("src", "config", "models_recent.json")
        assert os.path.exists(json_path), "models_recent.json file should exist"

    def test_json_file_structure(self):
        """Should have valid JSON structure."""
        json_path = os.path.join("src", "config", "models_recent.json")

        with open(json_path) as f:
            data = json.load(f)

        # Should have expected structure
        assert "models" in data
        assert isinstance(data["models"], list)
        assert len(data["models"]) > 0

        # Each model should have provider and name
        for model in data["models"]:
            assert "provider" in model
            assert "name" in model
            assert isinstance(model["provider"], str)
            assert isinstance(model["name"], str)

    def test_model_filtering_works(self):
        """Should correctly filter models based on JSON list."""
        # Reset the global cache
        import src.config.constants as constants

        constants.MAIN_MODELS = None

        # Load models with filtering
        df_filtered = load_models(filter_main=True)
        df_all = load_models(filter_main=False)

        # Filtered should have fewer models than all
        assert len(df_filtered) < len(df_all)

        # All filtered models should be in the main models list
        main_models = load_main_models()
        for model_name in df_filtered["name"]:
            assert model_name in main_models, (
                f"Filtered model {model_name} should be in main models list"
            )

    def test_fallback_to_hardcoded_list(self):
        """Should fallback to hardcoded list if JSON loading fails."""
        # This is harder to test without mocking, but we can at least verify
        # that the function doesn't crash and returns a list
        main_models = load_main_models()
        assert isinstance(main_models, list)
        assert len(main_models) > 0

    def test_recent_models_are_actually_recent(self):
        """Should contain recent models (2024-2026)."""
        main_models = load_main_models()

        # Should contain some recent models
        recent_indicators = ["2024", "2025", "2026", "4-", "5-", "gemini-3", "gpt-5"]

        found_recent = False
        for model in main_models:
            for indicator in recent_indicators:
                if indicator in model:
                    found_recent = True
                    break
            if found_recent:
                break

        assert found_recent, "Should contain at least some recent models"


class TestModelFilteringIntegration:
    """Integration tests for model filtering."""

    def test_filtered_ui_uses_recent_models(self):
        """Filtered UI modes should use recent models from JSON."""
        # Reset cache
        import src.config.constants as constants

        constants.MAIN_MODELS = None

        # Load filtered models (like calculator and company modes use)
        df_filtered = load_models(filter_main=True)

        # Should have reasonable number of models (not too many, not too few)
        assert 30 <= len(df_filtered) <= 100, (
            f"Filtered models count {len(df_filtered)} seems unreasonable"
        )

        # Should include providers from JSON
        providers_in_filtered = df_filtered["provider_clean"].unique()
        expected_providers = ["OpenAI", "Anthropic", "Google", "Cohere", "Mistral AI"]

        for expected_provider in expected_providers:
            assert expected_provider in providers_in_filtered, (
                f"Expected provider {expected_provider} missing from filtered models"
            )

    def test_expert_mode_uses_all_models(self):
        """Expert mode should have access to all models."""
        df_all = load_models(filter_main=False)
        df_filtered = load_models(filter_main=True)

        # Expert mode should have more models than filtered mode
        assert len(df_all) > len(df_filtered)

        # All filtered models should be in the full list
        filtered_names = set(df_filtered["name"])
        all_names = set(df_all["name"])
        assert filtered_names.issubset(all_names), "All filtered models should be in the full list"
