"""
CHE·NU™ Thread Service

╔══════════════════════════════════════════════════════════════════════════════╗
║                    THREAD SERVICE — THE HEART OF CHE·NU                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  This service implements the APPEND-ONLY event log architecture.             ║
║                                                                              ║
║  CRITICAL RULES:                                                             ║
║  1. Events are IMMUTABLE - never update, never delete                        ║
║  2. Corrections are made by appending NEW events                             ║
║  3. founding_intent is FROZEN forever after creation                         ║
║  4. All state changes produce events                                         ║
║  5. Identity boundary is ABSOLUTE                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from datetime import datetime
from typing import Optional, List, Tuple
from uuid import uuid4
import logging

from sqlalchemy import select, update, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.core.exceptions import (
    NotFoundError,
    ThreadNotFoundError,
    IdentityBoundaryError,
    ThreadImmutabilityError,
    ValidationError,
    CheckpointRequiredError,
)
from backend.models.thread import (
    Thread,
    ThreadEvent,
    ThreadDecision,
    ThreadAction,
    ThreadSnapshot,
    ThreadStatus,
    ThreadType,
    ThreadVisibility,
    ThreadEventType,
    ActionStatus,
    ActionPriority,
)
from backend.models.sphere import Sphere
from backend.schemas.thread_schemas import (
    ThreadCreate,
    ThreadResponse,
    ThreadSummary,
    ThreadUpdate,
    EventCreate,
    EventResponse,
    DecisionCreate,
    DecisionResponse,
    ActionCreate,
    ActionResponse,
    ActionUpdate,
    SnapshotCreate,
    SnapshotResponse,
    IntentRefinement,
)

logger = logging.getLogger(__name__)


class ThreadService:
    """
    Thread Service - Append-Only Event Log Engine.
    
    All operations that modify state MUST create events.
    Events are IMMUTABLE once created.
    """
    
    def __init__(self, db: AsyncSession, identity_id: str, user_id: str):
        self.db = db
        self.identity_id = identity_id
        self.user_id = user_id
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THREAD CREATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_thread(self, request: ThreadCreate) -> ThreadResponse:
        """
        Create a new thread with founding intent.
        
        The founding_intent is IMMUTABLE - it can never be changed.
        Creates the initial thread.created event.
        """
        # Verify sphere exists and belongs to this identity
        sphere = await self._verify_sphere(request.sphere_id)
        
        # Create thread
        thread_id = str(uuid4())
        
        thread = Thread(
            id=thread_id,
            identity_id=self.identity_id,
            sphere_id=request.sphere_id,
            parent_thread_id=request.parent_thread_id,
            founding_intent=request.founding_intent,
            title=request.title,
            current_intent=request.founding_intent,
            thread_type=ThreadType(request.thread_type.value),
            status=ThreadStatus.ACTIVE,
            visibility=ThreadVisibility(request.visibility.value),
            tags=request.tags,
            metadata=request.metadata,
            created_by=self.user_id,
        )
        
        self.db.add(thread)
        await self.db.flush()
        
        # Create the founding event (thread.created)
        event = await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType.THREAD_CREATED,
            payload={
                "founding_intent": request.founding_intent,
                "title": request.title,
                "type": request.thread_type.value,
                "visibility": request.visibility.value,
                "tags": request.tags,
                "parent_thread_id": request.parent_thread_id,
            },
            summary=f"Thread created: {request.title or request.founding_intent[:50]}",
        )
        
        # Also create the intent.declared event
        await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType.INTENT_DECLARED,
            payload={
                "intent": request.founding_intent,
            },
            summary="Founding intent declared",
            parent_event_id=event.id,
        )
        
        # Update sphere thread count
        await self._increment_sphere_thread_count(request.sphere_id)
        
        await self.db.commit()
        
        logger.info(f"Thread created: {thread_id} in sphere {request.sphere_id}")
        
        return ThreadResponse(
            id=thread.id,
            identity_id=thread.identity_id,
            sphere_id=thread.sphere_id,
            parent_thread_id=thread.parent_thread_id,
            title=thread.title,
            founding_intent=thread.founding_intent,
            current_intent=thread.current_intent,
            type=thread.thread_type,
            status=thread.status,
            visibility=thread.visibility,
            tags=thread.tags,
            event_count=thread.event_count,
            decision_count=thread.decision_count,
            action_count=thread.action_count,
            pending_action_count=thread.pending_action_count,
            created_at=thread.created_at,
            created_by=thread.created_by,
            updated_at=thread.updated_at,
            last_event_at=thread.last_event_at,
            metadata=thread.metadata,
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THREAD RETRIEVAL
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_thread(self, thread_id: str) -> ThreadResponse:
        """Get thread by ID with identity boundary check."""
        thread = await self._get_thread_with_check(thread_id)
        
        return ThreadResponse(
            id=thread.id,
            identity_id=thread.identity_id,
            sphere_id=thread.sphere_id,
            parent_thread_id=thread.parent_thread_id,
            title=thread.title,
            founding_intent=thread.founding_intent,
            current_intent=thread.current_intent or thread.founding_intent,
            type=thread.thread_type,
            status=thread.status,
            visibility=thread.visibility,
            tags=thread.tags,
            event_count=thread.event_count,
            decision_count=thread.decision_count,
            action_count=thread.action_count,
            pending_action_count=thread.pending_action_count,
            created_at=thread.created_at,
            created_by=thread.created_by,
            updated_at=thread.updated_at,
            last_event_at=thread.last_event_at,
            metadata=thread.metadata,
        )
    
    async def list_threads(
        self,
        sphere_id: Optional[str] = None,
        status: Optional[ThreadStatus] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[ThreadSummary], int]:
        """
        List threads for current identity with filters.
        
        Returns (threads, total_count).
        """
        # Base query with identity boundary
        query = select(Thread).where(Thread.identity_id == self.identity_id)
        count_query = select(func.count(Thread.id)).where(
            Thread.identity_id == self.identity_id
        )
        
        # Apply filters
        if sphere_id:
            query = query.where(Thread.sphere_id == sphere_id)
            count_query = count_query.where(Thread.sphere_id == sphere_id)
        
        if status:
            query = query.where(Thread.status == status)
            count_query = count_query.where(Thread.status == status)
        
        if search:
            search_filter = or_(
                Thread.title.ilike(f"%{search}%"),
                Thread.founding_intent.ilike(f"%{search}%"),
                Thread.current_intent.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
        
        # Get total count
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        
        # Get threads with pagination
        offset = (page - 1) * page_size
        query = query.order_by(Thread.last_event_at.desc().nullsfirst())
        query = query.offset(offset).limit(page_size)
        
        result = await self.db.execute(query)
        threads = result.scalars().all()
        
        return [
            ThreadSummary(
                id=t.id,
                sphere_id=t.sphere_id,
                title=t.title,
                founding_intent=t.founding_intent,
                current_intent=t.current_intent or t.founding_intent,
                type=t.thread_type,
                status=t.status,
                visibility=t.visibility,
                tags=t.tags,
                event_count=t.event_count,
                decision_count=t.decision_count,
                action_count=t.action_count,
                pending_action_count=t.pending_action_count,
                created_at=t.created_at,
                last_event_at=t.last_event_at,
            )
            for t in threads
        ], total
    
    # ═══════════════════════════════════════════════════════════════════════════
    # THREAD UPDATE (Creates events, never modifies existing data)
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def update_thread(
        self,
        thread_id: str,
        update_data: ThreadUpdate,
    ) -> ThreadResponse:
        """
        Update thread metadata.
        
        NOTE: founding_intent CANNOT be changed!
        Creates a thread.updated event.
        """
        thread = await self._get_thread_with_check(thread_id)
        
        # Build payload for event
        changes = {}
        
        if update_data.title is not None:
            changes["title"] = {"from": thread.title, "to": update_data.title}
            thread.title = update_data.title
        
        if update_data.tags is not None:
            changes["tags"] = {"from": thread.tags, "to": update_data.tags}
            thread.tags = update_data.tags
        
        if update_data.visibility is not None:
            changes["visibility"] = {
                "from": thread.visibility.value,
                "to": update_data.visibility.value,
            }
            thread.visibility = ThreadVisibility(update_data.visibility.value)
        
        if update_data.metadata is not None:
            changes["metadata"] = {"from": thread.metadata, "to": update_data.metadata}
            thread.metadata = update_data.metadata
        
        if changes:
            # Create update event
            await self._append_event(
                thread_id=thread_id,
                event_type=ThreadEventType.THREAD_UPDATED,
                payload={"changes": changes},
                summary=f"Thread updated: {', '.join(changes.keys())}",
            )
        
        await self.db.commit()
        
        return await self.get_thread(thread_id)
    
    async def archive_thread(self, thread_id: str) -> ThreadResponse:
        """
        Archive a thread (soft delete).
        
        Creates thread.archived event.
        """
        thread = await self._get_thread_with_check(thread_id)
        
        if thread.status == ThreadStatus.ARCHIVED:
            raise ValidationError(message="Thread is already archived")
        
        # Update status
        old_status = thread.status
        thread.status = ThreadStatus.ARCHIVED
        thread.archived_at = datetime.utcnow()
        
        # Create archive event
        await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType.THREAD_ARCHIVED,
            payload={
                "previous_status": old_status.value,
                "reason": "User archived",
            },
            summary="Thread archived",
        )
        
        # Update sphere thread count
        await self._decrement_sphere_thread_count(thread.sphere_id)
        
        await self.db.commit()
        
        logger.info(f"Thread archived: {thread_id}")
        
        return await self.get_thread(thread_id)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EVENT OPERATIONS (APPEND-ONLY)
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def append_event(
        self,
        thread_id: str,
        request: EventCreate,
    ) -> EventResponse:
        """
        Append a new event to a thread.
        
        This is the CORE operation. Events are IMMUTABLE.
        May trigger checkpoints for sensitive operations.
        """
        thread = await self._get_thread_with_check(thread_id)
        
        # Check for checkpoint-triggering events
        if self._requires_checkpoint(request.event_type):
            raise CheckpointRequiredError(
                checkpoint_id=str(uuid4()),
                checkpoint_type="governance",
                reason=f"Event type {request.event_type.value} requires approval",
                thread_id=thread_id,
            )
        
        event = await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType(request.event_type.value),
            payload=request.payload,
            summary=request.summary,
            source=request.source,
        )
        
        await self.db.commit()
        
        return EventResponse.model_validate(event)
    
    async def get_events(
        self,
        thread_id: str,
        page: int = 1,
        page_size: int = 50,
        event_types: Optional[List[ThreadEventType]] = None,
    ) -> Tuple[List[EventResponse], int, bool]:
        """
        Get events for a thread in causal order.
        
        Returns (events, total, has_more).
        """
        await self._get_thread_with_check(thread_id)
        
        # Base query
        query = select(ThreadEvent).where(ThreadEvent.thread_id == thread_id)
        count_query = select(func.count(ThreadEvent.id)).where(
            ThreadEvent.thread_id == thread_id
        )
        
        # Filter by event types
        if event_types:
            query = query.where(ThreadEvent.event_type.in_(event_types))
            count_query = count_query.where(ThreadEvent.event_type.in_(event_types))
        
        # Get total
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        
        # Get events with pagination
        offset = (page - 1) * page_size
        query = query.order_by(ThreadEvent.sequence_number)
        query = query.offset(offset).limit(page_size)
        
        result = await self.db.execute(query)
        events = result.scalars().all()
        
        has_more = (offset + page_size) < total
        
        return [
            EventResponse.model_validate(e) for e in events
        ], total, has_more
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTENT REFINEMENT
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def refine_intent(
        self,
        thread_id: str,
        request: IntentRefinement,
    ) -> ThreadResponse:
        """
        Refine thread intent (creates intent.refined event).
        
        NOTE: founding_intent remains unchanged!
        current_intent is updated for display.
        """
        thread = await self._get_thread_with_check(thread_id)
        
        # Update current_intent
        old_intent = thread.current_intent or thread.founding_intent
        thread.current_intent = request.refined_intent
        
        # Create refinement event
        await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType.INTENT_REFINED,
            payload={
                "previous_intent": old_intent,
                "refined_intent": request.refined_intent,
                "reason": request.reason,
            },
            summary=f"Intent refined: {request.refined_intent[:50]}...",
        )
        
        await self.db.commit()
        
        return await self.get_thread(thread_id)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DECISION OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def record_decision(
        self,
        thread_id: str,
        request: DecisionCreate,
    ) -> DecisionResponse:
        """
        Record a decision in the thread.
        
        Creates decision.recorded event and ThreadDecision record.
        """
        thread = await self._get_thread_with_check(thread_id)
        
        decision_id = str(uuid4())
        
        # Create decision event
        event = await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType.DECISION_RECORDED,
            payload={
                "decision_id": decision_id,
                "title": request.title,
                "description": request.description,
                "rationale": request.rationale,
                "options_considered": request.options_considered,
                "chosen_option": request.chosen_option,
            },
            summary=f"Decision: {request.title}",
        )
        
        # Create decision record
        decision = ThreadDecision(
            id=decision_id,
            thread_id=thread_id,
            event_id=event.id,
            title=request.title,
            description=request.description,
            rationale=request.rationale,
            options_considered=request.options_considered,
            chosen_option=request.chosen_option,
            tags=request.tags,
            created_by=self.user_id,
        )
        
        self.db.add(decision)
        
        # Update thread counter
        thread.decision_count += 1
        
        await self.db.commit()
        
        logger.info(f"Decision recorded: {decision_id} in thread {thread_id}")
        
        return DecisionResponse.model_validate(decision)
    
    async def get_decisions(
        self,
        thread_id: str,
    ) -> List[DecisionResponse]:
        """Get all decisions for a thread."""
        await self._get_thread_with_check(thread_id)
        
        result = await self.db.execute(
            select(ThreadDecision)
            .where(ThreadDecision.thread_id == thread_id)
            .order_by(ThreadDecision.created_at.desc())
        )
        
        decisions = result.scalars().all()
        
        return [DecisionResponse.model_validate(d) for d in decisions]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ACTION OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_action(
        self,
        thread_id: str,
        request: ActionCreate,
    ) -> ActionResponse:
        """
        Create an action item in the thread.
        
        Creates action.created event and ThreadAction record.
        """
        thread = await self._get_thread_with_check(thread_id)
        
        action_id = str(uuid4())
        
        # Create action event
        event = await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType.ACTION_CREATED,
            payload={
                "action_id": action_id,
                "title": request.title,
                "description": request.description,
                "priority": request.priority.value,
                "due_date": request.due_date.isoformat() if request.due_date else None,
                "assignee_id": request.assignee_id,
            },
            summary=f"Action: {request.title}",
        )
        
        # Create action record
        action = ThreadAction(
            id=action_id,
            thread_id=thread_id,
            event_id=event.id,
            title=request.title,
            description=request.description,
            status=ActionStatus.PENDING,
            priority=ActionPriority(request.priority.value),
            due_date=request.due_date,
            assignee_id=request.assignee_id,
            tags=request.tags,
            metadata=request.metadata,
            created_by=self.user_id,
        )
        
        self.db.add(action)
        
        # Update thread counters
        thread.action_count += 1
        thread.pending_action_count += 1
        
        await self.db.commit()
        
        logger.info(f"Action created: {action_id} in thread {thread_id}")
        
        return ActionResponse.model_validate(action)
    
    async def complete_action(self, thread_id: str, action_id: str) -> ActionResponse:
        """
        Complete an action.
        
        Creates action.completed event.
        """
        thread = await self._get_thread_with_check(thread_id)
        action = await self._get_action(thread_id, action_id)
        
        if action.status == ActionStatus.COMPLETED:
            raise ValidationError(message="Action is already completed")
        
        # Update action
        old_status = action.status
        action.status = ActionStatus.COMPLETED
        action.completed_at = datetime.utcnow()
        
        # Create completion event
        await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType.ACTION_COMPLETED,
            payload={
                "action_id": action_id,
                "title": action.title,
                "previous_status": old_status.value,
            },
            summary=f"Action completed: {action.title}",
        )
        
        # Update thread counter
        if old_status == ActionStatus.PENDING:
            thread.pending_action_count = max(0, thread.pending_action_count - 1)
        
        await self.db.commit()
        
        return ActionResponse.model_validate(action)
    
    async def get_actions(
        self,
        thread_id: str,
        status: Optional[ActionStatus] = None,
    ) -> Tuple[List[ActionResponse], int]:
        """Get actions for a thread with optional status filter."""
        await self._get_thread_with_check(thread_id)
        
        query = select(ThreadAction).where(ThreadAction.thread_id == thread_id)
        
        if status:
            query = query.where(ThreadAction.status == status)
        
        query = query.order_by(ThreadAction.created_at.desc())
        
        result = await self.db.execute(query)
        actions = result.scalars().all()
        
        pending_count = sum(
            1 for a in actions if a.status == ActionStatus.PENDING
        )
        
        return [ActionResponse.model_validate(a) for a in actions], pending_count
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SNAPSHOT OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_snapshot(self, thread_id: str) -> SnapshotResponse:
        """
        Get current thread snapshot (derived from events).
        
        Returns the latest state computed from the event log.
        """
        thread = await self._get_thread_with_check(thread_id)
        
        # Get latest snapshot or compute from events
        result = await self.db.execute(
            select(ThreadSnapshot)
            .where(ThreadSnapshot.thread_id == thread_id)
            .order_by(ThreadSnapshot.sequence_number.desc())
            .limit(1)
        )
        
        snapshot = result.scalar_one_or_none()
        
        if snapshot:
            return SnapshotResponse.model_validate(snapshot)
        
        # Compute snapshot from current state
        decisions = await self.get_decisions(thread_id)
        actions, _ = await self.get_actions(thread_id)
        
        return SnapshotResponse(
            id="computed",
            thread_id=thread_id,
            event_id="",
            sequence_number=thread.event_count,
            snapshot_type="computed",
            summary=None,
            key_decisions=[d.title for d in decisions[:5]],
            active_actions=[a.title for a in actions if a.status == ActionStatus.PENDING][:5],
            state={
                "title": thread.title,
                "current_intent": thread.current_intent or thread.founding_intent,
                "status": thread.status.value,
                "event_count": thread.event_count,
                "decision_count": thread.decision_count,
                "action_count": thread.action_count,
            },
            created_at=datetime.utcnow(),
            created_by=self.user_id,
        )
    
    async def create_snapshot(
        self,
        thread_id: str,
        request: SnapshotCreate,
    ) -> SnapshotResponse:
        """
        Create a manual snapshot for memory compression.
        
        Creates summary.snapshot event.
        """
        thread = await self._get_thread_with_check(thread_id)
        
        snapshot_id = str(uuid4())
        
        # Get current state
        decisions = await self.get_decisions(thread_id)
        actions, _ = await self.get_actions(thread_id)
        
        state = {
            "title": thread.title,
            "current_intent": thread.current_intent or thread.founding_intent,
            "status": thread.status.value,
            "event_count": thread.event_count,
            "decision_count": thread.decision_count,
            "action_count": thread.action_count,
            "pending_action_count": thread.pending_action_count,
        }
        
        # Create snapshot event
        event = await self._append_event(
            thread_id=thread_id,
            event_type=ThreadEventType.SUMMARY_SNAPSHOT,
            payload={
                "snapshot_id": snapshot_id,
                "summary": request.summary,
                "state": state,
            },
            summary=request.summary or "Snapshot created",
        )
        
        # Create snapshot record
        snapshot = ThreadSnapshot(
            id=snapshot_id,
            thread_id=thread_id,
            event_id=event.id,
            sequence_number=thread.event_count,
            snapshot_type=request.snapshot_type,
            state=state,
            summary=request.summary,
            key_decisions=[d.title for d in decisions[:10]],
            active_actions=[a.title for a in actions if a.status == ActionStatus.PENDING][:10],
            created_by=self.user_id,
        )
        
        self.db.add(snapshot)
        await self.db.commit()
        
        logger.info(f"Snapshot created: {snapshot_id} for thread {thread_id}")
        
        return SnapshotResponse.model_validate(snapshot)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PRIVATE HELPERS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def _get_thread_with_check(self, thread_id: str) -> Thread:
        """Get thread and verify identity boundary."""
        result = await self.db.execute(
            select(Thread).where(Thread.id == thread_id)
        )
        
        thread = result.scalar_one_or_none()
        
        if not thread:
            raise ThreadNotFoundError(thread_id=thread_id)
        
        if thread.identity_id != self.identity_id:
            raise IdentityBoundaryError(
                requested_identity=self.identity_id,
                resource_identity=thread.identity_id,
                resource_type="Thread",
            )
        
        return thread
    
    async def _verify_sphere(self, sphere_id: str) -> Sphere:
        """Verify sphere exists and belongs to identity."""
        result = await self.db.execute(
            select(Sphere).where(Sphere.id == sphere_id)
        )
        
        sphere = result.scalar_one_or_none()
        
        if not sphere:
            raise NotFoundError(message=f"Sphere not found: {sphere_id}")
        
        if sphere.identity_id != self.identity_id:
            raise IdentityBoundaryError(
                requested_identity=self.identity_id,
                resource_identity=sphere.identity_id,
                resource_type="Sphere",
            )
        
        return sphere
    
    async def _get_action(self, thread_id: str, action_id: str) -> ThreadAction:
        """Get action by ID."""
        result = await self.db.execute(
            select(ThreadAction)
            .where(
                and_(
                    ThreadAction.id == action_id,
                    ThreadAction.thread_id == thread_id,
                )
            )
        )
        
        action = result.scalar_one_or_none()
        
        if not action:
            raise NotFoundError(message=f"Action not found: {action_id}")
        
        return action
    
    async def _append_event(
        self,
        thread_id: str,
        event_type: ThreadEventType,
        payload: dict,
        summary: Optional[str] = None,
        source: str = "user",
        parent_event_id: Optional[str] = None,
        agent_id: Optional[str] = None,
    ) -> ThreadEvent:
        """
        CORE: Append an immutable event to a thread.
        
        This is THE critical operation - events are NEVER modified.
        """
        # Get next sequence number
        result = await self.db.execute(
            select(func.coalesce(func.max(ThreadEvent.sequence_number), 0))
            .where(ThreadEvent.thread_id == thread_id)
        )
        current_max = result.scalar() or 0
        next_sequence = current_max + 1
        
        # If no parent specified, use the previous event
        if parent_event_id is None and current_max > 0:
            prev_result = await self.db.execute(
                select(ThreadEvent.id)
                .where(
                    and_(
                        ThreadEvent.thread_id == thread_id,
                        ThreadEvent.sequence_number == current_max,
                    )
                )
            )
            parent_event_id = prev_result.scalar()
        
        # Create event
        event = ThreadEvent(
            id=str(uuid4()),
            thread_id=thread_id,
            sequence_number=next_sequence,
            parent_event_id=parent_event_id,
            event_type=event_type,
            payload=payload,
            summary=summary,
            source=source,
            agent_id=agent_id,
            created_by=self.user_id,
        )
        
        self.db.add(event)
        
        # Update thread counters
        await self.db.execute(
            update(Thread)
            .where(Thread.id == thread_id)
            .values(
                event_count=Thread.event_count + 1,
                last_event_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
        )
        
        return event
    
    def _requires_checkpoint(self, event_type: ThreadEventType) -> bool:
        """Check if event type requires governance checkpoint."""
        sensitive_events = {
            ThreadEventType.THREAD_ARCHIVED,
            ThreadEventType.CHECKPOINT_TRIGGERED,
        }
        return event_type in sensitive_events
    
    async def _increment_sphere_thread_count(self, sphere_id: str) -> None:
        """Increment sphere thread count."""
        await self.db.execute(
            update(Sphere)
            .where(Sphere.id == sphere_id)
            .values(
                thread_count=Sphere.thread_count + 1,
                last_activity_at=datetime.utcnow(),
            )
        )
    
    async def _decrement_sphere_thread_count(self, sphere_id: str) -> None:
        """Decrement sphere thread count."""
        await self.db.execute(
            update(Sphere)
            .where(Sphere.id == sphere_id)
            .values(
                thread_count=func.greatest(Sphere.thread_count - 1, 0),
            )
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE FACTORY
# ═══════════════════════════════════════════════════════════════════════════════

def get_thread_service(
    db: AsyncSession,
    identity_id: str,
    user_id: str,
) -> ThreadService:
    """Factory function for ThreadService."""
    return ThreadService(db, identity_id, user_id)
