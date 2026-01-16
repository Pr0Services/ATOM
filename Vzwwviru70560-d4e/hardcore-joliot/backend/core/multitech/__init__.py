"""
CHE·NU™ — Multi-Tech Integration Module
======================================
Technology stack abstraction and integration framework.

Architecture Levels:
- Level 0: Physical/Network (Fiber, QKD, Sensors)
- Level 1: NOVA Kernel (OPA, Orchestrator, Security)
- Level 2: Hubs (Communication, Navigation, Execution)
- Level 3: Agents (Permanent, Service)
- Level 4: Interfaces (UI, XR, API)

Integration Phases:
- Phase 1: Compatibility (0-6 months)
- Phase 2: Hybridation (6-18 months)
- Phase 3: Photonic/Quantum (18-36 months)
"""

from .multi_tech_integration import (
    MultiTechIntegration,
    TechnologyRegistry,
    Technology,
    TechnologyAdapter,
    TechnologyCategory,
    ArchitectureLevel,
    IntegrationPhase,
    HubTechConfig,
    TechDecisionRule,
    FallbackRule,
    ModularityRule,
    NoLockInRule,
    TransparencyRule,
    SocialImpactRule,
    COMMUNICATION_HUB_CONFIG,
    NAVIGATION_HUB_CONFIG,
    EXECUTION_HUB_CONFIG,
    get_multi_tech_integration
)

__all__ = [
    "MultiTechIntegration",
    "TechnologyRegistry",
    "Technology",
    "TechnologyAdapter",
    "TechnologyCategory",
    "ArchitectureLevel",
    "IntegrationPhase",
    "HubTechConfig",
    "TechDecisionRule",
    "FallbackRule",
    "get_multi_tech_integration",
    "COMMUNICATION_HUB_CONFIG",
    "NAVIGATION_HUB_CONFIG",
    "EXECUTION_HUB_CONFIG"
]
