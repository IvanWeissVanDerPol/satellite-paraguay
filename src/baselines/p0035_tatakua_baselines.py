"""Real baselines for P0035 Tatakua (air quality).

Baselines:
1. Mean forecast (climatology)
2. Linear regression on time
3. Persistence (last value)
"""

import numpy as np


def mean_forecast_baseline(historical: np.ndarray, horizon: int) -> np.ndarray:
    """Mean of historical period."""
    return np.full(horizon, np.mean(historical))


def persistence_forecast_baseline(historical: np.ndarray, horizon: int) -> np.ndarray:
    """Persistence — last value."""
    return np.full(horizon, historical[-1])


def linear_forecast_baseline(historical: np.ndarray, horizon: int) -> np.ndarray:
    """Linear trend extrapolation."""
    x = np.arange(len(historical))
    slope, intercept = np.polyfit(x, historical, 1)
    future_x = np.arange(len(historical), len(historical) + horizon)
    return slope * future_x + intercept


def run_all_baselines(historical: np.ndarray, horizon: int = 7) -> dict:
    """Run all baselines."""
    results = {}
    for name, fn in [
        ("mean", mean_forecast_baseline),
        ("persistence", persistence_forecast_baseline),
        ("linear_trend", linear_forecast_baseline),
    ]:
        forecast = fn(historical, horizon)
        results[name] = {
            "forecast": forecast,
            "mean": float(np.mean(forecast)),
        }
    return results


if __name__ == "__main__":
    # FAIL-LOUD (added 2026-08-11): no more np.random.rand() silent fallback.
    # Pass real PM2.5 hourly history as a .npy file via CLI; otherwise
    # raise FileNotFoundError so the user cannot accidentally benchmark
    # against random numbers.
    print("P0035 baselines demo (fail-loud mode)")
    print("Pass real PM2.5 history as a .npy file:")
    print("    python -m src.baselines.p0035_tatakua_baselines pm25_history.npy")
    import sys

    if len(sys.argv) >= 2:
        historical = np.load(sys.argv[1])
    else:
        raise FileNotFoundError(
            "P0035 baselines demo requires real PM2.5 history. "
            "Download from OpenAQ via src/external/openaq_client.py and save "
            "to data/cache/openaq/pm25_history.npy. "
            "Silent random-fill was removed 2026-08-11 — see BRUTAL_ROAST.md."
        )
    results = run_all_baselines(historical)
    for name, r in results.items():
        print(f"  {name}: mean forecast = {r['mean']:.2f} µg/m³")
