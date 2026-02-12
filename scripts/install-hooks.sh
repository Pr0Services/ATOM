#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# AT·OM — Install Git Security Hooks
# ═══════════════════════════════════════════════════════════════════════════
# Run this after cloning the repo to install security hooks
# Usage: bash scripts/install-hooks.sh
# ═══════════════════════════════════════════════════════════════════════════

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -z "$REPO_ROOT" ]; then
    echo "❌ Not in a git repository"
    exit 1
fi

HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "═══════════════════════════════════════════════════════════════"
echo "  AT·OM — Installing Security Hooks"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Copy pre-commit hook
if [ -f "$REPO_ROOT/scripts/pre-commit-hook.sh" ]; then
    cp "$REPO_ROOT/scripts/pre-commit-hook.sh" "$HOOKS_DIR/pre-commit"
    chmod +x "$HOOKS_DIR/pre-commit"
    echo "✅ Pre-commit hook installed"
else
    echo "⚠️  Pre-commit hook source not found at scripts/pre-commit-hook.sh"
    echo "   The hook may already be installed in .git/hooks/"
fi

# Verify
if [ -f "$HOOKS_DIR/pre-commit" ]; then
    echo ""
    echo "✅ Security hooks are active"
    echo "   Every commit will be scanned for secrets"
else
    echo ""
    echo "❌ Hook installation failed"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Next steps:"
echo "  1. Copy .env.example to .env"
echo "  2. Fill in your secrets in .env"
echo "  3. Run: bash scripts/audit-env-security.sh"
echo "═══════════════════════════════════════════════════════════════"
