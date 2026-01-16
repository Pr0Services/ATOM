"""
CHE·NU™ — Synaptic Graph (Inter-Module Connections)
===================================================
Defines the edges between modules with:
- Priority levels (P0, P1, P2, P3)
- Triggers (what causes the edge to fire)
- Actions (what happens when edge fires)
- Anti-loop protection (ttl, rate-limit, stability guards)

This is the neural network of CHE·NU™.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Set, Callable, Awaitable
from enum import Enum
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import asyncio
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class Priority(str, Enum):
    """Edge priority levels"""
    P0 = "P0"  # Critical - Governance, Security
    P1 = "P1"  # High - Core computation, Infrastructure
    P2 = "P2"  # Medium - Business logic, User flows
    P3 = "P3"  # Low - Nice-to-have, Enhancements


class ModuleID(str, Enum):
    """All CHE·NU modules"""
    # Governance
    MOD_01_OPA = "MOD_01_OPA"
    
    # Core Engine
    MOD_03_CAUSAL = "MOD_03_CAUSAL"
    MOD_04_WORLDENGINE = "MOD_04_WORLDENGINE"
    
    # Interface
    MOD_06_XR = "MOD_06_XR"
    
    # Bio/Hardware
    MOD_11_NEURO = "MOD_11_NEURO"
    MOD_13_MATTER = "MOD_13_MATTER"
    
    # Business
    MOD_17_GENESIS = "MOD_17_GENESIS"
    MOD_18_AGORA = "MOD_18_AGORA"
    
    # Knowledge
    MOD_19_CHRONOS = "MOD_19_CHRONOS"
    MOD_20_LIBRARY = "MOD_20_LIBRARY"
    MOD_21_EDU = "MOD_21_EDU"
    
    # Orchestration
    MOD_22_ORCH = "MOD_22_ORCH"
    
    # Community
    MOD_23_COMMUNITY = "MOD_23_COMMUNITY"
    MOD_24_RESONANCE = "MOD_24_RESONANCE"
    
    # Dashboard
    MOD_25_SYNAPTIC_DASH = "MOD_25_SYNAPTIC_DASH"
    
    # Infrastructure
    MOD_QP_PHOTONIC = "MOD_QP_PHOTONIC"


@dataclass
class EdgeTrigger:
    """Trigger that activates an edge"""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }


@dataclass
class EdgeAction:
    """Action executed when edge fires"""
    name: str
    description: str
    handler: Optional[str] = None  # Function name to call
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "handler": self.handler
        }


@dataclass
class StabilityGuard:
    """Prevents edge loops and cascades"""
    max_fires_per_minute: int = 10
    cooldown_seconds: int = 5
    derivative_threshold: float = 0.5  # Rate of change threshold
    enabled: bool = True


@dataclass
class SynapticEdge:
    """A connection between two modules"""
    edge_id: UUID = field(default_factory=uuid4)
    source: ModuleID = None
    target: ModuleID = None
    priority: Priority = Priority.P2
    trigger: EdgeTrigger = None
    action: EdgeAction = None
    stability_guard: StabilityGuard = field(default_factory=StabilityGuard)
    
    # Runtime state
    fire_count: int = 0
    last_fired: Optional[datetime] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge_id": str(self.edge_id),
            "source": self.source.value if self.source else None,
            "target": self.target.value if self.target else None,
            "priority": self.priority.value,
            "trigger": self.trigger.to_dict() if self.trigger else None,
            "action": self.action.to_dict() if self.action else None,
            "fire_count": self.fire_count,
            "last_fired": self.last_fired.isoformat() if self.last_fired else None,
            "is_active": self.is_active
        }
    
    def can_fire(self) -> bool:
        """Check if edge can fire (respects stability guard)"""
        if not self.is_active:
            return False
        
        if not self.stability_guard.enabled:
            return True
        
        if self.last_fired is None:
            return True
        
        # Check cooldown
        elapsed = (datetime.utcnow() - self.last_fired).total_seconds()
        if elapsed < self.stability_guard.cooldown_seconds:
            return False
        
        return True
    
    def fire(self) -> None:
        """Record edge firing"""
        self.fire_count += 1
        self.last_fired = datetime.utcnow()


@dataclass
class EdgeFireEvent:
    """Event emitted when edge fires"""
    event_id: UUID = field(default_factory=uuid4)
    edge_id: UUID = None
    source: ModuleID = None
    target: ModuleID = None
    trigger_name: str = ""
    action_name: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class SynapticGraph:
    """
    The neural network of CHE·NU™.
    
    Manages connections between modules and routes signals
    while preventing infinite loops and cascades.
    """
    
    def __init__(self):
        # All edges
        self._edges: Dict[UUID, SynapticEdge] = {}
        
        # Index: source -> [edges]
        self._outgoing: Dict[ModuleID, List[SynapticEdge]] = defaultdict(list)
        
        # Index: target -> [edges]
        self._incoming: Dict[ModuleID, List[SynapticEdge]] = defaultdict(list)
        
        # Edge handlers
        self._handlers: Dict[str, Callable[[EdgeFireEvent], Awaitable[Any]]] = {}
        
        # Event listeners
        self._listeners: List[Callable[[EdgeFireEvent], Awaitable[None]]] = []
        
        # Loop detection
        self._active_paths: Set[str] = set()
        
        # Initialize default graph
        self._init_default_edges()
    
    def _init_default_edges(self) -> None:
        """Initialize the canonical CHE·NU synaptic graph"""
        
        # P0: Governance edges (Critical)
        self.add_edge(
            source=ModuleID.MOD_01_OPA,
            target=ModuleID.MOD_22_ORCH,
            priority=Priority.P0,
            trigger=EdgeTrigger("PolicyCheck", "Autoriser/refuser actions"),
            action=EdgeAction("enforce_policy", "Apply governance decision")
        )
        
        self.add_edge(
            source=ModuleID.MOD_01_OPA,
            target=ModuleID.MOD_04_WORLDENGINE,
            priority=Priority.P0,
            trigger=EdgeTrigger("PolicySeal", "Signer/valider snapshots"),
            action=EdgeAction("seal_snapshot", "Sign world state")
        )
        
        # P1: Core computation edges
        self.add_edge(
            source=ModuleID.MOD_03_CAUSAL,
            target=ModuleID.MOD_04_WORLDENGINE,
            priority=Priority.P1,
            trigger=EdgeTrigger("ModelCompile", "Produire règles causales exécutables"),
            action=EdgeAction("compile_rules", "Generate executable causal rules")
        )
        
        self.add_edge(
            source=ModuleID.MOD_04_WORLDENGINE,
            target=ModuleID.MOD_03_CAUSAL,
            priority=Priority.P1,
            trigger=EdgeTrigger("ExplainWhy", "Retour preuve/why graph"),
            action=EdgeAction("explain_causality", "Return causal proof")
        )
        
        self.add_edge(
            source=ModuleID.MOD_04_WORLDENGINE,
            target=ModuleID.MOD_18_AGORA,
            priority=Priority.P1,
            trigger=EdgeTrigger("RiskAlert", "Session urgence + preuve"),
            action=EdgeAction("trigger_emergency", "Start emergency session with proof")
        )
        
        # P1: Quantum/Photonic infrastructure
        self.add_edge(
            source=ModuleID.MOD_QP_PHOTONIC,
            target=ModuleID.MOD_22_ORCH,
            priority=Priority.P1,
            trigger=EdgeTrigger("SecureChannel", "QKD/keys/latence"),
            action=EdgeAction("establish_secure", "Setup quantum-secure channel")
        )
        
        self.add_edge(
            source=ModuleID.MOD_QP_PHOTONIC,
            target=ModuleID.MOD_04_WORLDENGINE,
            priority=Priority.P1,
            trigger=EdgeTrigger("AccelCompute", "Accélération photonic/edge"),
            action=EdgeAction("accelerate", "Photonic compute acceleration")
        )
        
        # P2: User interface edges
        self.add_edge(
            source=ModuleID.MOD_04_WORLDENGINE,
            target=ModuleID.MOD_06_XR,
            priority=Priority.P2,
            trigger=EdgeTrigger("StreamState", "Streamer états & artifacts"),
            action=EdgeAction("stream_to_xr", "Stream state to XR renderer")
        )
        
        self.add_edge(
            source=ModuleID.MOD_06_XR,
            target=ModuleID.MOD_22_ORCH,
            priority=Priority.P2,
            trigger=EdgeTrigger("UserIntent", "Envoyer intent/gestes"),
            action=EdgeAction("process_intent", "Process user intent from XR")
        )
        
        # P2: Business edges
        self.add_edge(
            source=ModuleID.MOD_18_AGORA,
            target=ModuleID.MOD_17_GENESIS,
            priority=Priority.P2,
            trigger=EdgeTrigger("Consensus>80%", "Créer projet/contrats"),
            action=EdgeAction("create_project", "Create project from consensus")
        )
        
        self.add_edge(
            source=ModuleID.MOD_18_AGORA,
            target=ModuleID.MOD_04_WORLDENGINE,
            priority=Priority.P2,
            trigger=EdgeTrigger("NewProposal", "Simuler impact 10 ans"),
            action=EdgeAction("simulate_impact", "Run 10-year impact simulation")
        )
        
        self.add_edge(
            source=ModuleID.MOD_17_GENESIS,
            target=ModuleID.MOD_21_EDU,
            priority=Priority.P2,
            trigger=EdgeTrigger("SkillGapDetected", "Générer parcours JIT"),
            action=EdgeAction("create_learning_path", "Generate just-in-time learning")
        )
        
        self.add_edge(
            source=ModuleID.MOD_21_EDU,
            target=ModuleID.MOD_17_GENESIS,
            priority=Priority.P2,
            trigger=EdgeTrigger("FieldReadyBadge", "Débloquer missions"),
            action=EdgeAction("unlock_missions", "Unlock task missions")
        )
        
        # P2: Community edges
        self.add_edge(
            source=ModuleID.MOD_23_COMMUNITY,
            target=ModuleID.MOD_17_GENESIS,
            priority=Priority.P2,
            trigger=EdgeTrigger("NeedsHeatmap", "Ouvrir projets depuis besoins"),
            action=EdgeAction("open_projects", "Create projects from community needs")
        )
        
        self.add_edge(
            source=ModuleID.MOD_17_GENESIS,
            target=ModuleID.MOD_23_COMMUNITY,
            priority=Priority.P2,
            trigger=EdgeTrigger("EquityTelemetry", "Publier metrics & dividendes"),
            action=EdgeAction("publish_metrics", "Publish equity metrics")
        )
        
        self.add_edge(
            source=ModuleID.MOD_23_COMMUNITY,
            target=ModuleID.MOD_18_AGORA,
            priority=Priority.P2,
            trigger=EdgeTrigger("ScenarioVote", "Déclencher votes sur scénarios"),
            action=EdgeAction("start_vote", "Initiate scenario voting")
        )
        
        # P2: Resonance/Ambient edges
        self.add_edge(
            source=ModuleID.MOD_11_NEURO,
            target=ModuleID.MOD_24_RESONANCE,
            priority=Priority.P2,
            trigger=EdgeTrigger("StressIndex", "Nudge ambiance & priorités"),
            action=EdgeAction("adjust_ambient", "Adjust ambient based on stress")
        )
        
        self.add_edge(
            source=ModuleID.MOD_24_RESONANCE,
            target=ModuleID.MOD_13_MATTER,
            priority=Priority.P2,
            trigger=EdgeTrigger("AestheticNudge", "Adapter textures/couleurs"),
            action=EdgeAction("adjust_aesthetics", "Modify physical aesthetics")
        )
        
        self.add_edge(
            source=ModuleID.MOD_24_RESONANCE,
            target=ModuleID.MOD_17_GENESIS,
            priority=Priority.P2,
            trigger=EdgeTrigger("PriorityNudge", "Ajuster priorités non critiques"),
            action=EdgeAction("adjust_priorities", "Modify task priorities")
        )
        
        # P2: Dashboard edges
        self.add_edge(
            source=ModuleID.MOD_22_ORCH,
            target=ModuleID.MOD_25_SYNAPTIC_DASH,
            priority=Priority.P2,
            trigger=EdgeTrigger("ContextCapsule", "Mettre à jour 3 hubs"),
            action=EdgeAction("update_dashboard", "Sync dashboard with context")
        )
        
        # P3: Knowledge edges
        self.add_edge(
            source=ModuleID.MOD_20_LIBRARY,
            target=ModuleID.MOD_21_EDU,
            priority=Priority.P3,
            trigger=EdgeTrigger("ContentToCourse", "Transformer contenu en micro-learning"),
            action=EdgeAction("create_course", "Generate micro-learning from content")
        )
        
        self.add_edge(
            source=ModuleID.MOD_21_EDU,
            target=ModuleID.MOD_20_LIBRARY,
            priority=Priority.P3,
            trigger=EdgeTrigger("PublishTutorial", "Publier tutoriels validés"),
            action=EdgeAction("publish_tutorial", "Publish validated tutorials")
        )
        
        self.add_edge(
            source=ModuleID.MOD_19_CHRONOS,
            target=ModuleID.MOD_17_GENESIS,
            priority=Priority.P3,
            trigger=EdgeTrigger("CulturalContinuity", "Injecter références/contraintes"),
            action=EdgeAction("inject_context", "Add historical/cultural context")
        )
        
        self.add_edge(
            source=ModuleID.MOD_17_GENESIS,
            target=ModuleID.MOD_19_CHRONOS,
            priority=Priority.P3,
            trigger=EdgeTrigger("LogArtifacts", "Archiver récit & versions"),
            action=EdgeAction("archive_story", "Archive narrative and versions")
        )
        
        self.add_edge(
            source=ModuleID.MOD_25_SYNAPTIC_DASH,
            target=ModuleID.MOD_22_ORCH,
            priority=Priority.P3,
            trigger=EdgeTrigger("DensitySlider", "Négocier densité UI"),
            action=EdgeAction("adjust_density", "Modify UI information density")
        )
    
    def add_edge(
        self,
        source: ModuleID,
        target: ModuleID,
        priority: Priority,
        trigger: EdgeTrigger,
        action: EdgeAction,
        stability_guard: Optional[StabilityGuard] = None
    ) -> SynapticEdge:
        """Add an edge to the graph"""
        edge = SynapticEdge(
            source=source,
            target=target,
            priority=priority,
            trigger=trigger,
            action=action,
            stability_guard=stability_guard or StabilityGuard()
        )
        
        self._edges[edge.edge_id] = edge
        self._outgoing[source].append(edge)
        self._incoming[target].append(edge)
        
        logger.debug(f"Added edge: {source.value} -> {target.value} ({trigger.name})")
        
        return edge
    
    def register_handler(
        self, 
        action_name: str, 
        handler: Callable[[EdgeFireEvent], Awaitable[Any]]
    ) -> None:
        """Register handler for edge action"""
        self._handlers[action_name] = handler
    
    def add_listener(self, listener: Callable[[EdgeFireEvent], Awaitable[None]]) -> None:
        """Add listener for all edge fires"""
        self._listeners.append(listener)
    
    def get_outgoing_edges(self, module: ModuleID) -> List[SynapticEdge]:
        """Get all edges originating from module"""
        return self._outgoing.get(module, [])
    
    def get_incoming_edges(self, module: ModuleID) -> List[SynapticEdge]:
        """Get all edges targeting module"""
        return self._incoming.get(module, [])
    
    def get_edges_by_priority(self, priority: Priority) -> List[SynapticEdge]:
        """Get all edges with specific priority"""
        return [e for e in self._edges.values() if e.priority == priority]
    
    def _check_loop(self, source: ModuleID, target: ModuleID) -> bool:
        """Check if firing would create a loop"""
        path_key = f"{source.value}->{target.value}"
        
        if path_key in self._active_paths:
            logger.warning(f"Loop detected: {path_key}")
            return True
        
        return False
    
    async def fire_edge(
        self,
        edge_id: UUID,
        payload: Dict[str, Any] = None
    ) -> Optional[Any]:
        """Fire a specific edge"""
        edge = self._edges.get(edge_id)
        if not edge:
            logger.error(f"Edge not found: {edge_id}")
            return None
        
        return await self._fire(edge, payload or {})
    
    async def fire_trigger(
        self,
        source: ModuleID,
        trigger_name: str,
        payload: Dict[str, Any] = None
    ) -> List[Any]:
        """Fire all edges from source with matching trigger"""
        results = []
        
        for edge in self._outgoing.get(source, []):
            if edge.trigger and edge.trigger.name == trigger_name:
                result = await self._fire(edge, payload or {})
                if result is not None:
                    results.append(result)
        
        return results
    
    async def _fire(
        self,
        edge: SynapticEdge,
        payload: Dict[str, Any]
    ) -> Optional[Any]:
        """Internal fire implementation"""
        
        # Check if can fire
        if not edge.can_fire():
            logger.debug(f"Edge {edge.edge_id} cannot fire (cooldown)")
            return None
        
        # Check for loops
        if self._check_loop(edge.source, edge.target):
            return None
        
        # Mark path as active
        path_key = f"{edge.source.value}->{edge.target.value}"
        self._active_paths.add(path_key)
        
        try:
            # Create event
            event = EdgeFireEvent(
                edge_id=edge.edge_id,
                source=edge.source,
                target=edge.target,
                trigger_name=edge.trigger.name if edge.trigger else "",
                action_name=edge.action.name if edge.action else "",
                payload=payload
            )
            
            # Record firing
            edge.fire()
            
            logger.info(
                f"Edge fired: {edge.source.value} -> {edge.target.value} "
                f"({edge.trigger.name if edge.trigger else 'no trigger'})"
            )
            
            # Notify listeners
            for listener in self._listeners:
                try:
                    await listener(event)
                except Exception as e:
                    logger.error(f"Listener error: {e}")
            
            # Execute handler
            result = None
            if edge.action and edge.action.handler:
                handler = self._handlers.get(edge.action.handler)
                if handler:
                    result = await handler(event)
                else:
                    logger.warning(f"No handler for action: {edge.action.handler}")
            
            return result
            
        finally:
            # Clear path
            self._active_paths.discard(path_key)
    
    def get_graph_summary(self) -> Dict[str, Any]:
        """Get summary of the graph"""
        return {
            "total_edges": len(self._edges),
            "by_priority": {
                p.value: len(self.get_edges_by_priority(p))
                for p in Priority
            },
            "modules": {
                m.value: {
                    "outgoing": len(self._outgoing.get(m, [])),
                    "incoming": len(self._incoming.get(m, []))
                }
                for m in ModuleID
            },
            "active_paths": list(self._active_paths)
        }
    
    def export_edge_list(self) -> List[Dict[str, str]]:
        """Export edges as list for machine processing"""
        return [
            {
                "from": e.source.value,
                "to": e.target.value,
                "priority": e.priority.value,
                "trigger": e.trigger.name if e.trigger else "",
                "action": e.action.description if e.action else ""
            }
            for e in self._edges.values()
        ]
    
    def export_mermaid(self) -> str:
        """Export graph as Mermaid diagram"""
        lines = ["graph TD"]
        
        # Add nodes
        for m in ModuleID:
            lines.append(f'  {m.value}["{m.value}"]')
        
        # Add edges
        for edge in self._edges.values():
            label = edge.trigger.name if edge.trigger else ""
            lines.append(
                f'  {edge.source.value} -->|{edge.priority.value}: {label}| {edge.target.value}'
            )
        
        return "\n".join(lines)


# Singleton instance
_graph: Optional[SynapticGraph] = None

def get_synaptic_graph() -> SynapticGraph:
    """Get singleton graph instance"""
    global _graph
    if _graph is None:
        _graph = SynapticGraph()
    return _graph
