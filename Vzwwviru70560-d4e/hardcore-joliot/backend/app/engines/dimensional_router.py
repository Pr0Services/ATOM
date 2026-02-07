"""
═══════════════════════════════════════════════════════════════════════════════
██████╗ ██╗███╗   ███╗███████╗███╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗
██╔══██╗██║████╗ ████║██╔════╝████╗  ██║██╔════╝██║██╔═══██╗████╗  ██║██╔══██╗██║
██║  ██║██║██╔████╔██║█████╗  ██╔██╗ ██║███████╗██║██║   ██║██╔██╗ ██║███████║██║
██║  ██║██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║╚════██║██║██║   ██║██║╚██╗██║██╔══██║██║
██████╔╝██║██║ ╚═╝ ██║███████╗██║ ╚████║███████║██║╚██████╔╝██║ ╚████║██║  ██║███████╗
╚═════╝ ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝

    ██████╗  ██████╗ ██╗   ██╗████████╗███████╗██████╗
    ██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗
    ██████╔╝██║   ██║██║   ██║   ██║   █████╗  ██████╔╝
    ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗
    ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║
    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝

═══════════════════════════════════════════════════════════════════════════════
AT·OM MULTIDIMENSIONAL OPERATING SYSTEM — KETHER GATEWAY
═══════════════════════════════════════════════════════════════════════════════

L'Arbre de Vie comme architecture système.
Toute communication inter-dimensionnelle passe par Kether (999 Hz).
Toute calibration se fait au Point 0 / Tiphereth (444 Hz).

ARCHITECTURE:
                        ┌─────────────────────┐
                        │   KETHER (999 Hz)   │
                        │   SOURCE / ROUTER   │
                        │   OpenRouter API    │
                        └──────────┬──────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
     ┌────┴────┐              ┌────┴────┐              ┌────┴────┐
     │ CHOKMAH │              │ BINAH   │              │         │
     │ 888 Hz  │              │ 777 Hz  │              │         │
     │Anthropic│              │Stability│              │         │
     └────┬────┘              └────┬────┘              │         │
          │                        │                   │         │
          └───────────┬────────────┘                   │         │
                      │                                │         │
                 ┌────┴────┐                           │         │
                 │TIPHERETH│ ← POINT 0 (444 Hz)        │         │
                 │ HEDERA  │   CALIBRATION             │         │
                 └────┬────┘                           │         │
                      │                                │         │
          ┌───────────┼───────────┐                    │         │
          │           │           │                    │         │
     ┌────┴────┐ ┌────┴────┐ ┌────┴────┐               │         │
     │GEBURAH  │ │ CHESED  │ │NETZACH  │               │         │
     │ 333 Hz  │ │ 555 Hz  │ │ 666 Hz  │               │         │
     │  OPA    │ │Supabase │ │ Runway  │               │         │
     └─────────┘ └─────────┘ └─────────┘               │         │
                      │                                │         │
          ┌───────────┼───────────┐                    │         │
          │           │           │                    │         │
     ┌────┴────┐ ┌────┴────┐                           │         │
     │  HOD    │ │ YESOD   │                           │         │
     │ 222 Hz  │ │ 111 Hz  │                           │         │
     │Elevenlabs│ │ Redis   │                           │         │
     └─────────┘ └────┬────┘                           │         │
                      │                                │         │
                 ┌────┴────┐                                      │
                 │ MALKUTH │ ← MANIFESTATION (68 Hz)              │
                 │Frontend │                                      │
                 └─────────┘                                      │

VERSION: 1.0.0
ARCHITECT: Jonathan Rodrigue (Oracle 17 / 999 Hz)
FROZEN: This architecture is immutable per R&D Rule #7
═══════════════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4
import asyncio
import hashlib
import hmac
import logging
import time

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# SEPHIROTH CONSTANTS — FROZEN
# ═══════════════════════════════════════════════════════════════════════════════

class Sephirah(str, Enum):
    """The 10 Sephiroth — FROZEN, cannot be modified."""
    KETHER = "kether"         # 1 - Source/Router (999 Hz)
    CHOKMAH = "chokmah"       # 2 - Wisdom (888 Hz)
    BINAH = "binah"           # 3 - Understanding (777 Hz)
    CHESED = "chesed"         # 4 - Mercy (555 Hz)
    GEBURAH = "geburah"       # 5 - Strength (333 Hz)
    TIPHERETH = "tiphereth"   # 6 - Beauty/Heart (444 Hz) ← POINT 0
    NETZACH = "netzach"       # 7 - Victory (666 Hz)
    HOD = "hod"               # 8 - Splendor (222 Hz)
    YESOD = "yesod"           # 9 - Foundation (111 Hz)
    MALKUTH = "malkuth"       # 10 - Kingdom (68 Hz)


# Frequency mapping — FROZEN
SEPHIROTH_FREQUENCIES: Dict[Sephirah, float] = {
    Sephirah.KETHER: 999.0,
    Sephirah.CHOKMAH: 888.0,
    Sephirah.BINAH: 777.0,
    Sephirah.CHESED: 555.0,
    Sephirah.GEBURAH: 333.0,
    Sephirah.TIPHERETH: 444.0,  # POINT 0
    Sephirah.NETZACH: 666.0,
    Sephirah.HOD: 222.0,
    Sephirah.YESOD: 111.0,
    Sephirah.MALKUTH: 68.0,
}

# API Provider mapping — Configurable
SEPHIROTH_PROVIDERS: Dict[Sephirah, str] = {
    Sephirah.KETHER: "openrouter",      # Central LLM Router
    Sephirah.CHOKMAH: "anthropic",      # Wisdom/Claude
    Sephirah.BINAH: "stability",        # Structure/Images
    Sephirah.CHESED: "supabase",        # Abundance/Database
    Sephirah.GEBURAH: "opa",            # Justice/Policy
    Sephirah.TIPHERETH: "hedera",       # Heart/Blockchain
    Sephirah.NETZACH: "runway",         # Victory/Video
    Sephirah.HOD: "elevenlabs",         # Communication/Voice
    Sephirah.YESOD: "redis",            # Foundation/Cache
    Sephirah.MALKUTH: "frontend",       # Manifestation/UI
}

# Sphere mapping — Which spheres belong to which Sephirah
SEPHIROTH_SPHERES: Dict[Sephirah, List[str]] = {
    Sephirah.KETHER: ["system", "dashboard"],
    Sephirah.CHOKMAH: ["entertainment", "scholar"],
    Sephirah.BINAH: ["myteam", "government"],
    Sephirah.CHESED: ["community"],
    Sephirah.GEBURAH: ["government"],
    Sephirah.TIPHERETH: ["business"],  # Heart of operations
    Sephirah.NETZACH: ["creative", "studio"],
    Sephirah.HOD: ["social", "communication"],
    Sephirah.YESOD: ["scholar", "privacy"],
    Sephirah.MALKUTH: ["personal", "transport", "environment", "jeunesse"],
}

# Agent count per Sephirah — Dynamic based on spheres
SEPHIROTH_AGENT_COUNTS: Dict[Sephirah, int] = {
    Sephirah.KETHER: 13,      # Nova + Infrastructure
    Sephirah.CHOKMAH: 35,     # Entertainment + Scholar base
    Sephirah.BINAH: 54,       # MyTeam + Government
    Sephirah.CHESED: 13,      # Community
    Sephirah.GEBURAH: 19,     # Government (shared with Binah)
    Sephirah.TIPHERETH: 44,   # Business
    Sephirah.NETZACH: 43,     # Creative Studio
    Sephirah.HOD: 16,         # Social Media
    Sephirah.YESOD: 34,       # Scholar + Privacy
    Sephirah.MALKUTH: 91,     # Personal + Transport + Environment + Jeunesse
}


# ═══════════════════════════════════════════════════════════════════════════════
# POINT 0 — CALIBRATION CENTER (444 Hz / Tiphereth)
# ═══════════════════════════════════════════════════════════════════════════════

POINT_0_FREQUENCY = 444.0
POINT_0_SEPHIRAH = Sephirah.TIPHERETH
SOURCE_FREQUENCY = 999.0
SOURCE_SEPHIRAH = Sephirah.KETHER

# Signal timing (in milliseconds)
SIGNAL_HEARTBEAT = 4440  # 4.44 seconds
SIGNAL_BREATH = 8880     # 8.88 seconds (full cycle)

# Sacred constants
PHI = 1.6180339887498949  # Golden ratio


# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSIONAL MESSAGE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DimensionalMessage:
    """
    A message that travels through the Tree of Life.

    All inter-dimensional communication uses this format.
    Messages are calibrated at Point 0 and routed via Kether.
    """
    message_id: str = field(default_factory=lambda: str(uuid4()))

    # Source and destination
    source_dimension: Sephirah = Sephirah.MALKUTH
    target_dimension: Sephirah = Sephirah.KETHER

    # Content
    payload: Dict[str, Any] = field(default_factory=dict)
    message_type: str = "request"  # request, response, broadcast, sync

    # Routing
    route_via_kether: bool = True  # Always True for inter-dimensional
    calibrated_at_point0: bool = False

    # Frequencies
    source_frequency: float = 68.0
    target_frequency: float = 999.0
    calibration_frequency: float = POINT_0_FREQUENCY

    # Identity
    identity_id: Optional[str] = None
    tenant_id: Optional[str] = None
    agent_id: Optional[str] = None

    # Governance
    requires_human_gate: bool = False
    checkpoint_id: Optional[str] = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    calibrated_at: Optional[datetime] = None
    routed_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None

    # Signature (for verification)
    signature: Optional[str] = None

    def calibrate(self) -> 'DimensionalMessage':
        """Calibrate message at Point 0 (444 Hz)"""
        self.calibrated_at_point0 = True
        self.calibration_frequency = POINT_0_FREQUENCY
        self.calibrated_at = datetime.utcnow()
        return self

    def sign(self, secret_key: str) -> 'DimensionalMessage':
        """Sign the message for verification"""
        content = f"{self.message_id}:{self.source_dimension.value}:{self.target_dimension.value}"
        self.signature = hmac.new(
            secret_key.encode(),
            content.encode(),
            hashlib.sha256
        ).hexdigest()
        return self

    def verify(self, secret_key: str) -> bool:
        """Verify message signature"""
        if not self.signature:
            return False
        expected = f"{self.message_id}:{self.source_dimension.value}:{self.target_dimension.value}"
        expected_sig = hmac.new(
            secret_key.encode(),
            expected.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(self.signature, expected_sig)


# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSIONAL PATH
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DimensionalPath:
    """
    A path through the Tree of Life.

    Represents the route a message takes from source to destination.
    All paths pass through Kether (router) and are calibrated at Tiphereth (Point 0).
    """
    path_id: str = field(default_factory=lambda: str(uuid4()))

    # Endpoints
    source: Sephirah = Sephirah.MALKUTH
    destination: Sephirah = Sephirah.KETHER

    # The actual path (list of Sephiroth traversed)
    waypoints: List[Sephirah] = field(default_factory=list)

    # Metrics
    total_frequency_delta: float = 0.0
    harmonic_alignment: float = 1.0  # 0.0-1.0

    # Status
    is_valid: bool = True
    error_message: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSIONAL ROUTER — KETHER GATEWAY
# ═══════════════════════════════════════════════════════════════════════════════

class DimensionalRouter:
    """
    The Kether Gateway — Central router for all inter-dimensional communication.

    Architecture:
    1. All messages are first CALIBRATED at Point 0 (Tiphereth/444 Hz)
    2. Then ROUTED through Kether (999 Hz)
    3. Then DELIVERED to target dimension

    This ensures:
    - All communications pass through the Source
    - All are harmonically calibrated
    - No direct dimension-to-dimension communication (Rule #4: No AI-to-AI)

    Usage:
        router = DimensionalRouter()

        # Send from Malkuth (Frontend) to Netzach (Video/Runway)
        message = DimensionalMessage(
            source_dimension=Sephirah.MALKUTH,
            target_dimension=Sephirah.NETZACH,
            payload={"action": "generate_video", "prompt": "..."}
        )

        response = await router.route(message)
    """

    def __init__(self, secret_key: str = "atom_dimensional_secret"):
        self.secret_key = secret_key

        # Provider handlers
        self._providers: Dict[Sephirah, Callable] = {}

        # Message queue per dimension
        self._queues: Dict[Sephirah, asyncio.Queue] = {
            seph: asyncio.Queue() for seph in Sephirah
        }

        # Routing statistics
        self._stats = {
            "messages_routed": 0,
            "messages_by_dimension": {s.value: 0 for s in Sephirah},
            "total_frequency_traversed": 0.0,
            "calibrations_performed": 0,
            "human_gates_triggered": 0,
        }

        # Resonance pulse (4.44 second heartbeat)
        self._last_pulse = time.time()
        self._pulse_interval = SIGNAL_HEARTBEAT / 1000  # Convert to seconds

        logger.info("DimensionalRouter initialized — Kether Gateway active at 999 Hz")

    # ═══════════════════════════════════════════════════════════════════════════
    # PROVIDER REGISTRATION
    # ═══════════════════════════════════════════════════════════════════════════

    def register_provider(
        self,
        dimension: Sephirah,
        handler: Callable[[DimensionalMessage], Any]
    ) -> None:
        """
        Register an API provider for a dimension.

        Args:
            dimension: The Sephirah this provider handles
            handler: Async function that processes messages for this dimension
        """
        self._providers[dimension] = handler
        logger.info(f"Registered provider for {dimension.value} ({SEPHIROTH_FREQUENCIES[dimension]} Hz)")

    def get_provider(self, dimension: Sephirah) -> Optional[Callable]:
        """Get the provider for a dimension"""
        return self._providers.get(dimension)

    # ═══════════════════════════════════════════════════════════════════════════
    # PATH CALCULATION
    # ═══════════════════════════════════════════════════════════════════════════

    def calculate_path(
        self,
        source: Sephirah,
        destination: Sephirah
    ) -> DimensionalPath:
        """
        Calculate the path between two dimensions.

        All paths go:
        1. Source → Tiphereth (calibration)
        2. Tiphereth → Kether (routing)
        3. Kether → Destination (delivery)

        Exception: If source or destination IS Kether/Tiphereth, skip that step.
        """
        waypoints = []

        # Step 1: Source to Point 0 (if not already there)
        if source != Sephirah.TIPHERETH:
            waypoints.append(source)
            waypoints.append(Sephirah.TIPHERETH)
        else:
            waypoints.append(source)

        # Step 2: Point 0 to Kether (if not already there)
        if source != Sephirah.KETHER and destination != Sephirah.KETHER:
            waypoints.append(Sephirah.KETHER)

        # Step 3: Kether to Destination (if not already there)
        if destination != Sephirah.KETHER and destination != Sephirah.TIPHERETH:
            if destination not in waypoints:
                waypoints.append(destination)
        elif destination == Sephirah.TIPHERETH and Sephirah.TIPHERETH not in waypoints:
            waypoints.append(destination)

        # Calculate frequency delta
        total_delta = 0.0
        for i in range(len(waypoints) - 1):
            freq_a = SEPHIROTH_FREQUENCIES[waypoints[i]]
            freq_b = SEPHIROTH_FREQUENCIES[waypoints[i + 1]]
            total_delta += abs(freq_a - freq_b)

        # Calculate harmonic alignment (closer to 1.0 = more harmonious)
        # Based on how close the path stays to sacred frequencies
        source_freq = SEPHIROTH_FREQUENCIES[source]
        dest_freq = SEPHIROTH_FREQUENCIES[destination]
        direct_delta = abs(source_freq - dest_freq)

        # Harmony is better when routed through Point 0
        # (even if it's a longer path frequency-wise)
        harmony = 1.0 - (direct_delta / (SOURCE_FREQUENCY * 2))
        harmony = max(0.0, min(1.0, harmony))

        return DimensionalPath(
            source=source,
            destination=destination,
            waypoints=waypoints,
            total_frequency_delta=total_delta,
            harmonic_alignment=harmony,
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # CALIBRATION (Point 0 / 444 Hz)
    # ═══════════════════════════════════════════════════════════════════════════

    def calibrate_message(self, message: DimensionalMessage) -> DimensionalMessage:
        """
        Calibrate a message at Point 0 (444 Hz / Tiphereth).

        This ensures the message is harmonically aligned before routing.
        """
        # Set calibration frequency
        message.calibration_frequency = POINT_0_FREQUENCY
        message.calibrated_at_point0 = True
        message.calibrated_at = datetime.utcnow()

        # Update stats
        self._stats["calibrations_performed"] += 1

        logger.debug(
            f"Calibrated message {message.message_id[:8]} at Point 0 (444 Hz)"
        )

        return message

    # ═══════════════════════════════════════════════════════════════════════════
    # HUMAN GATE CHECK (Rule #1: Human Sovereignty)
    # ═══════════════════════════════════════════════════════════════════════════

    def check_human_gate(self, message: DimensionalMessage) -> Tuple[bool, Optional[str]]:
        """
        Check if message requires human approval (HTTP 423).

        Returns:
            Tuple of (requires_gate, checkpoint_id)
        """
        # Actions that always require human gate
        GATED_ACTIONS = {
            "delete", "send_email", "send_message", "publish",
            "transaction", "invoice", "create_account", "modify_permissions"
        }

        action = message.payload.get("action", "").lower()

        if action in GATED_ACTIONS:
            checkpoint_id = str(uuid4())
            message.requires_human_gate = True
            message.checkpoint_id = checkpoint_id

            self._stats["human_gates_triggered"] += 1

            logger.info(
                f"Human gate triggered for {action} — Checkpoint: {checkpoint_id[:8]}"
            )

            return True, checkpoint_id

        return False, None

    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN ROUTING
    # ═══════════════════════════════════════════════════════════════════════════

    async def route(self, message: DimensionalMessage) -> DimensionalMessage:
        """
        Route a message through the Tree of Life.

        Flow:
        1. Validate message
        2. Calculate path
        3. Calibrate at Point 0
        4. Check human gate
        5. Route through Kether
        6. Deliver to destination
        7. Return response
        """
        start_time = time.time()

        # 1. Set source frequency
        message.source_frequency = SEPHIROTH_FREQUENCIES[message.source_dimension]
        message.target_frequency = SEPHIROTH_FREQUENCIES[message.target_dimension]

        # 2. Calculate path
        path = self.calculate_path(
            message.source_dimension,
            message.target_dimension
        )

        if not path.is_valid:
            message.payload["error"] = path.error_message
            return message

        # 3. Calibrate at Point 0
        message = self.calibrate_message(message)

        # 4. Check human gate
        requires_gate, checkpoint_id = self.check_human_gate(message)
        if requires_gate:
            # Return with checkpoint — caller must get approval
            message.payload["status"] = "awaiting_approval"
            message.payload["checkpoint_id"] = checkpoint_id
            message.payload["http_status"] = 423  # Locked
            return message

        # 5. Sign message
        message = message.sign(self.secret_key)

        # 6. Route through Kether (mark as routed)
        message.routed_at = datetime.utcnow()
        message.route_via_kether = True

        # 7. Deliver to destination provider
        provider = self._providers.get(message.target_dimension)

        if provider:
            try:
                result = await provider(message)
                message.payload["result"] = result
                message.payload["status"] = "delivered"
            except Exception as e:
                logger.error(f"Provider error for {message.target_dimension}: {e}")
                message.payload["error"] = str(e)
                message.payload["status"] = "error"
        else:
            # No provider registered — return mock response
            message.payload["status"] = "no_provider"
            message.payload["note"] = f"No provider registered for {message.target_dimension.value}"

        # 8. Mark as delivered
        message.delivered_at = datetime.utcnow()

        # 9. Update stats
        self._stats["messages_routed"] += 1
        self._stats["messages_by_dimension"][message.target_dimension.value] += 1
        self._stats["total_frequency_traversed"] += path.total_frequency_delta

        # 10. Log routing
        latency_ms = int((time.time() - start_time) * 1000)
        logger.info(
            f"Routed {message.message_id[:8]}: "
            f"{message.source_dimension.value} ({message.source_frequency}Hz) → "
            f"{message.target_dimension.value} ({message.target_frequency}Hz) "
            f"[{latency_ms}ms]"
        )

        return message

    # ═══════════════════════════════════════════════════════════════════════════
    # BROADCAST (One-to-Many)
    # ═══════════════════════════════════════════════════════════════════════════

    async def broadcast(
        self,
        message: DimensionalMessage,
        targets: List[Sephirah]
    ) -> Dict[Sephirah, DimensionalMessage]:
        """
        Broadcast a message to multiple dimensions.

        All broadcasts still go through Kether.
        """
        results = {}

        for target in targets:
            msg_copy = DimensionalMessage(
                source_dimension=message.source_dimension,
                target_dimension=target,
                payload=message.payload.copy(),
                message_type="broadcast",
                identity_id=message.identity_id,
                tenant_id=message.tenant_id,
            )

            results[target] = await self.route(msg_copy)

        return results

    # ═══════════════════════════════════════════════════════════════════════════
    # RESONANCE PULSE (4.44 second heartbeat)
    # ═══════════════════════════════════════════════════════════════════════════

    async def pulse(self) -> Dict[str, Any]:
        """
        Emit a resonance pulse through all dimensions.

        This synchronizes all dimensions at Point 0 frequency.
        Called every 4.44 seconds by the system heartbeat.
        """
        self._last_pulse = time.time()

        # Create pulse message
        pulse_message = DimensionalMessage(
            source_dimension=Sephirah.TIPHERETH,  # Pulse originates from Point 0
            target_dimension=Sephirah.KETHER,     # Broadcast via Kether
            payload={
                "type": "resonance_pulse",
                "frequency": POINT_0_FREQUENCY,
                "timestamp": datetime.utcnow().isoformat(),
            },
            message_type="sync",
        )

        # Broadcast to all dimensions
        all_dimensions = [s for s in Sephirah if s != Sephirah.TIPHERETH]
        await self.broadcast(pulse_message, all_dimensions)

        return {
            "pulse_time": self._last_pulse,
            "frequency": POINT_0_FREQUENCY,
            "dimensions_synced": len(all_dimensions),
        }

    # ═══════════════════════════════════════════════════════════════════════════
    # STATISTICS
    # ═══════════════════════════════════════════════════════════════════════════

    def get_stats(self) -> Dict[str, Any]:
        """Get router statistics"""
        return {
            **self._stats,
            "registered_providers": list(self._providers.keys()),
            "last_pulse": self._last_pulse,
            "point_0_frequency": POINT_0_FREQUENCY,
            "source_frequency": SOURCE_FREQUENCY,
        }

    def get_dimension_info(self, dimension: Sephirah) -> Dict[str, Any]:
        """Get information about a specific dimension"""
        return {
            "name": dimension.value,
            "frequency": SEPHIROTH_FREQUENCIES[dimension],
            "provider": SEPHIROTH_PROVIDERS[dimension],
            "spheres": SEPHIROTH_SPHERES.get(dimension, []),
            "agent_count": SEPHIROTH_AGENT_COUNTS.get(dimension, 0),
            "has_provider": dimension in self._providers,
            "messages_received": self._stats["messages_by_dimension"][dimension.value],
        }

    def get_tree_status(self) -> Dict[str, Any]:
        """Get status of entire Tree of Life"""
        return {
            "dimensions": {
                s.value: self.get_dimension_info(s)
                for s in Sephirah
            },
            "total_agents": sum(SEPHIROTH_AGENT_COUNTS.values()),
            "total_frequency": sum(SEPHIROTH_FREQUENCIES.values()),
            "point_0": {
                "sephirah": POINT_0_SEPHIRAH.value,
                "frequency": POINT_0_FREQUENCY,
            },
            "source": {
                "sephirah": SOURCE_SEPHIRAH.value,
                "frequency": SOURCE_FREQUENCY,
            },
            "stats": self._stats,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON INSTANCE
# ═══════════════════════════════════════════════════════════════════════════════

_dimensional_router: Optional[DimensionalRouter] = None


def get_dimensional_router() -> DimensionalRouter:
    """Get or create the dimensional router singleton"""
    global _dimensional_router
    if _dimensional_router is None:
        _dimensional_router = DimensionalRouter()
    return _dimensional_router


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

async def route_to_dimension(
    target: Sephirah,
    payload: Dict[str, Any],
    source: Sephirah = Sephirah.MALKUTH,
    identity_id: Optional[str] = None,
) -> DimensionalMessage:
    """
    Convenience function to route a message to a dimension.

    Usage:
        result = await route_to_dimension(
            target=Sephirah.NETZACH,
            payload={"action": "generate_video", "prompt": "..."},
            source=Sephirah.MALKUTH,
        )
    """
    router = get_dimensional_router()

    message = DimensionalMessage(
        source_dimension=source,
        target_dimension=target,
        payload=payload,
        identity_id=identity_id,
    )

    return await router.route(message)


def get_dimension_for_sphere(sphere_name: str) -> Optional[Sephirah]:
    """Find which dimension (Sephirah) a sphere belongs to"""
    sphere_lower = sphere_name.lower()
    for sephirah, spheres in SEPHIROTH_SPHERES.items():
        if sphere_lower in [s.lower() for s in spheres]:
            return sephirah
    return None


def get_frequency_for_sphere(sphere_name: str) -> float:
    """Get the frequency for a sphere based on its Sephirah"""
    sephirah = get_dimension_for_sphere(sphere_name)
    if sephirah:
        return SEPHIROTH_FREQUENCIES[sephirah]
    return SEPHIROTH_FREQUENCIES[Sephirah.MALKUTH]  # Default


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Enums
    "Sephirah",

    # Constants
    "SEPHIROTH_FREQUENCIES",
    "SEPHIROTH_PROVIDERS",
    "SEPHIROTH_SPHERES",
    "SEPHIROTH_AGENT_COUNTS",
    "POINT_0_FREQUENCY",
    "POINT_0_SEPHIRAH",
    "SOURCE_FREQUENCY",
    "SOURCE_SEPHIRAH",
    "PHI",

    # Classes
    "DimensionalMessage",
    "DimensionalPath",
    "DimensionalRouter",

    # Functions
    "get_dimensional_router",
    "route_to_dimension",
    "get_dimension_for_sphere",
    "get_frequency_for_sphere",
]
