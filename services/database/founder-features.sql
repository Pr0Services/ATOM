-- ===============================================================================
-- AT·OM - FOUNDER FEATURES SQL
-- Version simplifiée - Ne touche PAS aux tables threads existantes
-- ===============================================================================
--
-- INSTRUCTIONS:
-- 1. Exécuter D'ABORD: 01-fix-existing-policies.sql (si erreur de participants)
-- 2. Ensuite exécuter ce fichier
--
-- ===============================================================================

-- ===============================================================================
-- SECTION 1: MISE À JOUR DE LA TABLE PROFILES
-- ===============================================================================

-- 1.1 Ajouter la colonne role si elle n'existe pas
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'profiles' AND column_name = 'role'
  ) THEN
    ALTER TABLE profiles ADD COLUMN role TEXT DEFAULT 'FOUNDER';
  END IF;
END $$;

-- 1.2 Ajouter les colonnes YouTube/Social si elles n'existent pas
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'profiles' AND column_name = 'youtube_channel_url'
  ) THEN
    ALTER TABLE profiles ADD COLUMN youtube_channel_url TEXT;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'profiles' AND column_name = 'facebook_url'
  ) THEN
    ALTER TABLE profiles ADD COLUMN facebook_url TEXT;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'profiles' AND column_name = 'is_active_creator'
  ) THEN
    ALTER TABLE profiles ADD COLUMN is_active_creator BOOLEAN DEFAULT FALSE;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'profiles' AND column_name = 'creator_verified_at'
  ) THEN
    ALTER TABLE profiles ADD COLUMN creator_verified_at TIMESTAMPTZ;
  END IF;
END $$;

-- 1.3 Index pour les créateurs actifs
CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);
CREATE INDEX IF NOT EXISTS idx_profiles_active_creator ON profiles(is_active_creator)
WHERE is_active_creator = TRUE;

-- ===============================================================================
-- SECTION 2: MISE À JOUR DE LA TABLE COMMUNITY_MESSAGES
-- ===============================================================================

-- 2.1 Créer si n'existe pas
CREATE TABLE IF NOT EXISTS community_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  sender_id TEXT NOT NULL,
  sender_name TEXT,
  room TEXT DEFAULT 'global',
  origin_context TEXT DEFAULT 'founder',
  future_sphere TEXT DEFAULT 'communication',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2.2 Ajouter la colonne room si elle n'existe pas
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'community_messages' AND column_name = 'room'
  ) THEN
    ALTER TABLE community_messages ADD COLUMN room TEXT DEFAULT 'global';
  END IF;
END $$;

-- 2.3 Index
CREATE INDEX IF NOT EXISTS idx_community_messages_room ON community_messages(room);
CREATE INDEX IF NOT EXISTS idx_community_messages_created ON community_messages(created_at);

-- 2.4 RLS
ALTER TABLE community_messages ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE
  pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'community_messages'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON community_messages', pol.policyname);
  END LOOP;
END $$;

CREATE POLICY "Anyone can view messages"
ON community_messages FOR SELECT
USING (true);

CREATE POLICY "Authenticated can send messages"
ON community_messages FOR INSERT
WITH CHECK (true);

-- ===============================================================================
-- SECTION 3: TABLE UNDERGROUND_VIDEOS (Vault)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS underground_videos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  file_path TEXT NOT NULL,
  file_size BIGINT,
  duration_seconds INTEGER,
  thumbnail_path TEXT,
  uploaded_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  uploader_name TEXT,
  visibility TEXT DEFAULT 'founders',
  category TEXT DEFAULT 'general',
  origin_context TEXT DEFAULT 'founder',
  future_sphere TEXT DEFAULT 'scholar',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_underground_videos_visibility ON underground_videos(visibility);
CREATE INDEX IF NOT EXISTS idx_underground_videos_category ON underground_videos(category);
CREATE INDEX IF NOT EXISTS idx_underground_videos_created ON underground_videos(created_at DESC);

-- RLS
ALTER TABLE underground_videos ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE
  pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'underground_videos'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON underground_videos', pol.policyname);
  END LOOP;
END $$;

CREATE POLICY "Founders can view underground videos"
ON underground_videos FOR SELECT
TO authenticated
USING (
  visibility = 'all'
  OR visibility = 'founders'
  OR (visibility = 'admins' AND EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
  ))
);

CREATE POLICY "Founders can upload underground videos"
ON underground_videos FOR INSERT
TO authenticated
WITH CHECK (true);

CREATE POLICY "Uploaders can update their videos"
ON underground_videos FOR UPDATE
TO authenticated
USING (uploaded_by = auth.uid());

-- ===============================================================================
-- SECTION 4: TABLE ACTIVITY_FEED
-- ===============================================================================

CREATE TABLE IF NOT EXISTS activity_feed (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  user_name TEXT,
  activity_type TEXT NOT NULL,
  content TEXT,
  metadata JSONB DEFAULT '{}',
  origin_context TEXT DEFAULT 'founder',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_activity_feed_created ON activity_feed(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_activity_feed_type ON activity_feed(activity_type);
CREATE INDEX IF NOT EXISTS idx_activity_feed_user ON activity_feed(user_id);

-- RLS
ALTER TABLE activity_feed ENABLE ROW LEVEL SECURITY;

DO $$
DECLARE
  pol RECORD;
BEGIN
  FOR pol IN SELECT policyname FROM pg_policies WHERE tablename = 'activity_feed'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON activity_feed', pol.policyname);
  END LOOP;
END $$;

CREATE POLICY "Anyone can view activity feed"
ON activity_feed FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "Users can create their activity"
ON activity_feed FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid() OR user_id IS NULL);

-- ===============================================================================
-- SECTION 5: TRIGGER POUR ENREGISTRER L'ACTIVITÉ
-- ===============================================================================

CREATE OR REPLACE FUNCTION log_user_activity()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_TABLE_NAME = 'community_messages' THEN
    INSERT INTO activity_feed (user_id, user_name, activity_type, content, metadata)
    VALUES (
      CASE WHEN NEW.sender_id ~ '^[0-9a-f-]{36}$' THEN NEW.sender_id::UUID ELSE NULL END,
      NEW.sender_name,
      'message',
      LEFT(NEW.content, 100),
      jsonb_build_object('room', COALESCE(NEW.room, 'global'))
    );
  END IF;

  IF TG_TABLE_NAME = 'underground_videos' THEN
    INSERT INTO activity_feed (user_id, user_name, activity_type, content, metadata)
    VALUES (
      NEW.uploaded_by,
      NEW.uploader_name,
      'video_upload',
      NEW.title,
      jsonb_build_object('category', NEW.category)
    );
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_message_activity ON community_messages;
CREATE TRIGGER on_message_activity
AFTER INSERT ON community_messages
FOR EACH ROW EXECUTE FUNCTION log_user_activity();

DROP TRIGGER IF EXISTS on_video_activity ON underground_videos;
CREATE TRIGGER on_video_activity
AFTER INSERT ON underground_videos
FOR EACH ROW EXECUTE FUNCTION log_user_activity();

-- ===============================================================================
-- SECTION 6: ACTIVER REALTIME
-- ===============================================================================

DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE community_messages;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE underground_videos;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE activity_feed;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;

-- ===============================================================================
-- FIN DU SCRIPT - FOUNDER FEATURES
-- ===============================================================================
