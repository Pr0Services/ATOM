"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                        CHE·NU™ V75 - SCENARIO LOCK ENGINE                            ║
║                                                                                      ║
║  Verrouillage de scénarios pour tests déterministes et reproductibilité             ║
║  Garantit la cohérence des tests E2E et des Golden Flows                            ║
║                                                                                      ║
║  Version: 75.0 | Status: CANON | License: Proprietary                               ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

from typing import Dict, Any, List, Optional, Callable
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import hashlib
import json
import logging
import copy

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

MODULE_VERSION = "75.0"
MODULE_STATUS = "CANON"
MODULE_NAME = "ScenarioLockEngine"

class LockStatus(str, Enum):
    """Status d'un verrou de scénario"""
    ACTIVE = "active"           # Verrou actif
    RELEASED = "released"       # Verrou libéré
    EXPIRED = "expired"         # Verrou expiré
    FAILED = "failed"           # Échec du scénario

class ScenarioType(str, Enum):
    """Types de scénarios verrouillables"""
    GOLDEN_FLOW = "golden_flow"     # Flow de référence
    E2E_TEST = "e2e_test"           # Test end-to-end
    INTEGRATION = "integration"      # Test d'intégration
    REGRESSION = "regression"        # Test de régression
    DEMO = "demo"                    # Démonstration
    CHECKPOINT = "checkpoint"        # Point de contrôle

class ReplayMode(str, Enum):
    """Modes de replay"""
    EXACT = "exact"             # Replay exact (même timing)
    ACCELERATED = "accelerated" # Replay accéléré
    STEP_BY_STEP = "step_by_step"  # Pas à pas avec validation

# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScenarioStep:
    """Étape d'un scénario"""
    id: str
    name: str
    action: str
    inputs: Dict[str, Any]
    expected_outputs: Dict[str, Any]
    assertions: List[str]
    timeout_ms: int = 5000
    depends_on: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LockedScenario:
    """Scénario verrouillé pour test"""
    id: UUID
    name: str
    type: ScenarioType
    version: str
    steps: List[ScenarioStep]
    initial_state: Dict[str, Any]
    expected_final_state: Dict[str, Any]
    hash: str
    locked_at: datetime
    locked_by: UUID
    status: LockStatus = LockStatus.ACTIVE
    release_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ScenarioExecution:
    """Exécution d'un scénario verrouillé"""
    id: UUID
    scenario_id: UUID
    started_at: datetime
    completed_at: Optional[datetime]
    status: str  # "running", "passed", "failed"
    current_step: int
    step_results: List[Dict[str, Any]]
    execution_mode: ReplayMode
    executor_id: UUID
    errors: List[str] = field(default_factory=list)

@dataclass
class StepResult:
    """Résultat d'une étape"""
    step_id: str
    passed: bool
    actual_outputs: Dict[str, Any]
    assertion_results: Dict[str, bool]
    duration_ms: int
    error: Optional[str] = None

# ═══════════════════════════════════════════════════════════════════════════════
# GOLDEN FLOWS DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

GOLDEN_FLOWS = {
    "GF-1": {
        "name": "Auth → Login → Bureau",
        "description": "Flow d'authentification et accès au bureau",
        "steps": [
            ScenarioStep(
                id="GF1_S1",
                name="Submit Login",
                action="POST /api/auth/login",
                inputs={"email": "test@chenu.app", "password": "***"},
                expected_outputs={"status": 200, "has_token": True},
                assertions=["response.token exists", "response.user.id exists"]
            ),
            ScenarioStep(
                id="GF1_S2",
                name="Get User Profile",
                action="GET /api/users/me",
                inputs={"authorization": "Bearer {token}"},
                expected_outputs={"status": 200},
                assertions=["response.user.email == input.email"],
                depends_on=["GF1_S1"]
            ),
            ScenarioStep(
                id="GF1_S3",
                name="Load Bureau",
                action="GET /api/bureau",
                inputs={"authorization": "Bearer {token}"},
                expected_outputs={"status": 200, "has_spheres": True},
                assertions=["response.spheres.length == 9"],
                depends_on=["GF1_S2"]
            ),
        ]
    },
    "GF-2": {
        "name": "Nova Query → Checkpoint → Execute",
        "description": "Flow de requête Nova avec checkpoint de gouvernance",
        "steps": [
            ScenarioStep(
                id="GF2_S1",
                name="Submit Nova Query",
                action="POST /api/nova/query",
                inputs={"query": "Create a new thread", "context": {}},
                expected_outputs={"status": 423},
                assertions=["response.checkpoint_id exists"]
            ),
            ScenarioStep(
                id="GF2_S2",
                name="Approve Checkpoint",
                action="POST /api/checkpoints/{id}/approve",
                inputs={"checkpoint_id": "{checkpoint_id}", "approved_by": "user"},
                expected_outputs={"status": 200, "approved": True},
                assertions=["response.status == 'approved'"],
                depends_on=["GF2_S1"]
            ),
            ScenarioStep(
                id="GF2_S3",
                name="Execute Approved Action",
                action="POST /api/nova/execute",
                inputs={"checkpoint_id": "{checkpoint_id}"},
                expected_outputs={"status": 200, "executed": True},
                assertions=["response.result exists"],
                depends_on=["GF2_S2"]
            ),
        ]
    },
    "GF-3": {
        "name": "Agent → Action → Audit",
        "description": "Flow d'exécution agent avec audit trail",
        "steps": [
            ScenarioStep(
                id="GF3_S1",
                name="Create Agent Task",
                action="POST /api/agents/{agent_id}/tasks",
                inputs={"agent_id": "test_agent", "task": "analyze_document"},
                expected_outputs={"status": 200, "task_id": "exists"},
                assertions=["response.task_id exists", "response.status == 'pending'"]
            ),
            ScenarioStep(
                id="GF3_S2",
                name="Execute Agent Task",
                action="POST /api/agents/{agent_id}/tasks/{task_id}/execute",
                inputs={"agent_id": "test_agent", "task_id": "{task_id}"},
                expected_outputs={"status": 200},
                assertions=["response.result exists"],
                depends_on=["GF3_S1"]
            ),
            ScenarioStep(
                id="GF3_S3",
                name="Verify Audit Trail",
                action="GET /api/audit/events",
                inputs={"entity_id": "{task_id}", "limit": 10},
                expected_outputs={"status": 200, "has_events": True},
                assertions=[
                    "response.events.length >= 2",
                    "response.events[0].action == 'task.created'",
                    "response.events[1].action == 'task.executed'"
                ],
                depends_on=["GF3_S2"]
            ),
        ]
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO LOCK ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class ScenarioLockEngine:
    """
    Moteur de verrouillage de scénarios pour tests déterministes.
    
    Le Scenario Lock Engine permet de:
    - Verrouiller des séquences d'actions pour reproductibilité
    - Exécuter des Golden Flows de référence
    - Valider les comportements système de manière déterministe
    """
    
    def __init__(self):
        self.locked_scenarios: Dict[UUID, LockedScenario] = {}
        self.executions: Dict[UUID, ScenarioExecution] = {}
        self.golden_flows = GOLDEN_FLOWS
        
        logger.info(
            f"ScenarioLockEngine V{MODULE_VERSION} initialized with "
            f"{len(self.golden_flows)} golden flows"
        )
    
    # ═══════════════════════════════════════════════════════════════════════
    # LOCKING
    # ═══════════════════════════════════════════════════════════════════════
    
    async def lock_scenario(
        self,
        name: str,
        scenario_type: ScenarioType,
        steps: List[ScenarioStep],
        initial_state: Dict[str, Any],
        expected_final_state: Dict[str, Any],
        locked_by: UUID,
        metadata: Optional[Dict[str, Any]] = None
    ) -> LockedScenario:
        """
        Verrouille un scénario pour test déterministe.
        
        Une fois verrouillé, le scénario ne peut pas être modifié
        jusqu'à libération explicite.
        """
        # Calculer hash du scénario
        scenario_data = {
            "name": name,
            "steps": [
                {
                    "id": s.id,
                    "action": s.action,
                    "inputs": s.inputs,
                    "expected_outputs": s.expected_outputs
                }
                for s in steps
            ],
            "initial_state": initial_state,
            "expected_final_state": expected_final_state
        }
        
        hash_value = hashlib.sha256(
            json.dumps(scenario_data, sort_keys=True).encode()
        ).hexdigest()[:16]
        
        scenario = LockedScenario(
            id=uuid4(),
            name=name,
            type=scenario_type,
            version=MODULE_VERSION,
            steps=steps,
            initial_state=initial_state,
            expected_final_state=expected_final_state,
            hash=hash_value,
            locked_at=datetime.utcnow(),
            locked_by=locked_by,
            metadata=metadata or {}
        )
        
        self.locked_scenarios[scenario.id] = scenario
        
        logger.info(
            f"Scenario '{name}' locked with hash {hash_value} by {locked_by}"
        )
        
        return scenario
    
    async def lock_golden_flow(
        self,
        flow_id: str,
        locked_by: UUID
    ) -> LockedScenario:
        """Verrouille un Golden Flow prédéfini."""
        if flow_id not in self.golden_flows:
            raise ValueError(f"Unknown golden flow: {flow_id}")
        
        flow = self.golden_flows[flow_id]
        
        return await self.lock_scenario(
            name=flow["name"],
            scenario_type=ScenarioType.GOLDEN_FLOW,
            steps=flow["steps"],
            initial_state={},
            expected_final_state={},
            locked_by=locked_by,
            metadata={"golden_flow_id": flow_id, "description": flow["description"]}
        )
    
    async def release_lock(
        self,
        scenario_id: UUID,
        released_by: UUID,
        reason: str
    ) -> LockedScenario:
        """
        Libère un verrou de scénario.
        
        Le scénario est marqué comme libéré et ne peut plus être exécuté.
        """
        if scenario_id not in self.locked_scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        scenario = self.locked_scenarios[scenario_id]
        
        if scenario.status != LockStatus.ACTIVE:
            raise ValueError(f"Scenario {scenario_id} is not active")
        
        scenario.status = LockStatus.RELEASED
        scenario.release_reason = reason
        
        logger.info(
            f"Scenario {scenario_id} released by {released_by}. Reason: {reason}"
        )
        
        return scenario
    
    # ═══════════════════════════════════════════════════════════════════════
    # EXECUTION
    # ═══════════════════════════════════════════════════════════════════════
    
    async def start_execution(
        self,
        scenario_id: UUID,
        executor_id: UUID,
        mode: ReplayMode = ReplayMode.ACCELERATED
    ) -> ScenarioExecution:
        """
        Démarre l'exécution d'un scénario verrouillé.
        """
        if scenario_id not in self.locked_scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        scenario = self.locked_scenarios[scenario_id]
        
        if scenario.status != LockStatus.ACTIVE:
            raise ValueError(f"Scenario {scenario_id} is not active")
        
        execution = ScenarioExecution(
            id=uuid4(),
            scenario_id=scenario_id,
            started_at=datetime.utcnow(),
            completed_at=None,
            status="running",
            current_step=0,
            step_results=[],
            execution_mode=mode,
            executor_id=executor_id
        )
        
        self.executions[execution.id] = execution
        
        logger.info(
            f"Execution {execution.id} started for scenario {scenario_id} "
            f"in mode {mode.value}"
        )
        
        return execution
    
    async def execute_step(
        self,
        execution_id: UUID,
        step_executor: Callable[[ScenarioStep, Dict[str, Any]], Dict[str, Any]]
    ) -> StepResult:
        """
        Exécute la prochaine étape du scénario.
        
        Args:
            execution_id: ID de l'exécution
            step_executor: Fonction qui exécute réellement l'étape
            
        Returns:
            StepResult avec le résultat de l'étape
        """
        if execution_id not in self.executions:
            raise ValueError(f"Execution {execution_id} not found")
        
        execution = self.executions[execution_id]
        scenario = self.locked_scenarios[execution.scenario_id]
        
        if execution.status != "running":
            raise ValueError(f"Execution {execution_id} is not running")
        
        if execution.current_step >= len(scenario.steps):
            raise ValueError("No more steps to execute")
        
        step = scenario.steps[execution.current_step]
        
        # Vérifier dépendances
        for dep_id in step.depends_on:
            dep_result = next(
                (r for r in execution.step_results if r.get("step_id") == dep_id),
                None
            )
            if not dep_result or not dep_result.get("passed"):
                return StepResult(
                    step_id=step.id,
                    passed=False,
                    actual_outputs={},
                    assertion_results={},
                    duration_ms=0,
                    error=f"Dependency {dep_id} not satisfied"
                )
        
        # Exécuter l'étape
        start_time = datetime.utcnow()
        
        try:
            # Préparer inputs avec substitutions
            resolved_inputs = self._resolve_inputs(
                step.inputs, 
                execution.step_results
            )
            
            # Appeler l'exécuteur
            actual_outputs = await step_executor(step, resolved_inputs)
            
            duration_ms = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            )
            
            # Valider assertions
            assertion_results = self._validate_assertions(
                step.assertions,
                step.expected_outputs,
                actual_outputs
            )
            
            passed = all(assertion_results.values())
            
            result = StepResult(
                step_id=step.id,
                passed=passed,
                actual_outputs=actual_outputs,
                assertion_results=assertion_results,
                duration_ms=duration_ms
            )
            
        except Exception as e:
            duration_ms = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            )
            
            result = StepResult(
                step_id=step.id,
                passed=False,
                actual_outputs={},
                assertion_results={},
                duration_ms=duration_ms,
                error=str(e)
            )
            
            execution.errors.append(str(e))
        
        # Mettre à jour l'exécution
        execution.step_results.append({
            "step_id": result.step_id,
            "passed": result.passed,
            "duration_ms": result.duration_ms,
            "error": result.error
        })
        
        execution.current_step += 1
        
        # Vérifier si terminé
        if execution.current_step >= len(scenario.steps):
            execution.status = "passed" if all(
                r.get("passed") for r in execution.step_results
            ) else "failed"
            execution.completed_at = datetime.utcnow()
        
        logger.info(
            f"Step {step.id} executed: passed={result.passed}, "
            f"duration={result.duration_ms}ms"
        )
        
        return result
    
    def _resolve_inputs(
        self,
        inputs: Dict[str, Any],
        previous_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Résout les références dans les inputs."""
        resolved = {}
        
        for key, value in inputs.items():
            if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                # Référence à un résultat précédent
                ref = value[1:-1]
                for result in previous_results:
                    if ref in str(result.get("actual_outputs", {})):
                        resolved[key] = result["actual_outputs"].get(ref, value)
                        break
                else:
                    resolved[key] = value
            else:
                resolved[key] = value
        
        return resolved
    
    def _validate_assertions(
        self,
        assertions: List[str],
        expected: Dict[str, Any],
        actual: Dict[str, Any]
    ) -> Dict[str, bool]:
        """Valide les assertions d'une étape."""
        results = {}
        
        for assertion in assertions:
            # Validation simplifiée - en production utiliserait un parser
            if "exists" in assertion:
                field = assertion.split(" ")[0].replace("response.", "")
                results[assertion] = field in actual
            elif "==" in assertion:
                parts = assertion.split("==")
                left = parts[0].strip().replace("response.", "")
                right = parts[1].strip()
                results[assertion] = str(actual.get(left)) == right
            elif ">=" in assertion:
                parts = assertion.split(">=")
                left = parts[0].strip().replace("response.", "")
                right = int(parts[1].strip())
                results[assertion] = actual.get(left, 0) >= right
            else:
                results[assertion] = True  # Par défaut
        
        # Vérifier expected outputs
        for key, value in expected.items():
            assertion = f"expected.{key}"
            if key == "status":
                results[assertion] = actual.get("status") == value
            elif key == "has_token":
                results[assertion] = "token" in actual
            elif key == "has_spheres":
                results[assertion] = "spheres" in actual
            elif key == "has_events":
                results[assertion] = "events" in actual and len(actual["events"]) > 0
            else:
                results[assertion] = actual.get(key) == value
        
        return results
    
    # ═══════════════════════════════════════════════════════════════════════
    # QUERIES
    # ═══════════════════════════════════════════════════════════════════════
    
    async def get_scenario(
        self,
        scenario_id: UUID
    ) -> Optional[LockedScenario]:
        """Récupère un scénario par ID."""
        return self.locked_scenarios.get(scenario_id)
    
    async def get_execution(
        self,
        execution_id: UUID
    ) -> Optional[ScenarioExecution]:
        """Récupère une exécution par ID."""
        return self.executions.get(execution_id)
    
    async def list_active_scenarios(self) -> List[LockedScenario]:
        """Liste les scénarios actifs."""
        return [
            s for s in self.locked_scenarios.values()
            if s.status == LockStatus.ACTIVE
        ]
    
    async def list_golden_flows(self) -> Dict[str, Dict[str, Any]]:
        """Liste les Golden Flows disponibles."""
        return {
            flow_id: {
                "name": flow["name"],
                "description": flow["description"],
                "steps_count": len(flow["steps"])
            }
            for flow_id, flow in self.golden_flows.items()
        }
    
    async def get_execution_report(
        self,
        execution_id: UUID
    ) -> Dict[str, Any]:
        """Génère un rapport d'exécution."""
        execution = self.executions.get(execution_id)
        if not execution:
            return {"error": "Execution not found"}
        
        scenario = self.locked_scenarios.get(execution.scenario_id)
        
        total_duration = sum(
            r.get("duration_ms", 0) for r in execution.step_results
        )
        
        passed_steps = sum(
            1 for r in execution.step_results if r.get("passed")
        )
        
        return {
            "execution_id": str(execution.id),
            "scenario_name": scenario.name if scenario else "Unknown",
            "scenario_hash": scenario.hash if scenario else None,
            "status": execution.status,
            "mode": execution.execution_mode.value,
            "started_at": execution.started_at.isoformat(),
            "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
            "total_duration_ms": total_duration,
            "steps": {
                "total": len(scenario.steps) if scenario else 0,
                "executed": execution.current_step,
                "passed": passed_steps,
                "failed": execution.current_step - passed_steps
            },
            "errors": execution.errors,
            "step_details": execution.step_results
        }


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    'ScenarioLockEngine',
    'LockStatus',
    'ScenarioType',
    'ReplayMode',
    'ScenarioStep',
    'LockedScenario',
    'ScenarioExecution',
    'StepResult',
    'GOLDEN_FLOWS',
    'MODULE_VERSION',
]
