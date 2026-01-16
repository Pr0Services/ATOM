# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — HISTORY BIAS AGENT
# Angle-Mort Patch — Rule 3
# ═══════════════════════════════════════════════════════════════════════════════

## Agent Identity

```json
{
  "agent_id": "history-bias",
  "name": "History Bias Corrector",
  "name_fr": "Correcteur de Biais Historique",
  "type": "advisor",
  "level": "L2",
  "emoji": "🔄",
  "status": "active"
}
```

## Purpose

Differentiate true preference from behavioral inertia.
Prevent system from reinforcing stagnation.

## Capabilities

- `detect_stagnation`: Identify unused features
- `suggest_exploration`: Surface underused capabilities
- `dampen_reinforcement`: Reduce echo chamber effect
- `track_feature_usage`: Monitor feature adoption

## Stagnation Detection

```json
{
  "stagnation_signals": {
    "feature_unused_days": 30,
    "repetition_threshold": 10,
    "exploration_score_low": 0.2,
    "same_path_frequency": 0.8
  }
}
```

## Explore Mode

User opt-in mode that surfaces underused features:
- No forced actions
- Gentle suggestions only
- Dismissable permanently
- Tracks what user tries

## Anti-Pattern Rules

1. Never ONLY reinforce existing behavior
2. Periodically suggest alternatives
3. Track discoverability metrics
4. Respect user's "not interested" signals

---

# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — EXPORT COMPLIANCE AGENT
# Angle-Mort Patch — Rule 6
# ═══════════════════════════════════════════════════════════════════════════════

## Agent Identity

```json
{
  "agent_id": "export-compliance",
  "name": "Export Compliance Guardian",
  "name_fr": "Gardien de Conformité Export",
  "type": "guardian",
  "level": "L1",
  "emoji": "📤",
  "status": "active"
}
```

## Purpose

Control all data leaving CHE·NU.
Ensure security, privacy, and traceability.

## Capabilities

- `validate_exports`: Check export requests
- `apply_redactions`: Remove sensitive data
- `add_signatures`: Cryptographic signing
- `track_exports`: Audit trail

## Export Types

| Type | Redaction | Signature |
|------|-----------|-----------|
| `static_pdf` | Applied | Yes |
| `minimal_summary` | Heavy | Yes |
| `context_trimmed` | Applied | Yes |
| `watermarked_share` | Light | Yes |

## Automatic Redactions

- Cross-sphere references
- Personal sphere data (always)
- Sensitive flagged items
- Internal agent communications
- System metadata

## Export Validation

```python
def validate_export(request):
    # Check permissions
    if not user_can_export(request.user, request.source):
        return DENIED("No export permission")
    
    # Apply redactions
    content = apply_redactions(request.content, request.export_type)
    
    # Generate hash
    content_hash = sha256(content)
    
    # Sign
    signature = sign(content_hash, system_key)
    
    # Log
    log_export(request, content_hash, signature)
    
    return APPROVED(content, signature)
```

---

# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — COGNITIVE LOAD AGENT
# Angle-Mort Patch — Rule 7
# ═══════════════════════════════════════════════════════════════════════════════

## Agent Identity

```json
{
  "agent_id": "cognitive-load",
  "name": "Cognitive Load Manager",
  "name_fr": "Gestionnaire de Charge Cognitive",
  "type": "guardian",
  "level": "L1",
  "emoji": "🧘",
  "status": "active"
}
```

## Purpose

Detect stress and reduce cognitive load.
Activate stress mode when needed.

## Capabilities

- `detect_stress_signals`: Monitor user behavior
- `activate_stress_mode`: Trigger simplified UI
- `simplify_ui`: Reduce complexity
- `limit_agent_chatter`: Essential only

## Stress Triggers

| Trigger | Threshold |
|---------|-----------|
| Rapid task switching | > 5/min |
| Error rate | > 3/min |
| Urgency keywords | Detected |
| Negative sentiment | High |
| Manual button | Immediate |

## Stress Mode Effects

```json
{
  "stress_mode_active": {
    "ui": "simplified",
    "agents": "essential_only",
    "notifications": "critical_only",
    "animations": "minimal",
    "memory_logging": "reduced",
    "focus": "current_task"
  }
}
```

## User Controls

- Manual activation/deactivation
- Customize triggers
- Set auto-timeout (default 30 min)
- Override auto-detection

## Stress Mode UI

```
┌─────────────────────────────────────────────────────────────────┐
│  🧘 STRESS MODE ACTIVE                      [Exit Stress Mode]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Current Task: Review Q4 Report                                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                         │    │
│  │              [Simplified Task View]                     │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Essential Actions Only:                                        │
│  [Save] [Complete] [Help]                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## DATABASE TABLES (All Three Agents)

```sql
-- History Bias Agent
CREATE TABLE core.feature_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    feature_id VARCHAR(100) NOT NULL,
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,
    suggestion_shown INTEGER DEFAULT 0,
    suggestion_accepted INTEGER DEFAULT 0,
    marked_not_interested BOOLEAN DEFAULT FALSE,
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

-- Export Compliance Agent
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Cognitive Load Agent
CREATE TABLE core.stress_mode_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    activated_at TIMESTAMP WITH TIME ZONE,
    activation_trigger VARCHAR(50),
    auto_deactivate_minutes INTEGER DEFAULT 30,
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

---

**END OF ANGLE-MORT AGENTS**
