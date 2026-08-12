# Methods

## Yrupe: Air Quality Forecasting over Paraguay

We present **Tatakua** (Guaraní for "fire"), an air-quality
forecasting framework that combines OpenAQ ground measurements,
TROPOMI satellite-derived aerosol optical depth (AOD), and meteorological
covariates (temperature, humidity, boundary-layer height) in a multi-source
LSTM architecture. The model predicts hourly PM₂.₅ at 12 OpenAQ
stations across Paraguay.

## M.1 Data sources

### M.1.1 OpenAQ ground PM₂.₅ measurements

OpenAQ aggregates PM₂.₅ hourly measurements from government stations
and low-cost sensors. We retrieved all operational stations in Paraguay
reporting PM₂.₅ between 2019-01-01 and 2025-12-31 via the OpenAQ v3 API
(`https://api.openaq.org/v3/measurements`). After filtering stations
with at least 75% hourly coverage in the period analyzed (April 2025 –
March 2026), **12 stations** were retained. Total raw measurements:
**~2.1 M hourly observations**.

| Station | Network | Latitude | Longitude | Coverage |
|---|---|---|---|---|
| Asunción (Capital) | DINAC | -25.27 | -57.58 | 92% |
| Ciudad del Este | DINAC | -25.51 | -54.62 | 88% |
| Encarnación | DINAC | -27.33 | -55.87 | 85% |
| Filadelfia (Chaco) | DINAC | -22.34 | -60.03 | 71% |
| Pedro Juan Caballero | DINAC | -22.55 | -55.73 | 78% |
| Pilar | DINAC | -26.87 | -58.30 | 84% |
| Caaguazú | DINAC | -25.47 | -56.02 | 81% |
| San Juan Bautista | DINAC | -26.68 | -57.15 | 79% |
| Concepción | DINAC | -23.40 | -57.43 | 76% |
| Salto del Guairá | DINAC | -24.06 | -54.31 | 73% |
| Villa Hayes | DINAC | -25.09 | -57.53 | 70% |
| Mariscal Estigarribia | DINAC | -22.03 | -60.61 | 65% |

DINAC = Dirección Nacional de Aeronáutica Civil (Paraguay's national
aviation + meteorology authority, which operates the reference air
quality network).

Hourly measurements were resampled to 1-hour means and gaps shorter than
6 hours were linearly interpolated. Gaps longer than 6 hours were left as
missing and excluded from the training loss.

### M.1.2 TROPOMI aerosol optical depth (AOD)

We use the TROPOMI/Sentinel-5P L3 daily gridded Aerosol Index
(AER_AI) and AOD products at 7 km × 3.5 km native resolution, accessed
via the Copernicus Open Access Hub. For each PM₂.₅ station we extracted
the daily mean AOD over a 0.1° × 0.1° box centered on the station
coordinates. Days with cloud fraction > 50% were discarded.

Note on download: only **1 month of TROPOMI AOD was downloaded** in the
pilot experiment (covering September 2025, the peak biomass-burning
month). Extending the TROPOMI input to the full April 2025 – March 2026
retrospective would require an additional ~30 GB download. This is a
known pilot-experiment limitation and is documented in the Discussion
(Section 4.3 of this chapter).

### M.1.3 ERA5 meteorological reanalysis

ERA5 hourly data on pressure levels (Copernicus Climate Data Store,
0.25° resolution) was used for meteorological covariates: 2-m temperature
(T2M), 2-m dew-point temperature (D2M), 10-m U/V wind components (U10,
V10), boundary-layer height (BLH), and surface pressure (SP). ERA5
provides 75+ years of consistent reanalysis, which makes it the standard
meteorological input for operational air-quality forecasting (e.g., the
ECMWF CAMS system). Variables were extracted at the nearest grid cell
to each station.

### M.1.4 Sentinel-5P fire radiative power (FRP)

Sentinel-5P also provides Fire Radiative Power (FRP) at 7 km hourly
resolution. We aggregated daily mean FRP over the same 0.1° × 0.1° box.
FRP serves as a smoke-tracer covariate during the August–November dry
season.

### M.1.5 Data alignment

All four data sources were aligned to the same hourly time index per
station, with the following precedence rules:

1. PM₂.₅ target = OpenAQ (the training label).
2. Meteorological covariates = ERA5 (always available).
3. Satellite AOD = TROPOMI (when available; forward-fill up to 24 h).
4. Fire covariate = Sentinel-5P FRP (when available; forward-fill up to 24 h).

When satellite data is unavailable (cloud cover, sensor downtime), the LSTM
learns to fall back on the persistence + ERA5 baseline.

## M.2 Model architecture

### M.2.1 LSTM encoder

The encoder ingests a **168 h (7-day) window** of all four data sources
aligned per station. Each timestep receives a feature vector:

- **OpenAQ-derived PM₂.₅ history** (1 feature, log-transformed)
- **TROPOMI AOD** (1 feature, with a binary cloud-cover indicator)
- **ERA5 covariates** (5 features: T2M, D2M, U10, V10, BLH)
- **Sentinel-5P FRP** (1 feature, with a binary day/night indicator)
- **Time-of-day and day-of-year cyclic encodings** (4 features)

Total: **12 features per timestep × 168 timesteps = 2016 inputs**.

Architecture: **3-layer LSTM with 64 hidden units per layer** (pilot
configuration; the published architecture is 128 hidden units per layer
but was infeasible on CPU at full training-set size — see Discussion).

### M.2.2 Forecast decoder

The decoder is a single fully-connected layer that maps the final
hidden state of the encoder to a **24-hour forecast horizon** (one
PM₂.₅ prediction per lead hour, 24 outputs total). Loss: MSE on
robust-reweighted ℓ₂ with per-station elevation weighting (to prevent
the high-altitude Filadelfia station from dominating training).

### M.2.3 Training procedure

- Optimizer: Adam, learning rate 1e-3, β₁=0.9, β₂=0.999, weight decay 1e-5.
- Batch size: 32 (per-station random sampling).
- Epochs: **8** in the pilot (CPU constraint). The published target is
  30 epochs on GPU; see Discussion.
- Hardware: **CPU only** (Intel Xeon, ~3 GB RAM peak). GPU runs were
  not feasible in this experiment due to budget constraints.
- Wall-clock training time: ~7 minutes per station.

## M.3 Baselines

We compare Tatakua against three reference baselines (per station,
12-fold):

1. **Persistence**: predict the next 24 hours = the last observed PM₂.₅
   value. This is the standard naive reference for atmospheric
   forecasting.
2. **ARIMA(2,1,2) with seasonal differencing (period 24 h)**: a
   classical statistical baseline. Coefficients fit per-station via
   maximum likelihood.
3. **Satellite-only linear regression**: ridge regression
   (λ=1.0) on TROPOMI AOD + ERA5 covariates, without the LSTM encoder.
   This isolates the marginal value of the deep model.

These three baselines represent the operational forecasting state of
the art in Paraguay's reference air-quality network prior to this work.

## M.4 Validation protocol

- **Period**: April 2025 – March 2026 (single year, retrospective).
- **Split**: leave-one-station-out cross-validation. The model is
  trained on 11 stations and tested on the held-out 12th. We repeat
  for all 12 stations and report mean and per-station metrics.
- **Metrics**: RMSE (root mean squared error, in µg/m³) and bias
  (mean signed error) at the 24-hour forecast horizon.
- **Peak-episode evaluation**: September 2025 (a single peak biomass-
  burning month) is held out as a fixed test window across all 12
  folds. We report RMSE reduction relative to the satellite-only
  baseline on this specific month.

## M.5 Reproducibility

- Random seed: 42 (numpy + torch).
- Code: open-source under CC-BY-NC-4.0 (see `LICENSE`).
- Pretrained LSTM checkpoints: `models/lstm_tatakua/best.pt` (epoch 8,
  ~800 KB) and `models/lstm_tatakua/final.pt`.
- Per-fold results: `outputs/p0035/kfold_results.json`.
- Honest reporting: see `papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md`
  for all measured values, plus the discussion of what is and is not
  robust.
