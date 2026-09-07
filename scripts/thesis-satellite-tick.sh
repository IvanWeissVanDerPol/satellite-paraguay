#!/usr/bin/env bash
# thesis-satellite-tick.sh — Cron entry point for satellite-paraguay daily tick.
#
# Picks the next [ ] or [P#] task from AGENT_TODO.md and tries to make
# progress on it. Self-contained — cron runs it in a fresh session, so
# the prompt must include everything the agent needs.
#
# Schedule: daily 06:00 UTC (after thesis-active's 06:00 tick).
#
# Tier: Tier 3 from AGENT_TODO.md (autonomous multi-session work).
# Constraint: only picks agent-actionable items (no [EXT], no [🤝], no [⚠️]).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# Activate venv if present
if [[ -f ".venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# 1. Run the data validator first — if anything critical is missing, the
#    agent prompt gets the audit context appended.
.venv/bin/python scripts/validate_data.py --quiet > /tmp/thesis_data_audit.txt 2>&1 || true

# 2. Run the agent tick. The prompt is self-contained: project state + next
#    task from AGENT_TODO.md + guard instructions. No chat context required.
cat > /tmp/thesis_satellite_tick_prompt.md <<'PROMPT_EOF'
You are running an autonomous tick on the satellite-paraguay thesis repo.

Working directory: /opt/data/work/satellite-paraguay

Your job: pick the next agent-actionable item from AGENT_TODO.md and make
genuine progress on it (not just describe what you would do).

Rules (NON-NEGOTIABLE):
1. ONLY pick items that are NOT marked [EXT], [🤝], or [⚠️]. Items
   requiring real money (Vast.ai), real signatures (IRB), or external
   action (email, submission, partnership) are out of scope.
2. You may ONLY do work that does not require Ivan's input or authorization.
3. After every change, run `make check-claims` (or
   `python3 scripts/check_claims.py && python3 scripts/check_ethics.py &&
   python3 scripts/check_latex.py`) to verify the honest-reporting guards
   stay green.
4. Run `pytest tests/test_fail_loud_guard.py tests/test_validate_data.py
   tests/test_reproducibility.py -q --no-cov` and confirm 0 failures.
5. Atomic commits with conventional commit messages (feat:, fix:, docs:,
   test:, chore:). Never push to GitHub.
6. Append a one-paragraph summary to /opt/data/work/satellite-paraguay/AGENT_TODO.md
   under a new "## Recent autonomous ticks (2026-09+)" section.

Priority order (pick the highest-priority [ ] item):
- 🔴 critical (blocks submission)
- 🟡 high value (blocks defense)
- 🟢 polish (nice-to-have)

If AGENT_TODO.md is empty / all [ ] are [x] / all remaining are
[EXT]/[🤝]/[⚠️]: do nothing, exit 0, log a "no agent-actionable items
remaining" message.

Data audit context (from validate_data.py):
PROMPT_EOF

cat /tmp/thesis_data_audit.txt >> /tmp/thesis_satellite_tick_prompt.md

# 3. Execute the agent tick. For cron-style execution, we run the agent
#    in --no-agent mode (script-only) by writing a small Python helper
#    that reads AGENT_TODO.md, picks the top agent-actionable item, and
#    emits the prompt to stdout for the parent cron runner to consume.
#    If --live flag is passed, the agent runs in full LLM mode.

MODE="${1:-script}"

if [[ "$MODE" == "script" ]]; then
    .venv/bin/python scripts/thesis_satellite_tick.py --emit-prompt \
        --audit-file /tmp/thesis_data_audit.txt \
        --output-file /tmp/thesis_satellite_tick_prompt.md
elif [[ "$MODE" == "live" ]]; then
    # Live mode requires the hermes agent CLI; not currently available
    # in the sandbox. Cron jobs should use --mode=script only.
    echo "Live mode not available in this sandbox; use --mode=script" >&2
    exit 2
fi

# 4. Append to the activity log so cron-debugging can see what ran
mkdir -p logs
echo "[$TS] thesis-satellite-tick.sh mode=$MODE data_audit=$(cat /tmp/thesis_data_audit.txt)" \
    >> logs/thesis_satellite_tick.log
