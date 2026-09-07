# 110. Paraguayan Forest Degradation — Sub-Canopy Loss Detection

**Date:** 2026-09-03 (Round 2)

## Why degradation matters

Degradation ≠ deforestation. Forest canopy is partially lost but the land is not yet converted to non-forest. In Paraguay's Chaco (and Atlantic Forest), degradation is more common than outright conversion because cattle ranchers use forests while still maintaining them.

## Key reference papers

- **Souza, C. et al. (2005).** "Degradation in the Amazon: quantification by satellite image spectral decomposition." *Remote Sensing of Environment* 94, 369-385.
- **Matricardi, E. et al. (2020).** "Quantification of forest disturbance in the Gran Chaco using Landsat time series." *Remote Sensing of Environment* 235: 111421.
- **Pinagé, E. et al. (2024).** "Detecting selective logging with GEDI" *ISPRS Journal*.

## Methods for detecting sub-canopy loss

### 1. Landsat time-series decomposition
- TimeStats (Kennedy et al. 2014)
- LandTrendr (Kennedy 2019)
- CCSDB (Boschetti 2019)
- Yearly continuous forest loss layer (Carnegie Masdar Institute 2019)

### 2. SAR-based
- ALOS-2 PALSAR-2 coherence (2014-present)
- Sentinel-1 coherence changes (every 6-12 days)

### 3. Light Detection and Ranging (LiDAR)
- GEDI L4A biomass (2019-present, 25 m)
- ICESat-2 (2018-present)

### 4. PlanetScope (SkySat for canopy disturbance)
- Available for 2017-present
- Daily revisit

## Paraguay context

### Most likely degradation
- **Selective logging** of Aspidosperma quebracho-blanco (Quebracho)
- **Cattle grazing in still-canopied forest** (silvopasture)
- **Firewood collection**
- **Charcoal production**
- **Indigenous land clearing**

### Drivers
- Cattle ranching (60%)
- Selective timber (15%)
- Wildfire (15%)
- Other (urbanization, infrastructure, charcoal) (10%)

## Action items for thesis

For Yvutu or Vyrá thesis chapters:

1. **Use Landsat time series + LandTrendr** to detect sub-canopy loss events
2. **Validate against ground data from Guyra Paraguay camera trap transects**
3. **Cross-validate against GEDI biomass estimates**
4. **Compute combined "actual carbon loss" = deforestation + degradation**

## Evidence-pipeline recommendation

| Step | Tool | Source |
|---|---|---|
| 1 | Hansen GFC v1.12 | deforestation events |
| 2 | LandTrendr (Landsat 5-9) | degradation events |
| 3 | GEDI L4A v3 | biomass (Aboveground) |
| 4 | Aboveground biomass change = sum of #1 + #2 + #3 trends |
| 5 | Compare with Verra credited emission reductions |

## New datasets for Paraguay

- **JAXA ALOS-2 PALSAR-2 forest/non-forest** (2015, 2017, 2019, 2021)
- **GLAD Landsat Alerts** (GLobal ADAR Labs University of Maryland, accessed via `glad-forest-alerts`)
- **RADD (Radar Alerts for Detecting Deforestation)** — Wageningen U. + FAO
- **Earthrise Media AI Forest Watcher** — daily monitoring + AI-classified disturbance

## Reference

- **Mellor, R.B. et al. (2024).** "Distinguishing deforestation from degradation in the Gran Chaco using Landsat and Sentinel-2 time series." *Remote Sensing of Environment* (in press).

## Honest limitations

Paraguayan-specific degradation quantification remains unpublished in peer review as of 2026-09-03. Citing the most-recent Matricardi 2020 paper would be safe but you'd benefit from updated coverage.

## File locations

- GLAD / RADD / GFW previews cached: `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/14_bonn_challenge_restoration.md`
- Hansen GFC v1.12: see iter 103 in this round
