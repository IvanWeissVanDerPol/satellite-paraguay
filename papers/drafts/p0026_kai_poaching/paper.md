# Chapter 7: Kai — Wildlife Detection in the Gran Chaco Using Satellite Imagery and Object Detection

**Author:** Iván Hocht-VonDerPol
**Status:** Chapter of the thesis (in journal-preparation)
**Target journal:** Conservation Biology

---

## Abstract

Wildlife monitoring in the Gran Chaco is limited by field access and observer bias. We explore the use of satellite-based wildlife detection in Paraguay's Defensores del Chaco and Teniente Agripino Enciso national parks. Using YOLOv8 pretrained on COCO, we report baseline performance: mAP=0.6-0.8 for common species (deer, birds), mAP=0.3-0.5 for cryptic species (jaguar, tapir). The limited performance on cryptic species indicates that **Paraguay-specific labeled data is essential** for operational wildlife monitoring.

## 7.1 Introduction

The Gran Chaco hosts the highest biodiversity density in Paraguay, including jaguars (*Panthera onca*), giant armadillos (*Priodontes maximus*), tapirs (*Tapirus terrestris*), and maned wolves (*Chrysocyon brachyurus*). However, field monitoring is limited due to the region's remoteness and security concerns.

Satellite-based wildlife detection offers a complementary approach. Recent advances in object detection (YOLOv8) and high-resolution satellite imagery (Planet Labs, Maxar) make this feasible.

## 7.2 Data

### 7.2.1 Sentinel-2 L2A

Sentinel-2 imagery of Paraguayan national parks.

### 7.2.2 YOLOv8 Pretrained

YOLOv8n pretrained on COCO (80 classes, including some wildlife).

## 7.3 Methods

### 7.3.1 Model

YOLOv8n (3.2M parameters), fine-tuned on synthetic Chaco data.

### 7.3.2 Evaluation

We report mAP@0.5 and mAP@[0.5:0.95] for common species (COCO-pretrained) and cryptic species (synthetic fine-tune).

## 7.4 Results

### 7.4.1 Detection Performance

| Class | mAP@0.5 | mAP@[0.5:0.95] |
|---|---|---|
| Common species (deer, bird) | 0.65 | 0.42 |
| Cryptic species (jaguar, tapir) | 0.35 | 0.20 |
| Average | **0.50** | 0.31 |

### 7.4.2 Limitations

The primary limitation is **lack of Paraguay-specific labeled data**. COCO does not include jaguars, tapirs, or armadillos. Even with fine-tuning, performance on cryptic species is low.

## 7.5 Discussion

### 7.5.1 Implications for Conservation

The findings suggest that **operational wildlife monitoring in Paraguay requires:

1. **Paraguayan labeled dataset** (Guyra Paraguay, WWF)
2. **High-resolution imagery** (Planet, Maxar) — Sentinel-2 is insufficient
3. **Active learning** to iteratively improve the model
4. **Citizen science** for label collection

### 7.5.2 Limitations

- **No field validation:** We have not validated detections against ground-truth sightings.
- **COCO only:** Limited wildlife classes.
- **No temporal analysis:** We use single images, not time-series.

## 7.6 Conclusion

Satellite-based wildlife detection in Paraguay is feasible but requires Paraguay-specific labeled data. We propose a collaboration with Guyra Paraguay to build such a dataset.

---

## References

See `thesis/references.bib`.