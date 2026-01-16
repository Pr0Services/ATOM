"""
============================================================================
CHE·NU™ V69 — POC ENTERPRISE MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_POC_ENTERPRISE_INVESTOR_DEMO.md
- CHE-NU_POC_ENTERPRISE_XR_PLAN.md
- CHE-NU_POC_ENTERPRISE_TECHNICAL_PLAN.md
- CHE-NU_Compliance_Legal_Governance.md
- CHE-NU_Enterprise_Readiness_Framework.md

"Governed, HITL, Audit Trails - Never promise autonomy in prod"

Principle: GOUVERNANCE > EXÉCUTION, XR = READ ONLY
============================================================================
"""

# Models
from .models import (
    # Utils
    generate_id, compute_hash,
    # Demo
    DemoPhase, DemoMetric, DemoScript, DemoRun,
    # XR
    RiskLevel, XRZone, XRAgent, XRTimeline, XRCockpit,
    # Compliance
    RegulatoryScope, CompliancePrinciple, ComplianceCheck, ComplianceReport,
    # Enterprise
    HITLTrigger, HITLRequest, AIDisclosure, EnterpriseChecklist,
    # Security
    ThreatCategory, ThreatAssessment, SecurityPosture,
)

# Systems
from .systems import (
    InvestorDemoEngine,
    XRCockpitService,
    ComplianceFramework,
    EnterpriseReadinessService,
    SecuritySTRIDEService,
    create_investor_demo,
    create_xr_cockpit,
    create_compliance_framework,
    create_enterprise_readiness,
    create_security_stride,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Utils
    "generate_id", "compute_hash",
    # Demo Models
    "DemoPhase", "DemoMetric", "DemoScript", "DemoRun",
    # XR Models
    "RiskLevel", "XRZone", "XRAgent", "XRTimeline", "XRCockpit",
    # Compliance Models
    "RegulatoryScope", "CompliancePrinciple", "ComplianceCheck", "ComplianceReport",
    # Enterprise Models
    "HITLTrigger", "HITLRequest", "AIDisclosure", "EnterpriseChecklist",
    # Security Models
    "ThreatCategory", "ThreatAssessment", "SecurityPosture",
    # Systems
    "InvestorDemoEngine", "XRCockpitService", "ComplianceFramework",
    "EnterpriseReadinessService", "SecuritySTRIDEService",
    "create_investor_demo", "create_xr_cockpit", "create_compliance_framework",
    "create_enterprise_readiness", "create_security_stride",
]
