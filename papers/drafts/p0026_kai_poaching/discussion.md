# Discussion

## D.1 The 0.32 gap as a resource-budgeting signal

The 0.32 absolute mAP@0.5 synthetic-to-real gap is the headline
finding. It is **not** surprising — synthetic-to-real gaps in
wildlife CV are documented at 15-40% absolute decline in the
literature [Beery et al. 2018; Bowers et al. 2021; Milani et al.
2022], and 0.32 is in the middle of that range. What is **useful**
about this paper is that the gap is **measured in this specific
biome + detector configuration**, with per-species breakdown and
per-fold variance reported.

The contribution to **resource-budgeting** is concrete:

- **Large-mammal mAP = 0.21 (real)** — below operational thresholds
  (typically mAP ≥ 0.50 for a usable deployment).
- **Gap is consistent across species** (0.27-0.45 absolute), so
  simply training on more synthetic data would not close it.
- **Closing the gap to operational** requires **10× more real
  labeled data** (50K images) plus a 50/50 synthetic-real mix
  during training.

This is the **decision-relevant measurement** that conservation
funders need. Without the gap measurement, the budget decision
(how much to spend on real-label vs. synthetic-vs-cascade
alternatives) is opaque.

## D.2 What the gap does NOT show

We deliberately resist over-interpretation:

- **It does not show synthetic data is useless.** The 0.32 gap
  is the **synthetic-only training** gap. A 50/50 mix is the
  standard recipe and would close most of it.
- **It does not show the architecture is broken.** YOLOv8-S is a
  standard detector; the issue is the **training data**, not the
  model.
- **It does not establish operational deployment.** mAP 0.18 is
  below operational thresholds. The paper is a baseline
  measurement, not a deployment.
- **It does not extrapolate to other biomes.** The Gran Chaco is a
  specific environment; the gap may be different in savanna or
  tropical wet forest.

## D.3 The cascading-architecture alternative (proposed in earlier
drafts)

Earlier drafts of this chapter proposed a **cascaded detector**
design:

1. **Stage 1**: a binary-class classifier ("animal" vs.
   "no-animal") trained on a larger synthetic dataset.
2. **Stage 2**: a species-level fine-tuned classifier that takes
   Stage-1 positive crops.
3. **Stage 3**: a temporal-context module that aggregates per-image
   detections into time-series abundance.

This is a **reasonable design** but **not implemented** in this
paper. The 0.18 mAP from the single-stage baseline is the
**empirical baseline against which the cascade should be compared**.
If a future implementation of the cascade achieves mAP 0.40+, it
would represent a meaningful improvement over the single-stage
baseline.

The cascade adds engineering complexity (3 model versions to
train and version), inference latency (3 sequential model
evaluations per image), and integration complexity (per-stage
failure modes). It is **not** clearly a win without measurements.

## D.4 The missing ethics dimension

The Guyra Paraguay public dataset has an unspecified license for
**commercial use**; we use it for academic research only,
attributed to Guyra in our outputs. The original draft of this
chapter claimed deployment with WWF/Guyra Paraguay "real-time
alerts to park rangers" — this is **aspirational, not measured**.
No partnership letter is on file.

A conservation deployment in Defensores del Chaco would also
require:

1. **Partnership with WWF Paraguay and/or Guyra Paraguay** for
   field validation and ranger workflow integration.
2. **Park-ranger workflow design** — the mAP is just one
   metric; a useful deployment requires thinking about false-
   positive rates on the ranger side (a daily alert of 100 false
   positives is useless; a weekly alert of 5 true positives is
   useful).
3. **Data-sovereignty considerations** for image data that
   potentially reveals park-ranger patterns.

These are all **human-relationship work** that cannot be
automated. The operational deployment in earlier drafts of this
chapter was a **paper aspiration**, not a measured plan.

## D.5 What needs to happen for Conservation Biology submission

The paper is publishable now as a **reproducible synthetic-to-real
gap measurement**. The path to publishing it as a **cascade
architecture paper** (the standard publication for wildlife-CV
contributions) requires the cascade to be implemented and
measured. Concrete next steps:

### D.5.1 Implementation roadmap

1. **(Tier 2, ~2-4 weeks engineering)** Implement the cascaded
   detector design (3-stage: binary → species fine-tune →
   temporal aggregation). Use YOLOv8-S for Stage 1, a fine-tuned
   species classifier for Stage 2, and a simple count-based
   aggregator for Stage 3.

2. **(Tier 2, 2-3 months data collection)** Train the cascade
   Stage 2 on 50K real labeled images (10× the current dataset).
   Estimated cost: $5K-10K of camera deployment + labeling.

3. **(Tier 2, $50 GPU)** Train the cascade on GPU rather than CPU.
   Same architecture, real-data training, batch=32, 30 epochs.

4. **(Tier 4, 3-6 months)** Partnership letters from WWF
   Paraguay + Guyra Paraguay + Defensores del Chaco park
   administration.

5. **(Tier 4) Conservation Biology editor email.** Submit as a
   methodology + measurement paper initially; cascade work is a
   future submission.

### D.5.2 Estimated total cost and timeline

- **Engineering**: 2-4 weeks, ~$0 cost.
- **Data collection**: 2-3 months, $5K-10K.
- **GPU**: $50.
- **Partnership**: 3-6 months human-only.
- **Total**: 6-12 months to a follow-on paper, ~$10K cost.

This is a **multi-year research program**, not a single-project
follow-on. Realistic deployment in Defensores del Chaco is
2-3 years out.

## D.6 The honest-reporting posture

We surface the gap honestly because:

- The literature has documented synthetic-to-real gaps of similar
  magnitude; the contribution is the biome-specific measurement.
- Claiming a smaller gap (e.g., "synthetic data closes 80% of the
  real-data gap") would require per-experiment evidence we do
  not have.
- The 50K-image recommendation is a target for the next round of
  data collection, not a claim about what the current system
  achieves.

This is the second paper in the thesis substrate to explicitly
report a measured result that contradicts the headline target.
The publication recommendation is the same: lead with the
**measurement**, acknowledge the **gap**, propose the
**resource-budget**, and let the journal reviewer assess.

## D.7 Limitations

The paper has the following limitations, in addition to the
synthetic-to-real gap itself:

- **Sample size 5,000 images across 8 species.** Statistical
  power is limited; standard deviation across folds is 0.04.
- **No reptile / bird real-data evaluation.** The Guyra public
  dataset does not cover these classes.
- **Synthetic-data quality** is operator-dependent. A more
  photorealistic synthetic dataset (e.g., using physics-based
  rendering) might produce a smaller gap; the cost would be
  higher but achievable.
- **No permutation-based cross-validation** for the location-aware
  split. The location-aware split is best-effort, not
  statistically principled.
- **No comparison to a real-data-only baseline** (training
  YOLOv8-S on real from scratch). This would establish a
  per-species upper bound on achievable mAP. The paper uses
  only the synthetic-trained model.
- **Per-image-uncertainty quantification** is absent; mAP
  averages over confidence thresholds.

These limitations are addressed by the resource-budget
recommendation in Section D.5.
