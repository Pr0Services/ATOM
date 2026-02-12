-- ═══════════════════════════════════════════════════════════
-- AT·OM — Schéma SQL Rosetta Core
-- Architecture tri-dimensionnelle (Pierre de Rosette)
-- Supabase / PostgreSQL avec Row Level Security
-- ═══════════════════════════════════════════════════════════

-- Extension UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ═══════════════════════════════════════════════════════════
-- TYPES ÉNUMÉRÉS
-- ═══════════════════════════════════════════════════════════

CREATE TYPE sphere_id AS ENUM (
  'TECHNO', 'POLITIQUE', 'ECONOMIE', 'EDUCATION', 'SANTE',
  'CULTURE', 'ENVIRONNEMENT', 'JUSTICE', 'SPIRITUALITE'
);

CREATE TYPE node_status AS ENUM (
  'genesis', 'active', 'polishing', 'aligned', 'archived'
);

CREATE TYPE alchemy_stage AS ENUM (
  'CALCINATION', 'DISSOLUTION', 'SEPARATION', 'CONJUNCTION',
  'FERMENTATION', 'DISTILLATION', 'COAGULATION'
);

CREATE TYPE rosetta_dimension AS ENUM ('TECH', 'PEOPLE', 'SPIRIT');

CREATE TYPE gear_event_type AS ENUM ('mutation', 'resonance', 'cascade', 'alignment');

CREATE TYPE emotional_tone AS ENUM ('neutre', 'encourageant', 'alerte', 'celebratoire', 'sacre');

-- ═══════════════════════════════════════════════════════════
-- TABLE : universal_constants
-- Les constantes sacrées immuables du système
-- ═══════════════════════════════════════════════════════════

CREATE TABLE universal_constants (
  key         TEXT PRIMARY KEY,
  value       NUMERIC NOT NULL,
  unit        TEXT,
  description TEXT,
  created_at  TIMESTAMPTZ DEFAULT now()
);

INSERT INTO universal_constants (key, value, unit, description) VALUES
  ('ATOM_M',     44.4,                'Hz',    'Masse / Matière'),
  ('ATOM_P',     161.8,               'Hz',    'Puissance / Potentiel (Phi × 100)'),
  ('ATOM_I',     369,                 'Hz',    'Intensité / Information (Tesla)'),
  ('ATOM_PO',    1728,                'Hz',    'Position / Polarité (12³)'),
  ('HEARTBEAT',  444,                 'Hz',    'Ancre du système'),
  ('SOURCE',     999,                 'Hz',    'Fréquence d''unité maximale'),
  ('LOVE',       528,                 'Hz',    'Fréquence de résonance'),
  ('PHI',        1.6180339887498949,  'ratio', 'Nombre d''Or'),
  ('POINT_ZERO_LAT', 21.4,           'deg',   'Latitude Cratère Chicxulub'),
  ('POINT_ZERO_LON', -89.5,          'deg',   'Longitude Cratère Chicxulub'),
  ('CRATER_RADIUS',  100,            'km',    'Rayon d''activation');

-- ═══════════════════════════════════════════════════════════
-- TABLE : nodes
-- Table maîtresse — chaque ligne est un point dans l'Arbre de Vie
-- ═══════════════════════════════════════════════════════════

CREATE TABLE nodes (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  parent_id       UUID REFERENCES nodes(id) ON DELETE SET NULL,
  sphere_id       sphere_id NOT NULL,
  title           TEXT NOT NULL,
  status          node_status DEFAULT 'active',
  depth           INTEGER DEFAULT 0,
  spiral_position NUMERIC DEFAULT 0,          -- Phaistos: angle en radians
  spiral_ring     INTEGER DEFAULT 0,          -- Phaistos: anneau
  resonance_level INTEGER CHECK (resonance_level BETWEEN 1 AND 9),
  created_by      UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_nodes_sphere ON nodes(sphere_id);
CREATE INDEX idx_nodes_parent ON nodes(parent_id);
CREATE INDEX idx_nodes_status ON nodes(status);
CREATE INDEX idx_nodes_resonance ON nodes(resonance_level);

-- ═══════════════════════════════════════════════════════════
-- TABLE : rosetta_mappings
-- Le cœur Rosetta — chaque node traduit en 3 dimensions
-- ═══════════════════════════════════════════════════════════

CREATE TABLE rosetta_mappings (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  node_id           UUID NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,

  -- Dimension TECH (Grec) — Logique pure
  tech_payload      JSONB NOT NULL,

  -- Dimension PEOPLE (Démotique) — Narration humaine
  people_narrative  TEXT NOT NULL,
  people_explanation TEXT,
  people_guide_steps TEXT[],
  people_tone       emotional_tone DEFAULT 'neutre',

  -- Dimension SPIRIT (Hiéroglyphe) — Vibration
  spirit_payload    JSONB NOT NULL,
  -- Structure spirit_payload attendue :
  -- {
  --   "frequency_hz": 444,
  --   "resonance_level": 4,
  --   "color": "#50C878",
  --   "sacred_geometry": "tetrahedron",
  --   "vibration_signature": [44.4, 161.8, 369, 1728],
  --   "phi_ratio": 1.618
  -- }

  source_dimension  rosetta_dimension DEFAULT 'TECH',
  integrity_hash    TEXT NOT NULL,
  created_at        TIMESTAMPTZ DEFAULT now(),

  -- Contrainte : un seul mapping actif par node
  UNIQUE(node_id)
);

CREATE INDEX idx_rosetta_node ON rosetta_mappings(node_id);
CREATE INDEX idx_rosetta_tech ON rosetta_mappings USING gin(tech_payload);
CREATE INDEX idx_rosetta_spirit ON rosetta_mappings USING gin(spirit_payload);

-- ═══════════════════════════════════════════════════════════
-- TABLE : vibrational_logs
-- Historique des activations fréquentielles
-- ═══════════════════════════════════════════════════════════

CREATE TABLE vibrational_logs (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id           UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  frequency_hz      NUMERIC NOT NULL,
  resonance_level   INTEGER CHECK (resonance_level BETWEEN 1 AND 9),
  latitude          NUMERIC,
  longitude         NUMERIC,
  distance_to_zero  NUMERIC,                  -- km depuis Chicxulub
  is_in_crater      BOOLEAN DEFAULT false,
  mode              TEXT DEFAULT 'standard',
  node_id           UUID REFERENCES nodes(id) ON DELETE SET NULL,
  metadata          JSONB,
  created_at        TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_viblog_user ON vibrational_logs(user_id);
CREATE INDEX idx_viblog_freq ON vibrational_logs(frequency_hz);
CREATE INDEX idx_viblog_crater ON vibrational_logs(is_in_crater) WHERE is_in_crater = true;
CREATE INDEX idx_viblog_time ON vibrational_logs(created_at DESC);

-- ═══════════════════════════════════════════════════════════
-- TABLE : gear_events (Machine d'Anticythère)
-- Propagation des changements entre sphères
-- ═══════════════════════════════════════════════════════════

CREATE TABLE gear_events (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_sphere     sphere_id NOT NULL,
  target_spheres    sphere_id[] NOT NULL,
  event_type        gear_event_type DEFAULT 'mutation',
  payload           JSONB NOT NULL,
  propagation_depth INTEGER DEFAULT 0,
  parent_event_id   UUID REFERENCES gear_events(id) ON DELETE SET NULL,
  created_at        TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_gear_source ON gear_events(source_sphere);
CREATE INDEX idx_gear_type ON gear_events(event_type);
CREATE INDEX idx_gear_parent ON gear_events(parent_event_id);

-- ═══════════════════════════════════════════════════════════
-- TABLE : alchemy_validations (Table d'Émeraude)
-- 7 niveaux de transformation alchimique par node
-- ═══════════════════════════════════════════════════════════

CREATE TABLE alchemy_validations (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  node_id         UUID NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
  current_stage   alchemy_stage NOT NULL,
  stage_index     INTEGER CHECK (stage_index BETWEEN 1 AND 7),
  is_aligned      BOOLEAN DEFAULT false,
  polishing_notes TEXT[],
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_alchemy_node ON alchemy_validations(node_id);
CREATE INDEX idx_alchemy_aligned ON alchemy_validations(is_aligned) WHERE is_aligned = false;

-- ═══════════════════════════════════════════════════════════
-- TABLE : alchemy_transformation_log
-- Journal détaillé de chaque étape de transformation
-- ═══════════════════════════════════════════════════════════

CREATE TABLE alchemy_transformation_log (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  validation_id   UUID NOT NULL REFERENCES alchemy_validations(id) ON DELETE CASCADE,
  stage           alchemy_stage NOT NULL,
  passed          BOOLEAN NOT NULL,
  reason          TEXT,
  created_at      TIMESTAMPTZ DEFAULT now()
);

-- ═══════════════════════════════════════════════════════════
-- TABLE : spiral_positions (Disque de Phaistos)
-- Positions spiralées pour visualisation non-linéaire
-- ═══════════════════════════════════════════════════════════

CREATE TABLE spiral_positions (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  node_id         UUID NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
  ring            INTEGER NOT NULL DEFAULT 0,     -- 0 = centre (essence)
  angle           NUMERIC NOT NULL DEFAULT 0,     -- Radians
  depth           INTEGER DEFAULT 0,              -- Couches d'information
  essence_distance NUMERIC DEFAULT 1.0,           -- 0 = essence atteinte
  created_at      TIMESTAMPTZ DEFAULT now(),

  UNIQUE(node_id)
);

-- ═══════════════════════════════════════════════════════════
-- TABLE : hedera_proofs
-- Preuves immuables sur le Consensus Service d'Hedera
-- ═══════════════════════════════════════════════════════════

CREATE TABLE hedera_proofs (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  rosetta_mapping_id  UUID NOT NULL REFERENCES rosetta_mappings(id) ON DELETE CASCADE,
  topic_id            TEXT NOT NULL,
  sequence_number     BIGINT,
  consensus_timestamp TEXT,
  message_hash        TEXT NOT NULL,
  created_at          TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_hedera_rosetta ON hedera_proofs(rosetta_mapping_id);
CREATE INDEX idx_hedera_topic ON hedera_proofs(topic_id);

-- ═══════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (Souveraineté des données)
-- ═══════════════════════════════════════════════════════════

ALTER TABLE nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE rosetta_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE vibrational_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE gear_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE alchemy_validations ENABLE ROW LEVEL SECURITY;
ALTER TABLE alchemy_transformation_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE spiral_positions ENABLE ROW LEVEL SECURITY;
ALTER TABLE hedera_proofs ENABLE ROW LEVEL SECURITY;

-- Politique : Les utilisateurs peuvent lire tous les nodes publics
CREATE POLICY "nodes_read_public" ON nodes
  FOR SELECT USING (true);

-- Politique : Seul le créateur peut modifier ses nodes
CREATE POLICY "nodes_owner_write" ON nodes
  FOR ALL USING (auth.uid() = created_by);

-- Politique : Lecture des mappings Rosetta pour tous (transparence)
CREATE POLICY "rosetta_read_all" ON rosetta_mappings
  FOR SELECT USING (true);

-- Politique : Seul le créateur du node parent peut écrire
CREATE POLICY "rosetta_owner_write" ON rosetta_mappings
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM nodes WHERE nodes.id = rosetta_mappings.node_id
      AND nodes.created_by = auth.uid()
    )
  );

-- Politique : Chaque utilisateur voit ses propres logs vibrationnels
CREATE POLICY "viblog_own" ON vibrational_logs
  FOR ALL USING (auth.uid() = user_id);

-- Politique : Les gear_events sont lisibles par tous (transparence mécanique)
CREATE POLICY "gear_read_all" ON gear_events
  FOR SELECT USING (true);

-- Politique : Les validations alchimiques suivent le propriétaire du node
CREATE POLICY "alchemy_owner" ON alchemy_validations
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM nodes WHERE nodes.id = alchemy_validations.node_id
      AND nodes.created_by = auth.uid()
    )
  );

CREATE POLICY "alchemy_log_owner" ON alchemy_transformation_log
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM alchemy_validations av
      JOIN nodes n ON n.id = av.node_id
      WHERE av.id = alchemy_transformation_log.validation_id
      AND n.created_by = auth.uid()
    )
  );

CREATE POLICY "spiral_owner" ON spiral_positions
  FOR ALL USING (
    EXISTS (
      SELECT 1 FROM nodes WHERE nodes.id = spiral_positions.node_id
      AND nodes.created_by = auth.uid()
    )
  );

CREATE POLICY "hedera_read_all" ON hedera_proofs
  FOR SELECT USING (true);

-- ═══════════════════════════════════════════════════════════
-- FONCTIONS UTILITAIRES
-- ═══════════════════════════════════════════════════════════

-- Calcul de distance Haversine (Point Zéro → utilisateur)
CREATE OR REPLACE FUNCTION distance_to_zero(lat NUMERIC, lon NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
  R NUMERIC := 6371; -- Rayon Terre en km
  dlat NUMERIC;
  dlon NUMERIC;
  a NUMERIC;
  c NUMERIC;
  zero_lat NUMERIC := 21.4;
  zero_lon NUMERIC := -89.5;
BEGIN
  dlat := radians(lat - zero_lat);
  dlon := radians(lon - zero_lon);
  a := sin(dlat/2) * sin(dlat/2) +
       cos(radians(zero_lat)) * cos(radians(lat)) *
       sin(dlon/2) * sin(dlon/2);
  c := 2 * atan2(sqrt(a), sqrt(1 - a));
  RETURN R * c;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Trigger : mise à jour automatique de updated_at
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER nodes_updated
  BEFORE UPDATE ON nodes
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER alchemy_updated
  BEFORE UPDATE ON alchemy_validations
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Vue : Résumé de résonance par sphère
CREATE OR REPLACE VIEW sphere_resonance_summary AS
SELECT
  n.sphere_id,
  COUNT(n.id) as node_count,
  AVG(n.resonance_level) as avg_resonance,
  COUNT(CASE WHEN av.is_aligned THEN 1 END) as aligned_nodes,
  COUNT(CASE WHEN NOT av.is_aligned THEN 1 END) as polishing_nodes
FROM nodes n
LEFT JOIN alchemy_validations av ON av.node_id = n.id
GROUP BY n.sphere_id;
