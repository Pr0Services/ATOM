"""
CHE·NU™ — Multi-Tech Integration API Routes
==========================================
Exposes technology integration:
- Technology registry queries
- Phase management
- Hub technology configurations
- Decision rules
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

from ..core.multitech import (
    MultiTechIntegration,
    TechnologyRegistry,
    Technology,
    TechnologyCategory,
    ArchitectureLevel,
    IntegrationPhase,
    get_multi_tech_integration
)

router = APIRouter(prefix="/api/v2/multitech", tags=["Multi-Tech Integration"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class TechnologyRequest(BaseModel):
    tech_id: str
    context: Dict[str, Any] = {}


class RegisterTechRequest(BaseModel):
    tech_id: str
    name: str
    category: str
    level: int
    phase: str
    is_available: bool = False
    is_production_ready: bool = False
    requires: List[str] = []
    fallback_to: Optional[str] = None


# =============================================================================
# TECHNOLOGY REGISTRY ENDPOINTS
# =============================================================================

@router.get("/technologies")
async def get_all_technologies() -> Dict[str, Any]:
    """Get all registered technologies"""
    integration = get_multi_tech_integration()
    registry = integration.registry
    
    techs = list(registry._technologies.values())
    
    return {
        "total": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


@router.get("/technologies/{tech_id}")
async def get_technology(tech_id: str) -> Dict[str, Any]:
    """Get specific technology by ID"""
    integration = get_multi_tech_integration()
    tech = integration.registry.get(tech_id)
    
    if not tech:
        raise HTTPException(status_code=404, detail=f"Technology not found: {tech_id}")
    
    return {
        "status": "found",
        "technology": tech.to_dict()
    }


@router.get("/technologies/level/{level}")
async def get_technologies_by_level(level: int) -> Dict[str, Any]:
    """Get technologies by architecture level"""
    try:
        arch_level = ArchitectureLevel(level)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid level: {level}. Valid: 0-4"
        )
    
    integration = get_multi_tech_integration()
    techs = integration.registry.get_by_level(arch_level)
    
    return {
        "level": level,
        "level_name": arch_level.name,
        "count": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


@router.get("/technologies/category/{category}")
async def get_technologies_by_category(category: str) -> Dict[str, Any]:
    """Get technologies by category"""
    try:
        cat = TechnologyCategory(category)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category: {category}. Valid: {[c.value for c in TechnologyCategory]}"
        )
    
    integration = get_multi_tech_integration()
    techs = integration.registry.get_by_category(cat)
    
    return {
        "category": category,
        "count": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


@router.get("/technologies/phase/{phase}")
async def get_technologies_by_phase(phase: str) -> Dict[str, Any]:
    """Get technologies by integration phase"""
    try:
        p = IntegrationPhase(phase)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid phase: {phase}. Valid: {[p.value for p in IntegrationPhase]}"
        )
    
    integration = get_multi_tech_integration()
    techs = integration.registry.get_by_phase(p)
    
    return {
        "phase": phase,
        "count": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


@router.get("/technologies/available")
async def get_available_technologies() -> Dict[str, Any]:
    """Get all currently available technologies"""
    integration = get_multi_tech_integration()
    techs = integration.registry.get_available()
    
    return {
        "count": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


@router.get("/technologies/production-ready")
async def get_production_ready_technologies() -> Dict[str, Any]:
    """Get all production-ready technologies"""
    integration = get_multi_tech_integration()
    techs = integration.registry.get_production_ready()
    
    return {
        "count": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


# =============================================================================
# SELECTION & ROUTING ENDPOINTS
# =============================================================================

@router.post("/select")
async def select_technology(request: TechnologyRequest) -> Dict[str, Any]:
    """
    Select technology with rule application.
    
    Applies decision rules:
    1. Always fallback non-quantum
    2. Modularity required
    3. Zero vendor lock-in
    4. User transparency
    5. Social impact measurement
    """
    integration = get_multi_tech_integration()
    
    # Check if technology exists
    tech = integration.registry.get(request.tech_id)
    if not tech:
        raise HTTPException(status_code=404, detail=f"Technology not found: {request.tech_id}")
    
    # Select with rules
    selected = integration.select_technology(request.tech_id, request.context)
    selected_tech = integration.registry.get(selected)
    
    return {
        "requested": request.tech_id,
        "selected": selected,
        "selected_technology": selected_tech.to_dict() if selected_tech else None,
        "fallback_applied": selected != request.tech_id
    }


@router.get("/dependencies/{tech_id}")
async def check_dependencies(tech_id: str) -> Dict[str, Any]:
    """Check if technology dependencies are met"""
    integration = get_multi_tech_integration()
    
    tech = integration.registry.get(tech_id)
    if not tech:
        raise HTTPException(status_code=404, detail=f"Technology not found: {tech_id}")
    
    deps_met, missing = integration.registry.check_dependencies(tech_id)
    
    return {
        "tech_id": tech_id,
        "dependencies": tech.requires,
        "dependencies_met": deps_met,
        "missing": missing
    }


@router.get("/fallback/{tech_id}")
async def resolve_fallback(tech_id: str) -> Dict[str, Any]:
    """Resolve technology to available via fallback chain"""
    integration = get_multi_tech_integration()
    
    tech = integration.registry.get(tech_id)
    if not tech:
        raise HTTPException(status_code=404, detail=f"Technology not found: {tech_id}")
    
    resolved = integration.registry.resolve_fallback(tech_id)
    resolved_tech = integration.registry.get(resolved)
    
    # Build fallback chain
    chain = [tech_id]
    current = tech
    while current.fallback_to and current.fallback_to != resolved:
        chain.append(current.fallback_to)
        current = integration.registry.get(current.fallback_to)
        if not current:
            break
    if tech_id != resolved:
        chain.append(resolved)
    
    return {
        "requested": tech_id,
        "resolved": resolved,
        "resolved_technology": resolved_tech.to_dict() if resolved_tech else None,
        "fallback_chain": chain
    }


# =============================================================================
# HUB CONFIGURATION ENDPOINTS
# =============================================================================

@router.get("/hubs")
async def get_hub_configs() -> Dict[str, Any]:
    """Get all hub technology configurations"""
    integration = get_multi_tech_integration()
    
    return {
        "hubs": {
            name: config.to_dict()
            for name, config in integration._hub_configs.items()
        }
    }


@router.get("/hubs/{hub_name}")
async def get_hub_config(hub_name: str) -> Dict[str, Any]:
    """Get technology configuration for specific hub"""
    integration = get_multi_tech_integration()
    
    config = integration._hub_configs.get(hub_name.lower())
    if not config:
        raise HTTPException(
            status_code=404,
            detail=f"Hub not found: {hub_name}. Valid: communication, navigation, execution"
        )
    
    return {
        "hub": hub_name,
        "config": config.to_dict()
    }


@router.get("/hubs/{hub_name}/technologies")
async def get_hub_technologies(hub_name: str) -> Dict[str, Any]:
    """Get resolved technologies for a hub"""
    integration = get_multi_tech_integration()
    
    techs = integration.get_hub_technologies(hub_name)
    if not techs:
        raise HTTPException(
            status_code=404,
            detail=f"Hub not found or no technologies: {hub_name}"
        )
    
    return {
        "hub": hub_name,
        "count": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


# =============================================================================
# PHASE MANAGEMENT ENDPOINTS
# =============================================================================

@router.get("/phase")
async def get_current_phase() -> Dict[str, Any]:
    """Get current integration phase"""
    integration = get_multi_tech_integration()
    
    return {
        "current_phase": integration.current_phase.value,
        "available_phases": [p.value for p in IntegrationPhase],
        "phase_description": _phase_description(integration.current_phase)
    }


@router.get("/phase/technologies")
async def get_phase_technologies() -> Dict[str, Any]:
    """Get technologies available in current phase"""
    integration = get_multi_tech_integration()
    techs = integration.get_phase_technologies()
    
    return {
        "phase": integration.current_phase.value,
        "count": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


@router.post("/phase/advance")
async def advance_phase() -> Dict[str, Any]:
    """Advance to next integration phase"""
    integration = get_multi_tech_integration()
    
    old_phase = integration.current_phase
    new_phase = integration.advance_phase()
    
    return {
        "status": "advanced" if old_phase != new_phase else "at_final_phase",
        "previous_phase": old_phase.value,
        "current_phase": new_phase.value,
        "description": _phase_description(new_phase)
    }


# =============================================================================
# STATUS & STATISTICS ENDPOINTS
# =============================================================================

@router.get("/status")
async def get_integration_status() -> Dict[str, Any]:
    """Get overall integration status"""
    integration = get_multi_tech_integration()
    return {
        "status": "ok",
        "integration": integration.get_integration_status()
    }


@router.get("/success-indicators")
async def get_success_indicators() -> Dict[str, Any]:
    """Get success indicators for integration"""
    integration = get_multi_tech_integration()
    return {
        "status": "ok",
        "indicators": integration.get_success_indicators()
    }


# =============================================================================
# ARCHITECTURE ENDPOINTS
# =============================================================================

@router.get("/architecture")
async def get_architecture_overview() -> Dict[str, Any]:
    """Get architecture level overview"""
    integration = get_multi_tech_integration()
    
    levels = []
    for level in ArchitectureLevel:
        techs = integration.registry.get_by_level(level)
        available = [t for t in techs if t.is_available]
        
        levels.append({
            "level": level.value,
            "name": level.name,
            "description": _level_description(level),
            "total_technologies": len(techs),
            "available": len(available)
        })
    
    return {
        "levels": levels
    }


# =============================================================================
# HEALTH & INFO
# =============================================================================

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check for multi-tech module"""
    integration = get_multi_tech_integration()
    status = integration.get_integration_status()
    
    return {
        "status": "healthy",
        "current_phase": status["current_phase"],
        "technologies": {
            "total": status["total_technologies"],
            "available": status["available"],
            "production_ready": status["production_ready"]
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/info")
async def get_module_info() -> Dict[str, Any]:
    """Get multi-tech module information"""
    return {
        "module": "multi_tech_integration",
        "version": "1.0.0",
        "description": "CHE·NU Multi-Tech Integration - Technology Stack Abstraction",
        "architecture_levels": [
            {"level": l.value, "name": l.name, "description": _level_description(l)}
            for l in ArchitectureLevel
        ],
        "integration_phases": [
            {"value": p.value, "description": _phase_description(p)}
            for p in IntegrationPhase
        ],
        "categories": [c.value for c in TechnologyCategory],
        "decision_rules": [
            "1. Always fallback non-quantum",
            "2. Modularity required",
            "3. Zero vendor lock-in",
            "4. User transparency",
            "5. Social impact measurement"
        ]
    }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _level_description(level: ArchitectureLevel) -> str:
    descriptions = {
        ArchitectureLevel.LEVEL_0_PHYSICAL: "Physical/Network - Fiber, QKD, PQC, Sensors",
        ArchitectureLevel.LEVEL_1_KERNEL: "NOVA Kernel - OPA, Orchestrator, Security",
        ArchitectureLevel.LEVEL_2_HUBS: "Hubs - Communication, Navigation, Execution",
        ArchitectureLevel.LEVEL_3_AGENTS: "Agents - Permanent, Service (on-demand)",
        ArchitectureLevel.LEVEL_4_INTERFACES: "Interfaces - UI, XR, API"
    }
    return descriptions.get(level, "")


def _phase_description(phase: IntegrationPhase) -> str:
    descriptions = {
        IntegrationPhase.PHASE_1_COMPATIBILITY: "Compatibility (0-6 months) - Standard cloud/crypto",
        IntegrationPhase.PHASE_2_HYBRIDATION: "Hybridation (6-18 months) - QKD, TEEs, XR",
        IntegrationPhase.PHASE_3_QUANTUM: "Photonic/Quantum (18-36 months) - Full quantum integration"
    }
    return descriptions.get(phase, "")
