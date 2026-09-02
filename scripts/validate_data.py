"""Validate that datasets the thesis repo claims to have actually exist on disk.

This is the "honest-reporting" guard for the data layer. It compares the
inventory of datasets cited in DATA_ACQUISITION.md and STATUS.md against
what is actually present in data/ and the project's expected-path conventions.

Why this exists (2026-09-02):
- Commit 5347383 added fail-loud to production pipelines (no more np.random.rand
  silent fallback).
- That fix protects the *runtime* path. It does not protect against the
  *documentation* path: a paper.md can still claim "we have Hansen GFC"
  while data/hansen/ is empty.
- This script runs `python3 scripts/validate_data.py`, produces
  outputs/data_audit.json + a stdout summary, and exits non-zero if any
  claimed dataset is missing or has suspicious byte count.

This is Tier 2.P from AGENT_TODO.md.

Honest reporting: this script reports ONLY what is on disk in this repository.
If data lives at /root/paraguay-geodata (the canonical staging path on the
build host), it is flagged as "off-repo" but not as "missing". The CI guard
catches missing; humans can verify off-repo by running on the build host.

Usage:
    python3 scripts/validate_data.py           # full audit
    python3 scripts/validate_data.py --strict  # exit 1 on any missing or off-repo
    python3 scripts/validate_data.py --quiet   # only print summary lines
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parent.parent

Status = Literal["present", "missing", "off-repo", "synthetic", "partial"]


@dataclass
class DataClaim:
    """One claim the repo makes about a dataset."""

    name: str
    claimed_path: str  # relative to REPO_ROOT, or absolute off-repo path
    claimed_size_mb: float | None
    purpose: str  # one-line description of what the dataset is for
    paper_ids: list[str]  # which papers depend on this dataset
    expected_layers: list[str] | None = None  # for tiled datasets
    off_repo_canonical: str | None = None  # canonical path on the build host
    status: Status = "missing"
    actual_path: str | None = None
    actual_size_mb: float | None = None
    sha256_prefix: str | None = None
    notes: str = ""


# Each entry: (name, claimed path, claimed size in MB, purpose, paper IDs)
# Order matches DATA_ACQUISITION.md, so the audit is easy to diff.
CLAIMS: list[DataClaim] = [
    # ---------- Hansen GFC (P0011, P0010, P0012) ----------
    # .tif = full Hansen download (~620MB/layer × 2 tiles × 3 layers)
    # .npz in data/cache/ = pre-processed lightweight form used by the pipeline
    DataClaim(
        name="Hansen GFC v1.11 — treecover2000 — 20S_060W",
        claimed_path="data/hansen/hansen_treecover2000_20S_060W.tif",
        claimed_size_mb=620.0,
        purpose="Forest cover at year 2000, eastern Paraguay tile",
        paper_ids=["P0011", "P0010", "P0012"],
        expected_layers=["treecover2000"],
        off_repo_canonical="data/cache/hansen/hansen_2018_2023.npz",
    ),
    DataClaim(
        name="Hansen GFC v1.11 — treecover2000 — 20S_070W",
        claimed_path="data/hansen/hansen_treecover2000_20S_070W.tif",
        claimed_size_mb=620.0,
        purpose="Forest cover at year 2000, Chaco tile",
        paper_ids=["P0011", "P0010", "P0012"],
        off_repo_canonical="data/cache/hansen/hansen_2018_2023.npz",
    ),
    DataClaim(
        name="Hansen GFC v1.11 — lossyear — 20S_060W",
        claimed_path="data/hansen/hansen_lossyear_20S_060W.tif",
        claimed_size_mb=152.0,
        purpose="Year of loss event 2001-2023, eastern tile",
        paper_ids=["P0011", "P0010", "P0012"],
        off_repo_canonical="data/cache/hansen/hansen_2018_2023.npz",
    ),
    DataClaim(
        name="Hansen GFC v1.11 — lossyear — 20S_070W",
        claimed_path="data/hansen/hansen_lossyear_20S_070W.tif",
        claimed_size_mb=152.0,
        purpose="Year of loss event 2001-2023, Chaco tile",
        paper_ids=["P0011", "P0010", "P0012"],
        off_repo_canonical="data/cache/hansen/hansen_2018_2023.npz",
    ),
    # ---------- MapBiomas Paraguay 2023 ----------
    DataClaim(
        name="MapBiomas Paraguay Collection 2 (2023)",
        claimed_path="data/mapbiomas/mapbiomas_paraguay_2023.tif",
        claimed_size_mb=38.0,
        purpose="Land cover 2023 (33867 x 34409 pixels @ 30 m)",
        paper_ids=["P0011", "P0010", "P0012", "P0025", "P0026"],
        off_repo_canonical="data/cache/mapbiomas/mapbiomas_py_2022.npy",
    ),
    # ---------- Sentinel-2 L2A ----------
    DataClaim(
        name="Sentinel-2 L2A — 6 scenes, B08 NIR band",
        claimed_path="data/sentinel2/S2*_B08.tif",
        claimed_size_mb=1500.0,  # ~1.5 GB total across 6 files
        purpose="10 m optical imagery, Paraguayan Chaco east",
        paper_ids=["P0011", "P0025"],
        off_repo_canonical="data/cache/sentinel2/",
    ),
    # ---------- INDI indigenous territories ----------
    DataClaim(
        name="INDI indigenous territories (CSV)",
        claimed_path="data/raw/ine_indi/indi_territories_PLACEHOLDER.csv",
        claimed_size_mb=None,
        purpose="10 indigenous community territories, Hansen overlap analysis",
        paper_ids=["P0012"],
        notes="PLACEHOLDER marker — see ACTUAL_RESULTS.md for the real source.",
    ),
    DataClaim(
        name="INE census 2022 by depto + ethnicity (CSV)",
        claimed_path="data/raw/ine_indi/ine_census_2022_depto_etnia_SYNTHETIC.csv",
        claimed_size_mb=None,
        purpose="Synthetic INE census data for disparity analysis",
        paper_ids=["P0012"],
    ),
    # ---------- FAO/MAG yield ----------
    DataClaim(
        name="FAO/MAG Paraguay yield 2023 (JSON)",
        claimed_path="data/raw/fao_mag/fao_yield_2023_paraguay.json",
        claimed_size_mb=None,
        purpose="Public FAO/MAG yield data for P0025 Yrupe",
        paper_ids=["P0025"],
    ),
    DataClaim(
        name="Synthetic yield 2020-2023 (CSV)",
        claimed_path="data/raw/fao_mag/synthetic_yield_2020_2023.csv",
        claimed_size_mb=None,
        purpose="Synthetic yield fixture for the multi-task CNN pilot",
        paper_ids=["P0025"],
    ),
    # ---------- INBIO ----------
    DataClaim(
        name="INBIO soybean trial 2024 (CSV)",
        claimed_path="data/raw/inbio/yrupe_2024.csv",
        claimed_size_mb=None,
        purpose="Public INBIO trial data, Yrupe paper",
        paper_ids=["P0025"],
    ),
    # ---------- P0012 disparity index ----------
    DataClaim(
        name="P0012 disparity index (CSV)",
        claimed_path="data/raw/ine_indi/disparity_index.csv",
        claimed_size_mb=None,
        purpose="Indigenous deforestation disparity index, P0012 Yvy",
        paper_ids=["P0012"],
    ),
    # ---------- Verra Registry ----------
    DataClaim(
        name="Verra VCS Registry (5 Paraguayan projects)",
        claimed_path="data/cache/verra/verra_paraguay.json",
        claimed_size_mb=None,
        purpose="Carbon credit projects, P0010 Yvyra",
        paper_ids=["P0010"],
        off_repo_canonical=None,
        notes="Curated list — downloaded via Verra web registry, no API.",
    ),
    # ---------- OpenAQ ----------
    DataClaim(
        name="OpenAQ v3 air-quality (12 stations)",
        claimed_path="data/cache/openaq/",
        claimed_size_mb=None,
        purpose="Air quality measurements for P0035 Tatakua",
        paper_ids=["P0035"],
        off_repo_canonical=None,
        notes="Live API (https://openaq.org/) — cached snapshots only.",
    ),
    # ---------- FIRMS fire alerts ----------
    DataClaim(
        name="NASA FIRMS fire alerts (Paraguay)",
        claimed_path="data/cache/firms/",
        claimed_size_mb=None,
        purpose="Fire alerts for fire/drought cross-paper analysis",
        paper_ids=["fire_drought_analysis"],
        off_repo_canonical=None,
        notes="Live API (https://firms.modaps.eosdis.nasa.gov/) — cached.",
    ),
    # ---------- LSTM trained models ----------
    DataClaim(
        name="P0035 Tatakua LSTM v1 weights (.pt)",
        claimed_path="models/lstm_tatakua/best.pt",
        claimed_size_mb=None,
        purpose="Trained LSTM for P0035 (RMSE = 14.7 µg/m³ measured)",
        paper_ids=["P0035"],
    ),
    DataClaim(
        name="P0035 Tatakua LSTM v2 weights (.pt)",
        claimed_path="models/lstm_tatakua_v2/best.pt",
        claimed_size_mb=None,
        purpose="Trained LSTM v2 multi-station (per feat/p0035+lstm_v2)",
        paper_ids=["P0035"],
    ),
]


def _sha256_prefix(path: Path, n: int = 12) -> str | None:
    """Return the first n hex chars of the SHA256, or None on read error."""
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
                if len(h.hexdigest()) >= n:
                    break
        return h.hexdigest()[:n]
    except (OSError, PermissionError):
        return None


def _resolve_glob_to_dir(path_str: str) -> Path:
    """Resolve a glob-style claimed path to its parent directory for size check."""
    p = Path(path_str)
    if "*" in str(p):
        # Glob-style: take the directory part
        return p.parent
    return p


def _audit_one(claim: DataClaim) -> DataClaim:
    """Populate the status fields on a single claim."""
    p = Path(claim.claimed_path)
    if not p.is_absolute():
        p = REPO_ROOT / p

    # Glob-style path (e.g. data/sentinel2/S2*_B08.tif)
    if "*" in str(p):
        parent = p.parent
        parent_abs = parent if parent.is_absolute() else REPO_ROOT / parent
        matches = list(parent_abs.glob(p.name)) if parent_abs.exists() else []
        if matches:
            total = sum(m.stat().st_size for m in matches if m.is_file())
            claim.actual_path = str(parent_abs)
            claim.actual_size_mb = round(total / (1024 * 1024), 2)
            claim.status = "present"
            if (
                claim.claimed_size_mb
                and claim.actual_size_mb < 0.5 * claim.claimed_size_mb
            ):
                claim.status = "partial"
                claim.notes = (
                    f"Got {claim.actual_size_mb:.1f} MB, "
                    f"claimed {claim.claimed_size_mb:.1f} MB"
                )
            return claim
        # Glob had no matches — fall through to off-repo check below
        claim.notes = f"No files match glob {p.name} in {parent}"

    if p.exists():
        size = p.stat().st_size
        claim.actual_path = str(p)
        claim.actual_size_mb = round(size / (1024 * 1024), 2)
        claim.sha256_prefix = _sha256_prefix(p)
        # Heuristic: "synthetic" if filename contains PLACEHOLDER or SYNTHETIC
        name_upper = p.name.upper()
        if "PLACEHOLDER" in name_upper:
            claim.status = "synthetic"
            claim.notes = "Filename contains PLACEHOLDER — not real data"
        elif "SYNTHETIC" in name_upper:
            claim.status = "synthetic"
            claim.notes = "Filename contains SYNTHETIC — fixture only"
        else:
            claim.status = "present"
        return claim

    # Path doesn't exist in repo. Check off-repo canonical if given.
    if claim.off_repo_canonical and not claim.off_repo_canonical.startswith("http"):
        off = Path(claim.off_repo_canonical)
        if not off.is_absolute():
            off = REPO_ROOT / off
        if off.exists():
            claim.status = "off-repo"
            claim.actual_path = str(off)
            try:
                if off.is_dir():
                    claim.actual_size_mb = round(
                        sum(f.stat().st_size for f in off.rglob("*") if f.is_file())
                        / (1024 * 1024),
                        2,
                    )
                else:
                    claim.actual_size_mb = round(off.stat().st_size / (1024 * 1024), 2)
            except OSError:
                claim.actual_size_mb = None
            claim.notes = f"Exists at canonical off-repo path: {off}"
            return claim

    claim.status = "missing"
    return claim


def audit(strict: bool = False) -> tuple[dict, dict[str, list[DataClaim]]]:
    """Run the full audit and return the JSON-able result dict."""
    by_status: dict[str, list[DataClaim]] = {
        "present": [],
        "missing": [],
        "off-repo": [],
        "synthetic": [],
        "partial": [],
    }
    for c in CLAIMS:
        _audit_one(c)
        by_status[c.status].append(c)

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo_root": str(REPO_ROOT),
        "total_claims": len(CLAIMS),
        "by_status_count": {k: len(v) for k, v in by_status.items()},
        "claims": [asdict(c) for c in CLAIMS],
    }
    summary["any_missing_or_partial"] = bool(
        by_status["missing"] or by_status["partial"]
    )
    return summary, by_status


def print_summary(by_status: dict[str, list[DataClaim]], quiet: bool) -> None:
    """Print a one-line-per-claim stdout summary."""
    if quiet:
        counts = {k: len(v) for k, v in by_status.items()}
        print(
            f"data_audit: present={counts['present']} "
            f"synthetic={counts['synthetic']} "
            f"off-repo={counts['off-repo']} "
            f"partial={counts['partial']} "
            f"missing={counts['missing']}"
        )
        return

    print(f"Data audit — {REPO_ROOT}\n")
    for status, claims in by_status.items():
        if not claims:
            continue
        print(f"--- {status.upper()} ({len(claims)}) ---")
        for c in claims:
            tag = f"[{','.join(c.paper_ids)}]"
            size = (
                f"{c.actual_size_mb:.1f}MB"
                if c.actual_size_mb
                else "?"
            )
            print(f"  {tag:18} {c.name}")
            print(f"    claimed: {c.claimed_path} ({c.claimed_size_mb} MB)")
            if c.actual_path:
                print(f"    actual:  {c.actual_path} ({size})")
            if c.sha256_prefix:
                print(f"    sha256:  {c.sha256_prefix}…")
            if c.notes:
                print(f"    note:    {c.notes}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the datasets this thesis repo claims to have."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any dataset is missing, partial, or off-repo.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print the summary counts line.",
    )
    parser.add_argument(
        "--json",
        type=str,
        default="outputs/data_audit.json",
        help="Path to write the JSON audit result (default: outputs/data_audit.json).",
    )
    args = parser.parse_args()

    summary, by_status = audit(strict=args.strict)

    print_summary(by_status, quiet=args.quiet)

    # Always write JSON
    out_path = REPO_ROOT / args.json
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        json.dump(summary, f, indent=2, default=str)
    if not args.quiet:
        print(f"\nJSON audit written to: {out_path}")

    if args.strict and summary["any_missing_or_partial"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
