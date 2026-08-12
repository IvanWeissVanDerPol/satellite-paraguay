# Chapter 4: Yvyra — Carbon Credit Integrity Verification in Paraguay Using Hansen Deforestation

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
methodological variations** (carbon fraction 0.42-0.52; Chave wet vs.
dry allometric form; forest-canopy threshold 30-70%): the sign test
on 5 of 5 positive $\Delta$ values has $p = 0.063$ (one-tailed) and the
Wilcoxon signed-rank test has $p = 0.031$.

The finding is **consistent with the global pattern** documented by
the 2023 Guardian investigation of Verra rainforest credits, but is
at the lower end of the Guardian-documented range. The +35.9% figure
has a ±8% sensitivity envelope from methodological choices;
**the qualitative direction (all 5 under-claim) is robust**.

We **acknowledge four substantial limitations**: (i) the baseline-
scenario adjustment that Verra's methodology applies is not modeled
here — the under-claim magnitude reflects absolute-loss under-claim,
not baseline-adjusted claim-vs-actual-discrepancy; (ii) the Chave
2014 model is not ground-truthed for our specific project polygons;
(iii) the sample is the 5 Paraguayan projects (exhausted); and
(iv) **we have no partnership with Verra**, the EU CRCF, or any
Article 6 mechanism — this is independent analysis.

We explicitly **do not** claim that any specific project is "phantom"
in the Guardian sense; that determination requires baseline-scenario
analysis (not done) and field validation (not done). The
contribution is the **methodology** for independent satellite
verification of REDD+ projects, applicable globally. The Paraguay-
specific quantification is a worked example.

All code + data + project listings under CC-BY-NC-4.0.

> **Honest Reporting Note (added 2026-08-10):** The abstract above
> does not include the "AlphaEarth R²=0.82 biomass" figure or the
> "50+ Verra projects comparison" figure from earlier drafts of this
> chapter. **Both are aspirational, not measured.** The AlphaEarth
> fine-tune was never run in this thesis; the global replication
> analysis (50+ Verra projects) is downloaded but not yet
> executed. See `ACTUAL_RESULTS.md` for the actual measured numbers
> (5 projects only, +35.9% mean, ±8% sensitivity envelope) and
> `discussion.md` Section D.4 for what needs to happen before a
> broader claim can be made.

---

## Paper body

This paper is organized as a set of structured sections in
companion files. Read in order:

- **`introduction.md`** — voluntary carbon market context, the
  Guardian investigation, the Paraguay test case, 1 research
  question, 4 contributions, honest limitations on the headline.
- **`methods.md`** — Verra registry extraction, Hansen GFC per-
  pixel loss, Chave 2014 allometric model, carbon conversion
  factors, per-project aggregation, statistical tests
  (sign + Wilcoxon), sensitivity analysis (3 dimensions).
- **`results.md`** — per-project discrepancy table, aggregate
  total (+1.19 MtCO₂e over-crediting), statistical robustness,
  sensitivity envelope (±8%), sub-departmental pattern.
- **`discussion.md`** — meaning of +35.9% in the Guardian context,
  four alternative explanations, implications for Paraguay's NDC
  and Article 6 readiness, limitations and next steps.
- **`conclusion.md`** — main contributions, honest limitations,
  submission roadmap for Nature Climate Change.
- **`related_work.md`** — Guardian/West Bloomberg investigation,
  Verra methodology (VM0007, VM0009, VM0015), Chave allometric
  papers, voluntary carbon market integrity literature.
- **`ACTUAL_RESULTS.md`** — the source of truth for every number
  in this paper.
- **`paper.tex`** — LaTeX Letter format for Nature Climate Change.
- **`cover_letter.md`** + **`submission_checklist.md`** — for
  Nature Climate Change submission.

---

## Headline numbers (measured)

| Finding | Value | Source |
|---|---|---|
| Total Paraguayan Verra project area | 124,310 ha (≈1,243 km²) | Verra registry |
| Total Verra-claimed CO₂e reductions (2001-2023) | 3.30 MtCO₂e | Verra project docs |
| Total Hansen-derived CO₂e loss (2001-2023) | **4.49 MtCO₂e** | Hansen GFC v1.11 + Chave 2014 |
| **Mean under-claim ratio** | **+35.9%** (range +33.3% to +50.0%) | Per-project Hansen vs Verra |
| Total over-crediting across 5 projects | **+1.19 MtCO₂e** | Aggregate |
| Projects where Verra under-claims | **5 / 5** | All 5 |
| Sign test p-value (one-tailed) | 0.063 | 5 of 5 positive |
| Wilcoxon signed-rank p-value | 0.031 | Statistically significant |
| Sensitivity envelope (±8%, quadrature combined) | +27.9% to +43.9% | Carbon fraction + Chave form + threshold |
| **AlphaEarth R²=0.82 biomass** | **NOT MEASURED** | Aspirational target, not a Yvyra result |

---

## Honest limitations

- **Baseline-scenario analysis not done.** The +35.9% is
  absolute-loss under-claim, not baseline-adjusted claim-vs-
  actual discrepancy. Closing this requires Verra partnership to
  obtain project-specific baselines.
- **Field validation not done.** The Chave 2014 model has not
  been ground-truthed for our specific project polygons. 25-50
  field plots per project would resolve this.
- **Sample of 5 projects only**, the population of Paraguayan
  Verra projects. Global replication on 30+ projects would
  support a stronger claim.
- **No partnership with Verra / Article 6 / EU CRCF.** This is
  independent analysis. Operational deployment requires
  partnership engagement.
- **No claim that any specific project is "phantom"** in the
  Guardian-investigation sense; that determination requires
  baseline-scenario + field-validation, neither of which this
  paper provides.

---

## What this paper is and isn't

This paper is:

- ✅ A reproducible methodology paper with measured numbers on
  the 5 Paraguayan projects.
- ✅ A defensible empirical claim about an open-data comparison
  of the 5 Paraguayan Verra projects vs. Hansen-derived loss.
- ✅ A contribution to the global "Verra integrity" literature
  with a Paraguay-specific quantification in the lower range of
  the Guardian findings.

This paper is not:

- ❌ A verdict that any specific project is "phantom".
- ❌ A claim about the global Verra portfolio (would require
  replication on 30+ projects from multiple countries).
- ❌ An Article 6 / EU CRCF audit tool (would require partnership
  and field validation).
- ❌ A claim that the projects acted in bad faith (the
  under-claim is consistent with multiple alternative
  explanations).

All code + data listings + per-project JSON outputs under
CC-BY-NC-4.0. Authors are committed to making the full Verra
discrepancy table publicly available if and when the projects
consent to unblinded attribution.
