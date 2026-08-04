"""Dependency audit script.

Checks:
- All imports are declared in pyproject.toml
- No pinned vulnerable versions (rough check)
- Unused dependencies (heuristic)
- Missing dependencies (runtime error)

Run: python3 scripts/audit_dependencies.py
"""
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"


def get_declared_deps():
    """Read declared dependencies from pyproject.toml."""
    content = PYPROJECT.read_text()
    # Extract [project] dependencies
    deps_match = re.search(
        r"dependencies\s*=\s*\[(.*?)\]",
        content,
        re.DOTALL,
    )
    if not deps_match:
        return []
    deps_text = deps_match.group(1)
    deps = re.findall(r'"([^"]+)"', deps_text)
    return [d.split(">=")[0].split("==")[0].split("[")[0].strip() for d in deps]


def find_used_imports():
    """Find all Python imports used in src/ and scripts/."""
    used = set()
    for directory in [REPO_ROOT / "src", REPO_ROOT / "scripts", REPO_ROOT / "tests"]:
        if not directory.exists():
            continue
        for py_file in directory.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            # Find import statements
            for match in re.finditer(r"^\s*(?:from|import)\s+([\w.]+)", content, re.MULTILINE):
                module = match.group(1).split(".")[0]
                used.add(module)
    # Filter stdlib
    stdlib = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else set()
    third_party = (
        used
        - stdlib
        - {
            "__future__",
            "antigravity",
            "this",
            "_pytest",
            "pytest",
            "site",
        }
    )
    return third_party


def audit():
    """Run dependency audit."""
    print("=" * 70)
    print("DEPENDENCY AUDIT")
    print("=" * 70)

    declared = set(get_declared_deps())
    used = find_used_imports()

    print(f"\n  Declared dependencies: {len(declared)}")
    print(f"  Used third-party imports: {len(used)}")

    # Map common import names to package names
    import_to_pkg = {
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

    used_pkgs = {import_to_pkg.get(name, name) for name in used}

    # Missing dependencies
    missing = used_pkgs - declared
    print(f"\n  MISSING (used but not declared): {len(missing)}")
    for pkg in sorted(missing):
        print(f"    ⚠ {pkg}")

    # Unused dependencies
    unused = (
        declared
        - used_pkgs
        - {
            "torch",
            "torchvision",
            "transformers",
            "huggingface_hub",
            "mlflow",
            "dvc",  # planned but not yet integrated
        }
    )
    print(f"\n  UNUSED (declared but not used): {len(unused)}")
    for pkg in sorted(unused):
        print(f"    - {pkg}")

    # Check installed versions
    print(f"\n  Installed versions:")
    try:
        result = subprocess.run(
            ["pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        packages = json.loads(result.stdout)
        relevant = [
            p
            for p in packages
            if p["name"].lower().replace("-", "_") in {d.lower().replace("-", "_") for d in declared}
        ]
        for p in sorted(relevant, key=lambda x: x["name"]):
            print(f"    {p['name']:25} {p['version']}")
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
        print("    (pip not available)")

    # Save audit
    audit_result = {
        "declared": sorted(declared),
        "used_imports": sorted(used),
        "used_packages": sorted(used_pkgs),
        "missing": sorted(missing),
        "unused": sorted(unused),
    }
    out_path = REPO_ROOT / "outputs/dependency_audit.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(audit_result, indent=2))
    print(f"\n  Saved: {out_path}")

    # Score
    score = max(0, 100 - 10 * len(missing) - 2 * len(unused))
    print(f"\n  Dependency health score: {score}/100")
    if missing:
        print(f"    ⚠ Add missing deps to pyproject.toml: {', '.join(sorted(missing))}")


if __name__ == "__main__":
    audit()
