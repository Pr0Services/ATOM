# AT·OM — Security Protocol

## INCIDENT 2026-02-05 : ZAMA Token Compromise

### What happened
Private keys for Hedera accounts were committed to the repository in `.env` files.
The ZAMA token (0.0.7730446) and associated accounts (0.0.7702951, 0.0.7727679) are **permanently compromised**.

### What was done
1. All compromised secrets purged from the codebase
2. Migration to new AT-OM$ token (0.0.7780104) on new account (0.0.7774579)
3. Pre-commit hook installed to prevent future leaks
4. `.gitignore` hardened with comprehensive secret patterns
5. Security audit script created

### Compromised assets (DO NOT USE)
| Asset | ID | Status |
|-------|-----|--------|
| Operator Account | 0.0.7702951 | COMPROMISED |
| Treasury Account | 0.0.7727679 | COMPROMISED |
| ZAMA Token | 0.0.7730446 | ABANDONED |

### New secure assets (AT-OM$)
| Asset | ID | Status |
|-------|-----|--------|
| Operator Account | 0.0.7774579 | ACTIVE |
| AT-OM$ Token | 0.0.7780104 | ACTIVE |
| NFT Collection | 0.0.7780274 | ACTIVE |

---

## Secret Management Protocol

### Rule 1: Never commit secrets
- Private keys, API keys, and passwords go in `.env` **only**
- `.env` is in `.gitignore` — NEVER remove it
- Use `.env.example` as template (no real values)

### Rule 2: Use the pre-commit hook
The pre-commit hook at `.git/hooks/pre-commit` scans every commit for:
- `.env` files being staged
- Private key patterns (hex keys, API keys, PEM files)
- Known compromised values
- AWS/GCP/Azure credential patterns

**Never bypass with `--no-verify` unless you understand the risk.**

### Rule 3: Run security audits
```bash
bash scripts/audit-env-security.sh
```
Run this before any deployment or after adding new secrets.

### Rule 4: Key rotation
If you suspect any key is compromised:
1. **Immediately** generate a new key
2. Update `.env` with the new key
3. Revoke the old key on the provider (Hedera Portal, Anthropic Console, etc.)
4. Run the audit script to verify cleanup
5. Document the incident in this file

### Rule 5: Separate environments
- **Development**: Use testnet, test API keys
- **Staging**: Use testnet with production-like config
- **Production**: Use mainnet, production keys, restricted access

---

## .env Setup Guide

### Step 1: Copy the template
```bash
cp .env.example .env
```

### Step 2: Fill in your secrets
Edit `.env` and replace all `YOUR_*_HERE` placeholders:

```
HEDERA_PRIVATE_KEY=your_actual_private_key
ANTHROPIC_API_KEY=your_actual_api_key
OPENAI_API_KEY=your_actual_api_key
```

### Step 3: Secure file permissions (Mac/Linux)
```bash
chmod 600 .env
```

### Step 4: Verify protection
```bash
# Should NOT show .env in output:
git status

# Run security audit:
bash scripts/audit-env-security.sh
```

---

## Security Checklist

Before any deployment:
- [ ] Run `bash scripts/audit-env-security.sh`
- [ ] Verify `.env` is NOT tracked: `git ls-files .env` (should be empty)
- [ ] Verify pre-commit hook is active: `ls -la .git/hooks/pre-commit`
- [ ] Check no private keys in source: `grep -r "0x[a-fA-F0-9]\{64\}" --include="*.js" --include="*.py" .`
- [ ] Verify compromised accounts are not used anywhere
- [ ] Rotate any keys that may have been exposed

---

## Emergency Response

If secrets are leaked:

### Immediate (within 5 minutes)
1. Rotate the compromised key on the provider
2. Update `.env` with the new key
3. If committed to git: `git rm --cached .env && git commit`

### Short term (within 1 hour)
4. Run full audit: `bash scripts/audit-env-security.sh`
5. Check git history: `git log --all -S "leaked_pattern"`
6. If in git history, use BFG Repo Cleaner:
   ```bash
   bfg --replace-text passwords.txt
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   ```

### Documentation
7. Add incident to this SECURITY.md
8. Update compromised assets table
9. Notify team members

---

*AT·OM : 444 Hz : Protection through Sovereignty*
