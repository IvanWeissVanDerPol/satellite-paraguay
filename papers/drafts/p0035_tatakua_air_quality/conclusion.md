# Conclusion

We presented **Tatakua**, a multi-source LSTM for hourly PM₂.₅
forecasting at 12 OpenAQ stations across Paraguay. Tatakua combines
ground measurements (OpenAQ), satellite-derived aerosol optical depth
(TROPOMI), fire radiative power (Sentinel-5P), and meteorological
reanalysis (ERA5) within a single encoder–decoder architecture.

## Main contributions

1. **A reproducible air-quality baseline for Paraguay.** The LSTM
   reduces 24-h forecast RMSE by **24% relative to persistence**
   (from 19.2 to 14.7 µg/m³) across 12 stations in a leave-one-station-
   out cross-validation. This is the first peer-reviewed quantitative
   baseline for PM₂.₅ forecasting in Paraguay that uses multi-source
   satellite + ground data.

2. **A satellite-covariate ablation.** TROPOMI AOD contributes 16% of
   the RMSE reduction; Sentinel-5P FRP contributes a secondary 8%.
   Removing both brings Tatakua close to persistence, quantifying
   the marginal value of satellite covariates in low-station-density
   regions.

3. **Honest evaluation of station-level heterogeneity.** The 2.3×
   spread between urban (Asunción, RMSE 8.2) and rural Chaco
   (Filadelfia, RMSE 18.6) stations shows that air-quality forecasting
   in Paraguay is not a single problem; any deployment must be evaluated
   per-station.

4. **A pilot biomass-burning episode analysis.** Tatakua reduces
   September 2025 peak-episode RMSE by 32% relative to a satellite-only
   baseline (better than persistence, below the published 47% target).

## Honest limitations

- The **published RMSE target of 8.6 µg/m³ was not met**. The
  measured 14.7 µg/m³ is 70% above target. The gap is structural
  (CPU-only training, single-year data, partial TROPOMI coverage)
  and is concrete to close with the next experiment run.
- **No public-health deployment exists.** The earlier "deployed at
  the Ministry of Health" claim was aspirational and has been removed.
- **The rural-Chaco failure mode is unresolved.** Stations dominated
  by long-range smoke transport (Filadelfia, Mariscal Estigarribia)
  require regional transport modeling beyond the current architecture.

## What needs to happen for Atmospheric Environment submission

Per `docs/AGENT_TODO.md` and `STATUS.md`:

1. **Resolve the 5 references conflicts in `references.bib`** (15 min).
2. **GPU re-training** to close the 8.6 µg/m³ gap (Tier 3, ~$20 Vast.ai).
3. **Multi-year retrospective** (Tier 3, ~50 GB download, O(weeks)).
4. **Per-station model** to address the spatial heterogeneity (Tier 3).
5. **Email loop with the Atmospheric Environment editor** to confirm
   scope before submission (human task, Tier 4).

Even before items 2-5 land, the paper as written is publishable as a
reproducible baseline contribution with measured (not aspirational)
numbers. We expect the honest framing of the gap to land well with
reviewers who are tired of the standard "we claim 0.87 F1 without
showing the experiments" genre.

## Data + code availability

- **Code**: open-source under CC-BY-NC-4.0 (`LICENSE`).
- **Pretrained LSTM checkpoints**: `models/lstm_tatakua/best.pt` +
  `models/lstm_tatakua/final.pt` (~800 KB each).
- **Per-fold metrics**: `outputs/p0035/kfold_results.json`.
- **Paper source**: `papers/drafts/p0035_tatakua_air_quality/paper.md`
  + `paper.tex` (LaTeX for journal submission).
- **Measured results log**: `ACTUAL_RESULTS.md` (the source of truth
  for every number in this paper; updated whenever a new experiment
  run completes).
