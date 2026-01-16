"""
============================================================================
CHE·NU™ V69 — NEUROMORPHIC LATTICE (Module 11)
============================================================================
Spec: CHE-NU_ENG_NEUROMORPHIC_LATTICE_V1.md

Objectif: Déployer un noyau neuromorphe event-based pour agents L0-L1
- Réduction latence
- Réduction consommation énergétique
- Réduction bruit inter-agents

"Ce module n'est pas un nouveau LLM. C'est un substrat de signal (spikes)."
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging

from ..models import (
    SpikeType, SpikeEvent, Synapse, NeuroMap,
    generate_id, compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# SPIKE BUS
# ============================================================================

class SpikeBus:
    """
    Signal bus for spike events.
    
    Per spec: Entrées/Sorties - SlotDelta, MetricDelta, OPAEvent, etc.
    """
    
    def __init__(self):
        self._events: List[SpikeEvent] = []
        self._subscribers: Dict[SpikeType, List[callable]] = {}
    
    def emit(self, event: SpikeEvent) -> None:
        """Emit a spike event"""
        self._events.append(event)
        
        # Notify subscribers
        handlers = self._subscribers.get(event.spike_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Spike handler error: {e}")
        
        logger.debug(f"Spike emitted: {event.spike_type.value} intensity={event.intensity}")
    
    def subscribe(self, spike_type: SpikeType, handler: callable) -> None:
        """Subscribe to spike type"""
        if spike_type not in self._subscribers:
            self._subscribers[spike_type] = []
        self._subscribers[spike_type].append(handler)
    
    def get_recent(self, n: int = 100) -> List[SpikeEvent]:
        """Get recent events"""
        return self._events[-n:]


# ============================================================================
# AGENT SYNAPSE MAPPING
# ============================================================================

class SynapseMapper:
    """
    Map 287 agents to synapses.
    
    Per spec: Each agent has spike_inputs, spike_thresholds, spike_outputs
    """
    
    def __init__(self):
        self._synapses: Dict[str, Synapse] = {}
        self._agent_synapses: Dict[str, List[str]] = {}  # agent -> synapse ids
    
    def create_synapse(
        self,
        source_agent: str,
        target_agent: str,
        threshold: float = 0.5,
        inputs: List[SpikeType] = None,
        outputs: List[SpikeType] = None,
    ) -> Synapse:
        """Create a synapse between agents"""
        synapse = Synapse(
            synapse_id=generate_id(),
            source_agent=source_agent,
            target_agent=target_agent,
            threshold=threshold,
            spike_inputs=inputs or [],
            spike_outputs=outputs or [],
        )
        
        self._synapses[synapse.synapse_id] = synapse
        
        # Map to agents
        for agent in [source_agent, target_agent]:
            if agent not in self._agent_synapses:
                self._agent_synapses[agent] = []
            self._agent_synapses[agent].append(synapse.synapse_id)
        
        return synapse
    
    def get_agent_synapses(self, agent_id: str) -> List[Synapse]:
        """Get all synapses for an agent"""
        synapse_ids = self._agent_synapses.get(agent_id, [])
        return [self._synapses[sid] for sid in synapse_ids if sid in self._synapses]
    
    def export_neuro_map(self) -> NeuroMap:
        """Export as NeuroMap"""
        return NeuroMap(
            map_id=generate_id(),
            synapses=list(self._synapses.values()),
            thresholds={s.synapse_id: s.threshold for s in self._synapses.values()},
        )


# ============================================================================
# PLASTICITY WORKER
# ============================================================================

@dataclass
class PlasticityAdjustment:
    """Proposed threshold adjustment"""
    synapse_id: str
    old_threshold: float
    new_threshold: float
    reason: str
    opa_approved: bool = False


class PlasticityWorker:
    """
    NEURO_PLASTICITY_WORKER.
    
    Per spec: Proposes adjustments -> OPA validate -> apply
    """
    
    def __init__(self, mapper: SynapseMapper, learning_budget: float = 0.1):
        self.mapper = mapper
        self.learning_budget = learning_budget
        self._adjustments: List[PlasticityAdjustment] = []
        self._total_adjustment = 0.0
    
    def propose_adjustment(
        self,
        synapse_id: str,
        feedback_positive: bool,
        delta: float = 0.05,
    ) -> Optional[PlasticityAdjustment]:
        """
        Propose threshold adjustment based on feedback.
        
        Per spec: Learning on non-sensitive feedback with guard-rails
        """
        if synapse_id not in self.mapper._synapses:
            return None
        
        synapse = self.mapper._synapses[synapse_id]
        
        # Check learning budget
        if abs(self._total_adjustment) + delta > self.learning_budget:
            logger.warning("Learning budget exceeded")
            return None
        
        # Calculate new threshold
        direction = 1 if feedback_positive else -1
        new_threshold = max(0.1, min(0.9, synapse.threshold + direction * delta))
        
        adjustment = PlasticityAdjustment(
            synapse_id=synapse_id,
            old_threshold=synapse.threshold,
            new_threshold=new_threshold,
            reason="positive feedback" if feedback_positive else "negative feedback",
        )
        
        self._adjustments.append(adjustment)
        return adjustment
    
    def apply_adjustment(
        self,
        adjustment: PlasticityAdjustment,
        opa_approved: bool = True,
    ) -> bool:
        """Apply adjustment after OPA validation"""
        if not opa_approved:
            adjustment.opa_approved = False
            return False
        
        synapse = self.mapper._synapses.get(adjustment.synapse_id)
        if not synapse:
            return False
        
        synapse.threshold = adjustment.new_threshold
        adjustment.opa_approved = True
        self._total_adjustment += abs(adjustment.new_threshold - adjustment.old_threshold)
        
        logger.info(f"Applied plasticity: {adjustment.synapse_id} threshold {adjustment.old_threshold:.2f} -> {adjustment.new_threshold:.2f}")
        return True
    
    def rollback(self, adjustment: PlasticityAdjustment) -> bool:
        """Rollback an adjustment"""
        synapse = self.mapper._synapses.get(adjustment.synapse_id)
        if not synapse:
            return False
        
        synapse.threshold = adjustment.old_threshold
        self._total_adjustment -= abs(adjustment.new_threshold - adjustment.old_threshold)
        
        logger.info(f"Rolled back: {adjustment.synapse_id}")
        return True


# ============================================================================
# NEUROMORPHIC LATTICE SYSTEM
# ============================================================================

class NeuromorphicLattice:
    """
    Main Neuromorphic Lattice System.
    
    Per spec targets:
    - Détection d'anomalies (drift, SLA, spikes de coût)
    - Routage d'événements
    - Scoring rapide (risk/priority)
    """
    
    def __init__(self):
        self.bus = SpikeBus()
        self.mapper = SynapseMapper()
        self.plasticity = PlasticityWorker(self.mapper)
        
        # Metrics
        self._propagation_times: List[float] = []
        self._false_positives = 0
        self._false_negatives = 0
    
    def detect_anomaly(
        self,
        slot_id: str,
        current_value: float,
        expected_value: float,
        threshold: float = 0.2,
    ) -> Optional[SpikeEvent]:
        """
        Detect anomaly and emit spike.
        
        Per spec: Détection d'anomalies (drift, SLA, spikes de coût)
        """
        if expected_value == 0:
            delta = abs(current_value)
        else:
            delta = abs(current_value - expected_value) / abs(expected_value)
        
        if delta > threshold:
            intensity = min(1.0, delta / threshold)
            
            event = SpikeEvent(
                event_id=generate_id(),
                spike_type=SpikeType.ALERT,
                intensity=intensity,
                source_agent="anomaly_detector",
                trace_id=generate_id(),
                payload={
                    "slot_id": slot_id,
                    "current": current_value,
                    "expected": expected_value,
                    "delta_percent": delta * 100,
                },
            )
            
            self.bus.emit(event)
            logger.info(f"Anomaly detected: {slot_id} delta={delta:.1%}")
            return event
        
        return None
    
    def route_event(
        self,
        source_agent: str,
        event_type: SpikeType,
        payload: Dict[str, Any],
    ) -> List[str]:
        """
        Route event to relevant agents.
        
        Per spec: Routage d'événements (slot changed → relevant agents)
        """
        event = SpikeEvent(
            event_id=generate_id(),
            spike_type=event_type,
            intensity=0.5,
            source_agent=source_agent,
            trace_id=generate_id(),
            payload=payload,
        )
        
        self.bus.emit(event)
        
        # Find target agents via synapses
        targets = []
        for synapse in self.mapper.get_agent_synapses(source_agent):
            if event_type in synapse.spike_inputs:
                if synapse.target_agent != source_agent:
                    targets.append(synapse.target_agent)
        
        return targets
    
    def score_priority(
        self,
        slot_id: str,
        risk_level: float,
        impact_score: float,
    ) -> Tuple[float, SpikeEvent]:
        """
        Quick priority scoring.
        
        Per spec: Scoring rapide (risk/priority) basé sur patterns
        """
        priority = (risk_level * 0.6 + impact_score * 0.4)
        
        event = SpikeEvent(
            event_id=generate_id(),
            spike_type=SpikeType.PRIORITY,
            intensity=priority,
            source_agent="priority_scorer",
            trace_id=generate_id(),
            payload={
                "slot_id": slot_id,
                "risk": risk_level,
                "impact": impact_score,
                "priority": priority,
            },
        )
        
        self.bus.emit(event)
        return priority, event
    
    def get_kpis(self) -> Dict[str, Any]:
        """
        Get KPIs.
        
        Per spec: temps propagation, énergie, false positives/negatives
        """
        return {
            "propagation_p50_ms": 0.5,  # Mock - would be measured
            "propagation_p95_ms": 2.0,
            "energy_per_event": 0.001,  # Joules
            "false_positives": self._false_positives,
            "false_negatives": self._false_negatives,
            "total_events": len(self.bus._events),
            "synapse_count": len(self.mapper._synapses),
        }
    
    def get_xr_aura_manifest(self) -> Dict[str, Any]:
        """
        Get XR "Aura des Agents" manifest.
        
        Per spec: Visualiser réseau pulsant, flux d'info, hot synapses
        """
        recent = self.bus.get_recent(50)
        
        return {
            "type": "neuro_aura",
            "pulsing_network": True,
            "active_spikes": len(recent),
            "hot_synapses": [
                s.synapse_id for s in self.mapper._synapses.values()
                if s.weight > 1.5
            ],
            "flow_visualization": "enabled",
        }


# ============================================================================
# FACTORY
# ============================================================================

def create_neuromorphic_lattice() -> NeuromorphicLattice:
    """Create neuromorphic lattice system"""
    return NeuromorphicLattice()
