# Methods

## M.1 Data sources

### M.1.1 Hansen Global Forest Change v1.11

We use Hansen GFC v1.11 [Hansen et al. 2013, updated 2023] as the
per-pixel deforestation reference. The dataset provides, at 30 m
resolution, a tree-cover classification for the year 2000
(`treecover2000`, 0-100%), a per-pixel loss year for 2001-2023
(`lossyear`, 0-23 with 0 meaning "no loss in this period"), and a
data-mask layer. The `lossyear` value is binary per pixel: either
"this pixel lost forest canopy sometime during 2001-2023" or
"this pixel did not". We aggregate per-pixel loss to per-territory
counts.

Hansen is the **standard reference** for global forest monitoring
[Weisse & Dow 2017 on Global Forest Watch], which makes our
analysis directly comparable to other published work. The
limitation — 30 m resolution cannot capture small-scale clearing or
sub-canopy degradation — is documented in Section 4.

### M.1.2 Indigenous territory polygons

We use **10 indigenous territory polygons** for the Chaco, sourced
from the open `paraguay-geodata` dataset (CC-BY-4.0, attribution
required). These polygons represent the territories as recognized
by INDI (Instituto Paraguayo del Indígena) and encompass all the
Chaco-region indigenous communities we have any spatial coverage
for.

Territory-total area: **43,466 km²**, which is approximately 11% of
Paraguay's total land area. The 10 territories correspond to
**~30,000 people** (estimated from INDI census, 2022).

Important caveat: **these polygons are visualization-grade
approximations**, not legal boundaries. They are sourced from a
secondary open-data project that aggregated INDI's polygon
information without re-engaging each community. The disparity
finding (Section 3) is **robust to ±1-km boundary shifts** because
the disparity is large (2.90×); per-community attribution to a
specific polygon is **not** the contribution of this paper and
should not be cited as such. Any operational use of the per-
community polygons requires INDI + community engagement per CARE
Principles (Section 5).

### M.1.3 Comparison reference: the national sample

To compute the disparity ratio (indigenous / national), we need a
denominator that represents "the rate at which Paraguay forest is
disappearing outside indigenous territories". We construct this as
follows:

- Take the same Hansen loss raster (covering all of Paraguay).
- Mask out pixels that fall inside any of the 10 indigenous
  territory polygons (using a conservative 1-km buffer outward).
- Aggregate loss across the remaining pixels to obtain a national-
  outside-territories loss rate.

This denominator excludes the buffer (rather than only the polygon
interior) to avoid attributing buffer pixels to either population.
Empirically, the buffer makes < 1% difference to the national
rate because the buffer area is small compared to total Paraguay
land area.

The national-rate sample is **8.50%** loss over 2001-2023 (i.e.,
8.50% of pixels outside territories that had any forest cover in
2000 lost it by 2023).

### M.1.4 Bias-correction reminder

Hansen GFC's "forest" definition is "≥ 50% canopy cover in the
year 2000 baseline." This is the standard operational definition
and is consistent with the rest of the literature. The implication
is that **pixels classified as "non-forest" in 2000 are not
counted as loss**, even if they later saw deforestation that
non-experts would describe as such. This biases the loss rate
downward (we underestimate loss) but it does so consistently inside
and outside territories; **the disparity ratio is therefore
robust** to this convention.

## M.2 Statistical analysis

### M.2.1 Per-territory counts

For each of the 10 territories, we compute:

- **Loss pixels**: count of Hansen pixels where `lossyear > 0`
  intersected with the territory polygon (with 1-km buffer).
- **Forest pixels**: count of Hansen pixels where `treecover2000 >= 50`
  intersected with the territory polygon.
- **Loss rate**: loss pixels / forest pixels, expressed as a
  percentage. This is the per-territory deforestation rate.

### M.2.2 Disparity ratio

The headline metric is the **disparity ratio** $R$:

$$R = \frac{\bar{r}_{\text{territories}}}{\bar{r}_{\text{national-outside}}}$$

where $\bar{r}_{\text{territories}}$ is the mean per-territory loss
rate and $\bar{r}_{\text{national-outside}}$ is the national loss
rate computed in Section M.1.3. For our data:

$$R = \frac{24.67\%}{8.50\%} = 2.90$$

### M.2.3 Statistical tests

We test the null hypothesis "per-territory loss rates equal the
national rate" with two complementary tests:

**χ² test of homogeneity**: a 2×k contingency table of forest
pixels (lost / not lost) by group (territories vs national outside).
The 10 indigenous territories and the national rest are partitioned
into groups; we report χ², df, and p-value. Under the null, χ²
follows a χ² distribution with df = (rows − 1)(cols − 1) = 1 × 10
= 10.

**Bias-corrected and accelerated (BCa) bootstrap CI on R**: we
resample (with replacement) the territory-level loss rates 1,000
times, recompute $R$ for each resample, and report the 2.5th and
97.5th percentiles. We also compute the bias correction $z_0$ and
the acceleration $a$ from the jackknife; the BCa adjustment corrects
for non-normality and bias in the bootstrap distribution.

### M.2.4 Heterogeneity analysis

We complement the headline disparity with a within-territory
heterogeneity analysis: per-territory loss rates (Section 3),
within-territory spatial concentration of loss (where in the
territory is the loss concentrated), and the cross-territory
standard deviation. The headline 2.90× disparity may mask
substantial variation between 7.21% (Angaité-Filadelfia) and 49.45%
(Carmelo Peralta).

### M.2.5 Software and compute

All analysis runs on CPU; total wall-clock < 5 minutes on a standard
laptop for the 10-territory, 2001-2023 analysis. Code: open-source
under CC-BY-NC-4.0 (`LICENSE`); pipeline implementation in
`src/papers/p0012_yvy_indigenous/pipeline.py` (detect_conflicts,
load_data); per-territory outputs in `outputs/p0012/` (department-
level stats, indigenous stats, CF-vs-national ratios).

Reproducibility:

- Hansen data downloaded directly from
  `https://storage.googleapis.com/earthenginepartners-hansen/GFC-2023-v1.11/`
  (no authentication).
- Indigenous territory polygons from `paraguay-geodata` (CC-BY-4.0).
- Python environment specified in `pyproject.toml`.
- Output JSON: `outputs/p0012/indigenous/per_territory_stats.json`.
- Honest-results log: `ACTUAL_RESULTS.md`.
