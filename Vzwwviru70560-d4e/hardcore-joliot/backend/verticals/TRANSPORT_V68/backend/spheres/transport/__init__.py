"""
CHE·NU V68 Transport & Logistics Module
AT·OM Flow - Intelligent Transport Management

Le transport comme un reseau neuronal:
- Chaque vehicule est un neurone
- Chaque trajet est une synapse
- L'intelligence collective optimise le flux

GOVERNANCE COMPLIANCE:
- Rule #1: Dispatch haute valeur + sous-traitance require APPROVAL
- Rule #5: All listings ALPHABETICAL or CHRONOLOGICAL
- Rule #6: Full audit trail
"""

from backend.verticals.TRANSPORT_V68.backend.spheres.transport.agents.transport_agent import (
    TransportAgent,
    get_transport_agent,
    # Enums
    VehicleType,
    VehicleStatus,
    TripType,
    TripStatus,
    LoadType,
    DispatchMode,
    SoustraitanceType,
    SoustraitanceStatus,
    ZoneType,
    OptimizationGoal,
    FlowStatus,
    # Data models
    GeoPoint,
    Vehicle,
    Driver,
    Trip,
    CheNuZone,
    SoustraitanceContract,
    DispatchDecision,
    PoolingOpportunity,
    FlowMetric,
)

from backend.verticals.TRANSPORT_V68.backend.spheres.transport.agents.transport_agents_registry import (
    get_transport_agents,
    validate_transport_agents,
    TRANSPORT_AGENT_COUNT,
    TRANSPORT_CATEGORIES,
)

__all__ = [
    # Main agent
    "TransportAgent",
    "get_transport_agent",
    # Enums
    "VehicleType",
    "VehicleStatus",
    "TripType",
    "TripStatus",
    "LoadType",
    "DispatchMode",
    "SoustraitanceType",
    "SoustraitanceStatus",
    "ZoneType",
    "OptimizationGoal",
    "FlowStatus",
    # Data models
    "GeoPoint",
    "Vehicle",
    "Driver",
    "Trip",
    "CheNuZone",
    "SoustraitanceContract",
    "DispatchDecision",
    "PoolingOpportunity",
    "FlowMetric",
    # Registry
    "get_transport_agents",
    "validate_transport_agents",
    "TRANSPORT_AGENT_COUNT",
    "TRANSPORT_CATEGORIES",
]

__version__ = "68.0.0"
__module__ = "AT·OM Flow"
