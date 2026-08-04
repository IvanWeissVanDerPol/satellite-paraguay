"""DVC (Data Version Control) setup for satellite-paraguay.

This script:
1. Initializes DVC in the repo
2. Tracks large data files (Hansen, Sentinel-2, MapBiomas)
3. Sets up remote storage (local filesystem by default)
4. Creates .dvcignore for transient files
5. Stages initial data versions

Run: python3 scripts/setup_dvc.py
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def run(cmd, check=True, capture=True):
    """Run shell command and return result."""
    print(f"  $ {cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=REPO_ROOT,
        capture_output=capture,
        text=True,
    )
    if check and result.returncode != 0:
        print(f"  ❌ Command failed: {result.stderr}")
    return result


def init_dvc():
    """Initialize DVC if not already done."""
    dvc_dir = REPO_ROOT / ".dvc"
    if dvc_dir.exists():
        print(f"  ✓ DVC already initialized")
        return
    result = run("dvc init --no-scm", check=False)
    if result.returncode == 0:
        print(f"  ✓ DVC initialized")
    else:
        print(f"  ⚠ DVC init failed (may not be installed)")


def setup_dvcignore():
    """Create .dvcignore for transient files."""
    dvcignore = REPO_ROOT / ".dvcignore"
    content = """# DVC ignore patterns
logs/
*.log
*.pyc
__pycache__/
.pytest_cache/
htmlcov/
.coverage
.mypy_cache/
.pyright/
outputs/weekly/*.log
"""
    dvcignore.write_text(content)
    print(f"  ✓ .dvcignore created")


def track_data():
    """Track large data files with DVC."""
    data_files = [
        "data/hansen/hansen_lossyear_20S_060W.tif",
        "data/hansen/hansen_treecover2000_20S_060W.tif",
        "data/mapbiomas/mapbiomas_paraguay_2023.tif",
    ]
    for f in data_files:
        full = REPO_ROOT / f
        if not full.exists():
            print(f"  ⊘ Skip (not found): {f}")
            continue
        dvc_file = full.with_suffix(full.suffix + ".dvc")
        if dvc_file.exists():
            print(f"  ✓ Already tracked: {f}")
            continue
        result = run(f"dvc add {f}", check=False)
        if result.returncode == 0:
            print(f"  ✓ Tracked: {f}")
        else:
            print(f"  ⚠ Failed to track {f}")


def setup_remote():
    """Set up local remote storage."""
    remote_path = REPO_ROOT / "data/dvc_remote"
    remote_path.mkdir(parents=True, exist_ok=True)
    run(f"dvc remote add -d local {remote_path}", check=False)
    run(f"dvc remote modify local type local", check=False)
    print(f"  ✓ Local remote: {remote_path}")


def create_pipeline():
    """Create DVC pipeline definition."""
    dvc_yaml = REPO_ROOT / "dvc.yaml"
    if dvc_yaml.exists():
        print(f"  ✓ dvc.yaml already exists")
        return

    content = """# DVC pipeline for satellite-paraguay
#
# Stages:
#   download: Acquire raw data
#   preprocess: Tile, mask, normalize
#   train: Train model
#   evaluate: Compute metrics
#   report: Generate visualizations and reports

stages:
  download:
    desc: Download raw satellite data
    cmd: python3 scripts/download_all_data.py
    deps:
      - scripts/download_all_data.py
    outs:
      - data/hansen/
      - data/sentinel2/
      - data/mapbiomas/

  preprocess:
    desc: Preprocess raw data into ML-ready format
    cmd: python3 scripts/paraguay_deforestation_analysis.py
    deps:
      - scripts/paraguay_deforestation_analysis.py
      - data/hansen/
    outs:
      - outputs/p0011/real_paraguay_analysis.json

  analyze_departments:
    desc: Department-level deforestation analysis
    cmd: python3 scripts/department_deforestation.py
    deps:
      - scripts/department_deforestation.py
      - data/hansen/
      - data/boundaries/
    outs:
      - outputs/p0011/departments/

  analyze_indigenous:
    desc: Indigenous territory overlap analysis
    cmd: python3 scripts/indigenous_overlap_analysis.py
    deps:
      - scripts/indigenous_overlap_analysis.py
      - data/hansen/
      - data/boundaries/
    outs:
      - outputs/p0011/indigenous/

  carbon:
    desc: Per-pixel carbon estimation
    cmd: python3 scripts/per_pixel_carbon.py
    deps:
      - scripts/per_pixel_carbon.py
      - data/hansen/
    outs:
      - outputs/p0011/carbon/

  uncertainty:
    desc: Uncertainty quantification with bootstrap
    cmd: python3 scripts/uncertainty_quantification.py
    deps:
      - scripts/uncertainty_quantification.py
      - data/hansen/
    outs:
      - outputs/p0011/uncertainty/

  verra_verify:
    desc: Verra carbon credit integrity verification
    cmd: python3 scripts/carbon_credit_verifier.py
    deps:
      - scripts/carbon_credit_verifier.py
      - data/hansen/
    outs:
      - outputs/carbon_credits/

  stats:
    desc: Statistical significance tests
    cmd: python3 scripts/statistical_tests.py
    deps:
      - scripts/statistical_tests.py
      - data/hansen/
    outs:
      - outputs/statistical_tests/

  report:
    desc: Generate final report and visualizations
    cmd: python3 scripts/generate_report.py
    deps:
      - outputs/p0011/
      - outputs/carbon_credits/
      - outputs/statistical_tests/
    outs:
      - docs/FINAL_REPORT.md
"""
    dvc_yaml.write_text(content)
    print(f"  ✓ dvc.yaml created with 9 stages")


def main():
    print("=" * 70)
    print("DVC SETUP")
    print("=" * 70)

    print("\n[1/5] Checking DVC installation...")
    result = run("dvc --version", check=False)
    if result.returncode != 0:
        print(f"  ⚠ DVC not installed. Install with: pip install dvc")
        print(f"  Creating config files anyway for future use.")
    else:
        print(f"  ✓ DVC version: {result.stdout.strip()}")

    print("\n[2/5] Initializing DVC...")
    init_dvc()

    print("\n[3/5] Setting up .dvcignore...")
    setup_dvcignore()

    print("\n[4/5] Creating pipeline definition...")
    create_pipeline()

    print("\n[5/5] Setting up remote storage...")
    setup_remote()

    print("\n  Setup complete. Workflow:")
    print("    dvc repro         # Run the full pipeline")
    print("    dvc dag           # Show pipeline DAG")
    print("    dvc metrics       # Show metrics")
    print("    dvc push          # Push to remote storage")


if __name__ == "__main__":
    main()
