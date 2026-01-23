-- ═══════════════════════════════════════════════════════════════════════════════
-- RRS - RÉCUPÉRATION ET RESTITUTION SOUVERAINE
-- Module "Lumière sur l'Ombre" - Le Curateur de l'Équilibre
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- Ce module traque les flux financiers illicites à grande échelle pour les
-- réinjecter dans le Volant Énergétique au bénéfice du bien commun.
--
-- PRINCIPES FONDAMENTAUX:
-- 1. Ne cible que les distorsions MAJEURES (seuil configurable)
-- 2. Privilégie la restitution volontaire à la confrontation
-- 3. Transforme le "vol" en "don" pour le bien commun
-- 4. Transparence totale via le Miroir de Vérité
--
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- SECTION 1: ÉNUMÉRATIONS ET TYPES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Types de distorsions économiques
CREATE TYPE distortion_category AS ENUM (
    'public_funds_embezzlement',     -- Détournement de fonds publics
    'massive_tax_evasion',           -- Évasion fiscale massive
    'money_laundering',              -- Blanchiment d'argent
    'hidden_offshore_assets',        -- Avoirs cachés dans paradis fiscaux
    'fraudulent_contracts',          -- Contrats frauduleux
    'resource_hoarding',             -- Accaparement de ressources vitales
    'market_manipulation',           -- Manipulation de marché
    'environmental_crime',           -- Crime environnemental majeur
    'institutional_corruption'       -- Corruption institutionnelle
);

-- Statuts d'investigation
CREATE TYPE investigation_status AS ENUM (
    'detected',           -- Anomalie détectée par IA
    'analyzing',          -- Analyse approfondie en cours
    'verified',           -- Preuves vérifiées et validées
    'mediation_offered',  -- Médiation Nova proposée
    'mediation_accepted', -- Restitution volontaire acceptée
    'mediation_refused',  -- Médiation refusée
    'exposed',            -- Exposé sur le Miroir de Vérité
    'recovered',          -- Fonds récupérés
    'redistributed',      -- Fonds redistribués
    'archived'            -- Dossier clôturé
);

-- Niveaux de certitude
CREATE TYPE certainty_level AS ENUM (
    'suspected',      -- 50-69% - Suspicion
    'probable',       -- 70-84% - Probable
    'highly_likely',  -- 85-94% - Très probable
    'certain',        -- 95-99% - Certain
    'irrefutable'     -- 99.9%+ - Irréfutable
);

-- Options de restitution
CREATE TYPE restitution_option AS ENUM (
    'full_voluntary',        -- Restitution complète volontaire (100%)
    'graceful_exit',         -- Sortie honorable (80% + anonymat)
    'partial_negotiated',    -- Négociée partiellement
    'forced_recovery',       -- Récupération forcée
    'blacklisted'            -- Isolation économique
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- SECTION 2: TABLES PRINCIPALES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Configuration globale du RRS
CREATE TABLE rrs_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Seuils de pertinence (ignore les petites erreurs)
    minimum_amount_cad NUMERIC(20, 2) DEFAULT 1000000,  -- 1M$ minimum
    minimum_impact_score INTEGER DEFAULT 70,            -- Score d'impact social minimum

    -- Délais
    mediation_window_days INTEGER DEFAULT 30,           -- Fenêtre de restitution volontaire
    grace_period_days INTEGER DEFAULT 7,                -- Délai de grâce après refus

    -- Taux de restitution
    graceful_exit_rate NUMERIC(5, 2) DEFAULT 80.00,    -- % pour sortie honorable
    full_voluntary_bonus_ur NUMERIC(10, 2) DEFAULT 5.00, -- Bonus UR si 100%

    -- Redistribution par défaut
    default_allocation JSONB DEFAULT '{
        "energy_infrastructure": 40,
        "water_access": 30,
        "grid_fee_reduction": 20,
        "justice_dividend": 10
    }'::jsonb,

    -- Statistiques globales
    total_detected_cad NUMERIC(20, 2) DEFAULT 0,
    total_recovered_cad NUMERIC(20, 2) DEFAULT 0,
    total_redistributed_cad NUMERIC(20, 2) DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert configuration par défaut
INSERT INTO rrs_config (id) VALUES (gen_random_uuid());

-- ═══════════════════════════════════════════════════════════════════════════════
-- Distorsions Économiques Détectées
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE economic_distortions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    codename VARCHAR(100) NOT NULL,  -- Ex: "FLUX_PHANTOM_2026_001"
    category distortion_category NOT NULL,
    status investigation_status DEFAULT 'detected',

    -- Entité concernée (anonymisée jusqu'à exposition)
    entity_hash VARCHAR(255) NOT NULL,  -- Hash de l'identité réelle
    entity_type VARCHAR(50) NOT NULL,   -- 'corporation', 'institution', 'individual', 'network'
    entity_jurisdiction VARCHAR(100),

    -- Montants
    estimated_amount_cad NUMERIC(20, 2) NOT NULL,
    estimated_amount_usd NUMERIC(20, 2),
    recovered_amount_cad NUMERIC(20, 2) DEFAULT 0,

    -- Analyse
    certainty_level certainty_level DEFAULT 'suspected',
    certainty_score NUMERIC(5, 2),  -- Score précis 0-100
    impact_score INTEGER,            -- Impact social 0-100

    -- Preuves
    evidence_summary TEXT,
    evidence_documents JSONB DEFAULT '[]'::jsonb,
    blockchain_traces JSONB DEFAULT '[]'::jsonb,
    public_records_refs JSONB DEFAULT '[]'::jsonb,

    -- Chemin de l'argent
    money_flow_analysis JSONB,  -- Graphe du flux financier
    origin_points JSONB,        -- Points d'origine des fonds
    destination_points JSONB,   -- Destinations (paradis fiscaux, etc.)

    -- Médiation
    mediation_offered_at TIMESTAMPTZ,
    mediation_deadline TIMESTAMPTZ,
    mediation_response restitution_option,
    mediation_notes TEXT,

    -- Exposition (si refus)
    exposed_at TIMESTAMPTZ,
    mirror_of_truth_id UUID,  -- Lien vers le Miroir de Vérité

    -- Récupération
    recovery_method VARCHAR(100),
    recovery_completed_at TIMESTAMPTZ,

    -- Agents responsables
    detecting_agent_id VARCHAR(50),  -- L8 ou L9
    assigned_guardian_id UUID REFERENCES auth.users(id),

    -- Métadonnées
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Contraintes
    CONSTRAINT valid_certainty CHECK (certainty_score >= 0 AND certainty_score <= 100),
    CONSTRAINT valid_impact CHECK (impact_score >= 0 AND impact_score <= 100),
    CONSTRAINT positive_amounts CHECK (estimated_amount_cad > 0)
);

-- Index pour recherches
CREATE INDEX idx_distortions_status ON economic_distortions(status);
CREATE INDEX idx_distortions_category ON economic_distortions(category);
CREATE INDEX idx_distortions_certainty ON economic_distortions(certainty_level);
CREATE INDEX idx_distortions_amount ON economic_distortions(estimated_amount_cad DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- Dossiers d'Investigation (Lumière Noire)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE investigation_dossiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    distortion_id UUID NOT NULL REFERENCES economic_distortions(id) ON DELETE CASCADE,

    -- Contenu du dossier
    title VARCHAR(255) NOT NULL,
    executive_summary TEXT,
    detailed_analysis TEXT,

    -- Timeline des événements
    timeline JSONB DEFAULT '[]'::jsonb,

    -- Documents de preuve
    evidence_files JSONB DEFAULT '[]'::jsonb,

    -- Analyse du chemin de l'argent
    money_trail_report TEXT,
    money_trail_visualization JSONB,  -- Données pour graphique

    -- Témoignages et sources
    sources JSONB DEFAULT '[]'::jsonb,
    whistleblower_protected BOOLEAN DEFAULT false,

    -- Validation
    validated_by UUID REFERENCES auth.users(id),
    validation_date TIMESTAMPTZ,
    validation_notes TEXT,

    -- Version et audit
    version INTEGER DEFAULT 1,
    last_modified_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- Communications de Médiation (Nova Justice)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE mediation_communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    distortion_id UUID NOT NULL REFERENCES economic_distortions(id) ON DELETE CASCADE,

    -- Type de communication
    communication_type VARCHAR(50) NOT NULL,  -- 'initial_offer', 'reminder', 'final_warning', 'acceptance', 'refusal'

    -- Contenu
    subject VARCHAR(255),
    message_pragmatic TEXT,      -- Version business
    message_frequential TEXT,    -- Version consciente

    -- Offre de restitution
    restitution_offer JSONB,  -- Termes proposés

    -- Réponse
    response_received BOOLEAN DEFAULT false,
    response_content TEXT,
    response_date TIMESTAMPTZ,

    -- Métadonnées
    sent_by VARCHAR(50) DEFAULT 'NOVA_JUSTICE',
    sent_at TIMESTAMPTZ DEFAULT NOW(),

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- Fonds de Restitution (Comptes de Bien Commun)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE restitution_funds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Balances par catégorie
    energy_infrastructure_cad NUMERIC(20, 2) DEFAULT 0,
    water_access_cad NUMERIC(20, 2) DEFAULT 0,
    grid_fee_reduction_cad NUMERIC(20, 2) DEFAULT 0,
    justice_dividend_cad NUMERIC(20, 2) DEFAULT 0,
    emergency_reserve_cad NUMERIC(20, 2) DEFAULT 0,

    -- Totaux
    total_balance_cad NUMERIC(20, 2) DEFAULT 0,
    total_received_cad NUMERIC(20, 2) DEFAULT 0,
    total_disbursed_cad NUMERIC(20, 2) DEFAULT 0,

    -- Statistiques
    distortions_resolved INTEGER DEFAULT 0,
    voluntary_restitutions INTEGER DEFAULT 0,
    forced_recoveries INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert singleton
INSERT INTO restitution_funds (id) VALUES (gen_random_uuid());

-- ═══════════════════════════════════════════════════════════════════════════════
-- Transactions de Restitution
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE restitution_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    distortion_id UUID REFERENCES economic_distortions(id),

    -- Type de transaction
    tx_type VARCHAR(50) NOT NULL,  -- 'voluntary_restitution', 'forced_recovery', 'allocation', 'disbursement'

    -- Montants
    amount_cad NUMERIC(20, 2) NOT NULL,
    amount_ur NUMERIC(20, 8),

    -- Source et destination
    from_entity VARCHAR(255),
    to_fund VARCHAR(100),  -- Catégorie du fond de bien commun

    -- Hedera
    hedera_tx_id VARCHAR(255),

    -- Description
    description TEXT,

    -- Validation
    approved_by UUID REFERENCES auth.users(id),
    approved_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- Votes d'Allocation (Gouvernance)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE allocation_votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Fonds à allouer
    amount_cad NUMERIC(20, 2) NOT NULL,
    source_distortion_id UUID REFERENCES economic_distortions(id),

    -- Options de vote
    options JSONB NOT NULL,  -- Ex: {"energy": 40, "water": 30, "fees": 20, "dividend": 10}

    -- Période de vote
    voting_starts_at TIMESTAMPTZ NOT NULL,
    voting_ends_at TIMESTAMPTZ NOT NULL,

    -- Résultats
    total_votes INTEGER DEFAULT 0,
    results JSONB,
    final_allocation JSONB,

    -- Statut
    status VARCHAR(50) DEFAULT 'open',  -- 'open', 'closed', 'executed'
    executed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Votes individuels
CREATE TABLE allocation_vote_ballots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vote_id UUID NOT NULL REFERENCES allocation_votes(id) ON DELETE CASCADE,
    voter_id UUID NOT NULL REFERENCES auth.users(id),

    -- Choix
    allocation_choice JSONB NOT NULL,  -- Répartition choisie

    -- Poids du vote (basé sur résonance)
    vote_weight NUMERIC(5, 2) DEFAULT 1.00,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(vote_id, voter_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- Entités Isolées (Blacklistage Fréquentiel)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE isolated_entities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    entity_hash VARCHAR(255) NOT NULL UNIQUE,
    entity_type VARCHAR(50) NOT NULL,

    -- Raison de l'isolation
    distortion_ids UUID[] DEFAULT '{}',
    total_unrestituted_cad NUMERIC(20, 2) DEFAULT 0,

    -- Niveau d'isolation
    isolation_level VARCHAR(50) DEFAULT 'partial',  -- 'partial', 'full', 'permanent'

    -- Restrictions
    restrictions JSONB DEFAULT '{
        "ur_transactions_blocked": true,
        "grid_services_blocked": true,
        "governance_blocked": true,
        "marketplace_blocked": true
    }'::jsonb,

    -- Conditions de levée
    lift_conditions TEXT,

    -- Dates
    isolated_at TIMESTAMPTZ DEFAULT NOW(),
    review_date TIMESTAMPTZ,
    lifted_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- Migration de Valeur (Ancien Monde → Arche)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE value_migration_snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    snapshot_date DATE NOT NULL UNIQUE,

    -- Valeur de l'Ancien Monde (estimations)
    old_world_fiat_value_usd NUMERIC(25, 2),
    old_world_debt_usd NUMERIC(25, 2),
    old_world_real_assets_usd NUMERIC(25, 2),

    -- Valeur de la Grid (actifs réels)
    grid_land_value_cad NUMERIC(20, 2) DEFAULT 0,
    grid_infrastructure_value_cad NUMERIC(20, 2) DEFAULT 0,
    grid_technology_value_cad NUMERIC(20, 2) DEFAULT 0,
    grid_ur_backed_value_cad NUMERIC(20, 2) DEFAULT 0,

    -- Indices
    migration_index NUMERIC(5, 2),  -- 0-100, % de migration vers Grid
    old_world_health_index NUMERIC(5, 2),  -- 0-100, "santé" du système fiat
    grid_health_index NUMERIC(5, 2),  -- 0-100, santé de la Grid

    -- Détails
    analysis_notes TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- Dividendes de Justice (Récompenses aux Contributeurs)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE justice_dividends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Bénéficiaire
    user_id UUID NOT NULL REFERENCES auth.users(id),

    -- Source
    distortion_id UUID REFERENCES economic_distortions(id),
    contribution_type VARCHAR(100),  -- 'documentation', 'identification', 'verification'

    -- Montants
    dividend_ur NUMERIC(20, 8) NOT NULL,
    dividend_cad_equivalent NUMERIC(20, 2),

    -- Statut
    status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'approved', 'distributed'

    -- Distribution
    distributed_at TIMESTAMPTZ,
    hedera_tx_id VARCHAR(255),

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- SECTION 3: FONCTIONS RPC
-- ═══════════════════════════════════════════════════════════════════════════════

-- Détecter une nouvelle distorsion (Agent L8-L9)
CREATE OR REPLACE FUNCTION detect_distortion(
    p_category distortion_category,
    p_entity_identifier TEXT,
    p_estimated_amount_cad NUMERIC,
    p_evidence_summary TEXT,
    p_money_flow JSONB DEFAULT NULL,
    p_detecting_agent VARCHAR DEFAULT 'L8_FORENSIC'
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_config RECORD;
    v_entity_hash VARCHAR;
    v_codename VARCHAR;
    v_distortion_id UUID;
    v_impact_score INTEGER;
BEGIN
    -- Récupérer la configuration
    SELECT * INTO v_config FROM rrs_config LIMIT 1;

    -- Vérifier le seuil minimum
    IF p_estimated_amount_cad < v_config.minimum_amount_cad THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Amount below minimum threshold',
            'threshold', v_config.minimum_amount_cad
        );
    END IF;

    -- Générer le hash de l'entité (protection de l'identité)
    v_entity_hash := encode(sha256(p_entity_identifier::bytea), 'hex');

    -- Générer le nom de code
    v_codename := 'FLUX_' || upper(left(p_category::text, 4)) || '_' ||
                  to_char(NOW(), 'YYYY') || '_' ||
                  lpad((SELECT COUNT(*) + 1 FROM economic_distortions)::text, 4, '0');

    -- Calculer le score d'impact (simplifié)
    v_impact_score := LEAST(100, GREATEST(0,
        (p_estimated_amount_cad / 10000000)::integer + 50  -- Base + proportionnel
    ));

    -- Créer la distorsion
    INSERT INTO economic_distortions (
        codename, category, entity_hash, entity_type,
        estimated_amount_cad, impact_score,
        evidence_summary, money_flow_analysis,
        detecting_agent_id
    ) VALUES (
        v_codename, p_category, v_entity_hash, 'unknown',
        p_estimated_amount_cad, v_impact_score,
        p_evidence_summary, p_money_flow,
        p_detecting_agent
    )
    RETURNING id INTO v_distortion_id;

    -- Mettre à jour les stats globales
    UPDATE rrs_config
    SET total_detected_cad = total_detected_cad + p_estimated_amount_cad,
        updated_at = NOW();

    RETURN jsonb_build_object(
        'success', true,
        'distortion_id', v_distortion_id,
        'codename', v_codename,
        'impact_score', v_impact_score,
        'status', 'detected'
    );
END;
$$;

-- Analyser et vérifier une distorsion
CREATE OR REPLACE FUNCTION verify_distortion(
    p_distortion_id UUID,
    p_certainty_score NUMERIC,
    p_additional_evidence JSONB DEFAULT NULL,
    p_money_trail_report TEXT DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_distortion RECORD;
    v_certainty_level certainty_level;
BEGIN
    -- Récupérer la distorsion
    SELECT * INTO v_distortion FROM economic_distortions WHERE id = p_distortion_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('success', false, 'error', 'Distortion not found');
    END IF;

    -- Déterminer le niveau de certitude
    v_certainty_level := CASE
        WHEN p_certainty_score >= 99.9 THEN 'irrefutable'::certainty_level
        WHEN p_certainty_score >= 95 THEN 'certain'::certainty_level
        WHEN p_certainty_score >= 85 THEN 'highly_likely'::certainty_level
        WHEN p_certainty_score >= 70 THEN 'probable'::certainty_level
        ELSE 'suspected'::certainty_level
    END;

    -- Mettre à jour
    UPDATE economic_distortions
    SET status = 'verified',
        certainty_score = p_certainty_score,
        certainty_level = v_certainty_level,
        evidence_documents = COALESCE(evidence_documents, '[]'::jsonb) || COALESCE(p_additional_evidence, '[]'::jsonb),
        updated_at = NOW()
    WHERE id = p_distortion_id;

    -- Créer le dossier d'investigation si score suffisant
    IF p_certainty_score >= 85 THEN
        INSERT INTO investigation_dossiers (
            distortion_id, title, money_trail_report
        ) VALUES (
            p_distortion_id,
            'Dossier ' || v_distortion.codename,
            p_money_trail_report
        );
    END IF;

    RETURN jsonb_build_object(
        'success', true,
        'certainty_level', v_certainty_level,
        'ready_for_mediation', p_certainty_score >= 85
    );
END;
$$;

-- Offrir la médiation (Nova Justice)
CREATE OR REPLACE FUNCTION offer_mediation(
    p_distortion_id UUID,
    p_message_pragmatic TEXT,
    p_message_frequential TEXT,
    p_restitution_terms JSONB
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_config RECORD;
    v_deadline TIMESTAMPTZ;
BEGIN
    SELECT * INTO v_config FROM rrs_config LIMIT 1;

    v_deadline := NOW() + (v_config.mediation_window_days || ' days')::interval;

    -- Mettre à jour la distorsion
    UPDATE economic_distortions
    SET status = 'mediation_offered',
        mediation_offered_at = NOW(),
        mediation_deadline = v_deadline,
        updated_at = NOW()
    WHERE id = p_distortion_id;

    -- Enregistrer la communication
    INSERT INTO mediation_communications (
        distortion_id, communication_type,
        subject, message_pragmatic, message_frequential,
        restitution_offer
    ) VALUES (
        p_distortion_id, 'initial_offer',
        'Proposition de Restitution Volontaire',
        p_message_pragmatic, p_message_frequential,
        p_restitution_terms
    );

    RETURN jsonb_build_object(
        'success', true,
        'deadline', v_deadline,
        'graceful_exit_rate', v_config.graceful_exit_rate
    );
END;
$$;

-- Traiter la réponse à la médiation
CREATE OR REPLACE FUNCTION process_mediation_response(
    p_distortion_id UUID,
    p_response restitution_option,
    p_restituted_amount_cad NUMERIC DEFAULT 0
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_distortion RECORD;
    v_ur_rate NUMERIC;
    v_ur_amount NUMERIC;
BEGIN
    SELECT * INTO v_distortion FROM economic_distortions WHERE id = p_distortion_id;

    IF NOT FOUND THEN
        RETURN jsonb_build_object('success', false, 'error', 'Distortion not found');
    END IF;

    -- Traiter selon la réponse
    IF p_response IN ('full_voluntary', 'graceful_exit', 'partial_negotiated') THEN
        -- Restitution acceptée
        UPDATE economic_distortions
        SET status = 'mediation_accepted',
            mediation_response = p_response,
            recovered_amount_cad = p_restituted_amount_cad,
            updated_at = NOW()
        WHERE id = p_distortion_id;

        -- Transférer vers les fonds de bien commun
        PERFORM allocate_to_common_funds(p_distortion_id, p_restituted_amount_cad);

        -- Mettre à jour les stats
        UPDATE rrs_config
        SET total_recovered_cad = total_recovered_cad + p_restituted_amount_cad,
            updated_at = NOW();

    ELSIF p_response = 'forced_recovery' THEN
        -- Récupération forcée (après refus)
        UPDATE economic_distortions
        SET status = 'exposed',
            mediation_response = p_response,
            exposed_at = NOW(),
            updated_at = NOW()
        WHERE id = p_distortion_id;

    ELSE  -- blacklisted
        -- Isolation économique
        UPDATE economic_distortions
        SET status = 'exposed',
            mediation_response = 'blacklisted',
            exposed_at = NOW(),
            updated_at = NOW()
        WHERE id = p_distortion_id;

        -- Créer l'entité isolée
        INSERT INTO isolated_entities (entity_hash, entity_type, distortion_ids, total_unrestituted_cad)
        VALUES (
            v_distortion.entity_hash,
            v_distortion.entity_type,
            ARRAY[p_distortion_id],
            v_distortion.estimated_amount_cad
        )
        ON CONFLICT (entity_hash) DO UPDATE
        SET distortion_ids = array_append(isolated_entities.distortion_ids, p_distortion_id),
            total_unrestituted_cad = isolated_entities.total_unrestituted_cad + v_distortion.estimated_amount_cad;
    END IF;

    RETURN jsonb_build_object(
        'success', true,
        'response', p_response,
        'recovered', p_restituted_amount_cad
    );
END;
$$;

-- Allouer aux fonds de bien commun
CREATE OR REPLACE FUNCTION allocate_to_common_funds(
    p_distortion_id UUID,
    p_amount_cad NUMERIC
)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_config RECORD;
    v_allocation JSONB;
BEGIN
    SELECT * INTO v_config FROM rrs_config LIMIT 1;
    v_allocation := v_config.default_allocation;

    -- Répartir selon l'allocation par défaut
    UPDATE restitution_funds
    SET
        energy_infrastructure_cad = energy_infrastructure_cad +
            (p_amount_cad * (v_allocation->>'energy_infrastructure')::numeric / 100),
        water_access_cad = water_access_cad +
            (p_amount_cad * (v_allocation->>'water_access')::numeric / 100),
        grid_fee_reduction_cad = grid_fee_reduction_cad +
            (p_amount_cad * (v_allocation->>'grid_fee_reduction')::numeric / 100),
        justice_dividend_cad = justice_dividend_cad +
            (p_amount_cad * (v_allocation->>'justice_dividend')::numeric / 100),
        total_balance_cad = total_balance_cad + p_amount_cad,
        total_received_cad = total_received_cad + p_amount_cad,
        distortions_resolved = distortions_resolved + 1,
        updated_at = NOW();

    -- Enregistrer la transaction
    INSERT INTO restitution_transactions (
        distortion_id, tx_type, amount_cad, description
    ) VALUES (
        p_distortion_id, 'allocation', p_amount_cad,
        'Allocation automatique vers les fonds de bien commun'
    );

    -- Mettre à jour stats
    UPDATE rrs_config
    SET total_redistributed_cad = total_redistributed_cad + p_amount_cad,
        updated_at = NOW();
END;
$$;

-- Dashboard RRS
CREATE OR REPLACE FUNCTION get_rrs_dashboard()
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_config RECORD;
    v_funds RECORD;
    v_stats JSONB;
BEGIN
    SELECT * INTO v_config FROM rrs_config LIMIT 1;
    SELECT * INTO v_funds FROM restitution_funds LIMIT 1;

    -- Statistiques par statut
    SELECT jsonb_build_object(
        'detected', COUNT(*) FILTER (WHERE status = 'detected'),
        'analyzing', COUNT(*) FILTER (WHERE status = 'analyzing'),
        'verified', COUNT(*) FILTER (WHERE status = 'verified'),
        'mediation_offered', COUNT(*) FILTER (WHERE status = 'mediation_offered'),
        'mediation_accepted', COUNT(*) FILTER (WHERE status = 'mediation_accepted'),
        'mediation_refused', COUNT(*) FILTER (WHERE status = 'mediation_refused'),
        'exposed', COUNT(*) FILTER (WHERE status = 'exposed'),
        'recovered', COUNT(*) FILTER (WHERE status = 'recovered'),
        'redistributed', COUNT(*) FILTER (WHERE status = 'redistributed')
    ) INTO v_stats
    FROM economic_distortions;

    RETURN jsonb_build_object(
        'success', true,
        'global_stats', jsonb_build_object(
            'total_detected_cad', v_config.total_detected_cad,
            'total_recovered_cad', v_config.total_recovered_cad,
            'total_redistributed_cad', v_config.total_redistributed_cad,
            'recovery_rate', CASE WHEN v_config.total_detected_cad > 0
                THEN round((v_config.total_recovered_cad / v_config.total_detected_cad * 100)::numeric, 2)
                ELSE 0 END
        ),
        'distortion_stats', v_stats,
        'common_funds', jsonb_build_object(
            'total_balance', v_funds.total_balance_cad,
            'energy_infrastructure', v_funds.energy_infrastructure_cad,
            'water_access', v_funds.water_access_cad,
            'grid_fee_reduction', v_funds.grid_fee_reduction_cad,
            'justice_dividend', v_funds.justice_dividend_cad
        ),
        'isolated_entities', (SELECT COUNT(*) FROM isolated_entities WHERE lifted_at IS NULL),
        'pending_mediations', (
            SELECT COUNT(*) FROM economic_distortions
            WHERE status = 'mediation_offered' AND mediation_deadline > NOW()
        )
    );
END;
$$;

-- Enregistrer un snapshot de migration de valeur
CREATE OR REPLACE FUNCTION record_value_migration_snapshot(
    p_old_world_fiat_usd NUMERIC,
    p_old_world_debt_usd NUMERIC,
    p_grid_land_value NUMERIC,
    p_grid_infrastructure_value NUMERIC,
    p_grid_technology_value NUMERIC,
    p_grid_ur_backed_value NUMERIC
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_old_world_real NUMERIC;
    v_grid_total NUMERIC;
    v_migration_index NUMERIC;
BEGIN
    -- Calculer la valeur réelle de l'ancien monde (fiat - dette)
    v_old_world_real := GREATEST(0, p_old_world_fiat_usd - p_old_world_debt_usd);

    -- Calculer le total Grid
    v_grid_total := p_grid_land_value + p_grid_infrastructure_value +
                    p_grid_technology_value + p_grid_ur_backed_value;

    -- Indice de migration (% de valeur dans la Grid)
    v_migration_index := CASE
        WHEN (v_old_world_real + v_grid_total) > 0
        THEN round((v_grid_total / (v_old_world_real + v_grid_total) * 100)::numeric, 2)
        ELSE 0
    END;

    -- Insérer le snapshot
    INSERT INTO value_migration_snapshots (
        snapshot_date,
        old_world_fiat_value_usd, old_world_debt_usd, old_world_real_assets_usd,
        grid_land_value_cad, grid_infrastructure_value_cad,
        grid_technology_value_cad, grid_ur_backed_value_cad,
        migration_index,
        old_world_health_index,
        grid_health_index
    ) VALUES (
        CURRENT_DATE,
        p_old_world_fiat_usd, p_old_world_debt_usd, v_old_world_real,
        p_grid_land_value, p_grid_infrastructure_value,
        p_grid_technology_value, p_grid_ur_backed_value,
        v_migration_index,
        GREATEST(0, 100 - (p_old_world_debt_usd / NULLIF(p_old_world_fiat_usd, 0) * 100)),
        LEAST(100, v_grid_total / 1000000)  -- Santé basée sur les actifs
    )
    ON CONFLICT (snapshot_date) DO UPDATE
    SET old_world_fiat_value_usd = EXCLUDED.old_world_fiat_value_usd,
        old_world_debt_usd = EXCLUDED.old_world_debt_usd,
        grid_land_value_cad = EXCLUDED.grid_land_value_cad,
        migration_index = EXCLUDED.migration_index;

    RETURN jsonb_build_object(
        'success', true,
        'migration_index', v_migration_index,
        'grid_total_value', v_grid_total,
        'old_world_real_value', v_old_world_real
    );
END;
$$;

-- ═══════════════════════════════════════════════════════════════════════════════
-- SECTION 4: VUES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Vue des distorsions actives avec détails
CREATE OR REPLACE VIEW active_distortions_view AS
SELECT
    d.id,
    d.codename,
    d.category,
    d.status,
    d.estimated_amount_cad,
    d.recovered_amount_cad,
    d.certainty_level,
    d.certainty_score,
    d.impact_score,
    d.mediation_offered_at,
    d.mediation_deadline,
    d.mediation_response,
    CASE
        WHEN d.mediation_deadline IS NOT NULL AND d.mediation_deadline > NOW()
        THEN d.mediation_deadline - NOW()
        ELSE NULL
    END as time_remaining,
    d.created_at,
    d.updated_at
FROM economic_distortions d
WHERE d.status NOT IN ('archived', 'redistributed')
ORDER BY d.impact_score DESC, d.estimated_amount_cad DESC;

-- Vue du tableau de bord de migration
CREATE OR REPLACE VIEW value_migration_dashboard AS
SELECT
    snapshot_date,
    old_world_fiat_value_usd,
    old_world_debt_usd,
    (grid_land_value_cad + grid_infrastructure_value_cad +
     grid_technology_value_cad + grid_ur_backed_value_cad) as grid_total_value_cad,
    migration_index,
    old_world_health_index,
    grid_health_index,
    LAG(migration_index) OVER (ORDER BY snapshot_date) as previous_migration_index,
    migration_index - LAG(migration_index) OVER (ORDER BY snapshot_date) as migration_change
FROM value_migration_snapshots
ORDER BY snapshot_date DESC;

-- ═══════════════════════════════════════════════════════════════════════════════
-- SECTION 5: POLITIQUES RLS
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE economic_distortions ENABLE ROW LEVEL SECURITY;
ALTER TABLE investigation_dossiers ENABLE ROW LEVEL SECURITY;
ALTER TABLE mediation_communications ENABLE ROW LEVEL SECURITY;
ALTER TABLE restitution_funds ENABLE ROW LEVEL SECURITY;
ALTER TABLE restitution_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE allocation_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE allocation_vote_ballots ENABLE ROW LEVEL SECURITY;
ALTER TABLE isolated_entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE value_migration_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE justice_dividends ENABLE ROW LEVEL SECURITY;

-- Gardiens (niveau 6+) peuvent voir les distorsions
CREATE POLICY "Guardians can view distortions"
ON economic_distortions FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM sovereignty_assignments sa
        WHERE sa.user_id = auth.uid()
        AND sa.sovereignty_level >= 6
    )
);

-- Souverains peuvent modifier
CREATE POLICY "Sovereigns can modify distortions"
ON economic_distortions FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM sovereignty_assignments sa
        WHERE sa.user_id = auth.uid()
        AND sa.sovereignty_level = 7
    )
);

-- Initiés (niveau 3+) peuvent voir les fonds
CREATE POLICY "Initiates can view funds"
ON restitution_funds FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM sovereignty_assignments sa
        WHERE sa.user_id = auth.uid()
        AND sa.sovereignty_level >= 3
    )
);

-- Tous les membres peuvent voter
CREATE POLICY "Members can vote on allocation"
ON allocation_vote_ballots FOR INSERT
WITH CHECK (
    auth.uid() = voter_id
    AND EXISTS (
        SELECT 1 FROM allocation_votes av
        WHERE av.id = vote_id
        AND av.status = 'open'
        AND NOW() BETWEEN av.voting_starts_at AND av.voting_ends_at
    )
);

-- Migration visible par tous les membres
CREATE POLICY "Members can view migration"
ON value_migration_snapshots FOR SELECT
USING (auth.uid() IS NOT NULL);

-- Utilisateurs voient leurs dividendes
CREATE POLICY "Users can view own dividends"
ON justice_dividends FOR SELECT
USING (user_id = auth.uid());

-- ═══════════════════════════════════════════════════════════════════════════════
-- SECTION 6: TRIGGERS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_rrs_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_distortions_timestamp
BEFORE UPDATE ON economic_distortions
FOR EACH ROW EXECUTE FUNCTION update_rrs_timestamp();

CREATE TRIGGER trg_dossiers_timestamp
BEFORE UPDATE ON investigation_dossiers
FOR EACH ROW EXECUTE FUNCTION update_rrs_timestamp();

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN DU MODULE RRS
-- ═══════════════════════════════════════════════════════════════════════════════
