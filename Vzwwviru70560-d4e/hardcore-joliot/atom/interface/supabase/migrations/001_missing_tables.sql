-- ═══════════════════════════════════════════════════════════════════════════
-- AT·OM — Migration: Tables manquantes pour intégration complète
-- À exécuter dans Supabase > SQL Editor
-- ═══════════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. WAITLIST — Inscriptions pré-signup
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS waitlist (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT,
  role TEXT DEFAULT 'citoyen' CHECK (role IN ('citoyen', 'collaborateur', 'investisseur')),
  interests TEXT[] DEFAULT '{}',
  referral_source TEXT,
  utm_source TEXT,
  utm_campaign TEXT,
  consent_given BOOLEAN DEFAULT false,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'invited', 'converted', 'unsubscribed')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  converted_at TIMESTAMPTZ
);

-- Index pour recherche rapide par email
CREATE INDEX IF NOT EXISTS idx_waitlist_email ON waitlist(email);
CREATE INDEX IF NOT EXISTS idx_waitlist_status ON waitlist(status);

-- RLS: lecture publique pour vérifier si email existe, insertion publique
ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can join waitlist" ON waitlist
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Check own email" ON waitlist
  FOR SELECT USING (true);

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. ANALYTICS_EVENTS — Tracking funnel utilisateur
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS analytics_events (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id TEXT NOT NULL,
  user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
  event_name TEXT NOT NULL,
  event_category TEXT DEFAULT 'general',
  properties JSONB DEFAULT '{}',
  page TEXT,
  referrer TEXT,
  user_agent TEXT,
  device_type TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour requêtes analytics
CREATE INDEX IF NOT EXISTS idx_analytics_session ON analytics_events(session_id);
CREATE INDEX IF NOT EXISTS idx_analytics_event ON analytics_events(event_name);
CREATE INDEX IF NOT EXISTS idx_analytics_created ON analytics_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_user ON analytics_events(user_id);

-- RLS: insertion publique (anon), lecture admin seulement
ALTER TABLE analytics_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can track events" ON analytics_events
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can read own events" ON analytics_events
  FOR SELECT USING (auth.uid() = user_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. USER_ACTIONS — Actions d'activation complétées
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_actions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  action_id TEXT NOT NULL,
  action_category TEXT DEFAULT 'activation',
  metadata JSONB DEFAULT '{}',
  completed_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, action_id)
);

CREATE INDEX IF NOT EXISTS idx_user_actions_user ON user_actions(user_id);

ALTER TABLE user_actions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users manage own actions" ON user_actions
  FOR ALL USING (auth.uid() = user_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- 4. USER_MISSIONS — Missions et objectifs utilisateur
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_missions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  mission_id TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'abandoned')),
  completed_steps TEXT[] DEFAULT '{}',
  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_missions_user ON user_missions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_missions_status ON user_missions(status);

ALTER TABLE user_missions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users manage own missions" ON user_missions
  FOR ALL USING (auth.uid() = user_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- 5. AB_TEST_ASSIGNMENTS — Assignation de variantes A/B
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ab_test_assignments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  session_id TEXT,
  experiment_id TEXT NOT NULL,
  variant_id TEXT NOT NULL,
  converted BOOLEAN DEFAULT false,
  conversion_event TEXT,
  assigned_at TIMESTAMPTZ DEFAULT NOW(),
  converted_at TIMESTAMPTZ,
  UNIQUE(user_id, experiment_id)
);

CREATE INDEX IF NOT EXISTS idx_ab_experiment ON ab_test_assignments(experiment_id);
CREATE INDEX IF NOT EXISTS idx_ab_user ON ab_test_assignments(user_id);

ALTER TABLE ab_test_assignments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can be assigned" ON ab_test_assignments
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Users read own assignments" ON ab_test_assignments
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users update own assignments" ON ab_test_assignments
  FOR UPDATE USING (auth.uid() = user_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- 6. USER_PREFERENCES — Préférences UI synchronisées
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_preferences (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL UNIQUE REFERENCES profiles(id) ON DELETE CASCADE,
  theme TEXT DEFAULT 'dark' CHECK (theme IN ('light', 'dark', 'system')),
  language TEXT DEFAULT 'symbolique' CHECK (language IN ('symbolique', 'clair')),
  experience_mode TEXT DEFAULT 'debutant' CHECK (experience_mode IN ('debutant', 'expert')),
  sidebar_open BOOLEAN DEFAULT true,
  active_spheres TEXT[] DEFAULT '{}',
  notification_enabled BOOLEAN DEFAULT true,
  reduced_motion BOOLEAN DEFAULT false,
  extra JSONB DEFAULT '{}',
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users manage own preferences" ON user_preferences
  FOR ALL USING (auth.uid() = user_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- 7. SESSIONS — Tracking de sessions utilisateur
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sessions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  session_id TEXT NOT NULL UNIQUE,
  user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  last_activity TIMESTAMPTZ DEFAULT NOW(),
  landing_page TEXT,
  referrer TEXT,
  user_agent TEXT,
  device_type TEXT,
  is_new_user BOOLEAN DEFAULT true,
  events_count INTEGER DEFAULT 0,
  duration_ms INTEGER DEFAULT 0,
  ended_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_started ON sessions(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON sessions(session_id);

ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can create session" ON sessions
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Users read own sessions" ON sessions
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Anyone can update session" ON sessions
  FOR UPDATE WITH CHECK (true);

-- ═══════════════════════════════════════════════════════════════════════════
-- FONCTIONS UTILITAIRES
-- ═══════════════════════════════════════════════════════════════════════════

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers pour updated_at automatique
CREATE TRIGGER trg_user_missions_updated
  BEFORE UPDATE ON user_missions
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_user_preferences_updated
  BEFORE UPDATE ON user_preferences
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ═══════════════════════════════════════════════════════════════════════════
-- VUES ANALYTICS (pour le dashboard admin)
-- ═══════════════════════════════════════════════════════════════════════════

-- Vue: Funnel de conversion
CREATE OR REPLACE VIEW funnel_summary AS
SELECT
  event_name,
  COUNT(*) as total_events,
  COUNT(DISTINCT session_id) as unique_sessions,
  COUNT(DISTINCT user_id) as unique_users,
  DATE_TRUNC('day', created_at) as event_date
FROM analytics_events
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY event_name, DATE_TRUNC('day', created_at)
ORDER BY event_date DESC, total_events DESC;

-- Vue: Waitlist stats
CREATE OR REPLACE VIEW waitlist_stats AS
SELECT
  status,
  role,
  COUNT(*) as count,
  MIN(created_at) as first_signup,
  MAX(created_at) as last_signup
FROM waitlist
GROUP BY status, role;

-- Vue: Activation progress
CREATE OR REPLACE VIEW activation_summary AS
SELECT
  ua.action_id,
  ua.action_category,
  COUNT(*) as completions,
  COUNT(DISTINCT ua.user_id) as unique_users
FROM user_actions ua
GROUP BY ua.action_id, ua.action_category
ORDER BY completions DESC;

-- ═══════════════════════════════════════════════════════════════════════════
-- FIN DE LA MIGRATION
-- ═══════════════════════════════════════════════════════════════════════════
-- Total: 7 nouvelles tables + 1 fonction + 3 vues
-- Résultat final: 28 tables au total
