# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — MEETING ROOM 2D (MR-2D)
# Official Canon — First-Class System Primitive
# ═══════════════════════════════════════════════════════════════════════════════

**Version**: 1.0.0
**Status**: CANONICAL
**Priority**: CORE PRIMITIVE

---

## DEFINITION

**Meeting Room 2D (MR-2D)** is a **first-class system primitive** in CHE·NU.

It is a **web/mobile-based cognitive collaboration space** for humans and agents.
MR-2D is the **DEFAULT meeting environment** across all of CHE·NU.

### Critical Rule

> **MR-2D MUST EXIST EVEN IF XR IS NEVER USED.**

MR-2D is NOT optional. It is NOT dependent on XR. It is the authoritative meeting space.

---

## SECTION 1 — MR-2D PROPERTIES

| Property | Value |
|----------|-------|
| **Attachment** | Always attached to exactly ONE sphere |
| **Governance** | Always respects that sphere's domain laws |
| **Mode** | Synchronous AND asynchronous |
| **Recording** | Decisions, rationale, divergences, outcomes |
| **Authority** | **Authoritative** for all decisions |
| **Persistence** | Fully persistent and searchable |
| **Availability** | Always available (web/mobile) |
| **Export** | Primary export source |

---

## SECTION 2 — MR-2D vs XR MEETING ROOM

### Comparison Matrix

| Aspect | Meeting Room 2D | XR Meeting Room |
|--------|-----------------|-----------------|
| **Authority** | ✅ Authoritative for decisions | ❌ Never sole source of truth |
| **Interface** | Textual + visual panels | Spatial + immersive |
| **Cognitive Load** | Low | High |
| **Availability** | Always | Optional extension |
| **Export Source** | Primary | Must sync to MR-2D |
| **Persistence** | Full | Session-based |
| **Searchability** | Full-text search | Replay-based |
| **Required** | YES | NO |

### Critical Rule

> **No XR session is valid unless it can be reconstructed in MR-2D.**

### Synchronization Direction

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYNCHRONIZATION FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   MR-2D ═══════════════════════════════════════════════════►    │
│     │                                                           │
│     │  State, Context, Decisions                                │
│     │                                                           │
│     ▼                                                           │
│   XR Meeting Room                                               │
│     │                                                           │
│     │  Spatial events, Interactions                             │
│     │                                                           │
│     ▼                                                           │
│   MR-2D ◄═══════════════════════════════════════════════════    │
│     │                                                           │
│     │  Replay, Transcription, Decisions                         │
│     │                                                           │
│                                                                 │
│   RULE: XR → MR-2D sync is MANDATORY                           │
│   RULE: MR-2D → XR sync is OPTIONAL                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## SECTION 3 — MR-2D AGENT ECOSYSTEM

### Core Meeting Agents

| Agent | Role | Capabilities |
|-------|------|--------------|
| **Meeting_Orchestrator** | Controls phases, flow, pacing | `start`, `pause`, `advance_phase`, `close` |
| **Agenda_Structuring** | Converts goals into agenda blocks | `create_agenda`, `reorder`, `estimate_time` |
| **Decision_Capture** | Records decisions with metadata | `propose`, `record`, `track_dissent` |
| **Methodology_Agent** | Applies selected methodology | `suggest_framework`, `evaluate_structure` |
| **Consensus_Divergence** | Detects alignment and conflict | `measure_agreement`, `flag_divergence` |
| **Narrative_Agent** | Produces human-readable synthesis | `summarize`, `generate_minutes`, `export` |
| **Nova** | Global mediator, contextual assistant | `assist`, `clarify`, `mediate` |

### Agent Communication Rules

1. **Explicit schemas only** — No hidden state
2. **Logged interactions** — Every agent action recorded
3. **Sphere-bound** — Agents respect sphere's domain laws
4. **Arbitration** — Conflicts go to Decision_Arbiter

### Agent Schema

```json
{
  "agent_id": "meeting-orchestrator",
  "meeting_id": "uuid",
  "sphere_id": "string",
  "action": {
    "type": "advance_phase",
    "from_phase": "discussion",
    "to_phase": "decision",
    "timestamp": "datetime"
  },
  "rationale": "All agenda items discussed, ready for decision",
  "confidence": 0.92
}
```

---

## SECTION 4 — MR-2D STRUCTURE

### Visual Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MEETING ROOM 2D — [Meeting Title]                    [Sphere: Business]   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐  ┌────────────────────────────────────────────────┐  │
│  │ 🎯 OBJECTIVE     │  │ 📋 AGENDA TIMELINE                             │  │
│  │                  │  │                                                │  │
│  │ Decide Q1       │  │ [✓] Opening (5m)                               │  │
│  │ marketing       │  │ [►] Discussion (20m) ◄── Current               │  │
│  │ budget          │  │ [ ] Decision (10m)                              │  │
│  │                  │  │ [ ] Closing (5m)                               │  │
│  └──────────────────┘  └────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 💬 TOPIC THREAD                                                        │ │
│  │                                                                        │ │
│  │ ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │ │ [User] We need to allocate more to digital ads...               │   │ │
│  │ └─────────────────────────────────────────────────────────────────┘   │ │
│  │ ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │ │ [Nova] Based on Q4 data, digital had 23% higher ROI...          │   │ │
│  │ └─────────────────────────────────────────────────────────────────┘   │ │
│  │ ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │ │ [Finance_Agent] Budget constraint: max 150K reallocation...     │   │ │
│  │ └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌──────────────────────────────┐  ┌───────────────────────────────────┐   │
│  │ 📊 DECISION MAP              │  │ 🤖 AGENT ACTIVITY                 │   │
│  │                              │  │                                   │   │
│  │ Proposed: +80K digital      │  │ Meeting_Orchestrator: Active      │   │
│  │ Confidence: 0.78            │  │ Decision_Capture: Monitoring      │   │
│  │ Dissent: Finance (budget)   │  │ Consensus: 72% alignment          │   │
│  │                              │  │                                   │   │
│  └──────────────────────────────┘  └───────────────────────────────────┘   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ 🧠 CONTEXT MEMORY                                                      │ │
│  │ Related: Q4 Review (Dec 5), Marketing Strategy (Nov 20)               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  [📤 Export] [🔄 Sync XR] [⏸️ Pause] [✅ Decision] [❌ Close]              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Required UI Components

| Component | Purpose | Required |
|-----------|---------|----------|
| **Objective Panel** | Display meeting goal | ✅ YES |
| **Agenda Timeline** | Show phases and progress | ✅ YES |
| **Topic Threads** | Threaded discussion | ✅ YES |
| **Decision Map** | Visualize proposals and votes | ✅ YES |
| **Agent Activity** | Show active agents | ✅ YES |
| **Context Memory** | Related meetings and data | ✅ YES |
| **Export Controls** | Export options | ✅ YES |

---

## SECTION 5 — TASK TYPES BY ENVIRONMENT

### MR-2D Supported Tasks

| Task Type | Description | Agents Involved |
|-----------|-------------|-----------------|
| **Planning** | Strategic and tactical planning | Agenda, Methodology, Nova |
| **Decision-making** | Formal decisions with record | Decision_Capture, Consensus, Orchestrator |
| **Reviews** | Performance, project, process review | Methodology, Narrative, Nova |
| **Conflict Resolution** | Dispute mediation | Consensus_Divergence, Arbiter, Nova |
| **Strategy** | High-level direction setting | Methodology, Nova, Domain experts |
| **Async Collaboration** | Non-real-time work | All (async mode) |

### XR Supported Tasks

| Task Type | Description | Limitation |
|-----------|-------------|------------|
| **Spatial Visualization** | 3D data, models, spaces | Visual only |
| **Experiential Review** | Walk-through, inspection | No decisions |
| **Immersive Brainstorm** | Creative spatial ideation | Must sync to MR-2D |
| **Presence Alignment** | Team bonding, presence | Social only |

### Forbidden in XR

- ❌ Authoritative decisions
- ❌ Legal/compliance meetings
- ❌ Sole record of discussion
- ❌ Export without MR-2D sync

---

## SECTION 6 — MR-2D DATA MODEL

### Meeting Schema

```json
{
  "$schema": "chenu://schemas/meeting/v1",
  "meeting_id": "uuid",
  "sphere_id": "string",
  "domain_code": "string",
  
  "title": "string",
  "objective": "string",
  "meeting_type": "planning|decision|review|conflict|strategy|async",
  
  "participants": [
    {
      "type": "human|agent",
      "id": "string",
      "role": "facilitator|participant|observer"
    }
  ],
  
  "agenda": [
    {
      "phase_id": "uuid",
      "title": "string",
      "duration_minutes": 10,
      "status": "pending|active|completed|skipped"
    }
  ],
  
  "threads": [
    {
      "thread_id": "uuid",
      "topic": "string",
      "messages": []
    }
  ],
  
  "decisions": [
    {
      "decision_id": "uuid",
      "proposal": "string",
      "confidence": 0.0-1.0,
      "status": "proposed|approved|rejected|deferred",
      "rationale": "string",
      "dissent": [],
      "recorded_at": "datetime"
    }
  ],
  
  "context_refs": ["meeting_ids"],
  
  "created_at": "datetime",
  "started_at": "datetime",
  "ended_at": "datetime",
  "status": "draft|active|paused|completed|cancelled"
}
```

### Decision Schema

```json
{
  "$schema": "chenu://schemas/decision/v1",
  "decision_id": "uuid",
  "meeting_id": "uuid",
  
  "proposal": "string",
  "proposed_by": "participant_id",
  "proposed_at": "datetime",
  
  "confidence_score": 0.85,
  "risk_level": "low|medium|high|critical",
  
  "votes": [
    {
      "participant_id": "string",
      "vote": "approve|reject|abstain",
      "rationale": "string"
    }
  ],
  
  "dissent": [
    {
      "participant_id": "string",
      "concern": "string",
      "acknowledged": true
    }
  ],
  
  "outcome": "approved|rejected|deferred",
  "recorded_at": "datetime",
  "recorded_by": "decision_capture_agent"
}
```

---

## SECTION 7 — MR-2D APIs

### Core APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/meetings` | POST | Create meeting |
| `/api/meetings/:id` | GET | Get meeting |
| `/api/meetings/:id/attach-sphere` | POST | Attach to sphere |
| `/api/meetings/:id/agents` | POST | Add agent |
| `/api/meetings/:id/agenda` | PUT | Update agenda |
| `/api/meetings/:id/threads` | POST | Create thread |
| `/api/meetings/:id/decisions/propose` | POST | Propose decision |
| `/api/meetings/:id/decisions/:did/record` | POST | Record decision |
| `/api/meetings/:id/export` | GET | Export snapshot |
| `/api/meetings/:id/replay-context` | GET | Get replay context |

### API Schema: Create Meeting

```json
{
  "endpoint": "POST /api/meetings",
  "request": {
    "sphere_id": "string (required)",
    "title": "string (required)",
    "objective": "string (required)",
    "meeting_type": "string (required)",
    "agenda": "array (optional)",
    "participants": "array (optional)"
  },
  "response": {
    "meeting_id": "uuid",
    "status": "draft",
    "created_at": "datetime"
  }
}
```

### API Schema: Propose Decision

```json
{
  "endpoint": "POST /api/meetings/:id/decisions/propose",
  "request": {
    "proposal": "string (required)",
    "proposed_by": "participant_id (required)",
    "rationale": "string (optional)",
    "risk_level": "string (optional)"
  },
  "response": {
    "decision_id": "uuid",
    "status": "proposed",
    "confidence_score": 0.0
  }
}
```

### API Constraints

1. **No API may bypass sphere constraints**
2. **No API may bypass domain constraints**
3. **All APIs require authentication**
4. **All APIs are logged**

---

## SECTION 8 — XR SYNCHRONIZATION

### XR-to-MR-2D APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/xr/enter-space` | POST | Enter XR from MR-2D |
| `/api/xr/sync-state` | POST | Sync current MR-2D state to XR |
| `/api/xr/record-event` | POST | Record spatial event |
| `/api/xr/exit-to-2d` | POST | Exit XR, sync back |
| `/api/xr/replay-to-2d` | POST | Replay XR session to MR-2D |

### Sync Rules

1. **Entry**: XR session MUST start from MR-2D state
2. **During**: Spatial events logged to XR session
3. **Exit**: All events synced back to MR-2D
4. **Replay**: XR session playable in MR-2D timeline

### Replay Schema

```json
{
  "xr_session_id": "uuid",
  "meeting_id": "uuid",
  "events": [
    {
      "timestamp": "datetime",
      "event_type": "spatial_move|gesture|voice|interaction",
      "participant_id": "string",
      "data": {}
    }
  ],
  "transcription": "string",
  "decisions_captured": ["decision_ids"],
  "synced_to_2d_at": "datetime"
}
```

---

## SECTION 9 — DATABASE TABLES

```sql
-- Meeting table
CREATE TABLE meetings.meetings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50) NOT NULL,
    domain_code VARCHAR(50) NOT NULL,
    
    title VARCHAR(500) NOT NULL,
    objective TEXT NOT NULL,
    meeting_type VARCHAR(50) NOT NULL,
    
    participants JSONB DEFAULT '[]',
    agenda JSONB DEFAULT '[]',
    
    status VARCHAR(30) DEFAULT 'draft',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE
);

-- Meeting threads
CREATE TABLE meetings.threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id),
    
    topic VARCHAR(500) NOT NULL,
    messages JSONB DEFAULT '[]',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Decisions
CREATE TABLE meetings.decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id),
    
    proposal TEXT NOT NULL,
    proposed_by VARCHAR(200) NOT NULL,
    proposed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    confidence_score FLOAT,
    risk_level VARCHAR(20),
    
    votes JSONB DEFAULT '[]',
    dissent JSONB DEFAULT '[]',
    
    outcome VARCHAR(30),
    rationale TEXT,
    
    recorded_at TIMESTAMP WITH TIME ZONE,
    recorded_by VARCHAR(100)
);

-- XR sessions linked to meetings
CREATE TABLE meetings.xr_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id),
    
    events JSONB DEFAULT '[]',
    transcription TEXT,
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    synced_to_2d_at TIMESTAMP WITH TIME ZONE
);

-- Agent activity log
CREATE TABLE meetings.agent_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id),
    agent_id VARCHAR(100) NOT NULL,
    
    action JSONB NOT NULL,
    rationale TEXT,
    confidence FLOAT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_meetings_sphere ON meetings.meetings(sphere_id);
CREATE INDEX idx_meetings_status ON meetings.meetings(status);
CREATE INDEX idx_decisions_meeting ON meetings.decisions(meeting_id);
CREATE INDEX idx_decisions_outcome ON meetings.decisions(outcome);
```

---

## SECTION 10 — VALIDATION REQUIREMENTS

### Tests Required

```python
def test_mr2d_exists_without_xr():
    """MR-2D must function without XR"""
    pass

def test_sphere_attachment():
    """Meeting must attach to exactly one sphere"""
    pass

def test_domain_law_enforcement():
    """Meeting respects sphere's domain laws"""
    pass

def test_decision_recording():
    """All decisions have rationale and dissent"""
    pass

def test_xr_sync_mandatory():
    """XR sessions must sync to MR-2D"""
    pass

def test_xr_not_authoritative():
    """XR cannot be sole decision source"""
    pass

def test_agent_explicit_schemas():
    """All agent communication uses explicit schemas"""
    pass

def test_export_from_2d():
    """Export originates from MR-2D only"""
    pass
```

---

## SECTION 11 — ORCHESTRATION RULES

### Execution Patterns

| Pattern | When | Agents |
|---------|------|--------|
| **Chain** | Critical decisions | Sequential, all must agree |
| **Parallel** | Exploration | Concurrent, best wins |
| **Arbiter** | Conflict | Decision_Arbiter resolves |

### Escalation Rules

| Condition | Action |
|-----------|--------|
| Confidence delta < 0.15 | Escalate to user |
| Risk level >= medium | Escalate to user |
| Agent disagreement | Invoke Arbiter |
| Domain boundary | Require bridge |

---

**END OF MEETING ROOM 2D CANON**

*CHE·NU Core Primitive*
*Pro-Service Construction*
