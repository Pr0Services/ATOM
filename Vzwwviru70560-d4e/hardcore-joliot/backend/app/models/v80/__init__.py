"""
CHE·NU™ V80 — Database Models Package
"""

from .base import (
    # Base classes
    Base,
    TimestampMixin,
    TraceabilityMixin,
    
    # Enums
    SphereType,
    ThreadStatus,
    ThreadType,
    Visibility,
    CheckpointStatus,
    CheckpointType,
    ThreadEventType,
    AuditLogAction,
    
    # Core models
    Identity,
    Thread,
    ThreadEvent,
    Checkpoint,
    AuditLog,
)

from .spheres import (
    # Personal
    Note, Task, Habit,
    # Business
    Contact, Invoice, Project,
    # Creative
    CreativeAsset, CreativeProject,
    # Entertainment
    Playlist, StreamHistory,
    # Community
    CommunityGroup, CommunityEvent,
    # Social
    SocialPost, SocialSchedule,
    # Scholar
    Reference, Manuscript,
    # Government
    ComplianceItem, ClinicalTrial,
    # My Team
    TeamMember, HiredAgent, TeamTask,
)

__all__ = [
    # Base
    "Base", "TimestampMixin", "TraceabilityMixin",
    
    # Enums
    "SphereType", "ThreadStatus", "ThreadType", "Visibility",
    "CheckpointStatus", "CheckpointType", "ThreadEventType", "AuditLogAction",
    
    # Core
    "Identity", "Thread", "ThreadEvent", "Checkpoint", "AuditLog",
    
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
