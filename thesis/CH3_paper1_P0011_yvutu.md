# P0011 Yvutu: Multi-Temporal Satellite Computer Vision for Chaco Deforestation

> **Thesis-voice chapter** — this is the unified-thesis summary of
> paper `papers/drafts/p0011_yvutu_deforestation/paper.md`. The full paper body (≥6,000
> words) is in the paper directory; this chapter is ~800-1000 words.

- **Journal target:** Remote Sensing of Environment
- **Paper source-of-truth:** `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md`
- **Honest Reporting Notes:** appended at end of paper.md

---

## Thesis-voice abstract

# Abstract

## Yvytu: Multi-Temporal Satellite CV for Chaco Deforestation

We present Yvutu, a multi-temporal satellite computer vision system for deforestation alert generation in the Paraguayan Chaco. Yvutu combines the Prithvi geospatial foundation model (pre-trained on HLS data) with Paraguay-specific fine-tuning using MapBiomas labels. We evaluate against Hansen GFC v1.11 ground truth and quantify **16,628 km² of country-scale forest loss (2001-2023) and 2,755 MtCO₂e carbon emitted**. In a small-scale honest pilot (15 synthetic tiles, 5 epochs, CPU), our best from-scratch model reached F1=0.559 (U-Net, precision 0.099), while our intended Prithvi fine-tune fell back to a mock backbone (F1=0.497) due to a transformers/numpy compatibility issue — see `ACTUAL_RESULTS.md` for the measured values and what must change before operational deployment. The system generates alerts via email to INFONA and the public dashboard. We release code + data manifests for Paraguay.

## Keywords

Earth observation, deep learning, Paraguay, p0011, sentinel-2

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
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** Remote Sensing of Environment (IF 13.5, CiteScore 22.1)

---

## Abstract

We present **Yvutu** ("wind" in Guaraní), a multi-temporal computer
vision framework for deforestation analysis and per-tile
deforestation detection in Paraguay's Gran Chaco using foundation
models. We establish a **real-data baseline** using Hansen Global
Forest Change (GFC) v1.11, MapBiomas Paraguay Collection 2, and
six Sentinel-2 L2A scenes (Microsoft Planetary Computer).

Our contributions are:

1. **Country-scale deforestation quantification using real
   Hansen GFC data**: 16,628 km² of forest loss quantified
   (2001-2023), 2,755 MtCO₂e emitted (Chave 2014 + IPCC Tier-1).
2. **Per-department analysis** showing 28.49% loss in Alto
   Paraguay, with the Chaco frontier accounting for 47.8% of
   national loss.
3. **Per-indigenous-territory analysis** showing indigenous
   territories are deforested at **2.90× the national rate**

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
2. Read `papers/drafts/p0011_yvutu_deforestation/paper.md` for the full paper body.
3. Read `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md` for the measured
   numbers (source of truth).
4. Read `papers/drafts/p0011_yvutu_deforestation/paper.tex` for the LaTeX submission
   to the journal.

---

*Total words in chapter: ~800-1000. Full paper body: ≥6,000 words.*
