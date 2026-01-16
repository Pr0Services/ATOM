"""
CHE·NU™ — Yellow Pages (Service Registry)
==========================================
Maps needs (tags) to:
- Authority modules (who owns this capability)
- Fallback services (on-demand agents)
- Guards (security requirements)

The orchestrator uses this to route requests to the right module/service.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Callable, Awaitable
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
import logging
from abc import ABC, abstractmethod

from .synaptic_graph import ModuleID, Priority

logger = logging.getLogger(__name__)


class NeedTag(str, Enum):
    """Tags representing user/system needs"""
    # Governance
    GOVERNANCE_POLICY = "#Governance_Policy"
    
    # Computation
    CAUSAL_EXPLAINWHY = "#Causal_ExplainWhy"
    SIMULATE_SCENARIO = "#Simulate_Scenario"
    
    # Interface
    XR_VISUALIZE = "#XR_Visualize"
    
    # Business
    EQUITY_CONTRACT = "#Equity_Contract"
    PUBLIC_DEBATE = "#Public_Debate"
    
    # Learning
    LEARN_SKILLGAP = "#Learn_SkillGap"
    PUBLISH_KNOWLEDGE = "#Publish_Knowledge"
    
    # Community
    COMMUNITY_NEEDS = "#Community_Needs"
    RESONANCE_NUDGE = "#Resonance_Nudge"
    
    # Dashboard
    DASHBOARD_CONTEXT = "#Dashboard_Context"
    
    # Security
    SECURE_TRANSPORT = "#Secure_Transport"
    
    # Generic
    ARTIFACT_CREATE = "#Artifact_Create"
    TASK_EXECUTE = "#Task_Execute"
    MEMORY_RECALL = "#Memory_Recall"


class GuardRequirement(str, Enum):
    """Guard requirements for service access"""
    NONE = "none"
    OPA_REQUIRED = "opa_required"
    TRUST_OPTIONAL = "trust_optional"
    TRUST_REQUIRED = "trust_required"
    RATE_LIMITED = "rate_limited"
    SCOPE_AWARE = "scope_aware"
    RIGHTS_PROTECTED = "rights_protected"
    PRIVACY_SAFE = "privacy_safe"
    SAFETY_GUARD = "safety_guard"
    COGNITIVE_LOAD = "cognitive_load"
    CIVICS_RULES = "civics_rules"
    JIT_SESSIONS = "jit_sessions"
    P0_INFRA = "p0_infra"
    P1_INFRA = "p1_infra"


@dataclass
class FallbackService:
    """On-demand service that can handle requests"""
    service_id: str
    name: str
    description: str
    is_available: bool = True
    cost_tokens: int = 100
    max_concurrent: int = 10
    current_load: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "name": self.name,
            "description": self.description,
            "is_available": self.is_available,
            "cost_tokens": self.cost_tokens,
            "max_concurrent": self.max_concurrent,
            "current_load": self.current_load
        }
    
    @property
    def has_capacity(self) -> bool:
        return self.current_load < self.max_concurrent


@dataclass
class YellowPageEntry:
    """Entry in the yellow pages registry"""
    entry_id: UUID = field(default_factory=uuid4)
    need_tag: NeedTag = None
    authority_module: ModuleID = None
    fallback_service: FallbackService = None
    guards: List[GuardRequirement] = field(default_factory=list)
    priority: Priority = Priority.P2
    description: str = ""
    
    # Usage stats
    call_count: int = 0
    last_called: Optional[datetime] = None
    avg_response_ms: float = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": str(self.entry_id),
            "need_tag": self.need_tag.value if self.need_tag else None,
            "authority_module": self.authority_module.value if self.authority_module else None,
            "fallback_service": self.fallback_service.to_dict() if self.fallback_service else None,
            "guards": [g.value for g in self.guards],
            "priority": self.priority.value,
            "description": self.description,
            "call_count": self.call_count,
            "last_called": self.last_called.isoformat() if self.last_called else None,
            "avg_response_ms": self.avg_response_ms
        }


class ServiceHandler(ABC):
    """Abstract handler for service execution"""
    
    @property
    @abstractmethod
    def service_id(self) -> str:
        pass
    
    @abstractmethod
    async def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute service request"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if service is healthy"""
        pass


class DefaultServiceHandler(ServiceHandler):
    """Default handler that logs and returns stub response"""
    
    def __init__(self, service_id: str):
        self._service_id = service_id
    
    @property
    def service_id(self) -> str:
        return self._service_id
    
    async def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Service {self._service_id} executing: {request}")
        return {
            "status": "completed",
            "service_id": self._service_id,
            "result": "stub_response"
        }
    
    async def health_check(self) -> bool:
        return True


@dataclass
class RoutingDecision:
    """Decision made by yellow pages router"""
    decision_id: UUID = field(default_factory=uuid4)
    need_tag: NeedTag = None
    routed_to: str = ""  # Module or service ID
    is_module: bool = True
    guards_required: List[GuardRequirement] = field(default_factory=list)
    reason: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": str(self.decision_id),
            "need_tag": self.need_tag.value if self.need_tag else None,
            "routed_to": self.routed_to,
            "is_module": self.is_module,
            "guards_required": [g.value for g in self.guards_required],
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat()
        }


class YellowPages:
    """
    Service registry for CHE·NU™.
    
    Routes needs to the right module or fallback service.
    Enforces guards and tracks usage.
    """
    
    def __init__(self):
        # Registry entries
        self._entries: Dict[NeedTag, YellowPageEntry] = {}
        
        # Service handlers
        self._handlers: Dict[str, ServiceHandler] = {}
        
        # Module availability
        self._module_status: Dict[ModuleID, bool] = {m: True for m in ModuleID}
        
        # Initialize default entries
        self._init_default_entries()
    
    def _init_default_entries(self) -> None:
        """Initialize the canonical yellow pages"""
        
        # Governance
        self.register(
            need_tag=NeedTag.GOVERNANCE_POLICY,
            authority_module=ModuleID.MOD_01_OPA,
            fallback_service=FallbackService(
                service_id="policy_inspector",
                name="Policy-Inspector",
                description="Inspect and validate policies"
            ),
            guards=[GuardRequirement.OPA_REQUIRED],
            priority=Priority.P0,
            description="Policy checking and enforcement"
        )
        
        # Causal reasoning
        self.register(
            need_tag=NeedTag.CAUSAL_EXPLAINWHY,
            authority_module=ModuleID.MOD_03_CAUSAL,
            fallback_service=FallbackService(
                service_id="causal_explainer",
                name="Causal-Explainer",
                description="Explain causal relationships"
            ),
            guards=[GuardRequirement.TRUST_OPTIONAL],
            priority=Priority.P1,
            description="Causal explanation and reasoning"
        )
        
        # Simulation
        self.register(
            need_tag=NeedTag.SIMULATE_SCENARIO,
            authority_module=ModuleID.MOD_04_WORLDENGINE,
            fallback_service=FallbackService(
                service_id="scenario_runner",
                name="Scenario-Runner",
                description="Run scenario simulations",
                cost_tokens=500
            ),
            guards=[GuardRequirement.RATE_LIMITED],
            priority=Priority.P1,
            description="World simulation and scenario analysis"
        )
        
        # XR visualization
        self.register(
            need_tag=NeedTag.XR_VISUALIZE,
            authority_module=ModuleID.MOD_06_XR,
            fallback_service=FallbackService(
                service_id="xr_renderer",
                name="XR-Renderer",
                description="Render XR visualizations"
            ),
            guards=[GuardRequirement.SCOPE_AWARE],
            priority=Priority.P2,
            description="XR and spatial visualization"
        )
        
        # Equity/Business
        self.register(
            need_tag=NeedTag.EQUITY_CONTRACT,
            authority_module=ModuleID.MOD_17_GENESIS,
            fallback_service=FallbackService(
                service_id="equity_calculator",
                name="Equity-Calculator",
                description="Calculate equity and contracts"
            ),
            guards=[GuardRequirement.OPA_REQUIRED, GuardRequirement.TRUST_REQUIRED],
            priority=Priority.P2,
            description="Equity, contracts, and task management"
        )
        
        # Public debate
        self.register(
            need_tag=NeedTag.PUBLIC_DEBATE,
            authority_module=ModuleID.MOD_18_AGORA,
            fallback_service=FallbackService(
                service_id="bias_moderator",
                name="Bias-Moderator",
                description="Moderate debates for bias"
            ),
            guards=[GuardRequirement.CIVICS_RULES],
            priority=Priority.P2,
            description="Public debate and voting"
        )
        
        # Learning
        self.register(
            need_tag=NeedTag.LEARN_SKILLGAP,
            authority_module=ModuleID.MOD_21_EDU,
            fallback_service=FallbackService(
                service_id="ghost_tutor",
                name="Ghost-Tutor",
                description="JIT learning assistance"
            ),
            guards=[GuardRequirement.JIT_SESSIONS],
            priority=Priority.P2,
            description="Skill gap analysis and learning paths"
        )
        
        # Knowledge publishing
        self.register(
            need_tag=NeedTag.PUBLISH_KNOWLEDGE,
            authority_module=ModuleID.MOD_20_LIBRARY,
            fallback_service=FallbackService(
                service_id="semantic_translator",
                name="Semantic-Translator",
                description="Translate and format knowledge"
            ),
            guards=[GuardRequirement.RIGHTS_PROTECTED],
            priority=Priority.P3,
            description="Knowledge publishing and library"
        )
        
        # Community needs
        self.register(
            need_tag=NeedTag.COMMUNITY_NEEDS,
            authority_module=ModuleID.MOD_23_COMMUNITY,
            fallback_service=FallbackService(
                service_id="needs_scanner",
                name="Needs-Scanner",
                description="Scan and analyze community needs"
            ),
            guards=[GuardRequirement.PRIVACY_SAFE],
            priority=Priority.P2,
            description="Community needs heatmap"
        )
        
        # Resonance/Ambient
        self.register(
            need_tag=NeedTag.RESONANCE_NUDGE,
            authority_module=ModuleID.MOD_24_RESONANCE,
            fallback_service=FallbackService(
                service_id="ambient_adjuster",
                name="Ambient-Adjuster",
                description="Adjust ambient conditions"
            ),
            guards=[GuardRequirement.SAFETY_GUARD],
            priority=Priority.P2,
            description="Ambient and aesthetic adjustments"
        )
        
        # Dashboard
        self.register(
            need_tag=NeedTag.DASHBOARD_CONTEXT,
            authority_module=ModuleID.MOD_25_SYNAPTIC_DASH,
            fallback_service=FallbackService(
                service_id="ui_composer",
                name="UI-Composer",
                description="Compose dashboard UI"
            ),
            guards=[GuardRequirement.COGNITIVE_LOAD],
            priority=Priority.P2,
            description="Dashboard context and UI"
        )
        
        # Secure transport
        self.register(
            need_tag=NeedTag.SECURE_TRANSPORT,
            authority_module=ModuleID.MOD_QP_PHOTONIC,
            fallback_service=FallbackService(
                service_id="qkd_key_manager",
                name="QKD-Key-Manager",
                description="Manage quantum keys"
            ),
            guards=[GuardRequirement.P1_INFRA],
            priority=Priority.P1,
            description="Quantum-secure transport"
        )
    
    def register(
        self,
        need_tag: NeedTag,
        authority_module: ModuleID,
        fallback_service: FallbackService,
        guards: List[GuardRequirement] = None,
        priority: Priority = Priority.P2,
        description: str = ""
    ) -> YellowPageEntry:
        """Register a new entry"""
        entry = YellowPageEntry(
            need_tag=need_tag,
            authority_module=authority_module,
            fallback_service=fallback_service,
            guards=guards or [],
            priority=priority,
            description=description
        )
        
        self._entries[need_tag] = entry
        
        # Register default handler for fallback
        if fallback_service.service_id not in self._handlers:
            self._handlers[fallback_service.service_id] = DefaultServiceHandler(
                fallback_service.service_id
            )
        
        logger.debug(f"Registered: {need_tag.value} -> {authority_module.value}")
        
        return entry
    
    def register_handler(self, service_id: str, handler: ServiceHandler) -> None:
        """Register a custom service handler"""
        self._handlers[service_id] = handler
    
    def set_module_status(self, module: ModuleID, is_available: bool) -> None:
        """Set module availability status"""
        self._module_status[module] = is_available
    
    def lookup(self, need_tag: NeedTag) -> Optional[YellowPageEntry]:
        """Lookup entry by need tag"""
        return self._entries.get(need_tag)
    
    def route(self, need_tag: NeedTag) -> RoutingDecision:
        """
        Route a need to the appropriate module or service.
        
        Routing priority:
        1. Authority module (if available)
        2. Fallback service (if module unavailable)
        """
        entry = self._entries.get(need_tag)
        
        if not entry:
            return RoutingDecision(
                need_tag=need_tag,
                routed_to="unknown",
                reason="No entry found for need tag"
            )
        
        # Check if authority module is available
        if self._module_status.get(entry.authority_module, False):
            return RoutingDecision(
                need_tag=need_tag,
                routed_to=entry.authority_module.value,
                is_module=True,
                guards_required=entry.guards,
                reason="Routed to authority module"
            )
        
        # Fallback to service
        if entry.fallback_service and entry.fallback_service.is_available:
            if entry.fallback_service.has_capacity:
                return RoutingDecision(
                    need_tag=need_tag,
                    routed_to=entry.fallback_service.service_id,
                    is_module=False,
                    guards_required=entry.guards,
                    reason="Module unavailable, routed to fallback service"
                )
            else:
                return RoutingDecision(
                    need_tag=need_tag,
                    routed_to=entry.fallback_service.service_id,
                    is_module=False,
                    guards_required=entry.guards,
                    reason="Fallback service at capacity"
                )
        
        return RoutingDecision(
            need_tag=need_tag,
            routed_to="none",
            reason="No available module or service"
        )
    
    async def execute(
        self,
        need_tag: NeedTag,
        request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Route and execute a request.
        
        Returns response from module or fallback service.
        """
        import time
        start = time.time()
        
        decision = self.route(need_tag)
        entry = self._entries.get(need_tag)
        
        if decision.routed_to in ("unknown", "none"):
            return {
                "status": "error",
                "error": decision.reason,
                "decision": decision.to_dict()
            }
        
        try:
            if decision.is_module:
                # Module execution (stub - would integrate with actual module)
                result = {
                    "status": "completed",
                    "module": decision.routed_to,
                    "result": f"Module {decision.routed_to} executed"
                }
            else:
                # Service execution
                handler = self._handlers.get(decision.routed_to)
                if handler:
                    # Update load
                    if entry and entry.fallback_service:
                        entry.fallback_service.current_load += 1
                    
                    try:
                        result = await handler.execute(request)
                    finally:
                        if entry and entry.fallback_service:
                            entry.fallback_service.current_load -= 1
                else:
                    result = {
                        "status": "error",
                        "error": f"No handler for service {decision.routed_to}"
                    }
            
            # Update stats
            if entry:
                entry.call_count += 1
                entry.last_called = datetime.utcnow()
                duration_ms = (time.time() - start) * 1000
                entry.avg_response_ms = (
                    (entry.avg_response_ms * (entry.call_count - 1) + duration_ms)
                    / entry.call_count
                )
            
            return {
                **result,
                "decision": decision.to_dict(),
                "duration_ms": (time.time() - start) * 1000
            }
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "decision": decision.to_dict()
            }
    
    def get_all_entries(self) -> List[YellowPageEntry]:
        """Get all registry entries"""
        return list(self._entries.values())
    
    def get_entries_by_priority(self, priority: Priority) -> List[YellowPageEntry]:
        """Get entries by priority"""
        return [e for e in self._entries.values() if e.priority == priority]
    
    def get_entries_by_module(self, module: ModuleID) -> List[YellowPageEntry]:
        """Get entries by authority module"""
        return [e for e in self._entries.values() if e.authority_module == module]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return {
            "total_entries": len(self._entries),
            "by_priority": {
                p.value: len(self.get_entries_by_priority(p))
                for p in Priority
            },
            "module_availability": {
                m.value: self._module_status.get(m, False)
                for m in ModuleID
            },
            "total_calls": sum(e.call_count for e in self._entries.values()),
            "handlers_registered": len(self._handlers)
        }
    
    def export_table(self) -> List[Dict[str, str]]:
        """Export as table for documentation"""
        return [
            {
                "Need Tag": e.need_tag.value,
                "Authority Module": e.authority_module.value,
                "Fallback Service": e.fallback_service.name if e.fallback_service else "None",
                "Guards": ", ".join(g.value for g in e.guards)
            }
            for e in self._entries.values()
        ]


# Singleton instance
_yellow_pages: Optional[YellowPages] = None

def get_yellow_pages() -> YellowPages:
    """Get singleton yellow pages instance"""
    global _yellow_pages
    if _yellow_pages is None:
        _yellow_pages = YellowPages()
    return _yellow_pages
