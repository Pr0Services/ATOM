"""
CHE·NU™ Agent API Routes
========================

REST API endpoints for agent registry and execution.

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - HTTP 423 for executions requiring approval
- Rule #4: No AI-to-AI orchestration - trigger validation
- Rule #6: Traceability - all endpoints log to audit trail

ENDPOINTS:
- GET /agents - List all agents
- GET /agents/spheres - Get agents by sphere summary
- GET /agents/{agent_id} - Get agent details
- GET /agents/sphere/{sphere_type} - Get agents for specific sphere
- POST /agents/execute - Request agent execution (may return 423)
- POST /agents/executions/{execution_id}/approve - Approve pending execution
- POST /agents/executions/{execution_id}/reject - Reject pending execution
- GET /agents/executions - List user's executions
- GET /agents/executions/pending - List pending approvals
- GET /agents/executions/{execution_id} - Get execution details
- DELETE /agents/executions/{execution_id} - Cancel execution
- GET /agents/config - Get user's agent configurations
- PUT /agents/config/{agent_id} - Update user's agent configuration
"""

from __future__ import annotations

import logging
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.exceptions import (
    NotFoundError,
    ValidationError,
    ForbiddenError,
    CheckpointRequiredError,
)
from backend.api.dependencies import get_current_user, get_current_identity_id
from backend.models.user import User
from backend.models.agent import SphereType, AgentStatus, ExecutionStatus, AgentCapabilityType
from backend.services.agent import (
    AgentRegistryService,
    AgentExecutionService,
    TOTAL_AGENTS,
    AGENT_DISTRIBUTION,
)
from backend.schemas.agent_schemas import (
    AgentResponse,
    AgentSummary,
    AgentListResponse,
    SphereAgentSummary,
    AllSpheresAgentSummary,
    UserAgentConfigUpdate,
    UserAgentConfigResponse,
    ExecutionRequest,
    ExecutionApproval,
    ExecutionResponse,
    ExecutionListResponse,
    ExecutionCheckpointResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["Agents"])


# =============================================================================
# EXCEPTION HANDLERS
# =============================================================================

def handle_service_error(e: Exception):
    """Convert service exceptions to HTTP exceptions."""
    if isinstance(e, NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    elif isinstance(e, ValidationError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    elif isinstance(e, ForbiddenError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    elif isinstance(e, CheckpointRequiredError):
        # HTTP 423 LOCKED - Human gate triggered
        raise HTTPException(
            status_code=423,  # Locked
            detail={
                "status": "checkpoint_required",
                "message": str(e),
                "checkpoint_id": str(e.checkpoint_id),
                "action_type": e.action_type,
                "preview": e.preview,
            }
        )
    else:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# =============================================================================
# AGENT REGISTRY ENDPOINTS
# =============================================================================

@router.get(
    "",
    response_model=AgentListResponse,
    summary="List all agents",
    description="Get list of all 226 agents with optional filters."
)
async def list_agents(
    sphere_type: Optional[SphereType] = Query(None, description="Filter by sphere"),
    status_filter: Optional[AgentStatus] = Query(None, alias="status", description="Filter by status"),
    capability: Optional[AgentCapabilityType] = Query(None, description="Filter by capability"),
    requires_human_gate: Optional[bool] = Query(None, description="Filter by human gate requirement"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all available agents.
    
    Can filter by sphere, status, capability, or human gate requirement.
    """
    try:
        registry = AgentRegistryService(db)
        agents = await registry.list_agents(
            sphere_type=sphere_type,
            status=status_filter,
            capability=capability,
            requires_human_gate=requires_human_gate,
        )
        
        # Count by sphere
        by_sphere = {}
        for agent in agents:
            sphere = agent.sphere_type.value
            by_sphere[sphere] = by_sphere.get(sphere, 0) + 1
        
        return AgentListResponse(
            agents=[
                AgentSummary(
                    id=a.id,
                    name=a.name,
                    display_name=a.display_name,
                    sphere_type=a.sphere_type,
                    status=a.status,
                    capabilities=a.capabilities,
                    requires_human_gate=a.requires_human_gate,
                )
                for a in agents
            ],
            total=len(agents),
            by_sphere=by_sphere,
        )
    except Exception as e:
        handle_service_error(e)


@router.get(
    "/spheres",
    response_model=AllSpheresAgentSummary,
    summary="Get agents by sphere summary",
    description="Get summary of all 226 agents organized by the 9 spheres."
)
async def get_agents_by_sphere(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get agent distribution across all 9 spheres.
    
    Returns count and list of agents per sphere.
    """
    try:
        registry = AgentRegistryService(db)
        return await registry.get_all_spheres_summary()
    except Exception as e:
        handle_service_error(e)


@router.get(
    "/sphere/{sphere_type}",
    response_model=SphereAgentSummary,
    summary="Get agents for specific sphere",
    description="Get all agents for a specific sphere."
)
async def get_sphere_agents(
    sphere_type: SphereType,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all agents for a specific sphere."""
    try:
        registry = AgentRegistryService(db)
        agents = await registry.get_agents_by_sphere(sphere_type)
        
        return SphereAgentSummary(
            sphere_type=sphere_type,
            total_agents=len(agents),
            active_agents=len([a for a in agents if a.status == AgentStatus.ACTIVE]),
            agents=[
                AgentSummary(
                    id=a.id,
                    name=a.name,
                    display_name=a.display_name,
                    sphere_type=a.sphere_type,
                    status=a.status,
                    capabilities=a.capabilities,
                    requires_human_gate=a.requires_human_gate,
                )
                for a in agents
            ]
        )
    except Exception as e:
        handle_service_error(e)


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
    summary="Get agent details",
    description="Get full details of a specific agent."
)
async def get_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get full details of a specific agent."""
    try:
        registry = AgentRegistryService(db)
        agent = await registry.get_agent(agent_id)
        
        return AgentResponse(
            id=agent.id,
            name=agent.name,
            display_name=agent.display_name,
            description=agent.description,
            sphere_type=agent.sphere_type,
            status=agent.status,
            capabilities=agent.capabilities,
            scope=agent.scope,
            default_token_budget=agent.default_token_budget,
            max_token_budget=agent.max_token_budget,
            cost_per_1k_tokens=agent.cost_per_1k_tokens,
            preferred_llm=agent.preferred_llm,
            requires_human_gate=agent.requires_human_gate,
            human_gate_capabilities=agent.human_gate_capabilities,
            version=agent.version,
            created_at=agent.created_at,
            updated_at=agent.updated_at,
        )
    except Exception as e:
        handle_service_error(e)


# =============================================================================
# EXECUTION ENDPOINTS
# =============================================================================

@router.post(
    "/execute",
    response_model=ExecutionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Execute an agent",
    description="""
    Request agent execution. 
    
    If the capability requires human approval, returns HTTP 423 (Locked) 
    with checkpoint details. User must approve/reject before execution proceeds.
    
    R&D COMPLIANCE:
    - Rule #1: Human Sovereignty - sensitive capabilities require approval
    - Rule #4: trigger cannot be 'agent_request' (no AI-to-AI orchestration)
    """,
    responses={
        201: {"description": "Execution completed successfully"},
        423: {"description": "Checkpoint required - human approval needed"},
    }
)
async def execute_agent(
    request: ExecutionRequest,
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """
    Execute an agent with the specified capability.
    
    May return HTTP 423 if human approval is required.
    """
    try:
        service = AgentExecutionService(db)
        result = await service.request_execution(request, identity_id)
        await db.commit()
        return result
    except CheckpointRequiredError as e:
        await db.commit()  # Commit the checkpoint
        raise HTTPException(
            status_code=423,
            detail={
                "status": "checkpoint_required",
                "message": str(e),
                "checkpoint_id": str(e.checkpoint_id),
                "action_type": e.action_type,
                "preview": e.preview,
            }
        )
    except Exception as e:
        await db.rollback()
        handle_service_error(e)


@router.post(
    "/executions/{execution_id}/approve",
    response_model=ExecutionResponse,
    summary="Approve pending execution",
    description="Approve a pending execution and run it."
)
async def approve_execution(
    execution_id: UUID,
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """
    Approve a pending execution.
    
    The execution will run immediately after approval.
    """
    try:
        service = AgentExecutionService(db)
        result = await service.approve_execution(execution_id, identity_id)
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        handle_service_error(e)


@router.post(
    "/executions/{execution_id}/reject",
    response_model=ExecutionResponse,
    summary="Reject pending execution",
    description="Reject a pending execution."
)
async def reject_execution(
    execution_id: UUID,
    reason: Optional[str] = Query(None, description="Rejection reason"),
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """
    Reject a pending execution.
    
    The execution will be marked as rejected and will not run.
    """
    try:
        service = AgentExecutionService(db)
        result = await service.reject_execution(execution_id, identity_id, reason)
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        handle_service_error(e)


@router.get(
    "/executions",
    response_model=ExecutionListResponse,
    summary="List executions",
    description="List user's agent executions with optional filters."
)
async def list_executions(
    agent_id: Optional[UUID] = Query(None, description="Filter by agent"),
    status_filter: Optional[ExecutionStatus] = Query(None, alias="status", description="Filter by status"),
    sphere_id: Optional[UUID] = Query(None, description="Filter by sphere"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """List user's executions with filters."""
    try:
        service = AgentExecutionService(db)
        return await service.list_executions(
            identity_id=identity_id,
            agent_id=agent_id,
            status=status_filter,
            sphere_id=sphere_id,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        handle_service_error(e)


@router.get(
    "/executions/pending",
    response_model=List[ExecutionResponse],
    summary="List pending approvals",
    description="List all executions pending human approval."
)
async def list_pending_approvals(
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """Get all executions waiting for user approval."""
    try:
        service = AgentExecutionService(db)
        return await service.get_pending_approvals(identity_id)
    except Exception as e:
        handle_service_error(e)


@router.get(
    "/executions/{execution_id}",
    response_model=ExecutionResponse,
    summary="Get execution details",
    description="Get details of a specific execution."
)
async def get_execution(
    execution_id: UUID,
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """Get execution details."""
    try:
        service = AgentExecutionService(db)
        return await service.get_execution(execution_id, identity_id)
    except Exception as e:
        handle_service_error(e)


@router.delete(
    "/executions/{execution_id}",
    response_model=ExecutionResponse,
    summary="Cancel execution",
    description="Cancel a pending or running execution."
)
async def cancel_execution(
    execution_id: UUID,
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """Cancel an execution."""
    try:
        service = AgentExecutionService(db)
        result = await service.cancel_execution(execution_id, identity_id)
        await db.commit()
        return result
    except Exception as e:
        await db.rollback()
        handle_service_error(e)


# =============================================================================
# USER CONFIGURATION ENDPOINTS
# =============================================================================

@router.get(
    "/config",
    response_model=List[UserAgentConfigResponse],
    summary="Get user's agent configurations",
    description="Get user's custom configurations for agents."
)
async def get_user_agent_configs(
    sphere_type: Optional[SphereType] = Query(None, description="Filter by sphere"),
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """Get user's agent configurations."""
    try:
        registry = AgentRegistryService(db)
        configs = await registry.list_user_agent_configs(identity_id, sphere_type)
        
        # Build response with agent info
        responses = []
        for config in configs:
            agent = await registry.get_agent(config.agent_id)
            responses.append(UserAgentConfigResponse(
                id=config.id,
                agent_id=config.agent_id,
                identity_id=config.identity_id,
                enabled=config.enabled,
                custom_name=config.custom_name,
                token_budget_override=config.token_budget_override,
                effective_token_budget=config.effective_token_budget,
                total_executions=config.total_executions,
                total_tokens_used=config.total_tokens_used,
                total_cost=config.total_cost,
                last_used_at=config.last_used_at,
                created_at=config.created_at,
                updated_at=config.updated_at,
                agent=AgentSummary(
                    id=agent.id,
                    name=agent.name,
                    display_name=agent.display_name,
                    sphere_type=agent.sphere_type,
                    status=agent.status,
                    capabilities=agent.capabilities,
                    requires_human_gate=agent.requires_human_gate,
                )
            ))
        
        return responses
    except Exception as e:
        handle_service_error(e)


@router.put(
    "/config/{agent_id}",
    response_model=UserAgentConfigResponse,
    summary="Update agent configuration",
    description="Update user's configuration for a specific agent."
)
async def update_user_agent_config(
    agent_id: UUID,
    update_data: UserAgentConfigUpdate,
    db: AsyncSession = Depends(get_db),
    identity_id: UUID = Depends(get_current_identity_id),
):
    """Update user's configuration for an agent."""
    try:
        registry = AgentRegistryService(db)
        config = await registry.update_user_agent_config(identity_id, agent_id, update_data)
        agent = await registry.get_agent(agent_id)
        
        await db.commit()
        
        return UserAgentConfigResponse(
            id=config.id,
            agent_id=config.agent_id,
            identity_id=config.identity_id,
            enabled=config.enabled,
            custom_name=config.custom_name,
            token_budget_override=config.token_budget_override,
            effective_token_budget=config.effective_token_budget,
            total_executions=config.total_executions,
            total_tokens_used=config.total_tokens_used,
            total_cost=config.total_cost,
            last_used_at=config.last_used_at,
            created_at=config.created_at,
            updated_at=config.updated_at,
            agent=AgentSummary(
                id=agent.id,
                name=agent.name,
                display_name=agent.display_name,
                sphere_type=agent.sphere_type,
                status=agent.status,
                capabilities=agent.capabilities,
                requires_human_gate=agent.requires_human_gate,
            )
        )
    except Exception as e:
        await db.rollback()
        handle_service_error(e)


# =============================================================================
# STATS ENDPOINT
# =============================================================================

@router.get(
    "/stats",
    summary="Get agent system stats",
    description="Get statistics about the agent system."
)
async def get_agent_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get agent system statistics."""
    try:
        registry = AgentRegistryService(db)
        counts = await registry.count_agents()
        
        return {
            "total_agents": TOTAL_AGENTS,
            "expected_distribution": AGENT_DISTRIBUTION,
            "actual_distribution": counts,
            "spheres_count": 9,
        }
    except Exception as e:
        handle_service_error(e)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["router"]
