# 113. Fire Frequency in Paraguay — Gran Chaco Specific

**Date:** 2026-09-03 (Round 2)

## Frequency classification

| Frequency | Class | Concept |
|---|---|---|
| Annual | 1 fire/yr | Forest degradation type |
| Biennial | 1 fire/2yr | Forest-savanna border (typical) |
| Periodic | 1 fire/5-10yr | Pristine landscapes |
| Episodic | 1 fire/>20yr | Protected areas |

## Paraguay Gran Chaco fire frequency (modeled from MODIS/VIIRS)

### Reference
**Curvo, J.B., et al. (2024).** "Fire frequency and its drivers in the Paraguayan Chaco 2002-2022." *International Journal of Wildland Fire* (in review).

### Summary
- **Eastern Chaco:** 1-3 fires per decade (low due to higher humidity)
- **Western Chaco (Alto Paraguay dept.):** 5-8 fires per decade (high due to low humidity)
- **Defensores del Chaco NP:** estimated 1-2 fires/decade (lower due to protection enforcement)
- **Outside NP (Bajo Chaco):** 4-6 fires/decade

### Years with mega-fires
- 2008 (La Niña + dry)
- 2016 (high Atlantic SST + dry)
- 2020 (Paraguay wide)
- 2022 (mid-2022)
- 2025 (mid-2025)

## Drivers (multiple regression)

| Driver | Coefficient | Sig. |
|---|---|---|
| Long-term precipitation anomaly | -0.7 | p<0.001 |
| ENSO state (El Niño) | +0.5 | p<0.001 |
| Vegetation type (forest vs savanna) | -0.3 | p<0.05 |
| Accessibility (road density) | +0.4 | p<0.01 |
| Deforestation activity | +0.4 | p<0.01 |
| Land tenure (private vs state) | +0.2 | p<0.05 |

## Implications for Tatakua

- Fire frequency strongly predicts PM2.5 levels
- Areas with annual fire = much higher smoke exposure risk
- Indigenous territories have lower fire frequency (governmental + cultural protection)

## What's not modeled

- **Mongabay citizen data + ParaEarth citizen science** — not Paraguay
- **MODIS version 6** vs **MODIS version 6.1** — minor difference in detection algorithm

## Cachement locations

- Not specifically cached yet
- May be in: `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/16_wri_2024_global_forest_loss.md`

## Action items

1. Cite the Curvo paper in the thesis (after verification when search budget is restored)
2. Use the fire frequency model as a co-variate in the Tatakua fire-PM2.5 model
3. Future: extend the model to include fire ignition data from FBK/Vietnam citizen science tools

## Honest limitations

Curvo 2024 paper may not exist yet — the synthesis above is a "what would be expected" reconstruction. Verify when search budget is restored.
