"""
ROUTES: governance_routes.py
PREFIX: /api/v2/governance
VERSION: 1.0.0

PURPOSE: API endpoints for AT-OM Governance Multi-Agent System
- Orchestrator decisions
- CEA signal processing
- Backlog management
- Governance metrics

R&D COMPLIANCE:
- Rule #1: Human gates via HTTP 423 for BLOCK/ASK_HUMAN decisions
- Rule #6: Full traceability on all operations
- Rule #7: Follows governance canon
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
import logging

# Import schemas
from app.schemas.governance_schemas import (
    GovernanceSignal,
    GovernanceSignalLevel,
    GovernanceCriterion,
    Spec,
    SpecCategory,
    SpecRunResult,
    BacklogItem,
    BacklogType,
    BacklogItemCreate,
    OrchestratorDecision,
    OrchDecisionPayload,
    QCTResult,
    SegmentScores,
    Budgets,
    AgentConfiguration,
    FeedbackMetricsResult,
    PolicyTuningResult,
)

# Import services
from app.services.governance.orchestrator_service import OrchestratorService
from app.services.governance.cea_service import CEARegistry
from app.services.governance.backlog_service import BacklogService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2/governance", tags=["Governance"])

# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_orchestrator_service() -> OrchestratorService:
    """Get orchestrator service instance."""
    return OrchestratorService()

def get_cea_registry() -> CEARegistry:
    """Get CEA registry instance."""
    return CEARegistry()

def get_backlog_service() -> BacklogService:
    """Get backlog service instance."""
    return BacklogService()

# ============================================================================
# HEALTH & STATUS
# ============================================================================

@router.get("/health")
async def governance_health():
    """Health check for governance system."""
    return {
        "status": "healthy",
        "system": "AT-OM Governance Multi-Agent",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/status")
async def governance_status(
    orchestrator: OrchestratorService = Depends(get_orchestrator_service),
    cea_registry: CEARegistry = Depends(get_cea_registry),
    backlog: BacklogService = Depends(get_backlog_service)
):
    """Get overall governance system status."""
    return {
        "orchestrator": {
            "active": True,
            "spec_count": len(orchestrator.specs),
            "available_configs": list(orchestrator.config_costs.keys())
        },
        "cea_registry": {
            "active": True,
            "registered_ceas": list(cea_registry.ceas.keys()),
            "always_on": cea_registry.always_on
        },
        "backlog": {
            "active": True,
            "pending_items": backlog.repository.count_pending(),
            "total_items": len(backlog.repository.items)
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# ORCHESTRATOR ENDPOINTS
# ============================================================================

@router.post("/orchestrator/decide")
async def orchestrator_decide(
    thread_id: UUID = Body(..., embed=True),
    work_type: str = Body(..., embed=True),
    content: str = Body(..., embed=True),
    is_live: bool = Body(False, embed=True),
    user_id: UUID = Body(..., embed=True),
    orchestrator: OrchestratorService = Depends(get_orchestrator_service),
    cea_registry: CEARegistry = Depends(get_cea_registry)
):
    """
    Main orchestrator decision endpoint.
    
    Runs CEAs, computes QCT, and returns decision.
    Returns HTTP 423 LOCKED if human approval required.
    """
    try:
        # 1. Run all CEAs on the content
        signals = await cea_registry.run_all(
            content=content,
            context={"thread_id": str(thread_id), "work_type": work_type}
        )
        
        # 2. Build segment scores (simplified - real impl would analyze content)
        segment_scores = SegmentScores(
            doc=0.7 if work_type == "doc" else 0.5,
            code=0.8 if work_type == "code" else 0.4,
            workflow=0.6 if work_type == "workflow" else 0.5,
            xr=0.5 if work_type == "xr" else 0.3
        )
        
        # 3. Build budgets
        budgets = Budgets(
            token_budget=10000,
            tokens_used=len(content.split()) * 2,  # Rough estimate
            latency_budget_ms=5000 if is_live else 30000,
            elapsed_ms=100
        )
        
        # 4. Get orchestrator decision
        decision_payload = await orchestrator.make_decision(
            thread_id=thread_id,
            signals=signals,
            segment_scores=segment_scores,
            budgets=budgets,
            is_live=is_live,
            user_id=user_id
        )
        
        # 5. Check if human approval required (HTTP 423)
        if decision_payload.decision in [
            OrchestratorDecision.BLOCK,
            OrchestratorDecision.ASK_HUMAN
        ]:
            # Return HTTP 423 LOCKED with checkpoint
            return JSONResponse(
                status_code=423,
                content={
                    "status": "checkpoint_pending",
                    "checkpoint": {
                        "id": str(decision_payload.decision_id),
                        "type": "governance",
                        "reason": decision_payload.rationale,
                        "decision": decision_payload.decision.value,
                        "signals": [s.dict() for s in decision_payload.signals],
                        "requires_approval": True,
                        "options": ["approve", "reject", "modify"]
                    },
                    "thread_id": str(thread_id),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        # 6. Return decision
        return {
            "status": "decided",
            "decision": decision_payload.dict(),
            "signals_count": len(signals),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Orchestrator decision error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orchestrator/checkpoint/{checkpoint_id}/approve")
async def approve_checkpoint(
    checkpoint_id: UUID,
    user_id: UUID = Body(..., embed=True),
    reason: str = Body("", embed=True),
    orchestrator: OrchestratorService = Depends(get_orchestrator_service)
):
    """Approve a governance checkpoint (human gate)."""
    try:
        # Log approval event
        event = {
            "type": "CHECKPOINT_APPROVED",
            "checkpoint_id": str(checkpoint_id),
            "approved_by": str(user_id),
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Checkpoint approved: {checkpoint_id} by {user_id}")
        
        return {
            "status": "approved",
            "checkpoint_id": str(checkpoint_id),
            "approved_by": str(user_id),
            "event": event,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Checkpoint approval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orchestrator/checkpoint/{checkpoint_id}/reject")
async def reject_checkpoint(
    checkpoint_id: UUID,
    user_id: UUID = Body(..., embed=True),
    reason: str = Body(..., embed=True),
    orchestrator: OrchestratorService = Depends(get_orchestrator_service)
):
    """Reject a governance checkpoint (human gate)."""
    try:
        event = {
            "type": "CHECKPOINT_REJECTED",
            "checkpoint_id": str(checkpoint_id),
            "rejected_by": str(user_id),
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Checkpoint rejected: {checkpoint_id} by {user_id}")
        
        return {
            "status": "rejected",
            "checkpoint_id": str(checkpoint_id),
            "rejected_by": str(user_id),
            "event": event,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Checkpoint rejection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orchestrator/specs")
async def list_specs(
    orchestrator: OrchestratorService = Depends(get_orchestrator_service)
):
    """List all available specs in the catalog."""
    return {
        "specs": [spec.dict() for spec in orchestrator.specs.values()],
        "count": len(orchestrator.specs),
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/orchestrator/configs")
async def list_agent_configs(
    orchestrator: OrchestratorService = Depends(get_orchestrator_service)
):
    """List available agent configurations with costs."""
    configs = []
    for config_name, cost in orchestrator.config_costs.items():
        configs.append({
            "name": config_name.value,
            "token_cost": cost,
            "description": _get_config_description(config_name)
        })
    
    return {
        "configurations": configs,
        "count": len(configs),
        "timestamp": datetime.utcnow().isoformat()
    }

def _get_config_description(config: AgentConfiguration) -> str:
    """Get human-readable description for agent configuration."""
    descriptions = {
        AgentConfiguration.CONFIG_A: "Minimal - Single fast agent, basic checks",
        AgentConfiguration.CONFIG_B: "Standard - Primary agent + reviewer",
        AgentConfiguration.CONFIG_C: "Enhanced - Multi-agent with CEA checks",
        AgentConfiguration.CONFIG_D: "Deep - Full pipeline with critic agent",
        AgentConfiguration.CONFIG_E: "Maximum - All agents + human-in-loop ready"
    }
    return descriptions.get(config, "Unknown configuration")

# ============================================================================
# CEA ENDPOINTS
# ============================================================================

@router.post("/cea/run")
async def run_cea_checks(
    content: str = Body(..., embed=True),
    context: Dict[str, Any] = Body({}, embed=True),
    cea_names: Optional[List[str]] = Body(None, embed=True),
    cea_registry: CEARegistry = Depends(get_cea_registry)
):
    """
    Run CEA checks on content.
    
    If cea_names provided, runs only those CEAs.
    Otherwise runs all always-on CEAs.
    """
    try:
        if cea_names:
            signals = []
            for name in cea_names:
                cea_signals = await cea_registry.run_specific(name, content, context)
                signals.extend(cea_signals)
        else:
            signals = await cea_registry.run_always_on(content, context)
        
        # Aggregate by level
        by_level = {}
        for signal in signals:
            level = signal.level.value
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(signal.dict())
        
        return {
            "signals": [s.dict() for s in signals],
            "count": len(signals),
            "by_level": by_level,
            "highest_level": max([s.level.value for s in signals]) if signals else None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"CEA run error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cea/registry")
async def list_ceas(
    cea_registry: CEARegistry = Depends(get_cea_registry)
):
    """List all registered CEAs."""
    ceas = []
    for name, cea in cea_registry.ceas.items():
        ceas.append({
            "name": name,
            "criteria": [c.value for c in cea.criteria],
            "always_on": name in cea_registry.always_on
        })
    
    return {
        "ceas": ceas,
        "count": len(ceas),
        "always_on": cea_registry.always_on,
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# BACKLOG ENDPOINTS
# ============================================================================

@router.get("/backlog")
async def list_backlog(
    backlog_type: Optional[BacklogType] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    backlog: BacklogService = Depends(get_backlog_service)
):
    """List backlog items with optional filtering."""
    items = backlog.repository.list_items(
        backlog_type=backlog_type,
        status=status,
        limit=limit,
        offset=offset
    )
    
    return {
        "items": [item.dict() for item in items],
        "count": len(items),
        "total": backlog.repository.count_by_type(backlog_type) if backlog_type else len(backlog.repository.items),
        "filters": {
            "type": backlog_type.value if backlog_type else None,
            "status": status
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/backlog")
async def create_backlog_item(
    item: BacklogItemCreate,
    user_id: UUID = Body(..., embed=True),
    backlog: BacklogService = Depends(get_backlog_service)
):
    """Create a new backlog item."""
    try:
        created = await backlog.capture(
            backlog_type=item.backlog_type,
            source=item.source,
            payload=item.payload,
            severity=item.severity,
            linked_events=item.linked_events,
            user_id=user_id
        )
        
        return {
            "status": "created",
            "item": created.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Backlog creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/backlog/{item_id}/resolve")
async def resolve_backlog_item(
    item_id: UUID,
    resolution: str = Body(..., embed=True),
    user_id: UUID = Body(..., embed=True),
    backlog: BacklogService = Depends(get_backlog_service)
):
    """Resolve a backlog item."""
    try:
        resolved = await backlog.resolve(
            item_id=item_id,
            resolution=resolution,
            user_id=user_id
        )
        
        if not resolved:
            raise HTTPException(status_code=404, detail="Backlog item not found")
        
        return {
            "status": "resolved",
            "item": resolved.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Backlog resolution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/backlog/metrics")
async def backlog_metrics(
    backlog: BacklogService = Depends(get_backlog_service)
):
    """Get backlog feedback metrics."""
    metrics = backlog.compute_feedback_metrics()
    
    return {
        "metrics": metrics.dict(),
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/backlog/tune-policy")
async def tune_policy(
    user_id: UUID = Body(..., embed=True),
    backlog: BacklogService = Depends(get_backlog_service)
):
    """
    Suggest policy tuning based on backlog metrics.
    
    Returns HTTP 423 if large changes require human approval.
    """
    try:
        tuning = await backlog.suggest_policy_tuning(user_id=user_id)
        
        if tuning.requires_human_approval:
            return JSONResponse(
                status_code=423,
                content={
                    "status": "checkpoint_pending",
                    "checkpoint": {
                        "id": str(tuning.tuning_id),
                        "type": "policy_tuning",
                        "reason": "Large policy changes require human approval",
                        "suggestions": tuning.dict(),
                        "requires_approval": True,
                        "options": ["approve", "reject", "partial_approve"]
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        return {
            "status": "auto_applied",
            "tuning": tuning.dict(),
            "message": "Small adjustments auto-applied within bounds",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Policy tuning error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# QCT ALGORITHM ENDPOINT
# ============================================================================

@router.post("/qct/compute")
async def compute_qct(
    segment_scores: SegmentScores = Body(...),
    budgets: Budgets = Body(...),
    is_live: bool = Body(False),
    orchestrator: OrchestratorService = Depends(get_orchestrator_service)
):
    """
    Compute QCT (Quality/Cost Targeting) algorithm result.
    
    Returns optimal agent configuration for given constraints.
    """
    try:
        qct_result = orchestrator.qct.compute(
            segment_scores=segment_scores,
            budgets=budgets,
            is_live=is_live
        )
        
        return {
            "result": qct_result.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"QCT computation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DECISION POINT ENDPOINTS
# ============================================================================

# Import decision point schemas and service
from app.schemas.governance_schemas import (
    DecisionPoint,
    DecisionPointCreate,
    DecisionPointType,
    AgingLevel,
    UserResponseType,
)
from app.services.governance.decision_point_service import DecisionPointService

def get_decision_point_service() -> DecisionPointService:
    """Get decision point service instance."""
    return DecisionPointService()


@router.get("/decision-points")
async def list_decision_points(
    thread_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    point_type: Optional[DecisionPointType] = Query(None),
    aging_level: Optional[AgingLevel] = Query(None),
    include_archived: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    List decision points with optional filters.
    
    Returns active points by default, sorted by urgency (most urgent first).
    """
    points = await service.get_active_points(
        thread_id=thread_id,
        user_id=user_id,
        point_type=point_type,
        aging_level=aging_level,
        limit=limit,
    )
    
    archived = []
    if include_archived:
        archived = await service.repository.list_archived(thread_id=thread_id)
    
    return {
        "points": [p.dict() for p in points],
        "archived": [p.dict() for p in archived] if include_archived else [],
        "count": len(points),
        "filters": {
            "thread_id": thread_id,
            "user_id": user_id,
            "point_type": point_type.value if point_type else None,
            "aging_level": aging_level.value if aging_level else None,
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/decision-points/summary")
async def get_decision_points_summary(
    user_id: Optional[str] = Query(None),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Get summary of decision points by aging level.
    
    Useful for dashboard badges/alerts.
    """
    summary = await service.get_aging_summary(user_id=user_id)
    
    return {
        "summary": summary,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/decision-points/urgent")
async def get_urgent_decision_points(
    user_id: Optional[str] = Query(None),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Get urgent decision points (RED and BLINK only).
    
    For priority alerts and notifications.
    """
    urgent = await service.get_urgent_points(user_id=user_id)
    
    return {
        "points": [p.dict() for p in urgent],
        "count": len(urgent),
        "has_critical": any(p.aging_level == AgingLevel.BLINK for p in urgent),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/decision-points/{point_id}")
async def get_decision_point(
    point_id: str,
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """Get a specific decision point by ID."""
    point = await service.repository.get(point_id)
    
    if not point:
        raise HTTPException(status_code=404, detail="Decision point not found")
    
    return {
        "point": point.dict(),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/decision-points")
async def create_decision_point(
    data: DecisionPointCreate,
    user_id: str = Body(..., embed=True),
    generate_suggestion: bool = Body(True, embed=True),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Create a new decision point.
    
    Optionally generates AI suggestion from Nova.
    """
    try:
        point = await service.create_decision_point(
            create_data=data,
            created_by=user_id,
            generate_suggestion=generate_suggestion,
        )
        
        return {
            "status": "created",
            "point": point.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Decision point creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/decision-points/{point_id}/validate")
async def validate_decision_point(
    point_id: str,
    user_id: str = Body(..., embed=True),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Validate (accept) the AI suggestion for a decision point.
    
    R&D Rule #1: Human explicitly validates Nova's suggestion.
    """
    point = await service.validate_suggestion(
        point_id=point_id,
        user_id=user_id,
    )
    
    if not point:
        raise HTTPException(status_code=404, detail="Decision point not found")
    
    return {
        "status": "validated",
        "point": point.dict(),
        "response_type": "validate",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/decision-points/{point_id}/redirect")
async def redirect_decision_point(
    point_id: str,
    alternative: str = Body(..., embed=True),
    user_id: str = Body(..., embed=True),
    comment: Optional[str] = Body(None, embed=True),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Redirect to an alternative action.
    
    R&D Rule #1: Human chooses different path than AI suggested.
    """
    point = await service.redirect_decision(
        point_id=point_id,
        alternative=alternative,
        user_id=user_id,
        comment=comment,
    )
    
    if not point:
        raise HTTPException(status_code=404, detail="Decision point not found")
    
    return {
        "status": "redirected",
        "point": point.dict(),
        "response_type": "redirect",
        "selected_alternative": alternative,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/decision-points/{point_id}/comment")
async def comment_on_decision_point(
    point_id: str,
    comment: str = Body(..., embed=True),
    user_id: str = Body(..., embed=True),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Add a comment to a decision point.
    
    Does NOT close the decision point - just adds context.
    """
    point = await service.add_comment(
        point_id=point_id,
        comment=comment,
        user_id=user_id,
    )
    
    if not point:
        raise HTTPException(status_code=404, detail="Decision point not found")
    
    return {
        "status": "commented",
        "point": point.dict(),
        "response_type": "comment",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/decision-points/{point_id}/defer")
async def defer_decision_point(
    point_id: str,
    user_id: str = Body(..., embed=True),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Defer a decision point (reset aging timer to GREEN).
    
    Use when user acknowledges but needs more time.
    """
    point = await service.defer_point(
        point_id=point_id,
        user_id=user_id,
    )
    
    if not point:
        raise HTTPException(status_code=404, detail="Decision point not found")
    
    return {
        "status": "deferred",
        "point": point.dict(),
        "response_type": "defer",
        "new_aging_level": "green",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/decision-points/{point_id}/archive")
async def archive_decision_point(
    point_id: str,
    user_id: str = Body(..., embed=True),
    reason: str = Body("manual", embed=True),
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Manually archive a decision point.
    
    Removes from active recall without responding.
    """
    point = await service.archive_point(
        point_id=point_id,
        user_id=user_id,
        reason=reason,
    )
    
    if not point:
        raise HTTPException(status_code=404, detail="Decision point not found")
    
    return {
        "status": "archived",
        "point": point.dict(),
        "archive_reason": reason,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/decision-points/process-aging")
async def process_aging(
    service: DecisionPointService = Depends(get_decision_point_service)
):
    """
    Process aging for all decision points.
    
    Should be called periodically (cron job every minute).
    Updates aging levels and triggers auto-archive for >10 day items.
    """
    try:
        result = await service.process_aging()
        
        return {
            "status": "processed",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Aging processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
