# Yvyra Soy — Methods

## Data sources

### INE 2022 indigenous communities census

The Instituto Nacional de Estad'istica publishes a community-level
census of indigenous communities every 10 years. The 2022 census
lists 557 communities across 19 pueblos. Per-pueblo aggregation is
available at
`data/raw/ine_indi/indigenous_communities_2022_summary.csv`.

### OSM community polygons

The OpenStreetMap Foundation hosts 30 polygon features at
admin\_level 10/11 with names matching *Comunidad Ind'igena \ldots*
patterns, scraped via the Overpass API on 2026-09-08.

Bbox: [lon_min, lat_min, lon_max, lat_max] = [-58.5, -25.5, -54.5, -19.5]
covering the Gran Chaco and Eastern regions.

### MAG cereal yield 2007/08--2024/25

The Ministerio de Agricultura y Ganader'ia publishes annual cereal
yield by department including soybean (*Glycine max*). Two files:

- `data/raw/fao_mag/mag_soja_rendimiento.csv` — kg/ha per department-year
- `data/raw/fao_mag/mag_soja_superficie.csv` — ha per department-year

### Hansen GFC v1.11

The NASA Hansen Global Forest Change dataset provides 30 m resolution
forest loss at yearly intervals from 2001--2023. We use the
256\times256 tile (~56 km²) included in `data/cache/hansen/` as a
territorial anchor only.

## Pipeline

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
   (this step requires a department\to pueblo mapping which is not
   available in public data; see "Limitations" below).

Output written to `outputs/p0030/p0030_analysis.json`
(machine-readable) and `outputs/p0030/p0030_analysis.md`
(human-readable report).

## Limitations

This is a **public-data-only analysis**. The following limitations
are inherent to that constraint:

1. **No community-level resolution.** The 30 OSM polygons cover
   ~5% of the 557 census communities. Per-community analysis is
   not possible.
2. **No FPIC engagement.** Per the 2026-09-09 audit, zero
   communities have been contacted.
3. **No causal claim.** Departmental correlation is not causation.
4. **Pilot scope.** The Hansen tile is a single 256\times256 sample
   (~56 km² of the ~250,000 km² Chaco).

## CARE Principles — non-compliance statement

P0030 does **not** claim CARE Principles for Indigenous Data
Governance \citep{gida2019, carroll2020care} compliance, and it
does **not** claim compliance with the earth-observation
operationalization by \citet{jennings2025}. CARE compliance
requires demonstrated engagement with affected communities —
Collective benefit, Authority to control, Responsibility, and
Ethics in practice, not just citation. As of 2026-09-16, this
paper has not engaged with any indigenous community,
organization, or representative body in Paraguay. The 19-pueblo
plus 557-community aggregate numbers come from Paraguay's
public 2022 census (INE), which the Paraguayan state published
without per-community consent. The per-region regression
(Occidental vs Oriental soy-yield trajectory) and the
indigenous-community-density computation are descriptive public-data
analyses only; they are not participatory research outputs and
they must not be cited as such. The thesis author is committed
to FPIC engagement as a post-defense extension and has flagged
the institutional pathway (FP-UNA Comité de Ética en
Investigación; INDI; Tierra Viva) for any such engagement. Any
follow-up work that publishes per-community identifying data,
per-community polygon analysis, or per-territory deforestation
rates must first satisfy the Newing et al.\ (2024) fourteen-
principle framework and obtain explicit FPIC. The reader is
referred to the thesis-level `appendix_b_ethics.tex` for the
full ethics framework statement.
