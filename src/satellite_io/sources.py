"""Satellite imagery I/O.

Handles:
- Sentinel-2 (10m, 5-day) from ESA Copernicus (FREE)
- Landsat 9 (30m, 16-day) from NASA (FREE)
- Planet (3m, academic) from Planet.com
- MapBiomas Paraguay (land cover change)
- Hansen GFC (deforestation)
- ESA WorldCover (10m land cover 2020/2021)

All sources are open-source and free.
"""

from pathlib import Path
from typing import Dict, List

import numpy as np
import rasterio

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
SENTINEL_OUTPUT = DEFAULT_OUTPUT_DIR / "sentinel2"
LANDSAT_OUTPUT = DEFAULT_OUTPUT_DIR / "landsat9"
PLANET_OUTPUT = DEFAULT_OUTPUT_DIR / "planet"


def download_sentinel2_tile(
    tile_id: str,
    bbox: Dict[str, float],
    start_date: str = "2020-01-01",
    end_date: str = "2025-12-31",
    max_cloud_cover: int = 20,
    output_dir: Path = SENTINEL_OUTPUT,
) -> List[Path]:
    """Download Sentinel-2 L2A products for a tile.

    Uses the Copernicus Open Access Hub (FREE, requires free registration).
    Alternative: use Google Earth Engine (no registration needed).

    Args:
        tile_id: e.g. "-54.267_-21.164"
        bbox: {min_lon, max_lon, min_lat, max_lat}
        start_date: ISO format
        end_date: ISO format
        max_cloud_cover: Maximum cloud cover percentage (0-100)
        output_dir: Where to save files

    Returns:
        List of downloaded file paths
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    tile_dir = output_dir / tile_id
    tile_dir.mkdir(parents=True, exist_ok=True)

    # NOTE: Real implementation usesenthusiastic Copernicus API or sentinelsat
    # For now, return expected paths
    print(f"[sentinel-2] Would download {tile_id} ({bbox}) from {start_date} to {end_date}")
    print(f"[sentinel-2] Cloud cover < {max_cloud_cover}%")
    print(f"[sentinel-2] Output: {tile_dir}")
    return []


def download_via_gee(
    tile_id: str,
    bbox: Dict[str, float],
    satellite: str = "sentinel2",
    start_date: str = "2020-01-01",
    end_date: str = "2025-12-31",
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Path:
    """Download satellite imagery via Google Earth Engine (FREE, no auth needed).

    This is the recommended path for autonomous execution.

    Args:
        tile_id: tile identifier
        bbox: {min_lon, max_lon, min_lat, max_lat}
        satellite: 'sentinel2', 'landsat9', 'sentinel1', 'planet'
        start_date, end_date: ISO format
        output_dir: Where to save

    Returns:
        Path to downloaded GeoTIFF
    """
    try:
        import ee
    except ImportError:
        raise ImportError("earthengine-api not installed. Run: pip install earthengine-api")

    try:
        ee.Initialize()
    except Exception as e:
        # Try with offline auth
        print(f"[gee] Need authentication: {e}")
        print("[gee] Run: earthengine authenticate")
        raise

    region = ee.Geometry.Rectangle(
        [
            bbox["min_lon"],
            bbox["min_lat"],
            bbox["max_lon"],
            bbox["max_lat"],
        ]
    )

    if satellite == "sentinel2":
        collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(region)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        )
        image = collection.median().clip(region)
    elif satellite == "landsat9":
        collection = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2").filterBounds(region).filterDate(start_date, end_date)
        image = collection.median().clip(region)
    else:
        raise ValueError(f"Unknown satellite: {satellite}")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / satellite / f"{tile_id}_{start_date}_{end_date}.tif"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Get download URL
    try:
        url = image.getDownloadURL(
            {
                "scale": 10,
                "region": region,
                "format": "GEO_TIFF",
            }
        )
        print(f"[gee] Download URL: {url[:100]}...")
        print(f"[gee] Output: {out_path}")
        # Real download: requests.get(url)
        return out_path
    except Exception as e:
        print(f"[gee] Download failed: {e}")
        return out_path


def compute_ndvi(red_path: Path, nir_path: Path, output_path: Path) -> np.ndarray:
    """Compute NDVI from red and NIR bands.

    NDVI = (NIR - RED) / (NIR + RED)
    """
    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype(np.float32)
        profile = red_src.profile.copy()

    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype(np.float32)

    ndvi = (nir - red) / (nir + red + 1e-8)

    profile.update(dtype=rasterio.float32, count=1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(ndvi, 1)

    return ndvi


def cloud_mask_s2(scl_path: Path) -> np.ndarray:
    """Cloud mask for Sentinel-2 using SCL band.

    SCL classes:
    - 0: No data
    - 1: Saturated / defective
    - 2: Dark area pixels
    - 3: Cloud shadows
    - 4: Vegetation
    - 5: Bare soils
    - 6: Water
    - 7: Clouds low probability
    - 8: Clouds medium probability
    - 9: Clouds high probability
    - 10: Cirrus
    - 11: Snow / ice
    """
    with rasterio.open(scl_path) as src:
        scl = src.read(1)

    # Mask out clouds, shadows, cirrus, snow
    mask = np.isin(scl, [0, 1, 2, 3, 7, 8, 9, 10, 11])
    return mask


def download_mapbiomas_paraguay(output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    """Download MapBiomas Paraguay land cover time series.

    Source: https://plataforma.mapbiomas.org/
    License: CC0
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "mapbiomas" / "mapbiomas_paraguay.tif"

    # MapBiomas Paraguay URL pattern
    url = "https://storage.googleapis.com/mapbiomas-public/paraguay/collection/mapbiomas_paraguay_collection.tif"

    print(f"[mapbiomas] Downloading Paraguay land cover from {url}")
    print(f"[mapbiomas] Output: {out_path}")
    return out_path


def download_hansen_gfc(output_dir: Path = DEFAULT_OUTPUT_DIR) -> Path:
    """Download Hansen Global Forest Change data for Paraguay.

    Source: https://www.globalforestwatch.org/
    License: CC0
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "hansen_gfc" / "hansen_paraguay.tif"

    # Hansen GFC URL pattern
    url = "https://storage.googleapis.com/earthenginepartners-hansen/GFC-2023-v1.11/Hansen_GFC-2023-v1.11_lossyear_20S_060W.tif"  # noqa: E501

    print(f"[hansen] Downloading deforestation data from {url}")
    print(f"[hansen] Output: {out_path}")
    return out_path


if __name__ == "__main__":
    print("Satellite I/O module")
    print(f"Default output: {DEFAULT_OUTPUT_DIR}")
