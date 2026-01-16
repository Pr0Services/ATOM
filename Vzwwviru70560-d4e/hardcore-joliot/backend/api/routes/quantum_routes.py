"""
CHE·NU™ — Quantum Orchestrator API Routes
=========================================
Exposes quantum orchestration:
- Compute routing (classical/photonic/quantum)
- Hub integration operations
- Capability queries
- Statistics

Note: User never directly requests quantum.
System uses it invisibly when necessary.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

from ..core.quantum import (
    QuantumOrchestrator,
    ComputeType,
    ComputePriority,
    HubIntegration,
    ComputeRequest,
    get_quantum_orchestrator
)

router = APIRouter(prefix="/api/v2/quantum", tags=["Quantum Orchestrator"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ComputeRequestModel(BaseModel):
    operation: str
    priority: str = "production"
    hub_target: Optional[str] = None
    payload: Dict[str, Any] = {}
    requires_encryption: bool = False
    requires_low_latency: bool = False
    requires_high_throughput: bool = False
    max_error_rate: float = 0.01
    max_cost: float = 1.0
    timeout_ms: int = 5000
    user_id: str = ""


class HubOperationRequest(BaseModel):
    hub: str
    operation: str
    payload: Dict[str, Any] = {}


class BackendConfigRequest(BaseModel):
    compute_type: str
    available: bool


# =============================================================================
# COMPUTE ENDPOINTS
# =============================================================================

@router.post("/compute")
async def execute_compute(request: ComputeRequestModel) -> Dict[str, Any]:
    """
    Execute computation with automatic routing.
    
    The system automatically selects optimal compute type:
    - Security priority → quantum/QKD preferred
    - Survival priority → fastest available (photonic)
    - Production → cost-optimized (classical)
    
    Always falls back to classical if advanced unavailable.
    """
    try:
        priority = ComputePriority(request.priority)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid priority: {request.priority}. Valid: {[p.value for p in ComputePriority]}"
        )
    
    hub_target = None
    if request.hub_target:
        try:
            hub_target = HubIntegration(request.hub_target)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid hub: {request.hub_target}. Valid: {[h.value for h in HubIntegration]}"
            )
    
    compute_request = ComputeRequest(
        operation=request.operation,
        priority=priority,
        hub_target=hub_target,
        payload=request.payload,
        requires_encryption=request.requires_encryption,
        requires_low_latency=request.requires_low_latency,
        requires_high_throughput=request.requires_high_throughput,
        max_error_rate=request.max_error_rate,
        max_cost=request.max_cost,
        timeout_ms=request.timeout_ms,
        user_id=request.user_id
    )
    
    orchestrator = get_quantum_orchestrator()
    result = await orchestrator.execute(compute_request)
    
    return {
        "status": result.status,
        "result": result.to_dict()
    }


@router.post("/compute/route")
async def route_compute(request: ComputeRequestModel) -> Dict[str, Any]:
    """
    Get routing decision without executing.
    
    Returns which compute type would be selected and why.
    """
    try:
        priority = ComputePriority(request.priority)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid priority: {request.priority}"
        )
    
    compute_request = ComputeRequest(
        operation=request.operation,
        priority=priority,
        payload=request.payload,
        requires_encryption=request.requires_encryption,
        requires_low_latency=request.requires_low_latency,
        requires_high_throughput=request.requires_high_throughput,
        user_id=request.user_id
    )
    
    orchestrator = get_quantum_orchestrator()
    decision = orchestrator.route(compute_request)
    
    return {
        "status": "routed",
        "decision": decision.to_dict()
    }


# =============================================================================
# HUB INTEGRATION ENDPOINTS
# =============================================================================

@router.post("/hub/operation")
async def hub_operation(request: HubOperationRequest) -> Dict[str, Any]:
    """
    Execute hub-specific operation.
    
    Communication Hub operations:
    - encrypt: Get QKD encryption key
    - rotate_key: Force key rotation
    
    Navigation Hub operations:
    - sync_sensors: Synchronize photonic sensors
    
    Execution Hub operations:
    - Any compute operation with high_throughput flag
    """
    try:
        hub = HubIntegration(request.hub)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid hub: {request.hub}. Valid: {[h.value for h in HubIntegration]}"
        )
    
    orchestrator = get_quantum_orchestrator()
    result = await orchestrator.execute_hub_operation(
        hub,
        request.operation,
        request.payload
    )
    
    return {
        "status": "completed",
        "hub": request.hub,
        "operation": request.operation,
        "result": result
    }


@router.post("/hub/sync")
async def sync_hubs() -> Dict[str, Any]:
    """Synchronize state across all hubs"""
    orchestrator = get_quantum_orchestrator()
    result = await orchestrator.sync_hub_states()
    
    return {
        "status": "synced",
        "result": result
    }


# =============================================================================
# CAPABILITY ENDPOINTS
# =============================================================================

@router.get("/capabilities")
async def get_capabilities() -> Dict[str, Any]:
    """Get all compute backend capabilities"""
    orchestrator = get_quantum_orchestrator()
    return {
        "status": "ok",
        "capabilities": orchestrator.get_capabilities()
    }


@router.get("/capabilities/{compute_type}")
async def get_capability(compute_type: str) -> Dict[str, Any]:
    """Get capability for specific compute type"""
    try:
        ct = ComputeType(compute_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid compute type: {compute_type}. Valid: {[c.value for c in ComputeType]}"
        )
    
    orchestrator = get_quantum_orchestrator()
    caps = orchestrator.get_capabilities()
    
    if compute_type not in caps:
        raise HTTPException(status_code=404, detail=f"No capability data for: {compute_type}")
    
    return {
        "compute_type": compute_type,
        "capability": caps[compute_type]
    }


# =============================================================================
# CONFIGURATION ENDPOINTS
# =============================================================================

@router.post("/config/backend")
async def configure_backend(request: BackendConfigRequest) -> Dict[str, Any]:
    """
    Configure backend availability.
    
    For testing/configuration purposes.
    In production, availability is determined automatically.
    """
    try:
        ct = ComputeType(request.compute_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid compute type: {request.compute_type}"
        )
    
    orchestrator = get_quantum_orchestrator()
    orchestrator.set_backend_availability(ct, request.available)
    
    return {
        "status": "configured",
        "compute_type": request.compute_type,
        "available": request.available
    }


# =============================================================================
# STATISTICS ENDPOINTS
# =============================================================================

@router.get("/stats")
async def get_stats() -> Dict[str, Any]:
    """Get orchestrator statistics"""
    orchestrator = get_quantum_orchestrator()
    return {
        "status": "ok",
        "stats": orchestrator.get_stats()
    }


# =============================================================================
# HEALTH & INFO
# =============================================================================

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check for quantum orchestrator"""
    orchestrator = get_quantum_orchestrator()
    caps = orchestrator.get_capabilities()
    
    available_backends = [
        ct for ct, cap in caps.items()
        if cap.get("is_available", False)
    ]
    
    return {
        "status": "healthy",
        "available_backends": available_backends,
        "total_backends": len(caps),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/info")
async def get_module_info() -> Dict[str, Any]:
    """Get quantum orchestrator module information"""
    return {
        "module": "quantum_orchestrator",
        "version": "1.0.0",
        "description": "CHE·NU Quantum Orchestrator - Intelligent Compute Routing",
        "principle": "User never asks for quantum. System uses it only when necessary.",
        "compute_types": [ct.value for ct in ComputeType],
        "priorities": [
            {"value": p.value, "description": _priority_description(p)}
            for p in ComputePriority
        ],
        "hubs": [
            {"value": h.value, "description": _hub_description(h)}
            for h in HubIntegration
        ],
        "features": [
            "Automatic compute selection",
            "Fallback to classical",
            "QKD key management",
            "Photonic sensor sync",
            "Multi-hub state sync"
        ]
    }


def _priority_description(p: ComputePriority) -> str:
    descriptions = {
        ComputePriority.SECURITY: "Highest - cryptographic operations, prefer quantum",
        ComputePriority.SURVIVAL: "Emergency/safety critical, prefer fastest",
        ComputePriority.PRODUCTION: "Normal business, cost-optimized",
        ComputePriority.BACKGROUND: "Low priority batch jobs"
    }
    return descriptions.get(p, "")


def _hub_description(h: HubIntegration) -> str:
    descriptions = {
        HubIntegration.COMMUNICATION: "QKD encryption for secure channels",
        HubIntegration.NAVIGATION: "Photonic sensor synchronization",
        HubIntegration.EXECUTION: "Compute acceleration"
    }
    return descriptions.get(h, "")
