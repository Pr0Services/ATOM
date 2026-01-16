"""
CHE·NU V68 Construction & Field Services API Routes
Vertical 13/15

GOVERNANCE ENDPOINTS:
- POST /safety-inspections/{id}/approve - GOVERNANCE Rule #1
- POST /change-orders/{id}/approve - GOVERNANCE Rule #1
- POST /punch-items/{id}/approve - GOVERNANCE Rule #1
"""

from datetime import date
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..agents.construction_agent import (
    get_construction_agent,
    ProjectStatus, RFIStatus, PunchItemStatus, SafetyStatus,
    ChangeOrderStatus, EquipmentStatus, TaskPriority, TaskStatus,
    WeatherCondition
)

router = APIRouter(prefix="/api/v2/construction", tags=["Construction"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CreateProjectRequest(BaseModel):
    name: str
    description: str
    client_name: str
    location: str
    start_date: date
    budget: float
    end_date: Optional[date] = None
    superintendent: Optional[str] = None
    project_manager: Optional[str] = None


class UpdateProjectStatusRequest(BaseModel):
    status: str


class CreateRFIRequest(BaseModel):
    project_id: str
    subject: str
    question: str
    priority: str = "medium"
    due_date: Optional[date] = None
    assigned_to: Optional[str] = None


class RespondRFIRequest(BaseModel):
    response: str


class CreateDailyLogRequest(BaseModel):
    project_id: str
    log_date: date
    weather: str
    workers_onsite: int
    work_completed: str
    temperature_high: Optional[int] = None
    temperature_low: Optional[int] = None
    equipment_used: Optional[List[str]] = None
    delays: Optional[str] = None
    safety_incidents: int = 0
    notes: Optional[str] = None


class CreatePunchItemRequest(BaseModel):
    project_id: str
    location: str
    description: str
    trade: str
    priority: str = "medium"
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None


class UpdatePunchItemStatusRequest(BaseModel):
    status: str


class CreateSafetyInspectionRequest(BaseModel):
    project_id: str
    inspection_type: str
    inspector_name: str
    inspection_date: date
    findings: Optional[List[str]] = None
    corrective_actions: Optional[List[str]] = None
    notes: Optional[str] = None


class SubmitInspectionRequest(BaseModel):
    findings: List[str]
    corrective_actions: List[str]


class ApproveInspectionRequest(BaseModel):
    passed: bool
    notes: Optional[str] = None


class CreateChangeOrderRequest(BaseModel):
    project_id: str
    title: str
    description: str
    reason: str
    cost_impact: float
    schedule_impact_days: int


class ApproveChangeOrderRequest(BaseModel):
    approved: bool


class AddEquipmentRequest(BaseModel):
    name: str
    equipment_type: str
    daily_rate: float
    serial_number: Optional[str] = None
    last_maintenance_date: Optional[date] = None
    next_maintenance_date: Optional[date] = None


class AssignEquipmentRequest(BaseModel):
    project_id: str


class AddSubcontractorRequest(BaseModel):
    company_name: str
    contact_name: str
    email: str
    phone: str
    trade: str
    license_number: Optional[str] = None
    insurance_expiry: Optional[date] = None
    notes: Optional[str] = None


class CreateTaskRequest(BaseModel):
    project_id: str
    title: str
    description: str
    due_date: date
    priority: str = "medium"
    assigned_to: Optional[str] = None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def serialize_project(project) -> dict:
    return {
        "id": str(project.id),
        "name": project.name,
        "description": project.description,
        "client_name": project.client_name,
        "location": project.location,
        "start_date": project.start_date.isoformat(),
        "end_date": project.end_date.isoformat() if project.end_date else None,
        "budget": float(project.budget),
        "status": project.status.value,
        "project_number": project.project_number,
        "superintendent": project.superintendent,
        "project_manager": project.project_manager,
        "created_by": str(project.created_by),
        "created_at": project.created_at.isoformat(),
    }


def serialize_rfi(rfi) -> dict:
    return {
        "id": str(rfi.id),
        "project_id": str(rfi.project_id),
        "rfi_number": rfi.rfi_number,
        "subject": rfi.subject,
        "question": rfi.question,
        "response": rfi.response,
        "status": rfi.status.value,
        "priority": rfi.priority.value,
        "due_date": rfi.due_date.isoformat() if rfi.due_date else None,
        "submitted_by": str(rfi.submitted_by),
        "assigned_to": str(rfi.assigned_to) if rfi.assigned_to else None,
        "created_at": rfi.created_at.isoformat(),
        "responded_at": rfi.responded_at.isoformat() if rfi.responded_at else None,
    }


def serialize_daily_log(log) -> dict:
    return {
        "id": str(log.id),
        "project_id": str(log.project_id),
        "log_date": log.log_date.isoformat(),
        "weather": log.weather.value,
        "temperature_high": log.temperature_high,
        "temperature_low": log.temperature_low,
        "workers_onsite": log.workers_onsite,
        "equipment_used": log.equipment_used,
        "work_completed": log.work_completed,
        "delays": log.delays,
        "safety_incidents": log.safety_incidents,
        "notes": log.notes,
        "created_by": str(log.created_by),
        "created_at": log.created_at.isoformat(),
    }


def serialize_punch_item(item) -> dict:
    return {
        "id": str(item.id),
        "project_id": str(item.project_id),
        "location": item.location,
        "description": item.description,
        "trade": item.trade,
        "status": item.status.value,
        "priority": item.priority.value,
        "assigned_to": str(item.assigned_to) if item.assigned_to else None,
        "due_date": item.due_date.isoformat() if item.due_date else None,
        "created_by": str(item.created_by),
        "created_at": item.created_at.isoformat(),
        "approved_by": str(item.approved_by) if item.approved_by else None,
        "approved_at": item.approved_at.isoformat() if item.approved_at else None,
    }


def serialize_safety_inspection(insp) -> dict:
    return {
        "id": str(insp.id),
        "project_id": str(insp.project_id),
        "inspection_type": insp.inspection_type,
        "inspector_name": insp.inspector_name,
        "inspection_date": insp.inspection_date.isoformat(),
        "status": insp.status.value,
        "findings": insp.findings,
        "corrective_actions": insp.corrective_actions,
        "notes": insp.notes,
        "created_by": str(insp.created_by),
        "created_at": insp.created_at.isoformat(),
        "approved_by": str(insp.approved_by) if insp.approved_by else None,
        "approved_at": insp.approved_at.isoformat() if insp.approved_at else None,
    }


def serialize_change_order(co) -> dict:
    return {
        "id": str(co.id),
        "project_id": str(co.project_id),
        "co_number": co.co_number,
        "title": co.title,
        "description": co.description,
        "reason": co.reason,
        "cost_impact": float(co.cost_impact),
        "schedule_impact_days": co.schedule_impact_days,
        "status": co.status.value,
        "submitted_by": str(co.submitted_by),
        "submitted_at": co.submitted_at.isoformat() if co.submitted_at else None,
        "approved_by": str(co.approved_by) if co.approved_by else None,
        "approved_at": co.approved_at.isoformat() if co.approved_at else None,
        "executed_at": co.executed_at.isoformat() if co.executed_at else None,
        "created_at": co.created_at.isoformat(),
    }


def serialize_equipment(eq) -> dict:
    return {
        "id": str(eq.id),
        "name": eq.name,
        "equipment_type": eq.equipment_type,
        "serial_number": eq.serial_number,
        "status": eq.status.value,
        "current_project_id": str(eq.current_project_id) if eq.current_project_id else None,
        "daily_rate": float(eq.daily_rate),
        "last_maintenance_date": eq.last_maintenance_date.isoformat() if eq.last_maintenance_date else None,
        "next_maintenance_date": eq.next_maintenance_date.isoformat() if eq.next_maintenance_date else None,
        "created_by": str(eq.created_by),
        "created_at": eq.created_at.isoformat(),
    }


def serialize_subcontractor(sub) -> dict:
    return {
        "id": str(sub.id),
        "company_name": sub.company_name,
        "contact_name": sub.contact_name,
        "email": sub.email,
        "phone": sub.phone,
        "trade": sub.trade,
        "license_number": sub.license_number,
        "insurance_expiry": sub.insurance_expiry.isoformat() if sub.insurance_expiry else None,
        "notes": sub.notes,
        "created_by": str(sub.created_by),
        "created_at": sub.created_at.isoformat(),
    }


def serialize_task(task) -> dict:
    return {
        "id": str(task.id),
        "project_id": str(task.project_id),
        "title": task.title,
        "description": task.description,
        "assigned_to": str(task.assigned_to) if task.assigned_to else None,
        "priority": task.priority.value,
        "status": task.status.value,
        "due_date": task.due_date.isoformat(),
        "created_by": str(task.created_by),
        "created_at": task.created_at.isoformat(),
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
    }


# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@router.post("/projects")
async def create_project(request: CreateProjectRequest, user_id: str = Query(...)):
    """Create a new construction project"""
    agent = get_construction_agent()
    project = await agent.create_project(
        name=request.name,
        description=request.description,
        client_name=request.client_name,
        location=request.location,
        start_date=request.start_date,
        budget=Decimal(str(request.budget)),
        created_by=UUID(user_id),
        end_date=request.end_date,
        superintendent=request.superintendent,
        project_manager=request.project_manager
    )
    return serialize_project(project)


@router.get("/projects")
async def get_projects(user_id: str = Query(...)):
    """
    Get all projects - ALPHABETICAL by name (Rule #5)
    NOT sorted by budget, progress, or activity
    """
    agent = get_construction_agent()
    projects = await agent.get_projects(UUID(user_id))
    return {
        "projects": [serialize_project(p) for p in projects],
        "total": len(projects),
        "sort_order": "alphabetical_by_name",  # Rule #5 compliance
    }


@router.get("/projects/{project_id}")
async def get_project(project_id: str):
    """Get project details"""
    agent = get_construction_agent()
    project = await agent.get_project(UUID(project_id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return serialize_project(project)


@router.post("/projects/{project_id}/status")
async def update_project_status(
    project_id: str,
    request: UpdateProjectStatusRequest,
    user_id: str = Query(...)
):
    """Update project status"""
    agent = get_construction_agent()
    try:
        status = ProjectStatus(request.status)
        project = await agent.update_project_status(
            UUID(project_id), status, UUID(user_id)
        )
        return serialize_project(project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/summary")
async def get_project_summary(project_id: str):
    """Get project summary with counts and financials"""
    agent = get_construction_agent()
    try:
        summary = await agent.get_project_summary(UUID(project_id))
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ============================================================================
# RFI ENDPOINTS
# ============================================================================

@router.post("/rfis")
async def create_rfi(request: CreateRFIRequest, user_id: str = Query(...)):
    """Create a new RFI"""
    agent = get_construction_agent()
    try:
        priority = TaskPriority(request.priority)
        rfi = await agent.create_rfi(
            project_id=UUID(request.project_id),
            subject=request.subject,
            question=request.question,
            submitted_by=UUID(user_id),
            priority=priority,
            due_date=request.due_date,
            assigned_to=UUID(request.assigned_to) if request.assigned_to else None
        )
        return serialize_rfi(rfi)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rfis/{rfi_id}/submit")
async def submit_rfi(rfi_id: str, user_id: str = Query(...)):
    """Submit RFI for review"""
    agent = get_construction_agent()
    try:
        rfi = await agent.submit_rfi(UUID(rfi_id), UUID(user_id))
        return serialize_rfi(rfi)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rfis/{rfi_id}/respond")
async def respond_to_rfi(
    rfi_id: str,
    request: RespondRFIRequest,
    user_id: str = Query(...)
):
    """Respond to an RFI"""
    agent = get_construction_agent()
    try:
        rfi = await agent.respond_to_rfi(
            UUID(rfi_id), request.response, UUID(user_id)
        )
        return serialize_rfi(rfi)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rfis/{rfi_id}/close")
async def close_rfi(rfi_id: str, user_id: str = Query(...)):
    """Close an RFI"""
    agent = get_construction_agent()
    try:
        rfi = await agent.close_rfi(UUID(rfi_id), UUID(user_id))
        return serialize_rfi(rfi)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/rfis")
async def get_project_rfis(project_id: str):
    """
    Get RFIs for project - CHRONOLOGICAL (Rule #5)
    NOT sorted by priority
    """
    agent = get_construction_agent()
    rfis = await agent.get_project_rfis(UUID(project_id))
    return {
        "rfis": [serialize_rfi(r) for r in rfis],
        "total": len(rfis),
        "sort_order": "chronological",  # Rule #5 compliance
    }


# ============================================================================
# DAILY LOG ENDPOINTS
# ============================================================================

@router.post("/daily-logs")
async def create_daily_log(request: CreateDailyLogRequest, user_id: str = Query(...)):
    """Create a daily field log"""
    agent = get_construction_agent()
    try:
        weather = WeatherCondition(request.weather)
        log = await agent.create_daily_log(
            project_id=UUID(request.project_id),
            log_date=request.log_date,
            weather=weather,
            workers_onsite=request.workers_onsite,
            work_completed=request.work_completed,
            created_by=UUID(user_id),
            temperature_high=request.temperature_high,
            temperature_low=request.temperature_low,
            equipment_used=request.equipment_used,
            delays=request.delays,
            safety_incidents=request.safety_incidents,
            notes=request.notes
        )
        return serialize_daily_log(log)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/daily-logs")
async def get_project_daily_logs(project_id: str):
    """
    Get daily logs for project - CHRONOLOGICAL (Rule #5)
    """
    agent = get_construction_agent()
    logs = await agent.get_project_daily_logs(UUID(project_id))
    return {
        "daily_logs": [serialize_daily_log(l) for l in logs],
        "total": len(logs),
        "sort_order": "chronological",  # Rule #5 compliance
    }


# ============================================================================
# PUNCH LIST ENDPOINTS
# ============================================================================

@router.post("/punch-items")
async def create_punch_item(request: CreatePunchItemRequest, user_id: str = Query(...)):
    """Create a punch list item"""
    agent = get_construction_agent()
    try:
        priority = TaskPriority(request.priority)
        item = await agent.create_punch_item(
            project_id=UUID(request.project_id),
            location=request.location,
            description=request.description,
            trade=request.trade,
            created_by=UUID(user_id),
            priority=priority,
            assigned_to=UUID(request.assigned_to) if request.assigned_to else None,
            due_date=request.due_date
        )
        return serialize_punch_item(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/punch-items/{item_id}/status")
async def update_punch_item_status(
    item_id: str,
    request: UpdatePunchItemStatusRequest,
    user_id: str = Query(...)
):
    """Update punch item status"""
    agent = get_construction_agent()
    try:
        status = PunchItemStatus(request.status)
        item = await agent.update_punch_item_status(
            UUID(item_id), status, UUID(user_id)
        )
        return serialize_punch_item(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/punch-items/{item_id}/approve")
async def approve_punch_item(item_id: str, user_id: str = Query(...)):
    """
    GOVERNANCE - Rule #1: Approve a punch list item
    Human must approve before item is closed
    """
    agent = get_construction_agent()
    try:
        item = await agent.approve_punch_item(UUID(item_id), UUID(user_id))
        return {
            "governance": "Rule #1 - Human Approval Required",
            "action": "punch_item_approved",
            "item": serialize_punch_item(item)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/punch-items")
async def get_project_punch_items(project_id: str):
    """
    Get punch items for project - ALPHABETICAL by location (Rule #5)
    NOT sorted by priority
    """
    agent = get_construction_agent()
    items = await agent.get_project_punch_items(UUID(project_id))
    return {
        "punch_items": [serialize_punch_item(i) for i in items],
        "total": len(items),
        "sort_order": "alphabetical_by_location",  # Rule #5 compliance
    }


# ============================================================================
# SAFETY INSPECTION ENDPOINTS (GOVERNANCE)
# ============================================================================

@router.post("/safety-inspections")
async def create_safety_inspection(
    request: CreateSafetyInspectionRequest,
    user_id: str = Query(...)
):
    """Create a safety inspection"""
    agent = get_construction_agent()
    try:
        inspection = await agent.create_safety_inspection(
            project_id=UUID(request.project_id),
            inspection_type=request.inspection_type,
            inspector_name=request.inspector_name,
            inspection_date=request.inspection_date,
            created_by=UUID(user_id),
            findings=request.findings,
            corrective_actions=request.corrective_actions,
            notes=request.notes
        )
        return serialize_safety_inspection(inspection)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/safety-inspections/{inspection_id}/submit")
async def submit_inspection_for_approval(
    inspection_id: str,
    request: SubmitInspectionRequest,
    user_id: str = Query(...)
):
    """Submit inspection findings for approval"""
    agent = get_construction_agent()
    try:
        inspection = await agent.submit_inspection_for_approval(
            UUID(inspection_id),
            request.findings,
            request.corrective_actions,
            UUID(user_id)
        )
        return {
            "message": "Inspection submitted for approval",
            "governance": "Rule #1 - Requires human approval before closing",
            "inspection": serialize_safety_inspection(inspection)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/safety-inspections/{inspection_id}/approve")
async def approve_safety_inspection(
    inspection_id: str,
    request: ApproveInspectionRequest,
    user_id: str = Query(...)
):
    """
    GOVERNANCE - Rule #1: Approve or fail a safety inspection
    REQUIRES human approval before closing
    """
    agent = get_construction_agent()
    try:
        inspection = await agent.approve_safety_inspection(
            UUID(inspection_id),
            request.passed,
            UUID(user_id),
            request.notes
        )
        return {
            "governance": "Rule #1 - Human Approval Required",
            "action": "safety_inspection_approved",
            "result": "PASSED" if request.passed else "FAILED",
            "inspection": serialize_safety_inspection(inspection)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/safety-inspections")
async def get_project_safety_inspections(project_id: str):
    """
    Get safety inspections for project - CHRONOLOGICAL (Rule #5)
    """
    agent = get_construction_agent()
    inspections = await agent.get_project_safety_inspections(UUID(project_id))
    return {
        "safety_inspections": [serialize_safety_inspection(i) for i in inspections],
        "total": len(inspections),
        "sort_order": "chronological",  # Rule #5 compliance
    }


# ============================================================================
# CHANGE ORDER ENDPOINTS (GOVERNANCE)
# ============================================================================

@router.post("/change-orders")
async def create_change_order(request: CreateChangeOrderRequest, user_id: str = Query(...)):
    """Create a change order"""
    agent = get_construction_agent()
    try:
        co = await agent.create_change_order(
            project_id=UUID(request.project_id),
            title=request.title,
            description=request.description,
            reason=request.reason,
            cost_impact=Decimal(str(request.cost_impact)),
            schedule_impact_days=request.schedule_impact_days,
            submitted_by=UUID(user_id)
        )
        return serialize_change_order(co)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/change-orders/{co_id}/submit")
async def submit_change_order(co_id: str, user_id: str = Query(...)):
    """Submit change order for approval"""
    agent = get_construction_agent()
    try:
        co = await agent.submit_change_order(UUID(co_id), UUID(user_id))
        return {
            "message": "Change order submitted for approval",
            "governance": "Rule #1 - Requires human approval before execution",
            "change_order": serialize_change_order(co)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/change-orders/{co_id}/approve")
async def approve_change_order(
    co_id: str,
    request: ApproveChangeOrderRequest,
    user_id: str = Query(...)
):
    """
    GOVERNANCE - Rule #1: Approve or reject a change order
    REQUIRES human approval before execution
    """
    agent = get_construction_agent()
    try:
        co = await agent.approve_change_order(
            UUID(co_id), request.approved, UUID(user_id)
        )
        return {
            "governance": "Rule #1 - Human Approval Required",
            "action": "change_order_approved" if request.approved else "change_order_rejected",
            "change_order": serialize_change_order(co)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/change-orders/{co_id}/execute")
async def execute_change_order(co_id: str, user_id: str = Query(...)):
    """
    Execute an approved change order
    Can only be executed after GOVERNANCE approval
    """
    agent = get_construction_agent()
    try:
        co = await agent.execute_change_order(UUID(co_id), UUID(user_id))
        return {
            "message": "Change order executed",
            "governance": "Rule #1 - Executed after human approval",
            "change_order": serialize_change_order(co)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/change-orders")
async def get_project_change_orders(project_id: str):
    """
    Get change orders for project - CHRONOLOGICAL (Rule #5)
    """
    agent = get_construction_agent()
    cos = await agent.get_project_change_orders(UUID(project_id))
    return {
        "change_orders": [serialize_change_order(c) for c in cos],
        "total": len(cos),
        "sort_order": "chronological",  # Rule #5 compliance
    }


# ============================================================================
# EQUIPMENT ENDPOINTS
# ============================================================================

@router.post("/equipment")
async def add_equipment(request: AddEquipmentRequest, user_id: str = Query(...)):
    """Add equipment to inventory"""
    agent = get_construction_agent()
    eq = await agent.add_equipment(
        name=request.name,
        equipment_type=request.equipment_type,
        daily_rate=Decimal(str(request.daily_rate)),
        created_by=UUID(user_id),
        serial_number=request.serial_number,
        last_maintenance_date=request.last_maintenance_date,
        next_maintenance_date=request.next_maintenance_date
    )
    return serialize_equipment(eq)


@router.get("/equipment")
async def get_equipment():
    """
    Get all equipment - ALPHABETICAL by name (Rule #5)
    NOT sorted by utilization or rate
    """
    agent = get_construction_agent()
    equipment = await agent.get_equipment()
    return {
        "equipment": [serialize_equipment(e) for e in equipment],
        "total": len(equipment),
        "sort_order": "alphabetical_by_name",  # Rule #5 compliance
    }


@router.post("/equipment/{equipment_id}/assign")
async def assign_equipment(
    equipment_id: str,
    request: AssignEquipmentRequest,
    user_id: str = Query(...)
):
    """Assign equipment to a project"""
    agent = get_construction_agent()
    try:
        eq = await agent.assign_equipment_to_project(
            UUID(equipment_id), UUID(request.project_id), UUID(user_id)
        )
        return serialize_equipment(eq)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/equipment/{equipment_id}/release")
async def release_equipment(equipment_id: str, user_id: str = Query(...)):
    """Release equipment from project"""
    agent = get_construction_agent()
    try:
        eq = await agent.release_equipment(UUID(equipment_id), UUID(user_id))
        return serialize_equipment(eq)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# SUBCONTRACTOR ENDPOINTS
# ============================================================================

@router.post("/subcontractors")
async def add_subcontractor(request: AddSubcontractorRequest, user_id: str = Query(...)):
    """Add a subcontractor"""
    agent = get_construction_agent()
    sub = await agent.add_subcontractor(
        company_name=request.company_name,
        contact_name=request.contact_name,
        email=request.email,
        phone=request.phone,
        trade=request.trade,
        created_by=UUID(user_id),
        license_number=request.license_number,
        insurance_expiry=request.insurance_expiry,
        notes=request.notes
    )
    return serialize_subcontractor(sub)


@router.get("/subcontractors")
async def get_subcontractors():
    """
    Get all subcontractors - ALPHABETICAL by company name (Rule #5)
    NOT sorted by rating or past performance
    """
    agent = get_construction_agent()
    subs = await agent.get_subcontractors()
    return {
        "subcontractors": [serialize_subcontractor(s) for s in subs],
        "total": len(subs),
        "sort_order": "alphabetical_by_company_name",  # Rule #5 compliance
    }


@router.get("/subcontractors/by-trade/{trade}")
async def get_subcontractors_by_trade(trade: str):
    """
    Get subcontractors by trade - ALPHABETICAL (Rule #5)
    """
    agent = get_construction_agent()
    subs = await agent.get_subcontractors_by_trade(trade)
    return {
        "subcontractors": [serialize_subcontractor(s) for s in subs],
        "total": len(subs),
        "trade": trade,
        "sort_order": "alphabetical",  # Rule #5 compliance
    }


# ============================================================================
# TASK ENDPOINTS
# ============================================================================

@router.post("/tasks")
async def create_task(request: CreateTaskRequest, user_id: str = Query(...)):
    """Create a project task"""
    agent = get_construction_agent()
    try:
        priority = TaskPriority(request.priority)
        task = await agent.create_task(
            project_id=UUID(request.project_id),
            title=request.title,
            description=request.description,
            due_date=request.due_date,
            created_by=UUID(user_id),
            priority=priority,
            assigned_to=UUID(request.assigned_to) if request.assigned_to else None
        )
        return serialize_task(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tasks/{task_id}/complete")
async def complete_task(task_id: str, user_id: str = Query(...)):
    """Mark a task as completed"""
    agent = get_construction_agent()
    try:
        task = await agent.complete_task(UUID(task_id), UUID(user_id))
        return serialize_task(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/tasks")
async def get_project_tasks(project_id: str):
    """
    Get tasks for project - CHRONOLOGICAL by due_date (Rule #5)
    Earliest due first
    """
    agent = get_construction_agent()
    tasks = await agent.get_project_tasks(UUID(project_id))
    return {
        "tasks": [serialize_task(t) for t in tasks],
        "total": len(tasks),
        "sort_order": "chronological_by_due_date",  # Rule #5 compliance
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Construction service health check"""
    return {
        "status": "healthy",
        "service": "construction",
        "version": "v68",
        "governance": {
            "rule_1": "Safety inspections and change orders require approval",
            "rule_5": "All listings alphabetical or chronological (no ranking)",
            "rule_6": "Full audit trail with UUID, timestamps, created_by"
        }
    }
