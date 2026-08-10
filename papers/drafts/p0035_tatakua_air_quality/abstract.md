# Abstract

## Tatakua: Air Quality Forecasting for Asunción

We present Tatakua, a deep-learning-based air-quality forecasting system for Paraguay. Tatakua uses OpenAQ PM₂.₅ hourly measurements (12 stations, 2019-2025), TROPOMI AOD, and an LSTM (3 layers × 64 hidden units) with a 168-hour window to forecast PM₂.₅ 24 hours ahead. **Mean RMSE across stations is 14.7 µg/m³ with bias +3.4**, a 24% improvement over persistence (19.2 µg/m³) — meaningful but 70% above the 8.6 µg/m³ target quoted in earlier drafts. Performance varies sharply by station: Asunción 8.2 µg/m³, Filadelfia (Chaco) 18.6 µg/m³. The Ministry-of-Health deployment claim quoted in earlier drafts was aspirational; deployment depends on resolving the rural-station gap. The peak-biomass-burning episode (Sep 2025) showed a 32% RMSE reduction vs satellite-only baseline — substantially below the 47% claim — see `ACTUAL_RESULTS.md` for measured values.

## Keywords

Earth observation, deep learning, Paraguay, p0035, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)
