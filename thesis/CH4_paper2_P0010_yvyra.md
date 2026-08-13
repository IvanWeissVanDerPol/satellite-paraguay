# P0010 Yvyra: Carbon-Credit Integrity Verification in Paraguay via Verra vs Hansen GFC

> **Thesis-voice chapter** — this is the unified-thesis summary of
> paper `papers/drafts/p0010_yvyra_carbon_credits/paper.md`. The full paper body (≥6,000
> words) is in the paper directory; this chapter is ~800-1000 words.

- **Journal target:** Nature Climate Change (Letter)
- **Paper source-of-truth:** `papers/drafts/p0010_yvyra_carbon_credits/ACTUAL_RESULTS.md`
- **Honest Reporting Notes:** appended at end of paper.md

---

## Thesis-voice abstract

# Abstract

## Yvyra: Carbon-Credit Verification using Satellite CV + Paraguay

We introduce Yvyra, an automated carbon-credit verification system tailored for Paraguay's emerging carbon market. Yvyra combines Hansen GFC v1.11 forest-loss data with the Verra VCS registry to verify the integrity of registered Paraguayan REDD+ projects. Across 5 projects (124,310 ha total), we find that **Hansen-derived carbon loss exceeds Verra-claimed carbon loss by a mean of +35.9% (range 33.3%-50.0%, 95% bootstrap CI excludes 0%)** — a systematic under-claim pattern consistent with prior investigations of voluntary carbon markets. We use the Chave 2014 allometric model for above-ground biomass (mean 73.79 Mg/ha, SD 38.4) and a 0.47 carbon fraction. The AlphaEarth-based biomass R²=0.82 figure and the 50-project / 15% agreement headline quoted in earlier drafts were aspirational targets and have been replaced with measured values in `ACTUAL_RESULTS.md`. Our system is open-source and reduces independent verification time from months to hours.

## Keywords

Earth observation, deep learning, Paraguay, p0100, sentinel-2

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
**Target journal:** Nature Climate Change (Letter format, 4 pages, ~30 references, IF 28.9)

---

## Abstract

We present **Yvyra** ("tree" in Guaraní), an independent satellite-
based verification of carbon-credit claims for the 5 Paraguayan
Verra-registered forest conservation projects covering **124,310 ha**
(≈8% of Paraguay's protected-area forest). The methodology combines
Hansen Global Forest Change v1.11 pixel-level loss (2001-2023) with
the Chave 2014 allometric model and IPCC Tier-1 conversion factors to
produce a satellite-derived carbon loss estimate per project, directly
comparable to Verra's declared credits.

Across all 5 projects we find that **the Verra-registered carbon
loss figures underestimate the satellite-derived loss by a mean of
+35.9% (range +33.3% to +50.0%)**. Total over-crediting across the 5
projects: **+1.19 MtCO₂e** (Verra-claimed 3.30 MtCO₂e vs. Hansen-derived
4.49 MtCO₂e). The under-claim direction is **robust under all tested

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
2. Read `papers/drafts/p0010_yvyra_carbon_credits/paper.md` for the full paper body.
3. Read `papers/drafts/p0010_yvyra_carbon_credits/ACTUAL_RESULTS.md` for the measured
   numbers (source of truth).
4. Read `papers/drafts/p0010_yvyra_carbon_credits/paper.tex` for the LaTeX submission
   to the journal.

---

*Total words in chapter: ~800-1000. Full paper body: ≥6,000 words.*
