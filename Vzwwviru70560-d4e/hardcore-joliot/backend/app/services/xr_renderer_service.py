"""
SERVICE: xr_renderer_service.py
SPHERE: CORE (cross-sphere)
VERSION: 1.0.0
INTENT: XR Renderer service - projection of Thread into XR room

DEPENDENCIES:
- Core: thread_service, maturity_service
- Schemas: xr_schemas

R&D COMPLIANCE: ✅
- Rule #3: Sphere Integrity - XR is PROJECTION only, no canonical state
- Rule #1: Human Sovereignty - Write interactions emit events with human gate
- Rule #6: Traceability - All interactions become thread events

HUMAN GATES:
- All write interactions must emit ThreadEvents (not modify state directly)
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import uuid4

from ..schemas.xr_schemas import (
    XRBlueprint,
    BlueprintZone,
    BlueprintItem,
    BlueprintItemAction,
    ThreadPortal,
    BlueprintReferences,
    ZoneType,
    ItemKind,
    XRTemplate,
    RedactionLevel,
    ViewerRole,
    ActionStatus,
    MaturityLevel,
    XRInteractionContext,
    ActionUpdatePayload,
    ActionCreatePayload,
    NoteAddPayload,
    ThreadLobbyData,
    XRPreflightData,
    ModeRecommendation,
    ThreadEntryMode,
    ThreadSummaryExcerpt,
    LiveSessionInfo,
    MaturityResult,
)
from .maturity_service import MaturityService

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# BLUEPRINT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class BlueprintGenerator:
    """
    Generates XR Blueprint from Thread state.
    
    Blueprint is derived from:
    - Thread events (founding_intent, decisions, actions, etc.)
    - Thread snapshots (summaries)
    - Maturity level (determines zones)
    """
    
    def __init__(self, maturity_service: MaturityService):
        self.maturity_service = maturity_service
    
    async def generate(
        self,
        thread_id: str,
        thread_state: Dict[str, Any],
        maturity: MaturityResult,
        viewer_role: ViewerRole = ViewerRole.VIEWER
    ) -> XRBlueprint:
        """
        Generate XR Blueprint from thread state.
        
        Args:
            thread_id: Thread ID
            thread_state: Current thread state (from snapshots/events)
            maturity: Computed maturity
            viewer_role: Role of the viewer
            
        Returns:
            XRBlueprint ready for rendering
        """
        # Select template based on thread type
        template = self._select_template(thread_state)
        
        # Get zones for maturity level
        zone_types = self.maturity_service.get_zones_for_maturity(maturity.level)
        
        # Build zones
        zones = []
        
        # Intent Wall (always present)
        if ZoneType.WALL in zone_types:
            zones.append(self._build_intent_zone(thread_state, viewer_role))
            zones.append(self._build_decision_zone(thread_state, viewer_role))
        
        # Action Table
        if ZoneType.TABLE in zone_types:
            zones.append(self._build_action_zone(thread_state, viewer_role))
        
        # Memory Kiosk
        if ZoneType.KIOSK in zone_types:
            zones.append(self._build_memory_zone(thread_state, viewer_role))
        
        # Timeline Strip
        if ZoneType.TIMELINE in zone_types:
            zones.append(self._build_timeline_zone(thread_state, viewer_role))
        
        # Resource Shelf
        if ZoneType.SHELF in zone_types:
            zones.append(self._build_resource_zone(thread_state, viewer_role))
        
        # Build portals to linked threads
        portals = self._build_portals(thread_state)
        
        # Collect references
        references = BlueprintReferences(
            events=thread_state.get("referenced_event_ids", []),
            snapshots=thread_state.get("referenced_snapshot_ids", [])
        )
        
        blueprint = XRBlueprint(
            thread_id=thread_id,
            template=template,
            zones=zones,
            portals=portals,
            references=references
        )
        
        logger.info(f"Generated blueprint for {thread_id}: {len(zones)} zones")
        return blueprint
    
    def _select_template(self, thread_state: Dict[str, Any]) -> XRTemplate:
        """Select XR template based on thread type."""
        thread_type = thread_state.get("thread_type", "personal")
        
        template_map = {
            "personal": XRTemplate.PERSONAL_ROOM,
            "business": XRTemplate.BUSINESS_ROOM,
            "cause": XRTemplate.CAUSE_ROOM,
            "research": XRTemplate.LAB_ROOM,
            "collective": XRTemplate.CAUSE_ROOM,
        }
        
        return template_map.get(thread_type, XRTemplate.PERSONAL_ROOM)
    
    def _build_intent_zone(self, thread_state: Dict[str, Any], viewer_role: ViewerRole) -> BlueprintZone:
        """Build the intent wall zone."""
        founding_intent = thread_state.get("founding_intent", "")
        
        items = [
            BlueprintItem(
                id="item_founding_intent",
                kind=ItemKind.INTENT,
                label=founding_intent,
                redaction_level=self._get_redaction_level(viewer_role),
                actions=[BlueprintItemAction.VIEW_DETAILS]
            )
        ]
        
        return BlueprintZone(
            id="zone_intent",
            type=ZoneType.WALL,
            title="Intent Wall",
            items=items
        )
    
    def _build_decision_zone(self, thread_state: Dict[str, Any], viewer_role: ViewerRole) -> BlueprintZone:
        """Build the decision wall zone."""
        decisions = thread_state.get("decisions", [])
        
        items = []
        for i, decision in enumerate(decisions[:10]):  # Limit to 10
            items.append(BlueprintItem(
                id=f"item_decision_{i}",
                kind=ItemKind.DECISION,
                label=decision.get("title", f"Decision {i+1}"),
                redaction_level=self._get_redaction_level(viewer_role),
                source_event_id=decision.get("event_id"),
                actions=[BlueprintItemAction.VIEW_DETAILS, BlueprintItemAction.JUMP_TO_SOURCE],
                metadata={"rationale": decision.get("rationale")}
            ))
        
        return BlueprintZone(
            id="zone_decisions",
            type=ZoneType.WALL,
            title="Decision Wall",
            items=items
        )
    
    def _build_action_zone(self, thread_state: Dict[str, Any], viewer_role: ViewerRole) -> BlueprintZone:
        """Build the action table zone."""
        actions = thread_state.get("actions", [])
        
        items = []
        for i, action in enumerate(actions[:20]):  # Limit to 20
            available_actions = [BlueprintItemAction.VIEW_DETAILS]
            
            # Add write actions based on role
            if viewer_role in [ViewerRole.CONTRIBUTOR, ViewerRole.ADMIN, ViewerRole.OWNER]:
                available_actions.extend([
                    BlueprintItemAction.MARK_DONE,
                    BlueprintItemAction.CHANGE_STATUS,
                    BlueprintItemAction.ADD_NOTE,
                ])
            
            items.append(BlueprintItem(
                id=action.get("id", f"item_action_{i}"),
                kind=ItemKind.ACTION,
                label=action.get("title", f"Action {i+1}"),
                redaction_level=self._get_redaction_level(viewer_role),
                source_event_id=action.get("event_id"),
                actions=available_actions,
                status=ActionStatus(action.get("status", "todo")),
                assignee=action.get("assignee"),
                due_date=action.get("due_date"),
                metadata={"description": action.get("description")}
            ))
        
        return BlueprintZone(
            id="zone_actions",
            type=ZoneType.TABLE,
            title="Action Table",
            items=items
        )
    
    def _build_memory_zone(self, thread_state: Dict[str, Any], viewer_role: ViewerRole) -> BlueprintZone:
        """Build the memory kiosk zone."""
        summaries = thread_state.get("summaries", [])
        
        items = []
        for i, summary in enumerate(summaries[:5]):  # Limit to 5 latest
            items.append(BlueprintItem(
                id=f"item_memory_{i}",
                kind=ItemKind.MEMORY,
                label=summary.get("excerpt", f"Summary {i+1}"),
                redaction_level=self._get_redaction_level(viewer_role),
                source_snapshot_id=summary.get("snapshot_id"),
                actions=[BlueprintItemAction.VIEW_DETAILS],
                metadata={"full_text": summary.get("content")}
            ))
        
        return BlueprintZone(
            id="zone_memory",
            type=ZoneType.KIOSK,
            title="Memory Kiosk",
            items=items
        )
    
    def _build_timeline_zone(self, thread_state: Dict[str, Any], viewer_role: ViewerRole) -> BlueprintZone:
        """Build the timeline strip zone."""
        events = thread_state.get("timeline_events", [])
        
        items = []
        for i, event in enumerate(events[:30]):  # Limit to 30
            items.append(BlueprintItem(
                id=f"item_timeline_{i}",
                kind=ItemKind.TIMELINE_EVENT,
                label=event.get("label", f"Event {i+1}"),
                redaction_level=self._get_redaction_level(viewer_role),
                source_event_id=event.get("event_id"),
                actions=[BlueprintItemAction.JUMP_TO_SOURCE],
                metadata={"event_type": event.get("type"), "timestamp": event.get("timestamp")}
            ))
        
        return BlueprintZone(
            id="zone_timeline",
            type=ZoneType.TIMELINE,
            title="Timeline",
            items=items
        )
    
    def _build_resource_zone(self, thread_state: Dict[str, Any], viewer_role: ViewerRole) -> BlueprintZone:
        """Build the resource shelf zone."""
        links = thread_state.get("links", [])
        
        items = []
        for i, link in enumerate(links[:15]):  # Limit to 15
            items.append(BlueprintItem(
                id=f"item_resource_{i}",
                kind=ItemKind.RESOURCE,
                label=link.get("title", f"Link {i+1}"),
                redaction_level=self._get_redaction_level(viewer_role),
                source_event_id=link.get("event_id"),
                actions=[BlueprintItemAction.VIEW_DETAILS],
                metadata={"url": link.get("url"), "type": link.get("type")}
            ))
        
        return BlueprintZone(
            id="zone_resources",
            type=ZoneType.SHELF,
            title="Resources",
            items=items
        )
    
    def _build_portals(self, thread_state: Dict[str, Any]) -> List[ThreadPortal]:
        """Build portals to linked threads."""
        linked_threads = thread_state.get("linked_threads", [])
        
        portals = []
        for lt in linked_threads[:5]:  # Limit to 5
            portals.append(ThreadPortal(
                label=lt.get("title", "Linked Thread"),
                thread_id=lt.get("thread_id"),
                preview_summary=lt.get("summary_excerpt")
            ))
        
        return portals
    
    def _get_redaction_level(self, viewer_role: ViewerRole) -> RedactionLevel:
        """Determine redaction level based on viewer role."""
        if viewer_role in [ViewerRole.OWNER, ViewerRole.ADMIN]:
            return RedactionLevel.PRIVATE
        elif viewer_role == ViewerRole.CONTRIBUTOR:
            return RedactionLevel.SEMI_PRIVATE
        else:
            return RedactionLevel.PUBLIC


# ═══════════════════════════════════════════════════════════════════════════════
# XR RENDERER SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class XRRendererService:
    """
    XR Renderer Service - projection of Thread into XR room.
    
    Responsibilities:
    - Generate blueprints from thread state
    - Handle XR interactions -> emit ThreadEvents
    - Enforce permissions and redaction
    - Support offline buffering
    
    CRITICAL: XR is a PROJECTION. No canonical XR state.
    All mutations go through thread events.
    """
    
    def __init__(self):
        self.maturity_service = MaturityService()
        self.blueprint_generator = BlueprintGenerator(self.maturity_service)
        self._blueprint_cache: Dict[str, XRBlueprint] = {}
        
        logger.info("XRRendererService initialized")
    
    async def get_thread_lobby(
        self,
        thread_id: str,
        thread_state: Dict[str, Any],
        viewer_role: ViewerRole = ViewerRole.VIEWER,
        viewer_id: str = ""
    ) -> ThreadLobbyData:
        """
        Get Thread Lobby data for entry screen.
        
        The lobby shows:
        - Title + founding intent
        - Maturity level + last updated
        - Latest summary excerpt
        - Mode CTAs (Chat/Live/XR)
        - Mode recommendation
        """
        # Compute maturity
        event_counts = thread_state.get("event_counts", {})
        metadata = thread_state.get("metadata", {})
        
        maturity = await self.maturity_service.compute_maturity(
            thread_id, event_counts, metadata
        )
        
        # Get latest summary
        summaries = thread_state.get("summaries", [])
        summary_excerpt = None
        if summaries:
            latest = summaries[0]
            summary_excerpt = ThreadSummaryExcerpt(
                text=latest.get("excerpt", "")[:200],
                snapshot_id=latest.get("snapshot_id", ""),
                created_at=datetime.fromisoformat(latest.get("created_at", datetime.utcnow().isoformat()))
            )
        
        # Check live session
        live_session = LiveSessionInfo(
            is_active=thread_state.get("live_active", False),
            session_id=thread_state.get("live_session_id"),
            participant_count=thread_state.get("live_participant_count", 0),
            started_at=thread_state.get("live_started_at"),
            roles_present=thread_state.get("live_roles", [])
        )
        
        # Compute mode recommendation
        recommended_mode = self._recommend_mode(maturity, live_session, summary_excerpt)
        
        # Check permissions
        can_start_live = viewer_role in [ViewerRole.ADMIN, ViewerRole.OWNER, ViewerRole.CONTRIBUTOR]
        
        return ThreadLobbyData(
            thread_id=thread_id,
            title=thread_state.get("title", "Untitled Thread"),
            founding_intent=thread_state.get("founding_intent", ""),
            maturity=maturity,
            last_updated=datetime.fromisoformat(
                metadata.get("last_updated", datetime.utcnow().isoformat())
            ),
            summary_excerpt=summary_excerpt,
            live_session=live_session,
            recommended_mode=recommended_mode,
            can_start_live=can_start_live,
            can_enter_xr=True,
            viewer_role=viewer_role,
            action_count=len(thread_state.get("actions", [])),
            decision_count=len(thread_state.get("decisions", [])),
            link_count=len(thread_state.get("links", []))
        )
    
    def _recommend_mode(
        self,
        maturity: MaturityResult,
        live_session: LiveSessionInfo,
        summary_excerpt: Optional[ThreadSummaryExcerpt]
    ) -> ModeRecommendation:
        """
        Recommend entry mode based on context.
        
        Rules:
        - If Live ongoing: Recommend Join Live
        - If Level 0-1: Recommend Chat (simplest)
        - If Level 2-3: Recommend XR for coordination
        - If summary stale: Recommend Chat to generate new summary
        """
        # Live takes priority
        if live_session.is_active:
            return ModeRecommendation(
                mode=ThreadEntryMode.LIVE,
                reason="A live session is in progress",
                confidence=0.95
            )
        
        # Maturity-based recommendation
        if maturity.level in [MaturityLevel.SEED, MaturityLevel.SPROUT]:
            return ModeRecommendation(
                mode=ThreadEntryMode.CHAT,
                reason="Chat is best for early-stage threads",
                confidence=0.8
            )
        
        if maturity.level in [MaturityLevel.WORKSHOP, MaturityLevel.STUDIO]:
            return ModeRecommendation(
                mode=ThreadEntryMode.XR,
                reason="XR provides better overview for coordination",
                confidence=0.75
            )
        
        # Default to chat
        return ModeRecommendation(
            mode=ThreadEntryMode.CHAT,
            reason="Continue where you left off",
            confidence=0.6
        )
    
    async def get_xr_preflight(
        self,
        thread_id: str,
        thread_state: Dict[str, Any],
        viewer_role: ViewerRole,
        is_first_time: bool = False
    ) -> XRPreflightData:
        """
        Get XR preflight data for modal before entering.
        
        Shows:
        - Zones that will be visible
        - Permissions
        - Privacy note
        """
        maturity = await self.maturity_service.get_cached_maturity(thread_id)
        if not maturity:
            event_counts = thread_state.get("event_counts", {})
            metadata = thread_state.get("metadata", {})
            maturity = await self.maturity_service.compute_maturity(
                thread_id, event_counts, metadata
            )
        
        zones = self.maturity_service.get_zones_for_maturity(maturity.level)
        
        return XRPreflightData(
            thread_id=thread_id,
            zones_visible=[z.value for z in zones],
            permissions=viewer_role,
            redaction_enforced=True,
            is_first_time=is_first_time
        )
    
    async def generate_blueprint(
        self,
        thread_id: str,
        thread_state: Dict[str, Any],
        viewer_role: ViewerRole = ViewerRole.VIEWER
    ) -> XRBlueprint:
        """
        Generate XR Blueprint for rendering.
        
        Blueprint is cached but always derived from thread state.
        """
        # Compute maturity
        event_counts = thread_state.get("event_counts", {})
        metadata = thread_state.get("metadata", {})
        
        maturity = await self.maturity_service.compute_maturity(
            thread_id, event_counts, metadata
        )
        
        # Generate blueprint
        blueprint = await self.blueprint_generator.generate(
            thread_id, thread_state, maturity, viewer_role
        )
        
        # Cache it
        self._blueprint_cache[thread_id] = blueprint
        
        return blueprint
    
    async def get_latest_blueprint(self, thread_id: str) -> Optional[XRBlueprint]:
        """Get cached blueprint if available."""
        return self._blueprint_cache.get(thread_id)
    
    def create_action_update_event(
        self,
        thread_id: str,
        action_id: str,
        new_status: ActionStatus,
        context: XRInteractionContext,
        actor_id: str
    ) -> Dict[str, Any]:
        """
        Create ACTION_UPDATED ThreadEvent from XR interaction.
        
        This is a PROJECTION -> EVENT conversion.
        The event must be POSTed to thread API, not applied locally.
        """
        return {
            "event_id": str(uuid4()),
            "thread_id": thread_id,
            "event_type": "ACTION_UPDATED",
            "created_at": datetime.utcnow().isoformat(),
            "actor_type": "human",
            "actor_id": actor_id,
            "payload": ActionUpdatePayload(
                action_id=action_id,
                status=new_status,
                context=context
            ).model_dump()
        }
    
    def create_action_create_event(
        self,
        thread_id: str,
        title: str,
        description: Optional[str],
        context: XRInteractionContext,
        actor_id: str
    ) -> Dict[str, Any]:
        """
        Create ACTION_CREATED ThreadEvent from XR interaction.
        """
        return {
            "event_id": str(uuid4()),
            "thread_id": thread_id,
            "event_type": "ACTION_CREATED",
            "created_at": datetime.utcnow().isoformat(),
            "actor_type": "human",
            "actor_id": actor_id,
            "payload": ActionCreatePayload(
                title=title,
                description=description,
                context=context
            ).model_dump()
        }
    
    def create_note_event(
        self,
        thread_id: str,
        text: str,
        context: XRInteractionContext,
        actor_id: str
    ) -> Dict[str, Any]:
        """
        Create MESSAGE_POSTED (note) ThreadEvent from XR interaction.
        """
        return {
            "event_id": str(uuid4()),
            "thread_id": thread_id,
            "event_type": "MESSAGE_POSTED",
            "created_at": datetime.utcnow().isoformat(),
            "actor_type": "human",
            "actor_id": actor_id,
            "payload": NoteAddPayload(
                text=text,
                tags=["note"],
                context=context
            ).model_dump()
        }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "BlueprintGenerator",
    "XRRendererService",
]
