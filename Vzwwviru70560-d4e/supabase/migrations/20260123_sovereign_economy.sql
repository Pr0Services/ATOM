-- ═══════════════════════════════════════════════════════════════════════════════
--
--       ███████╗ ██████╗ ██████╗ ███╗   ██╗ ██████╗ ███╗   ███╗██╗███████╗
--       ██╔════╝██╔════╝██╔═══██╗████╗  ██║██╔═══██╗████╗ ████║██║██╔════╝
--       █████╗  ██║     ██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║██║█████╗
--       ██╔══╝  ██║     ██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║██╔══╝
--       ███████╗╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║███████╗
--       ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚══════╝
--
--              SYSTÈME ÉCONOMIQUE SOUVERAIN - AT·OM / CHE·NU V76
--                    Unité de Résonance (UR) sur Hedera HTS
--
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- Ce script crée l'infrastructure PostgreSQL pour:
-- 1. Le Volant Énergétique (variables de pilotage)
-- 2. Les soldes et transactions en UR
-- 3. Le système de ristournes
-- 4. Le pont de liquidité (UR ↔ Fiat)
-- 5. La gouvernance décentralisée
--
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. TABLE DES PARAMÈTRES DU VOLANT ÉNERGÉTIQUE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS economic_settings (
  key TEXT PRIMARY KEY,
  value JSONB NOT NULL,
  category TEXT NOT NULL CHECK (category IN (
    'allocation',      -- Distribution des abonnements
    'rebates',         -- Ristournes et redistribution
    'tokens',          -- Allocation de puissance IA
    'expansion',       -- Fond d'expansion CHE·NU
    'referral',        -- Parrainage
    'stability',       -- Stabilisation Hedera
    'research',        -- R&D et science
    'marketplace',     -- Marché de l'utilité
    'lending',         -- Prêts P2P
    'monetary',        -- Politique monétaire
    'security',        -- Sécurité et anonymat
    'governance'       -- Gouvernance
  )),
  description TEXT,
  min_value NUMERIC,
  max_value NUMERIC,
  requires_vote BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_by UUID REFERENCES auth.users(id)
);

-- Insertion des valeurs par défaut du Volant Énergétique
INSERT INTO economic_settings (key, value, category, description, min_value, max_value, requires_vote) VALUES
-- ALLOCATION DES ABONNEMENTS
('infrastructure_allocation_pct', '40', 'allocation', 'Part pour API/serveurs', 0, 100, false),
('liquidity_reserve_pct', '30', 'allocation', 'Part pour garantie monétaire', 0, 100, false),
('development_fund_pct', '20', 'allocation', 'Part pour expansion CHE·NU', 0, 100, false),
('community_rewards_pct', '10', 'allocation', 'Part pour ristournes', 0, 100, false),

-- RISTOURNES
('resonance_rebate_pct', '5', 'rebates', 'Pourcentage de ristourne sur surplus', 0, 25, false),
('activity_threshold_score', '50', 'rebates', 'Score minimum pour éligibilité', 0, 100, false),
('distribution_frequency', '"monthly"', 'rebates', 'Fréquence de distribution', NULL, NULL, false),
('surplus_trigger_threshold', '1000', 'rebates', 'Surplus minimum pour déclencher', 0, NULL, false),
('reinvestment_bonus_pct', '10', 'rebates', 'Bonus pour réinvestissement', 0, 50, false),

-- TOKENS IA
('base_token_quota_citoyen', '50000', 'tokens', 'Quota mensuel Citoyen', 0, NULL, false),
('base_token_quota_fondateur', '500000', 'tokens', 'Quota mensuel Fondateur', 0, NULL, false),
('base_token_quota_souverain', '-1', 'tokens', 'Quota mensuel Souverain (-1=illimité)', -1, NULL, false),
('priority_burst_multiplier', '1.5', 'tokens', 'Multiplicateur de priorité', 1.0, 5.0, false),
('emergency_reserve_pct', '10', 'tokens', 'Réserve pour urgences', 0, 50, false),

-- EXPANSION CHE·NU
('expansion_tax_rate', '2', 'expansion', 'Part des transactions vers le fond', 0, 10, true),
('project_vote_weight_threshold', '67', 'expansion', 'Votes nécessaires pour débloquer', 50, 100, true),
('minimum_project_value', '5000', 'expansion', 'Valeur minimale d''un projet', 0, NULL, false),
('max_single_allocation_pct', '30', 'expansion', 'Maximum pour un seul projet', 0, 100, true),

-- PARRAINAGE
('referral_bonus_fixed_ur', '100', 'referral', 'Bonus fixe en UR au parrain', 0, NULL, false),
('referral_bonus_fixed_filleul', '50', 'referral', 'Bonus fixe au nouveau membre', 0, NULL, false),
('long_term_royalty_pct', '5', 'referral', 'Part des frais du filleul', 0, 20, false),
('royalty_duration_months', '12', 'referral', 'Durée de la royauté', 0, 60, false),
('max_referral_depth', '2', 'referral', 'Profondeur du réseau', 1, 5, false),

-- STABILISATION
('target_reserve_ratio', '100', 'stability', 'Ratio cible de couverture (%)', 50, 200, true),
('conversion_fee_ur_to_fiat', '2', 'stability', 'Frais de sortie vers fiat (%)', 0, 10, false),
('conversion_fee_fiat_to_ur', '0.5', 'stability', 'Frais d''entrée depuis fiat (%)', 0, 5, false),
('daily_conversion_limit_pct', '10', 'stability', 'Limite de conversion/jour (%)', 0, 100, false),
('emergency_lock_threshold', '30', 'stability', 'Seuil de verrouillage d''urgence (%)', 10, 50, true),

-- R&D
('research_grant_base_ur', '500', 'research', 'Subvention de base', 0, NULL, false),
('impact_multiplier_factor', '2.0', 'research', 'Multiplicateur selon l''impact', 1.0, 10.0, false),
('peer_review_bonus_pct', '25', 'research', 'Bonus si validé par pairs (%)', 0, 100, false),
('publication_requirement', 'true', 'research', 'Publication requise', NULL, NULL, false),

-- MARKETPLACE
('marketplace_fee_pct', '3', 'marketplace', 'Commission de la plateforme (%)', 0, 15, false),
('minimum_transaction_ur', '1', 'marketplace', 'Transaction minimum', 0, NULL, false),
('escrow_duration_days', '7', 'marketplace', 'Durée du séquestre', 1, 30, false),
('dispute_resolution_fee_pct', '5', 'marketplace', 'Frais de médiation (%)', 0, 20, false),

-- PRÊTS P2P
('max_loan_to_resonance_ratio', '200', 'lending', 'Ratio prêt/score maximum (%)', 0, 500, false),
('default_interest_rate_annual', '5', 'lending', 'Taux d''intérêt suggéré (%)', 0, 20, false),
('collateral_requirement_pct', '50', 'lending', 'Collatéral requis (%)', 0, 150, false),
('grace_period_days', '30', 'lending', 'Période de grâce', 0, 90, false),
('platform_guarantee_pct', '10', 'lending', 'Garantie plateforme (%)', 0, 50, true),

-- POLITIQUE MONÉTAIRE
('target_velocity', '5.0', 'monetary', 'Vélocité cible de la monnaie', 1.0, 20.0, true),
('inflation_adjustment_rate', '1', 'monetary', 'Taux d''ajustement si inflation (%)', 0, 10, false),
('deflation_adjustment_rate', '1', 'monetary', 'Taux d''ajustement si déflation (%)', 0, 10, false),
('measurement_period_days', '30', 'monetary', 'Période de mesure', 7, 90, false),
('burn_rate_on_transactions', '0.1', 'monetary', 'Taux de destruction/transaction (%)', 0, 5, false),
('ur_initial_rate_cad', '1.0', 'monetary', 'Taux initial 1 UR = X CAD', 0.01, 100, true),

-- SÉCURITÉ
('anonymity_layer_depth', '3', 'security', 'Niveau de cryptage', 1, 5, false),
('transaction_mixing_enabled', 'true', 'security', 'Mélange des transactions', NULL, NULL, false),
('kyc_threshold_ur', '10000', 'security', 'Seuil KYC obligatoire', 0, NULL, true),
('geographic_distribution_min', '3', 'security', 'Nœuds géographiques min', 1, 10, false),

-- GOUVERNANCE
('proposal_minimum_ur_stake', '100', 'governance', 'Mise minimale pour proposer', 0, NULL, false),
('voting_period_days', '7', 'governance', 'Durée du vote', 1, 30, false),
('quorum_pct', '33', 'governance', 'Participation minimale (%)', 0, 100, true),
('approval_threshold_pct', '67', 'governance', 'Seuil d''approbation (%)', 50, 100, true),
('vote_weight_by_resonance', 'true', 'governance', 'Poids selon le score', NULL, NULL, true)

ON CONFLICT (key) DO UPDATE SET
  value = EXCLUDED.value,
  updated_at = NOW();

-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. TABLE DES SOLDES EN UNITÉS DE RÉSONANCE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS member_balances (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Soldes UR
  ur_balance NUMERIC(20, 8) DEFAULT 0 CHECK (ur_balance >= 0),
  ur_locked NUMERIC(20, 8) DEFAULT 0 CHECK (ur_locked >= 0),
  ur_pending NUMERIC(20, 8) DEFAULT 0,

  -- Hedera
  hedera_account_id TEXT,
  hedera_public_key TEXT,

  -- Métriques de participation
  resonance_score NUMERIC(5, 2) DEFAULT 0,
  activity_score NUMERIC(5, 2) DEFAULT 0,
  contribution_score NUMERIC(5, 2) DEFAULT 0,
  tenure_months INTEGER DEFAULT 0,

  -- Totaux historiques
  total_ur_earned NUMERIC(20, 8) DEFAULT 0,
  total_ur_spent NUMERIC(20, 8) DEFAULT 0,
  total_rebates_received NUMERIC(20, 8) DEFAULT 0,
  total_referral_rewards NUMERIC(20, 8) DEFAULT 0,

  -- Statut
  is_frozen BOOLEAN DEFAULT false,
  freeze_reason TEXT,

  -- Timestamps
  last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. TABLE DES TRANSACTIONS UR
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS ur_transactions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Participants
  from_user_id UUID REFERENCES auth.users(id),
  to_user_id UUID REFERENCES auth.users(id),

  -- Montants
  amount NUMERIC(20, 8) NOT NULL CHECK (amount > 0),
  fee NUMERIC(20, 8) DEFAULT 0 CHECK (fee >= 0),
  burn_amount NUMERIC(20, 8) DEFAULT 0 CHECK (burn_amount >= 0),
  net_amount NUMERIC(20, 8) GENERATED ALWAYS AS (amount - fee - burn_amount) STORED,

  -- Type de transaction
  tx_type TEXT NOT NULL CHECK (tx_type IN (
    'mint',           -- Création de nouveaux UR
    'burn',           -- Destruction de UR
    'transfer',       -- Transfert entre membres
    'subscription',   -- Conversion abonnement → UR
    'rebate',         -- Distribution de ristourne
    'referral',       -- Bonus de parrainage
    'grant',          -- Subvention R&D
    'marketplace',    -- Achat sur le marché
    'loan_disbursement', -- Versement de prêt
    'loan_repayment', -- Remboursement de prêt
    'conversion_out', -- UR → Fiat
    'conversion_in',  -- Fiat → UR
    'stake',          -- Verrouillage pour gouvernance
    'unstake',        -- Libération
    'expansion_contribution' -- Contribution au fond
  )),

  -- Référence externe
  hedera_tx_id TEXT,
  stripe_payment_id TEXT,
  reference_id UUID,
  reference_type TEXT,

  -- Métadonnées
  description TEXT,
  metadata JSONB DEFAULT '{}',

  -- Statut
  status TEXT DEFAULT 'pending' CHECK (status IN (
    'pending', 'processing', 'completed', 'failed', 'cancelled'
  )),
  error_message TEXT,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  processed_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. TABLE DES RISTOURNES
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS rebate_distributions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Bénéficiaire
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

  -- Type de ristourne
  rebate_type TEXT NOT NULL CHECK (rebate_type IN (
    'resonance_dividend',      -- Dividende de résonance
    'reinvestment_bonus',      -- Bonus de réinvestissement
    'referral_bonus',          -- Bonus de parrainage
    'referral_royalty',        -- Royalties de parrainage
    'contribution_reward',     -- Récompense de contribution
    'infrastructure_savings',  -- Économies d'infrastructure
    'special_grant'            -- Subvention spéciale
  )),

  -- Montant
  amount_ur NUMERIC(20, 8) NOT NULL CHECK (amount_ur > 0),

  -- Calculs
  calculation_details JSONB DEFAULT '{}',

  -- Période concernée
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,

  -- Transaction liée
  transaction_id UUID REFERENCES ur_transactions(id),

  -- Statut
  status TEXT DEFAULT 'calculated' CHECK (status IN (
    'calculated', 'approved', 'distributed', 'cancelled'
  )),

  -- Timestamps
  calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  approved_at TIMESTAMP WITH TIME ZONE,
  distributed_at TIMESTAMP WITH TIME ZONE
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. TABLE DE LA RÉSERVE DE LIQUIDITÉ
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS liquidity_pool (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Soldes
  fiat_balance_cad NUMERIC(15, 2) DEFAULT 0 CHECK (fiat_balance_cad >= 0),
  fiat_balance_usd NUMERIC(15, 2) DEFAULT 0 CHECK (fiat_balance_usd >= 0),
  ur_total_supply NUMERIC(20, 8) DEFAULT 0,
  ur_in_circulation NUMERIC(20, 8) DEFAULT 0,

  -- Métriques
  reserve_ratio NUMERIC(8, 4) DEFAULT 1.0,
  current_ur_rate_cad NUMERIC(10, 6) DEFAULT 1.0,
  current_ur_rate_usd NUMERIC(10, 6) DEFAULT 0.75,

  -- Vélocité (calculée quotidiennement)
  velocity_30d NUMERIC(8, 4) DEFAULT 0,
  transaction_volume_30d NUMERIC(20, 8) DEFAULT 0,

  -- Statut
  is_emergency_mode BOOLEAN DEFAULT false,
  emergency_activated_at TIMESTAMP WITH TIME ZONE,
  emergency_reason TEXT,

  -- Timestamps
  last_rebalance_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Initialiser avec une seule ligne (singleton)
INSERT INTO liquidity_pool (id)
VALUES (gen_random_uuid())
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. TABLE DES CONVERSIONS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS conversion_requests (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Utilisateur
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

  -- Direction
  direction TEXT NOT NULL CHECK (direction IN ('ur_to_fiat', 'fiat_to_ur')),

  -- Montants
  source_amount NUMERIC(20, 8) NOT NULL,
  source_currency TEXT NOT NULL, -- 'UR', 'CAD', 'USD'
  target_amount NUMERIC(20, 8),
  target_currency TEXT NOT NULL,
  exchange_rate NUMERIC(10, 6),
  fee_amount NUMERIC(20, 8) DEFAULT 0,

  -- Méthode de paiement (pour ur_to_fiat)
  payout_method TEXT CHECK (payout_method IN (
    'virtual_card', 'bank_transfer', 'interac', 'crypto_bridge'
  )),
  payout_details JSONB DEFAULT '{}',

  -- Stripe (pour fiat_to_ur)
  stripe_payment_intent_id TEXT,
  stripe_payout_id TEXT,

  -- Priorité (pour file d'attente en cas de crise)
  priority INTEGER DEFAULT 5, -- 1 = urgent, 10 = normal
  priority_reason TEXT,

  -- Statut
  status TEXT DEFAULT 'pending' CHECK (status IN (
    'pending', 'queued', 'processing', 'completed', 'failed', 'cancelled'
  )),
  error_message TEXT,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  processed_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. TABLE DES PROPOSITIONS DE GOUVERNANCE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS governance_proposals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Auteur
  proposer_id UUID REFERENCES auth.users(id) NOT NULL,

  -- Contenu
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  proposal_type TEXT NOT NULL CHECK (proposal_type IN (
    'parameter_change',    -- Changement de paramètre du Volant
    'expansion_project',   -- Projet d'expansion
    'constitutional',      -- Changement fondamental
    'emergency',           -- Mesure d'urgence
    'grant_approval'       -- Approbation de subvention
  )),

  -- Changements proposés
  proposed_changes JSONB NOT NULL,

  -- Stake
  stake_amount NUMERIC(20, 8) NOT NULL,
  stake_transaction_id UUID REFERENCES ur_transactions(id),

  -- Votes
  votes_for_weighted NUMERIC(20, 8) DEFAULT 0,
  votes_against_weighted NUMERIC(20, 8) DEFAULT 0,
  votes_abstain_weighted NUMERIC(20, 8) DEFAULT 0,
  total_voters INTEGER DEFAULT 0,

  -- Statut
  status TEXT DEFAULT 'draft' CHECK (status IN (
    'draft', 'discussion', 'voting', 'passed', 'rejected', 'executed', 'cancelled'
  )),

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  discussion_ends_at TIMESTAMP WITH TIME ZONE,
  voting_starts_at TIMESTAMP WITH TIME ZONE,
  voting_ends_at TIMESTAMP WITH TIME ZONE,
  executed_at TIMESTAMP WITH TIME ZONE
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 8. TABLE DES VOTES
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS governance_votes (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  proposal_id UUID REFERENCES governance_proposals(id) ON DELETE CASCADE NOT NULL,
  voter_id UUID REFERENCES auth.users(id) NOT NULL,

  vote TEXT NOT NULL CHECK (vote IN ('for', 'against', 'abstain')),
  vote_weight NUMERIC(20, 8) NOT NULL, -- Basé sur resonance_score

  comment TEXT,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  UNIQUE(proposal_id, voter_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 9. TABLE DU RÉSEAU DE PARRAINAGE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS referral_network (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Relation
  referrer_id UUID REFERENCES auth.users(id) NOT NULL,
  referred_id UUID REFERENCES auth.users(id) NOT NULL,
  depth INTEGER DEFAULT 1, -- Niveau dans l'arbre (1 = direct)

  -- Bonus versés
  initial_bonus_ur NUMERIC(20, 8) DEFAULT 0,
  initial_bonus_paid BOOLEAN DEFAULT false,
  initial_bonus_tx_id UUID REFERENCES ur_transactions(id),

  -- Royalties
  royalty_start_date DATE,
  royalty_end_date DATE,
  total_royalties_paid NUMERIC(20, 8) DEFAULT 0,

  -- Statut
  is_active BOOLEAN DEFAULT true,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  UNIQUE(referrer_id, referred_id)
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 10. TABLE DU MARCHÉ DE L'UTILITÉ
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS marketplace_listings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Vendeur
  seller_id UUID REFERENCES auth.users(id) NOT NULL,

  -- Offre
  title TEXT NOT NULL,
  description TEXT,
  category TEXT CHECK (category IN (
    'computing',    -- Puissance de calcul
    'design',       -- Services créatifs
    'development',  -- Développement
    'consulting',   -- Conseil
    'education',    -- Formation
    'other'
  )),

  -- Prix
  price_ur NUMERIC(20, 8) NOT NULL CHECK (price_ur > 0),
  price_type TEXT DEFAULT 'fixed' CHECK (price_type IN ('fixed', 'hourly', 'negotiable')),

  -- Disponibilité
  is_available BOOLEAN DEFAULT true,
  quantity_available INTEGER DEFAULT 1,

  -- Métriques
  total_sales INTEGER DEFAULT 0,
  average_rating NUMERIC(3, 2),

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 11. TABLE DES COMMANDES MARKETPLACE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS marketplace_orders (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  listing_id UUID REFERENCES marketplace_listings(id) NOT NULL,
  buyer_id UUID REFERENCES auth.users(id) NOT NULL,
  seller_id UUID REFERENCES auth.users(id) NOT NULL,

  -- Montants
  amount_ur NUMERIC(20, 8) NOT NULL,
  platform_fee_ur NUMERIC(20, 8) NOT NULL,
  seller_receives_ur NUMERIC(20, 8) NOT NULL,

  -- Escrow
  escrow_tx_id UUID REFERENCES ur_transactions(id),
  escrow_released BOOLEAN DEFAULT false,

  -- Statut
  status TEXT DEFAULT 'pending' CHECK (status IN (
    'pending', 'paid', 'in_progress', 'delivered', 'completed', 'disputed', 'refunded', 'cancelled'
  )),

  -- Évaluations
  buyer_rating INTEGER CHECK (buyer_rating BETWEEN 1 AND 5),
  buyer_review TEXT,
  seller_rating INTEGER CHECK (seller_rating BETWEEN 1 AND 5),
  seller_review TEXT,

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  paid_at TIMESTAMP WITH TIME ZONE,
  delivered_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 12. TABLE DES PRÊTS P2P
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS peer_loans (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Participants
  lender_id UUID REFERENCES auth.users(id) NOT NULL,
  borrower_id UUID REFERENCES auth.users(id) NOT NULL,

  -- Montants
  principal_ur NUMERIC(20, 8) NOT NULL CHECK (principal_ur > 0),
  interest_rate_annual NUMERIC(5, 2) NOT NULL,
  collateral_ur NUMERIC(20, 8) DEFAULT 0,

  -- Termes
  term_months INTEGER NOT NULL,
  grace_period_days INTEGER DEFAULT 30,

  -- Calculs
  total_interest_ur NUMERIC(20, 8),
  monthly_payment_ur NUMERIC(20, 8),
  total_repaid_ur NUMERIC(20, 8) DEFAULT 0,
  remaining_balance_ur NUMERIC(20, 8),

  -- Transactions liées
  disbursement_tx_id UUID REFERENCES ur_transactions(id),
  collateral_tx_id UUID REFERENCES ur_transactions(id),

  -- Statut
  status TEXT DEFAULT 'pending' CHECK (status IN (
    'pending', 'approved', 'active', 'completed', 'defaulted', 'cancelled'
  )),

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  approved_at TIMESTAMP WITH TIME ZONE,
  disbursed_at TIMESTAMP WITH TIME ZONE,
  first_payment_due DATE,
  completed_at TIMESTAMP WITH TIME ZONE
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 13. TABLE DES PAIEMENTS DE PRÊT
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS loan_payments (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  loan_id UUID REFERENCES peer_loans(id) NOT NULL,

  -- Montants
  amount_ur NUMERIC(20, 8) NOT NULL,
  principal_portion NUMERIC(20, 8),
  interest_portion NUMERIC(20, 8),

  -- Transaction
  transaction_id UUID REFERENCES ur_transactions(id),

  -- Statut
  payment_number INTEGER NOT NULL,
  due_date DATE NOT NULL,
  paid_date DATE,
  is_late BOOLEAN DEFAULT false,
  late_fee_ur NUMERIC(20, 8) DEFAULT 0,

  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 14. TABLE DU FOND D'EXPANSION
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS expansion_fund (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Solde
  balance_ur NUMERIC(20, 8) DEFAULT 0,
  balance_fiat_cad NUMERIC(15, 2) DEFAULT 0,

  -- Totaux
  total_contributions NUMERIC(20, 8) DEFAULT 0,
  total_allocated NUMERIC(20, 8) DEFAULT 0,
  total_projects_funded INTEGER DEFAULT 0,

  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Initialiser avec une seule ligne
INSERT INTO expansion_fund (id)
VALUES (gen_random_uuid())
ON CONFLICT DO NOTHING;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 15. TABLE DES PROJETS D'EXPANSION
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS expansion_projects (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

  -- Détails
  title TEXT NOT NULL,
  description TEXT,
  category TEXT CHECK (category IN (
    'infrastructure', 'land', 'equipment', 'research', 'community', 'other'
  )),

  -- Budget
  requested_amount_ur NUMERIC(20, 8) NOT NULL,
  approved_amount_ur NUMERIC(20, 8),
  disbursed_amount_ur NUMERIC(20, 8) DEFAULT 0,

  -- Gouvernance
  proposal_id UUID REFERENCES governance_proposals(id),

  -- Statut
  status TEXT DEFAULT 'proposed' CHECK (status IN (
    'proposed', 'voting', 'approved', 'in_progress', 'completed', 'cancelled'
  )),

  -- Responsable
  lead_member_id UUID REFERENCES auth.users(id),

  -- Timestamps
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  approved_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE
);

-- ═══════════════════════════════════════════════════════════════════════════════
-- 16. ACTIVER RLS
-- ═══════════════════════════════════════════════════════════════════════════════

ALTER TABLE economic_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_balances ENABLE ROW LEVEL SECURITY;
ALTER TABLE ur_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE rebate_distributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE liquidity_pool ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversion_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE governance_proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE governance_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE referral_network ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketplace_listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE marketplace_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE peer_loans ENABLE ROW LEVEL SECURITY;
ALTER TABLE loan_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE expansion_fund ENABLE ROW LEVEL SECURITY;
ALTER TABLE expansion_projects ENABLE ROW LEVEL SECURITY;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 17. POLICIES DE SÉCURITÉ
-- ═══════════════════════════════════════════════════════════════════════════════

-- economic_settings : lecture publique, modification souverain seulement
CREATE POLICY "Anyone can read economic settings"
  ON economic_settings FOR SELECT USING (true);

CREATE POLICY "Souverain can modify economic settings"
  ON economic_settings FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid() AND profiles.role = 'souverain'
    )
  );

-- member_balances : chacun voit son solde
CREATE POLICY "Users can view own balance"
  ON member_balances FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Souverain can view all balances"
  ON member_balances FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid() AND profiles.role = 'souverain'
    )
  );

-- ur_transactions : chacun voit ses transactions
CREATE POLICY "Users can view own transactions"
  ON ur_transactions FOR SELECT
  USING (from_user_id = auth.uid() OR to_user_id = auth.uid());

CREATE POLICY "Souverain can view all transactions"
  ON ur_transactions FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid() AND profiles.role = 'souverain'
    )
  );

-- governance_proposals : visible par tous les membres
CREATE POLICY "Members can view proposals"
  ON governance_proposals FOR SELECT
  USING (
    EXISTS (SELECT 1 FROM member_balances WHERE user_id = auth.uid())
  );

CREATE POLICY "Members can create proposals"
  ON governance_proposals FOR INSERT
  WITH CHECK (proposer_id = auth.uid());

-- marketplace_listings : visible par tous
CREATE POLICY "Anyone can view listings"
  ON marketplace_listings FOR SELECT USING (true);

CREATE POLICY "Users can manage own listings"
  ON marketplace_listings FOR ALL
  USING (seller_id = auth.uid());

-- ═══════════════════════════════════════════════════════════════════════════════
-- 18. FONCTIONS UTILITAIRES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Récupérer un paramètre du Volant Énergétique
CREATE OR REPLACE FUNCTION get_economic_setting(p_key TEXT)
RETURNS JSONB AS $$
DECLARE
  result JSONB;
BEGIN
  SELECT value INTO result
  FROM economic_settings
  WHERE key = p_key AND is_active = true;

  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Mettre à jour un paramètre (Souverain seulement)
CREATE OR REPLACE FUNCTION update_economic_setting(
  p_key TEXT,
  p_value JSONB
)
RETURNS JSONB AS $$
DECLARE
  setting_record RECORD;
  numeric_value NUMERIC;
BEGIN
  -- Vérifier que l'appelant est Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object('success', false, 'error', 'Accès réservé au Souverain');
  END IF;

  -- Récupérer les contraintes
  SELECT * INTO setting_record FROM economic_settings WHERE key = p_key;

  IF setting_record IS NULL THEN
    RETURN jsonb_build_object('success', false, 'error', 'Paramètre inconnu');
  END IF;

  -- Vérifier les limites si numériques
  BEGIN
    numeric_value := p_value::NUMERIC;

    IF setting_record.min_value IS NOT NULL AND numeric_value < setting_record.min_value THEN
      RETURN jsonb_build_object('success', false, 'error', 'Valeur sous le minimum');
    END IF;

    IF setting_record.max_value IS NOT NULL AND numeric_value > setting_record.max_value THEN
      RETURN jsonb_build_object('success', false, 'error', 'Valeur au-dessus du maximum');
    END IF;
  EXCEPTION WHEN OTHERS THEN
    -- Pas un numérique, ignorer la validation
    NULL;
  END;

  -- Mettre à jour
  UPDATE economic_settings
  SET value = p_value, updated_at = NOW(), updated_by = auth.uid()
  WHERE key = p_key;

  RETURN jsonb_build_object(
    'success', true,
    'key', p_key,
    'new_value', p_value
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Calculer le score de résonance d'un membre
CREATE OR REPLACE FUNCTION calculate_resonance_score(p_user_id UUID)
RETURNS JSONB AS $$
DECLARE
  activity_score NUMERIC := 0;
  contribution_score NUMERIC := 0;
  tenure_score NUMERIC := 0;
  investment_score NUMERIC := 0;
  referral_score NUMERIC := 0;
  final_score NUMERIC := 0;

  avg_transactions NUMERIC;
  user_transactions NUMERIC;
  user_tenure_months INTEGER;
  user_balance NUMERIC;
  avg_balance NUMERIC;
  user_referrals INTEGER;
BEGIN
  -- Calcul activity_score (basé sur transactions des 30 derniers jours)
  SELECT COUNT(*) INTO user_transactions
  FROM ur_transactions
  WHERE (from_user_id = p_user_id OR to_user_id = p_user_id)
    AND created_at > NOW() - INTERVAL '30 days';

  SELECT AVG(tx_count) INTO avg_transactions
  FROM (
    SELECT COUNT(*) as tx_count
    FROM ur_transactions
    WHERE created_at > NOW() - INTERVAL '30 days'
    GROUP BY COALESCE(from_user_id, to_user_id)
  ) sub;

  IF avg_transactions > 0 THEN
    activity_score := LEAST(100, (user_transactions / avg_transactions) * 100);
  END IF;

  -- Calcul tenure_score
  SELECT EXTRACT(MONTH FROM AGE(NOW(), created_at))::INTEGER
  INTO user_tenure_months
  FROM member_balances WHERE user_id = p_user_id;

  tenure_score := LEAST(100, COALESCE(user_tenure_months, 0) / 12.0 * 100);

  -- Calcul investment_score
  SELECT ur_balance INTO user_balance
  FROM member_balances WHERE user_id = p_user_id;

  SELECT AVG(ur_balance) INTO avg_balance FROM member_balances WHERE ur_balance > 0;

  IF avg_balance > 0 THEN
    investment_score := LEAST(100, (COALESCE(user_balance, 0) / avg_balance) * 100);
  END IF;

  -- Calcul referral_score
  SELECT COUNT(*) INTO user_referrals
  FROM referral_network
  WHERE referrer_id = p_user_id AND is_active = true;

  referral_score := LEAST(100, COALESCE(user_referrals, 0) * 10);

  -- Score final pondéré
  final_score :=
    (activity_score * 0.25) +
    (contribution_score * 0.25) +
    (tenure_score * 0.20) +
    (investment_score * 0.15) +
    (referral_score * 0.15);

  -- Mettre à jour le solde du membre
  UPDATE member_balances
  SET
    resonance_score = final_score,
    activity_score = activity_score,
    updated_at = NOW()
  WHERE user_id = p_user_id;

  RETURN jsonb_build_object(
    'success', true,
    'user_id', p_user_id,
    'resonance_score', final_score,
    'breakdown', jsonb_build_object(
      'activity', activity_score,
      'contribution', contribution_score,
      'tenure', tenure_score,
      'investment', investment_score,
      'referral', referral_score
    )
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Obtenir le tableau de bord économique (Souverain)
CREATE OR REPLACE FUNCTION get_economic_dashboard()
RETURNS JSONB AS $$
DECLARE
  dashboard JSONB;
  pool RECORD;
BEGIN
  -- Vérifier accès Souverain
  IF NOT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'souverain'
  ) THEN
    RETURN jsonb_build_object('success', false, 'error', 'Accès réservé au Souverain');
  END IF;

  -- Récupérer l'état de la pool
  SELECT * INTO pool FROM liquidity_pool LIMIT 1;

  SELECT jsonb_build_object(
    'success', true,
    'liquidity', jsonb_build_object(
      'fiat_cad', pool.fiat_balance_cad,
      'fiat_usd', pool.fiat_balance_usd,
      'ur_supply', pool.ur_total_supply,
      'ur_circulation', pool.ur_in_circulation,
      'reserve_ratio', pool.reserve_ratio,
      'ur_rate_cad', pool.current_ur_rate_cad,
      'velocity_30d', pool.velocity_30d,
      'emergency_mode', pool.is_emergency_mode
    ),
    'members', jsonb_build_object(
      'total', (SELECT COUNT(*) FROM member_balances),
      'active_30d', (SELECT COUNT(DISTINCT COALESCE(from_user_id, to_user_id))
                     FROM ur_transactions
                     WHERE created_at > NOW() - INTERVAL '30 days'),
      'avg_balance', (SELECT AVG(ur_balance) FROM member_balances),
      'avg_resonance', (SELECT AVG(resonance_score) FROM member_balances)
    ),
    'transactions_30d', jsonb_build_object(
      'count', (SELECT COUNT(*) FROM ur_transactions WHERE created_at > NOW() - INTERVAL '30 days'),
      'volume', (SELECT COALESCE(SUM(amount), 0) FROM ur_transactions WHERE created_at > NOW() - INTERVAL '30 days'),
      'fees_collected', (SELECT COALESCE(SUM(fee), 0) FROM ur_transactions WHERE created_at > NOW() - INTERVAL '30 days')
    ),
    'governance', jsonb_build_object(
      'active_proposals', (SELECT COUNT(*) FROM governance_proposals WHERE status = 'voting'),
      'pending_proposals', (SELECT COUNT(*) FROM governance_proposals WHERE status = 'discussion')
    ),
    'expansion_fund', (SELECT jsonb_build_object('balance_ur', balance_ur, 'projects_funded', total_projects_funded) FROM expansion_fund LIMIT 1)
  ) INTO dashboard;

  RETURN dashboard;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ═══════════════════════════════════════════════════════════════════════════════
-- 19. INDEX POUR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_member_balances_resonance ON member_balances(resonance_score DESC);
CREATE INDEX IF NOT EXISTS idx_ur_transactions_users ON ur_transactions(from_user_id, to_user_id);
CREATE INDEX IF NOT EXISTS idx_ur_transactions_created ON ur_transactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ur_transactions_type ON ur_transactions(tx_type);
CREATE INDEX IF NOT EXISTS idx_rebate_distributions_user ON rebate_distributions(user_id);
CREATE INDEX IF NOT EXISTS idx_conversion_requests_user ON conversion_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_governance_proposals_status ON governance_proposals(status);
CREATE INDEX IF NOT EXISTS idx_referral_network_referrer ON referral_network(referrer_id);
CREATE INDEX IF NOT EXISTS idx_marketplace_listings_category ON marketplace_listings(category);
CREATE INDEX IF NOT EXISTS idx_peer_loans_status ON peer_loans(status);

-- ═══════════════════════════════════════════════════════════════════════════════
-- FIN DU SCRIPT
-- ═══════════════════════════════════════════════════════════════════════════════
--
-- RÉSUMÉ:
-- ✅ Table economic_settings : Variables du Volant Énergétique
-- ✅ Table member_balances : Soldes UR et scores
-- ✅ Table ur_transactions : Historique des transactions
-- ✅ Table rebate_distributions : Système de ristournes
-- ✅ Table liquidity_pool : Réserve de liquidité (singleton)
-- ✅ Table conversion_requests : Pont UR ↔ Fiat
-- ✅ Table governance_proposals : Propositions de vote
-- ✅ Table governance_votes : Votes des membres
-- ✅ Table referral_network : Réseau de parrainage
-- ✅ Table marketplace_listings : Marché de l'utilité
-- ✅ Table marketplace_orders : Commandes marketplace
-- ✅ Table peer_loans : Prêts P2P
-- ✅ Table expansion_fund : Fond d'expansion (singleton)
-- ✅ Table expansion_projects : Projets financés
--
-- FONCTIONS:
-- ✅ get_economic_setting() : Lire un paramètre
-- ✅ update_economic_setting() : Modifier (Souverain)
-- ✅ calculate_resonance_score() : Calculer le score d'un membre
-- ✅ get_economic_dashboard() : Tableau de bord (Souverain)
--
-- ═══════════════════════════════════════════════════════════════════════════════
