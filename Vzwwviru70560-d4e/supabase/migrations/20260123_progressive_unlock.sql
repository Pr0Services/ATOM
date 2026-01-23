-- ============================================================================
-- SYSTÈME DE DÉBLOCAGE PROGRESSIF PAR CONSENTEMENT
-- Progressive Unlock Engine - Respect du Libre Arbitre
-- ============================================================================
-- L'Arche propose au lieu d'imposer. Les modules avancés restent en sommeil
-- jusqu'à ce que l'utilisateur consente explicitement à leur activation.
-- ============================================================================

-- ============================================================================
-- PARTIE 1: DÉFINITION DES MODULES DÉBLOCABLES
-- ============================================================================

-- Catégories de modules
CREATE TYPE module_category AS ENUM (
    'productivity',      -- Outils de productivité
    'communication',     -- Communication avancée
    'analytics',         -- Analyses et rapports
    'automation',        -- Automatisation
    'integration',       -- Intégrations externes
    'vibrational',       -- Modules vibrationnels (Fondateurs)
    'economic',          -- Outils économiques
    'governance'         -- Gouvernance et vote
);

-- Niveau de complexité
CREATE TYPE complexity_level AS ENUM (
    'simple',      -- Interface minimale
    'moderate',    -- Quelques options
    'advanced',    -- Configuration détaillée
    'expert'       -- Contrôle total
);

-- Catalogue des modules déblocables
CREATE TABLE IF NOT EXISTS unlockable_modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    code VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    category module_category NOT NULL,

    -- Description
    description TEXT NOT NULL,
    description_en TEXT,
    value_proposition TEXT, -- "Cela libérera 15% de votre charge cognitive"

    -- Tutoriel
    tutorial_video_url TEXT,
    tutorial_gif_url TEXT,
    tutorial_steps JSONB DEFAULT '[]', -- [{step: 1, title: "", description: "", image_url: ""}]

    -- Prérequis
    min_sovereignty_level sovereignty_level DEFAULT 'MEMBER',
    requires_modules JSONB DEFAULT '[]', -- Modules prérequis
    complexity complexity_level DEFAULT 'simple',

    -- Impact
    cognitive_load_reduction INTEGER DEFAULT 0, -- % de réduction charge cognitive
    energy_impact VARCHAR(50) DEFAULT 'low', -- 'low', 'medium', 'high'
    api_permissions_required JSONB DEFAULT '[]', -- Permissions API nécessaires

    -- État par défaut
    default_locked BOOLEAN DEFAULT TRUE,
    auto_suggest BOOLEAN DEFAULT TRUE, -- L'agent peut suggérer ce module

    -- Fréquence associée (pour modules vibrationnels)
    frequency_hz INTEGER,

    -- Double langage Nova (Pragmatique / Fréquentiel)
    explanation_pragmatic TEXT, -- Explication rationnelle/business
    explanation_frequential TEXT, -- Explication vibratoire/souveraine

    -- Ordre d'affichage
    display_order INTEGER DEFAULT 100,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_modules_category ON unlockable_modules(category);
CREATE INDEX IF NOT EXISTS idx_modules_sovereignty ON unlockable_modules(min_sovereignty_level);

-- ============================================================================
-- PARTIE 2: ÉTAT DE DÉBLOCAGE PAR UTILISATEUR
-- ============================================================================

-- État d'un module pour un utilisateur
CREATE TYPE module_state AS ENUM (
    'locked',           -- Verrouillé (défaut)
    'suggested',        -- Suggéré par L4, en attente de décision
    'unlocked',         -- Débloqué et actif
    'dismissed',        -- Refusé par l'utilisateur
    'tutorial_pending', -- Débloqué, tutoriel en cours
    'disabled'          -- Désactivé après déblocage
);

-- Modules de l'utilisateur
CREATE TABLE IF NOT EXISTS user_modules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    module_id UUID NOT NULL REFERENCES unlockable_modules(id),

    -- État actuel
    state module_state DEFAULT 'locked',

    -- Historique des états
    state_history JSONB DEFAULT '[]',
    -- [{state: "suggested", at: timestamp, reason: "..."}]

    -- Suggestion
    suggested_at TIMESTAMPTZ,
    suggestion_reason TEXT,
    suggestion_dismissed_at TIMESTAMPTZ,
    dismiss_reason VARCHAR(255),

    -- Déblocage
    unlocked_at TIMESTAMPTZ,
    unlock_method VARCHAR(50), -- 'user_request', 'suggestion_accept', 'auto'

    -- Tutoriel
    tutorial_started_at TIMESTAMPTZ,
    tutorial_completed_at TIMESTAMPTZ,
    tutorial_step_current INTEGER DEFAULT 0,

    -- Utilisation
    last_used_at TIMESTAMPTZ,
    usage_count INTEGER DEFAULT 0,

    -- Préférences
    is_favorite BOOLEAN DEFAULT FALSE,
    custom_settings JSONB DEFAULT '{}',

    -- Ne plus suggérer
    do_not_suggest BOOLEAN DEFAULT FALSE,
    do_not_suggest_until TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(user_id, module_id)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_user_modules_user ON user_modules(user_id);
CREATE INDEX IF NOT EXISTS idx_user_modules_state ON user_modules(state);

-- ============================================================================
-- PARTIE 3: SUGGESTIONS DE L'AGENT L4
-- ============================================================================

-- Déclencheurs de suggestion
CREATE TYPE suggestion_trigger AS ENUM (
    'activity_pattern',   -- Comportement détecté
    'milestone_reached',  -- Jalon atteint
    'time_based',         -- Après X jours d'utilisation
    'manual_request',     -- Demande utilisateur
    'related_unlock',     -- Déblocage d'un module lié
    'onboarding'          -- Processus d'intégration
);

-- File des suggestions en attente
CREATE TABLE IF NOT EXISTS module_suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    module_id UUID NOT NULL REFERENCES unlockable_modules(id),

    -- Déclencheur
    trigger_type suggestion_trigger NOT NULL,
    trigger_data JSONB DEFAULT '{}',
    -- {pattern: "contacts_accumulation", count: 47, threshold: 30}

    -- Message personnalisé
    observation_text TEXT NOT NULL, -- "Je remarque que vous structurez..."
    proposition_text TEXT NOT NULL, -- "Souhaitez-vous activer..."

    -- Score de pertinence (0-100)
    relevance_score INTEGER DEFAULT 50,

    -- Priorité
    priority INTEGER DEFAULT 5, -- 1-10

    -- État
    status VARCHAR(50) DEFAULT 'pending',
    -- 'pending', 'shown', 'accepted', 'dismissed', 'expired'

    -- Affichage
    shown_at TIMESTAMPTZ,
    show_count INTEGER DEFAULT 0,
    max_shows INTEGER DEFAULT 3,

    -- Réponse
    responded_at TIMESTAMPTZ,
    response VARCHAR(50), -- 'accept', 'dismiss', 'later'
    response_feedback TEXT,

    -- Expiration
    expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '7 days',

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_suggestions_user ON module_suggestions(user_id);
CREATE INDEX IF NOT EXISTS idx_suggestions_status ON module_suggestions(status);
CREATE INDEX IF NOT EXISTS idx_suggestions_priority ON module_suggestions(priority DESC);

-- ============================================================================
-- PARTIE 4: PRÉFÉRENCES UTILISATEUR
-- ============================================================================

-- Préférences de suggestion
CREATE TABLE IF NOT EXISTS user_suggestion_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Fréquence des suggestions
    suggestion_frequency VARCHAR(50) DEFAULT 'moderate',
    -- 'off', 'minimal', 'moderate', 'proactive'

    -- Moments préférés
    preferred_suggestion_times JSONB DEFAULT '["10:00", "14:00"]',

    -- Catégories ignorées
    ignored_categories JSONB DEFAULT '[]',

    -- Modules ignorés définitivement
    permanently_ignored_modules JSONB DEFAULT '[]',

    -- Niveau de complexité maximum accepté
    max_complexity complexity_level DEFAULT 'moderate',

    -- Préférence d'interface
    prefer_simple_interface BOOLEAN DEFAULT TRUE,
    animation_enabled BOOLEAN DEFAULT TRUE,

    -- Son
    suggestion_sound_enabled BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 5: FONCTIONS DE GESTION
-- ============================================================================

-- Créer une suggestion pour un utilisateur
CREATE OR REPLACE FUNCTION create_module_suggestion(
    p_user_id UUID,
    p_module_code VARCHAR(100),
    p_trigger_type suggestion_trigger,
    p_observation TEXT,
    p_trigger_data JSONB DEFAULT '{}'
)
RETURNS UUID AS $$
DECLARE
    v_module unlockable_modules%ROWTYPE;
    v_user_module user_modules%ROWTYPE;
    v_suggestion_id UUID;
    v_relevance INTEGER;
BEGIN
    -- Récupérer le module
    SELECT * INTO v_module FROM unlockable_modules WHERE code = p_module_code;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Module % non trouvé', p_module_code;
    END IF;

    -- Vérifier si déjà débloqué ou ignoré
    SELECT * INTO v_user_module
    FROM user_modules
    WHERE user_id = p_user_id AND module_id = v_module.id;

    IF FOUND AND v_user_module.state IN ('unlocked', 'dismissed') THEN
        RETURN NULL; -- Ne pas suggérer
    END IF;

    IF FOUND AND v_user_module.do_not_suggest THEN
        RETURN NULL;
    END IF;

    -- Vérifier les préférences utilisateur
    IF EXISTS (
        SELECT 1 FROM user_suggestion_preferences
        WHERE user_id = p_user_id
          AND (
            suggestion_frequency = 'off'
            OR v_module.category::TEXT = ANY(SELECT jsonb_array_elements_text(ignored_categories))
            OR v_module.id::TEXT = ANY(SELECT jsonb_array_elements_text(permanently_ignored_modules))
          )
    ) THEN
        RETURN NULL;
    END IF;

    -- Calculer la pertinence
    v_relevance := 50;
    IF p_trigger_type = 'activity_pattern' THEN
        v_relevance := 75;
    ELSIF p_trigger_type = 'milestone_reached' THEN
        v_relevance := 85;
    END IF;

    -- Créer la suggestion
    INSERT INTO module_suggestions (
        user_id, module_id, trigger_type, trigger_data,
        observation_text, proposition_text, relevance_score
    ) VALUES (
        p_user_id,
        v_module.id,
        p_trigger_type,
        p_trigger_data,
        p_observation,
        'Souhaitez-vous activer le module ' || v_module.name || ' ?',
        v_relevance
    )
    RETURNING id INTO v_suggestion_id;

    -- Mettre à jour l'état du module utilisateur
    INSERT INTO user_modules (user_id, module_id, state, suggested_at, suggestion_reason)
    VALUES (p_user_id, v_module.id, 'suggested', NOW(), p_observation)
    ON CONFLICT (user_id, module_id) DO UPDATE SET
        state = 'suggested',
        suggested_at = NOW(),
        suggestion_reason = p_observation,
        updated_at = NOW();

    RETURN v_suggestion_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Accepter une suggestion (débloquer le module)
CREATE OR REPLACE FUNCTION accept_module_unlock(
    p_user_id UUID,
    p_suggestion_id UUID
)
RETURNS JSONB AS $$
DECLARE
    v_suggestion module_suggestions%ROWTYPE;
    v_module unlockable_modules%ROWTYPE;
BEGIN
    -- Récupérer la suggestion
    SELECT * INTO v_suggestion
    FROM module_suggestions
    WHERE id = p_suggestion_id AND user_id = p_user_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('success', FALSE, 'error', 'Suggestion non trouvée');
    END IF;

    -- Récupérer le module
    SELECT * INTO v_module FROM unlockable_modules WHERE id = v_suggestion.module_id;

    -- Mettre à jour la suggestion
    UPDATE module_suggestions
    SET status = 'accepted', responded_at = NOW(), response = 'accept'
    WHERE id = p_suggestion_id;

    -- Débloquer le module
    UPDATE user_modules
    SET state = 'tutorial_pending',
        unlocked_at = NOW(),
        unlock_method = 'suggestion_accept',
        state_history = state_history || jsonb_build_object(
            'state', 'unlocked',
            'at', NOW(),
            'method', 'suggestion_accept'
        ),
        updated_at = NOW()
    WHERE user_id = p_user_id AND module_id = v_suggestion.module_id;

    RETURN jsonb_build_object(
        'success', TRUE,
        'module_code', v_module.code,
        'module_name', v_module.name,
        'tutorial_steps', v_module.tutorial_steps,
        'message', 'Module débloqué ! Suivez le tutoriel pour commencer.'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Refuser une suggestion (garder simple)
CREATE OR REPLACE FUNCTION dismiss_module_suggestion(
    p_user_id UUID,
    p_suggestion_id UUID,
    p_reason VARCHAR(255) DEFAULT 'Pas maintenant',
    p_do_not_suggest_again BOOLEAN DEFAULT FALSE
)
RETURNS JSONB AS $$
DECLARE
    v_suggestion module_suggestions%ROWTYPE;
BEGIN
    -- Récupérer la suggestion
    SELECT * INTO v_suggestion
    FROM module_suggestions
    WHERE id = p_suggestion_id AND user_id = p_user_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('success', FALSE, 'error', 'Suggestion non trouvée');
    END IF;

    -- Mettre à jour la suggestion
    UPDATE module_suggestions
    SET status = 'dismissed',
        responded_at = NOW(),
        response = 'dismiss',
        response_feedback = p_reason
    WHERE id = p_suggestion_id;

    -- Mettre à jour le module utilisateur
    UPDATE user_modules
    SET state = 'dismissed',
        suggestion_dismissed_at = NOW(),
        dismiss_reason = p_reason,
        do_not_suggest = p_do_not_suggest_again,
        do_not_suggest_until = CASE
            WHEN p_do_not_suggest_again THEN NULL
            ELSE NOW() + INTERVAL '30 days'
        END,
        state_history = state_history || jsonb_build_object(
            'state', 'dismissed',
            'at', NOW(),
            'reason', p_reason
        ),
        updated_at = NOW()
    WHERE user_id = p_user_id AND module_id = v_suggestion.module_id;

    RETURN jsonb_build_object(
        'success', TRUE,
        'message', 'Préférence enregistrée. L''interface reste simple.'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Compléter le tutoriel
CREATE OR REPLACE FUNCTION complete_module_tutorial(
    p_user_id UUID,
    p_module_code VARCHAR(100)
)
RETURNS JSONB AS $$
DECLARE
    v_module unlockable_modules%ROWTYPE;
BEGIN
    SELECT * INTO v_module FROM unlockable_modules WHERE code = p_module_code;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('success', FALSE, 'error', 'Module non trouvé');
    END IF;

    UPDATE user_modules
    SET state = 'unlocked',
        tutorial_completed_at = NOW(),
        state_history = state_history || jsonb_build_object(
            'state', 'tutorial_completed',
            'at', NOW()
        ),
        updated_at = NOW()
    WHERE user_id = p_user_id AND module_id = v_module.id;

    RETURN jsonb_build_object(
        'success', TRUE,
        'message', 'Tutoriel complété ! Le module ' || v_module.name || ' est maintenant actif.'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Obtenir les suggestions actives pour un utilisateur
CREATE OR REPLACE FUNCTION get_active_suggestions(p_user_id UUID)
RETURNS TABLE (
    suggestion_id UUID,
    module_code VARCHAR(100),
    module_name VARCHAR(255),
    category module_category,
    observation_text TEXT,
    proposition_text TEXT,
    tutorial_gif_url TEXT,
    value_proposition TEXT,
    relevance_score INTEGER,
    priority INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        ms.id,
        um.code,
        um.name,
        um.category,
        ms.observation_text,
        ms.proposition_text,
        um.tutorial_gif_url,
        um.value_proposition,
        ms.relevance_score,
        ms.priority
    FROM module_suggestions ms
    JOIN unlockable_modules um ON ms.module_id = um.id
    WHERE ms.user_id = p_user_id
      AND ms.status = 'pending'
      AND ms.expires_at > NOW()
      AND ms.show_count < ms.max_shows
    ORDER BY ms.priority DESC, ms.relevance_score DESC
    LIMIT 3;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Obtenir les modules débloqués d'un utilisateur
CREATE OR REPLACE FUNCTION get_user_unlocked_modules(p_user_id UUID)
RETURNS TABLE (
    module_code VARCHAR(100),
    module_name VARCHAR(255),
    category module_category,
    unlocked_at TIMESTAMPTZ,
    last_used_at TIMESTAMPTZ,
    usage_count INTEGER,
    is_favorite BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        um.code,
        um.name,
        um.category,
        umod.unlocked_at,
        umod.last_used_at,
        umod.usage_count,
        umod.is_favorite
    FROM user_modules umod
    JOIN unlockable_modules um ON umod.module_id = um.id
    WHERE umod.user_id = p_user_id
      AND umod.state IN ('unlocked', 'tutorial_pending')
    ORDER BY umod.is_favorite DESC, umod.last_used_at DESC NULLS LAST;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- PARTIE 6: ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE unlockable_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE module_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_suggestion_preferences ENABLE ROW LEVEL SECURITY;

-- Modules: lecture pour tous les authentifiés
CREATE POLICY read_modules ON unlockable_modules
    FOR SELECT USING (auth.uid() IS NOT NULL);

-- User modules: propres données uniquement
CREATE POLICY own_user_modules ON user_modules
    FOR ALL USING (user_id = auth.uid());

-- Suggestions: propres données uniquement
CREATE POLICY own_suggestions ON module_suggestions
    FOR ALL USING (user_id = auth.uid());

-- Préférences: propres données uniquement
CREATE POLICY own_preferences ON user_suggestion_preferences
    FOR ALL USING (user_id = auth.uid());

-- ============================================================================
-- PARTIE 7: DONNÉES INITIALES - CATALOGUE DE MODULES
-- ============================================================================

INSERT INTO unlockable_modules (
    code, name, category, description, value_proposition,
    min_sovereignty_level, complexity, cognitive_load_reduction,
    energy_impact, tutorial_steps, frequency_hz, display_order
) VALUES
    -- Productivité
    ('alliance_mapping', 'Maillage des Alliances', 'productivity',
     'Visualisez et organisez votre réseau de contacts sous forme de carte interactive.',
     'Libère 15% de votre charge cognitive en structurant automatiquement vos relations.',
     'MEMBER', 'moderate', 15, 'low',
     '[{"step": 1, "title": "Importer vos contacts", "description": "Connectez vos sources de contacts existantes."},
       {"step": 2, "title": "Organiser par cercles", "description": "L''IA suggère des groupements naturels."},
       {"step": 3, "title": "Activer les rappels", "description": "Ne perdez plus jamais le fil d''une relation."}]',
     NULL, 10),

    ('resource_mesh', 'Maillage des Ressources', 'productivity',
     'Liez automatiquement vos projets aux ressources disponibles (contacts, fichiers, budgets).',
     'Réduit de 20% le temps de recherche d''information.',
     'MEMBER', 'advanced', 20, 'medium',
     '[{"step": 1, "title": "Scanner vos projets", "description": "L''agent analyse vos projets actifs."},
       {"step": 2, "title": "Lier les ressources", "description": "Association automatique contacts-projets."},
       {"step": 3, "title": "Tableau de bord", "description": "Vue unifiée de toutes vos ressources."}]',
     NULL, 20),

    -- Communication
    ('smart_threads', 'Fils Intelligents', 'communication',
     'Conversations qui s''organisent automatiquement par contexte et priorité.',
     'Économise 30 minutes par jour en tri de messages.',
     'MEMBER', 'simple', 25, 'low',
     '[{"step": 1, "title": "Activer le tri", "description": "L''IA classe automatiquement vos conversations."},
       {"step": 2, "title": "Personnaliser", "description": "Ajustez les règles de priorité."},
       {"step": 3, "title": "Résumés quotidiens", "description": "Recevez un digest de ce qui compte."}]',
     NULL, 30),

    -- Analytics
    ('energy_analytics', 'Analyse Énergétique', 'analytics',
     'Visualisez où va votre énergie et identifiez les fuites de productivité.',
     'Identifie les 20% d''activités qui drainent 80% de votre énergie.',
     'FOUNDER', 'moderate', 30, 'low',
     '[{"step": 1, "title": "Tracking passif", "description": "Le système observe votre activité (anonymisé)."},
       {"step": 2, "title": "Rapport hebdomadaire", "description": "Visualisez vos patterns énergétiques."},
       {"step": 3, "title": "Optimisation", "description": "Suggestions personnalisées d''amélioration."}]',
     444, 40),

    -- Automation
    ('flow_automations', 'Automatisations de Flux', 'automation',
     'Créez des règles automatiques : si X arrive, alors faire Y.',
     'Automatise les tâches répétitives qui vous font perdre 5h par semaine.',
     'MEMBER', 'advanced', 35, 'medium',
     '[{"step": 1, "title": "Choisir un déclencheur", "description": "Quand se déclenche l''automatisation ?"},
       {"step": 2, "title": "Définir l''action", "description": "Que doit faire le système ?"},
       {"step": 3, "title": "Tester et activer", "description": "Vérifiez que tout fonctionne."}]',
     NULL, 50),

    -- Vibrational (Fondateurs uniquement)
    ('frequency_tuner', 'Accordeur de Fréquence', 'vibrational',
     'Ajustez la fréquence vibratoire de votre interface selon votre état.',
     'Synchronise votre environnement digital avec votre énergie.',
     'FOUNDER', 'simple', 10, 'low',
     '[{"step": 1, "title": "Choisir une fréquence", "description": "432Hz (Terre), 444Hz (Harmonie), 528Hz (Amour)."},
       {"step": 2, "title": "Activer le son", "description": "Fond sonore optionnel."},
       {"step": 3, "title": "Observer", "description": "Notez les changements dans votre focus."}]',
     444, 100),

    ('sacred_geometry_bg', 'Géométrie Sacrée', 'vibrational',
     'Arrière-plan animé avec des formes géométriques sacrées.',
     'Élève subtilement votre état de conscience pendant le travail.',
     'FOUNDER', 'simple', 5, 'low',
     '[{"step": 1, "title": "Choisir une forme", "description": "Fleur de vie, Métatron, Sri Yantra..."},
       {"step": 2, "title": "Ajuster l''opacité", "description": "Subtil ou prononcé."},
       {"step": 3, "title": "Animation", "description": "Rotation lente ou statique."}]',
     528, 110),

    ('resonance_dashboard', 'Tableau de Résonance', 'vibrational',
     'Visualisez votre score de résonance et son évolution dans le temps.',
     'Conscience de votre contribution à la Grid collective.',
     'FOUNDER', 'moderate', 15, 'low',
     '[{"step": 1, "title": "Comprendre le score", "description": "Comment est calculée votre résonance."},
       {"step": 2, "title": "Historique", "description": "Suivez votre évolution."},
       {"step": 3, "title": "Objectifs", "description": "Fixez-vous des intentions de croissance."}]',
     963, 120),

    -- Economic
    ('ur_wallet', 'Portefeuille UR', 'economic',
     'Gérez vos Unités de Résonance : solde, transactions, conversions.',
     'Contrôle total sur votre monnaie souveraine.',
     'FOUNDER', 'moderate', 20, 'medium',
     '[{"step": 1, "title": "Votre solde", "description": "Vue en temps réel de vos UR."},
       {"step": 2, "title": "Transactions", "description": "Envoyez et recevez des UR."},
       {"step": 3, "title": "Conversion", "description": "Échangez UR ↔ CAD (bientôt)."}]',
     NULL, 200),

    -- Governance
    ('vote_governance', 'Vote de Gouvernance', 'governance',
     'Participez aux décisions collectives de l''Arche.',
     'Votre voix compte. Chaque vote façonne notre avenir commun.',
     'FOUNDER', 'simple', 10, 'low',
     '[{"step": 1, "title": "Propositions actives", "description": "Voir les votes en cours."},
       {"step": 2, "title": "Voter", "description": "Exprimez votre choix."},
       {"step": 3, "title": "Résultats", "description": "Transparence totale sur les décisions."}]',
     NULL, 300)

ON CONFLICT (code) DO NOTHING;

COMMIT;
