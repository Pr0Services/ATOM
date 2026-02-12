-- ═══════════════════════════════════════════════════════════
-- AT·OM — Schéma SQL : Facettes du Diamant
-- Gouvernance Directe · Économie de Résonance · Mapping Historique · Identité Souveraine
--
-- Supabase / PostgreSQL avec Row Level Security
-- ═══════════════════════════════════════════════════════════
--
-- PRÉREQUIS :
--   1. schema-rosetta.sql doit être exécuté EN PREMIER (définit les enums de base)
--   2. schema-pri.sql doit être exécuté EN SECOND (définit les types PRI)
--   3. Extension uuid-ossp déjà activée
--
-- TABLES CRÉÉES (8) :
--   GOUVERNANCE :
--     1. governance_proposals        — Propositions de gouvernance directe
--     2. governance_votes            — Votes pondérés par resonance_score
--   ÉCONOMIE :
--     3. economic_transactions       — Transactions en Unités de Résonance (UR)
--     4. flow_keeper_snapshots       — État du FlowKeeper (remplace les taxes)
--   MAPPING :
--     5. mapping_entries             — Entrées de cartographie historique (6 couches)
--     6. mapping_sources             — Sources vérifiées pour chaque entrée
--   IDENTITÉ :
--     7. sovereign_identities        — Identités souveraines DID
--     8. verifiable_credentials      — Credentials vérifiables
--
-- VUES (3) :
--   - governance_dashboard           — Résumé des propositions
--   - economy_sphere_flows           — Flux UR par sphère
--   - identity_sovereignty_summary   — Distribution des rangs souverains
--
-- TRIGGERS (3) :
--   - trg_gov_vote_tally             — Auto-comptage des votes
--   - trg_identity_rank_update       — Auto-calcul du rang
--   - updated_at sur toutes les tables (réutilise update_timestamp())
-- ═══════════════════════════════════════════════════════════


-- ═══════════════════════════════════════════════════════════
-- TYPES ÉNUMÉRÉS — FACETTES DU DIAMANT
-- ═══════════════════════════════════════════════════════════

-- Gouvernance
CREATE TYPE proposal_type AS ENUM ('OPERATIONNELLE', 'STRUCTURELLE', 'CONSTITUTIONNELLE');
CREATE TYPE proposal_status AS ENUM ('DRAFT', 'DISCUSSION', 'VOTING', 'APPROVED', 'REJECTED', 'EXECUTED');
CREATE TYPE vote_value AS ENUM ('POUR', 'CONTRE', 'ABSTENTION');

-- Économie
CREATE TYPE transaction_type AS ENUM (
  'CONTRIBUTION', 'FLOW_KEEPER', 'EXCHANGE', 'REBATE',
  'STIMULUS', 'BURN', 'MINT_JT', 'MINT_SOUVENIR'
);

-- Mapping
CREATE TYPE mapping_layer AS ENUM (
  'EVENEMENTS', 'NARRATIFS', 'PATTERNS', 'CAUSALITES', 'VIBRATIONS', 'PROJECTIONS'
);

-- Identité
CREATE TYPE identity_action AS ENUM (
  'CREATE_DID', 'VERIFY_CREDENTIAL', 'ISSUE_CREDENTIAL', 'REVOKE_CREDENTIAL',
  'UPDATE_PROFILE', 'MINT_NFT', 'SOVEREIGNTY_CLAIM', 'EXPORT_DATA', 'DELETE_DATA'
);

-- Rang de résonance
CREATE TYPE resonance_rank AS ENUM ('INITIE', 'CITOYEN', 'FONDATEUR', 'GARDIEN', 'ARCHITECTE');

-- Tier NFT
CREATE TYPE nft_tier AS ENUM ('GRAINE', 'POUSSE', 'BRANCHE', 'RACINE', 'ARBRE');


-- ═══════════════════════════════════════════════════════════
--  FACETTE POLITIQUE — GOUVERNANCE DIRECTE
-- ═══════════════════════════════════════════════════════════
-- "Nous décidons ensemble. Personne n'est au-dessus."
-- Conseil des 144, quorum 33%, consensus 67%
-- ═══════════════════════════════════════════════════════════

-- ─── TABLE : governance_proposals ──────────────────────────
-- Chaque proposition est traduite par le RosettaParser
-- et validée par la Table d'Émeraude avant soumission au vote.

CREATE TABLE governance_proposals (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  type                proposal_type NOT NULL,
  title               TEXT NOT NULL,
  description         TEXT NOT NULL,
  sphere_id           sphere_id,                            -- NULL = proposition trans-sphères
  proposer_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  status              proposal_status DEFAULT 'DRAFT',

  -- Paramètres de vote
  stake_required      NUMERIC NOT NULL DEFAULT 10,          -- UR minimum pour participer
  quorum_pct          NUMERIC DEFAULT 0.33,                 -- 33% du Conseil
  approval_pct        NUMERIC DEFAULT 0.67,                 -- 67% pour consensus
  discussion_days     INTEGER DEFAULT 3 CHECK (discussion_days BETWEEN 3 AND 7),

  -- Compteurs de votes (mis à jour par trigger)
  votes_pour          INTEGER DEFAULT 0,
  votes_contre        INTEGER DEFAULT 0,
  votes_abstention    INTEGER DEFAULT 0,

  -- Temporalité
  voting_ends_at      TIMESTAMPTZ,

  -- Liens Rosetta
  rosetta_mapping_id  UUID REFERENCES rosetta_mappings(id) ON DELETE SET NULL,
  node_id             UUID REFERENCES nodes(id) ON DELETE SET NULL,

  created_at          TIMESTAMPTZ DEFAULT now(),
  updated_at          TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE governance_proposals IS 'Propositions de gouvernance directe — traduites par Rosetta, validées par Émeraude';
COMMENT ON COLUMN governance_proposals.type IS 'OPERATIONNELLE (simple), STRUCTURELLE (75% requis), CONSTITUTIONNELLE (90% + 7 jours)';
COMMENT ON COLUMN governance_proposals.quorum_pct IS 'Pourcentage minimum de participants requis (défaut: 33% du Conseil)';
COMMENT ON COLUMN governance_proposals.approval_pct IS 'Pourcentage de POUR requis pour consensus (défaut: 67%)';
COMMENT ON COLUMN governance_proposals.stake_required IS 'Unités de Résonance minimum pour voter sur cette proposition';

CREATE INDEX idx_gov_proposals_proposer ON governance_proposals(proposer_id);
CREATE INDEX idx_gov_proposals_status ON governance_proposals(status);
CREATE INDEX idx_gov_proposals_sphere ON governance_proposals(sphere_id);
CREATE INDEX idx_gov_proposals_type ON governance_proposals(type);
CREATE INDEX idx_gov_proposals_voting_ends ON governance_proposals(voting_ends_at DESC);
CREATE INDEX idx_gov_proposals_rosetta ON governance_proposals(rosetta_mapping_id);
CREATE INDEX idx_gov_proposals_node ON governance_proposals(node_id);
CREATE INDEX idx_gov_proposals_created ON governance_proposals(created_at DESC);

-- ─── TABLE : governance_votes ──────────────────────────────
-- Un vote par utilisateur par proposition. Immutable (pas d'UPDATE/DELETE).
-- Le poids est calculé par calculateVoteWeight(resonance_score).

CREATE TABLE governance_votes (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  proposal_id     UUID NOT NULL REFERENCES governance_proposals(id) ON DELETE CASCADE,
  voter_id        UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  vote            vote_value NOT NULL,
  weight          NUMERIC DEFAULT 1 CHECK (weight > 0),     -- Pondéré par resonance_score
  resonance_score NUMERIC DEFAULT 0,                         -- Score au moment du vote
  created_at      TIMESTAMPTZ DEFAULT now(),

  -- Un seul vote par utilisateur par proposition
  UNIQUE(proposal_id, voter_id)
);

COMMENT ON TABLE governance_votes IS 'Votes immutables pondérés par resonance_score — un vote par personne par proposition';
COMMENT ON COLUMN governance_votes.weight IS 'Poids du vote calculé par calculateVoteWeight(resonance_score)';

CREATE INDEX idx_gov_votes_proposal ON governance_votes(proposal_id);
CREATE INDEX idx_gov_votes_voter ON governance_votes(voter_id);
CREATE INDEX idx_gov_votes_value ON governance_votes(vote);
CREATE INDEX idx_gov_votes_created ON governance_votes(created_at DESC);


-- ═══════════════════════════════════════════════════════════
--  FACETTE ÉCONOMIQUE — ÉCONOMIE DE RÉSONANCE
-- ═══════════════════════════════════════════════════════════
-- "La richesse circule comme le sang. Donner = Recevoir."
-- UR (Unité de Résonance), FlowKeeper (remplace les taxes)
-- ═══════════════════════════════════════════════════════════

-- ─── TABLE : economic_transactions ─────────────────────────
-- Chaque transaction porte la signature fréquentielle du VibrationalMotor.

CREATE TABLE economic_transactions (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  type                transaction_type NOT NULL,
  from_id             UUID REFERENCES auth.users(id) ON DELETE SET NULL,  -- NULL = SYSTÈME
  to_id               UUID REFERENCES auth.users(id) ON DELETE SET NULL,  -- NULL = SYSTÈME
  amount_ur           NUMERIC NOT NULL CHECK (amount_ur > 0),
  sphere_id           sphere_id NOT NULL,
  description         TEXT,

  -- Contexte de résonance
  from_resonance      NUMERIC DEFAULT 0,                     -- resonance_score de l'émetteur
  to_resonance        NUMERIC DEFAULT 0,                     -- resonance_score du receveur
  is_flow_keeper      BOOLEAN DEFAULT false,                 -- Est-ce une contribution FlowKeeper ?

  -- Métadonnées
  metadata            JSONB,

  -- Liens Rosetta
  rosetta_mapping_id  UUID REFERENCES rosetta_mappings(id) ON DELETE SET NULL,
  node_id             UUID REFERENCES nodes(id) ON DELETE SET NULL,

  created_at          TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE economic_transactions IS 'Transactions en Unités de Résonance — chaque mouvement porte une signature fréquentielle';
COMMENT ON COLUMN economic_transactions.type IS '8 types: CONTRIBUTION, FLOW_KEEPER, EXCHANGE, REBATE, STIMULUS, BURN, MINT_JT, MINT_SOUVENIR';
COMMENT ON COLUMN economic_transactions.is_flow_keeper IS 'TRUE si cette transaction est une contribution au FlowKeeper (remplace les taxes)';
COMMENT ON COLUMN economic_transactions.from_id IS 'NULL = transaction système (minting, stimulus)';
COMMENT ON COLUMN economic_transactions.to_id IS 'NULL = transaction système (burn, flow_keeper)';

CREATE INDEX idx_econ_tx_from ON economic_transactions(from_id);
CREATE INDEX idx_econ_tx_to ON economic_transactions(to_id);
CREATE INDEX idx_econ_tx_type ON economic_transactions(type);
CREATE INDEX idx_econ_tx_sphere ON economic_transactions(sphere_id);
CREATE INDEX idx_econ_tx_flow_keeper ON economic_transactions(is_flow_keeper) WHERE is_flow_keeper = true;
CREATE INDEX idx_econ_tx_created ON economic_transactions(created_at DESC);
CREATE INDEX idx_econ_tx_rosetta ON economic_transactions(rosetta_mapping_id);
CREATE INDEX idx_econ_tx_node ON economic_transactions(node_id);

-- ─── TABLE : flow_keeper_snapshots ─────────────────────────
-- Photographie périodique de l'état du FlowKeeper.
-- Permet de tracer l'évolution de la masse monétaire et de la vélocité.

CREATE TABLE flow_keeper_snapshots (
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Métriques économiques
  velocity_30d          NUMERIC,                              -- Vélocité sur 30 jours
  reserve_ratio         NUMERIC,                              -- Ratio de réserve (doit être ≥ 100%)
  total_supply          NUMERIC,                              -- Masse monétaire totale (UR)
  total_burned          NUMERIC DEFAULT 0,                    -- Total brûlé depuis le début

  -- Diagnostic FlowKeeper
  action_recommended    TEXT CHECK (action_recommended IN (
    'EQUILIBRE', 'ANTI_INFLATION', 'ANTI_DEFLATION', 'CRISE'
  )),
  severity              TEXT DEFAULT 'info' CHECK (severity IN ('info', 'warning', 'critical')),

  -- Paramètres actifs
  burn_rate_current     NUMERIC,                              -- Taux de burn actuel (%)
  resonance_rebate_pct  NUMERIC,                              -- Réduction pour haut resonance_score (%)
  cooperation_index     NUMERIC,                              -- Indice de coopération inter-sphères

  metadata              JSONB,
  created_at            TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE flow_keeper_snapshots IS 'Photographie périodique du FlowKeeper — évolution masse monétaire et vélocité';
COMMENT ON COLUMN flow_keeper_snapshots.action_recommended IS 'Diagnostic: EQUILIBRE (tout va bien), ANTI_INFLATION, ANTI_DEFLATION, CRISE';
COMMENT ON COLUMN flow_keeper_snapshots.reserve_ratio IS 'Ratio de réserve — doit rester ≥ 100% (principe de non-extraction)';

CREATE INDEX idx_fk_snapshots_created ON flow_keeper_snapshots(created_at DESC);
CREATE INDEX idx_fk_snapshots_action ON flow_keeper_snapshots(action_recommended);
CREATE INDEX idx_fk_snapshots_severity ON flow_keeper_snapshots(severity);


-- ═══════════════════════════════════════════════════════════
--  FACETTE HISTORIQUE — AT-OM MAPPING (6 COUCHES)
-- ═══════════════════════════════════════════════════════════
-- "Nous ne réécrivons pas l'histoire. Nous la DÉCHIFFRONS."
-- 6 couches : Événements → Narratifs → Patterns → Causalités → Vibrations → Projections
-- ═══════════════════════════════════════════════════════════

-- ─── TABLE : mapping_entries ───────────────────────────────
-- Chaque entrée est une donnée historique positionnée sur une couche
-- et connectée à des sphères, des patterns et des lois universelles.

CREATE TABLE mapping_entries (
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  layer                 mapping_layer NOT NULL,
  title                 TEXT NOT NULL,
  description           TEXT,

  -- Temporalité
  epoch_start           BIGINT,                               -- Année ou timestamp
  epoch_end             BIGINT,                               -- NULL = en cours

  -- Connexions
  sphere_connections    sphere_id[] DEFAULT '{}',             -- Sphères impactées
  patterns_linked       UUID[] DEFAULT '{}',                  -- IDs d'entrées liées (patterns)

  -- Analyse
  resonance_frequency   NUMERIC,                              -- Fréquence de résonance historique
  narratives            TEXT[] DEFAULT '{}',                   -- Perspectives multiples
  causal_chain          JSONB,                                -- [{cause, effect}]
  laws_manifested       TEXT[] DEFAULT '{}',                   -- Lois universelles manifestées

  -- Liens Rosetta
  node_id               UUID REFERENCES nodes(id) ON DELETE SET NULL,
  rosetta_mapping_id    UUID REFERENCES rosetta_mappings(id) ON DELETE SET NULL,

  created_by            UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  created_at            TIMESTAMPTZ DEFAULT now(),
  updated_at            TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE mapping_entries IS 'Cartographie historique à 6 couches — événements, narratifs, patterns, causalités, vibrations, projections';
COMMENT ON COLUMN mapping_entries.layer IS 'Couche de profondeur: EVENEMENTS (surface) → PROJECTIONS (profond)';
COMMENT ON COLUMN mapping_entries.sphere_connections IS 'Tableau des sphères souveraines impactées par cet événement';
COMMENT ON COLUMN mapping_entries.causal_chain IS 'JSONB: [{cause: "...", effect: "..."}] — chaîne causale';
COMMENT ON COLUMN mapping_entries.laws_manifested IS 'Lois universelles manifestées: CORRESPONDANCE, VIBRATION, RYTHME, etc.';

CREATE INDEX idx_mapping_entries_layer ON mapping_entries(layer);
CREATE INDEX idx_mapping_entries_spheres ON mapping_entries USING gin(sphere_connections);
CREATE INDEX idx_mapping_entries_epoch ON mapping_entries(epoch_start);
CREATE INDEX idx_mapping_entries_creator ON mapping_entries(created_by);
CREATE INDEX idx_mapping_entries_rosetta ON mapping_entries(rosetta_mapping_id);
CREATE INDEX idx_mapping_entries_node ON mapping_entries(node_id);
CREATE INDEX idx_mapping_entries_laws ON mapping_entries USING gin(laws_manifested);
CREATE INDEX idx_mapping_entries_created ON mapping_entries(created_at DESC);

-- ─── TABLE : mapping_sources ───────────────────────────────
-- Sources vérifiées pour chaque entrée de mapping.
-- Les sources vérifiées on-chain reçoivent un bonus de crédibilité.

CREATE TABLE mapping_sources (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entry_id            UUID NOT NULL REFERENCES mapping_entries(id) ON DELETE CASCADE,
  type                TEXT NOT NULL CHECK (type IN ('primary', 'secondary', 'oral', 'archaeological')),
  reference           TEXT NOT NULL,
  credibility_score   NUMERIC DEFAULT 0 CHECK (credibility_score BETWEEN 0 AND 100),
  verified_on_chain   BOOLEAN DEFAULT false,
  hedera_proof_id     UUID REFERENCES hedera_proofs(id) ON DELETE SET NULL,
  created_at          TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE mapping_sources IS 'Sources vérifiées pour la cartographie — crédibilité scorée, ancrage Hedera optionnel';
COMMENT ON COLUMN mapping_sources.type IS 'Type de source: primary (témoignage direct), secondary (analyse), oral (tradition), archaeological';
COMMENT ON COLUMN mapping_sources.credibility_score IS 'Score 0-100 calculé par calculateSourceCredibility()';
COMMENT ON COLUMN mapping_sources.verified_on_chain IS 'TRUE si la source est ancrée sur Hedera Hashgraph';

CREATE INDEX idx_mapping_sources_entry ON mapping_sources(entry_id);
CREATE INDEX idx_mapping_sources_type ON mapping_sources(type);
CREATE INDEX idx_mapping_sources_credibility ON mapping_sources(credibility_score);
CREATE INDEX idx_mapping_sources_verified ON mapping_sources(verified_on_chain) WHERE verified_on_chain = true;
CREATE INDEX idx_mapping_sources_hedera ON mapping_sources(hedera_proof_id);


-- ═══════════════════════════════════════════════════════════
--  FACETTE IDENTITAIRE — IDENTITÉ SOUVERAINE
-- ═══════════════════════════════════════════════════════════
-- "Si tu ne possèdes pas tes données, tu ne te possèdes pas toi-même."
-- DID (Decentralized Identity), anonymat sélectif, droit export/oubli
-- ═══════════════════════════════════════════════════════════

-- ─── TABLE : sovereign_identities ──────────────────────────
-- Chaque utilisateur AT·OM possède une identité souveraine.
-- Le DID est l'ancre — tout le reste gravite autour.

CREATE TABLE sovereign_identities (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id             UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  did                 TEXT NOT NULL UNIQUE,                    -- Decentralized Identifier (did:atom:xxx)
  display_name        TEXT NOT NULL,
  avatar_hash         TEXT,                                    -- Hash de l'avatar (IPFS ou Hedera)

  -- Métriques de résonance
  resonance_score     NUMERIC DEFAULT 0 CHECK (resonance_score BETWEEN 0 AND 100),
  rank                resonance_rank DEFAULT 'INITIE',        -- Calculé automatiquement par trigger
  nft_tier            nft_tier,                                -- NULL = pas de NFT

  -- Souveraineté
  spheres_active      sphere_id[] DEFAULT '{}',               -- Sphères où l'utilisateur est actif
  is_sovereign        BOOLEAN DEFAULT false,                   -- A complété le processus de souveraineté
  is_verified         BOOLEAN DEFAULT false,                   -- Identité vérifiée
  privacy_level       TEXT DEFAULT 'SELECTIVE' CHECK (privacy_level IN ('PUBLIC', 'SELECTIVE', 'ANONYMOUS')),

  -- Liens Rosetta
  node_id             UUID REFERENCES nodes(id) ON DELETE SET NULL,
  rosetta_mapping_id  UUID REFERENCES rosetta_mappings(id) ON DELETE SET NULL,

  created_at          TIMESTAMPTZ DEFAULT now(),
  updated_at          TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE sovereign_identities IS 'Identité souveraine AT·OM — DID, résonance, rang, souveraineté des données';
COMMENT ON COLUMN sovereign_identities.did IS 'Decentralized Identifier unique (format: did:atom:xxx)';
COMMENT ON COLUMN sovereign_identities.resonance_score IS 'Score 0-100 calculé par computeResonanceScore() — pondération 5 axes';
COMMENT ON COLUMN sovereign_identities.rank IS 'INITIÉ(0-20), CITOYEN(20-40), FONDATEUR(40-60), GARDIEN(60-80), ARCHITECTE(80-100)';
COMMENT ON COLUMN sovereign_identities.privacy_level IS 'PUBLIC (profil visible), SELECTIVE (choix par champ), ANONYMOUS (DID seul)';

CREATE INDEX idx_identity_user ON sovereign_identities(user_id);
CREATE INDEX idx_identity_did ON sovereign_identities(did);
CREATE INDEX idx_identity_rank ON sovereign_identities(rank);
CREATE INDEX idx_identity_score ON sovereign_identities(resonance_score);
CREATE INDEX idx_identity_nft ON sovereign_identities(nft_tier);
CREATE INDEX idx_identity_spheres ON sovereign_identities USING gin(spheres_active);
CREATE INDEX idx_identity_sovereign ON sovereign_identities(is_sovereign) WHERE is_sovereign = true;
CREATE INDEX idx_identity_verified ON sovereign_identities(is_verified) WHERE is_verified = true;
CREATE INDEX idx_identity_rosetta ON sovereign_identities(rosetta_mapping_id);
CREATE INDEX idx_identity_node ON sovereign_identities(node_id);

-- ─── TABLE : verifiable_credentials ────────────────────────
-- Credentials vérifiables émis entre identités souveraines.
-- Ancrables sur Hedera pour preuve immuable.

CREATE TABLE verifiable_credentials (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  type                TEXT NOT NULL CHECK (type IN ('skill', 'contribution', 'role', 'attestation')),
  issuer_did          TEXT NOT NULL,                           -- DID de l'émetteur
  subject_did         TEXT NOT NULL,                           -- DID du sujet
  claim               JSONB NOT NULL,                          -- Contenu du credential
  hedera_proof_id     UUID REFERENCES hedera_proofs(id) ON DELETE SET NULL,
  issued_at           TIMESTAMPTZ DEFAULT now(),
  expires_at          TIMESTAMPTZ,                             -- NULL = pas d'expiration
  revoked_at          TIMESTAMPTZ,                             -- NULL = actif
  identity_id         UUID REFERENCES sovereign_identities(id) ON DELETE CASCADE
);

COMMENT ON TABLE verifiable_credentials IS 'Credentials vérifiables — émis entre DID, ancrables sur Hedera';
COMMENT ON COLUMN verifiable_credentials.type IS 'Type: skill (compétence), contribution (apport), role (fonction), attestation (témoignage)';
COMMENT ON COLUMN verifiable_credentials.claim IS 'JSONB: contenu structuré du credential (libre selon le type)';

CREATE INDEX idx_vc_issuer ON verifiable_credentials(issuer_did);
CREATE INDEX idx_vc_subject ON verifiable_credentials(subject_did);
CREATE INDEX idx_vc_type ON verifiable_credentials(type);
CREATE INDEX idx_vc_identity ON verifiable_credentials(identity_id);
CREATE INDEX idx_vc_hedera ON verifiable_credentials(hedera_proof_id);
CREATE INDEX idx_vc_expires ON verifiable_credentials(expires_at);
CREATE INDEX idx_vc_revoked ON verifiable_credentials(revoked_at) WHERE revoked_at IS NULL;
CREATE INDEX idx_vc_issued ON verifiable_credentials(issued_at DESC);


-- ═══════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY — SOUVERAINETÉ DES DONNÉES
-- ═══════════════════════════════════════════════════════════

ALTER TABLE governance_proposals ENABLE ROW LEVEL SECURITY;
ALTER TABLE governance_votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE economic_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE flow_keeper_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE mapping_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE mapping_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE sovereign_identities ENABLE ROW LEVEL SECURITY;
ALTER TABLE verifiable_credentials ENABLE ROW LEVEL SECURITY;

-- ─── Gouvernance — Transparence totale ──────────────────────

-- Lecture : tout le monde peut voir les propositions (transparence)
CREATE POLICY "gov_proposals_read_all" ON governance_proposals
  FOR SELECT TO authenticated USING (true);

-- Création : utilisateurs authentifiés (contrôle par canPropose() côté app)
CREATE POLICY "gov_proposals_insert" ON governance_proposals
  FOR INSERT TO authenticated
  WITH CHECK (proposer_id = auth.uid());

-- Mise à jour : proposeur ou admin
CREATE POLICY "gov_proposals_update" ON governance_proposals
  FOR UPDATE TO authenticated
  USING (
    proposer_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Votes : lisibles par tous (transparence)
CREATE POLICY "gov_votes_read_all" ON governance_votes
  FOR SELECT TO authenticated USING (true);

-- Votes : un seul insert par voter (immutable — pas d'update ni delete)
CREATE POLICY "gov_votes_insert" ON governance_votes
  FOR INSERT TO authenticated
  WITH CHECK (voter_id = auth.uid());

-- ─── Économie — Traçabilité totale ──────────────────────────

-- Transactions : participants + admin
CREATE POLICY "econ_tx_read" ON economic_transactions
  FOR SELECT TO authenticated
  USING (
    from_id = auth.uid() OR to_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Transactions : insertion par le from_id ou système
CREATE POLICY "econ_tx_insert" ON economic_transactions
  FOR INSERT TO authenticated
  WITH CHECK (
    from_id = auth.uid() OR from_id IS NULL
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- FlowKeeper : lisible par tous (transparence économique)
CREATE POLICY "fk_snapshots_read_all" ON flow_keeper_snapshots
  FOR SELECT TO authenticated USING (true);

-- FlowKeeper : écriture système uniquement
CREATE POLICY "fk_snapshots_system_write" ON flow_keeper_snapshots
  FOR INSERT TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- ─── Mapping — Transparence historique ──────────────────────

-- Entrées : lisibles par tous (l'histoire appartient à tous)
CREATE POLICY "mapping_entries_read_all" ON mapping_entries
  FOR SELECT TO authenticated USING (true);

-- Entrées : création par utilisateurs authentifiés
CREATE POLICY "mapping_entries_insert" ON mapping_entries
  FOR INSERT TO authenticated
  WITH CHECK (created_by = auth.uid());

-- Entrées : mise à jour par créateur ou admin
CREATE POLICY "mapping_entries_update" ON mapping_entries
  FOR UPDATE TO authenticated
  USING (
    created_by = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Sources : lisibles par tous
CREATE POLICY "mapping_sources_read_all" ON mapping_sources
  FOR SELECT TO authenticated USING (true);

-- Sources : création par tout utilisateur authentifié
CREATE POLICY "mapping_sources_insert" ON mapping_sources
  FOR INSERT TO authenticated WITH CHECK (true);

-- ─── Identité — Souveraineté individuelle ───────────────────

-- Identités : lisibles selon privacy_level
CREATE POLICY "identity_read" ON sovereign_identities
  FOR SELECT TO authenticated
  USING (
    privacy_level = 'PUBLIC'
    OR user_id = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Identités : création par le propriétaire
CREATE POLICY "identity_insert" ON sovereign_identities
  FOR INSERT TO authenticated
  WITH CHECK (user_id = auth.uid());

-- Identités : mise à jour par le propriétaire (souveraineté)
CREATE POLICY "identity_update" ON sovereign_identities
  FOR UPDATE TO authenticated
  USING (user_id = auth.uid());

-- Credentials : lisibles par sujet ou émetteur
CREATE POLICY "vc_read" ON verifiable_credentials
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM sovereign_identities si
      WHERE si.user_id = auth.uid()
      AND (si.did = verifiable_credentials.issuer_did OR si.did = verifiable_credentials.subject_did)
    )
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Credentials : création par l'émetteur
CREATE POLICY "vc_insert" ON verifiable_credentials
  FOR INSERT TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM sovereign_identities si
      WHERE si.user_id = auth.uid()
      AND si.did = verifiable_credentials.issuer_did
    )
  );


-- ═══════════════════════════════════════════════════════════
-- TRIGGERS
-- ═══════════════════════════════════════════════════════════

-- ─── Trigger 1 : Auto-comptage des votes ────────────────────
-- Après INSERT sur governance_votes, met à jour les compteurs
-- de la proposition parente.

CREATE OR REPLACE FUNCTION fn_gov_vote_tally()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE governance_proposals SET
    votes_pour       = (SELECT COUNT(*) FROM governance_votes WHERE proposal_id = NEW.proposal_id AND vote = 'POUR'),
    votes_contre     = (SELECT COUNT(*) FROM governance_votes WHERE proposal_id = NEW.proposal_id AND vote = 'CONTRE'),
    votes_abstention = (SELECT COUNT(*) FROM governance_votes WHERE proposal_id = NEW.proposal_id AND vote = 'ABSTENTION'),
    updated_at       = now()
  WHERE id = NEW.proposal_id;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_gov_vote_tally ON governance_votes;
CREATE TRIGGER trg_gov_vote_tally
  AFTER INSERT ON governance_votes
  FOR EACH ROW
  EXECUTE FUNCTION fn_gov_vote_tally();

-- ─── Trigger 2 : Auto-calcul du rang ───────────────────────
-- Après UPDATE de resonance_score sur sovereign_identities,
-- recalcule automatiquement le rang selon les seuils :
-- INITIÉ(0-20), CITOYEN(20-40), FONDATEUR(40-60), GARDIEN(60-80), ARCHITECTE(80-100)

CREATE OR REPLACE FUNCTION fn_identity_rank_update()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.resonance_score IS DISTINCT FROM NEW.resonance_score THEN
    NEW.rank := CASE
      WHEN NEW.resonance_score >= 80 THEN 'ARCHITECTE'::resonance_rank
      WHEN NEW.resonance_score >= 60 THEN 'GARDIEN'::resonance_rank
      WHEN NEW.resonance_score >= 40 THEN 'FONDATEUR'::resonance_rank
      WHEN NEW.resonance_score >= 20 THEN 'CITOYEN'::resonance_rank
      ELSE 'INITIE'::resonance_rank
    END;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_identity_rank_update ON sovereign_identities;
CREATE TRIGGER trg_identity_rank_update
  BEFORE UPDATE ON sovereign_identities
  FOR EACH ROW
  EXECUTE FUNCTION fn_identity_rank_update();

-- ─── Triggers updated_at (réutilise update_timestamp()) ─────

CREATE TRIGGER gov_proposals_updated
  BEFORE UPDATE ON governance_proposals
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER mapping_entries_updated
  BEFORE UPDATE ON mapping_entries
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER identity_updated
  BEFORE UPDATE ON sovereign_identities
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();


-- ═══════════════════════════════════════════════════════════
-- VUES
-- ═══════════════════════════════════════════════════════════

-- ─── Vue : governance_dashboard ─────────────────────────────
CREATE OR REPLACE VIEW governance_dashboard AS
SELECT
  gp.sphere_id,
  gp.type,
  gp.status,
  COUNT(gp.id) as proposal_count,
  SUM(gp.votes_pour) as total_pour,
  SUM(gp.votes_contre) as total_contre,
  SUM(gp.votes_abstention) as total_abstention,
  AVG(CASE WHEN gp.votes_pour + gp.votes_contre > 0
    THEN gp.votes_pour::numeric / (gp.votes_pour + gp.votes_contre)
    ELSE 0
  END) as avg_approval_rate
FROM governance_proposals gp
GROUP BY gp.sphere_id, gp.type, gp.status;

-- ─── Vue : economy_sphere_flows ─────────────────────────────
CREATE OR REPLACE VIEW economy_sphere_flows AS
SELECT
  et.sphere_id,
  et.type,
  COUNT(et.id) as tx_count,
  SUM(et.amount_ur) as total_ur,
  AVG(et.amount_ur) as avg_ur,
  MIN(et.created_at) as first_tx,
  MAX(et.created_at) as last_tx
FROM economic_transactions et
GROUP BY et.sphere_id, et.type;

-- ─── Vue : identity_sovereignty_summary ─────────────────────
CREATE OR REPLACE VIEW identity_sovereignty_summary AS
SELECT
  si.rank,
  COUNT(si.id) as user_count,
  AVG(si.resonance_score) as avg_score,
  COUNT(CASE WHEN si.is_sovereign THEN 1 END) as sovereign_count,
  COUNT(CASE WHEN si.is_verified THEN 1 END) as verified_count,
  COUNT(CASE WHEN si.nft_tier IS NOT NULL THEN 1 END) as nft_holders
FROM sovereign_identities si
GROUP BY si.rank;


-- ═══════════════════════════════════════════════════════════
-- SUPABASE REALTIME
-- ═══════════════════════════════════════════════════════════

DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE governance_proposals;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE governance_votes;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE economic_transactions;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE flow_keeper_snapshots;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE mapping_entries;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE mapping_sources;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE sovereign_identities;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE verifiable_credentials;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;


-- ═══════════════════════════════════════════════════════════
-- VÉRIFICATION
-- ═══════════════════════════════════════════════════════════

DO $$
BEGIN
  RAISE NOTICE '═══ AT·OM — Facettes du Diamant (Schéma SQL) ═══';
  RAISE NOTICE '';
  RAISE NOTICE '  ENUMS (8) :';
  RAISE NOTICE '    ✓ proposal_type, proposal_status, vote_value';
  RAISE NOTICE '    ✓ transaction_type';
  RAISE NOTICE '    ✓ mapping_layer';
  RAISE NOTICE '    ✓ identity_action, resonance_rank, nft_tier';
  RAISE NOTICE '';
  RAISE NOTICE '  TABLES (8) :';
  RAISE NOTICE '    ✓ governance_proposals     (Facette Politique)';
  RAISE NOTICE '    ✓ governance_votes          (Facette Politique)';
  RAISE NOTICE '    ✓ economic_transactions     (Facette Économique)';
  RAISE NOTICE '    ✓ flow_keeper_snapshots     (Facette Économique)';
  RAISE NOTICE '    ✓ mapping_entries           (Facette Historique)';
  RAISE NOTICE '    ✓ mapping_sources           (Facette Historique)';
  RAISE NOTICE '    ✓ sovereign_identities      (Facette Identitaire)';
  RAISE NOTICE '    ✓ verifiable_credentials    (Facette Identitaire)';
  RAISE NOTICE '';
  RAISE NOTICE '  TRIGGERS (5) :';
  RAISE NOTICE '    ✓ trg_gov_vote_tally        (auto-comptage votes)';
  RAISE NOTICE '    ✓ trg_identity_rank_update  (auto-rang par resonance_score)';
  RAISE NOTICE '    ✓ gov_proposals_updated      (updated_at)';
  RAISE NOTICE '    ✓ mapping_entries_updated    (updated_at)';
  RAISE NOTICE '    ✓ identity_updated           (updated_at)';
  RAISE NOTICE '';
  RAISE NOTICE '  VUES (3) :';
  RAISE NOTICE '    ✓ governance_dashboard       (résumé propositions)';
  RAISE NOTICE '    ✓ economy_sphere_flows       (flux UR par sphère)';
  RAISE NOTICE '    ✓ identity_sovereignty_summary (distribution rangs)';
  RAISE NOTICE '';
  RAISE NOTICE '  RLS : Activé sur les 8 tables avec politiques de souveraineté';
  RAISE NOTICE '  Realtime : Activé pour les 8 tables';
  RAISE NOTICE '';
  RAISE NOTICE '═══ Facettes du Diamant installées avec succès ═══';
END $$;

-- ═══════════════════════════════════════════════════════════
-- FIN DU SCRIPT — FACETTES DU DIAMANT
-- ═══════════════════════════════════════════════════════════

-- Requêtes de vérification :
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('governance_proposals', 'governance_votes', 'economic_transactions', 'flow_keeper_snapshots', 'mapping_entries', 'mapping_sources', 'sovereign_identities', 'verifiable_credentials');
-- SELECT * FROM governance_dashboard LIMIT 10;
-- SELECT * FROM economy_sphere_flows LIMIT 10;
-- SELECT * FROM identity_sovereignty_summary;
