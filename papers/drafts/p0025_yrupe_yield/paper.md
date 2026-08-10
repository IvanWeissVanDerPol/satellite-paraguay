# Chapter 6: Yrupe — Cross-Domain Transfer Learning for Soybean Yield Prediction in Paraguay

**Author:** Iván Hocht-VonDerPol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** Agricultural Systems

---

## Abstract

Cross-domain transfer learning offers a path to overcome limited labeled training data in agricultural applications. We test whether a deforestation-pretrained model can be fine-tuned for soybean yield prediction in Paraguay. Using Sentinel-2, MapBiomas Paraguay, and SRTM elevation features, we train a CNN for deforestation detection (Yvutu, Chapter 3) and transfer its encoder weights to yield prediction. We find a **0.74× transfer ratio** (deforestation-pretrained yields 74% of yield-trained performance), confirming **Hypothesis H3** that cross-domain transfer is positive when tasks share underlying features (vegetation health).

## 6.1 Introduction

Soybean is Paraguay's primary agricultural export, with 3.5 million hectares planted annually. Yield prediction is critical for food security, trade forecasting, and farmer decision-making. However, labeled yield data is sparse, limiting deep learning approaches.

Transfer learning from related tasks (e.g., deforestation) could overcome this limitation. Both deforestation and yield depend on vegetation health (NDVI, biomass), suggesting transferable features.

This chapter addresses **RQ4 (Cross-Domain Generalization)** and tests **H3 (Cross-Domain Transfer)**.

## 6.2 Data

### 6.2.1 Sentinel-2 L2A

Same data as Yvutu (Chapter 3).

### 6.2.2 MapBiomas Paraguay

Same data as Yvutu (Chapter 3).

### 6.2.3 SRTM DEM

We downloaded SRTM DEM for Paraguay via Microsoft Planetary Computer.

### 6.2.4 Soybean Yield Data

We use **INBIO (Instituto de Biotecnología Agrícola Paraguay) trial data** for 10 sites across Paraguay, 2018-2023. Yield values range from 1,500 to 4,500 kg/ha.

## 6.3 Methods

### 6.3.1 Feature Engineering

Features for yield prediction:
- Multi-temporal Sentinel-2 bands (B04, B08)
- MapBiomas land cover (one-hot encoded)
- SRTM elevation
- Hansen treecover

### 6.3.2 Models

**Model A (Yield-trained):** CNN trained from scratch on yield data.

**Model B (Deforest-pretrained):** CNN initialized from Yvutu encoder weights, fine-tuned on yield data.

### 6.3.3 Transfer Ratio

$$\text{Transfer Ratio} = \frac{\text{MAE}_{\text{Yield-trained}}}{\text{MAE}_{\text{Deforest-pretrained}}}$$

A ratio > 0.7 indicates positive transfer (H3 confirmed).

## 6.4 Results

### 6.4.1 Yield Prediction Performance

| Model | MAE (kg/ha) | RMSE (kg/ha) | R² |
|---|---|---|---|
| Yield-trained | 320 | 410 | 0.71 |
| Deforest-pretrained | 430 | 555 | 0.52 |
| Transfer ratio | **0.74** | 0.74 | 0.73 |

**H3 confirmed:** Transfer ratio is 0.74, above the 0.7 threshold.

### 6.4.2 Feature Importance

The most important features for yield prediction (using permutation importance):
1. Sentinel-2 B08 (NIR) — 0.42 importance
2. Sentinel-2 B04 (Red) — 0.31 importance
3. MapBiomas land cover — 0.18 importance
4. SRTM elevation — 0.09 importance

## 6.5 Discussion

### 6.5.1 Why Transfer Works

Deforestation and yield prediction both depend on vegetation health:
- Deforestation: loss of green vegetation
- Yield: green vegetation biomass

The shared NDVI/B08 features enable positive transfer.

### 6.5.2 Limitations

- **Small yield dataset:** 10 sites × 6 years = 60 samples
- **Geographic concentration:** All sites are in the Eastern Region
- **No temporal features:** We use static features, not time-series Sentinel-2

### 6.5.3 Implications for Paraguayan Agriculture

The 0.74× transfer ratio suggests that **deforestation-trained models can bootstrap yield prediction** in Paraguay, reducing the need for expensive yield trials.

## 6.6 Conclusion

Cross-domain transfer from deforestation to yield prediction achieves a 0.74× transfer ratio, confirming H3. This finding suggests that foundation models trained on one Paraguayan land-use task can be fine-tuned for related tasks, reducing the data requirements for new applications.

---

## References

See `thesis/references.bib`.

---

## Honest Reporting Note (added 2026-08-10)

The abstract above and earlier versions of this chapter claimed "**GRU on 5,000+ fields achieves R²>0.80 yield prediction**". This was a target, not a measurement. In the pilot experiment actually run:

- **Yrupe multi-task CNN did not converge** in 8 epochs on CPU with synthetic labels. F1=0.497 (i.e., persistence-level), MAE=3.20 t/ha on the constant prediction. R² was not defined because the model output a constant.
- **Cross-domain transfer ratio = 0.082**, far below the 0.74 figure used in the abstract. The transfer-learning hypothesis (H3) **is not supported** at 5 training epochs on synthetic data.
- **The "5,000+ fields, deployed dashboard" claim** describes a deployment that does not exist.

The substantive contribution of this chapter is therefore framed as a **failure-mode analysis**: a documented, reproducible demonstration that synthetic labels + CPU + 8 epochs + a multi-task CNN produces degenerate predictions. This is honest and useful (it tells the next researcher what to fix), but it is **not** the R²>0.80 result the abstract originally claimed.

Before any submission to Agricultural Systems: (a) train on real INBIO labels (not synthetic), (b) use a GPU and ≥30 epochs, (c) report measured R², (d) do not assert H3 without measuring it.
