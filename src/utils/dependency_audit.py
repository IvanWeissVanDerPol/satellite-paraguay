"""Dependency audit utilities.

Checks:
- All imports are declared in pyproject.toml
- Unused dependencies (heuristic)
- Missing dependencies (runtime error)
- Installed versions

Pure logic, no network. Returns structured audit results.
"""
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


# Common import name -> package name mapping
IMPORT_TO_PKG = {
    "PIL": "Pillow",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
    "cv2": "opencv-python",
    "huggingface_hub": "huggingface_hub",
    "transformers": "transformers",
    "torch": "torch",
    "fastapi": "fastapi",
    "streamlit": "streamlit",
    "plotly": "plotly",
    "folium": "folium",
    "rasterio": "rasterio",
    "geopandas": "geopandas",
    "shapely": "shapely",
    "requests": "requests",
    "pydantic": "pydantic",
    "hypothesis": "hypothesis",
    "pytest": "pytest",
    "pandas": "pandas",
    "numpy": "numpy",
    "scipy": "scipy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "dotenv": "python-dotenv",
}

# Always-excluded from "unused" check (planned but not yet integrated)
PLANNED_BUT_UNUSED = {
    "torch",
    "torchvision",
    "transformers",
    "huggingface_hub",
    "mlflow",
    "dvc",
}

# Common third-party imports to exclude from stdlib heuristics
TEST_FRAMEWORK_EXCLUDES = {
    "__future__",
    "antigravity",
    "this",
    "_pytest",
    "pytest",
    "site",
}


def get_declared_deps(pyproject_path: Path) -> List[str]:
    """Read declared dependencies from pyproject.toml."""
    if not pyproject_path.exists():
        return []
    content = pyproject_path.read_text()
    deps_match = re.search(
        r"dependencies\s*=\s*\[(.*?)\]",
        content,
        re.DOTALL,
    )
    if not deps_match:
        return []
    deps_text = deps_match.group(1)
    deps = re.findall(r'"([^"]+)"', deps_text)
    return [
        d.split(">=")[0].split("==")[0].split("[")[0].strip() for d in deps
    ]


def _find_imports_in_file(py_file: Path) -> Set[str]:
    """Find top-level module imports in a Python file."""
    try:
        content = py_file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return set()
    imports = set()
    for match in re.finditer(
        r"^\s*(?:from|import)\s+([\w.]+)", content, re.MULTILINE
    ):
        module = match.group(1).split(".")[0]
        imports.add(module)
    return imports


def find_used_imports(
    repo_root: Path,
    directories: List[str] = None,
) -> Set[str]:
    """Find all Python imports used in src/, scripts/, tests/."""
    if directories is None:
        directories = ["src", "scripts", "tests"]

    used: Set[str] = set()
    for dirname in directories:
        directory = repo_root / dirname
        if not directory.exists():
            continue
        for py_file in directory.rglob("*.py"):
            used |= _find_imports_in_file(py_file)

    stdlib = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else set()
    third_party = used - stdlib - TEST_FRAMEWORK_EXCLUDES
    return third_party


def map_imports_to_packages(used_imports: Set[str]) -> Set[str]:
    """Convert import names to package names using IMPORT_TO_PKG."""
    return {IMPORT_TO_PKG.get(name, name) for name in used_imports}


def audit_dependencies(
    repo_root: Path,
    declared: Optional[List[str]] = None,
    used: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """Run dependency audit and return structured result.

    Args:
        repo_root: path to repo root
        declared: optional pre-loaded declared deps (skips pyproject read)
        used: optional pre-loaded used imports (skips scan)
    """
    if declared is None:
        declared = get_declared_deps(repo_root / "pyproject.toml")
    if used is None:
        used = find_used_imports(repo_root)

    declared_set = set(declared)
    used_pkgs = map_imports_to_packages(used)

    missing = used_pkgs - declared_set
    unused = declared_set - used_pkgs - PLANNED_BUT_UNUSED

    return {
        "declared": sorted(declared_set),
        "used_imports": sorted(used),
        "used_packages": sorted(used_pkgs),
        "missing": sorted(missing),
        "unused": sorted(unused),
    }


def compute_health_score(missing: List[str], unused: List[str]) -> int:
    """Compute 0-100 dependency health score."""
    return max(0, 100 - 10 * len(missing) - 2 * len(unused))


def get_installed_versions(declared: List[str]) -> List[Dict[str, str]]:
    """Get installed versions of declared packages via pip."""
    try:
        result = subprocess.run(
            ["pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        packages = json.loads(result.stdout)
        declared_set = {d.lower().replace("-", "_") for d in declared}
        relevant = [
            p
            for p in packages
            if p["name"].lower().replace("-", "_") in declared_set
        ]
        return [{"name": p["name"], "version": p["version"]} for p in relevant]
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        return []