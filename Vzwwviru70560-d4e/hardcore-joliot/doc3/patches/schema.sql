-- ═══════════════════════════════════════════════════════════════════════════════
-- CHE·NU — ANGLE-MORT PATCH DATABASE SCHEMA
-- All tables required for the 10 rules
-- ═══════════════════════════════════════════════════════════════════════════════

-- =============================================================================
-- RULE 1: DECISION CONFLICT ARBITRATION
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.arbiter_proposals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(100) NOT NULL,
    sphere_id VARCHAR(50),
    
    proposal JSONB NOT NULL,
    confidence_score FLOAT NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    rationale TEXT,
    risk_level VARCHAR(20) CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    
    status VARCHAR(30) DEFAULT 'pending' CHECK (status IN ('pending', 'resolved', 'expired', 'cancelled')),
    conflict_group_id UUID,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS core.arbiter_resolutions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conflict_group_id UUID,
    
    proposals UUID[] NOT NULL,
    resolution_type VARCHAR(30) CHECK (resolution_type IN ('auto', 'user', 'timeout', 'escalated')),
    resolved_by VARCHAR(50),
    chosen_proposal_id UUID,
    
    rationale TEXT,
    user_feedback TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_arbiter_proposals_status ON core.arbiter_proposals(status);
CREATE INDEX IF NOT EXISTS idx_arbiter_proposals_conflict ON core.arbiter_proposals(conflict_group_id);
CREATE INDEX IF NOT EXISTS idx_arbiter_proposals_agent ON core.arbiter_proposals(agent_id);

-- =============================================================================
-- RULE 2: UX STABILITY GUARD
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.ux_stability_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    
    -- Thresholds
    max_changes_per_day INTEGER DEFAULT 5,
    min_reorg_interval_hours INTEGER DEFAULT 4,
    drift_sensitivity VARCHAR(20) DEFAULT 'medium',
    
    -- Current state
    changes_today INTEGER DEFAULT 0,
    changes_reset_at DATE DEFAULT CURRENT_DATE,
    last_reorg_at TIMESTAMP WITH TIME ZONE,
    
    -- Freeze mode
    freeze_mode VARCHAR(20) DEFAULT 'off' CHECK (freeze_mode IN ('off', 'soft', 'medium', 'hard', 'total')),
    freeze_until TIMESTAMP WITH TIME ZONE,
    freeze_reason TEXT,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS core.spatial_anchors (
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

CREATE TABLE IF NOT EXISTS core.layout_changes (
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

CREATE INDEX IF NOT EXISTS idx_layout_changes_user ON core.layout_changes(user_id);
CREATE INDEX IF NOT EXISTS idx_layout_changes_date ON core.layout_changes(created_at);

-- =============================================================================
-- RULE 3: HISTORY BIAS CORRECTION
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.feature_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    feature_id VARCHAR(100) NOT NULL,
    sphere_id VARCHAR(50),
    
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,
    first_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    suggestion_shown INTEGER DEFAULT 0,
    suggestion_accepted INTEGER DEFAULT 0,
    marked_not_interested BOOLEAN DEFAULT FALSE,
    
    UNIQUE(user_id, feature_id)
);

CREATE TABLE IF NOT EXISTS core.exploration_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    features_surfaced TEXT[],
    features_tried TEXT[]
);

CREATE INDEX IF NOT EXISTS idx_feature_usage_user ON core.feature_usage(user_id);
CREATE INDEX IF NOT EXISTS idx_feature_usage_last ON core.feature_usage(last_used_at);

-- =============================================================================
-- RULE 4: MEMORY WEIGHT AND SILENT ZONES
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.memory_classification (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id UUID NOT NULL,
    classification VARCHAR(20) NOT NULL CHECK (classification IN ('ephemeral', 'persistent', 'critical', 'forbidden')),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    decay_started_at TIMESTAMP WITH TIME ZONE,
    is_decayed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS core.silent_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    was_no_trace BOOLEAN DEFAULT TRUE,
    verified_clean BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS core.forbidden_patterns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pattern_type VARCHAR(100) NOT NULL,
    description TEXT,
    applies_to TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_memory_classification_type ON core.memory_classification(classification);
CREATE INDEX IF NOT EXISTS idx_memory_classification_expires ON core.memory_classification(expires_at);

-- =============================================================================
-- RULE 5: MULTI-USER GOVERNANCE
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.sphere_governance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50) NOT NULL,
    
    owner_user_id UUID NOT NULL,
    governance_type VARCHAR(30) DEFAULT 'owner_decision',
    
    conflict_resolution_method VARCHAR(30) CHECK (conflict_resolution_method IN ('owner_decision', 'vote', 'arbiter')),
    vote_threshold FLOAT DEFAULT 0.5,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS core.sphere_authorities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50) NOT NULL,
    user_id UUID NOT NULL,
    authority_level VARCHAR(30) NOT NULL CHECK (authority_level IN ('owner', 'delegated_editor', 'view_only', 'guest')),
    
    delegated_by UUID,
    delegated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(sphere_id, user_id)
);

CREATE TABLE IF NOT EXISTS core.governance_conflicts (
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

-- =============================================================================
-- RULE 6: EXTERNAL EXPORT PROTOCOL
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.export_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    
    export_type VARCHAR(50) CHECK (export_type IN ('static_pdf', 'minimal_summary', 'context_trimmed', 'watermarked_share')),
    source_sphere VARCHAR(50),
    source_items UUID[],
    
    redactions_applied TEXT[],
    content_hash VARCHAR(64) NOT NULL,
    signature TEXT NOT NULL,
    
    recipient TEXT,
    recipient_type VARCHAR(30),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS core.export_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50) UNIQUE,
    
    allowed_types TEXT[],
    auto_redact_patterns JSONB,
    require_approval BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_export_log_user ON core.export_log(user_id);
CREATE INDEX IF NOT EXISTS idx_export_log_date ON core.export_log(created_at);

-- =============================================================================
-- RULE 7: STRESS MODE
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.stress_mode_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    
    is_active BOOLEAN DEFAULT FALSE,
    activated_at TIMESTAMP WITH TIME ZONE,
    activation_trigger VARCHAR(50),
    
    auto_deactivate_after_minutes INTEGER DEFAULT 30,
    manual_override BOOLEAN DEFAULT FALSE,
    
    -- Custom thresholds
    task_switch_threshold INTEGER DEFAULT 5,
    error_rate_threshold INTEGER DEFAULT 3,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS core.stress_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    signal_type VARCHAR(50),
    signal_value FLOAT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stress_signals_user ON core.stress_signals(user_id);
CREATE INDEX IF NOT EXISTS idx_stress_signals_date ON core.stress_signals(detected_at);

-- =============================================================================
-- RULE 8: GOVERNANCE OF UPDATES
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.governance_changes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    change_type VARCHAR(50) NOT NULL CHECK (change_type IN ('law', 'schema', 'behavior', 'config')),
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

CREATE TABLE IF NOT EXISTS core.system_version (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version VARCHAR(20) NOT NULL,
    changes UUID[],
    released_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_governance_changes_type ON core.governance_changes(change_type);
CREATE INDEX IF NOT EXISTS idx_governance_changes_date ON core.governance_changes(created_at);

-- =============================================================================
-- RULE 9: EXTERNAL INTERPRETATION LAYER
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.external_representations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    context_type VARCHAR(50) NOT NULL CHECK (context_type IN ('investor', 'public', 'demo', 'partner')),
    
    source_sphere VARCHAR(50),
    source_item_id UUID,
    
    simplified_title TEXT,
    simplified_description TEXT,
    abstracted_visuals JSONB,
    
    internal_truth_hash VARCHAR(64),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_external_rep_context ON core.external_representations(context_type);

-- =============================================================================
-- RULE 10: EMERGENCY AND CONTRADICTION PROTOCOL
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.emergency_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    
    detection_source VARCHAR(100),
    affected_components TEXT[],
    
    diagnostic_report JSONB,
    
    user_notified BOOLEAN DEFAULT FALSE,
    user_notified_at TIMESTAMP WITH TIME ZONE,
    
    resolution JSONB,
    resolved_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS core.safe_defaults (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    component VARCHAR(100) UNIQUE NOT NULL,
    default_state JSONB NOT NULL,
    last_validated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_emergency_events_severity ON core.emergency_events(severity);
CREATE INDEX IF NOT EXISTS idx_emergency_events_unresolved ON core.emergency_events(resolved_at) WHERE resolved_at IS NULL;

-- =============================================================================
-- VERIFICATION
-- =============================================================================

-- Count all tables created
DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'core'
    AND table_name IN (
        'arbiter_proposals', 'arbiter_resolutions',
        'ux_stability_state', 'spatial_anchors', 'layout_changes',
        'feature_usage', 'exploration_sessions',
        'memory_classification', 'silent_sessions', 'forbidden_patterns',
        'sphere_governance', 'sphere_authorities', 'governance_conflicts',
        'export_log', 'export_policies',
        'stress_mode_state', 'stress_signals',
        'governance_changes', 'system_version',
        'external_representations',
        'emergency_events', 'safe_defaults'
    );
    
    RAISE NOTICE 'Angle-Mort Patch: % tables created/verified', table_count;
END $$;
