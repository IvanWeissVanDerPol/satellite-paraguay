# 108. Paraguay SW Monsoon + Soil-Climate Interactions

**Date:** 2026-09-03 (Round 2)

## South American Monsoon System (SAMS) relevance

The South American Monsoon has direct impact on Paraguay, especially the Oriental region:
- **Wet season onset:** 17-22 October (Oriental); 25-30 November (Chaco)
- **Wet season retreat:** mid-April
- **SAMS variability:** ENSO strongly modulates (El Niño = eastern dry; La Niña = western wet)
- **Future projections:** SAMS intensity expected to increase under CMIP6 SSP2-4.5+

## Key papers for the southwest monsoon impact

- **Vera, C. et al. (2006).** "Toward a unified view of the American monsoon systems." *J. Climate* 19: 5117-5134.
- **Marengo, J. et al. (2012).** "Recent developments on South American monsoon system." *J. Climate* 25: 6239-6254.
- **Espinoza, J.C. et al. (2024).** "Droughts in the La Plata Basin" *Hydrol. Process.* — Argentina, Paraguay, Bolivia impacts.

## Soil-climate interaction layers

| Layer | Standard dataset | Resolution | Relevance |
|---|---|---|---|
| Soil moisture | SMAP L4 (Entekhabi 2016) | 9 km | Chaco water security |
| Soil moisture | ESA CCI SM (combining SMMR+SSM/I+SMAP+AMSR2+ASCAT) | 0.25° | Long-term time series |
| Soil temperature | ERA5-Land | 9 km | Acidity layers + vegetation |
| Soil bulk density | SoilGrids 2.0 | 250 m | Forest biomass correlation |
| Soil pH (H+) | SoilGrids 2.0 | 250 m | Crop yield modeling |
| Soil organic carbon | SoilGrids | 250 m | Carbon stock mapping |
| Topsoil texture | SoilGrids | 250 m | Agricultural suitability |

## Paraguay-specific soil data

- SoilGrids 2.0 best for country-level
- MAG Atlas de Suelos del Paraguay (1995) — older but still used
- Soil surveys by FAO/UNESCO — 1960-1980s
- Future: Paraguay Soil Database 2.0 (under MAG-UNESCO, expected 2026-2027)

## Climate models used for projection (CMIP6 ensemble)

### Standard models covering Paraguay
- CESM2 (NCAR)
- GFDL-CM4 (NOAA)
- CanESM5 (Canadian)
- MIROC6
- NorESM2
- EC-Earth3
- AWI-ESM (Alfred Wegener Institute)
- EC-Earth3-Veg-LR (land-atmosphere coupling)
- CNRM-ESM2-1

### Reference: latest IPCC AR6 WG1 Atlas data

## Future climate projections for Paraguay soil moisture (CMIP6 median, late-century SSP3-7.0):
- **Top soil (0-10 cm) drying:** -10% mean annual SM
- **Deep soil (1-3 m) drying:** -15%
- **Implications:** forest mortality risk, agricultural productivity decline

## Gaps for thesis

- Paraguay-specific soil survey (modern, post-2010s data) is sparse
- Soil carbon stocks for Chaco-region (Sanderman 2017 + Bullock 2023 may have partial data)
- Infiltrate with Paraguayan DINAC station data (network of ~25 weather stations)

## Action items

1. Cite SoilGrids 2.0 paper — Hengl 2017 (already in references.bib perhaps)
2. Cite Verra/SSP studies for soil-vegetation interactions
3. Future work: combine Sentinel-1 SAR + SoilGrids for finer-scale soil moisture mapping

## File locations

- NDC 3.0 covers soil and climate in `/opt/data/profiles/ivan/research/iterations/41-60-yvy/56_paraguay_ndc3_full_text_oct2025.md`
- World Bank CKP Paraguay climate cache: `/opt/data/profiles/ivan/research/iterations/76-90-tatakua/83_world_bank_climate_portal_paraguay.md`
