-- ============================================
-- CHENU - Schema PostgreSQL Complet
-- ============================================
-- Version: 1.0
-- Description: Base de données pour CHENU AI Creative Suite
-- ============================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Pour recherche full-text

-- ============================================
-- ENUMS
-- ============================================

CREATE TYPE agent_level AS ENUM ('L1', 'L2', 'L3');
CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed', 'failed', 'delegated', 'cancelled');
CREATE TYPE task_priority AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE workflow_status AS ENUM ('draft', 'active', 'paused', 'completed', 'archived');
CREATE TYPE tool_category AS ENUM ('communication', 'data', 'research', 'content', 'marketing', 'integrations', 'ai_ml', 'utilities', 'storage', 'security');
CREATE TYPE integration_type AS ENUM ('clickup', 'google_drive', 'notion', 'slack', 'hubspot', 'zapier', 'custom');

-- ============================================
-- TABLES PRINCIPALES
-- ============================================

-- Utilisateurs
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    role VARCHAR(50) DEFAULT 'user',
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login_at TIMESTAMP WITH TIME ZONE
);

-- Workspaces
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    owner_id UUID REFERENCES users(id) ON DELETE SET NULL,
    settings JSONB DEFAULT '{}',
    token_budget INTEGER DEFAULT 1000000,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Membres du workspace
CREATE TABLE workspace_members (
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (workspace_id, user_id)
);

-- ============================================
-- AGENTS
-- ============================================

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    external_id VARCHAR(100) NOT NULL, -- Ex: "creative_director"
    name VARCHAR(255) NOT NULL,
    icon VARCHAR(10),
    level agent_level NOT NULL,
    department VARCHAR(100),
    description TEXT,
    system_prompt TEXT NOT NULL,
    speciality VARCHAR(100),
    max_concurrent_tasks INTEGER DEFAULT 5,
    is_active BOOLEAN DEFAULT TRUE,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(workspace_id, external_id)
);

-- Relations de délégation entre agents
CREATE TABLE agent_delegations (
    parent_agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    child_agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    priority INTEGER DEFAULT 0,
    PRIMARY KEY (parent_agent_id, child_agent_id)
);

-- ============================================
-- OUTILS
-- ============================================

CREATE TABLE tools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    icon VARCHAR(10),
    category tool_category NOT NULL,
    description TEXT,
    cost_tokens INTEGER DEFAULT 100,
    parameters JSONB DEFAULT '{}',
    is_premium BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Outils assignés aux agents
CREATE TABLE agent_tools (
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES tools(id) ON DELETE CASCADE,
    config_override JSONB DEFAULT '{}',
    PRIMARY KEY (agent_id, tool_id)
);

-- ============================================
-- TÂCHES
-- ============================================

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    parent_task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    assigned_agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    external_id VARCHAR(100),
    title VARCHAR(500),
    description TEXT NOT NULL,
    status task_status DEFAULT 'pending',
    priority task_priority DEFAULT 'medium',
    
    context JSONB DEFAULT '{}',
    result JSONB,
    error_message TEXT,
    
    tokens_used INTEGER DEFAULT 0,
    execution_time_ms INTEGER,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    
    scheduled_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour les requêtes fréquentes
CREATE INDEX idx_tasks_workspace_status ON tasks(workspace_id, status);
CREATE INDEX idx_tasks_agent ON tasks(assigned_agent_id);
CREATE INDEX idx_tasks_parent ON tasks(parent_task_id);
CREATE INDEX idx_tasks_created ON tasks(created_at DESC);

-- ============================================
-- WORKFLOWS
-- ============================================

CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon VARCHAR(10),
    trigger_type VARCHAR(50), -- 'manual', 'scheduled', 'event', 'webhook'
    trigger_config JSONB DEFAULT '{}',
    status workflow_status DEFAULT 'draft',
    is_template BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Étapes du workflow
CREATE TABLE workflow_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    step_order INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    action TEXT NOT NULL,
    expected_output TEXT,
    config JSONB DEFAULT '{}',
    timeout_seconds INTEGER DEFAULT 300,
    on_failure VARCHAR(50) DEFAULT 'stop', -- 'stop', 'continue', 'retry'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Exécutions de workflow
CREATE TABLE workflow_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
    triggered_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    status task_status DEFAULT 'pending',
    current_step INTEGER DEFAULT 0,
    context JSONB DEFAULT '{}',
    result JSONB,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- CHAÎNES D'OUTILS (Tool Chains)
-- ============================================

CREATE TABLE tool_chains (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_preset BOOLEAN DEFAULT FALSE,
    created_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE tool_chain_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chain_id UUID REFERENCES tool_chains(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES tools(id) ON DELETE CASCADE,
    step_order INTEGER NOT NULL,
    config JSONB DEFAULT '{}'
);

-- ============================================
-- INTÉGRATIONS
-- ============================================

CREATE TABLE integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    type integration_type NOT NULL,
    name VARCHAR(255) NOT NULL,
    config JSONB NOT NULL, -- Encrypted credentials
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Mappings de synchronisation
CREATE TABLE integration_mappings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    integration_id UUID REFERENCES integrations(id) ON DELETE CASCADE,
    local_entity_type VARCHAR(50), -- 'task', 'agent', 'workflow'
    local_entity_id UUID,
    external_entity_type VARCHAR(50),
    external_entity_id VARCHAR(255),
    sync_direction VARCHAR(20) DEFAULT 'bidirectional', -- 'push', 'pull', 'bidirectional'
    last_synced_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- ANALYTICS & LOGS
-- ============================================

CREATE TABLE task_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    log_level VARCHAR(20) DEFAULT 'info',
    message TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_task_logs_task ON task_logs(task_id);
CREATE INDEX idx_task_logs_created ON task_logs(created_at DESC);

CREATE TABLE tool_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES tools(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    tokens_used INTEGER DEFAULT 0,
    execution_time_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tool_usage_workspace ON tool_usage(workspace_id, created_at DESC);

-- Stats agrégées quotidiennes
CREATE TABLE daily_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    total_tool_calls INTEGER DEFAULT 0,
    avg_task_duration_ms INTEGER,
    most_used_agent_id UUID REFERENCES agents(id),
    most_used_tool_id UUID REFERENCES tools(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(workspace_id, date)
);

-- ============================================
-- SESSIONS & CONVERSATIONS
-- ============================================

CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255),
    context JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    tokens INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at);

-- ============================================
-- FILES & ASSETS
-- ============================================

CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    uploaded_by_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    name VARCHAR(500) NOT NULL,
    mime_type VARCHAR(100),
    size_bytes BIGINT,
    storage_path TEXT NOT NULL,
    storage_provider VARCHAR(50) DEFAULT 'local', -- 'local', 's3', 'gcs', 'drive'
    external_id VARCHAR(255), -- ID in external storage
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- FONCTIONS & TRIGGERS
-- ============================================

-- Fonction pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers pour updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_workspaces_updated_at BEFORE UPDATE ON workspaces
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_integrations_updated_at BEFORE UPDATE ON integrations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Fonction pour mettre à jour les tokens du workspace
CREATE OR REPLACE FUNCTION update_workspace_tokens()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        UPDATE workspaces 
        SET tokens_used = tokens_used + NEW.tokens_used
        WHERE id = NEW.workspace_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tokens_on_task_complete AFTER UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_workspace_tokens();

-- ============================================
-- VUES UTILES
-- ============================================

-- Vue des tâches actives avec info agent
CREATE VIEW active_tasks_view AS
SELECT 
    t.*,
    a.name as agent_name,
    a.icon as agent_icon,
    a.level as agent_level,
    u.name as created_by_name
FROM tasks t
LEFT JOIN agents a ON t.assigned_agent_id = a.id
LEFT JOIN users u ON t.created_by_user_id = u.id
WHERE t.status IN ('pending', 'in_progress');

-- Vue des stats par agent
CREATE VIEW agent_stats_view AS
SELECT 
    a.id,
    a.name,
    a.level,
    COUNT(t.id) as total_tasks,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN t.status = 'failed' THEN 1 END) as failed_tasks,
    AVG(t.execution_time_ms) as avg_execution_time,
    SUM(t.tokens_used) as total_tokens
FROM agents a
LEFT JOIN tasks t ON a.id = t.assigned_agent_id
GROUP BY a.id, a.name, a.level;

-- ============================================
-- DONNÉES INITIALES
-- ============================================

-- Insérer les outils de base
INSERT INTO tools (external_id, name, icon, category, description, cost_tokens) VALUES
-- Communication
('email_sender', 'Email Sender', '📧', 'communication', 'Envoi d''emails', 50),
('slack_poster', 'Slack Poster', '💬', 'communication', 'Publication Slack', 30),
('sms_sender', 'SMS Sender', '📱', 'communication', 'Envoi de SMS', 100),
('webhook_caller', 'Webhook Caller', '🔗', 'communication', 'Appel de webhooks', 20),
-- Data
('csv_parser', 'CSV Parser', '📊', 'data', 'Parsing de fichiers CSV', 30),
('json_transformer', 'JSON Transformer', '🔄', 'data', 'Transformation JSON', 25),
('pdf_extractor', 'PDF Extractor', '📄', 'data', 'Extraction de PDF', 150),
-- AI
('sentiment_analyzer', 'Sentiment Analyzer', '😊', 'ai_ml', 'Analyse de sentiment', 100),
('entity_extractor', 'Entity Extractor', '🏷️', 'ai_ml', 'Extraction d''entités', 150),
('chatbot_engine', 'Chatbot Engine', '🤖', 'ai_ml', 'IA conversationnelle', 300);

-- Done!
SELECT 'CHENU Database Schema Created Successfully!' as status;
