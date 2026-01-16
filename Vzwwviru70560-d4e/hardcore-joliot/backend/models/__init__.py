"""
CHE·NU™ V75 Backend - Models Package

SQLAlchemy models - GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from models.user import User, Identity
from models.thread import Thread, ThreadEvent
from models.agent import Agent, HiredAgent, AgentTask
from models.governance import Checkpoint, Policy, AuditLog
from models.sphere import Sphere, Bureau, CANONICAL_SPHERE_IDS, CANONICAL_BUREAU_IDS, SPHERE_SEED_DATA, BUREAU_SEED_DATA
from models.decision import Decision, DecisionOption
from models.xr import XREnvironment, XRArtifact, XRVerificationResult
from models.dataspace import DataSpace, DataSpaceFile, DataSpaceLink
from models.streaming import (
    MediaContent, StreamSource, Channel, Genre, Tag,
    Playlist, WatchProgress, ChannelSubscription, ContentRating,
    LiveStream, ContentType, ContentStatus, GENRE_SEED_DATA,
)

# V75 Extended Models
from models.identity import Identity as IdentityV75, IdentityPermission, UserSphereAccess
from models.meeting import Meeting, MeetingParticipant, MeetingNote, MeetingTask
from models.workspace import Workspace, WorkspacePanel, WorkspaceState, WorkspaceTransformation
from models.oneclick import OneClickWorkflow, OneClickExecution, OneClickTemplate
from models.memory import MemoryItem, GovernanceAuditLog, ElevationRequest, CrossIdentityBlock
from models.immobilier import Property, PropertyUnit, Tenant, RentPayment, MaintenanceRequest

__all__ = [
    # User
    "User",
    "Identity",
    # Thread (APPEND-ONLY)
    "Thread",
    "ThreadEvent",
    # Agent
    "Agent",
    "HiredAgent",
    "AgentTask",
    # Governance
    "Checkpoint",
    "Policy",
    "AuditLog",
    # Sphere (FROZEN)
    "Sphere",
    "Bureau",
    "CANONICAL_SPHERE_IDS",
    "CANONICAL_BUREAU_IDS",
    "SPHERE_SEED_DATA",
    "BUREAU_SEED_DATA",
    # Decision
    "Decision",
    "DecisionOption",
    # XR (READ-ONLY)
    "XREnvironment",
    "XRArtifact",
    "XRVerificationResult",
    # DataSpace
    "DataSpace",
    "DataSpaceFile",
    "DataSpaceLink",
    # Streaming
    "MediaContent",
    "StreamSource",
    "Channel",
    "Genre",
    "Tag",
    "Playlist",
    "WatchProgress",
    "ChannelSubscription",
    "ContentRating",
    "LiveStream",
    "ContentType",
    "ContentStatus",
    "GENRE_SEED_DATA",
    # V75 - Identity
    "IdentityV75",
    "IdentityPermission",
    "UserSphereAccess",
    # V75 - Meeting
    "Meeting",
    "MeetingParticipant",
    "MeetingNote",
    "MeetingTask",
    # V75 - Workspace
    "Workspace",
    "WorkspacePanel",
    "WorkspaceState",
    "WorkspaceTransformation",
    # V75 - OneClick
    "OneClickWorkflow",
    "OneClickExecution",
    "OneClickTemplate",
    # V75 - Memory & Governance
    "MemoryItem",
    "GovernanceAuditLog",
    "ElevationRequest",
    "CrossIdentityBlock",
    # V75 - Immobilier
    "Property",
    "PropertyUnit",
    "Tenant",
    "RentPayment",
    "MaintenanceRequest",
]
