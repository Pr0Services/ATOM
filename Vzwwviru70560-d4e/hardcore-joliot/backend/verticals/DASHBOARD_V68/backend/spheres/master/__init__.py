"""
CHE·NU V68 Master Dashboard Module
AT·OM Vision - Le Tableau de Bord Maitre

La frequence 999Hz est notre objectif:
Quand tout est bleu cobalt, le systeme chante.

GOVERNANCE COMPLIANCE:
- Rule #1: Cross-domain interventions require APPROVAL
- Rule #5: All listings ALPHABETICAL or CHRONOLOGICAL
- Rule #6: Full audit trail from all sources
"""

from .agents.master_dashboard_agent import (
    MasterDashboardAgent,
    get_master_dashboard_agent,
    DomainType,
    HealthStatus,
    AlertType,
    TrendDirection,
    DomainStatus,
    GlobalIndex,
    CrossDomainAlert,
    HeatmapCell,
    SystemMetrics,
    STATUS_COLORS,
)

__all__ = [
    "MasterDashboardAgent",
    "get_master_dashboard_agent",
    "DomainType",
    "HealthStatus",
    "AlertType",
    "TrendDirection",
    "DomainStatus",
    "GlobalIndex",
    "CrossDomainAlert",
    "HeatmapCell",
    "SystemMetrics",
    "STATUS_COLORS",
]

__version__ = "68.0.0"
__module__ = "Master Dashboard"
