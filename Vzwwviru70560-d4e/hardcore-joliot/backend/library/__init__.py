"""
============================================================================
CHE·NU™ V69 — LIBRARY MODULE
============================================================================
Version: 1.0.0
Specs implemented:
- CHE-NU_LIB_UNIVERSAL_LITERATURE_ZONE.md
- CHE-NU_LIB_SEMANTIC_PUBLISHING_PROTOCOL.md
- CHE-NU_LIB_IMMERSIVE_READING_ENGINE.md
- CHE-NU_LIB_AUTHOR_EQUITY_SYSTEM.md

Concept: La Littera-Lattice — Un livre n'est plus un PDF mort,
mais un organisme culturel connecté.

Principle: GOUVERNANCE > EXÉCUTION, L'IA ne remplace jamais l'auteur
============================================================================
"""

# Models
from .models import (
    BookArtifact,
    ChapterChunk,
    PublishingStatus,
    LicenseType,
    ReaderProfile,
    ReadingMode,
    IntensityLevel,
    XRSceneManifest,
    Wallet,
    TipTransaction,
    SplitConfig,
    AutonomousPublishingContract,
    RevenueType,
    CreativeSuggestion,
    ConsistencyIssue,
    SemanticTranslation,
    SuggestionType,
    generate_id,
    compute_hash,
    sign_artifact,
)

# Publishing
from .publishing import (
    PublishingPipeline,
    TextNormalizer,
    OPAScreener,
    SemanticIndexer,
    create_pipeline,
    create_screener,
    create_indexer,
)

# Immersive Reading
from .immersive_reading import (
    ImmersiveReadingEngine,
    SceneGenerator,
    EmotionExtractor,
    AssetLibrary,
    create_engine,
    create_reader_profile,
)

# Author Equity
from .author_equity import (
    AuthorEquitySystem,
    WalletManager,
    TipService,
    RevenueDistributor,
    ContractManager,
    TrustMultiplier,
    create_equity_system,
    create_split_config,
)

# Literature Zone
from .literature_zone import (
    UniversalLiteratureZone,
    CreativeCompanion,
    SemanticTranslator,
    WorldConnector,
    create_literature_zone,
    create_companion,
    create_translator,
)

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Models
    "BookArtifact", "ChapterChunk", "PublishingStatus", "LicenseType",
    "ReaderProfile", "ReadingMode", "IntensityLevel", "XRSceneManifest",
    "Wallet", "TipTransaction", "SplitConfig", "AutonomousPublishingContract",
    "RevenueType", "CreativeSuggestion", "ConsistencyIssue", "SemanticTranslation",
    "SuggestionType",
    "generate_id", "compute_hash", "sign_artifact",
    # Publishing
    "PublishingPipeline", "TextNormalizer", "OPAScreener", "SemanticIndexer",
    "create_pipeline", "create_screener", "create_indexer",
    # Immersive Reading
    "ImmersiveReadingEngine", "SceneGenerator", "EmotionExtractor", "AssetLibrary",
    "create_engine", "create_reader_profile",
    # Author Equity
    "AuthorEquitySystem", "WalletManager", "TipService", "RevenueDistributor",
    "ContractManager", "TrustMultiplier", "create_equity_system", "create_split_config",
    # Literature Zone
    "UniversalLiteratureZone", "CreativeCompanion", "SemanticTranslator",
    "WorldConnector", "create_literature_zone", "create_companion", "create_translator",
]
