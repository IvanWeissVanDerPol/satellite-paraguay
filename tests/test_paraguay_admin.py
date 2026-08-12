"""Tests for src.paraguay_admin module."""

from src.paraguay_admin import (
    get_tile_bbox,
    list_tiles_in_region,
    load_catastro_parcels,
    load_indigenous_territories,
    load_tile_index,
)
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


# 2026-08-13: Per-test skipif — pure-Python tests still run, file-loading
# tests skip when the geodata dir isn't readable (sandbox/CI without
# /root/paraguay-geodata).
_DATA_DIR = Path(os.environ.get("PARAGUAY_GEODATA_DIR", "/root/paraguay-geodata/exports/web/data"))
try:
    _HAS_DATA = os.access(_DATA_DIR, os.R_OK) and _DATA_DIR.is_dir()
except (PermissionError, OSError):
    _HAS_DATA = False
NEEDS_REAL_DATA = pytest.mark.skipif(
    not _HAS_DATA,
    reason="paraguay-geodata not readable at /root/paraguay-geodata/exports/web/data "
    "(set PARAGUAY_GEODATA_DIR to enable)",
)


def test_get_tile_bbox():
    """Verify tile bbox calculation."""
    bbox = get_tile_bbox("-54.267_-21.164")
    assert bbox is not None
    assert "min_lon" in bbox
    assert "max_lon" in bbox
    assert "center_lon" in bbox
    assert bbox["center_lon"] == pytest.approx(-54.267, abs=1e-3)
    assert bbox["center_lat"] == pytest.approx(-21.164, abs=1e-3)


def test_get_tile_bbox_invalid():
    """Verify invalid tile returns None."""
    assert get_tile_bbox("invalid") is None
    assert get_tile_bbox("1_2_3") is None


@NEEDS_REAL_DATA
def test_list_tiles_in_region():
    """Verify tile listing."""
    bbox = {
        "min_lon": -55.0,
        "max_lon": -54.0,
        "min_lat": -22.0,
        "max_lat": -21.0,
    }
    tiles = list_tiles_in_region(bbox)
    assert isinstance(tiles, list)
    # All tiles should be in bbox
    for tile_id in tiles:
        lon, lat = tile_id.split("_")
        lon, lat = float(lon), float(lat)
        assert -55.0 <= lon <= -54.0
        assert -22.0 <= lat <= -21.0


@NEEDS_REAL_DATA
def test_load_tile_index():
    """Verify tile index loads."""
    try:
        tiles = load_tile_index()
        assert len(tiles) > 100
    except FileNotFoundError:
        pytest.skip("paraguay-geodata not available")


@NEEDS_REAL_DATA
def test_load_catastro_parcels():
    """Verify Catastro loads."""
    try:
        catastro = load_catastro_parcels()
        assert len(catastro) > 100
        assert "geometry" in catastro.columns
    except FileNotFoundError:
        pytest.skip("paraguay-geodata not available")


@NEEDS_REAL_DATA
def test_load_indigenous_territories():
    """Verify indigenous territories load."""
    try:
        indigenous = load_indigenous_territories()
        assert len(indigenous) >= 1
        assert "geometry" in indigenous.columns
    except FileNotFoundError:
        pytest.skip("paraguay-geodata not available")
