-- ═══════════════════════════════════════════════════════════════════════════════════════
--
--                           PROGRESO WAITLIST TABLE
--                      AT-OM : Phase I - Festival Progreso 2026
--
--   This table captures pre-registrations from the Progreso festival landing page
--   Three types: Citizen (waitlist), Founder (talents), Investor (support)
--
-- ═══════════════════════════════════════════════════════════════════════════════════════

-- Table: progreso_waitlist
-- Captures all pre-registrations from the festival landing page
CREATE TABLE IF NOT EXISTS public.progreso_waitlist (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Basic Info (all types)
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  phone TEXT,
  type TEXT NOT NULL CHECK (type IN ('citizen', 'founder', 'investor')),

  -- Founder-specific fields
  skills TEXT,                    -- What skills they bring
  motivation TEXT,                -- Why they want to join / How they want to contribute
  portfolio_url TEXT,             -- Link to their work
  facette_resonance TEXT,         -- Which facet resonates with them
  availability TEXT,              -- Hours per week available

  -- Investor-specific fields
  support_type TEXT,              -- Type of support (donation, investment, sponsorship)
  investment_range TEXT,          -- Budget range

  -- Tracking
  source TEXT DEFAULT 'progreso_2026',
  referral_code TEXT,             -- If referred by someone
  language TEXT DEFAULT 'fr',     -- Preferred language

  -- Engagement
  engagement_cooperation BOOLEAN DEFAULT false,  -- Agreed to cooperation principles
  newsletter_optin BOOLEAN DEFAULT true,

  -- Status
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'contacted', 'approved', 'rejected', 'converted')),
  notes TEXT,                     -- Admin notes

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  contacted_at TIMESTAMPTZ,
  converted_at TIMESTAMPTZ
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_progreso_waitlist_email ON public.progreso_waitlist(email);
CREATE INDEX IF NOT EXISTS idx_progreso_waitlist_type ON public.progreso_waitlist(type);
CREATE INDEX IF NOT EXISTS idx_progreso_waitlist_status ON public.progreso_waitlist(status);
CREATE INDEX IF NOT EXISTS idx_progreso_waitlist_created ON public.progreso_waitlist(created_at DESC);

-- Enable RLS
ALTER TABLE public.progreso_waitlist ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can insert (public signup)
CREATE POLICY "Allow public insert" ON public.progreso_waitlist
FOR INSERT TO anon, authenticated WITH CHECK (true);

-- Policy: Authenticated users can view their own entry
CREATE POLICY "Users can view own entry" ON public.progreso_waitlist
FOR SELECT TO authenticated USING (email = auth.email());

-- Policy: Service role can do everything (for admin dashboard)
CREATE POLICY "Service role full access" ON public.progreso_waitlist
FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Trigger: Auto-update updated_at
CREATE OR REPLACE FUNCTION update_progreso_waitlist_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_progreso_waitlist_updated_at
  BEFORE UPDATE ON public.progreso_waitlist
  FOR EACH ROW
  EXECUTE FUNCTION update_progreso_waitlist_updated_at();

-- ═══════════════════════════════════════════════════════════════════════════════════════
-- WAITLIST STATS VIEW
-- For dashboard analytics
-- ═══════════════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE VIEW public.progreso_waitlist_stats AS
SELECT
  type,
  status,
  COUNT(*) as count,
  MIN(created_at) as first_signup,
  MAX(created_at) as last_signup
FROM public.progreso_waitlist
GROUP BY type, status;

-- ═══════════════════════════════════════════════════════════════════════════════════════
-- SAMPLE DATA COMMENT (for testing)
-- ═══════════════════════════════════════════════════════════════════════════════════════

/*
-- Test insert for citizen
INSERT INTO public.progreso_waitlist (name, email, type, source)
VALUES ('Test Citizen', 'test.citizen@example.com', 'citizen', 'progreso_2026');

-- Test insert for founder
INSERT INTO public.progreso_waitlist (
  name, email, type, skills, motivation, facette_resonance, source
)
VALUES (
  'Test Founder',
  'test.founder@example.com',
  'founder',
  'Development, AI, Architecture',
  'I want to build systems that serve humanity',
  'Technologique',
  'progreso_2026'
);

-- Test insert for investor
INSERT INTO public.progreso_waitlist (
  name, email, type, support_type, motivation, source
)
VALUES (
  'Test Investor',
  'test.investor@example.com',
  'investor',
  'Investment fondateur',
  'I believe in the vision and want to support the infrastructure',
  'progreso_2026'
);
*/

-- ═══════════════════════════════════════════════════════════════════════════════════════
-- END OF MIGRATION
-- AT-OM : 444 Hz : Souveraineté
-- ═══════════════════════════════════════════════════════════════════════════════════════
