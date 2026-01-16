"""
============================================================================
CHE·NU™ V69 — WORLDENGINE TESTS
============================================================================
Version: 1.0.0
Purpose: Test WorldEngine simulation orchestration
============================================================================
"""

import pytest
from datetime import datetime, timedelta

from ..core.models import (
    Slot,
    WorldState,
    CausalRule,
    Scenario,
    Simulation,
    SimulationArtifact,
    SimulationConfig,
    SimulationStatus,
    ScenarioType,
    TimeUnit,
)
from ..core.engine import WorldEngine, RuleExecutor, create_simple_simulation
from ..scenarios.manager import ScenarioManager, WhatIfAnalyzer
from ..workers.manager import Worker, WorkerPool, WorkerManager
from ..temporal.iterator import (
    TemporalIterator,
    TemporalRange,
    LongTermProjector,
    convert_time_units,
)


# ============================================================================
# SLOT TESTS
# ============================================================================

class TestSlot:
    """Test Slot model"""
    
    def test_create_slot(self):
        slot = Slot(name="Budget", value=1000000, unit="USD")
        
        assert slot.name == "Budget"
        assert slot.value == 1000000
        assert slot.unit == "USD"
    
    def test_slot_delta(self):
        slot = Slot(name="Budget", value=1000000, previous_value=900000)
        
        assert slot.delta == 100000
    
    def test_slot_clamp(self):
        slot = Slot(
            name="Risk",
            value=1.5,
            min_value=0,
            max_value=1,
        )
        
        clamped = slot.clamp()
        assert clamped.value == 1.0
    
    def test_slot_advance(self):
        slot = Slot(name="Budget", value=1000000, tick=0)
        
        advanced = slot.advance(1100000, 1)
        
        assert advanced.value == 1100000
        assert advanced.previous_value == 1000000
        assert advanced.tick == 1


# ============================================================================
# WORLD STATE TESTS
# ============================================================================

class TestWorldState:
    """Test WorldState model"""
    
    def test_create_state(self):
        state = WorldState(
            simulation_id="sim-001",
            tick=0,
            slots={
                "Budget": Slot(name="Budget", value=1000000),
                "Risk": Slot(name="Risk", value=0.1),
            },
        )
        
        assert state.tick == 0
        assert len(state.slots) == 2
    
    def test_state_hash(self):
        state = WorldState(
            simulation_id="sim-001",
            tick=0,
            slots={"Budget": Slot(name="Budget", value=1000000)},
        )
        
        # Hash should be deterministic
        hash1 = state.state_hash
        hash2 = state.state_hash
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256
    
    def test_get_value(self):
        state = WorldState(
            simulation_id="sim-001",
            slots={"Budget": Slot(name="Budget", value=1000000)},
        )
        
        assert state.get_value("Budget") == 1000000
        assert state.get_value("Unknown", default=0) == 0
    
    def test_set_slot(self):
        state = WorldState(
            simulation_id="sim-001",
            slots={"Budget": Slot(name="Budget", value=1000000)},
        )
        
        new_slot = Slot(name="Risk", value=0.15)
        new_state = state.set_slot("Risk", new_slot)
        
        assert "Risk" in new_state.slots
        assert new_state.get_value("Risk") == 0.15


# ============================================================================
# WORLDENGINE TESTS
# ============================================================================

class TestWorldEngine:
    """Test WorldEngine core"""
    
    @pytest.fixture
    def engine(self):
        return WorldEngine()
    
    def test_create_simulation(self, engine):
        sim = engine.create_simulation("Test Simulation")
        
        assert sim is not None
        assert sim.name == "Test Simulation"
        assert sim.status == SimulationStatus.DRAFT
    
    def test_add_scenario(self, engine):
        sim = engine.create_simulation("Test")
        
        scenario = engine.add_scenario(
            sim.simulation_id,
            "Baseline",
            {"Budget": 1000000},
            scenario_type=ScenarioType.BASELINE,
        )
        
        assert scenario is not None
        assert scenario.name == "Baseline"
        assert sim.baseline_scenario_id == scenario.scenario_id
    
    def test_add_rule(self, engine):
        sim = engine.create_simulation("Test")
        
        rule = engine.add_rule(
            sim.simulation_id,
            name="Production",
            target_slot="Production",
            source_slots=["Budget", "Efficiency"],
        )
        
        assert rule is not None
        assert rule.name == "Production"
    
    def test_run_simulation(self, engine):
        sim = engine.create_simulation("Test")
        
        engine.add_scenario(
            sim.simulation_id,
            "Baseline",
            {"Budget": 1000000, "Efficiency": 0.85},
            scenario_type=ScenarioType.BASELINE,
            t_end=10,
        )
        
        results = engine.run_simulation(sim.simulation_id)
        
        assert len(results) == 1
        artifact = list(results.values())[0]
        assert artifact.total_ticks == 11  # 0 to 10 inclusive
        assert artifact.chain_valid


# ============================================================================
# RULE EXECUTOR TESTS
# ============================================================================

class TestRuleExecutor:
    """Test RuleExecutor"""
    
    def test_execute_simple_rule(self):
        executor = RuleExecutor()
        
        # Register custom function
        executor.register_rule_function(
            "prod_rule",
            lambda vals: vals["Budget"] * vals["Efficiency"],
        )
        
        rule = CausalRule(
            rule_id="prod_rule",
            name="Production",
            target_slot="Production",
            source_slots=["Budget", "Efficiency"],
        )
        
        state = WorldState(
            simulation_id="test",
            slots={
                "Budget": Slot(name="Budget", value=1000000),
                "Efficiency": Slot(name="Efficiency", value=0.85),
            },
        )
        
        result_slot = executor.execute_rule(rule, state)
        
        assert result_slot is not None
        assert result_slot.value == 850000


# ============================================================================
# SCENARIO MANAGER TESTS
# ============================================================================

class TestScenarioManager:
    """Test ScenarioManager"""
    
    @pytest.fixture
    def setup(self):
        engine = WorldEngine()
        sim = engine.create_simulation("Test")
        
        baseline = engine.add_scenario(
            sim.simulation_id,
            "Baseline",
            {"Budget": 1000000, "Risk": 0.1},
            scenario_type=ScenarioType.BASELINE,
        )
        
        return engine, sim, baseline
    
    def test_clone_scenario(self, setup):
        engine, sim, baseline = setup
        manager = ScenarioManager(sim)
        
        cloned = manager.clone_scenario(
            baseline,
            name="Cloned",
            modifications={"Budget": 1500000},
        )
        
        assert cloned.name == "Cloned"
        assert cloned.initial_values["Budget"] == 1500000
        assert cloned.initial_values["Risk"] == 0.1  # Unchanged
    
    def test_sensitivity_variants(self, setup):
        engine, sim, baseline = setup
        manager = ScenarioManager(sim)
        
        variants = manager.create_sensitivity_variants(
            baseline,
            "Budget",
            [0.8, 1.2],
        )
        
        assert len(variants) == 2


# ============================================================================
# TEMPORAL TESTS
# ============================================================================

class TestTemporalIterator:
    """Test TemporalIterator"""
    
    def test_basic_iteration(self):
        iterator = TemporalIterator(
            t_start=0,
            t_end=10,
            time_unit=TimeUnit.DAY,
        )
        
        ticks = list(iterator)
        
        assert len(ticks) == 11  # 0 to 10
        assert ticks[0][0] == 0  # First tick
        assert ticks[-1][0] == 10  # Last tick
    
    def test_date_calculation(self):
        start_date = datetime(2024, 1, 1)
        iterator = TemporalIterator(
            t_start=0,
            t_end=365,
            time_unit=TimeUnit.DAY,
            start_date=start_date,
        )
        
        ticks = list(iterator)
        
        # Last tick should be ~365 days later
        _, _, last_date = ticks[-1]
        assert last_date.year == 2024
        assert last_date.month == 12
    
    def test_progress(self):
        iterator = TemporalIterator(t_start=0, t_end=100)
        
        for tick, _, _ in iterator:
            if tick == 50:
                assert iterator.progress == 0.5
                break


class TestTemporalRange:
    """Test TemporalRange"""
    
    def test_duration(self):
        range_ = TemporalRange(t_start=0, t_end=365, time_unit=TimeUnit.DAY)
        
        assert range_.duration == 365
        assert range_.duration_years == pytest.approx(1.0, rel=0.01)
    
    def test_contains(self):
        range_ = TemporalRange(t_start=10, t_end=20)
        
        assert range_.contains(15)
        assert not range_.contains(5)
    
    def test_split(self):
        range_ = TemporalRange(t_start=0, t_end=99)
        
        chunks = range_.split(25)
        
        assert len(chunks) == 4


class TestLongTermProjector:
    """Test LongTermProjector"""
    
    def test_50_year_projection(self):
        projector = LongTermProjector(
            base_time_unit=TimeUnit.MONTH,
            projection_years=50,
        )
        
        assert projector.total_ticks == 600  # 50 * 12
    
    def test_checkpoints(self):
        projector = LongTermProjector(
            base_time_unit=TimeUnit.MONTH,
            projection_years=50,
        )
        
        checkpoints = projector.create_checkpoints(checkpoint_interval_years=5)
        
        assert len(checkpoints) == 10  # Every 5 years


# ============================================================================
# TIME CONVERSION TESTS
# ============================================================================

class TestTimeConversion:
    """Test time unit conversion"""
    
    def test_days_to_years(self):
        days = 365
        years = convert_time_units(days, TimeUnit.DAY, TimeUnit.YEAR)
        
        assert years == pytest.approx(1.0, rel=0.01)
    
    def test_months_to_days(self):
        months = 12
        days = convert_time_units(months, TimeUnit.MONTH, TimeUnit.DAY)
        
        assert days == 360  # 12 * 30


# ============================================================================
# WORKER TESTS
# ============================================================================

class TestWorker:
    """Test Worker"""
    
    def test_worker_execution(self):
        from ..core.models import WorkerTask
        
        worker = Worker()
        
        task = WorkerTask(
            simulation_id="sim-001",
            scenario_id="scen-001",
        )
        
        # Simple executor
        def executor(t):
            return SimulationArtifact(
                simulation_id=t.simulation_id,
                scenario_id=t.scenario_id,
            )
        
        result = worker.execute(task, executor)
        
        assert result is not None
        assert task.status.value == "completed"


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_full_workflow(self):
        """Test complete simulation workflow"""
        engine = WorldEngine()
        
        # 1. Create simulation
        sim = engine.create_simulation("Enterprise Budget Forecast")
        
        # 2. Add baseline scenario
        baseline = engine.add_scenario(
            sim.simulation_id,
            "Baseline",
            {
                "Budget": 1000000,
                "Efficiency": 0.85,
                "Risk": 0.1,
            },
            scenario_type=ScenarioType.BASELINE,
            t_end=50,
            seed=42,
        )
        
        # 3. Add alternative scenario
        aggressive = engine.add_scenario(
            sim.simulation_id,
            "Aggressive",
            {
                "Budget": 1500000,
                "Efficiency": 0.75,
                "Risk": 0.2,
            },
            scenario_type=ScenarioType.ALTERNATIVE,
            t_end=50,
            seed=42,
        )
        
        # 4. Add rule
        engine.add_rule(
            sim.simulation_id,
            name="Production",
            target_slot="Production",
            source_slots=["Budget", "Efficiency"],
            rule_function=lambda vals: vals["Budget"] * vals["Efficiency"],
        )
        
        # 5. Run simulation
        results = engine.run_simulation(sim.simulation_id)
        
        # 6. Verify results
        assert len(results) == 2
        
        for scenario_id, artifact in results.items():
            assert artifact.chain_valid
            assert artifact.total_ticks == 51  # 0 to 50
        
        # 7. Check scenario manager
        manager = ScenarioManager(sim)
        
        baseline_artifact = results[baseline.scenario_id]
        aggressive_artifact = results[aggressive.scenario_id]
        
        comparison = manager.compare_artifacts(
            baseline_artifact,
            aggressive_artifact,
        )
        
        assert comparison.total_divergence > 0
    
    def test_helper_function(self):
        """Test create_simple_simulation helper"""
        engine, sim, scenario = create_simple_simulation(
            name="Quick Test",
            initial_values={"X": 100, "Y": 200},
            rules=[
                {
                    "name": "Sum",
                    "target": "Z",
                    "sources": ["X", "Y"],
                    "function": lambda vals: vals["X"] + vals["Y"],
                },
            ],
            t_end=10,
        )
        
        results = engine.run_simulation(sim.simulation_id)
        
        assert len(results) == 1


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
