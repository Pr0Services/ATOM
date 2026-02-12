-- ===============================================================================
-- AT*OM -- Migration: Connect Founder-Phase Schema to Rosetta Core
-- ===============================================================================
-- This migration adds linking columns from existing founder-phase tables
-- (services/database/) to the new rosetta-core schema (schema-rosetta.sql).
-- It also enables Supabase Realtime for all rosetta-core tables and creates
-- the polymorphic entity_references table.
--
-- PREREQUISITES:
--   1. schema-rosetta.sql must be executed FIRST (defines enums + core tables)
--   2. All founder-phase SQL scripts must already be applied
--
-- INSTRUCTIONS:
--   1. Supabase Dashboard > SQL Editor
--   2. Paste this entire script
--   3. Click "Run"
-- ===============================================================================


-- ===============================================================================
-- SECTION 1: ALTER EXISTING FOUNDER TABLES -- ADD ROSETTA LINKING COLUMNS
-- ===============================================================================

-- -----------------------------------------------------------------------------
-- 1.1 agent_outputs: Link to rosetta_mappings + alchemy_stage
-- Connects agent AI outputs to the Rosetta tri-dimensional mapping and
-- tracks which alchemical stage the output corresponds to.
-- -----------------------------------------------------------------------------
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'agent_outputs' AND column_name = 'rosetta_mapping_id'
  ) THEN
    ALTER TABLE agent_outputs
      ADD COLUMN rosetta_mapping_id UUID REFERENCES rosetta_mappings(id) ON DELETE SET NULL;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'agent_outputs' AND column_name = 'alchemy_stage'
  ) THEN
    ALTER TABLE agent_outputs
      ADD COLUMN alchemy_stage alchemy_stage;
  END IF;
END $$;

COMMENT ON COLUMN agent_outputs.rosetta_mapping_id IS 'FK to rosetta_mappings -- links agent output to its Rosetta tri-dimensional translation';
COMMENT ON COLUMN agent_outputs.alchemy_stage IS 'Alchemical stage this output corresponds to (7 stages of transformation)';

CREATE INDEX IF NOT EXISTS idx_agent_outputs_rosetta ON agent_outputs(rosetta_mapping_id);
CREATE INDEX IF NOT EXISTS idx_agent_outputs_alchemy ON agent_outputs(alchemy_stage);

-- -----------------------------------------------------------------------------
-- 1.2 user_biometrics: Link to nodes + rosetta_mappings
-- Anchors each biometric measurement to a node in the Tree of Life and
-- its Rosetta mapping for tri-dimensional interpretation.
-- -----------------------------------------------------------------------------
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'user_biometrics' AND column_name = 'node_id'
  ) THEN
    ALTER TABLE user_biometrics
      ADD COLUMN node_id UUID REFERENCES nodes(id) ON DELETE SET NULL;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'user_biometrics' AND column_name = 'rosetta_mapping_id'
  ) THEN
    ALTER TABLE user_biometrics
      ADD COLUMN rosetta_mapping_id UUID REFERENCES rosetta_mappings(id) ON DELETE SET NULL;
  END IF;
END $$;

COMMENT ON COLUMN user_biometrics.node_id IS 'FK to nodes -- anchors biometric data to a node in the Tree of Life';
COMMENT ON COLUMN user_biometrics.rosetta_mapping_id IS 'FK to rosetta_mappings -- links biometric data to its Rosetta translation';

CREATE INDEX IF NOT EXISTS idx_user_biometrics_node ON user_biometrics(node_id);
CREATE INDEX IF NOT EXISTS idx_user_biometrics_rosetta ON user_biometrics(rosetta_mapping_id);

-- -----------------------------------------------------------------------------
-- 1.3 founder_ux_metrics: Link to vibrational_logs + sphere_id
-- Associates UX behavioral data with vibrational frequency logs and
-- assigns each metric to one of the 9 sovereign spheres.
-- -----------------------------------------------------------------------------
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'founder_ux_metrics' AND column_name = 'vibrational_log_id'
  ) THEN
    ALTER TABLE founder_ux_metrics
      ADD COLUMN vibrational_log_id UUID REFERENCES vibrational_logs(id) ON DELETE SET NULL;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'founder_ux_metrics' AND column_name = 'sphere_id'
  ) THEN
    ALTER TABLE founder_ux_metrics
      ADD COLUMN sphere_id sphere_id;
  END IF;
END $$;

COMMENT ON COLUMN founder_ux_metrics.vibrational_log_id IS 'FK to vibrational_logs -- correlates UX behavior with frequency activation';
COMMENT ON COLUMN founder_ux_metrics.sphere_id IS 'Sovereign sphere this metric belongs to (9 spheres)';

CREATE INDEX IF NOT EXISTS idx_founder_ux_metrics_viblog ON founder_ux_metrics(vibrational_log_id);
CREATE INDEX IF NOT EXISTS idx_founder_ux_metrics_sphere ON founder_ux_metrics(sphere_id);

-- -----------------------------------------------------------------------------
-- 1.4 grid_nodes: Link to rosetta nodes + sphere_id
-- Bridges the planetary grid (founder-phase) to the Tree of Life node
-- system and assigns each grid point to a sovereign sphere.
-- -----------------------------------------------------------------------------
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'grid_nodes' AND column_name = 'node_id'
  ) THEN
    ALTER TABLE grid_nodes
      ADD COLUMN node_id UUID REFERENCES nodes(id) ON DELETE SET NULL;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'grid_nodes' AND column_name = 'sphere_id'
  ) THEN
    ALTER TABLE grid_nodes
      ADD COLUMN sphere_id sphere_id;
  END IF;
END $$;

COMMENT ON COLUMN grid_nodes.node_id IS 'FK to nodes -- bridges grid point to its Tree of Life node';
COMMENT ON COLUMN grid_nodes.sphere_id IS 'Sovereign sphere this grid node belongs to (9 spheres)';

CREATE INDEX IF NOT EXISTS idx_grid_nodes_rosetta_node ON grid_nodes(node_id);
CREATE INDEX IF NOT EXISTS idx_grid_nodes_sphere ON grid_nodes(sphere_id);

-- -----------------------------------------------------------------------------
-- 1.5 founder_friction_signals: Link to alchemy_validations
-- Connects detected friction signals to the alchemical validation process,
-- enabling friction resolution through the 7-stage transformation.
-- -----------------------------------------------------------------------------
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'founder_friction_signals' AND column_name = 'alchemy_validation_id'
  ) THEN
    ALTER TABLE founder_friction_signals
      ADD COLUMN alchemy_validation_id UUID REFERENCES alchemy_validations(id) ON DELETE SET NULL;
  END IF;
END $$;

COMMENT ON COLUMN founder_friction_signals.alchemy_validation_id IS 'FK to alchemy_validations -- links friction to its alchemical resolution process';

CREATE INDEX IF NOT EXISTS idx_friction_signals_alchemy ON founder_friction_signals(alchemy_validation_id);

-- -----------------------------------------------------------------------------
-- 1.6 founder_layout_proposals: Link to gear_events
-- Associates layout proposals with Antikythera gear events, tracking
-- how layout changes propagate across spheres.
-- -----------------------------------------------------------------------------
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'founder_layout_proposals' AND column_name = 'gear_event_id'
  ) THEN
    ALTER TABLE founder_layout_proposals
      ADD COLUMN gear_event_id UUID REFERENCES gear_events(id) ON DELETE SET NULL;
  END IF;
END $$;

COMMENT ON COLUMN founder_layout_proposals.gear_event_id IS 'FK to gear_events -- tracks layout change propagation via Antikythera mechanism';

CREATE INDEX IF NOT EXISTS idx_layout_proposals_gear ON founder_layout_proposals(gear_event_id);


-- ===============================================================================
-- SECTION 2: ENABLE SUPABASE REALTIME FOR ALL ROSETTA-CORE TABLES
-- ===============================================================================
-- Wrapped in exception handlers to be idempotent (safe to re-run).

DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE nodes;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE rosetta_mappings;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE vibrational_logs;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE gear_events;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE alchemy_validations;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE alchemy_transformation_log;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE spiral_positions;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE hedera_proofs;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE universal_constants;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;


-- ===============================================================================
-- SECTION 3: POLYMORPHIC ENTITY REFERENCES TABLE
-- ===============================================================================
-- A universal reference table that can point to any entity across both
-- the founder-phase and rosetta-core schemas. Enables cross-schema lookups,
-- activity feeds, and flexible entity linking without hard FK coupling.

CREATE TABLE IF NOT EXISTS entity_references (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_type TEXT NOT NULL,              -- e.g. 'node', 'agent_output', 'grid_node', 'biometric', 'armor'
  entity_id   UUID NOT NULL,              -- PK of the referenced entity
  sphere_id   sphere_id,                  -- Optional sphere assignment
  owner_id    UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW(),

  -- Each entity can only be referenced once per type
  UNIQUE(entity_type, entity_id)
);

COMMENT ON TABLE entity_references IS 'Polymorphic reference table bridging founder-phase and rosetta-core entities';
COMMENT ON COLUMN entity_references.entity_type IS 'Discriminator: node, agent_output, grid_node, biometric, armor, vibrational_log, etc.';
COMMENT ON COLUMN entity_references.entity_id IS 'UUID primary key of the referenced entity in its source table';
COMMENT ON COLUMN entity_references.sphere_id IS 'Optional assignment to one of the 9 sovereign spheres';
COMMENT ON COLUMN entity_references.owner_id IS 'User who owns or created the referenced entity';

-- Indexes
CREATE INDEX IF NOT EXISTS idx_entity_refs_type ON entity_references(entity_type);
CREATE INDEX IF NOT EXISTS idx_entity_refs_entity ON entity_references(entity_id);
CREATE INDEX IF NOT EXISTS idx_entity_refs_sphere ON entity_references(sphere_id);
CREATE INDEX IF NOT EXISTS idx_entity_refs_owner ON entity_references(owner_id);
CREATE INDEX IF NOT EXISTS idx_entity_refs_type_sphere ON entity_references(entity_type, sphere_id);

-- RLS
ALTER TABLE entity_references ENABLE ROW LEVEL SECURITY;

-- Read: All authenticated users can read entity references (transparency)
DROP POLICY IF EXISTS "entity_refs_read_all" ON entity_references;
CREATE POLICY "entity_refs_read_all" ON entity_references
  FOR SELECT
  TO authenticated
  USING (true);

-- Write: Only the owner or admins can create/update entity references
DROP POLICY IF EXISTS "entity_refs_owner_write" ON entity_references;
CREATE POLICY "entity_refs_owner_write" ON entity_references
  FOR INSERT
  TO authenticated
  WITH CHECK (
    owner_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

DROP POLICY IF EXISTS "entity_refs_owner_update" ON entity_references;
CREATE POLICY "entity_refs_owner_update" ON entity_references
  FOR UPDATE
  TO authenticated
  USING (
    owner_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Realtime
DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE entity_references;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;


-- ===============================================================================
-- END OF MIGRATION -- CONNECT SCHEMAS
-- ===============================================================================

-- Verification queries:
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'agent_outputs' AND column_name IN ('rosetta_mapping_id', 'alchemy_stage');
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'user_biometrics' AND column_name IN ('node_id', 'rosetta_mapping_id');
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'founder_ux_metrics' AND column_name IN ('vibrational_log_id', 'sphere_id');
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'grid_nodes' AND column_name IN ('node_id', 'sphere_id');
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'founder_friction_signals' AND column_name = 'alchemy_validation_id';
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'founder_layout_proposals' AND column_name = 'gear_event_id';
-- SELECT * FROM entity_references LIMIT 1;
