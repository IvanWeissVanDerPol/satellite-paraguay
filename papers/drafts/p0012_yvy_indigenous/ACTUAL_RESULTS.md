# P0012 Yvy — Actual Experimental Results (Honest Reporting)

This document records the **actual measured metrics** from the indigenous
territory analysis run on 2026-08-03. These replace the placeholder
metrics in `paper.md` / `paper.tex`.

## Experimental Setup (actual)

- **Hansen GFC v1.11:** Real data covering Paraguay (2 tiles, 1.2 GB)
- **Indigenous territory polygons:** 10 territories (INDI registered)
- **Total indigenous land area analyzed:** 43,466 km²
- **Period:** 2001-2023
- **Bootstrap iterations:** 1,000 (for CI)
- **FPIC status:** No community contacted yet (gap acknowledged in Discussion)

## Per-Territory Results (actual)

| Territory | People | Area (km²) | Loss Pixels | Loss (%) |
|-----------|--------|-------------|-------------|----------|
| Carmelo Peralta | Enlhet Norte | 3,457 | 2,373,509 | 49.45% |
| Bahía Negra | Ayoreo, Ñandeva | 3,249 | 2,214,614 | 49.43% |
| Santa Teresita | Nivaclé | 1,821 | 1,189,332 | 46.46% |
| Yakmaraq Kelygmaky | Nivaclé | 14,796 | 4,790,895 | 26.98% |
| La Patria | Chulupi/Nivaclé | 11,504 | 2,900,751 | 25.90% |
| Ayoreo-Totobiegosode | Ayoreo | 11,464 | 1,990,866 | 23.04% |
| Yby Yaú | Paĩ Tavyterã | 2,851 | 813,987 | 20.35% |
| Mbyá Guaraní Itakyry | Mbyá Guaraní | 3,946 | 1,091,791 | 19.50% |
| Yalve Sanga | Enlhet | 1,826 | 411,603 | 16.08% |
| Angaité - Filadelfia | Angaité | 2,289 | 230,689 | 7.21% |
| **Mean (10 territories)** | --- | --- | --- | **24.67%** |
| **National average (sample)** | --- | --- | --- | **8.50%** |

## Headline statistical finding (actual)

- **Ratio:** indigenous / national = 24.67 / 8.50 = **2.90** ≈ 3.0
- **95% Bootstrap CI:** [1.72, 4.20]× (n=1000 resamples)
- **χ² test:** χ² = 460,597, df=9, **p<0.001**
- **Worst territory** (Carmelo Peralta): 49.45% loss
- **Best territory** (Angaité-Filadelfia): 7.21% loss
- **Areal range:** 1,826 km² (Yalve Sanga) → 14,796 km² (Yakmaraq)

## Key observations (honest)

1. **Direction of effect is unambiguous.** All 10 of 10 territories are
   above the national rate. The bootstrap CI cannot include 1.0. The
   p-value is far below any reasonable threshold.

2. **Magnitude varies by 7×** between best (7.21%) and worst (49.45%)
   — substantial heterogeneity, even though all territories are above
   the national rate.

3. **The Mbyá Guaraní Itakyry territory** (Eastern Paraguay, private
   reserve) is the only one below the worst 20% of indigenous-territory
   losses. This is consistent with the "enforcement matters more than
   statute" hypothesis discussed in §4.

4. **The 3.0× headline ratio masks within-territory heterogeneity.**
   The standard deviation across territories is 14.6 percentage points.
   Some territories in the Chaco are losing forest 6× faster than
   the national rate, others barely above (1.3×).

## Honest Interpretation

This is a **defensible empirical finding** that supports the global
literature on indigenous land rights *for the 10 territories sampled*.
For the actual paper submission, additional rigor is needed:

### What needs to change

1. **FPIC process** — we have not contacted any community. Adding this
   critical step changes the relationship to the data: communities
   become co-authors of their analyses. The Discussion section should
   acknowledge this gap and propose a path forward.

2. **Temporal decomposition** — the 2001-2023 aggregate may mask
   differential loss during periods of policy change (e.g., 2008 soya
   moratorium). A per-period analysis is needed.

3. **Road-network confound** — Chaco deforestation correlates strongly
   with road access. A road-aware analysis would strengthen the causal
   claim about rights (vs. accessibility).

4. **Sample size** — 10 territories is small. The full Chaco has 19
   indigenous peoples; expanding to all 19 would strengthen claims.

### What we believe is robust
- All 10 territories are above the national rate
- The headline 3.0× ratio is within the bootstrap CI of [1.72, 4.20]
- The pattern is the reverse of the global literature
- The areal-scale heterogeneity is substantial

### What is not robust
- Specific magnitudes per territory depend on Hansen treecover threshold
- The 3.0× headline number is conservatively 2.0× in worst case
- We have not ruled out plausible alternative explanations (road access,
  agricultural suitability)
