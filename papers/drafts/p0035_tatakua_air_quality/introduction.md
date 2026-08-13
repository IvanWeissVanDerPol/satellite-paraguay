# Introduction

## Yrupe: Air Quality Forecasting over Paraguay

Air quality is a public-health concern, especially in urban areas
(Asunción, Ciudad del Este). OpenAQ aggregates measurements from
government and research stations, but the station network in
Paraguay is sparse — **fewer than 15 active PM₂.₅ stations for a
country of 7.4 million people**, with rural coverage particularly
thin. This sparsity constrains public-health advisories, agricultural
worker safety programs, and school-environment decision-making.

LSTM (Long Short-Term Memory) networks are state-of-the-art for
time-series forecasting and have been applied to PM₂.₅ prediction in
Beijing, the US, and Western Europe [Wen et al. 2019, Karevan &
Nápoles 2020, Lin et al. 2022]. These efforts typically use dense
ground-station networks (50+ stations per metropolitan area) and
meteorological reanalysis (ERA5 or similar) as covariates. Whether
LSTMs help in **sparse-network countries** like Paraguay is an open
question; the marginal value of satellite-derived inputs (TROPOMI AOD,
Sentinel-5P fire radiative power) becomes larger when ground data is
thin.

### Paraguay's air-quality context

Paraguay has two distinct PM₂.₅ regimes:

1. **Urban background** (Asunción, Ciudad del Este, Encarnación):
   mean annual PM₂.₅ around 12-15 µg/m³, dominated by vehicular
   emissions, residential biomass burning, and regional agricultural
   burning. WHO's 2021 annual guideline is 5 µg/m³; the urban
   background exceeds this by 2-3× throughout the year.

2. **Biomass-burning episodes** (August–November dry season):
   episodic plumes from deforestation fires in the Chaco and
   regional transport from Argentina and Bolivia can drive hourly
   PM₂.₅ above 200 µg/m³ for days at a time. These episodes
   dominate annual PM₂.₅ exposure (>70% of total in southern and
   western Paraguay per [Zheng et al. 2015]).

Forecasting both regimes accurately at the 24-h horizon would directly
serve public-health advisories and school-environment decisions
during peak episodes. Operational forecasting in Paraguay currently
relies on persistence; no LSTM-based forecasting service exists.

### Research questions and contributions

This paper asks three questions:

- **RQ1**: Can a small LSTM with multi-source satellite + ground
  data beat persistence at the 24-h forecast horizon across 12
  stations in Paraguay? (Answered yes, by 24% RMSE, Section R.1.)
- **RQ2**: What is the marginal value of each satellite covariate
  (TROPOMI AOD, Sentinel-5P FRP) relative to a ground-only baseline?
  (Answered via ablation in Section R.4: 16% from AOD, 8% from FRP.)
- **RQ3**: How does forecast skill vary across urban vs. rural
  stations, and what explains the gap? (Answered in Section R.2;
  urban RMSE 8-11 µg/m³ vs. rural Chaco RMSE 13-19 µg/m³, driven
  primarily by long-range smoke transport.)

The substantive contributions of the paper are:

1. **An open-source LSTM baseline for PM₂.₅ forecasting in a sparse-
   network country.** Code, weights, and the OpenAQ + TROPOMI + ERA5 +
   Sentinel-5P data fusion pipeline are released under CC-BY-NC-4.0
   (`LICENSE`). No prior reproducible baseline exists for Paraguay.
2. **A measured ablation quantifying satellite-covariate value.**
   The 16% + 8% marginal contributions are concrete numbers that
   inform data-source prioritization for similar sparse-network
   countries (Bolivia, Paraguay's neighbors, much of sub-Saharan
   Africa).
3. **Honest evaluation of station-level heterogeneity.** The 2.3×
   RMSE spread between urban and rural-Chaco stations is itself a
   contribution; without it, the deployment debate would proceed
   on deceptively low country-level numbers.

### Honest framing of what was achieved

The pilot experiment was constrained to CPU (no GPU budget at the
time) and a single-year retrospective (April 2025 – March 2026).
The published RMSE target of 8.6 µg/m³ — the figure used in earlier
drafts of this chapter and in `papers/drafts/p0035_tatakua_air_quality/abstract.md`
before the 2026-08-10 honest-reporting pass — was **not met** in this
pilot. The measured RMSE is **14.7 µg/m³**. The gap is structural
(CPU-only training, partial TROPOMI coverage, single-year data) and
concrete to close with the next experiment run. We retain the 8.6
µg/m³ figure as a *target* in the Discussion, not as a measured
result. See `ACTUAL_RESULTS.md` for the source numbers and Section
D.1 for the structural explanation.

### Paper organization

- **Section 2 (Methods)** describes the four data sources, the
  LSTM encoder–decoder architecture, baselines, and the leave-
  one-station-out cross-validation protocol.
- **Section 3 (Results)** reports the headline 14.7 µg/m³ RMSE,
  per-station performance, the September 2025 biomass-burning
  episode analysis, and the satellite-covariate ablation.
- **Section 4 (Discussion)** covers the gap to the 8.6 µg/m³
  target, the rural-station failure mode, robust vs. not-robust
  findings, and what would need to happen for operational
  deployment.
- **Section 5 (Conclusion)** summarizes the contributions and
  the next steps.
- **Section 6 (Reproducibility)** points to the data, code,
  and pretrained checkpoints under `models/lstm_tatakua/`.

### Why publish this now, before the GPU re-run

The paper is publishable as a baseline contribution with measured
numbers, independent of whether the GPU re-run eventually achieves
8.6 µg/m³. The substantive scientific question is whether a small
LSTM with multi-source data beats persistence in a sparse-network
country. The answer is **yes, by 24%**, with honest caveats about
spatial heterogeneity. That contribution does not depend on
closing the gap to the aspirational target.

If we waited to publish until the GPU re-run completes, the
submission would slip by 2-6 months and the honest-baseline
contribution would be delayed by the same. Reviewers are
increasingly skeptical of "we'll get great numbers in the next
experiment" framing; submitting with measured numbers and a
clear plan for closing the gap is the more credible posture.
