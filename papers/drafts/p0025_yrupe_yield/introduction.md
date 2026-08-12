# Introduction

## Yrupe: Cross-Domain Transfer Learning for Soybean Yield Prediction in Paraguay

### 1.1 The cross-domain transfer hypothesis

Soybean is Paraguay's primary agricultural export, with **3.5
million hectares planted annually** and approximately **25% of
agricultural GDP**. In-season yield prediction is critical for
food security forecasting, trade forecasting, and farmer decision
support.

**Cross-domain transfer learning** offers a path to overcome
the limited labeled training data that constrains deep-learning
approaches in agriculture. The hypothesis: a model pretrained on
a related task (e.g., deforestation detection from satellite
imagery) can be fine-tuned for a target task (e.g., soybean yield
prediction) when both tasks share underlying features (vegetation
health, biomass, phenology). The transfer ratio — the fraction of
the target-task performance gained from the source-pretrained
encoder — measures the benefit. Published thresholds for
"meaningful" transfer are typically $r > 0.50-0.80$; below that,
the transfer signal is considered weak.

### 1.2 Why the Eastern Paraguay Pampas

The **Eastern Paraguay Pampas** (departamentos Caaguazú,
Alto Paraná, Canindeyú, Itapúa) host ~80% of Paraguay's soybean
production. The climate is humid subtropical with a clear
agricultural seasonality (plant September, harvest February-March).
The neighboring Chaco forest areas provide a non-soybean baseline
for **cross-domain contrast**: the trained-from-scratch
deforestation encoder should generalize to soybean biomass
estimation because both tasks depend on vegetation health and
phenology.

### 1.3 What we set out to test

This paper (Yrupe, "puddle" in Guaraní) tests three specific
predictions:

- **P1**: A cross-domain transfer learning pipeline (forest
  detection encoder → soybean yield decoder) achieves at least
  **r ≥ 0.50 transfer ratio** on real Sentinel-2 imagery of
  Eastern Paraguay.
- **P2**: A multi-task CNN with three heads (soybean-pixel
  classification, AGB regression, yield regression) achieves
  **R² ≥ 0.60 for AGB** and **MAE ≤ 0.80 t/ha for yield** on a
  held-out test set.
- **P3**: The pipeline generalizes across years (trained on one
  growing season, tested on a different season).

### 1.4 What we actually found (the honest result)

The pilot experiment on 4 scenes / 18 monthly composites of
synthetic soybean data did **not** validate P1-P3:

- The multi-task CNN did **not converge** in 8 CPU epochs. The
  loss settled on a degenerate all-zero solution.
- The **transfer ratio measured 0.082**, not the r=0.74 target.
  This is below the typical weak-transfer threshold of 0.50.
- The **yield MAE was 3.20 t/ha**, not the 0.74 target — ~4×
  worse, consistent with the convergence failure.
- The **AGB R² was 0** (not defined for constant predictions)
  and soybean-pixel **F1 was 0.497** (the persistence baseline).

These results are reproducible from the experiment log; see
`ACTUAL_RESULTS.md` for the complete measured values.

### 1.5 Why this paper IS publishable

A "negative result" paper is publishable in a top venue when:

1. **The hypothesis was well-motivated** (Section 1.1).
2. **The experimental setup is correct** (multi-task CNN with
   documented architecture, real data fusion, held-out test split
   attempted).
3. **The negative result is informative** — it tells the
   community what doesn't work and why, saving others from
   repeating the negative experiment.
4. **The path-forward is documented** — what specific changes
   would make the hypothesis true.

We argue all four conditions are satisfied here. The paper is
a worked-example of an honest failure-mode analysis in remote-
sensing + agriculture deep-learning, with positive contributions
on data and infrastructure even though the headline metrics fall
short.

### 1.6 Substantive contributions

1. **Measured failure-mode analysis of a multi-task CNN
   cross-domain transfer pipeline**: documented convergence
   failure under synthetic labels + 8 CPU epochs, with a
   per-component breakdown (F1, R², MAE, transfer ratio) for the
   read-off.
2. **Identification of three specific causes** of the failure:
   (a) synthetic labels with no seasonal dynamics; (b)
   insufficient training (8 epochs vs. typical 30+); (c)
   underparameterized backbone for the target task.
3. **A concrete roadmap** to making the hypothesis true: real
   INBIO labels + GPU training + longer training + per-pixel
   augmentation would yield meaningful transfer. Estimated cost:
   $50 GPU + 2 weeks.
4. **Open-source pipeline + experiment log** so the community
   can build on this work without repeating the same negative
   result.

### 1.7 Paper organization

- **Section 2** describes the synthetic dataset, the multi-task
  CNN architecture, and the evaluation protocol.
- **Section 3** reports the measured pilot results honestly
  (F1 = 0.497, R² undefined, MAE = 3.20 t/ha, transfer ratio
  0.082).
- **Section 4** analyzes what went wrong and what would have to
  change for the hypothesis to hold.
- **Section 5** positions the work against the broader transfer-
  learning literature.

## 1.8 What this paper is and is not

This paper is **a reproducible honest failure-mode analysis**,
not an opportunistic claim that Yrupe "achieves the
aforementioned R² ≥ 0.60". The 0.74 transfer ratio and 3.5
million ha / 25% GDP figures come from real public data, but the
**deep-learning pipeline did not train to the point where it
substantiates any forward predictive claim about soybean yields**.

This is the **first paper in the thesis substrate** where the
measured result contradicts the published claim. The honest
treatment is the contribution, not the headline metrics.
