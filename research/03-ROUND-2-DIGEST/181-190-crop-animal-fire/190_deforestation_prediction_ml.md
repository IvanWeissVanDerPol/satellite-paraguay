# 190. Paraguay Deforestation Prediction + Coffee Machine Learning (Round-2)

**Date:** 2026-09-03 (Round 2)

## Reference

- **Hethcoat, M., et al. (2024).** "Machine learning for deforestation prediction."
- **Masolele, M., et al. (2024).** "Deep learning for forest disturbance mapping."

## Background

Machine learning approaches:
- **Gradient Boosted Trees** (XGBoost, LightGBM)
- **Random Forest** (Breiman 2001)
- **Random Survival Forests**
- **Deep Learning** (CNNs, Transformers)

## Paraguay-specific datasets

| Dataset | Coverage | Period | Use |
|---|---|---|---|
| GFW | Global | 2003-present | Real-time alerts |
| Hansen GFC v1.12 | Global | 2000-2023 | Year-of-loss classification |
| RADD | Global | 2019-present | C-band SAR-based alerts |
| GLAD Alerts | Tropics | 2017-present | Weekly updates |
| PRODES | Brazil | 1988-2024 | Annual classification |

## Feature engineering

### Predictor variables
- **Distance to roads** (OpenStreetMap)
- **Population density** (WorldPop)
- **Elevation** (SRTM/Copernicus 30m)
- **Slope/aspect** (Copernicus)
- **Protected area overlap** (WDPA)
- **Previous loss** (Hansen)
- **Soil type** (SoilGrids)
- **Climate** (CHIRPS, ERA5-Land)

### Targets
- Year-of-loss
- Probability of loss in next 5 years
- Probability of pixel being protected area

## Implications for thesis

### Yvutu
- Predict deforestation probability
- Assess which features most predictive

## Cachement locations

- General deforestation references

## Action items

1. Cite Hethcoat 2024 + Masolele 2024
2. Build Paraguay-specific model
3. Apply to thesis

## Honest limitations

Reconstructions.
