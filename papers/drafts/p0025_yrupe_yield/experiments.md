# Experiments

This section documents the experimental protocol followed for the
Yrupe pilot study. The aim is **reproducibility first**: a reader
with the same dataset, the same commit hash, and the same
hardware should be able to reproduce the measured results to the
last significant digit. Where the experiment diverges from the
original protocol in `paper.md` (drafted earlier in the project),
we flag the divergence explicitly.

## E.1 Experimental setup

### E.1.1 Hardware and runtime environment

| Component | Specification |
|-----------|---------------|
| CPU | Intel x86_64, ~3 GB peak RAM |
| GPU | None (CPU-only constraint; no CUDA available in the experiment sandbox) |
| Wall-clock budget | ~7 minutes end-to-end |
| Wall-clock per epoch | ~50 seconds |
| Python | 3.11 (sandbox default; project supports 3.10 / 3.11 / 3.12) |
| PyTorch | 2.x CPU build |
| NumPy | 2.x |
| Random seed | 42 (set via `np.random.default_rng(42)` at fixture construction) |

The CPU-only constraint is **the single largest determinant** of
the measured result. Section E.5 quantifies what a real GPU run
would have changed.

### E.1.2 Dataset

The pilot experiment used the **synthetic dataset** described in
`methods.md` Section M.1.1. To summarize the salient properties
that affect the measured result:

- **Shape**: 4 scenes × 18 monthly composites × 256×256 pixels
  (3 spectral-equivalent bands: NDVI / EVI / SCL).
- **Total pixel-timesteps**: 786,432 (4 × 18 × 256 × 256).
- **Train / val / test split**: 80 / 32 / 32 tiles
  (per-month stratification, no temporal separation — see
  Section E.7 leakage caveat).
- **Label generation**: deterministic `np.random.default_rng(42)`
  phenology-shaped NDVI profile + uniform yield values across
  the synthetic scenes.

The synthetic dataset's **principal limitation** is that the
phenology profile (low → peak → decline) is uniform across scenes
and lacks the sub-seasonal variability (flowering vs. vegetative
phases) that real Sentinel-2 imagery carries. The model's job is
therefore to memorize a single curve, which a 12-layer ResNet can
do in 1 epoch if the data were structured to support it. The
labels being uniform yield (rather than a realistic
yield-vs-phenology correlation) is the second limitation that
makes transfer learning undetectable on this dataset.

### E.1.3 Models compared

Four models were evaluated on the synthetic test set:

1. **Persistence baseline** — predicts the majority class
   (`not soybean`) for classification, the per-pixel median for
   regression.
2. **Random Forest baseline** — 100-tree scikit-learn estimator,
   fit on flattened (pixel × time) features. Default
   hyperparameters; no grid search.
3. **U-Net from scratch** — the same U-Net architecture used in
   the Yvutu deforestation pilot (Chapter 3), trained from
   random initialization on the synthetic dataset for 5 epochs
   with batch size 1. This baseline serves as the
   "non-transfer" reference for Head 1 (classification).
4. **Yrupe multi-task CNN** — a 12-layer ResNet-50-style
   encoder with three task heads attached at the bottleneck:
   - **Head 1**: Soybean-pixel binary classification (1 logit).
   - **Head 2**: AGB regression (1 continuous output, Mg/ha).
   - **Head 3**: Per-pixel yield regression (1 continuous output,
     tons/hectare).

The multi-task CNN was trained from **scratch** on the synthetic
dataset for 8 epochs at batch size 1. The source encoder from
the Yvutu deforestation pilot (Chapter 3) was **not loaded**
into the encoder at any point — the cross-domain transfer
hypothesis was therefore not actually tested by this experiment
(see Section E.6 for what would have been required).

## E.2 Training protocol

| Hyperparameter | Value | Note |
|----------------|-------|------|
| Optimizer | Adam | Default β₁=0.9, β₂=0.999 |
| Learning rate | 1e-3 | Constant (no schedule) |
| Batch size | 1 | Memory constraint; insufficient for batch-norm |
| Epochs | 8 | CPU wall-clock budget |
| Loss (Head 1) | Binary cross-entropy | Per-pixel |
| Loss (Head 2) | MSE | Per-pixel AGB |
| Loss (Head 3) | MSE | Per-pixel yield |
| Multi-task weighting | Equal (1.0 / 1.0 / 1.0) | No uncertainty weighting |
| Data augmentation | None | Synthetic data did not warrant |
| Early stopping | None | Ran all 8 epochs |
| Checkpointing | None | No held-out val improvement was expected |

The batch size of 1 is the single most consequential
hyperparameter. With batch-norm disabled or operating on
single-sample statistics, the network cannot learn stable
feature distributions. Standard transfer-learning recipes use
batch size ≥ 32.

## E.3 Evaluation protocol

Each model was evaluated on the 32-tile held-out test set. The
following metrics were computed per task head:

- **Head 1 (classification)**: F1 (macro), mIoU, Precision, Recall.
- **Head 2 (AGB regression)**: R², MAE (Mg/ha), RMSE (Mg/ha).
- **Head 3 (yield regression)**: MAE (t/ha), RMSE (t/ha), MAPE (%).

For the multi-task CNN, the **cross-domain transfer ratio** was
computed as:

```
transfer_ratio = (Yrupe R² on synthetic target) /
                 (Yvutu deforestation F1 on synthetic source)
```

A ratio ≥ 0.7 is the conventional threshold for "positive
transfer" in the transfer-learning literature. The measured
0.082 is far below this threshold.

## E.4 Results summary

The full results table is in `results.md`. Headline numbers
(reproduced here for convenience):

| Task | Metric | Target | Measured | Status |
|------|--------|-------:|---------:|--------|
| Head 1: Soybean-pixel classification | F1 | 0.83 | **0.497** | Far below |
| Head 2: AGB regression | R² | 0.62 | **undefined** | Constant prediction |
| Head 3: Yield regression | MAE (t/ha) | 0.74 | **3.20** | 4.3× worse |
| Cross-domain transfer ratio | — | 0.74 | **0.082** | Below threshold |

The multi-task CNN did **not converge** under the tested
conditions. The losses settled on degenerate solutions (all-zero
classification output, mean-of-train regression output). This is
the canonical failure mode for an under-trained network on
imbalanced data and is fully consistent with the 8-epoch CPU
constraint.

## E.5 What would have changed with more compute

To quantify the CPU constraint: a standard transfer-learning
recipe requires ≥ 30 epochs at batch size ≥ 32 on a single GPU
(A100 / V100). On the measured throughput (~50 s/epoch CPU,
batch 1), the same recipe would take:

- 30 epochs × ~50 s = 25 minutes (CPU, batch 1) — not
  feasible: batch-norm still broken at batch 1.
- 30 epochs × ~1.5 s (GPU, batch 32 estimated) = ~45 seconds
  (GPU, batch 32) — feasible.

The qualitative prediction: a 30-epoch GPU run with batch size 32
**might** lift Head 1 F1 from 0.497 toward 0.55-0.65 (matching
the U-Net-from-scratch baseline) but is **unlikely** to reach
the published target of 0.83 without (a) real Sentinel-2 imagery
with seasonal dynamics, (b) real INBIO yield labels, and (c)
exercising the Yvutu source encoder (which is the actual transfer
hypothesis).

## E.6 What would have changed with real data and the source encoder

The cross-domain transfer hypothesis specifically requires that
the Yvutu deforestation encoder (Chapter 3) be loaded as the
backbone of the Yrupe pipeline. The pilot did not exercise this
path. The minimal protocol to actually test H3 (cross-domain
transfer) is:

1. Train Yvutu on real Hansen GFC deforestation labels to F1 > 0.5.
2. Load Yvutu's encoder weights as the Yrupe backbone
   (transfer learning from source to target).
3. Fine-tune the three Yrupe heads on real Sentinel-2 + real
   INBIO yield labels for 30+ epochs at batch size 32.
4. Compare transfer-trained Yrupe F1 against from-scratch Yrupe
   F1 on a held-out real-data test set with **temporal
   separation** (e.g., 2022 train / 2023 test).

Until steps 1-4 are completed, H3 is **untestable** on this
dataset.

## E.7 Caveats and known limitations

1. **No temporal separation in train / val / test split** — the
   pilot split per-month but did not hold out a contiguous
   growing season. A temporally separated split is the
   publication-quality standard for any yield-prediction paper.
2. **Synthetic labels may have data leakage** — the phenology
   profile is shared across scenes, so the random split may
   assign highly correlated pixels to train and test sets,
   inflating measured performance. (Note: the measured
   performance here is poor, so any leakage is in the
   conservative direction for the negative-result framing.)
3. **Single random seed** — only seed 42 was used. Bootstrapped
   CIs across multiple seeds would tighten the confidence
   intervals.
4. **No uncertainty quantification** — confidence intervals on
   the F1 / MAE / transfer ratio are not reported. With only one
   seed, the CIs are effectively unbounded.
5. **No held-out INBIO farm** — the pilot does not validate on
   any real farm. The synthetic-data transfer-to-real
   generalisation gap is therefore unmeasured.
6. **No comparison to a published yield-prediction baseline**
   such as the LSTM-of-NDVI used in P0035 (Chapter 4) or the
   random-forest baseline in P0010 (Chapter 2). The comparison
   would tighten the negative-result framing.

## E.8 Reproducibility checklist

The following are committed to the repository for reproducibility:

- [x] Synthetic dataset generation script
      (`src/utils/test_data.py`).
- [x] Multi-task CNN architecture code
      (`src/papers/p0025_yrupe_yield/pipeline.py`).
- [x] Training script with all hyperparameters hard-coded.
- [x] Evaluation script with all metrics implemented.
- [x] Random seed pinned (42).
- [x] `ACTUAL_RESULTS.md` — every number in this paper.
- [x] `requirements-ci.txt` — pinned dependency versions for CI.
- [ ] Trained model weights (synthetic-trained model is not
      worth preserving; the publication-quality model would be).
- [ ] Bootstrapped CIs across seeds (Section E.7 caveat 3).
- [ ] Real INBIO yield data — not available in this experiment
      cycle; required for the next iteration.

## E.9 Conclusion of the experiments section

The pilot experiment was sufficient to demonstrate that the
end-to-end pipeline (data loading → multi-task CNN → evaluation)
works as designed, but was **insufficient** to validate any of
the published headline claims. The honest framing for the paper
is therefore **methodology + failure-mode analysis**, as stated
in `discussion.md` Section D.4 and `conclusion.md`. Forward
claims require the GPU + real-data re-run described in Section
E.6.
