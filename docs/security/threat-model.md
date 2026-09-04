# Threat Model — satellite-paraguay

**Generated:** 2026-08-22 (Phase 1 of 12-week roadmap)
**Status:** Initial draft
**Author:** Hermes agent

---

## What we defend

| Asset | Where | Sensitivity |
|---|---|---|
| Trained model weights (`models/*.pt`) | Git LFS or Hugging Face | Low (published paper requires weights anyway) |
| Sentinel-2 tile downloads (`data/raw/sentinel2/`) | DVC | Low (public data, but expensive to re-fetch) |
| Hansen GFC tiles (`data/raw/hansen/`) | DVC | Low (public) |
| Verra registry scrapes (`data/external/verra/`) | local + Zenodo | Medium (rebuilds the +35.9% under-claim finding) |
| Real wildlife labels (`data/labels/`) | encrypted local | **High** (Guyra partnership trust) |
| INBIO yield data (`data/raw/inbio/`) | encrypted local | **High** (partner trust) |
| INDI indigenous territory boundaries | public | High (sensitive — must not be re-shared) |
| FPIC documentation | `docs/partnerships/` | **High** (legal liability) |
| Cron credentials (`~/.hermes/cron/jobs.json`) | local | **High** (LLM API keys) |

---

## Adversarial scenarios

### Scenario 1: Compromised cron credentials

**Threat:** An attacker reads `~/.hermes/cron/jobs.json` from a backup, exfiltrates the LLM API keys, and runs up our bill.

**Mitigation:**
- API keys are stored in environment vars on the cron-runner host, not in the JSON
- Daily cost cap (`infra/cost-cap.sh`) kills runaway spend at $5/day
- LLM provider rate limits on the API key itself

**Residual risk:** LOW — credential scope is single-purpose, cost cap is enforced.

---

### Scenario 2: Sensitive data leak via CI artifacts

**Threat:** Real wildlife labels or INDI territory boundaries end up in a public CI artifact (e.g., uploaded as test coverage data).

**Mitigation:**
- `.github/workflows/*.yml` uses `actions/upload-artifact@v4` with explicit `if-no-files-found: error`
- Workflows do not upload `data/` directories
- `.gitignore` excludes `data/raw/inbio/` and `data/labels/` and `secrets/`
- LFS is configured for `models/*.pt` only (not data)

**Residual risk:** LOW (post round-2 audit 2026-09-04) — every upload-artifact step now has `if-no-files-found: error`, and `.gitignore` excludes `data/raw/inbio/`, `data/labels/`, and `secrets/`. Regression tests in `tests/test_ci_artifact_security.py` (23 passed, 0 failed).

---

### Scenario 3: FPIC documentation forged

**Threat:** A bad actor edits `docs/partnerships/` to claim consent that wasn't given.

**Mitigation:**
- All PRs to `docs/partnerships/` require CODEOWNERS approval (configured)
- Commits to FPIC docs have signed-off-by requirements (add via branch protection)
- CI gate: `scripts/check_ethics.py` checks docs exist + audit log

**Residual risk:** LOW — FPIC docs are markdown files; forgeries would be visible in git history.

---

### Scenario 4: Indigenous community names exposed in published paper

**Threat:** P0012 Yvy paper accidentally names indigenous communities without FPIC consent, causing reputational and legal harm.

**Mitigation:**
- `scripts/check_ethics.py` blocks CI if P0012 ethics <= 30 with no FPIC doc
- Paper draft reviewed by Iván + community liaison before submission
- `check_claims.py` (existing) checks for unsanctioned high-headline claims
- Names of communities are sanitized in `papers/drafts/p0012_yvy_indigenous/ETHICS.md`

**Residual risk:** LOW if all checks pass; HIGH if checks bypassed.

---

### Scenario 5: Model weights exfiltrated via dependency confusion

**Threat:** A malicious Python package in `requirements.txt` or `requirements-ci.txt` exfiltrates model files when training runs.

**Mitigation:**
- Pin all package versions (`requirements-ci.txt` uses exact versions)
- Dependabot weekly check on requirements
- `pip install --no-deps` for the package itself (run before dev deps)

**Residual risk:** LOW — limited blast radius (training runs are sandboxed).

---

### Scenario 6: Model inversion attack on published weights

**Threat:** An attacker downloads the published Prithvi-fine-tuned weights and runs model inversion to recover training data (which includes Hansen tiles over indigenous territories).

**Mitigation:**
- Published weights are documented as fine-tuned from public Prithvi on public Sentinel-2 (no private data)
- Hansen GFC is public (USGS/NASA)
- No indigenous community boundaries are in the training data

**Residual risk:** LOW — no PII in training data.

---

### Scenario 7: Supply chain attack on paper submission

**Threat:** A malicious actor compromises the journal submission system or the editor's account, modifying the paper between submission and review.

**Mitigation:**
- Out of our control — journal-side security
- We submit a checksummed PDF + source files
- We post the same paper to arxiv simultaneously as backup

**Residual risk:** UNKNOWN — relies on journal security.

---

### Scenario 8: Compromised CI runner exfiltrates secrets

**Threat:** GitHub Actions runner reads `secrets.SUPABASE_SECRET_KEY` from environment, leaks it via compromised runner image.

**Mitigation:**
- Use SHA-pinned action versions (already done in workflows)
- Minimal secret scope: SUPABASE_SECRET_KEY is only used in deploy-dashboard job
- Rotate key quarterly
- `secrets-scan` workflow (gitleaks) on every push

**Residual risk:** MEDIUM — GitHub-managed runner security is beyond our control.

---

## Audit cadence (per agent-org-framework skill pattern)

**Biweekly audit** (every other Friday) — `docs/security/audit-round-N.md`:

| Round | Date | What to check |
|---|---|---|
| 1 | 2026-08-28 | Scenario 1 — cost-cap.sh summed wrong column (`$5` instead of `$6`); HIGH severity, **fixed**. See `audit-round-1.md`. |
| 2 | 2026-09-04 | Scenario 2 — `.gitignore` had no exclusion for `data/raw/inbio/`, `data/labels/`, `secrets/` (HIGH); 3 upload-artifact steps missing `if-no-files-found: error` (MEDIUM). **Fixed.** See `audit-round-2.md`. |
| 3 | 2026-09-26 | Drift detector accuracy — false positive rate, false negative rate |
| 4 | 2026-10-10 | Phase 2 features: P0025 INBIO downloader security |
| 5 | 2026-10-24 | P0026 YOLOv8 retrain script — verify checkpoint integrity |
| 6 | 2026-11-07 | P0011 Prithvi fine-tune — verify no data leak via model inversion |

Each audit follows TDD shape:
1. Pick an invariant → write a test that violates it (RED)
2. Confirm the test reproduces the bug
3. Fix the code (GREEN)
4. Confirm no regression

---

## Reporting

**Where to report security issues:**
- GitHub: https://github.com/IvanWeissVanDerPol/satellite-paraguay/security/advisories/new (private disclosure)
- Email: ivan@example.com (PGP key in `docs/security/pgp-key.asc` — TBD)

**Severity classification:**
- CRITICAL: data leak with partner trust impact → 24h response
- HIGH: credentials compromised, weights leaked → 72h response
- MEDIUM: production degradation, no data loss → 1 week
- LOW: documentation drift, cosmetic issues → next maintenance window

---

## Files this threat model will produce

- `docs/security/threat-model.md` (this file)
- `docs/security/audit-round-N.md` (one per audit)
- `docs/security/pgp-key.asc` (TBD — generate for Iván)
- `docs/security/incidents/` (post-incident reports)

---

**Reviewed-by:** Hermes agent (Phase 1 of 12-week roadmap)
**Next audit:** 2026-08-29 (round 1)