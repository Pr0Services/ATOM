"""
CHE·NU™ — Synaptic Context (Context Capsule)
=============================================
Core data structure that synchronizes the 3 hubs:
- Hub Communication (Dire)
- Hub Navigation (Voir)  
- Hub Execution/Workspace (Faire)

One context = One unified UI state across all hubs.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Set
from enum import Enum
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import hashlib
import json


class ScopeType(str, Enum):
    """Access scope for context"""
    PRIVATE = "private"      # Single user
    COOPERATIVE = "coop"     # Shared team/project
    COMMON = "common"        # Public/community


class HubType(str, Enum):
    """The 3 core hubs"""
    COMMUNICATION = "communication"  # Dire - messaging, meetings, votes
    NAVIGATION = "navigation"        # Voir - location, visualization, mapping
    EXECUTION = "execution"          # Faire - workspace, tools, artifacts


class GuardType(str, Enum):
    """OPA policy guard types"""
    OPA_REQUIRED = "opa_required"
    TRUST_REQUIRED = "trust_required"
    RATE_LIMITED = "rate_limited"
    SCOPE_AWARE = "scope_aware"
    IDENTITY_VERIFIED = "identity_verified"


@dataclass
class LocationAnchor:
    """Navigation anchor for spatial context"""
    anchor_id: str
    sphere_id: str
    coordinates: Optional[Dict[str, float]] = None  # x, y, z for XR
    zone_type: str = "default"  # private, shared, common
    parent_anchor: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "anchor_id": self.anchor_id,
            "sphere_id": self.sphere_id,
            "coordinates": self.coordinates,
            "zone_type": self.zone_type,
            "parent_anchor": self.parent_anchor
        }


@dataclass
class ToolchainConfig:
    """Workspace toolchain configuration"""
    tool_ids: List[str] = field(default_factory=list)
    agent_ids: List[str] = field(default_factory=list)
    sandbox_mode: bool = True
    artifact_signing: bool = True
    max_compute_tokens: int = 10000
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool_ids": self.tool_ids,
            "agent_ids": self.agent_ids,
            "sandbox_mode": self.sandbox_mode,
            "artifact_signing": self.artifact_signing,
            "max_compute_tokens": self.max_compute_tokens
        }


@dataclass
class CommunicationChannel:
    """Communication hub channel config"""
    channel_id: str
    member_ids: List[str] = field(default_factory=list)
    channel_type: str = "task"  # task, meeting, vote, emergency
    encryption_level: str = "standard"  # standard, pqc, qkd
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "channel_id": self.channel_id,
            "member_ids": self.member_ids,
            "channel_type": self.channel_type,
            "encryption_level": self.encryption_level
        }


@dataclass
class PolicyGuard:
    """OPA policy guard configuration"""
    guard_type: GuardType
    policy_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    required: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "guard_type": self.guard_type.value,
            "policy_id": self.policy_id,
            "parameters": self.parameters,
            "required": self.required
        }


@dataclass
class SynapticContext:
    """
    The Context Capsule - single source of truth for 3-hub synchronization.
    
    When this context switches, ALL hubs update atomically.
    No hub should ever diverge from this context state.
    """
    
    # Core identifiers
    context_id: UUID = field(default_factory=uuid4)
    task_id: str = ""
    sphere_id: str = ""
    user_id: str = ""
    
    # Hub configurations
    location: Optional[LocationAnchor] = None
    tools: Optional[ToolchainConfig] = None
    channel: Optional[CommunicationChannel] = None
    
    # Access control
    scope: ScopeType = ScopeType.PRIVATE
    guards: List[PolicyGuard] = field(default_factory=list)
    
    # Anti-spam / rate limiting
    ttl_seconds: int = 300
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    
    # State tracking
    version: int = 1
    parent_context_id: Optional[UUID] = None
    is_active: bool = True
    
    # Metadata
    trigger_source: str = ""  # What triggered this context (Agora, XR, etc.)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = self.created_at + timedelta(seconds=self.ttl_seconds)
    
    @property
    def is_expired(self) -> bool:
        """Check if context has expired"""
        return datetime.utcnow() > self.expires_at
    
    @property
    def remaining_ttl(self) -> int:
        """Remaining TTL in seconds"""
        delta = self.expires_at - datetime.utcnow()
        return max(0, int(delta.total_seconds()))
    
    @property
    def signature(self) -> str:
        """Generate context signature for verification"""
        data = f"{self.context_id}:{self.task_id}:{self.sphere_id}:{self.version}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def extend_ttl(self, additional_seconds: int = 300) -> None:
        """Extend context TTL"""
        self.expires_at = datetime.utcnow() + timedelta(seconds=additional_seconds)
        self.ttl_seconds = additional_seconds
    
    def add_guard(self, guard: PolicyGuard) -> None:
        """Add a policy guard"""
        self.guards.append(guard)
    
    def has_guard(self, guard_type: GuardType) -> bool:
        """Check if context has specific guard type"""
        return any(g.guard_type == guard_type for g in self.guards)
    
    def get_required_guards(self) -> List[PolicyGuard]:
        """Get all required guards"""
        return [g for g in self.guards if g.required]
    
    def fork(self, new_task_id: Optional[str] = None) -> 'SynapticContext':
        """Create a child context (for sub-tasks)"""
        return SynapticContext(
            task_id=new_task_id or f"{self.task_id}_fork",
            sphere_id=self.sphere_id,
            user_id=self.user_id,
            location=self.location,
            tools=self.tools,
            channel=self.channel,
            scope=self.scope,
            guards=self.guards.copy(),
            ttl_seconds=self.ttl_seconds,
            parent_context_id=self.context_id,
            trigger_source=f"fork:{self.trigger_source}",
            metadata=self.metadata.copy()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize context to dictionary"""
        return {
            "context_id": str(self.context_id),
            "task_id": self.task_id,
            "sphere_id": self.sphere_id,
            "user_id": self.user_id,
            "location": self.location.to_dict() if self.location else None,
            "tools": self.tools.to_dict() if self.tools else None,
            "channel": self.channel.to_dict() if self.channel else None,
            "scope": self.scope.value,
            "guards": [g.to_dict() for g in self.guards],
            "ttl_seconds": self.ttl_seconds,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "version": self.version,
            "parent_context_id": str(self.parent_context_id) if self.parent_context_id else None,
            "is_active": self.is_active,
            "trigger_source": self.trigger_source,
            "signature": self.signature,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Serialize to JSON string"""
        return json.dumps(self.to_dict(), default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SynapticContext':
        """Deserialize from dictionary"""
        ctx = cls(
            context_id=UUID(data["context_id"]) if data.get("context_id") else uuid4(),
            task_id=data.get("task_id", ""),
            sphere_id=data.get("sphere_id", ""),
            user_id=data.get("user_id", ""),
            scope=ScopeType(data.get("scope", "private")),
            ttl_seconds=data.get("ttl_seconds", 300),
            version=data.get("version", 1),
            trigger_source=data.get("trigger_source", ""),
            metadata=data.get("metadata", {})
        )
        
        if data.get("location"):
            ctx.location = LocationAnchor(**data["location"])
        if data.get("tools"):
            ctx.tools = ToolchainConfig(**data["tools"])
        if data.get("channel"):
            ctx.channel = CommunicationChannel(**data["channel"])
        if data.get("guards"):
            ctx.guards = [
                PolicyGuard(
                    guard_type=GuardType(g["guard_type"]),
                    policy_id=g["policy_id"],
                    parameters=g.get("parameters", {}),
                    required=g.get("required", True)
                )
                for g in data["guards"]
            ]
        if data.get("parent_context_id"):
            ctx.parent_context_id = UUID(data["parent_context_id"])
        if data.get("created_at"):
            ctx.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("expires_at"):
            ctx.expires_at = datetime.fromisoformat(data["expires_at"])
        
        return ctx


class ContextCapsuleBuilder:
    """Builder pattern for creating SynapticContext"""
    
    def __init__(self):
        self._context = SynapticContext()
    
    def with_task(self, task_id: str, sphere_id: str) -> 'ContextCapsuleBuilder':
        self._context.task_id = task_id
        self._context.sphere_id = sphere_id
        return self
    
    def with_user(self, user_id: str) -> 'ContextCapsuleBuilder':
        self._context.user_id = user_id
        return self
    
    def with_location(self, anchor_id: str, coordinates: Optional[Dict] = None) -> 'ContextCapsuleBuilder':
        self._context.location = LocationAnchor(
            anchor_id=anchor_id,
            sphere_id=self._context.sphere_id,
            coordinates=coordinates
        )
        return self
    
    def with_tools(self, tool_ids: List[str], agent_ids: Optional[List[str]] = None) -> 'ContextCapsuleBuilder':
        self._context.tools = ToolchainConfig(
            tool_ids=tool_ids,
            agent_ids=agent_ids or []
        )
        return self
    
    def with_channel(self, channel_id: str, members: List[str]) -> 'ContextCapsuleBuilder':
        self._context.channel = CommunicationChannel(
            channel_id=channel_id,
            member_ids=members
        )
        return self
    
    def with_scope(self, scope: ScopeType) -> 'ContextCapsuleBuilder':
        self._context.scope = scope
        return self
    
    def with_guard(self, guard_type: GuardType, policy_id: str, **params) -> 'ContextCapsuleBuilder':
        self._context.add_guard(PolicyGuard(
            guard_type=guard_type,
            policy_id=policy_id,
            parameters=params
        ))
        return self
    
    def with_ttl(self, seconds: int) -> 'ContextCapsuleBuilder':
        self._context.ttl_seconds = seconds
        self._context.expires_at = self._context.created_at + timedelta(seconds=seconds)
        return self
    
    def triggered_by(self, source: str) -> 'ContextCapsuleBuilder':
        self._context.trigger_source = source
        return self
    
    def build(self) -> SynapticContext:
        return self._context


# Convenience factory functions
def create_task_context(
    task_id: str,
    sphere_id: str,
    user_id: str,
    tools: List[str] = None,
    members: List[str] = None
) -> SynapticContext:
    """Quick factory for task context"""
    builder = ContextCapsuleBuilder()
    builder.with_task(task_id, sphere_id).with_user(user_id)
    
    if tools:
        builder.with_tools(tools)
    if members:
        builder.with_channel(f"ch_{task_id}", members)
    
    return builder.build()


def create_emergency_context(
    task_id: str,
    sphere_id: str,
    user_id: str,
    members: List[str]
) -> SynapticContext:
    """Emergency context with elevated priority"""
    return (
        ContextCapsuleBuilder()
        .with_task(task_id, sphere_id)
        .with_user(user_id)
        .with_channel(f"emergency_{task_id}", members)
        .with_scope(ScopeType.COOPERATIVE)
        .with_guard(GuardType.OPA_REQUIRED, "emergency_policy")
        .with_ttl(600)  # 10 minutes
        .triggered_by("emergency_system")
        .build()
    )
