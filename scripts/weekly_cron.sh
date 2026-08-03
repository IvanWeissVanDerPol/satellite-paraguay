#!/usr/bin/env bash
# Real weekly cron — runs lightweight, real-data ops
#
# This script runs every Sunday at 02:00 to:
# 1. Monitor real Paraguay data (catastro + indigenous)
# 2. Re-run statistical analysis on pilot results
# 3. Run integration test
# 4. Optionally: pull OpenAQ (if API key)
#
# Cron schedule: 0 2 * * 0 /root/satellite-paraguay/scripts/weekly_cron.sh

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

mkdir -p outputs/weekly
LOG_FILE="outputs/weekly/weekly_$(date +%Y%m%d_%H%M%S).log"

log() {
  echo "$@" | tee -a "$LOG_FILE"
}

log "=================================================="
log "Weekly cron run: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
log "=================================================="

# 1. Real conflict detection (Catastro + indigenous)
log "[1/4] Running real conflict detection..."
python3 -c "
import sys
sys.path.insert(0, '.')
from src.paraguay_admin.real_analysis import detect_conflicts_real
result = detect_conflicts_real(buffer_m=100)
print(f'Conflicts: {result[\"conflict_parcels\"]} / {result[\"total_parcels\"]}')
print(f'Conflict %: {result[\"conflict_fraction\"]*100:.2f}%')
" 2>&1 | tee -a "$LOG_FILE"

# 2. Statistical analysis on pilot
log "[2/4] Running statistical analysis..."
if [ -f "outputs/p0011/metrics.json" ]; then
  python3 scripts/analyze_pilot.py 2>&1 | tail -10 | tee -a "$LOG_FILE"
fi

# 3. Integration test
log "[3/4] Running integration test..."
python3 scripts/integration_test.py 2>&1 | tail -10 | tee -a "$LOG_FILE"

# 4. OpenAQ pull (if API key set)
if [ -n "${OPENAQ_API_KEY:-}" ]; then
  log "[4/4] Running OpenAQ pull..."
  python3 -c "
import sys
sys.path.insert(0, '.')
from src.external import fetch_openaq_asuncion
df = fetch_openaq_asuncion(days=30)
print(f'OpenAQ records: {len(df)}')
" 2>&1 | tee -a "$LOG_FILE"
else
  log "[4/4] Skipping OpenAQ (no API key)"
fi

log "=================================================="
log "Done: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
log "=================================================="
