# 97. Data Sources Inventory — Comprehensive list for all 6 papers

**Date:** 2026-09-03

## Data sources to integrate into the thesis pipeline

### A. Forest cover + land use (Yvutu, Vyrá, Yvy)

| Dataset | Provider | Resolution | Period | Free? | Paraguay Ready? |
|---|---|---|---|---|---|
| Hansen GFC v1.11 | UMD/MD | 30m | 2000-2023 | Yes | Yes |
| MapBiomas Chaco Collection 1 | MapBiomas | 30m | 2000-present | Yes | Yes (subproject) |
| MapBiomas Paraguay Collection 1 | MapBiomas | 30m | 2000-present | Yes | Yes |
| Dynamic World | Google | 10m | 2015-present | Yes | Yes |
| ESA WorldCover | ESA | 10m | 2020-2025 | Yes | Yes |
| ESRI Global Land Use Land Cover | ESRI | 10m | 2020-present | Yes | Yes |
| PALSAR-2 FNF4 | JAXA | 25m | 2017-2021 | Yes | Yes |
| PALSAR-2 Global 25m forest classification | JAXA | 25m | 2025 | Yes | Yes |
| Google Satellite Embedding V1 (AlphaEarth) | Google DeepMind | 10m | 2017-2024 | Yes (via GEE) | Yes |
| GEDI L4A v2.1 | NASA / USFS | 25m | 2019-present | Yes | Yes |
| GEDI L4A v3 | NASA / USFS | 25m | 2019-present | Yes | Yes |
| Global Pasture Watch | UMD | 30m | 2000-2022 | Yes | Yes |
| Tierras Indigenas map | FAPI | vector | 2018-present | Yes | Yes (Paraguay only) |
| Paraguayan national forest inventory 2026 | INFONA | field measurements | 2026 release | Free, request-based | Yes |

### B. Atmospheric / fire / air quality (Tatakua)

| Dataset | Provider | Resolution | Period | Free? | Paraguay Ready? |
|---|---|---|---|---|---|
| Sentinel-5P TROPOMI L2 | ESA | 3.5 × 5.5 km | 2018-present | Yes | Yes |
| TROPOMI L3 NRT | Copernicus | 5.5 × 3.5 km | 2018-present | Yes | Yes |
| MOPITT CO | NASA | 22 km | 2002-present | Yes | Yes |
| VIIRS Active Fire | NASA | 375m | 2012-present | Yes | Yes |
| MODIS MCD14ML | NASA | 1km | 2002-present | Yes | Yes |
| GFEDv5 fire emissions | ECMWF / GFED | 0.25° | 1997-present | Yes | Yes |
| CAMS Global Reanalysis | ECMWF | 0.4° | 2003-present | Yes | Yes |
| ERA5 | ECMWF | 0.25° | 1950-present | Yes | Yes |
| MERRA-2 | NASA GMAO | 0.5° × 0.625° | 1980-present | Yes | Yes |
| OpenAQ ground stations | OpenAQ | various | 2012-present | Yes | Partial (Asunción, Cuidad del Este) |
| IQAir ground stations | IQAir | various | 2016-present | Limited | Partial |
| CHIRPS rainfall | UCSB | 0.05° | 1981-present | Yes | Yes |

### C. Wildlife / camera-trap (Kai)

| Dataset | Provider | Type | Free? |
|---|---|---|---|
| MegaDetector V5/V6 | Microsoft / AI for Good | Pre-trained detection | Yes (MIT license) |
| MegaDetector-Classifier | Microsoft / AI for Good | Fine-tuning | Yes |
| LILA-BC | Camera trap archive | 10M+ labeled images | Yes (registration) |
| Wildlife Insights | Google + WCS | Platform | Yes |
| Snapshot Safari | Princeton | Dataset | Yes |
| GBIF | Global | Occurrences | Yes |
| IUCN Red List | IUCN | Conservation status | Yes |

### D. Agricultural / carbon / yield (Vyrá, Yrupe)

| Dataset | Provider | Type | Free? | Paraguay? |
|---|---|---|---|---|
| Verra Registry | Verra | Carbon credit projects | Yes (registry API) | Yes |
| Apify Verra + Gold Standard scraper | Apify | Carbon project aggregation | Yes (no account) | Yes |
| Sylvera ratings | Sylvera | Carbon project rating | No (paid) | Limited |
| BeZero ratings | BeZero | Carbon project rating | No (paid) | Limited |
| Faostat | FAO | Global agricultural statistics | Yes | Yes |
| Paraguayan Ministry of Agriculture (CAPECO, INBIO) | Local | Soy production data | Free / partial | Yes |
| Modis-NDVI | NASA | 250m NDVI | Yes | Yes |
| GlobSnow | Various | Snow cover (less relevant) | Yes | Limited |

### E. Indigenous / FPIC (Yvy)

| Dataset | Provider | Type | Free? |
|---|---|---|---|
| LandMark | RFN / SDI / WRI | Global Indigenous + Community Land boundaries | Yes |
| ICCA Registry | ICCA Consortium | Indigenous Community Conserved Areas | Yes |
| FAPI Tierras Indigenas | FAPI Paraguay | Paraguay Indigenous lands map | Yes |
| FAPI Centro de Documentación | FAPI | Indigenous land rights docs | Yes |
| IWGIA Indigenous World | IWGIA | Annual country reports | Yes |
| Minority Rights Group | MRG | Country profiles | Yes |
| Survival International | NGO | Specific peoples (Ayoreo) | Yes |
| INDI Paraguay (state) | Paraguay government | Indigenous registry | Partial |

## Datasets NOT in cache that need fetching next

- Hargreaves et al. SBT climate change Chaco scenario paper (for Tatakua PM2.5 future projections)
- SARAIH dataset (Southeast Asian smoke — irrelevant to Paraguay but useful method comparison)
- South American fire driver: Aragão et al. (2014) linking deforestation to fire activity in South America
- Stefanescu et al. (2023) CFAS South American fire attribution system
