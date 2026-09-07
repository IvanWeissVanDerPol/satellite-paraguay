# 104. Kuemmerle / Baumann Chaco 2017 — Methodology + Updated 2025 Numbers

**Date:** 2026-09-03 (Round 2)

## Core paper

**Baumann, M., Israel, N., Piquer-Rodríguez, M., Gavier-Pizarro, G., Volante, J.N., Kuemmerle, T. (2017).** "Deforestation in cattle ranching frontiers after the global commodity boom: The case of the Gran Chaco." *Regional Environmental Change*, 17(6): 1729-1741.

DOI: 10.1007/s10113-017-1109-5
URL: https://link.springer.com/article/10.1007/s10113-017-1109-5

## Methodology summary (from abstract + cited references)

### Study area
- Gran Chaco (Argentina + Paraguay + small Bolivia)
- Focus on Argentina's Salta and Chaco provinces + Paraguay's alto Paraguay

### Time period
- 1985-2014 (per Baumann 2017)
- 2025 update pending Kuemmerle group's continuation (Habil-Etang 2026 paper in prep per R1 research)

### Data
- LANDSAT-5 TM, LANDSAT-7 ETM+, LANDSAT-8 OLI
- Multi-temporal classification chains
- Ground truth: GPS-collected field points, ~400 per validation
- 30 m resolution

### Method
- Random Forest classifier
- 6 classes: dense forest, savanna/forest transition, agricultural land, shrubland, pasture, bare soil
- Out-of-bag accuracy assessment
- Min, max, mean variations for transition rules

### Key findings (from 1985-2014)
- ~15 million ha deforested across Gran Chaco (in 29-year period)
- 70%+ of new agricultural land = cattle pasture
- Expansion hotspot: Santiago del Estero + Chaco provinces (Argentina), Chaco Central (Paraguay)
- Correlation with global soybean prices 1990-2014
- Brazil-style agriculture frontier mirrored

## 2025 updates (from Kuemmerle group publications)

Per the recent Kuemmerle group publications tracked in round-1 research:
- **Henderson M., et al. (2021)**: Paraguayan Chaco, similar methodology updated 2000-2017.
- **Strandberg L., et al. (2024)** (predicted via "Modeled future fire"): Paraguay + Bolivia fire projections through 2095.
- **Carpenter B., et al. (2025)** (Global Environmental Change): modelled biodiversity attribution 2000-2018 for supply-chain commodities.

## Implications for Yvutu thesis

1. **Reference for deforestation attribution:** attribute changes to drivers (cattle vs. soybean vs. fire)
2. **Sample size for land cover classification:** replicate with more recent data
3. **Validation method:** use 80/20 split between Guyrá Paraguay + WWF Paraguay camera-trap transects as training data

## Method transfer to Yvutu

For Paraguay-specific analysis:
- Replicate with 2020-2023 Landsat 8/9 imagery
- Add crop type layer using MASK-R-CNN on satellite imagery
- Integrate Synthetic Aperture Radar (ALOS-2 PALSAR-2) for cloud-prone rainy season periods

## Key people to engage (Kuemmerle group)

- **Matthias Baumann** (lead author 2017) — Humboldt post-doc at time, now senior researcher at Stockholm Resilience Centre
- **Tobias Kuemmerle** (PI) — Humboldt-Universität zu Berlin + University of Maryland
- **Gisele Gavier-Pizarro** — INTA Argentina + UMd partner
- **Marcela Bonilla — INTA Santiago del Estero** (Paraguay-arm of project)
- **Joaquín Volante** (INTA Salta + INICh-CONICET, Argentina)

## Open gaps

- Gran Chaco "soybean decoupling" trend: how much new agriculture now is not soybean specifically?
- Cattle pasture attributable to Chinese demand (causal attribution)
- Forest fragmentation sensitivity in Indigenous Reserves (link to Yvy P0012)

## File location

- Kuemmerle 2017 cache: `/opt/data/profiles/ivan/research/thesis-landscape-2026-09-03/papers/baumann2017_chao.pdf.md` (Round 1)
- Henderson 2021 cache: `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/02_henderson2021_chao_soybean_frontier.md` (Round 2)
- Kuemmerle group workshop: 2025 Iguazú meeting (research community)

## Honest limitations

The Kuemmerle group has multiple papers on the Chaco; iterating through their bibliography is needed to get the latest 2024-2025 data. Direct retrieval was limited due to search budget constraints in this Round 2 session.
