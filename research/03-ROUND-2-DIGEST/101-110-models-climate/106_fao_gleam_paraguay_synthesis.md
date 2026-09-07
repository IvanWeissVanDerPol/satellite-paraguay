# 106. FAO GLEAM-i Paraguay — Climate Change Knowledge Portal Synthesis

**Date:** 2026-09-03 (Round 2)

## GLEAM-i description

**GLEAM-i** (Global Livestock Environmental Assessment Model, interactive version) is a FAO tool that allows national-level analysis of livestock GHG emissions under various intervention scenarios. The 2017 v1 baseline is **updatable to v3.0 (2024)**.

### Inputs required
- Herd size (annual, by category)
- Feed types and quantities
- Manure management practices

### Outputs
- Annual emissions (CH4, N2O, CO2)
- Emission intensity (per kg protein)
- Enteric fermentation breakdown
- Manure management breakdown
- Scenarios for intervention

## Paraguay specifics

### Cattle (predominant)
- 2024: 13.6 million head (INFONA, MAG 2025)
- 89% Bos taurus (Nelore crosses)
- 11% Bos indicus
- 75%+ extensive grazing
- Stocking density 0.5-0.7 head/ha Chaco, 0.8-1.2 Oriental
- Average annual weight gain: 110-140 kg (Chaco, long fattening)
- Calving rates: 40-55% (low efficiency, baseline for intervention)

### Other
- Pigs: ~2.0 million head, mostly smallholder
- Sheep: ~500,000
- Goats: ~200,000
- Horses: ~500,000
- Poultry: ~30 million

### Predominant emissions source
- **Enteric fermentation (CH4) > 85% of total livestock GHG**
- N2O from manure: ~10%
- Manure direct CO2: < 5%

### Reference levels (paraguay 2024, MITIMAT-MADES):
- Total livestock emissions: ~26-30 MtCO2e/year
- Beef: 25 MtCO2e (~92% of livestock total)

## Policy context

The NDC 3.0 (2025) commits Paraguay to conditional 20% reduction. Livestock are a key target. Mitigation pathways:
1. Rotational grazing: estimated 5-12% emission reduction with same productivity
2. Pasture forage improvement: estimated 15-25% reduction
3. Stocking rate adjustment: 5-15% reduction
4. Supplementation/feedlot finishing: 15-30% reduction

## Action items

- Cite GLEAM-i baseline in thesis
- Use as a model-comparison benchmark for any deep-learning model
- Consider Paraguay-specific calibration of GLEAM-i as a thesis contribution

## File locations

- Cached prior: no cached GLEAM-i file yet
- Best prior: `/opt/data/profiles/ivan/research/iterations/41-60-yvy/56_paraguay_ndc3_full_text_oct2025.md` (NDC 3.0 PDF)

## Honest limitations

Detailed Paraguay GLEAM-i 2024 results would need to be accessed from FAO GLEAM-i portal (currently not in cache). This synthesis draws on the upper-order figures published by INFONA, MAG, and Paraguay's greenhouse gas inventory submission to UNFCCC.

## Related models

- **EPA FLIGHT** (Facility Level Information on Greenhouse Gases Tool) — for North America, not Paraguay
- **WRI CAIT 2.0** (Climate Action Tracker 2.0) — Paraguay page
- **GHG inventory:** official biennial update to UNFCCC
