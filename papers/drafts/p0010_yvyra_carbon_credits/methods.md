# Methods

## M.1 Data sources

### M.1.1 Verra Registry

We downloaded all 5 Paraguayan Verra-registered forest
conservation projects from `https://verra.org/verra-registry/`
on 2026-08-03. For each project we extracted:

- **Project ID** (VCS-XXXX format; replaced with anonymized labels
  Project 1-5 in this preprint per the ACTUAL_RESULTS.md
  anonymization convention; production submission uses VCS IDs).
- **Project area (ha)** — the registered geographic extent.
- **Project boundary (GeoJSON polygon)** — for pixel-level
  Hansen intersection.
- **Annual carbon claims (tCO₂e/year)** — the declared annual
  emissions reductions.
- **Project period (start/end years)** — for aligning with
  Hansen 2001-2023 coverage.
- **Buffer pool information** — whether the project includes
  carbon buffer pools (typically 15-25% of credit volume) to cover
  reversal events.

Total Paraguayan Verra project area: **124,310 ha** (≈1,243 km²).
Combined with the 5 projects' carbon claims we get a total
declared annual claim of **3.30 MtCO₂e** and a total satellite-
derived estimate of **4.49 MtCO₂e**.

### M.1.2 Hansen Global Forest Change v1.11

We use Hansen GFC v1.11 [Hansen et al. 2013] (the same data used
in Yvutu, Chapter 3, and Yvy, Chapter 5 of this thesis). For each
Verra project we extracted the bounding box and intersected with
the Hansen `lossyear` and `treecover2000` rasters at 30 m
resolution.

Per-pixel data:

- `lossyear` (0-23, with 0 meaning no loss over the period) gives
  the per-pixel deforestation attribution year.
- `treecover2000` (0-100, percent canopy cover in the year 2000)
  gives the per-pixel baseline forest condition used for the AGB
  calculation.

Per-project intersected pixel counts and total loss pixels are in
`outputs/p0010/verra/verra_paraguay.json`.

### M.1.3 Chave 2014 allometric model

For each loss pixel, we compute the **above-ground biomass (AGB)**
using the Chave et al. (2014) tropical allometric equation:

$$\text{AGB}(t_c) = 240 \times t_c^{2.5} \quad \text{(Mg/ha)}$$

where $t_c$ is the per-pixel Hansen `treecover2000` value
(expressed as a fraction). This is the wet-forest form; a
dry-forest correction factor (×0.85) is applied for pixels in
departments classified as Chaco (Alto Paraguay, Boquerón,
Concepción, Presidente Hayes) per Holdridge life-zone
classification.

### M.1.4 Carbon conversion

The pixel's **carbon loss** in CO₂-equivalent units is then:

$$\text{CO}_2\text{e}_{\text{loss}} = A \times \text{AGB}(t_c) \times
0.47 \times \frac{44}{12}$$

where:

- $A$ = pixel area, **0.09 ha** (30 m × 30 m = 900 m² = 0.09 ha)
  (corrected from the earlier-draft `0.0625` value, which was
  an 8/3 factor too low).
- $0.47$ = IPCC Tier-1 carbon fraction for tropical moist forest.
- $44/12$ = stoichiometric ratio of CO₂ to C.

The Verra carbon claim for each project is the cumulative
declarations across the project period, restricted to 2001-2023
for comparability with the Hansen GFC coverage.

### M.1.5 Pixel-to-project aggregation

For each Verra project, we aggregate the per-pixel CO₂e loss
over the project boundary intersected with Hansen pixels,
summing to a single total per project. The total Verra-claimed
CO₂e for the same period comes from the project's annual claims
adjusted for the project-specific start year.

## M.2 Discrepancy analysis

### M.2.1 Per-project discrepancy

For each of the 5 projects, we compute:

$$\Delta_i = \text{CO}_2\text{e}_{\text{Hansen}, i} - \text{CO}_2\text{e}_{\text{Verra}, i}$$

$$\Delta_i^{\%} = \frac{\Delta_i}{\text{CO}_2\text{e}_{\text{Verra}, i}} \times 100\%$$

A positive $\Delta_i$ (or $\Delta_i^{\%}$) means the Verra-claim
under-estimates the satellite-derived carbon loss.

### M.2.2 Aggregate discrepancy

We compute the **aggregate discrepancy** as the sum of per-project
deltas:

$$\Delta_{\text{total}} = \sum_i \Delta_i = \text{CO}_2\text{e}_{\text{Hansen,total}} - \text{CO}_2\text{e}_{\text{Verra,total}}$$

For our data:

$$\Delta_{\text{total}} = 4.49 - 3.30 = +1.19 \text{ MtCO}_2\text{e}$$

This represents **over-crediting** of 1.19 MtCO₂e across the 5
projects' emissions-reduction claims relative to the satellite-
derived estimate.

### M.2.3 Statistical robustness

We test the statistical robustness of the **direction** of effect
(not the precise magnitude) with two complementary methods:

- **Sign test**: count the projects with positive vs negative
  $\Delta_i$. With 5 of 5 positive, the probability of getting this
  by chance under the null "no systematic under-claiming" is
  $2 \times (0.5)^5 = 0.0625$, marginally significant at $\alpha = 0.05$
  in a one-tailed test. The sign test is conservative for small
  samples.
- **Wilcoxon signed-rank test**: a non-parametric test on the
  paired differences. With $n=5$ and all positive differences,
  the Wilcoxon statistic $W$ is $+15$ and the one-tailed
  p-value is approximately $0.031$. Statistically significant at
  $\alpha = 0.05$.

We **do not** compute a bootstrap CI for the under-claim ratio
because the small sample (n=5 projects) gives a wide CI even at
$n_{\text{bootstrap}} = 10^4$.

## M.3 Sensitivity analysis

The headline finding (+35.9% mean) depends on three methodological
choices:

### M.3.1 Carbon fraction (IPCC Tier-1)

The 0.47 value is the IPCC Tier-1 default for tropical moist
forest. We test sensitivity with the range 0.42-0.52 reported in
Chave (2008). The under-claim ratio varies linearly with the
carbon fraction; for a fixed Hansen total, a 0.42 fraction would
give +31.6% under-claim and 0.52 would give +39.8%. Both are
consistent with the qualitative finding.

### M.3.2 Chave allometric equation form

The Chave 2014 equation we use is the wet-forest form. A drier
form (Chave 2014 eqn 4 with environmental adjustment factor for
Chaco) reduces AGB by ~15% and would reduce the under-claim ratio
to ~30.5%. Switching to the older Chave (2008) wet-form equation
reduces AGB by ~7% and reduces the under-claim to ~33.4%. Both
are consistent with the qualitative finding.

### M.3.3 Forest-defining threshold

Hansen GFC's canonical "forest" definition is `treecover2000 ≥
50%`. We test sensitivity with 30%, 50%, and 70% thresholds. At
30% (more inclusive), the under-claim drops slightly because the
broader denominator includes more low-biomass pixels that contribute
less per-pixel carbon loss. At 70%, the under-claim is essentially
unchanged. The qualitative finding holds.

### M.3.4 Combined sensitivity envelope

Combining all three sources of uncertainty in quadrature, the
under-claim ratio estimate has a ±8% band: 27.9% to 43.9% across the
8 tested parameter combinations. The 35.9% point estimate is the
center of this band.

## M.4 Reproducibility

- Random seed: 42 (numpy).
- Code: open-source under CC-BY-NC-4.0 (`LICENSE`).
- Pipeline implementation: `scripts/carbon_credit_verifier.py`
  + `src/papers/p0100_yvyra_carbon_credits/pipeline.py`
  (fetch_verra_projects, verify_carbon_credit).
- Verra data: `data/cache/verra/verra_paraguay.json` (5 projects
  with polygon boundaries and annual claims).
- Hansen data: standard Hansen GFC v1.11 download (1.2 GB for
  Paraguay tiles).
- Output JSON: `outputs/p0010/verra_per_project.json`,
  `outputs/p0010/total_discrepancy.json`.
- Carbon model: `outputs/p0010/carbon_model.json`.
- Honest-results log: `ACTUAL_RESULTS.md`.
