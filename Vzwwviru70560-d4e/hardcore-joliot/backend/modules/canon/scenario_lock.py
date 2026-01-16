"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ — SCENARIO LOCK SYSTEM                            ║
║                                                                              ║
║  "We vary factors, not form."                                               ║
║                                                                              ║
║  Scenario templates are fixed "shapes".                                     ║
║  Each run is a unique combination: template × factors × module set.         ║
║                                                                              ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
from typing import List, Dict, Any, Optional
from uuid import uuid4
import json
import logging

from .need_canon import NeedCanon
from .module_catalog import ModuleCatalog, Module

logger = logging.getLogger("chenu.simulation")

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class FactorCategory(str, Enum):
    """Categories of scenario factors."""
    PROFILE = "profile"           # User profile characteristics
    CIRCUMSTANCE = "circumstance" # External circumstances
    TOOL_ACTIVATION = "tool"      # Which tools/modules are active
    CADENCE = "cadence"           # Timing and frequency
    STRESS = "stress"             # Load and pressure levels

class StepType(str, Enum):
    """Types of scenario steps."""
    ACTION = "action"       # User takes an action
    SYSTEM = "system"       # System does something
    CHECKPOINT = "checkpoint"  # Governance checkpoint
    WAIT = "wait"           # Time passes
    DECISION = "decision"   # Decision point

class RunStatus(str, Enum):
    """Status of a simulation run."""
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"

# ═══════════════════════════════════════════════════════════════════════════════
# FACTOR MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Factor:
    """A variable factor in a scenario."""
    id: str
    category: FactorCategory
    label: str
    description: str
    possible_values: List[str]
    default_value: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category.value,
            "label": self.label,
            "description": self.description,
            "possible_values": self.possible_values,
            "default_value": self.default_value,
        }

@dataclass
class FactorLibrary:
    """Library of available factors."""
    factors: Dict[str, Factor] = field(default_factory=dict)
    
    @classmethod
    def default(cls) -> "FactorLibrary":
        """Create default factor library."""
        lib = cls()
        
        # Profile factors
        lib.add(Factor(
            id="profile.experience",
            category=FactorCategory.PROFILE,
            label="User Experience Level",
            description="How experienced is the user with similar tools?",
            possible_values=["novice", "intermediate", "expert"],
            default_value="intermediate",
        ))
        
        lib.add(Factor(
            id="profile.tech_comfort",
            category=FactorCategory.PROFILE,
            label="Tech Comfort Level",
            description="Comfort with technology and AI systems",
            possible_values=["low", "medium", "high"],
            default_value="medium",
        ))
        
        lib.add(Factor(
            id="profile.role",
            category=FactorCategory.PROFILE,
            label="User Role",
            description="Primary role of the user",
            possible_values=["individual", "team_lead", "executive", "freelancer"],
            default_value="individual",
        ))
        
        # Circumstance factors
        lib.add(Factor(
            id="circumstance.urgency",
            category=FactorCategory.CIRCUMSTANCE,
            label="Urgency Level",
            description="How urgent are the user's needs?",
            possible_values=["low", "medium", "high", "critical"],
            default_value="medium",
        ))
        
        lib.add(Factor(
            id="circumstance.complexity",
            category=FactorCategory.CIRCUMSTANCE,
            label="Project Complexity",
            description="Complexity of the user's project/context",
            possible_values=["simple", "moderate", "complex", "chaotic"],
            default_value="moderate",
        ))
        
        lib.add(Factor(
            id="circumstance.external_pressure",
            category=FactorCategory.CIRCUMSTANCE,
            label="External Pressure",
            description="External deadlines, stakeholders, etc.",
            possible_values=["none", "light", "moderate", "heavy"],
            default_value="light",
        ))
        
        # Tool activation factors
        lib.add(Factor(
            id="tool.ai_mode",
            category=FactorCategory.TOOL_ACTIVATION,
            label="AI Mode",
            description="Nova's activation level",
            possible_values=["guided", "balanced", "autonomous"],
            default_value="balanced",
        ))
        
        lib.add(Factor(
            id="tool.governance_level",
            category=FactorCategory.TOOL_ACTIVATION,
            label="Governance Strictness",
            description="How strict is governance?",
            possible_values=["relaxed", "standard", "strict", "paranoid"],
            default_value="standard",
        ))
        
        lib.add(Factor(
            id="tool.xr_enabled",
            category=FactorCategory.TOOL_ACTIVATION,
            label="XR Features",
            description="Are XR/immersive features available?",
            possible_values=["disabled", "view_only", "full"],
            default_value="view_only",
        ))
        
        # Cadence factors
        lib.add(Factor(
            id="cadence.interaction_frequency",
            category=FactorCategory.CADENCE,
            label="Interaction Frequency",
            description="How often does user interact?",
            possible_values=["sporadic", "daily", "multiple_daily", "continuous"],
            default_value="daily",
        ))
        
        lib.add(Factor(
            id="cadence.session_length",
            category=FactorCategory.CADENCE,
            label="Session Length",
            description="Typical session duration",
            possible_values=["micro", "short", "medium", "long"],
            default_value="medium",
        ))
        
        # Stress factors
        lib.add(Factor(
            id="stress.system_load",
            category=FactorCategory.STRESS,
            label="System Load",
            description="System load during simulation",
            possible_values=["light", "normal", "heavy", "overloaded"],
            default_value="normal",
        ))
        
        lib.add(Factor(
            id="stress.error_injection",
            category=FactorCategory.STRESS,
            label="Error Injection Rate",
            description="Rate of simulated errors",
            possible_values=["none", "low", "medium", "high"],
            default_value="low",
        ))
        
        return lib
    
    def add(self, factor: Factor):
        """Add a factor to the library."""
        self.factors[factor.id] = factor
    
    def get(self, factor_id: str) -> Optional[Factor]:
        """Get a factor by ID."""
        return self.factors.get(factor_id)
    
    def all(self) -> List[Factor]:
        """Get all factors."""
        return list(self.factors.values())

# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO STEP
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScenarioStep:
    """A step in a scenario template."""
    id: str
    step_type: StepType
    label: str
    needs: List[str]  # Need IDs from NeedCanon
    modules_required: List[str] = field(default_factory=list)  # Module IDs
    description: Optional[str] = None
    duration_minutes: int = 5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "step_type": self.step_type.value,
            "label": self.label,
            "needs": self.needs,
            "modules_required": self.modules_required,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
        }

@dataclass
class ScenarioPhase:
    """A phase containing multiple steps."""
    id: str
    label: str
    steps: List[ScenarioStep] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "steps": [s.to_dict() for s in self.steps],
        }

# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScenarioTemplate:
    """
    A fixed scenario template (the "shape").
    
    "We vary factors, not form."
    """
    template_id: str
    label: str
    description: str
    duration_days: int
    phases: List[ScenarioPhase] = field(default_factory=list)
    required_factors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "label": self.label,
            "description": self.description,
            "duration_days": self.duration_days,
            "phases": [p.to_dict() for p in self.phases],
            "required_factors": self.required_factors,
        }
    
    def get_all_needs(self) -> List[str]:
        """Get all needs referenced by this template."""
        needs = set()
        for phase in self.phases:
            for step in phase.steps:
                needs.update(step.needs)
        return list(needs)
    
    def get_all_modules(self) -> List[str]:
        """Get all modules required by this template."""
        modules = set()
        for phase in self.phases:
            for step in phase.steps:
                modules.update(step.modules_required)
        return list(modules)

# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO TEMPLATES LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════

class ScenarioTemplates:
    """Pre-defined scenario templates."""
    
    @staticmethod
    def onboarding_30d() -> ScenarioTemplate:
        """30-day onboarding scenario."""
        return ScenarioTemplate(
            template_id="template.onboarding_30d.v1",
            label="Onboarding → First Value → Integration → Habit (30 days)",
            description="New user journey from signup to daily usage habit",
            duration_days=30,
            phases=[
                ScenarioPhase(
                    id="phase.0_signup",
                    label="Signup & Setup",
                    steps=[
                        ScenarioStep("step.register", StepType.ACTION, "Register Account",
                                   needs=["need.trust", "need.safety"], modules_required=["auth.core"]),
                        ScenarioStep("step.identity_bootstrap", StepType.SYSTEM, "Identity Setup",
                                   needs=["need.identity", "need.trust"], modules_required=["identity.boundary"]),
                        ScenarioStep("step.sphere_select", StepType.ACTION, "Select Primary Sphere",
                                   needs=["need.organization", "need.discovery"], modules_required=["spheres.catalog"]),
                        ScenarioStep("step.first_thread", StepType.ACTION, "Create First Thread",
                                   needs=["need.memory", "need.clarity"], modules_required=["threads.v2"]),
                    ]
                ),
                ScenarioPhase(
                    id="phase.1_first_value",
                    label="First Value Delivery",
                    steps=[
                        ScenarioStep("step.nova_first_chat", StepType.ACTION, "First Nova Interaction",
                                   needs=["need.clarity", "need.execution", "need.communication"],
                                   modules_required=["nova.pipeline"]),
                        ScenarioStep("step.checkpoint_first", StepType.CHECKPOINT, "First Governance Checkpoint",
                                   needs=["need.governance", "need.trust"],
                                   modules_required=["governance.checkpoints"]),
                        ScenarioStep("step.decision_point_first", StepType.DECISION, "First Decision Point",
                                   needs=["need.clarity", "need.governance"],
                                   modules_required=["governance.decisions"]),
                    ]
                ),
                ScenarioPhase(
                    id="phase.2_integration",
                    label="Tool Integration",
                    steps=[
                        ScenarioStep("step.explore_spheres", StepType.ACTION, "Explore Multiple Spheres",
                                   needs=["need.discovery", "need.organization"], modules_required=["spheres.catalog"]),
                        ScenarioStep("step.browse_agents", StepType.ACTION, "Browse Agent Marketplace",
                                   needs=["need.discovery", "need.execution"], modules_required=["agents.marketplace"]),
                        ScenarioStep("step.hire_first_agent", StepType.ACTION, "Hire First Agent",
                                   needs=["need.execution", "need.governance"], modules_required=["agents.hire"]),
                    ]
                ),
                ScenarioPhase(
                    id="phase.3_habit",
                    label="Daily Habit Formation",
                    steps=[
                        ScenarioStep("step.daily_check", StepType.ACTION, "Daily Dashboard Check",
                                   needs=["need.clarity", "need.organization"], modules_required=["spheres.catalog"]),
                        ScenarioStep("step.aging_review", StepType.DECISION, "Review Aging Decisions",
                                   needs=["need.governance", "need.clarity"], modules_required=["governance.decisions"]),
                        ScenarioStep("step.weekly_review", StepType.ACTION, "Weekly Thread Review",
                                   needs=["need.memory", "need.learning"], modules_required=["threads.v2"]),
                    ]
                ),
            ],
            required_factors=[
                "profile.experience",
                "profile.tech_comfort",
                "circumstance.urgency",
                "tool.ai_mode",
                "cadence.interaction_frequency",
            ],
        )
    
    @staticmethod
    def project_assisted_30d() -> ScenarioTemplate:
        """30-day assisted project scenario."""
        return ScenarioTemplate(
            template_id="template.project_assisted_30d.v1",
            label="Project Assisted → Execution → Delivery (30 days)",
            description="User manages a project with AI assistance",
            duration_days=30,
            phases=[
                ScenarioPhase(
                    id="phase.0_setup",
                    label="Project Setup",
                    steps=[
                        ScenarioStep("step.project_thread", StepType.ACTION, "Create Project Thread",
                                   needs=["need.memory", "need.organization"], modules_required=["threads.v2"]),
                        ScenarioStep("step.define_scope", StepType.ACTION, "Define Project Scope with Nova",
                                   needs=["need.clarity", "need.execution"], modules_required=["nova.pipeline"]),
                        ScenarioStep("step.hire_team", StepType.ACTION, "Hire Required Agents",
                                   needs=["need.coordination", "need.governance"], modules_required=["agents.hire"]),
                    ]
                ),
                ScenarioPhase(
                    id="phase.1_execution",
                    label="Execution Phase",
                    steps=[
                        ScenarioStep("step.daily_standup", StepType.ACTION, "Daily Standup Review",
                                   needs=["need.coordination", "need.clarity"], modules_required=["threads.v2"]),
                        ScenarioStep("step.decision_sprint", StepType.DECISION, "Sprint Decision Points",
                                   needs=["need.governance", "need.clarity"], modules_required=["governance.decisions"]),
                        ScenarioStep("step.checkpoint_milestone", StepType.CHECKPOINT, "Milestone Checkpoint",
                                   needs=["need.governance", "need.trust"], modules_required=["governance.checkpoints"]),
                    ]
                ),
            ],
            required_factors=[
                "profile.role",
                "circumstance.complexity",
                "circumstance.external_pressure",
                "tool.governance_level",
            ],
        )

# ═══════════════════════════════════════════════════════════════════════════════
# SIMULATION RUN
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FactorSelection:
    """Selected factor values for a run."""
    selections: Dict[str, str] = field(default_factory=dict)
    
    def set(self, factor_id: str, value: str):
        self.selections[factor_id] = value
    
    def get(self, factor_id: str) -> Optional[str]:
        return self.selections.get(factor_id)

@dataclass
class SimulationRun:
    """
    A specific simulation run.
    
    Each run = template × factors × module set
    """
    run_id: str
    template_id: str
    factors: FactorSelection
    modules: List[str]
    status: RunStatus = RunStatus.PLANNED
    
    # Timing
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Results
    current_phase: Optional[str] = None
    current_step: Optional[str] = None
    events: List[Dict[str, Any]] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "template_id": self.template_id,
            "factors": self.factors.selections,
            "modules": self.modules,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "current_phase": self.current_phase,
            "current_step": self.current_step,
            "events": self.events,
            "metrics": self.metrics,
        }
    
    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Log an event during the run."""
        self.events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "data": data,
        })

# ═══════════════════════════════════════════════════════════════════════════════
# SCENARIO GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

class ScenarioGenerator:
    """
    Generate simulation runs from templates and factors.
    
    "We vary factors, not form."
    """
    
    def __init__(self):
        self.factor_library = FactorLibrary.default()
        self.templates: Dict[str, ScenarioTemplate] = {
            "onboarding_30d": ScenarioTemplates.onboarding_30d(),
            "project_assisted_30d": ScenarioTemplates.project_assisted_30d(),
        }
    
    def create_run(
        self,
        template_id: str,
        factor_values: Dict[str, str],
        module_overrides: Optional[List[str]] = None
    ) -> SimulationRun:
        """Create a new simulation run."""
        
        # Get template
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Unknown template: {template_id}")
        
        # Build factor selection
        factors = FactorSelection()
        for factor_id in template.required_factors:
            factor = self.factor_library.get(factor_id)
            if factor:
                value = factor_values.get(factor_id, factor.default_value)
                factors.set(factor_id, value)
        
        # Determine modules (from template or overrides)
        if module_overrides:
            modules = module_overrides
        else:
            modules = template.get_all_modules()
        
        # Resolve dependencies
        modules = ModuleCatalog.resolve_dependencies(modules)
        
        # Validate modules
        validation = ModuleCatalog.validate_module_set(modules)
        if not validation["valid"]:
            logger.warning(f"Module validation issues: {validation}")
        
        # Create run
        run = SimulationRun(
            run_id=str(uuid4()),
            template_id=template_id,
            factors=factors,
            modules=modules,
        )
        
        logger.info(f"Created simulation run: {run.run_id}")
        return run
    
    def start_run(self, run: SimulationRun) -> SimulationRun:
        """Start a simulation run."""
        run.status = RunStatus.RUNNING
        run.started_at = datetime.utcnow()
        
        # Get template
        template = self.templates.get(run.template_id)
        if template and template.phases:
            run.current_phase = template.phases[0].id
            if template.phases[0].steps:
                run.current_step = template.phases[0].steps[0].id
        
        run.log_event("run_started", {"factors": run.factors.selections})
        return run
    
    def advance_step(self, run: SimulationRun) -> bool:
        """Advance to the next step. Returns False if run is complete."""
        template = self.templates.get(run.template_id)
        if not template:
            return False
        
        # Find current position
        current_phase_idx = None
        current_step_idx = None
        
        for pi, phase in enumerate(template.phases):
            if phase.id == run.current_phase:
                current_phase_idx = pi
                for si, step in enumerate(phase.steps):
                    if step.id == run.current_step:
                        current_step_idx = si
                        break
                break
        
        if current_phase_idx is None:
            return False
        
        # Try to advance step
        current_phase = template.phases[current_phase_idx]
        if current_step_idx is not None and current_step_idx < len(current_phase.steps) - 1:
            run.current_step = current_phase.steps[current_step_idx + 1].id
            run.log_event("step_advanced", {"step": run.current_step})
            return True
        
        # Try to advance phase
        if current_phase_idx < len(template.phases) - 1:
            next_phase = template.phases[current_phase_idx + 1]
            run.current_phase = next_phase.id
            run.current_step = next_phase.steps[0].id if next_phase.steps else None
            run.log_event("phase_advanced", {"phase": run.current_phase})
            return True
        
        # Run complete
        run.status = RunStatus.COMPLETED
        run.completed_at = datetime.utcnow()
        run.log_event("run_completed", {"duration_seconds": (run.completed_at - run.started_at).total_seconds()})
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "Factor",
    "FactorLibrary",
    "FactorCategory",
    "ScenarioStep",
    "ScenarioPhase",
    "ScenarioTemplate",
    "ScenarioTemplates",
    "SimulationRun",
    "FactorSelection",
    "ScenarioGenerator",
    "StepType",
    "RunStatus",
]
