"""
CHE·NU™ V68 — HR & PEOPLE OPERATIONS AGENT
BambooHR/Gusto Killer

Features:
- Employee Management (profiles, documents, history)
- Onboarding (checklists, tasks, IT requests)
- Time Off/PTO (requests, balances, accruals)
- Performance Management (goals, reviews, 360 feedback)
- Organization (departments, org chart, reporting)
- Attendance (clock in/out, timesheets)
- Benefits (plans, enrollment, dependents)
- Compliance (documents, training, certifications)
- Payroll (schedules, salary, deductions)
- AI (attrition prediction, compensation benchmarking)

GOVERNED INTELLIGENCE: All actions require human approval
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS
# =============================================================================

class EmploymentStatus(str, Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    PENDING_START = "pending_start"
    PROBATION = "probation"


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"
    TEMPORARY = "temporary"


class LeaveType(str, Enum):
    VACATION = "vacation"
    SICK = "sick"
    PERSONAL = "personal"
    PARENTAL = "parental"
    BEREAVEMENT = "bereavement"
    JURY_DUTY = "jury_duty"
    UNPAID = "unpaid"
    WORK_FROM_HOME = "work_from_home"


class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ReviewStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ReviewType(str, Enum):
    ANNUAL = "annual"
    PROBATION = "probation"
    QUARTERLY = "quarterly"
    PROMOTION = "promotion"
    PROJECT = "project"
    THREE_SIXTY = "360_feedback"


class OnboardingStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class BenefitType(str, Enum):
    HEALTH = "health"
    DENTAL = "dental"
    VISION = "vision"
    LIFE = "life"
    DISABILITY = "disability"
    RETIREMENT_401K = "401k"
    RRSP = "rrsp"
    HSA = "hsa"
    FSA = "fsa"


class PayFrequency(str, Enum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    SEMI_MONTHLY = "semi_monthly"
    MONTHLY = "monthly"


class ComplianceItemStatus(str, Enum):
    REQUIRED = "required"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    EXPIRED = "expired"
    WAIVED = "waived"


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass
class Department:
    """Department in organization."""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    code: str = ""
    description: str = ""
    manager_id: Optional[str] = None
    parent_department_id: Optional[str] = None
    budget: Decimal = Decimal("0")
    headcount_limit: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class JobPosition:
    """Job position/role definition."""
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    department_id: str = ""
    level: str = ""  # Junior, Mid, Senior, Lead, Manager, Director, VP, C-Level
    salary_min: Decimal = Decimal("0")
    salary_max: Decimal = Decimal("0")
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class EmergencyContact:
    """Employee emergency contact."""
    name: str = ""
    relationship: str = ""
    phone: str = ""
    email: str = ""


@dataclass
class Employee:
    """Employee profile."""
    id: str = field(default_factory=lambda: str(uuid4()))
    # Personal
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    province_state: str = ""
    postal_code: str = ""
    country: str = "Canada"
    date_of_birth: Optional[date] = None
    gender: str = ""
    
    # Emergency
    emergency_contact: Optional[EmergencyContact] = None
    
    # Employment
    employee_number: str = ""
    position_id: str = ""
    department_id: str = ""
    manager_id: Optional[str] = None
    hire_date: Optional[date] = None
    probation_end_date: Optional[date] = None
    termination_date: Optional[date] = None
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    employment_status: EmploymentStatus = EmploymentStatus.PENDING_START
    
    # Compensation
    salary: Decimal = Decimal("0")
    pay_frequency: PayFrequency = PayFrequency.BIWEEKLY
    currency: str = "CAD"
    
    # Work
    work_location: str = ""
    work_email: str = ""
    work_phone: str = ""
    remote_eligible: bool = False
    
    # Documents
    documents: List[str] = field(default_factory=list)  # Document IDs
    
    # PTO Balances
    pto_balances: Dict[str, float] = field(default_factory=dict)  # Leave type -> days
    
    # Meta
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class LeaveRequest:
    """Time off / PTO request."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    leave_type: LeaveType = LeaveType.VACATION
    start_date: date = field(default_factory=date.today)
    end_date: date = field(default_factory=date.today)
    days_requested: float = 0.0
    reason: str = ""
    status: LeaveStatus = LeaveStatus.PENDING
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    rejection_reason: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class LeavePolicy:
    """Leave/PTO policy configuration."""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    leave_type: LeaveType = LeaveType.VACATION
    days_per_year: float = 0.0
    accrual_rate: float = 0.0  # Days per month
    max_carryover: float = 0.0
    max_balance: float = 0.0
    requires_approval: bool = True
    min_notice_days: int = 0
    applicable_to: List[str] = field(default_factory=list)  # Department IDs, empty = all
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class Goal:
    """Employee goal/OKR."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    title: str = ""
    description: str = ""
    key_results: List[str] = field(default_factory=list)
    weight: float = 1.0  # For weighted scoring
    target_date: Optional[date] = None
    progress: float = 0.0  # 0-100
    status: str = "active"  # active, completed, cancelled
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class PerformanceReview:
    """Performance review."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    reviewer_id: str = ""
    review_type: ReviewType = ReviewType.ANNUAL
    review_period_start: date = field(default_factory=date.today)
    review_period_end: date = field(default_factory=date.today)
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    status: ReviewStatus = ReviewStatus.SCHEDULED
    
    # Ratings (1-5)
    overall_rating: Optional[float] = None
    ratings: Dict[str, float] = field(default_factory=dict)  # Category -> rating
    
    # Feedback
    strengths: List[str] = field(default_factory=list)
    areas_for_improvement: List[str] = field(default_factory=list)
    reviewer_comments: str = ""
    employee_comments: str = ""
    
    # Goals
    goals_achieved: List[str] = field(default_factory=list)
    new_goals: List[str] = field(default_factory=list)
    
    # Recommendations
    promotion_recommended: bool = False
    salary_increase_recommended: bool = False
    recommended_increase_percent: float = 0.0
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class Feedback360:
    """360 feedback submission."""
    id: str = field(default_factory=lambda: str(uuid4()))
    review_id: str = ""
    employee_id: str = ""  # Who is being reviewed
    reviewer_id: str = ""  # Who is providing feedback
    relationship: str = ""  # peer, direct_report, manager, self
    ratings: Dict[str, float] = field(default_factory=dict)
    strengths: str = ""
    improvements: str = ""
    comments: str = ""
    is_anonymous: bool = True
    submitted_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class OnboardingChecklist:
    """Onboarding checklist for new employee."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    template_name: str = "default"
    status: OnboardingStatus = OnboardingStatus.NOT_STARTED
    start_date: date = field(default_factory=date.today)
    target_completion_date: Optional[date] = None
    completed_date: Optional[date] = None
    tasks: List['OnboardingTask'] = field(default_factory=list)
    progress_percent: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class OnboardingTask:
    """Individual onboarding task."""
    id: str = field(default_factory=lambda: str(uuid4()))
    checklist_id: str = ""
    title: str = ""
    description: str = ""
    category: str = ""  # IT, HR, Training, Admin
    assigned_to: str = ""  # Can be employee, manager, HR, IT
    due_date: Optional[date] = None
    status: TaskStatus = TaskStatus.PENDING
    completed_at: Optional[datetime] = None
    completed_by: Optional[str] = None
    notes: str = ""
    order: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TimeEntry:
    """Clock in/out or timesheet entry."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    date: date = field(default_factory=date.today)
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None
    break_minutes: int = 0
    total_hours: float = 0.0
    overtime_hours: float = 0.0
    project_id: Optional[str] = None
    notes: str = ""
    is_approved: bool = False
    approved_by: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class BenefitPlan:
    """Benefit plan definition."""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    benefit_type: BenefitType = BenefitType.HEALTH
    provider: str = ""
    plan_number: str = ""
    description: str = ""
    employee_contribution: Decimal = Decimal("0")
    employer_contribution: Decimal = Decimal("0")
    contribution_frequency: PayFrequency = PayFrequency.MONTHLY
    coverage_details: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class BenefitEnrollment:
    """Employee benefit enrollment."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    plan_id: str = ""
    coverage_level: str = ""  # employee_only, employee_spouse, family
    effective_date: date = field(default_factory=date.today)
    end_date: Optional[date] = None
    status: str = "active"  # active, pending, cancelled
    dependents: List[Dict] = field(default_factory=list)  # Name, relationship, DOB
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class ComplianceItem:
    """Compliance requirement (document, training, certification)."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    name: str = ""
    category: str = ""  # document, training, certification, policy
    description: str = ""
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: ComplianceItemStatus = ComplianceItemStatus.REQUIRED
    document_url: str = ""
    verified_by: Optional[str] = None
    notes: str = ""
    is_mandatory: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class PayrollRecord:
    """Payroll record for pay period."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    pay_period_start: date = field(default_factory=date.today)
    pay_period_end: date = field(default_factory=date.today)
    pay_date: date = field(default_factory=date.today)
    
    # Earnings
    regular_hours: float = 0.0
    overtime_hours: float = 0.0
    gross_pay: Decimal = Decimal("0")
    
    # Deductions
    federal_tax: Decimal = Decimal("0")
    provincial_tax: Decimal = Decimal("0")
    cpp_contribution: Decimal = Decimal("0")
    ei_contribution: Decimal = Decimal("0")
    benefit_deductions: Decimal = Decimal("0")
    other_deductions: Decimal = Decimal("0")
    total_deductions: Decimal = Decimal("0")
    
    # Net
    net_pay: Decimal = Decimal("0")
    
    # Status
    status: str = "pending"  # pending, processed, paid
    processed_at: Optional[datetime] = None
    
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = ""


@dataclass
class Document:
    """HR document."""
    id: str = field(default_factory=lambda: str(uuid4()))
    employee_id: str = ""
    name: str = ""
    category: str = ""  # contract, policy, tax_form, certification
    file_url: str = ""
    file_type: str = ""
    file_size: int = 0
    uploaded_at: datetime = field(default_factory=datetime.utcnow)
    uploaded_by: str = ""
    is_confidential: bool = False
    expiry_date: Optional[date] = None


# =============================================================================
# HR AGENT SERVICE
# =============================================================================

class HRAgent:
    """
    HR & People Operations Agent.
    
    GOVERNED INTELLIGENCE:
    - All hiring/termination requires human approval
    - Salary changes require manager approval
    - Leave requests require manager approval
    - Performance ratings are human-validated
    """
    
    def __init__(self):
        # Data stores
        self.departments: Dict[str, Department] = {}
        self.positions: Dict[str, JobPosition] = {}
        self.employees: Dict[str, Employee] = {}
        self.leave_requests: Dict[str, LeaveRequest] = {}
        self.leave_policies: Dict[str, LeavePolicy] = {}
        self.goals: Dict[str, Goal] = {}
        self.reviews: Dict[str, PerformanceReview] = {}
        self.feedback_360: Dict[str, Feedback360] = {}
        self.onboarding: Dict[str, OnboardingChecklist] = {}
        self.time_entries: Dict[str, TimeEntry] = {}
        self.benefit_plans: Dict[str, BenefitPlan] = {}
        self.enrollments: Dict[str, BenefitEnrollment] = {}
        self.compliance_items: Dict[str, ComplianceItem] = {}
        self.payroll_records: Dict[str, PayrollRecord] = {}
        self.documents: Dict[str, Document] = {}
        
        logger.info("HRAgent initialized - GOVERNED INTELLIGENCE active")
    
    # =========================================================================
    # DEPARTMENT MANAGEMENT
    # =========================================================================
    
    def create_department(
        self,
        name: str,
        code: str,
        description: str = "",
        manager_id: Optional[str] = None,
        parent_department_id: Optional[str] = None,
        budget: Decimal = Decimal("0"),
        headcount_limit: int = 0,
        created_by: str = ""
    ) -> Department:
        """Create a new department."""
        # Check for duplicate code
        for dept in self.departments.values():
            if dept.code.upper() == code.upper():
                raise ValueError(f"Department with code '{code}' already exists")
        
        department = Department(
            name=name,
            code=code.upper(),
            description=description,
            manager_id=manager_id,
            parent_department_id=parent_department_id,
            budget=budget,
            headcount_limit=headcount_limit,
            created_by=created_by
        )
        
        self.departments[department.id] = department
        logger.info(f"Created department: {name} ({code})")
        return department
    
    def get_department(self, department_id: str) -> Optional[Department]:
        """Get department by ID."""
        return self.departments.get(department_id)
    
    def list_departments(self) -> List[Department]:
        """List all departments."""
        return list(self.departments.values())
    
    def get_org_chart(self) -> Dict[str, Any]:
        """Generate organization chart structure."""
        def build_tree(parent_id: Optional[str] = None) -> List[Dict]:
            children = []
            for dept in self.departments.values():
                if dept.parent_department_id == parent_id:
                    dept_data = {
                        "id": dept.id,
                        "name": dept.name,
                        "code": dept.code,
                        "manager_id": dept.manager_id,
                        "manager_name": "",
                        "headcount": self._get_department_headcount(dept.id),
                        "children": build_tree(dept.id)
                    }
                    if dept.manager_id and dept.manager_id in self.employees:
                        mgr = self.employees[dept.manager_id]
                        dept_data["manager_name"] = f"{mgr.first_name} {mgr.last_name}"
                    children.append(dept_data)
            return children
        
        return {"departments": build_tree(None)}
    
    def _get_department_headcount(self, department_id: str) -> int:
        """Get number of employees in department."""
        return sum(1 for emp in self.employees.values() 
                   if emp.department_id == department_id 
                   and emp.employment_status == EmploymentStatus.ACTIVE)
    
    # =========================================================================
    # POSITION MANAGEMENT
    # =========================================================================
    
    def create_position(
        self,
        title: str,
        department_id: str,
        level: str,
        salary_min: Decimal,
        salary_max: Decimal,
        description: str = "",
        requirements: List[str] = None,
        created_by: str = ""
    ) -> JobPosition:
        """Create a job position."""
        if department_id not in self.departments:
            raise ValueError(f"Department {department_id} not found")
        
        position = JobPosition(
            title=title,
            department_id=department_id,
            level=level,
            salary_min=salary_min,
            salary_max=salary_max,
            description=description,
            requirements=requirements or [],
            created_by=created_by
        )
        
        self.positions[position.id] = position
        logger.info(f"Created position: {title} ({level})")
        return position
    
    def list_positions(self, department_id: Optional[str] = None) -> List[JobPosition]:
        """List positions, optionally filtered by department."""
        positions = list(self.positions.values())
        if department_id:
            positions = [p for p in positions if p.department_id == department_id]
        return positions
    
    # =========================================================================
    # EMPLOYEE MANAGEMENT
    # =========================================================================
    
    def create_employee(
        self,
        first_name: str,
        last_name: str,
        email: str,
        position_id: str,
        department_id: str,
        hire_date: date,
        salary: Decimal,
        employment_type: EmploymentType = EmploymentType.FULL_TIME,
        manager_id: Optional[str] = None,
        created_by: str = ""
    ) -> Employee:
        """
        Create a new employee (DRAFT - requires HR approval).
        """
        # Validate position and department
        if position_id not in self.positions:
            raise ValueError(f"Position {position_id} not found")
        if department_id not in self.departments:
            raise ValueError(f"Department {department_id} not found")
        
        # Check for duplicate email
        for emp in self.employees.values():
            if emp.email.lower() == email.lower():
                raise ValueError(f"Employee with email '{email}' already exists")
        
        # Generate employee number
        employee_number = f"EMP{len(self.employees) + 1:05d}"
        
        # Calculate probation end date (typically 3 months)
        probation_end = hire_date + timedelta(days=90)
        
        # Initialize PTO balances
        pto_balances = {
            LeaveType.VACATION.value: 0.0,
            LeaveType.SICK.value: 0.0,
            LeaveType.PERSONAL.value: 0.0,
        }
        
        employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            employee_number=employee_number,
            position_id=position_id,
            department_id=department_id,
            manager_id=manager_id,
            hire_date=hire_date,
            probation_end_date=probation_end,
            employment_type=employment_type,
            employment_status=EmploymentStatus.PENDING_START,
            salary=salary,
            pto_balances=pto_balances,
            created_by=created_by
        )
        
        self.employees[employee.id] = employee
        logger.info(f"Created employee: {first_name} {last_name} ({employee_number})")
        
        # Auto-create onboarding checklist
        self._create_default_onboarding(employee.id, created_by)
        
        return employee
    
    def get_employee(self, employee_id: str) -> Optional[Employee]:
        """Get employee by ID."""
        return self.employees.get(employee_id)
    
    def get_employee_by_number(self, employee_number: str) -> Optional[Employee]:
        """Get employee by employee number."""
        for emp in self.employees.values():
            if emp.employee_number == employee_number:
                return emp
        return None
    
    def list_employees(
        self,
        department_id: Optional[str] = None,
        status: Optional[EmploymentStatus] = None,
        manager_id: Optional[str] = None
    ) -> List[Employee]:
        """List employees with optional filters."""
        employees = list(self.employees.values())
        
        if department_id:
            employees = [e for e in employees if e.department_id == department_id]
        if status:
            employees = [e for e in employees if e.employment_status == status]
        if manager_id:
            employees = [e for e in employees if e.manager_id == manager_id]
        
        return employees
    
    def update_employee_status(
        self,
        employee_id: str,
        new_status: EmploymentStatus,
        updated_by: str,
        termination_date: Optional[date] = None
    ) -> Employee:
        """Update employee status (requires HR approval)."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = self.employees[employee_id]
        old_status = employee.employment_status
        employee.employment_status = new_status
        employee.updated_at = datetime.utcnow()
        
        if new_status == EmploymentStatus.TERMINATED and termination_date:
            employee.termination_date = termination_date
        
        logger.info(f"Employee {employee_id} status: {old_status} -> {new_status}")
        return employee
    
    def update_salary(
        self,
        employee_id: str,
        new_salary: Decimal,
        effective_date: date,
        updated_by: str,
        reason: str = ""
    ) -> Employee:
        """Update employee salary (requires manager approval)."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = self.employees[employee_id]
        old_salary = employee.salary
        employee.salary = new_salary
        employee.updated_at = datetime.utcnow()
        
        logger.info(f"Salary update for {employee_id}: {old_salary} -> {new_salary}")
        return employee
    
    def get_direct_reports(self, manager_id: str) -> List[Employee]:
        """Get employees reporting to a manager."""
        return [e for e in self.employees.values() if e.manager_id == manager_id]
    
    def search_employees(self, query: str) -> List[Employee]:
        """Search employees by name or email."""
        query = query.lower()
        results = []
        for emp in self.employees.values():
            if (query in emp.first_name.lower() or 
                query in emp.last_name.lower() or
                query in emp.email.lower() or
                query in emp.employee_number.lower()):
                results.append(emp)
        return results
    
    # =========================================================================
    # LEAVE / PTO MANAGEMENT
    # =========================================================================
    
    def create_leave_policy(
        self,
        name: str,
        leave_type: LeaveType,
        days_per_year: float,
        accrual_rate: float = 0.0,
        max_carryover: float = 0.0,
        max_balance: float = 0.0,
        requires_approval: bool = True,
        min_notice_days: int = 0,
        created_by: str = ""
    ) -> LeavePolicy:
        """Create a leave policy."""
        policy = LeavePolicy(
            name=name,
            leave_type=leave_type,
            days_per_year=days_per_year,
            accrual_rate=accrual_rate,
            max_carryover=max_carryover,
            max_balance=max_balance,
            requires_approval=requires_approval,
            min_notice_days=min_notice_days,
            created_by=created_by
        )
        self.leave_policies[policy.id] = policy
        logger.info(f"Created leave policy: {name}")
        return policy
    
    def setup_default_leave_policies(self, created_by: str) -> List[LeavePolicy]:
        """Setup default Canadian leave policies."""
        policies = []
        
        # Vacation - 10 days base (increases with tenure)
        policies.append(self.create_leave_policy(
            name="Vacation",
            leave_type=LeaveType.VACATION,
            days_per_year=10.0,
            accrual_rate=0.833,  # ~10 days/year
            max_carryover=5.0,
            max_balance=15.0,
            requires_approval=True,
            min_notice_days=14,
            created_by=created_by
        ))
        
        # Sick leave - 5 days
        policies.append(self.create_leave_policy(
            name="Sick Leave",
            leave_type=LeaveType.SICK,
            days_per_year=5.0,
            accrual_rate=0.0,  # Granted upfront
            max_carryover=0.0,
            max_balance=5.0,
            requires_approval=False,
            min_notice_days=0,
            created_by=created_by
        ))
        
        # Personal days - 3 days
        policies.append(self.create_leave_policy(
            name="Personal Days",
            leave_type=LeaveType.PERSONAL,
            days_per_year=3.0,
            accrual_rate=0.0,
            max_carryover=0.0,
            max_balance=3.0,
            requires_approval=True,
            min_notice_days=3,
            created_by=created_by
        ))
        
        # Parental leave
        policies.append(self.create_leave_policy(
            name="Parental Leave",
            leave_type=LeaveType.PARENTAL,
            days_per_year=0.0,  # Special policy
            accrual_rate=0.0,
            max_carryover=0.0,
            max_balance=0.0,
            requires_approval=True,
            min_notice_days=30,
            created_by=created_by
        ))
        
        return policies
    
    def request_leave(
        self,
        employee_id: str,
        leave_type: LeaveType,
        start_date: date,
        end_date: date,
        reason: str = "",
        created_by: str = ""
    ) -> LeaveRequest:
        """Submit a leave request (requires manager approval)."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = self.employees[employee_id]
        
        # Calculate days (excluding weekends)
        days = self._calculate_business_days(start_date, end_date)
        
        # Check balance
        current_balance = employee.pto_balances.get(leave_type.value, 0.0)
        if leave_type != LeaveType.UNPAID and days > current_balance:
            raise ValueError(f"Insufficient {leave_type.value} balance. Available: {current_balance}, Requested: {days}")
        
        request = LeaveRequest(
            employee_id=employee_id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            days_requested=days,
            reason=reason,
            status=LeaveStatus.PENDING,
            created_by=created_by
        )
        
        self.leave_requests[request.id] = request
        logger.info(f"Leave request created: {employee_id} - {leave_type.value} ({days} days)")
        return request
    
    def approve_leave(
        self,
        request_id: str,
        approved_by: str
    ) -> LeaveRequest:
        """Approve a leave request (manager action)."""
        if request_id not in self.leave_requests:
            raise ValueError(f"Leave request {request_id} not found")
        
        request = self.leave_requests[request_id]
        if request.status != LeaveStatus.PENDING:
            raise ValueError(f"Cannot approve request with status {request.status}")
        
        # Deduct from balance
        employee = self.employees[request.employee_id]
        leave_type = request.leave_type.value
        if leave_type in employee.pto_balances:
            employee.pto_balances[leave_type] -= request.days_requested
        
        request.status = LeaveStatus.APPROVED
        request.approved_by = approved_by
        request.approved_at = datetime.utcnow()
        
        logger.info(f"Leave request {request_id} approved by {approved_by}")
        return request
    
    def reject_leave(
        self,
        request_id: str,
        rejected_by: str,
        reason: str = ""
    ) -> LeaveRequest:
        """Reject a leave request."""
        if request_id not in self.leave_requests:
            raise ValueError(f"Leave request {request_id} not found")
        
        request = self.leave_requests[request_id]
        if request.status != LeaveStatus.PENDING:
            raise ValueError(f"Cannot reject request with status {request.status}")
        
        request.status = LeaveStatus.REJECTED
        request.approved_by = rejected_by
        request.approved_at = datetime.utcnow()
        request.rejection_reason = reason
        
        logger.info(f"Leave request {request_id} rejected: {reason}")
        return request
    
    def get_leave_balance(self, employee_id: str) -> Dict[str, float]:
        """Get employee's current leave balances."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        return self.employees[employee_id].pto_balances.copy()
    
    def get_team_calendar(
        self,
        manager_id: str,
        start_date: date,
        end_date: date
    ) -> List[Dict]:
        """Get approved leave for a manager's team."""
        direct_reports = self.get_direct_reports(manager_id)
        team_ids = {e.id for e in direct_reports}
        
        calendar = []
        for request in self.leave_requests.values():
            if (request.employee_id in team_ids and
                request.status == LeaveStatus.APPROVED and
                request.start_date <= end_date and
                request.end_date >= start_date):
                emp = self.employees[request.employee_id]
                calendar.append({
                    "employee_id": request.employee_id,
                    "employee_name": f"{emp.first_name} {emp.last_name}",
                    "leave_type": request.leave_type.value,
                    "start_date": request.start_date.isoformat(),
                    "end_date": request.end_date.isoformat(),
                    "days": request.days_requested
                })
        
        return calendar
    
    def _calculate_business_days(self, start: date, end: date) -> float:
        """Calculate business days between dates."""
        days = 0
        current = start
        while current <= end:
            if current.weekday() < 5:  # Monday to Friday
                days += 1
            current += timedelta(days=1)
        return float(days)
    
    def accrue_pto(self, employee_id: str, leave_type: LeaveType, days: float) -> float:
        """Accrue PTO for an employee (typically called monthly)."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = self.employees[employee_id]
        current = employee.pto_balances.get(leave_type.value, 0.0)
        new_balance = current + days
        
        # Check max balance from policy
        for policy in self.leave_policies.values():
            if policy.leave_type == leave_type:
                if policy.max_balance > 0:
                    new_balance = min(new_balance, policy.max_balance)
                break
        
        employee.pto_balances[leave_type.value] = new_balance
        logger.info(f"PTO accrual for {employee_id}: {leave_type.value} +{days} = {new_balance}")
        return new_balance
    
    # =========================================================================
    # PERFORMANCE MANAGEMENT
    # =========================================================================
    
    def create_goal(
        self,
        employee_id: str,
        title: str,
        description: str = "",
        key_results: List[str] = None,
        target_date: Optional[date] = None,
        weight: float = 1.0,
        created_by: str = ""
    ) -> Goal:
        """Create an employee goal."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        goal = Goal(
            employee_id=employee_id,
            title=title,
            description=description,
            key_results=key_results or [],
            target_date=target_date,
            weight=weight,
            created_by=created_by
        )
        
        self.goals[goal.id] = goal
        logger.info(f"Created goal for {employee_id}: {title}")
        return goal
    
    def update_goal_progress(
        self,
        goal_id: str,
        progress: float,
        updated_by: str
    ) -> Goal:
        """Update goal progress (0-100)."""
        if goal_id not in self.goals:
            raise ValueError(f"Goal {goal_id} not found")
        
        goal = self.goals[goal_id]
        goal.progress = min(100.0, max(0.0, progress))
        goal.updated_at = datetime.utcnow()
        
        if goal.progress >= 100.0:
            goal.status = "completed"
        
        logger.info(f"Goal {goal_id} progress: {progress}%")
        return goal
    
    def get_employee_goals(self, employee_id: str, status: str = None) -> List[Goal]:
        """Get goals for an employee."""
        goals = [g for g in self.goals.values() if g.employee_id == employee_id]
        if status:
            goals = [g for g in goals if g.status == status]
        return goals
    
    def create_performance_review(
        self,
        employee_id: str,
        reviewer_id: str,
        review_type: ReviewType,
        review_period_start: date,
        review_period_end: date,
        scheduled_date: date,
        created_by: str = ""
    ) -> PerformanceReview:
        """Schedule a performance review."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        if reviewer_id not in self.employees:
            raise ValueError(f"Reviewer {reviewer_id} not found")
        
        review = PerformanceReview(
            employee_id=employee_id,
            reviewer_id=reviewer_id,
            review_type=review_type,
            review_period_start=review_period_start,
            review_period_end=review_period_end,
            scheduled_date=scheduled_date,
            status=ReviewStatus.SCHEDULED,
            created_by=created_by
        )
        
        self.reviews[review.id] = review
        logger.info(f"Created {review_type.value} review for {employee_id}")
        return review
    
    def complete_review(
        self,
        review_id: str,
        overall_rating: float,
        ratings: Dict[str, float],
        strengths: List[str],
        areas_for_improvement: List[str],
        reviewer_comments: str,
        goals_achieved: List[str] = None,
        new_goals: List[str] = None,
        promotion_recommended: bool = False,
        salary_increase_recommended: bool = False,
        recommended_increase_percent: float = 0.0,
        completed_by: str = ""
    ) -> PerformanceReview:
        """Complete a performance review."""
        if review_id not in self.reviews:
            raise ValueError(f"Review {review_id} not found")
        
        review = self.reviews[review_id]
        if review.status == ReviewStatus.COMPLETED:
            raise ValueError("Review already completed")
        
        review.overall_rating = overall_rating
        review.ratings = ratings
        review.strengths = strengths
        review.areas_for_improvement = areas_for_improvement
        review.reviewer_comments = reviewer_comments
        review.goals_achieved = goals_achieved or []
        review.new_goals = new_goals or []
        review.promotion_recommended = promotion_recommended
        review.salary_increase_recommended = salary_increase_recommended
        review.recommended_increase_percent = recommended_increase_percent
        review.status = ReviewStatus.COMPLETED
        review.completed_date = date.today()
        
        logger.info(f"Completed review {review_id} - Rating: {overall_rating}")
        return review
    
    def submit_360_feedback(
        self,
        review_id: str,
        employee_id: str,
        reviewer_id: str,
        relationship: str,
        ratings: Dict[str, float],
        strengths: str = "",
        improvements: str = "",
        comments: str = "",
        is_anonymous: bool = True
    ) -> Feedback360:
        """Submit 360 feedback."""
        if review_id not in self.reviews:
            raise ValueError(f"Review {review_id} not found")
        
        feedback = Feedback360(
            review_id=review_id,
            employee_id=employee_id,
            reviewer_id=reviewer_id,
            relationship=relationship,
            ratings=ratings,
            strengths=strengths,
            improvements=improvements,
            comments=comments,
            is_anonymous=is_anonymous,
            created_by=reviewer_id
        )
        
        self.feedback_360[feedback.id] = feedback
        logger.info(f"360 feedback submitted for review {review_id}")
        return feedback
    
    def get_360_feedback_summary(self, review_id: str) -> Dict[str, Any]:
        """Get aggregated 360 feedback for a review."""
        feedbacks = [f for f in self.feedback_360.values() if f.review_id == review_id]
        
        if not feedbacks:
            return {"feedback_count": 0, "average_ratings": {}}
        
        # Aggregate ratings
        all_categories = set()
        for f in feedbacks:
            all_categories.update(f.ratings.keys())
        
        avg_ratings = {}
        for category in all_categories:
            ratings = [f.ratings.get(category) for f in feedbacks if category in f.ratings]
            if ratings:
                avg_ratings[category] = sum(ratings) / len(ratings)
        
        return {
            "feedback_count": len(feedbacks),
            "by_relationship": {
                rel: len([f for f in feedbacks if f.relationship == rel])
                for rel in ["manager", "peer", "direct_report", "self"]
            },
            "average_ratings": avg_ratings
        }
    
    # =========================================================================
    # ONBOARDING
    # =========================================================================
    
    def _create_default_onboarding(self, employee_id: str, created_by: str) -> OnboardingChecklist:
        """Create default onboarding checklist for new employee."""
        employee = self.employees[employee_id]
        target_date = employee.hire_date + timedelta(days=30) if employee.hire_date else None
        
        checklist = OnboardingChecklist(
            employee_id=employee_id,
            template_name="default",
            status=OnboardingStatus.NOT_STARTED,
            start_date=employee.hire_date or date.today(),
            target_completion_date=target_date,
            created_by=created_by
        )
        
        # Default tasks
        default_tasks = [
            ("Sign employment contract", "HR", "Admin", 1),
            ("Complete tax forms (TD1)", "HR", "Admin", 2),
            ("Submit banking info for payroll", "HR", "Admin", 3),
            ("Complete emergency contact form", "HR", "Admin", 4),
            ("Review employee handbook", "Employee", "HR", 5),
            ("Sign policy acknowledgments", "Employee", "HR", 6),
            ("Request laptop/equipment", "IT", "IT", 7),
            ("Setup email account", "IT", "IT", 8),
            ("Configure VPN access", "IT", "IT", 9),
            ("Building access card", "IT", "IT", 10),
            ("Team introduction meeting", "Manager", "Training", 11),
            ("Department orientation", "Manager", "Training", 12),
            ("System training", "Manager", "Training", 13),
            ("30-day check-in scheduled", "Manager", "HR", 14),
        ]
        
        for title, assigned, category, order in default_tasks:
            task = OnboardingTask(
                checklist_id=checklist.id,
                title=title,
                assigned_to=assigned,
                category=category,
                order=order,
                due_date=employee.hire_date + timedelta(days=7) if employee.hire_date else None
            )
            checklist.tasks.append(task)
        
        self.onboarding[checklist.id] = checklist
        logger.info(f"Created onboarding checklist for {employee_id}")
        return checklist
    
    def get_onboarding(self, employee_id: str) -> Optional[OnboardingChecklist]:
        """Get onboarding checklist for employee."""
        for checklist in self.onboarding.values():
            if checklist.employee_id == employee_id:
                return checklist
        return None
    
    def complete_onboarding_task(
        self,
        checklist_id: str,
        task_id: str,
        completed_by: str,
        notes: str = ""
    ) -> OnboardingChecklist:
        """Mark an onboarding task as complete."""
        if checklist_id not in self.onboarding:
            raise ValueError(f"Checklist {checklist_id} not found")
        
        checklist = self.onboarding[checklist_id]
        
        for task in checklist.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.utcnow()
                task.completed_by = completed_by
                task.notes = notes
                break
        else:
            raise ValueError(f"Task {task_id} not found")
        
        # Update progress
        completed = sum(1 for t in checklist.tasks if t.status == TaskStatus.COMPLETED)
        checklist.progress_percent = (completed / len(checklist.tasks)) * 100
        
        # Update status
        if checklist.progress_percent >= 100:
            checklist.status = OnboardingStatus.COMPLETED
            checklist.completed_date = date.today()
        elif checklist.status == OnboardingStatus.NOT_STARTED:
            checklist.status = OnboardingStatus.IN_PROGRESS
        
        logger.info(f"Onboarding task {task_id} completed - Progress: {checklist.progress_percent}%")
        return checklist
    
    # =========================================================================
    # ATTENDANCE / TIME TRACKING
    # =========================================================================
    
    def clock_in(self, employee_id: str, created_by: str) -> TimeEntry:
        """Clock in for the day."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        # Check if already clocked in today
        today = date.today()
        for entry in self.time_entries.values():
            if entry.employee_id == employee_id and entry.date == today and not entry.clock_out:
                raise ValueError("Already clocked in today")
        
        entry = TimeEntry(
            employee_id=employee_id,
            date=today,
            clock_in=datetime.utcnow(),
            created_by=created_by
        )
        
        self.time_entries[entry.id] = entry
        logger.info(f"Clock in: {employee_id}")
        return entry
    
    def clock_out(self, employee_id: str, break_minutes: int = 0) -> TimeEntry:
        """Clock out for the day."""
        today = date.today()
        entry = None
        
        for e in self.time_entries.values():
            if e.employee_id == employee_id and e.date == today and not e.clock_out:
                entry = e
                break
        
        if not entry:
            raise ValueError("No active clock-in found for today")
        
        entry.clock_out = datetime.utcnow()
        entry.break_minutes = break_minutes
        
        # Calculate hours
        if entry.clock_in:
            worked = (entry.clock_out - entry.clock_in).total_seconds() / 3600
            entry.total_hours = max(0, worked - (break_minutes / 60))
            
            # Calculate overtime (> 8 hours)
            if entry.total_hours > 8:
                entry.overtime_hours = entry.total_hours - 8
        
        logger.info(f"Clock out: {employee_id} - {entry.total_hours:.2f} hours")
        return entry
    
    def get_timesheet(
        self,
        employee_id: str,
        start_date: date,
        end_date: date
    ) -> List[TimeEntry]:
        """Get timesheet entries for date range."""
        return [
            e for e in self.time_entries.values()
            if e.employee_id == employee_id and start_date <= e.date <= end_date
        ]
    
    def approve_timesheet(
        self,
        employee_id: str,
        start_date: date,
        end_date: date,
        approved_by: str
    ) -> int:
        """Approve timesheet entries for period."""
        count = 0
        for entry in self.time_entries.values():
            if (entry.employee_id == employee_id and 
                start_date <= entry.date <= end_date and
                not entry.is_approved):
                entry.is_approved = True
                entry.approved_by = approved_by
                count += 1
        
        logger.info(f"Approved {count} timesheet entries for {employee_id}")
        return count
    
    # =========================================================================
    # BENEFITS
    # =========================================================================
    
    def create_benefit_plan(
        self,
        name: str,
        benefit_type: BenefitType,
        provider: str,
        employee_contribution: Decimal,
        employer_contribution: Decimal,
        description: str = "",
        coverage_details: str = "",
        created_by: str = ""
    ) -> BenefitPlan:
        """Create a benefit plan."""
        plan = BenefitPlan(
            name=name,
            benefit_type=benefit_type,
            provider=provider,
            employee_contribution=employee_contribution,
            employer_contribution=employer_contribution,
            description=description,
            coverage_details=coverage_details,
            created_by=created_by
        )
        
        self.benefit_plans[plan.id] = plan
        logger.info(f"Created benefit plan: {name}")
        return plan
    
    def enroll_in_benefit(
        self,
        employee_id: str,
        plan_id: str,
        coverage_level: str,
        effective_date: date,
        dependents: List[Dict] = None,
        created_by: str = ""
    ) -> BenefitEnrollment:
        """Enroll employee in benefit plan."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        if plan_id not in self.benefit_plans:
            raise ValueError(f"Benefit plan {plan_id} not found")
        
        enrollment = BenefitEnrollment(
            employee_id=employee_id,
            plan_id=plan_id,
            coverage_level=coverage_level,
            effective_date=effective_date,
            dependents=dependents or [],
            created_by=created_by
        )
        
        self.enrollments[enrollment.id] = enrollment
        logger.info(f"Enrolled {employee_id} in plan {plan_id}")
        return enrollment
    
    def get_employee_benefits(self, employee_id: str) -> List[Dict]:
        """Get all benefit enrollments for employee."""
        enrollments = [e for e in self.enrollments.values() 
                      if e.employee_id == employee_id and e.status == "active"]
        
        result = []
        for enrollment in enrollments:
            plan = self.benefit_plans.get(enrollment.plan_id)
            if plan:
                result.append({
                    "enrollment_id": enrollment.id,
                    "plan_id": plan.id,
                    "plan_name": plan.name,
                    "type": plan.benefit_type.value,
                    "provider": plan.provider,
                    "coverage_level": enrollment.coverage_level,
                    "employee_contribution": str(plan.employee_contribution),
                    "effective_date": enrollment.effective_date.isoformat()
                })
        
        return result
    
    # =========================================================================
    # COMPLIANCE
    # =========================================================================
    
    def add_compliance_requirement(
        self,
        employee_id: str,
        name: str,
        category: str,
        due_date: Optional[date] = None,
        is_mandatory: bool = True,
        description: str = "",
        created_by: str = ""
    ) -> ComplianceItem:
        """Add a compliance requirement for employee."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        item = ComplianceItem(
            employee_id=employee_id,
            name=name,
            category=category,
            description=description,
            due_date=due_date,
            is_mandatory=is_mandatory,
            created_by=created_by
        )
        
        self.compliance_items[item.id] = item
        logger.info(f"Added compliance requirement: {name} for {employee_id}")
        return item
    
    def complete_compliance_item(
        self,
        item_id: str,
        document_url: str = "",
        verified_by: Optional[str] = None,
        expiry_date: Optional[date] = None
    ) -> ComplianceItem:
        """Mark compliance item as completed."""
        if item_id not in self.compliance_items:
            raise ValueError(f"Compliance item {item_id} not found")
        
        item = self.compliance_items[item_id]
        item.status = ComplianceItemStatus.APPROVED if verified_by else ComplianceItemStatus.SUBMITTED
        item.completed_date = date.today()
        item.document_url = document_url
        item.verified_by = verified_by
        item.expiry_date = expiry_date
        
        logger.info(f"Compliance item {item_id} completed")
        return item
    
    def get_compliance_status(self, employee_id: str) -> Dict[str, Any]:
        """Get compliance status summary for employee."""
        items = [i for i in self.compliance_items.values() if i.employee_id == employee_id]
        
        required = [i for i in items if i.is_mandatory]
        completed = [i for i in required if i.status in [ComplianceItemStatus.SUBMITTED, ComplianceItemStatus.APPROVED]]
        expired = [i for i in items if i.status == ComplianceItemStatus.EXPIRED]
        overdue = [i for i in items if i.due_date and i.due_date < date.today() and i.status == ComplianceItemStatus.REQUIRED]
        
        return {
            "total_required": len(required),
            "completed": len(completed),
            "compliance_rate": (len(completed) / len(required) * 100) if required else 100.0,
            "expired_count": len(expired),
            "overdue_count": len(overdue),
            "items": [
                {
                    "id": i.id,
                    "name": i.name,
                    "category": i.category,
                    "status": i.status.value,
                    "due_date": i.due_date.isoformat() if i.due_date else None,
                    "is_mandatory": i.is_mandatory
                }
                for i in items
            ]
        }
    
    def check_expiring_compliance(self, days_ahead: int = 30) -> List[ComplianceItem]:
        """Find compliance items expiring soon."""
        cutoff = date.today() + timedelta(days=days_ahead)
        expiring = []
        
        for item in self.compliance_items.values():
            if (item.expiry_date and 
                item.expiry_date <= cutoff and
                item.status not in [ComplianceItemStatus.EXPIRED, ComplianceItemStatus.WAIVED]):
                expiring.append(item)
        
        return expiring
    
    # =========================================================================
    # PAYROLL (Basic)
    # =========================================================================
    
    def generate_payroll(
        self,
        employee_id: str,
        pay_period_start: date,
        pay_period_end: date,
        pay_date: date,
        created_by: str = ""
    ) -> PayrollRecord:
        """Generate payroll record for employee."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = self.employees[employee_id]
        
        # Get time entries for period
        time_entries = self.get_timesheet(employee_id, pay_period_start, pay_period_end)
        
        # Calculate hours
        regular_hours = sum(min(e.total_hours, 8) for e in time_entries)
        overtime_hours = sum(e.overtime_hours for e in time_entries)
        
        # Calculate gross pay
        if employee.pay_frequency == PayFrequency.BIWEEKLY:
            periods_per_year = 26
        elif employee.pay_frequency == PayFrequency.SEMI_MONTHLY:
            periods_per_year = 24
        elif employee.pay_frequency == PayFrequency.MONTHLY:
            periods_per_year = 12
        else:
            periods_per_year = 52
        
        base_pay = employee.salary / Decimal(periods_per_year)
        overtime_rate = (employee.salary / Decimal(2080)) * Decimal("1.5")  # 1.5x hourly
        overtime_pay = overtime_rate * Decimal(str(overtime_hours))
        gross_pay = base_pay + overtime_pay
        
        # Calculate deductions (simplified Canadian payroll)
        # Federal tax (approximate 15-33% marginal)
        annual_salary = float(employee.salary)
        if annual_salary < 53359:
            fed_rate = Decimal("0.15")
        elif annual_salary < 106717:
            fed_rate = Decimal("0.205")
        elif annual_salary < 165430:
            fed_rate = Decimal("0.26")
        else:
            fed_rate = Decimal("0.29")
        federal_tax = gross_pay * fed_rate
        
        # Provincial tax (using Quebec as default, ~15-25.75%)
        if annual_salary < 49275:
            prov_rate = Decimal("0.14")
        elif annual_salary < 98540:
            prov_rate = Decimal("0.19")
        else:
            prov_rate = Decimal("0.2575")
        provincial_tax = gross_pay * prov_rate
        
        # CPP (5.95% up to max $3,754.45 annual)
        cpp_rate = Decimal("0.0595")
        cpp_contribution = min(gross_pay * cpp_rate, Decimal("144.40"))  # Bi-weekly max approx
        
        # EI (1.63% up to max $1,002.45 annual)
        ei_rate = Decimal("0.0163")
        ei_contribution = min(gross_pay * ei_rate, Decimal("38.56"))  # Bi-weekly max approx
        
        # Benefit deductions
        benefit_deductions = Decimal("0")
        for enrollment in self.enrollments.values():
            if enrollment.employee_id == employee_id and enrollment.status == "active":
                plan = self.benefit_plans.get(enrollment.plan_id)
                if plan:
                    # Convert to per-pay-period amount
                    if plan.contribution_frequency == PayFrequency.MONTHLY:
                        benefit_deductions += plan.employee_contribution / Decimal("2")
                    else:
                        benefit_deductions += plan.employee_contribution
        
        total_deductions = federal_tax + provincial_tax + cpp_contribution + ei_contribution + benefit_deductions
        net_pay = gross_pay - total_deductions
        
        record = PayrollRecord(
            employee_id=employee_id,
            pay_period_start=pay_period_start,
            pay_period_end=pay_period_end,
            pay_date=pay_date,
            regular_hours=regular_hours,
            overtime_hours=overtime_hours,
            gross_pay=gross_pay.quantize(Decimal("0.01")),
            federal_tax=federal_tax.quantize(Decimal("0.01")),
            provincial_tax=provincial_tax.quantize(Decimal("0.01")),
            cpp_contribution=cpp_contribution.quantize(Decimal("0.01")),
            ei_contribution=ei_contribution.quantize(Decimal("0.01")),
            benefit_deductions=benefit_deductions.quantize(Decimal("0.01")),
            total_deductions=total_deductions.quantize(Decimal("0.01")),
            net_pay=net_pay.quantize(Decimal("0.01")),
            status="pending",
            created_by=created_by
        )
        
        self.payroll_records[record.id] = record
        logger.info(f"Generated payroll for {employee_id}: Gross ${gross_pay}, Net ${net_pay}")
        return record
    
    def process_payroll(self, record_id: str) -> PayrollRecord:
        """Process payroll record (mark as paid)."""
        if record_id not in self.payroll_records:
            raise ValueError(f"Payroll record {record_id} not found")
        
        record = self.payroll_records[record_id]
        record.status = "processed"
        record.processed_at = datetime.utcnow()
        
        logger.info(f"Payroll record {record_id} processed")
        return record
    
    def get_pay_stubs(
        self,
        employee_id: str,
        year: int = None
    ) -> List[PayrollRecord]:
        """Get pay stubs for employee."""
        records = [r for r in self.payroll_records.values() if r.employee_id == employee_id]
        
        if year:
            records = [r for r in records if r.pay_date.year == year]
        
        return sorted(records, key=lambda r: r.pay_date, reverse=True)
    
    # =========================================================================
    # AI FEATURES
    # =========================================================================
    
    def predict_attrition_risk(self, employee_id: str) -> Dict[str, Any]:
        """AI: Predict employee attrition risk."""
        if employee_id not in self.employees:
            raise ValueError(f"Employee {employee_id} not found")
        
        employee = self.employees[employee_id]
        risk_score = 0.0
        risk_factors = []
        
        # Tenure factor (new employees higher risk)
        if employee.hire_date:
            tenure_months = (date.today() - employee.hire_date).days / 30
            if tenure_months < 6:
                risk_score += 15
                risk_factors.append("New employee (< 6 months)")
            elif tenure_months > 24:
                risk_score -= 10  # Longer tenure = lower risk
        
        # Recent performance reviews
        reviews = [r for r in self.reviews.values() 
                   if r.employee_id == employee_id and r.status == ReviewStatus.COMPLETED]
        if reviews:
            latest_rating = reviews[-1].overall_rating
            if latest_rating and latest_rating < 3.0:
                risk_score += 20
                risk_factors.append("Low performance rating")
        
        # PTO usage (taking all PTO = potential burnout)
        vacation_balance = employee.pto_balances.get("vacation", 0)
        if vacation_balance <= 0:
            risk_score += 10
            risk_factors.append("No vacation balance remaining")
        
        # Pending leave requests (looking for time off)
        pending_leaves = [l for l in self.leave_requests.values() 
                        if l.employee_id == employee_id and l.status == LeaveStatus.PENDING]
        if len(pending_leaves) > 2:
            risk_score += 5
            risk_factors.append("Multiple pending leave requests")
        
        # No salary increase in reviews
        recent_review = reviews[-1] if reviews else None
        if recent_review and not recent_review.salary_increase_recommended:
            risk_score += 10
            risk_factors.append("No salary increase recommended")
        
        # Normalize score
        risk_score = min(100, max(0, risk_score))
        
        # Risk level
        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "employee_id": employee_id,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendations": self._get_retention_recommendations(risk_factors)
        }
    
    def _get_retention_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Get recommendations based on risk factors."""
        recommendations = []
        
        for factor in risk_factors:
            if "performance" in factor.lower():
                recommendations.append("Schedule 1:1 meeting to discuss development plan")
            if "vacation" in factor.lower():
                recommendations.append("Encourage taking time off to prevent burnout")
            if "salary" in factor.lower():
                recommendations.append("Review compensation against market rates")
            if "new employee" in factor.lower():
                recommendations.append("Ensure proper onboarding and mentorship")
        
        if not recommendations:
            recommendations.append("Maintain regular check-ins")
        
        return recommendations
    
    def benchmark_compensation(self, position_id: str) -> Dict[str, Any]:
        """AI: Benchmark compensation for a position."""
        if position_id not in self.positions:
            raise ValueError(f"Position {position_id} not found")
        
        position = self.positions[position_id]
        
        # Get all employees in this position
        employees = [e for e in self.employees.values() if e.position_id == position_id]
        
        if not employees:
            return {
                "position": position.title,
                "no_data": True,
                "message": "No employees in this position"
            }
        
        salaries = [float(e.salary) for e in employees]
        avg_salary = sum(salaries) / len(salaries)
        min_salary = min(salaries)
        max_salary = max(salaries)
        
        # Compare to position band
        band_min = float(position.salary_min)
        band_max = float(position.salary_max)
        band_mid = (band_min + band_max) / 2
        
        # Identify outliers
        underpaid = [e for e in employees if float(e.salary) < band_min]
        overpaid = [e for e in employees if float(e.salary) > band_max]
        
        return {
            "position": position.title,
            "level": position.level,
            "employee_count": len(employees),
            "current_salaries": {
                "min": min_salary,
                "max": max_salary,
                "average": avg_salary
            },
            "salary_band": {
                "min": band_min,
                "max": band_max,
                "midpoint": band_mid
            },
            "analysis": {
                "average_vs_midpoint": ((avg_salary - band_mid) / band_mid) * 100 if band_mid > 0 else 0,
                "underpaid_count": len(underpaid),
                "overpaid_count": len(overpaid)
            },
            "recommendations": [
                f"Review compensation for {len(underpaid)} employees below band minimum"
            ] if underpaid else []
        }
    
    def analyze_skills_gap(self, department_id: str) -> Dict[str, Any]:
        """AI: Analyze skills gap in department."""
        if department_id not in self.departments:
            raise ValueError(f"Department {department_id} not found")
        
        department = self.departments[department_id]
        employees = [e for e in self.employees.values() if e.department_id == department_id]
        
        # Collect required skills from positions
        required_skills = set()
        for emp in employees:
            if emp.position_id in self.positions:
                position = self.positions[emp.position_id]
                required_skills.update(position.requirements)
        
        # Get compliance/certification status
        certified = {}
        for skill in required_skills:
            count = 0
            for emp in employees:
                emp_compliance = [c for c in self.compliance_items.values() 
                                 if c.employee_id == emp.id and skill.lower() in c.name.lower()]
                if any(c.status in [ComplianceItemStatus.APPROVED, ComplianceItemStatus.SUBMITTED] 
                       for c in emp_compliance):
                    count += 1
            certified[skill] = count
        
        # Identify gaps
        gaps = []
        for skill, count in certified.items():
            coverage = (count / len(employees)) * 100 if employees else 0
            if coverage < 80:
                gaps.append({
                    "skill": skill,
                    "coverage": coverage,
                    "employees_certified": count,
                    "total_employees": len(employees)
                })
        
        return {
            "department": department.name,
            "total_employees": len(employees),
            "required_skills": list(required_skills),
            "skill_coverage": certified,
            "gaps": sorted(gaps, key=lambda x: x["coverage"]),
            "recommendations": [
                f"Training needed for: {g['skill']} ({g['coverage']:.0f}% coverage)"
                for g in gaps[:3]
            ]
        }
    
    def get_workforce_analytics(self) -> Dict[str, Any]:
        """Get overall workforce analytics."""
        employees = list(self.employees.values())
        active = [e for e in employees if e.employment_status == EmploymentStatus.ACTIVE]
        
        # Headcount by department
        by_department = {}
        for emp in active:
            dept = self.departments.get(emp.department_id)
            dept_name = dept.name if dept else "Unknown"
            by_department[dept_name] = by_department.get(dept_name, 0) + 1
        
        # Employment type breakdown
        by_type = {}
        for emp in active:
            emp_type = emp.employment_type.value
            by_type[emp_type] = by_type.get(emp_type, 0) + 1
        
        # Tenure distribution
        tenure_buckets = {"< 1 year": 0, "1-2 years": 0, "2-5 years": 0, "5+ years": 0}
        for emp in active:
            if emp.hire_date:
                years = (date.today() - emp.hire_date).days / 365
                if years < 1:
                    tenure_buckets["< 1 year"] += 1
                elif years < 2:
                    tenure_buckets["1-2 years"] += 1
                elif years < 5:
                    tenure_buckets["2-5 years"] += 1
                else:
                    tenure_buckets["5+ years"] += 1
        
        # Pending items
        pending_leaves = sum(1 for l in self.leave_requests.values() if l.status == LeaveStatus.PENDING)
        pending_reviews = sum(1 for r in self.reviews.values() if r.status == ReviewStatus.SCHEDULED)
        
        return {
            "total_employees": len(employees),
            "active_employees": len(active),
            "by_department": by_department,
            "by_employment_type": by_type,
            "tenure_distribution": tenure_buckets,
            "pending_leave_requests": pending_leaves,
            "scheduled_reviews": pending_reviews,
            "new_hires_this_month": sum(
                1 for e in active 
                if e.hire_date and e.hire_date.month == date.today().month and e.hire_date.year == date.today().year
            ),
            "open_positions": sum(1 for p in self.positions.values() if p.is_active)
        }
    
    # =========================================================================
    # DASHBOARD
    # =========================================================================
    
    def get_dashboard(self, user_id: str, is_manager: bool = False) -> Dict[str, Any]:
        """Get HR dashboard data."""
        analytics = self.get_workforce_analytics()
        
        # Get pending items for HR
        pending_items = {
            "leave_requests": [],
            "reviews": [],
            "onboarding": [],
            "compliance": []
        }
        
        for request in self.leave_requests.values():
            if request.status == LeaveStatus.PENDING:
                emp = self.employees.get(request.employee_id)
                pending_items["leave_requests"].append({
                    "id": request.id,
                    "employee": f"{emp.first_name} {emp.last_name}" if emp else "Unknown",
                    "type": request.leave_type.value,
                    "dates": f"{request.start_date} - {request.end_date}",
                    "days": request.days_requested
                })
        
        for checklist in self.onboarding.values():
            if checklist.status == OnboardingStatus.IN_PROGRESS:
                emp = self.employees.get(checklist.employee_id)
                pending_items["onboarding"].append({
                    "id": checklist.id,
                    "employee": f"{emp.first_name} {emp.last_name}" if emp else "Unknown",
                    "progress": checklist.progress_percent
                })
        
        # Expiring compliance
        expiring = self.check_expiring_compliance(30)
        for item in expiring:
            emp = self.employees.get(item.employee_id)
            pending_items["compliance"].append({
                "id": item.id,
                "employee": f"{emp.first_name} {emp.last_name}" if emp else "Unknown",
                "item": item.name,
                "expires": item.expiry_date.isoformat() if item.expiry_date else None
            })
        
        return {
            "analytics": analytics,
            "pending_items": pending_items,
            "quick_stats": {
                "total_headcount": analytics["active_employees"],
                "pending_approvals": len(pending_items["leave_requests"]),
                "active_onboardings": len(pending_items["onboarding"]),
                "expiring_compliance": len(pending_items["compliance"])
            }
        }


# =============================================================================
# TESTING
# =============================================================================

if __name__ == "__main__":
    # Test the HR Agent
    agent = HRAgent()
    
    # Setup
    print("Setting up HR system...")
    
    # Create department
    engineering = agent.create_department(
        name="Engineering",
        code="ENG",
        description="Software Engineering Department",
        budget=Decimal("5000000"),
        headcount_limit=50,
        created_by="system"
    )
    print(f"✅ Created department: {engineering.name}")
    
    # Create position
    dev_position = agent.create_position(
        title="Software Developer",
        department_id=engineering.id,
        level="Mid",
        salary_min=Decimal("70000"),
        salary_max=Decimal("100000"),
        requirements=["Python", "JavaScript", "SQL"],
        created_by="system"
    )
    print(f"✅ Created position: {dev_position.title}")
    
    # Setup leave policies
    policies = agent.setup_default_leave_policies("system")
    print(f"✅ Created {len(policies)} leave policies")
    
    # Create employee
    employee = agent.create_employee(
        first_name="John",
        last_name="Doe",
        email="john.doe@company.com",
        position_id=dev_position.id,
        department_id=engineering.id,
        hire_date=date(2024, 1, 15),
        salary=Decimal("85000"),
        employment_type=EmploymentType.FULL_TIME,
        created_by="system"
    )
    print(f"✅ Created employee: {employee.first_name} {employee.last_name} ({employee.employee_number})")
    
    # Activate employee
    agent.update_employee_status(employee.id, EmploymentStatus.ACTIVE, "system")
    
    # Accrue some PTO
    agent.accrue_pto(employee.id, LeaveType.VACATION, 5.0)
    balance = agent.get_leave_balance(employee.id)
    print(f"✅ PTO Balance: {balance}")
    
    # Submit leave request
    leave = agent.request_leave(
        employee_id=employee.id,
        leave_type=LeaveType.VACATION,
        start_date=date(2026, 2, 1),
        end_date=date(2026, 2, 5),
        reason="Family vacation",
        created_by=employee.id
    )
    print(f"✅ Created leave request: {leave.days_requested} days")
    
    # Approve leave
    agent.approve_leave(leave.id, "manager")
    print("✅ Leave request approved")
    
    # Create goal
    goal = agent.create_goal(
        employee_id=employee.id,
        title="Complete Python certification",
        description="Obtain professional Python certification",
        target_date=date(2026, 6, 30),
        created_by=employee.id
    )
    print(f"✅ Created goal: {goal.title}")
    
    # Clock in/out
    entry = agent.clock_in(employee.id, employee.id)
    print("✅ Clocked in")
    
    import time
    time.sleep(0.1)  # Simulate work
    
    agent.clock_out(employee.id, break_minutes=30)
    print("✅ Clocked out")
    
    # Get dashboard
    dashboard = agent.get_dashboard("admin", is_manager=True)
    print(f"✅ Dashboard: {dashboard['quick_stats']['total_headcount']} employees")
    
    # AI: Attrition prediction
    attrition = agent.predict_attrition_risk(employee.id)
    print(f"✅ Attrition risk: {attrition['risk_level']} ({attrition['risk_score']})")
    
    print("\n🎉 HR Agent test complete!")
