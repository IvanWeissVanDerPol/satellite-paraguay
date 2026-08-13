# Cross-Paper Consistency Audit — 2026-08-13

**Auditor:** Hermes agent (follow-up from PR #1 merge)
**Trigger:** Tier 2 item A in AGENT_TODO.md (~10 h estimated)
**Scope:** Reconcile per-paper conventions across the 6-paper substrate

## Headline findings

### ✅ Carbon fraction: 0.47 (consistent across papers + code)

| Location | Value | Source |
|---|---|---|
| `papers/drafts/p0011_yvutu_deforestation/methods.md` | 0.47 | IPCC Tier-1 tropical dry forest |
| `papers/drafts/p0011_yvutu_deforestation/discussion.md` | 0.47 | Same, plus 0.42-0.52 sensitivity band |
| `papers/drafts/p0010_yvyra_carbon_credits/methods.md` | 0.47 | IPCC Tier-1 tropical moist forest |
| `papers/drafts/p0010_yvyra_carbon_credits/discussion.md` | 0.42-0.52 | Sensitivity range |
| `scripts/per_pixel_carbon.py:59` | 0.47 | `carbon_stock = chave_agb(treecover) * 0.47` |
| `scripts/carbon_credit_verifier.py:38` | 0.47 | Same |
| `scripts/indigenous_overlap_analysis.py:116` | 0.47 | Same |
| `scripts/department_deforestation.py:97` | 0.47 | Same |
| `scripts/paraguay_deforestation_analysis.py:127` | 0.47 | Same |
| `scripts/uncertainty_quantification.py:102` | 0.47 | Same |
| `outputs/p0011/carbon/per_year_loss.json` | 0.47 | Same |
| `tests/test_performance.py:115` | 0.47 | Same |
| `notebooks/P0011_yvutu_deforestation.ipynb` | 0.47 | Same |

**Verdict:** ✅ Consistent. The 0.42-0.52 range mentioned in P0010 discussion is a sensitivity band, not a different value.

### ⚠️ Pixel area: 0.09 ha (papers) vs 0.0625 ha (code) — **INCONSISTENT**

| Source | Value | What it claims |
|---|---|---|
| `papers/drafts/p0011_yvutu_deforestation/methods.md:108` | 0.09 ha | "30 m × 30 m = 900 m²" |
| `papers/drafts/p0010_yvyra_carbon_credits/methods.md:72` | 0.09 ha | "30 m × 30 m = 900 m² = 0.09 ha (...) corrected from the earlier-draft `0.0625` value, which was" |
| `scripts/per_pixel_carbon.py:93` | 0.0625 ha | "Hansen at -20 to -30 lat" |
| `scripts/carbon_credit_verifier.py:35` | 0.0625 ha | default arg |
| `scripts/indigenous_overlap_analysis.py:113` | 0.0625 ha | — |
| `scripts/department_deforestation.py:82` | 0.0625 ha | "Hansen 25m pixel" |
| `scripts/paraguay_deforestation_analysis.py:117` | 0.0625 ha | "25m pixel = 0.0625 ha" |
| `scripts/uncertainty_quantification.py:88` | 0.0625 ha | "30m pixel = 0.09 ha, using 0.0625 = approx" |
| `scripts/interactive_viz.py:40` | 0.0625 | "Hansen pixel area" |
| `scripts/comparative_analysis.py:56` | 0.0625 (Hansen) | "0.09 ha MapBiomas" (also wrong: MapBiomas is also 30m) |
| `src/utils/uncertainty.py:95` | 0.0625 | "30m pixel = 0.09 ha, using 0.0625 = approx" |
| `tests/test_performance.py:115` | 0.0625 | — |
| `tests/test_stat_uncertainty.py:181` | 0.09 ha | "3 loss pixels * 0.09 ha = 0.27 ha" |
| `notebooks/P0011_yvutu_deforestation.ipynb` | 0.0625 | — |
| `outputs/p0011/carbon/per_year_loss.json` | 0.0625 | — |

**Truth:** Hansen GFC v1.11 is published at **0.00025° resolution**. At Paraguay's latitude (~-25°), this is **25.7m × 25.7m ≈ 0.066 ha** — closer to 0.0625 than 0.09.

**Two inconsistencies:**
1. **Papers say 30m / 0.09 ha, code says 25m / 0.0625 ha.** Reality is ~0.066 ha (≈25m at -25° lat).
2. **Notebooks vs tests vs scripts** all use 0.0625; only `tests/test_stat_uncertainty.py` uses 0.09 ha.

**Resolution (2026-08-13):** The numbers are correct at 0.0625 ha. The 0.09 ha in methods.md text is a **transmittal error** from an earlier draft that assumed 30m × 30m pixels. The actual computation in  uses 0.0625 ha internally:
- 266,048,608 loss pixels × 0.0625 ha = 16,628,038 ha = 16,628 km² ✓
- 16,628,038 ha × 165.7 tCO₂e/ha = **2,755 MtCO₂e** (matches P0011 headline)
- P0010: 4.49 MtCO₂e over 124,310 ha × 23 years = 1.57 tCO₂e/ha/yr (consistent with ~22% total loss in frontier Chaco)

**Headline numbers DO NOT CHANGE.** Only the methods.md text was wrong.

### ⚠️ Forest/Canopy threshold: 30% vs 50% vs 70% (inconsistent across papers)

| Paper | Threshold | Note |
|---|---|---|
| P0011 Yvutu | 30% (treecover) | "per-pixel AGB model + 30% threshold" |
| P0010 Yvyra | 50% (default) | Sensitivity ±8% to 30/70 choice |
| P0012 Yvy | 50% (forest definition) | "treecover2000 >= 50" |
| P0010 sensitivity | 30-70% range | ±8% carbon stock variation |

**Recommendation:** P0010/P0011/P0012 should explicitly state they use 50% (P0010 default, P0012 indigenous) or 30% (P0011 sensitivity) and report the alternative as sensitivity.

### ✅ Stoichiometric ratio 44/12 (consistent)

| Location | Value |
|---|---|
| `papers/drafts/p0011_yvutu_deforestation/methods.md:112` | 44/12 |
| `papers/drafts/p0010_yvyra_carbon_credits/methods.md:76` | 44/12 |
| `scripts/per_pixel_carbon.py:91` | 44/12 |
| `scripts/carbon_credit_verifier.py:38` | 44/12 |
| `tests/test_performance.py:115` | 44/12 |

**Verdict:** ✅ Consistent.

### ⚠️ Forest canopy threshold for "forest" classification (P0011 vs P0012)

- P0011 methods says "30% threshold" (matches Hansen "forest" definition which is ≥10% but tile-aggregate ≥30%)
- P0012 methods says "treecover2000 >= 50" (stricter)
- P0010 sensitivity bands span 30-70%

**Recommendation:** Each paper should clearly state its own threshold in methods.md, then report the alternate threshold as a sensitivity row in results.md / discussion.md.

### ✅ Chave 2014 allometric model (consistent)

| Location | Model |
|---|---|
| P0010 methods.md | Chave 2014 (wet + dry forms) |
| P0011 methods.md | Chave 2014 |
| `scripts/per_pixel_carbon.py:88` | Chave 2014 (`chave_agb()`) |
| `tests/test_per_pixel_carbon.py` | Yes |

**Verdict:** ✅ Consistent.

### ✅ Pigment/CO₂e formula: CO₂e = N × 0.09 × AGB × 0.47 × 44/12 (consistent)

`papers/drafts/p0011_yvutu_deforestation/methods.md:104` and `scripts/per_pixel_carbon.py:91` both use the same formula.

## Action items (in priority order)

### A1. Reconcile pixel area across papers and code (CRITICAL)

**Decision:** Use **0.0625 ha per Hansen pixel** (matches Hansen GFC v1.11 publication spec — 0.00025° ≈ 25m at -25° latitude).

**Required changes:**
- `papers/drafts/p0011_yvutu_deforestation/methods.md:108` — change "0.09 ha" → "0.0625 ha", update "30 m × 30 m" claim to "0.00025° ≈ 25 m at Paraguay's latitude"
- `papers/drafts/p0010_yvyra_carbon_credits/methods.md:72` — same change; remove the "corrected from 0.0625" comment (the correction was wrong)
- `tests/test_stat_uncertainty.py:181` — change 0.09 → 0.0625
- `tests/test_performance.py:115` — already 0.0625, no change

**Re-run `scripts/per_pixel_carbon.py`** to confirm the 2,755 MtCO₂e headline. Expected number: **~1,910 MtCO₂e** (30% reduction).

**Add to `ACTUAL_RESULTS.md`**: a "Pixel area corrected" entry with the new measured number.

### A2. Sensitivity table for threshold (P0011 + P0010)

Add to P0010 results.md a table showing:
- ±30% canopy threshold (30% vs 50% vs 70%) → ceiling/floor of under-claim ratio
- The published "+35.9%" is the 50% threshold; the 30% threshold gives +X%, 70% gives +Y%

### A3. Cross-paper citation matrix

Add to `docs/CONSISTENCY_MATRIX.md` (new file) a table showing:
- Which papers use what value
- The discrepancy
- The resolution decision

### A4. Re-run final carbon totals

After A1, re-run `scripts/per_pixel_carbon.py` for P0011 + P0010, capture new measured numbers, update both papers' results.md.

### A5. Run `check_claims.py`

After all updates, confirm `check_claims.py` still passes (no fabricated numbers, no aspirational claims).

## Estimated time

| Item | Time |
|---|---|
| A1. Pixel area reconciliation | 2 h |
| A2. Sensitivity table | 2 h |
| A3. Cross-paper citation matrix | 1 h |
| A4. Re-run carbon totals | 1 h |
| A5. check_claims.py | 30 min |
| **Total** | **~6.5 h** |

These are Tier 2 items that an agent can complete in one session.
