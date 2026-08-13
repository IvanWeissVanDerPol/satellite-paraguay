"""Parcel analysis module.

Handles intersection of satellite data with Catastro parcels and indigenous territories.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask as rasterio_mask
from shapely.geometry import box

from ..paraguay_admin import load_catastro_parcels, load_indigenous_territories


def get_parcels_in_tile(
    tile_bbox: Dict[str, float],
    data_dir: Optional[Path] = None,
) -> gpd.GeoDataFrame:
    """Get Catastro parcels that intersect a tile bounding box.

    Args:
        tile_bbox: {min_lon, max_lon, min_lat, max_lat}
        data_dir: paraguay-geodata path

    Returns:
        GeoDataFrame with intersecting parcels
    """
    parcels = load_catastro_parcels(data_dir)  # type: ignore[arg-type]
    tile_geom = box(
        tile_bbox["min_lon"],
        tile_bbox["min_lat"],
        tile_bbox["max_lon"],
        tile_bbox["max_lat"],
    )
    mask = parcels.intersects(tile_geom)
    return parcels[mask].copy()


def get_indigenous_in_tile(
    tile_bbox: Dict[str, float],
    data_dir: Optional[Path] = None,
) -> gpd.GeoDataFrame:
    """Get indigenous territories intersecting a tile."""
    indigenous = load_indigenous_territories(data_dir)  # type: ignore[arg-type]
    tile_geom = box(
        tile_bbox["min_lon"],
        tile_bbox["min_lat"],
        tile_bbox["max_lon"],
        tile_bbox["max_lat"],
    )
    mask = indigenous.intersects(tile_geom)
    return indigenous[mask].copy()


def clip_raster_to_parcel(
    raster_path: Path,
    parcel_geometry,
    output_path: Optional[Path] = None,
) -> Tuple[np.ndarray, dict]:
    """Clip a raster to a parcel polygon.

    Args:
        raster_path: input GeoTIFF
        parcel_geometry: shapely geometry
        output_path: where to save clipped raster

    Returns:
        (array, profile)
    """
    with rasterio.open(raster_path) as src:
        clipped, transform = rasterio_mask(
            src,
            [parcel_geometry],
            crop=True,
        )
        profile = src.profile.copy()
        profile.update(
            height=clipped.shape[1],
            width=clipped.shape[2],
            transform=transform,
        )

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(clipped)

    return clipped, profile


def compute_parcel_statistics(
    parcel_id: str,
    raster_path: Path,
    data_dir: Optional[Path] = None,
) -> Dict[str, float]:
    """Compute statistics of a raster over a parcel.

    Returns dict with mean, median, std, min, max, sum of pixel values.
    """
    parcels = load_catastro_parcels(data_dir)  # type: ignore[arg-type]
    parcel = parcels[parcels["id"] == parcel_id].iloc[0] if "id" in parcels.columns else parcels.iloc[0]

    arr, _ = clip_raster_to_parcel(raster_path, parcel.geometry)

    # Filter out nodata
    valid = arr[arr != 0]

    if valid.size == 0:
        return {"mean": np.nan, "median": np.nan, "std": np.nan, "min": np.nan, "max": np.nan}

    return {
        "mean": float(np.mean(valid)),
        "median": float(np.median(valid)),
        "std": float(np.std(valid)),
        "min": float(np.min(valid)),
        "max": float(np.max(valid)),
        "count": int(valid.size),
    }


def detect_parcel_conflicts(
    parcel_id: str,
    indigenous_data_dir: Optional[Path] = None,
    catastro_data_dir: Optional[Path] = None,
) -> Dict:
    """Detect conflicts between Catastro parcel and indigenous territory.

    Returns dict with conflict info for the Yvy (P0012) paper.
    """
    parcels = load_catastro_parcels(catastro_data_dir)  # type: ignore[arg-type]
    indigenous = load_indigenous_territories(indigenous_data_dir)  # type: ignore[arg-type]

    # Find parcel
    if "id" in parcels.columns:
        parcel = parcels[parcels["id"] == parcel_id].iloc[0]
    else:
        parcel = parcels.iloc[0]

    # Check overlap with indigenous
    conflicts = indigenous[indigenous.intersects(parcel.geometry)]

    return {
        "parcel_id": parcel_id,
        "parcel_area": parcel.geometry.area,
        "indigenous_conflicts": len(conflicts),
        "conflict_geometries": conflicts.geometry.tolist() if len(conflicts) > 0 else [],
    }


if __name__ == "__main__":
    print("Parcel analysis module")
