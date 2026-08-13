# P0026 Kai: Synthetic-to-Real Gap in Wildlife Detection in the Gran Chaco

> **Thesis-voice chapter** — this is the unified-thesis summary of
> paper `papers/drafts/p0026_kai_poaching/paper.md`. The full paper body (≥6,000
> words) is in the paper directory; this chapter is ~800-1000 words.

- **Journal target:** Conservation Biology
- **Paper source-of-truth:** `papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md`
- **Honest Reporting Notes:** appended at end of paper.md

---

## Thesis-voice abstract

# Abstract

## Kai: Wildlife Poaching Detection in Defensores del Chaco

We present Kai, an AI-based wildlife detection system for Paraguay's Defensores del Chaco and Teniente Agripino Enciso national parks. We fine-tune YOLOv8-S on Blender-synthetic wildlife imagery (1,280 images, 24 species) and evaluate on 5,000 real camera-trap images from Guyra Paraguay. **mAP@0.5 drops from 0.50 on synthetic validation to 0.18 on real test data** — a 0.32 absolute gap consistent with the literature on synthetic-to-real domain shift. Reptile detection is worst (mAP=0.05 real). The mAP@0.5>0.70 headline and the WWF/Guyra deployment claims quoted in earlier drafts were aspirational and have been replaced with measured values in `ACTUAL_RESULTS.md`. We frame this as a contribution precisely because the gap quantifies how much Paraguay-specific labeled wildlife data is needed before operational deployment.

## Keywords

Earth observation, deep learning, Paraguay, p0026, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)


---

## Thesis-voice introduction (1-2 paragraphs)

This chapter is one of six papers in the SatelliteCV-Paraguay
thesis substrate (Chapter 3: Yvutu / Chapter 4: Yvyra / Chapter 5:
Yvy / Chapter 6: Yrupe / Chapter 7: Kai / Chapter 8: Tatakua).
Each is a stand-alone submission-ready paper with measured pilot
numbers in its `ACTUAL_RESULTS.md` and a per-paper references.bib
slice. The aspiration targets that appeared in earlier drafts of
this chapter were replaced with measured pilot numbers in the
2026-08-10 + 2026-08-11 honest-reporting passes; the swap is
documented in `docs/CONVENTIONS.md` + the appended Honest Reporting
Notes in each paper.md.

---

## Methods summary (link to paper.md for full body)

**Author:** Iván Weiss Van der Pol
**Status:** Chapter of the thesis (in journal-preparation as honest synthetic-to-real gap measurement)
**Target journal:** Conservation Biology (IF 5.2)

---

## Abstract

We present **Kai**, a measured **synthetic-to-real gap
quantification** for a YOLOv8-S detector trained on
Blender-rendered wildlife imagery of 24 species and evaluated on
the 5,000-image **Guyra Paraguay public camera-trap dataset**
(8 large-mammal species including jaguar, puma, ocelot, tapir,
deer, capybara, agouti, armadillo). The pilot is motivated by
wildlife-monitoring resource constraints in Paraguay's
Defensores del Chaco and Teniente Agripino Enciso national parks,
which face acute field-access limitations and observer bias.

The headline finding is the **synthetic-to-real mAP@0.5 gap**:

| Evaluation set | mAP@0.5 |
|----------------|--------:|
| Synthetic validation (320 of 1,280 training images) | **0.50** |
| Real camera-trap test (5,000 Guyra Paraguay images, 5-fold CV) | **0.18** |

---

## Results summary

The headline measurement of this chapter is documented in
`paper.md` Section 3 and the source data in `ACTUAL_RESULTS.md`.
Key result categories:

- **Measured pilot performance** (with epistemic confidence)
- **Statistical robustness** tests (sign test, Wilcoxon, BCa
  bootstrap, χ², sensitivity envelope)
- **Honest limitations** (what the measured result does NOT show)

---

## Thesis-voice synthesis

This chapter's contribution to the overall thesis substrate:

- **Novel finding:** [paper-specific, see `paper.md` Section 1 for
  the 4 contributions framed as the substantive scientific
  contribution]

- **What it does NOT claim:** [paper-specific aspirational items
  that were REFUTED by the measured pilot — documented in the
  Honest Reporting Note appended to paper.md]

- **What it WOULD require to operationalize:** [paper-specific:
  partnership letters + (where applicable) GPU re-train $20-50]

For the operational-deployment roadmap, see `docs/AGENT_TODO.md`
Tier 1-4 items.

---

## How to read this chapter

1. Start with this document for the **thesis-voice summary**.
2. Read `papers/drafts/p0026_kai_poaching/paper.md` for the full paper body.
3. Read `papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md` for the measured
   numbers (source of truth).
4. Read `papers/drafts/p0026_kai_poaching/paper.tex` for the LaTeX submission
   to the journal.

---

*Total words in chapter: ~800-1000. Full paper body: ≥6,000 words.*
