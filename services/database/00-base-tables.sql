-- ===============================================================================
-- AT·OM — TABLES DE BASE
-- À exécuter EN PREMIER avant tous les autres scripts
-- ===============================================================================

-- 1. TABLE: PROFILES (utilisateurs/fondateurs)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  avatar_url TEXT,
  bio TEXT,
  role TEXT DEFAULT 'FOUNDER' CHECK (role IN ('FOUNDER', 'SOUVERAIN', 'admin', 'architect', 'member')),
  frequency DECIMAL(10, 2) DEFAULT 369,

  -- Métadonnées de migration (Founder → Sphères)
  origin_context TEXT DEFAULT 'founder',
  migration_status TEXT DEFAULT 'pending' CHECK (migration_status IN ('pending', 'ready', 'migrated')),

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);
CREATE INDEX IF NOT EXISTS idx_profiles_created ON profiles(created_at);

-- RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Policies
DROP POLICY IF EXISTS "Public profiles are viewable by everyone" ON profiles;
CREATE POLICY "Public profiles are viewable by everyone"
ON profiles FOR SELECT
USING (true);

DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;
CREATE POLICY "Users can insert own profile"
ON profiles FOR INSERT
WITH CHECK (auth.uid() = id OR auth.uid() IS NULL);

DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
CREATE POLICY "Users can update own profile"
ON profiles FOR UPDATE
USING (auth.uid() = id);

-- Trigger pour auto-créer profil à l'inscription
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, avatar_url)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
    NEW.raw_user_meta_data->>'avatar_url'
  )
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 2. TABLE: COMMUNITY_MESSAGES (chat global)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS community_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  sender_id TEXT NOT NULL,
  sender_name TEXT,

  -- Métadonnées de migration
  origin_context TEXT DEFAULT 'founder',
  future_sphere TEXT DEFAULT 'communication',

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_messages_created ON community_messages(created_at);
CREATE INDEX IF NOT EXISTS idx_messages_sender ON community_messages(sender_id);

-- RLS
ALTER TABLE community_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view messages" ON community_messages;
CREATE POLICY "Anyone can view messages"
ON community_messages FOR SELECT
USING (true);

DROP POLICY IF EXISTS "Authenticated can send messages" ON community_messages;
CREATE POLICY "Authenticated can send messages"
ON community_messages FOR INSERT
WITH CHECK (true);

-- 3. TABLE: PRIVATE_THREADS (conversations privées)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS private_threads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT,
  participants UUID[] NOT NULL,
  created_by UUID REFERENCES auth.users(id),

  -- Métadonnées de migration
  origin_context TEXT DEFAULT 'founder',
  future_sphere TEXT DEFAULT 'communication',

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_threads_participants ON private_threads USING GIN(participants);
CREATE INDEX IF NOT EXISTS idx_threads_updated ON private_threads(updated_at DESC);

-- RLS
ALTER TABLE private_threads ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Participants can view threads" ON private_threads;
CREATE POLICY "Participants can view threads"
ON private_threads FOR SELECT
USING (auth.uid() = ANY(participants));

DROP POLICY IF EXISTS "Authenticated can create threads" ON private_threads;
CREATE POLICY "Authenticated can create threads"
ON private_threads FOR INSERT
WITH CHECK (auth.uid() = created_by);

-- 4. TABLE: THREAD_MESSAGES (messages dans les threads privés)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS thread_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  thread_id UUID REFERENCES private_threads(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  sender_id UUID REFERENCES auth.users(id),
  sender_name TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_thread_messages_thread ON thread_messages(thread_id);
CREATE INDEX IF NOT EXISTS idx_thread_messages_created ON thread_messages(created_at);

-- RLS
ALTER TABLE thread_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Thread participants can view messages" ON thread_messages;
CREATE POLICY "Thread participants can view messages"
ON thread_messages FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM private_threads
    WHERE id = thread_messages.thread_id
    AND auth.uid() = ANY(participants)
  )
);

DROP POLICY IF EXISTS "Thread participants can send messages" ON thread_messages;
CREATE POLICY "Thread participants can send messages"
ON thread_messages FOR INSERT
WITH CHECK (
  EXISTS (
    SELECT 1 FROM private_threads
    WHERE id = thread_messages.thread_id
    AND auth.uid() = ANY(participants)
  )
);

-- 5. REALTIME
-- ===============================================================================

-- Activer realtime sur les tables principales
ALTER PUBLICATION supabase_realtime ADD TABLE profiles;
ALTER PUBLICATION supabase_realtime ADD TABLE community_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE private_threads;
ALTER PUBLICATION supabase_realtime ADD TABLE thread_messages;

-- ===============================================================================
-- FIN DU SCRIPT DE BASE
-- ===============================================================================

-- Vérification:
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
