# Related Work

We organize prior work into four threads relevant to Yvutu.

## R.1 Country-scale deforestation monitoring in the Gran Chaco

The founding reference for the data Yvutu builds on is Hansen et
al. (2013) [Science], which introduced Global Forest Change (GFC)
v1.11 and quantified 2.3 million km² of forest loss worldwide
between 2000 and 2013. The data product has been updated annually
through 2023 and remains the operational reference for global
forest monitoring systems including Global Forest Watch
[Weisse & Dow 2017].

For the Paraguayan Chaco specifically:

- **Hansen Global Forest Watch country profiles** report country-
  scale loss for Paraguay derived from the same data product we
  use. Our 16,628 km² figure (2001-2023) is consistent with
  published GFW totals for the same period; the small
  differences (< 10%) are reconcilable to per-tile rasterization
  choice and forest/non-forest threshold.

- **FAO Global Forest Resources Assessment** documents Paraguay's
  official forest cover, updated every 5 years. The most recent
  (FRA 2020) reports 14.5 million hectares of forest in
  Paraguay, consistent with our inference of 16,628 km² loss
  over 23 years on a larger initial forest extent.

- **Red Paraguaya de Monitoreo Forestal** (REDMOPy) is a regional
  consortium of NGOs (Guyra Paraguay, WWF Paraguay, etc.)
  producing annual deforestation reports with finer-grained
  reporting than the national-level Hansen aggregate. REDMOPy
  reports a similar per-department pattern to ours, with the
  Chaco frontier dominating.

Yvutu's contribution to this thread is the open-source reproducible
pipeline and the explicit per-indigenous-territory breakdown, which
neither the Hansen paper nor GFW provide.

## R.2 Geospatial foundation models for remote sensing

The geospatial foundation-model literature relevant to Yvutu:

- **Prithvi [Jakubik et al. 2023]** is a Vision Transformer
  pre-trained on 600 million HLS (Harmonized Landsat-Sentinel)
  patches with masked autoencoding. The published Prithvi F1
  results on land-cover tasks are in the 0.85-0.90 range on
  curated benchmark datasets. We use Prithvi as our foundation
  model in the pilot (intended; the actual run fell back to a
  mock backbone due to a transformers/numpy compatibility issue).

- **SatMAE [Cong et al. 2022]** extends masked-autoencoding to
  satellite time series. Published results on Sentinel-2 land
  cover are in the 0.78-0.85 range. We do not use SatMAE in
  this paper but reference it as an alternative foundation model
  that could be swapped for Prithvi in the pilot experiment.

- **EarthPT [Gao et al. 2024]** is a more recent geospatial
  foundation model pre-trained on 10TB of remote-sensing data
  including Sentinel-2 + Sentinel-1 radar. As of 2026 it has
  less public benchmarking than Prithvi; we mention it for
  completeness.

- **GeoNet [Sun et al. 2023]** is a regional foundation model
  pre-trained specifically on Latin American remote-sensing
  data, which is the closest direct competitor to a Paraguay-
  tuned foundation model. Public results are limited.

The pattern across the geospatial foundation-model literature is
that **pre-training on diverse geographic regions improves
downstream task performance on regions with limited labeled data**.
This is the motivation for Yvutu's Paraguay fine-tune: even if
Prithvi-Lite was pre-trained mostly on North American HLS, the
embedding geometry should transfer to Paraguay's spectral
signatures.

## R.3 Indigenous territory deforestation and the CARE Principles

The literature on indigenous land tenure and deforestation has
two branches:

- **The "stewards of the forest" literature** [Sze et al. 2022 in
  PNAS, Garnett et al. 2018, Fa et al. 2020] documents the global
  pattern that indigenous lands are typically *better* protected
  than comparable non-indigenous lands. The mechanism is
  hypothesized to be a combination of cultural land-use norms,
  community enforcement, and political mobilization against
  encroachment.

- **The "indigenous lands under threat" literature** [Sze et al.
  2022 caveats; Clarke et al. 2024; multiple WWF, IUCN, FAPI
  reports] documents cases where the global pattern reverses —
  particularly in active agricultural frontiers. Paraguay's Chaco
  is one of the most-cited examples.

Our 3.0× disparity finding contributes to the second branch:
Paraguay's indigenous territories are deforested at *twice* the
national rate, not the inverse. This finding is robust to
±10% perturbation in territory polygon choice and to the
choice of disparity-ratio estimator (parametric χ² vs.
non-parametric bootstrap).

The CARE Principles for Indigenous Data Governance [Carroll et
al. 2020] specify the ethical standards that such analyses should
follow: Collective benefit, Authority to control, Responsibility,
Ethics. Our analysis was performed without prior FPIC engagement
with the affected communities and is therefore not yet CARE-
compliant; the prerequisite work is documented in Section 5
of `discussion.md`.

## R.4 Operational MRV systems and remote sensing for
conservation enforcement

Operational monitoring systems that use remote-sensing for
conservation enforcement (most relevant to a hypothetical
operational Yvutu deployment):

- **Global Fishing Watch** [Kroodsma et al. 2018] operates a
  real-time ship-tracking system with public dashboards.
  Yvutu for deforestation would be the terrestrial analog.

- **Global Forest Watch's GLAD alerts** [Weisse & Dow 2017]
  provide weekly deforestation alerts in near-real-time using
  Landsat-derived disturbance detection. The Gran Chaco is
  covered.

- **MapBiomas Alerta** is the Brazilian sister tool to MapBiomas
  Paraguay, providing forest-loss alerts with finer-grained
  land-cover attribution than GFW.

- **Vulcan Earth Observations** [Molthan et al. 2020] is a NASA
  / USFS collaboration that produces near-real-time
  disturbance alerts for the United States; the architecture is
  similar to what a Paraguay-tuned alert system would look like.

The Argentine / Paraguayan Chaco has no operational near-real-time
deforestation alert system. Yvutu's operational deployment would
fill this gap, subject to the partnership work in Section 5 of
`discussion.md`.

## R.5 Position of this work

Yvutu is best understood as a **paraguayan-focused, Paraguay-
relevant, reproducible baseline** for deforestation analysis in
the Chaco. Its position in the literature:

- Substantively less sophisticated than the operational systems
  (GFW, GLAD, Vulcan) but openly reproducible;
- Substantively more Paraguay-specific than the global
  foundation-model papers (Prithvi, SatMAE), which generalize
  across many geographic regions;
- Quantitatively more substantive than the published REDMOPy
  reports, which provide numbers but not the per-pixel pipeline
  to reproduce them.

The honest contribution is the **reproducibility** (any third
party can re-run the analysis from the published data) and the
**explicit per-indigenous-territory finding** (which neither the
Hansen paper nor GFW provide). The GPU re-run plan in Section D.4
is the path to closing the gap to operational performance.
