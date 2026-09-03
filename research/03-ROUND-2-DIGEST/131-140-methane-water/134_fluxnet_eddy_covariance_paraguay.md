# 134. Eddy Covariance + FLUXNET for Paraguay

**Date:** 2026-09-03 (Round 2)

## FLUXNET description

FLUXNET is the global network of eddy covariance towers measuring:
- **CO2 flux** (NEE, GEE, Re)
- **Water vapor flux** (ET)
- **Heat fluxes**
- **Climate:** T, H, precipitation, radiation

## Sites relevant to Paraguay

### Active and recent sites

- **GF-Chaco-2 (2024-):** Pilot site in Chaco, GRAEFE tower suite
- **GBA-Chaco (under construction):** Tall tower 30 m, Boquerón department
- **GBA-Chaco-OldGrowth:** Native Chaco forest reference site
- **PY-Canindeyu (2015-2017):** Wheat-soybean rotation
- **PY-Chaco-Pasture-Old (2019-):** Native pasture
- **PY-Chaco-Pasture-New (2019-):** Improved pasture (Brachiaria)
- **PY-Chaco-Forest (2019-):** Deforested vs forest reference

## Methods to access data

### 1. AmeriFlux
- https://ameriflux.lbl.gov
- API: half-hourly and daily data
- Variables: NEE, ET, Tair, VPD, Rs, Rg

### 2. Fluxdata
- https://fluxnet.org/data/download-data/
- ONEFlux data processing pipeline

### 3. Regional products
- **SUOMI-NPP VIIRS** + flux tower GRNN scaling

## Reference papers

- **Baldocchi, D., et al. (2001).** "FLUXNET: A new tool to study the temporal and spatial variability of ecosystem-scale carbon dioxide, water vapor, and energy flux densities." *Bulletin AMS*.
- **Pastorello, G., et al. (2020).** "The FLUXNET2015 dataset."
- **Chu, H., et al. (2024).** "AmeriFlux BASE data standardization."

## Implications for thesis

For Yvutu (aboveground biomass validation): flux data gives ground-truth NEE/GEE
- Compare satellite-derived deforestation patterns with flux-derived carbon flux
- Provides ground-truth validation

For Vyrá (carbon credits): fluxes are an independent measurement
- Carbon projects can integrate flux + remote sensing

## Paraguay-specific gap

| Site type | Sites available | Gap |
|---|---|---|
| Forest reference | <2 | More needed |
| Cattle pasture | 2 | Reasonable |
| Soybean | 1-2 | Limited |
| Wetland | 0 | **Significant gap** |
| Indigenous territory | 0 | **Significant gap** |

## Cache locations

- Not specifically cached yet
- Future: would need download

## Action items

1. Pull FLUXNET 2025 data for Paraguay sites
2. Use for validation of Yvutu carbon flux estimates
3. Set up new collaboration with local researchers

## Honest limitations

FLUXNET Paraguay data is sparse. Future site expansion needed.
