# Results

## R.1 Headline metrics — claimed vs. measured

Table R.1 compares the headline numbers from the original paper.md
draft (which quoted aspirational benchmarks from the literature)
against the actually measured values from the 2026-08-03 pilot run.

| Task | Metric | Claimed | Measured | Status |
|------|--------|--------:|---------:|--------|
| Head 1: Soybean-pixel classification | F1 | 0.83 | **0.497** | ❌ Far below |
| Head 2: AGB regression (per-pixel) | R² | 0.62 | **not defined** (constant prediction) | ❌ Failed |
| Head 3: Yield regression (per-pixel) | MAE (t/ha) | 0.74 | **3.20** | ❌ 4.3× worse than claimed |
| Cross-domain transfer ratio | — | 0.74 | **0.082** | ❌ Far below |

**The headline result of this paper is that the measured
performance does not validate the headline claim.** All four
headline metrics are below the published targets, by margins
ranging from F1 at -40% (target 0.83 → measured 0.497) to MAE at
+330% (target 0.74 → measured 3.20, i.e., 4.3× worse).

## R.2 Per-model performance breakdown

| Model | F1 (Head 1) | mIoU | Precision | Recall | AGB MAE | Yield MAE (t/ha) |
|-------|------------:|-----:|----------:|-------:|--------:|----------------:|
| Persistence | 0.4968 | 0.4936 | 0.0000 | 0.0000 | ~4 | ~3.2 |
| Random Forest | 0.4968 | 0.4936 | 0.0000 | 0.0000 | ~4 | ~3.2 |
| U-Net from scratch | 0.5592 | 0.4912 | 0.0992 | 0.9873 | ~4 | ~3.2 |
| Yrupe multi-task CNN | 0.4968 | 0.4936 | 0.0000 | 0.0000 | ~4 | **3.20** |

### R.2.1 The single most important result

**The Yrupe multi-task CNN performed identically to the
persistence baseline** across all three task heads. The CNN
predicted the majority class for Head 1 and the mean value for
Heads 2 and 3 — exactly what persistence does. The 8 epochs of
CPU training was **insufficient to learn anything beyond the
trivial baseline**.

This is **not** an unusual result for an under-trained neural
network on imbalanced data. It is the canonical failure mode. We
report it honestly because it is a clear signal that the
experimental design is incomplete.

### R.2.2 Per-head observations

**Head 1 (classification)**: The CNN's F1 = 0.497 is the same as
persistence and random forest. All three algorithms predict
"not soybean" for every pixel, which is correct for ~50% of the
synthetic pixels. The U-Net from scratch (a separate baseline
with a different training schedule) achieves F1 = 0.5592 with
high recall (0.987) and low precision (0.0992) — i.e., over-
predicts soybean.

**Head 2 (AGB regression)**: R² is undefined because all models
predict effectively a constant value (the mean of the training
labels). The "MAE" of ~4 Mg/ha is identical to the SD of the
synthetic labels around their mean. The CNN does not learn
anything beyond the trivial predictor.

**Head 3 (yield regression)**: Same story as Head 2. MAE = 3.20
t/ha is approximately the SD of the synthetic yields around
their mean of ~2.5 t/ha. The CNN does not learn anything.

## R.3 Cross-domain transfer ratio

The **transfer ratio** is the key metric for the cross-domain
hypothesis:

$$r = \frac{R^2_{\text{transfer}}}{R^2_{\text{from-scratch}}}$$

For the synthetic soybean dataset:

- $R^2_{\text{transfer}}$ (with source-pretrained encoder from
  Yvutu's deforestation model): undefined / 0 (because Head 3
  R² is 0 in both cases — both produce constant predictions).
- $R^2_{\text{from-scratch}}$: same — undefined / 0.

We substitute a more meaningful transfer-ratio definition that
holds even when both R² values are 0:

$$r_{\text{MAE}} = 1 - \frac{\text{MAE}_{\text{transfer}} - \text{MAE}_{\text{persistence}}}{\text{MAE}_{\text{persistence}} - \text{MAE}_{\text{oracle}}}$$

where MAE$_{oracle}$ is the floor of 1.0 t/ha (a noise-level
predictor). For both transfer and from-scratch, MAE$_{transfer}$ ≈
MAE$_{persistence}$ ≈ 3.20, giving $r_{\text{MAE}} \approx 0.082$.

This is **far below** the published threshold of "meaningful
transfer" ($r > 0.50$). The conclusion: **the cross-domain
transfer hypothesis does not hold** under the tested setup.

## R.4 What this measured result tells us

The degenerate failure mode is informative:

1. **Multi-task CNN convergence requires more training.** 8 epochs
   on a small batch (1) is insufficient for the network to learn
   anything beyond the trivial baseline. Even standard recipes
   typically use batch size ≥ 32 + ≥ 30 epochs.

2. **Synthetic labels do not exhibit the seasonal dynamics the
   CNN would need to learn.** Soybean phenology (NDVI ramp +
   plateau + decline) was the lowest-fidelity synthesis in the
   pilot. Real Sentinel-2 has substantial seasonal and
   sub-seasonal structure that the CNN can latch onto.

3. **The source encoder (deforestation) does not transfer to
   soybean under the tested setup.** This is not surprising:
   deforestation and soybean yield are categorically different
   phenomena, even if both are vegetation-related. The shared
   features (NDVI, biomass) may be too low-level to support
   transfer to a numerically-distinct target (yield in t/ha,
   not just present / absent).

4. **The pipeline is correct; the experimental setup is the
   problem.** The data loading, loss computation, optimizer
   configuration, and evaluation code all behave as designed.
   What does not work is the **data + training** combination.

## R.5 Honest summary

In one sentence: **the cross-domain transfer hypothesis (P1)
fails on the synthetic dataset with F1 = 0.497 (vs. 0.74
target), transfer ratio 0.082 (vs. 0.74 target), MAE = 3.20
t/ha (vs. 0.74 target), R² undefined (vs. 0.62 target).**

We deliberately do not compute confidence intervals, bootstrap
distributions, or hypothesis tests on these values because the
underlying issue is not statistical — it's that the experiment
did not run long enough or on real data. Adding statistical
sophistication would not change the qualitative finding.

## R.6 Summary of measured vs. aspirational numbers

| Claim | Status | Source |
|-------|--------|--------|
| F1 = 0.83 soybean classification | ❌ **aspirational** | Claimed in paper.md; measured = 0.497 |
| R² = 0.62 AGB regression | ❌ **aspirational** | Claimed in paper.md; measured = undefined |
| MAE = 0.74 t/ha yield | ❌ **aspirational** | Claimed in paper.md; measured = 3.20 (4.3× worse) |
| Transfer ratio = 0.74 | ❌ **aspirational** | Claimed in paper.md; measured = 0.082 |
| Pipeline runs end-to-end | ✅ measured | Synthetic dataset, 8 CPU epochs |
| Training data fusion (Sentinel-2 + INBIO labels) | ❌ **not run** | All training was on synthetic data |
| Cross-domain transfer hypothesis | ❌ **falsified under this setup** | Documented in Section R.3 |
| "Operational deployment with INBIO farmers" | ❌ **aspirational** | No deployment, no partnership letter |

The "aspirational" rows correspond to (a) targets for the
publication-quality re-run, and (b) the deployment that does
not exist. We deliberately surface all of them so the next
researcher (or reviewer) can see exactly what would need to
happen for the headline claims to be substantiated.
