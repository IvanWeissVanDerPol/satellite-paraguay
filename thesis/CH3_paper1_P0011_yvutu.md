# P0011 Yvutu: Multi-Temporal Satellite Computer Vision for Chaco Deforestation

> **Snapshot generated 2026-09-08.** The LaTeX chapter at
> [`chapters/04_p0011_yvutu.tex`](chapters/04_p0011_yvutu.tex) is the
> canonical source for the thesis PDF build. This file is a
> human-readable summary that mirrors the LaTeX chapter's measured
> numbers and structure.

- **Journal target:** Remote Sensing of Environment
- **LaTeX chapter (canonical):** `thesis/chapters/04_p0011_yvutu.tex` (1,401 words)
- **Paper source-of-truth:** `papers/drafts/p0011_yvutu_deforestation/paper.tex`
- **Measured pilot:** `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md`
- **Honest Reporting Notes:** appended at end of paper.tex

## Summary (mirrors chapter §1–§5)

This chapter summarises Paper P0011, the multi-temporal deforestation detection study that anchors the thesis. Yvutu is presented as a system design with measured pilot results and an honest accounting of the gap between the as-pipeline-implemented behaviour and the originally aspirational headline metric. The chapter is written for the thesis reader who needs the measured numbers, the methods, and the gap analysis in one place — without having to read the full 11,378-word paper.

**Measured pilot numbers (15 synthetic Chaco tiles, 5 CPU epochs):**

| Model | F1 | Precision | Recall | Notes |
|---|---|---|---|---|
| Persistence baseline | 0.4968 | 0.4912 | 1.000 | Predict-all-deforestation |
| Random Forest | 0.4968 | 0.4912 | 0.762 | 320 trees |
| U-Net from scratch | **0.5592** | 0.0992 | 0.9873 | Over-predicts; recall-bound |
| Yvutu (Prithvi, mock) | 0.4968 | 0.4936 | 0.500 | transformers/numpy issue |

**Country-scale finding (real Hansen GFC v1.11 data):**
- 16,628 km² forest loss 2001–2023
- 2,755 MtCO₂e carbon emitted
- Peak deforestation 2012, partial recovery 2018–2020
- Concentration in Alto Paraguay Chaco (28.49%)

**Aspirational-vs-measured gap:** Earlier-draft headline framing was "Prithvi F1>0.85 vs U-Net F1=0.017 (50× improvement)". Measured pilot: U-Net F1=0.5592 (over-prediction); Prithvi mock F1=0.4968 (non-convergence in CPU budget). Real Prithvi run on 150 Chaco tiles is the next step — blocked on GPU budget.

**Keywords:** Earth observation, deep learning, Paraguay, p0011, sentinel-2, foundation models, Prithvi, MapBiomas, Hansen GFC, Chaco

**Author:** Iván Weiss Van der Pol (FP-UNA)

**Status:** Chapter of the thesis (in journal-preparation; RSE submission pending real Prithvi run + adviser email per Defensa/ADVISOR_PURSUIT_PACKET/EMAIL_01_cristaldo.md)
