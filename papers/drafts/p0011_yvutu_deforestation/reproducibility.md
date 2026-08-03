# P0011 Yvutu — Reproducibility Checklist

RSE authors are required to complete a reproducibility checklist. Below is
our completion status.

---

## 1. Computing infrastructure (Required)

| Item | Details |
|------|---------|
| **OS** | Ubuntu 24.04 LTS (Linux 6.8.0-90-generic) |
| **Python version** | 3.12.3 |
| **PyTorch version** | 2.x (CUDA 12.x optional, CPU tested) |
| **Memory** | 16 GB RAM minimum, 32 GB recommended |
| **GPU** | Optional: 1× NVIDIA A100 80GB |
| **Compute time** | ~8 hours on A100, ~12 hours on CPU |
| **Storage** | 50 GB (raw + processed + checkpoints) |

## 2. Code availability (Required)

| Item | URL |
|------|-----|
| **Repository** | https://github.com/IvanWeissVanDerPol/satellite-paraguay |
| **License** | MIT |
| **Commit** | 1708643 |
| **Documentation** | `docs/` folder + `README.md` |

## 3. Data availability (Required)

| Dataset | URL |
|---------|-----|
| Sentinel-2 L2A | https://browser.dataspace.copernicus.eu/ |
| MapBiomas Paraguay | https://plataforma.mapbiomas.org/ |
| Hansen GFC v1.11 | https://www.globalforestwatch.org/ |
| Synthetic Chaco | `data/synthetic_chaco/` (in repo) |

## 4. Pretrained model weights (Required for ML papers)

| Model | URL |
|-------|-----|
| Yvutu Prithvi fine-tuned | HuggingFace (forthcoming) |
| U-Net from scratch | `outputs/p0011/unet_weights.pt` (in repo) |
| Random Forest | `outputs/p0011/rf_model.pkl` (in repo) |

## 5. Hyperparameter documentation (Required)

All hyperparameters documented in:
- `configs/p0011_yvutu.yaml`
- `papers/drafts/p0011_yvutu_deforestation/methods.md`

## 6. Training procedure documentation (Required)

Documented in:
- `scripts/train_p0011_full.py` (executable script)
- `scripts/train_p0011_quickstart.sh` (one-command reproduction)
- `docs/REPRODUCIBILITY.md` (step-by-step guide)

## 7. Evaluation procedure documentation (Required)

Documented in:
- `scripts/evaluate_p0011.py` (executable)
- `docs/METRICS.md` (F1, IoU, precision, recall definitions)
- `outputs/p0011/metrics.json` (raw outputs)

## 8. Statistical testing (Recommended)

- Bootstrap confidence intervals on F1 scores (10,000 iterations)
- McNemar's test for pairwise model comparison (p < 0.05)

## 9. Random seeds (Required)

| Seed used | Where |
|-----------|-------|
| 42 | NumPy, PyTorch, scikit-learn (Python) |
| 42 | Random Forest (sklearn) |
| 42 | U-Net initialization |
| 42 | Yvutu initialization |
| 42 | Tile ID hashing |

## 10. Hyperparameter sensitivity analysis (Recommended)

- Tested 5, 10, 15, 20, 30 epochs
- Tested 12, 30, 50, 100 tiles
- Tested LR 1e-5, 1e-4, 1e-3
- Results in `outputs/p0011/hp_search/`

## 11. Code testing (Recommended)

- 27 unit tests passing
- Integration test (8 stages) passing
- Continuous integration via GitHub Actions

## 12. Docker image (Recommended)

```bash
docker pull weissvanderpol/satellite-paraguay:latest
docker run -it --rm satellite-paraguay make run-paper-1
```

---

## Reproducibility commands

```bash
# 1. Clone repo
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay
cd satellite-paraguay

# 2. Install dependencies
pip install -r requirements.txt

# 3. Reproduce paper results (CPU)
python3 scripts/train_p0011_full.py \
  --epochs 15 \
  --n-tiles 30 \
  --output-dir outputs/p0011 \
  --seed 42

# 4. Verify outputs match paper
python3 scripts/verify_reproducibility.py

# 5. View figures
ls outputs/p0011/figures/

# 6. View tables
ls outputs/p0011/tables/
```

Expected outputs:
- `outputs/p0011/metrics.json` — F1, mIoU, precision, recall per model
- `outputs/p0011/figures/fig1_ndvi_timeseries.png`
- `outputs/p0011/figures/fig2_model_comparison.png`
- `outputs/p0011/figures/fig3_model_comparison_bars.png`
- `outputs/p0011/figures/fig4_yvutu_confusion_matrix.png`
- `outputs/p0011/tables/table1_main_results.json`
- `outputs/p0011/tables/table2_confusion_matrices.json`
- `outputs/p0011/tables/table3_dataset_stats.json`
- `outputs/p0011/tables/table1_main_results.tex`

## Code DOI (Zenodo)

Will be minted upon acceptance:
- DOI: 10.5281/zenodo.XXXXXXX
- URL: https://doi.org/10.5281/zenodo.XXXXXXX

## Data DOI (Zenodo)

Synthetic Chaco dataset:
- DOI: 10.5281/zenodo.XXXXXXX
- URL: https://doi.org/10.5281/zenodo.XXXXXXX
