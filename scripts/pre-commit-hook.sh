#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# AT·OM — PRE-COMMIT SECURITY HOOK
# ═══════════════════════════════════════════════════════════════════════════
# Empêche le commit de secrets, clés privées, tokens et credentials
# Installé: 2026-02-05 (après compromission ZAMA)
# ═══════════════════════════════════════════════════════════════════════════

echo "🔒 AT·OM Security Check — Scanning for secrets..."

# Files that are staged for commit
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

FOUND_SECRETS=0

# ═══════════════════════════════════════════════════════════════════════════
# 1. Block .env files (even if somehow not in .gitignore)
# ═══════════════════════════════════════════════════════════════════════════
for FILE in $STAGED_FILES; do
    BASENAME=$(basename "$FILE")
    if [[ "$BASENAME" == ".env" || "$BASENAME" == .env.* ]]; then
        # Allow .env.example and .env.template
        if [[ "$BASENAME" != ".env.example" && "$BASENAME" != ".env.template" && "$BASENAME" != ".env.hedera.example" ]]; then
            echo "❌ BLOCKED: $FILE (environment file with potential secrets)"
            FOUND_SECRETS=1
        fi
    fi
done

# ═══════════════════════════════════════════════════════════════════════════
# 2. Scan for private key patterns in ALL staged files
# ═══════════════════════════════════════════════════════════════════════════
PRIVATE_KEY_PATTERNS=(
    "PRIVATE_KEY.*=.*[0-9a-fA-F]{32,}"
    "sk-ant-api[0-9a-zA-Z_-]{20,}"
    "sk-proj-[0-9a-zA-Z_-]{20,}"
    "sk-[0-9a-zA-Z]{20,}"
    "0x[0-9a-fA-F]{64}"
    "-----BEGIN.*PRIVATE KEY-----"
    "-----BEGIN RSA PRIVATE KEY-----"
    "-----BEGIN EC PRIVATE KEY-----"
    "-----BEGIN OPENSSH PRIVATE KEY-----"
    "AKIA[0-9A-Z]{16}"
    "sb_secret_[a-zA-Z0-9_-]{20,}"
    "ghp_[a-zA-Z0-9]{36}"
    "gho_[a-zA-Z0-9]{36}"
    "glpat-[a-zA-Z0-9_-]{20,}"
    "xoxb-[a-zA-Z0-9-]{20,}"
    "xoxp-[a-zA-Z0-9-]{20,}"
)

for FILE in $STAGED_FILES; do
    # Skip binary files and specific safe files
    if [[ "$FILE" == *.png || "$FILE" == *.jpg || "$FILE" == *.gif || "$FILE" == *.ico || "$FILE" == *.woff* ]]; then
        continue
    fi

    for PATTERN in "${PRIVATE_KEY_PATTERNS[@]}"; do
        MATCHES=$(git show ":$FILE" 2>/dev/null | grep -nE "$PATTERN" 2>/dev/null || true)
        if [ -n "$MATCHES" ]; then
            echo ""
            echo "❌ POTENTIAL SECRET DETECTED in: $FILE"
            echo "   Pattern: $PATTERN"
            echo "   Lines:"
            echo "$MATCHES" | head -3 | while read -r line; do
                echo "     $line"
            done
            FOUND_SECRETS=1
        fi
    done
done

# ═══════════════════════════════════════════════════════════════════════════
# 3. Scan for known compromised values
# ═══════════════════════════════════════════════════════════════════════════
COMPROMISED_VALUES=(
    "c8cd39aae1182effd990971a1c8c012979e7a7bd"
    "0.0.7702951"
    "0.0.7727679"
)

for FILE in $STAGED_FILES; do
    if [[ "$FILE" == *.png || "$FILE" == *.jpg || "$FILE" == *.gif ]]; then
        continue
    fi

    for VALUE in "${COMPROMISED_VALUES[@]}"; do
        if git show ":$FILE" 2>/dev/null | grep -q "$VALUE" 2>/dev/null; then
            # Allow if it's in a comment (documentation about compromised accounts)
            UNCOMMENTED=$(git show ":$FILE" 2>/dev/null | grep "$VALUE" | grep -v "^[[:space:]]*#" | grep -v "^[[:space:]]*//" | grep -v "^[[:space:]]*\*" || true)
            if [ -n "$UNCOMMENTED" ]; then
                echo ""
                echo "⚠️  COMPROMISED VALUE in: $FILE"
                echo "   Value: $VALUE"
                echo "   This account/key was compromised on 2026-02-05"
                FOUND_SECRETS=1
            fi
        fi
    done
done

# ═══════════════════════════════════════════════════════════════════════════
# RESULT
# ═══════════════════════════════════════════════════════════════════════════
if [ $FOUND_SECRETS -ne 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  ❌ COMMIT BLOCKED — Secrets detected"
    echo "═══════════════════════════════════════════════════════════════"
    echo "  Remove secrets before committing."
    echo "  Use .env for secrets, .env.example for templates."
    echo ""
    echo "  To bypass (DANGEROUS): git commit --no-verify"
    echo "═══════════════════════════════════════════════════════════════"
    exit 1
fi

echo "✅ Security check passed — no secrets detected"
exit 0
