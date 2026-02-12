"""
============================================================================
CHE·NU™ V69 — ROSETTA BRIDGE
============================================================================
System 5/5: TypeScript↔Python signal bridge

Problem: rosetta-core (TypeScript) has DigestiveSystem, ThreatAmygdala,
QuantumCorrector, VibrationalMotor, and PolishingEngine. The Python
backend has NeuromorphicLattice, FeedbackLoopEngine, etc. These two
worlds don't communicate — no shared event bus, no signal translation.

Solution: RosettaBridge defines a shared protocol for signal exchange
between TypeScript and Python systems. It translates spike events to
rosetta-core format and vice versa, using a message queue interface
(Redis, HTTP, or in-memory for testing).

Connects to:
- SpikeBus (Python side: emits/consumes SpikeEvents)
- rosetta-core DigestiveSystem (TS side: content pipeline events)
- rosetta-core ThreatAmygdala (TS side: threat alerts)
- NeuroFeedbackHub (aggregates cross-system signals)

Does NOT duplicate:
- SpikeBus (we bridge, not replace)
- DigestiveSystem (we translate signals, not process content)
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from enum import Enum
import json
import logging

from ..models import SpikeEvent, SpikeType, generate_id

logger = logging.getLogger(__name__)


class BridgeDirection(str, Enum):
    PY_TO_TS = "py_to_ts"   # Python → TypeScript
    TS_TO_PY = "ts_to_py"   # TypeScript → Python


class RosettaSignalType(str, Enum):
    """Signal types in rosetta-core (TypeScript side)."""
    DIGEST_STAGE = "digest_stage"          # DigestiveSystem stage completion
    THREAT_ALERT = "threat_alert"          # ThreatAmygdala detection
    QUANTUM_CORRECTION = "quantum_fix"     # QuantumCorrector correction
    VIBRATION_EVENT = "vibration_event"    # VibrationalMotor output
    POLISH_COMPLETE = "polish_complete"    # PolishingEngine done


# Mapping: rosetta-core signal → Python SpikeType
_ROSETTA_TO_SPIKE: Dict[RosettaSignalType, SpikeType] = {
    RosettaSignalType.DIGEST_STAGE: SpikeType.SLOT_DELTA,
    RosettaSignalType.THREAT_ALERT: SpikeType.ALERT,
    RosettaSignalType.QUANTUM_CORRECTION: SpikeType.METRIC_DELTA,
    RosettaSignalType.VIBRATION_EVENT: SpikeType.OPA_EVENT,
    RosettaSignalType.POLISH_COMPLETE: SpikeType.SLOT_DELTA,
}

# Mapping: Python SpikeType → closest rosetta-core signal
_SPIKE_TO_ROSETTA: Dict[SpikeType, RosettaSignalType] = {
    SpikeType.ALERT: RosettaSignalType.THREAT_ALERT,
    SpikeType.SLOT_DELTA: RosettaSignalType.DIGEST_STAGE,
    SpikeType.METRIC_DELTA: RosettaSignalType.QUANTUM_CORRECTION,
    SpikeType.OPA_EVENT: RosettaSignalType.VIBRATION_EVENT,
    SpikeType.PRIORITY: RosettaSignalType.DIGEST_STAGE,
    SpikeType.ROUTE: RosettaSignalType.DIGEST_STAGE,
    SpikeType.XR_INTERVENTION: RosettaSignalType.VIBRATION_EVENT,
}


@dataclass
class BridgeMessage:
    """A message crossing the TypeScript↔Python bridge."""
    message_id: str
    direction: BridgeDirection
    source_system: str      # e.g., "ThreatAmygdala", "NeuromorphicLattice"
    target_system: str      # e.g., "NeuroFeedbackHub", "DigestiveSystem"
    signal_type: str        # original signal type
    intensity: float
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    trace_id: str = ""


class RosettaBridge:
    """
    Signal bridge between rosetta-core (TypeScript) and Python backend.

    Operates as a bidirectional translator:
    - Python SpikeEvents → BridgeMessages → rosetta-core format (JSON)
    - rosetta-core signals (JSON) → BridgeMessages → Python SpikeEvents

    Transport is pluggable (in-memory for testing, Redis/HTTP for production).
    """

    def __init__(self):
        # Message queues (in-memory, replace with Redis in production)
        self._outbound: List[BridgeMessage] = []  # py → ts
        self._inbound: List[BridgeMessage] = []   # ts → py

        # Listeners for translated events
        self._spike_listeners: List[Callable[[SpikeEvent], None]] = []
        self._bridge_listeners: List[Callable[[BridgeMessage], None]] = []

        # Stats
        self._stats = {
            "py_to_ts": 0,
            "ts_to_py": 0,
            "translation_errors": 0,
        }

    def spike_to_bridge(self, event: SpikeEvent) -> BridgeMessage:
        """
        Translate a Python SpikeEvent to a bridge message (for TypeScript).
        """
        rosetta_type = _SPIKE_TO_ROSETTA.get(
            event.spike_type, RosettaSignalType.DIGEST_STAGE
        )

        message = BridgeMessage(
            message_id=generate_id(),
            direction=BridgeDirection.PY_TO_TS,
            source_system=event.source_agent,
            target_system="rosetta-core",
            signal_type=rosetta_type.value,
            intensity=event.intensity,
            payload={
                "original_spike_type": event.spike_type.value,
                "event_id": event.event_id,
                **event.payload,
            },
            trace_id=event.trace_id,
        )

        self._outbound.append(message)
        self._stats["py_to_ts"] += 1

        # Notify bridge listeners
        for listener in self._bridge_listeners:
            try:
                listener(message)
            except Exception as e:
                logger.error(f"[RosettaBridge] Bridge listener error: {e}")

        logger.debug(
            f"[RosettaBridge] PY→TS: {event.spike_type.value} → "
            f"{rosetta_type.value} (intensity={event.intensity:.2f})"
        )

        return message

    def bridge_to_spike(self, raw_signal: Dict[str, Any]) -> Optional[SpikeEvent]:
        """
        Translate a rosetta-core signal (JSON dict) to a Python SpikeEvent.

        Expected raw_signal format:
        {
            "type": "threat_alert",  # RosettaSignalType value
            "source": "ThreatAmygdala",
            "intensity": 0.8,
            "trace_id": "...",
            "payload": {...}
        }
        """
        try:
            signal_type_str = raw_signal.get("type", "")
            try:
                rosetta_type = RosettaSignalType(signal_type_str)
            except ValueError:
                logger.warning(
                    f"[RosettaBridge] Unknown rosetta signal: {signal_type_str}"
                )
                self._stats["translation_errors"] += 1
                return None

            spike_type = _ROSETTA_TO_SPIKE.get(rosetta_type, SpikeType.SLOT_DELTA)

            event = SpikeEvent(
                event_id=generate_id(),
                spike_type=spike_type,
                intensity=float(raw_signal.get("intensity", 0.5)),
                source_agent=raw_signal.get("source", "rosetta-core"),
                trace_id=raw_signal.get("trace_id", generate_id()),
                payload={
                    "bridge_origin": "rosetta-core",
                    "original_type": signal_type_str,
                    **(raw_signal.get("payload") or {}),
                },
            )

            # Record inbound
            bridge_msg = BridgeMessage(
                message_id=generate_id(),
                direction=BridgeDirection.TS_TO_PY,
                source_system=raw_signal.get("source", "rosetta-core"),
                target_system="NeuromorphicLattice",
                signal_type=signal_type_str,
                intensity=event.intensity,
                payload=event.payload,
                trace_id=event.trace_id,
            )
            self._inbound.append(bridge_msg)
            self._stats["ts_to_py"] += 1

            # Notify spike listeners
            for listener in self._spike_listeners:
                try:
                    listener(event)
                except Exception as e:
                    logger.error(f"[RosettaBridge] Spike listener error: {e}")

            logger.debug(
                f"[RosettaBridge] TS→PY: {signal_type_str} → "
                f"{spike_type.value} (intensity={event.intensity:.2f})"
            )

            return event

        except Exception as e:
            logger.error(f"[RosettaBridge] Translation error: {e}")
            self._stats["translation_errors"] += 1
            return None

    def to_json(self, message: BridgeMessage) -> str:
        """Serialize a bridge message to JSON (for transport to TypeScript)."""
        return json.dumps({
            "message_id": message.message_id,
            "direction": message.direction.value,
            "source": message.source_system,
            "target": message.target_system,
            "type": message.signal_type,
            "intensity": message.intensity,
            "payload": message.payload,
            "trace_id": message.trace_id,
            "timestamp": message.timestamp.isoformat(),
        })

    def from_json(self, raw: str) -> Optional[SpikeEvent]:
        """Parse a JSON signal from TypeScript and convert to SpikeEvent."""
        try:
            data = json.loads(raw)
            return self.bridge_to_spike(data)
        except json.JSONDecodeError as e:
            logger.error(f"[RosettaBridge] JSON parse error: {e}")
            self._stats["translation_errors"] += 1
            return None

    def on_spike(self, listener: Callable[[SpikeEvent], None]) -> None:
        """Register listener for translated spike events (TS → PY)."""
        self._spike_listeners.append(listener)

    def on_bridge_message(self, listener: Callable[[BridgeMessage], None]) -> None:
        """Register listener for outbound bridge messages (PY → TS)."""
        self._bridge_listeners.append(listener)

    def get_pending_outbound(self) -> List[BridgeMessage]:
        """Get and clear pending outbound messages (for transport layer)."""
        messages = list(self._outbound)
        self._outbound.clear()
        return messages

    def get_stats(self) -> Dict[str, int]:
        """Get bridge statistics."""
        return dict(self._stats)
