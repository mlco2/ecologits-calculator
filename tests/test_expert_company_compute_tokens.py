"""Tests for token computation in expert company mode."""

import pytest

from src.ui.pages.expert_company import _compute_row_tokens


class TestComputeRowTokens:
    """Test the _compute_row_tokens function."""

    def test_valid_input(self):
        """Test with valid input values."""
        assert _compute_row_tokens(
            {
                "Tokens per User per Selected Unit of Time": "500",
                "Number of Users": "100",
            }
        ) == 50_000

    def test_empty_num_users(self):
        """Test with empty number of users."""
        row = {
            "Tokens per User per Selected Unit of Time": "500",
            "Number of Users": "",
        }

        with pytest.raises(ValueError, match="Number of users cannot be empty or None"):
            _compute_row_tokens(row)

    def test_none_num_users(self):
        """Test with None number of users."""
        row = {
            "Tokens per User per Selected Unit of Time": "500",
            "Number of Users": None,
        }

        with pytest.raises(ValueError, match="Number of users cannot be empty or None"):
            _compute_row_tokens(row)

    def test_negative_num_users(self):
        """Test with negative number of users."""
        row = {
            "Tokens per User per Selected Unit of Time": "500",
            "Number of Users": "-100",
        }

        with pytest.raises(ValueError, match="Number of users must be non-negative"):
            _compute_row_tokens(row)

    def test_invalid_num_users_string(self):
        """Test with invalid string for number of users."""
        row = {
            "Tokens per User per Selected Unit of Time": "500",
            "Number of Users": "not_a_number",
        }

        with pytest.raises(ValueError, match="Invalid number of users value"):
            _compute_row_tokens(row)

    def test_zero_tokens_per_user(self):
        """Test with zero tokens per user (should be valid)."""
        row = {
            "Tokens per User per Selected Unit of Time": "0",
            "Number of Users": "100",
        }

        result = _compute_row_tokens(row)

        # Should return zero tokens
        assert result == 0
