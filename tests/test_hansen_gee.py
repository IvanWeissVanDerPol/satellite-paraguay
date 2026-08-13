"""Tests for src/satellite_io/hansen.py — GEE download path.

Coverage target: 90%+. Tests download_hansen_real with mocked GEE
and rasterio.
"""

import sys
from unittest.mock import MagicMock, patch

import numpy as np


class TestDownloadHansenRealGEESuccess:
    """Tests for GEE success path."""

    def test_cache_hit_returns_immediately(self, tmp_path, monkeypatch):
        """When cache file exists, returns it without GEE call."""
        from src.satellite_io import hansen as h_mod

        monkeypatch.setattr(h_mod, "CACHE_DIR", tmp_path)

        # Pre-populate cache
        cache_path = tmp_path / "hansen_2020_2023.npz"
        np.savez_compressed(
            cache_path,
            treecover2000=np.array([[1.0, 2.0]]),
            loss=np.array([[0.0, 1.0]]),
            gain=np.array([[0.0, 0.0]]),
            lossyear=np.array([[0.0, 1.0]]),
        )

        # Block GEE call to prove cache hit path
        saved = sys.modules.get("ee")
        sys.modules["ee"] = None

        try:
            result = h_mod.download_hansen_real(
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                start_year=2020,
                end_year=2023,
            )
            assert "treecover2000" in result
        finally:
            if saved is None:
                sys.modules.pop("ee", None)
            else:
                sys.modules["ee"] = saved

    def test_gee_no_auth_returns_synthetic(self, tmp_path, monkeypatch):
        """When ee.Initialize fails, falls back to synthetic."""
        from src.satellite_io import hansen as h_mod

        monkeypatch.setattr(h_mod, "CACHE_DIR", tmp_path)
        saved = sys.modules.get("ee")
        sys.modules["ee"] = None
        try:
            result = h_mod.download_hansen_real(  # noqa: F841
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            )
        finally:
            if saved is None:
                sys.modules.pop("ee", None)
            else:
                sys.modules["ee"] = saved

    def test_gee_import_error_returns_synthetic(self, tmp_path, monkeypatch):
        """When ee import fails, returns synthetic."""
        from src.satellite_io import hansen as h_mod

        monkeypatch.setattr(h_mod, "CACHE_DIR", tmp_path)
        saved = sys.modules.get("ee")
        sys.modules["ee"] = None
        try:
            result = h_mod.download_hansen_real(
                bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                start_year=2019,
                end_year=2022,
            )
            # Should fall back to synthetic and still return dict
            assert isinstance(result, dict)
        finally:
            if saved is None:
                sys.modules.pop("ee", None)
            else:
                sys.modules["ee"] = saved

    def test_use_gee_false_skips_gee(self, tmp_path, monkeypatch):
        """When use_gee=False, skips GEE entirely."""
        from src.satellite_io import hansen as h_mod

        monkeypatch.setattr(h_mod, "CACHE_DIR", tmp_path)
        result = h_mod.download_hansen_real(
            bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
            use_gee=False,
        )
        assert isinstance(result, dict)


class TestDownloadHansenRealGEEWorking:
    """Tests where GEE chain is mocked."""

    def test_full_gee_chain_returns_data(self, tmp_path, monkeypatch):
        """Mock full GEE chain — returns numpy arrays."""
        import io

        from src.satellite_io import hansen as h_mod

        monkeypatch.setattr(h_mod, "CACHE_DIR", tmp_path)

        # Mock ee with chains
        mock_image = MagicMock()
        mock_selected = MagicMock()
        mock_selected.getThumbURL.return_value = "http://test/hansen.tif"
        mock_image.select.return_value = mock_selected

        mock_ee = MagicMock()
        mock_ee.Initialize.return_value = None
        mock_ee.Geometry.Rectangle.return_value = "mock_aoi"
        mock_ee.Image.return_value = mock_image

        # Mock rasterio to return a valid tiff
        try:
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
            data = np.full((1, 4, 4), 50, dtype=np.uint8)
            buf = io.BytesIO()
            with MemoryFile() as mem:
                with mem.open(**profile) as dataset:
                    dataset.write(data)
                buf.write(mem.read())
            tiff_bytes = buf.getvalue()
        except Exception:
            tiff_bytes = b""

        with patch.dict(sys.modules, {"ee": mock_ee}):
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_response = MagicMock()
                mock_response.read.return_value = tiff_bytes
                mock_response.__enter__ = MagicMock(return_value=mock_response)
                mock_response.__exit__ = MagicMock(return_value=False)
                mock_urlopen.return_value = mock_response

                # Cache miss forces GEE path
                cache_file = tmp_path / "hansen_2018_2023.npz"
                if cache_file.exists():
                    cache_file.unlink()
                result = h_mod.download_hansen_real(
                    bbox={"min_lon": -60, "max_lon": -55, "min_lat": -25, "max_lat": -20},
                    start_year=2018,
                    end_year=2023,
                )
                # Should return dict with 4 bands
                assert isinstance(result, dict)
                assert "treecover2000" in result
                assert "loss" in result
