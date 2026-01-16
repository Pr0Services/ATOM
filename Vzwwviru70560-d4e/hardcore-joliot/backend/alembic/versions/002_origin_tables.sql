-- ═══════════════════════════════════════════════════════════════════════════════
-- CHE·NU™ V76 — ORIGIN MODULE DATABASE SCHEMA
-- ═══════════════════════════════════════════════════════════════════════════════
-- Tables pour le module ORIGIN-GENESIS-ULTIMA
-- Agent A: Préparé pour l'intégration par Agent B
-- 
-- TABLES:
--   1. origin_nodes          - Nœuds principaux (technologies, découvertes)
--   2. origin_causal_links   - Liens causaux (trigger → result)
--   3. origin_universal_links - Liens multi-entités pour visualisation
--   4. origin_media_assets   - Assets média (scripts, chapitres, etc.)
--   5. origin_civilization   - Piliers de civilisation
--   6. origin_customs        - Évolution des coutumes
--   7. origin_legacy         - Héritage humain (croyances, corps, planète)
--   8. origin_bio_eco        - Co-évolution gène-culture
-- ═══════════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════════
-- 1. ORIGIN NODES (Core)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS origin_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    
    -- Temporal fields (flexible dates)
    epoch VARCHAR(100),                            -- "Prehistoric", "Ancient", "Medieval", etc.
    exact_date VARCHAR(50),                        -- "c.1450", "1939", "-3000"
    date_start VARCHAR(50),                        -- Sortable boundary start
    date_end VARCHAR(50),                          -- Sortable boundary end
    date_start_int INTEGER,                        -- Parsed integer for comparisons (Agent A requirement)
    date_end_int INTEGER,                          -- Parsed integer for comparisons
    date_certainty FLOAT DEFAULT 0.8 NOT NULL,    -- 0.0 to 1.0
    
    description TEXT,
    
    -- JSON metadata
    metadata_json JSONB,                           -- {sources:[], shadow_contributors:[], tech_specs:[], tags:[]}
    geopolitical_context JSONB,                    -- {power_shift:"", conflicts:[], trade:[], societal_effects:[]}
    
    -- Validation lifecycle
    is_validated BOOLEAN DEFAULT FALSE NOT NULL,
    validated_by JSONB,                            -- {agent_ids:[], method:"", timestamp:""}
    
    -- R&D Rule #6: Traceability
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Soft delete
    is_deleted BOOLEAN DEFAULT FALSE NOT NULL,
    deleted_at TIMESTAMPTZ,
    deleted_by VARCHAR(50)
);

CREATE INDEX idx_origin_nodes_name ON origin_nodes(name);
CREATE INDEX idx_origin_nodes_epoch ON origin_nodes(epoch);
CREATE INDEX idx_origin_nodes_name_epoch ON origin_nodes(name, epoch);
CREATE INDEX idx_origin_nodes_date_start_int ON origin_nodes(date_start_int);
CREATE INDEX idx_origin_nodes_validated ON origin_nodes(is_validated);

CREATE TRIGGER update_origin_nodes_updated_at BEFORE UPDATE ON origin_nodes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ═══════════════════════════════════════════════════════════════════════════════
-- 2. CAUSAL LINKS (R&D Rule #1: Checkpoint required)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS origin_causal_links (
    trigger_id UUID NOT NULL REFERENCES origin_nodes(id) ON DELETE CASCADE,
    result_id UUID NOT NULL REFERENCES origin_nodes(id) ON DELETE CASCADE,
    
    link_strength FLOAT DEFAULT 1.0 NOT NULL,      -- 0.0 to 1.0
    description VARCHAR(500),
    
    -- R&D Rule #1: Checkpoint required for creation
    checkpoint_id UUID REFERENCES checkpoints(id),
    
    -- Evidence
    evidence JSONB,                                 -- {sources:[], confidence:0..1, notes:""}
    
    -- R&D Rule #6: Traceability
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    PRIMARY KEY (trigger_id, result_id),
    
    -- Anti-self-loop constraint
    CONSTRAINT no_self_loop CHECK (trigger_id != result_id)
);

CREATE INDEX idx_origin_causal_trigger ON origin_causal_links(trigger_id);
CREATE INDEX idx_origin_causal_result ON origin_causal_links(result_id);

COMMENT ON TABLE origin_causal_links IS 'R&D Rule #1: All causal links require checkpoint approval';


-- ═══════════════════════════════════════════════════════════════════════════════
-- 3. UNIVERSAL LINKS (Cross-entity visualization)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS origin_universal_links (
    from_type VARCHAR(50) NOT NULL,                -- node|pillar|custom|legacy|bio|media
    from_id UUID NOT NULL,
    to_type VARCHAR(50) NOT NULL,
    to_id UUID NOT NULL,
    
    relation VARCHAR(100) NOT NULL,                -- IMPACTS|DERIVES_FROM|CORRELATES_WITH|ENABLES|FEEDBACKS
    weight FLOAT DEFAULT 1.0 NOT NULL,
    evidence JSONB,                                 -- {sources:[], confidence:0..1, notes:""}
    
    -- R&D Rule #6: Traceability
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    PRIMARY KEY (from_type, from_id, to_type, to_id)
);

CREATE INDEX idx_origin_universal_from ON origin_universal_links(from_type, from_id);
CREATE INDEX idx_origin_universal_to ON origin_universal_links(to_type, to_id);


-- ═══════════════════════════════════════════════════════════════════════════════
-- 4. MEDIA ASSETS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS origin_media_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id UUID NOT NULL REFERENCES origin_nodes(id) ON DELETE CASCADE,
    
    -- Type: FILM_SCRIPT | BOOK_CHAPTER | GAME_MECHANIC | DOC_SCENE | VISUAL_ASSET | VOICE_OVER
    type VARCHAR(50) NOT NULL,
    
    -- Format: markdown | json | final_draft | fountain | fdx
    format VARCHAR(50) NOT NULL,
    
    content JSONB NOT NULL,
    version INTEGER DEFAULT 1 NOT NULL,
    
    -- Status: draft | validated | rendered | published | needs_revision
    production_status VARCHAR(50) DEFAULT 'draft' NOT NULL,
    
    -- Sync tracking
    source_node_snapshot JSONB,
    last_synced_at TIMESTAMPTZ,
    
    -- R&D Rule #6: Traceability
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_origin_media_node ON origin_media_assets(node_id);
CREATE INDEX idx_origin_media_type ON origin_media_assets(type);
CREATE INDEX idx_origin_media_status ON origin_media_assets(production_status);

CREATE TRIGGER update_origin_media_updated_at BEFORE UPDATE ON origin_media_assets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


-- ═══════════════════════════════════════════════════════════════════════════════
-- 5. CIVILIZATION PILLARS
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS origin_civilization (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id UUID NOT NULL REFERENCES origin_nodes(id) ON DELETE CASCADE,
    
    -- Category: LANGUAGE | EMPIRE | ARCHITECTURE | INDUSTRY | COMMUNICATION | SOVEREIGNTY | SPACE
    category VARCHAR(50) NOT NULL,
    
    description TEXT,
    
    migration_flow JSONB,                          -- {from:"", to:"", cause:"", evidence:[]}
    architectural_style VARCHAR(100),
    literature_refs JSONB,                         -- [{title, author, year, note, source}]
    tools_used JSONB,                              -- ["adze", "lathe", "loom", ...]
    
    -- R&D Rule #6: Traceability
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_origin_civ_node ON origin_civilization(node_id);
CREATE INDEX idx_origin_civ_category ON origin_civilization(category);
CREATE INDEX idx_origin_civ_node_category ON origin_civilization(node_id, category);


-- ═══════════════════════════════════════════════════════════════════════════════
-- 6. CUSTOMS EVOLUTION
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS origin_customs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id UUID NOT NULL REFERENCES origin_nodes(id) ON DELETE CASCADE,
    
    custom_name VARCHAR(200) NOT NULL,             -- "family meal", "remote work"
    
    -- Stage: Emergence | Mainstream | Obsolete | Hybrid
    evolution_stage VARCHAR(50) NOT NULL,
    
    -- Impact: {sleep:"", work:"", rituals:"", social:"", time_perception:""}
    impact_on_daily_life JSONB,
    
    sources JSONB,                                  -- anthropological refs
    
    -- R&D Rule #6: Traceability
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_origin_customs_node ON origin_customs(node_id);
CREATE INDEX idx_origin_customs_stage ON origin_customs(evolution_stage);
CREATE INDEX idx_origin_customs_node_stage ON origin_customs(node_id, evolution_stage);


-- ═══════════════════════════════════════════════════════════════════════════════
-- 7. HUMAN LEGACY (R&D Rule #1: Checkpoint for mysteries)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS origin_legacy (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id UUID NOT NULL REFERENCES origin_nodes(id) ON DELETE CASCADE,
    
    -- Beliefs & mysteries
    belief_system VARCHAR(100),                    -- "Polytheism", "Monotheism", "Scientific Rationalism"
    world_mystery_link VARCHAR(200),               -- "Great Pyramid Construction" - REQUIRES CHECKPOINT
    
    -- Body & capacities
    human_talents JSONB,                           -- ["Endurance","Memory","Abstract Thinking",...]
    sports_and_activities JSONB,                   -- [{name:"", era:"", role:"ritual|training|spectacle"}]
    
    -- Planetary adaptation
    planetary_event VARCHAR(100),                  -- "Younger Dryas", "Little Ice Age"
    
    -- Stage: Biological | Technological | Cognitive
    adaptation_stage VARCHAR(50),
    
    legacy_score FLOAT DEFAULT 0.5 NOT NULL,      -- 0..1
    
    evidence JSONB,                                 -- {sources:[], confidence:0..1, notes:""}
    
    -- R&D Rule #1: Checkpoint for mystery insertions
    checkpoint_id UUID REFERENCES checkpoints(id),
    
    -- R&D Rule #6: Traceability
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_origin_legacy_node ON origin_legacy(node_id);
CREATE INDEX idx_origin_legacy_event ON origin_legacy(planetary_event);
CREATE INDEX idx_origin_legacy_node_event ON origin_legacy(node_id, planetary_event);

COMMENT ON COLUMN origin_legacy.world_mystery_link IS 'R&D Rule #1: Requires checkpoint approval when not null';


-- ═══════════════════════════════════════════════════════════════════════════════
-- 8. BIO-EVOLUTION (R&D Rule #1: Checkpoint for medium/strong claims)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS origin_bio_eco (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id UUID NOT NULL REFERENCES origin_nodes(id) ON DELETE CASCADE,
    
    -- Genetic evolution
    genetic_mutation VARCHAR(200),                 -- "Lactase persistence"
    biological_impact TEXT,                        -- metabolism/morphology/immune changes
    
    -- Environment transformation
    env_modification VARCHAR(200),                 -- "Deforestation", "Irrigation", "Urbanization"
    biodiversity_shift JSONB,                      -- {domesticated:[], extinct:[], invasive:[], notes:""}
    
    -- Feedback loop narrative
    feedback_loop_description TEXT,
    
    -- Evidence (MANDATORY for medium/strong claims)
    -- {sources:[], confidence:0..1, claim_strength:"weak|medium|strong"}
    evidence JSONB NOT NULL DEFAULT '{"sources":[],"confidence":0.5,"claim_strength":"weak"}',
    
    -- R&D Rule #1: Checkpoint for medium/strong claims
    checkpoint_id UUID REFERENCES checkpoints(id),
    
    -- R&D Rule #6: Traceability
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    -- Constraint: claim_strength must be valid
    CONSTRAINT valid_claim_strength CHECK (
        evidence->>'claim_strength' IN ('weak', 'medium', 'strong')
    )
);

CREATE INDEX idx_origin_bio_node ON origin_bio_eco(node_id);
CREATE INDEX idx_origin_bio_mutation ON origin_bio_eco(genetic_mutation);
CREATE INDEX idx_origin_bio_env ON origin_bio_eco(env_modification);
CREATE INDEX idx_origin_bio_node_mut ON origin_bio_eco(node_id, genetic_mutation);

COMMENT ON TABLE origin_bio_eco IS 'R&D Rule #1: Medium/strong claims require checkpoint approval and evidence sources';
COMMENT ON COLUMN origin_bio_eco.evidence IS 'weak: 0 sources OK, medium: ≥1 source, strong: ≥2 sources required';


-- ═══════════════════════════════════════════════════════════════════════════════
-- VALIDATION FUNCTION: Check evidence sources
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION validate_bio_eco_evidence()
RETURNS TRIGGER AS $$
DECLARE
    claim_strength TEXT;
    sources_count INTEGER;
BEGIN
    claim_strength := NEW.evidence->>'claim_strength';
    sources_count := jsonb_array_length(COALESCE(NEW.evidence->'sources', '[]'::jsonb));
    
    -- Medium claims require at least 1 source
    IF claim_strength = 'medium' AND sources_count < 1 THEN
        RAISE EXCEPTION 'Medium claims require at least 1 source. Found: %', sources_count;
    END IF;
    
    -- Strong claims require at least 2 sources
    IF claim_strength = 'strong' AND sources_count < 2 THEN
        RAISE EXCEPTION 'Strong claims require at least 2 independent sources. Found: %', sources_count;
    END IF;
    
    -- Medium/Strong claims require checkpoint
    IF claim_strength IN ('medium', 'strong') AND NEW.checkpoint_id IS NULL THEN
        RAISE EXCEPTION 'Medium/Strong bio-eco claims require checkpoint approval (R&D Rule #1)';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_bio_eco_evidence
    BEFORE INSERT OR UPDATE ON origin_bio_eco
    FOR EACH ROW EXECUTE FUNCTION validate_bio_eco_evidence();


-- ═══════════════════════════════════════════════════════════════════════════════
-- VALIDATION FUNCTION: Check legacy mystery checkpoint
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION validate_legacy_mystery()
RETURNS TRIGGER AS $$
BEGIN
    -- Mystery links require checkpoint
    IF NEW.world_mystery_link IS NOT NULL AND NEW.world_mystery_link != '' THEN
        IF NEW.checkpoint_id IS NULL THEN
            RAISE EXCEPTION 'World mystery links require checkpoint approval (R&D Rule #1)';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_legacy_mystery
    BEFORE INSERT OR UPDATE ON origin_legacy
    FOR EACH ROW EXECUTE FUNCTION validate_legacy_mystery();


-- ═══════════════════════════════════════════════════════════════════════════════
-- VALIDATION FUNCTION: Anti-cycle detection for causal links
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION detect_causal_cycle()
RETURNS TRIGGER AS $$
DECLARE
    cycle_exists BOOLEAN;
BEGIN
    -- Check if adding this link would create a cycle
    -- Using recursive CTE to detect paths from result back to trigger
    WITH RECURSIVE path AS (
        -- Start from the result node
        SELECT result_id AS node_id, 1 AS depth
        FROM origin_causal_links
        WHERE trigger_id = NEW.result_id
        
        UNION ALL
        
        -- Follow the chain
        SELECT cl.result_id, p.depth + 1
        FROM origin_causal_links cl
        JOIN path p ON cl.trigger_id = p.node_id
        WHERE p.depth < 100  -- Prevent infinite recursion
    )
    SELECT EXISTS (
        SELECT 1 FROM path WHERE node_id = NEW.trigger_id
    ) INTO cycle_exists;
    
    IF cycle_exists THEN
        RAISE EXCEPTION 'Causal cycle detected: adding this link would create a cycle back to trigger node';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_detect_causal_cycle
    BEFORE INSERT ON origin_causal_links
    FOR EACH ROW EXECUTE FUNCTION detect_causal_cycle();


-- ═══════════════════════════════════════════════════════════════════════════════
-- VALIDATION FUNCTION: Chronology check (anti-anachronism)
-- ═══════════════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION validate_causal_chronology()
RETURNS TRIGGER AS $$
DECLARE
    trigger_date INTEGER;
    result_date INTEGER;
BEGIN
    -- Get parsed dates from nodes
    SELECT date_start_int INTO trigger_date FROM origin_nodes WHERE id = NEW.trigger_id;
    SELECT date_start_int INTO result_date FROM origin_nodes WHERE id = NEW.result_id;
    
    -- Only validate if both dates are known
    IF trigger_date IS NOT NULL AND result_date IS NOT NULL THEN
        IF result_date < trigger_date THEN
            RAISE EXCEPTION 'Chronology violation: result (%) precedes trigger (%) - anachronism not allowed', 
                result_date, trigger_date;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_causal_chronology
    BEFORE INSERT ON origin_causal_links
    FOR EACH ROW EXECUTE FUNCTION validate_causal_chronology();


-- ═══════════════════════════════════════════════════════════════════════════════
-- COMMENTS
-- ═══════════════════════════════════════════════════════════════════════════════

COMMENT ON TABLE origin_nodes IS 'ORIGIN Module: Core nodes representing technologies, discoveries, and practices';
COMMENT ON TABLE origin_causal_links IS 'R&D Rule #1: Causal links (trigger→result) require checkpoint approval';
COMMENT ON TABLE origin_bio_eco IS 'Gene-culture co-evolution - Evidence validation enforced by trigger';
COMMENT ON TABLE origin_legacy IS 'Human legacy - Mystery links require checkpoint approval';


-- ═══════════════════════════════════════════════════════════════════════════════
-- GRANTS
-- ═══════════════════════════════════════════════════════════════════════════════

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO chenu;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO chenu;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO chenu;
