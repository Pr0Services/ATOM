"""
============================================================================
CHE·NU™ V69 — SCHOLAR MODULE MODELS
============================================================================
Version: 1.0.0
Specs: GPT1/CHE-NU_SCH_*.md
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
import hashlib
import json
import uuid


# ============================================================================
# CAUSAL KNOWLEDGE GRAPH MODELS
# ============================================================================

class CausalLinkStrength(str, Enum):
    """Strength of causal links"""
    WEAK = "weak"  # p-value > 0.05
    MODERATE = "moderate"  # 0.01 < p-value <= 0.05
    STRONG = "strong"  # 0.001 < p-value <= 0.01
    VERY_STRONG = "very_strong"  # p-value <= 0.001


class VerificationStatus(str, Enum):
    """Verification status for discoveries"""
    UNVERIFIED = "unverified"
    PENDING = "pending"
    VERIFIED = "verified"
    DISPUTED = "disputed"
    RETRACTED = "retracted"


@dataclass
class CausalNode:
    """
    A node in the causal knowledge graph.
    
    Per spec: Nœud = Découverte / Artifact
    """
    node_id: str
    title: str
    domain: str  # biology, engineering, physics, etc.
    artifact_ref: Optional[str] = None  # Reference to artifact
    
    # Metadata
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    authors: List[str] = field(default_factory=list)
    
    # Verification
    status: VerificationStatus = VerificationStatus.UNVERIFIED
    reproducibility_score: float = 0.0  # 0-1
    
    # Position in XR (for visualization)
    xr_position: Dict[str, float] = field(default_factory=lambda: {"x": 0, "y": 0, "z": 0})
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    verified_at: Optional[datetime] = None


@dataclass
class CausalLink:
    """
    A causal link between nodes.
    
    Per spec: Lien = Preuve causale (p-value, source, reproductibilité)
    """
    link_id: str
    source_id: str
    target_id: str
    
    # Causal evidence
    p_value: float  # Statistical significance
    effect_size: float  # Magnitude of effect
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    
    # Strength (derived from p-value)
    strength: CausalLinkStrength = CausalLinkStrength.WEAK
    
    # Sources and verification
    sources: List[str] = field(default_factory=list)
    reproducibility_score: float = 0.0
    verified: bool = False
    
    # Signature (per spec: signatures immuables)
    signature: Optional[str] = None
    signed_by: Optional[str] = None
    
    # XR visualization (per spec: couleur/épaisseur = force)
    xr_color: str = "#888888"
    xr_thickness: float = 1.0
    
    def compute_strength(self) -> CausalLinkStrength:
        """Compute strength from p-value"""
        if self.p_value <= 0.001:
            self.strength = CausalLinkStrength.VERY_STRONG
        elif self.p_value <= 0.01:
            self.strength = CausalLinkStrength.STRONG
        elif self.p_value <= 0.05:
            self.strength = CausalLinkStrength.MODERATE
        else:
            self.strength = CausalLinkStrength.WEAK
        
        # Update XR properties
        thickness_map = {
            CausalLinkStrength.WEAK: 1.0,
            CausalLinkStrength.MODERATE: 2.0,
            CausalLinkStrength.STRONG: 3.0,
            CausalLinkStrength.VERY_STRONG: 4.0,
        }
        color_map = {
            CausalLinkStrength.WEAK: "#666666",
            CausalLinkStrength.MODERATE: "#4488FF",
            CausalLinkStrength.STRONG: "#44FF88",
            CausalLinkStrength.VERY_STRONG: "#FFD700",
        }
        
        self.xr_thickness = thickness_map[self.strength]
        self.xr_color = color_map[self.strength]
        
        return self.strength


# ============================================================================
# ANALOGICAL SEARCH MODELS
# ============================================================================

@dataclass
class TopologicalPattern:
    """
    A topological pattern for analogical matching.
    
    Per spec: Identifier des problèmes mathématiquement équivalents
    """
    pattern_id: str
    name: str
    
    # Pattern structure
    node_count: int
    edge_count: int
    structure_hash: str  # Hash of the topological structure
    
    # Features for matching
    features: Dict[str, float] = field(default_factory=dict)
    
    # Domain info
    source_domain: str = ""
    abstraction_level: int = 0  # Higher = more abstract


@dataclass
class AnalogicalMatch:
    """
    A match between two patterns.
    
    Per spec: Pattern matching (>85%)
    """
    match_id: str
    pattern_a: str  # Pattern ID
    pattern_b: str  # Pattern ID
    
    # Similarity
    similarity_score: float  # 0-1
    matched_features: List[str] = field(default_factory=list)
    
    # Cross-domain
    domain_a: str = ""
    domain_b: str = ""
    
    # Explanation
    mapping_explanation: str = ""


# ============================================================================
# IMPACT SIMULATOR MODELS
# ============================================================================

class ImpactMetric(str, Enum):
    """Impact metrics for simulation"""
    GDP = "gdp"
    PUBLIC_HEALTH = "public_health"
    RESILIENCE = "resilience"
    SUSTAINABILITY = "sustainability"
    INNOVATION = "innovation"
    EMPLOYMENT = "employment"


@dataclass
class FundingScenario:
    """
    A funding scenario for impact simulation.
    
    Per spec inputs: Montant, Domaine, Horizon temporel
    """
    scenario_id: str
    name: str
    
    # Inputs per spec
    amount: float  # Funding amount
    domain: str  # Research domain
    time_horizon_years: int  # Time horizon
    
    # Additional parameters
    allocation: Dict[str, float] = field(default_factory=dict)  # Sub-allocations
    assumptions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImpactResult:
    """
    Impact simulation result.
    
    Per spec outputs: PIB, santé publique, résilience, heatmaps XR, scoring
    """
    result_id: str
    scenario_id: str
    
    # Impact scores per metric
    impacts: Dict[str, float] = field(default_factory=dict)
    
    # Overall score
    total_impact_score: float = 0.0
    
    # Time series projections
    projections: Dict[str, List[float]] = field(default_factory=dict)
    
    # XR heatmap data
    heatmap_data: Dict[str, Any] = field(default_factory=dict)
    
    # Confidence
    confidence_score: float = 0.0
    uncertainty_range: Tuple[float, float] = (0.0, 0.0)


# ============================================================================
# CONTRIBUTION TRACKING MODELS
# ============================================================================

class ContributionType(str, Enum):
    """Types of contributions"""
    IDEA = "idea"
    DATA = "data"
    CODE = "code"
    REVIEW = "review"
    REPLICATION = "replication"
    CRITIQUE = "critique"
    CLEANING = "cleaning"
    ANNOTATION = "annotation"
    FUNDING = "funding"
    MENTORSHIP = "mentorship"


@dataclass
class MicroContribution:
    """
    A micro-contribution to scientific work.
    
    Per spec: Récompenser toutes les contributions mesurables
    """
    contribution_id: str
    artifact_id: str
    contributor_id: str
    
    # Contribution details
    contribution_type: ContributionType
    description: str
    
    # Equity share
    equity_share: float = 0.0  # Percentage of artifact
    
    # Verification
    verified: bool = False
    verified_by: Optional[str] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # Blockchain reference (per spec: ledger blockchain)
    ledger_hash: Optional[str] = None
    block_number: Optional[int] = None


@dataclass
class ScholarEquity:
    """
    Equity distribution for an artifact.
    
    Per spec: Attribution de parts (Scholar Equity)
    """
    artifact_id: str
    total_contributions: int = 0
    
    # Equity by contributor
    equity_distribution: Dict[str, float] = field(default_factory=dict)
    
    # By type
    equity_by_type: Dict[str, float] = field(default_factory=dict)
    
    # Immutable record
    ledger_root_hash: Optional[str] = None


# ============================================================================
# REPRODUCIBILITY PROTOCOL MODELS
# ============================================================================

class ReproducibilityStatus(str, Enum):
    """Status of reproducibility check"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class ReproducibilityJob:
    """
    A reproducibility verification job.
    
    Per spec pipeline:
    1. Ingestion (code + données synthétiques)
    2. Re-run autonome (WorldEngine)
    3. Comparaison des sorties
    4. Score de reproductibilité
    """
    job_id: str
    artifact_id: str
    
    # Input
    code_ref: str  # Reference to code
    data_ref: str  # Reference to synthetic data
    
    # Status
    status: ReproducibilityStatus = ReproducibilityStatus.PENDING
    
    # Results
    reproducibility_score: float = 0.0  # 0-1
    output_match_percentage: float = 0.0
    
    # Discrepancies
    discrepancies: List[Dict[str, Any]] = field(default_factory=list)
    
    # Timestamps
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class VerifiedBadge:
    """
    CHE·NU Verified badge.
    
    Per spec outputs: Badge Verified, Rapport d'écart, Artifact signé
    """
    badge_id: str
    artifact_id: str
    
    # Score
    reproducibility_score: float
    
    # Level
    badge_level: str = "bronze"  # bronze, silver, gold, platinum
    
    # Report
    report_ref: str = ""
    
    # Signature
    signature: str = ""
    signed_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# BIO-DIGITAL STORAGE MODELS
# ============================================================================

class BioStorageStatus(str, Enum):
    """Status of bio-digital storage"""
    PENDING = "pending"
    ENCODING = "encoding"
    STORED = "stored"
    RETRIEVING = "retrieving"
    RETRIEVED = "retrieved"
    ERROR = "error"


@dataclass
class BioCapsule:
    """
    A bio-digital storage capsule.
    
    Per spec: encoder en séquence ADN (A/T/C/G) + redondance + index
    """
    capsule_id: str
    artifact_id: str
    
    # Storage info
    status: BioStorageStatus = BioStorageStatus.PENDING
    
    # DNA encoding
    dna_sequence_hash: Optional[str] = None
    shard_count: int = 0
    redundancy_level: int = 3  # Number of copies
    
    # ECC info
    ecc_type: str = "reed_solomon"
    ecc_strength: int = 32  # Symbols
    
    # Signatures (per spec: ED25519 and/or PQC)
    payload_hash: str = ""
    signature_ed25519: Optional[str] = None
    signature_pqc: Optional[str] = None
    opa_bundle_hash: Optional[str] = None
    
    # Physical locations
    storage_locations: List[str] = field(default_factory=list)
    
    # Timestamps
    encoded_at: Optional[datetime] = None
    stored_at: Optional[datetime] = None


@dataclass
class DNAShard:
    """
    A shard of DNA-encoded data.
    
    Per spec: shards (ex: 256-1024 bp per fragment)
    """
    shard_id: str
    capsule_id: str
    shard_index: int
    
    # DNA data
    base_pairs: int = 0
    gc_content: float = 0.0  # 0-1, target ~50%
    homopolymer_max: int = 0  # Max consecutive identical bases
    
    # ECC
    ecc_data: bytes = b""
    
    # Hash
    shard_hash: str = ""


@dataclass
class DecodeRequest:
    """
    Request to decode/rehydrate an artifact.
    
    Per spec: "Rehydrate" déclenche decode pipeline — HITL obligatoire
    """
    request_id: str
    capsule_id: str
    
    # HITL requirement
    requires_hitl: bool = True
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    
    # Status
    status: str = "pending_approval"
    
    # Result
    decoded_artifact_ref: Optional[str] = None


# ============================================================================
# CROSS-POLLINATOR MODELS
# ============================================================================

@dataclass
class CrossPollinationMatch:
    """
    A cross-pollination match between artifacts.
    
    Per spec: Scanner les Artifacts et notifier des correspondances utiles
    """
    match_id: str
    
    # Matched artifacts
    artifact_a: str
    artifact_b: str
    domain_a: str
    domain_b: str
    
    # Match details
    similarity_type: str  # causal, structural, methodological
    similarity_score: float  # 0-1
    
    # Notification
    notification_sent: bool = False
    task_force_created: bool = False


@dataclass
class TaskForce:
    """
    A spontaneous task force from cross-pollination.
    
    Per spec: Création de task-forces spontanées
    """
    task_force_id: str
    name: str
    
    # Origin
    match_id: str
    
    # Members (from different domains)
    members: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    
    # Status
    status: str = "proposed"  # proposed, active, completed, disbanded
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())


def compute_hash(data: Any) -> str:
    """Compute SHA-256 hash of data"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(data).hexdigest()
