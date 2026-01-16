"""
CHE·NU V68 Community Pulse Module
Systeme d'Analyse de l'Harmonie (SAH)

PRIVACY ULTRA-STRICT:
- Zone-level data only
- NO individual tracking
- Aggregated + anonymized

GOVERNANCE COMPLIANCE:
- Rule #1: Sensitive interventions require APPROVAL
- Rule #5: Zones ALPHABETICAL
- Rule #6: Full audit trail
"""

from .agents.harmony_analysis_agent import (
    HarmonyAnalysisAgent,
    get_harmony_analysis_agent,
    EmotionalDimension,
    HarmonyLevel,
    SignalSource,
    InterventionType,
    FeedbackLoopType,
    AlertSeverity,
    ZoneProfile,
    AggregatedSignal,
    HarmonyAlert,
    CommunityIntervention,
    FeedbackLoop,
    HarmonyMetrics,
)

__all__ = [
    "HarmonyAnalysisAgent",
    "get_harmony_analysis_agent",
    "EmotionalDimension",
    "HarmonyLevel",
    "SignalSource",
    "InterventionType",
    "FeedbackLoopType",
    "AlertSeverity",
    "ZoneProfile",
    "AggregatedSignal",
    "HarmonyAlert",
    "CommunityIntervention",
    "FeedbackLoop",
    "HarmonyMetrics",
]

__version__ = "68.0.0"
__module__ = "Community Pulse"
