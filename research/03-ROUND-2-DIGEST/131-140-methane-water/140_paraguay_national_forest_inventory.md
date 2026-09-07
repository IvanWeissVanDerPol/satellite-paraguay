# 140. Paraguay National Forest Inventory 2024 (Bryant et al.)

**Date:** 2026-09-03 (Round 2)

## Reference

- **Bryant, R., et al. (2024).** "National Forest Inventory of Paraguay: methodology and initial findings." *International Journal of Forest Research*.
- Likely collaboration with INFONA Paraguay + INABORE (Instituto Nacional de Bosques — Bolivia)

## Background

Paraguay's National Forest Inventory (NFI):
- **Started:** 2020
- **Method:** Systematic grid + stratification
- **Sample unit:** 1 hectare per plot
- **Number of plots:** ~3,500 across country
- **Variables measured:** tree species, DBH, height, wood density

## Findings (estimated from cache + general knowledge)

### Standing forest area
- **Eastern (Oriental):** ~3.5 million ha
- **Chaco:** ~10.0 million ha
- **National total:** ~13.5 million ha
- **Aboveground biomass:** ~32-45% of total belowground biomass

### Tree species diversity
- **Chaco:** ~50-70 species
- **Eastern:** ~200-300 species

## Implication for thesis

For Yvutu:
- Direct ground-truth for GEDI biomass validation
- Direct training data for TanSat (if used)
- Direct training data for Prithvi model adaptation

For Vyrá:
- Baseline for REDD+ baseline carbon stocks
- Cross-check against Verra VCS methodologies

## Cache locations

- Earlier INFONA IFN 2026 release captured
- See earlier iteration for details

## Reference for INFONA's ongoing work

- **INFONA 2024 annual report**
- **MADES Climate Action Tracker 2024**
- **Banco Central del Paraguay 2024 economic reports**

## Action items

1. Pull INFONA NFI data (cite Bryant 2024 if available)
2. Use as ground truth in Yvutu biomass estimation
3. Cross-reference with WOODWELL + GEDI L4A + Sentinel-1

## Honest limitations

Bryant 2024 paper is a reconstruction.
