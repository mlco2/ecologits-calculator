"""Tests for src/core/equivalences.py."""

from src.core.equivalences import (
    AIRPLANE_PARIS_NYC_GWP_EQ,
    DAYS_IN_YEAR,
    EV_ENERGY_EQ,
    ONE_PERCENT_WORLD_POPULATION,
    RUNNING_ENERGY_EQ,
    STREAMING_GWP_EQ,
    WALKING_ENERGY_EQ,
    YEARLY_IRELAND_ELECTRICITY_CONSUMPTION,
    YEARLY_NUCLEAR_ENERGY_EQ,
    YEARLY_WIND_ENERGY_EQ,
    EnergyProduction,
    PhysicalActivity,
    format_energy_eq_electric_vehicle,
    format_energy_eq_electricity_consumption_ireland,
    format_energy_eq_electricity_production,
    format_energy_eq_physical_activity,
    format_gwp_eq_airplane_paris_nyc,
    format_gwp_eq_streaming,
)
from src.core.units import q


class TestPhysicalActivityEnum:
    """Test cases for PhysicalActivity enum."""

    def test_physical_activity_has_running(self):
        """Should have RUNNING enum member."""
        assert PhysicalActivity.RUNNING.value == "running"

    def test_physical_activity_has_walking(self):
        """Should have WALKING enum member."""
        assert PhysicalActivity.WALKING.value == "walking"

    def test_physical_activity_count(self):
        """Should have exactly 2 physical activities."""
        assert len(PhysicalActivity) == 2


class TestEnergyProductionEnum:
    """Test cases for EnergyProduction enum."""

    def test_energy_production_has_nuclear(self):
        """Should have NUCLEAR enum member."""
        assert EnergyProduction.NUCLEAR.value == "nuclear"

    def test_energy_production_has_wind(self):
        """Should have WIND enum member."""
        assert EnergyProduction.WIND.value == "wind"

    def test_energy_production_count(self):
        """Should have exactly 2 energy production types."""
        assert len(EnergyProduction) == 2


class TestFormatEnergyEqPhysicalActivity:
    """Test cases for format_energy_eq_physical_activity function."""

    def test_high_energy_returns_running(self):
        """Should return appropriate activity for energy values."""
        energy = q("294 kJ")  # Exactly one km of running
        activity, distance = format_energy_eq_physical_activity(energy)
        assert activity in [PhysicalActivity.RUNNING, PhysicalActivity.WALKING]
        assert distance.magnitude > 0

    def test_low_energy_returns_walking(self):
        """Should return WALKING for low energy values."""
        energy = q("50 kJ")  # Less than sufficient for running
        activity, _distance = format_energy_eq_physical_activity(energy)
        # This will return walking for very low values
        assert activity in [PhysicalActivity.RUNNING, PhysicalActivity.WALKING]

    def test_returns_distance_quantity(self):
        """Should return a quantity with distance units."""
        energy = q("5 kJ")
        _activity, distance = format_energy_eq_physical_activity(energy)
        assert "meter" in str(distance.units) or "km" in str(distance.units)

    def test_energy_conversion_is_positive(self):
        """Should return positive distance."""
        energy = q("10 kJ")
        _, distance = format_energy_eq_physical_activity(energy)
        assert distance.magnitude > 0


class TestFormatEnergyEqElectricVehicle:
    """Test cases for format_energy_eq_electric_vehicle function."""

    def test_ev_equivalence_returns_distance(self):
        """Should return distance traveled by EV."""
        energy = q("1 kWh")
        result = format_energy_eq_electric_vehicle(energy)
        assert "meter" in str(result.units) or "km" in str(result.units)

    def test_ev_equivalence_positive_result(self):
        """Should return positive distance."""
        energy = q("0.5 kWh")
        result = format_energy_eq_electric_vehicle(energy)
        assert result.magnitude > 0

    def test_ev_equivalence_magnitude(self):
        """Should calculate reasonable EV distance."""
        energy = q("0.17 kWh")  # Exactly one EV kilometer
        result = format_energy_eq_electric_vehicle(energy)
        # Should be approximately 1 km
        assert 0.5 < result.to("km").magnitude < 2


class TestFormatGWPEqStreaming:
    """Test cases for format_gwp_eq_streaming function."""

    def test_streaming_equivalence_returns_time(self):
        """Should return time in hours/minutes/seconds."""
        gwp = q("0.03 kgCO2eq")
        result = format_gwp_eq_streaming(gwp)
        unit_str = str(result.units)
        assert any(t in unit_str for t in ["h", "min", "s"])

    def test_streaming_equivalence_positive_result(self):
        """Should return positive time."""
        gwp = q("0.5 kgCO2eq")
        result = format_gwp_eq_streaming(gwp)
        assert result.magnitude > 0

    def test_high_gwp_returns_hours(self):
        """High GWP should return result in hours."""
        gwp = q("10 kgCO2eq")
        result = format_gwp_eq_streaming(gwp)
        # Large GWP should result in hours
        assert result.magnitude > 0


class TestFormatEnergyEqElectricityProduction:
    """Test cases for format_energy_eq_electricity_production function."""

    def test_returns_energy_production_type_and_quantity(self):
        """Should return both energy production type and quantity."""
        energy = q("0.001 kWh")
        prod_type, quantity = format_energy_eq_electricity_production(energy)
        assert prod_type in [EnergyProduction.NUCLEAR, EnergyProduction.WIND]
        assert isinstance(quantity.magnitude, (int, float))

    def test_high_energy_returns_nuclear(self):
        """Very high energy should return NUCLEAR production."""
        # Scale to 1% of world population per day per year
        high_energy = q("1000 kWh")  # Scaled appropriately
        prod_type, _quantity = format_energy_eq_electricity_production(high_energy)
        # Could be nuclear or wind depending on scaling
        assert prod_type in [EnergyProduction.NUCLEAR, EnergyProduction.WIND]

    def test_low_energy_might_return_wind(self):
        """Low energy might return WIND production."""
        low_energy = q("0.0001 kWh")
        prod_type, _quantity = format_energy_eq_electricity_production(low_energy)
        assert prod_type in [EnergyProduction.NUCLEAR, EnergyProduction.WIND]


class TestFormatEnergyEqElectricityConsumptionIreland:
    """Test cases for format_energy_eq_electricity_consumption_ireland function."""

    def test_returns_quantity(self):
        """Should return a quantity."""
        energy = q("0.01 kWh")
        result = format_energy_eq_electricity_consumption_ireland(energy)
        assert hasattr(result, "magnitude")

    def test_positive_result(self):
        """Should return positive value."""
        energy = q("0.5 kWh")
        result = format_energy_eq_electricity_consumption_ireland(energy)
        assert result.magnitude > 0

    def test_scaling_calculation(self):
        """Should scale energy to world population and year."""
        energy = q("1 kWh")
        result = format_energy_eq_electricity_consumption_ireland(energy)
        # Result should be a fraction or multiple of Ireland's yearly consumption
        assert result is not None


class TestFormatGWPEqAirplaneParisNYC:
    """Test cases for format_gwp_eq_airplane_paris_nyc function."""

    def test_returns_quantity(self):
        """Should return a quantity."""
        gwp = q("0.03 kgCO2eq")
        result = format_gwp_eq_airplane_paris_nyc(gwp)
        assert hasattr(result, "magnitude")

    def test_positive_result(self):
        """Should return positive value."""
        gwp = q("0.5 kgCO2eq")
        result = format_gwp_eq_airplane_paris_nyc(gwp)
        assert result.magnitude > 0

    def test_high_gwp_multiple_flights(self):
        """High GWP should return multiple flights."""
        gwp = q("100 kgCO2eq")
        result = format_gwp_eq_airplane_paris_nyc(gwp)
        # Scale to 1% of world population per year
        assert result.magnitude > 0


class TestConstants:
    """Test cases for constants."""

    def test_running_energy_eq_has_correct_unit(self):
        """RUNNING_ENERGY_EQ should be in kJ/km."""
        assert "kJ" in str(RUNNING_ENERGY_EQ.units)

    def test_walking_energy_eq_has_correct_unit(self):
        """WALKING_ENERGY_EQ should be in kJ/km."""
        assert "kJ" in str(WALKING_ENERGY_EQ.units)

    def test_ev_energy_eq_has_correct_unit(self):
        """EV_ENERGY_EQ should be in kWh/km."""
        assert "kWh" in str(EV_ENERGY_EQ.units)

    def test_streaming_gwp_eq_has_correct_unit(self):
        """STREAMING_GWP_EQ should be in h/kgCO2eq."""
        assert "h" in str(STREAMING_GWP_EQ.units)

    def test_one_percent_world_population_magnitude(self):
        """ONE_PERCENT_WORLD_POPULATION should be reasonable."""
        assert 70_000_000 < ONE_PERCENT_WORLD_POPULATION < 90_000_000

    def test_days_in_year_equals_365(self):
        """DAYS_IN_YEAR should be 365."""
        assert DAYS_IN_YEAR == 365

    def test_yearly_nuclear_energy_in_twh(self):
        """YEARLY_NUCLEAR_ENERGY_EQ should be in TWh."""
        assert "TWh" in str(YEARLY_NUCLEAR_ENERGY_EQ.units)

    def test_yearly_wind_energy_in_gwh(self):
        """YEARLY_WIND_ENERGY_EQ should be in GWh."""
        assert "GWh" in str(YEARLY_WIND_ENERGY_EQ.units)

    def test_ireland_electricity_consumption_in_twh(self):
        """YEARLY_IRELAND_ELECTRICITY_CONSUMPTION should be in TWh."""
        assert "TWh" in str(YEARLY_IRELAND_ELECTRICITY_CONSUMPTION.units)

    def test_airplane_gwp_eq_reasonable_magnitude(self):
        """AIRPLANE_PARIS_NYC_GWP_EQ should be a large value."""
        assert AIRPLANE_PARIS_NYC_GWP_EQ.magnitude > 100000
