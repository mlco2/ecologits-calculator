"""Tests for token computation in expert company mode."""

import pytest

from src.config.constants import PROMPTS, USAGE_INTENSITY
from src.ui.expert_company import _compute_row_tokens


class TestComputeRowTokens:
    """Test the _compute_row_tokens function."""

    def test_valid_input(self):
        """Test with valid input values."""
        row = {
            "_COL_USAGE_TYPE": "Write a tweet (50 output tokens)",
            "_COL_USAGE_INTENSITY": "Light (x1-x3)",
            "_COL_NUM_USERS": "100",
        }

        # Mock the column names
        import src.ui.expert_company as expert_company

        expert_company._COL_USAGE_TYPE = "_COL_USAGE_TYPE"
        expert_company._COL_USAGE_INTENSITY = "_COL_USAGE_INTENSITY"
        expert_company._COL_NUM_USERS = "_COL_NUM_USERS"

        result = _compute_row_tokens(row)

        # Find the prompt
        prompt = next(p for p in PROMPTS if p.label == "Write a tweet (50 output tokens)")
        daily_count = USAGE_INTENSITY["Light (x1-x3)"]
        num_users = 100

        expected = {
            "output_tokens": prompt.output_tokens * daily_count * num_users,
            "input_tokens": prompt.input_tokens * daily_count * num_users,
            "cached_tokens": prompt.cached_tokens * daily_count * num_users,
            "total_tokens": (prompt.output_tokens + prompt.input_tokens + prompt.cached_tokens)
            * daily_count
            * num_users,
        }

        assert result == expected

    def test_empty_num_users(self):
        """Test with empty number of users."""
        row = {
            "_COL_USAGE_TYPE": "Write a tweet (50 output tokens)",
            "_COL_USAGE_INTENSITY": "Light (x1-x3)",
            "_COL_NUM_USERS": "",
        }

        import src.ui.expert_company as expert_company

        expert_company._COL_USAGE_TYPE = "_COL_USAGE_TYPE"
        expert_company._COL_USAGE_INTENSITY = "_COL_USAGE_INTENSITY"
        expert_company._COL_NUM_USERS = "_COL_NUM_USERS"

        with pytest.raises(ValueError, match="Number of users cannot be empty or None"):
            _compute_row_tokens(row)

    def test_none_num_users(self):
        """Test with None number of users."""
        row = {
            "_COL_USAGE_TYPE": "Write a tweet (50 output tokens)",
            "_COL_USAGE_INTENSITY": "Light (x1-x3)",
            "_COL_NUM_USERS": None,
        }

        import src.ui.expert_company as expert_company

        expert_company._COL_USAGE_TYPE = "_COL_USAGE_TYPE"
        expert_company._COL_USAGE_INTENSITY = "_COL_USAGE_INTENSITY"
        expert_company._COL_NUM_USERS = "_COL_NUM_USERS"

        with pytest.raises(ValueError, match="Number of users cannot be empty or None"):
            _compute_row_tokens(row)

    def test_negative_num_users(self):
        """Test with negative number of users."""
        row = {
            "_COL_USAGE_TYPE": "Write a tweet (50 output tokens)",
            "_COL_USAGE_INTENSITY": "Light (x1-x3)",
            "_COL_NUM_USERS": "-100",
        }

        import src.ui.expert_company as expert_company

        expert_company._COL_USAGE_TYPE = "_COL_USAGE_TYPE"
        expert_company._COL_USAGE_INTENSITY = "_COL_USAGE_INTENSITY"
        expert_company._COL_NUM_USERS = "_COL_NUM_USERS"

        with pytest.raises(ValueError, match="Number of users must be non-negative"):
            _compute_row_tokens(row)

    def test_invalid_num_users_string(self):
        """Test with invalid string for number of users."""
        row = {
            "_COL_USAGE_TYPE": "Write a tweet (50 output tokens)",
            "_COL_USAGE_INTENSITY": "Light (x1-x3)",
            "_COL_NUM_USERS": "not_a_number",
        }

        import src.ui.expert_company as expert_company

        expert_company._COL_USAGE_TYPE = "_COL_USAGE_TYPE"
        expert_company._COL_USAGE_INTENSITY = "_COL_USAGE_INTENSITY"
        expert_company._COL_NUM_USERS = "_COL_NUM_USERS"

        with pytest.raises(ValueError, match="Invalid number of users value"):
            _compute_row_tokens(row)

    def test_zero_num_users(self):
        """Test with zero number of users (should be valid)."""
        row = {
            "_COL_USAGE_TYPE": "Write a tweet (50 output tokens)",
            "_COL_USAGE_INTENSITY": "Light (x1-x3)",
            "_COL_NUM_USERS": "0",
        }

        import src.ui.expert_company as expert_company

        expert_company._COL_USAGE_TYPE = "_COL_USAGE_TYPE"
        expert_company._COL_USAGE_INTENSITY = "_COL_USAGE_INTENSITY"
        expert_company._COL_NUM_USERS = "_COL_NUM_USERS"

        result = _compute_row_tokens(row)

        # Should return all zeros
        assert result == {
            "output_tokens": 0,
            "input_tokens": 0,
            "cached_tokens": 0,
            "total_tokens": 0,
        }
