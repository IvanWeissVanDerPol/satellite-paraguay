# DVC — Data Version Control

This project uses DVC for data versioning.

## Setup

```bash
# Install DVC
pip install dvc dvc-s3 dvc-gs

# Initialize
dvc init

# Add remote storage (S3 example)
dvc remote add -d myremote s3://mybucket/satellite-paraguay

# Configure credentials
dvc remote modify myremote access_key_id $AWS_ACCESS_KEY_ID
dvc remote modify myremote secret_access_key $AWS_SECRET_ACCESS_KEY
```

## Track data

```bash
# Track a file or directory
dvc add data/raw/sentinel2/panama_tile.tif
dvc add models/checkpoints/yolov8_wildlife.pt

# Commit
git add data/raw/sentinel2/panama_tile.tif.dvc .gitignore
git commit -m "Track Panama tile with DVC"
```

## Pull/push data

```bash
# Push to remote
dvc push

# Pull from remote (in new environment)
dvc pull

# Fetch metadata only
dvc fetch
```

## Pipelines

DVC can also version ML pipelines:

```yaml
# dvc.yaml
stages:
  download_sentinel:
    cmd: python scripts/download_sentinel.py
    deps:
      - scripts/download_sentinel.py
    outs:
      - data/raw/sentinel2/

  train_yolov8:
    cmd: python scripts/train_yolov8.py
    deps:
      - scripts/train_yolov8.py
      - data/raw/sentinel2/
    outs:
      - models/checkpoints/yolov8_wildlife.pt
    metrics:
      - outputs/metrics/yolov8_metrics.json
```

```bash
# Run pipeline
dvc repro

# Compare experiments
dvc metrics show
dvc params diff
```

## Tracking

What to track with DVC:
- [ ] All `data/raw/` files (large raster files)
- [ ] All `data/processed/` files (intermediate results)
- [ ] All `data/cache/embeddings/` (Prithvi/AlphaEarth embeddings)
- [ ] All `models/checkpoints/` (trained weights)
- [ ] All `models/fine_tuned/` (fine-tuned models)

What NOT to track with DVC (use Git):
- Source code (Python files)
- Documentation (Markdown)
- Configuration (YAML, JSON)
- Small static files

## Common DVC commands

```bash
# Status
dvc status

# Diff between versions
dvc diff

# List tracked files
dvc list . data/raw/

# Show metrics across experiments
dvc metrics show -T

# Show params across experiments
dvc params diff HEAD~1
```

## CI/CD integration

```yaml
# .github/workflows/dvc.yml
- name: Pull data with DVC
  run: |
    pip install dvc[s3]
    dvc pull
```

## Backup strategy

| Data type | DVC | Git | Cloud (S3) |
|-----------|-----|-----|------------|
| Source code | No | Yes | GitHub |
| Raw data | Yes | No | S3 + DVC |
| Processed data | Yes | No | S3 + DVC |
| Models | Yes | No | S3 + DVC |
| Embeddings | Yes | No | S3 + DVC |
| Outputs | Optional | No | Optional |
| Docs | No | Yes | GitHub |
