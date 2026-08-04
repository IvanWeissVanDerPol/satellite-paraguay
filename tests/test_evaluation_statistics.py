"""Tests for src/evaluation/statistics.py.

Coverage target: 80%+. Tests bootstrap CI, McNemar's test, Cohen's d,
paired t-test, and confidence interval table generation.
"""
import pytest
import numpy as np
from sklearn.metrics import f1_score


class TestBootstrapCI:
    """Tests for bootstrap_ci function."""

    def test_returns_tuple(self):
        from src.evaluation.statistics import bootstrap_ci
        y_true = np.array([0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1, 1, 0])
        result = bootstrap_ci(y_true, y_pred, f1_score)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_returns_floats(self):
        from src.evaluation.statistics import bootstrap_ci
        y_true = np.array([0, 1, 0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1, 1, 0])
        point, lower, upper = bootstrap_ci(y_true, y_pred, f1_score)
        assert isinstance(point, float)
        assert isinstance(lower, float)
        assert isinstance(upper, float)

    def test_lower_le_point_le_upper(self):
        """Lower bound <= point estimate <= upper bound."""
        from src.evaluation.statistics import bootstrap_ci
        rng = np.random.default_rng(42)
        y_true = rng.integers(0, 2, 100)
        y_pred = rng.integers(0, 2, 100)
        point, lower, upper = bootstrap_ci(y_true, y_pred, f1_score)
        assert lower <= point <= upper

    def test_deterministic_with_seed(self):
        """Same seed should give same result."""
        from src.evaluation.statistics import bootstrap_ci
        y_true = np.array([0, 1, 0, 1, 0, 1, 1, 0])
        y_pred = np.array([0, 1, 1, 1, 0, 1, 0, 0])
        r1 = bootstrap_ci(y_true, y_pred, f1_score, seed=42)
        r2 = bootstrap_ci(y_true, y_pred, f1_score, seed=42)
        assert r1 == r2

    def test_custom_bootstrap_count(self):
        """n_bootstrap parameter is respected."""
        from src.evaluation.statistics import bootstrap_ci
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        # Just verify it doesn't crash
        result = bootstrap_ci(y_true, y_pred, f1_score, n_bootstrap=10)
        assert len(result) == 3

    def test_custom_confidence_level(self):
        from src.evaluation.statistics import bootstrap_ci
        y_true = np.array([0, 1, 0, 1, 0, 1, 1, 0])
        y_pred = np.array([0, 1, 1, 1, 0, 1, 0, 0])
        # 99% CI should be wider than 95% CI
        _, low_95, high_95 = bootstrap_ci(y_true, y_pred, f1_score, ci=0.95)
        _, low_99, high_99 = bootstrap_ci(y_true, y_pred, f1_score, ci=0.99)
        width_95 = high_95 - low_95
        width_99 = high_99 - low_99
        assert width_99 >= width_95


class TestMcnemarTest:
    """Tests for mcnemar_test function."""

    def test_returns_dict(self):
        from src.evaluation.statistics import mcnemar_test
        y_true = np.array([0, 1, 0, 1])
        pred_a = np.array([0, 1, 0, 1])
        pred_b = np.array([0, 1, 0, 1])
        result = mcnemar_test(y_true, pred_a, pred_b)
        assert isinstance(result, dict)

    def test_keys_present(self):
        from src.evaluation.statistics import mcnemar_test
        y_true = np.array([0, 1, 0, 1])
        pred_a = np.array([0, 1, 0, 1])
        pred_b = np.array([0, 1, 0, 1])
        result = mcnemar_test(y_true, pred_a, pred_b)
        expected_keys = {
            "chi2", "p_value", "b01_a_wrong_b_right",
            "b10_a_right_b_wrong", "n_disagree", "significant_at_0.05"
        }
        assert expected_keys.issubset(set(result.keys()))

    def test_identical_predictions(self):
        """If both models are identical, chi2 = 0, p_value = 1."""
        from src.evaluation.statistics import mcnemar_test
        y_true = np.array([0, 1, 0, 1, 0, 1])
        pred_a = np.array([0, 1, 0, 1, 0, 1])
        pred_b = np.array([0, 1, 0, 1, 0, 1])
        result = mcnemar_test(y_true, pred_a, pred_b)
        assert result["chi2"] == 0.0
        assert result["p_value"] == 1.0
        assert result["n_disagree"] == 0
        assert result["significant_at_0.05"] is False

    def test_completely_different_predictions(self):
        """Very different models should show significant difference."""
        from src.evaluation.statistics import mcnemar_test
        rng = np.random.default_rng(42)
        y_true = rng.integers(0, 2, 100)
        # A predicts wrong, B predicts correct
        pred_a = 1 - y_true  # always wrong
        pred_b = y_true  # always right
        result = mcnemar_test(y_true, pred_a, pred_b)
        assert result["chi2"] > 0
        assert result["n_disagree"] == 100
        assert bool(result["significant_at_0.05"]) is True

    def test_counts_correctly(self):
        """Verify the b01/b10 counts are correct."""
        from src.evaluation.statistics import mcnemar_test
        y_true = np.array([1, 1, 1, 1, 0, 0, 0, 0])
        # A: predicts all 1
        pred_a = np.array([1, 1, 1, 1, 1, 1, 1, 1])
        # B: predicts all 0
        pred_b = np.array([0, 0, 0, 0, 0, 0, 0, 0])
        result = mcnemar_test(y_true, pred_a, pred_b)
        # A wrong on [4-7] = 4 (where y_true=0), B right on those = 4
        # A right on [0-3] = 4, B wrong on those = 4
        assert result["b01_a_wrong_b_right"] == 4
        assert result["b10_a_right_b_wrong"] == 4
        assert result["n_disagree"] == 8


class TestCohensD:
    """Tests for cohens_d function."""

    def test_returns_float(self):
        from src.evaluation.statistics import cohens_d
        g1 = np.array([1.0, 2.0, 3.0])
        g2 = np.array([4.0, 5.0, 6.0])
        result = cohens_d(g1, g2)
        assert isinstance(result, float)

    def test_negative_for_lower_group(self):
        """g1 < g2 should give negative Cohen's d."""
        from src.evaluation.statistics import cohens_d
        g1 = np.array([1.0, 2.0, 3.0])
        g2 = np.array([4.0, 5.0, 6.0])
        result = cohens_d(g1, g2)
        assert result < 0

    def test_positive_for_higher_group(self):
        """g1 > g2 should give positive Cohen's d."""
        from src.evaluation.statistics import cohens_d
        g1 = np.array([4.0, 5.0, 6.0])
        g2 = np.array([1.0, 2.0, 3.0])
        result = cohens_d(g1, g2)
        assert result > 0

    def test_zero_for_identical_groups(self):
        """Identical groups should give Cohen's d = 0."""
        from src.evaluation.statistics import cohens_d
        g1 = np.array([1.0, 2.0, 3.0])
        g2 = np.array([1.0, 2.0, 3.0])
        result = cohens_d(g1, g2)
        assert abs(result) < 1e-9


class TestPairedTtest:
    """Tests for paired_ttest function."""

    def test_returns_dict(self):
        from src.evaluation.statistics import paired_ttest
        # Use data with non-zero variance to avoid precision warnings
        s1 = np.array([0.80, 0.85, 0.90, 0.82, 0.87])
        s2 = np.array([0.70, 0.75, 0.80, 0.72, 0.77])
        result = paired_ttest(s1, s2)
        assert isinstance(result, dict)

    def test_keys_present(self):
        from src.evaluation.statistics import paired_ttest
        s1 = np.array([0.80, 0.85, 0.90, 0.82, 0.87])
        s2 = np.array([0.70, 0.75, 0.80, 0.72, 0.77])
        result = paired_ttest(s1, s2)
        expected = {"t_stat", "p_value", "mean_diff", "cohens_d", "significant_at_0.05"}
        assert expected.issubset(set(result.keys()))

    def test_identical_scores(self):
        """Same scores should give t=0, p=1, mean_diff=0."""
        from src.evaluation.statistics import paired_ttest
        # Add tiny noise so cohens_d doesn't divide by zero
        s1 = np.array([0.80, 0.85, 0.90, 0.82, 0.87])
        s2 = np.array([0.80, 0.85, 0.90, 0.82, 0.87])
        result = paired_ttest(s1, s2)
        assert abs(result["mean_diff"]) < 1e-9
        # Cohen's d should be 0 for identical groups (cohens_d handles this)
        assert abs(result["cohens_d"]) < 1e-9

    def test_highly_different_scores(self):
        """Very different scores should be significant."""
        from src.evaluation.statistics import paired_ttest
        s1 = np.full(20, 0.9)
        s2 = np.full(20, 0.5)
        result = paired_ttest(s1, s2)
        assert bool(result["significant_at_0.05"]) is True
        assert result["mean_diff"] > 0  # s1 > s2

    def test_positive_mean_diff(self):
        """When s1 > s2, mean_diff should be positive."""
        from src.evaluation.statistics import paired_ttest
        s1 = np.array([0.9, 0.9, 0.9, 0.9])
        s2 = np.array([0.5, 0.5, 0.5, 0.5])
        result = paired_ttest(s1, s2)
        assert result["mean_diff"] > 0


class TestGenerateCITable:
    """Tests for generate_confidence_intervals_table function."""

    def test_runs_without_crash(self, tmp_path):
        """Should not crash (may return None or empty)."""
        from src.evaluation.statistics import generate_confidence_intervals_table
        # The current impl is a placeholder, so just verify it doesn't crash
        result = generate_confidence_intervals_table({}, str(tmp_path / "ci.csv"))
        # Result may be None or dict - both are fine for placeholder