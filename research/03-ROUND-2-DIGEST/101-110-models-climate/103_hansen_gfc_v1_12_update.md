# 103. Hansen GFC v1.12 — Yvutu Dataset Updates 2024

**Date:** 2026-09-03 (Round 2)

## Overview

The UMD Global Forest Change (GFC) team continues to release updated versions of the Hansen dataset. **v1.12 was released in 2024**, adding forest cover data for 2022 and 2023.

### New in v1.12 (2024)
- Baseline year 2000 (unchanged from v1.7+)
- Updated tree cover 2000 (Hansen et al. 2013)
- Updated yearly gain/loss through **2023**
- Updated "year of gross forest cover loss" band
- Updated forest cover gain "2000-2020" to "2000-2024"
- Same methodology: Landsat 7 ETM+ (2000-2012), Landsat 8 OLI (2013-2021), Landsat 9 OLI-2 (2022-)

### Download

```
For Python notebook (pip install wri-change-api or rasterio):
```python
import rasterio
# Download year-of-loss tile from UMD GEE archive
```

The dataset is also available via:
- **GEE catalog:** `UMD/hansen/global_forest_change_2023_v1_12`
- **File:** `ee.Image("UMD/hansen/global_forest_change_2023_v1_12")`
- **Tile-level download:** UMD GFC archive (https://storage.googleapis.com/earthenginepartners/)

## Implications for Yvutu analysis

| Yvutu version | Baseline | End year | Loss/gain classification |
|---|---|---|---|
| v1.7 (2019) | 2000 | 2018 | Functional but stale |
| v1.9 (2021) | 2000 | 2020 | Functional |
| v1.10 (2023) | 2000 | 2022 | Functional |
| v1.12 (2024) | 2000 | **2023** | Current |

For Yvutu thesis (Sept 2026), use v1.12.

## Citations needed

- Hansen, M.C., et al. (2013). "High-Resolution Global Maps of 21st-Century Forest Cover Change." *Science* 342(6160): 850-853.
- Hansen, M.C., et al. (2023). "Version 1.10 update." (no formal paper; UMD README update).

## Cache landing

The Hansen GFC v1.12 catalog entry is documented in `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/19_hansen_gfc_v1.9_2021.md` (note: this file documents v1.9; v1.12 is structurally identical so the methodology references are reusable).

## Action items

1. Run `ee.Image("UMD/hansen/global_forest_change_2023_v1_12")` in the Yvutu pipeline
2. Adjust end-of-period aggregations (2017-2021 → 2017-2023)
3. Re-run validation against Bullock 2023 GEDI biomass values (which used v1.8?)
4. Use 2022-2023 to test model sensitivity to the most recent deforestation pressure

## Gaps remaining

- Need to verify whether v1.12 changed methodology for "year of gross forest cover loss event" vs older versions (likely no, but worth checking)
- Assessment of Landsat 9 OLI-2 calibration continuity
- Paraguay-specific loss magnitudes 2022-2023
- Whether Hansen v1.12 corrected for any stripe artifacts known from earlier versions
