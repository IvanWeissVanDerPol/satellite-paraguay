# Data Sheet — Landsat

**Dataset:** Landsat 8/9 Collection 2 Level-2 Science Products
**Provider:** USGS + NASA
**License:** Public (CC0)
**URL:** https://www.usgs.gov/landsat

## Motivation

Landsat provides the longest-running Earth observation record (1972-present). Critical for Paraguay time-series analysis (1985-2024 MapBiomas, 2000-2023 Hansen).

## Composition

- **Spatial coverage:** Global
- **Temporal coverage:** Landsat 1-9 (1972-present), L9 active since 2021
- **Spatial resolution:** 30m (multispectral), 15m (pan), 100m (thermal)
- **Temporal resolution:** 16-day revisit
- **Tile size:** 185x180 km (WRS-2 path/row)
- **Bands:** 11 (L8/L9 OLI + TIRS)

## Collection process

- Optical sensors (OLI, TIRS)
- 705 km sun-synchronous orbit
- 16-day revisit
- Atmospheric correction (LaSRC for L2)

## Uses

- Input to MapBiomas (P0011, P0025)
- Input to Hansen GFC (P0011)
- Long-term time series
- Pre-Sentinel-2 era studies

## Distribution

- **EarthExplorer:** https://earthexplorer.usgs.gov/
- **GEE:** LANDSAT/LT05/C02/T1_L2, LANDSAT/LC08/C02/T1_L2, LANDSAT/LC09/C02/T1_L2
- **Format:** GeoTIFF
- **Free** with USGS registration

## Maintenance

- Active (Landsat 9 operational)
- Continuity assured through Landsat Next (~2030)

## Limitations

- 30m resolution (coarser than Sentinel-2)
- 16-day revisit (slower than S2's 5-day)
- Cloud cover affects optical observations

## Ethical considerations

- Public — no consent required
- Used for: agriculture, forestry, urban planning, climate research
