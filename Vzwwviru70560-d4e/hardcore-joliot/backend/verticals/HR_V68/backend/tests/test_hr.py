"""
CHE·NU™ V68 — HR & PEOPLE OPERATIONS TESTS
Comprehensive test suite for HR Agent and API
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

# Import agent and routes
import sys
sys.path.insert(0, '/home/claude/HR_V68/backend')

from spheres.hr.agents.hr_agent import (
    HRAgent,
    EmploymentStatus,
    EmploymentType,
    LeaveType,
    LeaveStatus,
    ReviewStatus,
    ReviewType,
    BenefitType,
    OnboardingStatus,
    TaskStatus,
)
from spheres.hr.api.hr_routes import router


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def agent():
    """Create fresh HR agent for each test."""
    return HRAgent()


@pytest.fixture
def app():
    """Create FastAPI app with HR routes."""
    app = FastAPI()
    app.include_router(router, prefix="/api/v2/hr")
    return app


@pytest.fixture
def setup_basic_data(agent):
    """Setup basic test data: department, position, employee."""
    # Department
    dept = agent.create_department(
        name="Engineering",
        code="ENG",
        description="Software Engineering",
        budget=Decimal("1000000"),
        headcount_limit=50,
        created_by="test"
    )
    
    # Position
    position = agent.create_position(
        title="Software Developer",
        department_id=dept.id,
        level="Mid",
        salary_min=Decimal("60000"),
        salary_max=Decimal("90000"),
        requirements=["Python", "JavaScript"],
        created_by="test"
    )
    
    # Employee
    employee = agent.create_employee(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        position_id=position.id,
        department_id=dept.id,
        hire_date=date.today() - timedelta(days=180),
        salary=Decimal("75000"),
        created_by="test"
    )
    
    # Activate
    agent.update_employee_status(employee.id, EmploymentStatus.ACTIVE, "test")
    
    # Setup leave policies
    agent.setup_default_leave_policies("test")
    
    # Accrue some PTO
    agent.accrue_pto(employee.id, LeaveType.VACATION, 10.0)
    agent.accrue_pto(employee.id, LeaveType.SICK, 5.0)
    
    return {"department": dept, "position": position, "employee": employee}


# =============================================================================
# DEPARTMENT TESTS
# =============================================================================

class TestDepartments:
    """Test department management."""
    
    def test_create_department(self, agent):
        """Test creating a department."""
        dept = agent.create_department(
            name="Sales",
            code="SLS",
            description="Sales Team",
            budget=Decimal("500000"),
            headcount_limit=20,
            created_by="test"
        )
        
        assert dept.name == "Sales"
        assert dept.code == "SLS"
        assert dept.budget == Decimal("500000")
    
    def test_prevent_duplicate_department_code(self, agent):
        """Test that duplicate department codes are prevented."""
        agent.create_department(name="Dept1", code="D01", created_by="test")
        
        with pytest.raises(ValueError) as exc:
            agent.create_department(name="Dept2", code="D01", created_by="test")
        
        assert "already exists" in str(exc.value)
    
    def test_org_chart(self, agent):
        """Test org chart generation."""
        # Create parent
        parent = agent.create_department(name="Company", code="CO", created_by="test")
        
        # Create children
        agent.create_department(
            name="Engineering",
            code="ENG",
            parent_department_id=parent.id,
            created_by="test"
        )
        agent.create_department(
            name="Sales",
            code="SLS",
            parent_department_id=parent.id,
            created_by="test"
        )
        
        chart = agent.get_org_chart()
        
        assert "departments" in chart
        assert len(chart["departments"]) == 1  # Top-level
        assert len(chart["departments"][0]["children"]) == 2  # Children


class TestPositions:
    """Test position management."""
    
    def test_create_position(self, agent):
        """Test creating a position."""
        dept = agent.create_department(name="IT", code="IT", created_by="test")
        
        position = agent.create_position(
            title="DevOps Engineer",
            department_id=dept.id,
            level="Senior",
            salary_min=Decimal("80000"),
            salary_max=Decimal("120000"),
            requirements=["AWS", "Kubernetes", "Python"],
            created_by="test"
        )
        
        assert position.title == "DevOps Engineer"
        assert position.level == "Senior"
        assert "AWS" in position.requirements
    
    def test_position_requires_valid_department(self, agent):
        """Test that position requires valid department."""
        with pytest.raises(ValueError):
            agent.create_position(
                title="Test",
                department_id="invalid-id",
                level="Mid",
                salary_min=Decimal("50000"),
                salary_max=Decimal("70000"),
                created_by="test"
            )


# =============================================================================
# EMPLOYEE TESTS
# =============================================================================

class TestEmployees:
    """Test employee management."""
    
    def test_create_employee(self, agent, setup_basic_data):
        """Test employee is created with correct data."""
        emp = setup_basic_data["employee"]
        
        assert emp.first_name == "John"
        assert emp.last_name == "Doe"
        assert emp.employee_number.startswith("EMP")
        assert emp.employment_status == EmploymentStatus.ACTIVE
    
    def test_employee_number_generation(self, agent, setup_basic_data):
        """Test employee numbers are unique and sequential."""
        data = setup_basic_data
        
        emp2 = agent.create_employee(
            first_name="Jane",
            last_name="Smith",
            email="jane@test.com",
            position_id=data["position"].id,
            department_id=data["department"].id,
            hire_date=date.today(),
            salary=Decimal("70000"),
            created_by="test"
        )
        
        # First employee is EMP00001, second is EMP00002
        assert emp2.employee_number == "EMP00002"
    
    def test_prevent_duplicate_email(self, agent, setup_basic_data):
        """Test duplicate email prevention."""
        data = setup_basic_data
        
        with pytest.raises(ValueError) as exc:
            agent.create_employee(
                first_name="Another",
                last_name="Person",
                email="john@test.com",  # Duplicate
                position_id=data["position"].id,
                department_id=data["department"].id,
                hire_date=date.today(),
                salary=Decimal("60000"),
                created_by="test"
            )
        
        assert "already exists" in str(exc.value)
    
    def test_onboarding_auto_created(self, agent, setup_basic_data):
        """Test that onboarding checklist is auto-created."""
        emp = setup_basic_data["employee"]
        checklist = agent.get_onboarding(emp.id)
        
        assert checklist is not None
        assert checklist.employee_id == emp.id
        assert len(checklist.tasks) > 0
    
    def test_update_employee_status(self, agent, setup_basic_data):
        """Test status update."""
        emp = setup_basic_data["employee"]
        
        agent.update_employee_status(emp.id, EmploymentStatus.ON_LEAVE, "hr")
        
        updated = agent.get_employee(emp.id)
        assert updated.employment_status == EmploymentStatus.ON_LEAVE
    
    def test_salary_update(self, agent, setup_basic_data):
        """Test salary update."""
        emp = setup_basic_data["employee"]
        original = emp.salary
        
        agent.update_salary(
            employee_id=emp.id,
            new_salary=Decimal("85000"),
            effective_date=date.today(),
            updated_by="manager",
            reason="Annual increase"
        )
        
        updated = agent.get_employee(emp.id)
        assert updated.salary == Decimal("85000")
        assert updated.salary > original
    
    def test_search_employees(self, agent, setup_basic_data):
        """Test employee search."""
        results = agent.search_employees("John")
        assert len(results) == 1
        assert results[0].first_name == "John"
        
        results = agent.search_employees("EMP")
        assert len(results) >= 1
    
    def test_get_direct_reports(self, agent, setup_basic_data):
        """Test getting direct reports."""
        data = setup_basic_data
        
        # Create manager
        manager = agent.create_employee(
            first_name="Manager",
            last_name="Person",
            email="manager@test.com",
            position_id=data["position"].id,
            department_id=data["department"].id,
            hire_date=date.today(),
            salary=Decimal("100000"),
            manager_id=None,
            created_by="test"
        )
        
        # Update employee to report to manager
        data["employee"].manager_id = manager.id
        
        reports = agent.get_direct_reports(manager.id)
        assert len(reports) == 1
        assert reports[0].id == data["employee"].id


# =============================================================================
# LEAVE / PTO TESTS
# =============================================================================

class TestLeave:
    """Test leave management."""
    
    def test_setup_default_policies(self, agent):
        """Test default leave policies creation."""
        policies = agent.setup_default_leave_policies("test")
        
        assert len(policies) >= 3  # Vacation, Sick, Personal at minimum
        
        vacation = next((p for p in policies if p.leave_type == LeaveType.VACATION), None)
        assert vacation is not None
        assert vacation.days_per_year > 0
    
    def test_pto_accrual(self, agent, setup_basic_data):
        """Test PTO accrual."""
        emp = setup_basic_data["employee"]
        
        balance = agent.get_leave_balance(emp.id)
        assert balance["vacation"] == 10.0  # From fixture
    
    def test_request_leave(self, agent, setup_basic_data):
        """Test leave request creation."""
        emp = setup_basic_data["employee"]
        
        request = agent.request_leave(
            employee_id=emp.id,
            leave_type=LeaveType.VACATION,
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=32),
            reason="Family vacation",
            created_by=emp.id
        )
        
        assert request.status == LeaveStatus.PENDING
        assert request.days_requested > 0
    
    def test_insufficient_balance(self, agent, setup_basic_data):
        """Test leave request with insufficient balance."""
        emp = setup_basic_data["employee"]
        
        with pytest.raises(ValueError) as exc:
            agent.request_leave(
                employee_id=emp.id,
                leave_type=LeaveType.VACATION,
                start_date=date.today() + timedelta(days=30),
                end_date=date.today() + timedelta(days=60),  # 30+ days
                reason="Long vacation",
                created_by=emp.id
            )
        
        assert "Insufficient" in str(exc.value)
    
    def test_approve_leave(self, agent, setup_basic_data):
        """Test leave approval."""
        emp = setup_basic_data["employee"]
        
        request = agent.request_leave(
            employee_id=emp.id,
            leave_type=LeaveType.VACATION,
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=32),
            reason="Vacation",
            created_by=emp.id
        )
        
        approved = agent.approve_leave(request.id, "manager")
        
        assert approved.status == LeaveStatus.APPROVED
        
        # Check balance was deducted
        balance = agent.get_leave_balance(emp.id)
        assert balance["vacation"] < 10.0
    
    def test_reject_leave(self, agent, setup_basic_data):
        """Test leave rejection."""
        emp = setup_basic_data["employee"]
        
        request = agent.request_leave(
            employee_id=emp.id,
            leave_type=LeaveType.VACATION,
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=32),
            reason="Vacation",
            created_by=emp.id
        )
        
        rejected = agent.reject_leave(request.id, "manager", "Team needs coverage")
        
        assert rejected.status == LeaveStatus.REJECTED
        assert "coverage" in rejected.rejection_reason


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance:
    """Test performance management."""
    
    def test_create_goal(self, agent, setup_basic_data):
        """Test goal creation."""
        emp = setup_basic_data["employee"]
        
        goal = agent.create_goal(
            employee_id=emp.id,
            title="Complete AWS Certification",
            description="Obtain AWS Solutions Architect certification",
            key_results=["Pass exam", "Apply learnings to project"],
            target_date=date.today() + timedelta(days=90),
            created_by=emp.id
        )
        
        assert goal.title == "Complete AWS Certification"
        assert goal.progress == 0.0
        assert goal.status == "active"
    
    def test_update_goal_progress(self, agent, setup_basic_data):
        """Test goal progress update."""
        emp = setup_basic_data["employee"]
        
        goal = agent.create_goal(
            employee_id=emp.id,
            title="Test Goal",
            created_by=emp.id
        )
        
        agent.update_goal_progress(goal.id, 50.0, emp.id)
        
        updated = agent.goals[goal.id]
        assert updated.progress == 50.0
    
    def test_goal_auto_complete(self, agent, setup_basic_data):
        """Test goal auto-completes at 100%."""
        emp = setup_basic_data["employee"]
        
        goal = agent.create_goal(
            employee_id=emp.id,
            title="Test Goal",
            created_by=emp.id
        )
        
        agent.update_goal_progress(goal.id, 100.0, emp.id)
        
        updated = agent.goals[goal.id]
        assert updated.status == "completed"
    
    def test_create_performance_review(self, agent, setup_basic_data):
        """Test performance review creation."""
        emp = setup_basic_data["employee"]
        
        # Create manager
        manager = agent.create_employee(
            first_name="Manager",
            last_name="Test",
            email="mgr@test.com",
            position_id=setup_basic_data["position"].id,
            department_id=setup_basic_data["department"].id,
            hire_date=date.today(),
            salary=Decimal("100000"),
            created_by="test"
        )
        
        review = agent.create_performance_review(
            employee_id=emp.id,
            reviewer_id=manager.id,
            review_type=ReviewType.ANNUAL,
            review_period_start=date.today() - timedelta(days=365),
            review_period_end=date.today(),
            scheduled_date=date.today() + timedelta(days=7),
            created_by="hr"
        )
        
        assert review.status == ReviewStatus.SCHEDULED
        assert review.review_type == ReviewType.ANNUAL
    
    def test_complete_review(self, agent, setup_basic_data):
        """Test completing a review."""
        emp = setup_basic_data["employee"]
        
        manager = agent.create_employee(
            first_name="Manager",
            last_name="Test",
            email="mgr2@test.com",
            position_id=setup_basic_data["position"].id,
            department_id=setup_basic_data["department"].id,
            hire_date=date.today(),
            salary=Decimal("100000"),
            created_by="test"
        )
        
        review = agent.create_performance_review(
            employee_id=emp.id,
            reviewer_id=manager.id,
            review_type=ReviewType.ANNUAL,
            review_period_start=date.today() - timedelta(days=365),
            review_period_end=date.today(),
            scheduled_date=date.today(),
            created_by="hr"
        )
        
        completed = agent.complete_review(
            review_id=review.id,
            overall_rating=4.2,
            ratings={"communication": 4.5, "technical": 4.0, "teamwork": 4.0},
            strengths=["Strong problem solver", "Good communicator"],
            areas_for_improvement=["Time management"],
            reviewer_comments="Excellent year overall",
            salary_increase_recommended=True,
            recommended_increase_percent=5.0,
            completed_by=manager.id
        )
        
        assert completed.status == ReviewStatus.COMPLETED
        assert completed.overall_rating == 4.2
        assert completed.salary_increase_recommended is True


# =============================================================================
# ONBOARDING TESTS
# =============================================================================

class TestOnboarding:
    """Test onboarding functionality."""
    
    def test_onboarding_checklist_exists(self, agent, setup_basic_data):
        """Test onboarding checklist auto-creation."""
        emp = setup_basic_data["employee"]
        checklist = agent.get_onboarding(emp.id)
        
        assert checklist is not None
        assert checklist.status == OnboardingStatus.NOT_STARTED
        assert len(checklist.tasks) >= 10  # Default tasks
    
    def test_complete_onboarding_task(self, agent, setup_basic_data):
        """Test completing an onboarding task."""
        emp = setup_basic_data["employee"]
        checklist = agent.get_onboarding(emp.id)
        
        task = checklist.tasks[0]
        
        updated = agent.complete_onboarding_task(
            checklist_id=checklist.id,
            task_id=task.id,
            completed_by="hr",
            notes="Completed successfully"
        )
        
        assert updated.progress_percent > 0
        assert updated.status == OnboardingStatus.IN_PROGRESS
    
    def test_onboarding_progress_tracking(self, agent, setup_basic_data):
        """Test progress percentage calculation."""
        emp = setup_basic_data["employee"]
        checklist = agent.get_onboarding(emp.id)
        
        total_tasks = len(checklist.tasks)
        
        # Complete half the tasks
        for task in checklist.tasks[:total_tasks // 2]:
            agent.complete_onboarding_task(
                checklist_id=checklist.id,
                task_id=task.id,
                completed_by="hr"
            )
        
        updated = agent.get_onboarding(emp.id)
        assert updated.progress_percent >= 40  # Approximately half


# =============================================================================
# ATTENDANCE TESTS
# =============================================================================

class TestAttendance:
    """Test attendance/time tracking."""
    
    def test_clock_in(self, agent, setup_basic_data):
        """Test clock in."""
        emp = setup_basic_data["employee"]
        
        entry = agent.clock_in(emp.id, emp.id)
        
        assert entry.employee_id == emp.id
        assert entry.clock_in is not None
        assert entry.clock_out is None
    
    def test_prevent_double_clock_in(self, agent, setup_basic_data):
        """Test prevention of double clock in."""
        emp = setup_basic_data["employee"]
        
        agent.clock_in(emp.id, emp.id)
        
        with pytest.raises(ValueError) as exc:
            agent.clock_in(emp.id, emp.id)
        
        assert "Already clocked in" in str(exc.value)
    
    def test_clock_out(self, agent, setup_basic_data):
        """Test clock out."""
        emp = setup_basic_data["employee"]
        
        agent.clock_in(emp.id, emp.id)
        entry = agent.clock_out(emp.id, break_minutes=30)
        
        assert entry.clock_out is not None
        assert entry.break_minutes == 30
        assert entry.total_hours >= 0
    
    def test_timesheet_approval(self, agent, setup_basic_data):
        """Test timesheet approval."""
        emp = setup_basic_data["employee"]
        
        agent.clock_in(emp.id, emp.id)
        agent.clock_out(emp.id)
        
        count = agent.approve_timesheet(
            emp.id,
            date.today(),
            date.today(),
            "manager"
        )
        
        assert count == 1


# =============================================================================
# BENEFITS TESTS
# =============================================================================

class TestBenefits:
    """Test benefits management."""
    
    def test_create_benefit_plan(self, agent):
        """Test benefit plan creation."""
        plan = agent.create_benefit_plan(
            name="Health Insurance Premium",
            benefit_type=BenefitType.HEALTH,
            provider="Blue Cross",
            employee_contribution=Decimal("150"),
            employer_contribution=Decimal("350"),
            description="Comprehensive health coverage",
            created_by="hr"
        )
        
        assert plan.name == "Health Insurance Premium"
        assert plan.benefit_type == BenefitType.HEALTH
    
    def test_enroll_in_benefit(self, agent, setup_basic_data):
        """Test benefit enrollment."""
        emp = setup_basic_data["employee"]
        
        plan = agent.create_benefit_plan(
            name="Dental Plan",
            benefit_type=BenefitType.DENTAL,
            provider="Sun Life",
            employee_contribution=Decimal("25"),
            employer_contribution=Decimal("75"),
            created_by="hr"
        )
        
        enrollment = agent.enroll_in_benefit(
            employee_id=emp.id,
            plan_id=plan.id,
            coverage_level="family",
            effective_date=date.today(),
            dependents=[{"name": "Spouse", "relationship": "spouse", "dob": "1990-01-01"}],
            created_by="hr"
        )
        
        assert enrollment.coverage_level == "family"
        assert len(enrollment.dependents) == 1
    
    def test_get_employee_benefits(self, agent, setup_basic_data):
        """Test getting employee benefits."""
        emp = setup_basic_data["employee"]
        
        # Create and enroll in plans
        health = agent.create_benefit_plan(
            name="Health",
            benefit_type=BenefitType.HEALTH,
            provider="Provider",
            employee_contribution=Decimal("100"),
            employer_contribution=Decimal("300"),
            created_by="hr"
        )
        
        agent.enroll_in_benefit(
            employee_id=emp.id,
            plan_id=health.id,
            coverage_level="employee_only",
            effective_date=date.today(),
            created_by="hr"
        )
        
        benefits = agent.get_employee_benefits(emp.id)
        assert len(benefits) == 1
        assert benefits[0]["plan_name"] == "Health"


# =============================================================================
# COMPLIANCE TESTS
# =============================================================================

class TestCompliance:
    """Test compliance management."""
    
    def test_add_compliance_requirement(self, agent, setup_basic_data):
        """Test adding compliance requirement."""
        emp = setup_basic_data["employee"]
        
        item = agent.add_compliance_requirement(
            employee_id=emp.id,
            name="Safety Training",
            category="training",
            due_date=date.today() + timedelta(days=30),
            is_mandatory=True,
            created_by="hr"
        )
        
        assert item.name == "Safety Training"
        assert item.is_mandatory is True
    
    def test_complete_compliance_item(self, agent, setup_basic_data):
        """Test completing compliance item."""
        emp = setup_basic_data["employee"]
        
        item = agent.add_compliance_requirement(
            employee_id=emp.id,
            name="Background Check",
            category="document",
            created_by="hr"
        )
        
        completed = agent.complete_compliance_item(
            item_id=item.id,
            document_url="https://example.com/doc.pdf",
            verified_by="hr"
        )
        
        assert completed.status.value == "approved"
    
    def test_compliance_status(self, agent, setup_basic_data):
        """Test compliance status summary."""
        emp = setup_basic_data["employee"]
        
        # Add multiple items
        agent.add_compliance_requirement(
            employee_id=emp.id,
            name="Item 1",
            category="document",
            is_mandatory=True,
            created_by="hr"
        )
        
        item2 = agent.add_compliance_requirement(
            employee_id=emp.id,
            name="Item 2",
            category="training",
            is_mandatory=True,
            created_by="hr"
        )
        
        # Complete one
        agent.complete_compliance_item(item2.id, verified_by="hr")
        
        status = agent.get_compliance_status(emp.id)
        
        assert status["total_required"] == 2
        assert status["completed"] == 1
        assert status["compliance_rate"] == 50.0


# =============================================================================
# PAYROLL TESTS
# =============================================================================

class TestPayroll:
    """Test payroll functionality."""
    
    def test_generate_payroll(self, agent, setup_basic_data):
        """Test payroll generation."""
        emp = setup_basic_data["employee"]
        
        # Clock in/out for some time entries
        entry = agent.clock_in(emp.id, emp.id)
        agent.clock_out(emp.id)
        
        record = agent.generate_payroll(
            employee_id=emp.id,
            pay_period_start=date.today() - timedelta(days=14),
            pay_period_end=date.today(),
            pay_date=date.today() + timedelta(days=5),
            created_by="payroll"
        )
        
        assert record.employee_id == emp.id
        assert record.gross_pay > 0
        assert record.net_pay > 0
        assert record.net_pay < record.gross_pay  # Deductions applied
    
    def test_payroll_deductions(self, agent, setup_basic_data):
        """Test that payroll includes deductions."""
        emp = setup_basic_data["employee"]
        
        record = agent.generate_payroll(
            employee_id=emp.id,
            pay_period_start=date.today() - timedelta(days=14),
            pay_period_end=date.today(),
            pay_date=date.today() + timedelta(days=5),
            created_by="payroll"
        )
        
        # Should have Canadian deductions
        assert record.federal_tax > 0
        assert record.provincial_tax > 0
        assert record.cpp_contribution > 0
        assert record.ei_contribution > 0
    
    def test_process_payroll(self, agent, setup_basic_data):
        """Test processing payroll."""
        emp = setup_basic_data["employee"]
        
        record = agent.generate_payroll(
            employee_id=emp.id,
            pay_period_start=date.today() - timedelta(days=14),
            pay_period_end=date.today(),
            pay_date=date.today(),
            created_by="payroll"
        )
        
        processed = agent.process_payroll(record.id)
        
        assert processed.status == "processed"
        assert processed.processed_at is not None


# =============================================================================
# AI TESTS
# =============================================================================

class TestAI:
    """Test AI features."""
    
    def test_attrition_prediction(self, agent, setup_basic_data):
        """Test attrition risk prediction."""
        emp = setup_basic_data["employee"]
        
        result = agent.predict_attrition_risk(emp.id)
        
        assert "risk_score" in result
        assert "risk_level" in result
        assert result["risk_level"] in ["low", "medium", "high"]
        assert "recommendations" in result
    
    def test_compensation_benchmark(self, agent, setup_basic_data):
        """Test compensation benchmarking."""
        data = setup_basic_data
        
        result = agent.benchmark_compensation(data["position"].id)
        
        assert "position" in result
        assert "current_salaries" in result
        assert "salary_band" in result
    
    def test_skills_gap_analysis(self, agent, setup_basic_data):
        """Test skills gap analysis."""
        dept = setup_basic_data["department"]
        
        result = agent.analyze_skills_gap(dept.id)
        
        assert "department" in result
        assert "required_skills" in result


# =============================================================================
# ANALYTICS TESTS
# =============================================================================

class TestAnalytics:
    """Test analytics and dashboard."""
    
    def test_workforce_analytics(self, agent, setup_basic_data):
        """Test workforce analytics."""
        analytics = agent.get_workforce_analytics()
        
        assert "total_employees" in analytics
        assert "active_employees" in analytics
        assert "by_department" in analytics
        assert "tenure_distribution" in analytics
    
    def test_dashboard(self, agent, setup_basic_data):
        """Test dashboard data."""
        dashboard = agent.get_dashboard("admin", is_manager=True)
        
        assert "analytics" in dashboard
        assert "pending_items" in dashboard
        assert "quick_stats" in dashboard


# =============================================================================
# API ENDPOINT TESTS
# =============================================================================

class TestAPIEndpoints:
    """Test API endpoints."""
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, app):
        """Test health check endpoint."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v2/hr/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_create_department_endpoint(self, app):
        """Test department creation endpoint."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v2/hr/departments",
                json={
                    "name": "Marketing",
                    "code": "MKT",
                    "description": "Marketing Department",
                    "budget": 500000,
                    "headcount_limit": 15
                }
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Marketing"
        assert data["code"] == "MKT"
    
    @pytest.mark.asyncio
    async def test_setup_leave_policies_endpoint(self, app):
        """Test default leave policies setup endpoint."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/api/v2/hr/leave/policies/setup-defaults")
        
        assert response.status_code == 200
        data = response.json()
        assert "policies" in data
        assert len(data["policies"]) >= 3
    
    @pytest.mark.asyncio
    async def test_dashboard_endpoint(self, app):
        """Test dashboard endpoint."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v2/hr/dashboard")
        
        assert response.status_code == 200
        data = response.json()
        assert "analytics" in data
        assert "quick_stats" in data
    
    @pytest.mark.asyncio
    async def test_workforce_analytics_endpoint(self, app):
        """Test workforce analytics endpoint."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v2/hr/analytics/workforce")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_employees" in data


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
