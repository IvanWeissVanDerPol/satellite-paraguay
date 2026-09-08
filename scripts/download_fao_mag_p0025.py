#!/usr/bin/env python3
"""download_fao_mag_p0025.py — Real FAO/MAG cereal yield data for P0025 Yrupe.

Downloads the official Ministerio de Agricultura y Ganadería
(MAG) cereal yield dataset from datos.gov.py (Paraguay open data
portal). Contains surface (ha), production (tn), and yield (kg/ha)
for 6 main crops × 18 crop-years × ~18 departments.

Source: datos.gov.py dataset ffc383ae-bbdb-4fb3-a4a8-0cbb85b5f7a6
Title: Superficie y Rendimiento de los Principales Cereales
Publisher: Dirección de Censos y Estadísticas Agropecuarias (DCEA)
License: https://www.paraguay.gov.py/datos-abiertos/licencias

Crops covered:
  - SOJA          (soybean)
  - MAÍZ          (corn)
  - SORGO         (sorghum)
  - TRIGO         (wheat)
  - SESAMO        (sesame)
  - ARROZ CON RIEGO  (irrigated rice)

Output:
  data/raw/fao_mag/mag_<crop>_superficie.csv    (ha by dept × year)
  data/raw/fao_mag/mag_<crop>_produccion.csv     (tn by dept × year)
  data/raw/fao_mag/mag_<crop>_rendimiento.csv   (kg/ha by dept × year)

Usage:
  python3 scripts/download_fao_mag_p0025.py
  python3 scripts/download_fao_mag_p0025.py --years 2020-2023
  python3 scripts/download_fao_mag_p0025.py --out-dir data/raw/fao_mag
"""

import argparse
import csv
import sys
from pathlib import Path

import requests
from openpyxl import load_workbook

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_URL = "https://www.datos.gov.py/sites/default/files/" "CEREALES_2007-08%20al%202024-25.xlsx"
YEARS = [
    "2007/08",
    "2008/09",
    "2009/10",
    "2010/11",
    "2011/12",
    "2012/13",
    "2013/14",
    "2014/15",
    "2015/16",
    "2016/17",
    "2017/18",
    "2018/19",
    "2019/20",
    "2020/21",
    "2021/22",
    "2022/23",
    "2023/24",
    "2024/25",
]
SECTIONS = ["SUPERFICIE (ha.)", "PRODUCCION (tn)", "RENDIMIENTO (kg/ha)"]


def safe_num(v):
    """Parse a cell value as float; return None for empty/'--'."""
    if v is None or v == "-" or (isinstance(v, str) and not v.strip()):
        return None
    if isinstance(v, (int, float)):
        return v
    try:
        return float(str(v).replace(",", ""))
    except (ValueError, TypeError):
        return None


def slugify(name):
    """Turn 'ARROZ CON RIEGO' into 'arroz_con_riego'."""
    s = name.lower().strip()
    # Replace Spanish diacritics
    repl = {
        "í": "i",
        "á": "a",
        "é": "e",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
    }
    for src, dst in repl.items():
        s = s.replace(src, dst)
    return s.replace(" ", "_")


def parse_sheet(ws):
    """Parse one XLSX sheet into {dept: {year: {section: value}}}."""
    rows = list(ws.iter_rows(values_only=True))
    # Find section start rows (the row with the section label in col 1)
    section_rows = {}
    for i, row in enumerate(rows):
        if row[1] in SECTIONS:
            section_rows[row[1]] = i + 1  # 0-indexed → 1-indexed
    if not section_rows:
        return {}

    out = {}
    HEADER_ROWS = (
        "TOTAL",
        "DEPARTAMENTO",
        "(-) Ningun Valor",
        "Fuente: Sintesis Estadisticas DCEA/",
        "*Datos del Censo 2007/08, 2021/22",
        "** Merma en el rendimiento, por efe",
    )
    HEADER_TOKENS = (
        "MINISTERIO",
        "DIRECCION",
        "SOJA -",
        "MAIZ -",
        "MAÍZ -",
        "SORGO -",
        "TRIGO -",
        "SESAMO -",
        "ARROZ -",
    )

    for sec_label, sec_row in section_rows.items():
        for j, year in enumerate(YEARS):
            col_idx = 1 + j  # year columns start at col 1 (col 0 = DEPARTAMENTO)
            for k in range(sec_row + 1, min(sec_row + 22, len(rows))):
                row = rows[k - 1]
                dept = row[0]
                if not dept or not isinstance(dept, str):
                    continue
                dept = dept.strip()
                if dept in HEADER_ROWS or dept in ("",):
                    continue
                if any(t in dept.upper() for t in HEADER_TOKENS):
                    continue
                if col_idx < len(row):
                    val = safe_num(row[col_idx])
                    if dept not in out:
                        out[dept] = {}
                    if year not in out[dept]:
                        out[dept][year] = {}
                    out[dept][year][sec_label] = val
    return out


def download_and_extract(out_dir: Path, years: list[str]) -> dict:
    """Download the XLSX, parse all 6 sheets, write 18 CSVs."""
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {DATA_URL[:80]}...")
    r = requests.get(DATA_URL, timeout=120)
    r.raise_for_status()
    xlsx_path = out_dir / "CEREALES_2007-08_al_2024-25.xlsx"
    xlsx_path.write_bytes(r.content)
    print(f"Saved {xlsx_path} ({len(r.content) / 1024:.1f} KB)")

    wb = load_workbook(xlsx_path)
    summary = {}
    for sname in wb.sheetnames:
        parsed = parse_sheet(wb[sname])
        if not parsed:
            print(f"  {sname}: EMPTY (skipping)")
            continue
        for sec_label in SECTIONS:
            crop_slug = slugify(sname)
            sec_slug = sec_label.split("(")[0].strip().lower()
            csv_path = out_dir / f"mag_{crop_slug}_{sec_slug}.csv"
            with open(csv_path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["departamento"] + years)
                for dept, by_year in parsed.items():
                    row = [dept] + [by_year.get(y, {}).get(sec_label) for y in years]
                    w.writerow(row)
            nonzero = sum(1 for d, by in parsed.items() for y in years if by.get(y, {}).get(sec_label) is not None)
            summary[f"{sname} / {sec_label}"] = {
                "file": str(csv_path),
                "depts": len(parsed),
                "non_null_cells": nonzero,
            }
    return summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out-dir", default=str(REPO_ROOT / "data/raw/fao_mag"))
    p.add_argument("--years", nargs="*", default=YEARS, help="Subset of years to extract (default: all 18)")
    args = p.parse_args()
    out_dir = Path(args.out_dir)
    summary = download_and_extract(out_dir, args.years)
    print()
    print("=== Files written ===")
    for k, v in summary.items():
        print(f"  {k:50s}  {v['depts']:>2} depts, " f"{v['non_null_cells']:>4} cells  -> {v['file']}")


if __name__ == "__main__":
    sys.exit(main())
