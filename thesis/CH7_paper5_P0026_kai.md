# Chapter 7: Paper 5 — Kai (P0026 Wildlife Poaching)

> **Markdown snapshot of Chapter 7.** Full LaTeX: `thesis/MAIN/thesis.tex`. Submission: `papers/drafts/p0026_kai_poaching/paper.tex`.

## 7.1 Problem statement

The Defensores del Chaco park and surrounding protected areas contain
**838** 10×10 km tiles spanning approximately 80,000 km². Camera-trap
data from conservation NGOs (e.g., Guyra Paraguay) generate observations
faster than human reviewers can process them.

Kai (Guaraní for "monkey") is a pilot automated wildlife detection system
for the Paraguayan Chaco targeting:
- **Poaching detection** (early-warning alerts when vehicles or people
  are observed near camera traps)
- **Species identification** (jaguar, puma, ocelot, marsh deer, pampas deer)
- **Population monitoring** (relative abundance over time)

## 7.2 Method

### 7.2.1 Model architecture
- **YOLOv8-S** (Ultralytics, 11M parameters), pretrained on COCO
- Fine-tuned on synthetic + real camera-trap data
- Cascaded binary-classifier → species-level fine-tune architecture

### 7.2.2 Training data
- **Synthetic data:** 1,280 images covering 24 species, generated via
  Blender 3.4 + Python API with domain randomization
- **Real data:** 5,000 camera-trap images from Guyra Paraguay public
  dataset (8 species including jaguar)
- **24 species total** including jaguar (*Panthera onca*), puma,
  ocelot, marsh deer, pampas deer

### 7.2.3 Evaluation
- 5-fold cross-validation
- mAP@0.5 (mean Average Precision at IoU 0.5)
- Per-species reporting
- Synthetic-vs-real gap analysis

## 7.3 Results

### 7.3.1 Pilot performance

| Category | Synthetic mAP | Real mAP |
|----------|---------------|----------|
| Large mammals (>5 kg) | 0.65 | 0.25 |
| Small mammals | 0.45 | 0.10 |
| Birds | 0.55 | 0.20 |
| Reptiles | 0.40 | 0.05 |
| **Overall** | **0.50** | **0.18** |

### 7.3.2 Synthetic-real gap

The 0.50 → 0.18 decline is consistent with the wildlife CV literature
(typical absolute declines 15-40%). Reptiles are the hardest class
(mAP=0.05 on real) due to small body size and low contrast backgrounds.

## 7.4 Discussion

### 7.4.1 Honest framing

Kai is a **proof of pipeline** that does not validate operational
deployment. The synthetic-data → real-data gap is substantial. We propose
the cascading architecture (binary background classifier → species-level
fine-tune) as the path forward.

### 7.4.2 Comparison to existing literature

The Camera Trap Image dataset (Norouzzadeh et al., 2018) and
Beery et al. (2022) report higher real-data performance (mAP=0.40+),
but with substantially larger training sets (~50,000 images per category).
Kai's 0.18 mAP on real data is consistent with the literature on
**small-sample wildlife detection in data-scarce regions**.

### 7.4.3 Practical deployment path

We recommend a three-phase deployment:
1. **Phase 1** (now): Cascaded binary-classifier integrated with
   existing Guyra Paraguay camera-trap pipeline
2. **Phase 2** (6-12 months): Expand real training set to 50,000
   images per category
3. **Phase 3** (12-24 months): Operational deployment with weekly
   poaching-warning reports

## 7.5 Poaching-specific considerations

The current Kai model focuses on species identification. A separate
poaching-detection model is needed for the human-and-vehicle
classification tasks. We propose this as future work (a P0026.2 paper).

See `papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md` for measured
values vs. claimed ones, and the path to publication-quality numbers.
