"""Tests for src/satellite_io/mapbiomas.py — GEE download path.

Coverage target: 90%+.
"""

import sys
from unittest.mock import MagicMock, patch

import numpy as np


class TestDownloadMapBiomasGeeSuccess:
    """Tests for GEE success path of mapbiomas download."""

    def test_full_gee_chain_returns_array(self, tmp_path, monkeypatch):
        """Mock full GEE chain — returns numpy array."""
        import io

        from src.satellite_io import mapbiomas as mb_mod

        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)

        # Mock ee with chains
        mock_year_img = MagicMock()
        mock_year_img.getThumbURL.return_value = "http://test/mb.tif"

        mock_img = MagicMock()
        mock_img.select.return_value = mock_year_img

        mock_ee = MagicMock()
        mock_ee.Initialize.return_value = None
        mock_ee.Geometry.Rectangle.return_value = "mock_aoi"
        mock_ee.Image.return_value = mock_img

        # Build real TIFF for rasterio
        import rasterio
        from rasterio.io import MemoryFile

        profile = {
            "driver": "GTiff",
            "dtype": "uint8",
            "width": 4,
            "height": 4,
            "count": 1,
            "crs": "EPSG:4326",
            "transform": rasterio.transform.from_bounds(-60, -25, -55, -20, 4, 4),
        }
        data = np.full((1, 4, 4), 3, dtype=np.uint8)  # Forest class
        buf = io.BytesIO()
        with MemoryFile() as mem:
            with mem.open(**profile) as dataset:
                dataset.write(data)
            buf.write(mem.read())
        tiff_bytes = buf.getvalue()

        with patch.dict(sys.modules, {"ee": mock_ee}):
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_response = MagicMock()
                mock_response.read.return_value = tiff_bytes
                mock_response.__enter__ = MagicMock(return_value=mock_response)
                mock_response.__exit__ = MagicMock(return_value=False)
                mock_urlopen.return_value = mock_response

                result = mb_mod.download_mapbiomas_paraguay_real(
                    bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                    year=2020,
                )
        assert isinstance(result, np.ndarray)
        assert result.shape == (4, 4)
        # Should have saved to cache
        cache_file = tmp_path / "mapbiomas_py_2020.npy"
        assert cache_file.exists()


class TestDownloadMapBiomasFallback:
    """Tests for fallback paths."""

    def test_no_gee_returns_synthetic(self, tmp_path, monkeypatch):
        from src.satellite_io import mapbiomas as mb_mod

        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)
        saved = sys.modules.get("ee")
        sys.modules["ee"] = None
        try:
            result = mb_mod.download_mapbiomas_paraguay_real(
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                year=2021,
            )
            assert isinstance(result, np.ndarray)
        finally:
            if saved is None:
                sys.modules.pop("ee", None)
            else:
                sys.modules["ee"] = saved

    def test_use_gee_false_skips(self, tmp_path, monkeypatch):
        from src.satellite_io import mapbiomas as mb_mod

        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)
        result = mb_mod.download_mapbiomas_paraguay_real(
            bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            year=2018,
            use_gee=False,
        )
        assert isinstance(result, np.ndarray)


class TestDownloadMapBiomasCache:
    """Tests for cache hit path."""

    def test_cache_hit_returns_immediately(self, tmp_path, monkeypatch):
        """Pre-populated cache returns without GEE call."""
        from src.satellite_io import mapbiomas as mb_mod

        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)

        # Pre-populate cache
        cache_file = tmp_path / "mapbiomas_py_2022.npy"
        cached_arr = np.full((10, 10), 5, dtype=np.uint8)
        np.save(cache_file, cached_arr)

        # Block GEE call
        saved = sys.modules.get("ee")
        sys.modules["ee"] = None
        try:
            result = mb_mod.download_mapbiomas_paraguay_real(
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                year=2022,
            )
            np.testing.assert_array_equal(result, cached_arr)
        finally:
            if saved is None:
                sys.modules.pop("ee", None)
            else:
                sys.modules["ee"] = saved


class TestDownloadMapBiomasEdgeCases:
    """Additional edge case coverage."""

    def test_gee_initialize_raises(self, tmp_path, monkeypatch):
        """When ee.Initialize raises, fall back."""
        from src.satellite_io import mapbiomas as mb_mod

        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)

        mock_ee = MagicMock()
        mock_ee.Initialize.side_effect = Exception("auth failed")
        mock_ee.Geometry.Rectangle.return_value = "mock_aoi"

        with patch.dict(sys.modules, {"ee": mock_ee}):
            result = mb_mod.download_mapbiomas_paraguay_real(
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                year=2020,
            )
        assert isinstance(result, np.ndarray)

    def test_full_gee_download_fails_falls_back(self, tmp_path, monkeypatch):
        """When urlopen fails, fall back to synthetic."""
        from src.satellite_io import mapbiomas as mb_mod

        monkeypatch.setattr(mb_mod, "CACHE_DIR", tmp_path)

        mock_year_img = MagicMock()
        mock_year_img.getThumbURL.return_value = "http://test/mb.tif"

        mock_img = MagicMock()
        mock_img.select.return_value = mock_year_img

        mock_ee = MagicMock()
        mock_ee.Initialize.return_value = None
        mock_ee.Geometry.Rectangle.return_value = "mock_aoi"
        mock_ee.Image.return_value = mock_img

        with patch.dict(sys.modules, {"ee": mock_ee}):
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_urlopen.side_effect = Exception("Network error")
                result = mb_mod.download_mapbiomas_paraguay_real(
                    bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                    year=2019,
                )
        assert isinstance(result, np.ndarray)
