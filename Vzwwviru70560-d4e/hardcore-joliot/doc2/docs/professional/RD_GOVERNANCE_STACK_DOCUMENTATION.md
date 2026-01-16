# CHE·NU R&D GOVERNANCE STACK — DOCUMENTATION COMPLÈTE

**Version:** 1.0 ALL-IN-ONE  
**Status:** OFFICIAL — NON CREATIVE — NON NEGOTIABLE  
**Date:** 21 December 2025

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         R&D GOVERNANCE STACK — THREE LAYERS                  ║
║                                                               ║
║   CLI + API + CI/CD = COMPLETE PROTECTION                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 🎯 OVERVIEW

The R&D Governance Stack provides **three layers of protection**:

1. **CLI Layer** — Local development (chenu_rnd_lint_allinone.py)
2. **API Layer** — Runtime enforcement (FastAPI integration)
3. **CI/CD Layer** — Automated checks (GitHub Actions)

**Philosophy:**
- Humans define needs
- R&D validates hypotheses
- Architecture is frozen
- Automation is isolated

---

## 📦 STACK COMPONENTS

### 1️⃣ CLI LAYER (chenu_rnd_lint_allinone.py)

**Purpose:** Local R&D proposal validation

**Features:**
- ✅ Freeze architectural enforcement (9 spheres, 4 connections)
- ✅ Required fields validation (10 fields)
- ✅ Forbidden automation detection (13 patterns)
- ✅ My Team automation ban (7 patterns)
- ✅ **Repo duplication check** (token overlap)
- ✅ Human validation verification
- ✅ Reversibility check
- ✅ JSON output support

**Usage:**

```bash
# Basic lint
python3 chenu_rnd_lint_allinone.py --in proposal.md

# With repo duplication check (RECOMMENDED)
python3 chenu_rnd_lint_allinone.py \
    --in proposal.md \
    --repo /path/to/project

# With JSON output
python3 chenu_rnd_lint_allinone.py \
    --in proposal.md \
    --repo /path/to/project \
    --json report.json

# Fail on warnings
python3 chenu_rnd_lint_allinone.py \
    --in proposal.md \
    --fail-on-warn
```

**Exit Codes:**
- `0` = Pass (no errors)
- `1` = Fail (errors or warnings with --fail-on-warn)
- `2` = File not found

### 2️⃣ API LAYER (chenu_rnd_api_fastapi.py)

**Purpose:** Runtime R&D enforcement via API

**Features:**
- ✅ `/api/v1/rnd/lint` — Lint proposal endpoint
- ✅ `/api/v1/rnd/health` — System health check
- ✅ **Guard Middleware** — Blocks non-approved features
- ✅ Auto-rejection of proposals with errors
- ✅ Integration with existing FastAPI app

**Installation:**

```python
# main.py

from fastapi import FastAPI
from chenu_rnd_api_fastapi import install_rnd_governance

app = FastAPI(title="CHE·NU API")

# Install R&D governance
install_rnd_governance(
    app,
    repo_path="/path/to/project",  # For duplication check
    enable_guard=True,              # Block non-approved features
    protected_prefixes=[            # Optional custom prefixes
        "/api/v1/features",
        "/api/v1/modules",
        "/api/v1/connections"
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**API Usage:**

```bash
# Lint proposal via API
curl -X POST http://localhost:8000/api/v1/rnd/lint \
  -H "Content-Type: application/json" \
  -d '{
    "proposal_text": "USER TYPE: ...\nCONTEXT: ...",
    "check_repo_duplicates": true
  }'

# Response (PASS):
{
  "status": "PASS",
  "errors": 0,
  "warnings": 0,
  "findings": [
    {
      "level": "INFO",
      "code": "RND_OK",
      "message": "Proposal valid as R&D hypothesis",
      "hint": "Proceed to human review"
    }
  ]
}

# Response (FAIL):
# HTTP 422
{
  "error": "RND_PROPOSAL_REJECTED",
  "message": "Proposal failed R&D lint with 2 error(s)",
  "findings": [...]
}
```

**Guard Middleware:**

The guard middleware blocks feature deployment without R&D approval:

```bash
# Without approval header → BLOCKED
curl -X POST http://localhost:8000/api/v1/features \
  -H "Content-Type: application/json" \
  -d '{"name": "new-feature"}'

# Response: HTTP 403
{
  "error": "RND_APPROVAL_REQUIRED",
  "message": "Feature deployment requires R&D approval",
  "hint": "Submit proposal via /api/v1/rnd/lint first"
}

# With approval header → ALLOWED
curl -X POST http://localhost:8000/api/v1/features \
  -H "Content-Type: application/json" \
  -H "x-chenu-rnd-approved: true" \
  -d '{"name": "new-feature"}'

# Response: HTTP 200 (feature created)
```

### 3️⃣ CI/CD LAYER (chenu_rnd_github_actions.yml)

**Purpose:** Automated R&D governance in CI/CD

**Features:**
- ✅ Auto-lint all proposals on PR
- ✅ Architecture freeze verification
- ✅ Canonical validation gate integrity check
- ✅ PR comments with failure details
- ✅ Artifact upload for reports
- ✅ Summary generation

**Installation:**

```bash
# Copy workflow to GitHub Actions
cp chenu_rnd_github_actions.yml .github/workflows/

# Commit and push
git add .github/workflows/chenu_rnd_github_actions.yml
git commit -m "feat: Add R&D governance CI/CD"
git push
```

**What it checks:**

1. **R&D Proposal Lint**
   - All proposals in `docs/proposals/` must pass
   - Repo duplication check enabled
   - Fails on warnings

2. **Architecture Freeze**
   - No new spheres added
   - No new connection types beyond 4

3. **Canonical Validation Gate**
   - All 6 canonical tables present
   - No autonomy zone bypasses

**Workflow Triggers:**

- Pull requests modifying:
  - `docs/proposals/**/*.md`
  - `backend/**/*.py`
  - `frontend/**/*.ts(x)`
- Pushes to `main` or `develop`

---

## 🔒 VERIFICATION RULES

### Required Fields (10)

Every proposal MUST include:

1. `USER TYPE` — Exact persona from official list
2. `CONTEXT` — Real situation (not hypothetical)
3. `HUMAN ACTION` — What user voluntarily does
4. `NEED` — Actual user need
5. `WHAT MUST NEVER BE AUTOMATED` — Explicit list
6. `FAILURE RISK` — Consequences if wrongly automated
7. `SPHERES` — Which spheres involved
8. `HUMAN VALIDATION` — Explicit approval mechanism
9. `UNDO/REVERSIBILITY` — Rollback mechanism
10. `REDUNDANCY CHECK` — Modules/endpoints checked

### Frozen Architecture

**9 Spheres (EXACT):**
- Personal
- Business
- Government & Institutions
- Creative Studio
- Community
- Social & Media
- Entertainment
- My Team
- Scholar

**4 Connection Types (ONLY):**
- Projection (read-only, unidirectional)
- Request (human approval required)
- Reference (static reference)
- Delegation (explicit transfer)

### Forbidden Patterns

**Automation Patterns (13):**
- `auto`, `automatic`, `silent`
- `without approval`, `self-execute`
- `optimize engagement`

**My Team Banned (7):**
- `assign automatically`
- `group decision`, `team decides`
- `schedule automatically`

### Repo Duplication

**Token Overlap Check:**
- Scans existing repo for tokens (.py, .ts, .js, .sql, .md)
- Compares with proposal NEED field
- Warns if 3+ overlapping tokens (length > 4)

---

## 📊 INTEGRATION WORKFLOW

### Complete R&D Flow

```
1. DEVELOPER WRITES PROPOSAL
   └─> docs/proposals/feature-x.md

2. LOCAL LINT (CLI)
   └─> python3 tools/chenu_rnd_lint_allinone.py \
         --in docs/proposals/feature-x.md \
         --repo . \
         --fail-on-warn
   
   ✅ PASS → Continue
   ❌ FAIL → Fix violations

3. COMMIT & PUSH
   └─> git add docs/proposals/feature-x.md
       git commit -m "proposal: Feature X"
       git push origin feature-branch

4. CI/CD CHECK (GitHub Actions)
   └─> Auto-lint via GitHub Actions
       - R&D proposal lint
       - Architecture freeze check
       - Canonical gate integrity
   
   ✅ PASS → PR allowed
   ❌ FAIL → PR blocked with comment

5. HUMAN REVIEW
   └─> Team reviews proposal
       - Verify user type authentic
       - Validate need is real
       - Approve/Reject/Modify
   
   ✅ APPROVED → Implementation authorized

6. IMPLEMENTATION
   └─> Developer implements via canonical validation gate
       - Create execution session
       - Produce isolated results
       - Human validates per-result
       - Apply approved changes

7. DEPLOYMENT
   └─> API guard middleware enforces approval
       - x-chenu-rnd-approved header required
       - Without header → 403 blocked
       - With header → Feature deployed
```

---

## 🚀 QUICK START

### Step 1: Install CLI

```bash
# Copy linter to tools/
cp chenu_rnd_lint_allinone.py /path/to/project/tools/
chmod +x /path/to/project/tools/chenu_rnd_lint_allinone.py

# Test
python3 tools/chenu_rnd_lint_allinone.py --help
```

### Step 2: Install API

```bash
# Copy API integration
cp chenu_rnd_api_fastapi.py /path/to/project/backend/

# Add to main.py
# (see code example above)

# Start server
uvicorn main:app --reload

# Test
curl http://localhost:8000/api/v1/rnd/health
```

### Step 3: Install CI/CD

```bash
# Copy workflow
mkdir -p .github/workflows
cp chenu_rnd_github_actions.yml .github/workflows/

# Commit
git add .github/workflows/chenu_rnd_github_actions.yml
git commit -m "feat: R&D governance CI/CD"
git push
```

### Step 4: Test Complete Flow

```bash
# 1. Write proposal
cat > docs/proposals/test-feature.md << 'EOF'
USER TYPE: Academic Researcher
CONTEXT: Wants to share research
HUMAN ACTION: Clicks publish button
NEED: Share validated research
WHAT MUST NEVER BE AUTOMATED: Decision to publish
FAILURE RISK: Auto-publishing unvalidated work
SPHERES: Scholar, Social & Media
CONNECTION TYPE: Projection
HUMAN VALIDATION: Explicit click with preview review
UNDO/REVERSIBILITY: Delete projection via button, logged with undo_patch
REDUNDANCY CHECK: Verified against Scholar/Social modules, no duplication
EOF

# 2. Lint locally
python3 tools/chenu_rnd_lint_allinone.py \
    --in docs/proposals/test-feature.md \
    --repo .

# Output: ✅ PASS

# 3. Commit & push
git add docs/proposals/test-feature.md
git commit -m "proposal: Test feature"
git push

# 4. GitHub Actions runs automatically

# 5. Check PR for status
```

---

## 📈 METRICS & MONITORING

### Success Criteria

**CLI:**
- ✅ Valid proposals pass (exit 0)
- ✅ Invalid proposals fail (exit 1)
- ✅ Forbidden patterns detected
- ✅ Duplication warnings generated

**API:**
- ✅ Lint endpoint responds < 5s
- ✅ Guard blocks non-approved features
- ✅ Health check returns 200

**CI/CD:**
- ✅ All jobs pass on valid PRs
- ✅ Jobs fail on invalid proposals
- ✅ PR comments appear on failures
- ✅ Artifacts uploaded

### Monitoring

```bash
# CLI metrics
find docs/proposals -name "*.md" | \
  xargs -I {} python3 tools/chenu_rnd_lint_allinone.py \
    --in {} --json report-{}.json

# Count errors
jq '.summary.errors' report-*.json | paste -sd+ | bc

# API metrics
curl http://localhost:8000/api/v1/rnd/health

# CI/CD metrics
# Check GitHub Actions tab
```

---

## ⚠️ TROUBLESHOOTING

### CLI Issues

**Problem:** `ImportError: No module named 'dataclasses'`
**Solution:** Upgrade Python to 3.7+

**Problem:** `FileNotFoundError: proposal.md`
**Solution:** Use absolute or relative path

**Problem:** False positive on automation pattern
**Solution:** Rephrase proposal to avoid trigger words

### API Issues

**Problem:** `503 Service Unavailable`
**Solution:** Ensure linter exists at `tools/chenu_rnd_lint_allinone.py`

**Problem:** Guard middleware blocks legitimate request
**Solution:** Add `x-chenu-rnd-approved: true` header

**Problem:** Timeout on lint
**Solution:** Reduce proposal size or increase timeout (default 30s)

### CI/CD Issues

**Problem:** Workflow doesn't trigger
**Solution:** Check file paths in `on.pull_request.paths`

**Problem:** Permission denied on linter
**Solution:** Ensure `chmod +x` was applied and committed

**Problem:** Repo scan too slow
**Solution:** Limit `REPO_SCAN_EXT` or skip repo check

---

## 🎯 BEST PRACTICES

### For Developers

1. **Always lint locally first** before pushing
2. **Use repo duplication check** to avoid redundancy
3. **Read suggestions** in lint output carefully
4. **Iterate** until errors=0
5. **Document rejections** in proposal comments

### For Teams

1. **Enforce CI/CD** — Make workflow required
2. **Review approvals** — Human review after lint pass
3. **Track rejections** — Maintain rejection log
4. **Update personas** — Keep user type list current
5. **Audit quarterly** — Verify freeze integrity

### For Architects

1. **Monitor violations** — Track forbidden patterns
2. **Update linter** — Add new checks as needed
3. **Document exceptions** — Rare legitimate bypasses
4. **Review architecture** — Ensure freeze holds
5. **Educate team** — Training on R&D system

---

## 📚 REFERENCES

- **R&D System:** `CHENU_RD_SYSTEM_CANONICAL_v1.md`
- **Canonical Block:** `backend_migration_v41_canonical.py`
- **Middleware Safety:** `backend_middleware_canonical.py`
- **API Endpoints:** `backend_api_canonical_endpoints.py`

---

## ✅ CHECKLIST

### Installation Complete When:

- [ ] CLI linter in `tools/chenu_rnd_lint_allinone.py`
- [ ] API integration in `backend/chenu_rnd_api_fastapi.py`
- [ ] GitHub Actions workflow in `.github/workflows/`
- [ ] Example proposals in `docs/proposals/examples/`
- [ ] Documentation in `docs/`

### System Working When:

- [ ] Local lint passes valid proposal
- [ ] Local lint fails invalid proposal
- [ ] API `/health` returns 200
- [ ] API `/lint` rejects proposals with errors
- [ ] Guard blocks requests without header
- [ ] CI/CD runs on PR
- [ ] CI/CD fails on violations
- [ ] PR comments appear on failures

---

**Document Version:** 1.0 ALL-IN-ONE  
**Last Updated:** 21 December 2025  
**Status:** PRODUCTION READY
