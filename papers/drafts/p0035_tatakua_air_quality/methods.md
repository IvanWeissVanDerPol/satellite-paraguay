# Methods

## Tatakua: Air Quality Forecasting for Asunción

We collect 5 years of OpenAQ measurements from Asunción stations. We extract Sentinel-5P atmospheric data (NO2, SO2, CO, O3) for the same period. We use LSTM (2 layers, 128 hidden units) to forecast PM2.5 with horizon 1-7 days. Features: meteorological + spatial + temporal + atmospheric. Baselines: mean forecast, persistence, linear trend. Validate via 5-fold time-series cross-validation.

## Datasets

See `data/datasheets/` for detailed dataset descriptions.

## Models

See `models/cards/` for foundation model details.

## Code

All code is available in `src/papers/p0035_tatakua_air_quality/pipeline.py`.

## Reproducibility

See `src/utils/reproducibility.py` for random seed management + environment capture.

## Ethical Considerations

See `docs/STAKEHOLDERS.md` and per-paper README for ethics review.
