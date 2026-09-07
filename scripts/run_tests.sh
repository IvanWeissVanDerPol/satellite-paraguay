#!/usr/bin/env bash
# Test runner for satellite-paraguay thesis repo.
#
# Usage:
#   scripts/run_tests.sh            # Fast mode: skip coverage, ~30s
#   scripts/run_tests.sh --full     # Full mode: with coverage report
#   scripts/run_tests.sh <pattern>  # Run tests matching pattern (e.g. test_bib)
#
# Requires: .venv to be set up via `uv sync --all-extras`
# If .venv is missing, the script will try to create it.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Set up venv if missing
if [[ ! -x ".venv/bin/python" ]]; then
  echo "→ .venv missing; running 'uv sync --all-extras'..."
  uv sync --all-extras
fi

PYTEST=".venv/bin/python -m pytest"

# Mode selection
if [[ "${1:-}" == "--full" ]]; then
  echo "→ Running full test suite WITH coverage..."
  exec $PYTEST tests/ "${@:2}"
elif [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  echo "Usage: scripts/run_tests.sh [pattern] [--full]"
  echo "  no args  : fast mode, all tests, no coverage"
  echo "  pattern  : run only tests matching pattern (e.g. test_bib)"
  echo "  --full   : with coverage report"
  exit 0
elif [[ -n "${1:-}" ]]; then
  echo "→ Running filtered tests: $@"
  exec $PYTEST -p no:cacheprovider --no-cov -x -q -k "$@"
else
  echo "→ Running fast test suite (no coverage)..."
  exec $PYTEST -p no:cacheprovider --no-cov -q tests/
fi
