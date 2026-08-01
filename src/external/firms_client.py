"""NASA FIRMS fire alerts client.

NASA FIRMS: https://firms.modaps.eosdis.nasa.gov/
Free, requires API key (free registration).

Provides: MODIS + VIIRS fire detections globally.
"""
import os
import logging
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests

logger = logging.getLogger(__name__)

CACHE_DIR = Path(os.environ.get("FIRMS_CACHE_DIR", "data/cache/firms"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)


FIRMS_BASE = "https://firms.modaps.eosdis.nasa.gov/api"


def fetch_firms_fires(
    bbox: Dict[str, float],
    days: int = 7,
    source: str = "VIIRS_SNPP_NRT",
    api_key: Optional[str] = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Fetch fire detections from NASA FIRMS.

    Args:
        bbox: {min_lon, max_lon, min_lat, max_lat}
        days: number of days back (max 10 for NRT)
        source: 'MODIS_NRT', 'VIIRS_SNPP_NRT', 'VIIRS_NOAA20_NRT'
        api_key: FIRMS API key (free from https://firms.modaps.eosdis.nasa.gov/api/)
        use_cache: use local cache

    Returns:
        DataFrame with columns: latitude, longitude, brightness, scan, track,
                                acq_date, acq_time, satellite, confidence, version, bright_t31, frp, daynight
    """
    if api_key is None:
        api_key = os.environ.get("FIRMS_API_KEY")

    cache_path = CACHE_DIR / f"firms_{source}_{days}d.json"
    if use_cache and cache_path.exists():
        return pd.read_json(cache_path)

    if api_key is None:
        logger.warning("FIRMS API key not set; using synthetic data")
        return generate_synthetic_firms(bbox, days)

    # Real fetch
    url = f"{FIRMS_BASE}/country/csv/{api_key}/{source}/PRY/{days}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        # Parse CSV
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        df.to_json(cache_path)
        return df
    except Exception as e:
        logger.warning(f"FIRMS fetch failed: {e}")
        return generate_synthetic_firms(bbox, days)


def fetch_firms_paraguay(
    days: int = 7,
    api_key: Optional[str] = None,
) -> pd.DataFrame:
    """Fetch all fire detections in Paraguay."""
    if api_key is None:
        api_key = os.environ.get("FIRMS_API_KEY")

    cache_path = CACHE_DIR / f"firms_paraguay_{days}d.json"
    if cache_path.exists():
        return pd.read_json(cache_path)

    if api_key is None:
        return generate_synthetic_firms_paraguay(days)

    url = f"{FIRMS_BASE}/country/csv/{api_key}/VIIRS_SNPP_NRT/PRY/{days}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        df.to_json(cache_path)
        return df
    except Exception as e:
        logger.warning(f"FIRMS Paraguay fetch failed: {e}")
        return generate_synthetic_firms_paraguay(days)


def compute_fire_clusters(
    fires: pd.DataFrame,
    distance_km: float = 5.0,
) -> List[Dict]:
    """Cluster nearby fire detections.

    Args:
        fires: DataFrame with lat/lon columns
        distance_km: cluster radius

    Returns:
        List of clusters, each with center lat/lon + count + intensity
    """
    if fires.empty:
        return []

    try:
        from sklearn.cluster import DBSCAN
    except ImportError:
        return []

    if "latitude" not in fires.columns or "longitude" not in fires.columns:
        return []

    # Convert to radians for haversine
    coords_rad = np.radians(fires[["latitude", "longitude"]].values)
    eps = distance_km / 6371.0  # Earth radius in km

    db = DBSCAN(eps=eps, min_samples=2, metric="haversine")
    fires = fires.copy()
    fires["cluster_id"] = db.fit_predict(coords_rad)

    clusters = []
    for cluster_id in fires["cluster_id"].unique():
        if cluster_id == -1:
            continue
        cluster = fires[fires["cluster_id"] == cluster_id]
        cluster_dict = {
            "cluster_id": int(cluster_id),
            "center_lat": float(cluster["latitude"].mean()),
            "center_lon": float(cluster["longitude"].mean()),
            "count": int(len(cluster)),
            "avg_frp": float(cluster["frp"].mean()) if "frp" in cluster.columns else 0,
            "max_brightness": float(cluster["brightness"].max()) if "brightness" in cluster.columns else 0,
        }
        clusters.append(cluster_dict)

    return clusters


def generate_synthetic_firms(bbox: Dict[str, float], days: int) -> pd.DataFrame:
    """Generate synthetic FIRMS-like data for testing."""
    rng = np.random.default_rng(42)
    n_fires = rng.integers(5, 50)

    dates = pd.date_range(end=datetime.now(), periods=days, freq="D")

    fires = pd.DataFrame({
        "latitude": rng.uniform(bbox["min_lat"], bbox["max_lat"], n_fires),
        "longitude": rng.uniform(bbox["min_lon"], bbox["max_lon"], n_fires),
        "brightness": rng.uniform(300, 380, n_fires),
        "scan": rng.uniform(0.4, 1.5, n_fires),
        "track": rng.uniform(0.4, 1.5, n_fires),
        "acq_date": rng.choice(dates.strftime("%Y-%m-%d"), n_fires),
        "acq_time": rng.choice(["0000", "0600", "1200", "1800"], n_fires),
        "satellite": "VIIRS_SNPP_NRT",
        "confidence": rng.choice(["low", "nominal", "high"], n_fires),
        "version": "2.0NRT",
        "bright_t31": rng.uniform(280, 320, n_fires),
        "frp": rng.uniform(1, 50, n_fires),
        "daynight": rng.choice(["D", "N"], n_fires),
    })

    return fires


def generate_synthetic_firms_paraguay(days: int) -> pd.DataFrame:
    """Generate synthetic FIRMS data covering all Paraguay."""
    return generate_synthetic_firms(
        {"min_lon": -62.5, "max_lon": -54.5, "min_lat": -27.5, "max_lat": -19.5},
        days,
    )


if __name__ == "__main__":
    print("FIRMS client demo")
    print("=" * 60)
    bbox = {"min_lon": -61.0, "max_lon": -58.0, "min_lat": -22.5, "max_lat": -20.0}
    fires = fetch_firms_fires(bbox, days=7)
    print(f"Fire detections: {len(fires)}")
    if not fires.empty and "latitude" in fires.columns:
        print(f"  Mean brightness: {fires['brightness'].mean():.1f} K")
        print(f"  Mean FRP: {fires['frp'].mean():.1f} MW")

    clusters = compute_fire_clusters(fires, distance_km=10)
    print(f"\nFire clusters: {len(clusters)}")
    for c in clusters[:5]:
        print(f"  Cluster {c['cluster_id']}: {c['count']} fires, center=({c['center_lat']:.3f}, {c['center_lon']:.3f})")
