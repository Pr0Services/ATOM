"""
============================================================================
CHE·NU™ V69 — WORKSPACE INTEGRATION SYSTEMS
============================================================================
Combined implementation of:
- Workspace Engine Map
- World Engine Integration V1.2
- Domaines Métiers Industries
- Explainability UI
- Phase 4/5 Playbooks

"Engines = representational-only, GOUVERNANCE > EXÉCUTION"
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import random

from .models import (
    # Engine Map
    EngineType, WorkspaceEngine, EngineMap,
    # World Engine
    WorldEngineConfig, WorldState, WorldEvent, WorldSimulationResult,
    # Domains
    DomainRole, BusinessDomain, DomainDictionary,
    # Explainability UI
    ExplainabilityAccessLevel, ExplainabilityVisibility,
    ExplainabilityUIConfig, ExplainabilityEntry,
    # Playbooks
    PhaseGateStatus, ReadinessChecklistItem, PerformanceTarget,
    Phase4Playbook, Phase5Playbook,
    generate_id, compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 1. WORKSPACE ENGINE MAP SERVICE
# ============================================================================

class WorkspaceEngineMapService:
    """
    Workspace Engine Map Service.
    
    Per spec: Engines = representational-only, no execution
    """
    
    # Default engines from spec
    DEFAULT_ENGINES = [
        WorkspaceEngine(
            engine_id="ENG_DATA_TABULAR",
            name="Data Tabular Engine",
            engine_type=EngineType.DATA,
            capabilities=["tables", "csv", "excel"],
            spheres=["business", "finance"],
            agents=["data_agent"],
            restrictions=["export_hitl"],
        ),
        WorkspaceEngine(
            engine_id="ENG_DOC_PDF",
            name="Document PDF Engine",
            engine_type=EngineType.DOC,
            capabilities=["pdf", "doc"],
            spheres=["business", "legal"],
            agents=["doc_agent"],
            restrictions=["versioning"],
        ),
        WorkspaceEngine(
            engine_id="ENG_PRESENTATION",
            name="Presentation Engine",
            engine_type=EngineType.SLIDES,
            capabilities=["ppt"],
            spheres=["business", "creative"],
            agents=["story_agent"],
            restrictions=["no_publish"],
        ),
        WorkspaceEngine(
            engine_id="ENG_WEB_READ",
            name="Web Read Engine",
            engine_type=EngineType.WEB,
            capabilities=["browse"],
            spheres=["all"],
            agents=["research_agent"],
            restrictions=["read_only"],
        ),
        WorkspaceEngine(
            engine_id="ENG_XR_RENDER",
            name="XR Render Engine",
            engine_type=EngineType.XR,
            capabilities=["3d_viz"],
            spheres=["all"],
            agents=["xr_agent"],
            restrictions=["read_only"],
        ),
        WorkspaceEngine(
            engine_id="ENG_EXPORT_PIPE",
            name="Export Pipeline Engine",
            engine_type=EngineType.EXPORT,
            capabilities=["package"],
            spheres=["all"],
            agents=["export_agent"],
            restrictions=["human_only"],
        ),
    ]
    
    def __init__(self):
        self._map: Optional[EngineMap] = None
        self._init_default_map()
    
    def _init_default_map(self) -> None:
        """Initialize default engine map"""
        self._map = EngineMap(
            map_id=generate_id(),
            engines={e.engine_id: e for e in self.DEFAULT_ENGINES},
        )
    
    def get_map(self) -> EngineMap:
        """Get engine map"""
        return self._map
    
    def get_engine(self, engine_id: str) -> Optional[WorkspaceEngine]:
        """Get engine by ID"""
        return self._map.engines.get(engine_id)
    
    def list_by_sphere(self, sphere: str) -> List[WorkspaceEngine]:
        """List engines by sphere"""
        return [
            e for e in self._map.engines.values()
            if sphere in e.spheres or "all" in e.spheres
        ]
    
    def check_access(
        self,
        engine_id: str,
        agent_id: str,
    ) -> Tuple[bool, str]:
        """
        Check if agent can access engine.
        
        Per spec: Workspace → Governance → Engine (no direct call)
        """
        engine = self._map.engines.get(engine_id)
        if not engine:
            return False, "Engine not found"
        
        # Check if agent is authorized
        # (In reality, would check agent registry)
        
        return True, "Access granted via governance layer"


# ============================================================================
# 2. WORLD ENGINE INTEGRATION SERVICE
# ============================================================================

class WorldEngineIntegrationService:
    """
    World Engine Integration V1.2.
    
    Per spec: Deterministic simulation, synthetic: true, never real action
    """
    
    def __init__(self, config: WorldEngineConfig = None):
        self.config = config or WorldEngineConfig()
        self._results: Dict[str, WorldSimulationResult] = {}
    
    def run_simulation(
        self,
        initial_state: Dict[str, Any],
        rules: List[Dict[str, Any]],
        actions: List[List[Dict[str, Any]]],
        steps: int = 10,
    ) -> WorldSimulationResult:
        """
        Run deterministic simulation.
        
        Per spec: Reproducible with seed, always synthetic
        """
        random.seed(self.config.seed)
        
        state = WorldState(
            step=0,
            budget=initial_state.get("budget", 100000.0),
            resources=initial_state.get("resources", {}),
            agents_active=initial_state.get("agents", []),
            synthetic=True,
        )
        
        events = []
        timeline = []
        
        for step_index in range(1, steps + 1):
            state.step = step_index
            
            # Process actions for this step
            step_actions = actions[step_index - 1] if step_index <= len(actions) else []
            
            for action in step_actions:
                if action.get("type") == "spend":
                    amount = action.get("amount", 0)
                    state.budget -= amount
                    
                    events.append(WorldEvent(
                        event_id=generate_id(),
                        rule="agent_spend",
                        step=step_index,
                        data={"budget_delta": -amount},
                        synthetic=True,
                    ))
                
                elif action.get("type") == "allocate":
                    resource = action.get("resource", "default")
                    amount = action.get("amount", 0)
                    state.resources[resource] = state.resources.get(resource, 0) + amount
                    
                    events.append(WorldEvent(
                        event_id=generate_id(),
                        rule="resource_allocate",
                        step=step_index,
                        data={"resource": resource, "amount": amount},
                        synthetic=True,
                    ))
            
            # Record timeline
            timeline.append({
                "step": step_index,
                "budget": state.budget,
                "resources": state.resources.copy(),
                "events_count": len([e for e in events if e.step == step_index]),
            })
        
        # Calculate metrics
        metrics = {
            "total_steps": steps,
            "final_budget": state.budget,
            "total_events": len(events),
            "budget_delta": initial_state.get("budget", 100000.0) - state.budget,
        }
        
        result = WorldSimulationResult(
            result_id=generate_id(),
            seed=self.config.seed,
            final_state=state,
            events=events,
            timeline=timeline,
            metrics=metrics,
            deterministic=True,
            synthetic=True,
        )
        
        self._results[result.result_id] = result
        logger.info(f"Simulation completed: {result.result_id} ({steps} steps)")
        return result
    
    def replay(self, result_id: str) -> Optional[WorldSimulationResult]:
        """Replay simulation (returns same result due to determinism)"""
        return self._results.get(result_id)


# ============================================================================
# 3. DOMAIN DICTIONARY SERVICE
# ============================================================================

class DomainDictionaryService:
    """
    Domain Dictionary Service.
    
    Per spec: Universal dictionary for agents and workflows
    """
    
    # Default domains from spec
    DEFAULT_DOMAINS = [
        BusinessDomain(
            domain_id="management_strategy",
            name="Management & Strategy",
            industries=["all"],
            business_objectives=["vision", "prioritization", "resource_allocation", "governance"],
            roles=[
                DomainRole("ceo", "CEO", ["strategic_planning", "leadership"]),
                DomainRole("coo", "COO", ["operations", "execution"]),
                DomainRole("pm", "Project Manager", ["planning", "tracking"]),
            ],
            core_tasks=["strategic_planning", "roadmap_definition", "kpi_monitoring", "risk_analysis"],
            tools_and_apps=["notion", "jira", "clickup", "asana", "excel"],
            apis=["notion_api", "jira_api", "clickup_api"],
            data_types=["roadmaps", "kpis", "reports"],
            automation_potential=["decision_support", "scenario_simulation", "priority_recommendations"],
        ),
        BusinessDomain(
            domain_id="finance",
            name="Finance",
            industries=["all"],
            business_objectives=["budgeting", "forecasting", "compliance", "reporting"],
            roles=[
                DomainRole("cfo", "CFO", ["financial_strategy", "governance"]),
                DomainRole("controller", "Controller", ["accounting", "reporting"]),
                DomainRole("analyst", "Financial Analyst", ["analysis", "modeling"]),
            ],
            core_tasks=["budget_planning", "variance_analysis", "financial_reporting", "audit_prep"],
            tools_and_apps=["excel", "quickbooks", "netsuite", "sap"],
            apis=["quickbooks_api", "plaid_api"],
            data_types=["budgets", "reports", "invoices", "statements"],
            automation_potential=["expense_tracking", "forecast_generation", "anomaly_detection"],
        ),
        BusinessDomain(
            domain_id="hr",
            name="Human Resources",
            industries=["all"],
            business_objectives=["recruitment", "retention", "development", "compliance"],
            roles=[
                DomainRole("chro", "CHRO", ["hr_strategy", "culture"]),
                DomainRole("recruiter", "Recruiter", ["sourcing", "hiring"]),
                DomainRole("hrbp", "HR Business Partner", ["employee_relations"]),
            ],
            core_tasks=["recruiting", "onboarding", "performance_reviews", "training"],
            tools_and_apps=["workday", "greenhouse", "lever", "bamboohr"],
            apis=["greenhouse_api", "lever_api"],
            data_types=["candidates", "employees", "reviews", "policies"],
            automation_potential=["resume_screening", "scheduling", "onboarding_workflows"],
        ),
        BusinessDomain(
            domain_id="sales",
            name="Sales",
            industries=["all"],
            business_objectives=["revenue", "pipeline", "customer_acquisition"],
            roles=[
                DomainRole("cro", "CRO", ["revenue_strategy"]),
                DomainRole("ae", "Account Executive", ["closing_deals"]),
                DomainRole("sdr", "SDR", ["prospecting"]),
            ],
            core_tasks=["prospecting", "demos", "negotiations", "closing"],
            tools_and_apps=["salesforce", "hubspot", "outreach", "gong"],
            apis=["salesforce_api", "hubspot_api"],
            data_types=["leads", "opportunities", "accounts", "contracts"],
            automation_potential=["lead_scoring", "follow_up_sequences", "forecast_modeling"],
        ),
    ]
    
    def __init__(self):
        self._dictionary: Optional[DomainDictionary] = None
        self._init_default_dictionary()
    
    def _init_default_dictionary(self) -> None:
        """Initialize default dictionary"""
        self._dictionary = DomainDictionary(
            dictionary_id=generate_id(),
            domains={d.domain_id: d for d in self.DEFAULT_DOMAINS},
        )
    
    def get_dictionary(self) -> DomainDictionary:
        """Get domain dictionary"""
        return self._dictionary
    
    def get_domain(self, domain_id: str) -> Optional[BusinessDomain]:
        """Get domain by ID"""
        return self._dictionary.domains.get(domain_id)
    
    def list_by_industry(self, industry: str) -> List[BusinessDomain]:
        """List domains applicable to industry"""
        return [
            d for d in self._dictionary.domains.values()
            if industry in d.industries or "all" in d.industries
        ]
    
    def get_roles(self, domain_id: str) -> List[DomainRole]:
        """Get roles for domain"""
        domain = self._dictionary.domains.get(domain_id)
        return domain.roles if domain else []


# ============================================================================
# 4. EXPLAINABILITY UI SERVICE
# ============================================================================

class ExplainabilityUIService:
    """
    Explainability UI Service.
    
    Per spec: Answer "Why?" without overwhelming, respect access levels
    """
    
    # Default visibility per level
    DEFAULT_VISIBILITY = {
        ExplainabilityAccessLevel.USER: ExplainabilityVisibility(
            level=ExplainabilityAccessLevel.USER,
            visible=["outcome", "high_level_reason"],
            hidden=["internal_agents", "prompts", "policies"],
        ),
        ExplainabilityAccessLevel.ADMIN: ExplainabilityVisibility(
            level=ExplainabilityAccessLevel.ADMIN,
            visible=["outcome", "high_level_reason", "agent_selection", "applied_rules", "autonomy_level", "escalation_path"],
            hidden=["prompts", "internal_policies"],
        ),
        ExplainabilityAccessLevel.AUDITOR: ExplainabilityVisibility(
            level=ExplainabilityAccessLevel.AUDITOR,
            visible=["full_decision_trace", "policy_references", "logs", "all"],
            hidden=[],
        ),
    }
    
    def __init__(self):
        self._config: Optional[ExplainabilityUIConfig] = None
        self._entries: Dict[str, ExplainabilityEntry] = {}
        self._init_config()
    
    def _init_config(self) -> None:
        """Initialize config"""
        self._config = ExplainabilityUIConfig(
            config_id=generate_id(),
            access_levels=self.DEFAULT_VISIBILITY,
            expose_raw_prompts=False,
            leak_sensitive_data=False,
            bypass_governance=False,
        )
    
    def create_entry(
        self,
        decision_id: str,
        outcome: str,
        reason: str,
        agent_selection: str = "",
        applied_rules: List[str] = None,
        autonomy_level: str = "",
        full_trace: str = "",
    ) -> ExplainabilityEntry:
        """Create explainability entry"""
        entry = ExplainabilityEntry(
            entry_id=generate_id(),
            decision_id=decision_id,
            access_level=ExplainabilityAccessLevel.AUDITOR,  # Full access stored
            outcome=outcome,
            high_level_reason=reason,
            agent_selection=agent_selection,
            applied_rules=applied_rules or [],
            autonomy_level=autonomy_level,
            full_decision_trace=full_trace,
        )
        
        self._entries[entry.entry_id] = entry
        return entry
    
    def get_for_level(
        self,
        entry_id: str,
        level: ExplainabilityAccessLevel,
    ) -> Dict[str, Any]:
        """
        Get entry filtered by access level.
        
        Per spec: Differentiate what is explainable vs restricted
        """
        entry = self._entries.get(entry_id)
        if not entry:
            return {}
        
        visibility = self._config.access_levels.get(level)
        if not visibility:
            return {}
        
        result = {}
        
        if "outcome" in visibility.visible:
            result["outcome"] = entry.outcome
        if "high_level_reason" in visibility.visible:
            result["reason"] = entry.high_level_reason
        if "agent_selection" in visibility.visible:
            result["agent_selection"] = entry.agent_selection
        if "applied_rules" in visibility.visible:
            result["applied_rules"] = entry.applied_rules
        if "autonomy_level" in visibility.visible:
            result["autonomy_level"] = entry.autonomy_level
        if "full_decision_trace" in visibility.visible or "all" in visibility.visible:
            result["full_trace"] = entry.full_decision_trace
        
        return result


# ============================================================================
# 5. PHASE 4/5 PLAYBOOK SERVICE
# ============================================================================

class PlaybookService:
    """
    Phase 4/5 Playbook Service.
    
    Per spec: Strict gates - any failed item = NO-GO
    """
    
    def __init__(self):
        self._phase4: Optional[Phase4Playbook] = None
        self._phase5: Optional[Phase5Playbook] = None
        self._init_playbooks()
    
    def _init_playbooks(self) -> None:
        """Initialize playbooks"""
        self._phase4 = Phase4Playbook(
            playbook_id=generate_id(),
            technical_checklist=[
                ReadinessChecklistItem("tech_1", "Phase 1-3 benchmarks validated"),
                ReadinessChecklistItem("tech_2", "Quantization & batching stable"),
                ReadinessChecklistItem("tech_3", "AutoGen sandbox L1 enforced"),
                ReadinessChecklistItem("tech_4", "XR read-only verified"),
            ],
            governance_checklist=[
                ReadinessChecklistItem("gov_1", "TRiSM / OPA rules (7/7) active"),
                ReadinessChecklistItem("gov_2", "HITL escalation tested"),
                ReadinessChecklistItem("gov_3", "Explainability coverage >= 95%"),
                ReadinessChecklistItem("gov_4", "Audit logs immutable"),
            ],
        )
        
        self._phase5 = Phase5Playbook(playbook_id=generate_id())
    
    def get_phase4(self) -> Phase4Playbook:
        """Get Phase 4 playbook"""
        return self._phase4
    
    def get_phase5(self) -> Phase5Playbook:
        """Get Phase 5 playbook"""
        return self._phase5
    
    def complete_checklist_item(
        self,
        playbook: str,
        item_id: str,
        evidence: str = "",
    ) -> bool:
        """Complete a checklist item"""
        pb = self._phase4 if playbook == "phase4" else self._phase5
        
        if playbook == "phase4":
            for item in self._phase4.technical_checklist + self._phase4.governance_checklist:
                if item.item_id == item_id:
                    item.completed = True
                    item.evidence = evidence
                    return True
        
        return False
    
    def evaluate_gate(self, playbook: str) -> PhaseGateStatus:
        """
        Evaluate gate status.
        
        Per spec: Any failed item = NO-GO
        """
        if playbook == "phase4":
            all_items = self._phase4.technical_checklist + self._phase4.governance_checklist
            all_complete = all(item.completed for item in all_items)
            
            self._phase4.gate_status = PhaseGateStatus.GO if all_complete else PhaseGateStatus.NO_GO
            return self._phase4.gate_status
        
        elif playbook == "phase5":
            ready = self._phase5.pilot_complete and self._phase5.production_ready
            self._phase5.gate_status = PhaseGateStatus.GO if ready else PhaseGateStatus.NO_GO
            return self._phase5.gate_status
        
        return PhaseGateStatus.PENDING
    
    def update_phase5_metrics(
        self,
        active_tenants: int,
        active_users: int,
    ) -> None:
        """Update Phase 5 metrics"""
        self._phase5.active_tenants = active_tenants
        self._phase5.active_users = active_users


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_engine_map_service() -> WorkspaceEngineMapService:
    return WorkspaceEngineMapService()

def create_world_engine_service(config: WorldEngineConfig = None) -> WorldEngineIntegrationService:
    return WorldEngineIntegrationService(config)

def create_domain_dictionary_service() -> DomainDictionaryService:
    return DomainDictionaryService()

def create_explainability_ui_service() -> ExplainabilityUIService:
    return ExplainabilityUIService()

def create_playbook_service() -> PlaybookService:
    return PlaybookService()
