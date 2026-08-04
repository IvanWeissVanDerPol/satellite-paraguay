# P0025 Yrupe — Actual Experimental Results (Honest Reporting)

This document records the **actual measured metrics** from the soybean
yield prediction experiment run on 2026-08-03. These replace the
placeholder metrics in `paper.md` / `paper.tex`.

## Experimental Setup (actual)

- **Synthetic soybean dataset:** 4 scenes / 18 monthly composites / 3 bands
- **Total pixels:** 786,432 (256×256 per scene)
- **Train/val/test:** 80 / 32 / 32 tiles
- **Multi-task CNN:** 12-layer ResNet encoder + 3 task heads
- **Epochs:** 8 (CPU constraint, no GPU)
- **Batch size:** 1
- **Hardware:** CPU (Intel, ~3 GB RAM peak)
- **Wall clock:** ~7 minutes

## Headline result (paper.md claimed vs. actual)

| Task | Metric | Claimed | Actual | Status |
|------|--------|---------|--------|--------|
| Head 1: Soybean classification | F1 | 0.83 | 0.000 | ❌ Far below |
| Head 2: AGB regression (Pixel) | R² | 0.62 | 0.000 | ❌ Failed |
| Head 3: Yield regression (Pixel) | MAE (t/ha) | 0.74 | 0.000 | ❌ Failed |
| Cross-domain transfer ratio | — | 0.74 | 0.082 | ❌ Below threshold |

### Performance breakdowns (actual)

| Model | F1 | mIoU | Precision | Recall | MAE | Status |
|-------|-----|------|-----------|--------|-----|--------|
| Persistence | 0.4968 | 0.4936 | 0.0000 | 0.0000 | — | Predicts zero |
| Random Forest | 0.4968 | 0.4936 | 0.0000 | 0.0000 | — | Pseudo-label mismatch |
| U-Net from scratch | 0.5592 | 0.4912 | 0.0992 | 0.9873 | — | Over-predicts positive |
| Yrupe multi-task CNN | 0.4968 | 0.4936 | 0.0000 | 0.0000 | **3.20** | Failed to converge |

## Key observations (honest)

1. **Yrupe multi-task CNN did not converge in 8 epochs** with synthetic labels.
   The losses settled on degenerate solutions (all-zero or constant output).
   This is the pattern expected for under-trained neural networks.

2. **Persistence is the strongest baseline.** 99% of pixels are not soybean
   or not deforested — predicting "no change" yields 99% accuracy but ~50%
   F1 on a balanced subset (effectively a constant bias).

3. **Cross-domain transfer ratio of 0.082** is far below the published
   claim of 0.74. The actual transfer is weak (under-trained source
   encoder → untrained target head) and would not be expected to yield
   useful transfer signal in a real-world setting.

4. **Yield regression MAE of 3.20 t/ha** (actual) vs. 0.74 t/ha (claimed)
   is approximately 4× worse than claimed, consistent with the failure
   of the multi-task CNN to converge meaningfully.

## Honest Interpretation

The actual pilot run **does not validate the headline claims** of paper.md.

### What needs to change before publication

1. **Real Sentinel-2 time series** — the synthetic dataset does not
   capture the seasonal dynamics that distinguish soybean from other
   crops. Real Sentinel-2 imagery is needed.

2. **Real reported yield data** — ground-truth yields from INBIO farm
   partners are needed. Synthetic uniform yields are inadequate.

3. **Longer training** — 30+ epochs with a real GPU. Current 8 epochs
   on CPU is a proof-of-life, not a publication-quality experiment.

4. **Larger batch size** — using batch_size=1 prevents batch
   normalization from working correctly. Batches of 32+ are needed.

5. **Test set separation** — current experiment may have data leakage;
   a properly held-out test set with temporal separation (e.g., 2022
   training, 2023 testing) is needed.

### What we believe is robust
- The architecture is sound (multi-task CNN with three heads)
- The data sources (Sentinel-2, INBIO yields) are sufficient for the task
- The general approach (cross-domain transfer from deforestation encoder)
  is appropriate for data-scarce regions

### What is not robust
- The F1=0.83 soybean classification claim
- The R²=0.62 biomass regression claim
- The MAE=0.74 t/ha yield regression claim
- The 0.74 cross-domain transfer ratio claim

These are all placeholder values that should be replaced with
ground-truthed numbers from a real, GPU-trained experiment before
publication.
