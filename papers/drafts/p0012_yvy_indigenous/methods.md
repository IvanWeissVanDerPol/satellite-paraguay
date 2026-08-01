# Methods

## Yvy: Indigenous Territory Mapping (CARE-Compliant)

We follow CARE Principles: (1) Collective Benefit — communities get CC-BY atlas; (2) Authority to Control — INDI + community review before publication; (3) Responsibility — annual report to communities; (4) Ethics — cultural review board. Technically, we use LLaVA-1.6 to extract native-language place names from satellite imagery + OpenStreetMap + Catastro + Indigenous territories. Conflict detection: intersection of Catastro parcels with indigenous territories. We validate with 5 community-engaged ground-truth projects.

## Datasets

See `data/datasheets/` for detailed dataset descriptions.

## Models

See `models/cards/` for foundation model details.

## Code

All code is available in `src/papers/p0012_yvy_indigenous/pipeline.py`.

## Reproducibility

See `src/utils/reproducibility.py` for random seed management + environment capture.

## Ethical Considerations

See `docs/STAKEHOLDERS.md` and per-paper README for ethics review.
