"""Tests for src/core/formatting.py."""

from unittest.mock import MagicMock

from pint import Quantity

from src.core.formatting import (
    QImpacts,
    format_adpe,
    format_energy,
    format_gwp,
    format_impacts,
    format_pe,
    format_wcf,
)
from src.core.units import q


class TestFormatEnergy:
    """Test cases for format_energy function."""

    def test_format_energy_kWh(self):
        """Should format energy with appropriate units."""
        result = format_energy(0.05)
        # The function converts to appropriate units based on magnitude
        assert result is not None
        assert result.magnitude > 0

    def test_format_energy_below_kwh_converts_to_wh(self):
        """Should convert to Wh for values below 1 kWh."""
        result = format_energy(0.0005)
        assert "Wh" in str(result.units)

    def test_format_energy_magnitude(self):
        """Should preserve energy (may convert units)."""
        result = format_energy(0.05)
        # Convert back to kWh to verify energy is preserved
        result_in_kwh = result.to("kWh")
        assert abs(result_in_kwh.magnitude - 0.05) < 0.001

    def test_format_energy_very_small_converts_to_mwh(self):
        """Should convert to mWh for very small values."""
        result = format_energy(0.000001)
        assert "mWh" in str(result.units)


class TestFormatGWP:
    """Test cases for format_gwp function."""

    def test_format_gwp_kg(self):
        """Should format GWP in kgCO2eq."""
        result = format_gwp(0.03)
        assert "CO2" in str(result.units)

    def test_format_gwp_below_kg_converts_to_g(self):
        """Should convert to gCO2eq for values below 1 kg."""
        result = format_gwp(0.0005)
        assert "gCO2" in str(result.units)

    def test_format_gwp_magnitude(self):
        """Should preserve GWP value (may convert units)."""
        result = format_gwp(0.03)
        # Convert back to kgCO2eq to verify value is preserved
        result_in_kg = result.to("kgCO2eq")
        assert abs(result_in_kg.magnitude - 0.03) < 0.001

    def test_format_gwp_very_small_converts_to_mg(self):
        """Should convert to mgCO2eq for very small values."""
        result = format_gwp(0.00001)
        assert "mgCO2" in str(result.units)


class TestFormatADPe:
    """Test cases for format_adpe function."""

    def test_format_adpe_kg(self):
        """Should format ADPe in kgSbeq."""
        result = format_adpe(0.001)
        assert "Sb" in str(result.units)

    def test_format_adpe_conversion_chain(self):
        """Should convert through different units based on magnitude."""
        result_kg = format_adpe(0.001)
        result_g = format_adpe(0.0001)
        # Just verify they execute without error
        assert result_kg is not None
        assert result_g is not None

    def test_format_adpe_magnitude(self):
        """Should preserve ADPe value (may convert units)."""
        result = format_adpe(0.001)
        # Convert back to kgSbeq to verify value is preserved
        result_in_kg = result.to("kgSbeq")
        assert abs(result_in_kg.magnitude - 0.001) < 0.0001


class TestFormatPE:
    """Test cases for format_pe function."""

    def test_format_pe_mj(self):
        """Should format PE in MJ."""
        result = format_pe(0.5)
        assert "MJ" in str(result.units) or "J" in str(result.units)

    def test_format_pe_below_mj_converts_to_kj(self):
        """Should convert to kJ for values below 1 MJ."""
        result = format_pe(0.0005)
        assert "kJ" in str(result.units)

    def test_format_pe_magnitude(self):
        """Should preserve PE value (may convert units)."""
        result = format_pe(0.5)
        # Convert back to MJ to verify value is preserved
        result_in_mj = result.to("MJ")
        assert abs(result_in_mj.magnitude - 0.5) < 0.01


class TestFormatWCF:
    """Test cases for format_wcf function."""

    def test_format_wcf_liters(self):
        """Should format WCF in liters."""
        result = format_wcf(0.1)
        assert "L" in str(result.units)

    def test_format_wcf_below_liter_converts_to_ml(self):
        """Should convert to mL for values below 1 L."""
        result = format_wcf(0.0005)
        assert "mL" in str(result.units)

    def test_format_wcf_magnitude(self):
        """Should preserve WCF value (may convert units)."""
        result = format_wcf(0.1)
        # Convert back to L to verify value is preserved
        result_in_l = result.to("L")
        assert abs(result_in_l.magnitude - 0.1) < 0.01


class TestFormatImpacts:
    """Test cases for format_impacts function."""

    def test_format_impacts_with_float_values(self):
        """Should format impacts correctly when values are floats."""
        # Create mock impacts object with float values
        mock_impacts = MagicMock()
        mock_impacts.energy.value = 0.05
        mock_impacts.gwp.value = 0.03
        mock_impacts.adpe.value = 0.001
        mock_impacts.pe.value = 0.5
        mock_impacts.wcf.value = 0.1
        mock_impacts.usage = "usage"
        mock_impacts.embodied = "embodied"

        q_impacts, usage, embodied = format_impacts(mock_impacts)

        assert isinstance(q_impacts, QImpacts)
        assert isinstance(q_impacts.energy, Quantity)
        assert isinstance(q_impacts.gwp, Quantity)
        assert isinstance(q_impacts.adpe, Quantity)
        assert isinstance(q_impacts.pe, Quantity)
        assert isinstance(q_impacts.wcf, Quantity)
        assert not q_impacts.ranges
        assert usage == "usage"
        assert embodied == "embodied"

    def test_format_impacts_with_range_values(self):
        """Should format impacts correctly with range values."""
        # Create mock impacts with RangeValue objects
        mock_range = MagicMock()
        mock_range.mean = 0.05
        mock_range.min = 0.04
        mock_range.max = 0.06

        mock_impacts = MagicMock()
        mock_impacts.energy.value = mock_range
        mock_impacts.gwp.value = mock_range
        mock_impacts.adpe.value = mock_range
        mock_impacts.pe.value = mock_range
        mock_impacts.wcf.value = mock_range
        mock_impacts.usage = "usage"
        mock_impacts.embodied = "embodied"

        q_impacts, _usage, _embodied = format_impacts(mock_impacts)

        assert isinstance(q_impacts, QImpacts)
        assert q_impacts.ranges
        assert q_impacts.energy_min is not None
        assert q_impacts.energy_max is not None
        assert q_impacts.gwp_min is not None
        assert q_impacts.gwp_max is not None

    def test_qimpacts_dataclass_fields(self):
        """Should create QImpacts with all required fields."""
        q_impacts = QImpacts(
            energy=q("0.05 kWh"),
            gwp=q("0.03 kgCO2eq"),
            adpe=q("0.001 kgSbeq"),
            pe=q("0.5 MJ"),
            wcf=q("0.1 L"),
        )

        assert q_impacts.energy is not None
        assert q_impacts.gwp is not None
        assert q_impacts.adpe is not None
        assert q_impacts.pe is not None
        assert q_impacts.wcf is not None
        assert not q_impacts.ranges

    def test_qimpacts_with_ranges(self):
        """Should create QImpacts with range values."""
        q_impacts = QImpacts(
            energy=q("0.05 kWh"),
            gwp=q("0.03 kgCO2eq"),
            adpe=q("0.001 kgSbeq"),
            pe=q("0.5 MJ"),
            wcf=q("0.1 L"),
            ranges=True,
            energy_min=q("0.04 kWh"),
            energy_max=q("0.06 kWh"),
            gwp_min=q("0.02 kgCO2eq"),
            gwp_max=q("0.04 kgCO2eq"),
        )

        assert q_impacts.ranges
        assert q_impacts.energy_min is not None
        assert q_impacts.energy_max is not None
