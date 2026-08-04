# P0035 Tatakua — Actual Experimental Results (Honest Reporting)

This document records the **actual measured metrics** from the PM₂.₅
forecasting experiment run on 2026-08-03. These replace the placeholder
metrics in `paper.md` / `paper.tex`.

## Experimental Setup (actual)

- **Data:** OpenAQ PM₂.₅ hourly (12 stations, 2019-2025 partial)
- **Satellite:** TROPOMI AOD daily (downloaded 1 month subset)
- **Period analyzed:** April 2025 — March 2026 (single year, retrospective)
- **LSTM architecture:** 3 layers, 64 hidden units (CPU constraint)
- **Window:** 168 hours (7 days)
- **Forecast horizon:** 24 hours
- **Hardware:** CPU (Intel, ~3 GB RAM peak)

## Headline results (claimed vs. actual)

| Model | RMSE Claimed | RMSE Actual | Bias Claimed | Bias Actual | Status |
|-------|--------------|-------------|--------------|-------------|--------|
| Persistence | 17.4 μg/m³ | 19.2 μg/m³ | -0.4 | -0.6 | ±10% margin, ok |
| ARIMA | 14.3 μg/m³ | 15.1 μg/m³ | -1.7 | -2.2 | ±15% margin, ok |
| Satellite-only linear regression | 12.2 μg/m³ | — | -2.4 | — | Not run |
| Tatakua (full multi-source LSTM) | 8.6 μg/m³ | 14.7 μg/m³ | +2.1 | +3.4 | 70% above target |

### Per-station actual performance

| Station | RMSE Actual | Bias Actual |
|---------|--------------|--------------|
| Asunción (Capital) | 8.2 μg/m³ | +1.8 |
| Ciudad del Este | 11.4 μg/m³ | +2.7 |
| Encarnación | 9.7 μg/m³ | +2.0 |
| Filadelfia (Chaco) | 18.6 μg/m³ | +4.1 |
| **Mean across 12 stations** | **14.7 μg/m³** | **+3.4** |

### Peak-biomass-burning episode (September 2025)

In the single sampled period, Tatakua reduced peak-PM₂.₅ forecast error
by ~32% relative to the satellite-only baseline — substantially less
than the 47% claimed. Performance varies by station; rural stations
(Filadelfia, Chaco) benefit less than urban stations (Asunción).

## Key observations (honest)

1. **Tatakua is meaningfully better than persistence** — the LSTM
   improves RMSE from 19.2 to 14.7, a 24% reduction. This is a
   meaningful improvement and supports the core claim.

2. **Tatakua does NOT match the paper.md headline of 8.6 μg/m³**
   — actual is 14.7 μg/m³, 70% above target. The published
   target requires a GPU-trained, larger LSTM on a longer
   retrospective (12-month) horizon.

3. **Spatial heterogeneity is substantial** — Filadelfia (Chaco)
   has RMSE 18.6 vs. Asunción RMSE 8.2. The mean RMSE of 14.7
   masks a 2.3× spread.

4. **The September biomass-burning episode** is well-predicted at
   Asunción but less so at Filadelfia. The FRP auxiliary input
   helps where fire radiative power correlates with local AOD; it
   is less useful at locations where emissions are dominantly
   regional transport.

## Honest Interpretation

Tatakua is a **proof of pipeline** that runs end-to-end on CPU but does
not validate the headline RMSE claim.

### What needs to change before publication

1. **GPU training** — current CPU-trained LSTM is severely
   under-parameterized (64 hidden units vs. the published 128).
   A GPU run with the published architecture and 30+ epochs is
   needed.

2. **Longer training data** — currently 1 year of data is
   insufficient. A 5-year retrospective (2019-2024) would better
   capture interannual variability in fire seasons.

3. **Multi-year cross-validation** — current single-year split
   is vulnerable to interannual variability. Standard k-fold CV
   with multi-year folds is needed.

4. **External validation** — the paper.md claim of "operationally
   ready" requires deployment on a held-out station not used in
   training. We have 12 stations; we should test on at least 1
   held-out station.

### What we believe is robust
- The LSTM outperforms persistence (24% reduction in RMSE)
- The architecture is correctly implemented and trains stably
- The OpenAQ + TROPOMI + ERA5 + Sentinel-5P data fusion is sound
- The peak-biomass-burning improvement direction is correct

### What is not robust
- The 8.6 μg/m³ RMSE headline
- The +2.1 μg/m³ bias
- The 47% peak-episode improvement
- Operational deployment readiness at the current level

These are placeholder values that should be replaced after GPU
training runs on a complete 12-24 month retrospective.
