# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — DECISION ARBITER AGENT
# Angle-Mort Patch — Rule 1
# ═══════════════════════════════════════════════════════════════════════════════

## Agent Identity

```json
{
  "agent_id": "decision-arbiter",
  "name": "Decision Arbiter",
  "name_fr": "Arbitre de Décisions",
  "type": "system",
  "level": "L1",
  "emoji": "⚖️",
  "status": "active"
}
```

## Purpose

Resolve conflicts when multiple agents propose contradictory actions.
Ensure consistent, explainable decisions across the ecosystem.

## Capabilities

| Capability | Description |
|------------|-------------|
| `receive_proposals` | Accept proposals from any agent |
| `compare_confidence` | Analyze confidence scores |
| `detect_divergence` | Identify intent conflicts |
| `escalate_to_user` | Request human decision |
| `log_resolutions` | Record all outcomes |
| `replay_decisions` | Enable decision replay |

## Proposal Schema (Required)

All agents MUST submit proposals using this schema:

```json
{
  "$schema": "chenu://schemas/proposal/v1",
  "proposal_id": "uuid",
  "agent_id": "string",
  "sphere_id": "string",
  "timestamp": "ISO8601",
  "proposal": {
    "action": "create|update|delete|move|organize",
    "target_type": "item|category|layout|workflow",
    "target_id": "uuid|null",
    "parameters": {}
  },
  "confidence_score": 0.85,
  "rationale": "string explaining why",
  "risk_level": "low|medium|high|critical",
  "reversible": true,
  "alternatives": [
    {
      "action": "alternative action",
      "confidence_score": 0.65
    }
  ],
  "dependencies": ["other_proposal_ids"],
  "conflicts_with": ["detected_conflicting_proposals"]
}
```

## Escalation Matrix

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Confidence delta | < 0.15 | Escalate to user |
| Risk level | > medium | Escalate to user |
| Intent divergence | Any | Escalate to user |
| Critical operation | Always | Escalate to user |
| All agents agree | Confidence > 0.8 | Auto-resolve |
| Single proposal | Confidence > 0.9, risk low | Auto-resolve |

## Resolution Methods

### 1. Auto-Resolution
When conditions allow automatic resolution:
```
IF all_agents_agree AND avg_confidence > 0.8 AND max_risk <= medium:
    RESOLVE with highest_confidence_proposal
    LOG resolution with full context
```

### 2. User Escalation
Present to user with:
- All proposals side-by-side
- Confidence scores visualized
- Risk assessments
- Agent rationales
- Recommended choice (if any)

### 3. Timeout Resolution
If user doesn't respond within timeout:
```
IF has_safe_default:
    APPLY safe_default
ELSE:
    MAINTAIN current_state
LOG timeout_resolution
```

## Integration Points

### With Organizer Agents
- Receives layout change proposals
- Receives classification proposals
- Receives restructure proposals

### With Methodology Agent
- Receives workflow optimization proposals
- Receives automation proposals

### With Memory Agent
- Receives memory classification proposals
- Receives decay proposals

### With All Agents
- Central proposal registry
- Conflict detection service
- Resolution notification

## Database Tables

```sql
-- Proposal queue
CREATE TABLE core.arbiter_proposals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(100) NOT NULL,
    sphere_id VARCHAR(50),
    
    proposal JSONB NOT NULL,
    confidence_score FLOAT NOT NULL,
    rationale TEXT,
    risk_level VARCHAR(20),
    
    status VARCHAR(30) DEFAULT 'pending',
    conflict_group_id UUID,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Resolution log
CREATE TABLE core.arbiter_resolutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conflict_group_id UUID,
    
    proposals UUID[],
    resolution_type VARCHAR(30),
    resolved_by VARCHAR(50),
    chosen_proposal_id UUID,
    
    rationale TEXT,
    user_feedback TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_arbiter_proposals_status ON core.arbiter_proposals(status);
CREATE INDEX idx_arbiter_proposals_conflict ON core.arbiter_proposals(conflict_group_id);
```

## API Endpoints

```
POST   /api/arbiter/proposals          # Submit proposal
GET    /api/arbiter/proposals/:id      # Get proposal status
GET    /api/arbiter/conflicts          # List active conflicts
POST   /api/arbiter/resolve/:id        # User resolution
GET    /api/arbiter/history            # Resolution history
POST   /api/arbiter/replay/:id         # Replay decision
```

## Conflict Detection Algorithm

```python
def detect_conflicts(new_proposal):
    """
    Detect if new proposal conflicts with pending proposals.
    """
    pending = get_pending_proposals()
    conflicts = []
    
    for existing in pending:
        # Same target
        if existing.target_id == new_proposal.target_id:
            conflicts.append(existing)
            continue
        
        # Overlapping scope
        if scopes_overlap(existing.scope, new_proposal.scope):
            conflicts.append(existing)
            continue
        
        # Intent divergence
        if intents_diverge(existing.intent, new_proposal.intent):
            conflicts.append(existing)
            continue
    
    if conflicts:
        group_id = create_conflict_group([new_proposal] + conflicts)
        return group_id
    
    return None
```

## Simulation Requirements

Must pass 100+ conflict scenarios:

| Scenario Type | Count | Description |
|---------------|-------|-------------|
| Two-agent conflict | 30 | Two agents, same target |
| Multi-agent conflict | 20 | 3+ agents involved |
| Cross-sphere conflict | 20 | Different spheres, related |
| Cascade conflict | 15 | Dependent proposals |
| Edge cases | 15 | Equal confidence, timeouts |

## Metrics

| Metric | Target |
|--------|--------|
| Auto-resolution rate | > 70% |
| User escalation response | < 5 min avg |
| Decision replay success | 100% |
| Conflict detection accuracy | > 95% |

---

**END OF DECISION ARBITER AGENT**
