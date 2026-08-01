# Data Sheet — NASA FIRMS

**Dataset:** NASA Fire Information for Resource Management System (FIRMS)
**Provider:** NASA
**License:** Public
**URL:** https://firms.modaps.eosdis.nasa.gov/

## Motivation

Real-time global fire alerts from MODIS + VIIRS. Critical for P0026 Kai (wildlife poaching detection via fire signals).

## Composition

- **Spatial coverage:** Global
- **Temporal coverage:** MODIS: 2000-present, VIIRS: 2012-present
- **Temporal resolution:** Twice daily (MODIS), multiple (VIIRS)
- **Spatial resolution:** 1km (MODIS), 375m (VIIRS)
- **Update latency:** ~3 hours from observation
- **Sources:** MODIS (Terra/Aqua), VIIRS (Suomi-NPP, NOAA-20)

## Collection process

- Thermal anomaly detection from MODIS/VIIRS
- Cloud filtering
- Quality flags (confidence level)
- Distributed via FIRMS

## Uses

- Fire hotspot detection (P0026 Kai)
- Deforestation alerts (P0011 Yvutu complement)
- Agricultural monitoring (P0025 Yrupe)
- Public health (P0035 Tatakua — biomass burning)

## Distribution

- **Web:** https://firms.modaps.eosdis.nasa.gov/
- **API:** https://firms.modaps.eosdis.nasa.gov/api/
- **Format:** CSV (per country or bbox)
- **API key:** Free registration

## Maintenance

- Updated continuously (every 1-3 hours)

## Limitations

- Cloud cover blocks detection
- Small fires may be missed
- Confidence varies by sensor
- 1km resolution (MODIS) may miss small fires

## Ethical considerations

- Public — no consent required
- Used for: fire management, conservation, public health
- Real-time alerts may cause panic if misinterpreted
