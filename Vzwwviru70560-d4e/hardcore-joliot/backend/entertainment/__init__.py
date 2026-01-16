"""
============================================================================
CHE·NU™ V69 — ENTERTAINMENT MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_ENT_GAME_GEN_LLM_TEMPLATES.md
- CHE-NU_ENT_LLM_GAME_LOGIC_PROMPTS.md
- CHE-NU_ENT_TRUST_SCORE_LEADERBOARD.md

Principle: GOUVERNANCE > EXÉCUTION
CHE·NU ne crée pas un moteur de jeu.
Il génère des templates interprétables par le moteur XR existant.
============================================================================
"""

# Models
from .models import (
    GameManifest,
    GameTemplateType,
    GameLayer,
    NarrativeLayer,
    MechanicLayer,
    VisualLayer,
    GameAction,
    SimulationResult,
    GameFeedback,
    TrustScore,
    TrustPillar,
    LeaderboardEntry,
    TrustBadge,
    CrisisCard,
    ScenarioBranch,
    generate_id,
    sign_artifact,
    anonymize_id,
)

# Game Generator
from .game_generator import (
    GameTemplateGenerator,
    OptimizerGenerator,
    CrisisProtocolGenerator,
    ExplorerGenerator,
    create_generator,
)

# Game Logic
from .game_logic import (
    GameLogicEngine,
    GameLogicCoordinator,
    PromptManager,
    create_coordinator,
    create_engine,
    get_prompt_manager,
)

# Leaderboard
from .leaderboard import (
    TrustScoreSystem,
    TrustScoreCalculator,
    LeaderboardManager,
    BadgeIssuer,
    XRVisualization,
    create_trust_system,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "GameManifest", "GameTemplateType", "GameLayer",
    "NarrativeLayer", "MechanicLayer", "VisualLayer",
    "GameAction", "SimulationResult", "GameFeedback",
    "TrustScore", "TrustPillar", "LeaderboardEntry", "TrustBadge",
    "CrisisCard", "ScenarioBranch",
    "generate_id", "sign_artifact", "anonymize_id",
    # Game Generator
    "GameTemplateGenerator", "OptimizerGenerator",
    "CrisisProtocolGenerator", "ExplorerGenerator",
    "create_generator",
    # Game Logic
    "GameLogicEngine", "GameLogicCoordinator", "PromptManager",
    "create_coordinator", "create_engine", "get_prompt_manager",
    # Leaderboard
    "TrustScoreSystem", "TrustScoreCalculator",
    "LeaderboardManager", "BadgeIssuer", "XRVisualization",
    "create_trust_system",
]
