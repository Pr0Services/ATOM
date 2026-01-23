-- ═══════════════════════════════════════════════════════════════════════════════
-- AT·OM - SCHÉMA DE BASE DE DONNÉES SUPABASE
-- L'Arche des Résonances Universelles
-- CHE·NU V76 - Janvier 2026
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- INSTRUCTIONS:
-- 1. Créez un projet sur https://supabase.com
-- 2. Allez dans SQL Editor
-- 3. Copiez-collez ce script et exécutez-le
-- 4. Copiez vos clés API dans le fichier .env
--
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: PERCEPTIONS
-- Journal de Perception de l'Arche
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS perceptions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  text TEXT NOT NULL,
  frequency INTEGER DEFAULT 999,
  heartbeat INTEGER DEFAULT 444,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour les requêtes fréquentes
CREATE INDEX idx_perceptions_user_id ON perceptions(user_id);
CREATE INDEX idx_perceptions_created_at ON perceptions(created_at DESC);

-- RLS (Row Level Security)
ALTER TABLE perceptions ENABLE ROW LEVEL SECURITY;

-- Politique: Les utilisateurs peuvent voir leurs propres perceptions
CREATE POLICY "Users can view own perceptions"
  ON perceptions FOR SELECT
  USING (auth.uid() = user_id);

-- Politique: Les utilisateurs peuvent créer leurs propres perceptions
CREATE POLICY "Users can create own perceptions"
  ON perceptions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Politique: Les utilisateurs peuvent supprimer leurs propres perceptions
CREATE POLICY "Users can delete own perceptions"
  ON perceptions FOR DELETE
  USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: BESOINS LOCAUX
-- Moteur de Civilisation
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS local_needs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(50) DEFAULT 'general',
  location VARCHAR(255) DEFAULT 'Québec',
  priority VARCHAR(20) DEFAULT 'medium',
  votes INTEGER DEFAULT 0,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_local_needs_category ON local_needs(category);
CREATE INDEX idx_local_needs_location ON local_needs(location);
CREATE INDEX idx_local_needs_votes ON local_needs(votes DESC);
CREATE INDEX idx_local_needs_status ON local_needs(status);

-- RLS
ALTER TABLE local_needs ENABLE ROW LEVEL SECURITY;

-- Politique: Tout le monde peut voir les besoins
CREATE POLICY "Anyone can view needs"
  ON local_needs FOR SELECT
  USING (true);

-- Politique: Les utilisateurs authentifiés peuvent créer des besoins
CREATE POLICY "Authenticated users can create needs"
  ON local_needs FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Politique: Les créateurs peuvent modifier leurs besoins
CREATE POLICY "Users can update own needs"
  ON local_needs FOR UPDATE
  USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: VOTES
-- Suivi des votes pour éviter les doublons
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS need_votes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  need_id UUID REFERENCES local_needs(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, need_id)
);

-- RLS
ALTER TABLE need_votes ENABLE ROW LEVEL SECURITY;

-- Politique: Les utilisateurs peuvent voir leurs votes
CREATE POLICY "Users can view own votes"
  ON need_votes FOR SELECT
  USING (auth.uid() = user_id);

-- Politique: Les utilisateurs peuvent voter
CREATE POLICY "Users can vote"
  ON need_votes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- FONCTION: Incrémenter les votes
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION increment_votes(need_id UUID)
RETURNS void AS $$
BEGIN
  -- Insérer le vote (échoue si doublon grâce à UNIQUE)
  INSERT INTO need_votes (user_id, need_id)
  VALUES (auth.uid(), need_id);

  -- Incrémenter le compteur
  UPDATE local_needs
  SET votes = votes + 1, updated_at = NOW()
  WHERE id = need_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: PROFILS UTILISATEURS
-- Extension des données auth.users
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  display_name VARCHAR(255),
  role VARCHAR(50) DEFAULT 'citoyen',
  frequency INTEGER DEFAULT 444,
  avatar_url TEXT,
  bio TEXT,
  location VARCHAR(255),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Politique: Les profils sont publics
CREATE POLICY "Profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (true);

-- Politique: Les utilisateurs peuvent modifier leur profil
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- Politique: Création automatique du profil
CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGER: Créer le profil automatiquement à l'inscription
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO profiles (id, display_name, role)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'display_name', split_part(NEW.email, '@', 1)),
    COALESCE(NEW.raw_user_meta_data->>'role', 'citoyen')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Créer le trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

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

-- Index
CREATE INDEX idx_annales_user_id ON annales(user_id);
CREATE INDEX idx_annales_arithmos ON annales(arithmos);

-- RLS
ALTER TABLE annales ENABLE ROW LEVEL SECURITY;

-- Politique: Tout le monde peut voir les annales
CREATE POLICY "Anyone can view annales"
  ON annales FOR SELECT
  USING (true);

-- Politique: Les utilisateurs peuvent créer des entrées
CREATE POLICY "Authenticated users can create annales"
  ON annales FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: SUCCÈS HUMANITÉ - KNOWLEDGE BASE
-- Base de connaissances pour le documentaire/série et synthèses L4-L9
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS succes_humanite (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Métadonnées
  title VARCHAR(500) NOT NULL,
  subtitle VARCHAR(500),
  chapter VARCHAR(100),                    -- Ex: "Chapitre 1: L'Origine"
  episode INTEGER,                          -- Pour la série documentaire

  -- Contenu
  content TEXT NOT NULL,
  summary TEXT,                             -- Résumé court pour recherche
  keywords TEXT[],                          -- Tags pour recherche

  -- Classification AT-OM
  agent_level INTEGER DEFAULT 4,            -- L0-L9 (niveau d'analyse)
  frequency_tag INTEGER DEFAULT 999,        -- 444/999/963
  dimension VARCHAR(50),                    -- frequentiel, social, scientifique, territoire

  -- Mapping vers le système
  linked_perceptions UUID[],               -- IDs des perceptions sources
  linked_needs UUID[],                     -- IDs des besoins liés

  -- Propriété intellectuelle
  ip_status VARCHAR(50) DEFAULT 'draft',   -- draft, protected, published
  ip_filing_date TIMESTAMP,
  copyright_notice TEXT,

  -- Accès
  access_level VARCHAR(50) DEFAULT 'citoyen', -- souverain, collaborateur, citoyen, public
  is_published BOOLEAN DEFAULT false,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  published_at TIMESTAMP WITH TIME ZONE
);

-- Index pour recherche Full-Text
CREATE INDEX idx_succes_humanite_title ON succes_humanite USING gin(to_tsvector('french', title));
CREATE INDEX idx_succes_humanite_content ON succes_humanite USING gin(to_tsvector('french', content));
CREATE INDEX idx_succes_humanite_keywords ON succes_humanite USING gin(keywords);
CREATE INDEX idx_succes_humanite_dimension ON succes_humanite(dimension);
CREATE INDEX idx_succes_humanite_agent_level ON succes_humanite(agent_level);
CREATE INDEX idx_succes_humanite_chapter ON succes_humanite(chapter);

-- RLS
ALTER TABLE succes_humanite ENABLE ROW LEVEL SECURITY;

-- Politique: Contenu public visible par tous
CREATE POLICY "Public content viewable by everyone"
  ON succes_humanite FOR SELECT
  USING (is_published = true OR access_level = 'public');

-- Politique: Collaborateurs peuvent voir contenu collaborateur
CREATE POLICY "Collaborators can view collaborator content"
  ON succes_humanite FOR SELECT
  USING (
    access_level IN ('collaborateur', 'citoyen', 'public')
    AND EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('collaborateur', 'souverain')
    )
  );

-- Politique: Souverain peut tout voir et modifier
CREATE POLICY "Sovereign has full access"
  ON succes_humanite FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: MAPPING AT-OM
-- Flux de données: Perception → Analyse → Traitement → Synthèse
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS atom_mapping (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Source
  source_type VARCHAR(50) NOT NULL,        -- perception, need, annale, external
  source_id UUID,
  source_content TEXT,

  -- Étapes du flux
  step VARCHAR(50) NOT NULL,               -- input, analysis, processing, synthesis, output
  agent_level INTEGER NOT NULL,            -- L0-L9

  -- Résultat de l'étape
  result_summary TEXT,
  result_data JSONB,                       -- Données structurées
  confidence_score DECIMAL(3,2),           -- 0.00 - 1.00

  -- Chaînage
  parent_mapping_id UUID REFERENCES atom_mapping(id),
  child_mapping_ids UUID[],

  -- Métadonnées
  frequency_context INTEGER DEFAULT 999,
  sovereign_mode BOOLEAN DEFAULT true,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  processed_at TIMESTAMP WITH TIME ZONE
);

-- Index
CREATE INDEX idx_atom_mapping_source ON atom_mapping(source_type, source_id);
CREATE INDEX idx_atom_mapping_step ON atom_mapping(step);
CREATE INDEX idx_atom_mapping_agent_level ON atom_mapping(agent_level);
CREATE INDEX idx_atom_mapping_parent ON atom_mapping(parent_mapping_id);

-- RLS
ALTER TABLE atom_mapping ENABLE ROW LEVEL SECURITY;

-- Politique: Souverain et collaborateurs peuvent voir le mapping
CREATE POLICY "Authorized users can view mapping"
  ON atom_mapping FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('souverain', 'collaborateur')
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: LETTRE DE REMERCIEMENT
-- Portail avec liens vers les dimensions du projet
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS gratitude_letter (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Contenu de la lettre
  title VARCHAR(500) NOT NULL,
  greeting TEXT,
  body TEXT NOT NULL,
  signature TEXT,

  -- Liens actifs (mapping vers les dimensions)
  links JSONB DEFAULT '[]',                -- [{dimension, url, description, icon}]

  -- Statistiques
  view_count INTEGER DEFAULT 0,
  share_count INTEGER DEFAULT 0,

  -- Version
  version INTEGER DEFAULT 1,
  is_active BOOLEAN DEFAULT true,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS
ALTER TABLE gratitude_letter ENABLE ROW LEVEL SECURITY;

-- Politique: Lettres actives visibles par tous
CREATE POLICY "Active letters viewable by everyone"
  ON gratitude_letter FOR SELECT
  USING (is_active = true);

-- Politique: Souverain peut gérer les lettres
CREATE POLICY "Sovereign can manage letters"
  ON gratitude_letter FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: PROJETS TERRITOIRE (Québec)
-- Camping, Glamping, VTT, applications physiques
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS territory_projects (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Identification
  name VARCHAR(255) NOT NULL,
  type VARCHAR(100),                       -- camping, glamping, vtt, retreat, other
  description TEXT,

  -- Localisation
  location VARCHAR(255),
  coordinates POINT,                       -- Géolocalisation
  region VARCHAR(100) DEFAULT 'Québec',

  -- Statut
  status VARCHAR(50) DEFAULT 'concept',    -- concept, planning, development, operational

  -- Connexion AT-OM
  frequency_alignment INTEGER DEFAULT 999,
  linked_needs UUID[],                     -- Besoins locaux adressés
  quantum_light_integration BOOLEAN DEFAULT false,

  -- Business
  investment_required DECIMAL(12,2),
  roi_projection DECIMAL(5,2),
  timeline_months INTEGER,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_territory_projects_type ON territory_projects(type);
CREATE INDEX idx_territory_projects_status ON territory_projects(status);
CREATE INDEX idx_territory_projects_region ON territory_projects(region);

-- RLS
ALTER TABLE territory_projects ENABLE ROW LEVEL SECURITY;

-- Politique: Projets visibles par collaborateurs et souverain
CREATE POLICY "Authorized users can view projects"
  ON territory_projects FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('souverain', 'collaborateur')
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- FONCTIONS DE RECHERCHE
-- ═══════════════════════════════════════════════════════════════════════════════

-- Recherche full-text dans Succès Humanité
CREATE OR REPLACE FUNCTION search_knowledge_base(search_query TEXT, limit_results INTEGER DEFAULT 20)
RETURNS TABLE (
  id UUID,
  title VARCHAR(500),
  chapter VARCHAR(100),
  summary TEXT,
  dimension VARCHAR(50),
  relevance REAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    sh.id,
    sh.title,
    sh.chapter,
    sh.summary,
    sh.dimension,
    ts_rank(
      to_tsvector('french', sh.title || ' ' || COALESCE(sh.summary, '') || ' ' || sh.content),
      plainto_tsquery('french', search_query)
    ) as relevance
  FROM succes_humanite sh
  WHERE
    to_tsvector('french', sh.title || ' ' || COALESCE(sh.summary, '') || ' ' || sh.content)
    @@ plainto_tsquery('french', search_query)
    AND (sh.is_published = true OR sh.access_level = 'public')
  ORDER BY relevance DESC
  LIMIT limit_results;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction de mapping automatique: Perception → Analyse
CREATE OR REPLACE FUNCTION process_perception_to_analysis(perception_id UUID)
RETURNS UUID AS $$
DECLARE
  new_mapping_id UUID;
  perception_text TEXT;
BEGIN
  -- Récupérer le texte de la perception
  SELECT text INTO perception_text FROM perceptions WHERE id = perception_id;

  IF perception_text IS NULL THEN
    RAISE EXCEPTION 'Perception not found';
  END IF;

  -- Créer l'entrée de mapping L0-L3 (Analyse)
  INSERT INTO atom_mapping (
    source_type, source_id, source_content,
    step, agent_level, result_summary,
    frequency_context, sovereign_mode
  ) VALUES (
    'perception', perception_id, perception_text,
    'analysis',
    CASE
      WHEN LENGTH(perception_text) < 50 THEN 0
      WHEN LENGTH(perception_text) < 200 THEN 1
      WHEN LENGTH(perception_text) < 500 THEN 2
      ELSE 3
    END,
    'Perception analysée et catégorisée',
    999, true
  ) RETURNING id INTO new_mapping_id;

  RETURN new_mapping_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: ACCRÉDITATIONS INSTITUTIONNELLES
-- Portail de validation pour entreprises et services publics
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS accreditations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Identification de l'entité
  entity_name VARCHAR(255) NOT NULL,
  entity_type VARCHAR(50) NOT NULL,            -- public_service, enterprise, subcontractor
  registration_number VARCHAR(100),            -- NEQ, numéro d'entreprise
  contact_email VARCHAR(255) NOT NULL,
  contact_phone VARCHAR(50),
  website VARCHAR(255),

  -- Localisation
  address TEXT,
  city VARCHAR(100) DEFAULT 'Montréal',
  region VARCHAR(100) DEFAULT 'Québec',
  postal_code VARCHAR(20),

  -- Rôle demandé
  requested_role VARCHAR(50) NOT NULL,         -- public_service_auth, enterprise_client_auth, subcontractor_verified

  -- Engagement Fréquentiel (Proof of Resonance)
  frequency_charter_signed BOOLEAN DEFAULT false,
  sovereignty_declaration BOOLEAN DEFAULT false,
  ethics_agreement BOOLEAN DEFAULT false,

  -- Services proposés (pour sous-traitants)
  services_offered TEXT[],                     -- entretien, construction, guide, énergie, etc.
  expertise_areas TEXT[],

  -- Validation
  status VARCHAR(50) DEFAULT 'pending',        -- pending, under_review, approved, rejected
  validation_score DECIMAL(3,2),               -- Score calculé par les agents L4-L6
  validated_by UUID REFERENCES profiles(id),
  validation_notes TEXT,

  -- Arithmos de l'entité
  entity_arithmos INTEGER,
  frequency_alignment INTEGER DEFAULT 444,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  validated_at TIMESTAMP WITH TIME ZONE
);

-- Index
CREATE INDEX idx_accreditations_entity_type ON accreditations(entity_type);
CREATE INDEX idx_accreditations_status ON accreditations(status);
CREATE INDEX idx_accreditations_region ON accreditations(region);
CREATE INDEX idx_accreditations_requested_role ON accreditations(requested_role);

-- RLS
ALTER TABLE accreditations ENABLE ROW LEVEL SECURITY;

-- Politique: Les demandes sont visibles par le créateur et les souverains
CREATE POLICY "Accreditations viewable by authorized"
  ON accreditations FOR SELECT
  USING (
    contact_email = auth.email()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- Politique: Toute personne peut soumettre une demande
CREATE POLICY "Anyone can submit accreditation"
  ON accreditations FOR INSERT
  WITH CHECK (true);

-- Politique: Souverain peut modifier les accreditations
CREATE POLICY "Sovereign can update accreditations"
  ON accreditations FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: SERVICES DE SOUS-TRAITANTS
-- Catalogue des services disponibles pour les projets territoriaux
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS subcontractor_services (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Lien vers l'accréditation
  accreditation_id UUID REFERENCES accreditations(id) ON DELETE CASCADE,

  -- Catégorie de service
  category VARCHAR(100) NOT NULL,              -- entretien, construction, energie, transport, guide, restauration
  subcategory VARCHAR(100),

  -- Détails du service
  service_name VARCHAR(255) NOT NULL,
  description TEXT,

  -- Disponibilité
  availability VARCHAR(50) DEFAULT 'available', -- available, busy, seasonal, inactive
  seasonal_months INTEGER[],                    -- Mois de disponibilité (1-12)

  -- Zone de service
  service_radius_km INTEGER DEFAULT 50,
  service_regions TEXT[] DEFAULT ARRAY['Québec'],

  -- Tarification (optionnel)
  rate_type VARCHAR(50),                        -- hourly, daily, project, contract
  rate_range VARCHAR(100),

  -- Connexion aux besoins locaux
  linked_need_categories TEXT[],               -- Catégories de besoins que ce service peut combler

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_subcontractor_services_category ON subcontractor_services(category);
CREATE INDEX idx_subcontractor_services_availability ON subcontractor_services(availability);

-- RLS
ALTER TABLE subcontractor_services ENABLE ROW LEVEL SECURITY;

-- Politique: Services visibles par collaborateurs et souverains
CREATE POLICY "Services viewable by authorized users"
  ON subcontractor_services FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('souverain', 'collaborateur')
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: PARTENAIRES INSTITUTIONNELS
-- Entreprises et services publics accrédités
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS institutional_partners (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Lien vers l'accréditation approuvée
  accreditation_id UUID REFERENCES accreditations(id) ON DELETE CASCADE,

  -- Rôle attribué
  role_id VARCHAR(50) NOT NULL,                -- public_service_auth, enterprise_client_auth

  -- Permissions spécifiques
  can_view_needs_analysis BOOLEAN DEFAULT false,
  can_view_agent_synthesis BOOLEAN DEFAULT false,
  can_submit_challenges BOOLEAN DEFAULT false,
  can_access_quantum_light BOOLEAN DEFAULT false,

  -- Niveau d'accès aux agents
  max_agent_level INTEGER DEFAULT 6,           -- L0-L9

  -- Engagement
  partnership_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  partnership_end TIMESTAMP WITH TIME ZONE,

  -- Impact sur l'Arche
  contribution_score INTEGER DEFAULT 0,
  resonance_alignment DECIMAL(3,2) DEFAULT 0.00,

  -- Pour le documentaire "Succès Humanité"
  featured_in_documentary BOOLEAN DEFAULT false,
  testimonial TEXT,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_institutional_partners_role ON institutional_partners(role_id);

-- RLS
ALTER TABLE institutional_partners ENABLE ROW LEVEL SECURITY;

-- Politique: Partenaires visibles par collaborateurs et souverains
CREATE POLICY "Partners viewable by authorized"
  ON institutional_partners FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('souverain', 'collaborateur')
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- FONCTION: Calculer le score de validation d'une accréditation
-- Utilisée par les agents L4-L6
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION calculate_accreditation_score(accred_id UUID)
RETURNS DECIMAL AS $$
DECLARE
  score DECIMAL := 0;
  accred RECORD;
BEGIN
  SELECT * INTO accred FROM accreditations WHERE id = accred_id;

  IF accred IS NULL THEN
    RETURN 0;
  END IF;

  -- Points pour les engagements
  IF accred.frequency_charter_signed THEN score := score + 0.25; END IF;
  IF accred.sovereignty_declaration THEN score := score + 0.25; END IF;
  IF accred.ethics_agreement THEN score := score + 0.25; END IF;

  -- Points pour les informations complètes
  IF accred.registration_number IS NOT NULL THEN score := score + 0.10; END IF;
  IF accred.website IS NOT NULL THEN score := score + 0.05; END IF;
  IF accred.address IS NOT NULL THEN score := score + 0.05; END IF;

  -- Points pour l'alignement fréquentiel (999 = max)
  IF accred.frequency_alignment = 999 THEN score := score + 0.05; END IF;

  -- Mettre à jour le score
  UPDATE accreditations
  SET validation_score = score, updated_at = NOW()
  WHERE id = accred_id;

  RETURN score;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FONCTION: Approuver une accréditation et créer le partenariat
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION approve_accreditation(accred_id UUID, validator_id UUID, notes TEXT DEFAULT NULL)
RETURNS UUID AS $$
DECLARE
  partner_id UUID;
  accred RECORD;
BEGIN
  SELECT * INTO accred FROM accreditations WHERE id = accred_id;

  IF accred IS NULL THEN
    RAISE EXCEPTION 'Accreditation not found';
  END IF;

  -- Mettre à jour le statut
  UPDATE accreditations
  SET
    status = 'approved',
    validated_by = validator_id,
    validation_notes = notes,
    validated_at = NOW(),
    updated_at = NOW()
  WHERE id = accred_id;

  -- Créer le partenariat institutionnel si enterprise ou public_service
  IF accred.entity_type IN ('public_service', 'enterprise') THEN
    INSERT INTO institutional_partners (
      accreditation_id,
      role_id,
      can_view_needs_analysis,
      can_view_agent_synthesis,
      can_submit_challenges,
      max_agent_level
    ) VALUES (
      accred_id,
      accred.requested_role,
      TRUE,
      accred.entity_type = 'enterprise',
      accred.entity_type = 'enterprise',
      CASE WHEN accred.entity_type = 'public_service' THEN 6 ELSE 4 END
    ) RETURNING id INTO partner_id;

    RETURN partner_id;
  END IF;

  RETURN accred_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN DU SCHÉMA V3
-- ═══════════════════════════════════════════════════════════════════════════════

-- Afficher un message de confirmation
DO $$
BEGIN
  RAISE NOTICE '═══════════════════════════════════════════════════════════════';
  RAISE NOTICE '  AT·OM SCHEMA V3 INSTALLED SUCCESSFULLY';
  RAISE NOTICE '  Tables: perceptions, local_needs, need_votes, profiles, annales,';
  RAISE NOTICE '          succes_humanite, atom_mapping, gratitude_letter, territory_projects,';
  RAISE NOTICE '          accreditations, subcontractor_services, institutional_partners';
  RAISE NOTICE '  Functions: search_knowledge_base, process_perception_to_analysis,';
  RAISE NOTICE '             calculate_accreditation_score, approve_accreditation';
  RAISE NOTICE '  RLS: Enabled on all tables';
  RAISE NOTICE '  Ready for 999Hz Sovereign operations with institutional partners';
  RAISE NOTICE '═══════════════════════════════════════════════════════════════';
END $$;
