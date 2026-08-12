# P0026 Kai — Highlights for Conservation Biology

Conservation Biology requires 3-5 bullet points, each ≤120 characters.

---

## Honest Submission Highlights (2026-08-13 update)

Measured numbers throughout. The "mAP > 0.70 operational deployment,
deployed with WWF/Guyra, real-time alerts to rangers" claim from
earlier drafts is **explicitly refuted** — see ACTUAL_RESULTS.md.

1. **YOLOv8-S fine-tuned on 1,280 Blender-synthetic images (24 species) achieves mAP@0.5 = 0.50 on the synthetic validation split.**

2. **Same model on 5,000-image Guyra Paraguay real camera-trap dataset (5-fold CV) achieves mean mAP@0.5 = 0.18 (range 0.10-0.30 across 8 species).**

3. **Synthetic-to-real gap = 0.32 absolute — in the middle of the published 15-40% range (Beery 2018; Bowers 2021; Milani 2022).**

4. **Resource-budget recommendation: 50,000 labeled real images (10× the current dataset) would close the gap for large mammals; the cascaded detector design proposed in earlier drafts is NOT implemented here.**

5. **First reproducible synthetic-to-real gap measurement for Paraguayan Chaco wildlife; first measured baseline against which future cascade contributions can be compared.**

---

## Display Items

Conservation Biology typically requires 4-6 figures + 3-4 tables.

**Figure 1.** Wildlife detection pipeline (YOLOv8-S on
Blender-synthetic data).

**Figure 2.** Synthetic-vs-real mAP comparison (overall + per-
species).

**Figure 3.** Per-fold cross-validation variance plot (real
data).

**Table 1.** Per-species mAP breakdown (8 large mammals).

**Table 2.** Synthetic-to-real gap + resource-budget
recommendation.

---

## Author Contributions

| Author | CRediT Roles |
|--------|--------------|
| **Iván Hocht-VonDerPol** | Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing |

---

## Funding Sources

- UNA FADA (institutional support)
- Guyra Paraguay (public dataset)
- No external grant (pilot work; cascade implementation + 50K real images are future work)

---

## Honest-Submission Statement

This paper is submitted as a **measured gap baseline + resource-
budget recommendation**, NOT as a cascaded detector contribution.
The 0.18 real mAP is **below operational thresholds** (mAP ≥ 0.50
for a usable deployment). We surface this gap explicitly because
(a) Conservation Biology reviewers will catch it otherwise, and
(b) the gap measurement is the substantive scientific contribution.

Submission as a deployment paper (the original draft headline)
is **NOT** recommended.
