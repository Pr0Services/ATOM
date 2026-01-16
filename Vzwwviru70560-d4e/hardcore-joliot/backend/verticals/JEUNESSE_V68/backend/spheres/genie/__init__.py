"""
CHE·NU V68 Génie de Demain Module
L'Allumage du Feu Intérieur

═══════════════════════════════════════════════════════════════════════════════
"L'éducation n'est pas un remplissage de vase, mais l'allumage d'un feu."
                        - Apprentissage adapté, souveraineté dès l'enfance
═══════════════════════════════════════════════════════════════════════════════

LES 3 PILIERS:
1. LE CLAN - Apprentissage par passion, pas par âge
2. L'AGENT MENTOR - Révélateur de génie, pas évaluateur
3. LE RÉEL - Le monde est la salle de classe

PRIVACY: Protection renforcée des mineurs
GOVERNANCE: Approbation parentale pour projets réels
"""

from .agents.genie_demain_agent import (
    GenieDemainAgent,
    get_genie_demain_agent,
    # Enums
    PassionDomain,
    LearningRhythm,
    GeniusType,
    ClanRole,
    ProjectPhase,
    AccomplishmentType,
    ATOMModule,
    # Data models
    YoungLearner,
    Clan,
    RealWorldProject,
    Accomplishment,
    MentorProfile,
    GeniusObservation,
    JeunesseMetrics,
)

__all__ = [
    # Main agent
    "GenieDemainAgent",
    "get_genie_demain_agent",
    # Enums
    "PassionDomain",
    "LearningRhythm",
    "GeniusType",
    "ClanRole",
    "ProjectPhase",
    "AccomplishmentType",
    "ATOMModule",
    # Data models
    "YoungLearner",
    "Clan",
    "RealWorldProject",
    "Accomplishment",
    "MentorProfile",
    "GeniusObservation",
    "JeunesseMetrics",
]

__version__ = "68.0.0"
__module__ = "Génie de Demain"
