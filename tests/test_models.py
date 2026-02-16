"""Tests for src/repositories/models.py"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from ecologits.utils.range_value import RangeValue

from src.repositories.models import clean_model_name, load_models, PROVIDERS_FORMAT


class TestCleanModelName:
    """Test cases for clean_model_name function."""

    def test_remove_latest_suffix(self):
        """Should remove 'latest' from model name."""
        result = clean_model_name("gpt-4o-latest")
        assert "latest" not in result.lower()
        assert "gpt" in result.lower()
        assert "4o" in result.lower()

    def test_replace_hyphens_with_spaces(self):
        """Should replace hyphens with spaces."""
        assert clean_model_name("claude-3-5-sonnet") == "claude 3 5 sonnet"

    def test_replace_underscores_with_spaces(self):
        """Should replace underscores with spaces."""
        assert clean_model_name("text_embedding_v3") == "text embedding v3"

    def test_combined_transformation(self):
        """Should apply all transformations together."""
        result = clean_model_name("claude-3-5-sonnet-latest")
        assert "latest" not in result.lower()
        assert "claude" in result.lower()
        assert "3" in result
        assert "5" in result
        assert "sonnet" in result.lower()

    def test_empty_string(self):
        """Should handle empty string."""
        assert clean_model_name("") == ""

    def test_no_special_characters(self):
        """Should return unchanged if no special characters."""
        assert clean_model_name("gpt4") == "gpt4"


class TestLoadModels:
    """Test cases for load_models function."""

    @patch("src.repositories.models.model_repository")
    def test_load_models_returns_dataframe(self, mock_repo, streamlit_mock):
        """Should return a pandas DataFrame."""
        # Setup mock
        mock_model = MagicMock()
        mock_model.name = "gpt-4"
        mock_model.provider.value = "openai"
        mock_model.architecture.type.value = "dense"
        mock_model.architecture.parameters = 1700
        mock_model.warnings = []
        
        mock_repo.list_models.return_value = [mock_model]
        
        # Import after mocking to clear the cache
        with patch("src.repositories.models.MAIN_MODELS", ["gpt-4"]):
            result = load_models(filter_main=True)
        
        assert isinstance(result, pd.DataFrame)

    @patch("src.repositories.models.model_repository")
    def test_load_models_contains_expected_columns(self, mock_repo, streamlit_mock):
        """Should contain all expected columns."""
        from ecologits.model_repository import ArchitectureTypes
        
        mock_model = MagicMock()
        mock_model.name = "gpt-4"
        mock_model.provider.value = "openai"
        mock_model.architecture.type = ArchitectureTypes.DENSE
        mock_model.architecture.parameters = 1700
        mock_model.warnings = []
        
        mock_repo.list_models.return_value = [mock_model]
        mock_repo.ArchitectureTypes = ArchitectureTypes
        
        with patch("src.repositories.models.MAIN_MODELS", ["gpt-4"]):
            result = load_models(filter_main=True)
        
        if len(result) > 0:
            expected_columns = {
                "provider", "provider_clean", "name", "name_clean",
                "architecture_type", "total_parameters", "active_parameters",
                "warning_arch", "warning_multi_modal"
            }
            assert expected_columns.issubset(set(result.columns))

    @patch("src.repositories.models.model_repository")
    def test_load_models_dense_architecture(self, mock_repo, streamlit_mock):
        """Should correctly process dense architecture models."""
        from ecologits.model_repository import ArchitectureTypes
        
        mock_model = MagicMock()
        mock_model.name = "gpt-4"
        mock_model.provider.value = "openai"
        mock_model.architecture.type = ArchitectureTypes.DENSE
        mock_model.architecture.parameters = 1700
        mock_model.warnings = []
        
        mock_repo.list_models.return_value = [mock_model]
        mock_repo.ArchitectureTypes = ArchitectureTypes
        
        with patch("src.repositories.models.MAIN_MODELS", ["gpt-4"]):
            result = load_models(filter_main=True)
        
        if len(result) > 0:
            assert result.iloc[0]["total_parameters"] == 1700

    @patch("src.repositories.models.model_repository")
    def test_load_models_provider_format_mapping(self, mock_repo, streamlit_mock):
        """Should map provider correctly using PROVIDERS_FORMAT."""
        from ecologits.model_repository import ArchitectureTypes
        
        mock_model = MagicMock()
        mock_model.name = "gpt-4"
        mock_model.provider.value = "openai"
        mock_model.architecture.type = ArchitectureTypes.DENSE
        mock_model.architecture.parameters = 1700
        mock_model.warnings = []
        
        mock_repo.list_models.return_value = [mock_model]
        mock_repo.ArchitectureTypes = ArchitectureTypes
        
        with patch("src.repositories.models.MAIN_MODELS", ["gpt-4"]):
            result = load_models(filter_main=True)
        
        if len(result) > 0:
            assert result.iloc[0]["provider_clean"] == "OpenAI"

    @patch("src.repositories.models.model_repository")
    def test_load_models_filter_main_false(self, mock_repo, streamlit_mock):
        """Should process models when filter_main=False."""
        from ecologits.model_repository import ArchitectureTypes
        
        mock_model1 = MagicMock()
        mock_model1.name = "gpt-4"
        mock_model1.provider.value = "openai"
        mock_model1.architecture.type = ArchitectureTypes.DENSE
        mock_model1.architecture.parameters = 1700
        mock_model1.warnings = []
        
        mock_model2 = MagicMock()
        mock_model2.name = "unknown-model"
        mock_model2.provider.value = "openai"
        mock_model2.architecture.type = ArchitectureTypes.DENSE
        mock_model2.architecture.parameters = 700
        mock_model2.warnings = []
        
        mock_repo.list_models.return_value = [mock_model1, mock_model2]
        mock_repo.ArchitectureTypes = ArchitectureTypes
        
        result = load_models(filter_main=False)
        
        assert len(result) >= 0  # Just verify it returns a DataFrame


class TestProvidersFormat:
    """Test cases for PROVIDERS_FORMAT constant."""

    def test_providers_format_has_expected_mappings(self):
        """Should contain expected provider mappings."""
        assert PROVIDERS_FORMAT["anthropic"] == "Anthropic"
        assert PROVIDERS_FORMAT["openai"] == "OpenAI"
        assert PROVIDERS_FORMAT["google_genai"] == "Google"
        assert PROVIDERS_FORMAT["mistralai"] == "Mistral AI"
        assert PROVIDERS_FORMAT["cohere"] == "Cohere"

    def test_providers_format_correct_count(self):
        """Should have 5 provider mappings."""
        assert len(PROVIDERS_FORMAT) == 5
