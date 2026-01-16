"""
CHE·NU™ V68 - Project Management Tests
Comprehensive test coverage for PM vertical
"""

import pytest
from datetime import date, datetime, timedelta
from decimal import Decimal
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spheres.projects.agents.project_agent import (
    ProjectManagementService, ProjectAIEngine,
    Project, Task, Sprint, Milestone, TimeEntry, TeamMember, Comment,
    ProjectStatus, TaskStatus, TaskPriority, SprintStatus, MilestoneStatus,
    RiskLevel
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def service():
    """Fresh PM service instance"""
    return ProjectManagementService()


@pytest.fixture
def ai_engine():
    """AI engine instance"""
    return ProjectAIEngine()


@pytest.fixture
def user_id():
    """Test user ID"""
    return "test_user_123"


@pytest.fixture
def sample_project(service, user_id):
    """Create a sample project"""
    return service.create_project(
        user_id=user_id,
        name="Test Project",
        description="Test description",
        target_date=date.today() + timedelta(days=30),
        budget=Decimal("10000"),
        tags=["test", "development"]
    )


@pytest.fixture
def sample_team(service, sample_project, user_id):
    """Create sample team members"""
    members = []
    members.append(service.add_team_member(
        sample_project.id, user_id, "Alice", "alice@test.com", "lead",
        hourly_rate=Decimal("75"), capacity=Decimal("40")
    ))
    members.append(service.add_team_member(
        sample_project.id, user_id, "Bob", "bob@test.com", "developer",
        hourly_rate=Decimal("60"), capacity=Decimal("40")
    ))
    return members


@pytest.fixture
def sample_sprint(service, sample_project, user_id):
    """Create a sample sprint"""
    return service.create_sprint(
        sample_project.id, user_id, "Sprint 1",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=14),
        goal="Complete MVP",
        velocity_planned=20
    )


@pytest.fixture
def sample_tasks(service, sample_project, sample_sprint, sample_team, user_id):
    """Create sample tasks"""
    tasks = []
    tasks.append(service.create_task(
        sample_project.id, user_id, "Task 1",
        priority=TaskPriority.HIGH,
        assignee_id=sample_team[0].id,
        assignee_name=sample_team[0].name,
        sprint_id=sample_sprint.id,
        estimated_hours=Decimal("8"),
        due_date=date.today() + timedelta(days=7)
    ))
    tasks.append(service.create_task(
        sample_project.id, user_id, "Task 2",
        priority=TaskPriority.MEDIUM,
        assignee_id=sample_team[1].id,
        assignee_name=sample_team[1].name,
        sprint_id=sample_sprint.id,
        estimated_hours=Decimal("4"),
        due_date=date.today() + timedelta(days=5)
    ))
    tasks.append(service.create_task(
        sample_project.id, user_id, "Task 3",
        priority=TaskPriority.LOW,
        estimated_hours=Decimal("2")
    ))
    return tasks


# ============================================================================
# PROJECT TESTS
# ============================================================================

class TestProjectOperations:
    """Test project CRUD operations"""
    
    def test_create_project(self, service, user_id):
        """Test project creation"""
        project = service.create_project(
            user_id=user_id,
            name="New Project",
            description="Description",
            budget=Decimal("5000")
        )
        
        assert project is not None
        assert project.id is not None
        assert project.name == "New Project"
        assert project.status == ProjectStatus.PLANNING
        assert project.budget == Decimal("5000")
        assert project.spent == Decimal("0")
    
    def test_get_project(self, service, sample_project, user_id):
        """Test getting project by ID"""
        retrieved = service.get_project(sample_project.id, user_id)
        
        assert retrieved is not None
        assert retrieved.id == sample_project.id
        assert retrieved.name == sample_project.name
    
    def test_get_project_wrong_user(self, service, sample_project):
        """Test access control - wrong user"""
        retrieved = service.get_project(sample_project.id, "other_user")
        
        assert retrieved is None
    
    def test_list_projects(self, service, user_id):
        """Test listing projects"""
        # Create multiple projects
        service.create_project(user_id, "Project A")
        service.create_project(user_id, "Project B")
        service.create_project(user_id, "Project C")
        
        projects = service.list_projects(user_id)
        
        assert len(projects) == 3
    
    def test_list_projects_with_status_filter(self, service, user_id):
        """Test filtering projects by status"""
        p1 = service.create_project(user_id, "Project A")
        p2 = service.create_project(user_id, "Project B")
        
        # Update one to active
        service.update_project(p1.id, user_id, {'status': ProjectStatus.ACTIVE})
        
        active = service.list_projects(user_id, status=ProjectStatus.ACTIVE)
        planning = service.list_projects(user_id, status=ProjectStatus.PLANNING)
        
        assert len(active) == 1
        assert len(planning) == 1
    
    def test_update_project(self, service, sample_project, user_id):
        """Test updating project"""
        updated = service.update_project(sample_project.id, user_id, {
            'name': 'Updated Name',
            'status': ProjectStatus.ACTIVE,
            'budget': Decimal("15000")
        })
        
        assert updated.name == 'Updated Name'
        assert updated.status == ProjectStatus.ACTIVE
        assert updated.budget == Decimal("15000")
    
    def test_search_projects(self, service, user_id):
        """Test searching projects"""
        service.create_project(user_id, "Website Redesign", "Redesign corporate website")
        service.create_project(user_id, "Mobile App", "iOS and Android app")
        
        results = service.list_projects(user_id, search="website")
        
        assert len(results) == 1
        assert "Website" in results[0].name


# ============================================================================
# TASK TESTS
# ============================================================================

class TestTaskOperations:
    """Test task CRUD operations"""
    
    def test_create_task(self, service, sample_project, user_id):
        """Test task creation"""
        task = service.create_task(
            sample_project.id, user_id, "New Task",
            description="Task description",
            priority=TaskPriority.HIGH,
            estimated_hours=Decimal("6")
        )
        
        assert task is not None
        assert task.title == "New Task"
        assert task.status == TaskStatus.BACKLOG
        assert task.priority == TaskPriority.HIGH
        assert task.estimated_hours == Decimal("6")
    
    def test_list_tasks(self, service, sample_project, sample_tasks, user_id):
        """Test listing tasks"""
        tasks = service.list_tasks(sample_project.id, user_id)
        
        assert len(tasks) == 3
    
    def test_list_tasks_by_status(self, service, sample_project, sample_tasks, user_id):
        """Test filtering tasks by status"""
        # Move one task
        service.move_task(sample_tasks[0].id, user_id, TaskStatus.IN_PROGRESS)
        
        in_progress = service.list_tasks(
            sample_project.id, user_id, status=TaskStatus.IN_PROGRESS
        )
        backlog = service.list_tasks(
            sample_project.id, user_id, status=TaskStatus.BACKLOG
        )
        
        assert len(in_progress) == 1
        assert len(backlog) == 2
    
    def test_list_tasks_by_assignee(self, service, sample_project, sample_tasks, sample_team, user_id):
        """Test filtering tasks by assignee"""
        alice_tasks = service.list_tasks(
            sample_project.id, user_id, assignee_id=sample_team[0].id
        )
        
        assert len(alice_tasks) == 1
        assert alice_tasks[0].assignee_name == "Alice"
    
    def test_update_task(self, service, sample_tasks, user_id):
        """Test updating task"""
        updated = service.update_task(sample_tasks[0].id, user_id, {
            'title': 'Updated Title',
            'priority': TaskPriority.CRITICAL
        })
        
        assert updated.title == 'Updated Title'
        assert updated.priority == TaskPriority.CRITICAL
    
    def test_move_task_kanban(self, service, sample_tasks, user_id):
        """Test moving task through Kanban"""
        task = sample_tasks[0]
        
        # Move through workflow
        service.move_task(task.id, user_id, TaskStatus.TODO)
        service.move_task(task.id, user_id, TaskStatus.IN_PROGRESS)
        service.move_task(task.id, user_id, TaskStatus.IN_REVIEW)
        task = service.move_task(task.id, user_id, TaskStatus.DONE)
        
        assert task.status == TaskStatus.DONE
        assert task.completed_at is not None
    
    def test_task_completion_tracking(self, service, sample_tasks, user_id):
        """Test completion timestamp tracking"""
        task = sample_tasks[0]
        
        # Complete task
        service.move_task(task.id, user_id, TaskStatus.DONE)
        task = service.get_task(task.id, user_id)
        assert task.completed_at is not None
        
        # Reopen task
        service.move_task(task.id, user_id, TaskStatus.IN_PROGRESS)
        task = service.get_task(task.id, user_id)
        assert task.completed_at is None
    
    def test_subtasks(self, service, sample_project, sample_tasks, user_id):
        """Test subtask creation"""
        parent = sample_tasks[0]
        
        subtask = service.create_task(
            sample_project.id, user_id, "Subtask 1",
            parent_task_id=parent.id
        )
        
        assert subtask.parent_task_id == parent.id
    
    def test_task_with_checklist(self, service, sample_tasks, user_id):
        """Test task checklist"""
        checklist = [
            {"id": "1", "text": "Step 1", "completed": False},
            {"id": "2", "text": "Step 2", "completed": True}
        ]
        
        updated = service.update_task(sample_tasks[0].id, user_id, {
            'checklist': checklist
        })
        
        assert len(updated.checklist) == 2
        assert updated.checklist[1]['completed'] == True


# ============================================================================
# SPRINT TESTS
# ============================================================================

class TestSprintOperations:
    """Test sprint operations"""
    
    def test_create_sprint(self, service, sample_project, user_id):
        """Test sprint creation"""
        sprint = service.create_sprint(
            sample_project.id, user_id, "Sprint 1",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=14),
            goal="Complete features",
            velocity_planned=25
        )
        
        assert sprint is not None
        assert sprint.name == "Sprint 1"
        assert sprint.status == SprintStatus.PLANNED
        assert sprint.velocity_planned == 25
    
    def test_list_sprints(self, service, sample_project, user_id):
        """Test listing sprints"""
        service.create_sprint(sample_project.id, user_id, "Sprint 1",
                             date.today(), date.today() + timedelta(14))
        service.create_sprint(sample_project.id, user_id, "Sprint 2",
                             date.today() + timedelta(14), date.today() + timedelta(28))
        
        sprints = service.list_sprints(sample_project.id, user_id)
        
        assert len(sprints) == 2
    
    def test_start_sprint(self, service, sample_sprint, user_id):
        """Test starting a sprint"""
        sprint = service.start_sprint(sample_sprint.id, user_id)
        
        assert sprint.status == SprintStatus.ACTIVE
    
    def test_complete_sprint(self, service, sample_project, sample_sprint, sample_tasks, user_id):
        """Test completing a sprint with velocity calculation"""
        # Start sprint
        service.start_sprint(sample_sprint.id, user_id)
        
        # Complete some tasks
        service.move_task(sample_tasks[0].id, user_id, TaskStatus.DONE)
        service.move_task(sample_tasks[1].id, user_id, TaskStatus.DONE)
        
        # Complete sprint
        sprint = service.complete_sprint(sample_sprint.id, user_id)
        
        assert sprint.status == SprintStatus.COMPLETED
        assert sprint.velocity_actual == 2  # 2 tasks completed


# ============================================================================
# MILESTONE TESTS
# ============================================================================

class TestMilestoneOperations:
    """Test milestone operations"""
    
    def test_create_milestone(self, service, sample_project, user_id):
        """Test milestone creation"""
        milestone = service.create_milestone(
            sample_project.id, user_id, "MVP Launch",
            due_date=date.today() + timedelta(days=30),
            description="First release",
            deliverables=["Feature A", "Feature B"]
        )
        
        assert milestone is not None
        assert milestone.name == "MVP Launch"
        assert milestone.status == MilestoneStatus.UPCOMING
        assert len(milestone.deliverables) == 2
    
    def test_list_milestones(self, service, sample_project, user_id):
        """Test listing milestones sorted by date"""
        service.create_milestone(sample_project.id, user_id, "M1",
                                date.today() + timedelta(30))
        service.create_milestone(sample_project.id, user_id, "M2",
                                date.today() + timedelta(15))
        service.create_milestone(sample_project.id, user_id, "M3",
                                date.today() + timedelta(45))
        
        milestones = service.list_milestones(sample_project.id, user_id)
        
        assert len(milestones) == 3
        # Should be sorted by due date
        assert milestones[0].name == "M2"
        assert milestones[1].name == "M1"
        assert milestones[2].name == "M3"
    
    def test_complete_milestone(self, service, sample_project, user_id):
        """Test completing a milestone"""
        milestone = service.create_milestone(
            sample_project.id, user_id, "Milestone",
            due_date=date.today() + timedelta(7)
        )
        
        completed = service.complete_milestone(milestone.id, user_id)
        
        assert completed.status == MilestoneStatus.COMPLETED
        assert completed.completed_date == date.today()


# ============================================================================
# TIME TRACKING TESTS
# ============================================================================

class TestTimeTracking:
    """Test time tracking operations"""
    
    def test_log_time(self, service, sample_tasks, user_id):
        """Test logging time on a task"""
        entry = service.log_time(
            sample_tasks[0].id, user_id,
            hours=Decimal("4"),
            description="Worked on implementation"
        )
        
        assert entry is not None
        assert entry.hours == Decimal("4")
        
        # Check task actual hours updated
        task = service.get_task(sample_tasks[0].id, user_id)
        assert task.actual_hours == Decimal("4")
    
    def test_multiple_time_entries(self, service, sample_tasks, user_id):
        """Test multiple time entries on same task"""
        service.log_time(sample_tasks[0].id, user_id, Decimal("2"))
        service.log_time(sample_tasks[0].id, user_id, Decimal("3"))
        service.log_time(sample_tasks[0].id, user_id, Decimal("1.5"))
        
        task = service.get_task(sample_tasks[0].id, user_id)
        assert task.actual_hours == Decimal("6.5")
    
    def test_list_time_entries(self, service, sample_project, sample_tasks, user_id):
        """Test listing time entries"""
        service.log_time(sample_tasks[0].id, user_id, Decimal("4"))
        service.log_time(sample_tasks[1].id, user_id, Decimal("2"))
        
        entries = service.list_time_entries(project_id=sample_project.id)
        
        assert len(entries) == 2
    
    def test_billable_hours(self, service, sample_tasks, user_id):
        """Test billable vs non-billable time"""
        service.log_time(sample_tasks[0].id, user_id, Decimal("4"), billable=True)
        service.log_time(sample_tasks[0].id, user_id, Decimal("2"), billable=False)
        
        entries = service.list_time_entries(task_id=sample_tasks[0].id)
        
        billable = sum(e.hours for e in entries if e.billable)
        non_billable = sum(e.hours for e in entries if not e.billable)
        
        assert billable == Decimal("4")
        assert non_billable == Decimal("2")


# ============================================================================
# TEAM TESTS
# ============================================================================

class TestTeamOperations:
    """Test team management operations"""
    
    def test_add_team_member(self, service, sample_project, user_id):
        """Test adding team member"""
        member = service.add_team_member(
            sample_project.id, user_id, "Charlie",
            email="charlie@test.com",
            role="designer",
            hourly_rate=Decimal("65"),
            capacity=Decimal("32")
        )
        
        assert member is not None
        assert member.name == "Charlie"
        assert member.hourly_rate == Decimal("65")
        assert member.capacity_hours_week == Decimal("32")
    
    def test_list_team_members(self, service, sample_project, sample_team, user_id):
        """Test listing team members"""
        members = service.list_team_members(sample_project.id, user_id)
        
        assert len(members) == 2
    
    def test_remove_team_member(self, service, sample_project, sample_team, user_id):
        """Test removing team member"""
        success = service.remove_team_member(sample_team[0].id, user_id)
        
        assert success == True
        
        members = service.list_team_members(sample_project.id, user_id)
        assert len(members) == 1


# ============================================================================
# COMMENT TESTS
# ============================================================================

class TestCommentOperations:
    """Test comment operations"""
    
    def test_add_comment(self, service, sample_tasks, user_id):
        """Test adding comment to task"""
        comment = service.add_comment(
            sample_tasks[0].id, user_id,
            author_name="Alice",
            content="This looks good!",
            mentions=["Bob"]
        )
        
        assert comment is not None
        assert comment.content == "This looks good!"
        assert "Bob" in comment.mentions
    
    def test_list_comments(self, service, sample_tasks, user_id):
        """Test listing comments"""
        service.add_comment(sample_tasks[0].id, user_id, "Alice", "Comment 1")
        service.add_comment(sample_tasks[0].id, user_id, "Bob", "Comment 2")
        
        comments = service.list_comments(sample_tasks[0].id, user_id)
        
        assert len(comments) == 2
        # Should be sorted by creation time
        assert comments[0].author_name == "Alice"


# ============================================================================
# AI ENGINE TESTS
# ============================================================================

class TestProjectAIEngine:
    """Test AI analysis features"""
    
    def test_analyze_healthy_project(self, ai_engine, sample_project, sample_tasks, 
                                     sample_sprint, sample_team, user_id):
        """Test analysis of healthy project"""
        analysis = ai_engine.analyze_project(
            sample_project, sample_tasks, [sample_sprint], [], sample_team
        )
        
        assert analysis is not None
        assert analysis.health_score >= 70
        assert analysis.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]
    
    def test_analyze_at_risk_project(self, service, sample_project, user_id):
        """Test analysis of at-risk project"""
        # Create overdue tasks
        for i in range(5):
            task = service.create_task(
                sample_project.id, user_id, f"Overdue Task {i}",
                due_date=date.today() - timedelta(days=7),
                priority=TaskPriority.HIGH
            )
        
        # Create blocked tasks
        for i in range(3):
            task = service.create_task(
                sample_project.id, user_id, f"Blocked Task {i}"
            )
            service.move_task(task.id, user_id, TaskStatus.BLOCKED)
        
        analysis = service.analyze_project(sample_project.id, user_id)
        
        assert analysis.health_score < 80
        assert analysis.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
        assert len(analysis.risks) > 0  # Has risks detected
    
    def test_task_estimation(self, service, sample_project, sample_tasks, user_id):
        """Test AI task estimation"""
        # Complete some tasks with actual hours
        service.log_time(sample_tasks[0].id, user_id, Decimal("6"))
        service.move_task(sample_tasks[0].id, user_id, TaskStatus.DONE)
        
        # Create new task
        new_task = service.create_task(
            sample_project.id, user_id, "New Task",
            priority=TaskPriority.HIGH,
            tags=["test"]
        )
        
        estimate = service.estimate_task(new_task.id, user_id)
        
        assert estimate is not None
        assert estimate.estimated_hours > 0
        assert 0 <= estimate.confidence <= 1
    
    def test_assignee_suggestion(self, service, sample_project, sample_tasks, sample_team, user_id):
        """Test AI assignee suggestion"""
        # Alice has 1 task, Bob has 1 task
        # Create unassigned task
        new_task = service.create_task(
            sample_project.id, user_id, "New Task"
        )
        
        suggestion = service.suggest_assignee(new_task.id, user_id)
        
        assert "suggestion" in suggestion
        assert suggestion["suggestion"] is not None
        assert "reason" in suggestion
    
    def test_workload_analysis(self, ai_engine, sample_tasks, sample_team):
        """Test workload balance analysis"""
        workload = ai_engine._analyze_workload(sample_tasks, sample_team)
        
        assert "balanced" in workload
        assert "distribution" in workload
        assert len(workload["distribution"]) == 2


# ============================================================================
# DASHBOARD TESTS
# ============================================================================

class TestDashboard:
    """Test dashboard functionality"""
    
    def test_empty_dashboard(self, service, user_id):
        """Test dashboard with no data"""
        dashboard = service.get_dashboard(user_id)
        
        assert dashboard["projects"]["total"] == 0
        assert dashboard["tasks"]["total"] == 0
    
    def test_dashboard_with_data(self, service, sample_project, sample_tasks, user_id):
        """Test dashboard with data"""
        # Log some time
        service.log_time(sample_tasks[0].id, user_id, Decimal("4"))
        
        # Update project to active
        service.update_project(sample_project.id, user_id, {'status': ProjectStatus.ACTIVE})
        
        dashboard = service.get_dashboard(user_id)
        
        assert dashboard["projects"]["total"] == 1
        assert dashboard["projects"]["active"] == 1
        assert dashboard["tasks"]["total"] == 3
        assert dashboard["time"]["hours_this_week"] >= 4


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for full workflows"""
    
    def test_full_project_workflow(self, service, user_id):
        """Test complete project lifecycle"""
        # 1. Create project
        project = service.create_project(
            user_id, "Integration Test Project",
            target_date=date.today() + timedelta(30),
            budget=Decimal("20000")
        )
        
        # 2. Add team
        alice = service.add_team_member(
            project.id, user_id, "Alice", "alice@test.com", "lead",
            hourly_rate=Decimal("75")
        )
        bob = service.add_team_member(
            project.id, user_id, "Bob", "bob@test.com", "developer",
            hourly_rate=Decimal("60")
        )
        
        # 3. Create sprint
        sprint = service.create_sprint(
            project.id, user_id, "Sprint 1",
            start_date=date.today(),
            end_date=date.today() + timedelta(14),
            velocity_planned=10
        )
        
        # 4. Create milestone
        milestone = service.create_milestone(
            project.id, user_id, "MVP",
            due_date=date.today() + timedelta(14),
            deliverables=["Feature A", "Feature B"]
        )
        
        # 5. Create and assign tasks
        task1 = service.create_task(
            project.id, user_id, "Feature A",
            priority=TaskPriority.HIGH,
            assignee_id=alice.id,
            assignee_name=alice.name,
            sprint_id=sprint.id,
            estimated_hours=Decimal("16")
        )
        task2 = service.create_task(
            project.id, user_id, "Feature B",
            priority=TaskPriority.MEDIUM,
            assignee_id=bob.id,
            assignee_name=bob.name,
            sprint_id=sprint.id,
            estimated_hours=Decimal("12")
        )
        
        # 6. Start sprint
        service.start_sprint(sprint.id, user_id)
        
        # 7. Work on tasks
        service.move_task(task1.id, user_id, TaskStatus.IN_PROGRESS)
        service.log_time(task1.id, user_id, Decimal("8"), "Day 1 work")
        
        # 8. Add comments
        service.add_comment(task1.id, user_id, "Alice", "Making progress!")
        service.add_comment(task1.id, user_id, "Bob", "Looks good @Alice")
        
        # 9. Complete tasks
        service.log_time(task1.id, user_id, Decimal("6"))
        service.move_task(task1.id, user_id, TaskStatus.DONE)
        
        service.move_task(task2.id, user_id, TaskStatus.IN_PROGRESS)
        service.log_time(task2.id, user_id, Decimal("10"))
        service.move_task(task2.id, user_id, TaskStatus.DONE)
        
        # 10. Complete sprint
        sprint = service.complete_sprint(sprint.id, user_id)
        
        # 11. Complete milestone
        service.complete_milestone(milestone.id, user_id)
        
        # 12. Analyze project
        analysis = service.analyze_project(project.id, user_id)
        
        # Verify final state
        assert sprint.status == SprintStatus.COMPLETED
        assert sprint.velocity_actual == 2
        
        tasks = service.list_tasks(project.id, user_id)
        assert all(t.status == TaskStatus.DONE for t in tasks)
        
        milestones = service.list_milestones(project.id, user_id)
        assert milestones[0].status == MilestoneStatus.COMPLETED
        
        assert analysis.completion_percentage == 100
        assert analysis.health_score >= 80


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
