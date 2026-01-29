-- ===============================================================================
-- AT·OM - FOUNDER ADAPTIVE AGENTS SQL
-- Système d'agents UX adaptatifs pour la phase Founder
-- ===============================================================================
--
-- INSTRUCTIONS:
-- 1. Aller dans Supabase Dashboard > SQL Editor
-- 2. Copier-coller ce script EN ENTIER
-- 3. Cliquer "Run" (ignorer l'avertissement "destructive operation")
--
-- IMPORTANT: Exécuter APRÈS agents-tables.sql
--
-- ===============================================================================

-- ===============================================================================
-- SECTION 1: TABLES DE MÉTRIQUES UX
-- ===============================================================================

-- 1.1 Métriques d'usage par section
CREATE TABLE IF NOT EXISTS founder_ux_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_id TEXT NOT NULL,
  section TEXT NOT NULL,
  time_spent_seconds INTEGER DEFAULT 0,
  scroll_depth INTEGER DEFAULT 0,
  interactions INTEGER DEFAULT 0,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_founder_ux_metrics_user ON founder_ux_metrics(user_id);
CREATE INDEX IF NOT EXISTS idx_founder_ux_metrics_section ON founder_ux_metrics(section);
CREATE INDEX IF NOT EXISTS idx_founder_ux_metrics_created ON founder_ux_metrics(created_at);

ALTER TABLE founder_ux_metrics ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users can insert their metrics" ON founder_ux_metrics;
CREATE POLICY "Users can insert their metrics"
ON founder_ux_metrics FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid() OR user_id IS NULL);

DROP POLICY IF EXISTS "Admins can view all metrics" ON founder_ux_metrics;
CREATE POLICY "Admins can view all metrics"
ON founder_ux_metrics FOR SELECT
TO authenticated
USING (
  user_id = auth.uid()
  OR EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

-- 1.2 Signaux de friction détectés
CREATE TABLE IF NOT EXISTS founder_friction_signals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  signal_type TEXT NOT NULL,
  source TEXT NOT NULL,
  content TEXT,
  severity TEXT DEFAULT 'low',
  detected_patterns JSONB DEFAULT '[]',
  context JSONB DEFAULT '{}',
  resolved BOOLEAN DEFAULT FALSE,
  resolved_by UUID REFERENCES auth.users(id),
  resolved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_friction_signals_type ON founder_friction_signals(signal_type);
CREATE INDEX IF NOT EXISTS idx_friction_signals_severity ON founder_friction_signals(severity);
CREATE INDEX IF NOT EXISTS idx_friction_signals_resolved ON founder_friction_signals(resolved);

ALTER TABLE founder_friction_signals ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "System can create friction signals" ON founder_friction_signals;
CREATE POLICY "System can create friction signals"
ON founder_friction_signals FOR INSERT
TO authenticated
WITH CHECK (true);

DROP POLICY IF EXISTS "Admins can view friction signals" ON founder_friction_signals;
CREATE POLICY "Admins can view friction signals"
ON founder_friction_signals FOR SELECT
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

DROP POLICY IF EXISTS "Admins can resolve friction signals" ON founder_friction_signals;
CREATE POLICY "Admins can resolve friction signals"
ON founder_friction_signals FOR UPDATE
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

-- ===============================================================================
-- SECTION 2: PROPOSITIONS DE LAYOUT
-- ===============================================================================

CREATE TABLE IF NOT EXISTS founder_layout_proposals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proposal_id TEXT UNIQUE NOT NULL,
  trigger_reason TEXT NOT NULL,
  observed_signals JSONB DEFAULT '[]',
  problem TEXT NOT NULL,
  suggested_change TEXT NOT NULL,
  expected_effect TEXT,
  confidence TEXT DEFAULT 'moyen',
  status TEXT DEFAULT 'pending',
  responded_by UUID REFERENCES auth.users(id),
  responded_at TIMESTAMPTZ,
  rejection_reason TEXT,
  implementation_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_layout_proposals_status ON founder_layout_proposals(status);
CREATE INDEX IF NOT EXISTS idx_layout_proposals_created ON founder_layout_proposals(created_at DESC);

ALTER TABLE founder_layout_proposals ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view proposals" ON founder_layout_proposals;
CREATE POLICY "Anyone can view proposals"
ON founder_layout_proposals FOR SELECT
TO authenticated
USING (true);

DROP POLICY IF EXISTS "System can create proposals" ON founder_layout_proposals;
CREATE POLICY "System can create proposals"
ON founder_layout_proposals FOR INSERT
TO authenticated
WITH CHECK (true);

DROP POLICY IF EXISTS "Admins can respond to proposals" ON founder_layout_proposals;
CREATE POLICY "Admins can respond to proposals"
ON founder_layout_proposals FOR UPDATE
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

-- ===============================================================================
-- SECTION 3: ANALYSES PÉRIODIQUES
-- ===============================================================================

CREATE TABLE IF NOT EXISTS founder_periodic_analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  analysis_type TEXT NOT NULL,
  period_start TIMESTAMPTZ NOT NULL,
  period_end TIMESTAMPTZ NOT NULL,
  metrics_summary JSONB DEFAULT '{}',
  signals_summary JSONB DEFAULT '{}',
  recommendations JSONB DEFAULT '[]',
  generated_proposals INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_periodic_analyses_type ON founder_periodic_analyses(analysis_type);
CREATE INDEX IF NOT EXISTS idx_periodic_analyses_period ON founder_periodic_analyses(period_start, period_end);

ALTER TABLE founder_periodic_analyses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Admins can view analyses" ON founder_periodic_analyses;
CREATE POLICY "Admins can view analyses"
ON founder_periodic_analyses FOR SELECT
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

DROP POLICY IF EXISTS "System can create analyses" ON founder_periodic_analyses;
CREATE POLICY "System can create analyses"
ON founder_periodic_analyses FOR INSERT
TO authenticated
WITH CHECK (true);

-- ===============================================================================
-- SECTION 4: TRACKING DE MATURITÉ FOUNDER
-- ===============================================================================

CREATE TABLE IF NOT EXISTS founder_maturity_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  total_founders INTEGER DEFAULT 0,
  active_founders INTEGER DEFAULT 0,
  sections_usage JSONB DEFAULT '{}',
  feature_adoption JSONB DEFAULT '{}',
  complexity_score INTEGER DEFAULT 0,
  readiness_for_migration TEXT DEFAULT 'not_ready',
  snapshot_date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_maturity_tracking_date ON founder_maturity_tracking(snapshot_date);

ALTER TABLE founder_maturity_tracking ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Admins can view maturity tracking" ON founder_maturity_tracking;
CREATE POLICY "Admins can view maturity tracking"
ON founder_maturity_tracking FOR SELECT
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

DROP POLICY IF EXISTS "System can track maturity" ON founder_maturity_tracking;
CREATE POLICY "System can track maturity"
ON founder_maturity_tracking FOR INSERT
TO authenticated
WITH CHECK (true);

-- ===============================================================================
-- SECTION 5: AJOUTER LES AGENTS ADAPTATIFS
-- ===============================================================================

-- Vérifier que la table agents existe
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'agents') THEN
    RAISE NOTICE 'Table agents does not exist. Run agents-tables.sql first.';
  ELSE
    -- Insérer les agents adaptatifs
    INSERT INTO agents (agent_type, display_name, description, capabilities, config)
    VALUES
      ('ux_observer', 'Observateur UX', 'Observe silencieusement l''usage: temps par section, scroll, interactions',
       '["track_time", "track_scroll", "track_interactions"]'::jsonb,
       '{"silent": true, "sample_rate": 1.0}'::jsonb),
      ('feedback_analyst', 'Analyste Feedback', 'Détecte les signaux de friction dans les messages et comportements',
       '["detect_confusion", "detect_frustration", "pattern_recognition"]'::jsonb,
       '{"keywords": ["où trouver", "je ne comprends pas", "comment", "bug", "erreur"], "threshold": 3}'::jsonb),
      ('structure_architect', 'Architecte Structure', 'Propose des ajustements de layout basés sur les données',
       '["analyze_usage", "propose_changes", "simulate_impact"]'::jsonb,
       '{"analysis_interval_hours": 4, "min_confidence": 0.6}'::jsonb),
      ('coherence_guardian', 'Gardien Cohérence', 'Empêche la dérive vers la complexité prématurée',
       '["check_complexity", "validate_proposals", "enforce_boundaries"]'::jsonb,
       '{"max_tabs": 5, "max_depth": 2, "founder_only": true}'::jsonb)
    ON CONFLICT (agent_type) DO UPDATE SET
      display_name = EXCLUDED.display_name,
      description = EXCLUDED.description,
      capabilities = EXCLUDED.capabilities,
      config = EXCLUDED.config;
  END IF;
END $$;

-- ===============================================================================
-- SECTION 6: FONCTIONS UTILITAIRES
-- ===============================================================================

-- Fonction: Enregistrer une métrique UX
CREATE OR REPLACE FUNCTION record_ux_metric(
  p_user_id UUID,
  p_session_id TEXT,
  p_section TEXT,
  p_time_spent INTEGER,
  p_scroll_depth INTEGER DEFAULT 0,
  p_interactions INTEGER DEFAULT 0,
  p_metadata JSONB DEFAULT '{}'
)
RETURNS UUID AS $$
DECLARE
  v_metric_id UUID;
BEGIN
  INSERT INTO founder_ux_metrics (
    user_id, session_id, section, time_spent_seconds,
    scroll_depth, interactions, metadata
  )
  VALUES (
    p_user_id, p_session_id, p_section, p_time_spent,
    p_scroll_depth, p_interactions, p_metadata
  )
  RETURNING id INTO v_metric_id;

  RETURN v_metric_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Détecter un signal de friction
CREATE OR REPLACE FUNCTION detect_friction_signal(
  p_signal_type TEXT,
  p_source TEXT,
  p_content TEXT DEFAULT NULL,
  p_patterns JSONB DEFAULT '[]',
  p_context JSONB DEFAULT '{}'
)
RETURNS UUID AS $$
DECLARE
  v_signal_id UUID;
  v_severity TEXT := 'low';
  v_pattern_count INTEGER;
BEGIN
  -- Calculer la sévérité basée sur le nombre de patterns
  v_pattern_count := jsonb_array_length(p_patterns);
  IF v_pattern_count >= 5 THEN
    v_severity := 'high';
  ELSIF v_pattern_count >= 3 THEN
    v_severity := 'medium';
  END IF;

  INSERT INTO founder_friction_signals (
    signal_type, source, content, severity, detected_patterns, context
  )
  VALUES (
    p_signal_type, p_source, p_content, v_severity, p_patterns, p_context
  )
  RETURNING id INTO v_signal_id;

  RETURN v_signal_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Vérifier si une proposition doit être générée
CREATE OR REPLACE FUNCTION should_generate_proposal(
  p_hours_lookback INTEGER DEFAULT 4
)
RETURNS BOOLEAN AS $$
DECLARE
  v_friction_count INTEGER;
  v_section_imbalance BOOLEAN;
  v_low_usage_sections INTEGER;
BEGIN
  -- Compter les signaux de friction récents non résolus
  SELECT COUNT(*) INTO v_friction_count
  FROM founder_friction_signals
  WHERE created_at > NOW() - (p_hours_lookback || ' hours')::INTERVAL
  AND resolved = FALSE;

  -- Vérifier le déséquilibre des sections
  SELECT COUNT(*) INTO v_low_usage_sections
  FROM (
    SELECT section, SUM(time_spent_seconds) as total_time
    FROM founder_ux_metrics
    WHERE created_at > NOW() - (p_hours_lookback || ' hours')::INTERVAL
    GROUP BY section
    HAVING SUM(time_spent_seconds) < 60  -- Moins d'une minute
  ) low_sections;

  v_section_imbalance := v_low_usage_sections > 0;

  -- Générer proposition si friction >= 3 OU déséquilibre
  RETURN v_friction_count >= 3 OR v_section_imbalance;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Créer une proposition de layout
CREATE OR REPLACE FUNCTION create_layout_proposal(
  p_trigger_reason TEXT,
  p_signals JSONB,
  p_problem TEXT,
  p_suggested_change TEXT,
  p_expected_effect TEXT,
  p_confidence TEXT DEFAULT 'moyen'
)
RETURNS TEXT AS $$
DECLARE
  v_proposal_id TEXT;
BEGIN
  -- Générer un ID unique
  v_proposal_id := 'founder-ux-' || LPAD(
    (SELECT COUNT(*) + 1 FROM founder_layout_proposals)::TEXT,
    3, '0'
  );

  INSERT INTO founder_layout_proposals (
    proposal_id, trigger_reason, observed_signals,
    problem, suggested_change, expected_effect, confidence
  )
  VALUES (
    v_proposal_id, p_trigger_reason, p_signals,
    p_problem, p_suggested_change, p_expected_effect, p_confidence
  );

  RETURN v_proposal_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Répondre à une proposition
CREATE OR REPLACE FUNCTION respond_to_proposal(
  p_proposal_id TEXT,
  p_action TEXT,
  p_reason TEXT DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
  IF p_action NOT IN ('approve', 'reject', 'defer') THEN
    RAISE EXCEPTION 'Invalid action: %', p_action;
  END IF;

  UPDATE founder_layout_proposals
  SET
    status = CASE
      WHEN p_action = 'approve' THEN 'approved'
      WHEN p_action = 'reject' THEN 'rejected'
      ELSE 'deferred'
    END,
    responded_by = auth.uid(),
    responded_at = NOW(),
    rejection_reason = CASE WHEN p_action = 'reject' THEN p_reason ELSE NULL END
  WHERE proposal_id = p_proposal_id;

  RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===============================================================================
-- SECTION 7: ACTIVER REALTIME
-- ===============================================================================

DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE founder_ux_metrics;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE founder_friction_signals;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE founder_layout_proposals;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE founder_periodic_analyses;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;

-- ===============================================================================
-- FIN DU SCRIPT - FOUNDER ADAPTIVE AGENTS
-- ===============================================================================

-- Vérification:
-- SELECT * FROM agents WHERE agent_type LIKE '%observer%' OR agent_type LIKE '%analyst%';
-- SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'founder_%';
