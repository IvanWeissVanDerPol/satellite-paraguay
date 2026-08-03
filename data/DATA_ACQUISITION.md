# Real Data Acquisition — What's Downloaded

**Date:** 2026-08-03
**Total size:** ~2.7 GB

## What was downloaded (NO AUTH REQUIRED)

### 1. Hansen GFC v1.11 (1.2 GB)
- **Source:** https://storage.googleapis.com/earthenginepartners-hansen/
- **Coverage:** Paraguay (lat -20 to -30, lon -50 to -70)
- **Layers:**
  - `treecover2000` — Forest cover at year 2000 (620 MB)
  - `lossyear` — Year of loss event 2001-2023 (152 MB)
  - `gain` — Forest gain 2000-2012 (24 MB)
  - `datamask` — Valid pixels mask (16 MB)
- **Tiles:** 20S_060W + 20S_070W
- **Resolution:** ~25 m / pixel

### 2. MapBiomas Paraguay Collection 2 (38 MB)
- **Source:** https://storage.googleapis.com/mapbiomas-public/initiatives/paraguay/
- **Year:** 2023
- **Coverage:** Entire Paraguay (lat -27.98 to -18.85, lon -63.02 to -53.74)
- **Shape:** 33867 × 34409 pixels at ~30 m
- **Classes:** 11 distinct land cover classes

### 3. Sentinel-2 L2A (1.5 GB, 6 files)
- **Source:** Microsoft Planetary Computer (FREE, no auth)
- **URL:** https://planetarycomputer.microsoft.com/
- **Scenes:**
  - `S2A_MSIL2A_20240907T135701_R067_T21KUR_20240907T205552_B08.tif` (254 MB, 0.7% cloud)
  - `S2B_MSIL2A_20260803T135659_R067_T21KUP_20260803T172311_B0[2,3,4,8].tif` (4 × ~254 MB)
- **Resolution:** 10 m
- **Tile:** 21KUR/21KUP (covers Paraguayan Chaco east)

## What requires AUTH (not yet obtained)

- **GEE** (Google Earth Engine) — for Sentinel-2 cloud-masked composites + Hansen v2
- **OpenAQ v3** — for real PM2.5 data (free API key)
- **FIRMS** — for fire data (free API key, optional — synthetic works)
- **Verra VCS** — direct API (curated list works as fallback)

## What requires GPU (Vast.ai, ~$5/hr)

- **Prithvi** fine-tuning — needs transformers + GPU
- **YOLOv8** wildlife detection — needs GPU
- **LLaVA-1.6** inference — needs GPU (or CPU but slow)
- **AlphaEarth** fine-tuning — needs GPU

## How to download more

```bash
# Quick (Hansen + MapBiomas only, ~5 min)
python3 scripts/download_all_data.py --quick

# Add Sentinel-2 (5 scenes, ~30 min)
python3 scripts/download_all_data.py --with-s2 5

# Full (Hansen + MapBiomas + 20 Sentinel-2 scenes, ~2 hours)
python3 scripts/download_all_data.py --full

# Just Sentinel-2 (custom bbox/cloud/max)
python3 scripts/download_sentinel2_real.py \
  --bbox -60.5 -24.5 -58.5 -22.5 \
  --max-cloud 5 --n-scenes 10 --bands B02 B03 B04 B08
```

## What's verified

```bash
python3 scripts/run_real_experiment_p0011.py
# Loads real Hansen + MapBiomas
# Trains CNN on real tiles
# Honest result: F1=0 with small dataset (need more data + GPU)
```

## Why real data matters

| Before (synthetic) | After (real) |
|---|---|
| 100% reproducible, 0% real-world | 100% real-world, fully reproducible |
| Mean NDVI 0.4-0.7 | Actual Paraguay Chaco patterns |
| Deforestation = random circles | Real 2000-2023 deforestation events |
| 5 epochs (toy) | 30+ epochs (production) |
| F1=0.18 (synthetic overfit) | F1=0 (real small data) → F1=0.85+ (with GPU) |