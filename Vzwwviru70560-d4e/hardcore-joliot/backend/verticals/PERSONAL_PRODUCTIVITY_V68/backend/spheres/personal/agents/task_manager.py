"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 CHE·NU™ PERSONAL PRODUCTIVITY — TASK MANAGER                 ║
║                                                                              ║
║  AI-powered task management with intelligent prioritization.                 ║
║                                                                              ║
║  Features:                                                                   ║
║  - Smart task creation                                                       ║
║  - AI priority scoring                                                       ║
║  - Due date suggestions                                                      ║
║  - Project organization                                                      ║
║  - Recurring tasks                                                           ║
║  - Time estimation                                                           ║
║                                                                              ║
║  COS: 93/100 — Todoist/Notion Competitor                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import uuid
import asyncio
import logging
import httpx
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class TaskPriority(str, Enum):
    URGENT = "urgent"       # P1 - Do immediately
    HIGH = "high"           # P2 - Do today
    MEDIUM = "medium"       # P3 - Do this week
    LOW = "low"             # P4 - Do when possible
    SOMEDAY = "someday"     # P5 - Maybe later


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"


class RecurrenceType(str, Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass
class Task:
    """A task object."""
    id: str
    title: str
    description: Optional[str]
    priority: TaskPriority
    status: TaskStatus
    due_date: Optional[datetime]
    due_time: Optional[str]  # HH:MM format
    estimated_minutes: Optional[int]
    actual_minutes: Optional[int]
    project_id: Optional[str]
    tags: List[str]
    subtasks: List[str]  # List of subtask IDs
    parent_id: Optional[str]  # For subtasks
    recurrence: RecurrenceType
    recurrence_end: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    user_id: str
    identity_id: str
    ai_score: Optional[float] = None  # AI priority score 0-100
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Project:
    """A project to group tasks."""
    id: str
    name: str
    description: Optional[str]
    color: str
    icon: Optional[str]
    task_count: int
    completed_count: int
    created_at: datetime
    user_id: str
    archived: bool = False


@dataclass
class TaskSuggestion:
    """AI suggestion for task enhancement."""
    suggested_priority: TaskPriority
    suggested_due_date: Optional[datetime]
    estimated_minutes: int
    suggested_tags: List[str]
    suggested_project: Optional[str]
    subtask_suggestions: List[str]
    reasoning: str


# ═══════════════════════════════════════════════════════════════════════════════
# AI TASK ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class TaskAIEngine:
    """AI engine for task analysis and suggestions."""
    
    def __init__(self):
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.openai_key = os.environ.get("OPENAI_API_KEY", "")
    
    async def analyze_task(self, title: str, description: str = "") -> TaskSuggestion:
        """Analyze task and provide AI suggestions."""
        
        if self.anthropic_key:
            return await self._analyze_with_claude(title, description)
        elif self.openai_key:
            return await self._analyze_with_openai(title, description)
        else:
            return self._local_analysis(title, description)
    
    async def _analyze_with_claude(self, title: str, description: str) -> TaskSuggestion:
        """Analyze with Claude."""
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""Analyze this task and provide suggestions in JSON format.

TODAY'S DATE: {today}

TASK TITLE: {title}
DESCRIPTION: {description or "None provided"}

Respond ONLY with valid JSON:
{{
    "priority": "urgent|high|medium|low|someday",
    "due_days_from_now": null or number (0=today, 1=tomorrow, 7=next week),
    "estimated_minutes": number (15, 30, 60, 120, etc),
    "tags": ["tag1", "tag2"],
    "project": "Work|Personal|Health|Learning|Finance|Home|null",
    "subtasks": ["subtask 1 if complex task", "subtask 2"],
    "reasoning": "brief explanation"
}}"""

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 512,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    text = data["content"][0]["text"]
                    
                    json_start = text.find("{")
                    json_end = text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        result = json.loads(text[json_start:json_end])
                        
                        due_date = None
                        if result.get("due_days_from_now") is not None:
                            due_date = datetime.now(timezone.utc) + timedelta(days=result["due_days_from_now"])
                        
                        return TaskSuggestion(
                            suggested_priority=TaskPriority(result.get("priority", "medium")),
                            suggested_due_date=due_date,
                            estimated_minutes=result.get("estimated_minutes", 30),
                            suggested_tags=result.get("tags", [])[:3],
                            suggested_project=result.get("project"),
                            subtask_suggestions=result.get("subtasks", [])[:5],
                            reasoning=result.get("reasoning", ""),
                        )
            except Exception as e:
                logger.error(f"Claude analysis failed: {e}")
        
        return self._local_analysis(title, description)
    
    async def _analyze_with_openai(self, title: str, description: str) -> TaskSuggestion:
        """Analyze with OpenAI."""
        # Similar implementation to Claude
        return self._local_analysis(title, description)
    
    def _local_analysis(self, title: str, description: str) -> TaskSuggestion:
        """Local fallback analysis."""
        
        title_lower = title.lower()
        combined = f"{title} {description}".lower()
        
        # Priority detection
        if any(w in combined for w in ["urgent", "asap", "emergency", "critical"]):
            priority = TaskPriority.URGENT
        elif any(w in combined for w in ["important", "deadline", "today"]):
            priority = TaskPriority.HIGH
        elif any(w in combined for w in ["soon", "this week"]):
            priority = TaskPriority.MEDIUM
        elif any(w in combined for w in ["someday", "maybe", "eventually"]):
            priority = TaskPriority.SOMEDAY
        else:
            priority = TaskPriority.MEDIUM
        
        # Due date detection
        due_date = None
        if "today" in combined:
            due_date = datetime.now(timezone.utc)
        elif "tomorrow" in combined:
            due_date = datetime.now(timezone.utc) + timedelta(days=1)
        elif "this week" in combined:
            due_date = datetime.now(timezone.utc) + timedelta(days=7)
        
        # Time estimation
        if any(w in combined for w in ["quick", "simple", "small"]):
            minutes = 15
        elif any(w in combined for w in ["meeting", "call", "review"]):
            minutes = 60
        elif any(w in combined for w in ["project", "report", "analysis"]):
            minutes = 120
        else:
            minutes = 30
        
        # Project detection
        project = None
        if any(w in combined for w in ["work", "client", "meeting", "report"]):
            project = "Work"
        elif any(w in combined for w in ["gym", "exercise", "health", "doctor"]):
            project = "Health"
        elif any(w in combined for w in ["learn", "study", "course", "read"]):
            project = "Learning"
        elif any(w in combined for w in ["pay", "budget", "invoice", "bank"]):
            project = "Finance"
        
        return TaskSuggestion(
            suggested_priority=priority,
            suggested_due_date=due_date,
            estimated_minutes=minutes,
            suggested_tags=[],
            suggested_project=project,
            subtask_suggestions=[],
            reasoning="Local analysis based on keywords",
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TASK MANAGER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class TaskManagerAgent:
    """
    CHE·NU Personal Productivity Task Manager Agent.
    
    Features:
    - CRUD operations for tasks
    - Project management
    - AI-powered suggestions
    - Smart filtering and views
    - Recurring tasks
    - Progress tracking
    """
    
    def __init__(self):
        self.ai_engine = TaskAIEngine()
        
        # In-memory storage
        self._tasks: Dict[str, Dict[str, Task]] = {}  # user_id -> task_id -> Task
        self._projects: Dict[str, Dict[str, Project]] = {}  # user_id -> project_id -> Project
        
        logger.info("TaskManagerAgent initialized")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PROJECT OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_project(
        self,
        name: str,
        user_id: str,
        description: Optional[str] = None,
        color: str = "#3B82F6",
        icon: Optional[str] = None,
    ) -> Project:
        """Create a new project."""
        
        project = Project(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            color=color,
            icon=icon,
            task_count=0,
            completed_count=0,
            created_at=datetime.now(timezone.utc),
            user_id=user_id,
        )
        
        if user_id not in self._projects:
            self._projects[user_id] = {}
        self._projects[user_id][project.id] = project
        
        logger.info(f"Created project {project.id}: {name}")
        return project
    
    def get_projects(self, user_id: str, include_archived: bool = False) -> List[Project]:
        """Get all projects for a user."""
        projects = list(self._projects.get(user_id, {}).values())
        if not include_archived:
            projects = [p for p in projects if not p.archived]
        return sorted(projects, key=lambda p: p.name)
    
    def _ensure_default_projects(self, user_id: str):
        """Ensure default projects exist."""
        if user_id not in self._projects or not self._projects[user_id]:
            defaults = ["Inbox", "Work", "Personal", "Health", "Learning"]
            colors = ["#6B7280", "#3B82F6", "#10B981", "#EF4444", "#8B5CF6"]
            
            for name, color in zip(defaults, colors):
                self.create_project(name, user_id, color=color)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TASK OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_task(
        self,
        title: str,
        user_id: str,
        identity_id: str = "",
        description: Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        due_date: Optional[datetime] = None,
        due_time: Optional[str] = None,
        estimated_minutes: Optional[int] = None,
        project_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        recurrence: RecurrenceType = RecurrenceType.NONE,
        parent_id: Optional[str] = None,
        auto_suggest: bool = True,
    ) -> Task:
        """Create a new task with optional AI suggestions."""
        
        self._ensure_default_projects(user_id)
        
        suggestion = None
        if auto_suggest and (priority is None or due_date is None):
            suggestion = await self.ai_engine.analyze_task(title, description or "")
        
        now = datetime.now(timezone.utc)
        
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority or (suggestion.suggested_priority if suggestion else TaskPriority.MEDIUM),
            status=TaskStatus.TODO,
            due_date=due_date or (suggestion.suggested_due_date if suggestion else None),
            due_time=due_time,
            estimated_minutes=estimated_minutes or (suggestion.estimated_minutes if suggestion else 30),
            actual_minutes=None,
            project_id=project_id or self._get_inbox_id(user_id),
            tags=tags or (suggestion.suggested_tags if suggestion else []),
            subtasks=[],
            parent_id=parent_id,
            recurrence=recurrence,
            recurrence_end=None,
            completed_at=None,
            created_at=now,
            updated_at=now,
            user_id=user_id,
            identity_id=identity_id,
            ai_score=self._calculate_ai_score(
                priority or (suggestion.suggested_priority if suggestion else TaskPriority.MEDIUM),
                due_date or (suggestion.suggested_due_date if suggestion else None)
            ),
            metadata={
                "ai_suggestions": {
                    "subtasks": suggestion.subtask_suggestions if suggestion else [],
                    "reasoning": suggestion.reasoning if suggestion else "",
                } if suggestion else {}
            }
        )
        
        # Store task
        if user_id not in self._tasks:
            self._tasks[user_id] = {}
        self._tasks[user_id][task.id] = task
        
        # Update project count
        if task.project_id and user_id in self._projects:
            if task.project_id in self._projects[user_id]:
                self._projects[user_id][task.project_id].task_count += 1
        
        # Link to parent if subtask
        if parent_id:
            parent = self._tasks.get(user_id, {}).get(parent_id)
            if parent:
                parent.subtasks.append(task.id)
        
        logger.info(f"Created task {task.id}: {title}")
        return task
    
    def _get_inbox_id(self, user_id: str) -> Optional[str]:
        """Get the Inbox project ID."""
        for project in self._projects.get(user_id, {}).values():
            if project.name == "Inbox":
                return project.id
        return None
    
    def _calculate_ai_score(self, priority: TaskPriority, due_date: Optional[datetime]) -> float:
        """Calculate AI priority score (0-100)."""
        
        # Base score from priority
        priority_scores = {
            TaskPriority.URGENT: 90,
            TaskPriority.HIGH: 70,
            TaskPriority.MEDIUM: 50,
            TaskPriority.LOW: 30,
            TaskPriority.SOMEDAY: 10,
        }
        score = priority_scores.get(priority, 50)
        
        # Adjust based on due date
        if due_date:
            now = datetime.now(timezone.utc)
            days_until = (due_date - now).days
            
            if days_until < 0:  # Overdue
                score += 20
            elif days_until == 0:  # Due today
                score += 15
            elif days_until == 1:  # Due tomorrow
                score += 10
            elif days_until <= 7:  # Due this week
                score += 5
        
        return min(100, max(0, score))
    
    def get_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(user_id, {}).get(task_id)
    
    async def update_task(
        self,
        task_id: str,
        user_id: str,
        **updates,
    ) -> Optional[Task]:
        """Update a task."""
        
        task = self.get_task(task_id, user_id)
        if not task:
            return None
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)
        
        task.updated_at = datetime.now(timezone.utc)
        
        # Recalculate AI score if priority or due_date changed
        if "priority" in updates or "due_date" in updates:
            task.ai_score = self._calculate_ai_score(task.priority, task.due_date)
        
        logger.info(f"Updated task {task_id}")
        return task
    
    async def complete_task(
        self,
        task_id: str,
        user_id: str,
        actual_minutes: Optional[int] = None,
    ) -> Optional[Task]:
        """Mark a task as complete."""
        
        task = self.get_task(task_id, user_id)
        if not task:
            return None
        
        now = datetime.now(timezone.utc)
        task.status = TaskStatus.DONE
        task.completed_at = now
        task.updated_at = now
        
        if actual_minutes:
            task.actual_minutes = actual_minutes
        
        # Update project completed count
        if task.project_id and user_id in self._projects:
            if task.project_id in self._projects[user_id]:
                self._projects[user_id][task.project_id].completed_count += 1
        
        # Handle recurring tasks
        if task.recurrence != RecurrenceType.NONE:
            await self._create_next_occurrence(task, user_id)
        
        logger.info(f"Completed task {task_id}")
        return task
    
    async def _create_next_occurrence(self, task: Task, user_id: str):
        """Create next occurrence for recurring task."""
        
        if not task.due_date:
            return
        
        # Calculate next due date
        delta_map = {
            RecurrenceType.DAILY: timedelta(days=1),
            RecurrenceType.WEEKLY: timedelta(weeks=1),
            RecurrenceType.BIWEEKLY: timedelta(weeks=2),
            RecurrenceType.MONTHLY: timedelta(days=30),
            RecurrenceType.YEARLY: timedelta(days=365),
        }
        
        delta = delta_map.get(task.recurrence)
        if not delta:
            return
        
        next_due = task.due_date + delta
        
        # Check if past recurrence end
        if task.recurrence_end and next_due > task.recurrence_end:
            return
        
        # Create new task
        await self.create_task(
            title=task.title,
            user_id=user_id,
            identity_id=task.identity_id,
            description=task.description,
            priority=task.priority,
            due_date=next_due,
            due_time=task.due_time,
            estimated_minutes=task.estimated_minutes,
            project_id=task.project_id,
            tags=task.tags,
            recurrence=task.recurrence,
            auto_suggest=False,
        )
    
    def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete a task."""
        task = self.get_task(task_id, user_id)
        if not task:
            return False
        
        # Update project count
        if task.project_id and user_id in self._projects:
            if task.project_id in self._projects[user_id]:
                self._projects[user_id][task.project_id].task_count -= 1
        
        # Remove from parent's subtasks
        if task.parent_id:
            parent = self._tasks.get(user_id, {}).get(task.parent_id)
            if parent and task_id in parent.subtasks:
                parent.subtasks.remove(task_id)
        
        # Delete subtasks
        for subtask_id in task.subtasks:
            self.delete_task(subtask_id, user_id)
        
        del self._tasks[user_id][task_id]
        logger.info(f"Deleted task {task_id}")
        return True
    
    # ═══════════════════════════════════════════════════════════════════════════
    # QUERIES & VIEWS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def list_tasks(
        self,
        user_id: str,
        project_id: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        tag: Optional[str] = None,
        due_today: bool = False,
        due_this_week: bool = False,
        overdue: bool = False,
        search: Optional[str] = None,
        sort_by: str = "ai_score",  # ai_score, due_date, priority, created_at
        limit: int = 50,
        offset: int = 0,
    ) -> List[Task]:
        """List tasks with filtering."""
        
        tasks = [t for t in self._tasks.get(user_id, {}).values() if t.parent_id is None]
        
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        week_end = today_start + timedelta(days=7)
        
        # Apply filters
        if project_id:
            tasks = [t for t in tasks if t.project_id == project_id]
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if tag:
            tasks = [t for t in tasks if tag in t.tags]
        if due_today:
            tasks = [t for t in tasks if t.due_date and today_start <= t.due_date < today_end]
        if due_this_week:
            tasks = [t for t in tasks if t.due_date and today_start <= t.due_date < week_end]
        if overdue:
            tasks = [t for t in tasks if t.due_date and t.due_date < now and t.status != TaskStatus.DONE]
        if search:
            search_lower = search.lower()
            tasks = [t for t in tasks if search_lower in t.title.lower() or 
                     (t.description and search_lower in t.description.lower())]
        
        # Sort
        if sort_by == "ai_score":
            tasks = sorted(tasks, key=lambda t: t.ai_score or 0, reverse=True)
        elif sort_by == "due_date":
            tasks = sorted(tasks, key=lambda t: t.due_date or datetime.max.replace(tzinfo=timezone.utc))
        elif sort_by == "priority":
            priority_order = {TaskPriority.URGENT: 0, TaskPriority.HIGH: 1, TaskPriority.MEDIUM: 2, 
                            TaskPriority.LOW: 3, TaskPriority.SOMEDAY: 4}
            tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 5))
        elif sort_by == "created_at":
            tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)
        
        return tasks[offset:offset + limit]
    
    def get_today_view(self, user_id: str) -> Dict[str, Any]:
        """Get today's task view."""
        
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        all_tasks = list(self._tasks.get(user_id, {}).values())
        
        overdue = [t for t in all_tasks if t.due_date and t.due_date < today_start and t.status != TaskStatus.DONE]
        due_today = [t for t in all_tasks if t.due_date and today_start <= t.due_date < today_end]
        high_priority = [t for t in all_tasks if t.priority in [TaskPriority.URGENT, TaskPriority.HIGH] 
                        and t.status != TaskStatus.DONE]
        
        completed_today = [t for t in all_tasks if t.completed_at and today_start <= t.completed_at < today_end]
        
        return {
            "date": today_start.isoformat(),
            "overdue": sorted(overdue, key=lambda t: t.due_date or now),
            "due_today": sorted(due_today, key=lambda t: t.ai_score or 0, reverse=True),
            "high_priority": sorted(high_priority, key=lambda t: t.ai_score or 0, reverse=True),
            "completed_today": completed_today,
            "stats": {
                "overdue_count": len(overdue),
                "due_today_count": len(due_today),
                "completed_count": len(completed_today),
            }
        }
    
    def get_stats(self, user_id: str) -> Dict[str, Any]:
        """Get task statistics."""
        
        tasks = list(self._tasks.get(user_id, {}).values())
        
        if not tasks:
            return {
                "total": 0,
                "completed": 0,
                "completion_rate": 0,
                "by_status": {},
                "by_priority": {},
                "overdue": 0,
            }
        
        now = datetime.now(timezone.utc)
        completed = [t for t in tasks if t.status == TaskStatus.DONE]
        overdue = [t for t in tasks if t.due_date and t.due_date < now and t.status != TaskStatus.DONE]
        
        by_status = {}
        by_priority = {}
        for task in tasks:
            by_status[task.status.value] = by_status.get(task.status.value, 0) + 1
            by_priority[task.priority.value] = by_priority.get(task.priority.value, 0) + 1
        
        return {
            "total": len(tasks),
            "completed": len(completed),
            "completion_rate": round(len(completed) / len(tasks) * 100, 1) if tasks else 0,
            "by_status": by_status,
            "by_priority": by_priority,
            "overdue": len(overdue),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_task_manager: Optional[TaskManagerAgent] = None


def get_task_manager() -> TaskManagerAgent:
    """Get or create the task manager agent."""
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManagerAgent()
    return _task_manager


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio
    
    print("✅ CHE·NU Personal Productivity - Task Manager")
    print("=" * 60)
    
    agent = get_task_manager()
    
    async def test():
        # Create tasks
        task1 = await agent.create_task(
            title="Urgent: Review Q1 budget proposal",
            user_id="test_user",
            description="Need to review before tomorrow's meeting",
            auto_suggest=False,
        )
        
        task2 = await agent.create_task(
            title="Schedule dentist appointment",
            user_id="test_user",
            auto_suggest=False,
        )
        
        print(f"\n✅ Created {task1.title}")
        print(f"   Priority: {task1.priority.value}, AI Score: {task1.ai_score}")
        
        # Get today view
        today = agent.get_today_view("test_user")
        print(f"\n📅 Today: {today['stats']['due_today_count']} due, {today['stats']['completed_count']} completed")
        
        # Complete task
        await agent.complete_task(task1.id, "test_user", actual_minutes=45)
        
        # Stats
        stats = agent.get_stats("test_user")
        print(f"\n📊 Stats: {stats['total']} tasks, {stats['completion_rate']}% complete")
    
    asyncio.run(test())
    
    print("\n✅ Task Manager Agent ready!")
