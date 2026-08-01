# 30-DAY AUTONOMOUS EXECUTION PLAN

**Created:** 2026-07-31
**Target:** Build end-to-end pipeline for SatelliteCV-Paraguay mega-project
**Scope:** Everything ready to run — code, data, models, validation, dashboard

---

## 🎯 The Goal

By end of day 30, the repo will be:
- ✅ Fully installed (all dependencies)
- ✅ All data downloaded + indexed
- ✅ Foundation model embeddings pre-computed for all 7,912 Paraguay tiles
- ✅ 6 papers have working baselines (even if not fully tuned)
- ✅ Dashboard live with all 6 paper outputs
- ✅ All tests passing
- ✅ All configs ready for Iván to fine-tune

---

## 📅 Day-by-Day Plan

### Day 0 (Setup, day of starting)

**Total: ~2 hours of work**

- [ ] Verify Python 3.10+, pip, git
- [ ] Verify access to /root/paraguay-geodata/
- [ ] Verify Colab / Kaggle access
- [ ] Run `make bootstrap`

### Day 1-3: Foundation

**Day 1:**
- [ ] Bootstrap repo (`make install`)
- [ ] Set up DVC for data versioning
- [ ] Configure pre-commit + black + flake8
- [ ] Set up GitHub Actions CI

**Day 2:**
- [ ] Copy paraguay-geodata to `data/external/`
- [ ] Verify all 14 key datasets load
- [ ] Build data catalog (`make data-catalog`)

**Day 3:**
- [ ] Build Paraguay admin loader (18 deptos, 268 distritos)
- [ ] Build tile index loader (7,912 tiles)
- [ ] Build Catastro intersection helper
- [ ] Unit tests for admin/tile loaders

### Day 4-7: Satellite I/O

**Day 4:**
- [ ] Sentinel-2 download script (`make data-sentinel`)
- [ ] Cloud masking (s2cloudless)
- [ ] NDVI/EVI/SCL composites
- [ ] Store as Zarr/COG

**Day 5:**
- [ ] Landsat 9 download script
- [ ] Planet academic API integration (if available)
- [ ] Cross-sensor harmonization

**Day 6:**
- [ ] MapBiomas Paraguay download
- [ ] Hansen GFC download
- [ ] ESA WorldCover download
- [ ] Merge into single land-cover map

**Day 7:**
- [ ] Time-series stacking (10 years of composites)
- [ ] NDVI trend computation
- [ ] Change detection (BFAST-like)
- [ ] Tests + validation

### Day 8-12: Foundation Models

**Day 8:**
- [ ] Prithvi download + setup
- [ ] Prithvi embedding inference pipeline
- [ ] Cache embeddings per tile

**Day 9:**
- [ ] AlphaEarth setup (Google research API)
- [ ] AlphaEarth embeddings per tile
- [ ] Cache embeddings

**Day 10:**
- [ ] DINOv2 setup (vision foundation model, free)
- [ ] DINOv2 embeddings per tile (visual features)
- [ ] Cache embeddings

**Day 11:**
- [ ] Embedding fusion (Prithvi + AlphaEarth + DINOv2)
- [ ] Vector DB (FAISS) for similarity search
- [ ] Tests

**Day 12:**
- [ ] Embedding visualization (t-SNE/UMAP)
- [ ] First visualization notebook
- [ ] Validation against MapBiomas classes

### Day 13-16: Paper 1 (P0011 Yvytu) — Chaco Deforestation

**Day 13:**
- [ ] Train segmentation model on MapBiomas labels
- [ ] Apply to Chaco tiles
- [ ] Generate deforestation map

**Day 14:**
- [ ] Change detection (BFAST-like)
- [ ] Time-series analysis
- [ ] Deforestation alerts per tile

**Day 15:**
- [ ] Validation against Hansen GFC
- [ ] F1/IoU metrics
- [ ] Confusion matrix

**Day 16:**
- [ ] Figures (paper-ready)
- [ ] Draft methods section
- [ ] Run full baseline

### Day 17-19: Paper 2 (P0100 Yvyra) — Carbon Credits

**Day 17:**
- [ ] Verra VCS registry parser
- [ ] Match carbon projects to Paraguay tiles

**Day 18:**
- [ ] Carbon-credit verification model
- [ ] Comparison vs Verra ground truth
- [ ] F1/AUC

**Day 19:**
- [ ] Paper figures (carbon map + comparison)
- [ ] Integration with Bolsa de Valores data
- [ ] Draft methods

### Day 20-21: Paper 3 (P0025 Yrupe) — Soybean Yield

**Day 20:**
- [ ] INBIO data parser
- [ ] Sentinel-2 time series for Caaguazú
- [ ] Delineate Anything v2 inference (field boundaries)

**Day 21:**
- [ ] GRU/LSTM training on yield × NDVI
- [ ] Validation against INBIO records
- [ ] Paper figures

### Day 22-23: Paper 4 (P0012 Yvy) — Indigenous Territory

**Day 22:**
- [ ] LLaVA-1.6 setup (open-source VLM)
- [ ] Apply to Paraguay tiles for native-language place names

**Day 23:**
- [ ] Catastro intersection + indigenous_territories
- [ ] Conflict map generation
- [ ] Paper figures

### Day 24-25: Paper 5 (P0026 Kai) — Wildlife Poaching

**Day 24:**
- [ ] YOLOv8 training on COCO-zoo (transfer learning)
- [ ] Apply to Defensores del Chaco satellite

**Day 25:**
- [ ] NASA FIRMS integration (fire alerts)
- [ ] GBIF species overlay
- [ ] Paper figures

### Day 26-27: Paper 6 (P0035 Tatakua) — Air Quality

**Day 26:**
- [ ] OpenAQ data ingestion for Asunción
- [ ] Sentinel-5P atmospheric retrieval

**Day 27:**
- [ ] LSTM forecasting
- [ ] PM2.5 prediction
- [ ] Paper figures

### Day 28-29: Integration + Dashboard

**Day 28:**
- [ ] Streamlit unified dashboard
- [ ] All 6 papers accessible from single interface
- [ ] Live map with all layers

**Day 29:**
- [ ] Final integration testing
- [ ] Documentation polish
- [ ] Benchmark against all baselines

### Day 30: Validation + Release

**Day 30:**
- [ ] Run all tests + benchmarks
- [ ] Generate final report (`make report`)
- [ ] Push to GitHub
- [ ] Notify Iván
- [ ] Ready for Iván to fine-tune

---

## 📋 What Iván needs to do (NOT autonomous)

After day 30:
1. Fine-tune hyperparameters per paper
2. Send outreach emails (templates ready)
3. Defend each paper's novelty vs literature
4. Write final thesis document
5. Submit papers to journals

---

## ✅ Pre-flight checklist (Day 0)

Before starting autonomous execution:

- [ ] Python 3.10+ installed (`python3 --version`)
- [ ] pip installed (`pip --version`)
- [ ] git installed (`git --version`)
- [ ] Access to `/root/paraguay-geodata/` (549 MB)
- [ ] 100 GB free disk space (Sentinel-2 tiles)
- [ ] Internet access (for downloads)
- [ ] Optional: Colab Pro / Kaggle (for foundation models)

---

## 🚀 Run Autonomous Execution

```bash
cd /root/satellite-paraguay
./run-autonomous.sh
```

This will:
1. Run all 30 days of work
2. Log progress to `logs/autonomous/`
3. Skip steps that need human input
4. Report final state at end

---

## 📊 Expected outcomes

By day 30, the repo will have:

- ✅ 50+ Python source files (organized per paper)
- ✅ 6 working baseline models (one per paper)
- ✅ 100+ GB pre-computed embeddings
- ✅ Live Streamlit dashboard
- ✅ 6 paper-ready figure sets
- ✅ 1 draft methods section per paper
- ✅ All tests passing
- ✅ Complete data catalog
- ✅ Ready for Iván to fine-tune

---

## 📁 Files in this plan

- `AUTONOMOUS_30_DAY_PLAN.md` (this file) — high-level plan
- `scripts/day_*.sh` — daily execution scripts
- `docs/DATA_CATALOG.md` — what data + how to get
- `docs/MODELS.md` — what models + how to load
- `docs/PAPERS.md` — per-paper specs
- `docs/CHECKLIST.md` — completion criteria per day
