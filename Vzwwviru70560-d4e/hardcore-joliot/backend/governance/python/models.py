"""
============================================================================
CHE·NU™ V69 — GOVERNANCE MODELS
============================================================================
Version: 2.0.0
Purpose: Pydantic models for OPA governance
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


# ============================================================================
# ENUMS
# ============================================================================

class Environment(str, Enum):
    """Deployment environments"""
    LABS = "labs"
    PILOT = "pilot"
    PROD = "prod"


class AgentLevel(str, Enum):
    """Agent hierarchy levels"""
    L0 = "L0"  # Nova - System Intelligence
    L1 = "L1"  # User-Hired Agents
    L2 = "L2"  # Platform Agents
    L3 = "L3"  # System Agents


class Sphere(str, Enum):
    """CHE·NU 9 Spheres"""
    PERSONAL = "personal"
    BUSINESS = "business"
    HEALTH = "health"
    CREATIVE = "creative"
    DATA_AI = "data_ai"
    OPERATIONS = "operations"
    COMMUNICATION = "communication"
    FINANCE = "finance"
    LEGAL_COMPLIANCE = "legal_compliance"


class Autonomy(str, Enum):
    """Agent autonomy levels"""
    INFORMATIONAL = "informational"
    ASSISTED = "assisted"
    GOVERNED = "governed"
    RESTRICTED = "restricted"


class RiskLevel(str, Enum):
    """Risk classification"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ActionType(str, Enum):
    """Possible action types"""
    DISCUSS = "discuss"
    PROPOSE = "propose"
    PLAN = "plan"
    EXECUTE = "execute"
    WRITE = "write"
    DELETE = "delete"
    EXPORT = "export"
    CONNECT = "connect"
    RUN_SIMULATION = "RUN_SIMULATION"
    EXPORT_ARTIFACT = "EXPORT_ARTIFACT"
    READ_ARTIFACT = "READ_ARTIFACT"
    COMPARE_SCENARIOS = "COMPARE_SCENARIOS"
    CAUSAL_INTERVENTION = "CAUSAL_INTERVENTION"
    COUNTERFACTUAL_ANALYSIS = "COUNTERFACTUAL_ANALYSIS"
    REQUEST_EXPLAIN = "REQUEST_EXPLAIN"


class ActionTarget(str, Enum):
    """Action targets"""
    SYSTEM = "system"
    API = "api"
    DATA = "data"
    XR = "xr"
    AGENT_REGISTRY = "agent_registry"
    SIMULATION = "simulation"
    ARTIFACT = "artifact"


class DataClassification(str, Enum):
    """Data sensitivity levels"""
    PUBLIC = "public"
    INTERNAL = "internal"
    SENSITIVE = "sensitive"


class AuditLevel(str, Enum):
    """Audit logging levels"""
    STANDARD = "standard"
    ELEVATED = "elevated"
    CRITICAL = "critical"


class TenantPlan(str, Enum):
    """Tenant subscription plans"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


# ============================================================================
# INPUT MODELS
# ============================================================================

class Tenant(BaseModel):
    """Tenant information"""
    id: str = Field(..., description="Tenant UUID")
    plan: TenantPlan = Field(default=TenantPlan.FREE, description="Subscription plan")


class Actor(BaseModel):
    """Actor (user/system) information"""
    type: str = Field(..., description="Actor type: user, org_admin, agent")
    id: str = Field(..., description="Actor UUID")


class Agent(BaseModel):
    """Agent information"""
    blueprint_id: str = Field(..., description="Agent blueprint ID")
    level: AgentLevel = Field(..., description="Agent level L0-L3")
    sphere: Sphere = Field(..., description="Agent's authorized sphere")
    autonomy: Autonomy = Field(default=Autonomy.RESTRICTED, description="Autonomy level")
    risk_level: RiskLevel = Field(default=RiskLevel.LOW, description="Risk classification")
    is_autogen: bool = Field(default=False, description="Is AutoGen agent")
    is_user_hired: bool = Field(default=False, description="Is user-hired agent")
    scope_grants: List[str] = Field(default_factory=list, description="Explicit scope grants")
    prod_pinned: bool = Field(default=False, description="Pinned for PROD access")
    pin_approval_id: Optional[str] = Field(default=None, description="PROD pin approval ID")


class Action(BaseModel):
    """Action being requested"""
    type: ActionType = Field(..., description="Action type")
    target: ActionTarget = Field(..., description="Action target")
    resource_id: str = Field(default="", description="Optional resource ID")
    data_classification: DataClassification = Field(
        default=DataClassification.INTERNAL,
        description="Data sensitivity"
    )
    target_sphere: Optional[Sphere] = Field(default=None, description="Target sphere for cross-sphere actions")


class HITL(BaseModel):
    """Human-In-The-Loop approval"""
    required: bool = Field(default=False, description="Is HITL required")
    approved: bool = Field(default=False, description="Is HITL approved")
    approver_id: Optional[str] = Field(default=None, description="Approver ID")
    approvers: List[str] = Field(default_factory=list, description="List of approvers for multi-approval")
    expires_at: Optional[datetime] = Field(default=None, description="Approval expiration")
    external_approved: bool = Field(default=False, description="External export approval")


class Explainability(BaseModel):
    """Explainability requirements"""
    required: bool = Field(default=True, description="Is explainability required")
    provided: bool = Field(default=False, description="Is explainability provided")


class Controls(BaseModel):
    """Control requirements"""
    audit_logging: bool = Field(default=True, description="Audit logging enabled")
    trace_context: Optional[str] = Field(default=None, description="Trace context ID")


class Resource(BaseModel):
    """Resource being accessed"""
    type: Optional[str] = Field(default=None, description="Resource type")
    synthetic: bool = Field(default=True, description="Is synthetic data")
    steps: Optional[int] = Field(default=None, description="Simulation steps")
    mode: Optional[str] = Field(default="deterministic", description="Simulation mode")
    signature_required: bool = Field(default=False, description="Signature verification required")
    signature_valid: bool = Field(default=False, description="Is signature valid")
    signature_algorithm: Optional[str] = Field(default=None, description="Signature algorithm")
    checksum_valid: bool = Field(default=True, description="Is checksum valid")
    manifest_valid: bool = Field(default=True, description="Is manifest valid")
    signals_valid: bool = Field(default=True, description="Are signals valid")
    visibility: Optional[str] = Field(default="internal", description="Resource visibility")
    tenant_id: Optional[str] = Field(default=None, description="Resource owner tenant")
    destination: Optional[str] = Field(default=None, description="Export destination")
    format: Optional[str] = Field(default=None, description="Export format")
    size_bytes: Optional[int] = Field(default=None, description="Resource size")
    watermark_applied: bool = Field(default=False, description="Watermark applied")
    human_approval_token: Optional[str] = Field(default=None, description="HITL approval token")
    scenario_ids: List[str] = Field(default_factory=list, description="Scenario IDs for comparison")
    explain_range: Optional[Dict[str, int]] = Field(default=None, description="Explain range")
    version_mismatch: bool = Field(default=False, description="Version mismatch detected")
    integrity_check_required: bool = Field(default=False, description="Integrity check required")
    allow_non_deterministic: bool = Field(default=False, description="Allow non-deterministic mode")


class Context(BaseModel):
    """Request context"""
    time: Optional[datetime] = Field(default=None, description="Request time")
    client_app: str = Field(default="labs", description="Client application")
    xr_read_only: bool = Field(default=True, description="XR read-only mode")


class OPARequest(BaseModel):
    """Complete OPA request structure"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Request UUID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Request timestamp")
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Trace ID")
    environment: Environment = Field(default=Environment.LABS, description="Deployment environment")
    tenant: Tenant = Field(..., description="Tenant information")
    actor: Actor = Field(..., description="Actor information")
    agent: Agent = Field(..., description="Agent information")
    action: Action = Field(..., description="Action being requested")
    hitl: HITL = Field(default_factory=HITL, description="HITL status")
    explainability: Explainability = Field(default_factory=Explainability, description="Explainability")
    controls: Controls = Field(default_factory=Controls, description="Control requirements")
    resource: Resource = Field(default_factory=Resource, description="Resource being accessed")
    context: Context = Field(default_factory=Context, description="Request context")
    rate_limit_exceeded: bool = Field(default=False, description="Rate limit exceeded")

    def to_opa_input(self) -> Dict[str, Any]:
        """Convert to OPA input format"""
        return {"request": self.model_dump(mode="json")}


# ============================================================================
# OUTPUT MODELS
# ============================================================================

class OPADecision(BaseModel):
    """OPA decision response"""
    allow: bool = Field(..., description="Allow or deny")
    require_human_approval: bool = Field(default=False, description="HITL required")
    deny_reasons: List[str] = Field(default_factory=list, description="Denial reasons")
    required_controls: List[str] = Field(default_factory=list, description="Required controls")
    audit_level: AuditLevel = Field(default=AuditLevel.STANDARD, description="Audit level")
    synthetic: bool = Field(default=True, description="Synthetic mode")
    trace_id: Optional[str] = Field(default=None, description="Trace ID")
    redactions: List[str] = Field(default_factory=list, description="Data redactions")

    @property
    def is_denied(self) -> bool:
        """Check if request is denied"""
        return not self.allow

    @property
    def needs_hitl(self) -> bool:
        """Check if HITL is needed"""
        return self.require_human_approval or "HITL_APPROVAL_REQUIRED" in self.required_controls


class AuditDecision(BaseModel):
    """Audit record for governance decision"""
    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tenant_id: str = Field(...)
    user_id: str = Field(...)
    agent_id: str = Field(...)
    agent_level: AgentLevel = Field(...)
    environment: Environment = Field(...)
    action_type: ActionType = Field(...)
    action_target: ActionTarget = Field(...)
    decision: OPADecision = Field(...)
    request_hash: Optional[str] = Field(default=None, description="SHA-256 of request")


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_simulation_request(
    tenant_id: str,
    user_id: str,
    agent_blueprint: str,
    steps: int = 100,
    environment: Environment = Environment.LABS,
    sphere: Sphere = Sphere.BUSINESS,
) -> OPARequest:
    """Factory for simulation requests"""
    return OPARequest(
        environment=environment,
        tenant=Tenant(id=tenant_id, plan=TenantPlan.PRO),
        actor=Actor(type="user", id=user_id),
        agent=Agent(
            blueprint_id=agent_blueprint,
            level=AgentLevel.L1,
            sphere=sphere,
            autonomy=Autonomy.ASSISTED,
            risk_level=RiskLevel.LOW,
            is_autogen=False,
            is_user_hired=True,
        ),
        action=Action(
            type=ActionType.RUN_SIMULATION,
            target=ActionTarget.SIMULATION,
            data_classification=DataClassification.INTERNAL,
        ),
        explainability=Explainability(required=True, provided=True),
        controls=Controls(audit_logging=True),
        resource=Resource(
            type="simulation",
            synthetic=True,
            steps=steps,
        ),
    )


def create_export_request(
    tenant_id: str,
    user_id: str,
    agent_blueprint: str,
    artifact_id: str,
    hitl_approved: bool = False,
    approver_id: Optional[str] = None,
) -> OPARequest:
    """Factory for export requests"""
    return OPARequest(
        environment=Environment.LABS,
        tenant=Tenant(id=tenant_id, plan=TenantPlan.PRO),
        actor=Actor(type="user", id=user_id),
        agent=Agent(
            blueprint_id=agent_blueprint,
            level=AgentLevel.L1,
            sphere=Sphere.BUSINESS,
            autonomy=Autonomy.ASSISTED,
            risk_level=RiskLevel.LOW,
            is_autogen=False,
            is_user_hired=True,
        ),
        action=Action(
            type=ActionType.EXPORT_ARTIFACT,
            target=ActionTarget.ARTIFACT,
            resource_id=artifact_id,
            data_classification=DataClassification.INTERNAL,
        ),
        hitl=HITL(
            required=True,
            approved=hitl_approved,
            approver_id=approver_id,
        ),
        explainability=Explainability(required=True, provided=True),
        controls=Controls(audit_logging=True),
        resource=Resource(
            type="artifact",
            synthetic=True,
            format="json",
            destination="signed_download",
        ),
    )
