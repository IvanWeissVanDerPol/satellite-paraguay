# Thesis Autonomous Worker Schedule

**This document specifies how to wire the two autonomous workers into
cron, systemd, GitHub Actions, or any other scheduler.**

**Constraint:** All workers are agent-actionable only. They never
require human input, real money, real signatures, or external
authorization. See `AGENT_TODO.md` Tier 5 for the explicit out-of-scope
list.

---

## Worker 1: `thesis-satellite-tick`

**Purpose:** Pick the next agent-actionable task from `AGENT_TODO.md`
and emit a self-contained prompt for the LLM to execute.

**Script:** `scripts/thesis-satellite-tick.sh` (thin wrapper) →
`scripts/thesis_satellite_tick.py` (logic)

**Recommended schedule:** daily 06:00 UTC (after `thesis-active`'s
06:00 UTC tick).

**crontab entry:**
```cron
# satellite-paraguay daily tick (06:00 UTC, after substrate tick)
0 6 * * * cd /opt/data/work/satellite-paraguay && bash scripts/thesis-satellite-tick.sh script >> logs/cron.log 2>&1
```

**systemd timer (alternative):**
```ini
# /etc/systemd/system/thesis-satellite-tick.timer
[Unit]
Description=Satellite-paraguay daily thesis tick

[Timer]
OnCalendar=*-*-* 06:00:00 UTC
Persistent=true

[Install]
WantedBy=timers.target
```

**GitHub Actions (alternative, weekly only):**
```yaml
# .github/workflows/thesis-tick.yml
name: Thesis Tick (weekly)
on:
  schedule:
    - cron: '0 6 * * 1'  # Mondays 06:00 UTC
jobs:
  tick:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements-ci.txt && pip install -e . --no-deps
      - run: python scripts/thesis_satellite_tick.py --emit-prompt
```

**Output:** `/tmp/thesis_satellite_tick_prompt.md` (the prompt the
parent runner should hand to the LLM)

---

## Worker 2: `thesis-sync-watchdog`

**Purpose:** Refresh cross-repo state (validate data audit + drift
detection). Lightweight — runs every 6 hours.

**Script:** `scripts/thesis_sync_watchdog.py`

**Recommended schedule:** every 6 hours (00:00, 06:00, 12:00, 18:00 UTC).

**crontab entry:**
```cron
# satellite-paraguay cross-repo sync watchdog (every 6 hours)
0 */6 * * * cd /opt/data/work/satellite-paraguay && python3 scripts/thesis_sync_watchdog.py >> logs/cron.log 2>&1
```

**Output:**
- `outputs/data_audit.json` — always-regenerated audit of dataset claims
- `outputs/drift_note.md` — human-reviewable drift signals (never
  auto-edits STATUS.md or paper files)
- `logs/thesis_sync_watchdog.log` — append-only run log

---

## Worker integration patterns

### Pattern A: cron + separate LLM runner
This is the substrate's existing pattern. `cron` invokes the .sh
wrapper; the wrapper emits a prompt file; a separate LLM daemon
(not yet built) consumes the prompt and writes back results.

**Status:** the daemon-side consumer does not exist yet. To fully
wire up Worker 1 in this configuration, you would need to build a
small "prompt consumer" that:
1. Watches for new `/tmp/thesis_satellite_tick_prompt.md` files
2. Passes the prompt to the LLM with the right tools enabled
3. Captures the response
4. Triggers an atomic git commit if work was done

That daemon is out of scope for the agent-actionable set because it
requires Ivan to choose the LLM provider + cost envelope.

### Pattern B: GitHub Actions on push
Wire `thesis_sync_watchdog.py` into the existing CI workflow as a
post-test step. See `.github/workflows/cicd.yml` for the pattern.

**Status:** the watchdog is documented but not yet wired into CI.
A 1-line addition to the lint job would do it.

### Pattern C: Manual trigger
Ivan (or a maintainer) runs the scripts manually:

```bash
# Pick the next task + emit prompt
python3 scripts/thesis_satellite_tick.py --emit-prompt

# Refresh the data audit + drift note
python3 scripts/thesis_sync_watchdog.py
```

This is the safest pattern because every step requires a human to
actually execute it.

---

## What these workers CANNOT do

This is the explicit non-goals list. **The cron wrapper, the Python
tick, and the prompt template all enforce these as hard rules.**

1. ❌ Spend money (Vast.ai, AWS, GCP) — never calls paid APIs
2. ❌ Send emails — never invokes SMTP or any mail library
3. ❌ Submit papers — never calls journal/conference submission APIs
4. ❌ Sign or upload IRB documents
5. ❌ Defend the thesis orally
6. ❌ `git push` to GitHub — only `git commit` is allowed; push
   requires explicit `git push` invocation by Ivan
7. ❌ Modify STATUS.md, paper.md, paper.tex, *.bib
   (these are human-curated; the watchdog only writes drift_note.md)
8. ❌ Modify the git history (no force-push, no rebase)

If a worker reaches a step that requires any of the above, it must
STOP and document the blocker in `AGENT_TODO.md` under a new
"## Recent autonomous ticks (2026-09+)" section.

---

## Verification

After any worker run, these three commands MUST return 0:

```bash
cd /opt/data/work/satellite-paraguay
python3 scripts/check_claims.py        # OK -- no unsanctioned claims
python3 scripts/check_latex.py         # 6/6 papers pass
pytest tests/test_fail_loud_guard.py tests/test_validate_data.py \
       tests/test_thesis_satellite_tick.py tests/test_thesis_sync_watchdog.py \
       -q --no-cov                     # 55+ tests pass
```

The pytest suite includes 24 dedicated guard tests for the workers:
- 14 in `test_thesis_satellite_tick.py` (parser, picker, prompt emission)
- 10 in `test_thesis_sync_watchdog.py` (run, safety, drift detection, idempotency)
