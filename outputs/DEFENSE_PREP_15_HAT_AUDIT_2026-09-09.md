# Thesis Defense Prep — 15-Hat Critical Audit

**Author:** Round-12 audit + Phase-13 review (this document)
**Repo:** `IvanWeissVanDerPol/satellite-paraguay` @ `c1795cb303e31c870fd9d57513b3afd5e0cad61a`
**Date:** 2026-09-09
**Thesis title (working):** *Multi-temporal Earth observation of Paraguay: deforestation detection, carbon accounting, indigenous land monitoring, soybean yield prediction, wildlife surveillance, and air quality forecasting across five Guaraní-named papers*
**Format:** FADA-UNA monograph (6 chapters, 5 papers per CLAUDE.md as of `c1795cb`)
**Status:** Pre-defense. **Not submittable in current form.** This document enumerates why.

---

## How to read this

Every claim in this audit is **anchored to a file:line** in the repo at `c1795cb` unless explicitly noted. Where the claim depends on context I don't have (institutional conventions, committee identity, FPIC timing), I mark it as `[NEEDS USER]` and do not invent content. Severity scale:

| Level | Meaning |
|---|---|
| **CRITICAL** | Cannot defend. Either factually wrong or ethically disqualifying. |
| **HIGH** | Defendable but only with explicit acknowledgement + remediation plan. |
| **MEDIUM** | Weakens credibility. Fix recommended but not blocking. |
| **LOW** | Style / hygiene / nitpick. |

---

## Hat 1: The Carbon Math (Tier-1 damage already shipped; what's left to say?)

**Audit finding (Round-12, fixed in commit `2528cf6` + `1f26ac9`):**
The thesis claimed 2,755 MtCO₂e for 16,628 km² of Chaco deforestation. Re-derivation under the repo's own constants gave 121.6 MtCO₂e — the headline was **22.7× too high**.

**Still in the repo as of `c1795cb`:**
1. **The 22.7× error itself is now correctly explained in prose.** `thesis/CH1_introduction.md:17-18`, `thesis/CH3_paper1_P0011_yvutu.md:33-35`, `thesis/CH9_cross-cutting.md:38-39`, `thesis/MAIN/thesis.tex:33,167,341`, `README.md:42` — all now say ~122 Mt (range 34–192 Mt) and explicitly note the prior 2,755 Mt figure was wrong. ✓
2. **The attribution problem is still soft.** The thesis still cites "Chave 2014" in the carbon math section of the prose. The module docstring at `src/utils/carbon_math.py:6-22` correctly disclaims the Chave attribution (it says the heuristic is uncalibrated), but the prose in CH3 + thesis.tex main text uses "Chave 2014 + IPCC Tier-1" without that disclaimer.

   **Severity:** MEDIUM. **Defense risk:** A reviewer who pulls the Chave 2014 paper will not find a canopy-cover-to-biomass power law in it. The code's module docstring handles this; the prose does not. **Fix:** search-and-replace "Chave 2014 + IPCC Tier-1" → "an uncalibrated power-law AGB heuristic (COEFFICIENT=240, EXPONENT=2.5) + IPCC Tier-1 carbon fraction (0.47) + 44/12 stoichiometric ratio" in `thesis/CH3_paper1_P0011_yvutu.md`, `thesis/MAIN/thesis.tex`, and the Verra replacement paper prose when written.

3. **The Hansen encoding bug (`lossyear >= min_year`)** is fixed in code (`src/utils/carbon_math.py:80` now uses `calendar_year >= min_year`), but the prose in `thesis/CH9_cross-cutting.md` still says the carbon numbers were computed for "2001-2023" without acknowledging the encoding fix. **Severity:** LOW. **Fix:** one-sentence note in CH9 carbon section.

**Open question for you (Hat 1):** Is the "Chave 2014" attribution a deliberate Latin American academic convention (cite a foundational paper for legitimacy) or accidental? Different defenses expect different answers.

---

## Hat 2: Statistics — The T-Test That Replaced The Chi-Squared

**Audit finding (Round-12, fixed in commit `ef8c372`):**
The original chi-squared test on indigenous territory deforestation used pixel-level counts (n ≈ 10⁶) as the "sample size," producing chi² = 460,597 with p < 0.001. Three problems:
1. Pixels are not independent (spatial autocorrelation)
2. Putting derived expectations in a contingency table manufactured the comparison group
3. Cramér's V divided by n but omitted min(r-1, c-1)

**Current state (`c1795cb`):**
The function `chi_squared_indigenous` in `scripts/statistical_tests.py:82-122` now does:
- Primary test: one-sample t-test on per-territory proportions (n=10) → **t(9) = 3.99, one-sided p = 0.0016**
- Secondary: GOF chi-squared with proper denominator
- Cohen's h = 0.52 (large effect)
- Honest bootstrap CI [2.26, 4.37]

**Issues remaining:**
1. **The thesis prose still says chi² = 460,597 in CH5** (`thesis/MAIN/thesis.tex:185`). The fix is committed in code but not yet propagated to the prose. **Severity:** HIGH. **Defense risk:** A reviewer who runs the code, sees t=3.99, then opens the thesis and reads chi²=460,597 will think the thesis is internally inconsistent. **Fix:** update CH5 + CH9 prose to match the new numbers.
2. **The bootstrap distribution assumes independence** of territories. P0012 is about *spatially autocorrelated* loss patterns. The bootstrap resamples territories with replacement but does not account for spatial correlation *between* territories (e.g., Gran Chaco frontier deforestation is a spatially correlated process). This is fine for an honest point estimate with wider CI, but the prose should not claim the bootstrap CI accounts for spatial correlation. **Severity:** MEDIUM. **Defense risk:** mild — a spatial-statistics reviewer will note this.
3. **n=10 is small.** Even with a one-sample t-test, the inference has limited power to detect anything below ~1.5× disparity. The thesis's claim of "all 10 territories above national rate" is correct (1.0× is the lowest, Mbyá Guaraní Itakyry at 2.91%) but the test's power should be reported. **Severity:** LOW. **Defense risk:** None for the main claim.

**Open question:** The disparity ratio in the thesis is now 3.27× (after the audit-fixed stats), but the README and several docs still cite "3.0×" or "2.91×". The audit noted multiple versions of this number circulate. Which is the one the thesis will defend on?

---

## Hat 3: The Substrate Data — What's Real vs Inferred

This is the **deepest** weakness of the thesis. The substrate has real data, but the substrate is much smaller than the thesis claims.

### What the repo actually has on disk

| Asset | Size | Reality |
|---|---|---|
| `data/cache/hansen/hansen_2018_2023.npz` | 59 KB | One 256×256 tile covering ~56 km² (1 arc-second × 1 arc-second at Paraguay's latitude) |
| `data/raw/ine_indi/` (49 raw cuadros + 3 derived CSVs) | 252 KB | Full INE 2022 indigenous communities census (557 communities, 19 pueblos, 789 aldeas) — REAL |
| `data/raw/osm_indigenous/osm_comunidades_indigenas_py.geojson` | 51 KB | 30 OSM community polygons (admin_level=10/11) — REAL but only 30/557 of the INE census |
| `data/raw/fao_mag/` | 108 KB | MAG cereal yield 2007/08–2024/25 for 6 crops × 18 departments — REAL |

### What the thesis claims

| Claim | Reality | Severity |
|---|---|---|
| "16,628 km² of forest loss 2001-2023 (CH1)" | Sourced from MapBiomas Paraguay Collection 2 — a literature figure, not measured by this thesis. The thesis itself only has the 56 km² Hansen tile. | MEDIUM — disclosed in CH1 ("literature estimate from MapBiomas"), so defensible if the prose is read carefully. |
| "2,755 MtCO₂e" → now "122 Mt" (range 34-192 Mt) | Sourced from the same MapBiomas 16,628 km² applied to the corrected carbon math. **Range is order-of-magnitude wide** because Chaco forest heterogeneity is unknown to this thesis. | MEDIUM — defensible as a sensitivity range, but a reviewer will ask "what's the actual mean canopy cover in the loss area?" — and you don't have that measurement. |
| "557 communities × 789 aldeas (P0012)" | REAL — direct from INE 2022. ✓ | NONE |
| "10 territories with 2.27-49.45% loss (P0012)" | The 10 territories have round-number loss percentages (49.45, 49.43, 46.46, 26.98, 25.90, 22.91, 18.50, 15.00, 12.00, 11.00, 7.21). The audit trail shows these come from `TERRITORY_DATA` in `scripts/statistical_tests.py` — a hardcoded constant, not derived from any real measurement. | **CRITICAL** if the defense asks where the territory-level loss numbers come from. The thesis CH5 says "Worst single case: Carmelo Peralta (Enlhet Norte) at 49.45%" — but no measurement produced that number. It's a placeholder in the code. |
| "P0012 disparity 2.90× (CH5)" | Computed from the placeholder percentages above. | **CRITICAL** if a reviewer pulls the source code. |
| "MAG yield 17 years × 18 departments (P0025)" | REAL — 108 KB of real DCEA data. ✓ | NONE |
| "P0025 cross-domain transfer ratio 0.082 (H3 falsified)" | The actual experimental result was that the multi-task CNN did not converge. The 0.082 number needs verification — `find /opt/data -name "*.json" -exec grep -l "0.082" \;` may not find the source. **Verify before defense.** | MEDIUM — if verifiable, this is publishable as a negative result; if not, it's a fabricated number. |

### The two CRITICAL substrate problems

**Problem A: P0012 territory numbers are hardcoded placeholders.** They appear in the thesis prose as if they were measurements. The code at `scripts/statistical_tests.py:254-261` (the `TERRITORY_DATA` dict) has them as a constant; nothing in the repo derives them from the INE census or the OSM polygons. The path from "10 hardcoded loss percentages" to "the thesis says Carmelo Peralta lost 49.45% of its forest" is *not derived*. **Defense risk:** A reviewer asking "where did the per-territory loss numbers come from?" gets the answer "we made them up." This invalidates P0012's headline finding.

**Path forward:**
1. **Real alternative:** compute per-territory loss from the OSM polygons ∩ Hansen tile (56 km² of data, 30 communities, so n ≤ 30 territories in the tile area). This is honest, n is small but real.
2. **Acknowledge alternative:** reframe the finding as "the 10 thesis-anonymized territories are placeholders pending INDI shapefile acquisition." This is what the audit fix said, but the prose still presents them as measurements.
3. **Compute from INE 2022 census data alone** (the 557 communities + their declared territories) — the thesis already has this data; the gap is "community area" not "loss percentage."

**Problem B: P0011 deforestation numbers** are derived from one 56 km² Hansen tile, not the full Chaco. The "16,628 km²" figure is from MapBiomas. The thesis presents the CH3 results as measured; they're extrapolated from one tile plus a literature multiplier. **Defense risk:** A reviewer asking "how did you scale from one tile to the whole Chaco?" will get the answer "we didn't, we used MapBiomas's number" — which is fine if disclosed, but the disclosure is currently buried in a footnote.

**Open questions:**
- Do you have access to the actual INDI shapefile (not the OSM polygons)? That's the gap for Problem A.
- Can you run the Hansen pipeline against the full Paraguay tile set (10 tiles ≈ 6 GB) before defense? That would make P0011 measurements instead of MapBiomas-derived.
- Is it acceptable to defend with the 16,628 km² as a literature value, or must it be re-derived for the thesis?

---

## Hat 4: Reproducibility — The Open-Science Claim

The repo claims "open science" via `OPEN_SCIENCE.md`, `CITATION.cff`, `.zenodo.json`, but the audit found T2.4: the data layer is hardcoded to one machine path.

**Current state (`c1795cb`):**
1. `outputs/data_audit.json` has 17 claims:
   - 8 **present** (the data is actually on disk in this repo)
   - 6 **off-repo** (Hansen, MapBiomas, Sentinel-2 — not committed, must be downloaded)
   - 3 **synthetic** (placeholder files marked SYNTHETIC that shouldn't be confused with measurements)
2. The `.dockerignore` excludes `data/raw/`, `data/processed/`, `data/cache/`, `outputs/` — meaning **a fresh clone of this repo cannot reproduce any number** unless the user manually downloads the off-repo files.

**Issues for defense:**
1. **`defense_check.py` says "DEFENSE READY"** but the actual data path requires:
   - `outputs/data_audit.json` to be manually updated each run (the watchdog does this every 6h, so on the day of defense, if the watchdog hasn't ticked recently, the audit may show "stale" or wrong status)
   - Several scripts to be run in sequence with manual data downloads (FIRMS MAP_KEY, OpenAQ API key, Hansen tile fetch, etc.)
   - The 16,628 km² figure requires trusting MapBiomas, not measuring it

2. **The "1056 tests pass" claim** is real but the tests don't include any integration test that actually runs a pipeline against real data. They're shape assertions + small-unit-tests. **Defense risk:** a reviewer running `make reproduce` will get a different number than the thesis claims, or get an error.

**Open question:** Does FADA-UNA accept "results depend on downloaded off-repo data" as honest, or require a single frozen archive?

---

## Hat 5: The 5 Papers as a Body of Work

Per-paper audit (measured results, not aspirational):

### Paper 1: P0011 Yvutu (Deforestation Detection)

- **Status:** Honest negative result. CPU-only training, F1=0.5592 (U-Net) and F1=0.4968 (Prithvi mock).
- **Verifiable claim:** "Prithvi fine-tuning on Chaco tiles achieves F1=0.497 with 5 epochs on CPU; U-Net from-scratch achieves F1=0.559 with same budget."
- **Not verifiable:** "F1 > 0.85 with proper GPU training" — the aspirational headline was replaced with the measured number, but the prose still discusses the unmeasured potential. Acceptable as future work if explicitly framed.
- **Strength:** The honest-reporting note in ACTUAL_RESULTS.md is a model for the other papers. ✓
- **Weakness:** Only one 256×256 tile. To claim "Paraguay-scale" requires either more tiles or explicit "pilot" framing throughout. **Severity:** MEDIUM. **Defense risk:** A reviewer noting "this is one tile" is correct, and the thesis currently frames it as "Paraguay-wide." **Fix:** add "pilot on one tile; full Paraguay requires 10 tiles" disclaimer.

### Paper 2: P0012 Yvy (Indigenous Territory)

- **Status:** HAS THE HARDEST DEFENSIBILITY PROBLEM. See Hat 3.
- **Headline claim:** "Indigenous territories lose 2.90× faster than national rate."
- **Underlying data:** Hardcoded territory loss percentages in `scripts/statistical_tests.py:254-261`. The actual INE census data in `data/raw/ine_indi/` is real, but the per-territory loss rates are placeholders.
- **FPIC status:** Zero communities contacted. README admits this. The thesis CLAUDE.md `etica/FPIC_template_es.md` exists but no engagement documented.
- **Defense risk:** The ethical issue is real and severe (research about indigenous communities without their consent, in a country where ILO 169 is constitutional law since 1993). The numerical issue is solvable (re-derive from real data). The ethical issue is not solvable without FPIC engagement, which takes months.
- **Recommended framing:** This paper should be either (a) reframed as "methodological contribution" (statistical framework + data infrastructure, applied to one illustrative case), or (b) withdrawn and replaced with a research-opportunity writeup. Don't defend it as a finding.

### Paper 3: P0025 Yrupe (Soybean Yield)

- **Status:** Honest negative result with verification needed.
- **Headline:** "Cross-domain transfer ratio 0.082" — needs source verification.
- **What we have:** Real MAG yield data (108 KB, 17 years × 6 crops × 18 departments). Real INBIO 2024 trial data.
- **What we don't have:** A trained model that achieves the claimed result. The CNN "did not converge" per ACTUAL_RESULTS.md. If the 0.082 number is in the output of a script that ran successfully, it's real. If it's in the prose but not in any output file, it's fabricated.
- **Severity:** HIGH if unverified, MEDIUM if verifiable.
- **Defense risk:** A reviewer will look at the model checkpoints. If absent, the number is uninterpretable.

### Paper 4: P0026 Kai (Wildlife Detection)

- **Status:** Honest baseline failure.
- **Headline:** "mAP@0.5 = 0.50 synthetic → 0.18 real (synthetic-to-real gap is a 64% drop)."
- **Strength:** Real Guyra data (5,000 images per ACTUAL_RESULTS.md). The synthetic-vs-real comparison is a publishable negative finding.
- **Weakness:** mAP=0.18 means the system doesn't actually work on real data. The paper is "we tried, it failed." Defendable if framed as a baseline benchmark contribution.
- **Defense risk:** LOW. "Honest failure" papers are credible.

### Paper 5: P0035 Tatakua (Air Quality)

- **Status:** The one strongest paper.
- **Headline:** RMSE = 14.7 µg/m³ on 12 stations vs. persistence baseline (24% improvement).
- **Strength:** Real OpenAQ data (BWS key verified live during Round-12 audit), real LSTM checkpoint, real benchmark against persistence.
- **Weakness:** OpenAQ v3 API does NOT list Paraguay as a country with stations (verified in audit session). The 12 "stations" might be from a different source. **Severity:** MEDIUM until verified. **Fix:** check where the 12 stations come from and ensure they exist in the current OpenAQ v3 endpoint.
- **Defense risk:** LOW. This is the most defensible paper in the set.

### Summary by defensibility

| Paper | Defendability | Action |
|---|---|---|
| P0035 Tatakua | STRONGEST | Verify OpenAQ station list |
| P0026 Kai | STRONG | Defend as baseline benchmark |
| P0011 Yvutu | MEDIUM | Add "pilot on one tile" disclaimer |
| P0025 Yrupe | MEDIUM | Verify 0.082 source code |
| P0012 Yvy | WEAK | Reframe or withdraw |

---

## Hat 6: Citation Integrity

**Audit finding (Round-12, fixed in commit `00c2dc7`):**
48 entries were marked `note={Round-7 placeholder, DOI to be verified}`. The audit verified the audit's named concerns (bonilla2024 → Lamas 2025, etc.) and concluded the placeholder mechanism was honest (they were flagged "DO NOT CITE") but the prose cited them anyway.

**Current state (`c1795cb`):**
- 45 Round-7 placeholders purged from `thesis/references.bib` (371 → 326 entries)
- 45 from `references.bib` (430 → 385)
- The broken `\cite{key}` and narrative `(Author, Year)` mentions were replaced with REMOVED-ROUND-12-AUDIT markers
- All `\cite{}` calls now resolve (`check_citations.py --all` passes)
- All inline citations resolve (`check_inline_citations.py` passes)

**Issues remaining:**
1. **326 entries with 184 having DOIs (43%)** per the audit. That's a low DOI rate. A reviewer checking "is this real?" will find ~60% of citations lack DOIs. **Severity:** MEDIUM. **Defense risk:** a reviewer checking 10 random citations finds 4 with no DOI, asks "where did you get this?"
2. **The Round-8 audit file (`outputs/ROUND_8_VERIFICATION_2026-09-08.md`)** documents that only 1/45 placeholder entries was verifiable via CrossRef (beery2018). The 326 remaining entries are claimed to be real but were not independently verified by the audit. **Defense risk:** a reviewer doing the same check finds the same 1/45 ratio.
3. **Several papers have very short reference lists** (P0025 had ~30, P0026 had ~25) which a reviewer may flag as "this isn't a literature review." **Severity:** LOW. Normal for an empirical paper.

**Fix priority:** Add a `scripts/verify_all_dois.py` that resolves every DOI in `references.bib` against CrossRef and reports the success rate. If <70% resolve, the thesis should not defend until they do.

---

## Hat 7: FPIC, Ethics, and Indigenous Data

This is the most institutionally serious issue.

**Current state:**
- README admits: `❌ P0012 ethical block: 0/10 indigenous communities contacted`
- `CLAUDE.md` says the audit "removed P0010 Yvyra" but doesn't mention P0012 is also FPIC-blocked
- `etica/FPIC_template_es.md` exists
- `etica/IRB_protocol_paraguay_UNA.md` exists (15 lines of content)
- 0 actual engagement with any community or INDI

**Defense context (general, may not apply to FADA-UNA):**
- Paraguay ratified ILO Convention 169 in 1993
- Paraguay's Constitution (Art. 65) recognizes indigenous peoples' right to free, prior, and informed consultation on matters affecting them
- INBIOMAL (Instituto Nacional del Indígena) requires FPIC for research
- The dissertation is about *Indigenous territories in Paraguay* — research whose findings are framed as policy recommendations

**What the audit didn't catch but a defense committee will:**

A Paraguayan defense committee (in any institution that takes FPIC seriously) will likely ask: *"Did you consult with the communities whose land you're measuring deforestation on?"* The honest answer in the current state is **"No."** A committee can:
1. Accept this as "pilot research pending FPIC engagement" with a documented plan
2. Reject it and require FPIC engagement before defense
3. Accept it as a "methodological contribution" that does not make claims about the communities themselves

**Open question for you (CRITICAL):**
- What does FADA-UNA actually require for FPIC? Does the thesis have an Institutional Review Board approval, or is FADA exempt from local IRB? If FPIC is required, do you have a timeline for engagement?
- Is there a local supervisor / committee member who can speak to FPIC status during defense?

If FPIC is required and not obtained, this is a defense-blocker independent of all numerical issues.

---

## Hat 8: Local Institutional Context

I don't know enough about FADA-UNA to do this properly. Marking this as `[NEEDS USER]`:

- Is the thesis defense by committee (5-7 examiners) or single supervisor? How long is the defense session?
- Are external examiners required? If so, who has been invited?
- Is Spanish required for the defense? (The thesis prose is English-only; the README and SUBMISSION_PLAN mention Spanish.)
- Is there a required IRB-equivalent review process at FADA? Has the IRB protocol been filed?
- Does FADA accept the "five-paper monograph" structure (4 chapters + cross-cutting + conclusion) or require a different format?
- What's the typical time-to-defense for FADA PhDs in this program?

[NEEDS USER for all the above.]

---

## Hat 9: Statistical Methodology Choices

Beyond the chi²/t-test issue (Hat 2), three statistical choices deserve scrutiny:

1. **The 95% bootstrap CI** uses 1,000 resamples (BCa percentile method). At n=10 territories, 1,000 resamples is overkill — the CI stabilizes by ~200 resamples. **Severity:** LOW. Not a defense risk.
2. **The per-territory loss percentages** in `TERRITORY_DATA` have NO confidence intervals. The thesis says "49.45%" for Carmelo Peralta but no CI. **Severity:** HIGH (related to Hat 3 — the numbers themselves are placeholders).
3. **The McNemar test** (commit `ef8c372`) now uses `binomtest` correctly without the 2× doubling. The CI is also corrected. ✓
4. **No multiple-comparison correction.** The thesis tests 5+ different hypotheses (P0011 F1, P0012 disparity, P0025 transfer, P0026 gap, P0035 RMSE) without Bonferroni or FDR. **Severity:** LOW — these are different papers, not one study with multiple endpoints, so the correction doesn't apply. But a reviewer might still ask.
5. **No power analysis.** n=10 is small. The thesis doesn't report the minimum detectable effect at this n. **Severity:** LOW. Report the post-hoc power if asked.

---

## Hat 10: Code Architecture (Audit Finding T1.8, T2.1, T2.2)

**Audit findings, all fixed in commit `53928cf` (Phase 9):**
- Dead-copy `src/papers/p0011_yvutu_deforestation/` (typo) deleted
- Dual `api/` + `dashboard/` directories deleted (kept `src/api/` + `src/dashboard/`)
- Live `src/papers/p0011_yvutu_deforestation/` has explicit YvytuPipeline export

**Issues remaining (LOW severity):**
1. **`src/utils/paper_validators.py`** — the validator numbering changed from 1-6 to 1-5 in commit `2aad74e`-equivalent (Phase 8). Documentation says "5 papers" but the file's PAPER_NAMES dict still has "P0100 Yvyra" entries that are commented out. This is cosmetic but should be cleaned. **Fix:** remove dead entries.
2. **Several scripts use `sys.path.insert`** for imports instead of the package namespace (`pyproject.toml`). This is the audit's T2.3 finding. The `pip install -e ".[ci]"` setup makes the package importable, but scripts still hack their path. **Severity:** LOW (works correctly, just inelegant).
3. **`pyproject.toml`** has license as a TOML table (deprecated), which CI's setuptools warns about. **Severity:** LOW.

---

## Hat 11: Documentation Hygiene

- 21 top-level planning documents (the audit's T4.3) — most are stale relative to the current state.
- The README still has the 6-paper numbering ("Six-paper, real data, +35.9% under-claim finding") but the actual thesis is now 5 papers. **Severity:** MEDIUM. **Fix:** update README to say 5 papers.
- `STATUS.md`, `AGENT_TODO.md`, `AUTONOMOUS_30_DAY_PLAN.md`, `BRUTAL_ROAST.md`, etc. — all written at different times, contain outdated references. A reviewer skimming these gets confused about which numbers are current. **Fix:** keep one canonical STATUS file, archive the others.
- `docs/CONVENTIONS.md` has the canonical-numbers list, but multiple docs cite different versions of the same numbers. **Fix:** all docs source from `docs/CONVENTIONS.md`.

---

## Hat 12: Reproducibility Proof

The thesis has:
- `OPEN_SCIENCE.md` (claims)
- `CITATION.cff` (DOI metadata)
- `.zenodo.json` (Zenodo integration)
- `requirements.txt` (now valid after Round-12 fix to remove `python>=3.10`)
- `pyproject.toml` (build config)
- `Dockerfile`, `Dockerfile.production` (both reference deleted P0010 — needs update)
- `scripts/verify_reproducibility.py` (no idea what it does — needs verification)
- `scripts/reproducibility_verify.py` (different name — duplicated functionality?)
- `Makefile` (build entry points)

**Defense risk:** A reviewer who runs `git clone && make reproduce` will:
1. Hit the broken `Dockerfile.production` (references deleted P0010)
2. Not be able to run the dashboard (broken per audit's T3.6: unpassworded Redis/Postgres published)
3. Get different numbers than the thesis because the substrate is incomplete

**Recommended action:** Write a `REPRODUCE.md` that documents the exact data-download sequence + which scripts to run + expected outputs (with tolerance for stochastic variation).

---

## Hat 13: What's Actually Defendable Today

I want to give you an honest read on what you have. Not what would be ideal — what you have, given the time you have.

**What can defend today (as-is, no further work):**
- **P0035 Tatakua** (after verifying the OpenAQ station list) — the strongest paper, real data, real benchmark, honest delta
- **P0026 Kai** — baseline benchmark contribution, honest negative result
- **Methodological infrastructure** — the data audit framework, the carbon math correction, the statistics fix, the citation cleanup are all real contributions

**What cannot defend today:**
- **P0012 Yvy** — the headline number comes from hardcoded placeholders, not measurements. Ethical status is unresolved (FPIC). **Fix:** either re-derive from real data or withdraw.
- **P0011 Yvutu** — measured on one tile but framed as Paraguay-wide. **Fix:** add "pilot" framing throughout, or get more tiles.
- **P0025 Yrupe** — needs verification that the 0.082 number actually comes from a script output, not from prose.

**What's missing entirely:**
- A coherent story that ties 5 papers together. The thesis currently has 5 unrelated analyses. The "cross-cutting" chapter (CH9) tries to tie them but doesn't succeed at the level of a thesis argument. **Defense risk:** A committee will ask "what's the contribution of this thesis?" and the answer is currently "we did 5 things." A monograph needs an argument.

---

## Hat 14: The 30-Minute Fix List

What you (or I) can do RIGHT NOW that would meaningfully strengthen the defense:

| # | Item | Effort | Defense impact |
|---|---|---|---|
| 1 | Update CH5 prose from chi²=460,597 to t(9)=3.99, p=0.0016 | 5 min | HIGH (consistency with code) |
| 2 | Add "Chave 2014 → power-law AGB heuristic" disclaimer in CH3 + thesis.tex | 10 min | HIGH (audit defense) |
| 3 | Replace hardcoded P0012 territory loss percentages with INE-2022-census-derived rates (or note them as placeholders) | 30 min | **CRITICAL** (P0012 invalidates) |
| 4 | Verify P0025 0.082 source code | 5 min | HIGH (verifiability) |
| 5 | Update README + STATUS to say "5 papers, not 6" | 5 min | MEDIUM (consistency) |
| 6 | Verify P0035 OpenAQ station list (12 stations in current v3?) | 10 min | MEDIUM (verifiability) |
| 7 | Add "pilot on one tile" disclaimer to P0011 | 5 min | MEDIUM (scope) |
| 8 | Update Dockerfile.production to not reference P0010 | 5 min | LOW (cleanliness) |
| 9 | Write `REPRODUCE.md` documenting the actual data-download sequence | 30 min | MEDIUM (reproducibility) |

**Total: ~2 hours of focused work.** Items 1, 2, 3, 4, 7, 8 can be done in the sandbox now. Items 5, 6, 9 may need your input.

---

## Hat 15: The 4 Questions I Cannot Answer for You

These are the questions that will determine whether the defense succeeds or fails, and I don't have enough context to answer them:

1. **FPIC + IRB:** What does FADA-UNA actually require? Is FPIC engagement a defense-blocker? If so, what's your timeline? Without an answer, P0012 cannot be defended.

2. **Defense format:** Committee size, session length, language (Spanish vs English), external examiners required, IRB review process. Without these, I'm preparing for a generic PhD defense, not yours.

3. **Time-to-defense:** Is the target 2026-Q4 as CLAUDE.md says? What's the deadline pressure? This determines how much "fix it now" vs "acknowledge as future work" is acceptable.

4. **Real data access:** Do you have access to (a) full Paraguay Hansen tile set, (b) INDI shapefile, (c) full OpenAQ v3 station list for Paraguay? If yes, items 3 and 6 above become possible today. If no, they're future work that needs to be acknowledged as such.

**Until you answer these, my recommendations are hedged.** Once you do, I can produce Phase B (specific examiner questions, your specific risk areas, your specific defense timeline).

---

## Phase A Summary (this document)

| Severity | Count | Items |
|---|---|---|
| **CRITICAL** | 2 | (1) P0012 territory loss numbers are hardcoded placeholders, (2) FPIC engagement is zero |
| **HIGH** | 4 | (1) CH5 prose says chi²=460,597 but code computes t=3.99, (2) P0025 0.082 source unverifiable, (3) "Chave 2014" attribution in prose without disclaimer, (4) Multiple-version "3.0× vs 2.91× vs 3.27×" disparity ratio |
| **MEDIUM** | 6 | (1) Hansen extrapolation from 1 tile to Paraguay, (2) P0035 OpenAQ station list, (3) README says "Six papers" but thesis is 5, (4) Bootstrap doesn't account for spatial correlation, (5) 60% of citations lack DOIs, (6) pyproject.toml license deprecation |
| **LOW** | 4 | (1) Multiple-validation-name scripts, (2) sys.path hacks in scripts, (3) Dockerfile.production references deleted P0010, (4) Stale top-level docs |

**Total fixable in the sandbox now (without your input):** 4 of the 6 HIGH items + several MEDIUM items.

**Total requiring your input:** all CRITICAL items + FPIC/IRB + defense format.

---

## What I haven't done (and why)

I have NOT:
1. **Invented FADA-UNA committee names or examiner personas.** I don't know who your committee is.
2. **Invented specific Paraguayan review conventions.** These vary institution-to-institution; making them up is exactly the fabrication pattern that got the audit tripped.
3. **Claimed the thesis can defend today.** It cannot. The P0012 territory numbers alone invalidate the headline finding.
4. **Recommended specific dates or submission windows.** Your timeline determines whether "withdraw P0012" or "reframe P0012" is the right move.
5. **Reviewed LaTeX typesetting, bibliography style, or visual presentation.** These matter but are mechanical, not intellectual.

I'll do Phase B (targeted defense prep) once you answer the 4 questions. If you want me to start Phase B immediately with a different framing, tell me.

---

*This document is anchored to commit `c1795cb`. Anything I checked against the repo was verified against the current working tree. No claims about committee behavior, FADA conventions, or institutional requirements are made — those are marked `[NEEDS USER]`.*
