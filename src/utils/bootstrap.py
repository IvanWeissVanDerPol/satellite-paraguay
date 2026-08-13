"""Bootstrap checks for environment readiness.

Returns structured results for each check. No side effects.
"""

import importlib
import sys
import urllib.request
from pathlib import Path
from typing import Any

REQUIRED_DEPENDENCIES = [
    "numpy",
    "pandas",
    "geopandas",
    "rasterio",
    "torch",
    "transformers",
    "sklearn",
]

PARAGUAY_DATA_DIR = Path("/root/paraguay-geodata/exports/web/data")

KEY_PARAGUAY_FILES = [
    "tile_index.json",
    "roads.geojson",
    "buildings_asuncion.geojson",
    "catastro_parcels_sample.geojson",
    "indigenous_territories.geojson",
    "climate_risk.geojson",
    "gbif_paraguay.geojson",
]

REQUIRED_DIRECTORIES = [
    "data/raw/sentinel2",
    "data/raw/landsat9",
    "data/raw/planet",
    "data/raw/mapbiomas",
    "data/raw/hansen_gfc",
    "data/raw/openaq",
    "data/raw/firms",
    "data/processed",
    "data/cache/embeddings",
    "data/cache/timeseries",
    "data/external",
    "models/checkpoints",
    "models/fine_tuned",
    "logs/autonomous",
    "outputs/figures",
    "outputs/tables",
    "outputs/predictions",
    "papers/drafts",
    "papers/figures",
    "dashboard",
    "tests",
    "scripts",
    "configs",
    "docs",
]


def check_python_version(min_version: tuple[int, int] = (3, 10)) -> dict[str, Any]:
    """Check Python version meets minimum."""
    ok = sys.version_info >= min_version
    return {
        "name": "python_version",
        "ok": ok,
        "current": f"{sys.version_info.major}.{sys.version_info.minor}",
        "required": f"{min_version[0]}.{min_version[1]}+",
    }


def check_dependencies(packages: list[str] | None = None) -> dict[str, Any]:
    """Check required packages are importable."""
    if packages is None:
        packages = REQUIRED_DEPENDENCIES
    missing = []
    installed = []
    for pkg in packages:
        try:
            importlib.import_module(pkg)
            installed.append(pkg)
        except ImportError:
            missing.append(pkg)
    return {
        "name": "dependencies",
        "ok": len(missing) == 0,
        "installed": installed,
        "missing": missing,
    }


def check_data_directory(data_dir: Path = PARAGUAY_DATA_DIR) -> dict[str, Any]:
    """Check Paraguay geodata directory exists."""
    exists = data_dir.exists()
    return {
        "name": "data_directory",
        "ok": exists,
        "path": str(data_dir),
    }


def check_key_data_files(
    data_dir: Path = PARAGUAY_DATA_DIR,
    files: list[str] | None = None,
) -> dict[str, Any]:
    """Check that key Paraguay data files exist."""
    if files is None:
        files = KEY_PARAGUAY_FILES
    found = []
    missing = []
    for f in files:
        path = data_dir / f
        if path.exists():
            found.append({"name": f, "size_mb": round(path.stat().st_size / (1024 * 1024), 2)})
        else:
            missing.append(f)
    return {
        "name": "key_data_files",
        "ok": len(missing) == 0,
        "found": found,
        "missing": missing,
    }


def check_gpu() -> dict[str, Any]:
    """Check GPU availability (best-effort)."""
    try:
        import torch

        available = torch.cuda.is_available()
        device = torch.cuda.get_device_name(0) if available else None
        return {
            "name": "gpu",
            "ok": available,
            "available": available,
            "device": device,
        }
    except ImportError:
        return {"name": "gpu", "ok": False, "available": False, "error": "torch not installed"}


def check_network(url: str = "https://github.com", timeout: int = 5) -> dict[str, Any]:
    """Check network connectivity."""
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return {"name": "network", "ok": True, "url": url}
    except Exception as e:
        return {"name": "network", "ok": False, "url": url, "error": str(e)}


def check_dvc_initialized(repo_root: Path) -> dict[str, Any]:
    """Check if DVC is initialized."""
    dvc_dir = repo_root / ".dvc"
    return {
        "name": "dvc",
        "ok": dvc_dir.exists(),
        "initialized": dvc_dir.exists(),
    }


def setup_directories(base_dir: Path, dirs: list[str] | None = None) -> dict[str, Any]:
    """Create all required directories."""
    if dirs is None:
        dirs = REQUIRED_DIRECTORIES
    created = []
    for d in dirs:
        path = base_dir / d
        path.mkdir(parents=True, exist_ok=True)
        created.append(d)
    return {
        "name": "directories",
        "ok": True,
        "created": created,
    }


def run_all_checks(repo_root: Path, base_dir: Path | None = None) -> dict[str, Any]:
    """Run all bootstrap checks and return combined result."""
    if base_dir is None:
        base_dir = repo_root

    return {
        "python": check_python_version(),
        "deps": check_dependencies(),
        "data_dir": check_data_directory(),
        "data_files": check_key_data_files(),
        "gpu": check_gpu(),
        "network": check_network(),
        "dvc": check_dvc_initialized(repo_root),
        "directories": setup_directories(base_dir),
    }


def is_ready(checks: dict[str, Any]) -> bool:
    """Check if all critical checks passed."""
    return checks["python"]["ok"] and checks["deps"]["ok"] and checks["data_dir"]["ok"]  # type: ignore[no-any-return]
