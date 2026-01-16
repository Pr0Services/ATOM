"""
CHE·NU™ — Synaptic Module
========================
Core synaptic infrastructure for 3-hub synchronization.

Components:
- SynapticContext: The context capsule (single source of truth)
- SynapticSwitcher: Routes context to 3 hubs atomically
- SynapticGraph: Inter-module connection graph
- YellowPages: Service registry for routing
"""

from .synaptic_context import (
    SynapticContext,
    ScopeType,
    HubType,
    GuardType,
    LocationAnchor,
    ToolchainConfig,
    CommunicationChannel,
    PolicyGuard,
    ContextCapsuleBuilder,
    create_task_context,
    create_emergency_context
)

from .synaptic_switcher import (
    SynapticSwitcher,
    SwitchResult,
    SwitchReport,
    HubState,
    SwitchEvent,
    HubAdapter,
    CommunicationHubAdapter,
    NavigationHubAdapter,
    ExecutionHubAdapter,
    PolicyEnforcer,
    get_synaptic_switcher,
    synaptic_switch
)

from .synaptic_graph import (
    SynapticGraph,
    SynapticEdge,
    EdgeTrigger,
    EdgeAction,
    EdgeFireEvent,
    StabilityGuard,
    ModuleID,
    Priority,
    get_synaptic_graph
)

from .yellow_pages import (
    YellowPages,
    YellowPageEntry,
    NeedTag,
    GuardRequirement,
    FallbackService,
    RoutingDecision,
    ServiceHandler,
    get_yellow_pages
)

__all__ = [
    # Context
    "SynapticContext",
    "ScopeType",
    "HubType",
    "GuardType",
    "LocationAnchor",
    "ToolchainConfig",
    "CommunicationChannel",
    "PolicyGuard",
    "ContextCapsuleBuilder",
    "create_task_context",
    "create_emergency_context",
    
    # Switcher
    "SynapticSwitcher",
    "SwitchResult",
    "SwitchReport",
    "HubState",
    "SwitchEvent",
    "HubAdapter",
    "get_synaptic_switcher",
    "synaptic_switch",
    
    # Graph
    "SynapticGraph",
    "SynapticEdge",
    "EdgeTrigger",
    "EdgeAction",
    "EdgeFireEvent",
    "ModuleID",
    "Priority",
    "get_synaptic_graph",
    
    # Yellow Pages
    "YellowPages",
    "YellowPageEntry",
    "NeedTag",
    "GuardRequirement",
    "FallbackService",
    "get_yellow_pages"
]
