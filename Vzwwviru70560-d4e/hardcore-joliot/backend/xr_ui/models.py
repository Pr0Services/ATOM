"""
============================================================================
CHE·NU™ V69 — XR/UI MODULE MODELS
============================================================================
Version: 1.0.0
Specs: GPT1/CHE-NU_TIMELINE_DIVERGENCE_UI.md, CHE-NU_LAB_WORKBENCH_XR.md,
       CHE-NU_XR_CAUSAL_INTERVENTION_UX.md, CHE-NU_XR_CAUSAL_TRACE_VISUALIZATION.md
Principle: XR = READ ONLY, GOUVERNANCE > EXÉCUTION

"XR = espace de compréhension, jamais d'exécution"
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import uuid
import hashlib
import json


# ============================================================================
# ENUMS
# ============================================================================

class RenderMode(str, Enum):
    """
    XR render modes.
    
    Per spec: Ghost Reality, Risk Heatmap, Causal Threads
    """
    GHOST_REALITY = "ghost_reality"  # Base scenario transparent
    RISK_HEATMAP = "risk_heatmap"  # Unstable zones colored
    CAUSAL_THREADS = "causal_threads"  # Dependency threads


class InteractionType(str, Enum):
    """
    XR interaction types.
    
    Per spec: Grab & Slide, Ripple Effect, Causal Magnifier
    """
    GRAB_SLIDE = "grab_slide"
    RIPPLE_EFFECT = "ripple_effect"
    CAUSAL_MAGNIFIER = "causal_magnifier"
    TIME_SCRUB = "time_scrub"
    SNAPSHOT = "snapshot"


class ImpactColor(str, Enum):
    """Impact visualization colors"""
    GREEN = "green"  # Positive
    RED = "red"  # Negative
    YELLOW = "yellow"  # Neutral/Warning


class WorkbenchTool(str, Enum):
    """
    Lab workbench tools.
    
    Per spec: Stress-Testeur, Réacteur de Synthèse, Chronos, Spectromètre
    """
    STRESS_TESTER = "stress_testeur"
    SYNTHESIS_REACTOR = "reacteur_synthese"
    CHRONOS = "chronos"  # Time accelerator
    CAUSAL_SPECTROMETER = "spectrometre_causal"


# ============================================================================
# TIMELINE MODELS
# ============================================================================

@dataclass
class TimelinePoint:
    """A point on a timeline"""
    time: int  # Simulation time
    values: Dict[str, float] = field(default_factory=dict)
    is_key_decision: bool = False
    decision_label: str = ""


@dataclass
class Timeline:
    """A simulation timeline"""
    timeline_id: str
    scenario_id: str
    name: str
    
    points: List[TimelinePoint] = field(default_factory=list)
    
    # Visual
    color: str = "#3498db"
    opacity: float = 1.0


@dataclass
class DivergenceMarker:
    """
    Marker where timelines diverge.
    
    Per spec: Divergence markers
    """
    marker_id: str
    time: int
    
    # Diverging timelines
    timeline_a: str
    timeline_b: str
    
    # Delta
    delta_values: Dict[str, float] = field(default_factory=dict)
    cause: str = ""


@dataclass
class RiskHeatmapCell:
    """
    A cell in the risk heatmap.
    
    Per spec: Differential risk heatmaps
    """
    slot_id: str
    time: int
    risk_level: float  # 0-1
    color: ImpactColor = ImpactColor.GREEN


# ============================================================================
# WORKBENCH MODELS
# ============================================================================

@dataclass
class WorkbenchArtifact:
    """
    An artifact in the XR workbench.
    
    Per spec: Interface XR où l'utilisateur manipule des Artifacts
    """
    artifact_id: str
    name: str
    
    # Data
    data: Dict[str, Any] = field(default_factory=dict)
    
    # Position in XR space
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    
    # State
    is_selected: bool = False
    is_locked: bool = False


@dataclass
class ToolResult:
    """Result from a workbench tool"""
    tool: WorkbenchTool
    input_artifact: str
    output_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# CAUSAL INTERVENTION MODELS
# ============================================================================

@dataclass
class CausalProxy:
    """
    Causal proxy for intervention.
    
    Per spec: Causal Proxies - représentations physiques de variables causales
    """
    proxy_id: str
    slot_id: str
    name: str
    
    # Current value
    value: float
    original_value: float
    
    # Visual representation
    shape: str = "sphere"  # sphere, lever, slider
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    
    # Interaction state
    is_grabbed: bool = False
    is_modified: bool = False


@dataclass
class RippleWave:
    """
    Ripple effect visualization.
    
    Per spec: Onde visuelle propagée vers les effets
    """
    source_proxy: str
    affected_proxies: List[str] = field(default_factory=list)
    
    # Visual
    color: ImpactColor = ImpactColor.GREEN
    intensity: float = 1.0  # Force causale


@dataclass
class InterventionDraft:
    """
    Draft artifact from intervention.
    
    Per spec: génère un draft artifact
    """
    draft_id: str
    proxy_id: str
    
    # Changes
    original_value: float
    new_value: float
    
    # Effects
    downstream_effects: Dict[str, float] = field(default_factory=dict)
    
    # Validation
    opa_approved: bool = False
    approver_id: str = ""


# ============================================================================
# CAUSAL TRACE MODELS
# ============================================================================

@dataclass
class CausalPath:
    """
    Causal path visualization.
    
    Per spec: Liens lumineux entre causes et effets
    """
    path_id: str
    source_slot: str
    target_slot: str
    
    # Visual
    thickness: float = 1.0  # Force causale
    intensity: float = 1.0  # Certitude
    
    # Intermediate nodes
    path_nodes: List[str] = field(default_factory=list)


@dataclass
class UncertaintyNode:
    """
    Node of uncertainty.
    
    Per spec: Sphères nuageuses pulsantes - hypothèses non stabilisées
    """
    node_id: str
    slot_id: str
    
    # Missing data
    missing_slots: List[str] = field(default_factory=list)
    
    # Visual
    pulse_rate: float = 1.0  # Hz
    cloud_density: float = 0.5


@dataclass
class ConterfactualHeatmap:
    """
    Counterfactual heatmap.
    
    Per spec: Couleurs superposées - Vert: gains, Rouge: effets négatifs
    """
    heatmap_id: str
    
    # Comparison
    base_state: Dict[str, float] = field(default_factory=dict)
    modified_state: Dict[str, float] = field(default_factory=dict)
    
    # Cells
    cells: List[RiskHeatmapCell] = field(default_factory=list)


# ============================================================================
# XR PACK MODELS
# ============================================================================

@dataclass
class XRPack:
    """
    Signed XR pack for export.
    
    Per spec: Export XR Pack signé
    """
    pack_id: str
    session_id: str
    
    # Content
    timelines: List[Timeline] = field(default_factory=list)
    artifacts: List[WorkbenchArtifact] = field(default_factory=list)
    interventions: List[InterventionDraft] = field(default_factory=list)
    
    # Signature
    signature: str = ""
    
    # Read-only flag
    read_only: bool = True


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def compute_hash(data: Any) -> str:
    """Compute hash of data"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def sign_xr_pack(pack: XRPack, signer_id: str) -> str:
    """Sign an XR pack"""
    payload = {
        "pack_id": pack.pack_id,
        "session_id": pack.session_id,
        "timeline_count": len(pack.timelines),
        "artifact_count": len(pack.artifacts),
    }
    return compute_hash(f"{json.dumps(payload)}:{signer_id}")
