"""
SERVICE: decision_point_service.py
SPHERE: CORE (cross-sphere)
VERSION: 1.0.0
INTENT: Decision Point system for pending actions with AI suggestions and aging alerts

DEPENDENCIES:
- Core: governance_schemas
- External: anthropic (for AI suggestions)

R&D COMPLIANCE: ✅
- Rule #1: Human Sovereignty - Nova SUGGESTS, human DECIDES
- Rule #6: Traceability - All decision points tracked with created_by, responded_by

HUMAN GATES:
- All decision points require explicit human response
- No auto-execution of suggestions

AGING SYSTEM:
- GREEN:   0-24 hours
- YELLOW:  24h - 3 days
- RED:     3-7 days
- BLINK:   7-10 days (critical)
- ARCHIVE: >10 days (auto-archive)
"""

import logging
from typing import Optional, List, Dict, Any
from uuid import uuid4
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

from ..schemas.governance_schemas import (
    DecisionPoint,
    DecisionPointCreate,
    DecisionPointType,
    AgingLevel,
    AISuggestion,
    UserResponse,
    UserResponseType,
    compute_aging_level,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION POINT REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════

class DecisionPointRepository:
    """
    Repository for decision points.
    
    In production, backed by PostgreSQL table: decision_points
    """
    
    def __init__(self):
        self.points: Dict[str, DecisionPoint] = {}
        self.by_thread: Dict[str, List[str]] = defaultdict(list)
        self.by_user: Dict[str, List[str]] = defaultdict(list)
    
    async def create(self, point: DecisionPoint) -> DecisionPoint:
        """Create a new decision point."""
        self.points[point.id] = point
        self.by_thread[point.thread_id].append(point.id)
        self.by_user[point.created_by].append(point.id)
        
        logger.info(
            f"Created decision point: {point.id} "
            f"(type={point.point_type.value}, thread={point.thread_id})"
        )
        return point
    
    async def get(self, point_id: str) -> Optional[DecisionPoint]:
        """Get a decision point by ID."""
        return self.points.get(point_id)
    
    async def list_active(
        self,
        thread_id: Optional[str] = None,
        user_id: Optional[str] = None,
        point_type: Optional[DecisionPointType] = None,
        aging_level: Optional[AgingLevel] = None,
        limit: int = 100
    ) -> List[DecisionPoint]:
        """List active (non-archived) decision points with optional filters."""
        points = [p for p in self.points.values() if p.is_active and not p.is_archived]
        
        if thread_id:
            points = [p for p in points if p.thread_id == thread_id]
        if user_id:
            points = [p for p in points if p.created_by == user_id]
        if point_type:
            points = [p for p in points if p.point_type == point_type]
        if aging_level:
            points = [p for p in points if p.aging_level == aging_level]
        
        # Sort by urgency (most urgent first)
        aging_order = {
            AgingLevel.BLINK: 0,
            AgingLevel.RED: 1,
            AgingLevel.YELLOW: 2,
            AgingLevel.GREEN: 3,
            AgingLevel.ARCHIVE: 4,
        }
        points.sort(key=lambda p: aging_order.get(p.aging_level, 5))
        
        return points[:limit]
    
    async def list_archived(
        self,
        thread_id: Optional[str] = None,
        limit: int = 50
    ) -> List[DecisionPoint]:
        """List archived decision points."""
        points = [p for p in self.points.values() if p.is_archived]
        
        if thread_id:
            points = [p for p in points if p.thread_id == thread_id]
        
        points.sort(key=lambda p: p.archived_at or p.created_at, reverse=True)
        return points[:limit]
    
    async def update(self, point: DecisionPoint) -> DecisionPoint:
        """Update a decision point."""
        self.points[point.id] = point
        logger.info(f"Updated decision point: {point.id}")
        return point
    
    async def count_by_aging(self, user_id: Optional[str] = None) -> Dict[AgingLevel, int]:
        """Count active points by aging level."""
        points = [p for p in self.points.values() if p.is_active and not p.is_archived]
        
        if user_id:
            points = [p for p in points if p.created_by == user_id]
        
        counts = {level: 0 for level in AgingLevel}
        for p in points:
            counts[p.aging_level] += 1
        
        return counts


# ═══════════════════════════════════════════════════════════════════════════════
# AI SUGGESTION GENERATOR (Nova)
# ═══════════════════════════════════════════════════════════════════════════════

class SuggestionGenerator:
    """
    Generates AI suggestions for decision points.
    
    Uses Nova intelligence to analyze context and suggest next steps.
    
    R&D Rule #1: These are SUGGESTIONS only. Human decides.
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.suggestion_templates = self._load_templates()
    
    def _load_templates(self) -> Dict[DecisionPointType, str]:
        """Load suggestion templates by type."""
        return {
            DecisionPointType.CONFIRMATION: (
                "Based on the context: {context}\n"
                "Suggest the most appropriate action for confirming: {title}"
            ),
            DecisionPointType.TASK: (
                "For the task: {title}\n"
                "Context: {context}\n"
                "Suggest the best approach to complete this task."
            ),
            DecisionPointType.DECISION: (
                "Decision required: {title}\n"
                "Context: {context}\n"
                "Analyze options and suggest the best decision with rationale."
            ),
            DecisionPointType.CHECKPOINT: (
                "Governance checkpoint triggered: {title}\n"
                "Context: {context}\n"
                "Explain what needs approval and suggest recommended action."
            ),
            DecisionPointType.APPROVAL: (
                "Approval requested for: {title}\n"
                "Context: {context}\n"
                "Summarize what needs approval and recommend approve/reject."
            ),
            DecisionPointType.REVIEW: (
                "Review needed for: {title}\n"
                "Context: {context}\n"
                "Highlight key points to review and suggest improvements."
            ),
        }
    
    async def generate_suggestion(
        self,
        point_type: DecisionPointType,
        title: str,
        description: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> AISuggestion:
        """
        Generate an AI suggestion for a decision point.
        
        Falls back to template-based suggestions if LLM unavailable.
        """
        # For now, use rule-based suggestions
        # In production, would call LLM
        
        suggestion = await self._generate_rule_based(
            point_type, title, description, context
        )
        
        return suggestion
    
    async def _generate_rule_based(
        self,
        point_type: DecisionPointType,
        title: str,
        description: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> AISuggestion:
        """Generate rule-based suggestion when LLM unavailable."""
        
        # Default suggestions by type
        suggestions_by_type = {
            DecisionPointType.CONFIRMATION: {
                "summary": f"Confirmer: {title[:50]}",
                "suggested_action": "confirm",
                "alternatives": ["modifier", "annuler", "reporter"],
                "confidence": 0.75,
                "rationale": "Action standard de confirmation",
            },
            DecisionPointType.TASK: {
                "summary": f"Compléter la tâche: {title[:50]}",
                "suggested_action": "complete_task",
                "alternatives": ["déléguer", "décomposer", "reporter"],
                "confidence": 0.70,
                "rationale": "Tâche identifiée dans le flux",
            },
            DecisionPointType.DECISION: {
                "summary": f"Décider: {title[:50]}",
                "suggested_action": "decide",
                "alternatives": ["demander plus d'info", "consulter", "reporter"],
                "confidence": 0.65,
                "rationale": "Décision requise pour continuer",
            },
            DecisionPointType.CHECKPOINT: {
                "summary": f"Approuver le checkpoint: {title[:50]}",
                "suggested_action": "approve",
                "alternatives": ["rejeter", "demander révision"],
                "confidence": 0.80,
                "rationale": "Checkpoint de gouvernance déclenché",
            },
            DecisionPointType.APPROVAL: {
                "summary": f"Approuver: {title[:50]}",
                "suggested_action": "approve",
                "alternatives": ["rejeter", "demander modifications"],
                "confidence": 0.70,
                "rationale": "Approbation requise",
            },
            DecisionPointType.REVIEW: {
                "summary": f"Réviser: {title[:50]}",
                "suggested_action": "approve_with_comments",
                "alternatives": ["approuver", "rejeter", "demander révision"],
                "confidence": 0.65,
                "rationale": "Révision recommandée",
            },
        }
        
        defaults = suggestions_by_type.get(point_type, {
            "summary": title[:100],
            "suggested_action": "review",
            "alternatives": ["approuver", "rejeter"],
            "confidence": 0.50,
            "rationale": "Analyse standard",
        })
        
        # Enhance with context if available
        context_used = []
        if context:
            if "recent_actions" in context:
                context_used.append("recent_actions")
            if "user_preferences" in context:
                context_used.append("user_preferences")
            if "thread_history" in context:
                context_used.append("thread_history")
        
        return AISuggestion(
            summary=defaults["summary"],
            detailed_explanation=description or f"Suggestion pour: {title}",
            confidence=defaults["confidence"],
            suggested_action=defaults["suggested_action"],
            alternatives=defaults["alternatives"],
            rationale=defaults["rationale"],
            context_used=context_used,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# AGING MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class AgingManager:
    """
    Manages aging levels and auto-archiving of decision points.
    """
    
    def __init__(self, repository: DecisionPointRepository):
        self.repository = repository
    
    async def update_aging_levels(self) -> Dict[str, AgingLevel]:
        """
        Update aging levels for all active decision points.
        
        Returns dict of point_id -> new_aging_level for changed points.
        """
        changes = {}
        
        for point_id, point in self.repository.points.items():
            if not point.is_active or point.is_archived:
                continue
            
            new_level = compute_aging_level(point.created_at)
            
            if new_level != point.aging_level:
                old_level = point.aging_level
                point.aging_level = new_level
                
                # Auto-archive if past threshold
                if new_level == AgingLevel.ARCHIVE:
                    point.is_archived = True
                    point.archived_at = datetime.utcnow()
                    point.archive_reason = "timeout"
                    logger.info(f"Auto-archived decision point {point_id} (timeout)")
                
                changes[point_id] = new_level
                logger.debug(
                    f"Aging level changed for {point_id}: "
                    f"{old_level.value} -> {new_level.value}"
                )
        
        return changes
    
    async def get_due_reminders(
        self,
        min_aging: AgingLevel = AgingLevel.YELLOW
    ) -> List[DecisionPoint]:
        """
        Get decision points that should trigger reminders.
        
        Args:
            min_aging: Minimum aging level to trigger reminder
        """
        aging_order = {
            AgingLevel.GREEN: 0,
            AgingLevel.YELLOW: 1,
            AgingLevel.RED: 2,
            AgingLevel.BLINK: 3,
            AgingLevel.ARCHIVE: 4,
        }
        min_order = aging_order[min_aging]
        
        due = []
        for point in self.repository.points.values():
            if not point.is_active or point.is_archived:
                continue
            
            if aging_order[point.aging_level] >= min_order:
                # Check if reminder needed (not reminded in last 6 hours for yellow, 2h for red, 30min for blink)
                reminder_intervals = {
                    AgingLevel.YELLOW: timedelta(hours=6),
                    AgingLevel.RED: timedelta(hours=2),
                    AgingLevel.BLINK: timedelta(minutes=30),
                }
                
                interval = reminder_intervals.get(point.aging_level)
                if interval:
                    if point.last_reminded_at is None or \
                       datetime.utcnow() - point.last_reminded_at > interval:
                        due.append(point)
        
        return due


# ═══════════════════════════════════════════════════════════════════════════════
# DECISION POINT SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class DecisionPointService:
    """
    Main service for decision point management.
    
    Features:
    - Create decision points with AI suggestions
    - Track aging (green → yellow → red → blink → archive)
    - Process user responses (validate, redirect, comment)
    - Auto-archive old items
    - Send reminders for urgent items
    
    R&D Compliance:
    - Rule #1: Human Sovereignty - Nova suggests, human decides
    - Rule #6: Full traceability
    """
    
    def __init__(self, llm_client=None):
        self.repository = DecisionPointRepository()
        self.suggestion_generator = SuggestionGenerator(llm_client)
        self.aging_manager = AgingManager(self.repository)
        
        logger.info("DecisionPointService initialized")
    
    async def create_decision_point(
        self,
        create_data: DecisionPointCreate,
        created_by: str,
        generate_suggestion: bool = True
    ) -> DecisionPoint:
        """
        Create a new decision point.
        
        Args:
            create_data: Data for creating the point
            created_by: User ID creating the point
            generate_suggestion: Whether to auto-generate AI suggestion
        
        Returns:
            Created DecisionPoint
        """
        # Generate AI suggestion if requested
        suggestion = create_data.suggestion
        if generate_suggestion and not suggestion:
            suggestion = await self.suggestion_generator.generate_suggestion(
                point_type=create_data.point_type,
                title=create_data.title,
                description=create_data.description,
                context=create_data.context,
            )
        
        # Create decision point
        point = DecisionPoint(
            id=str(uuid4()),
            point_type=create_data.point_type,
            thread_id=create_data.thread_id,
            title=create_data.title,
            description=create_data.description,
            context=create_data.context,
            suggestion=suggestion,
            aging_level=create_data.urgency_override or AgingLevel.GREEN,
            source_event_id=create_data.source_event_id,
            source_module=create_data.source_module,
            created_by=created_by,
        )
        
        await self.repository.create(point)
        
        return point
    
    async def respond_to_point(
        self,
        point_id: str,
        response_type: UserResponseType,
        user_id: str,
        comment: Optional[str] = None,
        selected_alternative: Optional[str] = None,
        custom_action: Optional[str] = None
    ) -> Optional[DecisionPoint]:
        """
        Record user's response to a decision point.
        
        Args:
            point_id: Decision point ID
            response_type: Type of response
            user_id: User responding
            comment: Optional comment
            selected_alternative: If redirect, which alternative
            custom_action: If fully custom response
        
        Returns:
            Updated DecisionPoint or None if not found
        """
        point = await self.repository.get(point_id)
        if not point:
            return None
        
        # Record response
        point.user_response = UserResponse(
            response_type=response_type,
            comment=comment,
            selected_alternative=selected_alternative,
            custom_action=custom_action,
            responded_by=user_id,
        )
        
        # Mark as inactive (responded)
        point.is_active = False
        
        await self.repository.update(point)
        
        logger.info(
            f"User {user_id} responded to decision point {point_id}: "
            f"{response_type.value}"
        )
        
        return point
    
    async def validate_suggestion(
        self,
        point_id: str,
        user_id: str
    ) -> Optional[DecisionPoint]:
        """Shortcut to validate (accept) the AI suggestion."""
        return await self.respond_to_point(
            point_id=point_id,
            response_type=UserResponseType.VALIDATE,
            user_id=user_id,
        )
    
    async def redirect_decision(
        self,
        point_id: str,
        alternative: str,
        user_id: str,
        comment: Optional[str] = None
    ) -> Optional[DecisionPoint]:
        """Shortcut to redirect to an alternative."""
        return await self.respond_to_point(
            point_id=point_id,
            response_type=UserResponseType.REDIRECT,
            user_id=user_id,
            selected_alternative=alternative,
            comment=comment,
        )
    
    async def add_comment(
        self,
        point_id: str,
        comment: str,
        user_id: str
    ) -> Optional[DecisionPoint]:
        """Add a comment without closing the decision point."""
        point = await self.repository.get(point_id)
        if not point:
            return None
        
        # Record as comment response (doesn't close)
        point.user_response = UserResponse(
            response_type=UserResponseType.COMMENT,
            comment=comment,
            responded_by=user_id,
        )
        # Note: is_active stays True for comments
        
        await self.repository.update(point)
        return point
    
    async def defer_point(
        self,
        point_id: str,
        user_id: str
    ) -> Optional[DecisionPoint]:
        """Defer a decision point (reset aging to green)."""
        point = await self.repository.get(point_id)
        if not point:
            return None
        
        # Reset aging
        point.aging_level = AgingLevel.GREEN
        point.created_at = datetime.utcnow()  # Reset timer
        point.last_reminded_at = None
        point.reminder_count = 0
        
        # Record defer response
        point.user_response = UserResponse(
            response_type=UserResponseType.DEFER,
            responded_by=user_id,
        )
        
        await self.repository.update(point)
        
        logger.info(f"Deferred decision point {point_id}")
        
        return point
    
    async def archive_point(
        self,
        point_id: str,
        user_id: str,
        reason: str = "manual"
    ) -> Optional[DecisionPoint]:
        """Manually archive a decision point."""
        point = await self.repository.get(point_id)
        if not point:
            return None
        
        point.is_archived = True
        point.is_active = False
        point.archived_at = datetime.utcnow()
        point.archive_reason = reason
        
        await self.repository.update(point)
        
        logger.info(f"Archived decision point {point_id}: {reason}")
        
        return point
    
    async def get_active_points(
        self,
        thread_id: Optional[str] = None,
        user_id: Optional[str] = None,
        point_type: Optional[DecisionPointType] = None,
        aging_level: Optional[AgingLevel] = None,
        limit: int = 100
    ) -> List[DecisionPoint]:
        """Get active decision points with filtering."""
        return await self.repository.list_active(
            thread_id=thread_id,
            user_id=user_id,
            point_type=point_type,
            aging_level=aging_level,
            limit=limit,
        )
    
    async def get_urgent_points(
        self,
        user_id: Optional[str] = None
    ) -> List[DecisionPoint]:
        """Get urgent points (red + blink)."""
        points = await self.repository.list_active(user_id=user_id)
        return [
            p for p in points
            if p.aging_level in [AgingLevel.RED, AgingLevel.BLINK]
        ]
    
    async def get_aging_summary(
        self,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get summary of aging levels."""
        counts = await self.repository.count_by_aging(user_id)
        
        total_active = sum(counts.values()) - counts.get(AgingLevel.ARCHIVE, 0)
        urgent = counts.get(AgingLevel.RED, 0) + counts.get(AgingLevel.BLINK, 0)
        
        return {
            "counts": {level.value: count for level, count in counts.items()},
            "total_active": total_active,
            "urgent_count": urgent,
            "has_urgent": urgent > 0,
            "has_critical": counts.get(AgingLevel.BLINK, 0) > 0,
        }
    
    async def process_aging(self) -> Dict[str, Any]:
        """
        Process aging for all points.
        
        Should be called periodically (e.g., every minute).
        
        Returns:
            Summary of changes
        """
        changes = await self.aging_manager.update_aging_levels()
        reminders = await self.aging_manager.get_due_reminders()
        
        # Update reminder counts
        for point in reminders:
            point.last_reminded_at = datetime.utcnow()
            point.reminder_count += 1
            await self.repository.update(point)
        
        return {
            "aging_changes": len(changes),
            "reminders_sent": len(reminders),
            "changed_points": list(changes.keys()),
            "reminder_points": [p.id for p in reminders],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "DecisionPointRepository",
    "SuggestionGenerator",
    "AgingManager",
    "DecisionPointService",
]
