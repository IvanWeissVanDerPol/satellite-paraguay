# TODO.md — Defense-Blocking Items

> **Purpose:** A single checklist of what's blocking defense submission.
> Updated 2026-09-07 by Round-6 setup session.
>
> **Rule:** Each item is either 🔴 CRITICAL (blocks defense) or 🟡 NICE (improves quality).
> Items marked as 💡 are exploration, not commitments.

---

## 🔴 CRITICAL — Must fix before defense

### C1. LaTeX compile check
- **Status:** Untested in current sandbox
- **Why:** If `pdflatex` fails on any of the 6 papers, defense submission is dead on arrival
- **Action:** Run `pdflatex paper.tex` for all 6 papers; fix any errors
- **Owner:** Laptop with TeX Live (not in sandbox)
- **Estimate:** 30 min compile × 6 = 3h

### C2. Spanish translation of Chapters 0-11
- **Status:** All 11 chapters in English
- **Why:** FADA thesis at FP-UNA is filed in Spanish; FADA reviewers expect Spanish
- **Action:** Translate CH00-Abstract, CH01-Intro, CH02-LitReview, CH03-Methodology, CH10-Integration, CH11-Conclusions
- **Owner:** Native speaker + agent drafting
- **Estimate:** 4-6h

### C3. Unified thesis PDF (the monograph)
- **Status:** 6 paper PDFs exist independently; no bound monograph
- **Why:** FADA requires single PDF containing CH0-11 + all 6 papers as appendices
- **Action:** Build `thesis/main.tex` that includes 11 chapters + 6 papers; produce single PDF
- **Owner:** Laptop
- **Estimate:** 1h after C1 + C2 done

### C4. Real data for papers with low "data real" score
- **P0011 Yvutu:** 5/100 — need 30 Hansen tiles, 150 Sentinel-2 tiles
- **P0025 Yrupe:** 0/100 — synthetic labels only, need real FAO yield data
- **P0012 Yvy Indigenous:** FPIC BLOCKER — no ethics review, see C5

### C5. FPIC (Free, Prior, Informed Consent) for indigenous data
- **Status:** P0012 Yvy Indigenous is BLOCKED at 0% ethics
- **Why:** Indigenous community partnership required before publication
- **Action:** Reach out to 10 communities documented in INBIO dataset; obtain consent
- **Owner:** Iván (real-world interaction, not agent-taskable)
- **Estimate:** Weeks to months

---

## 🟡 MEDIUM — Important but not strictly blocking

### M1. Refresh FADA submission packet
- **Status:** Last refreshed 2026-08-13 in commit `c8c0c10`
- **Action:** Move `STATUS.md`, `CLAUDE.md`, `AUDIT/` into `submission_packet/`
- **Estimate:** 30 min

### M2. Decision on CITATION_STUBS (6 broken `\cite{}`)
- **Status:** Round-5 + Round-6 cleanup removed 7 fabricated citations
- **Action:** Run `check_citations.py --all`; if 0 broken, archive `CITATION_STUBS.md`
- **Estimate:** 5 min (verification only)

### M3. Train real models on real data (3 papers)
- **P0010:** AlphaEarth benchmark not run (only literature)
- **P0011:** U-Net honest baseline F1=0.017 (mock fallback at 0.497)
- **P0012:** LLaVA stub, no labeled conflict benchmark

### M4. Defense slides / talk
- **Status:** No slides authored yet for FADA defense
- **Action:** Author slides per thesis chapter highlighting Tier-A results
- **Estimate:** 4-6h

---

## 💡 EXPLORATORY — Not committed yet

### E1. Round-7 citation re-verification
- **Status:** Round-6 cleaned what could be cleaned automatically
- **Action:** Manual review of the 83 "no good CrossRef match" entries
- **Estimate:** 5-10h
- **Decision:** Skip unless time permits — Round-6 already reduced risk

### E2. Auto-update data-claim audit with revised paths
- **Status:** 9 of 17 claims are "off-repo" / "synthetic"
- **Action:** Update `outputs/data_audit.json` with canonical paths after C4

### E3. Author `slides/` HTML version of the talk
- **Status:** No slides
- **Why:** HTML slides are easier to share than PDF in FP-UNA context

---

## ✅ DONE — Recently completed

| Item | Commit | Date |
|---|---|---|
| Round-1: Reconstruct 226 citations from related_work prose | `c263668` | 2026-08-13 |
| Round-3 citation verification + prose polish | `6c359da` | 2026-08-13 |
| Round-4 citation cleanup + per-paper slices | `699d782` | 2026-08-13 |
| Related-work → `\section{Related Work}` LaTeX | `02f181e` | 2026-08-13 |
| Round-5: 6 verified entries + 7 fabricated flagged | `7fc3efa` | 2026-09-04 |
| Round-5 follow-up: purge 7 fabricated keys | `9a36592` | 2026-09-04 |
| Repo infrastructure: CLAUDE.md + AUDIT + verify_bib_dois.py | `7c86263` | 2026-09-07 |
| Document Hermes-hook noise on background test runs | `d6c7632` | 2026-09-07 |
| **Tier-1: 5 Conclusion sections + cite-pattern regression guard** | `6661c67` | 2026-09-07 |
| **Tier-2: defense_check.py wrapper + Makefile targets** | `1cb6c8b` | 2026-09-07 |
| **Fix MAE<5 defense finding: sanction CH11 + qualify row** | `eeeca93` | 2026-09-07 |
| Round-6: 7 DOI fixes applied, 76 false-positive confirmed | `c8c0c10` | 2026-09-07 |
| Repo infrastructure: CLAUDE.md + AUDIT + verify_bib_dois.py | (this commit) | 2026-09-07 |

---

## How to add a new item

1. Pick the severity tier (🔴 / 🟡 / 💡)
2. Add it under the right section
3. Add a "Status" line so others know where to start
4. Add "Estimate" so we can plan time

When you finish an item, **move it to the ✅ DONE section** with the commit SHA.
Don't delete — the trail matters.
