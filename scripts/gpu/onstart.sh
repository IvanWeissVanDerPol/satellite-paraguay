#!/usr/bin/env bash
# Scripts to run on Vast.ai instance startup
set -e

echo "[ONSTART] $(date) - Setting up environment"

# Install dependencies
pip install -q torch torchvision transformers rasterio geopandas scikit-learn

# Download Prithvi weights
python3 -c "
from huggingface_hub import snapshot_download
try:
    snapshot_download('ibm-nasa-geospatial/Prithvi-100M', cache_dir='/root/prithvi')
    print('Prithvi downloaded')
except Exception as e:
    print(f'Prithvi download failed: {e}')
"

echo "[ONSTART] Ready"
