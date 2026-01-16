"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 CHE·NU™ PERSONAL PRODUCTIVITY — API ROUTES                   ║
║                                                                              ║
║  RESTful API for notes, tasks, and productivity features.                    ║
║                                                                              ║
║  Endpoints:                                                                  ║
║  - /notes/* - Note management                                                ║
║  - /tasks/* - Task management                                                ║
║  - /projects/* - Project organization                                        ║
║  - /stats/* - Productivity statistics                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

from ..agents.note_assistant import (
    get_note_assistant, NoteType, NoteStatus, Note
)
from ..agents.task_manager import (
    get_task_manager, TaskPriority, TaskStatus, RecurrenceType, Task, Project
)

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════════

# --- Notes ---

class CreateNoteRequest(BaseModel):
    content: str = Field(..., min_length=1)
    title: Optional[str] = None
    tags: Optional[List[str]] = None
    folder: Optional[str] = None
    note_type: Optional[NoteType] = None
    auto_enhance: bool = True
    user_id: str = "default_user"
    identity_id: str = ""


class UpdateNoteRequest(BaseModel):
    content: Optional[str] = None
    title: Optional[str] = None
    tags: Optional[List[str]] = None
    folder: Optional[str] = None
    status: Optional[NoteStatus] = None
    auto_enhance: bool = False


class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    type: str
    status: str
    tags: List[str]
    folder: Optional[str]
    summary: Optional[str]
    created_at: str
    updated_at: str
    word_count: int
    ai_enhanced: bool
    metadata: Dict[str, Any] = {}


# --- Tasks ---

class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    estimated_minutes: Optional[int] = None
    project_id: Optional[str] = None
    tags: Optional[List[str]] = None
    recurrence: RecurrenceType = RecurrenceType.NONE
    parent_id: Optional[str] = None
    auto_suggest: bool = True
    user_id: str = "default_user"
    identity_id: str = ""


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    estimated_minutes: Optional[int] = None
    project_id: Optional[str] = None
    tags: Optional[List[str]] = None


class CompleteTaskRequest(BaseModel):
    actual_minutes: Optional[int] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    priority: str
    status: str
    due_date: Optional[str]
    due_time: Optional[str]
    estimated_minutes: Optional[int]
    actual_minutes: Optional[int]
    project_id: Optional[str]
    tags: List[str]
    subtasks: List[str]
    parent_id: Optional[str]
    recurrence: str
    completed_at: Optional[str]
    created_at: str
    ai_score: Optional[float]
    metadata: Dict[str, Any] = {}


# --- Projects ---

class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    color: str = "#3B82F6"
    icon: Optional[str] = None
    user_id: str = "default_user"


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    color: str
    icon: Optional[str]
    task_count: int
    completed_count: int
    created_at: str
    archived: bool


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def note_to_response(note: Note) -> NoteResponse:
    """Convert Note to response model."""
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        type=note.type.value,
        status=note.status.value,
        tags=note.tags,
        folder=note.folder,
        summary=note.summary,
        created_at=note.created_at.isoformat(),
        updated_at=note.updated_at.isoformat(),
        word_count=note.word_count,
        ai_enhanced=note.ai_enhanced,
        metadata=note.metadata,
    )


def task_to_response(task: Task) -> TaskResponse:
    """Convert Task to response model."""
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=task.priority.value,
        status=task.status.value,
        due_date=task.due_date.isoformat() if task.due_date else None,
        due_time=task.due_time,
        estimated_minutes=task.estimated_minutes,
        actual_minutes=task.actual_minutes,
        project_id=task.project_id,
        tags=task.tags,
        subtasks=task.subtasks,
        parent_id=task.parent_id,
        recurrence=task.recurrence.value,
        completed_at=task.completed_at.isoformat() if task.completed_at else None,
        created_at=task.created_at.isoformat(),
        ai_score=task.ai_score,
        metadata=task.metadata,
    )


def project_to_response(project: Project) -> ProjectResponse:
    """Convert Project to response model."""
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        color=project.color,
        icon=project.icon,
        task_count=project.task_count,
        completed_count=project.completed_count,
        created_at=project.created_at.isoformat(),
        archived=project.archived,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# NOTE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/notes", response_model=NoteResponse)
async def create_note(request: CreateNoteRequest):
    """Create a new note with optional AI enhancement."""
    agent = get_note_assistant()
    
    note = await agent.create_note(
        content=request.content,
        user_id=request.user_id,
        identity_id=request.identity_id,
        title=request.title,
        tags=request.tags,
        folder=request.folder,
        note_type=request.note_type,
        auto_enhance=request.auto_enhance,
    )
    
    return note_to_response(note)


@router.get("/notes", response_model=List[NoteResponse])
async def list_notes(
    user_id: str = "default_user",
    folder: Optional[str] = None,
    tag: Optional[str] = None,
    note_type: Optional[NoteType] = None,
    status: Optional[NoteStatus] = None,
    search: Optional[str] = None,
    limit: int = Query(default=50, le=100),
    offset: int = 0,
):
    """List notes with filtering."""
    agent = get_note_assistant()
    
    notes = agent.list_notes(
        user_id=user_id,
        folder=folder,
        tag=tag,
        note_type=note_type,
        status=status,
        search=search,
        limit=limit,
        offset=offset,
    )
    
    return [note_to_response(n) for n in notes]


@router.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str, user_id: str = "default_user"):
    """Get a specific note."""
    agent = get_note_assistant()
    
    note = agent.get_note(note_id, user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note_to_response(note)


@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, request: UpdateNoteRequest, user_id: str = "default_user"):
    """Update a note."""
    agent = get_note_assistant()
    
    note = await agent.update_note(
        note_id=note_id,
        user_id=user_id,
        content=request.content,
        title=request.title,
        tags=request.tags,
        folder=request.folder,
        status=request.status,
        auto_enhance=request.auto_enhance,
    )
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note_to_response(note)


@router.delete("/notes/{note_id}")
async def delete_note(note_id: str, user_id: str = "default_user"):
    """Delete a note."""
    agent = get_note_assistant()
    
    if not agent.delete_note(note_id, user_id):
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {"status": "deleted", "id": note_id}


@router.post("/notes/{note_id}/enhance", response_model=NoteResponse)
async def enhance_note(note_id: str, user_id: str = "default_user"):
    """Enhance a note with AI."""
    agent = get_note_assistant()
    
    note = await agent.enhance_note(note_id, user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return note_to_response(note)


@router.get("/notes/{note_id}/related", response_model=List[NoteResponse])
async def get_related_notes(note_id: str, user_id: str = "default_user", limit: int = 5):
    """Get related notes."""
    agent = get_note_assistant()
    
    related = await agent.suggest_related(note_id, user_id, limit)
    return [note_to_response(n) for n in related]


@router.get("/notes/folders/list")
async def list_folders(user_id: str = "default_user"):
    """List all folders with counts."""
    agent = get_note_assistant()
    return agent.get_folders(user_id)


@router.get("/notes/tags/list")
async def list_tags(user_id: str = "default_user", limit: int = 20):
    """List all tags with counts."""
    agent = get_note_assistant()
    return agent.get_tags(user_id, limit)


# ═══════════════════════════════════════════════════════════════════════════════
# TASK ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/tasks", response_model=TaskResponse)
async def create_task(request: CreateTaskRequest):
    """Create a new task with optional AI suggestions."""
    agent = get_task_manager()
    
    task = await agent.create_task(
        title=request.title,
        user_id=request.user_id,
        identity_id=request.identity_id,
        description=request.description,
        priority=request.priority,
        due_date=request.due_date,
        due_time=request.due_time,
        estimated_minutes=request.estimated_minutes,
        project_id=request.project_id,
        tags=request.tags,
        recurrence=request.recurrence,
        parent_id=request.parent_id,
        auto_suggest=request.auto_suggest,
    )
    
    return task_to_response(task)


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str = "default_user",
    project_id: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tag: Optional[str] = None,
    due_today: bool = False,
    due_this_week: bool = False,
    overdue: bool = False,
    search: Optional[str] = None,
    sort_by: str = "ai_score",
    limit: int = Query(default=50, le=100),
    offset: int = 0,
):
    """List tasks with filtering."""
    agent = get_task_manager()
    
    tasks = agent.list_tasks(
        user_id=user_id,
        project_id=project_id,
        status=status,
        priority=priority,
        tag=tag,
        due_today=due_today,
        due_this_week=due_this_week,
        overdue=overdue,
        search=search,
        sort_by=sort_by,
        limit=limit,
        offset=offset,
    )
    
    return [task_to_response(t) for t in tasks]


@router.get("/tasks/today")
async def get_today_view(user_id: str = "default_user"):
    """Get today's task view."""
    agent = get_task_manager()
    today = agent.get_today_view(user_id)
    
    return {
        "date": today["date"],
        "overdue": [task_to_response(t) for t in today["overdue"]],
        "due_today": [task_to_response(t) for t in today["due_today"]],
        "high_priority": [task_to_response(t) for t in today["high_priority"]],
        "completed_today": [task_to_response(t) for t in today["completed_today"]],
        "stats": today["stats"],
    }


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, user_id: str = "default_user"):
    """Get a specific task."""
    agent = get_task_manager()
    
    task = agent.get_task(task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_to_response(task)


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, request: UpdateTaskRequest, user_id: str = "default_user"):
    """Update a task."""
    agent = get_task_manager()
    
    task = await agent.update_task(
        task_id=task_id,
        user_id=user_id,
        **request.model_dump(exclude_unset=True),
    )
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_to_response(task)


@router.post("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: str, request: CompleteTaskRequest = None, user_id: str = "default_user"):
    """Mark a task as complete."""
    agent = get_task_manager()
    
    task = await agent.complete_task(
        task_id=task_id,
        user_id=user_id,
        actual_minutes=request.actual_minutes if request else None,
    )
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_to_response(task)


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, user_id: str = "default_user"):
    """Delete a task."""
    agent = get_task_manager()
    
    if not agent.delete_task(task_id, user_id):
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"status": "deleted", "id": task_id}


# ═══════════════════════════════════════════════════════════════════════════════
# PROJECT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/projects", response_model=ProjectResponse)
async def create_project(request: CreateProjectRequest):
    """Create a new project."""
    agent = get_task_manager()
    
    project = agent.create_project(
        name=request.name,
        user_id=request.user_id,
        description=request.description,
        color=request.color,
        icon=request.icon,
    )
    
    return project_to_response(project)


@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(user_id: str = "default_user", include_archived: bool = False):
    """List all projects."""
    agent = get_task_manager()
    projects = agent.get_projects(user_id, include_archived)
    return [project_to_response(p) for p in projects]


# ═══════════════════════════════════════════════════════════════════════════════
# STATS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats/notes")
async def get_note_stats(user_id: str = "default_user"):
    """Get note statistics."""
    agent = get_note_assistant()
    return agent.get_stats(user_id)


@router.get("/stats/tasks")
async def get_task_stats(user_id: str = "default_user"):
    """Get task statistics."""
    agent = get_task_manager()
    return agent.get_stats(user_id)


@router.get("/stats/overview")
async def get_overview_stats(user_id: str = "default_user"):
    """Get combined productivity statistics."""
    note_agent = get_note_assistant()
    task_agent = get_task_manager()
    
    note_stats = note_agent.get_stats(user_id)
    task_stats = task_agent.get_stats(user_id)
    
    return {
        "notes": note_stats,
        "tasks": task_stats,
        "productivity_score": _calculate_productivity_score(note_stats, task_stats),
    }


def _calculate_productivity_score(note_stats: Dict, task_stats: Dict) -> int:
    """Calculate overall productivity score (0-100)."""
    score = 50  # Base score
    
    # Task completion rate bonus
    if task_stats.get("completion_rate", 0) > 0:
        score += min(20, task_stats["completion_rate"] / 5)
    
    # Active notes bonus
    if note_stats.get("total_notes", 0) > 0:
        score += min(10, note_stats["total_notes"] / 10)
    
    # Overdue penalty
    if task_stats.get("overdue", 0) > 0:
        score -= min(20, task_stats["overdue"] * 5)
    
    return max(0, min(100, int(score)))


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH & INFO
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "personal-productivity"}


@router.get("/info")
async def service_info():
    """Service information."""
    return {
        "service": "CHE·NU Personal Productivity",
        "version": "1.0.0",
        "features": {
            "notes": {
                "ai_enhancement": True,
                "auto_tagging": True,
                "smart_folders": True,
                "related_notes": True,
            },
            "tasks": {
                "ai_prioritization": True,
                "smart_scheduling": True,
                "recurring_tasks": True,
                "subtasks": True,
                "projects": True,
            },
        },
        "competitive_positioning": {
            "vs_notion": "28 AI agents vs 1, native task management",
            "vs_todoist": "AI prioritization, integrated notes",
            "pricing": "$15/mo vs $15 Notion (more features)",
        }
    }
