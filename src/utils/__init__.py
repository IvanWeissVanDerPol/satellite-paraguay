"""Utils module — reproducibility, MLflow tracking, helpers."""

from .reproducibility import (
    DEFAULT_SEED,
    capture_environment,
    get_git_branch,
    get_git_hash,
    get_python_version,
    get_system_info,
    set_seed,
    verify_reproducibility,
)

try:
    from .mlflow_tracking import (
        get_best_run,
        log_experiment,
        log_p0011_experiment,
        log_p0100_experiment,
        setup_mlflow,
    )

    _HAS_MLFLOW = True
except ImportError:
    _HAS_MLFLOW = False

__all__ = [
    "DEFAULT_SEED",
    "set_seed",
    "get_git_hash",
    "get_git_branch",
    "get_python_version",
    "get_system_info",
    "capture_environment",
    "verify_reproducibility",
]
if _HAS_MLFLOW:
    __all__ += [
        "setup_mlflow",
        "log_experiment",
        "get_best_run",
        "log_p0011_experiment",
        "log_p0100_experiment",
    ]
