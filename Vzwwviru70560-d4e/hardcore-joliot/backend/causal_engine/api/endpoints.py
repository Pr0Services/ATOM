"""
============================================================================
CHE·NU™ V69 — CAUSAL ENGINE API
============================================================================
Version: 1.0.0
Purpose: FastAPI endpoints for causal reasoning
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field

from ..core.models import (
    CausalDAG,
    CausalNode,
    CausalEdge,
    CausalEffect,
    SensitivityScore,
    Intervention,
    InterventionType,
    ConfidenceLevel,
    ValidationStatus,
)
from ..core.dag_builder import DAGBuilder, DAGManager, get_dag_manager
from ..core.inference import CausalEngine
from ..counterfactual.engine import CounterfactualEngine, ScenarioComparator
from ..bridge.human_decision import HumanDecisionBridge, DecisionPackage, DecisionRecord

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/causal", tags=["Causal Engine"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CreateDAGRequest(BaseModel):
    """Request to create a new DAG"""
    name: str = Field(..., description="DAG name")
    description: Optional[str] = Field(default=None)
    tenant_id: Optional[str] = Field(default=None)
    sphere: Optional[str] = Field(default=None)
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)


class DAGResponse(BaseModel):
    """DAG response"""
    id: str
    name: str
    version: str
    node_count: int
    edge_count: int
    status: str
    hash: str
    created_at: datetime


class EffectQueryRequest(BaseModel):
    """Request for causal effect estimation"""
    dag_id: str = Field(...)
    treatment: str = Field(...)
    outcome: str = Field(...)


class SensitivityRequest(BaseModel):
    """Request for sensitivity analysis"""
    dag_id: str = Field(...)
    outcome: str = Field(...)
    top_n: int = Field(default=5)


class CounterfactualRequest(BaseModel):
    """Request for counterfactual analysis"""
    dag_id: str = Field(...)
    intervention_node: str = Field(...)
    intervention_value: float = Field(...)
    outcome_node: str = Field(...)
    factual_value: Optional[float] = Field(default=None)


class ScenarioCompareRequest(BaseModel):
    """Request to compare scenarios"""
    dag_id: str = Field(...)
    scenarios: List[Dict[str, float]] = Field(...)
    outcome_node: str = Field(...)
    scenario_names: Optional[List[str]] = Field(default=None)


class CreateDecisionPackageRequest(BaseModel):
    """Request to create decision package"""
    dag_id: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    outcome_node: str = Field(...)
    intervention_scenarios: List[Dict[str, float]] = Field(...)
    scenario_names: Optional[List[str]] = Field(default=None)
    deadline: Optional[datetime] = Field(default=None)


class RecordDecisionRequest(BaseModel):
    """Request to record human decision"""
    package_id: str = Field(...)
    selected_option_id: str = Field(...)
    rationale: str = Field(...)
    decider_name: Optional[str] = Field(default=None)
    decider_role: Optional[str] = Field(default=None)


class ApproveDAGRequest(BaseModel):
    """Request to approve DAG"""
    notes: Optional[str] = Field(default=None)


# ============================================================================
# DEPENDENCIES
# ============================================================================

def get_tenant_id(x_tenant_id: Optional[str] = Header(default=None)) -> str:
    """Get tenant ID from header"""
    return x_tenant_id or "default"


def get_user_id(x_user_id: Optional[str] = Header(default=None)) -> str:
    """Get user ID from header"""
    if not x_user_id:
        raise HTTPException(400, "X-User-Id header required")
    return x_user_id


# ============================================================================
# DAG ENDPOINTS
# ============================================================================

@router.post("/dags", response_model=DAGResponse)
async def create_dag(
    request: CreateDAGRequest,
    tenant_id: str = Depends(get_tenant_id),
    user_id: str = Depends(get_user_id),
):
    """Create a new causal DAG"""
    try:
        builder = DAGBuilder(
            name=request.name,
            tenant_id=tenant_id,
            sphere=request.sphere,
        )
        builder.set_description(request.description or "")
        builder.set_created_by(user_id)
        
        # Add nodes
        for node_data in request.nodes:
            builder.add_slot_node(
                name=node_data.get("name", "unnamed"),
                description=node_data.get("description"),
                domain=node_data.get("domain"),
                unit=node_data.get("unit"),
                is_manipulable=node_data.get("is_manipulable", True),
            )
        
        # Add edges
        for edge_data in request.edges:
            builder.add_causal_edge(
                source_name=edge_data.get("source"),
                target_name=edge_data.get("target"),
                coefficient=edge_data.get("coefficient"),
            )
        
        # Build and store
        dag = builder.build()
        manager = get_dag_manager()
        manager.store(dag)
        
        logger.info(f"Created DAG {dag.id} for tenant {tenant_id}")
        
        return DAGResponse(
            id=dag.id,
            name=dag.name,
            version=dag.version,
            node_count=dag.node_count,
            edge_count=dag.edge_count,
            status=dag.status.value,
            hash=dag.hash,
            created_at=dag.created_at,
        )
    
    except Exception as e:
        logger.error(f"Failed to create DAG: {e}")
        raise HTTPException(400, str(e))


@router.get("/dags/{dag_id}", response_model=Dict[str, Any])
async def get_dag(
    dag_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    """Get DAG by ID"""
    manager = get_dag_manager()
    dag = manager.get(dag_id)
    
    if dag is None:
        raise HTTPException(404, f"DAG not found: {dag_id}")
    
    if dag.tenant_id and dag.tenant_id != tenant_id:
        raise HTTPException(403, "Access denied")
    
    return {
        "id": dag.id,
        "name": dag.name,
        "version": dag.version,
        "description": dag.description,
        "nodes": [n.model_dump() for n in dag.nodes.values()],
        "edges": [e.model_dump() for e in dag.edges],
        "status": dag.status.value,
        "hash": dag.hash,
        "created_at": dag.created_at.isoformat(),
        "approved_by": dag.approved_by,
        "approved_at": dag.approved_at.isoformat() if dag.approved_at else None,
    }


@router.post("/dags/{dag_id}/submit-for-approval")
async def submit_dag_for_approval(
    dag_id: str,
    user_id: str = Depends(get_user_id),
):
    """Submit DAG for human approval"""
    manager = get_dag_manager()
    
    if not manager.submit_for_approval(dag_id, user_id):
        raise HTTPException(400, "Cannot submit DAG for approval")
    
    return {"status": "submitted", "dag_id": dag_id}


@router.post("/dags/{dag_id}/approve")
async def approve_dag(
    dag_id: str,
    request: ApproveDAGRequest,
    user_id: str = Depends(get_user_id),
):
    """Human approval of DAG (HITL)"""
    manager = get_dag_manager()
    
    if not manager.approve(dag_id, user_id, request.notes):
        raise HTTPException(400, "Cannot approve DAG")
    
    logger.info(f"DAG {dag_id} APPROVED by {user_id}")
    
    return {"status": "approved", "dag_id": dag_id, "approved_by": user_id}


@router.post("/dags/{dag_id}/reject")
async def reject_dag(
    dag_id: str,
    reason: str,
    user_id: str = Depends(get_user_id),
):
    """Human rejection of DAG"""
    manager = get_dag_manager()
    
    if not manager.reject(dag_id, user_id, reason):
        raise HTTPException(400, "Cannot reject DAG")
    
    return {"status": "rejected", "dag_id": dag_id, "reason": reason}


# ============================================================================
# CAUSAL EFFECT ENDPOINTS
# ============================================================================

@router.post("/effects/estimate")
async def estimate_causal_effect(
    request: EffectQueryRequest,
    tenant_id: str = Depends(get_tenant_id),
):
    """Estimate causal effect of treatment on outcome"""
    manager = get_dag_manager()
    dag = manager.get(request.dag_id)
    
    if dag is None:
        raise HTTPException(404, f"DAG not found: {request.dag_id}")
    
    engine = CausalEngine(dag)
    effect = engine.estimate_effect(request.treatment, request.outcome)
    
    return {
        "query_id": effect.query_id,
        "treatment": request.treatment,
        "outcome": request.outcome,
        "ate": effect.ate,
        "confidence_interval": effect.confidence_interval,
        "p_value": effect.p_value,
        "is_significant": effect.is_significant,
        "interpretation": effect.effect_size_interpretation,
        "summary": effect.summary,
        "estimator": effect.estimator,
        "synthetic": True,
    }


@router.post("/sensitivity/analyze")
async def analyze_sensitivity(
    request: SensitivityRequest,
    tenant_id: str = Depends(get_tenant_id),
):
    """Analyze variable sensitivity to outcome"""
    manager = get_dag_manager()
    dag = manager.get(request.dag_id)
    
    if dag is None:
        raise HTTPException(404, f"DAG not found: {request.dag_id}")
    
    engine = CausalEngine(dag)
    scores = engine.analyze_sensitivity(request.outcome)
    
    return {
        "outcome": request.outcome,
        "variables_analyzed": len(scores),
        "scores": [
            {
                "node_id": s.node_id,
                "node_name": s.node_name,
                "impact_score": s.impact_score,
                "volatility": s.volatility,
                "controllability": s.controllability,
                "risk_score": s.risk_score,
                "is_critical": s.is_critical,
                "alert_message": s.alert_message,
                "rank": s.rank,
            }
            for s in scores[:request.top_n]
        ],
        "synthetic": True,
    }


@router.post("/levers")
async def get_key_levers(
    request: SensitivityRequest,
    tenant_id: str = Depends(get_tenant_id),
):
    """Get most actionable levers for outcome"""
    manager = get_dag_manager()
    dag = manager.get(request.dag_id)
    
    if dag is None:
        raise HTTPException(404, f"DAG not found: {request.dag_id}")
    
    engine = CausalEngine(dag)
    levers = engine.get_key_levers(request.outcome, request.top_n)
    
    return {
        "outcome": request.outcome,
        "key_levers": [
            {
                "name": l.node_name,
                "impact": f"{l.impact_score:.0%}",
                "controllability": f"{l.controllability:.0%}",
                "recommendation": (
                    f"Focus on {l.node_name} - "
                    f"high impact ({l.impact_score:.0%}) and "
                    f"controllable ({l.controllability:.0%})"
                ),
            }
            for l in levers
        ],
        "synthetic": True,
    }


# ============================================================================
# COUNTERFACTUAL ENDPOINTS
# ============================================================================

@router.post("/counterfactual/what-if")
async def what_if_analysis(
    request: CounterfactualRequest,
    tenant_id: str = Depends(get_tenant_id),
):
    """What-if counterfactual analysis"""
    manager = get_dag_manager()
    dag = manager.get(request.dag_id)
    
    if dag is None:
        raise HTTPException(404, f"DAG not found: {request.dag_id}")
    
    cf_engine = CounterfactualEngine(dag)
    result = cf_engine.what_if(
        intervention_node=request.intervention_node,
        intervention_value=request.intervention_value,
        outcome_node=request.outcome_node,
        factual_value=request.factual_value,
    )
    
    return {
        "query_id": result.query_id,
        "factual_outcome": result.factual_outcome,
        "counterfactual_outcome": result.counterfactual_outcome,
        "effect": result.effect,
        "relative_effect": result.relative_effect,
        "confidence_interval": result.confidence_interval,
        "interpretation": result.interpretation,
        "summary": result.summary,
        "synthetic": True,
    }


@router.post("/counterfactual/compare-scenarios")
async def compare_scenarios(
    request: ScenarioCompareRequest,
    tenant_id: str = Depends(get_tenant_id),
):
    """Compare multiple intervention scenarios"""
    manager = get_dag_manager()
    dag = manager.get(request.dag_id)
    
    if dag is None:
        raise HTTPException(404, f"DAG not found: {request.dag_id}")
    
    comparator = ScenarioComparator(dag)
    result = comparator.compare_n_scenarios(
        scenarios=request.scenarios,
        outcome_node=request.outcome_node,
        scenario_names=request.scenario_names,
    )
    
    return result


# ============================================================================
# DECISION BRIDGE ENDPOINTS
# ============================================================================

# Store bridges per DAG (in-memory for demo)
_bridges: Dict[str, HumanDecisionBridge] = {}


def get_bridge(dag_id: str) -> HumanDecisionBridge:
    """Get or create decision bridge for DAG"""
    if dag_id not in _bridges:
        manager = get_dag_manager()
        dag = manager.get(dag_id)
        if dag is None:
            raise HTTPException(404, f"DAG not found: {dag_id}")
        
        engine = CausalEngine(dag)
        _bridges[dag_id] = HumanDecisionBridge(engine)
    
    return _bridges[dag_id]


@router.post("/decisions/package")
async def create_decision_package(
    request: CreateDecisionPackageRequest,
    tenant_id: str = Depends(get_tenant_id),
    user_id: str = Depends(get_user_id),
):
    """Create decision package for human review"""
    bridge = get_bridge(request.dag_id)
    
    package = bridge.create_decision_package(
        title=request.title,
        description=request.description,
        outcome_node=request.outcome_node,
        intervention_scenarios=request.intervention_scenarios,
        scenario_names=request.scenario_names,
        tenant_id=tenant_id,
        deadline=request.deadline,
    )
    
    return {
        "package_id": package.id,
        "title": package.title,
        "options_count": len(package.options),
        "recommended_option": package.recommended_option_id,
        "recommendation_rationale": package.recommendation_rationale,
        "requires_human_decision": True,
        "key_levers": [l.node_name for l in package.key_levers[:3]],
        "critical_alerts": package.critical_alerts,
        "created_at": package.created_at.isoformat(),
    }


@router.get("/decisions/package/{package_id}")
async def get_decision_package(
    package_id: str,
    dag_id: str,
    tenant_id: str = Depends(get_tenant_id),
    user_id: str = Depends(get_user_id),
):
    """Get decision package and mark as viewed"""
    bridge = get_bridge(dag_id)
    
    # Mark as viewed
    bridge.mark_viewed(package_id, user_id)
    
    package = bridge.get_package(package_id)
    if package is None:
        raise HTTPException(404, f"Package not found: {package_id}")
    
    return {
        "id": package.id,
        "title": package.title,
        "description": package.description,
        "options": [
            {
                "id": o.id,
                "name": o.name,
                "description": o.description,
                "expected_outcome": o.expected_outcome,
                "risk_level": o.risk_level,
                "benefits": o.benefits,
                "risks": o.risks,
            }
            for o in package.options
        ],
        "key_levers": [
            {
                "name": l.node_name,
                "impact": f"{l.impact_score:.0%}",
            }
            for l in package.key_levers
        ],
        "risk_factors": [
            {
                "name": r.node_name,
                "risk": f"{r.risk_score:.0%}",
                "alert": r.alert_message,
            }
            for r in package.risk_factors
        ],
        "critical_alerts": package.critical_alerts,
        "recommended_option_id": package.recommended_option_id,
        "recommendation_rationale": package.recommendation_rationale,
        "requires_human_decision": True,
        "deadline": package.deadline.isoformat() if package.deadline else None,
    }


@router.post("/decisions/record")
async def record_decision(
    request: RecordDecisionRequest,
    dag_id: str,
    tenant_id: str = Depends(get_tenant_id),
    user_id: str = Depends(get_user_id),
):
    """Record human decision (CRITICAL GOVERNANCE FUNCTION)"""
    bridge = get_bridge(dag_id)
    
    try:
        record = bridge.record_decision(
            package_id=request.package_id,
            decider_id=user_id,
            selected_option_id=request.selected_option_id,
            rationale=request.rationale,
            decider_name=request.decider_name,
            decider_role=request.decider_role,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))
    
    return {
        "record_id": record.id,
        "status": "DECIDED",
        "selected_option": record.selected_option,
        "rationale": record.decision_rationale,
        "decider_id": record.decider_id,
        "decided_at": record.decided_at.isoformat(),
        "signature": record.signature,
        "signature_valid": record.verify(),
        "human_decided": True,
        "ai_decided": False,  # ALWAYS FALSE
    }


@router.get("/decisions/record/{record_id}")
async def get_decision_record(
    record_id: str,
    dag_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    """Get decision record"""
    bridge = get_bridge(dag_id)
    
    record = bridge.get_record(record_id)
    if record is None:
        raise HTTPException(404, f"Record not found: {record_id}")
    
    return {
        "id": record.id,
        "package_id": record.recommendation_id,
        "status": record.status.value,
        "selected_option": record.selected_option,
        "rationale": record.decision_rationale,
        "decider_id": record.decider_id,
        "decided_at": record.decided_at.isoformat() if record.decided_at else None,
        "signature_valid": record.verify(),
    }


@router.get("/decisions/record/{record_id}/report")
async def get_decision_report(
    record_id: str,
    dag_id: str,
    tenant_id: str = Depends(get_tenant_id),
):
    """Generate signed decision report"""
    bridge = get_bridge(dag_id)
    
    try:
        report = bridge.generate_decision_report(record_id)
    except ValueError as e:
        raise HTTPException(404, str(e))
    
    return report


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "causal_engine",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }
