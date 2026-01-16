"""
CHE·NU V68 Construction & Field Services Agent
Vertical 13/15 - Procore Killer

GOVERNANCE COMPLIANCE:
- Rule #1: Safety inspections require APPROVAL before closing
- Rule #1: Change orders require APPROVAL before execution
- Rule #5: Projects ALPHABETICAL (not by budget/progress)
- Rule #5: RFIs CHRONOLOGICAL (not by priority)
- Rule #5: Subcontractors ALPHABETICAL (NOT by rating)
- Rule #6: Full audit trail (UUID, timestamps, created_by)

Competing with: Procore ($125/mo), Buildertrend ($99/mo), PlanGrid ($39/mo)
CHE·NU pricing: $29/mo with governance differentiators
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class ProjectStatus(Enum):
    PLANNING = "planning"
    BIDDING = "bidding"
    AWARDED = "awarded"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RFIStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    RESPONDED = "responded"
    CLOSED = "closed"


class PunchItemStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    READY_FOR_REVIEW = "ready_for_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class SafetyStatus(Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    PENDING_APPROVAL = "pending_approval"
    PASSED = "passed"
    FAILED = "failed"
    REQUIRES_FOLLOWUP = "requires_followup"


class ChangeOrderStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"


class EquipmentStatus(Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    OUT_OF_SERVICE = "out_of_service"


class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"


class WeatherCondition(Enum):
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"
    SNOWY = "snowy"
    WINDY = "windy"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Project:
    id: UUID
    name: str
    description: str
    client_name: str
    location: str
    start_date: date
    end_date: Optional[date]
    budget: Decimal
    status: ProjectStatus
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    project_number: str  # Sequential PRJ-001, PRJ-002
    superintendent: Optional[str] = None
    project_manager: Optional[str] = None


@dataclass
class RFI:
    """Request for Information"""
    id: UUID
    project_id: UUID
    rfi_number: str  # Sequential RFI-001, RFI-002
    subject: str
    question: str
    response: Optional[str]
    status: RFIStatus
    priority: TaskPriority
    due_date: Optional[date]
    submitted_by: UUID
    assigned_to: Optional[UUID]
    created_at: datetime
    responded_at: Optional[datetime]
    closed_at: Optional[datetime]


@dataclass
class DailyLog:
    id: UUID
    project_id: UUID
    log_date: date
    weather: WeatherCondition
    temperature_high: Optional[int]
    temperature_low: Optional[int]
    workers_onsite: int
    equipment_used: List[str]
    work_completed: str
    delays: Optional[str]
    safety_incidents: int
    notes: Optional[str]
    created_by: UUID
    created_at: datetime


@dataclass
class PunchItem:
    id: UUID
    project_id: UUID
    location: str
    description: str
    trade: str  # Electrical, Plumbing, HVAC, etc.
    status: PunchItemStatus
    priority: TaskPriority
    assigned_to: Optional[UUID]
    due_date: Optional[date]
    created_by: UUID
    created_at: datetime
    completed_at: Optional[datetime]
    approved_by: Optional[UUID]  # GOVERNANCE - Rule #1
    approved_at: Optional[datetime]


@dataclass
class SafetyInspection:
    """GOVERNANCE - Rule #1: Requires approval before closing"""
    id: UUID
    project_id: UUID
    inspection_type: str  # Weekly, OSHA, Fall Protection, etc.
    inspector_name: str
    inspection_date: date
    status: SafetyStatus
    findings: List[str]
    corrective_actions: List[str]
    created_by: UUID
    created_at: datetime
    approved_by: Optional[UUID]  # Required for pass/fail
    approved_at: Optional[datetime]
    notes: Optional[str] = None


@dataclass
class ChangeOrder:
    """GOVERNANCE - Rule #1: Requires approval before execution"""
    id: UUID
    project_id: UUID
    co_number: str  # Sequential CO-001, CO-002
    title: str
    description: str
    reason: str
    cost_impact: Decimal  # Can be negative for credits
    schedule_impact_days: int
    status: ChangeOrderStatus
    submitted_by: UUID
    submitted_at: Optional[datetime]
    approved_by: Optional[UUID]  # Required for execution
    approved_at: Optional[datetime]
    executed_at: Optional[datetime]
    created_at: datetime


@dataclass
class Equipment:
    id: UUID
    name: str
    equipment_type: str
    serial_number: Optional[str]
    status: EquipmentStatus
    current_project_id: Optional[UUID]
    daily_rate: Decimal
    last_maintenance_date: Optional[date]
    next_maintenance_date: Optional[date]
    created_by: UUID
    created_at: datetime


@dataclass
class Subcontractor:
    id: UUID
    company_name: str
    contact_name: str
    email: str
    phone: str
    trade: str
    license_number: Optional[str]
    insurance_expiry: Optional[date]
    created_by: UUID
    created_at: datetime
    notes: Optional[str] = None


@dataclass
class Task:
    id: UUID
    project_id: UUID
    title: str
    description: str
    assigned_to: Optional[UUID]
    priority: TaskPriority
    status: TaskStatus
    due_date: date
    created_by: UUID
    created_at: datetime
    completed_at: Optional[datetime]


# ============================================================================
# CONSTRUCTION AGENT
# ============================================================================

class ConstructionAgent:
    """
    CHE·NU V68 Construction & Field Services Agent
    
    GOVERNANCE COMPLIANCE:
    - Rule #1: Safety inspections require APPROVAL
    - Rule #1: Change orders require APPROVAL before execution
    - Rule #5: All listings ALPHABETICAL or CHRONOLOGICAL (NO ranking by metrics)
    - Rule #6: Full audit trail with UUID, timestamps, created_by
    """
    
    def __init__(self):
        self.projects: Dict[UUID, Project] = {}
        self.rfis: Dict[UUID, RFI] = {}
        self.daily_logs: Dict[UUID, DailyLog] = {}
        self.punch_items: Dict[UUID, PunchItem] = {}
        self.safety_inspections: Dict[UUID, SafetyInspection] = {}
        self.change_orders: Dict[UUID, ChangeOrder] = {}
        self.equipment: Dict[UUID, Equipment] = {}
        self.subcontractors: Dict[UUID, Subcontractor] = {}
        self.tasks: Dict[UUID, Task] = {}
        
        # Counters for sequential numbering
        self._project_counter = 0
        self._rfi_counters: Dict[UUID, int] = {}  # Per project
        self._co_counters: Dict[UUID, int] = {}  # Per project
    
    # ========================================================================
    # PROJECT MANAGEMENT
    # ========================================================================
    
    async def create_project(
        self,
        name: str,
        description: str,
        client_name: str,
        location: str,
        start_date: date,
        budget: Decimal,
        created_by: UUID,
        end_date: Optional[date] = None,
        superintendent: Optional[str] = None,
        project_manager: Optional[str] = None
    ) -> Project:
        """Create a new construction project"""
        self._project_counter += 1
        project_number = f"PRJ-{self._project_counter:03d}"
        
        now = datetime.utcnow()
        project = Project(
            id=uuid4(),
            name=name,
            description=description,
            client_name=client_name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            status=ProjectStatus.PLANNING,
            created_by=created_by,
            created_at=now,
            updated_at=now,
            project_number=project_number,
            superintendent=superintendent,
            project_manager=project_manager
        )
        
        self.projects[project.id] = project
        self._rfi_counters[project.id] = 0
        self._co_counters[project.id] = 0
        
        logger.info(f"Project created: {project_number} - {name}")
        return project
    
    async def update_project_status(
        self,
        project_id: UUID,
        new_status: ProjectStatus,
        updated_by: UUID
    ) -> Project:
        """Update project status"""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        project = self.projects[project_id]
        project.status = new_status
        project.updated_at = datetime.utcnow()
        
        logger.info(f"Project {project.project_number} status updated to {new_status.value}")
        return project
    
    async def get_projects(self, user_id: UUID) -> List[Project]:
        """
        Get all projects - ALPHABETICAL by name (Rule #5)
        NOT sorted by budget, progress, or activity
        """
        projects = list(self.projects.values())
        # RULE #5: ALPHABETICAL by name, NOT by budget/progress
        return sorted(projects, key=lambda p: p.name.lower())
    
    async def get_project(self, project_id: UUID) -> Optional[Project]:
        """Get project by ID"""
        return self.projects.get(project_id)
    
    # ========================================================================
    # RFI MANAGEMENT
    # ========================================================================
    
    async def create_rfi(
        self,
        project_id: UUID,
        subject: str,
        question: str,
        submitted_by: UUID,
        priority: TaskPriority = TaskPriority.MEDIUM,
        due_date: Optional[date] = None,
        assigned_to: Optional[UUID] = None
    ) -> RFI:
        """Create a new RFI (Request for Information)"""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        self._rfi_counters[project_id] += 1
        rfi_number = f"RFI-{self._rfi_counters[project_id]:03d}"
        
        rfi = RFI(
            id=uuid4(),
            project_id=project_id,
            rfi_number=rfi_number,
            subject=subject,
            question=question,
            response=None,
            status=RFIStatus.DRAFT,
            priority=priority,
            due_date=due_date,
            submitted_by=submitted_by,
            assigned_to=assigned_to,
            created_at=datetime.utcnow(),
            responded_at=None,
            closed_at=None
        )
        
        self.rfis[rfi.id] = rfi
        logger.info(f"RFI created: {rfi_number} - {subject}")
        return rfi
    
    async def submit_rfi(self, rfi_id: UUID, user_id: UUID) -> RFI:
        """Submit RFI for review"""
        if rfi_id not in self.rfis:
            raise ValueError(f"RFI not found: {rfi_id}")
        
        rfi = self.rfis[rfi_id]
        rfi.status = RFIStatus.SUBMITTED
        
        logger.info(f"RFI {rfi.rfi_number} submitted")
        return rfi
    
    async def respond_to_rfi(
        self,
        rfi_id: UUID,
        response: str,
        responder_id: UUID
    ) -> RFI:
        """Respond to an RFI"""
        if rfi_id not in self.rfis:
            raise ValueError(f"RFI not found: {rfi_id}")
        
        rfi = self.rfis[rfi_id]
        rfi.response = response
        rfi.status = RFIStatus.RESPONDED
        rfi.responded_at = datetime.utcnow()
        
        logger.info(f"RFI {rfi.rfi_number} responded")
        return rfi
    
    async def close_rfi(self, rfi_id: UUID, user_id: UUID) -> RFI:
        """Close an RFI"""
        if rfi_id not in self.rfis:
            raise ValueError(f"RFI not found: {rfi_id}")
        
        rfi = self.rfis[rfi_id]
        rfi.status = RFIStatus.CLOSED
        rfi.closed_at = datetime.utcnow()
        
        logger.info(f"RFI {rfi.rfi_number} closed")
        return rfi
    
    async def get_project_rfis(self, project_id: UUID) -> List[RFI]:
        """
        Get RFIs for project - CHRONOLOGICAL by created_at (Rule #5)
        NOT sorted by priority or status
        """
        rfis = [r for r in self.rfis.values() if r.project_id == project_id]
        # RULE #5: CHRONOLOGICAL, NOT by priority
        return sorted(rfis, key=lambda r: r.created_at, reverse=True)
    
    # ========================================================================
    # DAILY LOGS
    # ========================================================================
    
    async def create_daily_log(
        self,
        project_id: UUID,
        log_date: date,
        weather: WeatherCondition,
        workers_onsite: int,
        work_completed: str,
        created_by: UUID,
        temperature_high: Optional[int] = None,
        temperature_low: Optional[int] = None,
        equipment_used: Optional[List[str]] = None,
        delays: Optional[str] = None,
        safety_incidents: int = 0,
        notes: Optional[str] = None
    ) -> DailyLog:
        """Create a daily field log"""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        log = DailyLog(
            id=uuid4(),
            project_id=project_id,
            log_date=log_date,
            weather=weather,
            temperature_high=temperature_high,
            temperature_low=temperature_low,
            workers_onsite=workers_onsite,
            equipment_used=equipment_used or [],
            work_completed=work_completed,
            delays=delays,
            safety_incidents=safety_incidents,
            notes=notes,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.daily_logs[log.id] = log
        logger.info(f"Daily log created for {log_date}")
        return log
    
    async def get_project_daily_logs(self, project_id: UUID) -> List[DailyLog]:
        """
        Get daily logs for project - CHRONOLOGICAL by log_date (Rule #5)
        Newest first
        """
        logs = [l for l in self.daily_logs.values() if l.project_id == project_id]
        # RULE #5: CHRONOLOGICAL by date
        return sorted(logs, key=lambda l: l.log_date, reverse=True)
    
    # ========================================================================
    # PUNCH LIST MANAGEMENT
    # ========================================================================
    
    async def create_punch_item(
        self,
        project_id: UUID,
        location: str,
        description: str,
        trade: str,
        created_by: UUID,
        priority: TaskPriority = TaskPriority.MEDIUM,
        assigned_to: Optional[UUID] = None,
        due_date: Optional[date] = None
    ) -> PunchItem:
        """Create a punch list item"""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        item = PunchItem(
            id=uuid4(),
            project_id=project_id,
            location=location,
            description=description,
            trade=trade,
            status=PunchItemStatus.OPEN,
            priority=priority,
            assigned_to=assigned_to,
            due_date=due_date,
            created_by=created_by,
            created_at=datetime.utcnow(),
            completed_at=None,
            approved_by=None,
            approved_at=None
        )
        
        self.punch_items[item.id] = item
        logger.info(f"Punch item created: {location} - {description[:50]}")
        return item
    
    async def update_punch_item_status(
        self,
        item_id: UUID,
        new_status: PunchItemStatus,
        user_id: UUID
    ) -> PunchItem:
        """Update punch item status"""
        if item_id not in self.punch_items:
            raise ValueError(f"Punch item not found: {item_id}")
        
        item = self.punch_items[item_id]
        item.status = new_status
        
        if new_status == PunchItemStatus.READY_FOR_REVIEW:
            item.completed_at = datetime.utcnow()
        
        logger.info(f"Punch item status updated to {new_status.value}")
        return item
    
    async def approve_punch_item(
        self,
        item_id: UUID,
        approver_id: UUID
    ) -> PunchItem:
        """
        GOVERNANCE - Rule #1: Approve a punch list item
        Human must approve before item is closed
        """
        if item_id not in self.punch_items:
            raise ValueError(f"Punch item not found: {item_id}")
        
        item = self.punch_items[item_id]
        
        if item.status != PunchItemStatus.READY_FOR_REVIEW:
            raise ValueError("Item must be ready for review before approval")
        
        item.status = PunchItemStatus.APPROVED
        item.approved_by = approver_id
        item.approved_at = datetime.utcnow()
        
        logger.info(f"GOVERNANCE: Punch item approved by {approver_id}")
        return item
    
    async def get_project_punch_items(self, project_id: UUID) -> List[PunchItem]:
        """
        Get punch items for project - ALPHABETICAL by location (Rule #5)
        NOT sorted by priority or status
        """
        items = [i for i in self.punch_items.values() if i.project_id == project_id]
        # RULE #5: ALPHABETICAL by location
        return sorted(items, key=lambda i: i.location.lower())
    
    # ========================================================================
    # SAFETY INSPECTIONS (GOVERNANCE - Rule #1)
    # ========================================================================
    
    async def create_safety_inspection(
        self,
        project_id: UUID,
        inspection_type: str,
        inspector_name: str,
        inspection_date: date,
        created_by: UUID,
        findings: Optional[List[str]] = None,
        corrective_actions: Optional[List[str]] = None,
        notes: Optional[str] = None
    ) -> SafetyInspection:
        """Create a safety inspection record"""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        inspection = SafetyInspection(
            id=uuid4(),
            project_id=project_id,
            inspection_type=inspection_type,
            inspector_name=inspector_name,
            inspection_date=inspection_date,
            status=SafetyStatus.SCHEDULED,
            findings=findings or [],
            corrective_actions=corrective_actions or [],
            created_by=created_by,
            created_at=datetime.utcnow(),
            approved_by=None,
            approved_at=None,
            notes=notes
        )
        
        self.safety_inspections[inspection.id] = inspection
        logger.info(f"Safety inspection created: {inspection_type}")
        return inspection
    
    async def submit_inspection_for_approval(
        self,
        inspection_id: UUID,
        findings: List[str],
        corrective_actions: List[str],
        user_id: UUID
    ) -> SafetyInspection:
        """Submit inspection findings for approval"""
        if inspection_id not in self.safety_inspections:
            raise ValueError(f"Inspection not found: {inspection_id}")
        
        inspection = self.safety_inspections[inspection_id]
        inspection.findings = findings
        inspection.corrective_actions = corrective_actions
        inspection.status = SafetyStatus.PENDING_APPROVAL
        
        logger.info(f"Safety inspection submitted for approval")
        return inspection
    
    async def approve_safety_inspection(
        self,
        inspection_id: UUID,
        passed: bool,
        approver_id: UUID,
        notes: Optional[str] = None
    ) -> SafetyInspection:
        """
        GOVERNANCE - Rule #1: Approve or fail a safety inspection
        REQUIRES human approval before closing
        """
        if inspection_id not in self.safety_inspections:
            raise ValueError(f"Inspection not found: {inspection_id}")
        
        inspection = self.safety_inspections[inspection_id]
        
        if inspection.status != SafetyStatus.PENDING_APPROVAL:
            raise ValueError("Inspection must be pending approval")
        
        inspection.status = SafetyStatus.PASSED if passed else SafetyStatus.FAILED
        inspection.approved_by = approver_id
        inspection.approved_at = datetime.utcnow()
        if notes:
            inspection.notes = notes
        
        logger.info(f"GOVERNANCE: Safety inspection {'PASSED' if passed else 'FAILED'} by {approver_id}")
        return inspection
    
    async def get_project_safety_inspections(self, project_id: UUID) -> List[SafetyInspection]:
        """
        Get safety inspections for project - CHRONOLOGICAL (Rule #5)
        Newest first
        """
        inspections = [i for i in self.safety_inspections.values() 
                       if i.project_id == project_id]
        # RULE #5: CHRONOLOGICAL
        return sorted(inspections, key=lambda i: i.inspection_date, reverse=True)
    
    # ========================================================================
    # CHANGE ORDERS (GOVERNANCE - Rule #1)
    # ========================================================================
    
    async def create_change_order(
        self,
        project_id: UUID,
        title: str,
        description: str,
        reason: str,
        cost_impact: Decimal,
        schedule_impact_days: int,
        submitted_by: UUID
    ) -> ChangeOrder:
        """Create a change order"""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        self._co_counters[project_id] += 1
        co_number = f"CO-{self._co_counters[project_id]:03d}"
        
        co = ChangeOrder(
            id=uuid4(),
            project_id=project_id,
            co_number=co_number,
            title=title,
            description=description,
            reason=reason,
            cost_impact=cost_impact,
            schedule_impact_days=schedule_impact_days,
            status=ChangeOrderStatus.DRAFT,
            submitted_by=submitted_by,
            submitted_at=None,
            approved_by=None,
            approved_at=None,
            executed_at=None,
            created_at=datetime.utcnow()
        )
        
        self.change_orders[co.id] = co
        logger.info(f"Change order created: {co_number} - {title}")
        return co
    
    async def submit_change_order(self, co_id: UUID, user_id: UUID) -> ChangeOrder:
        """Submit change order for approval"""
        if co_id not in self.change_orders:
            raise ValueError(f"Change order not found: {co_id}")
        
        co = self.change_orders[co_id]
        co.status = ChangeOrderStatus.SUBMITTED
        co.submitted_at = datetime.utcnow()
        
        logger.info(f"Change order {co.co_number} submitted")
        return co
    
    async def approve_change_order(
        self,
        co_id: UUID,
        approved: bool,
        approver_id: UUID
    ) -> ChangeOrder:
        """
        GOVERNANCE - Rule #1: Approve or reject a change order
        REQUIRES human approval before execution
        """
        if co_id not in self.change_orders:
            raise ValueError(f"Change order not found: {co_id}")
        
        co = self.change_orders[co_id]
        
        if co.status != ChangeOrderStatus.SUBMITTED:
            raise ValueError("Change order must be submitted before approval")
        
        co.status = ChangeOrderStatus.APPROVED if approved else ChangeOrderStatus.REJECTED
        co.approved_by = approver_id
        co.approved_at = datetime.utcnow()
        
        logger.info(f"GOVERNANCE: Change order {co.co_number} {'APPROVED' if approved else 'REJECTED'} by {approver_id}")
        return co
    
    async def execute_change_order(self, co_id: UUID, user_id: UUID) -> ChangeOrder:
        """
        Execute an approved change order
        Can only be executed after GOVERNANCE approval
        """
        if co_id not in self.change_orders:
            raise ValueError(f"Change order not found: {co_id}")
        
        co = self.change_orders[co_id]
        
        if co.status != ChangeOrderStatus.APPROVED:
            raise ValueError("Change order must be approved before execution")
        
        co.status = ChangeOrderStatus.EXECUTED
        co.executed_at = datetime.utcnow()
        
        # Update project budget
        project = self.projects[co.project_id]
        project.budget += co.cost_impact
        project.updated_at = datetime.utcnow()
        
        logger.info(f"Change order {co.co_number} executed, project budget updated by {co.cost_impact}")
        return co
    
    async def get_project_change_orders(self, project_id: UUID) -> List[ChangeOrder]:
        """
        Get change orders for project - CHRONOLOGICAL by created_at (Rule #5)
        Newest first
        """
        cos = [c for c in self.change_orders.values() if c.project_id == project_id]
        # RULE #5: CHRONOLOGICAL
        return sorted(cos, key=lambda c: c.created_at, reverse=True)
    
    # ========================================================================
    # EQUIPMENT MANAGEMENT
    # ========================================================================
    
    async def add_equipment(
        self,
        name: str,
        equipment_type: str,
        daily_rate: Decimal,
        created_by: UUID,
        serial_number: Optional[str] = None,
        last_maintenance_date: Optional[date] = None,
        next_maintenance_date: Optional[date] = None
    ) -> Equipment:
        """Add equipment to inventory"""
        eq = Equipment(
            id=uuid4(),
            name=name,
            equipment_type=equipment_type,
            serial_number=serial_number,
            status=EquipmentStatus.AVAILABLE,
            current_project_id=None,
            daily_rate=daily_rate,
            last_maintenance_date=last_maintenance_date,
            next_maintenance_date=next_maintenance_date,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        self.equipment[eq.id] = eq
        logger.info(f"Equipment added: {name}")
        return eq
    
    async def assign_equipment_to_project(
        self,
        equipment_id: UUID,
        project_id: UUID,
        user_id: UUID
    ) -> Equipment:
        """Assign equipment to a project"""
        if equipment_id not in self.equipment:
            raise ValueError(f"Equipment not found: {equipment_id}")
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        eq = self.equipment[equipment_id]
        
        if eq.status != EquipmentStatus.AVAILABLE:
            raise ValueError(f"Equipment is not available: {eq.status.value}")
        
        eq.current_project_id = project_id
        eq.status = EquipmentStatus.IN_USE
        
        logger.info(f"Equipment {eq.name} assigned to project {project_id}")
        return eq
    
    async def release_equipment(self, equipment_id: UUID, user_id: UUID) -> Equipment:
        """Release equipment from project"""
        if equipment_id not in self.equipment:
            raise ValueError(f"Equipment not found: {equipment_id}")
        
        eq = self.equipment[equipment_id]
        eq.current_project_id = None
        eq.status = EquipmentStatus.AVAILABLE
        
        logger.info(f"Equipment {eq.name} released")
        return eq
    
    async def get_equipment(self) -> List[Equipment]:
        """
        Get all equipment - ALPHABETICAL by name (Rule #5)
        NOT sorted by utilization or rate
        """
        equipment_list = list(self.equipment.values())
        # RULE #5: ALPHABETICAL by name
        return sorted(equipment_list, key=lambda e: e.name.lower())
    
    # ========================================================================
    # SUBCONTRACTOR MANAGEMENT
    # ========================================================================
    
    async def add_subcontractor(
        self,
        company_name: str,
        contact_name: str,
        email: str,
        phone: str,
        trade: str,
        created_by: UUID,
        license_number: Optional[str] = None,
        insurance_expiry: Optional[date] = None,
        notes: Optional[str] = None
    ) -> Subcontractor:
        """Add a subcontractor"""
        sub = Subcontractor(
            id=uuid4(),
            company_name=company_name,
            contact_name=contact_name,
            email=email,
            phone=phone,
            trade=trade,
            license_number=license_number,
            insurance_expiry=insurance_expiry,
            created_by=created_by,
            created_at=datetime.utcnow(),
            notes=notes
        )
        
        self.subcontractors[sub.id] = sub
        logger.info(f"Subcontractor added: {company_name}")
        return sub
    
    async def get_subcontractors(self) -> List[Subcontractor]:
        """
        Get all subcontractors - ALPHABETICAL by company name (Rule #5)
        NOT sorted by rating, reliability score, or past performance
        """
        subs = list(self.subcontractors.values())
        # RULE #5: ALPHABETICAL by company name, NOT by rating
        return sorted(subs, key=lambda s: s.company_name.lower())
    
    async def get_subcontractors_by_trade(self, trade: str) -> List[Subcontractor]:
        """
        Get subcontractors by trade - ALPHABETICAL (Rule #5)
        """
        subs = [s for s in self.subcontractors.values() 
                if s.trade.lower() == trade.lower()]
        # RULE #5: ALPHABETICAL
        return sorted(subs, key=lambda s: s.company_name.lower())
    
    # ========================================================================
    # TASK MANAGEMENT
    # ========================================================================
    
    async def create_task(
        self,
        project_id: UUID,
        title: str,
        description: str,
        due_date: date,
        created_by: UUID,
        priority: TaskPriority = TaskPriority.MEDIUM,
        assigned_to: Optional[UUID] = None
    ) -> Task:
        """Create a project task"""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        task = Task(
            id=uuid4(),
            project_id=project_id,
            title=title,
            description=description,
            assigned_to=assigned_to,
            priority=priority,
            status=TaskStatus.TODO,
            due_date=due_date,
            created_by=created_by,
            created_at=datetime.utcnow(),
            completed_at=None
        )
        
        self.tasks[task.id] = task
        logger.info(f"Task created: {title}")
        return task
    
    async def complete_task(self, task_id: UUID, user_id: UUID) -> Task:
        """Mark a task as completed"""
        if task_id not in self.tasks:
            raise ValueError(f"Task not found: {task_id}")
        
        task = self.tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        
        logger.info(f"Task completed: {task.title}")
        return task
    
    async def get_project_tasks(self, project_id: UUID) -> List[Task]:
        """
        Get tasks for project - CHRONOLOGICAL by due_date (Rule #5)
        Earliest due first (natural order for tasks)
        """
        tasks = [t for t in self.tasks.values() if t.project_id == project_id]
        # RULE #5: CHRONOLOGICAL by due date
        return sorted(tasks, key=lambda t: t.due_date)
    
    # ========================================================================
    # ANALYTICS
    # ========================================================================
    
    async def get_project_summary(self, project_id: UUID) -> Dict[str, Any]:
        """Get project summary statistics"""
        if project_id not in self.projects:
            raise ValueError(f"Project not found: {project_id}")
        
        project = self.projects[project_id]
        
        rfis = [r for r in self.rfis.values() if r.project_id == project_id]
        punch_items = [p for p in self.punch_items.values() if p.project_id == project_id]
        inspections = [i for i in self.safety_inspections.values() if i.project_id == project_id]
        change_orders = [c for c in self.change_orders.values() if c.project_id == project_id]
        tasks = [t for t in self.tasks.values() if t.project_id == project_id]
        logs = [l for l in self.daily_logs.values() if l.project_id == project_id]
        
        # Calculate totals
        total_co_cost = sum(c.cost_impact for c in change_orders 
                           if c.status == ChangeOrderStatus.EXECUTED)
        
        open_rfis = len([r for r in rfis if r.status not in 
                        [RFIStatus.CLOSED, RFIStatus.RESPONDED]])
        open_punch = len([p for p in punch_items if p.status != PunchItemStatus.APPROVED])
        pending_inspections = len([i for i in inspections 
                                   if i.status == SafetyStatus.PENDING_APPROVAL])
        
        return {
            "project": {
                "id": str(project.id),
                "name": project.name,
                "number": project.project_number,
                "status": project.status.value,
                "budget": float(project.budget),
                "adjusted_budget": float(project.budget),  # Already includes COs
            },
            "counts": {
                "total_rfis": len(rfis),
                "open_rfis": open_rfis,
                "total_punch_items": len(punch_items),
                "open_punch_items": open_punch,
                "total_inspections": len(inspections),
                "pending_inspections": pending_inspections,
                "total_change_orders": len(change_orders),
                "total_tasks": len(tasks),
                "completed_tasks": len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
                "total_daily_logs": len(logs),
            },
            "financials": {
                "original_budget": float(project.budget - total_co_cost),
                "change_order_total": float(total_co_cost),
                "current_budget": float(project.budget),
            },
            "safety": {
                "total_incidents": sum(l.safety_incidents for l in logs),
                "passed_inspections": len([i for i in inspections 
                                           if i.status == SafetyStatus.PASSED]),
                "failed_inspections": len([i for i in inspections 
                                           if i.status == SafetyStatus.FAILED]),
            }
        }


# Singleton instance
_construction_agent: Optional[ConstructionAgent] = None


def get_construction_agent() -> ConstructionAgent:
    """Get or create construction agent singleton"""
    global _construction_agent
    if _construction_agent is None:
        _construction_agent = ConstructionAgent()
    return _construction_agent
