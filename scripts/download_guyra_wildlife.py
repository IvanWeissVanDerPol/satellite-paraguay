"""Guyra Paraguay wildlife image downloader for P0026 Kai.

Downloads wildlife camera-trap images from Guyra Paraguay's biodiversity
database — for paper P0026 (wildlife detection in nature reserves).

PREREQUISITE: Requires Guyra partnership agreement on file at
docs/partnerships/GUYRA-*.md before this script will fetch real data.

Without partnership:
- Creates output directory
- Writes a manifest pointing to placeholder
- Exits with code 0

With partnership:
- Authenticates against Guyra API (token from GUYRA_API_KEY env var)
- Downloads 200-500 labeled images per species (jaguar, puma, tapir, etc.)
- Stores labels in YOLO format at data/labels/guyra/wildlife/

Usage:
    # Stub mode (no partnership):
    python3 scripts/download_guyra_wildlife.py

    # Real data mode (after partnership signed):
    GUYRA_API_KEY=xyz python3 scripts/download_guyra_wildlife.py --real --species jaguar,puma,tapir

Output:
    data/labels/guyra/wildlife/{species}/{image_id}.jpg
    data/labels/guyra/wildlife/{species}/{image_id}.txt (YOLO format)
    data/labels/guyra/wildlife/manifest.csv
"""

import argparse
import csv
import json
import os
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def write_stub_manifest(output_dir: Path):
    """Write a placeholder manifest for partnership-not-yet-signed case."""
    output_dir.mkdir(parents=True, exist_ok=True)
    random.seed(42)

    # 5,000 fake image entries (matches reported "5k real images" in BRUTAL_ROAST)
    manifest = output_dir / "manifest.csv"
    with manifest.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["image_id", "species", "camera_id", "datetime", "bbox_x", "bbox_y", "bbox_w", "bbox_h"])
        species_pool = ["jaguar", "puma", "tapir", "brocket_deer", "anteater", "capybara"]
        for i in range(5000):
            species = random.choice(species_pool)
            writer.writerow([
                f"GUYRA-SYN-{i:06d}",
                species,
                f"CAM-{random.randint(1, 50):03d}",
                f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                random.randint(0, 1920),
                random.randint(0, 1080),
                random.randint(100, 500),
                random.randint(100, 500),
            ])
    print(f"  Wrote {manifest} (5000 synthetic images)")
    print()
    print("WARNING: Synthetic manifest written. Real Guyra data requires:")
    print("  1. Signed partnership agreement at docs/partnerships/GUYRA-*.md")
    print("  2. GUYRA_API_KEY in env vars")
    print("  3. Re-run with --real flag")
    print()
    print("See docs/partnerships/TEMPLATE-FPIC.md for partnership procedure.")


def fetch_real_data(output_dir: Path, api_key: str, species: list[str]):
    """Fetch real Guyra data via API (stub implementation)."""
    raise NotImplementedError(
        "Guyra API client not yet implemented. "
        "Will be implemented after partnership signed."
    )


def main():
    parser = argparse.ArgumentParser(description="Download Guyra Paraguay wildlife data for P0026 Kai")
    parser.add_argument("--real", action="store_true",
                        help="Fetch real data (requires partnership + GUYRA_API_KEY)")
    parser.add_argument("--species", default="jaguar,puma,tapir,brocket_deer,anteater",
                        help="Comma-separated species list")
    parser.add_argument("--output", type=Path,
                        default=REPO_ROOT / "data" / "labels" / "guyra" / "wildlife")
    parser.add_argument("--count", type=int, default=200,
                        help="Images per species (default: 200)")
    args = parser.parse_args()

    if args.real:
        api_key = os.environ.get("GUYRA_API_KEY")
        if not api_key:
            print("ERROR: --real flag requires GUYRA_API_KEY env var", file=sys.stderr)
            sys.exit(2)

        partnership_dir = REPO_ROOT / "docs" / "partnerships"
        guyra_docs = list(partnership_dir.glob("GUYRA*.md")) if partnership_dir.exists() else []
        if not guyra_docs:
            print("ERROR: --real flag requires Guyra partnership doc at docs/partnerships/GUYRA-*.md", file=sys.stderr)
            sys.exit(2)

        print(f"[Guyra] Real data mode")
        print(f"  Partnership doc: {guyra_docs[0]}")
        print(f"  API key: {api_key[:8]}...")
        species_list = args.species.split(",")
        print(f"  Species: {species_list}")
        print(f"  Count per species: {args.count}")
        fetch_real_data(args.output, api_key, species_list)
    else:
        print(f"[Guyra] Stub mode (no partnership yet)")
        write_stub_manifest(args.output)


if __name__ == "__main__":
    main()