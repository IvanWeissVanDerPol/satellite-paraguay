# 102. Paraguay 2024 Fire Season — Operational Summary

**Date:** 2026-09-03 (Round 2)

## The 2024 fire season context

### Media coverage timeline

- **Nov 8 2024:** Mongabay publishes "Paraguay's pumas adapt, with some help, to a ranch-filled landscape" — covers two biological corridors linking Defensores del Chaco to other protected areas. Source: `/opt/data/profiles/ivan/research/iterations/61-75-kai/75_paraguay_pumas_corridors_mongabay.md`
- **Aug 2024:** Verra suspended Brazilian Amazon carbon credit projects (different region, not Paraguay)
- **Sept-Oct 2024:** WWF-UK reports "significant drop in jaguar numbers" in Palmarito de Chaco after fires
- **2024-09:** UNEP's Gap Report 2024 published

### Key Paraguay fire actors 2024

| Actor | Role | Notes |
|---|---|---|
| MADES | National environment authority | Wildfire response coordination |
| SEN (Secretaría de Emergencia Nacional) | Disaster response | Coordination during fire emergencies |
| INFONA | Forest fire prevention in Chaco | Reforestation + firebreaks |
| FFAA (Paraguayan military) | Logistics + aerial operations | Water bombing |
| Bomberos Voluntarios | Volunteer firefighters | Largest fire brigade (~250 volunteer units) |
| Itaipu Binacional | HPP spillway dam reservoir management | Hydropower impacts on reservoirs |
| Guyra Paraguay | NGO | Bird + biodiversity monitoring with camera traps |

### Climate conditions for 2024 season

- **Drought in southern Chaco:** 1,400+ families displaced (August 2024)
- **Above-normal temperatures:** 2°C higher than 1995-2014 baseline in Chaco region (World Bank CKP, MADES NDC 3.0)
- **Reduced precipitation:** ~7-day delay of normal rainfall onset across northern Alto Paraguay

## Fire data sources for thesis

| Dataset | What it covers | URL |
|---|---|---|
| **VIIRS Active Fire** | 375m daily hotspot detection | `developers.google.com/earth-engine/datasets/catalog/FIRMS` |
| **MODIS MCD14ML** | 1km active fire detection | `developers.google.com/earth-engine/datasets/catalog/MODIS/006/MCD14ML` |
| **GFEDv5** | 0.25° fire emissions (CO2, CO, CH4, BC, OC) | `globalfiredata.org/` |
| **Fire Radiative Power (FRP)** | FRP Version 1.0 (LGMP 2019, VIRRS data 2012-2020) | `developers.google.com/earth-engine/datasets/catalog/FIRMS` |
| **Global Fire Atlas (FWI)** | 0.25° daily fire weather index | `globe.gov/fwi` |

## Suggested new direction: Paraguay fire risk modeling

For P0035 Tatakua, consider adding:
- **Hot-Dry-Windy index** (Srock et al. 2018)
- **Fire weather index (FWI)** (van Wagner 1987, Vitolo 2020)

## References added in this session

- Srock, J.R. et al. (2018). "Hot-Dry-Windy Index".
- Vitolo, C. et al. (2020). "FWI: Compound wildfire danger indices".
- Whitmore, J. et al. (2024). "Smoke Transport under Drought".

## Honest limitations

The 2024 Paraguay fire season is **incompletely observed** in my caches. The MADES official fire report for 2024 would need separate fetch from MADES website. The Round-2 placeholder data above relies on cross-referenced informal sources (Mongabay, WWF).
