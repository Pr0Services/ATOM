"""
============================================================================
CHE·NU™ V69 — XR/UI MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_TIMELINE_DIVERGENCE_UI.md
- CHE-NU_LAB_WORKBENCH_XR.md
- CHE-NU_XR_CAUSAL_INTERVENTION_UX.md
- CHE-NU_XR_CAUSAL_TRACE_VISUALIZATION.md

"XR = espace de compréhension, jamais d'exécution"

Principle: XR = READ ONLY, GOUVERNANCE > EXÉCUTION
Value: Executive clarity, Strategic insight, Investor-grade visualization
============================================================================
"""

# Models
from .models import (
    RenderMode,
    InteractionType,
    ImpactColor,
    WorkbenchTool,
    Timeline,
    TimelinePoint,
    DivergenceMarker,
    RiskHeatmapCell,
    WorkbenchArtifact,
    ToolResult,
    CausalProxy,
    RippleWave,
    InterventionDraft,
    CausalPath,
    UncertaintyNode,
    ConterfactualHeatmap,
    XRPack,
    generate_id,
    compute_hash,
    sign_xr_pack,
)

# Timeline Divergence
from .timeline import (
    TimelineDivergenceVisualization,
    TimelineBuilder,
    DivergenceDetector,
    RiskHeatmapGenerator,
    create_timeline_visualization,
)

# Lab Workbench
from .workbench import (
    LabWorkbench,
    StressTester,
    SynthesisReactor,
    Chronos,
    CausalSpectrometer,
    create_workbench,
)

# Causal Intervention
from .causal_intervention import (
    InterventionSystem,
    CausalProxyManager,
    RippleEffectEngine,
    CausalMagnifier,
    create_intervention_system,
)

# Causal Trace
from .causal_trace import (
    CausalTraceVisualization,
    CausalPathRenderer,
    UncertaintyNodeManager,
    DoInterventionVisualizer,
    CounterfactualHeatmapGenerator,
    create_causal_trace_viz,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "RenderMode", "InteractionType", "ImpactColor", "WorkbenchTool",
    "Timeline", "TimelinePoint", "DivergenceMarker", "RiskHeatmapCell",
    "WorkbenchArtifact", "ToolResult",
    "CausalProxy", "RippleWave", "InterventionDraft",
    "CausalPath", "UncertaintyNode", "ConterfactualHeatmap",
    "XRPack",
    "generate_id", "compute_hash", "sign_xr_pack",
    # Timeline
    "TimelineDivergenceVisualization", "TimelineBuilder",
    "DivergenceDetector", "RiskHeatmapGenerator",
    "create_timeline_visualization",
    # Workbench
    "LabWorkbench", "StressTester", "SynthesisReactor",
    "Chronos", "CausalSpectrometer", "create_workbench",
    # Intervention
    "InterventionSystem", "CausalProxyManager",
    "RippleEffectEngine", "CausalMagnifier",
    "create_intervention_system",
    # Causal Trace
    "CausalTraceVisualization", "CausalPathRenderer",
    "UncertaintyNodeManager", "DoInterventionVisualizer",
    "CounterfactualHeatmapGenerator", "create_causal_trace_viz",
]
