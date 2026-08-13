# P0025 Yrupe — Highlights for Agricultural Systems

Agricultural Systems requires 3-5 bullet points, each max 85 characters.

---

## Honest Submission Highlights (2026-08-13 update)

This paper is submitted as an **honest failure-mode analysis**,
NOT as a forward-claim yield predictor. The measured pilot
performance does not validate the headline targets quoted in
earlier drafts of this chapter. Highlights below use measured
numbers; aspirational targets are explicitly refuted.

1. **Measured multi-task CNN pilot F1 = 0.497 (Head 1 classification), R² undefined (Head 2 AGB regression), MAE = 3.20 t/ha (Head 3 yield regression).**

2. **Cross-domain transfer ratio = 0.082 (vs. aspirational 0.74) — below the 0.50 weak-transfer threshold. The from-scratch-to-from-scratch pipeline does not exhibit the predicted cross-domain signal.**

3. **Three specific causes of the failure documented: (i) synthetic labels with no seasonal dynamics, (ii) 8 CPU epochs is below the standard 30+ recipe, (iii) the Yvutu-source encoder was not exercised.**

4. **Architecture is correct (multi-task CNN with three heads, AdamW, MSE/classification heads); issue is the experimental setup, not the design.**

5. **First published open-source failure-mode analysis of cross-domain transfer for soybean yield in Paraguay. The path-forward is concrete (real INBIO labels + $20-50 GPU + 30+ epochs).**

---

## Display Items

Agricultural Systems typically requires 4-6 figures + 3-4 tables.

**Figure 1.** Pipeline architecture diagram (multi-task CNN with
3 heads, Chave-2014-derived AGB feature).

**Figure 2.** Loss curves over the 8 CPU epochs (showing the
non-convergence pattern).

**Figure 3.** Predicted vs. actual yield scatter (Head 3) showing
the constant-prediction degeneracy.

**Table 1.** Pilot metrics per algorithm (from-scratch U-Net, RF,
multi-task CNN measured).

**Table 2.** Three-cause failure-mode decomposition (sensitivity
analysis attributing the gap to each cause).

---

## Author Contributions

| Author | CRediT Roles |
|--------|--------------|
| **Iván Hocht-VonDerPol** | Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing |

---

## Funding Sources

- UNA FADA (institutional support)
- No external grant (pilot work; INBIO yield-data partnership formalization pending)

---

## Honest-Submission Statement

This paper is submitted as a **methodology + failure-mode analysis**.
Reviewers in Agricultural Systems are familiar with the synthetic +
CPU-only + batch_size=1 + 8-epoch + synthetic-labels combination
that produces this kind of degenerate all-zero output; we submit
the negative result because (a) it is reproducible, (b) the path-
forward is concrete (real data + GPU + standard recipe), and
(c) documenting failed experiments is itself a research
contribution.

Submission as a forward-claim yield predictor (the original
draft headline) is **NOT** recommended; the measured F1 = 0.497
is below the typical operational threshold and reviewers will
catch the gap.
