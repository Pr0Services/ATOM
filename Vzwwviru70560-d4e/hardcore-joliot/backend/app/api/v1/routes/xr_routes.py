"""
ROUTES: xr_routes.py
PREFIX: /api/v2/threads/{thread_id}/xr
VERSION: 1.0.0

PURPOSE: API endpoints for XR Renderer, Thread Maturity, and UX Entry
- Thread Lobby (entry point)
- Maturity computation
- XR Blueprint generation
- XR interactions → Thread events

R&D COMPLIANCE:
- Rule #1: XR interactions create events, don't modify state directly
- Rule #3: XR is PROJECTION, Thread is truth
- Rule #6: Full traceability on all interactions
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime
import logging

# Import schemas
from app.schemas.xr_schemas import (
    XRBlueprint,
    BlueprintZone,
    BlueprintItem,
    MaturityResult,
    MaturityLevel,
    MaturitySignals,
    ThreadLobbyData,
    XRPreflightData,
    ThreadEntryMode,
    ViewerRole,
    RedactionLevel,
    ActionStatus,
    ActionUpdatePayload,
    ActionCreatePayload,
    MessagePostPayload,
    XRTemplate,
)

# Import services
from app.services.xr.maturity_service import MaturityService
from app.services.xr.xr_renderer_service import XRRendererService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2/threads", tags=["XR", "Maturity"])

# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_maturity_service() -> MaturityService:
    """Get maturity service instance."""
    return MaturityService()

def get_xr_renderer_service() -> XRRendererService:
    """Get XR renderer service instance."""
    return XRRendererService()

# ============================================================================
# THREAD LOBBY ENDPOINTS (UX Entry Point)
# ============================================================================

@router.get("/{thread_id}/lobby")
async def get_thread_lobby(
    thread_id: UUID,
    viewer_id: UUID = Query(..., description="ID of user viewing the thread"),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """
    Get Thread Lobby data - the main entry point for any thread.
    
    Returns:
    - Thread summary
    - Maturity level with badge
    - Available modes (Chat/Live/XR)
    - Recommendations
    - Quick actions
    
    This is the "front door" to every thread in CHE·NU.
    """
    try:
        # Mock thread state for demo - in production, fetch from thread_service
        thread_state = _get_mock_thread_state(thread_id)
        
        # Determine viewer role
        viewer_role = _determine_viewer_role(thread_state, viewer_id)
        
        lobby_data = await xr_service.get_thread_lobby(
            thread_id=thread_id,
            thread_state=thread_state,
            viewer_role=viewer_role
        )
        
        return {
            "lobby": lobby_data.dict(),
            "viewer_role": viewer_role.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Thread lobby error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{thread_id}/lobby/mode-recommendation")
async def get_mode_recommendation(
    thread_id: UUID,
    viewer_id: UUID = Query(...),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """
    Get recommended entry mode for thread based on maturity and context.
    
    Returns recommendation with reasoning.
    """
    try:
        thread_state = _get_mock_thread_state(thread_id)
        viewer_role = _determine_viewer_role(thread_state, viewer_id)
        
        lobby_data = await xr_service.get_thread_lobby(
            thread_id=thread_id,
            thread_state=thread_state,
            viewer_role=viewer_role
        )
        
        return {
            "recommended_mode": lobby_data.recommended_mode.value,
            "reasoning": _get_mode_reasoning(lobby_data),
            "available_modes": [m.value for m in lobby_data.available_modes],
            "maturity_level": lobby_data.maturity.level.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Mode recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# MATURITY ENDPOINTS
# ============================================================================

@router.get("/{thread_id}/maturity")
async def get_thread_maturity(
    thread_id: UUID,
    force_recompute: bool = Query(False, description="Force fresh computation"),
    maturity_service: MaturityService = Depends(get_maturity_service)
):
    """
    Get thread maturity level and score.
    
    Maturity is computed from 10 signals and determines:
    - Available zones in XR
    - Recommended entry mode
    - UI complexity level
    """
    try:
        # Mock signals - in production, count from event store
        signals = _get_mock_maturity_signals(thread_id)
        
        maturity = await maturity_service.compute_maturity(
            thread_id=thread_id,
            signals=signals,
            force_recompute=force_recompute
        )
        
        return {
            "maturity": maturity.dict(),
            "zones_available": maturity_service.get_zones_for_level(maturity.level),
            "features_available": maturity_service.get_features_for_level(maturity.level),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Maturity computation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{thread_id}/maturity/history")
async def get_maturity_history(
    thread_id: UUID,
    limit: int = Query(10, ge=1, le=100),
    maturity_service: MaturityService = Depends(get_maturity_service)
):
    """Get historical maturity scores for a thread."""
    try:
        # In production, fetch from maturity history table
        history = maturity_service.get_maturity_history(thread_id, limit)
        
        return {
            "thread_id": str(thread_id),
            "history": history,
            "count": len(history),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Maturity history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{thread_id}/maturity/signals")
async def get_maturity_signals(
    thread_id: UUID,
    maturity_service: MaturityService = Depends(get_maturity_service)
):
    """
    Get detailed breakdown of maturity signals.
    
    Shows contribution of each signal to overall score.
    """
    try:
        signals = _get_mock_maturity_signals(thread_id)
        
        breakdown = []
        signal_dict = signals.dict()
        for signal_name, value in signal_dict.items():
            contribution = maturity_service.scorer.compute_signal_contribution(
                signal_name, value
            )
            breakdown.append({
                "signal": signal_name,
                "value": value,
                "max_contribution": 10,
                "actual_contribution": contribution,
                "description": _get_signal_description(signal_name)
            })
        
        total = sum(b["actual_contribution"] for b in breakdown)
        
        return {
            "thread_id": str(thread_id),
            "signals": breakdown,
            "total_score": total,
            "level": maturity_service.scorer.score_to_level(total).value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Maturity signals error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# XR BLUEPRINT ENDPOINTS
# ============================================================================

@router.get("/{thread_id}/xr/preflight")
async def xr_preflight(
    thread_id: UUID,
    viewer_id: UUID = Query(...),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """
    XR preflight check before entering XR mode.
    
    Returns:
    - Available zones
    - Permissions
    - Privacy note
    - Device requirements
    """
    try:
        thread_state = _get_mock_thread_state(thread_id)
        viewer_role = _determine_viewer_role(thread_state, viewer_id)
        
        preflight = await xr_service.get_xr_preflight(
            thread_id=thread_id,
            thread_state=thread_state,
            viewer_role=viewer_role
        )
        
        return {
            "preflight": preflight.dict(),
            "ready": preflight.can_enter_xr,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"XR preflight error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{thread_id}/xr/blueprint")
async def get_xr_blueprint(
    thread_id: UUID,
    viewer_id: UUID = Query(...),
    template: Optional[XRTemplate] = Query(None, description="Override template"),
    redaction: Optional[RedactionLevel] = Query(None, description="Override redaction"),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """
    Generate XR Blueprint for thread.
    
    Blueprint is a PROJECTION of thread state - never canonical.
    Contains zones, items, interactions, and portals.
    """
    try:
        thread_state = _get_mock_thread_state(thread_id)
        viewer_role = _determine_viewer_role(thread_state, viewer_id)
        
        blueprint = await xr_service.generate_blueprint(
            thread_id=thread_id,
            thread_state=thread_state,
            viewer_role=viewer_role,
            template_override=template,
            redaction_override=redaction
        )
        
        return {
            "blueprint": blueprint.dict(),
            "viewer_role": viewer_role.value,
            "zones_count": len(blueprint.zones),
            "items_count": sum(len(z.items) for z in blueprint.zones),
            "portals_count": len(blueprint.portals),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"XR blueprint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{thread_id}/xr/zones")
async def list_xr_zones(
    thread_id: UUID,
    viewer_id: UUID = Query(...),
    xr_service: XRRendererService = Depends(get_xr_renderer_service),
    maturity_service: MaturityService = Depends(get_maturity_service)
):
    """List available XR zones for thread based on maturity."""
    try:
        signals = _get_mock_maturity_signals(thread_id)
        maturity = await maturity_service.compute_maturity(thread_id, signals)
        
        available_zones = maturity_service.get_zones_for_level(maturity.level)
        
        zones = []
        for zone_type in available_zones:
            zones.append({
                "type": zone_type,
                "name": _get_zone_name(zone_type),
                "description": _get_zone_description(zone_type),
                "available": True
            })
        
        return {
            "thread_id": str(thread_id),
            "maturity_level": maturity.level.value,
            "zones": zones,
            "count": len(zones),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"XR zones error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# XR INTERACTION → EVENT ENDPOINTS
# ============================================================================

@router.post("/{thread_id}/xr/actions/{action_id}/update")
async def xr_update_action(
    thread_id: UUID,
    action_id: UUID,
    payload: ActionUpdatePayload,
    user_id: UUID = Body(..., embed=True),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """
    XR interaction: Update action status.
    
    Creates ACTION_UPDATED event in thread.
    XR is projection only - this generates the canonical event.
    """
    try:
        event = await xr_service.create_action_update_event(
            thread_id=thread_id,
            action_id=action_id,
            new_status=payload.new_status,
            user_id=user_id,
            source="xr_interaction"
        )
        
        return {
            "status": "event_created",
            "event": event,
            "message": "Action status will update when event is processed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"XR action update error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{thread_id}/xr/actions/create")
async def xr_create_action(
    thread_id: UUID,
    payload: ActionCreatePayload,
    user_id: UUID = Body(..., embed=True),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """
    XR interaction: Create new action.
    
    Creates ACTION_CREATED event in thread.
    """
    try:
        event = await xr_service.create_action_create_event(
            thread_id=thread_id,
            title=payload.title,
            description=payload.description,
            due_date=payload.due_date,
            assignee_id=payload.assignee_id,
            user_id=user_id,
            source="xr_interaction"
        )
        
        return {
            "status": "event_created",
            "event": event,
            "message": "Action will appear when event is processed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"XR action create error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{thread_id}/xr/notes/create")
async def xr_create_note(
    thread_id: UUID,
    payload: MessagePostPayload,
    user_id: UUID = Body(..., embed=True),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """
    XR interaction: Add note to memory kiosk.
    
    Creates MESSAGE_POSTED event in thread.
    """
    try:
        event = await xr_service.create_message_event(
            thread_id=thread_id,
            content=payload.content,
            note_type=payload.note_type,
            user_id=user_id,
            source="xr_interaction"
        )
        
        return {
            "status": "event_created",
            "event": event,
            "message": "Note will appear in memory kiosk when processed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"XR note create error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PORTAL ENDPOINTS
# ============================================================================

@router.get("/{thread_id}/xr/portals")
async def list_portals(
    thread_id: UUID,
    viewer_id: UUID = Query(...),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """List portals (links to other threads) available from this thread."""
    try:
        thread_state = _get_mock_thread_state(thread_id)
        viewer_role = _determine_viewer_role(thread_state, viewer_id)
        
        blueprint = await xr_service.generate_blueprint(
            thread_id=thread_id,
            thread_state=thread_state,
            viewer_role=viewer_role
        )
        
        return {
            "thread_id": str(thread_id),
            "portals": [p.dict() for p in blueprint.portals],
            "count": len(blueprint.portals),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Portal list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{thread_id}/xr/portals/{target_thread_id}/traverse")
async def traverse_portal(
    thread_id: UUID,
    target_thread_id: UUID,
    user_id: UUID = Body(..., embed=True),
    xr_service: XRRendererService = Depends(get_xr_renderer_service)
):
    """
    Traverse a portal to another thread.
    
    Returns new thread lobby data for seamless transition.
    """
    try:
        # Log traversal event
        event = {
            "type": "PORTAL_TRAVERSED",
            "from_thread": str(thread_id),
            "to_thread": str(target_thread_id),
            "user_id": str(user_id),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Get target thread lobby
        target_state = _get_mock_thread_state(target_thread_id)
        viewer_role = _determine_viewer_role(target_state, user_id)
        
        target_lobby = await xr_service.get_thread_lobby(
            thread_id=target_thread_id,
            thread_state=target_state,
            viewer_role=viewer_role
        )
        
        return {
            "status": "traversed",
            "from_thread": str(thread_id),
            "to_thread": str(target_thread_id),
            "target_lobby": target_lobby.dict(),
            "event": event,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Portal traversal error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_mock_thread_state(thread_id: UUID) -> Dict[str, Any]:
    """Get mock thread state for demo. In production, fetch from thread_service."""
    return {
        "id": str(thread_id),
        "owner_id": "user-123",
        "founding_intent": "Plan Q1 product launch",
        "status": "active",
        "sphere_id": "business",
        "visibility": "private",
        "participants": ["user-123", "user-456"],
        "linked_threads": [
            {"id": "thread-linked-1", "title": "Marketing assets"},
            {"id": "thread-linked-2", "title": "Budget planning"}
        ],
        "is_live": False,
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": datetime.utcnow().isoformat(),
        "actions": [
            {"id": "action-1", "title": "Draft announcement", "status": "done"},
            {"id": "action-2", "title": "Review copy", "status": "in_progress"},
            {"id": "action-3", "title": "Publish", "status": "todo"}
        ],
        "decisions": [
            {"id": "dec-1", "summary": "Launch date: Feb 15"},
            {"id": "dec-2", "summary": "Budget: $50k"}
        ],
        "summaries": [
            {"id": "sum-1", "content": "Initial planning phase complete"}
        ],
        "notes": [
            {"id": "note-1", "content": "Remember to check competitor pricing"}
        ]
    }

def _get_mock_maturity_signals(thread_id: UUID) -> MaturitySignals:
    """Get mock maturity signals. In production, count from event store."""
    return MaturitySignals(
        summary_count=2,
        decision_count=3,
        action_count=5,
        participant_count=2,
        live_session_count=1,
        link_count=2,
        message_count=15,
        learning_item_count=0,
        age_days=14,
        portal_count=2
    )

def _determine_viewer_role(thread_state: Dict, viewer_id: UUID) -> ViewerRole:
    """Determine viewer's role in thread."""
    owner_id = thread_state.get("owner_id")
    participants = thread_state.get("participants", [])
    
    if str(viewer_id) == owner_id:
        return ViewerRole.OWNER
    elif str(viewer_id) in participants:
        return ViewerRole.PARTICIPANT
    else:
        return ViewerRole.VIEWER

def _get_mode_reasoning(lobby_data: ThreadLobbyData) -> str:
    """Get human-readable reasoning for mode recommendation."""
    level = lobby_data.maturity.level
    mode = lobby_data.recommended_mode
    
    reasons = {
        (MaturityLevel.SEED, ThreadEntryMode.CHAT): 
            "Thread is new. Chat mode helps capture initial ideas quickly.",
        (MaturityLevel.SPROUT, ThreadEntryMode.CHAT):
            "Thread is developing. Chat mode good for rapid iteration.",
        (MaturityLevel.WORKSHOP, ThreadEntryMode.LIVE):
            "Thread has structure. Live mode enables real-time collaboration.",
        (MaturityLevel.STUDIO, ThreadEntryMode.XR):
            "Thread is mature. XR provides spatial overview of all elements.",
        (MaturityLevel.ORG, ThreadEntryMode.XR):
            "Complex thread. XR navigation helps manage multiple areas.",
        (MaturityLevel.ECOSYSTEM, ThreadEntryMode.XR):
            "Large thread network. XR portal system enables navigation."
    }
    
    return reasons.get((level, mode), "Mode selected based on thread maturity and activity.")

def _get_signal_description(signal_name: str) -> str:
    """Get human-readable description for maturity signal."""
    descriptions = {
        "summary_count": "Number of summary snapshots created",
        "decision_count": "Decisions recorded in thread",
        "action_count": "Actions created and tracked",
        "participant_count": "Active participants in thread",
        "live_session_count": "Live collaboration sessions held",
        "link_count": "External resources linked",
        "message_count": "Messages and notes added",
        "learning_item_count": "Learning items extracted",
        "age_days": "Thread age in days",
        "portal_count": "Connections to other threads"
    }
    return descriptions.get(signal_name, signal_name)

def _get_zone_name(zone_type: str) -> str:
    """Get display name for zone type."""
    names = {
        "intent_wall": "Intent Wall",
        "decision_wall": "Decision Wall", 
        "action_table": "Action Table",
        "memory_kiosk": "Memory Kiosk",
        "timeline_strip": "Timeline",
        "resource_shelf": "Resource Shelf",
        "portal_area": "Portals"
    }
    return names.get(zone_type, zone_type)

def _get_zone_description(zone_type: str) -> str:
    """Get description for zone type."""
    descriptions = {
        "intent_wall": "Displays the founding intent and thread purpose",
        "decision_wall": "Shows all decisions made in the thread",
        "action_table": "Interactive table of tasks and actions",
        "memory_kiosk": "Access to notes, summaries, and thread memory",
        "timeline_strip": "Chronological view of thread events",
        "resource_shelf": "External links and attached resources",
        "portal_area": "Gateways to linked threads"
    }
    return descriptions.get(zone_type, "")
