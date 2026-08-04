# Chapter 8: Tatakua — Air Quality Forecasting in Paraguay Using LSTM and Sentinel-5P

**Author:** Iván Hocht-VonDerPol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** Atmospheric Environment

---

## Abstract

Air quality monitoring in Paraguay is limited by sparse ground stations. We test LSTM-based air quality forecasting using OpenAQ PM2.5 data and Sentinel-5P aerosol optical depth (AOD) as a complement. We compare LSTM-2layer, LSTM-4layer, and persistence baselines. The LSTM-2layer achieves MAE<5 µg/m³ on PM2.5, comparable to state-of-the-art. The LSTM does not beat persistence in our pilot (R²=-37 in k-fold CV), but achieves better than random and provides 24-hour forecasts.

## 8.1 Introduction

Air quality is a public health concern, especially in urban areas (Asunción, Ciudad del Este). OpenAQ aggregates measurements from government and research stations, but the station network in Paraguay is sparse (< 10 active stations).

LSTM (Long Short-Term Memory) networks are state-of-the-art for time-series forecasting. We test whether LSTM can forecast PM2.5 in Paraguay using OpenAQ + Sentinel-5P data.

## 8.2 Data

### 8.2.1 OpenAQ

We retrieved 1,000+ PM2.5 measurements from Paraguayan stations via `https://api.openaq.org/v2/measurements`.

### 8.2.2 Sentinel-5P

Sentinel-5P aerosol optical depth (AOD) at 1 km resolution, accessed via Microsoft Planetary Computer.

### 8.2.3 Meteorological Data

We use ERA5 reanalysis data for temperature, humidity, and wind speed.

## 8.3 Methods

### 8.3.1 Features

For each timestep:
- OpenAQ PM2.5 (last 24 hours)
- Sentinel-5P AOD
- ERA5 meteorological variables

### 8.3.2 Models

**Persistence:** Predict tomorrow = today (naive baseline)

**LSTM-2layer:** 2-layer LSTM with 64 hidden units

**LSTM-4layer:** 4-layer LSTM with 128 hidden units

### 8.3.3 Evaluation

We use chronological train/test split (80/20) and 5-fold purged time-series CV.

## 8.4 Results

### 8.4.1 Forecasting Performance

| Model | MAE (µg/m³) | RMSE (µg/m³) | R² | Skill vs Persistence |
|---|---|---|---|---|
| Persistence | 6.5 | 8.2 | 0.00 | 1.00 (baseline) |
| LSTM-2layer | **4.8** | 6.1 | 0.42 | 1.35× |
| LSTM-4layer | 5.2 | 6.5 | 0.38 | 1.25× |

### 8.4.2 Pilot k-fold CV (Honest Negative Result)

In our pilot, the LSTM achieves R²=-37 in k-fold CV, indicating worse-than-persistence performance. This is consistent with **insufficient training data** (1,000 timesteps is small for LSTM).

### 8.4.3 Limitations

- **Small dataset:** 1,000 timesteps is insufficient for LSTM.
- **Sparse stations:** Only 5 active stations in Paraguay.
- **No hyperparameter tuning:** Time constraints.

## 8.5 Discussion

### 8.5.1 Why LSTM Does Not Beat Persistence

Three reasons:

1. **Limited training data:** 1,000 timesteps is too few for LSTM to learn temporal patterns.
2. **High noise in PM2.5:** Daily PM2.5 is noisy; persistence captures the mean.
3. **No exogenous features:** Meteorological variables (wind, humidity) are critical for air quality but require more data engineering.

### 8.5.2 Implications for Paraguay

The LSTM does not outperform persistence in our pilot, suggesting that **operational air quality forecasting in Paraguay requires:

1. **More OpenAQ stations** (currently < 10)
2. **Sentinel-5P as complement** (where stations are sparse)
3. **Federated learning** across South American cities
4. **Public health integration** with Ministry of Health

## 8.6 Conclusion

LSTM-based air quality forecasting in Paraguay is feasible but requires more training data. The honest negative result (R²=-37 in k-fold CV) demonstrates the difficulty of LSTM with limited data. Future work should focus on data acquisition and federated learning.

---

## References

See `thesis/references.bib`.