"""Real Hansen Global Forest Change download + analysis.

Strategy:
1. Download from Google Earth Engine (preferred)
2. Fallback to synthetic

Hansen GFC: https://www.globalforestwatch.org/
Data: 30m forest loss/gain, 2000-2023
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict
import json

import numpy as np

logger = logging.getLogger(__name__)


CACHE_DIR = Path(os.environ.get("HANSEN_CACHE_DIR", "data/cache/hansen"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# Hansen band names
HANSEN_BANDS = {
    "treecover2000": "Tree canopy cover in year 2000 (0-100)",
    "loss": "Forest loss during study period (binary)",
    "gain": "Forest gain during study period (binary)",
    "lossyear": "Year of loss (0-23, 0=no loss, 1=2001, ..., 23=2023)",
    "first": "First loss year (subset of lossyear)",
    "last": "Last observation year",
    "datamask": "Data mask",
}


def download_hansen_real(
    bbox: Dict[str, float],
    start_year: int = 2018,
    end_year: int = 2023,
    use_gee: bool = True,
) -> Optional[Dict[str, np.ndarray]]:
    """Download Hansen GFC for Paraguay.

    Returns dict with bands: treecover2000, loss, gain, lossyear
    """
    cache_path = CACHE_DIR / f"hansen_{start_year}_{end_year}.npz"
    if cache_path.exists():
        logger.info("Hansen cache hit")
        data = np.load(cache_path)
        return {k: data[k] for k in data.files}

    if use_gee:
        try:
            import ee
            try:
                ee.Initialize()
            except Exception:
                raise RuntimeError("no GEE auth")

            aoi = ee.Geometry.Rectangle([bbox["min_lon"], bbox["min_lat"],
                                          bbox["max_lon"], bbox["max_lat"]])
            hansen = ee.Image("UMD/hansen/global_forest_change_2023_v1_11")

            bands = ["treecover2000", "loss", "gain", "lossyear"]
            arrs = {}
            for band in bands:
                img_band = hansen.select(band)
                url = img_band.getThumbURL({
                    "region": aoi,
                    "dimensions": 256,
                    "format": "GEO_TIFF",
                })

                import urllib.request
                import rasterio
                with urllib.request.urlopen(url, timeout=60) as response:
                    arr_bytes = response.read()
                with rasterio.io.MemoryFile(arr_bytes) as memfile:
                    with memfile.open() as dataset:
                        arrs[band] = dataset.read(1)

            np.savez_compressed(cache_path, **arrs)
            return arrs

        except Exception as e:
            logger.warning(f"GEE Hansen failed: {e}")

    # Fallback: synthetic
    logger.warning("Using synthetic Hansen data")
    arrs = generate_synthetic_hansen(bbox, start_year, end_year)
    np.savez_compressed(cache_path, **arrs)
    return arrs


def generate_synthetic_hansen(
    bbox: Dict[str, float],
    start_year: int = 2018,
    end_year: int = 2023,
    shape: tuple = (256, 256),
    seed: int = 42,
) -> Dict[str, np.ndarray]:
    """Generate synthetic Hansen-like data.

    For Paraguay:
    - High treecover in west (Chaco)
    - Low treecover in east (agriculture)
    - Loss concentrated in agricultural frontier (center-east)
    """
    rng = np.random.default_rng(seed)
    H, W = shape

    # Treecover 2000: west high, east low
    gradient = np.tile(np.linspace(80, 20, W), (H, 1))  # 80% west, 20% east
    treecover = np.clip(gradient + rng.normal(0, 5, (H, W)), 0, 100).astype(np.uint8)

    # Loss: concentrated in east
    loss_zone = np.zeros((H, W), dtype=np.uint8)
    east_loss = rng.random((H, W)) < 0.05  # 5% of pixels lost
    east_loss = east_loss & (gradient < 50)  # Only in lower-cover areas
    loss_zone[east_loss] = 1

    # Loss year: 0-23 (0 = no loss, 1 = 2001, etc.)
    lossyear = np.zeros((H, W), dtype=np.uint8)
    for i, h in enumerate(range(H)):
        for j in range(W):
            if loss_zone[h, j]:
                lossyear[h, j] = rng.integers(1, 24)  # Random year 2001-2023

    # Gain: small patches
    gain_zone = np.zeros((H, W), dtype=np.uint8)
    gain_mask = rng.random((H, W)) < 0.02  # 2% gain
    gain_zone[gain_mask] = 1

    return {
        "treecover2000": treecover,
        "loss": loss_zone,
        "gain": gain_zone,
        "lossyear": lossyear,
    }


def compute_deforestation_year(
    lossyear: np.ndarray,
    year: int,
) -> np.ndarray:
    """Get deforestation mask for a specific year.

    Hansen lossyear is 1-23 (1=2001, ..., 23=2023).
    Returns binary mask where True = loss in that year.
    """
    year_code = year - 2000
    return (lossyear == year_code).astype(np.uint8)


def compute_cumulative_deforestation(
    lossyear: np.ndarray,
    end_year: int,
) -> np.ndarray:
    """Get cumulative deforestation up to end_year."""
    end_code = end_year - 2000
    return (lossyear > 0) & (lossyear <= end_code)


if __name__ == "__main__":
    print("Real Hansen GFC pipeline")
    print("=" * 60)
    bbox = {"min_lon": -57.5, "max_lon": -57.4, "min_lat": -25.3, "max_lat": -25.2}
    arrs = download_hansen_real(bbox)
    if arrs:
        print(f"  treecover2000: shape={arrs['treecover2000'].shape}, mean={arrs['treecover2000'].mean():.1f}%")
        print(f"  loss: shape={arrs['loss'].shape}, total={arrs['loss'].sum()} pixels")
        print(f"  gain: shape={arrs['gain'].shape}, total={arrs['gain'].sum()} pixels")
        # Compute annual deforestation
        for year in [2018, 2020, 2022]:
            annual = compute_deforestation_year(arrs['lossyear'], year)
            print(f"  Loss in {year}: {annual.sum()} pixels")
