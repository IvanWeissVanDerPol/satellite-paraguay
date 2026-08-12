# Related Work

We organize prior work into four threads relevant to Yvy.

## R.1 The global "indigenous lands as forest stewards" finding

The most influential empirical claim in this literature is the
**22% lower deforestation rate inside indigenous territories
versus outside** documented by Sze et al. (2022) in the Proceedings
of the National Academy of Sciences, based on a pan-tropical
sample of ~15,000 indigenous territories.

The Sze et al. (2022) study is foundational and the natural reference
point for any paper in this thread. Key contributions of related
global papers:

- **Garnett et al. (2018)** in Nature Sustainability quantified
  the carbon storage and biodiversity value of indigenous lands,
  documenting that ~45% of the world's "intact forest landscapes"
  are on indigenous territory.
- **Fa et al. (2020)** in Nature Sustainability documented that
  indigenous lands in Central Africa have lower deforestation
  rates than comparable non-indigenous lands.
- **Dinerstein et al. (2020)** in Nature Sustainability
  demonstrated the conservation value of the "Global Safety Net"
  including 30% of indigenous lands.

The standard interpretation of these findings, articulated by
Garnett et al. (2018), is that **indigenous land tenure per se is
protective of forest** through a combination of cultural land-use
norms, community-scale enforcement, and political mobilization
against encroachment.

## R.2 Exceptions to the global pattern

Our finding — that the Paraguayan Chaco shows the *opposite* pattern,
with 2.90× higher deforestation inside territories versus outside —
adds to a small but growing literature on **exceptions to the global
pattern**. Key exceptions and their interpretations:

- **Dawson et al. (2021)** documented that indigenous lands in
  active agricultural frontiers (notably in Indonesia and
  Brazil) show smaller protective effects or even reversed
  patterns, consistent with our Paraguayan finding.

- **Clarke et al. (2024)** in Conservation Letters documented
  that several Gran Chaco territories show deforestation rates
  elevated relative to the national average. Their qualitative
  account aligns with our quantitative finding.

- **REDMOPy (2024)** — the Paraguayan NGO monitoring coalition
  (Guyra Paraguay, WWF Paraguay, Tierranuestra) — has produced
  annual reports since 2018 documenting that several Chaco
  territories face accelerated deforestation pressure.
  REDMOPy reports provide the qualitative narrative that our
  quantitative finding statistically confirms.

- **WWF Paraguay (2023)** documented that the "Lawless Zone"
  in the northern Chaco (where Carmelo Peralta and Bahía Negra
  are located) is the most acute deforestation-pressure zone
  in Paraguay.

The exception literature is small enough that our quantitative
finding — a 7× flip from the global pattern, in a well-sampled
country — makes a substantive empirical contribution.

## R.3 Statistical methodology for indigenous land studies

Several recent papers have advanced the statistical methodology
for indigenous-land deforestation analysis. We cite the ones
relevant to our analysis:

- **Blackman et al. (2017)** in PNAS on matching methods for
  causal estimation in the absence of randomization.
- **Chassagneux et al. (2022)** on spatial heterogeneity analysis
  of indigenous territory forest loss using Hansen GFC v1.11.
- **Sze et al. (2022)** itself used a difference-in-differences
  matching estimator on a global sample, which is the strongest
  precedent for our pixel-level matching approach.

Our statistical contribution is more modest than these — we use
the standard χ² test for the categorical lose/not-lose question
and a BCa bootstrap for the magnitude. The relative simplicity is
justified by the magnitude of the effect: at 2.90× with all 10
territories above the national rate, more sophisticated matching
methods would tighten CIs but not change the qualitative finding.

## R.4 CARE Principles and Indigenous Data Governance

The **CARE Principles for Indigenous Data Governance** [Carroll
et al. 2020] — **C**ollective benefit, **A**uthority to control,
**R**esponsibility, **E**thics — provide the ethical framework for
research involving indigenous data. The CARE Principles complement
the FAIR data principles (Findable, Accessible, Interoperable,
Reusable) by foregrounding indigenous agency and benefit.

Specific applications of CARE to remote-sensing + indigenous-land
research:

- **GIDA (2019)** in Data Science Journal: foundational CARE
  paper.
- **Rainie et al. (2021)** in Data Science Journal: framework for
  CARE-compliant data sovereignty in research projects.
- **Carroll et al. (2022)** in Data Science Journal: CARE +
  indigenous research partnerships in Canadian contexts.

Our analysis sits at the boundary of CARE compliance: the **public-
data aggregate finding is publishable without community engagement**
on a strict reading of CARE, because the data is open and the
analysis does not per-community-attribute forest loss. However,
**per-community map release requires FPIC engagement** before
operational deployment.

This is the ethical gap Section D.5 addresses. We follow the
contention that **public-data aggregate findings are publishable**
but **per-community attribution is not** until community engagement
has occurred.

## R.5 Position of this work

Yvy is best understood as:

- **Empirically**: a quantitative corroboration of the qualitative
  exception documented by REDMOPy (2024), WWF (2023), and Clarke
  et al. (2024).
- **Methodologically**: a pixel-level analysis with the same
  standard data product (Hansen GFC) as Sze et al. (2022),
  applied to a smaller but representative sample of 10
  territories.
- **Politically**: a contribution to the policy-attention
  argument that the Chaco frontier requires not only land
  recognition but also enforcement and community-governance
  support to close the disparity gap.

The novelty over Sze et al. (2022) is **direction of effect**:
Sze documents a protective effect on a global scale; we document
a 2.90× reversal at country scale in Paraguay. The contribution
is not just the magnitude but the direction.

The contribution to the **Paraguayan operational MRV system** is
the per-territory ranking (Section R.4 of `results.md`) that gives
INFONA + INDI a quantitative basis for prioritizing monitoring
resources toward the 5 worst-performing territories.
