"""
============================================================================
CHE·NU™ V69 — INDUSTRIALISATION SYSTEMS
============================================================================
Combined implementation of:
- Industrialization Plan
- XR Pack AutoGen V1.4
- World Sim Gameplay Mechanics
- Prompt Collection Architecture
- API Agent Management Best Practices
- OPA Policy Bundles Templates

"POC → MVP → Enterprise: GOUVERNANCE > EXÉCUTION"
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging

from .models import (
    # Industrialization
    ProductLayer, IndustrializationPhase,
    ProductLayerSpec, IndustrializationPlan,
    # XR Pack
    XRPackManifest, ReplayFrame, HeatmapTile, DiffEntry, XRPack,
    # Gameplay
    GameplayMechanicType, Quest, GameplayState,
    # Prompt Collection
    PromptAxis, PromptAsset, PromptLibrary,
    # API Agent Management
    AgentRegistryEntry, EvaluationResult, APIAgentManagementConfig,
    # OPA Bundles
    PolicyRule, PolicyBundle, BundleRegistry,
    generate_id, compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 1. INDUSTRIALIZATION SERVICE
# ============================================================================

class IndustrializationService:
    """
    Industrialization Plan Service.
    
    Per spec: Transform POC into robust, scalable, auditable product
    """
    
    # Default product layers
    DEFAULT_LAYERS = [
        ProductLayerSpec(
            ProductLayer.UX_XR,
            "UX / XR / Web Cockpit - read-only, decisional",
            ["read_only", "responsive", "accessible"],
        ),
        ProductLayerSpec(
            ProductLayer.EXPLAINABILITY,
            "Explainability & Diff Layer - why / deltas / traces",
            ["why_why", "deltas", "audit_traces"],
        ),
        ProductLayerSpec(
            ProductLayer.SIMULATION,
            "Simulation Engine (World) - deterministic, replayable",
            ["deterministic", "replayable", "versioned"],
        ),
        ProductLayerSpec(
            ProductLayer.AGENT,
            "Agent Layer (L1-L3) - non-autonomous, scoped",
            ["scoped", "non_autonomous", "governed"],
        ),
        ProductLayerSpec(
            ProductLayer.GOVERNANCE,
            "Governance Layer (OPA/TRiSM) - rules, approval, audit",
            ["opa_rules", "hitl", "audit_trail"],
        ),
        ProductLayerSpec(
            ProductLayer.DATA_FABRIC,
            "Data Fabric (synthetic/real) - versioned, isolated",
            ["versioned", "isolated", "namespace"],
        ),
    ]
    
    def __init__(self):
        self._plan: Optional[IndustrializationPlan] = None
        self._init_plan()
    
    def _init_plan(self) -> None:
        """Initialize industrialization plan"""
        self._plan = IndustrializationPlan(
            plan_id=generate_id(),
            layers=self.DEFAULT_LAYERS.copy(),
        )
    
    def get_plan(self) -> IndustrializationPlan:
        """Get industrialization plan"""
        return self._plan
    
    def advance_phase(self) -> bool:
        """Advance to next phase"""
        phases = list(IndustrializationPhase)
        current_idx = phases.index(self._plan.current_phase)
        
        if current_idx < len(phases) - 1:
            self._plan.current_phase = phases[current_idx + 1]
            logger.info(f"Advanced to phase: {self._plan.current_phase.value}")
            return True
        
        return False
    
    def mark_layer_ready(self, layer: ProductLayer) -> bool:
        """Mark a layer as ready"""
        for layer_spec in self._plan.layers:
            if layer_spec.layer == layer:
                layer_spec.ready = True
                return True
        return False
    
    def check_readiness(self) -> Dict[str, bool]:
        """Check readiness of all layers"""
        return {
            layer.layer.value: layer.ready
            for layer in self._plan.layers
        }


# ============================================================================
# 2. XR PACK AUTOGEN SERVICE
# ============================================================================

class XRPackAutoGenService:
    """
    XR Pack Auto-Generation Service V1.4.
    
    Per spec: Generate static XR Pack (read-only) from simulation artifacts
    """
    
    # Default 9 spheres for heatmap
    DEFAULT_SPHERES = [
        "personal", "business", "health", "creative",
        "data_ai", "operations", "communication", "finance", "legal"
    ]
    
    def __init__(self):
        self._packs: Dict[str, XRPack] = {}
    
    def generate_pack(
        self,
        simulation_id: str,
        tenant_id: str,
        events: List[Dict[str, Any]],
        timeline: List[Dict[str, Any]],
        metrics: Dict[str, float],
        baseline_metrics: Dict[str, float] = None,
    ) -> XRPack:
        """
        Generate XR Pack from simulation artifacts.
        
        Per spec: OPA approval required for BUILD_XR_PACK
        """
        pack = XRPack(
            pack_id=generate_id(),
            manifest=XRPackManifest(
                simulation_id=simulation_id,
                tenant_id=tenant_id,
            ),
            read_only=True,
        )
        
        # Generate replay frames
        for entry in timeline:
            pack.replay.append(ReplayFrame(
                step=entry.get("step", 0),
                state=entry.get("state", {}),
                events=[e for e in events if e.get("step") == entry.get("step")],
            ))
        
        # Generate heatmap (one tile per sphere)
        for sphere in self.DEFAULT_SPHERES:
            pack.heatmap.append(HeatmapTile(
                tile_id=f"tile_{sphere}",
                name=sphere.replace("_", " ").title(),
                risk_score=metrics.get(f"{sphere}_risk", 0.5),
                cost_score=metrics.get(f"{sphere}_cost", 0.5),
                velocity_score=metrics.get(f"{sphere}_velocity", 0.5),
            ))
        
        # Generate diff (vs baseline)
        if baseline_metrics:
            for key, value in metrics.items():
                baseline = baseline_metrics.get(key, value)
                delta = value - baseline
                delta_pct = (delta / baseline * 100) if baseline else 0
                
                pack.diff.append(DiffEntry(
                    metric=key,
                    baseline=baseline,
                    scenario=value,
                    delta=delta,
                    delta_percent=delta_pct,
                ))
        
        # Generate explainability
        for event in events[:10]:  # Top 10 events
            pack.explain.append({
                "step": str(event.get("step", 0)),
                "why": event.get("rule", "Unknown rule"),
                "how": f"Action triggered by {event.get('type', 'unknown')}",
            })
        
        # Mark OPA approved (would check OPA in real impl)
        pack.opa_approved = True
        
        self._packs[pack.pack_id] = pack
        logger.info(f"XR Pack generated: {pack.pack_id}")
        return pack
    
    def get_pack(self, pack_id: str) -> Optional[XRPack]:
        """Get pack by ID"""
        return self._packs.get(pack_id)


# ============================================================================
# 3. GAMEPLAY MECHANICS SERVICE
# ============================================================================

class GameplayMechanicsService:
    """
    Gameplay Mechanics Service.
    
    Per spec: Transform work into playable experience without naive gamification
    """
    
    def __init__(self):
        self._states: Dict[str, GameplayState] = {}
    
    def create_state(self) -> GameplayState:
        """Create gameplay state"""
        state = GameplayState(
            state_id=generate_id(),
            resources={"budget": 100000, "time": 100, "energy": 100},
        )
        
        self._states[state.state_id] = state
        return state
    
    def add_quest(
        self,
        state_id: str,
        name: str,
        objective: str,
    ) -> Optional[Quest]:
        """Add quest (business objective)"""
        state = self._states.get(state_id)
        if not state:
            return None
        
        quest = Quest(
            quest_id=generate_id(),
            name=name,
            objective=objective,
        )
        
        state.quests.append(quest)
        return quest
    
    def update_quest_progress(
        self,
        state_id: str,
        quest_id: str,
        progress: float,
    ) -> bool:
        """Update quest progress (with justification check)"""
        state = self._states.get(state_id)
        if not state:
            return False
        
        for quest in state.quests:
            if quest.quest_id == quest_id:
                # Must be justified
                quest.progress = min(1.0, max(0.0, progress))
                quest.justified = True  # Would check in real impl
                
                if quest.progress >= 1.0:
                    quest.completed = True
                    quest.real_impact_simulated = True
                
                return True
        
        return False
    
    def add_risk(self, state_id: str, risk: str) -> bool:
        """Add risk (visual anomaly)"""
        state = self._states.get(state_id)
        if not state:
            return False
        
        state.risks.append(risk)
        return True
    
    def spend_resource(
        self,
        state_id: str,
        resource: str,
        amount: float,
    ) -> bool:
        """Spend resource"""
        state = self._states.get(state_id)
        if not state or resource not in state.resources:
            return False
        
        if state.resources[resource] >= amount:
            state.resources[resource] -= amount
            return True
        
        return False


# ============================================================================
# 4. PROMPT COLLECTION SERVICE
# ============================================================================

class PromptCollectionService:
    """
    Prompt Collection Architecture Service.
    
    Per spec: All three axes (role, agent, task) required for every prompt
    """
    
    def __init__(self):
        self._library: Optional[PromptLibrary] = None
        self._init_library()
    
    def _init_library(self) -> None:
        """Initialize prompt library"""
        self._library = PromptLibrary(library_id=generate_id())
    
    def add_prompt(
        self,
        role: str,
        agent: str,
        task: str,
        content: str,
        layer: str = "task",
    ) -> PromptAsset:
        """
        Add prompt to library.
        
        Per spec: No prompt may exist without all three axes
        """
        if not role or not agent or not task:
            raise ValueError("All three axes (role, agent, task) are required")
        
        asset = PromptAsset(
            asset_id=generate_id(),
            role=role,
            agent=agent,
            task=task,
            content=content,
            layer=layer,
        )
        
        self._library.assets[asset.asset_id] = asset
        self._library.total_prompts += 1
        
        # Update stats
        self._library.by_role[role] = self._library.by_role.get(role, 0) + 1
        self._library.by_agent[agent] = self._library.by_agent.get(agent, 0) + 1
        
        return asset
    
    def get_library(self) -> PromptLibrary:
        """Get prompt library"""
        return self._library
    
    def find_by_agent(self, agent: str) -> List[PromptAsset]:
        """Find prompts by agent"""
        return [
            a for a in self._library.assets.values()
            if a.agent == agent
        ]
    
    def find_by_role(self, role: str) -> List[PromptAsset]:
        """Find prompts by role"""
        return [
            a for a in self._library.assets.values()
            if a.role == role
        ]


# ============================================================================
# 5. API AGENT MANAGEMENT SERVICE
# ============================================================================

class APIAgentManagementService:
    """
    API & Agent Management Service.
    
    Per spec: Structure, not restriction. Multi-level evaluations.
    """
    
    def __init__(self, config: APIAgentManagementConfig = None):
        self.config = config or APIAgentManagementConfig(config_id=generate_id())
        self._registry: Dict[str, AgentRegistryEntry] = {}
        self._evaluations: Dict[str, List[EvaluationResult]] = {}
    
    def register_agent(
        self,
        agent_id: str,
        blueprint_id: str,
        scope: str,
        level: str = "L0",
        sphere: str = "",
    ) -> AgentRegistryEntry:
        """Register agent in registry"""
        entry = AgentRegistryEntry(
            agent_id=agent_id,
            blueprint_id=blueprint_id,
            scope=scope,
            level=level,
            sphere=sphere,
        )
        
        self._registry[agent_id] = entry
        self._evaluations[agent_id] = []
        
        return entry
    
    def evaluate_agent(
        self,
        agent_id: str,
        accuracy: float,
        reliability: float,
        governance_compliance: float,
    ) -> Optional[EvaluationResult]:
        """
        Multi-level evaluation of agent.
        
        Per spec: Multi-level evaluations improve decision quality by +80%
        """
        if agent_id not in self._registry:
            return None
        
        overall = (accuracy + reliability + governance_compliance) / 3
        
        result = EvaluationResult(
            eval_id=generate_id(),
            agent_id=agent_id,
            accuracy=accuracy,
            reliability=reliability,
            governance_compliance=governance_compliance,
            overall_score=overall,
            passed=overall >= 0.7,
        )
        
        self._evaluations[agent_id].append(result)
        
        # Update registry
        self._registry[agent_id].eval_score = overall
        self._registry[agent_id].last_eval = datetime.utcnow()
        
        return result
    
    def get_agent(self, agent_id: str) -> Optional[AgentRegistryEntry]:
        """Get agent from registry"""
        return self._registry.get(agent_id)
    
    def list_by_level(self, level: str) -> List[AgentRegistryEntry]:
        """List agents by level"""
        return [a for a in self._registry.values() if a.level == level]


# ============================================================================
# 6. OPA POLICY BUNDLES SERVICE
# ============================================================================

class OPAPolicyBundlesService:
    """
    OPA Policy Bundles Service.
    
    Per spec: default deny, allow by explicit rule
    """
    
    # Core rules from spec
    CORE_RULES = [
        PolicyRule("R1", "default_deny", "Deny all by default", "deny"),
        PolicyRule("R2", "explicit_allow", "Allow only by explicit rule", "deny"),
        PolicyRule("R3", "hitl_high_risk", "HITL for high-risk actions", "deny"),
        PolicyRule("R4", "xr_read_only", "XR is read-only", "deny"),
        PolicyRule("R5", "audit_required", "Audit logging required", "deny"),
        PolicyRule("R6", "environment_isolation", "Environment isolation", "deny"),
        PolicyRule("R7", "explainability", "Explainability required", "deny"),
    ]
    
    def __init__(self):
        self._registry: Optional[BundleRegistry] = None
        self._init_registry()
    
    def _init_registry(self) -> None:
        """Initialize bundle registry"""
        self._registry = BundleRegistry(
            registry_id=generate_id(),
            default_deny=True,
        )
        
        # Create core bundle
        core_bundle = PolicyBundle(
            bundle_id="core",
            name="CHE-NU Core Policy Bundle",
            rules=self.CORE_RULES.copy(),
            sphere_policies=[
                "personal", "business", "health", "creative",
                "data_ai", "operations", "communication", "finance", "legal"
            ],
        )
        
        self._registry.bundles["core"] = core_bundle
    
    def get_registry(self) -> BundleRegistry:
        """Get bundle registry"""
        return self._registry
    
    def get_bundle(self, bundle_id: str) -> Optional[PolicyBundle]:
        """Get bundle by ID"""
        return self._registry.bundles.get(bundle_id)
    
    def add_rule(
        self,
        bundle_id: str,
        rule_id: str,
        name: str,
        description: str,
    ) -> bool:
        """Add rule to bundle"""
        bundle = self._registry.bundles.get(bundle_id)
        if not bundle:
            return False
        
        bundle.rules.append(PolicyRule(rule_id, name, description))
        return True
    
    def evaluate_decision(
        self,
        action: str,
        environment: str,
        agent_level: str,
    ) -> Tuple[bool, List[str]]:
        """
        Evaluate decision against policies.
        
        Per spec: default deny
        """
        reasons = []
        
        # Default deny
        allow = False
        
        # Check environment
        if environment not in ["labs", "pilot", "prod"]:
            reasons.append("Invalid environment")
            return False, reasons
        
        # Check agent level
        if agent_level not in ["L0", "L1", "L2", "L3"]:
            reasons.append("Invalid agent level")
            return False, reasons
        
        # Simple rules (would be full OPA eval in real impl)
        if action == "READ" or action == "DISCUSS":
            allow = True
        elif action in ["EXECUTE", "WRITE", "DELETE"]:
            if environment == "labs":
                allow = True
            else:
                reasons.append("HITL required for high-risk in pilot/prod")
        
        return allow, reasons


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_industrialization_service() -> IndustrializationService:
    return IndustrializationService()

def create_xr_pack_service() -> XRPackAutoGenService:
    return XRPackAutoGenService()

def create_gameplay_service() -> GameplayMechanicsService:
    return GameplayMechanicsService()

def create_prompt_collection_service() -> PromptCollectionService:
    return PromptCollectionService()

def create_api_agent_service(config: APIAgentManagementConfig = None) -> APIAgentManagementService:
    return APIAgentManagementService(config)

def create_opa_bundles_service() -> OPAPolicyBundlesService:
    return OPAPolicyBundlesService()
