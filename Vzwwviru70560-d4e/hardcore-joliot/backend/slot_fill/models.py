"""
============================================================================
CHE·NU™ V69 — SLOT FILL ENGINE MODELS
============================================================================
Version: 1.0.0
Specs: GPT1/CHE-NU_ENG_SLOT_FILL_*.md
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
import uuid


# ============================================================================
# SLOT TYPES
# ============================================================================

class SlotType(str, Enum):
    """Types of slots - mapped to specialized agents"""
    TEXT = "text"
    NUMBER = "number"
    LIST = "list"
    LEGAL = "legal"
    FINANCE = "finance"
    BRAND = "brand"
    DATE = "date"
    BOOLEAN = "boolean"
    REFERENCE = "reference"
    CUSTOM = "custom"


class SlotStatus(str, Enum):
    """Slot fill status"""
    EMPTY = "empty"
    PENDING = "pending"
    FILLED = "filled"
    VALIDATED = "validated"
    FAILED = "failed"
    BLOCKED = "blocked"  # Requires HITL


class RiskLevel(str, Enum):
    """Risk level for slots"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# AGENT TYPES (per spec)
# ============================================================================

class AgentType(str, Enum):
    """Specialized agent types for slot filling"""
    WRITING_AGENT = "writing_agent"
    DATA_AGENT = "data_agent"
    PLANNING_AGENT = "planning_agent"
    COMPLIANCE_AGENT = "compliance_agent"
    FINANCE_AGENT = "finance_agent"
    BRAND_GUARD_AGENT = "brand_guard_agent"
    VERIFICATION_AGENT = "verification_agent"


# Mapping from slot type to agent (per spec)
SLOT_TO_AGENT_MAPPING: Dict[SlotType, AgentType] = {
    SlotType.TEXT: AgentType.WRITING_AGENT,
    SlotType.NUMBER: AgentType.DATA_AGENT,
    SlotType.LIST: AgentType.PLANNING_AGENT,
    SlotType.LEGAL: AgentType.COMPLIANCE_AGENT,
    SlotType.FINANCE: AgentType.FINANCE_AGENT,
    SlotType.BRAND: AgentType.BRAND_GUARD_AGENT,
    SlotType.DATE: AgentType.DATA_AGENT,
    SlotType.BOOLEAN: AgentType.DATA_AGENT,
    SlotType.REFERENCE: AgentType.DATA_AGENT,
    SlotType.CUSTOM: AgentType.WRITING_AGENT,
}


# ============================================================================
# SLOT MODEL
# ============================================================================

class Slot(BaseModel):
    """
    A fillable slot in a document or template.
    
    Per spec:
    - 1 slot = 1 agent principal
    - Aucun agent ne contrôle tout le document
    """
    
    slot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    
    # Type and mapping
    slot_type: SlotType
    assigned_agent: Optional[AgentType] = None
    
    # Status
    status: SlotStatus = SlotStatus.EMPTY
    risk_level: RiskLevel = RiskLevel.LOW
    
    # Value
    value: Optional[Any] = None
    default_value: Optional[Any] = None
    constraints: Dict[str, Any] = Field(default_factory=dict)
    
    # Causal priority (per CAUSAL_PRIORITY spec)
    causal_impact: float = 0.0  # 0-1
    sensitivity_score: float = 0.0  # 0-1
    priority_rank: int = 0
    
    # Explainability (per EXPLAINABILITY spec)
    explainability: Optional["SlotExplainability"] = None
    
    # Tracking
    fill_attempts: int = 0
    max_attempts: int = 2  # Per spec: if fails 2 times → HITL
    
    # Metadata
    document_id: Optional[str] = None
    section_id: Optional[str] = None
    parent_slot_id: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    filled_at: Optional[datetime] = None
    validated_at: Optional[datetime] = None
    
    def auto_assign_agent(self) -> AgentType:
        """Auto-assign agent based on slot type"""
        self.assigned_agent = SLOT_TO_AGENT_MAPPING.get(
            self.slot_type,
            AgentType.WRITING_AGENT
        )
        return self.assigned_agent
    
    def requires_hitl(self) -> bool:
        """Check if slot requires human-in-the-loop"""
        # Per spec: risk=high → HITL immédiat
        if self.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            return True
        # Per spec: fails 2 times → HITL
        if self.fill_attempts >= self.max_attempts:
            return True
        return False
    
    def is_blocking(self) -> bool:
        """Check if slot is blocking other slots"""
        return self.status == SlotStatus.BLOCKED or self.requires_hitl()


# ============================================================================
# EXPLAINABILITY MODEL (per spec)
# ============================================================================

class SlotExplainability(BaseModel):
    """
    Explainability layer for slot filling.
    
    Per spec: Each filled slot generates:
    - une justification textuelle
    - les sources utilisées
    - les hypothèses éventuelles
    - le score de confiance
    """
    
    slot_id: str
    decision_summary: str  # Brief summary of the decision
    rationale: str  # Why this content
    
    # Sources and evidence
    sources: List[str] = Field(default_factory=list)
    hypotheses: List[str] = Field(default_factory=list)
    
    # Validation
    constraints_respected: bool = True
    confidence_score: float = 0.0  # 0-1
    
    # Audit
    generated_by: str  # Agent ID
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    
    def is_valid_for_export(self) -> bool:
        """Per spec: Aucun export sans explainability validée"""
        return (
            self.constraints_respected and
            self.confidence_score >= 0.5 and
            len(self.rationale) > 0
        )


# ============================================================================
# XR VISUALIZATION MODEL (per spec)
# ============================================================================

class XRSlotVisualization(BaseModel):
    """
    XR visualization for slot structure.
    
    Per spec:
    - Chaque section = node spatial
    - Chaque slot = capsule
    - Couleurs: Vert=validé, Jaune=rempli non validé, Rouge=manquant
    - XR = lecture seule (OPA rule XR_READ_ONLY)
    """
    
    slot_id: str
    
    # Spatial position
    position: Dict[str, float] = Field(
        default_factory=lambda: {"x": 0, "y": 0, "z": 0}
    )
    
    # Visual properties
    color: str = "red"  # red, yellow, green
    shape: str = "capsule"
    size: float = 1.0
    
    # Status mapping
    @staticmethod
    def get_color_for_status(status: SlotStatus) -> str:
        """Map slot status to XR color"""
        color_map = {
            SlotStatus.EMPTY: "red",
            SlotStatus.PENDING: "yellow",
            SlotStatus.FILLED: "yellow",
            SlotStatus.VALIDATED: "green",
            SlotStatus.FAILED: "red",
            SlotStatus.BLOCKED: "red",
        }
        return color_map.get(status, "gray")
    
    # Connections to other slots
    connections: List[str] = Field(default_factory=list)  # slot_ids
    
    # Explainability preview (shown on selection)
    explainability_preview: Optional[str] = None
    
    # Interaction flags
    selectable: bool = True
    read_only: bool = True  # Per spec: XR = lecture seule


# ============================================================================
# CAUSAL PRIORITY MODEL (per spec)
# ============================================================================

class CausalPriority(BaseModel):
    """
    Causal priority for slot filling.
    
    Per spec:
    - mesure l'impact
    - calcule la sensibilité
    - ignore les variables négligeables
    """
    
    slot_id: str
    
    # Impact scores
    causal_impact: float = 0.0  # 0-1, how much this slot affects outcomes
    sensitivity: float = 0.0  # 0-1, how sensitive the system is to this slot
    uncertainty: float = 0.0  # 0-1, uncertainty in the value
    
    # Priority calculation
    priority_score: float = 0.0  # Combined score
    priority_rank: int = 0  # Rank among all slots
    
    # Thresholds
    impact_threshold: float = 0.1  # Below this = ignored
    
    # Justification
    justification: str = ""
    contributing_factors: List[str] = Field(default_factory=list)
    
    # Computed flag
    is_negligible: bool = False  # True if impact < threshold
    
    def compute_priority(self) -> float:
        """Compute priority score based on causal factors"""
        if self.causal_impact < self.impact_threshold:
            self.is_negligible = True
            self.priority_score = 0.0
        else:
            self.is_negligible = False
            # Weight: impact most important, then sensitivity, then uncertainty
            self.priority_score = (
                0.5 * self.causal_impact +
                0.3 * self.sensitivity +
                0.2 * self.uncertainty
            )
        return self.priority_score


# ============================================================================
# SLOT FILL REQUEST/RESULT
# ============================================================================

class SlotFillRequest(BaseModel):
    """Request to fill a slot"""
    
    slot_id: str
    context: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 0
    
    # Requester info
    requested_by: str
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class SlotFillResult(BaseModel):
    """Result of slot filling"""
    
    slot_id: str
    success: bool
    
    # Value
    value: Optional[Any] = None
    
    # Agent info
    filled_by_agent: Optional[AgentType] = None
    verified_by_agent: Optional[AgentType] = None
    
    # Explainability (required per spec)
    explainability: Optional[SlotExplainability] = None
    
    # Status
    requires_hitl: bool = False
    error_message: Optional[str] = None
    
    # Audit
    trace_id: str
    filled_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# DOCUMENT MODEL
# ============================================================================

class Document(BaseModel):
    """
    A document containing multiple slots.
    
    Per spec: Aucun agent ne contrôle tout le document
    """
    
    document_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    
    # Structure
    sections: List[str] = Field(default_factory=list)
    slots: Dict[str, Slot] = Field(default_factory=dict)
    
    # Status
    total_slots: int = 0
    filled_slots: int = 0
    validated_slots: int = 0
    blocked_slots: int = 0
    
    # Metadata
    tenant_id: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def add_slot(self, slot: Slot) -> None:
        """Add a slot to the document"""
        slot.document_id = self.document_id
        self.slots[slot.slot_id] = slot
        self.total_slots += 1
    
    def get_slots_by_status(self, status: SlotStatus) -> List[Slot]:
        """Get slots by status"""
        return [s for s in self.slots.values() if s.status == status]
    
    def get_priority_ordered_slots(self) -> List[Slot]:
        """Get slots ordered by causal priority"""
        return sorted(
            self.slots.values(),
            key=lambda s: s.priority_rank,
            reverse=True
        )
    
    def update_counts(self) -> None:
        """Update slot counts"""
        self.total_slots = len(self.slots)
        self.filled_slots = len([s for s in self.slots.values() if s.status in [SlotStatus.FILLED, SlotStatus.VALIDATED]])
        self.validated_slots = len([s for s in self.slots.values() if s.status == SlotStatus.VALIDATED])
        self.blocked_slots = len([s for s in self.slots.values() if s.is_blocking()])
    
    @property
    def completion_percentage(self) -> float:
        """Document completion percentage"""
        if self.total_slots == 0:
            return 0.0
        return (self.filled_slots / self.total_slots) * 100


# ============================================================================
# UPDATE FORWARD REFS
# ============================================================================

Slot.model_rebuild()
