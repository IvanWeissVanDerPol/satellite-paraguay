"""Paraguay admin boundaries + tile grid loader.

Handles:
- 18 departamentos
- 268 distritos
- 7,912 tiles (10x10 km grid from paraguay-geodata)
- Indigenous territories
- Catastro parcels

All data is loaded from /root/paraguay-geodata/ (already available).
"""
from pathlib import Path
from typing import Optional, List, Dict
import json

import geopandas as gpd
import pandas as pd

# Default path to paraguay-geodata
DEFAULT_DATA_DIR = Path("/root/paraguay-geodata/exports/web/data")


def load_departamentos(data_dir: Path = DEFAULT_DATA_DIR) -> gpd.GeoDataFrame:
    """Load 18 Paraguayan departments."""
    f = data_dir / "admin" / "departamentos.geojson"
    if not f.exists():
        # Try alternate name
        f = data_dir / "admin" / "departamentos_py.geojson"
    return gpd.read_file(f)


def load_distritos(data_dir: Path = DEFAULT_DATA_DIR) -> gpd.GeoDataFrame:
    """Load 268 Paraguayan districts."""
    f = data_dir / "admin" / "distritos.geojson"
    if not f.exists():
        f = data_dir / "admin" / "distritos_py.geojson"
    return gpd.read_file(f)


def load_catastro_parcels(data_dir: Path = DEFAULT_DATA_DIR) -> gpd.GeoDataFrame:
    """Load 7,500 Catastro parcelas."""
    f = data_dir / "admin" / "catastro_parcels_sample.geojson"
    if not f.exists():
        f = data_dir / "catastro_parcels_sample.geojson"
    return gpd.read_file(f)


def load_catastro_urbanizaciones(data_dir: Path = DEFAULT_DATA_DIR) -> gpd.GeoDataFrame:
    """Load 470 urbanizaciones."""
    f = data_dir / "admin" / "catastro_urba.geojson"
    if not f.exists():
        f = data_dir / "catastro_urba.geojson"
    return gpd.read_file(f)


def load_indigenous_territories(data_dir: Path = DEFAULT_DATA_DIR) -> gpd.GeoDataFrame:
    """Load indigenous territories."""
    f = data_dir / "indigenous_territories.geojson"
    return gpd.read_file(f)


def load_tile_index(data_dir: Path = DEFAULT_DATA_DIR) -> pd.DataFrame:
    """Load 7,912 tile index (10x10 km grid)."""
    f = data_dir / "tile_index.json"
    with open(f) as fp:
        tiles = json.load(fp)
    return pd.DataFrame(tiles)


def load_priority_tiles(data_dir: Path = DEFAULT_DATA_DIR) -> pd.DataFrame:
    """Load 37 priority urban-anchor tiles."""
    f = data_dir / "priority_tiles.json"
    with open(f) as fp:
        tiles = json.load(fp)
    return pd.DataFrame(tiles)


def get_country_boundary() -> gpd.GeoDataFrame:
    """Get country-level boundary as union of all departments."""
    deptos = load_departamentos()
    return gpd.GeoDataFrame(
        geometry=[deptos.unary_union],
        crs=deptos.crs,
    )


def get_tile_bbox(tile_id: str) -> Optional[Dict[str, float]]:
    """Get bounding box for a tile by ID.

    Args:
        tile_id: Format like "-54.267_-21.164" (lon_lat)

    Returns:
        Dict with keys: min_lon, max_lon, min_lat, max_lat, center_lon, center_lat
    """
    try:
        lon, lat = tile_id.split("_")
        lon, lat = float(lon), float(lat)
        # 10x10 km tile, so ~0.1 degrees
        delta = 0.05
        return {
            "min_lon": lon - delta,
            "max_lon": lon + delta,
            "min_lat": lat - delta,
            "max_lat": lat + delta,
            "center_lon": lon,
            "center_lat": lat,
        }
    except Exception:
        return None


def list_tiles_in_region(
    bbox: Dict[str, float],
    tile_index: Optional[pd.DataFrame] = None,
) -> List[str]:
    """List tile IDs that intersect a bounding box.

    Args:
        bbox: Dict with min_lon, max_lon, min_lat, max_lat
        tile_index: Optional pre-loaded DataFrame

    Returns:
        List of tile IDs
    """
    if tile_index is None:
        tile_index = load_tile_index()

    if "center_lon" not in tile_index.columns:
        # Build from tile_id
        tile_index = tile_index.copy()
        coords = tile_index["tile_id"].str.split("_", expand=True)
        tile_index["center_lon"] = coords[0].astype(float)
        tile_index["center_lat"] = coords[1].astype(float)

    mask = (
        (tile_index["center_lon"] >= bbox["min_lon"])
        & (tile_index["center_lon"] <= bbox["max_lon"])
        & (tile_index["center_lat"] >= bbox["min_lat"])
        & (tile_index["center_lat"] <= bbox["max_lat"])
    )
    return tile_index.loc[mask, "tile_id"].tolist()


if __name__ == "__main__":
    # Quick test
    print("Loading Paraguay admin data...")
    deptos = load_departamentos()
    print(f"  Departamentos: {len(deptos)}")

    distritos = load_distritos()
    print(f"  Distritos: {len(distritos)}")

    catastro = load_catastro_parcels()
    print(f"  Catastro parcels: {len(catastro)}")

    indigenous = load_indigenous_territories()
    print(f"  Indigenous territories: {len(indigenous)}")

    tiles = load_tile_index()
    print(f"  Tiles: {len(tiles)}")

    print("\nSample tile bbox:")
    print(get_tile_bbox("-54.267_-21.164"))
