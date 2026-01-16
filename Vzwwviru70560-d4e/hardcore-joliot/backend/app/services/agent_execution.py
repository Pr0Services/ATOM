"""
CHE·NU™ Agent Execution Service
===============================

Handles agent execution with Human Gates (Rule #1: Human Sovereignty).

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - Sensitive actions require approval (HTTP 423)
- Rule #4: My Team Restrictions - NO AI-to-AI orchestration
- Rule #6: Traceability - All executions audited

CRITICAL:
- Agents PROPOSE, humans DECIDE
- NO autonomous execution for sensitive capabilities
- All executions recorded in audit trail
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID, uuid4

from sqlalchemy import select, func, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    NotFoundError,
    ValidationError,
    ConflictError,
    ForbiddenError,
    CheckpointRequiredError,
)
from app.models.agent import (
    Agent,
    AgentStatus,
    AgentCapabilityType,
    SphereType,
    UserAgentConfig,
    AgentExecution,
    AgentExecutionStep,
    ExecutionStatus,
    ExecutionTrigger,
)
from app.models.governance import GovernanceCheckpoint, CheckpointStatus, CheckpointType
from app.schemas.agent_schemas import (
    ExecutionRequest,
    ExecutionApproval,
    ExecutionResponse,
    ExecutionSummary,
    ExecutionListResponse,
    ExecutionCheckpointResponse,
)
from app.services.agent_registry import AgentRegistryService

logger = logging.getLogger(__name__)


# =============================================================================
# CAPABILITY CLASSIFICATION
# =============================================================================

# Capabilities that ALWAYS require human approval
SENSITIVE_CAPABILITIES = {
    AgentCapabilityType.EMAIL_DRAFT,
    AgentCapabilityType.MESSAGE_DRAFT,
    AgentCapabilityType.NOTIFICATION_DRAFT,
}

# Capabilities that may require approval based on context
CONDITIONAL_APPROVAL_CAPABILITIES = {
    AgentCapabilityType.TEXT_GENERATION,      # For external communication
    AgentCapabilityType.CODE_GENERATION,       # For production code
    AgentCapabilityType.DOCUMENT_PROCESSING,   # For official documents
}


def requires_human_gate(
    agent: Agent,
    capability: AgentCapabilityType,
    context: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, str]:
    """
    Determine if execution requires human approval.
    
    Returns: (requires_approval: bool, reason: str)
    """
    # Check if agent always requires human gate
    if agent.requires_human_gate:
        return True, f"Agent '{agent.display_name}' requires approval for all actions"
    
    # Check if this specific capability requires gate on this agent
    if capability.value in agent.human_gate_capabilities:
        return True, f"Capability '{capability.value}' requires approval on this agent"
    
    # Check if capability is universally sensitive
    if capability in SENSITIVE_CAPABILITIES:
        return True, f"Capability '{capability.value}' always requires human approval"
    
    # Check context for conditional approval
    if capability in CONDITIONAL_APPROVAL_CAPABILITIES:
        if context:
            # External communication triggers gate
            if context.get("is_external", False):
                return True, "External communication requires approval"
            # Production deployment triggers gate
            if context.get("is_production", False):
                return True, "Production deployment requires approval"
    
    return False, ""


# =============================================================================
# AGENT EXECUTION SERVICE
# =============================================================================

class AgentExecutionService:
    """
    Service for executing agents with Human Gates.
    
    R&D COMPLIANCE:
    - Rule #1: Sensitive executions trigger HTTP 423 checkpoint
    - Rule #4: NO trigger type "agent_request" allowed
    - Rule #6: All executions recorded with full traceability
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.registry = AgentRegistryService(db)
    
    # -------------------------------------------------------------------------
    # EXECUTION CREATION
    # -------------------------------------------------------------------------
    
    async def request_execution(
        self,
        request: ExecutionRequest,
        identity_id: UUID,
    ) -> ExecutionResponse | ExecutionCheckpointResponse:
        """
        Request an agent execution.
        
        If the capability requires human approval, returns HTTP 423 checkpoint.
        Otherwise, starts execution and returns result.
        
        Args:
            request: Execution request with agent_id, capability, input_data
            identity_id: ID of the user requesting execution
            
        Returns:
            ExecutionResponse if no approval needed
            ExecutionCheckpointResponse (HTTP 423) if approval required
        """
        # Validate trigger (Rule #4: No AI-to-AI)
        if request.trigger.value == "agent_request":
            raise ValidationError("AI-to-AI orchestration is forbidden (Rule #4)")
        
        # Get agent
        agent = await self.registry.get_agent(request.agent_id)
        
        # Verify agent is active
        if agent.status != AgentStatus.ACTIVE:
            raise ValidationError(f"Agent '{agent.name}' is not active: {agent.status.value}")
        
        # Verify agent has the requested capability
        if request.capability.value not in agent.capabilities:
            raise ValidationError(
                f"Agent '{agent.name}' does not have capability: {request.capability.value}"
            )
        
        # Check sphere access if specified
        if request.sphere_id:
            await self._verify_sphere_access(identity_id, request.sphere_id, agent.sphere_type)
        
        # Get user's config for token budget
        user_config = await self.registry.get_or_create_user_agent_config(identity_id, agent.id)
        if not user_config.enabled:
            raise ValidationError(f"Agent '{agent.name}' is disabled for this user")
        
        # Calculate effective token budget
        token_budget = request.token_budget or user_config.effective_token_budget
        
        # Create execution record (Rule #6: Traceability)
        execution = AgentExecution(
            id=uuid4(),
            agent_id=agent.id,
            identity_id=identity_id,
            sphere_id=request.sphere_id,
            thread_id=request.thread_id,
            trigger=request.trigger,
            status=ExecutionStatus.PENDING,
            capability_used=request.capability.value,
            input_data=request.input_data,
            requires_approval=False,  # Will be updated
            created_at=datetime.now(timezone.utc),
            created_by=identity_id,  # Always human (Rule #1)
        )
        
        # Check if human gate is required (Rule #1)
        needs_approval, approval_reason = requires_human_gate(
            agent,
            request.capability,
            request.input_data.get("context"),
        )
        
        if needs_approval:
            return await self._create_execution_checkpoint(
                execution,
                agent,
                approval_reason,
            )
        
        # No approval needed - execute immediately
        self.db.add(execution)
        await self.db.flush()
        
        # Start execution
        result = await self._execute_agent(execution, agent, token_budget)
        
        return result
    
    async def _create_execution_checkpoint(
        self,
        execution: AgentExecution,
        agent: Agent,
        reason: str,
    ) -> ExecutionCheckpointResponse:
        """
        Create a checkpoint for execution requiring human approval.
        
        Returns HTTP 423 response with checkpoint details.
        """
        execution.status = ExecutionStatus.AWAITING_APPROVAL
        execution.requires_approval = True
        
        # Create governance checkpoint
        checkpoint = GovernanceCheckpoint(
            id=uuid4(),
            identity_id=execution.identity_id,
            checkpoint_type=CheckpointType.SENSITIVE_ACTION,
            status=CheckpointStatus.PENDING,
            action_type="agent_execution",
            action_data={
                "execution_id": str(execution.id),
                "agent_id": str(agent.id),
                "agent_name": agent.name,
                "capability": execution.capability_used,
                "input_preview": self._get_input_preview(execution.input_data),
            },
            reason=reason,
            requires_explicit_approval=True,
            created_by=execution.identity_id,
        )
        
        execution.checkpoint_id = checkpoint.id
        
        self.db.add(checkpoint)
        self.db.add(execution)
        await self.db.flush()
        
        logger.info(
            f"Checkpoint created for agent execution: "
            f"agent={agent.name}, capability={execution.capability_used}"
        )
        
        # Return HTTP 423 response
        raise CheckpointRequiredError(
            message=f"Execution requires human approval: {reason}",
            checkpoint_id=checkpoint.id,
            action_type="agent_execution",
            preview={
                "execution_id": str(execution.id),
                "agent_name": agent.display_name,
                "capability": execution.capability_used,
                "preview": self._get_input_preview(execution.input_data),
            }
        )
    
    def _get_input_preview(self, input_data: Dict[str, Any], max_length: int = 200) -> Dict[str, Any]:
        """Get a safe preview of input data for checkpoint display."""
        preview = {}
        for key, value in input_data.items():
            if isinstance(value, str):
                preview[key] = value[:max_length] + "..." if len(value) > max_length else value
            elif isinstance(value, (int, float, bool)):
                preview[key] = value
            elif isinstance(value, dict):
                preview[key] = "{...}"
            elif isinstance(value, list):
                preview[key] = f"[{len(value)} items]"
            else:
                preview[key] = str(type(value).__name__)
        return preview
    
    # -------------------------------------------------------------------------
    # APPROVAL HANDLING
    # -------------------------------------------------------------------------
    
    async def approve_execution(
        self,
        execution_id: UUID,
        approver_id: UUID,
    ) -> ExecutionResponse:
        """
        Approve a pending execution and run it.
        
        Args:
            execution_id: ID of execution to approve
            approver_id: ID of user approving (must match identity_id)
            
        Returns:
            ExecutionResponse with results
        """
        execution = await self._get_execution(execution_id)
        
        # Verify ownership (Identity Boundary)
        if execution.identity_id != approver_id:
            raise ForbiddenError("Cannot approve another user's execution")
        
        # Verify status
        if execution.status != ExecutionStatus.AWAITING_APPROVAL:
            raise ValidationError(
                f"Execution is not awaiting approval: {execution.status.value}"
            )
        
        # Update execution
        execution.status = ExecutionStatus.APPROVED
        execution.approved_by = approver_id
        execution.approved_at = datetime.now(timezone.utc)
        
        # Update checkpoint
        if execution.checkpoint_id:
            await self._resolve_checkpoint(execution.checkpoint_id, True, approver_id)
        
        await self.db.flush()
        
        # Get agent and execute
        agent = await self.registry.get_agent(execution.agent_id)
        user_config = await self.registry.get_user_agent_config(execution.identity_id, agent.id)
        token_budget = user_config.effective_token_budget if user_config else agent.default_token_budget
        
        result = await self._execute_agent(execution, agent, token_budget)
        
        logger.info(f"Execution approved and completed: {execution_id}")
        
        return result
    
    async def reject_execution(
        self,
        execution_id: UUID,
        rejector_id: UUID,
        reason: Optional[str] = None,
    ) -> ExecutionResponse:
        """
        Reject a pending execution.
        
        Args:
            execution_id: ID of execution to reject
            rejector_id: ID of user rejecting
            reason: Optional rejection reason
            
        Returns:
            ExecutionResponse with rejected status
        """
        execution = await self._get_execution(execution_id)
        
        # Verify ownership
        if execution.identity_id != rejector_id:
            raise ForbiddenError("Cannot reject another user's execution")
        
        # Verify status
        if execution.status != ExecutionStatus.AWAITING_APPROVAL:
            raise ValidationError(
                f"Execution is not awaiting approval: {execution.status.value}"
            )
        
        # Update execution
        execution.status = ExecutionStatus.REJECTED
        execution.rejection_reason = reason
        
        # Update checkpoint
        if execution.checkpoint_id:
            await self._resolve_checkpoint(execution.checkpoint_id, False, rejector_id, reason)
        
        await self.db.flush()
        
        logger.info(f"Execution rejected: {execution_id}, reason: {reason}")
        
        return await self._build_execution_response(execution)
    
    async def _resolve_checkpoint(
        self,
        checkpoint_id: UUID,
        approved: bool,
        resolver_id: UUID,
        reason: Optional[str] = None,
    ) -> None:
        """Update checkpoint status."""
        await self.db.execute(
            update(GovernanceCheckpoint)
            .where(GovernanceCheckpoint.id == checkpoint_id)
            .values(
                status=CheckpointStatus.APPROVED if approved else CheckpointStatus.REJECTED,
                resolved_by=resolver_id,
                resolved_at=datetime.now(timezone.utc),
                resolution_note=reason,
            )
        )
    
    # -------------------------------------------------------------------------
    # EXECUTION ENGINE
    # -------------------------------------------------------------------------
    
    async def _execute_agent(
        self,
        execution: AgentExecution,
        agent: Agent,
        token_budget: int,
    ) -> ExecutionResponse:
        """
        Execute the agent and record results.
        
        This is where the actual AI call would happen.
        For now, returns a mock response.
        """
        execution.status = ExecutionStatus.RUNNING
        execution.started_at = datetime.now(timezone.utc)
        
        await self.db.flush()
        
        start_time = time.time()
        
        try:
            # TODO: Actual LLM execution
            # This is where we would call the LLM with:
            # - agent.system_prompt
            # - agent.llm_config
            # - execution.input_data
            
            # Mock response for now
            output_data = {
                "result": f"Mock execution result for {agent.display_name}",
                "capability": execution.capability_used,
                "status": "completed",
                "note": "This is a placeholder. Real LLM integration pending.",
            }
            
            # Mock token counts
            input_tokens = len(str(execution.input_data)) // 4  # Rough estimate
            output_tokens = len(str(output_data)) // 4
            
            # Update execution
            execution.status = ExecutionStatus.COMPLETED
            execution.output_data = output_data
            execution.input_tokens = input_tokens
            execution.output_tokens = output_tokens
            execution.total_tokens = input_tokens + output_tokens
            execution.cost = (execution.total_tokens / 1000) * agent.cost_per_1k_tokens
            execution.llm_used = agent.preferred_llm or "mock"
            execution.completed_at = datetime.now(timezone.utc)
            execution.duration_ms = int((time.time() - start_time) * 1000)
            
            # Update user stats
            user_config = await self.registry.get_user_agent_config(
                execution.identity_id,
                agent.id
            )
            if user_config:
                user_config.total_executions += 1
                user_config.total_tokens_used += execution.total_tokens
                user_config.total_cost += execution.cost
                user_config.last_used_at = datetime.now(timezone.utc)
            
            await self.db.flush()
            
            logger.info(
                f"Execution completed: agent={agent.name}, "
                f"tokens={execution.total_tokens}, cost=${execution.cost:.4f}"
            )
            
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.error_message = str(e)
            execution.error_code = type(e).__name__
            execution.completed_at = datetime.now(timezone.utc)
            execution.duration_ms = int((time.time() - start_time) * 1000)
            
            await self.db.flush()
            
            logger.error(f"Execution failed: {execution.id}, error: {e}")
        
        return await self._build_execution_response(execution)
    
    # -------------------------------------------------------------------------
    # QUERIES
    # -------------------------------------------------------------------------
    
    async def _get_execution(self, execution_id: UUID) -> AgentExecution:
        """Get execution by ID."""
        result = await self.db.execute(
            select(AgentExecution).where(AgentExecution.id == execution_id)
        )
        execution = result.scalar_one_or_none()
        
        if not execution:
            raise NotFoundError(f"Execution not found: {execution_id}")
        
        return execution
    
    async def get_execution(
        self,
        execution_id: UUID,
        identity_id: UUID,
    ) -> ExecutionResponse:
        """Get execution by ID with identity boundary check."""
        execution = await self._get_execution(execution_id)
        
        if execution.identity_id != identity_id:
            raise ForbiddenError("Cannot access another user's execution")
        
        return await self._build_execution_response(execution)
    
    async def list_executions(
        self,
        identity_id: UUID,
        agent_id: Optional[UUID] = None,
        status: Optional[ExecutionStatus] = None,
        sphere_id: Optional[UUID] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> ExecutionListResponse:
        """List executions for a user."""
        query = select(AgentExecution).where(
            AgentExecution.identity_id == identity_id
        )
        
        conditions = []
        if agent_id:
            conditions.append(AgentExecution.agent_id == agent_id)
        if status:
            conditions.append(AgentExecution.status == status)
        if sphere_id:
            conditions.append(AgentExecution.sphere_id == sphere_id)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)
        
        # Get paginated results
        query = query.order_by(AgentExecution.created_at.desc())
        query = query.offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        executions = list(result.scalars().all())
        
        # Count by status
        status_query = select(
            AgentExecution.status,
            func.count(AgentExecution.id)
        ).where(
            AgentExecution.identity_id == identity_id
        ).group_by(AgentExecution.status)
        
        status_result = await self.db.execute(status_query)
        by_status = {row[0].value: row[1] for row in status_result.all()}
        
        return ExecutionListResponse(
            executions=[
                ExecutionSummary(
                    id=e.id,
                    agent_id=e.agent_id,
                    status=e.status,
                    capability_used=e.capability_used,
                    requires_approval=e.requires_approval,
                    total_tokens=e.total_tokens,
                    cost=e.cost,
                    duration_ms=e.duration_ms,
                    created_at=e.created_at,
                )
                for e in executions
            ],
            total=total or 0,
            by_status=by_status,
        )
    
    async def get_pending_approvals(
        self,
        identity_id: UUID,
    ) -> List[ExecutionResponse]:
        """Get all executions pending approval for a user."""
        result = await self.db.execute(
            select(AgentExecution)
            .where(
                and_(
                    AgentExecution.identity_id == identity_id,
                    AgentExecution.status == ExecutionStatus.AWAITING_APPROVAL,
                )
            )
            .order_by(AgentExecution.created_at.desc())
        )
        
        executions = list(result.scalars().all())
        return [await self._build_execution_response(e) for e in executions]
    
    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------
    
    async def _verify_sphere_access(
        self,
        identity_id: UUID,
        sphere_id: UUID,
        expected_sphere_type: SphereType,
    ) -> None:
        """
        Verify user has access to sphere and sphere matches agent type.
        
        This prevents using a Business agent in Personal sphere, etc.
        """
        # TODO: Implement sphere access check
        # For now, just log
        logger.debug(f"Sphere access check: {identity_id} -> {sphere_id} ({expected_sphere_type})")
    
    async def _build_execution_response(
        self,
        execution: AgentExecution,
    ) -> ExecutionResponse:
        """Build execution response from model."""
        # Get steps if any
        steps_result = await self.db.execute(
            select(AgentExecutionStep)
            .where(AgentExecutionStep.execution_id == execution.id)
            .order_by(AgentExecutionStep.step_number)
        )
        steps = list(steps_result.scalars().all())
        
        return ExecutionResponse(
            id=execution.id,
            agent_id=execution.agent_id,
            identity_id=execution.identity_id,
            sphere_id=execution.sphere_id,
            thread_id=execution.thread_id,
            trigger=execution.trigger,
            status=execution.status,
            capability_used=execution.capability_used,
            input_data=execution.input_data,
            output_data=execution.output_data,
            requires_approval=execution.requires_approval,
            checkpoint_id=execution.checkpoint_id,
            approved_by=execution.approved_by,
            approved_at=execution.approved_at,
            rejection_reason=execution.rejection_reason,
            input_tokens=execution.input_tokens,
            output_tokens=execution.output_tokens,
            total_tokens=execution.total_tokens,
            cost=execution.cost,
            duration_ms=execution.duration_ms,
            llm_used=execution.llm_used,
            error_message=execution.error_message,
            error_code=execution.error_code,
            created_at=execution.created_at,
            created_by=execution.created_by,
            started_at=execution.started_at,
            completed_at=execution.completed_at,
            steps=[],  # TODO: Map steps
        )
    
    async def cancel_execution(
        self,
        execution_id: UUID,
        identity_id: UUID,
    ) -> ExecutionResponse:
        """Cancel a pending or running execution."""
        execution = await self._get_execution(execution_id)
        
        if execution.identity_id != identity_id:
            raise ForbiddenError("Cannot cancel another user's execution")
        
        if execution.status not in [ExecutionStatus.PENDING, ExecutionStatus.RUNNING, ExecutionStatus.AWAITING_APPROVAL]:
            raise ValidationError(f"Cannot cancel execution in status: {execution.status.value}")
        
        execution.status = ExecutionStatus.CANCELLED
        execution.completed_at = datetime.now(timezone.utc)
        
        await self.db.flush()
        
        logger.info(f"Execution cancelled: {execution_id}")
        
        return await self._build_execution_response(execution)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "AgentExecutionService",
    "requires_human_gate",
    "SENSITIVE_CAPABILITIES",
    "CONDITIONAL_APPROVAL_CAPABILITIES",
]
