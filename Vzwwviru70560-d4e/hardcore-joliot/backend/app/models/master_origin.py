"""
═══════════════════════════════════════════════════════════════════════════════
ORIGIN-GENESIS-ULTIMA — Master Models (CHE·NU / AT·OM V76)
═══════════════════════════════════════════════════════════════════════════════

Purpose:
- Unified Technology (OriginNode), Causality, Media outputs, Civilization pillars,
  Customs evolution, Human legacy (belief/body/planet), and Bio-Eco evolution.

Design Goals:
- Scales to millions of causal links via indexed ids + association tables
- Flexible historical dating with uncertainty tracking
- Cross-domain linking: any OriginNode can connect to Pillar/Custom/Legacy/Bio

R&D COMPLIANCE:
- Rule #6 (Traceability): All entities have id, created_by, created_at, validated_by
- Expert agent validation required before persisting as facts

Tables Created:
- origin_nodes (core technology/discovery/practice)
- origin_causal_links (directed graph edges)
- origin_universal_links (cross-entity typed connections)
- origin_media_assets (film/book/game outputs)
- origin_civilization (language/empire/architecture pillars)
- origin_customs (anthropology & daily life)
- origin_legacy (belief/body/planet adaptation)
- origin_bio_eco (gene-culture + environmental feedback)
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import (
    Column, String, Integer, ForeignKey, Float, Boolean, 
    DateTime, Table, Index, Text, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import relationship

from app.core.database import Base


# ═══════════════════════════════════════════════════════════════════════════════
# ASSOCIATION TABLES
# ═══════════════════════════════════════════════════════════════════════════════

# Directed causal links: trigger -> result
origin_causal_links = Table(
    "origin_causal_links",
    Base.metadata,
    Column("id", PGUUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("trigger_id", PGUUID(as_uuid=True), ForeignKey("origin_nodes.id", ondelete="CASCADE"), nullable=False),
    Column("result_id", PGUUID(as_uuid=True), ForeignKey("origin_nodes.id", ondelete="CASCADE"), nullable=False),
    Column("link_strength", Float, default=1.0, nullable=False),
    Column("link_type", String(100), nullable=True),  # ENABLES | DERIVES_FROM | CORRELATES_WITH
    Column("description", Text, nullable=True),
    Column("evidence", JSONB, nullable=True),  # {sources:[], confidence:0..1}
    # Rule #6: Traceability
    Column("created_at", DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    Column("created_by", PGUUID(as_uuid=True), nullable=False),
    Column("validated_by_agent", String(100), nullable=True),  # Which expert agent validated
    Column("validation_timestamp", DateTime(timezone=True), nullable=True),
    UniqueConstraint("trigger_id", "result_id", name="uq_causal_link"),
)

# High-scale typed links between ANY entities (for graph visualization)
origin_universal_links = Table(
    "origin_universal_links",
    Base.metadata,
    Column("id", PGUUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("from_type", String(50), nullable=False),  # node|pillar|custom|legacy|bio|media
    Column("from_id", PGUUID(as_uuid=True), nullable=False),
    Column("to_type", String(50), nullable=False),
    Column("to_id", PGUUID(as_uuid=True), nullable=False),
    Column("relation", String(100), nullable=False),  # IMPACTS | DERIVES_FROM | CORRELATES_WITH | ENABLES | FEEDBACKS
    Column("weight", Float, default=1.0, nullable=False),
    Column("evidence", JSONB, nullable=True),  # {sources:[], confidence:0..1, notes:""}
    # Rule #6: Traceability
    Column("created_at", DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    Column("created_by", PGUUID(as_uuid=True), nullable=False),
    Column("validated_by_agent", String(100), nullable=True),
    UniqueConstraint("from_type", "from_id", "to_type", "to_id", "relation", name="uq_universal_link"),
)

# Indexes for causal links
Index("ix_causal_links_trigger", origin_causal_links.c.trigger_id)
Index("ix_causal_links_result", origin_causal_links.c.result_id)
Index("ix_universal_links_from", origin_universal_links.c.from_type, origin_universal_links.c.from_id)
Index("ix_universal_links_to", origin_universal_links.c.to_type, origin_universal_links.c.to_id)


# ═══════════════════════════════════════════════════════════════════════════════
# ORIGIN NODE — Core Technology/Discovery/Practice
# ═══════════════════════════════════════════════════════════════════════════════

class OriginNode(Base):
    """
    Core unit of the ORIGIN graph: represents a technology, discovery, 
    practice, or historical event.
    """
    __tablename__ = "origin_nodes"

    # Identity
    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(500), index=True, nullable=False)
    
    # Temporal positioning (flexible for historical uncertainty)
    epoch = Column(String(100), index=True, nullable=True)  # "Neolithic", "Industrial", "Digital"
    exact_date = Column(String(100), nullable=True)  # "c.1450", "1939", "~10,000 BCE"
    date_start = Column(String(100), nullable=True)  # Sortable boundary start
    date_end = Column(String(100), nullable=True)    # Sortable boundary end
    date_certainty = Column(Float, default=0.8, nullable=False)  # 0..1 confidence
    
    # Content
    description = Column(Text, nullable=True)
    
    # Rich metadata
    metadata_json = Column(JSONB, nullable=True)
    # {sources:[], shadow_contributors:[], tech_specs:[], tags:[], inventors:[]}
    
    geopolitical_context = Column(JSONB, nullable=True)
    # {power_shift:"", conflicts:[], trade:[], societal_effects:[], region:""}
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Rule #6: Full Traceability
    # ═══════════════════════════════════════════════════════════════════════════
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)  # Identity who created
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_by = Column(PGUUID(as_uuid=True), nullable=True)
    
    # Validation lifecycle (expert agent tracking)
    is_validated = Column(Boolean, default=False, nullable=False)
    validated_by = Column(JSONB, nullable=True)
    # {agent_ids:["ORIGIN_HISTORIAN", "ORIGIN_SCIENTIST"], method:"consensus", timestamp:"", confidence:0.9}
    
    validation_status = Column(String(50), default="pending", nullable=False)
    # pending | draft | under_review | validated | contested | archived
    
    # ═══════════════════════════════════════════════════════════════════════════
    # Relationships
    # ═══════════════════════════════════════════════════════════════════════════
    media_assets = relationship("OriginMediaAsset", back_populates="node", cascade="all, delete-orphan")
    civilization_pillars = relationship("OriginCivilizationPillar", back_populates="node", cascade="all, delete-orphan")
    customs = relationship("OriginCustomEvolution", back_populates="node", cascade="all, delete-orphan")
    legacies = relationship("OriginHumanLegacy", back_populates="node", cascade="all, delete-orphan")
    bio_evolutions = relationship("OriginBioEvolution", back_populates="node", cascade="all, delete-orphan")


Index("ix_origin_nodes_name_epoch", OriginNode.name, OriginNode.epoch)
Index("ix_origin_nodes_validation", OriginNode.validation_status)
Index("ix_origin_nodes_created_at", OriginNode.created_at)


# ═══════════════════════════════════════════════════════════════════════════════
# MEDIA ASSET — Film/Book/Game Outputs
# ═══════════════════════════════════════════════════════════════════════════════

class OriginMediaAsset(Base):
    """
    Media production linked to an OriginNode.
    Types: FILM_SCRIPT | BOOK_CHAPTER | GAME_MECHANIC | DOC_SCENE | VISUAL_ASSET | VOICE_OVER
    """
    __tablename__ = "origin_media_assets"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("origin_nodes.id", ondelete="CASCADE"), nullable=False)
    
    # Asset type and format
    asset_type = Column(String(50), index=True, nullable=False)
    # FILM_SCRIPT | BOOK_CHAPTER | GAME_MECHANIC | DOC_SCENE | VISUAL_ASSET | VOICE_OVER
    
    format = Column(String(50), index=True, nullable=False)
    # markdown | json | final_draft | fountain | fdx | png | mp3
    
    # Content
    title = Column(String(500), nullable=True)
    content = Column(JSONB, nullable=False)  # The actual content structure
    version = Column(Integer, default=1, nullable=False)
    
    # Production status
    production_status = Column(String(50), default="draft", index=True, nullable=False)
    # draft | validated | rendered | published | needs_revision
    
    # Synchronization
    source_node_snapshot = Column(JSONB, nullable=True)  # Snapshot of node at creation
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_by = Column(PGUUID(as_uuid=True), nullable=True)
    validated_by_agent = Column(String(100), nullable=True)  # SCENE_DIRECTOR, GHOST_WRITER, etc.
    
    # Relationships
    node = relationship("OriginNode", back_populates="media_assets")


Index("ix_origin_media_node_type", OriginMediaAsset.node_id, OriginMediaAsset.asset_type)


# ═══════════════════════════════════════════════════════════════════════════════
# CIVILIZATION PILLAR — Language/Empire/Architecture
# ═══════════════════════════════════════════════════════════════════════════════

class OriginCivilizationPillar(Base):
    """
    Civilization-level impacts of technologies.
    Categories: LANGUAGE | EMPIRE | ARCHITECTURE | INDUSTRY | COMMUNICATION | SOVEREIGNTY | SPACE
    """
    __tablename__ = "origin_civilization"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("origin_nodes.id", ondelete="CASCADE"), nullable=False)
    
    # Pillar category
    category = Column(String(50), index=True, nullable=False)
    # LANGUAGE | EMPIRE | ARCHITECTURE | INDUSTRY | COMMUNICATION | SOVEREIGNTY | SPACE
    
    # Content
    title = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    
    # Structured data
    migration_flow = Column(JSONB, nullable=True)
    # {from:"", to:"", cause:"", evidence:[], affected_populations:[]}
    
    architectural_style = Column(String(200), nullable=True)
    literature_refs = Column(JSONB, nullable=True)  # [{title, author, year, note, source}]
    tools_used = Column(JSONB, nullable=True)  # ["adze", "lathe", "loom", "steam engine"]
    
    # Evidence
    evidence = Column(JSONB, nullable=True)  # {sources:[], confidence:0..1}
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    validated_by_agent = Column(String(100), nullable=True)  # EMPIRE_STRATEGIST, LINGUIST_PHILOLOGIST, ARCHI_TECT
    
    # Relationships
    node = relationship("OriginNode", back_populates="civilization_pillars")


Index("ix_origin_civilization_node_category", OriginCivilizationPillar.node_id, OriginCivilizationPillar.category)


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM EVOLUTION — Anthropology & Daily Life
# ═══════════════════════════════════════════════════════════════════════════════

class OriginCustomEvolution(Base):
    """
    How daily life, rituals, and customs change due to tech transitions.
    Tracks emergence, mainstream adoption, obsolescence of practices.
    """
    __tablename__ = "origin_customs"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("origin_nodes.id", ondelete="CASCADE"), nullable=False)
    
    # Custom identification
    custom_name = Column(String(500), index=True, nullable=False)  # "family meal", "remote work"
    evolution_stage = Column(String(50), index=True, nullable=False)
    # Emergence | Mainstream | Obsolete | Hybrid | Reviving
    
    # Impact analysis
    impact_on_daily_life = Column(JSONB, nullable=True)
    # {sleep:"", work:"", rituals:"", social:"", time_perception:"", family_structure:""}
    
    region = Column(String(200), nullable=True)  # Geographic scope
    time_period = Column(String(200), nullable=True)
    
    # Sources
    sources = Column(JSONB, nullable=True)  # Anthropological references + evidence
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    validated_by_agent = Column(String(100), nullable=True)  # ETHNO_OBSERVER, CRAFT_MASTER
    
    # Relationships
    node = relationship("OriginNode", back_populates="customs")


Index("ix_origin_customs_node_stage", OriginCustomEvolution.node_id, OriginCustomEvolution.evolution_stage)


# ═══════════════════════════════════════════════════════════════════════════════
# HUMAN LEGACY — Belief/Body/Planet Adaptation
# ═══════════════════════════════════════════════════════════════════════════════

class OriginHumanLegacy(Base):
    """
    Human spirit/body/planet adaptation layer.
    Tracks beliefs, talents, sports, planetary events, and adaptations.
    """
    __tablename__ = "origin_legacy"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("origin_nodes.id", ondelete="CASCADE"), nullable=False)
    
    # Beliefs & mysteries
    belief_system = Column(String(200), nullable=True)  # Polytheism, Monotheism, Scientific Rationalism
    world_mystery_link = Column(String(500), nullable=True)  # Great Pyramid Construction, etc.
    
    # Body & capacities
    human_talents = Column(JSONB, nullable=True)  # ["Endurance", "Memory", "Abstract Thinking"]
    sports_and_activities = Column(JSONB, nullable=True)
    # [{name:"", era:"", role:"ritual|training|spectacle|warfare"}]
    
    # Planetary adaptation
    planetary_event = Column(String(200), index=True, nullable=True)  # Younger Dryas, Little Ice Age
    adaptation_stage = Column(String(100), nullable=True)  # Biological | Technological | Cognitive
    
    # Scoring & evidence
    legacy_score = Column(Float, default=0.5, nullable=False)  # 0..1
    evidence = Column(JSONB, nullable=True)  # {sources:[], confidence:0..1, notes:""}
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    validated_by_agent = Column(String(100), nullable=True)  # SOUL_CHRONICLER, BIO_ADAPT, GAIA_SENTINEL
    
    # Relationships
    node = relationship("OriginNode", back_populates="legacies")


Index("ix_origin_legacy_node_event", OriginHumanLegacy.node_id, OriginHumanLegacy.planetary_event)


# ═══════════════════════════════════════════════════════════════════════════════
# BIO EVOLUTION — Gene-Culture + Environmental Feedback
# ═══════════════════════════════════════════════════════════════════════════════

class OriginBioEvolution(Base):
    """
    Gene-culture co-evolution + environmental transformation feedback loops.
    CRITICAL: Must be evidence-backed; avoid overstating causality.
    """
    __tablename__ = "origin_bio_eco"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("origin_nodes.id", ondelete="CASCADE"), nullable=False)
    
    # Genetic evolution
    genetic_mutation = Column(String(200), index=True, nullable=True)  # "Lactase persistence", "AMY1 copies"
    biological_impact = Column(Text, nullable=True)  # Metabolism/morphology/immune changes
    
    # Environment transformation
    env_modification = Column(String(200), index=True, nullable=True)  # Deforestation, Irrigation, Urbanization
    biodiversity_shift = Column(JSONB, nullable=True)
    # {domesticated:[], extinct:[], invasive:[], notes:"", ecosystem_type:""}
    
    # Feedback loop
    feedback_loop_description = Column(Text, nullable=True)
    feedback_type = Column(String(100), nullable=True)
    # GENE_CULTURE | BIOEVO_FEEDBACK | EPIGENETIC_ENV | NICHE_CONSTRUCTION
    
    # Evidence (MANDATORY for strong claims)
    evidence = Column(JSONB, nullable=False, default={})
    # {sources:[], confidence:0..1, claim_strength:"weak|medium|strong", peer_reviewed:bool}
    
    # Hypothesis vs Fact tracking
    is_hypothesis = Column(Boolean, default=True, nullable=False)
    confidence_level = Column(Float, default=0.3, nullable=False)  # 0..1
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    validated_by_agent = Column(String(100), nullable=True)  # GENOME_ARCHITECT, ECO_SYSTEMIC_MAPPER
    validation_notes = Column(Text, nullable=True)
    
    # Relationships
    node = relationship("OriginNode", back_populates="bio_evolutions")


Index("ix_origin_bioeco_node_mutation", OriginBioEvolution.node_id, OriginBioEvolution.genetic_mutation)
Index("ix_origin_bioeco_node_env", OriginBioEvolution.node_id, OriginBioEvolution.env_modification)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPERT VALIDATION LOG — Track which agent validated what
# ═══════════════════════════════════════════════════════════════════════════════

class OriginExpertValidation(Base):
    """
    Audit log for expert agent validations.
    Rule #6 compliance: full traceability of who validated what and when.
    """
    __tablename__ = "origin_expert_validations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # What was validated
    entity_type = Column(String(50), nullable=False)  # node | media | pillar | custom | legacy | bio | link
    entity_id = Column(PGUUID(as_uuid=True), nullable=False)
    
    # Which expert validated
    agent_id = Column(String(100), nullable=False)  # ORIGIN_HISTORIAN, GENOME_ARCHITECT, etc.
    agent_role = Column(String(200), nullable=True)  # "Research & Validation" | "Transmédia" | etc.
    
    # Validation details
    validation_type = Column(String(50), nullable=False)  # approve | reject | request_revision | flag
    confidence = Column(Float, default=0.5, nullable=False)  # 0..1
    notes = Column(Text, nullable=True)
    
    # Sources checked
    sources_verified = Column(JSONB, nullable=True)  # [{source:"", verified:bool, notes:""}]
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)  # Identity who triggered validation


Index("ix_expert_validations_entity", OriginExpertValidation.entity_type, OriginExpertValidation.entity_id)
Index("ix_expert_validations_agent", OriginExpertValidation.agent_id)
Index("ix_expert_validations_created", OriginExpertValidation.created_at)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Association tables
    'origin_causal_links',
    'origin_universal_links',
    
    # Core models
    'OriginNode',
    'OriginMediaAsset',
    'OriginCivilizationPillar',
    'OriginCustomEvolution',
    'OriginHumanLegacy',
    'OriginBioEvolution',
    'OriginExpertValidation',
]
