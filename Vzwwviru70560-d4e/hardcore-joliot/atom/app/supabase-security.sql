-- ═══════════════════════════════════════════════════════════════════════════════
--
--       ███████╗██╗   ██╗██████╗  █████╗ ██████╗  █████╗ ███████╗███████╗
--       ██╔════╝██║   ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
--       ███████╗██║   ██║██████╔╝███████║██████╔╝███████║███████╗█████╗
--       ╚════██║██║   ██║██╔═══╝ ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝
--       ███████║╚██████╔╝██║     ██║  ██║██████╔╝██║  ██║███████║███████╗
--       ╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
--
--                    SCRIPT DE SÉCURITÉ RLS - AT·OM / CHE·NU V76
--                   Row Level Security & Policies pour Supabase
--
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- INSTRUCTIONS:
-- 1. Connectez-vous à votre dashboard Supabase
-- 2. Allez dans SQL Editor
-- 3. Copiez-collez ce script
-- 4. Exécutez-le
--
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. CRÉATION DES TABLES (si elles n'existent pas)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Table des perceptions utilisateur
CREATE TABLE IF NOT EXISTS perceptions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  text TEXT NOT NULL,
  frequency INTEGER DEFAULT 999,
  heartbeat INTEGER DEFAULT 444,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des besoins locaux
CREATE TABLE IF NOT EXISTS local_needs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  description TEXT,
  category TEXT NOT NULL,
  location TEXT DEFAULT 'Québec',
  priority TEXT DEFAULT 'medium',
  votes INTEGER DEFAULT 0,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des votes (pour éviter les votes multiples)
CREATE TABLE IF NOT EXISTS need_votes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  need_id UUID REFERENCES local_needs(id) ON DELETE CASCADE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, need_id)
);

-- Table des profils utilisateur (extension de auth.users)
CREATE TABLE IF NOT EXISTS profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  display_name TEXT,
  role TEXT DEFAULT 'citoyen',
  frequency INTEGER DEFAULT 444,
  avatar_url TEXT,
  bio TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des entrées de gratitude
CREATE TABLE IF NOT EXISTS gratitude_entries (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  content TEXT NOT NULL,
  category TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table des configurations utilisateur (chiffrées côté client)
CREATE TABLE IF NOT EXISTS user_settings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL UNIQUE,
  settings_encrypted TEXT, -- Données chiffrées côté client
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. ACTIVER ROW LEVEL SECURITY (RLS)
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE perceptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE local_needs ENABLE ROW LEVEL SECURITY;
ALTER TABLE need_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE gratitude_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. SUPPRIMER LES ANCIENNES POLICIES (pour éviter les conflits)
-- ═══════════════════════════════════════════════════════════════════════════════

DROP POLICY IF EXISTS "Users can view own perceptions" ON perceptions;
DROP POLICY IF EXISTS "Users can insert own perceptions" ON perceptions;
DROP POLICY IF EXISTS "Users can update own perceptions" ON perceptions;
DROP POLICY IF EXISTS "Users can delete own perceptions" ON perceptions;

DROP POLICY IF EXISTS "Anyone can view local needs" ON local_needs;
DROP POLICY IF EXISTS "Authenticated users can create needs" ON local_needs;
DROP POLICY IF EXISTS "Users can update own needs" ON local_needs;
DROP POLICY IF EXISTS "Users can delete own needs" ON local_needs;

DROP POLICY IF EXISTS "Users can view own votes" ON need_votes;
DROP POLICY IF EXISTS "Authenticated users can vote" ON need_votes;
DROP POLICY IF EXISTS "Users can remove own votes" ON need_votes;

DROP POLICY IF EXISTS "Public profiles are viewable by everyone" ON profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;

DROP POLICY IF EXISTS "Users can view own gratitude entries" ON gratitude_entries;
DROP POLICY IF EXISTS "Users can insert own gratitude entries" ON gratitude_entries;
DROP POLICY IF EXISTS "Users can delete own gratitude entries" ON gratitude_entries;

DROP POLICY IF EXISTS "Users can view own settings" ON user_settings;
DROP POLICY IF EXISTS "Users can upsert own settings" ON user_settings;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. POLICIES POUR PERCEPTIONS (Données privées par utilisateur)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Les utilisateurs peuvent voir UNIQUEMENT leurs propres perceptions
CREATE POLICY "Users can view own perceptions"
  ON perceptions FOR SELECT
  USING (auth.uid() = user_id);

-- Les utilisateurs peuvent créer des perceptions pour eux-mêmes
CREATE POLICY "Users can insert own perceptions"
  ON perceptions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Les utilisateurs peuvent modifier leurs propres perceptions
CREATE POLICY "Users can update own perceptions"
  ON perceptions FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Les utilisateurs peuvent supprimer leurs propres perceptions
CREATE POLICY "Users can delete own perceptions"
  ON perceptions FOR DELETE
  USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. POLICIES POUR LOCAL_NEEDS (Données publiques en lecture)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Tout le monde peut voir les besoins locaux (données publiques)
CREATE POLICY "Anyone can view local needs"
  ON local_needs FOR SELECT
  USING (true);

-- Seuls les utilisateurs authentifiés peuvent créer des besoins
CREATE POLICY "Authenticated users can create needs"
  ON local_needs FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Les utilisateurs peuvent modifier leurs propres besoins
CREATE POLICY "Users can update own needs"
  ON local_needs FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Les utilisateurs peuvent supprimer leurs propres besoins
CREATE POLICY "Users can delete own needs"
  ON local_needs FOR DELETE
  USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. POLICIES POUR NEED_VOTES (Votes uniques par utilisateur)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Les utilisateurs peuvent voir leurs propres votes
CREATE POLICY "Users can view own votes"
  ON need_votes FOR SELECT
  USING (auth.uid() = user_id);

-- Les utilisateurs authentifiés peuvent voter
CREATE POLICY "Authenticated users can vote"
  ON need_votes FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Les utilisateurs peuvent retirer leur vote
CREATE POLICY "Users can remove own votes"
  ON need_votes FOR DELETE
  USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. POLICIES POUR PROFILES (Profils publics)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Les profils sont visibles par tous (données publiques)
CREATE POLICY "Public profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (true);

-- Les utilisateurs peuvent créer leur propre profil
CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Les utilisateurs peuvent modifier leur propre profil
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 8. POLICIES POUR GRATITUDE_ENTRIES (Données privées)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Les utilisateurs peuvent voir leurs propres entrées de gratitude
CREATE POLICY "Users can view own gratitude entries"
  ON gratitude_entries FOR SELECT
  USING (auth.uid() = user_id);

-- Les utilisateurs peuvent créer des entrées de gratitude
CREATE POLICY "Users can insert own gratitude entries"
  ON gratitude_entries FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Les utilisateurs peuvent supprimer leurs propres entrées
CREATE POLICY "Users can delete own gratitude entries"
  ON gratitude_entries FOR DELETE
  USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 9. POLICIES POUR USER_SETTINGS (Données privées chiffrées)
-- ═══════════════════════════════════════════════════════════════════════════════

-- Les utilisateurs peuvent voir leurs propres paramètres
CREATE POLICY "Users can view own settings"
  ON user_settings FOR SELECT
  USING (auth.uid() = user_id);

-- Les utilisateurs peuvent créer/modifier leurs paramètres
CREATE POLICY "Users can upsert own settings"
  ON user_settings FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own settings"
  ON user_settings FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 10. FONCTIONS SÉCURISÉES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Fonction pour incrémenter les votes (avec vérification)
CREATE OR REPLACE FUNCTION increment_votes(need_id UUID)
RETURNS VOID AS $$
DECLARE
  existing_vote UUID;
BEGIN
  -- Vérifier si l'utilisateur a déjà voté
  SELECT id INTO existing_vote FROM need_votes
    WHERE need_votes.user_id = auth.uid()
    AND need_votes.need_id = increment_votes.need_id;

  IF existing_vote IS NOT NULL THEN
    RAISE EXCEPTION 'User has already voted for this need';
  END IF;

  -- Ajouter le vote
  INSERT INTO need_votes (user_id, need_id) VALUES (auth.uid(), increment_votes.need_id);

  -- Incrémenter le compteur
  UPDATE local_needs SET votes = votes + 1 WHERE id = increment_votes.need_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Fonction pour retirer un vote
CREATE OR REPLACE FUNCTION remove_vote(need_id UUID)
RETURNS VOID AS $$
BEGIN
  -- Supprimer le vote
  DELETE FROM need_votes
    WHERE need_votes.user_id = auth.uid()
    AND need_votes.need_id = remove_vote.need_id;

  -- Décrémenter le compteur
  UPDATE local_needs SET votes = GREATEST(0, votes - 1) WHERE id = remove_vote.need_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger pour créer automatiquement un profil à l'inscription
CREATE OR REPLACE FUNCTION create_profile_on_signup()
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

-- Supprimer le trigger s'il existe déjà
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Créer le trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION create_profile_on_signup();

-- ═══════════════════════════════════════════════════════════════════════════════
-- 11. INDEX POUR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_perceptions_user_id ON perceptions(user_id);
CREATE INDEX IF NOT EXISTS idx_perceptions_created_at ON perceptions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_local_needs_category ON local_needs(category);
CREATE INDEX IF NOT EXISTS idx_local_needs_votes ON local_needs(votes DESC);
CREATE INDEX IF NOT EXISTS idx_local_needs_status ON local_needs(status);
CREATE INDEX IF NOT EXISTS idx_need_votes_user_id ON need_votes(user_id);
CREATE INDEX IF NOT EXISTS idx_need_votes_need_id ON need_votes(need_id);
CREATE INDEX IF NOT EXISTS idx_gratitude_entries_user_id ON gratitude_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_gratitude_entries_created_at ON gratitude_entries(created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 12. VÉRIFICATION FINALE
-- ═══════════════════════════════════════════════════════════════════════════════

-- Vérifier que RLS est activé sur toutes les tables
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
AND tablename IN ('perceptions', 'local_needs', 'need_votes', 'profiles', 'gratitude_entries', 'user_settings');

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN DU SCRIPT DE SÉCURITÉ
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- RÉSUMÉ DES PROTECTIONS:
-- ✅ RLS activé sur toutes les tables
-- ✅ Perceptions: Données privées par utilisateur
-- ✅ Local Needs: Lecture publique, écriture authentifiée
-- ✅ Votes: Un vote par utilisateur par besoin
-- ✅ Profiles: Lecture publique, modification par propriétaire
-- ✅ Gratitude: Données privées par utilisateur
-- ✅ Settings: Données privées chiffrées par utilisateur
-- ✅ Fonctions sécurisées avec SECURITY DEFINER
-- ✅ Index pour performance
--
-- ═══════════════════════════════════════════════════════════════════════════════
