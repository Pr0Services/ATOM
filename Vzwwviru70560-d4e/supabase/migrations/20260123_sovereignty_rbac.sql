-- ============================================================================
-- SYSTÈME DE SOUVERAINETÉ - RBAC & DUALITÉ D'ACCÈS
-- Séparation stricte Fondateurs / Collaborateurs
-- ============================================================================
-- Ce module implémente le "Filtre d'Entrée" qui sépare:
-- 1. Les Fondateurs (Souverains) - Accès complet à la Grid et aux connaissances
-- 2. Les Collaborateurs (Utilisateurs) - Accès limité aux espaces de travail
-- ============================================================================

-- ============================================================================
-- PARTIE 1: SYSTÈME DE RÔLES HIÉRARCHIQUE
-- ============================================================================

-- Niveaux de souveraineté
CREATE TYPE sovereignty_level AS ENUM (
    'GUEST',        -- Visiteur non authentifié
    'COLLABORATOR', -- Utilisateur invité (entreprise)
    'MEMBER',       -- Membre payant standard
    'FOUNDER',      -- Fondateur (accès vibrationnel)
    'GUARDIAN',     -- Gardien de la Grid
    'ARCHITECT',    -- Architecte système
    'SOVEREIGN'     -- Souverain suprême (Jonathan)
);

-- Table des niveaux d'accès avec permissions
CREATE TABLE IF NOT EXISTS sovereignty_tiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    level sovereignty_level UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,

    -- Permissions binaires
    can_access_workspace BOOLEAN DEFAULT TRUE,
    can_access_vibrational_ui BOOLEAN DEFAULT FALSE,
    can_access_sacred_knowledge BOOLEAN DEFAULT FALSE,
    can_access_economic_controls BOOLEAN DEFAULT FALSE,
    can_access_agent_l4 BOOLEAN DEFAULT FALSE,
    can_access_agent_l7 BOOLEAN DEFAULT FALSE,
    can_access_agent_l9 BOOLEAN DEFAULT FALSE,
    can_invite_collaborators BOOLEAN DEFAULT FALSE,
    can_invite_founders BOOLEAN DEFAULT FALSE,
    can_vote_governance BOOLEAN DEFAULT FALSE,
    can_modify_volant BOOLEAN DEFAULT FALSE,
    can_view_exfiltration BOOLEAN DEFAULT FALSE,
    can_execute_transactions BOOLEAN DEFAULT FALSE,

    -- Limites
    max_workspaces INTEGER DEFAULT 1,
    max_invitations_monthly INTEGER DEFAULT 0,
    storage_limit_gb INTEGER DEFAULT 5,

    -- Coût mensuel
    monthly_fee_cad DECIMAL(10, 2) DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Profil de souveraineté utilisateur
CREATE TABLE IF NOT EXISTS user_sovereignty (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Niveau actuel
    sovereignty_level sovereignty_level DEFAULT 'GUEST',

    -- Signature de résonance (hash unique du fondateur)
    resonance_signature VARCHAR(255),
    signature_verified BOOLEAN DEFAULT FALSE,
    signature_verified_at TIMESTAMPTZ,

    -- Clé de décryptage pour modules haute fréquence
    decryption_key_hash VARCHAR(255),
    key_issued_at TIMESTAMPTZ,
    key_expires_at TIMESTAMPTZ,

    -- Statut d'abonnement
    subscription_active BOOLEAN DEFAULT FALSE,
    subscription_started_at TIMESTAMPTZ,
    subscription_expires_at TIMESTAMPTZ,
    stripe_subscription_id VARCHAR(255),

    -- Invitation
    invited_by UUID REFERENCES auth.users(id),
    invitation_type VARCHAR(50), -- 'founder_direct', 'enterprise', 'public'
    invitation_code VARCHAR(100),
    invited_at TIMESTAMPTZ,

    -- Entreprise associée (pour collaborateurs)
    enterprise_id UUID,
    enterprise_role VARCHAR(100),

    -- Flags spéciaux
    is_original_founder BOOLEAN DEFAULT FALSE,
    is_beta_tester BOOLEAN DEFAULT FALSE,
    bypass_payment BOOLEAN DEFAULT FALSE, -- Pour tests

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(user_id)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_user_sovereignty_user ON user_sovereignty(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sovereignty_level ON user_sovereignty(sovereignty_level);
CREATE INDEX IF NOT EXISTS idx_user_sovereignty_enterprise ON user_sovereignty(enterprise_id);

-- ============================================================================
-- PARTIE 2: CONNAISSANCES SACRÉES (ISOLATION TOTALE)
-- ============================================================================

-- Catégories de connaissances
CREATE TYPE knowledge_category AS ENUM (
    'public',           -- Accessible à tous
    'member_only',      -- Membres payants
    'founder_sacred',   -- Fondateurs uniquement
    'guardian_archive', -- Gardiens et au-dessus
    'sovereign_vault'   -- Souverain uniquement
);

-- Bibliothèque des connaissances sacrées
CREATE TABLE IF NOT EXISTS sacred_knowledge (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    code VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    category knowledge_category NOT NULL,

    -- Contenu (peut être crypté)
    content_encrypted BYTEA, -- Contenu crypté AES-256
    content_hash VARCHAR(255), -- Hash pour vérification
    encryption_key_id UUID, -- Référence à la clé de décryptage

    -- Métadonnées
    description TEXT,
    frequency_hz INTEGER, -- Fréquence associée (444, 528, 999...)
    vibration_level INTEGER DEFAULT 1, -- 1-9

    -- Classification
    tags JSONB DEFAULT '[]',
    related_knowledge JSONB DEFAULT '[]',

    -- Accès
    min_sovereignty_level sovereignty_level DEFAULT 'founder_sacred',
    requires_resonance_check BOOLEAN DEFAULT FALSE,
    access_count INTEGER DEFAULT 0,

    -- Audit
    created_by UUID REFERENCES auth.users(id),
    last_accessed_at TIMESTAMPTZ,
    last_accessed_by UUID REFERENCES auth.users(id),

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_sacred_knowledge_category ON sacred_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_sacred_knowledge_level ON sacred_knowledge(min_sovereignty_level);

-- Journal d'accès aux connaissances (audit immuable)
CREATE TABLE IF NOT EXISTS knowledge_access_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES auth.users(id),
    knowledge_id UUID NOT NULL REFERENCES sacred_knowledge(id),

    -- Contexte
    access_granted BOOLEAN NOT NULL,
    denial_reason TEXT,

    -- Empreinte
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),

    -- Timestamp immuable
    accessed_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Index pour audit
CREATE INDEX IF NOT EXISTS idx_knowledge_access_user ON knowledge_access_log(user_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_access_time ON knowledge_access_log(accessed_at DESC);

-- ============================================================================
-- PARTIE 3: ESPACES DE TRAVAIL ENTREPRISE
-- ============================================================================

-- Entreprises/Organisations
CREATE TABLE IF NOT EXISTS enterprises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,

    -- Propriétaire (doit être Fondateur minimum)
    owner_id UUID NOT NULL REFERENCES auth.users(id),

    -- Configuration
    logo_url TEXT,
    primary_color VARCHAR(7) DEFAULT '#D4AF37',
    custom_domain VARCHAR(255),

    -- Limites
    max_collaborators INTEGER DEFAULT 10,
    current_collaborators INTEGER DEFAULT 0,
    storage_used_gb DECIMAL(10, 2) DEFAULT 0,
    storage_limit_gb INTEGER DEFAULT 50,

    -- Abonnement entreprise
    subscription_tier VARCHAR(50) DEFAULT 'starter',
    monthly_fee_cad DECIMAL(10, 2) DEFAULT 0,
    subscription_active BOOLEAN DEFAULT FALSE,

    -- Flags
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Espaces de travail
CREATE TABLE IF NOT EXISTS workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Rattachement
    enterprise_id UUID REFERENCES enterprises(id) ON DELETE CASCADE,
    owner_id UUID NOT NULL REFERENCES auth.users(id),

    -- Identification
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,

    -- Configuration
    is_private BOOLEAN DEFAULT TRUE,
    requires_invitation BOOLEAN DEFAULT TRUE,

    -- Visibilité des insights L7+ (seulement pour fondateurs)
    show_ai_insights BOOLEAN DEFAULT TRUE, -- Fondateurs voient les insights
    ai_insights_visible_to_collaborators BOOLEAN DEFAULT FALSE,

    -- Limites
    max_members INTEGER DEFAULT 20,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(enterprise_id, slug)
);

-- Membres des espaces de travail
CREATE TABLE IF NOT EXISTS workspace_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id),

    -- Rôle dans l'espace
    role VARCHAR(50) DEFAULT 'member',
    -- 'owner', 'admin', 'member', 'viewer'

    -- Permissions spécifiques à l'espace
    can_invite BOOLEAN DEFAULT FALSE,
    can_edit_settings BOOLEAN DEFAULT FALSE,
    can_delete_content BOOLEAN DEFAULT FALSE,

    -- Timestamps
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    last_active_at TIMESTAMPTZ,

    UNIQUE(workspace_id, user_id)
);

-- ============================================================================
-- PARTIE 4: TUNNELS D'INVITATION
-- ============================================================================

-- Types d'invitation
CREATE TYPE invitation_tunnel AS ENUM (
    'founder_accreditation', -- Tunnel Fondateur (99$ + signature)
    'enterprise_invite',      -- Invitation entreprise
    'collaborator_direct',    -- Invitation directe collaborateur
    'public_waitlist'         -- Liste d'attente publique
);

-- Codes d'invitation
CREATE TABLE IF NOT EXISTS invitation_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Code unique
    code VARCHAR(50) UNIQUE NOT NULL,
    tunnel invitation_tunnel NOT NULL,

    -- Créateur
    created_by UUID NOT NULL REFERENCES auth.users(id),

    -- Cible (optionnel)
    target_email VARCHAR(255),
    target_enterprise_id UUID REFERENCES enterprises(id),
    target_workspace_id UUID REFERENCES workspaces(id),

    -- Configuration
    max_uses INTEGER DEFAULT 1,
    current_uses INTEGER DEFAULT 0,
    expires_at TIMESTAMPTZ,

    -- Niveau accordé à l'utilisation
    grants_level sovereignty_level DEFAULT 'COLLABORATOR',

    -- Statut
    is_active BOOLEAN DEFAULT TRUE,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    used_at TIMESTAMPTZ
);

-- Historique des invitations
CREATE TABLE IF NOT EXISTS invitation_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code_id UUID NOT NULL REFERENCES invitation_codes(id),
    user_id UUID NOT NULL REFERENCES auth.users(id),

    -- Résultat
    success BOOLEAN NOT NULL,
    failure_reason TEXT,

    -- Contexte
    ip_address INET,
    user_agent TEXT,

    -- Timestamp
    processed_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 5: FONCTIONS DE VÉRIFICATION DE SOUVERAINETÉ
-- ============================================================================

-- Vérifier le niveau de souveraineté d'un utilisateur
CREATE OR REPLACE FUNCTION check_sovereignty(p_user_id UUID)
RETURNS sovereignty_level AS $$
DECLARE
    v_level sovereignty_level;
BEGIN
    SELECT sovereignty_level INTO v_level
    FROM user_sovereignty
    WHERE user_id = p_user_id
      AND (subscription_active = TRUE OR sovereignty_level IN ('GUEST', 'COLLABORATOR'));

    IF NOT FOUND THEN
        RETURN 'GUEST';
    END IF;

    RETURN v_level;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Vérifier si un utilisateur peut accéder à une ressource
CREATE OR REPLACE FUNCTION can_access_resource(
    p_user_id UUID,
    p_resource_type VARCHAR(50),
    p_resource_id UUID DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    v_level sovereignty_level;
    v_tier sovereignty_tiers%ROWTYPE;
    v_can_access BOOLEAN := FALSE;
    v_reason TEXT := '';
BEGIN
    -- Obtenir le niveau
    v_level := check_sovereignty(p_user_id);

    -- Obtenir les permissions du tier
    SELECT * INTO v_tier FROM sovereignty_tiers WHERE level = v_level;

    -- Vérifier selon le type de ressource
    CASE p_resource_type
        WHEN 'vibrational_ui' THEN
            v_can_access := v_tier.can_access_vibrational_ui;
            v_reason := CASE WHEN NOT v_can_access THEN 'Niveau Fondateur requis pour l''interface vibrationnelle' ELSE '' END;

        WHEN 'sacred_knowledge' THEN
            v_can_access := v_tier.can_access_sacred_knowledge;
            v_reason := CASE WHEN NOT v_can_access THEN 'Accès réservé aux Fondateurs' ELSE '' END;

        WHEN 'economic_controls' THEN
            v_can_access := v_tier.can_access_economic_controls;
            v_reason := CASE WHEN NOT v_can_access THEN 'Niveau Gardien requis' ELSE '' END;

        WHEN 'agent_l4' THEN
            v_can_access := v_tier.can_access_agent_l4;

        WHEN 'agent_l7' THEN
            v_can_access := v_tier.can_access_agent_l7;
            v_reason := CASE WHEN NOT v_can_access THEN 'Agent L7 réservé aux Fondateurs' ELSE '' END;

        WHEN 'agent_l9' THEN
            v_can_access := v_tier.can_access_agent_l9;
            v_reason := CASE WHEN NOT v_can_access THEN 'Agent L9 réservé aux Gardiens' ELSE '' END;

        WHEN 'exfiltration' THEN
            v_can_access := v_tier.can_view_exfiltration;
            v_reason := CASE WHEN NOT v_can_access THEN 'Dashboard d''exfiltration réservé aux Architectes' ELSE '' END;

        WHEN 'governance_vote' THEN
            v_can_access := v_tier.can_vote_governance;

        WHEN 'workspace' THEN
            -- Vérifier l'appartenance à l'espace de travail
            IF p_resource_id IS NOT NULL THEN
                SELECT EXISTS(
                    SELECT 1 FROM workspace_members
                    WHERE workspace_id = p_resource_id AND user_id = p_user_id
                ) INTO v_can_access;
                v_reason := CASE WHEN NOT v_can_access THEN 'Non membre de cet espace de travail' ELSE '' END;
            ELSE
                v_can_access := v_tier.can_access_workspace;
            END IF;

        ELSE
            v_can_access := FALSE;
            v_reason := 'Type de ressource inconnu';
    END CASE;

    RETURN jsonb_build_object(
        'user_id', p_user_id,
        'sovereignty_level', v_level,
        'resource_type', p_resource_type,
        'can_access', v_can_access,
        'reason', v_reason
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Promouvoir un utilisateur au niveau Fondateur
CREATE OR REPLACE FUNCTION promote_to_founder(
    p_user_id UUID,
    p_invitation_code VARCHAR(50),
    p_resonance_signature VARCHAR(255),
    p_stripe_subscription_id VARCHAR(255) DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    v_code invitation_codes%ROWTYPE;
    v_decryption_key VARCHAR(255);
BEGIN
    -- Vérifier le code d'invitation
    SELECT * INTO v_code
    FROM invitation_codes
    WHERE code = p_invitation_code
      AND tunnel = 'founder_accreditation'
      AND is_active = TRUE
      AND (expires_at IS NULL OR expires_at > NOW())
      AND (max_uses IS NULL OR current_uses < max_uses);

    IF NOT FOUND THEN
        RETURN jsonb_build_object(
            'success', FALSE,
            'error', 'Code d''invitation invalide ou expiré'
        );
    END IF;

    -- Générer la clé de décryptage
    v_decryption_key := encode(gen_random_bytes(32), 'hex');

    -- Mettre à jour ou créer le profil de souveraineté
    INSERT INTO user_sovereignty (
        user_id, sovereignty_level, resonance_signature, signature_verified,
        signature_verified_at, decryption_key_hash, key_issued_at, key_expires_at,
        subscription_active, subscription_started_at, stripe_subscription_id,
        invited_by, invitation_type, invitation_code, invited_at
    ) VALUES (
        p_user_id, 'FOUNDER', p_resonance_signature, TRUE,
        NOW(), crypt(v_decryption_key, gen_salt('bf')), NOW(), NOW() + INTERVAL '1 year',
        TRUE, NOW(), p_stripe_subscription_id,
        v_code.created_by, 'founder_direct', p_invitation_code, NOW()
    )
    ON CONFLICT (user_id) DO UPDATE SET
        sovereignty_level = 'FOUNDER',
        resonance_signature = p_resonance_signature,
        signature_verified = TRUE,
        signature_verified_at = NOW(),
        decryption_key_hash = crypt(v_decryption_key, gen_salt('bf')),
        key_issued_at = NOW(),
        key_expires_at = NOW() + INTERVAL '1 year',
        subscription_active = TRUE,
        subscription_started_at = NOW(),
        stripe_subscription_id = p_stripe_subscription_id,
        updated_at = NOW();

    -- Incrémenter l'utilisation du code
    UPDATE invitation_codes
    SET current_uses = current_uses + 1,
        used_at = NOW()
    WHERE id = v_code.id;

    -- Logger
    INSERT INTO invitation_history (code_id, user_id, success)
    VALUES (v_code.id, p_user_id, TRUE);

    RETURN jsonb_build_object(
        'success', TRUE,
        'sovereignty_level', 'FOUNDER',
        'decryption_key', v_decryption_key, -- À transmettre de manière sécurisée
        'message', 'Bienvenue parmi les Fondateurs de l''Arche'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Inviter un collaborateur
CREATE OR REPLACE FUNCTION invite_collaborator(
    p_inviter_id UUID,
    p_target_email VARCHAR(255),
    p_workspace_id UUID,
    p_enterprise_id UUID DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    v_inviter_level sovereignty_level;
    v_code VARCHAR(50);
BEGIN
    -- Vérifier que l'inviteur peut inviter
    v_inviter_level := check_sovereignty(p_inviter_id);

    IF v_inviter_level NOT IN ('FOUNDER', 'GUARDIAN', 'ARCHITECT', 'SOVEREIGN') THEN
        RETURN jsonb_build_object(
            'success', FALSE,
            'error', 'Seuls les Fondateurs peuvent inviter des collaborateurs'
        );
    END IF;

    -- Vérifier que l'inviteur est membre du workspace
    IF NOT EXISTS (
        SELECT 1 FROM workspace_members
        WHERE workspace_id = p_workspace_id
          AND user_id = p_inviter_id
          AND role IN ('owner', 'admin')
    ) THEN
        RETURN jsonb_build_object(
            'success', FALSE,
            'error', 'Vous devez être admin de cet espace de travail'
        );
    END IF;

    -- Générer le code
    v_code := 'COLLAB-' || encode(gen_random_bytes(8), 'hex');

    -- Créer l'invitation
    INSERT INTO invitation_codes (
        code, tunnel, created_by, target_email,
        target_enterprise_id, target_workspace_id,
        max_uses, expires_at, grants_level
    ) VALUES (
        v_code, 'collaborator_direct', p_inviter_id, p_target_email,
        p_enterprise_id, p_workspace_id,
        1, NOW() + INTERVAL '7 days', 'COLLABORATOR'
    );

    RETURN jsonb_build_object(
        'success', TRUE,
        'invitation_code', v_code,
        'expires_at', NOW() + INTERVAL '7 days',
        'target_email', p_target_email
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- PARTIE 6: ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE user_sovereignty ENABLE ROW LEVEL SECURITY;
ALTER TABLE sacred_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_access_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE enterprises ENABLE ROW LEVEL SECURITY;
ALTER TABLE workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE workspace_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE invitation_codes ENABLE ROW LEVEL SECURITY;

-- Utilisateurs voient leur propre souveraineté
CREATE POLICY own_sovereignty ON user_sovereignty
    FOR SELECT USING (user_id = auth.uid());

-- Admins voient tout
CREATE POLICY admin_sovereignty ON user_sovereignty
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM user_sovereignty
            WHERE user_id = auth.uid()
              AND sovereignty_level IN ('ARCHITECT', 'SOVEREIGN')
        )
    );

-- Connaissances sacrées: accès selon niveau
CREATE POLICY sacred_knowledge_access ON sacred_knowledge
    FOR SELECT USING (
        CASE min_sovereignty_level
            WHEN 'public' THEN TRUE
            WHEN 'member_only' THEN EXISTS (
                SELECT 1 FROM user_sovereignty
                WHERE user_id = auth.uid() AND subscription_active = TRUE
            )
            WHEN 'founder_sacred' THEN EXISTS (
                SELECT 1 FROM user_sovereignty
                WHERE user_id = auth.uid()
                  AND sovereignty_level IN ('FOUNDER', 'GUARDIAN', 'ARCHITECT', 'SOVEREIGN')
            )
            WHEN 'guardian_archive' THEN EXISTS (
                SELECT 1 FROM user_sovereignty
                WHERE user_id = auth.uid()
                  AND sovereignty_level IN ('GUARDIAN', 'ARCHITECT', 'SOVEREIGN')
            )
            WHEN 'sovereign_vault' THEN EXISTS (
                SELECT 1 FROM user_sovereignty
                WHERE user_id = auth.uid()
                  AND sovereignty_level = 'SOVEREIGN'
            )
            ELSE FALSE
        END
    );

-- Espaces de travail: membres uniquement
CREATE POLICY workspace_member_access ON workspaces
    FOR SELECT USING (
        owner_id = auth.uid()
        OR EXISTS (
            SELECT 1 FROM workspace_members
            WHERE workspace_id = id AND user_id = auth.uid()
        )
    );

-- Membres workspace: voir ses propres appartenances
CREATE POLICY own_workspace_membership ON workspace_members
    FOR SELECT USING (user_id = auth.uid());

-- Codes d'invitation: créateur uniquement
CREATE POLICY invitation_creator_access ON invitation_codes
    FOR ALL USING (created_by = auth.uid());

-- ============================================================================
-- PARTIE 7: DONNÉES INITIALES
-- ============================================================================

-- Niveaux de souveraineté avec permissions
INSERT INTO sovereignty_tiers (
    level, display_name, description,
    can_access_workspace, can_access_vibrational_ui, can_access_sacred_knowledge,
    can_access_economic_controls, can_access_agent_l4, can_access_agent_l7, can_access_agent_l9,
    can_invite_collaborators, can_invite_founders, can_vote_governance,
    can_modify_volant, can_view_exfiltration, can_execute_transactions,
    max_workspaces, max_invitations_monthly, storage_limit_gb, monthly_fee_cad
) VALUES
    ('GUEST', 'Visiteur', 'Accès limité, en attente d''activation',
     FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE,
     0, 0, 0, 0),

    ('COLLABORATOR', 'Collaborateur', 'Membre invité d''une entreprise',
     TRUE, FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE,
     1, 0, 5, 0),

    ('MEMBER', 'Membre', 'Membre payant standard',
     TRUE, FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE,
     3, 5, 20, 29.00),

    ('FOUNDER', 'Fondateur', 'Gardien de la Grid - Accès vibrationnel complet',
     TRUE, TRUE, TRUE, FALSE, TRUE, TRUE, FALSE, TRUE, FALSE, TRUE, FALSE, FALSE, TRUE,
     10, 20, 100, 99.00),

    ('GUARDIAN', 'Gardien', 'Protecteur de l''Arche - Accès aux archives',
     TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE,
     50, 100, 500, 299.00),

    ('ARCHITECT', 'Architecte', 'Bâtisseur du système - Contrôle du Volant',
     TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE,
     -1, -1, -1, 0),

    ('SOVEREIGN', 'Souverain', 'Autorité suprême de l''Arche',
     TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE,
     -1, -1, -1, 0)
ON CONFLICT (level) DO NOTHING;

-- Connaissances sacrées initiales (exemples)
INSERT INTO sacred_knowledge (code, title, category, min_sovereignty_level, frequency_hz, vibration_level, description) VALUES
    ('PUBLIC_INTRO', 'Introduction à l''Arche', 'public', 'GUEST', 432, 1,
     'Présentation générale de la plateforme et de sa vision.'),

    ('MEMBER_ECONOMICS', 'Comprendre le Système Économique', 'member_only', 'MEMBER', 444, 2,
     'Guide détaillé sur les Unités de Résonance et le Volant Énergétique.'),

    ('FOUNDER_SECRETS', 'Les Secrets des Fréquences', 'founder_sacred', 'FOUNDER', 528, 5,
     'Connaissance approfondie des fréquences sacrées et leur application.'),

    ('FOUNDER_GRID_ACTIVATION', 'Activation de la Grid Personnelle', 'founder_sacred', 'FOUNDER', 639, 6,
     'Protocole d''activation et de synchronisation avec la Grid mondiale.'),

    ('GUARDIAN_PROTOCOLS', 'Protocoles de Protection', 'guardian_archive', 'GUARDIAN', 741, 7,
     'Procédures de sécurité et de réponse aux incidents.'),

    ('GUARDIAN_EXFILTRATION', 'Manuel d''Exfiltration Avancé', 'guardian_archive', 'GUARDIAN', 852, 8,
     'Stratégies avancées de conversion d''actifs et timing de marché.'),

    ('SOVEREIGN_GENESIS', 'Le Document Genesis', 'sovereign_vault', 'SOVEREIGN', 963, 9,
     'Document originel contenant la vision complète et les clés maîtresses.')
ON CONFLICT (code) DO NOTHING;

COMMIT;
