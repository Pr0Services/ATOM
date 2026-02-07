"""
═══════════════════════════════════════════════════════════════════════════════
AT·OM ENGINES — Multidimensional Operating System Core
═══════════════════════════════════════════════════════════════════════════════

The engines power the AT·OM Multidimensional OS:

1. DIMENSIONAL ROUTER (Kether Gateway)
   - Routes all inter-dimensional communication via Kether (999 Hz)
   - Calibrates messages at Point 0 / Tiphereth (444 Hz)
   - Enforces Human Sovereignty (Rule #1) via checkpoints

2. DIMENSIONAL PROVIDERS
   - 10 providers, one per Sephirah
   - Each connects to external APIs (OpenRouter, Anthropic, Hedera, etc.)

3. KABBALAH ENGINE
   - Tree of Life data structures
   - 10 Sephiroth + 22 Paths
   - Frequency mappings and harmonic calculations

ARCHITECTURE:
                    ┌─────────────────────┐
                    │   KETHER (999 Hz)   │
                    │   Central Router    │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   [CHOKMAH]              [TIPHERETH]             [BINAH]
    888 Hz                  444 Hz                  777 Hz
   Anthropic               Hedera                Stability
        │                   POINT 0                   │
        └──────────────────────┼──────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │          │           │           │          │
   [CHESED]  [GEBURAH]   [NETZACH]     [HOD]    [YESOD]
    555 Hz     333 Hz      666 Hz      222 Hz    111 Hz
   Supabase     OPA       Runway    ElevenLabs   Redis
        │          │           │           │          │
        └──────────┴───────────┼───────────┴──────────┘
                               │
                    ┌──────────┴──────────┐
                    │   MALKUTH (68 Hz)   │
                    │   Frontend/Manifest │
                    └─────────────────────┘

VERSION: 1.0.0
═══════════════════════════════════════════════════════════════════════════════
"""

# Dimensional Router
from .dimensional_router import (
    Sephirah,
    DimensionalMessage,
    DimensionalPath,
    DimensionalRouter,
    get_dimensional_router,
    route_to_dimension,
    get_dimension_for_sphere,
    get_frequency_for_sphere,
    SEPHIROTH_FREQUENCIES,
    SEPHIROTH_PROVIDERS,
    SEPHIROTH_SPHERES,
    SEPHIROTH_AGENT_COUNTS,
    POINT_0_FREQUENCY,
    POINT_0_SEPHIRAH,
    SOURCE_FREQUENCY,
    SOURCE_SEPHIRAH,
    PHI,
)

# Dimensional Providers
from .dimensional_providers import (
    DimensionalProvider,
    KetherProvider,
    ChokmahProvider,
    BinahProvider,
    TipherethProvider,
    ChesedProvider,
    GeburahProvider,
    NetzachProvider,
    HodProvider,
    YesodProvider,
    MalkuthProvider,
    create_all_providers,
    register_all_providers,
    initialize_dimensional_system,
)

# Dimensional Bus (Inter-dimensional communication)
from .dimensional_bus import (
    MessagePriority,
    SubscriptionType,
    Subscription,
    DimensionalBus,
    get_dimensional_bus,
)


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK START
# ═══════════════════════════════════════════════════════════════════════════════

def start_dimensional_os():
    """
    Start the AT·OM Multidimensional Operating System.

    Returns the initialized router with all providers registered.

    Usage:
        from backend.app.engines import start_dimensional_os, route_to_dimension, Sephirah

        # Initialize the system
        router = start_dimensional_os()

        # Route a message
        response = await route_to_dimension(
            target=Sephirah.NETZACH,
            payload={"action": "generate_video", "prompt": "A phoenix rising"},
        )

        # Get system status
        status = router.get_tree_status()
    """
    return initialize_dimensional_system()


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # Quick start
    "start_dimensional_os",

    # Router
    "Sephirah",
    "DimensionalMessage",
    "DimensionalPath",
    "DimensionalRouter",
    "get_dimensional_router",
    "route_to_dimension",
    "get_dimension_for_sphere",
    "get_frequency_for_sphere",

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

    # Providers
    "DimensionalProvider",
    "KetherProvider",
    "ChokmahProvider",
    "BinahProvider",
    "TipherethProvider",
    "ChesedProvider",
    "GeburahProvider",
    "NetzachProvider",
    "HodProvider",
    "YesodProvider",
    "MalkuthProvider",
    "create_all_providers",
    "register_all_providers",
    "initialize_dimensional_system",

    # Bus
    "MessagePriority",
    "SubscriptionType",
    "Subscription",
    "DimensionalBus",
    "get_dimensional_bus",
]
