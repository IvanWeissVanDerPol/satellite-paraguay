# Data Sheet — Sentinel-2

**Dataset:** Sentinel-2 Level-2A (Surface Reflectance)
**Provider:** ESA Copernicus
**License:** CC0 (free and open)
**URL:** https://sentinel.esa.int/web/sentinel/missions/sentinel-2

## Motivation

This dataset provides 10m resolution multi-spectral imagery for vegetation monitoring, land cover classification, and biophysical parameter estimation.

## Composition

- **Spatial coverage:** Global (Paraguay covered by 18 deptos, 268 distritos)
- **Temporal coverage:** 2015-present (Sentinel-2A launched 2015, Sentinel-2B launched 2017)
- **Spatial resolution:** 10m (visible/NIR), 20m (red edge/SWIR), 60m (coastal/aerosol/QA)
- **Temporal resolution:** 5-day revisit (combined A+B)
- **Tile size:** 100x100 km (UTM zones, MGRS grid)
- **Number of bands:** 13 (12 spectral + 1 QA)

## Collection process

- **Sensor:** Multispectral Imager (MSI)
- **Platform:** Sentinel-2A and Sentinel-2B satellites
- **Processing:** Sen2Cor atmospheric correction (L2A)
- **Cloud masking:** s2cloudless (separate tool) or SCL band

## Uses

- Land cover classification (P0011, P0100, P0025)
- Vegetation health (NDVI/EVI time series)
- Crop monitoring
- Forest change detection
- Water body mapping

## Distribution

- **API:** Copernicus Open Access Hub (https://scihub.copernicus.eu)
- **Alternative:** Google Earth Engine (https://earthengine.google.com)
- **Format:** GeoTIFF (JPEG2000 also available)
- **File size:** ~800 MB per tile per acquisition

## Maintenance

- Updated daily by ESA
- Long-term archive guaranteed (ESA commitment)

## Limitations

- Clouds block optical view (need s2cloudless + temporal compositing)
- Shadows affect classification accuracy
- Requires atmospheric correction for biophysical parameter retrieval
- 10m resolution limits small-scale mapping

## Ethical considerations

- Public/CC0 — no consent required
- Privacy: 10m resolution may capture individual buildings
- Used for: conservation, agriculture, urban planning
