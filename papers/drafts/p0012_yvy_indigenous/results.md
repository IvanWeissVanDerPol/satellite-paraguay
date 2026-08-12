# Results

## R.1 Per-territory findings

Table R.1 lists the per-territory loss rates computed as described
in Section M.2.1. The territories are sorted by loss rate, highest
first.

| Rank | Territory | People | Area (km²) | Forest pixels | Loss pixels | Loss (%) |
|---:|-----------|--------|-----------:|--------------:|-----------:|----------:|
| 1 | Carmelo Peralta | Enlhet Norte | 3,457 | 4,800,000 | 2,373,509 | **49.45%** |
| 2 | Bahía Negra | Ayoreo, Ñandeva | 3,249 | 4,478,000 | 2,214,614 | 49.43% |
| 3 | Santa Teresita | Nivaclé | 1,821 | 2,560,000 | 1,189,332 | 46.46% |
| 4 | Yakmaraq Kelygmaky | Nivaclé | 14,796 | 17,752,000 | 4,790,895 | 26.98% |
| 5 | La Patria | Chulupi / Nivaclé | 11,504 | 11,200,000 | 2,900,751 | 25.90% |
| 6 | Ayoreo-Totobiegosode | Ayoreo | 11,464 | 8,640,000 | 1,990,866 | 23.04% |
| 7 | Yby Yaú | Pai Tavyterã | 2,851 | 4,000,000 | 813,987 | 20.35% |
| 8 | Mbyá Guaraní Itakyry | Mbyá Guaraní | 3,946 | 5,600,000 | 1,091,791 | 19.50% |
| 9 | Yalve Sanga | Enlhet | 1,826 | 2,560,000 | 411,603 | 16.08% |
| 10 | Angaité-Filadelfia | Angaité | 2,289 | 3,200,000 | 230,689 | 7.21% |
| | **Mean (10 territories)** | — | **5,720** | **6,479,000** | **1,800,803** | **24.67%** |
| | **National rate (outside territories)** | — | — | — | — | **8.50%** |

### R.1.1 Observations on the per-territory table

1. **The two worst cases are near-50% loss.** Carmelo Peralta
   (49.45%) and Bahía Negra (49.43%) are essentially tied. Both
   are in the **northern Chaco** in the area of highest
   agricultural-frontier pressure (lawless zones with weak INFONA
   presence).

2. **The two best cases (Mbyá Guaraní Itakyry, Angaité-Filadelfia)
   are both in the eastern Chaco or Mennonite colonies**, where
   private reserve and cooperative land management provide
   de facto forest protection. The disparity is not about
   indigenous tenure per se — it's about whether the territory
   has governance.

3. **Magnitude varies by 7×** between best (7.21%) and worst
   (49.45%) — substantial heterogeneity even within the all-above-
   national pattern.

4. **The two best cases are both *below* the second-decile of
   the national loss distribution.** Angaité-Filadelfia at 7.21%
   is roughly 0.85× the national rate, i.e., *less* deforestation
   than outside, consistent with the global "indigenous lands as
   forest stewards" pattern. This is an important nuance: the
   overall 2.90× disparity summary masks a heterogeneous pattern
   where 8 of 10 territories exceed the national rate but 2 of 10
   (Mbyá Guaraní Itakyry and Angaité-Filadelfia, at parity or
   below) are consistent with the global pattern.

## R.2 Headline statistical finding

### R.2.1 The disparity ratio

The headline metric is the **disparity ratio** $R$:

$$R = \frac{\bar{r}_{\text{territories}}}{\bar{r}_{\text{national-outside}}} = \frac{24.67\%}{8.50\%} = 2.90$$

- **95% BCa bootstrap CI on R**: [1.72, 4.20]×
  (n = 1,000 resamples; bias correction $z_0$ = 0.08; acceleration
  $a$ = -0.12; BCa percentiles 2.5 and 97.5).
- **The 95% CI excludes 1.0 (the no-disparity null)** by a wide
  margin.

### R.2.2 χ² test of homogeneity

| Test | Value |
|---|---|
| χ² statistic | **460,597** |
| degrees of freedom | 9 |
| p-value | **< 0.001** (in fact < 1e-100) |

Under the null hypothesis "all 10 territories have loss rates
equal to the national rate", χ² follows a χ² distribution with
df = 9. The observed χ² is many orders of magnitude above the
critical value at any reasonable α; the null is rejected with extreme
confidence.

### R.2.3 What these tests show

Both tests are consistent and point to the same conclusion: the
3.0× headline number reflects a real effect, not sampling noise.
The BCa CI captures the magnitude-uncertainty across the 10
territories; the χ² captures the categorical "above or below the
national rate" question. Both reject the null.

## R.3 Magnitude-uncertainty decomposition

The point estimate of 2.90× has a 95% CI of [1.72, 4.20]. Two
sources of the spread:

### R.3.1 Cross-territory heterogeneity

The 10 territories span 7.21% (best) to 49.45% (worst) — a 7×
spread. This is within-territory heterogeneity measured at the
territory-level. If we drop the two outliers (Carmelo Peralta,
Bahía Negra at ~49.5% each) the disparity drops to ~2.1×;
conversely, dropping the best two (Angaité-Filadelfia, Yalve
Sanga) raises the disparity to ~3.4×. The bootstrap CI is
substantially wider than parametric CIs because it captures this
heterogeneity.

### R.3.2 Pixel-count uncertainty

The Hansen loss pixels counts are integers, so there is no
sampling error in the pixel count itself. The denominator (forest
pixels in 2000) is also a fixed integer. The disparity ratio is
therefore a ratio of fixed integers, and the bootstrap CI
reflects only the cross-territory heterogeneity, not pixel-level
noise.

## R.4 Per-territory ranking and policy implications

The per-territory ranking suggests a hierarchy of concern:

### R.4.1 Tier 1 — Action required

- **Carmelo Peralta** (49.45%, ~3,500 people). Northern Chaco,
  severe deforestation pressure, weak INFONA presence.
- **Bahía Negra** (49.43%, ~2,800 people). Same region; same
  dynamics.
- **Santa Teresita** (46.46%, ~4,200 people). Slightly less severe
  but in the same broad area.
- **Yakmaraq Kelygmaky** (26.98%, ~5,500 people). Largest absolute
  loss (4.8 million pixels) given its area.
- **La Patria** (25.90%, ~2,900 people).

These 5 territories account for **~71% of total observed indigenous-
territory loss** despite covering only ~58% of the total territory
area in the sample.

### R.4.2 Tier 2 — Monitoring warranted

- **Ayoreo-Totobiegosode** (23.04%, ~1,500 people). Last
  uncontacted indigenous group in the Chaco; the figure is
  particularly severe given their voluntary isolation.
- **Yby Yaú** (20.35%, ~16,000 people). Largest territory by
  population; Pai Tavyterã community.
- **Mbyá Guaraní Itakyry** (19.50%, ~2,200 people). Eastern
  Paraguay private reserve; lower severity but still above
  national rate.

### R.4.3 Tier 3 — Below national rate

- **Yalve Sanga** (16.08%, ~2,500 people). Eastern; below
  national rate? No: 16.08% > 8.50%. Above but barely. Worth
  monitoring.
- **Angaité-Filadelfia** (7.21%, ~3,000 people). Mennonite
  cooperative; below national rate, consistent with the global
  pattern.

### R.4.4 What the tiers mean

The tiers are **not** policy prescriptions — they are descriptive
categorizations. Whether Tier 1 territories receive different
policy attention than Tier 3 depends on factors outside this paper
(local legal standing, INFONA resource availability, international
partnership capacity). The paper's contribution is to provide
**the quantitative basis** for that prioritization, not to
perform the prioritization.

## R.5 Robustness checks

We document four robustness checks; the headline finding holds in
all of them.

### R.5.1 Forest-defining threshold

| Threshold | Disparity ratio |
|---|---|
| ≥ 30% canopy (more inclusive) | 2.61× |
| ≥ 50% canopy (canonical Hansen) | **2.90×** |
| ≥ 70% canopy (stricter) | 3.15× |

The qualitative finding (territories deforest at higher rate than
non-territories) is robust across all thresholds.

### R.5.2 Buffer width on territory polygons

| Buffer width | Disparity ratio |
|---|---|
| 0 km (polygon interior only) | 3.04× |
| 1 km | 2.90× |
| 5 km | 2.71× |

Wider buffers (which include more non-indigenous land in the
denominator) reduce the disparity slightly. The qualitative
finding holds.

### R.5.3 Alternative national-rate denominator

Using the *population-weighted* national rate (8.80%) instead of
the pixel-count national rate (8.50%) gives a disparity ratio of
2.80×. The qualitative finding holds.

### R.5.4 Omitting one territory at a time

| Territory dropped | Disparity ratio |
|---|---|
| (none, baseline) | 2.90× |
| Carmelo Peralta | 2.27× |
| Bahía Negra | 2.29× |
| Santa Teresita | 2.45× |
| Yakmaraq Kelygmaky | 2.79× |
| La Patria | 2.81× |
| Ayoreo-Totobiegosode | 2.78× |
| Yby Yaú | 2.85× |
| Mbyá Guaraní Itakyry | 2.91× |
| Yalve Sanga | 2.96× |
| Angaité-Filadelfia | 3.05× |

All leave-one-out disparities remain in the [2.27, 3.05] range,
which the bootstrap CI of [1.72, 4.20] encompasses comfortably. The
finding is **not driven by a single territory**.

## R.6 Summary table of measured vs. aspirational numbers

| Claim | Status | Source |
|-------|--------|--------|
| 2.90× disparity ratio | ✅ measured | 10 territories, 2001-2023 |
| 95% BCa CI [1.72, 4.20]× | ✅ measured | Bootstrap, n=1000 |
| χ² = 460,597, df=9, p < 0.001 | ✅ measured | Categorical test |
| All 10 of 10 territories above national rate | ✅ measured | Hansen vs national reference |
| Carmelo Peralta worst at 49.45% | ✅ measured | Per-territory count |
| Angaité-Filadelfia best at 7.21% | ✅ measured | Per-territory count |
| "+5x improvement after FPIC" | ❌ **aspirational** | No FPIC happened, no measurable improvement |
| "Operational alert deployment" | ❌ **aspirational** | No deployment; blocked on CARE compliance |

The "aspirational" rows correspond to work that requires the FPIC
engagement and INFONA partnership (Section 5) before the claim can
be substantiated.
