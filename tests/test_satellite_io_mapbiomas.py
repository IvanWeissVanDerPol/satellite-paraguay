"""Tests for src/satellite_io/mapbiomas.py.

Coverage target: 70%+. Tests the synthetic data generation,
parcel statistics, and module constants.
"""
import pytest
from unittest.mock import MagicMock

import numpy as np

from src.satellite_io import mapbiomas as _mb
from src.satellite_io.mapbiomas import (
    MAPBIOMAS_CLASSES,
    generate_synthetic_mapbiomas,
    compute_parcel_statistics_real,
)


# =========================
# Constants
# =========================


class TestMapBiomasConstants:
    def test_classes_is_dict(self):
        assert isinstance(MAPBIOMAS_CLASSES, dict)
        assert len(MAPBIOMAS_CLASSES) > 0

    def test_known_classes_present(self):
        """Common MapBiomas class codes."""
        assert 1 in MAPBIOMAS_CLASSES  # Forest
        assert 4 in MAPBIOMAS_CLASSES  # Pasture
        assert 14 in MAPBIOMAS_CLASSES  # Water
        assert 21 in MAPBIOMAS_CLASSES  # Urban
        assert 39 in MAPBIOMAS_CLASSES  # Soybean

    def test_class_names_are_strings(self):
        for k, v in MAPBIOMAS_CLASSES.items():
            assert isinstance(v, str)


# =========================
# generate_synthetic_mapbiomas
# =========================


class TestGenerateSyntheticMapBiomas:
    def test_returns_ndarray(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_mapbiomas(bbox, year=2022)
        assert isinstance(result, np.ndarray)

    def test_custom_shape(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_mapbiomas(bbox, year=2022, shape=(64, 64))
        assert result.shape == (64, 64)

    def test_default_shape(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_mapbiomas(bbox, year=2022)
        assert result.shape == (256, 256)

    def test_classes_in_valid_range(self):
        """MapBiomas Paraguay codes are 0-70."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_mapbiomas(bbox, year=2022, shape=(64, 64))
        assert result.min() >= 0
        assert result.max() <= 70

    def test_contains_forest_class(self):
        """West region should have forest (class 1)."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_mapbiomas(bbox, year=2022, shape=(128, 128))
        # Should have at least some forest pixels
        assert (result == 1).sum() > 0

    def test_contains_agriculture_class(self):
        """East region should have soybean (class 39)."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = generate_synthetic_mapbiomas(bbox, year=2022, shape=(128, 128))
        assert (result == 39).sum() > 0

    def test_recent_year_has_less_forest(self):
        """Year 2020+ should lose forest to agriculture per the simulation."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        # Use a shape with forest coverage
        old = generate_synthetic_mapbiomas(bbox, year=2010, shape=(128, 128))
        new = generate_synthetic_mapbiomas(bbox, year=2023, shape=(128, 128))
        # Forest count should be lower in newer year (some convert to ag)
        old_forest = (old == 1).sum()
        new_forest = (new == 1).sum()
        assert new_forest <= old_forest

    def test_deterministic_with_seed(self):
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        a = generate_synthetic_mapbiomas(bbox, year=2022, shape=(32, 32), seed=42)
        b = generate_synthetic_mapbiomas(bbox, year=2022, shape=(32, 32), seed=42)
        np.testing.assert_array_equal(a, b)


# =========================
# compute_parcel_statistics_real
# =========================


class TestComputeParcelStatistics:
    def test_returns_dict(self):
        """Test with a simple geometry that has bounds."""
        mapbiomas = np.full((100, 100), 1, dtype=np.uint8)  # all forest
        # Mock geometry with bounds
        geom = MagicMock()
        geom.bounds = (100, 100, 200, 200)
        result = compute_parcel_statistics_real(mapbiomas, geom)
        assert isinstance(result, dict)

    def test_dominant_class(self):
        """All-forest parcel should return forest as dominant."""
        mapbiomas = np.full((100, 100), 1, dtype=np.uint8)
        geom = MagicMock()
        geom.bounds = (100, 100, 200, 200)
        result = compute_parcel_statistics_real(mapbiomas, geom)
        assert result["dominant_class"] == 1
        assert result["dominant_fraction"] == 1.0

    def test_dominant_class_name(self):
        """The class name should be looked up from MAPBIOMAS_CLASSES."""
        mapbiomas = np.full((100, 100), 39, dtype=np.uint8)  # Soybean
        geom = MagicMock()
        geom.bounds = (100, 100, 200, 200)
        result = compute_parcel_statistics_real(mapbiomas, geom)
        assert "Soybean" in result["dominant_class_name"]

    def test_class_fractions_sum_to_one(self):
        """Class fractions should sum to approximately 1.0."""
        rng = np.random.default_rng(42)
        mapbiomas = rng.integers(0, 10, (100, 100), dtype=np.uint8)
        geom = MagicMock()
        geom.bounds = (100, 100, 8000, 8000)
        result = compute_parcel_statistics_real(mapbiomas, geom)
        fractions = result["parcel_class_fractions"]
        assert abs(sum(fractions.values()) - 1.0) < 1e-6

    def test_total_pixels_positive(self):
        mapbiomas = np.full((100, 100), 1, dtype=np.uint8)
        geom = MagicMock()
        geom.bounds = (100, 100, 200, 200)
        result = compute_parcel_statistics_real(mapbiomas, geom)
        assert result["total_pixels"] > 0

    def test_mixed_dominant(self):
        """Parcel with mixed cover should pick the most common."""
        mapbiomas = np.zeros((100, 100), dtype=np.uint8)
        mapbiomas[:, :] = 1  # start with all forest
        mapbiomas[10:80, 10:80] = 39  # bigger soybean region (dominant)
        mapbiomas[0:5, :] = 4  # small pasture strip
        geom = MagicMock()
        geom.bounds = (0, 0, 10000, 10000)
        result = compute_parcel_statistics_real(mapbiomas, geom)
        assert result["dominant_class"] == 39



class TestDownloadMapbiomasReal:
    """Tests for download_mapbiomas_paraguay_real function."""

    def test_cache_hit(self, tmp_path, monkeypatch):
        """When cache exists, return cached array."""
        from src.satellite_io import mapbiomas as mb_mod
        cache_file = tmp_path / "mapbiomas_py_2022.npy"
        cached = np.zeros((10, 10), dtype=np.uint8)
        np.save(cache_file, cached)

        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)

        result = mb_mod.download_mapbiomas_paraguay_real(
            bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            use_gee=False,
        )
        assert result is not None
        assert result.shape == (10, 10)

    def test_use_gee_false_returns_synthetic(self, tmp_path, monkeypatch):
        """When use_gee=False, generate synthetic MapBiomas data."""
        from src.satellite_io import mapbiomas as mb_mod
        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)

        result = mb_mod.download_mapbiomas_paraguay_real(
            bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            year=2022,
            use_gee=False,
        )
        assert result is not None
        assert result.ndim == 2

    def test_gee_fails_falls_back_to_synthetic(self, tmp_path, monkeypatch):
        """When GEE fails, falls back to synthetic data."""
        from src.satellite_io import mapbiomas as mb_mod
        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)

        # Block ee import
        import sys as _sys
        saved = _sys.modules.get("ee")
        _sys.modules["ee"] = None
        try:
            result = mb_mod.download_mapbiomas_paraguay_real(
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                year=2023,
                use_gee=True,
            )
            assert result is not None
        finally:
            if saved is None:
                _sys.modules.pop("ee", None)
            else:
                _sys.modules["ee"] = saved
