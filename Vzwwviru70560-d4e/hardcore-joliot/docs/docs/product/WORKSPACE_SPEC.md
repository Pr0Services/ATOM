# CHE·NU™ — WORKSPACE SPECIFICATION
## Core Operational Center

> **Version:** V1 FREEZE  
> **Status:** CANONICAL  
> **Role:** Define workspace modes and operations

---

## 1. WORKSPACE OVERVIEW

The Workspace is the **operational heart** of CHE·NU. It's where work actually happens.

### 1.1 Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                       WORKSPACE                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    CONTENT AREA                          │   │
│  │                                                          │   │
│  │   Active Section from Bureau (Notes, Tasks, etc.)        │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    MODE BAR                              │   │
│  │   [Draft] [Staging] [Review] [Version]                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ACTION BAR                            │   │
│  │   [Create] [Transform] [Export] [Share]                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. WORKSPACE MODES

### 2.1 The Four Modes

CHE·NU uses a **staged workflow** for all content:

| Mode | Icon | Description | AI Allowed |
|------|------|-------------|------------|
| **Draft** | 📝 | Work in progress | Full assistance |
| **Staging** | 🔄 | Ready for review | Suggestions only |
| **Review** | 👁️ | Human validation | Read-only |
| **Version** | ✅ | Locked & versioned | None |

### 2.2 Mode Transition Flow

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  DRAFT  │ ─► │ STAGING │ ─► │ REVIEW  │ ─► │ VERSION │
│   📝    │    │   🔄    │    │   👁️    │    │   ✅    │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
     │              │              │              │
     ▼              ▼              ▼              ▼
  AI active    AI suggests    Human only    Immutable
```

### 2.3 Draft Mode

**Purpose:** Active creation and modification

```yaml
Draft Mode:
  AI Permissions:
    - Create content
    - Suggest edits
    - Auto-complete
    - Generate variations
  
  User Actions:
    - Free editing
    - AI collaboration
    - Iterative refinement
  
  Token Usage: Full
  
  Exit Condition: User promotes to Staging
```

### 2.4 Staging Mode

**Purpose:** Pre-review preparation with AI witness

```yaml
Staging Mode:
  AI Permissions:
    - Suggest improvements (not auto-apply)
    - Highlight issues
    - Calculate token cost
  
  User Actions:
    - Accept/reject suggestions
    - Final adjustments
    - Add review notes
  
  Agent Witness:
    - Nova observes all changes
    - Logs modifications
    - Prepares diff report
  
  Exit Condition: User promotes to Review
```

### 2.5 Review Mode

**Purpose:** Human validation, no AI interference

```yaml
Review Mode:
  AI Permissions:
    - None (read-only)
    - Cannot suggest
    - Cannot modify
  
  User Actions:
    - Read and evaluate
    - Add comments
    - Approve or reject
  
  Governance:
    - Changes tracked
    - Decision logged
    - Approval required
  
  Exit Condition: User approves → Version
```

### 2.6 Version Mode

**Purpose:** Immutable record

```yaml
Version Mode:
  AI Permissions:
    - None
  
  User Actions:
    - View only
    - Compare versions
    - Export
  
  Properties:
    - Immutable content
    - Timestamped
    - Hash-verified
    - Full audit trail
  
  Modify: Create new Draft from Version
```

---

## 3. ACTIONS

### 3.1 Create Actions

| Action | Description | Modes |
|--------|-------------|-------|
| **New** | Create blank item | Draft only |
| **Duplicate** | Copy existing item | Draft only |
| **Generate** | AI-assisted creation | Draft only |
| **Import** | Bring in external data | Draft only |

### 3.2 Transform Actions

| Action | Description | Modes |
|--------|-------------|-------|
| **Edit** | Modify content | Draft, Staging |
| **Format** | Change presentation | Draft, Staging |
| **Convert** | Change type | Draft only |
| **Merge** | Combine items | Draft only |
| **Split** | Divide item | Draft only |

### 3.3 Export Actions

| Action | Description | Modes |
|--------|-------------|-------|
| **Download** | Save locally | All modes |
| **Share** | Generate share link | Review, Version |
| **Print** | Physical output | All modes |
| **API** | External integration | Version only |

---

## 4. AGENT WITNESS SYSTEM

### 4.1 Concept

During Staging mode, an **Agent Witness** observes all changes:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT WITNESS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Who: Nova (always) or assigned agent                           │
│                                                                 │
│  When: Active during Staging mode                               │
│                                                                 │
│  What:                                                          │
│  - Observes all modifications                                   │
│  - Records change timeline                                      │
│  - Generates diff reports                                       │
│  - Calculates token impact                                      │
│  - Notes anomalies                                              │
│                                                                 │
│  Output: Staging Report for Review mode                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Witness Report

```json
{
  "witness_report": {
    "item_id": "uuid",
    "item_type": "note",
    "sphere": "business",
    "witness_agent": "nova",
    "staging_period": {
      "start": "2024-01-01T10:00:00Z",
      "end": "2024-01-01T11:30:00Z",
      "duration_minutes": 90
    },
    "changes": {
      "total_edits": 15,
      "ai_suggestions_shown": 8,
      "ai_suggestions_accepted": 3,
      "ai_suggestions_rejected": 5,
      "human_edits": 7
    },
    "diff_summary": {
      "lines_added": 45,
      "lines_removed": 12,
      "sections_modified": ["introduction", "conclusion"]
    },
    "token_impact": {
      "estimated_at_staging": 250,
      "actual_used": 180
    },
    "anomalies": [],
    "witness_notes": "Clean staging, ready for review"
  }
}
```

---

## 5. DIFF & VERSIONING

### 5.1 Version Structure

```
Item: "Q4 Marketing Plan"
├── v1.0 (2024-01-01) - Initial version
├── v1.1 (2024-01-05) - Minor updates
├── v2.0 (2024-01-15) - Major revision
│   ├── Draft history
│   ├── Staging report
│   ├── Review approval
│   └── Final content
└── v2.1 (2024-01-20) - Current
```

### 5.2 Diff Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    VERSION DIFF                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  v1.0                          v2.0                             │
│  ─────                         ─────                            │
│  Introduction                  Introduction                     │
│  - Basic overview              + Comprehensive overview         │
│                                + Market analysis                │
│  Strategy                      Strategy                         │
│  - Plan A                      - Plan A (unchanged)             │
│  - Plan B                      - Plan B (modified)              │
│                                + Plan C (new)                   │
│                                                                 │
│  Legend: + added  - removed  (unchanged) (modified)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Version Metadata

```yaml
Version Metadata:
  id: "v2.0"
  item_id: "uuid"
  created_at: "2024-01-15T14:30:00Z"
  created_by: "user-uuid"
  
  workflow:
    draft_duration: "4 hours"
    staging_duration: "2 hours"
    review_duration: "30 minutes"
    total_duration: "6.5 hours"
  
  approvals:
    - approver: "user-uuid"
      timestamp: "2024-01-15T14:25:00Z"
      comment: "Approved for release"
  
  tokens:
    ai_tokens_used: 1250
    encoding_savings: 380
    net_cost: 870
  
  hash: "sha256:abc123..."
  
  previous_version: "v1.1"
```

---

## 6. WORKSPACE RULES

### 6.1 Mode Transition Rules

| From | To | Condition |
|------|-----|-----------|
| Draft | Staging | User action |
| Staging | Review | User action + Witness report |
| Review | Version | Approval required |
| Version | Draft | Creates new draft |
| Staging | Draft | User can revert |
| Review | Staging | Rejection with notes |

### 6.2 AI Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI BOUNDARIES BY MODE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Draft:    ████████████████████████  Full AI                    │
│  Staging:  ████████░░░░░░░░░░░░░░░░  Suggestions only           │
│  Review:   ░░░░░░░░░░░░░░░░░░░░░░░░  No AI                      │
│  Version:  ░░░░░░░░░░░░░░░░░░░░░░░░  No AI                      │
│                                                                 │
│  Legend: ████ = Active  ░░░░ = Inactive                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 Governance Integration

Every workspace action is governed:

1. **Token Check** — Sufficient budget?
2. **Permission Check** — User authorized?
3. **Scope Check** — Within sphere?
4. **Rule Check** — Governance rules pass?
5. **Log Action** — Activity recorded

---

## 7. CROSS-SPHERE OPERATIONS

### 7.1 Referencing Across Spheres

Items can **reference** items in other spheres:

```yaml
Cross-Sphere Reference:
  type: "reference"
  source_sphere: "business"
  source_item: "uuid"
  target_sphere: "personal"
  target_item: "uuid"
  
  permissions:
    - Requires governance approval
    - Creates audit trail
    - Read-only by default
```

### 7.2 Moving Items Between Spheres

```
Move Operation:
1. User initiates move
2. Governance validates
3. Create copy in target sphere
4. Update references
5. Archive original (don't delete)
6. Log operation
```

---

## 8. CANONICAL RULES

1. **Four Modes Only** — Draft → Staging → Review → Version
2. **AI Decreases** — AI access decreases through modes
3. **Human Final** — Humans approve all versions
4. **Witness Required** — Staging requires agent witness
5. **Immutable Versions** — Versions cannot be modified
6. **Audit Everything** — All actions logged

---

*CHE·NU™ — Governed Intelligence Operating System*
