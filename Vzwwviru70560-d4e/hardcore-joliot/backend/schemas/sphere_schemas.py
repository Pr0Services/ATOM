"""
CHE·NU™ Sphere Schemas

Pydantic models for sphere requests and responses.
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class SphereTypeEnum(str, Enum):
    """The 9 Spheres - FROZEN."""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE = "creative"
    COMMUNITY = "community"
    SOCIAL = "social"
    ENTERTAINMENT = "entertainment"
    TEAM = "team"
    SCHOLAR = "scholar"


class BureauSectionTypeEnum(str, Enum):
    """The 6 Bureau sections."""
    QUICK_CAPTURE = "quick_capture"
    RESUME_WORKSPACE = "resume_workspace"
    THREADS = "threads"
    DATA_FILES = "data_files"
    ACTIVE_AGENTS = "active_agents"
    MEETINGS = "meetings"


class QuickCaptureTypeEnum(str, Enum):
    """Types of quick captures."""
    NOTE = "note"
    TASK = "task"
    IDEA = "idea"
    LINK = "link"


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class SphereSummary(BaseModel):
    """Sphere summary for list views."""
    
    id: str
    type: SphereTypeEnum
    name: str
    slug: str
    icon: str
    color: str
    description: Optional[str] = None
    is_active: bool = True
    is_pinned: bool = False
    thread_count: int = 0
    active_agent_count: int = 0
    last_activity_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SphereDetail(SphereSummary):
    """Full sphere details."""
    
    identity_id: str
    display_order: int = 0
    settings: dict = {}
    bureau_sections: List["BureauSectionResponse"] = []
    recent_threads: List["ThreadSummaryResponse"] = []
    created_at: datetime
    updated_at: datetime


class SphereUpdate(BaseModel):
    """Sphere update request."""
    
    name: Optional[str] = Field(None, max_length=100)
    icon: Optional[str] = Field(None, max_length=10)
    color: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    is_pinned: Optional[bool] = None
    display_order: Optional[int] = None
    settings: Optional[dict] = None


class SphereStats(BaseModel):
    """Sphere statistics."""
    
    sphere_id: str
    period: str  # day, week, month, year
    thread_count: int = 0
    new_threads: int = 0
    total_events: int = 0
    agent_executions: int = 0
    tokens_used: int = 0
    decision_points: int = 0
    checkpoints_resolved: int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# BUREAU SECTION SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class BureauSectionResponse(BaseModel):
    """Bureau section response."""
    
    id: str
    type: BureauSectionTypeEnum
    name: str
    icon: str
    is_active: bool = True
    display_order: int = 0
    item_count: int = 0
    unread_count: int = 0
    has_unread: bool = False
    
    class Config:
        from_attributes = True


class BureauSectionContent(BaseModel):
    """Bureau section with content."""
    
    type: BureauSectionTypeEnum
    items: List[dict] = []
    pagination: Optional["PaginationResponse"] = None


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK CAPTURE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class QuickCaptureRequest(BaseModel):
    """Quick capture creation request."""
    
    content: str = Field(..., min_length=1, max_length=5000)
    type: QuickCaptureTypeEnum = QuickCaptureTypeEnum.NOTE
    tags: List[str] = []
    target_thread_id: Optional[str] = None


class QuickCaptureResponse(BaseModel):
    """Quick capture response."""
    
    id: str
    sphere_id: str
    content: str
    type: QuickCaptureTypeEnum
    status: str
    tags: List[str] = []
    target_thread_id: Optional[str] = None
    suggested_thread_id: Optional[str] = None
    source: Optional[str] = None
    created_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD SUMMARY (for sphere views)
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadSummaryResponse(BaseModel):
    """Thread summary for sphere views."""
    
    id: str
    title: Optional[str] = None
    founding_intent: str
    status: str
    event_count: int = 0
    last_event_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════════════════
# PAGINATION
# ═══════════════════════════════════════════════════════════════════════════════

class PaginationResponse(BaseModel):
    """Pagination metadata."""
    
    page: int = 1
    page_size: int = 20
    total: int = 0
    total_pages: int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# LIST RESPONSES
# ═══════════════════════════════════════════════════════════════════════════════

class SphereListResponse(BaseModel):
    """List of spheres."""
    
    spheres: List[SphereSummary]
    total: int


class BureauSectionListResponse(BaseModel):
    """List of bureau sections."""
    
    sections: List[BureauSectionResponse]


# Update forward references
SphereDetail.model_rebuild()
BureauSectionContent.model_rebuild()
