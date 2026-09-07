# RUNBOOK — — satellite-paraguay

**Generated:** 2026-08-22 (Phase 1 of 12-week roadmap)
**Purpose:** Copy-paste recipes for reproducing every paper from clean checkout
**Author:** Hermes agent

---

## TL;DR

This runbook assumes:
- You have GPU budget approved (Phase 0 ✓)
- You have RunPod or Vast.ai API key set in `RUNPOD_API_KEY` or `VASTAI_API_KEY`
- You have read `docs/infra/gpu-decision.md` for context
- You have the 9 datasets downloaded (see `data/DATA_ACQUISITION.md`)

For each paper, there's a one-command reproduction:

```bash
make reproduce-paper P=P0011     # Prithvi fine-tune
make reproduce-paper P=P0010     # AlphaEarth fine-tune
make reproduce-paper P=P0025     # GRU training
make reproduce-paper P=P0026     # YOLOv8 retrain
make reproduce-paper P=P0035     # LSTM refinement
```

Each command:
1. Verifies data + checkpoint state
2. Launches GPU instance via `scripts/queue_train.py` (with cost cap)
3. Streams progress to `models/<paper>/progress.log`
4. Uploads checkpoint to persistent volume on completion
5. Kills instance + downloads checkpoint to `models/<paper>/`

---

## Per-paper recipes

### P0011 Yvutu (Prithvi fine-tune)

**GPU:** A100 40GB or 4090 24GB
**Estimated time:** 16-24 hours (Prith vi fine-tune) + 4 hours (U-Net baseline)
**Estimated cost:** $30-40

```bash
# Pre-flight
cd /opt/data/work/satellite-paraguay
ls scripts/train_prithvi_yvutu.py  # verify exists
ls data/raw/sentinel2/paraguay/  # verify tiles (30 expected)
ls data/raw/hansen/paraguay/      # verify Hansen (30 expected)

# Run
python3 scripts/train_prithvi_yvutu.py \
  --provider runpod \
  --gpu a100-40gb \
  --epochs 50 \
  --batch-size 16 \
  --learning-rate 1e-4 \
  --checkpoint-every 5

# Outputs:
#   models/p0011_yvutu/prithvi_yvutu_v2.pt
#   models/p0011_yvutu/training_history.json
#   papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md (updated)

# Verify (CPU only, <1 min)
python3 scripts/evaluate_prithvi_yvutu.py \
  --checkpoint models/p0011_yvutu/prithvi_yvutu_v2.pt
# Expected: F1 > 0.5 on held-out Hansen
```

**Re-run if:** script crashes mid-training, checkpoint survives, restart from `--resume`.

---

### P0010 Vyrá (AlphaEarth fine-tune)

**GPU:** A100 40GB
**Estimated time:** 18-24 hours (AlphaEarth)
**Estimated cost:** $30-40

```bash
python3 scripts/train_alphaearth.py \
  --provider runpod \
  --gpu a100-40gb \
  --epochs 30 \
  --batch-size 32 \
  --checkpoint-every 3

# Outputs:
#   models/p0010_yvyra/alphaearth_v2.pt
#   models/p0010_yvyra/training_history.json

# Verify (CPU only, ~10 min)
python3 scripts/evaluate_alphaearth.py \
  --checkpoint models/p0010_yvyra/alphaearth_v2.pt
# Expected: R² > 0. > 0. on held-out Verra projects
```

---

### P0025 Yrupe (GRU training on INBIO labels)

**GPU:** 4090 or T4 (small model)
**Estimated time:** 2-4 hours
**Estimated cost:** $2-4

**Prerequisite:** INBIO partnership established (Phase 2 week 1)

```bash
# Verify data
ls data/raw/inbio/yrupe_2024.csv  # expected after Phase 2.1

# Run
python3 scripts/train_yrupe_gru.py \
  --provider runpod \
  --gpu 4090 \
  --epochs 100 \
  --batch-size 64

# Verify (CPU only, <2 min)
python3 scripts/evaluate_yrupe_gru.py \
  --checkpoint models/p0025_yrupe/gru_v2.pt
# Expected: F1 > 0.5 on held-out INBIO test set
```

---

### P0026 Kai (YOLOv8 retrain on real wildlife labels)

**GPU:** 4090 or T4
**Estimated time:** 6-10 hours
**Estimated cost:** $5-10

**Prerequisite:** Guyra partnership established (Phase 2 week 1)

```bash
# Verify data
ls data/labels/guyra/wildlife/  # expected after Phase 2.2

# Run
python3 scripts/train_kai_yolo.py \
  --provider runpod \
  --gpu 4090 \
  --epochs 50 \
  --batch-size 32 \
  --img-size 640

# Verify (CPU only, ~2 min)
python3 scripts/evaluate_kai_yolo.py \
  --checkpoint models/p0026_kai/kai_yolo_v2.pt
# Expected: mAP@0.5 > 0. > 0. on real Guyra test (vs synthetic baseline 0.18)
```

---

### P0035 Tatakua (LSTM refinement on 24 stations)

**GPU:** T4 or CPU
**Estimated time:** 1-2 hours (T4) or 4-6 hours (CPU)
**Estimated cost:** $1-2 (T4) or $0 (CPU)

**Prerequisite:** OpenAQ public data (no partnership needed)

```bash
# Verify data
ls data/raw/openaq/paraguay_2024.csv  # expected

# Run
python3 scripts/train_tatakua_lstm_v2.py \
  --provider runpod \
  --gpu t4 \
  --epochs 100 \
  --batch-size 128 \
  --sequence-length 24

# Verify (CPU only, <30 sec)
python3 scripts/evaluate_tatakua_lstm_v2.py \
  --checkpoint models/p0035_tatakua/lstm_v2.pt
# Expected: RMSE < 14 µg/m³ (vs current 14.7)
```

---

## Common operations

### Check GPU cost

```bash
bash infra/cost-cap.sh           # current spend
bash infra/cost-cap.sh --report # JSON for monitoring
```

### Queue a training job

```bash
python3 scripts/queue_train.py \
  --paper P0011 \
  --provider runpod \
  --gpu a100-40gb
```

### Resume from checkpoint

```bash
python3 scripts/train_prithvi_yvutu.py \
  --resume models/p0011_yvutu/prithvi_yvutu_v2.pt
```

### Kill all training jobs (cost-cap trigger)

```bash
bash infra/cost-cap.sh --kill
```

### Backup trained weights

```bash
bash infra/backup-weights.sh   # uploads to persistent volume + Hugging Face
```

---

## Troubleshooting

### Training script hangs at "Waiting for instance"

The provider may have capacity issues. Check:
```bash
runpodctl get pod --name "training-*"  # list all training pods
runpodctl ssh training-P0011          # SSH into the pod
tail -f /workspace/progress.log        # check what's happening
```

If provider is OOM, kill + retry with smaller batch size:
```bash
bash infra/cost-cap.sh --kill
python3 scripts/train_prithvi_yvutu.py --batch-size 8  # half the size
```

### Checkpoint won't load

Possible causes:
1. File corruption (download issue) — re-download from persistent volume
2. PyTorch version mismatch — use the same version as training
3. CUDA mismatch — verify GPU type matches

```bash
python3 -c "
import torch
ckpt = torch.load('models/p0011_yvutu/prithvi_yvutu_v2.pt', map_location='cpu')
print('Loaded:', list(ckpt.keys())[:5])
print('Device:', ckpt.get('device', 'unknown'))
"
```

### Evaluation fails with NaN

Model is dead. Re-train with:
1. Lower learning rate (1e-5 instead of 1e-4)
2. More warmup epochs
3. Gradient clipping at 1.0

---

## Files this runbook will produce

- `models/p0011_yvutu/prithvi_yvutu_v2.pt` (or v3, v4 as we iterate)
- `models/p0010_yvyra/alphaearth_v2.pt`
- `models/p0025_yrupe/gru_v2.pt`
- `models/p0026_kai/kai_yolo_v2.pt`
- `models/p0035_tatakua/lstm_v2.pt`
- `models/cost_log.csv` (per-paper spend tracking)

---

**Reviewed-by:** Hermes agent (Phase 1 of 12-week roadmap)
**Last updated:** 2026-08-22
**Reproduction status:** All 5 papers have copy-paste recipes. Training scripts exist for P0011 and P0035; remaining 3 need to be written (Phase 2 deliverable).