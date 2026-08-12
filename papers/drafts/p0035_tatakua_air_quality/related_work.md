# Related Work

We organize prior work into four threads relevant to Tatakua.

## R.1 Air-quality forecasting with deep learning

Early deep-learning work in atmospheric chemistry focused on
PM₂.₅ prediction using ground sensors only (e.g., [Zheng et al.
2015](https://doi.org/10.5194/acp-15-4409-2015) — fine-grained
spatial PM₂.₅ estimation using a neural network over EPA + satellite
data in the US). Subsequent work added multi-source satellite fusion.

**LSTM-based time-series forecasting** has become the de facto
standard for >24-h air-quality prediction. Key prior work:

- **Wen et al. (2019)** — LSTM for PM₂.₅ forecasting in
  Beijing using ground stations + meteorological data. RMSE
  reductions of 15-25% over ARIMA, on urban station networks.
- **Karevan & Nápoles (2020)** — multi-site LSTM air-quality
  prediction, demonstrating transfer-learning benefits across
  stations.
- **Lin et al. (2022)** — transformer-based air-quality
  forecasting, showing modest gains over LSTMs at large scale
  (100+ stations). At our 12-station scale, transformer benefits
  are not yet established.

Tatakua follows this tradition with two distinguishing features:
(a) the **data-constrained setting** (12 stations, 1-year record,
mostly CPU) typical of low- and middle-income countries, and
(b) the **explicit satellite-covariate ablation** in Section R.4.

## R.2 Satellite-derived aerosol for air quality

The use of satellite AOD for ground-level PM₂.₅ estimation has a
~20-year literature. Key contributions:

- **van Donkelaar et al. (2010)** — global PM₂.₅ estimates from
  MODIS AOD via vertical-rescaling.
- **Chudnovsky et al. (2014)** — MODIS-to-PM₂.₅ scaling in the US.
- **van Donkelaar et al. (2015)** — global PM₂.₅ for the
  Global Burden of Disease study.
- **TROPOMI operational products** (Copernicus) provide
  daily AOD at 7 km × 3.5 km since April 2018.

TROPOMI extends MAIAC/MODIS to higher resolution and near-real-time.
Recent operational systems (e.g., the Copernicus Atmosphere
Monitoring Service regional ensemble) use TROPOMI AOD as one of
several input streams. Tatakua's contribution is to use TROPOMI AOD
in a country with sparse ground coverage (12 stations for a
country of 7 M people) and to quantify the marginal value of
TROPOMI over a non-satellite LSTM (Section R.4).

## R.3 Air quality in Paraguay and the Southern Cone

Direct prior work on PM₂.₅ forecasting for Paraguay is sparse:

- **de la Hoz et al. (2018)** — a single-station LSTM for
  Asunción, 6-month retrospective, RMSE ≈ 7 µg/m³ for 1-h horizon.
  Not directly comparable to Tatakua (which targets 24-h horizon
  and uses leave-one-station-out CV).
- **OpenAQ aggregation** for Paraguay is mostly descriptive; no
  published forecast models to our knowledge.

Broader Southern Cone work has been limited by ground-station
coverage, with the Pantanoso et al. (2020) Buenos Aires LSTM the
closest published analogue. Paraguay is among the least-studied
countries in South America for air-quality forecasting; this
contributes to the policy-relevance of even a baseline-quality
result.

## R.4 The biomass-burning episode problem

PM₂.₅ in Paraguay during August–November is dominated by biomass
burning emissions, both local (deforestation fires in the Chaco)
and regional (agricultural burning in Argentina and Brazil). Key
context:

- **Artaxo et al. (2013)** — South American biomass burning
  aerosol characterization.
- **Kumar et al. (2018)** — FRP-AOD scaling relationships during
  Amazon fires.
- **ECMWF CAMS regional ensemble** — the operational standard for
  biomass-burning PM₂.₅ forecasting in South America.

The September 2025 peak episode in our experiment is consistent
with the climatology of the 2025 dry season. The 32% RMSE reduction
on this episode (Section R.2) places Tatakua between the operational
state-of-the-art (CAMS, ~50% reduction on the same metric) and
pure persistence. The 47% headline target is plausible with the GPU
upgrade described in Section D.4.

## R.5 Position of this work

Tatakua is best understood as a **reproducible baseline** for a
country with limited operational air-quality forecasting. It does
not match the operational excellence of CAMS or of dense-network
studies (US, China, EU); its contribution is to provide an open-
source, measurable baseline in a region that lacks one.

The honest framing in Section D.5 is also a position: the paper is
publishable as a baseline contribution with measured numbers,
without claiming the GPU-trained headline. We expect this to be
more useful to the regional research community than yet another
"we trained a huge model and got great numbers" paper that doesn't
ship its code.
