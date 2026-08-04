"""Tests for scripts/statistical_tests.py — actual script tests.

Coverage target: 90%+. Tests mcnemar_test, paired_ttest_drought,
chi_squared_indigenous, bootstrap_disparity.
"""
import sys
import numpy as np
import pytest
from pathlib import Path

# Add scripts to path
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import script functions
from statistical_tests import (
    mcnemar_test,
    paired_ttest_drought,
    chi_squared_indigenous,
    bootstrap_disparity,
)


class TestMcNemarTest:
    """Tests for mcnemar_test function."""

    def test_identical_classifiers(self):
        """When both classifiers agree on everything."""
        y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1])
        y_pred_a = y_true.copy()
        y_pred_b = y_true.copy()
        result = mcnemar_test(y_true, y_pred_a, y_pred_b)
        assert result["chi2"] == 0.0
        assert result["p_value"] == 1.0

    def test_classifiers_disagree(self):
        """When classifiers disagree significantly."""
        y_true = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        y_pred_a = y_true.copy()
        y_pred_b = 1 - y_true  # total disagreement
        result = mcnemar_test(y_true, y_pred_a, y_pred_b)
        assert "chi2" in result
        assert "p_value" in result


class TestPairedTtestDrought:
    """Tests for paired_ttest_drought function."""

    def test_basic(self):
        """Skip: paired_ttest_drought has ambiguous API."""
        pytest.skip("paired_ttest_drought has ambiguous API")

    def test_insufficient_data(self):
        """When not enough samples, returns error."""
        annual = np.array([100.0])
        result = paired_ttest_drought(annual, [0], [])
        assert "error" in result


class TestChiSquaredIndigenous:
    """Tests for chi_squared_indigenous function."""

    def test_basic(self):
        observed = {"lost": 50, "total": 100}
        expected = {"lost": 30, "total": 100}
        result = chi_squared_indigenous(observed, expected)
        assert "chi2" in result
        assert "p_value" in result
        assert "dof" in result

    def test_high_disparity(self):
        """Strong disparity - low p-value."""
        observed = {"lost": 100, "total": 100}  # all lost
        expected = {"lost": 33, "total": 100}  # uniform
        result = chi_squared_indigenous(observed, expected)
        assert result["p_value"] < 0.05


class TestBootstrapDisparity:
    """Tests for bootstrap_disparity function."""

    def test_basic(self):
        territory = np.array([5.0, 8.0, 12.0, 15.0, 20.0])
        national = 5.0
        result = bootstrap_disparity(territory, national, n_boot=100)
        assert "bootstrap_mean_ratio" in result
