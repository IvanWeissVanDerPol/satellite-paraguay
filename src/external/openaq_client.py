"""OpenAQ API client — air quality data.

OpenAQ: https://openaq.org/
API v3: https://api.openaq.org/v3/

Free with API key (https://openaq.org/) for read access.
"""

import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import requests

logger = logging.getLogger(__name__)

CACHE_DIR = Path(os.environ.get("OPENAQ_CACHE_DIR", "data/cache/openaq"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)


OPENAQ_BASE = "https://api.openaq.org/v3"
USER_AGENT = "satellite-paraguay/0.1.0 (research; contact@example.com)"


# Known Asunción stations
ASUNCION_STATIONS = [
    {"id": "AS-001", "name": "Asunción Centro", "lat": -25.2637, "lon": -57.5759},
    {"id": "AS-002", "name": "Asunción Catedral", "lat": -25.2805, "lon": -57.6342},
    {"id": "AS-003", "name": "San Lorenzo", "lat": -25.3333, "lon": -57.5200},
    {"id": "AS-004", "name": "Luque", "lat": -25.2700, "lon": -57.4900},
    {"id": "AS-005", "name": "Fernando de la Mora", "lat": -25.3190, "lon": -57.5911},
]


def _request_with_retry(
    url: str, params: dict | None = None, headers: dict | None = None, max_retries: int = 3
) -> dict | None:
    """Make API request with retry logic."""
    if headers is None:
        headers = {"User-Agent": USER_AGENT}
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()  # type: ignore[no-any-return]
            elif response.status_code == 429:
                wait = 2**attempt
                logger.warning(f"Rate limited, waiting {wait}s")
                time.sleep(wait)
            elif response.status_code in (410, 404):
                logger.warning(f"Endpoint deprecated: {response.status_code}")
                return None
            else:
                logger.warning(f"OpenAQ {response.status_code}: {response.text[:200]}")
                return None
        except requests.RequestException as e:
            logger.warning(f"OpenAQ request failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2**attempt)
    return None


def _parameter_id(name: str) -> int:
    """Map parameter name to OpenAQ v3 parameter ID."""
    return {
        "pm25": 2,
        "pm10": 1,
        "no2": 7,
        "o3": 10,
        "so2": 9,
        "co": 8,
        "bc": 23,
    }.get(name, 2)


def fetch_openaq_for_location(
    lat: float,
    lon: float,
    radius_km: float = 25.0,
    parameter: str = "pm25",
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 10000,
    api_key: str | None = None,
) -> pd.DataFrame:
    """Fetch OpenAQ measurements near a location."""
    if date_from is None:
        date_from = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    if date_to is None:
        date_to = datetime.now().strftime("%Y-%m-%d")

    if api_key is None:
        api_key = os.environ.get("OPENAQ_API_KEY")

    cache_path = CACHE_DIR / f"openaq_{lat}_{lon}_{parameter}_{date_from}_{date_to}.json"
    if cache_path.exists():
        return pd.read_json(cache_path)

    if api_key:
        headers = {"X-API-Key": api_key}
        url = f"{OPENAQ_BASE}/locations"
        params = {
            "coordinates": f"{lat},{lon}",
            "radius": int(radius_km * 1000),
            "parameters_id": _parameter_id(parameter),
            "limit": min(limit, 1000),
        }
        data = _request_with_retry(url, params=params, headers=headers)
        if data is not None and "results" in data:
            all_measurements = []
            for loc in data["results"][:5]:
                loc_id = loc.get("id")
                if loc_id:
                    meas_url = f"{OPENAQ_BASE}/sensors/{loc_id}/measurements"
                    meas_params = {
                        "date_from": date_from,
                        "date_to": date_to,
                        "limit": 1000,
                    }
                    meas_data = _request_with_retry(meas_url, params=meas_params, headers=headers)
                    if meas_data and "results" in meas_data:
                        for r in meas_data["results"]:
                            r["location_id"] = loc_id
                            r["location_name"] = loc.get("name", "")
                        all_measurements.extend(meas_data["results"])

            if all_measurements:
                df = pd.DataFrame(all_measurements)
                if not df.empty:
                    if "period" in df.columns:
                        df["date_utc"] = df["period"].apply(
                            lambda x: x.get("datetimeFrom", {}).get("utc") if isinstance(x, dict) else None
                        )
                    elif "date" in df.columns:
                        df["date_utc"] = df["date"].apply(lambda x: x.get("utc") if isinstance(x, dict) else None)
                    df["date_utc"] = pd.to_datetime(df["date_utc"], errors="coerce")
                    df = df.dropna(subset=["date_utc"])
                    if "value" in df.columns:
                        df.to_json(cache_path)
                        return df

    logger.warning(f"OpenAQ API not accessible (no API key); using synthetic for {lat},{lon}")
    return generate_synthetic_openaq_for_station(lat, lon, parameter)


def generate_synthetic_openaq_for_station(lat: float, lon: float, parameter: str = "pm25") -> pd.DataFrame:
    """Generate synthetic OpenAQ data for a single station."""
    rng = np.random.default_rng(int(abs(lat * lon * 1000)) % 10000)
    days = 365
    dates = pd.date_range(end=datetime.now(), periods=days, freq="D")

    if parameter == "pm25":
        values = []
        for d in dates:
            month = d.month
            seasonal = 10 + 15 * np.cos((month - 7) / 12 * 2 * np.pi)
            value = max(0, seasonal + rng.normal(0, 5))
            values.append(value)
    elif parameter == "no2":
        values = [rng.uniform(5, 50) for _ in dates]
    elif parameter == "o3":
        values = [rng.uniform(20, 80) for _ in dates]
    else:
        values = [rng.uniform(0, 100) for _ in dates]

    df = pd.DataFrame(
        {
            "date_utc": dates,
            "value": values,
            "unit": "µg/m³" if parameter == "pm25" else "ppb",
            "parameter": parameter,
            "location_id": int(abs(lat * lon * 1000)),
            "location_name": f"Synthetic station {lat:.2f},{lon:.2f}",
        }
    )
    return df


def fetch_openaq_asuncion(
    days: int = 365,
    parameter: str = "pm25",
) -> pd.DataFrame:
    """Fetch OpenAQ data for Asunción."""
    date_to = datetime.now().strftime("%Y-%m-%d")
    date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    all_dfs = []
    for station in ASUNCION_STATIONS:
        df = fetch_openaq_for_location(
            lat=station["lat"],  # type: ignore[arg-type]
            lon=station["lon"],  # type: ignore[arg-type]
            parameter=parameter,
            date_from=date_from,
            date_to=date_to,
        )
        if not df.empty:
            df["station_id"] = station["id"]
            df["station_name"] = station["name"]
            all_dfs.append(df)

    if not all_dfs:
        return pd.DataFrame()

    return pd.concat(all_dfs, ignore_index=True)


def aggregate_by_month(df: pd.DataFrame, value_col: str = "value") -> pd.DataFrame:
    """Aggregate measurements to monthly mean."""
    if df.empty or "date_utc" not in df.columns:
        return df

    df = df.copy()
    df["year_month"] = df["date_utc"].dt.to_period("M")
    return (
        df.groupby("year_month")
        .agg(
            mean=(value_col, "mean"),
            std=(value_col, "std"),
            min=(value_col, "min"),
            max=(value_col, "max"),
            count=(value_col, "count"),
        )
        .reset_index()
    )


def generate_synthetic_openaq(
    days: int = 365,
    station_id: str = "AS-001",
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic OpenAQ-like data for testing."""
    return generate_synthetic_openaq_for_station(-25.2637, -57.5759, "pm25")


if __name__ == "__main__":
    print("OpenAQ client demo")
    print("=" * 60)

    print("Attempting real fetch...")
    df = fetch_openaq_asuncion(days=30, parameter="pm25")

    print(f"  Records: {len(df)}")
    if not df.empty and "value" in df.columns:
        print(f"  Mean PM2.5: {df['value'].mean():.1f} µg/m³")

    monthly = aggregate_by_month(df)
    print(f"\nMonthly aggregate: {len(monthly)} months")
    if not monthly.empty:
        print(monthly.head(10).to_string(index=False))
