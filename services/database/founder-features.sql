-- ===============================================================================
-- AT·OM - FOUNDER FEATURES SQL
-- Intégration YouTube, Vault Vidéo Underground, Chat Rooms
-- ===============================================================================

-- 1. AJOUTER LES CHAMPS YOUTUBE ET SOCIAL AU PROFIL
-- ===============================================================================

ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS youtube_channel_url TEXT,
ADD COLUMN IF NOT EXISTS facebook_url TEXT,
ADD COLUMN IF NOT EXISTS is_active_creator BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS creator_verified_at TIMESTAMPTZ;

-- Index pour les créateurs actifs
CREATE INDEX IF NOT EXISTS idx_profiles_active_creator
ON profiles(is_active_creator) WHERE is_active_creator = TRUE;

-- 2. AJOUTER LE CHAMP ROOM AU CHAT COMMUNAUTAIRE
-- ===============================================================================

ALTER TABLE community_messages
ADD COLUMN IF NOT EXISTS room TEXT DEFAULT 'global';

-- Index pour filtrer par room
CREATE INDEX IF NOT EXISTS idx_community_messages_room
ON community_messages(room);

-- 3. TABLE POUR LES VIDÉOS UNDERGROUND (VAULT)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS underground_videos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  file_path TEXT NOT NULL,  -- Chemin dans Supabase Storage
  file_size BIGINT,         -- Taille en bytes
  duration_seconds INTEGER,
  thumbnail_path TEXT,
  uploaded_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  uploader_name TEXT,
  visibility TEXT DEFAULT 'founders', -- 'founders', 'admins', 'all'
  category TEXT DEFAULT 'general',    -- 'ceremony', 'teaching', 'message', 'general'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour les requêtes
CREATE INDEX IF NOT EXISTS idx_underground_videos_visibility
ON underground_videos(visibility);

CREATE INDEX IF NOT EXISTS idx_underground_videos_category
ON underground_videos(category);

CREATE INDEX IF NOT EXISTS idx_underground_videos_created
ON underground_videos(created_at DESC);

-- RLS pour les vidéos underground
ALTER TABLE underground_videos ENABLE ROW LEVEL SECURITY;

-- Politique: Seuls les membres authentifiés peuvent voir
CREATE POLICY "Founders can view underground videos"
ON underground_videos FOR SELECT
TO authenticated
USING (
  visibility = 'all'
  OR visibility = 'founders'
  OR (visibility = 'admins' AND EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect')
  ))
);

-- Politique: Seuls les admins peuvent insérer
CREATE POLICY "Admins can upload underground videos"
ON underground_videos FOR INSERT
TO authenticated
WITH CHECK (
  EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect', 'founder')
  )
);

-- Politique: Seuls les admins peuvent modifier
CREATE POLICY "Admins can update underground videos"
ON underground_videos FOR UPDATE
TO authenticated
USING (
  uploaded_by = auth.uid()
  OR EXISTS (
    SELECT 1 FROM profiles
    WHERE profiles.id = auth.uid()
    AND profiles.role IN ('admin', 'architect')
  )
);

-- 4. TABLE POUR LE FLUX D'ACTIVITÉ
-- ===============================================================================

CREATE TABLE IF NOT EXISTS activity_feed (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  user_name TEXT,
  activity_type TEXT NOT NULL, -- 'joined', 'message', 'video_upload', 'thread_created', 'profile_updated'
  content TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour le flux chronologique
CREATE INDEX IF NOT EXISTS idx_activity_feed_created
ON activity_feed(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_activity_feed_type
ON activity_feed(activity_type);

-- RLS pour le flux d'activité
ALTER TABLE activity_feed ENABLE ROW LEVEL SECURITY;

-- Tout le monde peut lire le flux
CREATE POLICY "Anyone can view activity feed"
ON activity_feed FOR SELECT
TO authenticated
USING (true);

-- Seul le système ou l'utilisateur peut créer ses entrées
CREATE POLICY "Users can create their activity"
ON activity_feed FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid() OR user_id IS NULL);

-- 5. ACTIVER REALTIME POUR LES NOUVELLES TABLES
-- ===============================================================================

ALTER PUBLICATION supabase_realtime ADD TABLE underground_videos;
ALTER PUBLICATION supabase_realtime ADD TABLE activity_feed;

-- 6. FONCTION TRIGGER POUR ENREGISTRER L'ACTIVITÉ
-- ===============================================================================

CREATE OR REPLACE FUNCTION log_user_activity()
RETURNS TRIGGER AS $$
BEGIN
  -- Log quand un message est envoyé
  IF TG_TABLE_NAME = 'community_messages' THEN
    INSERT INTO activity_feed (user_id, user_name, activity_type, content, metadata)
    VALUES (
      NEW.sender_id::UUID,
      NEW.sender_name,
      'message',
      LEFT(NEW.content, 100),
      jsonb_build_object('room', NEW.room)
    );
  END IF;

  -- Log quand une vidéo est uploadée
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

-- Trigger pour les messages
DROP TRIGGER IF EXISTS on_message_activity ON community_messages;
CREATE TRIGGER on_message_activity
AFTER INSERT ON community_messages
FOR EACH ROW EXECUTE FUNCTION log_user_activity();

-- Trigger pour les vidéos
DROP TRIGGER IF EXISTS on_video_activity ON underground_videos;
CREATE TRIGGER on_video_activity
AFTER INSERT ON underground_videos
FOR EACH ROW EXECUTE FUNCTION log_user_activity();

-- 7. CRÉER LE BUCKET POUR LES VIDÉOS UNDERGROUND
-- ===============================================================================
-- Note: Exécuter ces commandes via l'interface Supabase ou l'API

-- CREATE BUCKET 'underground-vault' (à faire via Dashboard Supabase)
-- Paramètres recommandés:
--   - Public: FALSE
--   - File size limit: 50MB (50000000 bytes)
--   - Allowed MIME types: video/mp4, video/webm, video/quicktime

-- Politique de stockage (à exécuter dans SQL Editor de Supabase):

-- INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
-- VALUES (
--   'underground-vault',
--   'underground-vault',
--   false,
--   52428800,  -- 50MB
--   ARRAY['video/mp4', 'video/webm', 'video/quicktime']
-- );

-- Politique pour lire (membres authentifiés uniquement)
-- CREATE POLICY "Authenticated users can read underground vault"
-- ON storage.objects FOR SELECT
-- TO authenticated
-- USING (bucket_id = 'underground-vault');

-- Politique pour upload (founders et admins)
-- CREATE POLICY "Founders can upload to underground vault"
-- ON storage.objects FOR INSERT
-- TO authenticated
-- WITH CHECK (
--   bucket_id = 'underground-vault'
--   AND EXISTS (
--     SELECT 1 FROM profiles
--     WHERE profiles.id = auth.uid()
--     AND profiles.role IN ('admin', 'architect', 'founder')
--   )
-- );

-- ===============================================================================
-- FIN DU SCRIPT
-- ===============================================================================

-- Pour vérifier l'installation:
-- SELECT column_name FROM information_schema.columns WHERE table_name = 'profiles';
-- SELECT * FROM underground_videos LIMIT 5;
-- SELECT * FROM activity_feed ORDER BY created_at DESC LIMIT 10;
