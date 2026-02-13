"""
CHE-NU Analytics Schemas

Pydantic models for analytics event tracking, funnel metrics, and session statistics.

Funnel Steps:
1. landing_view - User views the landing page
2. cta_click - User clicks a call-to-action
3. sceau_activate - User activates their sceau (seal)
4. essaim_view - User views the essaim (swarm)
5. module_enter - User enters a module
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from enum import Enum


# =============================================================================
# ENUMS
# =============================================================================

class FunnelStepName(str, Enum):
    """Funnel step names in order."""
    LANDING_VIEW = "landing_view"
    CTA_CLICK = "cta_click"
    SCEAU_ACTIVATE = "sceau_activate"
    ESSAIM_VIEW = "essaim_view"
    MODULE_ENTER = "module_enter"


class EventCategory(str, Enum):
    """Event categories for analytics."""
    FUNNEL = "funnel"
    NAVIGATION = "navigation"
    INTERACTION = "interaction"
    ERROR = "error"
    PERFORMANCE = "performance"
    SYSTEM = "system"


# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

class AnalyticsEventCreate(BaseModel):
    """Single analytics event to track."""

    name: str = Field(..., min_length=1, max_length=100, description="Event name")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    session_id: str = Field(..., alias="sessionId", min_length=1, max_length=100, description="Session identifier")
    user_id: Optional[str] = Field(None, alias="userId", max_length=100, description="User identifier (optional)")
    properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional event properties")
    page: Optional[str] = Field(None, max_length=500, description="Current page URL or path")
    referrer: Optional[str] = Field(None, max_length=500, description="Referrer URL")

    class Config:
        populate_by_name = True

    @field_validator("name")
    @classmethod
    def validate_event_name(cls, v: str) -> str:
        """Validate and normalize event name."""
        return v.strip().lower().replace(" ", "_")


class AnalyticsEventBatchCreate(BaseModel):
    """Batch of analytics events to track."""

    events: List[AnalyticsEventCreate] = Field(..., min_length=1, max_length=100, description="List of events")


class FunnelQueryParams(BaseModel):
    """Query parameters for funnel metrics."""

    start_date: Optional[datetime] = Field(None, description="Start date for funnel data")
    end_date: Optional[datetime] = Field(None, description="End date for funnel data")
    session_id: Optional[str] = Field(None, alias="sessionId", description="Filter by specific session")


class SessionQueryParams(BaseModel):
    """Query parameters for session statistics."""

    start_date: Optional[datetime] = Field(None, description="Start date filter")
    end_date: Optional[datetime] = Field(None, description="End date filter")
    min_events: Optional[int] = Field(None, ge=1, description="Minimum events per session")
    limit: int = Field(100, ge=1, le=1000, description="Maximum sessions to return")
    offset: int = Field(0, ge=0, description="Pagination offset")


# =============================================================================
# RESPONSE SCHEMAS
# =============================================================================

class AnalyticsEventResponse(BaseModel):
    """Response for a tracked event."""

    id: str = Field(..., description="Unique event ID")
    name: str = Field(..., description="Event name")
    timestamp: datetime = Field(..., description="Event timestamp")
    session_id: str = Field(..., alias="sessionId", description="Session identifier")
    user_id: Optional[str] = Field(None, alias="userId", description="User identifier")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Event properties")
    page: Optional[str] = Field(None, description="Page URL/path")
    referrer: Optional[str] = Field(None, description="Referrer URL")
    created_at: datetime = Field(..., description="Server creation timestamp")

    class Config:
        populate_by_name = True
        from_attributes = True


class AnalyticsEventBatchResponse(BaseModel):
    """Response for batch event tracking."""

    success: bool = Field(..., description="Whether all events were tracked")
    tracked_count: int = Field(..., description="Number of events tracked")
    failed_count: int = Field(0, description="Number of events that failed")
    events: List[AnalyticsEventResponse] = Field(..., description="Tracked events")
    errors: List[str] = Field(default_factory=list, description="Error messages for failed events")


class FunnelStep(BaseModel):
    """Single step in the funnel."""

    step: int = Field(..., ge=1, le=5, description="Step number (1-5)")
    name: str = Field(..., description="Step name")
    completed: int = Field(..., ge=0, description="Number of sessions that completed this step")
    timestamp: Optional[datetime] = Field(None, description="Average timestamp for this step")
    duration: Optional[float] = Field(None, ge=0, description="Average duration from previous step (seconds)")
    conversion_rate: Optional[float] = Field(None, ge=0, le=100, description="Conversion rate from previous step (%)")


class FunnelMetrics(BaseModel):
    """Complete funnel metrics response."""

    steps: List[FunnelStep] = Field(..., description="Funnel steps with metrics")
    total_sessions: int = Field(..., ge=0, description="Total sessions in funnel")
    completed_sessions: int = Field(..., ge=0, description="Sessions that completed all steps")
    overall_conversion_rate: float = Field(..., ge=0, le=100, description="Overall funnel conversion rate (%)")
    average_duration: Optional[float] = Field(None, description="Average time through funnel (seconds)")
    start_date: Optional[datetime] = Field(None, description="Data start date")
    end_date: Optional[datetime] = Field(None, description="Data end date")


class SessionStats(BaseModel):
    """Statistics for a single session."""

    session_id: str = Field(..., alias="sessionId", description="Session identifier")
    user_id: Optional[str] = Field(None, alias="userId", description="User identifier")
    events_count: int = Field(..., alias="eventsCount", ge=0, description="Total events in session")
    funnel_progress: int = Field(..., alias="funnelProgress", ge=0, le=5, description="Furthest funnel step reached (0-5)")
    funnel_completed: bool = Field(..., alias="funnelCompleted", description="Whether funnel was completed")
    first_event_at: datetime = Field(..., alias="firstEventAt", description="First event timestamp")
    last_event_at: datetime = Field(..., alias="lastEventAt", description="Last event timestamp")
    duration_seconds: float = Field(..., alias="durationSeconds", ge=0, description="Session duration in seconds")
    pages_viewed: List[str] = Field(default_factory=list, alias="pagesViewed", description="List of pages viewed")

    class Config:
        populate_by_name = True
        from_attributes = True


class SessionStatsResponse(BaseModel):
    """Response for session statistics list."""

    sessions: List[SessionStats] = Field(..., description="Session statistics")
    total_count: int = Field(..., ge=0, description="Total sessions matching filter")
    average_events_per_session: float = Field(..., ge=0, description="Average events per session")
    average_duration: float = Field(..., ge=0, description="Average session duration (seconds)")
    funnel_completion_rate: float = Field(..., ge=0, le=100, description="Percentage completing funnel")


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str = Field(..., description="Response message")
    success: bool = Field(True, description="Operation success status")


# =============================================================================
# INTERNAL SCHEMAS
# =============================================================================

class AnalyticsEventInternal(BaseModel):
    """Internal event model with all fields."""

    id: str
    name: str
    timestamp: datetime
    session_id: str
    user_id: Optional[str] = None
    properties: Dict[str, Any] = {}
    page: Optional[str] = None
    referrer: Optional[str] = None
    created_at: datetime
    category: EventCategory = EventCategory.INTERACTION
    funnel_step: Optional[int] = None

    class Config:
        from_attributes = True


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "FunnelStepName",
    "EventCategory",
    "AnalyticsEventCreate",
    "AnalyticsEventBatchCreate",
    "FunnelQueryParams",
    "SessionQueryParams",
    "AnalyticsEventResponse",
    "AnalyticsEventBatchResponse",
    "FunnelStep",
    "FunnelMetrics",
    "SessionStats",
    "SessionStatsResponse",
    "MessageResponse",
    "AnalyticsEventInternal",
]
