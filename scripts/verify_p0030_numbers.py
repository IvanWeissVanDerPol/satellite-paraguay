#!/usr/bin/env python3
"""Independent verification of P0030 Yvyra Soy headline numbers.

Reads the raw CSVs directly (bypassing src.papers.p0030_yvyra_soy.*)
and re-derives the same headline numbers the pipeline produces.
Any divergence indicates the pipeline is computing something other
than the raw data shows.

Exit code: 0 if all checks match, 1 otherwise.

Run:
    .venv/bin/python scripts/verify_p0030_numbers.py
"""

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INE_PATH = REPO / "data" / "raw" / "ine_indi" / "indigenous_communities_2022_summary.csv"
REND_PATH = REPO / "data" / "raw" / "fao_mag" / "mag_soja_rendimiento.csv"
PIPELINE_OUT = REPO / "outputs" / "p0030" / "p0030_analysis.json"


def main():
    failures = []

    # 1. INE 2022 census
    pueblos = defaultdict(int)
    with open(INE_PATH) as f:
        reader = csv.reader(f)
        header = next(reader)
        pueblo_col = header.index("pueblo")
        count_col = header.index("comunidades_count_2022")
        for row in reader:
            if not row or not row[pueblo_col].strip():
                continue
            try:
                pueblos[row[pueblo_col].strip()] += int(row[count_col])
            except (ValueError, IndexError):
                continue

    n_pueblos = len(pueblos)
    total_communities = sum(pueblos.values())
    top5_pueblos_names = [name for name, _ in sorted(pueblos.items(), key=lambda x: -x[1])[:5]]

    # 2. MAG soy yield
    dept_yields = {}
    with open(REND_PATH) as f:
        reader = csv.reader(f)
        header = next(reader)
        year_cols = [(i, h) for i, h in enumerate(header[1:], start=1)]
        for row in reader:
            if not row or not row[0].strip():
                continue
            dept = row[0].strip()
            values = []
            for idx, year_str in year_cols:
                if idx >= len(row):
                    continue
                try:
                    v = float(row[idx])
                    if v > 0:
                        values.append(v)
                except ValueError:
                    continue
            if values:
                dept_yields[dept] = sum(values[-5:]) / min(5, len(values[-5:]))

    n_departments = len(dept_yields)
    national_mean = sum(dept_yields.values()) / n_departments if dept_yields else 0
    top5_depts_names = [d for d, _ in sorted(dept_yields.items(), key=lambda x: -x[1])[:5]]

    # 3. Compare against pipeline output
    if not PIPELINE_OUT.exists():
        print(f"PIPELINE OUTPUT MISSING: {PIPELINE_OUT}")
        print("Run the pipeline first:")
        print("  from src.papers.p0030_yvyra_soy import run_p0030_demo")
        return 1

    with open(PIPELINE_OUT) as f:
        pipeline = json.load(f)

    pipe_pueblos = pipeline["census"]["n_pueblos"]
    pipe_total = pipeline["census"]["national_total_2022"]
    pipe_n_depts = len(pipeline["soy_by_department"])
    pipe_nat_mean = pipeline["national_mean_yield_kg_per_ha"]
    pipe_top5_pueblos_names = [p["pueblo"] for p in pipeline["census"]["pueblos"][:5]]
    pipe_top5_depts_names = sorted(
        pipeline["soy_by_department"].items(),
        key=lambda x: -(x[1]["mean_yield_kg_per_ha_5yr"] or 0),
    )
    pipe_top5_depts_names = [d for d, _ in pipe_top5_depts_names[:5]]

    print("=" * 70)
    print("P0030 INDEPENDENT VERIFICATION")
    print("=" * 70)
    print(f"  Pueblos count:        raw={n_pueblos}  pipe={pipe_pueblos}")
    print(f"  Communities total:    raw={total_communities}  pipe={pipe_total}")
    print(f"  Departments:          raw={n_departments}  pipe={pipe_n_depts}")
    print(f"  National mean yield:  raw={round(national_mean, 1)}  pipe={round(pipe_nat_mean, 1)}")
    print(f"  Top 5 pueblos:         raw={top5_pueblos_names}")
    print(f"                        pipe={pipe_top5_pueblos_names}")
    print(f"  Top 5 departments:    raw={top5_depts_names}")
    print(f"                        pipe={pipe_top5_depts_names}")

    checks = [
        ("Pueblos count", n_pueblos, pipe_pueblos),
        ("Communities total", total_communities, pipe_total),
        ("Departments", n_departments, pipe_n_depts),
        ("National mean yield", round(national_mean, 1), round(pipe_nat_mean, 1)),
        ("Top 5 pueblos", top5_pueblos_names, pipe_top5_pueblos_names),
        ("Top 5 departments", top5_depts_names, pipe_top5_depts_names),
    ]
    for name, raw, pipe in checks:
        if raw != pipe:
            failures.append(name)
            print(f"  MISMATCH on {name}: raw={raw}  pipe={pipe}")

    print()
    if failures:
        print(f"FAIL ({len(failures)} mismatches): {failures}")
        return 1
    else:
        print(f"PASS (all {len(checks)} checks match)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
