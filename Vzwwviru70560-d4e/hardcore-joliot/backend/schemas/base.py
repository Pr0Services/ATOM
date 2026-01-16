"""
CHE·NU™ V75 Backend - Base Schemas

Common types and response formats.

@version 75.0.0
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Generic, TypeVar
from datetime import datetime
from enum import Enum
import uuid


# ============================================================================
# GENERIC TYPE
# ============================================================================

T = TypeVar("T")


# ============================================================================
# BASE RESPONSE
# ============================================================================

class Meta(BaseModel):
    """Response metadata."""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "v1"


class ErrorDetail(BaseModel):
    """Error details."""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class BaseResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    data: Optional[T] = None
    meta: Meta = Field(default_factory=Meta)


class ErrorResponse(BaseModel):
    """Error response."""
    success: bool = False
    error: ErrorDetail
    meta: Meta = Field(default_factory=Meta)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response."""
    success: bool = True
    data: List[T] = []
    pagination: "PaginationMeta"
    meta: Meta = Field(default_factory=Meta)


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    page: int = 1
    limit: int = 20
    total: int = 0
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False


# ============================================================================
# ENUMS
# ============================================================================

class SphereId(str, Enum):
    """9 Canonical Spheres - FROZEN."""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    STUDIO = "studio"
    COMMUNITY = "community"
    SOCIAL = "social"
    ENTERTAINMENT = "entertainment"
    TEAM = "team"
    SCHOLAR = "scholar"


class BureauId(str, Enum):
    """6 Canonical Bureaus - FROZEN."""
    QUICK_CAPTURE = "quick_capture"
    RESUME_WORKSPACE = "resume_workspace"
    THREADS = "threads"
    DATA_FILES = "data_files"
    ACTIVE_AGENTS = "active_agents"
    MEETINGS = "meetings"


class AgentLevel(str, Enum):
    """Agent hierarchy levels."""
    L0 = "L0"  # System (Nova only)
    L1 = "L1"  # Personal
    L2 = "L2"  # Specialized
    L3 = "L3"  # Enterprise


class AgentStatus(str, Enum):
    """Agent status."""
    AVAILABLE = "available"
    HIRED = "hired"
    BUSY = "busy"
    OFFLINE = "offline"


class ThreadStatus(str, Enum):
    """Thread status."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CheckpointType(str, Enum):
    """Governance checkpoint types."""
    GOVERNANCE = "governance"
    COST = "cost"
    IDENTITY = "identity"
    SENSITIVE = "sensitive"
    AGENT = "agent"
    EXTERNAL = "external"


class CheckpointStatus(str, Enum):
    """Checkpoint status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class DecisionType(str, Enum):
    """Decision types."""
    APPROVAL = "approval"
    CHOICE = "choice"
    CONFIRMATION = "confirmation"
    INPUT = "input"
    ESCALATION = "escalation"


class DecisionStatus(str, Enum):
    """Decision status."""
    PENDING = "pending"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class XREnvironmentType(str, Enum):
    """XR environment types."""
    SANCTUAIRE = "sanctuaire"
    COMMAND_CENTER = "command_center"
    DATA_VISUALIZATION = "data_visualization"
    MEETING_SPACE = "meeting_space"
    FOCUS_ZONE = "focus_zone"


# ============================================================================
# BASE ENTITIES
# ============================================================================

class BaseEntity(BaseModel):
    """Base entity with common fields."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# QUERY PARAMETERS
# ============================================================================

class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)


class SortParams(BaseModel):
    """Sorting query parameters."""
    sort_by: Optional[str] = None
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")


class FilterParams(BaseModel):
    """Common filter parameters."""
    sphere_id: Optional[SphereId] = None
    status: Optional[str] = None
    search: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
