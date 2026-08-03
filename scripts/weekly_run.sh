#!/usr/bin/env bash
# Run all 6 papers weekly via cron
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
echo "Running weekly all-6-papers at $(date)"
python3 scripts/run_all_6_papers.py >> logs/weekly_run.log 2>&1
echo "Done at $(date)"
