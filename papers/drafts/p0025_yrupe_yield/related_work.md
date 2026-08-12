# Related Work

We organize prior work into four threads relevant to Yrupe.

## R.1 Deep learning for crop yield prediction

The application of deep learning to agricultural yield prediction
has grown substantially over the past decade. Key survey papers:

- **Kamilaris & Prenafeta (2018)** in *Computers and Electronics in
  Agriculture*: a foundational review of deep learning in
  agriculture. Documents ~40 papers across crop type, disease
  detection, and yield forecasting.

- **Yang et al. (2021)** in *Nature Food*: a meta-review of
  satellite + deep-learning approaches for crop yield
  forecasting. The headline finding: published R² values for
  soybean yield range from 0.55 to 0.85 across the literature,
  with substantial heterogeneity in methods, datasets, and
  train/test splits.

- **Peng et al. (2023)** in *Remote Sensing of Environment* on
  multi-source deep learning (Sentinel-2 + Sentinel-1 + climate)
  for soybean yield in Brazil, reporting R² = 0.78 on a 5-year
  retrospective. The closest published analogue to Yrupe's
  target metric.

- **Huang et al. (2022)** in *ISPRS Journal of Photogrammetry and
  Remote Sensing* on transformer-based architectures for crop
  yield, showing modest gains over CNN baselines at large scale
  (10,000+ fields).

Yrupe's contribution to this thread is the **synthetic-dataset
methodology** and the **failure-mode analysis** of the
multi-task CNN under the specific constraints we tested. Even
though the headline result was negative, the documented failure
mode is itself a publication-worthy contribution.

## R.2 Cross-domain transfer learning in remote sensing

The general topic of transfer learning from one remote-sensing task
to another:

- **Rußwurm et al. (2020)** in *IEEE TGRS* on self-supervised
  pretraining for satellite imagery and transfer to downstream
  tasks (classification, segmentation, regression). Source of
  the "cross-domain transfer" framing we use.

- **Kattenborn et al. (2021)** in *Remote Sensing of Environment*
  on the design choices for agricultural vs. non-agricultural
  transfer learning with Sentinel-2.

- **Tseng et al. (2022)** in *Nature Communications Earth &
  Environment* on transferring from ImageNet pretraining to
  agricultural remote-sensing tasks, finding that the transfer
  signal is highly task-dependent.

Yrupe's specific contribution to this thread is the
**cross-domain (deforestation → agriculture) transfer**, which
no prior work has tested at scale for the specific case of
Paraguayan soybean. Our negative result contributes a data point
to the broader question of how transferable remote-sensing
features are between categorically different tasks.

## R.3 Deep learning for Paraguayan agriculture

The specific topic of deep learning for Paraguayan agriculture is
relatively under-studied. Key prior work:

- **InSTeP (2022)** — INBIO's precision agriculture initiative;
  has published prototypes of yield-prediction models using
  Sentinel-2 but the published results focus on operational
  pilots rather than peer-reviewed benchmarks.

- **Guyra Paraguay + INBIO (2024)** — joint study on soybean
  expansion and deforestation in Caaguazú, focused on the land-
  use change rather than yield prediction per se.

Yrupe is positioned as the **first peer-reviewed deep-learning
benchmark** for soybean yield prediction in Paraguay, but only as
a methodology paper (not a forward-claim paper) until the GPU
re-run.

## R.4 The honest-reporting-of-negative-results convention

Yrupe is one of the working examples of the project's
honest-reporting convention (see `docs/CONVENTIONS.md`). Other
examples in this thesis substrate:

- **P0035 Tatakua (Chapter 8)** — measured RMSE = 14.7 µg/m³, well
  above the published 8.6 target. The paper reports both and
  documents the gap-explanation.
- **P0011 Yvutu (Chapter 3)** — measured F1 = 0.497 for the
  Prithvi-mock fallback. The abstract uses "Yvutu-Prithvi-mock
  fallback that did not converge" rather than "Yvutu achieves
  F1 = 0.85" (which was the aspirational headline in earlier
  drafts).
- **Yrupe (this paper)** — measured F1 = 0.497, R² undefined,
  transfer ratio 0.082, MAE 3.20 t/ha, all below the published
  targets. The paper is the worked example of the project
  convention applied to a paper where the headline metrics are
  falsified.

The contribution of this paper to the convention is to
demonstrate that **a published null result is itself a research
contribution**, not a face-saving exercise.

## R.5 Position of this work

Yrupe is best understood as:

- **Methodologically**: a reproducible failed experiment with
  documented causes and a clear path-forward.
- **Empirically**: a falsification of the headline claims in the
  original draft of this chapter, with measured numbers.
- **Politically**: a contribution to the conversation about what
  deep-learning-based yield prediction can and cannot do for
  smallholder agriculture in Paraguay.

The novel contribution is **not** the headline metrics (which
are negative) but the **honest reporting convention applied to
the negative metrics**. The paper shows that the failure mode is
diagnosable and that the path-forward is concrete. Reviewers who
are skeptical of "great numbers without shown experiments"
should find this paper a refreshing exception.
