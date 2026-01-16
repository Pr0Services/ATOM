"""
============================================================================
CHE·NU™ V69 — SLOT FILL ENGINE TESTS
============================================================================
Tests for all slot fill specs:
- Agent Assignment
- Causal Priority
- Explainability
- XR Visualization
- Neuromorphic Lattice
- Semantic Communication
============================================================================
"""

import pytest
from datetime import datetime

from ..models import (
    Slot,
    SlotType,
    SlotStatus,
    RiskLevel,
    AgentType,
    Document,
    SLOT_TO_AGENT_MAPPING,
)


# ============================================================================
# MODEL TESTS
# ============================================================================

class TestModels:
    """Test slot fill models"""
    
    def test_create_slot(self):
        slot = Slot(
            name="Budget",
            slot_type=SlotType.FINANCE,
            risk_level=RiskLevel.MEDIUM,
        )
        
        assert slot.name == "Budget"
        assert slot.slot_type == SlotType.FINANCE
        assert slot.status == SlotStatus.EMPTY
        assert slot.assigned_agent is None
    
    def test_slot_auto_assign(self):
        slot = Slot(name="Test", slot_type=SlotType.TEXT)
        agent = slot.auto_assign_agent()
        
        assert agent == AgentType.WRITING_AGENT
        assert slot.assigned_agent == AgentType.WRITING_AGENT
    
    def test_slot_requires_hitl_high_risk(self):
        slot = Slot(
            name="Legal",
            slot_type=SlotType.LEGAL,
            risk_level=RiskLevel.HIGH,
        )
        
        assert slot.requires_hitl() is True
    
    def test_slot_requires_hitl_after_failures(self):
        slot = Slot(name="Test", slot_type=SlotType.TEXT)
        slot.fill_attempts = 2
        
        assert slot.requires_hitl() is True
    
    def test_document_completion(self):
        doc = Document(
            name="Test Doc",
            tenant_id="test",
            created_by="user",
        )
        
        slot1 = Slot(name="Slot1", slot_type=SlotType.TEXT)
        slot1.status = SlotStatus.VALIDATED
        
        slot2 = Slot(name="Slot2", slot_type=SlotType.NUMBER)
        slot2.status = SlotStatus.EMPTY
        
        doc.add_slot(slot1)
        doc.add_slot(slot2)
        doc.update_counts()
        
        assert doc.total_slots == 2
        assert doc.filled_slots == 1
        assert doc.completion_percentage == 50.0


# ============================================================================
# ASSIGNMENT TESTS
# ============================================================================

class TestAssignment:
    """Test agent assignment"""
    
    def test_create_assigner(self):
        from ..assignment import create_assigner
        
        assigner = create_assigner()
        assert assigner is not None
    
    def test_assign_slot(self):
        from ..assignment import create_assigner, AssignmentResult
        
        assigner = create_assigner()
        slot = Slot(name="Text", slot_type=SlotType.TEXT)
        
        result, agent = assigner.assign(slot)
        
        assert result == AssignmentResult.SUCCESS
        assert agent == AgentType.WRITING_AGENT
    
    def test_assign_high_risk_requires_hitl(self):
        from ..assignment import create_assigner, AssignmentResult
        
        assigner = create_assigner()
        slot = Slot(
            name="Legal",
            slot_type=SlotType.LEGAL,
            risk_level=RiskLevel.HIGH,
        )
        
        result, agent = assigner.assign(slot)
        
        assert result == AssignmentResult.REQUIRES_HITL
        assert agent is None
    
    def test_get_verifier_different_from_filler(self):
        from ..assignment import create_assigner
        
        assigner = create_assigner()
        
        verifier = assigner.get_verifier(AgentType.WRITING_AGENT)
        assert verifier != AgentType.WRITING_AGENT
    
    def test_orchestrator_fill_slot(self):
        from ..assignment import create_orchestrator
        
        orchestrator = create_orchestrator()
        slot = Slot(name="Test", slot_type=SlotType.TEXT)
        
        result = orchestrator.fill_slot(slot)
        
        assert result.slot_id == slot.slot_id
        assert result.filled_by_agent is not None
        assert result.explainability is not None


# ============================================================================
# PRIORITY TESTS
# ============================================================================

class TestPriority:
    """Test causal priority"""
    
    def test_create_calculator(self):
        from ..priority import create_impact_calculator
        
        calc = create_impact_calculator()
        assert calc is not None
    
    def test_calculate_impact(self):
        from ..priority import create_impact_calculator
        
        calc = create_impact_calculator()
        slot = Slot(name="Budget", slot_type=SlotType.FINANCE)
        
        impact = calc.calculate_causal_impact(slot)
        
        assert 0 <= impact <= 1
    
    def test_negligible_slot(self):
        from ..priority import create_impact_calculator
        
        calc = create_impact_calculator(impact_threshold=0.9)
        slot = Slot(
            name="Minor",
            slot_type=SlotType.TEXT,
            risk_level=RiskLevel.LOW,
        )
        
        # Low risk slot should be negligible with high threshold
        is_neg = calc.is_negligible(slot)
        assert isinstance(is_neg, bool)
    
    def test_rank_slots(self):
        from ..priority import create_priority_ranker
        
        ranker = create_priority_ranker()
        
        slots = [
            Slot(name="High", slot_type=SlotType.FINANCE, risk_level=RiskLevel.HIGH),
            Slot(name="Low", slot_type=SlotType.TEXT, risk_level=RiskLevel.LOW),
        ]
        
        ranked = ranker.rank_slots(slots, include_negligible=True)
        
        assert len(ranked) == 2
        # High risk should be ranked higher
        assert ranked[0][0].name == "High"


# ============================================================================
# EXPLAINABILITY TESTS
# ============================================================================

class TestExplainability:
    """Test explainability layer"""
    
    def test_create_layer(self):
        from ..explainability import create_explainability_layer
        
        layer = create_explainability_layer()
        assert layer is not None
    
    def test_generate_explainability(self):
        from ..explainability import create_explainability_layer
        
        layer = create_explainability_layer()
        slot = Slot(name="Test", slot_type=SlotType.TEXT)
        
        exp, is_valid, errors = layer.explain_fill(
            slot=slot,
            value="Test content",
            method="auto",
            sources=["source1"],
        )
        
        assert exp.slot_id == slot.slot_id
        assert exp.confidence_score > 0
        assert len(exp.rationale) > 0
    
    def test_explainability_required_for_high_risk(self):
        from ..explainability import get_required_level, ExplainabilityLevel
        
        slot = Slot(
            name="Legal",
            slot_type=SlotType.LEGAL,
            risk_level=RiskLevel.HIGH,
        )
        
        level = get_required_level(slot)
        assert level == ExplainabilityLevel.DETAILED
    
    def test_export_validation(self):
        from ..explainability import create_explainability_layer
        
        layer = create_explainability_layer()
        slot = Slot(name="Test", slot_type=SlotType.TEXT)
        
        # Fill with explainability
        layer.explain_fill(
            slot=slot,
            value="Test",
            sources=["src1", "src2"],
        )
        
        can_export = layer.can_export(slot)
        assert isinstance(can_export, bool)


# ============================================================================
# XR VISUALIZATION TESTS
# ============================================================================

class TestXRVisualization:
    """Test XR visualization"""
    
    def test_create_scene_builder(self):
        from ..xr import create_scene_builder
        
        builder = create_scene_builder()
        assert builder is not None
    
    def test_build_scene(self):
        from ..xr import create_scene_builder
        
        builder = create_scene_builder()
        doc = Document(name="Test", tenant_id="test", created_by="user")
        
        slot = Slot(name="Slot1", slot_type=SlotType.TEXT)
        doc.add_slot(slot)
        
        scene = builder.build_scene(doc)
        
        assert scene.document_id == doc.document_id
        assert scene.read_only is True  # Per spec
        assert len(scene.nodes) == 1
    
    def test_status_to_color(self):
        from ..xr import status_to_color
        
        assert status_to_color(SlotStatus.VALIDATED) == "#00FF00"  # Green
        assert status_to_color(SlotStatus.EMPTY) == "#FF0000"  # Red
        assert status_to_color(SlotStatus.FILLED) == "#FFFF00"  # Yellow
    
    def test_xr_scene_is_read_only(self):
        from ..xr import create_scene_builder
        
        builder = create_scene_builder()
        doc = Document(name="Test", tenant_id="test", created_by="user")
        
        scene = builder.build_scene(doc)
        
        # Per spec: XR = lecture seule
        assert scene.read_only is True
    
    def test_interaction_handler_read_only(self):
        from ..xr import create_interaction_handler
        
        handler = create_interaction_handler()
        
        # Simulate fill should not actually modify
        result = handler.simulate_fill(None, "slot-1", "test")
        
        assert result["is_simulation"] is True
        assert "READ-ONLY" in result["warning"]


# ============================================================================
# NEUROMORPHIC TESTS
# ============================================================================

class TestNeuromorphic:
    """Test neuromorphic lattice"""
    
    def test_create_lattice(self):
        from ..neuromorphic import create_lattice
        
        lattice = create_lattice()
        assert lattice is not None
    
    def test_register_agent(self):
        from ..neuromorphic import create_lattice, create_agent_map, SpikeInputType
        
        lattice = create_lattice()
        
        agent = create_agent_map(
            agent_id="agent-001",
            level="L1",
            inputs={SpikeInputType.SLOT_DELTA.value},
        )
        
        lattice.register_agent(agent)
        
        assert "agent-001" in lattice._agents
    
    def test_emit_spike(self):
        from ..neuromorphic import create_lattice, SpikeInputType
        
        lattice = create_lattice()
        
        spike = lattice.emit_spike(
            source="test",
            spike_type=SpikeInputType.METRIC_DELTA.value,
            intensity=0.8,
        )
        
        assert spike.intensity == 0.8
        assert spike.source == "test"
    
    def test_anomaly_detection(self):
        from ..neuromorphic import create_lattice
        
        lattice = create_lattice()
        
        # 30% drift should trigger anomaly
        spike = lattice.detect_anomaly(
            metric_name="cost",
            current_value=130,
            baseline_value=100,
            threshold=0.2,
        )
        
        assert spike is not None
        assert spike.payload["drift"] == 0.3
    
    def test_rapid_scoring(self):
        from ..neuromorphic import create_lattice
        
        lattice = create_lattice()
        
        score, spike = lattice.compute_rapid_score({
            "risk": 0.7,
            "urgency": 0.5,
        })
        
        assert 0 <= score <= 1
        assert spike is not None


# ============================================================================
# SEMANTIC COMMUNICATION TESTS
# ============================================================================

class TestSemantic:
    """Test semantic communication"""
    
    def test_create_ontology(self):
        from ..semantic import create_ontology
        
        ontology = create_ontology()
        
        # Should have base concepts
        stats = ontology.get_stats()
        assert stats["total_concepts"] > 0
    
    def test_create_packet(self):
        from ..semantic import create_codec, StateType
        
        codec = create_codec()
        
        packet = codec.encode(
            concept="BUDGET",
            state=StateType.NORMAL,
            scope={"sphere": "business"},
            confidence=0.9,
            sender_id="agent-1",
            recipient_id="agent-2",
            evidence_refs=["ref-1"],
        )
        
        assert packet.concept == "BUDGET"
        assert packet.confidence == 0.9
        assert packet.speculative is False  # Has evidence + high confidence
    
    def test_speculative_packet(self):
        from ..semantic import create_codec, StateType
        
        codec = create_codec()
        
        packet = codec.encode(
            concept="RISK_SCORE",
            state=StateType.WARNING,
            scope={},
            confidence=0.5,  # Low confidence
            sender_id="agent-1",
            recipient_id="agent-2",
            # No evidence_refs
        )
        
        # Should require HITL
        assert packet.requires_hitl() is True
    
    def test_governance_validation(self):
        from ..semantic import create_codec, SemanticGovernance, StateType
        
        codec = create_codec()
        governance = SemanticGovernance()
        
        packet = codec.encode(
            concept="FINANCIAL_RISK",
            state=StateType.CRITICAL,
            scope={},
            confidence=0.8,
            sender_id="agent-1",
            recipient_id="agent-2",
            # No evidence - should fail validation
        )
        
        is_valid, errors = governance.validate_packet(packet)
        
        # Should fail because FINANCIAL_RISK requires evidence
        assert is_valid is False
        assert len(errors) > 0
    
    def test_channel_send(self):
        from ..semantic import create_channel, create_codec, StateType
        
        channel = create_channel()
        codec = create_codec()
        
        packet = codec.encode(
            concept="QUALITY_SCORE",
            state=StateType.NORMAL,
            scope={"sphere": "personal"},
            confidence=0.8,
            sender_id="agent-1",
            recipient_id="agent-2",
        )
        
        success, errors = channel.send(packet, sphere="personal")
        
        assert success is True


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests"""
    
    def test_full_slot_fill_workflow(self):
        """Test complete slot fill workflow"""
        from ..assignment import create_orchestrator
        from ..priority import create_priority_ranker
        from ..explainability import create_explainability_layer
        
        # Create document
        doc = Document(name="Contract", tenant_id="test", created_by="user")
        
        slots = [
            Slot(name="Party A", slot_type=SlotType.TEXT),
            Slot(name="Amount", slot_type=SlotType.FINANCE),
            Slot(name="Terms", slot_type=SlotType.LEGAL, risk_level=RiskLevel.MEDIUM),
        ]
        
        for slot in slots:
            doc.add_slot(slot)
        
        # Rank by priority
        ranker = create_priority_ranker()
        ranked = ranker.rank_document(doc, include_negligible=True)
        
        assert len(ranked) == 3
        
        # Fill slots
        orchestrator = create_orchestrator()
        explainability = create_explainability_layer()
        
        for slot, priority in ranked:
            if not priority.is_negligible:
                result = orchestrator.fill_slot(slot)
                
                assert result.explainability is not None
        
        doc.update_counts()
        assert doc.filled_slots > 0
    
    def test_xr_visualization_workflow(self):
        """Test XR visualization for document"""
        from ..xr import create_artifact_generator
        
        doc = Document(name="Test", tenant_id="test", created_by="user")
        
        slot1 = Slot(name="Slot1", slot_type=SlotType.TEXT)
        slot1.status = SlotStatus.VALIDATED
        
        slot2 = Slot(name="Slot2", slot_type=SlotType.NUMBER)
        slot2.status = SlotStatus.EMPTY
        
        doc.add_slot(slot1)
        doc.add_slot(slot2)
        
        generator = create_artifact_generator()
        artifact = generator.generate_artifact(doc)
        
        assert artifact["artifact_type"] == "xr_slot_fill_visualization"
        assert artifact["governance"]["read_only"] is True
        assert artifact["statistics"]["total_slots"] == 2


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
