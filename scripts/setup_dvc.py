"""DVC setup script — initialize data versioning.

Usage:
    python scripts/setup_dvc.py
"""
import subprocess
import os
from pathlib import Path


def main():
    repo_root = Path(__file__).parent.parent

    print("=" * 60)
    print("DVC Setup for SatelliteCV-Paraguay")
    print("=" * 60)

    # Initialize DVC if not already initialized
    if not (repo_root / ".dvc").exists():
        print("\n[1] Initializing DVC...")
        try:
            subprocess.run(["dvc", "init"], cwd=repo_root, check=False)
            print("  Done")
        except FileNotFoundError:
            print("  DVC not installed. Install with: pip install dvc")
            print("  Skipping DVC init (you can run 'dvc init' later)")
    else:
        print("\n[1] DVC already initialized")

    # Set up local remote (can be changed to S3 later)
    config_path = repo_root / ".dvc" / "config"
    if config_path.exists():
        config = config_path.read_text()
        if "storage-local" not in config:
            print("\n[2] Setting up local remote...")
            subprocess.run(
                ["dvc", "remote", "add", "-d", "storage-local", "/tmp/dvc-storage"],
                cwd=repo_root, check=False,
            )
            print("  Done")

    # Create data directories
    print("\n[3] Creating data directories...")
    data_dirs = [
        "data/raw/sentinel2",
        "data/raw/landsat9",
        "data/raw/planet",
        "data/raw/mapbiomas",
        "data/raw/hansen",
        "data/raw/openaq",
        "data/raw/firms",
        "data/raw/sentinel5p",
        "data/raw/verra",
        "data/cache/sentinel2",
        "data/cache/embeddings",
        "data/cache/models",
        "data/external",
        "data/processed",
        "models/checkpoints",
        "models/fine_tuned",
    ]
    for d in data_dirs:
        (repo_root / d).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {d}")

    # Create DVC pipeline file
    print("\n[4] Creating DVC pipeline...")
    dvc_yaml = repo_root / "dvc.yaml"
    if not dvc_yaml.exists():
        dvc_yaml.write_text("""stages:
  download_sentinel:
    cmd: python scripts/download_sentinel_sample.py
    deps:
      - scripts/download_sentinel_sample.py
      - src/satellite_io/real_download.py
    outs:
      - data/raw/sentinel2/

  train_baselines_p0011:
    cmd: python scripts/train_prithvi_yvutu.py --epochs 2 --max-tiles 5
    deps:
      - scripts/train_prithvi_yvutu.py
      - src/satellite_io/real_download.py
      - src/satellite_io/mapbiomas.py
      - src/satellite_io/hansen.py
    outs:
      - models/prithvi_yvutu/best.pt
    metrics:
      - outputs/metrics/p0011_metrics.json

  train_lstm_p0035:
    cmd: python scripts/train_lstm_tatakua.py --epochs 5
    deps:
      - scripts/train_lstm_tatakua.py
      - src/external/openaq_client.py
      - src/external/sentinel5p_client.py
    outs:
      - models/lstm_tatakua/best.pt
    metrics:
      - outputs/metrics/p0035_metrics.json

  profile:
    cmd: python scripts/profile_performance.py
    deps:
      - scripts/profile_performance.py
    metrics:
      - outputs/performance_report.json
""")
        print(f"  ✓ dvc.yaml")

    # Set up gitignore for data
    gitignore = repo_root / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text()
        if "data/raw" not in content:
            with open(gitignore, "a") as f:
                f.write("""
# Data (tracked via DVC)
data/raw/
data/cache/
data/external/
data/processed/
models/checkpoints/
models/fine_tuned/
mlruns/
outputs/

# Credentials
.env
*.env
""")
            print(f"  ✓ Updated .gitignore")

    print("\n" + "=" * 60)
    print("DVC setup complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. dvc repro                # Run pipeline")
    print("  2. dvc dag                  # Show DAG")
    print("  3. dvc metrics show         # Show metrics")
    print("  4. git add .dvc dvc.yaml    # Commit DVC config")


if __name__ == "__main__":
    main()
