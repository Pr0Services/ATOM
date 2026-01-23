-- ═══════════════════════════════════════════════════════════════════════════════
--
--       ██╗   ██╗███████╗ █████╗  ██████╗ ███████╗
--       ██║   ██║██╔════╝██╔══██╗██╔════╝ ██╔════╝
--       ██║   ██║███████╗███████║██║  ███╗█████╗
--       ██║   ██║╚════██║██╔══██║██║   ██║██╔══╝
--       ╚██████╔╝███████║██║  ██║╚██████╔╝███████╗
--        ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
--
--              SYSTEME DE CREDITS ET USAGE API - AT·OM / CHE·NU V76
--                  Tokens Pre-payes & Tracking de Consommation
--
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- ARCHITECTURE:
-- L'Arche agit comme Proxy Souverain - une seule cle API maitre
-- Les utilisateurs consomment des "credits de resonance" (tokens)
-- Pas besoin de leurs propres cles API
--
-- PLANS:
-- - citoyen (gratuit): 50,000 tokens/mois
-- - fondateur: 500,000 tokens/mois
-- - souverain: Illimite
--
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. TABLE D'USAGE MENSUEL PAR UTILISATEUR
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS api_usage (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

  -- Periode (format: YYYY-MM)
  month TEXT NOT NULL,

  -- Compteurs
  tokens_used INTEGER DEFAULT 0,
  requests_count INTEGER DEFAULT 0,
  cost_cents INTEGER DEFAULT 0,  -- Cout en centimes pour l'Arche

  -- Limites (copie du plan au moment de la creation)
  tokens_limit INTEGER DEFAULT 50000,

  -- Metadonnees
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Un seul enregistrement par utilisateur par mois
  UNIQUE(user_id, month)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. TABLE DETAILLEE DES REQUETES API
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS api_requests (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

  -- Details de la requete
  provider TEXT NOT NULL,           -- openrouter, anthropic, openai
  model TEXT NOT NULL,              -- claude-3-sonnet, gpt-4, etc.

  -- Tokens utilises
  input_tokens INTEGER DEFAULT 0,
  output_tokens INTEGER DEFAULT 0,
  total_tokens INTEGER DEFAULT 0,

  -- Cout pour l'Arche (en centimes)
  cost_cents INTEGER DEFAULT 0,

  -- Contexte (optionnel)
  context_type TEXT,                -- agent, chat, analysis, etc.
  context_id TEXT,                  -- ID de l'agent ou session

  -- Timing
  latency_ms INTEGER,               -- Temps de reponse

  -- Metadonnees
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. TABLE DES PLANS ET ALLOCATIONS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS subscription_plans (
  id TEXT PRIMARY KEY,              -- citoyen, fondateur, souverain
  name TEXT NOT NULL,

  -- Allocations mensuelles
  tokens_monthly INTEGER NOT NULL,  -- -1 pour illimite

  -- Prix (en centimes)
  price_monthly_cents INTEGER DEFAULT 0,

  -- Fonctionnalites
  features JSONB DEFAULT '[]',

  -- Metadonnees
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Inserer les plans par defaut
INSERT INTO subscription_plans (id, name, tokens_monthly, price_monthly_cents, features) VALUES
  ('citoyen', 'Citoyen', 50000, 0, '["Acces basique", "50K tokens/mois", "Support communautaire"]'),
  ('fondateur', 'Membre Fondateur', 500000, 9900, '["500K tokens/mois", "Acces Grid", "Support prioritaire", "Agents L4-L6"]'),
  ('souverain', 'Souverain', -1, 0, '["Tokens illimites", "Acces total", "Controle Grid", "Tous les agents"]')
ON CONFLICT (id) DO UPDATE SET
  tokens_monthly = EXCLUDED.tokens_monthly,
  price_monthly_cents = EXCLUDED.price_monthly_cents,
  features = EXCLUDED.features;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. ACTIVER RLS
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE api_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_plans ENABLE ROW LEVEL SECURITY;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. POLICIES
-- ═══════════════════════════════════════════════════════════════════════════════

-- api_usage: Les utilisateurs voient leur propre usage
CREATE POLICY "Users can view own usage"
  ON api_usage FOR SELECT
  USING (auth.uid() = user_id);

-- api_usage: Le systeme peut inserer/modifier (via fonction SECURITY DEFINER)
CREATE POLICY "System can manage usage"
  ON api_usage FOR ALL
  USING (true)
  WITH CHECK (true);

-- api_requests: Les utilisateurs voient leurs propres requetes
CREATE POLICY "Users can view own requests"
  ON api_requests FOR SELECT
  USING (auth.uid() = user_id);

-- api_requests: Le systeme peut inserer
CREATE POLICY "System can insert requests"
  ON api_requests FOR INSERT
  WITH CHECK (true);

-- subscription_plans: Tout le monde peut voir les plans
CREATE POLICY "Anyone can view plans"
  ON subscription_plans FOR SELECT
  USING (true);

-- Souverain peut tout voir
CREATE POLICY "Souverain can view all usage"
  ON api_usage FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

CREATE POLICY "Souverain can view all requests"
  ON api_requests FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. FONCTIONS SECURISEES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Fonction pour enregistrer l'usage API
CREATE OR REPLACE FUNCTION record_api_usage(
  p_user_id UUID,
  p_month TEXT,
  p_tokens INTEGER,
  p_cost INTEGER DEFAULT 0
)
RETURNS VOID AS $$
DECLARE
  user_plan TEXT;
  tokens_limit INTEGER;
BEGIN
  -- Recuperer le plan de l'utilisateur
  SELECT role INTO user_plan FROM profiles WHERE id = p_user_id;

  -- Determiner la limite selon le plan
  SELECT tokens_monthly INTO tokens_limit
  FROM subscription_plans
  WHERE id = COALESCE(user_plan, 'citoyen');

  -- Upsert l'usage mensuel
  INSERT INTO api_usage (user_id, month, tokens_used, requests_count, cost_cents, tokens_limit)
  VALUES (p_user_id, p_month, p_tokens, 1, p_cost, COALESCE(tokens_limit, 50000))
  ON CONFLICT (user_id, month) DO UPDATE SET
    tokens_used = api_usage.tokens_used + p_tokens,
    requests_count = api_usage.requests_count + 1,
    cost_cents = api_usage.cost_cents + p_cost,
    updated_at = NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour verifier les credits disponibles
CREATE OR REPLACE FUNCTION check_user_credits(p_user_id UUID)
RETURNS JSONB AS $$
DECLARE
  user_plan TEXT;
  tokens_limit INTEGER;
  tokens_used INTEGER;
  current_month TEXT;
BEGIN
  current_month := to_char(NOW(), 'YYYY-MM');

  -- Recuperer le plan
  SELECT role INTO user_plan FROM profiles WHERE id = p_user_id;

  -- Souverain = illimite
  IF user_plan = 'souverain' THEN
    RETURN jsonb_build_object(
      'allowed', true,
      'remaining', -1,
      'limit', -1,
      'plan', 'souverain'
    );
  END IF;

  -- Recuperer la limite
  SELECT tokens_monthly INTO tokens_limit
  FROM subscription_plans
  WHERE id = COALESCE(user_plan, 'citoyen');

  -- Recuperer l'usage actuel
  SELECT COALESCE(u.tokens_used, 0) INTO tokens_used
  FROM api_usage u
  WHERE u.user_id = p_user_id AND u.month = current_month;

  RETURN jsonb_build_object(
    'allowed', (COALESCE(tokens_limit, 50000) - COALESCE(tokens_used, 0)) > 0,
    'remaining', COALESCE(tokens_limit, 50000) - COALESCE(tokens_used, 0),
    'used', COALESCE(tokens_used, 0),
    'limit', COALESCE(tokens_limit, 50000),
    'plan', COALESCE(user_plan, 'citoyen')
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour obtenir les stats globales (Souverain seulement)
CREATE OR REPLACE FUNCTION get_api_stats()
RETURNS JSONB AS $$
DECLARE
  stats JSONB;
  current_month TEXT;
BEGIN
  -- Verifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object('error', 'Acces reserve au Souverain');
  END IF;

  current_month := to_char(NOW(), 'YYYY-MM');

  SELECT jsonb_build_object(
    'month', current_month,
    'total_users', (SELECT COUNT(DISTINCT user_id) FROM api_usage WHERE month = current_month),
    'total_tokens', (SELECT COALESCE(SUM(tokens_used), 0) FROM api_usage WHERE month = current_month),
    'total_requests', (SELECT COALESCE(SUM(requests_count), 0) FROM api_usage WHERE month = current_month),
    'total_cost_cents', (SELECT COALESCE(SUM(cost_cents), 0) FROM api_usage WHERE month = current_month),
    'top_models', (
      SELECT jsonb_agg(row_to_json(m))
      FROM (
        SELECT model, COUNT(*) as count, SUM(total_tokens) as tokens
        FROM api_requests
        WHERE created_at >= date_trunc('month', NOW())
        GROUP BY model
        ORDER BY count DESC
        LIMIT 5
      ) m
    ),
    'daily_usage', (
      SELECT jsonb_agg(row_to_json(d))
      FROM (
        SELECT
          date_trunc('day', created_at)::date as day,
          SUM(total_tokens) as tokens,
          COUNT(*) as requests
        FROM api_requests
        WHERE created_at >= date_trunc('month', NOW())
        GROUP BY date_trunc('day', created_at)
        ORDER BY day
      ) d
    )
  ) INTO stats;

  RETURN stats;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. INDEX POUR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_api_usage_user_month ON api_usage(user_id, month);
CREATE INDEX IF NOT EXISTS idx_api_requests_user_id ON api_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_api_requests_created_at ON api_requests(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_api_requests_model ON api_requests(model);

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN DU SCRIPT
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- RESUME:
-- ✅ Table api_usage: Tracking mensuel par utilisateur
-- ✅ Table api_requests: Detail de chaque requete
-- ✅ Table subscription_plans: Definition des plans
-- ✅ Fonctions: record_api_usage, check_user_credits, get_api_stats
-- ✅ RLS: Utilisateurs voient leur usage, Souverain voit tout
--
-- INTEGRATION:
-- Le service APIRouter.js utilise ces tables pour:
-- 1. Verifier les credits avant chaque appel
-- 2. Enregistrer la consommation
-- 3. Fournir des statistiques
--
-- ═══════════════════════════════════════════════════════════════════════════════
