# P0011 Yvutu — Highlights for Remote Sensing of Environment

RSE requires 3-5 bullet points, each maximum 85 characters.

---

## Honest Submission Highlights (2026-08-13 update)

The bullet points below replace the original draft's aspirational claims
with **measured** numbers from the 2026-08-03 pilot run. See
`ACTUAL_RESULTS.md` for the source values.

1. **Country-scale deforestation quantification (real Hansen GFC v1.11): 16,628 km² of loss over 2001-2023, equivalent to 2,755 MtCO₂e.**

2. **Per-department analysis showing 28.49% loss in Alto Paraguay, with the Chaco frontier accounting for ~47.8% of national loss.**

3. **Per-indigenous-territory analysis showing 2.90× the national rate (95% BCa CI [1.72, 4.20]×, χ² = 460,597, df = 9, p < 0.001), with Carmelo Peralta worst at 49.45% loss.**

4. **End-to-end ML pipeline + measured pilot baseline: F1 = 0.5592 (U-Net from scratch) and F1 = 0.4968 (Yvutu with Prithvi mock fallback that did not converge in 5 CPU epochs).**

5. **The aspirational "F1 = 0.876 vs F1 = 0.017 from-scratch" claim from earlier drafts is REFUTED by the measured pilot. Honest Reporting Note appended to paper.md documents this.**

---

## Display Items

**Figure 1.** Country-scale deforestation map (2023 state) and per-
department breakdown (Alto Paraguay dominant).

**Figure 2.** Per-indigenous-territory disparity visualization
(Carmelo Peralta + Bahía Negra as worst cases).

**Figure 3.** ML pilot run: U-Net vs. Yvutu-Prithvi-mock on 15
synthetic tiles, confusion matrix and per-class breakdown.

**Table 1.** Per-department loss statistics (18 departments).

**Table 2.** Per-indigenous-territory analysis (10 territories).

**Table 3.** ML pilot metrics comparison table.

---

## Author Contributions (CRediT taxonomy)

| Author | CRediT Roles |
|--------|--------------|
| **Iván Weiss Van der Pol** | Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing — original draft; Visualization |
| **Juan Carlos Cristaldo** | Supervision; Resources; Writing — review & editing |

---

## Funding Sources

This work was supported by:

- UNA FADA — research infrastructure and compute time
- Personal equipment and computational resources (the agent-side sandbox)

No external grant number is associated with this pilot.

---

## Data + Code Availability

- **Code**: CC-BY-NC-4.0 (LICENSE).
- **Hansen GFC v1.11**: CC-BY-4.0.
- **Indigenous territory polygons**: CC-BY-4.0 (paraguay-geodata).
- **Pretrained pipeline weights** (planned): `outputs/p0011/unet_weights.pt`.
- **Measured-results log**: ACTUAL_RESULTS.md.

---

## RSE Honest-Submission Statement

This paper is submitted **as a reproducible baseline contribution**.
The measured pilot performance does not validate the aspirational
headline published in earlier drafts of this chapter. We explicitly
state the gap so reviewers do not discover it themselves.

If the editorial team prefers the paper framed as a methodology +
measured-results contribution, we are happy to revise the abstract
to lead with the operationalization plan (Section D.4 of
`discussion.md`) rather than the headline metric.
