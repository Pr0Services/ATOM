"""
═══════════════════════════════════════════════════════════════════════════════
AT-OM MAPPING SYSTEM — Pydantic Schemas (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Request/Response models for AT-OM API endpoints.
Evidence-first design with mandatory provenance for high-confidence claims.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ATOMDimension(str, Enum):
    PHYSICAL = "PHYSICAL"
    BIOLOGICAL = "BIOLOGICAL"
    SOCIAL = "SOCIAL"
    SPIRITUAL = "SPIRITUAL"
    CONCEPTUAL = "CONCEPTUAL"
    ECOLOGICAL = "ECOLOGICAL"
    LOGISTICAL = "LOGISTICAL"
    SENSORY = "SENSORY"


class CausalLinkType(str, Enum):
    BIO = "BIO"
    TECH = "TECH"
    SOCIAL = "SOCIAL"
    SPIRITUAL = "SPIRITUAL"
    ECO = "ECO"
    SENSORY = "SENSORY"
    CONCEPT = "CONCEPT"
    LOGISTICS = "LOGISTICS"


class ValidationStatus(str, Enum):
    PENDING = "pending"
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    VALIDATED = "validated"
    CONTESTED = "contested"
    ARCHIVED = "archived"


class ReviewStatus(str, Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    PUBLISHED = "published"


# ═══════════════════════════════════════════════════════════════════════════════
# PROVENANCE (Evidence tracking)
# ═══════════════════════════════════════════════════════════════════════════════

class ProvenanceSource(BaseModel):
    """A single source reference."""
    source: str = Field(..., description="Citation or reference")
    type: str = Field(default="unknown", description="paper|book|archive|dataset|artifact|oral")
    note: Optional[str] = None
    url: Optional[str] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class ProvenanceData(BaseModel):
    """Collection of provenance sources."""
    sources: List[ProvenanceSource] = Field(default_factory=list)
    uncertainty_notes: Optional[str] = Field(None, description="Required for psychological claims")
    counter_signals: Optional[List[str]] = Field(default_factory=list, description="Required for balance")


# ═══════════════════════════════════════════════════════════════════════════════
# DATE RANGE (Flexible ancient dates)
# ═══════════════════════════════════════════════════════════════════════════════

class DateRange(BaseModel):
    """Flexible date range for ancient/uncertain dates."""
    from_date: Optional[str] = Field(None, alias="from", description="Start date, e.g., '-10000' for 10000 BCE")
    to_date: Optional[str] = Field(None, alias="to", description="End date")
    label: Optional[str] = Field(None, description="e.g., 'approx', 'circa', 'uncertain'")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    class Config:
        populate_by_name = True


class LocationData(BaseModel):
    """Geographic location with uncertainty."""
    region: Optional[str] = None
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lon: Optional[float] = Field(None, ge=-180, le=180)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# ATOM NODE
# ═══════════════════════════════════════════════════════════════════════════════

class ATOMNodeBase(BaseModel):
    """Base fields for ATOMNode."""
    name: str = Field(..., min_length=1, max_length=500)
    dimension: Optional[ATOMDimension] = None
    epoch: Optional[str] = Field(None, max_length=100)
    date_range: Optional[DateRange] = None
    location: Optional[LocationData] = None
    description: Optional[str] = None
    
    # Multi-dimensional embedded data
    technical_specs: Optional[Dict[str, Any]] = None
    biological_impact: Optional[Dict[str, Any]] = None
    social_customs: Optional[Dict[str, Any]] = None
    planetary_context: Optional[Dict[str, Any]] = None
    psychology: Optional[Dict[str, Any]] = None


class ATOMNodeCreate(ATOMNodeBase):
    """Create a new ATOMNode."""
    pass


class ATOMNodeUpdate(BaseModel):
    """Update an existing ATOMNode."""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    dimension: Optional[ATOMDimension] = None
    epoch: Optional[str] = None
    date_range: Optional[DateRange] = None
    location: Optional[LocationData] = None
    description: Optional[str] = None
    technical_specs: Optional[Dict[str, Any]] = None
    biological_impact: Optional[Dict[str, Any]] = None
    social_customs: Optional[Dict[str, Any]] = None
    planetary_context: Optional[Dict[str, Any]] = None
    psychology: Optional[Dict[str, Any]] = None


class ATOMNodeResponse(ATOMNodeBase):
    """Response model for ATOMNode."""
    id: UUID
    validation_status: ValidationStatus = ValidationStatus.PENDING
    validated_by: Optional[UUID] = None
    validated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    created_at: datetime
    modified_by: Optional[UUID] = None
    modified_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ATOMNodeFull(ATOMNodeResponse):
    """Full node with all dimension profiles."""
    sensory_profile: Optional[SensoryProfileResponse] = None
    psycho_profile: Optional[PsychoEmotionalProfileResponse] = None
    resource_footprint: Optional[ResourceFootprintResponse] = None
    conceptual_drift: Optional[ConceptualDriftResponse] = None
    logistics_network: Optional[LogisticsNetworkResponse] = None
    harmonic_signature: Optional[HarmonicSignatureResponse] = None


# ═══════════════════════════════════════════════════════════════════════════════
# CAUSAL LINKS
# ═══════════════════════════════════════════════════════════════════════════════

class CausalLinkBase(BaseModel):
    """Base for causal links."""
    trigger_id: UUID
    result_id: UUID
    link_type: CausalLinkType
    strength: float = Field(default=1.0, ge=0.0, le=10.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    rationale: Optional[str] = None
    provenance: Optional[List[ProvenanceSource]] = None

    @model_validator(mode="after")
    def high_confidence_requires_provenance(self):
        """Gate: high-confidence links MUST have provenance sources."""
        if self.confidence >= 0.75 and not self.provenance:
            raise ValueError("High-confidence links (>=0.75) require provenance sources")
        return self


class CausalLinkCreate(CausalLinkBase):
    """Create a causal link."""
    pass


class CausalLinkResponse(CausalLinkBase):
    """Response model for causal link."""
    id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CausalLinkCandidate(BaseModel):
    """A suggested (not yet created) causal link."""
    trigger_id: UUID
    result_id: UUID
    link_type: CausalLinkType
    strength: float = 1.0
    confidence: float = 0.5
    rationale: str = ""
    provenance: Optional[List[ProvenanceSource]] = None
    is_validated: bool = False
    gate_reason: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# ENCYCLOPEDIA ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

class EncyclopediaEntryBase(BaseModel):
    """Base for encyclopedia entry."""
    title: str = Field(..., min_length=1, max_length=500)
    content_html: Optional[str] = None
    content_md: Optional[str] = None
    metadata_tags: Optional[Dict[str, List[str]]] = None
    completeness: float = Field(default=0.0, ge=0.0, le=1.0)
    review_status: ReviewStatus = ReviewStatus.DRAFT
    provenance: Optional[List[ProvenanceSource]] = None


class EncyclopediaEntryCreate(EncyclopediaEntryBase):
    """Create encyclopedia entry."""
    node_id: UUID


class EncyclopediaEntryUpdate(BaseModel):
    """Update encyclopedia entry."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content_html: Optional[str] = None
    content_md: Optional[str] = None
    metadata_tags: Optional[Dict[str, List[str]]] = None
    completeness: Optional[float] = Field(None, ge=0.0, le=1.0)
    review_status: Optional[ReviewStatus] = None
    provenance: Optional[List[ProvenanceSource]] = None


class EncyclopediaEntryResponse(EncyclopediaEntryBase):
    """Response model for encyclopedia entry."""
    id: UUID
    node_id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSION PROFILES
# ═══════════════════════════════════════════════════════════════════════════════

class SensoryProfileBase(BaseModel):
    """Sensory dimension data."""
    ergonomics: Optional[Dict[str, Any]] = None
    acoustics: Optional[Dict[str, Any]] = None
    other_senses: Optional[Dict[str, Any]] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    provenance: Optional[List[ProvenanceSource]] = None


class SensoryProfileCreate(SensoryProfileBase):
    """Create sensory profile."""
    node_id: UUID


class SensoryProfileResponse(SensoryProfileBase):
    """Response for sensory profile."""
    id: UUID
    node_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class PsychoEmotionalProfileBase(BaseModel):
    """Psychology dimension data."""
    psycho_emotional: Optional[Dict[str, Any]] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    provenance: Optional[List[ProvenanceSource]] = None

    @model_validator(mode="after")
    def require_counter_signals(self):
        """Psychological claims must include counter-signals."""
        if self.psycho_emotional:
            if not self.psycho_emotional.get("counter_signals"):
                raise ValueError("Psychological claims require counter_signals for balance")
            if not self.psycho_emotional.get("uncertainty_notes"):
                raise ValueError("Psychological claims require uncertainty_notes")
        return self


class PsychoEmotionalProfileCreate(PsychoEmotionalProfileBase):
    """Create psycho-emotional profile."""
    node_id: UUID


class PsychoEmotionalProfileResponse(PsychoEmotionalProfileBase):
    """Response for psycho-emotional profile."""
    id: UUID
    node_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ResourceFootprintBase(BaseModel):
    """Resource dimension data."""
    resource_footprint: Optional[Dict[str, Any]] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    provenance: Optional[List[ProvenanceSource]] = None


class ResourceFootprintCreate(ResourceFootprintBase):
    """Create resource footprint."""
    node_id: UUID


class ResourceFootprintResponse(ResourceFootprintBase):
    """Response for resource footprint."""
    id: UUID
    node_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ConceptualDriftBase(BaseModel):
    """Conceptual dimension data."""
    conceptual_drift: Optional[Dict[str, Any]] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    provenance: Optional[List[ProvenanceSource]] = None


class ConceptualDriftCreate(ConceptualDriftBase):
    """Create conceptual drift."""
    node_id: UUID


class ConceptualDriftResponse(ConceptualDriftBase):
    """Response for conceptual drift."""
    id: UUID
    node_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class LogisticsNetworkBase(BaseModel):
    """Logistics dimension data."""
    logistics_networks: Optional[Dict[str, Any]] = None
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    provenance: Optional[List[ProvenanceSource]] = None


class LogisticsNetworkCreate(LogisticsNetworkBase):
    """Create logistics network."""
    node_id: UUID


class LogisticsNetworkResponse(LogisticsNetworkBase):
    """Response for logistics network."""
    id: UUID
    node_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class HarmonicSignatureBase(BaseModel):
    """Harmonic dimension data (CREATIVE LAYER - NOT SCIENTIFIC)."""
    numeric_signatures: Optional[Dict[str, Any]] = None
    vibration_mapping: Optional[Dict[str, Any]] = None
    is_interpretive: bool = Field(default=True, description="Always True - this is not factual")
    provenance: Optional[List[ProvenanceSource]] = None


class HarmonicSignatureCreate(HarmonicSignatureBase):
    """Create harmonic signature."""
    node_id: UUID


class HarmonicSignatureResponse(HarmonicSignatureBase):
    """Response for harmonic signature."""
    id: UUID
    node_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════════════════════
# RESONANCE SUGGESTIONS
# ═══════════════════════════════════════════════════════════════════════════════

class ResonanceSuggestion(BaseModel):
    """A suggestion for cross-dimension resonance."""
    node_id: UUID
    module: str  # sensory | psychology | resources | concepts | logistics
    payload: Dict[str, Any]
    confidence: float = 0.5
    rationale: str = ""
    provenance: Optional[List[ProvenanceSource]] = None


class UnifiedSuggestions(BaseModel):
    """Combined suggestions from all services."""
    node_id: UUID
    causal_links: List[Dict[str, Any]] = Field(default_factory=list)
    resonance: List[ResonanceSuggestion] = Field(default_factory=list)
    guardrails: Dict[str, bool] = Field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# GEMATRIA (CREATIVE LAYER)
# ═══════════════════════════════════════════════════════════════════════════════

class GematriaResult(BaseModel):
    """Result of gematria analysis (INTERPRETIVE ONLY)."""
    text: str
    normalized: str
    a1z26_sum: int
    ascii_sum: int
    token_sums: Dict[str, int]
    # Pythagorean numerology
    pythagorean: Optional[Dict[str, Any]] = None
    # Sacred geometry coords
    sacred_geometry: Optional[Dict[str, Any]] = None
    # Symbolic meaning
    meaning: Optional[Dict[str, Any]] = None
    # Mandatory flags
    is_interpretive: bool = True  # Always True
    disclaimer: str = (
        "This is a creative/interpretive tool, not scientific analysis. "
        "All numeric patterns are coincidental and carry no causal meaning."
    )


class SacredGeometryCoords(BaseModel):
    """Phi-based spiral coordinates (SYMBOLIC ONLY)."""
    x: float
    y: float
    angle_degrees: float
    radius: float
    frequency_symbolic: float
    is_interpretive: bool = True
    note: str = "Coordinates are symbolic for visualization, not physical positions"


class NumberMeaning(BaseModel):
    """Symbolic meaning of a number (TRADITIONAL INTERPRETATIONS)."""
    archetype: str
    element: str
    planet: str
    is_master: bool = False
    is_interpretive: bool = True
    note: str = "Traditional symbolic associations, not factual claims"


class GoldNodeCandidate(BaseModel):
    """A node identified by harmonic synchronizer (INTERPRETIVE)."""
    node_id: UUID
    score: float
    reasons: List[str]
    artifacts: Dict[str, Any]
    is_interpretive: bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# GUARDRAILS
# ═══════════════════════════════════════════════════════════════════════════════

class Guardrails(BaseModel):
    """Static guardrails for UI & agents."""
    no_absolute_truth_claims: bool = True
    require_sources_for_high_confidence: bool = True
    store_uncertainty_explicitly: bool = True
    human_in_the_loop: bool = True
    psycho_requires_counter_signals: bool = True
    harmonic_is_interpretive_only: bool = True


# ═══════════════════════════════════════════════════════════════════════════════
# PAGINATION
# ═══════════════════════════════════════════════════════════════════════════════

class PaginatedNodes(BaseModel):
    """Paginated list of nodes."""
    items: List[ATOMNodeResponse]
    total: int
    page: int
    size: int
    pages: int


# Forward references for full node
ATOMNodeFull.model_rebuild()


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Enums
    "ATOMDimension",
    "CausalLinkType", 
    "ValidationStatus",
    "ReviewStatus",
    # Provenance
    "ProvenanceSource",
    "ProvenanceData",
    "DateRange",
    "LocationData",
    # Node
    "ATOMNodeBase",
    "ATOMNodeCreate",
    "ATOMNodeUpdate",
    "ATOMNodeResponse",
    "ATOMNodeFull",
    # Causal Links
    "CausalLinkBase",
    "CausalLinkCreate",
    "CausalLinkResponse",
    "CausalLinkCandidate",
    # Encyclopedia
    "EncyclopediaEntryBase",
    "EncyclopediaEntryCreate",
    "EncyclopediaEntryUpdate",
    "EncyclopediaEntryResponse",
    # Dimension Profiles
    "SensoryProfileBase",
    "SensoryProfileCreate",
    "SensoryProfileResponse",
    "PsychoEmotionalProfileBase",
    "PsychoEmotionalProfileCreate",
    "PsychoEmotionalProfileResponse",
    "ResourceFootprintBase",
    "ResourceFootprintCreate",
    "ResourceFootprintResponse",
    "ConceptualDriftBase",
    "ConceptualDriftCreate",
    "ConceptualDriftResponse",
    "LogisticsNetworkBase",
    "LogisticsNetworkCreate",
    "LogisticsNetworkResponse",
    "HarmonicSignatureBase",
    "HarmonicSignatureCreate",
    "HarmonicSignatureResponse",
    # Suggestions
    "ResonanceSuggestion",
    "UnifiedSuggestions",
    # Gematria
    "GematriaResult",
    "GoldNodeCandidate",
    # Guardrails
    "Guardrails",
    # Pagination
    "PaginatedNodes",
]
