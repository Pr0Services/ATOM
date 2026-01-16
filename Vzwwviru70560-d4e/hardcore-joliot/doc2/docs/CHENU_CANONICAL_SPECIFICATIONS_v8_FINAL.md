# CHE·NU™ — SPÉCIFICATIONS CANONIQUES v8 FINAL

**Version:** 8 — FINAL COMPLETE  
**Statut:** 🔒 MVP OFFICIALLY FROZEN  
**Date:** 14 décembre 2025

---

> **"The MVP is complete. From now on, we build, not redesign."**

---

## 📊 STRUCTURE

| Layer | Specs | Description |
|-------|-------|-------------|
| **L1** | 1-6 | Foundation |
| **L2** | 7-9 | Quality & Optimization |
| **L3** | 10-12 | UX & Productivity |
| **L4** | 13-14 | SDK & Governance |
| **L5** | 15-16 | Thread System |
| **L6** | 17-18 | Reference |

**18 Specifications | 18 Canonical Statements | 6 Layers**

---

## L1: FOUNDATION (SPEC 1-6)

### Key Concepts

- **External LLMs:** User-mediated, never silent connections
- **Encoding:** ~80% token savings with KEY=VALUE format
- **3 Views:** HUMAN (~1200 tok) | ENCODED (~250 tok) | BINARY (~80 tok)

### SPEC 1: External Intelligence Bridge
> **"CHE·NU governs what you decide to bring back."**

### SPEC 2: Semantic Encoding Layer
> **"Intent is compressed. Meaning is preserved. Cost is controlled."**

### SPEC 3: Semantic Encoding Dictionary v1

```
ACT: SUM|EXT|STR|CMP|ANA|GEN|REF|VER|MAP|CLS|DEC|PLN
SRC: SEL|DOC|WS|MTG|EXT|MIX
FOCUS: FACT|RISK|CONS|OPP|NEXT|DEC|GAP|OPT
MODE: ANA|PREP|DRAFT|CHECK|NONE
FLAGS: RW|UNC|SENS|TRACE
LEN: XS|S|M|L|XL
```

### SPEC 4: Encoding Auto-Suggestion Layer
> **"Suggestions guide understanding. Decisions remain human."**

### SPEC 5: Binary Semantic Encoding
> **"Binary encoding is invisible, reversible, and never authoritative."**

### SPEC 6: Dual Interface UI
> **"Humans write meaning. Systems compress intent. CHE·NU shows both."**

---

## L2: QUALITY & OPTIMIZATION (SPEC 7-9)

### SPEC 7: Encoding Quality Score (EQS)
> **"Quality is visible. Decisions remain human."**

| Score | Quality |
|-------|---------|
| 90-100 | Excellent |
| 70-89 | Good |
| 50-69 | Acceptable |
| <50 | Needs improvement |

### SPEC 8: Agent Compatibility Matrix (ACM)
> **"Agents declare capabilities. Systems enforce limits. No guessing."**

### SPEC 9: Encoding Auto-Optimization
> **"Optimization reduces cost. Meaning remains intact. Control remains human."**

---

## L3: UX & PRODUCTIVITY (SPEC 10-12)

### SPEC 10: Visual Diff Interface
> **"Transparency is not decoration. It is governance made visible."**

### SPEC 11: Batch Encoding Optimization
> **"Patterns are optimized together. Intent remains individual."**

### SPEC 12: Encoding Presets

**6 Initial Presets:**
1. Quick Summary
2. Risk Analysis
3. Decision Prep
4. Document Extract
5. Comparison
6. Planning

> **"Presets accelerate clarity. Control always remains human."**

---

## L4: SDK & GOVERNANCE (SPEC 13-14)

### SPEC 13: SDK Agent Contract

**Agent Definition:**
```
Agent = Stateless analysis unit | No memory | No execution rights | Disposable & replaceable
```

**Forbidden Agent Behaviors:**
- ⛔ Call other agents
- ⛔ Access databases
- ⛔ Modify data
- ⛔ Store memory
- ⛔ Speak to users
- ⛔ Request more scope
- ⛔ Self-optimize

**Agent Declaration Schema:**
```yaml
agent_id: "example_v1"
capabilities: {actions: [SUM,STR,ANA], input_levels: [L1]}
constraints: {max_tokens: 1200, supports_binary: false}
scope_support: [SEL, DOC]
```

> **"Agents are tools. They do not think for the system. They do not act for the user."**

### SPEC 14: Internal Data Governance
> **"Internal data deserves the same respect as intelligence."**

---

## L5: THREAD SYSTEM (SPEC 15-16)

### SPEC 15: .chenu File Format

**Every .chenu file is a thread that represents a user-intention lifecycle.**

```
.chenu File
├── human_intent (string)      ← Original natural language
├── semantic_encoding (string) ← KEY=VALUE format
├── optimized_encoding (string)← Token-optimized
├── binary_encoding (optional) ← Ultra-compact
├── EQS_score (float)          ← 0-100
├── action (string)            ← ACT code
├── proposal (object)          ← Agent proposal
├── versioning (object)        ← Version history
├── scope (string)             ← SEL/DOC/WS/MTG
├── metadata (object)          ← Project, user, etc.
└── audit_log (array)          ← Action history
```

**Example:**
```json
{
  "human_intent": "Summarize risks from the contract",
  "semantic_encoding": "ACT=SUM SRC=DOC SCOPE=SEL FOCUS=[RISK,CONS]",
  "optimized_encoding": "ACT=SUM SRC=DOC SCOPE=SEL FOCUS=[RISK,CONS] RW=0",
  "EQS_score": 85.4,
  "action": "SUM",
  "scope": "SEL",
  "versioning": {"v1": {"timestamp": "2025-01-01T10:00:00Z", "author": "user1"}},
  "audit_log": [{"timestamp": "2025-01-01T10:00:00Z", "action": "created"}]
}
```

**What .chenu Is NOT:**
- ⛔ NOT a chat log
- ⛔ NOT a raw prompt
- ⛔ NOT agent memory
- ⛔ NOT a hidden system file

> **"A .chenu file is not a conversation. It is a governed history of intent and action."**

### SPEC 16: Thread Architecture & Tree

**Tree Structure:**
```
/chenu
├── /personal        (projects, tasks, notes, decisions)
├── /enterprise      (departments, projects, meetings, policies)
├── /creative_studio (concepts, assets, iterations)
├── /architecture    (designs, constraints, approvals)
├── /ai_labs         (experiments, benchmarks, models)
├── /my_team         (roles, agents, workflows)
├── /workspace       (active, archived, templates)
└── /system          (presets, schemas, logs)
```

**Thread Linking (Graph Model):**
```json
"links": {
  "parent": "thread_id_123",
  "related": ["thread_id_456", "thread_id_789"],
  "derived_from": "thread_id_001"
}
```

⚠ No circular dependencies allowed.

> **"The thread is the unit. The tree is the navigation. Meaning lives in the thread."**

---

## L6: REFERENCE (SPEC 17-18)

### SPEC 17: System Architecture Flowchart

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              UI (3 Surfaces: Nova • Context • Workspace)     │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      HUMAN INTENT                            │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│    INTENT COMPRESSION → SEMANTIC ENCODING → AUTO-OPTIMIZE    │
│                         ↓                                    │
│                      EQS SCORE                               │
│                         ↓                                    │
│    VISUAL DIFF (Human ↔ Encoded ↔ Optimized)                │
│                         ↓                                    │
│              [Approve] → BINARY ENCODING (optional)          │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              GOVERNANCE CORE                                 │
│         (Scope • Budget • Permissions • Ledger)              │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│           AGENT COMPATIBILITY MATRIX (ACM)                   │
│     (Check: encoding level, scope, ACT compatibility)        │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENTS (Analysis-only, SDK Contract)            │
│           168 agents • Stateless • Sandboxed                 │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    .chenu THREAD                             │
│         (Atomic Unit • Versioned • Auditable)                │
│                         ↓                                    │
│         VERSIONING & DIFF → LEDGER & AUDIT                   │
│                         ↓                                    │
│              THREAD LINKS (Graph Model)                      │
└─────────────────────────────┬───────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              WORKSPACE ENGINE                                │
│      (Internal/External Data ↔ Thread ↔ UI Feedback)         │
└─────────────────────────────────────────────────────────────┘
```

> **"Architecture is visible. Flow is explicit. Governance is everywhere."**

### SPEC 18: Encoding Handbook

**Encoding Pipeline (Fixed):**
```
Human Intent → Intent Compression → Semantic Encoding (L1)
     → Auto-Optimization → (Optional) Binary Encoding (L2)
     → Agents → Decoding → User

⚠ No step is automatic without consent.
```

**Core Encoding Format:**
```
KEY=VALUE | Arrays: [A,B,C] | Flags: 1/0 | No free text.
```

**Mandatory Keys:**
- ACT (Action)
- SRC (Source)
- SCOPE (Boundary)
- MODE (Behavior)

⚠ Execution is BLOCKED if any mandatory key is missing.

**Canonical Example:**
```
ACT=SUM SRC=DOC SCOPE=SEL FOCUS=[RISK,CONS,NEXT] MODE=ANA OUT=LIST RW=0 TRACE=1
```

**Governance Rules (Absolute):**
- Encoding never executes
- Encoding never decides
- Encoding never hides meaning
- User always confirms

> **"Encode intent. Preserve meaning. Minimize cost."**

---

## 🔒 MVP OFFICIAL FREEZE

### Freeze Status
**MVP architecture is OFFICIALLY FROZEN.**

No new concepts may be added. Only implementation, stabilization, and documentation allowed.

### Change Policy
| Allowed | Forbidden |
|---------|-----------|
| Bug fixes | New specs |
| Implementation | New concepts |
| Documentation | Architecture changes |
| Optimization | Scope expansion |

---

## 📜 ALL 18 CANONICAL STATEMENTS

### L1: Foundation (1-6)
1. "CHE·NU governs what you decide to bring back."
2. "Intent is compressed. Meaning is preserved. Cost is controlled."
3. [Dictionary provides the vocabulary]
4. "Suggestions guide understanding. Decisions remain human."
5. "Binary encoding is invisible, reversible, and never authoritative."
6. "Humans write meaning. Systems compress intent. CHE·NU shows both."

### L2: Quality (7-9)
7. "Quality is visible. Decisions remain human."
8. "Agents declare capabilities. Systems enforce limits. No guessing."
9. "Optimization reduces cost. Meaning remains intact. Control remains human."

### L3: UX (10-12)
10. "Transparency is not decoration. It is governance made visible."
11. "Patterns are optimized together. Intent remains individual."
12. "Presets accelerate clarity. Control always remains human."

### L4: SDK (13-14)
13. "Agents are tools. They do not think for the system. They do not act for the user."
14. "Internal data deserves the same respect as intelligence."

### L5: Threads (15-16)
15. "A .chenu file is not a conversation. It is a governed history of intent and action."
16. "The thread is the unit. The tree is the navigation. Meaning lives in the thread."

### L6: Reference (17-18)
17. "Architecture is visible. Flow is explicit. Governance is everywhere."
18. "Encode intent. Preserve meaning. Minimize cost."

---

## 📊 Architecture Summary

| Component | Count |
|-----------|-------|
| Specifications | 18 |
| Canonical Statements | 18 |
| Layers | 6 |
| Agents | 168 (SDK) |

---

**— END OF CANONICAL SPECIFICATIONS v8 FINAL —**

🔒 **MVP OFFICIALLY FROZEN** 🔒

CHE·NU v27 — Governed Intelligence OS  
Pro-Service Construction • Brossard, Québec  
14 décembre 2025
