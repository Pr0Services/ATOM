"""
============================================================================
CHE·NU™ V69 — SLOT FILL XR VISUALIZATION
============================================================================
Spec: GPT1/CHE-NU_ENG_SLOT_FILL_XR_VISUALIZATION.md

Objective: Visualize in XR:
- la structure du document
- les slots remplis / manquants
- les dépendances logiques

Concepts XR:
- Chaque section = node spatial
- Chaque slot = capsule
- Couleurs: Vert=validé, Jaune=rempli non validé, Rouge=manquant/bloquant

Interactions:
- Sélection d'un slot → afficher explainability
- Validation humaine en XR (read-only décisionnel)
- Simulation de remplissage (no write)

Governance:
- XR = lecture seule
- Aucune modification possible
- Conforme OPA rule XR_READ_ONLY
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import json
import math
import logging

from ..models import (
    Slot,
    SlotStatus,
    Document,
    XRSlotVisualization,
)

logger = logging.getLogger(__name__)


# ============================================================================
# XR COLORS (per spec)
# ============================================================================

class XRColor(str, Enum):
    """XR colors per spec"""
    GREEN = "#00FF00"  # Validé
    YELLOW = "#FFFF00"  # Rempli non validé
    RED = "#FF0000"  # Manquant / bloquant
    GRAY = "#808080"  # Disabled / inactive
    BLUE = "#0088FF"  # Selected
    ORANGE = "#FF8800"  # Warning


def status_to_color(status: SlotStatus) -> str:
    """Map status to XR color per spec"""
    mapping = {
        SlotStatus.VALIDATED: XRColor.GREEN.value,
        SlotStatus.FILLED: XRColor.YELLOW.value,
        SlotStatus.PENDING: XRColor.YELLOW.value,
        SlotStatus.EMPTY: XRColor.RED.value,
        SlotStatus.FAILED: XRColor.RED.value,
        SlotStatus.BLOCKED: XRColor.RED.value,
    }
    return mapping.get(status, XRColor.GRAY.value)


# ============================================================================
# XR NODE TYPES
# ============================================================================

class XRNodeType(str, Enum):
    """Types of XR nodes"""
    SECTION = "section"  # Document section
    SLOT = "slot"  # Individual slot
    CONNECTION = "connection"  # Dependency link


# ============================================================================
# XR SCENE MODELS
# ============================================================================

@dataclass
class XRPosition:
    """3D position in XR space"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}
    
    def distance_to(self, other: "XRPosition") -> float:
        """Calculate distance to another position"""
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )


@dataclass
class XRNode:
    """
    A node in the XR scene.
    
    Per spec: Chaque section = node spatial
    """
    node_id: str
    node_type: XRNodeType
    position: XRPosition
    label: str
    color: str
    size: float = 1.0
    visible: bool = True
    selectable: bool = True
    
    # Slot-specific data
    slot_id: Optional[str] = None
    slot_status: Optional[SlotStatus] = None
    explainability_preview: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "position": self.position.to_dict(),
            "label": self.label,
            "color": self.color,
            "size": self.size,
            "visible": self.visible,
            "selectable": self.selectable,
            "slot_id": self.slot_id,
            "slot_status": self.slot_status.value if self.slot_status else None,
            "explainability_preview": self.explainability_preview,
            "metadata": self.metadata,
        }


@dataclass
class XRConnection:
    """
    A connection between nodes (dependency).
    
    Per spec: Visualize les dépendances logiques
    """
    connection_id: str
    source_id: str
    target_id: str
    color: str = "#FFFFFF"
    width: float = 0.1
    animated: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "connection_id": self.connection_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "color": self.color,
            "width": self.width,
            "animated": self.animated,
        }


@dataclass
class XRScene:
    """
    Complete XR scene for document visualization.
    
    Per spec: XR = lecture seule
    """
    scene_id: str
    document_id: str
    nodes: List[XRNode] = field(default_factory=list)
    connections: List[XRConnection] = field(default_factory=list)
    
    # Scene metadata
    read_only: bool = True  # Per spec: XR = lecture seule
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # View settings
    camera_position: XRPosition = field(default_factory=lambda: XRPosition(0, 5, 10))
    background_color: str = "#1a1a2e"
    
    def add_node(self, node: XRNode) -> None:
        self.nodes.append(node)
    
    def add_connection(self, connection: XRConnection) -> None:
        self.connections.append(connection)
    
    def get_node(self, node_id: str) -> Optional[XRNode]:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "document_id": self.document_id,
            "nodes": [n.to_dict() for n in self.nodes],
            "connections": [c.to_dict() for c in self.connections],
            "read_only": self.read_only,
            "created_at": self.created_at.isoformat(),
            "camera_position": self.camera_position.to_dict(),
            "background_color": self.background_color,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# ============================================================================
# XR LAYOUT STRATEGIES
# ============================================================================

class LayoutStrategy(str, Enum):
    """Layout strategies for XR visualization"""
    CIRCULAR = "circular"
    GRID = "grid"
    HIERARCHICAL = "hierarchical"
    FORCE_DIRECTED = "force_directed"


class XRLayoutEngine:
    """
    Computes node positions for XR visualization.
    """
    
    def __init__(self, strategy: LayoutStrategy = LayoutStrategy.CIRCULAR):
        self.strategy = strategy
        self.spacing = 2.0  # Default spacing between nodes
    
    def compute_layout(
        self,
        slots: List[Slot],
        sections: Dict[str, List[str]] = None,  # section_id → slot_ids
    ) -> Dict[str, XRPosition]:
        """Compute positions for all slots"""
        if self.strategy == LayoutStrategy.CIRCULAR:
            return self._circular_layout(slots)
        elif self.strategy == LayoutStrategy.GRID:
            return self._grid_layout(slots)
        elif self.strategy == LayoutStrategy.HIERARCHICAL:
            return self._hierarchical_layout(slots, sections)
        else:
            return self._circular_layout(slots)
    
    def _circular_layout(
        self,
        slots: List[Slot],
    ) -> Dict[str, XRPosition]:
        """Arrange slots in a circle"""
        positions = {}
        n = len(slots)
        
        if n == 0:
            return positions
        
        radius = max(self.spacing * n / (2 * math.pi), 3.0)
        
        for i, slot in enumerate(slots):
            angle = (2 * math.pi * i) / n
            positions[slot.slot_id] = XRPosition(
                x=radius * math.cos(angle),
                y=0,
                z=radius * math.sin(angle),
            )
        
        return positions
    
    def _grid_layout(
        self,
        slots: List[Slot],
    ) -> Dict[str, XRPosition]:
        """Arrange slots in a grid"""
        positions = {}
        n = len(slots)
        
        if n == 0:
            return positions
        
        cols = math.ceil(math.sqrt(n))
        
        for i, slot in enumerate(slots):
            row = i // cols
            col = i % cols
            positions[slot.slot_id] = XRPosition(
                x=(col - cols / 2) * self.spacing,
                y=0,
                z=(row - n / cols / 2) * self.spacing,
            )
        
        return positions
    
    def _hierarchical_layout(
        self,
        slots: List[Slot],
        sections: Dict[str, List[str]] = None,
    ) -> Dict[str, XRPosition]:
        """Arrange slots hierarchically by section"""
        positions = {}
        
        if not sections:
            return self._grid_layout(slots)
        
        section_y = 0
        for section_id, slot_ids in sections.items():
            section_slots = [s for s in slots if s.slot_id in slot_ids]
            
            for i, slot in enumerate(section_slots):
                positions[slot.slot_id] = XRPosition(
                    x=(i - len(section_slots) / 2) * self.spacing,
                    y=section_y,
                    z=0,
                )
            
            section_y -= self.spacing * 1.5
        
        return positions


# ============================================================================
# XR SCENE BUILDER
# ============================================================================

class XRSceneBuilder:
    """
    Builds XR scenes from documents.
    
    Per spec concepts:
    - Chaque section = node spatial
    - Chaque slot = capsule
    """
    
    def __init__(
        self,
        layout_strategy: LayoutStrategy = LayoutStrategy.CIRCULAR,
    ):
        self.layout_engine = XRLayoutEngine(layout_strategy)
    
    def build_scene(
        self,
        document: Document,
    ) -> XRScene:
        """Build XR scene from document"""
        scene = XRScene(
            scene_id=f"xr_{document.document_id}",
            document_id=document.document_id,
            read_only=True,  # Per spec
        )
        
        slots = list(document.slots.values())
        
        # Compute layout
        positions = self.layout_engine.compute_layout(slots)
        
        # Create nodes for slots
        for slot in slots:
            node = self._create_slot_node(slot, positions.get(slot.slot_id))
            scene.add_node(node)
        
        # Create connections for dependencies
        for slot in slots:
            for dep_id in slot.dependencies:
                if dep_id in document.slots:
                    connection = XRConnection(
                        connection_id=f"conn_{slot.slot_id}_{dep_id}",
                        source_id=f"node_{dep_id}",
                        target_id=f"node_{slot.slot_id}",
                        color="#4444FF",
                        animated=True,
                    )
                    scene.add_connection(connection)
        
        return scene
    
    def _create_slot_node(
        self,
        slot: Slot,
        position: XRPosition = None,
    ) -> XRNode:
        """Create XR node for a slot"""
        position = position or XRPosition()
        
        # Get color based on status (per spec)
        color = status_to_color(slot.status)
        
        # Get explainability preview
        preview = None
        if slot.explainability:
            preview = (
                f"{slot.explainability.decision_summary}\n"
                f"Confidence: {slot.explainability.confidence_score:.0%}"
            )
        
        return XRNode(
            node_id=f"node_{slot.slot_id}",
            node_type=XRNodeType.SLOT,
            position=position,
            label=slot.name,
            color=color,
            size=1.0 + (slot.causal_impact * 0.5),  # Size reflects importance
            visible=True,
            selectable=True,
            slot_id=slot.slot_id,
            slot_status=slot.status,
            explainability_preview=preview,
            metadata={
                "slot_type": slot.slot_type.value,
                "risk_level": slot.risk_level.value,
                "priority_rank": slot.priority_rank,
            },
        )
    
    def update_node_status(
        self,
        scene: XRScene,
        slot: Slot,
    ) -> bool:
        """Update node to reflect slot status change"""
        node = scene.get_node(f"node_{slot.slot_id}")
        if node:
            node.color = status_to_color(slot.status)
            node.slot_status = slot.status
            return True
        return False


# ============================================================================
# XR INTERACTION HANDLER
# ============================================================================

class XRInteractionHandler:
    """
    Handles XR interactions.
    
    Per spec:
    - Sélection d'un slot → afficher explainability
    - Validation humaine en XR (read-only décisionnel)
    - Simulation de remplissage (no write)
    
    IMPORTANT: XR = READ ONLY. No actual modifications.
    """
    
    def __init__(self):
        self._selected_node: Optional[str] = None
        self._simulated_fills: Dict[str, Any] = {}
    
    def select_node(
        self,
        scene: XRScene,
        node_id: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Select a node and return its details.
        
        Per spec: Sélection d'un slot → afficher explainability
        """
        node = scene.get_node(node_id)
        if not node:
            return None
        
        self._selected_node = node_id
        
        return {
            "node_id": node_id,
            "slot_id": node.slot_id,
            "label": node.label,
            "status": node.slot_status.value if node.slot_status else None,
            "explainability": node.explainability_preview,
            "metadata": node.metadata,
        }
    
    def simulate_fill(
        self,
        scene: XRScene,
        slot_id: str,
        simulated_value: Any,
    ) -> Dict[str, Any]:
        """
        Simulate a fill WITHOUT actually modifying.
        
        Per spec: Simulation de remplissage (no write)
        """
        # Store simulation (temporary, not persisted)
        self._simulated_fills[slot_id] = simulated_value
        
        # Temporarily update visual (in memory only)
        node = scene.get_node(f"node_{slot_id}")
        if node:
            # Show as yellow (filled but not validated)
            node.color = XRColor.YELLOW.value
        
        return {
            "slot_id": slot_id,
            "simulated_value": simulated_value,
            "is_simulation": True,
            "warning": "This is a READ-ONLY simulation. No actual changes made.",
        }
    
    def clear_simulation(
        self,
        scene: XRScene,
        slot_id: str,
        original_status: SlotStatus,
    ) -> None:
        """Clear a simulation and restore original state"""
        if slot_id in self._simulated_fills:
            del self._simulated_fills[slot_id]
        
        node = scene.get_node(f"node_{slot_id}")
        if node:
            node.color = status_to_color(original_status)
    
    def get_validation_request(
        self,
        slot_id: str,
    ) -> Dict[str, Any]:
        """
        Generate a validation request for HITL.
        
        Per spec: Validation humaine en XR (read-only décisionnel)
        
        NOTE: XR cannot validate directly. It generates a REQUEST
        that must be processed by the backend.
        """
        return {
            "type": "hitl_validation_request",
            "slot_id": slot_id,
            "requested_from": "xr_interface",
            "timestamp": datetime.utcnow().isoformat(),
            "note": "XR is READ-ONLY. This request must be processed by backend.",
        }


# ============================================================================
# XR ARTIFACT GENERATOR
# ============================================================================

class XRSlotFillArtifact:
    """
    Generate XR artifacts for slot fill visualization.
    
    Per spec use cases:
    - Audits complexes
    - Documents légaux
    - Backlog → blueprint review
    """
    
    def __init__(self):
        self.builder = XRSceneBuilder()
    
    def generate_artifact(
        self,
        document: Document,
    ) -> Dict[str, Any]:
        """Generate complete XR artifact for document"""
        scene = self.builder.build_scene(document)
        
        # Generate statistics
        stats = self._compute_stats(document)
        
        return {
            "artifact_type": "xr_slot_fill_visualization",
            "schema_version": "v1",
            "document_id": document.document_id,
            "document_name": document.name,
            "scene": scene.to_dict(),
            "statistics": stats,
            "governance": {
                "read_only": True,
                "opa_rule": "XR_READ_ONLY",
                "no_modifications_allowed": True,
            },
            "generated_at": datetime.utcnow().isoformat(),
        }
    
    def _compute_stats(self, document: Document) -> Dict[str, Any]:
        """Compute visualization statistics"""
        slots = list(document.slots.values())
        
        status_counts = {}
        for slot in slots:
            status = slot.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_slots": len(slots),
            "status_breakdown": status_counts,
            "completion_percentage": document.completion_percentage,
            "blocked_count": document.blocked_slots,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_scene_builder(
    layout: LayoutStrategy = LayoutStrategy.CIRCULAR,
) -> XRSceneBuilder:
    """Create an XR scene builder"""
    return XRSceneBuilder(layout)


def create_interaction_handler() -> XRInteractionHandler:
    """Create an XR interaction handler"""
    return XRInteractionHandler()


def create_artifact_generator() -> XRSlotFillArtifact:
    """Create an XR artifact generator"""
    return XRSlotFillArtifact()
