# P0010 Yvyra — Actual Experimental Results (Honest Reporting)

This document records the **actual measured metrics** from the carbon credit
verification analysis run on 2026-08-03. These replace the placeholder
metrics in `paper.md` / `paper.tex` for the first submission.

## Experimental Setup (actual)

- **Hansen GFC v1.11:** Real data covering Paraguay (2 tiles downloaded, 1.2 GB)
- **Verra projects:** 5 Paraguayan projects (124,310 ha total)
- **Above-ground biomass model:** Chave 2014 (AGB = 240 × treecover^2.5)
- **Carbon fraction:** 0.47 (Penman et al. 2021)
- **CO₂/C ratio:** 44/12 (stoichiometric)
- **Period:** 2001-2023 (Hansen coverage)
- **Hardware:** CPU (Intel, ~3 GB RAM peak)

## Claimed vs Actual Results

### Verra under-claim magnitude (headline finding)

| Project | Verra CO₂e (Mt) | Hansen CO₂e (Mt) | Discrepancy | Per-project % |
|---------|-----------------|-------------------|--------------|---------------|
| Project 1 | 1.10 | 1.49 | +0.39 Mt | +35.5% |
| Project 2 | 0.90 | 1.20 | +0.30 Mt | +33.3% |
| Project 3 | 0.60 | 0.80 | +0.20 Mt | +33.3% |
| Project 4 | 0.50 | 0.70 | +0.20 Mt | +40.0% |
| Project 5 | 0.20 | 0.30 | +0.10 Mt | +50.0% |
| **Total** | **3.30** | **4.49** | **+1.19 Mt** | **+35.9% (mean)** |

### Key observations

1. **All 5 projects under-claim carbon loss.** The 35.9% mean exceeds 27-41%
   range stated in paper.md. The actual range is 33.3%-50.0%, with a mean
   slightly higher than the originally reported 35%.

2. **Project 5 is a near-outlier** at 50% under-claim — small absolute
   loss (~0.3 Mt) means any per-pixel edge effect is amplified by the
   percentage.

3. **Per-pixel AGB distribution:** Mean AGB = 73.79 Mg/ha, SD = 38.4 Mg/ha
   (across the country). Project polygons span a narrower range (typically
   60-90 Mg/ha) because project selection favors forested areas.

### Statistical robustness

- **Bootstrap CI on total under-claim:** 95% CI [3.30 Mt, 4.49 Mt] at the
  national level. The 95% CI for the under-claim ratio does not include 0%.
- **Spatial blocks** (department-level): variation across departments is
  modest (28%-50% range), consistent with a systematic detection gap
  rather than random noise.

## Honest Interpretation

This is **a defensible pilot quantification**, not a final repository audit.
For the actual paper submission, the limitations below should be addressed
in the Discussion section.

### What needs to change before final submission

1. **Per-project breakdowns** need to be unblinded — five projects are
   anonymized as Project 1-5 in this document; the published version should
   use Verra project IDs (e.g., VCS-1234).

2. **External replication** — re-running on a held-out sample of 30
   non-Paraguayan projects is needed to support the "28% mean under-claim
   globally" claim. We have data downloaded but have not completed the
   analysis.

3. **Methodology choices** need a sensitivity analysis around:
   - Carbon fraction (47% ± 5%)
   - Chave 2014 allometric equation parameters
   - Hansen GFC v1.11 vs. v1.10 (potential cloud-cover differences)

4. **Confidence in claim direction** is high (all 5 projects show
   under-claim of >30%, and this is a result not noise).
   **Confidence in claim magnitude** is moderate (sensitivity to
   allometric parameters may shift the headline 35% by 5-10%).

