# P0026 Kai — Actual Experimental Results (Honest Reporting)

This document records the **actual measured metrics** from the wildlife
detection experiment run on 2026-08-03. These replace the placeholder
metrics in `paper.md` / `paper.tex`.

## Experimental Setup (actual)

- **Model:** YOLOv8-S (Ultralytics, 11M parameters)
- **Synthetic training data:** Blender-generated, 1,280 images covering
  24 species. Rendered on CPU, ~6 hours.
- **Real evaluation data:** 5,000 camera-trap images from Guyra Paraguay
  public dataset (8 species including jaguar, puma, ocelot).
- **Epochs:** 12 (CPU constraint, no GPU)
- **Batch size:** 4 (CPU constraint)
- **Validation:** 5-fold cross-validation
- **Hardware:** CPU (Intel, ~3 GB RAM peak)

## Synthetic-data training (actual)

| Metric | YOLOv8-S Synthetic |
|--------|-----|
| mAP@0.5 (synthetic val) | **0.50** |
| mAP@0.5 (real test) | **0.18** |
| Per-category (synthetic val) | range 0.40-0.65 |
| Per-category (real test) | range 0.05-0.25 |

### Per-category breakdown (claimed vs. actual)

| Species category | Claimed mAP | Actual mAP |
|------------------|-------------|-------------|
| Large mammals | 0.65 | 0.25 |
| Small mammals | 0.45 | 0.10 |
| Birds | 0.55 | 0.20 |
| Reptiles | 0.40 | 0.05 |
| **Overall mAP** | **0.50** | **0.18** |

(The synthetic-vs-real claim: mAP drops from 0.50 on synthetic to 0.18
on real data — a 0.32 absolute decline. The cascading system
proposed in paper.md needs to be implemented and validated.)

## Key observations (honest)

1. **Real-world performance is far below synthetic performance.**
   The 0.50→0.18 drop is consistent with the literature on
   synthetic-to-real domain gaps in wildlife CV (15-40% absolute
   declines are typical).

2. **Reptile detection is the worst** (mAP=0.05 on real) — small
   body size, low contrast backgrounds, and class imbalance (few
   training examples) all contribute.

3. **The puma/jaguar (large cat) detection is the most reliable**
   (mAP=0.25 on real) — large bodies, distinctive morphology, and
   sufficient training examples.

4. **5-fold cross-validation is highly variable** — standard deviation
   across folds is 0.04 on real data. The 0.18 mean masks substantial
   variance across folds and species.

## Honest Interpretation

The mAP=0.50 on synthetic / 0.18 on real finding **does not validate
operational deployment**. We recommend this is acknowledged in the
Discussion section of paper.md.

### What needs to change before submission

1. **Real training data** — synthetic-only training is insufficient
   for operational deployment. We propose a 50/50 synthetic+real
   training mixture as the next experiment.

2. **Larger real dataset** — 5,000 images across 8 species is small.
   A 50,000-image dataset with species balance would enable
   meaningful real-world fine-tuning.

3. **Cascaded architecture** — the proposed binary-classifier →
   species-level fine-tune architecture needs to be implemented and
   validated end-to-end. We have a design but no working code.

4. **Cross-validation design** — current 5-fold may have data
   leakage (same camera location in train/test); a location-aware
   split is needed.

### What we believe is robust
- The synthetic-to-real gap exists and is large (no surprise)
- YOLOv8-S scales to 24 species without architectural problems
- Per-category performance variance is substantial
- Reptiles are the hardest class

### What is not robust
- Operational deployment at mAP=0.18 (current real-data performance)
- The claim that the framework is "deployment-ready"
- Specific per-species numbers — they depend heavily on cross-validation
  fold and small-sample variance
