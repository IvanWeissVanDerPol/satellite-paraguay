"""Tests for src/baselines/p0100_yvyra_baselines.py — run_all_baselines.

Coverage target: 100%+. Covers error handling paths.
"""

from unittest.mock import patch

import numpy as np


class TestRunAllBaselines:
    """Tests for run_all_baselines function."""

    def test_runs_all_baselines(self):
        """When all baselines succeed, returns 3 results."""
        from src.baselines.p0100_yvyra_baselines import run_all_baselines

        # 50 samples × 5 features, balanced target
        np.random.seed(42)
        features = np.random.rand(50, 5)
        target = features @ np.array([1, 0.5, 0, 0, 0]) + np.random.randn(50) * 0.1

        result = run_all_baselines(features, target)

        assert "persistence" in result
        assert "linear_regression" in result
        assert "random_forest" in result

    def test_linear_regression_failure(self):
        """When Ridge fails, records error."""
        from src.baselines.p0100_yvyra_baselines import run_all_baselines

        features = np.array([[1.0], [2.0]])
        target = np.array([1.0, 2.0])

        # Mock Ridge.fit to raise
        with patch(
            "src.baselines.p0100_yvyra_baselines.linear_regression_baseline", side_effect=ValueError("solver failed")
        ):
            result = run_all_baselines(features, target)

        # persistence should still run
        assert "persistence" in result
        # linear_regression should have error
        assert "linear_regression" in result
        assert "error" in result["linear_regression"]

    def test_random_forest_failure(self):
        """When RandomForest fails, records error."""
        from src.baselines.p0100_yvyra_baselines import run_all_baselines

        features = np.array([[1.0], [2.0]])
        target = np.array([1.0, 2.0])

        with patch(
            "src.baselines.p0100_yvyra_baselines.random_forest_regression_baseline",
            side_effect=ValueError("n_estimators invalid"),
        ):
            result = run_all_baselines(features, target)

        assert "random_forest" in result
        assert "error" in result["random_forest"]

    def test_both_baselines_fail(self):
        """When both baselines fail, persistence result still returned."""
        from src.baselines.p0100_yvyra_baselines import run_all_baselines

        features = np.array([[1.0]])
        target = np.array([1.0])

        with patch(
            "src.baselines.p0100_yvyra_baselines.linear_regression_baseline", side_effect=RuntimeError("lr fail")
        ):
            with patch(
                "src.baselines.p0100_yvyra_baselines.random_forest_regression_baseline",
                side_effect=RuntimeError("rf fail"),
            ):
                result = run_all_baselines(features, target)

        assert "persistence" in result
        assert "error" in result["linear_regression"]
        assert "error" in result["random_forest"]
