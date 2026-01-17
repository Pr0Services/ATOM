-- ╔══════════════════════════════════════════════════════════════════════════════╗
-- ║                         AT·OM - INFRASTRUCTURE INVISIBLE                      ║
-- ║                                                                              ║
-- ║            PROPRIÉTÉ EXCLUSIVE DE JONATHAN EMMANUEL RODRIGUE                 ║
-- ║                    TOUS DROITS RÉSERVÉS - BREVET EN COURS                    ║
-- ║                                    2025                                       ║
-- ╚══════════════════════════════════════════════════════════════════════════════╝
--
-- SCHÉMA POSTGRESQL v15+ POUR NOVA-999
-- Database: defaultdb @ db-postgresql-nyc9-999-999-do-user-32084357-0.h.db.ondigitalocean.com
-- ═══════════════════════════════════════════════════════════════════════════════

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: spheres (16 Sphères de l'Essaim)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS spheres (
    id              SERIAL PRIMARY KEY,
    code            VARCHAR(20) UNIQUE NOT NULL,
    name            VARCHAR(100) NOT NULL,
    description     TEXT,
    color           VARCHAR(7) DEFAULT '#0047AB',
    frequency_base  INTEGER DEFAULT 999,
    agent_count     INTEGER DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour recherche rapide
CREATE INDEX idx_spheres_code ON spheres(code);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: agents (6500 Agents de l'Essaim)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS agents (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id        VARCHAR(50) UNIQUE NOT NULL,       -- Ex: "TECH-001", "FIN-042"
    name            VARCHAR(200) NOT NULL,
    sphere_id       INTEGER REFERENCES spheres(id),

    -- Métadonnées Agent
    specialty       VARCHAR(200),
    function        TEXT,
    description     TEXT,

    -- Fréquence AT·OM
    frequency       INTEGER DEFAULT 999,               -- Hz (432-999)
    resonance_level DECIMAL(5,2) DEFAULT 1.00,        -- Niveau de résonance (0.00-9.99)

    -- Source & Fichier
    source_file     VARCHAR(500),                      -- Chemin fichier original
    file_hash       VARCHAR(64),                       -- SHA-256 du contenu
    file_size       BIGINT,                            -- Taille en bytes
    content_type    VARCHAR(100),                      -- MIME type

    -- Données brutes (JSONB pour flexibilité)
    metadata        JSONB DEFAULT '{}',
    raw_content     TEXT,                              -- Contenu texte si applicable

    -- État & Contrôle
    status          VARCHAR(20) DEFAULT 'active',      -- active, dormant, dispersed
    last_activated  TIMESTAMP WITH TIME ZONE,
    activation_count INTEGER DEFAULT 0,

    -- Audit
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    imported_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour performance sur 6500+ entrées
CREATE INDEX idx_agents_sphere ON agents(sphere_id);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_frequency ON agents(frequency);
CREATE INDEX idx_agents_specialty ON agents(specialty);
CREATE INDEX idx_agents_metadata ON agents USING GIN(metadata);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: modules (Génie, Alchimie, Flux, Santé + V68)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS modules (
    id              SERIAL PRIMARY KEY,
    code            VARCHAR(50) UNIQUE NOT NULL,
    name            VARCHAR(100) NOT NULL,
    version         VARCHAR(20) DEFAULT 'V68',
    description     TEXT,
    config          JSONB DEFAULT '{}',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: agent_modules (Association N:N)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS agent_modules (
    agent_id        UUID REFERENCES agents(id) ON DELETE CASCADE,
    module_id       INTEGER REFERENCES modules(id) ON DELETE CASCADE,
    assigned_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (agent_id, module_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: protocol_999_logs (Brise-Circuit / Kill Switch)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS protocol_999_logs (
    id              SERIAL PRIMARY KEY,
    action_type     VARCHAR(50) NOT NULL,              -- partial, sectoral, total
    dispersion_pct  INTEGER NOT NULL,                  -- 20, 50, 100
    affected_count  INTEGER DEFAULT 0,
    initiated_by    VARCHAR(100),
    confirmation_code VARCHAR(50),
    executed_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata        JSONB DEFAULT '{}'
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: activity_log (Causalité - Loi 6)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS activity_log (
    id              BIGSERIAL PRIMARY KEY,
    event_type      VARCHAR(50) NOT NULL,
    entity_type     VARCHAR(50),                       -- agent, sphere, module, protocol
    entity_id       VARCHAR(100),
    action          VARCHAR(100),
    details         JSONB DEFAULT '{}',
    ip_address      INET,
    user_agent      TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour requêtes temporelles
CREATE INDEX idx_activity_created ON activity_log(created_at DESC);
CREATE INDEX idx_activity_entity ON activity_log(entity_type, entity_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- DONNÉES INITIALES: 15 Sphères Canon AT·OM (350 agents total)
-- ═══════════════════════════════════════════════════════════════════════════════
INSERT INTO spheres (code, name, description, color, agent_count) VALUES
    ('PERSONAL', 'Personnel', 'Agents personnels et assistants', '#4A90D9', 28),
    ('BUSINESS', 'Business', 'Agents commerciaux et entreprise', '#50C878', 43),
    ('GOVERNMENT', 'Gouvernement', 'Agents institutionnels et publics', '#9B59B6', 18),
    ('CREATIVE', 'Créatif', 'Agents artistiques et design', '#F39C12', 42),
    ('COMMUNITY', 'Communauté', 'Agents communautaires', '#E74C3C', 12),
    ('SOCIAL', 'Social', 'Agents réseaux sociaux', '#1ABC9C', 15),
    ('ENTERTAINMENT', 'Divertissement', 'Agents média et loisirs', '#E91E63', 8),
    ('TEAM', 'Équipe', 'Agents collaboration et équipe', '#3498DB', 35),
    ('SCHOLAR', 'Éducation', 'Agents éducatifs et formation', '#8E44AD', 25),
    ('TRANSPORT', 'Transport', 'Agents mobilité et logistique', '#27AE60', 50),
    ('SOCIETAL', 'Sociétal', 'Agents impact sociétal', '#F1C40F', 20),
    ('ENVIRONMENT', 'Environnement', 'Agents écologie et durabilité', '#2ECC71', 25),
    ('PRIVACY', 'Vie Privée', 'Agents protection données', '#95A5A6', 8),
    ('JEUNESSE', 'Jeunesse', 'Agents jeunesse et avenir', '#FF6B6B', 15),
    ('DASHBOARD', 'Tableau de Bord', 'Agents monitoring souverain', '#D4AF37', 6)
ON CONFLICT (code) DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- DONNÉES INITIALES: Modules V68
-- ═══════════════════════════════════════════════════════════════════════════════
INSERT INTO modules (code, name, version, description) VALUES
    ('GENIE', 'Génie', 'V68', 'Module d''intelligence et résolution'),
    ('ALCHIMIE', 'Alchimie', 'V68', 'Transformation et synthèse'),
    ('FLUX', 'Flux', 'V68', 'Gestion des flux de données'),
    ('SANTE', 'Santé', 'V68', 'Monitoring et bien-être système'),
    ('SCEAU', 'Le Sceau', 'V68', 'Authentification souveraine'),
    ('ESSAIM', 'L''Essaim', 'V68', 'Coordination multi-agents'),
    ('PROTOCOL999', 'Protocol-999', 'V68', 'Brise-circuit d''urgence')
ON CONFLICT (code) DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FONCTION: Mise à jour automatique updated_at
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER trigger_spheres_updated
    BEFORE UPDATE ON spheres
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_agents_updated
    BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ═══════════════════════════════════════════════════════════════════════════════
-- VUE: Dashboard Essaim
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE OR REPLACE VIEW v_essaim_dashboard AS
SELECT
    s.code AS sphere_code,
    s.name AS sphere_name,
    s.color,
    COUNT(a.id) AS total_agents,
    COUNT(CASE WHEN a.status = 'active' THEN 1 END) AS active_agents,
    AVG(a.frequency) AS avg_frequency,
    MAX(a.last_activated) AS last_activity
FROM spheres s
LEFT JOIN agents a ON s.id = a.sphere_id
GROUP BY s.id, s.code, s.name, s.color
ORDER BY total_agents DESC;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN DU SCHÉMA NOVA-999
-- ═══════════════════════════════════════════════════════════════════════════════
