# Data Sheet — MapBiomas Paraguay

**Dataset:** MapBiomas Paraguay Collection
**Provider:** MapBiomas (with Paraguay partnership)
**License:** CC0
**URL:** https://plataforma.mapbiomas.org/

## Motivation

Provides annual land cover maps for Paraguay from 1985-2024, used as ground truth for satellite CV validation.

## Composition

- **Spatial coverage:** Paraguay (all 18 deptos)
- **Temporal coverage:** 1985-2024 (40 years)
- **Spatial resolution:** 30m
- **Classes:** 10+ land cover classes (forest, agriculture, urban, water, etc.)
- **Update frequency:** Annual (1-2 year lag)

## Collection process

- **Method:** Random Forest per-pixel classification of Landsat time series
- **Input data:** Landsat 5/7/8/9
- **Training data:** Expert-labeled samples (~5,000 per class)
- **Validation:** Independent validation samples

## Uses

- Ground truth for P0011 Yvytu (Chaco deforestation)
- Ground truth for P0025 Yrupe (soybean mapping)
- Historical analysis (1985-2024)

## Distribution

- **Download:** https://storage.googleapis.com/mapbiomas-public/paraguay/
- **Format:** GeoTIFF (per year)
- **File size:** ~50 MB per year for Paraguay

## Maintenance

- Updated annually
- Coordinated by MapBiomas Paraguay team

## Limitations

- 30m resolution (coarser than Sentinel-2)
- Classification accuracy varies by class
- Annual — misses intra-year changes
- Some classes conflated (e.g., grassland vs pasture)

## Ethical considerations

- Public/CC0 — no consent required
- No personal data
