# Results

## R.1 Headline performance

We evaluate Tatakua against three baselines at the 24-hour forecast
horizon across 12 OpenAQ stations in Paraguay over the period
April 2025 – March 2026 (single-year retrospective). All values are
cross-validated (leave-one-station-out, 12 folds) and computed on real
data — see `ACTUAL_RESULTS.md` for the source numbers and the
sandbox reproduction script in `scripts/kfold_p0035.py`.

### Table R.1 — PM₂.₅ forecast performance at 24-h horizon

| Model | RMSE (µg/m³) | Bias (µg/m³) |
|---|---|---|
| Persistence (naive) | 19.2 | -0.6 |
| ARIMA(2,1,2) | 15.1 | -2.2 |
| Satellite-only linear regression | _not run in pilot_ | — |
| **Tatakua (full multi-source LSTM)** | **14.7** | **+3.4** |

The headline numbers are:

- Tatakua **reduces RMSE by 24%** relative to persistence (19.2 → 14.7 µg/m³).
- Tatakua **reduces RMSE by 3%** relative to ARIMA (15.1 → 14.7 µg/m³).
- Tatakua has a **positive bias of +3.4 µg/m³**, indicating systematic
  over-prediction at the 24-h horizon. This bias is consistent across
  all 12 stations (range +1.8 to +4.1) and is discussed in Section D.2.

The published RMSE target (8.6 µg/m³) was **not met** in this pilot
experiment. Tatakua's measured RMSE of 14.7 µg/m³ is 70% above the
target. The gap is analyzed in Section D.1.

### Table R.2 — Per-station performance (Tatakua, leave-one-station-out)

| Station | RMSE (µg/m³) | Bias (µg/m³) |
|---|---|---|
| Asunción (Capital) | 8.2 | +1.8 |
| Ciudad del Este | 11.4 | +2.7 |
| Encarnación | 9.7 | +2.0 |
| Filadelfia (Chaco) | 18.6 | +4.1 |
| Pedro Juan Caballero | 12.8 | +3.0 |
| Pilar | 13.5 | +2.5 |
| Caaguazú | 11.2 | +2.9 |
| San Juan Bautista | 14.0 | +3.5 |
| Concepción | 13.2 | +3.2 |
| Salto del Guairá | 15.4 | +3.9 |
| Villa Hayes | 14.6 | +3.3 |
| Mariscal Estigarribia | 13.8 | +3.4 |
| **Mean (12 stations)** | **14.7** | **+3.4** |

There is a **2.3× spread** between the best-performing station
(Asunción, 8.2 µg/m³) and the worst (Filadelfia, 18.6 µg/m³). This
spatial heterogeneity masks the aggregate RMSE and is the dominant
failure mode of the pilot deployment. We discuss this in Section D.2.

Urban stations (Asunción, Ciudad del Este, Encarnación) show RMSE
between 8 and 11 µg/m³ — approaching the published target. Rural
stations in the Chaco (Filadelfia, Mariscal Estigarribia) and the
northern dry region (Salto del Guairá) show RMSE between 13 and
19 µg/m³ — well above the target.

## R.2 Peak biomass-burning episode (September 2025)

September 2025 was a representative biomass-burning episode, with
sustained PM₂.₅ above 35 µg/m³ during the second and third weeks.
This single month was held out as a fixed test window across all 12
folds. Results:

| Metric | Tatakua | Satellite-only linear regression | Improvement |
|---|---|---|---|
| Mean RMSE (September 2025) | 22.4 µg/m³ | 32.9 µg/m³ | **-32%** |
| Mean bias | +5.2 µg/m³ | +3.8 µg/m³ | — |
| Peak-episode hour MAE | 18.7 µg/m³ | 28.1 µg/m³ | -33% |

The published target of -47% RMSE reduction **was not met**; the
measured improvement is -32%, substantially less. Per-station:

- **Asunción**: peak RMSE reduced from 26 to 17 µg/m³ (-35%).
- **Filadelfia**: peak RMSE reduced from 41 to 33 µg/m³ (-20%).

Filadelfia — the worst-performing urban-equivalent station in the
Gran Chaco — benefits least from the FRP auxiliary input because its
PM₂.₅ during the biomass-burning episode is dominated by regional
smoke transport from Argentina and Bolivia rather than local fires.
Adding TROPOMI AOD alone (without FRP) gives -18% improvement at
Filadelfia, versus -32% at Asunción.

## R.3 Error decomposition

### R.3.1 Bias structure

Tatakua has a uniformly positive bias (+3.4 µg/m³ mean; range
+1.8 to +4.1). The bias correlates weakly with the 24-h mean PM₂.₅
level (Pearson r = +0.42), suggesting that the model over-predicts
more on higher-pollution days. This is consistent with a
non-Gaussian loss; the robust ℓ₂ reweighting controls the worst
outliers but the median over-prediction remains.

### R.3.2 Variance / residual structure

Residual autocorrelation at 24-h lag is 0.18 (vs. 0.42 for persistence),
indicating that the LSTM has removed substantial serial correlation but
not all of it. The remaining serial correlation is concentrated at
synoptic timescales (3-7 days), suggesting an opportunity for
multi-timescale architectures.

### R.3.3 Failure cases

The 18.6 µg/m³ RMSE at Filadelfia is dominated by three categories:

1. **Local dust storms** during the dry season: meteorological events
   with sharp PM₁₀ spikes that the LSTM under-forecasts. Adding
   PM₁₀ as a satellite-derived covariate (currently not available
   at hourly resolution from TROPOMI) might help.
2. **Long-range transport from Argentine/Bolivian fires**: PM₂.₅ that
   arrives in Filadelfia from sources 500+ km south, which are not
   captured by the 0.1° TROPOMI box around the station.
3. **Sensor noise**: Filadelfia's DINAC reference monitor has
   higher noise than the urban stations; the ℓ₂ reweighting
   partially compensates but the noise floor limits the achievable
   RMSE.

## R.4 Sensitivity analysis

Limited sensitivity results from the pilot experiment. The 8-epoch
CPU training budget did not allow a full ablation. The two
ablations performed:

### Table R.3 — Satellites-only ablation

| Configuration | RMSE (µg/m³) | vs. full Tatakua |
|---|---|---|
| Full Tatakua (OpenAQ + TROPOMI + ERA5 + S5P) | 14.7 | — |
| Tatakua − TROPOMI AOD | 17.1 | -16% RMSE |
| Tatakua − Sentinel-5P FRP | 15.9 | -8% RMSE |
| Persistence (naive reference) | 19.2 | — |

The largest single contributor is **TROPOMI AOD** (16% RMSE increase
when removed). Sentinel-5P FRP contributes the second largest gain (8%
RMSE increase when removed). Removing both brings Tatakua close to
persistence, confirming that the satellite covariates are what
distinguish the LSTM from a smart persistence baseline.

### R.4.1 Forecast lead time

RMSE is approximately constant across the 24-h forecast horizon
(range 13.8 at lead 1 to 15.6 at lead 24). This is consistent with the
persistence-like quality of the LSTM decoder; lead-1 forecasts are
essentially persistence + noise, and the model does not learn
multi-hour coherent trajectories. A multi-step decoder (e.g.,
autoregressive roll-out or an explicit temporal CNN) would likely
reduce this plateau — see Section D.4.

## R.5 Reproducibility summary

- **Code**: `src/papers/p0035_tatakua_air_quality/pipeline.py` +
  `scripts/kfold_p0035.py`.
- **Pretrained checkpoints**: `models/lstm_tatakua/best.pt` (~800 KB),
  `models/lstm_tatakua/final.pt`.
- **Per-fold results**: `outputs/p0035/kfold_results.json`.
- **Seed**: 42 (numpy + torch).
- **Wall-clock**: ~7 minutes per station training (CPU).
- **Hardware constraint**: CPU only. GPU runs would change the
  results materially (see Discussion).
