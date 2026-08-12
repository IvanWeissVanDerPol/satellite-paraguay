"""Tests for src/satellite_io/sources.py — multi-source satellite data API."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from src.satellite_io.sources import (
    DEFAULT_OUTPUT_DIR,
    LANDSAT_OUTPUT,
    SENTINEL_OUTPUT,
    cloud_mask_s2,
    compute_ndvi,
    download_sentinel2_tile,
    download_via_gee,
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
        scl_data = np.array(
            [
                [4, 4, 4, 4, 4],
                [4, 9, 9, 9, 4],
                [4, 9, 6, 9, 4],
                [4, 9, 9, 9, 4],
                [4, 4, 4, 4, 4],
            ],
            dtype=np.uint8,
        )
        with rasterio.open(scl_path, "w", **profile) as dst:
            dst.write(scl_data, 1)

        mask = cloud_mask_s2(scl_path)
        assert isinstance(mask, np.ndarray)
        assert mask.shape == (5, 5)
        assert mask.dtype == bool
        # Vegetation (4) and water (6) should NOT be masked
        assert not mask[0, 0]  # vegetation
        assert not mask[2, 2]  # water
        # Cloud (9) should be masked
        assert mask[1, 1]
        assert mask[1, 2]

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


class TestComputeNDVISynthetic:
    """Tests for compute_ndvi synthetic-data path."""

    def test_compute_ndvi(self, tmp_path):
        from src.satellite_io.sources import compute_ndvi

        red_path = tmp_path / "red.tif"
        nir_path = tmp_path / "nir.tif"
        out_path = tmp_path / "ndvi.tif"
        red_path.write_text("dummy")
        nir_path.write_text("dummy")

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        mock_src.read.return_value = np.array([[0.2, 0.3], [0.4, 0.5]])
        mock_src.profile = {"driver": "GTiff", "dtype": "uint8"}

        with patch("src.satellite_io.sources.rasterio.open", return_value=mock_src):
            ndvi = compute_ndvi(red_path, nir_path, out_path)
        assert ndvi.shape == (2, 2)


class TestCloudMaskS2Synthetic:
    """Tests for cloud_mask_s2 synthetic-data path."""

    def test_cloud_mask(self, tmp_path):
        from src.satellite_io.sources import cloud_mask_s2

        scl_path = tmp_path / "scl.tif"
        scl_path.write_text("dummy")

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        # SCL: vegetation (4), bare soil (5), water (6), cloud (8)
        mock_src.read.return_value = np.array([[4, 5, 6, 8, 9]], dtype=np.uint8)

        with patch("src.satellite_io.sources.rasterio.open", return_value=mock_src):
            mask = cloud_mask_s2(scl_path)
        # mask True for clouds/shadows/no-data
        assert mask.shape == (1, 5)


class TestDownloadMapbiomas:
    """Tests for download_mapbiomas_paraguay function."""

    def test_returns_path(self, tmp_path):
        from src.satellite_io.sources import download_mapbiomas_paraguay

        result = download_mapbiomas_paraguay(output_dir=tmp_path)
        assert isinstance(result, Path)


class TestDownloadHansenGfc:
    """Tests for download_hansen_gfc function."""

    def test_returns_path(self, tmp_path):
        from src.satellite_io.sources import download_hansen_gfc

        result = download_hansen_gfc(output_dir=tmp_path)
        assert isinstance(result, Path)


class TestModuleConstants:
    def test_default_output_dir(self):
        from src.satellite_io import sources

        assert sources.DEFAULT_OUTPUT_DIR is not None


class TestDownloadViaGeeSynthetic:
    """Tests for download_via_gee synthetic-data path."""

    def test_sentinel2_path(self, tmp_path, monkeypatch):
        from src.satellite_io.sources import download_via_gee

        # Mock ee module
        mock_ee = MagicMock()
        mock_ee.Geometry.Rectangle.return_value = "mock_region"
        mock_ee.ImageCollection.return_value = mock_ee
        mock_ee.filterBounds.return_value = mock_ee
        mock_ee.filterDate.return_value = mock_ee
        mock_ee.filter.return_value = mock_ee
        mock_ee.median.return_value = mock_ee
        mock_ee.clip.return_value = mock_ee
        mock_ee.Initialize.return_value = None
        mock_ee.Filter.lt.return_value = "mock_filter"
        mock_image = MagicMock()
        mock_image.getDownloadURL.return_value = "http://example.com/test.tif"
        # When .median().clip() is called, return mock_image
        mock_ee.median.return_value.clip.return_value = mock_image

        with patch.dict("sys.modules", {"ee": mock_ee}):
            result = download_via_gee(
                tile_id="T_001",
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                satellite="sentinel2",
                start_date="2024-01-01",
                end_date="2024-06-01",
                output_dir=tmp_path,
            )
        assert result is not None

    def test_landsat9_path(self, tmp_path):
        from src.satellite_io.sources import download_via_gee

        mock_ee = MagicMock()
        mock_ee.Geometry.Rectangle.return_value = "mock_region"
        mock_ee.ImageCollection.return_value = mock_ee
        mock_ee.filterBounds.return_value = mock_ee
        mock_ee.filterDate.return_value = mock_ee
        mock_ee.median.return_value = mock_ee
        mock_ee.clip.return_value = mock_ee
        mock_ee.Initialize.return_value = None
        mock_image = MagicMock()
        mock_image.getDownloadURL.return_value = "http://example.com/test.tif"
        mock_ee.median.return_value.clip.return_value = mock_image

        with patch.dict("sys.modules", {"ee": mock_ee}):
            result = download_via_gee(
                tile_id="T_001",
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                satellite="landsat9",
                output_dir=tmp_path,
            )
        assert result is not None

    def test_unknown_satellite_raises(self, tmp_path):
        from src.satellite_io.sources import download_via_gee

        mock_ee = MagicMock()
        mock_ee.Geometry.Rectangle.return_value = "mock_region"
        mock_ee.Initialize.return_value = None

        with patch.dict("sys.modules", {"ee": mock_ee}):
            with pytest.raises(ValueError):
                download_via_gee(
                    tile_id="T_001",
                    bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                    satellite="invalid_satellite",
                    output_dir=tmp_path,
                )

    def test_ee_import_error(self):
        # Block ee import
        import sys as _sys

        from src.satellite_io.sources import download_via_gee

        saved = _sys.modules.get("ee")
        _sys.modules["ee"] = None
        try:
            with pytest.raises(ImportError):
                download_via_gee(
                    tile_id="T_001",
                    bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                )
        finally:
            if saved is None:
                _sys.modules.pop("ee", None)
            else:
                _sys.modules["ee"] = saved

    def test_download_url_failure_falls_back(self, tmp_path):
        """When getDownloadURL fails, returns the path anyway."""
        from src.satellite_io.sources import download_via_gee

        mock_ee = MagicMock()
        mock_ee.Geometry.Rectangle.return_value = "mock_region"
        mock_ee.ImageCollection.return_value = mock_ee
        mock_ee.filterBounds.return_value = mock_ee
        mock_ee.filterDate.return_value = mock_ee
        mock_ee.filter.return_value = mock_ee
        mock_ee.median.return_value = mock_ee
        mock_ee.clip.return_value = mock_ee
        mock_ee.Initialize.return_value = None
        mock_ee.Filter.lt.return_value = "mock_filter"
        mock_image = MagicMock()
        mock_image.getDownloadURL.side_effect = Exception("GEE error")
        mock_ee.median.return_value.clip.return_value = mock_image

        with patch.dict("sys.modules", {"ee": mock_ee}):
            result = download_via_gee(
                tile_id="T_001",
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                output_dir=tmp_path,
            )
        # Should still return a path
        assert result is not None
