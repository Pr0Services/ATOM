#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# AT·OM — ENV SECURITY AUDIT SCRIPT
# ═══════════════════════════════════════════════════════════════════════════
# Scans the entire repository for leaked secrets, exposed keys,
# and misconfigured .env files.
#
# Usage: bash scripts/audit-env-security.sh
# ═══════════════════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════"
echo "  AT·OM — SECURITY AUDIT"
echo "  $(date)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
cd "$REPO_ROOT"

ISSUES=0
WARNINGS=0

# ═══════════════════════════════════════════════════════════════════════════
# 1. CHECK .gitignore
# ═══════════════════════════════════════════════════════════════════════════
echo "📋 1. Checking .gitignore..."

if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "   ❌ .env is NOT in .gitignore!"
    ISSUES=$((ISSUES + 1))
else
    echo "   ✅ .env is in .gitignore"
fi

if ! grep -q "\.env\.\*" .gitignore 2>/dev/null; then
    echo "   ❌ .env.* pattern is NOT in .gitignore!"
    ISSUES=$((ISSUES + 1))
else
    echo "   ✅ .env.* pattern is in .gitignore"
fi

if ! grep -q "\*\.key" .gitignore 2>/dev/null; then
    echo "   ⚠️  *.key pattern is NOT in .gitignore"
    WARNINGS=$((WARNINGS + 1))
else
    echo "   ✅ *.key pattern is in .gitignore"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 2. CHECK FOR TRACKED .env FILES
# ═══════════════════════════════════════════════════════════════════════════
echo "📋 2. Checking for tracked .env files..."

TRACKED_ENV=$(git ls-files | grep -E "\.env$|\.env\.local$|\.env\.production$|\.env\.development$" | grep -v "\.example$" | grep -v "\.template$" || true)

if [ -n "$TRACKED_ENV" ]; then
    echo "   ❌ TRACKED .env files found (REMOVE THESE):"
    echo "$TRACKED_ENV" | while read -r f; do
        echo "      - $f"
    done
    ISSUES=$((ISSUES + 1))
else
    echo "   ✅ No .env files are tracked by git"
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 3. SCAN GIT HISTORY FOR LEAKED SECRETS
# ═══════════════════════════════════════════════════════════════════════════
echo "📋 3. Scanning git history for leaked secrets..."

# Known compromised patterns
COMPROMISED_PATTERNS=(
    "c8cd39aae1182effd990971a1c8c012979e7a7bd"
    "sk-ant-api03-"
    "sk-proj-"
)

for PATTERN in "${COMPROMISED_PATTERNS[@]}"; do
    HISTORY_MATCHES=$(git log --all --oneline -S "$PATTERN" 2>/dev/null | head -5 || true)
    if [ -n "$HISTORY_MATCHES" ]; then
        echo "   ⚠️  Pattern '$PATTERN' found in git history:"
        echo "$HISTORY_MATCHES" | while read -r line; do
            echo "      $line"
        done
        WARNINGS=$((WARNINGS + 1))
    fi
done

echo "   Note: Git history may contain old leaked secrets."
echo "   Consider: git filter-branch or BFG Repo Cleaner to purge."
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 4. SCAN CURRENT FILES FOR PRIVATE KEYS
# ═══════════════════════════════════════════════════════════════════════════
echo "📋 4. Scanning current files for private key patterns..."

PATTERNS=(
    "0x[0-9a-fA-F]{64}"
    "-----BEGIN.*PRIVATE KEY-----"
    "sk-ant-api[0-9a-zA-Z_-]{20,}"
    "sk-proj-[0-9a-zA-Z_-]{20,}"
    "AKIA[0-9A-Z]{16}"
    "sb_secret_[a-zA-Z0-9_-]{20,}"
)

for PATTERN in "${PATTERNS[@]}"; do
    MATCHES=$(grep -rlE "$PATTERN" --include="*.js" --include="*.py" --include="*.json" --include="*.ts" --include="*.jsx" --include="*.tsx" --include="*.yaml" --include="*.yml" --include="*.toml" . 2>/dev/null | grep -v node_modules | grep -v ".git/" | grep -v ".env.example" || true)
    if [ -n "$MATCHES" ]; then
        echo "   ⚠️  Pattern found in source files:"
        echo "$MATCHES" | while read -r f; do
            echo "      - $f"
        done
        WARNINGS=$((WARNINGS + 1))
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 5. CHECK .env FILE PERMISSIONS (Unix/Mac)
# ═══════════════════════════════════════════════════════════════════════════
echo "📋 5. Checking .env file permissions..."

find . -name ".env" -not -path "./.git/*" -not -path "*/node_modules/*" 2>/dev/null | while read -r envfile; do
    if [ -f "$envfile" ]; then
        PERMS=$(stat -c "%a" "$envfile" 2>/dev/null || stat -f "%Lp" "$envfile" 2>/dev/null || echo "unknown")
        if [ "$PERMS" != "unknown" ] && [ "$PERMS" != "600" ] && [ "$PERMS" != "400" ]; then
            echo "   ⚠️  $envfile has permissions: $PERMS (should be 600 or 400)"
            WARNINGS=$((WARNINGS + 1))
        else
            echo "   ✅ $envfile permissions: $PERMS"
        fi
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 6. CHECK PRE-COMMIT HOOK
# ═══════════════════════════════════════════════════════════════════════════
echo "📋 6. Checking pre-commit hook..."

if [ -f ".git/hooks/pre-commit" ]; then
    if [ -x ".git/hooks/pre-commit" ] 2>/dev/null || [ -s ".git/hooks/pre-commit" ]; then
        echo "   ✅ Pre-commit hook is installed and executable"
    else
        echo "   ⚠️  Pre-commit hook exists but may not be executable"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "   ❌ No pre-commit hook installed!"
    echo "   Run: cp scripts/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit"
    ISSUES=$((ISSUES + 1))
fi

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# 7. VERIFY COMPROMISED ACCOUNTS ARE NOT ACTIVE
# ═══════════════════════════════════════════════════════════════════════════
echo "📋 7. Verifying compromised accounts are deactivated..."

COMPROMISED_ACCOUNTS=("0.0.7702951" "0.0.7727679")
ACTIVE_ENV=$(cat .env 2>/dev/null || echo "")

for ACCOUNT in "${COMPROMISED_ACCOUNTS[@]}"; do
    if echo "$ACTIVE_ENV" | grep -v "^#" | grep -q "$ACCOUNT"; then
        echo "   ❌ COMPROMISED account $ACCOUNT is still ACTIVE in .env!"
        ISSUES=$((ISSUES + 1))
    else
        echo "   ✅ Compromised account $ACCOUNT is not active"
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
echo "═══════════════════════════════════════════════════════════════"
if [ $ISSUES -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "  🟢 AUDIT PASSED — No security issues found"
elif [ $ISSUES -eq 0 ]; then
    echo "  🟡 AUDIT PASSED WITH WARNINGS"
    echo "  Warnings: $WARNINGS"
else
    echo "  🔴 AUDIT FAILED"
    echo "  Critical issues: $ISSUES"
    echo "  Warnings: $WARNINGS"
fi
echo "═══════════════════════════════════════════════════════════════"
echo ""

exit $ISSUES
