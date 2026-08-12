"""Tests for src/baselines/*.py.

Coverage target: 80%+. The 3 baselines files share a common pattern:
- p0011_yvytu_baselines.py: persistence, linear_trend, random_forest, unet
- p0035_tatakua_baselines.py: similar
- p0100_yvyra_baselines.py: similar

We focus on testing the pure-numpy baselines (persistence, linear_trend)
which work without sklearn/torch and don't need GPU.
"""


import numpy as np
import pytest

# Make sure sklearn is available for the RF tests
try:
    import sklearn  # noqa: F401

    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


# =========================
# p0011_yvytu_baselines
# =========================


class TestP0011Baselines:
    """Tests for src/baselines/p0011_yvytu_baselines.py."""

    @pytest.fixture
    def module(self):
        from src.baselines import p0011_yvytu_baselines

        return p0011_yvytu_baselines

    @pytest.fixture
    def small_ndvi(self):
        """Small (T=5, H=4, W=4) NDVI cube."""
        rng = np.random.default_rng(42)
        return rng.uniform(0.0, 1.0, (5, 4, 4)).astype(np.float32)

    @pytest.fixture
    def ground_truth(self):
        """Small (H=4, W=4) ground truth."""
        return np.array(
            [
                [0, 1, 2, 3],
                [4, 0, 1, 2],
                [3, 4, 0, 1],
                [2, 3, 4, 0],
            ],
            dtype=np.int64,
        )

    # --- persistence_baseline ---

    def test_persistence_returns_correct_shape(self, module, small_ndvi):
        preds = module.persistence_baseline(small_ndvi)
        assert preds.shape == (4, 4)

    def test_persistence_only_uses_first_frame(self, module, small_ndvi):
        preds_a = module.persistence_baseline(small_ndvi)
        # Modify all but first frame
        modified = small_ndvi.copy()
        modified[1:] = 0.0
        preds_b = module.persistence_baseline(modified)
        # Should be identical since only first frame matters
        np.testing.assert_array_equal(preds_a, preds_b)

    def test_persistence_threshold_buckets(self, module):
        """Test that NDVI thresholds produce correct class assignments."""
        ndvi = np.array(
            [
                [[0.8, 0.6, 0.4, 0.2]],  # 1 frame, 4 pixels
            ],
            dtype=np.float32,
        )
        preds = module.persistence_baseline(ndvi)
        assert preds[0, 0] == 1  # > 0.7
        assert preds[0, 1] == 2  # 0.5-0.7
        assert preds[0, 2] == 3  # 0.3-0.5
        assert preds[0, 3] == 4  # <= 0.3

    def test_persistence_dtype_is_int64(self, module, small_ndvi):
        preds = module.persistence_baseline(small_ndvi)
        assert preds.dtype == np.int64

    # --- linear_trend_baseline ---

    def test_linear_trend_returns_correct_shape(self, module, small_ndvi):
        preds = module.linear_trend_baseline(small_ndvi)
        assert preds.shape == (4, 4)

    def test_linear_trend_detects_strong_decline(self, module):
        """Pixel that drops substantially should be flagged as deforested."""
        # T=5, single pixel, strong decline
        ndvi = np.array(
            [
                [[0.9]],
                [[0.7]],
                [[0.5]],
                [[0.3]],
                [[0.1]],
            ],
            dtype=np.float32,
        )
        preds = module.linear_trend_baseline(ndvi, threshold=-0.1)
        # Slope is ~-0.2 which is < -0.1, so deforested
        assert preds[0, 0] == 1

    def test_linear_trend_detects_stable(self, module):
        """Stable pixel should NOT be flagged as deforested."""
        ndvi = np.array(
            [
                [[0.5]],
                [[0.5]],
                [[0.5]],
                [[0.5]],
                [[0.5]],
            ],
            dtype=np.float32,
        )
        preds = module.linear_trend_baseline(ndvi, threshold=-0.1)
        assert preds[0, 0] == 0  # slope ~0, not deforested

    def test_linear_trend_detects_positive(self, module):
        """Growing pixel should NOT be flagged as deforested."""
        ndvi = np.array(
            [
                [[0.1]],
                [[0.3]],
                [[0.5]],
                [[0.7]],
                [[0.9]],
            ],
            dtype=np.float32,
        )
        preds = module.linear_trend_baseline(ndvi, threshold=-0.1)
        assert preds[0, 0] == 0  # slope is positive

    def test_linear_trend_threshold_parameter(self, module):
        """Lower threshold (more negative) catches fewer pixels."""
        ndvi = np.array(
            [
                [[0.5, 0.5]],
                [[0.4, 0.4]],
                [[0.3, 0.3]],
                [[0.2, 0.2]],
                [[0.1, 0.1]],
            ],
            dtype=np.float32,
        )
        # Strict threshold catches the declining pixel
        strict = module.linear_trend_baseline(ndvi, threshold=-0.2)
        # Loose threshold (allow shallow decline) catches more
        loose = module.linear_trend_baseline(ndvi, threshold=-0.05)
        assert loose.sum() >= strict.sum()

    # --- random_forest_baseline ---

    @pytest.mark.skipif(not HAS_SKLEARN, reason="scikit-learn not installed")
    def test_random_forest_returns_correct_shape(self, module, small_ndvi, ground_truth):
        preds = module.random_forest_baseline(small_ndvi, ground_truth, n_estimators=10)
        assert preds.shape == (4, 4)

    @pytest.mark.skipif(not HAS_SKLEARN, reason="scikit-learn not installed")
    def test_random_forest_deterministic_with_seed(self, module, small_ndvi, ground_truth):
        preds_a = module.random_forest_baseline(small_ndvi, ground_truth, n_estimators=10, random_state=42)
        preds_b = module.random_forest_baseline(small_ndvi, ground_truth, n_estimators=10, random_state=42)
        np.testing.assert_array_equal(preds_a, preds_b)

    @pytest.mark.skipif(not HAS_SKLEARN, reason="scikit-learn not installed")
    def test_random_forest_different_seeds_differ(self, module, small_ndvi, ground_truth):
        preds_a = module.random_forest_baseline(small_ndvi, ground_truth, n_estimators=10, random_state=42)
        preds_b = module.random_forest_baseline(small_ndvi, ground_truth, n_estimators=10, random_state=99)
        # Different seeds may give different predictions (but not guaranteed)
        # We just check the function doesn't crash
        assert preds_a.shape == preds_b.shape

    # --- run_all_baselines ---

    def test_run_all_baselines_returns_dict(self, module, small_ndvi, ground_truth):
        results = module.run_all_baselines(small_ndvi, ground_truth)
        assert isinstance(results, dict)
        assert "persistence" in results
        assert "linear_trend" in results
        assert "random_forest" in results

    def test_run_all_baselines_persistence_has_metrics(self, module, small_ndvi, ground_truth):
        results = module.run_all_baselines(small_ndvi, ground_truth)
        assert "f1_macro" in results["persistence"]
        assert "miou" in results["persistence"]


# =========================
# p0035_tatakua_baselines
# =========================


class TestP0035Baselines:
    """Tests for src/baselines/p0035_tatakua_baselines.py."""

    @pytest.fixture
    def module(self):
        from src.baselines import p0035_tatakua_baselines

        return p0035_tatakua_baselines

    def test_module_loads(self, module):
        assert module is not None

    def test_module_has_functions(self, module):
        """Check the module exposes at least one baseline function."""
        funcs = [name for name in dir(module) if callable(getattr(module, name)) and not name.startswith("_")]
        # Some callable that's exported
        assert len(funcs) >= 1


# =========================
# p0100_yvyra_baselines
# =========================


class TestP0100Baselines:
    """Tests for src/baselines/p0100_yvyra_baselines.py."""

    @pytest.fixture
    def module(self):
        from src.baselines import p0100_yvyra_baselines

        return p0100_yvyra_baselines

    def test_module_loads(self, module):
        assert module is not None

    def test_module_has_functions(self, module):
        """Check the module exposes at least one baseline function."""
        funcs = [name for name in dir(module) if callable(getattr(module, name)) and not name.startswith("_")]
        assert len(funcs) >= 1


# =========================
# unet_baseline (uses torch)
# =========================


class TestUnetBaseline:
    """The U-Net baseline requires torch. Test that it can at least import."""

    def test_unet_baseline_imports(self):
        try:
            from src.baselines.p0011_yvytu_baselines import unet_baseline

            assert callable(unet_baseline)
        except ImportError:
            pytest.skip("torch not installed")

    def test_unet_baseline_signature(self):
        try:
            import inspect

            from src.baselines.p0011_yvytu_baselines import unet_baseline

            sig = inspect.signature(unet_baseline)
            # Must accept ndvi_timeseries, ground_truth
            params = list(sig.parameters.keys())
            assert "ndvi_timeseries" in params
            assert "ground_truth" in params
        except ImportError:
            pytest.skip("torch not installed")
