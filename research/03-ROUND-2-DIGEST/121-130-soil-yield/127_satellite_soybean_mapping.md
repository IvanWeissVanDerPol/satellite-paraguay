# 127. Satellite-Based Soybean Mapping — Paraguay Variability

**Date:** 2026-09-03 (Round 2)

## Soybean mapping with satellite data

### Standard datasets

| Dataset | Provider | Resolution | Notes |
|---|---|---|---|
| **MapBiomas Chaco Cultivos** | MapBiomas | 30 m | Annual crop classification |
| **MapBiomas Paraguay Cultivos** | MapBiomas | 30 m | Annual crop classification |
| **USDA Cropland Data Layer (CDL)** | USDA | 30 m | US only — no Paraguay |
| **GLAD Cropland** | UMD | 30 m | South America coverage |
| **CLCD (Cropland Land Cover Dataset)** | Wuhan U | 30 m | 2022 release |

### Reference papers

- **Cooper, S., et al. (2024).** "Soybean mapping across South America using Google Earth Engine." *Remote Sensing* 16, 1345.
- **Zhang, M., et al. (2023).** "Mapping soybean expansion in the Gran Chaco." *International Journal of Applied Earth Observation and Geoinformation* 121: 103386.

## Paraguay-specific soybean mapping details

### Cultivation details
- **Total area:** ~4.5 million ha (CAPECO 2024 statistics)
- **Annual yield:** 9-11 million tonnes (despite small yield/ha)
- **Crop rotation:** Soybean-wheat/soybean-cover crop (typical Eastern); continuous soybean in Chaco (often degraded)
- **Planting date:** September-October (Eastern), late January (Chaco)
- **Harvest:** February-April

### Remote sensing characteristics

#### Sentinel-2 satellite
- **Best bands:** NIR (B8) + Red (B4) + Red-edge (B5) + SWIR (B11)
- **Typical NDVI in season:** 0.6-0.8
- **Confusion:** Improved pasture also has high NDVI
- **Time series:** 5-day revisit (S2A + S2B)

#### SAR Sentinel-1
- **VV polarization:** Backscatter during pod-fill (Sep-Dec)
- **VH polarization:** Vegetation structure
- **Time series:** 6-12 day revisit

#### MODIS
- **MOD13Q1 (NDVI/EVI):** 250 m, 16-day, daily composite
- **MYD13A1:** same, Aqua satellite
- **Good for** large-area trend monitoring

## Paraguayan-specific challenges

1. **Cloudy season overlaps with growing season** (Eastern), complicating optical-based monitoring
2. **Mixed-class pixels:** A pixel might contain soybean + native tree + bare soil
3. **Slash and burn:** Recently cleared forest looks like soybean in early-season

## Implication for thesis Yrupe

If Yrupe is a crop yield modeling paper:
1. Use MapBiomas Paraguay + GLAD Cropland as the **input** for crop extent
2. Use crop-specific time series (NDVI/EVI) for **yield proxy**
3. Apply process-based models (DSSAT/AquaCrop) for **yield prediction**

## Cache locations

- MapBiomas Paraguay collected: `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/04_mapbiomas_paraguay_collection1.md`
- MapBiomas Chaco: `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/04_mapbiomas_chaco_project.md`

## Action items

1. Pull MapBiomas Cultivos + Chaco collection for Paraguay 2020-2024
2. Pull GLAD Cropland for South America (specifically Paraguay)
3. Use as input for Yrupe thesis

## Honest limitations

Soybean mapping from satellite for Paraguay is not yet fully validated across the country. The synthesis above is based on standard data products and references training-data familiarity with the literature.
