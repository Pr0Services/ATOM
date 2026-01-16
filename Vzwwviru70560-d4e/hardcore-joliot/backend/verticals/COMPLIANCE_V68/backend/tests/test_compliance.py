"""
CHE·NU V68 - Compliance & Regulatory Tests
Vertical 14: ServiceNow GRC Killer

Tests governance compliance:
- Rule #1: Audits, incidents, risks require approval
- Rule #5: Policies ALPHABETICAL, incidents CHRONOLOGICAL
- Rule #6: Full audit trail with UUID, timestamps
"""

import pytest
from uuid import UUID, uuid4
from datetime import datetime, date

import sys
sys.path.insert(0, '/home/claude/COMPLIANCE_V68/backend')

from spheres.compliance.agents.compliance_agent import (
    ComplianceAgent,
    PolicyStatus,
    ControlStatus,
    AuditStatus,
    FindingSeverity,
    FindingStatus,
    IncidentSeverity,
    IncidentStatus,
    RiskLevel,
    RiskStatus,
    CertificationStatus,
    DocumentStatus
)


@pytest.fixture
def agent():
    """Create fresh Compliance agent for each test."""
    return ComplianceAgent()


@pytest.fixture
def user_id():
    return uuid4()


# ============================================================
# POLICY MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_policy(agent, user_id):
    """Test policy creation."""
    policy = await agent.create_policy(
        title="Data Protection Policy",
        description="Guidelines for handling sensitive data",
        category="Security",
        owner_id=user_id,
        created_by=user_id
    )
    
    assert policy is not None
    assert isinstance(policy.id, UUID)
    assert policy.title == "Data Protection Policy"
    assert policy.status == PolicyStatus.DRAFT
    assert policy.policy_number == "POL-001"


@pytest.mark.asyncio
async def test_policy_approval_governance_rule1(agent, user_id):
    """RULE #1: Policy requires GOVERNANCE approval."""
    policy = await agent.create_policy(
        title="Security Policy",
        description="Security guidelines",
        category="Security",
        owner_id=user_id,
        created_by=user_id
    )
    
    # Submit for review
    await agent.submit_policy_for_review(policy.id, user_id)
    
    # GOVERNANCE: Approve
    approver = uuid4()
    approved = await agent.approve_policy(
        policy_id=policy.id,
        approver_id=approver,
        effective_date=date(2026, 2, 1)
    )
    
    assert approved.status == PolicyStatus.APPROVED
    assert approved.approved_by == approver
    assert approved.approved_at is not None


@pytest.mark.asyncio
async def test_policies_alphabetical_rule5(agent, user_id):
    """RULE #5: Policies must be listed ALPHABETICALLY."""
    await agent.create_policy(
        title="Zebra Policy", description="Z",
        category="C1", owner_id=user_id, created_by=user_id
    )
    await agent.create_policy(
        title="Alpha Policy", description="A",
        category="C2", owner_id=user_id, created_by=user_id
    )
    await agent.create_policy(
        title="Beta Policy", description="B",
        category="C3", owner_id=user_id, created_by=user_id
    )
    
    policies = await agent.get_policies()
    
    titles = [p.title for p in policies]
    assert titles == sorted(titles), "RULE #5 VIOLATION: Policies must be ALPHABETICAL"


# ============================================================
# CONTROL MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_control(agent, user_id):
    """Test control creation."""
    control = await agent.create_control(
        control_id="SOC2-CC1.1",
        title="Access Control Management",
        description="Logical and physical access controls",
        framework="SOC2",
        category="Security",
        owner_id=user_id,
        evidence_required=["Access logs", "User reviews"],
        created_by=user_id
    )
    
    assert control is not None
    assert control.control_id == "SOC2-CC1.1"
    assert control.framework == "SOC2"
    assert control.status == ControlStatus.NOT_IMPLEMENTED


@pytest.mark.asyncio
async def test_controls_alphabetical_by_framework_rule5(agent, user_id):
    """RULE #5: Controls ALPHABETICAL by control_id."""
    await agent.create_control(
        control_id="ISO-A.9.1", title="C1", description="D1",
        framework="ISO27001", category="Security",
        owner_id=user_id, evidence_required=[], created_by=user_id
    )
    await agent.create_control(
        control_id="ISO-A.5.1", title="C2", description="D2",
        framework="ISO27001", category="Security",
        owner_id=user_id, evidence_required=[], created_by=user_id
    )
    
    controls = await agent.get_controls_by_framework("ISO27001")
    
    ids = [c.control_id for c in controls]
    assert ids == sorted(ids), "RULE #5 VIOLATION: Controls must be ALPHABETICAL by ID"


# ============================================================
# AUDIT MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_audit(agent, user_id):
    """Test audit creation."""
    audit = await agent.create_audit(
        title="Annual SOC2 Audit",
        audit_type="External",
        scope="All production systems",
        framework="SOC2",
        scheduled_start=date(2026, 3, 1),
        scheduled_end=date(2026, 3, 31),
        lead_auditor_id=user_id,
        created_by=user_id
    )
    
    assert audit is not None
    assert audit.audit_number == "AUD-001"
    assert audit.status == AuditStatus.PLANNED


@pytest.mark.asyncio
async def test_audit_approval_governance_rule1(agent, user_id):
    """RULE #1: Audit completion requires GOVERNANCE approval."""
    audit = await agent.create_audit(
        title="Internal Audit",
        audit_type="Internal",
        scope="Finance systems",
        framework="SOX",
        scheduled_start=date(2026, 3, 1),
        scheduled_end=date(2026, 3, 15),
        lead_auditor_id=user_id,
        created_by=user_id
    )
    
    # Start audit
    await agent.start_audit(audit.id, user_id)
    
    # Submit findings
    await agent.submit_audit_findings(audit.id, user_id)
    
    # Submit for approval
    await agent.submit_audit_for_approval(audit.id, user_id)
    
    # GOVERNANCE: Approve
    approver = uuid4()
    approved = await agent.approve_audit(audit.id, approver)
    
    assert approved.status == AuditStatus.COMPLETED
    assert approved.actual_end is not None


@pytest.mark.asyncio
async def test_audits_chronological_rule5(agent, user_id):
    """RULE #5: Audits listed CHRONOLOGICALLY."""
    await agent.create_audit(
        title="Audit 1", audit_type="Internal",
        scope="S1", framework="F1",
        scheduled_start=date(2026, 1, 1),
        scheduled_end=date(2026, 1, 15),
        lead_auditor_id=user_id, created_by=user_id
    )
    await agent.create_audit(
        title="Audit 2", audit_type="Internal",
        scope="S2", framework="F2",
        scheduled_start=date(2026, 3, 1),
        scheduled_end=date(2026, 3, 15),
        lead_auditor_id=user_id, created_by=user_id
    )
    
    audits = await agent.get_audits()
    
    # Should be newest first (reverse chronological)
    assert len(audits) >= 2
    for i in range(len(audits) - 1):
        assert audits[i].scheduled_start >= audits[i+1].scheduled_start


# ============================================================
# FINDING MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_finding(agent, user_id):
    """Test finding creation."""
    audit = await agent.create_audit(
        title="Test Audit", audit_type="Internal",
        scope="S", framework="F",
        scheduled_start=date(2026, 3, 1),
        scheduled_end=date(2026, 3, 15),
        lead_auditor_id=user_id, created_by=user_id
    )
    
    finding = await agent.create_finding(
        audit_id=audit.id,
        title="Missing Access Logs",
        description="Access logs not retained for 90 days",
        severity=FindingSeverity.HIGH,
        recommendation="Implement log retention policy",
        created_by=user_id
    )
    
    assert finding is not None
    assert finding.finding_number == "F-001"
    assert finding.status == FindingStatus.OPEN


@pytest.mark.asyncio
async def test_finding_closure_governance_rule1(agent, user_id):
    """RULE #1: Finding closure requires GOVERNANCE verification."""
    audit = await agent.create_audit(
        title="Test Audit", audit_type="Internal",
        scope="S", framework="F",
        scheduled_start=date(2026, 3, 1),
        scheduled_end=date(2026, 3, 15),
        lead_auditor_id=user_id, created_by=user_id
    )
    
    finding = await agent.create_finding(
        audit_id=audit.id,
        title="Test Finding",
        description="Description",
        severity=FindingSeverity.MEDIUM,
        recommendation="Fix it",
        created_by=user_id
    )
    
    # Assign and remediate
    await agent.assign_finding(
        finding_id=finding.id,
        assigned_to=user_id,
        remediation_plan="Will fix",
        user_id=user_id
    )
    
    # Submit for verification
    await agent.submit_finding_for_verification(finding.id, user_id)
    
    # GOVERNANCE: Close
    closer = uuid4()
    closed = await agent.close_finding(finding.id, closer)
    
    assert closed.status == FindingStatus.CLOSED
    assert closed.closed_by == closer


# ============================================================
# INCIDENT MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_report_incident(agent, user_id):
    """Test incident reporting."""
    incident = await agent.report_incident(
        title="Data Breach Suspected",
        description="Unusual data access patterns detected",
        category="Data Breach",
        severity=IncidentSeverity.CRITICAL,
        affected_systems=["Database", "API Gateway"],
        reported_by=user_id
    )
    
    assert incident is not None
    assert incident.incident_number == "INC-001"
    assert incident.status == IncidentStatus.REPORTED


@pytest.mark.asyncio
async def test_incident_closure_governance_rule1(agent, user_id):
    """RULE #1: Incident closure requires GOVERNANCE approval."""
    incident = await agent.report_incident(
        title="Test Incident",
        description="Test description",
        category="Security",
        severity=IncidentSeverity.LOW,
        affected_systems=["System A"],
        reported_by=user_id
    )
    
    # Update status through workflow
    await agent.update_incident_status(
        incident.id, IncidentStatus.INVESTIGATING, user_id
    )
    await agent.add_containment_action(
        incident.id, "Isolated affected system", user_id
    )
    
    # Submit for closure
    await agent.submit_incident_for_closure(
        incident_id=incident.id,
        root_cause="Human error",
        lessons_learned="Improve training",
        user_id=user_id
    )
    
    # GOVERNANCE: Close
    closer = uuid4()
    closed = await agent.close_incident(incident.id, closer)
    
    assert closed.status == IncidentStatus.CLOSED
    assert closed.closed_by == closer


@pytest.mark.asyncio
async def test_incidents_chronological_rule5(agent, user_id):
    """RULE #5: Incidents listed CHRONOLOGICALLY (newest first)."""
    await agent.report_incident(
        title="Incident 1", description="D1",
        category="C1", severity=IncidentSeverity.LOW,
        affected_systems=[], reported_by=user_id
    )
    await agent.report_incident(
        title="Incident 2", description="D2",
        category="C2", severity=IncidentSeverity.CRITICAL,
        affected_systems=[], reported_by=user_id
    )
    
    incidents = await agent.get_incidents()
    
    # Should be newest first, NOT by severity
    for i in range(len(incidents) - 1):
        assert incidents[i].reported_at >= incidents[i+1].reported_at


# ============================================================
# RISK MANAGEMENT TESTS
# ============================================================

@pytest.mark.asyncio
async def test_identify_risk(agent, user_id):
    """Test risk identification."""
    risk = await agent.identify_risk(
        title="Third-Party Vendor Risk",
        description="Risk from external vendors with data access",
        category="Third-Party",
        likelihood=4,
        impact=5,
        owner_id=user_id,
        created_by=user_id
    )
    
    assert risk is not None
    assert risk.risk_id == "RISK-001"
    assert risk.status == RiskStatus.IDENTIFIED
    assert risk.inherent_risk == RiskLevel.CRITICAL  # 4*5=20 >= 20


@pytest.mark.asyncio
async def test_risk_treatment_approval_governance_rule1(agent, user_id):
    """RULE #1: Risk treatment requires GOVERNANCE approval."""
    risk = await agent.identify_risk(
        title="Test Risk",
        description="Description",
        category="Operational",
        likelihood=3,
        impact=3,
        owner_id=user_id,
        created_by=user_id
    )
    
    # Assess risk
    await agent.assess_risk(
        risk_id=risk.id,
        treatment_plan="Implement additional controls",
        residual_risk=RiskLevel.LOW,
        user_id=user_id
    )
    
    # GOVERNANCE: Approve treatment
    approver = uuid4()
    approved = await agent.approve_risk_treatment(risk.id, approver)
    
    assert approved.status == RiskStatus.ACCEPTED  # Low residual = accepted
    assert approved.approved_by == approver


@pytest.mark.asyncio
async def test_risks_alphabetical_rule5(agent, user_id):
    """RULE #5: Risks listed ALPHABETICALLY (NOT by risk level)."""
    await agent.identify_risk(
        title="Zebra Risk", description="D",
        category="C", likelihood=5, impact=5,
        owner_id=user_id, created_by=user_id
    )
    await agent.identify_risk(
        title="Alpha Risk", description="D",
        category="C", likelihood=1, impact=1,
        owner_id=user_id, created_by=user_id
    )
    
    risks = await agent.get_risks()
    
    titles = [r.title for r in risks]
    assert titles == sorted(titles), \
        "RULE #5 VIOLATION: Risks must be ALPHABETICAL (NOT by risk level)"


# ============================================================
# CERTIFICATION TRACKING TESTS
# ============================================================

@pytest.mark.asyncio
async def test_add_certification(agent, user_id):
    """Test certification tracking."""
    cert = await agent.add_certification(
        employee_id=user_id,
        employee_name="John Smith",
        certification_name="CISSP",
        issuing_body="ISC2",
        created_by=user_id,
        issue_date=date(2025, 6, 1),
        expiry_date=date(2028, 6, 1)
    )
    
    assert cert is not None
    assert cert.certification_name == "CISSP"
    assert cert.status == CertificationStatus.COMPLETED


# ============================================================
# DOCUMENT CONTROL TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_controlled_document(agent, user_id):
    """Test document creation."""
    doc = await agent.create_controlled_document(
        title="Information Security Policy",
        document_type="Policy",
        category="Security",
        owner_id=user_id,
        review_cycle_months=12,
        created_by=user_id
    )
    
    assert doc is not None
    assert doc.document_number == "DOC-001"
    assert doc.status == DocumentStatus.DRAFT


@pytest.mark.asyncio
async def test_document_approval_governance_rule1(agent, user_id):
    """RULE #1: Document approval requires GOVERNANCE."""
    doc = await agent.create_controlled_document(
        title="Test Document",
        document_type="Procedure",
        category="Operations",
        owner_id=user_id,
        review_cycle_months=6,
        created_by=user_id
    )
    
    # GOVERNANCE: Approve
    approver = uuid4()
    approved = await agent.approve_document(doc.id, approver)
    
    assert approved.status == DocumentStatus.APPROVED
    assert approved.approved_by == approver


@pytest.mark.asyncio
async def test_documents_alphabetical_rule5(agent, user_id):
    """RULE #5: Documents listed ALPHABETICALLY."""
    await agent.create_controlled_document(
        title="Zebra Procedure", document_type="Procedure",
        category="C1", owner_id=user_id,
        review_cycle_months=12, created_by=user_id
    )
    await agent.create_controlled_document(
        title="Alpha Policy", document_type="Policy",
        category="C2", owner_id=user_id,
        review_cycle_months=12, created_by=user_id
    )
    
    docs = await agent.get_documents()
    
    titles = [d.title for d in docs]
    assert titles == sorted(titles)


# ============================================================
# ANALYTICS TESTS
# ============================================================

@pytest.mark.asyncio
async def test_compliance_dashboard(agent, user_id):
    """Test dashboard metrics."""
    # Add some data
    await agent.create_policy(
        title="Policy 1", description="D",
        category="C", owner_id=user_id, created_by=user_id
    )
    await agent.report_incident(
        title="Incident 1", description="D",
        category="C", severity=IncidentSeverity.LOW,
        affected_systems=[], reported_by=user_id
    )
    
    dashboard = await agent.get_compliance_dashboard()
    
    assert "policies" in dashboard
    assert "incidents" in dashboard
    assert "risks" in dashboard
    assert dashboard["policies"]["total"] >= 1


# ============================================================
# AGENT INITIALIZATION TEST
# ============================================================

def test_agent_initialization(agent):
    """Test agent initialization."""
    assert agent is not None
    assert hasattr(agent, 'policies')
    assert hasattr(agent, 'audits')
    assert hasattr(agent, 'incidents')
    assert hasattr(agent, 'risks')


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
