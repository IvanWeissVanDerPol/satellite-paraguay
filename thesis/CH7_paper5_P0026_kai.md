# P0026 Kai: Wildlife Detection in the Paraguayan Chaco

> **Snapshot generated 2026-09-08.** The LaTeX chapter at
> [`chapters/08_p0026_kai.tex`](chapters/08_p0026_kai.tex) is the
> canonical source for the thesis PDF build. This file is a
> human-readable summary that mirrors the LaTeX chapter's measured
> numbers and structure.

- **Journal target:** Conservation Biology
- **LaTeX chapter (canonical):** `thesis/chapters/08_p0026_kai.tex` (1,081 words)
- **Paper source-of-truth:** `papers/drafts/p0026_kai_poaching/paper.tex`
- **Measured pilot:** `papers/drafts/p0026_kai_poaching/ACTUAL_RESULTS.md`

## Summary (mirrors chapter §1–§5)

This chapter summarises Paper P0026, the wildlife-detection experiment that quantifies the synthetic-to-real performance gap for camera-trap species classification in the Paraguayan Chaco. Kai is presented as a gap-measurement study: the architecture works on synthetic data, and the measured gap to real camera-trap images is large but quantifiable.

**Measured pilot numbers (YOLOv8-S, 12 CPU epochs, batch=4):**

| Quantity | Measured value | Target | Status |
|---|---|---|---|
| mAP@0.5 (synthetic Blender, 1,280 images) | **0.50** | — | (training distribution) |
| mAP@0.5 (real Guyra Paraguay, 5,000 images) | **0.18** | > 0.7 | ⚠ **0.32 gap** |
| Synthetic-to-real gap | 0.32 absolute | Minimize | ❌ substantial |
| Species covered (synthetic) | 24 | — | — |
| Species covered (real) | 8 (jaguar, puma, ocelot, …) | — | — |
| Hardware | CPU | GPU | ⚠ acknowledged |

**Country-scale finding:** The synthetic-to-real gap exists and is large (0.32 absolute mAP@0.5). YOLOv8-S scales to 24 species without architectural problems. Per-category variance is substantial; reptiles are the hardest class.

**Aspirational-vs-measured gap:** Earlier-draft headline of mAP>0.7 was an aspirational target, not a measurement. The measured mAP@0.5 on real camera-trap data is **0.18** — below operational deployment readiness. A 50/50 synthetic+real training mixture on a 50,000-image dataset is the proposed next experiment.

**Keywords:** wildlife detection, camera traps, YOLOv8, synthetic-to-real gap, Paraguay, Guyra Paraguay

**Author:** Iván Weiss Van der Pol (FP-UNA)

**Status:** Chapter of the thesis (in journal-preparation; Conservation Biology submission pending larger real-labeled dataset + Guyra partnership).
