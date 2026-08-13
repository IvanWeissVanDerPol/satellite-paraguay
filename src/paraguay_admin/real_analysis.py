"""Real Catastro + indigenous territory analysis.

Uses local Paraguay geodata (already in /root/paraguay-geodata/) for:
- 7,500 Catastro parcels
- Indigenous territories
- Conflict detection

Production-grade replacement for the stub in src/parcel_analysis/intersect.py.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)


PG_DATA_DIR = Path(os.environ.get("PARAGUAY_GEODATA_PATH", "/root/paraguay-geodata/exports/web/data"))


def _find_catastro_paths(data_dir: Path) -> List[Path]:
    """Find Catastro files in either root or admin/ subdirectory."""
    paths = []
    for fname in ["catastro_parcels_sample.geojson", "catastro_urba.geojson", "catastro_dist.geojson"]:
        # Try root
        root_path = data_dir / fname
        if root_path.exists():
            paths.append(root_path)
        # Try admin/
        admin_path = data_dir / "admin" / fname
        if admin_path.exists():
            paths.append(admin_path)
    return paths


def _find_indigenous_path(data_dir: Path) -> Optional[Path]:
    """Find indigenous territories file."""
    for subdir in ["", "admin"]:
        path = data_dir / subdir / "indigenous_territories.geojson"
        if path.exists():
            return path
    return None


def load_catastro_parcels_real(data_dir: Path = None) -> gpd.GeoDataFrame:
    """Load Catastro parcels from local Paraguay geodata."""
    if data_dir is None:
        data_dir = PG_DATA_DIR

    catastro_paths = _find_catastro_paths(data_dir)
    if not catastro_paths:
        raise FileNotFoundError(f"No Catastro data found in {data_dir}")

    gdfs = []
    for path in catastro_paths:
        try:
            gdf = gpd.read_file(path)
            gdf["source_file"] = path.name
            gdfs.append(gdf)
            logger.info(f"Loaded {len(gdf)} parcels from {path.name}")
        except Exception as e:
            logger.warning(f"Failed to load {path}: {e}")

    if not gdfs:
        raise FileNotFoundError(f"Failed to load any Catastro data in {data_dir}")

    # Combine
    combined = pd.concat(gdfs, ignore_index=True)
    # Deduplicate by geometry
    if "id" in combined.columns:
        combined = combined.drop_duplicates(subset=["id"])
    else:
        combined = combined.drop_duplicates(subset=["geometry"])

    return combined


def load_indigenous_territories_real(data_dir: Path = None) -> gpd.GeoDataFrame:
    """Load indigenous territories from local Paraguay geodata."""
    if data_dir is None:
        data_dir = PG_DATA_DIR

    path = _find_indigenous_path(data_dir)
    if path is None:
        raise FileNotFoundError(f"Indigenous territories not found in {data_dir}")

    gdf = gpd.read_file(path)
    logger.info(f"Loaded {len(gdf)} indigenous territories from {path.name}")
    return gdf


def detect_conflicts_real(
    buffer_m: float = 100,
    data_dir: Path = None,
) -> Dict:
    """Detect real conflicts between Catastro parcels and indigenous territories.

    A conflict occurs when a Catastro parcel overlaps or is within
    buffer_m of an indigenous territory boundary.

    Args:
        buffer_m: buffer distance in meters
        data_dir: Paraguay geodata directory

    Returns:
        Dict with conflict statistics
    """
    if data_dir is None:
        data_dir = PG_DATA_DIR

    parcels = load_catastro_parcels_real(data_dir)
    indigenous = load_indigenous_territories_real(data_dir)

    # Ensure same CRS
    if parcels.crs != indigenous.crs:
        indigenous = indigenous.to_crs(parcels.crs)

    # Reproject to projected CRS for accurate distance calculations
    # Paraguay uses UTM zone 21S (EPSG:32721) for eastern region
    target_crs = "EPSG:32721"
    try:
        parcels_proj = parcels.to_crs(target_crs)
        indigenous_proj = indigenous.to_crs(target_crs)
    except Exception as e:
        logger.warning(f"Reprojection failed ({e}), using original CRS")
        parcels_proj = parcels
        indigenous_proj = indigenous

    # Buffer indigenous territories (now in meters)
    indigenous_buffered = indigenous_proj.copy()
    indigenous_buffered["geometry"] = indigenous_proj.geometry.buffer(buffer_m)
    # Fix any invalid geometries from buffering
    indigenous_buffered["geometry"] = indigenous_buffered.geometry.buffer(0)

    # Find intersecting parcels
    logger.info(f"Checking {len(parcels_proj)} parcels against {len(indigenous_proj)} indigenous territories")
    indigenous_union = indigenous_buffered.unary_union
    conflicts_mask = parcels_proj.intersects(indigenous_union)
    conflicts = parcels_proj[conflicts_mask].copy()

    # Compute overlap area
    if not conflicts.empty:

        def compute_overlap(g):
            try:
                if g.intersects(indigenous_union):
                    return g.intersection(indigenous_union).area
            except Exception:
                return 0
            return 0

        conflicts["overlap_area_m2"] = conflicts.geometry.apply(compute_overlap)
        conflicts["overlap_area_ha"] = conflicts["overlap_area_m2"] / 10000

    result = {
        "total_parcels": int(len(parcels)),
        "total_indigenous_territories": int(len(indigenous)),
        "conflict_parcels": int(len(conflicts)),
        "conflict_fraction": float(len(conflicts) / len(parcels)) if len(parcels) > 0 else 0,
        "buffer_m": buffer_m,
        "conflicts": conflicts,
        "timestamp": datetime.now().isoformat(),
    }

    logger.info(f"Found {len(conflicts)} conflicts ({result['conflict_fraction']*100:.2f}% of parcels)")

    return result


def get_parcels_in_department(
    department: str,
    data_dir: Path = None,
) -> gpd.GeoDataFrame:
    """Get all parcels in a specific department."""
    parcels = load_catastro_parcels_real(data_dir)

    if "department" in parcels.columns:
        return parcels[parcels["department"] == department].copy()
    elif "departamento" in parcels.columns:
        return parcels[parcels["departamento"] == department].copy()
    else:
        logger.warning(f"No department column found in parcels. Columns: {list(parcels.columns)}")
        return parcels


def compute_parcel_summary_stats(
    parcels: gpd.GeoDataFrame,
) -> Dict:
    """Compute summary statistics for a set of parcels."""
    if parcels.empty:
        return {"count": 0}

    areas = parcels.geometry.area
    centroids = parcels.geometry.centroid

    return {
        "count": int(len(parcels)),
        "total_area_m2": float(areas.sum()),
        "total_area_ha": float(areas.sum() / 10000),
        "mean_area_m2": float(areas.mean()),
        "median_area_m2": float(areas.median()),
        "bbox": {
            "min_lon": float(centroids.x.min()),
            "max_lon": float(centroids.x.max()),
            "min_lat": float(centroids.y.min()),
            "max_lat": float(centroids.y.max()),
        },
    }


if __name__ == "__main__":
    print("Real Catastro + Indigenous analysis")
    print("=" * 60)

    try:
        result = detect_conflicts_real(buffer_m=100)
        print(f"\nTotal parcels: {result['total_parcels']}")
        print(f"Indigenous territories: {result['total_indigenous_territories']}")
        print(f"Conflict parcels: {result['conflict_parcels']}")
        print(f"Conflict fraction: {result['conflict_fraction']*100:.2f}%")

        if not result["conflicts"].empty:
            print("\nFirst 3 conflicts:")
            print(result["conflicts"][[c for c in result["conflicts"].columns if c != "geometry"]].head(3).to_string())
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
