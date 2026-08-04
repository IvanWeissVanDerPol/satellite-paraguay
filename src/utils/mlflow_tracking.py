"""Experiment tracking utilities using MLflow.

Provides a unified interface for logging experiments across all 6 papers.
"""
from pathlib import Path
from typing import Optional, Dict, Any
import os


def setup_mlflow(
    tracking_uri: Optional[str] = None,
    experiment_name: str = "satellite-paraguay",
) -> "mlflow.tracking.MlflowClient":
    """Set up MLflow tracking.

    Args:
        tracking_uri: MLflow tracking URI (default: local file)
        experiment_name: experiment name

    Returns:
        MlflowClient instance
    """
    try:
        import mlflow
        from mlflow.tracking import MlflowClient
    except ImportError:
        raise ImportError("mlflow not installed. Run: pip install mlflow")

    if tracking_uri is None:
        # Default: local file in ./mlruns, but allow override via env var
        # for testability. MLFLOW_TRACKING_URI follows mlflow's own convention.
        env_uri = os.environ.get("MLFLOW_TRACKING_URI")
        if env_uri:
            tracking_uri = env_uri
        else:
            mlflow_dir = Path("mlruns")
            mlflow_dir.mkdir(exist_ok=True)
            tracking_uri = f"file://{mlflow_dir.absolute()}"

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    return MlflowClient()


def log_experiment(
    run_name: str,
    params: Dict[str, Any],
    metrics: Dict[str, float],
    artifacts: Optional[Dict[str, str]] = None,
    tags: Optional[Dict[str, str]] = None,
    tracking_uri: Optional[str] = None,
) -> str:
    """Log an experiment to MLflow.

    Args:
        run_name: name of the run
        params: hyperparameters (e.g. lr, batch_size)
        metrics: evaluation metrics (e.g. f1, accuracy)
        artifacts: {local_path: artifact_name}
        tags: {tag_key: tag_value}
        tracking_uri: MLflow tracking URI

    Returns:
        run_id
    """
    try:
        import mlflow
    except ImportError:
        raise ImportError("mlflow not installed. Run: pip install mlflow")

    setup_mlflow(tracking_uri)

    with mlflow.start_run(run_name=run_name) as run:
        # Log params
        for k, v in params.items():
            mlflow.log_param(k, v)

        # Log metrics
        for k, v in metrics.items():
            mlflow.log_metric(k, v)

        # Log artifacts
        if artifacts:
            for local_path, artifact_name in artifacts.items():
                if Path(local_path).exists():
                    mlflow.log_artifact(local_path, artifact_name)

        # Log tags
        if tags:
            mlflow.set_tags(tags)

        return run.info.run_id


def get_best_run(
    metric_name: str,
    experiment_name: str = "satellite-paraguay",
    ascending: bool = False,
) -> Optional[Dict]:
    """Get best run by metric.

    Args:
        metric_name: name of the metric to sort by
        experiment_name: experiment to search
        ascending: sort ascending (True) or descending (False)
    """
    try:
        from mlflow.tracking import MlflowClient
    except ImportError:
        raise ImportError("mlflow not installed. Run: pip install mlflow")

    client = setup_mlflow()
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        return None

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        max_results=1000,
    )

    runs_with_metric = [r for r in runs if metric_name in r.data.metrics]
    if not runs_with_metric:
        return None

    return sorted(runs_with_metric, key=lambda r: r.data.metrics[metric_name], reverse=not ascending)[0]


# ============================================
# Example usage for each paper
# ============================================

def log_p0011_experiment(f1_macro, miou, params):
    """Log P0011 Yvutu experiment."""
    return log_experiment(
        run_name=f"yvytu_{params.get('model', 'unknown')}",
        params=params,
        metrics={
            "f1_macro": f1_macro,
            "miou": miou,
        },
        tags={
            "paper": "P0011",
            "advisor": "Cristaldo",
            "target_journal": "Remote Sensing of Environment",
        },
    )


def log_p0100_experiment(r2, rmse, mae, params):
    """Log P0100 Yvyra experiment."""
    return log_experiment(
        run_name=f"yvyra_{params.get('model', 'unknown')}",
        params=params,
        metrics={
            "r2": r2,
            "rmse": rmse,
            "mae": mae,
        },
        tags={
            "paper": "P0100",
            "advisor": "Cristaldo",
            "target_journal": "Nature Climate Change",
        },
    )


def log_p0025_experiment(r2, rmse, mae, params):
    """Log P0025 Yrupe experiment."""
    return log_experiment(
        run_name=f"yrupe_{params.get('model', 'unknown')}",
        params=params,
        metrics={
            "r2": r2,
            "rmse": rmse,
            "mae": mae,
        },
        tags={
            "paper": "P0025",
            "target_journal": "Computers and Electronics in Agriculture",
        },
    )


def log_p0026_experiment(map50, map50_95, epochs, params):
    """Log P0026 Kai experiment."""
    return log_experiment(
        run_name=f"kai_{params.get('model', 'unknown')}",
        params={**params, "epochs": epochs},
        metrics={
            "map50": map50,
            "map50_95": map50_95,
        },
        tags={
            "paper": "P0026",
            "target_journal": "Conservation Biology",
        },
    )


def log_p0035_experiment(val_mae, epochs, params):
    """Log P0035 Tatakua experiment."""
    return log_experiment(
        run_name=f"tatakua_{params.get('horizon', 'unknown')}d",
        params={**params, "epochs": epochs},
        metrics={
            "val_mae_ug_per_m3": val_mae,
        },
        tags={
            "paper": "P0035",
            "target_journal": "Atmospheric Environment",
        },
    )


if __name__ == "__main__":
    # Demo
    print("MLflow experiment tracking demo")

    # Setup
    setup_mlflow(experiment_name="satellite-paraguay-demo")

    # Log example runs
    import random
    for i in range(3):
        params = {"lr": 0.001, "batch_size": 32, "epochs": 50}
        metrics = {
            "f1_macro": random.uniform(0.7, 0.9),
            "miou": random.uniform(0.6, 0.8),
        }
        run_id = log_experiment(
            run_name=f"demo_run_{i}",
            params=params,
            metrics=metrics,
        )
        print(f"  Logged run {run_id}: F1={metrics['f1_macro']:.3f}")

    # Get best
    best = get_best_run("f1_macro")
    if best:
        print(f"\nBest run: F1={best.data.metrics['f1_macro']:.3f}")
