-- ============================================================
-- CHE·NU DATABASE SCHEMA v29 — COMPLETE ENGINE STACK
-- Generated: December 2024
-- Includes: All Engines, Domains, Systems
-- ============================================================

-- ============================================================
-- SECTION 1: CORE IDENTITY & USER MANAGEMENT
-- ============================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    avatar_url TEXT,
    preferred_language VARCHAR(10) DEFAULT 'fr',
    timezone VARCHAR(50) DEFAULT 'America/Toronto',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE identities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    identity_type VARCHAR(50) NOT NULL, -- 'personal', 'enterprise', 'creative', 'design', 'architecture', 'construction'
    identity_name VARCHAR(100) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, identity_type, identity_name)
);

CREATE TABLE identity_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_id UUID NOT NULL REFERENCES identities(id) ON DELETE CASCADE,
    permission_key VARCHAR(100) NOT NULL,
    permission_value JSONB DEFAULT '{}',
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    granted_by UUID REFERENCES users(id),
    expires_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(identity_id, permission_key)
);

-- ============================================================
-- SECTION 2: SPHERE & DOMAIN MANAGEMENT
-- ============================================================

CREATE TABLE spheres (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL, -- 'maison', 'entreprise', 'creative', 'scholar', 'team'
    name_fr VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    config JSONB DEFAULT '{}'
);

CREATE TABLE domains (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id UUID NOT NULL REFERENCES spheres(id),
    code VARCHAR(50) NOT NULL, -- 'finance', 'immobilier', 'construction', 'architecture'
    name_fr VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    config JSONB DEFAULT '{}',
    UNIQUE(sphere_id, code)
);

CREATE TABLE user_sphere_access (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    identity_id UUID NOT NULL REFERENCES identities(id) ON DELETE CASCADE,
    sphere_id UUID NOT NULL REFERENCES spheres(id),
    access_level VARCHAR(20) DEFAULT 'full', -- 'full', 'read', 'limited'
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(identity_id, sphere_id)
);

-- ============================================================
-- SECTION 3: DATASPACE ENGINE
-- ============================================================

CREATE TABLE dataspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    sphere_id UUID REFERENCES spheres(id),
    domain_id UUID REFERENCES domains(id),
    parent_id UUID REFERENCES dataspaces(id),
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    dataspace_type VARCHAR(50) NOT NULL, -- 'project', 'property', 'client', 'meeting', 'document', 'custom'
    
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'archived', 'deleted'
    visibility VARCHAR(20) DEFAULT 'private', -- 'private', 'shared', 'public'
    
    metadata JSONB DEFAULT '{}',
    tags TEXT[],
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    archived_at TIMESTAMP WITH TIME ZONE,
    
    -- Full-text search
    search_vector TSVECTOR
);

CREATE INDEX idx_dataspaces_owner ON dataspaces(owner_id);
CREATE INDEX idx_dataspaces_identity ON dataspaces(identity_id);
CREATE INDEX idx_dataspaces_sphere ON dataspaces(sphere_id);
CREATE INDEX idx_dataspaces_domain ON dataspaces(domain_id);
CREATE INDEX idx_dataspaces_type ON dataspaces(dataspace_type);
CREATE INDEX idx_dataspaces_search ON dataspaces USING GIN(search_vector);

CREATE TABLE dataspace_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataspace_id UUID NOT NULL REFERENCES dataspaces(id) ON DELETE CASCADE,
    item_type VARCHAR(50) NOT NULL, -- 'document', 'note', 'task', 'link', 'file', 'reference'
    title VARCHAR(255),
    content TEXT,
    metadata JSONB DEFAULT '{}',
    position INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE dataspace_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_dataspace_id UUID NOT NULL REFERENCES dataspaces(id) ON DELETE CASCADE,
    target_dataspace_id UUID NOT NULL REFERENCES dataspaces(id) ON DELETE CASCADE,
    link_type VARCHAR(50) DEFAULT 'reference', -- 'reference', 'parent', 'related', 'derived'
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(source_dataspace_id, target_dataspace_id, link_type)
);

-- ============================================================
-- SECTION 4: THREAD ENGINE
-- ============================================================

CREATE TABLE threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataspace_id UUID REFERENCES dataspaces(id) ON DELETE SET NULL,
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    title VARCHAR(255),
    thread_type VARCHAR(50) DEFAULT 'conversation', -- 'conversation', 'decision', 'task', 'meeting', 'support'
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'resolved', 'archived'
    
    participants UUID[], -- Array of user IDs
    
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE thread_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    sender_id UUID REFERENCES users(id),
    agent_id UUID, -- If sent by an agent
    
    message_type VARCHAR(50) DEFAULT 'text', -- 'text', 'file', 'action', 'decision', 'system'
    content TEXT NOT NULL,
    
    attachments JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    edited_at TIMESTAMP WITH TIME ZONE,
    is_edited BOOLEAN DEFAULT FALSE
);

CREATE TABLE thread_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    message_id UUID REFERENCES thread_messages(id),
    
    decision_text TEXT NOT NULL,
    decision_type VARCHAR(50), -- 'approval', 'direction', 'assignment', 'policy'
    
    made_by UUID REFERENCES users(id),
    made_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    affected_dataspaces UUID[],
    metadata JSONB DEFAULT '{}'
);

-- ============================================================
-- SECTION 5: WORKSPACE ENGINE
-- ============================================================

CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    dataspace_id UUID REFERENCES dataspaces(id),
    
    name VARCHAR(255) NOT NULL,
    workspace_mode VARCHAR(50) NOT NULL, -- 'document', 'board', 'timeline', 'spreadsheet', 'dashboard', 'diagram', 'whiteboard', 'xr', 'hybrid'
    
    layout_config JSONB DEFAULT '{}',
    view_state JSONB DEFAULT '{}',
    
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE workspace_panels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    panel_type VARCHAR(50) NOT NULL, -- 'editor', 'preview', 'chat', 'files', 'agents', 'timeline', 'canvas'
    position JSONB NOT NULL, -- {x, y, width, height}
    
    config JSONB DEFAULT '{}',
    is_visible BOOLEAN DEFAULT TRUE,
    z_index INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE workspace_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    state_name VARCHAR(100),
    state_data JSONB NOT NULL,
    
    is_autosave BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE TABLE workspace_transformations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    from_mode VARCHAR(50) NOT NULL,
    to_mode VARCHAR(50) NOT NULL,
    
    transformation_data JSONB NOT NULL,
    
    triggered_by UUID REFERENCES users(id),
    triggered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    is_reversible BOOLEAN DEFAULT TRUE,
    reverse_data JSONB
);

-- ============================================================
-- SECTION 6: 1-CLICK ASSISTANT ENGINE
-- ============================================================

CREATE TABLE oneclick_workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    trigger_patterns TEXT[], -- Intent patterns that trigger this workflow
    
    sphere_id UUID REFERENCES spheres(id),
    domain_id UUID REFERENCES domains(id),
    
    workflow_steps JSONB NOT NULL, -- Array of step definitions
    
    required_inputs JSONB DEFAULT '[]',
    output_types TEXT[], -- 'document', 'dataspace', 'dashboard', 'xr', etc.
    
    is_system BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE oneclick_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES oneclick_workflows(id),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    input_data JSONB NOT NULL,
    input_type VARCHAR(50), -- 'prompt', 'file', 'context', 'dataspace'
    
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed', 'cancelled'
    
    steps_completed INTEGER DEFAULT 0,
    total_steps INTEGER,
    
    output_data JSONB,
    output_dataspaces UUID[],
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    error_message TEXT,
    execution_log JSONB DEFAULT '[]'
);

CREATE TABLE oneclick_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50), -- 'construction', 'immobilier', 'finance', 'creative', 'enterprise'
    
    prompt_template TEXT NOT NULL,
    workflow_id UUID REFERENCES oneclick_workflows(id),
    
    example_inputs JSONB DEFAULT '[]',
    
    usage_count INTEGER DEFAULT 0,
    is_featured BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- SECTION 7: BACKSTAGE INTELLIGENCE ENGINE
-- ============================================================

CREATE TABLE backstage_contexts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    session_id UUID NOT NULL,
    
    context_type VARCHAR(50) NOT NULL, -- 'workspace', 'thread', 'meeting', 'workflow'
    context_data JSONB NOT NULL,
    
    -- Pre-processed intelligence
    detected_intent JSONB,
    suggested_agents UUID[],
    suggested_dataspaces UUID[],
    
    relevance_score FLOAT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE backstage_preparations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    context_id UUID REFERENCES backstage_contexts(id) ON DELETE CASCADE,
    
    preparation_type VARCHAR(50) NOT NULL, -- 'template', 'data_fetch', 'agent_warmup', 'prediction'
    preparation_data JSONB NOT NULL,
    
    status VARCHAR(20) DEFAULT 'pending',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    used_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE backstage_classifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    input_hash VARCHAR(64) NOT NULL, -- Hash of input for caching
    input_type VARCHAR(50) NOT NULL, -- 'text', 'file', 'image', 'audio'
    
    classification_result JSONB NOT NULL,
    confidence FLOAT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(input_hash, input_type)
);

-- ============================================================
-- SECTION 8: MEMORY & GOVERNANCE ENGINE
-- ============================================================

-- Memory Storage
CREATE TABLE memory_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    identity_id UUID NOT NULL REFERENCES identities(id) ON DELETE CASCADE,
    
    memory_type VARCHAR(50) NOT NULL, -- 'short_term', 'mid_term', 'long_term', 'institutional', 'agent'
    memory_category VARCHAR(50), -- 'preference', 'instruction', 'fact', 'context', 'rule'
    
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    
    dataspace_id UUID REFERENCES dataspaces(id) ON DELETE SET NULL,
    thread_id UUID REFERENCES threads(id) ON DELETE SET NULL,
    
    -- Lifecycle
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'pinned', 'archived', 'deleted'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    last_accessed_at TIMESTAMP WITH TIME ZONE,
    
    -- Governance
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT memory_identity_scope CHECK (identity_id IS NOT NULL)
);

CREATE INDEX idx_memory_user_identity ON memory_items(user_id, identity_id);
CREATE INDEX idx_memory_type ON memory_items(memory_type);
CREATE INDEX idx_memory_status ON memory_items(status);

-- Governance Audit Log
CREATE TABLE governance_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID REFERENCES users(id),
    identity_id UUID REFERENCES identities(id),
    agent_id UUID,
    
    action_type VARCHAR(50) NOT NULL, -- 'create', 'read', 'update', 'delete', 'share', 'elevate'
    resource_type VARCHAR(50) NOT NULL, -- 'memory', 'dataspace', 'thread', 'file', 'agent'
    resource_id UUID NOT NULL,
    
    action_details JSONB DEFAULT '{}',
    
    -- Before/After state for reversibility
    before_state JSONB,
    after_state JSONB,
    
    -- Permission context
    permission_used VARCHAR(100),
    elevation_required BOOLEAN DEFAULT FALSE,
    elevation_approved BOOLEAN,
    
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON governance_audit_log(user_id);
CREATE INDEX idx_audit_resource ON governance_audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_time ON governance_audit_log(created_at);

-- Elevation Requests
CREATE TABLE elevation_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    requested_action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id UUID NOT NULL,
    
    reason TEXT,
    
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'approved', 'denied', 'expired'
    
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    responded_at TIMESTAMP WITH TIME ZONE,
    responded_by UUID REFERENCES users(id),
    
    expires_at TIMESTAMP WITH TIME ZONE,
    
    metadata JSONB DEFAULT '{}'
);

-- Cross-Identity Protection Log
CREATE TABLE cross_identity_blocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    user_id UUID NOT NULL REFERENCES users(id),
    source_identity_id UUID NOT NULL REFERENCES identities(id),
    target_identity_id UUID NOT NULL REFERENCES identities(id),
    
    blocked_action VARCHAR(100) NOT NULL,
    blocked_resource_type VARCHAR(50),
    blocked_resource_id UUID,
    
    block_reason TEXT,
    
    blocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- SECTION 9: AGENT SYSTEM
-- ============================================================

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    code VARCHAR(50) UNIQUE NOT NULL,
    name_fr VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description TEXT,
    
    agent_level VARCHAR(10) NOT NULL, -- 'L0', 'L1', 'L2', 'L3'
    agent_type VARCHAR(50) NOT NULL, -- 'orchestrator', 'specialist', 'support', 'analyzer'
    
    sphere_id UUID REFERENCES spheres(id),
    domain_id UUID REFERENCES domains(id),
    
    capabilities JSONB DEFAULT '[]',
    constraints JSONB DEFAULT '[]',
    
    llm_provider VARCHAR(50) DEFAULT 'claude', -- 'claude', 'gpt4', 'gemini', 'ollama'
    llm_model VARCHAR(100),
    
    system_prompt TEXT,
    
    is_active BOOLEAN DEFAULT TRUE,
    is_system BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE agent_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    identity_id UUID REFERENCES identities(id),
    
    config_key VARCHAR(100) NOT NULL,
    config_value JSONB NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(agent_id, identity_id, config_key)
);

CREATE TABLE agent_memory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    
    memory_type VARCHAR(50) NOT NULL, -- 'instruction', 'rule', 'template', 'procedure'
    memory_key VARCHAR(100) NOT NULL,
    memory_value JSONB NOT NULL,
    
    -- NO personal data allowed - enforced by application
    is_personal_data BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(agent_id, memory_type, memory_key),
    CONSTRAINT no_personal_data CHECK (is_personal_data = FALSE)
);

CREATE TABLE agent_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    thread_id UUID REFERENCES threads(id),
    dataspace_id UUID REFERENCES dataspaces(id),
    workflow_id UUID REFERENCES oneclick_workflows(id),
    
    input_data JSONB NOT NULL,
    output_data JSONB,
    
    status VARCHAR(20) DEFAULT 'running', -- 'running', 'completed', 'failed', 'cancelled'
    
    tokens_used INTEGER,
    execution_time_ms INTEGER,
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    error_message TEXT
);

-- ============================================================
-- SECTION 10: MEETING SYSTEM
-- ============================================================

CREATE TABLE meetings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataspace_id UUID NOT NULL REFERENCES dataspaces(id) ON DELETE CASCADE,
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    title VARCHAR(255) NOT NULL,
    description TEXT,
    
    meeting_type VARCHAR(50) NOT NULL, -- 'standup', 'planning', 'review', 'brainstorm', 'decision', 'workshop'
    
    scheduled_start TIMESTAMP WITH TIME ZONE,
    scheduled_end TIMESTAMP WITH TIME ZONE,
    actual_start TIMESTAMP WITH TIME ZONE,
    actual_end TIMESTAMP WITH TIME ZONE,
    
    status VARCHAR(20) DEFAULT 'scheduled', -- 'scheduled', 'active', 'completed', 'cancelled'
    
    location VARCHAR(255),
    is_xr_meeting BOOLEAN DEFAULT FALSE,
    xr_room_id UUID,
    
    agenda JSONB DEFAULT '[]',
    
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE meeting_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    
    role VARCHAR(50) DEFAULT 'participant', -- 'organizer', 'participant', 'observer', 'presenter'
    
    rsvp_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'accepted', 'declined', 'tentative'
    
    joined_at TIMESTAMP WITH TIME ZONE,
    left_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(meeting_id, user_id)
);

CREATE TABLE meeting_notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    
    note_type VARCHAR(50) DEFAULT 'general', -- 'general', 'decision', 'action', 'question', 'idea'
    content TEXT NOT NULL,
    
    created_by UUID REFERENCES users(id),
    agent_id UUID REFERENCES agents(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE meeting_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    meeting_id UUID NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    
    title VARCHAR(255) NOT NULL,
    description TEXT,
    
    assignee_id UUID REFERENCES users(id),
    due_date DATE,
    
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'cancelled'
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'urgent'
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- ============================================================
-- SECTION 11: IMMOBILIER DOMAIN
-- ============================================================

CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataspace_id UUID NOT NULL REFERENCES dataspaces(id) ON DELETE CASCADE,
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    property_type VARCHAR(50) NOT NULL, -- 'residential', 'commercial', 'industrial', 'land', 'mixed'
    ownership_type VARCHAR(50) NOT NULL, -- 'personal', 'enterprise', 'investment'
    
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    province VARCHAR(50) DEFAULT 'QC',
    postal_code VARCHAR(10),
    country VARCHAR(50) DEFAULT 'Canada',
    
    coordinates POINT,
    
    -- Property Details
    lot_size_sqft DECIMAL(12, 2),
    building_size_sqft DECIMAL(12, 2),
    year_built INTEGER,
    num_units INTEGER DEFAULT 1,
    num_bedrooms INTEGER,
    num_bathrooms DECIMAL(3, 1),
    
    -- Financial
    purchase_price DECIMAL(12, 2),
    purchase_date DATE,
    current_value DECIMAL(12, 2),
    last_valuation_date DATE,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'for_sale', 'sold', 'archived'
    
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE property_units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    
    unit_number VARCHAR(20),
    unit_type VARCHAR(50), -- 'apartment', 'commercial', 'storage', 'parking'
    
    size_sqft DECIMAL(10, 2),
    num_bedrooms INTEGER,
    num_bathrooms DECIMAL(3, 1),
    
    monthly_rent DECIMAL(10, 2),
    
    status VARCHAR(20) DEFAULT 'vacant', -- 'vacant', 'occupied', 'renovating', 'unavailable'
    
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    unit_id UUID REFERENCES property_units(id),
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    -- Personal info (Enterprise identity only)
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    
    -- Lease info
    lease_start DATE NOT NULL,
    lease_end DATE,
    monthly_rent DECIMAL(10, 2) NOT NULL,
    security_deposit DECIMAL(10, 2),
    
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'notice_given', 'ended'
    
    -- Quebec TAL compliance
    tal_registered BOOLEAN DEFAULT FALSE,
    tal_registration_number VARCHAR(50),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE rent_payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    property_id UUID NOT NULL REFERENCES properties(id),
    
    payment_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50), -- 'cheque', 'transfer', 'cash', 'interac'
    
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    status VARCHAR(20) DEFAULT 'received', -- 'pending', 'received', 'late', 'partial', 'bounced'
    
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE maintenance_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL REFERENCES properties(id) ON DELETE CASCADE,
    unit_id UUID REFERENCES property_units(id),
    tenant_id UUID REFERENCES tenants(id),
    
    title VARCHAR(255) NOT NULL,
    description TEXT,
    
    category VARCHAR(50), -- 'plumbing', 'electrical', 'hvac', 'appliance', 'structural', 'other'
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'emergency'
    
    status VARCHAR(20) DEFAULT 'open', -- 'open', 'assigned', 'in_progress', 'completed', 'cancelled'
    
    assigned_contractor_id UUID,
    estimated_cost DECIMAL(10, 2),
    actual_cost DECIMAL(10, 2),
    
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    photos TEXT[],
    notes TEXT
);

-- ============================================================
-- SECTION 12: CONSTRUCTION DOMAIN
-- ============================================================

CREATE TABLE construction_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataspace_id UUID NOT NULL REFERENCES dataspaces(id) ON DELETE CASCADE,
    identity_id UUID NOT NULL REFERENCES identities(id),
    property_id UUID REFERENCES properties(id),
    
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    project_type VARCHAR(50) NOT NULL, -- 'new_build', 'renovation', 'addition', 'repair', 'commercial'
    
    -- Dates
    estimated_start DATE,
    estimated_end DATE,
    actual_start DATE,
    actual_end DATE,
    
    -- Budget
    estimated_budget DECIMAL(14, 2),
    actual_cost DECIMAL(14, 2),
    
    status VARCHAR(20) DEFAULT 'planning', -- 'planning', 'permitted', 'active', 'paused', 'completed', 'cancelled'
    
    -- Quebec RBQ compliance
    rbq_license_required BOOLEAN DEFAULT TRUE,
    rbq_license_number VARCHAR(50),
    cnesst_registered BOOLEAN DEFAULT FALSE,
    ccq_compliant BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE construction_estimates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES construction_projects(id) ON DELETE CASCADE,
    
    estimate_name VARCHAR(255) NOT NULL,
    estimate_version INTEGER DEFAULT 1,
    
    -- Totals
    materials_total DECIMAL(12, 2) DEFAULT 0,
    labor_total DECIMAL(12, 2) DEFAULT 0,
    equipment_total DECIMAL(12, 2) DEFAULT 0,
    overhead_total DECIMAL(12, 2) DEFAULT 0,
    profit_margin DECIMAL(5, 2) DEFAULT 15.00,
    
    grand_total DECIMAL(14, 2) GENERATED ALWAYS AS (
        (materials_total + labor_total + equipment_total + overhead_total) * (1 + profit_margin / 100)
    ) STORED,
    
    status VARCHAR(20) DEFAULT 'draft', -- 'draft', 'submitted', 'approved', 'rejected'
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    approved_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE estimate_line_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    estimate_id UUID NOT NULL REFERENCES construction_estimates(id) ON DELETE CASCADE,
    
    category VARCHAR(50) NOT NULL, -- 'materials', 'labor', 'equipment', 'subcontractor', 'permit'
    description VARCHAR(255) NOT NULL,
    
    quantity DECIMAL(10, 2) NOT NULL,
    unit VARCHAR(20) NOT NULL, -- 'sqft', 'lf', 'each', 'hour', 'day', 'lot'
    unit_cost DECIMAL(10, 2) NOT NULL,
    
    total_cost DECIMAL(12, 2) GENERATED ALWAYS AS (quantity * unit_cost) STORED,
    
    notes TEXT,
    
    position INTEGER DEFAULT 0
);

CREATE TABLE materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    code VARCHAR(50) UNIQUE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    category VARCHAR(50) NOT NULL, -- 'concrete', 'steel', 'lumber', 'drywall', 'electrical', 'plumbing', 'hvac'
    subcategory VARCHAR(50),
    
    unit VARCHAR(20) NOT NULL,
    unit_cost DECIMAL(10, 2),
    
    supplier VARCHAR(100),
    
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- SECTION 13: OCW (OPERATIONAL COGNITIVE WORKSPACE)
-- ============================================================

CREATE TABLE ocw_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    session_type VARCHAR(50) NOT NULL, -- 'shareview', 'whiteboard', 'cockpit', 'collaboration'
    
    host_user_id UUID NOT NULL REFERENCES users(id),
    
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'paused', 'ended'
    
    config JSONB DEFAULT '{}',
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE ocw_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES ocw_sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    agent_id UUID REFERENCES agents(id),
    
    role VARCHAR(50) DEFAULT 'viewer', -- 'host', 'editor', 'viewer', 'spectator'
    
    cursor_position JSONB,
    viewport JSONB,
    
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    left_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(session_id, user_id)
);

CREATE TABLE ocw_canvas_objects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES ocw_sessions(id) ON DELETE CASCADE,
    
    object_type VARCHAR(50) NOT NULL, -- 'shape', 'text', 'image', 'drawing', 'sticky', 'connector', 'frame'
    
    position JSONB NOT NULL, -- {x, y}
    size JSONB, -- {width, height}
    rotation DECIMAL(5, 2) DEFAULT 0,
    
    properties JSONB DEFAULT '{}', -- type-specific properties
    
    layer INTEGER DEFAULT 0,
    is_locked BOOLEAN DEFAULT FALSE,
    
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE ocw_annotations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES ocw_sessions(id) ON DELETE CASCADE,
    object_id UUID REFERENCES ocw_canvas_objects(id) ON DELETE CASCADE,
    
    annotation_type VARCHAR(50) NOT NULL, -- 'comment', 'highlight', 'marker', 'voice_note'
    content TEXT,
    
    position JSONB,
    
    created_by UUID REFERENCES users(id),
    agent_id UUID REFERENCES agents(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- SECTION 14: XR SPATIAL ENGINE
-- ============================================================

CREATE TABLE xr_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataspace_id UUID REFERENCES dataspaces(id) ON DELETE SET NULL,
    meeting_id UUID REFERENCES meetings(id) ON DELETE SET NULL,
    
    name VARCHAR(255) NOT NULL,
    room_type VARCHAR(50) NOT NULL, -- 'meeting', 'presentation', 'brainstorm', 'walkthrough', 'showroom'
    
    -- Spatial config
    room_template VARCHAR(50), -- 'conference', 'amphitheater', 'open_space', 'custom'
    dimensions JSONB, -- {width, height, depth}
    
    environment_config JSONB DEFAULT '{}',
    
    is_persistent BOOLEAN DEFAULT FALSE,
    
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE xr_objects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES xr_rooms(id) ON DELETE CASCADE,
    
    object_type VARCHAR(50) NOT NULL, -- 'model', 'screen', 'whiteboard', 'annotation', 'avatar', 'furniture'
    
    position JSONB NOT NULL, -- {x, y, z}
    rotation JSONB DEFAULT '{"x":0,"y":0,"z":0}',
    scale JSONB DEFAULT '{"x":1,"y":1,"z":1}',
    
    properties JSONB DEFAULT '{}',
    
    source_url TEXT, -- For 3D models
    
    is_interactive BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE xr_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id UUID NOT NULL REFERENCES xr_rooms(id) ON DELETE CASCADE,
    
    status VARCHAR(20) DEFAULT 'active',
    
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE xr_session_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES xr_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id),
    
    avatar_config JSONB DEFAULT '{}',
    
    position JSONB,
    rotation JSONB,
    
    device_type VARCHAR(50), -- 'vr_headset', 'ar_glasses', 'desktop', 'mobile'
    
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    left_at TIMESTAMP WITH TIME ZONE
);

-- ============================================================
-- SECTION 15: FILE TRANSFORMATION ENGINE
-- ============================================================

CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataspace_id UUID REFERENCES dataspaces(id) ON DELETE SET NULL,
    identity_id UUID NOT NULL REFERENCES identities(id),
    
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    
    mime_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL,
    
    storage_path TEXT NOT NULL,
    storage_provider VARCHAR(50) DEFAULT 'local', -- 'local', 's3', 'gcs', 'azure'
    
    checksum VARCHAR(64),
    
    is_processed BOOLEAN DEFAULT FALSE,
    processing_status VARCHAR(20),
    
    metadata JSONB DEFAULT '{}',
    extracted_text TEXT,
    
    uploaded_by UUID NOT NULL REFERENCES users(id),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE file_transformations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_file_id UUID NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    output_file_id UUID REFERENCES files(id),
    
    transformation_type VARCHAR(50) NOT NULL, -- 'convert', 'extract', 'compress', 'ocr', 'transcribe'
    
    input_format VARCHAR(50),
    output_format VARCHAR(50),
    
    parameters JSONB DEFAULT '{}',
    
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    error_message TEXT
);

-- ============================================================
-- SECTION 16: NOTIFICATIONS & ALERTS
-- ============================================================

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    identity_id UUID REFERENCES identities(id),
    
    notification_type VARCHAR(50) NOT NULL, -- 'info', 'warning', 'alert', 'task', 'mention', 'reminder'
    
    title VARCHAR(255) NOT NULL,
    message TEXT,
    
    source_type VARCHAR(50), -- 'system', 'agent', 'meeting', 'task', 'property', 'workflow'
    source_id UUID,
    
    action_url TEXT,
    
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX idx_notifications_created ON notifications(created_at);

-- ============================================================
-- SECTION 17: ANALYTICS & METRICS
-- ============================================================

CREATE TABLE usage_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    identity_id UUID REFERENCES identities(id),
    
    metric_type VARCHAR(50) NOT NULL, -- 'session', 'agent_call', 'file_upload', 'workflow', 'meeting'
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(14, 4),
    
    metadata JSONB DEFAULT '{}',
    
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_metrics_user_type ON usage_metrics(user_id, metric_type);
CREATE INDEX idx_metrics_time ON usage_metrics(recorded_at);

-- ============================================================
-- SECTION 18: SYSTEM CONFIGURATION
-- ============================================================

CREATE TABLE system_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value JSONB NOT NULL,
    
    description TEXT,
    
    is_public BOOLEAN DEFAULT FALSE,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_by UUID REFERENCES users(id)
);

CREATE TABLE feature_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    flag_key VARCHAR(100) UNIQUE NOT NULL,
    flag_value BOOLEAN DEFAULT FALSE,
    
    description TEXT,
    
    rollout_percentage INTEGER DEFAULT 0, -- 0-100
    
    enabled_for_users UUID[],
    enabled_for_identities UUID[],
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- SECTION 19: INDEXES FOR PERFORMANCE
-- ============================================================

-- DataSpaces
CREATE INDEX idx_dataspaces_status ON dataspaces(status) WHERE status = 'active';
CREATE INDEX idx_dataspaces_created ON dataspaces(created_at);

-- Threads
CREATE INDEX idx_threads_dataspace ON threads(dataspace_id);
CREATE INDEX idx_threads_status ON threads(status);
CREATE INDEX idx_thread_messages_thread ON thread_messages(thread_id);

-- Properties
CREATE INDEX idx_properties_identity ON properties(identity_id);
CREATE INDEX idx_properties_type ON properties(property_type);
CREATE INDEX idx_properties_status ON properties(status);

-- Tenants
CREATE INDEX idx_tenants_property ON tenants(property_id);
CREATE INDEX idx_tenants_status ON tenants(status);

-- Agents
CREATE INDEX idx_agent_executions_agent ON agent_executions(agent_id);
CREATE INDEX idx_agent_executions_user ON agent_executions(user_id);
CREATE INDEX idx_agent_executions_status ON agent_executions(status);

-- Meetings
CREATE INDEX idx_meetings_dataspace ON meetings(dataspace_id);
CREATE INDEX idx_meetings_scheduled ON meetings(scheduled_start);
CREATE INDEX idx_meetings_status ON meetings(status);

-- ============================================================
-- SECTION 20: TRIGGERS & FUNCTIONS
-- ============================================================

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_identities_updated_at BEFORE UPDATE ON identities FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_dataspaces_updated_at BEFORE UPDATE ON dataspaces FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_workspaces_updated_at BEFORE UPDATE ON workspaces FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_properties_updated_at BEFORE UPDATE ON properties FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_tenants_updated_at BEFORE UPDATE ON tenants FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_meetings_updated_at BEFORE UPDATE ON meetings FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- DataSpace search vector update
CREATE OR REPLACE FUNCTION update_dataspace_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector = to_tsvector('french', COALESCE(NEW.name, '') || ' ' || COALESCE(NEW.description, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_dataspaces_search BEFORE INSERT OR UPDATE ON dataspaces FOR EACH ROW EXECUTE FUNCTION update_dataspace_search_vector();

-- Memory governance enforcement
CREATE OR REPLACE FUNCTION enforce_memory_governance()
RETURNS TRIGGER AS $$
BEGIN
    -- Ensure identity is always set
    IF NEW.identity_id IS NULL THEN
        RAISE EXCEPTION 'Memory items must have an identity_id (Law 3: Identity Scoping)';
    END IF;
    
    -- Log the memory operation
    INSERT INTO governance_audit_log (
        user_id, identity_id, action_type, resource_type, resource_id, action_details
    ) VALUES (
        NEW.user_id, NEW.identity_id, TG_OP, 'memory', NEW.id, 
        jsonb_build_object('memory_type', NEW.memory_type, 'category', NEW.memory_category)
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_memory_governance_trigger 
BEFORE INSERT OR UPDATE ON memory_items 
FOR EACH ROW EXECUTE FUNCTION enforce_memory_governance();

-- Cross-identity access prevention
CREATE OR REPLACE FUNCTION prevent_cross_identity_access()
RETURNS TRIGGER AS $$
DECLARE
    source_identity UUID;
BEGIN
    -- Get the identity of the source dataspace
    SELECT identity_id INTO source_identity FROM dataspaces WHERE id = NEW.source_dataspace_id;
    
    -- Check if target has same identity
    IF NOT EXISTS (
        SELECT 1 FROM dataspaces 
        WHERE id = NEW.target_dataspace_id 
        AND identity_id = source_identity
    ) THEN
        -- Log the blocked attempt
        INSERT INTO cross_identity_blocks (
            user_id, source_identity_id, target_identity_id,
            blocked_action, blocked_resource_type, blocked_resource_id, block_reason
        ) VALUES (
            current_setting('app.current_user_id', true)::UUID,
            source_identity,
            (SELECT identity_id FROM dataspaces WHERE id = NEW.target_dataspace_id),
            'dataspace_link',
            'dataspace',
            NEW.target_dataspace_id,
            'Cross-identity linking blocked (Law 4: No Cross-Identity Access)'
        );
        
        RAISE EXCEPTION 'Cross-identity dataspace linking is not allowed (Memory Law 4)';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_cross_identity_dataspace_links
BEFORE INSERT ON dataspace_links
FOR EACH ROW EXECUTE FUNCTION prevent_cross_identity_access();

-- ============================================================
-- SECTION 21: VIEWS FOR COMMON QUERIES
-- ============================================================

-- Active properties with tenant info
CREATE VIEW v_property_summary AS
SELECT 
    p.id,
    p.identity_id,
    p.property_type,
    p.ownership_type,
    p.address_line1,
    p.city,
    p.current_value,
    p.status,
    COUNT(DISTINCT pu.id) as total_units,
    COUNT(DISTINCT t.id) FILTER (WHERE t.status = 'active') as occupied_units,
    SUM(t.monthly_rent) FILTER (WHERE t.status = 'active') as monthly_revenue
FROM properties p
LEFT JOIN property_units pu ON pu.property_id = p.id
LEFT JOIN tenants t ON t.property_id = p.id
WHERE p.status = 'active'
GROUP BY p.id;

-- Meeting summaries
CREATE VIEW v_meeting_summary AS
SELECT 
    m.id,
    m.title,
    m.meeting_type,
    m.scheduled_start,
    m.status,
    COUNT(DISTINCT mp.id) as participant_count,
    COUNT(DISTINCT mn.id) as notes_count,
    COUNT(DISTINCT mt.id) as tasks_count,
    COUNT(DISTINCT mt.id) FILTER (WHERE mt.status = 'completed') as completed_tasks
FROM meetings m
LEFT JOIN meeting_participants mp ON mp.meeting_id = m.id
LEFT JOIN meeting_notes mn ON mn.meeting_id = m.id
LEFT JOIN meeting_tasks mt ON mt.meeting_id = m.id
GROUP BY m.id;

-- Agent performance
CREATE VIEW v_agent_performance AS
SELECT 
    a.id,
    a.code,
    a.name_fr,
    a.agent_level,
    COUNT(ae.id) as total_executions,
    AVG(ae.execution_time_ms) as avg_execution_time_ms,
    SUM(ae.tokens_used) as total_tokens,
    COUNT(ae.id) FILTER (WHERE ae.status = 'completed') as successful_executions,
    COUNT(ae.id) FILTER (WHERE ae.status = 'failed') as failed_executions
FROM agents a
LEFT JOIN agent_executions ae ON ae.agent_id = a.id
WHERE a.is_active = TRUE
GROUP BY a.id;

-- Memory usage by identity
CREATE VIEW v_memory_by_identity AS
SELECT 
    i.id as identity_id,
    i.identity_type,
    i.identity_name,
    COUNT(mi.id) as total_memories,
    COUNT(mi.id) FILTER (WHERE mi.memory_type = 'long_term') as long_term_count,
    COUNT(mi.id) FILTER (WHERE mi.status = 'pinned') as pinned_count
FROM identities i
LEFT JOIN memory_items mi ON mi.identity_id = i.id AND mi.status != 'deleted'
GROUP BY i.id;

-- ============================================================
-- END OF SCHEMA
-- ============================================================

COMMENT ON SCHEMA public IS 'CHE·NU Database Schema v29 - Complete Engine Stack';
