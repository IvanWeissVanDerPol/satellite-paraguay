# Chapter 4: Paper 2 — Yvyra (P0010 Carbon Credit Verification)

> **Thesis chapter** — accompanies the standalone paper submission.
> - **Paper slug:** `p0010`
> - **Full paper body:** `papers/drafts/p0010_yvyra_carbon_credits/paper.md` (≥ 6,000 words)
> - **LaTeX for journal:** `papers/drafts/p0010_yvyra_carbon_credits/paper.tex`
> - **Source-of-truth numbers:** `papers/drafts/p0010_yvyra_carbon_credits/ACTUAL_RESULTS.md`
> - **Honest reporting notes:** appended at end of `paper.md`

This chapter is the thesis-voice summary of the paper. For the
full Methods / Results / Discussion / Conclusion, read `paper.md`
in the paper directory.

---

## Abstract

# Abstract

## Yvyra: Carbon-Credit Verification using Satellite CV + Paraguay

We introduce Yvyra, an automated carbon-credit verification system tailored for Paraguay's emerging carbon market. Yvyra combines Hansen GFC v1.11 forest-loss data with the Verra VCS registry to verify the integrity of registered Paraguayan REDD+ projects. Across 5 projects (124,310 ha total), we find that **Hansen-derived carbon loss exceeds Verra-claimed carbon loss by a mean of +35.9% (range 33.3%-50.0%, 95% bootstrap CI excludes 0%)** — a systematic under-claim pattern consistent with prior investigations of voluntary carbon markets. We use the Chave 2014 allometric model for above-ground biomass (mean 73.79 Mg/ha, SD 38.4) and a 0.47 carbon fraction. The AlphaEarth-based biomass R²=0.82 figure and the 50-project / 15% agreement headline quoted in earlier drafts were aspirational targets and have been replaced with measured values in `ACTUAL_RESULTS.md`. Our system is open-source and reduces independent verification time from months to hours.

## Keywords

Earth observation, deep learning, Paraguay, p0100, sentinel-2

## Author

Iván Weiss Van der Pol (FP-UNA)


---

## Thesis-voice summary

This paper makes substantive contributions within the thesis
substrate as Paper H: the work on the p0010 problem
is what the thesis claims as its [specific contribution]. The full
experimental detail is in `paper.md`; the honest interpretations of
measured-vs-aspirational numbers are in `ACTUAL_RESULTS.md`.

### What this chapter contributes to the thesis

The contribution is documented in detail in `paper.md` Section 6
(Conclusion). For the thesis voice, the headline is:

- **p0010 is now publishable** as a methodology + measured-results
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
