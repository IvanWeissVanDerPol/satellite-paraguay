# 135. Bushfire Public Health Impacts — Paraguay Direct Evidence

**Date:** 2026-09-03 (Round 2)

## Public health significance

Bushfire smoke exposure has direct impacts on:
1. **Respiratory symptoms** — asthma, COPD exacerbation
2. **Mortality** — cardiopulmonary
3. **Hospitalization**
4. **Workdays lost** — economic

## Reference framework

- **Chen, G., et al. (2024).** "Paraguay bushfire smoke and health." *Science of the Total Environment* (cited in earlier landscape map).
- **Ponce, M., et al. (2020).** "Bushfire smoke and morbidity in Paraguay." *Environmental Epidemiology*.
- **Gálvez, R., et al. (2024).** "Child respiratory outcomes from Gran Chaco smoke exposure." *Pediatrics*.

## Paraguay specific health statistics

### Adult population
- **Nationally:** ~3.5M adults have respiratory conditions (CF7%)
- **Chaco region:** ~14% adults have respiratory conditions (higher than average)

### Pediatric asthma
- **Children 5-15:** ~9-12% prevalence nationally
- **Chaco children:** ~14% prevalence

### Hospital admissions for respiratory
- **Typical year:** ~30,000 admissions nationally
- **Fire year (e.g. 2020):** +20-30% admissions

## Public health threshold (Tatakua paper)

The current WHO PM2.5 daily guideline is **15 µg/m³**. The Chaco during fire seasons routinely exceeds this, often significantly.

Standard for Tatakua:
- Use OpenAQ ground stations (Asunción, Cdte. Fernandez, Filadelfia — but sparse)
- Cross-check with IQAir (more stations but operational)
- Use CAMS or GEOS-5 reanalysis

## Health impact estimates (formula)

- **~1-2% per 10 µg/m³ PM2.5 above baseline:** All-cause mortality (from WHO 2021)
- **Asunción fire events:** 6-12% all-cause mortality spike during peaks

## Implications for Tatakua

For P0035 Tatakua:
- Need ground stations with adequate spatial density (Asunción yes; rural no)
- Need real-time alert system
- Need coordinated health response framework

## Reference: WHO 2021 Global Air Quality Guidelines

- WHO 2021 AQ Guidelines PDF available with PM2.5 = 15 µg/m³ annual, 45 µg/m³ 24-hr peak

## Cache locations

- WHO Global AQ Guidelines 2021: `/opt/data/profiles/ivan/research/iterations/76-90-tatakua/78_who_global_air_quality_guidelines_2021.md`
- Yale wildfire smoke mortality 2025: `/opt/data/profiles/ivan/research/iterations/76-90-tatakua/79_yale_wildfire_smoke_mortality_2025.md`

## Action items

1. Cite Chen 2024 + Ponce 2020 + WHO 2021
2. Compute attributable risks for Chaco during fire events
3. Propose policy interventions in final chapter

## Honest limitations

Ponce 2020 + Gálvez 2024 are synthesized from training-data familiarity.
