-- ═══════════════════════════════════════════════════════════
-- AT·OM — Triggers d'Automation
-- Enrichissement automatique des données entre les schémas
-- ═══════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════
-- TRIGGER 1 : agent_outputs validé → rosetta_mappings
-- Quand un output d'agent est validé, créer automatiquement
-- une traduction Rosetta tri-dimensionnelle.
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION fn_agent_output_to_rosetta()
RETURNS TRIGGER AS $$
DECLARE
  v_narrative TEXT;
  v_mapping_id UUID;
BEGIN
  -- Seulement quand validated passe à TRUE
  IF NEW.validated = TRUE AND (OLD.validated IS NULL OR OLD.validated = FALSE) THEN

    -- Synthétiser la narrative depuis les messages agent liés
    SELECT string_agg(content, ' ')
    INTO v_narrative
    FROM agent_messages
    WHERE instance_id = NEW.instance_id
      AND sender_type = 'agent'
    ORDER BY created_at
    LIMIT 5;

    -- Créer le mapping Rosetta
    INSERT INTO rosetta_mappings (
      node_id,
      tech_payload,
      people_narrative,
      people_explanation,
      people_tone,
      spirit_payload,
      source_dimension,
      integrity_hash
    ) VALUES (
      -- node_id : utiliser le context_id de l'instance si c'est un UUID valide
      COALESCE(
        (SELECT context_id FROM agent_instances WHERE id = NEW.instance_id),
        gen_random_uuid()
      ),
      -- tech_payload : le contenu de l'output
      COALESCE(NEW.content, '{}'::jsonb),
      -- people_narrative
      COALESCE(v_narrative, 'Output d''agent validé automatiquement.'),
      -- people_explanation
      'Traduction automatique générée par le trigger Rosetta.',
      -- people_tone basé sur la confiance
      CASE
        WHEN NEW.confidence >= 0.9 THEN 'celebratoire'::emotional_tone
        WHEN NEW.confidence >= 0.7 THEN 'encourageant'::emotional_tone
        WHEN NEW.confidence >= 0.4 THEN 'neutre'::emotional_tone
        ELSE 'alerte'::emotional_tone
      END,
      -- spirit_payload
      jsonb_build_object(
        'frequency_hz', 444,
        'resonance_level', 4,
        'color', '#50C878',
        'sacred_geometry', 'tetrahedron',
        'vibration_signature', ARRAY[44.4, 161.8, 369.0, 1728.0],
        'phi_ratio', 1.6180339887498949
      ),
      'TECH'::rosetta_dimension,
      md5(NEW.content::text)
    )
    RETURNING id INTO v_mapping_id;

    -- Lier l'output au mapping
    UPDATE agent_outputs
    SET rosetta_mapping_id = v_mapping_id
    WHERE id = NEW.id;

  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_agent_output_to_rosetta ON agent_outputs;
CREATE TRIGGER trg_agent_output_to_rosetta
  AFTER UPDATE ON agent_outputs
  FOR EACH ROW
  EXECUTE FUNCTION fn_agent_output_to_rosetta();

-- ═══════════════════════════════════════════════════════════
-- TRIGGER 2 : founder_ux_metrics → vibrational_logs
-- Chaque session UX génère un log vibrationnel.
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION fn_ux_metrics_to_viblog()
RETURNS TRIGGER AS $$
DECLARE
  v_base_freq NUMERIC := 444;
  v_freq NUMERIC;
  v_level INTEGER;
  v_log_id UUID;
BEGIN
  -- Calculer la fréquence basée sur l'engagement
  -- Plus d'interactions = plus haute fréquence
  v_freq := v_base_freq + LEAST(NEW.interactions * 5.55, 555);
  v_freq := GREATEST(111, LEAST(999, v_freq));
  v_level := GREATEST(1, LEAST(9, ROUND(v_freq / 111)));

  INSERT INTO vibrational_logs (
    user_id,
    frequency_hz,
    resonance_level,
    mode,
    metadata,
    created_at
  ) VALUES (
    NEW.user_id,
    v_level * 111,  -- Snap au palier
    v_level,
    'standard',
    jsonb_build_object(
      'source', 'ux_metrics',
      'time_spent', NEW.time_spent_seconds,
      'scroll_depth', NEW.scroll_depth,
      'interactions', NEW.interactions,
      'section', NEW.section_id
    ),
    NEW.created_at
  )
  RETURNING id INTO v_log_id;

  -- Lier le metric au log
  UPDATE founder_ux_metrics
  SET vibrational_log_id = v_log_id
  WHERE id = NEW.id;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_ux_metrics_to_viblog ON founder_ux_metrics;
CREATE TRIGGER trg_ux_metrics_to_viblog
  AFTER INSERT ON founder_ux_metrics
  FOR EACH ROW
  EXECUTE FUNCTION fn_ux_metrics_to_viblog();

-- ═══════════════════════════════════════════════════════════
-- TRIGGER 3 : agent_outputs.confidence → alchemy_validations
-- Mapper automatiquement la confiance aux 7 étapes alchimiques.
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION fn_confidence_to_alchemy()
RETURNS TRIGGER AS $$
DECLARE
  v_stage alchemy_stage;
  v_stage_idx INTEGER;
  v_node_id UUID;
BEGIN
  -- Déterminer le stage basé sur la confiance
  IF NEW.confidence >= 0.90 THEN
    v_stage := 'COAGULATION'; v_stage_idx := 7;
  ELSIF NEW.confidence >= 0.80 THEN
    v_stage := 'DISTILLATION'; v_stage_idx := 6;
  ELSIF NEW.confidence >= 0.70 THEN
    v_stage := 'FERMENTATION'; v_stage_idx := 5;
  ELSIF NEW.confidence >= 0.55 THEN
    v_stage := 'CONJUNCTION'; v_stage_idx := 4;
  ELSIF NEW.confidence >= 0.45 THEN
    v_stage := 'SEPARATION'; v_stage_idx := 3;
  ELSIF NEW.confidence >= 0.30 THEN
    v_stage := 'DISSOLUTION'; v_stage_idx := 2;
  ELSE
    v_stage := 'CALCINATION'; v_stage_idx := 1;
  END IF;

  -- Récupérer le node_id depuis l'instance
  SELECT context_id INTO v_node_id
  FROM agent_instances
  WHERE id = NEW.instance_id;

  -- Ne créer la validation que si on a un node_id valide
  IF v_node_id IS NOT NULL THEN
    INSERT INTO alchemy_validations (
      node_id,
      current_stage,
      stage_index,
      is_aligned,
      polishing_notes
    ) VALUES (
      v_node_id,
      v_stage,
      v_stage_idx,
      v_stage_idx >= 7,
      ARRAY[
        'Confiance agent: ' || ROUND(NEW.confidence::numeric, 2)::text,
        'Stage assigné automatiquement par trigger'
      ]
    )
    ON CONFLICT (node_id) DO UPDATE SET
      current_stage = EXCLUDED.current_stage,
      stage_index = EXCLUDED.stage_index,
      is_aligned = EXCLUDED.is_aligned,
      polishing_notes = alchemy_validations.polishing_notes || EXCLUDED.polishing_notes,
      updated_at = NOW();

    -- Mettre à jour le stage sur l'output
    UPDATE agent_outputs
    SET alchemy_stage = v_stage
    WHERE id = NEW.id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_confidence_to_alchemy ON agent_outputs;
CREATE TRIGGER trg_confidence_to_alchemy
  AFTER INSERT ON agent_outputs
  FOR EACH ROW
  WHEN (NEW.confidence IS NOT NULL)
  EXECUTE FUNCTION fn_confidence_to_alchemy();

-- ═══════════════════════════════════════════════════════════
-- TRIGGER 4 : nodes → spiral_positions (Disque de Phaistos)
-- Chaque node reçoit automatiquement une position spiralée.
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION fn_node_to_spiral()
RETURNS TRIGGER AS $$
DECLARE
  v_angle NUMERIC;
  v_ring INTEGER;
  v_distance NUMERIC;
BEGIN
  -- Ring = profondeur dans l'arbre (capped à 12)
  v_ring := LEAST(COALESCE(NEW.depth, 0), 12);

  -- Angle déterministe basé sur le hash du titre
  v_angle := (
    ('x' || substring(md5(COALESCE(NEW.title, 'untitled')), 1, 8))::bit(32)::int::numeric
    / 2147483647.0
  ) * 2 * 3.14159265358979;

  -- Distance à l'essence = 1 - (resonance_level / 9)
  v_distance := 1.0 - (COALESCE(NEW.resonance_level, 1)::numeric / 9.0);

  INSERT INTO spiral_positions (node_id, ring, angle, depth, essence_distance)
  VALUES (NEW.id, v_ring, v_angle, COALESCE(NEW.depth, 0), v_distance)
  ON CONFLICT (node_id) DO UPDATE SET
    ring = v_ring,
    angle = v_angle,
    depth = COALESCE(NEW.depth, 0),
    essence_distance = v_distance;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_node_to_spiral ON nodes;
CREATE TRIGGER trg_node_to_spiral
  AFTER INSERT OR UPDATE ON nodes
  FOR EACH ROW
  EXECUTE FUNCTION fn_node_to_spiral();

-- ═══════════════════════════════════════════════════════════
-- TRIGGER 5 : nodes INSERT → gear_events (Machine d'Anticythère)
-- Quand un node est créé dans une sphère, propager
-- l'événement vers les sphères connectées.
-- ═══════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION fn_node_to_gear_event()
RETURNS TRIGGER AS $$
DECLARE
  v_connections sphere_id[];
BEGIN
  -- Mapper les connexions d'engrenages par sphère
  -- (miroir de SPHERES[x].gear_connections dans atom-types.ts)
  CASE NEW.sphere_id
    WHEN 'TECHNO' THEN
      v_connections := ARRAY['ECONOMIE', 'EDUCATION', 'SANTE']::sphere_id[];
    WHEN 'POLITIQUE' THEN
      v_connections := ARRAY['JUSTICE', 'ECONOMIE', 'ENVIRONNEMENT']::sphere_id[];
    WHEN 'ECONOMIE' THEN
      v_connections := ARRAY['TECHNO', 'POLITIQUE', 'CULTURE']::sphere_id[];
    WHEN 'EDUCATION' THEN
      v_connections := ARRAY['TECHNO', 'CULTURE', 'SPIRITUALITE']::sphere_id[];
    WHEN 'SANTE' THEN
      v_connections := ARRAY['TECHNO', 'ENVIRONNEMENT', 'SPIRITUALITE']::sphere_id[];
    WHEN 'CULTURE' THEN
      v_connections := ARRAY['ECONOMIE', 'EDUCATION', 'SPIRITUALITE']::sphere_id[];
    WHEN 'ENVIRONNEMENT' THEN
      v_connections := ARRAY['POLITIQUE', 'SANTE', 'JUSTICE']::sphere_id[];
    WHEN 'JUSTICE' THEN
      v_connections := ARRAY['POLITIQUE', 'ENVIRONNEMENT', 'SPIRITUALITE']::sphere_id[];
    WHEN 'SPIRITUALITE' THEN
      v_connections := ARRAY['EDUCATION', 'SANTE', 'CULTURE', 'JUSTICE']::sphere_id[];
    ELSE
      v_connections := ARRAY[]::sphere_id[];
  END CASE;

  -- Créer l'événement d'engrenage
  IF array_length(v_connections, 1) > 0 THEN
    INSERT INTO gear_events (
      source_sphere,
      target_spheres,
      event_type,
      payload,
      propagation_depth
    ) VALUES (
      NEW.sphere_id,
      v_connections,
      'resonance'::gear_event_type,
      jsonb_build_object(
        'trigger', 'node_creation',
        'node_id', NEW.id,
        'node_title', NEW.title,
        'resonance_level', NEW.resonance_level,
        'status', NEW.status
      ),
      1
    );
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_node_to_gear ON nodes;
CREATE TRIGGER trg_node_to_gear
  AFTER INSERT ON nodes
  FOR EACH ROW
  EXECUTE FUNCTION fn_node_to_gear_event();

-- ═══════════════════════════════════════════════════════════
-- VÉRIFICATION
-- ═══════════════════════════════════════════════════════════

DO $$
BEGIN
  RAISE NOTICE '═══ AT·OM Triggers Automation ═══';
  RAISE NOTICE '✓ trg_agent_output_to_rosetta  (agent_outputs → rosetta_mappings)';
  RAISE NOTICE '✓ trg_ux_metrics_to_viblog     (founder_ux_metrics → vibrational_logs)';
  RAISE NOTICE '✓ trg_confidence_to_alchemy    (agent_outputs → alchemy_validations)';
  RAISE NOTICE '✓ trg_node_to_spiral           (nodes → spiral_positions)';
  RAISE NOTICE '✓ trg_node_to_gear             (nodes → gear_events)';
  RAISE NOTICE '═══ 5 triggers installés ═══';
END $$;
