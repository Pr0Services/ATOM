-- ============================================================================
-- MOTEUR D'EXFILTRATION ARCHE-ALPHA
-- Asset Exfiltration Engine & Systemic Risk Monitor
-- ============================================================================
-- Ce module gère la conversion stratégique des actifs fiat vers:
-- 1. Monnaie souveraine (Unités de Résonance)
-- 2. Actifs tangibles (terrains, infrastructures, équipements)
-- 3. Réserves Hedera sécurisées
-- ============================================================================

-- ============================================================================
-- PARTIE 1: FOND D'EXFILTRATION ARCHE-ALPHA
-- ============================================================================

-- Configuration du fond d'exfiltration (singleton)
CREATE TABLE IF NOT EXISTS exfiltration_fund (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Réserves en monnaie fiat (avant conversion)
    fiat_reserves_cad DECIMAL(18, 2) DEFAULT 0,
    fiat_reserves_usd DECIMAL(18, 2) DEFAULT 0,
    fiat_reserves_eur DECIMAL(18, 2) DEFAULT 0,

    -- Réserves converties en UR
    ur_reserves DECIMAL(18, 6) DEFAULT 0,

    -- Actifs tangibles valorisés
    tangible_assets_value DECIMAL(18, 2) DEFAULT 0,

    -- Paramètres de vitesse d'extraction
    extraction_speed DECIMAL(5, 2) DEFAULT 10.00, -- % par mois
    min_fiat_buffer DECIMAL(18, 2) DEFAULT 50000, -- Tampon de sécurité

    -- Seuils d'alerte
    inflation_trigger_threshold DECIMAL(5, 2) DEFAULT 8.00, -- % inflation déclencheur
    bank_risk_trigger_threshold DECIMAL(5, 2) DEFAULT 70.00, -- Score risque bancaire

    -- Mode d'urgence
    emergency_mode BOOLEAN DEFAULT FALSE,
    emergency_extraction_speed DECIMAL(5, 2) DEFAULT 100.00, -- Évacuation totale

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Contrainte singleton
    CONSTRAINT single_fund CHECK (id IS NOT NULL)
);

-- Types d'actifs tangibles
CREATE TYPE tangible_asset_type AS ENUM (
    'land',              -- Terrains
    'building',          -- Bâtiments/Infrastructures
    'solar_infrastructure', -- Panneaux solaires, batteries
    'technology',        -- Équipement technologique
    'vehicle',           -- Véhicules
    'equipment',         -- Équipement divers
    'precious_metals',   -- Métaux précieux
    'cryptocurrency',    -- Crypto hors Hedera
    'inventory'          -- Inventaire matériel
);

-- Registre des actifs tangibles
CREATE TABLE IF NOT EXISTS tangible_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Identification
    asset_type tangible_asset_type NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Localisation (pour terrains/bâtiments)
    address TEXT,
    coordinates POINT, -- lat/long
    region VARCHAR(100),

    -- Valeur
    acquisition_cost DECIMAL(18, 2) NOT NULL,
    acquisition_date DATE NOT NULL,
    current_value DECIMAL(18, 2) NOT NULL,
    last_valuation_date DATE DEFAULT CURRENT_DATE,

    -- Statut
    status VARCHAR(50) DEFAULT 'active',
    ownership_percentage DECIMAL(5, 2) DEFAULT 100.00,

    -- Documents
    legal_documents JSONB DEFAULT '[]',
    photos JSONB DEFAULT '[]',

    -- Métadonnées spécifiques par type
    metadata JSONB DEFAULT '{}',
    -- Pour terrains: superficie, zonage, accès eau/électricité
    -- Pour solar: capacité kWh, rendement, garantie
    -- Pour véhicules: marque, modèle, immatriculation

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour recherche géographique
CREATE INDEX IF NOT EXISTS idx_tangible_assets_region ON tangible_assets(region);
CREATE INDEX IF NOT EXISTS idx_tangible_assets_type ON tangible_assets(asset_type);

-- Transactions d'exfiltration
CREATE TYPE exfiltration_action AS ENUM (
    'deposit_fiat',      -- Dépôt fiat dans le fond
    'convert_to_ur',     -- Conversion fiat → UR
    'acquire_asset',     -- Achat d'actif tangible
    'sell_asset',        -- Vente d'actif tangible
    'emergency_extract', -- Extraction d'urgence
    'debt_buyback',      -- Rachat de dette membre
    'dividend_payout'    -- Distribution aux membres
);

CREATE TABLE IF NOT EXISTS exfiltration_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Type d'action
    action exfiltration_action NOT NULL,

    -- Montants
    fiat_amount DECIMAL(18, 2),
    fiat_currency VARCHAR(3) DEFAULT 'CAD',
    ur_amount DECIMAL(18, 6),

    -- Référence à l'actif (si applicable)
    tangible_asset_id UUID REFERENCES tangible_assets(id),

    -- Membre concerné (si applicable)
    member_id UUID REFERENCES auth.users(id),

    -- Justification
    reason TEXT,
    approved_by UUID REFERENCES auth.users(id),

    -- Taux de conversion utilisé
    conversion_rate DECIMAL(18, 6),

    -- Statut
    status VARCHAR(50) DEFAULT 'pending',
    executed_at TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 2: MONITEUR DE RISQUE SYSTÉMIQUE
-- ============================================================================

-- Sources de données économiques surveillées
CREATE TABLE IF NOT EXISTS risk_data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- 'api', 'scraper', 'manual'
    url TEXT,

    -- Configuration
    update_frequency_hours INTEGER DEFAULT 24,
    last_update TIMESTAMPTZ,

    -- Statut
    is_active BOOLEAN DEFAULT TRUE,
    reliability_score DECIMAL(3, 2) DEFAULT 0.80,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Types d'indicateurs de risque
CREATE TYPE risk_indicator_type AS ENUM (
    'inflation_rate',
    'interest_rate',
    'bank_stability',
    'currency_volatility',
    'market_index',
    'unemployment',
    'debt_to_gdp',
    'housing_bubble',
    'supply_chain',
    'geopolitical'
);

-- Indicateurs de risque systémique
CREATE TABLE IF NOT EXISTS systemic_risk_indicators (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    indicator_type risk_indicator_type NOT NULL,
    region VARCHAR(100) DEFAULT 'global',

    -- Valeur actuelle
    current_value DECIMAL(18, 6) NOT NULL,
    previous_value DECIMAL(18, 6),

    -- Seuils
    warning_threshold DECIMAL(18, 6),
    critical_threshold DECIMAL(18, 6),

    -- Score de risque normalisé (0-100)
    risk_score DECIMAL(5, 2) DEFAULT 0,

    -- Tendance
    trend VARCHAR(20), -- 'rising', 'stable', 'falling'
    trend_velocity DECIMAL(8, 4), -- Vitesse de changement

    -- Source
    data_source_id UUID REFERENCES risk_data_sources(id),

    -- Timestamps
    measured_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour requêtes temporelles
CREATE INDEX IF NOT EXISTS idx_risk_indicators_time ON systemic_risk_indicators(measured_at DESC);
CREATE INDEX IF NOT EXISTS idx_risk_indicators_type ON systemic_risk_indicators(indicator_type);

-- Historique des scores de risque agrégés
CREATE TABLE IF NOT EXISTS risk_score_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Score global
    global_risk_score DECIMAL(5, 2) NOT NULL,

    -- Scores par catégorie
    financial_risk DECIMAL(5, 2),
    currency_risk DECIMAL(5, 2),
    political_risk DECIMAL(5, 2),
    supply_risk DECIMAL(5, 2),

    -- Recommandation générée
    recommendation TEXT,
    recommended_extraction_percentage DECIMAL(5, 2),

    -- Alerte déclenchée?
    alert_triggered BOOLEAN DEFAULT FALSE,
    alert_level VARCHAR(20), -- 'info', 'warning', 'critical', 'emergency'

    -- Timestamp
    calculated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Alertes de risque
CREATE TABLE IF NOT EXISTS risk_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    alert_level VARCHAR(20) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,

    -- Indicateur déclencheur
    trigger_indicator_id UUID REFERENCES systemic_risk_indicators(id),
    trigger_value DECIMAL(18, 6),

    -- Action recommandée
    recommended_action TEXT,
    auto_action_enabled BOOLEAN DEFAULT FALSE,

    -- Statut
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by UUID REFERENCES auth.users(id),
    acknowledged_at TIMESTAMPTZ,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- PARTIE 3: RACHAT DE DETTES MEMBRES
-- ============================================================================

-- Types de dettes
CREATE TYPE debt_type AS ENUM (
    'mortgage',      -- Hypothèque
    'car_loan',      -- Prêt auto
    'student_loan',  -- Prêt étudiant
    'credit_card',   -- Carte de crédit
    'personal_loan', -- Prêt personnel
    'business_loan', -- Prêt commercial
    'other'
);

-- Dettes des membres (pour rachat potentiel)
CREATE TABLE IF NOT EXISTS member_debts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    member_id UUID NOT NULL REFERENCES auth.users(id),

    -- Détails de la dette
    debt_type debt_type NOT NULL,
    creditor_name VARCHAR(255) NOT NULL,
    original_amount DECIMAL(18, 2) NOT NULL,
    current_balance DECIMAL(18, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    monthly_payment DECIMAL(18, 2),

    -- Potentiel de rachat
    buyback_eligible BOOLEAN DEFAULT FALSE,
    estimated_discount DECIMAL(5, 2), -- % de rabais possible
    buyback_priority INTEGER DEFAULT 0,

    -- Statut
    status VARCHAR(50) DEFAULT 'active',
    -- 'active', 'buyback_pending', 'bought_back', 'converted_to_ur'

    -- Si racheté
    buyback_amount DECIMAL(18, 2),
    buyback_date DATE,
    ur_conversion_amount DECIMAL(18, 6),
    ur_interest_rate DECIMAL(5, 2) DEFAULT 0, -- Généralement 0%

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_member_debts_member ON member_debts(member_id);
CREATE INDEX IF NOT EXISTS idx_member_debts_status ON member_debts(status);

-- ============================================================================
-- PARTIE 4: FONCTIONS D'EXFILTRATION
-- ============================================================================

-- Calculer le score de risque global
CREATE OR REPLACE FUNCTION calculate_global_risk_score()
RETURNS DECIMAL AS $$
DECLARE
    v_score DECIMAL(5, 2);
    v_financial DECIMAL(5, 2);
    v_currency DECIMAL(5, 2);
    v_political DECIMAL(5, 2);
BEGIN
    -- Moyenne pondérée des indicateurs récents
    SELECT
        COALESCE(AVG(CASE WHEN indicator_type IN ('inflation_rate', 'interest_rate', 'bank_stability')
                         THEN risk_score END), 50) INTO v_financial
    FROM systemic_risk_indicators
    WHERE measured_at > NOW() - INTERVAL '7 days';

    SELECT
        COALESCE(AVG(CASE WHEN indicator_type = 'currency_volatility'
                         THEN risk_score END), 50) INTO v_currency
    FROM systemic_risk_indicators
    WHERE measured_at > NOW() - INTERVAL '7 days';

    SELECT
        COALESCE(AVG(CASE WHEN indicator_type = 'geopolitical'
                         THEN risk_score END), 50) INTO v_political
    FROM systemic_risk_indicators
    WHERE measured_at > NOW() - INTERVAL '7 days';

    -- Score global pondéré
    v_score := (v_financial * 0.5) + (v_currency * 0.3) + (v_political * 0.2);

    -- Enregistrer dans l'historique
    INSERT INTO risk_score_history (
        global_risk_score, financial_risk, currency_risk, political_risk,
        recommended_extraction_percentage,
        alert_triggered, alert_level
    ) VALUES (
        v_score, v_financial, v_currency, v_political,
        CASE
            WHEN v_score >= 80 THEN 50.00
            WHEN v_score >= 60 THEN 30.00
            WHEN v_score >= 40 THEN 20.00
            ELSE 10.00
        END,
        v_score >= 60,
        CASE
            WHEN v_score >= 90 THEN 'emergency'
            WHEN v_score >= 80 THEN 'critical'
            WHEN v_score >= 60 THEN 'warning'
            ELSE 'info'
        END
    );

    RETURN v_score;
END;
$$ LANGUAGE plpgsql;

-- Exécuter une transaction d'exfiltration
CREATE OR REPLACE FUNCTION execute_exfiltration(
    p_action exfiltration_action,
    p_fiat_amount DECIMAL DEFAULT NULL,
    p_fiat_currency VARCHAR(3) DEFAULT 'CAD',
    p_ur_amount DECIMAL DEFAULT NULL,
    p_asset_id UUID DEFAULT NULL,
    p_member_id UUID DEFAULT NULL,
    p_reason TEXT DEFAULT NULL,
    p_approved_by UUID DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_transaction_id UUID;
    v_conversion_rate DECIMAL(18, 6);
    v_fund exfiltration_fund%ROWTYPE;
BEGIN
    -- Récupérer l'état du fond
    SELECT * INTO v_fund FROM exfiltration_fund LIMIT 1;

    -- Obtenir le taux de conversion actuel
    SELECT (value->>'rate')::DECIMAL INTO v_conversion_rate
    FROM economic_settings
    WHERE key = 'ur_exchange_rate'
    LIMIT 1;

    IF v_conversion_rate IS NULL THEN
        v_conversion_rate := 1.0;
    END IF;

    -- Créer la transaction
    INSERT INTO exfiltration_transactions (
        action, fiat_amount, fiat_currency, ur_amount,
        tangible_asset_id, member_id, reason, approved_by,
        conversion_rate, status, executed_at
    ) VALUES (
        p_action, p_fiat_amount, p_fiat_currency, p_ur_amount,
        p_asset_id, p_member_id, p_reason, p_approved_by,
        v_conversion_rate, 'executed', NOW()
    )
    RETURNING id INTO v_transaction_id;

    -- Mettre à jour le fond selon l'action
    CASE p_action
        WHEN 'deposit_fiat' THEN
            UPDATE exfiltration_fund
            SET fiat_reserves_cad = fiat_reserves_cad +
                CASE WHEN p_fiat_currency = 'CAD' THEN p_fiat_amount ELSE 0 END,
                fiat_reserves_usd = fiat_reserves_usd +
                CASE WHEN p_fiat_currency = 'USD' THEN p_fiat_amount ELSE 0 END,
                fiat_reserves_eur = fiat_reserves_eur +
                CASE WHEN p_fiat_currency = 'EUR' THEN p_fiat_amount ELSE 0 END,
                updated_at = NOW();

        WHEN 'convert_to_ur' THEN
            UPDATE exfiltration_fund
            SET fiat_reserves_cad = fiat_reserves_cad -
                CASE WHEN p_fiat_currency = 'CAD' THEN p_fiat_amount ELSE 0 END,
                ur_reserves = ur_reserves + (p_fiat_amount * v_conversion_rate),
                updated_at = NOW();

        WHEN 'acquire_asset' THEN
            UPDATE exfiltration_fund
            SET fiat_reserves_cad = fiat_reserves_cad - p_fiat_amount,
                tangible_assets_value = tangible_assets_value + p_fiat_amount,
                updated_at = NOW();

        WHEN 'emergency_extract' THEN
            -- Convertir tout le fiat restant en UR
            UPDATE exfiltration_fund
            SET ur_reserves = ur_reserves +
                ((fiat_reserves_cad + fiat_reserves_usd + fiat_reserves_eur) * v_conversion_rate),
                fiat_reserves_cad = 0,
                fiat_reserves_usd = 0,
                fiat_reserves_eur = 0,
                emergency_mode = TRUE,
                updated_at = NOW();
    END CASE;

    RETURN v_transaction_id;
END;
$$ LANGUAGE plpgsql;

-- Calculer la recommandation d'exfiltration
CREATE OR REPLACE FUNCTION get_exfiltration_recommendation()
RETURNS JSONB AS $$
DECLARE
    v_risk_score DECIMAL;
    v_fund exfiltration_fund%ROWTYPE;
    v_recommendation JSONB;
BEGIN
    v_risk_score := calculate_global_risk_score();
    SELECT * INTO v_fund FROM exfiltration_fund LIMIT 1;

    v_recommendation := jsonb_build_object(
        'timestamp', NOW(),
        'global_risk_score', v_risk_score,
        'current_reserves', jsonb_build_object(
            'fiat_cad', v_fund.fiat_reserves_cad,
            'fiat_usd', v_fund.fiat_reserves_usd,
            'fiat_eur', v_fund.fiat_reserves_eur,
            'ur', v_fund.ur_reserves,
            'tangible_assets', v_fund.tangible_assets_value
        ),
        'alert_level', CASE
            WHEN v_risk_score >= 90 THEN 'EMERGENCY'
            WHEN v_risk_score >= 80 THEN 'CRITICAL'
            WHEN v_risk_score >= 60 THEN 'WARNING'
            ELSE 'STABLE'
        END,
        'recommended_action', CASE
            WHEN v_risk_score >= 90 THEN 'ÉVACUATION TOTALE - Convertir 100% des réserves fiat immédiatement'
            WHEN v_risk_score >= 80 THEN 'EXTRACTION ACCÉLÉRÉE - Convertir 50% des réserves fiat'
            WHEN v_risk_score >= 60 THEN 'EXTRACTION PRÉVENTIVE - Convertir 30% des réserves fiat'
            ELSE 'EXTRACTION STANDARD - Maintenir le rythme de ' || v_fund.extraction_speed || '% par mois'
        END,
        'suggested_targets', CASE
            WHEN v_risk_score >= 80 THEN jsonb_build_array(
                'Finaliser acquisitions foncières en cours',
                'Augmenter réserves UR sur Hedera',
                'Convertir comptes bancaires secondaires'
            )
            WHEN v_risk_score >= 60 THEN jsonb_build_array(
                'Accélérer conversion vers UR',
                'Identifier nouvelles opportunités foncières',
                'Racheter dettes membres prioritaires'
            )
            ELSE jsonb_build_array(
                'Maintenir rythme d''extraction',
                'Surveiller indicateurs',
                'Optimiser rendement temporaire des réserves fiat'
            )
        END
    );

    RETURN v_recommendation;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PARTIE 5: ROW LEVEL SECURITY
-- ============================================================================

ALTER TABLE exfiltration_fund ENABLE ROW LEVEL SECURITY;
ALTER TABLE tangible_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE exfiltration_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_data_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE systemic_risk_indicators ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_debts ENABLE ROW LEVEL SECURITY;

-- Politiques pour administrateurs (accès complet)
CREATE POLICY admin_exfiltration_fund ON exfiltration_fund
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign'))
    );

CREATE POLICY admin_tangible_assets ON tangible_assets
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign'))
    );

CREATE POLICY admin_exfiltration_transactions ON exfiltration_transactions
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign'))
    );

-- Les membres peuvent voir leurs propres dettes
CREATE POLICY member_own_debts ON member_debts
    FOR SELECT USING (member_id = auth.uid());

CREATE POLICY admin_all_debts ON member_debts
    FOR ALL USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid() AND role IN ('admin', 'sovereign'))
    );

-- Indicateurs de risque: lecture pour tous les membres vérifiés
CREATE POLICY read_risk_indicators ON systemic_risk_indicators
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid())
    );

CREATE POLICY read_risk_alerts ON risk_alerts
    FOR SELECT USING (
        EXISTS (SELECT 1 FROM user_roles WHERE user_id = auth.uid())
    );

-- ============================================================================
-- PARTIE 6: DONNÉES INITIALES
-- ============================================================================

-- Initialiser le fond d'exfiltration
INSERT INTO exfiltration_fund (
    fiat_reserves_cad,
    extraction_speed,
    min_fiat_buffer,
    inflation_trigger_threshold,
    bank_risk_trigger_threshold
) VALUES (
    0,
    10.00,  -- 10% par mois
    50000,  -- 50k CAD tampon
    8.00,   -- 8% inflation trigger
    70.00   -- 70% bank risk trigger
) ON CONFLICT DO NOTHING;

-- Sources de données initiales
INSERT INTO risk_data_sources (name, source_type, url, update_frequency_hours) VALUES
    ('Banque du Canada', 'api', 'https://www.bankofcanada.ca/rates/', 24),
    ('Statistique Canada - IPC', 'api', 'https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810000401', 168),
    ('Federal Reserve - US', 'api', 'https://fred.stlouisfed.org/series/FEDFUNDS', 24),
    ('S&P 500 Index', 'api', 'https://finance.yahoo.com/quote/%5EGSPC', 1),
    ('Taux de Change CAD/USD', 'api', 'https://www.x-rates.com/calculator/', 1),
    ('Indice VIX (Volatilité)', 'api', 'https://finance.yahoo.com/quote/%5EVIX', 1)
ON CONFLICT DO NOTHING;

-- Indicateurs initiaux (valeurs de référence)
INSERT INTO systemic_risk_indicators (indicator_type, region, current_value, warning_threshold, critical_threshold, risk_score) VALUES
    ('inflation_rate', 'canada', 3.50, 5.00, 8.00, 35),
    ('interest_rate', 'canada', 5.00, 6.00, 8.00, 50),
    ('bank_stability', 'canada', 85.00, 70.00, 50.00, 15),
    ('currency_volatility', 'cad_usd', 2.50, 5.00, 10.00, 25),
    ('inflation_rate', 'usa', 3.20, 5.00, 8.00, 32),
    ('geopolitical', 'global', 45.00, 60.00, 80.00, 45)
ON CONFLICT DO NOTHING;

COMMIT;
