"""
============================================================================
CHE·NU™ V69 — XR PACK BUILDER
============================================================================
Version: 1.6.0
Purpose: Build complete XR visualization packs
Principle: XR = READ ONLY. All computation done offline worker.
============================================================================
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import hashlib
import json
import logging
import os
import zipfile
import io

from ..models.artifacts import (
    ManifestV1,
    ExplainV1,
    ExplainEntry,
    HeatmapV1,
    SphereHeatmap,
    SparklineData,
    DiffV1,
    ChecksumsV1,
    ReplayIndexV1,
    ReplayChunk,
    ReplayFrame,
    XRPackV1,
    XRPackSignatureV1,
    XRPackPublicKeyV1,
    PackStatus,
    ReplayMode,
    CacheHints,
)
from ..divergence.calculator import (
    DivergenceCalculator,
    Timeline,
    TimelineSnapshot,
    DivergenceConfig,
)
from ..replay.chunker import ReplayChunker, ChunkFileGenerator

# Import security module for signing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from security import (
    get_key_manager,
    get_unified_signer,
    SignatureAlgorithm,
    KeyPurpose,
)

logger = logging.getLogger(__name__)


# ============================================================================
# XR PACK BUILDER
# ============================================================================

class XRPackBuilder:
    """
    Builds complete XR visualization packs from simulation data.
    
    The XR Pack is a self-contained, signed artifact that can be:
    - Served from CDN (immutable, cacheable)
    - Loaded progressively in WebXR
    - Verified cryptographically (Ed25519/Hybrid)
    
    Build process:
    1. Create manifest
    2. Generate explain layer
    3. Generate heatmap
    4. Calculate divergence diff
    5. Chunk replay frames
    6. Compute checksums
    7. Create ZIP
    8. Sign with Ed25519/Hybrid
    
    Usage:
        builder = XRPackBuilder(
            simulation_id="sim-001",
            tenant_id="enterprise",
        )
        
        # Add simulation data
        builder.add_simulation_states(states)
        builder.add_scenarios(baseline, scenarios)
        builder.add_explanations(explanations)
        
        # Build pack
        pack = builder.build()
        
        # Sign pack
        signed_pack = builder.sign(key_id)
        
        # Export
        builder.export("/path/to/output")
    """
    
    def __init__(
        self,
        simulation_id: str,
        tenant_id: Optional[str] = None,
        chunk_size: int = 250,
    ):
        self.simulation_id = simulation_id
        self.tenant_id = tenant_id
        self.chunk_size = chunk_size
        
        # Data storage
        self._states: List[Dict[str, Any]] = []
        self._baseline_timeline: Optional[Timeline] = None
        self._scenario_timelines: List[Timeline] = []
        self._explanations: List[ExplainEntry] = []
        self._sphere_data: Dict[str, Dict[str, List[float]]] = {}
        
        # Built artifacts
        self._pack: Optional[XRPackV1] = None
        self._zip_bytes: Optional[bytes] = None
    
    def add_simulation_states(
        self,
        states: List[Dict[str, Any]],
    ) -> "XRPackBuilder":
        """
        Add simulation states for replay.
        
        Args:
            states: List of {"step": int, "slots": {name: value}, "events": [...]}
        """
        self._states.extend(states)
        return self
    
    def set_baseline(
        self,
        states: List[Dict[str, Any]],
        scenario_id: str = "baseline",
        scenario_name: str = "Baseline",
    ) -> "XRPackBuilder":
        """Set baseline scenario for divergence analysis"""
        self._baseline_timeline = Timeline(scenario_id, scenario_name)
        
        for state in states:
            snapshot = TimelineSnapshot(
                step=state.get("step", 0),
                slots=state.get("slots", {}),
                events=state.get("events", []),
            )
            self._baseline_timeline.add_snapshot(snapshot)
        
        return self
    
    def add_scenario(
        self,
        states: List[Dict[str, Any]],
        scenario_id: str,
        scenario_name: str = "",
    ) -> "XRPackBuilder":
        """Add alternative scenario for divergence analysis"""
        timeline = Timeline(scenario_id, scenario_name or scenario_id)
        
        for state in states:
            snapshot = TimelineSnapshot(
                step=state.get("step", 0),
                slots=state.get("slots", {}),
                events=state.get("events", []),
            )
            timeline.add_snapshot(snapshot)
        
        self._scenario_timelines.append(timeline)
        return self
    
    def add_explanation(
        self,
        step: int,
        slot: str,
        rule_id: str,
        explanation: str,
        impact: float = 0.0,
    ) -> "XRPackBuilder":
        """Add explanation entry"""
        self._explanations.append(ExplainEntry(
            step=step,
            slot=slot,
            rule_id=rule_id,
            explanation=explanation,
            impact=impact,
        ))
        return self
    
    def add_sphere_data(
        self,
        sphere: str,
        slot: str,
        values: List[float],
    ) -> "XRPackBuilder":
        """Add sphere-specific data for heatmap"""
        if sphere not in self._sphere_data:
            self._sphere_data[sphere] = {}
        self._sphere_data[sphere][slot] = values
        return self
    
    def build(self) -> XRPackV1:
        """
        Build the complete XR Pack.
        
        Returns:
            XRPackV1 with all artifacts
        """
        logger.info(f"Building XR Pack for simulation {self.simulation_id}")
        
        # 1. Create manifest
        manifest = self._build_manifest()
        
        # 2. Build explain layer
        explain = self._build_explain()
        
        # 3. Build heatmap
        heatmap = self._build_heatmap()
        
        # 4. Build diff with divergence
        diff = self._build_diff()
        
        # 5. Build replay chunks
        replay_index, chunks = self._build_replay()
        
        # Update manifest with totals
        manifest.total_steps = replay_index.total_steps
        manifest.t_end = replay_index.total_steps - 1 if replay_index.total_steps > 0 else 0
        
        # 6. Build checksums (after all artifacts created)
        checksums = self._build_checksums(
            manifest, explain, heatmap, diff, replay_index, chunks
        )
        
        # Update manifest status
        manifest.status = PackStatus.READY
        
        # 7. Assemble pack
        self._pack = XRPackV1(
            manifest=manifest,
            explain=explain,
            heatmap=heatmap,
            diff=diff,
            checksums=checksums,
            replay_index=replay_index,
            chunks=chunks,
        )
        
        logger.info(
            f"Built XR Pack: {len(chunks)} chunks, "
            f"{replay_index.total_steps} steps, "
            f"{len(diff.divergence.get('points', []))} divergence points"
        )
        
        return self._pack
    
    def _build_manifest(self) -> ManifestV1:
        """Build manifest"""
        return ManifestV1(
            simulation_id=self.simulation_id,
            tenant_id=self.tenant_id,
            t_start=0,
            replay_mode=ReplayMode.CHUNKED,
            chunk_size=self.chunk_size,
            status=PackStatus.BUILDING,
        )
    
    def _build_explain(self) -> ExplainV1:
        """Build explain layer"""
        explain = ExplainV1(simulation_id=self.simulation_id)
        
        for entry in self._explanations:
            explain.add_entry(entry)
        
        # Generate key insights from high-impact explanations
        high_impact = sorted(
            self._explanations,
            key=lambda e: abs(e.impact),
            reverse=True,
        )[:5]
        
        explain.key_insights = [
            f"Step {e.step}: {e.explanation}" for e in high_impact
        ]
        
        return explain
    
    def _build_heatmap(self) -> HeatmapV1:
        """Build heatmap"""
        heatmap = HeatmapV1(simulation_id=self.simulation_id)
        
        # Build global intensity from states
        if self._states:
            heatmap.global_intensity = self._calculate_global_intensity()
        
        # Build sphere heatmaps
        for sphere, slots in self._sphere_data.items():
            sphere_heatmap = SphereHeatmap(sphere=sphere, slots=slots)
            
            # Calculate sparklines
            for slot, values in slots.items():
                if values:
                    sparkline = SparklineData(
                        metric=slot,
                        values=values,
                        min_value=min(values),
                        max_value=max(values),
                    )
                    sphere_heatmap.sparklines.append(sparkline)
            
            # Calculate risk score (average of normalized values)
            if slots:
                all_values = []
                for v in slots.values():
                    all_values.extend(v)
                if all_values:
                    sphere_heatmap.risk_score = sum(all_values) / len(all_values)
            
            heatmap.spheres[sphere] = sphere_heatmap
        
        return heatmap
    
    def _calculate_global_intensity(self) -> List[float]:
        """Calculate global intensity per step"""
        intensities = []
        
        for state in sorted(self._states, key=lambda s: s.get("step", 0)):
            slots = state.get("slots", {})
            if slots:
                # Normalize and average slot values
                values = list(slots.values())
                avg = sum(abs(v) for v in values) / len(values)
                # Normalize to 0-1 (arbitrary scale)
                intensity = min(1.0, avg / 1000000) if avg > 0 else 0
                intensities.append(intensity)
            else:
                intensities.append(0)
        
        return intensities
    
    def _build_diff(self) -> DiffV1:
        """Build diff with divergence analysis"""
        if self._baseline_timeline is None:
            # No divergence analysis without baseline
            return DiffV1(
                simulation_id=self.simulation_id,
                baseline_scenario="none",
            )
        
        calculator = DivergenceCalculator(DivergenceConfig())
        calculator.set_baseline(self._baseline_timeline)
        
        for scenario in self._scenario_timelines:
            calculator.add_scenario(scenario)
        
        return calculator.calculate(self.simulation_id)
    
    def _build_replay(self) -> tuple[ReplayIndexV1, List[ReplayChunk]]:
        """Build chunked replay"""
        chunker = ReplayChunker(self.chunk_size)
        
        for state in sorted(self._states, key=lambda s: s.get("step", 0)):
            frame = ReplayFrame(
                step=state.get("step", 0),
                timestamp_sim=state.get("timestamp", 0),
                slots=state.get("slots", {}),
                events=state.get("events", []),
            )
            chunker.add_frame(frame)
        
        return chunker.build()
    
    def _build_checksums(
        self,
        manifest: ManifestV1,
        explain: ExplainV1,
        heatmap: HeatmapV1,
        diff: DiffV1,
        replay_index: ReplayIndexV1,
        chunks: List[ReplayChunk],
    ) -> ChecksumsV1:
        """Build checksums for all files"""
        checksums = ChecksumsV1(pack_id=manifest.pack_id)
        
        # Add main files
        checksums.add_file("manifest.v1.json", manifest.model_dump_json().encode())
        checksums.add_file("explain.v1.json", explain.model_dump_json().encode())
        checksums.add_file("heatmap.v1.json", heatmap.model_dump_json().encode())
        checksums.add_file("diff.v1.json", diff.model_dump_json().encode())
        checksums.add_file("replay/index.v1.json", replay_index.model_dump_json().encode())
        
        # Add chunk files
        for chunk in chunks:
            filename = f"replay/chunk_{chunk.chunk_id:04d}.v1.json"
            checksums.add_file(filename, chunk.model_dump_json().encode())
        
        checksums.compute_pack_hash()
        
        return checksums
    
    def create_zip(self) -> bytes:
        """
        Create ZIP archive of the pack.
        
        Returns:
            ZIP file bytes
        """
        if self._pack is None:
            raise ValueError("Pack not built yet. Call build() first.")
        
        # Create in-memory ZIP
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Write main files
            zf.writestr("manifest.v1.json", self._pack.manifest.model_dump_json(indent=2))
            zf.writestr("explain.v1.json", self._pack.explain.model_dump_json(indent=2))
            zf.writestr("heatmap.v1.json", self._pack.heatmap.model_dump_json(indent=2))
            zf.writestr("diff.v1.json", self._pack.diff.model_dump_json(indent=2))
            zf.writestr("checksums.v1.json", self._pack.checksums.model_dump_json(indent=2))
            
            # Write replay files
            zf.writestr("replay/index.v1.json", self._pack.replay_index.model_dump_json(indent=2))
            
            for chunk in self._pack.chunks:
                filename = f"replay/chunk_{chunk.chunk_id:04d}.v1.json"
                zf.writestr(filename, chunk.model_dump_json(indent=2))
        
        self._zip_bytes = zip_buffer.getvalue()
        
        logger.info(f"Created ZIP: {len(self._zip_bytes)} bytes")
        
        return self._zip_bytes
    
    def sign(
        self,
        key_id: Optional[str] = None,
        algorithm: SignatureAlgorithm = SignatureAlgorithm.HYBRID_ED25519_DILITHIUM2,
    ) -> XRPackV1:
        """
        Sign the XR Pack with Ed25519 or Hybrid signature.
        
        Args:
            key_id: Key ID from KeyManager (generates new if None)
            algorithm: Signature algorithm to use
        """
        if self._pack is None:
            raise ValueError("Pack not built yet. Call build() first.")
        
        if self._zip_bytes is None:
            self.create_zip()
        
        # Get or generate key
        key_manager = get_key_manager()
        
        if key_id is None:
            key_id = key_manager.generate_key(
                algorithm=algorithm,
                purpose=KeyPurpose.XR_PACK_SIGNING,
                tenant_id=self.tenant_id,
            )
        
        key_pair = key_manager.get_key(key_id)
        if key_pair is None:
            raise ValueError(f"Key not found: {key_id}")
        
        # Compute ZIP hash
        zip_hash = hashlib.sha256(self._zip_bytes).hexdigest()
        
        # Sign
        signer = get_unified_signer()
        signature = signer.sign(self._zip_bytes, key_pair, "xr_pack")
        
        # Create signature artifact
        self._pack.signature = XRPackSignatureV1(
            algo=key_pair.algorithm.value,
            zip_sha256=zip_hash,
            signature_b64=signature.signature_b64,
            key_id=key_pair.key_id,
        )
        
        if signature.is_hybrid:
            self._pack.signature.hybrid_signatures = {
                "classical_b64": signature.classical_signature_b64,
                "pq_b64": signature.pq_signature_b64,
            }
        
        # Create public key artifact
        public_key = key_manager.get_public_key(key_id)
        self._pack.public_key = XRPackPublicKeyV1(
            algo=public_key.algorithm.value,
            key_id=public_key.key_id,
            public_key_b64=public_key.public_key_b64,
        )
        
        if public_key.is_hybrid:
            self._pack.public_key.hybrid_keys = {
                "classical_b64": public_key.classical_public_key_b64,
                "pq_b64": public_key.pq_public_key_b64,
            }
        
        # Update manifest
        self._pack.manifest.public_key_b64 = public_key.public_key_b64
        self._pack.manifest.key_id = public_key.key_id
        self._pack.manifest.signature_file = "xr_pack.v1.sig.json"
        self._pack.manifest.cache_hints.etag = f"sha256:{zip_hash}"
        self._pack.manifest.status = PackStatus.SIGNED
        
        logger.info(f"Signed XR Pack with {key_pair.algorithm.value}")
        
        return self._pack
    
    def export(self, output_dir: str) -> Dict[str, str]:
        """
        Export pack to directory.
        
        Args:
            output_dir: Output directory path
            
        Returns:
            Dict of {filename: path}
        """
        if self._pack is None:
            raise ValueError("Pack not built yet. Call build() first.")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create pack directory
        pack_dir = output_path / "xr_pack.v1"
        pack_dir.mkdir(exist_ok=True)
        (pack_dir / "replay").mkdir(exist_ok=True)
        (pack_dir / "assets").mkdir(exist_ok=True)
        
        exported_files = {}
        
        # Write main files
        files = {
            "manifest.v1.json": self._pack.manifest.model_dump_json(indent=2),
            "explain.v1.json": self._pack.explain.model_dump_json(indent=2),
            "heatmap.v1.json": self._pack.heatmap.model_dump_json(indent=2),
            "diff.v1.json": self._pack.diff.model_dump_json(indent=2),
            "checksums.v1.json": self._pack.checksums.model_dump_json(indent=2),
            "replay/index.v1.json": self._pack.replay_index.model_dump_json(indent=2),
        }
        
        for filename, content in files.items():
            file_path = pack_dir / filename
            file_path.parent.mkdir(exist_ok=True)
            file_path.write_text(content)
            exported_files[filename] = str(file_path)
        
        # Write chunks
        for chunk in self._pack.chunks:
            filename = f"replay/chunk_{chunk.chunk_id:04d}.v1.json"
            file_path = pack_dir / filename
            file_path.write_text(chunk.model_dump_json(indent=2))
            exported_files[filename] = str(file_path)
        
        # Write ZIP
        if self._zip_bytes:
            zip_path = output_path / "xr_pack.v1.zip"
            zip_path.write_bytes(self._zip_bytes)
            exported_files["xr_pack.v1.zip"] = str(zip_path)
        
        # Write signature artifacts
        if self._pack.signature:
            sig_path = output_path / "xr_pack.v1.sig.json"
            sig_path.write_text(self._pack.signature.model_dump_json(indent=2))
            exported_files["xr_pack.v1.sig.json"] = str(sig_path)
        
        if self._pack.public_key:
            key_path = output_path / "xr_pack.v1.pubkey.json"
            key_path.write_text(self._pack.public_key.model_dump_json(indent=2))
            exported_files["xr_pack.v1.pubkey.json"] = str(key_path)
        
        logger.info(f"Exported {len(exported_files)} files to {output_dir}")
        
        return exported_files
    
    @property
    def pack(self) -> Optional[XRPackV1]:
        """Get built pack"""
        return self._pack
    
    @property
    def zip_bytes(self) -> Optional[bytes]:
        """Get ZIP bytes"""
        return self._zip_bytes
