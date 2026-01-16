# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — ANGLE-MORT TO RULESET PATCH
# System Update — Close All Remaining Blind Spots
# ═══════════════════════════════════════════════════════════════════════════════

**Version**: 1.0.0
**Status**: CANONICAL
**Applies To**: All agents, orchestration, UI/UX, memory, XR, database, narrative

---

## PATCH OVERVIEW

This patch closes all identified blind spots in CHE·NU architecture.
Each rule is translated into enforceable logic across the ecosystem.

| Rule | Name | New Agent Required |
|------|------|-------------------|
| 1 | Decision Conflict Arbitration | ✅ Decision_Arbiter_Agent |
| 2 | UX Stability Guard | ✅ UX_Stability_Agent |
| 3 | History Bias Correction | ✅ History_Bias_Agent |
| 4 | Memory Weight and Silent Zones | Update Memory_Agent |
| 5 | Multi-User Governance | Update Team Sphere |
| 6 | External Export Protocol | ✅ Export_Compliance_Agent |
| 7 | Stress Mode | ✅ Cognitive_Load_Agent |
| 8 | Governance of Updates | Update Core System |
| 9 | External Interpretation Layer | Update Narrative System |
| 10 | Emergency and Contradiction Protocol | Update Orchestration |

---

## RULE 1 — DECISION CONFLICT ARBITRATION

### Purpose
Resolve conflicts when multiple agents propose contradictory actions.

### New Agent: `Decision_Arbiter_Agent`

```json
{
  "agent_id": "decision-arbiter",
  "type": "system",
  "level": "L1",
  "capabilities": [
    "receive_proposals",
    "compare_confidence",
    "detect_divergence",
    "escalate_to_user",
    "log_resolutions"
  ]
}
```

### Proposal Schema (All Agents Must Use)

```json
{
  "$schema": "chenu://schemas/proposal/v1",
  "proposal_id": "uuid",
  "agent_id": "string",
  "timestamp": "datetime",
  "proposal": {
    "action": "string",
    "target": "string",
    "parameters": {}
  },
  "confidence_score": 0.0-1.0,
  "rationale": "string",
  "risk_level": "low|medium|high|critical",
  "alternatives": []
}
```

### Escalation Rules

| Condition | Action |
|-----------|--------|
| Confidence delta < 0.15 | Escalate to user |
| Risk level > medium | Escalate to user |
| Intent divergence detected | Escalate to user |
| All agents agree | Auto-resolve (log) |

### Resolution Log Schema

```sql
CREATE TABLE core.decision_resolutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proposals JSONB NOT NULL,
    resolution_type VARCHAR(30),
    resolved_by VARCHAR(50),
    chosen_proposal_id UUID,
    rationale TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Validation Requirement
- Simulate 100+ conflict scenarios across spheres
- Test edge cases: equal confidence, multi-agent conflicts
- Verify replay capability

---

## RULE 2 — UX STABILITY GUARD

### Purpose
Prevent excessive UI reconfiguration that disrupts user mental models.

### New Agent: `UX_Stability_Agent`

```json
{
  "agent_id": "ux-stability",
  "type": "guardian",
  "level": "L1",
  "capabilities": [
    "track_layout_changes",
    "enforce_thresholds",
    "manage_freeze_mode",
    "preserve_anchors"
  ]
}
```

### Stability Thresholds

```json
{
  "max_layout_changes_per_day": 5,
  "min_time_between_reorg_hours": 4,
  "anchor_protection": true,
  "freeze_mode_available": true
}
```

### Database Extension

```sql
CREATE TABLE core.ux_stability (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    sphere_id VARCHAR(50),
    
    -- Thresholds
    max_changes_per_day INTEGER DEFAULT 5,
    min_reorg_interval_hours INTEGER DEFAULT 4,
    
    -- State
    changes_today INTEGER DEFAULT 0,
    last_reorg_at TIMESTAMP WITH TIME ZONE,
    freeze_mode_enabled BOOLEAN DEFAULT FALSE,
    freeze_until TIMESTAMP WITH TIME ZONE,
    
    -- Anchors (positions that must not move)
    spatial_anchors JSONB DEFAULT '[]',
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE core.layout_change_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    sphere_id VARCHAR(50),
    change_type VARCHAR(50),
    before_state JSONB,
    after_state JSONB,
    requested_by VARCHAR(100),
    was_blocked BOOLEAN DEFAULT FALSE,
    block_reason TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### User Controls

| Control | Description |
|---------|-------------|
| Freeze Layout | Lock all positions |
| Set Anchors | Mark immovable elements |
| Adjust Thresholds | Custom limits |
| Override | One-time bypass |

### Validation Requirement
- Test with aggressive behavioral drift simulation
- Verify anchors persist across sessions
- Test freeze mode edge cases

---

## RULE 3 — HISTORY BIAS CORRECTION

### Purpose
Differentiate true preference from behavioral inertia.

### New Agent: `History_Bias_Agent`

```json
{
  "agent_id": "history-bias",
  "type": "advisor",
  "level": "L2",
  "capabilities": [
    "detect_stagnation",
    "suggest_exploration",
    "dampen_reinforcement",
    "track_feature_usage"
  ]
}
```

### Preference Exploration Dampener

```json
{
  "dampener_config": {
    "repetition_threshold": 10,
    "exploration_suggestion_interval_days": 7,
    "force_exploration": false,
    "surface_unseen_features": true
  }
}
```

### Explore Mode

| Feature | Behavior |
|---------|----------|
| Activation | User opt-in |
| Duration | Session or timed |
| Effect | Surface underused features |
| Pressure | None (suggestions only) |

### Database Extension

```sql
CREATE TABLE core.feature_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    feature_id VARCHAR(100) NOT NULL,
    sphere_id VARCHAR(50),
    
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,
    first_used_at TIMESTAMP WITH TIME ZONE,
    
    -- Discovery tracking
    was_suggested BOOLEAN DEFAULT FALSE,
    suggestion_count INTEGER DEFAULT 0,
    suggestion_accepted INTEGER DEFAULT 0,
    
    UNIQUE(user_id, feature_id)
);

CREATE TABLE core.exploration_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    features_surfaced TEXT[],
    features_tried TEXT[]
);
```

### Anti-Stagnation Rules
1. Never reinforce stagnation exclusively
2. Periodically surface underused features
3. No forced adoption
4. Track discoverability over time

---

## RULE 4 — MEMORY WEIGHT AND SILENT ZONES

### Purpose
Classify memory and enable complete privacy modes.

### Memory Classification

| Type | Retention | Description |
|------|-----------|-------------|
| `ephemeral` | Session only | Deleted on exit |
| `persistent` | Until deleted | User-controlled |
| `critical` | Protected | Cannot auto-delete |
| `forbidden` | Never stored | No-trace items |

### No-Trace Sessions

```json
{
  "session_config": {
    "no_trace_mode": true,
    "memory_writes": "blocked",
    "indexing": "disabled",
    "export_allowed": false,
    "audit_log": "minimal"
  }
}
```

### Memory Decay Rules

```json
{
  "decay_config": {
    "ephemeral_ttl_hours": 0,
    "short_term_ttl_days": 7,
    "standard_decay_days": 90,
    "critical_decay": "never",
    "decay_check_interval_hours": 24
  }
}
```

### Database Extension

```sql
CREATE TABLE core.memory_classification (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id UUID NOT NULL,
    classification VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    decay_started_at TIMESTAMP WITH TIME ZONE,
    is_decayed BOOLEAN DEFAULT FALSE
);

CREATE TABLE core.silent_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    was_no_trace BOOLEAN DEFAULT TRUE
);

-- Forbidden memory types (never written)
CREATE TABLE core.forbidden_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pattern_type VARCHAR(100),
    description TEXT,
    applies_to TEXT[]
);
```

### Validation Requirement
- Test total absence of persistence in silent sessions
- Verify forbidden memory is never written/indexed/exported
- Test decay timing accuracy

---

## RULE 5 — MULTI-USER GOVERNANCE

### Purpose
Define explicit ownership and authority for shared spheres.

### Governance Roles

| Role | Authority |
|------|-----------|
| `owner` | Full control, final decision |
| `delegated_editor` | Can modify, not delete |
| `view_only` | Read access only |
| `guest` | Temporary limited access |

### Conflict Resolution Protocol

```json
{
  "conflict_resolution": {
    "methods": ["owner_decision", "vote", "arbiter"],
    "default_method": "owner_decision",
    "vote_threshold": 0.5,
    "arbiter_agent": "decision-arbiter",
    "timeout_hours": 24
  }
}
```

### Database Extension

```sql
CREATE TABLE core.sphere_governance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50) NOT NULL,
    
    owner_user_id UUID NOT NULL,
    governance_type VARCHAR(30) DEFAULT 'owner_decision',
    
    conflict_resolution_method VARCHAR(30),
    vote_threshold FLOAT DEFAULT 0.5,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE core.sphere_authorities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50) NOT NULL,
    user_id UUID NOT NULL,
    authority_level VARCHAR(30) NOT NULL,
    delegated_by UUID,
    delegated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(sphere_id, user_id)
);

CREATE TABLE core.governance_conflicts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50),
    conflict_type VARCHAR(50),
    parties JSONB,
    proposed_changes JSONB,
    resolution_method VARCHAR(30),
    resolution JSONB,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Disagreement Visibility
- Conflicts are visible to all parties
- No forced consensus
- Clear audit trail

---

## RULE 6 — EXTERNAL EXPORT PROTOCOL

### Purpose
Control all data leaving CHE·NU.

### New Agent: `Export_Compliance_Agent`

```json
{
  "agent_id": "export-compliance",
  "type": "guardian",
  "level": "L1",
  "capabilities": [
    "validate_exports",
    "apply_redactions",
    "add_signatures",
    "track_exports"
  ]
}
```

### Supported Export Types

| Type | Description | Redaction |
|------|-------------|-----------|
| `static_pdf` | PDF snapshot | Applied |
| `minimal_summary` | Brief summary | Heavy |
| `context_trimmed` | Narrative without links | Applied |
| `watermarked_share` | With ownership mark | Light |

### Export Schema

```json
{
  "export_id": "uuid",
  "export_type": "string",
  "source_sphere": "string",
  "source_items": ["uuid"],
  "requested_by": "uuid",
  "requested_at": "datetime",
  "redactions_applied": ["string"],
  "hash": "sha256",
  "signature": "string",
  "recipient": "string|null"
}
```

### Database Extension

```sql
CREATE TABLE core.export_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    export_type VARCHAR(50),
    source_sphere VARCHAR(50),
    source_items UUID[],
    
    redactions_applied TEXT[],
    content_hash VARCHAR(64),
    signature TEXT,
    
    recipient TEXT,
    recipient_type VARCHAR(30),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE core.export_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50),
    
    allowed_types TEXT[],
    auto_redact_patterns JSONB,
    require_approval BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Security Requirements
- Cryptographic hashing (SHA-256)
- Digital signatures
- Redact sensitive/cross-sphere data by default
- Validate exports cannot leak unintended context

---

## RULE 7 — STRESS MODE

### Purpose
Reduce cognitive load during high-stress periods.

### New Agent: `Cognitive_Load_Agent`

```json
{
  "agent_id": "cognitive-load",
  "type": "guardian",
  "level": "L1",
  "capabilities": [
    "detect_stress_signals",
    "activate_stress_mode",
    "simplify_ui",
    "limit_agent_chatter"
  ]
}
```

### Stress Detection Triggers

| Trigger | Threshold |
|---------|-----------|
| Rapid task switching | > 5 switches/minute |
| Urgency signals | Keywords, deadlines |
| Negative sentiment | Detected frustration |
| Error rate | > 3 errors/minute |
| Manual activation | User button |

### Stress Mode Effects

```json
{
  "stress_mode": {
    "ui_simplification": true,
    "agent_chatter_limit": "essential_only",
    "priority_focus": "current_task",
    "animation_reduction": true,
    "memory_logging": "minimal",
    "notifications": "critical_only"
  }
}
```

### Database Extension

```sql
CREATE TABLE core.stress_mode_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    
    is_active BOOLEAN DEFAULT FALSE,
    activated_at TIMESTAMP WITH TIME ZONE,
    activation_trigger VARCHAR(50),
    
    auto_deactivate_after_minutes INTEGER DEFAULT 30,
    manual_override BOOLEAN DEFAULT FALSE,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE core.stress_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    signal_type VARCHAR(50),
    signal_value FLOAT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### User Controls
- Manual activation/deactivation
- Override auto-detection
- Customize thresholds
- Set duration

---

## RULE 8 — GOVERNANCE OF UPDATES

### Purpose
Version and audit all changes to laws, schemas, or core behavior.

### Change Record Schema

```json
{
  "change_id": "uuid",
  "change_type": "law|schema|behavior|config",
  "author": "string",
  "reason": "string",
  "timestamp": "datetime",
  "affected_components": ["string"],
  "before_hash": "sha256",
  "after_hash": "sha256",
  "approved_by": "uuid|null",
  "approval_timestamp": "datetime|null"
}
```

### Database Extension

```sql
CREATE TABLE core.governance_changes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    change_type VARCHAR(50) NOT NULL,
    component_path TEXT NOT NULL,
    
    author VARCHAR(100) NOT NULL,
    reason TEXT NOT NULL,
    
    before_state JSONB,
    after_state JSONB,
    before_hash VARCHAR(64),
    after_hash VARCHAR(64),
    
    requires_approval BOOLEAN DEFAULT TRUE,
    approved_by UUID,
    approved_at TIMESTAMP WITH TIME ZONE,
    
    applied_at TIMESTAMP WITH TIME ZONE,
    rolled_back_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE core.system_version (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version VARCHAR(20) NOT NULL,
    changes UUID[],
    released_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Version Mismatch Warning
- Detect when running components have different versions
- Alert user before operations
- Prevent silent rule evolution

---

## RULE 9 — EXTERNAL INTERPRETATION LAYER

### Purpose
Simplify external-facing representations.

### External Contexts

| Context | Simplification Level |
|---------|---------------------|
| `investor` | High (abstract) |
| `public` | High (marketing) |
| `demo` | Medium (showcase) |
| `partner` | Low (technical) |

### Interpretation Rules

```json
{
  "external_layer": {
    "ontology": "simplified",
    "visuals": "abstract",
    "agent_exposure": "limited",
    "narrative": "clear",
    "technical_depth": "minimal",
    "internal_complexity": "hidden"
  }
}
```

### Database Extension

```sql
CREATE TABLE core.external_representations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    context_type VARCHAR(50) NOT NULL,
    
    source_sphere VARCHAR(50),
    source_item_id UUID,
    
    simplified_title TEXT,
    simplified_description TEXT,
    abstracted_visuals JSONB,
    
    internal_truth_hash VARCHAR(64),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Consistency Requirement
- External representation must be consistent with internal truth
- No misleading abstractions
- Traceable back to source

---

## RULE 10 — EMERGENCY AND CONTRADICTION PROTOCOL

### Purpose
Handle system instability safely.

### Contradiction Detection

| Type | Detection Method |
|------|------------------|
| Law conflict | Rule comparison |
| Agent conflict | Proposal analysis |
| Narrative conflict | Story consistency |
| Data conflict | State validation |

### Emergency Response

```json
{
  "emergency_protocol": {
    "trigger": "contradiction_or_instability",
    "actions": [
      "halt_automated_execution",
      "generate_diagnostic_report",
      "notify_user",
      "fallback_to_safe_defaults"
    ],
    "auto_correction": "disabled",
    "require_explicit_validation": true
  }
}
```

### Database Extension

```sql
CREATE TABLE core.emergency_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    
    detection_source VARCHAR(100),
    affected_components TEXT[],
    
    diagnostic_report JSONB,
    
    user_notified BOOLEAN DEFAULT FALSE,
    user_notified_at TIMESTAMP WITH TIME ZONE,
    
    resolution JSONB,
    resolved_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE core.safe_defaults (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    component VARCHAR(100) UNIQUE NOT NULL,
    default_state JSONB NOT NULL,
    last_validated_at TIMESTAMP WITH TIME ZONE
);
```

### Critical Rule
**NO automatic correction without explicit user validation**

---

## NEW AGENTS SUMMARY

| Agent ID | Type | Level | Primary Function |
|----------|------|-------|------------------|
| `decision-arbiter` | system | L1 | Resolve agent conflicts |
| `ux-stability` | guardian | L1 | Protect UI stability |
| `history-bias` | advisor | L2 | Prevent stagnation |
| `export-compliance` | guardian | L1 | Control data export |
| `cognitive-load` | guardian | L1 | Manage stress mode |

---

## INTEGRATION CHECKLIST

### Agents
- [ ] Decision_Arbiter_Agent created and integrated
- [ ] UX_Stability_Agent created and integrated
- [ ] History_Bias_Agent created and integrated
- [ ] Export_Compliance_Agent created and integrated
- [ ] Cognitive_Load_Agent created and integrated

### Database
- [ ] All new tables created
- [ ] Indexes optimized
- [ ] Migration scripts ready

### UI Components
- [ ] Universe View updated for stability
- [ ] Sphere View updated for stability
- [ ] Minimap anchors supported
- [ ] Stress mode UI implemented
- [ ] Freeze Layout control added

### Testing
- [ ] 100+ conflict scenarios simulated
- [ ] Aggressive drift tested
- [ ] Memory suppression verified
- [ ] Export redaction validated
- [ ] XR replay integrity checked

---

## FINAL VALIDATION

Before deployment, verify:

1. ✅ Consistency checks pass
2. ✅ Inheritance propagation works
3. ✅ Stress simulations pass
4. ✅ Multi-agent conflict tests pass
5. ✅ XR replay validation passes
6. ✅ Explainability checks pass

**The system must ALWAYS be able to explain how a decision was made.**

---

**END OF ANGLE-MORT PATCH**

*CHE·NU System Update — Canonical*
*Pro-Service Construction*
