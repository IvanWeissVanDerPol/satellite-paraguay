# P0025 Yrupe: Cross-Domain Transfer for Soybean Yield Prediction

> **Snapshot generated 2026-09-08.** The LaTeX chapter at
> [`chapters/p0025_yrupe_ch06.tex`](chapters/p0025_yrupe_ch06.tex) is the
> canonical source for the thesis PDF build. This file is a
> human-readable summary that mirrors the LaTeX chapter's measured
> numbers and structure.

- **Journal target:** Agricultural Systems
- **LaTeX chapter (canonical):** `thesis/chapters/p0025_yrupe_ch06.tex` (1,243 words)
- **Paper source-of-truth:** `papers/drafts/p0025_yrupe_yield/paper.tex`
- **Measured pilot:** `papers/drafts/p0025_yrupe_yield/ACTUAL_RESULTS.md`

## Summary (mirrors chapter §1–§5)

This chapter summarises Paper P0025, the cross-domain transfer experiment that tests whether a deforestation-trained encoder can be reused for soybean yield prediction. Yrupe is presented as a falsification study: the measured cross-domain transfer ratio is far below the conventional threshold, so H3 is reported as a negative result rather than an aspirational claim.

**Measured pilot numbers (synthetic Sentinel-2 + synthetic yields, 8 CPU epochs):**

| Quantity | Measured value | Target | Status |
|---|---|---|---|
| Cross-domain transfer ratio | **undefined (CNN did not converge)** | > 0.7 | ❌ **H3 falsified** |
| Yield regression MAE | **3.20 t/ha** | < 5 t/ha | ✅ (within target) |
| Test-set separation | Not held-out (data leakage risk) | Required | ⚠ acknowledged |
| Hardware | CPU, 8 epochs, batch=1 | GPU, 30+ epochs, batch=32 | ⚠ acknowledged |

**Country-scale finding:** The cross-domain generalization hypothesis (H3) is **falsified** in the current pilot configuration: the measured transfer ratio ≈ 0.0 (CNN did not converge; no model output to compute transfer from) is far below the conventional 0.7× threshold. The Yrupe architecture is sound, but the cross-domain transfer claim does not survive measurement.

**Aspirational-vs-measured gap:** Earlier-draft headline numbers (F1=0.83 classification; R²=0.62 biomass regression; MAE=0.74 t/ha yield regression) were placeholders, not measurements, and have been removed. Real Sentinel-2 + INBIO ground-truth yield runs are the next step — blocked on GPU budget + INBIO partnership.

**Keywords:** cross-domain transfer, soybean yield, foundation models, falsification, Paraguay, INBIO

**Author:** Iván Weiss Van der Pol (FP-UNA)

**Status:** Chapter of the thesis (in journal-preparation; Agricultural Systems submission pending INBIO partnership + GPU run).
