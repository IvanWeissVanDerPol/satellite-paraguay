# Methods

## M.1 Data sources

The pilot experiment used **synthetic data only**. This is the
single most important caveat of the paper, so we state it first
and explain the chain of choices:

### M.1.1 Synthetic dataset

We generated **4 scenes** of synthetic soybean NDVI/EVI time series,
each 256×256 pixels with **18 monthly composites** spanning the
2022-2023 growing season (18 months × 4 scenes = 72 monthly composites
total; 786,432 pixels).

Why synthetic:

- **No real INBIO farm-yield data was available** in the
  experiment environment. The INBIO partnership exists in the
  project but the yield-data transfer was not completed at
  experiment time.
- **No real Sentinel-2 for the specific period was downloaded**
  (the 2 cached tiles are 2024 and over a different geography).
- A synthetic dataset was the fastest path to a proof-of-pipeline
  demonstration. The synthetic data was generated from a simple
  "phenology-shaped" NDVI profile (low at start, peak mid-season,
  decline at harvest) plus uniform-yield labels.

The synthetic dataset is **adequate for pipeline validation**
(the train/val/test split works, the loss decreases monotonically,
the evaluation script runs end-to-end) but **inadequate for
publication-quality performance claims** (the synthetic
patterns are too simple for any transfer signal to develop).

### M.1.2 Three-band NDVI/EVI/SCL features

Each synthetic scene provides 3 spectral-band-equivalent features
per pixel:

- **NDVI** (Normalized Difference Vegetation Index): phenology
  signal.
- **EVI** (Enhanced Vegetation Index): biomass signal with less
  saturation than NDVI.
- **SCL** (Scene Classification): pixel-quality mask (we keep
  cloud-free pixels only).

The 3-band choice simulates the input pipeline that real Sentinel-2
L2A would provide; the real-data pipeline uses the same 3 features
plus B02-B08 surface reflectance.

## M.2 Model architecture

### M.2.1 Multi-task CNN backbone

The architecture is a 12-layer ResNet-50-style encoder with three
task heads attached at the bottleneck:

- **Head 1**: Soybean-pixel binary classification (1 logit).
- **Head 2**: AGB regression (1 continuous output, Mg/ha).
- **Head 3**: Per-pixel yield regression (1 continuous output,
  t/ha).

This is the standard multi-task learning setup. The shared
backbone means the three tasks are trained jointly via a
combined loss:

$$\mathcal{L} = \alpha \mathcal{L}_{\text{cls}} + \beta \mathcal{L}_{\text{AGB}} + \gamma \mathcal{L}_{\text{yield}}$$

with hyperparameters $\alpha = 1.0$, $\beta = 0.1$, $\gamma = 1.0$
selected to balance the magnitude of the per-task losses.

### M.2.2 Cross-domain transfer learning

We tested the cross-domain transfer hypothesis by:

1. **Source task**: deforestation detection from Hansen GFC v1.11
   `lossyear` × `treecover2000` features (the model trained in
   Yvutu, Chapter 3).
2. **Target task**: soybean yield regression on the synthetic
   dataset.
3. **Transfer ratio**: the ratio of the target-task performance
   with the source-pretrained encoder vs. a from-scratch
   encoder on the target task.

A transfer ratio $r = 1.0$ means identical performance (perfect
transfer); $r = 0$ means no benefit; $r > 1$ would mean
counterproductive negative transfer.

### M.2.3 Training procedure

- Optimizer: Adam, learning rate $1 \times 10^{-3}$, weight decay
  $1 \times 10^{-5}$.
- Batch size: **1** (CPU constraint). This is below the
  recommended minimum of 32 for batch normalization to work
  correctly.
- Epochs: **8** (CPU constraint, ~7 minutes wall clock).
- Hardware: CPU (Intel, ~3 GB RAM peak).
- Random seed: 42.

The combination of **batch_size=1 + 8 epochs + synthetic labels**
is the specific set of constraints that produced the degenerate
all-zero prediction.

## M.3 Evaluation protocol

We use:

- **Per-pixel binary classification metrics** (precision, recall,
  F1, mIoU) for Head 1.
- **AGB regression** (R², RMSE, MAE) for Head 2.
- **Yield regression** (R², RMSE, MAE) for Head 3.
- **Cross-task transfer ratio** (Head 3 R² with source-pretrained
  backbone / Head 3 R² from-scratch).

Baseline models:

- **Persistence**: predict the average per-pixel value for
  regressions; predict all-zero for classification.
- **Random Forest**: 50 trees, 30 features, on the same
  3-band input.
- **From-scratch U-Net**: 12-layer ResNet encoder, single
  classification head; we compare the multi-task CNN against
  this for the transfer signal.

### M.3.1 Train / val / test split

- **Train**: 80 / 144 = 56% of pixels (random split within
  scene 1 only — see Section 4.3 for the temporal-leakage
  caveat).
- **Validation**: 32 / 144 = 22% (random split, scene 1).
- **Test**: 32 / 144 = 22% (random split, scene 1).

The **scenes (n=4)** are not split across train/val/test —
all train and val come from the same scene, with the other three
scenes held out for qualitative inspection but not formally
included in the test split.

## M.4 Reproducibility

- Random seed: 42 (numpy + torch).
- Code: open-source under CC-BY-NC-4.0 (`LICENSE`).
- Pipeline implementation: `scripts/train_improved_unet.py` for
  the encoder + `src/papers/p0025_yrupe_yield/pipeline.py`
  (YrupePipeline class with predict_yield, load_inbio_data).
- Synthetic dataset: generated reproducibly from `set_seed(42)`
  + the NDVI phenology profile.
- Output JSON: `outputs/p0025/real_metrics.json` (or the
  experiment log in `ACTUAL_RESULTS.md`).
- Pretrained weights: planned but not produced (the CNN did not
  converge).
- Honest-results log: `ACTUAL_RESULTS.md`.

## M.5 What the experiment did NOT control for

The pilot is intentionally minimal. The honest enumeration:

- **No augmentation**: the synthetic data is not rotated /
  flipped / crop-augmented.
- **No class weighting**: the soybean / non-soybean class
  imbalance is not addressed.
- **No dropout / regularization**: the network is small enough
  that overfitting was not the dominant failure mode; the
  issue is under-training, not over-fitting.
- **No early stopping**: training runs for the full 8 epochs.
- **No curriculum**: training does not start with easy
  examples and progress to hard.

A production-quality version of this experiment would have all
of these. The pilot deliberately omits them to keep the
fail-loud failure mode visible: **the synthetic + CPU + 8-epoch
setup is what makes the negative result reproducible**.

A successful replication requires:

1. Real Sentinel-2 (≥150 tiles) + real INBIO labels (≥500 farm
   records).
2. GPU training (Vast.ai A100, ~$20).
3. 30+ epochs with batch normalization working.
4. Train/test temporal split (2022 train / 2023 test, or
  analogous).

The cost is **2 weeks + $20** for a publication-quality
replication. We did not do it because the synthetic pilot
returned a clear negative result that did not justify the spend
without first revisiting the experimental design.
