"""
CHE·NU V68 Compliance & Regulatory Agent
Vertical 14/15 - ServiceNow GRC Killer

GOVERNANCE COMPLIANCE:
- Rule #1: Audit findings require APPROVAL before resolution
- Rule #1: Incidents require APPROVAL before closure
- Rule #1: Risk assessments require APPROVAL before acceptance
- Rule #5: Policies ALPHABETICAL (not by importance)
- Rule #5: Incidents CHRONOLOGICAL (not by severity)
- Rule #5: Audits CHRONOLOGICAL (not by risk score)
- Rule #6: Full audit trail (UUID, timestamps, created_by)

Competing with: ServiceNow GRC ($150/mo), SAP GRC ($200/mo), LogicGate ($100/mo)
CHE·NU pricing: $29/mo with governance differentiators
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class PolicyStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    ACTIVE = "active"
    RETIRED = "retired"


class ControlStatus(Enum):
    NOT_IMPLEMENTED = "not_implemented"
    PARTIALLY_IMPLEMENTED = "partially_implemented"
    IMPLEMENTED = "implemented"
    NOT_APPLICABLE = "not_applicable"


class AuditStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    FINDINGS_REVIEW = "findings_review"
    PENDING_APPROVAL = "pending_approval"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class FindingSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingStatus(Enum):
    OPEN = "open"
    IN_REMEDIATION = "in_remediation"
    PENDING_VERIFICATION = "pending_verification"
    CLOSED = "closed"


class IncidentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(Enum):
    REPORTED = "reported"
    INVESTIGATING = "investigating"
    CONTAINMENT = "containment"
    REMEDIATION = "remediation"
    PENDING_CLOSURE = "pending_closure"
    CLOSED = "closed"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskStatus(Enum):
    IDENTIFIED = "identified"
    ASSESSING = "assessing"
    PENDING_APPROVAL = "pending_approval"
    ACCEPTED = "accepted"
    MITIGATING = "mitigating"
    MITIGATED = "mitigated"


class CertificationStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"


class DocumentStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    OBSOLETE = "obsolete"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Policy:
    id: UUID
    policy_number: str
    title: str
    description: str
    category: str
    version: str
    status: PolicyStatus
    effective_date: Optional[date]
    review_date: Optional[date]
    owner_id: UUID
    created_by: UUID
    created_at: datetime
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None


@dataclass
class Control:
    id: UUID
    control_id: str  # e.g., "SOC2-CC1.1"
    title: str
    description: str
    framework: str  # SOC2, ISO27001, GDPR, HIPAA
    category: str
    status: ControlStatus
    owner_id: UUID
    evidence_required: List[str]
    last_assessment_date: Optional[date]
    next_assessment_date: Optional[date]
    created_by: UUID
    created_at: datetime


@dataclass
class Audit:
    id: UUID
    audit_number: str
    title: str
    audit_type: str  # Internal, External, Regulatory
    scope: str
    framework: str
    status: AuditStatus
    scheduled_start: date
    scheduled_end: date
    actual_start: Optional[date]
    actual_end: Optional[date]
    lead_auditor_id: UUID
    created_by: UUID
    created_at: datetime
    findings_count: int = 0


@dataclass
class Finding:
    id: UUID
    audit_id: UUID
    finding_number: str
    title: str
    description: str
    severity: FindingSeverity
    status: FindingStatus
    control_id: Optional[UUID]
    root_cause: Optional[str]
    recommendation: str
    remediation_plan: Optional[str]
    due_date: Optional[date]
    assigned_to: Optional[UUID]
    created_by: UUID
    created_at: datetime
    closed_by: Optional[UUID] = None
    closed_at: Optional[datetime] = None


@dataclass
class Incident:
    id: UUID
    incident_number: str
    title: str
    description: str
    category: str  # Data Breach, Policy Violation, Security, etc.
    severity: IncidentSeverity
    status: IncidentStatus
    reported_by: UUID
    reported_at: datetime
    affected_systems: List[str]
    root_cause: Optional[str]
    containment_actions: List[str]
    remediation_actions: List[str]
    lessons_learned: Optional[str]
    created_by: UUID
    created_at: datetime
    closed_by: Optional[UUID] = None
    closed_at: Optional[datetime] = None


@dataclass
class Risk:
    id: UUID
    risk_id: str
    title: str
    description: str
    category: str
    likelihood: int  # 1-5
    impact: int  # 1-5
    inherent_risk: RiskLevel
    residual_risk: Optional[RiskLevel]
    status: RiskStatus
    owner_id: UUID
    mitigating_controls: List[UUID]
    treatment_plan: Optional[str]
    created_by: UUID
    created_at: datetime
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None


@dataclass
class Certification:
    id: UUID
    employee_id: UUID
    employee_name: str
    certification_name: str
    issuing_body: str
    status: CertificationStatus
    issue_date: Optional[date]
    expiry_date: Optional[date]
    certificate_number: Optional[str]
    created_by: UUID
    created_at: datetime


@dataclass
class ControlledDocument:
    id: UUID
    document_number: str
    title: str
    document_type: str  # Policy, Procedure, Standard, Guideline
    version: str
    status: DocumentStatus
    category: str
    owner_id: UUID
    review_cycle_months: int
    last_review_date: Optional[date]
    next_review_date: Optional[date]
    created_by: UUID
    created_at: datetime
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None


# ============================================================================
# COMPLIANCE AGENT
# ============================================================================

class ComplianceAgent:
    """
    CHE·NU V68 Compliance & Regulatory Agent
    
    Governance-first GRC platform:
    - RULE #1: Audits, incidents, risks require APPROVAL
    - RULE #5: ALPHABETICAL/CHRONOLOGICAL ordering only
    - RULE #6: Complete audit trail
    """
    
    def __init__(self):
        self.policies: Dict[UUID, Policy] = {}
        self.controls: Dict[UUID, Control] = {}
        self.audits: Dict[UUID, Audit] = {}
        self.findings: Dict[UUID, Finding] = {}
        self.incidents: Dict[UUID, Incident] = {}
        self.risks: Dict[UUID, Risk] = {}
        self.certifications: Dict[UUID, Certification] = {}
        self.documents: Dict[UUID, ControlledDocument] = {}
        
        self._policy_counter = 0
        self._audit_counter = 0
        self._finding_counters: Dict[UUID, int] = {}
        self._incident_counter = 0
        self._risk_counter = 0
        self._document_counter = 0
        
        logger.info("ComplianceAgent initialized - V68")
    
    # ========================================================================
    # POLICY MANAGEMENT
    # ========================================================================
    
    async def create_policy(
        self,
        title: str,
        description: str,
        category: str,
        owner_id: UUID,
        created_by: UUID,
        version: str = "1.0"
    ) -> Policy:
        """Create a new policy (starts as DRAFT)"""
        self._policy_counter += 1
        policy_number = f"POL-{self._policy_counter:03d}"
        
        policy = Policy(
            id=uuid4(),
            policy_number=policy_number,
            title=title,
            description=description,
            category=category,
            version=version,
            status=PolicyStatus.DRAFT,
            effective_date=None,
            review_date=None,
            owner_id=owner_id,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.policies[policy.id] = policy
        logger.info(f"Policy created: {policy_number} - {title}")
        return policy
    
    async def submit_policy_for_review(
        self,
        policy_id: UUID,
        user_id: UUID
    ) -> Policy:
        """Submit policy for review"""
        if policy_id not in self.policies:
            raise ValueError(f"Policy not found: {policy_id}")
        
        policy = self.policies[policy_id]
        policy.status = PolicyStatus.UNDER_REVIEW
        logger.info(f"Policy {policy.policy_number} submitted for review")
        return policy
    
    async def approve_policy(
        self,
        policy_id: UUID,
        approver_id: UUID,
        effective_date: date
    ) -> Policy:
        """
        GOVERNANCE - Rule #1: Approve a policy
        Human approval required before activation
        """
        if policy_id not in self.policies:
            raise ValueError(f"Policy not found: {policy_id}")
        
        policy = self.policies[policy_id]
        
        if policy.status != PolicyStatus.UNDER_REVIEW:
            raise ValueError("Policy must be under review before approval")
        
        policy.status = PolicyStatus.APPROVED
        policy.approved_by = approver_id
        policy.approved_at = datetime.utcnow()
        policy.effective_date = effective_date
        
        logger.info(f"GOVERNANCE: Policy {policy.policy_number} approved by {approver_id}")
        return policy
    
    async def activate_policy(
        self,
        policy_id: UUID,
        user_id: UUID
    ) -> Policy:
        """Activate an approved policy"""
        if policy_id not in self.policies:
            raise ValueError(f"Policy not found: {policy_id}")
        
        policy = self.policies[policy_id]
        
        if policy.status != PolicyStatus.APPROVED:
            raise ValueError("Policy must be approved before activation")
        
        policy.status = PolicyStatus.ACTIVE
        logger.info(f"Policy {policy.policy_number} activated")
        return policy
    
    async def get_policies(self) -> List[Policy]:
        """
        Get all policies - ALPHABETICAL by title (Rule #5)
        NOT sorted by importance or risk level
        """
        policies = list(self.policies.values())
        # RULE #5: ALPHABETICAL by title
        return sorted(policies, key=lambda p: p.title.lower())
    
    # ========================================================================
    # CONTROL MANAGEMENT
    # ========================================================================
    
    async def create_control(
        self,
        control_id: str,
        title: str,
        description: str,
        framework: str,
        category: str,
        owner_id: UUID,
        evidence_required: List[str],
        created_by: UUID
    ) -> Control:
        """Create a compliance control"""
        control = Control(
            id=uuid4(),
            control_id=control_id,
            title=title,
            description=description,
            framework=framework,
            category=category,
            status=ControlStatus.NOT_IMPLEMENTED,
            owner_id=owner_id,
            evidence_required=evidence_required,
            last_assessment_date=None,
            next_assessment_date=None,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.controls[control.id] = control
        logger.info(f"Control created: {control_id} - {title}")
        return control
    
    async def update_control_status(
        self,
        control_id: UUID,
        new_status: ControlStatus,
        user_id: UUID
    ) -> Control:
        """Update control implementation status"""
        if control_id not in self.controls:
            raise ValueError(f"Control not found: {control_id}")
        
        control = self.controls[control_id]
        control.status = new_status
        control.last_assessment_date = date.today()
        
        logger.info(f"Control {control.control_id} status updated to {new_status.value}")
        return control
    
    async def get_controls_by_framework(self, framework: str) -> List[Control]:
        """
        Get controls by framework - ALPHABETICAL by control_id (Rule #5)
        """
        controls = [c for c in self.controls.values() 
                   if c.framework.lower() == framework.lower()]
        # RULE #5: ALPHABETICAL by control_id
        return sorted(controls, key=lambda c: c.control_id.lower())
    
    # ========================================================================
    # AUDIT MANAGEMENT
    # ========================================================================
    
    async def create_audit(
        self,
        title: str,
        audit_type: str,
        scope: str,
        framework: str,
        scheduled_start: date,
        scheduled_end: date,
        lead_auditor_id: UUID,
        created_by: UUID
    ) -> Audit:
        """Create a new audit"""
        self._audit_counter += 1
        audit_number = f"AUD-{self._audit_counter:03d}"
        
        audit = Audit(
            id=uuid4(),
            audit_number=audit_number,
            title=title,
            audit_type=audit_type,
            scope=scope,
            framework=framework,
            status=AuditStatus.PLANNED,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            actual_start=None,
            actual_end=None,
            lead_auditor_id=lead_auditor_id,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.audits[audit.id] = audit
        self._finding_counters[audit.id] = 0
        logger.info(f"Audit created: {audit_number} - {title}")
        return audit
    
    async def start_audit(
        self,
        audit_id: UUID,
        user_id: UUID
    ) -> Audit:
        """Start an audit"""
        if audit_id not in self.audits:
            raise ValueError(f"Audit not found: {audit_id}")
        
        audit = self.audits[audit_id]
        audit.status = AuditStatus.IN_PROGRESS
        audit.actual_start = date.today()
        
        logger.info(f"Audit {audit.audit_number} started")
        return audit
    
    async def submit_audit_findings(
        self,
        audit_id: UUID,
        user_id: UUID
    ) -> Audit:
        """Submit audit findings for review"""
        if audit_id not in self.audits:
            raise ValueError(f"Audit not found: {audit_id}")
        
        audit = self.audits[audit_id]
        audit.status = AuditStatus.FINDINGS_REVIEW
        
        logger.info(f"Audit {audit.audit_number} findings submitted for review")
        return audit
    
    async def submit_audit_for_approval(
        self,
        audit_id: UUID,
        user_id: UUID
    ) -> Audit:
        """Submit audit for final approval"""
        if audit_id not in self.audits:
            raise ValueError(f"Audit not found: {audit_id}")
        
        audit = self.audits[audit_id]
        audit.status = AuditStatus.PENDING_APPROVAL
        
        logger.info(f"Audit {audit.audit_number} submitted for approval")
        return audit
    
    async def approve_audit(
        self,
        audit_id: UUID,
        approver_id: UUID
    ) -> Audit:
        """
        GOVERNANCE - Rule #1: Approve audit completion
        Human approval required
        """
        if audit_id not in self.audits:
            raise ValueError(f"Audit not found: {audit_id}")
        
        audit = self.audits[audit_id]
        
        if audit.status != AuditStatus.PENDING_APPROVAL:
            raise ValueError("Audit must be pending approval")
        
        audit.status = AuditStatus.COMPLETED
        audit.actual_end = date.today()
        
        logger.info(f"GOVERNANCE: Audit {audit.audit_number} approved by {approver_id}")
        return audit
    
    async def get_audits(self) -> List[Audit]:
        """
        Get all audits - CHRONOLOGICAL by scheduled_start (Rule #5)
        NOT sorted by risk score or priority
        """
        audits = list(self.audits.values())
        # RULE #5: CHRONOLOGICAL
        return sorted(audits, key=lambda a: a.scheduled_start, reverse=True)
    
    # ========================================================================
    # FINDING MANAGEMENT
    # ========================================================================
    
    async def create_finding(
        self,
        audit_id: UUID,
        title: str,
        description: str,
        severity: FindingSeverity,
        recommendation: str,
        created_by: UUID,
        control_id: Optional[UUID] = None,
        due_date: Optional[date] = None
    ) -> Finding:
        """Create an audit finding"""
        if audit_id not in self.audits:
            raise ValueError(f"Audit not found: {audit_id}")
        
        self._finding_counters[audit_id] += 1
        finding_number = f"F-{self._finding_counters[audit_id]:03d}"
        
        finding = Finding(
            id=uuid4(),
            audit_id=audit_id,
            finding_number=finding_number,
            title=title,
            description=description,
            severity=severity,
            status=FindingStatus.OPEN,
            control_id=control_id,
            root_cause=None,
            recommendation=recommendation,
            remediation_plan=None,
            due_date=due_date,
            assigned_to=None,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.findings[finding.id] = finding
        self.audits[audit_id].findings_count += 1
        
        logger.info(f"Finding created: {finding_number} - {title}")
        return finding
    
    async def assign_finding(
        self,
        finding_id: UUID,
        assigned_to: UUID,
        remediation_plan: str,
        user_id: UUID
    ) -> Finding:
        """Assign finding for remediation"""
        if finding_id not in self.findings:
            raise ValueError(f"Finding not found: {finding_id}")
        
        finding = self.findings[finding_id]
        finding.assigned_to = assigned_to
        finding.remediation_plan = remediation_plan
        finding.status = FindingStatus.IN_REMEDIATION
        
        logger.info(f"Finding {finding.finding_number} assigned to {assigned_to}")
        return finding
    
    async def submit_finding_for_verification(
        self,
        finding_id: UUID,
        user_id: UUID
    ) -> Finding:
        """Submit finding remediation for verification"""
        if finding_id not in self.findings:
            raise ValueError(f"Finding not found: {finding_id}")
        
        finding = self.findings[finding_id]
        finding.status = FindingStatus.PENDING_VERIFICATION
        
        logger.info(f"Finding {finding.finding_number} submitted for verification")
        return finding
    
    async def close_finding(
        self,
        finding_id: UUID,
        closed_by: UUID
    ) -> Finding:
        """
        GOVERNANCE - Rule #1: Close a finding
        Human verification required
        """
        if finding_id not in self.findings:
            raise ValueError(f"Finding not found: {finding_id}")
        
        finding = self.findings[finding_id]
        
        if finding.status != FindingStatus.PENDING_VERIFICATION:
            raise ValueError("Finding must be pending verification before closure")
        
        finding.status = FindingStatus.CLOSED
        finding.closed_by = closed_by
        finding.closed_at = datetime.utcnow()
        
        logger.info(f"GOVERNANCE: Finding {finding.finding_number} closed by {closed_by}")
        return finding
    
    async def get_audit_findings(self, audit_id: UUID) -> List[Finding]:
        """
        Get findings for audit - CHRONOLOGICAL by created_at (Rule #5)
        NOT sorted by severity
        """
        findings = [f for f in self.findings.values() if f.audit_id == audit_id]
        # RULE #5: CHRONOLOGICAL
        return sorted(findings, key=lambda f: f.created_at)
    
    # ========================================================================
    # INCIDENT MANAGEMENT
    # ========================================================================
    
    async def report_incident(
        self,
        title: str,
        description: str,
        category: str,
        severity: IncidentSeverity,
        affected_systems: List[str],
        reported_by: UUID
    ) -> Incident:
        """Report a new incident"""
        self._incident_counter += 1
        incident_number = f"INC-{self._incident_counter:03d}"
        
        now = datetime.utcnow()
        incident = Incident(
            id=uuid4(),
            incident_number=incident_number,
            title=title,
            description=description,
            category=category,
            severity=severity,
            status=IncidentStatus.REPORTED,
            reported_by=reported_by,
            reported_at=now,
            affected_systems=affected_systems,
            root_cause=None,
            containment_actions=[],
            remediation_actions=[],
            lessons_learned=None,
            created_by=reported_by,
            created_at=now
        )
        
        self.incidents[incident.id] = incident
        logger.info(f"Incident reported: {incident_number} - {title}")
        return incident
    
    async def update_incident_status(
        self,
        incident_id: UUID,
        new_status: IncidentStatus,
        user_id: UUID
    ) -> Incident:
        """Update incident status"""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident not found: {incident_id}")
        
        incident = self.incidents[incident_id]
        incident.status = new_status
        
        logger.info(f"Incident {incident.incident_number} status updated to {new_status.value}")
        return incident
    
    async def add_containment_action(
        self,
        incident_id: UUID,
        action: str,
        user_id: UUID
    ) -> Incident:
        """Add containment action to incident"""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident not found: {incident_id}")
        
        incident = self.incidents[incident_id]
        incident.containment_actions.append(action)
        
        logger.info(f"Containment action added to incident {incident.incident_number}")
        return incident
    
    async def submit_incident_for_closure(
        self,
        incident_id: UUID,
        root_cause: str,
        lessons_learned: str,
        user_id: UUID
    ) -> Incident:
        """Submit incident for closure approval"""
        if incident_id not in self.incidents:
            raise ValueError(f"Incident not found: {incident_id}")
        
        incident = self.incidents[incident_id]
        incident.root_cause = root_cause
        incident.lessons_learned = lessons_learned
        incident.status = IncidentStatus.PENDING_CLOSURE
        
        logger.info(f"Incident {incident.incident_number} submitted for closure")
        return incident
    
    async def close_incident(
        self,
        incident_id: UUID,
        closed_by: UUID
    ) -> Incident:
        """
        GOVERNANCE - Rule #1: Close an incident
        Human approval required
        """
        if incident_id not in self.incidents:
            raise ValueError(f"Incident not found: {incident_id}")
        
        incident = self.incidents[incident_id]
        
        if incident.status != IncidentStatus.PENDING_CLOSURE:
            raise ValueError("Incident must be pending closure")
        
        incident.status = IncidentStatus.CLOSED
        incident.closed_by = closed_by
        incident.closed_at = datetime.utcnow()
        
        logger.info(f"GOVERNANCE: Incident {incident.incident_number} closed by {closed_by}")
        return incident
    
    async def get_incidents(self) -> List[Incident]:
        """
        Get all incidents - CHRONOLOGICAL by reported_at (Rule #5)
        NOT sorted by severity
        """
        incidents = list(self.incidents.values())
        # RULE #5: CHRONOLOGICAL (newest first)
        return sorted(incidents, key=lambda i: i.reported_at, reverse=True)
    
    # ========================================================================
    # RISK MANAGEMENT
    # ========================================================================
    
    async def identify_risk(
        self,
        title: str,
        description: str,
        category: str,
        likelihood: int,
        impact: int,
        owner_id: UUID,
        created_by: UUID
    ) -> Risk:
        """Identify a new risk"""
        self._risk_counter += 1
        risk_id = f"RISK-{self._risk_counter:03d}"
        
        # Calculate inherent risk level
        risk_score = likelihood * impact
        if risk_score >= 20:
            inherent_risk = RiskLevel.CRITICAL
        elif risk_score >= 12:
            inherent_risk = RiskLevel.HIGH
        elif risk_score >= 6:
            inherent_risk = RiskLevel.MEDIUM
        else:
            inherent_risk = RiskLevel.LOW
        
        risk = Risk(
            id=uuid4(),
            risk_id=risk_id,
            title=title,
            description=description,
            category=category,
            likelihood=likelihood,
            impact=impact,
            inherent_risk=inherent_risk,
            residual_risk=None,
            status=RiskStatus.IDENTIFIED,
            owner_id=owner_id,
            mitigating_controls=[],
            treatment_plan=None,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.risks[risk.id] = risk
        logger.info(f"Risk identified: {risk_id} - {title}")
        return risk
    
    async def assess_risk(
        self,
        risk_id: UUID,
        treatment_plan: str,
        residual_risk: RiskLevel,
        user_id: UUID
    ) -> Risk:
        """Assess and develop treatment plan for risk"""
        if risk_id not in self.risks:
            raise ValueError(f"Risk not found: {risk_id}")
        
        risk = self.risks[risk_id]
        risk.treatment_plan = treatment_plan
        risk.residual_risk = residual_risk
        risk.status = RiskStatus.PENDING_APPROVAL
        
        logger.info(f"Risk {risk.risk_id} assessed")
        return risk
    
    async def approve_risk_treatment(
        self,
        risk_id: UUID,
        approver_id: UUID
    ) -> Risk:
        """
        GOVERNANCE - Rule #1: Approve risk treatment plan
        Human approval required before acceptance or mitigation
        """
        if risk_id not in self.risks:
            raise ValueError(f"Risk not found: {risk_id}")
        
        risk = self.risks[risk_id]
        
        if risk.status != RiskStatus.PENDING_APPROVAL:
            raise ValueError("Risk treatment must be pending approval")
        
        risk.approved_by = approver_id
        risk.approved_at = datetime.utcnow()
        
        # Determine next status based on residual risk
        if risk.residual_risk == RiskLevel.LOW:
            risk.status = RiskStatus.ACCEPTED
        else:
            risk.status = RiskStatus.MITIGATING
        
        logger.info(f"GOVERNANCE: Risk {risk.risk_id} treatment approved by {approver_id}")
        return risk
    
    async def get_risks(self) -> List[Risk]:
        """
        Get all risks - ALPHABETICAL by title (Rule #5)
        NOT sorted by risk level
        """
        risks = list(self.risks.values())
        # RULE #5: ALPHABETICAL
        return sorted(risks, key=lambda r: r.title.lower())
    
    # ========================================================================
    # CERTIFICATION TRACKING
    # ========================================================================
    
    async def add_certification(
        self,
        employee_id: UUID,
        employee_name: str,
        certification_name: str,
        issuing_body: str,
        created_by: UUID,
        issue_date: Optional[date] = None,
        expiry_date: Optional[date] = None
    ) -> Certification:
        """Track employee certification"""
        status = CertificationStatus.NOT_STARTED
        if issue_date:
            if expiry_date and expiry_date < date.today():
                status = CertificationStatus.EXPIRED
            else:
                status = CertificationStatus.COMPLETED
        
        cert = Certification(
            id=uuid4(),
            employee_id=employee_id,
            employee_name=employee_name,
            certification_name=certification_name,
            issuing_body=issuing_body,
            status=status,
            issue_date=issue_date,
            expiry_date=expiry_date,
            certificate_number=None,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.certifications[cert.id] = cert
        logger.info(f"Certification tracked: {employee_name} - {certification_name}")
        return cert
    
    async def get_certifications_by_employee(self, employee_id: UUID) -> List[Certification]:
        """Get certifications for employee - ALPHABETICAL by name (Rule #5)"""
        certs = [c for c in self.certifications.values() 
                if c.employee_id == employee_id]
        return sorted(certs, key=lambda c: c.certification_name.lower())
    
    # ========================================================================
    # DOCUMENT CONTROL
    # ========================================================================
    
    async def create_controlled_document(
        self,
        title: str,
        document_type: str,
        category: str,
        owner_id: UUID,
        review_cycle_months: int,
        created_by: UUID,
        version: str = "1.0"
    ) -> ControlledDocument:
        """Create a controlled document"""
        self._document_counter += 1
        document_number = f"DOC-{self._document_counter:03d}"
        
        doc = ControlledDocument(
            id=uuid4(),
            document_number=document_number,
            title=title,
            document_type=document_type,
            version=version,
            status=DocumentStatus.DRAFT,
            category=category,
            owner_id=owner_id,
            review_cycle_months=review_cycle_months,
            last_review_date=None,
            next_review_date=None,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.documents[doc.id] = doc
        logger.info(f"Document created: {document_number} - {title}")
        return doc
    
    async def approve_document(
        self,
        document_id: UUID,
        approver_id: UUID
    ) -> ControlledDocument:
        """
        GOVERNANCE - Rule #1: Approve document
        Human approval required
        """
        if document_id not in self.documents:
            raise ValueError(f"Document not found: {document_id}")
        
        doc = self.documents[document_id]
        doc.status = DocumentStatus.APPROVED
        doc.approved_by = approver_id
        doc.approved_at = datetime.utcnow()
        doc.last_review_date = date.today()
        
        logger.info(f"GOVERNANCE: Document {doc.document_number} approved by {approver_id}")
        return doc
    
    async def get_documents(self) -> List[ControlledDocument]:
        """Get all documents - ALPHABETICAL by title (Rule #5)"""
        docs = list(self.documents.values())
        return sorted(docs, key=lambda d: d.title.lower())
    
    # ========================================================================
    # ANALYTICS
    # ========================================================================
    
    async def get_compliance_dashboard(self) -> Dict[str, Any]:
        """Get compliance dashboard metrics"""
        return {
            "policies": {
                "total": len(self.policies),
                "active": len([p for p in self.policies.values() 
                              if p.status == PolicyStatus.ACTIVE]),
                "draft": len([p for p in self.policies.values() 
                             if p.status == PolicyStatus.DRAFT])
            },
            "controls": {
                "total": len(self.controls),
                "implemented": len([c for c in self.controls.values() 
                                   if c.status == ControlStatus.IMPLEMENTED]),
                "not_implemented": len([c for c in self.controls.values() 
                                       if c.status == ControlStatus.NOT_IMPLEMENTED])
            },
            "audits": {
                "total": len(self.audits),
                "in_progress": len([a for a in self.audits.values() 
                                   if a.status == AuditStatus.IN_PROGRESS]),
                "completed": len([a for a in self.audits.values() 
                                 if a.status == AuditStatus.COMPLETED])
            },
            "findings": {
                "total": len(self.findings),
                "open": len([f for f in self.findings.values() 
                            if f.status == FindingStatus.OPEN]),
                "closed": len([f for f in self.findings.values() 
                              if f.status == FindingStatus.CLOSED])
            },
            "incidents": {
                "total": len(self.incidents),
                "open": len([i for i in self.incidents.values() 
                            if i.status != IncidentStatus.CLOSED]),
                "closed": len([i for i in self.incidents.values() 
                              if i.status == IncidentStatus.CLOSED])
            },
            "risks": {
                "total": len(self.risks),
                "high_critical": len([r for r in self.risks.values() 
                                     if r.inherent_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]]),
                "mitigating": len([r for r in self.risks.values() 
                                  if r.status == RiskStatus.MITIGATING])
            }
        }


def get_compliance_agent() -> ComplianceAgent:
    """Factory function for ComplianceAgent"""
    return ComplianceAgent()
