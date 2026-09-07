# Audit round 1 — 2026-08-28

**Auditor:** Erebus (security-auditor agent)
**Threat audited:** Scenario 1 — Compromised cron credentials (`docs/security/threat-model.md`)
**Severity:** **HIGH**
**Status:** ✅ Fixed, regression tests in place

---

## Threat audited

Scenario 1: An attacker reads `~/.hermes/cron/jobs.json` from a backup,
exfiltrates the LLM API keys, and runs up our bill.

Mitigations claimed in the threat model:

1. API keys are stored in environment vars on the cron-runner host, not in the JSON
2. Daily cost cap (`infra/cost-cap.sh`) kills runaway spend at $5/day
3. LLM provider rate limits on the API key itself

**Residual risk stated: LOW** — credential scope is single-purpose, cost cap is enforced.

---

## Finding: cost-cap.sh silently under-reports spend by summing the wrong column

### Invariant violated

> "Daily cost cap (`infra/cost-cap.sh`) kills runaway spend at $5/day." — `docs/security/threat-model.md` § Scenario 1

**The cost cap was not being enforced.** `infra/cost-cap.sh` lines 66–67
used `awk ... {sum += $5}` to aggregate the daily and monthly spend.
The CSV header is

```
date,paper_id,provider,gpu_type,duration_hr,cost_usd,status
#  $1     $2        $3       $4         $5         $6       $7
```

so `$5` is `duration_hr` (hours), not `cost_usd` (USD). The script was
summing hours and reporting them as dollars.

### Concrete impact (before fix)

| Test case | Actual cost_usd | Script reported | Script status | Reality |
|---|---|---|---|---|
| Single row, $7.50 over $5 daily cap | $7.50 | **$2.00 (40%)** | `OK` (exit 0) | Should be `OVER_DAILY` (exit 1) |
| At-cap: $5.00 over $5 daily cap | $5.00 | **$1.00 (20%)** | `OK` (exit 0) | Should be `OVER_DAILY` (exit 1) |
| 80% alert: $4.00 / $5.00 | $4.00 | **$0.80 (16%)** | `OK` (exit 0) | Should be `ALERT_DAILY` (exit 1) |
| 3 rows: $4.00 + $2.00 + $0.80 = $6.80 | $6.80 | **$2.70** (sum of 2.0+0.5+0.2 hours) | `OK` (exit 0) | Should be `OVER_DAILY` (exit 1) |

The residual risk for Scenario 1 is therefore **not LOW** — the cost
cap, the script's primary enforcement mechanism, was effectively
disabled. The "killed by the daily cap" line in the threat model was
false until this fix landed.

### Reproduction snippet (RED)

```python
# tests/test_cost_cap_enforcement.py::TestCostCapUsesCostUsdNotDurationHr
def test_over_daily_cap_is_detected(self, tmp_path):
    csv = _make_csv(tmp_path, [{
        "paper_id": "P0001", "provider": "runpod", "gpu_type": "A100",
        "duration_hr": 2.0, "cost_usd": 7.50, "status": "active",
    }])
    result = _run_cost_cap(csv)
    assert "OVER_DAILY" in result.stdout, (
        f"cost-cap.sh failed to detect $7.50 over $5 daily cap.\n"
        f"Output:\n{result.stdout}\n"
        f"This means Scenario 1's mitigation is UNMITIGATED."
    )
    assert result.returncode == 1
```

Run:

```bash
bash /opt/data/scratchpad/run_audit_tests.sh
# Before fix: 5 failed, 4 passed
# After fix:  9 passed
```

---

## Fix applied

**File:** `infra/cost-cap.sh`
**Commit-ready diff:**

```diff
-today_spend=$(awk -F, -v d="$TODAY" 'NR>1 && $1 ~ d {sum += $5} END {printf "%.2f", sum+0}' "$COST_LOG_FILE" 2>/dev/null || echo "0.00")
-month_spend=$(awk -F, -v d="$THIS_MONTH" 'NR>1 && $1 ~ d {sum += $5} END {printf "%.2f", sum+0}' "$COST_LOG_FILE" 2>/dev/null || echo "0.00")
+# Column 6 is `cost_usd` per the canonical header:
+#   date,paper_id,provider,gpu_type,duration_hr,cost_usd,status
+# Earlier versions summed $5 (duration_hr) which silently under-reported spend
+# by ~2-4x and prevented the OVER_DAILY / ALERT_DAILY thresholds from ever
+# firing. See docs/security/audit-round-1.md.
+today_spend=$(awk -F, -v d="$TODAY" 'NR>1 && $1 ~ d {sum += $6} END {printf "%.2f", sum+0}' "$COST_LOG_FILE" 2>/dev/null || echo "0.00")
+month_spend=$(awk -F, -v d="$THIS_MONTH" 'NR>1 && $1 ~ d {sum += $6} END {printf "%.2f", sum+0}' "$COST_LOG_FILE" 2>/dev/null || echo "0.00")
```

The fix changes both `today_spend` and `month_spend` aggregations to
sum column 6 (`cost_usd`). No other behavior changes. All existing
test assertions still pass.

---

## Regression test added

**New file:** `tests/test_cost_cap_enforcement.py` (9 tests)

| Test | Purpose |
|---|---|
| `test_over_daily_cap_is_detected` | $7.50 over $5 daily cap → OVER_DAILY, exit 1 |
| `test_at_daily_cap_triggers_alert` | $5.00 at $5 daily cap → OVER_DAILY (>= boundary) |
| `test_eighty_percent_triggers_alert` | $4.00 at 80% of $5 daily cap → ALERT_DAILY, exit 1 |
| `test_under_cap_does_not_alert` | $3.00 (60%) → OK, exit 0 (negative test) |
| `test_sums_correct_column_in_report_mode` | Multi-row sum is 6.80 USD, not 2.70 hours |
| `test_old_dates_excluded_from_today` | 2020-01-01 spend does not count toward today |
| `test_past_month_excluded_from_this_month` | 2026-07-15 spend does not count toward this month |
| `test_empty_log_is_ok` | Header-only CSV → OK, exit 0 |
| `test_jobs_json_does_not_contain_api_key_values` | `jobs.json` invariant for Scenario 1's mitigation #1 |

The cron-jobs test (last one) is a regression test for mitigation #1
("API keys in env vars, not the JSON"). It scans `jobs.json` for
high-entropy string values that look like leaked API keys. At the
time of this audit, only slug-style job names (e.g.
`aiw-eval-gate-runner-on-agent-run`) match the heuristic, and they
are explicitly excluded as non-credentials. If a real token ever
lands in the JSON, this test will fire.

### Existing test coverage preserved

`tests/test_reproducibility.py::TestCostCapScript` (4 tests) still
passes — script exists, is executable, runs in check mode, runs in
report mode, and passes `bash -n` syntax check.

---

## Other invariants checked (not violated)

- **Mitigation #1 (credentials in env, not JSON):** `jobs.json`
  contains 4662 lines, 36 KB. Manual scan + heuristic test confirms
  no high-entropy credential values. The keywords "secret", "token",
  "bearer", "authorization" appear only inside natural-language
  prompts and schema field names (`last_error`).
- **Cost log date filtering:** Works correctly before and after fix.
  Old dates and past-month spend do not contaminate the daily or
  monthly aggregates.
- **No `set -u` failures:** Script does not crash on missing log
  file, header-only log, or malformed rows.

---

## Status checklist

- [x] Test reproduces bug (RED confirmed, 5/9 failed)
- [x] Fix applied in `infra/cost-cap.sh` (column 5 → column 6)
- [x] Regression test added in `tests/test_cost_cap_enforcement.py` (9 tests)
- [x] All 9 new tests pass after fix
- [x] Existing 4 cost-cap tests still pass (no regression)
- [x] Threat model updated — this audit doc IS the update

---

## Severity: HIGH

**Invariant violated:** "Daily cost cap (`infra/cost-cap.sh`) kills
runaway spend at $5/day."

**Why HIGH and not CRITICAL:** No real spend event has happened
(`infra/cost_log.csv` is header-only, so production has spent $0).
The bug is silent — the script never triggered in any prior
test run because the only existing tests didn't probe the numeric
output. The blast radius is bounded by GPU provider rate limits and
the user's own $5/day VPS card cap. The window of exposure is from
the script's first deployment (Phase 1, 2026-08) until this fix
(2026-08-28). A real attacker or a misconfigured training job
during that window would have run unmitigated.

**Threat model residual risk update:** Mitigation #2 is now
operational. Residual risk for Scenario 1 returns to **LOW** as
stated, contingent on these regression tests running in CI.

---

## Next audit (round 2, scheduled 2026-09-12)

Scenario 2 — Sensitive data leak via CI artifacts. The threat model
flags a residual risk of MEDIUM with a specific missing control: "need
to add a workflow-level check that no `data/labels/` path is
referenced." The audit will write a test that asserts no GitHub
Actions workflow globs or uploads under `data/labels/` or
`data/raw/inbio/`.
