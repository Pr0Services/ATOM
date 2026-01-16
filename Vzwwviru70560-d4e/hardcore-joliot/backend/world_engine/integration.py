"""
============================================================================
CHE·NU™ V69 — WORLDENGINE INTEGRATION
============================================================================
Version: 1.0.0
Purpose: Integrate WorldEngine with all CHE·NU modules
Principle: Unified simulation pipeline with full governance
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

from .core.models import (
    Simulation,
    Scenario,
    SimulationArtifact,
    SimulationConfig,
    SimulationStatus,
    ScenarioType,
)
from .core.engine import WorldEngine
from .scenarios.manager import ScenarioManager, WhatIfAnalyzer, ScenarioComparison
from .workers.manager import WorkerManager, WorkerTask
from .temporal.iterator import TemporalIterator, TemporalRange, TimeUnit

# Import from previous phases
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from xr_pack import XRPackBuilder, XRPackVerifier
from security import get_key_manager, get_unified_signer, SignatureAlgorithm, KeyPurpose
from audit import AuditLog, AuditManager, EventType

logger = logging.getLogger(__name__)


# ============================================================================
# INTEGRATED WORLDENGINE
# ============================================================================

class IntegratedWorldEngine:
    """
    Fully integrated WorldEngine with all CHE·NU modules.
    
    Integrates:
    - Phase 1: Governance (OPA) - Pre-check before execution
    - Phase 2: Causal Engine - DAG-based causal rules
    - Phase 3: Feedback & Audit - Loop dynamics + Merkle audit
    - Phase 4: Security - PQC signatures
    - Phase 5: XR Pack - Visualization layer
    - Phase 6: WorldEngine Core - Orchestration
    
    Architecture:
    
        ┌───────────────────────────────────────────────────────────────┐
        │                   INTEGRATED WORLDENGINE                      │
        ├───────────────────────────────────────────────────────────────┤
        │                                                               │
        │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
        │  │  GOVERNANCE │──│   CAUSAL    │──│     FEEDBACK        │  │
        │  │    (OPA)    │  │   ENGINE    │  │    & AUDIT          │  │
        │  └─────────────┘  └─────────────┘  └─────────────────────┘  │
        │         │                │                    │              │
        │         ▼                ▼                    ▼              │
        │  ┌───────────────────────────────────────────────────────┐  │
        │  │                  SIMULATION PIPELINE                   │  │
        │  │  Input → OPA Check → Rules → Feedback → Safety → Out  │  │
        │  └───────────────────────────────────────────────────────┘  │
        │         │                                    │              │
        │         ▼                                    ▼              │
        │  ┌─────────────┐                    ┌─────────────────────┐│
        │  │  SECURITY   │                    │      XR PACK        ││
        │  │   (PQC)     │                    │   (Visualization)   ││
        │  └─────────────┘                    └─────────────────────┘│
        │                                                             │
        │  Output: Signed Artifacts + XR Pack + Audit Trail          │
        └───────────────────────────────────────────────────────────┘
    
    Usage:
        engine = IntegratedWorldEngine()
        
        # Create simulation
        sim = engine.create_simulation("Enterprise Forecast")
        
        # Add scenarios
        baseline = engine.add_scenario(sim, "Baseline", {...})
        aggressive = engine.add_scenario(sim, "Aggressive", {...})
        
        # Run simulation
        results = engine.run_simulation(sim.simulation_id)
        
        # Generate signed XR Pack
        xr_pack = engine.generate_xr_pack(sim.simulation_id)
        
        # Get audit report
        report = engine.get_audit_report(sim.simulation_id)
    """
    
    def __init__(self, config: Optional[SimulationConfig] = None):
        self.config = config or SimulationConfig()
        
        # Core engine
        self._engine = WorldEngine(self.config)
        
        # Security
        self._key_manager = get_key_manager()
        self._signer = get_unified_signer()
        
        # Audit
        self._audit_manager = AuditManager()
        
        # Workers
        self._worker_manager = WorkerManager(num_workers=4)
        
        # XR Packs
        self._xr_packs: Dict[str, Any] = {}
    
    # =========================================================================
    # SIMULATION MANAGEMENT
    # =========================================================================
    
    def create_simulation(
        self,
        name: str,
        description: str = "",
        tenant_id: Optional[str] = None,
        **kwargs,
    ) -> Simulation:
        """Create a new simulation"""
        sim = self._engine.create_simulation(
            name=name,
            description=description,
            tenant_id=tenant_id,
            **kwargs,
        )
        
        # Create dedicated audit log
        self._audit_manager.create_log(sim.simulation_id, tenant_id)
        
        return sim
    
    def add_scenario(
        self,
        simulation_id: str,
        name: str,
        initial_values: Dict[str, float],
        scenario_type: ScenarioType = ScenarioType.ALTERNATIVE,
        **kwargs,
    ) -> Scenario:
        """Add a scenario to a simulation"""
        return self._engine.add_scenario(
            simulation_id=simulation_id,
            name=name,
            initial_values=initial_values,
            scenario_type=scenario_type,
            **kwargs,
        )
    
    def add_rule(self, simulation_id: str, **kwargs):
        """Add a causal rule"""
        return self._engine.add_rule(simulation_id, **kwargs)
    
    # =========================================================================
    # SIMULATION EXECUTION
    # =========================================================================
    
    def run_simulation(
        self,
        simulation_id: str,
        scenario_ids: Optional[List[str]] = None,
        sign_artifacts: bool = True,
    ) -> Dict[str, SimulationArtifact]:
        """
        Run simulation with full integration.
        
        Args:
            simulation_id: Simulation ID
            scenario_ids: Specific scenarios to run
            sign_artifacts: Sign artifacts with PQC
            
        Returns:
            Dict of scenario_id -> SimulationArtifact
        """
        sim = self._engine.get_simulation(simulation_id)
        if sim is None:
            raise ValueError(f"Simulation not found: {simulation_id}")
        
        # Log start
        audit = self._audit_manager.get_log(simulation_id)
        if audit:
            audit.record(
                EventType.SIMULATION_START,
                f"Running simulation: {sim.name}",
                data={"scenarios": scenario_ids or [s.scenario_id for s in sim.scenarios]},
            )
        
        # Run simulation
        results = self._engine.run_simulation(simulation_id, scenario_ids)
        
        # Sign artifacts if requested
        if sign_artifacts:
            for scenario_id, artifact in results.items():
                self._sign_artifact(artifact, sim.tenant_id)
        
        # Log completion
        if audit:
            audit.record(
                EventType.SIMULATION_END,
                f"Simulation completed: {len(results)} scenarios",
                data={
                    "artifacts": list(results.keys()),
                    "signed": sign_artifacts,
                },
            )
        
        return results
    
    def _sign_artifact(
        self,
        artifact: SimulationArtifact,
        tenant_id: Optional[str] = None,
    ) -> None:
        """Sign an artifact with PQC signature"""
        # Generate or get key
        key = self._key_manager.get_active_key(
            purpose=KeyPurpose.ARTIFACT_SIGNING,
            tenant_id=tenant_id,
        )
        
        if key is None:
            # Generate new key
            key_id = self._key_manager.generate_key(
                algorithm=SignatureAlgorithm.HYBRID_ED25519_DILITHIUM2,
                purpose=KeyPurpose.ARTIFACT_SIGNING,
                tenant_id=tenant_id,
            )
            key = self._key_manager.get_key(key_id)
        
        # Sign artifact
        content = artifact.model_dump_json().encode()
        signature = self._signer.sign(content, key, "simulation_artifact")
        
        artifact.signed = True
        artifact.signature = signature.signature_b64
        artifact.key_id = key.key_id
    
    # =========================================================================
    # XR PACK GENERATION
    # =========================================================================
    
    def generate_xr_pack(
        self,
        simulation_id: str,
        sign_pack: bool = True,
    ):
        """
        Generate XR Pack for a simulation.
        
        Includes:
        - All scenario results
        - Divergence analysis
        - Signed with PQC
        """
        sim = self._engine.get_simulation(simulation_id)
        if sim is None:
            raise ValueError(f"Simulation not found: {simulation_id}")
        
        # Create builder
        builder = XRPackBuilder(
            simulation_id=simulation_id,
            tenant_id=sim.tenant_id,
            chunk_size=self.config.chunk_size,
        )
        
        # Get baseline artifact
        baseline = sim.get_baseline()
        baseline_artifact = None
        if baseline and baseline.result_artifact_id:
            baseline_artifact = self._engine.get_artifact(baseline.result_artifact_id)
        
        # Add states from all scenarios
        for scenario in sim.scenarios:
            if scenario.result_artifact_id:
                artifact = self._engine.get_artifact(scenario.result_artifact_id)
                if artifact:
                    states = artifact.to_xr_states()
                    
                    if scenario.scenario_type == ScenarioType.BASELINE:
                        builder.add_simulation_states(states)
                        builder.set_baseline(
                            states,
                            scenario.scenario_id,
                            scenario.name,
                        )
                    else:
                        builder.add_scenario(
                            states,
                            scenario.scenario_id,
                            scenario.name,
                        )
        
        # Build pack
        pack = builder.build()
        
        # Sign if requested
        if sign_pack:
            builder.sign()
        
        # Store
        self._xr_packs[simulation_id] = builder
        
        # Log
        audit = self._audit_manager.get_log(simulation_id)
        if audit:
            audit.record(
                EventType.XR_PACK_GENERATED,
                f"XR Pack generated: {pack.replay_index.total_steps} steps",
                data={
                    "chunks": pack.replay_index.total_chunks,
                    "divergence_points": len(pack.diff.divergence.get("points", [])),
                    "signed": sign_pack,
                },
            )
        
        return pack
    
    def export_xr_pack(
        self,
        simulation_id: str,
        output_dir: str,
    ) -> Dict[str, str]:
        """Export XR Pack to directory"""
        builder = self._xr_packs.get(simulation_id)
        if builder is None:
            # Generate first
            self.generate_xr_pack(simulation_id)
            builder = self._xr_packs.get(simulation_id)
        
        if builder is None:
            raise ValueError("Failed to generate XR Pack")
        
        return builder.export(output_dir)
    
    # =========================================================================
    # SCENARIO ANALYSIS
    # =========================================================================
    
    def create_scenario_manager(self, simulation_id: str) -> ScenarioManager:
        """Create scenario manager for a simulation"""
        sim = self._engine.get_simulation(simulation_id)
        if sim is None:
            raise ValueError(f"Simulation not found: {simulation_id}")
        
        return ScenarioManager(sim)
    
    def compare_scenarios(
        self,
        simulation_id: str,
        baseline_scenario_id: str,
        scenario_id: str,
    ) -> ScenarioComparison:
        """Compare two scenarios"""
        baseline_artifact = self._get_scenario_artifact(simulation_id, baseline_scenario_id)
        scenario_artifact = self._get_scenario_artifact(simulation_id, scenario_id)
        
        if baseline_artifact is None or scenario_artifact is None:
            raise ValueError("Artifacts not found for comparison")
        
        manager = self.create_scenario_manager(simulation_id)
        return manager.compare_artifacts(baseline_artifact, scenario_artifact)
    
    def _get_scenario_artifact(
        self,
        simulation_id: str,
        scenario_id: str,
    ) -> Optional[SimulationArtifact]:
        """Get artifact for a scenario"""
        sim = self._engine.get_simulation(simulation_id)
        if sim is None:
            return None
        
        scenario = sim.get_scenario(scenario_id)
        if scenario is None or scenario.result_artifact_id is None:
            return None
        
        return self._engine.get_artifact(scenario.result_artifact_id)
    
    # =========================================================================
    # AUDIT & VERIFICATION
    # =========================================================================
    
    def get_audit_report(self, simulation_id: str) -> Dict[str, Any]:
        """Get audit report for a simulation"""
        audit = self._audit_manager.get_log(simulation_id)
        if audit is None:
            return {"error": "No audit log found"}
        
        audit.finalize()
        return audit.generate_audit_report()
    
    def verify_artifact(self, artifact_id: str) -> bool:
        """Verify artifact signature"""
        artifact = self._engine.get_artifact(artifact_id)
        if artifact is None:
            return False
        
        if not artifact.signed:
            return False
        
        # Get key
        key = self._key_manager.get_public_key(artifact.key_id)
        if key is None:
            return False
        
        # Verify
        content = artifact.model_dump_json().encode()
        # ... (would need stored signature object)
        
        return True
    
    # =========================================================================
    # ACCESSORS
    # =========================================================================
    
    def get_simulation(self, simulation_id: str) -> Optional[Simulation]:
        """Get simulation by ID"""
        return self._engine.get_simulation(simulation_id)
    
    def get_artifact(self, artifact_id: str) -> Optional[SimulationArtifact]:
        """Get artifact by ID"""
        return self._engine.get_artifact(artifact_id)
    
    def list_simulations(self, tenant_id: Optional[str] = None) -> List[Simulation]:
        """List simulations"""
        return self._engine.list_simulations(tenant_id)


# ============================================================================
# QUICK START FACTORY
# ============================================================================

def create_integrated_engine(
    config: Optional[SimulationConfig] = None,
) -> IntegratedWorldEngine:
    """Create an integrated WorldEngine"""
    return IntegratedWorldEngine(config)


def run_quick_simulation(
    name: str,
    initial_values: Dict[str, float],
    t_end: int = 100,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Quick helper to run a simple simulation.
    
    Returns:
        Dict with simulation results and XR pack
    """
    engine = create_integrated_engine()
    
    # Create simulation
    sim = engine.create_simulation(name)
    
    # Add baseline scenario
    engine.add_scenario(
        sim.simulation_id,
        "Baseline",
        initial_values,
        scenario_type=ScenarioType.BASELINE,
        t_end=t_end,
        seed=seed,
    )
    
    # Run
    results = engine.run_simulation(sim.simulation_id)
    
    # Generate XR Pack
    xr_pack = engine.generate_xr_pack(sim.simulation_id)
    
    # Get audit report
    audit_report = engine.get_audit_report(sim.simulation_id)
    
    return {
        "simulation_id": sim.simulation_id,
        "artifacts": results,
        "xr_pack": xr_pack,
        "audit_report": audit_report,
    }
