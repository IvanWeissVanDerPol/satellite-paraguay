# INDEX — satellite-paraguay

> **🌍 This is one half of Iván's FADA thesis. Read [`THESIS_ARCHITECTURE.md`](THESIS_ARCHITECTURE.md) first** for the cross-repo map (sustrato ↔ tesis).

Top-level files, then key subdirectories. Use `grep -r` on this file to find what you need.

## Top-level files

| Path | Size | Description |
|---|---|---|
| `AGENT_TODO.md` | 18,769 B | AGENT_TODO.md — Operational plan for the autonomous agent |
| `AUTONOMOUS_30_DAY_PLAN.md` | 6,732 B | 30-DAY AUTONOMOUS EXECUTION PLAN |
| `BRUTAL_ROAST.md` | 12,036 B | BRUTAL ROAST 2 — 2026-08-11 (autonomous self-audit) |
| `CHANGELOG.md` | 9,740 B | Changelog — SatelliteCV-Paraguay |
| `CITATION.cff` | 3,295 B |  |
| `CONTRIBUTING.md` | 3,158 B | Contributing — SatelliteCV-Paraguay |
| `CRITIC_200_ANGLES.md` | 45,620 B | 🔥 200-ANGLE PROFESSIONAL ROAST & GAP ANALYSIS |
| `CV.md` | 2,799 B | Iván Weiss Van der Pol — Curriculum Vitae |
| `Dockerfile` | 1,879 B |  |
| `Dockerfile.production` | 539 B |  |
| `EMAIL_OUTREACH.md` | 5,168 B | Email outreach — ready to send |
| `FINAL_REPORT.md` | 4,697 B | SatelliteCV-Paraguay — FINAL STATE REPORT (v2) |
| `GAP_AUDIT_2026-08-04.md` | 6,442 B | Gap Audit — satellite-paraguay (2026-08-04) |
| `LICENSE` | 1,500 B |  |
| `MASTER_PLAN.md` | 10,547 B | 🎯 MASTER AUTONOMOUS EXECUTION PLAN |
| `Makefile` | 7,579 B |  |
| `OPEN_SCIENCE.md` | 4,569 B | Open Science Plan |
| `POLICY_BRIEF_es.md` | 5,573 B | POLICY BRIEF: Monitoreo Satelital de la Deforestación en Paraguay |
| `README.md` | 13,078 B | SatelliteCV-Paraguay (Yvutu) |
| `ROAST.md` | 14,838 B | 🔥 ROAST — Honest critique of the satellite-paraguay project |
| `STAKEHOLDER_OUTREACH.md` | 6,681 B | Stakeholder Engagement Plan |
| `STATUS.md` | 8,597 B | Submission Readiness Status — 2026-08-13 (CI green-build pass) |
| `SUBMISSION_PLAN.md` | 6,072 B | Paper Submission Plan |
| `THESIS_ABSTRACT.md` | 5,656 B | Thesis Abstract — Hocht-VonDerPol (2026) |
| `THESIS_ARCHITECTURE.md` | 14,628 B | THESIS ARCHITECTURE — Cross-Repo Map |
| `THESIS_SUMMARY.md` | 1,753 B | 🛰️ SatelliteCV-Paraguay — Full Thesis Autonomous Build — Summary |
| `WORKLOG_2026-08-10.md` | 7,037 B | Worklog — 2026-08-10 (autonomous honesty pass) |
| `configs/` | dir (6 entries) | (see below) |
| `coverage.xml` | 372,138 B |  |
| `dashboard/` | dir (1 entries) | (see below) |
| `docker-compose.production.yml` | 1,388 B | (YAML config) |
| `docker-compose.yml` | 1,880 B | (YAML config) |
| `docs/` | dir (19 entries) | (see below) |
| `dvc.yaml` | 1,049 B | (YAML config) |
| `etica/` | dir (3 entries) | (see below) |
| `models/` | dir (4 entries) | (see below) |
| `notebooks/` | dir (7 entries) | (see below) |
| `papers/` | dir (3 entries) | (see below) |
| `pyproject.toml` | 6,530 B | (pyproject config) |
| `references.bib` | 42,159 B | (BibTeX references) |
| `requirements-ci.txt` | 1,290 B | (text doc) |
| `requirements.txt` | 1,043 B | (text doc) |
| `run-autonomous.sh` | 4,009 B | (Shell script) |
| `scripts/` | dir (57 entries) | (see below) |
| `src/` | dir (16 entries) | (see below) |
| `tests/` | dir (72 entries) | (see below) |
| `thesis/` | dir (18 entries) | (see below) |

## Subdirectories

### `docs/` (19 entries)

| Path | Description |
|---|---|
| `docs/12-week-roadmap-2026-Q3.md` | 12-Week Roadmap — satellite-paraguay (Yvutu thesis) |
| `docs/BUSINESS_MODEL.md` | Business Model & Monetization Strategy — SatelliteCV-Paraguay |
| `docs/CITATION.md` | Citation Guidelines |
| `docs/COMMERCIALIZATION_ROADMAP.md` | Commercialization Roadmap — Next 90 Days |
| `docs/COMPREHENSIVE_TODO.md` | ⚠️ This document is deprecated (2026-08-10). |
| `docs/CONSISTENCY_AUDIT_2026-08-13.md` | Cross-Paper Consistency Audit — 2026-08-13 |
| `docs/CONVENTIONS.md` | Conventions — SatelliteCV-Paraguay |
| `docs/DVC.md` | DVC — Data Version Control |
| `docs/FAQ.md` | FAQ — Frequently Asked Questions |
| `docs/FINAL_REPORT.md` | SatelliteCV-Paraguay — Final Integration Report |
| `docs/GLOSSARY.md` | Glossary — English / Spanish / Guaraní |
| `docs/HARDWARE.md` | Hardware Requirements |
| `docs/LAPTOP_VPS_DEPLOYMENT.md` | 🛰️ Laptop + VPS Deployment Guide |
| `docs/LATEX_COMPILE_STATUS_2026-08-13.md` | Per-paper LaTeX compile check — sandbox constraint note |
| `docs/README.md` | docs/ — SatelliteCV-Paraguay |
| `docs/REAL_TODO.md` | SatelliteCV-Paraguay — Real TODO (2026-08-10 trim) |
| `docs/STAKEHOLDERS.md` | Stakeholders & Communication Plan |
| `docs/THREATS_TO_VALIDITY.md` | Threat to Validity — Common to All 6 Papers |
| `docs/TROUBLESHOOTING.md` | Troubleshooting Guide |

### `papers/` (3 entries)

| Path | Description |
|---|---|
| `papers/drafts/` | dir (6 entries) |
| `papers/figures/` | dir (0 entries) |
| `papers/references.bib` | (BibTeX references) |

### `scripts/` (57 entries)

| Path | Description |
|---|---|
| `scripts/ablation_p0011.py` | Real ablation study for P0011 Yvutu. |
| `scripts/alert_cron_failures.py` | Alert system for cron job failures. |
| `scripts/analyze_pilot.py` | Real statistical analysis of pilot experiment. |
| `scripts/audit_dependencies.py` | Dependency audit script. |
| `scripts/bootstrap.py` | Bootstrap script — runs at start of autonomous execution. |
| `scripts/build_deforestation_animation.py` | Build animated GIF showing forest loss progression 2001-2023 in Paraguay. |
| `scripts/build_thesis_bibliography.py` | Build thesis citation graph across all 6 papers. |
| `scripts/capture_dashboard_screenshots.py` | Capture dashboard screenshots for portfolio. |
| `scripts/carbon_credit_verifier.py` | Carbon credit integrity verifier. |
| `scripts/check_claims.py` | Honest-reporting guard. |
| `scripts/check_latex.py` | AC3: per-paper LaTeX syntax + bib-resolve check. |
| `scripts/comparative_analysis.py` | Comparative analysis: Hansen vs INPE PRODES vs MapBiomas for Paraguay. |
| `scripts/crontab.txt` | (text doc) |
| `scripts/cross_transfer_experiment.py` | Cross-paper transfer learning experiment (RQ4, H3). |
| `scripts/dashboard_live_check.py` | Dashboard live deployment verification script. |
| `scripts/data_catalog.py` | Generate data catalog from paraguay-geodata + remote sources. |
| `scripts/department_deforestation.py` | Per-department deforestation analysis using real Hansen GFC + Paraguay departmen |
| `scripts/download_all_data.py` | Master data download — gets all real datasets needed for the thesis. |
| `scripts/download_sentinel2_real.py` | Real Sentinel-2 download via Microsoft Planetary Computer. |
| `scripts/evaluate_repo.py` | Real evaluation of the satellite-paraguay repo. |
| `scripts/fire_drought_analysis.py` | Fire detection (FIRMS) + Drought correlation (SPI/SPEI) analysis. |
| `scripts/generate_crontab.py` | Cron job scheduler for satellite-paraguay. |
| `scripts/generate_ndvi_from_hansen.py` | Generate NDVI/EVI time series from Hansen treecover data. |
| `scripts/generate_report.py` | Generate final report on all 6 papers. |
| `scripts/gpu/` | dir (6 entries) |
| `scripts/ground_truth_design.py` | Ground-truth validation methodology for Hansen deforestation. |
| `scripts/indigenous_overlap_analysis.py` | Indigenous territory overlap with deforestation — using Hansen data. |
| `scripts/install_git_hooks.sh` | (Shell script) |
| `scripts/integration_test.py` | End-to-end integration test for the full thesis workflow. |
| `scripts/interactive_viz.py` | Interactive visualization generator. |
| `scripts/kfold_p0035.py` | Real K-fold cross-validation for P0035 Tatakua LSTM. |
| `scripts/manage_test_data.py` | Test data versioning for satellite-paraguay. |
| `scripts/mapbiomas_temporal.py` | MapBiomas temporal comparison — synthetic 2020 vs 2023 from Hansen. |
| `scripts/merge_bib.py` | Merge thesis/references.bib + papers/references.bib into a single references.bib |
| `scripts/mutation_testing.py` | Mutation testing for satellite-paraguay using mutmut. |
| `scripts/paraguay_deforestation_analysis.py` | Paraguay-wide deforestation analysis using real Hansen GFC + MapBiomas data. |
| `scripts/per_pixel_carbon.py` | Per-pixel carbon estimation with proper Chave 2014 allometric model. |
| `scripts/pre_push_hook.sh` | (Shell script) |
| `scripts/profile_performance.py` | Performance profiling for all 6 paper pipelines. |
| `scripts/real_baselines.py` | Real baseline experiments on Hansen GFC + MapBiomas data. |
| `scripts/run_all_6_papers.py` | Run all 6 paper pipelines in sequence. |
| `scripts/run_real_experiment_p0011.py` | Real experiment using downloaded Hansen + MapBiomas data. |
| `scripts/setup_dvc.py` | DVC (Data Version Control) setup for satellite-paraguay. |
| `scripts/setup_production.py` | Production deployment script. |
| `scripts/setup_real_execution.sh` | (Shell script) |
| `scripts/statistical_tests.py` | Statistical significance tests for thesis findings. |
| `scripts/train_improved_unet.py` | Improved model training on real Hansen + MapBiomas data. |
| `scripts/train_lstm_tatakua.py` | Real LSTM training script for P0035 Tatakua (Asunción PM2.5 forecasting). |
| `scripts/train_p0011_full.py` | Real training pipeline for P0011 Yvutu (Chaco deforestation). |
| `scripts/train_prithvi_yvutu.py` | Real Prithvi fine-tuning script for P0011 Yvutu (Chaco deforestation). |
| `scripts/train_yolov8_kai.py` | Real YOLOv8 training script for P0026 Kai (wildlife poaching detection). |
| `scripts/uncertainty_quantification.py` | Uncertainty quantification for Hansen deforestation analysis. |
| `scripts/validate.py` | Validate predictions for each paper. |
| `scripts/verify.py` | Verify that everything is set up correctly. |
| `scripts/verify_reproducibility.py` | Reproducibility verifier. |
| `scripts/weekly_cron.sh` | (Shell script) |
| `scripts/weekly_run.sh` | (Shell script) |

### `src/` (16 entries)

| Path | Description |
|---|---|
| `src/__init__.py` | satellite-paraguay — Multi-temporal earth observation of Paraguay. |
| `src/api/` | dir (1 entries) |
| `src/baselines/` | dir (4 entries) |
| `src/dashboard/` | dir (2 entries) |
| `src/evaluation/` | dir (4 entries) |
| `src/external/` | dir (5 entries) |
| `src/foundation_models/` | dir (2 entries) |
| `src/logging_config.py` | Structured logging for satellite-paraguay. |
| `src/mlflow_tracking.py` | MLflow experiment tracking for satellite-paraguay. |
| `src/observability_dashboard.py` | Observability dashboard for satellite-paraguay. |
| `src/papers/` | dir (8 entries) |
| `src/paraguay_admin/` | dir (3 entries) |
| `src/parcel_analysis/` | dir (2 entries) |
| `src/satellite_io/` | dir (5 entries) |
| `src/timeseries/` | dir (2 entries) |
| `src/utils/` | dir (19 entries) |

### `tests/` (72 entries)

| Path | Description |
|---|---|
| `tests/conftest.py` | Shared pytest fixtures and configuration for satellite-paraguay tests. |
| `tests/test_api.py` | Tests for FastAPI endpoints. |
| `tests/test_api_main.py` | Tests for src/api/main.py — FastAPI endpoints. |
| `tests/test_baselines.py` | Tests for src/baselines/*.py. |
| `tests/test_baselines_p0011_extended.py` | Extended tests for src/baselines/p0011_yvytu_baselines.py. |
| `tests/test_baselines_p0035.py` | Tests for src/baselines/p0035_tatakua_baselines.py — air quality |
| `tests/test_baselines_p0100.py` | Tests for src/baselines/p0100_yvyra_baselines.py — regression baselines |
| `tests/test_baselines_p0100_extended.py` | Tests for src/baselines/p0100_yvyra_baselines.py — run_all_baselines. |
| `tests/test_bibliography.py` | Tests for src/utils/bibliography.py. |
| `tests/test_bootstrap.py` | Tests for src/utils/bootstrap.py. |
| `tests/test_carbon_math.py` | Tests for src/utils/carbon_math.py. |
| `tests/test_cross_transfer.py` | Tests for cross-paper transfer learning. |
| `tests/test_dashboard_app.py` | Tests for src/dashboard/app.py — Streamlit dashboard. |
| `tests/test_dashboard_app_final.py` | Final coverage tests for src/dashboard/app.py. |
| `tests/test_dashboard_deploy.py` | AC4: Dashboard live deployment verification. |
| `tests/test_dashboard_pages.py` | Tests for src/dashboard/app.py page functions. |
| `tests/test_dashboard_pages_extended.py` | Extended dashboard tests — all remaining pages. |
| `tests/test_deploy_templates.py` | Tests for src/utils/deploy_templates.py. |
| `tests/test_evaluation.py` | Tests for src.evaluation module. |
| `tests/test_evaluation_metrics_extended.py` | Tests for src/evaluation/metrics.py — additional coverage. |
| `tests/test_evaluation_statistics.py` | Tests for src/evaluation/statistics.py. |
| `tests/test_external_firms.py` | Tests for src/external/firms_client.py. |
| `tests/test_external_openaq.py` | Tests for src/external/openaq_client.py. |
| `tests/test_external_s5p.py` | Tests for src/external/sentinel5p_client.py. |
| `tests/test_external_verra.py` | Tests for src/external/verra_client.py. |
| `tests/test_fail_loud_guard.py` | Fail-loud guard tests for the 2026-08-11 pass (BRUTAL_ROAST fix). |
| `tests/test_foundation_models.py` | Tests for src/foundation_models/models.py. |
| `tests/test_foundation_models_extended.py` | Extended tests for src/foundation_models/models.py. |
| `tests/test_hansen_gee.py` | Tests for src/satellite_io/hansen.py — GEE download path. |
| `tests/test_integration.py` | Integration tests exercising the public API surface. |
| `tests/test_latex_check.py` | AC3: LaTeX syntax + bib-resolve check for all 6 papers. |
| `tests/test_logging_config.py` | Tests for src/logging_config.py. |
| `tests/test_mapbiomas_gee.py` | Tests for src/satellite_io/mapbiomas.py — GEE download path. |
| `tests/test_mlflow_tracking.py` | Tests for src/mlflow_tracking.py. |
| `tests/test_observability_dashboard.py` | Tests for src/observability_dashboard.py — Observability dashboard. |
| `tests/test_observability_main.py` | Tests for src/observability_dashboard.py main() function. |
| `tests/test_openaq_client_extended.py` | Extended tests for src/external/openaq_client.py. |
| `tests/test_paper_demos.py` | Tests for paper pipeline demo functions — p0025, p0026, p0035, p0100. |
| `tests/test_paper_validators.py` | Tests for src/utils/paper_validators.py. |
| `tests/test_papers_p0011.py` | Tests for src/papers/p0011_yvytu_deforestation/pipeline.py. |
| `tests/test_papers_p0011_extended.py` | Tests for src/papers/p0011_yvytu_deforestation/pipeline.py |
| `tests/test_papers_p0012.py` | Tests for src/papers/p0012_yvy_indigenous/pipeline.py. |
| `tests/test_papers_p0012_vlm.py` | Tests for src/papers/p0012_yvy_indigenous/pipeline.py VLM paths. |
| `tests/test_papers_p0025.py` | Tests for src/papers/p0025_yrupe_yield/pipeline.py. |
| `tests/test_papers_p0026.py` | Tests for src/papers/p0026_kai_poaching/pipeline.py. |
| `tests/test_papers_p0035.py` | Tests for src/papers/p0035_tatakua_air_quality/pipeline.py. |
| `tests/test_papers_p0100.py` | Tests for src/papers/p0100_yvyra_carbon_credits/pipeline.py. |
| `tests/test_paraguay_admin.py` | Tests for src.paraguay_admin module. |
| `tests/test_paraguay_admin_loader.py` | Tests for src/paraguay_admin/loader.py. |
| `tests/test_paraguay_admin_real_analysis.py` | Tests for src/paraguay_admin/real_analysis.py. |
| `tests/test_paraguay_admin_real_analysis_extended.py` | Extended tests for src/paraguay_admin/real_analysis.py. |
| `tests/test_parcel_analysis_intersect.py` | Tests for src/parcel_analysis/intersect.py. |
| `tests/test_per_pixel_carbon.py` | Tests for Chave 2014 AGB model. |
| `tests/test_performance.py` | Performance benchmark suite for satellite-paraguay. |
| `tests/test_pipelines.py` | Tests for src.papers pipelines. |
| `tests/test_properties.py` | Property-based tests for satellite-paraguay using hypothesis. |
| `tests/test_property_based.py` | Property-based tests using hypothesis. |
| `tests/test_real_download.py` | Tests for src/satellite_io/real_download.py. |
| `tests/test_real_download_gee.py` | Tests for src/satellite_io/real_download.py GEE paths. |
| `tests/test_satellite_io_hansen.py` | Tests for src/satellite_io/hansen.py. |
| `tests/test_satellite_io_mapbiomas.py` | Tests for src/satellite_io/mapbiomas.py. |
| `tests/test_satellite_io_sources.py` | Tests for src/satellite_io/sources.py — multi-source satellite data API. |
| `tests/test_scripts_statistical.py` | Tests for scripts/statistical_tests.py — actual script tests. |
| `tests/test_sentinel5p_extended.py` | Extended tests for src/external/sentinel5p_client.py. |
| `tests/test_stat_uncertainty.py` | Tests for src/utils/stat_analysis.py and src/utils/uncertainty.py. |
| `tests/test_test_data.py` | Tests for src/utils/test_data.py. |
| `tests/test_thesis_structure.py` | Tests for thesis chapters and references. |
| `tests/test_timeseries_analysis.py` | Tests for src/timeseries/analysis.py. |
| `tests/test_utils_mlflow.py` | Tests for src/utils/mlflow_tracking.py. |
| `tests/test_utils_more.py` | Tests for src/utils/reproducibility_verify, repo_evaluator, repo_verify. |
| `tests/test_utils_refactored.py` | Tests for src/utils/cron_monitor.py, dependency_audit.py, crontab_gen.py, |
| `tests/test_utils_reproducibility.py` | Tests for src/utils/reproducibility.py — coverage target: 100%. |

### `thesis/` (18 entries)

| Path | Description |
|---|---|
| `thesis/CH10_discussion.md` | Chapter 10: Discussion |
| `thesis/CH11_conclusion.md` | Chapter 11: Conclusion |
| `thesis/CH1_introduction.md` | Chapter 1: Introduction |
| `thesis/CH2_methodology.md` | Chapter 2: Methodology |
| `thesis/CH3_paper1_P0011_yvutu.md` | P0011 Yvutu: Multi-Temporal Satellite Computer Vision for Chaco Deforestation |
| `thesis/CH4_paper2_P0010_yvyra.md` | P0010 Yvyra: Carbon-Credit Integrity Verification in Paraguay via Verra vs Hanse |
| `thesis/CH5_paper3_P0012_yvy.md` | P0012 Yvy: Indigenous Land Tenure and Deforestation in the Paraguayan Chaco |
| `thesis/CH6_paper4_P0025_yrupe.md` | P0025 Yrupe: Cross-Domain Transfer Learning for Soybean Yield — Honest Failure-M |
| `thesis/CH7_paper5_P0026_kai.md` | P0026 Kai: Synthetic-to-Real Gap in Wildlife Detection in the Gran Chaco |
| `thesis/CH8_paper6_P0035_tatakua.md` | P0035 Tatakua: PM₂.₅ Forecasting in Paraguay via Multi-Source LSTM |
| `thesis/CH9_cross-cutting.md` | Chapter 9: Cross-Cutting Analysis |
| `thesis/INDEX.md` | Thesis Index — Markdown Snapshot |
| `thesis/MAIN/` | dir (1 entries) |
| `thesis/chapters/` | dir (6 entries) |
| `thesis/citation_graph.json` | (JSON data) |
| `thesis/main.tex` | (LaTeX source) |
| `thesis/preamble.tex` | (LaTeX source) |
| `thesis/references.bib` | (BibTeX references) |

### `etica/` (3 entries)

| Path | Description |
|---|---|
| `etica/FPIC_template_es.md` | PROTOCOLO DE CONSENTIMIENTO LIBRE, PREVIO E INFORMADO (CLPI) |
| `etica/IRB_protocol_paraguay_UNA.md` | IRB Protocol — Universidad Nacional de Asunción (UNA) |
| `etica/UNA_IRB_SUBMISSION_PACKAGE.md` | UNA FADA Ethics Committee — Submission Package |

### `configs/` (6 entries)

| Path | Description |
|---|---|
| `configs/p0010_yvyra.yaml` | (YAML config) |
| `configs/p0011_yvytu.yaml` | (YAML config) |
| `configs/p0012_yvy.yaml` | (YAML config) |
| `configs/p0025_yrupe.yaml` | (YAML config) |
| `configs/p0026_kai.yaml` | (YAML config) |
| `configs/p0035_tatakua.yaml` | (YAML config) |

### `notebooks/` (7 entries)

| Path | Description |
|---|---|
| `notebooks/P0010_yvyra_carbon.ipynb` |  |
| `notebooks/P0011_yvutu_deforestation.ipynb` |  |
| `notebooks/P0012_yvy_indigenous.ipynb` |  |
| `notebooks/P0025_yrupe_yield.ipynb` |  |
| `notebooks/P0026_kai_wildlife.ipynb` |  |
| `notebooks/P0035_tatakua_air.ipynb` |  |
| `notebooks/eda_paraguay_geodata.ipynb` |  |

### `dashboard/` (1 entries)

| Path | Description |
|---|---|
| `dashboard/app.py` | Streamlit dashboard for SatelliteCV-Paraguay mega-project. |

### `models/` (4 entries)

| Path | Description |
|---|---|
| `models/cards/` | dir (7 entries) |
| `models/checkpoints/` | dir (0 entries) |
| `models/fine_tuned/` | dir (0 entries) |
| `models/lstm_tatakua/` | dir (2 entries) |

## Important subdirs NOT indexed above (too many files)

- `data/` — datasets (Hansen, Sentinel-2, etc.). See `data/DATA_ACQUISITION.md`.
- `models/` — trained model checkpoints. See `models/README.md` (if present).
- `outputs/` — generated figures, tables, predictions. See `outputs/README.md` (if present).
- `logs/` — runtime logs (cron output, training logs).

---

Generated by Hermes agent (cross-repo architecture review), 2026-08-15.
Total tracked files: 750 (see `git ls-files`).

---

## 🔗 See also

- **Other half of the thesis (data substrate):** [`IvanWeissVanDerPol/paraguay-geodata-vlm`](https://github.com/IvanWeissVanDerPol/paraguay-geodata-vlm) — OSM/IGN/Sentinel download, SAM/GroundingDINO pipeline, autonomous cron, web app demo.
- **Cross-repo architecture map:** [`THESIS_ARCHITECTURE.md`](THESIS_ARCHITECTURE.md) — read this first.
