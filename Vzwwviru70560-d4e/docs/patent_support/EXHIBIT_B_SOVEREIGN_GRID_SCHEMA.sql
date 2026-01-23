-- ═══════════════════════════════════════════════════════════════════════════════
--
--       ███████╗ ██████╗ ██╗   ██╗██╗   ██╗███████╗██████╗  █████╗ ██╗███╗   ██╗
--       ██╔════╝██╔═══██╗██║   ██║██║   ██║██╔════╝██╔══██╗██╔══██╗██║████╗  ██║
--       ███████╗██║   ██║██║   ██║██║   ██║█████╗  ██████╔╝███████║██║██╔██╗ ██║
--       ╚════██║██║   ██║╚██╗ ██╔╝╚██╗ ██╔╝██╔══╝  ██╔══██╗██╔══██║██║██║╚██╗██║
--       ███████║╚██████╔╝ ╚████╔╝  ╚████╔╝ ███████╗██║  ██║██║  ██║██║██║ ╚████║
--       ╚══════╝ ╚═════╝   ╚═══╝    ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
--
--              ARCHITECTURE SOUVERAINE - GRID & RELAIS ENERGETIQUES
--                           AT.OM / CHE.NU V76
--
--   TABLES:
--   ├── members_grid: Membres fondateurs et leur resonance
--   ├── sovereign_databases: Provisionnement DB par membre
--   ├── resource_relays: Distribution Stripe Connect
--   └── admin_setup_status: Monitoring du Guide Admin
--
--   FREQUENCES:
--   444 Hz = Heartbeat (Coeur de l'Arche)
--   999 Hz = Source (Frequence Souveraine)
--
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. TABLE DES MEMBRES DE LA GRID (Extension Energetique)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS members_grid (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE,

  -- Role dans la Grid
  role_id TEXT DEFAULT 'FOUNDER' CHECK (role_id IN (
    'FOUNDER',      -- Membre Fondateur (99$/mois)
    'CITOYEN',      -- Membre Citoyen (gratuit)
    'SOVEREIGN'     -- Souverain (acces total)
  )),

  -- Identite
  full_name TEXT,
  email TEXT UNIQUE,

  -- Signature Energetique
  energy_signature TEXT DEFAULT '999Hz' CHECK (energy_signature IN (
    '111Hz', '222Hz', '333Hz', '444Hz', '528Hz',
    '639Hz', '741Hz', '852Hz', '963Hz', '999Hz'
  )),

  -- Score de Resonance (0-100)
  -- Mesure l'alignement du membre avec la Grid
  resonance_score DECIMAL(5,2) DEFAULT 0.00 CHECK (
    resonance_score >= 0 AND resonance_score <= 100
  ),

  -- Statut d'activation
  is_active BOOLEAN DEFAULT FALSE,
  activation_date TIMESTAMP WITH TIME ZONE,

  -- Metadonnees
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. TABLE DE PROVISIONNEMENT DES BASES DE DONNEES SOUVERAINES
-- ═══════════════════════════════════════════════════════════════════════════════
-- Chaque membre fondateur peut avoir sa propre instance de base de donnees
-- isolee pour garantir la souverainete de ses donnees

CREATE TABLE IF NOT EXISTS sovereign_databases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  member_id UUID REFERENCES members_grid(id) ON DELETE CASCADE,

  -- Configuration de la base
  db_name TEXT UNIQUE NOT NULL,
  db_region TEXT DEFAULT 'nyc1',  -- Region DigitalOcean/Supabase

  -- Statut de provisionnement
  db_status TEXT DEFAULT 'PENDING' CHECK (db_status IN (
    'PENDING',      -- En attente de creation
    'PROVISIONING', -- En cours de creation
    'ACTIVE',       -- Base active et operationnelle
    'SUSPENDED',    -- Suspendue (paiement manque)
    'ARCHIVED'      -- Archivee (donnees conservees)
  )),

  -- Connection (chiffree en production)
  connection_string_encrypted TEXT,
  service_role_key_encrypted TEXT,

  -- Quota de tokens (credits API)
  allocated_tokens BIGINT DEFAULT 500000,  -- 500K pour fondateurs
  used_tokens BIGINT DEFAULT 0,
  tokens_reset_date TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '1 month'),

  -- Metriques
  storage_used_mb INTEGER DEFAULT 0,
  last_activity_at TIMESTAMP WITH TIME ZONE,

  -- Metadonnees
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. TABLE DES RELAIS DE DISTRIBUTION (STRIPE CONNECT)
-- ═══════════════════════════════════════════════════════════════════════════════
-- Gestion automatique de la redistribution des paiements aux partenaires

CREATE TABLE IF NOT EXISTS resource_relays (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Identification du partenaire
  provider_name TEXT NOT NULL,
  provider_type TEXT DEFAULT 'service' CHECK (provider_type IN (
    'api_provider',     -- OpenRouter, Anthropic, etc.
    'infrastructure',   -- DigitalOcean, Vercel, etc.
    'service',          -- Services tiers
    'founder_reward',   -- Recompenses fondateurs
    'reserve'           -- Reserve de l'Arche
  )),

  -- Stripe Connect
  stripe_account_id TEXT UNIQUE,
  stripe_account_status TEXT DEFAULT 'pending' CHECK (stripe_account_status IN (
    'pending',
    'active',
    'restricted',
    'disabled'
  )),

  -- Distribution automatique
  distribution_percentage DECIMAL(5,2) DEFAULT 0.00 CHECK (
    distribution_percentage >= 0 AND distribution_percentage <= 100
  ),

  -- Comptabilite
  total_distributed DECIMAL(15,2) DEFAULT 0.00,
  last_distribution_at TIMESTAMP WITH TIME ZONE,
  last_distribution_amount DECIMAL(10,2),

  -- Metadonnees
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. TABLE DE MONITORING DU GUIDE ADMIN (WIZARD SETUP)
-- ═══════════════════════════════════════════════════════════════════════════════
-- Table singleton pour suivre l'etat de configuration du systeme

CREATE TABLE IF NOT EXISTS admin_setup_status (
  id INTEGER PRIMARY KEY DEFAULT 1,

  -- ═══════════════════════════════════════════════════════════════════
  -- ETAPE 1: CONNEXIONS API
  -- ═══════════════════════════════════════════════════════════════════
  api_openrouter_connected BOOLEAN DEFAULT FALSE,
  api_openrouter_tested_at TIMESTAMP WITH TIME ZONE,
  api_openrouter_models_available TEXT[],

  api_anthropic_connected BOOLEAN DEFAULT FALSE,
  api_anthropic_tested_at TIMESTAMP WITH TIME ZONE,

  api_stripe_connected BOOLEAN DEFAULT FALSE,
  api_stripe_tested_at TIMESTAMP WITH TIME ZONE,
  api_stripe_connect_enabled BOOLEAN DEFAULT FALSE,

  api_digitalocean_connected BOOLEAN DEFAULT FALSE,
  api_digitalocean_tested_at TIMESTAMP WITH TIME ZONE,

  api_vercel_connected BOOLEAN DEFAULT FALSE,
  api_vercel_tested_at TIMESTAMP WITH TIME ZONE,

  -- ═══════════════════════════════════════════════════════════════════
  -- ETAPE 2: BASE DE DONNEES
  -- ═══════════════════════════════════════════════════════════════════
  db_supabase_connected BOOLEAN DEFAULT FALSE,
  db_supabase_tested_at TIMESTAMP WITH TIME ZONE,
  db_tables_initialized BOOLEAN DEFAULT FALSE,
  db_functions_initialized BOOLEAN DEFAULT FALSE,
  db_rls_enabled BOOLEAN DEFAULT FALSE,

  -- ═══════════════════════════════════════════════════════════════════
  -- ETAPE 3: GRID ENERGETIQUE
  -- ═══════════════════════════════════════════════════════════════════
  grid_initialized BOOLEAN DEFAULT FALSE,
  grid_initial_point_created BOOLEAN DEFAULT FALSE,
  grid_founders_count INTEGER DEFAULT 0,
  grid_active_founders INTEGER DEFAULT 0,

  -- ═══════════════════════════════════════════════════════════════════
  -- ETAPE 4: FLUX FINANCIER
  -- ═══════════════════════════════════════════════════════════════════
  stripe_connect_configured BOOLEAN DEFAULT FALSE,
  distribution_rules_set BOOLEAN DEFAULT FALSE,
  first_payment_received BOOLEAN DEFAULT FALSE,

  -- ═══════════════════════════════════════════════════════════════════
  -- METRIQUES GLOBALES
  -- ═══════════════════════════════════════════════════════════════════
  setup_completion_percentage INTEGER DEFAULT 0,
  current_frequency INTEGER DEFAULT 444,  -- 444 Hz par defaut, 999 Hz quand complet

  -- Metadonnees
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_updated_by UUID REFERENCES auth.users(id),

  -- Contrainte: une seule ligne de configuration maitre
  CONSTRAINT one_row_only CHECK (id = 1)
);

-- Inserer la ligne de configuration initiale
INSERT INTO admin_setup_status (id) VALUES (1)
ON CONFLICT (id) DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. ACTIVER RLS
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE members_grid ENABLE ROW LEVEL SECURITY;
ALTER TABLE sovereign_databases ENABLE ROW LEVEL SECURITY;
ALTER TABLE resource_relays ENABLE ROW LEVEL SECURITY;
ALTER TABLE admin_setup_status ENABLE ROW LEVEL SECURITY;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. POLICIES
-- ═══════════════════════════════════════════════════════════════════════════════

-- members_grid: Les membres voient leur propre entree
CREATE POLICY "Members can view own grid entry"
  ON members_grid FOR SELECT
  USING (user_id = auth.uid());

-- members_grid: Souverain voit tout
CREATE POLICY "Sovereign can view all grid members"
  ON members_grid FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- members_grid: Souverain peut tout modifier
CREATE POLICY "Sovereign can manage grid members"
  ON members_grid FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- sovereign_databases: Membres voient leur propre DB
CREATE POLICY "Members can view own database"
  ON sovereign_databases FOR SELECT
  USING (
    member_id IN (
      SELECT id FROM members_grid WHERE user_id = auth.uid()
    )
  );

-- sovereign_databases: Souverain gere tout
CREATE POLICY "Sovereign can manage all databases"
  ON sovereign_databases FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- resource_relays: Souverain seulement
CREATE POLICY "Sovereign can manage resource relays"
  ON resource_relays FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- admin_setup_status: Souverain seulement
CREATE POLICY "Sovereign can view setup status"
  ON admin_setup_status FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

CREATE POLICY "Sovereign can update setup status"
  ON admin_setup_status FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. FONCTIONS SECURISEES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Fonction pour mettre a jour le statut d'une API dans le Setup Wizard
CREATE OR REPLACE FUNCTION update_api_connection_status(
  p_api_name TEXT,
  p_connected BOOLEAN,
  p_extra_data JSONB DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
  completion_pct INTEGER;
BEGIN
  -- Verifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Acces reserve au Souverain'
    );
  END IF;

  -- Mettre a jour selon l'API
  CASE p_api_name
    WHEN 'openrouter' THEN
      UPDATE admin_setup_status SET
        api_openrouter_connected = p_connected,
        api_openrouter_tested_at = CASE WHEN p_connected THEN NOW() ELSE NULL END,
        api_openrouter_models_available = COALESCE((p_extra_data->>'models')::TEXT[], api_openrouter_models_available),
        last_updated = NOW(),
        last_updated_by = auth.uid()
      WHERE id = 1;

    WHEN 'anthropic' THEN
      UPDATE admin_setup_status SET
        api_anthropic_connected = p_connected,
        api_anthropic_tested_at = CASE WHEN p_connected THEN NOW() ELSE NULL END,
        last_updated = NOW(),
        last_updated_by = auth.uid()
      WHERE id = 1;

    WHEN 'stripe' THEN
      UPDATE admin_setup_status SET
        api_stripe_connected = p_connected,
        api_stripe_tested_at = CASE WHEN p_connected THEN NOW() ELSE NULL END,
        api_stripe_connect_enabled = COALESCE((p_extra_data->>'connect_enabled')::BOOLEAN, FALSE),
        last_updated = NOW(),
        last_updated_by = auth.uid()
      WHERE id = 1;

    WHEN 'digitalocean' THEN
      UPDATE admin_setup_status SET
        api_digitalocean_connected = p_connected,
        api_digitalocean_tested_at = CASE WHEN p_connected THEN NOW() ELSE NULL END,
        last_updated = NOW(),
        last_updated_by = auth.uid()
      WHERE id = 1;

    WHEN 'vercel' THEN
      UPDATE admin_setup_status SET
        api_vercel_connected = p_connected,
        api_vercel_tested_at = CASE WHEN p_connected THEN NOW() ELSE NULL END,
        last_updated = NOW(),
        last_updated_by = auth.uid()
      WHERE id = 1;

    WHEN 'supabase' THEN
      UPDATE admin_setup_status SET
        db_supabase_connected = p_connected,
        db_supabase_tested_at = CASE WHEN p_connected THEN NOW() ELSE NULL END,
        last_updated = NOW(),
        last_updated_by = auth.uid()
      WHERE id = 1;

    ELSE
      RETURN jsonb_build_object(
        'success', false,
        'error', 'API inconnue: ' || p_api_name
      );
  END CASE;

  -- Recalculer le pourcentage de completion
  SELECT INTO completion_pct
    (
      (CASE WHEN api_openrouter_connected THEN 15 ELSE 0 END) +
      (CASE WHEN api_anthropic_connected THEN 10 ELSE 0 END) +
      (CASE WHEN api_stripe_connected THEN 15 ELSE 0 END) +
      (CASE WHEN api_digitalocean_connected THEN 10 ELSE 0 END) +
      (CASE WHEN api_vercel_connected THEN 10 ELSE 0 END) +
      (CASE WHEN db_supabase_connected THEN 15 ELSE 0 END) +
      (CASE WHEN grid_initialized THEN 15 ELSE 0 END) +
      (CASE WHEN stripe_connect_configured THEN 10 ELSE 0 END)
    )
  FROM admin_setup_status WHERE id = 1;

  -- Mettre a jour le pourcentage et la frequence
  UPDATE admin_setup_status SET
    setup_completion_percentage = completion_pct,
    current_frequency = CASE
      WHEN completion_pct >= 100 THEN 999
      WHEN completion_pct >= 75 THEN 852
      WHEN completion_pct >= 50 THEN 639
      WHEN completion_pct >= 25 THEN 528
      ELSE 444
    END
  WHERE id = 1;

  RETURN jsonb_build_object(
    'success', true,
    'api', p_api_name,
    'connected', p_connected,
    'completion_percentage', completion_pct
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour obtenir le statut complet du Setup
CREATE OR REPLACE FUNCTION get_setup_status()
RETURNS JSONB AS $$
DECLARE
  status_record RECORD;
BEGIN
  -- Verifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Acces reserve au Souverain'
    );
  END IF;

  SELECT * INTO status_record FROM admin_setup_status WHERE id = 1;

  RETURN jsonb_build_object(
    'success', true,
    'apis', jsonb_build_object(
      'openrouter', jsonb_build_object(
        'connected', status_record.api_openrouter_connected,
        'tested_at', status_record.api_openrouter_tested_at,
        'models', status_record.api_openrouter_models_available
      ),
      'anthropic', jsonb_build_object(
        'connected', status_record.api_anthropic_connected,
        'tested_at', status_record.api_anthropic_tested_at
      ),
      'stripe', jsonb_build_object(
        'connected', status_record.api_stripe_connected,
        'tested_at', status_record.api_stripe_tested_at,
        'connect_enabled', status_record.api_stripe_connect_enabled
      ),
      'digitalocean', jsonb_build_object(
        'connected', status_record.api_digitalocean_connected,
        'tested_at', status_record.api_digitalocean_tested_at
      ),
      'vercel', jsonb_build_object(
        'connected', status_record.api_vercel_connected,
        'tested_at', status_record.api_vercel_tested_at
      )
    ),
    'database', jsonb_build_object(
      'connected', status_record.db_supabase_connected,
      'tables_initialized', status_record.db_tables_initialized,
      'functions_initialized', status_record.db_functions_initialized,
      'rls_enabled', status_record.db_rls_enabled
    ),
    'grid', jsonb_build_object(
      'initialized', status_record.grid_initialized,
      'initial_point_created', status_record.grid_initial_point_created,
      'founders_count', status_record.grid_founders_count,
      'active_founders', status_record.grid_active_founders
    ),
    'finance', jsonb_build_object(
      'stripe_connect_configured', status_record.stripe_connect_configured,
      'distribution_rules_set', status_record.distribution_rules_set,
      'first_payment_received', status_record.first_payment_received
    ),
    'completion_percentage', status_record.setup_completion_percentage,
    'current_frequency', status_record.current_frequency,
    'last_updated', status_record.last_updated
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour provisionner une base de donnees pour un membre
CREATE OR REPLACE FUNCTION provision_member_database(
  p_member_id UUID,
  p_db_name TEXT,
  p_region TEXT DEFAULT 'nyc1'
)
RETURNS JSONB AS $$
DECLARE
  new_db_id UUID;
BEGIN
  -- Verifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Acces reserve au Souverain'
    );
  END IF;

  -- Verifier que le membre existe
  IF NOT EXISTS (SELECT 1 FROM members_grid WHERE id = p_member_id) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Membre non trouve'
    );
  END IF;

  -- Creer l'entree de base de donnees
  INSERT INTO sovereign_databases (
    member_id,
    db_name,
    db_region,
    db_status
  ) VALUES (
    p_member_id,
    p_db_name,
    p_region,
    'PROVISIONING'
  )
  RETURNING id INTO new_db_id;

  -- Note: Le provisionnement reel serait fait par une Edge Function
  -- qui appellerait l'API DigitalOcean/Supabase

  RETURN jsonb_build_object(
    'success', true,
    'database_id', new_db_id,
    'status', 'PROVISIONING',
    'message', 'Base de donnees en cours de creation'
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour ajouter un relais de distribution
CREATE OR REPLACE FUNCTION add_resource_relay(
  p_provider_name TEXT,
  p_provider_type TEXT,
  p_stripe_account_id TEXT,
  p_distribution_percentage DECIMAL
)
RETURNS JSONB AS $$
DECLARE
  new_relay_id UUID;
  total_pct DECIMAL;
BEGIN
  -- Verifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Acces reserve au Souverain'
    );
  END IF;

  -- Verifier que le total des pourcentages ne depasse pas 100%
  SELECT COALESCE(SUM(distribution_percentage), 0) INTO total_pct
  FROM resource_relays WHERE is_active = TRUE;

  IF (total_pct + p_distribution_percentage) > 100 THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Le total des distributions ne peut pas depasser 100%',
      'current_total', total_pct,
      'requested', p_distribution_percentage
    );
  END IF;

  -- Creer le relais
  INSERT INTO resource_relays (
    provider_name,
    provider_type,
    stripe_account_id,
    distribution_percentage
  ) VALUES (
    p_provider_name,
    p_provider_type,
    p_stripe_account_id,
    p_distribution_percentage
  )
  RETURNING id INTO new_relay_id;

  RETURN jsonb_build_object(
    'success', true,
    'relay_id', new_relay_id,
    'message', 'Relais de distribution cree'
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour calculer la resonance d'un membre
CREATE OR REPLACE FUNCTION calculate_member_resonance(p_user_id UUID)
RETURNS JSONB AS $$
DECLARE
  member_rec RECORD;
  resonance DECIMAL;
  factors JSONB;
BEGIN
  -- Recuperer les donnees du membre
  SELECT mg.*, sd.used_tokens, sd.allocated_tokens, sd.last_activity_at
  INTO member_rec
  FROM members_grid mg
  LEFT JOIN sovereign_databases sd ON sd.member_id = mg.id
  WHERE mg.user_id = p_user_id;

  IF member_rec IS NULL THEN
    RETURN jsonb_build_object('success', false, 'error', 'Membre non trouve');
  END IF;

  -- Calculer la resonance basee sur plusieurs facteurs
  resonance := 0;
  factors := '{}';

  -- Facteur 1: Profil complet (25 points max)
  IF member_rec.full_name IS NOT NULL THEN
    resonance := resonance + 10;
    factors := factors || '{"profile_name": 10}';
  END IF;
  IF member_rec.email IS NOT NULL THEN
    resonance := resonance + 10;
    factors := factors || '{"profile_email": 10}';
  END IF;
  IF member_rec.energy_signature IS NOT NULL THEN
    resonance := resonance + 5;
    factors := factors || '{"energy_signature": 5}';
  END IF;

  -- Facteur 2: Activite (25 points max)
  IF member_rec.last_activity_at IS NOT NULL THEN
    IF member_rec.last_activity_at > NOW() - INTERVAL '7 days' THEN
      resonance := resonance + 25;
      factors := factors || '{"recent_activity": 25}';
    ELSIF member_rec.last_activity_at > NOW() - INTERVAL '30 days' THEN
      resonance := resonance + 15;
      factors := factors || '{"monthly_activity": 15}';
    ELSE
      resonance := resonance + 5;
      factors := factors || '{"past_activity": 5}';
    END IF;
  END IF;

  -- Facteur 3: Utilisation des tokens (25 points max)
  IF member_rec.allocated_tokens > 0 AND member_rec.used_tokens IS NOT NULL THEN
    DECLARE
      usage_pct DECIMAL;
    BEGIN
      usage_pct := (member_rec.used_tokens::DECIMAL / member_rec.allocated_tokens) * 100;
      IF usage_pct BETWEEN 20 AND 80 THEN
        resonance := resonance + 25;
        factors := factors || '{"healthy_usage": 25}';
      ELSIF usage_pct < 20 THEN
        resonance := resonance + 10;
        factors := factors || '{"low_usage": 10}';
      ELSE
        resonance := resonance + 15;
        factors := factors || '{"high_usage": 15}';
      END IF;
    END;
  END IF;

  -- Facteur 4: Statut d'activation (25 points max)
  IF member_rec.is_active THEN
    resonance := resonance + 25;
    factors := factors || '{"active_status": 25}';
  END IF;

  -- Mettre a jour la resonance du membre
  UPDATE members_grid SET
    resonance_score = resonance,
    updated_at = NOW()
  WHERE user_id = p_user_id;

  RETURN jsonb_build_object(
    'success', true,
    'resonance_score', resonance,
    'factors', factors,
    'energy_signature', member_rec.energy_signature
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 8. INDEX POUR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_members_grid_user_id ON members_grid(user_id);
CREATE INDEX IF NOT EXISTS idx_members_grid_role_id ON members_grid(role_id);
CREATE INDEX IF NOT EXISTS idx_members_grid_energy_signature ON members_grid(energy_signature);
CREATE INDEX IF NOT EXISTS idx_members_grid_resonance ON members_grid(resonance_score DESC);
CREATE INDEX IF NOT EXISTS idx_sovereign_databases_member_id ON sovereign_databases(member_id);
CREATE INDEX IF NOT EXISTS idx_sovereign_databases_status ON sovereign_databases(db_status);
CREATE INDEX IF NOT EXISTS idx_resource_relays_provider_type ON resource_relays(provider_type);
CREATE INDEX IF NOT EXISTS idx_resource_relays_active ON resource_relays(is_active);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 9. DONNEES INITIALES - RELAIS DE DISTRIBUTION PAR DEFAUT
-- ═══════════════════════════════════════════════════════════════════════════════

-- Configuration par defaut pour la distribution des 99$/mois
INSERT INTO resource_relays (provider_name, provider_type, distribution_percentage, is_active) VALUES
  ('OpenRouter Credits', 'api_provider', 40.00, TRUE),
  ('Development Fund', 'reserve', 30.00, TRUE),
  ('Founder Rewards', 'founder_reward', 20.00, TRUE),
  ('Emergency Reserve', 'reserve', 10.00, TRUE)
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN DU SCRIPT
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- RESUME:
-- ✅ Table members_grid: Membres fondateurs avec resonance energetique
-- ✅ Table sovereign_databases: Provisionnement DB par membre
-- ✅ Table resource_relays: Distribution Stripe Connect
-- ✅ Table admin_setup_status: Monitoring du Guide Admin (singleton)
-- ✅ Fonctions: update_api_connection_status, get_setup_status
-- ✅ Fonctions: provision_member_database, add_resource_relay
-- ✅ Fonction: calculate_member_resonance
-- ✅ RLS strict: Souverain seulement pour la configuration
--
-- ISOLATION SOUVERAINE:
-- Chaque membre fondateur peut avoir sa propre base de donnees isolee
-- Les flux financiers sont traces et redistribues automatiquement
-- La resonance est calculee pour identifier les membres les plus alignes
--
-- FREQUENCES:
-- 444 Hz: Heartbeat (< 25% completion)
-- 528 Hz: Amour (25-49% completion)
-- 639 Hz: Connexion (50-74% completion)
-- 852 Hz: Vision (75-99% completion)
-- 999 Hz: Source (100% completion)
--
-- ═══════════════════════════════════════════════════════════════════════════════
