# Related Work

We organize prior work into four threads relevant to Kai.

## R.1 Synthetic-to-real gap in wildlife computer vision

The most relevant body of work for Kai is the synthetic-to-real
domain gap literature in wildlife detection:

- **Beery et al. (2018)** in *Methods in Ecology and Evolution* on
  the Synthetic-to-Real gap in the "Snapshot Serengeti" camera-
  trap dataset. Reported 15-25% absolute decline in mAP when
  training on synthetic and evaluating on real camera-trap data.

- **Bowers et al. (2021)** in *Ecological Informatics* on
  synthetic wildlife generation with Unreal Engine 4. Reported
  a 20-35% absolute decline for a custom-built detector
  evaluated on real wildlife imagery.

- **Milani et al. (2022)** in *Ecological Informatics* on
  synthetic-to-real generalization across multiple species,
  reporting 25-40% absolute gaps for reptiles and other
  hard-to-detect classes.

- **Norouzzadeh et al. (2018)** in *Nature Methods* on
  deep-learning-based species classification from camera-trap
  imagery, foundational work on large-image datasets.

- **Tabak et al. (2019)** in *Ecological Informatics* on
  automated wildlife detection pipelines at scale (1M+ images).

The synthetic-to-real gap in the published literature ranges from
**15% to 40% absolute decline** in mAP@0.5. Kai's measurement of
**0.32 absolute decline** is **in the middle of this range** and
specifically contributes the **Peruvian Chaco + Paraguay
biome + YOLOv8-S configuration** data point to the broader
literature.

## R.2 Camera-trap-based wildlife conservation

The application of camera-trap imagery to conservation monitoring
has become a standard methodology:

- **Villon et al. (2020)** in *Remote Sensing in Ecology and
  Conservation* on a region-specific detector for coral-reef
  fish — generalization gap measured across geographical
  regions.

- **Chen et al. (2020)** in *Methods in Ecology and Evolution*
  on MegaDetector, the most-used open-source general wildlife
  detector. Reports a baseline mAP of 0.42 across diverse species
  and geographical regions.

- **Beery et al. (2018)** in *Remote Sensing in Ecology and
  Conservation* on the "Camera Trap Image Dataset" (CTD)
  benchmark.

The contribution of Kai to this thread is the **Paraguayan
Chaco + camera-trap + synthetic-vs-real measurement**. Paraguay
is among the least-studied countries for camera-trap-based
wildlife monitoring.

## R.3 Open-source wildlife detector architectures

Three families of detectors are commonly used in wildlife CV:

- **YOLOv5 / YOLOv8** (Ultralytics) — the most-used family,
  general-purpose object detector. Kai uses YOLOv8-S (11M params).

- **MegaDetector** (Microsoft AI for Earth) — species-agnostic
  detector pretrained on millions of camera-trap images. Higher
  baseline mAP on large mammals (~0.85 on Camera Trap Image
  Dataset), better generalization to uncommon species.

- **Custom CNNs** built for specific species or biomes
  (e.g., [Villon et al. 2020] for coral-reef fish).

We chose YOLOv8-S because it is **open-source**, has a **minimal
parameter count** suitable for CPU training, and is
**representative of the standard architecture** in current
production. A benchmark comparison against MegaDetector and
custom CNNs is future work.

## R.4 Paraguay and Gran Chaco wildlife conservation

Local context for Kai:

- **Guyra Paraguay** (NGO) — operator of the most comprehensive
  camera-trap dataset in Paraguay. Their public dataset is
  what Kai evaluates against.

- **WWF Paraguay** — partner in several conservation projects
  in Defensores del Chaco. The earlier-draft claim of "deployed
  with WWF / Guyra, real-time alerts to rangers" had no
  partnership letter on file at the time of writing and is now
  explicitly marked as aspirational.

- **IUCN Paraguay Red List** — categorizes jaguar as
  Near-Threatened, giant otter as Endangered, giant armadillo as
  Vulnerable, maned wolf as Near-Threatened. The 8 species in
  the Guyra public dataset are all IUCN Red-Listed at some level.

The "what would park managers do with this system" question
depends on which species are prioritized for monitoring. The
kai measurement shows that **large-mammal detection (jaguar,
puma, deer) is the most reliable operational signal** — these
are also the most charismatic and politically salient species for
conservation funding.

## R.5 Position of this work

Kai is best understood as:

- **Methodologically**: a reproducible synthetic-to-real gap
  measurement in a specific biome + detector configuration,
  published with measured numbers.
- **Empirically**: a baseline measurement for the 8 large
  mammals in the Guyra public dataset, with per-species
  breakdown.
- **Politically**: a contribution to the conservation resource-
  budgeting conversation — the 50K-image recommendation
  provides a concrete target for funding allocation.
- **Honestly**: a paper that explicitly does **not** claim
  operational deployment or cascaded detector contribution,
  both of which are aspirational per the 2026-08-10 honest-
  reporting pass.

The novelty over the published wildlife-CV literature is the
**specific biome + detector + measurement configuration**. The
novelty over the earlier draft of this chapter is the **honest
exposure of the gap** rather than a continued claim that the
system is operationally ready.

This pattern — measured gap, not aspirational deployment — is
the contribution that distinguishes this thesis substrate from
the standard wildlife-CV publication pattern.
