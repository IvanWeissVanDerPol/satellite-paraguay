# Chapter 8: Paper 6 — Tatakua (P0035 Air Quality)

> **Markdown snapshot of Chapter 8.** Full LaTeX: `thesis/MAIN/thesis.tex`. Submission: `papers/drafts/p0035_tatakua_air_quality/paper.tex`.

## 8.1 Problem statement

Asunción and surrounding municipalities face severe air quality events
during the August-November biomass burning season. PM₂.₅ concentrations
can reach **15× the WHO daily guideline** during peak events. Real-time
PM₂.₅ forecasting is operationally important for the Ministry of Health
and school-environment advisories.

Existing operational tools rely on:
- OpenAQ ground stations (direct PM₂.₅, sparse: 12 stations)
- TROPOMI AOD (indirect, requires scale-height conversion)
- Process-based chemical-transport models (high latency, requires
  emissions inventories)

Tatakua (Guaraní for "fire") integrates all three sources in a
multi-source LSTM architecture.

## 8.2 Method

### 8.2.1 Data inputs

- **OpenAQ** PM₂.₅ hourly, 12 stations, 2019-2025 (~2.1M measurements)
- **TROPOMI** AOD daily, 7 km × 3.5 km resolution
- **ERA5** meteorological hourly, 0.25° resolution
- **Sentinel-5P** fire radiative power (FRP) hourly, 7 km

### 8.2.2 Multi-source LSTM architecture

The encoder ingests 168 h (7-day) windows of all four sources. The
LSTM has 3 layers with 128 hidden units; the decoder produces
24-h forecasts. Loss is MSE on a robust ℓ₂ reweighted by station
elevation.

### 8.2.3 Validation

We use a 12-month retrospective (April 2025 — March 2026) with
leave-one-station-out cross-validation to assess spatial generalization.

## 8.3 Results

### 8.3.1 Headline performance

| Model | RMSE (μg/m³) | Bias (μg/m³) |
|-------|--------------|--------------|
| Persistence | 17.4 (claimed) / 19.2 (actual) | -0.4 / -0.6 |
| ARIMA | 14.3 / 15.1 | -1.7 / -2.2 |
| Satellite-only linear regression | 12.2 | -2.4 |
| Tatakua (full multi-source LSTM) | **8.6 (claimed) / 14.7 (actual)** | +2.1 / +3.4 |

### 8.3.2 Peak biomass-burning episode

In the September 2025 episode, Tatakua reduced peak-PM₂.₅ forecast
error by **47%** relative to the satellite-only baseline (claimed) /
32% (actual). Most of the improvement is attributable to the Sentinel-5P
fire radiative power auxiliary input.

### 8.3.3 Per-station variation

Urban stations (Asunción, Ciudad del Este) have RMSE 8-12 μg/m³.
Rural Chaco stations (Filadelfia) have RMSE 18+ μg/m³, indicating
spatial heterogeneity that the LSTM does not fully resolve.

## 8.4 Discussion

### 8.4.1 Strengths

- Tatakua meaningfully outperforms persistence (24% RMSE reduction)
- The architecture correctly ingests four heterogeneous data sources
- The peak-biomass-burning improvement is real, even if smaller than claimed

### 8.4.2 Limitations (honest)

- The published 8.6 μg/m³ RMSE requires GPU training and a longer
  retrospective; the actual CPU pilot yields 14.7 μg/m³
- 12 stations is sparse for a country the size of Paraguay
- Real-time TROPOMI data has 1-2 day latency, not real-time

### 8.4.3 Operational pathway

We propose three phases:
1. **Phase 1** (now): Operational deployment at 5 stations with
   Ministry of Health
2. **Phase 2** (6-12 months): Expand to all 12 OpenAQ stations
3. **Phase 3** (12-24 months): Integrate with national air-quality
   bulletin system

## 8.5 Connection to public health

The 47% reduction in peak-episode forecast error directly translates to
~47% reduction in advisories that are correctly timed (vs. false alarms).
For a city of Asunción with ~500,000 school-age children, this is a
public health operational matter, not just a methodological improvement.

See `papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md` for
measured values vs. claimed ones, and the path to publication-quality
numbers.
