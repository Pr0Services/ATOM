"""
============================================================================
CHE·NU™ V69 — LABS FINAL SYSTEMS
============================================================================
Combined implementation of:
- LABS Chapter 1 (Innovation Track)
- Workspace Agent Roles
- XR Pack V1.5 (Real Diff + Signed ZIP)
- XR Pack V1.6 (Chunked Replay + Ed25519)
- V52 Adoption Upgrade Plan

"Execution builds the product. LABS builds the future."
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import hashlib
import json
import base64

from .models import (
    # LABS Chapter 1
    LABSDomain, TaskStatus, LivingTask, LABSFeature, LABSInnovationTrack,
    # Workspace Agent Roles
    AgentCategory, AgentCapability, AgentRestriction,
    WorkspaceAgentRole, WorkspaceAgentRegistry,
    # XR Pack V1.5
    MetricsDelta, ComputedHeatmapTile, PackSignature, XRPackV15,
    # XR Pack V1.6
    DivergencePoint, DivergenceConfig, ReplayChunk, ReplayIndex,
    Ed25519Signature, XRPackV16,
    # Adoption Upgrade Plan
    UpgradePhase, UpgradeTask, PerformanceBaseline, PerformanceTarget,
    AdoptionUpgradePlan,
    generate_id, compute_hash,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 1. LABS INNOVATION TRACK SERVICE
# ============================================================================

class LABSInnovationService:
    """
    LABS Innovation Track Service.
    
    Per spec: Parallel innovation track, isolated from PROD
    """
    
    # Default features per domain
    DEFAULT_FEATURES = {
        LABSDomain.META_ROADMAP: [
            LABSFeature("A1", LABSDomain.META_ROADMAP, "Living Task Objects",
                       "Tasks as first-class computable objects"),
            LABSFeature("A2", LABSDomain.META_ROADMAP, "Dependency Graph",
                       "Real-time dependency visualization"),
        ],
        LABSDomain.COGNITIVE_LOAD: [
            LABSFeature("B1", LABSDomain.COGNITIVE_LOAD, "Load Estimation",
                       "Nova estimates cognitive load per task"),
            LABSFeature("B2", LABSDomain.COGNITIVE_LOAD, "Context Switching",
                       "Minimize context switches for humans"),
        ],
        LABSDomain.AGENT_EVOLUTION: [
            LABSFeature("C1", LABSDomain.AGENT_EVOLUTION, "Performance Tracking",
                       "Track agent performance over time"),
            LABSFeature("C2", LABSDomain.AGENT_EVOLUTION, "Trust Score",
                       "Evolving trust based on outcomes"),
        ],
        LABSDomain.GOVERNANCE_INTEL: [
            LABSFeature("D1", LABSDomain.GOVERNANCE_INTEL, "Predictive Rules",
                       "Predict governance violations before they happen"),
            LABSFeature("D2", LABSDomain.GOVERNANCE_INTEL, "Explainable Policies",
                       "Natural language policy explanations"),
        ],
        LABSDomain.XR_DECISION: [
            LABSFeature("E1", LABSDomain.XR_DECISION, "Decision Visualization",
                       "XR for understanding decisions, not spectacle"),
            LABSFeature("E2", LABSDomain.XR_DECISION, "What-If Explorer",
                       "Interactive scenario exploration in XR"),
        ],
    }
    
    def __init__(self):
        self._track: Optional[LABSInnovationTrack] = None
        self._init_track()
    
    def _init_track(self) -> None:
        """Initialize innovation track"""
        self._track = LABSInnovationTrack(
            track_id=generate_id(),
            domains=self.DEFAULT_FEATURES.copy(),
        )
    
    def get_track(self) -> LABSInnovationTrack:
        """Get innovation track"""
        return self._track
    
    def add_task(
        self,
        task_id: str,
        phase: str,
        agent_owner: str,
        estimated_time: float = 0.0,
    ) -> LivingTask:
        """Add living task"""
        task = LivingTask(
            task_id=task_id,
            phase=phase,
            agent_owner=agent_owner,
            estimated_time=estimated_time,
        )
        
        self._track.tasks[task_id] = task
        return task
    
    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        real_time: float = 0.0,
    ) -> bool:
        """Update task status"""
        task = self._track.tasks.get(task_id)
        if not task:
            return False
        
        task.status = status
        if real_time > 0:
            task.real_time = real_time
        
        return True
    
    def graduate_feature(
        self,
        feature_id: str,
        nova_approved: bool,
        governance_approved: bool,
    ) -> bool:
        """
        Graduate feature from LABS to PROD.
        
        Per spec: Requires Nova + Governance approval
        """
        for domain, features in self._track.domains.items():
            for feature in features:
                if feature.feature_id == feature_id:
                    feature.nova_approved = nova_approved
                    feature.governance_approved = governance_approved
                    
                    if nova_approved and governance_approved:
                        feature.graduated_to_prod = True
                        logger.info(f"Feature graduated: {feature_id}")
                    
                    return True
        
        return False


# ============================================================================
# 2. WORKSPACE AGENT ROLES SERVICE
# ============================================================================

class WorkspaceAgentRolesService:
    """
    Workspace Agent Roles Service.
    
    Per spec: Human is always the commit point
    """
    
    # Default roles
    DEFAULT_ROLES = [
        WorkspaceAgentRole(
            "data_structuring", "Data Structuring Agent",
            AgentCategory.STRUCTURATION,
            "Transform raw data into exploitable structures",
            engines=["ENG_DATA_TABULAR", "ENG_TEXT_STRUCT"],
            capabilities=[AgentCapability.OBSERVE, AgentCapability.STRUCTURE, AgentCapability.PROPOSE],
            restrictions=[AgentRestriction.EXPORT, AgentRestriction.DECIDE],
        ),
        WorkspaceAgentRole(
            "writing_formatting", "Writing / Formatting Agent",
            AgentCategory.STRUCTURATION,
            "Structure texts, titles, sections",
            engines=["ENG_TEXT_STRUCT"],
            capabilities=[AgentCapability.STRUCTURE, AgentCapability.PROPOSE],
            restrictions=[AgentRestriction.PUBLISH, AgentRestriction.DECIDE],
        ),
        WorkspaceAgentRole(
            "analysis", "Analysis Agent",
            AgentCategory.ANALYSIS,
            "Analyze data and provide insights",
            engines=["ENG_DATA_TABULAR", "ENG_DATA_VIZ"],
            capabilities=[AgentCapability.OBSERVE, AgentCapability.ANALYZE, AgentCapability.PROPOSE],
            restrictions=[AgentRestriction.EXPORT, AgentRestriction.DECIDE],
        ),
        WorkspaceAgentRole(
            "creative", "Creative Agent",
            AgentCategory.CREATIVE,
            "Generate creative content",
            engines=["ENG_IMAGE_EDIT", "ENG_PRESENTATION"],
            capabilities=[AgentCapability.PROPOSE, AgentCapability.STRUCTURE],
            restrictions=[AgentRestriction.PUBLISH, AgentRestriction.DECIDE],
        ),
        WorkspaceAgentRole(
            "conformity", "Conformity Agent",
            AgentCategory.CONFORMITY,
            "Check compliance with rules and standards",
            engines=["ENG_TEXT_STRUCT"],
            capabilities=[AgentCapability.OBSERVE, AgentCapability.ANALYZE],
            restrictions=[AgentRestriction.DECIDE, AgentRestriction.EXPORT],
        ),
        WorkspaceAgentRole(
            "validation", "Validation Agent",
            AgentCategory.VALIDATION,
            "Validate outputs before human review",
            engines=["ENG_TEXT_STRUCT", "ENG_DATA_TABULAR"],
            capabilities=[AgentCapability.OBSERVE, AgentCapability.ANALYZE],
            restrictions=[AgentRestriction.DECIDE, AgentRestriction.PUBLISH],
        ),
        WorkspaceAgentRole(
            "xr_viz", "XR Visualization Agent",
            AgentCategory.XR_VIZ,
            "Prepare data for XR visualization (read-only)",
            engines=["ENG_XR_RENDER"],
            capabilities=[AgentCapability.OBSERVE, AgentCapability.STRUCTURE],
            restrictions=[AgentRestriction.CLICK, AgentRestriction.DECIDE, AgentRestriction.EXPORT],
        ),
    ]
    
    def __init__(self):
        self._registry: Optional[WorkspaceAgentRegistry] = None
        self._init_registry()
    
    def _init_registry(self) -> None:
        """Initialize registry"""
        self._registry = WorkspaceAgentRegistry(
            registry_id=generate_id(),
            roles={r.role_id: r for r in self.DEFAULT_ROLES},
        )
    
    def get_registry(self) -> WorkspaceAgentRegistry:
        """Get registry"""
        return self._registry
    
    def get_role(self, role_id: str) -> Optional[WorkspaceAgentRole]:
        """Get role by ID"""
        return self._registry.roles.get(role_id)
    
    def list_by_category(self, category: AgentCategory) -> List[WorkspaceAgentRole]:
        """List roles by category"""
        return [r for r in self._registry.roles.values() if r.category == category]
    
    def can_agent_do(self, role_id: str, action: str) -> Tuple[bool, str]:
        """
        Check if agent can perform action.
        
        Per spec: Agents observe, analyze, propose, structure - never decide
        """
        role = self._registry.roles.get(role_id)
        if not role:
            return False, "Role not found"
        
        # Check restrictions
        for restriction in role.restrictions:
            if restriction.value.lower() == action.lower():
                return False, f"Action '{action}' is restricted for this role"
        
        return True, "Action allowed"


# ============================================================================
# 3. XR PACK V1.5 SERVICE
# ============================================================================

class XRPackV15Service:
    """
    XR Pack V1.5 Service.
    
    Per spec: Real diff, computed heatmap, signed ZIP
    """
    
    SPHERES = [
        "personal", "business", "health", "creative",
        "data_ai", "operations", "communication", "finance", "legal"
    ]
    
    def __init__(self):
        self._packs: Dict[str, XRPackV15] = {}
    
    def compute_diff(
        self,
        baseline_metrics: Dict[str, float],
        scenario_metrics: Dict[str, float],
    ) -> List[MetricsDelta]:
        """Compute real diff between baseline and scenario"""
        deltas = []
        
        for metric, scenario_val in scenario_metrics.items():
            baseline_val = baseline_metrics.get(metric, scenario_val)
            delta = scenario_val - baseline_val
            delta_pct = (delta / baseline_val * 100) if baseline_val else 0
            
            deltas.append(MetricsDelta(
                metric=metric,
                baseline_value=baseline_val,
                scenario_value=scenario_val,
                delta=delta,
                delta_percent=delta_pct,
            ))
        
        return deltas
    
    def compute_heatmap(
        self,
        signals: Dict[str, Dict[str, float]],
    ) -> List[ComputedHeatmapTile]:
        """Compute heatmap from signals"""
        tiles = []
        
        for sphere in self.SPHERES:
            sphere_signals = signals.get(sphere, {})
            
            budget = sphere_signals.get("budget", 0.5)
            risk = sphere_signals.get("risk", 0.5)
            velocity = sphere_signals.get("velocity", 0.5)
            events = int(sphere_signals.get("events", 0))
            
            # Compute heat score (weighted average)
            heat = (budget * 0.3 + risk * 0.4 + velocity * 0.2 + min(events / 10, 1) * 0.1)
            
            tiles.append(ComputedHeatmapTile(
                sphere=sphere,
                budget_signal=budget,
                risk_signal=risk,
                velocity_signal=velocity,
                events_count=events,
                heat_score=heat,
            ))
        
        return tiles
    
    def sign_pack(
        self,
        pack: XRPackV15,
        signer: str = "system",
    ) -> PackSignature:
        """Sign pack with SHA256"""
        # Create data to sign
        data = {
            "pack_id": pack.pack_id,
            "version": pack.version,
            "checksums": pack.checksums,
        }
        
        hash_value = compute_hash(data)
        
        signature = PackSignature(
            algorithm="sha256",
            hash_value=hash_value,
            signer=signer,
        )
        
        pack.signature = signature
        return signature
    
    def build_pack(
        self,
        simulation_id: str,
        baseline_metrics: Dict[str, float],
        scenario_metrics: Dict[str, float],
        signals: Dict[str, Dict[str, float]],
        replay_data: List[Dict[str, Any]] = None,
        explain_data: List[Dict[str, str]] = None,
    ) -> XRPackV15:
        """
        Build XR Pack V1.5.
        
        Per spec: OPA actions BUILD_XR_PACK, ZIP_XR_PACK, SIGN_XR_PACK
        """
        pack = XRPackV15(
            pack_id=generate_id(),
            manifest={
                "simulation_id": simulation_id,
                "version": "1.5",
                "created_at": datetime.utcnow().isoformat(),
            },
        )
        
        # Compute diff
        pack.diff = self.compute_diff(baseline_metrics, scenario_metrics)
        
        # Compute heatmap
        pack.heatmap = self.compute_heatmap(signals)
        
        # Add replay and explain
        pack.replay = replay_data or []
        pack.explain = explain_data or []
        
        # Compute checksums
        pack.checksums = {
            "diff": compute_hash(pack.diff),
            "heatmap": compute_hash(pack.heatmap),
            "replay": compute_hash(pack.replay),
            "explain": compute_hash(pack.explain),
        }
        
        # Sign
        self.sign_pack(pack)
        
        self._packs[pack.pack_id] = pack
        logger.info(f"XR Pack V1.5 built: {pack.pack_id}")
        return pack


# ============================================================================
# 4. XR PACK V1.6 SERVICE
# ============================================================================

class XRPackV16Service:
    """
    XR Pack V1.6 Service.
    
    Per spec: Scalable enterprise - divergence, chunked replay, Ed25519
    """
    
    def __init__(self, chunk_size: int = 100):
        self.chunk_size = chunk_size
        self._packs: Dict[str, XRPackV16] = {}
    
    def detect_divergence(
        self,
        baseline_timeline: List[Dict[str, Any]],
        scenario_timeline: List[Dict[str, Any]],
        config: DivergenceConfig = None,
    ) -> List[DivergencePoint]:
        """
        Detect divergence points.
        
        Per spec: Steps where |delta(state)| exceeds threshold
        """
        config = config or DivergenceConfig()
        points = []
        
        for i, (base, scen) in enumerate(zip(baseline_timeline, scenario_timeline)):
            step = base.get("step", i)
            
            # Check budget
            base_budget = base.get("budget", 0)
            scen_budget = scen.get("budget", 0)
            if abs(scen_budget - base_budget) > config.budget_threshold:
                points.append(DivergencePoint(
                    step=step,
                    metric="budget",
                    baseline_value=base_budget,
                    scenario_value=scen_budget,
                    delta=scen_budget - base_budget,
                    reason="Budget threshold exceeded",
                    impact="Significant financial divergence",
                ))
            
            # Check risk
            base_risk = base.get("risk", 0)
            scen_risk = scen.get("risk", 0)
            if abs(scen_risk - base_risk) > config.risk_threshold:
                points.append(DivergencePoint(
                    step=step,
                    metric="risk",
                    baseline_value=base_risk,
                    scenario_value=scen_risk,
                    delta=scen_risk - base_risk,
                    reason="Risk threshold exceeded",
                    impact="Risk profile changed significantly",
                ))
        
        return points
    
    def chunk_replay(
        self,
        replay_data: List[Dict[str, Any]],
    ) -> Tuple[ReplayIndex, List[ReplayChunk]]:
        """Chunk replay data for pagination"""
        chunks = []
        total_steps = len(replay_data)
        
        for i in range(0, total_steps, self.chunk_size):
            chunk_data = replay_data[i:i + self.chunk_size]
            
            chunk = ReplayChunk(
                chunk_id=generate_id(),
                chunk_index=len(chunks),
                start_step=i,
                end_step=min(i + self.chunk_size, total_steps) - 1,
                frames=chunk_data,
            )
            
            chunks.append(chunk)
        
        index = ReplayIndex(
            total_chunks=len(chunks),
            chunk_size=self.chunk_size,
            total_steps=total_steps,
            chunks=[f"chunk_{c.chunk_index:04d}.v1.json" for c in chunks],
        )
        
        return index, chunks
    
    def sign_ed25519(
        self,
        pack: XRPackV16,
    ) -> Ed25519Signature:
        """
        Sign with Ed25519 (mock - real impl would use cryptography lib).
        
        Per spec: Private key server-side, public key in pack
        """
        # Mock Ed25519 - in real impl would use nacl/cryptography
        data = json.dumps({
            "pack_id": pack.pack_id,
            "version": pack.version,
            "timestamp": datetime.utcnow().isoformat(),
        }, sort_keys=True)
        
        # Mock signature
        signature_bytes = hashlib.sha512(data.encode()).digest()
        signature_b64 = base64.b64encode(signature_bytes).decode()[:64]
        
        # Mock public key
        public_key = "ed25519_pub_" + generate_id()[:16]
        
        sig = Ed25519Signature(
            public_key=public_key,
            signature=signature_b64,
        )
        
        pack.ed25519_signature = sig
        return sig
    
    def build_pack(
        self,
        simulation_id: str,
        baseline_timeline: List[Dict[str, Any]],
        scenario_timeline: List[Dict[str, Any]],
        replay_data: List[Dict[str, Any]],
        heatmap_data: List[ComputedHeatmapTile] = None,
    ) -> XRPackV16:
        """
        Build XR Pack V1.6.
        
        Per spec: OPA gate before build/zip/sign
        """
        pack = XRPackV16(
            pack_id=generate_id(),
            manifest={
                "simulation_id": simulation_id,
                "version": "1.6",
                "replay_mode": "chunked",
                "chunk_size": self.chunk_size,
                "created_at": datetime.utcnow().isoformat(),
            },
        )
        
        # Detect divergence
        pack.divergence_points = self.detect_divergence(
            baseline_timeline, scenario_timeline
        )
        
        # Chunk replay
        pack.replay_index, pack.chunks = self.chunk_replay(replay_data)
        
        # Add heatmap
        pack.heatmap = heatmap_data or []
        
        # Generate sparklines (mini timeseries per sphere)
        for tile in pack.heatmap:
            pack.sparklines[tile.sphere] = [
                tile.heat_score * (0.9 + 0.2 * (i % 3) / 3)
                for i in range(10)
            ]
        
        # Sign with Ed25519
        self.sign_ed25519(pack)
        
        # Generate ETag for caching
        pack.etag = compute_hash(pack.pack_id + str(datetime.utcnow()))[:16]
        pack.cache_hints = {
            "max_age": "3600",
            "cdn_ready": "true",
        }
        
        self._packs[pack.pack_id] = pack
        logger.info(f"XR Pack V1.6 built: {pack.pack_id}")
        return pack


# ============================================================================
# 5. ADOPTION UPGRADE PLAN SERVICE
# ============================================================================

class AdoptionUpgradePlanService:
    """
    V52 Adoption & Upgrade Plan Service.
    
    Per spec: Without violating frozen architecture
    """
    
    # Default tasks per phase
    DEFAULT_TASKS = {
        UpgradePhase.PHASE_1: [
            UpgradeTask("T1.1", UpgradePhase.PHASE_1, "Measure latency (p50/p95/p99)"),
            UpgradeTask("T1.2", UpgradePhase.PHASE_1, "Identify bottlenecks"),
            UpgradeTask("T1.3", UpgradePhase.PHASE_1, "Measure error rates"),
        ],
        UpgradePhase.PHASE_2: [
            UpgradeTask("T2.1", UpgradePhase.PHASE_2, "Integrate AutoGen (LABS only)"),
            UpgradeTask("T2.2", UpgradePhase.PHASE_2, "Define HITL points"),
            UpgradeTask("T2.3", UpgradePhase.PHASE_2, "Implement Nova escalation"),
        ],
        UpgradePhase.PHASE_3: [
            UpgradeTask("T3.1", UpgradePhase.PHASE_3, "Implement quantization"),
            UpgradeTask("T3.2", UpgradePhase.PHASE_3, "Dynamic batching"),
            UpgradeTask("T3.3", UpgradePhase.PHASE_3, "Verify non-regression"),
        ],
        UpgradePhase.PHASE_4: [
            UpgradeTask("T4.1", UpgradePhase.PHASE_4, "Verify OPA rules (7/7)"),
            UpgradeTask("T4.2", UpgradePhase.PHASE_4, "Test HITL escalation"),
            UpgradeTask("T4.3", UpgradePhase.PHASE_4, "Verify audit trails"),
        ],
        UpgradePhase.PHASE_5: [
            UpgradeTask("T5.1", UpgradePhase.PHASE_5, "Pilot rollout"),
            UpgradeTask("T5.2", UpgradePhase.PHASE_5, "Monitor 70K users"),
            UpgradeTask("T5.3", UpgradePhase.PHASE_5, "Final validation"),
        ],
    }
    
    def __init__(self):
        self._plan: Optional[AdoptionUpgradePlan] = None
        self._init_plan()
    
    def _init_plan(self) -> None:
        """Initialize plan"""
        self._plan = AdoptionUpgradePlan(
            plan_id=generate_id(),
            tasks=self.DEFAULT_TASKS.copy(),
        )
    
    def get_plan(self) -> AdoptionUpgradePlan:
        """Get plan"""
        return self._plan
    
    def set_baseline(
        self,
        latency_p50: float,
        latency_p95: float,
        latency_p99: float,
        error_rate: float,
        bottlenecks: List[str] = None,
    ) -> PerformanceBaseline:
        """Set performance baseline"""
        baseline = PerformanceBaseline(
            latency_p50=latency_p50,
            latency_p95=latency_p95,
            latency_p99=latency_p99,
            error_rate=error_rate,
            bottlenecks=bottlenecks or [],
        )
        
        self._plan.baseline = baseline
        return baseline
    
    def complete_task(
        self,
        task_id: str,
        evidence: str = "",
    ) -> bool:
        """Complete a task"""
        for phase, tasks in self._plan.tasks.items():
            for task in tasks:
                if task.task_id == task_id:
                    task.completed = True
                    task.evidence = evidence
                    return True
        
        return False
    
    def advance_phase(self) -> bool:
        """Advance to next phase if current is complete"""
        phases = list(UpgradePhase)
        current_idx = phases.index(self._plan.current_phase)
        
        # Check if current phase tasks are complete
        current_tasks = self._plan.tasks.get(self._plan.current_phase, [])
        if not all(t.completed for t in current_tasks):
            return False
        
        # Advance
        if current_idx < len(phases) - 1:
            self._plan.current_phase = phases[current_idx + 1]
            logger.info(f"Advanced to phase: {self._plan.current_phase.value}")
            return True
        
        return False
    
    def check_compliance(self) -> Dict[str, bool]:
        """Check frozen architecture compliance"""
        return {
            "humans_over_automation": self._plan.humans_over_automation,
            "nova_is_authority": self._plan.nova_is_authority,
            "agents_user_hired": self._plan.agents_user_hired,
            "engines_representational_only": self._plan.engines_representational_only,
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_labs_innovation_service() -> LABSInnovationService:
    return LABSInnovationService()

def create_workspace_roles_service() -> WorkspaceAgentRolesService:
    return WorkspaceAgentRolesService()

def create_xr_pack_v15_service() -> XRPackV15Service:
    return XRPackV15Service()

def create_xr_pack_v16_service(chunk_size: int = 100) -> XRPackV16Service:
    return XRPackV16Service(chunk_size)

def create_adoption_upgrade_service() -> AdoptionUpgradePlanService:
    return AdoptionUpgradePlanService()
