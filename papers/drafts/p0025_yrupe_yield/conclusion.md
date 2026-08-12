# Conclusion

We presented **Yrupe**, a multi-task CNN cross-domain transfer
learning pipeline that combines Sentinel-2 imagery, INBIO yield
labels, and a Chave-2014-derived AGB feature stack to predict
soybean yields in the Eastern Paraguay Pampas. The **measured
pilot result** on synthetic data is that the headline hypothesis
(P1: cross-domain transfer ratio ≥ 0.50) was **not validated**:
the measured transfer ratio was 0.082, the F1 was 0.497 (vs. the
0.83 target), the AGB R² was undefined, and the yield MAE was
3.20 t/ha (4.3× the 0.74 target).

## Main contributions

1. **Measured failure-mode analysis** documenting that the
   multi-task CNN did not converge under the synthetic + CPU + 8
   epoch conditions.

2. **Identification of three specific causes** of the failure
   (synthetic labels, insufficient training, missing source
   encoder) and a concrete path-forward (Section D.3 of
   `discussion.md`).

3. **Open-source pipeline + experiment log** so the community
   can build on this work without repeating the same negative
   result.

4. **An honest failure-mode framing** in the publication-ready
   paper as a worked example of the project's broader
   honest-reporting convention (see `docs/CONVENTIONS.md`).

## Honest limitations

- **The headline claim was falsified** under the tested setup;
  publication-quality forward predictive claims about soybean
  yields are not substantiated.
- **The synthetic dataset is inadequate** for non-trivial
  learning — 4 scenes × 18 monthly composites × 256×256 pixels
  is too small and too uniform to support transfer learning.
- **The source-pretrained encoder (Yvutu's Prithvi fine-tune)
  was not exercised** in the cross-domain test. The transfer
  ratio measured here is from-scratch-to-from-scratch, not
  from-pretrained-to-from-scratch.
- **No field validation**, no temporal split, no augmentation —
  standard requirements for any forward-claim paper.

## What needs to happen for Agricultural Systems submission

Per `docs/AGENT_TODO.md` and `docs/REAL_TODO.md`:

1. **(Tier 1, prerequisite) Yvutu (Chapter 3) GPU re-run.** The
   Yvutu encoder weights are the source for the cross-domain
   transfer. Until Yvutu has measured weights, Yrupe cannot
   test the genuine transfer hypothesis. ~$20 + 1 week.
2. **(Tier 2, 2-3 months) INBIO partnership.** Real yield labels
   from 500+ farms across 2+ growing seasons. The fundamental
   constraint.
3. **(Tier 2, $50-150 GPU) Real training.** A100, batch=32,
   30 epochs on the combined real dataset.
4. **(Tier 2, ~4 h) Per-paper `references.bib` slice** for
   `papers/drafts/p0025_yrupe_yield/` so `paper.tex` compiles
   standalone.

Step 1 is the prerequisite for any meaningful reproduction.
Steps 2-4 are the publication-quality re-run. Without steps 1-4
the paper is publishable only as a methodology + failure-mode
analysis paper, **not** as a forward-claim paper.

The honest publication recommendation: **submit this paper as a
synthetic-dataset cross-domain transfer **methodology** paper,
not as a forward-claim paper.** Reviewers in Agricultural Systems
will be skeptical of "we report F1 = 0.83" submissions without
showing the experiments; the methodology + failure-mode framing
is publishable. The forward-claim paper is the GPU re-run.

## Data + code availability

- **Code**: open-source under CC-BY-NC-4.0 (`LICENSE`).
- **Synthetic dataset**: generated reproducibly from
  `set_seed(42) + NDVI phenology profile` in
  `src/utils/test_data.py`.
- **Pipeline**: `src/papers/p0025_yrupe_yield/pipeline.py`
  (YrupePipeline class with predict_yield, load_inbio_data,
  delineate_fields). **Fail-loud since 2026-08-11**: the
  pipeline raises `FileNotFoundError` when real Sentinel-2 +
  INBIO NDVI data is missing rather than silently faking it
  with random numbers (see `BRUTAL_ROAST.md`).
- **Experiment log**: `ACTUAL_RESULTS.md` — every number in this
  paper.
- **Paper sources**: `paper.md` (Markdown), `paper.tex`
  (LaTeX elsarticle for Agricultural Systems).
