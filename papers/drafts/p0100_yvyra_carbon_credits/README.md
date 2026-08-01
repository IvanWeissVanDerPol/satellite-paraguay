# P0100_YVYRA_CARBON_CREDITS — Yvyra (Carbon-credit verification (satellite CV + Paraguay farms))

**Status:** Pipeline scaffolding complete; awaiting real data + training.

## At a glance

- **Title (Guaraní):** **Yvyra**
- **Title (English):** Carbon-credit verification (satellite CV + Paraguay farms)
- **Title (Spanish):** Verificación de créditos de carbono (visión satelital + granjas de Paraguay)
- **Target journal:** **Nature Climate Change**
- **Advisor:** Juan Carlos Cristaldo (FADA-UNA) + INFONA partnership
- **Timeline:** 12 weeks
- **Metric:** R² > 0.82 on carbon stock estimation (matching AlphaEarth benchmark)

## Data sources

Sentinel-2 + Verra VCS API + Gold Standard + AlphaEarth foundation model

## Novelty

First Paraguayan AI thesis on carbon credit verification

## Status checklist

- [x] Pipeline scaffolding (`pipeline.py`)
- [x] Configuration (`configs/p0100_yvyra_carbon_credits.yaml`)
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
make run-paper-0100
# Or directly:
python -m src.papers.p0100_yvyra_carbon_credits.pipeline
```

## Files

- `../src/papers/p0100_yvyra_carbon_credits/pipeline.py` — main pipeline
- `../configs/p0100_yvyra_carbon_credits.yaml` — configuration
- `../notebooks/p0100_yvyra.ipynb` — Jupyter
- `../src/baselines/p0100_yvyra_baselines.py` — baselines
