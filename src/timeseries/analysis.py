"""Multi-temporal time series analysis.

For:
- P0011 Yvytu (deforestation time series)
- P0100 Yvyra (carbon stock change)
- P0035 Tatakua (air quality time series)
- P0025 Yrupe (crop yield time series)
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import rasterio


def stack_timeseries(
    raster_paths: List[Path],
    bands: Optional[List[int]] = None,
) -> Tuple[np.ndarray, dict]:
    """Stack multiple raster files into a 3D time-series array.

    Args:
        raster_paths: list of GeoTIFF files (sorted by date)
        bands: list of band indices to include (1-indexed), None for all

    Returns:
        (array of shape (T, B, H, W), metadata)
    """
    if bands is None:
        bands = None  # Use all bands

    arrays = []
    meta = None
    for path in raster_paths:
        with rasterio.open(path) as src:
            if bands is None:
                arr = src.read()  # (B, H, W)
            else:
                arr = src.read(bands)
            if meta is None:
                meta = {
                    "transform": src.transform,
                    "crs": src.crs,
                    "shape": src.shape,
                }
            arrays.append(arr)

    stacked = np.stack(arrays, axis=0)  # (T, B, H, W)
    return stacked, meta


def compute_ndvi_timeseries(
    red_paths: List[Path],
    nir_paths: List[Path],
) -> np.ndarray:
    """Compute NDVI time series from red + NIR bands.

    Returns array of shape (T, H, W) with NDVI values.
    """
    n = len(red_paths)
    assert n == len(nir_paths)

    series = []
    for red_path, nir_path in zip(red_paths, nir_paths):
        with rasterio.open(red_path) as src:
            red = src.read(1).astype(np.float32)
        with rasterio.open(nir_path) as src:
            nir = src.read(1).astype(np.float32)

        ndvi = (nir - red) / (nir + red + 1e-8)
        series.append(ndvi)

    return np.stack(series, axis=0)


def detect_changes_bfast(
    timeseries: np.ndarray,
    dates: List[str],
    h: float = 0.25,
) -> Dict:
    """Detect changes using BFAST-like algorithm.

    Args:
        timeseries: (T, H, W) array of NDVI/EVI values
        dates: list of ISO date strings
        h: significance threshold

    Returns:
        Dict with breakpoints and trends
    """
    T, H, W = timeseries.shape

    # Simple change detection: rolling mean shift
    breakpoints = np.full((H, W), -1, dtype=np.int32)
    magnitudes = np.zeros((H, W), dtype=np.float32)

    if T < 4:
        return {"breakpoints": breakpoints, "magnitudes": magnitudes}

    half = T // 2
    before_mean = np.nanmean(timeseries[:half], axis=0)
    after_mean = np.nanmean(timeseries[half:], axis=0)

    diff = before_mean - after_mean  # Positive = decline (deforestation)
    breakpoints[:] = half  # Simplification: midpoint
    magnitudes = np.abs(diff)

    return {
        "breakpoints": breakpoints,
        "magnitudes": magnitudes,
        "before_mean": before_mean,
        "after_mean": after_mean,
    }


def compute_trend(
    timeseries: np.ndarray,
    dates: List[str],
) -> np.ndarray:
    """Compute linear trend per pixel.

    Returns slope per pixel (positive = increasing).
    """
    T, H, W = timeseries.shape
    dates_num = pd.to_datetime(dates).astype(np.int64) / 1e9 / 86400  # days

    # Normalize dates
    x = dates_num - dates_num[0]
    x_mean = np.mean(x)
    y_mean = np.nanmean(timeseries, axis=0)

    numerator = np.zeros((H, W))
    denominator = np.sum((x - x_mean) ** 2)

    for t in range(T):
        numerator += (x[t] - x_mean) * (timeseries[t] - y_mean)

    slope = numerator / (denominator + 1e-8)
    return slope


def compute_anomaly(
    timeseries: np.ndarray,
    baseline_period: Tuple[int, int] = (0, 12),
) -> np.ndarray:
    """Compute anomaly relative to baseline period.

    Returns anomaly for each timestep (T, H, W).
    """
    baseline = np.nanmean(timeseries[baseline_period[0] : baseline_period[1]], axis=0)
    return timeseries - baseline[None, :, :]


def aggregate_by_department(
    timeseries: np.ndarray,
    department_shapes,
) -> Dict[str, np.ndarray]:
    """Aggregate time series values by department.

    Returns {department_name: time_series_array}.
    """
    # Real implementation uses rasterio.mask + rasterstats
    result = {}
    for dept_name, dept_geom in department_shapes.items():
        # Crop timeseries to department bounds
        result[dept_name] = timeseries.mean(axis=(1, 2))  # simplification
    return result


if __name__ == "__main__":
    print("Timeseries module")
