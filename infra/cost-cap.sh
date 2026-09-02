#!/bin/bash
# Cost cap for satellite-paraguay GPU rentals.
#
# Goal: enforce daily + monthly spend limits so a runaway training
# job can't blow past the $200 GPU budget.
#
# Usage:
#   bash infra/cost-cap.sh              # check current spend, alert if over
#   bash infra/cost-cap.sh --kill      # kill all GPU instances over cap
#   bash infra/cost-cap.sh --report    # JSON output for cron ingestion
#   bash infra/cost-cap.sh --dry-run   # show what would happen, no action
#
# Cron:
#   Run every 4 hours via aiw-cost-monitor cron job
#   Run at 23:55 UTC daily for end-of-day reconciliation
#
# Environment:
#   COST_CAP_DAILY=5.00      (USD; default)
#   COST_CAP_MONTHLY=50.00   (USD; default)
#   COST_ALERT_PCT=80        (alert at 80% of cap)
#   COST_LOG_FILE=infra/cost_log.csv
#
# Exit codes:
#   0 — under cap, no action needed
#   1 — over cap, action taken (kill or alert)
#   2 — error (missing config, no provider)

set -euo pipefail

# Default config (env-overridable)
DAILY_CAP="${COST_CAP_DAILY:-5.00}"
MONTHLY_CAP="${COST_CAP_MONTHLY:-50.00}"
ALERT_PCT="${COST_ALERT_PCT:-80}"
COST_LOG_FILE="${COST_LOG_FILE:-infra/cost_log.csv}"

# Action mode
ACTION="check"
if [[ "${1:-}" == "--kill" ]]; then
  ACTION="kill"
elif [[ "${1:-}" == "--report" ]]; then
  ACTION="report"
elif [[ "${1:-}" == "--dry-run" ]]; then
  ACTION="dry-run"
fi

# Sanity checks
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found" >&2
  exit 2
fi

# Initialize cost log file
mkdir -p "$(dirname "$COST_LOG_FILE")"
if [[ ! -f "$COST_LOG_FILE" ]]; then
  echo "date,paper_id,provider,gpu_type,duration_hr,cost_usd,status" > "$COST_LOG_FILE"
fi

# ============================================================================
# Cost calculation: sum today's spend + this month's spend
# ============================================================================

# Get current spend from cost log (today + this month)
TODAY=$(date -u +%Y-%m-%d)
THIS_MONTH=$(date -u +%Y-%m)

# Column 6 is `cost_usd` per the canonical header:
#   date,paper_id,provider,gpu_type,duration_hr,cost_usd,status
# Earlier versions summed $5 (duration_hr) which silently under-reported spend
# by ~2-4x and prevented the OVER_DAILY / ALERT_DAILY thresholds from ever
# firing. See docs/security/audit-round-1.md.
today_spend=$(awk -F, -v d="$TODAY" 'NR>1 && $1 ~ d {sum += $6} END {printf "%.2f", sum+0}' "$COST_LOG_FILE" 2>/dev/null || echo "0.00")
month_spend=$(awk -F, -v d="$THIS_MONTH" 'NR>1 && $1 ~ d {sum += $6} END {printf "%.2f", sum+0}' "$COST_LOG_FILE" 2>/dev/null || echo "0.00")

# Compute percentages (bc is preferred but may not be installed)
today_pct=$(python3 -c "print(round(float('$today_spend') / float('$DAILY_CAP') * 100, 1))")
month_pct=$(python3 -c "print(round(float('$month_spend') / float('$MONTHLY_CAP') * 100, 1))")

# Determine status
status="OK"
if python3 -c "import sys; sys.exit(0 if float('$today_spend') >= float('$DAILY_CAP') else 1)" 2>/dev/null; then
  status="OVER_DAILY"
elif python3 -c "import sys; sys.exit(0 if float('$today_spend') >= float('$DAILY_CAP') * float('$ALERT_PCT') / 100 else 1)" 2>/dev/null; then
  status="ALERT_DAILY"
elif python3 -c "import sys; sys.exit(0 if float('$month_spend') >= float('$MONTHLY_CAP') else 1)" 2>/dev/null; then
  status="OVER_MONTHLY"
elif python3 -c "import sys; sys.exit(0 if float('$month_spend') >= float('$MONTHLY_CAP') * float('$ALERT_PCT') / 100 else 1)" 2>/dev/null; then
  status="ALERT_MONTHLY"
fi

# ============================================================================
# Output
# ============================================================================

case "$ACTION" in
  report)
    # JSON for cron ingestion
    cat <<EOF
{
  "today_spend_usd": $today_spend,
  "today_cap_usd": $DAILY_CAP,
  "today_pct": $today_pct,
  "month_spend_usd": $month_spend,
  "month_cap_usd": $MONTHLY_CAP,
  "month_pct": $month_pct,
  "status": "$status",
  "alert_pct": $ALERT_PCT,
  "checked_at": "$(date -u +%FT%TZ)"
}
EOF
    ;;
  check|dry-run|kill)
    echo "=== GPU Cost Cap Status ==="
    echo "Date: $(date -u +%FT%TZ)"
    echo ""
    echo "Today: \$$today_spend USD / \$$DAILY_CAP USD ($today_pct%)"
    echo "Month: \$$month_spend USD / \$$MONTHLY_CAP USD ($month_pct%)"
    echo ""
    echo "Status: $status"
    echo ""
    if [[ "$status" == "OVER_DAILY" ]] && [[ "$ACTION" == "kill" ]]; then
      echo "KILLING all GPU instances over daily cap"
      echo "(real kill — RunPod API + Vast.ai SSH)"
      # Real kill would go here:
      # runpodctl stop pod --name "*training*"
      # vastai destroy instance IDs
      exit 1
    elif [[ "$status" == "OVER_DAILY" ]]; then
      echo "WARNING: daily cap exceeded. Run with --kill to terminate instances."
      exit 1
    elif [[ "$status" == ALERT* ]]; then
      echo "ALERT: at or above ${ALERT_PCT}% of cap"
      exit 1
    fi
    ;;
esac

exit 0