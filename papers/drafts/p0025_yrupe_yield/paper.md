# Chapter 6: Yrupe — Cross-Domain Transfer Learning for Soybean Yield Prediction in Paraguay

**Author:** Iván Weiss Van der Pol
**Status:** Chapter of the thesis (in journal-preparation as honest failure-mode analysis)
**Target journal:** Agricultural Systems (IF 8.3)

---

## Abstract

We present **Yrupe** (Guaraní for "puddle"), a multi-task
convolutional neural network for soybean yield prediction in
the Eastern Paraguay Pampas that combines multi-temporal
Sentinel-2 imagery with a Chave-2014-derived above-ground biomass
feature stack. The architecture tests the **cross-domain transfer
hypothesis**: that a satellite-based deforestation-detection
encoder (Yvutu, Chapter 3) can be fine-tuned for soybean yield
regression in a data-scarce agricultural application.

The pilot experiment was run on a **synthetic dataset** (4 scenes
× 18 monthly composites × 256×256 pixels) due to lack of real
INBIO yield labels at experiment time. The headline measured
results:

| Task | Target | Measured |
|------|-------:|----------:|
| Soybean-pixel classification F1 | 0.83 | **0.497** |
| AGB regression R² | 0.62 | **undefined** |
| Yield regression MAE (t/ha) | 0.74 | **3.20** (4.3× worse) |
| Cross-domain transfer ratio | 0.74 | **0.082** |

**The hypothesis was not validated.** The multi-task CNN did not
converge under the tested conditions (8 CPU epochs, batch=1,
synthetic labels). The cross-domain transfer ratio measured 0.082,
well below the typical weak-transfer threshold of 0.50.

We attribute the failure to **three specific causes** that are
diagnosable in the experiment log: (i) synthetic labels with no
seasonal dynamics; (ii) insufficient training (8 epochs is below
the standard 30+ recipe); (iii) the source encoder (Yvutu's
Prithvi-fine-tune) was not exercised — the test was from-scratch-
to-from-scratch, not pretrained-to-from-scratch as the hypothesis
requires.

This paper is published **as a reproducible failure-mode analysis**
and a methodology paper, **not** as a forward-claim yield predictor.
The path-forward to making the hypothesis testable is documented
in `discussion.md` Section D.3: real INBIO labels + GPU training
+ Yvutu encoder integration. Estimated cost: $50-150 GPU +
2-3 months partnership + 1 week integration.

> **Honest Reporting Note (added 2026-08-10):** The headline metrics
> in the abstract above (F1 = 0.83 / R² = 0.62 / MAE = 0.74 / transfer
> ratio = 0.74) are **aspirational**, not measured. The measured values
> are documented in `ACTUAL_RESULTS.md` and shown in the table above.
> Earlier drafts of this chapter cited the aspirational numbers as
> measured results; this version of the abstract explicitly surfaces
> the gap.

---

## Paper body

This paper is organized as a set of structured sections in
companion files. Read in order:

- **`introduction.md`** — cross-domain transfer hypothesis,
  Paraguay test case, the three predictions tested, the measured
  falsification of predictions P1-P3, 4 honest failure-mode
  contributions.
- **`methods.md`** — synthetic dataset, multi-task CNN architecture,
  cross-domain transfer protocol, evaluation metrics, the three
  failure causes enumerated.
- **`results.md`** — measured vs claimed table, per-model
  performance breakdown, transfer ratio analysis, summary of
  measured vs aspirational numbers.
- **`discussion.md`** — what the negative result means (and doesn't
  mean), three concrete changes to make the hypothesis testable,
  why publish a negative result.
- **`conclusion.md`** — main contributions, honest limitations,
  Agricultural Systems submission roadmap.
- **`related_work.md`** — deep learning for crop yield (Kamilaris,
  Yang, Peng, Huang), cross-domain transfer in remote sensing
  (Rußwurm, Kattenborn, Tseng), Paraguayan agriculture, the
  honest-reporting-of-negative-results convention.
- **`ACTUAL_RESULTS.md`** — the source of truth for every number
  in this paper.
- **`paper.tex`** — LaTeX elsarticle for Agricultural Systems.
- **`cover_letter.md`** + **`submission_checklist.md`** — for
  Agricultural Systems submission.

---

## Headline numbers (measured)

| Finding | Value | Source |
|---|---|---|
| Soybean-pixel classification F1 | **0.497** | Synthetic, 8 CPU epochs |
| AGB regression R² | **undefined** (constant prediction) | Synthetic |
| Yield regression MAE (t/ha) | **3.20** | Synthetic, Head 3 |
| Cross-domain transfer ratio | **0.082** | Yvutu source (not actually run) vs from-scratch |
| Training wall clock | 7 minutes | 8 epochs × 1 batch × 4 scenes |
| Synthetic dataset size | 4 scenes × 18 months | NDVI phenology profile |
| **F1 = 0.83 soybean classification** | **NOT MEASURED** | Aspirational target from earlier drafts |
| **R² = 0.62 AGB regression** | **NOT MEASURED** | Aspirational target |
| **MAE = 0.74 t/ha yield regression** | **NOT MEASURED** | Aspirational target; measured is 4.3× higher |

---

## Honest limitations

- **The headline metrics were not achieved.** F1 = 0.497 vs. 0.83
  target. R² undefined vs. 0.62 target. MAE 3.20 vs. 0.74 target.
  Transfer ratio 0.082 vs. 0.74 target.
- **The synthetic dataset is inadequate** for the cross-domain
  transfer hypothesis to be tested. Real INBIO yield labels
  + real Sentinel-2 imagery are required.
- **The source encoder (Yvutu's Prithvi fine-tune) was not
  exercised.** The "cross-domain" experiment tested from-scratch-
  to-from-scratch, which is not the hypothesis.
- **No field validation**, no temporal generalization test.
- **No operational deployment** with INBIO farmers.

---

## What this paper is and is not

This paper is:

- ✅ A reproducible failure-mode analysis with measured numbers.
- ✅ A methodology paper (synthetic cross-domain transfer pipeline).
- ✅ A documentation of what does and doesn't work, and why.

This paper is not:

- ❌ A forward-claim soybean yield predictor.
- ❌ A validation of the cross-domain transfer hypothesis.
- ❌ A claim of operational deployment with INBIO farmers.

The publication recommendation: **submit as a methodology +
failure-mode analysis paper**. Avoid framing as a forward-claim
paper; reviewers will catch the gap between measured 0.497 F1 and
aspirational 0.83 F1.
