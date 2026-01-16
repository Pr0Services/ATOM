"""
============================================================================
CHE·NU™ V69 — FEEDBACK & AUDIT TESTS
============================================================================
Version: 1.0.0
Purpose: Test feedback loops and audit trail
============================================================================
"""

import pytest
from datetime import datetime

# Feedback imports
from ..models import (
    Slot,
    WorldState,
    FeedbackEdge,
    TransferFunction,
    FeedbackParams,
    SimulationConfig,
    SimulationArtifact,
    LoopType,
    FeedbackModel,
    StabilityStatus,
)
from ..loops.engine import FeedbackLoopEngine, L2SafetyController
from ..loops.audited import AuditedFeedbackEngine, create_audited_simulation

# Audit imports
from ...audit.logs.immutable import (
    AuditLog,
    AuditEvent,
    EventType,
    AuditLevel,
    MerkleTree,
)


# ============================================================================
# SLOT TESTS
# ============================================================================

class TestSlot:
    """Test Slot model"""
    
    def test_slot_creation(self):
        slot = Slot(name="Budget", value=1000000, unit="EUR")
        assert slot.name == "Budget"
        assert slot.value == 1000000
        assert slot.unit == "EUR"
    
    def test_slot_delta(self):
        slot = Slot(name="Budget", value=1100000, previous_value=1000000)
        assert slot.delta == 100000
        assert slot.growth_ratio == 1.1
    
    def test_slot_clamp(self):
        slot = Slot(name="Budget", value=1500000, min_value=0, max_value=1000000)
        clamped = slot.apply_clamp()
        assert clamped == True
        assert slot.value == 1000000
    
    def test_slot_advance(self):
        slot = Slot(name="Budget", value=1000000, timestamp_sim=0)
        new_slot = slot.advance(1100000, 1)
        assert new_slot.value == 1100000
        assert new_slot.previous_value == 1000000
        assert new_slot.timestamp_sim == 1


# ============================================================================
# WORLD STATE TESTS
# ============================================================================

class TestWorldState:
    """Test WorldState model"""
    
    def test_state_creation(self):
        state = WorldState(tick=0, simulation_id="sim-001")
        assert state.tick == 0
        assert state.synthetic == True
    
    def test_state_slots(self):
        state = WorldState(tick=0)
        state.set_slot(Slot(name="Budget", value=1000000))
        state.set_slot(Slot(name="Production", value=850000))
        
        assert state.get_value("Budget") == 1000000
        assert state.get_value("Production") == 850000
        assert state.get_value("Unknown", 0) == 0
    
    def test_state_hash(self):
        state = WorldState(tick=0)
        state.set_slot(Slot(name="Budget", value=1000000))
        
        hash1 = state.hash
        assert len(hash1) == 64  # SHA256
        
        # Same state should have same hash
        assert state.hash == hash1
    
    def test_state_clone(self):
        state = WorldState(tick=0, simulation_id="sim-001")
        state.set_slot(Slot(name="Budget", value=1000000))
        
        next_state = state.clone_for_next_tick()
        assert next_state.tick == 1
        assert next_state.previous_state_hash == state.hash


# ============================================================================
# FEEDBACK EDGE TESTS
# ============================================================================

class TestFeedbackEdge:
    """Test FeedbackEdge model"""
    
    def test_linear_feedback(self):
        edge = FeedbackEdge(
            name="budget_feedback",
            target_slot="Budget",
            source_slots=["Budget", "Production"],
            coefficients={"Budget": 0.95, "Production": 0.1},
            model=FeedbackModel.LINEAR,
        )
        
        state = WorldState(tick=0)
        state.set_slot(Slot(name="Budget", value=1000000))
        state.set_slot(Slot(name="Production", value=850000))
        
        next_value = edge.compute_next_value(state)
        
        # Budget * 0.95 + Production * 0.1 = 950000 + 85000 = 1035000
        assert next_value == pytest.approx(1035000)
    
    def test_logistic_feedback(self):
        edge = FeedbackEdge(
            name="growth",
            target_slot="Users",
            source_slots=["Users"],
            model=FeedbackModel.LOGISTIC,
            carrying_capacity=1000000,
            growth_rate=0.1,
        )
        
        state = WorldState(tick=0)
        state.set_slot(Slot(name="Users", value=100000))
        
        next_value = edge.compute_next_value(state)
        
        # Logistic: 100000 + 0.1 * 100000 * (1 - 100000/1000000) = 109000
        assert next_value == pytest.approx(109000)


# ============================================================================
# FEEDBACK ENGINE TESTS
# ============================================================================

class TestFeedbackEngine:
    """Test FeedbackLoopEngine"""
    
    @pytest.fixture
    def simple_config(self):
        return SimulationConfig(
            name="Simple Test",
            t_start=0,
            t_end=5,
            initial_slots=[
                Slot(name="Budget", value=1000000),
                Slot(name="Efficiency", value=0.85),
            ],
            transfer_functions=[
                TransferFunction(
                    name="compute_production",
                    output_slot="Production",
                    input_slots=["Budget", "Efficiency"],
                    coefficients={"Budget": 0.85},
                ),
            ],
            feedback_edges=[
                FeedbackEdge(
                    name="budget_feedback",
                    target_slot="Budget",
                    source_slots=["Budget", "Production"],
                    coefficients={"Budget": 0.95, "Production": 0.1},
                ),
            ],
            params=FeedbackParams(
                clamp_min=0,
                clamp_max=10000000,
            ),
        )
    
    def test_engine_creation(self, simple_config):
        engine = FeedbackLoopEngine(simple_config)
        assert len(engine.states) == 1
        assert engine.current_tick == 0
    
    def test_single_step(self, simple_config):
        engine = FeedbackLoopEngine(simple_config)
        result = engine.step()
        
        assert result["t_from"] == 0
        assert result["t_to"] == 1
        assert "artifact_id" in result
        assert len(engine.states) == 2
        assert len(engine.artifacts) == 1
    
    def test_full_simulation(self, simple_config):
        engine = FeedbackLoopEngine(simple_config)
        summary = engine.run()
        
        assert summary["ticks_executed"] == 5
        assert summary["artifact_chain_valid"] == True
        assert "final_state" in summary
    
    def test_artifact_chain(self, simple_config):
        engine = FeedbackLoopEngine(simple_config)
        engine.run()
        
        # Verify chain
        for i, artifact in enumerate(engine.artifacts):
            assert artifact.verify()
            
            if i > 0:
                prev_artifact = engine.artifacts[i - 1]
                assert artifact.previous_artifact_hash == prev_artifact.hash


# ============================================================================
# L2 SAFETY CONTROLLER TESTS
# ============================================================================

class TestL2SafetyController:
    """Test L2SafetyController"""
    
    def test_explosion_detection(self):
        params = FeedbackParams(max_growth_ratio=1.3)
        controller = L2SafetyController(params)
        
        prev_state = WorldState(tick=0)
        prev_state.set_slot(Slot(name="Budget", value=1000000))
        
        next_state = WorldState(tick=1)
        next_state.set_slot(Slot(name="Budget", value=2000000))  # 2x growth
        
        status, actions = controller.analyze(prev_state, next_state)
        
        assert status == StabilityStatus.EXPLODING
        assert len(actions) > 0
        assert actions[0]["action"] == "clamp"
    
    def test_collapse_detection(self):
        params = FeedbackParams(min_value_floor=100)
        controller = L2SafetyController(params)
        
        prev_state = WorldState(tick=0)
        prev_state.set_slot(Slot(name="Budget", value=1000))
        
        next_state = WorldState(tick=1)
        next_state.set_slot(Slot(name="Budget", value=50))  # Below floor
        
        status, actions = controller.analyze(prev_state, next_state)
        
        assert status == StabilityStatus.COLLAPSING
        assert len(actions) > 0


# ============================================================================
# MERKLE TREE TESTS
# ============================================================================

class TestMerkleTree:
    """Test MerkleTree"""
    
    def test_tree_creation(self):
        tree = MerkleTree()
        assert tree.root is None
        assert len(tree.leaves) == 0
    
    def test_add_events(self):
        tree = MerkleTree()
        
        event1 = AuditEvent(
            event_type=EventType.SIMULATION_START,
            message="Test 1",
        )
        event2 = AuditEvent(
            event_type=EventType.SIMULATION_END,
            message="Test 2",
        )
        
        tree.add_event(event1)
        tree.add_event(event2)
        
        assert len(tree.leaves) == 2
    
    def test_build_tree(self):
        tree = MerkleTree()
        
        for i in range(4):
            event = AuditEvent(
                event_type=EventType.SIMULATION_STEP,
                message=f"Step {i}",
            )
            tree.add_event(event)
        
        root = tree.build()
        
        assert root is not None
        assert len(root) == 64  # SHA256
    
    def test_proof_verification(self):
        tree = MerkleTree()
        events = []
        
        for i in range(4):
            event = AuditEvent(
                event_type=EventType.SIMULATION_STEP,
                message=f"Step {i}",
            )
            tree.add_event(event)
            events.append(event)
        
        tree.build()
        
        # Get proof for first event
        proof = tree.get_proof(events[0].hash)
        
        assert len(proof) > 0
        
        # Verify proof
        is_valid = tree.verify_proof(events[0].hash, proof, tree.root)
        assert is_valid == True


# ============================================================================
# AUDIT LOG TESTS
# ============================================================================

class TestAuditLog:
    """Test AuditLog"""
    
    def test_log_creation(self):
        log = AuditLog(simulation_id="sim-001")
        assert len(log.events) == 0
    
    def test_record_event(self):
        log = AuditLog(simulation_id="sim-001")
        
        event = log.record(
            EventType.SIMULATION_START,
            "Simulation started",
            data={"t_start": 0},
        )
        
        assert len(log.events) == 1
        assert event.simulation_id == "sim-001"
        assert event.synthetic == True
    
    def test_finalize(self):
        log = AuditLog(simulation_id="sim-001")
        
        log.record(EventType.SIMULATION_START, "Start")
        log.record(EventType.SIMULATION_STEP, "Step 1")
        log.record(EventType.SIMULATION_END, "End")
        
        root = log.finalize()
        
        assert root is not None
        assert len(root) == 64
    
    def test_verify_event(self):
        log = AuditLog(simulation_id="sim-001")
        
        event = log.record(EventType.SIMULATION_START, "Start")
        log.record(EventType.SIMULATION_END, "End")
        
        log.finalize()
        
        is_valid = log.verify_event(event.event_id)
        assert is_valid == True
    
    def test_audit_report(self):
        log = AuditLog(simulation_id="sim-001")
        
        log.record(EventType.SIMULATION_START, "Start")
        log.record_opa_decision("opa-001", True)
        log.record_safety_action("clamp", "Budget", "Growth exceeded")
        log.finalize()
        
        report = log.generate_audit_report()
        
        assert report["summary"]["total_events"] > 0
        assert "merkle_root" in report["integrity"]


# ============================================================================
# AUDITED FEEDBACK ENGINE TESTS
# ============================================================================

class TestAuditedFeedbackEngine:
    """Test AuditedFeedbackEngine integration"""
    
    def test_audited_simulation(self):
        engine = create_audited_simulation(
            name="Audited Test",
            initial_values={"Budget": 1000000},
            feedback_rules={"Budget": {"Budget": 1.05}},
            num_ticks=5,
        )
        
        results = engine.run()
        
        assert results["audit"]["finalized"] == True
        assert results["audit"]["event_count"] > 0
        assert "merkle_root" in results["audit"]
    
    def test_verify_events(self):
        engine = create_audited_simulation(
            name="Verify Test",
            initial_values={"Budget": 1000000},
            feedback_rules={"Budget": {"Budget": 1.05}},
            num_ticks=3,
        )
        
        engine.run()
        
        # Verify all events
        for event in engine.audit_log.events:
            is_valid = engine.verify_event(event.event_id)
            assert is_valid == True
    
    def test_get_proof(self):
        engine = create_audited_simulation(
            name="Proof Test",
            initial_values={"Budget": 1000000},
            feedback_rules={"Budget": {"Budget": 1.05}},
            num_ticks=3,
        )
        
        engine.run()
        
        # Get proof for first event
        event = engine.audit_log.events[0]
        proof = engine.get_proof(event.event_id)
        
        assert proof is not None
        assert "merkle_root" in proof or "root" in proof


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_workflow(self):
        """Test complete feedback + audit workflow"""
        
        # 1. Create audited simulation
        engine = create_audited_simulation(
            name="Enterprise Model",
            initial_values={
                "Budget": 1000000,
                "Efficiency": 0.85,
            },
            feedback_rules={
                "Budget": {"Budget": 0.95, "Production": 0.1},
            },
            transfer_rules={
                "Production": {"Budget": 0.85},
            },
            num_ticks=10,
            params=FeedbackParams(
                clamp_min=0,
                clamp_max=10000000,
                max_growth_ratio=1.5,
            ),
        )
        
        # 2. Run simulation
        results = engine.run()
        
        # 3. Verify results
        assert results["ticks_executed"] == 10
        assert results["artifact_chain_valid"] == True
        assert results["audit"]["finalized"] == True
        
        # 4. Verify Merkle root
        root = engine.get_merkle_root()
        assert len(root) == 64
        
        # 5. Get audit report
        report = engine.get_audit_report()
        assert report["summary"]["total_events"] > 10
        assert report["integrity"]["merkle_root"] == root
        
        # 6. Verify all artifacts signed
        for artifact in engine.artifacts:
            assert artifact.verify() == True
        
        # 7. Verify chain integrity
        for i in range(1, len(engine.artifacts)):
            assert engine.artifacts[i].previous_artifact_hash == engine.artifacts[i-1].hash


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
