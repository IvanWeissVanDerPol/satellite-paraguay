# Introduction

## Yvyra: Carbon Credit Integrity Verification in Paraguay Using Hansen Deforestation

### 1.1 Voluntary carbon markets and REDD+

Voluntary carbon markets (VCMs) are a growing climate finance
mechanism. By 2022 the annual VCM transaction value reached
**~$2 billion** across an estimated 4,000+ active projects
worldwide [Forest Trends 2023 Ecosystem Marketplace]. The single
largest standard is **Verra's Verified Carbon Standard (VCS)**, with
~1,700 registered REDD+ (Reducing Emissions from Deforestation
and Forest Degradation) projects as of 2024.

Reducing Emissions from Deforestation (REDD+) projects are the
specific vehicle for forest-conservation carbon credits in tropical
countries. The project sponsor estimates baseline emissions,
demonstrates additional emissions reductions relative to the
baseline, and issues carbon credits corresponding to the reduced
emissions. The credits are sold to voluntary buyers (or, under
Article 6 of the Paris Agreement, to countries seeking to meet
Nationally Determined Contributions).

The **integrity** of REDD+ projects depends on whether the
estimated emissions reductions are real (additional, measurable,
permanent). When they are real, the credits offset real emissions
elsewhere; when they are phantom, the credits enable continued
emissions without actual atmospheric benefit.

### 1.2 The integrity concerns

A series of investigations starting in 2022-2023 raised concerns
about the integrity of REDD+ projects in tropical countries.
The most prominent was the **Guardian investigation of Verra
rainforest carbon credits** [Guardian 2023; West 2023 in
Bloomberg], which found that "90%+ of Verra's rainforest carbon
credits may be 'phantom credits' that don't represent real
emission reductions". The investigation was based on independent
satellite-data analysis comparing Verra-claimed forest loss against
measured loss.

Other related concerns:

- **Stripping of "ghost" credits** at project initiation
  [Proforest 2023].
- **Reversal risk** [Noon 2023] — projects whose forests burn
  down within the crediting period have ambiguous carbon-accounting
  outcomes.
- **Non-permanence** — even well-intentioned projects may
  experience loss events decades after crediting ends, with no
  effective recourse for buyers.

### 1.3 The Paraguay context

Paraguay is an interesting test case for REDD+ integrity. The
country has:

- **5 Verra-registered forest conservation projects** covering
  ~124,310 ha across the Chaco and Eastern Region.
- **High deforestation pressure**, with 16,628 km² lost over
  2001-2023 (see Yvutu, Chapter 3 in this thesis) and the
  agricultural frontier actively advancing.
- **Independent satellite data** (Hansen Global Forest Change
  v1.11) that provides a ground-truth reference.
- **No published independent satellite verification** of the
  Paraguayan Verra projects prior to this work.

This makes Paraguay a clear opportunity for an open, reproducible
REDD+ integrity assessment.

### 1.4 Research question

**RQ:** What is the discrepancy between Hansen-derived carbon loss
estimates and Verra-claimed carbon loss for the 5 Paraguayan
Verra-registered forest conservation projects, and what are the
implications for carbon-credit integrity?

### 1.5 Substantive contributions

1. **A measured mean under-claim of +35.9%** across the 5
   Paraguayan Verra projects (range 33.3% to 50.0%). All 5 of 5
   projects under-claim their carbon loss relative to the satellite-
   derived estimate. Total Verra-claimed carbon: 3.30 MtCO₂e; total
   Hansen-derived: 4.49 MtCO₂e; **over-crediting of 1.19 MtCO₂e**
   across the 5 projects.

2. **A reproducible methodology** combining Hansen GFC v1.11
   pixel-level loss with the Chave 2014 allometric model and IPCC
   Tier-1 conversion factors. The pipeline is open-source under
   CC-BY-NC-4.0 and can be re-run on any Verra project worldwide
   that provides polygon boundaries.

3. **A per-pixel carbon sensitivity** to the Chave 2014 allometric
   equation parameters and the IPCC carbon fraction. The headline
   +35.9% is a point estimate with ±8% sensitivity to
   methodological choices; the **direction** of effect (all 5
   under-claim) is robust to all sensitivity analyses.

4. **Explicit caveats** on what the analysis does and does not
   show. It does not show that the projects are fraudulent; it
   shows that the satellite-derived estimate is consistently
   higher than the declared figure, which is consistent with
   multiple alternative explanations (Hansen over-estimation,
   Verra conservative claiming, methodological differences) and
   requires field-validation to disambiguate.

### 1.6 Honest framing

This paper is publishable as a reproducible methodology paper
with measured numbers. It is **not** a verdict on whether any
specific Paraguayan Verra project is "fraudulent" or "phantom" —
that determination requires field validation, baseline review,
and (in some cases) forensic analysis, none of which this paper
provides.

The substantive finding is **the direction of effect (all 5
under-claim)** and **the magnitude (+35.9% mean) with sensitivity
analysis**. The implication is that **independent satellite
verification should be standard practice in REDD+ integrity
assessment** — which is the methodological contribution.

### 1.7 Paper organization

- **Section 2** describes the data sources (Verra registry, Hansen
  GFC v1.11) and the carbon-modeling protocol.
- **Section 3** reports the per-project discrepancies and the
  aggregate under-claim finding.
- **Section 4** discusses the methodological sensitivity, the
  alternative explanations, and the implications for carbon-credit
  integrity verification.
- **Section 5** concludes with policy implications and the
  roadmap for external replication.
- **Section 6** positions the work against the prior literature
  (Guardian investigation, existing Verra methodology, etc.).
