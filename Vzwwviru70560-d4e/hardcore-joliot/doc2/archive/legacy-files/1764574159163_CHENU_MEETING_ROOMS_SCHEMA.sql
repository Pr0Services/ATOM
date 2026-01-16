-- ═══════════════════════════════════════════════════════════════════════════
-- CHENU MEETING ROOMS - DATABASE SCHEMA
-- Additional tables for multi-agent collaboration
-- ═══════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════
-- 1. MEETINGS TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS meetings (
    meeting_id VARCHAR(100) PRIMARY KEY,
    meeting_name VARCHAR(200) NOT NULL,
    created_by_user_id VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    mode VARCHAR(50) NOT NULL DEFAULT 'round-robin',
    
    -- Limits
    tokens_limit INTEGER NOT NULL DEFAULT 20000,
    tokens_used INTEGER NOT NULL DEFAULT 0,
    cost_limit DECIMAL(10,2) NOT NULL DEFAULT 5.00,
    cost_so_far DECIMAL(10,4) NOT NULL DEFAULT 0.0000,
    
    -- Timestamps
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    paused_at TIMESTAMP,
    ended_at TIMESTAMP,
    
    -- Project/Task linking
    project_id VARCHAR(100),
    task_id VARCHAR(100),
    
    -- AI-generated content
    summary TEXT,
    action_items JSONB,
    
    -- Settings
    context_pruning_enabled BOOLEAN DEFAULT FALSE,
    auto_summarization_enabled BOOLEAN DEFAULT FALSE,
    summarization_threshold INTEGER DEFAULT 500,
    current_speaker_index INTEGER DEFAULT -1,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Foreign Keys
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT check_status CHECK (status IN ('active', 'paused', 'ended')),
    CONSTRAINT check_mode CHECK (mode IN ('round-robin', 'free', 'moderated', 'hierarchical')),
    CONSTRAINT check_tokens_positive CHECK (tokens_used >= 0),
    CONSTRAINT check_cost_positive CHECK (cost_so_far >= 0)
);

-- Indexes
CREATE INDEX idx_meetings_user ON meetings(created_by_user_id);
CREATE INDEX idx_meetings_status ON meetings(status);
CREATE INDEX idx_meetings_created_at ON meetings(created_at DESC);
CREATE INDEX idx_meetings_project ON meetings(project_id);
CREATE INDEX idx_meetings_task ON meetings(task_id);

-- ═══════════════════════════════════════════════════════════════════════════
-- 2. MEETING PARTICIPANTS TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS meeting_participants (
    participant_id VARCHAR(100) PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    meeting_id VARCHAR(100) NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    joined_at TIMESTAMP NOT NULL DEFAULT NOW(),
    left_at TIMESTAMP,
    
    -- Usage tracking
    messages_sent INTEGER DEFAULT 0,
    tokens_used INTEGER DEFAULT 0,
    cost_incurred DECIMAL(10,4) DEFAULT 0.0000,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Foreign Keys
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT check_participant_status CHECK (status IN ('active', 'inactive', 'removed')),
    CONSTRAINT unique_meeting_agent UNIQUE (meeting_id, agent_id)
);

-- Indexes
CREATE INDEX idx_meeting_participants_meeting ON meeting_participants(meeting_id);
CREATE INDEX idx_meeting_participants_agent ON meeting_participants(agent_id);
CREATE INDEX idx_meeting_participants_status ON meeting_participants(status);

-- ═══════════════════════════════════════════════════════════════════════════
-- 3. MEETING MESSAGES TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS meeting_messages (
    message_id VARCHAR(100) PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    meeting_id VARCHAR(100) NOT NULL,
    
    -- Sender info
    sender_id VARCHAR(100) NOT NULL,
    sender_type VARCHAR(50) NOT NULL,
    sender_name VARCHAR(200) NOT NULL,
    
    -- Message content
    content TEXT NOT NULL,
    
    -- Token/Cost tracking
    tokens INTEGER NOT NULL DEFAULT 0,
    cost DECIMAL(10,4) NOT NULL DEFAULT 0.0000,
    
    -- LLM info (for agent messages)
    llm_provider VARCHAR(50),
    llm_model VARCHAR(100),
    
    -- Metadata
    is_system_message BOOLEAN DEFAULT FALSE,
    is_summarized BOOLEAN DEFAULT FALSE,
    original_message_id VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Foreign Keys
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT check_sender_type CHECK (sender_type IN ('user', 'agent', 'system'))
);

-- Indexes
CREATE INDEX idx_meeting_messages_meeting ON meeting_messages(meeting_id);
CREATE INDEX idx_meeting_messages_sender ON meeting_messages(sender_id);
CREATE INDEX idx_meeting_messages_created_at ON meeting_messages(created_at);
CREATE INDEX idx_meeting_messages_meeting_created ON meeting_messages(meeting_id, created_at);

-- ═══════════════════════════════════════════════════════════════════════════
-- 4. MEETING ANALYTICS TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS meeting_analytics (
    analytics_id VARCHAR(100) PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    meeting_id VARCHAR(100) NOT NULL,
    
    -- Overall metrics
    total_messages INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    total_cost DECIMAL(10,4) NOT NULL DEFAULT 0.0000,
    duration_minutes INTEGER NOT NULL DEFAULT 0,
    
    -- Participant metrics
    total_participants INTEGER NOT NULL DEFAULT 0,
    participants_data JSONB,  -- Per-agent breakdown
    
    -- Quality metrics
    avg_message_length INTEGER,
    avg_response_time_seconds INTEGER,
    topic_coverage JSONB,  -- AI-analyzed topics discussed
    
    -- Optimization metrics
    token_optimizations_applied INTEGER DEFAULT 0,
    tokens_saved INTEGER DEFAULT 0,
    cost_saved DECIMAL(10,4) DEFAULT 0.0000,
    
    -- Engagement metrics
    most_active_agent VARCHAR(100),
    least_active_agent VARCHAR(100),
    conversation_flow_rating DECIMAL(3,2),  -- 0-5 rating
    
    -- Timestamps
    calculated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Foreign Keys
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT unique_meeting_analytics UNIQUE (meeting_id)
);

-- Indexes
CREATE INDEX idx_meeting_analytics_meeting ON meeting_analytics(meeting_id);
CREATE INDEX idx_meeting_analytics_calculated_at ON meeting_analytics(calculated_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════
-- 5. MEETING ACTION ITEMS TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS meeting_action_items (
    action_item_id VARCHAR(100) PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    meeting_id VARCHAR(100) NOT NULL,
    
    -- Action item details
    description TEXT NOT NULL,
    assigned_to VARCHAR(100),  -- Agent ID or user ID
    assigned_type VARCHAR(50),  -- 'agent' or 'user'
    priority VARCHAR(50) DEFAULT 'medium',
    status VARCHAR(50) DEFAULT 'pending',
    
    -- Due date
    due_date TIMESTAMP,
    
    -- Completion
    completed_at TIMESTAMP,
    completed_by VARCHAR(100),
    
    -- External linking
    external_task_id VARCHAR(200),  -- ClickUp, Jira, etc.
    external_platform VARCHAR(50),  -- 'clickup', 'jira', etc.
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Foreign Keys
    FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT check_action_priority CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    CONSTRAINT check_action_status CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    CONSTRAINT check_assigned_type CHECK (assigned_type IN ('agent', 'user', 'external'))
);

-- Indexes
CREATE INDEX idx_action_items_meeting ON meeting_action_items(meeting_id);
CREATE INDEX idx_action_items_assigned_to ON meeting_action_items(assigned_to);
CREATE INDEX idx_action_items_status ON meeting_action_items(status);
CREATE INDEX idx_action_items_due_date ON meeting_action_items(due_date);

-- ═══════════════════════════════════════════════════════════════════════════
-- 6. MEETING TEMPLATES TABLE
-- ═══════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS meeting_templates (
    template_id VARCHAR(100) PRIMARY KEY DEFAULT gen_random_uuid()::TEXT,
    template_name VARCHAR(200) NOT NULL,
    created_by_user_id VARCHAR(100) NOT NULL,
    
    -- Template configuration
    mode VARCHAR(50) NOT NULL DEFAULT 'round-robin',
    default_agent_ids JSONB,  -- List of default agents
    tokens_limit INTEGER DEFAULT 20000,
    cost_limit DECIMAL(10,2) DEFAULT 5.00,
    
    -- Settings
    settings JSONB,  -- All other settings
    
    -- Usage tracking
    times_used INTEGER DEFAULT 0,
    
    -- Sharing
    is_public BOOLEAN DEFAULT FALSE,
    is_system_template BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Foreign Keys
    FOREIGN KEY (created_by_user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Constraints
    CONSTRAINT check_template_mode CHECK (mode IN ('round-robin', 'free', 'moderated', 'hierarchical'))
);

-- Indexes
CREATE INDEX idx_meeting_templates_user ON meeting_templates(created_by_user_id);
CREATE INDEX idx_meeting_templates_public ON meeting_templates(is_public);
CREATE INDEX idx_meeting_templates_system ON meeting_templates(is_system_template);

-- ═══════════════════════════════════════════════════════════════════════════
-- VIEWS
-- ═══════════════════════════════════════════════════════════════════════════

-- View: Active Meetings with Participant Count
CREATE OR REPLACE VIEW v_active_meetings AS
SELECT 
    m.meeting_id,
    m.meeting_name,
    m.created_by_user_id,
    m.mode,
    m.status,
    m.tokens_used,
    m.tokens_limit,
    ROUND((m.tokens_used::NUMERIC / m.tokens_limit::NUMERIC * 100), 2) AS tokens_percent,
    m.cost_so_far,
    m.cost_limit,
    ROUND((m.cost_so_far::NUMERIC / m.cost_limit::NUMERIC * 100), 2) AS cost_percent,
    COUNT(DISTINCT mp.agent_id) AS participant_count,
    COUNT(DISTINCT mm.message_id) AS message_count,
    EXTRACT(EPOCH FROM (NOW() - m.started_at)) / 60 AS duration_minutes,
    m.started_at,
    m.project_id,
    m.task_id
FROM meetings m
LEFT JOIN meeting_participants mp ON m.meeting_id = mp.meeting_id AND mp.status = 'active'
LEFT JOIN meeting_messages mm ON m.meeting_id = mm.meeting_id
WHERE m.status = 'active'
GROUP BY m.meeting_id;

-- View: Meeting History with Analytics
CREATE OR REPLACE VIEW v_meeting_history AS
SELECT 
    m.meeting_id,
    m.meeting_name,
    m.created_by_user_id,
    u.full_name AS created_by_name,
    m.status,
    m.mode,
    COUNT(DISTINCT mp.agent_id) AS participant_count,
    COUNT(DISTINCT mm.message_id) AS message_count,
    m.tokens_used,
    m.cost_so_far,
    EXTRACT(EPOCH FROM (COALESCE(m.ended_at, NOW()) - m.started_at)) / 60 AS duration_minutes,
    m.started_at,
    m.ended_at,
    m.summary IS NOT NULL AS has_summary,
    COALESCE(jsonb_array_length(m.action_items), 0) AS action_items_count
FROM meetings m
LEFT JOIN users u ON m.created_by_user_id = u.user_id
LEFT JOIN meeting_participants mp ON m.meeting_id = mp.meeting_id
LEFT JOIN meeting_messages mm ON m.meeting_id = mm.meeting_id
GROUP BY m.meeting_id, u.full_name;

-- View: User Meeting Statistics
CREATE OR REPLACE VIEW v_user_meeting_stats AS
SELECT 
    u.user_id,
    u.full_name,
    COUNT(DISTINCT m.meeting_id) AS total_meetings,
    COUNT(DISTINCT CASE WHEN m.status = 'active' THEN m.meeting_id END) AS active_meetings,
    COUNT(DISTINCT CASE WHEN m.status = 'ended' THEN m.meeting_id END) AS completed_meetings,
    SUM(m.cost_so_far) AS total_meeting_cost,
    AVG(m.tokens_used) AS avg_tokens_per_meeting,
    AVG(EXTRACT(EPOCH FROM (COALESCE(m.ended_at, NOW()) - m.started_at)) / 60) AS avg_duration_minutes
FROM users u
LEFT JOIN meetings m ON u.user_id = m.created_by_user_id
GROUP BY u.user_id, u.full_name;

-- ═══════════════════════════════════════════════════════════════════════════
-- FUNCTIONS
-- ═══════════════════════════════════════════════════════════════════════════

-- Function: Calculate Meeting Duration
CREATE OR REPLACE FUNCTION calculate_meeting_duration(p_meeting_id VARCHAR)
RETURNS INTEGER AS $$
DECLARE
    v_duration INTEGER;
BEGIN
    SELECT EXTRACT(EPOCH FROM (COALESCE(ended_at, NOW()) - started_at)) / 60
    INTO v_duration
    FROM meetings
    WHERE meeting_id = p_meeting_id;
    
    RETURN COALESCE(v_duration, 0);
END;
$$ LANGUAGE plpgsql;

-- Function: Get Meeting Summary
CREATE OR REPLACE FUNCTION get_meeting_summary(p_meeting_id VARCHAR)
RETURNS TABLE (
    meeting_name VARCHAR,
    duration_minutes INTEGER,
    participant_count BIGINT,
    message_count BIGINT,
    total_tokens INTEGER,
    total_cost DECIMAL,
    action_items_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.meeting_name,
        calculate_meeting_duration(p_meeting_id),
        COUNT(DISTINCT mp.agent_id),
        COUNT(DISTINCT mm.message_id),
        m.tokens_used,
        m.cost_so_far,
        COALESCE(jsonb_array_length(m.action_items), 0)
    FROM meetings m
    LEFT JOIN meeting_participants mp ON m.meeting_id = mp.meeting_id
    LEFT JOIN meeting_messages mm ON m.meeting_id = mm.meeting_id
    WHERE m.meeting_id = p_meeting_id
    GROUP BY m.meeting_id;
END;
$$ LANGUAGE plpgsql;

-- ═══════════════════════════════════════════════════════════════════════════
-- TRIGGERS
-- ═══════════════════════════════════════════════════════════════════════════

-- Trigger: Update meetings.updated_at on changes
CREATE TRIGGER trigger_meetings_updated_at
    BEFORE UPDATE ON meetings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger: Update meeting_action_items.updated_at on changes
CREATE TRIGGER trigger_action_items_updated_at
    BEFORE UPDATE ON meeting_action_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger: Update meeting_templates.updated_at on changes
CREATE TRIGGER trigger_templates_updated_at
    BEFORE UPDATE ON meeting_templates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ═══════════════════════════════════════════════════════════════════════════
-- SAMPLE DATA
-- ═══════════════════════════════════════════════════════════════════════════

-- Sample Template: Brainstorm Session
INSERT INTO meeting_templates (
    template_id, template_name, created_by_user_id, mode,
    default_agent_ids, tokens_limit, cost_limit, is_system_template
) VALUES (
    'template_brainstorm_001',
    'Brainstorm Session',
    'system',
    'free',
    '["data_scientist", "architect", "marketing_strategist", "creative_director"]'::jsonb,
    25000,
    8.00,
    TRUE
);

-- Sample Template: Code Review
INSERT INTO meeting_templates (
    template_id, template_name, created_by_user_id, mode,
    default_agent_ids, tokens_limit, cost_limit, is_system_template
) VALUES (
    'template_code_review_001',
    'Code Review Meeting',
    'system',
    'round-robin',
    '["backend_developer", "frontend_developer", "qa_engineer", "devops_engineer"]'::jsonb,
    15000,
    5.00,
    TRUE
);

-- Sample Template: Planning Meeting
INSERT INTO meeting_templates (
    template_id, template_name, created_by_user_id, mode,
    default_agent_ids, tokens_limit, cost_limit, is_system_template
) VALUES (
    'template_planning_001',
    'Planning Meeting',
    'system',
    'hierarchical',
    '["project_manager", "data_analyst", "financial_analyst", "architect"]'::jsonb,
    20000,
    6.00,
    TRUE
);

-- ═══════════════════════════════════════════════════════════════════════════
-- COMMENTS
-- ═══════════════════════════════════════════════════════════════════════════

COMMENT ON TABLE meetings IS 'Multi-agent meeting rooms for collaborative work';
COMMENT ON TABLE meeting_participants IS 'Agents participating in meetings';
COMMENT ON TABLE meeting_messages IS 'All messages exchanged in meetings';
COMMENT ON TABLE meeting_analytics IS 'Analytics and metrics for completed meetings';
COMMENT ON TABLE meeting_action_items IS 'Action items extracted from meetings';
COMMENT ON TABLE meeting_templates IS 'Reusable meeting configurations';

-- ═══════════════════════════════════════════════════════════════════════════
-- SUCCESS MESSAGE
-- ═══════════════════════════════════════════════════════════════════════════

DO $$
BEGIN
    RAISE NOTICE '✅ Meeting Rooms schema created successfully!';
    RAISE NOTICE '📊 Tables: meetings, meeting_participants, meeting_messages, meeting_analytics, meeting_action_items, meeting_templates';
    RAISE NOTICE '🔍 Views: v_active_meetings, v_meeting_history, v_user_meeting_stats';
    RAISE NOTICE '⚡ Functions: calculate_meeting_duration, get_meeting_summary';
    RAISE NOTICE '🎯 Ready for multi-agent collaboration!';
END $$;
