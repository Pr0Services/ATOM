-- ===============================================================================
-- AT·OM - AGENTS INVITÉS SQL
-- Système d'agents IA invitables dans les rooms et threads
-- ===============================================================================

-- 1. TABLE: AGENTS (Définition des agents disponibles)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('facilitator', 'synthesis', 'memory')),
  description TEXT,
  provider TEXT DEFAULT 'claude',
  model TEXT DEFAULT 'claude-3-5-sonnet',
  capabilities JSONB DEFAULT '[]',
  default_objective TEXT,
  icon TEXT DEFAULT '🤖',
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);

-- Agents par défaut
INSERT INTO agents (name, type, description, default_objective, icon) VALUES
  ('Facilitateur', 'facilitator', 'Clarifie, reformule et aide à converger', 'Aider le groupe à clarifier ses idées et atteindre un consensus', '🎯'),
  ('Synthèse', 'synthesis', 'Observe et produit résumés, décisions, actions', 'Produire un résumé structuré des échanges', '📋'),
  ('Mémoire', 'memory', 'Extrait faits, décisions et accords pour archivage', 'Extraire et structurer les informations importantes', '🧠')
ON CONFLICT DO NOTHING;

-- 2. TABLE: AGENT_INSTANCES (Instances actives dans rooms/threads)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS agent_instances (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
  context_type TEXT NOT NULL CHECK (context_type IN ('room', 'thread', 'global')),
  context_id TEXT,  -- ID de la room ou du thread
  objective TEXT NOT NULL,
  mode TEXT DEFAULT 'observe' CHECK (mode IN ('observe', 'assist', 'active')),
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'stopped')),
  added_by UUID REFERENCES auth.users(id),
  added_by_name TEXT,
  config JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour les instances actives
CREATE INDEX IF NOT EXISTS idx_agent_instances_context
ON agent_instances(context_type, context_id) WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_agent_instances_agent
ON agent_instances(agent_id);

-- RLS
ALTER TABLE agent_instances ENABLE ROW LEVEL SECURITY;

-- Lecture pour tous les authentifiés
CREATE POLICY "Authenticated can view agent instances"
ON agent_instances FOR SELECT
TO authenticated
USING (true);

-- Création par les membres
CREATE POLICY "Members can create agent instances"
ON agent_instances FOR INSERT
TO authenticated
WITH CHECK (added_by = auth.uid());

-- Modification par le créateur ou admin
CREATE POLICY "Creators can update agent instances"
ON agent_instances FOR UPDATE
TO authenticated
USING (
  added_by = auth.uid()
  OR EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect')
  )
);

-- 3. TABLE: AGENT_OUTPUTS (Artefacts produits par les agents)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS agent_outputs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  instance_id UUID REFERENCES agent_instances(id) ON DELETE CASCADE,
  output_type TEXT NOT NULL CHECK (output_type IN (
    'summary', 'memory_candidate', 'plan', 'clarification',
    'decisions', 'actions', 'insights', 'extraction'
  )),
  title TEXT,
  content TEXT,
  payload JSONB DEFAULT '{}',
  validated BOOLEAN DEFAULT FALSE,
  validated_by UUID REFERENCES auth.users(id),
  validated_at TIMESTAMPTZ,
  archived BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour les outputs
CREATE INDEX IF NOT EXISTS idx_agent_outputs_instance
ON agent_outputs(instance_id);

CREATE INDEX IF NOT EXISTS idx_agent_outputs_type
ON agent_outputs(output_type);

CREATE INDEX IF NOT EXISTS idx_agent_outputs_pending
ON agent_outputs(validated) WHERE validated = FALSE;

-- RLS
ALTER TABLE agent_outputs ENABLE ROW LEVEL SECURITY;

-- Lecture pour tous les authentifiés
CREATE POLICY "Authenticated can view agent outputs"
ON agent_outputs FOR SELECT
TO authenticated
USING (true);

-- Création par le système (via service role)
CREATE POLICY "System can create agent outputs"
ON agent_outputs FOR INSERT
TO authenticated
WITH CHECK (true);

-- Validation par les membres
CREATE POLICY "Members can validate agent outputs"
ON agent_outputs FOR UPDATE
TO authenticated
USING (true)
WITH CHECK (true);

-- 4. TABLE: AGENT_MESSAGES (Messages des agents dans les discussions)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS agent_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  instance_id UUID REFERENCES agent_instances(id) ON DELETE CASCADE,
  context_type TEXT NOT NULL,
  context_id TEXT,
  content TEXT NOT NULL,
  message_type TEXT DEFAULT 'response' CHECK (message_type IN (
    'response', 'summary', 'question', 'clarification', 'suggestion'
  )),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_agent_messages_context
ON agent_messages(context_type, context_id);

-- RLS
ALTER TABLE agent_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated can view agent messages"
ON agent_messages FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "System can create agent messages"
ON agent_messages FOR INSERT
TO authenticated
WITH CHECK (true);

-- 5. TABLE: VALIDATED_MEMORY (Mémoire validée par les humains)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS validated_memory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_output_id UUID REFERENCES agent_outputs(id),
  memory_type TEXT NOT NULL CHECK (memory_type IN (
    'fact', 'decision', 'agreement', 'action', 'insight'
  )),
  content TEXT NOT NULL,
  context TEXT,
  tags TEXT[],
  importance INTEGER DEFAULT 5 CHECK (importance BETWEEN 1 AND 10),
  validated_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ  -- NULL = permanent
);

-- Index pour la recherche
CREATE INDEX IF NOT EXISTS idx_validated_memory_type
ON validated_memory(memory_type);

CREATE INDEX IF NOT EXISTS idx_validated_memory_tags
ON validated_memory USING GIN(tags);

-- RLS
ALTER TABLE validated_memory ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated can view validated memory"
ON validated_memory FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "Validators can create memory"
ON validated_memory FOR INSERT
TO authenticated
WITH CHECK (validated_by = auth.uid());

-- 6. REALTIME
-- ===============================================================================

ALTER PUBLICATION supabase_realtime ADD TABLE agent_instances;
ALTER PUBLICATION supabase_realtime ADD TABLE agent_outputs;
ALTER PUBLICATION supabase_realtime ADD TABLE agent_messages;

-- 7. FONCTIONS UTILITAIRES
-- ===============================================================================

-- Fonction pour ajouter un agent à un contexte
CREATE OR REPLACE FUNCTION add_agent_to_context(
  p_agent_type TEXT,
  p_context_type TEXT,
  p_context_id TEXT,
  p_objective TEXT,
  p_mode TEXT DEFAULT 'observe'
)
RETURNS UUID AS $$
DECLARE
  v_agent_id UUID;
  v_instance_id UUID;
BEGIN
  -- Trouver l'agent
  SELECT id INTO v_agent_id FROM agents WHERE type = p_agent_type AND is_active = TRUE LIMIT 1;

  IF v_agent_id IS NULL THEN
    RAISE EXCEPTION 'Agent type not found: %', p_agent_type;
  END IF;

  -- Créer l'instance
  INSERT INTO agent_instances (agent_id, context_type, context_id, objective, mode, added_by)
  VALUES (v_agent_id, p_context_type, p_context_id, p_objective, p_mode, auth.uid())
  RETURNING id INTO v_instance_id;

  RETURN v_instance_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour retirer un agent
CREATE OR REPLACE FUNCTION remove_agent_from_context(p_instance_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  UPDATE agent_instances
  SET status = 'stopped', updated_at = NOW()
  WHERE id = p_instance_id
  AND (added_by = auth.uid() OR EXISTS (
    SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin', 'architect')
  ));

  RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour valider un output d'agent
CREATE OR REPLACE FUNCTION validate_agent_output(
  p_output_id UUID,
  p_create_memory BOOLEAN DEFAULT FALSE,
  p_memory_type TEXT DEFAULT 'insight'
)
RETURNS BOOLEAN AS $$
DECLARE
  v_output RECORD;
BEGIN
  -- Marquer comme validé
  UPDATE agent_outputs
  SET validated = TRUE, validated_by = auth.uid(), validated_at = NOW()
  WHERE id = p_output_id
  RETURNING * INTO v_output;

  IF NOT FOUND THEN
    RETURN FALSE;
  END IF;

  -- Créer une entrée mémoire si demandé
  IF p_create_memory THEN
    INSERT INTO validated_memory (source_output_id, memory_type, content, validated_by)
    VALUES (p_output_id, p_memory_type, v_output.content, auth.uid());
  END IF;

  RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===============================================================================
-- FIN DU SCRIPT
-- ===============================================================================

-- Pour vérifier l'installation:
-- SELECT * FROM agents;
-- SELECT * FROM agent_instances WHERE status = 'active';
-- SELECT * FROM agent_outputs WHERE validated = FALSE;
