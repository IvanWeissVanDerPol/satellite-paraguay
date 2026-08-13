"""Tests for src/paraguay_admin/real_analysis.py.

Coverage target: 70%+. Uses real Paraguay geodata from
/root/paraguay-geodata/exports/web/data when available, with
synthetic fallbacks.
"""

import os
from pathlib import Path

import pytest  # noqa: E402

pytest.importorskip("geopandas", reason="CI: requires optional system dep 'geopandas' (not installed)")  # noqa: E402

import geopandas as gpd  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402

REAL_DATA_DIR = Path("/root/paraguay-geodata/exports/web/data")


# Skip all tests if real data doesn't exist
# 2026-08-13: Use os.access to avoid PermissionError when /root is not
# readable (e.g., when CI runs as a non-root user, or when the sandbox
# filesystem forbids stat() on /root).

try:
    _has_real_data = os.access(REAL_DATA_DIR, os.R_OK) and REAL_DATA_DIR.is_dir()
except (PermissionError, OSError):
    _has_real_data = False

pytestmark = pytest.mark.skipif(
    not _has_real_data,
    reason="Paraguay geodata not available",
)


class TestFindCatastroPaths:
    """Tests for _find_catastro_paths helper."""

    def test_finds_in_admin_dir(self, tmp_path):
        from src.paraguay_admin.real_analysis import _find_catastro_paths

        admin = tmp_path / "admin"
        admin.mkdir()
        (admin / "catastro_parcels_sample.geojson").write_text("{}")
        result = _find_catastro_paths(tmp_path)
        assert len(result) >= 1
        assert any("catastro" in p.name for p in result)

    def test_finds_in_root(self, tmp_path):
        from src.paraguay_admin.real_analysis import _find_catastro_paths

        (tmp_path / "catastro_urba.geojson").write_text("{}")
        result = _find_catastro_paths(tmp_path)
        assert len(result) >= 1

    def test_no_files_returns_empty(self, tmp_path):
        from src.paraguay_admin.real_analysis import _find_catastro_paths

        result = _find_catastro_paths(tmp_path)
        assert result == []

    def test_finds_multiple_files(self, tmp_path):
        from src.paraguay_admin.real_analysis import _find_catastro_paths

        (tmp_path / "catastro_urba.geojson").write_text("{}")
        admin = tmp_path / "admin"
        admin.mkdir()
        (admin / "catastro_dist.geojson").write_text("{}")
        result = _find_catastro_paths(tmp_path)
        assert len(result) == 2


class TestFindIndigenousPath:
    """Tests for _find_indigenous_path helper."""

    def test_found_in_admin(self, tmp_path):
        from src.paraguay_admin.real_analysis import _find_indigenous_path

        admin = tmp_path / "admin"
        admin.mkdir()
        (admin / "indigenous_territories.geojson").write_text("{}")
        result = _find_indigenous_path(tmp_path)
        assert result is not None
        assert "indigenous_territories" in result.name

    def test_found_in_root(self, tmp_path):
        from src.paraguay_admin.real_analysis import _find_indigenous_path

        (tmp_path / "indigenous_territories.geojson").write_text("{}")
        result = _find_indigenous_path(tmp_path)
        assert result is not None

    def test_not_found_returns_none(self, tmp_path):
        from src.paraguay_admin.real_analysis import _find_indigenous_path

        result = _find_indigenous_path(tmp_path)
        assert result is None


class TestLoadCatastroParcelsReal:
    """Tests for load_catastro_parcels_real function."""

    def test_load_from_real_dir(self):
        """Load from default /root/paraguay-geodata directory."""
        from src.paraguay_admin.real_analysis import load_catastro_parcels_real

        if not (REAL_DATA_DIR / "admin" / "catastro_parcels_sample.geojson").exists():
            pytest.skip("catastro_parcels_sample.geojson not available")
        gdf = load_catastro_parcels_real()
        assert isinstance(gdf, gpd.GeoDataFrame)
        assert len(gdf) > 0

    def test_load_raises_when_no_files(self, tmp_path):
        from src.paraguay_admin.real_analysis import load_catastro_parcels_real

        with pytest.raises(FileNotFoundError):
            load_catastro_parcels_real(data_dir=tmp_path)

    def test_load_handles_failed_files_gracefully(self, tmp_path):
        """If files exist but fail to load, should raise."""
        from src.paraguay_admin.real_analysis import load_catastro_parcels_real

        (tmp_path / "catastro_urba.geojson").write_text("not valid geojson")
        with pytest.raises(FileNotFoundError):
            load_catastro_parcels_real(data_dir=tmp_path)

    def test_load_adds_source_file_column(self):
        from src.paraguay_admin.real_analysis import load_catastro_parcels_real

        if not (REAL_DATA_DIR / "admin" / "catastro_parcels_sample.geojson").exists():
            pytest.skip("catastro not available")
        gdf = load_catastro_parcels_real()
        assert "source_file" in gdf.columns


class TestLoadIndigenousTerritoriesReal:
    """Tests for load_indigenous_territories_real function."""

    def test_load_from_real_dir(self):
        from src.paraguay_admin.real_analysis import load_indigenous_territories_real

        if (
            not (REAL_DATA_DIR / "indigenous_territories.geojson").exists()
            and not (REAL_DATA_DIR / "admin" / "indigenous_territories.geojson").exists()
        ):
            pytest.skip("indigenous_territories.geojson not available")
        gdf = load_indigenous_territories_real()
        assert isinstance(gdf, gpd.GeoDataFrame)

    def test_load_raises_when_not_found(self, tmp_path):
        from src.paraguay_admin.real_analysis import load_indigenous_territories_real

        with pytest.raises(FileNotFoundError):
            load_indigenous_territories_real(data_dir=tmp_path)


class TestDetectConflictsReal:
    """Tests for detect_conflicts_real function.

    detect_conflicts_real(buffer_m=100, data_dir=None) — loads internally.
    """

    def test_detect_conflicts_returns_dict(self):
        from src.paraguay_admin.real_analysis import detect_conflicts_real

        try:
            result = detect_conflicts_real(buffer_m=50)
        except FileNotFoundError:
            pytest.skip("Real data not available")
        assert isinstance(result, dict)
        assert "total_parcels" in result
        assert "conflict_parcels" in result
        assert "conflict_fraction" in result

    def test_detect_conflicts_custom_buffer(self):
        from src.paraguay_admin.real_analysis import detect_conflicts_real

        try:
            result = detect_conflicts_real(buffer_m=500)
        except FileNotFoundError:
            pytest.skip("Real data not available")
        assert isinstance(result, dict)


class TestGetParcelsInDepartment:
    """Tests for get_parcels_in_department function."""

    def test_get_parcels_in_department(self):
        from src.paraguay_admin.real_analysis import (
            get_parcels_in_department,
        )

        try:
            result = get_parcels_in_department("Central")
        except FileNotFoundError:
            pytest.skip("catastro not available")
        assert isinstance(result, gpd.GeoDataFrame)

    def test_get_parcels_unknown_department(self):
        from src.paraguay_admin.real_analysis import (
            get_parcels_in_department,
        )

        try:
            result = get_parcels_in_department("FakeDept123")
        except FileNotFoundError:
            pytest.skip("catastro not available")
        # Should return empty or partial match
        assert isinstance(result, gpd.GeoDataFrame)


class TestComputeParcelSummaryStats:
    """Tests for compute_parcel_summary_stats function."""

    def test_returns_dict(self):
        from src.paraguay_admin.real_analysis import compute_parcel_summary_stats

        # Use a synthetic GeoDataFrame
        gdf = gpd.GeoDataFrame(
            {
                "id": ["P1", "P2", "P3"],
                "geometry": [
                    Polygon([(0, 0), (10, 0), (10, 10), (0, 10)]),
                    Polygon([(20, 20), (30, 20), (30, 30), (20, 30)]),
                    Polygon([(40, 40), (50, 40), (50, 50), (40, 50)]),
                ],
            }
        )
        result = compute_parcel_summary_stats(gdf)
        assert isinstance(result, dict)
        assert "count" in result
        assert result["count"] == 3

    def test_empty_gdf(self):
        from src.paraguay_admin.real_analysis import compute_parcel_summary_stats

        gdf = gpd.GeoDataFrame()
        result = compute_parcel_summary_stats(gdf)
        assert isinstance(result, dict)
        assert result["count"] == 0


class TestConstants:
    """Test module-level constants."""

    def test_pg_data_dir_is_path(self):
        from src.paraguay_admin import real_analysis

        assert isinstance(real_analysis.PG_DATA_DIR, Path)
