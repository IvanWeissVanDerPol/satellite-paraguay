# P0011 Yvutu — Statistical Analysis (Pilot Run)

**Date:** 2026-08-03
**Bootstrap samples:** 10,000
**Confidence level:** 95%

## Honest reporting

This pilot experiment was run on **synthetic data** with **5 epochs**.
Real-data results are expected to differ significantly.
Yvutu's lightweight fallback (Prithvi not available in this environment)
performed essentially identically to the persistence baseline.

## Per-model metrics with 95% bootstrap CIs

| Model | Precision (mean [95% CI]) | Recall (mean [95% CI]) | F1 (mean [95% CI]) |
|-------|---------------------------|------------------------|--------------------|
| persistence | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| random_forest | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| unet | 0.0992 [0.0954, 0.1028] | 0.9873 [0.9826, 0.9913] | 0.1803 [0.1739, 0.1863] |
| yvutu | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |

## Confusion matrices

### persistence

| | Predicted + | Predicted - |
|---|---|---|
| Actual + | 0 | 2,522 |
| Actual - | 0 | 194,086 |

### random_forest

| | Predicted + | Predicted - |
|---|---|---|
| Actual + | 0 | 2,522 |
| Actual - | 0 | 194,086 |

### unet

| | Predicted + | Predicted - |
|---|---|---|
| Actual + | 2,490 | 32 |
| Actual - | 22,605 | 171,481 |

### yvutu

| | Predicted + | Predicted - |
|---|---|---|
| Actual + | 0 | 2,522 |
| Actual - | 0 | 194,086 |


## What this means

1. **U-Net overpredicts** deforestation (precision = 0.099, recall = 0.987).
   It predicts 24,632 pixels as deforested when only 2,522 are actually.
2. **Persistence, Random Forest, and Yvutu** all predict zero deforestation.
   They achieve 99% accuracy by predicting the majority class.
3. **F1 ~0.50** is the result of predicting the majority class correctly.
4. **The pilot experiment demonstrates pipeline correctness**, not model quality.
5. **Real data + real training** (Prithvi fine-tune on 50 Chaco tiles for 30 epochs)
   is expected to yield higher F1, but **this has not been measured**. The F1 = 0.85-0.90
   figure quoted in earlier versions of this report is a Prithvi literature benchmark,
   not a Yvutu measurement, and is preserved here only as an aspirational target.
   See `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md` for measured values.
