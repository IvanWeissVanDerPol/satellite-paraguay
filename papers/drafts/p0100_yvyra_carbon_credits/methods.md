# Methods

## Yvyra: Carbon-Credit Verification using Satellite CV + Paraguay

For each Verra VCS-registered carbon project in Paraguay, we (1) download the project geometry; (2) extract Sentinel-2 + AlphaEarth embeddings for the project area; (3) compute biomass proxy using AlphaEarth features + climate + Catastro parcels; (4) compare against claimed carbon credits using Ridge regression baseline + Random Forest; (5) output verification status with confidence score. We validate against 30 ground-truth projects.

## Datasets

See `data/datasheets/` for detailed dataset descriptions.

## Models

See `models/cards/` for foundation model details.

## Code

All code is available in `src/papers/p0100_yvyra_carbon_credits/pipeline.py`.

## Reproducibility

See `src/utils/reproducibility.py` for random seed management + environment capture.

## Ethical Considerations

See `docs/STAKEHOLDERS.md` and per-paper README for ethics review.
