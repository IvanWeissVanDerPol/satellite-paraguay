# P0011_YVYTU_DEFORESTATION — Yvytu (Multi-temporal satellite CV for Chaco deforestation alert system)

**Status:** Pipeline scaffolding complete; awaiting real data + training.

## At a glance

- **Title (Guaraní):** **Yvytu**
- **Title (English):** Multi-temporal satellite CV for Chaco deforestation alert system
- **Title (Spanish):** Sistema de alerta de deforestación del Chaco con visión por computadora satelital multi-temporal
- **Target journal:** **Remote Sensing of Environment**
- **Advisor:** Juan Carlos Cristaldo (FADA-UNA)
- **Timeline:** 12 weeks
- **Metric:** F1 macro > 0.85 on deforestation detection

## Data sources

Sentinel-2 + MapBiomas Paraguay + Hansen GFC + Prithvi foundation model

## Novelty

First Paraguayan AI thesis on Chaco deforestation using foundation models

## Status checklist

- [x] Pipeline scaffolding (`pipeline.py`)
- [x] Configuration (`configs/p0011_yvytu_deforestation.yaml`)
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
make run-paper-0011
# Or directly:
python -m src.papers.p0011_yvytu_deforestation.pipeline
```

## Files

- `../src/papers/p0011_yvytu_deforestation/pipeline.py` — main pipeline
- `../configs/p0011_yvytu_deforestation.yaml` — configuration
- `../notebooks/p0011_yvytu.ipynb` — Jupyter
- `../src/baselines/p0011_yvytu_baselines.py` — baselines
