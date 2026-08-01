# Data Sheet — OpenAQ

**Dataset:** OpenAQ Air Quality Measurements
**Provider:** OpenAQ Foundation
**License:** CC0
**URL:** https://openaq.org/

## Motivation

Global open air quality data aggregated from government + low-cost sensors. Critical for P0035 Tatakua (Asunción PM2.5 forecast).

## Composition

- **Spatial coverage:** Global (5+ stations in Asunción)
- **Temporal coverage:** 2013-present (varies by station)
- **Parameters:** pm25, pm10, no2, o3, so2, co, bc
- **Update frequency:** Hourly
- **Number of stations:** ~30,000 globally, 5 in Asunción

## Collection process

- Aggregated from: EPA, EEA, OpenAQ community
- Quality-controlled (removes outliers)
- Standardized to common units

## Uses

- Train PM2.5 forecast model (P0035 Tatakua)
- Validate against satellite S5P
- Real-time air quality monitoring

## Distribution

- **API v3:** https://api.openaq.org/v3 (requires API key)
- **Browse UI:** https://openaq.org/
- **API docs:** https://openaq.org/docs
- **Format:** JSON via REST API

## Maintenance

- Updated continuously
- API versioned (v3 is current; v1/v2 deprecated 2025)

## Limitations

- Stations may have gaps
- Different sensors = different uncertainty
- Not all pollutants available everywhere
- API key required for v3

## Ethical considerations

- Public/CC0 — no consent required
- Privacy: no personal data
- Use cases: public health, research
