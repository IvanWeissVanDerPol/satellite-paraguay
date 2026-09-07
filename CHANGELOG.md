# CHANGELOG.md — Thesis-Affecting Commits

> **Purpose:** Map commits to thesis sections so reviewers can trace provenance.
> Format: Commit → Theme → Affected files → Thesis section

## Theme: Citation verification (the Round-5/6 cleanup)

| Commit | Date | Theme | Affects | Thesis section |
|---|---|---|---|---|
| `c8c0c10` | 2026-09-07 | **Round-6:** 7 DOI fixes applied, 76 false-positive confirmed | `thesis/references.bib` (7 entries) | CH02 Literature Review, all 6 papers' Related Work |
| `13b3e03` | 2026-09-04 | Refresh data_audit + drift_note from post-fix run | `outputs/data_audit.json` | CH03 Methodology |
| `6ec9595` | 2026-09-04 | Style: black/isort on citation-stub updater | `scripts/check_citations.py` | tooling |
| `9a36592` | 2026-09-04 | **Round-5 follow-up:** purged 7 fabricated keys (baumann2022south_american, huang2021paraguay, alphaearth2025, cristaldo2024paraguay, rikap2021indigenous, zheng2015fine_grained) | Prose in 4 papers | All 6 papers |
| `cdf1606` | 2026-09-04 | Security audit round 2 — CI artifact data-leak guard | `tests/test_ci_artifact_security.py` | tooling |
| `7fc3efa` | 2026-09-04 | **Round-5:** 6 verified citation entries added (carroll2022, dinerstein2020, russwurm2020, donkelaar2010, norouzzadeh2018, kamilaris2018) | `thesis/references.bib` (+6) | All papers |
| `02f181e` | 2026-09-04 | Converted `related_work.md` → `\section{Related Work}` in 6 papers | `papers/drafts/*/paper.tex` (6) | Each paper's Related Work |
| `699d782` | 2026-09-04 | **Round-4:** Citation cleanup + per-paper bib slices | `papers/drafts/*/references.bib` | Per-paper bibliography |

## Theme: Citation reconstruction (Round-1/2/3)

| Commit | Date | Theme | Affects | Thesis section |
|---|---|---|---|---|
| `6c359da` | 2026-09-04 | **Round-3:** Citation verification + prose polish | All 6 papers prose | All papers |
| `874b36c` | 2026-09-03 | Per-paper `related_work.md` synthesis (thesis-prose ready) | `papers/drafts/*/related_work.md` (6) | Each paper's Related Work source |
| `1689af5` | 2026-09-03 | Made citation integration idempotent + cleanup | `scripts/convert_related_work.py` | tooling |
| `06cd3b7` | 2026-09-03 | Cleanup redundant header + commit substrate deliverables | `scripts/substrate_sync.py` | tooling |
| `c263668` | 2026-09-03 | **Round-2:** 47 verified CrossRef-checked DOIs | `thesis/references.bib` (+47) | All papers |
| `4180844` | 2026-09-03 | Register citation verification — 47 of 226 verified | `papers/drafts/CITATION_STUBS.md` | Citation audit trail |
| `94a66b1` | 2026-09-03 | Same as above (duplicate cleanup) | same | same |
| `ce1f7a0` | 2026-09-03 | Register Round-2 100-iter research findings | `outputs/research_round_2.md` | Discovery |
| `a5a73fa` | 2026-09-03 | Register 100-iter research campaign | `outputs/research_100_iter.md` | Discovery |
| `68144be` | 2026-09-03 | Register research findings — 24 new entries + master catalog | `thesis/references.bib` (+24) | All papers |
| `ec960dc` | 2026-09-03 | 30-minute professor reading path + sync-docs fix | `PROFESSOR_READING_PATH.md` | Navigation |

## Theme: Repo infrastructure (this Round)

| Commit | Date | Theme | Affects |
|---|---|---|---|
| (pending) | 2026-09-07 | **Repo setup:** CLAUDE.md + AUDIT + TODO + CHANGELOG + verify_bib_dois.py + run_tests.sh | `CLAUDE.md`, `TODO.md`, `CHANGELOG.md`, `papers/drafts/AUDIT/*`, `scripts/verify_bib_dois.py`, `scripts/run_tests.sh` |

## Theme: Worker infrastructure (autonomous ops)

| Commit | Date | Theme | Affects |
|---|---|---|---|
| `a1b8ea4` | 2026-09-02 | Content-based gate on picker — skip Vast.ai/IRB/FPIC tasks | Workers |
| `3096f87` | 2026-09-02 | flake8 + mypy + black + isort clean on Tier 2 | `src/`, `scripts/` |
| `e879227` | 2026-09-02 | AUTONOMOUS_WORKERS.md — cron wiring + hard-constraint spec | `docs/` |
| `efc3906` | 2026-09-02 | Two autonomous cron workers + 24 pytest guards | Workers + tests |
| `ae527ba` | 2026-09-02 | validate_data.py — honest data-layer audit + 10 pytest guards | `scripts/`, tests |
| `4b09dd5` | 2026-09-02 | p0025: experiments.md + label test-fixture rand() sites | `papers/p0025`, tests |
| `29e7f02` | 2026-08-22 | p0025: FAO/MAG public yield data puller | `scripts/download_fao_mag_p0025.py` |
| `3cc207b` | 2026-08-22 | p0012: INE/INDI public data puller (no FPIC needed) | `scripts/download_ine_indi_p0012.py` |
| `cb9581f` | 2026-08-22 | p0035 + p0026: LSTM v2 multi-station + iNaturalist | scripts |
| `305189c` | 2026-08-22 | ACTIVATION.md + 4 Tier S application drafts | docs |
| `a971bce` | 2026-08-22 | COMPLETE-PLAN.md master synthesis | docs |
| `bf0813e` | 2026-08-22 | FUNDING_PLAN.md + funding-applications.log | docs |
| `f9b909c` | 2026-08-22 | Phase-2.1: real-data acquisition downloaders | scripts |
| `07c2479` | 2026-08-22 | Phase-1: pilot-readiness docs + reproducibility tests | docs, tests |
| `2eda3ed` | 2026-08-22 | Phase-0: agent-owned deliverables for 12-week roadmap | docs |

## Theme: Thesis-writing sessions (Aug 12)

| Commit | Date | Theme | Affects | Thesis section |
|---|---|---|---|---|
| `6847250` | 2026-08-12 | p0026: write all 6 paper sections — 21% → 90% | `papers/p0026/paper.tex` | p0026 Kai |
| `b7dcc3e` | 2026-08-12 | p0025: write all 6 paper sections — 24% → 92% | `papers/p0025/paper.tex` | p0025 Yrupe |
| `b15e61f` | 2026-08-12 | p0010: write all 6 paper sections — 22% → 73% | `papers/p0010/paper.tex` | p0010 Yvyra |
| `211c338` | 2026-08-12 | p0012: write all 6 paper sections — 25% → 92% | `papers/p0012/paper.tex` | p0012 Yvy |
| `a5872f7` | 2026-08-12 | p0011: write all 6 paper sections — 35% → 98% | `papers/p0011/paper.tex` | p0011 Yvutu |
| `8f128fa` | 2026-08-12 | P0035 paper sections + CI integration | `papers/p0035/paper.tex` | p0035 Tatakua |
| `cbdd704` | 2026-08-12 | Resolve 5 citation conflicts + add 5 pytest guards | `thesis/references.bib`, tests |
| `cb2c480` | 2026-08-12 | Add BUSINESS_MODEL.md (USD 1.25M-5M Y1) + COMMERCIALIZATION_ROADMAP.md | docs |
| `5347383` | 2026-08-12 | Fail-loud on missing data (no np.random.rand silent fills) | code, README |
| `d3cb374` | 2026-08-12 | BRUTAL_ROAST.md, STATUS.md, AGENT_TODO.md | docs |
| `88e337e` | 2026-08-11 | Honesty pass — fix fabricated claims | code, docs |
| `65621c4` | 2026-08-10 | Honest-reporting pass — fix aspirational abstracts + add LICENSE/CITATION | code, docs |
| `c0e4d88` | 2026-08-04 | Milestone: 40% coverage through systematic script refactoring | tests |

## Theme: CI / LaTeX hardening (Aug 13)

| Commit | Date | Theme |
|---|---|---|
| `728a3dd` + downstream | 2026-08-13 | LaTeX / CI / pytest hardening (13 fix commits, see git log) |
| `04eea81` | 2026-08-13 | Expand CH3-CH8 chapters with paper methods + results (3.97k → 11.18k words) |
| `c82b005` | 2026-08-13 | Pixel area 0.09 ha → 0.0625 ha in papers + code |
| `a0b8a93` | 2026-08-12 | Install requirements-ci.txt + lazy rasterio import in conftest |

## Theme: Initial scaffolding (Aug 4-12)

Pre-Aug 12 commits — see `git log --reverse` for full history. Key ones:
- `c0e4d88` (2026-08-04): Milestone: 40% coverage
- Earliest repo history lives in pre-Aug-2026 milestones (see Status.md)

---

## How to use this file

1. **Reviewer asks:** "Where did the citations come from?"
   → Point them to "Theme: Citation reconstruction" + "Theme: Citation verification"
2. **Reviewer asks:** "How do I re-run the citation verification?"
   → `scripts/verify_bib_dois.py --resume` + see `papers/drafts/AUDIT/README.md`
3. **Reviewer asks:** "What's left to do?"
   → `TODO.md`
