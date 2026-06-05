"""Tests for electricity mix warnings integration."""

from ecologits.electricity_mix_repository import electricity_mixes

from src.ui.components import display_electricity_mix_warnings


class TestElectricityMixWarnings:
    """Test cases for electricity mix warnings functionality."""

    def test_find_electricity_mix_with_warnings(self):
        """Should find at least one electricity mix with warnings."""
        em_with_warnings = None
        for em in electricity_mixes.list_electricity_mixes():
            if em.has_warnings:
                em_with_warnings = em
                break

        assert em_with_warnings is not None
        assert len(em_with_warnings.warnings) > 0

    def test_find_electricity_mix_without_warnings(self):
        """Should find at least one electricity mix without warnings."""
        em_without_warnings = None
        for em in electricity_mixes.list_electricity_mixes():
            if not em.has_warnings:
                em_without_warnings = em
                break

        assert em_without_warnings is not None
        assert len(em_without_warnings.warnings) == 0

    def test_warning_structure(self):
        """Warnings should have proper structure."""
        em_with_warnings = None
        for em in electricity_mixes.list_electricity_mixes():
            if em.has_warnings:
                em_with_warnings = em
                break

        assert em_with_warnings is not None

        for warning in em_with_warnings.warnings:
            assert hasattr(warning, "code")
            assert hasattr(warning, "message")
            assert isinstance(warning.code, str)
            assert isinstance(warning.message, str)
            assert len(warning.code) > 0
            assert len(warning.message) > 0

    def test_display_function_with_warnings(self):
        """Display function should handle electricity mixes with warnings."""
        em_with_warnings = None
        for em in electricity_mixes.list_electricity_mixes():
            if em.has_warnings:
                em_with_warnings = em
                break

        assert em_with_warnings is not None

        # Should not raise an exception
        try:
            display_electricity_mix_warnings(em_with_warnings)
        except Exception as e:
            raise AssertionError(
                f"display_electricity_mix_warnings should not raise exception: {e}"
            ) from e

    def test_display_function_without_warnings(self):
        """Display function should handle electricity mixes without warnings."""
        em_without_warnings = None
        for em in electricity_mixes.list_electricity_mixes():
            if not em.has_warnings:
                em_without_warnings = em
                break

        assert em_without_warnings is not None

        # Should not raise an exception
        try:
            display_electricity_mix_warnings(em_without_warnings)
        except Exception as e:
            raise AssertionError(
                f"display_electricity_mix_warnings should not raise exception: {e}"
            ) from e

    def test_display_function_with_none(self):
        """Display function should handle None input."""
        # Should not raise an exception
        try:
            display_electricity_mix_warnings(None)
        except Exception as e:
            raise AssertionError(
                f"display_electricity_mix_warnings should not raise exception with None: {e}"
            ) from e

    def test_specific_warning_codes(self):
        """Should find specific known warning codes."""
        expected_codes = {
            "electricity-mix-adpe-world",
            "electricity-mix-pe-world",
            "electricity-mix-wue-world",
        }

        found_codes = set()
        for em in electricity_mixes.list_electricity_mixes():
            for warning in em.warnings:
                found_codes.add(warning.code)

        # Should find at least some of the expected warning codes
        assert len(found_codes.intersection(expected_codes)) > 0, (
            f"Should find some expected warning codes, found: {found_codes}"
        )

    def test_france_electricity_mix(self):
        """France electricity mix should be available and have specific properties."""
        em_fra = electricity_mixes.find_electricity_mix("FRA")
        assert em_fra is not None
        assert em_fra.zone == "FRA"
        assert isinstance(em_fra.gwp, float)
        assert isinstance(em_fra.has_warnings, bool)
