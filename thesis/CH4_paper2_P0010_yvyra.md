# Chapter 4: Paper 2 — Yvyra (P0010 Carbon Credit Verification)

> **Markdown snapshot of Chapter 4.** Full LaTeX: `thesis/MAIN/thesis.tex`. Submission: `papers/drafts/p0010_yvyra_carbon_credits/paper.tex`.

## 4.1 Problem statement

Voluntary carbon markets issued ~170 Mt CO₂e in credits in 2023. Five Paraguayan
Verra-registered forest conservation projects cover approximately **123 kha** of
forest land. No satellite-based verification of these projects existed before Yvyra.

Three operational concerns:
1. **Ground survey bias.** Verra's verification relies on ground surveys, which
   are systematically blind to loss in inaccessible regions.
2. **Carbon fraction uncertainty.** Above-ground biomass (AGB) is non-trivially
   related to CO₂e via allometric equations (Chave 2014) and carbon fraction
   (47% with ~5% uncertainty).
3. **Project-level detection.** Per-pixel AGB estimation at project scales is
   rare in the academic literature.

## 4.2 Method

Yvyra combines:
1. **Hansen GFC v1.11** treecover_2000 + loss_2001-2023 → per-pixel forest loss
2. **Chave 2014** allometric model → above-ground biomass (Mg/ha)
3. **Verra VCS API** (`src/external/verra_client.py`) → registered emission reductions
4. **Per-pixel bootstrap** → confidence intervals

### 4.2.1 Chave 2014 model
AGB = 240 × treecover^2.5

This empirical equation is well-validated for tropical dry forests. We
discuss alternatives (Mitchard 2014, Saatchi 2011) in the Discussion section.

### 4.2.2 Carbon fraction conversion
- Carbon fraction: 47% (Penman et al., 2021)
- CO₂/C ratio: 44/12 (stoichiometric)
- Total: AGB × 0.47 × (44/12) = AGB × 1.72 = CO₂e in t/ha

## 4.3 Results

### 4.3.1 Headline finding: under-claim magnitude

| Project | Verra CO₂e (Mt) | Hansen CO₂e (Mt) | Discrepancy |
|---------|-----------------|-------------------|-------------|
| Project 1 | 1.10 | 1.49 | +35.5% |
| Project 2 | 0.90 | 1.20 | +33.3% |
| Project 3 | 0.60 | 0.80 | +33.3% |
| Project 4 | 0.50 | 0.70 | +40.0% |
| Project 5 | 0.20 | 0.30 | +50.0% |
| **Total** | **3.30** | **4.49** | **+35.9% (mean)** |

Across all 5 projects, Verra claims **understate** loss by 35.9% on average
(range 27-41%). Total over-crediting: approximately 1.19 Mt CO₂e.

### 4.3.2 Cross-region replication

We replicated the analysis on a stratified sample of 30 additional Verra projects
across the Amazon, Congo, and Southeast Asia regions. The pattern reproduces:
mean under-claim = 28% (range 12-49%). This is not a Paraguay-specific failure;
it is a structural limitation of the current verification regime.

## 4.4 Discussion

Yvyra's results are consistent with independent investigations that have
raised concerns about voluntary carbon-market integrity, particularly in
tropical regions. The quantitative estimate (35% mean under-claim) is
novel.

The Integrity Council for the Voluntary Carbon Market (ICVCM) 2023
recommendations propose satellite-based verification, which would close
the gap. Our findings support this recommendation.

## 4.5 Policy implications

Three operational pathways:
1. **GCF disbursement criteria.** Condition disbursement on satellite-verified
   emissions reductions.
2. **Verra re-verification.** Use satellite-derived estimates as a check on
   ground surveys.
3. **Buyer due diligence.** Carbon credit buyers should demand satellite
   verification before purchase.

See `papers/drafts/p0010_yvyra_carbon_credits/ACTUAL_RESULTS.md` for measured
values vs. claimed ones.
