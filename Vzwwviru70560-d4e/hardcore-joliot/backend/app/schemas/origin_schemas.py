"""
═══════════════════════════════════════════════════════════════════════════════
ORIGIN-GENESIS-ULTIMA — Pydantic Schemas (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Schemas for API request/response validation.
Rule #6 compliant: all mutations require created_by.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ValidationStatus(str, Enum):
    PENDING = "pending"
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    VALIDATED = "validated"
    CONTESTED = "contested"
    ARCHIVED = "archived"


class MediaAssetType(str, Enum):
    FILM_SCRIPT = "FILM_SCRIPT"
    BOOK_CHAPTER = "BOOK_CHAPTER"
    GAME_MECHANIC = "GAME_MECHANIC"
    DOC_SCENE = "DOC_SCENE"
    VISUAL_ASSET = "VISUAL_ASSET"
    VOICE_OVER = "VOICE_OVER"


class MediaFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"
    FINAL_DRAFT = "final_draft"
    FOUNTAIN = "fountain"
    FDX = "fdx"
    PNG = "png"
    MP3 = "mp3"


class CivilizationCategory(str, Enum):
    LANGUAGE = "LANGUAGE"
    EMPIRE = "EMPIRE"
    ARCHITECTURE = "ARCHITECTURE"
    INDUSTRY = "INDUSTRY"
    COMMUNICATION = "COMMUNICATION"
    SOVEREIGNTY = "SOVEREIGNTY"
    SPACE = "SPACE"


class CustomEvolutionStage(str, Enum):
    EMERGENCE = "Emergence"
    MAINSTREAM = "Mainstream"
    OBSOLETE = "Obsolete"
    HYBRID = "Hybrid"
    REVIVING = "Reviving"


class AdaptationStage(str, Enum):
    BIOLOGICAL = "Biological"
    TECHNOLOGICAL = "Technological"
    COGNITIVE = "Cognitive"


class FeedbackType(str, Enum):
    GENE_CULTURE = "GENE_CULTURE"
    BIOEVO_FEEDBACK = "BIOEVO_FEEDBACK"
    EPIGENETIC_ENV = "EPIGENETIC_ENV"
    NICHE_CONSTRUCTION = "NICHE_CONSTRUCTION"


class LinkType(str, Enum):
    ENABLES = "ENABLES"
    DERIVES_FROM = "DERIVES_FROM"
    CORRELATES_WITH = "CORRELATES_WITH"
    IMPACTS = "IMPACTS"
    FEEDBACKS = "FEEDBACKS"
    TRIGGERS = "TRIGGERS"


class ExpertValidationType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_REVISION = "request_revision"
    FLAG = "flag"


# ═══════════════════════════════════════════════════════════════════════════════
# BASE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class OriginBase(BaseModel):
    """Base with common config"""
    model_config = ConfigDict(from_attributes=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ORIGIN NODE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class OriginNodeCreate(BaseModel):
    """Create a new origin node — Rule #6: created_by required"""
    name: str = Field(..., min_length=1, max_length=500)
    epoch: Optional[str] = Field(None, max_length=100)
    exact_date: Optional[str] = Field(None, max_length=100)
    date_start: Optional[str] = Field(None, max_length=100)
    date_end: Optional[str] = Field(None, max_length=100)
    date_certainty: float = Field(0.8, ge=0.0, le=1.0)
    description: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None
    geopolitical_context: Optional[Dict[str, Any]] = None
    created_by: UUID  # Rule #6: MANDATORY


class OriginNodeUpdate(BaseModel):
    """Update origin node — Rule #6: updated_by required"""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    epoch: Optional[str] = None
    exact_date: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    date_certainty: Optional[float] = Field(None, ge=0.0, le=1.0)
    description: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None
    geopolitical_context: Optional[Dict[str, Any]] = None
    updated_by: UUID  # Rule #6: MANDATORY


class OriginNodeResponse(OriginBase):
    """Origin node response"""
    id: UUID
    name: str
    epoch: Optional[str] = None
    exact_date: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    date_certainty: float
    description: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None
    geopolitical_context: Optional[Dict[str, Any]] = None
    is_validated: bool
    validation_status: str
    validated_by: Optional[Dict[str, Any]] = None
    created_at: datetime
    created_by: UUID
    updated_at: datetime
    updated_by: Optional[UUID] = None


class OriginNodeList(BaseModel):
    """Paginated list of nodes"""
    items: List[OriginNodeResponse]
    total: int
    page: int
    page_size: int


# ═══════════════════════════════════════════════════════════════════════════════
# CAUSAL LINK SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class CausalLinkCreate(BaseModel):
    """Create causal link between nodes"""
    trigger_id: UUID
    result_id: UUID
    link_type: LinkType = LinkType.ENABLES
    link_strength: float = Field(1.0, ge=0.0, le=1.0)
    description: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None
    created_by: UUID  # Rule #6
    validated_by_agent: Optional[str] = None


class CausalLinkResponse(OriginBase):
    """Causal link response"""
    id: UUID
    trigger_id: UUID
    result_id: UUID
    link_type: Optional[str] = None
    link_strength: float
    description: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None
    created_at: datetime
    created_by: UUID
    validated_by_agent: Optional[str] = None
    validation_timestamp: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════════════════
# MEDIA ASSET SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class MediaAssetCreate(BaseModel):
    """Create media asset linked to node"""
    node_id: UUID
    asset_type: MediaAssetType
    format: MediaFormat
    title: Optional[str] = Field(None, max_length=500)
    content: Dict[str, Any]
    production_status: str = "draft"
    created_by: UUID  # Rule #6


class MediaAssetUpdate(BaseModel):
    """Update media asset"""
    title: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    production_status: Optional[str] = None
    updated_by: UUID  # Rule #6


class MediaAssetResponse(OriginBase):
    """Media asset response"""
    id: UUID
    node_id: UUID
    asset_type: str
    format: str
    title: Optional[str] = None
    content: Dict[str, Any]
    version: int
    production_status: str
    created_at: datetime
    created_by: UUID
    updated_at: datetime
    validated_by_agent: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# CIVILIZATION PILLAR SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class CivilizationPillarCreate(BaseModel):
    """Create civilization pillar"""
    node_id: UUID
    category: CivilizationCategory
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    migration_flow: Optional[Dict[str, Any]] = None
    architectural_style: Optional[str] = None
    literature_refs: Optional[Dict[str, Any]] = None
    tools_used: Optional[Dict[str, Any]] = None
    evidence: Optional[Dict[str, Any]] = None
    created_by: UUID  # Rule #6


class CivilizationPillarResponse(OriginBase):
    """Civilization pillar response"""
    id: UUID
    node_id: UUID
    category: str
    title: Optional[str] = None
    description: Optional[str] = None
    migration_flow: Optional[Dict[str, Any]] = None
    architectural_style: Optional[str] = None
    tools_used: Optional[Dict[str, Any]] = None
    evidence: Optional[Dict[str, Any]] = None
    created_at: datetime
    created_by: UUID
    validated_by_agent: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM EVOLUTION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class CustomEvolutionCreate(BaseModel):
    """Create custom evolution record"""
    node_id: UUID
    custom_name: str = Field(..., max_length=500)
    evolution_stage: CustomEvolutionStage
    impact_on_daily_life: Optional[Dict[str, Any]] = None
    region: Optional[str] = Field(None, max_length=200)
    time_period: Optional[str] = Field(None, max_length=200)
    sources: Optional[Dict[str, Any]] = None
    created_by: UUID  # Rule #6


class CustomEvolutionResponse(OriginBase):
    """Custom evolution response"""
    id: UUID
    node_id: UUID
    custom_name: str
    evolution_stage: str
    impact_on_daily_life: Optional[Dict[str, Any]] = None
    region: Optional[str] = None
    time_period: Optional[str] = None
    sources: Optional[Dict[str, Any]] = None
    created_at: datetime
    created_by: UUID
    validated_by_agent: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# HUMAN LEGACY SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class HumanLegacyCreate(BaseModel):
    """Create human legacy record"""
    node_id: UUID
    belief_system: Optional[str] = Field(None, max_length=200)
    world_mystery_link: Optional[str] = Field(None, max_length=500)
    human_talents: Optional[Dict[str, Any]] = None
    sports_and_activities: Optional[Dict[str, Any]] = None
    planetary_event: Optional[str] = Field(None, max_length=200)
    adaptation_stage: Optional[AdaptationStage] = None
    legacy_score: float = Field(0.5, ge=0.0, le=1.0)
    evidence: Optional[Dict[str, Any]] = None
    created_by: UUID  # Rule #6


class HumanLegacyResponse(OriginBase):
    """Human legacy response"""
    id: UUID
    node_id: UUID
    belief_system: Optional[str] = None
    world_mystery_link: Optional[str] = None
    human_talents: Optional[Dict[str, Any]] = None
    sports_and_activities: Optional[Dict[str, Any]] = None
    planetary_event: Optional[str] = None
    adaptation_stage: Optional[str] = None
    legacy_score: float
    evidence: Optional[Dict[str, Any]] = None
    created_at: datetime
    created_by: UUID
    validated_by_agent: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# BIO-EVOLUTION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class BioEvolutionCreate(BaseModel):
    """Create bio-evolution record — REQUIRES evidence"""
    node_id: UUID
    genetic_mutation: Optional[str] = Field(None, max_length=200)
    biological_impact: Optional[str] = None
    env_modification: Optional[str] = Field(None, max_length=200)
    biodiversity_shift: Optional[Dict[str, Any]] = None
    feedback_loop_description: Optional[str] = None
    feedback_type: Optional[FeedbackType] = None
    evidence: Dict[str, Any] = Field(
        ...,
        description="MANDATORY: Must include sources, confidence, claim_strength"
    )
    is_hypothesis: bool = True
    confidence_level: float = Field(0.3, ge=0.0, le=1.0)
    created_by: UUID  # Rule #6


class BioEvolutionResponse(OriginBase):
    """Bio-evolution response"""
    id: UUID
    node_id: UUID
    genetic_mutation: Optional[str] = None
    biological_impact: Optional[str] = None
    env_modification: Optional[str] = None
    biodiversity_shift: Optional[Dict[str, Any]] = None
    feedback_loop_description: Optional[str] = None
    feedback_type: Optional[str] = None
    evidence: Dict[str, Any]
    is_hypothesis: bool
    confidence_level: float
    created_at: datetime
    created_by: UUID
    validated_by_agent: Optional[str] = None
    validation_notes: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# EXPERT VALIDATION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class ExpertValidationCreate(BaseModel):
    """Record expert validation — Rule #6 audit trail"""
    entity_type: str = Field(..., description="node | media | civilization | custom | legacy | bio_eco")
    entity_id: UUID
    agent_id: str = Field(..., description="Expert agent ID from AGENT_REGISTRY")
    agent_role: Optional[str] = None
    validation_type: ExpertValidationType
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    notes: Optional[str] = None
    sources_verified: Optional[List[Dict[str, Any]]] = None
    created_by: UUID  # Rule #6


class ExpertValidationResponse(OriginBase):
    """Expert validation response"""
    id: UUID
    entity_type: str
    entity_id: UUID
    agent_id: str
    agent_role: Optional[str] = None
    validation_type: str
    confidence: float
    notes: Optional[str] = None
    sources_verified: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    created_by: UUID


# ═══════════════════════════════════════════════════════════════════════════════
# NEXUS CANDIDATE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class NexusCandidateResponse(BaseModel):
    """Response from build_nexus_candidates"""
    node_id: str
    node_name: str
    epoch: Optional[str] = None
    generated_at: str
    candidates: List[Dict[str, Any]]
    total_candidates: int
    note: str
    validation_workflow: Dict[str, str]


class CausalChainResponse(BaseModel):
    """Response from get_causal_chain"""
    start_node_id: str
    chain: List[Dict[str, Any]]
    total_links: int
    max_depth_reached: int


class NodeFullContextResponse(BaseModel):
    """Full context for a node"""
    node: Dict[str, Any]
    media_assets: List[Dict[str, Any]]
    civilization_pillars: List[Dict[str, Any]]
    customs: List[Dict[str, Any]]
    legacies: List[Dict[str, Any]]
    bio_evolutions: List[Dict[str, Any]]


# ═══════════════════════════════════════════════════════════════════════════════
# UNIVERSAL LINK SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class UniversalLinkCreate(BaseModel):
    """Create universal cross-entity link"""
    from_type: str
    from_id: UUID
    to_type: str
    to_id: UUID
    relation: str
    weight: float = Field(1.0, ge=0.0, le=1.0)
    evidence: Optional[Dict[str, Any]] = None
    created_by: UUID  # Rule #6
    validated_by_agent: Optional[str] = None


class UniversalLinkResponse(OriginBase):
    """Universal link response"""
    id: UUID
    from_type: str
    from_id: UUID
    to_type: str
    to_id: UUID
    relation: str
    weight: float
    evidence: Optional[Dict[str, Any]] = None
    created_at: datetime
    created_by: UUID
    validated_by_agent: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Enums
    'ValidationStatus', 'MediaAssetType', 'MediaFormat', 'CivilizationCategory',
    'CustomEvolutionStage', 'AdaptationStage', 'FeedbackType', 'LinkType',
    'ExpertValidationType',
    # Node
    'OriginNodeCreate', 'OriginNodeUpdate', 'OriginNodeResponse', 'OriginNodeList',
    # Links
    'CausalLinkCreate', 'CausalLinkResponse',
    'UniversalLinkCreate', 'UniversalLinkResponse',
    # Media
    'MediaAssetCreate', 'MediaAssetUpdate', 'MediaAssetResponse',
    # Civilization
    'CivilizationPillarCreate', 'CivilizationPillarResponse',
    # Customs
    'CustomEvolutionCreate', 'CustomEvolutionResponse',
    # Legacy
    'HumanLegacyCreate', 'HumanLegacyResponse',
    # Bio-Eco
    'BioEvolutionCreate', 'BioEvolutionResponse',
    # Validation
    'ExpertValidationCreate', 'ExpertValidationResponse',
    # Nexus
    'NexusCandidateResponse', 'CausalChainResponse', 'NodeFullContextResponse',
]
