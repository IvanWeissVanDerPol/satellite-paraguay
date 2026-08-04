#!/usr/bin/env bash
# Install git hooks for satellite-paraguay
# Run once after cloning the repo: bash scripts/install_git_hooks.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "Installing git hooks..."

# Pre-push hook
if [[ -f "$REPO_ROOT/scripts/pre_push_hook.sh" ]]; then
    cp "$REPO_ROOT/scripts/pre_push_hook.sh" "$HOOKS_DIR/pre-push"
    chmod +x "$HOOKS_DIR/pre-push"
    echo "  ✓ Installed pre-push hook (runs tests)"
else
    echo "  ⚠ scripts/pre_push_hook.sh not found"
fi

# Pre-commit hook (delegates to pre-commit framework if installed)
cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/usr/bin/env bash
# Run pre-commit framework if available
if command -v pre-commit >/dev/null 2>&1; then
    pre-commit run --files $(git diff --cached --name-only --diff-filter=ACM)
    exit $?
else
    exit 0
fi
EOF
chmod +x "$HOOKS_DIR/pre-commit"
echo "  ✓ Installed pre-commit hook"

# Commit-msg hook for conventional commits
cat > "$HOOKS_DIR/commit-msg" << 'EOF'
#!/usr/bin/env bash
# Enforce conventional commit format
COMMIT_MSG=$(cat "$1")
PATTERN='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert|research)(\(.+\))?: .+'

if ! [[ "$COMMIT_MSG" =~ $PATTERN ]]; then
    echo "⚠ Commit message does not follow Conventional Commits format"
    echo "  Expected: <type>(<scope>): <description>"
    echo "  Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert, research"
    echo ""
    echo "  Examples:"
    echo "    feat: add MapBiomas temporal analysis"
    echo "    fix(api): handle empty department list"
    echo "    research: complete thesis chapters 1-2"
    echo ""
    echo "  Your message: $COMMIT_MSG"
    echo ""
    echo "  To bypass: git commit --no-verify"
    # Don't fail, just warn (uncomment to enforce)
    # exit 1
fi
EOF
chmod +x "$HOOKS_DIR/commit-msg"
echo "  ✓ Installed commit-msg hook (conventional commits)"

echo ""
echo "All hooks installed. To skip pre-push: SKIP_PRE_PUSH=1 git push"
