# SatelliteCV-Paraguay

**One Python package → 6 peer-reviewed papers → 1 dissertation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests: pytest](https://img.shields.io/badge/tests-pytest-green.svg)](https://docs.pytest.org/)

## 🎯 Mission

Build a unified, open-source Python toolkit for multi-temporal earth observation of Paraguay, then use it to publish 6 peer-reviewed papers covering deforestation, carbon credits, agriculture, indigenous territory, wildlife conservation, and air quality — all sharing the same data pipeline, foundation models, and code infrastructure.

## 📄 The 6 papers

| ID | Title (Guaraní / English) | Journal | Lead author |
|----|---------------------------|---------|-------------|
| **P0011** | **Yvytu** — Multi-temporal satellite CV for Chaco deforestation alert system | Remote Sensing of Environment | Iván Weiss |
| **P0100** | **Yvyra** — Carbon-credit verification (satellite CV + Paraguay farms) | Nature Climate Change | Iván Weiss |
| **P0025** | **Yrupe** — Soybean yield prediction with Sentinel-2 + GRU/LSTM in Caaguazú | Computers and Electronics in Agriculture | Iván Weiss |
| **P0012** | **Yvy** — Indigenous community territory mapping with participatory cartography + GPT-4 enrichment | World Development | Iván Weiss |
| **P0026** | **Kai** — Wildlife poaching detection (YOLO/COCO-zoo + drone CV in Defensores del Chaco) | Conservation Biology | Iván Weiss |
| **P0035** | **Tatakua** — Air-quality forecasting for Asunción (LSTM + OpenAQ + PM2.5 satellite) | Atmospheric Environment | Iván Weiss |

## 🏗️ Architecture

```
satellite-paraguay/
├── data/
│   ├── raw/                # Sentinel-2 tiles, Planet imagery (DVC-tracked)
│   ├── processed/          # Cloud-masked, NDVI/EVI composites
│   ├── external/           # Hansen, MapBiomas, Catastro, OSM
│   └── cache/              # Pre-computed embeddings (Prithvi, AlphaEarth)
├── src/
│   ├── satellite_io/       # Download + preprocess Sentinel-2 / Landsat / Planet
│   ├── paraguay_admin/     # Load 18 deptos, 268 distritos, 7,912 tiles, Catastro
│   ├── foundation_models/  # Prithvi (IBM-NASA), AlphaEarth (Google), DINOv2
│   ├── parcel_analysis/    # Catastro intersection + buffer
│   ├── timeseries/         # Multi-temporal stacking + change detection
│   ├── evaluation/         # F1/IoU metrics + benchmarks (vs MapBiomas)
│   └── papers/             # One folder per paper with shared entry points
├── notebooks/              # Jupyter exploration
├── dashboard/              # Streamlit unified dashboard (live map)
├── tests/                  # pytest unit tests
├── configs/                # Hydra / OmegaConf YAML configs per paper
├── models/checkpoints/     # Trained model weights (DVC-tracked)
├── outputs/                # Figures, tables, intermediate results
├── papers/drafts/          # Markdown drafts
├── papers/figures/         # Final figures for papers
└── logs/                   # Training logs, evaluation logs
```

## 🚀 Quick start

### 1. Install

```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay
cd satellite-paraguay
make install
```

### 2. Verify

```bash
make verify
```

### 3. Run first notebook

```bash
make notebook-paper-1
```

### 4. Train first model

```bash
make paper-1-train
```

### 5. Generate dashboard

```bash
make dashboard
```

## 💾 Data sources (all open-source)

### Already local (in `/root/paraguay-geodata/`)

| Asset | Size | Count |
|-------|------|-------|
| `tile_index.json` | 3.6 MB | 7,912 tiles (10×10 km each) |
| `roads.geojson` | 5.6 MB | 14,835 OSM roads |
| `buildings_asuncion.geojson` | 13 MB | 49,641 OSM buildings |
| `catastro_parcels.geojson` | 4.4 MB | 7,500 Catastro parcels |
| `properties_latest.geojson` | 14 MB | 10,898 listings |
| `hillshade_*.jpg` | dozens | DEM hillshades (Copernicus GLO-30) |
| `indigenous_territories.geojson` | 8 KB | Indigenous territories |
| `climate_risk.geojson` | 36 KB | Climate risk layer |
| `gbif_paraguay.geojson` | 96 KB | 200 species (biodiversity) |
| `inbio_zafra_2025_2026.json` | 4 KB | Crop area (INBIO) |

### Online (free, fetched by `make data`)

| Asset | Source | License |
|-------|--------|---------|
| Sentinel-2 (10m, 5-day) | ESA Copernicus | CC0 |
| Landsat 9 (30m) | NASA | CC0 |
| Planet (3m academic) | Planet | CC BY-NC academic |
| MapBiomas Paraguay | MapBiomas | CC0 |
| Hansen GFC | GFW | CC0 |
| ESA WorldCover | ESA | CC0 |
| WorldClim | WorldClim | CC0 |
| ERA5 | ECMWF | CC0 |
| Verra VCS Registry | Verra | Free public API |
| Gold Standard Registry | Gold Standard | Free |
| NASA FIRMS | NASA | CC0 |
| OpenAQ | OpenAQ | CC0 |
| INBIO (Paraguayan agri) | INBIO | Open |
| INFONA (Forestry) | INFONA | Open |

## 🤖 Models used (all open-source)

| Model | License | Used in paper |
|-------|---------|---------------|
| **Prithvi** (IBM-NASA) | Apache 2.0 | All 6 papers (foundation) |
| **AlphaEarth** (Google) | Free research | P0011, P0100 |
| **YOLOv8** | GPL-3.0 | P0026 Kai |
| **Detectron2** | Apache 2.0 | P0010/P0012 |
| **segmentation-models-pytorch** | MIT | P0011, P0100 |
| **Delineate Anything v2** | Open | P0025 Yrupe |
| **TimesFM** | Apache 2.0 | P0035 Tatakua |
| **GPT-4V / LLaVA-1.6** | MIT (LLaVA) | P0012 Yvy |

## 📅 Timeline

- **Phase 1 (Weeks 1-4):** Setup + data ingestion + foundation model embeddings
- **Phase 2 (Weeks 5-8):** Paper 1 (P0011 Yvytu) + Paper 5 (P0026 Kai)
- **Phase 3 (Weeks 9-12):** Paper 2 (P0100 Yvyra) + Paper 3 (P0025 Yrupe)
- **Phase 4 (Weeks 13-16):** Paper 4 (P0012 Yvy) + Paper 6 (P0035 Tatakua)
- **Phase 5 (Weeks 17-20):** Final integration, dashboard, thesis document

**Total:** 5 months for all 6 papers (parallel work where possible)

## 🎓 Dissertation structure

```
dissertation/
├── 01_introduction/
├── 02_literature_review/
├── 03_methodology/             # = src/satellite_io + src/foundation_models
├── 04_p0011_yvytu/
├── 05_p0100_yvyra/
├── 06_p0025_yrupe/
├── 07_p0012_yvy/
├── 08_p0026_kai/
├── 09_p0035_tatakua/
├── 10_integration/             # = dashboard/ unified platform
└── 11_conclusions/
```

## 📊 Validation

Each paper has a validation pipeline:

```bash
make paper-1-validate
make paper-2-validate
...
```

Metrics tracked:
- F1 / IoU (per paper)
- AUC-ROC (P0031 Karamanu)
- CER / WER (P0040 Kuatianee)
- mAP@0.5 (P0026 Kai)
- R² (P0010 Yvyra carbon)

## 🧪 Testing

```bash
make test           # all unit tests
make test-fast      # skip slow tests
make test-coverage  # with coverage report
```

## 📦 Deployment

```bash
make dashboard      # local Streamlit
make deploy-staging # staging server
make deploy-prod    # production
```

Dashboard lives at: https://satellite.paragu-ai.com

## 🤝 Contributing

We accept contributions to any of the 6 papers. See `docs/CONTRIBUTING.md`.

## 📄 License

Code: MIT License
Data: CC0 (where applicable)
Models: Respective open-source licenses

## 👤 Author

**Iván Weiss Van der Pol** (ivan@example.com)
Universidad Nacional de Asunción, Facultad Politécnica
Director: Prof. Juan Carlos Cristaldo (FADA)

## 🙏 Acknowledgments

- **Cristaldo Lab (FADA-UNA)** for cartography mentorship + 1M polygon dataset
- **UN-Habitat Paraguay** for Open Day partnership
- **paraguay-geodata** project for the 549 MB local data foundation
- **Ai-Whisperers** org for institutional support
- **OSS community**: PyTorch, HuggingFace, ESA, NASA, IBM-NASA Prithvi, Google AlphaEarth
