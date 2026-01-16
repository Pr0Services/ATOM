"""
CHE·NU V68 Biodiversity Module
Sentinelles de la Biodiversite

GOVERNANCE COMPLIANCE:
- Rule #1: Protected species interventions require APPROVAL
- Rule #5: Species ALPHABETICAL
- Rule #6: Full audit trail
"""

from .agents.biodiversity_sentinel_agent import (
    BiodiversitySentinelAgent,
    get_biodiversity_sentinel_agent,
    TaxonomicGroup,
    ConservationStatus,
    ThreatType,
    MigrationType,
    ObservationType,
    AlertPriority,
    CorridorStatus,
    GeoPoint,
    Species,
    Observation,
    ThreatAlert,
    MigrationRoute,
    EcologicalCorridor,
    NestingSite,
    BiodiversityMetrics,
)

__all__ = [
    "BiodiversitySentinelAgent",
    "get_biodiversity_sentinel_agent",
    "TaxonomicGroup",
    "ConservationStatus",
    "ThreatType",
    "MigrationType",
    "ObservationType",
    "AlertPriority",
    "CorridorStatus",
    "GeoPoint",
    "Species",
    "Observation",
    "ThreatAlert",
    "MigrationRoute",
    "EcologicalCorridor",
    "NestingSite",
    "BiodiversityMetrics",
]

__version__ = "68.0.0"
__module__ = "Sentinelles Biodiversite"
