-- ═══════════════════════════════════════════════════════════════════════════════
-- CHE·NU — DOMAIN ARCHITECTURE DATABASE SCHEMA
-- Domain → Department → Sphere + Meeting Room 2D
-- ═══════════════════════════════════════════════════════════════════════════════

-- =============================================================================
-- DOMAINS
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.domains (
    code VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_fr VARCHAR(100) NOT NULL,
    
    primary_objective TEXT NOT NULL,
    allowed_tasks TEXT[] NOT NULL,
    forbidden_tasks TEXT[] NOT NULL,
    
    primary_apis TEXT[] NOT NULL,
    secondary_apis TEXT[],
    
    data_sensitivity VARCHAR(20) NOT NULL 
        CHECK (data_sensitivity IN ('low', 'medium', 'high', 'critical')),
    
    default_agents TEXT[] NOT NULL,
    allowed_meeting_types TEXT[] NOT NULL,
    export_permissions VARCHAR(30) NOT NULL,
    
    special_properties JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert domains
INSERT INTO core.domains (code, name, name_fr, primary_objective, allowed_tasks, forbidden_tasks, 
                          primary_apis, secondary_apis, data_sensitivity, default_agents, 
                          allowed_meeting_types, export_permissions)
VALUES
('PERSONAL', 'Personal', 'Personnel',
 'Protect identity, privacy, wellbeing',
 ARRAY['Self-reflection', 'journaling', 'health tracking', 'personal finance', 'preferences'],
 ARRAY['External sharing without consent', 'monetization of personal data'],
 ARRAY['Identity_API', 'Health_API', 'Memory_API', 'Preferences_API'],
 ARRAY['Calendar_Personal', 'Notes_API'],
 'critical',
 ARRAY['Identity_Guardian', 'Preference_Agent', 'Health_Monitor'],
 ARRAY['Self-reflection', 'Personal planning'],
 'restricted'),

('BUSINESS', 'Business', 'Affaires',
 'Generate value, manage operations, ensure profitability',
 ARRAY['CRM', 'forecasting', 'project management', 'invoicing', 'reporting'],
 ARRAY['Personal data exploitation', 'non-compliant practices'],
 ARRAY['CRM_API', 'Project_Management', 'Invoicing', 'Analytics'],
 ARRAY['Calendar', 'Communication', 'Document_Management'],
 'high',
 ARRAY['CRM_Agent', 'Project_Agent', 'Finance_Agent', 'Sales_Agent'],
 ARRAY['Strategy', 'Planning', 'Review', 'Decision', 'Negotiation'],
 'controlled'),

('SCHOLAR', 'Scholar', 'Académique',
 'Learning, knowledge acquisition, research',
 ARRAY['Learning paths', 'exploration', 'citation', 'research', 'tutoring'],
 ARRAY['Plagiarism', 'credential falsification'],
 ARRAY['Knowledge_Graph', 'Citation', 'Learning_Path', 'Quiz'],
 ARRAY['Document_Analysis', 'Search'],
 'medium',
 ARRAY['Tutor_Agent', 'Knowledge_Curator', 'Research_Agent'],
 ARRAY['Learning session', 'Study group', 'Research discussion'],
 'open'),

('CREATIVE', 'Creative', 'Créatif',
 'Artistic creation, divergent thinking, generation',
 ARRAY['Ideation', 'generation', 'rendering', 'composition', 'exploration'],
 ARRAY['Copyright infringement', 'unauthorized reproduction'],
 ARRAY['Image_Gen', 'Audio_Gen', 'Video_Gen', 'Text_Gen'],
 ARRAY['Asset_Management', 'Versioning'],
 'medium',
 ARRAY['Render_Agent', 'Audio_Agent', 'Video_Agent', 'Ideation_Agent'],
 ARRAY['Brainstorm', 'Creative review', 'Critique'],
 'flexible'),

('SOCIAL', 'Social', 'Social',
 'Human connection, expression, community building',
 ARRAY['Posting', 'engagement', 'trend analysis', 'community management'],
 ARRAY['Harassment', 'manipulation', 'misinformation'],
 ARRAY['Social_Platforms', 'Analytics', 'Scheduling', 'Messaging'],
 ARRAY['Content_Creation', 'Audience_Analysis'],
 'medium',
 ARRAY['Social_Poster', 'Trend_Analyzer', 'Community_Agent'],
 ARRAY['Content planning', 'Community sync', 'Campaign review'],
 'public-ready'),

('INSTITUTIONAL', 'Institutional', 'Institutionnel',
 'Compliance, governance, regulatory adherence',
 ARRAY['Compliance checking', 'audit trails', 'certification', 'reporting'],
 ARRAY['Circumventing regulations', 'falsifying records'],
 ARRAY['Compliance_Check', 'Audit_Log', 'Certification', 'Reporting'],
 ARRAY['Document_Management', 'Workflow'],
 'critical',
 ARRAY['Compliance_Agent', 'Audit_Agent', 'Regulatory_Agent'],
 ARRAY['Audit', 'Compliance review', 'Governance', 'Board meeting'],
 'strict'),

('METHODOLOGY', 'Methodology', 'Méthodologie',
 'Process evaluation, optimization, decision quality',
 ARRAY['Framework application', 'process analysis', 'methodology selection'],
 ARRAY[]::TEXT[],
 ARRAY['Framework_Library', 'Process_Analysis', 'Quality_Metrics'],
 ARRAY['All domain APIs (read-only)'],
 'low',
 ARRAY['Methodology_Agent', 'Strategy_Agent', 'Arbiter_Agent'],
 ARRAY['Process review', 'Methodology selection', 'Retrospective'],
 'open'),

('XR', 'XR / Immersive', 'XR / Immersif',
 'Spatial experience, immersive collaboration',
 ARRAY['Spatial visualization', 'immersive meetings', 'presence-based work'],
 ARRAY['Authoritative decisions without 2D backup'],
 ARRAY['XR_Rendering', 'Spatial_Audio', 'Hand_Tracking', 'Replay'],
 ARRAY['Sync_with_2D', 'Session_Recording'],
 'medium',
 ARRAY['XR_Meeting_Agent', 'Spatial_Agent', 'Replay_Agent'],
 ARRAY['Immersive review', 'Spatial brainstorm', 'Presence session'],
 'derived')
ON CONFLICT (code) DO NOTHING;

-- =============================================================================
-- DEPARTMENTS
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain_code VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    
    code VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    name_fr VARCHAR(200) NOT NULL,
    
    workflows TEXT[] NOT NULL,
    available_apis TEXT[] NOT NULL,
    kpis JSONB,
    
    additional_constraints JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(domain_code, code)
);

CREATE INDEX IF NOT EXISTS idx_departments_domain ON core.departments(domain_code);

-- =============================================================================
-- SPHERES (User Instances)
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.sphere_instances (
    id VARCHAR(50) PRIMARY KEY,
    user_id UUID NOT NULL,
    domain_code VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    
    name VARCHAR(200) NOT NULL,
    name_fr VARCHAR(200),
    
    active_departments UUID[],
    
    database_namespace VARCHAR(100) NOT NULL UNIQUE,
    
    organizer_agent_id VARCHAR(100),
    memory_context_id UUID,
    
    ui_state JSONB DEFAULT '{}',
    preferences JSONB DEFAULT '{}',
    
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sphere_instances_user ON core.sphere_instances(user_id);
CREATE INDEX IF NOT EXISTS idx_sphere_instances_domain ON core.sphere_instances(domain_code);

-- =============================================================================
-- CROSS-DOMAIN BRIDGES
-- =============================================================================

CREATE TABLE IF NOT EXISTS core.domain_bridges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    source_domain VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    target_domain VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    
    access_type VARCHAR(20) NOT NULL CHECK (access_type IN ('read', 'write', 'sync')),
    data_scope TEXT[] NOT NULL,
    
    authorized_by UUID NOT NULL,
    authorized_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    
    is_active BOOLEAN DEFAULT TRUE,
    revoked_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(source_domain, target_domain, access_type)
);

CREATE TABLE IF NOT EXISTS core.bridge_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bridge_id UUID NOT NULL REFERENCES core.domain_bridges(id),
    
    operation VARCHAR(50) NOT NULL,
    data_transferred JSONB,
    
    source_sphere_id VARCHAR(50),
    target_sphere_id VARCHAR(50),
    
    performed_by UUID,
    performed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bridge_audit_bridge ON core.bridge_audit_log(bridge_id);
CREATE INDEX IF NOT EXISTS idx_bridge_audit_date ON core.bridge_audit_log(performed_at);

-- =============================================================================
-- MEETING ROOM 2D SCHEMA
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS meetings;

-- Main meetings table
CREATE TABLE IF NOT EXISTS meetings.meetings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id VARCHAR(50) NOT NULL,
    domain_code VARCHAR(50) NOT NULL REFERENCES core.domains(code),
    
    title VARCHAR(500) NOT NULL,
    objective TEXT NOT NULL,
    meeting_type VARCHAR(50) NOT NULL 
        CHECK (meeting_type IN ('planning', 'decision', 'review', 'conflict', 'strategy', 'async', 'brainstorm', 'learning')),
    
    participants JSONB DEFAULT '[]',
    agenda JSONB DEFAULT '[]',
    
    status VARCHAR(30) DEFAULT 'draft'
        CHECK (status IN ('draft', 'scheduled', 'active', 'paused', 'completed', 'cancelled')),
    
    context_refs UUID[],
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    scheduled_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_meetings_sphere ON meetings.meetings(sphere_id);
CREATE INDEX IF NOT EXISTS idx_meetings_domain ON meetings.meetings(domain_code);
CREATE INDEX IF NOT EXISTS idx_meetings_status ON meetings.meetings(status);
CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings.meetings(created_at);

-- Meeting threads
CREATE TABLE IF NOT EXISTS meetings.threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id) ON DELETE CASCADE,
    
    topic VARCHAR(500) NOT NULL,
    messages JSONB DEFAULT '[]',
    
    is_resolved BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_threads_meeting ON meetings.threads(meeting_id);

-- Decisions
CREATE TABLE IF NOT EXISTS meetings.decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id) ON DELETE CASCADE,
    thread_id UUID REFERENCES meetings.threads(id),
    
    proposal TEXT NOT NULL,
    proposed_by VARCHAR(200) NOT NULL,
    proposed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    risk_level VARCHAR(20) CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    
    votes JSONB DEFAULT '[]',
    dissent JSONB DEFAULT '[]',
    
    outcome VARCHAR(30) CHECK (outcome IN ('proposed', 'approved', 'rejected', 'deferred', 'superseded')),
    rationale TEXT,
    
    recorded_at TIMESTAMP WITH TIME ZONE,
    recorded_by VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_decisions_meeting ON meetings.decisions(meeting_id);
CREATE INDEX IF NOT EXISTS idx_decisions_outcome ON meetings.decisions(outcome);

-- XR sessions linked to meetings
CREATE TABLE IF NOT EXISTS meetings.xr_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id) ON DELETE CASCADE,
    
    events JSONB DEFAULT '[]',
    transcription TEXT,
    spatial_data JSONB,
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    synced_to_2d BOOLEAN DEFAULT FALSE,
    synced_to_2d_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_xr_sessions_meeting ON meetings.xr_sessions(meeting_id);

-- Agent activity log
CREATE TABLE IF NOT EXISTS meetings.agent_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id) ON DELETE CASCADE,
    agent_id VARCHAR(100) NOT NULL,
    
    action_type VARCHAR(100) NOT NULL,
    action_data JSONB NOT NULL,
    rationale TEXT,
    confidence FLOAT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_agent_activity_meeting ON meetings.agent_activity(meeting_id);
CREATE INDEX IF NOT EXISTS idx_agent_activity_agent ON meetings.agent_activity(agent_id);

-- Meeting exports
CREATE TABLE IF NOT EXISTS meetings.exports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings.meetings(id),
    
    export_type VARCHAR(50) NOT NULL,
    format VARCHAR(30) NOT NULL,
    content_hash VARCHAR(64),
    
    exported_by UUID,
    exported_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- MEETING AGENTS REGISTRY
-- =============================================================================

CREATE TABLE IF NOT EXISTS meetings.meeting_agents (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    name_fr VARCHAR(200),
    
    role VARCHAR(100) NOT NULL,
    capabilities TEXT[] NOT NULL,
    
    is_core BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    
    schema JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert core meeting agents
INSERT INTO meetings.meeting_agents (id, name, name_fr, role, capabilities, is_core)
VALUES
('meeting-orchestrator', 'Meeting Orchestrator', 'Orchestrateur de Réunion',
 'Controls phases, flow, pacing',
 ARRAY['start', 'pause', 'resume', 'advance_phase', 'close'],
 TRUE),

('agenda-structuring', 'Agenda Structuring Agent', 'Agent de Structuration d''Agenda',
 'Converts goals into agenda blocks',
 ARRAY['create_agenda', 'reorder', 'estimate_time', 'add_item', 'remove_item'],
 TRUE),

('decision-capture', 'Decision Capture Agent', 'Agent de Capture de Décisions',
 'Records decisions with metadata',
 ARRAY['propose', 'record', 'track_dissent', 'log_rationale', 'export'],
 TRUE),

('methodology-meeting', 'Methodology Agent', 'Agent de Méthodologie',
 'Applies selected methodology',
 ARRAY['suggest_framework', 'evaluate_structure', 'guide_process'],
 TRUE),

('consensus-divergence', 'Consensus/Divergence Agent', 'Agent de Consensus/Divergence',
 'Detects alignment and conflict',
 ARRAY['measure_agreement', 'flag_divergence', 'suggest_resolution'],
 TRUE),

('narrative-meeting', 'Narrative Agent', 'Agent Narratif',
 'Produces human-readable synthesis',
 ARRAY['summarize', 'generate_minutes', 'export_narrative', 'create_report'],
 TRUE),

('nova-mediator', 'Nova (Global Mediator)', 'Nova (Médiateur Global)',
 'Contextual assistant',
 ARRAY['assist', 'clarify', 'mediate', 'suggest', 'recall_context'],
 TRUE)
ON CONFLICT (id) DO NOTHING;

-- =============================================================================
-- VERIFICATION FUNCTIONS
-- =============================================================================

-- Function to verify sphere respects domain laws
CREATE OR REPLACE FUNCTION verify_sphere_domain_compliance(p_sphere_id VARCHAR(50))
RETURNS BOOLEAN AS $$
DECLARE
    v_domain_code VARCHAR(50);
    v_domain_record RECORD;
BEGIN
    -- Get sphere's domain
    SELECT domain_code INTO v_domain_code
    FROM core.sphere_instances
    WHERE id = p_sphere_id;
    
    IF v_domain_code IS NULL THEN
        RAISE EXCEPTION 'Sphere not found: %', p_sphere_id;
    END IF;
    
    -- Get domain constraints
    SELECT * INTO v_domain_record
    FROM core.domains
    WHERE code = v_domain_code;
    
    -- Verification logic would go here
    -- For now, return true if domain exists
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Function to verify XR session has MR-2D sync
CREATE OR REPLACE FUNCTION verify_xr_session_sync(p_session_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    v_synced BOOLEAN;
BEGIN
    SELECT synced_to_2d INTO v_synced
    FROM meetings.xr_sessions
    WHERE id = p_session_id;
    
    RETURN COALESCE(v_synced, FALSE);
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- VERIFICATION
-- =============================================================================

DO $$
DECLARE
    domain_count INTEGER;
    meeting_table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO domain_count FROM core.domains;
    
    SELECT COUNT(*) INTO meeting_table_count
    FROM information_schema.tables
    WHERE table_schema = 'meetings';
    
    RAISE NOTICE 'Domain Architecture Schema: % domains, % meeting tables', 
                 domain_count, meeting_table_count;
END $$;
