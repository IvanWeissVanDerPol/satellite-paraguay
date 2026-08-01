# P0026_KAI_POACHING — Kai (Wildlife poaching detection (YOLOv8 + COCO-zoo transfer))

**Status:** Pipeline scaffolding complete; awaiting real data + training.

## At a glance

- **Title (Guaraní):** **Kai**
- **Title (English):** Wildlife poaching detection (YOLOv8 + COCO-zoo transfer)
- **Title (Spanish):** Detección de caza furtiva (YOLOv8 + transferencia COCO)
- **Target journal:** **Conservation Biology**
- **Advisor:** Multi (FCM + WWF Paraguay + Guyra)
- **Timeline:** 10 weeks
- **Metric:** mAP@0.5 > 0.70 on poaching camp detection

## Data sources

YOLOv8 + COCO-zoo transfer + NASA FIRMS

## Novelty

First Paraguayan AI thesis on poaching detection

## Status checklist

- [x] Pipeline scaffolding (`pipeline.py`)
- [x] Configuration (`configs/p0026_kai_poaching.yaml`)
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
make run-paper-0026
# Or directly:
python -m src.papers.p0026_kai_poaching.pipeline
```

## Files

- `../src/papers/p0026_kai_poaching/pipeline.py` — main pipeline
- `../configs/p0026_kai_poaching.yaml` — configuration
- `../notebooks/p0026_kai.ipynb` — Jupyter
- `../src/baselines/p0026_kai_baselines.py` — baselines
