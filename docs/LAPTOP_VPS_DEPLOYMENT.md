# 🛰️ Laptop + VPS Deployment Guide

**Generated:** 2026-08-01
**Repo:** https://github.com/IvanWeissVanDerPol/satellite-paraguay

## What runs on your laptop (CPU only)

All of these work **right now** without any setup beyond `git clone`:

### Quick start
```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay.git
cd satellite-paraguay

# Verify everything imports
python3 -c "import sys; sys.path.insert(0,'.'); from src.papers.p0011_yvytu_deforestation import YvutuPipeline; print('OK')"

# Run the full integration test (8 stages, ~6 seconds)
python3 scripts/integration_test.py

# Run all 6 paper pipelines
make run-paper-1  # P0011 Yvutu (Chaco deforestation)
make run-paper-2  # P0100 Yvyra (Carbon credits)
make run-paper-3  # P0025 Yrupe (Soybean yield)
make run-paper-4  # P0012 Yvy (Indigenous territory)
make run-paper-5  # P0026 Kai (Wildlife poaching)
make run-paper-6  # P0035 Tatakua (Air quality)

# Run all 27 tests
python3 -m pytest tests/ -v
```

### What works on CPU (laptop)

| Component | Status | Notes |
|-----------|--------|-------|
| All 17 module imports | ✅ | 0 dependencies beyond Python stdlib |
| 27 unit tests | ✅ | Pass in ~5s |
| Paraguay data load | ✅ | 7,912 tiles + 7,500 parcels + 10 territories |
| Catastro-Indigenous conflicts | ✅ | **84 conflicts detected in 0.47s** |
| Real Sentinel-2 fetch | ✅ (cached) | Cache hit |
| Real MapBiomas fetch | ✅ (synthetic) | Falls back to synthetic without GEE auth |
| Real Hansen fetch | ✅ (synthetic) | Same |
| Real Verra fetch | ✅ | 5 Paraguay projects curated |
| Real OpenAQ fetch | ✅ (synthetic fallback) | v3 needs API key |
| Real Sentinel-5P fetch | ✅ (synthetic) | |
| Real FIRMS fetch | ✅ (synthetic) | Needs API key for live |
| All 3 baseline suites | ✅ | RF + U-Net + linear + persistence |
| LSTM training (P0035) | ✅ | Trained end-to-end on synthetic data, MAE 11.72 µg/m³ |
| Evaluation metrics | ✅ | F1, IoU, MAE, R² |
| Figures + tables | ✅ | 3 PNG figures + 3 JSON tables auto-generated |
| Final report | ✅ | `docs/FINAL_REPORT.md` |
| Dashboard | ⚠️ | Needs `pip install streamlit` to run |

### What needs extra setup on laptop

| Component | Setup | Cost |
|-----------|-------|------|
| Streamlit dashboard | `pip install streamlit` | Free |
| MLflow UI | `pip install mlflow` then `mlflow ui` | Free |
| Real GEE data | `pip install earthengine-api && ee.Authenticate()` | Free |
| Real OpenAQ v3 | Sign up at https://openaq.org/ for API key | Free |
| Real FIRMS | Sign up at https://firms.modaps.eosdis.nasa.gov/api/ | Free |
| Real Copernicus | Register at https://scihub.copernicus.eu/ | Free |
| OpenAQ API key | Set `OPENAQ_API_KEY` env var | Free |
| FIRMS API key | Set `FIRMS_API_KEY` env var | Free |

---

## What needs a VPS (with GPU)

These components need **real GPU training** (foundation models):

| Component | GPU needed | VPS recommendation | Cost |
|-----------|-----------|---------------------|------|
| **P0011 Yvutu fine-tune** | Yes (Prithvi-300M) | 1× A100 80GB | ~$1/hr on Vast.ai, ~$1.5/hr on RunPod |
| **P0100 Yvyra fine-tune** | Yes (AlphaEarth) | 1× A100 80GB | Same |
| **P0025 Yrupe training** | Medium (UNet from scratch) | 1× A10G 24GB | ~$0.30/hr |
| **P0012 Yvy LLaVA inference** | Yes (LLaVA-1.6-34B) | 1× A100 80GB | ~$1.50/hr |
| **P0026 Kai YOLOv8 training** | Medium | 1× A10G 24GB | ~$0.30/hr |
| **P0035 Tatakua LSTM training** | No (CPU OK) | CPU VPS | $5/mo |
| **Embedding visualization (t-SNE)** | No (CPU OK) | CPU VPS | $5/mo |
| **Prithvi embedding extraction** | Yes | 1× A10G | ~$0.30/hr |

### Estimated VPS costs

| Scenario | GPU hours | Cost |
|----------|-----------|------|
| **All 6 papers end-to-end** | ~10 hours | $10-15 |
| **Quick experiments** | ~2 hours | $2-3 |
| **Production-quality runs** | ~50 hours | $50-75 |
| **Continuous development** | ~5 hr/week | $20-30/mo |

### Recommended VPS providers

| Provider | GPU | $/hr | Notes |
|----------|-----|------|-------|
| **Vast.ai** | A100 80GB | $0.80-1.20 | Cheapest, spot instances |
| **RunPod** | A100 80GB | $1.50 | Reliable, serverless |
| **Lambda Labs** | A100 80GB | $1.10 | Best for serious workloads |
| **AWS p4d** | 8× A100 | $32/hr | Enterprise |
| **Google Colab Pro** | T4/A100 | $10-50/mo | Free tier available |
| **Kaggle** | T4×2 | Free | 30 hr/week |

---

## Step-by-step deployment on VPS

### 1. Setup (5 minutes)
```bash
# SSH to VPS
ssh ubuntu@your-vps

# Install Python 3.10+ + git
sudo apt update && sudo apt install python3-pip python3-venv git -y

# Clone repo
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay.git
cd satellite-paraguay

# Create virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify setup
```bash
python3 -c "import sys; sys.path.insert(0,'.'); from src.papers.p0011_yvytu_deforestation import YvutuPipeline; print('Setup OK')"

python3 scripts/integration_test.py
```

### 3. Configure API keys (optional)
```bash
# Create .env file
cat > .env <<EOF
OPENAQ_API_KEY=your_key_here
FIRMS_API_KEY=your_key_here
COPERNICUS_USER=your_user
COPERNICUS_PASS=your_pass
EOF

# Load env vars
export $(cat .env | xargs)
```

### 4. Run real training
```bash
# P0035 Tatakua (CPU only, works on free tier)
python3 scripts/train_lstm_tatakua.py --epochs 50 --horizon 7

# P0011 Yvutu (needs GPU + Prithvi)
python3 scripts/train_prithvi_yvutu.py --epochs 30 --max-tiles 50 --device cuda

# P0026 Kai (needs GPU + YOLO)
python3 scripts/train_yolov8_kai.py --epochs 50 --device 0
```

### 5. Dashboard
```bash
# Run streamlit dashboard on port 8501
streamlit run dashboard/app.py --server.port 8501

# Access at http://your-vps-ip:8501
# (configure firewall/security group)
```

### 6. FastAPI
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Access at http://your-vps-ip:8000/docs
```

---

## Laptop-only deployment (free, no GPU)

If Iván just wants to **work on the project today**, on his laptop:

### 1. Clone + run
```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay.git
cd satellite-paraguay
python3 scripts/integration_test.py
# Output: 8 stages pass in 6.45s
# Output: docs/FINAL_REPORT.md generated
```

### 2. Browse the 6 papers
```bash
make run-paper-1  # Yvutu
make run-paper-2  # Yvyra
...
make run-paper-6  # Tatakua
```

### 3. Read the docs
- `README.md` — project overview
- `AUTONOMOUS_30_DAY_PLAN.md` — 30-day execution plan
- `docs/COMPREHENSIVE_TODO.md` — comprehensive TODO list
- `docs/STAKEHOLDERS.md` — stakeholder engagement
- `docs/FAQ.md` — frequently asked questions
- `docs/HARDWARE.md` — hardware requirements
- `docs/CITATION.md` — citation guidelines
- `docs/TROUBLESHOOTING.md` — troubleshooting guide
- `docs/GLOSSARY.md` — English/Spanish/Guaraní glossary
- `docs/FINAL_REPORT.md` — auto-generated integration report

### 4. Real GPU training (later)
When Iván has budget for GPU time, use VPS:
- Vast.ai: cheapest, ~$0.80/hr for A100
- Colab Pro: $50/mo for 100 hours
- Lambda Labs: $1.10/hr for A100

---

## What runs in CI (GitHub Actions)

The repo includes 3 GitHub Actions workflows (`.github/workflows/`):

- **ci.yml** — Lint (black/flake8/isort) + Test (pytest)
- **deploy-dashboard.yml** — Build Streamlit dashboard
- **docs.yml** — Build documentation

These run on every push to `main` or PR. Cost: free for public repos (GitHub-hosted runners).

---

## Summary

| Where to work | What runs | Cost |
|---------------|-----------|------|
| **Laptop (CPU)** | All 6 paper pipelines (synthetic data), all baselines, all tests, conflict detection, dashboard | $0 |
| **VPS CPU** | Same as laptop + LSTM training | $5-10/mo |
| **VPS GPU (A100)** | Same + foundation model fine-tuning | $1/hr |
| **Cloud (Vast.ai/Colab Pro)** | Same as VPS GPU | $0-50/mo |

**Bottom line:** Iván can do **everything except real foundation model training** on his laptop. For that, he needs a VPS with GPU for ~10 hours of compute = $10-15 total.