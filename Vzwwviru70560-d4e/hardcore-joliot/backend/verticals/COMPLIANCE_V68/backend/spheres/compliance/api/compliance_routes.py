"""
CHE·NU™ V68 - Compliance & Regulatory API Routes
ServiceNow GRC Killer - $150/mo → $29/mo with GOVERNANCE

GOVERNANCE COMPLIANCE:
- Rule #1: Policy/audit/finding/incident/risk/document approval requires HUMAN approval
- Rule #5: ALPHABETICAL/CHRONOLOGICAL ordering (NOT by risk/severity/importance)
- Rule #6: Full audit trail with UUID, timestamps, created_by, approved_by
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.spheres.compliance.agents.compliance_agent import (
    ComplianceAgent, ComplianceFramework, FindingSeverity, IncidentSeverity
)

router = APIRouter(prefix="/api/v2/compliance", tags=["Compliance & Regulatory"])

# Initialize agent
agent = ComplianceAgent()

# ============================================================
# REQUEST/RESPONSE MODELS
# ============================================================

# Policy Models
class PolicyCreateRequest(BaseModel):
    title: str
    description: str
    framework: str = "INTERNAL"
    created_by: str

class PolicyApproveRequest(BaseModel):
    approved_by: str

# Control Models
class ControlCreateRequest(BaseModel):
    control_id: str
    title: str
    description: str
    framework: str = "SOC2"
    category: str = "Security"
    created_by: str

class ControlUpdateRequest(BaseModel):
    status: str
    implementation_notes: Optional[str] = None
    updated_by: str

# Audit Models
class AuditCreateRequest(BaseModel):
    title: str
    scope: str
    framework: str = "SOC2"
    lead_auditor: str
    start_date: str  # ISO format
    end_date: str    # ISO format
    created_by: str

class AuditStartRequest(BaseModel):
    started_by: str

class AuditSubmitRequest(BaseModel):
    findings_summary: str
    submitted_by: str

class AuditApproveRequest(BaseModel):
    approved_by: str

# Finding Models
class FindingCreateRequest(BaseModel):
    audit_id: str
    title: str
    description: str
    severity: str = "medium"
    control_id: Optional[str] = None
    created_by: str

class FindingAssignRequest(BaseModel):
    assignee: str
    remediation_plan: str
    due_date: str  # ISO format
    assigned_by: str

class FindingSubmitRequest(BaseModel):
    remediation_notes: str
    submitted_by: str

class FindingCloseRequest(BaseModel):
    verified_by: str
    verification_notes: str

# Incident Models
class IncidentReportRequest(BaseModel):
    title: str
    description: str
    severity: str = "medium"
    affected_systems: List[str] = []
    reported_by: str

class IncidentUpdateRequest(BaseModel):
    status: str
    updated_by: str

class IncidentContainmentRequest(BaseModel):
    action: str
    performed_by: str

class IncidentCloseRequest(BaseModel):
    root_cause: str
    lessons_learned: str
    closed_by: str

# Risk Models
class RiskIdentifyRequest(BaseModel):
    title: str
    description: str
    category: str
    likelihood: int  # 1-5
    impact: int      # 1-5
    identified_by: str

class RiskAssessRequest(BaseModel):
    treatment_plan: str
    residual_likelihood: int
    residual_impact: int
    assessed_by: str

class RiskApproveRequest(BaseModel):
    approved_by: str

# Certification Models
class CertificationAddRequest(BaseModel):
    employee_id: str
    employee_name: str
    certification_name: str
    issuing_body: str
    issue_date: str      # ISO format
    expiry_date: str     # ISO format
    created_by: str

# Document Models
class DocumentCreateRequest(BaseModel):
    title: str
    description: str
    category: str
    content: str
    created_by: str

class DocumentUpdateRequest(BaseModel):
    content: str
    change_summary: str
    updated_by: str

class DocumentApproveRequest(BaseModel):
    approved_by: str

# ============================================================
# POLICY ENDPOINTS
# ============================================================

@router.post("/policies")
async def create_policy(request: PolicyCreateRequest):
    """Create a new compliance policy (starts as DRAFT)."""
    policy = agent.create_policy(
        title=request.title,
        description=request.description,
        framework=request.framework,
        created_by=request.created_by
    )
    return {
        "status": "success",
        "policy": {
            "id": str(policy.id),
            "policy_number": policy.policy_number,
            "title": policy.title,
            "status": policy.status.value,
            "framework": policy.framework.value
        }
    }

@router.post("/policies/{policy_id}/submit")
async def submit_policy_for_review(policy_id: str, submitted_by: str = Query(...)):
    """Submit policy for review."""
    policy = agent.submit_policy_for_review(policy_id, submitted_by)
    return {
        "status": "success",
        "policy": {
            "id": str(policy.id),
            "status": policy.status.value
        }
    }

@router.post("/policies/{policy_id}/approve")
async def approve_policy(policy_id: str, request: PolicyApproveRequest):
    """
    GOVERNANCE (Rule #1): Approve policy - requires human approval.
    Policy cannot be activated without explicit approval.
    """
    policy = agent.approve_policy(policy_id, request.approved_by)
    return {
        "status": "success",
        "governance": "RULE_1_HUMAN_APPROVAL",
        "policy": {
            "id": str(policy.id),
            "status": policy.status.value,
            "approved_by": policy.approved_by,
            "approved_at": policy.approved_at.isoformat() if policy.approved_at else None
        }
    }

@router.post("/policies/{policy_id}/activate")
async def activate_policy(policy_id: str, activated_by: str = Query(...)):
    """Activate an approved policy."""
    policy = agent.activate_policy(policy_id, activated_by)
    return {
        "status": "success",
        "policy": {
            "id": str(policy.id),
            "status": policy.status.value
        }
    }

@router.get("/policies")
async def list_policies(framework: Optional[str] = None):
    """
    List policies - ALPHABETICAL by title (Rule #5).
    NOT sorted by importance or risk level.
    """
    policies = agent.list_policies(framework=framework)
    return {
        "status": "success",
        "rule5_compliance": "ALPHABETICAL_BY_TITLE",
        "policies": [
            {
                "id": str(p.id),
                "policy_number": p.policy_number,
                "title": p.title,
                "status": p.status.value,
                "framework": p.framework.value
            }
            for p in policies
        ]
    }

# ============================================================
# CONTROL ENDPOINTS
# ============================================================

@router.post("/controls")
async def create_control(request: ControlCreateRequest):
    """Create a compliance control."""
    framework = ComplianceFramework[request.framework.upper()]
    control = agent.create_control(
        control_id=request.control_id,
        title=request.title,
        description=request.description,
        framework=framework,
        category=request.category,
        created_by=request.created_by
    )
    return {
        "status": "success",
        "control": {
            "id": str(control.id),
            "control_id": control.control_id,
            "title": control.title,
            "status": control.status.value,
            "framework": control.framework.value
        }
    }

@router.put("/controls/{control_uuid}/status")
async def update_control_status(control_uuid: str, request: ControlUpdateRequest):
    """Update control implementation status."""
    control = agent.update_control_status(
        control_uuid=control_uuid,
        status=request.status,
        implementation_notes=request.implementation_notes,
        updated_by=request.updated_by
    )
    return {
        "status": "success",
        "control": {
            "id": str(control.id),
            "control_id": control.control_id,
            "status": control.status.value
        }
    }

@router.get("/controls")
async def list_controls(framework: Optional[str] = None):
    """
    List controls - ALPHABETICAL by control_id (Rule #5).
    NOT sorted by risk or importance.
    """
    framework_enum = ComplianceFramework[framework.upper()] if framework else None
    controls = agent.list_controls(framework=framework_enum)
    return {
        "status": "success",
        "rule5_compliance": "ALPHABETICAL_BY_CONTROL_ID",
        "controls": [
            {
                "id": str(c.id),
                "control_id": c.control_id,
                "title": c.title,
                "status": c.status.value,
                "framework": c.framework.value
            }
            for c in controls
        ]
    }

# ============================================================
# AUDIT ENDPOINTS
# ============================================================

@router.post("/audits")
async def create_audit(request: AuditCreateRequest):
    """Create a compliance audit."""
    framework = ComplianceFramework[request.framework.upper()]
    audit = agent.create_audit(
        title=request.title,
        scope=request.scope,
        framework=framework,
        lead_auditor=request.lead_auditor,
        start_date=date.fromisoformat(request.start_date),
        end_date=date.fromisoformat(request.end_date),
        created_by=request.created_by
    )
    return {
        "status": "success",
        "audit": {
            "id": str(audit.id),
            "audit_number": audit.audit_number,
            "title": audit.title,
            "status": audit.status.value
        }
    }

@router.post("/audits/{audit_id}/start")
async def start_audit(audit_id: str, request: AuditStartRequest):
    """Start an audit."""
    audit = agent.start_audit(audit_id, request.started_by)
    return {
        "status": "success",
        "audit": {
            "id": str(audit.id),
            "status": audit.status.value
        }
    }

@router.post("/audits/{audit_id}/submit")
async def submit_audit_findings(audit_id: str, request: AuditSubmitRequest):
    """Submit audit findings for review."""
    audit = agent.submit_audit_findings(
        audit_id=audit_id,
        findings_summary=request.findings_summary,
        submitted_by=request.submitted_by
    )
    return {
        "status": "success",
        "audit": {
            "id": str(audit.id),
            "status": audit.status.value
        }
    }

@router.post("/audits/{audit_id}/approve")
async def approve_audit(audit_id: str, request: AuditApproveRequest):
    """
    GOVERNANCE (Rule #1): Approve audit completion.
    Requires human approval before audit can be marked complete.
    """
    audit = agent.approve_audit(audit_id, request.approved_by)
    return {
        "status": "success",
        "governance": "RULE_1_HUMAN_APPROVAL",
        "audit": {
            "id": str(audit.id),
            "status": audit.status.value,
            "approved_by": audit.approved_by
        }
    }

@router.get("/audits")
async def list_audits(framework: Optional[str] = None):
    """
    List audits - CHRONOLOGICAL (Rule #5).
    NOT sorted by risk score or severity.
    """
    framework_enum = ComplianceFramework[framework.upper()] if framework else None
    audits = agent.list_audits(framework=framework_enum)
    return {
        "status": "success",
        "rule5_compliance": "CHRONOLOGICAL_ORDER",
        "audits": [
            {
                "id": str(a.id),
                "audit_number": a.audit_number,
                "title": a.title,
                "status": a.status.value,
                "framework": a.framework.value,
                "created_at": a.created_at.isoformat()
            }
            for a in audits
        ]
    }

# ============================================================
# FINDING ENDPOINTS
# ============================================================

@router.post("/findings")
async def create_finding(request: FindingCreateRequest):
    """Create an audit finding."""
    severity = FindingSeverity[request.severity.upper()]
    finding = agent.create_finding(
        audit_id=request.audit_id,
        title=request.title,
        description=request.description,
        severity=severity,
        control_id=request.control_id,
        created_by=request.created_by
    )
    return {
        "status": "success",
        "finding": {
            "id": str(finding.id),
            "finding_number": finding.finding_number,
            "title": finding.title,
            "severity": finding.severity.value,
            "status": finding.status.value
        }
    }

@router.post("/findings/{finding_id}/assign")
async def assign_finding(finding_id: str, request: FindingAssignRequest):
    """Assign finding for remediation."""
    finding = agent.assign_finding(
        finding_id=finding_id,
        assignee=request.assignee,
        remediation_plan=request.remediation_plan,
        due_date=date.fromisoformat(request.due_date),
        assigned_by=request.assigned_by
    )
    return {
        "status": "success",
        "finding": {
            "id": str(finding.id),
            "status": finding.status.value,
            "assignee": finding.assignee
        }
    }

@router.post("/findings/{finding_id}/submit")
async def submit_finding_remediation(finding_id: str, request: FindingSubmitRequest):
    """Submit finding remediation for verification."""
    finding = agent.submit_finding_remediation(
        finding_id=finding_id,
        remediation_notes=request.remediation_notes,
        submitted_by=request.submitted_by
    )
    return {
        "status": "success",
        "finding": {
            "id": str(finding.id),
            "status": finding.status.value
        }
    }

@router.post("/findings/{finding_id}/close")
async def close_finding(finding_id: str, request: FindingCloseRequest):
    """
    GOVERNANCE (Rule #1): Close finding after verification.
    Requires human verification before closure.
    """
    finding = agent.close_finding(
        finding_id=finding_id,
        verified_by=request.verified_by,
        verification_notes=request.verification_notes
    )
    return {
        "status": "success",
        "governance": "RULE_1_HUMAN_VERIFICATION",
        "finding": {
            "id": str(finding.id),
            "status": finding.status.value,
            "closed_by": finding.closed_by
        }
    }

@router.get("/findings")
async def list_findings(audit_id: Optional[str] = None):
    """
    List findings - CHRONOLOGICAL (Rule #5).
    NOT sorted by severity or risk.
    """
    findings = agent.list_findings(audit_id=audit_id)
    return {
        "status": "success",
        "rule5_compliance": "CHRONOLOGICAL_ORDER",
        "findings": [
            {
                "id": str(f.id),
                "finding_number": f.finding_number,
                "title": f.title,
                "severity": f.severity.value,
                "status": f.status.value,
                "created_at": f.created_at.isoformat()
            }
            for f in findings
        ]
    }

# ============================================================
# INCIDENT ENDPOINTS
# ============================================================

@router.post("/incidents")
async def report_incident(request: IncidentReportRequest):
    """Report a security/compliance incident."""
    severity = IncidentSeverity[request.severity.upper()]
    incident = agent.report_incident(
        title=request.title,
        description=request.description,
        severity=severity,
        affected_systems=request.affected_systems,
        reported_by=request.reported_by
    )
    return {
        "status": "success",
        "incident": {
            "id": str(incident.id),
            "incident_number": incident.incident_number,
            "title": incident.title,
            "severity": incident.severity.value,
            "status": incident.status.value
        }
    }

@router.put("/incidents/{incident_id}/status")
async def update_incident_status(incident_id: str, request: IncidentUpdateRequest):
    """Update incident status."""
    incident = agent.update_incident_status(
        incident_id=incident_id,
        status=request.status,
        updated_by=request.updated_by
    )
    return {
        "status": "success",
        "incident": {
            "id": str(incident.id),
            "status": incident.status.value
        }
    }

@router.post("/incidents/{incident_id}/containment")
async def add_containment_action(incident_id: str, request: IncidentContainmentRequest):
    """Add containment action to incident."""
    incident = agent.add_containment_action(
        incident_id=incident_id,
        action=request.action,
        performed_by=request.performed_by
    )
    return {
        "status": "success",
        "incident": {
            "id": str(incident.id),
            "containment_actions": incident.containment_actions
        }
    }

@router.post("/incidents/{incident_id}/close")
async def close_incident(incident_id: str, request: IncidentCloseRequest):
    """
    GOVERNANCE (Rule #1): Close incident.
    Requires human approval with root cause analysis.
    """
    incident = agent.close_incident(
        incident_id=incident_id,
        root_cause=request.root_cause,
        lessons_learned=request.lessons_learned,
        closed_by=request.closed_by
    )
    return {
        "status": "success",
        "governance": "RULE_1_HUMAN_APPROVAL",
        "incident": {
            "id": str(incident.id),
            "status": incident.status.value,
            "closed_by": incident.closed_by
        }
    }

@router.get("/incidents")
async def list_incidents(status: Optional[str] = None):
    """
    List incidents - CHRONOLOGICAL (Rule #5).
    NOT sorted by severity or priority.
    """
    incidents = agent.list_incidents(status=status)
    return {
        "status": "success",
        "rule5_compliance": "CHRONOLOGICAL_ORDER",
        "incidents": [
            {
                "id": str(i.id),
                "incident_number": i.incident_number,
                "title": i.title,
                "severity": i.severity.value,
                "status": i.status.value,
                "reported_at": i.reported_at.isoformat()
            }
            for i in incidents
        ]
    }

# ============================================================
# RISK ENDPOINTS
# ============================================================

@router.post("/risks")
async def identify_risk(request: RiskIdentifyRequest):
    """Identify a new risk."""
    risk = agent.identify_risk(
        title=request.title,
        description=request.description,
        category=request.category,
        likelihood=request.likelihood,
        impact=request.impact,
        identified_by=request.identified_by
    )
    return {
        "status": "success",
        "risk": {
            "id": str(risk.id),
            "risk_number": risk.risk_number,
            "title": risk.title,
            "inherent_risk_level": risk.inherent_risk_level.value,
            "status": risk.status.value
        }
    }

@router.post("/risks/{risk_id}/assess")
async def assess_risk(risk_id: str, request: RiskAssessRequest):
    """Assess risk with treatment plan."""
    risk = agent.assess_risk(
        risk_id=risk_id,
        treatment_plan=request.treatment_plan,
        residual_likelihood=request.residual_likelihood,
        residual_impact=request.residual_impact,
        assessed_by=request.assessed_by
    )
    return {
        "status": "success",
        "risk": {
            "id": str(risk.id),
            "status": risk.status.value,
            "residual_risk_level": risk.residual_risk_level.value if risk.residual_risk_level else None
        }
    }

@router.post("/risks/{risk_id}/approve")
async def approve_risk_treatment(risk_id: str, request: RiskApproveRequest):
    """
    GOVERNANCE (Rule #1): Approve risk treatment plan.
    Requires human approval.
    """
    risk = agent.approve_risk_treatment(risk_id, request.approved_by)
    return {
        "status": "success",
        "governance": "RULE_1_HUMAN_APPROVAL",
        "risk": {
            "id": str(risk.id),
            "status": risk.status.value,
            "approved_by": risk.approved_by
        }
    }

@router.get("/risks")
async def list_risks(category: Optional[str] = None):
    """
    List risks - ALPHABETICAL by title (Rule #5).
    NOT sorted by risk level or severity.
    """
    risks = agent.list_risks(category=category)
    return {
        "status": "success",
        "rule5_compliance": "ALPHABETICAL_BY_TITLE",
        "risks": [
            {
                "id": str(r.id),
                "risk_number": r.risk_number,
                "title": r.title,
                "inherent_risk_level": r.inherent_risk_level.value,
                "status": r.status.value
            }
            for r in risks
        ]
    }

# ============================================================
# CERTIFICATION ENDPOINTS
# ============================================================

@router.post("/certifications")
async def add_certification(request: CertificationAddRequest):
    """Add employee certification record."""
    cert = agent.add_certification(
        employee_id=request.employee_id,
        employee_name=request.employee_name,
        certification_name=request.certification_name,
        issuing_body=request.issuing_body,
        issue_date=date.fromisoformat(request.issue_date),
        expiry_date=date.fromisoformat(request.expiry_date),
        created_by=request.created_by
    )
    return {
        "status": "success",
        "certification": {
            "id": str(cert.id),
            "employee_name": cert.employee_name,
            "certification_name": cert.certification_name,
            "status": cert.status.value,
            "expiry_date": cert.expiry_date.isoformat()
        }
    }

@router.get("/certifications")
async def list_certifications(employee_id: Optional[str] = None):
    """
    List certifications - ALPHABETICAL by certification name (Rule #5).
    """
    certs = agent.list_certifications(employee_id=employee_id)
    return {
        "status": "success",
        "rule5_compliance": "ALPHABETICAL_BY_CERTIFICATION_NAME",
        "certifications": [
            {
                "id": str(c.id),
                "employee_name": c.employee_name,
                "certification_name": c.certification_name,
                "status": c.status.value,
                "expiry_date": c.expiry_date.isoformat()
            }
            for c in certs
        ]
    }

@router.get("/certifications/expiring")
async def get_expiring_certifications(days: int = Query(default=30)):
    """Get certifications expiring within specified days."""
    certs = agent.get_expiring_certifications(days=days)
    return {
        "status": "success",
        "days_ahead": days,
        "expiring_certifications": [
            {
                "id": str(c.id),
                "employee_name": c.employee_name,
                "certification_name": c.certification_name,
                "expiry_date": c.expiry_date.isoformat()
            }
            for c in certs
        ]
    }

# ============================================================
# DOCUMENT CONTROL ENDPOINTS
# ============================================================

@router.post("/documents")
async def create_controlled_document(request: DocumentCreateRequest):
    """Create a controlled document."""
    doc = agent.create_controlled_document(
        title=request.title,
        description=request.description,
        category=request.category,
        content=request.content,
        created_by=request.created_by
    )
    return {
        "status": "success",
        "document": {
            "id": str(doc.id),
            "document_number": doc.document_number,
            "title": doc.title,
            "version": doc.version,
            "status": doc.status.value
        }
    }

@router.put("/documents/{document_id}")
async def update_document(document_id: str, request: DocumentUpdateRequest):
    """Update document (creates new version)."""
    doc = agent.update_document(
        document_id=document_id,
        content=request.content,
        change_summary=request.change_summary,
        updated_by=request.updated_by
    )
    return {
        "status": "success",
        "document": {
            "id": str(doc.id),
            "version": doc.version,
            "status": doc.status.value
        }
    }

@router.post("/documents/{document_id}/submit")
async def submit_document_for_review(document_id: str, submitted_by: str = Query(...)):
    """Submit document for review."""
    doc = agent.submit_document_for_review(document_id, submitted_by)
    return {
        "status": "success",
        "document": {
            "id": str(doc.id),
            "status": doc.status.value
        }
    }

@router.post("/documents/{document_id}/approve")
async def approve_document(document_id: str, request: DocumentApproveRequest):
    """
    GOVERNANCE (Rule #1): Approve document.
    Requires human approval before document becomes effective.
    """
    doc = agent.approve_document(document_id, request.approved_by)
    return {
        "status": "success",
        "governance": "RULE_1_HUMAN_APPROVAL",
        "document": {
            "id": str(doc.id),
            "status": doc.status.value,
            "approved_by": doc.approved_by
        }
    }

@router.get("/documents")
async def list_documents(category: Optional[str] = None):
    """
    List documents - ALPHABETICAL by title (Rule #5).
    """
    docs = agent.list_documents(category=category)
    return {
        "status": "success",
        "rule5_compliance": "ALPHABETICAL_BY_TITLE",
        "documents": [
            {
                "id": str(d.id),
                "document_number": d.document_number,
                "title": d.title,
                "version": d.version,
                "status": d.status.value
            }
            for d in docs
        ]
    }

# ============================================================
# DASHBOARD & ANALYTICS
# ============================================================

@router.get("/dashboard")
async def get_compliance_dashboard():
    """Get compliance dashboard with all metrics."""
    dashboard = agent.get_compliance_dashboard()
    return {
        "status": "success",
        "dashboard": dashboard
    }

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "compliance",
        "version": "v68",
        "governance_rules": ["RULE_1_HUMAN_APPROVAL", "RULE_5_NO_RANKING", "RULE_6_TRACEABILITY"]
    }


# ============================================================
# MAIN (for testing)
# ============================================================

if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI(title="CHE·NU Compliance API V68")
    app.include_router(router)
    
    uvicorn.run(app, host="0.0.0.0", port=8014)
