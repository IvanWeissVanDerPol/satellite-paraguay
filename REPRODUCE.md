# REPRODUCE.md — What is and isn't reproducible from this repo

> **Last updated:** 2026-09-16 (Tier-2 polish pass)
> **Defends:** `OPEN_SCIENCE.md` (archived 2026-09-16) — that doc claimed
> the repo was "open and reproducible"; this doc tells you the actual
> reproducibility ceiling.

## TL;DR — what you can and can't reproduce

| Subset | Reproducible from a fresh clone? | Time | Notes |
|---|---|---|---|
| **Full pytest suite** (1081 tests) | ✅ Yes | ~110s | `bash scripts/run_tests.sh` |
| **Fast subset** (~81 tests, every-commit guards) | ✅ Yes | ~2s | `bash scripts/run_tests_fast.sh` |
| **LaTeX syntax check** (6 papers) | ✅ Yes | <1s | `python3 scripts/check_latex.py` |
| **Bib DOI verification** (CrossRef, 45 entries) | ✅ Yes | ~30s | `python3 scripts/verify_bib_dois.py --summary` |
| **Defense gate** (13/13 structural checks) | ✅ Yes | ~30s | `.venv/bin/python scripts/defense_check.py` |
| **P0030 Yvyra Soy pipeline** (INE census + MAG yield + OSM polygons) | ✅ Yes — IF you keep the parquet fixtures | ~5s | See §1 below |
| **P0011 Yvutu Prithvi fine-tuning** | ❌ **No** — requires A100 GPU + Hansen tiles (~6 GB) | 3-4h | Off-repo data + paid compute (~$5 on Vast.ai) |
| **P0012 Yvy per-territory deforestation rates** | ❌ **No** — INDI shapefiles not public | weeks | Multi-month institutional request to Paraguay's INDI |
| **P0035 Tatakua air-quality LSTM** (real weights) | ✅ Yes (existing `models/lstm_tatakua/best.pt` ships in-repo) | <1s | The only paper with real trained weights |
| **Spanish translation CH1-CH11** | ⚠️ Partial — automated translation possible, academic register needs review | 4-6h | See TODO below |

## What you need to reproduce

### Software (in-repo)

```bash
# Install
uv sync --all-extras    # creates .venv; takes ~60s on a clean machine

# Run tests
bash scripts/run_tests.sh           # full suite, ~110s
bash scripts/run_tests_fast.sh      # fast subset, ~2s (use during development)
```

### Data — what lives in this repo

- `data/raw/ine_indi/2022_comunidades/` — 49 real INE IV Censo Nacional
  de Población y Viviendas para Pueblos Indígenas 2022 cuadros (C1..C30,
  A1..A30). Source: Paraguay datos.gov.py open-data archive (verified
  2026-09-08; see `outputs/ROUND_11_12_DATA_SUBSTRATE_FINDINGS.md`).
- `data/raw/ine_indi/indigenous_communities_2022_summary.csv` — derived
  per-pueblo rollup (19 pueblos, 557 communities total).
- `data/raw/ine_indi/p0012_indigenous_territories_real.csv` — OSM-derived
  community polygon features (30 features, ~5% of census universe).
- `data/raw/fao_mag/mag_soja_*.csv` — MAG/DCEA soybean yield + superficie
  + producción, 18 departments × 18 years (2007/08-2024/25).
- `data/cache/hansen/hansen_2018_2023.npz` — single Hansen GFC v1.11
  tile (256×256 pixels ≈ 56 km²), downloaded 2026-08-10.
- `models/lstm_tatakua/best.pt` — P0035 LSTM weights, real trained.

### Data — what is OFF-repo and must be acquired separately

- **Full Paraguay Hansen GFC v1.11 tile set** (~6 GB, ~4,400 tiles covering
  ~250,000 km²). Required for: full-paraguay deforestation analysis
  (P0011), per-community loss rates (P0012), spatial join with OSM
  polygons (P0030). Status: NOT acquired; on hold pending Vast.ai budget.
- **INDI shapefile** (per-community territory polygons). Required for:
  P0012 per-territory deforestation rates. Status: NOT acquired; blocked
  on Paraguay's Instituto Paraguayo del Indígena institutional process.
- **Sentinel-5P TROPOMI AOD** (subset already in `data/cache/sentinel5p/`
  but a partial scrape). Required for: P0035's full AOD validation.
- **OpenAQ v3 stations for Paraguay** — currently **0 stations exist**
  (OpenAQ v3 decommissioned PY coverage in 2024; verified 2026-09-09).
  Required for: P0035 station-level RMSE. Mitigation: P0035 is reframed
  in `ACTUAL_RESULTS.md` as methodology-only.
- **Verra registry API access** — was required for P0010 (Vyrá
  carbon-credits paper). P0010 was deleted 2026-09-08 (Round-12 audit
  found `35 + np.random.normal(0, 5)` fabrication); no longer required.

## What this repo does NOT compute (and never will without FPIC)

- **Per-community deforestation rates** — gated on FPIC engagement
  with 10 indigenous communities in Chaco. See
  `thesis/chapters/appendix_b_ethics.tex` and the
  `outputs/HONEST_GAP_LIST_2026-09-10.md` §3.1 entry.
- **Per-community identifying data** (named communities, polygon-level
  loss rates, household-level data). The thesis is a public-data analysis
  only; per the explicit CARE Principles non-compliance statement in
  `appendix_b_ethics.tex` and `papers/drafts/p0030_yvyra_soy/methods.md`.
- **Causal inference on indigenous-community density → soy expansion.**
  The P0030 cross-department Pearson correlation is r=-0.306 (p=0.27,
  n=14) — NOT statistically significant. The interpretation in
  `outputs/p0030/p0030_regression_analysis.json` explicitly says the
  data does NOT support this causal claim.

## Step-by-step: reproducing P0030 from a fresh clone

The single paper with the most complete reproducibility story.

```bash
# 1. Clone (or copy) the repo
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay.git
cd satellite-paraguay

# 2. Install
uv sync --all-extras
source .venv/bin/activate

# 3. Verify data is in place
ls data/raw/ine_indi/indigenous_communities_2022_summary.csv
ls data/raw/fao_mag/mag_soja_rendimiento.csv
ls data/raw/fao_mag/mag_soja_superficie.csv
ls data/raw/osm_indigenous/osm_comunidades_indigenas_py.geojson

# 4. Run the pipeline
python3 -c "
import sys
sys.path.insert(0, '.')
from src.papers.p0030_yvyra_soy import run_p0030_demo
result = run_p0030_demo()
print('Communities:', result['census']['national_total_2022'])
print('Pueblos:', result['census']['n_pueblos'])
print('National mean yield:', round(result['national_mean_yield_kg_per_ha'], 1), 'kg/ha')
"

# Expected output:
# Communities: 557
# Pueblos: 19
# National mean yield: 2428.8 kg/ha

# 5. Run the per-region regression
python3 -c "
import sys, json
sys.path.insert(0, '.')
from src.papers.p0030_yvyra_soy.pipeline import run_p0030_regression
result = run_p0030_regression()
print(json.dumps(result['headline_finding'], indent=2))
"

# Expected headline_finding:
# {
#   'ratio_occident_vs_orient': 1.95,
#   'n_occidental_with_data': 2,
#   'n_oriental_with_data': 12,
#   'cross_dept_regression.pearson_r': -0.306,
#   ...
# }

# 6. Run the defense gate
python3 scripts/defense_check.py
# Expected: Total: 13 passed, 0 warnings, 0 failed, 0 errored
```

If any of these fail, the repo is broken — please open an issue at
`IvanWeissVanDerPol/satellite-paraguay/issues`.

## What you should NOT try to reproduce

- **The 5 aspirational headline numbers from the abstract** (F1>0.85,
  50×, MAE<5, etc.) — these were aspirational placeholders replaced
  by measured numbers on 2026-08-10 (the "honest reporting" pass).
  The measured numbers (e.g., P0011 U-Net F1=0.5592 on 15 synthetic
  tiles, P0035 LSTM RMSE=14.7 µg/m³ on 12 OpenAQ v2 stations) ARE
  reproducible. The aspirational numbers were never implemented.
- **P0010 Vyrá carbon-credits paper** — deleted 2026-09-08 after
  Round-12 audit found `np.random.normal(0, 5)` fabrication. Do not
  try to reproduce. The directory `papers/drafts/p0010_yvyra_carbon_credits/`
  is gone.
- **Per-paper Discussion sections claiming "future work" with
  world-record F1, 50× improvements, etc.** — these were aspirational
  targets from early drafts; the measured numbers and honest reporting
  notes are what you can trust.

## TODO (to close the reproducibility gap)

1. **Acquire the full Paraguay Hansen tile set** (~6 GB, ~4,400 tiles).
   Vendor options: NASA MEaSUREs direct download, AWS S3 mirror, or
   GEE export. Estimated transfer time on a 100 Mbps line: ~10 minutes.
   After acquisition, P0011 + P0012 can be re-run with real
   full-paraguay data instead of the single-tile pilot.
2. **Request INDI shapefile** (multi-month institutional process).
   After acquisition, P0012's per-territory percentages become real
   measurements instead of the 10 hardcoded placeholders.
3. **FPIC engagement** (40-100h in-person, 3-6 months, ILO-169
   process). Required before any per-community publication.
4. **Spanish translation** of CH1-CH11 (4-6h automated + academic-
   register review). The substrate's Spanish version of the data
   viewer is live; the thesis prose is English-only.
5. **OpenAQ data refresh** — OpenAQ v3 has 0 PY stations. Options:
   (a) submit PY stations to OpenAQ via partner organization, (b)
   migrate P0035 to Sentinel-5P AOD + ground truth from a Paraguayan
   partner, (c) reframe P0035 as methodology-only.

## See also

- `outputs/HONEST_GAP_LIST_2026-09-10.md` — the forward-looking gap list
- `outputs/DEFENSE_PREP_15_HAT_AUDIT_2026-09-09.md` — the 15-hat critical pass
- `outputs/ROUND_8_VERIFICATION_2026-09-08.md` — Round-8 bib verification
- `thesis/chapters/appendix_b_ethics.tex` — ethics framework + CARE
  Principles non-compliance statement
- `CLAUDE.md` — agent instructions for working in this repo
- `STATUS.md` — live state (regenerated by watchdog every 6h)
