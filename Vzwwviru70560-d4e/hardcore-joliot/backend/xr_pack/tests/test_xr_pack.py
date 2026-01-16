"""
============================================================================
CHE·NU™ V69 — XR PACK TESTS
============================================================================
Version: 1.0.0
Purpose: Test XR Pack building, chunking, and verification
============================================================================
"""

import pytest
import tempfile
from pathlib import Path

from ..models import (
    ReplayMode,
    PackStatus,
    ManifestV1,
    ExplainV1,
    ExplainEntry,
    HeatmapV1,
    DiffV1,
    DivergencePoint,
    DivergenceConfig,
    ChecksumsV1,
    ReplayFrame,
    ReplayChunk,
    ReplayIndexV1,
    XRPackV1,
)
from ..divergence import (
    Timeline,
    TimelineSnapshot,
    DivergenceCalculator,
    calculate_divergence,
)
from ..replay import ReplayChunker, ChunkLoader
from ..builder import XRPackBuilder
from ..verify import XRPackVerifier


# ============================================================================
# MODEL TESTS
# ============================================================================

class TestModels:
    """Test XR Pack models"""
    
    def test_manifest_creation(self):
        manifest = ManifestV1(
            simulation_id="sim-001",
            tenant_id="enterprise",
        )
        assert manifest.simulation_id == "sim-001"
        assert manifest.replay_mode == ReplayMode.CHUNKED
        assert manifest.status == PackStatus.BUILDING
    
    def test_replay_frame(self):
        frame = ReplayFrame(
            step=42,
            slots={"Budget": 1000000, "Risk": 0.15},
            events=["budget_adjustment"],
        )
        assert frame.step == 42
        assert frame.slots["Budget"] == 1000000
    
    def test_replay_chunk(self):
        frames = [
            ReplayFrame(step=i, slots={"value": i * 100})
            for i in range(10)
        ]
        
        chunk = ReplayChunk(
            chunk_id=0,
            from_step=0,
            to_step=9,
            frames=frames,
        )
        
        assert chunk.chunk_id == 0
        assert len(chunk.frames) == 10
        assert len(chunk.sha256) == 64  # SHA256 hex
    
    def test_divergence_point(self):
        point = DivergencePoint(
            step=42,
            signals={"budget_delta": -50000, "risk_delta": 0.1},
            top_reasons=["aggressive_spending", "market_shift"],
            summary="Significant divergence at step 42",
            severity="high",
        )
        assert point.step == 42
        assert point.severity == "high"


# ============================================================================
# REPLAY CHUNKER TESTS
# ============================================================================

class TestReplayChunker:
    """Test replay chunking"""
    
    def test_empty_chunker(self):
        chunker = ReplayChunker(chunk_size=10)
        index, chunks = chunker.build()
        
        assert index.total_steps == 0
        assert index.total_chunks == 0
        assert len(chunks) == 0
    
    def test_single_chunk(self):
        chunker = ReplayChunker(chunk_size=100)
        
        for i in range(50):
            chunker.add_frame(ReplayFrame(step=i, slots={"v": i}))
        
        index, chunks = chunker.build()
        
        assert index.total_steps == 50
        assert index.total_chunks == 1
        assert len(chunks) == 1
        assert chunks[0].from_step == 0
        assert chunks[0].to_step == 49
    
    def test_multiple_chunks(self):
        chunker = ReplayChunker(chunk_size=25)
        
        for i in range(100):
            chunker.add_frame(ReplayFrame(step=i, slots={"v": i}))
        
        index, chunks = chunker.build()
        
        assert index.total_steps == 100
        assert index.total_chunks == 4
        assert len(chunks) == 4
        
        # Check chunk boundaries
        assert chunks[0].from_step == 0
        assert chunks[0].to_step == 24
        assert chunks[1].from_step == 25
        assert chunks[1].to_step == 49
    
    def test_chunk_loader(self):
        chunker = ReplayChunker(chunk_size=25)
        
        for i in range(100):
            chunker.add_frame(ReplayFrame(step=i, slots={"v": i}))
        
        index, chunks = chunker.build()
        loader = ChunkLoader(chunks)
        
        # Get specific frame
        frame = loader.get_frame(42, index)
        assert frame is not None
        assert frame.step == 42
        assert frame.slots["v"] == 42


# ============================================================================
# DIVERGENCE CALCULATOR TESTS
# ============================================================================

class TestDivergenceCalculator:
    """Test divergence calculation"""
    
    def test_no_divergence(self):
        """Test when scenarios are identical"""
        baseline_states = [
            {"step": i, "slots": {"Budget": 1000000}}
            for i in range(10)
        ]
        scenario_states = baseline_states.copy()
        
        diff = calculate_divergence(
            baseline_states,
            scenario_states,
            simulation_id="test",
        )
        
        assert len(diff.divergence.get("points", [])) == 0
    
    def test_with_divergence(self):
        """Test when scenarios diverge"""
        baseline_states = [
            {"step": i, "slots": {"Budget": 1000000}}
            for i in range(10)
        ]
        
        scenario_states = [
            {"step": i, "slots": {"Budget": 1000000 - (i * 20000)}}
            for i in range(10)
        ]
        
        config = DivergenceConfig(budget_threshold=10000)
        diff = calculate_divergence(
            baseline_states,
            scenario_states,
            simulation_id="test",
            config=config,
        )
        
        # Should have divergence points
        points = diff.divergence.get("points", [])
        assert len(points) > 0
    
    def test_multiple_scenarios(self):
        """Test with multiple scenarios"""
        calculator = DivergenceCalculator()
        
        # Baseline
        baseline = Timeline("baseline", "Baseline")
        for i in range(10):
            baseline.add_snapshot(TimelineSnapshot(
                step=i,
                slots={"Budget": 1000000},
            ))
        calculator.set_baseline(baseline)
        
        # Scenario 1
        scen1 = Timeline("aggressive", "Aggressive")
        for i in range(10):
            scen1.add_snapshot(TimelineSnapshot(
                step=i,
                slots={"Budget": 1000000 - (i * 50000)},
            ))
        calculator.add_scenario(scen1)
        
        # Scenario 2
        scen2 = Timeline("conservative", "Conservative")
        for i in range(10):
            scen2.add_snapshot(TimelineSnapshot(
                step=i,
                slots={"Budget": 1000000 + (i * 10000)},
            ))
        calculator.add_scenario(scen2)
        
        diff = calculator.calculate("test")
        
        assert len(diff.scenarios) == 2
        assert diff.scenarios[0].scenario_id == "aggressive"
        assert diff.scenarios[1].scenario_id == "conservative"


# ============================================================================
# XR PACK BUILDER TESTS
# ============================================================================

class TestXRPackBuilder:
    """Test XR Pack building"""
    
    @pytest.fixture
    def sample_states(self):
        return [
            {
                "step": i,
                "slots": {
                    "Budget": 1000000 - (i * 10000),
                    "Risk": 0.1 + (i * 0.02),
                },
                "events": [f"event_{i}"] if i % 3 == 0 else [],
            }
            for i in range(100)
        ]
    
    def test_build_basic_pack(self, sample_states):
        """Test basic pack building"""
        builder = XRPackBuilder(
            simulation_id="test-sim",
            tenant_id="test-tenant",
            chunk_size=25,
        )
        
        builder.add_simulation_states(sample_states)
        pack = builder.build()
        
        assert pack is not None
        assert pack.manifest.simulation_id == "test-sim"
        assert pack.manifest.status == PackStatus.READY
        assert pack.replay_index.total_steps == 100
        assert pack.replay_index.total_chunks == 4
    
    def test_build_with_divergence(self, sample_states):
        """Test pack with divergence analysis"""
        builder = XRPackBuilder(
            simulation_id="test-sim",
            chunk_size=25,
        )
        
        builder.add_simulation_states(sample_states)
        
        # Add baseline
        builder.set_baseline(sample_states, "baseline", "Baseline")
        
        # Add alternative scenario
        alt_states = [
            {
                "step": i,
                "slots": {
                    "Budget": 1000000 - (i * 30000),
                    "Risk": 0.1 + (i * 0.05),
                },
            }
            for i in range(100)
        ]
        builder.add_scenario(alt_states, "aggressive", "Aggressive")
        
        pack = builder.build()
        
        assert pack.diff.baseline_scenario == "baseline"
        assert len(pack.diff.scenarios) == 1
    
    def test_build_with_explanations(self, sample_states):
        """Test pack with explanations"""
        builder = XRPackBuilder(
            simulation_id="test-sim",
            chunk_size=25,
        )
        
        builder.add_simulation_states(sample_states)
        
        # Add explanations
        builder.add_explanation(
            step=10,
            slot="Budget",
            rule_id="rule_001",
            explanation="Budget decreased due to aggressive spending",
            impact=-0.5,
        )
        builder.add_explanation(
            step=50,
            slot="Risk",
            rule_id="rule_002",
            explanation="Risk increased due to market volatility",
            impact=0.3,
        )
        
        pack = builder.build()
        
        assert len(pack.explain.entries) == 2
        assert len(pack.explain.key_insights) > 0
    
    def test_create_zip(self, sample_states):
        """Test ZIP creation"""
        builder = XRPackBuilder(
            simulation_id="test-sim",
            chunk_size=25,
        )
        
        builder.add_simulation_states(sample_states)
        builder.build()
        
        zip_bytes = builder.create_zip()
        
        assert zip_bytes is not None
        assert len(zip_bytes) > 0
    
    def test_sign_pack(self, sample_states):
        """Test pack signing"""
        builder = XRPackBuilder(
            simulation_id="test-sim",
            chunk_size=25,
        )
        
        builder.add_simulation_states(sample_states)
        builder.build()
        
        signed_pack = builder.sign()
        
        assert signed_pack.is_signed
        assert signed_pack.signature is not None
        assert signed_pack.public_key is not None
        assert signed_pack.manifest.status == PackStatus.SIGNED
    
    def test_export_pack(self, sample_states):
        """Test pack export"""
        builder = XRPackBuilder(
            simulation_id="test-sim",
            chunk_size=25,
        )
        
        builder.add_simulation_states(sample_states)
        builder.build()
        builder.sign()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            exported = builder.export(tmpdir)
            
            # Check files exist
            assert "manifest.v1.json" in exported
            assert "replay/index.v1.json" in exported
            assert "xr_pack.v1.zip" in exported
            assert "xr_pack.v1.sig.json" in exported


# ============================================================================
# VERIFIER TESTS
# ============================================================================

class TestXRPackVerifier:
    """Test XR Pack verification"""
    
    @pytest.fixture
    def built_pack(self):
        """Create a built and signed pack"""
        states = [
            {"step": i, "slots": {"Budget": 1000000 - (i * 10000)}}
            for i in range(50)
        ]
        
        builder = XRPackBuilder(
            simulation_id="verify-test",
            chunk_size=25,
        )
        builder.add_simulation_states(states)
        builder.build()
        builder.sign()
        
        return builder
    
    def test_verify_zip(self, built_pack):
        """Test ZIP verification"""
        verifier = XRPackVerifier()
        
        result = verifier.verify_zip(
            built_pack.zip_bytes,
            built_pack.pack.signature,
            built_pack.pack.public_key,
        )
        
        assert result.valid
        assert result.signature_result.is_valid
    
    def test_verify_directory(self, built_pack):
        """Test directory verification"""
        with tempfile.TemporaryDirectory() as tmpdir:
            built_pack.export(tmpdir)
            
            verifier = XRPackVerifier()
            result = verifier.verify_directory(f"{tmpdir}/xr_pack.v1")
            
            assert result.valid
            assert "manifest_exists" in result.checks
            assert result.checks["manifest_exists"]
    
    def test_verify_corrupted_zip(self, built_pack):
        """Test verification fails on corrupted ZIP"""
        verifier = XRPackVerifier()
        
        # Corrupt the ZIP
        corrupted = built_pack.zip_bytes[:-100] + b"corrupted"
        
        result = verifier.verify_zip(
            corrupted,
            built_pack.pack.signature,
            built_pack.pack.public_key,
        )
        
        # Should fail signature check
        assert not result.signature_result.is_valid


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_workflow(self):
        """Test complete XR Pack workflow"""
        # 1. Generate simulation data
        baseline_states = [
            {
                "step": i,
                "slots": {
                    "Budget": 1000000 - (i * 5000),
                    "Risk": 0.1 + (i * 0.01),
                    "Velocity": 0.8 - (i * 0.005),
                },
                "events": [f"step_{i}_event"] if i % 5 == 0 else [],
            }
            for i in range(200)
        ]
        
        aggressive_states = [
            {
                "step": i,
                "slots": {
                    "Budget": 1000000 - (i * 15000),
                    "Risk": 0.1 + (i * 0.03),
                    "Velocity": 0.8 - (i * 0.002),
                },
            }
            for i in range(200)
        ]
        
        # 2. Build XR Pack
        builder = XRPackBuilder(
            simulation_id="enterprise-sim-001",
            tenant_id="acme-corp",
            chunk_size=50,
        )
        
        builder.add_simulation_states(baseline_states)
        builder.set_baseline(baseline_states, "baseline", "Baseline Scenario")
        builder.add_scenario(aggressive_states, "aggressive", "Aggressive Spending")
        
        builder.add_explanation(
            step=100,
            slot="Budget",
            rule_id="spend_rule",
            explanation="Aggressive scenario depletes budget faster",
            impact=-0.7,
        )
        
        pack = builder.build()
        
        # 3. Verify structure
        assert pack.manifest.simulation_id == "enterprise-sim-001"
        assert pack.replay_index.total_steps == 200
        assert pack.replay_index.total_chunks == 4  # 200 / 50
        assert len(pack.diff.scenarios) == 1
        assert len(pack.diff.divergence.get("points", [])) > 0
        
        # 4. Sign pack
        signed_pack = builder.sign()
        assert signed_pack.is_signed
        
        # 5. Create ZIP
        zip_bytes = builder.create_zip()
        assert len(zip_bytes) > 0
        
        # 6. Verify pack
        verifier = XRPackVerifier()
        result = verifier.verify_zip(
            zip_bytes,
            signed_pack.signature,
            signed_pack.public_key,
        )
        
        assert result.valid
        assert result.signature_result.is_valid
        
        # 7. Export and verify directory
        with tempfile.TemporaryDirectory() as tmpdir:
            exported = builder.export(tmpdir)
            
            # Verify exported files
            dir_result = verifier.verify_directory(f"{tmpdir}/xr_pack.v1")
            assert dir_result.valid


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
