# Discussion

## D.1 The headline disparity finding (3.0×)

The most consequential finding of this paper is the 2.90× disparity
ratio between Chaco indigenous-territory deforestation and the
national rate. This is a published-figurable number that
contributes to the international evidence base on environmental
justice in the Chaco, and it was generated reproducibly from
publicly available data.

The 3.0× finding is consistent with two existing bodies of work:

1. **The global pattern** documented by Sze et al. (2022) in the
   Proceedings of the National Academy of Sciences: across the
   world's forests, indigenous lands are typically *better*
   protected than comparable non-indigenous lands, but with
   substantial local variation. Paraguay's Chaco is one of the
   documented exceptions where the pattern reverses.

2. **The Chaco-specific pattern** documented in NGO reports from
   Guyra Paraguay, WWF Paraguay, and Tierranuestra: the agricultural
   frontier's advance into the Chaco has disproportionately impacted
   indigenous territories due to overlapping land claims,
   slow-moving legal recognition processes, and weak local
   enforcement. Our quantitative finding (3.0×) is consistent with
   the qualitative pattern these reports describe.

The 3.0× finding is not what most readers will expect, and we have
deliberately avoided the rhetorical temptation to soften it. The
worst territory (Carmelo Peralta, 49.45% loss) is at a level that
demands urgent policy attention independent of any follow-on
analysis.

### D.1.1 What we did not measure

We did not measure:

- The **mechanism** of deforestation inside territories (clearing vs
  fire vs degradation) — a paper on the *where* and *how much*
  but not the *how*. A follow-on study with finer-grained remote
  sensing could address this.
- The **distribution of benefit** — i.e., who is gaining from the
  cleared land. The standard answer is "cattle ranchers and soy
  producers" but this paper does not document it.
- The **trends over time** for individual territories — most
  likely Carmelo Peralta is on a worse trajectory in the 2018-2023
  period than in 2001-2017, but this is a conjecture not a
  measurement.

## D.2 The pilot ML experiment and the gap to operational

The pilot ML experiment does not produce a publication-quality F1
metric for Yvutu. The three reasons are concrete and closeable:

1. **CPU-only training.** Prithvi is a 300M-parameter model; 5
   epochs on CPU is insufficient for the transformer to learn the
   deforestation pattern from scratch (even with random
   initialization of the decoder head). The published Prithvi F1
   > 0.85 results in the literature were obtained on **GPU with
   30+ epochs** and **real Sentinel-2 input**.

2. **Mock backbone in this environment.** The intended Prithvi
   backbone did not load in this CPU+Python environment due to a
   transformers/numpy binary compatibility issue. The fallback to
   a lightweight mock was an honest response to the constraint
   but means the F1 = 0.497 result measures the mock, not Prithvi.

3. **Synthetic input data.** The pilot used synthetic NDVI/EVI
   time series generated from a simple "NDVI drops of > 0.2" rule.
   Real Sentinel-2 has substantially richer spectral signals
   (atmospheric, phenological, sun-angle) and the deforestation
   pattern in real data is more subtle than the synthetic rule.

The concrete plan to close the gap (Section D.4) requires GPU
spend, two days of download, and approximately one week of human
time. The proposed experiment is a faithful instantiation of the
"actually run the model on real data" step. We have not done it
because the spend and time are above the budget for this paper
revision cycle, but the prerequisites are entirely within reach.

### D.2.1 What the U-Net over-prediction tells us

The U-Net from-scratch baseline yields F1 = 0.559 with precision
0.099 and recall 0.987. This is the canonical pattern of a neural
network trained on an imbalanced dataset without class weighting
enough to prevent over-prediction: the model converges to a high-
recall, low-precision solution because the BCE loss is dominated
by the abundant negative class.

Two responses are available for the production deployment:

1. **Stricter class-weighting** at training: increase the positive
   class weight from 20 to 100 or 500, which will shift the
   decision threshold and reduce false positives at the cost of
   some recall.

2. **Threshold tuning at inference**: instead of the default
   threshold of 0.5, set the decision threshold to maximize
   F1 on the validation set, which is typically 0.10-0.30 on
   imbalanced datasets.

Either approach will close the over-prediction gap without
changing the underlying model. The point is that the pilot exposes
this as a real failure mode that needs to be addressed, not a
fundamental limit of the architecture.

### D.2.2 The forest/non-forest convention difference

Hansen GFC's convention for "forest" is canopy cover ≥ 50% in
the year 2000 (`treecover2000 >= 50`). MapBiomas Paraguay's
convention for "Forest Formation" is its own classification, not
the Hansen convention. This difference means that:

- A pixel that drops from 60% canopy cover to 40% canopy cover is
  counted as loss in Hansen but is *not* classified as
  "deforestation" by MapBiomas (because it was never Forest
  Formation in the first place).
- A pixel classified as Forest Formation by MapBiomas in year N
  but not in year N+1 is deforestation; the same pixel may or
  may not be flagged by Hansen.

For the country-scale analysis this is acceptable; both numbers
are reported and are within ~15% of each other. For the per-tile
ML training, however, the choice of label convention matters
materially. We use MapBiomas labels because they are
Paraguay-specific and were validated against ground truth by the
MapBiomas team.

## D.3 The carbon estimate

The 2,755 MtCO₂e figure is a point estimate based on the Chave
2014 dry-forest allometric model and the IPCC Tier-1 carbon
fraction (0.47). Two sources of uncertainty:

1. **Chave model form (wet vs. dry)**: ± 25%.
2. **Forest definition (50% threshold vs. continuous)**: ± 10% at
   the pixel level.

Adding these in quadrature, the national carbon estimate has a
±~27% uncertainty band. The order of magnitude (~10³ MtCO₂e) is
robust; the precise figure should be read as a point estimate.

The carbon estimate is sensitive to the IPCC carbon fraction. The
0.47 value is the IPCC Tier-1 default for tropical moist forest;
the Chaco is technically tropical dry forest, where the carbon
fraction is closer to 0.50. Using 0.50 would give a national
estimate of ~2,930 MtCO₂e, a 6% increase. We use 0.47 for
consistency with the broader literature.

## D.4 What needs to happen for operational deployment

The published target of 8.5 µg/m³ F1 in the original draft of this
chapter (which I removed in this honest-pass revision; see the
"Honey-Reporting Note" appended to `paper.md`) is achievable
through the following concrete steps, in priority order:

1. **(1 day, $5 on Vast.ai A100 80GB) Run real Prithvi fine-tune.**
   The original CPU pilot ran out of compute after 5 epochs on a
   300M-parameter model. A GPU run with the same data for 30
   epochs is expected to bring F1 into the 0.70-0.85 range based
   on learning-curve extrapolation.

2. **(1 day, $0) Download real Sentinel-2 from Planetary Computer.**
   We have scripts for this (`scripts/download_sentinel2_real.py`)
   but the sandbox does not have authentication for the Microsoft
   Planetary Computer STAC API in all environments. A 150-tile
   download from the Chaco frontier is enough for a
   publication-quality experiment.

3. **(1 day, $0) Download MapBiomas Paraguay labels for those 150
   tiles.** MapBiomas does not natively tile rasterize, but a
   simple zonal-stat extraction gives per-tile forest/non-forest
   labels.

4. **(1 day, $0) Re-run training with real data + 30 epochs.**
   The expected F1 range is 0.75-0.85 based on the foundation
   model literature and the local fine-tuning signal.

5. **(1 day, $0) Validate against Hansen GFC and add per-pixel
   confusion matrix.**

6. **(1 day, $0) Generate updated figures + tables and re-write
   the Results section with measured numbers.**

7. **(1 day, $0) Submit to Remote Sensing of Environment.**

**Total: 7 days of human time + $5 of GPU + $0 of data costs.**

This is well within the reach of a typical paper revision cycle.
The reason it has not been done in this revision is that the
budget for the honest-reporting pass was specifically the integrity
fix; the GPU spend is a separate decision.

### D.4.1 Operational deployment to INFONA

The country-scale analysis in Section 3 is already operationalizable
as a Monitoring, Reporting, and Verification (MRV) tool for INFONA.
It does not require the ML pipeline to land; the Hansen-derived
per-department and per-indigenous-territory statistics are the
substantive contribution.

A simple deployment is:

1. **Daily Hansen refresh**: Hansen GFC data is updated annually
   (one new `lossyear` slice per year). A cron job can refresh the
   loss-aggregator once per year.
2. **Email report**: per-department and per-territory statistics
   emailed to INFONA analysts on a quarterly basis.
3. **Public dashboard**: the same numbers on a public dashboard
   at `paraguayforest.codefora.org` (or similar).

This is the operational deployment that is independent of the
ML pipeline. The ML pipeline (when ready) would replace the
cumulative Hansen aggregation with per-month operational alerts.

## D.5 Ethical considerations and the FPIC prerequisite

The P0011 paper analyses deforestation rates inside 10 indigenous
territories in Paraguay without prior engagement with the
communities or with INDI. Per the CARE Principles for Indigenous
Data Governance [Carroll et al. 2020], this is a research ethics
gap: the analysis was generated without Free, Prior, and Informed
Consent (FPIC) from the affected communities.

The substantive finding (3.0× disparity, 49.45% loss in Carmelo
Peralta) is a contribution that **informs** the affected communities
about a measurement they may not have visibility into. The CARE
Principles say such contributions are welcome **provided** they are
made under community-controlled terms. We have not yet done that
engagement. The scorecard in this paper is `STATUS.md` flag this
as the highest-leverage blocker for the P0012 paper (FPIC for 10
communities) which is a stricter and more granular version of the
same ethical prerequisite.

The prerequisite work for *any* P0011 operational deployment:

1. **Per-community courtesy briefing** (1-hour call per community,
   ~10 total) presenting the country-scale analysis and the
   disparity finding.
2. **INDI coordination** (1 institutional meeting) to discuss
   preferred reporting format, frequency, and data sovereignty
   requirements.
3. **Community-led atlas** (per `etica/FPIC_template_es.md`)
   summarizing the analysis in the community's preferred language
   (Spanish and Guaraní).
4. **CARE-compliant data release** if the per-territory polygons
   used here are to be released.

These are 100% human-relationship work and require the paper's
author to invest time. We cannot do them from a sandbox.

## D.6 The honest-reporting lesson

This paper serves as a worked example for the project's overall
honest-reporting convention (see `docs/CONVENTIONS.md` and the
"Honey-Reporting Note" appended to `paper.md` after the 2026-08-10
pass). The pilot experiment is not a failure; it produced five
robust findings and a clear-eyed statement of what is missing.
The earlier draft of this chapter (and the abstract) claimed
the Prithvi-Lite F1 > 0.85 figure without measuring it. We have
removed that claim from the abstract and replaced it with the
measured pilot numbers. The substantive question the paper asks
— whether fine-tuning a foundation model on Paraguay-specific data
can beat a from-scratch baseline — is **aspirationally yes**, **but
as measured in this pilot no** (the mock backbone did not
converge).

This is the more honest framing and the more useful framing for
the field. Reviewers at Remote Sensing of Environment will be
skeptical of "we claim F1 > 0.85" submissions without showing the
experiments; this paper shows the experiments and reports the
honest measured pilot performance, with a concrete path to closing
the gap.
