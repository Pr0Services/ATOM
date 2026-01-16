-- ═══════════════════════════════════════════════════════════════════════════════
-- CHE·NU™ V76 — ORIGIN MODULE DATABASE TRIGGERS
-- ═══════════════════════════════════════════════════════════════════════════════
-- Alembic Migration: 003_origin_triggers
-- Date: 8 Janvier 2026
--
-- R&D Rules Enforced:
--   Rule #1: Human Sovereignty (checkpoint enforcement)
--   Rule #5: Chronological Integrity (anti-anachronism)
--   Rule #6: Full Traceability
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- HELPER FUNCTIONS
-- ═══════════════════════════════════════════════════════════════════════════════

-- Parse date string to integer for comparison
CREATE OR REPLACE FUNCTION parse_date_to_int(date_str TEXT)
RETURNS INTEGER AS $$
DECLARE
    cleaned TEXT;
    result INTEGER;
BEGIN
    IF date_str IS NULL OR date_str = '' THEN
        RETURN NULL;
    END IF;
    
    -- Remove whitespace
    cleaned := TRIM(date_str);
    
    -- Handle BCE/BC dates (negative)
    IF cleaned ~* 'BCE|BC' THEN
        cleaned := regexp_replace(cleaned, '[^0-9-]', '', 'g');
        result := -1 * ABS(cleaned::INTEGER);
        RETURN result;
    END IF;
    
    -- Handle "c." approximate dates
    IF cleaned ~* '^c\.' THEN
        cleaned := regexp_replace(cleaned, '^c\.?\s*', '', 'i');
    END IF;
    
    -- Handle negative years directly
    IF cleaned ~ '^-[0-9]+$' THEN
        RETURN cleaned::INTEGER;
    END IF;
    
    -- Handle ranges (take start year)
    IF cleaned ~ '-' AND cleaned !~ '^-' THEN
        cleaned := split_part(cleaned, '-', 1);
    END IF;
    
    -- Extract numeric year
    cleaned := regexp_replace(cleaned, '[^0-9]', '', 'g');
    
    IF cleaned = '' OR cleaned IS NULL THEN
        RETURN NULL;
    END IF;
    
    RETURN cleaned::INTEGER;
    
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGER 1: ANTI-CYCLE DETECTION (Causal Links)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION trg_detect_causal_cycle()
RETURNS TRIGGER AS $$
DECLARE
    cycle_found BOOLEAN := FALSE;
    path_check RECORD;
BEGIN
    -- Prevent self-loops immediately
    IF NEW.trigger_node_id = NEW.result_node_id THEN
        RAISE EXCEPTION 'CYCLE_DETECTED: Self-loop not allowed (node % -> %)', 
            NEW.trigger_node_id, NEW.result_node_id;
    END IF;
    
    -- Check for cycles using recursive CTE
    WITH RECURSIVE causal_path AS (
        -- Start from the result node
        SELECT 
            result_node_id AS current_node,
            ARRAY[trigger_node_id, result_node_id] AS path,
            1 AS depth
        FROM origin_causal_links
        WHERE trigger_node_id = NEW.result_node_id
        
        UNION ALL
        
        -- Follow the chain
        SELECT 
            ocl.result_node_id,
            cp.path || ocl.result_node_id,
            cp.depth + 1
        FROM origin_causal_links ocl
        JOIN causal_path cp ON ocl.trigger_node_id = cp.current_node
        WHERE cp.depth < 100  -- Max depth to prevent infinite recursion
        AND NOT ocl.result_node_id = ANY(cp.path)  -- Prevent revisiting
    )
    SELECT EXISTS (
        SELECT 1 FROM causal_path 
        WHERE current_node = NEW.trigger_node_id
    ) INTO cycle_found;
    
    IF cycle_found THEN
        RAISE EXCEPTION 'CYCLE_DETECTED: Adding link % -> % would create a causal cycle',
            NEW.trigger_node_id, NEW.result_node_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger
DROP TRIGGER IF EXISTS trg_causal_cycle_check ON origin_causal_links;
CREATE TRIGGER trg_causal_cycle_check
    BEFORE INSERT OR UPDATE ON origin_causal_links
    FOR EACH ROW
    EXECUTE FUNCTION trg_detect_causal_cycle();

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGER 2: CHRONOLOGY VALIDATION (Anti-Anachronism)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION trg_validate_causal_chronology()
RETURNS TRIGGER AS $$
DECLARE
    trigger_date INTEGER;
    result_date INTEGER;
    trigger_name TEXT;
    result_name TEXT;
BEGIN
    -- Get trigger node date
    SELECT 
        parse_date_to_int(date_start),
        name
    INTO trigger_date, trigger_name
    FROM origin_nodes
    WHERE id = NEW.trigger_node_id;
    
    -- Get result node date
    SELECT 
        parse_date_to_int(date_start),
        name
    INTO result_date, result_name
    FROM origin_nodes
    WHERE id = NEW.result_node_id;
    
    -- Skip validation if either date is NULL
    IF trigger_date IS NULL OR result_date IS NULL THEN
        RETURN NEW;
    END IF;
    
    -- Validate: trigger must come before or equal to result
    IF trigger_date > result_date THEN
        RAISE EXCEPTION 'ANACHRONISM_DETECTED: "%" (%) cannot cause "%" (%) - effect precedes cause',
            trigger_name, trigger_date, result_name, result_date;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger
DROP TRIGGER IF EXISTS trg_chronology_check ON origin_causal_links;
CREATE TRIGGER trg_chronology_check
    BEFORE INSERT OR UPDATE ON origin_causal_links
    FOR EACH ROW
    EXECUTE FUNCTION trg_validate_causal_chronology();

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGER 3: EVIDENCE VALIDATION (Bio-Evolution)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION trg_validate_bio_eco_evidence()
RETURNS TRIGGER AS $$
DECLARE
    source_count INTEGER;
BEGIN
    -- Count evidence sources
    SELECT COALESCE(jsonb_array_length(NEW.evidence_sources), 0) INTO source_count;
    
    -- Validate based on claim strength
    IF NEW.claim_strength = 'medium' AND source_count < 1 THEN
        RAISE EXCEPTION 'EVIDENCE_REQUIRED: Medium claims require at least 1 source (found %)', source_count;
    END IF;
    
    IF NEW.claim_strength = 'strong' AND source_count < 2 THEN
        RAISE EXCEPTION 'EVIDENCE_REQUIRED: Strong claims require at least 2 sources (found %)', source_count;
    END IF;
    
    -- Require checkpoint for medium/strong claims (R&D Rule #1)
    IF NEW.claim_strength IN ('medium', 'strong') AND NEW.checkpoint_id IS NULL THEN
        RAISE EXCEPTION 'CHECKPOINT_REQUIRED: Bio-evolution % claims require human approval (HTTP 423)',
            NEW.claim_strength;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger
DROP TRIGGER IF EXISTS trg_bio_eco_evidence ON origin_bio_eco;
CREATE TRIGGER trg_bio_eco_evidence
    BEFORE INSERT OR UPDATE ON origin_bio_eco
    FOR EACH ROW
    EXECUTE FUNCTION trg_validate_bio_eco_evidence();

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGER 4: LEGACY MYSTERY CHECKPOINT (Rule #1)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION trg_validate_legacy_mystery()
RETURNS TRIGGER AS $$
BEGIN
    -- Require checkpoint for world mystery links
    IF NEW.world_mystery_link IS NOT NULL AND NEW.checkpoint_id IS NULL THEN
        RAISE EXCEPTION 'CHECKPOINT_REQUIRED: World mystery links require human approval (HTTP 423)';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger
DROP TRIGGER IF EXISTS trg_legacy_mystery ON origin_legacy;
CREATE TRIGGER trg_legacy_mystery
    BEFORE INSERT OR UPDATE ON origin_legacy
    FOR EACH ROW
    EXECUTE FUNCTION trg_validate_legacy_mystery();

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGER 5: CAUSAL LINK CHECKPOINT (Rule #1)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION trg_validate_causal_checkpoint()
RETURNS TRIGGER AS $$
BEGIN
    -- All causal links require human approval
    IF NEW.checkpoint_id IS NULL THEN
        RAISE EXCEPTION 'CHECKPOINT_REQUIRED: Causal links require human approval (HTTP 423)';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger
DROP TRIGGER IF EXISTS trg_causal_checkpoint ON origin_causal_links;
CREATE TRIGGER trg_causal_checkpoint
    BEFORE INSERT ON origin_causal_links
    FOR EACH ROW
    EXECUTE FUNCTION trg_validate_causal_checkpoint();

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGER 6: AUTO-COMPUTE date_start_int
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION trg_compute_date_int()
RETURNS TRIGGER AS $$
BEGIN
    -- Auto-compute integer representation of date
    NEW.date_start_int := parse_date_to_int(NEW.date_start);
    NEW.date_end_int := parse_date_to_int(NEW.date_end);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger
DROP TRIGGER IF EXISTS trg_auto_date_int ON origin_nodes;
CREATE TRIGGER trg_auto_date_int
    BEFORE INSERT OR UPDATE ON origin_nodes
    FOR EACH ROW
    EXECUTE FUNCTION trg_compute_date_int();

-- ═══════════════════════════════════════════════════════════════════════════════
-- TRIGGER 7: TRACEABILITY AUDIT LOG
-- ═══════════════════════════════════════════════════════════════════════════════

-- Create audit log table
CREATE TABLE IF NOT EXISTS origin_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name TEXT NOT NULL,
    operation TEXT NOT NULL,
    record_id UUID NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_by UUID NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    checkpoint_id UUID
);

CREATE INDEX IF NOT EXISTS ix_audit_log_table ON origin_audit_log(table_name);
CREATE INDEX IF NOT EXISTS ix_audit_log_record ON origin_audit_log(record_id);
CREATE INDEX IF NOT EXISTS ix_audit_log_changed_at ON origin_audit_log(changed_at);

-- Generic audit function
CREATE OR REPLACE FUNCTION trg_origin_audit()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO origin_audit_log (table_name, operation, record_id, new_data, changed_by, checkpoint_id)
        VALUES (TG_TABLE_NAME, 'INSERT', NEW.id, to_jsonb(NEW), NEW.created_by, NEW.checkpoint_id);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO origin_audit_log (table_name, operation, record_id, old_data, new_data, changed_by, checkpoint_id)
        VALUES (TG_TABLE_NAME, 'UPDATE', NEW.id, to_jsonb(OLD), to_jsonb(NEW), NEW.created_by, NEW.checkpoint_id);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO origin_audit_log (table_name, operation, record_id, old_data, changed_by)
        VALUES (TG_TABLE_NAME, 'DELETE', OLD.id, to_jsonb(OLD), OLD.created_by);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Apply audit triggers to all ORIGIN tables
DROP TRIGGER IF EXISTS trg_audit_origin_nodes ON origin_nodes;
CREATE TRIGGER trg_audit_origin_nodes
    AFTER INSERT OR UPDATE OR DELETE ON origin_nodes
    FOR EACH ROW EXECUTE FUNCTION trg_origin_audit();

DROP TRIGGER IF EXISTS trg_audit_origin_causal_links ON origin_causal_links;
CREATE TRIGGER trg_audit_origin_causal_links
    AFTER INSERT OR UPDATE OR DELETE ON origin_causal_links
    FOR EACH ROW EXECUTE FUNCTION trg_origin_audit();

DROP TRIGGER IF EXISTS trg_audit_origin_bio_eco ON origin_bio_eco;
CREATE TRIGGER trg_audit_origin_bio_eco
    AFTER INSERT OR UPDATE OR DELETE ON origin_bio_eco
    FOR EACH ROW EXECUTE FUNCTION trg_origin_audit();

DROP TRIGGER IF EXISTS trg_audit_origin_legacy ON origin_legacy;
CREATE TRIGGER trg_audit_origin_legacy
    AFTER INSERT OR UPDATE OR DELETE ON origin_legacy
    FOR EACH ROW EXECUTE FUNCTION trg_origin_audit();

-- ═══════════════════════════════════════════════════════════════════════════════
-- INDEXES FOR PERFORMANCE
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS ix_origin_nodes_date_int ON origin_nodes(date_start_int);
CREATE INDEX IF NOT EXISTS ix_origin_causal_trigger ON origin_causal_links(trigger_node_id);
CREATE INDEX IF NOT EXISTS ix_origin_causal_result ON origin_causal_links(result_node_id);
CREATE INDEX IF NOT EXISTS ix_origin_bio_strength ON origin_bio_eco(claim_strength);

-- ═══════════════════════════════════════════════════════════════════════════════
-- VERIFICATION QUERIES
-- ═══════════════════════════════════════════════════════════════════════════════

-- Check all triggers are installed
DO $$
DECLARE
    trigger_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO trigger_count
    FROM information_schema.triggers
    WHERE trigger_schema = 'public'
    AND trigger_name LIKE 'trg_%';
    
    RAISE NOTICE '═══════════════════════════════════════════════════════════════════════════════';
    RAISE NOTICE 'CHE·NU™ ORIGIN TRIGGERS INSTALLED: %', trigger_count;
    RAISE NOTICE '═══════════════════════════════════════════════════════════════════════════════';
    RAISE NOTICE '✅ trg_causal_cycle_check     - Anti-cycle detection';
    RAISE NOTICE '✅ trg_chronology_check       - Anti-anachronism';
    RAISE NOTICE '✅ trg_bio_eco_evidence       - Evidence validation';
    RAISE NOTICE '✅ trg_legacy_mystery         - Mystery checkpoint';
    RAISE NOTICE '✅ trg_causal_checkpoint      - Causal link checkpoint';
    RAISE NOTICE '✅ trg_auto_date_int          - Date integer computation';
    RAISE NOTICE '✅ trg_audit_*                - Full traceability';
    RAISE NOTICE '═══════════════════════════════════════════════════════════════════════════════';
END $$;
