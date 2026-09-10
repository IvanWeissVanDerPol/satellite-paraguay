# P0030 Yvyra Soy — Indigenous Territory × Soybean Frontier in Paraguay

## Overview

This paper presents **Yvyra Soy** (\textit{field of the wild pig} in
Guaraní, used here to evoke the intersection of cultivation and
frontier land), a public-data analysis of the relationship between
indigenous territory presence and soybean frontier expansion across
Paraguay's 16 soy-producing departments, 2007/08--2024/25.

The paper joins three openly-published data sources:

- **INE 2022 indigenous communities census** (557 communities across 19
  pueblos)
- **OSM community polygons** (30 features with admin_level 10/11,
  scraped via the Overpass API)
- **MAG cereal yield 2007/08--2024/25** (soybean *Glycine max* by
  department-year, sourced from datos.gov.py / DCEA)

The headline contribution is **infrastructure**: a reproducible,
public-data pipeline under MIT license that future ethics-approved
studies can build on. The specific findings on pueblo distribution
and departmental yield are illustrative and limited by the public-data
granularity (no per-community loss rates without INDI shapefile
acquisition, which is outside the scope of public-data analysis).

## Data integrity statement (2026-09-09)

The thesis author has not contacted any indigenous community. This
is a public-data analysis only — no FPIC engagement has been
conducted. See `ACTUAL_RESULTS.md` for data provenance and
`outputs/DEFENSE_PREP_15_HAT_AUDIT_2026-09-09.md` Hat 7 for the
ethics context.

The Per-pueblo and per-department numbers in this paper are real
measurements from public data. No number in this paper comes from a
fabricated or hallucinated source.

## Measured pilot results (see `ACTUAL_RESULTS.md` for full table)

### Indigenous communities by pueblo (INE 2022)

Total: 19 pueblos, 557 communities. The five largest pueblos:

| Rank | Pueblo | Communities | % of total |
|---|---|---:|---:|
| 1 | Mbya Guaraní | 200 | 35.9% |
| 2 | Ava Guaraní | 150 | 26.9% |
| 3 | Pai Tavytera | 61 | 10.9% |
| 4 | Ayoreo | 26 | 4.7% |
| 5 | Nivacle | 23 | 4.1% |
| | (Other 14 pueblos) | 97 | 17.4% |
| | **Total** | **557** | **100%** |

Source: `data/raw/ine_indi/indigenous_communities_2022_summary.csv`
(INE 2022 census, public; downloaded 2026-09-08 via datos.gov.py).

### Soybean yield by department (MAG, 5-year mean)

16 departments with positive yield data. National mean: **2,429 kg/ha**
(weighted by 5-year area). Top 5 departments:

| Rank | Department | Mean yield (kg/ha) | 5yr total area (ha) |
|---|---|---:|---:|
| 1 | Amambay | 3,095 | 863,308 |
| 2 | Alto Paraguay | 2,982 | 86,765 |
| 3 | Paraguarí | 2,930 | 22,109 |
| 4 | Cordillera | 2,742 | 6,487 |
| 5 | Guairá | 2,662 | 91,610 |

Source: `data/raw/fao_mag/mag_soja_rendimiento.csv` and
`mag_soja_superficie.csv` (MAG/DCEA, public; downloaded 2026-09-08).

### OSM community polygon coverage

30 features with admin_level 10/11 and names matching
*Comunidad Indígena …* patterns. Bounding box:
`[lon_min, lat_min, lon_max, lat_max] = [-58.5, -25.5, -54.5, -19.5]`.
Source: `data/raw/osm_indigenous/osm_comunidades_indigenas_py.geojson`
(Overpass API, downloaded 2026-09-08).

## Method

### Data sources

| Source | Coverage | Granularity | Use in P0030 |
|---|---|---|---|
| INE 2022 census | 557 communities, 19 pueblos | Per-pueblo aggregation | Census counts |
| OSM community polygons | 30 features | Polygon | Spatial coverage check |
| MAG cereal yield | 18 departments × 18 years | Per-department-year | Soy yield trend |
| Hansen GFC v1.11 | 1 tile (256×256, 56 km²) | Per-pixel | Territorial anchor only |

### Pipeline

The `src/papers/p0030_yvyra_soy/pipeline.py` module implements four
joins:

1. **INE census:** load `indigenous_communities_2022_summary.csv`,
   aggregate per-pueblo.
2. **MAG yield:** load `mag_soja_rendimiento.csv`,
   `mag_soja_superficie.csv`; compute 5-year mean yield per
   department.
3. **OSM polygons:** load GeoJSON; compute bounding box + feature
   count.
4. **Joint table:** merge per-pueblo counts with departmental yields
   (this step requires a department→pueblo mapping which is not
   available in public data; see "Limitations" below).

Output: `outputs/p0030/p0030_analysis.json` (machine-readable) and
`outputs/p0030/p0030_analysis.md` (human-readable report).

## What this paper does NOT compute

- **Per-community loss rates.** These would require the INDI shapefile
  (which is not public), per-community land-use history, and
  FPIC-engaged ground-truthing.
- **Causal attribution.** Correlation only, at departmental scale.
  No causal inference attempted.
- **FPIC compliance.** No community engagement (per the 2026-09-09
  audit). The infrastructure is built so future work can pursue
  CARE-Principles-compliant co-production.
- **Sub-pixel boundary disputes.** No high-resolution land-cover map;
  community boundaries approximated from OSM polygons.

## Discussion

The pipeline is reproducible end-to-end from public data. The pueblo
distribution and departmental yield numbers are real measurements.

The framework supports extension in three directions:

1. **Acquire INDI shapefiles** (a multi-month institutional process
   outside the scope of this thesis) for per-community loss analysis.
2. **Integrate Hansen full-Paraguay tiles** (off-repo, ~6 GB) for
   spatial overlap between soy expansion and deforestation frontiers.
3. **Add FPIC-engaged community co-production** of the analysis
   protocol per CARE Principles (Carroll et al. 2020).

The contribution of this paper is the **infrastructure**, not the
specific findings. As Paraguay's environmental governance evolves,
this infrastructure can be repurposed for monitoring under INFONA's
deforestation control program, MAG's agricultural census, or
INDI's territorial registry.

## Limitations

This is a **public-data-only analysis**. The following limitations
are inherent to that constraint:

1. **No community-level resolution.** The 30 OSM polygons cover
   ~5% of the 557 census communities. Per-community analysis is
   not possible.
2. **No FPIC engagement.** Per the 2026-09-09 audit, zero communities
   have been contacted. This paper cannot make claims about how
   specific communities experience soybean expansion.
3. **No causal claim.** Departmental correlation is not causation.
   The framework supports future causal analysis (e.g., matching
   estimators, instrumental variables) but does not perform it.
4. **Pilot scope.** The Hansen tile is a single 256×256 sample
   (~56 km² of the ~250,000 km² Chaco). Full Paraguay coverage
   would require downloading ~4,400 tiles.

## Data and Code Availability

All code, data processing scripts, and the analysis pipeline are
released as open-source under the MIT license at
<https://github.com/IvanWeissVanDerPol/satellite-paraguay>.

Raw data sources:
- INE 2022: <https://www.ine.gov.py/censo2022/>
- OSM: <https://www.openstreetmap.org/> (via Overpass API)
- MAG: <https://datos.gov.py/> (DCEA yield records)
- Hansen GFC: <https://www.globalforestwatch.org/>

## Author and affiliation

**Author:** Iván Weiss Van der Pol

**Affiliation:** FP-UNA (Facultad Politécnica de la Universidad Nacional
de Asunción), San Lorenzo, Paraguay

**Adviser:** PENDING (thesis author has not identified or contacted a
thesis adviser as of 2026-09-09; see audit document)

**Keywords:** indigenous lands, soybean, Paraguay, Gran Chaco,
public data, OSM, INE, CARE Principles, FPIC

## Status

- [x] Pipeline implemented (`src/papers/p0030_yvyra_soy/`)
- [x] Pipeline runs end-to-end on real data
- [x] Pueblo + departmental + OSM numbers measured
- [x] LaTeX paper template (`paper.tex`)
- [x] Markdown long-form version (`paper.md`)
- [x] ACTUAL_RESULTS.md with data lineage
- [ ] Related work + references (Phase A4)
- [ ] Tests (Phase A6)
- [ ] Thesis integration (Phase A7)

See `outputs/p0030/p0030_analysis.md` for the analysis output.
