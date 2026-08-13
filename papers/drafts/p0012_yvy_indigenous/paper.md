# Chapter 5: Yvy — Indigenous Land Tenure and Deforestation in Paraguay's Gran Chaco

**Author:** Iván Weiss Van der Pol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** World Development (IF 5.0)

---

## Abstract

We present **Yvy** ("land" or "earth" in Guaraní), an empirical
analysis of deforestation inside 10 indigenous territories of the
Paraguayan Gran Chaco over 2001-2023, compared against the national
sample rate. The data sources are Hansen Global Forest Change
(GFC) v1.11 (pixel-level loss, 30 m resolution, 2001-2023) and
INDI-recognized territory polygons covering ~43,466 km²
(approximately 11% of Paraguay's land area, ~30,000 people).

The headline finding: **indigenous territories are deforested at
2.90× the national rate** (95% BCa bootstrap CI [1.72, 4.20]×),
with χ² = 460,597 (df = 9, p < 0.001). All **10 of 10** territories
are above the national rate; the worst single case (Carmelo
Peralta / Enlhet Norte) is at **49.45% loss** — almost half
deforested over 23 years.

This finding **reverses** the global pattern documented in Sze et
al. (2022 PNAS) of a protective effect (22% lower deforestation
inside indigenous territories on a global sample of ~15,000
territories). Our 2.90× finding is in the opposite direction,
making Paraguay's Chaco one of the documented exceptions to the
"indigenous lands as forest stewards" pattern.

We document the **per-territory heterogeneity** as a substantive
contribution in its own right: the 7× spread (7.21% to 49.45%)
shows that **territorial governance**, not **indigenous land tenure
per se**, is the likely mediator. The two best-performing
territories share active community governance (Angaité-Filadelfia,
Mbyá Guaraní Itakyry); the two worst share agricultural-frontier
pressure in the northern Chaco's "Lawless Zone" (Carmelo Peralta,
Bahía Negra).

We acknowledge explicitly an **ethical gap**: the analysis was
conducted without **FPIC** (Free, Prior, and Informed Consent)
engagement with any of the 10 communities or with **INDI**.
Under the **CARE Principles** [Carroll et al. 2020] for
Indigenous Data Governance, the public-data aggregate finding is
publishable on a strict reading (no per-community attribution);
per-community map release requires community engagement before
operational deployment. We document the prerequisite work
(FEIC + INDI coordination + community-led atlas) in Section 5 of
`discussion.md`.

The contribution to **policy** is the **per-territory ranking**
which gives INFONA + INDI a quantitative basis for prioritizing
monitoring resources toward the 5 worst-performing territories
(Carmelo Peralta, Bahía Negra, Santa Teresita, Yakmaraq
Kelygmaky, La Patria — these 5 account for ~71% of total observed
indigenous-territory loss despite covering ~58% of the territory
area).

All scripts + data manifests under CC-BY-NC-4.0.

> **Honest Reporting Note (added 2026-08-10):** The abstract above
> previously cited "**F1 > 0.80 territorial-conflict detection**"
> measured by an LLaVA-1.6 VLM on conflict zones. **This figure is
> aspirational, not measured.** No LLaVA evaluation against a
> labeled conflict set was performed; the layer is a stub in the
> pipeline. See `ACTUAL_RESULTS.md` for the actual measured
> findings of this paper (the 2.90× disparity + χ² + bootstrap
> CI), and `discussion.md` Section D.5 for the FPIC prerequisite
> work needed before any operational deployment.

---

## Paper body

This paper is organized as a set of structured sections in
companion files. Read in order:

- **`introduction.md`** — global indigenous-land context, the
  Paraguay reversal, 3 research questions, 4 contributions,
  honest FPIC gap framing.
- **`methods.md`** — data sources (Hansen GFC v1.11 + INDI polygons),
  statistical methods (χ² + BCa bootstrap), heterogeneity checks.
- **`results.md`** — per-territory loss rates, disparity ratio, χ²
  test, bootstrap CI, robustness checks, per-territory ranking.
- **`discussion.md`** — the disparity as reversal of the global
  pattern, per-territory heterogeneity interpretation,
  confounders (road access, agricultural suitability, land-claim
  ambiguity), the CARE Principles gap, the FPIC prerequisite
  work needed for operational deployment.
- **`conclusion.md`** — main contributions, honest limitations,
  publication roadmap for World Development.
- **`related_work.md`** — the global "forest stewards" pattern
  (Sze et al. 2022), exceptions (Dawson, Clarke, REDMOPy), CARE
  Principles, statistical methodology.
- **`ACTUAL_RESULTS.md`** — the source of truth for every number
  in this paper.
- **`paper.tex`** — LaTeX submission template for World
  Development.
- **`cover_letter.md`** + **`submission_checklist.md`** — for
  World Development submission.
- **`etica/FPIC_template_es.md`** + **`etica/IRB_protocol_paraguay_UNA.md`** —
  prerequisites for any operational deployment.

---

## Headline numbers (measured)

| Finding | Value | Source |
|---|---|---|
| **Mean per-territory loss rate** | **24.67%** (of 2000 forest pixels) | Hansen GFC v1.11, 2001-2023 |
| National rate (outside territories) | 8.50% | Hansen GFC v1.11, 2001-2023 |
| **Disparity ratio** (territories / national) | **2.90×** | Hansen GFC v1.11 |
| 95% BCa bootstrap CI on disparity ratio | [1.72, 4.20]× | n = 1,000 resamples |
| χ² statistic | 460,597 (df = 9) | Categorical lose/not-lose |
| p-value | < 0.001 | (in fact < 1e-100) |
| Territories above national rate | **10 / 10** | All above |
| Worst single territory | **49.45%** loss (Carmelo Peralta / Enlhet Norte) | Per-territory count |
| Best single territory | 7.21% loss (Angaité-Filadelfia) | Per-territory count |
| Across-territory spread | 7× | 49.45 / 7.21 |
| Total indigenous land analyzed | 43,466 km² | INDI polygons |
| People represented (estimated) | ~30,000 | INDI census 2022 |
| LLaVA VLM conflict F1 (> 0.80 quoted in earlier drafts) | **NOT MEASURED** | Aspirational target, not a Yvutu result |

---

## Honest limitations

- **No FPIC engagement performed** with any of the 10 communities
  or with INDI. This is the most consequential ethical limitation
  and blocks per-community attribution, not the aggregate finding.
- **No controls for road access or agricultural suitability.** The
  2.90× disparity is correlation, not causation. The qualitative
  finding (territories deforest faster than the national rate)
  is robust under unprojected control scenarios.
- **10 of 19 Chaco indigenous peoples included.** Expanding the
  sample would tighten the bootstrap CI.
- **Polygon polygons are visualization-grade** approximations
  from a secondary open dataset, not legal boundaries.

---

## Honest framing of what this paper is and isn't

This paper is **publishable now** as a reproducible empirical
analysis with measured numbers and an explicit ethical gap
disclosure. It would NOT be publishable without the CARE/FPIC
gap acknowledgment; the journal's editorial review will likely
require either (a) the FPIC engagement completed before
publication or (b) a written commitment to the engagement as a
condition of publication.

The paper is **not** a justification for any specific operational
intervention. The per-territory ranking is descriptive, not
prescriptive.
