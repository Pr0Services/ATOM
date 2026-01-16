"""
CHE·NU™ — Synaptic API Routes
=============================
Exposes the synaptic infrastructure:
- Context creation and management
- 3-hub switching
- Graph queries
- Yellow pages lookups
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

from ..core.synaptic import (
    SynapticContext,
    ScopeType,
    HubType,
    GuardType,
    LocationAnchor,
    ToolchainConfig,
    CommunicationChannel,
    PolicyGuard,
    ContextCapsuleBuilder,
    get_synaptic_switcher,
    synaptic_switch,
    SwitchResult,
    get_synaptic_graph,
    ModuleID,
    Priority,
    get_yellow_pages,
    NeedTag
)

router = APIRouter(prefix="/api/v2/synaptic", tags=["Synaptic"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class LocationAnchorRequest(BaseModel):
    anchor_id: str
    sphere_id: str
    coordinates: Optional[Dict[str, float]] = None
    zone_type: str = "default"


class ToolchainRequest(BaseModel):
    tool_ids: List[str] = []
    agent_ids: List[str] = []
    sandbox_mode: bool = True
    max_compute_tokens: int = 10000


class ChannelRequest(BaseModel):
    channel_id: str
    member_ids: List[str] = []
    channel_type: str = "task"
    encryption_level: str = "standard"


class GuardRequest(BaseModel):
    guard_type: str
    policy_id: str
    parameters: Dict[str, Any] = {}
    required: bool = True


class CreateContextRequest(BaseModel):
    task_id: str
    sphere_id: str
    user_id: str
    location: Optional[LocationAnchorRequest] = None
    tools: Optional[ToolchainRequest] = None
    channel: Optional[ChannelRequest] = None
    scope: str = "private"
    guards: List[GuardRequest] = []
    ttl_seconds: int = 300
    trigger_source: str = ""


class SwitchRequest(BaseModel):
    context_id: str
    user_id: str


class RouteRequest(BaseModel):
    need_tag: str
    payload: Dict[str, Any] = {}


class FireEdgeRequest(BaseModel):
    source_module: str
    trigger_name: str
    payload: Dict[str, Any] = {}


# =============================================================================
# CONTEXT ENDPOINTS
# =============================================================================

@router.post("/context/create")
async def create_context(request: CreateContextRequest) -> Dict[str, Any]:
    """Create a new synaptic context"""
    try:
        builder = ContextCapsuleBuilder()
        builder.with_task(request.task_id, request.sphere_id)
        builder.with_user(request.user_id)
        
        if request.location:
            builder.with_location(
                request.location.anchor_id,
                request.location.coordinates
            )
        
        if request.tools:
            builder.with_tools(
                request.tools.tool_ids,
                request.tools.agent_ids
            )
        
        if request.channel:
            builder.with_channel(
                request.channel.channel_id,
                request.channel.member_ids
            )
        
        builder.with_scope(ScopeType(request.scope))
        builder.with_ttl(request.ttl_seconds)
        
        if request.trigger_source:
            builder.triggered_by(request.trigger_source)
        
        for guard in request.guards:
            builder.with_guard(
                GuardType(guard.guard_type),
                guard.policy_id,
                **guard.parameters
            )
        
        context = builder.build()
        
        return {
            "status": "created",
            "context": context.to_dict()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/context/{context_id}")
async def get_context(context_id: str) -> Dict[str, Any]:
    """Get context by ID (from current switcher state)"""
    switcher = get_synaptic_switcher()
    
    if switcher.current_context and str(switcher.current_context.context_id) == context_id:
        return {
            "status": "found",
            "context": switcher.current_context.to_dict()
        }
    
    raise HTTPException(status_code=404, detail="Context not found or not active")


# =============================================================================
# SWITCHER ENDPOINTS
# =============================================================================

@router.post("/switch")
async def switch_context(request: CreateContextRequest) -> Dict[str, Any]:
    """Create and switch to a new context atomically"""
    try:
        # Build context
        builder = ContextCapsuleBuilder()
        builder.with_task(request.task_id, request.sphere_id)
        builder.with_user(request.user_id)
        
        if request.location:
            builder.with_location(
                request.location.anchor_id,
                request.location.coordinates
            )
        
        if request.tools:
            builder.with_tools(
                request.tools.tool_ids,
                request.tools.agent_ids
            )
        
        if request.channel:
            builder.with_channel(
                request.channel.channel_id,
                request.channel.member_ids
            )
        
        builder.with_scope(ScopeType(request.scope))
        builder.with_ttl(request.ttl_seconds)
        
        context = builder.build()
        
        # Perform switch
        report = await synaptic_switch(context, request.user_id)
        
        # Check result
        if report.result == SwitchResult.BLOCKED:
            raise HTTPException(
                status_code=423,
                detail={
                    "message": "Switch blocked by guards",
                    "reason": report.blocked_reason,
                    "report": report.to_dict()
                }
            )
        
        if report.result == SwitchResult.ERROR:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Switch failed",
                    "reason": report.blocked_reason,
                    "report": report.to_dict()
                }
            )
        
        return {
            "status": "switched",
            "result": report.result.value,
            "report": report.to_dict(),
            "context": context.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/switch/status")
async def get_switcher_status() -> Dict[str, Any]:
    """Get current switcher status"""
    switcher = get_synaptic_switcher()
    return await switcher.get_status()


@router.get("/switch/dashboard")
async def get_dashboard() -> Dict[str, Any]:
    """Get dashboard render data for current context"""
    switcher = get_synaptic_switcher()
    
    if not switcher.current_context:
        return {
            "status": "no_context",
            "dashboard": None
        }
    
    dashboard = await switcher.render_dashboard(switcher.current_context)
    return {
        "status": "active",
        "dashboard": dashboard
    }


# =============================================================================
# GRAPH ENDPOINTS
# =============================================================================

@router.get("/graph/summary")
async def get_graph_summary() -> Dict[str, Any]:
    """Get synaptic graph summary"""
    graph = get_synaptic_graph()
    return graph.get_graph_summary()


@router.get("/graph/edges")
async def get_all_edges() -> Dict[str, Any]:
    """Get all edges in the graph"""
    graph = get_synaptic_graph()
    return {
        "total": len(graph._edges),
        "edges": graph.export_edge_list()
    }


@router.get("/graph/edges/{module_id}")
async def get_module_edges(module_id: str) -> Dict[str, Any]:
    """Get edges for a specific module"""
    try:
        module = ModuleID(module_id)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown module: {module_id}")
    
    graph = get_synaptic_graph()
    
    return {
        "module": module_id,
        "outgoing": [e.to_dict() for e in graph.get_outgoing_edges(module)],
        "incoming": [e.to_dict() for e in graph.get_incoming_edges(module)]
    }


@router.get("/graph/priority/{priority}")
async def get_edges_by_priority(priority: str) -> Dict[str, Any]:
    """Get edges by priority level"""
    try:
        p = Priority(priority)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown priority: {priority}")
    
    graph = get_synaptic_graph()
    edges = graph.get_edges_by_priority(p)
    
    return {
        "priority": priority,
        "count": len(edges),
        "edges": [e.to_dict() for e in edges]
    }


@router.post("/graph/fire")
async def fire_graph_edge(request: FireEdgeRequest) -> Dict[str, Any]:
    """Fire an edge trigger"""
    try:
        source = ModuleID(request.source_module)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown module: {request.source_module}")
    
    graph = get_synaptic_graph()
    results = await graph.fire_trigger(source, request.trigger_name, request.payload)
    
    return {
        "status": "fired",
        "source": request.source_module,
        "trigger": request.trigger_name,
        "results_count": len(results)
    }


@router.get("/graph/mermaid")
async def get_mermaid_diagram() -> Dict[str, Any]:
    """Get graph as Mermaid diagram"""
    graph = get_synaptic_graph()
    return {
        "format": "mermaid",
        "diagram": graph.export_mermaid()
    }


# =============================================================================
# YELLOW PAGES ENDPOINTS
# =============================================================================

@router.get("/yellowpages/entries")
async def get_all_entries() -> Dict[str, Any]:
    """Get all yellow pages entries"""
    yp = get_yellow_pages()
    return {
        "total": len(yp._entries),
        "entries": [e.to_dict() for e in yp.get_all_entries()]
    }


@router.get("/yellowpages/lookup/{need_tag}")
async def lookup_need(need_tag: str) -> Dict[str, Any]:
    """Lookup entry by need tag"""
    try:
        tag = NeedTag(need_tag)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown need tag: {need_tag}")
    
    yp = get_yellow_pages()
    entry = yp.lookup(tag)
    
    if not entry:
        raise HTTPException(status_code=404, detail=f"No entry for: {need_tag}")
    
    return {
        "status": "found",
        "entry": entry.to_dict()
    }


@router.post("/yellowpages/route")
async def route_need(request: RouteRequest) -> Dict[str, Any]:
    """Route a need to module/service"""
    try:
        tag = NeedTag(request.need_tag)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown need tag: {request.need_tag}")
    
    yp = get_yellow_pages()
    decision = yp.route(tag)
    
    return {
        "status": "routed",
        "decision": decision.to_dict()
    }


@router.post("/yellowpages/execute")
async def execute_need(request: RouteRequest) -> Dict[str, Any]:
    """Route and execute a need"""
    try:
        tag = NeedTag(request.need_tag)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown need tag: {request.need_tag}")
    
    yp = get_yellow_pages()
    result = await yp.execute(tag, request.payload)
    
    return result


@router.get("/yellowpages/stats")
async def get_yellowpages_stats() -> Dict[str, Any]:
    """Get yellow pages statistics"""
    yp = get_yellow_pages()
    return yp.get_stats()


@router.get("/yellowpages/table")
async def get_yellowpages_table() -> Dict[str, Any]:
    """Get yellow pages as table for documentation"""
    yp = get_yellow_pages()
    return {
        "format": "table",
        "rows": yp.export_table()
    }


# =============================================================================
# HEALTH & INFO
# =============================================================================

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check for synaptic module"""
    switcher = get_synaptic_switcher()
    graph = get_synaptic_graph()
    yp = get_yellow_pages()
    
    return {
        "status": "healthy",
        "components": {
            "switcher": {
                "active": switcher.current_context is not None,
                "history_count": len(switcher._history)
            },
            "graph": {
                "edges": len(graph._edges),
                "modules": len(ModuleID)
            },
            "yellow_pages": {
                "entries": len(yp._entries),
                "handlers": len(yp._handlers)
            }
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/info")
async def get_module_info() -> Dict[str, Any]:
    """Get synaptic module information"""
    return {
        "module": "synaptic",
        "version": "1.0.0",
        "description": "CHE·NU Synaptic Infrastructure - 3-Hub Synchronization",
        "components": [
            "SynapticContext - Context capsule",
            "SynapticSwitcher - 3-hub atomic switching",
            "SynapticGraph - Inter-module connections",
            "YellowPages - Service registry"
        ],
        "hubs": [hub.value for hub in HubType],
        "modules": [mod.value for mod in ModuleID],
        "priorities": [p.value for p in Priority],
        "need_tags": [tag.value for tag in NeedTag]
    }
