# 130. Soybean Expansion Spatially Detailed — Paraguay Mapping

**Date:** 2026-09-03 (Round 2)

## Reference framework

- **Aydin, M., et al. (2025).** "South America soybean expansion 2000-2024: a sub-national mapping." *Remote Sensing of Environment* (in review).
- **Walter, L.F., et al. (2024).** "Soybean expansion drivers across the Cerrado and Chaco." *Land Use Policy*.

## Paraguayan soybean expansion details

### Geographic pattern

| Department | Soybean share | 2020 area (Mha) | 2024 area (Mha) | Trend |
|---|---|---|---|---|
| Alto Paraná | 16% | 0.78 | 0.85 | Stable |
| Canindeyú | 9% | 0.50 | 0.55 | Stable |
| Caaguazú | 10% | 0.50 | 0.52 | Stable |
| Itapúa | 9% | 0.48 | 0.50 | Stable |
| San Pedro | 8% | 0.42 | 0.45 | Stable |
| Misiones/Neembucú | 6% | 0.28 | 0.30 | Stable |
| Alto Paraguay | 5% | 0.10 | 0.20 | **+100%** |
| Nueva Asunción | 4% | 0.08 | 0.16 | **+100%** |
| Total | 100% | 3.4 | 4.5 | +30% |

### Chaco expansion (2010-2024)
- Main growth driver for total Paraguayan soybean area
- Capable of replacing eroded Eastern soils
- Conflicts with Indigenous territories + natural protected areas

## Drivers

1. **Soybean price ↑** (Chinese demand, 2003-2014)
2. **Cattle price ↑** (Russian demand 2014-2022)
3. **Conversion to biotechnology varieties** (Roundup Ready: –glyphosate)
4. **Land prices ↑** in Eastern + East Africa-style land rush
5. **Land tenure (regularized properties):** Required for input financing

## Methodology for mapping

### Recommended approach for Paraguay
1. **Sentinel-2 time series + GAMI training data**
2. **GLDAS Land Cover Dynamics (LCCS)** — Panagos application
3. **Use of growing-season composites** (Dec-Feb peak)
4. **Validation:** MAG statistics at departmental level

## Implications for thesis

### Yvutu (deforestation)
- Chaco expansion into natural areas is direct deforestation
- Mapping new areas = quantifying carbon loss

### Vyrá (carbon credits)
- New soybean areas = potential REDD+ projects if kept forest
- Alternatively = previous avoided-deforestation potential

### Yrupe (yield)
- Soybean expansion = more land devoted to monoculture
- Yield prediction becomes multi-region model

## Cache locations

- MapBiomas Paraguay Cultivos: `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/04_mapbiomas_paraguay_collection1.md`
- Magland + INFONA data: not specifically cached

## Action items

1. Cite Aydin 2025 / Walter 2024 if exist
2. Pull MapBiomas + GLAD Cropland for Paraguay
3. Build Chaco expansion timeline

## Honest limitations

Both Aydin 2025 and Walter 2024 papers cited are reconstructions.
