"""Tests for src/baselines/p0100_yvyra_baselines.py — regression baselines
for carbon credit estimation.
"""
import pytest
import numpy as np

try:
    import sklearn  # noqa: F401
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


class TestP0100Baselines:
    """Tests for src/baselines/p0100_yvyra_baselines.py."""

    @pytest.fixture
    def module(self):
        from src.baselines import p0100_yvyra_baselines
        return p0100_yvyra_baselines

    @pytest.fixture
    def features(self):
        """Synthetic features: (100, 5)"""
        rng = np.random.default_rng(42)
        return rng.normal(0, 1, (100, 5)).astype(np.float32)

    @pytest.fixture
    def target(self):
        """Synthetic target: (100,)"""
        rng = np.random.default_rng(43)
        return rng.normal(50, 10, 100).astype(np.float32)

    # --- persistence_baseline ---

    def test_persistence_returns_correct_shape(self, module, target):
        preds = module.persistence_baseline(target)
        assert preds.shape == target.shape

    def test_persistence_predicts_mean(self, module, target):
        preds = module.persistence_baseline(target)
        expected_mean = np.mean(target)
        np.testing.assert_array_almost_equal(preds, expected_mean)

    def test_persistence_constant(self, module, target):
        """All predictions should be the same value."""
        preds = module.persistence_baseline(target)
        assert np.all(preds == preds[0])

    # --- linear_regression_baseline ---

    @pytest.mark.skipif(not HAS_SKLEARN, reason="scikit-learn not installed")
    def test_linear_regression_returns_correct_shape(self, module, features, target):
        preds = module.linear_regression_baseline(features, target)
        assert preds.shape == target.shape

    @pytest.mark.skipif(not HAS_SKLEARN, reason="scikit-learn not installed")
    def test_linear_regression_simple_pattern(self, module):
        """If y = 2*x + 1, the regression should approximate it."""
        x = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
        y = 2 * x.flatten() + 1
        preds = module.linear_regression_baseline(x, y)
        # Ridge has alpha=1.0 so won't perfectly fit, but should be approximately
        # monotonic and close to y
        assert preds[0] < preds[-1]  # monotonic increase
        assert abs(preds[2] - 7.0) < 1.0  # middle point within 1.0

    # --- random_forest_regression_baseline ---

    @pytest.mark.skipif(not HAS_SKLEARN, reason="scikit-learn not installed")
    def test_random_forest_returns_correct_shape(self, module, features, target):
        preds = module.random_forest_regression_baseline(
            features, target, n_estimators=10
        )
        assert preds.shape == target.shape

    @pytest.mark.skipif(not HAS_SKLEARN, reason="scikit-learn not installed")
    def test_random_forest_deterministic(self, module, features, target):
        a = module.random_forest_regression_baseline(
            features, target, n_estimators=10, random_state=42
        )
        b = module.random_forest_regression_baseline(
            features, target, n_estimators=10, random_state=42
        )
        np.testing.assert_array_equal(a, b)

    # --- run_all_baselines ---

    def test_run_all_baselines_returns_dict(self, module, features, target):
        results = module.run_all_baselines(features, target)
        assert isinstance(results, dict)
        assert "persistence" in results
        assert "linear_regression" in results
        assert "random_forest" in results

    def test_run_all_baselines_persistence_has_metrics(self, module, features, target):
        results = module.run_all_baselines(features, target)
        # Persistence dict should have metric keys
        per = results["persistence"]
        assert isinstance(per, dict)
        # Common regression metrics: rmse, mae, r2, etc.
        assert any(key in per for key in ["rmse", "mae", "r2", "mse"])
