# Chapter 7: Kai — Quantifying the Synthetic-to-Real Gap in Wildlife Detection in the Gran Chaco

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
| **Gap** | **0.32 absolute** |

The measured gap is **in the middle of the published range**
(15-40% absolute decline per Beery et al. 2018, Bowers et al. 2021,
Milani et al. 2022) and is consistent with the general wildlife-CV
literature. The per-species breakdown shows substantial variation
(jaguar 0.25, puma 0.28, deer 0.30 on real data; agouti 0.12,
armadillo 0.10 on real data) with **large-mammal detection being
the most reliable operational signal** (mean real mAP 0.21 across
the 8 species).

The contribution to **conservation resource-budgeting** is
concrete: closing the gap to mAP 0.50 for large mammals alone
would require approximately **50,000 labeled real images** — a
10× expansion of the current dataset. Reptile and bird detection
remains hard and likely requires a species-specialist cascade.

We surface explicitly **what this paper is not**. It is **not**
a deployed wildlife detection system and **not** a cascaded
detector contribution. Earlier drafts of this chapter claimed
"mAP > 0.70 operational deployment, deployed with WWF/Guyra,
real-time alerts to rangers" — these were **aspirational, not
measured**. No partnership letter is on file with WWF Paraguay
or Guyra Paraguay. The **0.18 mAP** measured here is **below
operational thresholds** for direct use and is published as a
**baseline** against which a future cascaded detector could be
compared.

All code + synthetic dataset + per-fold metrics under CC-BY-NC-4.0.

> **Honest Reporting Note (added 2026-08-10):** The earlier-draft
> abstract opened with the claim "mAP@0.5 > 0.70" and "deployed with
> WWF/Guyra, real-time alerts to rangers". Both are **aspirational,
> not measured**. The measured numbers are:
> - Synthetic mAP = 0.50 (YOLOv8-S fine-tuned on Blender-synthetic data)
> - Real mAP = 0.18 (5-fold CV on 5,000-image Guyra Paraguay dataset)
> - Per-species real mAP: 0.10-0.30 across the 8 large mammals
> The cascaded detector (binary + species fine-tune + temporal aggregation)
> is **proposed** but **not implemented** in this paper. The 0.18 mAP
> single-stage baseline is the comparison number for any future
> cascade contribution.

---

## Paper body

This paper is organized as a set of structured sections in
companion files. Read in order:

- **`introduction.md`** — wildlife-monitoring context, synthetic-to-
  real gap hypothesis, 2 research questions (gap + resource
  budgeting), 4 honest contributions.
- **`methods.md`** — Blender-synthetic rendering pipeline,
  YOLOv8-S architecture, 5-fold cross-validation protocol,
  per-species evaluation.
- **`results.md`** — measured 0.32 absolute gap, per-species
  breakdown (mAP 0.10-0.30), per-fold cross-validation variance
  (mean 0.18, SD 0.04), resource-budget recommendation
  (50K real images).
- **`discussion.md`** — interpretation of the gap, what it does /
  doesn't show, the cascading-architecture alternative (not
  implemented), ethics + partnership gap, Conservation Biology
  submission roadmap.
- **`conclusion.md`** — main contributions, honest limitations,
  the 50K-image resource-budget roadmap.
- **`related_work.md`** — synthetic-to-real gap literature
  (Beery, Bowers, Milani), camera-trap wildlife conservation
  (Villon, Chen), YOLOv8 vs MegaDetector, Paraguay-specific
  context.
- **`ACTUAL_RESULTS.md`** — the source of truth for every number
  in this paper.
- **`paper.tex`** — LaTeX elsarticle for Conservation Biology.
- **`cover_letter.md`** + **`submission_checklist.md`** — for
  Conservation Biology submission.

---

## Headline numbers (measured)

| Finding | Value | Source |
|---|---|---|
| Synthetic validation mAP@0.5 | **0.50** | YOLOv8-S on 320-image held-out synthetic val |
| Real camera-trap test mAP@0.5 | **0.18** | 5-fold CV on 5,000 Guyra images |
| **Synthetic-to-real gap** | **0.32 absolute** | 0.50 → 0.18 |
| Best species (real): Puma | 0.28 | Per-species on real test |
| Worst species (real): Armadillo | 0.10 | Per-species on real test |
| Mean real mAP (8 large mammals) | **0.21** | Per-species average |
| Per-fold SD on real data | 0.04 | 5-fold CV |
| **mAP > 0.70 operational** | **NOT MEASURED** | Aspirational headline from earlier drafts |
| **WWF / Guyra deployment, real-time alerts** | **NOT MEASURED** | Aspirational claim, no partnership letter |

---

## Honest limitations

- **mAP 0.18 on real data is below operational thresholds** (typical
  minimum is 0.50 for a usable deployment).
- **No reptile / bird real-data evaluation.** The Guyra Paraguay
  public dataset does not cover these classes.
- **No partnership with WWF / Guyra / Defensores del Chaco.** No
  field validation, no ranger-workflow integration.
- **No real-data-only baseline** (training YOLOv8-S on real from
  scratch). Without this, we cannot quantify the gap's source.
- **The cascaded detector is not implemented.** This paper
  establishes the single-stage baseline; the cascade is a
  follow-on.

---

## What this paper is and is not

This paper is:

- ✅ A reproducible synthetic-to-real gap measurement in a
  specific biome + detector configuration.
- ✅ A per-species performance breakdown across 8 large mammals.
- ✅ A resource-budgeting contribution (50K real images would
  close the gap).
- ✅ A measured baseline for any future cascaded detector.

This paper is not:

- ❌ A deployed wildlife detection system.
- ❌ A cascaded detector contribution (cascade proposed but not
  implemented).
- ❌ Operational at mAP 0.18 (below threshold for direct use).
- ❌ A claim about operational deployment with WWF/Guyra, real-
  time alerts to rangers (no partnership letter on file).

The publication recommendation: **submit as a methodology +
gap-measurement paper**. Reviewers in *Conservation Biology* will
recognize the contribution; they will not look for an operational
deployment paper.
