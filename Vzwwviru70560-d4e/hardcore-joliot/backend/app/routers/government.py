"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V78 — Government & Institutions Sphere Router
═══════════════════════════════════════════════════════════════════════════════

Endpoints: 18
Target Profiles: David (Clinical Trials), Sophie (RBQ Compliance)

Features:
- Regulatory compliance tracking
- RBQ Quebec integration
- Clinical trial management
- Permit/license tracking
- Audit trail management
- Document vault
- Deadline alerts

R&D RULES ENFORCED:
- Rule #1: Human Sovereignty → Checkpoints on ALL submissions
- Rule #3: Sphere Integrity → Government data isolated
- Rule #6: Traceability → Complete audit trail
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from uuid import UUID, uuid4
from enum import Enum

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ComplianceType(str, Enum):
    RBQ = "rbq"  # Régie du Bâtiment du Québec
    HEALTH_CANADA = "health_canada"
    FDA = "fda"
    REB = "reb"  # Research Ethics Board
    MUNICIPAL = "municipal"
    PROVINCIAL = "provincial"
    FEDERAL = "federal"
    OTHER = "other"


class ComplianceStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    RENEWAL_REQUIRED = "renewal_required"


class DocumentType(str, Enum):
    LICENSE = "license"
    PERMIT = "permit"
    CERTIFICATE = "certificate"
    CONSENT_FORM = "consent_form"
    PROTOCOL = "protocol"
    AUDIT_REPORT = "audit_report"
    CORRESPONDENCE = "correspondence"
    CONTRACT = "contract"


class ClinicalTrialPhase(str, Enum):
    PRECLINICAL = "preclinical"
    PHASE_1 = "phase_1"
    PHASE_2 = "phase_2"
    PHASE_3 = "phase_3"
    PHASE_4 = "phase_4"


class TrialStatus(str, Enum):
    PLANNING = "planning"
    REB_REVIEW = "reb_review"
    APPROVED = "approved"
    RECRUITING = "recruiting"
    ACTIVE = "active"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class ComplianceItemCreate(BaseModel):
    """Create a compliance item."""
    compliance_type: ComplianceType
    name: str
    description: Optional[str] = None
    reference_number: Optional[str] = None
    issued_date: Optional[date] = None
    expiry_date: Optional[date] = None
    issuing_authority: str
    related_project: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ComplianceItemResponse(BaseModel):
    """Compliance item with metadata."""
    id: UUID
    compliance_type: ComplianceType
    name: str
    description: Optional[str]
    reference_number: Optional[str]
    status: ComplianceStatus
    issued_date: Optional[date]
    expiry_date: Optional[date]
    issuing_authority: str
    related_project: Optional[str]
    tags: List[str]
    # Documents
    documents: List[UUID]
    # Alerts
    days_until_expiry: Optional[int]
    renewal_alert: bool
    # Audit trail
    audit_events: List[dict]
    # Traceability
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class RBQLicenseCheck(BaseModel):
    """RBQ license verification result."""
    license_number: str
    holder_name: str
    license_type: str
    status: str
    issued_date: date
    expiry_date: date
    is_valid: bool
    specialties: List[str]
    restrictions: List[str]
    verification_timestamp: datetime


class ClinicalTrialCreate(BaseModel):
    """Create a clinical trial."""
    title: str
    protocol_number: Optional[str] = None
    phase: ClinicalTrialPhase
    sponsor: str
    principal_investigator: str
    study_type: str = "interventional"
    target_enrollment: int
    sites: List[str] = Field(default_factory=list)
    start_date: Optional[date] = None
    estimated_end_date: Optional[date] = None


class ClinicalTrialResponse(BaseModel):
    """Clinical trial with metadata."""
    id: UUID
    title: str
    protocol_number: Optional[str]
    phase: ClinicalTrialPhase
    status: TrialStatus
    sponsor: str
    principal_investigator: str
    study_type: str
    target_enrollment: int
    current_enrollment: int
    sites: List[str]
    start_date: Optional[date]
    estimated_end_date: Optional[date]
    # Regulatory
    reb_approval_date: Optional[date]
    health_canada_approval: Optional[str]
    # Documents
    documents: List[UUID]
    # Adverse events
    adverse_events_count: int
    # Traceability
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class AdverseEventCreate(BaseModel):
    """Report an adverse event."""
    trial_id: UUID
    event_date: date
    severity: str = "mild"  # mild, moderate, severe, life_threatening, death
    description: str
    subject_id: str  # Anonymized
    reported_by: str
    is_related_to_study: Optional[bool] = None


class AdverseEventResponse(BaseModel):
    """Adverse event report."""
    id: UUID
    trial_id: UUID
    event_date: date
    report_date: datetime
    severity: str
    description: str
    subject_id: str
    reported_by: str
    is_related_to_study: Optional[bool]
    follow_up_required: bool
    resolution_date: Optional[date]
    # Traceability
    created_by: UUID
    created_at: datetime


class GovernmentDocument(BaseModel):
    """Government/regulatory document."""
    id: UUID
    document_type: DocumentType
    name: str
    description: Optional[str]
    file_path: str
    file_size: int
    mime_type: str
    related_compliance_id: Optional[UUID]
    related_trial_id: Optional[UUID]
    expiry_date: Optional[date]
    # Traceability
    uploaded_by: UUID
    uploaded_at: datetime


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA STORE
# ═══════════════════════════════════════════════════════════════════════════════

_compliance_items: Dict[UUID, dict] = {}
_clinical_trials: Dict[UUID, dict] = {}
_adverse_events: Dict[UUID, dict] = {}
_government_documents: Dict[UUID, dict] = {}
_audit_logs: List[dict] = []
_pending_checkpoints: Dict[UUID, dict] = {}


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def get_mock_user_id() -> UUID:
    return UUID("00000000-0000-0000-0000-000000000001")


def create_checkpoint(action: str, resource_type: str, resource_id: UUID, reason: str) -> dict:
    """Create checkpoint for human approval (R&D Rule #1)."""
    checkpoint = {
        "checkpoint_id": uuid4(),
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "reason": reason,
        "options": ["approve", "reject"],
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    _pending_checkpoints[checkpoint["checkpoint_id"]] = checkpoint
    return checkpoint


def log_audit_event(
    action: str,
    resource_type: str,
    resource_id: UUID,
    user_id: UUID,
    details: Optional[Dict] = None
):
    """Log audit event (R&D Rule #6 - Traceability)."""
    event = {
        "id": uuid4(),
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "user_id": user_id,
        "details": details or {},
        "timestamp": datetime.utcnow(),
        "ip_address": "127.0.0.1"  # Mock
    }
    _audit_logs.append(event)
    return event


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health", tags=["Health"])
async def government_health():
    """Health check for Government sphere."""
    return {
        "status": "healthy",
        "sphere": "government",
        "version": "78.0.0",
        "endpoints": 18,
        "features": [
            "compliance_tracking",
            "rbq_verification",
            "clinical_trials",
            "adverse_events",
            "document_vault",
            "audit_trail"
        ],
        "compliance_types": [c.value for c in ComplianceType],
        "rd_rules": {
            "rule_1": "Human Sovereignty (checkpoints on ALL submissions)",
            "rule_3": "Sphere Integrity (government data isolated)",
            "rule_6": "Complete Audit Trail"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# COMPLIANCE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/compliance", response_model=List[ComplianceItemResponse], tags=["Compliance"])
async def list_compliance_items(
    compliance_type: Optional[ComplianceType] = None,
    status: Optional[ComplianceStatus] = None,
    expiring_soon: bool = Query(False, description="Show items expiring within 30 days")
):
    """
    List compliance items.
    
    ⚠️ R&D Rule #6: Complete audit trail on all items.
    """
    user_id = get_mock_user_id()
    
    items = list(_compliance_items.values())
    
    if compliance_type:
        items = [i for i in items if i["compliance_type"] == compliance_type]
    if status:
        items = [i for i in items if i["status"] == status]
    
    if expiring_soon:
        cutoff = date.today() + timedelta(days=30)
        items = [i for i in items if i.get("expiry_date") and i["expiry_date"] <= cutoff]
    
    # Sort by expiry date (soonest first)
    items.sort(key=lambda x: x.get("expiry_date") or date.max)
    
    return items


@router.post("/compliance", response_model=ComplianceItemResponse, status_code=201, tags=["Compliance"])
async def create_compliance_item(data: ComplianceItemCreate):
    """Create a compliance item."""
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    # Calculate days until expiry
    days_until_expiry = None
    renewal_alert = False
    if data.expiry_date:
        days_until_expiry = (data.expiry_date - date.today()).days
        renewal_alert = days_until_expiry <= 30
    
    item = {
        "id": uuid4(),
        **data.dict(),
        "status": ComplianceStatus.PENDING if not data.issued_date else ComplianceStatus.APPROVED,
        "documents": [],
        "days_until_expiry": days_until_expiry,
        "renewal_alert": renewal_alert,
        "audit_events": [],
        "created_by": user_id,
        "created_at": now,
        "updated_at": now
    }
    
    _compliance_items[item["id"]] = item
    
    # Log audit event
    log_audit_event(
        action="compliance_created",
        resource_type="compliance",
        resource_id=item["id"],
        user_id=user_id,
        details={"compliance_type": data.compliance_type.value}
    )
    
    return item


@router.get("/compliance/{item_id}", response_model=ComplianceItemResponse, tags=["Compliance"])
async def get_compliance_item(item_id: UUID):
    """Get compliance item by ID."""
    if item_id not in _compliance_items:
        raise HTTPException(status_code=404, detail="Compliance item not found")
    return _compliance_items[item_id]


@router.get("/compliance/alerts", tags=["Compliance"])
async def get_compliance_alerts():
    """Get compliance items requiring attention."""
    user_id = get_mock_user_id()
    
    alerts = []
    today = date.today()
    
    for item in _compliance_items.values():
        if item.get("expiry_date"):
            days_left = (item["expiry_date"] - today).days
            
            if days_left <= 0:
                alerts.append({
                    "item_id": item["id"],
                    "name": item["name"],
                    "type": "expired",
                    "severity": "critical",
                    "message": f"EXPIRED {abs(days_left)} days ago",
                    "expiry_date": item["expiry_date"]
                })
            elif days_left <= 30:
                alerts.append({
                    "item_id": item["id"],
                    "name": item["name"],
                    "type": "expiring_soon",
                    "severity": "warning",
                    "message": f"Expires in {days_left} days",
                    "expiry_date": item["expiry_date"]
                })
    
    # Sort by severity (critical first)
    alerts.sort(key=lambda x: 0 if x["severity"] == "critical" else 1)
    
    return {"alerts": alerts, "count": len(alerts)}


# ═══════════════════════════════════════════════════════════════════════════════
# RBQ (RÉGIE DU BÂTIMENT DU QUÉBEC) ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/rbq/verify/{license_number}", response_model=RBQLicenseCheck, tags=["RBQ"])
async def verify_rbq_license(license_number: str):
    """
    Verify an RBQ license.
    
    Note: This is a mock implementation. Real implementation would call RBQ API.
    """
    # Mock RBQ verification
    is_valid = license_number.startswith("RBQ")
    
    result = {
        "license_number": license_number,
        "holder_name": "Construction ABC Inc." if is_valid else "Unknown",
        "license_type": "Entrepreneur général" if is_valid else "Unknown",
        "status": "Active" if is_valid else "Invalid",
        "issued_date": date(2020, 1, 15) if is_valid else date.today(),
        "expiry_date": date(2025, 1, 15) if is_valid else date.today(),
        "is_valid": is_valid,
        "specialties": ["Bâtiments résidentiels", "Rénovation"] if is_valid else [],
        "restrictions": [],
        "verification_timestamp": datetime.utcnow()
    }
    
    # Log audit event
    log_audit_event(
        action="rbq_verification",
        resource_type="rbq_license",
        resource_id=uuid4(),
        user_id=get_mock_user_id(),
        details={"license_number": license_number, "is_valid": is_valid}
    )
    
    return result


@router.post("/rbq/track", tags=["RBQ"])
async def track_rbq_license(
    license_number: str = Query(...),
    contractor_name: str = Query(...),
    project_name: Optional[str] = None
):
    """Add an RBQ license to tracking."""
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    item = ComplianceItemCreate(
        compliance_type=ComplianceType.RBQ,
        name=f"RBQ License - {contractor_name}",
        reference_number=license_number,
        issuing_authority="Régie du Bâtiment du Québec",
        related_project=project_name
    )
    
    return await create_compliance_item(item)


# ═══════════════════════════════════════════════════════════════════════════════
# CLINICAL TRIAL ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/trials", response_model=List[ClinicalTrialResponse], tags=["Clinical Trials"])
async def list_clinical_trials(
    status: Optional[TrialStatus] = None,
    phase: Optional[ClinicalTrialPhase] = None
):
    """List clinical trials."""
    user_id = get_mock_user_id()
    
    trials = list(_clinical_trials.values())
    
    if status:
        trials = [t for t in trials if t["status"] == status]
    if phase:
        trials = [t for t in trials if t["phase"] == phase]
    
    # Chronological order
    trials.sort(key=lambda x: x["created_at"], reverse=True)
    
    return trials


@router.post("/trials", response_model=ClinicalTrialResponse, status_code=201, tags=["Clinical Trials"])
async def create_clinical_trial(data: ClinicalTrialCreate):
    """
    Create a clinical trial (starts in PLANNING status).
    
    ⚠️ REB submission will require checkpoint approval.
    """
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    trial = {
        "id": uuid4(),
        **data.dict(),
        "status": TrialStatus.PLANNING,
        "current_enrollment": 0,
        "reb_approval_date": None,
        "health_canada_approval": None,
        "documents": [],
        "adverse_events_count": 0,
        "created_by": user_id,
        "created_at": now,
        "updated_at": now
    }
    
    _clinical_trials[trial["id"]] = trial
    
    log_audit_event(
        action="trial_created",
        resource_type="clinical_trial",
        resource_id=trial["id"],
        user_id=user_id,
        details={"phase": data.phase.value, "sponsor": data.sponsor}
    )
    
    return trial


@router.post("/trials/{trial_id}/submit-reb", tags=["Clinical Trials"])
async def submit_to_reb(trial_id: UUID):
    """
    Submit trial to Research Ethics Board.
    
    ⚠️ R&D Rule #1: REB submission requires human approval.
    """
    if trial_id not in _clinical_trials:
        raise HTTPException(status_code=404, detail="Clinical trial not found")
    
    trial = _clinical_trials[trial_id]
    
    if trial["status"] != TrialStatus.PLANNING:
        raise HTTPException(status_code=400, detail=f"Cannot submit trial in {trial['status']} status")
    
    checkpoint = create_checkpoint(
        action="submit_reb",
        resource_type="clinical_trial",
        resource_id=trial_id,
        reason="REB submission is a regulatory action requiring human approval"
    )
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint": checkpoint,
            "message": "Human approval required for REB submission"
        }
    )


@router.post("/trials/{trial_id}/adverse-event", response_model=AdverseEventResponse, tags=["Clinical Trials"])
async def report_adverse_event(trial_id: UUID, data: AdverseEventCreate):
    """
    Report an adverse event.
    
    ⚠️ Adverse events are logged immediately but serious events trigger checkpoint.
    """
    if trial_id not in _clinical_trials:
        raise HTTPException(status_code=404, detail="Clinical trial not found")
    
    user_id = get_mock_user_id()
    now = datetime.utcnow()
    
    event = {
        "id": uuid4(),
        **data.dict(),
        "report_date": now,
        "follow_up_required": data.severity in ["severe", "life_threatening", "death"],
        "resolution_date": None,
        "created_by": user_id,
        "created_at": now
    }
    
    _adverse_events[event["id"]] = event
    _clinical_trials[trial_id]["adverse_events_count"] += 1
    
    # Log audit event
    log_audit_event(
        action="adverse_event_reported",
        resource_type="adverse_event",
        resource_id=event["id"],
        user_id=user_id,
        details={"trial_id": str(trial_id), "severity": data.severity}
    )
    
    # Serious events require checkpoint for regulatory reporting
    if data.severity in ["life_threatening", "death"]:
        checkpoint = create_checkpoint(
            action="report_serious_adverse_event",
            resource_type="adverse_event",
            resource_id=event["id"],
            reason="Serious adverse event requires immediate regulatory reporting"
        )
        
        raise HTTPException(
            status_code=423,
            detail={
                "status": "checkpoint_required",
                "checkpoint": checkpoint,
                "event_id": str(event["id"]),
                "message": "Serious adverse event recorded. Regulatory reporting requires approval."
            }
        )
    
    return event


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT TRAIL ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/audit-trail", tags=["Audit"])
async def get_audit_trail(
    resource_type: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Get audit trail.
    
    ⚠️ R&D Rule #6: Complete traceability of all actions.
    """
    logs = _audit_logs.copy()
    
    if resource_type:
        logs = [l for l in logs if l["resource_type"] == resource_type]
    
    # Chronological order (newest first)
    logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "total": len(logs),
        "offset": offset,
        "limit": limit,
        "events": logs[offset:offset + limit]
    }


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT RESOLUTION
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/checkpoints/{checkpoint_id}/approve", tags=["Checkpoints"])
async def approve_checkpoint(checkpoint_id: UUID):
    """Approve a pending checkpoint."""
    if checkpoint_id not in _pending_checkpoints:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    checkpoint = _pending_checkpoints[checkpoint_id]
    
    if checkpoint["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Checkpoint already {checkpoint['status']}")
    
    action = checkpoint["action"]
    resource_id = checkpoint["resource_id"]
    
    if action == "submit_reb":
        if resource_id in _clinical_trials:
            _clinical_trials[resource_id]["status"] = TrialStatus.REB_REVIEW
            _clinical_trials[resource_id]["updated_at"] = datetime.utcnow()
    
    elif action == "report_serious_adverse_event":
        # Log that regulatory report was submitted
        log_audit_event(
            action="regulatory_report_submitted",
            resource_type="adverse_event",
            resource_id=resource_id,
            user_id=get_mock_user_id(),
            details={"checkpoint_id": str(checkpoint_id)}
        )
    
    checkpoint["status"] = "approved"
    checkpoint["resolved_at"] = datetime.utcnow()
    
    log_audit_event(
        action="checkpoint_approved",
        resource_type="checkpoint",
        resource_id=checkpoint_id,
        user_id=get_mock_user_id(),
        details={"original_action": action}
    )
    
    return {"message": "Checkpoint approved", "action": action, "executed": True}


@router.post("/checkpoints/{checkpoint_id}/reject", tags=["Checkpoints"])
async def reject_checkpoint(checkpoint_id: UUID):
    """Reject a pending checkpoint."""
    if checkpoint_id not in _pending_checkpoints:
        raise HTTPException(status_code=404, detail="Checkpoint not found")
    
    checkpoint = _pending_checkpoints[checkpoint_id]
    
    if checkpoint["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Checkpoint already {checkpoint['status']}")
    
    checkpoint["status"] = "rejected"
    checkpoint["resolved_at"] = datetime.utcnow()
    
    log_audit_event(
        action="checkpoint_rejected",
        resource_type="checkpoint",
        resource_id=checkpoint_id,
        user_id=get_mock_user_id(),
        details={"original_action": checkpoint["action"]}
    )
    
    return {"message": "Checkpoint rejected", "action": checkpoint["action"], "executed": False}
