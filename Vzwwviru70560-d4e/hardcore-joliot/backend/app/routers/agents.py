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
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from uuid import uuid4
from enum import Enum

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
# MOCK DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

# Nova - SYSTEM agent (never hireable)
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

# Sample marketplace agents
MOCK_MARKETPLACE: Dict[str, Dict] = {
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
        "sphere_scope": ["Personal", "Business"]
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
        "sphere_scope": ["Business", "Scholar"]
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
        "sphere_scope": ["Business"]
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
        "sphere_scope": ["Business", "My Team"]
    }
}

# User's hired agents
MOCK_HIRED: Dict[str, List[str]] = {}  # user_id -> [agent_ids]

# Checkpoints
MOCK_CHECKPOINTS: Dict[str, Dict] = {}


def get_current_user_id() -> str:
    return "test-user-001"


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
    offset: int = Query(0, ge=0)
):
    """
    Browse available agents in marketplace.
    
    NOTE: Nova is NEVER listed here (system agent).
    R&D RULE #4: All agents have can_call_other_agents=False
    """
    agents = list(MOCK_MARKETPLACE.values())
    
    # Filter out system agents (Nova)
    agents = [a for a in agents if not a.get("is_system", False)]
    
    # Apply filters
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
        "note": "Nova (system) is never listed in marketplace"
    }


@router.get("/marketplace/{agent_id}", summary="Get agent details")
async def get_marketplace_agent(agent_id: str):
    """Get details of a marketplace agent."""
    if agent_id == "nova-system-001":
        raise HTTPException(
            status_code=400,
            detail="Nova is a system agent and not available in marketplace"
        )
    
    if agent_id not in MOCK_MARKETPLACE:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return MOCK_MARKETPLACE[agent_id]


# ═══════════════════════════════════════════════════════════════════════════════
# HIRED AGENTS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/hired", summary="List user's hired agents")
async def list_hired_agents():
    """
    List agents hired by current user.
    
    NOTE: Nova is always available but not in this list.
    """
    user_id = get_current_user_id()
    
    hired_ids = MOCK_HIRED.get(user_id, [])
    agents = []
    
    for agent_id in hired_ids:
        if agent_id in MOCK_MARKETPLACE:
            agent = MOCK_MARKETPLACE[agent_id].copy()
            agent["hired_at"] = "2026-01-08T00:00:00Z"  # Mock
            agents.append(agent)
    
    return {
        "hired_agents": agents,
        "total": len(agents),
        "nova_available": True,  # Nova always available
        "note": "Nova (system assistant) is always available separately"
    }


@router.post("/hired/{agent_id}", summary="Hire an agent")
async def hire_agent(agent_id: str):
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
    
    if agent_id not in MOCK_MARKETPLACE:
        raise HTTPException(status_code=404, detail="Agent not found in marketplace")
    
    agent = MOCK_MARKETPLACE[agent_id]
    
    if not agent.get("is_hireable", True):
        raise HTTPException(status_code=400, detail="Agent is not hireable")
    
    # Initialize user's hired list
    if user_id not in MOCK_HIRED:
        MOCK_HIRED[user_id] = []
    
    if agent_id in MOCK_HIRED[user_id]:
        raise HTTPException(status_code=400, detail="Agent already hired")
    
    MOCK_HIRED[user_id].append(agent_id)
    
    return {
        "status": "hired",
        "agent_id": agent_id,
        "agent_name": agent["name"],
        "hired_at": datetime.now(timezone.utc).isoformat(),
        "hired_by": user_id  # Rule #6: Traceability
    }


@router.delete("/hired/{agent_id}", summary="Fire an agent")
async def fire_agent(agent_id: str):
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
    
    if user_id not in MOCK_HIRED or agent_id not in MOCK_HIRED[user_id]:
        raise HTTPException(status_code=404, detail="Agent not hired")
    
    MOCK_HIRED[user_id].remove(agent_id)
    
    return {
        "status": "fired",
        "agent_id": agent_id,
        "fired_at": datetime.now(timezone.utc).isoformat(),
        "fired_by": user_id
    }


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
    agent_chain: Optional[List[str]] = Body(None)
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
    
    # Get agent
    if agent_id == "nova-system-001":
        agent = NOVA_AGENT
    elif agent_id in MOCK_MARKETPLACE:
        agent = MOCK_MARKETPLACE[agent_id]
        # Check if hired (except Nova)
        if user_id not in MOCK_HIRED or agent_id not in MOCK_HIRED[user_id]:
            raise HTTPException(
                status_code=403,
                detail="Agent not hired. Hire the agent first."
            )
    else:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # ==== Rule #1: Checkpoint for L2/L3 ====
    if agent.get("requires_checkpoint", False):
        if not checkpoint_id:
            checkpoint = {
                "id": str(uuid4()),
                "type": "agent_execution",
                "status": "pending",
                "agent_id": agent_id,
                "agent_level": agent["level"],
                "message": f"Agent {agent['name']} (Level {agent['level']}) requires approval",
                "input_preview": input[:100] + "..." if len(input) > 100 else input,
                "created_by": user_id,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            MOCK_CHECKPOINTS[checkpoint["id"]] = checkpoint
            
            raise HTTPException(
                status_code=423,
                detail={
                    "status": "checkpoint_required",
                    "checkpoint_id": checkpoint["id"],
                    "message": f"L{agent['level'][-1]} agent execution requires human approval",
                    "agent": agent["name"],
                    "level": agent["level"]
                }
            )
        
        # Verify checkpoint
        if checkpoint_id not in MOCK_CHECKPOINTS:
            raise HTTPException(status_code=400, detail="Invalid checkpoint")
        
        cp = MOCK_CHECKPOINTS[checkpoint_id]
        if cp["status"] != "approved":
            raise HTTPException(status_code=423, detail="Checkpoint not approved")
    # ==== End Rule #1 ====
    
    # Execute (mock response)
    now = datetime.now(timezone.utc).isoformat()
    
    execution_result = {
        "execution_id": str(uuid4()),
        "agent_id": agent_id,
        "agent_name": agent["name"],
        "level": agent["level"],
        "input": input,
        "output": f"[Mock response from {agent['name']}]: Processed input successfully",
        "tokens_used": agent.get("token_cost", 0),
        "thread_id": thread_id,
        # Rule #6: Traceability
        "executed_by": user_id,
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
        "requested_by": user_id,
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
async def agent_stats():
    """Get agent service statistics."""
    user_id = get_current_user_id()
    hired = MOCK_HIRED.get(user_id, [])
    
    # Count by level
    level_counts = {"L0": 0, "L1": 0, "L2": 0, "L3": 0}
    for agent_id in hired:
        if agent_id in MOCK_MARKETPLACE:
            level = MOCK_MARKETPLACE[agent_id]["level"]
            level_counts[level] = level_counts.get(level, 0) + 1
    
    return {
        "user_id": user_id,
        "total_hired": len(hired),
        "hired_by_level": level_counts,
        "marketplace_total": len(MOCK_MARKETPLACE),
        "nova_available": True,
        "r&d_rule_4_enforced": True,
        "ai_to_ai_calls_blocked": "always"
    }


@router.get("/health", summary="Agents service health")
async def agents_health():
    """Health check for agents service."""
    return {
        "service": "agents",
        "status": "healthy",
        "version": "v76",
        "total_agents_available": len(MOCK_MARKETPLACE) + 1,  # +1 for Nova
        "nova_status": "active",
        "r&d_compliance": {
            "rule_1": "HTTP 423 for L2/L3 execution",
            "rule_3": "Agent scope to user identity",
            "rule_4": "AI-to-AI orchestration BLOCKED",
            "rule_6": "Full execution traceability"
        }
    }
