"""
CHE·NU V68 Circular Economy Module
Economie Circulaire - Zero Dechet

GOVERNANCE COMPLIANCE:
- Rule #1: Hazardous flows require APPROVAL
- Rule #5: Materials ALPHABETICAL
- Rule #6: Full audit trail
"""

from .agents.circular_economy_agent import (
    CircularEconomyAgent,
    get_circular_economy_agent,
    MaterialCategory,
    MaterialState,
    FlowType,
    ProcessType,
    ActorType,
    SymbiosisType,
    CircularityLevel,
    Material,
    MaterialFlow,
    Actor,
    SymbiosisConnection,
    RecyclingLoop,
    WasteAudit,
    CircularMetrics,
)

__all__ = [
    "CircularEconomyAgent",
    "get_circular_economy_agent",
    "MaterialCategory",
    "MaterialState",
    "FlowType",
    "ProcessType",
    "ActorType",
    "SymbiosisType",
    "CircularityLevel",
    "Material",
    "MaterialFlow",
    "Actor",
    "SymbiosisConnection",
    "RecyclingLoop",
    "WasteAudit",
    "CircularMetrics",
]

__version__ = "68.0.0"
__module__ = "Economie Circulaire"
