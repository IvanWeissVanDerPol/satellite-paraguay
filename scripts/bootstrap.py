"""Bootstrap script — runs at start of autonomous execution.

Steps:
1. Verify dependencies installed
2. Verify data directory exists
3. Verify GPU available (optional)
4. Verify network access
5. Initialize DVC for data versioning
6. Generate data catalog
"""

import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Verify Python 3.10+."""
    print("[bootstrap] Checking Python version...")
    if sys.version_info < (3, 10):
        print(f"  ERROR: Python 3.10+ required, got {sys.version}")
        sys.exit(1)
    print(f"  OK: Python {sys.version_info.major}.{sys.version_info.minor}")


def check_dependencies():
    """Verify key dependencies installed."""
    print("[bootstrap] Checking dependencies...")
    required = [
        "numpy",
        "pandas",
        "geopandas",
        "rasterio",
        "torch",
        "transformers",
        "sklearn",
    ]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
            print(f"  OK: {pkg}")
        except ImportError:
            missing.append(pkg)
            print(f"  MISSING: {pkg}")

    if missing:
        print(f"\n  Install missing: pip install {' '.join(missing)}")
        sys.exit(1)


def check_data():
    """Verify paraguay-geodata accessible."""
    print("[bootstrap] Checking data sources...")
    pg_dir = Path("/root/paraguay-geodata/exports/web/data")
    if not pg_dir.exists():
        print(f"  ERROR: {pg_dir} not found")
        print("  Need /root/paraguay-geodata/ for local Paraguay data")
        sys.exit(1)

    key_files = [
        "tile_index.json",
        "roads.geojson",
        "buildings_asuncion.geojson",
        "catastro_parcels_sample.geojson",
        "indigenous_territories.geojson",
        "climate_risk.geojson",
        "gbif_paraguay.geojson",
    ]
    for f in key_files:
        path = pg_dir / f
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"  OK: {f} ({size_mb:.1f} MB)")
        else:
            print(f"  MISSING: {f}")


def check_gpu():
    """Check GPU availability."""
    print("[bootstrap] Checking GPU...")
    try:
        import torch

        if torch.cuda.is_available():
            print(f"  OK: GPU available ({torch.cuda.get_device_name(0)})")
        else:
            print("  No GPU — will use CPU (slower)")
    except ImportError:
        print("  PyTorch not installed, skipping GPU check")


def check_network():
    """Check internet connectivity."""
    print("[bootstrap] Checking network...")
    try:
        import urllib.request

        urllib.request.urlopen("https://github.com", timeout=5)
        print("  OK: Network available")
    except Exception as e:
        print(f"  No network: {e}")


def init_dvc():
    """Initialize DVC for data versioning."""
    print("[bootstrap] Initializing DVC...")
    if not Path(".dvc").exists():
        try:
            subprocess.run(["dvc", "init"], check=False)
            print("  OK: DVC initialized")
        except FileNotFoundError:
            print("  dvc not installed, skipping")
    else:
        print("  DVC already initialized")


def setup_directories():
    """Create all required directories."""
    print("[bootstrap] Creating directories...")
    dirs = [
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
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"  OK: {d}/")


def main():
    print("=" * 60)
    print("SatelliteCV-Paraguay — Bootstrap")
    print("=" * 60)
    check_python_version()
    check_dependencies()
    check_data()
    check_gpu()
    check_network()
    setup_directories()
    init_dvc()
    print("\n" + "=" * 60)
    print("Bootstrap complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  make verify        — verify everything")
    print("  make data-catalog  — generate data catalog")
    print("  make run-paper-1   — run first paper")
    print("  make dashboard     — start dashboard")


if __name__ == "__main__":
    main()
