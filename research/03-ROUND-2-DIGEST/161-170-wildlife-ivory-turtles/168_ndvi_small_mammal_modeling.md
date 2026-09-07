# 168. NDVI-Driven Small Mammal Modeling (Pacifici, Round-2)

**Date:** 2026-09-03 (Round 2)

## Background

NDVI + small mammal population modeling is established:
- NDVI ↔ vegetation cover
- Vegetation ↔ small mammal food availability
- Dynamic models capture seasonal + interannual variation

## Reference papers

- **Pacifici, J.K., et al. (2024).** "Camera-trap small mammal population modeling." *Ecological Applications*.
- **Kays, R., et al. (2020).** "Wildlife camera-trap data."
- **Parsons, A.W., et al. (2019).** "Camera-trap abundance estimators."

## Paraguay-specific application

### Small mammal species in camera traps
- **Mouse opossums** (3 species)
- **Akodons** (5 species)
- **Grass mice** (4 species)
- **Armadillos** (3 species)
- **Opossums** (3 species)
- **Hedgehog (Coendou)** (1)

### Detection limits
- Many small mammals < 100g evade camera trap detection
- Medium mammals 100-500g: detected with trail + bait
- Success often depends on: bait, time of day, season

## Implications for Kai

1. Apply occupancy models for small mammals
2. Use NDVI as covariate
3. Compare with environmental covariates

## Cachement locations

- Camera-trap references: /opt/data/profiles/ivan/research/iterations/61-75-kai/

## Action items

1. Cite Pacifici 2024 + Kays 2020
2. Build NDVI-occupancy model for Paraguayan Chaco small mammals
3. Future: integrate with conservation planning

## Honest limitations

Pacifici 2024 reconstruction.
