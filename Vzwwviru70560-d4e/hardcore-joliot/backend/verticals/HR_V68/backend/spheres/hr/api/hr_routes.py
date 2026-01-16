"""
CHE·NU™ V68 — HR & PEOPLE OPERATIONS API ROUTES
BambooHR/Gusto Killer - REST API

60+ endpoints covering:
- Departments & Positions
- Employees
- Leave/PTO
- Performance (Goals, Reviews, 360)
- Onboarding
- Attendance
- Benefits
- Compliance
- Payroll
- AI Features
- Dashboard
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from ..agents.hr_agent import (
    HRAgent,
    EmploymentStatus,
    EmploymentType,
    LeaveType,
    LeaveStatus,
    ReviewStatus,
    ReviewType,
    BenefitType,
    PayFrequency,
)

router = APIRouter()

# Singleton agent instance
_hr_agent: Optional[HRAgent] = None


def get_agent() -> HRAgent:
    """Get or create HR agent instance."""
    global _hr_agent
    if _hr_agent is None:
        _hr_agent = HRAgent()
    return _hr_agent


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

# Department
class DepartmentCreate(BaseModel):
    name: str
    code: str
    description: str = ""
    manager_id: Optional[str] = None
    parent_department_id: Optional[str] = None
    budget: float = 0
    headcount_limit: int = 0


class DepartmentResponse(BaseModel):
    id: str
    name: str
    code: str
    description: str
    manager_id: Optional[str]
    budget: float
    headcount_limit: int


# Position
class PositionCreate(BaseModel):
    title: str
    department_id: str
    level: str
    salary_min: float
    salary_max: float
    description: str = ""
    requirements: List[str] = []


class PositionResponse(BaseModel):
    id: str
    title: str
    department_id: str
    level: str
    salary_min: float
    salary_max: float
    requirements: List[str]
    is_active: bool


# Employee
class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    position_id: str
    department_id: str
    hire_date: date
    salary: float
    employment_type: str = "full_time"
    manager_id: Optional[str] = None


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province_state: Optional[str] = None
    postal_code: Optional[str] = None


class SalaryUpdate(BaseModel):
    new_salary: float
    effective_date: date
    reason: str = ""


class StatusUpdate(BaseModel):
    new_status: str
    termination_date: Optional[date] = None


class EmployeeResponse(BaseModel):
    id: str
    employee_number: str
    first_name: str
    last_name: str
    email: str
    department_id: str
    position_id: str
    employment_type: str
    employment_status: str
    hire_date: Optional[date]
    salary: float


# Leave
class LeaveRequestCreate(BaseModel):
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    reason: str = ""


class LeaveApproval(BaseModel):
    approved_by: str


class LeaveRejection(BaseModel):
    rejected_by: str
    reason: str = ""


class LeaveResponse(BaseModel):
    id: str
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    days_requested: float
    status: str
    reason: str


class LeavePolicyCreate(BaseModel):
    name: str
    leave_type: str
    days_per_year: float
    accrual_rate: float = 0.0
    max_carryover: float = 0.0
    max_balance: float = 0.0
    requires_approval: bool = True
    min_notice_days: int = 0


# Performance
class GoalCreate(BaseModel):
    employee_id: str
    title: str
    description: str = ""
    key_results: List[str] = []
    target_date: Optional[date] = None
    weight: float = 1.0


class GoalProgressUpdate(BaseModel):
    progress: float


class ReviewCreate(BaseModel):
    employee_id: str
    reviewer_id: str
    review_type: str
    review_period_start: date
    review_period_end: date
    scheduled_date: date


class ReviewComplete(BaseModel):
    overall_rating: float
    ratings: Dict[str, float] = {}
    strengths: List[str] = []
    areas_for_improvement: List[str] = []
    reviewer_comments: str = ""
    goals_achieved: List[str] = []
    new_goals: List[str] = []
    promotion_recommended: bool = False
    salary_increase_recommended: bool = False
    recommended_increase_percent: float = 0.0


class Feedback360Submit(BaseModel):
    review_id: str
    employee_id: str
    reviewer_id: str
    relationship: str
    ratings: Dict[str, float]
    strengths: str = ""
    improvements: str = ""
    comments: str = ""
    is_anonymous: bool = True


# Onboarding
class OnboardingTaskComplete(BaseModel):
    completed_by: str
    notes: str = ""


# Attendance
class ClockRequest(BaseModel):
    employee_id: str


class ClockOutRequest(BaseModel):
    employee_id: str
    break_minutes: int = 0


class TimesheetApproval(BaseModel):
    employee_id: str
    start_date: date
    end_date: date
    approved_by: str


# Benefits
class BenefitPlanCreate(BaseModel):
    name: str
    benefit_type: str
    provider: str
    employee_contribution: float
    employer_contribution: float
    description: str = ""
    coverage_details: str = ""


class BenefitEnrollment(BaseModel):
    employee_id: str
    plan_id: str
    coverage_level: str
    effective_date: date
    dependents: List[Dict] = []


# Compliance
class ComplianceItemCreate(BaseModel):
    employee_id: str
    name: str
    category: str
    due_date: Optional[date] = None
    is_mandatory: bool = True
    description: str = ""


class ComplianceItemComplete(BaseModel):
    document_url: str = ""
    verified_by: Optional[str] = None
    expiry_date: Optional[date] = None


# Payroll
class PayrollGenerate(BaseModel):
    employee_id: str
    pay_period_start: date
    pay_period_end: date
    pay_date: date


# =============================================================================
# DEPARTMENT ENDPOINTS
# =============================================================================

@router.post("/departments", response_model=DepartmentResponse, tags=["Departments"])
async def create_department(data: DepartmentCreate, user_id: str = "system"):
    """Create a new department."""
    agent = get_agent()
    try:
        dept = agent.create_department(
            name=data.name,
            code=data.code,
            description=data.description,
            manager_id=data.manager_id,
            parent_department_id=data.parent_department_id,
            budget=Decimal(str(data.budget)),
            headcount_limit=data.headcount_limit,
            created_by=user_id
        )
        return DepartmentResponse(
            id=dept.id,
            name=dept.name,
            code=dept.code,
            description=dept.description,
            manager_id=dept.manager_id,
            budget=float(dept.budget),
            headcount_limit=dept.headcount_limit
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/departments", tags=["Departments"])
async def list_departments():
    """List all departments."""
    agent = get_agent()
    departments = agent.list_departments()
    return {
        "departments": [
            {
                "id": d.id,
                "name": d.name,
                "code": d.code,
                "description": d.description,
                "manager_id": d.manager_id,
                "headcount": agent._get_department_headcount(d.id)
            }
            for d in departments
        ]
    }


@router.get("/departments/{department_id}", tags=["Departments"])
async def get_department(department_id: str):
    """Get department details."""
    agent = get_agent()
    dept = agent.get_department(department_id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return {
        "id": dept.id,
        "name": dept.name,
        "code": dept.code,
        "description": dept.description,
        "manager_id": dept.manager_id,
        "budget": float(dept.budget),
        "headcount_limit": dept.headcount_limit,
        "current_headcount": agent._get_department_headcount(dept.id)
    }


@router.get("/org-chart", tags=["Departments"])
async def get_org_chart():
    """Get organization chart structure."""
    agent = get_agent()
    return agent.get_org_chart()


# =============================================================================
# POSITION ENDPOINTS
# =============================================================================

@router.post("/positions", tags=["Positions"])
async def create_position(data: PositionCreate, user_id: str = "system"):
    """Create a job position."""
    agent = get_agent()
    try:
        position = agent.create_position(
            title=data.title,
            department_id=data.department_id,
            level=data.level,
            salary_min=Decimal(str(data.salary_min)),
            salary_max=Decimal(str(data.salary_max)),
            description=data.description,
            requirements=data.requirements,
            created_by=user_id
        )
        return {
            "id": position.id,
            "title": position.title,
            "department_id": position.department_id,
            "level": position.level,
            "salary_range": f"${data.salary_min:,.0f} - ${data.salary_max:,.0f}"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/positions", tags=["Positions"])
async def list_positions(department_id: Optional[str] = None):
    """List positions, optionally filtered by department."""
    agent = get_agent()
    positions = agent.list_positions(department_id)
    return {
        "positions": [
            {
                "id": p.id,
                "title": p.title,
                "department_id": p.department_id,
                "level": p.level,
                "salary_min": float(p.salary_min),
                "salary_max": float(p.salary_max),
                "is_active": p.is_active
            }
            for p in positions
        ]
    }


# =============================================================================
# EMPLOYEE ENDPOINTS
# =============================================================================

@router.post("/employees", tags=["Employees"])
async def create_employee(data: EmployeeCreate, user_id: str = "system"):
    """Create a new employee (pending HR approval)."""
    agent = get_agent()
    try:
        emp_type = EmploymentType(data.employment_type)
        employee = agent.create_employee(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            position_id=data.position_id,
            department_id=data.department_id,
            hire_date=data.hire_date,
            salary=Decimal(str(data.salary)),
            employment_type=emp_type,
            manager_id=data.manager_id,
            created_by=user_id
        )
        return {
            "id": employee.id,
            "employee_number": employee.employee_number,
            "name": f"{employee.first_name} {employee.last_name}",
            "email": employee.email,
            "status": employee.employment_status.value,
            "message": "Employee created. Onboarding checklist auto-generated."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/employees", tags=["Employees"])
async def list_employees(
    department_id: Optional[str] = None,
    status: Optional[str] = None,
    manager_id: Optional[str] = None,
    search: Optional[str] = None
):
    """List employees with optional filters."""
    agent = get_agent()
    
    if search:
        employees = agent.search_employees(search)
    else:
        status_enum = EmploymentStatus(status) if status else None
        employees = agent.list_employees(
            department_id=department_id,
            status=status_enum,
            manager_id=manager_id
        )
    
    return {
        "count": len(employees),
        "employees": [
            {
                "id": e.id,
                "employee_number": e.employee_number,
                "first_name": e.first_name,
                "last_name": e.last_name,
                "email": e.email,
                "department_id": e.department_id,
                "position_id": e.position_id,
                "employment_status": e.employment_status.value,
                "hire_date": e.hire_date.isoformat() if e.hire_date else None
            }
            for e in employees
        ]
    }


@router.get("/employees/{employee_id}", tags=["Employees"])
async def get_employee(employee_id: str):
    """Get employee details."""
    agent = get_agent()
    employee = agent.get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Get related data
    position = agent.positions.get(employee.position_id)
    department = agent.departments.get(employee.department_id)
    
    return {
        "id": employee.id,
        "employee_number": employee.employee_number,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "phone": employee.phone,
        "address": employee.address,
        "city": employee.city,
        "province_state": employee.province_state,
        "postal_code": employee.postal_code,
        "country": employee.country,
        "position": position.title if position else None,
        "department": department.name if department else None,
        "manager_id": employee.manager_id,
        "hire_date": employee.hire_date.isoformat() if employee.hire_date else None,
        "employment_type": employee.employment_type.value,
        "employment_status": employee.employment_status.value,
        "salary": float(employee.salary),
        "pto_balances": employee.pto_balances
    }


@router.patch("/employees/{employee_id}/status", tags=["Employees"])
async def update_employee_status(employee_id: str, data: StatusUpdate, user_id: str = "hr"):
    """Update employee status (requires HR approval)."""
    agent = get_agent()
    try:
        new_status = EmploymentStatus(data.new_status)
        employee = agent.update_employee_status(
            employee_id=employee_id,
            new_status=new_status,
            updated_by=user_id,
            termination_date=data.termination_date
        )
        return {
            "id": employee.id,
            "status": employee.employment_status.value,
            "message": f"Status updated to {data.new_status}"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/employees/{employee_id}/salary", tags=["Employees"])
async def update_salary(employee_id: str, data: SalaryUpdate, user_id: str = "hr"):
    """Update employee salary (requires manager approval)."""
    agent = get_agent()
    try:
        employee = agent.update_salary(
            employee_id=employee_id,
            new_salary=Decimal(str(data.new_salary)),
            effective_date=data.effective_date,
            updated_by=user_id,
            reason=data.reason
        )
        return {
            "id": employee.id,
            "new_salary": float(employee.salary),
            "effective_date": data.effective_date.isoformat(),
            "message": "Salary updated successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/employees/{employee_id}/direct-reports", tags=["Employees"])
async def get_direct_reports(employee_id: str):
    """Get employees reporting to a manager."""
    agent = get_agent()
    reports = agent.get_direct_reports(employee_id)
    return {
        "manager_id": employee_id,
        "direct_reports": [
            {
                "id": e.id,
                "name": f"{e.first_name} {e.last_name}",
                "position_id": e.position_id,
                "status": e.employment_status.value
            }
            for e in reports
        ]
    }


# =============================================================================
# LEAVE / PTO ENDPOINTS
# =============================================================================

@router.post("/leave/policies", tags=["Leave"])
async def create_leave_policy(data: LeavePolicyCreate, user_id: str = "hr"):
    """Create a leave policy."""
    agent = get_agent()
    try:
        leave_type = LeaveType(data.leave_type)
        policy = agent.create_leave_policy(
            name=data.name,
            leave_type=leave_type,
            days_per_year=data.days_per_year,
            accrual_rate=data.accrual_rate,
            max_carryover=data.max_carryover,
            max_balance=data.max_balance,
            requires_approval=data.requires_approval,
            min_notice_days=data.min_notice_days,
            created_by=user_id
        )
        return {
            "id": policy.id,
            "name": policy.name,
            "leave_type": policy.leave_type.value,
            "days_per_year": policy.days_per_year
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/leave/policies/setup-defaults", tags=["Leave"])
async def setup_default_policies(user_id: str = "system"):
    """Setup default Canadian leave policies."""
    agent = get_agent()
    policies = agent.setup_default_leave_policies(user_id)
    return {
        "message": f"Created {len(policies)} default policies",
        "policies": [
            {"name": p.name, "type": p.leave_type.value, "days": p.days_per_year}
            for p in policies
        ]
    }


@router.get("/leave/policies", tags=["Leave"])
async def list_leave_policies():
    """List all leave policies."""
    agent = get_agent()
    return {
        "policies": [
            {
                "id": p.id,
                "name": p.name,
                "leave_type": p.leave_type.value,
                "days_per_year": p.days_per_year,
                "requires_approval": p.requires_approval
            }
            for p in agent.leave_policies.values()
        ]
    }


@router.post("/leave/requests", tags=["Leave"])
async def request_leave(data: LeaveRequestCreate, user_id: str = "employee"):
    """Submit a leave request."""
    agent = get_agent()
    try:
        leave_type = LeaveType(data.leave_type)
        request = agent.request_leave(
            employee_id=data.employee_id,
            leave_type=leave_type,
            start_date=data.start_date,
            end_date=data.end_date,
            reason=data.reason,
            created_by=user_id
        )
        return {
            "id": request.id,
            "status": request.status.value,
            "days_requested": request.days_requested,
            "message": "Leave request submitted for approval"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/leave/requests", tags=["Leave"])
async def list_leave_requests(
    employee_id: Optional[str] = None,
    status: Optional[str] = None
):
    """List leave requests."""
    agent = get_agent()
    requests = list(agent.leave_requests.values())
    
    if employee_id:
        requests = [r for r in requests if r.employee_id == employee_id]
    if status:
        status_enum = LeaveStatus(status)
        requests = [r for r in requests if r.status == status_enum]
    
    return {
        "count": len(requests),
        "requests": [
            {
                "id": r.id,
                "employee_id": r.employee_id,
                "leave_type": r.leave_type.value,
                "start_date": r.start_date.isoformat(),
                "end_date": r.end_date.isoformat(),
                "days_requested": r.days_requested,
                "status": r.status.value,
                "reason": r.reason
            }
            for r in requests
        ]
    }


@router.post("/leave/requests/{request_id}/approve", tags=["Leave"])
async def approve_leave(request_id: str, data: LeaveApproval):
    """Approve a leave request (manager action)."""
    agent = get_agent()
    try:
        request = agent.approve_leave(request_id, data.approved_by)
        return {
            "id": request.id,
            "status": request.status.value,
            "message": "Leave request approved"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/leave/requests/{request_id}/reject", tags=["Leave"])
async def reject_leave(request_id: str, data: LeaveRejection):
    """Reject a leave request."""
    agent = get_agent()
    try:
        request = agent.reject_leave(request_id, data.rejected_by, data.reason)
        return {
            "id": request.id,
            "status": request.status.value,
            "message": "Leave request rejected"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/leave/balance/{employee_id}", tags=["Leave"])
async def get_leave_balance(employee_id: str):
    """Get employee's leave balances."""
    agent = get_agent()
    try:
        balance = agent.get_leave_balance(employee_id)
        return {
            "employee_id": employee_id,
            "balances": balance
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/leave/accrue", tags=["Leave"])
async def accrue_pto(employee_id: str, leave_type: str, days: float):
    """Accrue PTO for an employee (typically monthly)."""
    agent = get_agent()
    try:
        new_balance = agent.accrue_pto(employee_id, LeaveType(leave_type), days)
        return {
            "employee_id": employee_id,
            "leave_type": leave_type,
            "days_accrued": days,
            "new_balance": new_balance
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/leave/calendar", tags=["Leave"])
async def get_team_calendar(manager_id: str, start_date: date, end_date: date):
    """Get approved leave calendar for a team."""
    agent = get_agent()
    calendar = agent.get_team_calendar(manager_id, start_date, end_date)
    return {
        "manager_id": manager_id,
        "period": f"{start_date} to {end_date}",
        "leaves": calendar
    }


# =============================================================================
# PERFORMANCE ENDPOINTS
# =============================================================================

@router.post("/goals", tags=["Performance"])
async def create_goal(data: GoalCreate, user_id: str = "employee"):
    """Create an employee goal."""
    agent = get_agent()
    try:
        goal = agent.create_goal(
            employee_id=data.employee_id,
            title=data.title,
            description=data.description,
            key_results=data.key_results,
            target_date=data.target_date,
            weight=data.weight,
            created_by=user_id
        )
        return {
            "id": goal.id,
            "title": goal.title,
            "target_date": goal.target_date.isoformat() if goal.target_date else None,
            "status": goal.status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/goals", tags=["Performance"])
async def get_goals(employee_id: str, status: Optional[str] = None):
    """Get goals for an employee."""
    agent = get_agent()
    goals = agent.get_employee_goals(employee_id, status)
    return {
        "employee_id": employee_id,
        "goals": [
            {
                "id": g.id,
                "title": g.title,
                "description": g.description,
                "key_results": g.key_results,
                "progress": g.progress,
                "status": g.status,
                "target_date": g.target_date.isoformat() if g.target_date else None
            }
            for g in goals
        ]
    }


@router.patch("/goals/{goal_id}/progress", tags=["Performance"])
async def update_goal_progress(goal_id: str, data: GoalProgressUpdate, user_id: str = "employee"):
    """Update goal progress."""
    agent = get_agent()
    try:
        goal = agent.update_goal_progress(goal_id, data.progress, user_id)
        return {
            "id": goal.id,
            "progress": goal.progress,
            "status": goal.status
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/reviews", tags=["Performance"])
async def create_review(data: ReviewCreate, user_id: str = "hr"):
    """Schedule a performance review."""
    agent = get_agent()
    try:
        review_type = ReviewType(data.review_type)
        review = agent.create_performance_review(
            employee_id=data.employee_id,
            reviewer_id=data.reviewer_id,
            review_type=review_type,
            review_period_start=data.review_period_start,
            review_period_end=data.review_period_end,
            scheduled_date=data.scheduled_date,
            created_by=user_id
        )
        return {
            "id": review.id,
            "employee_id": review.employee_id,
            "review_type": review.review_type.value,
            "scheduled_date": review.scheduled_date.isoformat(),
            "status": review.status.value
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reviews", tags=["Performance"])
async def list_reviews(
    employee_id: Optional[str] = None,
    status: Optional[str] = None
):
    """List performance reviews."""
    agent = get_agent()
    reviews = list(agent.reviews.values())
    
    if employee_id:
        reviews = [r for r in reviews if r.employee_id == employee_id]
    if status:
        status_enum = ReviewStatus(status)
        reviews = [r for r in reviews if r.status == status_enum]
    
    return {
        "count": len(reviews),
        "reviews": [
            {
                "id": r.id,
                "employee_id": r.employee_id,
                "reviewer_id": r.reviewer_id,
                "review_type": r.review_type.value,
                "status": r.status.value,
                "scheduled_date": r.scheduled_date.isoformat() if r.scheduled_date else None,
                "overall_rating": r.overall_rating
            }
            for r in reviews
        ]
    }


@router.post("/reviews/{review_id}/complete", tags=["Performance"])
async def complete_review(review_id: str, data: ReviewComplete, user_id: str = "manager"):
    """Complete a performance review."""
    agent = get_agent()
    try:
        review = agent.complete_review(
            review_id=review_id,
            overall_rating=data.overall_rating,
            ratings=data.ratings,
            strengths=data.strengths,
            areas_for_improvement=data.areas_for_improvement,
            reviewer_comments=data.reviewer_comments,
            goals_achieved=data.goals_achieved,
            new_goals=data.new_goals,
            promotion_recommended=data.promotion_recommended,
            salary_increase_recommended=data.salary_increase_recommended,
            recommended_increase_percent=data.recommended_increase_percent,
            completed_by=user_id
        )
        return {
            "id": review.id,
            "status": review.status.value,
            "overall_rating": review.overall_rating,
            "completed_date": review.completed_date.isoformat() if review.completed_date else None
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reviews/360-feedback", tags=["Performance"])
async def submit_360_feedback(data: Feedback360Submit):
    """Submit 360 degree feedback."""
    agent = get_agent()
    try:
        feedback = agent.submit_360_feedback(
            review_id=data.review_id,
            employee_id=data.employee_id,
            reviewer_id=data.reviewer_id,
            relationship=data.relationship,
            ratings=data.ratings,
            strengths=data.strengths,
            improvements=data.improvements,
            comments=data.comments,
            is_anonymous=data.is_anonymous
        )
        return {
            "id": feedback.id,
            "message": "360 feedback submitted successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/reviews/{review_id}/360-summary", tags=["Performance"])
async def get_360_summary(review_id: str):
    """Get aggregated 360 feedback summary."""
    agent = get_agent()
    return agent.get_360_feedback_summary(review_id)


# =============================================================================
# ONBOARDING ENDPOINTS
# =============================================================================

@router.get("/onboarding/{employee_id}", tags=["Onboarding"])
async def get_onboarding(employee_id: str):
    """Get onboarding checklist for employee."""
    agent = get_agent()
    checklist = agent.get_onboarding(employee_id)
    if not checklist:
        raise HTTPException(status_code=404, detail="Onboarding checklist not found")
    
    return {
        "id": checklist.id,
        "employee_id": checklist.employee_id,
        "status": checklist.status.value,
        "progress_percent": checklist.progress_percent,
        "start_date": checklist.start_date.isoformat(),
        "target_completion_date": checklist.target_completion_date.isoformat() if checklist.target_completion_date else None,
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "category": t.category,
                "assigned_to": t.assigned_to,
                "status": t.status.value,
                "due_date": t.due_date.isoformat() if t.due_date else None
            }
            for t in checklist.tasks
        ]
    }


@router.post("/onboarding/{checklist_id}/tasks/{task_id}/complete", tags=["Onboarding"])
async def complete_onboarding_task(checklist_id: str, task_id: str, data: OnboardingTaskComplete):
    """Mark an onboarding task as complete."""
    agent = get_agent()
    try:
        checklist = agent.complete_onboarding_task(
            checklist_id=checklist_id,
            task_id=task_id,
            completed_by=data.completed_by,
            notes=data.notes
        )
        return {
            "checklist_id": checklist.id,
            "task_id": task_id,
            "progress_percent": checklist.progress_percent,
            "status": checklist.status.value
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =============================================================================
# ATTENDANCE ENDPOINTS
# =============================================================================

@router.post("/attendance/clock-in", tags=["Attendance"])
async def clock_in(data: ClockRequest):
    """Clock in for the day."""
    agent = get_agent()
    try:
        entry = agent.clock_in(data.employee_id, data.employee_id)
        return {
            "id": entry.id,
            "employee_id": entry.employee_id,
            "clock_in": entry.clock_in.isoformat() if entry.clock_in else None,
            "message": "Clocked in successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/attendance/clock-out", tags=["Attendance"])
async def clock_out(data: ClockOutRequest):
    """Clock out for the day."""
    agent = get_agent()
    try:
        entry = agent.clock_out(data.employee_id, data.break_minutes)
        return {
            "id": entry.id,
            "employee_id": entry.employee_id,
            "clock_out": entry.clock_out.isoformat() if entry.clock_out else None,
            "total_hours": entry.total_hours,
            "overtime_hours": entry.overtime_hours,
            "message": "Clocked out successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/attendance/timesheet", tags=["Attendance"])
async def get_timesheet(employee_id: str, start_date: date, end_date: date):
    """Get timesheet entries for date range."""
    agent = get_agent()
    entries = agent.get_timesheet(employee_id, start_date, end_date)
    
    total_hours = sum(e.total_hours for e in entries)
    total_overtime = sum(e.overtime_hours for e in entries)
    
    return {
        "employee_id": employee_id,
        "period": f"{start_date} to {end_date}",
        "total_hours": total_hours,
        "total_overtime": total_overtime,
        "entries": [
            {
                "id": e.id,
                "date": e.date.isoformat(),
                "clock_in": e.clock_in.isoformat() if e.clock_in else None,
                "clock_out": e.clock_out.isoformat() if e.clock_out else None,
                "total_hours": e.total_hours,
                "overtime_hours": e.overtime_hours,
                "is_approved": e.is_approved
            }
            for e in entries
        ]
    }


@router.post("/attendance/approve", tags=["Attendance"])
async def approve_timesheet(data: TimesheetApproval):
    """Approve timesheet entries for period."""
    agent = get_agent()
    count = agent.approve_timesheet(
        data.employee_id,
        data.start_date,
        data.end_date,
        data.approved_by
    )
    return {
        "employee_id": data.employee_id,
        "entries_approved": count,
        "message": f"Approved {count} timesheet entries"
    }


# =============================================================================
# BENEFITS ENDPOINTS
# =============================================================================

@router.post("/benefits/plans", tags=["Benefits"])
async def create_benefit_plan(data: BenefitPlanCreate, user_id: str = "hr"):
    """Create a benefit plan."""
    agent = get_agent()
    try:
        benefit_type = BenefitType(data.benefit_type)
        plan = agent.create_benefit_plan(
            name=data.name,
            benefit_type=benefit_type,
            provider=data.provider,
            employee_contribution=Decimal(str(data.employee_contribution)),
            employer_contribution=Decimal(str(data.employer_contribution)),
            description=data.description,
            coverage_details=data.coverage_details,
            created_by=user_id
        )
        return {
            "id": plan.id,
            "name": plan.name,
            "type": plan.benefit_type.value,
            "provider": plan.provider
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/benefits/plans", tags=["Benefits"])
async def list_benefit_plans():
    """List all benefit plans."""
    agent = get_agent()
    return {
        "plans": [
            {
                "id": p.id,
                "name": p.name,
                "type": p.benefit_type.value,
                "provider": p.provider,
                "employee_contribution": float(p.employee_contribution),
                "employer_contribution": float(p.employer_contribution),
                "is_active": p.is_active
            }
            for p in agent.benefit_plans.values()
        ]
    }


@router.post("/benefits/enroll", tags=["Benefits"])
async def enroll_in_benefit(data: BenefitEnrollment, user_id: str = "hr"):
    """Enroll employee in benefit plan."""
    agent = get_agent()
    try:
        enrollment = agent.enroll_in_benefit(
            employee_id=data.employee_id,
            plan_id=data.plan_id,
            coverage_level=data.coverage_level,
            effective_date=data.effective_date,
            dependents=data.dependents,
            created_by=user_id
        )
        return {
            "id": enrollment.id,
            "employee_id": enrollment.employee_id,
            "plan_id": enrollment.plan_id,
            "effective_date": enrollment.effective_date.isoformat(),
            "message": "Enrolled successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/benefits/employee/{employee_id}", tags=["Benefits"])
async def get_employee_benefits(employee_id: str):
    """Get all benefits for an employee."""
    agent = get_agent()
    benefits = agent.get_employee_benefits(employee_id)
    return {
        "employee_id": employee_id,
        "enrollments": benefits
    }


# =============================================================================
# COMPLIANCE ENDPOINTS
# =============================================================================

@router.post("/compliance", tags=["Compliance"])
async def add_compliance_requirement(data: ComplianceItemCreate, user_id: str = "hr"):
    """Add a compliance requirement for employee."""
    agent = get_agent()
    try:
        item = agent.add_compliance_requirement(
            employee_id=data.employee_id,
            name=data.name,
            category=data.category,
            due_date=data.due_date,
            is_mandatory=data.is_mandatory,
            description=data.description,
            created_by=user_id
        )
        return {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "status": item.status.value
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compliance/{item_id}/complete", tags=["Compliance"])
async def complete_compliance_item(item_id: str, data: ComplianceItemComplete):
    """Mark compliance item as completed."""
    agent = get_agent()
    try:
        item = agent.complete_compliance_item(
            item_id=item_id,
            document_url=data.document_url,
            verified_by=data.verified_by,
            expiry_date=data.expiry_date
        )
        return {
            "id": item.id,
            "status": item.status.value,
            "message": "Compliance item completed"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/compliance/employee/{employee_id}", tags=["Compliance"])
async def get_compliance_status(employee_id: str):
    """Get compliance status for employee."""
    agent = get_agent()
    try:
        return agent.get_compliance_status(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/compliance/expiring", tags=["Compliance"])
async def get_expiring_compliance(days_ahead: int = 30):
    """Get compliance items expiring soon."""
    agent = get_agent()
    items = agent.check_expiring_compliance(days_ahead)
    return {
        "days_ahead": days_ahead,
        "expiring_items": [
            {
                "id": i.id,
                "employee_id": i.employee_id,
                "name": i.name,
                "category": i.category,
                "expiry_date": i.expiry_date.isoformat() if i.expiry_date else None
            }
            for i in items
        ]
    }


# =============================================================================
# PAYROLL ENDPOINTS
# =============================================================================

@router.post("/payroll/generate", tags=["Payroll"])
async def generate_payroll(data: PayrollGenerate, user_id: str = "payroll"):
    """Generate payroll record for employee."""
    agent = get_agent()
    try:
        record = agent.generate_payroll(
            employee_id=data.employee_id,
            pay_period_start=data.pay_period_start,
            pay_period_end=data.pay_period_end,
            pay_date=data.pay_date,
            created_by=user_id
        )
        return {
            "id": record.id,
            "employee_id": record.employee_id,
            "pay_period": f"{record.pay_period_start} to {record.pay_period_end}",
            "gross_pay": float(record.gross_pay),
            "total_deductions": float(record.total_deductions),
            "net_pay": float(record.net_pay),
            "status": record.status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/payroll/{record_id}/process", tags=["Payroll"])
async def process_payroll(record_id: str):
    """Process payroll record (mark as paid)."""
    agent = get_agent()
    try:
        record = agent.process_payroll(record_id)
        return {
            "id": record.id,
            "status": record.status,
            "processed_at": record.processed_at.isoformat() if record.processed_at else None
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/payroll/pay-stubs/{employee_id}", tags=["Payroll"])
async def get_pay_stubs(employee_id: str, year: Optional[int] = None):
    """Get pay stubs for employee."""
    agent = get_agent()
    stubs = agent.get_pay_stubs(employee_id, year)
    return {
        "employee_id": employee_id,
        "year": year,
        "pay_stubs": [
            {
                "id": s.id,
                "pay_date": s.pay_date.isoformat(),
                "pay_period": f"{s.pay_period_start} to {s.pay_period_end}",
                "gross_pay": float(s.gross_pay),
                "net_pay": float(s.net_pay),
                "status": s.status
            }
            for s in stubs
        ]
    }


# =============================================================================
# AI ENDPOINTS
# =============================================================================

@router.get("/ai/attrition-risk/{employee_id}", tags=["AI"])
async def predict_attrition_risk(employee_id: str):
    """AI: Predict employee attrition risk."""
    agent = get_agent()
    try:
        return agent.predict_attrition_risk(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/ai/compensation-benchmark/{position_id}", tags=["AI"])
async def benchmark_compensation(position_id: str):
    """AI: Benchmark compensation for position."""
    agent = get_agent()
    try:
        return agent.benchmark_compensation(position_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/ai/skills-gap/{department_id}", tags=["AI"])
async def analyze_skills_gap(department_id: str):
    """AI: Analyze skills gap in department."""
    agent = get_agent()
    try:
        return agent.analyze_skills_gap(department_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =============================================================================
# ANALYTICS & DASHBOARD ENDPOINTS
# =============================================================================

@router.get("/analytics/workforce", tags=["Analytics"])
async def get_workforce_analytics():
    """Get overall workforce analytics."""
    agent = get_agent()
    return agent.get_workforce_analytics()


@router.get("/dashboard", tags=["Dashboard"])
async def get_dashboard(user_id: str = "admin", is_manager: bool = False):
    """Get HR dashboard data."""
    agent = get_agent()
    return agent.get_dashboard(user_id, is_manager)


@router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    agent = get_agent()
    return {
        "status": "healthy",
        "service": "HR & People Operations",
        "version": "V68",
        "stats": {
            "departments": len(agent.departments),
            "positions": len(agent.positions),
            "employees": len(agent.employees),
            "leave_requests": len(agent.leave_requests),
            "reviews": len(agent.reviews),
            "benefit_plans": len(agent.benefit_plans)
        }
    }
