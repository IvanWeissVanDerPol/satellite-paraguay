# Data Sheet — Paraguay Geodata

**Dataset:** paraguay-geodata (Ai-Whisperers project)
**Provider:** Ai-Whisperers (Ivan Weiss Van der Pol)
**License:** Various (mostly CC0 or open)
**URL:** https://github.com/Ai-Whisperers/paraguay-geodata
**Live deploy:** https://geodata.paragu-ai.com/

## Motivation

Comprehensive geospatial dataset for Paraguay, including admin boundaries, OSM data, climate, biodiversity, real-estate, and indigenous territories. Used as ground truth across all 6 papers.

## Composition

### Total size
- 549 MB across 14+ datasets
- 7,912 tiles (10x10 km grid covering all Paraguay)
- 49,641 OSM buildings
- 14,835 OSM roads
- 7,500 Catastro parcels
- 10,898 real-estate listings
- 200 GBIF species observations
- 8 KB indigenous territories
- 36 KB climate risk layer

### Datasets

| File | Size | Description |
|------|------|-------------|
| `tile_index.json` | 3.6 MB | 7,912 tile index (10x10 km) |
| `roads.geojson` | 5.6 MB | 14,835 OSM roads |
| `buildings_asuncion.geojson` | 13 MB | 49,641 OSM buildings (Asunción) |
| `catastro_parcels_sample.geojson` | 4.4 MB | 7,500 Catastro parcels |
| `properties_latest.geojson` | 14 MB | 10,898 listings |
| `properties_scrubbed.geojson` | 15 MB | PII-scrubbed listings |
| `water.geojson` | 2.5 MB | Water bodies |
| `indigenous_territories.geojson` | 8 KB | Indigenous communities |
| `climate_risk.geojson` | 36 KB | Climate risk layer |
| `flood_risk.geojson` | 4 KB | Flood risk |
| `gbif_paraguay.geojson` | 96 KB | 200 species |
| `hillshade_*.jpg` | dozens | DEM hillshades |
| `bcp_snapshot.json` | 2 KB | BCP macro |
| `nasa_power_asuncion.json` | 1 KB | NASA POWER climate |
| `inbio_zafra_2025_2026.json` | 4 KB | INBIO crop area |

## Collection process

- **OSM data:** OpenStreetMap contributors (Geofabrik extracts)
- **Catastro:** Official Catastro Nacional (public)
- **Climate:** NASA POWER API
- **Biodiversity:** GBIF API
- **Real estate:** Public listings
- **Indigenous:** INDI + community partnerships (CARE-compliant)

## Uses

- Paraguay admin boundaries for all 6 papers
- OSM buildings/roads for P0010 Tava-i (related project)
- Catastro for P0012 Yvy (indigenous conflict)
- Climate + biodiversity for P0035 Tatakua
- Indigenous territories for P0012 Yvy

## Distribution

- **GitHub:** https://github.com/Ai-Whisperers/paraguay-geodata
- **Live deploy:** https://geodata.paragu-ai.com/
- **API:** Available via Paraguay geodata portal

## Maintenance

- Updated monthly by Ai-Whisperers team
- New datasets added as needed

## Limitations

- Real-estate listings are point data, not parcel boundaries
- Indigenous territories are simplified polygons
- OSM coverage uneven (better in urban areas)
- Catastro is sample, not full coverage

## Ethical considerations

- **Indigenous data (CARE Principles):**
  - Collective Benefit: communities get CC-BY atlas
  - Authority to Control: INDI + community review before publication
  - Responsibility: annual report to communities
  - Ethics: cultural review board
- **Privacy:** Real-estate listings are PII-scrubbed
- **Use restrictions:** None for academic research
