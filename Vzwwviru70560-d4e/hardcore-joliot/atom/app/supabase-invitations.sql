-- ═══════════════════════════════════════════════════════════════════════════════
--
--       ██╗███╗   ██╗██╗   ██╗██╗████████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗
--       ██║████╗  ██║██║   ██║██║╚══██╔══╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
--       ██║██╔██╗ ██║██║   ██║██║   ██║   ███████║   ██║   ██║██║   ██║██╔██╗ ██║███████╗
--       ██║██║╚██╗██║╚██╗ ██╔╝██║   ██║   ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║
--       ██║██║ ╚████║ ╚████╔╝ ██║   ██║   ██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║███████║
--       ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
--
--                    SYSTÈME D'INVITATION - AT·OM / CHE·NU V76
--              Points de Lumière Internationaux - Membres Fondateurs
--
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- INSTRUCTIONS:
-- 1. Exécutez ce script APRÈS supabase-security.sql
-- 2. Ce script ajoute le système d'invitation pour les membres fondateurs
--
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. TABLE DES INVITATIONS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS invitations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Code d'invitation unique (ex: ATOM-LIGHT-7X9K)
  code TEXT UNIQUE NOT NULL,

  -- Informations sur l'invité
  invited_name TEXT NOT NULL,
  invited_email TEXT,
  personal_message TEXT,

  -- Type de membre fondateur
  founder_type TEXT DEFAULT 'lumiere' CHECK (founder_type IN (
    'lumiere',       -- Point de Lumière International
    'gardien',       -- Gardien de l'Arche
    'architecte',    -- Architecte de Civilisation
    'tisserand',     -- Tisserand de Liens
    'porteur'        -- Porteur de Flamme
  )),

  -- Contribution énergétique reconnue
  contribution_note TEXT,

  -- Statut de l'invitation
  status TEXT DEFAULT 'pending' CHECK (status IN (
    'pending',       -- En attente d'utilisation
    'accepted',      -- Acceptée et compte créé
    'expired',       -- Expirée
    'revoked'        -- Révoquée
  )),

  -- Utilisateur qui a accepté l'invitation
  accepted_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  accepted_at TIMESTAMP WITH TIME ZONE,

  -- Métadonnées
  created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '30 days'),

  -- Limites d'utilisation
  max_uses INTEGER DEFAULT 1,
  use_count INTEGER DEFAULT 0
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. TABLE DES MEMBRES FONDATEURS (Extension du profil avec Grid Énergétique)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS founders (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE UNIQUE NOT NULL,

  -- Invitation utilisée
  invitation_id UUID REFERENCES invitations(id) ON DELETE SET NULL,

  -- Type de fondateur (hérité de l'invitation)
  founder_type TEXT NOT NULL,

  -- Numéro de fondateur (ordre d'arrivée)
  founder_number INTEGER,

  -- ═══════════════════════════════════════════════════════════════════════════
  -- GRID ÉNERGÉTIQUE - Coordonnées et Ancrage Planétaire
  -- ═══════════════════════════════════════════════════════════════════════════

  -- Coordonnées géographiques pour la Grid mondiale
  grid_latitude DECIMAL(10, 8),           -- Latitude du point d'ancrage
  grid_longitude DECIMAL(11, 8),          -- Longitude du point d'ancrage
  grid_location_name TEXT,                -- Nom du lieu d'ancrage (ex: "Montréal, Québec")

  -- Signature fréquentielle pour validation énergétique
  energy_signature INTEGER DEFAULT 444 CHECK (energy_signature IN (
    111, 222, 333, 444, 528, 639, 741, 852, 963, 999
  )),

  -- Statut d'activation (l'énergie doit être alignée avant activation)
  energy_status TEXT DEFAULT 'calibrating' CHECK (energy_status IN (
    'calibrating',    -- En cours de calibration énergétique
    'aligned',        -- Énergie alignée, prêt pour activation
    'activated',      -- Pleinement activé dans la Grid
    'dormant'         -- Temporairement en pause
  )),

  -- Date d'activation dans la Grid (quand l'énergie n'est plus "dangereuse")
  grid_activated_at TIMESTAMP WITH TIME ZONE,

  -- Type de contribution à la Grid
  contribution_type TEXT DEFAULT 'energetic' CHECK (contribution_type IN (
    'energetic',      -- Contribution énergétique pure
    'material',       -- Ressources matérielles
    'scientific',     -- Expertise scientifique/technique
    'creative',       -- Arts et création
    'healing',        -- Guérison et bien-être
    'bridge'          -- Pont entre les mondes
  )),

  -- ═══════════════════════════════════════════════════════════════════════════
  -- INFORMATIONS PERSONNELLES
  -- ═══════════════════════════════════════════════════════════════════════════

  -- Localisation (texte, pour affichage)
  location_country TEXT,
  location_city TEXT,
  timezone TEXT,

  -- Présentation
  story TEXT,                    -- Histoire personnelle / parcours
  intention TEXT,                -- Intention dans la communauté
  gifts TEXT[],                  -- Dons/talents à partager
  seeking TEXT[],                -- Ce qu'ils cherchent

  -- Résonance spirituelle
  resonance_frequency INTEGER DEFAULT 444,
  spirit_animal TEXT,
  element TEXT CHECK (element IN ('feu', 'eau', 'terre', 'air', 'ether')),

  -- ═══════════════════════════════════════════════════════════════════════════
  -- ACTIVITÉ ET MÉTADONNÉES
  -- ═══════════════════════════════════════════════════════════════════════════

  is_active BOOLEAN DEFAULT true,
  last_seen_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2.1 TABLE DE LA GRID MONDIALE (Points d'ancrage actifs)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS energy_grid (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Point d'ancrage
  name TEXT NOT NULL,                     -- Nom du point d'ancrage
  latitude DECIMAL(10, 8) NOT NULL,
  longitude DECIMAL(11, 8) NOT NULL,

  -- Type de point
  point_type TEXT DEFAULT 'anchor' CHECK (point_type IN (
    'anchor',         -- Point d'ancrage fondateur
    'node',           -- Nœud de connexion
    'portal',         -- Portail énergétique
    'sanctuary'       -- Sanctuaire
  )),

  -- Fréquence du point
  frequency INTEGER DEFAULT 444,

  -- Fondateur responsable de ce point (si applicable)
  guardian_id UUID REFERENCES founders(user_id) ON DELETE SET NULL,

  -- Nombre de fondateurs connectés à ce point
  connected_founders INTEGER DEFAULT 0,

  -- Statut
  is_active BOOLEAN DEFAULT true,
  activated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Métadonnées
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. TABLE DES CONNEXIONS ENTRE FONDATEURS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS founder_connections (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Les deux fondateurs connectés
  founder_a UUID REFERENCES founders(user_id) ON DELETE CASCADE NOT NULL,
  founder_b UUID REFERENCES founders(user_id) ON DELETE CASCADE NOT NULL,

  -- Type de connexion
  connection_type TEXT DEFAULT 'resonance' CHECK (connection_type IN (
    'resonance',     -- Connexion énergétique
    'collaboration', -- Projet commun
    'mentorship',    -- Mentorat
    'friendship'     -- Amitié
  )),

  -- Note sur la connexion
  note TEXT,

  -- Statut
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined')),

  -- Qui a initié
  initiated_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Éviter les doublons
  UNIQUE(founder_a, founder_b),
  CHECK (founder_a < founder_b) -- Assure l'ordre pour éviter les doublons inversés
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. TABLE DES MESSAGES COMMUNAUTAIRES (Cercle des Fondateurs)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS founder_messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Auteur
  author_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

  -- Contenu
  content TEXT NOT NULL,

  -- Type de message
  message_type TEXT DEFAULT 'sharing' CHECK (message_type IN (
    'sharing',       -- Partage général
    'gratitude',     -- Expression de gratitude
    'intention',     -- Déclaration d'intention
    'celebration',   -- Célébration
    'support',       -- Demande/offre de soutien
    'announcement'   -- Annonce importante
  )),

  -- Réponse à un autre message
  reply_to UUID REFERENCES founder_messages(id) ON DELETE SET NULL,

  -- Réactions (stockées comme JSON pour flexibilité)
  reactions JSONB DEFAULT '{}',

  -- Visibilité
  is_pinned BOOLEAN DEFAULT false,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. ACTIVER RLS
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE invitations ENABLE ROW LEVEL SECURITY;
ALTER TABLE founders ENABLE ROW LEVEL SECURITY;
ALTER TABLE founder_connections ENABLE ROW LEVEL SECURITY;
ALTER TABLE founder_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE energy_grid ENABLE ROW LEVEL SECURITY;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. POLICIES POUR INVITATIONS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Seul le Souverain peut voir toutes les invitations
CREATE POLICY "Souverain can view all invitations"
  ON invitations FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- Les utilisateurs peuvent voir leur propre invitation (via le code)
CREATE POLICY "Users can view invitation by code"
  ON invitations FOR SELECT
  USING (accepted_by = auth.uid());

-- Seul le Souverain peut créer des invitations
CREATE POLICY "Souverain can create invitations"
  ON invitations FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- Seul le Souverain peut modifier les invitations
CREATE POLICY "Souverain can update invitations"
  ON invitations FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. POLICIES POUR FONDATEURS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Tous les fondateurs peuvent voir les autres fondateurs
CREATE POLICY "Founders can view all founders"
  ON founders FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM founders f
      WHERE f.user_id = auth.uid()
    )
    OR
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- Les fondateurs peuvent modifier leur propre profil
CREATE POLICY "Founders can update own profile"
  ON founders FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- Insertion gérée par fonction sécurisée
CREATE POLICY "System can insert founders"
  ON founders FOR INSERT
  WITH CHECK (user_id = auth.uid());

-- ═══════════════════════════════════════════════════════════════════════════════
-- 8. POLICIES POUR CONNEXIONS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Les fondateurs peuvent voir leurs connexions
CREATE POLICY "Founders can view connections"
  ON founder_connections FOR SELECT
  USING (
    founder_a = auth.uid() OR founder_b = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- Les fondateurs peuvent créer des connexions
CREATE POLICY "Founders can create connections"
  ON founder_connections FOR INSERT
  WITH CHECK (
    initiated_by = auth.uid()
    AND EXISTS (SELECT 1 FROM founders WHERE user_id = auth.uid())
  );

-- Les fondateurs peuvent modifier leurs connexions
CREATE POLICY "Founders can update own connections"
  ON founder_connections FOR UPDATE
  USING (founder_a = auth.uid() OR founder_b = auth.uid());

-- ═══════════════════════════════════════════════════════════════════════════════
-- 9. POLICIES POUR MESSAGES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Tous les fondateurs peuvent voir les messages
CREATE POLICY "Founders can view messages"
  ON founder_messages FOR SELECT
  USING (
    EXISTS (SELECT 1 FROM founders WHERE user_id = auth.uid())
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- Les fondateurs peuvent créer des messages
CREATE POLICY "Founders can create messages"
  ON founder_messages FOR INSERT
  WITH CHECK (
    author_id = auth.uid()
    AND EXISTS (SELECT 1 FROM founders WHERE user_id = auth.uid())
  );

-- Les fondateurs peuvent modifier leurs propres messages
CREATE POLICY "Founders can update own messages"
  ON founder_messages FOR UPDATE
  USING (author_id = auth.uid());

-- Les fondateurs peuvent supprimer leurs propres messages
CREATE POLICY "Founders can delete own messages"
  ON founder_messages FOR DELETE
  USING (author_id = auth.uid());

-- ═══════════════════════════════════════════════════════════════════════════════
-- 9.1 POLICIES POUR ENERGY_GRID
-- ═══════════════════════════════════════════════════════════════════════════════

-- Seuls les fondateurs activés peuvent voir la Grid
CREATE POLICY "Activated founders can view energy grid"
  ON energy_grid FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM founders f
      WHERE f.user_id = auth.uid()
      AND f.energy_status = 'activated'
    )
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- Seul le Souverain peut créer des points de Grid
CREATE POLICY "Souverain can create grid points"
  ON energy_grid FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- Seul le Souverain peut modifier la Grid
CREATE POLICY "Souverain can update grid points"
  ON energy_grid FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'souverain'
    )
  );

-- ═══════════════════════════════════════════════════════════════════════════════
-- 10. FONCTIONS SÉCURISÉES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Fonction pour valider et utiliser un code d'invitation
CREATE OR REPLACE FUNCTION use_invitation_code(invitation_code TEXT)
RETURNS JSONB AS $$
DECLARE
  inv RECORD;
  founder_num INTEGER;
  result JSONB;
BEGIN
  -- Trouver l'invitation
  SELECT * INTO inv FROM invitations
    WHERE code = invitation_code
    AND status = 'pending'
    AND (expires_at IS NULL OR expires_at > NOW())
    AND use_count < max_uses;

  IF inv IS NULL THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Code d''invitation invalide, expiré ou déjà utilisé'
    );
  END IF;

  -- Vérifier si l'utilisateur n'est pas déjà fondateur
  IF EXISTS (SELECT 1 FROM founders WHERE user_id = auth.uid()) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Vous êtes déjà membre fondateur'
    );
  END IF;

  -- Calculer le numéro de fondateur
  SELECT COALESCE(MAX(founder_number), 0) + 1 INTO founder_num FROM founders;

  -- Créer l'entrée fondateur
  INSERT INTO founders (user_id, invitation_id, founder_type, founder_number)
  VALUES (auth.uid(), inv.id, inv.founder_type, founder_num);

  -- Mettre à jour l'invitation
  UPDATE invitations
  SET
    status = CASE WHEN use_count + 1 >= max_uses THEN 'accepted' ELSE status END,
    use_count = use_count + 1,
    accepted_by = auth.uid(),
    accepted_at = NOW()
  WHERE id = inv.id;

  -- Mettre à jour le profil avec le rôle fondateur
  UPDATE profiles
  SET role = 'fondateur', updated_at = NOW()
  WHERE id = auth.uid();

  RETURN jsonb_build_object(
    'success', true,
    'founder_number', founder_num,
    'founder_type', inv.founder_type,
    'message', inv.personal_message
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour vérifier un code sans l'utiliser
CREATE OR REPLACE FUNCTION verify_invitation_code(invitation_code TEXT)
RETURNS JSONB AS $$
DECLARE
  inv RECORD;
BEGIN
  SELECT invited_name, founder_type, personal_message, expires_at
  INTO inv FROM invitations
    WHERE code = invitation_code
    AND status = 'pending'
    AND (expires_at IS NULL OR expires_at > NOW())
    AND use_count < max_uses;

  IF inv IS NULL THEN
    RETURN jsonb_build_object('valid', false);
  END IF;

  RETURN jsonb_build_object(
    'valid', true,
    'invited_name', inv.invited_name,
    'founder_type', inv.founder_type,
    'personal_message', inv.personal_message,
    'expires_at', inv.expires_at
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour générer un code d'invitation unique
CREATE OR REPLACE FUNCTION generate_invitation_code()
RETURNS TEXT AS $$
DECLARE
  chars TEXT := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  result TEXT := 'ATOM-';
  i INTEGER;
BEGIN
  -- Format: ATOM-XXXX-XXXX
  FOR i IN 1..4 LOOP
    result := result || substr(chars, floor(random() * length(chars) + 1)::integer, 1);
  END LOOP;
  result := result || '-';
  FOR i IN 1..4 LOOP
    result := result || substr(chars, floor(random() * length(chars) + 1)::integer, 1);
  END LOOP;
  RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour créer une invitation (réservée au Souverain)
CREATE OR REPLACE FUNCTION create_invitation(
  p_invited_name TEXT,
  p_invited_email TEXT DEFAULT NULL,
  p_personal_message TEXT DEFAULT NULL,
  p_founder_type TEXT DEFAULT 'lumiere',
  p_contribution_note TEXT DEFAULT NULL,
  p_expires_days INTEGER DEFAULT 30
)
RETURNS JSONB AS $$
DECLARE
  new_code TEXT;
  inv_id UUID;
BEGIN
  -- Vérifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Seul le Souverain peut créer des invitations'
    );
  END IF;

  -- Générer un code unique
  LOOP
    new_code := generate_invitation_code();
    EXIT WHEN NOT EXISTS (SELECT 1 FROM invitations WHERE code = new_code);
  END LOOP;

  -- Créer l'invitation
  INSERT INTO invitations (
    code, invited_name, invited_email, personal_message,
    founder_type, contribution_note, created_by,
    expires_at
  ) VALUES (
    new_code, p_invited_name, p_invited_email, p_personal_message,
    p_founder_type, p_contribution_note, auth.uid(),
    NOW() + (p_expires_days || ' days')::interval
  )
  RETURNING id INTO inv_id;

  RETURN jsonb_build_object(
    'success', true,
    'invitation_id', inv_id,
    'code', new_code,
    'expires_at', NOW() + (p_expires_days || ' days')::interval
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 10.1 FONCTIONS GRID ÉNERGÉTIQUE
-- ═══════════════════════════════════════════════════════════════════════════════

-- Fonction pour activer un fondateur dans la Grid (Souverain seulement)
CREATE OR REPLACE FUNCTION activate_founder_in_grid(
  p_user_id UUID,
  p_energy_signature INTEGER DEFAULT 444
)
RETURNS JSONB AS $$
DECLARE
  founder_rec RECORD;
BEGIN
  -- Vérifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Seul le Souverain peut activer les fondateurs dans la Grid'
    );
  END IF;

  -- Vérifier que le fondateur existe
  SELECT * INTO founder_rec FROM founders WHERE user_id = p_user_id;

  IF founder_rec IS NULL THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Fondateur non trouvé'
    );
  END IF;

  -- Activer le fondateur
  UPDATE founders
  SET
    energy_status = 'activated',
    energy_signature = p_energy_signature,
    grid_activated_at = NOW(),
    updated_at = NOW()
  WHERE user_id = p_user_id;

  RETURN jsonb_build_object(
    'success', true,
    'message', 'Fondateur activé dans la Grid',
    'founder_number', founder_rec.founder_number,
    'energy_signature', p_energy_signature
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour mettre à jour la position Grid d'un fondateur
CREATE OR REPLACE FUNCTION update_grid_position(
  p_latitude DECIMAL,
  p_longitude DECIMAL,
  p_location_name TEXT
)
RETURNS JSONB AS $$
BEGIN
  -- Vérifier que l'utilisateur est fondateur
  IF NOT EXISTS (SELECT 1 FROM founders WHERE user_id = auth.uid()) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Vous devez être membre fondateur'
    );
  END IF;

  -- Mettre à jour la position
  UPDATE founders
  SET
    grid_latitude = p_latitude,
    grid_longitude = p_longitude,
    grid_location_name = p_location_name,
    updated_at = NOW()
  WHERE user_id = auth.uid();

  RETURN jsonb_build_object(
    'success', true,
    'message', 'Position Grid mise à jour'
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour créer un point d'ancrage dans la Grid (Souverain seulement)
CREATE OR REPLACE FUNCTION create_grid_point(
  p_name TEXT,
  p_latitude DECIMAL,
  p_longitude DECIMAL,
  p_point_type TEXT DEFAULT 'anchor',
  p_frequency INTEGER DEFAULT 444,
  p_guardian_id UUID DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
  new_point_id UUID;
BEGIN
  -- Vérifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Seul le Souverain peut créer des points de Grid'
    );
  END IF;

  -- Créer le point
  INSERT INTO energy_grid (
    name, latitude, longitude, point_type, frequency, guardian_id
  ) VALUES (
    p_name, p_latitude, p_longitude, p_point_type, p_frequency, p_guardian_id
  )
  RETURNING id INTO new_point_id;

  RETURN jsonb_build_object(
    'success', true,
    'point_id', new_point_id,
    'message', 'Point de Grid créé: ' || p_name
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour obtenir les statistiques de la Grid
CREATE OR REPLACE FUNCTION get_grid_stats()
RETURNS JSONB AS $$
DECLARE
  stats JSONB;
BEGIN
  -- Vérifier que l'utilisateur est fondateur activé ou Souverain
  IF NOT EXISTS (
    SELECT 1 FROM founders
    WHERE user_id = auth.uid() AND energy_status = 'activated'
  ) AND NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object(
      'success', false,
      'error', 'Accès réservé aux fondateurs activés'
    );
  END IF;

  SELECT jsonb_build_object(
    'success', true,
    'total_founders', (SELECT COUNT(*) FROM founders),
    'activated_founders', (SELECT COUNT(*) FROM founders WHERE energy_status = 'activated'),
    'calibrating_founders', (SELECT COUNT(*) FROM founders WHERE energy_status = 'calibrating'),
    'grid_points', (SELECT COUNT(*) FROM energy_grid WHERE is_active = true),
    'countries_represented', (SELECT COUNT(DISTINCT location_country) FROM founders WHERE location_country IS NOT NULL),
    'frequency_distribution', (
      SELECT jsonb_object_agg(energy_signature, count)
      FROM (
        SELECT energy_signature, COUNT(*) as count
        FROM founders
        WHERE energy_signature IS NOT NULL
        GROUP BY energy_signature
      ) freq
    )
  ) INTO stats;

  RETURN stats;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 11. INDEX POUR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_invitations_code ON invitations(code);
CREATE INDEX IF NOT EXISTS idx_invitations_status ON invitations(status);
CREATE INDEX IF NOT EXISTS idx_founders_user_id ON founders(user_id);
CREATE INDEX IF NOT EXISTS idx_founders_founder_number ON founders(founder_number);
CREATE INDEX IF NOT EXISTS idx_founders_energy_status ON founders(energy_status);
CREATE INDEX IF NOT EXISTS idx_founders_grid_location ON founders(grid_latitude, grid_longitude);
CREATE INDEX IF NOT EXISTS idx_founder_connections_founders ON founder_connections(founder_a, founder_b);
CREATE INDEX IF NOT EXISTS idx_founder_messages_author ON founder_messages(author_id);
CREATE INDEX IF NOT EXISTS idx_founder_messages_created ON founder_messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_energy_grid_location ON energy_grid(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_energy_grid_guardian ON energy_grid(guardian_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 12. MISE À JOUR DU RÔLE PROFILES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Ajouter 'fondateur' comme rôle valide si pas déjà fait
-- (Note: profiles.role est TEXT sans contrainte, donc pas de modification nécessaire)

-- ═══════════════════════════════════════════════════════════════════════════════
-- 13. POINT D'ANCRAGE INITIAL - QUÉBEC
-- ═══════════════════════════════════════════════════════════════════════════════

-- Créer le premier point d'ancrage au Québec (Centre de la Grid)
INSERT INTO energy_grid (name, latitude, longitude, point_type, frequency, is_active)
VALUES ('Québec - Point Zéro', 46.8139, -71.2080, 'anchor', 999, true)
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN DU SCRIPT D'INVITATION ET GRID ÉNERGÉTIQUE
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- RÉSUMÉ:
-- ✅ Table invitations: Codes d'invitation uniques avec expiration
-- ✅ Table founders: Profils étendus avec Grid énergétique
-- ✅ Table energy_grid: Points d'ancrage planétaires
-- ✅ Table founder_connections: Liens entre fondateurs
-- ✅ Table founder_messages: Cercle de communication
-- ✅ Fonctions sécurisées pour gérer les invitations
-- ✅ Fonctions Grid: activation, positionnement, statistiques
-- ✅ RLS strict: Seuls les fondateurs activés voient la Grid
--
-- TYPES DE FONDATEURS:
-- 🌟 lumiere - Point de Lumière International
-- 🛡️ gardien - Gardien de l'Arche
-- 🏛️ architecte - Architecte de Civilisation
-- 🕸️ tisserand - Tisserand de Liens
-- 🔥 porteur - Porteur de Flamme
--
-- SIGNATURES ÉNERGÉTIQUES:
-- 111, 222, 333, 444 (Heartbeat), 528 (Love), 639, 741, 852, 963, 999 (Source)
--
-- STATUTS D'ACTIVATION:
-- calibrating → aligned → activated → (dormant si pause)
--
-- TYPES DE CONTRIBUTION:
-- energetic, material, scientific, creative, healing, bridge
--
-- TYPES DE POINTS GRID:
-- anchor, node, portal, sanctuary
--
-- ═══════════════════════════════════════════════════════════════════════════════
