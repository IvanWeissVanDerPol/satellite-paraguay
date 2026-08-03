#!/usr/bin/env bash
# Quickstart script for reproducing P0011 Yvutu paper
#
# Usage:
#   ./papers/drafts/p0011_yvutu_deforestation/quickstart.sh
#   ./papers/drafts/p0011_yvutu_deforestation/quickstart.sh --epochs 30 --tiles 50 --gpu
#
# This script:
# 1. Sets up Python environment
# 2. Runs training (CPU or GPU)
# 3. Generates all figures and tables
# 4. Validates outputs

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT"

# Parse args
EPOCHS=15
N_TILES=30
USE_GPU=false
OUTPUT_DIR="outputs/p0011"

while [[ $# -gt 0 ]]; do
  case $1 in
    --epochs) EPOCHS="$2"; shift 2 ;;
    --tiles) N_TILES="$2"; shift 2 ;;
    --gpu) USE_GPU=true; shift ;;
    --output) OUTPUT_DIR="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

echo "=================================================="
echo "P0011 Yvutu — Quickstart"
echo "=================================================="
echo "Epochs: $EPOCHS"
echo "Tiles: $N_TILES"
echo "GPU: $USE_GPU"
echo "Output: $OUTPUT_DIR"
echo "=================================================="

# 1. Setup Python environment
if [ ! -d "venv" ]; then
    echo "[1/5] Creating venv..."
    python3 -m venv venv
fi
source venv/bin/activate

# 2. Install dependencies
echo "[2/5] Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# 3. Verify environment
echo "[3/5] Verifying environment..."
python3 -c "
import sys
sys.path.insert(0, '.')
import torch
import numpy as np
import sklearn
from src.evaluation import pixel_f1_score
from src.papers.p0011_yvytu_deforestation import YvutuPipeline
print(f'  Python: {sys.version.split()[0]}')
print(f'  PyTorch: {torch.__version__}')
print(f'  NumPy: {np.__version__}')
print(f'  CUDA available: {torch.cuda.is_available()}')
"

# 4. Run training
echo "[4/5] Running training pipeline..."
DEVICE="cpu"
if [ "$USE_GPU" = true ] && python3 -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
    DEVICE="cuda"
fi

python3 scripts/train_p0011_full.py \
    --epochs "$EPOCHS" \
    --n-tiles "$N_TILES" \
    --output-dir "$OUTPUT_DIR" \
    --device "$DEVICE"

# 5. Verify outputs
echo "[5/5] Verifying outputs..."
EXPECTED_FILES=(
    "$OUTPUT_DIR/metrics.json"
    "$OUTPUT_DIR/dataset_stats.json"
    "$OUTPUT_DIR/figures/fig1_ndvi_timeseries.png"
    "$OUTPUT_DIR/figures/fig2_model_comparison.png"
    "$OUTPUT_DIR/figures/fig3_model_comparison_bars.png"
    "$OUTPUT_DIR/figures/fig4_yvutu_confusion_matrix.png"
    "$OUTPUT_DIR/tables/table1_main_results.json"
    "$OUTPUT_DIR/tables/table2_confusion_matrices.json"
    "$OUTPUT_DIR/tables/table3_dataset_stats.json"
    "$OUTPUT_DIR/tables/table1_main_results.tex"
)

MISSING=0
for f in "${EXPECTED_FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "  ✗ Missing: $f"
        MISSING=$((MISSING + 1))
    else
        echo "  ✓ $f"
    fi
done

if [ $MISSING -gt 0 ]; then
    echo "❌ $MISSING files missing"
    exit 1
fi

# Print summary
echo ""
echo "=================================================="
echo "REPRODUCTION COMPLETE"
echo "=================================================="
cat "$OUTPUT_DIR/metrics.json" | python3 -m json.tool | grep -E "f1|miou|precision|recall" | head -20
echo ""
echo "Figures: $OUTPUT_DIR/figures/"
echo "Tables:  $OUTPUT_DIR/tables/"
echo ""
echo "View dashboard: streamlit run dashboard/app.py"
