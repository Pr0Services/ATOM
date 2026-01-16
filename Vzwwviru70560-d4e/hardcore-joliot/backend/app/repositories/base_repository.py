"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V80 — Repository Pattern
═══════════════════════════════════════════════════════════════════════════════

Repository pattern for database operations.

Key Features:
- Identity boundary enforcement (R&D Rule #3)
- Automatic audit logging (R&D Rule #6)
- Chronological ordering (R&D Rule #5)
- Transaction support
"""

from datetime import datetime
from typing import TypeVar, Generic, Optional, List, Dict, Any, Type
from uuid import UUID, uuid4
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import (
    Base, Identity, Thread, ThreadEvent, Checkpoint, AuditLog,
    SphereType, ThreadStatus, CheckpointStatus, AuditLogAction
)

# Generic type for models
T = TypeVar("T", bound=Base)


# ═══════════════════════════════════════════════════════════════════════════════
# BASE REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════

class BaseRepository(Generic[T]):
    """
    Base repository with identity boundary enforcement.
    
    R&D Rule #3: All queries are scoped to identity.
    R&D Rule #6: All mutations are logged.
    """
    
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
    
    async def get_by_id(
        self,
        id: UUID,
        identity_id: UUID
    ) -> Optional[T]:
        """
        Get entity by ID with identity check.
        
        R&D Rule #3: Returns None if identity doesn't match.
        """
        stmt = select(self.model).where(
            and_(
                self.model.id == id,
                self.model.created_by == identity_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list_all(
        self,
        identity_id: UUID,
        limit: int = 100,
        offset: int = 0,
        order_by_created: bool = True
    ) -> List[T]:
        """
        List all entities for an identity.
        
        R&D Rule #3: Only returns identity's data.
        R&D Rule #5: Ordered by created_at DESC (chronological).
        """
        stmt = select(self.model).where(
            self.model.created_by == identity_id
        )
        
        if order_by_created:
            stmt = stmt.order_by(self.model.created_at.desc())
        
        stmt = stmt.limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def count(self, identity_id: UUID) -> int:
        """Count entities for an identity."""
        stmt = select(func.count()).select_from(self.model).where(
            self.model.created_by == identity_id
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0
    
    async def create(
        self,
        identity_id: UUID,
        data: Dict[str, Any],
        audit_action: Optional[AuditLogAction] = AuditLogAction.CREATE
    ) -> T:
        """
        Create entity with traceability.
        
        R&D Rule #6: Logs creation to audit trail.
        """
        entity = self.model(
            id=uuid4(),
            created_by=identity_id,
            **data
        )
        
        self.session.add(entity)
        await self.session.flush()
        
        # Audit log
        if audit_action:
            await self._log_audit(
                identity_id=identity_id,
                action=audit_action,
                resource_type=self.model.__tablename__,
                resource_id=entity.id,
                details={"created": data}
            )
        
        return entity
    
    async def update(
        self,
        id: UUID,
        identity_id: UUID,
        data: Dict[str, Any]
    ) -> Optional[T]:
        """
        Update entity with identity check.
        
        R&D Rule #3: Only updates if identity matches.
        R&D Rule #6: Logs update to audit trail.
        """
        entity = await self.get_by_id(id, identity_id)
        if not entity:
            return None
        
        for key, value in data.items():
            if hasattr(entity, key):
                setattr(entity, key, value)
        
        await self.session.flush()
        
        # Audit log
        await self._log_audit(
            identity_id=identity_id,
            action=AuditLogAction.UPDATE,
            resource_type=self.model.__tablename__,
            resource_id=id,
            details={"updated": data}
        )
        
        return entity
    
    async def delete(
        self,
        id: UUID,
        identity_id: UUID
    ) -> bool:
        """
        Delete entity with identity check.
        
        R&D Rule #3: Only deletes if identity matches.
        R&D Rule #6: Logs deletion to audit trail.
        """
        entity = await self.get_by_id(id, identity_id)
        if not entity:
            return False
        
        await self.session.delete(entity)
        await self.session.flush()
        
        # Audit log
        await self._log_audit(
            identity_id=identity_id,
            action=AuditLogAction.DELETE,
            resource_type=self.model.__tablename__,
            resource_id=id,
            details={}
        )
        
        return True
    
    async def _log_audit(
        self,
        identity_id: UUID,
        action: AuditLogAction,
        resource_type: str,
        resource_id: UUID,
        details: Dict[str, Any],
        sphere: Optional[SphereType] = None
    ) -> None:
        """Log to audit trail (R&D Rule #6)."""
        audit = AuditLog(
            id=uuid4(),
            identity_id=identity_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            sphere=sphere,
            details=details
        )
        self.session.add(audit)


# ═══════════════════════════════════════════════════════════════════════════════
# IDENTITY REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════════

class IdentityRepository:
    """Repository for identity management."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, id: UUID) -> Optional[Identity]:
        """Get identity by ID."""
        stmt = select(Identity).where(Identity.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[Identity]:
        """Get identity by email."""
        stmt = select(Identity).where(Identity.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(
        self,
        email: str,
        name: str,
        hashed_password: str
    ) -> Identity:
        """Create new identity."""
        identity = Identity(
            id=uuid4(),
            email=email,
            name=name,
            hashed_password=hashed_password
        )
        self.session.add(identity)
        await self.session.flush()
        return identity


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD REPOSITORY (Event Sourcing)
# ═══════════════════════════════════════════════════════════════════════════════

class ThreadRepository:
    """
    Repository for Thread event sourcing.
    
    Threads use append-only event log pattern.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(
        self,
        id: UUID,
        identity_id: UUID,
        include_events: bool = False
    ) -> Optional[Thread]:
        """
        Get thread with identity check.
        
        R&D Rule #3: Returns None if identity doesn't match.
        """
        stmt = select(Thread).where(
            and_(
                Thread.id == id,
                Thread.owner_identity_id == identity_id
            )
        )
        
        if include_events:
            stmt = stmt.options(selectinload(Thread.events))
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def list_by_sphere(
        self,
        identity_id: UUID,
        sphere: SphereType,
        status: Optional[ThreadStatus] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Thread]:
        """
        List threads by sphere.
        
        R&D Rule #5: Chronological ordering.
        """
        conditions = [
            Thread.owner_identity_id == identity_id,
            Thread.sphere == sphere
        ]
        
        if status:
            conditions.append(Thread.status == status)
        
        stmt = select(Thread).where(
            and_(*conditions)
        ).order_by(
            Thread.updated_at.desc()
        ).limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def create(
        self,
        identity_id: UUID,
        founding_intent: str,
        sphere: SphereType,
        **kwargs
    ) -> Thread:
        """Create new thread with initial event."""
        thread = Thread(
            id=uuid4(),
            owner_identity_id=identity_id,
            founding_intent=founding_intent,
            sphere=sphere,
            **kwargs
        )
        self.session.add(thread)
        await self.session.flush()
        
        # Create initial event
        await self.append_event(
            thread_id=thread.id,
            identity_id=identity_id,
            event_type="thread.created",
            payload={
                "founding_intent": founding_intent,
                "sphere": sphere.value
            }
        )
        
        return thread
    
    async def append_event(
        self,
        thread_id: UUID,
        identity_id: UUID,
        event_type: str,
        payload: Dict[str, Any],
        actor_type: str = "human",
        actor_id: Optional[UUID] = None
    ) -> ThreadEvent:
        """
        Append event to thread (append-only).
        
        Events are IMMUTABLE after creation.
        """
        # Get next sequence number
        stmt = select(func.coalesce(func.max(ThreadEvent.sequence_number), 0)).where(
            ThreadEvent.thread_id == thread_id
        )
        result = await self.session.execute(stmt)
        next_seq = (result.scalar() or 0) + 1
        
        # Get last event ID for causal chain
        stmt = select(ThreadEvent.id).where(
            ThreadEvent.thread_id == thread_id
        ).order_by(ThreadEvent.sequence_number.desc()).limit(1)
        result = await self.session.execute(stmt)
        parent_event_id = result.scalar()
        
        # Create event
        event = ThreadEvent(
            id=uuid4(),
            thread_id=thread_id,
            sequence_number=next_seq,
            parent_event_id=parent_event_id,
            event_type=event_type,
            payload=payload,
            created_by=identity_id,
            actor_type=actor_type,
            actor_id=actor_id
        )
        self.session.add(event)
        
        # Update thread event count
        stmt = update(Thread).where(Thread.id == thread_id).values(
            event_count=Thread.event_count + 1,
            updated_at=func.now()
        )
        await self.session.execute(stmt)
        
        await self.session.flush()
        return event
    
    async def get_events(
        self,
        thread_id: UUID,
        identity_id: UUID,
        limit: int = 100,
        after_sequence: Optional[int] = None
    ) -> List[ThreadEvent]:
        """
        Get thread events.
        
        Events are returned in causal order.
        """
        # Verify ownership
        thread = await self.get_by_id(thread_id, identity_id)
        if not thread:
            return []
        
        conditions = [ThreadEvent.thread_id == thread_id]
        
        if after_sequence:
            conditions.append(ThreadEvent.sequence_number > after_sequence)
        
        stmt = select(ThreadEvent).where(
            and_(*conditions)
        ).order_by(
            ThreadEvent.sequence_number.asc()
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT REPOSITORY (R&D Rule #1)
# ═══════════════════════════════════════════════════════════════════════════════

class CheckpointRepository:
    """
    Repository for checkpoint management.
    
    R&D Rule #1: All sensitive actions require checkpoint approval.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(
        self,
        identity_id: UUID,
        sphere: SphereType,
        checkpoint_type: str,
        action: str,
        description: str,
        payload: Dict[str, Any],
        thread_id: Optional[UUID] = None,
        expires_at: Optional[datetime] = None
    ) -> Checkpoint:
        """Create new checkpoint requiring approval."""
        checkpoint = Checkpoint(
            id=uuid4(),
            identity_id=identity_id,
            sphere=sphere,
            thread_id=thread_id,
            checkpoint_type=checkpoint_type,
            action=action,
            description=description,
            payload=payload,
            status=CheckpointStatus.PENDING,
            expires_at=expires_at
        )
        self.session.add(checkpoint)
        await self.session.flush()
        return checkpoint
    
    async def get_pending(
        self,
        identity_id: UUID,
        limit: int = 20
    ) -> List[Checkpoint]:
        """Get pending checkpoints for identity."""
        stmt = select(Checkpoint).where(
            and_(
                Checkpoint.identity_id == identity_id,
                Checkpoint.status == CheckpointStatus.PENDING
            )
        ).order_by(
            Checkpoint.created_at.desc()
        ).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def approve(
        self,
        checkpoint_id: UUID,
        identity_id: UUID,
        reason: Optional[str] = None
    ) -> Optional[Checkpoint]:
        """Approve a checkpoint."""
        stmt = select(Checkpoint).where(
            and_(
                Checkpoint.id == checkpoint_id,
                Checkpoint.identity_id == identity_id,
                Checkpoint.status == CheckpointStatus.PENDING
            )
        )
        result = await self.session.execute(stmt)
        checkpoint = result.scalar_one_or_none()
        
        if not checkpoint:
            return None
        
        checkpoint.status = CheckpointStatus.APPROVED
        checkpoint.resolved_at = datetime.utcnow()
        checkpoint.resolved_by = identity_id
        checkpoint.resolution_reason = reason
        
        await self.session.flush()
        return checkpoint
    
    async def reject(
        self,
        checkpoint_id: UUID,
        identity_id: UUID,
        reason: str
    ) -> Optional[Checkpoint]:
        """Reject a checkpoint."""
        stmt = select(Checkpoint).where(
            and_(
                Checkpoint.id == checkpoint_id,
                Checkpoint.identity_id == identity_id,
                Checkpoint.status == CheckpointStatus.PENDING
            )
        )
        result = await self.session.execute(stmt)
        checkpoint = result.scalar_one_or_none()
        
        if not checkpoint:
            return None
        
        checkpoint.status = CheckpointStatus.REJECTED
        checkpoint.resolved_at = datetime.utcnow()
        checkpoint.resolved_by = identity_id
        checkpoint.resolution_reason = reason
        
        await self.session.flush()
        return checkpoint


# ═══════════════════════════════════════════════════════════════════════════════
# AUDIT LOG REPOSITORY (R&D Rule #6)
# ═══════════════════════════════════════════════════════════════════════════════

class AuditLogRepository:
    """
    Repository for audit logs.
    
    R&D Rule #6: Complete audit trail.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def log(
        self,
        identity_id: UUID,
        action: AuditLogAction,
        resource_type: str,
        resource_id: Optional[UUID] = None,
        sphere: Optional[SphereType] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        request_id: Optional[UUID] = None,
        actor_type: str = "human",
        actor_id: Optional[UUID] = None
    ) -> AuditLog:
        """Create audit log entry."""
        audit = AuditLog(
            id=uuid4(),
            identity_id=identity_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            sphere=sphere,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            actor_type=actor_type,
            actor_id=actor_id
        )
        self.session.add(audit)
        await self.session.flush()
        return audit
    
    async def get_for_identity(
        self,
        identity_id: UUID,
        limit: int = 100,
        offset: int = 0,
        action: Optional[AuditLogAction] = None,
        sphere: Optional[SphereType] = None
    ) -> List[AuditLog]:
        """Get audit logs for identity (chronological)."""
        conditions = [AuditLog.identity_id == identity_id]
        
        if action:
            conditions.append(AuditLog.action == action)
        if sphere:
            conditions.append(AuditLog.sphere == sphere)
        
        stmt = select(AuditLog).where(
            and_(*conditions)
        ).order_by(
            AuditLog.timestamp.desc()
        ).limit(limit).offset(offset)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "BaseRepository",
    "IdentityRepository",
    "ThreadRepository",
    "CheckpointRepository",
    "AuditLogRepository",
]
