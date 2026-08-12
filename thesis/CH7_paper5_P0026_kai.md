# Chapter 7: Paper 5 — Kai (P0026 Wildlife Poaching)

> **Thesis chapter** — accompanies the standalone paper submission.
> - **Paper slug:** `p0026`
> - **Full paper body:** `papers/drafts/p0026_kai_poaching/paper.md` (≥ 6,000 words)
> - **LaTeX for journal:** `papers/drafts/p0026_kai_poaching/paper.tex`
> - **Source-of-truth numbers:** `papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md`
> - **Honest reporting notes:** appended at end of `paper.md`

This chapter is the thesis-voice summary of the paper. For the
full Methods / Results / Discussion / Conclusion, read `paper.md`
in the paper directory.

---

## Abstract

# Abstract

## Kai: Wildlife Poaching Detection in Defensores del Chaco

We present Kai, an AI-based wildlife detection system for Paraguay's Defensores del Chaco and Teniente Agripino Enciso national parks. We fine-tune YOLOv8-S on Blender-synthetic wildlife imagery (1,280 images, 24 species) and evaluate on 5,000 real camera-trap images from Guyra Paraguay. **mAP@0.5 drops from 0.50 on synthetic validation to 0.18 on real test data** — a 0.32 absolute gap consistent with the literature on synthetic-to-real domain shift. Reptile detection is worst (mAP=0.05 real). The mAP@0.5>0.70 headline and the WWF/Guyra deployment claims quoted in earlier drafts were aspirational and have been replaced with measured values in `ACTUAL_RESULTS.md`. We frame this as a contribution precisely because the gap quantifies how much Paraguay-specific labeled wildlife data is needed before operational deployment.

## Keywords

Earth observation, deep learning, Paraguay, p0026, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)


---

## Thesis-voice summary

This paper makes substantive contributions within the thesis
substrate as Paper H: the work on the p0026 problem
is what the thesis claims as its [specific contribution]. The full
experimental detail is in `paper.md`; the honest interpretations of
measured-vs-aspirational numbers are in `ACTUAL_RESULTS.md`.

### What this chapter contributes to the thesis

The contribution is documented in detail in `paper.md` Section 6
(Conclusion). For the thesis voice, the headline is:

- **p0026 is now publishable** as a methodology + measured-results
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
