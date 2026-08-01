# Data Sheet — Hansen Global Forest Change

**Dataset:** Hansen GFC v1.11 (2023)
**Provider:** Global Forest Watch (GFW)
**License:** CC0
**URL:** https://www.globalforestwatch.org/

## Motivation

Global annual forest loss/gain maps from 2000-present, used as ground truth for deforestation validation.

## Composition

- **Spatial coverage:** Global (Hansen tiles for Paraguay)
- **Temporal coverage:** 2000-2023
- **Spatial resolution:** 30m
- **Bands:**
  - treecover2000: tree canopy cover in 2000 (0-100%)
  - loss: forest loss (binary 0/1)
  - lossyear: year of loss (0-23)
  - gain: forest gain (binary 0/1)
  - first (and others)

## Collection process

- **Method:** Landsat time series analysis
- **Input data:** Landsat 7 ETM+ (2000-2013), Landsat 8 OLI (2013-present)
- **Reference:** Year 2000 baseline

## Uses

- Ground truth for P0011 Yvytu (Chaco deforestation)
- Cross-validation with MapBiomas
- Long-term deforestation trends

## Distribution

- **Download:** https://storage.googleapis.com/earthenginepartners-hansen/
- **GEE:** `UMD/hansen/global_forest_change_2023_v1_11`
- **Format:** GeoTIFF (per Hansen tile)
- **File size:** ~200 MB per Hansen tile for Paraguay

## Maintenance

- Updated annually by Hansen lab + Global Forest Watch

## Limitations

- "Loss" definition is binary (any canopy reduction)
- Does not distinguish cause of loss (deforestation vs fire)
- Cloud cover affects detection
- 30m resolution (matches Landsat)

## Ethical considerations

- Public/CC0 — no consent required
- Used for: conservation, climate policy, REDD+ accounting
