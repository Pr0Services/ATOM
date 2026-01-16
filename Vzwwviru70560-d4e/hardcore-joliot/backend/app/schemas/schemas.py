"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — PYDANTIC SCHEMAS
═══════════════════════════════════════════════════════════════════════════════
API request/response schemas with full R&D Rules compliance

Rule #6: All responses include id, created_by, created_at
Rule #7: SphereType and BureauSection enums are frozen
═══════════════════════════════════════════════════════════════════════════════
"""

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS (Rule #7: Frozen)
# ═══════════════════════════════════════════════════════════════════════════════

class SphereType(str, Enum):
    """9 Spheres - FROZEN (Rule #7)"""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE_STUDIO = "creative_studio"
    COMMUNITY = "community"
    SOCIAL_MEDIA = "social_media"
    ENTERTAINMENT = "entertainment"
    MY_TEAM = "my_team"
    SCHOLAR = "scholar"


class BureauSection(str, Enum):
    """6 Bureau Sections - FROZEN (Rule #7)"""
    QUICK_CAPTURE = "quick_capture"
    RESUME_WORKSPACE = "resume_workspace"
    THREADS = "threads"
    DATA_FILES = "data_files"
    ACTIVE_AGENTS = "active_agents"
    MEETINGS = "meetings"


class ThreadStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    MATURING = "maturing"
    DECISION_READY = "decision_ready"
    DECIDED = "decided"
    ARCHIVED = "archived"


class CheckpointStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class CheckpointType(str, Enum):
    DELETE = "delete"
    ARCHIVE = "archive"
    CRITICAL_DECISION = "critical_decision"
    TRANSFER = "transfer"
    EXTERNAL_ACTION = "external_action"


class DecisionSeverity(str, Enum):
    INFORMATIONAL = "informational"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"


class MemoryLayer(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


# ═══════════════════════════════════════════════════════════════════════════════
# BASE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class TrackedBase(BaseModel):
    """Base schema with traceability (Rule #6)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID


class PaginatedResponse(BaseModel):
    """Paginated list response"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTITY SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class IdentityCreate(BaseModel):
    """Create identity request"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8)


class IdentityUpdate(BaseModel):
    """Update identity request"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None


class IdentityResponse(TrackedBase):
    """Identity response"""
    email: EmailStr
    name: str
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str]
    preferences: Optional[Dict[str, Any]]


class IdentityWithSpheres(IdentityResponse):
    """Identity with spheres (Rule #7: always 9)"""
    spheres: List["SphereResponse"]


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE SCHEMAS (Rule #7: 9 Spheres Frozen)
# ═══════════════════════════════════════════════════════════════════════════════

class SphereCreate(BaseModel):
    """Create sphere (auto-created with identity)"""
    sphere_type: SphereType
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class SphereUpdate(BaseModel):
    """Update sphere"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class SphereResponse(TrackedBase):
    """Sphere response"""
    owner_id: UUID
    sphere_type: SphereType
    name: str
    description: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    is_active: bool
    settings: Optional[Dict[str, Any]]


# ═══════════════════════════════════════════════════════════════════════════════
# WORKSPACE SCHEMAS (Rule #7: 6 Bureau Sections)
# ═══════════════════════════════════════════════════════════════════════════════

class WorkspaceCreate(BaseModel):
    """Create workspace"""
    sphere_id: UUID
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_default: bool = False


class WorkspaceUpdate(BaseModel):
    """Update workspace"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class WorkspaceResponse(TrackedBase):
    """Workspace response"""
    sphere_id: UUID
    name: str
    description: Optional[str]
    sections: Dict[str, Any]  # 6 bureau sections
    is_default: bool
    settings: Optional[Dict[str, Any]]


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadCreate(BaseModel):
    """Create thread"""
    title: str = Field(..., min_length=1, max_length=500)
    founding_intent: str = Field(..., min_length=1)
    sphere_id: Optional[UUID] = None
    parent_thread_id: Optional[UUID] = None
    tags: Optional[List[str]] = None


class ThreadUpdate(BaseModel):
    """Update thread"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    status: Optional[ThreadStatus] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ThreadResponse(TrackedBase):
    """Thread response"""
    owner_id: UUID
    sphere_id: Optional[UUID]
    parent_thread_id: Optional[UUID]
    title: str
    founding_intent: str
    status: ThreadStatus
    maturity_score: int
    tags: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]


class ThreadWithEvents(ThreadResponse):
    """Thread with events"""
    events: List["ThreadEventResponse"]
    decisions: List["DecisionResponse"]


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD EVENT SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadEventCreate(BaseModel):
    """Create thread event"""
    thread_id: UUID
    event_type: str = Field(..., min_length=1, max_length=100)
    event_data: Dict[str, Any]
    parent_event_id: Optional[UUID] = None


class ThreadEventResponse(TrackedBase):
    """Thread event response (immutable)"""
    thread_id: UUID
    event_type: str
    event_data: Dict[str, Any]
    parent_event_id: Optional[UUID]
    sequence_number: int


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class DecisionCreate(BaseModel):
    """Create decision"""
    thread_id: UUID
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    severity: DecisionSeverity = DecisionSeverity.INFORMATIONAL
    rationale: Optional[str] = None


class DecisionUpdate(BaseModel):
    """Update decision"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    outcome: Optional[str] = None
    is_final: Optional[bool] = None


class DecisionResponse(TrackedBase):
    """Decision response"""
    thread_id: UUID
    title: str
    description: Optional[str]
    severity: DecisionSeverity
    checkpoint_id: Optional[UUID]
    rationale: Optional[str]
    outcome: Optional[str]
    is_final: bool


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT SCHEMAS (Rule #1: Human Sovereignty)
# ═══════════════════════════════════════════════════════════════════════════════

class CheckpointCreate(BaseModel):
    """Create checkpoint (internal use)"""
    checkpoint_type: CheckpointType
    resource_type: str
    resource_id: UUID
    action_type: str
    action_data: Dict[str, Any]


class CheckpointApprove(BaseModel):
    """Approve checkpoint"""
    reason: Optional[str] = None


class CheckpointReject(BaseModel):
    """Reject checkpoint"""
    reason: str = Field(..., min_length=1)


class CheckpointResponse(TrackedBase):
    """Checkpoint response (HTTP 423)"""
    checkpoint_type: CheckpointType
    status: CheckpointStatus
    resource_type: str
    resource_id: UUID
    action_type: str
    action_data: Dict[str, Any]
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    rejection_reason: Optional[str]
    expires_at: datetime


class HTTP423Response(BaseModel):
    """HTTP 423 LOCKED response"""
    status: str = "checkpoint_required"
    checkpoint_id: UUID
    checkpoint_type: CheckpointType
    message: str
    action_required: str = "approve_or_reject"
    expires_at: datetime


# ═══════════════════════════════════════════════════════════════════════════════
# DATASPACE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class DataSpaceCreate(BaseModel):
    """Create dataspace"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_encrypted: bool = True


class DataSpaceUpdate(BaseModel):
    """Update dataspace"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DataSpaceResponse(TrackedBase):
    """DataSpace response"""
    owner_id: UUID
    name: str
    description: Optional[str]
    is_encrypted: bool
    storage_bytes: int
    file_count: int
    metadata: Optional[Dict[str, Any]]


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT SCHEMAS (Rule #4: No AI-to-AI)
# ═══════════════════════════════════════════════════════════════════════════════

class AgentCreate(BaseModel):
    """Create agent"""
    name: str = Field(..., min_length=1, max_length=255)
    agent_type: str = Field(..., min_length=1, max_length=100)
    sphere_id: Optional[UUID] = None
    capabilities: Optional[List[str]] = None
    token_budget: int = Field(default=10000, ge=0)


class AgentUpdate(BaseModel):
    """Update agent"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    capabilities: Optional[List[str]] = None
    token_budget: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class AgentResponse(TrackedBase):
    """Agent response"""
    owner_id: UUID
    name: str
    agent_type: str
    sphere_id: Optional[UUID]
    capabilities: List[str]
    can_call_other_agents: bool  # Always False (Rule #4)
    token_budget: int
    tokens_used: int
    is_active: bool
    is_hired: bool


class AgentHire(BaseModel):
    """Hire agent"""
    agent_id: UUID
    sphere_id: UUID


class HTTP403AgentResponse(BaseModel):
    """HTTP 403 for AI-to-AI violation (Rule #4)"""
    status: str = "forbidden"
    rule: str = "R&D Rule #4"
    message: str = "AI-to-AI orchestration is forbidden"
    detail: str = "Agents cannot call other agents directly"


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class MemorySnapshotCreate(BaseModel):
    """Create memory snapshot"""
    thread_id: UUID
    layer: MemoryLayer = MemoryLayer.WARM
    snapshot_data: Dict[str, Any]


class MemorySnapshotResponse(TrackedBase):
    """Memory snapshot response"""
    thread_id: UUID
    layer: MemoryLayer
    snapshot_data: Dict[str, Any]
    compression_ratio: Optional[float]
    events_included: int


class TriLayerMemoryResponse(BaseModel):
    """Tri-layer memory status"""
    thread_id: UUID
    hot: Optional[Dict[str, Any]]
    warm: Optional[Dict[str, Any]]
    cold_count: int


# ═══════════════════════════════════════════════════════════════════════════════
# NOVA PIPELINE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class NovaRequest(BaseModel):
    """Nova pipeline request"""
    intent: str = Field(..., min_length=1)
    context: Optional[Dict[str, Any]] = None
    thread_id: Optional[UUID] = None
    sphere_id: Optional[UUID] = None
    options: Optional[Dict[str, Any]] = None


class NovaLaneResult(BaseModel):
    """Result from a Nova lane"""
    lane: str
    status: str
    data: Optional[Dict[str, Any]]
    duration_ms: int


class NovaResponse(BaseModel):
    """Nova pipeline response"""
    execution_id: UUID
    status: str
    lanes: List[NovaLaneResult]
    checkpoint_required: bool
    checkpoint_id: Optional[UUID]
    total_duration_ms: int


# ═══════════════════════════════════════════════════════════════════════════════
# MEETING SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class MeetingCreate(BaseModel):
    """Create meeting"""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    workspace_id: Optional[UUID] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: int = Field(default=30, ge=5)


class MeetingUpdate(BaseModel):
    """Update meeting"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=5)
    status: Optional[str] = None
    notes: Optional[str] = None
    action_items: Optional[List[Dict[str, Any]]] = None


class MeetingResponse(TrackedBase):
    """Meeting response"""
    owner_id: UUID
    workspace_id: Optional[UUID]
    title: str
    description: Optional[str]
    scheduled_at: Optional[datetime]
    duration_minutes: int
    status: str
    notes: Optional[str]
    action_items: Optional[List[Dict[str, Any]]]


# ═══════════════════════════════════════════════════════════════════════════════
# NOTIFICATION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class NotificationCreate(BaseModel):
    """Create notification (internal)"""
    notification_type: str
    title: str
    message: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[UUID] = None


class NotificationResponse(TrackedBase):
    """Notification response"""
    owner_id: UUID
    notification_type: str
    title: str
    message: Optional[str]
    is_read: bool
    read_at: Optional[datetime]
    resource_type: Optional[str]
    resource_id: Optional[UUID]


# ═══════════════════════════════════════════════════════════════════════════════
# XR SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class XRBlueprintRequest(BaseModel):
    """Generate XR blueprint"""
    thread_id: UUID
    template: str = "personal_room"
    options: Optional[Dict[str, Any]] = None


class XRZone(BaseModel):
    """XR canonical zone"""
    zone_type: str
    position: Dict[str, float]
    content: Optional[Dict[str, Any]]


class XRBlueprintResponse(BaseModel):
    """XR environment blueprint"""
    thread_id: UUID
    template: str
    zones: List[XRZone]
    metadata: Dict[str, Any]
    generated_at: datetime


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class TokenRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    """Refresh token request"""
    refresh_token: str


# ═══════════════════════════════════════════════════════════════════════════════
# STATS SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class APIStats(BaseModel):
    """API statistics"""
    version: str
    routers: int
    endpoints: int
    uptime_seconds: float
    requests_total: int
    active_checkpoints: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str
    database: str
    cache: str
    timestamp: datetime


# Forward references
IdentityWithSpheres.model_rebuild()
ThreadWithEvents.model_rebuild()
