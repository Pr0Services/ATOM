-- ============================================================================
-- LA FORGE - MOTEUR DE CIVILISATION
-- Board des Rôles, Agents d'Étude & Espace Projets
-- ============================================================================
-- La Forge transforme l'Arche d'un logiciel en société opérationnelle
-- capable de recruter, organiser et exécuter des projets.
-- ============================================================================

-- ============================================================================
-- PARTIE 1: BOARD DES RÔLES (STRUCTURE DE COMMANDEMENT)
-- ============================================================================

-- Catégories de rôles
CREATE TYPE role_category AS ENUM (
    'operations',      -- Gardiens de la Grid
    'legal_finance',   -- Architectes de Transition
    'human_relations', -- Médiateurs de Résonance
    'market_research', -- Explorateurs d'Actifs
    'technology',      -- Développeurs & Ingénieurs
    'communication',   -- Ambassadeurs & Créateurs
    'governance',      -- Conseil & Décision
    'field_ops'        -- Opérations Terrain
);

-- Niveaux de compétence
CREATE TYPE skill_level AS ENUM (
    'beginner',
    'intermediate',
    'advanced',
    'expert',
    'master'
);

-- Définition des rôles de l'Arche
CREATE TABLE IF NOT EXISTS arche_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    code VARCHAR(50) UNIQUE NOT NULL, -- Ex: 'GUARDIAN_GRID_01'
    title VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    category role_category NOT NULL,

    -- Description
    description TEXT NOT NULL,
    responsibilities JSONB DEFAULT '[]', -- Liste des responsabilités
    deliverables JSONB DEFAULT '[]', -- Livrables attendus

    -- Exigences
    required_skills JSONB DEFAULT '[]', -- [{skill, level}]
    min_resonance_score DECIMAL(5, 2) DEFAULT 0,
    min_tenure_months INTEGER DEFAULT 0,

    -- Rémunération
    base_ur_monthly DECIMAL(18, 6) DEFAULT 0,
    performance_bonus_max DECIMAL(18, 6) DEFAULT 0,
    equity_allocation DECIMAL(5, 4) DEFAULT 0, -- % du fond

    -- Capacité
    max_holders INTEGER DEFAULT 1, -- Nombre max de personnes dans ce rôle
    current_holders INTEGER DEFAULT 0,

    -- Hiérarchie
    reports_to UUID REFERENCES arche_roles(id),
    supervision_scope JSONB DEFAULT '[]', -- Rôles supervisés

    -- Statut
    is_active BOOLEAN DEFAULT TRUE,
    is_critical BOOLEAN DEFAULT FALSE, -- Rôle essentiel
    urgency_level INTEGER DEFAULT 0, -- 0-10, pour prioriser recrutement

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Compétences disponibles
CREATE TABLE IF NOT EXISTS skill_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    description TEXT,

    -- Méthode d'évaluation
    assessment_method VARCHAR(50) DEFAULT 'self_declared',
    -- 'self_declared', 'test', 'certification', 'peer_review'

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Compétences des membres
CREATE TABLE IF NOT EXISTS member_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    member_id UUID NOT NULL REFERENCES auth.users(id),
    skill_id UUID NOT NULL REFERENCES skill_definitions(id),

    -- Niveau
    level skill_level NOT NULL,
    years_experience DECIMAL(4, 1) DEFAULT 0,

    -- Validation
    validated BOOLEAN DEFAULT FALSE,
    validated_by UUID REFERENCES auth.users(id),
    validation_date DATE,
    evidence_url TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(member_id, skill_id)
);

-- Assignation des rôles aux membres
CREATE TABLE IF NOT EXISTS role_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    role_id UUID NOT NULL REFERENCES arche_roles(id),
    member_id UUID NOT NULL REFERENCES auth.users(id),

    -- Période
    start_date DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date DATE,

    -- Performance
    performance_score DECIMAL(5, 2) DEFAULT 50,
    last_review_date DATE,

    -- Rémunération effective
    ur_monthly_rate DECIMAL(18, 6),

    -- Statut
    status VARCHAR(50) DEFAULT 'active',
    -- 'pending', 'active', 'on_leave', 'terminated'

    -- Notes
    notes TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(role_id, member_id, start_date)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_role_assignments_member ON role_assignments(member_id);
CREATE INDEX IF NOT EXISTS idx_role_assignments_role ON role_assignments(role_id);
CREATE INDEX IF NOT EXISTS idx_member_skills_member ON member_skills(member_id);

-- ============================================================================
-- PARTIE 2: MOTEUR DE MATCHING (RECRUTEMENT AUTOMATISÉ)
-- ============================================================================

-- Candidatures aux rôles
CREATE TABLE IF NOT EXISTS role_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    role_id UUID NOT NULL REFERENCES arche_roles(id),
    member_id UUID NOT NULL REFERENCES auth.users(id),

    -- Score de matching calculé par L4
    matching_score DECIMAL(5, 2),
    matching_breakdown JSONB DEFAULT '{}',
    -- {skills_match: 85, resonance_match: 90, availability_match: 100}

    -- Motivation
    motivation_text TEXT,
    availability_hours_weekly INTEGER,

    -- Statut
    status VARCHAR(50) DEFAULT 'pending',
    -- 'pending', 'reviewing', 'interview', 'accepted', 'rejected'

    -- Décision
    reviewed_by UUID REFERENCES auth.users(id),
    review_notes TEXT,
    decision_date TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Suggestions de rôles générées par L4
CREATE TABLE IF NOT EXISTS role_suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    member_id UUID NOT NULL REFERENCES auth.users(id),
    role_id UUID NOT NULL REFERENCES arche_roles(id),

    -- Analyse L4
    suggestion_score DECIMAL(5, 2) NOT NULL,
    reasoning TEXT,
    skill_gaps JSONB DEFAULT '[]', -- Compétences manquantes
    development_path JSONB DEFAULT '[]', -- Parcours suggéré

    -- Statut
    presented_at TIMESTAMPTZ,
    member_response VARCHAR(50), -- 'interested', 'not_now', 'declined'
    response_date TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 3: AGENTS D'ÉTUDE DE MARCHÉ
-- ============================================================================

-- Types d'agents
CREATE TYPE market_agent_type AS ENUM (
    'oracle_financier',      -- Surveillance marchés financiers
    'detecteur_foncier',     -- Opportunités terrains/immobilier
    'veille_tech',           -- Brevets et technologies
    'analyse_concurrence',   -- Veille concurrentielle
    'opportunite_partenariat', -- Partenariats potentiels
    'risque_reglementaire'   -- Changements légaux/réglementaires
);

-- Configuration des agents
CREATE TABLE IF NOT EXISTS market_agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    agent_type market_agent_type NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Configuration
    is_active BOOLEAN DEFAULT TRUE,
    scan_frequency_hours INTEGER DEFAULT 24,
    last_scan TIMESTAMPTZ,

    -- Sources surveillées
    data_sources JSONB DEFAULT '[]',
    -- [{name, url, type, priority}]

    -- Filtres
    geographic_focus JSONB DEFAULT '["quebec", "canada"]',
    keywords JSONB DEFAULT '[]',
    exclusions JSONB DEFAULT '[]',

    -- Seuils d'alerte
    alert_thresholds JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Rapports des agents
CREATE TABLE IF NOT EXISTS market_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    agent_id UUID NOT NULL REFERENCES market_agents(id),

    -- Contenu
    report_type VARCHAR(50) NOT NULL,
    -- 'opportunity', 'alert', 'analysis', 'recommendation'

    title VARCHAR(255) NOT NULL,
    summary TEXT NOT NULL,
    full_content JSONB,

    -- Évaluation
    confidence_score DECIMAL(3, 2) DEFAULT 0.50,
    urgency_level INTEGER DEFAULT 5, -- 1-10
    potential_value DECIMAL(18, 2), -- Valeur estimée en CAD

    -- Sources
    source_urls JSONB DEFAULT '[]',
    raw_data JSONB DEFAULT '{}',

    -- Action suggérée
    suggested_action TEXT,
    action_type VARCHAR(50),
    -- 'investigate', 'acquire', 'ignore', 'monitor', 'escalate'

    -- Statut
    status VARCHAR(50) DEFAULT 'new',
    -- 'new', 'reviewed', 'actioned', 'archived'

    reviewed_by UUID REFERENCES auth.users(id),
    review_notes TEXT,

    -- Timestamps
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ
);

-- Index
CREATE INDEX IF NOT EXISTS idx_market_reports_agent ON market_reports(agent_id);
CREATE INDEX IF NOT EXISTS idx_market_reports_status ON market_reports(status);
CREATE INDEX IF NOT EXISTS idx_market_reports_urgency ON market_reports(urgency_level DESC);

-- Suggestions de transaction
CREATE TABLE IF NOT EXISTS transaction_suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    report_id UUID REFERENCES market_reports(id),

    -- Type de transaction
    transaction_type VARCHAR(50) NOT NULL,
    -- 'buy_asset', 'sell_asset', 'convert_currency', 'invest', 'divest'

    -- Détails
    asset_description TEXT NOT NULL,
    estimated_cost DECIMAL(18, 2),
    estimated_value DECIMAL(18, 2),
    roi_estimate DECIMAL(5, 2), -- % retour estimé

    -- Justification
    rationale TEXT,
    risk_assessment TEXT,
    risk_score DECIMAL(3, 2) DEFAULT 0.50,

    -- Timing
    optimal_window_start DATE,
    optimal_window_end DATE,
    time_sensitivity VARCHAR(50), -- 'immediate', 'week', 'month', 'flexible'

    -- Décision
    status VARCHAR(50) DEFAULT 'pending',
    -- 'pending', 'approved', 'rejected', 'executed', 'expired'

    approved_by UUID REFERENCES auth.users(id),
    approval_date TIMESTAMPTZ,
    execution_date TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 4: LA FORGE - ESPACE PROJETS
-- ============================================================================

-- Statuts de projet
CREATE TYPE project_status AS ENUM (
    'draft',
    'proposed',
    'approved',
    'active',
    'paused',
    'completed',
    'cancelled'
);

-- Projets de la Forge
CREATE TABLE IF NOT EXISTS forge_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Catégorie
    category VARCHAR(100),
    -- 'infrastructure', 'acquisition', 'development', 'expansion', 'research'

    -- Budget
    budget_ur DECIMAL(18, 6) DEFAULT 0,
    budget_fiat DECIMAL(18, 2) DEFAULT 0,
    spent_ur DECIMAL(18, 6) DEFAULT 0,
    spent_fiat DECIMAL(18, 2) DEFAULT 0,

    -- Équipe
    lead_member_id UUID REFERENCES auth.users(id),
    team_size_target INTEGER DEFAULT 1,

    -- Objectifs
    objectives JSONB DEFAULT '[]',
    deliverables JSONB DEFAULT '[]',
    success_criteria JSONB DEFAULT '[]',

    -- Calendrier
    planned_start DATE,
    planned_end DATE,
    actual_start DATE,
    actual_end DATE,

    -- Statut
    status project_status DEFAULT 'draft',
    progress_percentage DECIMAL(5, 2) DEFAULT 0,

    -- Gouvernance
    requires_vote BOOLEAN DEFAULT FALSE,
    governance_proposal_id UUID, -- Lien vers governance_proposals si vote requis

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Membres d'équipe projet
CREATE TABLE IF NOT EXISTS project_team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL REFERENCES forge_projects(id) ON DELETE CASCADE,
    member_id UUID NOT NULL REFERENCES auth.users(id),
    role_in_project VARCHAR(100),

    -- Contribution
    hours_allocated_weekly DECIMAL(4, 1) DEFAULT 0,
    ur_rate_hourly DECIMAL(18, 6) DEFAULT 0,

    -- Statut
    status VARCHAR(50) DEFAULT 'active',
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    left_at TIMESTAMPTZ,

    UNIQUE(project_id, member_id)
);

-- Tâches de projet
CREATE TABLE IF NOT EXISTS project_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL REFERENCES forge_projects(id) ON DELETE CASCADE,

    -- Détails
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority INTEGER DEFAULT 5, -- 1-10

    -- Assignation
    assigned_to UUID REFERENCES auth.users(id),

    -- Dates
    due_date DATE,
    completed_at TIMESTAMPTZ,

    -- Statut
    status VARCHAR(50) DEFAULT 'pending',
    -- 'pending', 'in_progress', 'review', 'completed', 'blocked'

    -- Dépendances
    depends_on UUID REFERENCES project_tasks(id),

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chat d'équipe projet (messages)
CREATE TABLE IF NOT EXISTS project_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL REFERENCES forge_projects(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES auth.users(id),

    -- Contenu
    message_type VARCHAR(50) DEFAULT 'text',
    -- 'text', 'file', 'decision', 'milestone', 'alert'

    content TEXT NOT NULL,
    attachments JSONB DEFAULT '[]',

    -- Pour les décisions
    is_decision BOOLEAN DEFAULT FALSE,
    decision_status VARCHAR(50), -- 'proposed', 'approved', 'rejected'

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    edited_at TIMESTAMPTZ
);

-- Index
CREATE INDEX IF NOT EXISTS idx_project_messages_project ON project_messages(project_id);
CREATE INDEX IF NOT EXISTS idx_project_tasks_project ON project_tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_project_tasks_assigned ON project_tasks(assigned_to);

-- Décaissements de projet
CREATE TABLE IF NOT EXISTS project_disbursements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL REFERENCES forge_projects(id),

    -- Montant
    amount_ur DECIMAL(18, 6),
    amount_fiat DECIMAL(18, 2),
    currency VARCHAR(3) DEFAULT 'CAD',

    -- Bénéficiaire
    recipient_type VARCHAR(50) NOT NULL,
    -- 'member', 'supplier', 'contractor', 'asset_purchase'

    recipient_member_id UUID REFERENCES auth.users(id),
    recipient_external_name VARCHAR(255),
    recipient_hedera_account VARCHAR(100),
    recipient_bank_info JSONB, -- Crypté

    -- Justification
    description TEXT NOT NULL,
    invoice_reference VARCHAR(100),
    attachments JSONB DEFAULT '[]',

    -- Approbation
    status VARCHAR(50) DEFAULT 'pending',
    -- 'pending', 'approved', 'executed', 'rejected', 'cancelled'

    requested_by UUID NOT NULL REFERENCES auth.users(id),
    approved_by UUID REFERENCES auth.users(id),
    approval_date TIMESTAMPTZ,

    -- Exécution
    executed_at TIMESTAMPTZ,
    transaction_hash VARCHAR(255), -- Hash Hedera si UR
    bank_reference VARCHAR(100), -- Référence bancaire si fiat

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 5: FONCTIONS DE MATCHING ET SUGGESTIONS
-- ============================================================================

-- Calculer le score de matching entre un membre et un rôle
CREATE OR REPLACE FUNCTION calculate_role_match(
    p_member_id UUID,
    p_role_id UUID
)
RETURNS JSONB AS $$
DECLARE
    v_role arche_roles%ROWTYPE;
    v_member_resonance DECIMAL;
    v_skills_match DECIMAL := 0;
    v_skills_required INTEGER := 0;
    v_skills_matched INTEGER := 0;
    v_skill JSONB;
    v_member_skill RECORD;
    v_final_score DECIMAL;
BEGIN
    -- Récupérer le rôle
    SELECT * INTO v_role FROM arche_roles WHERE id = p_role_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('error', 'Role not found');
    END IF;

    -- Score de résonance du membre
    SELECT resonance_score INTO v_member_resonance
    FROM member_balances WHERE user_id = p_member_id;

    IF v_member_resonance IS NULL THEN
        v_member_resonance := 0;
    END IF;

    -- Calculer le match de compétences
    FOR v_skill IN SELECT * FROM jsonb_array_elements(v_role.required_skills)
    LOOP
        v_skills_required := v_skills_required + 1;

        SELECT ms.* INTO v_member_skill
        FROM member_skills ms
        JOIN skill_definitions sd ON ms.skill_id = sd.id
        WHERE ms.member_id = p_member_id
          AND sd.code = v_skill->>'skill';

        IF FOUND THEN
            -- Vérifier le niveau
            IF (v_member_skill.level::TEXT >= (v_skill->>'level')::TEXT) THEN
                v_skills_matched := v_skills_matched + 1;
            ELSE
                v_skills_matched := v_skills_matched + 0.5; -- Partial match
            END IF;
        END IF;
    END LOOP;

    IF v_skills_required > 0 THEN
        v_skills_match := (v_skills_matched::DECIMAL / v_skills_required) * 100;
    ELSE
        v_skills_match := 100; -- Pas de compétences requises
    END IF;

    -- Score de résonance match
    DECLARE
        v_resonance_match DECIMAL;
    BEGIN
        IF v_role.min_resonance_score > 0 THEN
            v_resonance_match := LEAST((v_member_resonance / v_role.min_resonance_score) * 100, 100);
        ELSE
            v_resonance_match := 100;
        END IF;

        -- Score final pondéré
        v_final_score := (v_skills_match * 0.6) + (v_resonance_match * 0.4);

        RETURN jsonb_build_object(
            'member_id', p_member_id,
            'role_id', p_role_id,
            'final_score', ROUND(v_final_score, 2),
            'breakdown', jsonb_build_object(
                'skills_match', ROUND(v_skills_match, 2),
                'resonance_match', ROUND(v_resonance_match, 2),
                'skills_required', v_skills_required,
                'skills_matched', v_skills_matched
            ),
            'meets_minimum', (v_member_resonance >= v_role.min_resonance_score),
            'skill_gaps', (
                SELECT COALESCE(jsonb_agg(skill->>'skill'), '[]'::JSONB)
                FROM jsonb_array_elements(v_role.required_skills) skill
                WHERE NOT EXISTS (
                    SELECT 1 FROM member_skills ms
                    JOIN skill_definitions sd ON ms.skill_id = sd.id
                    WHERE ms.member_id = p_member_id
                      AND sd.code = skill->>'skill'
                )
            )
        );
    END;
END;
$$ LANGUAGE plpgsql;

-- Générer des suggestions de rôles pour un membre
CREATE OR REPLACE FUNCTION generate_role_suggestions(p_member_id UUID)
RETURNS SETOF role_suggestions AS $$
DECLARE
    v_role RECORD;
    v_match JSONB;
    v_suggestion role_suggestions;
BEGIN
    -- Pour chaque rôle actif avec des places disponibles
    FOR v_role IN
        SELECT * FROM arche_roles
        WHERE is_active = TRUE
          AND current_holders < max_holders
        ORDER BY urgency_level DESC, is_critical DESC
    LOOP
        -- Calculer le match
        v_match := calculate_role_match(p_member_id, v_role.id);

        -- Si score > 50%, créer une suggestion
        IF (v_match->>'final_score')::DECIMAL >= 50 THEN
            -- Vérifier si suggestion existe déjà
            IF NOT EXISTS (
                SELECT 1 FROM role_suggestions
                WHERE member_id = p_member_id
                  AND role_id = v_role.id
                  AND created_at > NOW() - INTERVAL '30 days'
            ) THEN
                INSERT INTO role_suggestions (
                    member_id, role_id, suggestion_score,
                    reasoning, skill_gaps, development_path
                ) VALUES (
                    p_member_id,
                    v_role.id,
                    (v_match->>'final_score')::DECIMAL,
                    'Match calculé automatiquement par L4',
                    v_match->'skill_gaps',
                    '[]'::JSONB
                )
                RETURNING * INTO v_suggestion;

                RETURN NEXT v_suggestion;
            END IF;
        END IF;
    END LOOP;

    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Trouver les meilleurs candidats pour un projet
CREATE OR REPLACE FUNCTION find_project_candidates(
    p_project_id UUID,
    p_required_skills JSONB DEFAULT '[]'
)
RETURNS TABLE (
    member_id UUID,
    match_score DECIMAL,
    available_hours DECIMAL,
    resonance_score DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        mb.user_id,
        COALESCE(
            (SELECT AVG((calculate_role_match(mb.user_id, ar.id)->>'final_score')::DECIMAL)
             FROM arche_roles ar
             WHERE ar.required_skills ?| ARRAY(SELECT jsonb_array_elements_text(p_required_skills))
            ), 50.0
        ) as match_score,
        40.0 - COALESCE(
            (SELECT SUM(ptm.hours_allocated_weekly)
             FROM project_team_members ptm
             JOIN forge_projects fp ON ptm.project_id = fp.id
             WHERE ptm.member_id = mb.user_id
               AND fp.status = 'active'
            ), 0
        ) as available_hours,
        mb.resonance_score
    FROM member_balances mb
    WHERE mb.user_id NOT IN (
        SELECT member_id FROM project_team_members
        WHERE project_id = p_project_id AND status = 'active'
    )
    ORDER BY match_score DESC, resonance_score DESC
    LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTIE 6: ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE arche_roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE skill_definitions ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE role_assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE role_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE role_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE market_agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE market_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE transaction_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE forge_projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_disbursements ENABLE ROW LEVEL SECURITY;

-- Lecture publique pour rôles et compétences
CREATE POLICY read_roles ON arche_roles FOR SELECT USING (TRUE);
CREATE POLICY read_skills ON skill_definitions FOR SELECT USING (TRUE);

-- Membres voient leurs propres données
CREATE POLICY member_own_skills ON member_skills
    FOR ALL USING (member_id = auth.uid());

CREATE POLICY member_own_applications ON role_applications
    FOR ALL USING (member_id = auth.uid());

CREATE POLICY member_own_suggestions ON role_suggestions
    FOR SELECT USING (member_id = auth.uid());

-- Projets: membres de l'équipe peuvent voir
CREATE POLICY project_team_access ON forge_projects
    FOR SELECT USING (
        lead_member_id = auth.uid()
        OR EXISTS (
            SELECT 1 FROM project_team_members
            WHERE project_id = id AND member_id = auth.uid()
        )
        OR EXISTS (
            SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign')
        )
    );

CREATE POLICY project_messages_team ON project_messages
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM project_team_members
            WHERE project_id = project_messages.project_id AND member_id = auth.uid()
        )
        OR EXISTS (
            SELECT 1 FROM forge_projects
            WHERE id = project_messages.project_id AND lead_member_id = auth.uid()
        )
    );

-- Admin accès complet
CREATE POLICY admin_all_roles ON arche_roles
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign'))
    );

CREATE POLICY admin_all_projects ON forge_projects
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign'))
    );

CREATE POLICY admin_market_agents ON market_agents
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign'))
    );

CREATE POLICY admin_market_reports ON market_reports
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign'))
    );

-- ============================================================================
-- PARTIE 7: DONNÉES INITIALES
-- ============================================================================

-- Compétences de base
INSERT INTO skill_definitions (code, name, category, description) VALUES
    -- Technique
    ('dev_frontend', 'Développement Frontend', 'technology', 'React, Vue, Angular, HTML/CSS'),
    ('dev_backend', 'Développement Backend', 'technology', 'Node.js, Python, Go, APIs'),
    ('dev_blockchain', 'Développement Blockchain', 'technology', 'Hedera, Solidity, Web3'),
    ('devops', 'DevOps & Infrastructure', 'technology', 'Docker, K8s, CI/CD, Cloud'),
    ('security', 'Cybersécurité', 'technology', 'Audit, Pentesting, Conformité'),
    ('ai_ml', 'Intelligence Artificielle', 'technology', 'ML, NLP, Vision, LLMs'),

    -- Finance/Légal
    ('accounting', 'Comptabilité', 'legal_finance', 'Tenue de livres, États financiers'),
    ('legal_corporate', 'Droit Corporatif', 'legal_finance', 'Incorporation, Contrats'),
    ('legal_ip', 'Propriété Intellectuelle', 'legal_finance', 'Brevets, Marques, Droits'),
    ('investment', 'Investissement', 'legal_finance', 'Analyse financière, Portefeuilles'),
    ('tax', 'Fiscalité', 'legal_finance', 'Optimisation fiscale, Conformité'),

    -- Opérations
    ('project_mgmt', 'Gestion de Projet', 'operations', 'Agile, Scrum, Planification'),
    ('hr_management', 'Ressources Humaines', 'human_relations', 'Recrutement, Formation'),
    ('customer_support', 'Support Client', 'human_relations', 'Assistance, Résolution'),
    ('real_estate', 'Immobilier', 'market_research', 'Acquisition, Évaluation'),
    ('market_analysis', 'Analyse de Marché', 'market_research', 'Études, Tendances'),

    -- Communication
    ('content_creation', 'Création de Contenu', 'communication', 'Rédaction, Vidéo, Design'),
    ('community_mgmt', 'Gestion Communauté', 'communication', 'Modération, Engagement'),
    ('public_relations', 'Relations Publiques', 'communication', 'Média, Communication'),

    -- Terrain
    ('construction', 'Construction', 'field_ops', 'Bâtiment, Rénovation'),
    ('agriculture', 'Agriculture', 'field_ops', 'Permaculture, Élevage'),
    ('energy_systems', 'Systèmes Énergétiques', 'field_ops', 'Solaire, Éolien, Batteries')
ON CONFLICT (code) DO NOTHING;

-- Rôles clés de l'Arche
INSERT INTO arche_roles (code, title, category, description, required_skills, min_resonance_score, is_critical, urgency_level) VALUES
    -- Gardiens de la Grid
    ('GUARDIAN_INFRA', 'Gardien de l''Infrastructure', 'operations',
     'Assure la stabilité des serveurs, bases de données et réseau Hedera. Monitoring 24/7 et réponse aux incidents.',
     '[{"skill": "devops", "level": "advanced"}, {"skill": "security", "level": "intermediate"}]',
     50.00, TRUE, 9),

    ('GUARDIAN_SECURITY', 'Gardien de la Sécurité', 'operations',
     'Audite et renforce la sécurité de tous les systèmes. Veille aux menaces et coordonne les réponses.',
     '[{"skill": "security", "level": "expert"}, {"skill": "devops", "level": "intermediate"}]',
     60.00, TRUE, 10),

    -- Architectes de Transition
    ('ARCHITECT_LEGAL', 'Architecte Juridique', 'legal_finance',
     'Gère les dossiers de brevets, la structure légale et la conformité réglementaire.',
     '[{"skill": "legal_corporate", "level": "advanced"}, {"skill": "legal_ip", "level": "intermediate"}]',
     40.00, TRUE, 8),

    ('ARCHITECT_FINANCE', 'Architecte Financier', 'legal_finance',
     'Pilote l''exfiltration des fonds, optimise le rendement et gère les conversions UR/Fiat.',
     '[{"skill": "investment", "level": "advanced"}, {"skill": "accounting", "level": "intermediate"}]',
     50.00, TRUE, 9),

    -- Médiateurs de Résonance
    ('MEDIATOR_ONBOARD', 'Médiateur d''Intégration', 'human_relations',
     'Accueille les nouveaux membres, les guide dans le tri de leur passé et leur intégration.',
     '[{"skill": "hr_management", "level": "intermediate"}, {"skill": "customer_support", "level": "intermediate"}]',
     30.00, FALSE, 7),

    ('MEDIATOR_SUPPORT', 'Médiateur de Support', 'human_relations',
     'Aide les membres avec leurs questions et problèmes quotidiens. Premier point de contact.',
     '[{"skill": "customer_support", "level": "advanced"}]',
     20.00, FALSE, 6),

    -- Explorateurs d'Actifs
    ('EXPLORER_LAND', 'Explorateur Foncier', 'market_research',
     'Source et analyse les opportunités de terrains au Québec pour le projet camping.',
     '[{"skill": "real_estate", "level": "advanced"}, {"skill": "market_analysis", "level": "intermediate"}]',
     40.00, FALSE, 8),

    ('EXPLORER_TECH', 'Explorateur Technologique', 'market_research',
     'Surveille les brevets concurrents et identifie les technologies à acquérir ou développer.',
     '[{"skill": "market_analysis", "level": "advanced"}, {"skill": "ai_ml", "level": "intermediate"}]',
     50.00, FALSE, 7),

    -- Développement
    ('DEV_LEAD', 'Lead Développeur', 'technology',
     'Coordonne l''équipe de développement et architeure les solutions techniques.',
     '[{"skill": "dev_backend", "level": "expert"}, {"skill": "dev_frontend", "level": "advanced"}]',
     60.00, TRUE, 9),

    ('DEV_BLOCKCHAIN', 'Développeur Blockchain', 'technology',
     'Implémente les smart contracts et intégrations Hedera.',
     '[{"skill": "dev_blockchain", "level": "advanced"}, {"skill": "dev_backend", "level": "intermediate"}]',
     50.00, TRUE, 8),

    ('DEV_AI', 'Développeur IA', 'technology',
     'Développe et entraîne les agents L4 et systèmes d''intelligence artificielle.',
     '[{"skill": "ai_ml", "level": "advanced"}, {"skill": "dev_backend", "level": "intermediate"}]',
     50.00, TRUE, 8)
ON CONFLICT (code) DO NOTHING;

-- Agents de marché initiaux
INSERT INTO market_agents (agent_type, name, description, scan_frequency_hours, geographic_focus, keywords) VALUES
    ('oracle_financier', 'Oracle Financier Alpha',
     'Surveille les marchés financiers canadiens et américains pour identifier les opportunités d''arbitrage et les signaux de risque.',
     1,
     '["canada", "usa", "global"]',
     '["interest rates", "inflation", "bank stocks", "market volatility", "CAD/USD"]'),

    ('detecteur_foncier', 'Détecteur Foncier Québec',
     'Analyse les ventes de terrains au Québec, particulièrement les régions avec accès VTT/motoneige et valeur écologique.',
     24,
     '["quebec", "lac-saint-jean", "laurentides", "charlevoix"]',
     '["terrain à vendre", "camping", "glamping", "bord de lac", "forêt", "sentiers"]'),

    ('veille_tech', 'Veille Technologique',
     'Surveille les dépôts de brevets et publications scientifiques dans nos domaines d''innovation.',
     168,
     '["global"]',
     '["quantum computing", "AI agents", "blockchain", "renewable energy", "light therapy"]'),

    ('analyse_concurrence', 'Analyseur Concurrentiel',
     'Surveille les concurrents potentiels et alternatives à nos solutions.',
     72,
     '["north america", "europe"]',
     '["community platform", "sovereign currency", "decentralized governance"]')
ON CONFLICT DO NOTHING;

COMMIT;
