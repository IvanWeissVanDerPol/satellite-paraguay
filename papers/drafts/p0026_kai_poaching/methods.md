# Methods

## M.1 Data sources

### M.1.1 Synthetic training data — Blender renders

We generated **1,280 synthetic training images** covering 24 species
(10 large mammals, 8 birds, 4 reptiles, 2 small mammals) using
Blender 4.x with the BlenderProc procedural rendering pipeline.
Each image rendered in 3-5 random poses per species (300-500
images per species), placed on 4 random backgrounds (dry Chaco
forest, palm savanna, riparian, trail clearing) with random
lighting and camera-angle variation.

Rendering time per image: ~17 seconds on CPU; ~1.5 seconds on GPU
(the experiment ran on CPU due to budget constraints, so the
~6-hour total rendering wall clock). The synthetic images
approximate the visual character of camera-trap imagery at a
differentiable level: animal bodies are modeled with reasonable
fidelity, but **the texture and lighting match between synthetic
and real is not pixel-accurate**. This is a typical limitation of
photorealistic synthetic data for wildlife CV.

### M.1.2 Real evaluation data — Guyra Paraguay

We evaluated the trained model on the **Guyra Paraguay public
camera-trap dataset** (5,000 images, 8 species: jaguar, puma,
ocelot, tapir, deer, capybara, agouti, armadillo). The dataset is
hosted at a public URL and is the most comprehensive real wildlife
camera-trap dataset available for Paraguay.

The 8 species cover ~80% of the large-mammal camera-trap captures
in Defensores del Chaco. **Reptiles and birds are not in the
Guyra Paraguay public dataset**; our per-species analysis is
therefore restricted to the 8 large-mammal species.

The 5,000 images are split into 5 folds for cross-validation
(1,000 per fold), with **location-aware stratification** where
possible (a single camera location's images are kept in one
fold to avoid leakage).

## M.2 Model architecture

### M.2.1 YOLOv8-S

We use the **Ultralytics YOLOv8-Small** architecture (11.2M
parameters), pretrained on **COCO 2017** for 100 epochs. The COCO
pretraining provides a generic object detector; we fine-tune on
the 1,280 synthetic images for 12 epochs at batch size 4 (CPU
constraint).

YOLOv8-S specifications:

- 11.2M parameters (the "S" or small variant)
- Backbone: CSPDarknet53
- Head: YOLOv8 anchor-free detection head
- Loss: YOLOv8 composite (objectness + classification +
  bounding-box)

The fine-tune initialization is COCO-pretrained weights
downloaded from the Ultralytics model hub. We do **not** initialize
from YOLOv8-M, -L, or -X variants because their larger parameter
count exceeds our CPU memory budget.

### M.2.2 Training procedure

- Optimizer: AdamW with cosine LR schedule.
- Learning rate: $1 \times 10^{-3}$.
- Batch size: **4** (CPU constraint).
- Epochs: **12** (CPU constraint).
- Augmentation: standard YOLOv8 augmentations (mosaic, random
  affine, color jitter, random erasing).
- Hardware: CPU (Intel, ~3 GB RAM peak).
- Random seed: 42.

The combination of **batch=4 + 12 epochs + synthetic data** is the
specific combination tested. It is below the standard YOLOv8
recipe (typically batch=32-64 + 100+ epochs on full real data) but
reflects the constraints of the pilot environment.

## M.3 Evaluation protocol

### M.3.1 5-fold cross-validation

We evaluate the trained model on the **Guyra Paraguay real
camera-trap dataset** using 5-fold cross-validation:

- Each fold = 1,000 images, stratified by species.
- The detector is run on each fold with the synthetic-trained
  weights.
- mAP@0.5 (mean Average Precision at IoU threshold 0.5) is
  computed per fold, then averaged.
- Standard deviation across folds is reported as the
  variance measure.

### M.3.2 Per-species breakdown

For each of the 8 species in the Guyra dataset, we compute
per-species mAP. This is the **substantive per-species finding**
of the paper — different species respond differently to
synthetic-vs-real gap.

### M.3.3 Synthetic vs Real comparison

The same YOLOv8-S trained on synthetic data is evaluated on:

1. The **synthetic validation split** (320 of 1,280 images held
   out during training) — measures in-distribution performance.
2. The **real camera-trap test split** (5,000 images from Guyra
   Paraguay) — measures out-of-distribution performance.

The **gap** between (1) and (2) is the synthetic-to-real
generalization gap, which is the headline finding.

## M.4 Reproducibility

- Random seed: 42 (numpy).
- Blender rendering script: `scripts/render_synthetic_wildlife.sh`.
- YOLOv8 training script: `scripts/train_yolov8_synthetic.py`.
- Synthetic dataset: `data/synthetic/wildlife_blender/` (1,280
  images, ~6 hours generation time on CPU).
- Real evaluation dataset: `data/cache/cameratrap/guyra_5k/` (5,000
  images, public URL).
- Per-fold metrics: `outputs/p0026/per_fold_metrics.json`.
- Output JSON: `outputs/p0026/synthetic_vs_real_gap.json`.
- Pretrained weights: `models/yolov8_s/kai_synthetic.pt` (~44 MB).
- Honest-results log: `ACTUAL_RESULTS.md`.

## M.5 Software and compute

- Python 3.11 + Ultralytics YOLOv8 8.0+ + PyTorch 2.0+.
- Blender 4.x + BlenderProc for synthetic image generation.
- Total wall-clock compute: ~6 hours (synthetic) + ~1 hour
  (training) + ~30 minutes (evaluation across 5 folds).
- All training and evaluation on CPU.
