"""Tests for parameter extraction in expert mode."""

import pytest

from src.ui.expert import extract_param_value


class TestExtractParamValue:
    """Test the extract_param_value function."""

    def test_extract_scalar_int(self):
        """Test extraction from a scalar integer."""
        result = extract_param_value(10)
        assert result == 10

    def test_extract_scalar_float(self):
        """Test extraction from a scalar float."""
        result = extract_param_value(10.5)
        assert result == 10

    def test_extract_range_dict(self):
        """Test extraction from a RangeValue dict."""
        result = extract_param_value({"min": 5, "max": 15})
        assert result == 10

    def test_extract_range_dict_with_decimals(self):
        """Test extraction from a RangeValue dict with decimal values."""
        result = extract_param_value({"min": 5.5, "max": 14.5})
        assert result == 10

    def test_none_value_raises_error(self):
        """Test that None value raises ValueError."""
        with pytest.raises(ValueError, match="Parameter value is None"):
            extract_param_value(None)

    def test_invalid_dict_missing_min_key(self):
        """Test that dict missing 'min' key raises ValueError."""
        with pytest.raises(ValueError, match="RangeValue dict missing valid 'min' or 'max' keys"):
            extract_param_value({"max": 15})

    def test_invalid_dict_missing_max_key(self):
        """Test that dict missing 'max' key raises ValueError."""
        with pytest.raises(ValueError, match="RangeValue dict missing valid 'min' or 'max' keys"):
            extract_param_value({"min": 5})

    def test_invalid_dict_non_numeric_values(self):
        """Test that dict with non-numeric values raises ValueError."""
        with pytest.raises(ValueError, match="RangeValue dict missing valid 'min' or 'max' keys"):
            extract_param_value({"min": "5", "max": "15"})

    def test_invalid_type_string(self):
        """Test that string value raises ValueError."""
        with pytest.raises(ValueError, match="Parameter value must be int, float, or dict"):
            extract_param_value("10")

    def test_invalid_type_list(self):
        """Test that list value raises ValueError."""
        with pytest.raises(ValueError, match="Parameter value must be int, float, or dict"):
            extract_param_value([10, 20])

    def test_invalid_type_bool(self):
        """Test that boolean value raises ValueError."""
        with pytest.raises(ValueError, match="Parameter value must be int, float, or dict"):
            extract_param_value(True)
