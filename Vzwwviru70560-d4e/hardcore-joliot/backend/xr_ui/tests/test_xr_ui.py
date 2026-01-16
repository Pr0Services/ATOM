"""
============================================================================
CHE·NU™ V69 — XR/UI MODULE TESTS
============================================================================
"""

import pytest
from datetime import datetime


# ============================================================================
# TIMELINE TESTS
# ============================================================================

class TestTimelineDivergence:
    """Test timeline divergence visualization"""
    
    def test_create_visualization(self):
        from ..timeline import create_timeline_visualization
        viz = create_timeline_visualization()
        assert viz is not None
    
    def test_add_timeline(self):
        from ..timeline import create_timeline_visualization
        
        viz = create_timeline_visualization()
        timeline = viz.add_timeline(
            "scenario-1",
            "Optimistic",
            [{"revenue": 100}, {"revenue": 110}, {"revenue": 125}],
        )
        
        assert timeline.name == "Optimistic"
        assert len(timeline.points) == 3
    
    def test_find_divergences(self):
        from ..timeline import create_timeline_visualization
        
        viz = create_timeline_visualization()
        t1 = viz.add_timeline("s1", "Base", [{"v": 10}, {"v": 20}])
        t2 = viz.add_timeline("s2", "Alt", [{"v": 10}, {"v": 30}])  # Diverge at t=1
        
        divergences = viz.inspect_delta(t1.timeline_id, t2.timeline_id)
        
        assert len(divergences) == 1
        assert divergences[0].time == 1
    
    def test_scrub_time(self):
        from ..timeline import create_timeline_visualization
        
        viz = create_timeline_visualization()
        viz.add_timeline("s1", "Test", [{"a": 1}, {"a": 2}, {"a": 3}])
        
        snapshot = viz.scrub_time(1)
        
        assert snapshot["time"] == 1
        assert "Test" in snapshot["snapshot"]


# ============================================================================
# WORKBENCH TESTS
# ============================================================================

class TestLabWorkbench:
    """Test lab workbench"""
    
    def test_create_workbench(self):
        from ..workbench import create_workbench
        wb = create_workbench()
        assert wb is not None
    
    def test_add_artifact(self):
        from ..workbench import create_workbench
        
        wb = create_workbench()
        artifact = wb.add_artifact("Test", {"value": 100})
        
        assert artifact.name == "Test"
        assert artifact.data["value"] == 100
    
    def test_stress_tester(self):
        from ..workbench import create_workbench
        from ..models import WorkbenchTool
        
        wb = create_workbench()
        a = wb.add_artifact("Data", {"metric": 50})
        
        result = wb.use_tool(
            WorkbenchTool.STRESS_TESTER,
            [a.artifact_id],
            stress_factor=2.0,
        )
        
        assert result is not None
        assert result.output_data["stressed"]["metric"] == 100
    
    def test_chronos(self):
        from ..workbench import create_workbench
        from ..models import WorkbenchTool
        
        wb = create_workbench()
        a = wb.add_artifact("Projection", {"budget": 1000})
        
        result = wb.use_tool(
            WorkbenchTool.CHRONOS,
            [a.artifact_id],
            months=6,
            growth_rate=0.1,
        )
        
        assert len(result.output_data["projections"]) == 6


# ============================================================================
# CAUSAL INTERVENTION TESTS
# ============================================================================

class TestCausalIntervention:
    """Test causal intervention UX"""
    
    def test_create_system(self):
        from ..causal_intervention import create_intervention_system
        sys = create_intervention_system()
        assert sys is not None
    
    def test_create_proxy(self):
        from ..causal_intervention import create_intervention_system
        
        sys = create_intervention_system()
        proxy = sys.proxies.create_proxy("slot-1", "Budget", 1000)
        
        assert proxy.value == 1000
        assert not proxy.is_modified
    
    def test_grab_and_slide(self):
        from ..causal_intervention import create_intervention_system
        
        sys = create_intervention_system()
        proxy = sys.proxies.create_proxy("s1", "Test", 100)
        
        result, wave = sys.grab_and_slide(proxy.proxy_id, 150)
        
        assert result.value == 150
        assert result.is_modified
    
    def test_snapshot(self):
        from ..causal_intervention import create_intervention_system
        
        sys = create_intervention_system()
        proxy = sys.proxies.create_proxy("s1", "Test", 100)
        sys.grab_and_slide(proxy.proxy_id, 200)
        
        drafts = sys.snapshot("approver-1")
        
        assert len(drafts) == 1
        assert drafts[0].opa_approved


# ============================================================================
# CAUSAL TRACE TESTS
# ============================================================================

class TestCausalTrace:
    """Test causal trace visualization"""
    
    def test_create_system(self):
        from ..causal_trace import create_causal_trace_viz
        viz = create_causal_trace_viz()
        assert viz is not None
    
    def test_add_path(self):
        from ..causal_trace import create_causal_trace_viz
        
        viz = create_causal_trace_viz()
        path = viz.add_causal_path("A", "B", strength=0.8, certainty=0.9)
        
        assert path.source_slot == "A"
        assert path.target_slot == "B"
    
    def test_uncertainty_node(self):
        from ..causal_trace import create_causal_trace_viz
        
        viz = create_causal_trace_viz()
        node = viz.add_uncertainty("slot-x", ["data-1", "data-2"])
        
        info = viz.inspect_uncertainty(node.node_id)
        
        assert len(info["missing_slots"]) == 2
    
    def test_do_intervention(self):
        from ..causal_trace import create_causal_trace_viz
        
        viz = create_causal_trace_viz()
        viz.set_world_state({"A": 100, "B": 50})
        
        result = viz.apply_intervention(
            "A", 150,
            propagation={"B": 0.5}
        )
        
        assert result["modified_state"]["A"] == 150
        assert result["modified_state"]["B"] == 75  # 50 + (150-100)*0.5


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestXRUIIntegration:
    """Integration tests"""
    
    def test_full_xr_pipeline(self):
        """Test complete XR workflow"""
        from ..timeline import create_timeline_visualization
        from ..workbench import create_workbench
        from ..causal_intervention import create_intervention_system
        from ..causal_trace import create_causal_trace_viz
        from ..models import WorkbenchTool
        
        # 1. Timeline Divergence
        timeline = create_timeline_visualization()
        t1 = timeline.add_timeline("s1", "Base", [
            {"revenue": 100, "cost": 50},
            {"revenue": 110, "cost": 55},
        ])
        t2 = timeline.add_timeline("s2", "Growth", [
            {"revenue": 100, "cost": 50},
            {"revenue": 130, "cost": 60},
        ])
        
        divergences = timeline.inspect_delta(t1.timeline_id, t2.timeline_id)
        assert len(divergences) > 0
        
        # 2. Lab Workbench
        workbench = create_workbench()
        artifact = workbench.add_artifact("Analysis", {"kpi": 75})
        result = workbench.use_tool(WorkbenchTool.CAUSAL_SPECTROMETER, [artifact.artifact_id])
        assert result is not None
        
        # 3. Causal Intervention
        intervention = create_intervention_system()
        proxy = intervention.proxies.create_proxy("budget", "Budget", 1000)
        intervention.ripple.set_graph({proxy.proxy_id: ["revenue", "cost"]})
        _, wave = intervention.grab_and_slide(proxy.proxy_id, 1200)
        assert len(wave.affected_proxies) == 2
        
        # 4. Causal Trace
        trace = create_causal_trace_viz()
        trace.add_causal_path("budget", "revenue", 0.9, 0.95)
        trace.add_causal_path("budget", "cost", 0.7, 0.85)
        trace.add_uncertainty("profit", ["tax_rate", "exchange_rate"])
        
        trace.set_world_state({"budget": 1000, "revenue": 500, "cost": 300})
        result = trace.apply_intervention("budget", 1200, {"revenue": 0.5, "cost": 0.3})
        
        # 5. All manifests are read-only
        assert timeline.export_xr_manifest()["read_only"] == True
        assert workbench.get_xr_manifest()["read_only"] == True
        assert intervention.get_xr_manifest()["read_only"] == True
        assert trace.get_full_manifest()["read_only"] == True
        
        print()
        print("✅ Full XR/UI pipeline verified!")
        print(f"   Timelines: {len(timeline._timelines)}")
        print(f"   Divergences: {len(divergences)}")
        print(f"   Causal paths: {len(trace.paths.get_all_paths())}")
        print(f"   All read-only: Yes")


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
