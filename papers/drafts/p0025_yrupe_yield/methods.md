# Methods

## Yrupe: Soybean Yield Prediction using Sentinel-2 + INBIO

We download 5 years of Sentinel-2 for Caaguazú (10m). We delineate individual field boundaries using Delineate Anything v2. For each field, we extract monthly NDVI/EVI composites (12 timesteps/year). We train a GRU with embeddings + weather features to predict yield (tons/hectare). We validate against held-out INBIO records.

## Datasets

See `data/datasheets/` for detailed dataset descriptions.

## Models

See `models/cards/` for foundation model details.

## Code

All code is available in `src/papers/p0025_yrupe_yield/pipeline.py`.

## Reproducibility

See `src/utils/reproducibility.py` for random seed management + environment capture.

## Ethical Considerations

See `docs/STAKEHOLDERS.md` and per-paper README for ethics review.
