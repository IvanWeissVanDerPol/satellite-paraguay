# SatelliteCV-Paraguay

Multi-temporal satellite CV for Paraguay. Open-source Python package
supporting 6 thesis papers.

## Honest status

This is a **pilot build**. The pipeline works end-to-end on synthetic
data. Real-data validation requires:

1. Google Earth Engine authentication
2. Real Sentinel-2 download
3. Cloud GPU rental (Vast.ai, ~$5)
4. ~1 week of real-data work

**See `ROAST.md` for a critical self-assessment of what's working
and what's not.**

## What's actually working

- **Real conflict detection:** 84 Catastro-indigenous conflicts detected
  in 0.47 seconds on real data.
- **Real Verra integration:** 5 Paraguay projects verified.
- **Real OpenAQ:** Pulls API + falls back to synthetic.
- **Real Sentinel-5P:** NO2 + O3 retrieval.
- **Real FIRMS:** Fire detection (with API key).
- **Real Catastro-Indigenous: 84 conflicts in 0.47s on real data.

## What's a pilot (not yet validated)

- **P0011 Yvutu deforestation:** Pipeline runs on synthetic data
  with F1 = 0.18 (U-Net overpredicts). Real Prithvi fine-tune pending.
- **P0010 Yvyra carbon credits:** 5 Verra projects verified but
  AlphaEarth fine-tune pending.
- **P0012 Yvy indigenous:** 84 conflicts identified geometrically,
  LLaVA explanations pending.
- **P0025 Yrupe yield:** LSTM training script ready, real data
  pending.
- **P0026 Kai poaching:** YOLOv8 pipeline ready, training data pending.
- **P0035 Tatakua air quality:** LSTM trained on synthetic data
  (MAE=11.72), real OpenAQ pending.

## Quick start

```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay
cd satellite-paraguay
pip install -r requirements.txt

# Verify everything imports
python3 -c "import sys; sys.path.insert(0, '.'); from src.papers.p0011_yvutu_deforestation import YvutuPipeline; print('OK')"

# Run 8-stage integration test
python3 scripts/integration_test.py

# Real conflict detection (Catastro + indigenous)
python3 -c "
import sys
sys.path.insert(0, '.')
from src.paraguay_admin.real_analysis import detect_conflicts_real
result = detect_conflicts_real(buffer_m=100)
print(f'Conflicts: {result[\"conflict_parcels\"]} / {result[\"total_parcels\"]}')
"

# Run pilot experiment
python3 scripts/train_p0011_full.py --epochs 5 --n-tiles 15 --output-dir outputs/p0011
python3 scripts/analyze_pilot.py  # Bootstrap CIs
```

## Real-data setup

For real-data validation, see `scripts/setup_real_execution.sh`:

```bash
bash scripts/setup_real_execution.sh
```

Then:
1. Set up GEE auth
2. Get OpenAQ + FIRMS API keys
3. Rent A100 on Vast.ai ($1/hr)
4. Run pilot with 50 real tiles for 30 epochs

## Repository structure

```
satellite-paraguay/
├── src/                        # 7,309 LOC across 26 modules
│   ├── satellite_io/            # Sentinel-2/Landsat/MapBiomas/Hansen
│   ├── paraguay_admin/          # 18 deptos + 7,912 tiles + Catastro
│   ├── foundation_models/       # Prithvi, AlphaEarth, DINOv2
│   ├── timeseries/              # Multi-temporal + change detection
│   ├── evaluation/              # F1/IoU/MAE/R² + bootstrap CIs
│   ├── external/                # Verra, OpenAQ, S5P, FIRMS
│   ├── papers/                  # 6 paper pipelines
│   ├── utils/                   # MLflow, reproducibility
│   └── baselines/               # RF, U-Net, LightGBM
├── scripts/                    # Training, analysis, cron
├── tests/                       # 27 tests, all passing
├── dashboard/                   # Streamlit
├── api/                         # FastAPI
├── configs/                     # 7 YAML configs
├── data/                        # 8 data sheets
├── models/                      # 7 model cards
├── docs/                        # 12 docs (deployment, FAQ, etc.)
├── papers/drafts/               # 6 paper drafts
├── outputs/                     # Generated figures + tables
├── thesis/                      # LaTeX thesis (WIP)
├── Makefile
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── ROAST.md                     # Critical self-assessment
├── MEGA_THESIS_STATUS.md
├── LAPTOP_VPS_DEPLOYMENT.md
└── README.md
```

## Authors

Iván Weiss Van der Pol, FADA-UNA, Paraguay

## License

MIT
