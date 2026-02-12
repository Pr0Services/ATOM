-- ===============================================================================
-- AT·OM - GRID TABLES SQL
-- Tables pour la grille planétaire et les connexions entre fondateurs
-- ===============================================================================
--
-- INSTRUCTIONS:
-- 1. Aller dans Supabase Dashboard > SQL Editor
-- 2. Copier-coller ce script EN ENTIER
-- 3. Cliquer "Run" (ignorer l'avertissement "destructive operation")
--
-- ===============================================================================

-- ===============================================================================
-- SECTION 1: TABLE GRID_NODES (Points sur la grille)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS grid_nodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  node_type TEXT DEFAULT 'founder',
  position_x DECIMAL(10, 6) NOT NULL,
  position_y DECIMAL(10, 6) NOT NULL,
  position_z DECIMAL(10, 6) DEFAULT 0,
  frequency DECIMAL(10, 2) DEFAULT 369,
  resonance_strength DECIMAL(5, 2) DEFAULT 1.0,
  metadata JSONB DEFAULT '{}',
  origin_context TEXT DEFAULT 'founder',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_grid_nodes_user ON grid_nodes(user_id);
CREATE INDEX IF NOT EXISTS idx_grid_nodes_type ON grid_nodes(node_type);
CREATE INDEX IF NOT EXISTS idx_grid_nodes_position ON grid_nodes(position_x, position_y);

-- RLS
ALTER TABLE grid_nodes ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view grid nodes" ON grid_nodes;
CREATE POLICY "Anyone can view grid nodes"
ON grid_nodes FOR SELECT
TO authenticated
USING (true);

DROP POLICY IF EXISTS "Users can create their node" ON grid_nodes;
CREATE POLICY "Users can create their node"
ON grid_nodes FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

DROP POLICY IF EXISTS "Users can update their node" ON grid_nodes;
CREATE POLICY "Users can update their node"
ON grid_nodes FOR UPDATE
TO authenticated
USING (user_id = auth.uid());

-- ===============================================================================
-- SECTION 2: TABLE GRID_CONNECTIONS (Liens entre nodes)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS grid_connections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  node_a_id UUID REFERENCES grid_nodes(id) ON DELETE CASCADE,
  node_b_id UUID REFERENCES grid_nodes(id) ON DELETE CASCADE,
  connection_type TEXT DEFAULT 'resonance',
  strength DECIMAL(5, 2) DEFAULT 1.0,
  bidirectional BOOLEAN DEFAULT TRUE,
  metadata JSONB DEFAULT '{}',
  origin_context TEXT DEFAULT 'founder',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(node_a_id, node_b_id)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_grid_connections_node_a ON grid_connections(node_a_id);
CREATE INDEX IF NOT EXISTS idx_grid_connections_node_b ON grid_connections(node_b_id);
CREATE INDEX IF NOT EXISTS idx_grid_connections_type ON grid_connections(connection_type);

-- RLS
ALTER TABLE grid_connections ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view connections" ON grid_connections;
CREATE POLICY "Anyone can view connections"
ON grid_connections FOR SELECT
TO authenticated
USING (true);

DROP POLICY IF EXISTS "Users can create connections from their node" ON grid_connections;
CREATE POLICY "Users can create connections from their node"
ON grid_connections FOR INSERT
TO authenticated
WITH CHECK (
  EXISTS (
    SELECT 1 FROM grid_nodes
    WHERE id = node_a_id AND user_id = auth.uid()
  )
);

-- ===============================================================================
-- SECTION 3: TABLE GRID_SECTORS (Zones de la grille)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS grid_sectors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sector_name TEXT NOT NULL UNIQUE,
  sector_code TEXT NOT NULL UNIQUE,
  center_x DECIMAL(10, 6) NOT NULL,
  center_y DECIMAL(10, 6) NOT NULL,
  radius DECIMAL(10, 6) NOT NULL,
  color TEXT DEFAULT '#FFD700',
  description TEXT,
  capacity INTEGER DEFAULT 12,
  current_count INTEGER DEFAULT 0,
  metadata JSONB DEFAULT '{}',
  origin_context TEXT DEFAULT 'founder',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_grid_sectors_code ON grid_sectors(sector_code);

-- RLS
ALTER TABLE grid_sectors ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view sectors" ON grid_sectors;
CREATE POLICY "Anyone can view sectors"
ON grid_sectors FOR SELECT
USING (true);

DROP POLICY IF EXISTS "Admins can manage sectors" ON grid_sectors;
CREATE POLICY "Admins can manage sectors"
ON grid_sectors FOR ALL
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  )
);

-- Insérer les 12 secteurs de base (Zodiaque énergétique)
INSERT INTO grid_sectors (sector_name, sector_code, center_x, center_y, radius, color, description, capacity)
VALUES
  ('Bélier', 'ARIES', 1.0, 0.0, 0.5, '#FF4444', 'Énergie d''initiative et de leadership', 12),
  ('Taureau', 'TAURUS', 0.866, 0.5, 0.5, '#44FF44', 'Stabilité et ancrage terrestre', 12),
  ('Gémeaux', 'GEMINI', 0.5, 0.866, 0.5, '#FFFF44', 'Communication et dualité', 12),
  ('Cancer', 'CANCER', 0.0, 1.0, 0.5, '#44FFFF', 'Protection et intuition', 12),
  ('Lion', 'LEO', -0.5, 0.866, 0.5, '#FF8844', 'Rayonnement et créativité', 12),
  ('Vierge', 'VIRGO', -0.866, 0.5, 0.5, '#88FF44', 'Analyse et service', 12),
  ('Balance', 'LIBRA', -1.0, 0.0, 0.5, '#FF44FF', 'Harmonie et équilibre', 12),
  ('Scorpion', 'SCORPIO', -0.866, -0.5, 0.5, '#880044', 'Transformation et profondeur', 12),
  ('Sagittaire', 'SAGITTARIUS', -0.5, -0.866, 0.5, '#8844FF', 'Expansion et vision', 12),
  ('Capricorne', 'CAPRICORN', 0.0, -1.0, 0.5, '#444444', 'Structure et accomplissement', 12),
  ('Verseau', 'AQUARIUS', 0.5, -0.866, 0.5, '#4488FF', 'Innovation et humanité', 12),
  ('Poissons', 'PISCES', 0.866, -0.5, 0.5, '#44FF88', 'Transcendance et compassion', 12)
ON CONFLICT (sector_code) DO NOTHING;

-- ===============================================================================
-- SECTION 4: FONCTIONS UTILITAIRES
-- ===============================================================================

-- Fonction: Créer un node pour un utilisateur
CREATE OR REPLACE FUNCTION create_grid_node(
  p_user_id UUID,
  p_position_x DECIMAL,
  p_position_y DECIMAL,
  p_position_z DECIMAL DEFAULT 0,
  p_frequency DECIMAL DEFAULT 369
)
RETURNS UUID AS $$
DECLARE
  v_node_id UUID;
BEGIN
  -- Vérifier si le user a déjà un node
  SELECT id INTO v_node_id FROM grid_nodes WHERE user_id = p_user_id;

  IF v_node_id IS NOT NULL THEN
    -- Mettre à jour le node existant
    UPDATE grid_nodes
    SET position_x = p_position_x,
        position_y = p_position_y,
        position_z = p_position_z,
        frequency = p_frequency,
        updated_at = NOW()
    WHERE id = v_node_id;
  ELSE
    -- Créer un nouveau node
    INSERT INTO grid_nodes (user_id, position_x, position_y, position_z, frequency)
    VALUES (p_user_id, p_position_x, p_position_y, p_position_z, p_frequency)
    RETURNING id INTO v_node_id;
  END IF;

  RETURN v_node_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Créer une connexion entre deux nodes
CREATE OR REPLACE FUNCTION create_grid_connection(
  p_node_a_id UUID,
  p_node_b_id UUID,
  p_connection_type TEXT DEFAULT 'resonance',
  p_strength DECIMAL DEFAULT 1.0
)
RETURNS UUID AS $$
DECLARE
  v_connection_id UUID;
BEGIN
  -- Vérifier que les deux nodes existent
  IF NOT EXISTS (SELECT 1 FROM grid_nodes WHERE id = p_node_a_id) THEN
    RAISE EXCEPTION 'Node A does not exist';
  END IF;

  IF NOT EXISTS (SELECT 1 FROM grid_nodes WHERE id = p_node_b_id) THEN
    RAISE EXCEPTION 'Node B does not exist';
  END IF;

  -- Créer la connexion (ou mettre à jour si elle existe)
  INSERT INTO grid_connections (node_a_id, node_b_id, connection_type, strength)
  VALUES (p_node_a_id, p_node_b_id, p_connection_type, p_strength)
  ON CONFLICT (node_a_id, node_b_id) DO UPDATE
  SET strength = EXCLUDED.strength, connection_type = EXCLUDED.connection_type
  RETURNING id INTO v_connection_id;

  RETURN v_connection_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction: Obtenir les nodes proches
CREATE OR REPLACE FUNCTION get_nearby_nodes(
  p_center_x DECIMAL,
  p_center_y DECIMAL,
  p_radius DECIMAL DEFAULT 0.5
)
RETURNS TABLE (
  node_id UUID,
  user_id UUID,
  distance DECIMAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    gn.id as node_id,
    gn.user_id,
    SQRT(POWER(gn.position_x - p_center_x, 2) + POWER(gn.position_y - p_center_y, 2))::DECIMAL as distance
  FROM grid_nodes gn
  WHERE SQRT(POWER(gn.position_x - p_center_x, 2) + POWER(gn.position_y - p_center_y, 2)) <= p_radius
  ORDER BY distance;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ===============================================================================
-- SECTION 5: ACTIVER REALTIME
-- ===============================================================================

DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE grid_nodes;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE grid_connections;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE grid_sectors;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;

-- ===============================================================================
-- FIN DU SCRIPT - GRID TABLES
-- ===============================================================================

-- Vérification:
-- SELECT * FROM grid_sectors;
-- SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'grid_%';
