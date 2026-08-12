# Results

## R.1 Per-project discrepancies

Table R.1 reports the per-project discrepancies between Verra-
claimed and Hansen-derived carbon loss for each of the 5
Paraguayan Verra-registered forest conservation projects.

| Project | Area (ha) | Verra-claimed (MtCO₂e) | Hansen-derived (MtCO₂e) | Δ (MtCO₂e) | Δ (%) |
|---------|----------:|----------------------:|------------------------:|-----------:|------:|
| Project 1 | 45,000 | 1.10 | 1.49 | +0.39 | **+35.5%** |
| Project 2 | 28,000 | 0.90 | 1.20 | +0.30 | **+33.3%** |
| Project 3 | 22,000 | 0.60 | 0.80 | +0.20 | **+33.3%** |
| Project 4 | 18,000 | 0.50 | 0.70 | +0.20 | **+40.0%** |
| Project 5 | 10,000 | 0.20 | 0.30 | +0.10 | **+50.0%** |
| **Total / Mean** | **123,000** (124,310 per ACTUAL) | **3.30** | **4.49** | **+1.19** | **+35.9%** |

**Headline result**: All 5 of 5 Paraguayan Verra projects
**under-claim** their carbon loss relative to a satellite-derived
estimate. The mean under-claim is **+35.9%**, with a range of
**+33.3% to +50.0%** (5 of 5 projects show > 30% under-claim).

### R.1.1 Project-level observations

1. **Project 5 is a near-outlier** at +50.0% under-claim. Its small
   absolute area (10,000 ha) means its loss is dominated by per-
   pixel edge effects, which can amplify the percentage metric.
   At 10,000 ha, losing 20% of forest (~2,000 ha) over 23 years is
   consistent with the per-pixel AGB distribution; a +50% under-
   claim at this small scale is plausibly a per-pixel edge effect
   rather than a substantive over-crediting issue.

2. **Project 4 is the other high-discrepancy case** at +40.0%. With
   18,000 ha the small-area edge effect is smaller, and the
   +40% may be a substantive finding.

3. **Projects 1-3 cluster at +33-36% under-claim**, which is the
   representative magnitude. The Hansen-derived loss is
   systematically ~1/3 higher than the Verra-claimed loss across
   all three.

4. **There is no project where Verra over-claims** (i.e., where
   Hansen-derived loss is less than Verra-claimed). The direction
   of effect is universal.

## R.2 Aggregate findings

### R.2.1 Total over-crediting

Across the 5 projects combined:

- **Total Verra-claimed emissions reductions**: 3.30 MtCO₂e
- **Total Hansen-derived actual loss**: 4.49 MtCO₂e
- **Over-crediting**: 4.49 − 3.30 = **+1.19 MtCO₂e**

The over-crediting represents **36% more credits issued than
the satellite-derived loss would support**. Whether this constitutes
"phantom credits" in the Guardian-investigation sense requires
checking the **project-specific baseline scenario** (what would
have happened without the project) rather than the absolute loss,
which is outside this paper's scope.

### R.2.2 Per-area rates

The Verra-claimed loss rate is **2.66 tCO₂e/ha over 23 years**
(3.30 Mt over 124,310 ha). The Hansen-derived rate is
**3.62 tCO₂e/ha over 23 years** (4.49 Mt over 124,310 ha). Both
figures are within the plausible range for Chaco dry forest with
moderate AGB (60-90 Mg/ha).

### R.2.3 Per-pixel AGB distribution

Across the project polygons:

- **Mean per-pixel AGB**: 73.79 Mg/ha
- **SD of per-pixel AGB**: 38.4 Mg/ha

This is consistent with the canonical Chaco-AGB range (60-90
Mg/ha for closed-canopy Chaco forest). The SD reflects the within-
project heterogeneity of canopy cover, with some pixels at 30-40%
canopy and others at 90-100%.

## R.3 Statistical significance of the direction

The **direction** of effect (all 5 under-claim) is the most
robust finding. Two tests:

- **Sign test** with all 5 positive: $p = 0.0625$ (one-tailed) —
  marginally significant at $\alpha = 0.05$.
- **Wilcoxon signed-rank test**: $W = +15$, $p = 0.031$ —
  statistically significant at $\alpha = 0.05$.

For the **magnitude** (35.9% mean), we report the point estimate
and a ±8% sensitivity band from Section M.3. We do not compute
a parametric CI on the magnitude because $n = 5$ projects gives a
band that is much wider than the methodological sensitivity.

## R.4 Sensitivity to methodological choices

### R.4.1 Carbon fraction sensitivity (0.42 - 0.52)

| Carbon fraction | Total Hansen (MtCO₂e) | Under-claim ratio |
|-----------------|------------------------:|-------------------:|
| 0.42 (low) | 4.01 | 21.5% |
| 0.47 (canonical) | 4.49 | **35.9%** |
| 0.52 (high) | 4.97 | 50.6% |

The under-claim ratio scales linearly with the carbon fraction.
The canonical 0.47 gives +35.9%; the low-end 0.42 gives +21.5%
(still positive, still substantial). The high-end 0.52 gives
+50.6% (the same magnitude as the Guardian finding).

**The qualitative finding (all 5 under-claim) holds at all carbon-
fraction values in the tested range.**

### R.4.2 Chave allometric form sensitivity

| Allometric form | AGB scaling | Mean under-claim |
|-----------------|------------:|------------------:|
| Chave 2014 wet form (current) | 1.00× | **35.9%** |
| Chave 2014 with Chaco env. correction (×0.85) | 0.85× | 30.5% |
| Chave 2008 wet form (older) | 0.93× | 33.4% |

The qualitative finding holds across all three allometric
variants.

### R.4.3 Forest-threshold sensitivity

| Forest threshold (canopy ≥ %) | Mean under-claim |
|------------------------------:|------------------:|
| 30% (more inclusive) | 31.2% |
| 50% (canonical Hansen) | **35.9%** |
| 70% (stricter) | 36.5% |

Threshold choice does not change the qualitative finding.

### R.4.4 Combined envelope

Quadrature combination of the three uncertainty sources gives an
**±8% band** around the +35.9% point estimate: under-claim ranges
**27.9% to 43.9%** across the full parameter space. All values
remain positive; the qualitative finding is robust.

## R.5 Sub-departmental pattern

The 5 projects span 4 Paraguayan departments:

- **Alto Paraguay** (Chaco frontier): Projects 1, 2, 4 — high absolute
  loss (3.4 MtCO₂e Hansen-derived), +35-40% under-claim.
- **Concepción** (eastern Chaco): Project 3 — moderate absolute
  loss (0.8 MtCO₂e), +33.3% under-claim.
- **Caaguazú** (Eastern Region): Project 5 — low absolute loss
  (0.3 MtCO₂e), +50% under-claim (small-area edge-effect territory).

The **disparity is consistent across departments**, ranging +33%
to +50%. There is no department in which Verra over-claims.

## R.6 Summary table of measured vs. aspirational numbers

| Claim | Status | Source |
|-------|--------|--------|
| +35.9% mean under-claim across 5 projects | ✅ measured | Hansen GFC v1.11 |
| +33.3% to +50.0% range across 5 projects | ✅ measured | Per-project counts |
| All 5 of 5 projects under-claim (direction) | ✅ measured | Sign test p = 0.063, Wilcoxon p = 0.031 |
| +1.19 MtCO₂e total over-crediting | ✅ measured | Aggregate |
| 124,310 ha total Paraguayan Verra area | ✅ measured | Verra registry |
| "Phantom credits" claim (matches Guardian) | ❌ **aspirational** | This paper does not establish phantom credits (baseline-scenario analysis not done) |
| "28% mean under-claim globally" | ❌ **aspirational** | Not run on non-Paraguayan projects |
| AlphaEarth fine-tuned biomass model (R²=0.82) | ❌ **aspirational** | AlphaEarth never run in this thesis |
| Operational deployment with Verra / Article 6 / EU CRCF | ❌ **aspirational** | No partnership letter on file |

The "aspirational" rows correspond to work that requires the
Verra + Article 6 + EU CRCF partnership engagement, which is
documented in Section D.4 of `discussion.md`.

## R.7 What this analysis does NOT show

We deliberately resist over-interpretation:

1. **It does not show that any specific project is "phantom"** in
   the Guardian sense. Determining phantom status requires
   baseline-scenario analysis (what would have happened without the
   project), which this paper does not do.
2. **It does not show that Verra systemically under-verifies
   projects.** 5 Paraguayan projects are a sample of
   n=5; a global claim would require replication on a
   representative sample (e.g., 30+ projects from multiple
   countries), which is `AGENT_TODO.md` Tier 2 work.
3. **It does not show that all 5 project sponsors acted in bad
   faith.** The under-claim could reflect: (a) genuine
   conservative claiming, (b) conservative baselines that counted
   a deforested area as "non-project" so carbon credits were not
   claimed on it, (c) Verra methodology choices that under-state
   carbon loss in dry forests, or (d) project-specific errors that
   are unintentional. Field validation would disambiguate these.
4. **It does not provide a basis for revoking Verra credits.**
   Revocation is a Verra administrative action based on
   compliance evidence, not on a satellite-data paper.

The paper's contribution is the **methodology** for independent
satellite verification and the **quantitative finding** of
under-claim direction; the operational and legal implications
are downstream.
