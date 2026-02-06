-- ═══════════════════════════════════════════════════════════════════════════════════════
--
--                           AT·OM TOKEN ECONOMY TABLES
--                    Phase 6: Progreso 2026 — Tokenomics Infrastructure
--
--   Tables:
--   1. token_contributions   — JT minting records (investor contributions)
--   2. nft_registry          — NFT minting records (5 tiers)
--   3. flow_keeper_ledger    — Flow Keeper contributions (community stimulus)
--   4. atom_transactions     — ATOM bonding curve transactions
--   5. ur_ledger             — UR mint/burn/transfer records
--   6. token_economy_state   — Snapshot of economy state
--
--   Author: AT·OM Collective
--   Date: 2026-02-05
--
-- ═══════════════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. TOKEN CONTRIBUTIONS (JT Minting)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.token_contributions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Contributor
  contributor_id UUID NOT NULL,
  waitlist_id UUID REFERENCES public.progreso_waitlist(id),

  -- Contribution details
  amount_usd NUMERIC(12, 2) NOT NULL CHECK (amount_usd > 0),
  jt_tier TEXT NOT NULL CHECK (jt_tier IN ('etincelle', 'flamme', 'feu', 'brasier', 'soleil')),
  jt_minted NUMERIC(14, 2) NOT NULL,
  jt_bonus_pct NUMERIC(5, 2) DEFAULT 0,

  -- NFT (if applicable)
  nft_tier TEXT CHECK (nft_tier IN ('graine', 'pousse', 'branche', 'racine', 'arbre')),
  nft_serial INTEGER,

  -- Flow Token
  flow_token_id TEXT,
  flow_type TEXT CHECK (flow_type IN ('tech', 'vie', 'sagesse', 'justice', 'graine', 'terre')),

  -- Fund allocation
  fund_development NUMERIC(12, 2),
  fund_stimulation NUMERIC(12, 2),
  fund_structure NUMERIC(12, 2),
  fund_emergency NUMERIC(12, 2),

  -- Hedera
  hedera_tx_id TEXT,
  hedera_token_id TEXT,

  -- Personal message
  message TEXT,

  -- Status
  status TEXT DEFAULT 'confirmed' CHECK (status IN ('pending', 'confirmed', 'converted', 'failed')),
  converted_at TIMESTAMPTZ,
  conversion_rate NUMERIC(4, 2),
  ur_received NUMERIC(14, 2),

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_contributions_contributor ON public.token_contributions(contributor_id);
CREATE INDEX IF NOT EXISTS idx_contributions_tier ON public.token_contributions(jt_tier);
CREATE INDEX IF NOT EXISTS idx_contributions_status ON public.token_contributions(status);
CREATE INDEX IF NOT EXISTS idx_contributions_created ON public.token_contributions(created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. NFT REGISTRY
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.nft_registry (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- NFT Identity
  tier TEXT NOT NULL CHECK (tier IN ('graine', 'pousse', 'branche', 'racine', 'arbre')),
  serial_number INTEGER NOT NULL,
  edition_label TEXT, -- e.g., "#042/144"

  -- Owner
  owner_id UUID NOT NULL,
  owner_name TEXT,

  -- Metadata
  name TEXT NOT NULL, -- "Graine de l'Arche #042"
  frequency_hz INTEGER,
  sphere_assigned INTEGER CHECK (sphere_assigned BETWEEN 1 AND 9),
  contribution_usd NUMERIC(12, 2),
  contribution_id UUID REFERENCES public.token_contributions(id),

  -- Hedera
  hedera_token_id TEXT, -- NFT collection ID
  hedera_serial TEXT,   -- Hedera serial number
  hedera_tx_id TEXT,
  metadata_ipfs TEXT,   -- IPFS hash for metadata

  -- Evolution
  current_stage INTEGER DEFAULT 1 CHECK (current_stage BETWEEN 1 AND 5),
  max_stage INTEGER DEFAULT 5,
  last_evolution_at TIMESTAMPTZ,

  -- Utilities
  utilities TEXT[], -- Array of utility strings

  -- Status
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'transferred', 'burned', 'evolved')),

  -- Timestamps
  minted_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Unique constraint: one serial per tier
  UNIQUE(tier, serial_number)
);

CREATE INDEX IF NOT EXISTS idx_nft_owner ON public.nft_registry(owner_id);
CREATE INDEX IF NOT EXISTS idx_nft_tier ON public.nft_registry(tier);
CREATE INDEX IF NOT EXISTS idx_nft_status ON public.nft_registry(status);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. FLOW KEEPER LEDGER
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.flow_keeper_ledger (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Token Identity
  token_id TEXT UNIQUE NOT NULL, -- FLOW-TECH-2026-0205-00001
  sequential_number INTEGER NOT NULL,

  -- Contributor
  contributor_id UUID NOT NULL,
  contributor_name TEXT,
  anonymous BOOLEAN DEFAULT false,

  -- Contribution
  amount_usd NUMERIC(12, 2) NOT NULL CHECK (amount_usd > 0),
  flow_type TEXT NOT NULL CHECK (flow_type IN ('tech', 'vie', 'sagesse', 'justice', 'graine', 'terre')),
  message TEXT,

  -- Hedera
  hedera_tx_id TEXT,
  hedera_topic_id TEXT,

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_flow_contributor ON public.flow_keeper_ledger(contributor_id);
CREATE INDEX IF NOT EXISTS idx_flow_type ON public.flow_keeper_ledger(flow_type);
CREATE INDEX IF NOT EXISTS idx_flow_created ON public.flow_keeper_ledger(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_flow_sequential ON public.flow_keeper_ledger(sequential_number DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. ATOM BONDING CURVE TRANSACTIONS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.atom_transactions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Transaction
  action TEXT NOT NULL CHECK (action IN ('buy', 'sell', 'genesis')),
  account_id UUID NOT NULL,

  -- Amounts
  amount_tokens NUMERIC(14, 6) NOT NULL,
  price_per_token NUMERIC(10, 6) NOT NULL,
  total_usd NUMERIC(14, 2) NOT NULL,
  reserve_change NUMERIC(14, 2),

  -- State after transaction
  new_supply NUMERIC(14, 6),
  new_price NUMERIC(10, 6),
  new_reserve NUMERIC(14, 2),

  -- Hedera
  hedera_tx_id TEXT,

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_atom_account ON public.atom_transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_atom_action ON public.atom_transactions(action);
CREATE INDEX IF NOT EXISTS idx_atom_created ON public.atom_transactions(created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. UR LEDGER
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.ur_ledger (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Transaction type
  action TEXT NOT NULL CHECK (action IN ('mint', 'burn', 'transfer', 'conversion', 'reward', 'fee')),

  -- Accounts
  from_account UUID,
  to_account UUID,

  -- Amount
  amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
  reason TEXT,

  -- Reference
  reference_type TEXT, -- 'jt_conversion', 'flow_reward', 'service_fee', etc.
  reference_id UUID,

  -- Hedera
  hedera_tx_id TEXT,

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ur_from ON public.ur_ledger(from_account);
CREATE INDEX IF NOT EXISTS idx_ur_to ON public.ur_ledger(to_account);
CREATE INDEX IF NOT EXISTS idx_ur_action ON public.ur_ledger(action);
CREATE INDEX IF NOT EXISTS idx_ur_created ON public.ur_ledger(created_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. ECONOMY STATE SNAPSHOTS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.token_economy_snapshots (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- UR State
  ur_total_supply NUMERIC(16, 2) DEFAULT 0,
  ur_circulating NUMERIC(16, 2) DEFAULT 0,
  ur_treasury NUMERIC(16, 2) DEFAULT 0,

  -- JT State
  jt_total_minted NUMERIC(16, 2) DEFAULT 0,
  jt_outstanding NUMERIC(16, 2) DEFAULT 0,
  jt_converted NUMERIC(16, 2) DEFAULT 0,

  -- ATOM State
  atom_supply NUMERIC(16, 6) DEFAULT 0,
  atom_price NUMERIC(10, 6) DEFAULT 0.01,
  atom_reserve NUMERIC(16, 2) DEFAULT 0,
  atom_market_cap NUMERIC(16, 2) DEFAULT 0,

  -- NFT Counts
  nft_graine_minted INTEGER DEFAULT 0,
  nft_pousse_minted INTEGER DEFAULT 0,
  nft_branche_minted INTEGER DEFAULT 0,
  nft_racine_minted INTEGER DEFAULT 0,
  nft_arbre_minted INTEGER DEFAULT 0,

  -- Fund Balances
  fund_development NUMERIC(14, 2) DEFAULT 0,
  fund_stimulation NUMERIC(14, 2) DEFAULT 0,
  fund_structure NUMERIC(14, 2) DEFAULT 0,
  fund_emergency NUMERIC(14, 2) DEFAULT 0,

  -- Flow Keeper
  flow_total NUMERIC(14, 2) DEFAULT 0,
  flow_token_count INTEGER DEFAULT 0,

  -- Aggregate
  total_raised_usd NUMERIC(16, 2) DEFAULT 0,
  total_contributors INTEGER DEFAULT 0,

  -- Timestamp
  snapshot_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_snapshot_at ON public.token_economy_snapshots(snapshot_at DESC);

-- ═══════════════════════════════════════════════════════════════════════════════
-- RLS POLICIES
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE public.token_contributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.nft_registry ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.flow_keeper_ledger ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.atom_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ur_ledger ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.token_economy_snapshots ENABLE ROW LEVEL SECURITY;

-- Public can view NFT registry and flow wall
CREATE POLICY "Public can view NFTs" ON public.nft_registry
FOR SELECT TO anon, authenticated USING (true);

CREATE POLICY "Public can view flow wall" ON public.flow_keeper_ledger
FOR SELECT TO anon, authenticated USING (true);

CREATE POLICY "Public can view economy snapshots" ON public.token_economy_snapshots
FOR SELECT TO anon, authenticated USING (true);

-- Authenticated users can view their own contributions
CREATE POLICY "Users view own contributions" ON public.token_contributions
FOR SELECT TO authenticated USING (contributor_id = auth.uid());

CREATE POLICY "Users view own ATOM txs" ON public.atom_transactions
FOR SELECT TO authenticated USING (account_id = auth.uid());

CREATE POLICY "Users view own UR txs" ON public.ur_ledger
FOR SELECT TO authenticated USING (from_account = auth.uid() OR to_account = auth.uid());

-- Service role can do everything
CREATE POLICY "Service role full access contributions" ON public.token_contributions
FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role full access nft" ON public.nft_registry
FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role full access flow" ON public.flow_keeper_ledger
FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role full access atom" ON public.atom_transactions
FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role full access ur" ON public.ur_ledger
FOR ALL TO service_role USING (true) WITH CHECK (true);

CREATE POLICY "Service role full access snapshots" ON public.token_economy_snapshots
FOR ALL TO service_role USING (true) WITH CHECK (true);

-- ═══════════════════════════════════════════════════════════════════════════════
-- VIEWS
-- ═══════════════════════════════════════════════════════════════════════════════

-- NFT Supply Dashboard
CREATE OR REPLACE VIEW public.nft_supply_dashboard AS
SELECT
  tier,
  COUNT(*) as minted,
  CASE tier
    WHEN 'graine' THEN NULL  -- unlimited
    WHEN 'pousse' THEN 1000
    WHEN 'branche' THEN 144
    WHEN 'racine' THEN 36
    WHEN 'arbre' THEN 9
  END as max_supply,
  MIN(minted_at) as first_mint,
  MAX(minted_at) as last_mint
FROM public.nft_registry
WHERE status = 'active'
GROUP BY tier;

-- Flow Keeper Dashboard
CREATE OR REPLACE VIEW public.flow_keeper_dashboard AS
SELECT
  flow_type,
  COUNT(*) as contributions,
  SUM(amount_usd) as total_usd,
  AVG(amount_usd) as avg_contribution,
  MIN(created_at) as first_flow,
  MAX(created_at) as last_flow
FROM public.flow_keeper_ledger
GROUP BY flow_type;

-- Momentum Tracker
CREATE OR REPLACE VIEW public.momentum_tracker AS
SELECT
  COUNT(*) as total_contributions,
  COUNT(DISTINCT contributor_id) as unique_contributors,
  SUM(amount_usd) as total_raised,
  SUM(jt_minted) as total_jt_minted,
  SUM(CASE WHEN nft_tier IS NOT NULL THEN 1 ELSE 0 END) as nfts_minted,
  MIN(created_at) as first_contribution,
  MAX(created_at) as last_contribution,
  ROUND(SUM(amount_usd) / 100000 * 100, 1) as progress_pct
FROM public.token_contributions
WHERE status IN ('confirmed', 'converted');

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGERS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Auto-update updated_at on contributions
CREATE OR REPLACE FUNCTION update_token_contributions_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_contributions_updated_at
  BEFORE UPDATE ON public.token_contributions
  FOR EACH ROW
  EXECUTE FUNCTION update_token_contributions_updated_at();

-- Auto-update updated_at on NFTs
CREATE OR REPLACE FUNCTION update_nft_registry_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_nft_registry_updated_at
  BEFORE UPDATE ON public.nft_registry
  FOR EACH ROW
  EXECUTE FUNCTION update_nft_registry_updated_at();

-- ═══════════════════════════════════════════════════════════════════════════════
-- END OF MIGRATION
-- AT·OM : 444 Hz : Souveraineté Économique : 4 Instruments en Parallèle
-- ═══════════════════════════════════════════════════════════════════════════════
