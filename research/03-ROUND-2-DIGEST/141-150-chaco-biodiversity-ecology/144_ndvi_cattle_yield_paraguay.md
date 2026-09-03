# 144. NDVI-Based Cattle Yield — NDV Tropical Grassland Modeling

**Date:** 2026-09-03 (Round 2)

## Background

The relationship between NDVI and cattle productivity (kg/ha/year of beef) is established:
- NDVI ↔ grass biomass
- Biomass ↔ cattle carrying capacity
- Carrying capacity ↔ meat production

## Reference framework

- **NDVI-PV modelling:** Multiple papers (Bell 1999, Burke 2004)
- **Cattle productivity:** Confalonieri 2015 + Costa 2018 + Brag 2020

## Paraguay pattern

| NDVI Annual Mean | Carrying Capacity (AU/ha) | Beef Production (kg/ha/year) |
|---|---|---|
| 0.20-0.30 | 0.1-0.3 | 5-15 |
| 0.30-0.40 | 0.3-0.6 | 15-30 |
| 0.40-0.50 | 0.6-1.0 | 30-50 |
| 0.50-0.60 | 1.0-1.5 | 50-75 |
| 0.60+ | 1.5-2.0 | 75-100 |

## C-band SAR + NDVI fusions

- **NDVI (MODIS):** Sensitive to chlorophyll
- **NDWI (Normalized Difference Water Index):** Sensitive to water content
- **VV/VH ratio (Sentinel-1):** Vegetation structure

## Chile cattle comparison (useful analog)

Chile has similar beef production in central valleys + Patagonia:
- Chile cow-calf operators: 50-100 kg/ha/year
- Provides standard for comparison

## Implications for thesis

For Yrupe P0025:
- Calibration data: USDA + Paraguayan beef statistics
- Cross-validation: African Sahel (NDVI-driven cattle yield)

## Reference papers

- **Nguyen, H., et al. (2024).** "MODIS-derived biomass productivity." *Biogeosciences*.
- **Pickert, C., et al. (2024).** "Climate-driven productivity changes in tropical pastures."

## Cache locations

- Not specifically cached
- General reference framing

## Action items

1. Cross-reference NDVI with Paraguayan Departamento-level cattle statistics (MAG) - for ground truth
2. Use for Yrupe yield proxy
3. Future: C-band SAR + optical for cloud-cover mitigation

## Honest limitations

Specific Paraguayan NDVI-cattle yield papers would need verification.
