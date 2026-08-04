#!/usr/bin/env bash
# Pre-push git hook for satellite-paraguay
# Runs tests before allowing push
# Install: ln -s ../../scripts/pre_push_hook.sh .git/hooks/pre-push

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

echo "▶ Pre-push: running test suite..."

# Skip if env var is set
if [[ "${SKIP_PRE_PUSH:-0}" == "1" ]]; then
    echo "  ⊘ Skipped (SKIP_PRE_PUSH=1)"
    exit 0
fi

# Skip on certain branches
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" == "gh-pages" || "$BRANCH" == "docs" ]]; then
    echo "  ⊘ Skipped (branch $BRANCH)"
    exit 0
fi

# Run fast tests only (skip slow, gpu, performance)
if command -v python3 >/dev/null 2>&1; then
    python3 -m pytest tests/ \
        --no-cov \
        -m "not slow and not gpu and not performance and not network" \
        -x \
        -q \
        --timeout=60 \
        2>&1 | tail -30
    EXIT_CODE=${PIPESTATUS[0]}

    if [[ $EXIT_CODE -eq 0 ]]; then
        echo "✓ Tests passed"
        exit 0
    elif [[ $EXIT_CODE -eq 5 ]]; then
        # No tests collected
        echo "⊘ No tests collected, allowing push"
        exit 0
    else
        echo "✗ Tests failed (exit $EXIT_CODE)"
        echo ""
        echo "To skip this check: SKIP_PRE_PUSH=1 git push"
        exit 1
    fi
fi

echo "⊘ python3 not available, skipping tests"
exit 0
