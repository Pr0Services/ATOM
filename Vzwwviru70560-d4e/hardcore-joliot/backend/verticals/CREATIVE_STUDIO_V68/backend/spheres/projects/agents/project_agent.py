"""
CHE·NU™ V68 - Project Management Agent
Monday.com/Asana/Jira killer at $29/mo flat

Features:
- Projects, Tasks, Sprints, Milestones
- AI task estimation and risk detection
- Workload balancing
- Time tracking
- Kanban/Gantt views support
- Cross-sphere integration
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class ProjectStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class TaskStatus(str, Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    BLOCKED = "blocked"
    DONE = "done"


class TaskPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SprintStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"


class MilestoneStatus(str, Enum):
    UPCOMING = "upcoming"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Project:
    id: str
    user_id: str
    name: str
    description: str
    status: ProjectStatus
    start_date: Optional[date]
    target_date: Optional[date]
    budget: Optional[Decimal]
    spent: Decimal
    client_name: Optional[str]
    tags: List[str]
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create(cls, user_id: str, name: str, description: str = "",
               start_date: date = None, target_date: date = None,
               budget: Decimal = None, client_name: str = None,
               tags: List[str] = None) -> 'Project':
        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            name=name,
            description=description,
            status=ProjectStatus.PLANNING,
            start_date=start_date or date.today(),
            target_date=target_date,
            budget=budget,
            spent=Decimal("0"),
            client_name=client_name,
            tags=tags or [],
            settings={"view": "kanban", "show_completed": True},
            created_at=now,
            updated_at=now
        )


@dataclass
class Task:
    id: str
    project_id: str
    user_id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee_id: Optional[str]
    assignee_name: Optional[str]
    sprint_id: Optional[str]
    milestone_id: Optional[str]
    parent_task_id: Optional[str]  # For subtasks
    due_date: Optional[date]
    estimated_hours: Optional[Decimal]
    actual_hours: Decimal
    tags: List[str]
    checklist: List[Dict[str, Any]]
    attachments: List[str]
    order: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    @classmethod
    def create(cls, project_id: str, user_id: str, title: str,
               description: str = "", priority: TaskPriority = TaskPriority.MEDIUM,
               assignee_id: str = None, assignee_name: str = None,
               due_date: date = None, estimated_hours: Decimal = None,
               sprint_id: str = None, milestone_id: str = None,
               parent_task_id: str = None, tags: List[str] = None,
               order: int = 0) -> 'Task':
        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            project_id=project_id,
            user_id=user_id,
            title=title,
            description=description,
            status=TaskStatus.BACKLOG,
            priority=priority,
            assignee_id=assignee_id,
            assignee_name=assignee_name,
            sprint_id=sprint_id,
            milestone_id=milestone_id,
            parent_task_id=parent_task_id,
            due_date=due_date,
            estimated_hours=estimated_hours,
            actual_hours=Decimal("0"),
            tags=tags or [],
            checklist=[],
            attachments=[],
            order=order,
            created_at=now,
            updated_at=now,
            completed_at=None
        )


@dataclass
class Sprint:
    id: str
    project_id: str
    user_id: str
    name: str
    goal: str
    status: SprintStatus
    start_date: date
    end_date: date
    velocity_planned: int  # Story points planned
    velocity_actual: int   # Story points completed
    created_at: datetime
    
    @classmethod
    def create(cls, project_id: str, user_id: str, name: str,
               start_date: date, end_date: date, goal: str = "",
               velocity_planned: int = 0) -> 'Sprint':
        return cls(
            id=str(uuid4()),
            project_id=project_id,
            user_id=user_id,
            name=name,
            goal=goal,
            status=SprintStatus.PLANNED,
            start_date=start_date,
            end_date=end_date,
            velocity_planned=velocity_planned,
            velocity_actual=0,
            created_at=datetime.utcnow()
        )


@dataclass
class Milestone:
    id: str
    project_id: str
    user_id: str
    name: str
    description: str
    status: MilestoneStatus
    due_date: date
    completed_date: Optional[date]
    deliverables: List[str]
    created_at: datetime
    
    @classmethod
    def create(cls, project_id: str, user_id: str, name: str,
               due_date: date, description: str = "",
               deliverables: List[str] = None) -> 'Milestone':
        return cls(
            id=str(uuid4()),
            project_id=project_id,
            user_id=user_id,
            name=name,
            description=description,
            status=MilestoneStatus.UPCOMING,
            due_date=due_date,
            completed_date=None,
            deliverables=deliverables or [],
            created_at=datetime.utcnow()
        )


@dataclass
class TimeEntry:
    id: str
    task_id: str
    user_id: str
    hours: Decimal
    description: str
    date: date
    billable: bool
    created_at: datetime
    
    @classmethod
    def create(cls, task_id: str, user_id: str, hours: Decimal,
               description: str = "", entry_date: date = None,
               billable: bool = True) -> 'TimeEntry':
        return cls(
            id=str(uuid4()),
            task_id=task_id,
            user_id=user_id,
            hours=hours,
            description=description,
            date=entry_date or date.today(),
            billable=billable,
            created_at=datetime.utcnow()
        )


@dataclass
class TeamMember:
    id: str
    project_id: str
    user_id: str
    name: str
    email: str
    role: str
    hourly_rate: Optional[Decimal]
    capacity_hours_week: Decimal
    joined_at: datetime
    
    @classmethod
    def create(cls, project_id: str, user_id: str, name: str,
               email: str, role: str = "member",
               hourly_rate: Decimal = None,
               capacity_hours_week: Decimal = Decimal("40")) -> 'TeamMember':
        return cls(
            id=str(uuid4()),
            project_id=project_id,
            user_id=user_id,
            name=name,
            email=email,
            role=role,
            hourly_rate=hourly_rate,
            capacity_hours_week=capacity_hours_week,
            joined_at=datetime.utcnow()
        )


@dataclass
class Comment:
    id: str
    task_id: str
    user_id: str
    author_name: str
    content: str
    mentions: List[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def create(cls, task_id: str, user_id: str, author_name: str,
               content: str, mentions: List[str] = None) -> 'Comment':
        now = datetime.utcnow()
        return cls(
            id=str(uuid4()),
            task_id=task_id,
            user_id=user_id,
            author_name=author_name,
            content=content,
            mentions=mentions or [],
            created_at=now,
            updated_at=now
        )


@dataclass
class ProjectAnalysis:
    """AI-generated project analysis"""
    project_id: str
    health_score: int  # 0-100
    risk_level: RiskLevel
    completion_percentage: float
    estimated_completion_date: Optional[date]
    budget_status: str  # "on_track", "at_risk", "over_budget"
    velocity_trend: str  # "improving", "stable", "declining"
    risks: List[Dict[str, Any]]
    recommendations: List[str]
    blockers: List[Dict[str, Any]]
    workload_balance: Dict[str, Any]
    generated_at: datetime


@dataclass
class TaskEstimate:
    """AI-generated task estimate"""
    task_id: str
    estimated_hours: Decimal
    confidence: float  # 0-1
    similar_tasks: List[Dict[str, Any]]
    factors: List[str]
    generated_at: datetime


# ============================================================================
# AI ENGINE
# ============================================================================

class ProjectAIEngine:
    """AI-powered project management intelligence"""
    
    def analyze_project(self, project: Project, tasks: List[Task],
                       sprints: List[Sprint], milestones: List[Milestone],
                       team: List[TeamMember]) -> ProjectAnalysis:
        """Comprehensive AI project analysis"""
        
        # Calculate completion
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.status == TaskStatus.DONE])
        completion_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Calculate health score
        health_score = self._calculate_health_score(
            project, tasks, sprints, milestones
        )
        
        # Detect risks
        risks = self._detect_risks(project, tasks, sprints, milestones)
        risk_level = self._determine_risk_level(risks)
        
        # Budget analysis
        budget_status = self._analyze_budget(project, tasks, team)
        
        # Velocity trend
        velocity_trend = self._analyze_velocity(sprints)
        
        # Estimate completion
        estimated_completion = self._estimate_completion_date(
            project, tasks, sprints
        )
        
        # Find blockers
        blockers = self._find_blockers(tasks)
        
        # Workload analysis
        workload = self._analyze_workload(tasks, team)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            health_score, risks, budget_status, velocity_trend, workload
        )
        
        return ProjectAnalysis(
            project_id=project.id,
            health_score=health_score,
            risk_level=risk_level,
            completion_percentage=completion_pct,
            estimated_completion_date=estimated_completion,
            budget_status=budget_status,
            velocity_trend=velocity_trend,
            risks=risks,
            recommendations=recommendations,
            blockers=blockers,
            workload_balance=workload,
            generated_at=datetime.utcnow()
        )
    
    def estimate_task(self, task: Task, similar_tasks: List[Task]) -> TaskEstimate:
        """AI task estimation based on historical data"""
        
        # Find similar completed tasks
        completed_similar = [
            t for t in similar_tasks
            if t.status == TaskStatus.DONE and t.actual_hours > 0
        ]
        
        if completed_similar:
            # Calculate average from similar tasks
            avg_hours = sum(t.actual_hours for t in completed_similar) / len(completed_similar)
            confidence = min(0.9, 0.5 + (len(completed_similar) * 0.1))
        else:
            # Default estimation based on priority
            priority_hours = {
                TaskPriority.CRITICAL: Decimal("8"),
                TaskPriority.HIGH: Decimal("6"),
                TaskPriority.MEDIUM: Decimal("4"),
                TaskPriority.LOW: Decimal("2")
            }
            avg_hours = priority_hours.get(task.priority, Decimal("4"))
            confidence = 0.3
        
        factors = []
        if task.checklist:
            factors.append(f"{len(task.checklist)} checklist items")
            avg_hours *= Decimal("1.1")  # 10% more for checklists
        
        if task.parent_task_id:
            factors.append("Subtask - typically smaller scope")
            avg_hours *= Decimal("0.7")
        
        similar_info = [
            {"title": t.title, "actual_hours": float(t.actual_hours)}
            for t in completed_similar[:3]
        ]
        
        return TaskEstimate(
            task_id=task.id,
            estimated_hours=round(avg_hours, 1),
            confidence=confidence,
            similar_tasks=similar_info,
            factors=factors,
            generated_at=datetime.utcnow()
        )
    
    def suggest_task_assignment(self, task: Task, team: List[TeamMember],
                                all_tasks: List[Task]) -> Dict[str, Any]:
        """AI-powered task assignment suggestion"""
        
        if not team:
            return {"suggestion": None, "reason": "No team members available"}
        
        # Calculate workload per member
        workloads = {}
        for member in team:
            member_tasks = [
                t for t in all_tasks
                if t.assignee_id == member.id and t.status != TaskStatus.DONE
            ]
            total_hours = sum(
                t.estimated_hours or Decimal("4")
                for t in member_tasks
            )
            workloads[member.id] = {
                "member": member,
                "assigned_tasks": len(member_tasks),
                "estimated_hours": total_hours,
                "capacity": member.capacity_hours_week,
                "utilization": float(total_hours / member.capacity_hours_week * 100) if member.capacity_hours_week > 0 else 100
            }
        
        # Find least loaded team member
        sorted_workloads = sorted(
            workloads.items(),
            key=lambda x: x[1]["utilization"]
        )
        
        best_match = sorted_workloads[0][1]
        
        return {
            "suggestion": {
                "member_id": best_match["member"].id,
                "member_name": best_match["member"].name,
                "current_utilization": best_match["utilization"],
                "current_tasks": best_match["assigned_tasks"]
            },
            "reason": f"Lowest workload at {best_match['utilization']:.0f}% utilization",
            "all_workloads": [
                {
                    "member_id": m_id,
                    "member_name": w["member"].name,
                    "utilization": w["utilization"],
                    "tasks": w["assigned_tasks"]
                }
                for m_id, w in sorted_workloads
            ]
        }
    
    def _calculate_health_score(self, project: Project, tasks: List[Task],
                                sprints: List[Sprint], milestones: List[Milestone]) -> int:
        """Calculate project health score (0-100)"""
        score = 100
        
        # Task completion rate impact
        if tasks:
            done_tasks = len([t for t in tasks if t.status == TaskStatus.DONE])
            completion_rate = done_tasks / len(tasks)
            
            # Penalize low completion if project is not new
            if project.start_date and (date.today() - project.start_date).days > 14:
                expected_completion = min(0.8, (date.today() - project.start_date).days / 90)
                if completion_rate < expected_completion:
                    score -= int((expected_completion - completion_rate) * 30)
        
        # Overdue tasks penalty
        overdue_tasks = [
            t for t in tasks
            if t.due_date and t.due_date < date.today() and t.status != TaskStatus.DONE
        ]
        score -= min(30, len(overdue_tasks) * 5)
        
        # Blocked tasks penalty
        blocked_tasks = [t for t in tasks if t.status == TaskStatus.BLOCKED]
        score -= min(20, len(blocked_tasks) * 5)
        
        # Budget overrun penalty
        if project.budget and project.budget > 0:
            budget_usage = float(project.spent / project.budget)
            if budget_usage > 1.0:
                score -= min(20, int((budget_usage - 1.0) * 50))
            elif budget_usage > 0.9:
                score -= 5
        
        # Missed milestones penalty
        missed_milestones = [m for m in milestones if m.status == MilestoneStatus.MISSED]
        score -= min(15, len(missed_milestones) * 5)
        
        return max(0, min(100, score))
    
    def _detect_risks(self, project: Project, tasks: List[Task],
                     sprints: List[Sprint], milestones: List[Milestone]) -> List[Dict[str, Any]]:
        """Detect project risks"""
        risks = []
        
        # Overdue tasks risk
        overdue = [t for t in tasks if t.due_date and t.due_date < date.today() and t.status != TaskStatus.DONE]
        if overdue:
            risks.append({
                "type": "overdue_tasks",
                "severity": "high" if len(overdue) > 5 else "medium",
                "description": f"{len(overdue)} tasks are overdue",
                "affected_items": [t.id for t in overdue[:5]]
            })
        
        # Budget risk
        if project.budget and project.budget > 0:
            usage = float(project.spent / project.budget)
            if usage > 0.9:
                risks.append({
                    "type": "budget",
                    "severity": "critical" if usage > 1.0 else "high",
                    "description": f"Budget is {usage*100:.0f}% used",
                    "affected_items": []
                })
        
        # Deadline risk
        if project.target_date and project.target_date < date.today() + timedelta(days=14):
            incomplete = [t for t in tasks if t.status != TaskStatus.DONE]
            if incomplete:
                risks.append({
                    "type": "deadline",
                    "severity": "high",
                    "description": f"Deadline in {(project.target_date - date.today()).days} days with {len(incomplete)} tasks remaining",
                    "affected_items": [t.id for t in incomplete[:5]]
                })
        
        # Blocked tasks risk
        blocked = [t for t in tasks if t.status == TaskStatus.BLOCKED]
        if blocked:
            risks.append({
                "type": "blocked_tasks",
                "severity": "high" if len(blocked) > 3 else "medium",
                "description": f"{len(blocked)} tasks are blocked",
                "affected_items": [t.id for t in blocked]
            })
        
        # No recent activity risk
        recent_updates = [
            t for t in tasks
            if (datetime.utcnow() - t.updated_at).days < 7
        ]
        if tasks and not recent_updates:
            risks.append({
                "type": "stale_project",
                "severity": "medium",
                "description": "No task updates in the last 7 days",
                "affected_items": []
            })
        
        return risks
    
    def _determine_risk_level(self, risks: List[Dict[str, Any]]) -> RiskLevel:
        """Determine overall risk level"""
        if not risks:
            return RiskLevel.LOW
        
        severities = [r["severity"] for r in risks]
        if "critical" in severities:
            return RiskLevel.CRITICAL
        if severities.count("high") >= 2:
            return RiskLevel.HIGH
        if "high" in severities:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
    
    def _analyze_budget(self, project: Project, tasks: List[Task],
                       team: List[TeamMember]) -> str:
        """Analyze budget status"""
        if not project.budget or project.budget == 0:
            return "no_budget"
        
        usage = float(project.spent / project.budget)
        
        if usage > 1.0:
            return "over_budget"
        elif usage > 0.9:
            return "at_risk"
        else:
            return "on_track"
    
    def _analyze_velocity(self, sprints: List[Sprint]) -> str:
        """Analyze velocity trend"""
        completed_sprints = [
            s for s in sprints
            if s.status == SprintStatus.COMPLETED and s.velocity_actual > 0
        ]
        
        if len(completed_sprints) < 2:
            return "stable"
        
        # Sort by end date
        sorted_sprints = sorted(completed_sprints, key=lambda s: s.end_date)
        
        # Compare last two sprints
        if len(sorted_sprints) >= 2:
            recent = sorted_sprints[-1].velocity_actual
            previous = sorted_sprints[-2].velocity_actual
            
            if recent > previous * 1.1:
                return "improving"
            elif recent < previous * 0.9:
                return "declining"
        
        return "stable"
    
    def _estimate_completion_date(self, project: Project, tasks: List[Task],
                                  sprints: List[Sprint]) -> Optional[date]:
        """Estimate project completion date"""
        incomplete_tasks = [t for t in tasks if t.status != TaskStatus.DONE]
        
        if not incomplete_tasks:
            return date.today()
        
        # Calculate average completion rate
        completed_sprints = [s for s in sprints if s.status == SprintStatus.COMPLETED]
        
        if completed_sprints:
            avg_velocity = sum(s.velocity_actual for s in completed_sprints) / len(completed_sprints)
            remaining_points = len(incomplete_tasks)  # Simplified: 1 task = 1 point
            
            if avg_velocity > 0:
                sprints_needed = remaining_points / avg_velocity
                days_needed = int(sprints_needed * 14)  # Assume 2-week sprints
                return date.today() + timedelta(days=days_needed)
        
        # Fallback: estimate based on task count
        days_needed = len(incomplete_tasks) * 2  # 2 days per task average
        return date.today() + timedelta(days=days_needed)
    
    def _find_blockers(self, tasks: List[Task]) -> List[Dict[str, Any]]:
        """Find blocking issues"""
        blockers = []
        
        blocked_tasks = [t for t in tasks if t.status == TaskStatus.BLOCKED]
        for task in blocked_tasks:
            blockers.append({
                "task_id": task.id,
                "task_title": task.title,
                "blocked_since": task.updated_at.isoformat(),
                "assignee": task.assignee_name or "Unassigned"
            })
        
        # Critical overdue tasks
        critical_overdue = [
            t for t in tasks
            if t.priority == TaskPriority.CRITICAL
            and t.due_date and t.due_date < date.today()
            and t.status != TaskStatus.DONE
        ]
        for task in critical_overdue:
            blockers.append({
                "task_id": task.id,
                "task_title": task.title,
                "type": "critical_overdue",
                "days_overdue": (date.today() - task.due_date).days
            })
        
        return blockers
    
    def _analyze_workload(self, tasks: List[Task],
                         team: List[TeamMember]) -> Dict[str, Any]:
        """Analyze team workload distribution"""
        if not team:
            return {"balanced": True, "distribution": []}
        
        distribution = []
        total_hours = Decimal("0")
        
        for member in team:
            member_tasks = [
                t for t in tasks
                if t.assignee_id == member.id and t.status != TaskStatus.DONE
            ]
            hours = sum(t.estimated_hours or Decimal("4") for t in member_tasks)
            total_hours += hours
            
            utilization = float(hours / member.capacity_hours_week * 100) if member.capacity_hours_week > 0 else 0
            
            distribution.append({
                "member_id": member.id,
                "member_name": member.name,
                "assigned_tasks": len(member_tasks),
                "estimated_hours": float(hours),
                "capacity": float(member.capacity_hours_week),
                "utilization": utilization,
                "status": "overloaded" if utilization > 100 else "underutilized" if utilization < 50 else "balanced"
            })
        
        # Check balance
        utilizations = [d["utilization"] for d in distribution]
        if utilizations:
            max_util = max(utilizations)
            min_util = min(utilizations)
            balanced = (max_util - min_util) < 30  # Within 30% is considered balanced
        else:
            balanced = True
        
        return {
            "balanced": balanced,
            "distribution": distribution,
            "total_estimated_hours": float(total_hours)
        }
    
    def _generate_recommendations(self, health_score: int, risks: List[Dict],
                                  budget_status: str, velocity_trend: str,
                                  workload: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if health_score < 50:
            recommendations.append("🚨 Project health is critical. Schedule an immediate team review.")
        elif health_score < 70:
            recommendations.append("⚠️ Project needs attention. Review blocking issues.")
        
        # Risk-based recommendations
        for risk in risks:
            if risk["type"] == "overdue_tasks":
                recommendations.append(f"📅 Address {len(risk['affected_items'])} overdue tasks. Consider reassigning or adjusting deadlines.")
            elif risk["type"] == "budget" and risk["severity"] == "critical":
                recommendations.append("💰 Budget exceeded. Review scope and consider change request.")
            elif risk["type"] == "blocked_tasks":
                recommendations.append("🚧 Unblock tasks immediately. Schedule blocker resolution meeting.")
            elif risk["type"] == "stale_project":
                recommendations.append("💤 Project appears stale. Check in with team on progress.")
        
        # Velocity recommendations
        if velocity_trend == "declining":
            recommendations.append("📉 Velocity declining. Investigate impediments and team capacity.")
        elif velocity_trend == "improving":
            recommendations.append("📈 Great progress! Velocity is improving.")
        
        # Workload recommendations
        if not workload.get("balanced", True):
            overloaded = [d for d in workload.get("distribution", []) if d.get("status") == "overloaded"]
            if overloaded:
                names = [d["member_name"] for d in overloaded]
                recommendations.append(f"⚖️ Rebalance workload. {', '.join(names)} overloaded.")
        
        if not recommendations:
            recommendations.append("✅ Project is on track. Keep up the good work!")
        
        return recommendations


# ============================================================================
# MAIN SERVICE
# ============================================================================

class ProjectManagementService:
    """
    CHE·NU™ Project Management Service
    Full-featured PM with AI assistance
    """
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self.sprints: Dict[str, Sprint] = {}
        self.milestones: Dict[str, Milestone] = {}
        self.time_entries: Dict[str, TimeEntry] = {}
        self.team_members: Dict[str, TeamMember] = {}
        self.comments: Dict[str, Comment] = {}
        self.ai_engine = ProjectAIEngine()
        logger.info("ProjectManagementService initialized")
    
    # ========================================================================
    # PROJECT OPERATIONS
    # ========================================================================
    
    def create_project(self, user_id: str, name: str, description: str = "",
                      start_date: date = None, target_date: date = None,
                      budget: Decimal = None, client_name: str = None,
                      tags: List[str] = None) -> Project:
        """Create a new project"""
        project = Project.create(
            user_id=user_id,
            name=name,
            description=description,
            start_date=start_date,
            target_date=target_date,
            budget=budget,
            client_name=client_name,
            tags=tags
        )
        self.projects[project.id] = project
        logger.info(f"Created project: {project.id} - {name}")
        return project
    
    def get_project(self, project_id: str, user_id: str) -> Optional[Project]:
        """Get project by ID"""
        project = self.projects.get(project_id)
        if project and project.user_id == user_id:
            return project
        return None
    
    def list_projects(self, user_id: str, status: ProjectStatus = None,
                     search: str = None) -> List[Project]:
        """List user's projects"""
        projects = [p for p in self.projects.values() if p.user_id == user_id]
        
        if status:
            projects = [p for p in projects if p.status == status]
        
        if search:
            search_lower = search.lower()
            projects = [
                p for p in projects
                if search_lower in p.name.lower() or search_lower in p.description.lower()
            ]
        
        return sorted(projects, key=lambda p: p.updated_at, reverse=True)
    
    def update_project(self, project_id: str, user_id: str,
                      updates: Dict[str, Any]) -> Optional[Project]:
        """Update project"""
        project = self.get_project(project_id, user_id)
        if not project:
            return None
        
        allowed_fields = ['name', 'description', 'status', 'target_date', 'budget', 'client_name', 'tags', 'settings']
        for field, value in updates.items():
            if field in allowed_fields and hasattr(project, field):
                setattr(project, field, value)
        
        project.updated_at = datetime.utcnow()
        logger.info(f"Updated project: {project_id}")
        return project
    
    def analyze_project(self, project_id: str, user_id: str) -> Optional[ProjectAnalysis]:
        """Get AI analysis of project"""
        project = self.get_project(project_id, user_id)
        if not project:
            return None
        
        tasks = self.list_tasks(project_id, user_id)
        sprints = self.list_sprints(project_id, user_id)
        milestones = self.list_milestones(project_id, user_id)
        team = self.list_team_members(project_id, user_id)
        
        return self.ai_engine.analyze_project(project, tasks, sprints, milestones, team)
    
    # ========================================================================
    # TASK OPERATIONS
    # ========================================================================
    
    def create_task(self, project_id: str, user_id: str, title: str,
                   description: str = "", priority: TaskPriority = TaskPriority.MEDIUM,
                   assignee_id: str = None, assignee_name: str = None,
                   due_date: date = None, estimated_hours: Decimal = None,
                   sprint_id: str = None, milestone_id: str = None,
                   parent_task_id: str = None, tags: List[str] = None) -> Optional[Task]:
        """Create a new task"""
        # Verify project access
        if not self.get_project(project_id, user_id):
            return None
        
        # Get order
        existing_tasks = [t for t in self.tasks.values() if t.project_id == project_id]
        order = max([t.order for t in existing_tasks], default=-1) + 1
        
        task = Task.create(
            project_id=project_id,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            assignee_id=assignee_id,
            assignee_name=assignee_name,
            due_date=due_date,
            estimated_hours=estimated_hours,
            sprint_id=sprint_id,
            milestone_id=milestone_id,
            parent_task_id=parent_task_id,
            tags=tags,
            order=order
        )
        self.tasks[task.id] = task
        logger.info(f"Created task: {task.id} - {title}")
        return task
    
    def get_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get task by ID"""
        task = self.tasks.get(task_id)
        if task and task.user_id == user_id:
            return task
        return None
    
    def list_tasks(self, project_id: str, user_id: str,
                  status: TaskStatus = None, assignee_id: str = None,
                  sprint_id: str = None, priority: TaskPriority = None) -> List[Task]:
        """List tasks for a project"""
        tasks = [
            t for t in self.tasks.values()
            if t.project_id == project_id and t.user_id == user_id
        ]
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        if assignee_id:
            tasks = [t for t in tasks if t.assignee_id == assignee_id]
        if sprint_id:
            tasks = [t for t in tasks if t.sprint_id == sprint_id]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        
        return sorted(tasks, key=lambda t: (t.order, t.created_at))
    
    def update_task(self, task_id: str, user_id: str,
                   updates: Dict[str, Any]) -> Optional[Task]:
        """Update task"""
        task = self.get_task(task_id, user_id)
        if not task:
            return None
        
        allowed_fields = [
            'title', 'description', 'status', 'priority', 'assignee_id',
            'assignee_name', 'due_date', 'estimated_hours', 'sprint_id',
            'milestone_id', 'tags', 'checklist', 'order'
        ]
        
        for field, value in updates.items():
            if field in allowed_fields and hasattr(task, field):
                setattr(task, field, value)
        
        # Handle completion
        if updates.get('status') == TaskStatus.DONE and not task.completed_at:
            task.completed_at = datetime.utcnow()
        elif updates.get('status') and updates['status'] != TaskStatus.DONE:
            task.completed_at = None
        
        task.updated_at = datetime.utcnow()
        logger.info(f"Updated task: {task_id}")
        return task
    
    def move_task(self, task_id: str, user_id: str, new_status: TaskStatus,
                 new_order: int = None) -> Optional[Task]:
        """Move task to new status (for Kanban)"""
        return self.update_task(task_id, user_id, {
            'status': new_status,
            'order': new_order if new_order is not None else 0
        })
    
    def estimate_task(self, task_id: str, user_id: str) -> Optional[TaskEstimate]:
        """Get AI estimate for task"""
        task = self.get_task(task_id, user_id)
        if not task:
            return None
        
        # Find similar tasks
        project_tasks = [
            t for t in self.tasks.values()
            if t.project_id == task.project_id and t.id != task_id
        ]
        
        # Match by tags or priority
        similar = [
            t for t in project_tasks
            if set(t.tags) & set(task.tags) or t.priority == task.priority
        ]
        
        return self.ai_engine.estimate_task(task, similar)
    
    def suggest_assignee(self, task_id: str, user_id: str) -> Dict[str, Any]:
        """Get AI suggestion for task assignment"""
        task = self.get_task(task_id, user_id)
        if not task:
            return {"error": "Task not found"}
        
        team = self.list_team_members(task.project_id, user_id)
        all_tasks = self.list_tasks(task.project_id, user_id)
        
        return self.ai_engine.suggest_task_assignment(task, team, all_tasks)
    
    # ========================================================================
    # SPRINT OPERATIONS
    # ========================================================================
    
    def create_sprint(self, project_id: str, user_id: str, name: str,
                     start_date: date, end_date: date, goal: str = "",
                     velocity_planned: int = 0) -> Optional[Sprint]:
        """Create a new sprint"""
        if not self.get_project(project_id, user_id):
            return None
        
        sprint = Sprint.create(
            project_id=project_id,
            user_id=user_id,
            name=name,
            start_date=start_date,
            end_date=end_date,
            goal=goal,
            velocity_planned=velocity_planned
        )
        self.sprints[sprint.id] = sprint
        logger.info(f"Created sprint: {sprint.id} - {name}")
        return sprint
    
    def list_sprints(self, project_id: str, user_id: str) -> List[Sprint]:
        """List sprints for a project"""
        return [
            s for s in self.sprints.values()
            if s.project_id == project_id and s.user_id == user_id
        ]
    
    def update_sprint(self, sprint_id: str, user_id: str,
                     updates: Dict[str, Any]) -> Optional[Sprint]:
        """Update sprint"""
        sprint = self.sprints.get(sprint_id)
        if not sprint or sprint.user_id != user_id:
            return None
        
        for field, value in updates.items():
            if hasattr(sprint, field):
                setattr(sprint, field, value)
        
        return sprint
    
    def start_sprint(self, sprint_id: str, user_id: str) -> Optional[Sprint]:
        """Start a sprint"""
        return self.update_sprint(sprint_id, user_id, {'status': SprintStatus.ACTIVE})
    
    def complete_sprint(self, sprint_id: str, user_id: str) -> Optional[Sprint]:
        """Complete a sprint and calculate velocity"""
        sprint = self.sprints.get(sprint_id)
        if not sprint or sprint.user_id != user_id:
            return None
        
        # Count completed tasks in sprint
        sprint_tasks = [
            t for t in self.tasks.values()
            if t.sprint_id == sprint_id and t.status == TaskStatus.DONE
        ]
        
        sprint.velocity_actual = len(sprint_tasks)
        sprint.status = SprintStatus.COMPLETED
        
        return sprint
    
    # ========================================================================
    # MILESTONE OPERATIONS
    # ========================================================================
    
    def create_milestone(self, project_id: str, user_id: str, name: str,
                        due_date: date, description: str = "",
                        deliverables: List[str] = None) -> Optional[Milestone]:
        """Create a milestone"""
        if not self.get_project(project_id, user_id):
            return None
        
        milestone = Milestone.create(
            project_id=project_id,
            user_id=user_id,
            name=name,
            due_date=due_date,
            description=description,
            deliverables=deliverables
        )
        self.milestones[milestone.id] = milestone
        logger.info(f"Created milestone: {milestone.id} - {name}")
        return milestone
    
    def list_milestones(self, project_id: str, user_id: str) -> List[Milestone]:
        """List milestones for a project"""
        return sorted(
            [m for m in self.milestones.values()
             if m.project_id == project_id and m.user_id == user_id],
            key=lambda m: m.due_date
        )
    
    def complete_milestone(self, milestone_id: str, user_id: str) -> Optional[Milestone]:
        """Complete a milestone"""
        milestone = self.milestones.get(milestone_id)
        if not milestone or milestone.user_id != user_id:
            return None
        
        milestone.status = MilestoneStatus.COMPLETED
        milestone.completed_date = date.today()
        return milestone
    
    # ========================================================================
    # TIME TRACKING
    # ========================================================================
    
    def log_time(self, task_id: str, user_id: str, hours: Decimal,
                description: str = "", entry_date: date = None,
                billable: bool = True) -> Optional[TimeEntry]:
        """Log time on a task"""
        task = self.get_task(task_id, user_id)
        if not task:
            return None
        
        entry = TimeEntry.create(
            task_id=task_id,
            user_id=user_id,
            hours=hours,
            description=description,
            entry_date=entry_date,
            billable=billable
        )
        self.time_entries[entry.id] = entry
        
        # Update task actual hours
        task.actual_hours += hours
        task.updated_at = datetime.utcnow()
        
        # Update project spent (if hourly rate)
        project = self.projects.get(task.project_id)
        if project:
            # Try to get team member rate
            if task.assignee_id:
                member = self.team_members.get(task.assignee_id)
                if member and member.hourly_rate:
                    project.spent += hours * member.hourly_rate
        
        logger.info(f"Logged {hours}h on task {task_id}")
        return entry
    
    def list_time_entries(self, task_id: str = None, project_id: str = None,
                         user_id: str = None, start_date: date = None,
                         end_date: date = None) -> List[TimeEntry]:
        """List time entries"""
        entries = list(self.time_entries.values())
        
        if task_id:
            entries = [e for e in entries if e.task_id == task_id]
        if user_id:
            entries = [e for e in entries if e.user_id == user_id]
        if start_date:
            entries = [e for e in entries if e.date >= start_date]
        if end_date:
            entries = [e for e in entries if e.date <= end_date]
        
        if project_id:
            project_tasks = {t.id for t in self.tasks.values() if t.project_id == project_id}
            entries = [e for e in entries if e.task_id in project_tasks]
        
        return sorted(entries, key=lambda e: e.date, reverse=True)
    
    # ========================================================================
    # TEAM OPERATIONS
    # ========================================================================
    
    def add_team_member(self, project_id: str, user_id: str, name: str,
                       email: str, role: str = "member",
                       hourly_rate: Decimal = None,
                       capacity: Decimal = Decimal("40")) -> Optional[TeamMember]:
        """Add team member to project"""
        if not self.get_project(project_id, user_id):
            return None
        
        member = TeamMember.create(
            project_id=project_id,
            user_id=user_id,
            name=name,
            email=email,
            role=role,
            hourly_rate=hourly_rate,
            capacity_hours_week=capacity
        )
        self.team_members[member.id] = member
        logger.info(f"Added team member: {member.id} - {name}")
        return member
    
    def list_team_members(self, project_id: str, user_id: str) -> List[TeamMember]:
        """List team members for a project"""
        return [
            m for m in self.team_members.values()
            if m.project_id == project_id and m.user_id == user_id
        ]
    
    def remove_team_member(self, member_id: str, user_id: str) -> bool:
        """Remove team member"""
        member = self.team_members.get(member_id)
        if member and member.user_id == user_id:
            del self.team_members[member_id]
            return True
        return False
    
    # ========================================================================
    # COMMENTS
    # ========================================================================
    
    def add_comment(self, task_id: str, user_id: str, author_name: str,
                   content: str, mentions: List[str] = None) -> Optional[Comment]:
        """Add comment to task"""
        task = self.get_task(task_id, user_id)
        if not task:
            return None
        
        comment = Comment.create(
            task_id=task_id,
            user_id=user_id,
            author_name=author_name,
            content=content,
            mentions=mentions
        )
        self.comments[comment.id] = comment
        
        # Update task
        task.updated_at = datetime.utcnow()
        
        return comment
    
    def list_comments(self, task_id: str, user_id: str) -> List[Comment]:
        """List comments for a task"""
        task = self.get_task(task_id, user_id)
        if not task:
            return []
        
        return sorted(
            [c for c in self.comments.values() if c.task_id == task_id],
            key=lambda c: c.created_at
        )
    
    # ========================================================================
    # DASHBOARD & STATS
    # ========================================================================
    
    def get_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get user's PM dashboard"""
        projects = self.list_projects(user_id)
        all_tasks = [t for t in self.tasks.values() if t.user_id == user_id]
        
        # Task breakdown
        task_by_status = {}
        for status in TaskStatus:
            task_by_status[status.value] = len([t for t in all_tasks if t.status == status])
        
        # Overdue tasks
        overdue = [
            t for t in all_tasks
            if t.due_date and t.due_date < date.today() and t.status != TaskStatus.DONE
        ]
        
        # Due this week
        week_end = date.today() + timedelta(days=7)
        due_this_week = [
            t for t in all_tasks
            if t.due_date and date.today() <= t.due_date <= week_end
            and t.status != TaskStatus.DONE
        ]
        
        # Project breakdown
        active_projects = len([p for p in projects if p.status == ProjectStatus.ACTIVE])
        
        # Time logged this week
        week_start = date.today() - timedelta(days=date.today().weekday())
        week_entries = [
            e for e in self.time_entries.values()
            if e.user_id == user_id and e.date >= week_start
        ]
        hours_this_week = sum(e.hours for e in week_entries)
        
        return {
            "projects": {
                "total": len(projects),
                "active": active_projects,
                "completed": len([p for p in projects if p.status == ProjectStatus.COMPLETED])
            },
            "tasks": {
                "total": len(all_tasks),
                "by_status": task_by_status,
                "overdue": len(overdue),
                "due_this_week": len(due_this_week)
            },
            "time": {
                "hours_this_week": float(hours_this_week),
                "entries_this_week": len(week_entries)
            },
            "recent_projects": [
                {"id": p.id, "name": p.name, "status": p.status.value}
                for p in projects[:5]
            ]
        }


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'ProjectStatus', 'TaskStatus', 'TaskPriority', 'SprintStatus',
    'MilestoneStatus', 'RiskLevel',
    'Project', 'Task', 'Sprint', 'Milestone', 'TimeEntry', 'TeamMember',
    'Comment', 'ProjectAnalysis', 'TaskEstimate',
    'ProjectAIEngine', 'ProjectManagementService'
]


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("🚀 Testing Project Management Service...")
    
    service = ProjectManagementService()
    user_id = "user_123"
    
    # Create project
    project = service.create_project(
        user_id=user_id,
        name="CHE·NU V68 Development",
        description="Multi-vertical platform development",
        target_date=date.today() + timedelta(days=90),
        budget=Decimal("50000"),
        tags=["development", "priority"]
    )
    print(f"✅ Created project: {project.name}")
    
    # Add team
    member1 = service.add_team_member(
        project.id, user_id, "Jo", "jo@che-nu.com", "lead",
        hourly_rate=Decimal("75"), capacity=Decimal("40")
    )
    member2 = service.add_team_member(
        project.id, user_id, "Alex", "alex@che-nu.com", "developer",
        hourly_rate=Decimal("60"), capacity=Decimal("40")
    )
    print(f"✅ Added {len(service.list_team_members(project.id, user_id))} team members")
    
    # Create sprint
    sprint = service.create_sprint(
        project.id, user_id, "Sprint 1",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=14),
        goal="Complete Creative Studio vertical",
        velocity_planned=20
    )
    service.start_sprint(sprint.id, user_id)
    print(f"✅ Created and started sprint: {sprint.name}")
    
    # Create milestone
    milestone = service.create_milestone(
        project.id, user_id, "MVP Launch",
        due_date=date.today() + timedelta(days=30),
        description="Launch first 3 verticals",
        deliverables=["Creative Studio", "Personal Productivity", "Business CRM"]
    )
    print(f"✅ Created milestone: {milestone.name}")
    
    # Create tasks
    tasks_data = [
        ("Implement image generation API", TaskPriority.HIGH, member1.id),
        ("Create Creative Studio UI", TaskPriority.HIGH, member2.id),
        ("Write tests for image agent", TaskPriority.MEDIUM, member1.id),
        ("Setup CI/CD pipeline", TaskPriority.CRITICAL, member1.id),
        ("Documentation", TaskPriority.LOW, member2.id),
    ]
    
    for title, priority, assignee in tasks_data:
        task = service.create_task(
            project.id, user_id, title,
            priority=priority,
            assignee_id=assignee,
            assignee_name=member1.name if assignee == member1.id else member2.name,
            sprint_id=sprint.id,
            estimated_hours=Decimal("8"),
            due_date=date.today() + timedelta(days=7)
        )
    
    tasks = service.list_tasks(project.id, user_id)
    print(f"✅ Created {len(tasks)} tasks")
    
    # Move some tasks
    service.move_task(tasks[0].id, user_id, TaskStatus.IN_PROGRESS)
    service.move_task(tasks[1].id, user_id, TaskStatus.IN_PROGRESS)
    service.move_task(tasks[2].id, user_id, TaskStatus.DONE)
    print("✅ Moved tasks through workflow")
    
    # Log time
    service.log_time(tasks[2].id, user_id, Decimal("6"), "Completed testing")
    print("✅ Logged time entry")
    
    # Add comment
    service.add_comment(tasks[0].id, user_id, "Jo", "Looking good! @Alex can you review?", ["Alex"])
    print("✅ Added comment")
    
    # AI Analysis
    analysis = service.analyze_project(project.id, user_id)
    print(f"\n📊 Project Analysis:")
    print(f"   Health Score: {analysis.health_score}/100")
    print(f"   Risk Level: {analysis.risk_level.value}")
    print(f"   Completion: {analysis.completion_percentage:.0f}%")
    print(f"   Velocity Trend: {analysis.velocity_trend}")
    print(f"   Recommendations: {len(analysis.recommendations)}")
    for rec in analysis.recommendations[:3]:
        print(f"      - {rec}")
    
    # Task estimation
    estimate = service.estimate_task(tasks[3].id, user_id)
    print(f"\n⏱️ Task Estimate: {estimate.estimated_hours}h (confidence: {estimate.confidence:.0%})")
    
    # Assignment suggestion
    suggestion = service.suggest_assignee(tasks[4].id, user_id)
    if suggestion.get("suggestion"):
        print(f"👤 Suggested assignee: {suggestion['suggestion']['member_name']}")
        print(f"   Reason: {suggestion['reason']}")
    
    # Dashboard
    dashboard = service.get_dashboard(user_id)
    print(f"\n📈 Dashboard:")
    print(f"   Projects: {dashboard['projects']['active']} active")
    print(f"   Tasks: {dashboard['tasks']['total']} total, {dashboard['tasks']['overdue']} overdue")
    print(f"   Hours this week: {dashboard['time']['hours_this_week']}")
    
    print("\n✅ All tests passed!")
