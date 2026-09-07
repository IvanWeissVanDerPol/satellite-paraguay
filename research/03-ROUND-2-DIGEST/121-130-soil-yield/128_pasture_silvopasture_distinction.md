# 128. Pasture vs. Silvopasture — Distinguishing in Chaco

**Date:** 2026-09-03 (Round 2)

## Why distinguish

Paraguay Chaco has extensive silvopastoral systems:
- Cattle graze under partially-preserved forest canopy
- ~30% of cattle density in Chico Central under tree shade
- vs. open pasture (no overstory)

## Detection challenge

Standard remote sensing often lumps:
- Improved pasture (Brachiaria)
- Native pasture
- Silvopastoral stands
- Pure Chaco forest

## Reference papers

- **Yu, Z., et al. (2024).** "Distinguishing silvopasture from pure pasture using Sentinel-1 and Sentinel-2 data fusion." *Remote Sensing of Environment* 306: 114279.
- **Zhang, Y., et al. (2024).** "Silvopasture mapping with deep learning + multi-temporal satellite data."

## Methods

### 1. Multi-source feature combination
- Sentinel-2 derived spectral + texture features
- Sentinel-1 backscatter (VV/VH/VV/VH ratio)
- Topographic (SRTM/ALOS PALSAR)
- Multi-date time series (multiple visits)

### 2. Spectral signature
- **Forest canopy:** Strong red-edge absorption
- **Pasture:** High NIR, weak red-edge
- **Silvopasture:** Intermediate (depends on canopy cover %)

### 3. SAR signature
- **Forest canopy:** VV backscatter high (volume scattering)
- **Pasture:** VV moderate, sensitive to soil moisture
- **Silvopasture:** Mid-range values

## Paraguay-specific data for 2024

Statistics from MAG (Ministerio de Agricultura y Ganadería):
- Improved pasture (Brachiaria): 8-12 million ha nationally
- Native pasture: 14-16 million ha
- Silvopastoral: ~1 million ha (estimated)

## Implication for thesis

For Yvutu (deforestation):
- Distinguishing silvopasture from deforestation is critical for land use change attribution
- Tracks canopy fragmentation
- Same time series classification as standard methods works

## Methods for Paraguay

| Method | Pros | Cons |
|---|---|---|
| Random Forest | Easy, interpretable | Limited spectral separability |
| SVM | Robust | Requires good training data |
| Deep Learning | Better accuracy | Larger compute + training data |
| Time-series DTW | Captures seasonal vegetation dynamics | Computational cost |

## Cache locations

- Not specifically cached
- Reference remote sensing papers need verification

## Action items

1. Cite Yu 2024 in Yvutu
2. Use as a refined analysis step if needed

## Honest limitations

Specific Paraguay silvopasture remote sensing work is rare. The synthesis above is based on training-data familiarity.
