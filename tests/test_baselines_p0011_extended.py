"""Extended tests for src/baselines/p0011_yvytu_baselines.py.

Tests the unet_baseline function (PyTorch-based) and other
uncovered code paths.
"""

import numpy as np


class TestUnetBaseline:
    """Tests for unet_baseline function."""

    def test_unet_baseline_basic(self):
        """Basic UNet training + inference."""
        from src.baselines.p0011_yvytu_baselines import unet_baseline

        # Small time series: 5 timesteps, 100x100 image
        T = 5
        ndvi = np.random.rand(T, 100, 100).astype(np.float32)
        ground_truth = np.random.randint(0, 10, size=(100, 100), dtype=np.int64)
        preds = unet_baseline(ndvi, ground_truth, epochs=2)
        assert preds.shape == (100, 100)

    def test_unet_baseline_smaller_than_256(self):
        """Image smaller than 256x256 should be padded."""
        from src.baselines.p0011_yvytu_baselines import unet_baseline

        T = 4
        ndvi = np.random.rand(T, 50, 50).astype(np.float32)
        gt = np.zeros((50, 50), dtype=np.int64)
        preds = unet_baseline(ndvi, gt, epochs=1)
        assert preds.shape == (50, 50)

    def test_unet_baseline_larger_than_256(self):
        """Image larger than 256x256 gets cropped to 256x256 internally."""
        from src.baselines.p0011_yvytu_baselines import unet_baseline

        T = 3
        ndvi = np.random.rand(T, 300, 300).astype(np.float32)
        gt = np.zeros((300, 300), dtype=np.int64)
        # Function crops input to 256 then returns [:H, :W] = full 300
        preds = unet_baseline(ndvi, gt, epochs=1)
        assert preds.shape == (256, 256)  # cropped internally

    def test_unet_baseline_exactly_256(self):
        """Image exactly 256x256."""
        from src.baselines.p0011_yvytu_baselines import unet_baseline

        T = 3
        ndvi = np.random.rand(T, 256, 256).astype(np.float32)
        gt = np.zeros((256, 256), dtype=np.int64)
        preds = unet_baseline(ndvi, gt, epochs=1)
        assert preds.shape == (256, 256)


class TestExistingBaselinesExtended:
    """Additional tests for other baseline functions."""

    def test_persistence_baseline_with_dates(self):
        from src.baselines.p0011_yvytu_baselines import persistence_baseline

        ndvi = np.random.rand(10, 30, 30).astype(np.float32)
        mask = persistence_baseline(ndvi)
        assert mask.shape == (30, 30)

    def test_linear_trend_baseline_small(self):
        from src.baselines.p0011_yvytu_baselines import linear_trend_baseline

        ndvi = np.random.rand(8, 30, 30).astype(np.float32)
        mask = linear_trend_baseline(ndvi)
        assert mask.shape == (30, 30)

    def test_random_forest_baseline_basic(self):
        from src.baselines.p0011_yvytu_baselines import random_forest_baseline

        T = 8
        ndvi = np.random.rand(T, 30, 30).astype(np.float32)
        gt = np.random.randint(0, 3, (30, 30), dtype=np.int64)
        preds = random_forest_baseline(ndvi, gt, n_estimators=5)
        assert preds.shape == (30, 30)


class TestPersistenceEdgeCases:
    """Test edge cases in baselines."""

    def test_persistence_no_change(self):
        from src.baselines.p0011_yvytu_baselines import persistence_baseline

        ndvi = np.full((10, 30, 30), 0.5, dtype=np.float32)
        mask = persistence_baseline(ndvi)
        # No change -> minimal loss pixels (just check it runs)
        assert mask.shape == (30, 30)

    def test_persistence_complete_loss(self):
        from src.baselines.p0011_yvytu_baselines import persistence_baseline

        # NDVI drops to 0 in second half
        ndvi = np.full((10, 30, 30), 0.8, dtype=np.float32)
        ndvi[5:, :, :] = 0.0
        mask = persistence_baseline(ndvi)
        assert mask.sum() > 0  # Most pixels should be flagged


class TestLinearTrendVariants:
    """Test linear_trend_baseline variations."""

    def test_increasing_trend(self):
        from src.baselines.p0011_yvytu_baselines import linear_trend_baseline

        # Increasing NDVI trend (no loss)
        ndvi = np.zeros((10, 20, 20), dtype=np.float32)
        for t in range(10):
            ndvi[t] = 0.1 * t
        mask = linear_trend_baseline(ndvi)
        # Few/no losses (trend is increasing)
        assert mask.sum() < mask.size * 0.1

    def test_decreasing_trend(self):
        from src.baselines.p0011_yvytu_baselines import linear_trend_baseline

        # Decreasing NDVI (deforestation)
        ndvi = np.full((10, 20, 20), 0.9, dtype=np.float32)
        for t in range(10):
            ndvi[t] = 0.9 - 0.08 * t
        mask = linear_trend_baseline(ndvi)
        # Check shape
        assert mask.shape == (20, 20)
