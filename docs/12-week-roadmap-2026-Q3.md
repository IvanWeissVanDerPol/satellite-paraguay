# 12-Week Roadmap — satellite-paraguay (Yvutu thesis)

> **🌍 Cross-repo note:** This roadmap covers the **thesis-paper side** (6 papers, models, manuscript). The data substrate + autonomous cron runner (`paraguay-geodata-vlm`) runs in parallel via `thesis-daily-tick` at 06:00 UTC. **Read [`THESIS_ARCHITECTURE.md`](../THESIS_ARCHITECTURE.md) first** for the cross-repo map.

**Generated:** 2026-08-15
**Operator:** Hermes agent (autonomous, under Iván's "do all" grant)
**Current state (verified 2026-08-15):**
- main @ `fe24ca1d` (squash-merged PR #24 → CI green)
- 1006 pytest pass / 38 skip / 0 fail (was 997; +9 new bootstrap tests)
- flake8 0 / black 0 / isort 0 / mypy 0
- 6 of 6 LaTeX papers compile (`scripts/check_latex.py` green)
- `check_claims.py` clean (no unsanctioned headlines)
- CODEOWNERS, Dependabot, SBOM, gitleaks, release-drafter, vulture-nightly, codacy/sonarcloud configs all in
- Tier 0 + Tier 1 + Tier 2.5 + Tier 3 (CI hardening) all done

## Goal (12 weeks out — defense submission window)

Ship the **thesis manuscript** as 6 publishable papers + integration manuscript:

- **P0010 Vyrá carbon credits** → submission-ready for Verra-aligned journal
- **P0011 Yvutu deforestation** → submission-ready after Prithvi real fine-tune
- **P0012 Yvy indigenous** → submission-blocked on FPIC partnership; submit when unblocked
- **P0025 Yrupe yield** → submission-blocked on INBIO data; submit when unblocked
- **P0026 Kai poaching** → submission-ready after real Paraguay-labeled wildlife data
- **P0035 Tatakua air quality** → submission-ready for Atmospheric Environment
- **Thesis integration manuscript** (CH1-CH11) → submitted as monograph candidate to FPUNA / external press

**Concrete end-state:** All 6 papers have measured scores on real held-out data. Thesis integration is ~85% complete (CH1-CH11 fully written; defense prep pending). Honest-reporting checks pass at all times. Zero fabricated results.

---

## Phase 0 — Unblock (Week 1)

**Goal:** Get the project out of its current "ethics-blocked + GPU-blocked" state so Phase 2 can start.

### Human-owned (Iván)

| Task | Time | Steps | Verification |
|---|---|---|---|
| Sign 6 institutional partnership letters (Guyra Paraguay, INBIO, INDI, Verra, FPUNA ethics committee, OpenAQ attribution) | 4 h | Draft → legal review → send | Letters on file in `docs/partnerships/` |
| Confirm $200 GPU budget via VPS billing (Linode/Hetzner/RunPod quote comparison) | 1 h | Pick provider, set up billing | `docs/infra/gpu-decision.md` committed |
| Schedule first FPIC engagement call with INDI representative | 0.5 h | Email → calendar invite | Calendar event with notes |

### Agent-owned

| Task | Time | Verification |
|---|---|---|
| Write `docs/infra/gpu-decision.md` (3-provider comparison table, $X/HR rate, queue strategy) | 30 min | File committed, links from README |
| Write `docs/partnerships/TEMPLATE-FPIC.md` (free, prior, informed consent script for indigenous data use) | 1 h | Template reviewed by you |
| Add `infra/cost-cap.sh` — daily spend cap of $5 on GPU rentals, alerts at 80% | 30 min | `bash infra/cost-cap.sh` exits 0, dry-run safe |
| Add `scripts/check_ethics.py` — gates every paper's status with the required partnership/FPIC/IRB evidence; exits 1 if any "Model trained ≥50" paper has "Ethics ≤30" without a doc/partnership note | 1 h | `python3 scripts/check_ethics.py` runs in CI `lint` job |
| Wire `scripts/check_ethics.py` into `.github/workflows/cicd.yml` lint step | 10 min | CI run shows the check passing/failing |

---

## Phase 1 — Pilot-readiness (parallel with Phase 0, Week 1)

### Agent-owned, no human gate

| Task | Time | Verification |
|---|---|---|
| Write `docs/security/threat-model.md` (what data leaks, what adversarial scenarios, what mitigations) | 2 h | File committed, cited from README |
| Write `docs/operations/RUNBOOK.md` (per-paper reproduce-from-data recipe with exact GPU commands) | 3 h | 6 papers each have a copy-paste recipe |
| Write `tests/test_reproducibility.py` — smoke test that each paper's main script can run end-to-end on synthetic data and produce deterministic output | 4 h | `pytest tests/test_reproducibility.py -v` passes 6/6 |
| Add `scripts/drift-detector.sh` — daily cron compares measured scores in `STATUS.md` vs `BRUTAL_ROAST.md`; alerts if any paper's reported metric drifts by >10% | 1 h | Cron job added; first run output clean |
| Run vulture nightly, gitleaks, Dependabot auto-merge once each and confirm they all hit green | 30 min | All 4 monitoring jobs show "ok" in their first 7-day run |

---

## Phase 2 — Feature build (the meat, Weeks 2-10)

Sequenced by **safety → privacy → infra-light → infra-heavy**.

### Week 2: Real-data acquisition for the 3 ethics-blocked papers

| Feature | Effort | Paper | Why first | Privacy/safety invariant | TDD plan |
|---|---|---|---|---|---|
| P0025 INBIO data download script | S (1 day) | P0025 | Unblocks 16 h of GPU training in Week 3 | n/a (data is agricultural census, public post-partnership) | red: `tests/test_yrupe_data_loader.py::test_loads_real_labels` fails on real fixture; green: downloader pulls 10K rows from INBIO API and CSV lands in `data/raw/inbio/yrupe_2024.csv`; refactor: dry-run mode, retry-on-429 |
| P0026 Real Paraguay wildlife labels | M (1 week) | P0026 | Unblocks 30/100→70/100 model score | Wildlife data ethics: partner attribution, no GPS for endangered species | red: `tests/test_kai_dataset.py::test_real_guyra_labels_count`; green: 200+ labeled images via Guyra API + manual label-verification; refactor: label noise audit |
| P0011 Sentinel-2 tile acquisition | S (2 days) | P0011 | Unblocks Prithvi fine-tune in Week 4 | n/a (data is public Sentinel-2) | red: `tests/test_yvutu_s2_loader.py::test_30_tiles_loaded`; green: `scripts/download_s2_paraguay.py` produces 30 .tif in `data/raw/sentinel2/`; refactor: rate-limit + checksum |

### Week 3: GPU training (Iván pays, agent orchestrates)

| Feature | Effort | Paper | Why this order | Privacy/safety invariant | TDD plan |
|---|---|---|---|---|---|
| P0025 GRU training on real INBIO data | M (3 days) | P0025 | Cheap model, validates GPU pipeline first | n/a | red: `tests/test_yrupe_gru.py::test_converges_on_real`; green: train.py produces yrupe_gru_v2.pt with measured F1>0.5 on held-out; refactor: W&B run logged |
| P0011 Prithvi fine-tune on real Hansen | M (3 days) | P0011 | The headline result (16,628 km² measurement) | n/a | red: `tests/test_prithvi_finetune.py::test_unet_f1_on_held_out`; green: train_prithvi_yvutu.py produces prithvi_yvutu_v2.pt with F1>0.5 on held-out Hansen; refactor: log metrics to MLflow |
| P0026 YOLOv8 retrain on real labels | M (3 days) | P0026 | Synthetic-to-real gap 0.50→0.18, retrain should close it | wildlife GPS strip | red: `tests/test_kai_yolo.py::test_real_gap_lt_synthetic_gap`; green: train_kai_yolo.py produces kai_yolo_v2.pt with real-data F1>0.3; refactor: augmentation audit |

### Week 4-5: P0010 + P0035 polish (already strong)

| Feature | Effort | Paper | Why this order | Privacy/safety invariant | TDD plan |
|---|---|---|---|---|---|
| P0035 LSTM refinement on 24 more stations | S (3 days) | P0035 | Quick win, single-author paper | OpenAQ public attribution | red: `tests/test_tatakua_lstm_v2.py::test_rmse_below_15`; green: train_tatakua_lstm_v2.py → RMSE 14.7→<14; refactor: per-station variance breakdown in paper |
| P0010 AlphaEarth fine-tune | M (1 week) | P0010 | Strong existing baseline, validates literature benchmark | n/a | red: `tests/test_alphaearth.py::test_improves_over_baseline`; green: train_alphaearth.py produces alphaearth_v2.pt with R²>0.4; refactor: confusion matrix + per-region breakdown |
| P0011 country-scale deforestation re-measurement | S (2 days) | P0011 | Headline number, refresh after model upgrade | n/a | red: `tests/test_yvutu_country_total.py::test_within_5pct`; green: re-run with new model, update RESULTS section; refactor: paper Section 4 with new figure |

### Week 6: Privacy/safety infrastructure (mandatory before thesis integration)

| Feature | Effort | Why this order | Privacy/safety invariant | TDD plan |
|---|---|---|---|---|
| Per-paper access logging | M (1 week) | Required before thesis integration exposes any data | Records every read of sensitive data with user/timestamp/reason | red: `tests/test_audit_log.py::test_read_writes_audit_row`; green: every `read_*()` function in `src/satellite_io/`, `src/paraguay_admin/`, `src/external/` calls `audit_log()`; refactor: audit queryable from admin API |
| Rate limiting on external API clients | S (2 days) | Hardening before thesis load tests | n/a | red: `tests/test_rate_limit.py::test_blocks_after_10_calls`; green: token-bucket per-API-key in `src/external/*`; refactor: env-tunable rates |
| Encryption-at-rest for sensitive labels | S (3 days) | INBIO + Guyra labels are sensitive | AES-256-GCM at rest, AES key in env var | red: `tests/test_encryption.py::test_decrypt_round_trip`; green: every write to `data/labels/` is encrypted; refactor: key rotation script |

### Week 7-9: Thesis integration manuscript

| Feature | Effort | Why this order | Privacy/safety invariant | TDD plan |
|---|---|---|---|---|
| CH1 Introduction full | S (2 days) | Foundation for all other chapters | n/a | red: `tests/test_thesis_ch1.py::test_no_inflation`; green: 6000-word CH1 in `thesis/MAIN/chapters/01-introduction.tex`; refactor: cross-references to all 6 papers |
| CH2 Methodology full | M (3 days) | Reader needs this before any Results chapter | n/a | red: `tests/test_ch2_coverage.py::test_all_6_methods_listed`; green: 8000-word CH2 covering all 6 paper methods; refactor: figure list |
| CH3-CH8 per-paper results chapters (6 chapters) | M each (3 days × 6 = 18 days) | Meat of thesis | Each chapter must cite measured scores only | red: `tests/test_chapter_X.py::test_no_inflated_numbers`; green: each chapter is 8000 words with measured F1/R²/MAE; refactor: shared figure macros |
| CH9 Cross-cutting findings | M (3 days) | What emerges from comparing 6 papers | n/a | red: `tests/test_ch9_novelty.py::test_5_cross_findings`; green: 5000-word CH9 with 5+ cross-cutting insights; refactor: cited from each chapter |
| CH10 Discussion | M (3 days) | Future work + limitations | Must include ethics/FPIC/IRB gaps explicitly | red: `tests/test_ch10_ethics.py::test_lists_ethics_gaps`; green: 5000-word CH10 with explicit gaps; refactor: defense-talking-points appendix |
| CH11 Conclusion | S (2 days) | Final synthesis | n/a | red: `tests/test_ch11.py::test_no_new_claims`; green: 3000-word CH11 that ONLY summarizes what's in CH1-CH10; refactor: ensure no new numbers introduced |

### Week 10: Defense prep

| Feature | Effort | Why this order | Privacy/safety invariant | TDD plan |
|---|---|---|---|---|
| Defense slides (45 slides, 30 min) | M (3 days) | Time-bound: defense date | n/a | red: `tests/test_slides.py::test_45_slides`; green: `thesis/DEFENSE/slides.pdf` exists; refactor: speaker notes |
| Q&A prep document (50 likely questions + answers) | S (2 days) | Same | n/a | red: `tests/test_qa.py::test_50_questions`; green: `thesis/DEFENSE/qa.md`; refactor: link to relevant paper sections |
| Mock defense with thesis-tracker cron | S (1 day) | Practice run | n/a | red: n/a; green: cron fires `ai-thesis-defense-mock` and produces feedback; refactor: feedback goes into qa.md |

### Week 11: Final integration + submission prep

| Feature | Effort | Why this order | Privacy/safety invariant | TDD plan |
|---|---|---|---|---|
| Submit 4 ready papers to journals (P0010, P0011, P0026, P0035) | M (3 days, mostly coordination) | These are publishable as-is | n/a (journals have own review) | red: n/a; green: submission emails + cover letters filed; refactor: tracking doc |
| Update Zenodo deposit with current versions | S (1 day) | Citable version of thesis | n/a | red: n/a; green: 6 DOIs minted; refactor: CITATION.cff |
| Final defense rehearsal | S (1 day) | Same | n/a | red: n/a; green: 30-min talk recorded + reviewed; refactor: timing per slide |

### Week 12: Buffer + post-defense backlog

| Task | Time | Notes |
|---|---|---|
| Apply any reviewer feedback from submitted papers (1-2 rounds of revisions expected) | 5 days | Async |
| Update STATUS.md to reflect post-defense state | 1 h | Routine |
| Onboard the next thesis cohort (handoff doc) | 2 days | Optional |

---

## Phase 3 — Continuous (every week, ongoing)

### Weekly cadence (Tuesdays)

| Cadence | Time | Owner | Action |
|---|---|---|---|
| 09:00 — Feedback triage | 30 min | management-coordinator cron | New issues/PRs labeled and assigned |
| 14:00 — Backlog grooming | 1 h | research-tracker cron | Stale items re-prioritized; `[!]` blockers escalated |
| 17:00 — Perf regression check | 30 min | engineering-roster cron | pytest-benchmark diff vs last week; alerts on >10% regression |

### Biweekly cadence

| Cadence | Time | Owner | Action |
|---|---|---|---|
| Day 1, 14 — Privacy/security audit | 2 h | compliance-monitor cron | Adversarial review per skill pattern (RED-test → confirm bug → fix → no regression). Output: `docs/security/audit-round-N.md` |
| Day 7, 21 — Dependency review | 1 h | devops-monitor cron | Dependabot PRs reviewed; non-trivial updates batched to a weekly "deps" PR |
| Day 14 — Cost-cap review | 30 min | finance-controller cron | Weekly spend vs budget; alert at 80% of monthly cap |

### Per-session

| Cadence | Owner | Action |
|---|---|---|
| Per autonomous session | (current agent) | Append to SESSION-LOG.md with: session ID, duration, files touched, decisions made, next steps |
| Per milestone | research-tracker cron | Append to CHANGELOG.md with: milestone name, papers affected, measured deltas |
| Per push to main | CI | Run all 12 CI jobs; block on any failure |

---

## Phase 4 — Post-pilot (Week 12+)

Grouped by category, not in priority order:

### Research follow-ups
- P0012 resubmit after FPIC partnership lands
- P0025 resubmit after INBIO partnership lands
- New paper: cross-paper carbon-yield-air-quality tradeoff analysis (3-paper combo)
- New paper: open-source Prithvi fine-tune pipeline (reproducibility paper)

### Infra
- Move from Cloudflare Pages + Supabase to in-house hosting (decision needed)
- Add Kubernetes manifests for GPU training (replace runbook shell scripts)
- Self-host MLflow (replace hosted W&B)

### Operational
- Hire first FTE: ethics & partnerships officer (the FPIC gap)
- Spin up ParaguAI lead-pipeline as a separate business unit
- Apply for FPUNA grant to extend dataset (P0011 Sentinel-2 full country)

### Documentation
- Translate thesis to Spanish (Spanish is the primary language per CLAUDE.md — currently the manuscript is in English for international submission; a Spanish translation is a separate deliverable for FPUNA's institutional repository)

---

## Risks + Open Decisions

### High-risk
- **FPIC partnership takes 2-6 months of human time** (P0012). Mitigation: start in Week 1 (Phase 0) so by Week 12 the relationship is at least warmed.
- **GPU budget overrun.** Mitigation: `infra/cost-cap.sh` hard-caps at $5/day; alert at 80%.
- **INBIO partnership denial.** Mitigation: alternative is synthetic data with explicit "no real-data" framing — P0025's existing 100% paper-text status is preserved.

### Medium-risk
- **Prithvi fine-tune doesn't converge.** Mitigation: the existing U-Net honest baseline (F1=0.017) is a fallback; the paper text already supports that result.
- **Real wildlife labels cost more than expected.** Mitigation: cap at 500 images; document the cap as a limitation.
- **Reviewer rejection on P0035.** Mitigation: Atmospheric Environment is the target journal, with 3-week revision cycles; budget 2-3 weeks for revisions in Week 12 buffer.

### Decisions pending Iván
- **Thesis submission journal**: monograph press (e.g., Springer thesis series) vs. arXiv-only vs. institutional repository only? Decision by Week 4.
- **Spanish translation scope**: full vs. summary? Decision by Week 8.
- **GPU provider final pick**: Linode vs. Hetzner vs. RunPod. Decision by Week 1.

### Honest assessment of what's actually hard
1. **FPIC and partnerships** — these are not engineering problems, they are trust problems with institutions. The agent can write emails and templates, but Ivan must lead.
2. **GPU training convergence** — Prithvi fine-tuning on 30 Sentinel-2 tiles may not converge with enough data; the U-Net baseline (F1=0.017) is what you can defend if it doesn't.
3. **Thesis integration** — the 6 papers are independent; CH9 (cross-cutting) requires genuine synthesis, not just restating each chapter.

---

## Command-level checklist (Week 1, Phase 0 + Phase 1)

Copy-paste in order. Assumes `cd /opt/data/work/satellite-paraguay`.

```bash
# --- Phase 0: agent-owned ---

# 1. GPU decision doc
mkdir -p docs/infra
# (you write the comparison table; agent fills the markdown)

# 2. FPIC template
mkdir -p docs/partnerships
# (you write the script; agent formats)

# 3. Cost cap
mkdir -p infra
cat > infra/cost-cap.sh <<'EOF'
#!/bin/bash
# Daily spend cap; alerts at 80% of $5/day
# Run from cron daily at 23:00 PYT
# ...
EOF
chmod +x infra/cost-cap.sh
bash infra/cost-cap.sh  # dry-run

# 4. Ethics check
cat > scripts/check_ethics.py <<'EOF'
#!/usr/bin/env python3
"""Gate every paper's status with the required partnership/FPIC/IRB evidence."""
# Reads STATUS.md, BRUTAL_ROAST.md, checks each paper's Ethics axis >= Model axis
# or has explicit partnership note in docs/partnerships/
# ...
EOF
python3 scripts/check_ethics.py

# 5. Wire into CI
# Edit .github/workflows/cicd.yml to add `python3 scripts/check_ethics.py` to the Lint job

# --- Phase 1: agent-owned ---

# 6. Threat model
mkdir -p docs/security
# (write threat-model.md per skill template)

# 7. Runbook
mkdir -p docs/operations
# (write RUNBOOK.md per paper)

# 8. Reproducibility tests
# Add tests/test_reproducibility.py
pytest tests/test_reproducibility.py -v

# 9. Drift detector
cat > scripts/drift-detector.sh <<'EOF'
#!/bin/bash
# Compare STATUS.md scores vs BRUTAL_ROAST.md; alert if drift > 10%
# ...
EOF
chmod +x scripts/drift-detector.sh
bash scripts/drift-detector.sh  # dry-run

# 10. Verify monitoring jobs
hermes cron list | grep -E "vulture|gitleaks|dependabot|release-drafter"
# All should show "active"
```

---

## Definition of done

Concrete, falsifiable. By end of Week 12:

- [ ] `python3 scripts/check_ethics.py` exits 0 (all papers have required partnership/FPIC/IRB evidence)
- [ ] `python3 scripts/check_claims.py` exits 0 (no unsanctioned headlines)
- [ ] `python3 scripts/check_latex.py` exits 0 (6/6 papers compile)
- [ ] `pytest tests/ -q --no-cov` reports 1006+ passed, 0 failed
- [ ] `mypy --explicit-package-bases scripts/ src/` reports 0 errors
- [ ] `flake8 src/ tests/ scripts/` reports 0 violations
- [ ] 4 of 6 papers submitted (P0010, P0011, P0026, P0035); 2 (P0012, P0025) marked as "blocked on partnership" in `STATUS.md`
- [ ] `thesis/MAIN/thesis.tex` compiles with CH1-CH11 all present
- [ ] `thesis/DEFENSE/slides.pdf` exists, 45 slides, 30-minute talk
- [ ] `thesis/DEFENSE/qa.md` exists with 50 questions
- [ ] Zenodo deposit minted, 6 DOIs in `CITATION.cff`
- [ ] GPU spend ≤ $5/day average over the 12 weeks
- [ ] Zero fabricated results in any paper or chapter
- [ ] Privacy/security audit round-6 (biweekly cadence × 6 rounds) shows no HIGH findings

### What is NOT promised

- **Publication acceptance.** Submission ≠ acceptance. Reviewer revisions are expected and may add 4-12 weeks.
- **Spanish translation.** Out of scope this 12 weeks; deferred to Phase 4.
- **P0012 / P0025 publication.** These are gated on FPIC/INBIO partnerships, which are human-owned, not agent-owned. We will do everything we can in parallel; we don't promise partner sign-off.
- **Defense.** This roadmap gets the manuscript + slides + Q&A ready. The defense date itself is set by FPUNA's committee, not by this roadmap.
- **All 6 papers at 100% submission-ready.** We aim for it; we promise it for 4 of 6.

---

## Open questions before Week 1 starts

1. **GPU provider pick** — Linode, Hetzner, or RunPod? (Decision by Week 1)
2. **Thesis journal/monograph venue** — Springer thesis series, arXiv, or FPUNA institutional? (Decision by Week 4)
3. **Spanish translation scope** — full or summary? (Decision by Week 8)
4. **FPIC partnership lead** — Iván direct contact, or through an FPUNA faculty intermediary? (Decision by Week 1)

---

**Generated by:** Hermes agent (roadmap-planning skill)
**References:** `STATUS.md`, `AGENT_TODO.md`, `BRUTAL_ROAST.md`, `docs/CONVENTIONS.md`
**Status:** PLAN WRITTEN, NOT EXECUTED. Awaiting Iván's "go" before any Phase 0 work begins.
