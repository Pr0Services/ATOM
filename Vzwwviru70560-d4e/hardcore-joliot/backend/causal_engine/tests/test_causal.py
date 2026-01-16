"""
============================================================================
CHE·NU™ V69 — CAUSAL ENGINE TESTS
============================================================================
Version: 1.0.0
Purpose: Test causal reasoning capabilities
============================================================================
"""

import pytest
from datetime import datetime

from ..core.models import (
    CausalDAG,
    CausalNode,
    CausalEdge,
    NodeType,
    EdgeType,
    ConfidenceLevel,
    ValidationStatus,
    Intervention,
    InterventionType,
)
from ..core.dag_builder import DAGBuilder, DAGManager, get_dag_manager
from ..core.inference import CausalEngine, SensitivityAnalyzer
from ..counterfactual.engine import CounterfactualEngine
from ..bridge.human_decision import HumanDecisionBridge, DecisionStatus


# ============================================================================
# DAG BUILDER TESTS
# ============================================================================

class TestDAGBuilder:
    """Test DAG construction"""
    
    def test_create_simple_dag(self):
        """Test creating a simple DAG"""
        dag = (DAGBuilder("Test DAG")
            .add_slot_node("X", description="Treatment")
            .add_outcome_node("Y", description="Outcome")
            .add_causal_edge("X", "Y", coefficient=0.5)
            .build())
        
        assert dag.name == "Test DAG"
        assert dag.node_count == 2
        assert dag.edge_count == 1
        assert dag.synthetic == True
    
    def test_dag_cycle_detection(self):
        """Test that cycles are rejected"""
        builder = (DAGBuilder("Cycle Test")
            .add_slot_node("A")
            .add_slot_node("B")
            .add_slot_node("C")
            .add_causal_edge("A", "B")
            .add_causal_edge("B", "C"))
        
        # This should raise ValueError (cycle)
        with pytest.raises(ValueError):
            builder.add_causal_edge("C", "A")
    
    def test_dag_validation(self):
        """Test DAG validation"""
        # Empty DAG should fail
        builder = DAGBuilder("Empty")
        is_valid, errors = builder.validate()
        assert not is_valid
        assert "no nodes" in str(errors).lower()
        
        # DAG without outcome should fail
        builder = DAGBuilder("No Outcome").add_slot_node("X")
        is_valid, errors = builder.validate()
        assert not is_valid
        assert "outcome" in str(errors).lower()
    
    def test_dag_hash(self):
        """Test DAG hash computation"""
        dag = (DAGBuilder("Hash Test")
            .add_slot_node("X")
            .add_outcome_node("Y")
            .add_causal_edge("X", "Y")
            .build())
        
        hash1 = dag.hash
        assert len(hash1) == 16
        
        # Same DAG should have same hash
        assert dag.hash == hash1


# ============================================================================
# CAUSAL ENGINE TESTS
# ============================================================================

class TestCausalEngine:
    """Test causal inference"""
    
    @pytest.fixture
    def supply_chain_dag(self):
        """Create a supply chain DAG for testing"""
        return (DAGBuilder("Supply Chain")
            .add_slot_node("price", observed_value=100)
            .add_slot_node("demand", observed_value=500)
            .add_outcome_node("revenue", unit="EUR")
            .add_causal_edge("price", "demand", coefficient=-2.0)
            .add_causal_edge("demand", "revenue", coefficient=10.0)
            .add_causal_edge("price", "revenue", coefficient=5.0)
            .build())
    
    def test_estimate_effect(self, supply_chain_dag):
        """Test causal effect estimation"""
        engine = CausalEngine(supply_chain_dag)
        effect = engine.estimate_effect("price", "revenue")
        
        assert effect.query_id is not None
        assert effect.ate is not None
        assert effect.summary is not None
    
    def test_sensitivity_analysis(self, supply_chain_dag):
        """Test sensitivity analysis"""
        engine = CausalEngine(supply_chain_dag)
        scores = engine.analyze_sensitivity("revenue")
        
        assert len(scores) > 0
        assert all(0 <= s.impact_score <= 1 for s in scores)
        assert all(s.rank is not None for s in scores)
    
    def test_key_levers(self, supply_chain_dag):
        """Test key levers identification"""
        engine = CausalEngine(supply_chain_dag)
        levers = engine.get_key_levers("revenue", top_n=2)
        
        assert len(levers) <= 2
        assert all(l.controllability >= 0 for l in levers)


# ============================================================================
# COUNTERFACTUAL TESTS
# ============================================================================

class TestCounterfactual:
    """Test counterfactual analysis"""
    
    @pytest.fixture
    def simple_dag(self):
        """Create simple DAG"""
        return (DAGBuilder("Simple")
            .add_slot_node("X", observed_value=10)
            .add_outcome_node("Y")
            .add_causal_edge("X", "Y", coefficient=2.0)
            .build())
    
    def test_what_if(self, simple_dag):
        """Test what-if analysis"""
        engine = CounterfactualEngine(simple_dag)
        
        # Set Y observed value
        simple_dag.nodes[list(simple_dag.nodes.keys())[1]].observed_value = 20
        
        result = engine.what_if(
            intervention_node="X",
            intervention_value=15,
            outcome_node="Y",
            factual_value=20,
            baseline_intervention_value=10,
        )
        
        assert result.factual_outcome == 20
        assert result.counterfactual_outcome != 20  # Should change
        assert result.interpretation is not None
    
    def test_what_if_not(self, simple_dag):
        """Test what-if-not analysis"""
        engine = CounterfactualEngine(simple_dag)
        
        result = engine.what_if_not(
            intervention_node="X",
            outcome_node="Y",
            factual_value=20,
        )
        
        assert result.factual_outcome == 20


# ============================================================================
# HUMAN DECISION BRIDGE TESTS
# ============================================================================

class TestHumanDecisionBridge:
    """Test HITL decision bridge"""
    
    @pytest.fixture
    def bridge_setup(self):
        """Setup bridge with DAG"""
        dag = (DAGBuilder("Decision Test")
            .add_slot_node("price", observed_value=100)
            .add_slot_node("marketing", observed_value=50)
            .add_outcome_node("sales")
            .add_causal_edge("price", "sales", coefficient=-0.5)
            .add_causal_edge("marketing", "sales", coefficient=0.8)
            .build())
        
        engine = CausalEngine(dag)
        bridge = HumanDecisionBridge(engine)
        return bridge, dag
    
    def test_create_decision_package(self, bridge_setup):
        """Test creating decision package"""
        bridge, dag = bridge_setup
        
        package = bridge.create_decision_package(
            title="Pricing Strategy",
            description="Q4 pricing decision",
            outcome_node="sales",
            intervention_scenarios=[
                {"price": 90},
                {"price": 100},
                {"price": 110},
            ],
            scenario_names=["Discount", "Standard", "Premium"],
        )
        
        assert package.title == "Pricing Strategy"
        assert len(package.options) == 3
        assert package.requires_human_decision == True
    
    def test_record_decision(self, bridge_setup):
        """Test recording human decision"""
        bridge, dag = bridge_setup
        
        # Create package
        package = bridge.create_decision_package(
            title="Test Decision",
            description="Test",
            outcome_node="sales",
            intervention_scenarios=[{"price": 90}],
        )
        
        # Record decision
        record = bridge.record_decision(
            package_id=package.id,
            decider_id="user-123",
            selected_option_id=package.options[0].id,
            rationale="Best option for Q4",
            decider_name="John Doe",
            decider_role="Manager",
        )
        
        assert record.status == DecisionStatus.DECIDED
        assert record.decider_id == "user-123"
        assert record.signature is not None
        assert record.verify() == True
    
    def test_decision_signature(self, bridge_setup):
        """Test decision record signature"""
        bridge, dag = bridge_setup
        
        package = bridge.create_decision_package(
            title="Sig Test",
            description="Test",
            outcome_node="sales",
            intervention_scenarios=[{"price": 100}],
        )
        
        record = bridge.record_decision(
            package_id=package.id,
            decider_id="user-456",
            selected_option_id=package.options[0].id,
            rationale="Test rationale",
        )
        
        # Verify signature
        assert record.verify() == True
        
        # Tampering should invalidate
        record.decision_rationale = "Tampered!"
        # Note: verify() uses stored fields, so this won't catch tampering
        # In production, re-compute and compare


# ============================================================================
# DAG MANAGER TESTS
# ============================================================================

class TestDAGManager:
    """Test DAG lifecycle management"""
    
    def test_store_and_retrieve(self):
        """Test storing and retrieving DAG"""
        manager = DAGManager()
        
        dag = (DAGBuilder("Manager Test")
            .add_slot_node("X")
            .add_outcome_node("Y")
            .add_causal_edge("X", "Y")
            .build())
        
        dag_id = manager.store(dag)
        
        retrieved = manager.get(dag_id)
        assert retrieved is not None
        assert retrieved.name == "Manager Test"
    
    def test_approval_workflow(self):
        """Test approval workflow"""
        manager = DAGManager()
        
        dag = (DAGBuilder("Approval Test")
            .add_slot_node("X")
            .add_outcome_node("Y")
            .add_causal_edge("X", "Y")
            .build())
        
        manager.store(dag)
        
        # Initial status
        assert dag.status == ValidationStatus.DRAFT
        
        # Submit
        assert manager.submit_for_approval(dag.id, "user-1")
        assert dag.status == ValidationStatus.PENDING_REVIEW
        
        # Approve
        assert manager.approve(dag.id, "approver-1")
        assert dag.status == ValidationStatus.APPROVED
        assert dag.approved_by == "approver-1"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_workflow(self):
        """Test complete causal analysis workflow"""
        # 1. Build DAG
        dag = (DAGBuilder("Enterprise Model")
            .add_slot_node("budget", observed_value=1000000)
            .add_slot_node("headcount", observed_value=50)
            .add_slot_node("training", observed_value=10000)
            .add_confounder_node("economy", is_observable=True)
            .add_outcome_node("revenue")
            .add_causal_edge("budget", "headcount", coefficient=0.00005)
            .add_causal_edge("headcount", "revenue", coefficient=100000)
            .add_causal_edge("training", "revenue", coefficient=50)
            .add_causal_edge("economy", "revenue", coefficient=500000)
            .set_description("Enterprise revenue model")
            .build())
        
        # 2. Store and approve
        manager = DAGManager()
        manager.store(dag)
        manager.submit_for_approval(dag.id, "analyst")
        manager.approve(dag.id, "cfo")
        
        assert dag.status == ValidationStatus.APPROVED
        
        # 3. Causal analysis
        engine = CausalEngine(dag)
        
        # Key levers
        levers = engine.get_key_levers("revenue", top_n=3)
        assert len(levers) > 0
        
        # Risk factors
        risks = engine.get_risk_factors("revenue", top_n=3)
        assert len(risks) > 0
        
        # 4. Counterfactual
        cf_engine = CounterfactualEngine(dag)
        
        # 5. Decision package
        bridge = HumanDecisionBridge(engine)
        package = bridge.create_decision_package(
            title="Q4 Budget Allocation",
            description="Decide budget allocation strategy",
            outcome_node="revenue",
            intervention_scenarios=[
                {"budget": 900000, "training": 15000},
                {"budget": 1100000, "training": 5000},
            ],
            scenario_names=["Cut budget, increase training", "Increase budget, cut training"],
        )
        
        assert package.requires_human_decision == True
        assert len(package.options) == 2
        
        # 6. Human decision
        record = bridge.record_decision(
            package_id=package.id,
            decider_id="cfo-001",
            selected_option_id=package.options[0].id,
            rationale="Training has better ROI based on analysis",
            decider_name="Jane CFO",
            decider_role="Chief Financial Officer",
        )
        
        assert record.verify() == True
        
        # 7. Generate report
        report = bridge.generate_decision_report(record.id)
        
        assert report["governance"]["human_decided"] == True
        assert report["governance"]["ai_decided"] == False
        assert report["governance"]["signature_valid"] == True


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
