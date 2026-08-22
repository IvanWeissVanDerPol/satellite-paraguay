"""INBIO data downloader for P0025 Yrupe.

Downloads Paraguayan agricultural yield trial data from INBIO (Instituto
de Biotecnología Agrícola) — for paper P0025.

PREREQUISITE: Requires INBIO partnership agreement on file at
docs/partnerships/INBIO-*.md before this script will fetch real data.

Without partnership, this script:
- Creates the output directory
- Writes a stub data file (synthetic labels)
- Logs a warning that partnership is needed
- Exits with code 0 (not an error — synthetic data is fine for pipeline testing)

With partnership:
- Authenticates against INBIO API (token from INBIO_API_KEY env var)
- Fetches the 10 most recent yield trials
- Downloads genotype + phenotype data per trial
- Stores in data/raw/inbio/yrupe_2024.csv

Usage:
    # Stub mode (no partnership):
    python3 scripts/download_inbio_yrupe.py

    # Real data mode (after partnership signed):
    INBIO_API_KEY=xyz python3 scripts/download_inbio_yrupe.py --real

Output:
    data/raw/inbio/yrupe_2024.csv
"""

import argparse
import csv
import json
import os
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def write_stub_data(output_path: Path):
    """Generate synthetic yield data for pipeline testing (no partnership)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    random.seed(42)  # reproducibility

    with output_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "trial_id",
            "year",
            "region",
            "variety",
            "yield_t_ha",
            "rainfall_mm",
            "soil_ph",
        ])
        # 10 synthetic trials
        for i in range(10):
            writer.writerow([
                f"INBIO-SYN-{i:03d}",
                2024,
                random.choice(["Alto Paraná", "Itapúa", "Caaguazú", "Alto Paraguay"]),
                random.choice(["BMX Potência", "CD 2710", "DM 53i54", "NS 6700"]),
                round(random.gauss(3.0, 0.5), 2),
                random.randint(800, 1500),
                round(random.uniform(4.5, 7.5), 1),
            ])

    print(f"  Wrote {output_path} (10 synthetic trials)")
    print()
    print("WARNING: Synthetic data written. Real INBIO data requires:")
    print("  1. Signed partnership agreement at docs/partnerships/INBIO-*.md")
    print("  2. INBIO_API_KEY in env vars")
    print("  3. Re-run with --real flag")
    print()
    print("See docs/partnerships/TEMPLATE-FPIC.md for partnership procedure.")


def fetch_real_data(output_path: Path, api_key: str):
    """Fetch real INBIO data via API (stub implementation)."""
    # TODO: implement actual API call when partnership signed
    raise NotImplementedError(
        "INBIO API client not yet implemented. "
        "Will be implemented after partnership signed."
    )


def main():
    parser = argparse.ArgumentParser(description="Download INBIO data for P0025 Yrupe")
    parser.add_argument("--real", action="store_true",
                        help="Fetch real data (requires partnership + INBIO_API_KEY)")
    parser.add_argument("--output", type=Path,
                        default=REPO_ROOT / "data" / "raw" / "inbio" / "yrupe_2024.csv")
    args = parser.parse_args()

    if args.real:
        api_key = os.environ.get("INBIO_API_KEY")
        if not api_key:
            print("ERROR: --real flag requires INBIO_API_KEY env var", file=sys.stderr)
            print("  Get one at https://www.inbio.org.py/api after partnership signed", file=sys.stderr)
            sys.exit(2)

        # Check partnership docs exist
        partnership_dir = REPO_ROOT / "docs" / "partnerships"
        inbio_docs = list(partnership_dir.glob("INBIO*.md")) if partnership_dir.exists() else []
        if not inbio_docs:
            print("ERROR: --real flag requires INBIO partnership doc at docs/partnerships/INBIO-*.md", file=sys.stderr)
            print("  See docs/partnerships/TEMPLATE-FPIC.md for procedure", file=sys.stderr)
            sys.exit(2)

        print(f"[INBIO] Real data mode")
        print(f"  Partnership doc: {inbio_docs[0]}")
        print(f"  API key: {api_key[:8]}...")
        fetch_real_data(args.output, api_key)
    else:
        print(f"[INBIO] Stub mode (no partnership yet)")
        write_stub_data(args.output)


if __name__ == "__main__":
    main()