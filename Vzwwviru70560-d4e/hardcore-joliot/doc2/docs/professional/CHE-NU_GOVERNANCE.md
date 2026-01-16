# CHE·NU GOVERNANCE — ARCHITECTURE FREEZE

**Version:** 1.0 CANONICAL  
**Status:** OFFICIAL — NON-CREATIVE — NON-NEGOTIABLE  
**Date:** 21 December 2025  
**Authority:** CHE·NU Project

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         CHE·NU ARCHITECTURE FREEZE                           ║
║                                                               ║
║   This document defines the IMMUTABLE architecture           ║
║   that governs all CHE·NU development.                       ║
║                                                               ║
║   NO EXCEPTIONS. NO INTERPRETATIONS.                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## I. CONSTITUTIONAL PRINCIPLES

### 1. Human Sovereignty

**ABSOLUTE RULE:**  
Humans decide always in last resort.

**Implementation:**
- Every execution requires explicit human validation
- No "smart defaults" that bypass human decision
- Human can override any system recommendation
- AI suggests, human validates, system executes

**Violations:**
- ❌ Auto-execute based on confidence score
- ❌ Batch approval of multiple actions
- ❌ "Trust this agent always" settings
- ❌ Background execution without consent

### 2. No Silent Action

**ABSOLUTE RULE:**  
Every action is visible, traceable, and revocable.

**Implementation:**
- All actions logged with who/what/when/why
- All changes produce undo patches
- All executions have audit trails
- UI displays all pending/active operations

**Violations:**
- ❌ Background synchronization
- ❌ Automatic updates without notification
- ❌ Silent data modifications
- ❌ Hidden agent actions

### 3. Single Responsibility

**ABSOLUTE RULE:**  
Each action has ONE identifiable human owner.

**Implementation:**
- Every execution session linked to user_id
- Every validation decision logged with validator
- Every change attributed to specific human
- No "system" or "automatic" as owners

**Violations:**
- ❌ Group ownership without individual attribution
- ❌ "Team decided" without named decider
- ❌ System-initiated changes
- ❌ Collective responsibility dilution

### 4. Reversibility

**ABSOLUTE RULE:**  
Every change can be undone.

**Implementation:**
- All modifications generate undo_patch
- All deletions preserve original data
- All updates store previous state
- Rollback available for configurable period

**Violations:**
- ❌ Destructive operations without backup
- ❌ Irreversible data transformations
- ❌ Permanent deletions without recovery
- ❌ Cascading changes without undo chain

### 5. Auditability

**ABSOLUTE RULE:**  
Complete logs with who/what/when/why.

**Implementation:**
- Timestamp on every operation
- User ID on every action
- Reasoning field for decisions
- Full execution context captured

**Violations:**
- ❌ Anonymous actions
- ❌ Unlogged modifications
- ❌ Missing timestamps
- ❌ Incomplete audit trails

### 6. Separation Cognition/Execution

**ABSOLUTE RULE:**  
"Freedom is cognitive, not executive."

**Implementation:**
- Agents can think/reason/explore freely (Autonomy Zone)
- Execution requires human validation (Verified Zone)
- Simulation mode for risk-free exploration
- Quarantine for all autonomous outputs

**Violations:**
- ❌ Direct write access for agents
- ❌ Auto-apply of agent recommendations
- ❌ Execution without validation gate
- ❌ Bypass of quarantine system

---

## II. ARCHITECTURE FREEZE

### Frozen Elements

**The following are IMMUTABLE:**

#### 1. Spheres (9 Exact)

```
1. Personal 🏠
2. Business 💼
3. Government & Institutions 🏛️
4. Creative Studio 🎨
5. Community 👥
6. Social & Media 📱
7. Entertainment 🎬
8. My Team 🤝
9. Scholar 📚
```

**Rules:**
- ✅ Count: EXACTLY 9
- ❌ Cannot add
- ❌ Cannot remove
- ❌ Cannot merge
- ❌ Cannot rename
- ❌ Cannot redefine semantically

**Max per proposal:** 3-4 spheres

#### 2. Connection Types (4 Only)

```
1. PROJECTION
   - Type: Read-only
   - Direction: Unidirectional
   - Approval: Human required
   - Example: Scholar → Social profile

2. REQUEST
   - Type: Action request
   - Approval: Human required per-action
   - Logged: Yes
   - Example: Personal → Business delegation

3. REFERENCE
   - Type: Static reference
   - Sync: None
   - Direction: Any
   - Example: Business → Personal contact

4. DELEGATION
   - Type: Explicit transfer
   - Logged: Yes
   - Revocable: Yes
   - Example: User → Agent ownership
```

**Rules:**
- ✅ Count: EXACTLY 4
- ❌ Cannot add types
- ❌ Cannot remove types
- ❌ Cannot modify definitions
- ❌ Cannot create hybrids

**Forbidden Connection Types:**
- ❌ Auto-cross-posting
- ❌ Background synchronization
- ❌ Implicit propagation
- ❌ Event listeners across spheres
- ❌ Smart suggestions cross-sphere
- ❌ Group-level decisions

#### 3. Execution Zones (2 Only)

```
🟦 AUTONOMY EXECUTION ZONE
   │
   ├─ Agent can: Reason, explore, simulate, use tools
   ├─ Agent cannot: Modify user data, write memory, trigger agents
   ├─ Output: isolated_execution_results
   └─ Status: UNVERIFIED

              ↓ HUMAN GATE ↓

🟩 VERIFIED EXECUTION ZONE
   │
   ├─ Requires: Human validation per-result
   ├─ Generates: undo_patch for every change
   ├─ Output: domain_tables
   └─ Status: APPLIED
```

**Rules:**
- ✅ Zones: EXACTLY 2
- ❌ Cannot add zones
- ❌ Cannot merge zones
- ❌ Cannot bypass gate
- ❌ Cannot auto-promote

---

## III. MY TEAM SPECIAL RULES

**CRITICAL: My Team is the MOST RESTRICTED sphere.**

### Absolute Prohibitions

```json
{
  "automation": false,
  "auto_assign": false,
  "auto_delegate": false,
  "group_decision": false,
  "team_decides": false,
  "schedule_automatically": false,
  "resolve_conflicts_automatically": false,
  "prioritize_automatically": false
}
```

### Required Patterns

```json
{
  "human_owner_required": true,
  "single_responsible_human": true,
  "per_action_approval": true,
  "explicit_delegation": true,
  "revocable_delegation": true
}
```

### Forbidden Language

**These phrases trigger IMMEDIATE rejection:**

- "assign automatically"
- "team decides"
- "group decision"
- "auto-delegate"
- "schedule automatically"
- "resolve conflicts automatically"
- "prioritize based on..."

**Correct patterns:**

- "Human selects assignee from list"
- "Owner decides after review"
- "User delegates with explicit click"
- "Human schedules after viewing availability"

---

## IV. R&D SYSTEM INTEGRATION

### Mandatory Pipeline

**Every proposal MUST pass through:**

```
1. IDENTIFICATION
   ↓
2. SPHERE ANALYSIS
   ↓
3. CONNECTION TYPE
   ↓
4. RISKS & LIMITS
   ↓
5. REDUNDANCY CHECK
   ↓
6. DECISION (ACCEPT/MODIFY/REJECT)
```

### Required Fields (10)

Every R&D proposal MUST include:

1. **USER TYPE** — Exact persona from official list
2. **CONTEXT** — Real situation (not hypothetical)
3. **HUMAN ACTION** — What user voluntarily does
4. **NEED** — Actual user need (not feature request)
5. **WHAT MUST NEVER BE AUTOMATED** — Explicit list
6. **FAILURE RISK** — Consequences if wrongly automated
7. **SPHERES** — Which spheres involved (max 3-4)
8. **HUMAN VALIDATION** — Explicit approval mechanism
9. **UNDO/REVERSIBILITY** — Rollback mechanism description
10. **REDUNDANCY CHECK** — Modules/endpoints verified

### Allowed Outputs (3 Only)

```
✅ ACCEPT   — Proposal complies, proceed to implementation
⚠️ MODIFY   — Proposal needs changes, return to submitter
❌ REJECT   — Proposal violates policy, permanent rejection
```

**CRITICAL:** Rejection is a SUCCESS of the R&D system.

---

## V. SIMULATION MODE

### Definition

**Simulation allows:**
- Execute logic
- Produce artifacts
- Generate outcomes
- **ZERO side effects**

### Simulation Output

```json
{
  "simulation_id": "sim_abc123",
  "proposed_changes": [...],
  "risk_analysis": {...},
  "human_validation_points": [...],
  "artifacts": [...],
  "quarantined": true,
  "auto_promotable": false
}
```

### Absolute Rules

1. **Quarantine:** All simulation results isolated
2. **No Auto-Promote:** Cannot be applied automatically
3. **Human Gate Required:** Must pass validation gate
4. **Existence Rule:** If not (simulated + linted + human-reviewed + validated), it does not exist

---

## VI. FORBIDDEN AUTOMATION PATTERNS

### Detected Automatically

```regex
auto
automatic
silent
without approval
self-execute
optimize engagement
auto-publish
auto-post
auto-merge
auto-commit
self-approve
decide on behalf
background sync
infinite scroll
```

### Enforcement

- **Level:** ERROR
- **Bypass:** NOT ALLOWED
- **Action:** Immediate rejection

---

## VII. CANONICAL TABLES

### Required for Validation Gate

```sql
1. agent_executions
   - Tracks autonomous execution sessions
   
2. isolated_execution_results
   - Quarantined outputs (UNVERIFIED)
   
3. execution_validations
   - Human validation records
   
4. execution_validation_decisions
   - Per-result decisions (NO batch)
   
5. verified_changes_log
   - Applied changes with undo patches
   
6. cross_sphere_requests
   - Inter-sphere staging (NEVER auto-executed)
```

### Integrity Check

**All 6 tables MUST exist.**  
**Missing any table = Architecture violation.**

---

## VIII. ENFORCEMENT LAYERS

### 1. CLI Layer

**Tool:** `chenu_rnd_lint_allinone.py`

**Checks:**
- Required fields (10)
- Frozen spheres (9)
- Connection types (4)
- Forbidden patterns (20+)
- Repo duplication

**Exit codes:**
- 0 = PASS
- 1 = FAIL

### 2. API Layer

**Tool:** `chenu_rnd_api_fastapi.py`

**Features:**
- Lint endpoint `/api/v1/rnd/lint`
- Health check `/api/v1/rnd/health`
- Guard middleware (blocks non-approved features)

**Headers:**
- `x-chenu-rnd-approved: true` (required for feature deployment)

### 3. CI/CD Layer

**Tool:** `chenu_rnd_github_actions.yml`

**Checks:**
- R&D proposal lint
- Architecture freeze verification
- Canonical table integrity

**Action:** BLOCKS PR if violations

### 4. SDK Layer

**Tool:** `chenu_sdk.py`

**Safe Mode:**
- Can submit proposals
- Can run simulations
- Can query decisions
- **Cannot apply changes**
- **Cannot bypass R&D**
- **Cannot trigger agents**

---

## IX. VERIFICATION MODE

### When Verifying Proposals

**Exact order:**

1. Read `/docs/CHE-NU_POLICY.json`
2. Read `/docs/CHE-NU_GOVERNANCE.md` (this file)
3. Read R&D proposal under review
4. Apply CHE·NU R&D Lint rules logically
5. Produce ONLY: ACCEPT / MODIFY / REJECT

### NOT Allowed

- ❌ Invent rules
- ❌ Reinterpret policy
- ❌ Optimize solutions
- ❌ Suggest features

### Decision Rule

**If any reference is missing or unclear → REJECT.**

**Role:** Verify compliance, not design.

---

## X. COMPLIANCE CHECKLIST

### Architecture Freeze Intact

- [ ] Exactly 9 spheres (no additions/removals)
- [ ] Exactly 4 connection types (no additions/removals)
- [ ] Exactly 2 execution zones (autonomy/verified)
- [ ] 6 canonical tables present
- [ ] My Team automation = ZERO

### Principles Enforced

- [ ] Human sovereignty (every action human-approved)
- [ ] No silent action (all logged/traceable)
- [ ] Single responsibility (one human owner)
- [ ] Reversibility (undo patches generated)
- [ ] Auditability (complete logs)
- [ ] Cognition/execution separation (validation gate)

### R&D System Operational

- [ ] Pipeline 6 steps enforced
- [ ] 10 required fields validated
- [ ] 3 decision outputs only
- [ ] Rejection counted as success

### Enforcement Active

- [ ] CLI linter operational
- [ ] API guard middleware active
- [ ] CI/CD blocking enabled
- [ ] SDK safe mode enforced

---

## XI. AMENDMENT PROCESS

### This Document Can Be Amended ONLY When:

1. **Human authority** explicitly approves
2. **Constitutional principles** remain intact
3. **Architecture freeze** not weakened
4. **Audit trail** documents change rationale

### This Document CANNOT Be Amended For:

- ❌ Convenience
- ❌ Speed
- ❌ "Market demands"
- ❌ "Just this once"

### Frozen Forever:

- 9 spheres
- 4 connection types
- 6 constitutional principles
- My Team zero automation

---

## XII. CONCLUSION

This governance architecture is **NON-NEGOTIABLE**.

**It guarantees:**
- ✅ Human sovereignty absolute
- ✅ No silent actions
- ✅ Complete auditability
- ✅ Full reversibility
- ✅ Architecture stability

**It prohibits:**
- ❌ Automation without validation
- ❌ Bypassing R&D system
- ❌ Violating freeze
- ❌ Group decisions without owners

**The system protects CHE·NU's integrity.**

**The freeze prevents architectural drift.**

**The governance ensures human control.**

---

**Document Authority:** CHE·NU Project  
**Effective Date:** 21 December 2025  
**Version:** 1.0 CANONICAL  
**Status:** OFFICIAL — BINDING — IMMUTABLE
