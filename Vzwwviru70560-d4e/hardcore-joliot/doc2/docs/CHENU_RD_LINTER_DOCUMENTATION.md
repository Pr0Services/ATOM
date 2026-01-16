# CHE·NU R&D LINTER — DOCUMENTATION OFFICIELLE

**Version:** 1.0  
**Status:** PRODUCTION TOOL  
**Purpose:** Automated enforcement of CHE·NU R&D System

---

## 🎯 OVERVIEW

The CHE·NU R&D Linter automatically verifies R&D proposals against the canonical CHE·NU architecture and governance rules.

**What it does:**
- ✅ Enforces freeze architectural (9 spheres, 4 connection types)
- ✅ Validates required fields presence and quality
- ✅ Detects forbidden automation patterns
- ✅ Prevents My Team automation drift
- ✅ Ensures human validation gates exist
- ✅ Checks reversibility documentation
- ✅ Verifies redundancy checking

**What it prevents:**
- ❌ Propositions without user types
- ❌ Unknown/invented spheres
- ❌ Invalid connection types
- ❌ Silent/automatic execution
- ❌ Vague validation mechanisms
- ❌ Missing undo capabilities

---

## 📥 INSTALLATION

```bash
# Copy linter to project
cp chenu_rnd_lint.py /path/to/project/tools/

# Make executable
chmod +x chenu_rnd_lint.py

# Test installation
python3 chenu_rnd_lint.py --help
```

**Requirements:**
- Python 3.7+
- No external dependencies (uses stdlib only)

---

## 🚀 USAGE

### Basic Usage

```bash
# Lint a proposal
python3 chenu_rnd_lint.py --in proposal.md

# Output:
# CHE·NU R&D Lint Report — proposals=1 errors=0 warns=0 infos=1
# 
# --- Proposal #1 ---
# USER TYPE: Academic Researcher
# SPHERES: Scholar, Social & Media
# INFO: RND_OK — No blocking violations found.
```

### With JSON Output

```bash
# Generate JSON report
python3 chenu_rnd_lint.py --in proposal.md --json-out report.json

# View JSON
cat report.json
```

### Fail on Warnings

```bash
# Exit nonzero if ANY warnings exist
python3 chenu_rnd_lint.py --in proposal.md --fail-on-warn

# Exit code:
#   0 = No errors or warnings
#   1 = Errors or warnings found
#   2 = File not found
```

---

## 📝 PROPOSAL FORMAT

### Required Fields

Every proposal MUST include these fields:

```markdown
USER TYPE: [Exact persona name from official list]

CONTEXT: [Real situation, not hypothetical]

HUMAN ACTION: [What user voluntarily does]

NEED: [Actual user need, not feature request]

WHAT MUST NEVER BE AUTOMATED: [Explicit list]

FAILURE RISK: [Consequences if wrongly automated]

SPHERES: [Sphere1, Sphere2, ...]

CONNECTION TYPE: [Projection|Request|Reference|Delegation]

HUMAN VALIDATION: [Explicit approval mechanism with logging]

UNDO/REVERSIBILITY: [Mechanism description with undo_patch]

REDUNDANCY CHECK: [Modules/endpoints checked for duplication]
```

### Example: Valid Proposal

```markdown
USER TYPE: Academic Researcher

CONTEXT: Professor has completed peer-reviewed research paper 
accepted in Nature journal. Wants to announce publication to 
professional network.

HUMAN ACTION: User clicks "Publish to Social" button in Scholar 
sphere, reviews preview of social post, confirms publication.

NEED: Share validated research results with professional community 
without manual reposting.

WHAT MUST NEVER BE AUTOMATED: Decision to publish (user must click), 
timing of publication, content of social post (user reviews first).

FAILURE RISK: Auto-publishing research could share 
preliminary/unvalidated work, violate journal embargos, or publish 
during inappropriate times.

SPHERES: Scholar, Social & Media

CONNECTION TYPE: Projection

HUMAN VALIDATION: Explicit per-action approval. User must click 
"Publish" button after reviewing generated social post preview. 
Action logged with timestamp and user_id in 
scholar_social_projections table.

UNDO/REVERSIBILITY: User can delete social post via 
"Remove Projection" button. Original Scholar content remains 
unchanged. Deletion logged in audit trail with undo_patch containing 
original post data.

REDUNDANCY CHECK: Verified against existing Scholar→Social features. 
No current projection mechanism exists. Checked social.py, scholar.py, 
and cross_sphere_requests table—no duplication.
```

---

## 🔍 VERIFICATION RULES

### 1. REQUIRED FIELDS
- **Code:** `RND_MISSING_FIELD`
- **Level:** ERROR
- **Check:** All 10 required fields present and non-empty

### 2. SPHERES FREEZE
- **Code:** `RND_UNKNOWN_SPHERE`
- **Level:** ERROR
- **Check:** Only 9 frozen spheres allowed
- **Frozen set:**
  - Personal
  - Business
  - Government & Institutions
  - Creative Studio
  - Community
  - Social & Media
  - Entertainment
  - My Team
  - Scholar

### 3. TOO MANY SPHERES
- **Code:** `RND_TOO_MANY_SPHERES`
- **Level:** WARN
- **Check:** Max 3-4 spheres recommended per proposal
- **Fix:** Split into smaller proposals or reduce coupling

### 4. CONNECTION TYPE
- **Code:** `RND_BAD_CONNECTION_TYPE`
- **Level:** ERROR
- **Check:** Must be one of 4 allowed types
- **Allowed:**
  - Projection (read-only, unidirectional)
  - Request (human approval required)
  - Reference (static reference)
  - Delegation (explicit human transfer)

### 5. MISSING CONNECTION TYPE
- **Code:** `RND_MISSING_CONNECTION_TYPE`
- **Level:** WARN
- **Check:** If 2+ spheres, connection type should be specified

### 6. HUMAN VALIDATION
- **Code:** `RND_NO_EXPLICIT_HUMAN_GATE`
- **Level:** ERROR
- **Check:** Must contain gating keywords
- **Required keywords (at least one):**
  - explicit
  - approve
  - confirm
  - human
  - review
  - validation
  - click
  - per-action

### 7. REVERSIBILITY
- **Code:** `RND_UNDO_TOO_VAGUE`
- **Level:** ERROR
- **Check:** Undo description must be substantial (min 8 chars)
- **Must describe:** undo_patch, log, version restore mechanism

### 8. REDUNDANCY CHECK
- **Code:** `RND_REDUNDANCY_VAGUE`
- **Level:** WARN
- **Check:** Must reference specific modules/endpoints checked

### 9. FORBIDDEN AUTOMATION
- **Code:** `RND_FORBIDDEN_AUTOMATION`
- **Level:** ERROR
- **Detects patterns:**
  - auto-execute
  - automatically
  - silent action
  - background sync
  - without approval
  - auto-publish/post/merge/commit
  - self-approve
  - decide on behalf
  - optimize engagement
  - infinite scroll

### 10. MY TEAM RISKS
- **Code:** `RND_MYTEAM_AUTOMATION_RISK`
- **Level:** ERROR
- **Detects patterns:**
  - assign automatically
  - auto-delegate
  - team decision
  - group voice
  - resolve conflicts automatically
  - prioritize automatically
  - schedule automatically

---

## 📊 OUTPUT FORMAT

### Human-Readable

```
CHE·NU R&D Lint Report — proposals=1 errors=2 warns=1 infos=0

--- Proposal #1 ---
USER TYPE: Some User
SPHERES: Personal, Business
ERROR: RND_NO_EXPLICIT_HUMAN_GATE (line 10) — HUMAN VALIDATION 
       does not clearly state explicit per-action approval.
  ↳ fix: Specify: 'explicit per-action approval', 'human click', ...

WARN: RND_TOO_MANY_SPHERES (line 8) — Proposal references 5 spheres.
  ↳ fix: Split into smaller proposals or reduce coupling.
```

### JSON Format

```json
{
  "summary": {
    "proposals": 1,
    "errors": 2,
    "warns": 1,
    "infos": 0
  },
  "reports": [
    {
      "proposal_index": 1,
      "findings": [
        {
          "level": "ERROR",
          "code": "RND_NO_EXPLICIT_HUMAN_GATE",
          "message": "HUMAN VALIDATION does not clearly state...",
          "suggestion": "Specify: 'explicit per-action approval'...",
          "line": 10
        }
      ],
      "extracted": {
        "USER TYPE": "Some User",
        "SPHERES": "Personal, Business",
        ...
      }
    }
  ]
}
```

---

## 🔄 INTEGRATION WITH WORKFLOW

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Lint all proposals in /docs/proposals/
for file in docs/proposals/*.md; do
    python3 tools/chenu_rnd_lint.py --in "$file" --fail-on-warn
    if [ $? -ne 0 ]; then
        echo "❌ Proposal $file failed R&D lint"
        exit 1
    fi
done

echo "✅ All proposals pass R&D lint"
```

### CI/CD Pipeline

```yaml
# .github/workflows/rnd-lint.yml
name: R&D Proposals Lint

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Lint R&D Proposals
        run: |
          python3 tools/chenu_rnd_lint.py \
            --in docs/proposals/*.md \
            --json-out lint-report.json \
            --fail-on-warn
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: lint-report
          path: lint-report.json
```

### Manual Review Process

```bash
# 1. Developer writes proposal
vim docs/proposals/feature-x.md

# 2. Run linter
python3 tools/chenu_rnd_lint.py --in docs/proposals/feature-x.md

# 3. Fix violations
# ... edit proposal based on suggestions ...

# 4. Re-run until clean
python3 tools/chenu_rnd_lint.py --in docs/proposals/feature-x.md
# Output: errors=0 warns=0 ✅

# 5. Submit for human review
git add docs/proposals/feature-x.md
git commit -m "proposal: Feature X (linter passed)"
```

---

## ⚠️ IMPORTANT NOTES

### What Linter Does NOT Do

The linter is a **first-pass filter**, not a replacement for human judgment.

**It does NOT:**
- ❌ Verify user type is in official persona list
- ❌ Check if need is genuinely real vs. hypothetical
- ❌ Validate implementation feasibility
- ❌ Assess business value or priority
- ❌ Replace architectural review
- ❌ Guarantee proposal quality

**Human review is STILL REQUIRED for:**
- ✅ User type validation against official list
- ✅ Need authenticity verification
- ✅ Implementation feasibility
- ✅ Final ACCEPT/MODIFY/REJECT decision

### Linter Philosophy

**The linter enforces RULES, not JUDGMENT.**

Rules (linter):
- Must use frozen spheres
- Must specify connection type
- Must document human validation
- Must avoid automation keywords

Judgment (human):
- Is this user type real?
- Is this need genuine?
- Is this the right solution?
- Should we accept this?

---

## 🎯 EXIT CODES

- **0:** No errors (warnings allowed unless --fail-on-warn)
- **1:** Errors found OR warnings found with --fail-on-warn
- **2:** File not found or invalid arguments

---

## 📚 EXAMPLES

### Example 1: Clean Proposal

```bash
$ python3 chenu_rnd_lint.py --in scholar-social-projection.md

CHE·NU R&D Lint Report — proposals=1 errors=0 warns=0 infos=1

--- Proposal #1 ---
USER TYPE: Academic Researcher
SPHERES: Scholar, Social & Media
INFO: RND_OK (line 3) — No blocking violations found.
  ↳ fix: Proceed to human review and, if approved, implement via 
         Human Validation Gate (quarantine → validate → apply).

$ echo $?
0
```

### Example 2: Violations Detected

```bash
$ python3 chenu_rnd_lint.py --in auto-sync-bad.md

CHE·NU R&D Lint Report — proposals=1 errors=3 warns=2 infos=0

--- Proposal #1 ---
USER TYPE: General User
SPHERES: Entertainment, Social & Media, Personal, Business, Community
WARN: RND_TOO_MANY_SPHERES (line 15) — 5 spheres (max 3-4)
ERROR: RND_BAD_CONNECTION_TYPE (line 17) — Invalid 'AutoSync'
ERROR: RND_NO_EXPLICIT_HUMAN_GATE (line 19) — Validation too vague
ERROR: RND_FORBIDDEN_AUTOMATION (line 3) — Pattern 'automatically'

$ echo $?
1
```

---

## 🔧 MAINTENANCE

### Adding New Checks

To add a new lint rule:

1. Add pattern to appropriate list (FORBIDDEN_AUTOMATION_PATTERNS, etc.)
2. Add check in `lint_block()` function
3. Add new Finding with appropriate code
4. Update this documentation
5. Add test case

### Updating Frozen Rules

If CHE·NU architecture changes (extremely rare):

1. Update `FROZEN_SPHERES` set
2. Update `ALLOWED_CONNECTION_TYPES` set
3. Update documentation
4. Update all existing proposals
5. Commit with note: "BREAKING: Architecture freeze update"

---

## 📞 SUPPORT

**Questions:**
1. Read this documentation
2. Check example proposals (valid/invalid)
3. Review CHENU_RD_SYSTEM_CANONICAL_v1.md

**Issues:**
- Bug in linter: Report with minimal reproduction
- False positive: Provide proposal + expected behavior
- Missing check: Provide pattern that should be caught

---

## ✅ SUCCESS CRITERIA

Linter is working correctly when:

✅ Valid proposals pass (exit code 0)  
✅ Invalid proposals fail (exit code 1)  
✅ Forbidden patterns detected  
✅ Frozen rules enforced  
✅ JSON output parseable  
✅ Suggestions actionable  

---

**Document Version:** 1.0  
**Tool Version:** 1.0  
**Last Updated:** 21 December 2025  
**Status:** PRODUCTION READY
