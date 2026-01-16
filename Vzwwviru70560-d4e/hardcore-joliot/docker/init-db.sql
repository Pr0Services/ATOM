-- CHE·NU™ V75 — Database Initialization
-- ======================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
DO $$ BEGIN
    CREATE TYPE thread_status AS ENUM ('active', 'paused', 'archived', 'completed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE thread_maturity AS ENUM ('seed', 'sprouting', 'growing', 'mature', 'archived');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE checkpoint_type AS ENUM ('governance', 'cost', 'sensitive', 'cross_sphere', 'identity');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE checkpoint_status AS ENUM ('pending', 'approved', 'rejected');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE decision_status AS ENUM ('pending', 'resolved', 'deferred', 'escalated');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    avatar_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    preferences JSONB DEFAULT '{}',
    token_budget INTEGER DEFAULT 500000,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Spheres table
CREATE TABLE IF NOT EXISTS spheres (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert default spheres
INSERT INTO spheres (id, name, description, icon, color) VALUES
    ('personal', 'Personal', 'Vie personnelle, notes, tâches, habitudes', 'Home', '#4F46E5'),
    ('business', 'Business', 'Entreprise, CRM, facturation, projets pro', 'Briefcase', '#059669'),
    ('government', 'Government', 'Relations institutionnelles, compliance', 'Building', '#DC2626'),
    ('creative_studio', 'Creative Studio', 'Création, design, médias, génération AI', 'Palette', '#7C3AED'),
    ('community', 'Community', 'Groupes, événements, coordination', 'Users', '#F59E0B'),
    ('social', 'Social & Media', 'Réseaux sociaux, publication, scheduling', 'Share2', '#EC4899'),
    ('entertainment', 'Entertainment', 'Streaming, jeux, contenu divertissement', 'Film', '#06B6D4'),
    ('my_team', 'My Team', 'Collaboration équipe, ressources humaines', 'Users', '#8B5CF6'),
    ('scholar', 'Scholar', 'Recherche, académique, apprentissage', 'GraduationCap', '#10B981')
ON CONFLICT (id) DO NOTHING;

-- Threads table
CREATE TABLE IF NOT EXISTS threads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    founding_intent TEXT NOT NULL,
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    sphere_id VARCHAR(50) NOT NULL REFERENCES spheres(id),
    parent_thread_id UUID REFERENCES threads(id),
    status thread_status DEFAULT 'active',
    maturity thread_maturity DEFAULT 'seed',
    visibility VARCHAR(20) DEFAULT 'private',
    metadata JSONB DEFAULT '{}',
    events_count INTEGER DEFAULT 0,
    decisions_pending INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Thread events table
CREATE TABLE IF NOT EXISTS thread_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    created_by UUID REFERENCES users(id),
    parent_event_id UUID REFERENCES thread_events(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Agents table
CREATE TABLE IF NOT EXISTS agents (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    domain VARCHAR(50) NOT NULL,
    level INTEGER DEFAULT 1,
    capabilities JSONB DEFAULT '[]',
    token_cost INTEGER DEFAULT 100,
    description TEXT,
    sphere_restrictions JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User agents (hired agents)
CREATE TABLE IF NOT EXISTS user_agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL REFERENCES agents(id),
    hired_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    configuration JSONB DEFAULT '{}',
    UNIQUE(user_id, agent_id)
);

-- Checkpoints table
CREATE TABLE IF NOT EXISTS checkpoints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type checkpoint_type NOT NULL,
    status checkpoint_status DEFAULT 'pending',
    reason TEXT NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255),
    resource_type VARCHAR(50),
    initiated_by UUID REFERENCES users(id),
    resolved_by UUID REFERENCES users(id),
    context JSONB DEFAULT '{}',
    resolution TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Decisions table
CREATE TABLE IF NOT EXISTS decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    context TEXT,
    thread_id UUID REFERENCES threads(id) ON DELETE SET NULL,
    owner_id UUID NOT NULL REFERENCES users(id),
    status decision_status DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    deadline TIMESTAMP WITH TIME ZONE,
    options JSONB DEFAULT '[]',
    selected_option JSONB,
    resolution_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Nova conversations table
CREATE TABLE IF NOT EXISTS nova_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    pipeline_status JSONB,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    action_url VARCHAR(500),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit log table
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_threads_owner ON threads(owner_id);
CREATE INDEX IF NOT EXISTS idx_threads_sphere ON threads(sphere_id);
CREATE INDEX IF NOT EXISTS idx_threads_status ON threads(status);
CREATE INDEX IF NOT EXISTS idx_thread_events_thread ON thread_events(thread_id);
CREATE INDEX IF NOT EXISTS idx_thread_events_type ON thread_events(event_type);
CREATE INDEX IF NOT EXISTS idx_checkpoints_status ON checkpoints(status);
CREATE INDEX IF NOT EXISTS idx_decisions_status ON decisions(status);
CREATE INDEX IF NOT EXISTS idx_decisions_owner ON decisions(owner_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_action ON audit_log(action);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to tables
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_threads_updated_at ON threads;
CREATE TRIGGER update_threads_updated_at BEFORE UPDATE ON threads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert test user (password: test123)
INSERT INTO users (id, email, hashed_password, name, token_budget, is_verified)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'test@chenu.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G7VVJSYzqYe6Hy',
    'Jo',
    500000,
    true
) ON CONFLICT (email) DO NOTHING;

-- Insert sample agents
INSERT INTO agents (id, name, domain, level, capabilities, token_cost, description, sphere_restrictions) VALUES
    ('agent-coordinator', 'Project Coordinator', 'business', 2, '["project_planning", "resource_allocation"]', 500, 'Coordonne les projets', '["business", "my_team"]'),
    ('agent-researcher', 'Research Analyst', 'scholar', 3, '["literature_review", "data_analysis"]', 750, 'Analyse la recherche', '["scholar", "personal"]'),
    ('agent-creator', 'Content Creator', 'creative', 2, '["content_writing", "image_generation"]', 600, 'Crée du contenu', '["creative_studio", "social"]'),
    ('agent-finance', 'Financial Advisor', 'finance', 3, '["budget_planning", "financial_analysis"]', 800, 'Conseille finances', '["business", "personal"]'),
    ('agent-automator', 'Task Automator', 'productivity', 1, '["task_scheduling", "workflow_automation"]', 300, 'Automatise les tâches', '["personal", "business"]')
ON CONFLICT (id) DO NOTHING;

COMMIT;
