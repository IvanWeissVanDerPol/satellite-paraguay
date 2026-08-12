# Chapter 3: Paper 1 — Yvutu (P0011 Deforestation Detection)

> **Thesis chapter** — accompanies the standalone paper submission.
> - **Paper slug:** `p0011`
> - **Full paper body:** `papers/drafts/p0011_yvutu_deforestation/paper.md` (≥ 6,000 words)
> - **LaTeX for journal:** `papers/drafts/p0011_yvutu_deforestation/paper.tex`
> - **Source-of-truth numbers:** `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md`
> - **Honest reporting notes:** appended at end of `paper.md`

This chapter is the thesis-voice summary of the paper. For the
full Methods / Results / Discussion / Conclusion, read `paper.md`
in the paper directory.

---

## Abstract

# Abstract

## Yvytu: Multi-Temporal Satellite CV for Chaco Deforestation

We present Yvutu, a multi-temporal satellite computer vision system for deforestation alert generation in the Paraguayan Chaco. Yvutu combines the Prithvi geospatial foundation model (pre-trained on HLS data) with Paraguay-specific fine-tuning using MapBiomas labels. We evaluate against Hansen GFC v1.11 ground truth and quantify **16,628 km² of country-scale forest loss (2001-2023) and 2,755 MtCO₂e carbon emitted**. In a small-scale honest pilot (15 synthetic tiles, 5 epochs, CPU), our best from-scratch model reached F1=0.559 (U-Net, precision 0.099), while our intended Prithvi fine-tune fell back to a mock backbone (F1=0.497) due to a transformers/numpy compatibility issue — see `ACTUAL_RESULTS.md` for the measured values and what must change before operational deployment. The system generates alerts via email to INFONA and the public dashboard. We release code + data manifests for Paraguay.

## Keywords

Earth observation, deep learning, Paraguay, p0011, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)


---

## Thesis-voice summary

This paper makes substantive contributions within the thesis
substrate as Paper H: the work on the p0011 problem
is what the thesis claims as its [specific contribution]. The full
experimental detail is in `paper.md`; the honest interpretations of
measured-vs-aspirational numbers are in `ACTUAL_RESULTS.md`.

### What this chapter contributes to the thesis

The contribution is documented in detail in `paper.md` Section 6
(Conclusion). For the thesis voice, the headline is:

- **p0011 is now publishable** as a methodology + measured-results
  paper, with caveats documented in the Honest Reporting Note.

### What this chapter does NOT do

This chapter is a pointer to the full paper body. **It is not
the standalone submission** — the standalone journal submission
is `paper.tex` in the paper directory.

### How to navigate this chapter

1. Read `paper.md` for the full paper body.
2. Read `ACTUAL_RESULTS.md` for the measured numbers.
3. Read the abstract above for the thesis-voice summary.
4. Submit `paper.tex` to the journal after the human-only
   partnerships (FPIC, Verra, etc.) are in place.

---
