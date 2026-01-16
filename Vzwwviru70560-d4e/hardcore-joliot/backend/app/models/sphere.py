"""
CHE·NU™ Sphere Models

SQLAlchemy models for the 9 Spheres and Bureau sections.

The 9 Spheres (FROZEN - cannot change):
- Personal, Business, Government, Creative, Community
- Social, Entertainment, Team, Scholar
"""

from datetime import datetime
from typing import Optional, List
from uuid import uuid4
from enum import Enum

from sqlalchemy import String, Boolean, DateTime, Text, JSON, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class SphereType(str, Enum):
    """The 9 Spheres - FROZEN, cannot be modified."""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE = "creative"
    COMMUNITY = "community"
    SOCIAL = "social"
    ENTERTAINMENT = "entertainment"
    TEAM = "team"
    SCHOLAR = "scholar"


class BureauSectionType(str, Enum):
    """The 6 Bureau sections per sphere."""
    QUICK_CAPTURE = "quick_capture"
    RESUME_WORKSPACE = "resume_workspace"
    THREADS = "threads"
    DATA_FILES = "data_files"
    ACTIVE_AGENTS = "active_agents"
    MEETINGS = "meetings"


# Sphere metadata (icons, colors, descriptions)
SPHERE_METADATA = {
    SphereType.PERSONAL: {
        "name": "Personal",
        "icon": "🏠",
        "color": "#4F46E5",
        "description": "Private life, notes, tasks, habits, goals",
    },
    SphereType.BUSINESS: {
        "name": "Business",
        "icon": "💼",
        "color": "#059669",
        "description": "Enterprise, CRM, invoicing, projects, finance",
    },
    SphereType.GOVERNMENT: {
        "name": "Government",
        "icon": "🏛️",
        "color": "#7C3AED",
        "description": "Institutional relations, compliance, regulations",
    },
    SphereType.CREATIVE: {
        "name": "Creative Studio",
        "icon": "🎨",
        "color": "#EC4899",
        "description": "Creation, design, media, AI generation",
    },
    SphereType.COMMUNITY: {
        "name": "Community",
        "icon": "👥",
        "color": "#F59E0B",
        "description": "Groups, events, coordination, volunteering",
    },
    SphereType.SOCIAL: {
        "name": "Social & Media",
        "icon": "📱",
        "color": "#3B82F6",
        "description": "Social networks, publishing, scheduling",
    },
    SphereType.ENTERTAINMENT: {
        "name": "Entertainment",
        "icon": "🎬",
        "color": "#EF4444",
        "description": "Streaming, games, entertainment content",
    },
    SphereType.TEAM: {
        "name": "My Team",
        "icon": "🤝",
        "color": "#14B8A6",
        "description": "Team collaboration, HR, resources",
    },
    SphereType.SCHOLAR: {
        "name": "Scholar",
        "icon": "📚",
        "color": "#8B5CF6",
        "description": "Research, academic, learning, knowledge",
    },
}

BUREAU_SECTION_METADATA = {
    BureauSectionType.QUICK_CAPTURE: {
        "name": "Quick Capture",
        "icon": "📥",
        "description": "Inbox for quick notes and captures",
    },
    BureauSectionType.RESUME_WORKSPACE: {
        "name": "Resume Workspace",
        "icon": "📂",
        "description": "Main workspace for active work",
    },
    BureauSectionType.THREADS: {
        "name": "Threads",
        "icon": "🧵",
        "description": "All threads in this sphere",
    },
    BureauSectionType.DATA_FILES: {
        "name": "Data & Files",
        "icon": "📁",
        "description": "Files and documents",
    },
    BureauSectionType.ACTIVE_AGENTS: {
        "name": "Active Agents",
        "icon": "🤖",
        "description": "Running AI agents",
    },
    BureauSectionType.MEETINGS: {
        "name": "Meetings",
        "icon": "📅",
        "description": "Calendar and meetings",
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# SPHERE MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class Sphere(Base):
    """
    User's sphere instance.
    
    Each user has 9 spheres (one of each type).
    Spheres are created automatically on user registration.
    """
    
    __tablename__ = "spheres"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    # Identity boundary
    identity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
    )
    
    # Sphere type (one of 9)
    sphere_type: Mapped[SphereType] = mapped_column(
        SQLEnum(SphereType),
        nullable=False,
    )
    
    # Display name (can be customized)
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    
    # Slug for URL
    slug: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    
    # Customization
    icon: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    
    color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    is_pinned: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    
    # Display order
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # Settings
    settings: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    
    # Statistics (cached, updated periodically)
    thread_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    active_agent_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    last_activity_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    
    # Relationships
    bureau_sections: Mapped[List["BureauSection"]] = relationship(
        "BureauSection",
        back_populates="sphere",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        return f"<Sphere {self.sphere_type.value} ({self.identity_id})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "identity_id": self.identity_id,
            "type": self.sphere_type.value,
            "name": self.name,
            "slug": self.slug,
            "icon": self.icon,
            "color": self.color,
            "description": self.description,
            "is_active": self.is_active,
            "is_pinned": self.is_pinned,
            "display_order": self.display_order,
            "thread_count": self.thread_count,
            "active_agent_count": self.active_agent_count,
            "settings": self.settings,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_activity_at": self.last_activity_at.isoformat() if self.last_activity_at else None,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# BUREAU SECTION MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class BureauSection(Base):
    """
    Bureau section within a sphere.
    
    Each sphere has exactly 6 bureau sections.
    Sections are created automatically with the sphere.
    """
    
    __tablename__ = "bureau_sections"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    # Parent sphere
    sphere_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("spheres.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Section type (one of 6)
    section_type: Mapped[BureauSectionType] = mapped_column(
        SQLEnum(BureauSectionType),
        nullable=False,
    )
    
    # Display name
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    
    icon: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )
    
    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    # Display order within sphere
    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # Statistics
    item_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    unread_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    
    # Settings
    settings: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    
    # Relationship
    sphere: Mapped["Sphere"] = relationship(
        "Sphere",
        back_populates="bureau_sections",
    )
    
    def __repr__(self) -> str:
        return f"<BureauSection {self.section_type.value} ({self.sphere_id})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "sphere_id": self.sphere_id,
            "type": self.section_type.value,
            "name": self.name,
            "icon": self.icon,
            "is_active": self.is_active,
            "display_order": self.display_order,
            "item_count": self.item_count,
            "unread_count": self.unread_count,
            "has_unread": self.unread_count > 0,
            "settings": self.settings,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK CAPTURE MODEL
# ═══════════════════════════════════════════════════════════════════════════════

class QuickCaptureType(str, Enum):
    """Types of quick capture items."""
    NOTE = "note"
    TASK = "task"
    IDEA = "idea"
    LINK = "link"


class QuickCaptureStatus(str, Enum):
    """Status of quick capture items."""
    CAPTURED = "captured"
    PROCESSING = "processing"
    ROUTED = "routed"
    ARCHIVED = "archived"


class QuickCapture(Base):
    """
    Quick capture item in a sphere's inbox.
    
    Items can be automatically or manually routed to threads.
    """
    
    __tablename__ = "quick_captures"
    
    # Primary key
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    
    # Identity boundary
    identity_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
        index=True,
    )
    
    # Parent sphere
    sphere_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("spheres.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    # Content
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    capture_type: Mapped[QuickCaptureType] = mapped_column(
        SQLEnum(QuickCaptureType),
        default=QuickCaptureType.NOTE,
        nullable=False,
    )
    
    # Status
    status: Mapped[QuickCaptureStatus] = mapped_column(
        SQLEnum(QuickCaptureStatus),
        default=QuickCaptureStatus.CAPTURED,
        nullable=False,
    )
    
    # Tags
    tags: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    
    # Routing
    target_thread_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        nullable=True,
    )
    
    suggested_thread_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        nullable=True,
    )
    
    routed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    
    # Metadata
    source: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        default="web",
    )
    
    item_metadata: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        nullable=False,
    )
    
    def __repr__(self) -> str:
        return f"<QuickCapture {self.id[:8]}... ({self.capture_type.value})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "sphere_id": self.sphere_id,
            "content": self.content,
            "type": self.capture_type.value,
            "status": self.status.value,
            "tags": self.tags,
            "target_thread_id": self.target_thread_id,
            "suggested_thread_id": self.suggested_thread_id,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }
