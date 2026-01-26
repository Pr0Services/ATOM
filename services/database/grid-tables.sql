-- ===============================================================================
-- AT·OM - TABLES POUR LA GRILLE DES FONDATEURS
-- À exécuter dans Supabase SQL Editor
-- ===============================================================================

-- ===============================================================================
-- TABLE: community_messages (Chat global)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS public.community_messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  content TEXT NOT NULL,
  sender_id TEXT NOT NULL,
  sender_name TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour performance
CREATE INDEX IF NOT EXISTS idx_community_messages_created
  ON public.community_messages(created_at DESC);

-- RLS (Row Level Security)
ALTER TABLE public.community_messages ENABLE ROW LEVEL SECURITY;

-- Politique: Tout le monde peut lire les messages
CREATE POLICY "Anyone can read community messages"
  ON public.community_messages FOR SELECT
  USING (true);

-- Politique: Les utilisateurs authentifiés peuvent poster
CREATE POLICY "Authenticated users can insert messages"
  ON public.community_messages FOR INSERT
  WITH CHECK (true);

-- ===============================================================================
-- TABLE: private_threads (Threads privés)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS public.private_threads (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  participant_ids TEXT[] NOT NULL DEFAULT '{}',
  participants_count INTEGER DEFAULT 0,
  messages_count INTEGER DEFAULT 0,
  created_by TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_private_threads_participants
  ON public.private_threads USING GIN(participant_ids);
CREATE INDEX IF NOT EXISTS idx_private_threads_updated
  ON public.private_threads(updated_at DESC);

-- RLS
ALTER TABLE public.private_threads ENABLE ROW LEVEL SECURITY;

-- Politique: Seuls les participants peuvent voir le thread
CREATE POLICY "Participants can read their threads"
  ON public.private_threads FOR SELECT
  USING (auth.uid()::text = ANY(participant_ids) OR created_by = auth.uid()::text);

-- Politique: Les utilisateurs authentifiés peuvent créer des threads
CREATE POLICY "Users can create threads"
  ON public.private_threads FOR INSERT
  WITH CHECK (auth.uid()::text = created_by);

-- ===============================================================================
-- TABLE: thread_messages (Messages des threads privés)
-- ===============================================================================

CREATE TABLE IF NOT EXISTS public.thread_messages (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  thread_id UUID REFERENCES public.private_threads(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  sender_id TEXT NOT NULL,
  sender_name TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_thread_messages_thread
  ON public.thread_messages(thread_id);
CREATE INDEX IF NOT EXISTS idx_thread_messages_created
  ON public.thread_messages(created_at ASC);

-- RLS
ALTER TABLE public.thread_messages ENABLE ROW LEVEL SECURITY;

-- Politique: Seuls les participants du thread peuvent lire les messages
CREATE POLICY "Participants can read thread messages"
  ON public.thread_messages FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.private_threads
      WHERE id = thread_messages.thread_id
      AND (auth.uid()::text = ANY(participant_ids) OR created_by = auth.uid()::text)
    )
  );

-- Politique: Les participants peuvent poster des messages
CREATE POLICY "Participants can insert messages"
  ON public.thread_messages FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.private_threads
      WHERE id = thread_messages.thread_id
      AND (auth.uid()::text = ANY(participant_ids) OR created_by = auth.uid()::text)
    )
  );

-- ===============================================================================
-- FONCTION: Incrémenter le compteur de messages d'un thread
-- ===============================================================================

CREATE OR REPLACE FUNCTION increment_thread_messages()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.private_threads
  SET messages_count = messages_count + 1,
      updated_at = NOW()
  WHERE id = NEW.thread_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger pour mettre à jour automatiquement
DROP TRIGGER IF EXISTS on_thread_message_insert ON public.thread_messages;
CREATE TRIGGER on_thread_message_insert
  AFTER INSERT ON public.thread_messages
  FOR EACH ROW
  EXECUTE FUNCTION increment_thread_messages();

-- ===============================================================================
-- ACTIVER LE REALTIME POUR CES TABLES
-- ===============================================================================

-- Dans Supabase Dashboard > Database > Replication
-- Activer les publications pour:
-- - community_messages
-- - private_threads
-- - thread_messages

ALTER PUBLICATION supabase_realtime ADD TABLE community_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE private_threads;
ALTER PUBLICATION supabase_realtime ADD TABLE thread_messages;

-- ===============================================================================
-- MISE À JOUR DE LA TABLE PROFILES (si nécessaire)
-- ===============================================================================

-- Ajouter la colonne metadata si elle n'existe pas
ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- Ajouter la colonne frequency si elle n'existe pas
ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS frequency INTEGER DEFAULT 369;

-- ===============================================================================
-- VÉRIFICATION
-- ===============================================================================

-- Exécuter pour vérifier que les tables sont créées:
-- SELECT table_name FROM information_schema.tables
-- WHERE table_schema = 'public'
-- AND table_name IN ('community_messages', 'private_threads', 'thread_messages');
