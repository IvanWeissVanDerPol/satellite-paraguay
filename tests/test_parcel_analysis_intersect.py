"""Tests for src/parcel_analysis/intersect.py.

Coverage target: 70%+. Tests intersection helpers using
synthetic GeoDataFrames and mocks for rasterio.
"""
import pytest
import numpy as np
import geopandas as gpd
from pathlib import Path
from unittest.mock import patch, MagicMock
from shapely.geometry import box, Polygon


class TestGetParcelsInTile:
    """Tests for get_parcels_in_tile function."""

    def test_get_parcels_intersecting_tile(self, tmp_path):
        """Find parcels that intersect a tile bbox."""
        from src.parcel_analysis.intersect import get_parcels_in_tile

        # Create mock parcels
        parcels = gpd.GeoDataFrame({
            "id": ["P1", "P2", "P3"],
            "geometry": [
                Polygon([(0, 0), (10, 0), (10, 10), (0, 10)]),  # inside
                Polygon([(50, 50), (60, 50), (60, 60), (50, 60)]),  # outside
                Polygon([(5, 5), (15, 5), (15, 15), (5, 15)]),  # inside
            ],
        })

        bbox = {"min_lon": -5, "max_lon": 20, "min_lat": -5, "max_lat": 20}

        with patch("src.parcel_analysis.intersect.load_catastro_parcels", return_value=parcels):
            result = get_parcels_in_tile(bbox, data_dir=tmp_path)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 2  # P1 and P3

    def test_get_parcels_no_intersection(self, tmp_path):
        """No parcels intersect the tile."""
        from src.parcel_analysis.intersect import get_parcels_in_tile

        parcels = gpd.GeoDataFrame({
            "id": ["P1"],
            "geometry": [Polygon([(100, 100), (110, 100), (110, 110), (100, 110)])],
        })
        bbox = {"min_lon": 0, "max_lon": 10, "min_lat": 0, "max_lat": 10}

        with patch("src.parcel_analysis.intersect.load_catastro_parcels", return_value=parcels):
            result = get_parcels_in_tile(bbox, data_dir=tmp_path)

        assert len(result) == 0


class TestGetIndigenousInTile:
    """Tests for get_indigenous_in_tile function."""

    def test_get_indigenous_intersecting_tile(self, tmp_path):
        from src.parcel_analysis.intersect import get_indigenous_in_tile

        indigenous = gpd.GeoDataFrame({
            "id": ["I1", "I2"],
            "geometry": [
                Polygon([(0, 0), (10, 0), (10, 10), (0, 10)]),
                Polygon([(50, 50), (60, 50), (60, 60), (50, 60)]),
            ],
        })

        bbox = {"min_lon": -5, "max_lon": 20, "min_lat": -5, "max_lat": 20}

        with patch("src.parcel_analysis.intersect.load_indigenous_territories", return_value=indigenous):
            result = get_indigenous_in_tile(bbox, data_dir=tmp_path)

        assert isinstance(result, gpd.GeoDataFrame)
        assert len(result) == 1


class TestClipRasterToParcel:
    """Tests for clip_raster_to_parcel function."""

    def test_clip_raster(self, tmp_path):
        """Clip a raster using a parcel geometry."""
        from src.parcel_analysis.intersect import clip_raster_to_parcel

        # Mock rasterio
        arr = np.random.rand(3, 50, 50).astype(np.float32)
        profile = {"driver": "GTiff", "dtype": "float32", "height": 50, "width": 50}

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        mock_src.profile = profile

        # Mock rasterio_mask to return (clipped_array, transform)
        clipped_arr = np.random.rand(3, 20, 20).astype(np.float32)
        from rasterio.transform import Affine
        transform = Affine(1.0, 0.0, 0.0, 0.0, -1.0, 20.0)

        with patch("src.parcel_analysis.intersect.rasterio.open", return_value=mock_src):
            with patch("src.parcel_analysis.intersect.rasterio_mask", return_value=(clipped_arr, transform)):
                parcel_geom = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
                result_arr, result_profile = clip_raster_to_parcel(
                    tmp_path / "test.tif", parcel_geom
                )

        assert isinstance(result_arr, np.ndarray)
        assert result_profile["height"] == 20

    def test_clip_raster_with_output(self, tmp_path):
        """Clip a raster and write to output."""
        from src.parcel_analysis.intersect import clip_raster_to_parcel

        arr = np.random.rand(3, 20, 20).astype(np.float32)
        from rasterio.transform import Affine
        transform = Affine(1.0, 0.0, 0.0, 0.0, -1.0, 20.0)

        mock_src = MagicMock()
        mock_src.__enter__ = MagicMock(return_value=mock_src)
        mock_src.__exit__ = MagicMock(return_value=False)
        mock_src.profile = {"driver": "GTiff", "dtype": "float32"}

        # Mock the destination write
        mock_dst = MagicMock()
        mock_dst.__enter__ = MagicMock(return_value=mock_dst)
        mock_dst.__exit__ = MagicMock(return_value=False)

        with patch("src.parcel_analysis.intersect.rasterio.open") as mock_open:
            mock_open.side_effect = [mock_src, mock_dst]
            with patch("src.parcel_analysis.intersect.rasterio_mask", return_value=(arr, transform)):
                parcel_geom = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
                output = tmp_path / "out.tif"
                clip_raster_to_parcel(
                    tmp_path / "test.tif", parcel_geom, output_path=output
                )


class TestComputeParcelStatistics:
    """Tests for compute_parcel_statistics function."""

    def test_compute_stats_with_id_column(self, tmp_path):
        """Find parcel by id and compute stats."""
        from src.parcel_analysis.intersect import compute_parcel_statistics

        parcels = gpd.GeoDataFrame({
            "id": ["P1", "P2"],
            "geometry": [
                Polygon([(0, 0), (10, 0), (10, 10), (0, 10)]),
                Polygon([(20, 20), (30, 20), (30, 30), (20, 30)]),
            ],
        })

        # Mock clipped raster
        arr = np.array([[[10, 20, 30], [40, 50, 60], [70, 80, 90]]], dtype=np.float32)

        with patch("src.parcel_analysis.intersect.load_catastro_parcels", return_value=parcels):
            with patch("src.parcel_analysis.intersect.clip_raster_to_parcel", return_value=(arr, {})):
                stats = compute_parcel_statistics("P1", tmp_path / "test.tif")

        assert "mean" in stats
        assert stats["mean"] > 0

    def test_compute_stats_no_id_column(self, tmp_path):
        """When no 'id' column, use first parcel."""
        from src.parcel_analysis.intersect import compute_parcel_statistics

        parcels = gpd.GeoDataFrame({
            "geometry": [Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])],
        })
        arr = np.array([[[10, 20, 30]]], dtype=np.float32)

        with patch("src.parcel_analysis.intersect.load_catastro_parcels", return_value=parcels):
            with patch("src.parcel_analysis.intersect.clip_raster_to_parcel", return_value=(arr, {})):
                stats = compute_parcel_statistics("P1", tmp_path / "test.tif")
        assert "mean" in stats

    def test_compute_stats_zero_raster(self, tmp_path):
        """All-zero raster returns NaN stats."""
        from src.parcel_analysis.intersect import compute_parcel_statistics

        parcels = gpd.GeoDataFrame({
            "id": ["P1"],
            "geometry": [Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])],
        })
        arr = np.zeros((1, 5, 5), dtype=np.float32)

        with patch("src.parcel_analysis.intersect.load_catastro_parcels", return_value=parcels):
            with patch("src.parcel_analysis.intersect.clip_raster_to_parcel", return_value=(arr, {})):
                stats = compute_parcel_statistics("P1", tmp_path / "test.tif")
        # All values are 0, filtered out
        assert np.isnan(stats["mean"]) or stats["mean"] == 0


class TestDetectParcelConflicts:
    """Tests for detect_parcel_conflicts function."""

    def test_detect_no_conflicts(self, tmp_path):
        """Parcel doesn't overlap any indigenous territory."""
        from src.parcel_analysis.intersect import detect_parcel_conflicts

        parcels = gpd.GeoDataFrame({
            "id": ["P1"],
            "geometry": [Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])],
        })
        indigenous = gpd.GeoDataFrame({
            "id": ["I1"],
            "geometry": [Polygon([(100, 100), (110, 100), (110, 110), (100, 110)])],
        })

        with patch("src.parcel_analysis.intersect.load_catastro_parcels", return_value=parcels):
            with patch("src.parcel_analysis.intersect.load_indigenous_territories", return_value=indigenous):
                result = detect_parcel_conflicts("P1")
        assert isinstance(result, dict)
        assert result["parcel_id"] == "P1"
        assert result["indigenous_conflicts"] == 0

    def test_detect_with_conflict(self, tmp_path):
        """Parcel overlaps an indigenous territory."""
        from src.parcel_analysis.intersect import detect_parcel_conflicts

        parcels = gpd.GeoDataFrame({
            "id": ["P1"],
            "geometry": [Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])],
        })
        indigenous = gpd.GeoDataFrame({
            "id": ["I1", "I2"],
            "geometry": [
                Polygon([(5, 5), (15, 5), (15, 15), (5, 15)]),  # overlaps
                Polygon([(100, 100), (110, 100), (110, 110), (100, 110)]),  # doesn't
            ],
        })

        with patch("src.parcel_analysis.intersect.load_catastro_parcels", return_value=parcels):
            with patch("src.parcel_analysis.intersect.load_indigenous_territories", return_value=indigenous):
                result = detect_parcel_conflicts("P1")
        assert result["indigenous_conflicts"] == 1


class TestModuleImport:
    """Tests for module import."""

    def test_module_imports(self):
        from src.parcel_analysis import intersect
        assert intersect is not None