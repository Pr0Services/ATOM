"""
═══════════════════════════════════════════════════════════════════════════════
AT-OM MAPPING SYSTEM — SQLAlchemy Models (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Multi-dimensional civilization knowledge graph with:
- Core nodes (ATOMNode)
- Causal links (atom_causal_links)
- Encyclopedia entries
- 6 specialized dimension tables:
  - Sensory, Psychology, Resources, Concepts, Logistics, Harmonics

Rule #6 Compliant: All entities have id, created_by, created_at, provenance
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any

from sqlalchemy import (
    Column, String, Integer, ForeignKey, JSON, Float, 
    Boolean, DateTime, Table, Text, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB

from app.core.database import Base


# ═══════════════════════════════════════════════════════════════════════════════
# CAUSAL GRAPH (Many-to-Many with attributes)
# ═══════════════════════════════════════════════════════════════════════════════

atom_causal_links = Table(
    "atom_causal_links",
    Base.metadata,
    Column("id", PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("trigger_id", PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("result_id", PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), index=True, nullable=False),
    # Link types: BIO | TECH | SOCIAL | SPIRITUAL | ECO | SENSORY | CONCEPT | LOGISTICS
    Column("link_type", String(50), nullable=False, index=True),
    Column("strength", Float, default=1.0),
    Column("rationale", Text, nullable=True),
    Column("confidence", Float, default=0.5),
    # Evidence-first: provenance required for high-confidence links
    Column("provenance", JSONB, nullable=True),
    # Rule #6 traceability
    Column("created_by", PG_UUID(as_uuid=True), nullable=True),
    Column("created_at", DateTime(timezone=True), default=datetime.utcnow),
    # Indexes
    Index("ix_atom_causal_trigger_result", "trigger_id", "result_id", unique=True),
    Index("ix_atom_causal_confidence", "confidence"),
)


# ═══════════════════════════════════════════════════════════════════════════════
# CORE NODE
# ═══════════════════════════════════════════════════════════════════════════════

class ATOMNode(Base):
    """
    A node in the unified AT-OM mapping graph.
    
    Represents civilization-scale knowledge: technologies, discoveries,
    events, practices, institutions, adaptations.
    """
    __tablename__ = "atom_nodes"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(500), index=True, nullable=False)

    # Dimensions: PHYSICAL | BIOLOGICAL | SOCIAL | SPIRITUAL | CONCEPTUAL | ECOLOGICAL | LOGISTICAL | SENSORY
    dimension: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)

    # Time metadata (flexible for ancient/uncertain dates)
    epoch: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    date_range: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {"from": "-10000", "to": "-8000", "label": "approx"}
    
    location: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {"region": "Mesopotamia", "lat": 33.0, "lon": 44.0, "confidence": 0.8}

    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Multi-dimensional embedded data (high-level summaries)
    technical_specs: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    biological_impact: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    social_customs: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    planetary_context: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    psychology: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)

    # Validation lifecycle
    validation_status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    validated_by: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    validated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Rule #6 traceability
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    modified_by: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    modified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    sensory_profile = relationship("AtomSensoryProfile", back_populates="node", uselist=False, cascade="all, delete-orphan")
    psycho_profile = relationship("AtomPsychoEmotionalProfile", back_populates="node", uselist=False, cascade="all, delete-orphan")
    resource_footprint = relationship("AtomResourceFootprint", back_populates="node", uselist=False, cascade="all, delete-orphan")
    conceptual_drift = relationship("AtomConceptualDrift", back_populates="node", uselist=False, cascade="all, delete-orphan")
    logistics_network = relationship("AtomLogisticsNetwork", back_populates="node", uselist=False, cascade="all, delete-orphan")
    harmonic_signature = relationship("AtomHarmonicSignature", back_populates="node", uselist=False, cascade="all, delete-orphan")
    encyclopedia_entries = relationship("EncyclopediaEntry", back_populates="node", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_atom_nodes_dim_epoch", "dimension", "epoch"),
        Index("ix_atom_nodes_validation", "validation_status"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ENCYCLOPEDIA ENTRY (Transmedia output)
# ═══════════════════════════════════════════════════════════════════════════════

class EncyclopediaEntry(Base):
    """
    Curated entry for a node - renderable to book/film/game templates.
    """
    __tablename__ = "atom_encyclopedia"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), index=True, nullable=False)

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_md: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Tags for filtering
    metadata_tags: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {"languages": [], "empires": [], "industries": [], "eras": []}

    completeness: Mapped[float] = mapped_column(Float, default=0.0)
    review_status: Mapped[str] = mapped_column(String(20), default="draft")  # draft | validated | published
    provenance: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)

    # Rule #6 traceability
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=datetime.utcnow)

    # Relationship
    node = relationship("ATOMNode", back_populates="encyclopedia_entries")


# ═══════════════════════════════════════════════════════════════════════════════
# SENSORY PROFILE
# ═══════════════════════════════════════════════════════════════════════════════

class AtomSensoryProfile(Base):
    """
    Sensory dimension: ergonomics, acoustics, visual/olfactory/tactile.
    """
    __tablename__ = "atom_sensory_profiles"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), unique=True, nullable=False)

    ergonomics: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {"grip": "...", "posture": "...", "load": "...", "skeletal_markers": [...]}
    
    acoustics: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {"soundscape": "...", "ambient_db": 45, "asset_refs": [...]}
    
    other_senses: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {"visual": "...", "olfactory": "...", "tactile": "..."}

    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    provenance: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship
    node = relationship("ATOMNode", back_populates="sensory_profile")


# ═══════════════════════════════════════════════════════════════════════════════
# PSYCHO-EMOTIONAL PROFILE
# ═══════════════════════════════════════════════════════════════════════════════

class AtomPsychoEmotionalProfile(Base):
    """
    Psychology dimension: collective emotions, motivations, beliefs.
    
    ⚠️ Evidence-first: always include counter-signals and uncertainty.
    """
    __tablename__ = "atom_psycho_emotional_profiles"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), unique=True, nullable=False)

    psycho_emotional: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {
    #   "societal_mood": [{"label": "anxiety", "signal": "millenarian pamphlets", "confidence": 0.4}],
    #   "drivers": [{"type": "fear|desire|status|survival", "note": "...", "confidence": 0.3}],
    #   "counter_signals": [...],  # REQUIRED for balance
    #   "uncertainty_notes": "..."  # REQUIRED
    # }

    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    provenance: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship
    node = relationship("ATOMNode", back_populates="psycho_profile")


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCE FOOTPRINT
# ═══════════════════════════════════════════════════════════════════════════════

class AtomResourceFootprint(Base):
    """
    Resource dimension: materials, supply chains, environmental impacts.
    """
    __tablename__ = "atom_resource_footprints"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), unique=True, nullable=False)

    resource_footprint: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {
    #   "materials": [{"name": "tin", "origin": "Cornwall", "evidence": [...]}],
    #   "supply_chain": [{"step": "smelting", "location": "...", "era": "..."}],
    #   "environmental_impacts": [{"type": "deforestation", "note": "...", "confidence": 0.5}],
    #   "biodiversity_shift": [{"species": "...", "change": "extinct|domesticated", "confidence": 0.2}]
    # }

    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    provenance: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship
    node = relationship("ATOMNode", back_populates="resource_footprint")


# ═══════════════════════════════════════════════════════════════════════════════
# CONCEPTUAL DRIFT
# ═══════════════════════════════════════════════════════════════════════════════

class AtomConceptualDrift(Base):
    """
    Conceptual dimension: etymology, semantic evolution, cross-language.
    """
    __tablename__ = "atom_conceptual_drifts"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), unique=True, nullable=False)

    conceptual_drift: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {
    #   "term": "time",
    #   "stages": [{"era": "agricultural", "meaning": "cycle", "sources": [...]}],
    #   "cross_language": [{"lang": "latin", "form": "tempus", "note": "..."}]
    # }

    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    provenance: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship
    node = relationship("ATOMNode", back_populates="conceptual_drift")


# ═══════════════════════════════════════════════════════════════════════════════
# LOGISTICS NETWORK
# ═══════════════════════════════════════════════════════════════════════════════

class AtomLogisticsNetwork(Base):
    """
    Logistics dimension: routes, cables, orbits, supply chains, trade networks.
    """
    __tablename__ = "atom_logistics_networks"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), unique=True, nullable=False)

    logistics_networks: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {
    #   "networks": [{"type": "road|cable|orbit|trade_route", "name": "Silk Road", "era": "...", "geometry_ref": "..."}],
    #   "nodes": [{"name": "...", "lat": ..., "lon": ...}],
    #   "edges": [{"from": "...", "to": "...", "capacity": "...", "confidence": 0.4}]
    # }

    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    provenance: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship
    node = relationship("ATOMNode", back_populates="logistics_network")


# ═══════════════════════════════════════════════════════════════════════════════
# HARMONIC SIGNATURE (CREATIVE LAYER - ADDON)
# ═══════════════════════════════════════════════════════════════════════════════

class AtomHarmonicSignature(Base):
    """
    Harmonic dimension: numeric signatures for creative/media purposes.
    
    ⚠️ NOT SCIENTIFIC: This is for film/game UX sonification and visualization.
    Always labeled as interpretive, never as factual causation.
    """
    __tablename__ = "atom_harmonic_signatures"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Computed signatures (A1Z26, ASCII sum, custom)
    numeric_signatures: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {"a1z26_sum": 74, "ascii_sum": 1234, "tokens": {"fire": 38, "wheel": 52}}

    # UX mapping for sonification/visualization
    vibration_mapping: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    # {"sonification": {"method": "midi_scale", "base_note": 60, "range": 24}, "visual": {"pattern": "lissajous"}}

    # Metadata
    is_interpretive: Mapped[bool] = mapped_column(Boolean, default=True)  # Always True - not factual
    provenance: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationship
    node = relationship("ATOMNode", back_populates="harmonic_signature")


# ═══════════════════════════════════════════════════════════════════════════════
# SUB-MODULE (Generic attachment helper)
# ═══════════════════════════════════════════════════════════════════════════════

class ATOMSubModule(Base):
    """
    Generic attachment point for specialized modules.
    Use for quick prototyping; detailed data should go to specialized tables.
    """
    __tablename__ = "atom_sub_modules"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("atom_nodes.id", ondelete="CASCADE"), index=True, nullable=False)

    # Free-form JSON sections
    sensory_data: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    psycho_emotional: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    resource_footprint: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    conceptual_drift: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    logistics_networks: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)

    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    provenance: Mapped[Optional[Dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "atom_causal_links",
    "ATOMNode",
    "EncyclopediaEntry",
    "AtomSensoryProfile",
    "AtomPsychoEmotionalProfile",
    "AtomResourceFootprint",
    "AtomConceptualDrift",
    "AtomLogisticsNetwork",
    "AtomHarmonicSignature",
    "ATOMSubModule",
]
