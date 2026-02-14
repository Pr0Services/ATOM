"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V76 — AGENTS ROUTER
═══════════════════════════════════════════════════════════════════════════════
Agent B - Phase B2: Core Routers
Date: 8 Janvier 2026

226 AGENTS SPÉCIALISÉS
- L0: Utility (free, no checkpoint)
- L1: Specialist (paid, no checkpoint)
- L2: Advisor (paid, checkpoint L2+)
- L3: Orchestrator (paid, checkpoint always)
- Nova: System (NOT hireable)

R&D RULES ENFORCED:
- Rule #1: HTTP 423 for L2/L3 execution
- Rule #3: Agents scoped to user identity
- Rule #4: NO AI-to-AI orchestration (CRITICAL)
- Rule #6: Full traceability

DATABASE:
- Migrated from mock dicts to SQLAlchemy async queries
- Graceful fallback when DB unavailable
- NOVA_AGENT remains a constant (never in DB)
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Query, Body, Depends
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from uuid import uuid4, UUID
from enum import Enum
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_db_optional
from app.models.models import Agent as AgentModel

# Logging
logger = logging.getLogger("nova999.agents")

router = APIRouter(prefix="/api/v2/agents", tags=["Agents"])


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class AgentLevel(str, Enum):
    L0 = "L0"  # Utility
    L1 = "L1"  # Specialist
    L2 = "L2"  # Advisor
    L3 = "L3"  # Orchestrator
    SYSTEM = "system"  # Nova only


class AgentCategory(str, Enum):
    UTILITY = "utility"
    ANALYSIS = "analysis"
    CREATION = "creation"
    STRATEGIC = "strategic"
    COMMUNICATION = "communication"
    SYSTEM = "system"


AGENT_LEVEL_CONFIG = {
    "L0": {
        "name": "Utility",
        "requires_checkpoint": False,
        "token_cost": 10,
        "is_free": True,
        "description": "Basic utility agents"
    },
    "L1": {
        "name": "Specialist",
        "requires_checkpoint": False,
        "token_cost": 25,
        "is_free": False,
        "description": "Domain specialists"
    },
    "L2": {
        "name": "Advisor",
        "requires_checkpoint": True,
        "token_cost": 50,
        "is_free": False,
        "description": "Strategic advisors"
    },
    "L3": {
        "name": "Orchestrator",
        "requires_checkpoint": True,
        "token_cost": 100,
        "is_free": False,
        "description": "Complex orchestrators"
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Nova - SYSTEM agent (never hireable, never in DB)
NOVA_AGENT = {
    "id": "nova-system-001",
    "name": "Nova",
    "description": "CHE·NU System Intelligence - Always present, never hireable",
    "level": "system",
    "level_name": "System",
    "category": "system",
    "is_system": True,
    "is_active": True,
    "requires_checkpoint": False,  # Nova CREATES checkpoints
    "can_call_other_agents": False,  # Rule #4: NO AI-to-AI
    "is_hireable": False,  # NEVER in marketplace
    "token_cost": 0,
    "capabilities": ["assist", "guide", "checkpoint_create", "explain", "analyze"]
}

# Fallback marketplace agents (when DB unavailable)
FALLBACK_MARKETPLACE: Dict[str, Dict] = {
    "agent-l0-writer": {
        "id": "agent-l0-writer",
        "name": "Quick Writer",
        "description": "Basic text formatting and editing",
        "level": "L0",
        "level_name": "Utility",
        "category": "utility",
        "is_system": False,
        "is_active": True,
        "requires_checkpoint": False,
        "can_call_other_agents": False,  # Rule #4
        "is_hireable": True,
        "token_cost": 10,
        "capabilities": ["format", "edit", "proofread"],
        "sphere_scope": ["Personal", "Business"],
        "is_hired": False
    },
    "agent-l1-analyst": {
        "id": "agent-l1-analyst",
        "name": "Data Analyst",
        "description": "Data analysis and visualization",
        "level": "L1",
        "level_name": "Specialist",
        "category": "analysis",
        "is_system": False,
        "is_active": True,
        "requires_checkpoint": False,
        "can_call_other_agents": False,  # Rule #4
        "is_hireable": True,
        "token_cost": 25,
        "capabilities": ["analyze", "visualize", "report"],
        "sphere_scope": ["Business", "Scholar"],
        "is_hired": False
    },
    "agent-l2-strategist": {
        "id": "agent-l2-strategist",
        "name": "Strategy Advisor",
        "description": "Strategic planning and recommendations",
        "level": "L2",
        "level_name": "Advisor",
        "category": "strategic",
        "is_system": False,
        "is_active": True,
        "requires_checkpoint": True,  # L2+ requires checkpoint
        "can_call_other_agents": False,  # Rule #4
        "is_hireable": True,
        "token_cost": 50,
        "capabilities": ["strategize", "plan", "recommend"],
        "sphere_scope": ["Business"],
        "is_hired": False
    },
    "agent-l3-orchestrator": {
        "id": "agent-l3-orchestrator",
        "name": "Project Orchestrator",
        "description": "Complex project coordination",
        "level": "L3",
        "level_name": "Orchestrator",
        "category": "strategic",
        "is_system": False,
        "is_active": True,
        "requires_checkpoint": True,  # Always checkpoint
        "can_call_other_agents": False,  # Rule #4: CRITICAL
        "is_hireable": True,
        "token_cost": 100,
        "capabilities": ["coordinate", "plan", "monitor"],
        "sphere_scope": ["Business", "My Team"],
        "is_hired": False
    }
}

# Checkpoints storage (temporary in-memory until checkpoints router handles DB)
_checkpoints: Dict[str, Dict] = {}


def get_current_user_id() -> UUID:
    """Get current user ID (mock - replace with actual auth)."""
    return UUID("00000000-0000-0000-0000-000000000001")


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def _agent_to_dict(agent: AgentModel) -> dict:
    """
    Convert SQLAlchemy Agent model to API response dict.

    Args:
        agent: AgentModel instance

    Returns:
        Dict matching current API response format
    """
    level = agent.agent_type or "L0"
    level_config = AGENT_LEVEL_CONFIG.get(level, AGENT_LEVEL_CONFIG["L0"])

    return {
        "id": str(agent.id),
        "name": agent.name,
        "description": "",  # TODO: Add description field to Agent model
        "level": level,
        "level_name": level_config["name"],
        "category": "utility",  # TODO: Add category field to Agent model
        "is_system": False,
        "is_active": agent.is_active,
        "requires_checkpoint": level_config["requires_checkpoint"],
        "can_call_other_agents": agent.can_call_other_agents,
        "is_hireable": True,
        "token_cost": level_config["token_cost"],
        "capabilities": agent.capabilities or [],
        "is_hired": agent.is_hired,
        "sphere_id": str(agent.sphere_id) if agent.sphere_id else None,
        "owner_id": str(agent.owner_id),
        "token_budget": agent.token_budget,
        "tokens_used": agent.tokens_used,
        "created_at": agent.created_at.isoformat() if hasattr(agent, 'created_at') and agent.created_at else None,
        "updated_at": agent.updated_at.isoformat() if hasattr(agent, 'updated_at') and agent.updated_at else None
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MARKETPLACE ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/marketplace", summary="Browse available agents")
async def list_marketplace(
    level: Optional[AgentLevel] = Query(None),
    category: Optional[AgentCategory] = Query(None),
    sphere: Optional[str] = Query(None),
    is_free: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Browse available agents in marketplace.

    NOTE: Nova is NEVER listed here (system agent).
    R&D RULE #4: All agents have can_call_other_agents=False

    Gracefully falls back to FALLBACK_MARKETPLACE if DB unavailable.
    """
    try:
        if not db:
            raise Exception("DB not connected")
        # Build query
        query = select(AgentModel).where(AgentModel.is_active == True)

        # Apply filters
        if level and level != AgentLevel.SYSTEM:
            query = query.where(AgentModel.agent_type == level.value)

        # Sphere filter
        if sphere:
            pass

        # Free filter
        if is_free is not None:
            if is_free:
                query = query.where(AgentModel.agent_type == "L0")
            else:
                query = query.where(AgentModel.agent_type != "L0")

        # Get total count
        total_query = select(func.count(AgentModel.id)).where(AgentModel.is_active == True)
        if level and level != AgentLevel.SYSTEM:
            total_query = total_query.where(AgentModel.agent_type == level.value)

        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0

        # Apply pagination
        query = query.offset(offset).limit(limit)

        # Execute query
        result = await db.execute(query)
        agents = result.scalars().all()

        # Convert to dicts
        items = [_agent_to_dict(a) for a in agents]

        logger.info(f"Marketplace: Loaded {len(items)} agents from database (total: {total})")

        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
            "note": "Nova (system) is never listed in marketplace",
            "source": "database"
        }

    except Exception as e:
        logger.warning(f"Database unavailable, using fallback marketplace: {e}")

        # Fallback to static data
        agents = list(FALLBACK_MARKETPLACE.values())

        # Apply filters to fallback
        agents = [a for a in agents if not a.get("is_system", False)]

        if level and level != AgentLevel.SYSTEM:
            agents = [a for a in agents if a["level"] == level.value]
        if category:
            agents = [a for a in agents if a["category"] == category.value]
        if sphere:
            agents = [a for a in agents if sphere in a.get("sphere_scope", [])]
        if is_free is not None:
            agents = [a for a in agents if (a["token_cost"] == 0) == is_free]

        total = len(agents)
        agents = agents[offset:offset + limit]

        return {
            "items": agents,
            "total": total,
            "limit": limit,
            "offset": offset,
            "note": "Nova (system) is never listed in marketplace",
            "source": "fallback",
            "warning": "Database unavailable - using fallback data"
        }


@router.get("/marketplace/{agent_id}", summary="Get agent details")
async def get_marketplace_agent(agent_id: str, db: Optional[AsyncSession] = Depends(get_db_optional)):
    """Get details of a marketplace agent."""
    if agent_id == "nova-system-001":
        raise HTTPException(
            status_code=400,
            detail="Nova is a system agent and not available in marketplace"
        )

    try:
        # Try to parse as UUID
        try:
            agent_uuid = UUID(agent_id)
        except ValueError:
            # Check fallback for string IDs
            if agent_id in FALLBACK_MARKETPLACE:
                return FALLBACK_MARKETPLACE[agent_id]
            raise HTTPException(status_code=404, detail="Agent not found")

        # Query database
        result = await db.execute(
            select(AgentModel).where(AgentModel.id == agent_uuid)
        )
        agent = result.scalar_one_or_none()

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        return _agent_to_dict(agent)

    except Exception as e:
        logger.warning(f"Database unavailable, checking fallback: {e}")

        # Fallback to static data
        if agent_id in FALLBACK_MARKETPLACE:
            return FALLBACK_MARKETPLACE[agent_id]

        raise HTTPException(status_code=404, detail="Agent not found")


# ═══════════════════════════════════════════════════════════════════════════════
# HIRED AGENTS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/hired", summary="List user's hired agents")
async def list_hired_agents(db: Optional[AsyncSession] = Depends(get_db_optional)):
    """
    List agents hired by current user.

    NOTE: Nova is always available but not in this list.
    """
    user_id = get_current_user_id()

    try:
        # Query hired agents for this user
        result = await db.execute(
            select(AgentModel).where(
                AgentModel.owner_id == user_id,
                AgentModel.is_hired == True
            )
        )
        agents = result.scalars().all()

        # Convert to dicts
        hired_agents = [_agent_to_dict(a) for a in agents]

        logger.info(f"Hired agents: Found {len(hired_agents)} for user {user_id}")

        return {
            "hired_agents": hired_agents,
            "total": len(hired_agents),
            "nova_available": True,  # Nova always available
            "note": "Nova (system assistant) is always available separately",
            "source": "database"
        }

    except Exception as e:
        logger.warning(f"Database unavailable, returning empty hired list: {e}")

        # Fallback to empty list
        return {
            "hired_agents": [],
            "total": 0,
            "nova_available": True,
            "note": "Nova (system assistant) is always available separately",
            "source": "fallback",
            "warning": "Database unavailable - showing empty hired list"
        }


@router.post("/hired/{agent_id}", summary="Hire an agent")
async def hire_agent(agent_id: str, db: Optional[AsyncSession] = Depends(get_db_optional)):
    """
    Hire an agent from marketplace.

    R&D RULE #6: Hiring is traced.
    """
    user_id = get_current_user_id()

    if agent_id == "nova-system-001":
        raise HTTPException(
            status_code=400,
            detail="Nova is a system agent and cannot be hired (always available)"
        )

    try:
        # Try to parse as UUID
        try:
            agent_uuid = UUID(agent_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Agent not found in marketplace")

        # Find agent
        result = await db.execute(
            select(AgentModel).where(AgentModel.id == agent_uuid)
        )
        agent = result.scalar_one_or_none()

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found in marketplace")

        # Check if already hired
        if agent.is_hired and agent.owner_id == user_id:
            raise HTTPException(status_code=400, detail="Agent already hired")

        # Hire agent
        agent.is_hired = True
        agent.owner_id = user_id
        if hasattr(agent, 'updated_at'):
            agent.updated_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(agent)

        logger.info(f"Agent hired: {agent.name} ({agent.id}) by user {user_id}")

        return {
            "status": "hired",
            "agent_id": str(agent.id),
            "agent_name": agent.name,
            "hired_at": datetime.now(timezone.utc).isoformat(),
            "hired_by": str(user_id),  # Rule #6: Traceability
            "source": "database"
        }

    except Exception as e:
        logger.error(f"Database error during hire: {e}")
        raise HTTPException(
            status_code=503,
            detail="Database unavailable - cannot hire agent at this time"
        )


@router.delete("/hired/{agent_id}", summary="Fire an agent")
async def fire_agent(agent_id: str, db: Optional[AsyncSession] = Depends(get_db_optional)):
    """
    Fire (remove) a hired agent.

    NOTE: Cannot fire Nova.
    """
    user_id = get_current_user_id()

    if agent_id == "nova-system-001":
        raise HTTPException(
            status_code=400,
            detail={
                "error": "cannot_fire_nova",
                "message": "Nova is a system agent and cannot be fired",
                "rule": "R&D_RULE_NOVA_PERMANENT"
            }
        )

    try:
        # Try to parse as UUID
        try:
            agent_uuid = UUID(agent_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Agent not hired")

        # Find agent
        result = await db.execute(
            select(AgentModel).where(
                AgentModel.id == agent_uuid,
                AgentModel.owner_id == user_id,
                AgentModel.is_hired == True
            )
        )
        agent = result.scalar_one_or_none()

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not hired")

        # Fire agent
        agent.is_hired = False
        if hasattr(agent, 'updated_at'):
            agent.updated_at = datetime.now(timezone.utc)

        await db.commit()

        logger.info(f"Agent fired: {agent.name} ({agent.id}) by user {user_id}")

        return {
            "status": "fired",
            "agent_id": str(agent.id),
            "fired_at": datetime.now(timezone.utc).isoformat(),
            "fired_by": str(user_id),
            "source": "database"
        }

    except Exception as e:
        logger.error(f"Database error during fire: {e}")
        raise HTTPException(
            status_code=503,
            detail="Database unavailable - cannot fire agent at this time"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT EXECUTION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/{agent_id}/execute", summary="Execute agent task")
async def execute_agent(
    agent_id: str,
    input: str = Body(..., min_length=1),
    context: Optional[Dict[str, Any]] = Body(None),
    thread_id: Optional[str] = Body(None),
    checkpoint_id: Optional[str] = Body(None),
    # Rule #4: These parameters are FORBIDDEN
    call_agent: Optional[str] = Body(None),
    agent_chain: Optional[List[str]] = Body(None),
    db: Optional[AsyncSession] = Depends(get_db_optional)
):
    """
    Execute an agent task.

    R&D RULE #1: L2/L3 agents require checkpoint (HTTP 423)
    R&D RULE #4: AI-to-AI calls FORBIDDEN (400 error)
    """
    user_id = get_current_user_id()

    # ==== Rule #4: CRITICAL - NO AI-to-AI orchestration ====
    if call_agent is not None:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ai_to_ai_forbidden",
                "message": "R&D Rule #4: AI-to-AI orchestration is FORBIDDEN",
                "rule": "R&D_RULE_4",
                "attempted_call": call_agent,
                "recommendation": "Human must coordinate multiple agents"
            }
        )

    if agent_chain is not None and len(agent_chain) > 0:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "agent_chain_forbidden",
                "message": "R&D Rule #4: Agent chaining is FORBIDDEN",
                "rule": "R&D_RULE_4",
                "attempted_chain": agent_chain,
                "recommendation": "Human must execute agents sequentially"
            }
        )
    # ==== End Rule #4 check ====

    # Get agent (Nova or from DB)
    agent_dict: Optional[Dict[str, Any]] = None

    if agent_id == "nova-system-001":
        agent_dict = NOVA_AGENT
    else:
        try:
            # Try to get from database
            try:
                agent_uuid = UUID(agent_id)
            except ValueError:
                # Check fallback
                if agent_id in FALLBACK_MARKETPLACE:
                    agent_dict = FALLBACK_MARKETPLACE[agent_id]
                else:
                    raise HTTPException(status_code=404, detail="Agent not found")

            if agent_dict is None:
                # Query database
                result = await db.execute(
                    select(AgentModel).where(AgentModel.id == agent_uuid)
                )
                agent_model = result.scalar_one_or_none()

                if not agent_model:
                    raise HTTPException(status_code=404, detail="Agent not found")

                # Check if hired (except Nova)
                if not agent_model.is_hired or agent_model.owner_id != user_id:
                    raise HTTPException(
                        status_code=403,
                        detail="Agent not hired. Hire the agent first."
                    )

                agent_dict = _agent_to_dict(agent_model)

        except Exception as e:
            logger.warning(f"Database unavailable during execute, checking fallback: {e}")

            # Fallback
            if agent_id in FALLBACK_MARKETPLACE:
                agent_dict = FALLBACK_MARKETPLACE[agent_id]
            else:
                raise HTTPException(
                    status_code=503,
                    detail="Database unavailable and agent not in fallback cache"
                )

    if agent_dict is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    # ==== Rule #1: Checkpoint for L2/L3 ====
    if agent_dict.get("requires_checkpoint", False):
        if not checkpoint_id:
            checkpoint = {
                "id": str(uuid4()),
                "type": "agent_execution",
                "status": "pending",
                "agent_id": agent_id,
                "agent_level": agent_dict["level"],
                "message": f"Agent {agent_dict['name']} (Level {agent_dict['level']}) requires approval",
                "input_preview": input[:100] + "..." if len(input) > 100 else input,
                "created_by": str(user_id),
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            _checkpoints[checkpoint["id"]] = checkpoint

            raise HTTPException(
                status_code=423,
                detail={
                    "status": "checkpoint_required",
                    "checkpoint_id": checkpoint["id"],
                    "message": f"L{agent_dict['level'][-1]} agent execution requires human approval",
                    "agent": agent_dict["name"],
                    "level": agent_dict["level"]
                }
            )

        # Verify checkpoint
        if checkpoint_id not in _checkpoints:
            raise HTTPException(status_code=400, detail="Invalid checkpoint")

        cp = _checkpoints[checkpoint_id]
        if cp["status"] != "approved":
            raise HTTPException(status_code=423, detail="Checkpoint not approved")
    # ==== End Rule #1 ====

    # Execute (mock response)
    now = datetime.now(timezone.utc).isoformat()

    execution_result = {
        "execution_id": str(uuid4()),
        "agent_id": agent_id,
        "agent_name": agent_dict["name"],
        "level": agent_dict["level"],
        "input": input,
        "output": f"[Mock response from {agent_dict['name']}]: Processed input successfully",
        "tokens_used": agent_dict.get("token_cost", 0),
        "thread_id": thread_id,
        # Rule #6: Traceability
        "executed_by": str(user_id),
        "executed_at": now,
        "checkpoint_id": checkpoint_id,
        # Rule #4 verification
        "ai_to_ai_calls": 0,  # Always 0
        "agent_chain_used": False  # Always False
    }

    return execution_result


# ═══════════════════════════════════════════════════════════════════════════════
# NOVA SPECIFIC ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/nova", summary="Get Nova info")
async def get_nova():
    """
    Get Nova system agent information.

    Nova is the system intelligence - always present, never hireable.
    """
    return {
        **NOVA_AGENT,
        "note": "Nova is always available and cannot be hired or fired"
    }


@router.post("/nova/assist", summary="Ask Nova for assistance")
async def nova_assist(
    query: str = Body(...),
    context: Optional[Dict[str, Any]] = Body(None),
    thread_id: Optional[str] = Body(None)
):
    """
    Ask Nova for assistance.

    Nova provides guidance and can create checkpoints.
    NOTE: Nova NEVER executes actions autonomously.
    """
    user_id = get_current_user_id()
    now = datetime.now(timezone.utc).isoformat()

    # Mock Nova response
    response = {
        "response_id": str(uuid4()),
        "query": query,
        "response": f"[Nova]: I understand you're asking about '{query[:50]}...'. As your system assistant, I can guide you but won't execute actions autonomously. Would you like me to create a checkpoint for any specific action?",
        "suggestions": [
            {"type": "action", "description": "Create a new thread for this topic"},
            {"type": "checkpoint", "description": "Review pending decisions"},
            {"type": "agent", "description": "Consider hiring a specialist agent"}
        ],
        # Rule #6: Traceability
        "requested_by": str(user_id),
        "requested_at": now,
        "thread_id": thread_id,
        # Nova metadata
        "nova_version": "v76",
        "autonomous_actions_taken": 0  # Always 0 - Nova never acts autonomously
    }

    return response


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT STATS & HEALTH
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats", summary="Agent service statistics")
async def agent_stats(db: Optional[AsyncSession] = Depends(get_db_optional)):
    """Get agent service statistics."""
    user_id = get_current_user_id()

    try:
        # Query hired agents
        result = await db.execute(
            select(AgentModel).where(
                AgentModel.owner_id == user_id,
                AgentModel.is_hired == True
            )
        )
        hired_agents = result.scalars().all()

        # Count by level
        level_counts = {"L0": 0, "L1": 0, "L2": 0, "L3": 0}
        for agent in hired_agents:
            level = agent.agent_type
            if level in level_counts:
                level_counts[level] += 1

        # Get marketplace total
        marketplace_result = await db.execute(
            select(func.count(AgentModel.id)).where(AgentModel.is_active == True)
        )
        marketplace_total = marketplace_result.scalar() or 0

        return {
            "user_id": str(user_id),
            "total_hired": len(hired_agents),
            "hired_by_level": level_counts,
            "marketplace_total": marketplace_total,
            "nova_available": True,
            "r&d_rule_4_enforced": True,
            "ai_to_ai_calls_blocked": "always",
            "source": "database"
        }

    except Exception as e:
        logger.warning(f"Database unavailable, using fallback stats: {e}")

        # Fallback stats
        return {
            "user_id": str(user_id),
            "total_hired": 0,
            "hired_by_level": {"L0": 0, "L1": 0, "L2": 0, "L3": 0},
            "marketplace_total": len(FALLBACK_MARKETPLACE),
            "nova_available": True,
            "r&d_rule_4_enforced": True,
            "ai_to_ai_calls_blocked": "always",
            "source": "fallback",
            "warning": "Database unavailable - showing fallback stats"
        }


@router.get("/health", summary="Agents service health")
async def agents_health(db: Optional[AsyncSession] = Depends(get_db_optional)):
    """Health check for agents service."""

    db_status = "unknown"
    total_agents = len(FALLBACK_MARKETPLACE) + 1  # +1 for Nova

    try:
        # Try to query database
        result = await db.execute(
            select(func.count(AgentModel.id)).where(AgentModel.is_active == True)
        )
        db_count = result.scalar() or 0
        total_agents = db_count + 1  # +1 for Nova
        db_status = "connected"

    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        db_status = "disconnected"

    return {
        "service": "agents",
        "status": "healthy",
        "version": "v76",
        "database_status": db_status,
        "total_agents_available": total_agents,
        "nova_status": "active",
        "r&d_compliance": {
            "rule_1": "HTTP 423 for L2/L3 execution",
            "rule_3": "Agent scope to user identity",
            "rule_4": "AI-to-AI orchestration BLOCKED",
            "rule_6": "Full execution traceability"
        }
    }
