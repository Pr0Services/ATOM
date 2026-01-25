-- ═══════════════════════════════════════════════════════════════════════════
-- AT·OM — USER BIOMETRICS SCHEMA
-- ═══════════════════════════════════════════════════════════════════════════
-- Table pour stocker les mesures biométriques M, P, I, Po
-- et le tokenId Hedera correspondant
-- ═══════════════════════════════════════════════════════════════════════════
--
-- INSTRUCTIONS:
-- 1. Aller sur Supabase Dashboard > SQL Editor
-- 2. Copier-coller ce script
-- 3. Exécuter
-- ═══════════════════════════════════════════════════════════════════════════

-- Créer la table user_biometrics
CREATE TABLE IF NOT EXISTS user_biometrics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Identifiant utilisateur
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    wallet_address TEXT,

    -- Mesures Biométriques (M, P, I, Po)
    measure_m DECIMAL(18, 8) NOT NULL,        -- Masse / Matière
    measure_p DECIMAL(18, 8) NOT NULL,        -- Puissance / Potentiel
    measure_i DECIMAL(18, 8) NOT NULL,        -- Intensité / Information
    measure_po DECIMAL(18, 8) NOT NULL,       -- Position / Polarité

    -- Signature Composite
    biometric_hash TEXT NOT NULL,             -- Hash SHA-256 de M+P+I+Po
    resonance_frequency DECIMAL(10, 4),       -- Fréquence de résonance calculée

    -- Lien Hedera
    hedera_token_id TEXT,                     -- Token ID UR associé
    hedera_account_id TEXT,                   -- Compte Hedera lié
    hedera_tx_id TEXT,                        -- Transaction de création

    -- Métadonnées
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    verified_at TIMESTAMP WITH TIME ZONE,

    -- Status
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'minted', 'active', 'revoked'))
);

-- Index pour recherches rapides
CREATE INDEX IF NOT EXISTS idx_user_biometrics_user_id ON user_biometrics(user_id);
CREATE INDEX IF NOT EXISTS idx_user_biometrics_wallet ON user_biometrics(wallet_address);
CREATE INDEX IF NOT EXISTS idx_user_biometrics_hedera ON user_biometrics(hedera_account_id);
CREATE INDEX IF NOT EXISTS idx_user_biometrics_hash ON user_biometrics(biometric_hash);
CREATE INDEX IF NOT EXISTS idx_user_biometrics_status ON user_biometrics(status);

-- Fonction de mise à jour automatique du timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour mise à jour automatique
DROP TRIGGER IF EXISTS trigger_update_biometrics_timestamp ON user_biometrics;
CREATE TRIGGER trigger_update_biometrics_timestamp
    BEFORE UPDATE ON user_biometrics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Row Level Security (RLS)
ALTER TABLE user_biometrics ENABLE ROW LEVEL SECURITY;

-- Politique: Les utilisateurs ne voient que leurs propres données
CREATE POLICY "Users can view own biometrics"
    ON user_biometrics
    FOR SELECT
    USING (auth.uid() = user_id);

-- Politique: Les utilisateurs peuvent insérer leurs propres données
CREATE POLICY "Users can insert own biometrics"
    ON user_biometrics
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Politique: Les utilisateurs peuvent mettre à jour leurs propres données
CREATE POLICY "Users can update own biometrics"
    ON user_biometrics
    FOR UPDATE
    USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════
-- VÉRIFICATION
-- ═══════════════════════════════════════════════════════════════════════════
-- Exécuter cette requête pour vérifier que la table est créée:
-- SELECT * FROM information_schema.tables WHERE table_name = 'user_biometrics';
-- ═══════════════════════════════════════════════════════════════════════════
