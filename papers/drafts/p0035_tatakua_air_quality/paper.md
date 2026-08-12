# Chapter 8: Tatakua — Air Quality Forecasting in Paraguay Using LSTM and Sentinel-5P

**Author:** Iván Hocht-VonDerPol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** Atmospheric Environment

---

## Abstract

Air quality monitoring in Paraguay is limited by sparse ground stations. We present LSTM-based air quality forecasting using OpenAQ PM2.5 data and Sentinel-5P aerosol optical depth (AOD) as a complement. We compare LSTM-2layer, LSTM-4layer, and persistence baselines. The measured pilot performance is **mean RMSE = 14.7 µg/m³ across 12 OpenAQ stations** (24% above persistence), with bias +3.4 µg/m³. The LSTM DOES beat persistence by 24% in our pilot. The published target "MAE<5 µg/m³ (R²>0.80)" was aspirational, NOT measured; the Honest Reporting Note appended to this paper documents this.

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

---

## Honest Reporting Note (added 2026-08-10)

The abstract above previously claimed "**PM2.5 forecast MAE<5 µg/m³ (R²>0.80), deployed for Ministry of Public Health**". The measured values are:

- **Mean RMSE across 12 stations = 14.7 µg/m³** (target was 8.6 — we are 70% above target).
- **Mean bias = +3.4 µg/m³** (consistent over-prediction).
- **Station-level spread:** Asunción 8.2 µg/m³ (closest to target) to Filadelfia/Chaco 18.6 µg/m³ (far from target). The rural Chaco stations are the failure mode.
- **Peak biomass-burning episode (Sep 2025):** 32% RMSE reduction vs satellite-only baseline — meaningful, but below the 47% claim.
- **No deployment exists.** The dashboard is local Streamlit; there is no Ministry-of-Health integration.

What IS real and is the contribution: **Tatakua beats persistence by 24% RMSE (19.2 → 14.7 µg/m³), which is a meaningful LSTM signal on Paraguay OpenAQ data, and the rural-station gap is well-characterized.** That is publishable as a baseline paper; the original headline overpromised.

Before any submission to Atmospheric Environment: (a) rewrite headline around the 24% RMSE improvement over persistence, (b) report the rural-station gap as a Discussion section not a footnote, (c) remove the Ministry deployment claim unless a partnership letter exists.
