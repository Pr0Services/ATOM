"""
============================================================================
CHE·NU™ V69 — LIBRARY MODULE MODELS
============================================================================
Version: 1.0.0
Specs: GPT1/CHE-NU_LIB_*.md
Principle: GOUVERNANCE > EXÉCUTION

"Un livre n'est plus un PDF mort, mais un organisme culturel connecté."
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import uuid
import hashlib
import json


# ============================================================================
# BOOK ARTIFACT MODELS
# ============================================================================

class LicenseType(str, Enum):
    """License types for books"""
    ALL_RIGHTS_RESERVED = "all_rights_reserved"
    CREATIVE_COMMONS = "creative_commons"
    PUBLIC_DOMAIN = "public_domain"
    REMIX_ALLOWED = "remix_allowed"
    ADAPTATION_ALLOWED = "adaptation_allowed"


class PublishingStatus(str, Enum):
    """Publishing status"""
    DRAFT = "draft"
    UPLOADED = "uploaded"
    NORMALIZED = "normalized"
    SCREENED = "screened"
    INDEXED = "indexed"
    SIGNED = "signed"
    PUBLISHED = "published"
    FLAGGED = "flagged"


@dataclass
class ChapterChunk:
    """
    Unit of reading & payment.
    
    Per spec: unité de lecture & paiement
    """
    chunk_id: str
    chapter_no: int
    order_index: int
    
    # Content
    text: str
    word_count: int = 0
    
    # Audio (if applicable)
    timecode_map: Dict[str, float] = field(default_factory=dict)
    
    # Rights & payment
    rights: Dict[str, Any] = field(default_factory=dict)
    tip_wallet_ref: str = ""
    
    # Semantic
    semantic_tags: List[str] = field(default_factory=list)
    emotion_markers: List[str] = field(default_factory=list)


@dataclass
class BookArtifact:
    """
    A signed book container.
    
    Per spec: BookArtifact (conteneur signé)
    """
    book_id: str
    title: str
    author_id: str
    
    # Metadata
    language_original: str = "fr"
    description: str = ""
    genres: List[str] = field(default_factory=list)
    
    # License
    license: LicenseType = LicenseType.ALL_RIGHTS_RESERVED
    
    # Content
    chapters: List[ChapterChunk] = field(default_factory=list)
    
    # Semantic indexing
    semantic_index_ref: str = ""
    semantic_vector: List[float] = field(default_factory=list)
    
    # Governance
    opa_policy_ref: str = ""
    
    # Signatures
    signatures: List[Dict[str, str]] = field(default_factory=list)
    
    # Status
    status: PublishingStatus = PublishingStatus.DRAFT
    
    # WorldEngine connections
    world_links: List[str] = field(default_factory=list)
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None


# ============================================================================
# XR READING MODELS
# ============================================================================

class ReadingMode(str, Enum):
    """Reading modes"""
    READ_ONLY = "read_only"
    GUIDED = "guided"
    IMMERSIVE = "immersive"


class IntensityLevel(str, Enum):
    """Scene intensity levels"""
    CALM = "calm"
    NEUTRAL = "neutral"
    DRAMATIC = "dramatic"
    INTENSE = "intense"


@dataclass
class ReaderProfile:
    """
    Reader preferences for XR experience.
    
    Per spec: reader_profile (préférences, sensibilité)
    """
    reader_id: str
    
    # Preferences
    preferred_mode: ReadingMode = ReadingMode.READ_ONLY
    intensity_preference: IntensityLevel = IntensityLevel.NEUTRAL
    
    # Accessibility
    dyslexia_mode: bool = False
    audio_first: bool = False
    high_contrast: bool = False
    
    # Sensitivities
    avoid_themes: List[str] = field(default_factory=list)
    
    # Performance
    max_scene_complexity: int = 5  # 1-10


@dataclass
class XRSceneManifest:
    """
    XR scene configuration for reading.
    
    Per spec outputs: XR Scene Manifest (XRS)
    """
    manifest_id: str
    chunk_id: str
    
    # Environment
    environment_theme: str = "library"
    lighting_profile: Dict[str, Any] = field(default_factory=dict)
    soundscape_profile: Dict[str, Any] = field(default_factory=dict)
    haptic_profile: Dict[str, Any] = field(default_factory=dict)
    
    # Semantic markers
    semantic_markers: List[Dict[str, Any]] = field(default_factory=list)
    
    # Controls
    intensity: IntensityLevel = IntensityLevel.NEUTRAL
    mode: ReadingMode = ReadingMode.READ_ONLY
    
    # Signature
    signature: str = ""


# ============================================================================
# AUTHOR EQUITY MODELS
# ============================================================================

class RevenueType(str, Enum):
    """Revenue types"""
    TIP = "tip"
    MICRO_LICENSE = "micro_license"
    SPONSORSHIP = "sponsorship"
    SCHOLAR_GRANT = "scholar_grant"


@dataclass
class Wallet:
    """A wallet for payments"""
    wallet_id: str
    owner_id: str
    owner_type: str  # author, collaborator, platform, community
    
    balance: float = 0.0
    currency: str = "CHE-NU"


@dataclass
class TipTransaction:
    """
    A tip transaction.
    
    Per spec: Tips (par chunk / chapitre / livre)
    """
    tx_id: str
    from_wallet: str
    to_wallet: str
    
    # Target
    book_id: str
    chunk_id: Optional[str] = None
    
    # Amount
    amount: float = 0.0
    currency: str = "CHE-NU"
    
    # Timestamp
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SplitConfig:
    """
    Revenue split configuration.
    
    Per spec: Wallets & splits
    """
    author_split: float = 0.85  # 85% to author
    collaborator_splits: Dict[str, float] = field(default_factory=dict)
    platform_fee: float = 0.05  # 5% platform
    community_fund: float = 0.10  # 10% community


@dataclass
class AutonomousPublishingContract:
    """
    Autonomous publishing contract (CEA).
    
    Per spec: Contrat d'édition autonome
    """
    contract_id: str
    book_id: str
    author_id: str
    
    # Rights
    rights_granted: List[str] = field(default_factory=list)
    
    # Revenue
    split_config: SplitConfig = field(default_factory=SplitConfig)
    
    # Conditions
    withdrawal_conditions: Dict[str, Any] = field(default_factory=dict)
    content_policy: str = ""
    
    # Signature
    signature: str = ""
    signed_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# CREATIVE COMPANION MODELS
# ============================================================================

class SuggestionType(str, Enum):
    """Types of creative suggestions"""
    STRUCTURE = "structure"
    STYLE = "style"
    CONSISTENCY = "consistency"
    RHYTHM = "rhythm"


@dataclass
class CreativeSuggestion:
    """
    A suggestion from the Creative Companion.
    
    Per spec: Suggestions stylistiques optionnelles
    """
    suggestion_id: str
    book_id: str
    chunk_id: str
    
    # Suggestion
    suggestion_type: SuggestionType
    description: str
    
    # Location
    start_position: int = 0
    end_position: int = 0
    
    # Status
    accepted: Optional[bool] = None  # None = not reviewed yet
    
    # Governance: No automatic rewrite
    auto_applied: bool = False  # Always False per spec


@dataclass
class ConsistencyIssue:
    """
    A detected consistency issue.
    
    Per spec: Détection d'incohérences (personnages, chronologie, concepts)
    """
    issue_id: str
    book_id: str
    
    # Issue type
    issue_type: str  # character, chronology, concept
    
    # Details
    description: str
    locations: List[Dict[str, int]] = field(default_factory=list)
    
    # Resolution
    resolved: bool = False


# ============================================================================
# SEMANTIC TRANSLATION MODELS
# ============================================================================

@dataclass
class SemanticTranslation:
    """
    A semantic translation.
    
    Per spec: Traduction par intention, non par mot
    """
    translation_id: str
    book_id: str
    chunk_id: str
    
    # Languages
    source_language: str
    target_language: str
    
    # Content
    translated_text: str
    
    # Quality
    rhythm_preserved: bool = True
    metaphors_adapted: bool = True
    
    # Signature
    signature: str = ""


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())


def compute_hash(data: Any) -> str:
    """Compute hash of data"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def sign_artifact(data: Dict[str, Any], signer_id: str) -> str:
    """Sign an artifact"""
    payload = json.dumps(data, sort_keys=True)
    return compute_hash(f"{payload}:{signer_id}")
