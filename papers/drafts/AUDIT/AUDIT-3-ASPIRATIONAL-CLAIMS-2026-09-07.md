# Audit #3 — Aspirational Claims vs. Measured Values

**Date:** 2026-09-07
**Auditor:** Hermes (subagent delegated audit task)
**Source of truth:** `papers/drafts/p<NNNN>_<slug>/ACTUAL_RESULTS.md` (per paper)
**Scope:** 6 papers (paper.md + paper.tex) and thesis chapters (CH1–CH11 + MAIN/thesis.tex)

---

## 0. Executive Summary

Following the 2026-08-10 + 2026-08-11 honest-reporting passes (Round-1), each paper's
**abstract.md and the relevant parts of paper.md / introduction.md / conclusion.md have
been swapped to measured values**, with explicit "Honest Reporting Notes" appended.
Round-2 verification by this audit finds that the **substitution is approximately
80–90% complete in paper.md / abstract.md / introduction.md / conclusion.md**, but the
following significant drift remains:

### Class A — CRITICAL: Markdown vs LaTeX drift within the same paper
The **paper.tex** submission templates for **P0011 (Yvutu)** still contain the OLD
aspirational numbers (F1 = 0.876, mIoU = 0.794, "operational deployment"), while the
same paper's paper.md/abstract.md have been corrected. If a reviewer compiles LaTeX
without re-reading the .md, they will see aspirational claims.

### Class B — CRITICAL: thesis/MAIN/thesis.tex uses wrong measured values
The unified thesis main.tex (lines 286–294, 339) reports a **completely wrong Tatakua
result** — RMSE = 4.8 µg/m³ vs. the measured ACTUAL_RESULTS.md value of 14.7 µg/m³ —
and lists an LSTM-2layer at 6.1 µg/m³ vs. ACTUAL_RESULTS.md (which reports a single
3-layer × 64-hidden LSTM at 14.7 µg/m³). This is an internal-consistency failure
between the thesis main.tex and its own source-of-truth file.

### Class C — MEDIUM: Stale numerical claims in thesis chapters
- `thesis/CH1_introduction.md:19` claims "average deforestation rate of **28.4%**"
  and "**3.3 times** the national average". ACTUAL_RESULTS.md gives 24.67% mean
  and 2.90× ratio.
- `thesis/CH10_discussion.md:13` uses "**3.3 times**". Same stale figure.
- `thesis/CH9_cross-cutting.md:42,43` still says Verra projects "under-claim carbon
  loss by **30-50%**" — ACTUAL_RESULTS.md gives 35.9% mean, range 33.3–50.0%.

### Class D — LOW: Partnership / deployment claims without partnership letter on file
For every paper that mentions partnership/deployment:
- The partnerships folder (`docs/partnerships/`) contains **templates, decision memos,
  and one-pagers — but no signed partnership letter on file**. The synthetic-to-real
  gap and operational claims in P0026 (Kai) and P0012 (Yvy) are explicitly noted as
  having no partnership letter.
- P0010 Yvyra Acknowledgments in paper.md (line 19: "Iván Weiss Van der Pol
  (FP-UNA)") is a single-author claim; conclusion.md states "No partnership with Verra
  / Article 6 / EU CRCF / NGOs. This is an independent analysis. Operational
  deployment requires partnership engagement." — internally consistent and honest.

---

## 1. Per-Paper Audit

### 1.1 P0010 Yvyra — Carbon-Credit Verification

**File:** `papers/drafts/p0010_yvyra_carbon_credits/`

#### Headline measured values (ACTUAL_RESULTS.md)
- Verra mean under-claim: **+35.9%** (range 33.3%–50.0%)
- Total over-crediting: **+1.19 MtCO₂e** (Verra 3.30 vs Hansen 4.49)
- Bootstrap 95% CI excludes 0%
- AGB mean 73.79 Mg/ha, SD 38.4 Mg/ha
- Direction (all 5 under-claim) is robust; magnitude ±8% sensitivity

#### Aspirational claims found

| # | Location | Claim | Status |
|---|----------|-------|--------|
| A1 | `paper.md:42–43` | "Hansen-derived biomass R²=0.82 figure and the 50-project / 15% agreement headline quoted in earlier drafts" — paper.md itself flags this as replaced | ✓ Acknowledged |
| A2 | `paper.tex:23` title | "Verra claims underestimate forest loss by 35% (range 27-41%)" — **paper.md range is 33.3%–50.0%, NOT 27–41%**. LaTeX title is **stale**. | ⚠ MEDIUM |
| A3 | `paper.tex:44` | "an average of 35% (range 27--41%)" — same stale range | ⚠ MEDIUM |
| A4 | `paper.tex:46` | "over-crediting of approximately 1.14 Mt of CO₂e" — ACTUAL_RESULTS says **+1.19 MtCO₂e** | ⚠ MEDIUM |
| A5 | `paper.tex:57` | "replicated the analysis on a stratified sample of 30 Verra projects across the Amazon, Congo, and Southeast Asia, finding similar patterns (mean under-claim 28%)" — **ACTUAL_RESULTS.md line 63-67 explicitly says this replication has NOT been run**: "External replication... re-running on a held-out sample of 30 non-Paraguayan projects is needed to support the '28% mean under-claim globally' claim. We have data downloaded but have not completed the analysis." | **🚨 CRITICAL — paper.tex claims the replication was done, ACTUAL_RESULTS says it was not** |
| A6 | `paper.tex:70-72` | "a cross-region replication across Amazon / Congo / SE-Asia projects has not yet been executed" — this directly contradicts A5 two paragraphs above in the same paper.tex | 🚨 CRITICAL — internal contradiction within paper.tex |
| A7 | `paper.md:127–129` | "No partnership with Verra / Article 6 / EU CRCF / NGOs. This is an independent analysis." — consistent with partnerships/ folder | ✓ Honest |
| A8 | `paper.md:42` | "we have no partnership with Verra" | ✓ Honest |

#### Verdict
- **paper.md and abstract.md are honest** (the stale targets are explicitly flagged as removed).
- **paper.tex has TWO critical issues**: (i) the title and main text use the old 27–41% range; (ii) the paper.tex claims a 30-project replication was completed when it wasn't.
- **FIX**: re-write paper.tex title to "Verra claims underestimate forest loss by 35.9% (range 33.3–50.0%)"; remove the "30 Verra projects... finding similar patterns (mean under-claim 28%)" claim that contradicts the same paper's own footnote two paragraphs later.

---

### 1.2 P0011 Yvutu — Multi-Temporal Deforestation Detection

**File:** `papers/drafts/p0011_yvutu_deforestation/`

#### Headline measured values (ACTUAL_RESULTS.md)
- U-Net from scratch: **F1 = 0.5592** (precision 0.0992, recall 0.9873 — over-predicts)
- Prithvi (mock fallback): **F1 = 0.4968** (didn't converge in 5 CPU epochs)
- Real-data country-scale analysis: **16,628 km² loss 2001–2023**, **2,755 MtCO₂e**
- All 10 of 10 indigenous territories above national rate; 2.90× disparity

#### Aspirational claims found

| # | Location | Claim | Status |
|---|----------|-------|--------|
| A9 | `paper.md:5` (Abstract), `introduction.md:36–39`, `conclusion.md:28` | "Prithvi F1 > 0.85" is **explicitly removed** in the abstract/intro/conclusion and replaced with honest measured values. The Honest Reporting Note (added 2026-08-10) is present. | ✓ Honest |
| A10 | `paper.tex:36` (Abstract) | "**Yvutu achieves a macro-averaged F1 score of 0.876 and a mean Intersection-over-Union (mIoU) of 0.794, outperforming three baselines (persistence, per-pixel Random Forest, U-Net from scratch) by 12.4–22.7 percentage points F1.**" | **🚨 CRITICAL — paper.tex Abstract still claims F1=0.876 and mIoU=0.794, which are completely inconsistent with the paper's own abstract.md (F1=0.559 measured).** |
| A11 | `paper.tex:99` | "**Operational deployment.** We release Yvutu as open-source code with documented API, command-line interface, and Streamlit dashboard." | ⚠ MEDIUM — paper.md qualifies this clearly with "operational deployment requires one week of human time + ~$5 of GPU spend"; paper.tex doesn't qualify. |
| A12 | `paper.tex:117`, `paper.tex:255–259` | "The Argentine / Paraguayan Chaco has no operational near-real-time deforestation alert system. Yvutu's operational deployment would fill this gap, subject to the partnership work" — hypothetically framed; acceptable | ✓ Acceptable |
| A13 | `paper.tex:165` | "Prithvi-300M foundation model on Paraguay-specific data... Yvutu achieves state-of-the-art deforestation detection on the Paraguayan Chaco (F1=0.876, mIoU=0.794)" | **🚨 CRITICAL — repeats the aspirational 0.876/0.794 in the Conclusion section** |
| A14 | `paper.tex:362–365` (Table 1) | Hard-coded results table: **Yvutu (Prithvi) F1=0.876, mIoU=0.794, Precision=0.901, Recall=0.852**. The actual measured values from ACTUAL_RESULTS.md are F1=0.559, mIoU=0.491, Precision=0.099, Recall=0.987. | **🚨 CRITICAL — the entire results table in paper.tex uses aspirational values** |
| A15 | `paper.tex:268` | Acknowledges "Juan Carlos Cristaldo (FADA-UNA)" as a co-author "for supervision, resources, writing-review" and acknowledges "INFONA for collaboration, and MapBiomas Paraguay team for sharing collection 8" — **no partnership letter on file with INFONA confirmed**; partners in `docs/partnerships/ONE-PAGERS-2026-09-07.md` are outreach drafts only. | ⚠ MEDIUM — Acknowledgment implies partnership collaboration that may not exist. |

#### Verdict
- **paper.md / introduction.md / conclusion.md are honest** and explicitly acknowledge the gap.
- **paper.tex is severely out of date** with the measured results: abstract, methods, results table, and conclusion all still report F1 = 0.876 / mIoU = 0.794. This is **the worst markdown-vs-LaTeX drift in the thesis substrate**.
- **FIX priority (highest)**: rewrite paper.tex Abstract, Results table (lines 359–366), and Conclusion (line 165) to use ACTUAL_RESULTS.md values (F1=0.559, mIoU=0.491). Verify the co-author Acknowledgments against `docs/partnerships/ONE-PAGERS-2026-09-07.md` to confirm partnership letter status before submission.

---

### 1.3 P0012 Yvy — Indigenous Territory Deforestation

**File:** `papers/drafts/p0012_yvy_indigenous/`

#### Headline measured values (ACTUAL_RESULTS.md)
- Indigenous/national ratio: **2.90×** (BCa bootstrap 95% CI [1.72, 4.20])
- χ² = 460,597, df = 9, p < 0.001
- Mean indigenous-territory loss: **24.67%** vs national 8.50%
- 10 of 10 territories above national
- Range: 7.21% (Angaité-Filadelfia) to 49.45% (Carmelo Peralta)

#### Aspirational claims found

| # | Location | Claim | Status |
|---|----------|-------|--------|
| A16 | `paper.md:5` Abstract | "**LLaVA-1.6 territorial-conflict F1>0.80 figure quoted in earlier drafts was aspirational; the LLaVA explanation layer has not yet been evaluated**" | ✓ Honestly flagged |
| A17 | `paper.md:104–107` | "Acknowledgements (to be added after FPIC)" — Acknowledgements intentionally blank | ✓ Honest |
| A18 | `paper.md:69–71` conclusion | "per-community map release is not CARE-compliant and requires community engagement before operational deployment" | ✓ Honest |
| A19 | `paper.md:155–159` | "submission rows": "P0012 FPIC engagement" marked as ❌ missing | ✓ Honest |
| A20 | `paper.md:5, conclusion.md:46` | FPIC engagement status: no community contacted yet | ✓ Consistent with `docs/partnerships/FPIC-DECISION-STATUS-2026-09-07.md` |
| A21 | `paper.md:94–96` | "cross-references Hansen deforestation with indigenous territory boundaries... PNAS result by Sze et al. (2022) used a global sample of ~15,000 indigenous territories and found a 22% lower deforestation rate" | ✓ Real literature citation |
| A22 | `paper.tex:269` | Table 3: "**Mby\\'a Guaran\\'i Itakyry & Mby\\'a Guaran\\'i & 2.91**" — ACTUAL_RESULTS.md gives Mbyá Guaraní Itakyry **19.50%** loss (NOT 2.91%). | **🚨 CRITICAL — paper.tex table contains a wrong measured value for one territory** |
| A23 | `paper.tex:342–346` (Acknowledgements) | "We thank community members of the ten indigenous territories included in this study. Names of individual community members are withheld per FPIC requirements." | ⚠ MEDIUM — implies consent was obtained; per `FPIC-DECISION-STATUS-2026-09-07.md` no community has been contacted. **This Acknowledgement fabricates engagement**. |
| A24 | `paper.tex:355–360` | "FPIC engagement status (as of submission): Pending. This manuscript reports only public-data aggregate findings" | ✓ Honest |

#### Verdict
- **paper.md / abstract.md are honest** and the FPIC gap is explicitly flagged.
- **paper.tex has TWO problems**: (i) the per-territory table has a 2.91% number for Mbyá Guaraní Itakyry that contradicts the 19.50% in ACTUAL_RESULTS.md (this also appears in `CH9_cross-cutting.md:91` and is wrong in both places — the actual Eastern-private-reserve territory has 19.50% loss, not 2.91%); (ii) the Acknowledgements section "thank[s] community members" when no community contact has been made.
- **FIX**: correct Mbyá Guaraní Itakyry row in paper.tex Table 3 from 2.91% → 19.50%; re-write Acknowledgements to mirror the honest blank "to be added after FPIC" version that already exists in paper.md.

---

### 1.4 P0025 Yrupe — Soybean Yield Prediction

**File:** `papers/drafts/p0025_yrupe_yield/`

#### Headline measured values (ACTUAL_RESULTS.md)
- Soybean classification: F1 = **0.497** (vs. claimed 0.83) — **did not converge**
- AGB regression: R² = **0.000** (vs. claimed 0.62) — failed
- Yield regression: MAE = **3.20 t/ha** (vs. claimed 0.74 t/ha) — 4.3× worse
- Cross-domain transfer ratio: **0.082** (vs. claimed 0.74) — far below threshold

#### Aspirational claims found

| # | Location | Claim | Status |
|---|----------|-------|--------|
| A25 | `paper.md:5` Abstract | "R²>0.80 / 5,000-fields headline was a target, not a measurement, and has been corrected" | ✓ Honestly flagged |
| A26 | `paper.md:107–109` | Final results table explicitly marks F1=0.83, R²=0.62, MAE=0.74 as "**NOT MEASURED**" | ✓ Honest |
| A27 | `paper.tex:39` Abstract | "F1 = 0.497, MAE = 3.20\\,t/ha on constant predictions... F1 = 0.83 / MAE = 0.74 / 5,000-field figures quoted in earlier drafts" | ✓ Honest |
| A28 | `paper.tex:252–255` | Explicit itemized honest results (F1=0.497, R² undefined, MAE=3.20, transfer 0.082) | ✓ Honest |
| A29 | `paper.tex:230` | "Heads 1 and 2 are trained on synthetic labels" | ✓ Real, transparent |
| A30 | `conclusion.md:34–35` | "**The headline claim was falsified** under the tested setup; publication-quality forward predictive claims about soybean yields are not substantiated." | ✓ Honest |
| A31 | `conclusion.md:69–73` (recommendation) | "submit this paper as a synthetic-dataset cross-domain transfer methodology paper, not as a forward-claim paper" | ✓ Honest |
| A32 | `paper.md:125, 141` | "No operational deployment with INBIO farmers" | ✓ Consistent with no partnership letter |

#### Verdict
- **paper.md, abstract.md, paper.tex are ALL consistently honest** about the failed convergence. The headline numbers (F1=0.497, R²=0, MAE=3.20, transfer=0.082) appear uniformly.
- **No aspirational claims found in this paper**.
- **Minor issue**: `paper.tex:185–230` describes a 12-layer ResNet + 3-task head architecture, but `ACTUAL_RESULTS.md` does not validate whether the architecture was correctly built before training. Recommend documenting that the multi-task CNN **failed to train**, not that the **architecture is wrong**.

---

### 1.5 P0026 Kai — Wildlife Poaching Detection

**File:** `papers/drafts/p0026_kai_poaching/`

#### Headline measured values (ACTUAL_RESULTS.md)
- Synthetic val mAP@0.5: **0.50**
- Real test mAP@0.5: **0.18** (a 0.32 absolute synthetic-to-real gap)
- Per-species real mAP range: 0.05 (reptiles) to 0.25 (large mammals)
- 5-fold CV SD = 0.04 on real

#### Aspirational claims found

| # | Location | Claim | Status |
|---|----------|-------|--------|
| A33 | `paper.md:5` Abstract | "**mAP@0.5>0.70 headline and the WWF/Guyra deployment claims quoted in earlier drafts were aspirational**" | ✓ Honestly flagged |
| A34 | `paper.md:115–116` | Headline numbers table explicitly marks "**mAP > 0.70 operational — NOT MEASURED — Aspirational headline from earlier drafts**" and "**WWF / Guyra deployment, real-time alerts — NOT MEASURED — Aspirational claim, no partnership letter**" | ✓ Honest |
| A35 | `paper.md:153–154` | "❌ A claim about operational deployment with WWF/Guyra, real-time alerts to rangers (no partnership letter on file)" | ✓ Honest, consistent with no letter in `docs/partnerships/` |
| A36 | `conclusion.md:36–39` | "**No partnership with WWF / Guyra / Defensores del Chaco.** No field validation, no ranger-workflow integration. The 'deployed with WWF / Guyra, real-time alerts to rangers' claim in earlier drafts is **aspirational, not measured**" | ✓ Honest |
| A37 | `paper.tex:38–45` | Abstract: "mAP@0.5 of 0.50 (overall), with per-category performance ranging from mAP 0.65 (large mammals) to 0.40 (reptiles). We then evaluated transfer to real-world Paraguayan camera-trap data... Performance on the real data was substantially lower (mAP 0.18)" | ✓ Honest |
| A38 | `paper.tex:240–246` | "The earlier-draft claim of 'deployed in Defensores del Chaco'... no partnership letter on file at the time of writing and is now..." | ✓ Honest |
| A39 | `conclusion.md:155–159` (recommendation) | "submit this paper as a **synthetic-to-real gap measurement** + **cascade baseline measurement**. Avoid framing as an operational deployment or cascaded detector contribution; reviewers will catch the gap. Lead with the methodology, acknowledge the gap, propose the resource-budget for closing it." | ✓ Honest publication advice |
| A40 | `paper.tex:128–129` (Acknowledgments) | "Guyra Paraguay provided the camera-trap data." — the **public dataset is used without further collaboration**, so this is factually accurate (public release, not a partnership). | ✓ Acceptable |

#### Verdict
- **paper.md, abstract.md, paper.tex are ALL consistently honest** about the synthetic-to-real gap and the absence of partnerships.
- **No aspirational claims found in this paper**.
- The pipeline scripts at `scripts/train_yolov8_kai.py`, `scripts/download_guyra_wildlife.py`, `scripts/check_latex.py` are ready for re-train on real data when partnership letter is signed and `GUYRA_API_KEY` is supplied — see `docs/partnerships/T3-M-YOLOV8-STATUS-2026-09-07.md`.

---

### 1.6 P0035 Tatakua — Air-Quality Forecasting

**File:** `papers/drafts/p0035_tatakua_air_quality/`

#### Headline measured values (ACTUAL_RESULTS.md)
- LSTM mean RMSE: **14.7 µg/m³** (vs. claimed 8.6 µg/m³ target — 70% above)
- LSTM mean bias: **+3.4 µg/m³**
- 24% improvement over persistence (19.2 → 14.7)
- Per-station range: 8.2 (Asunción) to 18.6 (Filadelfia/Chaco)
- Peak-episode RMSE reduction: **32%** (vs. claimed 47%)

#### Aspirational claims found

| # | Location | Claim | Status |
|---|----------|-------|--------|
| A41 | `paper.md:5` Abstract | "**Ministry-of-Health deployment claim quoted in earlier drafts was aspirational**; deployment depends on resolving the rural-station gap" | ✓ Honestly flagged |
| A42 | `paper.md:107–116` (Honest Reporting Note) | Explicit table of measured vs. aspirational | ✓ Honest |
| A43 | `paper.md:115` | "**Tatakua beats persistence by 24% RMSE (19.2 → 14.7 µg/m³), which is a meaningful LSTM signal on Paraguay OpenAQ data**" | ✓ Honest, measured |
| A44 | `paper.tex:33–52` Abstract | Title: "with measured mean RMSE = 14.7 µg/m³ for PM₂.₅ (24% improvement over persistence)". Abstract explicitly says "This is 70% above the 8.6 µg/m³ target" | ✓ Honest |
| A45 | `paper.tex:48` | "There is **no Ministry-of-Health deployment** of this system; that claim in earlier drafts was aspirational." | ✓ Honest |
| A46 | `paper.tex:260–272` | "(b) operational public-health deployment)... (i) operational deployment'' mentioned in earlier drafts of this Discussion does not exist" | ✓ Honest |
| A47 | `conclusion.md:38–41` | "**published RMSE target of 8.6 µg/m³ was not met**" + "**No public-health deployment exists. The earlier 'deployed at the Ministry of Health' claim was aspirational and has been removed.**" | ✓ Honest |
| A48 | `paper.tex:288–294` | "LSTM-1layer RMSE: 4.8 µg/m³ (24% better than persistence baseline), LSTM-2layer RMSE: 6.1 µg/m³ (worse than 1layer — overfitting), Peak biomass burning episode: -32% error reduction" — **ACTUAL_RESULTS.md reports a single 3-layer × 64-hidden unit LSTM at 14.7 µg/m³**. The architecture, layer count, and RMSE values in the .md trail (in CH8 paper body) and the paper.md do **not match** the architecture described in ACTUAL_RESULTS.md. The 14.7 µg/m³ figure is the headline. | **🚨 CRITICAL — `conclusion.md` itself is consistent, but `thesis/CH8_paper6_P0035_tatakua.md` line 57 and the `paper.md` body may use architecture descriptions (LSTM-2layer, LSTM-4layer) that aren't the implementation in ACTUAL_RESULTS.md (3 layers × 64 hidden).** |

#### Verdict
- **paper.tex / abstract.md / conclusion.md are honest** about the aspirational target and aspirational Ministry-of-Health deployment.
- **One inconsistency**: the architecture described in `paper.md` Section 8 (LSTM-2layer, LSTM-4layer vs. persistence) doesn't match the architecture in `ACTUAL_RESULTS.md` (single 3-layer × 64-hidden LSTM). The 14.7 µg/m³ measured value should be tied to a specific architecture description.
- **FIX**: confirm the actual trained LSTM architecture with `outputs/p0035/kfold_results.json` and re-write the methods section to be consistent with the implemented model.

---

## 2. Thesis Chapters Audit

### 2.1 CH1_introduction.md — STALE NUMBERS 🚨 CRITICAL

**File:** `thesis/CH1_introduction.md`

| # | Line | Claim | Issue |
|---|------|-------|-------|
| C1 | 19 | "the ten indigenous territories in the Gran Chaco have an average deforestation rate of **28.4%**, which is **3.3 times the national average** of 8.5%" | ACTUAL_RESULTS.md says **24.67% mean** and **2.90× ratio**. The 28.4% and 3.3× are stale numbers (likely from an earlier pilot with a smaller territory sample). |
| C2 | 65 (Contributions) | "3.0× multiplier" — consistent with ACTUAL_RESULTS.md (24.67 / 8.50 = 2.90, often reported as 3.0× in other docs) | ✓ Acceptable (3.0× is a rounded shorthand) |

**Severity**: 🚨 CRITICAL — these are introduced in the very first paragraph of the thesis Introduction; readers will see wrong numbers first.

**FIX**: Replace `28.4%` → `24.67%` and `3.3 times` → `2.90×` in CH1 line 19.

---

### 2.2 CH9_cross-cutting.md — STALE NUMBERS ⚠ MEDIUM

**File:** `thesis/CH9_cross-cutting.md`

| # | Line | Claim | Issue |
|---|------|-------|-------|
| C3 | 41–43 | "**16,628 km² lost 2001-2023 (2,755 MtCO₂e)** ... Alto Paraguay **28.49%** of total ... Indigenous territories at **3.0× national rate** ... **Carbon pattern:** Verra projects under-claim carbon loss by **30-50%**" | The 16,628 km² and 3.0× are correct; the **"30-50%"** range is the old aspirational range — ACTUAL_RESULTS.md gives **+35.9% mean, range 33.3%–50.0%**. |
| C4 | 91 | Table row: "**Itakyry | Mbyá Guaraní | 2.91%**" | ACTUAL_RESULTS.md says **Mbyá Guaraní Itakyry = 19.50%** loss, not 2.91%. (Same error as paper.tex Table 3 for P0012.) |
| C5 | 50 | "mAP@0.5 = 0.50 on synthetic validation but **drops to 0.18 on 5,000 real camera-trap images**" | ✓ Consistent with ACTUAL_RESULTS.md |
| C6 | 76 | "the **Wildlife ratio (0.42) is the synthetic-to-real drop**" — but ACTUAL_RESULTS synthetic-to-real drop is **0.50 → 0.18 = 0.32 absolute**. The "0.42" is unexplained. | ⚠ MEDIUM — references an unmeasured ratio. |

**Severity**: ⚠ MEDIUM — the 30-50% Verra claim is a stale range; the 2.91% for Mbyá Guaraní Itakyry is a stale per-territory number.

**FIX**: replace "30-50%" with "35.9% mean (range 33.3%–50.0%)" in CH9 line 43; correct Itakyry row to **19.50%** in CH9 line 91.

---

### 2.3 CH10_discussion.md — STALE NUMBERS ⚠ MEDIUM

**File:** `thesis/CH10_discussion.md`

| # | Line | Claim | Issue |
|---|------|-------|-------|
| C7 | 13 | "indigenous territories in Paraguay's Chaco are deforested at **3.3 times the national average**" | Stale; ACTUAL_RESULTS says **2.90×** |
| C8 | 40 | "**3.0× the national rate**" (carbon reversal risk) | ✓ Consistent (rounded shorthand) |
| C9 | 48 | "**Prithvi-Lite**... F1 ≈ 0.85 vs. from-scratch F1 ≈ 0.017 on dry-forest pilots" | The 0.017 figure is the older U-Net baseline run referenced in `STATUS.md:52` and `FINAL_REPORT.md:96`; the **measured 2026-08-03 value is F1 = 0.559**, not 0.017. This stale 0.017 number appears in multiple files. |

**Severity**: ⚠ MEDIUM

**FIX**: replace "3.3 times" → "2.90×" in CH10 line 13; replace "≈ 0.017" → "0.559" in line 48 of the dry-forest baseline reference.

---

### 2.4 CH11_conclusion.md — MOSTLY HONEST ✓

**File:** `thesis/CH11_conclusion.md`

| # | Line | Claim | Issue |
|---|------|-------|-------|
| C10 | 19 | "**3.0× multiplier**" | ✓ Consistent (rounded) |
| C11 | 27 | "Prithvi-Lite 'F1=0.85+' headline quoted in earlier drafts of this chapter was a literature benchmark, not a Yvutu measurement" | ✓ Honest |
| C12 | 88–94 (Honest Reporting Notes table) | Explicit table of aspirational → measured substitutions | ✓ Honest |
| C13 | 95 (citation verification row) | "**213 verified, 13 LIKELY, 0 NOT_FOUND**" — this contradicts `ROUND_6_AUDIT.md` which reports 78 unresolved entries | ⚠ MEDIUM — the citation-vetting row in CH11 overstates verification |

**Severity**: Low–Medium

**FIX**: align CH11 citation row with `ROUND_6_AUDIT.md` (92 of 183 confirmed, 12 fixed, 78 unresolved).

---

### 2.5 CH2_methodology.md — MOSTLY HONEST ✓

**File:** `thesis/CH2_methodology.md`

- §2.2.2 Yvutu section explicitly cites `ACTUAL_RESULTS.md` and reports F1 = 0.559 (U-Net), F1 = 0.497 (Prithvi mock fallback). ✓ Honest
- §2.2.6 Kai section reports mAP = 0.50 synthetic, 0.18 real. ✓ Honest
- §2.2.4 Yvy section states "indigenous territories are deforested at 3.0× the national average". ✓ Consistent (rounded)
- §2.2.7 Tatakua section reports RMSE = 14.7 µg/m³ and 70%-above-target framing. ✓ Honest

**Verdict**: honest and internally consistent.

---

### 2.6 CH3–CH8 (paper-summary chapters) — ALL HONEST ✓

Each thesis-voice paper-summary chapter (CH3 through CH8) **directly re-uses the honest abstract.md** from the corresponding paper/drafts/p*/abstract.md. Their claims match the corresponding ACTUAL_RESULTS.md.

**Verdict**: ✓ No aspirational claims found in CH3–CH8.

---

### 2.7 thesis/MAIN/thesis.tex — WRONG TATAKUA NUMBERS 🚨 CRITICAL

**File:** `thesis/MAIN/thesis.tex`

| # | Line | Claim | Issue |
|---|------|-------|-------|
| C14 | 30 (Abstract) | "RMSE 14.7 µg/m³ on air-quality forecasting" — correct | ✓ |
| C15 | 286–294 (P0035 Results section) | "**LSTM-1layer RMSE: 4.8 µg/m³** (24% better than persistence baseline), **LSTM-2layer RMSE: 6.1 µg/m³** (worse than 1layer — overfitting), **Peak biomass burning episode: -32% error reduction, 12 OpenAQ stations, 13-month retrospective, MAE = 11.72 µg/m³ figure in earlier drafts was aspirational. The measured RMSE 4.8 µg/m³ is well within the operational range for air-quality forecasting.**" | **🚨 CRITICAL — three wrong claims:** (i) ACTUAL_RESULTS.md says **single LSTM at 14.7 µg/m³, not two-layer/one-layer split with 4.8/6.1**; (ii) ACTUAL_RESULTS.md says **32% peak-episode RMSE reduction (positive)**, not "-32%"; (iii) the "aspirational MAE = 11.72" framing is from much earlier drafts, not from 2026-08-11 (the latest aspirational MAE was 5 µg/m³; 11.72 was a different old draft). |
| C16 | 339 (Conclusions) | "**4.8 µg/m³ RMSE air-quality LSTM** (24% over persistence)" | **🚨 CRITICAL — repeats the wrong 4.8 µg/m³ figure in the thesis conclusions.** |

**Severity**: 🚨 CRITICAL — these are wrong measured values in the unified thesis main file, contradicting both `papers/drafts/p0035/ACTUAL_RESULTS.md` and the corresponding `paper.tex` for P0035.

**FIX**: Replace the lines 286–294 Tatakua section with the ACTUAL_RESULTS.md content (single 3-layer × 64-hidden LSTM, RMSE 14.7 µg/m³, bias +3.4, 32% peak episode reduction, 12 stations, 12-month retrospective).

---

### 2.8 thesis/references.bib — Note ✓

The `references.bib` does contain fabricated citation stubs flagged in `papers/drafts/CITATION_STUBS.md` (alphaearth2025, baumann2022south_american, cristaldo2024paraguay, huang2021paraguay, rikap2021indigenous, zheng2015fine_grained — all marked DELETED). The integrity audit is OUT OF SCOPE for this aspirational-claims audit, but flagged for completeness.

---

## 3. Partnership Evidence Audit

Per `docs/partnerships/` (last modified 2026-09-07):

| Partner | Status on file | Used in paper |
|---------|----------------|----------------|
| INFONA | Draft one-pager (Option C in `FPIC-DECISION-STATUS-2026-09-07.md`) — not sent | P0011 (Yvutu) — Acknowledgments line 422-426 of `paper.tex` thanks INFONA "for collaboration" |
| INDI | Draft one-pager + decision memo — not sent | P0012 (Yvy) — `paper.tex` Acknowledgements line 345: "thank community members of the ten indigenous territories" |
| INBIO | No one-pager — blocked on partnership | P0025 (Yrupe) — `paper.md` line 125, 141 acknowledge "no operational deployment with INBIO farmers" |
| SENEPA | Draft one-pager — not sent | P0035 (Tatakua) — `paper.md` acknowledges "Ministry-of-Health deployment" aspirational |
| Verra | No one-pager — independent analysis | P0010 (Yvyra) — `paper.md` line 127 acknowledges "no partnership with Verra" |
| WWF Paraguay | No one-pager | P0026 (Kai) — `paper.md` line 49: "No partnership letter is on file with WWF Paraguay" |
| Guyra Paraguay | One-pager drafted; pipeline ready; `GUYRA_API_KEY` needed | P0026 (Kai) — public dataset access only |

**Aspirational partnership/deployment claims:**
- All papers **explicitly acknowledge** that no operational partnership/deployment exists. None of the falsified claims (mAP>0.70 deployed, Ministry-of-Health deployment, FPIC engagement completed) appear in the **final text** of paper.md/paper.tex after the 2026-08-10/11 honest-reporting passes — **with the following exceptions:**

  - **P0011 paper.tex (line 422–426)** Acknowledgments thank "INFONA for collaboration" — this implies a working relationship that, per `docs/partnerships/ONE-PAGERS-2026-09-07.md` partner #1, is only a drafted one-pager awaiting Iván's review. **MEDIUM severity**.
  - **P0012 paper.tex (line 345)** Acknowledgments "thank community members of the ten indigenous territories" — per FPIC-DECISION-STATUS, **no community has been contacted**. **MEDIUM severity**.

**FIX**: Before submitting paper.tex files to journals, replace the Acknowledgements sections that imply partnership/FPIC engagement that hasn't happened, with placeholders that mirror the honest paper.md versions.

---

## 4. Aggregate Findings

### 4.1 Critical (must fix before any submission)

1. **P0011 paper.tex (Yvutu)**: Abstract, Results table, and Conclusion still report F1=0.876, mIoU=0.794 — directly contradicts paper.md and ACTUAL_RESULTS.md (F1=0.559, mIoU=0.491). **Fix by replacing all such references with measured values.**
2. **P0010 paper.tex (Yvyra)**: Title and main text still report "range 27–41%" — actual range 33.3%–50.0%. **Plus a self-contradiction: line 57 claims a 30-project replication was completed; line 70–72 admits it wasn't.**
3. **P0012 paper.tex (Yvy)**: Table 3 lists Mbyá Guaraní Itakyry at 2.91% — ACTUAL_RESULTS.md says 19.50%. Same error in CH9_cross-cutting.md table.
4. **CH1_introduction.md line 19**: "average deforestation rate of **28.4%**" and "**3.3 times** the national average" — ACTUAL_RESULTS.md says **24.67% mean / 2.90×**.
5. **CH10_discussion.md line 13**: "**3.3 times the national average**" — stale.
6. **thesis/MAIN/thesis.tex lines 286–294 + 339**: Tatakua LSTM results given as RMSE 4.8 µg/m³ and 6.1 µg/m³ (two-layer architecture) — ACTUAL_RESULTS.md says 14.7 µg/m³ (single 3-layer × 64-hidden LSTM).

### 4.2 Medium (should fix)

7. **P0010 paper.tex**: Acknowledgements thank INFONA despite the partnership letter existing only as a draft one-pager.
8. **P0012 paper.tex (line 345)**: "thank community members of the ten indigenous territories" — false; no FPIC engagement per `FPIC-DECISION-STATUS-2026-09-07.md`.
9. **CH11_conclusion.md line 95**: Citation count contradicts `ROUND_6_AUDIT.md` (says 213 verified but ROUND_6 found 78 unresolved).
10. **P0026 paper.tex**: Interleaved honest and aspirational discussion is acceptable but the Acknowledgments should be re-verified.

### 4.3 Low (acceptable as-is)

11. P0025 paper.md/paper.tex are uniformly honest.
12. P0026 paper.md/paper.tex are uniformly honest.
13. P0035 paper.md/paper.tex are honest (modulo architecture description consistency check).
14. CH2, CH3–CH8 are uniformly honest.
15. Partnership files are templates/drafts awaiting Iván's review, consistent with the universe of claims.

---

## 5. Recommendations (FIX Plan)

**Priority 1 (CRITICAL — must do before any submission):**
1. Rewrite P0011 paper.tex Abstract, Methods, Results table (lines 359–366), and Conclusion (line 165) to use measured values (F1=0.559 U-Net, F1=0.497 mock-Yvutu, mIoU=0.491, Precision=0.099, Recall=0.987).
2. Update P0010 paper.tex title from "27–41%" to "33.3%–50.0%" and remove the "30-project replication" claim (line 57) that contradicts the caveat 2 paragraphs later (line 70–72).
3. Correct P0012 paper.tex Table 3 row for Mbyá Guaraní Itakyry from **2.91%** → **19.50%**, and same correction in CH9_cross-cutting.md table.
4. Update thesis/MAIN/thesis.tex lines 286–294 (P0035 Results) to use measured 14.7 µg/m³ from ACTUAL_RESULTS.md, not the invented 4.8/6.1 numbers; and update line 339 accordingly.
5. Update thesis/CH1_introduction.md line 19: "28.4% / 3.3 times" → "24.67% / 2.90×".
6. Update thesis/CH10_discussion.md line 13: "3.3 times" → "2.90×".

**Priority 2 (MEDIUM — should do):**
7. Replace P0010 and P0011 paper.tex Acknowledgements to mirror the honest paper.md versions.
8. Update CH11_conclusion.md citation count to match ROUND_6_AUDIT.md figures.
9. Re-verify the LSTM architecture in P0035 paper.tex (line 280–294) and CH8_paper6_P0035_tatakua.md (line 57) against ACTUAL_RESULTS.md "3 layers × 64 hidden units" — they should be consistent.

**Priority 3 (LOW — review):**
10. Cross-reference the cross-domain transfer ratio claims (CH9 line 76 "Wildlife ratio = 0.42") against ACTUAL_RESULTS.md (0.32 absolute gap, not 0.42 ratio).

---

## 6. Files Audited

### Per-paper drafts (6 papers × 6 files)

| Paper | paper.md | paper.tex | abstract.md | introduction.md | conclusion.md | ACTUAL_RESULTS.md |
|-------|----------|-----------|-------------|-----------------|---------------|-------------------|
| P0010 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| P0011 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| P0012 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| P0025 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| P0026 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| P0035 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### Thesis (11 files)

- thesis/CH1_introduction.md ✓
- thesis/CH2_methodology.md ✓
- thesis/CH3_paper1_P0011_yvutu.md ✓
- thesis/CH4_paper2_P0010_yvyra.md ✓
- thesis/CH5_paper3_P0012_yvy.md ✓
- thesis/CH6_paper4_P0025_yrupe.md ✓
- thesis/CH7_paper5_P0026_kai.md ✓
- thesis/CH8_paper6_P0035_tatakua.md ✓
- thesis/CH9_cross-cutting.md ✓
- thesis/CH10_discussion.md ✓
- thesis/CH11_conclusion.md ✓
- thesis/MAIN/thesis.tex ✓

### Partnership evidence (5 files)

- docs/partnerships/ONE-PAGERS-2026-09-07.md ✓
- docs/partnerships/FPIC-DECISION-STATUS-2026-09-07.md ✓
- docs/partnerships/IRB_PROTOCOL_PARAGUAY_UNA-2026-09-07.md ✓
- docs/partnerships/JOURNAL-SUBMISSION-MATRIX-2026-09-07.md ✓
- docs/partnerships/T3-M-YOLOV8-STATUS-2026-09-07.md ✓

### No files written or modified by this audit beyond this report.

---

## 7. Summary Metrics

| Metric | Count |
|--------|------:|
| Papers audited | 6 |
| Per-paper files read | 36 (6 papers × 6 files) |
| Thesis chapters audited | 11 |
| Thesis main.tex audited | 1 |
| Partnership files audited | 5 |
| Total aspirational claims found | 48 |
| Of which CRITICAL | 6 |
| Of which MEDIUM | 4 |
| Of which LOW (verified-honest or acceptable-as-is) | 38 |

The Round-1 honest-reporting work in August 2026 was substantially successful at the abstract/conclusion layer. **The remaining critical issues are concentrated in (a) the paper.tex LaTeX submission templates, which were not updated in lockstep with paper.md, and (b) the unified thesis/MAIN/thesis.tex file.** These are likely the highest-leverage fixes before any journal submission.

---

**End of Audit #3.**
