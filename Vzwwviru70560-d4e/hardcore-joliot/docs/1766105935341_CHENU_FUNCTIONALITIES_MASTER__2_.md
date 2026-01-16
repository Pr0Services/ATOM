# CHE·NU™ FUNCTIONALITIES DEEP SPECIFICATION

## Canonical Functional Reference — Source of Truth

---

> ⚠️ **IMPORTANT — RULES FOR THIS DOCUMENT**
> 
> - **DO NOT** change the structure
> - **DO NOT** merge sections
> - **DO NOT** simplify or remove content
> - **EXTEND**, illustrate, explain
> - **KEEP** all functionalities listed
> - This document is **FROZEN** as canonical reference

---

## 📋 METADATA

| Field | Value |
|-------|-------|
| **Title** | CHE·NU™ Functionalities Deep Specification |
| **Version** | Canonical v1.0 |
| **Status** | 🔒 FREEZE |
| **Date** | 2024 |
| **Audience** | Product · Development · Investor · Design · Operations |
| **Source** | CHE·NU System Canonical Architecture |
| **Classification** | Strategic Reference Document |
| **Languages** | Primary: English | Secondary: French annotations |

---

# PART I: FOUNDATION

---

## 1. INTRODUCTION — FUNCTIONAL SCOPE OF CHE·NU

### 1.1 What This Document Is

This document serves as the **exhaustive functional reference** for CHE·NU™ — the Governed Intelligence Operating System. It provides:

#### Comprehensive Coverage
- **Feature-by-feature** documentation of all system capabilities
- **Menu-by-menu** breakdown of navigation and interaction points
- **Option-by-option** specification of configurable elements
- **Flow-by-flow** description of user journeys and state transitions

#### Purpose & Usage
| Audience | Primary Use |
|----------|-------------|
| **Product Team** | Feature specification, roadmap planning, prioritization |
| **Development Team** | Implementation reference, API design, technical specifications |
| **Investors** | Capability overview, market differentiation, value proposition |
| **Design Team** | UX patterns, interaction models, visual hierarchy |
| **Operations** | Deployment planning, support documentation, training materials |

#### Document Hierarchy
```
CHENU_FUNCTIONALITIES_MASTER.md (This Document)
    └── Source of Truth
         ├── PDF: System Manual (80-120 pages)
         ├── PDF: Investor Version (30-40 pages)
         ├── PDF: User Guide (50-60 pages)
         ├── PDF: Technical Reference (100+ pages)
         └── PDF: XR/Design Specification (40-50 pages)
```

### 1.2 What CHE·NU IS

CHE·NU is a **Governed Intelligence Operating System** that:

#### Core Identity
1. **Unifies life management** across personal, professional, and institutional contexts
2. **Governs AI interactions** with transparency, budgets, and human oversight
3. **Structures information** through 8 canonical spheres and consistent bureau design
4. **Enables collaboration** between humans and AI agents with clear roles
5. **Provides spatial organization** for both 2D interfaces and XR environments

#### Functional Pillars
| Pillar | Description | Key Features |
|--------|-------------|--------------|
| **Context Management** | Know where you are before acting | Spheres, Identities, Projects |
| **Governed Execution** | Validate before executing | Laws, Budgets, Approvals |
| **Collaborative Intelligence** | Humans + AI working together | Agents, Orchestration, Threads |
| **Transparent Economics** | See and control AI costs | Tokens, Budgets, Tracking |
| **Spatial Organization** | Everything has a place | Bureaus, Workspaces, Universe Views |

### 1.3 What CHE·NU IS NOT

#### Explicit Exclusions

| CHE·NU is NOT | Explanation |
|---------------|-------------|
| **A single-purpose app** | Not just tasks, not just notes, not just chat |
| **A chatbot** | Nova guides and assists; she doesn't just chat |
| **A collection of disconnected tools** | Unified system, not a suite of apps |
| **A cryptocurrency platform** | Tokens are internal credits, not tradeable assets |
| **A social network** | Community features exist but don't define the system |
| **An automation-first tool** | Governance always precedes automation |
| **A replacement for human judgment** | AI suggests, humans decide |

#### Differentiation from Market Categories
```
┌─────────────────────────────────────────────────────────────┐
│                    CHE·NU POSITIONING                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Productivity Apps    AI Assistants    Operating Systems   │
│   (Notion, Asana)      (ChatGPT, etc.)  (macOS, Windows)    │
│         │                    │                │             │
│         └────────────────────┼────────────────┘             │
│                              │                              │
│                              ▼                              │
│                    ┌─────────────────┐                      │
│                    │    CHE·NU™      │                      │
│                    │   Governed      │                      │
│                    │   Intelligence  │                      │
│                    │   Operating     │                      │
│                    │   System        │                      │
│                    └─────────────────┘                      │
│                                                             │
│   Combines structure, intelligence, and governance          │
│   in a single unified system                                │
└─────────────────────────────────────────────────────────────┘
```

---

# PART II: NAVIGATION & CORE INTERFACES

---

## 2. GLOBAL NAVIGATION & MENUS

### 2.1 Diamond Hub

The Diamond Hub (◆) is the **central convergence point** of CHE·NU — always visible, always reflecting current state.

#### Core Principle
> **The Diamond Hub SIGNALS only. It does NOT execute.**
> It reflects system state but triggers no actions by itself.

#### Diamond Hub Components

| Component | Type | Function | Interaction |
|-----------|------|----------|-------------|
| **Diamond Icon** | Visual | Central anchor, rotation indicates activity | Click: Open context menu |
| **Context Label** | Text | Shows: Identity • Sphere • [Project] | Click: Open context switcher |
| **State Indicator** | Badge | Current state (Entry/Context/Action/Workspace) | Read-only |
| **Alert Counter** | Number | Count of pending alerts requiring attention | Click: Open alerts panel |
| **Meeting Counter** | Number | Upcoming meetings within 24h | Click: Open meetings view |
| **Task Counter** | Number | Tasks due today | Click: Open task list |
| **Hub Toggles** | Buttons | Show/hide Communication, Navigation, Workspace | Click: Toggle visibility |
| **Governance Badge** | Icon | Confirms governed mode is active | Hover: Show governance status |

#### Diamond Hub States

```
┌─────────────────────────────────────────────────────────────┐
│                    DIAMOND HUB STATES                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐ │
│  │  IDLE    │    │  ACTIVE  │    │ WORKING  │    │ ALERT  │ │
│  │    ◆     │    │    ◇     │    │    ◈     │    │   ⚠◆   │ │
│  │ Static   │    │ Rotating │    │ Pulsing  │    │ Urgent │ │
│  └──────────┘    └──────────┘    └──────────┘    └────────┘ │
│                                                              │
│  IDLE: No activity, system ready                            │
│  ACTIVE: Processing request or navigation                   │
│  WORKING: Agent or workspace actively operating             │
│  ALERT: Requires immediate attention                        │
└─────────────────────────────────────────────────────────────┘
```

#### Diamond Hub Visual Zones

```
┌─────────────────────────────────────────────────────────────┐
│  ┌─────┐  Personal • Business Sphere        [Entry]         │
│  │  ◆  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  └─────┘                                                     │
│                                                              │
│  🔔 3   📹 2   ✅ 5              💬  🧭  🔧      🛡️ Governed │
│  ─────────────────              ───────────      ─────────── │
│  Status Counters                Hub Toggles      Governance  │
└─────────────────────────────────────────────────────────────┘
```

#### Interaction Patterns

| Action | Trigger | Result |
|--------|---------|--------|
| **Single Click on Diamond** | Left click | Open quick action menu |
| **Double Click on Diamond** | Double left click | Return to Action Bureau |
| **Long Press on Diamond** | Hold 1 second | Open context switcher |
| **Hover on Diamond** | Mouse hover | Show full context tooltip |
| **Swipe on Diamond** (mobile) | Swipe gesture | Cycle through hubs |

### 2.2 Global Search

#### Search Modes

CHE·NU provides multiple search paradigms to match user intent:

| Mode | Scope | Use Case | Activation |
|------|-------|----------|------------|
| **Scoped Search** | Current context only | Find within current sphere/project | Default when in context |
| **Sphere Search** | Single sphere | Find across all projects in sphere | Select sphere in search |
| **Identity Search** | All spheres of identity | Find across all contexts of one identity | Select identity in search |
| **Global Search** | Everything accessible | Find anywhere user has permission | Uncheck scope filters |
| **Agent-Assisted Search** | AI-enhanced | Natural language queries | Enable AI toggle |

#### Search Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Search CHE·NU...                              ⌘K        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SCOPE: ☑️ Current Context  ☐ All Spheres  ☐ Global         │
│                                                              │
│  TYPE:  ☑️ All  ☐ Notes  ☐ Tasks  ☐ Threads  ☐ Files        │
│                                                              │
│  AI: ☐ Enable agent-assisted search                         │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  RECENT SEARCHES                                             │
│  • "Q3 budget report"                                        │
│  • "meeting notes marketing"                                 │
│  • "client proposal draft"                                   │
├─────────────────────────────────────────────────────────────┤
│  SUGGESTED                                                   │
│  📄 Q3 Budget Final.chenu          Business > Finance        │
│  ✅ Review budget allocations       Due today                │
│  🧵 Budget discussion thread        3 new messages           │
└─────────────────────────────────────────────────────────────┘
```

#### Search Result Types

| Type | Icon | Preview Content | Actions |
|------|------|-----------------|---------|
| **Note** | 📝 | Title + excerpt | Open, Edit, Share |
| **Task** | ✅ | Title + due date + status | Open, Complete, Reschedule |
| **Thread** | 🧵 | Title + last message preview | Open, Reply, Archive |
| **Document** | 📄 | Title + excerpt | Open, Edit, Export |
| **Project** | 📁 | Name + progress | Open, View details |
| **Agent** | 🤖 | Name + status | Open, Configure, Call |
| **Meeting** | 📹 | Title + time + participants | Open, Join, Reschedule |
| **File** | 📎 | Filename + type + size | Open, Download, Move |

#### Agent-Assisted Search

When enabled, the search becomes conversational:

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 "Find all documents related to the Smith project        │
│      that were modified last week"                          │
├─────────────────────────────────────────────────────────────┤
│  🤖 Nova: I found 7 documents matching your query:          │
│                                                              │
│  📄 Smith Project Proposal v3        Modified: Mon          │
│  📄 Smith Contract Draft             Modified: Tue          │
│  📄 Smith Meeting Notes 03/15        Modified: Wed          │
│  📄 Smith Budget Revision            Modified: Wed          │
│  📄 Smith Timeline Update            Modified: Thu          │
│  📄 Smith Deliverables List          Modified: Fri          │
│  📄 Smith Final Review               Modified: Fri          │
│                                                              │
│  Would you like me to create a summary thread of these?     │
│                                                              │
│  [Yes, create thread]  [Show in folder]  [Refine search]   │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Context Switcher

The Context Switcher provides structured navigation through the CHE·NU hierarchy.

#### Context Hierarchy

```
IDENTITY (Who)
    └── SPHERE (What domain)
            └── PROJECT (What initiative) [Optional]
                    └── WORKSPACE (What specific work)
```

#### Context Switcher Interface

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT SWITCHER                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  IDENTITY                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ 🏠 Personal │  │ 💼 Business │  │ 🏛️ Govern.  │          │
│  │   Jo B.     │  │ Pro Service │  │   Tax ID    │          │
│  │      ✓      │  │             │  │             │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  SPHERE                                                      │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐                    │
│  │ 🏠    │ │ 💼    │ │ 🎨    │ │ 🤝    │                    │
│  │Person.│ │Busine.│ │Studio │ │ Team  │                    │
│  │   ✓   │ │       │ │       │ │       │                    │
│  └───────┘ └───────┘ └───────┘ └───────┘                    │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐                    │
│  │ 👥    │ │ 📱    │ │ 🎬    │ │ 🏛️    │                    │
│  │Commun.│ │Social │ │Entert.│ │Govern.│                    │
│  └───────┘ └───────┘ └───────┘ └───────┘                    │
│                                                              │
│  PROJECT (Optional)                                          │
│  ☐ All projects  ○ Home Renovation  ○ Health Goals          │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  CURRENT CONTEXT SUMMARY                                     │
│  Personal > Personal Sphere > All Projects                   │
│  📊 3 urgent tasks  📹 1 meeting today  🔔 2 alerts          │
├─────────────────────────────────────────────────────────────┤
│            [Cancel]                    [Confirm Context]     │
└─────────────────────────────────────────────────────────────┘
```

#### Context Switching Rules

| Rule | Description |
|------|-------------|
| **Identity Switch** | Clears sphere, project, and workspace selection |
| **Sphere Switch** | Clears project and workspace selection |
| **Project Switch** | Clears workspace selection |
| **Validation Required** | Context must be confirmed before proceeding to Action Bureau |
| **Auto-Select** | If only one option exists, system pre-fills (marked "Auto") |
| **Never Skip** | Context Bureau is NEVER bypassed, even with auto-selection |

#### Context Persistence

| Scenario | Behavior |
|----------|----------|
| **Session Restart** | Restores last confirmed context |
| **App Close** | Saves current context to local storage |
| **Identity Change** | Saves previous identity's last context |
| **Timeout** | Context remains stable; no auto-logout from context |

---

# PART III: THREADS & FILE SYSTEM

---

## 3. THREADS & .CHENU FILES (SYSTEM BACKBONE)

Threads and .chenu files form the **persistent memory and communication backbone** of CHE·NU.

### 3.1 Threads

Threads are **first-class objects** in CHE·NU — not just chat histories, but structured containers of thought, decision, and collaboration.

#### Thread Definition

> A **Thread** is a persistent, governed line of thought that:
> - Has an owner and defined scope
> - Has a token budget
> - Records decisions and their rationale
> - Is fully auditable
> - Can include both human and AI participants

#### Thread Types

| Type | Visibility | Participants | Use Case |
|------|------------|--------------|----------|
| **Private Thread** | Owner only | Owner + Agents | Personal thinking, planning |
| **Shared Thread** | Invited users | Multiple humans + Agents | Team collaboration |
| **Public Thread** | Community | Anyone in sphere | Open discussion, Q&A |
| **Agent Thread** | Owner + System | User ↔ Agent | Task execution, assistance |
| **System Thread** | System only | Nova + System | Audit, governance logs |

#### Thread Structure

```
┌─────────────────────────────────────────────────────────────┐
│  🧵 THREAD: Q4 Marketing Strategy                           │
├─────────────────────────────────────────────────────────────┤
│  Owner: Jo Bouchard                                          │
│  Sphere: 💼 Business > Marketing Project                     │
│  Created: 2024-03-15                                         │
│  Status: Active                                              │
│  Token Budget: 5,000 / 10,000 used                           │
├─────────────────────────────────────────────────────────────┤
│  PARTICIPANTS                                                │
│  👤 Jo Bouchard (Owner)                                      │
│  👤 Marie Dupont (Collaborator)                              │
│  🤖 Marketing Agent (Assigned)                               │
│  ✦ Nova (System)                                             │
├─────────────────────────────────────────────────────────────┤
│  PERMISSIONS                                                 │
│  ☑️ Read: All participants                                   │
│  ☑️ Write: Owner, Marie                                      │
│  ☑️ Decide: Owner only                                       │
│  ☐ Public: No                                                │
├─────────────────────────────────────────────────────────────┤
│  LINKED ITEMS                                                │
│  📄 Marketing Plan v3.docx                                   │
│  ✅ Task: Finalize campaign budget                           │
│  📹 Meeting: Marketing sync (03/20)                          │
└─────────────────────────────────────────────────────────────┘
```

#### Thread Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    THREAD LIFECYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   CREATE ──► ACTIVE ──► PAUSE ──► ARCHIVE ──► DELETE        │
│      │          │          │          │          │          │
│      │          │          │          │          │          │
│      ▼          ▼          ▼          ▼          ▼          │
│   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐          │
│   │New  │   │Live │   │Hold │   │Read │   │Gone │          │
│   │Empty│   │Work │   │Wait │   │Only │   │     │          │
│   └─────┘   └─────┘   └─────┘   └─────┘   └─────┘          │
│                                                              │
│   Actions available at each stage:                           │
│   CREATE: Set name, scope, budget, participants              │
│   ACTIVE: Message, decide, link, share                       │
│   PAUSE:  Resume, archive, transfer                          │
│   ARCHIVE: Export, restore, delete                           │
│   DELETE: Permanent removal (with audit trail)               │
└─────────────────────────────────────────────────────────────┘
```

#### Thread Permissions Matrix

| Permission | Owner | Collaborator | Observer | Agent | System |
|------------|-------|--------------|----------|-------|--------|
| Read messages | ✅ | ✅ | ✅ | ✅ | ✅ |
| Write messages | ✅ | ✅ | ❌ | ✅* | ✅* |
| Make decisions | ✅ | ❌ | ❌ | ❌ | ❌ |
| Add participants | ✅ | ❌ | ❌ | ❌ | ❌ |
| Change permissions | ✅ | ❌ | ❌ | ❌ | ✅* |
| Archive thread | ✅ | ❌ | ❌ | ❌ | ✅* |
| Delete thread | ✅ | ❌ | ❌ | ❌ | ❌ |
| Export thread | ✅ | ✅ | ❌ | ❌ | ✅ |

*With governance approval

### 3.2 .chenu Files

The `.chenu` format is CHE·NU's **native file format** — a structured, portable container for intelligence artifacts.

#### .chenu File Definition

> A **.chenu file** is a self-contained, portable artifact that packages:
> - Complete context of creation
> - Full decision history
> - Version chain
> - References and links
> - Human AND machine readable content

#### .chenu File Structure

```yaml
# EXAMPLE: project_plan.chenu

chenu_version: "1.0"
file_type: "document"
created: "2024-03-15T10:30:00Z"
modified: "2024-03-18T14:22:00Z"

# CONTEXT
context:
  identity: "business"
  identity_name: "Pro Service Inc"
  sphere: "business"
  project: "client-portal-v2"
  creator: "jo.bouchard"

# METADATA
metadata:
  title: "Client Portal v2 - Project Plan"
  description: "Complete project plan for portal redesign"
  tags: ["project", "planning", "client", "portal"]
  language: "en"
  encoding_score: 0.85

# PERMISSIONS
permissions:
  owner: "jo.bouchard"
  read: ["team-dev", "team-design"]
  write: ["jo.bouchard", "marie.dupont"]
  share: "internal"

# GOVERNANCE
governance:
  budget_allocated: 2000
  budget_spent: 450
  laws_applied: ["data-privacy", "client-confidential"]
  approvals:
    - type: "content"
      approver: "jo.bouchard"
      date: "2024-03-16"

# VERSIONS
versions:
  - version: "1.0"
    date: "2024-03-15"
    author: "jo.bouchard"
    changes: "Initial draft"
  - version: "1.1"
    date: "2024-03-16"
    author: "marie.dupont"
    changes: "Added timeline section"
  - version: "2.0"
    date: "2024-03-18"
    author: "jo.bouchard"
    changes: "Major revision after client feedback"

# REFERENCES
references:
  - type: "thread"
    id: "thread-123"
    title: "Portal planning discussion"
  - type: "meeting"
    id: "meeting-456"
    title: "Client kickoff call"
  - type: "document"
    id: "doc-789"
    title: "Requirements document"

# DECISIONS
decisions:
  - id: "dec-001"
    date: "2024-03-16"
    decision: "Use React for frontend"
    rationale: "Team expertise, client preference"
    decided_by: "jo.bouchard"
  - id: "dec-002"
    date: "2024-03-17"
    decision: "Launch date: Q2 2024"
    rationale: "Client timeline requirement"
    decided_by: "jo.bouchard"

# CONTENT
content:
  format: "markdown"
  body: |
    # Client Portal v2 - Project Plan
    
    ## Overview
    [Content here...]
    
    ## Timeline
    [Content here...]
    
    ## Resources
    [Content here...]

# ENCODING (for agent optimization)
encoding:
  compressed: true
  dictionary_id: "business-project-v1"
  token_estimate: 1250
  agent_compatible: ["gpt-4", "claude-3", "local-llm"]
```

#### .chenu File Usage

| Use Case | Description | Example |
|----------|-------------|---------|
| **Memory** | Store and recall context | "What did we decide about the timeline?" |
| **Audit** | Complete decision trail | Review all changes and approvals |
| **Agent Seed** | Initialize agent with context | Agent reads .chenu before task |
| **Handoff** | Transfer work between people/agents | New team member gets full context |
| **Export** | Portable format for sharing | Send to external party |
| **Archive** | Long-term storage | Compliance and records |

#### File Type Extensions

| Extension | Type | Content |
|-----------|------|---------|
| `.chenu` | Generic | Any CHE·NU artifact |
| `.chenu.doc` | Document | Rich text document |
| `.chenu.note` | Note | Quick capture note |
| `.chenu.task` | Task | Task definition |
| `.chenu.thread` | Thread | Thread export |
| `.chenu.meeting` | Meeting | Meeting record |
| `.chenu.data` | Data | Structured data |
| `.chenu.agent` | Agent | Agent configuration |

---

# PART IV: ENCODING & OPTIMIZATION

---

## 4. ENCODING & OPTIMIZATION ENGINE

The Encoding Engine is CHE·NU's **core intellectual property** — a system for optimizing AI interactions through intelligent compression and formatting.

### 4.1 Semantic Encoding

#### Purpose
Transform verbose human input into optimized formats that:
- Reduce token consumption
- Clarify intent
- Enforce scope boundaries
- Improve agent performance

#### Encoding Techniques

| Technique | Description | Reduction |
|-----------|-------------|-----------|
| **Context Compression** | Remove redundant context already known to agent | 30-50% |
| **Token Reduction** | Replace verbose phrases with efficient alternatives | 20-30% |
| **Dictionary Encoding** | Map common terms to short codes | 10-20% |
| **Structure Optimization** | Reorganize for better LLM processing | 15-25% |
| **Binary Encoding** (Optional) | Compact binary representation for storage | 50-70% |

#### Encoding Example

```
┌─────────────────────────────────────────────────────────────┐
│                    ENCODING EXAMPLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ORIGINAL INPUT (127 tokens):                                │
│  "Hello, I would like you to help me create a detailed       │
│  marketing plan for my new product launch. The product is    │
│  a mobile application for personal finance management. The   │
│  target audience is millennials aged 25-35 who are           │
│  interested in saving money and investing. Please include    │
│  sections for social media strategy, content marketing,      │
│  and paid advertising budget recommendations."               │
│                                                              │
│  ENCODED INPUT (43 tokens):                                  │
│  "[CTX:business/marketing/product-launch]                    │
│  REQ: marketing_plan                                         │
│  PRODUCT: mobile_app | personal_finance                      │
│  AUDIENCE: millennials | 25-35 | savings+investing           │
│  SECTIONS: social_media, content_mktg, paid_ads_budget"      │
│                                                              │
│  REDUCTION: 66%                                              │
│  ENCODING SCORE: 0.92                                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Encoding Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                  ENCODING LIFECYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐│
│  │  RAW     │    │CONDENSED │    │  AGENT   │    │DECODED ││
│  │  INPUT   │───►│   FORM   │───►│COMPATIBLE│───►│ OUTPUT ││
│  └──────────┘    └──────────┘    └──────────┘    └────────┘│
│                                                              │
│  Stage 1: RAW INPUT                                          │
│  - User's natural language                                   │
│  - Verbose, contextual                                       │
│  - May include irrelevant information                        │
│                                                              │
│  Stage 2: CONDENSED FORM                                     │
│  - Context markers applied                                   │
│  - Redundancy removed                                        │
│  - Structure optimized                                       │
│                                                              │
│  Stage 3: AGENT-COMPATIBLE                                   │
│  - Formatted for specific LLM                                │
│  - Tokens minimized                                          │
│  - Scope enforced                                            │
│                                                              │
│  Stage 4: DECODED OUTPUT                                     │
│  - Agent response                                            │
│  - Expanded back to human-readable                           │
│  - Context restored                                          │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Quality & Compatibility

#### Encoding Quality Score

| Score Range | Quality | Meaning |
|-------------|---------|---------|
| **0.90 - 1.00** | Excellent | Optimal compression, no information loss |
| **0.75 - 0.89** | Good | High compression, minimal information loss |
| **0.60 - 0.74** | Acceptable | Moderate compression, some clarification may be needed |
| **0.40 - 0.59** | Fair | Low compression, ambiguity possible |
| **< 0.40** | Poor | Minimal compression, requires review |

#### Agent Compatibility Matrix

| Agent Type | Encoding Support | Optimal Format | Notes |
|------------|------------------|----------------|-------|
| **GPT-4** | Full | Structured JSON | Best with explicit structure |
| **Claude-3** | Full | Markdown + context | Prefers natural flow |
| **Local LLM** | Partial | Simplified structure | May need dictionary |
| **Specialized Agent** | Varies | Agent-specific | Check compatibility |

#### LLM Compatibility Flags

```
encoding:
  compatible_llms:
    - name: "gpt-4"
      version: "turbo"
      support: "full"
      format: "json_structured"
    - name: "claude-3"
      version: "opus"
      support: "full"
      format: "markdown_contextual"
    - name: "llama-3"
      version: "70b"
      support: "partial"
      format: "simple_structured"
      notes: "Requires dictionary file"
```

---

# PART V: WORKSPACE SYSTEM

---

## 5. WORKSPACE CAPABILITIES (UNIVERSAL)

Workspaces are where **actual work happens** in CHE·NU. They provide consistent environments across all spheres.

### 5.1 Universal Workspace Types

| Type | Icon | Primary Use | Key Features |
|------|------|-------------|--------------|
| **Note** | 📝 | Quick capture | Fast creation, tags, links |
| **Document** | 📄 | Rich content | Formatting, sections, media |
| **Table** | 📊 | Structured data | Columns, formulas, views |
| **Board** | 📋 | Visual organization | Kanban, columns, drag-drop |
| **Canvas** | 🎨 | Freeform | Drawing, diagrams, spatial |

#### Note Workspace

```
┌─────────────────────────────────────────────────────────────┐
│  📝 Quick Note                               [Pin] [Share]   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Meeting with client tomorrow at 2pm                         │
│  - Discuss Q3 projections                                    │
│  - Review contract terms                                     │
│  - Address support tickets                                   │
│                                                              │
│  #meeting #client #q3                                        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  Created: Today 10:23 AM                                     │
│  Sphere: 💼 Business                                         │
│  Links: 📹 Meeting (tomorrow)  ✅ Prep presentation          │
└─────────────────────────────────────────────────────────────┘
```

#### Document Workspace

```
┌─────────────────────────────────────────────────────────────┐
│  📄 Project Proposal                    [Draft] [◆] [Share] │
├─────────────────────────────────────────────────────────────┤
│  📑 Outline  │  B I U  │ H1 H2 H3 │ 📷 📎 📊 │ 🤖 AI       │
├──────────────┴─────────────────────────────────────────────┤│
│                                                              │
│  # Project Proposal: Client Portal Redesign                  │
│                                                              │
│  ## Executive Summary                                        │
│  This proposal outlines the comprehensive redesign of...     │
│                                                              │
│  ## Objectives                                               │
│  1. Improve user experience                                  │
│  2. Increase engagement by 40%                               │
│  3. Reduce support tickets by 25%                            │
│                                                              │
│  ## Timeline                                                 │
│  | Phase | Duration | Deliverable |                         │
│  |-------|----------|-------------|                         │
│  | Discovery | 2 weeks | Requirements doc |                 │
│  | Design | 4 weeks | UI mockups |                          │
│  | Development | 8 weeks | Working prototype |              │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  Word count: 2,450  │  Last saved: 2 min ago  │  v2.3       │
└─────────────────────────────────────────────────────────────┘
```

#### Table Workspace

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Budget Tracker                         [Filter] [Views] │
├─────────────────────────────────────────────────────────────┤
│  + Add row  │  Σ Sum  │  ƒ Formula  │  🔽 Sort  │  📤 Export│
├─────────────────────────────────────────────────────────────┤
│  │ Category    │ Budgeted │ Actual   │ Variance │ Status   │
│  ├─────────────┼──────────┼──────────┼──────────┼──────────┤
│  │ Marketing   │ $50,000  │ $47,500  │ +$2,500  │ ✅ Under │
│  │ Development │ $120,000 │ $125,000 │ -$5,000  │ ⚠️ Over  │
│  │ Operations  │ $30,000  │ $28,000  │ +$2,000  │ ✅ Under │
│  │ Support     │ $25,000  │ $24,500  │ +$500    │ ✅ Under │
│  ├─────────────┼──────────┼──────────┼──────────┼──────────┤
│  │ TOTAL       │ $225,000 │ $225,000 │ $0       │ ✅ On    │
└─────────────────────────────────────────────────────────────┘
```

#### Board Workspace

```
┌─────────────────────────────────────────────────────────────┐
│  📋 Sprint Board                          [+ Column] [Filter]│
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📥 Backlog    │  🔄 In Progress  │  👀 Review    │  ✅ Done │
│  ────────────  │  ──────────────  │  ──────────   │  ─────── │
│  ┌──────────┐  │  ┌──────────┐    │  ┌──────────┐ │ ┌──────┐ │
│  │Auth page │  │  │Dashboard │    │  │API docs  │ │ │Login │ │
│  │@marie    │  │  │@jo       │    │  │@team     │ │ │      │ │
│  │3 pts     │  │  │5 pts     │    │  │2 pts     │ │ │✓     │ │
│  └──────────┘  │  └──────────┘    │  └──────────┘ │ └──────┘ │
│  ┌──────────┐  │  ┌──────────┐    │               │ ┌──────┐ │
│  │Settings  │  │  │Profile   │    │               │ │Signup│ │
│  │@pierre   │  │  │@marie    │    │               │ │      │ │
│  │2 pts     │  │  │3 pts     │    │               │ │✓     │ │
│  └──────────┘  │  └──────────┘    │               │ └──────┘ │
│                │                   │               │          │
│  4 items       │  2 items         │  1 item       │ 2 items  │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Workspace Transformations

Workspaces can be **transformed** between types while preserving content:

| From | To | Transformation |
|------|----|----------------|
| **Note** | Document | Expand formatting, add structure |
| **Note** | Task | Extract action items |
| **Document** | Report | Add executive summary, format |
| **Document** | Presentation | Extract key points to slides |
| **Table** | Dashboard | Add visualizations, charts |
| **Table** | Report | Generate analysis narrative |
| **Board** | Table | Flatten to rows/columns |
| **Any** | .chenu | Package with full context |

#### Transformation Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🔄 TRANSFORM WORKSPACE                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Current: 📝 Meeting Notes                                   │
│                                                              │
│  Transform to:                                               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  📄 Document                                          │   │
│  │  Expand to full document with sections                │   │
│  │  Preserves: All content, links                        │   │
│  │  Adds: Headers, table of contents                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ✅ Task List                                         │   │
│  │  Extract action items as tasks                        │   │
│  │  Preserves: Action items, assignees, dates            │   │
│  │  Creates: Individual task cards                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  📦 .chenu Package                                    │   │
│  │  Export as portable artifact                          │   │
│  │  Preserves: Everything + context + history            │   │
│  │  Creates: Self-contained .chenu file                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│            [Cancel]                    [Transform]           │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Versioning

Every workspace maintains a complete version history with powerful tools for managing changes.

#### Version States

```
┌─────────────────────────────────────────────────────────────┐
│                    VERSION STATES                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│  │  DRAFT   │───►│ STAGING  │───►│  REVIEW  │               │
│  │ (Work)   │    │(Preview) │    │(Approve) │               │
│  └──────────┘    └──────────┘    └──────────┘               │
│       │               │               │                      │
│       │               │               ▼                      │
│       │               │          ┌──────────┐               │
│       │               │          │PUBLISHED │               │
│       │               │          │(Final)   │               │
│       │               │          └──────────┘               │
│       │               │               │                      │
│       ▼               ▼               ▼                      │
│  ┌──────────────────────────────────────────┐               │
│  │            VERSION HISTORY               │               │
│  │  v1.0 → v1.1 → v2.0 → v2.1 → v3.0       │               │
│  └──────────────────────────────────────────┘               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Versioning Operations

| Operation | Description | Availability |
|-----------|-------------|--------------|
| **Save Draft** | Save current work without publishing | Always |
| **Submit to Staging** | Move to preview/review ready state | From Draft |
| **Request Review** | Send to approver for validation | From Staging |
| **Approve** | Mark as approved, publish | From Review |
| **Reject** | Send back with feedback | From Review |
| **Fork** | Create parallel version | Any state |
| **Merge** | Combine forked versions | Between forks |
| **Rollback** | Revert to previous version | Published versions |
| **Discard** | Delete without saving | Draft only |

#### Diff View

```
┌─────────────────────────────────────────────────────────────┐
│  DIFF: v2.0 ↔ v2.1                          [◄ Prev] [Next ►]│
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  VERSION 2.0                │  VERSION 2.1                   │
│  ─────────────────────────  │  ─────────────────────────     │
│                             │                                │
│  ## Budget                  │  ## Budget                     │
│                             │                                │
│  Total: $50,000            │  Total: $55,000    [CHANGED]   │
│                             │                                │
│  - Marketing: $20,000      │  - Marketing: $20,000          │
│  - Development: $25,000    │  - Development: $28,000 [+]    │
│  - Operations: $5,000      │  - Operations: $5,000          │
│                             │  - Support: $2,000   [NEW]     │
│                             │                                │
│  ## Timeline               │  ## Timeline                   │
│                             │                                │
│  Launch: Q2 2024           │  Launch: Q3 2024   [CHANGED]   │
│                             │                                │
├─────────────────────────────────────────────────────────────┤
│  Changes: 3 modified, 1 added, 0 deleted                     │
│  Changed by: Marie Dupont | 2024-03-18 14:30                │
│                                                              │
│  [Accept All]  [Reject All]  [Review Each]  [Close]         │
└─────────────────────────────────────────────────────────────┘
```

### 5.4 Parallel & Chain Work

#### Parallel Versions

Multiple versions can exist simultaneously for:
- A/B testing
- Different audiences
- Experimental features
- Team member variations

```
┌─────────────────────────────────────────────────────────────┐
│                  PARALLEL VERSIONS                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌─────────┐                               │
│               ┌───►│ v2.0-A  │ (Marketing version)           │
│               │    └─────────┘                               │
│  ┌─────────┐  │                                              │
│  │  v1.0   │──┤    ┌─────────┐                               │
│  └─────────┘  ├───►│ v2.0-B  │ (Technical version)           │
│               │    └─────────┘                               │
│               │                                              │
│               │    ┌─────────┐                               │
│               └───►│ v2.0-C  │ (Executive summary)           │
│                    └─────────┘                               │
│                                                              │
│  Each version can be independently edited, reviewed,         │
│  and approved. Merge options available.                      │
└─────────────────────────────────────────────────────────────┘
```

#### Sequential Pipelines

Work flows through defined stages with handoffs:

```
┌─────────────────────────────────────────────────────────────┐
│                  SEQUENTIAL PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐       │
│  │ Draft  │───►│ Edit   │───►│ Review │───►│Publish │       │
│  │ (Jo)   │    │(Marie) │    │(Pierre)│    │(System)│       │
│  └────────┘    └────────┘    └────────┘    └────────┘       │
│                                                              │
│  Stage rules:                                                │
│  - Each stage has assigned role                              │
│  - Automatic notification on handoff                         │
│  - Cannot skip stages                                        │
│  - Governance validation at each transition                  │
└─────────────────────────────────────────────────────────────┘
```

#### Human + Agent Collaboration

```
┌─────────────────────────────────────────────────────────────┐
│              HUMAN + AGENT COLLABORATION                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐         ┌────────────┐                      │
│  │  👤 Human  │◄───────►│  🤖 Agent  │                      │
│  │   Draft    │         │  Enhance   │                      │
│  └────────────┘         └────────────┘                      │
│        │                      │                              │
│        ▼                      ▼                              │
│  ┌────────────┐         ┌────────────┐                      │
│  │  👤 Human  │◄────────│  🤖 Agent  │                      │
│  │  Review    │  merge  │  Analysis  │                      │
│  └────────────┘         └────────────┘                      │
│        │                                                     │
│        ▼                                                     │
│  ┌────────────┐                                             │
│  │  👤 Human  │ (Final approval always human)               │
│  │  Approve   │                                             │
│  └────────────┘                                             │
│                                                              │
│  KEY: Agents PROPOSE, Humans DECIDE                          │
└─────────────────────────────────────────────────────────────┘
```

---

# PART VI: AGENT SYSTEM

---

## 6. AGENT COLLABORATION

### 6.1 Agent Workspaces

Agents operate in **isolated workspaces** with controlled access.

#### Agent Workspace Principles

| Principle | Implementation |
|-----------|----------------|
| **Isolation** | Agent workspace is separate from user workspace |
| **No Direct Write** | Agents cannot modify user content directly |
| **Logged Actions** | Every agent action is recorded |
| **Scoped Access** | Agents only see what they're permitted |
| **Budget Limited** | Operations limited by token budget |

#### Agent Workspace Structure

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 AGENT WORKSPACE: Marketing Agent                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  STATUS: Active                                              │
│  SCOPE: 💼 Business > Marketing Project                      │
│  BUDGET: 2,450 / 5,000 tokens                                │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  CURRENT TASK                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Analyzing Q3 campaign performance                    │   │
│  │  Progress: ███████░░░ 70%                            │   │
│  │  Estimated completion: 2 minutes                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  INPUTS (Read-Only Access)                                   │
│  📄 Q3 Campaign Report.docx                                  │
│  📊 Analytics Dashboard Export                               │
│  🧵 Marketing Discussion Thread                              │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  OUTPUTS (Pending User Approval)                             │
│  📄 Campaign Analysis Summary [DRAFT]                        │
│  📊 Performance Metrics Table [DRAFT]                        │
│  💡 3 Recommendations [PENDING REVIEW]                       │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  ACTION LOG                                                  │
│  14:23:01 - Read Q3 Campaign Report                          │
│  14:23:15 - Extracted key metrics                            │
│  14:23:45 - Generated analysis                               │
│  14:24:02 - Created recommendations                          │
│                                                              │
│  [View Full Log]  [Pause Agent]  [Cancel Task]              │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Agent Proposals

When agents complete work, they submit **proposals** for human validation.

#### Proposal Types

| Type | Description | Approval Required |
|------|-------------|-------------------|
| **Content** | New document or text | Yes |
| **Edit** | Modification to existing | Yes |
| **Analysis** | Insights and findings | Review recommended |
| **Recommendation** | Suggested actions | Yes for execution |
| **Action** | Task completion | Depends on task type |

#### Proposal Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 AGENT PROPOSAL                           [Marketing Agent]│
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PROPOSAL: Campaign Analysis Report                          │
│  TYPE: Content Creation                                      │
│  SUBMITTED: Today 14:25                                      │
│  TOKENS USED: 450                                            │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  PREVIEW                                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  # Q3 Campaign Analysis                               │   │
│  │                                                       │   │
│  │  ## Key Findings                                      │   │
│  │  - Overall engagement up 23%                          │   │
│  │  - Email open rate: 28% (industry avg: 21%)          │   │
│  │  - Social reach increased 45%                         │   │
│  │                                                       │   │
│  │  ## Recommendations                                   │   │
│  │  1. Increase budget for high-performing channels      │   │
│  │  2. A/B test new email subject lines                  │   │
│  │  3. Expand social content calendar                    │   │
│  │                                                       │   │
│  │  [Show full document]                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  OPTIONS                                                     │
│                                                              │
│  ☑️ Accept entire proposal                                   │
│  ☐ Accept with modifications                                 │
│  ☐ Partial acceptance (select sections)                      │
│  ☐ Reject and provide feedback                               │
│  ☐ Request revision                                          │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  DESTINATION                                                 │
│  ☑️ Add to: 💼 Business > Marketing > Q3 Campaign            │
│  ☐ Create new workspace                                      │
│  ☐ Merge with existing document                              │
│                                                              │
│                      [Cancel]  [Accept Proposal]             │
└─────────────────────────────────────────────────────────────┘
```

#### Partial Acceptance

Users can accept parts of a proposal while rejecting others:

```
┌─────────────────────────────────────────────────────────────┐
│  PARTIAL ACCEPTANCE                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ☑️ Section 1: Key Findings           [Accept]               │
│  ☑️ Section 2: Performance Metrics    [Accept]               │
│  ☐ Section 3: Budget Recommendations  [Reject - needs data]  │
│  ☑️ Section 4: Timeline               [Accept with edits]    │
│                                                              │
│  Feedback for rejected sections:                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Section 3 needs actual budget numbers and ROI       │   │
│  │  calculations. Please revise with Q2 data.           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│                [Cancel]  [Submit Partial Acceptance]         │
└─────────────────────────────────────────────────────────────┘
```

### 6.3 Orchestration

#### Orchestration Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                ORCHESTRATION HIERARCHY                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌─────────────────┐                       │
│                    │ GENERAL         │                       │
│                    │ ORCHESTRATOR    │                       │
│                    │ (System-wide)   │                       │
│                    └────────┬────────┘                       │
│                             │                                │
│         ┌───────────────────┼───────────────────┐           │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ BUSINESS    │    │ PERSONAL    │    │ CREATIVE    │     │
│  │ORCHESTRATOR │    │ORCHESTRATOR │    │ORCHESTRATOR │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                   │                   │           │
│    ┌────┴────┐         ┌────┴────┐         ┌────┴────┐     │
│    ▼         ▼         ▼         ▼         ▼         ▼     │
│ ┌─────┐  ┌─────┐   ┌─────┐  ┌─────┐   ┌─────┐  ┌─────┐    │
│ │Agent│  │Agent│   │Agent│  │Agent│   │Agent│  │Agent│    │
│ │Mktg │  │Sales│   │Health│ │Finc │   │Design│ │Write│    │
│ └─────┘  └─────┘   └─────┘  └─────┘   └─────┘  └─────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Orchestration Functions

| Function | Description | Level |
|----------|-------------|-------|
| **Task Delegation** | Assign tasks to appropriate agents | All levels |
| **Load Balancing** | Distribute work across agents | Sphere level |
| **Priority Management** | Ensure urgent tasks get resources | All levels |
| **Conflict Resolution** | Handle competing requests | General level |
| **Budget Allocation** | Distribute tokens to agents | Sphere level |
| **Performance Monitoring** | Track agent efficiency | All levels |

#### Supervision Rules

| Rule | Description |
|------|-------------|
| **Scope Enforcement** | Agent cannot operate outside assigned sphere |
| **Budget Limits** | Agent stops when budget exhausted |
| **Time Limits** | Long-running tasks require checkpoints |
| **Output Validation** | All outputs must pass quality checks |
| **Escalation** | Uncertain situations escalate to human |
| **Audit Trail** | All actions logged for review |

---

# PART VII: DATA & ECONOMICS

---

## 7. DATA, SHARING & TOKENS

### 7.1 Data Sharing

#### Sharing Modes

| Mode | Visibility | Use Case |
|------|------------|----------|
| **Private** | Owner only | Personal work, drafts |
| **Internal** | Within organization | Team collaboration |
| **Restricted** | Specific users/groups | Controlled sharing |
| **External** | Outside organization | Client/partner sharing |
| **Public** | Anyone | Published content |

#### Permission Dimensions

```
┌─────────────────────────────────────────────────────────────┐
│                  PERMISSION MATRIX                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PERMISSION TYPES                                            │
│  ├── Read: View content                                      │
│  ├── Write: Edit content                                     │
│  ├── Comment: Add comments                                   │
│  ├── Share: Grant access to others                           │
│  ├── Delete: Remove content                                  │
│  └── Admin: Full control                                     │
│                                                              │
│  PERMISSION SCOPES                                           │
│  ├── By Sphere: Apply to entire sphere                       │
│  ├── By Identity: Apply to all work under identity           │
│  ├── By Project: Apply within project                        │
│  ├── By Workspace: Apply to specific workspace               │
│  └── By Item: Apply to individual item                       │
│                                                              │
│  PERMISSION INHERITANCE                                      │
│  Identity → Sphere → Project → Workspace → Item              │
│  (More specific overrides less specific)                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Sharing Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🔗 SHARE: Project Proposal                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CURRENT ACCESS                                              │
│  👤 Jo Bouchard (Owner)                    Admin             │
│  👤 Marie Dupont                           Write             │
│  👥 Design Team                            Read              │
│                                                              │
│  ADD PEOPLE OR GROUPS                                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  🔍 Search users, teams, or email...                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  LINK SHARING                                                │
│  ☐ Anyone with link can view                                 │
│  ☐ Anyone with link can comment                              │
│  ☐ Anyone with link can edit                                 │
│                                                              │
│  ADVANCED OPTIONS                                            │
│  ☐ Allow download                                            │
│  ☐ Allow print                                               │
│  ☐ Set expiration date: [__________]                         │
│  ☐ Require password: [__________]                            │
│                                                              │
│                      [Cancel]  [Update Sharing]              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Token Systems

CHE·NU uses **internal utility tokens** to make AI costs visible and controllable.

#### Token Types

| Type | Purpose | Source |
|------|---------|--------|
| **AI Tokens** | LLM API consumption | External providers |
| **CHE·NU Tokens** | Internal credits | Subscription/purchase |
| **Bonus Tokens** | Promotional credits | Referrals, events |

#### Token Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    TOKEN HIERARCHY                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ACCOUNT LEVEL                                               │
│  └── Total tokens available: 100,000                         │
│                                                              │
│      IDENTITY LEVEL                                          │
│      ├── Personal: 20,000 allocated                          │
│      │   └── Spheres: 2,500 each                             │
│      │                                                       │
│      └── Business: 80,000 allocated                          │
│          ├── Business Sphere: 30,000                         │
│          │   └── Projects:                                   │
│          │       ├── Client Portal: 15,000                   │
│          │       └── Marketing: 15,000                       │
│          │                                                   │
│          ├── Creative Sphere: 20,000                         │
│          ├── Team Sphere: 20,000                             │
│          └── Reserve: 10,000                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Budget Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  💰 TOKEN BUDGET                        [This Month]  [Year] │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  OVERVIEW                                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Total: 100,000    Used: 45,230    Available: 54,770 │   │
│  │  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░  45%   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  BY SPHERE                                                   │
│  💼 Business        ████████████████░░░░░  78%  23,400      │
│  🎨 Creative        ████████░░░░░░░░░░░░░  40%   8,000      │
│  🏠 Personal        ██████░░░░░░░░░░░░░░░  30%   6,000      │
│  🤝 Team            ████░░░░░░░░░░░░░░░░░  20%   4,000      │
│  Other              ███░░░░░░░░░░░░░░░░░░  15%   3,830      │
│                                                              │
│  BY ACTIVITY                                                 │
│  🤖 Agent tasks     ████████████████       60%  27,138      │
│  🧵 Threads         ████████░░░░░░░░       30%  13,569      │
│  📄 Documents       ████░░░░░░░░░░░░       10%   4,523      │
│                                                              │
│  ALERTS                                                      │
│  ⚠️ Business sphere at 78% - consider reallocation          │
│  ℹ️ Projected to exhaust by March 25 at current rate        │
│                                                              │
│  [Reallocate]  [Purchase More]  [View Details]              │
└─────────────────────────────────────────────────────────────┘
```

#### Usage Tracking

Every token expenditure is logged:

```
┌─────────────────────────────────────────────────────────────┐
│  📊 TOKEN USAGE LOG                    [Export]  [Filter]    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TIME          SPHERE    ACTION              TOKENS  AGENT   │
│  ────────────  ────────  ─────────────────   ──────  ─────── │
│  14:25:03      Business  Generate report       450   Mktg    │
│  14:22:15      Business  Analyze data          320   Mktg    │
│  14:18:42      Personal  Summarize article     125   Nova    │
│  14:15:00      Creative  Edit image desc       200   Design  │
│  14:10:22      Business  Draft email           180   Comm    │
│  14:05:18      Team      Code review           580   Dev     │
│  ...                                                         │
│                                                              │
│  Showing 6 of 234 entries  [Load More]                       │
└─────────────────────────────────────────────────────────────┘
```

---

# PART VIII: COLLABORATION

---

## 8. MEETINGS & COLLABORATION

### 8.1 Meetings

Meetings in CHE·NU are **first-class objects** with rich functionality.

#### Meeting Types

| Type | Participants | Features |
|------|--------------|----------|
| **Human-Only** | Multiple users | Video, screen share, notes |
| **Human + Agent** | Users + AI agents | Analysis, real-time assistance |
| **Agent-Only** | Multiple agents | Automated workflows |
| **Async Meeting** | Participants at different times | Recorded contributions |

#### Meeting Interface

```
┌─────────────────────────────────────────────────────────────┐
│  📹 MEETING: Q3 Strategy Review                 [Recording] │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                                                       │  │
│  │     ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐           │  │
│  │     │ Jo  │   │Marie│   │ 🤖  │   │ ✦  │           │  │
│  │     │     │   │     │   │Agent│   │Nova │           │  │
│  │     └─────┘   └─────┘   └─────┘   └─────┘           │  │
│  │                                                       │  │
│  │              [🎥 Video]  [🔇 Mute]  [📺 Share]       │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  MEETING TOOLS                                               │
│  ├── 📝 Live Notes (auto-transcription)                      │
│  ├── ✅ Action Items (auto-detected)                         │
│  ├── 📊 Shared Screen                                        │
│  ├── 💬 Chat                                                 │
│  └── 🤖 AI Assistant (summaries, answers)                    │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  AGENDA                                                      │
│  ☑️ 1. Review Q2 results (10 min)                            │
│  ☐ 2. Discuss Q3 targets (20 min)                            │
│  ☐ 3. Resource allocation (15 min)                           │
│  ☐ 4. Action items & next steps (5 min)                      │
│                                                              │
│  [End Meeting]                             Duration: 23:45   │
└─────────────────────────────────────────────────────────────┘
```

#### Meeting Outputs

| Output | Generation | Content |
|--------|------------|---------|
| **Transcript** | Automatic | Full text of conversation |
| **Summary** | AI-generated | Key points, decisions |
| **Action Items** | AI-detected | Tasks with assignees |
| **Recording** | Optional | Video/audio file |
| **.chenu File** | Automatic | Complete meeting artifact |

#### .chenu Meeting File

```yaml
# meeting_q3_strategy.chenu.meeting

chenu_version: "1.0"
file_type: "meeting"

meeting:
  title: "Q3 Strategy Review"
  date: "2024-03-20T14:00:00Z"
  duration: 3600  # seconds
  
participants:
  - name: "Jo Bouchard"
    role: "host"
    attendance: "full"
  - name: "Marie Dupont"
    role: "participant"
    attendance: "full"
  - name: "Marketing Agent"
    role: "assistant"
    type: "agent"
  - name: "Nova"
    role: "system"
    type: "system"

agenda:
  - item: "Review Q2 results"
    duration: 600
    status: "completed"
  - item: "Discuss Q3 targets"
    duration: 1200
    status: "completed"
  # ...

transcript:
  format: "timestamped"
  file: "transcript_q3_strategy.txt"

summary:
  key_points:
    - "Q2 exceeded targets by 15%"
    - "Q3 focus on market expansion"
    - "Budget increase approved"
  decisions:
    - "Launch new product line in Q3"
    - "Hire 2 additional developers"
  
action_items:
  - task: "Prepare market analysis"
    assignee: "Marie Dupont"
    due: "2024-03-25"
  - task: "Draft hiring plan"
    assignee: "Jo Bouchard"
    due: "2024-03-22"

recording:
  available: true
  file: "recording_q3_strategy.mp4"
  duration: 3580
```

### 8.2 Collaboration Modes

#### Live Collaboration

Multiple users work simultaneously:

```
┌─────────────────────────────────────────────────────────────┐
│  📄 Project Plan                    [LIVE] 👤👤🤖 3 active   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  # Project Plan                                              │
│                                                              │
│  ## Timeline                                                 │
│  - Phase 1: March[👤Jo]                                      │
│  - Phase 2: April[👤Marie|                                   │
│  - Phase 3: May                                              │
│                                                              │
│  ## Budget                                                   │
│  [🤖Agent is analyzing this section...]                      │
│                                                              │
│  ─────────────────────────────────────────────────────────   │
│  ACTIVE COLLABORATORS                                        │
│  👤 Jo - Line 4                                              │
│  👤 Marie - Line 5                                           │
│  🤖 Agent - Analyzing Budget section                         │
│                                                              │
│  CHAT                                                        │
│  Marie: "Should we add a contingency?"                       │
│  Jo: "Yes, 10% buffer"                                       │
│  Agent: "Suggestion: Based on similar projects, 15%..."      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Async Collaboration

Contributions at different times:

```
┌─────────────────────────────────────────────────────────────┐
│  📄 Design Brief                         [ASYNC COLLAB]      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CONTRIBUTION TIMELINE                                       │
│  ─────────────────────────────────────────────────────────   │
│                                                              │
│  Mar 18, 09:00 - Jo created document                         │
│  │                                                           │
│  ├── Mar 18, 11:30 - Marie added brand section               │
│  │   └── 📝 "Added color palette and typography"             │
│  │                                                           │
│  ├── Mar 18, 14:00 - Pierre added technical specs            │
│  │   └── 📝 "Added responsive breakpoints"                   │
│  │                                                           │
│  ├── Mar 19, 09:00 - Agent analyzed accessibility            │
│  │   └── 🤖 "Flagged contrast issues in section 3"           │
│  │                                                           │
│  └── Mar 19, 10:30 - Jo approved changes                     │
│      └── ✅ "Approved with minor edits"                      │
│                                                              │
│  PENDING REVIEWS                                              │
│  ⏳ Waiting for: Sarah (Legal review)                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Observer / Spectator Mode

View-only access with optional commenting:

```
┌─────────────────────────────────────────────────────────────┐
│  📄 Executive Report                    [OBSERVER MODE] 👁️   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ⚠️ You are viewing this document as an observer.            │
│     You can read and comment, but cannot edit.               │
│                                                              │
│  # Executive Summary                                         │
│                                                              │
│  [Content displayed in read-only mode...]                    │
│                                                              │
│  ─────────────────────────────────────────────────────────   │
│                                                              │
│  YOUR COMMENTS                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Add a comment... (visible to editors)               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  [Request Edit Access]  [Export as PDF]                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# PART IX: MY TEAM & TOOLS

---

## 9. MY TEAM, IA LABS & TOOLS

The **My Team sphere (🤝)** is the central hub for all collaborative intelligence.

### 9.1 Agents

#### Agent Types

| Type | Description | Example |
|------|-------------|---------|
| **Role-Based** | Assigned to specific function | Marketing Agent, Sales Agent |
| **Skill-Based** | Specialized capability | Writing Agent, Analysis Agent |
| **Sphere-Specific** | Dedicated to one sphere | Personal Finance Agent |
| **General** | Multi-purpose assistant | Research Agent |

#### Agent Configuration

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 AGENT CONFIGURATION: Marketing Agent                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  BASIC INFO                                                  │
│  Name: Marketing Agent                                       │
│  Type: Role-Based                                            │
│  Status: ● Active                                            │
│  Created: 2024-01-15                                         │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  SCOPE                                                       │
│  ☑️ Business Sphere                                          │
│     ☑️ Marketing Project                                     │
│     ☐ Sales Project                                          │
│     ☐ Operations Project                                     │
│  ☐ Personal Sphere                                           │
│  ☐ Creative Sphere                                           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  CAPABILITIES                                                │
│  ☑️ Content generation                                       │
│  ☑️ Data analysis                                            │
│  ☑️ Email drafting                                           │
│  ☑️ Social media management                                  │
│  ☐ Code generation                                           │
│  ☐ Financial analysis                                        │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  BUDGET                                                      │
│  Monthly allocation: 10,000 tokens                           │
│  Used this month: 6,234 tokens                               │
│  Per-task limit: 500 tokens                                  │
│  ☑️ Alert at 80% usage                                       │
│  ☑️ Stop at 100% (require approval to continue)              │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  PERMISSIONS                                                 │
│  ☑️ Read documents in scope                                  │
│  ☑️ Propose content changes                                  │
│  ☐ Direct write access (requires approval)                   │
│  ☑️ Access thread history                                    │
│  ☐ Access other agents' work                                 │
│                                                              │
│              [Deactivate]  [Reset]  [Save Changes]           │
└─────────────────────────────────────────────────────────────┘
```

#### Agent Library

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 MY AGENTS                          [+ Add Agent]         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ACTIVE AGENTS                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  🤖 Marketing Agent     ● Active    6.2k/10k tokens  │   │
│  │     Scope: Business > Marketing                       │   │
│  │     Last active: 5 min ago                           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  🤖 Research Agent      ● Active    3.8k/5k tokens   │   │
│  │     Scope: All spheres (read-only)                   │   │
│  │     Last active: 2 hours ago                         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  🤖 Code Review Agent   ● Active    8.1k/15k tokens  │   │
│  │     Scope: Business > Development                     │   │
│  │     Last active: 30 min ago                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  AVAILABLE TO HIRE                                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  🤖 Financial Analyst   Recommended for Business     │   │
│  │     Capabilities: Budgeting, forecasting, reporting  │   │
│  │     [Learn More]  [Hire]                             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Tools & Skills

#### Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| **Document** | PDF creator, DOCX editor, Markdown | Create documents |
| **Data** | Table editor, CSV processor, JSON formatter | Handle data |
| **Analysis** | Chart generator, Statistics, Comparison | Analyze information |
| **Media** | Image processor, Audio transcriber | Handle media |
| **Integration** | API connector, Webhook, Import/Export | Connect services |

#### Tool Library

```
┌─────────────────────────────────────────────────────────────┐
│  🔧 TOOLS & SKILLS                      [Browse All]         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DOCUMENT TOOLS                                              │
│  ├── 📄 PDF Creator          Create professional PDFs        │
│  ├── 📝 Document Editor      Rich text editing               │
│  ├── 📊 Spreadsheet          Tables with formulas            │
│  └── 📑 Presentation         Slides and decks                │
│                                                              │
│  DATA TOOLS                                                  │
│  ├── 📈 Chart Generator      Visualize data                  │
│  ├── 🔄 Data Transformer     Convert between formats         │
│  ├── 🔍 Data Extractor       Pull data from sources          │
│  └── 📋 Template Engine      Fill templates with data        │
│                                                              │
│  ANALYSIS TOOLS                                              │
│  ├── 📊 Statistics           Calculate metrics               │
│  ├── 🔎 Comparison           Side-by-side analysis           │
│  ├── 📉 Trend Analysis       Identify patterns               │
│  └── ⚖️ Decision Matrix      Evaluate options                │
│                                                              │
│  INTEGRATION TOOLS                                           │
│  ├── 🔗 API Connector        Connect external services       │
│  ├── 📤 Export Engine        Output to various formats       │
│  ├── 📥 Import Engine        Bring in external data          │
│  └── 🔔 Webhook Manager      Automated triggers              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 9.3 Tool Availability & Governance

#### Tool Access Control

```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ TOOL GOVERNANCE                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GLOBAL SETTINGS                                             │
│  ☑️ Tools available across all spheres                       │
│  ☑️ Agent access requires approval                           │
│  ☐ Users can install custom tools                            │
│                                                              │
│  TOOL PERMISSIONS BY SPHERE                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  💼 Business                                          │   │
│  │  ☑️ PDF Creator  ☑️ Spreadsheet  ☑️ API Connector    │   │
│  │  ☑️ Export       ☐ Custom Tools                       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  🏠 Personal                                          │   │
│  │  ☑️ PDF Creator  ☑️ Spreadsheet  ☐ API Connector    │   │
│  │  ☑️ Export       ☐ Custom Tools                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  USAGE LIMITS                                                │
│  PDF Generation: 100/month                                   │
│  API Calls: 1,000/month                                      │
│  Data Export: 50GB/month                                     │
│                                                              │
│                            [Save Governance Settings]        │
└─────────────────────────────────────────────────────────────┘
```

---

# PART X: SPATIAL & XR

---

## 10. XR & SPATIAL FEATURES

CHE·NU is designed for **spatial computing** — every element has a place in 3D space.

### 10.1 Spheres as Places

Each sphere is a **distinct spatial environment** that users can enter and explore.

#### Spatial Mapping

| CHE·NU Element | Spatial Representation |
|----------------|------------------------|
| **Sphere** | Distinct location/realm |
| **Bureau** | Central building/structure |
| **Section** | Room within bureau |
| **Workspace** | Desk/workstation |
| **Thread** | Path/connection between elements |
| **Agent** | Character/entity |

#### Sphere Environments

```
┌─────────────────────────────────────────────────────────────┐
│                  SPATIAL SPHERE DESIGN                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🏠 PERSONAL SPHERE                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Environment: Comfortable home/retreat                │    │
│  │  Architecture: Warm, private, personal scale         │    │
│  │  Rooms: Living space, study, wellness area           │    │
│  │  Mood: Calm, reflective, safe                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  💼 BUSINESS SPHERE                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Environment: Professional office complex            │    │
│  │  Architecture: Clean, efficient, corporate           │    │
│  │  Rooms: Meeting rooms, project spaces, data center   │    │
│  │  Mood: Focused, productive, collaborative            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  🎨 CREATIVE SPHERE                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Environment: Artist studio/creative workshop        │    │
│  │  Architecture: Open, inspiring, flexible             │    │
│  │  Rooms: Design lab, media studio, gallery            │    │
│  │  Mood: Imaginative, expressive, playful              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Bureau Layout

```
┌─────────────────────────────────────────────────────────────┐
│               BUREAU SPATIAL LAYOUT                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌─────────────┐                          │
│                    │  DASHBOARD  │ (Entry/Overview)          │
│                    │   (Main)    │                          │
│                    └──────┬──────┘                          │
│                           │                                  │
│     ┌─────────────────────┼─────────────────────┐           │
│     │                     │                     │           │
│  ┌──┴──┐  ┌─────┐  ┌─────┴─────┐  ┌─────┐  ┌──┴──┐        │
│  │Notes│  │Tasks│  │  Projects │  │Data │  │Agents│        │
│  └─────┘  └─────┘  └───────────┘  └─────┘  └─────┘        │
│                                                              │
│     ┌─────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐        │
│     │Thrds│  │Meetings │  │ Reports │  │ Budget   │        │
│     └─────┘  └─────────┘  └─────────┘  └──────────┘        │
│                                                              │
│  All rooms connected to central hub                          │
│  User teleports or walks between rooms                       │
│  Each room has its own spatial layout                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 10.2 Universe Views

Same structure, completely different visual experience.

#### View Comparison

| Aspect | Regular | Futuristic | Natural | Astral |
|--------|---------|------------|---------|--------|
| **Palette** | Gray, white, accent | Cyan, magenta, black | Green, brown, blue | Purple, gold, cosmic |
| **Materials** | Glass, metal, paper | Holograms, light, energy | Wood, stone, water | Crystal, light, void |
| **Architecture** | Clean office | Sci-fi station | Organic structures | Floating geometry |
| **Lighting** | Professional | Neon, glow | Natural, warm | Ethereal, magical |
| **Audio** | Subtle ambient | Electronic hum | Nature sounds | Cosmic resonance |
| **Interaction** | Click, drag | Gesture, voice | Touch, flow | Intent, thought |

#### View Switching

```
┌─────────────────────────────────────────────────────────────┐
│  🌍 UNIVERSE VIEW                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Current: Regular / Professional                             │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Regular  │  │Futuristic│  │ Natural  │  │  Astral  │    │
│  │    ✓     │  │          │  │          │  │          │    │
│  │ ▓▓▓▓▓▓▓ │  │ ░░░░░░░░ │  │ ▒▒▒▒▒▒▒▒ │  │ ▓░▒░▓░▒░ │    │
│  │ Clean   │  │ Hologram  │  │ Organic   │  │ Cosmic   │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                              │
│  ⚠️ Switching views does not change functionality.           │
│     Same data, same structure, different visual.             │
│                                                              │
│                      [Preview]  [Apply View]                 │
└─────────────────────────────────────────────────────────────┘
```

### 10.3 XR Interaction

#### Navigation Methods

| Method | Input | Use Case |
|--------|-------|----------|
| **Teleport** | Point and click | Quick movement between areas |
| **Walk** | Thumbstick/trackpad | Exploration |
| **Portal** | Enter doorway | Sphere/room transition |
| **Voice** | "Go to Business" | Hands-free navigation |
| **Menu** | Wrist menu | Direct access to any location |

#### XR Meetings

```
┌─────────────────────────────────────────────────────────────┐
│                    XR MEETING ROOM                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│           ┌─────────────────────────────────┐               │
│           │      SHARED WORKSPACE           │               │
│           │      (3D documents, boards)     │               │
│           └─────────────────────────────────┘               │
│                                                              │
│      👤 Jo            🤖 Agent           👤 Marie            │
│      (Avatar)         (Entity)           (Avatar)            │
│                                                              │
│                     ✦ Nova                                   │
│                   (Floating)                                 │
│                                                              │
│   TOOLS                                                      │
│   ├── 🖊️ Spatial pen (draw in 3D)                           │
│   ├── 📋 Floating boards                                     │
│   ├── 🔊 Spatial audio (voice positioning)                   │
│   └── 📹 Record spatial meeting                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### XR Workspaces

```
┌─────────────────────────────────────────────────────────────┐
│                   XR WORKSPACE                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                MAIN CANVAS (floating)                │   │
│   │           ┌─────────────────────────┐               │   │
│   │           │    Document/Board/      │               │   │
│   │           │    Canvas content       │               │   │
│   │           │    (manipulable)        │               │   │
│   │           └─────────────────────────┘               │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
│   ┌──────────┐                           ┌──────────┐       │
│   │ TOOL     │                           │ CONTEXT  │       │
│   │ PALETTE  │                           │ PANEL    │       │
│   │ (left)   │                           │ (right)  │       │
│   └──────────┘                           └──────────┘       │
│                                                              │
│                      👤 (User position)                      │
│                                                              │
│   INTERACTIONS                                               │
│   ├── Hand gestures: grab, pinch, point                      │
│   ├── Voice: "Make this bigger", "Add a section"            │
│   ├── Gaze: Select by looking                               │
│   └── Controller: Traditional input fallback                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# PART XI: GOVERNANCE

---

## 11. GOVERNANCE & CONTROL (FUNCTIONAL)

### 11.1 Laws

Laws are **non-bypassable rules** that govern all CHE·NU operations.

#### Law Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **Privacy Laws** | Protect user data | Data encryption, access logging |
| **Execution Laws** | Control AI actions | Human approval for high-impact |
| **Content Laws** | Ensure appropriate output | Filtering, moderation |
| **Budget Laws** | Control spending | Limits, alerts, caps |
| **Scope Laws** | Enforce boundaries | Cross-sphere restrictions |

#### Law Configuration

```
┌─────────────────────────────────────────────────────────────┐
│  ⚖️ GOVERNANCE LAWS                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GLOBAL LAWS (Cannot be disabled)                            │
│  ────────────────────────────────────────────────────────    │
│  🔒 Data Privacy                                [Enforced]   │
│     All personal data encrypted at rest and transit          │
│                                                              │
│  🔒 Human Validation                            [Enforced]   │
│     High-impact actions require human approval               │
│                                                              │
│  🔒 Audit Trail                                 [Enforced]   │
│     All actions logged with complete history                 │
│                                                              │
│  SPHERE LAWS (Configurable)                                  │
│  ────────────────────────────────────────────────────────    │
│  💼 Business Sphere                                          │
│  ☑️ Client data isolation                      [Enabled]     │
│  ☑️ Contract approval workflow                 [Enabled]     │
│  ☐ Auto-publish to social                      [Disabled]    │
│                                                              │
│  🏠 Personal Sphere                                          │
│  ☑️ Financial data extra protection            [Enabled]     │
│  ☐ Share health data with agents               [Disabled]    │
│                                                              │
│  CUSTOM LAWS                                                 │
│  ────────────────────────────────────────────────────────    │
│  [+ Add Custom Law]                                          │
│                                                              │
│  Existing:                                                   │
│  📜 "No agent access to salary data"           [Active]      │
│  📜 "Require 2 approvals for external share"   [Active]      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Human Validation Points

| Action Type | Validation Required | Approvers |
|-------------|---------------------|-----------|
| **Content Publish** | Yes (external) | Owner |
| **Data Export** | Yes | Owner |
| **Budget Change** | Yes | Owner + Admin |
| **Agent Hire** | Yes | Owner |
| **Scope Change** | Yes | Owner |
| **Delete Permanently** | Yes (confirm) | Owner |
| **External Share** | Yes | Owner |

### 11.2 Audit

#### Audit Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│  📋 AUDIT LOG                          [Export]  [Filter]    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  FILTER                                                      │
│  Date: [Last 7 days ▼]  Type: [All ▼]  Sphere: [All ▼]      │
│                                                              │
│  AUDIT ENTRIES                                               │
│  ─────────────────────────────────────────────────────────   │
│                                                              │
│  Mar 20, 14:25:03                                            │
│  ACTION: Document created                                    │
│  USER: Jo Bouchard                                           │
│  SPHERE: Business > Marketing                                │
│  DETAILS: Created "Q3 Campaign Analysis"                     │
│  TOKENS: 0                                                   │
│  ─────────────────────────────────────────────────────────   │
│                                                              │
│  Mar 20, 14:22:15                                            │
│  ACTION: Agent task completed                                │
│  AGENT: Marketing Agent                                      │
│  SPHERE: Business > Marketing                                │
│  DETAILS: Generated report, submitted for approval           │
│  TOKENS: 450                                                 │
│  ─────────────────────────────────────────────────────────   │
│                                                              │
│  Mar 20, 14:18:42                                            │
│  ACTION: Data exported                                       │
│  USER: Marie Dupont                                          │
│  SPHERE: Business                                            │
│  DETAILS: Exported client list to CSV (145 records)          │
│  APPROVAL: Jo Bouchard (14:17:30)                            │
│  ─────────────────────────────────────────────────────────   │
│                                                              │
│  [Load More...]                         Showing 3 of 1,245   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Version History

```
┌─────────────────────────────────────────────────────────────┐
│  📚 VERSION HISTORY: Project Proposal                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  TIMELINE                                                    │
│  ─────────────────────────────────────────────────────────   │
│                                                              │
│  v3.0 ─ Mar 20, 14:30 ─ Current                             │
│  │      Author: Jo Bouchard                                  │
│  │      Changes: Final review edits                          │
│  │      Status: Published                                    │
│  │      [View] [Compare] [Restore]                           │
│  │                                                           │
│  v2.1 ─ Mar 18, 16:45                                       │
│  │      Author: Marie Dupont                                 │
│  │      Changes: Added timeline section                      │
│  │      Status: Approved                                     │
│  │      [View] [Compare] [Restore]                           │
│  │                                                           │
│  v2.0 ─ Mar 18, 11:00                                       │
│  │      Author: Marketing Agent 🤖                           │
│  │      Changes: Enhanced executive summary                  │
│  │      Status: Approved                                     │
│  │      [View] [Compare] [Restore]                           │
│  │                                                           │
│  v1.0 ─ Mar 15, 09:00                                       │
│         Author: Jo Bouchard                                  │
│         Changes: Initial draft                               │
│         Status: Archived                                     │
│         [View] [Compare] [Restore]                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Decision Traceability

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 DECISION TRACE: Product Launch Date                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  DECISION: Launch product in Q3 2024 (September)             │
│  MADE BY: Jo Bouchard                                        │
│  DATE: March 18, 2024                                        │
│                                                              │
│  CONTEXT                                                     │
│  ─────────────────────────────────────────────────────────   │
│  Thread: Product Planning Discussion (#thread-456)           │
│  Meeting: Strategy Review (March 15)                         │
│  Documents: Market Analysis, Resource Plan                   │
│                                                              │
│  RATIONALE                                                   │
│  ─────────────────────────────────────────────────────────   │
│  "Q3 aligns with back-to-school season and allows           │
│   adequate development time. Market analysis shows           │
│   competitor launching in Q2, so Q3 differentiates."         │
│                                                              │
│  ALTERNATIVES CONSIDERED                                     │
│  ─────────────────────────────────────────────────────────   │
│  ✗ Q2 2024: Too aggressive timeline                          │
│  ✗ Q4 2024: Miss holiday season                              │
│  ✓ Q3 2024: Optimal balance                                  │
│                                                              │
│  IMPACT                                                      │
│  ─────────────────────────────────────────────────────────   │
│  • 15 tasks created/updated                                  │
│  • 3 milestones set                                          │
│  • Budget allocated: $150,000                                │
│  • 5 team members assigned                                   │
│                                                              │
│  [View Related Items]  [Export Decision Record]              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# PART XII: USER EXPERIENCE

---

## 12. UX & ADAPTIVE DISPLAY

### 12.1 Adaptive Menus

Menus adapt based on **context**, **user level**, and **mode**.

#### Context-Based Adaptation

| Context | Menu Emphasis | Hidden Elements |
|---------|---------------|-----------------|
| **Personal Sphere** | Health, Finance, Family | Business tools |
| **Business Sphere** | Projects, Clients, Reports | Personal items |
| **Creative Sphere** | Design, Media, Portfolio | Administrative tools |
| **Workspace Active** | Editing, Versioning | Navigation |

#### User Level Adaptation

```
┌─────────────────────────────────────────────────────────────┐
│                  USER LEVEL SETTINGS                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SELECT YOUR EXPERIENCE LEVEL                                │
│                                                              │
│  ○ BEGINNER                                                  │
│    • Simplified menus                                        │
│    • Guided workflows                                        │
│    • Helpful tooltips                                        │
│    • Reduced options                                         │
│    • Nova assistance prominent                               │
│                                                              │
│  ● STANDARD                                                  │
│    • Full menu access                                        │
│    • Balanced interface                                      │
│    • Context-sensitive help                                  │
│    • All features available                                  │
│                                                              │
│  ○ ADVANCED                                                  │
│    • Power user shortcuts                                    │
│    • Minimal guidance                                        │
│    • Dense information display                               │
│    • Custom workflows                                        │
│    • API access                                              │
│                                                              │
│                            [Save Preference]                 │
└─────────────────────────────────────────────────────────────┘
```

#### Mode Comparison

| Element | Beginner Mode | Advanced Mode |
|---------|---------------|---------------|
| **Menu depth** | 2 levels | Unlimited |
| **Keyboard shortcuts** | Basic | Full set |
| **Settings visible** | Essential | All |
| **Confirmations** | Always | Configurable |
| **Tooltips** | Everywhere | On demand |
| **Nova prompts** | Frequent | Minimal |
| **Quick actions** | 4 | 12+ |

### 12.2 Intelligent Shortcuts

#### Per-Sphere Shortcuts

```
┌─────────────────────────────────────────────────────────────┐
│  ⌨️ KEYBOARD SHORTCUTS                   [Customize]         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GLOBAL SHORTCUTS                                            │
│  ⌘K          Open search                                     │
│  ⌘Space      Toggle Nova                                     │
│  ⌘1-8        Switch to sphere 1-8                           │
│  ⌘N          New item (context-aware)                        │
│  ⌘S          Save                                            │
│  ⌘Z          Undo                                            │
│  ⌘⇧Z         Redo                                            │
│                                                              │
│  💼 BUSINESS SPHERE                                          │
│  ⌘⇧P         New project                                     │
│  ⌘⇧M         Schedule meeting                                │
│  ⌘⇧R         Generate report                                 │
│  ⌘⇧C         Open client list                                │
│                                                              │
│  🎨 CREATIVE SPHERE                                          │
│  ⌘⇧D         New design                                      │
│  ⌘⇧E         Export media                                    │
│  ⌘⇧G         Open gallery                                    │
│                                                              │
│  🔧 WORKSPACE                                                │
│  ⌘B          Bold                                            │
│  ⌘I          Italic                                          │
│  ⌘⇧S         Submit to staging                               │
│  ⌘Enter      Quick save and continue                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Per-Role Shortcuts

| Role | Key Shortcuts |
|------|---------------|
| **Writer** | Formatting, word count, outline |
| **Analyst** | Charts, formulas, comparison |
| **Manager** | Delegation, timeline, reports |
| **Designer** | Layers, export, preview |

#### Per-Workflow Shortcuts

```
┌─────────────────────────────────────────────────────────────┐
│  🔄 WORKFLOW: Content Review                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  QUICK ACTIONS FOR THIS WORKFLOW                             │
│                                                              │
│  A          Approve current item                             │
│  R          Reject with comment                              │
│  N          Next item in queue                               │
│  P          Previous item                                    │
│  C          Add comment                                      │
│  D          View diff                                        │
│  E          Request edit from author                         │
│  Space      Toggle preview                                   │
│                                                              │
│  QUEUE: 12 items remaining                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# PART XIII: APPENDICES

---

## 13. FINAL NOTES FOR PROCESSING

### For Claude / AI Processing

```
┌─────────────────────────────────────────────────────────────┐
│                  PROCESSING INSTRUCTIONS                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ DO:                                                      │
│  • Expand each section with detailed explanations            │
│  • Add diagrams and visual representations                   │
│  • Include examples for every feature                        │
│  • Cross-reference related sections                          │
│  • Maintain consistent terminology                           │
│  • Generate comprehensive PDF (80-120 pages)                 │
│  • Include table of contents and index                       │
│                                                              │
│  ❌ DO NOT:                                                  │
│  • Remove any section                                        │
│  • Merge chapters                                            │
│  • Simplify technical details                                │
│  • Change canonical structure                                │
│  • Modify terminology                                        │
│  • Skip any functionality listed                             │
│                                                              │
│  📋 OUTPUT FORMATS:                                          │
│  • PDF: System Manual (full)                                 │
│  • PDF: Investor Version (condensed)                         │
│  • PDF: User Guide (friendly)                                │
│  • PDF: Technical Reference (detailed)                       │
│  • PDF: XR/Design Specification                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Version Control

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1.0 | 2024-03 | Initial canonical release | CHE·NU |

### Document Status

```
┌─────────────────────────────────────────────────────────────┐
│                      DOCUMENT STATUS                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ Canonical                                                │
│  🔒 Frozen (structure)                                       │
│  📘 Source of Truth                                          │
│  🎯 Ready for PDF expansion                                  │
│                                                              │
│  This document serves as the MASTER REFERENCE for all        │
│  CHE·NU functional documentation. All derived documents      │
│  must maintain consistency with this source.                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## END OF DOCUMENT

---

**CHE·NU™ — Governed Intelligence Operating System**

*CLARITY over FEATURES*

---
