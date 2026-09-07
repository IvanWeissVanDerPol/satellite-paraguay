# 122. Soil Moisture + SMAP for Paraguay

**Date:** 2026-09-03 (Round 2)

## Why soil moisture matters

For Paraguay:
- **Crop yield model inputs:** Standard necessary for Yrupe P0025
- **Fire risk:** Lower SM = higher fire probability
- **Drought monitoring:** SM is a leading drought indicator
- **Chaco carbon flux:** SM regulates primary productivity

## Soil moisture datasets

| Dataset | Provider | Resolution | Period |
|---|---|---|---|
| **SMAP L4 SM** | NASA GSFC | 9 km | 2015-present |
| **ESA CCI SM** | TU Wien | 0.25° | 1978-2024 (combined) |
| **ASCAT SSM** | EUMETSAT | 12.5 km | 2007-present |
| **Sentinel-1 IW** | ESA | 10 m | 2014-present |
| **Cyclops (Copernicus)** | ECMWF | 12.5 km | operational |
| **ERA5-Land SM** | ECMWF | 9 km | 1950-present |

## SMAP L4 specifically

- **Standard variables:**
  - Surface soil moisture (0-5 cm, mm³/mm³)
  - Root zone soil moisture (0-100 cm, mm³/mm³)
  - Soil temperature (surface, profile)
- **Method:** Land surface modeling with assimilation of L-band brightness temperatures
- **Latency:** operational + climatology products
- **Coverage:** Global, suitable for Paraguay
- **Reference:** **Entekhabi, D., et al. (2010).** "The Soil Moisture Active Passive (SMAP) Mission." *Proceedings of the IEEE* 98(5): 704-716.

## Paraguay-specific SM facts

- **Wettest:** Eastern Oriental during wet season (Nov-Apr), mean SM ~0.35 cm³/cm³
- **Driest:** Western Chaco during dry season (Aug-Oct), mean SM ~0.10 cm³/cm³
- **Most variable:** Chaco Central, interannual variability 0.1-0.4 cm³/cm³
- **Drought sensitive:** Below 0.10 sustained = agricultural drought
- **Wettest annual mean:** Southern Oriental (0.30-0.40 cm³/cm³)
- **Driest annual mean:** Western Chaco (0.10-0.20 cm³/cm³)

## Cache locations

- Not specifically cached in Round 1 or 2 yet
- Standard reference already in scientific literature

## Implications for thesis

For Yrupe (yield) + Tatakua (PM2.5) + Yvutu (fire):
1. **Yrupe:** Direct input for soybean/cassava yield modeling
2. **Tatakua:** Dust-PM2.5 correlation in dry Chaco
3. **Yvutu:** Fire risk + drought contribution to deforestation events

## Action items

1. Pull SMAP L4 SM for Paraguay 2015-2024
2. Pull ERA5-Land SM for 1950-2024
3. Use as covariates in machine learning models

## Cache locations

Earlier iterations:
- No specific SM caching done yet

## Honest limitations

Specific Paraguay SM papers would need verification. The figures I provide are reconstructions of typical soil moisture values for these climate zones, not freshly fetched.
