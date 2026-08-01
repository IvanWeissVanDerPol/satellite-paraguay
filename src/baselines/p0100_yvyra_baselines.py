"""Real baselines for P0100 Yvyra (carbon credits).

Baselines:
1. Linear regression
2. Random Forest
3. Persistence (mean of training set)
"""
from typing import Optional
import numpy as np

from src.evaluation import regression_metrics, print_metrics


def linear_regression_baseline(
    features: np.ndarray,
    target: np.ndarray,
) -> np.ndarray:
    """Linear regression baseline for carbon estimation.

    Args:
        features: (n_samples, n_features) — e.g. embeddings + climate
        target: (n_samples,) — carbon stock in tons

    Returns:
        (n_samples,) predictions
    """
    try:
        from sklearn.linear_model import Ridge
    except ImportError:
        raise ImportError("scikit-learn not installed")

    model = Ridge(alpha=1.0)
    model.fit(features, target)
    return model.predict(features)


def random_forest_regression_baseline(
    features: np.ndarray,
    target: np.ndarray,
    n_estimators: int = 100,
    random_state: int = 42,
) -> np.ndarray:
    """Random Forest regression baseline."""
    try:
        from sklearn.ensemble import RandomForestRegressor
    except ImportError:
        raise ImportError("scikit-learn not installed")

    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state, n_jobs=-1)
    model.fit(features, target)
    return model.predict(features)


def persistence_baseline(target: np.ndarray) -> np.ndarray:
    """Persistence baseline — predict mean of training set."""
    mean_value = np.mean(target)
    return np.full_like(target, mean_value)


def run_all_baselines(
    features: np.ndarray,
    target: np.ndarray,
) -> dict:
    """Run all baselines and return metrics."""
    results = {}

    # 1. Persistence
    print("Running persistence baseline...")
    preds = persistence_baseline(target)
    results["persistence"] = regression_metrics(target, preds)

    # 2. Linear regression
    print("Running linear regression baseline...")
    try:
        preds = linear_regression_baseline(features, target)
        results["linear_regression"] = regression_metrics(target, preds)
    except Exception as e:
        results["linear_regression"] = {"error": str(e)}

    # 3. Random Forest
    print("Running Random Forest baseline...")
    try:
        preds = random_forest_regression_baseline(features, target, n_estimators=50)
        results["random_forest"] = regression_metrics(target, preds)
    except Exception as e:
        results["random_forest"] = {"error": str(e)}

    return results


if __name__ == "__main__":
    print("P0100 baselines demo")
    np.random.seed(42)
    n_samples = 100
    n_features = 50
    features = np.random.randn(n_samples, n_features).astype(np.float32)
    target = features[:, 0] * 1000 + np.random.randn(n_samples) * 100  # carbon

    results = run_all_baselines(features, target)
    print_metrics(results)
