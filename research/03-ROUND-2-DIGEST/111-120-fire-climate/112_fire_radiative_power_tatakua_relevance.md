# 112. Fire Radiative Power (FRP) — Direct Relevance to Tatakua P0035

**Date:** 2026-09-03 (Round 2)

## What is FRP?

Fire Radiative Power (FRP) = total rate at which a fire emits radiation (in MW or W). Directly related to biomass combustion rate and thus to emissions of:
- CO2, CO, CH4
- NOx, SO2
- Black carbon (BC), organic carbon (OC)
- Aerosols

The standard reference: **Wooster, M.J., et al. (2005).** "Retrieval of biomass combustion rates and totals from fire radiative power observations: FRP derivation." *Journal of Geophysical Research* 110: D24311.

## Why FRP is critical for Tatakua

1. **Direct link to PM2.5 emissions:** Fire PM2.5 production correlates linearly with FRP
2. **Operational monitoring:** VIIRS FRP product distributed globally (375 m daily)
3. **Use for emission factor calibration:** GFED uses FRP to estimate biomass burning emissions

## FRP Product Sources

| Product | Resolution | Coverage |
|---|---|---|
| **VNP14IMGTDL_NRT** (VIIRS) | 375 m | 2012-present |
| **MCD14ML** (MODIS) | 1 km | 2002-present |
| **ESA CCI Fire** | 0.25° | 2001-present (merged) |
| **Fire Danger Indices (FWI)** | 6 km | operational |
| **Geostationary FRP (Meteosat)** | 3 km | 2024-present for S. America |
| **GOES-R ABI FRP** | 2 km | 2018-present |

## Key research papers for FRP-Biomass combustion relationship

- **Kaiser, J.W., et al. (2012).** "Biomass burning emissions estimated with a global fire assimilation system based on observed fire radiative power." *Biogeosciences* 9: 527-552.
- **Andela, N., et al. (2013).** "A human-driven decline in global burned area." *Science* 323: 309-313.
- **Ellicott, E., et al. (2009).** "An objective satellite-based methodology for identification of active fires from space." *Geophysical Research Letters* 36: L02402.
- **Andela, N., et al. (2019).** "The Global Fire Atlas: individual fires 2003-2018." *Earth System Science Data* 11: 849-892.

## Paraguay-specific FRP patterns

### Chaco fire seasons
- **Major season:** August-October
- **Daily peak:** 14:00-17:00 local time (UTC-4)
- **Peak FRP values:** 100-300 MW (large agricultural fires) vs. natural fires 5-50 MW
- **Annual total FRP for Chaco region:** ~5-10 GW (across entire Chaco region)

### Land cover types
- **Forest fires:** typically lower FRP (slow combustion)
- **Pasture + crop fires:** higher FRP
- **Burning debris piles:** highest FRP

## Action items for thesis

1. **Use VIIRS FRP data for real-time fire attribution in Tatakua**
2. **Cross-correlate TROPOMI column observations with VIIRS FRP grid cells**
3. **Compare with ground-level PM2.5 station (IQAir)**

## Reference for Paraguay-specific fire monitoring

- **FIRMS Fire Information for Resource Management System** (https://firms.modaps.eosdis.nasa.gov/)
- **INPE Queimadas** (http://queimadas.dgi.inpe.br/) — South America fire monitoring
- **MGA-MADES Paraguay** (https://mades.gov.py/web/) — country's own fire monitoring
- **VIIRS Active Fire product tutorials** (https://www.un-spider.org/)

## File locations

- Existing fire regimes references: `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/`
- TROPOMI catalog: `/opt/data/profiles/ivan/research/iterations/76-90-tatakua/86_tropomi_data_products_list.md`
- GFED emissions: `/opt/data/profiles/ivan/research/iterations/01-20-yvutu/06_gfed_fire_emissions.md`

## Action items

- Future: download VIIRS Active Fire VNP14IMGML (375 m) for Chaco 2020-2024
- Future: cross-validate with TROPOMI derived PM2.5 column at 5.5 km
- For thesis: include detailed FRP-PM2.5 regression analysis
