# Model Card — TimesFM

**Model:** TimesFM (Google Research)
**License:** Apache 2.0
**GitHub:** https://github.com/google-research/time-series-foundation-model
**Used in:** P0035 Tatakua (PM2.5 forecast baseline)

## Model details

- **Architecture:** Decoder-only transformer (200M params)
- **Input:** 512-token time series context
- **Output:** Up to 128-step forecast horizon
- **Pre-training:** 100B+ time points from various domains

## Intended use

- Zero-shot time series forecasting
- Probabilistic forecasts
- Multiple domains: energy, traffic, weather, finance, biology

## Training data

- **Pre-training:** Google Trends, Wiki visits, traffic, energy, etc.
- **No fine-tuning required** (zero-shot)

## Evaluation

- **MSE on Monash benchmarks:** competitive with full-supervision models
- **Energy forecasting:** beats LSTM baselines
- **Weather:** comparable to dedicated models

## Limitations

- 512-token context limit
- 128-token forecast horizon
- Pre-training on mostly Western data
- Not designed for distribution shift

## Ethical considerations

- Public/Apache 2.0
- Used for: forecasting, planning, anomaly detection
- Should not be used for: critical decisions without verification

## Why TimesFM for P0035?

- **Zero-shot:** no training needed initially
- **Speed:** inference in milliseconds
- **Multi-modal:** handles PM2.5 + NO2 + O3 inputs

## Citation

```bibtex
@misc{timesfm2024,
  title={TimesFM: A Decoder-Only Foundation Model for Time-Series Forecasting},
  author={Das, Abhimanyu and Kong, Weihao and Sen, Raj and Zhou, Yue},
  year={2024},
  archiveprefix={arXiv},
  eprint={2310.10688}
}
```
