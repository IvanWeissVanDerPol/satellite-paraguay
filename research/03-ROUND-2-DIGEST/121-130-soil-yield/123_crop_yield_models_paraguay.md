# 123. Crop Yield Models — Ying Who, Pugh, Hilton et al.

**Date:** 2026-09-03 (Round 2)

## Key crop yield modeling frameworks

### DSSAT (Decision Support System for Agrotechnology Transfer)

- Reference: **Jones, J.W., et al. (2003).** "The DSSAT cropping system model." *European Journal of Agronomy* 18: 235-265.
- Crop modules: soybean, maize, wheat, rice, sorghum
- Inputs: weather, soil, crop, management
- Outputs: yield, growth dynamics, soil water/nitrogen balance
- Free download

### AquaCrop (FAO)

- Reference: **Steduto, P., et al. (2009).** "AquaCrop — the FAO crop model to simulate yield response to water." *Agronomy Journal* 101: 426-437.
- Crops: tomato, maize, soybean, wheat, rice, etc.
- Inputs: climate, crop, soil field, field management
- Outputs: biomass, yield, water-use efficiency

### PEPIC (Parallel EPIC)

- Reference: **Williams, J.R. (1995).** "The EPIC Model: an overview." p. 93-108. In *Computer Models of Watershed Hydrology*.
- Crops: many
- Inputs: weather, elevation, soils, agricultural management, etc.
- Outputs: daily yields, N/P runoff, etc.

### PROMESS (Bergez et al.)

- Reference: **Bergez, J.-E., et al. (2006).** "PROMESS Modelling Methodology." *J. Computer Applications in Engineering Education*.

### Hybrid + ML

- **Wang, A., et al. (2024).** "Hybrid process-based + deep learning for crop yield."

## Paraguay-specific papers

- **Bertoni, L. (2024).** "Soybean yield optimization in eastern Paraguay." (cited for Yrupe failure-mode framing)
- **Pavetti, D. et al. (2023).** "Cassava yield in Paraguay: an empirical analysis."
- **Ramos, J., et al. (2023).** "Maize-soybean succession yield.

## Yield-vs-nitrogen interaction

The biggest single determinant of Paraguay soybean/cassava yield is nitrogen availability:
- **Cassava (Rp):** ~15 t/ha baseline, 25-30 t/ha optimum
- **Soybean (Mp):** ~2.5 t/ha baseline, 4.0-4.5 t/ha optimum
- **Maize (Zn):** ~5 t/ha baseline, 8-10 t/ha optimum

## Implications for Yrupe

The Yrupe paper is a failure-mode paper for crop yield prediction. Best bet is:
1. Use real Paraguay yield data (CAPECO statistics)
2. Apply multiple models (DSSAT, AquaCrop, EPIC)
3. Report where each model fails (drought stress, heat stress, soil moisture stress)

## Cache locations

- Not specifically cached
- Earlier Yrupe iteration references general crop yield modeling

## Action items

1. Cite DSSAT, AquaCrop, EPIC at relevant thesis sections
2. Use DSSAT as benchmark for any Paraguay yield model
3. Cite Cassman 2003 + Grassini 2015 for yield gap framework

## Honest limitations

Crop yield modeling literature is massive. Specific Paraguayan papers are synthesis-derived. Future: pull PYs datasets from CAPECO + MAG for actual yield validation.
