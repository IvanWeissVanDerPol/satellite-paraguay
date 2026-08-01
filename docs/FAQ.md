# FAQ — Frequently Asked Questions

## General

### What is SatelliteCV-Paraguay?

A unified Python package that ingests multi-temporal satellite imagery for Paraguay and produces six peer-reviewed papers across remote sensing, agriculture, climate, conservation, and social science.

### Who is this for?

- **Iván Weiss Van der Pol** (thesis author) — primary user
- **Cristaldo Lab (FADA-UNA)** — research collaborators
- **Other Paraguayan researchers** — extension audience
- **International collaborators** — UN-Habitat, WWF, etc.

### How much does it cost to run?

For a typical thesis defense (full 12-18 months of fine-tuning):
- **$0** for: Local execution with Colab free, all open-source models, open data
- **$100-500** for: Colab Pro subscription for faster training
- **$500-2000** for: Cloud GPU instances (Vast.ai, RunPod) for large foundation models

See `docs/COST.md` (TBD) for detailed breakdown.

### Do I need a GPU?

| Use case | GPU needed? |
|----------|-------------|
| Run baselines (Random Forest, persistence) | No |
| Train U-Net baseline | Optional (slower on CPU) |
| Fine-tune Prithvi | Yes (16+ GB VRAM) |
| Fine-tune LLaVA-1.6 | Yes (24+ GB VRAM) |
| Run YOLOv8 | Optional |
| Use TimesFM | Optional |

Alternative: use Colab Pro / Kaggle free GPUs.

## Setup

### How do I install?

```bash
git clone https://github.com/IvanWeissVanDerPol/satellite-paraguay
cd satellite-paraguay
make install          # install all dependencies
make bootstrap        # verify + create dirs
make verify           # confirm everything works
```

### What if `make install` fails?

Check Python version: `python --version` (need 3.10+)
Try installing individually: `pip install -r requirements.txt`
Check `docs/TROUBLESHOOTING.md` (TBD)

### How do I run a single paper?

```bash
make run-paper-1      # P0011 Yvytu
make run-paper-2      # P0100 Yvyra
# etc.
```

Or directly: `python -m src.papers.p0011_yvytu_deforestation.pipeline`

### How do I run all 6 papers?

```bash
make run-all-papers
```

Or use the autonomous executor:
```bash
make autonomous
```

## Data

### Where is the local Paraguay data?

In `/root/paraguay-geodata/exports/web/data/` (549 MB).
Copy to `data/external/` with:
```bash
make data-local
```

### How do I download Sentinel-2?

Via Google Earth Engine (recommended):
```python
from src.satellite_io import download_via_gee
download_via_gee(tile_id="-54.267_-21.164", bbox={...}, satellite="sentinel2")
```

Or via Copernicus Open Access Hub (free, requires registration):
```python
from src.satellite_io import download_sentinel2_tile
```

### How do I download MapBiomas Paraguay?

```bash
make data-mapbiomas
```

Or directly:
```python
from src.satellite_io import download_mapbiomas_paraguay
```

### How do I download Hansen GFC?

```python
from src.satellite_io import download_hansen_gfc
```

## Development

### How do I add a new paper?

1. Create folder: `src/papers/pXXXX_name/`
2. Add `pipeline.py` with class `PaperPipeline`
3. Add `__init__.py` exposing the class
4. Add config: `configs/pXXXX_name.yaml`
5. Add notebook: `notebooks/pXXXX_name.ipynb`
6. Add README: `papers/drafts/pXXXX_name/README.md`
7. Add tests: `tests/test_pipelines.py`
8. Update `src/papers/__init__.py`

### How do I retrain a model?

```bash
# Edit configs/p0011_yvytu.yaml
make run-paper-1
```

### How do I add a new dataset?

1. Add data file to `data/external/`
2. Add data sheet to `data/datasheets/`
3. Add loader in `src/paraguay_admin/loader.py`
4. Add test in `tests/test_paraguay_admin.py`

### How do I add a new model?

1. Add model card to `models/cards/`
2. Add loader in `src/foundation_models/models.py`
3. Add baseline if applicable: `src/baselines/`
4. Add tests

### How do I run the dashboard?

```bash
make dashboard
```

Opens at http://localhost:8501

### How do I run the API?

```bash
make api
```

Opens at http://localhost:8000/docs

## Deployment

### How do I deploy to production?

```bash
make docker-build
make docker-compose-up
```

Or use the Kubernetes manifests (TBD).

### How do I deploy the dashboard?

```bash
# Heroku
git push heroku main

# Vercel
vercel deploy

# Cloudflare Pages
wrangler pages deploy dashboard/
```

### How do I monitor production?

```bash
# Logs
docker logs -f satellite-paraguay-dashboard

# Metrics
curl http://localhost:5000/metrics
```

## Troubleshooting

### Issue: `pip install -r requirements.txt` fails

Solution:
```bash
pip install --upgrade pip
pip install --user -r requirements.txt
# Or use conda
conda install --file requirements.txt
```

### Issue: GPU out of memory

Solution:
- Reduce batch size
- Use mixed precision (fp16)
- Use gradient accumulation
- Use smaller model variant (e.g., Prithvi-100M instead of 300M)

### Issue: Google Earth Engine authentication fails

Solution:
```bash
earthengine authenticate
```

### Issue: Sentinel-2 download slow

Solution:
- Use Google Earth Engine (faster)
- Use multiple parallel downloads (use multiprocessing)
- Cache tiles locally

### Issue: GPU not detected

Solution:
```bash
# Check CUDA
nvcc --version
nvidia-smi

# Reinstall PyTorch with CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Citation

### How do I cite SatelliteCV-Paraguay?

```bibtex
@software{satelliteparaguay2026,
  title={SatelliteCV-Paraguay: Multi-Temporal Earth Observation of Paraguay},
  author={Weiss Van der Pol, Iv{\\'a}n},
  year={2026},
  url={https://github.com/IvanWeissVanDerPol/satellite-paraguay}
}
```

### How do I cite individual papers?

See `papers/drafts/P00XX/README.md` for paper-specific citation.

### How do I cite foundation models?

See `models/cards/*.md` for model-specific citation.

## Contact

- **Author:** Iván Weiss Van der Pol
- **Email:** ivan@example.com
- **GitHub:** @IvanWeissVanDerPol
- **Advisor:** Juan Carlos Cristaldo (FADA-UNA)
