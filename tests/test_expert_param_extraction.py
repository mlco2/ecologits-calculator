"""Tests for parameter extraction in expert mode."""

import pytest

from ecologits.utils.range_value import RangeValue

from src.ui.expert import extract_param_value, impact_param_value


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


class TestImpactParamValue:
    """Test the impact_param_value function."""

    def test_preserves_default_range_dict(self):
        """Should convert an unchanged range dict to RangeValue."""
        result = impact_param_value({"min": 70, "max": 120}, 95)

        assert isinstance(result, RangeValue)
        assert result.min == 70
        assert result.max == 120

    def test_uses_scalar_when_range_input_was_changed(self):
        """Should use the expert input when it differs from the range midpoint."""
        result = impact_param_value({"min": 70, "max": 120}, 100)

        assert result == 100

    def test_uses_scalar_for_scalar_model_value(self):
        """Should keep scalar model metadata scalar."""
        result = impact_param_value(440, 440)

        assert result == 440
