"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ — MODULE CATALOG V1                               ║
║                                                                              ║
║  Every module declares: needs_served, dependencies, activation_modes,       ║
║  cost_profile, risk_profile, known_usages.                                  ║
║                                                                              ║
║  Modules without needs_served are NOT eligible for activation.              ║
║  Dependencies are hard constraints.                                         ║
║  Governance-required modules must emit/consume thread events.               ║
║                                                                              ║
║  GOUVERNANCE > EXÉCUTION                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set
import logging

logger = logging.getLogger("chenu.canon.modules")

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════

class ActivationMode(str, Enum):
    """Module activation modes."""
    DISABLED = "disabled"                   # Not available to this identity/thread
    ENABLED_PASSIVE = "enabled_passive"     # Only responds when called
    ENABLED_GUIDED = "enabled_guided"       # Step-by-step guidance, more checkpoints
    ENABLED_BALANCED = "enabled_balanced"   # Default; mix of suggestions and autonomy
    ENABLED_AUTONOMOUS = "enabled_autonomous"  # High autonomy (still audited)
    ENABLED_RESTRICTED = "enabled_restricted"  # High-risk/low-trust contexts
    ENABLED_OVERCLOCKED = "enabled_overclocked"  # Stress-test mode

class RiskLevel(str, Enum):
    """Module risk level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CostProfile(str, Enum):
    """Module cost profile."""
    FREE = "free"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VARIABLE = "variable"

class ModuleCategory(str, Enum):
    """Module categories."""
    CORE = "core"
    COMMUNICATION = "communication"
    GOVERNANCE = "governance"
    AGENTS = "agents"
    SIMULATION = "simulation"
    XR = "xr"
    INTEGRATION = "integration"
    ANALYTICS = "analytics"

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE MODEL
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Module:
    """
    A system module with declared capabilities and constraints.
    
    Rules:
    - Module MUST declare needs_served (or it cannot be activated)
    - Dependencies are HARD constraints
    - Governance modules MUST emit/consume thread events
    """
    id: str
    category: ModuleCategory
    needs_served: List[str]  # Need IDs from NeedCanon
    dependencies: List[str]  # Other module IDs
    risk_level: RiskLevel
    cost_profile: CostProfile
    risk_profile: List[str]  # Specific risks this module poses
    activation_modes: List[ActivationMode]
    known_usages: List[str]  # Known use cases
    
    # Optional metadata
    label: Optional[str] = None
    description: Optional[str] = None
    requires_governance: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category.value,
            "needs_served": self.needs_served,
            "dependencies": self.dependencies,
            "risk_level": self.risk_level.value,
            "cost_profile": self.cost_profile.value,
            "risk_profile": self.risk_profile,
            "activation_modes": [m.value for m in self.activation_modes],
            "known_usages": self.known_usages,
            "label": self.label,
            "description": self.description,
            "requires_governance": self.requires_governance,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Module":
        return cls(
            id=data["id"],
            category=ModuleCategory(data["category"]),
            needs_served=data.get("needs_served", []),
            dependencies=data.get("dependencies", []),
            risk_level=RiskLevel(data.get("risk_level", "medium")),
            cost_profile=CostProfile(data.get("cost_profile", "low")),
            risk_profile=data.get("risk_profile", []),
            activation_modes=[ActivationMode(m) for m in data.get("activation_modes", [])],
            known_usages=data.get("known_usages", []),
            label=data.get("label"),
            description=data.get("description"),
            requires_governance=data.get("requires_governance", False),
        )
    
    def can_activate(self) -> bool:
        """Check if module can be activated (has needs_served)."""
        return len(self.needs_served) > 0
    
    def supports_mode(self, mode: ActivationMode) -> bool:
        """Check if module supports a specific activation mode."""
        return mode in self.activation_modes

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE CATALOG
# ═══════════════════════════════════════════════════════════════════════════════

class ModuleCatalog:
    """
    The catalog of all system modules.
    
    Version: v1
    """
    
    VERSION = "v1"
    NAMESPACE = "module"
    
    # Rules
    RULES = [
        "Every module declares: needs_served, dependencies, activation_modes, cost_profile, risk_profile, known_usages.",
        "Modules without needs_served are not eligible for activation.",
        "Dependencies are hard constraints; scenario generator must satisfy them.",
        "Governance-required modules must emit/consume thread events (append-only).",
    ]
    
    # The Module Registry
    MODULES: Dict[str, Module] = {
        # ═══════════════════════════════════════════════════════════════════════
        # CORE MODULES
        # ═══════════════════════════════════════════════════════════════════════
        
        "auth.core": Module(
            id="auth.core",
            category=ModuleCategory.CORE,
            needs_served=["need.trust", "need.safety", "need.identity"],
            dependencies=[],
            risk_level=RiskLevel.HIGH,
            cost_profile=CostProfile.LOW,
            risk_profile=["credential_stuffing", "token_leak", "session_hijack"],
            activation_modes=[ActivationMode.ENABLED_GUIDED, ActivationMode.ENABLED_BALANCED, ActivationMode.ENABLED_RESTRICTED],
            known_usages=["register", "login", "refresh", "logout", "me"],
            label="Authentication Core",
            requires_governance=True,
        ),
        
        "identity.boundary": Module(
            id="identity.boundary",
            category=ModuleCategory.CORE,
            needs_served=["need.identity", "need.safety", "need.trust"],
            dependencies=["auth.core"],
            risk_level=RiskLevel.CRITICAL,
            cost_profile=CostProfile.LOW,
            risk_profile=["cross_tenant_leak", "permission_bypass"],
            activation_modes=[ActivationMode.ENABLED_BALANCED, ActivationMode.ENABLED_RESTRICTED],
            known_usages=["tenant_isolation", "identity_context_injection"],
            label="Identity Boundary",
            requires_governance=True,
        ),
        
        "spheres.catalog": Module(
            id="spheres.catalog",
            category=ModuleCategory.CORE,
            needs_served=["need.organization", "need.discovery", "need.trust"],
            dependencies=["identity.boundary"],
            risk_level=RiskLevel.MEDIUM,
            cost_profile=CostProfile.LOW,
            risk_profile=["wrong_scope", "misrouting"],
            activation_modes=[ActivationMode.ENABLED_PASSIVE, ActivationMode.ENABLED_BALANCED, ActivationMode.ENABLED_GUIDED],
            known_usages=["list_spheres", "select_sphere", "seed_fixed_spheres"],
            label="Spheres Catalog (9 spheres)",
        ),
        
        "bureau.sections": Module(
            id="bureau.sections",
            category=ModuleCategory.CORE,
            needs_served=["need.organization", "need.clarity", "need.communication"],
            dependencies=["spheres.catalog"],
            risk_level=RiskLevel.MEDIUM,
            cost_profile=CostProfile.LOW,
            risk_profile=["ux_confusion"],
            activation_modes=[ActivationMode.ENABLED_BALANCED, ActivationMode.ENABLED_GUIDED],
            known_usages=["tabs_quickcapture", "threads", "datafiles", "active_agents", "meetings", "resume_workspace"],
            label="Bureau Sections (6 per sphere)",
        ),
        
        "threads.v2": Module(
            id="threads.v2",
            category=ModuleCategory.CORE,
            needs_served=["need.memory", "need.clarity", "need.trust"],
            dependencies=["identity.boundary", "spheres.catalog"],
            risk_level=RiskLevel.HIGH,
            cost_profile=CostProfile.LOW,
            risk_profile=["event_overload", "schema_drift", "poor_summaries"],
            activation_modes=[ActivationMode.ENABLED_BALANCED, ActivationMode.ENABLED_GUIDED, ActivationMode.ENABLED_RESTRICTED],
            known_usages=["create_thread", "append_event", "append_correction", "list_threads", "get_events", "snapshots"],
            label="Thread System V2",
            requires_governance=True,
        ),
        
        # ═══════════════════════════════════════════════════════════════════════
        # NOVA & AI MODULES
        # ═══════════════════════════════════════════════════════════════════════
        
        "nova.pipeline": Module(
            id="nova.pipeline",
            category=ModuleCategory.CORE,
            needs_served=["need.execution", "need.clarity", "need.learning", "need.communication", "need.performance"],
            dependencies=["threads.v2", "governance.core"],
            risk_level=RiskLevel.HIGH,
            cost_profile=CostProfile.VARIABLE,
            risk_profile=["hallucination", "cost_spike", "latency", "context_overflow"],
            activation_modes=[ActivationMode.ENABLED_GUIDED, ActivationMode.ENABLED_BALANCED, ActivationMode.ENABLED_AUTONOMOUS],
            known_usages=["chat", "draft", "summarize", "extract", "classify"],
            label="Nova AI Pipeline",
            requires_governance=True,
        ),
        
        # ═══════════════════════════════════════════════════════════════════════
        # GOVERNANCE MODULES
        # ═══════════════════════════════════════════════════════════════════════
        
        "governance.core": Module(
            id="governance.core",
            category=ModuleCategory.GOVERNANCE,
            needs_served=["need.governance", "need.safety", "need.trust"],
            dependencies=["identity.boundary"],
            risk_level=RiskLevel.CRITICAL,
            cost_profile=CostProfile.LOW,
            risk_profile=["policy_bypass", "audit_gap"],
            activation_modes=[ActivationMode.ENABLED_BALANCED, ActivationMode.ENABLED_RESTRICTED],
            known_usages=["checkpoints", "audit_log", "policy_check", "signals"],
            label="Governance Core",
            requires_governance=True,
        ),
        
        "governance.checkpoints": Module(
            id="governance.checkpoints",
            category=ModuleCategory.GOVERNANCE,
            needs_served=["need.governance", "need.trust", "need.safety"],
            dependencies=["governance.core"],
            risk_level=RiskLevel.HIGH,
            cost_profile=CostProfile.LOW,
            risk_profile=["checkpoint_fatigue", "approval_delay"],
            activation_modes=[ActivationMode.ENABLED_BALANCED, ActivationMode.ENABLED_RESTRICTED],
            known_usages=["create_checkpoint", "resolve_checkpoint", "pending_checkpoints"],
            label="Checkpoint System",
            requires_governance=True,
        ),
        
        "governance.decisions": Module(
            id="governance.decisions",
            category=ModuleCategory.GOVERNANCE,
            needs_served=["need.clarity", "need.governance", "need.coordination"],
            dependencies=["governance.core", "threads.v2"],
            risk_level=RiskLevel.HIGH,
            cost_profile=CostProfile.LOW,
            risk_profile=["decision_paralysis", "aging_ignored"],
            activation_modes=[ActivationMode.ENABLED_GUIDED, ActivationMode.ENABLED_BALANCED],
            known_usages=["create_decision", "make_decision", "aging_timeline", "defer"],
            label="Decision Points (Aging)",
            requires_governance=True,
        ),
        
        # ═══════════════════════════════════════════════════════════════════════
        # AGENT MODULES
        # ═══════════════════════════════════════════════════════════════════════
        
        "agents.marketplace": Module(
            id="agents.marketplace",
            category=ModuleCategory.AGENTS,
            needs_served=["need.execution", "need.discovery", "need.coordination"],
            dependencies=["identity.boundary", "spheres.catalog"],
            risk_level=RiskLevel.MEDIUM,
            cost_profile=CostProfile.LOW,
            risk_profile=["wrong_agent_match", "cost_confusion"],
            activation_modes=[ActivationMode.ENABLED_PASSIVE, ActivationMode.ENABLED_BALANCED],
            known_usages=["list_agents", "search_agents", "agent_details"],
            label="Agent Marketplace",
        ),
        
        "agents.hire": Module(
            id="agents.hire",
            category=ModuleCategory.AGENTS,
            needs_served=["need.execution", "need.coordination", "need.governance"],
            dependencies=["agents.marketplace", "governance.checkpoints"],
            risk_level=RiskLevel.HIGH,
            cost_profile=CostProfile.VARIABLE,
            risk_profile=["unauthorized_hire", "budget_overrun"],
            activation_modes=[ActivationMode.ENABLED_GUIDED, ActivationMode.ENABLED_BALANCED],
            known_usages=["hire_agent", "dismiss_agent", "agent_status"],
            label="Agent Hire/Dismiss",
            requires_governance=True,
        ),
        
        "agents.stagiaire": Module(
            id="agents.stagiaire",
            category=ModuleCategory.AGENTS,
            needs_served=["need.learning", "need.memory", "need.trust"],
            dependencies=["threads.v2"],
            risk_level=RiskLevel.LOW,
            cost_profile=CostProfile.LOW,
            risk_profile=["noise_accumulation", "missed_patterns"],
            activation_modes=[ActivationMode.ENABLED_PASSIVE],
            known_usages=["observe_conversation", "create_note", "promotion_candidate"],
            label="Stagiaire (Learning Agent)",
        ),
        
        "agents.professeur": Module(
            id="agents.professeur",
            category=ModuleCategory.AGENTS,
            needs_served=["need.learning", "need.governance", "need.trust"],
            dependencies=["agents.stagiaire"],
            risk_level=RiskLevel.LOW,
            cost_profile=CostProfile.LOW,
            risk_profile=["over_correction", "false_failures"],
            activation_modes=[ActivationMode.ENABLED_PASSIVE],
            known_usages=["mark_failure", "create_recentering", "apply_recentering"],
            label="Professeur (Stability Agent)",
        ),
        
        # ═══════════════════════════════════════════════════════════════════════
        # XR MODULES
        # ═══════════════════════════════════════════════════════════════════════
        
        "xr.viewer": Module(
            id="xr.viewer",
            category=ModuleCategory.XR,
            needs_served=["need.presence", "need.clarity", "need.organization"],
            dependencies=["spheres.catalog", "threads.v2"],
            risk_level=RiskLevel.MEDIUM,
            cost_profile=CostProfile.MEDIUM,
            risk_profile=["performance_degradation", "immersion_break"],
            activation_modes=[ActivationMode.ENABLED_PASSIVE, ActivationMode.ENABLED_BALANCED],
            known_usages=["enter_xr", "navigate_spheres", "view_thread_room"],
            label="XR Viewer (READ-ONLY)",
        ),
        
        "xr.artifacts": Module(
            id="xr.artifacts",
            category=ModuleCategory.XR,
            needs_served=["need.presence", "need.memory", "need.trust"],
            dependencies=["xr.viewer", "governance.core"],
            risk_level=RiskLevel.MEDIUM,
            cost_profile=CostProfile.MEDIUM,
            risk_profile=["artifact_tampering", "integrity_failure"],
            activation_modes=[ActivationMode.ENABLED_PASSIVE],
            known_usages=["load_artifact", "verify_signature", "display_artifact"],
            label="XR Artifacts (Signed)",
            requires_governance=True,
        ),
        
        # ═══════════════════════════════════════════════════════════════════════
        # COMMUNICATION MODULES
        # ═══════════════════════════════════════════════════════════════════════
        
        "meetings.core": Module(
            id="meetings.core",
            category=ModuleCategory.COMMUNICATION,
            needs_served=["need.communication", "need.coordination", "need.memory"],
            dependencies=["threads.v2", "identity.boundary"],
            risk_level=RiskLevel.MEDIUM,
            cost_profile=CostProfile.LOW,
            risk_profile=["scheduling_conflict", "missed_participants"],
            activation_modes=[ActivationMode.ENABLED_GUIDED, ActivationMode.ENABLED_BALANCED],
            known_usages=["schedule_meeting", "join_meeting", "meeting_notes"],
            label="Meetings Core",
        ),
        
        "notifications.core": Module(
            id="notifications.core",
            category=ModuleCategory.COMMUNICATION,
            needs_served=["need.communication", "need.coordination"],
            dependencies=["identity.boundary"],
            risk_level=RiskLevel.LOW,
            cost_profile=CostProfile.LOW,
            risk_profile=["notification_flood", "missed_critical"],
            activation_modes=[ActivationMode.ENABLED_BALANCED],
            known_usages=["send_notification", "mark_read", "unread_count"],
            label="Notifications",
        ),
    }
    
    @classmethod
    def get(cls, module_id: str) -> Optional[Module]:
        """Get a module by ID."""
        return cls.MODULES.get(module_id)
    
    @classmethod
    def all(cls) -> List[Module]:
        """Get all modules."""
        return list(cls.MODULES.values())
    
    @classmethod
    def by_category(cls, category: ModuleCategory) -> List[Module]:
        """Get modules by category."""
        return [m for m in cls.MODULES.values() if m.category == category]
    
    @classmethod
    def by_need(cls, need_id: str) -> List[Module]:
        """Get modules that serve a specific need."""
        return [m for m in cls.MODULES.values() if need_id in m.needs_served]
    
    @classmethod
    def activatable(cls) -> List[Module]:
        """Get all modules that can be activated (have needs_served)."""
        return [m for m in cls.MODULES.values() if m.can_activate()]
    
    @classmethod
    def governance_required(cls) -> List[Module]:
        """Get modules that require governance."""
        return [m for m in cls.MODULES.values() if m.requires_governance]
    
    @classmethod
    def resolve_dependencies(cls, module_ids: List[str]) -> List[str]:
        """Resolve all dependencies for a list of modules (topological sort)."""
        resolved: List[str] = []
        visited: Set[str] = set()
        
        def visit(module_id: str):
            if module_id in visited:
                return
            visited.add(module_id)
            
            module = cls.get(module_id)
            if module:
                for dep in module.dependencies:
                    visit(dep)
                resolved.append(module_id)
        
        for mid in module_ids:
            visit(mid)
        
        return resolved
    
    @classmethod
    def validate_module_set(cls, module_ids: List[str]) -> Dict[str, Any]:
        """Validate a set of modules for a scenario."""
        result = {
            "valid": True,
            "missing_modules": [],
            "unmet_dependencies": [],
            "needs_covered": set(),
        }
        
        # Check all modules exist
        for mid in module_ids:
            if mid not in cls.MODULES:
                result["valid"] = False
                result["missing_modules"].append(mid)
        
        # Check dependencies are met
        for mid in module_ids:
            module = cls.get(mid)
            if module:
                for dep in module.dependencies:
                    if dep not in module_ids:
                        result["valid"] = False
                        result["unmet_dependencies"].append({"module": mid, "missing_dep": dep})
                
                # Collect needs covered
                result["needs_covered"].update(module.needs_served)
        
        result["needs_covered"] = list(result["needs_covered"])
        return result

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "Module",
    "ModuleCatalog",
    "ActivationMode",
    "RiskLevel",
    "CostProfile",
    "ModuleCategory",
]
