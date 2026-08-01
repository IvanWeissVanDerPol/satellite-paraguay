# P0025_YRUPE_YIELD — Yrupe (Soybean yield prediction in Caaguazú)

**Status:** Pipeline scaffolding complete; awaiting real data + training.

## At a glance

- **Title (Guaraní):** **Yrupe**
- **Title (English):** Soybean yield prediction in Caaguazú
- **Title (Spanish):** Predicción de rendimiento de soja en Caaguazú
- **Target journal:** **Computers and Electronics in Agriculture**
- **Advisor:** Multi (FCA + INBIO)
- **Timeline:** 8 weeks
- **Metric:** R² > 0.80 on yield prediction

## Data sources

Sentinel-2 time series + INBIO records + Delineate Anything v2

## Novelty

First ML-based soybean yield prediction for Paraguay

## Status checklist

- [x] Pipeline scaffolding (`pipeline.py`)
- [x] Configuration (`configs/p0025_yrupe_yield.yaml`)
- [x] Baseline implementations (`src/baselines/`)
- [x] Tests (`tests/test_pipelines.py`)
- [ ] Real data download + preprocessing
- [ ] Model training on real data
- [ ] Evaluation against ground truth
- [ ] Paper draft (`abstract.md`, `introduction.md`, `methods.md`, `results.md`)
- [ ] Figures + tables
- [ ] Internal review
- [ ] Submission to journal

## Open issues / blockers

_None yet — pipeline ready for real data._

## Next actions (this week)

1. Set up Google Earth Engine authentication
2. Download real Sentinel-2 data for first tile
3. Run baseline comparison
4. Begin training
5. Start drafting methods section

## How to run

```bash
make run-paper-0025
# Or directly:
python -m src.papers.p0025_yrupe_yield.pipeline
```

## Files

- `../src/papers/p0025_yrupe_yield/pipeline.py` — main pipeline
- `../configs/p0025_yrupe_yield.yaml` — configuration
- `../notebooks/p0025_yrupe.ipynb` — Jupyter
- `../src/baselines/p0025_yrupe_baselines.py` — baselines
