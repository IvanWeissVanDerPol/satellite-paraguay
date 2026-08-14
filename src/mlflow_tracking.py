"""MLflow experiment tracking for satellite-paraguay.

Tracks all analysis runs with parameters, metrics, and artifacts.

Usage:
    from src.mlflow_tracking import start_run, log_metrics, log_artifact

    with start_run("p0011_yvutu_v2"):
        log_params({"epochs": 30, "lr": 1e-4})
        log_metrics({"f1": 0.85, "precision": 0.85, "recall": 0.85})
        log_artifact("outputs/p0011/metrics.json")
"""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, ContextManager

REPO_ROOT = Path(__file__).resolve().parents[1]
MLRUNS_DIR = REPO_ROOT / "mlruns"

# Configure MLflow before importing
os.environ.setdefault("MLFLOW_TRACKING_URI", f"file:{MLRUNS_DIR}")


def _try_import_mlflow():
    try:
        import mlflow

        return mlflow
    except ImportError:
        return None


@contextmanager  # type: ignore[arg-type]
def start_run(  # type: ignore[misc]
    run_name: str,
    experiment_name: str = "satellite-paraguay",
    tags: dict[str, str] | None = None,
) -> ContextManager[Any]:
    """Start an MLflow run.

    Falls back to a no-op context if MLflow is not installed.
    """
    mlflow = _try_import_mlflow()
    if mlflow is None:
        # No-op fallback
        class _NoOpRun:
            def info(self):
                return None

        yield _NoOpRun()
        return

    MLRUNS_DIR.mkdir(exist_ok=True)
    mlflow.set_tracking_uri(f"file:{MLRUNS_DIR}")
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name, tags=tags or {}):
        yield mlflow.active_run()


def log_params(params: dict[str, Any]) -> None:
    """Log parameters to current MLflow run."""
    mlflow = _try_import_mlflow()
    if mlflow is None:
        return
    # MLflow requires values to be string/int/float
    clean = {}
    for k, v in params.items():
        if isinstance(v, (str, int, float, bool)):
            clean[k] = v
        else:
            clean[k] = str(v)
    mlflow.log_params(clean)


def log_metrics(metrics: dict[str, float], step: int | None = None) -> None:
    """Log metrics to current MLflow run."""
    mlflow = _try_import_mlflow()
    if mlflow is None:
        return
    clean = {k: float(v) for k, v in metrics.items()}
    mlflow.log_metrics(clean, step=step)


def log_artifact(local_path: str) -> None:
    """Log an artifact (file) to current MLflow run."""
    mlflow = _try_import_mlflow()
    if mlflow is None:
        return
    full = REPO_ROOT / local_path if not Path(local_path).is_absolute() else Path(local_path)
    if full.exists():
        mlflow.log_artifact(str(full))


def log_dict_as_json(data: dict[str, Any], filename: str) -> None:
    """Log a dict as a JSON artifact."""
    import json
    import tempfile

    mlflow = _try_import_mlflow()
    if mlflow is None:
        return
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f, indent=2, default=str)
        f.flush()
        temp_path = f.name
    try:
        # mlflow.log_artifact(local_path, artifact_path=None)
        # Place the file under the given filename in the artifact dir
        # by writing to a temp dir with the target filename.
        import os
        import shutil

        tmp_dir = tempfile.mkdtemp()
        target = os.path.join(tmp_dir, filename)
        shutil.move(temp_path, target)
        try:
            mlflow.log_artifact(target)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
    except Exception:
        Path(temp_path).unlink(missing_ok=True)


def end_run() -> None:
    """End current MLflow run."""
    mlflow = _try_import_mlflow()
    if mlflow is None:
        return
    mlflow.end_run()


def list_experiments() -> list:
    """List all experiments with their run counts."""
    mlflow = _try_import_mlflow()
    if mlflow is None:
        return []
    return [{"name": e.name, "experiment_id": e.experiment_id} for e in mlflow.search_experiments()]


def search_runs(experiment_name: str = "satellite-paraguay", max_results: int = 20) -> list:
    """Search recent runs in experiment."""
    mlflow = _try_import_mlflow()
    if mlflow is None:
        return []
    runs = mlflow.search_runs(
        experiment_names=[experiment_name],
        max_results=max_results,
        order_by=["start_time DESC"],
    )
    return runs.to_dict("records") if runs is not None else []
