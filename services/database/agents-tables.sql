-- ===============================================================================
-- AT·OM - AGENTS TABLES SQL
-- Système d'agents IA pour la plateforme
-- ===============================================================================
--
-- INSTRUCTIONS:
-- 1. Aller dans Supabase Dashboard > SQL Editor
-- 2. Copier-coller ce script EN ENTIER
-- 3. Cliquer "Run" (ignorer l'avertissement "destructive operation")
--
-- ===============================================================================

-- ===============================================================================
-- SECTION 1: TABLE AGENTS (Définition des agents)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_type TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  description TEXT,
  capabilities JSONB DEFAULT '[]',
  config JSONB DEFAULT '{}',
  is_active BOOLEAN DEFAULT TRUE,
  origin_context TEXT DEFAULT 'founder',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(agent_type);
CREATE INDEX IF NOT EXISTS idx_agents_active ON agents(is_active);

-- RLS
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view agents" ON agents;
CREATE POLICY "Anyone can view agents"
ON agents FOR SELECT
USING (true);

DROP POLICY IF EXISTS "Only admins can modify agents" ON agents;
CREATE POLICY "Only admins can modify agents"
ON agents FOR ALL
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

-- Insérer les agents de base (s'ils n'existent pas)
INSERT INTO agents (agent_type, display_name, description, capabilities, config)
VALUES
  ('facilitator', 'Agent Facilitateur', 'Facilite les conversations et aide les utilisateurs',
   '["conversation", "guidance", "help"]'::jsonb,
   '{"tone": "helpful", "language": "fr"}'::jsonb),
  ('synthesis', 'Agent de Synthèse', 'Résume les discussions et extrait les points clés',
   '["summarize", "extract", "analyze"]'::jsonb,
   '{"max_length": 500}'::jsonb),
  ('memory', 'Agent Mémoire', 'Conserve et retrouve les informations importantes',
   '["store", "retrieve", "connect"]'::jsonb,
   '{"retention_days": 365}'::jsonb)
ON CONFLICT (agent_type) DO NOTHING;

-- ===============================================================================
-- SECTION 2: TABLE AGENT_INSTANCES (Sessions actives des agents)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS agent_instances (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
  context_type TEXT NOT NULL,
  context_id UUID,
  status TEXT DEFAULT 'active',
  metadata JSONB DEFAULT '{}',
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ
);

-- Index
CREATE INDEX IF NOT EXISTS idx_agent_instances_agent ON agent_instances(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_instances_context ON agent_instances(context_type, context_id);
CREATE INDEX IF NOT EXISTS idx_agent_instances_status ON agent_instances(status);

-- RLS
ALTER TABLE agent_instances ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Authenticated can view agent instances" ON agent_instances;
CREATE POLICY "Authenticated can view agent instances"
ON agent_instances FOR SELECT
TO authenticated
USING (true);

DROP POLICY IF EXISTS "System can manage agent instances" ON agent_instances;
CREATE POLICY "System can manage agent instances"
ON agent_instances FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

-- ===============================================================================
-- SECTION 3: TABLE AGENT_OUTPUTS (Sorties/Réponses des agents)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS agent_outputs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  instance_id UUID REFERENCES agent_instances(id) ON DELETE CASCADE,
  output_type TEXT NOT NULL,
  content JSONB NOT NULL,
  confidence DECIMAL(3, 2),
  validated BOOLEAN DEFAULT FALSE,
  validated_by UUID REFERENCES auth.users(id),
  validated_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_agent_outputs_instance ON agent_outputs(instance_id);
CREATE INDEX IF NOT EXISTS idx_agent_outputs_type ON agent_outputs(output_type);
CREATE INDEX IF NOT EXISTS idx_agent_outputs_validated ON agent_outputs(validated);

-- RLS
ALTER TABLE agent_outputs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Authenticated can view agent outputs" ON agent_outputs;
CREATE POLICY "Authenticated can view agent outputs"
ON agent_outputs FOR SELECT
TO authenticated
USING (true);

DROP POLICY IF EXISTS "System can create agent outputs" ON agent_outputs;
CREATE POLICY "System can create agent outputs"
ON agent_outputs FOR INSERT
TO authenticated
WITH CHECK (true);

DROP POLICY IF EXISTS "Admins can validate outputs" ON agent_outputs;
CREATE POLICY "Admins can validate outputs"
ON agent_outputs FOR UPDATE
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

-- ===============================================================================
-- SECTION 4: TABLE AGENT_MESSAGES (Messages entre agents et utilisateurs)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS agent_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  instance_id UUID REFERENCES agent_instances(id) ON DELETE CASCADE,
  sender_type TEXT NOT NULL,
  sender_id TEXT,
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_agent_messages_instance ON agent_messages(instance_id);
CREATE INDEX IF NOT EXISTS idx_agent_messages_created ON agent_messages(created_at);

-- RLS
ALTER TABLE agent_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Authenticated can view agent messages" ON agent_messages;
CREATE POLICY "Authenticated can view agent messages"
ON agent_messages FOR SELECT
TO authenticated
USING (true);

DROP POLICY IF EXISTS "Authenticated can send agent messages" ON agent_messages;
CREATE POLICY "Authenticated can send agent messages"
ON agent_messages FOR INSERT
TO authenticated
WITH CHECK (true);

-- ===============================================================================
-- SECTION 5: TABLE VALIDATED_MEMORY (Mémoire validée par les humains)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS validated_memory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  memory_type TEXT NOT NULL,
  title TEXT NOT NULL,
  content JSONB NOT NULL,
  source_output_id UUID REFERENCES agent_outputs(id),
  validated_by UUID REFERENCES auth.users(id),
  tags TEXT[] DEFAULT '{}',
  importance INTEGER DEFAULT 1,
  origin_context TEXT DEFAULT 'founder',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

-- Index
CREATE INDEX IF NOT EXISTS idx_validated_memory_type ON validated_memory(memory_type);
CREATE INDEX IF NOT EXISTS idx_validated_memory_tags ON validated_memory USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_validated_memory_importance ON validated_memory(importance DESC);

-- RLS
ALTER TABLE validated_memory ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Authenticated can view validated memory" ON validated_memory;
CREATE POLICY "Authenticated can view validated memory"
ON validated_memory FOR SELECT
TO authenticated
USING (true);

DROP POLICY IF EXISTS "Admins can manage validated memory" ON validated_memory;
CREATE POLICY "Admins can manage validated memory"
ON validated_memory FOR ALL
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

-- ===============================================================================
-- SECTION 6: FONCTIONS UTILITAIRES
-- ===============================================================================

-- Fonction: Ajouter un agent à un contexte
CREATE OR REPLACE FUNCTION add_agent_to_context(
  p_agent_type TEXT,
  p_context_type TEXT,
  p_context_id UUID DEFAULT NULL,
  p_metadata JSONB DEFAULT '{}'
)
RETURNS UUID AS $$
DECLARE
  v_agent_id UUID;
  v_instance_id UUID;
BEGIN
  -- Trouver l'agent
  SELECT id INTO v_agent_id FROM agents WHERE agent_type = p_agent_type AND is_active = TRUE;

  IF v_agent_id IS NULL THEN
    RAISE EXCEPTION 'Agent % not found or not active', p_agent_type;
  END IF;

  -- Créer l'instance
  INSERT INTO agent_instances (agent_id, context_type, context_id, metadata)
  VALUES (v_agent_id, p_context_type, p_context_id, p_metadata)
  RETURNING id INTO v_instance_id;

  RETURN v_instance_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Retirer un agent d'un contexte
CREATE OR REPLACE FUNCTION remove_agent_from_context(
  p_instance_id UUID
)
RETURNS BOOLEAN AS $$
BEGIN
  UPDATE agent_instances
  SET status = 'ended', ended_at = NOW()
  WHERE id = p_instance_id;

  RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Valider une sortie d'agent
CREATE OR REPLACE FUNCTION validate_agent_output(
  p_output_id UUID,
  p_validator_id UUID
)
RETURNS BOOLEAN AS $$
BEGIN
  UPDATE agent_outputs
  SET validated = TRUE, validated_by = p_validator_id, validated_at = NOW()
  WHERE id = p_output_id;

  RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===============================================================================
-- SECTION 7: ACTIVER REALTIME
-- ===============================================================================

DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE agents;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE agent_instances;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE agent_outputs;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE agent_messages;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;

-- ===============================================================================
-- FIN DU SCRIPT - AGENTS TABLES
-- ===============================================================================

-- Vérification:
-- SELECT * FROM agents;
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'agent%';
