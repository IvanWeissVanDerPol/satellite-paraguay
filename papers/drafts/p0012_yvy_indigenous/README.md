# P0012_YVY_INDIGENOUS — Yvy (Indigenous community territory mapping (CARE-compliant))

**Status:** Pipeline scaffolding complete; awaiting real data + training.

## At a glance

- **Title (Guaraní):** **Yvy**
- **Title (English):** Indigenous community territory mapping (CARE-compliant)
- **Title (Spanish):** Cartografía de territorios de comunidades indígenas (cumple CARE)
- **Target journal:** **World Development**
- **Advisor:** Juan Carlos Cristaldo (FADA-UNA) + UN-Habitat partnership
- **Timeline:** 12 weeks
- **Metric:** F1 > 0.80 on conflict detection

## Data sources

Catastro + LLaVA-1.6 + Indigenous territories (free VLM)

## Novelty

First Paraguayan AI thesis on indigenous territories with CARE compliance

## Status checklist

- [x] Pipeline scaffolding (`pipeline.py`)
- [x] Configuration (`configs/p0012_yvy_indigenous.yaml`)
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
make run-paper-0012
# Or directly:
python -m src.papers.p0012_yvy_indigenous.pipeline
```

## Files

- `../src/papers/p0012_yvy_indigenous/pipeline.py` — main pipeline
- `../configs/p0012_yvy_indigenous.yaml` — configuration
- `../notebooks/p0012_yvy.ipynb` — Jupyter
- `../src/baselines/p0012_yvy_baselines.py` — baselines
