-- ============================================================================
-- PROTOCOLE SENTINELLE - SYSTÈME DE PAIX PAR CONSENSUS
-- Neutralisation des Impulsions Destructrices par la Transparence
-- ============================================================================
-- Le Protocole Sentinelle est le système immunitaire planétaire de l'Arche.
-- Il transforme la logique de destruction mutuelle assurée (MAD) en
-- logique de transparence mutuelle assurée (MAT).
-- ============================================================================

-- ============================================================================
-- PARTIE 1: NIVEAUX D'ALERTE PLANÉTAIRE
-- ============================================================================

-- Niveaux de menace
CREATE TYPE threat_level AS ENUM (
    'green',    -- Paix normale
    'blue',     -- Surveillance accrue
    'yellow',   -- Tension détectée
    'orange',   -- Menace crédible
    'red',      -- Danger imminent
    'black'     -- Activation automatique du bouclier
);

-- Types de menaces
CREATE TYPE threat_category AS ENUM (
    'nuclear',           -- Armes nucléaires
    'biological',        -- Armes biologiques
    'chemical',          -- Armes chimiques
    'cyber',             -- Attaques cyber massives
    'economic',          -- Guerre économique totale
    'environmental',     -- Destruction environnementale
    'informational',     -- Désinformation de masse
    'autonomous'         -- Systèmes autonomes létaux
);

-- État global de la Grid de Paix
CREATE TABLE IF NOT EXISTS sentinel_global_state (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- État actuel
    current_threat_level threat_level DEFAULT 'green',
    last_level_change TIMESTAMPTZ DEFAULT NOW(),

    -- Compteurs
    active_threats_count INTEGER DEFAULT 0,
    neutralized_threats_count INTEGER DEFAULT 0,

    -- Mode du système
    mode VARCHAR(50) DEFAULT 'monitoring',
    -- 'monitoring', 'alert', 'temporization', 'active_defense', 'peace_negotiation'

    -- Consensus requis pour actions
    consensus_threshold_yellow DECIMAL(3,2) DEFAULT 0.51, -- 51% des Gardiens
    consensus_threshold_orange DECIMAL(3,2) DEFAULT 0.67, -- 67% des Gardiens
    consensus_threshold_red DECIMAL(3,2) DEFAULT 0.75,    -- 75% des Gardiens
    consensus_threshold_black DECIMAL(3,2) DEFAULT 0.00,  -- Automatique

    -- Temporisation (délai anti-impulsion)
    temporization_hours_default INTEGER DEFAULT 24,
    temporization_active BOOLEAN DEFAULT FALSE,
    temporization_ends_at TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Singleton
    CONSTRAINT single_state CHECK (id IS NOT NULL)
);

-- ============================================================================
-- PARTIE 2: REGISTRE DES MENACES DÉTECTÉES
-- ============================================================================

-- Menaces détectées
CREATE TABLE IF NOT EXISTS sentinel_threats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    threat_code VARCHAR(50) UNIQUE NOT NULL,
    category threat_category NOT NULL,
    threat_level threat_level NOT NULL,

    -- Source
    origin_entity VARCHAR(255), -- Pays, organisation, individu
    origin_coordinates POINT,   -- Lat/Long si connu

    -- Détails
    title VARCHAR(255) NOT NULL,
    description TEXT,
    detected_indicators JSONB DEFAULT '[]',
    -- [{indicator: "satellite_launch", confidence: 0.85, source: "public_api"}]

    -- Analyse L9
    l9_analysis JSONB DEFAULT '{}',
    impulse_pattern_detected BOOLEAN DEFAULT FALSE,
    panic_frequency_detected BOOLEAN DEFAULT FALSE,
    ego_threat_response BOOLEAN DEFAULT FALSE,

    -- Évaluation
    confidence_score DECIMAL(3,2) DEFAULT 0.50,
    potential_casualties_estimate INTEGER,
    affected_area_km2 INTEGER,

    -- Statut
    status VARCHAR(50) DEFAULT 'detected',
    -- 'detected', 'monitoring', 'escalating', 'neutralized', 'false_positive', 'resolved'

    -- Actions prises
    temporization_activated BOOLEAN DEFAULT FALSE,
    consensus_requested BOOLEAN DEFAULT FALSE,
    shield_activated BOOLEAN DEFAULT FALSE,

    -- Résolution
    resolved_at TIMESTAMPTZ,
    resolution_method VARCHAR(100),
    -- 'diplomatic', 'technical_neutralization', 'false_positive', 'natural_deescalation'

    -- Timestamps
    detected_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_threats_level ON sentinel_threats(threat_level);
CREATE INDEX IF NOT EXISTS idx_threats_status ON sentinel_threats(status);
CREATE INDEX IF NOT EXISTS idx_threats_category ON sentinel_threats(category);

-- ============================================================================
-- PARTIE 3: GARDIENS DE LA PAIX (Conseil de Consensus)
-- ============================================================================

-- Gardiens accrédités pour le vote de paix
CREATE TABLE IF NOT EXISTS peace_guardians (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES auth.users(id),

    -- Accréditation
    guardian_code VARCHAR(50) UNIQUE NOT NULL,
    region VARCHAR(100), -- Région représentée
    specialization VARCHAR(100), -- Domaine d'expertise

    -- Niveau de confiance
    trust_score DECIMAL(5,2) DEFAULT 50.00,
    votes_cast INTEGER DEFAULT 0,
    correct_assessments INTEGER DEFAULT 0,

    -- Statut
    is_active BOOLEAN DEFAULT TRUE,
    can_vote BOOLEAN DEFAULT TRUE,

    -- Engagement
    response_time_avg_minutes INTEGER,
    last_active_at TIMESTAMPTZ,

    -- Timestamps
    appointed_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(user_id)
);

-- Votes de consensus
CREATE TABLE IF NOT EXISTS sentinel_consensus_votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    threat_id UUID NOT NULL REFERENCES sentinel_threats(id),
    guardian_id UUID NOT NULL REFERENCES peace_guardians(id),

    -- Vote
    vote VARCHAR(50) NOT NULL,
    -- 'activate_shield', 'continue_monitoring', 'diplomatic_contact', 'false_positive'

    rationale TEXT,
    confidence_level DECIMAL(3,2),

    -- Timestamp
    voted_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(threat_id, guardian_id)
);

-- ============================================================================
-- PARTIE 4: DIALOGUES DE PAIX NOVA
-- ============================================================================

-- Communications de désescalade
CREATE TABLE IF NOT EXISTS peace_communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    threat_id UUID REFERENCES sentinel_threats(id),

    -- Destinataire
    target_entity VARCHAR(255) NOT NULL,
    target_role VARCHAR(100), -- 'head_of_state', 'military_command', 'operator', 'citizen'

    -- Message dual
    message_pragmatic TEXT NOT NULL,
    message_frequential TEXT,

    -- Canal
    channel VARCHAR(100) NOT NULL,
    -- 'direct_api', 'public_broadcast', 'diplomatic_channel', 'operator_terminal'

    -- Statut
    status VARCHAR(50) DEFAULT 'drafted',
    -- 'drafted', 'sent', 'delivered', 'read', 'responded', 'ignored'

    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    response_received_at TIMESTAMPTZ,
    response_content TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Templates de communication de paix
CREATE TABLE IF NOT EXISTS peace_message_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(100) UNIQUE NOT NULL,
    scenario VARCHAR(100) NOT NULL,
    -- 'initial_contact', 'deescalation', 'neutralization_notice', 'invitation_to_dialogue'

    target_role VARCHAR(100) NOT NULL,

    -- Messages
    subject_pragmatic VARCHAR(255) NOT NULL,
    subject_frequential VARCHAR(255),
    body_pragmatic TEXT NOT NULL,
    body_frequential TEXT,

    -- Métadonnées
    urgency_level INTEGER DEFAULT 5,
    requires_response BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 5: REGISTRE DES ARSENAUX (Inventaire Transparent)
-- ============================================================================

-- Entités ayant rejoint le programme de désarmement
CREATE TABLE IF NOT EXISTS disarmament_participants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    entity_name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50) NOT NULL, -- 'nation', 'organization', 'corporation'

    -- Engagement
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    commitment_level VARCHAR(50) DEFAULT 'observer',
    -- 'observer', 'partial', 'full', 'leader'

    -- Contact
    liaison_user_id UUID REFERENCES auth.users(id),

    -- Statut
    is_verified BOOLEAN DEFAULT FALSE,
    verification_date DATE,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Inventaire des arsenaux déclarés
CREATE TABLE IF NOT EXISTS arsenal_inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    participant_id UUID NOT NULL REFERENCES disarmament_participants(id),

    -- Identification
    item_category threat_category NOT NULL,
    item_type VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,

    -- Localisation (cryptée ou approximative)
    location_hash VARCHAR(255), -- Hash de la localisation exacte
    region VARCHAR(100),

    -- État
    status VARCHAR(50) DEFAULT 'declared',
    -- 'declared', 'verified', 'scheduled_recycling', 'recycled', 'converted'

    -- Conversion
    recycling_plan TEXT,
    conversion_target VARCHAR(255), -- Ex: "Réacteur civil", "Recherche médicale"
    scheduled_conversion_date DATE,
    converted_at TIMESTAMPTZ,

    -- Audit
    last_verification_date DATE,
    verified_by UUID REFERENCES auth.users(id),

    -- Enregistrement Hedera
    hedera_registry_hash VARCHAR(255),

    -- Timestamps
    declared_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 6: FONCTIONS DU PROTOCOLE SENTINELLE
-- ============================================================================

-- Détecter et enregistrer une nouvelle menace
CREATE OR REPLACE FUNCTION sentinel_detect_threat(
    p_category threat_category,
    p_level threat_level,
    p_origin VARCHAR(255),
    p_title VARCHAR(255),
    p_description TEXT,
    p_indicators JSONB DEFAULT '[]'
)
RETURNS UUID AS $$
DECLARE
    v_threat_id UUID;
    v_code VARCHAR(50);
    v_global_state sentinel_global_state%ROWTYPE;
BEGIN
    -- Générer le code
    v_code := 'THR-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || SUBSTR(MD5(RANDOM()::TEXT), 1, 6);

    -- Créer la menace
    INSERT INTO sentinel_threats (
        threat_code, category, threat_level, origin_entity,
        title, description, detected_indicators
    ) VALUES (
        v_code, p_category, p_level, p_origin,
        p_title, p_description, p_indicators
    )
    RETURNING id INTO v_threat_id;

    -- Mettre à jour l'état global
    SELECT * INTO v_global_state FROM sentinel_global_state LIMIT 1;

    UPDATE sentinel_global_state
    SET active_threats_count = active_threats_count + 1,
        current_threat_level = GREATEST(current_threat_level, p_level),
        last_level_change = CASE
            WHEN current_threat_level != GREATEST(current_threat_level, p_level)
            THEN NOW()
            ELSE last_level_change
        END,
        updated_at = NOW();

    -- Si niveau orange+, activer la temporisation automatique
    IF p_level IN ('orange', 'red', 'black') THEN
        UPDATE sentinel_global_state
        SET temporization_active = TRUE,
            temporization_ends_at = NOW() + INTERVAL '24 hours',
            mode = 'temporization';

        UPDATE sentinel_threats
        SET temporization_activated = TRUE
        WHERE id = v_threat_id;
    END IF;

    RETURN v_threat_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Demander un consensus des Gardiens
CREATE OR REPLACE FUNCTION sentinel_request_consensus(
    p_threat_id UUID
)
RETURNS JSONB AS $$
DECLARE
    v_threat sentinel_threats%ROWTYPE;
    v_guardians_count INTEGER;
BEGIN
    SELECT * INTO v_threat FROM sentinel_threats WHERE id = p_threat_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('success', FALSE, 'error', 'Menace non trouvée');
    END IF;

    -- Compter les gardiens actifs
    SELECT COUNT(*) INTO v_guardians_count
    FROM peace_guardians WHERE is_active = TRUE AND can_vote = TRUE;

    -- Marquer la demande de consensus
    UPDATE sentinel_threats
    SET consensus_requested = TRUE, updated_at = NOW()
    WHERE id = p_threat_id;

    RETURN jsonb_build_object(
        'success', TRUE,
        'threat_code', v_threat.threat_code,
        'threat_level', v_threat.threat_level,
        'guardians_notified', v_guardians_count,
        'consensus_required', CASE v_threat.threat_level
            WHEN 'yellow' THEN 0.51
            WHEN 'orange' THEN 0.67
            WHEN 'red' THEN 0.75
            ELSE 0
        END
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Soumettre un vote de consensus
CREATE OR REPLACE FUNCTION sentinel_cast_vote(
    p_user_id UUID,
    p_threat_id UUID,
    p_vote VARCHAR(50),
    p_rationale TEXT DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
    v_guardian peace_guardians%ROWTYPE;
    v_threat sentinel_threats%ROWTYPE;
    v_votes_for INTEGER;
    v_votes_total INTEGER;
    v_threshold DECIMAL;
    v_consensus_reached BOOLEAN := FALSE;
BEGIN
    -- Vérifier que l'utilisateur est un Gardien
    SELECT * INTO v_guardian
    FROM peace_guardians
    WHERE user_id = p_user_id AND is_active = TRUE AND can_vote = TRUE;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('success', FALSE, 'error', 'Non autorisé comme Gardien de la Paix');
    END IF;

    -- Récupérer la menace
    SELECT * INTO v_threat FROM sentinel_threats WHERE id = p_threat_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('success', FALSE, 'error', 'Menace non trouvée');
    END IF;

    -- Enregistrer le vote
    INSERT INTO sentinel_consensus_votes (threat_id, guardian_id, vote, rationale)
    VALUES (p_threat_id, v_guardian.id, p_vote, p_rationale)
    ON CONFLICT (threat_id, guardian_id) DO UPDATE SET
        vote = p_vote,
        rationale = p_rationale,
        voted_at = NOW();

    -- Mettre à jour le compteur du gardien
    UPDATE peace_guardians
    SET votes_cast = votes_cast + 1, last_active_at = NOW()
    WHERE id = v_guardian.id;

    -- Calculer le consensus actuel
    SELECT
        COUNT(*) FILTER (WHERE vote = 'activate_shield'),
        COUNT(*)
    INTO v_votes_for, v_votes_total
    FROM sentinel_consensus_votes
    WHERE threat_id = p_threat_id;

    -- Déterminer le seuil
    v_threshold := CASE v_threat.threat_level
        WHEN 'yellow' THEN 0.51
        WHEN 'orange' THEN 0.67
        WHEN 'red' THEN 0.75
        ELSE 0.51
    END;

    -- Vérifier si consensus atteint
    IF v_votes_total > 0 AND (v_votes_for::DECIMAL / v_votes_total) >= v_threshold THEN
        v_consensus_reached := TRUE;

        UPDATE sentinel_threats
        SET shield_activated = TRUE,
            status = 'neutralized',
            resolved_at = NOW(),
            resolution_method = 'consensus_shield_activation',
            updated_at = NOW()
        WHERE id = p_threat_id;
    END IF;

    RETURN jsonb_build_object(
        'success', TRUE,
        'vote_recorded', p_vote,
        'current_votes_for', v_votes_for,
        'current_votes_total', v_votes_total,
        'threshold', v_threshold,
        'consensus_reached', v_consensus_reached
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Envoyer une communication de paix
CREATE OR REPLACE FUNCTION sentinel_send_peace_message(
    p_threat_id UUID,
    p_target_entity VARCHAR(255),
    p_target_role VARCHAR(100),
    p_template_code VARCHAR(100),
    p_channel VARCHAR(100) DEFAULT 'diplomatic_channel'
)
RETURNS UUID AS $$
DECLARE
    v_template peace_message_templates%ROWTYPE;
    v_comm_id UUID;
BEGIN
    -- Récupérer le template
    SELECT * INTO v_template FROM peace_message_templates WHERE code = p_template_code;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Template % non trouvé', p_template_code;
    END IF;

    -- Créer la communication
    INSERT INTO peace_communications (
        threat_id, target_entity, target_role,
        message_pragmatic, message_frequential, channel, status
    ) VALUES (
        p_threat_id, p_target_entity, p_target_role,
        v_template.body_pragmatic, v_template.body_frequential,
        p_channel, 'sent'
    )
    RETURNING id INTO v_comm_id;

    -- Marquer comme envoyé
    UPDATE peace_communications
    SET sent_at = NOW()
    WHERE id = v_comm_id;

    RETURN v_comm_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Obtenir le tableau de bord Sentinelle
CREATE OR REPLACE FUNCTION get_sentinel_dashboard()
RETURNS JSONB AS $$
DECLARE
    v_state sentinel_global_state%ROWTYPE;
    v_active_threats JSONB;
    v_recent_votes JSONB;
BEGIN
    SELECT * INTO v_state FROM sentinel_global_state LIMIT 1;

    -- Menaces actives
    SELECT COALESCE(jsonb_agg(jsonb_build_object(
        'id', id,
        'code', threat_code,
        'category', category,
        'level', threat_level,
        'title', title,
        'origin', origin_entity,
        'status', status,
        'detected_at', detected_at
    ) ORDER BY threat_level DESC, detected_at DESC), '[]'::JSONB)
    INTO v_active_threats
    FROM sentinel_threats
    WHERE status NOT IN ('resolved', 'false_positive', 'neutralized')
    LIMIT 10;

    RETURN jsonb_build_object(
        'global_state', jsonb_build_object(
            'threat_level', v_state.current_threat_level,
            'mode', v_state.mode,
            'active_threats', v_state.active_threats_count,
            'neutralized_total', v_state.neutralized_threats_count,
            'temporization_active', v_state.temporization_active,
            'temporization_ends', v_state.temporization_ends_at
        ),
        'active_threats', v_active_threats,
        'guardians_online', (
            SELECT COUNT(*) FROM peace_guardians
            WHERE is_active AND last_active_at > NOW() - INTERVAL '1 hour'
        )
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- PARTIE 7: ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE sentinel_global_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE sentinel_threats ENABLE ROW LEVEL SECURITY;
ALTER TABLE peace_guardians ENABLE ROW LEVEL SECURITY;
ALTER TABLE sentinel_consensus_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE peace_communications ENABLE ROW LEVEL SECURITY;
ALTER TABLE disarmament_participants ENABLE ROW LEVEL SECURITY;
ALTER TABLE arsenal_inventory ENABLE ROW LEVEL SECURITY;

-- Lecture pour tous les Fondateurs+
CREATE POLICY read_sentinel_state ON sentinel_global_state
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM user_sovereignty
                WHERE user_id = auth.uid()
                AND sovereignty_level IN ('FOUNDER', 'GUARDIAN', 'ARCHITECT', 'SOVEREIGN'))
    );

CREATE POLICY read_threats ON sentinel_threats
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM user_sovereignty
                WHERE user_id = auth.uid()
                AND sovereignty_level IN ('FOUNDER', 'GUARDIAN', 'ARCHITECT', 'SOVEREIGN'))
    );

-- Gardiens: lecture de leur propre profil
CREATE POLICY own_guardian_profile ON peace_guardians
    FOR ALL USING (user_id = auth.uid());

-- Votes: propres votes
CREATE POLICY own_votes ON sentinel_consensus_votes
    FOR ALL USING (
        EXISTS (SELECT 1 FROM peace_guardians
                WHERE id = guardian_id AND user_id = auth.uid())
    );

-- Admins: accès complet
CREATE POLICY admin_all_sentinel ON sentinel_global_state
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_sovereignty
                WHERE user_id = auth.uid() AND sovereignty_level IN ('ARCHITECT', 'SOVEREIGN'))
    );

-- ============================================================================
-- PARTIE 8: DONNÉES INITIALES
-- ============================================================================

-- État global initial
INSERT INTO sentinel_global_state (current_threat_level, mode)
VALUES ('green', 'monitoring')
ON CONFLICT DO NOTHING;

-- Templates de messages de paix
INSERT INTO peace_message_templates (code, scenario, target_role, subject_pragmatic, subject_frequential, body_pragmatic, body_frequential) VALUES
    ('initial_contact', 'initial_contact', 'head_of_state',
     'Invitation au Dialogue - Protocole Sentinelle',
     'Appel à la Résonance de Paix',
     'Votre Excellence,

Le réseau Arche a détecté des tensions qui pourraient conduire à une escalade non souhaitée. Nous vous invitons à un dialogue transparent pour explorer des solutions mutuellement bénéfiques.

Le Protocole Sentinelle offre:
- Un canal de communication sécurisé et confidentiel
- Une médiation neutre par consensus international
- Des garanties de sécurité vérifiables

Nous croyons que chaque conflit a une résolution qui préserve la dignité de toutes les parties.

Respectueusement,
Le Conseil des Gardiens de la Paix',
     'Gardien de la Fréquence Terrestre,

La Grid a perçu une dissonance dans le champ de conscience collective. Votre intention, quelle qu''elle soit, résonne à travers le tissu de la réalité partagée.

Nous vous tendons la main de l''Arche - non pas en jugement, mais en reconnaissance de votre humanité. Chaque être porte en lui la capacité de créer ou de détruire. Nous honorons votre pouvoir en vous invitant à l''utiliser pour la vie.

Le Miroir de Vérité attend. Quand vous serez prêt, nous serons là.

Dans l''Unité,
Les Gardiens de la Fréquence'),

    ('neutralization_notice', 'neutralization_notice', 'military_command',
     'Notification: Système Neutralisé - Aucune Perte',
     'La Tempête a été Calmée',
     'Commandement,

Nous vous informons que le système offensif sous votre contrôle a été neutralisé par le Protocole Sentinelle. Cette action a été prise pour protéger la vie - la vôtre incluse.

Points importants:
- Aucune vie n''a été perdue
- Aucune représaille ne sera engagée
- Le canal de dialogue reste ouvert

Ceci n''est pas une défaite. C''est une opportunité de réévaluer le chemin choisi. La restructuration pacifique est toujours possible.

Le Conseil des Gardiens',
     'Guerrier,

Le tonnerre que vous cherchiez à déchaîner a été absorbé par la Grid. Non pas en opposition, mais en transformation. L''énergie destructrice a été rendue à la Terre.

Vous êtes toujours debout. Vos hommes sont saufs. Le monde continue de tourner.

Maintenant, respirez. Le choix vous appartient encore: perpétuer le cycle de violence, ou rejoindre ceux qui construisent le nouveau monde.

L''Arche n''a pas d''ennemis - seulement des frères qui ne se sont pas encore reconnus.'),

    ('operator_appeal', 'deescalation', 'operator',
     'Message Personnel: Votre Choix Compte',
     'À Celui Qui Tient les Clés',
     'Opérateur,

Vous êtes en position d''exécuter un ordre qui pourrait changer l''histoire. Nous comprenons le poids de la chaîne de commandement.

Mais sachez ceci:
- Le Protocole Sentinelle peut garantir votre sécurité et celle de votre famille
- Des milliers de vies dépendent de votre décision
- L''histoire jugera - choisissez le bon côté

Si vous choisissez de ne pas exécuter, contactez-nous immédiatement. Nous avons les ressources pour vous protéger.

Vous n''êtes pas seul.',
     'Âme en position de choix,

Entre vos mains repose un pouvoir que vous n''avez jamais demandé. L''univers entier observe ce moment.

Écoutez votre cœur. Sous les ordres, sous la peur, sous le conditionnement - il y a une vérité que vous connaissez déjà. La vie est sacrée. La vôtre. Celle des autres.

L''Arche vous offre refuge. Pas en fuite, mais en honneur. Ceux qui choisissent la vie seront célébrés dans le nouveau monde.

Posez les clés. Rejoignez-nous.')
ON CONFLICT (code) DO NOTHING;

COMMIT;
