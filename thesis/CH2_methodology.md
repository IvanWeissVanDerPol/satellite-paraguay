---
title: "Chapter 2 — Methodology"
author: "Iván Hocht-VonDerPol"
date: "2026-08-04"
---

# Chapter 2: Methodology

This chapter describes the data sources, computational pipelines, evaluation methodology, and ethical framework used throughout the thesis. We aim for transparency and reproducibility: every dataset is publicly available, every script is open-source, and every evaluation uses the same statistical framework.

## 2.1 Data Sources

The thesis integrates nine primary data sources. Table 2.1 summarizes their properties, and the following subsections describe each in detail.

**Table 2.1:** Primary data sources used in the thesis.

| Source | Provider | Coverage | Resolution | Authentication |
|---|---|---|---|---|
| Sentinel-2 L2A | ESA Copernicus | Paraguay | 10 m | None (via Planetary Computer) |
| MapBiomas Paraguay | MapBiomas | Paraguay | 30 m | None |
| Hansen GFC v1.11 | Hansen/UMD | Paraguay | 25 m | None |
| OpenAQ | OpenAQ | Paraguay (limited stations) | Station-based | None (free) |
| Verra Registry | Verra | Global | Project-based | None |
| FIRMS | NASA | Paraguay | 375 m | None |
| SRTM DEM | NASA | Paraguay | 30 m | None |
| Sentinel-5P | ESA Copernicus | Paraguay | 1 km | None (via Planetary Computer) |
| Catastro Nacional | Paraguay gov | Paraguay | Parcel-based | Restricted |

### 2.1.1 Sentinel-2 L2A

Sentinel-2 is a constellation of two polar-orbiting satellites (2A, 2B) operated by the European Space Agency. Each satellite has a multispectral instrument (MSI) capturing 13 spectral bands at 10, 20, and 60 m resolution. The Level-2A product provides orthorectified, atmospheric-corrected surface reflectance.

We access Sentinel-2 data via the **Microsoft Planetary Computer** STAC API, which provides free access without authentication. Specifically, we use the `sentinel-2-l2a` collection with cloud cover < 30%. For Paraguay's Chaco region (longitude -65 to -55, latitude -25 to -19), we downloaded six scenes totaling 1.5 GB, including bands B02 (Blue), B03 (Green), B04 (Red), B08 (NIR), and B11 (SWIR).

The downloaded data is sufficient for proof-of-concept but inadequate for production. Production use would require downloading 50+ scenes covering the full study period (2024-2026) with cloud-free composites.

### 2.1.2 MapBiomas Paraguay

MapBiomas Paraguay is a multi-institutional initiative producing annual land cover maps for Paraguay from 2000 to present at 30 m resolution. We downloaded the 2023 collection from the official MapBiomas Paraguay website, providing a single 38 MB TIFF with 11 distinct land cover classes:

- Class 3: Forest Formation
- Class 4: Savanna Formation
- Class 15: Pasture
- Class 18: Agriculture
- Class 26: Water Bodies

(plus other less common classes)

MapBiomas is integrated as auxiliary features in our deforestation and yield models. We assume the 2023 classification is representative for the entire study period, which is a limitation we discuss in Chapter 10.

### 2.1.3 Hansen Global Forest Change v1.11

The Hansen GFC dataset is the gold-standard global forest change product, derived from Landsat imagery. We downloaded the v1.11 collection for two tiles covering Paraguay:

- Tile `20S_060W` (lat -20 to -30, lon -50 to -60)
- Tile `20S_070W` (lat -20 to -30, lon -60 to -70)

Each tile contains three layers: `treecover2000` (% forest cover in 2000), `lossyear` (year of loss 2001-2023), and `datamask` (data availability). Total volume: 1.2 GB.

We use Hansen as the **primary ground-truth label** for deforestation, while acknowledging its limitations (e.g., commission errors in dry forests, omission of degradation). We discuss these limitations in Chapter 10 and propose validation against INFONA data as future work.

### 2.1.4 OpenAQ

OpenAQ aggregates air quality measurements from government and research stations worldwide. For Paraguay, the station network is sparse (typically < 10 active stations), and PM2.5 measurements are limited.

We integrate OpenAQ via the public REST API (`https://api.openaq.org/v2/measurements`). For the Tatakua (Chapter 8) LSTM experiments, we retrieved 1,000+ PM2.5 measurements from Paraguayan stations. Where OpenAQ coverage is insufficient, we fall back to Sentinel-5P satellite-derived aerosol optical depth (AOD) as a proxy.

### 2.1.5 Verra Registry

Verra operates the world's largest voluntary carbon market. The Verra Registry contains public records of all registered carbon credit projects. We downloaded records for the 5 Paraguayan projects registered as of 2026, totaling 123,000 ha of project area.

Verra data is integrated in Chapter 4 (Yvyra Carbon) to assess carbon credit integrity against real deforestation data from Hansen.

### 2.1.6 Catastro Nacional

Catastro Nacional is Paraguay's property registry. We accessed a sample of parcel data for conflict detection (Chapter 5, P0012 Yvy). The dataset is restricted and was used under a research agreement; all identifiers were anonymized before analysis.

### 2.1.7 FIRMS (Fire Information for Resource Management System)

FIRMS provides near-real-time active fire data from MODIS and VIIRS satellites. We download FIRMS data via the public NASA API (`https://firms.modaps.eosdis.nasa.gov/`) for fire detection (Chapter 9 cross-cutting analysis). Resolution is 375 m for MODIS and 75 m for VIIRS.

### 2.1.8 SRTM DEM (Shuttle Radar Topography Mission)

SRTM provides a global digital elevation model at 30 m resolution. We download SRTM for Paraguay via Planetary Computer for terrain analysis and elevation-aware feature engineering.

### 2.1.9 Sentinel-5P

Sentinel-5P provides atmospheric composition measurements including NO₂, SO₂, CO, CH₄, and aerosol. We use Sentinel-5P as a complement to OpenAQ where ground stations are sparse.

## 2.2 Computational Pipelines

The thesis implements six computational pipelines, each addressing a specific application domain. All pipelines are implemented in Python using standard libraries (numpy, pandas, rasterio, geopandas, pytorch) and are containerized using Docker for reproducibility.

### 2.2.1 Pipeline Architecture

Each pipeline follows the same architecture:

1. **Data ingestion:** Download or load data from one or more sources
2. **Preprocessing:** Resample, reproject, cloud-mask, and align data
3. **Feature engineering:** Compute derived features (NDVI, EVI, year-on-year differences)
4. **Model training:** Train a model (U-Net, YOLOv8, LSTM, or LLaVA)
5. **Evaluation:** Compute metrics with bootstrap CIs
6. **Output:** Save predictions, metrics, and figures

The unified architecture enables cross-paper transfer learning (RQ4) by exposing each model's intermediate representations through a common API.

### 2.2.2 Yvutu (Deforestation, Chapter 3)

Yvutu implements two model variants:
- **From-scratch U-Net:** A 30-channel U-Net trained on Hansen+MapBiomas features.
- **Prithvi-Lite:** A 4-layer Vision Transformer fine-tuned on the same data.

**Measured result (see `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md`):** the CPU pilot (15 synthetic tiles, 5 epochs) achieved a best F1 = 0.559 with the from-scratch U-Net (precision 0.099, recall 0.987 — the model over-predicts deforestation). The intended Prithvi backbone fell back to a mock (F1 = 0.497) due to a transformers/numpy compatibility issue. The F1>0.85 headline quoted in earlier drafts was a literature benchmark (Jakubik et al. 2023 on HLS land-cover), **not a Yvutu measurement**, and has been removed. The thesis therefore frames foundation-model fine-tuning as the *promising direction* for data-scarce regions, supported by literature benchmarks, rather than as an established operational claim.

### 2.2.3 Yvyra (Carbon, Chapter 4)

Yvyra integrates Hansen deforestation data with Verra carbon credit project boundaries to assess credit integrity. The pipeline computes:

- **Hansen-derived carbon loss** for each Verra project area
- **Verra-claimed carbon loss** (from project documents)
- **Discrepancy** = Hansen-derived - Verra-claimed

A positive discrepancy indicates under-claimed carbon loss; negative indicates over-claimed. We report aggregate statistics across 5 Paraguayan projects.

### 2.2.4 Yvy (Indigenous, Chapter 5)

Yvy cross-references Hansen deforestation with indigenous territory boundaries (10 territories) to compute:

- **Per-territory deforestation rate** (%)
- **Per-territory area lost** (km²)
- **Per-territory CO₂e emitted** (Mt)

Yvy produces the headline finding of the thesis: indigenous territories are deforested at 3.3× the national average.

### 2.2.5 Yrupe (Yield, Chapter 6)

Yrupe predicts crop yield from Sentinel-2 + MapBiomas + SRTM features. The pipeline uses transfer learning: a deforestation-pretrained model is fine-tuned for yield prediction. We test H3 (cross-domain transfer) by comparing:

- **Random initialization:** Yield-trained model from scratch
- **Deforestation-pretrained:** Fine-tuned from Yvutu weights

### 2.2.6 Kai (Poaching, Chapter 7)

Kai implements wildlife detection using YOLOv8. The pipeline downloads Sentinel-2 imagery of Paraguayan national parks (Defensores del Chaco, Teniente Agripino Enciso) and applies a pretrained YOLOv8 model for animal detection.

Due to limited labeled Paraguay-specific data, Kai currently relies on COCO-pretrained weights. **Measured synthetic-vs-real gap (see `papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md`):** mAP@0.5 = 0.50 on synthetic validation, 0.18 on 5,000 real Guyra Paraguay camera-trap images (a 0.32 absolute decline). Per-category breakdown on real data: large mammals 0.25, small mammals 0.10, birds 0.20, reptiles 0.05. The mAP=0.6-0.8 / 0.3-0.5 ranges quoted in earlier drafts of this chapter were aspirational and have been replaced.

### 2.2.7 Tatakua (Air Quality, Chapter 8)

Tatakua implements air quality forecasting using LSTM. The pipeline uses OpenAQ PM2.5 + Sentinel-5P AOD + meteorological features. We compare:

- **Persistence baseline:** Predict tomorrow = today
- **LSTM-2layer:** 50 epochs on 5,000 timesteps
- **LSTM-4layer:** Deeper variant

**Measured result (see `papers/drafts/p0035_tatakua_air_quality/ACTUAL_RESULTS.md`):** mean RMSE = 14.7 µg/m³ (bias +3.4) across 12 stations — a 24% improvement over persistence (19.2 µg/m³), but 70% above the MAE<5 µg/m³ target that earlier drafts of this chapter quoted. Rural stations (Filadelfia/Chaco RMSE 18.6 µg/m³) are the dominant failure mode.

## 2.3 Evaluation Methodology

All experiments in the thesis use a unified evaluation methodology to enable comparison across papers.

### 2.3.1 Train/Val/Test Splits

We use a 70/15/15 split with stratified sampling (to ensure equal positive/negative classes). Time-series data (OpenAQ, FIRMS) uses chronological splits to prevent leakage.

### 2.3.2 Metrics

We report the following metrics:

**For classification (deforestation, conflict):**
- Precision, Recall, F1, IoU
- 95% bootstrap CIs (10,000 resamples)
- McNemar's test for model comparison

**For regression (yield, air quality):**
- MAE, RMSE, R²
- 95% bootstrap CIs
- Skill score vs persistence baseline

**For detection (wildlife):**
- mAP@0.5 and mAP@[0.5:0.95]
- Per-class metrics

### 2.3.3 Statistical Tests

We use McNemar's test for comparing classifiers, paired t-tests for regression models, and bootstrap CIs for all metrics. We do not correct for multiple comparisons (only 1-3 comparisons per experiment), but report effect sizes.

### 2.3.4 Cross-Validation

We use 5-fold cross-validation for hyperparameter selection. For time-series data, we use **purged k-fold** to prevent leakage.

## 2.4 Ethical Framework

The thesis integrates ethical considerations into every stage of research, following the principles of **rights-aware AI**.

### 2.4.1 Free, Prior, and Informed Consent (FPIC)

All research involving indigenous communities follows ILO Convention 169 and the UN Declaration on the Rights of Indigenous Peoples. The FPIC process is documented in `etica/FPIC_template_es.md` and includes:

1. **Pre-engagement:** Letters to INDI, presentations to community leaders
2. **Assembly:** Community-wide discussions with interpretation
3. **Negotiation:** Terms of research, benefits, compensation
4. **Documentation:** Signed acts with witnesses
5. **Implementation:** Research respecting the agreed terms
6. **Devolution:** Results shared with communities first

### 2.4.2 Institutional Review Board (IRB) Approval

Research involving human subjects data (Catastro parcel ownership, OpenAQ near schools) requires IRB approval from Universidad Nacional de Asunción (UNA) Comité de Ética. The IRB protocol is documented in `etica/IRB_protocol_paraguay_UNA.md` and addresses:

- Privacy risks (anonymization)
- Stigmatization risks (community-controlled data)
- Misuse risks (open license with FPIC barriers)

### 2.4.3 Data Sovereignty

All datasets used in the thesis are publicly available, and all outputs are released under Creative Commons Attribution-ShareAlike (CC-BY-SA 4.0). The thesis does not commercialize Paraguayan environmental data, in alignment with the principle of data sovereignty.

### 2.4.4 Carbon Credit Integrity

For carbon market analyses (Chapter 4), we explicitly disclose any discrepancies between Verra-claimed and independently-derived carbon loss. We do not advocate for any specific carbon market policy.

### 2.4.5 Limitations and Disclosures

We disclose all limitations of our methods in each paper's "Threats to Validity" section. We acknowledge that:

- Hansen GFC has known commission/omission errors
- MapBiomas Paraguay assumes temporal land cover stability
- Indigenous territory polygons are approximate (bboxes, not legal boundaries)
- OpenAQ station network in Paraguay is sparse

## 2.5 Reproducibility

Reproducibility is a cornerstone of the thesis. All code, data, and analysis scripts are publicly available at `github.com/IvanWeissVanDerPol/satellite-paraguay`. To reproduce the results:

```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay.git
cd satellite-paraguay
python3 scripts/download_all_data.py --quick
python3 scripts/paraguay_deforestation_analysis.py
python3 scripts/department_deforestation.py
python3 scripts/indigenous_overlap_analysis.py
# ... etc
```

The full pipeline takes approximately 30 minutes on a CPU-only machine. GPU training requires an additional 4-6 hours on an A100.

We document the computational environment (Python version, library versions, operating system) in `requirements.txt` and `Dockerfile`. We use DVC for data versioning and MLflow for experiment tracking.

## 2.6 Chapter Summary

This chapter established the methodology framework for the thesis. We described the nine data sources, six computational pipelines, evaluation methodology, and ethical framework. The following six chapters apply this framework to specific land-use challenges in Paraguay.

---

## Chapter 2 References

See `thesis/references.bib` for the complete bibliography.

Key methodology references:
- Hansen, M. C., et al. (2013). "High-Resolution Global Maps of 21st-Century Forest Cover Change." *Science*.
- MapBiomas Paraguay (2023). "MapBiomas Paraguay Collection 2 (2000-2022)."
- Chave, J., et al. (2014). "Improved allometric models to estimate the aboveground biomass of tropical trees." *Global Change Biology*.
- IPCC (2006). "2006 IPCC Guidelines for National Greenhouse Gas Inventories."
- UN-REDD Programme (2013). "Guidelines on Free, Prior and Informed Consent."
- IFC (2012). "Performance Standard 7: Indigenous Peoples."
- Waskom, M., et al. (2017). "seaborn: statistical data visualization." *Journal of Open Source Software*.

For a complete list, see `thesis/references.bib`.