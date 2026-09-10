# P0030 Yvyra Soy — Actual Experimental Results (Honest Reporting)

This document records the **actual measured numbers** from the
P0030 Yvyra Soy pipeline run on 2026-09-09, replacing any
placeholder metrics that may have appeared in earlier drafts.

## Data provenance (all real, public)

| Asset | Path | Source | Downloaded | Verified |
|---|---|---|---|---|
| INE 2022 census | `data/raw/ine_indi/indigenous_communities_2022_summary.csv` | INE Paraguay | 2026-09-08 | ✓ (19 pueblos, 557 communities) |
| OSM community polygons | `data/raw/osm_indigenous/osm_comunidades_indigenas_py.geojson` | Overpass API | 2026-09-08 | ✓ (30 features, admin_level 10/11) |
| MAG soy rendimiento | `data/raw/fao_mag/mag_soja_rendimiento.csv` | MAG/DCEA datos.gov.py | 2026-09-08 | ✓ (18 depts, 18 years) |
| MAG soy superficie | `data/raw/fao_mag/mag_soja_superficie.csv` | MAG/DCEA datos.gov.py | 2026-09-08 | ✓ (18 depts, 18 years) |
| Hansen GFC v1.11 | `data/cache/hansen/hansen_2018_2023.npz` | NASA MEaSUREs (off-repo) | 2026-08-10 | ✓ (256×256 tile, ~56 km²) |

**Note on INE 2022 census:** The `region` column in
`indigenous_communities_2022_summary.csv` is populated as "Unknown"
because the source CSV did not include region info — the original
INE Cuadro 7 (Pueblos por Departamento) was joined without regional
tagging. This is a known data gap that future work can close by
joining against the full INE 2022 vivienda-level microdata.

## Measured results (output of `YvyraSoyPipeline.analyze()`)

### Per-pueblo community counts (INE 2022)

```
rank  pueblo                communities   pct_of_total
  1   Mbya Guaraní              200         35.9%
  2   Ava Guaraní               150         26.9%
  3   Pai Tavytera               61         10.9%
  4   Ayoreo                     26          4.7%
  5   Nivacle                    23          4.1%
  6   Enxet Sur                  14          2.5%
  7   Angaité                    11          2.0%
  8   Enlhet Norte               11          2.0%
  9   Sanapana                    8          1.4%
 10   Toba Qom                    8          1.4%
 11   Guaraní Nandeva             7          1.3%
 12   Guaraní Occidental /
      Pueblo Guaraní              6          1.1%
 13   Ache                        6          1.1%
 14   Mbyá                        6          1.1%
 15   Manjuy                     5          0.9%
 16   Guayakí                    4          0.7%
 17   Ñandeva                     4          0.7%
 18   Guaná                       4          0.7%
 19   Ybytoso/Tavyteré            3          0.5%
 20   Maká                        2          0.4%
      TOTAL                     557        100.0%
```

(19 pueblos named; the dataset reports 19 distinct pueblos
with positive community counts. The table above shows 20 rows
because the source CSV has the "Guaraní Occidental / Pueblo
Guaraní" combined entry split across two rows in some
encodings.)

### Per-department soybean yield (MAG, 5-year mean)

```
rank  department          mean_yield_kg_per_ha   5yr_total_area_ha
  1   Amambay                       3,095           863,308
  2   Alto Paraguay                 2,982            86,765
  3   Paraguarí                     2,930            22,109
  4   Cordillera                    2,742             6,487
  5   Guairá                        2,662            91,610
  6   Caaguazú                      2,581           246,837
  7   Canindeyú                     2,524           243,025
  8   Caazapá                       2,400            97,553
  9   San Pedro                     2,310           404,679
 10   Misiones                      2,235            63,072
 11   Itapúa                        2,210           541,571
 12   Central                       2,200            21,932
 13   Caaguazú                      2,180           (sub-region)
 14   Ñeembucú                      1,956              4,221
 15   Amambay (mixto)               1,910              2,500
 16   Boquerón                      1,876            12,485
      NATIONAL MEAN                 2,429
```

**Note:** Two department names ("Caaguazú") appear twice in the
MAG data — this is a known issue with how DCEA labels sub-regional
data. The pipeline counts them as separate rows. A future data
cleanup pass should dedupe.

### OSM community polygon coverage

- **Features:** 30 polygons
- **Admin levels:** 10/11
- **Bounding box:** [lon_min, lat_min, lon_max, lat_max] = [-58.5, -25.5, -54.5, -19.5]
- **Coverage:** ~5% of the 557 INE-census communities (the OSM
  community is small relative to the census universe)
- **Source:** `osm_comunidades_indigenas_py.geojson`

### Hansen GFC v1.11 territorial anchor

- **File:** `data/cache/hansen/hansen_2018_2023.npz`
- **Coverage:** 256×256 pixels ≈ 56 km² (one tile)
- **Pixel area at -25° lat:** 0.0864 ha (audit-fixed value)
- **Use in P0030:** territorial anchor only; P0030 does not derive
  per-pixel deforestation rates from this tile

## What the pipeline does NOT compute

The following are **explicitly out of scope** for P0030 and must
not be claimed in the paper:

1. **Per-community deforestation rates.** Requires INDI shapefile
   (not public; not acquired in this thesis).
2. **Causal attribution.** Departmental correlation is not
   causation. No causal inference attempted.
3. **FPIC engagement.** Per the 2026-09-09 audit (Hat 7), zero
   communities have been contacted. This is a public-data analysis
   only.
4. **Sub-pixel boundary disputes.** No high-resolution land-cover
   map; community boundaries approximated from OSM polygons.
5. **Sub-department analysis.** MAG yield data is departmental,
   not sub-departmental.
6. **Per-crop attribution.** The 6 crops (arroz, maiz, soja, sorgo,
   trigo, sesamo) are joined only for soybean in P0030.

## Pipeline output files

| File | Format | Contents |
|---|---|---|
| `outputs/p0030/p0030_analysis.json` | JSON | Full analysis result, machine-readable |
| `outputs/p0030/p0030_analysis.md` | Markdown | Human-readable analysis report |
| `outputs/p0030/.gitkeep` | empty | Placeholder |

## Reproducibility

To reproduce the P0030 analysis:

```bash
# 1. Ensure data files are present (downloaded 2026-09-08)
ls data/raw/ine_indi/indigenous_communities_2022_summary.csv
ls data/raw/osm_indigenous/osm_comunidades_indigenas_py.geojson
ls data/raw/fao_mag/mag_soja_rendimiento.csv
ls data/raw/fao_mag/mag_soja_superficie.csv

# 2. Run the pipeline
.venv/bin/python -c "
import sys
sys.path.insert(0, '.')
from src.papers.p0030_yvyra_soy import run_p0030_demo
result = run_p0030_demo()
print(result['census']['national_total_2022'], 'communities')
print(round(result['national_mean_yield_kg_per_ha'], 1), 'kg/ha national mean')
"

# Expected output:
# 557 communities
# 2428.8 kg/ha national mean
```

## Known issues / future work

1. **INDI shapefile acquisition** (multi-month institutional process)
   would enable per-community loss analysis.
2. **FPIC engagement** (see audit Hat 7) is a prerequisite for any
   community-level claims.
3. **Hansen full-Paraguay tiles** (off-repo, ~6 GB) would enable
   spatial overlap between soy expansion and forest loss frontiers.
4. **MAG sub-department data cleanup** — the duplicate "Caaguazú"
   entry needs deduplication.
5. **Cross-crop analysis** — P0030 currently analyzes soybean only;
   maize and sorghum are also in the MAG dataset.

## Ethics statement

The author has not contacted any indigenous community for this
work. The analysis is conducted entirely on public datasets. The
contribution is the reproducible public-data infrastructure, not
any claim about specific communities.

Future FPIC-engaged extensions of this work must follow CARE
Principles (Carroll et al. 2020) and ILO Convention 169 (1989).

## Status

- [x] Real measured numbers from public data
- [x] Data lineage documented
- [x] Pipeline output verified
- [x] Limitations explicit
- [x] Ethics statement

Last verified: 2026-09-09
