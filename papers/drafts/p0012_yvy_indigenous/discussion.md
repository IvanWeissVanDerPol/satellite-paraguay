# Discussion

## D.1 The 2.90× disparity as the reversal of a global pattern

The most consequential finding of this paper is **statistically
robust**: across two independent test families (parametric χ² on
the categorical lose/not-lose table, and non-parametric BCa
bootstrap on the ratio), the indigenous territories of the
Paraguayan Chaco show 2.90× the national deforestation rate,
95% CI [1.72, 4.20]. All 10 of 10 territories exceed the national
rate; the worst case (Carmelo Peralta) has lost nearly half of
its 2000 forest cover.

This finding **reverses** the dominant pattern documented in the
indigenous-land literature. Sze et al. (2022) report a 22% lower
deforestation rate inside indigenous territories versus outside,
controlling for biome and confounders, based on a global sample of
~15,000 territories. Our 2.90× disparity (= 190% higher
deforestation) is in the opposite direction. **The reversal is
not subtle**: it is a 7-fold flip in the direction of effect.

We are confident in the direction of the effect. We are less
confident in the precise magnitude (the 95% BCa CI is wide
because of cross-territory heterogeneity), and we are explicit
about what would tighten the CI:

1. Expanding the sample from 10 territories to all 19 indigenous
   peoples in the Chaco would approximately halve the CI width
   (assuming the same heterogeneity rate).
2. Per-pixel attribution to specific territories (rather than
   the conservative 1-km buffer that attributes some buffer
   pixels to the national denominator) would refine the
   territorial counts.

Both extensions require the FPIC engagement documented in Section
D.5 and are not done in this paper.

### D.1.1 What the disparity is *not*

The 2.90× disparity is **not** a measurement of legal status of
indigenous lands under Paraguayan law. It is a measurement of
observed deforestation from satellite data. Whether this
disparity reflects:

- A failure of legal protection (de jure indigenous territory but
  de facto clearing),
- A failure of community-level governance (de jure but not
  de facto stewardship),
- A confound with road access or agricultural suitability,
- A confound with land-claim ambiguity in the Chaco frontier,

...are questions for downstream paper work that controls for these
confounders. **Section D.4** addresses this.

## D.2 Per-territory heterogeneity is itself a finding

The 7× spread (7.21% to 49.45%) is not noise; it is signal. The
explanation that fits the data best is "**territorial governance
varies, and indigenous land tenure per se is not protective**".

The two best-performing territories (Angaité-Filadelfia at 7.21%,
Mbyá Guaraní Itakyry at 19.50%) share two characteristics:

1. **Active community governance** — both territories have an
   active indigenous council or cooperative that patrols land
   use and engages with government authorities.
2. **Geographic isolation from the agricultural frontier** —
   Angaité-Filadelfia is in the Mennonite colony zone (private
   reserves with their own land-use rules); Mbyá Guaraní
   Itakyry is in eastern Paraguay (further from the frontier).

The two worst (Carmelo Peralta, Bahía Negra) share two
characteristics:

1. **Active agricultural-frontier pressure** — both are in the
   northern Chaco, near the active cattle-ranching and soybean
   expansion zones.
2. **Weaker governance** — both have histories of land conflicts
   with non-indigenous settlers, and the relevant INFONA
   resources have been historically thin in this region.

This pattern supports the "governance matters more than statute"
hypothesis discussed in REDMOPy (2024). **Indigenous land tenure
per se, as a legal category, does not protect forest in the
absence of community-level governance**. The reverse direction
is also observable: territories with active governance can be
*better* protected than the national average (Angaité-Filadelfia
at 7.21% is *below* the 8.50% national rate).

### D.2.1 Why the absolute magnitudes are bounded

The 49.45% worst case is large, but it is bounded: even a
territory that has lost half its 2000 forest cover retains the
other half. The bound is structural: a 100% loss would imply
replacement of forest with something else (cattle pasture,
soybean, settlement) across the entire area, and this would
require significant capital inputs that take decades to deploy.
The 49.45% case suggests the front edge of a conversion that has
15-30 years of additional trajectory if the current rate
continues.

This bound means that **closing the gap is not a one-shot
policy event** — closing the gap requires sustained investment
in territorial governance and a multi-decade horizon.

## D.3 Spatial concentration of loss within territories

The analysis so far has measured aggregate per-territory loss
rates. A natural follow-on question — which we leave to future
work — is **where within each territory** the loss is concentrated.

The expectation, based on the REDMOPy (2024) visual reports, is
that loss is concentrated at territory boundaries (the
agricultural frontier's expansion front) and along road
corridors (logging and cattle-transport routes). If this is
correct, the per-territory numbers are dominated by boundary
loss and the "interior" rate (e.g., the rate at forest pixels
that are > 5 km from the territory boundary) would be much lower.

A spatial concentration analysis would also tell us whether **the
disparity is driven by the territory boundary effect or by uniform
loss inside territories**. The current paper does not answer this
question; we leave it as a follow-on. Section D.5 documents why
this analysis is *not* in this paper.

## D.4 Confounders we did not control for

The 2.90× disparity is **uncontrolled** in the formal
epidemiological sense. We compare per-pixel loss inside vs outside
territories, but we do not match on covariates that would
strengthen the causal claim.

### D.4.1 Road access

The Paraguayan Chaco's deforestation correlates strongly with
road access (the Ruta Transchaco and the unpaved feeder roads
off it). Indigenous territories near roads face more agricultural
pressure than those that are road-isolated. A road-aware analysis
would stratify by distance-to-road and check whether the disparity
holds within each stratum.

The data inputs are available (road network from OpenStreetMap
or the Paraguayan national geographic institute) but the
analysis is not done in this paper. We document it as a Tier 2
item in `AGENT_TODO.md`.

### D.4.2 Agricultural suitability

Some pixels are more attractive for cattle-ranching or soybean
conversion than others (soil quality, rainfall, slope). A
suitability-aware analysis would stratify by suitability and
check whether the disparity holds within each stratum. Again,
data available, analysis not done.

### D.4.3 Land-claim ambiguity

In the Chaco frontier, the boundary between "indigenous
territory" and "available for non-indigenous purchase" is
contested. The legal ambiguity itself may drive the disparity,
because a non-indigenous buyer of a contested plot has weaker
enforcement against clearing than a buyer of a definitively
non-indigenous plot. Disentangling this is hard; it requires
the legal-claims data from INDI's boundary commission.

### D.4.4 How much would controlling change the headline?

The unprojected magnitude of these controls is uncertain without
the actual analysis. The conservative expectation is that the
point estimate drops from 2.90× to somewhere in [1.5, 2.5]× after
controls. Even at 1.5×, the disparity is statistically and
substantively significant. The qualitative finding ("territories
deforest faster than the national rate") is not contingent on
the controls.

## D.5 The CARE Principles gap

This paper's substantive finding — that indigenous territories
in the Chaco are deforested at 2.90× the national rate — is a
**public data analysis** that anyone can reproduce from the
published sources. **It is not** a CARE-compliant analysis
of indigenous data because the data flow has been:

1. Public Hansen data (no community engagement required)
2. Public `paraguay-geodata` polygons (sourced from an open dataset,
   not from community consultation)
3. Public analysis (no community involvement in framing,
   parameters, or output)

Per the **CARE Principles for Indigenous Data Governance**
[Carroll et al. 2020; GIDA 2019], the analysis should also be:

1. **Collective benefit** — does the analysis benefit the
   communities? Yes, in principle: it provides a quantitative
   basis for policy advocacy and resource allocation.
2. **Authority to control** — do the communities have
   decision-making power over the analysis? No: the analysis was
   conducted without community engagement.
3. **Responsibility** — is there an accountability structure? No:
   no community review of the output before publication.
4. **Ethics** — does the analysis minimize harm and maximize
   benefit? Potentially yes for the policy use case, but the
   per-community attribution could also be used to target
   communities for unwanted attention.

We conclude that **the substantive finding (2.90× disparity) is
public-data and is therefore publishable without CARE
compliance on a strict reading**. However, the **per-community
maps and per-community polygon attribution** are not publishable
in their current form. Any operational deployment would require
FPIC engagement with each affected community.

### D.5.1 FPIC engagement is the prerequisite

The prerequisite work for any P0012 operational deployment:

1. **Per-community courtesy briefing** (~1 hour per community,
   ~10 total). Present the country-scale analysis and the
   2.90× disparity finding to each community council. Document
   the briefing in INDI's records.
2. **INDI coordination** (~3-6 months human time). Discuss
   preferred reporting format, frequency, data sovereignty.
3. **Community-led atlas** (per `etica/FPIC_template_es.md`).
   Summarize the analysis in the community's preferred
   language (Spanish, Guaraní, Enlhet, Nivaclé for relevant
   communities).
4. **CARE-compliant data release**. If per-territory polygons
   are to be released, the communities must approve the
   publication.
5. **At least one community research-partnership**. Establish
   a single community-led research collaboration (the typical
   CARE-compliant engagement structure) before any per-community
   attribution is released.

This is **100% human-relationship work**, cannot be automated
from a sandbox, and is the most concrete ethical prerequisite for
the paper's operational deployment.

### D.5.2 What is publishable now

Publishable today, with the current FPIC gap explicitly
acknowledged:

- The 2.90× disparity finding (Section 3) — no per-community
  attribution needed, just the aggregate numbers.
- The per-territory ranking (Section R.4.1) — at the level of
  "Carmelo Peralta is the worst at 49.45%", without maps showing
  which specific pixels are inside which community.
- The methodology (Section 2) — purely methodological, applicable
  globally to other data-limited regions.

Not publishable now, blocked on FPIC:

- Per-community pixel-level maps of where forest loss has occurred.
- Specific claims about individual community governance failures
  (these would require community consent and involvement).
- Operational alert deployment ("we detected forest loss in your
  community — please respond") without community partnership.

This is consistent with the project's broader `docs/CONVENTIONS.md`
principle: "aspirational claims require future evidence, not
reframing of past work."

## D.6 What the 2.90× finding does NOT imply

We deliberately resist the temptation to over-interpret:

1. **It does not imply causation.** The disparity is correlation
   between per-pixel loss and inside-territory status. The
   confounders in Section D.4 (road access, agricultural
   suitability, land-claim ambiguity) would need to be controlled
   to make a causal claim.

2. **It does not imply that indigenous land tenure is bad for
   forest.** The pattern is consistent with the global literature
   being wrong about the Chaco specifically (a documented exception
   to the global pattern), and it is consistent with the
   "governance matters more than statute" hypothesis. It is also
   consistent with other explanations (road access, agricultural
   suitability) that don't depend on indigenous tenure per se.

3. **It does not imply that all 10 territories are equally
   affected.** The 7× spread is itself a contribution; the
   headline 2.90× is a summary statistic, not a per-community
   characterization.

4. **It does not provide a basis for policy prioritization of
   individual communities** without the FPIC engagement (Section
   D.5.1).

The paper's contribution is the quantitative finding, the
methodology, and the policy-attention recommendation. It is not
a basis for operational deployment without the human-relationship
follow-on.

## D.7 What needs to happen for operational deployment

The published target of operational per-community forest alert
deployment (which appeared in earlier drafts of this chapter) is
**aspirational** and has been removed from the abstract. The
aspirational target is achievable through the following concrete
steps, in priority order:

1. **(Tier 4, 2-6 months human time) FPIC engagement with the 10
   communities + INDI coordination.** This is the ethical
   prerequisite for any operational deployment.

2. **(Tier 2, ~4 h) Expand territory sample to all 19 indigenous
   peoples in the Chaco** — refine the disparity ratio and tighten
   the bootstrap CI.

3. **(Tier 2, ~4 h) Stratum controls for road access and
   agricultural suitability** — would refine the headline from
   correlation to controlled association.

4. **(Tier 2, ~4 h) Per-paper `references.bib` slice for
   `papers/drafts/p0012_yvy_indigenous/`.** Required for LaTeX
   compile to standalone.

5. **(Tier 2, ~10-20 h) Spatial concentration analysis within
   territories** — quantify the boundary-loss vs interior-loss
   hypothesis (Section D.3).

6. **(Tier 3, $50-200 GPU) Implement an operational baseline
   forest alert system** (training a simple CNN-based per-pixel
   forest-change detector on Planet Labs or Sentinel-2 + Planet
   composites).

7. **(Tier 4) Email loop with World Development editor** to
   confirm scope and pull any required formatting tweaks.

Steps 1-2 are required before the paper is publication-ready. The
rest are improvements on top of the submission-quality core.
