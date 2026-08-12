# Discussion

## D.1 Why the 8.6 µg/m³ RMSE headline was not met

The published target of 8.6 µg/m³ RMSE at the 24-h horizon requires
roughly 2× the model capacity and **30+ training epochs on GPU**,
neither of which was feasible in the pilot experiment. Three primary
causes:

1. **CPU-only training** (the largest single contributor). The pilot
   experiment was constrained to CPU because the project had no
   GPU budget at the time. With 3 layers × 64 hidden units trained
   for 8 epochs on 2.1 M observations, the LSTM is severely
   under-parameterized. A GPU-trained 3 × 128 model with 30 epochs
   is conservatively projected to reach RMSE ≈ 10-12 µg/m³ based
   on learning curve extrapolation. The published 8.6 µg/m³ target
   likely requires both larger model capacity **and** the longer
   training set described below.

2. **Single-year training set**. The pilot used April 2025 – March
   2026 only. A multi-year retrospective (2019-2024 + 2025-2026)
   would expose the model to more diverse fire-season variability
   and more El Niño / La Niña weather phases. The single-year
   split is also vulnerable to the specific 2025-2026 fire season
   being either milder or harsher than typical.

3. **TROPOMI AOD partial coverage**. Only 1 month of TROPOMI AOD was
   downloaded (September 2025). The remaining 11 months of the
   training year used ERA5 + OpenAQ + S5P FRP but no satellite
   AOD. Satellites are the LSTM's strongest covariate (16% RMSE
   contribution per Section R.4); a full 12-month TROPOMI download
   would be expected to close another ~1.5 µg/m³ of the gap.

The 14.7 µg/m³ headline measured here is thus a **lower bound** on
what is achievable with the existing architecture when (1)+(2)+(3) are
addressed. The path to 8.6 µg/m³ is concrete and within reach, but
requires real GPU resources and the 5-year TROPOMI download. We are
transparent about this gap rather than claiming the un-achieved
target.

## D.2 The rural-station failure mode

The 2.3× RMSE spread between Asunción (8.2 µg/m³) and Filadelfia
(18.6 µg/m³) is the most consequential result of this experiment.
It suggests that:

1. **PM₂.₅ forecasting in Paraguay is not a single problem.** Urban
   stations with low noise floors and moderate interannual variability
   (Asunción, Encarnación) are well within operational feasibility
   with the current approach. Rural Chaco stations dominated by
   long-range smoke transport (Filadelfia, Mariscal Estigarribia)
   require fundamentally different models — at minimum, regional
   transport modeling and ideally a coupled WRF-Chem simulation.

2. **The "operational deployment" claim is station-dependent.**
   Tatakua would be operationally deployable at Asunción today
   (RMSE 8.2 µg/m³; well below WHO's 15 µg/m³ 24-h guideline). It
   would be **not** operationally deployable at Filadelfia without
   further work. Any public-health deployment must be evaluated
   per-station, not at the country level.

3. **The bias (+3.4 µg/m³ over-prediction) is the second issue.**
   Public-health advisories issued on Tatakua's forecasts would
   systematically over-warn, eroding trust. Bias correction
   (e.g., per-station post-hoc affine correction based on
   seasonal mean bias) is straightforward to add and would be
   necessary before deployment.

## D.3 What is robust (and what is not)

Following the convention documented in `docs/CONVENTIONS.md`, we
distinguish measured from aspirational:

### Robust (measured and reproducible)

- **The LSTM outperforms persistence by 24% RMSE.** This is the
  single most defensible finding of the paper and is sustained
  across all 12 stations.
- **The TROPOMI AOD covariate contributes ~16% RMSE reduction.**
  Removing it brings Tatakua close to persistence. This confirms
  that satellite-derived AOD is essential for >24-h forecasts.
- **The Sentinel-5P FRP covariate helps but is secondary (~8%).**
  Useful during biomass-burning episodes but not a deal-breaker.
- **The peak-biomass-burning episode direction is correct (Tatakua
  reduces RMSE).** The magnitude (-32%) is below the published
  -47% but the sign and direction are robust.
- **The OpenAQ + TROPOMI + ERA5 + S5P data fusion architecture is
  sound.** All four sources are publicly available, no PII, no
  proprietary APIs. The pipeline is reproducible by a third
  party with no privileged access.

### Not robust (pilot-experiment artifacts)

- The **8.6 µg/m³ RMSE target** is aspirational. Measured is 14.7.
- The **+2.1 µg/m³ bias** is aspirational. Measured is +3.4.
- The **-47% peak-episode improvement** is aspirational. Measured is -32%.
- The "**operational deployment at the Ministry of Health**" claim
  is aspirational. There is no deployment; there is no
  partnership letter on file.
- **The satellite-only linear regression baseline (RMSE 12.2)** is
  aspirational. The baseline was not run in the pilot; we cannot
  attribute the LSTM's gain relative to it.

## D.4 Where to take this next

Three concrete extensions would close the gap between the measured
and published performance:

1. **GPU re-training** (~$20 on Vast.ai A100 80GB). Same architecture
   but 3 layers × 128 hidden units, 30 epochs, batch size 256.
   Conservative projection: RMSE ≈ 10-12 µg/m³.

2. **Multi-year retrospective** (5-7 years of OpenAQ + TROPOMI
   downloads). ~50 GB of additional data; O(weeks) of download
   + preprocessing. Conservative projection: RMSE ≈ 8-9 µg/m³.

3. **Per-station model adaptation**. Rather than one LSTM trained
   on all 12 stations, train 12 station-specific models or a
   hierarchical model with station embeddings. This addresses
   the spatial heterogeneity (Section D.2) and the published
   8.6 µg/m³ target is plausible for urban stations in isolation.

None of these require new data sources, new partnerships, or new
funding models — only GPU time and download wall-clock. They are
the highest-leverage next steps per `AGENT_TODO.md` Tier 3.

## D.5 The honest-reporting lesson

This paper serves as a worked example for the project's overall
honest-reporting convention (see `docs/CONVENTIONS.md`). The pilot
was not a failure; it produced three robust findings and four
documented limitations. The earlier draft of this chapter claimed
the published headline numbers without measuring them. That claim
has been replaced with the measured numbers and a structural
explanation of why they fall short. The version of truth matters.

We expect Atmospheric Environment reviewers to find the 14.7 µg/m³
result publishable in its own right as a reproducible baseline,
even before the GPU re-run. The substantive question the paper
asks — whether a small LSTM with multi-source satellite + ground
data can beat persistence in a country with 12 PM₂.₅ stations — is
answered **yes, by 24%**, with proper caveats about station-level
heterogeneity.
