"""Real baselines for P0035 Tatakua (air quality).

Baselines:
1. Mean forecast (climatology)
2. Linear regression on time
3. Persistence (last value)
"""
import numpy as np

from src.evaluation import regression_metrics


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
    np.random.seed(42)
    historical = np.random.rand(30) * 25 + 5
    results = run_all_baselines(historical)
    for name, r in results.items():
        print(f"  {name}: mean forecast = {r['mean']:.2f} µg/m³")
