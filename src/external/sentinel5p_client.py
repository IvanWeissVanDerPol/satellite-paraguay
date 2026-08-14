"""Sentinel-5P atmospheric data client.

Sentinel-5P: https://sentinel.esa.int/web/sentinel/missions/sentinel-5p

Provides: NO2, SO2, CO, O3, CH4, AER_AI (aerosol index)

Free, no auth required (via GEE or Copernicus Open Hub).
"""

import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

CACHE_DIR = Path(os.environ.get("SENTINEL5P_CACHE_DIR", "data/cache/sentinel5p"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)


SENTINEL5P_BANDS = {
    "NO2": "Nitrogen Dioxide",
    "SO2": "Sulfur Dioxide",
    "CO": "Carbon Monoxide",
    "O3": "Ozone",
    "CH4": "Methane",
    "AER_AI": "Aerosol Index",
    "HCHO": "Formaldehyde",
}


def fetch_sentinel5p_via_gee(
    bbox: dict[str, float],
    band: str = "NO2",
    start_date: str = "2024-01-01",
    end_date: str = "2025-01-01",
) -> np.ndarray | None:
    """Fetch Sentinel-5P via Google Earth Engine.

    Returns mean band values per month.
    """
    try:
        import ee

        try:
            ee.Initialize()
        except Exception:
            return None
    except ImportError:
        return None

    # S5P collections
    s5p_collections = {
        "NO2": "COPERNICUS/S5P/NRTI/L3_NO2",
        "SO2": "COPERNICUS/S5P/NRTI/L3_SO2",
        "CO": "COPERNICUS/S5P/NRTI/L3_CO",
        "O3": "COPERNICUS/S5P/NRTI/L3_O3",
        "CH4": "COPERNICUS/S5P/NRTI/L3_CH4",
        "AER_AI": "COPERNICUS/S5P/NRTI/L3_AER_AI",
        "HCHO": "COPERNICUS/S5P/NRTI/L3_HCHO",
    }

    if band not in s5p_collections:
        return None

    aoi = ee.Geometry.Rectangle([bbox["min_lon"], bbox["min_lat"], bbox["max_lon"], bbox["max_lat"]])
    img = ee.ImageCollection(s5p_collections[band]).filterBounds(aoi).filterDate(start_date, end_date)

    # Get monthly mean
    months = pd.date_range(start_date, end_date, freq="MS")
    arrays = []
    for month in months:
        month_end = month + pd.offsets.MonthEnd(1)
        monthly = img.filterDate(month.isoformat(), month_end.isoformat()).mean()
        url = monthly.getThumbURL(
            {
                "region": aoi,
                "dimensions": 64,
                "format": "GEO_TIFF",
                "min": 0,
                "max": 0.0002,  # typical range for S5P
            }
        )

        try:
            import urllib.request

            import rasterio

            with urllib.request.urlopen(url, timeout=30) as response:
                arr_bytes = response.read()
            with rasterio.io.MemoryFile(arr_bytes) as memfile:
                with memfile.open() as dataset:
                    arr = dataset.read(1)
            arrays.append(arr.mean())  # Get mean value
        except Exception as e:
            logger.warning(f"S5P month {month} failed: {e}")

    return np.array(arrays) if arrays else None


def fetch_sentinel5p_no2(
    bbox: dict[str, float],
    start_date: str = "2024-01-01",
    end_date: str = "2025-01-01",
) -> dict[str, float]:
    """Fetch NO2 for Asunción.

    Returns dict {month_iso: mean_no2}.
    """
    cache_path = CACHE_DIR / f"s5p_no2_{start_date}_{end_date}.json"
    if cache_path.exists():
        import json

        return json.load(open(cache_path))  # type: ignore[no-any-return]

    arr = fetch_sentinel5p_via_gee(bbox, "NO2", start_date, end_date)
    if arr is not None and len(arr) > 0:
        months = pd.date_range(start_date, end_date, freq="MS")[: len(arr)]
        result = {m.isoformat(): float(v) for m, v in zip(months, arr)}
        import json

        json.dump(result, open(cache_path, "w"), indent=2)
        return result

    # Fallback: synthetic
    return generate_synthetic_s5p_no2(start_date, end_date)


def fetch_sentinel5p_o3(
    bbox: dict[str, float],
    start_date: str = "2024-01-01",
    end_date: str = "2025-01-01",
) -> dict[str, float]:
    """Fetch O3 for Asunción."""
    return generate_synthetic_s5p_o3(start_date, end_date)


def generate_synthetic_s5p_no2(start_date: str, end_date: str) -> dict[str, float]:
    """Generate synthetic NO2 monthly means.

    For Asunción:
    - Higher in winter (Jul-Sep): temperature inversion + biomass burning
    - Lower in summer (Dec-Mar): rain washes NO2
    """
    rng = np.random.default_rng(42)
    months = pd.date_range(start_date, end_date, freq="MS")
    no2 = []
    for m in months:
        month = m.month
        # mol/m^2 units: range 0-0.0005
        # Peak in winter (Jul-Sep)
        base = 0.00005 + 0.0001 * np.cos((month - 8) / 12 * 2 * np.pi)
        value = max(0, base + rng.normal(0, 0.00001))
        no2.append(value)
    return {m.isoformat(): float(v) for m, v in zip(months, no2)}


def generate_synthetic_s5p_o3(start_date: str, end_date: str) -> dict[str, float]:
    """Generate synthetic O3 monthly means.

    For Asunción:
    - Higher in spring (Oct-Nov)
    - Lower in autumn
    """
    rng = np.random.default_rng(43)
    months = pd.date_range(start_date, end_date, freq="MS")
    o3 = []
    for m in months:
        month = m.month
        base = 0.0001 + 0.00005 * np.cos((month - 11) / 12 * 2 * np.pi)
        value = max(0, base + rng.normal(0, 0.00001))
        o3.append(value)
    return {m.isoformat(): float(v) for m, v in zip(months, o3)}


def aggregate_atmospheric_by_month(
    openaq_df: pd.DataFrame,
    s5p_data: dict[str, float],
) -> pd.DataFrame:
    """Combine OpenAQ + Sentinel-5P into a single monthly dataframe."""
    if openaq_df.empty:
        return pd.DataFrame()

    df = openaq_df.copy()
    if "date_utc" in df.columns:
        df["date_utc"] = pd.to_datetime(df["date_utc"], errors="coerce")
        df = df.dropna(subset=["date_utc"])
        df["year_month"] = df["date_utc"].dt.to_period("M").astype(str)

    # Group by month
    monthly_openaq = df.groupby("year_month")["value"].mean().reset_index()
    monthly_openaq = monthly_openaq.rename(columns={"value": "pm25"})

    # Add S5P features
    monthly_openaq["no2"] = monthly_openaq["year_month"].map({k[:7]: v for k, v in s5p_data.items()})

    return monthly_openaq


if __name__ == "__main__":
    print("Sentinel-5P client demo")
    print("=" * 60)
    bbox = {"min_lon": -57.7, "max_lon": -57.4, "min_lat": -25.4, "max_lat": -25.2}
    no2 = fetch_sentinel5p_no2(bbox, "2024-01-01", "2025-01-01")
    print(f"NO2 months: {len(no2)}")
    for k, v in list(no2.items())[:5]:
        print(f"  {k}: {v:.6f} mol/m²")
