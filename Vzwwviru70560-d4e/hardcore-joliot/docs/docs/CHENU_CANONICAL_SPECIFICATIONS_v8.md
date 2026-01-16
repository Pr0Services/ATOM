**SPÉCIFICATIONS CANONIQUES**

**VERSION 8 --- FINAL COMPLETE**

CHE·NU v27 --- Governed Intelligence OS

L1: Foundation (1-6) \| L2: Quality (7-9) \| L3: UX (10-12)

L4: SDK (13-14) \| L5: Threads (15-16) \| L6: Reference (17-18)

**18 Specifications \| 18 Canonical Statements \| 6 Layers**

**🔒 MVP OFFICIALLY FROZEN --- 14 DÉCEMBRE 2025 🔒**

*\"The MVP is complete. From now on, we build, not redesign.\"*

TABLE DES MATIÈRES

**L1: FOUNDATION (Spec 1-6)**

Summary
\...\...\...\...\...\...\...\...\...\...\...\...\...\...\...\..... p.3

**L2: QUALITY & OPTIMIZATION (Spec 7-9)**

Summary
\...\...\...\...\...\...\...\...\...\...\...\...\...\...\...\..... p.4

**L3: UX & PRODUCTIVITY (Spec 10-12)**

Summary
\...\...\...\...\...\...\...\...\...\...\...\...\...\...\...\..... p.5

**L4: SDK & GOVERNANCE (Spec 13-14)**

Summary
\...\...\...\...\...\...\...\...\...\...\...\...\...\...\...\..... p.6

**L5: THREAD SYSTEM (Spec 15-16)**

SPEC 15: .chenu File Format \...\...\...\...\...\...\...\...\.... p.7

SPEC 16: Thread Architecture \...\...\...\...\...\...\...\...\... p.9

**L6: REFERENCE (Spec 17-18) --- NEW**

**SPEC 17: System Architecture Flowchart** \...\...\...\.... p.11

**SPEC 18: Encoding Handbook** \...\...\...\...\...\...\...\.... p.13

**MVP FREEZE & APPENDIX**

Freeze Declaration + 18 Canonical Statements \...\...\..... p.15

L1: FOUNDATION (SPEC 1-6)

  --------- --------------------- ----------------------------------------
  **\#**    **Specification**     **Canonical Statement**

  **1**     External Intelligence *\"CHE·NU governs what you decide to
            Bridge                bring back.\"*

  **2**     Semantic Encoding     *\"Intent is compressed. Meaning is
            Layer                 preserved. Cost is controlled.\"*

  **3**     Dictionary v1         12 ACT + 6 SRC + 8 FOCUS + 5 MODE + 4
                                  FLAGS

  **4**     Auto-Suggestion       *\"Suggestions guide understanding.
                                  Decisions remain human.\"*

  **5**     Binary Encoding       *\"Binary is invisible, reversible, and
                                  never authoritative.\"*

  **6**     Dual Interface UI     *\"Humans write meaning. Systems
                                  compress. CHE·NU shows both.\"*
  --------- --------------------- ----------------------------------------

Key Concepts

-   **External LLMs:** User-mediated, never silent connections

-   **Encoding:** \~80% token savings with KEY=VALUE format

-   **3 Views:** HUMAN (\~1200 tok) \| ENCODED (\~250 tok) \| BINARY
    (\~80 tok)

L2: QUALITY & OPTIMIZATION (SPEC 7-9)

  --------- --------------------- ----------------------------------------
  **\#**    **Specification**     **Canonical Statement**

  **7**     EQS Score (0-100)     *\"Quality is visible. Decisions remain
                                  human.\"*

  **8**     Agent Compatibility   *\"Agents declare capabilities. Systems
            Matrix                enforce limits. No guessing.\"*

  **9**     Auto-Optimization     *\"Optimization reduces cost. Meaning
                                  remains intact.\"*
  --------- --------------------- ----------------------------------------

EQS Score Ranges

  ----------------- ----------------- ----------------- -----------------
  **0-30 🔴 Poor**  **31-60 🟠 OK**   **61-80 🟢 Good** **81-100 🟢🟢
                                                        Optimal**

  ----------------- ----------------- ----------------- -----------------

Optimization Rules

  ----------------------------------- -----------------------------------
  **✓ MAY: Reduce, tighten,           **✗ MAY NOT: Change ACT/SRC, expand
  simplify**                          scope**

  ----------------------------------- -----------------------------------

L3: UX & PRODUCTIVITY (SPEC 10-12)

  --------- --------------------- ----------------------------------------
  **\#**    **Specification**     **Canonical Statement**

  **10**    Visual Diff Interface *\"Transparency is not decoration. It is
                                  governance made visible.\"*

  **11**    Batch Optimization    *\"Patterns are optimized together.
                                  Intent remains individual.\"*

  **12**    Encoding Presets      *\"Presets accelerate clarity. Control
                                  always remains human.\"*
  --------- --------------------- ----------------------------------------

6 Initial Presets

  ----------------- ---------------------------------------------------------
  **Preset**        **Encoding**

  **Summary**       ACT=SUM SRC=DOC SCOPE=SEL FOCUS=\[FACT,NEXT\] RW=0

  **Analysis**      ACT=ANA SRC=DOC SCOPE=SEL FOCUS=\[RISK,CONS,GAP\] UNC=1

  **Structuring**   ACT=STR SRC=DOC SCOPE=SEL FOCUS=\[FACT\] OUT=TREE

  **Decision**      ACT=DEC SRC=DOC SCOPE=SEL FOCUS=\[OPT,RISK,CONS\] OUT=TAB

  **Comparison**    ACT=CMP SRC=MIX SCOPE=SEL FOCUS=\[FACT,GAP,OPT\] OUT=TAB

  **Meeting**       ACT=SUM SRC=MTG SCOPE=MTG FOCUS=\[DEC,NEXT\]
  ----------------- ---------------------------------------------------------

L4: SDK & GOVERNANCE (SPEC 13-14)

  --------- --------------------- ----------------------------------------
  **\#**    **Specification**     **Canonical Statement**

  **13**    SDK Agent Contract    *\"Agents are tools. They do not think
                                  for the system.\"*

  **14**    Internal Data         *\"Internal data deserves the same
            Governance            respect as intelligence.\"*
  --------- --------------------- ----------------------------------------

Agent Definition

**Agent = Stateless analysis unit \| No memory \| No execution rights \|
Disposable & replaceable**

Forbidden Agent Behaviors

**⛔ Call other agents \| Access databases \| Modify data \| Store
memory \| Speak to users \| Request more scope \| Self-optimize**

Agent Declaration Schema

agent_id: \"example_v1\" capabilities: {actions: \[SUM,STR,ANA\],
input_levels: \[L1\]} constraints: {max_tokens: 1200, supports_binary:
false} scope_support: \[SEL, DOC\]

SPEC 15: .chenu FILE FORMAT

*Every .chenu file is a thread that represents a user-intention
lifecycle. It tracks transformation from human input to machine encoding
to agent outputs.*

File Structure

.chenu File ├── human_intent (string) ← Original natural language ├──
semantic_encoding (string) ← KEY=VALUE format ├── optimized_encoding
(string) ← Token-optimized ├── binary_encoding (optional) ←
Ultra-compact ├── EQS_score (float) ← 0-100 ├── action (string) ← ACT
code ├── proposal (object) ← Agent proposal ├── versioning (object) ←
Version history ├── scope (string) ← SEL/DOC/WS/MTG ├── metadata
(object) ← Project, user, etc. └── audit_log (array) ← Action history

Example .chenu File

{ \"human_intent\": \"Summarize risks from the contract\",
\"semantic_encoding\": \"ACT=SUM SRC=DOC SCOPE=SEL
FOCUS=\[RISK,CONS\]\", \"optimized_encoding\": \"ACT=SUM SRC=DOC
SCOPE=SEL FOCUS=\[RISK,CONS\] RW=0\", \"EQS_score\": 85.4, \"action\":
\"SUM\", \"scope\": \"SEL\", \"versioning\": {\"v1\": {\"timestamp\":
\"2025-01-01T10:00:00Z\", \"author\": \"user1\"}}, \"audit_log\":
\[{\"timestamp\": \"2025-01-01T10:00:00Z\", \"action\": \"created\"}\] }

What .chenu Is NOT

**⛔ NOT a chat log \| NOT a raw prompt \| NOT agent memory \| NOT a
hidden system file**

Governance Rules

-   **All files must be versioned**

-   No silent transformations

-   User always confirms

-   **No file automatically executed**

***\"A .chenu file is not a conversation. It is a governed history of
intent and action.\"***

SPEC 16: THREAD ARCHITECTURE & TREE

*Threads are living units. Folders are contextual views. The thread is
the truth. The tree is a lens.*

Tree Structure

/chenu ├── /personal (projects, tasks, notes, decisions) ├── /enterprise
(departments, projects, meetings, policies) ├── /creative_studio
(concepts, assets, iterations) ├── /architecture (designs, constraints,
approvals) ├── /ai_labs (experiments, benchmarks, models) ├── /my_team
(roles, agents, workflows) ├── /workspace (active, archived, templates)
└── /system (presets, schemas, logs)

Thread Lifecycle States

  ----------- -------------- -------------- -------------- -------------- --------------
  **draft**   **analyzed**   **proposed**   **accepted**   **executed**   **archived**

  ----------- -------------- -------------- -------------- -------------- --------------

Thread Linking (Graph Model)

\"links\": { \"parent\": \"thread_id_123\", \"related\":
\[\"thread_id_456\", \"thread_id_789\"\], \"derived_from\":
\"thread_id_001\" } ⚠ No circular dependencies allowed.

Export Formats

**Markdown \| JSON \| PDF \| Dataset** --- Export preserves versions,
audit, links

***\"The thread is the unit. The tree is the navigation. Meaning lives
in the thread.\"***

SPEC 17: SYSTEM ARCHITECTURE FLOWCHART

*Complete visual representation of the CHE·NU data flow and governance
architecture.*

System Flow Diagram

┌─────────────────────────────────────────────────────────────┐ │ USER │
└─────────────────────────────┬───────────────────────────────┘ ▼
┌─────────────────────────────────────────────────────────────┐ │ UI (3
Surfaces: Nova • Context • Workspace) │
└─────────────────────────────┬───────────────────────────────┘ ▼
┌─────────────────────────────────────────────────────────────┐ │ HUMAN
INTENT │ └─────────────────────────────┬───────────────────────────────┘
▼ ┌─────────────────────────────────────────────────────────────┐ │
INTENT COMPRESSION → SEMANTIC ENCODING → AUTO-OPTIMIZE │ │ ↓ │ │ EQS
SCORE │ │ ↓ │ │ VISUAL DIFF (Human ↔ Encoded ↔ Optimized) │ │ ↓ │ │
\[Approve\] → BINARY ENCODING (optional) │
└─────────────────────────────┬───────────────────────────────┘ ▼
┌─────────────────────────────────────────────────────────────┐ │
GOVERNANCE CORE │ │ (Scope • Budget • Permissions • Ledger) │
└─────────────────────────────┬───────────────────────────────┘ ▼
┌─────────────────────────────────────────────────────────────┐ │ AGENT
COMPATIBILITY MATRIX (ACM) │ │ (Check: encoding level, scope, ACT
compatibility) │
└─────────────────────────────┬───────────────────────────────┘ ▼
┌─────────────────────────────────────────────────────────────┐ │ AGENTS
(Analysis-only, SDK Contract) │ │ 168 agents • Stateless • Sandboxed │
└─────────────────────────────┬───────────────────────────────┘ ▼
┌─────────────────────────────────────────────────────────────┐ │ .chenu
THREAD │ │ (Atomic Unit • Versioned • Auditable) │ │ ↓ │ │ VERSIONING &
DIFF → LEDGER & AUDIT │ │ ↓ │ │ THREAD LINKS (Graph Model) │
└─────────────────────────────┬───────────────────────────────┘ ▼
┌─────────────────────────────────────────────────────────────┐ │
WORKSPACE ENGINE │ │ (Internal/External Data ↔ Thread ↔ UI Feedback) │
└─────────────────────────────────────────────────────────────┘

Component Legend

  ----------------------- -----------------------------------------------
  **Component**           **Role**

  **UI (3 Surfaces)**     Nova (governance) • Context (info) • Workspace
                          (action)

  **Governance Core**     Scope enforcement, budget control, permission
                          check, ledger

  **ACM**                 Pre-execution validation: encoding level,
                          scope, action check

  **.chenu Thread**       Atomic unit of work, versioned, auditable,
                          linked
  ----------------------- -----------------------------------------------

***\"Architecture is visible. Flow is explicit. Governance is
everywhere.\"***

SPEC 18: ENCODING HANDBOOK (MINIMAL)

*Encode user intent into a compact, governed, reversible format to
reduce token cost, ambiguity, and execution risk. Encoding = semantic
calculator.*

Encoding Pipeline (Fixed)

Human Intent → Intent Compression → Semantic Encoding (L1) →
Auto-Optimization → (Optional) Binary Encoding (L2) → Agents → Decoding
→ User ⚠ No step is automatic without consent.

Core Encoding Format

KEY=VALUE \| Arrays: \[A,B,C\] \| Flags: 1/0 \| No free text.

Mandatory Keys

**ACT (Action) \| SRC (Source) \| SCOPE (Boundary) \| MODE (Behavior) ⚠
Execution is BLOCKED if any mandatory key is missing.**

Common Keys (v1)

  ----------- -----------------------------------------------------------
  **Key**     **Values**

  **ACT**     SUM \| EXT \| STR \| CMP \| ANA \| GEN \| DEC \| PLN \| REF
              \| VER \| MAP \| CLS

  **SRC**     SEL \| DOC \| WS \| MTG \| EXT \| MIX

  **SCOPE**   SEL \| DOC \| WS \| MTG \| LOCK

  **MODE**    ANA \| PREP \| DRAFT \| CHECK \| NONE

  **FOCUS**   FACT \| RISK \| CONS \| OPP \| NEXT \| DEC \| GAP \| OPT

  **OUT**     LIST \| TAB \| TREE \| FLOW \| TEXT \| JSON

  **FLAGS**   RW \| UNC \| SENS \| TRACE (0/1)

  **LEN**     XS \| S \| M \| L \| XL
  ----------- -----------------------------------------------------------

Canonical Example

ACT=SUM SRC=DOC SCOPE=SEL FOCUS=\[RISK,CONS,NEXT\] MODE=ANA OUT=LIST
RW=0 TRACE=1

Encoding Levels

  ----------- -------------------------- ---------------------------------
  **Level**   **Type**                   **Notes**

  **L0**      Human language only        No encoding

  **L1**      **Semantic Encoding**      Default --- human-readable

  **L2**      Binary Encoding            Expert only --- derived, never
                                         authored
  ----------- -------------------------- ---------------------------------

Governance Rules (Absolute)

-   **Encoding never executes**

-   **Encoding never decides**

-   Encoding never hides meaning

-   **User always confirms**

***\"Encode intent. Preserve meaning. Minimize cost.\"***

**🔒 MVP OFFICIAL FREEZE 🔒**

Freeze Status

**MVP architecture is OFFICIALLY FROZEN. No new concepts may be added.
Only implementation, stabilization, and documentation allowed.**

Change Policy

  ----------------------------------- -----------------------------------
  **✓ ALLOWED**                       **✗ NOT ALLOWED**

  Bug fixes • Performance •           Conceptual changes • New specs •
  Documentation                       Governance violations
  ----------------------------------- -----------------------------------

ALL 18 CANONICAL STATEMENTS

**18 SPECIFICATIONS \| 18 STATEMENTS \| 6 LAYERS \| MVP FROZEN**

**L1: Foundation (1-6)**

*1. \"CHE·NU governs what you decide to bring back.\"*

*2. \"Intent is compressed. Meaning is preserved. Cost is controlled.\"*

*3. \[Dictionary provides the vocabulary\]*

*4. \"Suggestions guide understanding. Decisions remain human.\"*

*5. \"Binary encoding is invisible, reversible, and never
authoritative.\"*

*6. \"Humans write meaning. Systems compress intent. CHE·NU shows
both.\"*

**L2: Quality (7-9)**

*7. \"Quality is visible. Decisions remain human.\"*

*8. \"Agents declare capabilities. Systems enforce limits. No
guessing.\"*

*9. \"Optimization reduces cost. Meaning remains intact. Control remains
human.\"*

**L3: UX (10-12)**

*10. \"Transparency is not decoration. It is governance made visible.\"*

*11. \"Patterns are optimized together. Intent remains individual.\"*

*12. \"Presets accelerate clarity. Control always remains human.\"*

**L4: SDK (13-14)**

*13. \"Agents are tools. They do not think for the system. They do not
act for the user.\"*

*14. \"Internal data deserves the same respect as intelligence.\"*

**L5: Threads (15-16)**

*15. \"A .chenu file is not a conversation. It is a governed history of
intent and action.\"*

*16. \"The thread is the unit. The tree is the navigation. Meaning lives
in the thread.\"*

**L6: Reference (17-18)**

*17. \"Architecture is visible. Flow is explicit. Governance is
everywhere.\"*

*18. \"Encode intent. Preserve meaning. Minimize cost.\"*

Architecture Summary

+-----------+-----------+-----------+-----------+-----------+-----------+
| **L1**    | **L2**    | **L3**    | **L4**    | **L5**    | **L6**    |
|           |           |           |           |           |           |
| F         | Quality   | UX        | SDK       | Threads   | Reference |
| oundation |           |           |           |           |           |
+-----------+-----------+-----------+-----------+-----------+-----------+
| 1-6       | 7-9       | 10-12     | 13-14     | 15-16     | 17-18     |
+-----------+-----------+-----------+-----------+-----------+-----------+

**--- END OF CANONICAL SPECIFICATIONS v8 FINAL ---**

**🔒 MVP OFFICIALLY FROZEN 🔒**

CHE·NU v27 --- Governed Intelligence OS

Pro-Service Construction • Brossard, Québec

14 décembre 2025
