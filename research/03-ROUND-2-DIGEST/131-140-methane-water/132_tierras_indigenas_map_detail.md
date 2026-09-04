# 132. Tierras Indigenas Digital Map Update — Detailed Reference

**Date:** 2026-09-03 (Round 2)

## Background

Tierras Indigenas is FAPI Paraguay's open-access platform for Indigenous land records:
- Web: https://tierrasindigenas.org.py
- Launched: 2024 (per Wikipedia earlier cache)
- Alternative: Global Forest Watch + LandMarklayer

## Map features

### 1. Indigenous territory polygons
- 244 communities (per IWGIA Paraguay profile)
- Official recognition status (titulada, en proceso, no reconocida)
- Surface area (ha)
- Linguistic family (5: Guaraní, Mataco-Mataguayo, Zamuco, Lengua-Maskoy, Guaicurú)

### 2. Map overlays
- Deforestation (Forest Loss since 2002)
- Protected areas (from WDPA)
- Population (from WorldPop)
- Biodiversity indicators (from IUCN Red List)
- Climate hazards (from ThinkHazard!)

### 3. Active deforestation alerts
- GLAD alerts
- RADD alerts
- User-reported geo-references

## API access

- Web interactive map frontend (Leaflet/Mapbox)
- Backend uses Vector Tiles + GeoJSON
- Direct API endpoint for limited data layers

## Reference papers + organizations

- **FAPI (Federación por la Autodeterminación de los Pueblos Indígenas)** — operating organization
- **GIZ Cooperation Paraguay** — German Federal Enterprise for International Cooperation (sponsor?)
- **LandMark** — global Indigenous+Community land rights layer
- **Indigenous Peoples Rights International (IPRI)** — global rights tracking
- **Cultural Survival** — global + specific (Ayoreo outreach)
- **Forest Peoples Programme (UK)** — Gran Chaco secure land title project

## Synthetic considerations

For P0012 Yvy (Indigenous land tenure × remote sensing):
1. Use Tierras Indigenas polygons as ground truth
2. Train semantic segmentation for Indigenous-vs-private land
3. Compare deforestation rates inside vs outside Indigenous territories

## Cache locations

- Tierras Indigenas + FAPI: `/opt/data/profiles/ivan/research/iterations/41-60-yvy/54_forest_peoples_programme_overview.md`
- IWGIA Paraguay: `/opt/data/profiles/ivan/research/organizations/iwgia_paraguay.html.md`

## Specific Paraguayan Indigenous peoples in Tierras Indigenas

1. **Ayoreo-Totobiegosode** — northern Chaco, some in voluntary isolation
2. **Nivaclé (Chulupí)** — Boquerón
3. **Maskoy (Toba-Maskoy, Enlhet Norte, Enlhet Sur)** — Boquerón
4. **Nivaclé (Augeleo 26 de Junio)** — historical case
5. **Enlhet** — Bajo Chaco
6. **Toba Qom** — Chaco
7. **Guayaki?** — no, Guaraní
8. **Aché** — formerly isolated

## Contact + outreach

- FAPI internal collaborators: Tatiana Franklin (cited earlier)
- FAPI website: https://www.fapi.org.py
- LandMark +63 Indigenous Peoples (Paraguay)

## Action items

1. Pull Tierras Indigenas + LandMark merged polygon file
2. Verify map accessibility during fieldwork
3. Cross-check with INDI official registry

## Honest limitations

Some platform features may have evolved. Live verification needed.
