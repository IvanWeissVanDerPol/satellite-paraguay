# 🛰️ SATELLITE-PARAGUAY — Comprehensive TODO

**Generated:** 2026-07-31
**Status:** 36 modules / 2,869 lines / 8% of production target
**Target:** ~300 files / ~30,000 lines / 6 papers publishable
**34 gaps identified across 4 priority tiers**

---

## 📊 Current State vs Target

| Asset | Current | Target | Gap |
|-------|---------|--------|-----|
| Python modules | 36 | 80 | +44 |
| Lines of code | 2,869 | 25,000 | +22,131 |
| Test files | 3 | 30 | +27 |
| Test coverage | ~15% | 80% | +65% |
| Notebooks | 1 | 12 | +11 |
| YAML configs | 6 | 30 | +24 |
| Documentation pages | 3 | 40 | +37 |
| Papers drafted | 0 | 6 | +6 |
| Models trained | 0 | 6 | +6 |
| Benchmarks run | 0 | 12+ | +12 |

**Total work to do: ~250 tasks across 34 gap categories**

---

## 🔥 TIER 1: CRITICAL (blocks publication) — 7 gaps

These MUST be done before any paper can be submitted.

### T1.1 Real Sentinel-2 download pipeline (currently stub)
- [ ] Set up Google Earth Engine authentication (`earthengine authenticate`)
- [ ] Implement real `download_via_gee()` with retry logic
- [ ] Add rate limiting + quota management
- [ ] Add checksum validation for downloaded files
- [ ] Add resumable downloads (large tiles)
- [ ] Add cloud masking with `s2cloudless` (production-ready)
- [ ] Add atmospheric correction (Sen2Cor or `atmcor`)
- [ ] Implement COG (Cloud-Optimized GeoTIFF) output
- [ ] Test against known Paraguay tiles
- [ ] Document GEE setup in `docs/GEE_SETUP.md`

### T1.2 Real model training (currently all stubs)
- [ ] P0011 Yvutu: Train Prithvi fine-tune on MapBiomas labels (real data)
- [ ] P0100 Yvyra: Train AlphaEarth-based biomass estimator
- [ ] P0025 Yrupe: Train GRU/LSTM on INBIO yield data
- [ ] P0012 Yvy: Fine-tune LLaVA-1.6 on Paraguay tiles
- [ ] P0026 Kai: Train YOLOv8 on COCO + wildlife data
- [ ] P0035 Tatakua: Train LSTM on OpenAQ time series
- [ ] Save model checkpoints with metadata
- [ ] Implement training loop with early stopping
- [ ] Add learning rate finder
- [ ] Add gradient accumulation for large models
- [ ] Add mixed-precision training (fp16)
- [ ] Add model EMA (exponential moving average)

### T1.3 Real evaluation against actual MapBiomas/Hansen ground truth
- [ ] Download actual MapBiomas Paraguay TIFF (~500 MB)
- [ ] Download actual Hansen GFC Paraguay (~200 MB)
- [ ] Implement per-pixel evaluation
- [ ] Implement per-department evaluation
- [ ] Implement temporal evaluation (year-by-year)
- [ ] Implement per-class confusion matrix
- [ ] Bootstrap confidence intervals for metrics
- [ ] McNemar's test for model comparison
- [ ] Statistical significance tests

### T1.4 Real Verra VCS API integration
- [ ] Register for Verra API access (free research)
- [ ] Implement `VerraClient` class
- [ ] Parse project metadata (id, name, location, area, methodology)
- [ ] Match Paraguay projects to tiles
- [ ] Download carbon credit project geometries
- [ ] Implement rate limiting + caching
- [ ] Error handling for missing data
- [ ] Unit tests with mocked responses
- [ ] Documentation

### T1.5 Real YOLOv8 training on COCO + wildlife data
- [ ] Download COCO-zoo (or use cached version)
- [ ] Acquire wildlife datasets:
  - [ ] iNaturalist (open)
  - [ ] WWF wildlife monitoring data
  - [ ] Snapshot Serengeti (camera traps)
- [ ] Train YOLOv8 medium on wildlife + poaching camp classes
- [ ] Validate on held-out test set
- [ ] Implement mAP@0.5 + mAP@0.5:0.95
- [ ] Implement confidence calibration
- [ ] Save best checkpoint
- [ ] Export to ONNX for deployment

### T1.6 Real OpenAQ + Sentinel-5P pipeline
- [ ] Implement `OpenAQClient` with rate limiting
- [ ] Fetch all Asunción stations (last 5 years)
- [ ] Implement `Sentinel5PClient` via GEE
- [ ] Fetch NO2, SO2, CO, O3, CH4, AER_AI for Asunción
- [ ] Align OpenAQ + Sentinel-5P on same time grid
- [ ] Handle missing data gracefully
- [ ] Build features: meteorological + spatial + temporal
- [ ] Train LSTM with cross-validation
- [ ] Report MAE, RMSE, R² with confidence intervals

### T1.7 Real Catastro + indigenous territory analysis
- [ ] Download full Catastro (not just sample 7,500)
- [ ] Download full indigenous territories from INDI
- [ ] Implement conflict detection algorithm
- [ ] Implement overlay visualization (interactive map)
- [ ] CARE Principles review + sign-off
- [ ] INDI consultation protocol
- [ ] Community engagement plan
- [ ] Data sovereignty framework

---

## 🟡 TIER 2: HIGH PRIORITY (production-ready) — 10 gaps

Required for the repo to be considered production-grade.

### T2.1 CI/CD pipeline
- [ ] GitHub Actions: run pytest on push
- [ ] GitHub Actions: run black + flake8 + mypy
- [ ] GitHub Actions: build docs
- [ ] GitHub Actions: deploy dashboard to staging
- [ ] GitHub Actions: auto-bump version
- [ ] Pre-commit hooks: black
- [ ] Pre-commit hooks: flake8
- [ ] Pre-commit hooks: mypy
- [ ] Pre-commit hooks: trailing whitespace
- [ ] Pre-commit hooks: end-of-file
- [ ] Branch protection rules

### T2.2 Docker containerization
- [ ] `Dockerfile` for development environment
- [ ] `Dockerfile` for production dashboard
- [ ] `docker-compose.yml` for full stack
- [ ] Multi-stage builds to minimize image size
- [ ] GPU support (CUDA base image)
- [ ] Volume mounts for data
- [ ] Health checks
- [ ] Logging configuration

### T2.3 DVC data versioning
- [ ] Initialize DVC (`dvc init`)
- [ ] Configure remote storage (S3 / GCS / local)
- [ ] Track all `data/raw/` files
- [ ] Track all `data/processed/` files
- [ ] Track all model checkpoints
- [ ] Document DVC workflow
- [ ] Add DVC to CI/CD

### T2.4 Real notebooks per paper (need 6 total, currently 1)
- [ ] `notebooks/p0011_yvytu.ipynb` (currently exists, needs real content)
- [ ] `notebooks/p0100_yvyra.ipynb`
- [ ] `notebooks/p0025_yrupe.ipynb`
- [ ] `notebooks/p0012_yvy.ipynb`
- [ ] `notebooks/p0026_kai.ipynb`
- [ ] `notebooks/p0035_tatakua.ipynb`
- [ ] Each notebook should have:
  - [ ] Motivation (markdown)
  - [ ] Data exploration
  - [ ] Visualization
  - [ ] Model training
  - [ ] Evaluation
  - [ ] Discussion
  - [ ] References

### T2.5 EDA notebooks (exploratory data analysis)
- [ ] `notebooks/eda_paraguay_geodata.ipynb` — overview of all 14 datasets
- [ ] `notebooks/eda_sentinel2_tiles.ipynb` — sample tiles visualization
- [ ] `notebooks/eda_chaco_deforestation.ipynb` — historical trends
- [ ] `notebooks/eda_indigenous_territories.ipynb` — overlap analysis
- [ ] `notebooks/eda_openaq_asuncion.ipynb` — air quality trends
- [ ] `notebooks/eda_firms_fires.ipynb` — fire patterns

### T2.6 Real baselines (currently no baselines implemented)
- [ ] P0011 baseline: Random Forest per-pixel
- [ ] P0011 baseline: U-Net from scratch
- [ ] P0100 baseline: Linear regression
- [ ] P0100 baseline: Random Forest
- [ ] P0025 baseline: Persistence forecast
- [ ] P0025 baseline: Linear regression
- [ ] P0012 baseline: Catastro only (no AI)
- [ ] P0026 baseline: YOLOv8n pretrained (no fine-tune)
- [ ] P0035 baseline: Mean forecast
- [ ] P0035 baseline: Linear regression
- [ ] Per-paper `benchmarks/` directory

### T2.7 Reproducibility
- [ ] Set random seeds everywhere (`src/utils/seeding.py`)
- [ ] Lock Python version (3.10.x)
- [ ] Lock all dependency versions (`requirements.lock`)
- [ ] Capture environment info per experiment
- [ ] Save git commit hash per experiment
- [ ] Container hash (Docker image tag) per experiment
- [ ] Hardware info (CPU/GPU) per experiment
- [ ] Wall-clock time per experiment
- [ ] Reproducibility report (`docs/REPRODUCIBILITY.md`)

### T2.8 Model training scripts
- [ ] `scripts/train_p0011.py` (not stub)
- [ ] `scripts/train_p0100.py`
- [ ] `scripts/train_p0025.py`
- [ ] `scripts/train_p0012.py`
- [ ] `scripts/train_p0026.py`
- [ ] `scripts/train_p0035.py`
- [ ] Each supports: `--config`, `--checkpoint`, `--eval-only`
- [ ] Each supports: `--gpu`, `--batch-size`, `--epochs`
- [ ] Each logs to MLflow / W&B
- [ ] Each saves checkpoints + metadata

### T2.9 Experiment tracking (MLflow or W&B)
- [ ] Set up MLflow tracking server (or W&B account)
- [ ] Log hyperparameters per experiment
- [ ] Log metrics per epoch
- [ ] Log model artifacts
- [ ] Log figures + tables
- [ ] Log git commit + branch
- [ ] Log system info
- [ ] Comparison UI for multiple runs
- [ ] Reproducibility from any logged run

### T2.10 API endpoint (FastAPI)
- [ ] `api/main.py` — FastAPI app
- [ ] `/health` endpoint
- [ ] `/predict/deforestation` — P0011 inference
- [ ] `/predict/carbon` — P0100 inference
- [ ] `/predict/yield` — P0025 inference
- [ ] `/predict/indigenous` — P0012 inference
- [ ] `/predict/poaching` — P0026 inference
- [ ] `/predict/air-quality` — P0035 inference
- [ ] OpenAPI docs auto-generated
- [ ] Rate limiting
- [ ] Authentication (API key)
- [ ] Docker deployment
- [ ] Tests for each endpoint
- [ ] Load testing

---

## 🟢 TIER 3: MEDIUM (research-grade) — 11 gaps

Required for the repo to be considered research-grade (publication-ready).

### T3.1 Thesis document template
- [ ] `thesis/main.tex` — root LaTeX file
- [ ] `thesis/chapters/01_introduction.tex`
- [ ] `thesis/chapters/02_literature_review.tex`
- [ ] `thesis/chapters/03_methodology.tex`
- [ ] `thesis/chapters/04_p0011_yvytu.tex`
- [ ] `thesis/chapters/05_p0100_yvyra.tex`
- [ ] `thesis/chapters/06_p0025_yrupe.tex`
- [ ] `thesis/chapters/07_p0012_yvy.tex`
- [ ] `thesis/chapters/08_p0026_kai.tex`
- [ ] `thesis/chapters/09_p0035_tatakua.tex`
- [ ] `thesis/chapters/10_integration.tex`
- [ ] `thesis/chapters/11_conclusions.tex`
- [ ] `thesis/references.bib`
- [ ] `thesis/preamble.tex`
- [ ] Makefile target: `make thesis-pdf`

### T3.2 Bibliography management
- [ ] BibTeX file with 200+ references
- [ ] Cross-references to all 53 baseline papers
- [ ] Cross-references to all 107 open data sources
- [ ] Cross-references to all foundation models
- [ ] Auto-fetch DOIs / arXiv IDs
- [ ] Citation style: APA / IEEE / Nature
- [ ] Citation count per paper
- [ ] PDF storage for offline access

### T3.3 Per-paper draft folders
- [ ] `papers/drafts/p0011_yvytu/` — full draft folder
- [ ] `papers/drafts/p0100_yvyra/` — full draft folder
- [ ] `papers/drafts/p0025_yrupe/` — full draft folder
- [ ] `papers/drafts/p0012_yvy/` — full draft folder
- [ ] `papers/drafts/p0026_kai/` — full draft folder
- [ ] `papers/drafts/p0035_tatakua/` — full draft folder
- [ ] Each draft folder contains:
  - [ ] `abstract.md`
  - [ ] `introduction.md`
  - [ ] `related_work.md`
  - [ ] `methods.md`
  - [ ] `experiments.md`
  - [ ] `results.md`
  - [ ] `discussion.md`
  - [ ] `conclusion.md`
  - [ ] `references.bib`
  - [ ] `figures/` (placeholder)
  - [ ] `tables/` (placeholder)

### T3.4 Per-paper figures + tables
- [ ] P0011: 8-12 figures + 3-5 tables
- [ ] P0100: 8-12 figures + 3-5 tables
- [ ] P0025: 6-8 figures + 2-4 tables
- [ ] P0012: 6-10 figures + 2-4 tables
- [ ] P0026: 6-8 figures + 2-4 tables
- [ ] P0035: 6-8 figures + 2-4 tables
- [ ] Figure style guide (consistent fonts, colors, sizes)
- [ ] Auto-generation from notebooks
- [ ] Figure catalog (`docs/FIGURE_CATALOG.md`)

### T3.5 Per-paper README
- [ ] `papers/drafts/p0011_yvytu/README.md` — status, next actions, blockers
- [ ] `papers/drafts/p0100_yvyra/README.md`
- [ ] `papers/drafts/p0025_yrupe/README.md`
- [ ] `papers/drafts/p0012_yvy/README.md`
- [ ] `papers/drafts/p0026_kai/README.md`
- [ ] `papers/drafts/p0035_tatakua/README.md`
- [ ] Each README has: title, status, target journal, methods, data, results, blockers

### T3.6 Glossary (multilingual)
- [ ] `docs/GLOSSARY.md` — English/Spanish/Guaraní
- [ ] Terms for each paper (e.g. Yvytu = wind in Guaraní)
- [ ] Technical terms (NDVI, F1, etc.)
- [ ] Domain terms (Chaco, Catastro, etc.)

### T3.7 Data Sheets (per dataset)
- [ ] `data/datasheets/SENTINEL2.md`
- [ ] `data/datasheets/LANDSAT9.md`
- [ ] `data/datasheets/MAPBIOMAS.md`
- [ ] `data/datasheets/HANSEN_GFC.md`
- [ ] `data/datasheets/OPENAQ.md`
- [ ] `data/datasheets/VERRA_VCS.md`
- [ ] `data/datasheets/FIRMS.md`
- [ ] `data/datasheets/PARAGUAY_GEODATA.md`
- [ ] Each datasheet has: source, license, version, date, fields, limitations

### T3.8 Model Cards (per model)
- [ ] `models/cards/PRITHVI.md`
- [ ] `models/cards/ALPHAEARTH.md`
- [ ] `models/cards/DINOV2.md`
- [ ] `models/cards/YOLOV8.md`
- [ ] `models/cards/LLAVA.md`
- [ ] `models/cards/WHISPER.md`
- [ ] `models/cards/TIMESFM.md`
- [ ] Each card has: purpose, training data, limitations, bias considerations

### T3.9 Stakeholder map
- [ ] `docs/STAKEHOLDERS.md`
- [ ] Ivan (thesis author)
- [ ] Advisor (Cristaldo)
- [ ] Co-authors (multi-advisor for some papers)
- [ ] Institutions (UNA, INFONA, INDI, SENEPA, etc.)
- [ ] Funding agencies (CONACYT, PROCIENCIA, etc.)
- [ ] Journal editors (RSE, Nature CC, etc.)
- [ ] Community partners (5 indigenous communities)
- [ ] Communication plan per stakeholder

### T3.10 Communication plan
- [ ] Weekly advisor meeting (Mondays 14:00)
- [ ] Monthly stakeholder update
- [ ] Quarterly journal submission prep
- [ ] Conference deadlines (NeurIPS, IGARSS, etc.)
- [ ] Workshop participation (AI for Social Good, FAccT)
- [ ] Public engagement (UN-Habitat Open Day)

### T3.11 Performance profiling
- [ ] Profile each pipeline (cProfile)
- [ ] Memory profiling (memory_profiler)
- [ ] GPU utilization monitoring
- [ ] Bottleneck identification
- [ ] Optimization recommendations
- [ ] Performance regression tests

---

## ⚪ TIER 4: LOW PRIORITY (polish) — 6 gaps

Nice-to-have but not blocking.

### T4.1 FAQ section
- [ ] `docs/FAQ.md` — common questions
- [ ] How do I add a new paper?
- [ ] How do I retrain a model?
- [ ] How do I add a new dataset?
- [ ] How do I deploy the dashboard?
- [ ] How do I cite this work?

### T4.2 Video walkthroughs
- [ ] 5-minute overview
- [ ] 15-minute setup tutorial
- [ ] 30-minute paper walkthrough (one per paper)

### T4.3 Cost estimator
- [ ] `docs/COST.md` — compute, storage, API costs
- [ ] Per-paper cost breakdown
- [ ] Scaling considerations
- [ ] Cost optimization tips

### T4.4 Hardware requirements matrix
- [ ] `docs/HARDWARE.md`
- [ ] Minimum: CPU-only, 16 GB RAM, 100 GB disk
- [ ] Recommended: 1× GPU, 32 GB RAM, 500 GB disk
- [ ] Optimal: 4× GPU, 128 GB RAM, 2 TB disk
- [ ] Cloud alternatives (Colab, Kaggle, Vast.ai, Lambda)

### T4.5 Citation guidelines
- [ ] `docs/CITATION.md`
- [ ] How to cite the megaproyect
- [ ] How to cite individual papers
- [ ] How to cite foundation models
- [ ] How to cite datasets
- [ ] BibTeX snippets

### T4.6 Troubleshooting guide
- [ ] `docs/TROUBLESHOOTING.md`
- [ ] Common errors + solutions
- [ ] GEE authentication issues
- [ ] GPU out-of-memory
- [ ] Package version conflicts
- [ ] Data download failures

---

## 🔬 AREAS OF INTEREST — Beyond the basics

### A. Cross-cutting scientific questions
- [ ] Can satellite CV detect ENSO climate cycles in Paraguay?
- [ ] Can Chaco deforestation be predicted from ENSO 6 months in advance?
- [ ] What's the relationship between deforestation and carbon credit issuance?
- [ ] Are indigenous territories correlated with biodiversity hotspots?
- [ ] How does air quality in Asunción correlate with regional fires?
- [ ] Can wildlife poaching be predicted from road density?
- [ ] Does soybean yield correlate with deforestation rate?

### B. Methodological extensions
- [ ] Multi-modal fusion (Sentinel-2 + Sentinel-1 SAR + DEM)
- [ ] Self-supervised pretraining on Paraguay tiles
- [ ] Active learning for labeling (minimize human labeling cost)
- [ ] Domain adaptation (Paraguay → Bolivia → Argentina)
- [ ] Few-shot learning for new deforestation classes
- [ ] Causal inference (not just correlation)
- [ ] Counterfactual reasoning
- [ ] Uncertainty quantification
- [ ] Explainability (LIME, SHAP, attention maps)

### C. Deployment & operations
- [ ] Real-time dashboard with live satellite feeds
- [ ] Mobile app (React Native + TensorFlow Lite)
- [ ] WhatsApp bot for deforestation alerts
- [ ] Telegram bot for carbon credit updates
- [ ] Integration with Paraguay's national systems (SINAM, SIRT, etc.)
- [ ] Edge deployment (NVIDIA Jetson)
- [ ] Federated learning across multiple regions

### D. Community engagement
- [ ] INDI community partnerships
- [ ] WWF Paraguay partnership
- [ ] Guyra Paraguay (bird conservation)
- [ ] Fundación Moisés Bertoni (conservation)
- [ ] Universidad Católica (Silicon Misiones)
- [ ] Code for Paraguay (civic tech)
- [ ] PyData Asunción meetup
- [ ] AI for Social Good Paraguay

### E. Policy & impact
- [ ] Brief for INFONA on automated deforestation alerts
- [ ] Brief for INDI on indigenous data sovereignty
- [ ] Brief for SENEPA on Chagas vector monitoring
- [ ] Brief for MEC on indigenous education
- [ ] Brief for Congress on carbon market transparency
- [ ] Open data policy recommendations

### F. Education & training
- [ ] Tutorial series for UNA students
- [ ] Workshop on satellite CV for Paraguay
- [ ] Course material: "Earth Observation for Social Good"
- [ ] Mentorship program for next cohort

### G. Replication & expansion
- [ ] Replicate for Bolivia (similar deforestation dynamics)
- [ ] Replicate for Argentina (Gran Chaco extension)
- [ ] Replicate for Uruguay (smaller, easier)
- [ ] Latin America regional megaproyect
- [ ] Comparative analysis: Paraguay vs Brazil Cerrado

### H. Novel research directions
- [ ] Cross-tile attention for long-range context
- [ ] Foundation model fine-tuned on Paraguay specifically
- [ ] Multi-task learning across all 6 papers
- [ ] Reinforcement learning for adaptive monitoring
- [ ] Graph neural networks for parcel adjacency
- [ ] Diffusion models for future deforestation scenarios

### I. Funding & sustainability
- [ ] PROCIENCIA grant application
- [ ] FEEI equipment grant
- [ ] Private foundation grants (Itaú, Azul)
- [ ] International grants (NSF, EU Horizon, IDB)
- [ ] Crowdfunding for community engagement
- [ ] Open Science Foundation grant

### J. Data sovereignty & ethics
- [ ] CARE Principles review (full audit)
- [ ] FAIR Principles review
- [ ] Indigenous data sovereignty policy
- [ ] Ethical AI audit (UNESCO, OECD)
- [ ] Bias audit (geographic, demographic)
- [ ] Privacy impact assessment
- [ ] Data sharing agreement templates

---

## 📅 30-day autonomous execution plan (already exists)

The current `AUTONOMOUS_30_DAY_PLAN.md` covers basic execution. This new TODO list is **much more detailed** and covers the full 250+ tasks needed to take the project from current state (8% complete) to production-ready (100%).

### Execution strategy

1. **Days 1-7: TIER 1 critical paths**
   - Set up GEE authentication
   - Download real Sentinel-2 + MapBiomas + Hansen
   - Implement real model training scripts (not stubs)

2. **Days 8-14: TIER 1 + start TIER 2**
   - Real evaluations against ground truth
   - Verra VCS + OpenAQ + Sentinel-5P API clients
   - CI/CD + Docker + DVC setup

3. **Days 15-21: TIER 2 + start TIER 3**
   - Real notebooks per paper
   - EDA notebooks
   - Baselines implementation
   - Thesis template (LaTeX)

4. **Days 22-30: TIER 3 + TIER 4**
   - Per-paper draft folders
   - Bibliography
   - Glossary, datasheets, model cards
   - Stakeholder map + communication plan

5. **Days 31-90: Beyond (areas of interest)**
   - Cross-cutting scientific questions
   - Methodological extensions
   - Deployment & operations
   - Community engagement
   - Policy briefs

---

## 📊 Success metrics

| Tier | Tasks | Effort (person-days) | When done |
|------|-------|----------------------|-----------|
| Tier 1 (Critical) | 50+ | 30 | Before paper submission |
| Tier 2 (High) | 100+ | 60 | Before defense |
| Tier 3 (Medium) | 80+ | 90 | Before graduation |
| Tier 4 (Low) | 30+ | 20 | After graduation (polish) |
| Areas of Interest | 50+ | ongoing | Career-spanning |

**Total: ~250 tasks, ~200 person-days of focused work**

---

## 📁 Files to update with this TODO

- [x] `docs/GAP_ANALYSIS.md` — this file (auto-generated above)
- [ ] `docs/TODO.md` — copy of this file (link from README)
- [ ] `docs/ROADMAP.md` — quarterly breakdown
- [ ] GitHub Issues — one per gap (250 issues)
- [ ] GitHub Projects board — kanban with these tasks

---

## 🎯 Recommended first 10 tasks

If Ivan wants to start TODAY:

1. **T1.1** Set up Google Earth Engine authentication
2. **T1.3** Download actual MapBiomas + Hansen data
3. **T2.6** Implement P0011 baseline (Random Forest)
4. **T2.4** Create 5 more notebooks (1 per paper)
5. **T2.7** Set random seeds + environment capture
6. **T2.1** GitHub Actions for CI
7. **T3.1** Thesis LaTeX template
8. **T3.2** BibTeX with 200+ references
9. **T3.5** Per-paper READMEs
10. **T3.7** Data Sheets for all 14 datasets

Each task has well-defined inputs/outputs and can be done independently.

---

**Status:** Awaiting Ivan's input on which priority tier to start with.
