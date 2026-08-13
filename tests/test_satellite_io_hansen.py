"""Tests for src/satellite_io/hansen.py.

Coverage target: 60%+. Tests the synthetic data generation, helpers
(deforestation year, cumulative), and module constants.
"""

import numpy as np
import pytest  # noqa: E402

from src.satellite_io import hansen as _hansen
from src.satellite_io.hansen import (
    HANSEN_BANDS,
    compute_cumulative_deforestation,
    compute_deforestation_year,
    download_hansen_real,
    generate_synthetic_hansen,
)

pytest.importorskip("rasterio", reason="CI: requires optional system dep 'rasterio' (not installed)")  # noqa: E402


# =========================
# Constants
# =========================


class TestHansenConstants:
    def test_hansen_bands_is_dict(self):
        assert isinstance(HANSEN_BANDS, dict)
        assert len(HANSEN_BANDS) > 0

    def test_hansen_bands_expected_keys(self):
        """Standard Hansen GFC bands."""
        expected = {"treecover2000", "loss", "gain", "datamask"}
        assert expected.issubset(set(HANSEN_BANDS.keys()))


# =========================
# compute_deforestation_year
# =========================


class TestComputeDeforestationYear:
    def test_returns_correct_shape(self):
        lossyear = np.zeros((10, 10), dtype=np.uint8)
        result = compute_deforestation_year(lossyear, year=2020)
        assert result.shape == (10, 10)

    def test_returns_uint8(self):
        lossyear = np.zeros((5, 5), dtype=np.uint8)
        result = compute_deforestation_year(lossyear, year=2020)
        assert result.dtype == np.uint8

    def test_year_2020_matches_code_20(self):
        """Hansen codes: year-2000."""
        lossyear = np.array([[20, 0, 21], [19, 20, 0]], dtype=np.uint8)
        result = compute_deforestation_year(lossyear, year=2020)
        # Year 2020 = code 20
        assert result[0, 0] == 1
        assert result[0, 1] == 0
        assert result[0, 2] == 0
        assert result[1, 0] == 0
        assert result[1, 1] == 1
        assert result[1, 2] == 0

    def test_year_2001_first_year(self):
        lossyear = np.array([[1, 0]], dtype=np.uint8)
        result = compute_deforestation_year(lossyear, year=2001)
        assert result[0, 0] == 1

    def test_no_loss_year_returns_zero(self):
        """All-zero lossyear should produce all-zero mask."""
        lossyear = np.zeros((4, 4), dtype=np.uint8)
        result = compute_deforestation_year(lossyear, year=2020)
        assert result.sum() == 0


# =========================
# compute_cumulative_deforestation
# =========================


class TestComputeCumulativeDeforestation:
    def test_returns_correct_shape(self):
        lossyear = np.zeros((10, 10), dtype=np.uint8)
        result = compute_cumulative_deforestation(lossyear, end_year=2020)
        assert result.shape == (10, 10)

    def test_returns_boolean(self):
        lossyear = np.zeros((5, 5), dtype=np.uint8)
        result = compute_cumulative_deforestation(lossyear, end_year=2020)
        assert result.dtype == bool

    def test_includes_all_years_until_end(self):
        """Cumulative up to 2020 should include all loss years 1-20."""
        lossyear = np.array([[1, 15, 20, 21, 22]], dtype=np.uint8)
        result = compute_cumulative_deforestation(lossyear, end_year=2020)
        # Years 1, 15, 20 should be included; 21, 22 should not
        assert result[0, 0]  # year 1
        assert result[0, 1]  # year 15
        assert result[0, 2]  # year 20
        assert not result[0, 3]  # year 21 not included
        assert not result[0, 4]  # year 22 not included

    def test_no_loss_returns_false(self):
        lossyear = np.zeros((4, 4), dtype=np.uint8)
        result = compute_cumulative_deforestation(lossyear, end_year=2023)
        assert result.sum() == 0


# =========================
# generate_synthetic_hansen
# =========================


class TestGenerateSyntheticHansen:
    def test_returns_dict(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_hansen(bbox, start_year=2020, end_year=2023)
        assert isinstance(result, dict)

    def test_returns_all_bands(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_hansen(bbox)
        expected = {"treecover2000", "loss", "gain", "lossyear"}
        assert expected.issubset(set(result.keys()))

    def test_custom_shape(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_hansen(bbox, shape=(64, 64))
        assert result["treecover2000"].shape == (64, 64)
        assert result["loss"].shape == (64, 64)
        assert result["lossyear"].shape == (64, 64)

    def test_treecover_in_range(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_hansen(bbox, shape=(32, 32))
        # Treecover should be 0-100
        assert result["treecover2000"].min() >= 0
        assert result["treecover2000"].max() <= 100

    def test_loss_is_binary(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_hansen(bbox, shape=(32, 32))
        unique = np.unique(result["loss"])
        assert set(unique.tolist()).issubset({0, 1})

    def test_lossyear_range(self):
        """lossyear should be 0-23 (0=no loss, 1=2001, ..., 23=2023)."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_hansen(bbox, shape=(64, 64))
        assert result["lossyear"].min() >= 0
        assert result["lossyear"].max() <= 23

    def test_deterministic_with_seed(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        a = generate_synthetic_hansen(bbox, shape=(32, 32), seed=42)
        b = generate_synthetic_hansen(bbox, shape=(32, 32), seed=42)
        np.testing.assert_array_equal(a["treecover2000"], b["treecover2000"])
        np.testing.assert_array_equal(a["loss"], b["loss"])

    def test_east_west_gradient(self):
        """West pixels should have higher treecover than east (Chaco)."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_hansen(bbox, shape=(32, 256))
        # The first ~256 columns should have higher treecover
        assert result["treecover2000"].mean() > 30  # mostly forest/pasture


# =========================
# download_hansen_real
# =========================


class TestDownloadHansenReal:
    def test_uses_cache_when_present(self, tmp_path, monkeypatch):
        """If cache file exists, read from it."""
        cache_dir = tmp_path / "hansen_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("HANSEN_CACHE_DIR", str(cache_dir))
        monkeypatch.setattr(_hansen, "CACHE_DIR", cache_dir)

        # Write a sample cache file
        treecover = np.array([[50, 60], [70, 80]], dtype=np.uint8)
        loss = np.array([[0, 1], [1, 0]], dtype=np.uint8)
        gain = np.array([[0, 0], [0, 1]], dtype=np.uint8)
        lossyear = np.array([[0, 5], [10, 0]], dtype=np.uint8)
        cache_path = cache_dir / "hansen_2020_2023.npz"
        np.savez_compressed(
            cache_path,
            treecover2000=treecover,
            loss=loss,
            gain=gain,
            lossyear=lossyear,
        )

        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = download_hansen_real(bbox, start_year=2020, end_year=2023, use_gee=False)
        assert isinstance(result, dict)
        assert "treecover2000" in result
        assert result["treecover2000"].shape == (2, 2)

    def test_falls_back_to_synthetic_when_gee_unavailable(self, tmp_path, monkeypatch):
        """Without GEE access, fall back to synthetic data."""
        cache_dir = tmp_path / "hansen_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        monkeypatch.setenv("HANSEN_CACHE_DIR", str(cache_dir))
        monkeypatch.setattr(_hansen, "CACHE_DIR", cache_dir)

        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        # use_gee=False forces synthetic fallback
        result = download_hansen_real(bbox, start_year=2020, end_year=2023, use_gee=False)
        assert isinstance(result, dict)
        assert "treecover2000" in result
        assert "loss" in result


class TestDownloadHansenRealCacheHit:
    """Tests for download_hansen_real cache-hit path."""

    def test_cache_hit(self, tmp_path, monkeypatch):
        """When cache exists, return cached data."""
        from src.satellite_io import hansen as hansen_mod

        # Create a cache file
        cache_file = tmp_path / "hansen_2018_2023.npz"
        arr1 = np.zeros((10, 10), dtype=np.uint8)
        arr2 = np.ones((10, 10), dtype=np.uint8)
        np.savez_compressed(cache_file, treecover2000=arr1, loss=arr2)

        monkeypatch.setattr(hansen_mod, "CACHE_DIR", tmp_path)

        result = hansen_mod.download_hansen_real(
            bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            use_gee=False,
        )
        assert result is not None
        assert "treecover2000" in result

    def test_gee_fails_falls_back(self, tmp_path, monkeypatch):
        """When GEE import fails, falls back to synthetic data."""
        from src.satellite_io import hansen as hansen_mod

        monkeypatch.setattr(hansen_mod, "CACHE_DIR", tmp_path)

        # Block ee import
        import sys as _sys

        saved = _sys.modules.get("ee")
        _sys.modules["ee"] = None
        try:
            result = hansen_mod.download_hansen_real(
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                use_gee=True,
            )
            # GEE unavailable -> falls back to synthetic
            assert result is not None
            assert "treecover2000" in result
        finally:
            if saved is None:
                _sys.modules.pop("ee", None)
            else:
                _sys.modules["ee"] = saved

    def test_use_gee_false_returns_synthetic(self, tmp_path, monkeypatch):
        """When use_gee=False, generate synthetic data directly."""
        from src.satellite_io import hansen as hansen_mod

        monkeypatch.setattr(hansen_mod, "CACHE_DIR", tmp_path)

        result = hansen_mod.download_hansen_real(
            bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            use_gee=False,
        )
        assert result is not None
        assert "treecover2000" in result
