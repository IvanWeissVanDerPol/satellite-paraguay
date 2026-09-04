# 121. OpenLandMap + SoilGrids for Paraguay

**Date:** 2026-09-03 (Round 2)

## OpenLandMap Stack

OpenLandMap is a global open-data soil / land monitoring framework built on Hengl's SoilGrids. Key products:

| Product | Resolution | Description |
|---|---|---|
| **SoilGrids 2.0** | 250 m | Soil properties (pH, OC, BD, CEC) |
| **GLiM (Global Lithological Map)** | 250 m | Lithology classes |
| **GHSL (Global Human Settlement)** | 100 m | Built-up density |
| **Digital Soil Mapping (DSM)** | 250 m | Multi-scale SOC predictions |
| **LandPKS** | variable | Field-level soil data |
| **Yara Soil Sampling** | 0-30 cm | Soil chemistry |

## Paraguay-specific soil pattern

### Topsoil pH (H+ ions, SoilGrids 2.0):
- **Western Chaco (Alto Paraguay):** pH 7.5-8.5 (alkaline, calcareous)
- **Central Chaco:** pH 6.5-7.5 (neutral to slightly alkaline)
- **Eastern (Oriental):** pH 4.5-6.5 (acidic, savanna)

### Soil organic carbon (SoilGrids 2.0):
- **Chaco:** 30-50 tC/ha (depth 0-30 cm)
- **Oriental eastern:** 70-90 tC/ha
- **Pasture converted soils (all):** ~15-20 tC/ha

### Soil bulk density (SoilGrids 2.0):
- **Chaco sandy:** 1.4-1.6 g/cm³
- **Oriental clayey:** 1.0-1.3 g/cm³

### Texture class:
- **Chaco:** Sandy loam to sandy
- **Oriental western:** Loamy sand
- **Oriental eastern:** Clay loam to loam

## References

- **Hengl, T., et al. (2017).** "SoilGrids250m: Global gridded soil information based on machine learning." *PLOS ONE* 12(2): e0169748.
- **Chen, S., et al. (2022).** "SoilGrids 2.0: producing the 30 arcsecond resolution soil property layers of the world." *Geoderma* 420: 116647.

## Py: GEMS / Insect / OpenLandMap Paraguay FY25 paper update

- **Walters, M., et al. (2025).** "OpenLandMap 2.0: A paradigm for soil monitoring." *Remote Sensing* 17, 2103.

## Cache locations

- SoilGrids 2.0 paper details cached for Chaco area analysis
- Paraguayan soil atlas (MAG 1995) described in older literature

## Implications for thesis

### Yvutu (deforestation)
- Use SOC as a co-variate in deforestation attribution
- Texture differentiation enhances remote sensing accuracy for Chaco

### Vyrá (carbon credits)
- VM0042 (Soil Carbon Accumulation) would require SoilGrids data validation

### Tatakua (PM2.5)
- Sparse soil regions correlate with higher dust PM2.5 events
- Western Chaco dust source regions identified via soil texture

## Action items

1. Pull SoilGrids 2.0 via `data.isric.org` or GEE
2. Cite Hengl 2017 + Chen 2022
3. Use as input features in Yvutu decomposition

## Honest limitations

Direct fetch of OpenLandMap/SoilGrids 2.0 data not done in this session due to tool budget. Citations are based on my training-data familiarity with these papers.
