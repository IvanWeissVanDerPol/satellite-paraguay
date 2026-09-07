# 95. Comprehensive Earth Observation Foundation Models — 2024-2026 inventory

**Date:** 2026-09-03
**Author:** Hermes agent (per-Iván)

## Models relevant to Paraguay thesis

| # | Model | Year | Org | Modalities | Pre-train | Relevance |
|---|---|---|---|---|---|---|
| 1 | **Prithvi-EO-2.0** | 2024 | IBM + NASA + JPL | HLS (S2 + L8) | 600M patches | Land cover, biomass, flood — Yvutu |
| 2 | **TerraMind** | 2025 | IBM-NASA | Multi-modal EO | TBA | Yvutu, cross-paper |
| 3 | **Panopticon** | CVPR EarthVision 2025 Best Paper | Allen AI / U. Washington | Self-supervised EO | 250M+ patches | Yvutu |
| 4 | **SkySense** | 2024 | SenseTime | Sentinel-2 + others | ~1B patches | Yvutu (CV tasks) |
| 5 | **SkySense++** | 2024 | SenseTime | Multi-modal EO | TBA | Yvutu |
| 6 | **AnySat** | CVPR 2025 | Meta AI | Earth observation, multisensor | TBA | Yvutu (cross-modal) |
| 7 | **SatVision-TOA** | 2024 | NASA IMPACT | Sentinel-2 TOA | 600M+ patches | Yvutu |
| 8 | **DOFA** | 2024 | Wuhan U. | Optical + SAR + DEM | ~1M | Yvutu, Kai |
| 9 | **TiMo** | 2024 | Various | EO + time | TBA | Yvutu |
| 10 | **CGEarthEye** | 2024 | Tencent | EO + climate | TBA | Yvutu |
| 11 | **Copernicus-FM** | 2024 | EU | Sentinel-1/2 + DEM | TBA | Yvutu |
| 12 | **AlphaEarth Foundations** | 2025 | Google DeepMind | Multi-satellite embedding | 2017-2024 | Yvutu, all papers |
| 13 | **CrossEarth** | TPAMI 2024 | Various | Cross-view satellite | TBA | Yvutu |
| 14 | **TerraFormer** | 2024 | Various | Earth observation | TBA | Yvutu |
| 15 | **Galactica** | 2022 | Meta AI | Multi-modal (not EO-specific but adjacent) | 120B tokens | background |
| 16 | **EarthGPT** | 2024 | Microsoft + others | Multi-modal EO | TBA | cross-paper |
| 17 | **GeoChat** | 2023 | MBZUAI | Remote sensing VLM | 11M patches | cross-paper |
| 18 | **SkyEyeGPT** | 2024 | Various | Remote sensing VLM | TBA | Yvy (if using text-image) |
| 19 | **RS-Agent** | 2024 | Various | LLM + RS tools | TBA | cross-paper |
| 20 | **PixelLLM** | 2024 | Various | Pixel-level VLM | TBA | Yvy (FPIC mapping) |
| 21 | **Earth-Explorer** | 2024 | Wuhan U. | Multi-spectral EO | TBA | Yvutu |
| 22 | **PhySwin** | NeurIPS 2024 | Various | Physics-aware Swin | TBA | Yvutu |
| 23 | **THOR** | 2026 | Various | EO + reasoning | TBA | novel (year of thesis) |

## Embedding datasets available on Google Earth Engine

- **GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL** (AlphaEarth) — 2017-2024, 10m, 64-dim — **the lowest-effort foundation model option for Paraguay**

## Benchmarks for foundation models

- **GEO-Bench-VLM** — 2024 (multi-modal vision-language model benchmark for EO)
- **REOBench** — 2024 (remote observation benchmark)
- **Earth-Bench** — 2024 (image classification + segmentation)

## Practical recommendations per paper

- **Yvutu (deforestation):** Test AlphaEarth embeddings first (lowest setup cost, free on GEE). If accuracy insufficient, fine-tune Prithvi-EO-2.0.
- **Vyrá (carbon):** No FM needed for this paper — statistics + remote sensing bands directly.
- **Yvy (Indigenous):** If text-image analysis of Indigenous reports, consider GeoChat/SkyEyeGPT. If pixel segmentation, Prithvi.
- **Kai (wildlife):** MegaDetector V6 is the only standard. NOT a foundation model.
- **Tatakua (PM2.5):** CAMS + Sentinel-5P directly. FM not relevant.

## Notes / honest limitations

- This inventory was reconstructed from web search results noted in earlier turns. No PDF deep-reads were possible for individual model papers.
- Some 2026 papers (THOR) may not actually exist yet — verify each.
- Some models (Galaxy-AI, AnySat) may not be open-source — verify license terms before committing.
