"""
============================================================================
CHE·NU™ V69 — XR PACK
============================================================================
Version: 1.6.0
Purpose: Scalable XR visualization layer for decision cockpit
Principle: XR = READ ONLY. All computation done offline.

The XR Pack provides:
- Chunked replay for progressive loading
- Divergence analysis for executive focus
- Heatmaps for visual intensity mapping
- Ed25519/Hybrid signatures for integrity
- CDN-friendly immutable artifacts

Usage:
    from xr_pack import XRPackBuilder
    
    # Build pack
    builder = XRPackBuilder(
        simulation_id="sim-001",
        tenant_id="enterprise",
    )
    
    builder.add_simulation_states(states)
    builder.set_baseline(baseline_states)
    builder.add_scenario(scenario_states, "aggressive")
    
    pack = builder.build()
    
    # Sign with hybrid signature
    signed_pack = builder.sign()
    
    # Export
    builder.export("/path/to/output")
============================================================================
"""

# Models
from .models import (
    # Enums
    ReplayMode,
    PackStatus,
    # Manifest
    CacheHints,
    ManifestV1,
    # Explain
    ExplainEntry,
    ExplainV1,
    # Heatmap
    SparklineData,
    SphereHeatmap,
    HeatmapV1,
    # Diff
    DivergencePoint,
    DivergenceConfig,
    ScenarioDiff,
    DiffV1,
    # Checksums
    FileChecksum,
    ChecksumsV1,
    # Replay
    ReplayFrame,
    ReplayChunk,
    ChunkReference,
    ReplayIndexV1,
    # Signature
    XRPackSignatureV1,
    XRPackPublicKeyV1,
    # Complete pack
    XRPackV1,
)

# Divergence
from .divergence import (
    TimelineSnapshot,
    Timeline,
    DivergenceCalculator,
    create_timeline_from_states,
    calculate_divergence,
)

# Replay
from .replay import (
    ReplayChunker,
    ChunkFileGenerator,
    ChunkLoader,
)

# Builder
from .builder import XRPackBuilder

# Verify
from .verify import (
    XRPackVerificationResult,
    XRPackVerifier,
    verify_xr_pack,
)

__version__ = "1.6.0"

__all__ = [
    # Version
    "__version__",
    # Enums
    "ReplayMode",
    "PackStatus",
    # Manifest
    "CacheHints",
    "ManifestV1",
    # Explain
    "ExplainEntry",
    "ExplainV1",
    # Heatmap
    "SparklineData",
    "SphereHeatmap",
    "HeatmapV1",
    # Diff
    "DivergencePoint",
    "DivergenceConfig",
    "ScenarioDiff",
    "DiffV1",
    # Checksums
    "FileChecksum",
    "ChecksumsV1",
    # Replay
    "ReplayFrame",
    "ReplayChunk",
    "ChunkReference",
    "ReplayIndexV1",
    # Signature
    "XRPackSignatureV1",
    "XRPackPublicKeyV1",
    # Complete pack
    "XRPackV1",
    # Divergence
    "TimelineSnapshot",
    "Timeline",
    "DivergenceCalculator",
    "create_timeline_from_states",
    "calculate_divergence",
    # Replay
    "ReplayChunker",
    "ChunkFileGenerator",
    "ChunkLoader",
    # Builder
    "XRPackBuilder",
    # Verify
    "XRPackVerificationResult",
    "XRPackVerifier",
    "verify_xr_pack",
]
