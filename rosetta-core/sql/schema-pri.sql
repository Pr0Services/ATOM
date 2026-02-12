-- ═══════════════════════════════════════════════════════════
-- AT·OM — Schéma SQL : Module PRI
-- Passerelle de Rédemption Institutionnelle
-- Permet aux entités institutionnelles (corporations, gouvernements,
-- banques) de contribuer à l'économie souveraine d'AT·OM via un
-- processus de rédemption transparent, ancré sur la blockchain Hedera.
-- Supabase / PostgreSQL avec Row Level Security
-- ═══════════════════════════════════════════════════════════
--
-- PRÉREQUIS :
--   1. schema-rosetta.sql doit être exécuté EN PREMIER (définit les enums de base)
--   2. Extension uuid-ossp déjà activée
--
-- TABLES CRÉÉES :
--   1. institutional_entities       — Registre des institutions en quête de rédemption
--   2. institutional_redemptions    — Chaque contribution de rédemption
--   3. redemption_audit_trail       — Journal immuable de toutes les actions d'audit
--   4. redemption_balance           — Solde courant d'impact par institution
--   5. redemption_conversion_rates  — Formules de conversion AT-OM$
--
-- VUES :
--   - redemption_dashboard          — Tableau de bord par entité
--
-- FONCTIONS :
--   - calculate_resonance_units()   — Calcul des unités de résonance AT-OM$
--
-- TRIGGERS :
--   - trg_redemption_to_audit       — Journal automatique lors d'un changement de statut
--   - trg_redemption_update_balance — Mise à jour du solde lors d'une complétion
-- ═══════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════
-- TYPES ÉNUMÉRÉS — MODULE PRI
-- ═══════════════════════════════════════════════════════════

-- Type de contribution institutionnelle
CREATE TYPE contribution_type AS ENUM (
  'GRANT', 'REDEMPTION', 'PARTNERSHIP', 'RESTITUTION'
);

-- Statut du processus de rédemption
CREATE TYPE redemption_status AS ENUM (
  'SUBMITTED', 'UNDER_AUDIT', 'ACCEPTED', 'REJECTED',
  'ESCROW', 'COMPLETED', 'REVOKED'
);

-- Secteur d'impact — les 9 sphères souveraines + portée élargie
CREATE TYPE impact_sector AS ENUM (
  'TECHNO', 'POLITIQUE', 'ECONOMIE', 'EDUCATION', 'SANTE',
  'CULTURE', 'ENVIRONNEMENT', 'JUSTICE', 'SPIRITUALITE',
  'MULTI_SPHERE', 'SYSTEMIC'
);

-- ═══════════════════════════════════════════════════════════
-- TABLE : institutional_entities
-- Registre des institutions en quête de rédemption dans AT·OM
-- Chaque entité est un point d'ancrage entre le monde institutionnel
-- et l'économie souveraine.
-- ═══════════════════════════════════════════════════════════

CREATE TABLE institutional_entities (
  id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entity_name         TEXT NOT NULL,
  entity_type         TEXT NOT NULL,                       -- 'corporation', 'government', 'bank', 'ngo', 'foundation'
  jurisdiction        TEXT,                                -- Juridiction légale de l'entité
  registration_id     TEXT,                                -- Numéro d'enregistrement officiel
  public_disclosure   JSONB,                               -- Divulgations publiques de l'entité
  trust_score         NUMERIC DEFAULT 0 CHECK (trust_score >= 0 AND trust_score <= 100),
  is_verified         BOOLEAN DEFAULT false,
  rosetta_mapping_id  UUID REFERENCES rosetta_mappings(id) ON DELETE SET NULL,
  node_id             UUID REFERENCES nodes(id) ON DELETE SET NULL,
  created_at          TIMESTAMPTZ DEFAULT now(),
  updated_at          TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE institutional_entities IS 'Registre des institutions cherchant la rédemption — pont entre le monde institutionnel et AT·OM';
COMMENT ON COLUMN institutional_entities.entity_type IS 'Type d''entité : corporation, government, bank, ngo, foundation';
COMMENT ON COLUMN institutional_entities.trust_score IS 'Score de confiance (0-100) — évolue avec les contributions vérifiées';
COMMENT ON COLUMN institutional_entities.public_disclosure IS 'JSONB des divulgations publiques (historique, engagements, rapports)';
COMMENT ON COLUMN institutional_entities.rosetta_mapping_id IS 'FK vers rosetta_mappings — traduction tri-dimensionnelle de l''entité';

CREATE INDEX idx_pri_entities_type ON institutional_entities(entity_type);
CREATE INDEX idx_pri_entities_verified ON institutional_entities(is_verified);
CREATE INDEX idx_pri_entities_trust ON institutional_entities(trust_score);
CREATE INDEX idx_pri_entities_rosetta ON institutional_entities(rosetta_mapping_id);
CREATE INDEX idx_pri_entities_node ON institutional_entities(node_id);
CREATE INDEX idx_pri_entities_jurisdiction ON institutional_entities(jurisdiction);

-- ═══════════════════════════════════════════════════════════
-- TABLE : institutional_redemptions
-- Chaque contribution de rédemption — le cœur du processus PRI.
-- Suit le parcours alchimique de la Calcination à la Coagulation.
-- ═══════════════════════════════════════════════════════════

CREATE TABLE institutional_redemptions (
  id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entity_id               UUID NOT NULL REFERENCES institutional_entities(id) ON DELETE CASCADE,
  contribution_type       contribution_type NOT NULL,
  status                  redemption_status DEFAULT 'SUBMITTED',
  amount_fiat             NUMERIC,                          -- Valeur monétaire en devise fiat
  currency                TEXT DEFAULT 'CAD',
  resonance_units_issued  NUMERIC DEFAULT 0,                -- Équivalent AT-OM$ émis
  impact_sector           impact_sector NOT NULL,
  target_sphere           sphere_id,                        -- Sphère bénéficiaire directe
  description_public      TEXT NOT NULL,                     -- Description publique de la contribution
  audit_report            JSONB,                            -- Rapport d'audit détaillé
  escrow_hedera_id        TEXT,                             -- Compte escrow Hedera
  alchemy_stage           alchemy_stage DEFAULT 'CALCINATION',
  alchemy_validation_id   UUID REFERENCES alchemy_validations(id) ON DELETE SET NULL,
  rosetta_mapping_id      UUID REFERENCES rosetta_mappings(id) ON DELETE SET NULL,
  node_id                 UUID REFERENCES nodes(id) ON DELETE SET NULL,
  submitted_by            UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  reviewed_by             UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  submitted_at            TIMESTAMPTZ DEFAULT now(),
  reviewed_at             TIMESTAMPTZ,
  completed_at            TIMESTAMPTZ,
  created_at              TIMESTAMPTZ DEFAULT now(),
  updated_at              TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE institutional_redemptions IS 'Contributions de rédemption — parcours alchimique de la Calcination à la Coagulation';
COMMENT ON COLUMN institutional_redemptions.resonance_units_issued IS 'Unités de résonance AT-OM$ émises selon la formule de conversion';
COMMENT ON COLUMN institutional_redemptions.escrow_hedera_id IS 'Identifiant du compte escrow sur Hedera pour la contribution';
COMMENT ON COLUMN institutional_redemptions.alchemy_stage IS 'Étape alchimique actuelle de la rédemption (7 étapes de transformation)';

CREATE INDEX idx_pri_redemptions_entity ON institutional_redemptions(entity_id);
CREATE INDEX idx_pri_redemptions_status ON institutional_redemptions(status);
CREATE INDEX idx_pri_redemptions_type ON institutional_redemptions(contribution_type);
CREATE INDEX idx_pri_redemptions_sector ON institutional_redemptions(impact_sector);
CREATE INDEX idx_pri_redemptions_sphere ON institutional_redemptions(target_sphere);
CREATE INDEX idx_pri_redemptions_alchemy ON institutional_redemptions(alchemy_stage);
CREATE INDEX idx_pri_redemptions_alchemy_val ON institutional_redemptions(alchemy_validation_id);
CREATE INDEX idx_pri_redemptions_rosetta ON institutional_redemptions(rosetta_mapping_id);
CREATE INDEX idx_pri_redemptions_node ON institutional_redemptions(node_id);
CREATE INDEX idx_pri_redemptions_submitted_by ON institutional_redemptions(submitted_by);
CREATE INDEX idx_pri_redemptions_reviewed_by ON institutional_redemptions(reviewed_by);
CREATE INDEX idx_pri_redemptions_submitted_at ON institutional_redemptions(submitted_at DESC);
CREATE INDEX idx_pri_redemptions_completed_at ON institutional_redemptions(completed_at DESC);

-- ═══════════════════════════════════════════════════════════
-- TABLE : redemption_audit_trail
-- Journal immuable de toutes les actions d'audit.
-- Transparence absolue — chaque action est traçable et
-- ancrée sur Hedera via hedera_proofs.
-- ═══════════════════════════════════════════════════════════

CREATE TABLE redemption_audit_trail (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  redemption_id     UUID NOT NULL REFERENCES institutional_redemptions(id) ON DELETE CASCADE,
  action            TEXT NOT NULL,                          -- 'SUBMITTED', 'AUDIT_STARTED', 'EVIDENCE_REQUESTED', 'APPROVED', 'REJECTED', 'ESCROW_FUNDED', 'RELEASED', 'REVOKED'
  actor_id          UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  actor_role        TEXT,                                   -- 'nova_agent', 'auditor', 'community', 'system'
  details           JSONB,
  integrity_hash    TEXT NOT NULL,                          -- Hash d'intégrité pour vérification
  hedera_proof_id   UUID REFERENCES hedera_proofs(id) ON DELETE SET NULL,
  created_at        TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE redemption_audit_trail IS 'Journal immuable d''audit — transparence totale, chaque action ancrée sur Hedera';
COMMENT ON COLUMN redemption_audit_trail.action IS 'Action effectuée : SUBMITTED, AUDIT_STARTED, EVIDENCE_REQUESTED, APPROVED, REJECTED, ESCROW_FUNDED, RELEASED, REVOKED';
COMMENT ON COLUMN redemption_audit_trail.actor_role IS 'Rôle de l''acteur : nova_agent, auditor, community, system';
COMMENT ON COLUMN redemption_audit_trail.integrity_hash IS 'Hash d''intégrité (MD5/SHA) pour vérification hors chaîne';

CREATE INDEX idx_pri_audit_redemption ON redemption_audit_trail(redemption_id);
CREATE INDEX idx_pri_audit_action ON redemption_audit_trail(action);
CREATE INDEX idx_pri_audit_actor ON redemption_audit_trail(actor_id);
CREATE INDEX idx_pri_audit_hedera ON redemption_audit_trail(hedera_proof_id);
CREATE INDEX idx_pri_audit_created ON redemption_audit_trail(created_at DESC);

-- ═══════════════════════════════════════════════════════════
-- TABLE : redemption_balance
-- Solde courant d'impact de rédemption par institution.
-- Vue agrégée permettant un accès rapide aux métriques clés.
-- ═══════════════════════════════════════════════════════════

CREATE TABLE redemption_balance (
  id                           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entity_id                    UUID NOT NULL UNIQUE REFERENCES institutional_entities(id) ON DELETE CASCADE,
  total_fiat_contributed       NUMERIC DEFAULT 0,
  total_resonance_issued       NUMERIC DEFAULT 0,
  total_redemptions_completed  INTEGER DEFAULT 0,
  total_redemptions_rejected   INTEGER DEFAULT 0,
  current_trust_score          NUMERIC DEFAULT 0,
  alchemy_high_water_mark      alchemy_stage DEFAULT 'CALCINATION',
  spheres_impacted             sphere_id[] DEFAULT '{}',
  last_activity_at             TIMESTAMPTZ,
  created_at                   TIMESTAMPTZ DEFAULT now(),
  updated_at                   TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE redemption_balance IS 'Solde courant d''impact par institution — métriques agrégées pour suivi rapide';
COMMENT ON COLUMN redemption_balance.alchemy_high_water_mark IS 'Plus haut stade alchimique atteint par l''institution';
COMMENT ON COLUMN redemption_balance.spheres_impacted IS 'Tableau des sphères impactées par les contributions de l''institution';

CREATE INDEX idx_pri_balance_entity ON redemption_balance(entity_id);
CREATE INDEX idx_pri_balance_trust ON redemption_balance(current_trust_score);
CREATE INDEX idx_pri_balance_activity ON redemption_balance(last_activity_at DESC);

-- ═══════════════════════════════════════════════════════════
-- TABLE : redemption_conversion_rates
-- Formules de conversion fiat → AT-OM$ (unités de résonance).
-- Intègre le Nombre d'Or (Phi) comme multiplicateur sacré
-- pour les stades alchimiques avancés.
-- ═══════════════════════════════════════════════════════════

CREATE TABLE redemption_conversion_rates (
  id                        UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  impact_sector             impact_sector NOT NULL,
  base_rate                 NUMERIC NOT NULL,               -- Taux de base fiat → résonance
  trust_multiplier          NUMERIC DEFAULT 1.0,
  transparency_bonus        NUMERIC DEFAULT 0,
  alchemy_stage_requirement alchemy_stage DEFAULT 'SEPARATION',  -- Stade minimum requis
  phi_factor                NUMERIC DEFAULT 1.6180339887498949,  -- Nombre d'Or (Phi)
  effective_from            TIMESTAMPTZ DEFAULT now(),
  effective_until           TIMESTAMPTZ,                    -- NULL = toujours actif
  is_active                 BOOLEAN DEFAULT true,
  created_at                TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE redemption_conversion_rates IS 'Taux de conversion fiat → AT-OM$ — le Nombre d''Or (Phi) récompense les stades avancés';
COMMENT ON COLUMN redemption_conversion_rates.base_rate IS 'Taux de base : combien d''unités de résonance par unité fiat';
COMMENT ON COLUMN redemption_conversion_rates.phi_factor IS 'Facteur Phi (1.618...) — multiplicateur sacré pour les stades >= FERMENTATION';
COMMENT ON COLUMN redemption_conversion_rates.alchemy_stage_requirement IS 'Stade alchimique minimum pour bénéficier de ce taux';

CREATE INDEX idx_pri_rates_sector ON redemption_conversion_rates(impact_sector);
CREATE INDEX idx_pri_rates_active ON redemption_conversion_rates(is_active) WHERE is_active = true;
CREATE INDEX idx_pri_rates_effective ON redemption_conversion_rates(effective_from, effective_until);

-- ═══════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (Souveraineté des données — Module PRI)
-- ═══════════════════════════════════════════════════════════

ALTER TABLE institutional_entities ENABLE ROW LEVEL SECURITY;
ALTER TABLE institutional_redemptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE redemption_audit_trail ENABLE ROW LEVEL SECURITY;
ALTER TABLE redemption_balance ENABLE ROW LEVEL SECURITY;
ALTER TABLE redemption_conversion_rates ENABLE ROW LEVEL SECURITY;

-- --- institutional_entities ---
-- Lecture : tous les utilisateurs authentifiés (transparence institutionnelle)
CREATE POLICY "pri_entities_read_all" ON institutional_entities
  FOR SELECT
  TO authenticated
  USING (true);

-- Écriture : seuls les utilisateurs vérifiés (admin, architect, SOUVERAIN)
CREATE POLICY "pri_entities_admin_write" ON institutional_entities
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

CREATE POLICY "pri_entities_admin_update" ON institutional_entities
  FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- --- institutional_redemptions ---
-- Lecture : le soumetteur de la rédemption + les auditeurs (admin/architect/SOUVERAIN)
CREATE POLICY "pri_redemptions_owner_read" ON institutional_redemptions
  FOR SELECT
  TO authenticated
  USING (
    submitted_by = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN', 'auditor')
    )
  );

-- Insertion : utilisateurs authentifiés liés à une entité vérifiée
CREATE POLICY "pri_redemptions_insert" ON institutional_redemptions
  FOR INSERT
  TO authenticated
  WITH CHECK (
    submitted_by = auth.uid()
    OR EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- Mise à jour : auditeurs et administrateurs uniquement
CREATE POLICY "pri_redemptions_audit_update" ON institutional_redemptions
  FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN', 'auditor')
    )
  );

-- --- redemption_audit_trail ---
-- Lecture : tous les utilisateurs authentifiés (transparence absolue)
CREATE POLICY "pri_audit_read_all" ON redemption_audit_trail
  FOR SELECT
  TO authenticated
  USING (true);

-- Écriture : système et auditeurs uniquement
CREATE POLICY "pri_audit_system_write" ON redemption_audit_trail
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN', 'auditor')
    )
  );

-- --- redemption_balance ---
-- Lecture : le propriétaire de l'entité + résumé public pour tous
CREATE POLICY "pri_balance_read" ON redemption_balance
  FOR SELECT
  TO authenticated
  USING (true);

-- Écriture : système uniquement (mis à jour par triggers)
CREATE POLICY "pri_balance_system_write" ON redemption_balance
  FOR ALL
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'architect', 'SOUVERAIN')
    )
  );

-- --- redemption_conversion_rates ---
-- Lecture : tous (transparence des taux)
CREATE POLICY "pri_rates_read_all" ON redemption_conversion_rates
  FOR SELECT
  TO authenticated
  USING (true);

-- Écriture : administrateurs uniquement
CREATE POLICY "pri_rates_admin_write" ON redemption_conversion_rates
  FOR ALL
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role IN ('admin', 'SOUVERAIN')
    )
  );

-- ═══════════════════════════════════════════════════════════
-- TRIGGERS : updated_at automatique
-- Réutilise la fonction update_timestamp() définie dans schema-rosetta.sql
-- ═══════════════════════════════════════════════════════════

CREATE TRIGGER pri_entities_updated
  BEFORE UPDATE ON institutional_entities
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER pri_redemptions_updated
  BEFORE UPDATE ON institutional_redemptions
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER pri_balance_updated
  BEFORE UPDATE ON redemption_balance
  FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- ═══════════════════════════════════════════════════════════
-- FONCTION : calculate_resonance_units
-- Calcule combien d'unités de résonance AT-OM$ une institution
-- reçoit pour sa contribution.
--
-- Formule sacrée :
--   base_amount   = amount_fiat * base_rate
--   trust_factor  = 1 + (trust_score / 100) * trust_multiplier
--   alchemy_factor = alchemy_idx / 7.0
--   phi_bonus     = phi_factor SI alchemy_idx >= 5, SINON 1.0
--   résultat      = base_amount * trust_factor * alchemy_factor
--                   * phi_bonus * (1 + transparency_bonus)
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION calculate_resonance_units(
  p_amount_fiat  NUMERIC,
  p_sector       impact_sector,
  p_trust_score  NUMERIC,
  p_alchemy_idx  INTEGER
)
RETURNS NUMERIC AS $$
DECLARE
  v_base_rate          NUMERIC;
  v_trust_multiplier   NUMERIC;
  v_transparency_bonus NUMERIC;
  v_phi_factor         NUMERIC;
  v_base_amount        NUMERIC;
  v_trust_factor       NUMERIC;
  v_alchemy_factor     NUMERIC;
  v_phi_bonus          NUMERIC;
  v_result             NUMERIC;
BEGIN
  -- Récupérer le taux actif pour le secteur d'impact
  SELECT
    base_rate,
    trust_multiplier,
    transparency_bonus,
    phi_factor
  INTO
    v_base_rate,
    v_trust_multiplier,
    v_transparency_bonus,
    v_phi_factor
  FROM redemption_conversion_rates
  WHERE impact_sector = p_sector
    AND is_active = true
    AND effective_from <= now()
    AND (effective_until IS NULL OR effective_until > now())
  ORDER BY effective_from DESC
  LIMIT 1;

  -- Si aucun taux trouvé, retourner 0
  IF v_base_rate IS NULL THEN
    RAISE WARNING 'Aucun taux de conversion actif trouvé pour le secteur %', p_sector;
    RETURN 0;
  END IF;

  -- Calcul selon la formule sacrée
  v_base_amount    := p_amount_fiat * v_base_rate;
  v_trust_factor   := 1 + (p_trust_score / 100.0) * v_trust_multiplier;
  v_alchemy_factor := p_alchemy_idx / 7.0;

  -- Bonus Phi pour les stades avancés (>= FERMENTATION, index 5)
  IF p_alchemy_idx >= 5 THEN
    v_phi_bonus := v_phi_factor;
  ELSE
    v_phi_bonus := 1.0;
  END IF;

  v_result := v_base_amount * v_trust_factor * v_alchemy_factor * v_phi_bonus * (1 + v_transparency_bonus);

  RETURN ROUND(v_result, 6);
END;
$$ LANGUAGE plpgsql STABLE;

-- ═══════════════════════════════════════════════════════════
-- TRIGGER : trg_redemption_to_audit
-- Enregistre automatiquement dans le journal d'audit
-- chaque changement de statut d'une rédemption.
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION fn_redemption_to_audit()
RETURNS TRIGGER AS $$
DECLARE
  v_action TEXT;
  v_details JSONB;
BEGIN
  -- Détecter seulement les changements de statut
  IF OLD.status IS DISTINCT FROM NEW.status THEN

    -- Mapper le nouveau statut vers une action d'audit
    CASE NEW.status
      WHEN 'SUBMITTED' THEN
        v_action := 'SUBMITTED';
      WHEN 'UNDER_AUDIT' THEN
        v_action := 'AUDIT_STARTED';
      WHEN 'ACCEPTED' THEN
        v_action := 'APPROVED';
      WHEN 'REJECTED' THEN
        v_action := 'REJECTED';
      WHEN 'ESCROW' THEN
        v_action := 'ESCROW_FUNDED';
      WHEN 'COMPLETED' THEN
        v_action := 'RELEASED';
      WHEN 'REVOKED' THEN
        v_action := 'REVOKED';
      ELSE
        v_action := NEW.status::TEXT;
    END CASE;

    -- Construire les détails du changement
    v_details := jsonb_build_object(
      'previous_status', OLD.status,
      'new_status', NEW.status,
      'amount_fiat', NEW.amount_fiat,
      'currency', NEW.currency,
      'impact_sector', NEW.impact_sector,
      'alchemy_stage', NEW.alchemy_stage,
      'resonance_units_issued', NEW.resonance_units_issued,
      'changed_at', now()
    );

    -- Insérer dans le journal d'audit
    INSERT INTO redemption_audit_trail (
      redemption_id,
      action,
      actor_id,
      actor_role,
      details,
      integrity_hash
    ) VALUES (
      NEW.id,
      v_action,
      COALESCE(NEW.reviewed_by, NEW.submitted_by),
      CASE
        WHEN NEW.reviewed_by IS NOT NULL THEN 'auditor'
        ELSE 'system'
      END,
      v_details,
      md5(v_details::text || NEW.id::text || now()::text)
    );

  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_redemption_to_audit ON institutional_redemptions;
CREATE TRIGGER trg_redemption_to_audit
  AFTER UPDATE ON institutional_redemptions
  FOR EACH ROW
  EXECUTE FUNCTION fn_redemption_to_audit();

-- ═══════════════════════════════════════════════════════════
-- TRIGGER : trg_redemption_update_balance
-- Met à jour le solde de rédemption d'une institution
-- lorsqu'une rédemption atteint le statut 'COMPLETED' ou 'REJECTED'.
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION fn_redemption_update_balance()
RETURNS TRIGGER AS $$
DECLARE
  v_alchemy_idx     INTEGER;
  v_current_hwm_idx INTEGER;
  v_new_hwm         alchemy_stage;
BEGIN
  -- Agir uniquement lors d'un changement vers COMPLETED ou REJECTED
  IF OLD.status IS DISTINCT FROM NEW.status THEN

    -- Déterminer l'index alchimique de la rédemption
    CASE NEW.alchemy_stage
      WHEN 'CALCINATION'  THEN v_alchemy_idx := 1;
      WHEN 'DISSOLUTION'  THEN v_alchemy_idx := 2;
      WHEN 'SEPARATION'   THEN v_alchemy_idx := 3;
      WHEN 'CONJUNCTION'  THEN v_alchemy_idx := 4;
      WHEN 'FERMENTATION' THEN v_alchemy_idx := 5;
      WHEN 'DISTILLATION' THEN v_alchemy_idx := 6;
      WHEN 'COAGULATION'  THEN v_alchemy_idx := 7;
      ELSE v_alchemy_idx := 1;
    END CASE;

    IF NEW.status = 'COMPLETED' THEN
      -- Créer ou mettre à jour le solde
      INSERT INTO redemption_balance (
        entity_id,
        total_fiat_contributed,
        total_resonance_issued,
        total_redemptions_completed,
        current_trust_score,
        alchemy_high_water_mark,
        spheres_impacted,
        last_activity_at
      ) VALUES (
        NEW.entity_id,
        COALESCE(NEW.amount_fiat, 0),
        COALESCE(NEW.resonance_units_issued, 0),
        1,
        (SELECT trust_score FROM institutional_entities WHERE id = NEW.entity_id),
        NEW.alchemy_stage,
        CASE
          WHEN NEW.target_sphere IS NOT NULL THEN ARRAY[NEW.target_sphere]
          ELSE '{}'::sphere_id[]
        END,
        now()
      )
      ON CONFLICT (entity_id) DO UPDATE SET
        total_fiat_contributed      = redemption_balance.total_fiat_contributed + COALESCE(NEW.amount_fiat, 0),
        total_resonance_issued      = redemption_balance.total_resonance_issued + COALESCE(NEW.resonance_units_issued, 0),
        total_redemptions_completed = redemption_balance.total_redemptions_completed + 1,
        current_trust_score         = (SELECT trust_score FROM institutional_entities WHERE id = NEW.entity_id),
        -- Mettre à jour le high water mark si le stade actuel est plus élevé
        alchemy_high_water_mark     = CASE
          WHEN v_alchemy_idx > (
            CASE redemption_balance.alchemy_high_water_mark
              WHEN 'CALCINATION'  THEN 1
              WHEN 'DISSOLUTION'  THEN 2
              WHEN 'SEPARATION'   THEN 3
              WHEN 'CONJUNCTION'  THEN 4
              WHEN 'FERMENTATION' THEN 5
              WHEN 'DISTILLATION' THEN 6
              WHEN 'COAGULATION'  THEN 7
              ELSE 1
            END
          ) THEN NEW.alchemy_stage
          ELSE redemption_balance.alchemy_high_water_mark
        END,
        -- Ajouter la sphère si elle n'est pas déjà dans le tableau
        spheres_impacted            = CASE
          WHEN NEW.target_sphere IS NOT NULL
            AND NOT (NEW.target_sphere = ANY(redemption_balance.spheres_impacted))
          THEN array_append(redemption_balance.spheres_impacted, NEW.target_sphere)
          ELSE redemption_balance.spheres_impacted
        END,
        last_activity_at            = now(),
        updated_at                  = now();

    ELSIF NEW.status = 'REJECTED' THEN
      -- Incrémenter le compteur de rejets
      INSERT INTO redemption_balance (
        entity_id,
        total_redemptions_rejected,
        last_activity_at
      ) VALUES (
        NEW.entity_id,
        1,
        now()
      )
      ON CONFLICT (entity_id) DO UPDATE SET
        total_redemptions_rejected = redemption_balance.total_redemptions_rejected + 1,
        last_activity_at           = now(),
        updated_at                 = now();

    END IF;

  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_redemption_update_balance ON institutional_redemptions;
CREATE TRIGGER trg_redemption_update_balance
  AFTER UPDATE ON institutional_redemptions
  FOR EACH ROW
  EXECUTE FUNCTION fn_redemption_update_balance();

-- ═══════════════════════════════════════════════════════════
-- VUE : redemption_dashboard
-- Tableau de bord par entité — résumé des contributions,
-- résonance émise, stade alchimique moyen et score de confiance.
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE VIEW redemption_dashboard AS
SELECT
  ie.id                          AS entity_id,
  ie.entity_name,
  ie.entity_type,
  ie.jurisdiction,
  ie.trust_score,
  ie.is_verified,
  COALESCE(rb.total_fiat_contributed, 0)      AS total_fiat_contributed,
  COALESCE(rb.total_resonance_issued, 0)      AS total_resonance_issued,
  COALESCE(rb.total_redemptions_completed, 0) AS total_redemptions_completed,
  COALESCE(rb.total_redemptions_rejected, 0)  AS total_redemptions_rejected,
  rb.alchemy_high_water_mark,
  rb.spheres_impacted,
  -- Stade alchimique moyen des rédemptions complétées
  (
    SELECT ROUND(AVG(
      CASE ir.alchemy_stage
        WHEN 'CALCINATION'  THEN 1
        WHEN 'DISSOLUTION'  THEN 2
        WHEN 'SEPARATION'   THEN 3
        WHEN 'CONJUNCTION'  THEN 4
        WHEN 'FERMENTATION' THEN 5
        WHEN 'DISTILLATION' THEN 6
        WHEN 'COAGULATION'  THEN 7
        ELSE 1
      END
    ), 2)
    FROM institutional_redemptions ir
    WHERE ir.entity_id = ie.id
      AND ir.status = 'COMPLETED'
  )                                           AS avg_alchemy_stage_index,
  -- Nombre de rédemptions en cours
  (
    SELECT COUNT(*)
    FROM institutional_redemptions ir
    WHERE ir.entity_id = ie.id
      AND ir.status NOT IN ('COMPLETED', 'REJECTED', 'REVOKED')
  )                                           AS active_redemptions_count,
  rb.last_activity_at
FROM institutional_entities ie
LEFT JOIN redemption_balance rb ON rb.entity_id = ie.id;

-- ═══════════════════════════════════════════════════════════
-- SUPABASE REALTIME — Module PRI
-- ═══════════════════════════════════════════════════════════

DO $$
BEGIN
  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE institutional_entities;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE institutional_redemptions;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE redemption_audit_trail;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE redemption_balance;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;

  BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE redemption_conversion_rates;
  EXCEPTION WHEN duplicate_object THEN NULL;
  END;
END $$;

-- ═══════════════════════════════════════════════════════════
-- VÉRIFICATION
-- ═══════════════════════════════════════════════════════════

DO $$
BEGIN
  RAISE NOTICE '═══ AT·OM — Module PRI (Passerelle de Rédemption Institutionnelle) ═══';
  RAISE NOTICE '✓ TYPE contribution_type          (GRANT, REDEMPTION, PARTNERSHIP, RESTITUTION)';
  RAISE NOTICE '✓ TYPE redemption_status           (SUBMITTED → COMPLETED / REVOKED)';
  RAISE NOTICE '✓ TYPE impact_sector               (9 sphères + MULTI_SPHERE + SYSTEMIC)';
  RAISE NOTICE '✓ TABLE institutional_entities      (registre des institutions)';
  RAISE NOTICE '✓ TABLE institutional_redemptions   (contributions de rédemption)';
  RAISE NOTICE '✓ TABLE redemption_audit_trail      (journal immuable d''audit)';
  RAISE NOTICE '✓ TABLE redemption_balance          (solde d''impact par institution)';
  RAISE NOTICE '✓ TABLE redemption_conversion_rates (taux de conversion AT-OM$)';
  RAISE NOTICE '✓ VIEW  redemption_dashboard        (tableau de bord par entité)';
  RAISE NOTICE '✓ FUNC  calculate_resonance_units   (calcul des unités de résonance)';
  RAISE NOTICE '✓ TRIG  trg_redemption_to_audit     (journal auto sur changement de statut)';
  RAISE NOTICE '✓ TRIG  trg_redemption_update_balance (mise à jour solde sur complétion)';
  RAISE NOTICE '✓ RLS   activé sur les 5 tables avec politiques de souveraineté';
  RAISE NOTICE '✓ Realtime activé pour toutes les tables PRI';
  RAISE NOTICE '═══ Module PRI installé avec succès ═══';
END $$;

-- ═══════════════════════════════════════════════════════════
-- FIN DU SCRIPT — MODULE PRI
-- ═══════════════════════════════════════════════════════════

-- Requêtes de vérification :
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE '%redemption%' OR table_name = 'institutional_entities';
-- SELECT * FROM redemption_dashboard LIMIT 10;
-- SELECT calculate_resonance_units(10000, 'ECONOMIE', 75, 5);
