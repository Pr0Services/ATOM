"""
============================================================================
CHE·NU™ V69 — SECURITY MODULE TESTS
============================================================================
"""

import pytest
from datetime import datetime


# ============================================================================
# POST-QUANTUM SECURITY TESTS
# ============================================================================

class TestPostQuantumSecurity:
    """Test post-quantum security"""
    
    def test_create_system(self):
        from ..post_quantum import create_security_system
        system = create_security_system()
        assert system is not None
    
    def test_key_generation(self):
        from ..post_quantum import create_key_manager
        from ..models import SignatureAlgorithm
        
        keys = create_key_manager()
        key = keys.generate_key_pair(SignatureAlgorithm.DILITHIUM)
        
        assert key is not None
        assert key.algorithm == SignatureAlgorithm.DILITHIUM
        assert keys.is_key_valid(key.key_id)
    
    def test_hybrid_signature(self):
        from ..post_quantum import create_security_system
        from ..models import SignatureAlgorithm
        
        system = create_security_system()
        
        # Get hybrid key
        keys = system.keys.get_keys_by_algorithm(SignatureAlgorithm.HYBRID)
        key = keys[0] if keys else system.keys.generate_key_pair(SignatureAlgorithm.HYBRID)
        
        # Sign
        data = {"test": "data"}
        signature = system.signatures.sign(data, key.key_id)
        
        assert signature.algorithm == SignatureAlgorithm.HYBRID
        assert signature.classical_signature is not None
        assert signature.pq_signature is not None
    
    def test_verify_signature(self):
        from ..post_quantum import create_security_system
        
        system = create_security_system()
        
        data = {"important": "artifact"}
        signature = system.sign_artifact(data, "client-1")
        
        assert system.verify_artifact(data, signature)


# ============================================================================
# AUDIT LOG TESTS
# ============================================================================

class TestAuditLogs:
    """Test immutable audit logs"""
    
    def test_create_system(self):
        from ..audit_logs import create_audit_system
        system = create_audit_system()
        assert system is not None
    
    def test_log_events(self):
        from ..audit_logs import create_audit_system
        from ..models import EventType
        
        system = create_audit_system()
        
        event = system.log(
            EventType.WORLD_ENGINE_STEP,
            "engine",
            "step_1",
            {"inputs": {"a": 1}}
        )
        
        assert event.event_hash != ""
        assert event.previous_hash == "genesis"
    
    def test_event_chain(self):
        from ..audit_logs import create_audit_system
        from ..models import EventType
        
        system = create_audit_system()
        
        e1 = system.log(EventType.WORLD_ENGINE_STEP, "engine", "step_1", {})
        e2 = system.log(EventType.OPA_DECISION, "opa", "allow", {"policy": "test"})
        
        # Chain integrity
        assert e2.previous_hash == e1.event_hash
    
    def test_merkle_tree(self):
        from ..audit_logs import create_audit_system
        from ..models import EventType
        
        system = create_audit_system()
        
        # Log events
        for i in range(5):
            system.log(EventType.WORLD_ENGINE_STEP, "engine", f"step_{i}", {})
        
        # Finalize
        tree = system.finalize_simulation("sim-1")
        
        assert tree.root_hash != ""
        assert tree.leaf_count == 5
    
    def test_export_jsonl(self):
        from ..audit_logs import create_audit_system
        from ..models import EventType
        
        system = create_audit_system()
        system.log(EventType.RANDOM_SEED, "system", "seed", {"seed": 42})
        
        jsonl = system.export_audit_log()
        
        assert "RANDOM_SEED" in jsonl
        assert "42" in jsonl


# ============================================================================
# XR VERIFICATION TESTS
# ============================================================================

class TestXRVerification:
    """Test XR blockchain verification"""
    
    def test_create_system(self):
        from ..xr_verification import create_xr_verification_system
        system = create_xr_verification_system()
        assert system is not None
    
    def test_hash_frames(self):
        from ..xr_verification import create_xr_verification_system
        
        system = create_xr_verification_system()
        
        frames = [
            {"position": [0, 0, 0], "data": "frame_0"},
            {"position": [1, 0, 0], "data": "frame_1"},
            {"position": [2, 0, 0], "data": "frame_2"},
        ]
        
        chunks = system.hasher.hash_frame_sequence(frames)
        
        assert len(chunks) == 3
        assert all(c.content_hash != "" for c in chunks)
    
    def test_create_proof(self):
        from ..xr_verification import create_xr_verification_system
        
        system = create_xr_verification_system()
        
        frames = [{"data": f"frame_{i}"} for i in range(10)]
        proof = system.process_xr_session("session-1", frames)
        
        assert proof.merkle_root != ""
        assert len(proof.chunk_hashes) == 10
        assert proof.ledger_ref != ""
    
    def test_verify_before_render(self):
        from ..xr_verification import create_xr_verification_system
        
        system = create_xr_verification_system()
        
        frames = [{"data": "frame_0"}, {"data": "frame_1"}]
        system.process_xr_session("session-1", frames)
        
        # Verify valid frame
        valid = system.verify_before_render("session-1", 0, {"data": "frame_0"})
        assert valid
        
        # Verify tampered frame
        invalid = system.verify_before_render("session-1", 0, {"data": "TAMPERED"})
        assert not invalid
    
    def test_ledger_chain(self):
        from ..xr_verification import create_xr_verification_system
        
        system = create_xr_verification_system()
        
        # Create multiple sessions
        for i in range(3):
            frames = [{"data": f"session_{i}_frame_{j}"} for j in range(5)]
            system.process_xr_session(f"session-{i}", frames)
        
        status = system.get_ledger_status()
        
        assert status["chain_length"] == 3
        assert status["chain_valid"] == True


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestSecurityIntegration:
    """Integration tests"""
    
    def test_full_security_pipeline(self):
        """Test complete security flow"""
        from ..post_quantum import create_security_system
        from ..audit_logs import create_audit_system
        from ..xr_verification import create_xr_verification_system
        from ..models import EventType
        
        # 1. Setup systems
        pq = create_security_system()
        audit = create_audit_system()
        xr = create_xr_verification_system()
        
        # 2. Simulate a workflow with audit
        audit.log(EventType.WORLD_ENGINE_STEP, "engine", "start", {})
        audit.log(EventType.OPA_DECISION, "opa", "allow", {"policy": "sim"})
        audit.log(EventType.WORLD_ENGINE_STEP, "engine", "compute", {})
        
        # 3. Finalize simulation
        tree = audit.finalize_simulation("sim-1")
        
        # 4. Protect audit with PQ signature
        audit_data = {"root": tree.root_hash, "count": tree.leaf_count}
        audit_signature = pq.protect_audit_log(audit_data)
        
        # 5. Create XR visualization
        xr_frames = [
            {"type": "dag_view", "nodes": 5},
            {"type": "flow_view", "edges": 3},
        ]
        xr_proof = xr.process_xr_session("xr-sim-1", xr_frames)
        
        # 6. Log XR pack
        audit.log(EventType.XR_PACK_GENERATION, "xr", "pack", {
            "session": xr_proof.session_id,
            "root": xr_proof.merkle_root,
        })
        
        # 7. Verify everything
        assert tree.root_hash != ""
        assert pq.verify_artifact(audit_data, audit_signature)
        assert xr.get_ledger_status()["chain_valid"]
        
        print()
        print("✅ Full security pipeline verified!")
        print(f"   Audit events: {len(audit.logger.get_events())}")
        print(f"   Merkle root: {tree.root_hash[:16]}...")
        print(f"   PQ signature: {audit_signature.algorithm.value}")
        print(f"   XR ledger blocks: {xr.get_ledger_status()['chain_length']}")


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
