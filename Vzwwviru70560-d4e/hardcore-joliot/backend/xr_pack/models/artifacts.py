"""
============================================================================
CHE·NU™ V69 — XR PACK MODELS
============================================================================
Version: 1.6.0
Purpose: Models for XR Pack visualization layer
Principle: XR = READ ONLY. All computation done offline.
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, computed_field
import uuid
import hashlib
import json


# ============================================================================
# ENUMS
# ============================================================================

class ReplayMode(str, Enum):
    """Replay mode"""
    CHUNKED = "chunked"
    FULL = "full"


class PackStatus(str, Enum):
    """XR Pack build status"""
    BUILDING = "building"
    READY = "ready"
    SIGNED = "signed"
    PUBLISHED = "published"
    ERROR = "error"


# ============================================================================
# MANIFEST
# ============================================================================

class CacheHints(BaseModel):
    """CDN cache hints"""
    immutable: bool = Field(default=True)
    max_age_seconds: int = Field(default=31536000)  # 1 year
    etag: Optional[str] = Field(default=None)


class ManifestV1(BaseModel):
    """
    XR Pack manifest (manifest.v1.json)
    
    Central index for the XR pack.
    """
    
    schema_version: str = Field(default="v1")
    pack_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Simulation reference
    simulation_id: str = Field(...)
    tenant_id: Optional[str] = Field(default=None)
    
    # Temporal
    created_at: datetime = Field(default_factory=datetime.utcnow)
    t_start: int = Field(default=0)
    t_end: int = Field(default=0)
    total_steps: int = Field(default=0)
    
    # Replay config
    replay_mode: ReplayMode = Field(default=ReplayMode.CHUNKED)
    chunk_size: int = Field(default=250)
    
    # Files
    files: Dict[str, str] = Field(default_factory=lambda: {
        "manifest": "manifest.v1.json",
        "explain": "explain.v1.json",
        "heatmap": "heatmap.v1.json",
        "diff": "diff.v1.json",
        "checksums": "checksums.v1.json",
        "replay_index": "replay/index.v1.json",
    })
    
    # Security
    public_key_b64: Optional[str] = Field(default=None)
    key_id: Optional[str] = Field(default=None)
    signature_file: Optional[str] = Field(default=None)
    
    # Cache
    cache_hints: CacheHints = Field(default_factory=CacheHints)
    
    # Status
    status: PackStatus = Field(default=PackStatus.BUILDING)
    synthetic: bool = Field(default=True)


# ============================================================================
# EXPLAIN (Explainability layer)
# ============================================================================

class ExplainEntry(BaseModel):
    """Single explanation entry"""
    step: int = Field(...)
    slot: str = Field(...)
    rule_id: str = Field(...)
    explanation: str = Field(...)
    confidence: float = Field(default=1.0, ge=0, le=1)
    impact: float = Field(default=0.0)
    sources: List[str] = Field(default_factory=list)


class ExplainV1(BaseModel):
    """
    Explainability layer (explain.v1.json)
    
    Provides human-readable explanations for simulation outcomes.
    """
    
    schema_version: str = Field(default="v1")
    simulation_id: str = Field(...)
    
    # Entries by step
    entries: List[ExplainEntry] = Field(default_factory=list)
    
    # Summary
    key_insights: List[str] = Field(default_factory=list)
    causal_chain_summary: Optional[str] = Field(default=None)
    
    # XR hooks
    highlight_steps: List[int] = Field(default_factory=list)
    
    def add_entry(self, entry: ExplainEntry) -> None:
        self.entries.append(entry)
        if entry.step not in self.highlight_steps and abs(entry.impact) > 0.1:
            self.highlight_steps.append(entry.step)


# ============================================================================
# HEATMAP
# ============================================================================

class SparklineData(BaseModel):
    """Mini time series for a metric"""
    metric: str = Field(...)
    values: List[float] = Field(default_factory=list)
    min_value: float = Field(default=0)
    max_value: float = Field(default=1)
    unit: str = Field(default="")


class SphereHeatmap(BaseModel):
    """Heatmap data for a single sphere"""
    sphere: str = Field(...)
    slots: Dict[str, List[float]] = Field(default_factory=dict)
    sparklines: List[SparklineData] = Field(default_factory=list)
    risk_score: float = Field(default=0.0, ge=0, le=1)
    alert_level: str = Field(default="normal")  # normal, warning, critical


class HeatmapV1(BaseModel):
    """
    Heatmap visualization (heatmap.v1.json)
    
    Provides color-coded intensity map for XR visualization.
    """
    
    schema_version: str = Field(default="v1")
    simulation_id: str = Field(...)
    
    # Global heatmap (step -> intensity)
    global_intensity: List[float] = Field(default_factory=list)
    
    # Per-sphere heatmaps
    spheres: Dict[str, SphereHeatmap] = Field(default_factory=dict)
    
    # Legend
    color_scale: Dict[str, str] = Field(default_factory=lambda: {
        "low": "#00FF00",      # Green
        "medium": "#FFFF00",   # Yellow
        "high": "#FF0000",     # Red
    })
    
    # Thresholds
    thresholds: Dict[str, float] = Field(default_factory=lambda: {
        "low": 0.3,
        "medium": 0.6,
        "high": 0.9,
    })


# ============================================================================
# DIFF & DIVERGENCE
# ============================================================================

class DivergencePoint(BaseModel):
    """A point where scenarios diverge significantly"""
    step: int = Field(...)
    signals: Dict[str, float] = Field(default_factory=dict)
    top_reasons: List[str] = Field(default_factory=list)
    summary: str = Field(default="")
    severity: str = Field(default="medium")  # low, medium, high, critical


class DivergenceConfig(BaseModel):
    """Thresholds for divergence detection"""
    budget_threshold: float = Field(default=10000)
    risk_threshold: float = Field(default=0.05)
    velocity_threshold: float = Field(default=0.1)
    max_points: int = Field(default=50)


class ScenarioDiff(BaseModel):
    """Diff between two scenarios"""
    baseline_id: str = Field(...)
    scenario_id: str = Field(...)
    scenario_name: str = Field(default="")
    
    # Deltas per step
    deltas: Dict[str, List[float]] = Field(default_factory=dict)
    
    # Summary stats
    max_delta: float = Field(default=0)
    total_divergence: float = Field(default=0)


class DiffV1(BaseModel):
    """
    Diff and divergence analysis (diff.v1.json)
    
    Compares scenarios and identifies key divergence points.
    """
    
    schema_version: str = Field(default="v1")
    simulation_id: str = Field(...)
    
    # Baseline
    baseline_scenario: str = Field(...)
    
    # Scenarios compared
    scenarios: List[ScenarioDiff] = Field(default_factory=list)
    
    # Divergence analysis
    divergence: Dict[str, Any] = Field(default_factory=lambda: {
        "thresholds": {},
        "points": [],
    })
    
    # Summary
    summary: str = Field(default="")
    
    def add_divergence_point(self, point: DivergencePoint) -> None:
        if "points" not in self.divergence:
            self.divergence["points"] = []
        self.divergence["points"].append(point.model_dump())


# ============================================================================
# CHECKSUMS
# ============================================================================

class FileChecksum(BaseModel):
    """Checksum for a single file"""
    file: str = Field(...)
    sha256: str = Field(...)
    size_bytes: int = Field(default=0)


class ChecksumsV1(BaseModel):
    """
    Checksums for pack integrity (checksums.v1.json)
    """
    
    schema_version: str = Field(default="v1")
    pack_id: str = Field(...)
    
    # File checksums
    files: List[FileChecksum] = Field(default_factory=list)
    
    # Pack checksum (all files combined)
    pack_sha256: Optional[str] = Field(default=None)
    
    # Timestamp
    computed_at: datetime = Field(default_factory=datetime.utcnow)
    
    def add_file(self, filename: str, content: bytes) -> None:
        checksum = hashlib.sha256(content).hexdigest()
        self.files.append(FileChecksum(
            file=filename,
            sha256=checksum,
            size_bytes=len(content),
        ))
    
    def compute_pack_hash(self) -> str:
        """Compute combined hash of all files"""
        combined = "".join(sorted(f.sha256 for f in self.files))
        self.pack_sha256 = hashlib.sha256(combined.encode()).hexdigest()
        return self.pack_sha256


# ============================================================================
# REPLAY (Chunked)
# ============================================================================

class ReplayFrame(BaseModel):
    """Single frame in replay"""
    step: int = Field(...)
    timestamp_sim: float = Field(default=0)
    
    # State snapshot
    slots: Dict[str, float] = Field(default_factory=dict)
    
    # Events at this step
    events: List[str] = Field(default_factory=list)
    
    # XR hints
    camera_focus: Optional[str] = Field(default=None)
    highlights: List[str] = Field(default_factory=list)


class ReplayChunk(BaseModel):
    """
    Single replay chunk (replay/chunk_XXXX.v1.json)
    """
    
    schema_version: str = Field(default="v1")
    chunk_id: int = Field(...)
    from_step: int = Field(...)
    to_step: int = Field(...)
    
    # Frames
    frames: List[ReplayFrame] = Field(default_factory=list)
    
    @computed_field
    @property
    def sha256(self) -> str:
        """Compute chunk hash"""
        content = json.dumps([f.model_dump() for f in self.frames], sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()


class ChunkReference(BaseModel):
    """Reference to a chunk in the index"""
    id: int = Field(...)
    file: str = Field(...)
    from_step: int = Field(...)
    to_step: int = Field(...)
    sha256: str = Field(...)


class ReplayIndexV1(BaseModel):
    """
    Replay index (replay/index.v1.json)
    
    Index of all replay chunks for progressive loading.
    """
    
    schema_version: str = Field(default="v1")
    mode: ReplayMode = Field(default=ReplayMode.CHUNKED)
    chunk_size: int = Field(default=250)
    total_steps: int = Field(default=0)
    total_chunks: int = Field(default=0)
    
    # Chunk references
    chunks: List[ChunkReference] = Field(default_factory=list)
    
    def add_chunk(self, chunk: ReplayChunk) -> None:
        """Add chunk reference"""
        ref = ChunkReference(
            id=chunk.chunk_id,
            file=f"chunk_{chunk.chunk_id:04d}.v1.json",
            from_step=chunk.from_step,
            to_step=chunk.to_step,
            sha256=chunk.sha256,
        )
        self.chunks.append(ref)
        self.total_chunks = len(self.chunks)


# ============================================================================
# SIGNATURE ARTIFACTS
# ============================================================================

class XRPackSignatureV1(BaseModel):
    """
    Signature artifact (xr_pack.v1.sig.json)
    """
    
    schema_version: str = Field(default="v1")
    algo: str = Field(default="Ed25519")
    zip_sha256: str = Field(...)
    signature_b64: str = Field(...)
    signed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    key_id: str = Field(...)
    
    # For hybrid signatures
    hybrid_signatures: Optional[Dict[str, str]] = Field(default=None)


class XRPackPublicKeyV1(BaseModel):
    """
    Public key artifact (xr_pack.v1.pubkey.json)
    """
    
    schema_version: str = Field(default="v1")
    algo: str = Field(default="Ed25519")
    key_id: str = Field(...)
    public_key_b64: str = Field(...)
    
    # For hybrid keys
    hybrid_keys: Optional[Dict[str, str]] = Field(default=None)


# ============================================================================
# XR PACK (Complete)
# ============================================================================

class XRPackV1(BaseModel):
    """
    Complete XR Pack structure.
    
    Contains all artifacts for XR visualization.
    """
    
    pack_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Core artifacts
    manifest: ManifestV1 = Field(...)
    explain: ExplainV1 = Field(...)
    heatmap: HeatmapV1 = Field(...)
    diff: DiffV1 = Field(...)
    checksums: ChecksumsV1 = Field(...)
    replay_index: ReplayIndexV1 = Field(...)
    
    # Chunks (generated separately)
    chunks: List[ReplayChunk] = Field(default_factory=list)
    
    # Signature (optional, added after signing)
    signature: Optional[XRPackSignatureV1] = Field(default=None)
    public_key: Optional[XRPackPublicKeyV1] = Field(default=None)
    
    @computed_field
    @property
    def is_signed(self) -> bool:
        return self.signature is not None
