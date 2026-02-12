-- ===============================================================================
-- AT*OM -- Missing Tables: Discovered During Schema Analysis
-- ===============================================================================
-- These tables were referenced in code or architecture documents but never
-- formally defined in SQL. This script creates them with proper types,
-- RLS policies, indexes, and Realtime support.
--
-- TABLES CREATED:
--   1. armors           -- ZAMA NFT armor data (referenced in save-zama-nft.js)
--   2. sphere_assignments -- Links users to sovereign spheres with roles
--   3. transformation_timeline -- User journey through the 7 alchemy stages
--   4. resonance_records -- Daily snapshot of user resonance across spheres
--
-- PREREQUISITES:
--   1. schema-rosetta.sql must be executed FIRST (defines enums)
--   2. 00-base-tables.sql must be applied (profiles table for RLS checks)
--
-- INSTRUCTIONS:
--   1. Supabase Dashboard > SQL Editor
--   2. Paste this entire script
--   3. Click "Run"
-- ===============================================================================


-- ===============================================================================
-- TABLE 1: armors
-- ===============================================================================
-- ZAMA NFT armor data. Referenced in services/database/save-zama-nft.js
-- but never formally defined. Stores the M/P/I/Po frequency measurements
-- for each minted armor token on Hedera.

CREATE TABLE IF NOT EXISTS armors (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  token_id         TEXT UNIQUE NOT NULL,                  -- Hedera token ID (e.g. 0.0.7780104)
  m_frequency      DECIMAL,                               -- Masse / Matiere (44.4 Hz)
  p_ratio          DECIMAL,                               -- Puissance / Potentiel (161.8 Hz, Phi x 100)
  i_sequence       DECIMAL,                               -- Intensite / Information (369 Hz, Tesla)
  po_stability     DECIMAL,                               -- Position / Polarite (1728 Hz, 12 cubed)
  image_url        TEXT,                                   -- URL to armor visual asset
  status           TEXT DEFAULT 'ACTIVE',                  -- ACTIVE, INACTIVE, REVOKED, TRANSFERRING
  owner_id         UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  hedera_metadata  JSONB,                                  -- Full Hedera token metadata payload
  created_at       TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE armors IS 'ZAMA NFT armors -- each armor carries M/P/I/Po frequency signature on Hedera';
COMMENT ON COLUMN armors.token_id IS 'Hedera token ID -- unique identifier on the Hedera network';
COMMENT ON COLUMN armors.m_frequency IS 'Masse/Matiere frequency component (sacred constant: 44.4 Hz)';
COMMENT ON COLUMN armors.p_ratio IS 'Puissance/Potentiel ratio (sacred constant: 161.8 Hz, Phi x 100)';
COMMENT ON COLUMN armors.i_sequence IS 'Intensite/Information sequence (sacred constant: 369 Hz, Tesla)';
COMMENT ON COLUMN armors.po_stability IS 'Position/Polarite stability (sacred constant: 1728 Hz, 12 cubed)';
COMMENT ON COLUMN armors.hedera_metadata IS 'Full Hedera token metadata including consensus timestamps and proofs';

-- Indexes
CREATE INDEX IF NOT EXISTS idx_armors_token ON armors(token_id);
CREATE INDEX IF NOT EXISTS idx_armors_owner ON armors(owner_id);
CREATE INDEX IF NOT EXISTS idx_armors_status ON armors(status);

-- RLS
ALTER TABLE armors ENABLE ROW LEVEL SECURITY;

-- Read: All authenticated users can view armors (transparency of the forge)
DROP POLICY IF EXISTS "armors_read_all" ON armors;
CREATE POLICY "armors_read_all" ON armors
  FOR SELECT
  TO authenticated
  USING (true);

-- Insert: Only admins/architects can mint new armors
DROP POLICY IF EXISTS "armors_admin_insert" ON armors;
CREATE POLICY "armors_admin_insert" ON armors
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Update: Owner can update their own armor, admins can update any
DROP POLICY IF EXISTS "armors_owner_update" ON armors;
CREATE POLICY "armors_owner_update" ON armors
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


-- ===============================================================================
-- TABLE 2: sphere_assignments
-- ===============================================================================
-- Links users to sovereign spheres with a specific role. A user can belong
-- to multiple spheres but only hold one role per sphere.

CREATE TABLE IF NOT EXISTS sphere_assignments (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  sphere_id   sphere_id NOT NULL,
  role        TEXT CHECK (role IN ('explorer', 'builder', 'guardian', 'architect')),
  assigned_at TIMESTAMPTZ DEFAULT NOW(),

  -- One assignment per user per sphere
  UNIQUE(user_id, sphere_id)
);

COMMENT ON TABLE sphere_assignments IS 'Assigns users to sovereign spheres with progression roles';
COMMENT ON COLUMN sphere_assignments.sphere_id IS 'One of the 9 sovereign spheres (TECHNO, POLITIQUE, ECONOMIE, etc.)';
COMMENT ON COLUMN sphere_assignments.role IS 'Progression role within the sphere: explorer -> builder -> guardian -> architect';

-- Indexes
CREATE INDEX IF NOT EXISTS idx_sphere_assign_user ON sphere_assignments(user_id);
CREATE INDEX IF NOT EXISTS idx_sphere_assign_sphere ON sphere_assignments(sphere_id);
CREATE INDEX IF NOT EXISTS idx_sphere_assign_role ON sphere_assignments(role);

-- RLS
ALTER TABLE sphere_assignments ENABLE ROW LEVEL SECURITY;

-- Read: All authenticated users can see sphere assignments (community transparency)
DROP POLICY IF EXISTS "sphere_assign_read_all" ON sphere_assignments;
CREATE POLICY "sphere_assign_read_all" ON sphere_assignments
  FOR SELECT
  TO authenticated
  USING (true);

-- Insert: Users can assign themselves, admins can assign anyone
DROP POLICY IF EXISTS "sphere_assign_self_insert" ON sphere_assignments;
CREATE POLICY "sphere_assign_self_insert" ON sphere_assignments
  FOR INSERT
  TO authenticated
  WITH CHECK (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Update: Only the assigned user or admins can change the role
DROP POLICY IF EXISTS "sphere_assign_owner_update" ON sphere_assignments;
CREATE POLICY "sphere_assign_owner_update" ON sphere_assignments
  FOR UPDATE
  TO authenticated
  USING (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Delete: Only admins can remove sphere assignments
DROP POLICY IF EXISTS "sphere_assign_admin_delete" ON sphere_assignments;
CREATE POLICY "sphere_assign_admin_delete" ON sphere_assignments
  FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );


-- ===============================================================================
-- TABLE 3: transformation_timeline
-- ===============================================================================
-- Records a user's journey through the 7 alchemical stages per node.
-- Each row is a stage transition event (from_stage -> to_stage).

CREATE TABLE IF NOT EXISTS transformation_timeline (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  node_id     UUID NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
  from_stage  alchemy_stage,                              -- NULL for initial entry
  to_stage    alchemy_stage,                              -- NULL for exit/archival
  reason      TEXT,                                       -- Why the transition happened
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE transformation_timeline IS 'User journey through the 7 alchemical stages -- each row is a stage transition';
COMMENT ON COLUMN transformation_timeline.from_stage IS 'Previous alchemy stage (NULL for initial entry into the process)';
COMMENT ON COLUMN transformation_timeline.to_stage IS 'New alchemy stage (NULL for exit or archival)';
COMMENT ON COLUMN transformation_timeline.reason IS 'Human-readable reason for the stage transition';

-- Indexes
CREATE INDEX IF NOT EXISTS idx_transform_timeline_user ON transformation_timeline(user_id);
CREATE INDEX IF NOT EXISTS idx_transform_timeline_node ON transformation_timeline(node_id);
CREATE INDEX IF NOT EXISTS idx_transform_timeline_to ON transformation_timeline(to_stage);
CREATE INDEX IF NOT EXISTS idx_transform_timeline_created ON transformation_timeline(created_at DESC);

-- RLS
ALTER TABLE transformation_timeline ENABLE ROW LEVEL SECURITY;

-- Read: Users can see their own timeline, admins can see all
DROP POLICY IF EXISTS "transform_timeline_own_read" ON transformation_timeline;
CREATE POLICY "transform_timeline_own_read" ON transformation_timeline
  FOR SELECT
  TO authenticated
  USING (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Insert: System or node owner can record transitions
DROP POLICY IF EXISTS "transform_timeline_insert" ON transformation_timeline;
CREATE POLICY "transform_timeline_insert" ON transformation_timeline
  FOR INSERT
  TO authenticated
  WITH CHECK (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );


-- ===============================================================================
-- TABLE 4: resonance_records
-- ===============================================================================
-- Daily snapshot of a user's resonance state across all spheres.
-- One record per user per day, capturing sphere-level scores and
-- the global system frequency / alignment score.

CREATE TABLE IF NOT EXISTS resonance_records (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  record_date      DATE DEFAULT CURRENT_DATE,
  sphere_scores    JSONB,                                  -- { "TECHNO": 7.2, "SANTE": 8.1, ... }
  system_frequency DECIMAL(10, 2),                         -- Overall system frequency for this user
  alignment_score  DECIMAL(5, 2),                          -- 0.00 to 100.00 alignment percentage
  created_at       TIMESTAMPTZ DEFAULT NOW(),

  -- One record per user per day
  UNIQUE(user_id, record_date)
);

COMMENT ON TABLE resonance_records IS 'Daily resonance snapshot per user -- sphere scores, frequency, and alignment';
COMMENT ON COLUMN resonance_records.sphere_scores IS 'JSONB object with per-sphere resonance scores, e.g. {"TECHNO": 7.2, "SANTE": 8.1}';
COMMENT ON COLUMN resonance_records.system_frequency IS 'Computed overall system frequency for this user on this date';
COMMENT ON COLUMN resonance_records.alignment_score IS 'Percentage (0-100) indicating alignment across all spheres';

-- Indexes
CREATE INDEX IF NOT EXISTS idx_resonance_records_user ON resonance_records(user_id);
CREATE INDEX IF NOT EXISTS idx_resonance_records_date ON resonance_records(record_date DESC);
CREATE INDEX IF NOT EXISTS idx_resonance_records_user_date ON resonance_records(user_id, record_date DESC);
CREATE INDEX IF NOT EXISTS idx_resonance_records_frequency ON resonance_records(system_frequency);
CREATE INDEX IF NOT EXISTS idx_resonance_records_scores ON resonance_records USING GIN(sphere_scores);

-- RLS
ALTER TABLE resonance_records ENABLE ROW LEVEL SECURITY;

-- Read: Users see their own records, admins see all
DROP POLICY IF EXISTS "resonance_own_read" ON resonance_records;
CREATE POLICY "resonance_own_read" ON resonance_records
  FOR SELECT
  TO authenticated
  USING (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Insert: Users can create their own daily record, system/admins can create for anyone
DROP POLICY IF EXISTS "resonance_insert" ON resonance_records;
CREATE POLICY "resonance_insert" ON resonance_records
  FOR INSERT
  TO authenticated
  WITH CHECK (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Update: Users can update their own record for today, admins can update any
DROP POLICY IF EXISTS "resonance_own_update" ON resonance_records;
CREATE POLICY "resonance_own_update" ON resonance_records
  FOR UPDATE
  TO authenticated
  USING (
    user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );


-- ===============================================================================
-- SECTION 5: ENABLE SUPABASE REALTIME FOR ALL NEW TABLES
-- ===============================================================================

DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE armors;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE sphere_assignments;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE transformation_timeline;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE resonance_records;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;


-- ===============================================================================
-- END OF SCRIPT -- MISSING TABLES
-- ===============================================================================

-- Verification queries:
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('armors', 'sphere_assignments', 'transformation_timeline', 'resonance_records');
-- SELECT * FROM armors LIMIT 1;
-- SELECT * FROM sphere_assignments LIMIT 1;
-- SELECT * FROM transformation_timeline LIMIT 1;
-- SELECT * FROM resonance_records LIMIT 1;
