"""
CHE·NU™ — Synaptic Switcher (3-Hub Router)
==========================================
Routes SynapticContext to the 3 hubs atomically:
- Hub Communication (Dire) - messaging, meetings, votes
- Hub Navigation (Voir) - location, visualization, mapping
- Hub Execution (Faire) - workspace, tools, artifacts

Critical Rule: Hubs NEVER diverge. One context = One state.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable, Awaitable
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
import asyncio
import logging
from abc import ABC, abstractmethod

from .synaptic_context import (
    SynapticContext, 
    HubType, 
    ScopeType,
    GuardType,
    PolicyGuard
)

logger = logging.getLogger(__name__)


class SwitchResult(str, Enum):
    """Result of a synaptic switch operation"""
    SUCCESS = "success"
    PARTIAL = "partial"  # Some hubs updated
    BLOCKED = "blocked"  # Guards prevented switch
    EXPIRED = "expired"  # Context TTL expired
    ERROR = "error"


@dataclass
class HubState:
    """Current state of a hub"""
    hub_type: HubType
    context_id: Optional[UUID] = None
    is_active: bool = False
    last_updated: datetime = field(default_factory=datetime.utcnow)
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "hub_type": self.hub_type.value,
            "context_id": str(self.context_id) if self.context_id else None,
            "is_active": self.is_active,
            "last_updated": self.last_updated.isoformat(),
            "error": self.error
        }


@dataclass
class SwitchEvent:
    """Event emitted during switch"""
    event_id: UUID = field(default_factory=uuid4)
    context_id: UUID = None
    hub_type: HubType = None
    action: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)


class HubAdapter(ABC):
    """Abstract adapter for hub operations"""
    
    @property
    @abstractmethod
    def hub_type(self) -> HubType:
        pass
    
    @abstractmethod
    async def activate(self, context: SynapticContext) -> bool:
        """Activate hub with context"""
        pass
    
    @abstractmethod
    async def deactivate(self) -> bool:
        """Deactivate hub"""
        pass
    
    @abstractmethod
    async def get_state(self) -> HubState:
        """Get current hub state"""
        pass


class CommunicationHubAdapter(HubAdapter):
    """Adapter for Communication Hub (Dire)"""
    
    def __init__(self):
        self._current_context: Optional[SynapticContext] = None
        self._active_channel: Optional[str] = None
    
    @property
    def hub_type(self) -> HubType:
        return HubType.COMMUNICATION
    
    async def activate(self, context: SynapticContext) -> bool:
        """Open communication thread/channel"""
        try:
            if context.channel:
                # Open thread with members
                self._active_channel = context.channel.channel_id
                self._current_context = context
                
                logger.info(
                    f"COMM Hub: Opened channel {context.channel.channel_id} "
                    f"with {len(context.channel.member_ids)} members "
                    f"for task {context.task_id}"
                )
                
                # TODO: Actual integration with messaging system
                # await self._messaging_service.open_thread(
                #     channel_id=context.channel.channel_id,
                #     members=context.channel.member_ids,
                #     encryption=context.channel.encryption_level
                # )
                
            return True
        except Exception as e:
            logger.error(f"COMM Hub activation failed: {e}")
            return False
    
    async def deactivate(self) -> bool:
        """Close communication channel"""
        if self._active_channel:
            logger.info(f"COMM Hub: Closing channel {self._active_channel}")
            self._active_channel = None
            self._current_context = None
        return True
    
    async def get_state(self) -> HubState:
        return HubState(
            hub_type=self.hub_type,
            context_id=self._current_context.context_id if self._current_context else None,
            is_active=self._active_channel is not None
        )


class NavigationHubAdapter(HubAdapter):
    """Adapter for Navigation Hub (Voir)"""
    
    def __init__(self):
        self._current_context: Optional[SynapticContext] = None
        self._focused_location: Optional[str] = None
    
    @property
    def hub_type(self) -> HubType:
        return HubType.NAVIGATION
    
    async def activate(self, context: SynapticContext) -> bool:
        """Focus navigation on location"""
        try:
            if context.location:
                self._focused_location = context.location.anchor_id
                self._current_context = context
                
                logger.info(
                    f"NAV Hub: Focused on location {context.location.anchor_id} "
                    f"in sphere {context.sphere_id}"
                )
                
                # TODO: Actual integration with navigation/XR system
                # await self._navigation_service.focus(
                #     anchor_id=context.location.anchor_id,
                #     coordinates=context.location.coordinates,
                #     zone_type=context.location.zone_type
                # )
                
            return True
        except Exception as e:
            logger.error(f"NAV Hub activation failed: {e}")
            return False
    
    async def deactivate(self) -> bool:
        """Clear navigation focus"""
        if self._focused_location:
            logger.info(f"NAV Hub: Clearing focus from {self._focused_location}")
            self._focused_location = None
            self._current_context = None
        return True
    
    async def get_state(self) -> HubState:
        return HubState(
            hub_type=self.hub_type,
            context_id=self._current_context.context_id if self._current_context else None,
            is_active=self._focused_location is not None
        )


class ExecutionHubAdapter(HubAdapter):
    """Adapter for Execution/Workspace Hub (Faire)"""
    
    def __init__(self):
        self._current_context: Optional[SynapticContext] = None
        self._active_workspace: Optional[str] = None
        self._loaded_tools: List[str] = []
    
    @property
    def hub_type(self) -> HubType:
        return HubType.EXECUTION
    
    async def activate(self, context: SynapticContext) -> bool:
        """Open workspace with tools"""
        try:
            if context.tools:
                self._active_workspace = f"ws_{context.task_id}"
                self._loaded_tools = context.tools.tool_ids.copy()
                self._current_context = context
                
                logger.info(
                    f"EXEC Hub: Opened workspace {self._active_workspace} "
                    f"with {len(self._loaded_tools)} tools "
                    f"and {len(context.tools.agent_ids)} agents"
                )
                
                # TODO: Actual integration with workspace system
                # await self._workspace_service.open(
                #     workspace_id=self._active_workspace,
                #     tools=context.tools.tool_ids,
                #     agents=context.tools.agent_ids,
                #     sandbox=context.tools.sandbox_mode
                # )
                
            return True
        except Exception as e:
            logger.error(f"EXEC Hub activation failed: {e}")
            return False
    
    async def deactivate(self) -> bool:
        """Close workspace"""
        if self._active_workspace:
            logger.info(f"EXEC Hub: Closing workspace {self._active_workspace}")
            self._active_workspace = None
            self._loaded_tools = []
            self._current_context = None
        return True
    
    async def get_state(self) -> HubState:
        return HubState(
            hub_type=self.hub_type,
            context_id=self._current_context.context_id if self._current_context else None,
            is_active=self._active_workspace is not None
        )


class PolicyEnforcer:
    """Enforces OPA guards before switch"""
    
    async def check_guards(
        self, 
        context: SynapticContext,
        user_id: str
    ) -> tuple[bool, Optional[str]]:
        """
        Check all required guards.
        Returns (allowed, reason_if_blocked)
        """
        for guard in context.get_required_guards():
            allowed, reason = await self._check_single_guard(guard, context, user_id)
            if not allowed:
                return False, reason
        
        return True, None
    
    async def _check_single_guard(
        self,
        guard: PolicyGuard,
        context: SynapticContext,
        user_id: str
    ) -> tuple[bool, Optional[str]]:
        """Check a single guard"""
        
        if guard.guard_type == GuardType.OPA_REQUIRED:
            # TODO: Actual OPA integration
            # result = await opa_client.evaluate(guard.policy_id, context.to_dict())
            logger.info(f"OPA Guard: Checking policy {guard.policy_id}")
            return True, None
            
        elif guard.guard_type == GuardType.IDENTITY_VERIFIED:
            # Verify user identity
            if context.user_id != user_id:
                return False, "Identity mismatch"
            return True, None
            
        elif guard.guard_type == GuardType.RATE_LIMITED:
            # TODO: Rate limit check
            logger.info(f"Rate limit guard: {guard.parameters}")
            return True, None
            
        elif guard.guard_type == GuardType.SCOPE_AWARE:
            # Check scope permissions
            logger.info(f"Scope guard: {context.scope.value}")
            return True, None
            
        elif guard.guard_type == GuardType.TRUST_REQUIRED:
            # TODO: Trust score check
            logger.info(f"Trust guard: {guard.parameters}")
            return True, None
        
        return True, None


@dataclass
class SwitchReport:
    """Report of a synaptic switch operation"""
    switch_id: UUID = field(default_factory=uuid4)
    context_id: UUID = None
    result: SwitchResult = SwitchResult.SUCCESS
    hub_states: Dict[str, HubState] = field(default_factory=dict)
    events: List[SwitchEvent] = field(default_factory=list)
    blocked_reason: Optional[str] = None
    duration_ms: float = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "switch_id": str(self.switch_id),
            "context_id": str(self.context_id) if self.context_id else None,
            "result": self.result.value,
            "hub_states": {k: v.to_dict() for k, v in self.hub_states.items()},
            "events": len(self.events),
            "blocked_reason": self.blocked_reason,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp.isoformat()
        }


class SynapticSwitcher:
    """
    Main switcher that routes context to all 3 hubs atomically.
    
    Core principle: One switch = All hubs update together.
    If any hub fails, rollback all.
    """
    
    def __init__(self):
        # Hub adapters
        self._comm_hub = CommunicationHubAdapter()
        self._nav_hub = NavigationHubAdapter()
        self._exec_hub = ExecutionHubAdapter()
        
        # Policy enforcer
        self._policy = PolicyEnforcer()
        
        # Current context
        self._current_context: Optional[SynapticContext] = None
        
        # Event listeners
        self._listeners: List[Callable[[SwitchEvent], Awaitable[None]]] = []
        
        # Switch history
        self._history: List[SwitchReport] = []
    
    @property
    def current_context(self) -> Optional[SynapticContext]:
        return self._current_context
    
    @property
    def hub_adapters(self) -> Dict[HubType, HubAdapter]:
        return {
            HubType.COMMUNICATION: self._comm_hub,
            HubType.NAVIGATION: self._nav_hub,
            HubType.EXECUTION: self._exec_hub
        }
    
    def add_listener(self, listener: Callable[[SwitchEvent], Awaitable[None]]) -> None:
        """Add event listener for switch events"""
        self._listeners.append(listener)
    
    async def _emit_event(self, event: SwitchEvent) -> None:
        """Emit event to all listeners"""
        for listener in self._listeners:
            try:
                await listener(event)
            except Exception as e:
                logger.error(f"Event listener error: {e}")
    
    async def switch(
        self, 
        context: SynapticContext,
        user_id: str
    ) -> SwitchReport:
        """
        Perform atomic switch to new context.
        All hubs update together or none do.
        """
        import time
        start_time = time.time()
        
        report = SwitchReport(context_id=context.context_id)
        
        # 1. Check if context is expired
        if context.is_expired:
            report.result = SwitchResult.EXPIRED
            report.blocked_reason = "Context TTL expired"
            return report
        
        # 2. Check guards (OPA policies)
        allowed, reason = await self._policy.check_guards(context, user_id)
        if not allowed:
            report.result = SwitchResult.BLOCKED
            report.blocked_reason = reason
            
            await self._emit_event(SwitchEvent(
                context_id=context.context_id,
                action="switch_blocked",
                data={"reason": reason}
            ))
            
            return report
        
        # 3. Deactivate current context (if any)
        if self._current_context:
            await self._deactivate_all()
        
        # 4. Activate all hubs atomically
        hub_results = {}
        activated_hubs = []
        
        try:
            # Communication Hub
            if await self._comm_hub.activate(context):
                activated_hubs.append(HubType.COMMUNICATION)
                hub_results[HubType.COMMUNICATION.value] = await self._comm_hub.get_state()
                
                await self._emit_event(SwitchEvent(
                    context_id=context.context_id,
                    hub_type=HubType.COMMUNICATION,
                    action="hub_activated"
                ))
            
            # Navigation Hub
            if await self._nav_hub.activate(context):
                activated_hubs.append(HubType.NAVIGATION)
                hub_results[HubType.NAVIGATION.value] = await self._nav_hub.get_state()
                
                await self._emit_event(SwitchEvent(
                    context_id=context.context_id,
                    hub_type=HubType.NAVIGATION,
                    action="hub_activated"
                ))
            
            # Execution Hub
            if await self._exec_hub.activate(context):
                activated_hubs.append(HubType.EXECUTION)
                hub_results[HubType.EXECUTION.value] = await self._exec_hub.get_state()
                
                await self._emit_event(SwitchEvent(
                    context_id=context.context_id,
                    hub_type=HubType.EXECUTION,
                    action="hub_activated"
                ))
            
            # Check if all hubs activated
            if len(activated_hubs) == 3:
                report.result = SwitchResult.SUCCESS
                self._current_context = context
                
                await self._emit_event(SwitchEvent(
                    context_id=context.context_id,
                    action="switch_complete",
                    data={"hubs": [h.value for h in activated_hubs]}
                ))
                
            elif len(activated_hubs) > 0:
                report.result = SwitchResult.PARTIAL
                report.blocked_reason = f"Only {len(activated_hubs)}/3 hubs activated"
                
                # Rollback partial activation
                await self._deactivate_all()
                
            else:
                report.result = SwitchResult.ERROR
                report.blocked_reason = "No hubs could be activated"
                
        except Exception as e:
            logger.error(f"Switch error: {e}")
            report.result = SwitchResult.ERROR
            report.blocked_reason = str(e)
            
            # Rollback on error
            await self._deactivate_all()
        
        # Finalize report
        report.hub_states = hub_results
        report.duration_ms = (time.time() - start_time) * 1000
        
        # Store in history
        self._history.append(report)
        
        return report
    
    async def _deactivate_all(self) -> None:
        """Deactivate all hubs"""
        await self._comm_hub.deactivate()
        await self._nav_hub.deactivate()
        await self._exec_hub.deactivate()
        self._current_context = None
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current switcher status"""
        return {
            "current_context": self._current_context.to_dict() if self._current_context else None,
            "hubs": {
                HubType.COMMUNICATION.value: (await self._comm_hub.get_state()).to_dict(),
                HubType.NAVIGATION.value: (await self._nav_hub.get_state()).to_dict(),
                HubType.EXECUTION.value: (await self._exec_hub.get_state()).to_dict()
            },
            "history_count": len(self._history),
            "last_switch": self._history[-1].to_dict() if self._history else None
        }
    
    async def render_dashboard(self, context: SynapticContext) -> Dict[str, Any]:
        """
        Prepare dashboard render data for MOD_25 (Synaptic Dashboard).
        UI density is controlled by user preferences.
        """
        return {
            "context": context.to_dict(),
            "hubs": {
                "communication": {
                    "active": context.channel is not None,
                    "channel_id": context.channel.channel_id if context.channel else None,
                    "members_count": len(context.channel.member_ids) if context.channel else 0
                },
                "navigation": {
                    "active": context.location is not None,
                    "location": context.location.anchor_id if context.location else None,
                    "sphere": context.sphere_id
                },
                "execution": {
                    "active": context.tools is not None,
                    "tools_count": len(context.tools.tool_ids) if context.tools else 0,
                    "agents_count": len(context.tools.agent_ids) if context.tools else 0
                }
            },
            "guards": [g.guard_type.value for g in context.guards],
            "ttl_remaining": context.remaining_ttl,
            "signature": context.signature
        }


# Singleton instance
_switcher: Optional[SynapticSwitcher] = None

def get_synaptic_switcher() -> SynapticSwitcher:
    """Get singleton switcher instance"""
    global _switcher
    if _switcher is None:
        _switcher = SynapticSwitcher()
    return _switcher


async def synaptic_switch(context: SynapticContext, user_id: str) -> SwitchReport:
    """Convenience function for switching context"""
    switcher = get_synaptic_switcher()
    return await switcher.switch(context, user_id)
