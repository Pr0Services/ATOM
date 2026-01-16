"""
============================================================================
CHE·NU™ V69 — POC ENTERPRISE MODULE MODELS
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_POC_ENTERPRISE_INVESTOR_DEMO.md
- CHE-NU_POC_ENTERPRISE_XR_PLAN.md
- CHE-NU_POC_ENTERPRISE_TECHNICAL_PLAN.md
- CHE-NU_Compliance_Legal_Governance.md
- CHE-NU_Enterprise_Readiness_Framework.md

"Governed, HITL, Audit Trails - Never promise autonomy in prod"
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
import hashlib
import json


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    return str(uuid.uuid4())

def compute_hash(data: Any) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif isinstance(data, bytes):
        pass
    else:
        data = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


# ============================================================================
# 1. INVESTOR DEMO MODELS
# ============================================================================

class DemoPhase(str, Enum):
    """Demo phases (3-5 min structure)"""
    HOOK = "hook"           # 15s
    PROBLEM = "problem"     # 30s
    SOLUTION = "solution"   # 60s
    DEMO_LIVE = "demo_live" # 90-120s
    RESULTS = "results"     # 30s
    NEXT_STEPS = "next"     # 30s


@dataclass
class DemoMetric:
    """A metric shown in the demo"""
    name: str
    before_value: float
    after_value: float
    unit: str = "%"
    improvement: str = ""  # e.g., "-20%", "+12%"


@dataclass
class DemoScript:
    """
    Investor demo script.
    
    Per spec: 3-5 min demo with hook, problem, solution, live, results
    """
    script_id: str
    title: str = "CHE·NU Enterprise Demo"
    
    phases: Dict[DemoPhase, str] = field(default_factory=dict)
    metrics: List[DemoMetric] = field(default_factory=list)
    
    # Materials
    dataset_path: str = ""
    xr_capture_path: str = ""
    seed: int = 42  # For reproducibility
    
    # Claims discipline
    claims: List[str] = field(default_factory=lambda: [
        "Never promise autonomy in prod",
        "Always: governed, HITL, audit trails",
    ])


@dataclass
class DemoRun:
    """A single demo run"""
    run_id: str
    script_id: str
    
    steps_executed: int = 0
    metrics_collected: Dict[str, float] = field(default_factory=dict)
    report_generated: bool = False
    xr_ready: bool = False
    
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


# ============================================================================
# 2. XR COCKPIT MODELS
# ============================================================================

class RiskLevel(str, Enum):
    """Visual risk levels"""
    LOW = "low"       # Small anomaly
    MEDIUM = "medium" # Pulsation
    HIGH = "high"     # Glitch + alert


@dataclass
class XRZone:
    """A zone in the XR scene"""
    zone_id: str
    name: str
    position: tuple = (0, 0, 0)
    
    # State
    active_agents: int = 0
    risk_level: RiskLevel = RiskLevel.LOW


@dataclass
class XRAgent:
    """An agent avatar in XR"""
    agent_id: str
    name: str
    zone_id: str
    
    position: tuple = (0, 0, 0)
    state: Dict[str, Any] = field(default_factory=dict)
    last_events: List[str] = field(default_factory=list)


@dataclass
class XRTimeline:
    """Timeline for replay"""
    current_step: int = 0
    total_steps: int = 0
    
    # Scrubber state (read-only)
    scrubber_position: float = 0.0  # 0-1


@dataclass
class XRCockpit:
    """
    XR Cockpit state.
    
    Per spec: Read-only, no actions, no writes
    """
    cockpit_id: str
    
    zones: List[XRZone] = field(default_factory=list)
    agents: List[XRAgent] = field(default_factory=list)
    timeline: XRTimeline = field(default_factory=XRTimeline)
    
    # Data feed
    world_state_path: str = ""
    metrics_path: str = ""
    
    # Governance
    read_only: bool = True  # ENFORCED


# ============================================================================
# 3. COMPLIANCE MODELS
# ============================================================================

class RegulatoryScope(str, Enum):
    """Regulatory frameworks"""
    # Global
    ISO_27001 = "ISO_27001"
    SOC_2 = "SOC_2"
    # Privacy
    GDPR = "GDPR"
    CCPA = "CCPA"
    PIPEDA = "PIPEDA"
    # AI Specific
    EU_AI_ACT = "EU_AI_Act"
    ALGORITHMIC_ACCOUNTABILITY = "Algorithmic_Accountability_Act"
    # Industry
    HIPAA = "HIPAA"
    PCI_DSS = "PCI_DSS"
    SOX = "SOX"


class CompliancePrinciple(str, Enum):
    """Core compliance principles"""
    PREVENT_BEFORE_DETECT = "prevent_before_detect"
    EXPLAIN_BEFORE_EXECUTE = "explain_before_execute"
    RESTRICT_BEFORE_TRUST = "restrict_before_trust"
    DOCUMENT_EVERYTHING = "document_everything"
    HUMAN_OVERRIDE_EXISTS = "human_override_exists"


@dataclass
class ComplianceCheck:
    """A compliance check result"""
    check_id: str
    scope: RegulatoryScope
    requirement: str
    
    passed: bool = False
    evidence: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ComplianceReport:
    """Compliance report"""
    report_id: str
    tenant_id: str
    
    scopes_checked: List[RegulatoryScope] = field(default_factory=list)
    checks: List[ComplianceCheck] = field(default_factory=list)
    
    overall_compliant: bool = False
    generated_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# 4. ENTERPRISE READINESS MODELS
# ============================================================================

class HITLTrigger(str, Enum):
    """HITL trigger conditions"""
    HIGH_RISK_DECISION = "high_risk_decision"
    REGULATED_DATA = "regulated_data"
    IRREVERSIBLE_ACTION = "irreversible_action"
    FINANCIAL_THRESHOLD = "financial_threshold"
    LEGAL_IMPLICATION = "legal_implication"


@dataclass
class HITLRequest:
    """
    Human-in-the-Loop request.
    
    Per spec: Automation without override is illegal in many jurisdictions
    """
    request_id: str
    trigger: HITLTrigger
    action_description: str
    
    requested_at: datetime = field(default_factory=datetime.utcnow)
    approved: Optional[bool] = None
    approver_id: str = ""
    approved_at: Optional[datetime] = None
    
    evidence: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIDisclosure:
    """
    Mandatory AI disclosure.
    
    Per spec: Users must be informed AI is involved
    """
    disclosure_id: str
    
    text: str = """CHE·NU uses artificial intelligence to assist decision-making.
Final responsibility remains with the human user."""
    
    shown_to_user: bool = False
    acknowledged: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EnterpriseChecklist:
    """Enterprise onboarding checklist"""
    checklist_id: str
    tenant_id: str
    
    items: Dict[str, bool] = field(default_factory=lambda: {
        "ai_disclosure_configured": False,
        "hitl_playbook_defined": False,
        "compliance_scopes_set": False,
        "security_review_passed": False,
        "data_classification_done": False,
        "audit_trail_enabled": False,
        "backup_recovery_tested": False,
    })
    
    completed: bool = False


# ============================================================================
# 5. SECURITY MODELS (STRIDE)
# ============================================================================

class ThreatCategory(str, Enum):
    """STRIDE threat categories"""
    SPOOFING = "spoofing"
    TAMPERING = "tampering"
    REPUDIATION = "repudiation"
    INFORMATION_DISCLOSURE = "information_disclosure"
    DENIAL_OF_SERVICE = "denial_of_service"
    ELEVATION_OF_PRIVILEGE = "elevation_of_privilege"


@dataclass
class ThreatAssessment:
    """Security threat assessment"""
    assessment_id: str
    category: ThreatCategory
    asset: str
    
    risk_score: float = 0.0  # 0-10
    mitigation: str = ""
    mitigated: bool = False


@dataclass
class SecurityPosture:
    """Overall security posture"""
    posture_id: str
    tenant_id: str
    
    assessments: List[ThreatAssessment] = field(default_factory=list)
    overall_score: float = 0.0
    
    last_reviewed: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Utils
    "generate_id", "compute_hash",
    # Demo
    "DemoPhase", "DemoMetric", "DemoScript", "DemoRun",
    # XR
    "RiskLevel", "XRZone", "XRAgent", "XRTimeline", "XRCockpit",
    # Compliance
    "RegulatoryScope", "CompliancePrinciple", "ComplianceCheck", "ComplianceReport",
    # Enterprise
    "HITLTrigger", "HITLRequest", "AIDisclosure", "EnterpriseChecklist",
    # Security
    "ThreatCategory", "ThreatAssessment", "SecurityPosture",
]
