#!/usr/bin/env bash
# Fast inner-loop test runner for satellite-paraguay thesis repo.
#
# Runs the 7 test files that should pass on every commit (the regression-
# protection layer from Tier-7 audit 2026-09-07 + the 2 tests that caught
# regressions in Round-8 verification 2026-09-08) PLUS the 3 always-on
# guards (check_claims.py, check_latex.py, verify_bib_dois.py --summary).
#
# Use this for inner-loop work (post-edit sanity check, ~5s).
# Use scripts/run_tests.sh for pre-commit / pre-summary verification
# (full 759-test suite, ~80s).
#
# Usage:
#   scripts/run_tests_fast.sh              # run pytest + 3 guards (default)
#   scripts/run_tests_fast.sh --no-guards  # run only pytest tests
#   scripts/run_tests_fast.sh --guards-only # run only the 3 guards
#
# Exit code: 0 on success, non-zero if any check fails.
#
# Requires: .venv to be set up via `uv sync --all-extras`
set -uo pipefail

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

PYTHON=".venv/bin/python"

# Fast test files (must stay under 10s on a normal box; the 7 listed
# cover the regression-protection layer + Round-8 fixes)
FAST_TESTS=(
    tests/test_input_references.py
    tests/test_numerical_consistency.py
    tests/test_citation_completeness.py
    tests/test_latex_check.py
    tests/test_latex_safety.py
    tests/test_bibliography.py
    tests/test_citation_patterns.py
)

run_pytest() {
    echo "→ Running fast pytest subset (7 files, ~5s)..."
    "$PYTHON" -m pytest -p no:cacheprovider --no-cov -q "${FAST_TESTS[@]}"
}

run_check_claims() {
    echo "→ check_claims.py (prose-vs-data integrity guard)..."
    "$PYTHON" scripts/check_claims.py
}

run_check_latex() {
    echo "→ check_latex.py (LaTeX syntax + bib resolve, all 6 papers)..."
    "$PYTHON" scripts/check_latex.py
}

run_verify_bib_dois_summary() {
    echo "→ verify_bib_dois.py --summary (CrossRef DOI verification summary)..."
    "$PYTHON" scripts/verify_bib_dois.py --summary
}

case "${1:-all}" in
    --no-guards)
        run_pytest
        ;;
    --guards-only)
        run_check_claims
        run_check_latex
        run_verify_bib_dois_summary
        ;;
    --help|-h)
        echo "Usage: scripts/run_tests_fast.sh [--no-guards | --guards-only]"
        echo "  default   : run pytest + 3 guards (recommended)"
        echo "  --no-guards: run only pytest tests, skip guards"
        echo "  --guards-only: run only the 3 guards, skip pytest"
        exit 0
        ;;
    all|"")
        run_pytest
        run_check_claims
        run_check_latex
        run_verify_bib_dois_summary
        ;;
    *)
        echo "Unknown argument: $1"
        echo "Run with --help for usage."
        exit 2
        ;;
esac
