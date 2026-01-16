"""
============================================================================
CHE·NU™ V69 — CORE ENGINES MODULE TESTS
============================================================================
"""

import pytest
from datetime import datetime


# ============================================================================
# WORLDENGINE TESTS
# ============================================================================

class TestWorldEngine:
    """Test WorldEngine core"""
    
    def test_create_engine(self):
        from ..world_engine import create_engine
        engine = create_engine()
        assert engine is not None
    
    def test_create_state(self):
        from ..world_engine import create_engine
        
        engine = create_engine()
        state = engine.create_state({
            "budget": 1000,
            "efficiency": 0.8,
        })
        
        assert state is not None
        assert "budget" in state.slots
        assert state.slots["budget"].value == 1000
    
    def test_run_cycle(self):
        from ..world_engine import create_engine
        
        engine = create_engine()
        state = engine.create_state({
            "budget": 1000,
            "efficiency": 0.8,
        })
        
        new_state, artifact = engine.run_cycle(
            state.state_id,
            "production",
            {"budget": "budget", "efficiency": "efficiency"},
            "production",
        )
        
        assert artifact is not None
        assert "production" in new_state.slots
        assert new_state.slots["production"].value == 800  # 1000 * 0.8
    
    def test_artifact_verified(self):
        from ..world_engine import create_engine
        
        engine = create_engine()
        state = engine.create_state({"budget": 100, "efficiency": 1.0})
        _, artifact = engine.run_cycle(
            state.state_id, "production",
            {"budget": "budget", "efficiency": "efficiency"}, "production"
        )
        
        assert engine.verify_artifact(artifact)


# ============================================================================
# CAUSAL INFERENCE TESTS
# ============================================================================

class TestCausalInference:
    """Test causal inference engine"""
    
    def test_create_engine(self):
        from ..causal_inference import create_inference_engine
        engine = create_inference_engine()
        assert engine is not None
    
    def test_build_dag(self):
        from ..causal_inference import create_dag_builder
        
        builder = create_dag_builder()
        dag = (builder
            .new_dag("Test DAG")
            .add_slot("A", 10)
            .add_slot("B", 20)
            .add_slot("C", 0)
            .add_edge("A", "B", 0.5)
            .add_edge("B", "C", 0.8)
            .build())
        
        assert dag is not None
        assert len(dag.slots) == 3
        assert len(dag.edges) == 2
    
    def test_find_root_causes(self):
        from ..causal_inference import create_inference_engine, create_dag_builder
        
        builder = create_dag_builder()
        dag = (builder
            .new_dag("Test")
            .add_slot("root1", 10)
            .add_slot("root2", 20)
            .add_slot("middle", 0)
            .add_slot("target", 0)
            .add_edge("root1", "middle", 0.5)
            .add_edge("root2", "middle", 0.3)
            .add_edge("middle", "target", 0.8)
            .build())
        
        engine = create_inference_engine()
        engine.register_dag(dag)
        
        roots = engine.find_root_causes(dag.dag_id, "target")
        
        assert "root1" in roots
        assert "root2" in roots
    
    def test_do_intervention(self):
        from ..causal_inference import create_inference_engine, create_dag_builder
        
        builder = create_dag_builder()
        dag = (builder
            .new_dag("Test")
            .add_slot("X", 10)
            .add_slot("Y", 20)
            .add_edge("X", "Y", 0.5)
            .build())
        
        engine = create_inference_engine()
        engine.register_dag(dag)
        
        modified_dag, intervention = engine.do_intervention(
            dag.dag_id, "X", 50, "admin"
        )
        
        assert modified_dag.slots["X"].value == 50
        assert len(modified_dag.edges) == 0  # Incoming edges removed


# ============================================================================
# CAUSAL DECISION TESTS
# ============================================================================

class TestCausalDecision:
    """Test causal decision engine"""
    
    def test_create_engine(self):
        from ..causal_decision import create_decision_engine
        engine = create_decision_engine()
        assert engine is not None
    
    def test_register_dag_with_validation(self):
        from ..causal_decision import create_decision_engine
        from ..causal_inference import create_dag_builder
        
        builder = create_dag_builder()
        dag = (builder
            .new_dag("Business Model")
            .add_slot("marketing", 100)
            .add_slot("sales", 0)
            .add_slot("revenue", 0)
            .add_edge("marketing", "sales", 0.7)
            .add_edge("sales", "revenue", 0.9)
            .build())
        
        engine = create_decision_engine()
        valid, issues = engine.register_dag(dag, "admin-1")
        
        assert valid
        assert len(issues) == 0
        assert dag.validated
    
    def test_blocked_discriminatory_dag(self):
        from ..causal_decision import create_decision_engine
        from ..causal_inference import create_dag_builder
        
        builder = create_dag_builder()
        dag = (builder
            .new_dag("Bad DAG")
            .add_slot("race_factor", 1)
            .add_slot("outcome", 0)
            .add_edge("race_factor", "outcome", 0.5)
            .build())
        
        engine = create_decision_engine()
        valid, issues = engine.register_dag(dag, "admin-1")
        
        assert not valid
        assert len(issues) > 0
    
    def test_analyze_impact(self):
        from ..causal_decision import create_decision_engine
        from ..causal_inference import create_dag_builder
        
        builder = create_dag_builder()
        dag = (builder
            .new_dag("Impact Test")
            .add_slot("budget", 100)
            .add_slot("team", 50)
            .add_slot("output", 0)
            .add_edge("budget", "output", 0.8)
            .add_edge("team", "output", 0.2)
            .build())
        
        engine = create_decision_engine()
        engine.register_dag(dag, "admin")
        
        scores = engine.analyze_slot_impact(dag.dag_id, "output")
        
        assert "budget" in scores
        assert scores["budget"].impact_percent > scores["team"].impact_percent


# ============================================================================
# GAME BRIDGE TESTS
# ============================================================================

class TestGameBridge:
    """Test world to game bridge"""
    
    def test_create_bridge(self):
        from ..game_bridge import create_bridge
        bridge = create_bridge()
        assert bridge is not None
    
    def test_auto_map(self):
        from ..game_bridge import create_bridge
        from ..models import Slot
        
        bridge = create_bridge()
        slot = Slot(slot_id="s1", name="budget_total", value=1000)
        
        mapping = bridge.auto_map(slot)
        
        assert mapping is not None
        assert mapping.mechanic_type.value == "points"
    
    def test_transform_state(self):
        from ..game_bridge import create_bridge
        from ..world_engine import create_engine
        
        engine = create_engine()
        state = engine.create_state({
            "budget": 1000,
            "health": 80,
            "risk": 0.3,
        })
        
        bridge = create_bridge()
        game_state = bridge.transform_state(state)
        
        assert "mechanics" in game_state
    
    def test_fog_of_war(self):
        from ..game_bridge import create_bridge
        from ..models import Slot
        
        bridge = create_bridge()
        slot = Slot(slot_id="s1", name="hidden_value", value=42)
        
        # High p-value = high fog
        fogged = bridge.apply_fog_of_war(slot, p_value=0.8)
        
        assert fogged["fog_level"] == 0.8
        assert fogged["visible_value"] == "???"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestCoreEnginesIntegration:
    """Integration tests"""
    
    def test_full_causal_pipeline(self):
        """Test complete causal reasoning pipeline"""
        from ..world_engine import create_engine
        from ..causal_decision import create_decision_engine
        from ..causal_inference import create_dag_builder
        from ..game_bridge import create_bridge
        
        # 1. Create WorldEngine state
        world = create_engine()
        state = world.create_state({
            "energy_price": 50,
            "production_cost": 30,
            "sales": 100,
            "profit": 0,
        })
        
        # 2. Build causal DAG
        builder = create_dag_builder()
        dag = (builder
            .new_dag("Business Causality")
            .add_slot("energy_price", 50)
            .add_slot("production_cost", 30)
            .add_slot("sales", 100)
            .add_slot("profit", 0)
            .add_edge("energy_price", "production_cost", 0.7)
            .add_edge("production_cost", "profit", -0.6)
            .add_edge("sales", "profit", 0.9)
            .build())
        
        # 3. Register with decision engine
        decision = create_decision_engine()
        valid, _ = decision.register_dag(dag, "ceo")
        assert valid
        
        # 4. Analyze impact
        scores = decision.analyze_slot_impact(dag.dag_id, "profit")
        levers = decision.get_actionable_levers(dag.dag_id, "profit")
        
        assert len(levers) > 0
        
        # 5. What-if analysis
        what_if = decision.what_if(
            dag.dag_id,
            "energy_price",
            30,  # Reduce energy price
            "profit"
        )
        
        assert "estimated_effect" in what_if
        
        # 6. Generate XR overlay
        overlay = decision.generate_xr_overlay(dag.dag_id, "profit")
        assert overlay["read_only"] == True
        
        # 7. Bridge to game
        bridge = create_bridge()
        game_manifest = bridge.generate_game_manifest(state, dag)
        
        assert "mechanics" in game_manifest
        assert "causal_links" in game_manifest


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
