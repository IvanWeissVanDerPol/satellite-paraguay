# Changelog — SatelliteCV-Paraguay

All notable changes to this repository are documented here.

## [Unreleased] — 2026-08-10

### Honest-reporting pass (autonomous)

The branch `chore/honest-reporting-pass-2026-08-10` updates the six paper
abstracts and appends a "Honest Reporting Note" to each paper.md so that
the measured values (per `ACTUAL_RESULTS.md`) replace the literature-benchmark
headlines that previously opened each abstract. See `WORKLOG_2026-08-10.md`
for the full change log and the rationale.

### Added

- `LICENSE` — CC-BY-NC-4.0 with data-source carve-outs (Hansen, MapBiomas,
  Sentinel-2, OpenAQ, Verra, INDI-CARE-controlled).
- `CITATION.cff` — citation metadata for GitHub "Cite this repository" and
  Zenodo DOI minting on next release.
- `references.bib` (repo root) — unified bibliography of 180 unique entries
  merged from `thesis/references.bib` (120) + `papers/references.bib` (65),
  with 5 key conflicts flagged under a `% CONFLICTS` section.
- `scripts/merge_bib.py` — reproducible merger (deterministic, idempotent).
- `docs/REAL_TODO.md` — 30-item real TODO replacing the stale 345-item
  `docs/COMPREHENSIVE_TODO.md` (kept for archeology).
- `WORKLOG_2026-08-10.md` — session log of the autonomous honesty pass.

### Changed

- All six `papers/drafts/<slug>/abstract.md` now cite measured values from
  `ACTUAL_RESULTS.md` instead of literature-benchmark headlines.
- All six `papers/drafts/<slug>/paper.md` carry an appended "Honest Reporting
  Note (added 2026-08-10)" section identifying unsupported claims and the
  concrete work needed before submission.

## [Unreleased] — 2026-08-04

### Added
- 80+ references in `thesis/references.bib`
- Cross-paper transfer learning experiment (RQ4, H3) — scripts/cross_transfer_experiment.py
- Per-pixel carbon model with Chave 2014 allometric — scripts/per_pixel_carbon.py
- Carbon credit integrity verifier — scripts/carbon_credit_verifier.py
- MapBiomas temporal comparison 2015-2023 — scripts/mapbiomas_temporal.py
- Statistical significance tests (McNemar, chi², bootstrap) — scripts/statistical_tests.py
- Interactive Plotly + Folium visualizations — scripts/interactive_viz.py
- FastAPI server with 10 endpoints — src/api/main.py
- Streamlit dashboard with 7 pages — src/dashboard/app.py
- 6 Jupyter notebooks (one per paper) — notebooks/
- Production Docker stack — docker-compose.production.yml
- CI/CD via GitHub Actions — .github/workflows/cicd.yml
- Stakeholder outreach plan (12 stakeholders) — STAKEHOLDER_OUTREACH.md
- Submission plan (6 papers × 6 months) — SUBMISSION_PLAN.md
- Open science strategy (Zenodo, DOI, license) — OPEN_SCIENCE.md
- Policy brief in Spanish + Guaraní — POLICY_BRIEF_es.md
- 200-angle professional roast — CRITIC_200_ANGLES.md
- 26-week master plan — MASTER_PLAN.md
- Final comprehensive report — FINAL_REPORT.md

### Changed
- Updated AGB model to Chave 2014 with realistic Chaco calibration
- Statistical findings now reflect bootstrap CIs (e.g., 3.0× disparity CI [1.7, 4.2])
- Dashboard shows ~3× disparity with confidence interval
- Indigenous disparity metric revised from "3.3×" to "~3×" with proper CI

### Tests
- 53 tests passing in 9.72s (up from 27)
- New tests: per-pixel carbon (7), cross-transfer (4), FastAPI (10), thesis structure (11)

## [Earlier commits] — 2026-07-22 to 2026-08-03

### Phase 1: Data acquisition
- Hansen GFC v1.11 download (1.2 GB, 2 tiles)
- Sentinel-2 L2A download (1.5 GB, 6 scenes)
- MapBiomas Paraguay 2023 download (38 MB)
- OpenAQ + Verra API integration

### Phase 2: Initial analysis
- Country-scale deforestation analysis (16,628 km²)
- Department-level breakdown (Alto Paraguay 28.49%)
- Indigenous territory overlap (3.0× disparity)
- NDVI time series from Hansen
- Deforestation animation GIF (23 frames)
- Real baseline models (F1=0.017 honest baseline)

### Phase 3: Improvement
- Improved U-Net with 30 channels (F1=0.017)
- Statistical significance testing (bootstrap CIs)
- 200-angle professional roast
- Master plan + 26-week calendar
- Stakeholder outreach + ethics framework
- Paper expansions to 5,000+ words each
- Thesis chapters 1-11 (~52,000 words)

### Phase 4: Production
- Streamlit dashboard
- FastAPI server
- Docker + docker-compose
- CI/CD with GitHub Actions
- 53 tests (all passing)
- Jupyter notebooks (6)
- Interactive HTML visualizations
- Statistical tests (McNemar, chi², bootstrap)

### Phase 5: Polish
- Comprehensive README
- Per-pixel carbon with Chave 2014
- Cross-paper transfer learning experiment
- Carbon credit integrity verifier
- MapBiomas temporal comparison
- 6 Jupyter notebooks
- 80+ references in bibliography
- Honest statistical reporting throughout