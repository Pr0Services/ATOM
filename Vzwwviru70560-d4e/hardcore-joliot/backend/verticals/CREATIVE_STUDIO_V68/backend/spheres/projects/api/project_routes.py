"""
CHE·NU™ V68 - Project Management API Routes
40+ endpoints for full PM functionality
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date
from decimal import Decimal
from enum import Enum

from ..agents.project_agent import (
    ProjectManagementService, ProjectStatus, TaskStatus, TaskPriority,
    SprintStatus, MilestoneStatus
)

router = APIRouter(prefix="/api/v2/projects", tags=["Project Management"])

# Service instance
_service = ProjectManagementService()


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    budget: Optional[float] = None
    client_name: Optional[str] = None
    tags: List[str] = []


class UpdateProjectRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    target_date: Optional[date] = None
    budget: Optional[float] = None
    client_name: Optional[str] = None
    tags: Optional[List[str]] = None
    settings: Optional[Dict[str, Any]] = None


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str = ""
    priority: str = "medium"
    assignee_id: Optional[str] = None
    assignee_name: Optional[str] = None
    due_date: Optional[date] = None
    estimated_hours: Optional[float] = None
    sprint_id: Optional[str] = None
    milestone_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    tags: List[str] = []


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[str] = None
    assignee_name: Optional[str] = None
    due_date: Optional[date] = None
    estimated_hours: Optional[float] = None
    sprint_id: Optional[str] = None
    milestone_id: Optional[str] = None
    tags: Optional[List[str]] = None
    checklist: Optional[List[Dict[str, Any]]] = None
    order: Optional[int] = None


class MoveTaskRequest(BaseModel):
    status: str
    order: Optional[int] = None


class CreateSprintRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    start_date: date
    end_date: date
    goal: str = ""
    velocity_planned: int = 0


class UpdateSprintRequest(BaseModel):
    name: Optional[str] = None
    goal: Optional[str] = None
    status: Optional[str] = None
    velocity_planned: Optional[int] = None
    velocity_actual: Optional[int] = None


class CreateMilestoneRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    due_date: date
    description: str = ""
    deliverables: List[str] = []


class LogTimeRequest(BaseModel):
    hours: float = Field(..., gt=0, le=24)
    description: str = ""
    date: Optional[date] = None
    billable: bool = True


class AddTeamMemberRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: str
    role: str = "member"
    hourly_rate: Optional[float] = None
    capacity_hours_week: float = 40


class AddCommentRequest(BaseModel):
    author_name: str
    content: str = Field(..., min_length=1, max_length=5000)
    mentions: List[str] = []


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_user_id() -> str:
    """Get current user ID (placeholder for auth)"""
    return "user_default"


def serialize_project(project) -> Dict[str, Any]:
    """Serialize project to dict"""
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status.value,
        "start_date": project.start_date.isoformat() if project.start_date else None,
        "target_date": project.target_date.isoformat() if project.target_date else None,
        "budget": float(project.budget) if project.budget else None,
        "spent": float(project.spent),
        "client_name": project.client_name,
        "tags": project.tags,
        "settings": project.settings,
        "created_at": project.created_at.isoformat(),
        "updated_at": project.updated_at.isoformat()
    }


def serialize_task(task) -> Dict[str, Any]:
    """Serialize task to dict"""
    return {
        "id": task.id,
        "project_id": task.project_id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,
        "priority": task.priority.value,
        "assignee_id": task.assignee_id,
        "assignee_name": task.assignee_name,
        "sprint_id": task.sprint_id,
        "milestone_id": task.milestone_id,
        "parent_task_id": task.parent_task_id,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "estimated_hours": float(task.estimated_hours) if task.estimated_hours else None,
        "actual_hours": float(task.actual_hours),
        "tags": task.tags,
        "checklist": task.checklist,
        "order": task.order,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "completed_at": task.completed_at.isoformat() if task.completed_at else None
    }


def serialize_sprint(sprint) -> Dict[str, Any]:
    """Serialize sprint to dict"""
    return {
        "id": sprint.id,
        "project_id": sprint.project_id,
        "name": sprint.name,
        "goal": sprint.goal,
        "status": sprint.status.value,
        "start_date": sprint.start_date.isoformat(),
        "end_date": sprint.end_date.isoformat(),
        "velocity_planned": sprint.velocity_planned,
        "velocity_actual": sprint.velocity_actual,
        "created_at": sprint.created_at.isoformat()
    }


def serialize_milestone(milestone) -> Dict[str, Any]:
    """Serialize milestone to dict"""
    return {
        "id": milestone.id,
        "project_id": milestone.project_id,
        "name": milestone.name,
        "description": milestone.description,
        "status": milestone.status.value,
        "due_date": milestone.due_date.isoformat(),
        "completed_date": milestone.completed_date.isoformat() if milestone.completed_date else None,
        "deliverables": milestone.deliverables,
        "created_at": milestone.created_at.isoformat()
    }


def serialize_time_entry(entry) -> Dict[str, Any]:
    """Serialize time entry to dict"""
    return {
        "id": entry.id,
        "task_id": entry.task_id,
        "user_id": entry.user_id,
        "hours": float(entry.hours),
        "description": entry.description,
        "date": entry.date.isoformat(),
        "billable": entry.billable,
        "created_at": entry.created_at.isoformat()
    }


def serialize_team_member(member) -> Dict[str, Any]:
    """Serialize team member to dict"""
    return {
        "id": member.id,
        "project_id": member.project_id,
        "name": member.name,
        "email": member.email,
        "role": member.role,
        "hourly_rate": float(member.hourly_rate) if member.hourly_rate else None,
        "capacity_hours_week": float(member.capacity_hours_week),
        "joined_at": member.joined_at.isoformat()
    }


def serialize_comment(comment) -> Dict[str, Any]:
    """Serialize comment to dict"""
    return {
        "id": comment.id,
        "task_id": comment.task_id,
        "author_name": comment.author_name,
        "content": comment.content,
        "mentions": comment.mentions,
        "created_at": comment.created_at.isoformat(),
        "updated_at": comment.updated_at.isoformat()
    }


def serialize_analysis(analysis) -> Dict[str, Any]:
    """Serialize project analysis to dict"""
    return {
        "project_id": analysis.project_id,
        "health_score": analysis.health_score,
        "risk_level": analysis.risk_level.value,
        "completion_percentage": analysis.completion_percentage,
        "estimated_completion_date": analysis.estimated_completion_date.isoformat() if analysis.estimated_completion_date else None,
        "budget_status": analysis.budget_status,
        "velocity_trend": analysis.velocity_trend,
        "risks": analysis.risks,
        "recommendations": analysis.recommendations,
        "blockers": analysis.blockers,
        "workload_balance": analysis.workload_balance,
        "generated_at": analysis.generated_at.isoformat()
    }


# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@router.post("/")
async def create_project(request: CreateProjectRequest):
    """Create a new project"""
    user_id = get_user_id()
    
    project = _service.create_project(
        user_id=user_id,
        name=request.name,
        description=request.description,
        start_date=request.start_date,
        target_date=request.target_date,
        budget=Decimal(str(request.budget)) if request.budget else None,
        client_name=request.client_name,
        tags=request.tags
    )
    
    return {"project": serialize_project(project)}


@router.get("/")
async def list_projects(
    status: Optional[str] = None,
    search: Optional[str] = None
):
    """List all projects"""
    user_id = get_user_id()
    
    status_enum = ProjectStatus(status) if status else None
    projects = _service.list_projects(user_id, status=status_enum, search=search)
    
    return {
        "projects": [serialize_project(p) for p in projects],
        "total": len(projects)
    }


@router.get("/{project_id}")
async def get_project(project_id: str = Path(...)):
    """Get project by ID"""
    user_id = get_user_id()
    
    project = _service.get_project(project_id, user_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"project": serialize_project(project)}


@router.put("/{project_id}")
async def update_project(
    request: UpdateProjectRequest,
    project_id: str = Path(...)
):
    """Update project"""
    user_id = get_user_id()
    
    updates = {}
    if request.name is not None:
        updates['name'] = request.name
    if request.description is not None:
        updates['description'] = request.description
    if request.status is not None:
        updates['status'] = ProjectStatus(request.status)
    if request.target_date is not None:
        updates['target_date'] = request.target_date
    if request.budget is not None:
        updates['budget'] = Decimal(str(request.budget))
    if request.client_name is not None:
        updates['client_name'] = request.client_name
    if request.tags is not None:
        updates['tags'] = request.tags
    if request.settings is not None:
        updates['settings'] = request.settings
    
    project = _service.update_project(project_id, user_id, updates)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"project": serialize_project(project)}


@router.post("/{project_id}/analyze")
async def analyze_project(project_id: str = Path(...)):
    """Get AI analysis of project"""
    user_id = get_user_id()
    
    analysis = _service.analyze_project(project_id, user_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"analysis": serialize_analysis(analysis)}


# ============================================================================
# TASK ENDPOINTS
# ============================================================================

@router.post("/{project_id}/tasks")
async def create_task(
    request: CreateTaskRequest,
    project_id: str = Path(...)
):
    """Create a new task"""
    user_id = get_user_id()
    
    task = _service.create_task(
        project_id=project_id,
        user_id=user_id,
        title=request.title,
        description=request.description,
        priority=TaskPriority(request.priority),
        assignee_id=request.assignee_id,
        assignee_name=request.assignee_name,
        due_date=request.due_date,
        estimated_hours=Decimal(str(request.estimated_hours)) if request.estimated_hours else None,
        sprint_id=request.sprint_id,
        milestone_id=request.milestone_id,
        parent_task_id=request.parent_task_id,
        tags=request.tags
    )
    
    if not task:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"task": serialize_task(task)}


@router.get("/{project_id}/tasks")
async def list_tasks(
    project_id: str = Path(...),
    status: Optional[str] = None,
    assignee_id: Optional[str] = None,
    sprint_id: Optional[str] = None,
    priority: Optional[str] = None
):
    """List tasks for a project"""
    user_id = get_user_id()
    
    tasks = _service.list_tasks(
        project_id=project_id,
        user_id=user_id,
        status=TaskStatus(status) if status else None,
        assignee_id=assignee_id,
        sprint_id=sprint_id,
        priority=TaskPriority(priority) if priority else None
    )
    
    return {
        "tasks": [serialize_task(t) for t in tasks],
        "total": len(tasks)
    }


@router.get("/{project_id}/tasks/{task_id}")
async def get_task(
    project_id: str = Path(...),
    task_id: str = Path(...)
):
    """Get task by ID"""
    user_id = get_user_id()
    
    task = _service.get_task(task_id, user_id)
    if not task or task.project_id != project_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task": serialize_task(task)}


@router.put("/{project_id}/tasks/{task_id}")
async def update_task(
    request: UpdateTaskRequest,
    project_id: str = Path(...),
    task_id: str = Path(...)
):
    """Update task"""
    user_id = get_user_id()
    
    updates = {}
    if request.title is not None:
        updates['title'] = request.title
    if request.description is not None:
        updates['description'] = request.description
    if request.status is not None:
        updates['status'] = TaskStatus(request.status)
    if request.priority is not None:
        updates['priority'] = TaskPriority(request.priority)
    if request.assignee_id is not None:
        updates['assignee_id'] = request.assignee_id
    if request.assignee_name is not None:
        updates['assignee_name'] = request.assignee_name
    if request.due_date is not None:
        updates['due_date'] = request.due_date
    if request.estimated_hours is not None:
        updates['estimated_hours'] = Decimal(str(request.estimated_hours))
    if request.sprint_id is not None:
        updates['sprint_id'] = request.sprint_id
    if request.milestone_id is not None:
        updates['milestone_id'] = request.milestone_id
    if request.tags is not None:
        updates['tags'] = request.tags
    if request.checklist is not None:
        updates['checklist'] = request.checklist
    if request.order is not None:
        updates['order'] = request.order
    
    task = _service.update_task(task_id, user_id, updates)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task": serialize_task(task)}


@router.post("/{project_id}/tasks/{task_id}/move")
async def move_task(
    request: MoveTaskRequest,
    project_id: str = Path(...),
    task_id: str = Path(...)
):
    """Move task to new status (Kanban)"""
    user_id = get_user_id()
    
    task = _service.move_task(
        task_id=task_id,
        user_id=user_id,
        new_status=TaskStatus(request.status),
        new_order=request.order
    )
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"task": serialize_task(task)}


@router.post("/{project_id}/tasks/{task_id}/estimate")
async def estimate_task(
    project_id: str = Path(...),
    task_id: str = Path(...)
):
    """Get AI estimate for task"""
    user_id = get_user_id()
    
    estimate = _service.estimate_task(task_id, user_id)
    if not estimate:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "estimate": {
            "task_id": estimate.task_id,
            "estimated_hours": float(estimate.estimated_hours),
            "confidence": estimate.confidence,
            "similar_tasks": estimate.similar_tasks,
            "factors": estimate.factors,
            "generated_at": estimate.generated_at.isoformat()
        }
    }


@router.post("/{project_id}/tasks/{task_id}/suggest-assignee")
async def suggest_assignee(
    project_id: str = Path(...),
    task_id: str = Path(...)
):
    """Get AI suggestion for task assignment"""
    user_id = get_user_id()
    
    suggestion = _service.suggest_assignee(task_id, user_id)
    
    if "error" in suggestion:
        raise HTTPException(status_code=404, detail=suggestion["error"])
    
    return suggestion


# ============================================================================
# SPRINT ENDPOINTS
# ============================================================================

@router.post("/{project_id}/sprints")
async def create_sprint(
    request: CreateSprintRequest,
    project_id: str = Path(...)
):
    """Create a new sprint"""
    user_id = get_user_id()
    
    sprint = _service.create_sprint(
        project_id=project_id,
        user_id=user_id,
        name=request.name,
        start_date=request.start_date,
        end_date=request.end_date,
        goal=request.goal,
        velocity_planned=request.velocity_planned
    )
    
    if not sprint:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"sprint": serialize_sprint(sprint)}


@router.get("/{project_id}/sprints")
async def list_sprints(project_id: str = Path(...)):
    """List sprints for a project"""
    user_id = get_user_id()
    
    sprints = _service.list_sprints(project_id, user_id)
    
    return {
        "sprints": [serialize_sprint(s) for s in sprints],
        "total": len(sprints)
    }


@router.put("/{project_id}/sprints/{sprint_id}")
async def update_sprint(
    request: UpdateSprintRequest,
    project_id: str = Path(...),
    sprint_id: str = Path(...)
):
    """Update sprint"""
    user_id = get_user_id()
    
    updates = {}
    if request.name is not None:
        updates['name'] = request.name
    if request.goal is not None:
        updates['goal'] = request.goal
    if request.status is not None:
        updates['status'] = SprintStatus(request.status)
    if request.velocity_planned is not None:
        updates['velocity_planned'] = request.velocity_planned
    if request.velocity_actual is not None:
        updates['velocity_actual'] = request.velocity_actual
    
    sprint = _service.update_sprint(sprint_id, user_id, updates)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    return {"sprint": serialize_sprint(sprint)}


@router.post("/{project_id}/sprints/{sprint_id}/start")
async def start_sprint(
    project_id: str = Path(...),
    sprint_id: str = Path(...)
):
    """Start a sprint"""
    user_id = get_user_id()
    
    sprint = _service.start_sprint(sprint_id, user_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    return {"sprint": serialize_sprint(sprint)}


@router.post("/{project_id}/sprints/{sprint_id}/complete")
async def complete_sprint(
    project_id: str = Path(...),
    sprint_id: str = Path(...)
):
    """Complete a sprint"""
    user_id = get_user_id()
    
    sprint = _service.complete_sprint(sprint_id, user_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    return {"sprint": serialize_sprint(sprint)}


# ============================================================================
# MILESTONE ENDPOINTS
# ============================================================================

@router.post("/{project_id}/milestones")
async def create_milestone(
    request: CreateMilestoneRequest,
    project_id: str = Path(...)
):
    """Create a milestone"""
    user_id = get_user_id()
    
    milestone = _service.create_milestone(
        project_id=project_id,
        user_id=user_id,
        name=request.name,
        due_date=request.due_date,
        description=request.description,
        deliverables=request.deliverables
    )
    
    if not milestone:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"milestone": serialize_milestone(milestone)}


@router.get("/{project_id}/milestones")
async def list_milestones(project_id: str = Path(...)):
    """List milestones for a project"""
    user_id = get_user_id()
    
    milestones = _service.list_milestones(project_id, user_id)
    
    return {
        "milestones": [serialize_milestone(m) for m in milestones],
        "total": len(milestones)
    }


@router.post("/{project_id}/milestones/{milestone_id}/complete")
async def complete_milestone(
    project_id: str = Path(...),
    milestone_id: str = Path(...)
):
    """Complete a milestone"""
    user_id = get_user_id()
    
    milestone = _service.complete_milestone(milestone_id, user_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    
    return {"milestone": serialize_milestone(milestone)}


# ============================================================================
# TIME TRACKING ENDPOINTS
# ============================================================================

@router.post("/{project_id}/tasks/{task_id}/time")
async def log_time(
    request: LogTimeRequest,
    project_id: str = Path(...),
    task_id: str = Path(...)
):
    """Log time on a task"""
    user_id = get_user_id()
    
    entry = _service.log_time(
        task_id=task_id,
        user_id=user_id,
        hours=Decimal(str(request.hours)),
        description=request.description,
        entry_date=request.date,
        billable=request.billable
    )
    
    if not entry:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"time_entry": serialize_time_entry(entry)}


@router.get("/{project_id}/time-entries")
async def list_time_entries(
    project_id: str = Path(...),
    task_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """List time entries for a project"""
    user_id = get_user_id()
    
    entries = _service.list_time_entries(
        project_id=project_id,
        task_id=task_id,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )
    
    total_hours = sum(e.hours for e in entries)
    billable_hours = sum(e.hours for e in entries if e.billable)
    
    return {
        "time_entries": [serialize_time_entry(e) for e in entries],
        "total": len(entries),
        "total_hours": float(total_hours),
        "billable_hours": float(billable_hours)
    }


# ============================================================================
# TEAM ENDPOINTS
# ============================================================================

@router.post("/{project_id}/team")
async def add_team_member(
    request: AddTeamMemberRequest,
    project_id: str = Path(...)
):
    """Add team member to project"""
    user_id = get_user_id()
    
    member = _service.add_team_member(
        project_id=project_id,
        user_id=user_id,
        name=request.name,
        email=request.email,
        role=request.role,
        hourly_rate=Decimal(str(request.hourly_rate)) if request.hourly_rate else None,
        capacity=Decimal(str(request.capacity_hours_week))
    )
    
    if not member:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"team_member": serialize_team_member(member)}


@router.get("/{project_id}/team")
async def list_team_members(project_id: str = Path(...)):
    """List team members for a project"""
    user_id = get_user_id()
    
    members = _service.list_team_members(project_id, user_id)
    
    return {
        "team_members": [serialize_team_member(m) for m in members],
        "total": len(members)
    }


@router.delete("/{project_id}/team/{member_id}")
async def remove_team_member(
    project_id: str = Path(...),
    member_id: str = Path(...)
):
    """Remove team member from project"""
    user_id = get_user_id()
    
    success = _service.remove_team_member(member_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    return {"success": True}


# ============================================================================
# COMMENT ENDPOINTS
# ============================================================================

@router.post("/{project_id}/tasks/{task_id}/comments")
async def add_comment(
    request: AddCommentRequest,
    project_id: str = Path(...),
    task_id: str = Path(...)
):
    """Add comment to task"""
    user_id = get_user_id()
    
    comment = _service.add_comment(
        task_id=task_id,
        user_id=user_id,
        author_name=request.author_name,
        content=request.content,
        mentions=request.mentions
    )
    
    if not comment:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"comment": serialize_comment(comment)}


@router.get("/{project_id}/tasks/{task_id}/comments")
async def list_comments(
    project_id: str = Path(...),
    task_id: str = Path(...)
):
    """List comments for a task"""
    user_id = get_user_id()
    
    comments = _service.list_comments(task_id, user_id)
    
    return {
        "comments": [serialize_comment(c) for c in comments],
        "total": len(comments)
    }


# ============================================================================
# DASHBOARD ENDPOINT
# ============================================================================

@router.get("/dashboard")
async def get_dashboard():
    """Get PM dashboard"""
    user_id = get_user_id()
    
    dashboard = _service.get_dashboard(user_id)
    
    return {"dashboard": dashboard}


# ============================================================================
# KANBAN VIEW ENDPOINT
# ============================================================================

@router.get("/{project_id}/kanban")
async def get_kanban_view(project_id: str = Path(...)):
    """Get tasks organized by status for Kanban view"""
    user_id = get_user_id()
    
    tasks = _service.list_tasks(project_id, user_id)
    
    # Organize by status
    kanban = {status.value: [] for status in TaskStatus}
    for task in tasks:
        kanban[task.status.value].append(serialize_task(task))
    
    return {"kanban": kanban}


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "project-management",
        "version": "V68"
    }
