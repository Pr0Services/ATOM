"""
Waitlist Schemas

Pydantic models for waitlist management.
Sources: landing page, auth flow, essaim, modules
"""

from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum
import re


# =============================================================================
# ENUMS
# =============================================================================

class WaitlistSource(str, Enum):
    """Source of waitlist signup."""
    LANDING = "landing"
    AUTH = "auth"
    ESSAIM = "essaim"
    MODULE = "module"
    REFERRAL = "referral"
    PARTNER = "partner"
    OTHER = "other"


class WaitlistStatus(str, Enum):
    """Status of waitlist entry."""
    PENDING = "pending"
    INVITED = "invited"
    REGISTERED = "registered"
    DECLINED = "declined"


# =============================================================================
# REQUEST SCHEMAS
# =============================================================================

class WaitlistSubmitRequest(BaseModel):
    """Submit email to waitlist."""

    email: EmailStr = Field(..., description="Email address to add to waitlist")
    source: WaitlistSource = Field(
        default=WaitlistSource.LANDING,
        description="Source of signup (landing, auth, essaim, module)"
    )
    campaign: Optional[str] = Field(
        None,
        max_length=100,
        description="Marketing campaign identifier"
    )
    referrer: Optional[str] = Field(
        None,
        max_length=200,
        description="Referrer URL or code"
    )
    consent: bool = Field(
        ...,
        description="User consent for communications"
    )
    metadata: Optional[dict] = Field(
        None,
        description="Additional metadata (e.g., user agent, locale)"
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Normalize email to lowercase."""
        return v.lower().strip()

    @field_validator("campaign")
    @classmethod
    def clean_campaign(cls, v: Optional[str]) -> Optional[str]:
        """Clean campaign identifier."""
        if v:
            # Remove special characters except hyphens and underscores
            v = re.sub(r"[^a-zA-Z0-9\-_]", "", v.strip())
        return v if v else None


class WaitlistCheckRequest(BaseModel):
    """Check if email exists on waitlist."""

    email: EmailStr = Field(..., description="Email to check")

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Normalize email to lowercase."""
        return v.lower().strip()


# =============================================================================
# RESPONSE SCHEMAS
# =============================================================================

class WaitlistEntry(BaseModel):
    """Complete waitlist entry data."""

    id: str = Field(..., description="Unique entry ID")
    email: str = Field(..., description="Email address")
    source: WaitlistSource = Field(..., description="Signup source")
    campaign: Optional[str] = Field(None, description="Campaign identifier")
    referrer: Optional[str] = Field(None, description="Referrer info")
    status: WaitlistStatus = Field(default=WaitlistStatus.PENDING)
    consent: bool = Field(..., description="Communication consent")
    consent_timestamp: datetime = Field(..., description="When consent was given")
    position: int = Field(..., description="Position in queue")
    created_at: datetime = Field(..., description="Signup timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    invited_at: Optional[datetime] = Field(None, description="When invitation was sent")
    registered_at: Optional[datetime] = Field(None, description="When user registered")
    metadata: Optional[dict] = Field(None, description="Additional metadata")

    class Config:
        from_attributes = True


class WaitlistResponse(BaseModel):
    """Response after waitlist submission."""

    success: bool = Field(..., description="Whether submission was successful")
    message: str = Field(..., description="Status message")
    position: Optional[int] = Field(None, description="Queue position")
    already_exists: bool = Field(default=False, description="Email already on waitlist")
    entry_id: Optional[str] = Field(None, description="Entry ID if successful")


class WaitlistCheckResponse(BaseModel):
    """Response for waitlist check."""

    exists: bool = Field(..., description="Whether email exists on waitlist")
    status: Optional[WaitlistStatus] = Field(None, description="Current status if exists")
    position: Optional[int] = Field(None, description="Queue position if pending")
    message: str = Field(..., description="Status message")


class WaitlistStats(BaseModel):
    """Waitlist statistics for admin."""

    total_entries: int = Field(..., description="Total waitlist entries")
    pending_count: int = Field(..., description="Entries awaiting invitation")
    invited_count: int = Field(..., description="Invitations sent")
    registered_count: int = Field(..., description="Users who registered")
    declined_count: int = Field(..., description="Users who declined")

    # By source breakdown
    by_source: dict = Field(..., description="Counts by source")

    # Time-based stats
    signups_today: int = Field(..., description="Signups today")
    signups_this_week: int = Field(..., description="Signups this week")
    signups_this_month: int = Field(..., description="Signups this month")

    # Conversion rates
    invite_to_register_rate: float = Field(
        ...,
        description="Percentage of invites that registered"
    )

    # Recent activity
    recent_signups: List[WaitlistEntry] = Field(
        default_factory=list,
        description="Most recent signups"
    )

    timestamp: datetime = Field(..., description="Stats generated at")


class WaitlistStatsResponse(BaseModel):
    """Admin stats response."""

    success: bool = Field(default=True)
    stats: WaitlistStats


# =============================================================================
# INTERNAL SCHEMAS
# =============================================================================

class WaitlistEntryCreate(BaseModel):
    """Internal model for creating waitlist entry."""

    email: str
    source: WaitlistSource
    campaign: Optional[str] = None
    referrer: Optional[str] = None
    consent: bool
    consent_timestamp: datetime
    metadata: Optional[dict] = None


class WaitlistEntryUpdate(BaseModel):
    """Internal model for updating waitlist entry."""

    status: Optional[WaitlistStatus] = None
    invited_at: Optional[datetime] = None
    registered_at: Optional[datetime] = None
    metadata: Optional[dict] = None


class WaitlistBulkInviteRequest(BaseModel):
    """Request to send bulk invitations."""

    count: int = Field(..., ge=1, le=1000, description="Number of users to invite")
    source_filter: Optional[WaitlistSource] = Field(
        None,
        description="Only invite from specific source"
    )
    campaign_filter: Optional[str] = Field(
        None,
        description="Only invite from specific campaign"
    )


class WaitlistBulkInviteResponse(BaseModel):
    """Response for bulk invitation."""

    success: bool
    invited_count: int
    message: str
    entry_ids: List[str] = Field(default_factory=list)
