"""Tests for src/timeseries/analysis.py.

Coverage target: 90%+. Tests stack_timeseries, compute_ndvi_timeseries,
detect_changes_bfast, compute_trend, compute_anomaly,
aggregate_by_department.
"""

import pytest  # noqa: E402
pytest.importorskip("rasterio", reason="CI: requires optional system dep 'rasterio' (not installed)")  # noqa: E402

from unittest.mock import MagicMock, patch

import numpy as np


class TestStackTimeseries:
    """Tests for stack_timeseries function."""

    def test_stack_with_bands(self, tmp_path):
        """Stack rasters with specific bands."""
        from src.timeseries.analysis import stack_timeseries

        # Create mock rasters
        paths = []
        for i in range(3):
            p = tmp_path / f"test_{i}.tif"
            p.write_text("dummy")
            paths.append(p)

        # Mock rasterio
        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        # Each raster has 3 bands
        mock_src.read.return_value = np.zeros((3, 10, 10), dtype=np.uint8)
        mock_src.transform = "transform"
        mock_src.crs = "EPSG:4326"
        mock_src.shape = (10, 10)

        with patch("src.timeseries.analysis.rasterio.open", return_value=mock_src):
            stacked, meta = stack_timeseries(paths, bands=[1, 2, 3])
        assert stacked.shape[0] == 3  # 3 timesteps
        assert meta is not None

    def test_stack_without_bands(self, tmp_path):
        """Stack rasters without band selection."""
        from src.timeseries.analysis import stack_timeseries

        paths = [tmp_path / "a.tif", tmp_path / "b.tif"]
        for p in paths:
            p.write_text("dummy")

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        mock_src.read.return_value = np.zeros((2, 5, 5), dtype=np.uint8)
        mock_src.transform = "t"
        mock_src.crs = "c"
        mock_src.shape = (5, 5)

        with patch("src.timeseries.analysis.rasterio.open", return_value=mock_src):
            stacked, meta = stack_timeseries(paths)
        assert stacked.shape[0] == 2


class TestComputeNDVITimeseries:
    """Tests for compute_ndvi_timeseries function."""

    def test_ndvi_with_dummy_data(self, tmp_path):
        from src.timeseries.analysis import compute_ndvi_timeseries

        # Create dummy red and nir rasters
        red_paths = []
        nir_paths = []
        for i in range(2):
            r = tmp_path / f"red_{i}.tif"
            n = tmp_path / f"nir_{i}.tif"
            r.write_text("dummy")
            n.write_text("dummy")
            red_paths.append(r)
            nir_paths.append(n)

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)

        # NIR > RED so NDVI positive
        def side_effect(*args, **kwargs):
            # First call is red, second is nir (per iter)
            # alternate between red and nir
            return np.array([[0.2, 0.3], [0.4, 0.5]])

        # Alternate values via side_effect with iterator
        vals = iter(
            [
                np.array([[0.2, 0.3], [0.4, 0.5]]),  # red
                np.array([[0.5, 0.6], [0.7, 0.8]]),  # nir
                np.array([[0.2, 0.3], [0.4, 0.5]]),  # red
                np.array([[0.5, 0.6], [0.7, 0.8]]),  # nir
            ]
        )
        mock_src.read.side_effect = lambda *args, **kwargs: next(vals)

        with patch("src.timeseries.analysis.rasterio.open", return_value=mock_src):
            ndvi = compute_ndvi_timeseries(red_paths, nir_paths)
        assert ndvi.shape == (2, 2, 2)


class TestDetectChangesBfast:
    """Tests for detect_changes_bfast function."""

    def test_detect_with_insufficient_data(self):
        """When T < 4, return zeros."""
        from src.timeseries.analysis import detect_changes_bfast

        ts = np.random.rand(3, 5, 5)
        dates = ["2024-01-01", "2024-02-01", "2024-03-01"]
        result = detect_changes_bfast(ts, dates)
        assert result["breakpoints"].shape == (5, 5)
        assert result["magnitudes"].shape == (5, 5)
        # All breakpoints should be -1 (no detection)
        assert (result["breakpoints"] == -1).all()

    def test_detect_with_sufficient_data(self):
        """When T >= 4, compute changes."""
        from src.timeseries.analysis import detect_changes_bfast

        ts = np.random.rand(10, 5, 5)
        dates = [f"2024-{m:02d}-01" for m in range(1, 11)]
        result = detect_changes_bfast(ts, dates)
        assert "breakpoints" in result
        assert "magnitudes" in result
        assert "before_mean" in result
        assert "after_mean" in result

    def test_detect_with_drop(self):
        """NDVI drops should be detected."""
        from src.timeseries.analysis import detect_changes_bfast

        # Stable NDVI
        ts = np.full((10, 5, 5), 0.8, dtype=np.float32)
        ts[5:, :, :] = 0.3  # Drop in second half
        dates = [f"2024-{m:02d}-01" for m in range(1, 11)]
        result = detect_changes_bfast(ts, dates)
        # Magnitudes should be positive
        assert result["magnitudes"].sum() > 0

    def test_detect_with_threshold(self):
        """Different h thresholds work."""
        from src.timeseries.analysis import detect_changes_bfast

        ts = np.random.rand(8, 5, 5)
        dates = [f"2024-{m:02d}-01" for m in range(1, 9)]
        for h_val in [0.1, 0.5, 1.0]:
            result = detect_changes_bfast(ts, dates, h=h_val)
            assert "breakpoints" in result


class TestComputeTrend:
    """Tests for compute_trend function."""

    def test_trend_perfectly_linear(self):
        """Perfectly linear data should have a non-zero trend."""
        from src.timeseries.analysis import compute_trend

        # Increasing linearly
        ts = np.zeros((10, 5, 5), dtype=np.float32)
        for t in range(10):
            ts[t] = 0.1 * t
        dates = [f"2024-{m:02d}-01" for m in range(1, 11)]
        trend = compute_trend(ts, dates)
        assert trend.shape == (5, 5)
        # Should be positive
        assert (trend > 0).all()

    def test_trend_constant_data(self):
        """Constant data should have ~zero trend."""
        from src.timeseries.analysis import compute_trend

        ts = np.full((10, 5, 5), 0.5, dtype=np.float32)
        dates = [f"2024-{m:02d}-01" for m in range(1, 11)]
        trend = compute_trend(ts, dates)
        # Should be near zero
        assert np.abs(trend).max() < 0.01

    def test_trend_decreasing(self):
        """Decreasing data should have negative trend."""
        from src.timeseries.analysis import compute_trend

        ts = np.zeros((10, 5, 5), dtype=np.float32)
        for t in range(10):
            ts[t] = 1.0 - 0.1 * t
        dates = [f"2024-{m:02d}-01" for m in range(1, 11)]
        trend = compute_trend(ts, dates)
        # Should be negative
        assert (trend < 0).all()


class TestComputeAnomaly:
    """Tests for compute_anomaly function."""

    def test_anomaly_with_default_baseline(self):
        from src.timeseries.analysis import compute_anomaly

        ts = np.random.rand(20, 5, 5).astype(np.float32)
        anomaly = compute_anomaly(ts)
        assert anomaly.shape == (20, 5, 5)

    def test_anomaly_with_custom_baseline(self):
        from src.timeseries.analysis import compute_anomaly

        ts = np.random.rand(15, 5, 5).astype(np.float32)
        anomaly = compute_anomaly(ts, baseline_period=(0, 5))
        assert anomaly.shape == (15, 5, 5)

    def test_anomaly_constant_baseline(self):
        """If data is constant, anomaly should be zero."""
        from src.timeseries.analysis import compute_anomaly

        ts = np.full((10, 5, 5), 0.5, dtype=np.float32)
        anomaly = compute_anomaly(ts)
        assert np.abs(anomaly).max() < 1e-5


class TestAggregateByDepartment:
    """Tests for aggregate_by_department function."""

    def test_aggregate_with_departments(self):
        from src.timeseries.analysis import aggregate_by_department

        ts = np.random.rand(10, 20, 20).astype(np.float32)
        depts = {
            "Asunción": "geom1",
            "Central": "geom2",
            "Alto Paraná": "geom3",
        }
        result = aggregate_by_department(ts, depts)
        assert len(result) == 3
        assert "Asunción" in result
        # Each result is a time series (T,) shape
        assert result["Asunción"].shape == (10,)

    def test_aggregate_empty_departments(self):
        from src.timeseries.analysis import aggregate_by_department

        ts = np.random.rand(5, 10, 10).astype(np.float32)
        result = aggregate_by_department(ts, {})
        assert len(result) == 0


class TestModuleImports:
    def test_module_imports(self):
        from src.timeseries import analysis

        assert analysis is not None
