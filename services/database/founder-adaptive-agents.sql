-- ===============================================================================
-- AT·OM - SYSTÈME D'AGENTS ADAPTATIFS FOUNDER
-- Agents d'observation, analyse et proposition pour la phase fondatrice
-- ===============================================================================
--
-- PRINCIPE CLÉ:
-- Les agents n'imposent jamais un layout.
-- Ils OBSERVENT → PROPOSENT → PRÉPARENT → ATTENDENT validation.
--
-- AGENTS:
-- 1. Observateur UX (silencieux) - voir sans intervenir
-- 2. Analyste Feedback - écouter les humains
-- 3. Architecte Structure - proposer des ajustements
-- 4. Gardien Cohérence - empêcher la dérive
--
-- ===============================================================================

-- 1. TABLE: AGENTS ADAPTATIFS (types spécifiques Founder)
-- ===============================================================================

-- Ajouter les nouveaux types d'agents
ALTER TABLE agents DROP CONSTRAINT IF EXISTS agents_type_check;
ALTER TABLE agents ADD CONSTRAINT agents_type_check
CHECK (type IN (
  'facilitator', 'synthesis', 'memory',
  'ux_observer', 'feedback_analyst', 'structure_architect', 'coherence_guardian'
));

-- Insérer les 4 agents adaptatifs Founder
INSERT INTO agents (name, type, description, default_objective, icon, capabilities) VALUES
  (
    'Observateur UX',
    'ux_observer',
    'Observe l''usage réel sans intervenir. Produit des rapports périodiques et des signaux de friction.',
    'Détecter les patterns d''usage et les zones de friction',
    '👁️',
    '["scroll_tracking", "time_tracking", "navigation_patterns", "heatmap_logic"]'
  ),
  (
    'Analyste Feedback',
    'feedback_analyst',
    'Écoute les messages humains et extrait les frustrations, attentes et demandes répétées.',
    'Traduire l''émotion humaine en signal UX actionnable',
    '👂',
    '["sentiment_analysis", "friction_detection", "pattern_extraction", "redundancy_check"]'
  ),
  (
    'Architecte Structure',
    'structure_architect',
    'Propose des ajustements de layout basés sur les signaux UX et feedback. Ne modifie JAMAIS directement.',
    'Proposer des ajustements minimaux pour réduire la confusion',
    '🏗️',
    '["layout_proposal", "section_analysis", "priority_suggestion", "migration_readiness"]'
  ),
  (
    'Gardien Cohérence',
    'coherence_guardian',
    'Vérifie que Founder reste une page fondation, sans dérive vers complexité prématurée.',
    'Empêcher l''exposition prématurée de logiques opérationnelles',
    '🛡️',
    '["complexity_check", "sphere_leak_detection", "automation_guard", "human_level_check"]'
  )
ON CONFLICT DO NOTHING;

-- 2. TABLE: MÉTRIQUES UX FOUNDER
-- ===============================================================================

CREATE TABLE IF NOT EXISTS founder_ux_metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  session_id TEXT NOT NULL,

  -- Métriques de navigation
  section_name TEXT NOT NULL,
  time_spent_ms INTEGER DEFAULT 0,
  scroll_depth_percent INTEGER DEFAULT 0,
  visit_order INTEGER,

  -- Métriques d'interaction
  clicks INTEGER DEFAULT 0,
  messages_sent INTEGER DEFAULT 0,
  messages_read INTEGER DEFAULT 0,

  -- Contexte
  device_type TEXT DEFAULT 'desktop',
  window_start TIMESTAMPTZ DEFAULT NOW(),
  window_end TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour les analyses
CREATE INDEX IF NOT EXISTS idx_founder_ux_section ON founder_ux_metrics(section_name);
CREATE INDEX IF NOT EXISTS idx_founder_ux_session ON founder_ux_metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_founder_ux_time ON founder_ux_metrics(created_at);

-- RLS
ALTER TABLE founder_ux_metrics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "System can insert metrics"
ON founder_ux_metrics FOR INSERT
TO authenticated
WITH CHECK (true);

CREATE POLICY "Admins can view metrics"
ON founder_ux_metrics FOR SELECT
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

-- 3. TABLE: SIGNAUX DE FRICTION (feedbacks verbaux)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS founder_friction_signals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Source du signal
  source_type TEXT NOT NULL CHECK (source_type IN ('chat', 'thread', 'feedback')),
  source_id UUID,
  message_content TEXT NOT NULL,

  -- Analyse
  friction_type TEXT NOT NULL CHECK (friction_type IN (
    'confusion',      -- "je ne comprends pas"
    'navigation',     -- "où est...", "je cherche..."
    'overload',       -- "c'est trop", "c'est chargé"
    'suggestion',     -- "on devrait...", "il faudrait..."
    'question',       -- questions répétées
    'frustration'     -- expressions négatives
  )),
  keywords TEXT[],
  severity INTEGER DEFAULT 1 CHECK (severity BETWEEN 1 AND 5),

  -- Contexte
  user_id UUID REFERENCES auth.users(id),
  detected_at TIMESTAMPTZ DEFAULT NOW(),
  processed BOOLEAN DEFAULT FALSE,
  processed_at TIMESTAMPTZ
);

-- Index
CREATE INDEX IF NOT EXISTS idx_friction_type ON founder_friction_signals(friction_type);
CREATE INDEX IF NOT EXISTS idx_friction_unprocessed ON founder_friction_signals(processed) WHERE processed = FALSE;
CREATE INDEX IF NOT EXISTS idx_friction_time ON founder_friction_signals(detected_at);

-- RLS
ALTER TABLE founder_friction_signals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "System can insert friction signals"
ON founder_friction_signals FOR INSERT
TO authenticated
WITH CHECK (true);

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

-- 4. TABLE: PROPOSITIONS D'AJUSTEMENT (Agent Architecte)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS founder_layout_proposals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proposal_id TEXT UNIQUE NOT NULL,  -- ex: "founder-ux-004"

  -- Fenêtre d'analyse
  trigger_window_start TIMESTAMPTZ NOT NULL,
  trigger_window_end TIMESTAMPTZ NOT NULL,

  -- Raison du déclenchement
  trigger_reason TEXT NOT NULL,
  observed_signals JSONB NOT NULL DEFAULT '[]',

  -- Proposition unique
  problem TEXT NOT NULL,
  suggested_change TEXT NOT NULL,
  expected_effect TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('faible', 'moyen', 'élevé')),

  -- Statut
  status TEXT DEFAULT 'pending' CHECK (status IN (
    'pending',    -- En attente de discussion
    'discussed',  -- Discuté mais pas de décision
    'approved',   -- Approuvé, en attente d'implémentation
    'rejected',   -- Rejeté
    'implemented' -- Implémenté
  )),

  -- Validation humaine
  discussed_in_thread UUID,
  discussion_summary TEXT,
  validated_by UUID REFERENCES auth.users(id),
  validated_at TIMESTAMPTZ,
  rejection_reason TEXT,

  -- Métadonnées
  agent_instance_id UUID REFERENCES agent_instances(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_proposals_status ON founder_layout_proposals(status);
CREATE INDEX IF NOT EXISTS idx_proposals_pending ON founder_layout_proposals(created_at) WHERE status = 'pending';

-- RLS
ALTER TABLE founder_layout_proposals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated can view proposals"
ON founder_layout_proposals FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "Agents can create proposals"
ON founder_layout_proposals FOR INSERT
TO authenticated
WITH CHECK (true);

CREATE POLICY "Validators can update proposals"
ON founder_layout_proposals FOR UPDATE
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN', 'FOUNDER')
  )
);

-- 5. TABLE: ANALYSES PÉRIODIQUES (rapports toutes les 4h)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS founder_periodic_analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Fenêtre d'analyse
  window_start TIMESTAMPTZ NOT NULL,
  window_end TIMESTAMPTZ NOT NULL,

  -- Métriques agrégées par section
  section_metrics JSONB NOT NULL DEFAULT '{}',
  -- Format: { "vision": { "avg_time": 45000, "visits": 23, "scroll_depth": 78 }, ... }

  -- Signaux de friction agrégés
  friction_summary JSONB NOT NULL DEFAULT '{}',
  -- Format: { "confusion": 3, "navigation": 5, "total": 8 }

  -- Décision de l'agent
  proposal_generated BOOLEAN DEFAULT FALSE,
  proposal_id TEXT REFERENCES founder_layout_proposals(proposal_id),
  no_proposal_reason TEXT,  -- Si pas de proposition, pourquoi

  -- Métadonnées
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_analyses_time ON founder_periodic_analyses(window_end DESC);

-- RLS
ALTER TABLE founder_periodic_analyses ENABLE ROW LEVEL SECURITY;

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

-- 6. TABLE: ÉTAT DE MATURITÉ FONDATION → OPÉRATION
-- ===============================================================================

CREATE TABLE IF NOT EXISTS founder_maturity_tracking (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Sujet suivi
  topic TEXT NOT NULL,
  topic_type TEXT NOT NULL CHECK (topic_type IN (
    'discussion',  -- Fil de discussion
    'decision',    -- Décision émergente
    'process',     -- Processus potentiel
    'section'      -- Section de la page
  )),

  -- Indicateurs de maturité
  first_mentioned_at TIMESTAMPTZ NOT NULL,
  mention_count INTEGER DEFAULT 1,
  participant_count INTEGER DEFAULT 1,
  divergence_level INTEGER DEFAULT 5 CHECK (divergence_level BETWEEN 1 AND 10),
  -- 10 = très divergent (fondation), 1 = convergé (opération)

  -- Signaux de stabilisation
  decision_phrases_detected INTEGER DEFAULT 0,
  -- "on décide que", "on est d'accord", "à partir de maintenant"

  -- Statut
  maturity_status TEXT DEFAULT 'foundation' CHECK (maturity_status IN (
    'foundation',      -- Encore en discussion libre
    'stabilizing',     -- Commence à converger
    'ready_synthesis', -- Prêt pour synthèse agent
    'synthesized',     -- Synthèse produite
    'ready_migration', -- Prêt pour migration vers sphère
    'migrated'         -- Migré
  )),

  -- Migration
  target_sphere TEXT,  -- 'communication', 'scholar', 'identity', etc.
  migrated_at TIMESTAMPTZ,
  migrated_by UUID REFERENCES auth.users(id),

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_maturity_status ON founder_maturity_tracking(maturity_status);
CREATE INDEX IF NOT EXISTS idx_maturity_topic ON founder_maturity_tracking(topic);

-- RLS
ALTER TABLE founder_maturity_tracking ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated can view maturity tracking"
ON founder_maturity_tracking FOR SELECT
TO authenticated
USING (true);

-- 7. FONCTIONS UTILITAIRES
-- ===============================================================================

-- Fonction pour enregistrer une métrique UX
CREATE OR REPLACE FUNCTION record_ux_metric(
  p_session_id TEXT,
  p_section_name TEXT,
  p_time_spent_ms INTEGER,
  p_scroll_depth INTEGER DEFAULT 0,
  p_visit_order INTEGER DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
  v_metric_id UUID;
BEGIN
  INSERT INTO founder_ux_metrics (
    user_id, session_id, section_name,
    time_spent_ms, scroll_depth_percent, visit_order
  )
  VALUES (
    auth.uid(), p_session_id, p_section_name,
    p_time_spent_ms, p_scroll_depth, p_visit_order
  )
  RETURNING id INTO v_metric_id;

  RETURN v_metric_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour détecter un signal de friction
CREATE OR REPLACE FUNCTION detect_friction_signal(
  p_source_type TEXT,
  p_source_id UUID,
  p_message TEXT
)
RETURNS UUID AS $$
DECLARE
  v_signal_id UUID;
  v_friction_type TEXT;
  v_keywords TEXT[];
  v_severity INTEGER;
BEGIN
  -- Détection simple basée sur les mots-clés
  IF p_message ~* '(je ne comprends pas|c''est confus|pas clair)' THEN
    v_friction_type := 'confusion';
    v_severity := 3;
    v_keywords := ARRAY['comprendre', 'confus', 'clair'];
  ELSIF p_message ~* '(où est|je cherche|je trouve pas|où trouver)' THEN
    v_friction_type := 'navigation';
    v_severity := 2;
    v_keywords := ARRAY['où', 'cherche', 'trouve'];
  ELSIF p_message ~* '(c''est trop|trop chargé|trop complexe|trop de)' THEN
    v_friction_type := 'overload';
    v_severity := 3;
    v_keywords := ARRAY['trop', 'chargé', 'complexe'];
  ELSIF p_message ~* '(on devrait|il faudrait|pourquoi pas|et si on)' THEN
    v_friction_type := 'suggestion';
    v_severity := 1;
    v_keywords := ARRAY['devrait', 'faudrait', 'pourquoi'];
  ELSE
    -- Pas de friction détectée
    RETURN NULL;
  END IF;

  INSERT INTO founder_friction_signals (
    source_type, source_id, message_content,
    friction_type, keywords, severity, user_id
  )
  VALUES (
    p_source_type, p_source_id, p_message,
    v_friction_type, v_keywords, v_severity, auth.uid()
  )
  RETURNING id INTO v_signal_id;

  RETURN v_signal_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour vérifier si une proposition doit être générée
CREATE OR REPLACE FUNCTION should_generate_proposal(
  p_window_hours INTEGER DEFAULT 4
)
RETURNS JSONB AS $$
DECLARE
  v_window_start TIMESTAMPTZ;
  v_confusion_count INTEGER;
  v_section_imbalance BOOLEAN;
  v_redundancy_count INTEGER;
  v_result JSONB;
BEGIN
  v_window_start := NOW() - (p_window_hours || ' hours')::INTERVAL;

  -- Critère 1: Confusion répétée (>= 3)
  SELECT COUNT(*) INTO v_confusion_count
  FROM founder_friction_signals
  WHERE friction_type IN ('confusion', 'navigation')
  AND detected_at > v_window_start
  AND processed = FALSE;

  -- Critère 2: Déséquilibre structurel (section > 60% ou < 15%)
  SELECT EXISTS (
    SELECT 1 FROM (
      SELECT section_name,
        SUM(time_spent_ms) * 100.0 / NULLIF(SUM(SUM(time_spent_ms)) OVER (), 0) as pct
      FROM founder_ux_metrics
      WHERE created_at > v_window_start
      GROUP BY section_name
    ) sub
    WHERE pct > 60 OR pct < 15
  ) INTO v_section_imbalance;

  -- Critère 3: Redondance (même question >= 3 fois)
  SELECT COUNT(*) INTO v_redundancy_count
  FROM (
    SELECT message_content, COUNT(*) as cnt
    FROM founder_friction_signals
    WHERE friction_type = 'question'
    AND detected_at > v_window_start
    GROUP BY message_content
    HAVING COUNT(*) >= 3
  ) sub;

  -- Construire le résultat
  v_result := jsonb_build_object(
    'should_trigger', (v_confusion_count >= 3 OR v_section_imbalance OR v_redundancy_count > 0),
    'confusion_count', v_confusion_count,
    'section_imbalance', v_section_imbalance,
    'redundancy_detected', v_redundancy_count > 0,
    'window_start', v_window_start,
    'window_end', NOW()
  );

  RETURN v_result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour créer une proposition
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
  v_window_start TIMESTAMPTZ;
BEGIN
  v_window_start := NOW() - INTERVAL '4 hours';

  -- Générer un ID unique
  v_proposal_id := 'founder-ux-' || LPAD(
    (SELECT COUNT(*) + 1 FROM founder_layout_proposals)::TEXT,
    3, '0'
  );

  INSERT INTO founder_layout_proposals (
    proposal_id, trigger_window_start, trigger_window_end,
    trigger_reason, observed_signals,
    problem, suggested_change, expected_effect, confidence
  )
  VALUES (
    v_proposal_id, v_window_start, NOW(),
    p_trigger_reason, p_signals,
    p_problem, p_suggested_change, p_expected_effect, p_confidence
  );

  RETURN v_proposal_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour valider/rejeter une proposition
CREATE OR REPLACE FUNCTION respond_to_proposal(
  p_proposal_id TEXT,
  p_action TEXT,  -- 'approve', 'reject', 'discuss'
  p_reason TEXT DEFAULT NULL,
  p_thread_id UUID DEFAULT NULL
)
RETURNS BOOLEAN AS $$
BEGIN
  UPDATE founder_layout_proposals
  SET
    status = CASE p_action
      WHEN 'approve' THEN 'approved'
      WHEN 'reject' THEN 'rejected'
      WHEN 'discuss' THEN 'discussed'
      ELSE status
    END,
    validated_by = auth.uid(),
    validated_at = CASE WHEN p_action IN ('approve', 'reject') THEN NOW() ELSE NULL END,
    rejection_reason = CASE WHEN p_action = 'reject' THEN p_reason ELSE NULL END,
    discussed_in_thread = COALESCE(p_thread_id, discussed_in_thread),
    updated_at = NOW()
  WHERE proposal_id = p_proposal_id;

  RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 8. REALTIME
-- ===============================================================================

ALTER PUBLICATION supabase_realtime ADD TABLE founder_layout_proposals;
ALTER PUBLICATION supabase_realtime ADD TABLE founder_friction_signals;

-- 9. VUES UTILES
-- ===============================================================================

-- Vue des propositions en attente
CREATE OR REPLACE VIEW pending_proposals AS
SELECT
  p.*,
  (SELECT COUNT(*) FROM founder_friction_signals
   WHERE detected_at BETWEEN p.trigger_window_start AND p.trigger_window_end
  ) as signal_count
FROM founder_layout_proposals p
WHERE p.status = 'pending'
ORDER BY p.created_at DESC;

-- Vue des métriques agrégées par section (dernières 24h)
CREATE OR REPLACE VIEW section_metrics_24h AS
SELECT
  section_name,
  COUNT(DISTINCT session_id) as unique_sessions,
  COUNT(DISTINCT user_id) as unique_users,
  AVG(time_spent_ms) as avg_time_ms,
  AVG(scroll_depth_percent) as avg_scroll_depth,
  SUM(messages_sent) as total_messages
FROM founder_ux_metrics
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY section_name
ORDER BY avg_time_ms DESC;

-- ===============================================================================
-- FIN DU SCRIPT
-- ===============================================================================

-- Pour vérifier l'installation:
-- SELECT * FROM agents WHERE type LIKE '%_observer' OR type LIKE '%_analyst' OR type LIKE '%_architect' OR type LIKE '%_guardian';
-- SELECT * FROM pending_proposals;
-- SELECT * FROM section_metrics_24h;
