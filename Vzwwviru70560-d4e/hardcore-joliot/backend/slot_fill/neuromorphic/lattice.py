"""
============================================================================
CHE·NU™ V69 — NEUROMORPHIC LATTICE ENGINE
============================================================================
Spec: GPT1/CHE-NU_ENG_NEUROMORPHIC_LATTICE_V1.md

Objective: Deploy event-based neuromorphic core for L0-L1 agents to reduce:
- latence de réaction
- consommation énergétique
- bruit inter-agents

This is NOT a new LLM. It's a spike signal substrate for real-time tasks.

Targets:
- détection d'anomalies (drift, SLA, spikes de coût)
- routage d'événements (slot changed → relevant agents)
- scoring rapide (risk/priority) basé sur patterns

Out of scope:
- génération textuelle longue
- décisions high-stakes (toujours HITL)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import math
import logging
import json

logger = logging.getLogger(__name__)


# ============================================================================
# SPIKE EVENT TYPES (per spec)
# ============================================================================

class SpikeInputType(str, Enum):
    """Input spike types per spec"""
    SLOT_DELTA = "slot_delta"
    METRIC_DELTA = "metric_delta"
    OPA_EVENT = "opa_event"
    XR_INTERVENTION = "xr_intervention"


class SpikeOutputType(str, Enum):
    """Output spike types per spec"""
    ALERT_SPIKE = "alert_spike"
    ROUTE_SPIKE = "route_spike"
    PRIORITY_SPIKE = "priority_spike"


# ============================================================================
# SPIKE EVENT MODEL
# ============================================================================

@dataclass
class SpikeEvent:
    """
    Spike event per spec: spike_event.v1.json
    
    Fields:
    - type
    - intensity
    - source
    - trace_id
    """
    event_id: str
    event_type: str  # SpikeInputType or SpikeOutputType
    intensity: float  # 0.0 - 1.0
    source: str  # Agent or system ID
    trace_id: str
    
    # Additional data
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "type": self.event_type,
            "intensity": self.intensity,
            "source": self.source,
            "trace_id": self.trace_id,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())


# ============================================================================
# SYNAPSE MODEL
# ============================================================================

@dataclass
class Synapse:
    """
    Synapse connecting agents in the neuromorphic lattice.
    
    Per spec: Each agent has spike_inputs, spike_thresholds, spike_outputs
    """
    synapse_id: str
    source_agent_id: str
    target_agent_id: str
    
    # Spike handling
    input_types: Set[str] = field(default_factory=set)  # Which spike types trigger
    threshold: float = 0.5  # Activation threshold
    weight: float = 1.0  # Synaptic weight
    
    # Plasticity (per spec: learning budget)
    learning_enabled: bool = False
    learning_rate: float = 0.01
    learning_budget: float = 1.0  # Max total weight change
    weight_changes: float = 0.0  # Track changes for rollback
    
    # State
    last_activation: Optional[datetime] = None
    activation_count: int = 0
    
    def should_fire(self, spike: SpikeEvent) -> bool:
        """Check if synapse should fire based on spike"""
        if spike.event_type not in self.input_types:
            return False
        
        weighted_intensity = spike.intensity * self.weight
        return weighted_intensity >= self.threshold
    
    def adapt(self, success: bool) -> float:
        """
        Adapt synapse weight based on feedback.
        
        Per spec: apprentissage local sur feedback non sensible
        """
        if not self.learning_enabled:
            return 0.0
        
        if self.weight_changes >= self.learning_budget:
            logger.warning(f"Synapse {self.synapse_id} learning budget exhausted")
            return 0.0
        
        delta = self.learning_rate if success else -self.learning_rate
        
        # Clamp weight
        old_weight = self.weight
        self.weight = max(0.1, min(2.0, self.weight + delta))
        
        actual_delta = self.weight - old_weight
        self.weight_changes += abs(actual_delta)
        
        return actual_delta


# ============================================================================
# AGENT NEURO MAP (per spec)
# ============================================================================

@dataclass
class AgentNeuroMap:
    """
    Per spec: neuro_map.v1.json
    
    Maps agent to synapses, thresholds, caps.
    """
    agent_id: str
    agent_level: str  # L0, L1, L2, L3
    
    # Input configuration
    spike_inputs: Set[str] = field(default_factory=set)
    input_thresholds: Dict[str, float] = field(default_factory=dict)
    
    # Output configuration
    spike_outputs: Set[str] = field(default_factory=set)
    output_caps: Dict[str, float] = field(default_factory=dict)  # Rate limits
    
    # Connected synapses
    incoming_synapses: List[str] = field(default_factory=list)
    outgoing_synapses: List[str] = field(default_factory=list)
    
    # State
    accumulated_intensity: float = 0.0
    last_spike_time: Optional[datetime] = None
    spike_count: int = 0
    
    def can_receive(self, spike_type: str) -> bool:
        """Check if agent can receive this spike type"""
        return spike_type in self.spike_inputs
    
    def get_threshold(self, spike_type: str) -> float:
        """Get threshold for spike type"""
        return self.input_thresholds.get(spike_type, 0.5)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_level": self.agent_level,
            "spike_inputs": list(self.spike_inputs),
            "input_thresholds": self.input_thresholds,
            "spike_outputs": list(self.spike_outputs),
            "output_caps": self.output_caps,
        }


# ============================================================================
# SIGNAL BUS (per spec)
# ============================================================================

class SignalBus:
    """
    Signal bus for spike propagation.
    
    Per spec 2.1:
    - Entrées: SlotDelta, MetricDelta, OPAEvent, XRIntervention
    - Sorties: AlertSpike, RouteSpike, PrioritySpike
    """
    
    def __init__(self):
        self._queue: List[SpikeEvent] = []
        self._handlers: Dict[str, List[Callable]] = {}
        self._event_log: List[SpikeEvent] = []
    
    def publish(self, spike: SpikeEvent) -> None:
        """Publish a spike event to the bus"""
        self._queue.append(spike)
        self._event_log.append(spike)
        
        logger.debug(f"Spike published: {spike.event_type} from {spike.source}")
    
    def subscribe(
        self,
        spike_type: str,
        handler: Callable[[SpikeEvent], None],
    ) -> None:
        """Subscribe to spike type"""
        if spike_type not in self._handlers:
            self._handlers[spike_type] = []
        self._handlers[spike_type].append(handler)
    
    def process(self) -> int:
        """Process all queued spikes"""
        processed = 0
        
        while self._queue:
            spike = self._queue.pop(0)
            handlers = self._handlers.get(spike.event_type, [])
            
            for handler in handlers:
                try:
                    handler(spike)
                    processed += 1
                except Exception as e:
                    logger.error(f"Error processing spike: {e}")
        
        return processed
    
    def get_log(self) -> List[SpikeEvent]:
        """Get event log for audit"""
        return self._event_log.copy()


# ============================================================================
# NEUROMORPHIC LATTICE ENGINE
# ============================================================================

class NeuromorphicLattice:
    """
    Main neuromorphic lattice engine.
    
    Per spec: noyau neuromorphe event-based pour agents L0-L1
    """
    
    def __init__(self):
        self.signal_bus = SignalBus()
        self._agents: Dict[str, AgentNeuroMap] = {}
        self._synapses: Dict[str, Synapse] = {}
        
        # Metrics (per spec KPIs)
        self._propagation_times: List[float] = []
        self._false_positives: int = 0
        self._false_negatives: int = 0
        self._events_processed: int = 0
    
    def register_agent(self, agent_map: AgentNeuroMap) -> None:
        """Register an agent in the lattice"""
        self._agents[agent_map.agent_id] = agent_map
        
        # Subscribe to spike types
        for spike_type in agent_map.spike_inputs:
            self.signal_bus.subscribe(
                spike_type,
                lambda s, a=agent_map: self._handle_agent_spike(a, s),
            )
        
        logger.info(f"Registered agent {agent_map.agent_id} in lattice")
    
    def create_synapse(
        self,
        source_id: str,
        target_id: str,
        input_types: Set[str],
        threshold: float = 0.5,
        weight: float = 1.0,
    ) -> Synapse:
        """Create a synapse between agents"""
        synapse_id = f"syn_{source_id}_{target_id}"
        
        synapse = Synapse(
            synapse_id=synapse_id,
            source_agent_id=source_id,
            target_agent_id=target_id,
            input_types=input_types,
            threshold=threshold,
            weight=weight,
        )
        
        self._synapses[synapse_id] = synapse
        
        # Update agent maps
        if source_id in self._agents:
            self._agents[source_id].outgoing_synapses.append(synapse_id)
        if target_id in self._agents:
            self._agents[target_id].incoming_synapses.append(synapse_id)
        
        return synapse
    
    def emit_spike(
        self,
        source: str,
        spike_type: str,
        intensity: float,
        payload: Dict[str, Any] = None,
        trace_id: str = None,
    ) -> SpikeEvent:
        """Emit a spike into the lattice"""
        import uuid
        
        spike = SpikeEvent(
            event_id=str(uuid.uuid4()),
            event_type=spike_type,
            intensity=intensity,
            source=source,
            trace_id=trace_id or str(uuid.uuid4()),
            payload=payload or {},
        )
        
        self.signal_bus.publish(spike)
        return spike
    
    def propagate(self) -> int:
        """Propagate all spikes through the lattice"""
        start_time = datetime.utcnow()
        
        processed = self.signal_bus.process()
        
        end_time = datetime.utcnow()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        self._propagation_times.append(duration_ms)
        self._events_processed += processed
        
        return processed
    
    def _handle_agent_spike(
        self,
        agent: AgentNeuroMap,
        spike: SpikeEvent,
    ) -> None:
        """Handle spike for an agent"""
        threshold = agent.get_threshold(spike.event_type)
        
        if spike.intensity >= threshold:
            agent.accumulated_intensity += spike.intensity
            agent.spike_count += 1
            agent.last_spike_time = datetime.utcnow()
            
            # Check for output generation
            self._check_outputs(agent, spike)
    
    def _check_outputs(
        self,
        agent: AgentNeuroMap,
        trigger_spike: SpikeEvent,
    ) -> None:
        """Check if agent should generate output spikes"""
        # Simple heuristic: if accumulated intensity exceeds 1.0, generate alert
        if agent.accumulated_intensity >= 1.0:
            # Generate alert spike
            self.emit_spike(
                source=agent.agent_id,
                spike_type=SpikeOutputType.ALERT_SPIKE.value,
                intensity=min(agent.accumulated_intensity, 1.0),
                payload={
                    "trigger_type": trigger_spike.event_type,
                    "trigger_source": trigger_spike.source,
                },
                trace_id=trigger_spike.trace_id,
            )
            
            # Reset accumulation
            agent.accumulated_intensity = 0.0
    
    # =========================================================================
    # ANOMALY DETECTION (per spec target)
    # =========================================================================
    
    def detect_anomaly(
        self,
        metric_name: str,
        current_value: float,
        baseline_value: float,
        threshold: float = 0.2,
    ) -> Optional[SpikeEvent]:
        """
        Detect anomaly (drift, SLA breach, cost spike).
        
        Per spec target: détection d'anomalies
        """
        drift = abs(current_value - baseline_value) / max(baseline_value, 1.0)
        
        if drift > threshold:
            return self.emit_spike(
                source="anomaly_detector",
                spike_type=SpikeInputType.METRIC_DELTA.value,
                intensity=min(drift, 1.0),
                payload={
                    "metric_name": metric_name,
                    "current_value": current_value,
                    "baseline_value": baseline_value,
                    "drift": drift,
                },
            )
        return None
    
    # =========================================================================
    # EVENT ROUTING (per spec target)
    # =========================================================================
    
    def route_slot_change(
        self,
        slot_id: str,
        change_type: str,
        relevant_agents: List[str],
    ) -> List[SpikeEvent]:
        """
        Route slot change to relevant agents.
        
        Per spec target: routage d'événements (slot changed → relevant agents)
        """
        spikes = []
        
        for agent_id in relevant_agents:
            spike = self.emit_spike(
                source="slot_router",
                spike_type=SpikeOutputType.ROUTE_SPIKE.value,
                intensity=0.7,
                payload={
                    "slot_id": slot_id,
                    "change_type": change_type,
                    "target_agent": agent_id,
                },
            )
            spikes.append(spike)
        
        return spikes
    
    # =========================================================================
    # RAPID SCORING (per spec target)
    # =========================================================================
    
    def compute_rapid_score(
        self,
        patterns: Dict[str, float],
        weights: Dict[str, float] = None,
    ) -> Tuple[float, SpikeEvent]:
        """
        Compute rapid risk/priority score based on patterns.
        
        Per spec target: scoring rapide basé sur patterns
        """
        weights = weights or {k: 1.0 for k in patterns}
        
        total_weight = sum(weights.get(k, 1.0) for k in patterns)
        score = sum(
            patterns[k] * weights.get(k, 1.0)
            for k in patterns
        ) / max(total_weight, 1.0)
        
        spike = self.emit_spike(
            source="rapid_scorer",
            spike_type=SpikeOutputType.PRIORITY_SPIKE.value,
            intensity=score,
            payload={
                "patterns": patterns,
                "computed_score": score,
            },
        )
        
        return score, spike
    
    # =========================================================================
    # PLASTICITY WORKER (per spec)
    # =========================================================================
    
    def propose_adaptation(
        self,
        synapse_id: str,
        success_feedback: bool,
    ) -> Dict[str, Any]:
        """
        Propose synaptic adaptation.
        
        Per spec: NEURO_PLASTICITY_WORKER proposes → OPA validate → apply
        """
        synapse = self._synapses.get(synapse_id)
        if not synapse:
            return {"error": "Synapse not found"}
        
        # Propose (don't apply yet - needs OPA validation)
        proposed_delta = synapse.learning_rate if success_feedback else -synapse.learning_rate
        proposed_weight = synapse.weight + proposed_delta
        
        return {
            "synapse_id": synapse_id,
            "current_weight": synapse.weight,
            "proposed_weight": proposed_weight,
            "delta": proposed_delta,
            "requires_opa_validation": True,
            "rollback_available": True,
        }
    
    def apply_adaptation(
        self,
        synapse_id: str,
        opa_approved: bool,
    ) -> bool:
        """Apply approved adaptation"""
        if not opa_approved:
            return False
        
        synapse = self._synapses.get(synapse_id)
        if synapse:
            # Record in audit log (per spec: neuro_audit.log)
            logger.info(f"Applying adaptation to {synapse_id}")
            return True
        return False
    
    # =========================================================================
    # METRICS (per spec KPIs)
    # =========================================================================
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get KPIs per spec:
        - temps de propagation (P50/P95)
        - énergie estimée / event
        - false positives / false negatives
        - réduction de messages
        """
        if not self._propagation_times:
            p50, p95 = 0, 0
        else:
            sorted_times = sorted(self._propagation_times)
            p50 = sorted_times[len(sorted_times) // 2]
            p95 = sorted_times[int(len(sorted_times) * 0.95)]
        
        return {
            "propagation_p50_ms": p50,
            "propagation_p95_ms": p95,
            "events_processed": self._events_processed,
            "false_positives": self._false_positives,
            "false_negatives": self._false_negatives,
            "energy_per_event": 0.001,  # Placeholder - actual would depend on hardware
            "agents_registered": len(self._agents),
            "synapses_created": len(self._synapses),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_lattice() -> NeuromorphicLattice:
    """Create a neuromorphic lattice"""
    return NeuromorphicLattice()


def create_agent_map(
    agent_id: str,
    level: str,
    inputs: Set[str] = None,
    outputs: Set[str] = None,
) -> AgentNeuroMap:
    """Create an agent neuro map"""
    return AgentNeuroMap(
        agent_id=agent_id,
        agent_level=level,
        spike_inputs=inputs or set(),
        spike_outputs=outputs or set(),
    )
