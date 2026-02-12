-- ═══════════════════════════════════════════════════════════════════════════════
-- AT·OM - TABLES MANQUANTES SEULEMENT
-- Compatible avec la structure profiles existante (role_id au lieu de role)
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: PERCEPTIONS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS perceptions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  text TEXT NOT NULL,
  frequency INTEGER DEFAULT 999,
  heartbeat INTEGER DEFAULT 444,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_perceptions_user_id ON perceptions(user_id);
CREATE INDEX IF NOT EXISTS idx_perceptions_created_at ON perceptions(created_at DESC);

ALTER TABLE perceptions ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  CREATE POLICY "Users can view own perceptions" ON perceptions FOR SELECT USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE POLICY "Users can create own perceptions" ON perceptions FOR INSERT WITH CHECK (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE POLICY "Users can delete own perceptions" ON perceptions FOR DELETE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: BESOINS LOCAUX
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS local_needs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(50) DEFAULT 'general',
  location VARCHAR(255) DEFAULT 'Quebec',
  priority VARCHAR(20) DEFAULT 'medium',
  votes INTEGER DEFAULT 0,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_local_needs_category ON local_needs(category);
CREATE INDEX IF NOT EXISTS idx_local_needs_location ON local_needs(location);
CREATE INDEX IF NOT EXISTS idx_local_needs_votes ON local_needs(votes DESC);

ALTER TABLE local_needs ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  CREATE POLICY "Anyone can view needs" ON local_needs FOR SELECT USING (true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE POLICY "Authenticated users can create needs" ON local_needs FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE POLICY "Users can update own needs" ON local_needs FOR UPDATE USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: VOTES
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS need_votes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  need_id UUID REFERENCES local_needs(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, need_id)
);

ALTER TABLE need_votes ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  CREATE POLICY "Users can view own votes" ON need_votes FOR SELECT USING (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE POLICY "Users can vote" ON need_votes FOR INSERT WITH CHECK (auth.uid() = user_id);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: ANNALES (Calculs Arithmos)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS annales (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  word VARCHAR(255) NOT NULL,
  arithmos INTEGER NOT NULL,
  oracle_level INTEGER,
  frequency INTEGER DEFAULT 999,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_annales_user_id ON annales(user_id);
CREATE INDEX IF NOT EXISTS idx_annales_arithmos ON annales(arithmos);

ALTER TABLE annales ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  CREATE POLICY "Anyone can view annales" ON annales FOR SELECT USING (true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
  CREATE POLICY "Authenticated users can create annales" ON annales FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: SUCCES HUMANITE - KNOWLEDGE BASE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS succes_humanite (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  subtitle VARCHAR(500),
  chapter VARCHAR(100),
  episode INTEGER,
  content TEXT NOT NULL,
  summary TEXT,
  keywords TEXT[],
  agent_level INTEGER DEFAULT 4,
  frequency_tag INTEGER DEFAULT 999,
  dimension VARCHAR(50),
  linked_perceptions UUID[],
  linked_needs UUID[],
  ip_status VARCHAR(50) DEFAULT 'draft',
  ip_filing_date TIMESTAMP,
  copyright_notice TEXT,
  access_level VARCHAR(50) DEFAULT 'citoyen',
  is_published BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  published_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_succes_humanite_dimension ON succes_humanite(dimension);
CREATE INDEX IF NOT EXISTS idx_succes_humanite_agent_level ON succes_humanite(agent_level);

ALTER TABLE succes_humanite ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  CREATE POLICY "Public content viewable" ON succes_humanite FOR SELECT USING (is_published = true OR access_level = 'public');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: ATOM MAPPING - Flux de donnees
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS atom_mapping (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  source_type VARCHAR(50) NOT NULL,
  source_id UUID,
  source_content TEXT,
  step VARCHAR(50) NOT NULL,
  agent_level INTEGER NOT NULL,
  result_summary TEXT,
  result_data JSONB,
  confidence_score DECIMAL(3,2),
  parent_mapping_id UUID REFERENCES atom_mapping(id),
  child_mapping_ids UUID[],
  frequency_context INTEGER DEFAULT 999,
  sovereign_mode BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  processed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_atom_mapping_source ON atom_mapping(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_atom_mapping_step ON atom_mapping(step);

ALTER TABLE atom_mapping ENABLE ROW LEVEL SECURITY;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: GRATITUDE LETTER
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS gratitude_letter (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  greeting TEXT,
  body TEXT NOT NULL,
  signature TEXT,
  links JSONB DEFAULT '[]',
  view_count INTEGER DEFAULT 0,
  share_count INTEGER DEFAULT 0,
  version INTEGER DEFAULT 1,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE gratitude_letter ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  CREATE POLICY "Active letters viewable" ON gratitude_letter FOR SELECT USING (is_active = true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: TERRITORY PROJECTS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS territory_projects (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(100),
  description TEXT,
  location VARCHAR(255),
  coordinates POINT,
  region VARCHAR(100) DEFAULT 'Quebec',
  status VARCHAR(50) DEFAULT 'concept',
  frequency_alignment INTEGER DEFAULT 999,
  linked_needs UUID[],
  quantum_light_integration BOOLEAN DEFAULT false,
  investment_required DECIMAL(12,2),
  roi_projection DECIMAL(5,2),
  timeline_months INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_territory_projects_type ON territory_projects(type);
CREATE INDEX IF NOT EXISTS idx_territory_projects_status ON territory_projects(status);

ALTER TABLE territory_projects ENABLE ROW LEVEL SECURITY;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: ACCREDITATIONS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS accreditations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  entity_name VARCHAR(255) NOT NULL,
  entity_type VARCHAR(50) NOT NULL,
  registration_number VARCHAR(100),
  contact_email VARCHAR(255) NOT NULL,
  contact_phone VARCHAR(50),
  website VARCHAR(255),
  address TEXT,
  city VARCHAR(100) DEFAULT 'Montreal',
  region VARCHAR(100) DEFAULT 'Quebec',
  postal_code VARCHAR(20),
  requested_role VARCHAR(50) NOT NULL,
  frequency_charter_signed BOOLEAN DEFAULT false,
  sovereignty_declaration BOOLEAN DEFAULT false,
  ethics_agreement BOOLEAN DEFAULT false,
  services_offered TEXT[],
  expertise_areas TEXT[],
  status VARCHAR(50) DEFAULT 'pending',
  validation_score DECIMAL(3,2),
  validated_by UUID,
  validation_notes TEXT,
  entity_arithmos INTEGER,
  frequency_alignment INTEGER DEFAULT 444,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  validated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_accreditations_entity_type ON accreditations(entity_type);
CREATE INDEX IF NOT EXISTS idx_accreditations_status ON accreditations(status);

ALTER TABLE accreditations ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
  CREATE POLICY "Anyone can submit accreditation" ON accreditations FOR INSERT WITH CHECK (true);
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FONCTION: Incrementer votes (sans reference a profiles.role)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION increment_votes(p_need_id UUID)
RETURNS void AS $$
BEGIN
  INSERT INTO need_votes (user_id, need_id)
  VALUES (auth.uid(), p_need_id);

  UPDATE local_needs
  SET votes = votes + 1, updated_at = NOW()
  WHERE id = p_need_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN - Tables manquantes ajoutees
-- ═══════════════════════════════════════════════════════════════════════════════

DO $$
BEGIN
  RAISE NOTICE '════════════════════════════════════════════════════════════';
  RAISE NOTICE '  AT-OM MISSING TABLES ADDED SUCCESSFULLY';
  RAISE NOTICE '  Tables: perceptions, local_needs, need_votes, annales,';
  RAISE NOTICE '          succes_humanite, atom_mapping, gratitude_letter,';
  RAISE NOTICE '          territory_projects, accreditations';
  RAISE NOTICE '════════════════════════════════════════════════════════════';
END $$;
