# Results

## R.1 Headline metric — the synthetic-to-real gap

The single most consequential finding of this paper is the
**synthetic-to-real mAP gap** for the YOLOv8-S detector:

| Evaluation set | mAP@0.5 |
|----------------|--------:|
| Synthetic validation (320 of 1,280 training images) | **0.50** |
| Real camera-trap test (5,000 Guyra Paraguay images) | **0.18** |
| **Synthetic-to-real gap** | **0.32 absolute** (0.50 → 0.18) |

The trained YOLOv8-S achieves mAP = 0.50 on its **own synthetic
validation set** and drops to **mAP = 0.18** on **real camera-trap
data**. The **0.32 absolute gap** is the synthetic-to-real
generalization deficit.

This gap is in the **middle of the published range** (15-40%
absolute decline, per [Beery et al. 2018; Bowers et al. 2021;
Milani et al. 2022]) and is consistent with the general literature
on synthetic-to-real gap in wildlife CV. It is **not** an unusual
result; it is the canonical failure mode.

## R.2 Per-species breakdown (real data)

| Species | Real mAP@0.5 | Synthetic mAP@0.5 | Gap (abs) |
|---------|------------:|-----------------:|----------:|
| Jaguar | 0.25 | 0.65 | -0.40 |
| Puma | 0.28 | 0.62 | -0.34 |
| Ocelot | 0.20 | 0.55 | -0.35 |
| Tapir | 0.22 | 0.60 | -0.38 |
| Deer | 0.30 | 0.62 | -0.32 |
| Capybara | 0.18 | 0.45 | -0.27 |
| Agouti | 0.12 | 0.50 | -0.38 |
| Armadillo | 0.10 | 0.55 | -0.45 |
| **Mean (8 large mammals)** | **0.21** | **0.57** | **-0.36** |

### R.2.1 Observations

1. **Puma (mAP 0.28) and deer (0.30)** are the best-performing
   species on real data. Both have large body sizes, distinctive
   morphology, and sufficient training examples.

2. **Agouti (mAP 0.12) and armadillo (0.10)** are the worst. Both
   are small-bodied, low-contrast against background, and have
   unusual body shapes that the synthetic training does not capture
   faithfully.

3. **Jaguar (mAP 0.25)** is intermediate; the absolute gap (0.40)
   is the largest of any species — the synthetic dataset produces
   jaguars with idealized body morphology that does not match the
   varied real camera-trap postures.

4. **The gap range** (0.27-0.45 absolute) is substantial across
   all species. The narrowest gap is for capybara (0.27), where
   the synthetic training happened to capture a useful prior.

### R.2.2 Reptiles and birds — not measured

The Guyra Paraguay public camera-trap dataset does **not include
reptiles or birds** with sufficient examples for per-species
breakdown. The synthetic dataset includes these classes (4
reptiles, 8 birds out of 24 species) but the lack of real
evaluation data means we cannot quantify the gap for those
classes.

Earlier drafts of this chapter reported per-class numbers for
reptiles (mAP = 0.05 real) and birds (mAP = 0.20 real). **These
numbers were estimated or extrapolated**, not measured. We have
removed them from the results table.

We can **expect** (by analogy to published literature) that:

- Reptiles would have the **highest synthetic-to-real gap** (small
  bodies, low contrast, atypical postures) — likely > 0.50
  absolute decline.
- Birds would have a **moderate gap** — likely 0.20-0.30 absolute.

These are expectations, not measurements.

## R.3 Per-fold cross-validation variance

Across the 5 folds on the real data:

| Fold | mAP@0.5 |
|------|--------:|
| Fold 1 | 0.20 |
| Fold 2 | 0.15 |
| Fold 3 | 0.22 |
| Fold 4 | 0.18 |
| Fold 5 | 0.16 |
| **Mean** | **0.18** |
| **Standard deviation** | **0.04** |

The standard deviation of 0.04 across folds reflects the
**small-sample variance** on 5,000 images distributed across 5
folds of ~1,000 images each. The 95% confidence interval on the
mAP would be roughly ±0.04 — a relatively wide range, which makes
the gap itself more uncertain than the point estimate suggests.

## R.4 Cross-validation design

The 5-fold split is **location-aware** where possible: a single
camera location's images are kept in one fold to avoid data
leakage. This is a methodological improvement over the earlier
4-fold design (which had potential location leakage).

**Limitation**: the Guyra Paraguay public dataset metadata does
not always include per-image camera-location tags. For images
without location tags, the leak-avoidance strategy is
**permutation-random within the unlabeled subset**, which may
still leak across some location pairs.

## R.5 What the synthetic-vs-real gap does and does not show

### R.5.1 What it shows

The 0.32 absolute mAP gap shows:

- Synthetic data alone is **not sufficient** for operational
  wildlife detection in the Gran Chaco.
- The gap is **larger than typical published estimates** for
  general-purpose object detection but **within the published range**
  for wildlife CV specifically. The biome-specific challenges
  (cryptic backgrounds, varied postures, occlusions) contribute.
- **Large-mammal detection** (mAP 0.21 mean on real) is the most
  reliable operational signal. Reptile and bird detection would
  likely be below operational thresholds even at higher
  synthetic-data fidelity.

### R.5.2 What it does not show

- The gap does **not** show that synthetic data is useless for
  wildlife CV. A 50/50 mix of synthetic + real training data is
  the standard recipe for closing the gap; this paper does not
  test that mix.
- The gap does **not** extrapolate to the 50K-image real dataset
  recommended for operational deployment. The mAP would likely
  be substantially higher with 10× more real labeled images; this
  paper uses only 5,000.
- The gap does **not** show that the model architecture is wrong.
  YOLOv8-S is a standard architecture and works well on real
  data when trained on real data.

## R.6 Summary table of measured vs. aspirational numbers

| Claim | Status | Source |
|-------|--------|--------|
| mAP = 0.50 on synthetic | ✅ measured | YOLOv8-S fine-tune on synthetic validation |
| mAP = 0.18 on real | ✅ measured | 5-fold CV on 5,000 Guyra images |
| Synthetic-to-real gap = 0.32 absolute | ✅ measured | Within published 0.15-0.40 range |
| Large-mammal mAP > 0.50 | ❌ **aspirational** | Earlier-draft number was for in-distribution synthetic; real mAP is 0.21 |
| mAP > 0.70 operational deployment | ❌ **aspirational** | Not at this point; mAP 0.18 is below operational threshold |
| Reptile mAP = 0.05 (real) | ❌ **estimated, not measured** | No reptile examples in Guyra public dataset |
| Bird mAP = 0.20 (real) | ❌ **estimated, not measured** | No bird examples in Guyra public dataset |
| Cascaded detector (binary + species fine-tune) | ❌ **aspirational** | Cascade design proposed but not implemented |
| WWF / Guyra deployment | ❌ **aspirational** | No partnership letter on file; no deployment |

The "aspirational" rows correspond to work that requires:

1. Per-species real labeled data expansion from 5K to ~50K images
   (resource: ~$5K of camera-trap data collection + labeling
   labor, or ~$10K of CrowdAI labeling).
2. Implementation of the cascaded detector design (a few days of
   engineering).
3. Partnership letter from WWF Paraguay and/or Guyra Paraguay
   (human-only, 3-6 months).

Until then, the paper should be published **as a reproducible
synthetic-to-real gap measurement**, not as an operational
deployment.

## R.7 What the resource-budgeting implication is

Given the 0.32 absolute gap and the per-species per-fold
variance:

- To close the gap from mAP 0.18 to mAP 0.50 for **large
  mammals** alone, the standard recommendation is roughly 10× the
  training data size — i.e., **50,000 labeled real images**.
  Realistic data-collection timeline: 1-3 years of camera-trap
  deployment in the park, plus labeling effort.
- To close the gap for **reptiles and birds** would require a
  larger real dataset (perhaps 100K-200K images) plus a
  species-specialist detector in cascade. This is a multi-year
  research program rather than a single project.

The contribution of this paper is the **measurement of where the
gap is**, which informs the budget decision. Without this
measurement, the budget would be a guess.
