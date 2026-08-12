# AGENT_TODO.md — Operational plan for the autonomous agent

**Generated:** 2026-08-11
**Operator:** Hermes agent
**Authority:** User-granted "do \all" on 2026-08-10 + 2026-08-11
**Refresh cadence:** mark items `[x]` when done; bump priorities every session.

**Legend:**
- 🔴 = critical / blocks submission
- 🟡 = high value / blocks defense
- 🟢 = polish / nice-to-have
- ⏱ = estimated autonomous session time
- 🤝 = needs user (FPIC, money, partnership email, signature)
- ⚠️ = destructive (needs explicit per-call consent: `rm`, force-push, drop, etc.)

---

## Tier 1 — PR #1 from previous session landed (done)

- [x] 6 abstracts rewritten with measured values (commit 65621c4)
- [x] 6 paper.md honest-reporting notes appended (commit 65621c4)
- [x] 3 paper.tex files patched (commit 65621c4)
- [x] LICENSE CC-BY-NC-4.0 added
- [x] CITATION.cff + .zenodo.json added
- [x] references.bib unified 180 entries, 5 conflicts resolved (commit 88e337e)
- [x] scripts/merge_bib.py + scripts/check_claims.py added
- [x] CONTRIBUTING.md + docs/CONVENTIONS.md added
- [x] thesis/MAIN/thesis.tex + 3 chapter files patched (commit 88e337e)
- [x] MASTER_PLAN.md "shipped" list rewritten (commit 88e337e)
- [x] src/api/main.py ModelMetric corrected (commit 88e337e)
- [x] PR #1 opened: https://github.com/IvanWeissVanDerPol/satellite-paraguay/pull/1
- [x] BRUTAL_ROAST.md + STATUS.md + AGENT_TODO.md (this file) drafted

---

## Tier 2 — Single-session autonomous wins (next 2-4 sessions)

### 🔴 A. Random.rand() stub elimination — FAIL-LOUD, not silent
- ⏱ 6-10 h
- Files: 9 in `src/` + reproduce in scripts/integration_test.py
- Approach:
  1. Add `from typing import Optional` + an explicit `data: Optional[str] = None` arg to each baseline that takes data path.
  2. When data path is None or path doesn't exist → `raise FileNotFoundError(f"...{expected_path}")` with a clear message + remediation hint ("run `make data-sentinel2` first").
  3. For `mlflow_tracking.py` + `reproducibility.py`: replace random-fill with zeros + a `warnings.warn(...)` explaining the missing field.
  4. Add `pytest` test per file: `with pytest.raises(FileNotFoundError): pipeline.run(...)`.
- Output: `src/baselines/*` no longer produces random numbers silently. **PR-ready.**

### 🔴 B. Rewrite README.md — kill the "Ship-ready" lie
- ⏱ 2 h
- Lead with honest status: "Pilot-stage thesis substrate, ~25% submission-ready, see `STATUS.md`."
- Replace `**Status:** Ship-ready. Pilot validation. All data real, all tests passing.` with the scorecard from STATUS.md.
- Move the per-paper headline findings table down to a "What we measured so far" section.
- Keep the diagram of repo structure.
- Add the badges: `[![CI](https://github.com/IvanWeissVanDerPol/satellite-paraguay/actions/workflows/cicd.yml/badge.svg)]` etc.

### 🔴 C. Add `scripts/check_claims.py` to CI
- ⏱ 30 min
- Open `.github/workflows/cicd.yml`, add a step: `python3 scripts/check_claims.py` after the test step.
- Fails the build if anyone re-introduces a fabricated headline.

### 🔴 D. Fill in the 30 TODO template sections
- ⏱ 30-60 h across multiple sessions
- Per paper, write the Methods/Results/Discussion/Conclusion/Related_Work sections using the ACTUAL_RESULTS.md as the data source.
- Priority order:
  - **P0035 Tatakua first** — only paper with measured model, easiest to publish
  - **P0012 Yvy second** — has the strongest finding (indigenous disparity, +35.9%) and the social-good story is unique
  - **P0010 Yvyra third** — solid Verra data, single +35.9% finding
  - **P0011 Yvutu fourth** — core paper but blocked on real Prithvi run
  - **P0026 Kai fifth** — needs more data
  - **P0025 Yrupe last** — currently a failure-mode analysis, can frame as lessons-learned
- Target: each paper 6,000+ words.

### 🟡 E. Add unit tests for paper pipelines
- ⏱ 12 h
- For each `src/papers/*/pipeline.py`, add 3-5 tests:
  - `test_pipeline_loads_real_data_if_available` (skip if data missing)
  - `test_pipeline_fails_loud_if_data_missing`
  - `test_pipeline_outputs_match_schema` (validate output JSON shape)
- Increases coverage from 39.8% to an estimated 55-65%.

### 🟡 F. CI badge + repo polish
- ⏱ 1 h
- Add README badges (CI status, Zenodo DOI placeholder, CC-BY-NC-4.0)
- Confirm `.github/workflows/cicd.yml` works on `pip install -r requirements.txt`
- Add this file to `docs/`

### 🟢 G. Add GH topics
- ⏱ 5 min (API call)
- ⚠ needs user OK first because it changes repo discoverability permanently
- Topics: `deforestation`, `paraguay`, `remote-sensing`, `prithvi`, `carbon-credits`, `indigenous-data-sovereignty`, `open-science`

### 🟢 H. Dashboard verification
- ⏱ 4 h
- Spin up the dashboard (`streamlit run dashboard/app.py`) + verify each of 7 pages renders
- Spin up the API (`uvicorn src.api.main:app`) + curl every endpoint
- Capture new screenshots into `outputs/screenshots/`
- Fix any breakage from the `src/api/main.py` honesty edits (pass 2 changed f1=0.85 → 0.497)

### 🟢 I. Updated `outputs/REPO_EVALUATION.md`
- ⏱ 1 h
- Re-run `scripts/evaluate_repo.py` after pass-2
- The current version says "4 test files" — that's clearly outdated

### 🟢 J. `coverage.xml` → `.gitignore`
- ⏱ 5 min
- It's 350KB in the repo; should be a CI artifact, not a tracked file
- ⚠ destructive (`git rm --cached`) — file history retains a record

---

## Tier 3 — Multi-session autonomous work (1-2 months)

### 🔴 K. Run Vast.ai training for P0011 Prithvi (real model)
- ⏱ Setup 4 h + queue 12-24 h on A100 80GB
- Pre-req: 🤝 user OK + Vast.ai account + ~$20 budget
- Tasks:
  1. Set up GEE auth (`ee.Authenticate()`), generate service-account JSON
  2. Download 150 real Paraguay Chaco tiles via Planetary Computer STAC API (no auth needed)
  3. Spin up Vast.ai A100 (or H100 if cheaper), clone repo, install deps
  4. Run `scripts/train_prithvi_remote.py --tiles 150 --epochs 30 --gpu`
  5. Save best.pt to `models/checkpoints/p0011_prithvi_best.pt`, push back
  6. Re-evaluate on held-out test set
  7. Update `papers/drafts/p0011_yvutu_deforestation/ACTUAL_RESULTS.md`
  8. Rewrite `papers/drafts/p0011_yvutu_deforestation/paper.md` results section
- Replaces F1=0.497 mock with a real measured number

### 🔴 L. Run Vast.ai training for P0025 INBIO model
- ⏱ Setup 4 h + queue 8-12 h on A100
- Same as K but smaller. Multi-task CNN with real INBIO yield labels.
- Blocked by user unless INBIO partnership exists.

### 🔴 M. Run Vast.ai training for P0026 YOLOv8 (real labeled wildlife)
- ⏱ Setup 6 h (label creation) + queue 12 h on A100
- Even with no partnership, you can train on the 5,000 Guyra public images
- Should reach mAP@0.5 in the 0.3-0.5 range on real (vs current 0.18)

### 🟡 N. Expand `reproducibility.py`
- ⏱ 6 h
- Capture git SHA, CUDA version, GPU model, `pip freeze`, OS info as part of every model run
- Plug into `mlflow_tracking.py`
- Tests for the captured environment

### 🟡 O. Per-paper risk-of-validity section
- ⏱ 8 h
- `docs/THREATS_TO_VALIDITY.md` exists but is generic
- Add per-paper threats (e.g., P0012: "All 10 territories are in the Chaco — not representative of eastern Paraguay"; P0035: "12 stations under-represent rural air quality")

### 🟡 P. Data ingestion validation script
- ⏱ 8 h
- `scripts/validate_data.py`: check every dataset the repo claims (Hansen, Sentinel-2, MapBiomas, Verra, OpenAQ, FIRMS, S5P) and report actual byte count, expected byte count, missing fields.
- Output: `outputs/data_audit.json` + stdout summary

### 🟡 Q. Re-run all baselines with mock-elimination
- ⏱ 8 h
- After Tier 2.A (random.rand → fail-loud), re-run `scripts/real_baselines.py` to confirm all numbers in ACTUAL_RESULTS.md are stable

### 🟢 R. Pre-commit + CI hygiene
- ⏱ 4 h
- `.pre-commit-config.yaml` exists, but the hooks haven't been wired
- Add: black, isort, flake8, check_claims, merge_bib
- This way a PR can't introduce fabricated numbers OR untested code

### 🟢 S. Index/contents page in thesis
- ⏱ 2 h
- LaTeX `\tableofcontents`, list of figures, list of tables, list of acronyms — generate with pandoc

### 🟢 T. BibTeX per-paper bibliography files
- ⏱ 4 h
- Today we have one big `references.bib` at repo root
- For LaTeX compile, need per-paper `references.bib` files in `papers/drafts/*/` that contain only the cited keys

### 🟢 U. Sphinx / mkdocs docs site
- ⏱ 16 h
- Convert the markdown docs to a hosted static site
- Hook into GitHub Pages
- API auto-docs from FastAPI

### 🟢 V. Clean up `scripts/`
- ⏱ 6 h
- 33+ scripts; many overlap (multiple "analyze_pilot" style)
- Merge into a single `scripts/<tool_name>.py` per concept
- Document each in `scripts/README.md`

---

## Tier 4 — Needs human, agent supports (🤝 = user/partner does)

### 🤝 W. FPIC engagement with 10 indigenous communities (P0012)
- 🤝 100% human; 6-12 months
- Agent supports: draft email + Spanish/Guaraní template per `etica/FPIC_template_es.md`, prepare 1-page community-friendly atlas when ready

### 🤝 X. UNA IRB submission
- 🤝 100% human; 2-4 months
- Agent supports: prepare IRB_protocol_paraguay_UNA.md into formal UNA format, fill out forms

### 🤝 Y. INFONA / INDI / SENEPA / Verra / Guyra / WWF / INBIO partnership letters
- 🤝 100% human; 3-6 months
- Agent supports: draft partnership MOUs per `STAKEHOLDER_OUTREACH.md`, prepare per-partner one-pagers

### 🤝 Z. Submit papers to journals
- 🤝 100% human; user submits through their account
- Agent supports: final paper.md → paper.tex conversion, validation against journal template, submission checklist filled out

### 🤝 AA. Thesis defense
- 🤝 100% human
- Agent supports: 30-slide deck per paper + cross-cutting, mock-defense Q&A generation

---

## Tier 5 — Explicitly out of scope for agent

- Training any model on **real Paraguay satellite imagery** without user OK (Vast.ai cost)
- Sending **any email** to indigenous communities, INDI, INFONA, Verra, etc.
- **Submitting** to any journal under the author's name
- **Signing** IRB / partnership documents
- **Defending** the thesis orally
- Any action marked `⚠️ destructive` without explicit per-call consent

---

## Daily operational rhythm

For each new session, the agent should:

1. Check `STATUS.md` for any updates
2. Pick the highest-priority 🔴 item from this TODO
3. Do it. Verify with a command. Commit. Report.
4. If blocked: document the block in `STATUS.md` and surface to the user.

---

## Definition of "done"

When this TODO is complete, the project will:
- ✅ Have 6 papers, each ≥6,000 words, with measured model + held-out test
- ✅ Have IRB + FPIC + partnership letters on file
- ✅ Have the agent produce a release v0.2 with Zenodo DOI
- ✅ Pass 80% line coverage + `pytest -q` green
- ✅ Have a thesis document ≥50,000 words ready for defense
- ✅ Have zero random.rand in production code
- ✅ Have `check_claims.py` green and integrated in CI

The 🟢 polish items can be punted past defense without harm.

---

**Total estimated agent work to "done": ~700 hours over 8-12 weeks.**
**Total estimated human work to "done": ~200-700 hours (relationships).**

These can run partially in parallel after the core paper-writing + real-model-training are unblocked.
