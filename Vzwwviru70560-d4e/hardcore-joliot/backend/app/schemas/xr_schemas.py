"""
SCHEMA: xr_schemas.py
VERSION: 1.0.0
INTENT: Pydantic schemas for XR Renderer + Thread Maturity + UX Entry

R&D COMPLIANCE: ✅
- Rule #3: Sphere Integrity - XR is PROJECTION only, no canonical state
- Rule #6: Traceability - All objects have proper identifiers
"""

from typing import Optional, List, Dict, Any, Literal
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class RedactionLevel(str, Enum):
    """Visibility levels for content."""
    PUBLIC = "public"
    SEMI_PRIVATE = "semi_private"
    PRIVATE = "private"


class ZoneType(str, Enum):
    """Types of zones in XR environment."""
    WALL = "wall"
    TABLE = "table"
    KIOSK = "kiosk"
    SHELF = "shelf"
    TIMELINE = "timeline"
    PORTAL_AREA = "portal_area"


class ItemKind(str, Enum):
    """Types of items in XR zones."""
    INTENT = "intent"
    DECISION = "decision"
    ACTION = "action"
    MEMORY = "memory"
    RESOURCE = "resource"
    TIMELINE_EVENT = "timeline_event"
    NOTE = "note"


class XRTemplate(str, Enum):
    """Available XR room templates."""
    PERSONAL_ROOM = "personal_room"
    BUSINESS_ROOM = "business_room"
    CAUSE_ROOM = "cause_room"
    LAB_ROOM = "lab_room"
    CUSTOM_ROOM = "custom_room"


class MaturityLevel(int, Enum):
    """Thread maturity levels 0-5."""
    SEED = 0        # Intent only, few messages
    SPROUT = 1      # Chat active, first actions/decisions appear
    WORKSHOP = 2    # Tasks structured, summaries exist
    STUDIO = 3      # Multiple participants, live sessions, linked threads
    ORG = 4         # Cross-thread dependencies, governance, regular snapshots
    ECOSYSTEM = 5   # Many linked threads, portals, high continuity


class ThreadEntryMode(str, Enum):
    """Modes for entering a thread."""
    CHAT = "chat"
    LIVE = "live"
    XR = "xr"


class ViewerRole(str, Enum):
    """Roles for XR viewers."""
    VIEWER = "viewer"           # Read-only
    CONTRIBUTOR = "contributor"  # Can create/update actions, add notes
    ADMIN = "admin"             # Full permissions (still append-only)
    OWNER = "owner"             # Same as admin


class ActionStatus(str, Enum):
    """Status of actions."""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


# ═══════════════════════════════════════════════════════════════════════════════
# XR BLUEPRINT
# ═══════════════════════════════════════════════════════════════════════════════

class BlueprintItemAction(str, Enum):
    """Available actions on blueprint items."""
    MARK_DONE = "mark_done"
    CHANGE_STATUS = "change_status"
    ADD_NOTE = "add_note"
    VIEW_DETAILS = "view_details"
    JUMP_TO_SOURCE = "jump_to_source"


class BlueprintItem(BaseModel):
    """An item rendered in an XR zone."""
    id: str
    kind: ItemKind
    label: str
    redaction_level: RedactionLevel = RedactionLevel.SEMI_PRIVATE
    source_event_id: Optional[str] = None
    source_snapshot_id: Optional[str] = None
    actions: List[BlueprintItemAction] = []
    metadata: Optional[Dict[str, Any]] = None
    
    # For action items
    status: Optional[ActionStatus] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None


class ZoneLayout(BaseModel):
    """Layout configuration for a zone."""
    position: Optional[Dict[str, float]] = None  # x, y, z
    rotation: Optional[Dict[str, float]] = None  # pitch, yaw, roll
    scale: Optional[Dict[str, float]] = None     # w, h, d
    style: Optional[str] = None


class BlueprintZone(BaseModel):
    """A zone in the XR environment."""
    id: str
    type: ZoneType
    title: str
    items: List[BlueprintItem] = []
    layout: Optional[ZoneLayout] = None


class ThreadPortal(BaseModel):
    """Portal to another thread."""
    label: str
    thread_id: str
    preview_summary: Optional[str] = None


class BlueprintReferences(BaseModel):
    """References to source data for the blueprint."""
    events: List[str] = []
    snapshots: List[str] = []


class XRBlueprint(BaseModel):
    """Complete XR environment blueprint (derived from Thread)."""
    thread_id: str
    template: XRTemplate
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0"
    zones: List[BlueprintZone]
    portals: List[ThreadPortal] = []
    references: Optional[BlueprintReferences] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "thread_id": "th_123",
                "template": "personal_room",
                "generated_at": "2026-01-07T00:00:00Z",
                "version": "1.0.0",
                "zones": [
                    {
                        "id": "zone_intent",
                        "type": "wall",
                        "title": "Intent Wall",
                        "items": [
                            {
                                "id": "item_1",
                                "kind": "intent",
                                "label": "Build a personal finance tracker",
                                "redaction_level": "semi_private"
                            }
                        ]
                    }
                ]
            }
        }


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD MATURITY
# ═══════════════════════════════════════════════════════════════════════════════

class MaturitySignals(BaseModel):
    """Signals used to compute maturity score."""
    has_summary: bool = False
    has_decisions: bool = False
    action_count: int = 0
    participant_count: int = 0
    has_live_segments: bool = False
    link_count: int = 0
    message_count: int = 0
    learning_event_count: int = 0
    thread_age_days: int = 0
    linked_thread_count: int = 0


class MaturityResult(BaseModel):
    """Result of maturity computation (derived)."""
    thread_id: str
    score: int = Field(ge=0, le=100)
    level: MaturityLevel
    label: Literal["Seed", "Sprout", "Workshop", "Studio", "Org", "Ecosystem"]
    signals: MaturitySignals
    computed_at: datetime = Field(default_factory=datetime.utcnow)
    
    @staticmethod
    def score_to_level(score: int) -> MaturityLevel:
        """Convert numeric score to maturity level."""
        if score < 10:
            return MaturityLevel.SEED
        elif score < 25:
            return MaturityLevel.SPROUT
        elif score < 45:
            return MaturityLevel.WORKSHOP
        elif score < 65:
            return MaturityLevel.STUDIO
        elif score < 85:
            return MaturityLevel.ORG
        else:
            return MaturityLevel.ECOSYSTEM
    
    @staticmethod
    def level_to_label(level: MaturityLevel) -> str:
        """Convert maturity level to human-readable label."""
        labels = {
            MaturityLevel.SEED: "Seed",
            MaturityLevel.SPROUT: "Sprout",
            MaturityLevel.WORKSHOP: "Workshop",
            MaturityLevel.STUDIO: "Studio",
            MaturityLevel.ORG: "Org",
            MaturityLevel.ECOSYSTEM: "Ecosystem"
        }
        return labels[level]


# ═══════════════════════════════════════════════════════════════════════════════
# THREAD LOBBY / UX ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

class LiveSessionInfo(BaseModel):
    """Information about ongoing live session."""
    is_active: bool = False
    session_id: Optional[str] = None
    participant_count: int = 0
    started_at: Optional[datetime] = None
    roles_present: List[str] = []


class ThreadSummaryExcerpt(BaseModel):
    """Excerpt from latest summary for lobby display."""
    text: str
    snapshot_id: str
    created_at: datetime


class ModeRecommendation(BaseModel):
    """Recommended mode for entering thread."""
    mode: ThreadEntryMode
    reason: str
    confidence: float = Field(ge=0.0, le=1.0)


class ThreadLobbyData(BaseModel):
    """Data for Thread Lobby screen."""
    thread_id: str
    title: str
    founding_intent: str
    
    # Maturity
    maturity: MaturityResult
    
    # Status
    last_updated: datetime
    summary_excerpt: Optional[ThreadSummaryExcerpt] = None
    
    # Live
    live_session: LiveSessionInfo
    
    # Recommendations
    recommended_mode: ModeRecommendation
    
    # Permissions
    can_start_live: bool = False
    can_enter_xr: bool = True
    viewer_role: ViewerRole = ViewerRole.VIEWER
    
    # Stats
    action_count: int = 0
    decision_count: int = 0
    link_count: int = 0


class XRPreflightData(BaseModel):
    """Data for XR preflight modal."""
    thread_id: str
    zones_visible: List[str]  # Zone types that will be rendered
    permissions: ViewerRole
    redaction_enforced: bool = True
    is_first_time: bool = False


class XROnboardingStep(BaseModel):
    """Step in first-time XR onboarding."""
    step_number: int
    message_fr: str
    message_en: str
    highlight_zone: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# XR INTERACTIONS (Events to emit)
# ═══════════════════════════════════════════════════════════════════════════════

class XRInteractionContext(BaseModel):
    """Context for XR interaction."""
    zone_id: str
    item_id: Optional[str] = None
    position: Optional[Dict[str, float]] = None


class ActionUpdatePayload(BaseModel):
    """Payload for ACTION_UPDATED from XR."""
    action_id: str
    status: ActionStatus
    context: Optional[XRInteractionContext] = None


class ActionCreatePayload(BaseModel):
    """Payload for ACTION_CREATED from XR."""
    title: str
    description: Optional[str] = None
    status: ActionStatus = ActionStatus.TODO
    due_date: Optional[datetime] = None
    assignee: Optional[str] = None
    context: Optional[XRInteractionContext] = None


class NoteAddPayload(BaseModel):
    """Payload for MESSAGE_POSTED (note) from XR."""
    text: str
    tags: List[str] = ["note"]
    context: Optional[XRInteractionContext] = None


# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT EVOLUTION RULES
# ═══════════════════════════════════════════════════════════════════════════════

class EnvironmentEvolutionRule(BaseModel):
    """Rule for what zones appear at each maturity level."""
    level: MaturityLevel
    zones: List[ZoneType]
    features: List[str]
    
    @staticmethod
    def get_zones_for_level(level: MaturityLevel) -> List[ZoneType]:
        """Get zones that should be visible at a maturity level."""
        evolution = {
            MaturityLevel.SEED: [ZoneType.WALL, ZoneType.KIOSK],
            MaturityLevel.SPROUT: [ZoneType.WALL, ZoneType.KIOSK, ZoneType.TABLE],
            MaturityLevel.WORKSHOP: [ZoneType.WALL, ZoneType.KIOSK, ZoneType.TABLE, ZoneType.SHELF, ZoneType.TIMELINE],
            MaturityLevel.STUDIO: [ZoneType.WALL, ZoneType.KIOSK, ZoneType.TABLE, ZoneType.SHELF, ZoneType.TIMELINE, ZoneType.PORTAL_AREA],
            MaturityLevel.ORG: [ZoneType.WALL, ZoneType.KIOSK, ZoneType.TABLE, ZoneType.SHELF, ZoneType.TIMELINE, ZoneType.PORTAL_AREA],
            MaturityLevel.ECOSYSTEM: [ZoneType.WALL, ZoneType.KIOSK, ZoneType.TABLE, ZoneType.SHELF, ZoneType.TIMELINE, ZoneType.PORTAL_AREA],
        }
        return evolution.get(level, [])


# ═══════════════════════════════════════════════════════════════════════════════
# UX MICROCOPY
# ═══════════════════════════════════════════════════════════════════════════════

class UXMicrocopy:
    """Static UX microcopy in French and English."""
    
    LOBBY_HEADER_FR = "Bienvenue dans ce thread."
    LOBBY_HEADER_EN = "Welcome to this thread."
    
    LOBBY_SUBTITLE_FR = "Voici où on en est, et ce que tu peux faire maintenant."
    LOBBY_SUBTITLE_EN = "Here's where we stand, and what you can do now."
    
    MATURITY_LABEL_FR = "Niveau de maturité"
    MATURITY_LABEL_EN = "Maturity level"
    
    LAST_UPDATE_FR = "Dernière mise à jour"
    LAST_UPDATE_EN = "Last updated"
    
    SUMMARY_FR = "Résumé"
    SUMMARY_EN = "Summary"
    
    CTA_CHAT_FR = "Continuer en chat"
    CTA_CHAT_EN = "Continue in chat"
    
    CTA_XR_FR = "Entrer dans la salle (XR)"
    CTA_XR_EN = "Enter XR Room"
    
    CTA_START_LIVE_FR = "Démarrer un live"
    CTA_START_LIVE_EN = "Start Live"
    
    CTA_JOIN_LIVE_FR = "Rejoindre le live"
    CTA_JOIN_LIVE_EN = "Join Live"
    
    PREFLIGHT_NOTE_1_FR = "Cette salle est une projection du thread."
    PREFLIGHT_NOTE_1_EN = "This room is a projection of the thread."
    
    PREFLIGHT_NOTE_2_FR = "Tes actions ici deviennent des événements."
    PREFLIGHT_NOTE_2_EN = "Your actions here become events."
    
    PREFLIGHT_NOTE_3_FR = "Ta visibilité respecte les niveaux de confidentialité."
    PREFLIGHT_NOTE_3_EN = "Your visibility respects privacy levels."
    
    ONBOARDING_1_FR = "Rien ne se perd."
    ONBOARDING_1_EN = "Nothing is lost."
    
    ONBOARDING_2_FR = "Chaque décision garde son 'pourquoi'."
    ONBOARDING_2_EN = "Every decision keeps its 'why'."
    
    ONBOARDING_3_FR = "Tu peux demander un résumé à tout moment."
    ONBOARDING_3_EN = "You can request a summary anytime."


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Enums
    "RedactionLevel",
    "ZoneType",
    "ItemKind",
    "XRTemplate",
    "MaturityLevel",
    "ThreadEntryMode",
    "ViewerRole",
    "ActionStatus",
    "BlueprintItemAction",
    
    # Blueprint
    "BlueprintItem",
    "ZoneLayout",
    "BlueprintZone",
    "ThreadPortal",
    "BlueprintReferences",
    "XRBlueprint",
    
    # Maturity
    "MaturitySignals",
    "MaturityResult",
    
    # Lobby/UX
    "LiveSessionInfo",
    "ThreadSummaryExcerpt",
    "ModeRecommendation",
    "ThreadLobbyData",
    "XRPreflightData",
    "XROnboardingStep",
    
    # Interactions
    "XRInteractionContext",
    "ActionUpdatePayload",
    "ActionCreatePayload",
    "NoteAddPayload",
    
    # Evolution
    "EnvironmentEvolutionRule",
    
    # Microcopy
    "UXMicrocopy",
]
