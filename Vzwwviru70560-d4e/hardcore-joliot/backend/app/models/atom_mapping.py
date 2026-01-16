"""
═══════════════════════════════════════════════════════════════════════════════
AT·OM MAPPING SYSTEM — SQLAlchemy Models (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Purpose:
- Unified knowledge graph for civilization-scale data
- Multi-dimensional modules (sensory, psycho, resources, concepts, logistics)
- Evidence-first posture: provenance + confidence on all profiles

R&D Compliance:
- Rule #6: All models have created_at, created_by
- Evidence tracking on all profile tables

Tables:
- atom_nodes (core knowledge graph)
- atom_causal_links (directed causal edges)
- atom_encyclopedia (curated entries)
- atom_sensory_profiles
- atom_psycho_emotional_profiles
- atom_resource_footprints
- atom_conceptual_drift
- atom_logistics_networks
- atom_harmonic_signatures (OPTIONAL creative layer)
- atom_sub_modules (generic extension)
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
# CAUSAL LINKS TABLE (Association)
# ═══════════════════════════════════════════════════════════════════════════════

atom_causal_links = Table(
    "atom_causal_links",
    Base.metadata,
    Column("id", PGUUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("trigger_id", PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False),
    Column("result_id", PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False),
    Column("link_type", String(50), nullable=False),  # BIO|TECH|SOCIAL|SPIRITUAL|ECO|SENSORY|CONCEPT|LOGISTICS
    Column("strength", Float, default=1.0, nullable=False),
    Column("rationale", Text, nullable=True),
    Column("confidence", Float, default=0.5, nullable=False),
    Column("provenance", JSONB, nullable=True),
    # Rule #6: Traceability
    Column("created_at", DateTime(timezone=True), default=datetime.utcnow, nullable=False),
    Column("created_by", PGUUID(as_uuid=True), nullable=False),
    UniqueConstraint("trigger_id", "result_id", name="uq_atom_causal_link"),
)

Index("ix_atom_causal_trigger", atom_causal_links.c.trigger_id)
Index("ix_atom_causal_result", atom_causal_links.c.result_id)


# ═══════════════════════════════════════════════════════════════════════════════
# ATOM NODE — Core Knowledge Graph
# ═══════════════════════════════════════════════════════════════════════════════

class ATOMNode(Base):
    """
    Core node in the AT·OM unified knowledge graph.
    Represents technologies, discoveries, events, concepts.
    """
    __tablename__ = "atom_nodes"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(500), index=True, nullable=False)
    
    # Dimension classification
    dimension = Column(String(50), index=True, nullable=True)
    # PHYSICAL | BIOLOGICAL | SOCIAL | SPIRITUAL | CONCEPTUAL | ECOLOGICAL | LOGISTICAL | SENSORY
    
    # Time metadata (flexible for historical uncertainty)
    epoch = Column(String(100), index=True, nullable=True)
    date_range = Column(JSONB, nullable=True)  # {from, to, label, confidence}
    location = Column(JSONB, nullable=True)    # {region, lat, lon, confidence}
    
    # Content
    description = Column(Text, nullable=True)
    
    # Multi-dimensional data summaries
    technical_specs = Column(JSONB, nullable=True)
    biological_impact = Column(JSONB, nullable=True)
    social_customs = Column(JSONB, nullable=True)
    planetary_context = Column(JSONB, nullable=True)
    psychology = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_by = Column(PGUUID(as_uuid=True), nullable=True)
    
    # Relationships
    sensory_profiles = relationship("AtomSensoryProfile", back_populates="node", cascade="all, delete-orphan")
    psycho_profiles = relationship("AtomPsychoEmotionalProfile", back_populates="node", cascade="all, delete-orphan")
    resource_footprints = relationship("AtomResourceFootprint", back_populates="node", cascade="all, delete-orphan")
    conceptual_drifts = relationship("AtomConceptualDrift", back_populates="node", cascade="all, delete-orphan")
    logistics_networks = relationship("AtomLogisticsNetwork", back_populates="node", cascade="all, delete-orphan")
    harmonic_signatures = relationship("AtomHarmonicSignature", back_populates="node", cascade="all, delete-orphan")
    encyclopedia_entries = relationship("AtomEncyclopediaEntry", back_populates="node", cascade="all, delete-orphan")
    
    # Graph connections
    connected_to = relationship(
        "ATOMNode",
        secondary=atom_causal_links,
        primaryjoin=id == atom_causal_links.c.trigger_id,
        secondaryjoin=id == atom_causal_links.c.result_id,
        backref="connected_from",
    )


Index("ix_atom_nodes_dim_epoch", ATOMNode.dimension, ATOMNode.epoch)


# ═══════════════════════════════════════════════════════════════════════════════
# ENCYCLOPEDIA ENTRY — Curated Renderable Content
# ═══════════════════════════════════════════════════════════════════════════════

class AtomEncyclopediaEntry(Base):
    """Curated entry for rendering to book/film/game templates."""
    __tablename__ = "atom_encyclopedia"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(500), nullable=False)
    content_html = Column(Text, nullable=True)
    content_md = Column(Text, nullable=True)
    metadata_tags = Column(JSONB, nullable=True)
    
    # Quality tracking
    completeness = Column(Float, default=0.0, nullable=False)
    review_status = Column(String(50), default="draft", nullable=False)
    provenance = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    
    # Relationship
    node = relationship("ATOMNode", back_populates="encyclopedia_entries")


# ═══════════════════════════════════════════════════════════════════════════════
# SENSORY PROFILE — Ergonomics, Acoustics, Other Senses
# ═══════════════════════════════════════════════════════════════════════════════

class AtomSensoryProfile(Base):
    """
    Sensory layer: ergonomics, acoustics, visual/olfactory/tactile.
    Evidence-first: reconstructions are hypotheses with assumptions.
    """
    __tablename__ = "atom_sensory_profiles"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    ergonomics = Column(JSONB, nullable=True)   # grip, posture, load, skeletal markers
    acoustics = Column(JSONB, nullable=True)    # soundscape reconstruction
    other_senses = Column(JSONB, nullable=True) # visual/olfactory/tactile hypotheses
    
    # Evidence tracking
    confidence = Column(Float, default=0.5, nullable=False)
    assumptions = Column(Text, nullable=True)
    provenance = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    
    # Relationship
    node = relationship("ATOMNode", back_populates="sensory_profiles")


# ═══════════════════════════════════════════════════════════════════════════════
# PSYCHO-EMOTIONAL PROFILE — Societal Moods, Motivations
# ═══════════════════════════════════════════════════════════════════════════════

class AtomPsychoEmotionalProfile(Base):
    """
    Psycho-emotional layer: societal mood, motivations, counter-signals.
    Data framed as observed signals + interpretation hypotheses.
    """
    __tablename__ = "atom_psycho_emotional_profiles"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    psycho_emotional = Column(JSONB, nullable=True)
    # {societal_mood:[], drivers:[], counter_signals:[]}
    
    # Evidence tracking
    confidence = Column(Float, default=0.5, nullable=False)
    assumptions = Column(Text, nullable=True)
    provenance = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    
    # Relationship
    node = relationship("ATOMNode", back_populates="psycho_profiles")


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE FOOTPRINT — Extraction, Gaia Impact
# ═══════════════════════════════════════════════════════════════════════════════

class AtomResourceFootprint(Base):
    """Resource layer: materials, extraction, environmental impact."""
    __tablename__ = "atom_resource_footprints"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    resource_footprint = Column(JSONB, nullable=True)
    # {materials:[], extraction:{}, gaia_impact:{}, lifecycle:{}}
    
    # Evidence tracking
    confidence = Column(Float, default=0.5, nullable=False)
    assumptions = Column(Text, nullable=True)
    provenance = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    
    # Relationship
    node = relationship("ATOMNode", back_populates="resource_footprints")


# ═══════════════════════════════════════════════════════════════════════════════
# CONCEPTUAL DRIFT — Etymology, Concept Evolution
# ═══════════════════════════════════════════════════════════════════════════════

class AtomConceptualDrift(Base):
    """Conceptual layer: etymology, semantic shifts, cultural contexts."""
    __tablename__ = "atom_conceptual_drift"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    concept_evolution = Column(JSONB, nullable=True)
    # {etymology:{}, semantic_shifts:[], cultural_contexts:[], modern_meanings:[]}
    
    # Evidence tracking
    confidence = Column(Float, default=0.5, nullable=False)
    assumptions = Column(Text, nullable=True)
    provenance = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    
    # Relationship
    node = relationship("ATOMNode", back_populates="conceptual_drifts")


# ═══════════════════════════════════════════════════════════════════════════════
# LOGISTICS NETWORK — Routes, Supply Chains, Infrastructure
# ═══════════════════════════════════════════════════════════════════════════════

class AtomLogisticsNetwork(Base):
    """Logistics layer: routes, cables, orbits, supply chains."""
    __tablename__ = "atom_logistics_networks"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    logistics_data = Column(JSONB, nullable=True)
    # {routes:[], nodes:[], cables:[], orbits:[], supply_chains:[], bottlenecks:[]}
    
    # Evidence tracking
    confidence = Column(Float, default=0.5, nullable=False)
    assumptions = Column(Text, nullable=True)
    provenance = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    
    # Relationship
    node = relationship("ATOMNode", back_populates="logistics_networks")


# ═══════════════════════════════════════════════════════════════════════════════
# HARMONIC SIGNATURE — OPTIONAL Creative Layer
# ═══════════════════════════════════════════════════════════════════════════════

class AtomHarmonicSignature(Base):
    """
    OPTIONAL creative layer for gematria/vibration metadata.
    
    ⚠️ WARNING: This is NOT scientific. Treat as interpretive/artistic.
    - confidence defaults to 0.2 (low)
    - interpretive_note MUST contain disclaimer for UI
    - HARMONICS_ENABLED feature flag should default to False
    """
    __tablename__ = "atom_harmonic_signatures"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Gematria/numeric signatures (creative, NOT scientific)
    numeric_signatures = Column(JSONB, nullable=True)
    vibration_mapping = Column(JSONB, nullable=True)  # UX sonification hints
    
    # MANDATORY disclaimer for UI
    interpretive_note = Column(Text, nullable=True)
    
    # Keep confidence LOW by default (interpretive layer)
    confidence = Column(Float, default=0.2, nullable=False)
    provenance = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)
    
    # Relationship
    node = relationship("ATOMNode", back_populates="harmonic_signatures")


# ═══════════════════════════════════════════════════════════════════════════════
# SUB-MODULE — Generic Extension Point
# ═══════════════════════════════════════════════════════════════════════════════

class AtomSubModule(Base):
    """Generic attachment point for specialized modules."""
    __tablename__ = "atom_sub_modules"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    node_id = Column(PGUUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Free-form JSON for specialized data
    sensory_data = Column(JSONB, nullable=True)
    psycho_emotional = Column(JSONB, nullable=True)
    resource_footprint = Column(JSONB, nullable=True)
    conceptual_drift = Column(JSONB, nullable=True)
    logistics_networks = Column(JSONB, nullable=True)
    
    # Evidence tracking
    confidence = Column(Float, default=0.5, nullable=False)
    provenance = Column(JSONB, nullable=True)
    
    # Rule #6: Traceability
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_by = Column(PGUUID(as_uuid=True), nullable=False)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Core
    'ATOMNode',
    'atom_causal_links',
    'AtomEncyclopediaEntry',
    
    # Profiles
    'AtomSensoryProfile',
    'AtomPsychoEmotionalProfile',
    'AtomResourceFootprint',
    'AtomConceptualDrift',
    'AtomLogisticsNetwork',
    
    # Creative (optional)
    'AtomHarmonicSignature',
    
    # Generic
    'AtomSubModule',
]
