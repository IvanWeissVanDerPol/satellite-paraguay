# P0035_TATAKUA_AIR_QUALITY — Tatakua (Air-quality forecasting for Asunción (LSTM + OpenAQ + PM2.5 satellite))

**Status:** Pipeline scaffolding complete; awaiting real data + training.

## At a glance

- **Title (Guaraní):** **Tatakua**
- **Title (English):** Air-quality forecasting for Asunción (LSTM + OpenAQ + PM2.5 satellite)
- **Title (Spanish):** Pronóstico de calidad del aire para Asunción (LSTM + OpenAQ + satélite PM2.5)
- **Target journal:** **Atmospheric Environment**
- **Advisor:** Multi (FIA + Lic. Ciencias Atmosféricas)
- **Timeline:** 8 weeks
- **Metric:** MAE < 5 µg/m³ on PM2.5 forecasting

## Data sources

OpenAQ + Sentinel-5P + TimesFM/LSTM

## Novelty

First ML-based PM2.5 forecast for Asunción

## Status checklist

- [x] Pipeline scaffolding (`pipeline.py`)
- [x] Configuration (`configs/p0035_tatakua_air_quality.yaml`)
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
make run-paper-0035
# Or directly:
python -m src.papers.p0035_tatakua_air_quality.pipeline
```

## Files

- `../src/papers/p0035_tatakua_air_quality/pipeline.py` — main pipeline
- `../configs/p0035_tatakua_air_quality.yaml` — configuration
- `../notebooks/p0035_tatakua.ipynb` — Jupyter
- `../src/baselines/p0035_tatakua_baselines.py` — baselines
