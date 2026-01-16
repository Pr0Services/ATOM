"""
CHE·NU™ V75 — SYNAPTIC CONTEXT MODULE
======================================

Context management for intelligent sphere navigation.

Version: 75.0
Status: PRODUCTION
R&D Compliance: ✅ Rule #1-7
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
import logging

logger = logging.getLogger("chenu.v75.synaptic_context")


class ContextLayer(str, Enum):
    """Context layers for memory management"""
    HOT = "hot"       # Immediate context (session)
    WARM = "warm"     # Recent context (30 days)
    COLD = "cold"     # Archived context


class SphereContext(str, Enum):
    """Active sphere context"""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE = "creative"
    COMMUNITY = "community"
    SOCIAL = "social"
    ENTERTAINMENT = "entertainment"
    TEAM = "team"
    SCHOLAR = "scholar"


@dataclass
class ContextSnapshot:
    """
    Snapshot of current user context.
    
    R&D Compliance:
    - Rule #1: Human Sovereignty - context read-only, human decides
    - Rule #6: Traceability - all fields tracked
    """
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    
    # Active context
    active_sphere: SphereContext = SphereContext.PERSONAL
    active_thread_id: Optional[UUID] = None
    active_agents: List[str] = field(default_factory=list)
    
    # Context layers
    hot_memory: Dict[str, Any] = field(default_factory=dict)
    warm_memory_summary: Optional[str] = None
    cold_memory_available: bool = False
    
    # Navigation history
    sphere_history: List[SphereContext] = field(default_factory=list)
    thread_history: List[UUID] = field(default_factory=list)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Initialize context with history"""
        if not self.sphere_history:
            self.sphere_history = [self.active_sphere]


class SynapticContextEngine:
    """
    Synaptic Context Engine for CHE·NU V75.
    
    Manages user context across spheres and sessions.
    
    R&D Compliance:
    - Rule #1: Human Sovereignty - illuminates, never decides
    - Rule #2: Autonomy Isolation - sandbox context only
    - Rule #3: Sphere Integrity - cross-sphere requires validation
    """
    
    def __init__(self):
        self._contexts: Dict[UUID, ContextSnapshot] = {}
        self._active_users: set = set()
        logger.info("SynapticContextEngine initialized")
    
    async def get_context(self, user_id: UUID) -> ContextSnapshot:
        """
        Get or create user context.
        
        Returns:
            ContextSnapshot: Current user context
        """
        if user_id not in self._contexts:
            self._contexts[user_id] = ContextSnapshot(user_id=user_id)
            self._active_users.add(user_id)
            logger.info(f"Created new context for user {user_id}")
        
        return self._contexts[user_id]
    
    async def switch_sphere(
        self,
        user_id: UUID,
        target_sphere: SphereContext,
        initiated_by: UUID
    ) -> Dict[str, Any]:
        """
        Switch user to different sphere.
        
        GOVERNANCE: Cross-sphere switch requires explicit request.
        
        Args:
            user_id: User ID
            target_sphere: Target sphere to switch to
            initiated_by: ID of initiator (must match user_id)
            
        Returns:
            Dict with switch result
        """
        # Rule #1: Verify human initiated
        if initiated_by != user_id:
            raise PermissionError("Sphere switch must be initiated by user")
        
        context = await self.get_context(user_id)
        previous_sphere = context.active_sphere
        
        # Record history
        context.sphere_history.append(target_sphere)
        if len(context.sphere_history) > 50:
            context.sphere_history = context.sphere_history[-50:]
        
        # Switch
        context.active_sphere = target_sphere
        context.updated_at = datetime.utcnow()
        
        logger.info(f"User {user_id} switched from {previous_sphere} to {target_sphere}")
        
        return {
            "status": "switched",
            "from_sphere": previous_sphere.value,
            "to_sphere": target_sphere.value,
            "context_id": str(context.id),
            "timestamp": context.updated_at.isoformat()
        }
    
    async def update_hot_memory(
        self,
        user_id: UUID,
        key: str,
        value: Any,
        updated_by: UUID
    ) -> Dict[str, Any]:
        """
        Update hot memory (immediate context).
        
        Args:
            user_id: User ID
            key: Memory key
            value: Memory value
            updated_by: ID of updater
            
        Returns:
            Update confirmation
        """
        context = await self.get_context(user_id)
        
        context.hot_memory[key] = {
            "value": value,
            "updated_by": str(updated_by),
            "updated_at": datetime.utcnow().isoformat()
        }
        context.updated_at = datetime.utcnow()
        
        return {
            "status": "updated",
            "key": key,
            "layer": "hot",
            "context_id": str(context.id)
        }
    
    async def get_context_summary(self, user_id: UUID) -> Dict[str, Any]:
        """
        Get summary of user context.
        
        Returns:
            Context summary for display
        """
        context = await self.get_context(user_id)
        
        return {
            "context_id": str(context.id),
            "active_sphere": context.active_sphere.value,
            "active_thread": str(context.active_thread_id) if context.active_thread_id else None,
            "active_agents_count": len(context.active_agents),
            "hot_memory_keys": list(context.hot_memory.keys()),
            "sphere_history_length": len(context.sphere_history),
            "warm_memory_available": context.warm_memory_summary is not None,
            "cold_memory_available": context.cold_memory_available,
            "created_at": context.created_at.isoformat(),
            "updated_at": context.updated_at.isoformat()
        }
    
    async def clear_hot_memory(self, user_id: UUID, cleared_by: UUID) -> Dict[str, Any]:
        """
        Clear hot memory.
        
        GOVERNANCE: User must explicitly request.
        """
        if cleared_by != user_id:
            raise PermissionError("Memory clear must be initiated by user")
        
        context = await self.get_context(user_id)
        previous_count = len(context.hot_memory)
        context.hot_memory = {}
        context.updated_at = datetime.utcnow()
        
        logger.info(f"Cleared {previous_count} hot memory items for user {user_id}")
        
        return {
            "status": "cleared",
            "items_cleared": previous_count,
            "context_id": str(context.id)
        }


# Singleton instance
_engine: Optional[SynapticContextEngine] = None


def get_synaptic_context_engine() -> SynapticContextEngine:
    """Get or create SynapticContextEngine instance"""
    global _engine
    if _engine is None:
        _engine = SynapticContextEngine()
    return _engine


# Export
__all__ = [
    "SynapticContextEngine",
    "ContextSnapshot",
    "ContextLayer",
    "SphereContext",
    "get_synaptic_context_engine"
]
