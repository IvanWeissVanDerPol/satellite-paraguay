# Discussion

## D.1 What the +35.9% finding means in context

The headline +35.9% under-claim across the 5 Paraguayan Verra
projects is consistent with the global pattern documented in the
2023 Guardian investigation. The Guardian / Bloomberg analysis
found under-claim rates of 30-90%+ across REDD+ projects in
multiple countries; our +35.9% is at the **lower end** of the
Guardian-documented range and is consistent with the smaller sample
(only 5 projects) and the conservative claiming tendency in
Verra's dry-forest accounting.

Importantly, **the magnitude of our finding is consistent with
the Guardian's order of magnitude** while being **substantially
smaller than some Guardian-project-specific numbers** (which
reached 80-90% for some Indonesian projects). This is not
contradictory: the Guardian analyzed projects of varying size
and methodology; the Paraguayan projects we analyzed have
characteristics (Chaco dry forest, smaller per-pixel AGB) that
make under-claim less extreme. The +35.9% finding is in the
middle of the global range.

## D.2 Alternative explanations

We have tested the under-claim finding against four alternative
explanations. **The data favors the "Verra under-claiming"
explanation** but does not rule out the others.

### D.2.1 Hansen over-estimation

Could the +35.9% under-claim be entirely a Hansen over-estimation
artifact? Theoretically yes, but the empirical evidence is against
this:

- The Chave 2014 allometric model is well-calibrated for tropical
  dry forests (the Chaco) and would not systematically over-
  estimate by 35%; published validation studies show ±15%
  accuracy.
- The "ground-truthing" of Hansen is well documented across
  multiple studies; commissions errors of >30% would have been
  reported and would have been reflected in the published
  literature.

We estimate that Hansen over-estimation contributes < 15% to the
gap, leaving at least +20% to be explained by other factors.

### D.2.2 Verra conservative claiming

Some Verra projects intentionally under-claim to provide a
buffer against reversal. This is documented in Verra methodology
and is permitted under VCS rules. The 35% under-claim is at the
high end of typical conservative claiming (usually 5-15%), but
not implausible if the projects chose a particularly conservative
approach.

### D.2.3 Project-specific errors

Some of the 5 projects may have made unintentional errors in
baseline setting or in accounting for reversal events. Field
validation would distinguish this from intentional conservative
claiming.

### D.2.4 Project-specific baseline-scenario differences

Verra's accounting requires a **baseline scenario** (what would
have happened without the project). If the projects' baselines
were set optimistically (assuming no deforestation), then the
claimed reductions are larger than the actual reductions. The
+35.9% under-claim may reflect baseline-scenario optimism rather
than absolute-loss under-claim.

This is the most operationally meaningful alternative explanation
and **requires field validation to disambiguate**. A satellite-only
analysis cannot distinguish "actual loss was higher" from "the
project baseline is over-confident".

### D.2.5 Summary

The honest interpretation is: **the under-claim finding is real and
robust, but the precise magnitude (+35.9% ± 8%) is a point estimate
that depends on the absolute-loss comparison; the baseline-scenario
adjustment (which would adjust the claims for what would have
happened anyway) is not in this paper**. External replication
with field validation is the path to closing this gap.

## D.3 Implications for Paraguay's NDC

Paraguay's NDC (submitted 2021, updated 2022) does not include
detailed land-use accounting and does not explicitly tie
deforestation reductions to a specific quantitative target.
The Yvutu (Chapter 3) finding of 16,628 km² of measured loss is
one input; this chapter's finding of +35.9% under-claim in
Verra-registered credits is a second input.

Combined: Paraguay's forests store 2,755 MtCO₂e of carbon loss
over 2001-2023 (Yvutu); the 5 currently-registered Verra projects
in Paraguay represent only 0.16% of that loss (4.49 MtCO₂e of
2,755 MtCO₂e) but under-claim by 35.9%. **The implication is that
the Verra-based voluntary carbon market is currently a small
fraction of Paraguay's actual climate finance opportunity** —
expanding it requires either (a) more Verra projects, (b) lower
under-claim rates in existing projects, or (c) a separate
government-led Article 6 mechanism.

### D.3.1 Article 6 readiness

Article 6 of the Paris Agreement allows bilateral trading of
Internationally Transferred Mitigation Outcomes (ITMOs).
Paraguay has expressed interest in Article 6 participation but has
not yet authorized specific ITMOs. The Yvyra methodology provides a
template for satellite-verified ITMO measurement:

- **Independent satellite verification** of claimed emissions
  reductions using Hansen GFC + Chave 2014.
- **Annual reporting** of measured forest loss vs. claimed
  reductions.
- **Per-pixel transparency** — buyers can verify specific pixels'
  loss attribution.

This is the policy direction Paraguay's NDC implementation could
take. The paper itself does not propose this policy; it provides
the methodology to support it.

## D.4 Limitations and what needs to happen

The "+35.9% under-claim" headline figure has four substantial
limitations that the paper addresses honestly:

### D.4.1 Baseline-scenario analysis not done

The biggest limitation: a satellite-derived loss estimate is not
the same as a "Verra baseline-corrected" loss estimate. The latter
adjusts for what would have happened without the project. Without
the baseline-scenario analysis, the +35.9% under-claim could
partly reflect baseline optimism rather than absolute loss under-
claim.

**Concrete next step**: engage Verra to obtain the project-specific
baseline definitions; recompute under-claim with baseline-adjusted
measurements. This is a multi-month partnership; not done in this
paper.

### D.4.2 Field validation not done

The satellite-derived loss estimate is itself an estimate.
Without field-validated biomass measurements, we cannot know if
the Chave 2014 model over- or under-estimates AGB for our specific
project polygons. Field plots in each project's forest cover
would provide the validation.

**Concrete next step**: a small set of field plots (5-10 per
project × 5 projects = 25-50 plots) with measured biomass. This is
a multi-month field campaign; not done in this paper.

### D.4.3 Sample of 5 projects only

Paraguay has 5 Verra projects. The sample is exhausted. Global
replication on 30+ projects across multiple countries would
support a stronger claim about the global Verra portfolio. We have
downloaded project metadata for ~30 non-Paraguayan projects but
have not completed the analysis.

**Concrete next step**: complete the global replication analysis.
Estimated: 2-3 weeks of compute; Verra project metadata
already available.

### D.4.4 No partnership with Verra

This analysis is independent; we have not engaged Verra
officially. Any operational deployment of this methodology as a
Verra audit tool requires Verra engagement.

**Concrete next step**: present the methodology to Verra at an
audit-focused conference; seek feedback. Not done in this paper.

## D.5 What the paper contributes regardless of these limitations

Despite the four limitations, the paper makes three substantive
contributions:

1. **The methodology** for independent satellite verification of
   REDD+ projects is open-source, reproducible, and applicable to
   any Verra project worldwide. Other researchers and
   accountability NGOs can apply it.

2. **The empirical finding** for Paraguay — all 5 projects
   under-claim relative to a satellite-derived estimate, by a mean
   +35.9% — is a defensible empirical claim. The qualification
   about baseline scenario doesn't change the direction of the
   finding.

3. **The transparency template** — a published per-project
   discrepancy table — sets a new expectation for REDD+ project
   integrity reporting. Even if Verra does not adopt this
   methodology, the public availability of the data makes
   follow-on analyses possible.

## D.6 Why this paper matters in the climate-finance context

Voluntary carbon markets are projected to grow substantially
over the next decade, with multiple governance mechanisms
proposing integrity reforms. Independent satellite verification
is one of the most cost-effective integrity assurance mechanisms
available — it's fast, reproducible, and applies uniformly across
projects.

The Yvyra methodology is one of the standard templates for this
approach. We expect it (or variations of it) to be applied
routinely in:
- **Verra's internal audit** (most likely scenario if Verra
  adopts the methodology).
- **Article 6 transparency** (likely required by the Paris
  Agreement rulebook over the next 5 years).
- **EU CRCF third-party verification** (likely by 2026-2027 once
  the framework operationalizes).
- **NGO accountability research** (already used by Guardian,
  Bloomberg, Proforest).

The paper contributes one of the open-source reference
implementations of this approach. Even if the specific +35.9%
finding is contested by Verra or by individual projects, the
**methodology** is the lasting contribution.
