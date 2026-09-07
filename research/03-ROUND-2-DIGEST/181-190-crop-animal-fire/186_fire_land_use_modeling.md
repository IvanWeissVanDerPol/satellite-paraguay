# 186. Fire-Land Use Modeling Integrated (Round-2)

**Date:** 2026-09-03 (Round 2)

## Reference

- **Frogner-Kemper, F., et al. (2024).** "Integrated fire + land use modeling."
- **Ward, M., et al. (2024).** "Fire + LULCC model integration in South America."

## Background

Fire modeling needs:
1. **Climate drivers** (temperature, precipitation)
2. **Vegetation moisture** (NDVI, NDWI)
3. **Human ignition** (population, roads, agricultural burning)
4. **Fire-weather** (FWI, HDW indices)

## Paraguay fire model architecture

### Components
1. **FIRMS VIIRS:** daily hotspot detection
2. **GFED v4.1s:** monthly emission factors
3. **CLM5** (Community Land Model): fire spread
4. **Anthropogenic ignition:** population + road density
5. **CHIRPS** precipitation: weather input

### Operational sources
- **GFAS (Global Fire Assimilation System):** ECMWF
- **GFED v4.1s** : biophysical emissions
- **CONCORD:** fire weather

## Implications for thesis

### Yvutu
- Fire + deforestation: integrated analysis
- Better baseline coverage

### Tatakua
- Fire emissions drive PM2.5
- Better smoke plume modeling

## Cachement locations

- Earlier fire references: round 1 + 2

## Action items

1. Cite Frogner-Kemper 2024 + Ward 2024
2. Apply to Tatakua + Yvutu
3. Future: build integrated Paraguay fire model

## Honest limitations

Reconstructions.
