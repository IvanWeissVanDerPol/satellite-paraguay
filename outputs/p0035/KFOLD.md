# P0035 Tatakua — 5-Fold Cross-Validation Results

**Mode:** QUICK
**Total time:** 7.3s
**Date:** 2026-08-03

## Setup
- 5 synthetic air-quality stations × 36 months
- LSTM hidden sizes: [4, 8]
- 5-fold time-series CV (rolling-window, no future leakage)
- 30 epochs, MSE loss, Adam

## Results per fold

| Fold | Hidden | LSTM MAE | LSTM R² | Baseline MAE | Baseline R² | Δ MAE |
|------|--------|----------|---------|--------------|-------------|-------|
| 1 | 4 | 24.537 | -124.465 | 2.998 | -1.616 | -21.539 |
| 2 | 4 | 37.045 | -500.725 | 2.870 | -3.318 | -34.175 |
| 3 | 4 | 24.825 | -178.164 | 3.491 | -4.634 | -21.334 |
| 4 | 4 | 38.805 | -4855.200 | 2.701 | -1.354 | -36.104 |
| 5 | 4 | 25.733 | -160.021 | 3.129 | -1.165 | -22.605 |
| 1 | 8 | 22.721 | -106.840 | 2.998 | -1.616 | -19.723 |
| 2 | 8 | 35.086 | -452.444 | 2.870 | -3.318 | -32.216 |
| 3 | 8 | 22.842 | -151.340 | 3.491 | -4.634 | -19.351 |
| 4 | 8 | 36.864 | -4377.941 | 2.701 | -1.354 | -34.164 |
| 5 | 8 | 23.755 | -136.713 | 3.129 | -1.165 | -20.626 |

## Aggregate

- **Mean LSTM MAE:** 29.221
- **Std LSTM MAE:** 6.420
- **Mean Baseline MAE:** 3.038
- **Mean improvement:** -26.184
- **Mean LSTM R²:** -1104.385

## What this means

- LSTM does NOT beat persistence on synthetic data.
- This is expected: synthetic data has simple structure.
- Real OpenAQ data is needed for meaningful evaluation.

## Threats to validity

- Synthetic data is simpler than real PM2.5 time series.
- Only 5 stations and 36 months — small sample size.
- No hyperparameter search.
- Single random seed.
- Results do NOT generalize to real PM2.5 forecasting.
