"""Tests for src/repositories/electricity_mix.py."""

from src.config.constants import COUNTRY_CODES
from src.repositories.electricity_mix import (
    CRITERIA,
    format_country_name,
    format_electricity_mix_criterion,
)


class TestFormatCountryName:
    """Test cases for format_country_name function."""

    def test_format_country_name_valid_code(self):
        """Should return formatted country name for valid country code."""
        result = format_country_name("USA")
        assert result == "🇺🇸 United States"

    def test_format_country_name_france(self):
        """Should correctly format France."""
        result = format_country_name("FRA")
        assert result == "🇫🇷 France"

    def test_format_country_name_world(self):
        """Should correctly format World."""
        result = format_country_name("WOR")
        assert result == "🌎 World"

    def test_format_country_name_invalid_code(self):
        """Should return None for invalid country code."""
        result = format_country_name("XXX")
        assert result is None

    def test_format_country_name_empty_string(self):
        """Should return None for empty string."""
        result = format_country_name("")
        assert result is None

    def test_format_country_name_case_sensitive(self):
        """Should be case-sensitive (requires uppercase)."""
        # Assuming the function uses exact matching
        result = format_country_name("usa")
        assert result is None


class TestFormatElectricityMixCriterion:
    """Test cases for format_electricity_mix_criterion function."""

    def test_format_gwp_criterion(self):
        """Should return GHG Emission label for 'gwp'."""
        result = format_electricity_mix_criterion("gwp")
        assert result == "GHG Emission (kg CO2 eq)"

    def test_format_adpe_criterion(self):
        """Should return Abiotic Resources label for 'adpe'."""
        result = format_electricity_mix_criterion("adpe")
        assert result == "Abiotic Resources (kg Sb eq)"

    def test_format_pe_criterion(self):
        """Should return Primary Energy label for 'pe'."""
        result = format_electricity_mix_criterion("pe")
        assert result == "Primary Energy (MJ)"

    def test_format_wue_criterion(self):
        """Should return Water Usage Effectiveness label for 'wue'."""
        result = format_electricity_mix_criterion("wue")
        assert result == "Water Usage Effectiveness (L/kWh)"

    def test_format_invalid_criterion(self):
        """Should return None for invalid criterion."""
        result = format_electricity_mix_criterion("invalid")
        assert result is None

    def test_format_empty_criterion(self):
        """Should return None for empty criterion."""
        result = format_electricity_mix_criterion("")
        assert result is None


class TestCriteriaConstant:
    """Test cases for CRITERIA constant."""

    def test_criteria_has_four_entries(self):
        """Should contain exactly 4 criteria."""
        assert len(CRITERIA) == 4

    def test_criteria_keys(self):
        """Should have expected keys."""
        expected_keys = {"gwp", "adpe", "pe", "wue"}
        assert set(CRITERIA.keys()) == expected_keys

    def test_criteria_non_empty_values(self):
        """All criteria values should be non-empty strings."""
        for _key, value in CRITERIA.items():
            assert isinstance(value, str)
            assert len(value) > 0


class TestCountryCodesIntegration:
    """Integration tests with COUNTRY_CODES constant."""

    def test_all_country_codes_can_be_formatted(self):
        """All country codes should be formattable."""
        for country_display, country_code in COUNTRY_CODES:
            result = format_country_name(country_code)
            assert result is not None
            assert country_code in country_display or country_display in result

    def test_country_codes_unique(self):
        """All country codes should be unique."""
        codes = [code for _, code in COUNTRY_CODES]
        assert len(codes) == len(set(codes))
