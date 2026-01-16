# CHE·NU V1 — GAPS & RISKS ANALYSIS

**Date:** 16 décembre 2025  
**Phase:** Consolidation Pre-Development  
**Criticality:** HIGH - Must resolve before MVP development

---

## 🚨 BLOCKERS (Must Fix Immediately)

| ID | Risk | Description | Impact | Mitigation | Owner | ETA |
|----|------|-------------|--------|------------|-------|-----|
| B01 | **Sphere Count Mismatch** | Code has 10 spheres, MEMORY mandates 8 | Cannot proceed with MVP | Consolidate: Architecture + IA Labs + Design → Team/Studio | Arch Team | Week 1 |
| B02 | **No Approval Gates** | Agents can execute without human approval | Violates core governance | Add approval modals at Pipeline Steps 6 & 10 | Backend + UI | Week 1-2 |
| B03 | **MVP Scope Violation** | All spheres implemented (should be 2 only) | Resource waste, confusion | Disable 6 spheres, isolate Personal + Business | Full Stack | Week 1 |
| B04 | **Agent Autonomy** | master_mind.py makes decisions autonomously | Core principle violation | Refactor to request-approval model | Backend | Week 2 |
| B05 | **Missing Encoding Engine** | Governance Step 3 not implemented | Pipeline incomplete | Implement encoding/decoding layer | Backend | Week 2-3 |
| B06 | **Bureau Structure Mismatch** | Each sphere has custom UI | Violates universal model | Create universal Bureau component | Frontend | Week 2-3 |

---

## 🔴 HIGH RISKS (Must Address in MVP)

| ID | Risk | Description | Impact | Mitigation | Priority |
|----|------|-------------|--------|------------|----------|
| H01 | **Nova Role Confusion** | Code treats Nova as orchestrator, MEMORY says guide | User confusion, wrong mental model | Clarify roles: Nova=guide, User Orchestrator=executor | P0 |
| H02 | **Silent Automation** | Multiple services auto-create/execute | Trust violation | Add confirmation at every action | P0 |
| H03 | **Token Misunderstanding** | Docs imply crypto, should be utility | Legal/regulatory risk | Update all documentation | P0 |
| H04 | **No Budget Enforcement** | Token system exists but no hard stops | Cost overruns possible | Implement budget checks before execution | P0 |
| H05 | **Versioning Inconsistency** | Multiple versioning strategies in code | Data integrity risk | Standardize to append-only everywhere | P1 |
| H06 | **Context Isolation Weak** | Data mixing between spheres possible | Privacy/security risk | Enforce strict context validation | P0 |
| H07 | **No Intent Clarification UI** | Users jump straight to execution | Poor quality inputs | Build intent capture + clarification flow | P1 |
| H08 | **Workspace Model Unclear** | GitHub-style vs transversal confusion | UX inconsistency | Clarify and implement transversal model | P1 |
| H09 | **Missing Governance UI** | Budget, permissions, audit not visible | Opacity = distrust | Build governance dashboard/indicators | P1 |
| H10 | **Backend Duplication** | services/ AND app/ folders with overlap | Maintenance nightmare | Consolidate into single structure | P2 |

---

## 🟡 MEDIUM RISKS (Address Post-MVP or Monitor)

| ID | Risk | Description | Impact | Action |
|----|------|-------------|--------|--------|
| M01 | **Frontend Duplication** | web/ (Next.js) AND frontend/ (React/Vite) | Confusion, maintenance | Choose primary, archive other |
| M02 | **Incomplete Thread System** | .chenu concept partially implemented | Feature incompleteness | Complete thread lifecycle |
| M03 | **Meeting Governance Missing** | Meetings exist but not governed | Inconsistent experience | Add governance to meetings |
| M04 | **No Encoding Quality Metric** | Encoding happens but quality unmeasured | Optimization impossible | Add quality scoring |
| M05 | **Audit Trail Gaps** | Some actions not logged | Compliance risk | Complete audit coverage |
| M06 | **No Agent Sandboxing** | Agents may access system resources | Security risk | Implement runtime sandboxing |
| M07 | **Documentation Outdated** | README describes Community focus, not MVP | Onboarding confusion | Update all docs to reflect MEMORY |
| M08 | **Naming Inconsistency** | Enterprise vs Business, Creative vs Studio | Developer confusion | Standardize all naming |
| M09 | **No Performance Baseline** | 508K LOC but no performance data | Scaling unknowns | Establish performance benchmarks |
| M10 | **Test Coverage Unknown** | Tests exist but coverage unmeasured | Quality unknowns | Measure and establish targets |

---

## 🟢 LOW / COSMETIC (Nice to Have)

| ID | Risk | Description | Impact | Action |
|----|------|-------------|--------|--------|
| L01 | **UI Polish** | 3-Hub layout functional but basic | Visual appeal | Design refinement post-MVP |
| L02 | **Error Messages** | Generic errors, not user-friendly | UX friction | Improve messaging |
| L03 | **Loading States** | Minimal loading indicators | Perceived performance | Add skeletons/spinners |
| L04 | **Keyboard Shortcuts** | Mouse-only navigation | Power user UX | Add shortcuts |
| L05 | **Dark Mode** | Light mode only | Preference | Add theme support |
| L06 | **Internationalization** | English only | Market reach | Add i18n post-MVP |
| L07 | **File Naming** | chenu-b10-, chenu-b11- prefixes | Code navigation | Rename logically |
| L08 | **Code Comments** | Minimal inline documentation | Maintainability | Add JSDoc/docstrings |
| L09 | **Git History** | Monolithic commits possible | Blame/archeology | Enforce commit standards |
| L10 | **Logo/Branding** | Placeholder assets | Brand identity | Professional design |

---

## 📊 RISK MATRIX

```
                    LIKELIHOOD
                    ↓
    ┌───────────────────────────────────┐
  I │                                   │
  M │  H04  H06   │  B02  B04   │       │
  P │  H05  M06   │  B01  B03   │       │
  A │─────────────┼─────────────┼───────│
  C │  H07  H08   │  B05  B06   │       │
  T │  M02  M03   │  H01  H02   │       │
    │─────────────┼─────────────┼───────│
    │  M07  M08   │  H03  H09   │       │
    │  L01→L10    │  H10        │       │
    └───────────────────────────────────┘
         LOW      MEDIUM      HIGH
```

**Interpretation:**
- **Top-Right (Red Zone):** BLOCKERS - cannot proceed
- **Middle-Right (Orange):** HIGH RISKS - must address in MVP
- **Middle-Center (Yellow):** MEDIUM - monitor, address as needed
- **Bottom-Left (Green):** LOW - post-MVP improvements

---

## 🎯 RISK MITIGATION PRIORITIES

### Week 1 (Critical Path)

**BLOCKERS ONLY:**
```
1. B01: Consolidate to 8 spheres
2. B03: Disable non-MVP spheres
3. B02: Add approval gate modals (UI mockups)
4. B04: Audit agent autonomy (identify violations)
```

**Deliverable:** MVP scope locked, no autonomous agents, 8 spheres confirmed

---

### Week 2 (High Risks)

**HIGH RISKS + Continue Blockers:**
```
1. B02: Implement approval gates (backend + frontend)
2. B04: Refactor orchestration (request-approval model)
3. B05: Build encoding engine (basic version)
4. H01: Clarify Nova vs Orchestrator roles
5. H02: Audit silent automation (add confirms)
6. H04: Implement budget enforcement
7. H06: Enforce context isolation
```

**Deliverable:** Governance pipeline functional, no silent actions, budget enforced

---

### Week 3 (Completion)

**Remaining HIGH + Start MEDIUM:**
```
1. B06: Universal Bureau component
2. H03: Update token documentation
3. H05: Standardize versioning
4. H07: Intent clarification UI
5. H08: Clarify workspace model
6. H09: Governance visibility UI
7. M02: Complete thread system
```

**Deliverable:** MVP feature-complete, governance visible, UX consistent

---

### Week 4-6 (Polish + Testing)

**MEDIUM risks + Testing:**
```
1. H10: Backend consolidation
2. M01: Choose primary frontend
3. M03: Meeting governance
4. M05: Complete audit trail
5. M07: Update documentation
6. M08: Naming standardization
7. Full integration testing
8. Security audit
9. Performance baseline
10. Investor demo preparation
```

**Deliverable:** Production-ready MVP, docs updated, demo ready

---

## 🚦 GO/NO-GO CRITERIA

### Cannot Proceed to Development Until:

- [ ] **B01-B06 RESOLVED** (All blockers cleared)
- [ ] **8 Spheres Confirmed** (Code matches MEMORY)
- [ ] **MVP Scope Frozen** (Personal + Business only)
- [ ] **Approval Gates Designed** (UI/UX mockups ready)
- [ ] **Architecture Document Updated** (Canonical structure defined)
- [ ] **Backend Structure Decided** (services/ vs app/ resolved)
- [ ] **Frontend Primary Chosen** (web/ or frontend/ decided)
- [ ] **Nova Role Clarified** (Documentation + Code alignment)
- [ ] **Token Nature Clarified** (All docs say "utility credits")
- [ ] **Governance Pipeline Documented** (10 steps with owners)

### Cannot Proceed to Testing Until:

- [ ] **All BLOCKERS Resolved** (B01-B06 = ✅)
- [ ] **All HIGH RISKS Addressed** (H01-H10 mitigated)
- [ ] **MVP Features Implemented** (Identity, Context, Thread, Governance, Budget)
- [ ] **No Silent Automation** (Every action requires approval)
- [ ] **Budget Enforcement Works** (Hard stops implemented)
- [ ] **Context Isolation Verified** (No data leakage between spheres)
- [ ] **Universal Bureau Built** (10 sections for Personal + Business)
- [ ] **Documentation Updated** (README, API docs, architecture)

### Cannot Proceed to Demo Until:

- [ ] **All BLOCKERS + HIGH Resolved**
- [ ] **Key MEDIUM Risks Addressed** (M02, M03, M05, M07, M08)
- [ ] **End-to-End Tests Passing** (Happy path works)
- [ ] **Security Baseline Met** (No critical vulnerabilities)
- [ ] **Performance Acceptable** (<3s page load, <500ms API)
- [ ] **Governance Visible** (User can see what AI does)
- [ ] **Demo Script Ready** (7-minute walkthrough)
- [ ] **Investor Materials Ready** (Deck + one-pager)

---

## 📋 RISK TRACKING TEMPLATE

Use this for each risk during mitigation:

```markdown
## Risk ID: [XXX]

**Title:** [Risk Name]

**Status:** [ ] Open [ ] In Progress [ ] Resolved [ ] Accepted

**Severity:** [ ] BLOCKER [ ] HIGH [ ] MEDIUM [ ] LOW

**Description:**
[What is the risk?]

**Impact:**
[What happens if we don't fix it?]

**Root Cause:**
[Why does this risk exist?]

**Mitigation Plan:**
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Verification:**
- [ ] [How we know it's fixed]
- [ ] [Test case or validation]

**Owner:** [Name]
**Due Date:** [Date]
**Actual Resolution:** [Date + Notes]
```

---

## 🔍 CONTINUOUS MONITORING

### Daily Standup Questions:

1. Any new risks discovered?
2. Any BLOCKER risks resolved?
3. Any HIGH risks escalating?
4. Any dependencies blocking risk mitigation?

### Weekly Review:

- Update risk severity (may change as we learn more)
- Re-prioritize based on new information
- Identify risks that can be moved to "Accepted"
- Flag risks requiring architecture decisions

### Pre-Milestone Gates:

Before each major milestone (Week 2, 4, 6):
- Review all BLOCKER + HIGH risks
- Ensure mitigation plans are on track
- Escalate any risks trending worse
- Update stakeholders on risk status

---

## 📈 SUCCESS METRICS

**Risk Management is Successful When:**

1. **Zero BLOCKERS at Week 1 end**
2. **<5 HIGH risks unresolved at Week 3 end**
3. **All MEDIUM risks have mitigation plans**
4. **No new BLOCKER risks introduced**
5. **Risk burn-down trend is negative (risks decreasing)**
6. **Team confidence in MVP delivery: >80%**

---

## 🎯 FINAL NOTE

**Risk management is not about perfection.**  
It's about **awareness, prioritization, and mitigation velocity**.

The goal is NOT to have zero risks.  
The goal is to have NO UNMANAGED risks.

**Every risk should be:**
- Identified
- Assessed
- Owned
- Tracked
- Mitigated or Accepted

**If a risk becomes reality, we:**
1. Assess impact
2. Communicate clearly
3. Adjust plan
4. Learn for next time

---

**🚀 LET'S MANAGE THESE RISKS AND SHIP A GREAT MVP! 🔥**
