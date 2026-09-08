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

# Set up venv if missing (local dev only — CI runner uses pip install)
if [[ ! -x ".venv/bin/python" ]] && [[ "${SKIP_UV_FALLBACK:-0}" != "1" ]]; then
  if command -v uv >/dev/null 2>&1; then
    echo "→ .venv missing; running 'uv sync --all-extras'..."
    uv sync --all-extras
  else
    echo "→ .venv missing AND no 'uv' binary; assuming CI runner with pip-installed deps."
    echo "   Set SKIP_UV_FALLBACK=1 to suppress this fallback entirely."
  fi
fi

# Detect the Python interpreter to use (CI vs local dev):
# - Local dev: .venv/bin/python (from `uv sync --all-extras`)
# - CI runner: system Python (no .venv; pip-installed deps land in site-packages)
# CI runners signal with GITHUB_ACTIONS=true (and/or CI=true on some providers).
if [[ -x ".venv/bin/python" ]] && [[ -z "${GITHUB_ACTIONS:-}" ]] && [[ -z "${CI:-}" ]]; then
    PYTEST=".venv/bin/python -m pytest"
else
    PYTEST="${PYTHON:-python3} -m pytest"
fi

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
