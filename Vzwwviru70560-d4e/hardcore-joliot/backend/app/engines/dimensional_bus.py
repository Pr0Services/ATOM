"""
═══════════════════════════════════════════════════════════════════════════════
DIMENSIONAL MESSAGE BUS — Inter-Dimensional Communication System
═══════════════════════════════════════════════════════════════════════════════

The bus enables real-time communication between all 10 dimensions and 362+ agents.

PROTOCOL:
1. All messages go through Point 0 (Tiphereth/444 Hz) for calibration
2. Then route via Kether (999 Hz) for distribution
3. Agents subscribe to their dimension's channel
4. Human gates (HTTP 423) block sensitive actions

CHANNELS:
┌──────────────────────────────────────────────────────────────────────────────┐
│                           KETHER BROADCAST (999 Hz)                          │
│                          [System-wide announcements]                         │
├────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┬─────┤
│CHOKMAH │ BINAH  │ CHESED │GEBURAH │TIPHRTH │NETZACH │  HOD   │ YESOD  │MALKTH│
│ 888 Hz │ 777 Hz │ 555 Hz │ 333 Hz │ 444 Hz │ 666 Hz │ 222 Hz │ 111 Hz │68 Hz │
│ Wisdom │Struct  │Abundnce│Justice │ Heart  │Victory │ Comm   │ Found  │World │
│ 35 agt │ 54 agt │ 13 agt │ 19 agt │ 44 agt │ 43 agt │ 16 agt │ 34 agt │91 agt│
└────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┴─────┘
                                     ↓
                         ┌───────────────────────┐
                         │   POINT 0 CALIBRATOR  │
                         │   (Tiphereth/444 Hz)  │
                         └───────────────────────┘

VERSION: 1.0.0
═══════════════════════════════════════════════════════════════════════════════
"""

import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4

from .dimensional_router import (
    Sephirah,
    DimensionalMessage,
    DimensionalRouter,
    get_dimensional_router,
    SEPHIROTH_FREQUENCIES,
    POINT_0_FREQUENCY,
    SOURCE_FREQUENCY,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE TYPES
# ═══════════════════════════════════════════════════════════════════════════════

class MessagePriority(str, Enum):
    """Message priority levels."""
    CRITICAL = "critical"    # Immediate processing (human gates, security)
    HIGH = "high"           # Fast processing (user actions)
    NORMAL = "normal"       # Standard processing
    LOW = "low"             # Background tasks
    PULSE = "pulse"         # Resonance pulses (4.44s heartbeat)


class SubscriptionType(str, Enum):
    """Subscription types."""
    DIMENSION = "dimension"     # Subscribe to a Sephirah
    SPHERE = "sphere"           # Subscribe to a sphere
    AGENT = "agent"             # Subscribe as an agent
    BROADCAST = "broadcast"     # Receive all broadcasts
    SYSTEM = "system"           # System events only


# ═══════════════════════════════════════════════════════════════════════════════
# SUBSCRIPTION
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Subscription:
    """A subscription to the dimensional bus."""
    subscription_id: str = field(default_factory=lambda: str(uuid4()))

    # Subscriber identity
    subscriber_id: str = ""  # agent_id, user_id, or system
    subscriber_type: str = "agent"  # agent, user, system

    # What to subscribe to
    subscription_type: SubscriptionType = SubscriptionType.DIMENSION
    dimension: Optional[Sephirah] = None
    sphere: Optional[str] = None

    # Filters
    message_types: Set[str] = field(default_factory=set)  # Empty = all
    min_priority: MessagePriority = MessagePriority.LOW

    # Callback
    handler: Optional[Callable[[DimensionalMessage], Any]] = None

    # Status
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None
    message_count: int = 0


# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSIONAL BUS
# ═══════════════════════════════════════════════════════════════════════════════

class DimensionalBus:
    """
    The inter-dimensional message bus.

    Enables publish/subscribe communication between all dimensions and agents.

    Usage:
        bus = get_dimensional_bus()

        # Subscribe an agent to a dimension
        sub_id = bus.subscribe(
            subscriber_id="agent_123",
            dimension=Sephirah.NETZACH,
            handler=my_handler,
        )

        # Publish a message
        await bus.publish(
            message=DimensionalMessage(
                source_dimension=Sephirah.MALKUTH,
                target_dimension=Sephirah.NETZACH,
                payload={"action": "generate"},
            )
        )

        # Broadcast to all
        await bus.broadcast(
            payload={"event": "system_update"},
            priority=MessagePriority.HIGH,
        )
    """

    def __init__(self):
        # Router integration
        self._router = get_dimensional_router()

        # Subscriptions
        self._subscriptions: Dict[str, Subscription] = {}

        # Indexes for fast lookup
        self._by_dimension: Dict[Sephirah, Set[str]] = defaultdict(set)
        self._by_sphere: Dict[str, Set[str]] = defaultdict(set)
        self._by_subscriber: Dict[str, Set[str]] = defaultdict(set)
        self._broadcasts: Set[str] = set()

        # Message queues per dimension
        self._queues: Dict[Sephirah, asyncio.Queue] = {
            seph: asyncio.Queue() for seph in Sephirah
        }
        self._broadcast_queue: asyncio.Queue = asyncio.Queue()

        # Statistics
        self._stats = {
            "messages_published": 0,
            "messages_delivered": 0,
            "broadcasts_sent": 0,
            "subscriptions_active": 0,
            "by_dimension": {s.value: 0 for s in Sephirah},
        }

        # Resonance pulse tracking
        self._pulse_count = 0
        self._last_pulse = datetime.utcnow()

        logger.info("DimensionalBus initialized — 10 dimension channels active")

    # ═══════════════════════════════════════════════════════════════════════════
    # SUBSCRIPTIONS
    # ═══════════════════════════════════════════════════════════════════════════

    def subscribe(
        self,
        subscriber_id: str,
        dimension: Optional[Sephirah] = None,
        sphere: Optional[str] = None,
        handler: Optional[Callable[[DimensionalMessage], Any]] = None,
        subscription_type: SubscriptionType = SubscriptionType.DIMENSION,
        min_priority: MessagePriority = MessagePriority.LOW,
        message_types: Optional[Set[str]] = None,
    ) -> str:
        """
        Subscribe to messages on the bus.

        Returns subscription_id for later unsubscription.
        """
        sub = Subscription(
            subscriber_id=subscriber_id,
            subscription_type=subscription_type,
            dimension=dimension,
            sphere=sphere,
            handler=handler,
            min_priority=min_priority,
            message_types=message_types or set(),
        )

        # Store subscription
        self._subscriptions[sub.subscription_id] = sub

        # Index
        if dimension:
            self._by_dimension[dimension].add(sub.subscription_id)
        if sphere:
            self._by_sphere[sphere].add(sub.subscription_id)
        if subscription_type == SubscriptionType.BROADCAST:
            self._broadcasts.add(sub.subscription_id)

        self._by_subscriber[subscriber_id].add(sub.subscription_id)
        self._stats["subscriptions_active"] += 1

        logger.debug(
            f"Subscription created: {subscriber_id} → "
            f"{dimension.value if dimension else sphere or 'broadcast'}"
        )

        return sub.subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Remove a subscription."""
        sub = self._subscriptions.get(subscription_id)
        if not sub:
            return False

        # Remove from indexes
        if sub.dimension:
            self._by_dimension[sub.dimension].discard(subscription_id)
        if sub.sphere:
            self._by_sphere[sub.sphere].discard(subscription_id)
        if sub.subscription_type == SubscriptionType.BROADCAST:
            self._broadcasts.discard(subscription_id)

        self._by_subscriber[sub.subscriber_id].discard(subscription_id)

        # Remove subscription
        del self._subscriptions[subscription_id]
        self._stats["subscriptions_active"] -= 1

        return True

    def unsubscribe_all(self, subscriber_id: str) -> int:
        """Remove all subscriptions for a subscriber."""
        sub_ids = list(self._by_subscriber.get(subscriber_id, set()))
        count = 0
        for sub_id in sub_ids:
            if self.unsubscribe(sub_id):
                count += 1
        return count

    # ═══════════════════════════════════════════════════════════════════════════
    # PUBLISHING
    # ═══════════════════════════════════════════════════════════════════════════

    async def publish(
        self,
        message: DimensionalMessage,
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> DimensionalMessage:
        """
        Publish a message to the bus.

        Message is:
        1. Calibrated at Point 0
        2. Routed via Kether
        3. Delivered to target dimension subscribers
        """
        # Add priority to payload
        message.payload["_priority"] = priority.value

        # Route through dimensional router (calibration + Kether routing)
        routed = await self._router.route(message)

        # Deliver to subscribers
        await self._deliver(routed, priority)

        self._stats["messages_published"] += 1
        self._stats["by_dimension"][message.target_dimension.value] += 1

        return routed

    async def broadcast(
        self,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        source: Sephirah = Sephirah.KETHER,
    ) -> Dict[Sephirah, DimensionalMessage]:
        """
        Broadcast a message to all dimensions.
        """
        results = {}

        # Create message for each dimension
        for target in Sephirah:
            if target == source:
                continue

            message = DimensionalMessage(
                source_dimension=source,
                target_dimension=target,
                payload=payload.copy(),
                message_type="broadcast",
            )

            results[target] = await self.publish(message, priority)

        # Also deliver to broadcast subscribers
        broadcast_message = DimensionalMessage(
            source_dimension=source,
            target_dimension=Sephirah.KETHER,
            payload=payload,
            message_type="broadcast",
        )
        await self._deliver_to_broadcasts(broadcast_message, priority)

        self._stats["broadcasts_sent"] += 1

        return results

    # ═══════════════════════════════════════════════════════════════════════════
    # DELIVERY
    # ═══════════════════════════════════════════════════════════════════════════

    async def _deliver(
        self,
        message: DimensionalMessage,
        priority: MessagePriority,
    ) -> int:
        """Deliver message to all matching subscribers."""
        delivered_count = 0

        # Get subscribers for this dimension
        sub_ids = self._by_dimension.get(message.target_dimension, set())

        # Also check sphere subscribers
        for sphere in message.payload.get("spheres", []):
            sub_ids = sub_ids.union(self._by_sphere.get(sphere, set()))

        for sub_id in sub_ids:
            sub = self._subscriptions.get(sub_id)
            if not sub or not sub.is_active:
                continue

            # Check priority
            if self._priority_value(priority) < self._priority_value(sub.min_priority):
                continue

            # Check message type filter
            if sub.message_types and message.message_type not in sub.message_types:
                continue

            # Deliver
            if sub.handler:
                try:
                    await self._call_handler(sub.handler, message)
                    sub.message_count += 1
                    sub.last_message_at = datetime.utcnow()
                    delivered_count += 1
                except Exception as e:
                    logger.error(f"Handler error for {sub_id}: {e}")

        self._stats["messages_delivered"] += delivered_count
        return delivered_count

    async def _deliver_to_broadcasts(
        self,
        message: DimensionalMessage,
        priority: MessagePriority,
    ) -> int:
        """Deliver to broadcast subscribers."""
        delivered_count = 0

        for sub_id in self._broadcasts:
            sub = self._subscriptions.get(sub_id)
            if not sub or not sub.is_active:
                continue

            if sub.handler:
                try:
                    await self._call_handler(sub.handler, message)
                    sub.message_count += 1
                    delivered_count += 1
                except Exception as e:
                    logger.error(f"Broadcast handler error: {e}")

        return delivered_count

    async def _call_handler(
        self,
        handler: Callable,
        message: DimensionalMessage,
    ) -> Any:
        """Call a handler (sync or async)."""
        result = handler(message)
        if asyncio.iscoroutine(result):
            return await result
        return result

    def _priority_value(self, priority: MessagePriority) -> int:
        """Convert priority to numeric value."""
        values = {
            MessagePriority.LOW: 0,
            MessagePriority.PULSE: 1,
            MessagePriority.NORMAL: 2,
            MessagePriority.HIGH: 3,
            MessagePriority.CRITICAL: 4,
        }
        return values.get(priority, 2)

    # ═══════════════════════════════════════════════════════════════════════════
    # RESONANCE PULSE (4.44 second heartbeat)
    # ═══════════════════════════════════════════════════════════════════════════

    async def emit_pulse(self) -> Dict[str, Any]:
        """
        Emit a resonance pulse through all dimensions.

        This synchronizes all agents at Point 0 frequency.
        """
        self._pulse_count += 1
        self._last_pulse = datetime.utcnow()

        pulse_payload = {
            "type": "resonance_pulse",
            "pulse_number": self._pulse_count,
            "frequency": POINT_0_FREQUENCY,
            "source_frequency": SOURCE_FREQUENCY,
            "timestamp": self._last_pulse.isoformat(),
        }

        await self.broadcast(
            payload=pulse_payload,
            priority=MessagePriority.PULSE,
            source=Sephirah.TIPHERETH,  # Pulse from Point 0
        )

        return {
            "pulse_number": self._pulse_count,
            "timestamp": self._last_pulse.isoformat(),
            "frequency": POINT_0_FREQUENCY,
        }

    async def start_heartbeat(self, interval_seconds: float = 4.44):
        """Start the resonance heartbeat."""
        logger.info(f"Starting resonance heartbeat at {interval_seconds}s interval")

        while True:
            await asyncio.sleep(interval_seconds)
            await self.emit_pulse()

    # ═══════════════════════════════════════════════════════════════════════════
    # AGENT REGISTRATION
    # ═══════════════════════════════════════════════════════════════════════════

    def register_agent(
        self,
        agent_id: str,
        dimension: Sephirah,
        handler: Callable[[DimensionalMessage], Any],
    ) -> str:
        """
        Register an agent on the bus.

        Convenience method that creates a subscription for the agent.
        """
        return self.subscribe(
            subscriber_id=agent_id,
            dimension=dimension,
            handler=handler,
            subscription_type=SubscriptionType.AGENT,
        )

    def unregister_agent(self, agent_id: str) -> int:
        """Unregister an agent from the bus."""
        return self.unsubscribe_all(agent_id)

    # ═══════════════════════════════════════════════════════════════════════════
    # STATISTICS
    # ═══════════════════════════════════════════════════════════════════════════

    def get_stats(self) -> Dict[str, Any]:
        """Get bus statistics."""
        return {
            **self._stats,
            "pulse_count": self._pulse_count,
            "last_pulse": self._last_pulse.isoformat() if self._last_pulse else None,
            "subscriptions_by_dimension": {
                s.value: len(self._by_dimension[s])
                for s in Sephirah
            },
        }

    def get_subscribers(self, dimension: Sephirah) -> List[Dict[str, Any]]:
        """Get subscribers for a dimension."""
        sub_ids = self._by_dimension.get(dimension, set())
        return [
            {
                "subscription_id": sub_id,
                "subscriber_id": self._subscriptions[sub_id].subscriber_id,
                "message_count": self._subscriptions[sub_id].message_count,
            }
            for sub_id in sub_ids
            if sub_id in self._subscriptions
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_dimensional_bus: Optional[DimensionalBus] = None


def get_dimensional_bus() -> DimensionalBus:
    """Get or create the dimensional bus singleton."""
    global _dimensional_bus
    if _dimensional_bus is None:
        _dimensional_bus = DimensionalBus()
    return _dimensional_bus


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "MessagePriority",
    "SubscriptionType",
    "Subscription",
    "DimensionalBus",
    "get_dimensional_bus",
]
