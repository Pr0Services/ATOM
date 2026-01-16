"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V80 — Sphere Models
═══════════════════════════════════════════════════════════════════════════════

SQLAlchemy models for all 9 spheres.

Each sphere has isolated tables with identity-scoped data (R&D Rule #3).
"""

from datetime import datetime, date
from typing import Optional
from uuid import uuid4, UUID
from decimal import Decimal
from sqlalchemy import (
    Column, String, DateTime, Text, Boolean, Integer, Float,
    ForeignKey, Enum as SQLEnum, JSON, Index, Numeric, Date
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import enum

from .base import Base, TraceabilityMixin, TimestampMixin, SphereType


# ═══════════════════════════════════════════════════════════════════════════════
# 🏠 PERSONAL SPHERE
# ═══════════════════════════════════════════════════════════════════════════════

class Note(Base, TraceabilityMixin):
    """Personal notes."""
    __tablename__ = "personal_notes"
    
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    folder: Mapped[Optional[str]] = mapped_column(String(255))
    tags: Mapped[list] = mapped_column(JSON, default=list)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    
    __table_args__ = (
        Index("ix_personal_notes_owner", "created_by"),
        Index("ix_personal_notes_folder", "created_by", "folder"),
    )


class Task(Base, TraceabilityMixin):
    """Personal tasks."""
    __tablename__ = "personal_tasks"
    
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    tags: Mapped[list] = mapped_column(JSON, default=list)
    
    __table_args__ = (
        Index("ix_personal_tasks_owner_status", "created_by", "status"),
    )


class Habit(Base, TraceabilityMixin):
    """Personal habits tracking."""
    __tablename__ = "personal_habits"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    frequency: Mapped[str] = mapped_column(String(50), default="daily")
    streak: Mapped[int] = mapped_column(Integer, default=0)
    last_completed: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    __table_args__ = (
        Index("ix_personal_habits_owner", "created_by"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 💼 BUSINESS SPHERE
# ═══════════════════════════════════════════════════════════════════════════════

class Contact(Base, TraceabilityMixin):
    """Business contacts/CRM."""
    __tablename__ = "business_contacts"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    company: Mapped[Optional[str]] = mapped_column(String(255))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Lead scoring
    lead_score: Mapped[int] = mapped_column(Integer, default=0)
    lead_status: Mapped[str] = mapped_column(String(50), default="new")
    
    # Metadata
    source: Mapped[Optional[str]] = mapped_column(String(100))
    tags: Mapped[list] = mapped_column(JSON, default=list)
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict)
    
    __table_args__ = (
        Index("ix_business_contacts_owner", "created_by"),
        Index("ix_business_contacts_company", "created_by", "company"),
    )


class Invoice(Base, TraceabilityMixin):
    """Business invoices."""
    __tablename__ = "business_invoices"
    
    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("business_contacts.id")
    )
    
    # Amounts
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), default=Decimal("0"))
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(String(50), default="draft")
    due_date: Mapped[Optional[date]] = mapped_column(Date)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Items stored as JSON
    line_items: Mapped[list] = mapped_column(JSON, default=list)
    
    __table_args__ = (
        Index("ix_business_invoices_owner", "created_by"),
        Index("ix_business_invoices_status", "created_by", "status"),
    )


class Project(Base, TraceabilityMixin):
    """Business projects."""
    __tablename__ = "business_projects"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="planning")
    
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    budget: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))
    progress: Mapped[int] = mapped_column(Integer, default=0)
    
    __table_args__ = (
        Index("ix_business_projects_owner", "created_by"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 CREATIVE STUDIO SPHERE
# ═══════════════════════════════════════════════════════════════════════════════

class CreativeAsset(Base, TraceabilityMixin):
    """Creative assets (images, videos, audio)."""
    __tablename__ = "creative_assets"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(50), nullable=False)  # image, video, audio
    
    # Storage
    file_url: Mapped[Optional[str]] = mapped_column(String(1000))
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(1000))
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    
    # AI Generation info
    generation_engine: Mapped[Optional[str]] = mapped_column(String(100))
    prompt: Mapped[Optional[str]] = mapped_column(Text)
    generation_params: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Metadata
    tags: Mapped[list] = mapped_column(JSON, default=list)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    
    __table_args__ = (
        Index("ix_creative_assets_owner", "created_by"),
        Index("ix_creative_assets_type", "created_by", "asset_type"),
    )


class CreativeProject(Base, TraceabilityMixin):
    """Creative projects (collections of assets)."""
    __tablename__ = "creative_projects"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    project_type: Mapped[str] = mapped_column(String(100))  # branding, video, campaign
    status: Mapped[str] = mapped_column(String(50), default="active")
    
    __table_args__ = (
        Index("ix_creative_projects_owner", "created_by"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 🎬 ENTERTAINMENT SPHERE
# ═══════════════════════════════════════════════════════════════════════════════

class Playlist(Base, TraceabilityMixin):
    """Entertainment playlists."""
    __tablename__ = "entertainment_playlists"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    playlist_type: Mapped[str] = mapped_column(String(50))  # video, music, mixed
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Items stored as JSON (ordered list)
    items: Mapped[list] = mapped_column(JSON, default=list)
    item_count: Mapped[int] = mapped_column(Integer, default=0)
    
    __table_args__ = (
        Index("ix_entertainment_playlists_owner", "created_by"),
    )


class StreamHistory(Base, TraceabilityMixin):
    """Streaming history (chronological, R&D Rule #5)."""
    __tablename__ = "entertainment_stream_history"
    
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)
    content_id: Mapped[str] = mapped_column(String(255), nullable=False)
    content_title: Mapped[str] = mapped_column(String(500))
    
    watched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    duration_watched: Mapped[int] = mapped_column(Integer, default=0)  # seconds
    
    __table_args__ = (
        # Chronological ordering (R&D Rule #5)
        Index("ix_entertainment_history_chrono", "created_by", "watched_at"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 👥 COMMUNITY SPHERE
# ═══════════════════════════════════════════════════════════════════════════════

class CommunityGroup(Base, TraceabilityMixin):
    """Community groups."""
    __tablename__ = "community_groups"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    group_type: Mapped[str] = mapped_column(String(50), default="general")
    
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    member_count: Mapped[int] = mapped_column(Integer, default=1)
    
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    
    __table_args__ = (
        Index("ix_community_groups_owner", "created_by"),
    )


class CommunityEvent(Base, TraceabilityMixin):
    """Community events."""
    __tablename__ = "community_events"
    
    group_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("community_groups.id")
    )
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    event_type: Mapped[str] = mapped_column(String(50), default="meetup")
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    location: Mapped[Optional[str]] = mapped_column(String(500))
    is_virtual: Mapped[bool] = mapped_column(Boolean, default=False)
    virtual_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    rsvp_count: Mapped[int] = mapped_column(Integer, default=0)
    
    __table_args__ = (
        Index("ix_community_events_owner", "created_by"),
        Index("ix_community_events_time", "start_time"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 📱 SOCIAL SPHERE (NO RANKING - R&D Rule #5)
# ═══════════════════════════════════════════════════════════════════════════════

class SocialPost(Base, TraceabilityMixin):
    """Social posts (chronological feed, NO ranking)."""
    __tablename__ = "social_posts"
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Media attachments
    media_urls: Mapped[list] = mapped_column(JSON, default=list)
    media_type: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Visibility (NOT engagement-based ranking!)
    visibility: Mapped[str] = mapped_column(String(50), default="public")
    
    # Engagement counters (for display only, NOT for ranking)
    like_count: Mapped[int] = mapped_column(Integer, default=0)
    comment_count: Mapped[int] = mapped_column(Integer, default=0)
    share_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Scheduling
    scheduled_for: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    __table_args__ = (
        # CHRONOLOGICAL index (R&D Rule #5 - NO engagement ranking)
        Index("ix_social_posts_chrono", "created_by", "created_at"),
        Index("ix_social_posts_published", "published_at"),
    )


class SocialSchedule(Base, TraceabilityMixin):
    """Social media scheduling."""
    __tablename__ = "social_schedules"
    
    post_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("social_posts.id")
    )
    
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    scheduled_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="scheduled")
    
    __table_args__ = (
        Index("ix_social_schedules_time", "scheduled_time"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 📚 SCHOLAR SPHERE
# ═══════════════════════════════════════════════════════════════════════════════

class Reference(Base, TraceabilityMixin):
    """Academic references."""
    __tablename__ = "scholar_references"
    
    # Citation info
    title: Mapped[str] = mapped_column(String(1000), nullable=False)
    authors: Mapped[list] = mapped_column(JSON, default=list)
    year: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Source
    source_type: Mapped[str] = mapped_column(String(50))  # journal, book, conference
    journal: Mapped[Optional[str]] = mapped_column(String(500))
    volume: Mapped[Optional[str]] = mapped_column(String(50))
    pages: Mapped[Optional[str]] = mapped_column(String(50))
    doi: Mapped[Optional[str]] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(1000))
    
    # Abstract
    abstract: Mapped[Optional[str]] = mapped_column(Text)
    
    # File
    pdf_url: Mapped[Optional[str]] = mapped_column(String(1000))
    
    # Tags and notes
    tags: Mapped[list] = mapped_column(JSON, default=list)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    __table_args__ = (
        Index("ix_scholar_references_owner", "created_by"),
        Index("ix_scholar_references_doi", "doi"),
    )


class Manuscript(Base, TraceabilityMixin):
    """Academic manuscripts."""
    __tablename__ = "scholar_manuscripts"
    
    title: Mapped[str] = mapped_column(String(1000), nullable=False)
    abstract: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(50), default="draft")
    
    # Content sections as JSON
    sections: Mapped[list] = mapped_column(JSON, default=list)
    
    # Submission tracking
    target_journal: Mapped[Optional[str]] = mapped_column(String(500))
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    __table_args__ = (
        Index("ix_scholar_manuscripts_owner", "created_by"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 🏛️ GOVERNMENT SPHERE
# ═══════════════════════════════════════════════════════════════════════════════

class ComplianceItem(Base, TraceabilityMixin):
    """Compliance tracking items."""
    __tablename__ = "government_compliance"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    compliance_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    status: Mapped[str] = mapped_column(String(50), default="active")
    
    # Dates
    effective_date: Mapped[Optional[date]] = mapped_column(Date)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Reference
    license_number: Mapped[Optional[str]] = mapped_column(String(100))
    issuing_authority: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Documents
    documents: Mapped[list] = mapped_column(JSON, default=list)
    
    __table_args__ = (
        Index("ix_government_compliance_owner", "created_by"),
        Index("ix_government_compliance_expiry", "expiry_date"),
    )


class ClinicalTrial(Base, TraceabilityMixin):
    """Clinical trial tracking."""
    __tablename__ = "government_clinical_trials"
    
    trial_id: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    
    phase: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(50), default="planning")
    
    # Dates
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    
    # Participants
    target_enrollment: Mapped[Optional[int]] = mapped_column(Integer)
    current_enrollment: Mapped[int] = mapped_column(Integer, default=0)
    
    # Regulatory
    reb_approval: Mapped[bool] = mapped_column(Boolean, default=False)
    reb_approval_date: Mapped[Optional[date]] = mapped_column(Date)
    
    __table_args__ = (
        Index("ix_government_trials_owner", "created_by"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 🤝 MY TEAM SPHERE (R&D Rule #4)
# ═══════════════════════════════════════════════════════════════════════════════

class TeamMember(Base, TraceabilityMixin):
    """Team members (humans)."""
    __tablename__ = "team_members"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(100))
    
    status: Mapped[str] = mapped_column(String(50), default="active")
    
    # For sorting (alphabetical, R&D Rule #5)
    sort_name: Mapped[str] = mapped_column(String(255))
    
    __table_args__ = (
        Index("ix_team_members_owner", "created_by"),
        # Alphabetical ordering (R&D Rule #5)
        Index("ix_team_members_alpha", "created_by", "sort_name"),
    )


class HiredAgent(Base, TraceabilityMixin):
    """
    Hired AI agents.
    
    R&D Rule #4: Agents cannot hire/fire other agents.
    All agent lifecycle changes require human checkpoint.
    """
    __tablename__ = "team_agents"
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    status: Mapped[str] = mapped_column(String(50), default="active")
    
    # Capabilities
    capabilities: Mapped[list] = mapped_column(JSON, default=list)
    
    # Budget
    token_budget: Mapped[int] = mapped_column(Integer, default=10000)
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
    
    # Hiring info (for R&D Rule #4 audit)
    hired_by: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=False
    )
    hired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now()
    )
    hire_checkpoint_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True))
    
    __table_args__ = (
        Index("ix_team_agents_owner", "created_by"),
    )


class TeamTask(Base, TraceabilityMixin):
    """Team tasks."""
    __tablename__ = "team_tasks"
    
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    status: Mapped[str] = mapped_column(String(50), default="pending")
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    
    # Assignment
    assignee_type: Mapped[str] = mapped_column(String(50))  # human or agent
    assignee_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True))
    
    # Dates
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    __table_args__ = (
        Index("ix_team_tasks_owner", "created_by"),
        # Chronological ordering (R&D Rule #5)
        Index("ix_team_tasks_chrono", "created_by", "created_at"),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Personal
    "Note", "Task", "Habit",
    # Business
    "Contact", "Invoice", "Project",
    # Creative
    "CreativeAsset", "CreativeProject",
    # Entertainment
    "Playlist", "StreamHistory",
    # Community
    "CommunityGroup", "CommunityEvent",
    # Social
    "SocialPost", "SocialSchedule",
    # Scholar
    "Reference", "Manuscript",
    # Government
    "ComplianceItem", "ClinicalTrial",
    # My Team
    "TeamMember", "HiredAgent", "TeamTask",
]
