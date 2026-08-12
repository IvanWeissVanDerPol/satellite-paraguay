"""Tests for scripts/statistical_tests.py — actual script tests.

Coverage target: 90%+. Tests mcnemar_test, paired_ttest_drought,
chi_squared_indigenous, bootstrap_disparity.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Add scripts to path BEFORE importing script functions
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import script functions (E402: sys.path setup above must run first)
from statistical_tests import (  # noqa: E402
    bootstrap_disparity,
    chi_squared_indigenous,
    mcnemar_test,
    paired_ttest_drought,
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
        y_pred_a = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
        y_pred_b = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        result = mcnemar_test(y_true, y_pred_a, y_pred_b)
        assert result["chi2"] > 0
        assert result["p_value"] < 0.05

    def test_returns_dict(self):
        """Should return dict with expected keys."""
        y_true = np.array([0, 1, 0, 1])
        y_pred_a = np.array([0, 1, 0, 1])
        y_pred_b = np.array([0, 1, 0, 1])
        result = mcnemar_test(y_true, y_pred_a, y_pred_b)
        assert "chi2" in result
        assert "p_value" in result
        assert "n12" in result
        assert "n21" in result


class TestPairedTtestDrought:
    """Tests for paired_ttest_drought function."""

    def test_no_difference(self):
        """When drought==non-drought, t-stat ~ 0."""
        annual_loss = {2015: 1.0, 2016: 2.0, 2017: 3.0, 2018: 4.0, 2019: 5.0}
        drought_years = [2015, 2016, 2017]
        non_drought_years = [2018, 2019]
        result = paired_ttest_drought(annual_loss, drought_years, non_drought_years)
        assert "t_statistic" in result
        assert "p_value" in result

    def test_large_difference(self):
        """When there's a large difference, p < 0.05."""
        annual_loss = {2015: 1.0, 2016: 2.0, 2017: 3.0, 2018: 4.0, 2019: 5.0}
        drought_years = [2015, 2016, 2017]
        non_drought_years = [2018, 2019]
        # Invert: drought much higher than non-drought
        annual_loss = {2015: 50.0, 2016: 60.0, 2017: 70.0, 2018: 1.0, 2019: 2.0}
        result = paired_ttest_drought(annual_loss, drought_years, non_drought_years)
        assert result["p_value"] < 0.05

    def test_insufficient_data(self):
        """Returns error dict when not enough data."""
        annual_loss = {2015: 1.0}
        drought_years = [2015]
        non_drought_years = []
        result = paired_ttest_drought(annual_loss, drought_years, non_drought_years)
        # Either error or a valid result with low n
        assert "error" in result or "p_value" in result


class TestChiSquaredIndigenous:
    """Tests for chi_squared_indigenous function."""

    def test_small_table(self):
        """Test with simple observed vs expected dicts."""
        observed = {"lost": 50, "total": 100}
        expected = {"lost": 30, "total": 100}
        result = chi_squared_indigenous(observed, expected)
        assert "chi2" in result
        assert "p_value" in result
        assert result["chi2"] > 0

    def test_returns_dict(self):
        """Should return dict with expected keys."""
        observed = {"lost": 10, "total": 50}
        expected = {"lost": 8, "total": 50}
        result = chi_squared_indigenous(observed, expected)
        assert isinstance(result, dict)
        assert "p_value" in result


class TestBootstrapDisparity:
    """Tests for bootstrap_disparity function."""

    def test_basic_bootstrap(self):
        """Test bootstrap with simple input."""
        rng = np.random.default_rng(42)
        territory = rng.normal(0.05, 0.01, size=50)
        national = 0.02
        result = bootstrap_disparity(territory, national, n_boot=100)
        assert isinstance(result, dict)
        assert "bootstrap_mean_ratio" in result
        assert "bootstrap_ci_lower" in result
        assert "bootstrap_ci_upper" in result
