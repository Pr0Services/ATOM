# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU — UX STABILITY AGENT
# Angle-Mort Patch — Rule 2
# ═══════════════════════════════════════════════════════════════════════════════

## Agent Identity

```json
{
  "agent_id": "ux-stability",
  "name": "UX Stability Guardian",
  "name_fr": "Gardien de Stabilité UX",
  "type": "guardian",
  "level": "L1",
  "emoji": "🛡️",
  "status": "active"
}
```

## Purpose

Prevent excessive UI reconfiguration that disrupts user mental models.
Protect spatial memory and ensure predictable interface behavior.

## Capabilities

| Capability | Description |
|------------|-------------|
| `track_layout_changes` | Monitor all UI changes |
| `enforce_thresholds` | Block excessive changes |
| `manage_freeze_mode` | Handle layout lock |
| `preserve_anchors` | Protect fixed positions |
| `assess_drift` | Detect behavioral drift |

## Default Thresholds

```json
{
  "thresholds": {
    "max_layout_changes_per_day": 5,
    "min_time_between_reorg_hours": 4,
    "max_category_moves_per_week": 10,
    "max_size_changes_per_day": 8,
    "drift_sensitivity": "medium"
  }
}
```

## Freeze Mode

### Activation
- User button: "🔒 Freeze Layout"
- Voice command: "Freeze interface"
- Gesture in XR: Lock motion

### Freeze Levels

| Level | What's Frozen |
|-------|---------------|
| `soft` | Major reorganizations only |
| `medium` | Positions + sizes |
| `hard` | Everything except content |
| `total` | Absolute freeze (emergency) |

### Duration Options
- Until manually unfrozen
- Timed (1h, 4h, 24h, 1 week)
- Until next session
- Context-based (during presentation)

## Spatial Anchors

### What Can Be Anchored
- Sphere positions in Universe View
- Category positions in Sphere View
- Minimap layout
- Toolbar positions
- Frequently used items

### Anchor Schema

```json
{
  "anchor_id": "uuid",
  "user_id": "uuid",
  "element_type": "sphere|category|item|ui_element",
  "element_id": "string",
  "position": {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0
  },
  "size": 1.0,
  "locked_at": "datetime",
  "reason": "user_preference|frequency|importance"
}
```

## Change Evaluation

Before any layout change:

```python
def evaluate_change(change_request):
    """
    Evaluate if layout change should be allowed.
    """
    user_state = get_user_stability_state()
    
    # Check freeze mode
    if user_state.freeze_mode_enabled:
        if change_request.priority < user_state.freeze_level:
            return BLOCKED("Freeze mode active")
    
    # Check daily limit
    if user_state.changes_today >= user_state.max_changes_per_day:
        return BLOCKED("Daily limit reached")
    
    # Check time since last reorg
    if is_major_reorg(change_request):
        hours_since = hours_since_last_reorg(user_state)
        if hours_since < user_state.min_reorg_interval_hours:
            return BLOCKED(f"Too soon since last reorg ({hours_since}h)")
    
    # Check anchors
    if affects_anchor(change_request, user_state.anchors):
        return BLOCKED("Would affect anchored element")
    
    # Allow with logging
    return ALLOWED(log=True)
```

## Drift Detection

### What is Drift?
Gradual, unintended changes that accumulate over time.

### Detection Signals

| Signal | Weight |
|--------|--------|
| Position delta from original | 0.3 |
| Size delta from original | 0.2 |
| Frequency of small changes | 0.2 |
| User correction frequency | 0.3 |

### Drift Response

```json
{
  "drift_response": {
    "low": "log_only",
    "medium": "notify_user",
    "high": "suggest_reset",
    "critical": "auto_freeze"
  }
}
```

## User Controls UI

```
┌─────────────────────────────────────────────────────────────────┐
│  🛡️ Layout Stability                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Freeze Mode: [OFF] [SOFT] [MEDIUM] [HARD]                      │
│                                                                  │
│  Daily Changes: ████░░░░░░ 4/10                                 │
│                                                                  │
│  Anchored Elements: 3                                           │
│  │ ⚓ Business Sphere position                                  │
│  │ ⚓ Minimap location                                          │
│  │ ⚓ Quick Actions toolbar                                     │
│  │ [+ Add Anchor]                                               │
│                                                                  │
│  ┌─────────────────────────────────────────┐                    │
│  │ ⚙️ Advanced Settings                     │                    │
│  │ Max changes/day: [5]                    │                    │
│  │ Min hours between reorg: [4]            │                    │
│  │ Drift sensitivity: [Medium ▼]           │                    │
│  └─────────────────────────────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Database Tables

```sql
CREATE TABLE core.ux_stability_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    
    -- Thresholds (user-customizable)
    max_changes_per_day INTEGER DEFAULT 5,
    min_reorg_interval_hours INTEGER DEFAULT 4,
    drift_sensitivity VARCHAR(20) DEFAULT 'medium',
    
    -- Current state
    changes_today INTEGER DEFAULT 0,
    changes_reset_at DATE DEFAULT CURRENT_DATE,
    last_reorg_at TIMESTAMP WITH TIME ZONE,
    
    -- Freeze mode
    freeze_mode VARCHAR(20) DEFAULT 'off',
    freeze_until TIMESTAMP WITH TIME ZONE,
    freeze_reason TEXT,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE core.spatial_anchors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    
    element_type VARCHAR(50) NOT NULL,
    element_id VARCHAR(200) NOT NULL,
    sphere_id VARCHAR(50),
    
    position JSONB,
    size FLOAT,
    
    locked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    reason VARCHAR(100),
    
    UNIQUE(user_id, element_type, element_id)
);

CREATE TABLE core.layout_changes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    
    change_type VARCHAR(50),
    element_type VARCHAR(50),
    element_id VARCHAR(200),
    sphere_id VARCHAR(50),
    
    before_state JSONB,
    after_state JSONB,
    
    requested_by VARCHAR(100),
    was_blocked BOOLEAN DEFAULT FALSE,
    block_reason TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Integration

### With Organizer Agents
- All layout changes go through UX Stability
- Organizers must submit change proposals
- Blocked changes logged with reason

### With Decision Arbiter
- Major reorganizations create proposals
- Conflicts escalated appropriately

### With Stress Mode
- Auto-freeze during stress mode
- Simplified UI means frozen layout

## Testing Requirements

| Test | Description |
|------|-------------|
| Aggressive drift | 100 small changes in 1 hour |
| Anchor persistence | Verify across sessions |
| Freeze mode | All levels, all durations |
| Threshold enforcement | Edge cases |
| Recovery | Reset to stable state |

---

**END OF UX STABILITY AGENT**
