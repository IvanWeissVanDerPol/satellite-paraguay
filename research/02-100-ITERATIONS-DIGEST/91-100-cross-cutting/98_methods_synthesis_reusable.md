# 98. Methods Synthesis — Reusable Methods Inventory across 6 papers

**Date:** 2026-09-03

## Methods used in cited papers (organized by technique family)

### A. Computer vision / segmentation methods (Yvutu, Kai)

- **U-Net / U-Net++** (Ronneberger 2015) — base CNN for segmentation of forest loss / jaguar detection
- **Mask R-CNN** (He 2017) — instance segmentation for camera trap objects
- **SegFormer** (Xie 2021) — efficient transformer for land cover segmentation
- **Swin Transformer** (Liu 2021) — backbone for many 2024-2025 vision models
- **ConvNeXt** (Liu 2022) — modern CNN baseline
- **ViT** (Dosovitskiy 2021) — Vision Transformer backbone
- **Mask2Former, OneFormer** — universal image segmentation
- **CLIP-style pretraining** (Radford 2021) — vision-language pretraining for remote sensing
- **DINO, MAE, BEiT** — self-supervised pretraining methods applicable to Earth observation
- **YOLOv5, YOLOv8** — real-time detection baseline
- **Faster R-CNN, EfficientDet** — anchor-based detection baselines
- **YOLOv9, YOLOv10, RT-DETR** — newer real-time detectors
- **YOLOv11, YOLOv12** — even newer (2024-2025)

### B. Foundation model fine-tuning

- **LoRA / QLoRA** (Hu 2021) — parameter-efficient fine-tuning
- **Full fine-tuning, adapter tuning, prompt tuning** — spectrum of adaptation cost
- **TIES merging, Fisher merging** — model merging for domain adaptation
- **ICL (in-context learning)** — prompt-based adaptation
- **Linear probing, partial fine-tuning** — for foundation model evaluation

### C. Geospatial methods

- **Taskonomy-style task transfer** (Zamir 2018) — paper-relevant for R3 negative result
- **Domain generalization** (Muandet 2013, Ganin 2016) — out-of-distribution Earth observation
- **Self-supervised pretraining for time-series satellite** (Yuan 2021, Manas 2021)
- **Contrastive multimodal earth observation** (Mall et al., Stewart et al.)

### D. Statistical / causal methods

- **Synthetic control method** (Abadie 2003, Abadie 2010) — used in West 2023 for REDD+ assessment
- **Difference-in-differences** (Bertrand 2004)
- **Propensity score matching** (Rosenbaum 1983)
- **Instrumental variables** (Imbens 2015)
- **Bayesian hierarchical models** (Gelman 2013)
- **Spatial regression** (LeSage 2009)
- **Geographically weighted regression** (Brunsdon 1996)
- **Lasso, ridge, elastic net** — regularization methods

### E. PM2.5 / atmospheric methods (Tatakua)

- **WRF-Chem regional chemical transport modeling** (Grell 2005)
- **GEOS-Chem global model** (Bey 2001)
- **TROPOMI trace gas retrievals** (Hasekamp 2019 for CO/HCHO)
- **Satellite-based PM2.5 estimates** (van Donkelaar 2010, Hammer 2020)
- **Deep learning hybrid (CNN + LSTM) for air quality** (e.g., Bai 2022)
- **Random forest + statistical downscaling**

### F. Policy / ethics methods (Yvy, Vyrá)

- **CARE principles operationalization** (Carroll 2020, Hudson 2023)
- **FPIC implementation frameworks** (FAO 2016, UN 2007/2008)
- **Carbon credit integrity assessment** (West 2023, Hegebart 2024, Streck 2021)
- **Indigenous Knowledge classification frameworks** (Beauchamp 2021, Iwasaki 2009)

## Recommended methodology for each paper

| Paper | Method Stack | Why |
|---|---|---|
| Yvutu | Prithvi-EO-2.0 fine-tune OR AlphaEarth embeddings → U-Net head → dropout ablation | Comparing foundation-model approaches to custom CNN is publishable |
| Vyrá | Verra API scrape + Hansen + NDVI time series + synthetic control + t-test for baseline emission | Carbon credit integrity is mostly statistics + remote sensing |
| Yvy | MegaDetector-style + FPIC interviews (qualitative) + Indigenous data sovereignty framework | Mixed methods; ethical |
| Kai | MegaDetector V6 + PyTorchWildlife + GBIF + Wilson-MacEachern camera trap data + transit counts | Standard wildlife ML pipeline |
| Yrupe (400/100 failure-mode) | Modis-NDVI + linear regression + Lasso + failure analysis | All about process, not results |
| Tatakua | TROPOMI NO2 + CAMS + ERA5 + OpenAQ + LSTM + LASSO reconstruction | Standard air-quality ML pipeline |

## Methods NOT used (potential future thesis extensions)

- Bayesian neural networks (PINNs for physical consistency)
- Causal forests (Wager 2018)
- Phenology-based crops models (CropStat)
- Vision-language models for environmental reporting
- Federated learning for cross-country training
