# CHE·NU V1 — ULTIMATE QUICK REFERENCE GUIDE
## Everything You Need in One Place

**Version:** V1 CANONICAL FREEZE  
**Date:** 16 décembre 2025  
**Purpose:** Fast lookup for any CHE·NU question

---

## 🎯 CORE IDENTITY

```
CHE·NU is a GOVERNED INTELLIGENCE OPERATING SYSTEM

NOT: chatbot, productivity app, crypto platform
IS:  Intelligence governance for humans
```

---

## 📐 ARCHITECTURE IN 10 SECONDS

```
3 WORKSPACES:
  User      → Full control, no auto-save
  Agent     → Staging only, autonomous
  Review    → Governed integration

8 SPHERES:
  Personal, Business, Government, Creative,
  Community, Social, Entertainment, My Team

10 GOVERNANCE STEPS:
  Intent → Clarify → Encode → Scope → Budget →
  APPROVE → Agent → Staging → Propose → ACCEPT

2 APPROVAL GATES:
  Before execution + Before integration
```

---

## 🔒 GOLDEN RULES (Never Violate)

```
1. Spheres may TALK, LOOK, COPY - never MERGE
2. Agents explore - Humans decide
3. Versions never overwrite - always append
4. No auto-save - explicit only
5. Context always visible
6. Budget always enforced
7. Audit always logged
```

---

## 🏛️ SPHERE → PLACE MAPPING

```yaml
Every Sphere Contains:
  - Entrance Hall (context, welcome)
  - Bureau/Dashboard (overview, threads)
  - Workspace (active editing)
  - Archives (history, versions)
  - Meeting Room (collaboration)
  - Agent Backstage (staging, hidden)

Personal 🏠:
  Theme: Natural (warm, organic)
  Use: Private thinking, planning
  
Business 💼:
  Theme: Futuristic (professional, tech)
  Use: Structured work, accountability
  
Community 👥:
  Theme: Natural (welcoming)
  Use: Shared discussions, public threads
  
...and 5 more (post-MVP)
```

---

## 🎨 UI STATES CHEAT SHEET

```typescript
EDITABLE          → User may modify
READ_ONLY         → View only (external sphere)
STAGING           → Agent-owned, non-destructive
PENDING_APPROVAL  → Waiting for human decision
LOCKED            → Context/scope lock
ERROR             → Governance blocked
DRAFT             → Not yet persisted
VERSIONED         → Immutable snapshot
```

**Rule:** Every state MUST explain WHY

---

## 🛡️ BACKEND MIDDLEWARE STACK

```
Request Flow:
  User/Agent
  → API Gateway
  → M0: Trace (UUID)
  → M1: Auth (validate session)
  → M2: Identity (verify ownership)
  → M3: Context (check validity)
  → M4: Sphere Scope (enforce boundaries)
  → M5: Budget (check/reserve)
  → M6: Policy (CORE - evaluate rules)
  → M7: Audit (log everything)
  → Target Service
```

---

## ⚖️ POLICY RULES QUICK REF

```
R1:  Cross-sphere writes → DENY (403_SCOPE_VIOLATION)
R2:  Cross-sphere reads → ALLOW_READ_ONLY
R3:  Decision updates → DENY (403_DECISION_IMMUTABLE)
R4:  Workspace saves → Must create new version
R5:  Agent production writes → DENY (403_AGENT_WRITE_FORBIDDEN)
R6:  Staging integration → Requires review
R7:  Execution → Requires approval token
R8:  Transformations → Output to staging
R9:  Global search → Read-only + origin visible
R10: Browser extract → Manual only
```

---

## 🎮 FRONTEND STATE MACHINES

```yaml
Session Machine:
  States: booting → unauthenticated → authenticated

Context Machine:
  States: ready ↔ switchingSphere
  Rule: Close all workspaces on sphere switch

Workspace Machine:
  User:   clean → dirty → saving → saved
  Agent:  viewing (read-only)
  Review: comparing → savingUser/Agent → done
  
Agent Machine:
  idle → planning → planReady → pendingApproval →
  executing → completed
  
Search Machine:
  Modes: sphere (editable) | profile (read-only)
  Rule: Origin sphere always shown
  
Budget Machine:
  States: synced | stale | blocked
  Rule: Block if cost > remaining
```

---

## 💾 DATABASE QUICK REF

```sql
-- Immutable Tables (append-only)
threads           -- No UPDATE/DELETE
thread_entries    -- No UPDATE/DELETE  
versions          -- No UPDATE/DELETE
audit_logs        -- No UPDATE/DELETE

-- Mutable Tables (controlled)
user_workspaces       -- UPDATE content allowed (drafts)
agent_staging_workspaces  -- Agent writes here only
contexts          -- Can lock, can switch
spheres           -- User configuration
identities        -- User management

-- Required Headers (ALL requests)
X-Identity-Id
X-Sphere-Id
X-Context-Id
X-Request-Intent
X-Client
X-Trace-Id

-- Optional Headers
X-Approval-Token (for gated operations)
X-Execution-Id (for agent operations)
```

---

## 🚫 FORBIDDEN PATTERNS (Do Not Reintroduce!)

```
❌ Auto-save (setInterval, beforeunload, blur)
❌ Silent modifications (no user awareness)
❌ Version overwrites (UPDATE versions)
❌ Agent direct production writes
❌ Approval bypasses (skip approval flow)
❌ Cross-sphere fusion (merge spheres)
❌ Hidden context switches (silent transitions)
❌ Scope-less search (no origin indicator)
❌ Unlimited execution (no budget check)
❌ Forced workflows (user trapped)
❌ Shared mutable state (race conditions)
❌ Audit gaps (incomplete logs)
```

---

## 🎯 USER FLOWS (5 Key Scenarios)

```
Flow 1: Thread → Agent → Review → Keep Both
  1. Open thread in workspace
  2. Request agent help
  3. Approve plan + cost
  4. Agent works in staging
  5. Review side-by-side
  6. Choose: discard/user/agent/both
  Time: < 3 min

Flow 2: Global Search → Context Switch
  1. Search profile-wide
  2. See result from external sphere
  3. View read-only preview
  4. Switch context to edit
  Time: < 2 min

Flow 3: Encoding → Reject
  1. Request encoding
  2. Review proposal
  3. Reject (no changes)
  Time: < 2 min

Flow 4: Budget Exceeded
  1. Plan execution
  2. See cost exceeds budget
  3. Top up or reduce scope
  Time: < 1 min

Flow 5: Browser Extract
  1. Open external platform
  2. Browse (multi-account)
  3. Manual extract selection
  4. Save to workspace
  Time: < 3 min
```

---

## 🔑 API ENDPOINTS QUICK REF

```bash
# Workspaces
POST   /api/workspaces
PUT    /api/workspaces/:id
POST   /api/workspaces/:id/save
DELETE /api/workspaces/:id?save=true

# Versions
GET    /api/versions/:contentId
GET    /api/versions/:id/compare/:otherId
POST   /api/versions (create new)

# Agent Staging
POST   /api/agent/staging
GET    /api/agent/staging/:executionId
PUT    /api/agent/staging/:executionId/complete

# Comparison
POST   /api/comparisons
GET    /api/comparisons/:id

# Search
GET    /api/search?scope=sphere&q=...
GET    /api/search?scope=profile&q=...

# Context
POST   /api/context/switch
GET    /api/context/:id

# Approval
POST   /api/approvals
POST   /api/approvals/:id/approve
POST   /api/approvals/:id/reject

# Budget
GET    /api/budget
POST   /api/budget/topup
```

---

## 🎨 DESIGN TOKENS

```css
/* 4 Themes */
--theme-futuristic-primary: #3B82F6;
--theme-natural-primary: #22C55E;
--theme-astral-primary: #8B5CF6;
--theme-neutral-primary: #64748B;

/* Sacred Gold (Brand) */
--sacred-gold: #D8B26A;
--ancient-stone: #8D8371;
--jungle-emerald: #3F7249;

/* States */
--color-draft: #FCD34D;
--color-readonly: #60A5FA;
--color-staging: #A78BFA;
--color-versioned: #34D399;
--color-error: #F87171;

/* Workspace Types */
--workspace-user-border: var(--theme-primary);
--workspace-agent-border: #A78BFA;
--workspace-review-border: #F59E0B;
```

---

## 📊 INFRASTRUCTURE COST

```
MVP Monthly Budget ($2,500):
  - AI APIs: $1,500
  - Database: $200
  - Storage: $100
  - Compute: $300
  - Auth/Security: $150
  - Monitoring: $100
  - Other: $150

Production (Scale-dependent):
  - $5,000-20,000/month
```

---

## 🧪 TEST COMMANDS

```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# Policy tests
npm run test:policy

# Specific test files
npm test -- contextService.test.ts
npm test -- policyEngine.test.ts
npm test -- workspace.test.ts

# Coverage
npm run test:coverage

# Watch mode
npm test -- --watch
```

---

## 🚀 DEPLOYMENT COMMANDS

```bash
# Development
npm run dev

# Production build
npm run build

# Production start
npm start

# Database migrations
npm run migrate

# Database seed
npm run seed

# Docker
docker-compose up -d

# Kubernetes
kubectl apply -f k8s/

# Health check
curl http://localhost:3000/health
```

---

## 📋 VALIDATION CHECKLIST

```
Before Deploy:
  [ ] Headers present (100% endpoints)
  [ ] No write without approval
  [ ] Agent writes staging only
  [ ] Versions immutable
  [ ] Search scoped + origin visible
  [ ] Inter-sphere references only
  [ ] Close without save works
  [ ] Save creates new version
  [ ] Diff/comparison works
  [ ] Budget blocks execution
  [ ] Audit log complete

Before Launch:
  [ ] All 5 flows tested
  [ ] Performance acceptable
  [ ] Security audit passed
  [ ] Monitoring configured
  [ ] Rollback plan ready
  [ ] Support channel ready
  [ ] Feedback form ready
```

---

## 🎯 SUCCESS METRICS

```
Technical:
  Zero auto-save violations
  Zero agent production writes
  100% approval coverage
  100% version immutability
  100% workspace isolation

User:
  100% context awareness
  100% cancellation ability
  100% governance visibility
  100% agent transparency

Business:
  MVP demonstrates governance
  Enterprise-ready security
  Audit compliance built-in
  Investor demo compelling
  Defensible IP established
```

---

## 💬 KEY MESSAGES

```
For Investors:
  "The world's first Governed Intelligence OS.
   Autonomy in staging. Authority with humans."

For Users:
  "Intelligence you can trust.
   Every action requires your approval.
   Every change is reversible."

For Enterprise:
  "AI with governance, compliance, and audit trails.
   Enterprise-grade security built-in."
```

---

## 📚 DOCUMENT INDEX

```
ANALYSIS (4 docs):
  1. Analysis & Plan
  2. Gaps & Risks
  3. Canonical Structure
  4. Validation Audit

GOVERNANCE (3 docs):
  5. Addendum v1 (Inter-sphere)
  6. Addendum v2 (Governance)
  7. Addendum v3 (Workspace)

DESIGN (1 doc):
  8. Figma Design System

IMPLEMENTATION (7 docs):
  9.  Integration Roadmap
  10. Do-Not-Reintroduce
  11. Canonical Mapping
  12. Permission & UI States
  13. Backend Governance Guards
  14. Frontend State Machines
  15. Implementation Checklist

TOTAL: 15 documents, ~700 pages
```

---

## 🔍 QUICK TROUBLESHOOTING

```
Problem: Context becomes stale
Solution: Check context expiration, switch sphere closes old context

Problem: Agent can't write
Solution: Verify zone=staging, check agent role permissions

Problem: Version not saving
Solution: Check immutable table permissions, verify append-only

Problem: Budget not blocking
Solution: Verify budgetMiddleware, check reservation logic

Problem: Search showing wrong sphere
Solution: Verify scope parameter, check origin sphere badge

Problem: Approval bypassed
Solution: Check approval token validation, verify gate enforcement

Problem: Workspace won't close
Solution: Remove forced workflows, verify close without save

Problem: Diff not working
Solution: Check version IDs exist, verify content format
```

---

## 🎓 ONBOARDING (New Developers)

```
Day 1: Read This Guide + MEMORY PROMPT
Day 2: Read Workspace Model + Backend Guards
Day 3: Read Frontend State Machines
Day 4: Read Do-Not-Reintroduce List
Day 5: Set up local environment
Day 6-7: Complete first feature (with review)
```

---

## ⚡ EMERGENCY CONTACTS

```
Code Issues:
  - Check GitHub issues
  - Review do-not-reintroduce list
  - Validate against canonical docs

Governance Violations:
  - STOP deployment
  - Review violation type
  - Fix before proceeding
  - Re-run validation

Production Issues:
  - Check monitoring dashboard
  - Review audit logs
  - Check budget status
  - Verify context health
```

---

## 🔒 FINAL PRINCIPLE

```
╔═══════════════════════════════════════════════╗
║                                               ║
║  When in doubt:                               ║
║  1. Check the MEMORY PROMPT                   ║
║  2. Verify governance is visible              ║
║  3. Ensure user can cancel/close              ║
║  4. Confirm context is clear                  ║
║  5. Test that approval is required            ║
║                                               ║
║  If any of these fail → STOP AND FIX          ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

---

**📖 QUICK REFERENCE COMPLETE! EVERYTHING IN ONE PLACE! 🚀**
