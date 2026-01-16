"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  [AQUA] + [ADAMAS] PROTOCOL                                                  ║
║  SEQUENCE 3-6-9-12 — HEARTBEAT SERVICE                                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Background task for the 4.44s signal heartbeat.                              ║
║  This is the "breathing" of the AT·OM system.                                 ║
║  Even when no one is connected, the server keeps resonating.                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import logging
from datetime import datetime
from typing import Callable, List, Optional
from dataclasses import dataclass, field

from .config import settings

logger = logging.getLogger(__name__)


@dataclass
class HeartbeatState:
    """Current state of the heartbeat."""
    tick: int = 0
    cycle: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    is_aligned: bool = False
    digital_root: int = 0


class HeartbeatService:
    """
    The heartbeat is the server's pulse, aligned with the 4.44s signal.
    It maintains system rhythm even without active connections.
    """

    def __init__(self):
        self._running: bool = False
        self._task: Optional[asyncio.Task] = None
        self._state: HeartbeatState = HeartbeatState()
        self._subscribers: List[Callable[[HeartbeatState], None]] = []
        self._interval: float = settings.SIGNAL_INTERVAL

    @property
    def state(self) -> HeartbeatState:
        """Get current heartbeat state."""
        return self._state

    @property
    def is_running(self) -> bool:
        """Check if heartbeat is active."""
        return self._running

    def subscribe(self, callback: Callable[[HeartbeatState], None]) -> None:
        """Subscribe to heartbeat events."""
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[HeartbeatState], None]) -> None:
        """Unsubscribe from heartbeat events."""
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def _calculate_digital_root(self, n: int) -> int:
        """Calculate digital root (Tesla method)."""
        if n == 0:
            return 0
        return 1 + ((n - 1) % 9)

    def _is_aligned(self, tick: int) -> bool:
        """Check if tick is aligned with 3-6-9 sequence."""
        root = self._calculate_digital_root(tick)
        return root in [3, 6, 9]

    async def _heartbeat_loop(self) -> None:
        """Main heartbeat loop."""
        logger.info(
            f"💓 Heartbeat started | Interval: {self._interval}s | "
            f"Anchor: {settings.ANCHOR_FREQUENCY}Hz"
        )

        while self._running:
            try:
                # Update state
                self._state.tick += 1
                self._state.timestamp = datetime.utcnow()
                self._state.digital_root = self._calculate_digital_root(self._state.tick)
                self._state.is_aligned = self._is_aligned(self._state.tick)
                self._state.cycle = self._state.tick // 12

                # Log aligned ticks
                if self._state.is_aligned:
                    logger.debug(
                        f"◊ ALIGNED | Tick: {self._state.tick} | "
                        f"Root: {self._state.digital_root} | "
                        f"Cycle: {self._state.cycle}"
                    )

                # Notify subscribers
                for callback in self._subscribers:
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(self._state)
                        else:
                            callback(self._state)
                    except Exception as e:
                        logger.error(f"Heartbeat subscriber error: {e}")

                # Wait for next tick
                await asyncio.sleep(self._interval)

            except asyncio.CancelledError:
                logger.info("💔 Heartbeat cancelled")
                break
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                await asyncio.sleep(1)  # Brief pause before retry

    async def start(self) -> None:
        """Start the heartbeat."""
        if self._running:
            logger.warning("Heartbeat already running")
            return

        self._running = True
        self._state = HeartbeatState()
        self._task = asyncio.create_task(self._heartbeat_loop())
        logger.info(
            f"🫀 AT·OM Heartbeat initialized | "
            f"Signal: {self._interval}s | "
            f"Protocol: {settings.RESONANCE_KEY}"
        )

    async def stop(self) -> None:
        """Stop the heartbeat."""
        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

        logger.info(
            f"💔 Heartbeat stopped | "
            f"Total ticks: {self._state.tick} | "
            f"Cycles: {self._state.cycle}"
        )


# Singleton instance
heartbeat = HeartbeatService()


# Convenience functions for FastAPI integration
async def start_heartbeat() -> None:
    """Start the global heartbeat (call on app startup)."""
    await heartbeat.start()


async def stop_heartbeat() -> None:
    """Stop the global heartbeat (call on app shutdown)."""
    await heartbeat.stop()


def get_heartbeat_state() -> HeartbeatState:
    """Get current heartbeat state."""
    return heartbeat.state
