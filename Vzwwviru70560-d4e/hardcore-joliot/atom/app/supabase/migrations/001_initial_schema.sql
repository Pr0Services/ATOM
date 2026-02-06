-- ═══════════════════════════════════════════════════════════════════════════════
-- AT·OM — Schema Initial Supabase
-- Migration 001: Toutes les tables référencées par le frontend
-- ═══════════════════════════════════════════════════════════════════════════════

-- Extension UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: profiles
-- Profils utilisateurs (étendu depuis Supabase Auth)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT,
  display_name TEXT,
  email TEXT,
  avatar_url TEXT,
  role TEXT DEFAULT 'CITOYEN' CHECK (role IN ('CITOYEN', 'COLLABORATEUR', 'SOUVERAIN')),
  frequency NUMERIC DEFAULT 369,
  hedera_account_id TEXT,
  categories JSONB DEFAULT '[]'::jsonb,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger auto-update
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, email, avatar_url)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'name', ''),
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'avatar_url', NEW.raw_user_meta_data->>'picture', '')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public profiles are viewable by everyone"
  ON public.profiles FOR SELECT USING (true);

CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: community_messages
-- Chat communautaire temps réel
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.community_messages (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL CHECK (char_length(content) <= 500),
  sender_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  sender_name TEXT NOT NULL DEFAULT 'Anonyme',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.community_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Messages are viewable by everyone"
  ON public.community_messages FOR SELECT USING (true);

CREATE POLICY "Authenticated users can send messages"
  ON public.community_messages FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- Index pour performance
CREATE INDEX idx_community_messages_created ON public.community_messages(created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: private_threads
-- Fils de discussion privés entre fondateurs
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.private_threads (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  creator_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  participants UUID[] DEFAULT '{}',
  participants_count INT DEFAULT 0,
  messages_count INT DEFAULT 0,
  unread_count INT DEFAULT 0,
  last_message_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.private_threads ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Thread participants can view"
  ON public.private_threads FOR SELECT
  USING (auth.uid() = creator_id OR auth.uid() = ANY(participants));

CREATE POLICY "Authenticated users can create threads"
  ON public.private_threads FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: thread_messages
-- Messages dans les fils privés
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.thread_messages (
  id BIGSERIAL PRIMARY KEY,
  thread_id UUID REFERENCES public.private_threads(id) ON DELETE CASCADE,
  content TEXT NOT NULL CHECK (char_length(content) <= 2000),
  sender_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  sender_name TEXT NOT NULL DEFAULT 'Anonyme',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.thread_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Thread members can view messages"
  ON public.thread_messages FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.private_threads t
      WHERE t.id = thread_id
      AND (auth.uid() = t.creator_id OR auth.uid() = ANY(t.participants))
    )
  );

CREATE POLICY "Thread members can send messages"
  ON public.thread_messages FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.private_threads t
      WHERE t.id = thread_id
      AND (auth.uid() = t.creator_id OR auth.uid() = ANY(t.participants))
    )
  );

CREATE INDEX idx_thread_messages_thread ON public.thread_messages(thread_id, created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: perceptions
-- Mots/analyses soumis dans le NEXUS
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.perceptions (
  id BIGSERIAL PRIMARY KEY,
  word TEXT NOT NULL,
  oracle_number INT,
  frequency NUMERIC,
  analysis JSONB DEFAULT '{}'::jsonb,
  user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.perceptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Perceptions viewable by all"
  ON public.perceptions FOR SELECT USING (true);

CREATE POLICY "Authenticated users can create perceptions"
  ON public.perceptions FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE INDEX idx_perceptions_user ON public.perceptions(user_id, created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: local_needs
-- Besoins locaux avec système de votes
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.local_needs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  category TEXT DEFAULT 'general',
  location TEXT,
  latitude NUMERIC,
  longitude NUMERIC,
  votes INT DEFAULT 0,
  status TEXT DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
  user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.local_needs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Needs viewable by all"
  ON public.local_needs FOR SELECT USING (true);

CREATE POLICY "Authenticated users can create needs"
  ON public.local_needs FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "Users can update own needs"
  ON public.local_needs FOR UPDATE
  USING (auth.uid() = user_id);

-- RPC: Incrémenter les votes
CREATE OR REPLACE FUNCTION increment_votes(need_id UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE public.local_needs SET votes = votes + 1 WHERE id = need_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: founders
-- Membres fondateurs (Grille des 144)
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.founders (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  full_name TEXT NOT NULL,
  role TEXT DEFAULT 'FOUNDER',
  intention TEXT,
  hedera_account_id TEXT,
  invitation_code TEXT UNIQUE,
  invited_by UUID REFERENCES public.founders(id),
  activated BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.founders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Founders viewable by all"
  ON public.founders FOR SELECT USING (true);

CREATE POLICY "Authenticated users can join"
  ON public.founders FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: founder_messages
-- Messages dans le Cercle des Fondateurs
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.founder_messages (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL CHECK (char_length(content) <= 1000),
  sender_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  sender_name TEXT NOT NULL DEFAULT 'Fondateur',
  message_type TEXT DEFAULT 'text',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.founder_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Founder messages viewable by authenticated"
  ON public.founder_messages FOR SELECT
  USING (auth.uid() IS NOT NULL);

CREATE POLICY "Authenticated can post founder messages"
  ON public.founder_messages FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: energy_grid
-- Données de la grille énergétique planétaire
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.energy_grid (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  node_type TEXT DEFAULT 'founder',
  latitude NUMERIC,
  longitude NUMERIC,
  frequency NUMERIC DEFAULT 444,
  intensity NUMERIC DEFAULT 1.0,
  user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.energy_grid ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Grid viewable by all"
  ON public.energy_grid FOR SELECT USING (true);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: armors (NFT Armor Display)
-- Armures visuelles liées aux NFT
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.armors (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  tier TEXT CHECK (tier IN ('graine', 'pousse', 'branche', 'racine', 'arbre')),
  name TEXT,
  asset_url TEXT,
  nft_serial TEXT,
  equipped BOOLEAN DEFAULT true,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.armors ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Armors viewable by all"
  ON public.armors FOR SELECT USING (true);

CREATE POLICY "Users can manage own armors"
  ON public.armors FOR ALL USING (auth.uid() = user_id);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: activity_feed
-- Flux d'activité des fondateurs
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.activity_feed (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  action TEXT NOT NULL,
  target_type TEXT,
  target_id TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.activity_feed ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Activity viewable by authenticated"
  ON public.activity_feed FOR SELECT
  USING (auth.uid() IS NOT NULL);

CREATE INDEX idx_activity_feed_user ON public.activity_feed(user_id, created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: founding_members (Setup Wizard)
-- Membres fondateurs depuis le setup wizard admin
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.founding_members (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT,
  role TEXT DEFAULT 'FOUNDER',
  invited_at TIMESTAMPTZ DEFAULT NOW(),
  accepted_at TIMESTAMPTZ,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'declined'))
);

ALTER TABLE public.founding_members ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Founding members viewable by authenticated"
  ON public.founding_members FOR SELECT
  USING (auth.uid() IS NOT NULL);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: progreso_waitlist
-- Liste d'attente Progreso 2026
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.progreso_waitlist (
  id BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  full_name TEXT,
  interest TEXT,
  source TEXT DEFAULT 'landing',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.progreso_waitlist ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Waitlist insertable by anyone"
  ON public.progreso_waitlist FOR INSERT
  WITH CHECK (true);

-- ═══════════════════════════════════════════════════════════════════════════════
-- TABLE: api_usage
-- Tracking de l'utilisation API par utilisateur
-- ═══════════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS public.api_usage (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  endpoint TEXT NOT NULL,
  method TEXT DEFAULT 'GET',
  status_code INT,
  response_time_ms INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.api_usage ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own usage"
  ON public.api_usage FOR SELECT
  USING (auth.uid() = user_id);

CREATE INDEX idx_api_usage_user ON public.api_usage(user_id, created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- STORAGE BUCKETS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Bucket avatars (à créer manuellement dans Supabase Dashboard > Storage)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('avatars', 'avatars', true);

-- Bucket zama-assets (NFT assets)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('zama-assets', 'zama-assets', true);

-- ═══════════════════════════════════════════════════════════════════════════════
-- REALTIME — Activer les subscriptions
-- ═══════════════════════════════════════════════════════════════════════════════

-- Activer Realtime pour les tables critiques
ALTER PUBLICATION supabase_realtime ADD TABLE public.community_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.profiles;
ALTER PUBLICATION supabase_realtime ADD TABLE public.founders;
ALTER PUBLICATION supabase_realtime ADD TABLE public.private_threads;
ALTER PUBLICATION supabase_realtime ADD TABLE public.thread_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.founder_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.activity_feed;
