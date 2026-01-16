"""
CHE·NU™ Checkpoint Service
==========================

Service for managing governance checkpoints (HTTP 423 human gates).

When a sensitive action is detected:
1. Create a checkpoint
2. Return HTTP 423 LOCKED
3. Block until human approval
4. Execute or cancel based on resolution

R&D COMPLIANCE:
✅ Rule #1: Human Sovereignty - all sensitive actions gated
✅ Rule #6: Full traceability via audit logs
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
import logging

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.governance import (
    GovernanceCheckpoint,
    AuditLog,
    CheckpointType,
    CheckpointStatus,
    AuditAction,
    AuditResourceType,
)
from app.core.exceptions import (
    NotFoundError,
    ForbiddenError,
    CheckpointRequiredError,
)

logger = logging.getLogger(__name__)


class CheckpointService:
    """
    Service for governance checkpoints.
    
    Checkpoints are the core mechanism for human sovereignty.
    When an action requires human approval:
    1. create_checkpoint() creates a pending checkpoint
    2. API returns HTTP 423 LOCKED
    3. Human reviews and resolves (approve/reject)
    4. Original action executes or cancels
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # =========================================================================
    # CREATE CHECKPOINT
    # =========================================================================
    
    async def create_checkpoint(
        self,
        identity_id: UUID,
        checkpoint_type: str,
        reason: str,
        action_data: Dict[str, Any],
        thread_id: Optional[UUID] = None,
        options: Optional[List[str]] = None,
        expires_in_minutes: Optional[int] = 60,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> GovernanceCheckpoint:
        """
        Create a new governance checkpoint.
        
        This will block the requested action until human resolution.
        
        Args:
            identity_id: User who initiated the action
            checkpoint_type: Type (governance, cost, identity, sensitive, etc.)
            reason: Human-readable reason for checkpoint
            action_data: The pending action data to execute on approval
            thread_id: Optional thread context
            options: Resolution options (default: ["approve", "reject"])
            expires_in_minutes: Expiration time (None for no expiration)
            metadata: Additional context
        
        Returns:
            Created checkpoint
        """
        checkpoint = GovernanceCheckpoint(
            id=uuid4(),
            identity_id=identity_id,
            thread_id=thread_id,
            checkpoint_type=checkpoint_type,
            reason=reason,
            action_data=action_data,
            options=options or ["approve", "reject"],
            status=CheckpointStatus.PENDING,
            expires_at=(
                datetime.utcnow() + timedelta(minutes=expires_in_minutes)
                if expires_in_minutes else None
            ),
            metadata=metadata or {},
        )
        
        self.db.add(checkpoint)
        await self.db.flush()
        
        # Audit log
        await self._audit(
            identity_id=identity_id,
            action=AuditAction.CHECKPOINT_CREATED,
            resource_type=AuditResourceType.CHECKPOINT,
            resource_id=checkpoint.id,
            details={
                "checkpoint_type": checkpoint_type,
                "reason": reason,
                "thread_id": str(thread_id) if thread_id else None,
            }
        )
        
        logger.info(
            f"Checkpoint created: {checkpoint.id} "
            f"(type={checkpoint_type}, identity={identity_id})"
        )
        
        return checkpoint
    
    # =========================================================================
    # GET CHECKPOINTS
    # =========================================================================
    
    async def get_checkpoint(
        self,
        checkpoint_id: UUID,
        identity_id: UUID,
    ) -> GovernanceCheckpoint:
        """
        Get a checkpoint by ID.
        
        Args:
            checkpoint_id: Checkpoint ID
            identity_id: Requesting user (for identity boundary)
        
        Returns:
            The checkpoint
        
        Raises:
            NotFoundError: Checkpoint not found
            ForbiddenError: Cross-identity access
        """
        result = await self.db.execute(
            select(GovernanceCheckpoint)
            .where(GovernanceCheckpoint.id == checkpoint_id)
        )
        checkpoint = result.scalar_one_or_none()
        
        if not checkpoint:
            raise NotFoundError(f"Checkpoint not found: {checkpoint_id}")
        
        # Identity boundary check
        if checkpoint.identity_id != identity_id:
            raise ForbiddenError("Identity boundary violation")
        
        return checkpoint
    
    async def list_pending_checkpoints(
        self,
        identity_id: UUID,
        thread_id: Optional[UUID] = None,
        checkpoint_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[GovernanceCheckpoint]:
        """
        List pending checkpoints for a user.
        
        Args:
            identity_id: User ID
            thread_id: Optional filter by thread
            checkpoint_type: Optional filter by type
            limit: Max results
        
        Returns:
            List of pending checkpoints
        """
        query = (
            select(GovernanceCheckpoint)
            .where(
                and_(
                    GovernanceCheckpoint.identity_id == identity_id,
                    GovernanceCheckpoint.status == CheckpointStatus.PENDING,
                )
            )
            .order_by(GovernanceCheckpoint.created_at.desc())
            .limit(limit)
        )
        
        if thread_id:
            query = query.where(GovernanceCheckpoint.thread_id == thread_id)
        
        if checkpoint_type:
            query = query.where(GovernanceCheckpoint.checkpoint_type == checkpoint_type)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def list_checkpoints(
        self,
        identity_id: UUID,
        status: Optional[str] = None,
        thread_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[List[GovernanceCheckpoint], int]:
        """
        List checkpoints with pagination.
        
        Args:
            identity_id: User ID
            status: Optional filter by status
            thread_id: Optional filter by thread
            limit: Page size
            offset: Skip count
        
        Returns:
            Tuple of (checkpoints, total_count)
        """
        base_query = (
            select(GovernanceCheckpoint)
            .where(GovernanceCheckpoint.identity_id == identity_id)
        )
        
        if status:
            base_query = base_query.where(GovernanceCheckpoint.status == status)
        
        if thread_id:
            base_query = base_query.where(GovernanceCheckpoint.thread_id == thread_id)
        
        # Get total count
        from sqlalchemy import func
        count_query = select(func.count()).select_from(base_query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Get page
        query = (
            base_query
            .order_by(GovernanceCheckpoint.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        checkpoints = list(result.scalars().all())
        
        return checkpoints, total
    
    # =========================================================================
    # RESOLVE CHECKPOINT
    # =========================================================================
    
    async def approve_checkpoint(
        self,
        checkpoint_id: UUID,
        identity_id: UUID,
        reason: Optional[str] = None,
    ) -> GovernanceCheckpoint:
        """
        Approve a pending checkpoint.
        
        Args:
            checkpoint_id: Checkpoint to approve
            identity_id: User approving
            reason: Optional approval reason
        
        Returns:
            Updated checkpoint
        
        Raises:
            NotFoundError: Checkpoint not found
            ForbiddenError: Cross-identity or already resolved
        """
        checkpoint = await self.get_checkpoint(checkpoint_id, identity_id)
        
        if not checkpoint.is_pending:
            raise ForbiddenError(
                f"Checkpoint already resolved: {checkpoint.status}"
            )
        
        if checkpoint.is_expired:
            checkpoint.status = CheckpointStatus.EXPIRED
            await self.db.flush()
            raise ForbiddenError("Checkpoint has expired")
        
        # Approve
        checkpoint.approve(resolved_by=identity_id, reason=reason)
        await self.db.flush()
        
        # Audit log
        await self._audit(
            identity_id=identity_id,
            action=AuditAction.CHECKPOINT_APPROVED,
            resource_type=AuditResourceType.CHECKPOINT,
            resource_id=checkpoint.id,
            details={
                "checkpoint_type": checkpoint.checkpoint_type,
                "reason": reason,
            }
        )
        
        logger.info(f"Checkpoint approved: {checkpoint_id}")
        
        return checkpoint
    
    async def reject_checkpoint(
        self,
        checkpoint_id: UUID,
        identity_id: UUID,
        reason: Optional[str] = None,
    ) -> GovernanceCheckpoint:
        """
        Reject a pending checkpoint.
        
        Args:
            checkpoint_id: Checkpoint to reject
            identity_id: User rejecting
            reason: Optional rejection reason
        
        Returns:
            Updated checkpoint
        """
        checkpoint = await self.get_checkpoint(checkpoint_id, identity_id)
        
        if not checkpoint.is_pending:
            raise ForbiddenError(
                f"Checkpoint already resolved: {checkpoint.status}"
            )
        
        # Reject
        checkpoint.reject(resolved_by=identity_id, reason=reason)
        await self.db.flush()
        
        # Audit log
        await self._audit(
            identity_id=identity_id,
            action=AuditAction.CHECKPOINT_REJECTED,
            resource_type=AuditResourceType.CHECKPOINT,
            resource_id=checkpoint.id,
            details={
                "checkpoint_type": checkpoint.checkpoint_type,
                "reason": reason,
            }
        )
        
        logger.info(f"Checkpoint rejected: {checkpoint_id}")
        
        return checkpoint
    
    # =========================================================================
    # EXPIRE CHECKPOINTS
    # =========================================================================
    
    async def expire_stale_checkpoints(self) -> int:
        """
        Expire all checkpoints past their expiration date.
        
        This should be called periodically by a background task.
        
        Returns:
            Number of checkpoints expired
        """
        from sqlalchemy import update
        
        now = datetime.utcnow()
        
        result = await self.db.execute(
            update(GovernanceCheckpoint)
            .where(
                and_(
                    GovernanceCheckpoint.status == CheckpointStatus.PENDING,
                    GovernanceCheckpoint.expires_at < now,
                )
            )
            .values(status=CheckpointStatus.EXPIRED)
            .returning(GovernanceCheckpoint.id)
        )
        
        expired_ids = list(result.scalars().all())
        
        logger.info(f"Expired {len(expired_ids)} checkpoints")
        
        return len(expired_ids)
    
    # =========================================================================
    # HELPER: RAISE IF CHECKPOINT REQUIRED
    # =========================================================================
    
    def raise_checkpoint_required(
        self,
        checkpoint: GovernanceCheckpoint,
    ) -> None:
        """
        Raise CheckpointRequiredError with checkpoint details.
        
        Use this after creating a checkpoint to trigger HTTP 423.
        """
        raise CheckpointRequiredError(
            checkpoint_id=checkpoint.id,
            checkpoint_type=checkpoint.checkpoint_type,
            reason=checkpoint.reason,
            options=checkpoint.options,
        )
    
    # =========================================================================
    # AUDIT LOGGING
    # =========================================================================
    
    async def _audit(
        self,
        identity_id: UUID,
        action: str,
        resource_type: str,
        resource_id: Optional[UUID] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """Create an audit log entry."""
        audit = AuditLog(
            id=uuid4(),
            identity_id=identity_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(audit)
        await self.db.flush()
        return audit


# =============================================================================
# AUDIT SERVICE
# =============================================================================

class AuditService:
    """
    Service for querying audit logs.
    
    Audit logs are read-only after creation.
    This service provides query capabilities.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def log(
        self,
        identity_id: Optional[UUID],
        action: str,
        resource_type: str,
        resource_id: Optional[UUID] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """
        Create an audit log entry.
        
        Args:
            identity_id: User who performed action (None for system)
            action: Action type (use AuditAction constants)
            resource_type: Resource type (use AuditResourceType constants)
            resource_id: ID of affected resource
            details: Additional context
            ip_address: Client IP
            user_agent: Client user agent
        
        Returns:
            Created audit log
        """
        audit = AuditLog(
            id=uuid4(),
            identity_id=identity_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(audit)
        await self.db.flush()
        return audit
    
    async def list_logs(
        self,
        identity_id: Optional[UUID] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[List[AuditLog], int]:
        """
        Query audit logs with filters.
        
        Args:
            identity_id: Filter by user
            action: Filter by action type
            resource_type: Filter by resource type
            resource_id: Filter by resource ID
            start_date: Filter from date
            end_date: Filter to date
            limit: Page size
            offset: Skip count
        
        Returns:
            Tuple of (logs, total_count)
        """
        query = select(AuditLog)
        
        if identity_id:
            query = query.where(AuditLog.identity_id == identity_id)
        
        if action:
            query = query.where(AuditLog.action == action)
        
        if resource_type:
            query = query.where(AuditLog.resource_type == resource_type)
        
        if resource_id:
            query = query.where(AuditLog.resource_id == resource_id)
        
        if start_date:
            query = query.where(AuditLog.created_at >= start_date)
        
        if end_date:
            query = query.where(AuditLog.created_at <= end_date)
        
        # Count
        from sqlalchemy import func
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Get page
        query = (
            query
            .order_by(AuditLog.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        logs = list(result.scalars().all())
        
        return logs, total
    
    async def get_resource_history(
        self,
        resource_type: str,
        resource_id: UUID,
        limit: int = 50,
    ) -> List[AuditLog]:
        """
        Get full audit history for a resource.
        
        Args:
            resource_type: Type of resource
            resource_id: Resource ID
            limit: Max results
        
        Returns:
            List of audit logs for this resource
        """
        result = await self.db.execute(
            select(AuditLog)
            .where(
                and_(
                    AuditLog.resource_type == resource_type,
                    AuditLog.resource_id == resource_id,
                )
            )
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
    
    async def get_user_activity(
        self,
        identity_id: UUID,
        limit: int = 50,
    ) -> List[AuditLog]:
        """
        Get recent activity for a user.
        
        Args:
            identity_id: User ID
            limit: Max results
        
        Returns:
            List of recent audit logs for this user
        """
        result = await self.db.execute(
            select(AuditLog)
            .where(AuditLog.identity_id == identity_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
