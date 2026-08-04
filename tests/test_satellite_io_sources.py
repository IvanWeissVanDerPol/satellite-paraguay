"""Tests for src/satellite_io/sources.py — multi-source satellite data API."""
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.satellite_io import sources as _sources
from src.satellite_io.sources import (
    download_sentinel2_tile,
    download_via_gee,
    compute_ndvi,
    cloud_mask_s2,
    download_mapbiomas_paraguay,
    download_hansen_gfc,
    DEFAULT_OUTPUT_DIR,
    SENTINEL_OUTPUT,
    LANDSAT_OUTPUT,
)


# =========================
# Constants
# =========================


class TestSourcesConstants:
    def test_default_output_dir_is_path(self):
        assert isinstance(DEFAULT_OUTPUT_DIR, Path)

    def test_sentinel_output_under_default(self):
        assert SENTINEL_OUTPUT.parent == DEFAULT_OUTPUT_DIR

    def test_landsat_output_under_default(self):
        assert LANDSAT_OUTPUT.parent == DEFAULT_OUTPUT_DIR


# =========================
# download_sentinel2_tile
# =========================


class TestDownloadSentinel2Tile:
    def test_returns_list(self):
        """Function returns a list (possibly empty)."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        result = download_sentinel2_tile(
            tile_id="test_tile",
            bbox=bbox,
            output_dir=Path("/tmp/test_sentinel"),
        )
        assert isinstance(result, list)

    def test_creates_output_dir(self, tmp_path):
        """Function should create the output directory."""
        bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
        output = tmp_path / "s2_test"
        download_sentinel2_tile(
            tile_id="test_tile",
            bbox=bbox,
            output_dir=output,
        )
        assert output.exists()


# =========================
# download_via_gee
# =========================


class TestDownloadViaGee:
    def test_raises_without_ee(self):
        """Without earthengine-api, should raise ImportError."""
        import sys as _sys
        saved = _sys.modules.get("ee")
        _sys.modules["ee"] = None  # type: ignore
        try:
            bbox = {"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20}
            with pytest.raises((ImportError, Exception)):
                download_via_gee(
                    tile_id="test",
                    bbox=bbox,
                    output_dir=Path("/tmp/test_gee"),
                )
        finally:
            if saved is None:
                _sys.modules.pop("ee", None)
            else:
                _sys.modules["ee"] = saved


# =========================
# compute_ndvi
# =========================


class TestComputeNDVI:
    def test_compute_ndvi_basic(self, tmp_path):
        """Test NDVI computation with a small realistic raster."""
        import rasterio
        from rasterio.transform import from_bounds

        # Create a red band raster (3x3, all vegetation ~0.2 reflectance)
        red_path = tmp_path / "red.tif"
        nir_path = tmp_path / "nir.tif"
        out_path = tmp_path / "ndvi.tif"

        profile = {
            "driver": "GTiff",
            "height": 3,
            "width": 3,
            "count": 1,
            "dtype": "float32",
            "transform": from_bounds(0, 0, 3, 3, 3, 3),
        }
        # Red = 0.2 everywhere, NIR = 0.6 everywhere
        # NDVI = (0.6 - 0.2) / (0.6 + 0.2) = 0.5
        with rasterio.open(red_path, "w", **profile) as dst:
            dst.write(np.full((3, 3), 0.2, dtype=np.float32), 1)
        with rasterio.open(nir_path, "w", **profile) as dst:
            dst.write(np.full((3, 3), 0.6, dtype=np.float32), 1)

        ndvi = compute_ndvi(red_path, nir_path, out_path)
        assert ndvi.shape == (3, 3)
        np.testing.assert_allclose(ndvi, 0.5, atol=1e-5)
        assert out_path.exists()

    def test_compute_ndvi_water(self, tmp_path):
        """Water pixels (NIR < RED) should have negative NDVI."""
        import rasterio
        from rasterio.transform import from_bounds

        red_path = tmp_path / "red.tif"
        nir_path = tmp_path / "nir.tif"
        out_path = tmp_path / "ndvi.tif"

        profile = {
            "driver": "GTiff",
            "height": 3,
            "width": 3,
            "count": 1,
            "dtype": "float32",
            "transform": from_bounds(0, 0, 3, 3, 3, 3),
        }
        # Red = 0.05, NIR = 0.02 (water)
        # NDVI = (0.02 - 0.05) / (0.02 + 0.05) = -0.428...
        with rasterio.open(red_path, "w", **profile) as dst:
            dst.write(np.full((3, 3), 0.05, dtype=np.float32), 1)
        with rasterio.open(nir_path, "w", **profile) as dst:
            dst.write(np.full((3, 3), 0.02, dtype=np.float32), 1)

        ndvi = compute_ndvi(red_path, nir_path, out_path)
        assert ndvi.mean() < 0  # water has negative NDVI


# =========================
# cloud_mask_s2
# =========================


class TestCloudMaskS2:
    def test_returns_numpy_array(self, tmp_path):
        """Test that cloud_mask_s2 returns a boolean mask."""
        import rasterio
        from rasterio.transform import from_bounds

        scl_path = tmp_path / "scl.tif"
        profile = {
            "driver": "GTiff",
            "height": 5,
            "width": 5,
            "count": 1,
            "dtype": "uint8",
            "transform": from_bounds(0, 0, 5, 5, 5, 5),
        }
        # Mix of SCL values: 4 (vegetation), 9 (cloud high), 6 (water)
        scl_data = np.array([
            [4, 4, 4, 4, 4],
            [4, 9, 9, 9, 4],
            [4, 9, 6, 9, 4],
            [4, 9, 9, 9, 4],
            [4, 4, 4, 4, 4],
        ], dtype=np.uint8)
        with rasterio.open(scl_path, "w", **profile) as dst:
            dst.write(scl_data, 1)

        mask = cloud_mask_s2(scl_path)
        assert isinstance(mask, np.ndarray)
        assert mask.shape == (5, 5)
        assert mask.dtype == bool
        # Vegetation (4) and water (6) should NOT be masked
        assert mask[0, 0] == False  # vegetation
        assert mask[2, 2] == False  # water
        # Cloud (9) should be masked
        assert mask[1, 1] == True
        assert mask[1, 2] == True

    def test_all_clean_returns_no_mask(self, tmp_path):
        """All-vegetation pixels should not be masked."""
        import rasterio
        from rasterio.transform import from_bounds

        scl_path = tmp_path / "scl.tif"
        profile = {
            "driver": "GTiff",
            "height": 3,
            "width": 3,
            "count": 1,
            "dtype": "uint8",
            "transform": from_bounds(0, 0, 3, 3, 3, 3),
        }
        with rasterio.open(scl_path, "w", **profile) as dst:
            dst.write(np.full((3, 3), 4, dtype=np.uint8), 1)  # all vegetation

        mask = cloud_mask_s2(scl_path)
        assert not mask.any()  # nothing masked
