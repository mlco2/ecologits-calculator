"""Shared pytest configuration and fixtures."""

from unittest.mock import MagicMock, patch

import pytest

# Patch st.cache_data BEFORE any test module imports src.repositories.models,
# so the decorator is a no-op instead of the real Streamlit caching wrapper.
_cache_data_patcher = patch(
    "streamlit.cache_data",
    side_effect=lambda f=None, **kwargs: f if f is not None else (lambda f: f),
)
_cache_data_patcher.start()

from src.core.units import q


@pytest.fixture
def sample_energy_quantity():
    """Return a sample energy quantity for testing."""
    return q("0.05 kWh")


@pytest.fixture
def sample_gwp_quantity():
    """Return a sample GWP (carbon) quantity for testing."""
    return q("0.03 kgCO2eq")


@pytest.fixture
def sample_adpe_quantity():
    """Return a sample ADPe quantity for testing."""
    return q("0.001 kgSbeq")


@pytest.fixture
def sample_pe_quantity():
    """Return a sample PE (primary energy) quantity for testing."""
    return q("0.5 MJ")


@pytest.fixture
def sample_wcf_quantity():
    """Return a sample WCF (water) quantity for testing."""
    return q("0.1 L")


@pytest.fixture
def mock_model():
    """Return a mock ecologits model."""
    mock = MagicMock()
    mock.name = "gpt-4"
    mock.provider.value = "openai"
    mock.architecture.type.value = "dense"
    mock.architecture.parameters = 1700
    mock.warnings = []
    return mock


@pytest.fixture
def mock_moe_model():
    """Return a mock MoE (Mixture of Experts) model."""
    mock = MagicMock()
    mock.name = "mistral-large-latest"
    mock.provider.value = "mistralai"
    mock.architecture.type.value = "moe"

    # Mock MoE parameters
    total_params = MagicMock()
    total_params.__class__.__name__ = "RangeValue"
    total_params.min = 41000
    total_params.max = 41000

    active_params = MagicMock()
    active_params.__class__.__name__ = "RangeValue"
    active_params.min = 14000
    active_params.max = 14000

    mock.architecture.parameters.total = total_params
    mock.architecture.parameters.active = active_params
    mock.warnings = []
    return mock


@pytest.fixture
def streamlit_mock():
    """No-op fixture for backward compatibility.

    Streamlit's cache_data is patched at module level above, so this fixture
    is kept only to avoid breaking test signatures that reference it.
    """
    yield
