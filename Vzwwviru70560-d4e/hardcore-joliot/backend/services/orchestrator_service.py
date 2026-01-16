"""
SERVICE: orchestrator_service.py
SPHERE: CORE (cross-sphere)
VERSION: 1.0.0
INTENT: AT-OM Orchestrator implementing QCT, SES, RDC algorithms

DEPENDENCIES:
- Core: thread_service, event_service
- External: None

R&D COMPLIANCE: ✅
- Rule #1: Human Sovereignty - ASK_HUMAN decision requires checkpoint
- Rule #2: Autonomy Isolation - All decisions are recommendations
- Rule #6: Traceability - All decisions logged as events
- Rule #7: R&D Continuity - Follows governance canon

HUMAN GATES:
- BLOCK decisions require human approval
- ASK_HUMAN creates HTTP 423 checkpoint
"""

import logging
from typing import Optional, List, Dict, Any, Tuple
from uuid import uuid4
from datetime import datetime
from dataclasses import dataclass, field

from ..schemas.governance_schemas import (
    GovernanceSignal,
    GovernanceSignalLevel,
    GovernanceCriterion,
    Spec,
    SpecRunResult,
    PatchInstruction,
    SegmentScores,
    Budgets,
    QCTResult,
    OrchestratorDecision,
    OrchDecisionPayload,
    EscalationPayload,
    SpecDeferredPayload,
    AgentConfiguration,
    ExecutionMode,
    SignalScope,
    BacklogItem,
    BacklogType,
    BacklogItemCreate,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# Cost estimates per configuration (tokens)
CONFIG_COSTS = {
    AgentConfiguration.CONFIG_A: 500,    # Cheap executor + light CEAs
    AgentConfiguration.CONFIG_B: 1500,   # Strong executor + light CEAs
    AgentConfiguration.CONFIG_C: 2500,   # Strong executor + cheap critic
    AgentConfiguration.CONFIG_D: 4000,   # Strong executor + strong critic
    AgentConfiguration.CONFIG_E: 6000,   # 2 strong workers parallel
}

# Latency estimates per configuration (ms)
CONFIG_LATENCIES = {
    AgentConfiguration.CONFIG_A: 200,
    AgentConfiguration.CONFIG_B: 500,
    AgentConfiguration.CONFIG_C: 800,
    AgentConfiguration.CONFIG_D: 1200,
    AgentConfiguration.CONFIG_E: 1500,
}

# Quality estimates per configuration (0-1)
CONFIG_QUALITY = {
    AgentConfiguration.CONFIG_A: 0.5,
    AgentConfiguration.CONFIG_B: 0.7,
    AgentConfiguration.CONFIG_C: 0.8,
    AgentConfiguration.CONFIG_D: 0.9,
    AgentConfiguration.CONFIG_E: 0.95,
}


# ═══════════════════════════════════════════════════════════════════════════════
# QCT ALGORITHM (Quality/Cost Targeting)
# ═══════════════════════════════════════════════════════════════════════════════

class QCTAlgorithm:
    """
    Quality/Cost Targeting Algorithm.
    
    Chooses an agent configuration that minimizes cost while meeting
    required quality, respecting budget and mode constraints.
    """
    
    @staticmethod
    def compute_required_quality(scores: SegmentScores) -> float:
        """
        Compute Required Quality (RQ) from segment scores.
        
        Formula: RQ = clamp(0.2 + 0.35*C + 0.25*X + 0.25*E + 0.25*R + 0.15*U, 0, 1)
        
        Interpretation:
        - 0.0-0.3: draft acceptable
        - 0.3-0.6: professional internal
        - 0.6-0.85: high quality deliverable
        - 0.85-1.0: critical / near-zero defect
        """
        rq = (
            0.2 +
            0.35 * scores.criticality +
            0.25 * scores.complexity +
            0.25 * scores.exposure +
            0.25 * scores.irreversibility +
            0.15 * scores.uncertainty
        )
        return max(0.0, min(1.0, rq))
    
    @staticmethod
    def compute_expected_error_rate(scores: SegmentScores) -> float:
        """
        Compute Expected Error Rate (ER) from segment scores.
        
        Formula: ER = clamp(0.1 + 0.45*S + 0.25*X + 0.20*U, 0, 1)
        """
        er = (
            0.1 +
            0.45 * scores.segment_size +
            0.25 * scores.complexity +
            0.20 * scores.uncertainty
        )
        return max(0.0, min(1.0, er))
    
    @staticmethod
    def select_configuration(
        rq: float,
        er: float,
        budgets: Budgets,
        available_specs: List[str]
    ) -> QCTResult:
        """
        Select optimal agent configuration based on quality requirements and budgets.
        
        Rules:
        - Pick configuration with minimal cost that meets RQ
        - Live mode restricts to configs A/B/C unless critical (RQ > 0.85)
        - Respect cost and latency budgets
        """
        # Determine available configs based on mode
        if budgets.mode == ExecutionMode.LIVE:
            # Live mode: prefer low-latency configs
            if rq > 0.85:
                # Critical: allow all configs
                allowed_configs = list(AgentConfiguration)
            else:
                # Normal live: only A/B/C
                allowed_configs = [
                    AgentConfiguration.CONFIG_A,
                    AgentConfiguration.CONFIG_B,
                    AgentConfiguration.CONFIG_C,
                ]
        else:
            # Async mode: all configs allowed
            allowed_configs = list(AgentConfiguration)
        
        # Filter by budget constraints
        viable_configs = []
        for config in allowed_configs:
            cost = CONFIG_COSTS[config]
            latency = CONFIG_LATENCIES[config]
            quality = CONFIG_QUALITY[config]
            
            if cost <= budgets.cost_remaining and latency <= budgets.latency_budget_ms:
                if quality >= rq:
                    viable_configs.append((config, cost, latency, quality))
        
        if not viable_configs:
            # Fallback to cheapest that fits budget
            for config in allowed_configs:
                cost = CONFIG_COSTS[config]
                if cost <= budgets.cost_remaining:
                    viable_configs.append((
                        config,
                        cost,
                        CONFIG_LATENCIES[config],
                        CONFIG_QUALITY[config]
                    ))
                    break
        
        if not viable_configs:
            # Last resort: cheapest config
            selected = AgentConfiguration.CONFIG_A
            rationale = "Budget exhausted, using minimal config"
        else:
            # Sort by cost (ascending) and pick first
            viable_configs.sort(key=lambda x: x[1])
            selected = viable_configs[0][0]
            rationale = f"Selected {selected.value} for RQ={rq:.2f}, budget={budgets.cost_remaining}"
        
        return QCTResult(
            required_quality=rq,
            expected_error_rate=er,
            selected_config=selected,
            specs_to_run=available_specs,
            estimated_cost=CONFIG_COSTS[selected],
            estimated_latency_ms=CONFIG_LATENCIES[selected],
            rationale=rationale
        )


# ═══════════════════════════════════════════════════════════════════════════════
# SES ALGORITHM (Selective Escalation by Segment)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Segment:
    """A segment of work with its own scores."""
    id: str
    scores: SegmentScores
    content_type: str  # "doc_section", "code_module", "workflow_step", "xr_zone"
    
    
class SESAlgorithm:
    """
    Selective Escalation by Segment Algorithm.
    
    For large tasks, activates expensive intelligence only for
    segments that justify it based on criticality/complexity.
    """
    
    # Escalation thresholds
    RQ_ESCALATION_THRESHOLD = 0.85
    CONFLICT_THRESHOLD = 2  # Number of conflicting signals
    REPEATED_CORRECTIONS_THRESHOLD = 3
    
    @staticmethod
    def segment_work(
        content: Dict[str, Any],
        content_type: str
    ) -> List[Segment]:
        """
        Segment work into logical pieces.
        
        Args:
            content: The content to segment (doc, code, workflow, etc.)
            content_type: Type of content being segmented
            
        Returns:
            List of segments with default scores
        """
        segments = []
        
        if content_type == "doc":
            # Segment by sections
            sections = content.get("sections", [content])
            for i, section in enumerate(sections):
                segments.append(Segment(
                    id=f"seg_doc_{i}",
                    scores=SegmentScores(
                        criticality=0.3,
                        complexity=0.3,
                        exposure=0.2,
                        irreversibility=0.2,
                        uncertainty=0.3,
                        segment_size=min(1.0, len(str(section)) / 10000)
                    ),
                    content_type="doc_section"
                ))
        
        elif content_type == "code":
            # Segment by modules/files
            modules = content.get("modules", [content])
            for i, module in enumerate(modules):
                segments.append(Segment(
                    id=f"seg_code_{i}",
                    scores=SegmentScores(
                        criticality=0.5,  # Code is more critical
                        complexity=0.5,
                        exposure=0.3,
                        irreversibility=0.7,  # Code changes harder to revert
                        uncertainty=0.4,
                        segment_size=min(1.0, len(str(module)) / 5000)
                    ),
                    content_type="code_module"
                ))
        
        elif content_type == "workflow":
            # Segment by steps
            steps = content.get("steps", [content])
            for i, step in enumerate(steps):
                segments.append(Segment(
                    id=f"seg_workflow_{i}",
                    scores=SegmentScores(
                        criticality=0.4,
                        complexity=0.4,
                        exposure=0.3,
                        irreversibility=0.5,
                        uncertainty=0.3,
                        segment_size=0.2
                    ),
                    content_type="workflow_step"
                ))
        
        elif content_type == "xr":
            # Segment by zones
            zones = content.get("zones", [])
            for zone in zones:
                segments.append(Segment(
                    id=f"seg_xr_{zone.get('id', 'unknown')}",
                    scores=SegmentScores(
                        criticality=0.3,
                        complexity=0.3,
                        exposure=0.4,  # XR is visible
                        irreversibility=0.3,
                        uncertainty=0.2,
                        segment_size=0.3
                    ),
                    content_type="xr_zone"
                ))
        
        return segments if segments else [Segment(
            id="seg_default",
            scores=SegmentScores(
                criticality=0.5,
                complexity=0.5,
                exposure=0.5,
                irreversibility=0.5,
                uncertainty=0.5,
                segment_size=0.5
            ),
            content_type="default"
        )]
    
    @staticmethod
    def check_escalation_triggers(
        segment: Segment,
        signals: List[GovernanceSignal],
        correction_count: int = 0
    ) -> Tuple[bool, str]:
        """
        Check if a segment should trigger escalation.
        
        Triggers:
        - RQ > 0.85
        - Conflict between CEAs > threshold
        - Repeated corrections on same segment
        - Schema/security guard fails
        - High ER and irreversible
        
        Returns:
            (should_escalate, reason)
        """
        rq = QCTAlgorithm.compute_required_quality(segment.scores)
        er = QCTAlgorithm.compute_expected_error_rate(segment.scores)
        
        # High required quality
        if rq > SESAlgorithm.RQ_ESCALATION_THRESHOLD:
            return True, f"RQ={rq:.2f} exceeds threshold"
        
        # Check for conflicting signals
        segment_signals = [s for s in signals if s.scope and s.scope.segment_id == segment.id]
        if len(segment_signals) >= SESAlgorithm.CONFLICT_THRESHOLD:
            return True, f"Multiple signals ({len(segment_signals)}) on segment"
        
        # Check for blocking signals
        for signal in segment_signals:
            if signal.level in [GovernanceSignalLevel.BLOCK, GovernanceSignalLevel.ESCALATE]:
                return True, f"Signal {signal.level.value} from {signal.criterion.value}"
        
        # Repeated corrections
        if correction_count >= SESAlgorithm.REPEATED_CORRECTIONS_THRESHOLD:
            return True, f"Repeated corrections ({correction_count}) on segment"
        
        # High error rate on irreversible segment
        if er > 0.5 and segment.scores.irreversibility > 0.7:
            return True, f"High ER={er:.2f} on irreversible segment"
        
        return False, ""
    
    @staticmethod
    def select_per_segment_config(
        segments: List[Segment],
        signals: List[GovernanceSignal],
        budgets: Budgets
    ) -> Dict[str, QCTResult]:
        """
        Select configuration for each segment.
        
        Simple segments -> cheap executor + light checks
        Complex segments -> strong executor + CEAs
        Critical segments -> add second agent locally
        
        Returns:
            Dict mapping segment_id to QCTResult
        """
        results = {}
        remaining_budget = budgets.cost_remaining
        
        for segment in segments:
            # Create segment-specific budget
            segment_budget = Budgets(
                cost_remaining=remaining_budget / len(segments),
                latency_budget_ms=budgets.latency_budget_ms,
                mode=budgets.mode
            )
            
            # Get QCT result for segment
            rq = QCTAlgorithm.compute_required_quality(segment.scores)
            er = QCTAlgorithm.compute_expected_error_rate(segment.scores)
            
            # Check escalation
            should_escalate, reason = SESAlgorithm.check_escalation_triggers(
                segment, signals
            )
            
            if should_escalate:
                # Force stronger config for escalated segments
                result = QCTAlgorithm.select_configuration(
                    rq=max(rq, 0.85),  # Bump RQ
                    er=er,
                    budgets=segment_budget,
                    available_specs=["CANON_GUARD", "SCHEMA_GUARD", "SECURITY_GUARD", "COHERENCE_GUARD", "DEEP_CRITIC"]
                )
                result.rationale = f"ESCALATED: {reason}. {result.rationale}"
            else:
                result = QCTAlgorithm.select_configuration(
                    rq=rq,
                    er=er,
                    budgets=segment_budget,
                    available_specs=["CANON_GUARD", "SCHEMA_GUARD", "STYLE_GUARD"]
                )
            
            results[segment.id] = result
            remaining_budget -= result.estimated_cost
        
        return results


# ═══════════════════════════════════════════════════════════════════════════════
# RDC ALGORITHM (Realtime Drift Control)
# ═══════════════════════════════════════════════════════════════════════════════

class RDCAlgorithm:
    """
    Realtime Drift Control Algorithm.
    
    Continuously realigns the executor when it drifts by:
    1. Observing CEA signals
    2. Deciding intervention type
    3. Generating patch instructions
    """
    
    @staticmethod
    def decide_intervention(
        signals: List[GovernanceSignal],
        budgets: Budgets
    ) -> Tuple[OrchestratorDecision, Optional[str]]:
        """
        Decide intervention type based on signals.
        
        Returns:
            (decision, reason)
        """
        if not signals:
            return OrchestratorDecision.RUN_SPEC, "No signals, continue normally"
        
        # Sort signals by severity
        severity_order = {
            GovernanceSignalLevel.WARN: 1,
            GovernanceSignalLevel.CORRECT: 2,
            GovernanceSignalLevel.PAUSE: 3,
            GovernanceSignalLevel.BLOCK: 4,
            GovernanceSignalLevel.ESCALATE: 5,
        }
        signals_sorted = sorted(signals, key=lambda s: severity_order[s.level], reverse=True)
        worst_signal = signals_sorted[0]
        
        # Decide based on worst signal
        if worst_signal.level == GovernanceSignalLevel.WARN:
            return OrchestratorDecision.RUN_SPEC, f"WARN: {worst_signal.message}"
        
        elif worst_signal.level == GovernanceSignalLevel.CORRECT:
            return OrchestratorDecision.PATCH_INSTRUCTION, f"CORRECT: {worst_signal.message}"
        
        elif worst_signal.level == GovernanceSignalLevel.PAUSE:
            return OrchestratorDecision.ASK_HUMAN, f"PAUSE: {worst_signal.message}"
        
        elif worst_signal.level == GovernanceSignalLevel.BLOCK:
            return OrchestratorDecision.BLOCK, f"BLOCK: {worst_signal.message}"
        
        elif worst_signal.level == GovernanceSignalLevel.ESCALATE:
            return OrchestratorDecision.ESCALATE, f"ESCALATE: {worst_signal.message}"
        
        return OrchestratorDecision.RUN_SPEC, "Default: continue"
    
    @staticmethod
    def generate_patch_instruction(
        signal: GovernanceSignal,
        verification_spec_id: str = "COHERENCE_GUARD",
        created_by: str = "orchestrator"
    ) -> PatchInstruction:
        """
        Generate a PATCH_INSTRUCTION from a CORRECT signal.
        
        Patch format:
        - scope: segment_id + region
        - constraint: what must hold
        - correction: what to change
        - rationale: short explanation
        - verification: which spec confirms
        """
        return PatchInstruction(
            id=str(uuid4()),
            scope=signal.scope or SignalScope(),
            constraint=f"Must maintain {signal.criterion.value} integrity",
            correction=signal.message,
            rationale=f"CEA {signal.cea_id} detected drift with confidence {signal.confidence:.2f}",
            verification_spec_id=verification_spec_id,
            created_by=created_by
        )


# ═══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class OrchestratorService:
    """
    AT-OM Orchestrator Service.
    
    Centralized decision authority for:
    - Which specs/agents to run
    - When to run them
    - How to respond to CEA signals
    - When to escalate to specialists or humans
    
    All decisions are logged as ORCH_DECISION_MADE events.
    """
    
    def __init__(self):
        self.qct = QCTAlgorithm()
        self.ses = SESAlgorithm()
        self.rdc = RDCAlgorithm()
        self.pending_signals: List[GovernanceSignal] = []
        self.spec_catalog: Dict[str, Spec] = {}
        
        logger.info("OrchestratorService initialized")
    
    def register_spec(self, spec: Spec) -> None:
        """Register a specification in the catalog."""
        self.spec_catalog[spec.id] = spec
        logger.info(f"Registered spec: {spec.id}")
    
    def receive_signal(self, signal: GovernanceSignal) -> None:
        """Receive a governance signal from a CEA."""
        self.pending_signals.append(signal)
        logger.info(f"Received signal: {signal.level.value} from {signal.cea_id}")
    
    async def make_decision(
        self,
        thread_id: str,
        segment_scores: SegmentScores,
        budgets: Budgets,
        user_id: str
    ) -> OrchDecisionPayload:
        """
        Make an orchestration decision.
        
        This is the main entry point for the orchestrator.
        
        1. Process pending signals with RDC
        2. If correction needed, generate patch
        3. Else, compute QCT for next action
        4. Log decision as event
        
        Returns:
            OrchDecisionPayload to be emitted as ORCH_DECISION_MADE event
        """
        # Process signals with RDC
        decision, reason = self.rdc.decide_intervention(
            self.pending_signals,
            budgets
        )
        
        # Build decision payload
        payload = OrchDecisionPayload(
            decision=decision,
            reason=reason or "No intervention needed",
            budgets=budgets,
            signals=self.pending_signals.copy(),
            scope=None
        )
        
        # Handle specific decisions
        if decision == OrchestratorDecision.PATCH_INSTRUCTION:
            # Generate patch for worst signal
            worst_signal = max(
                self.pending_signals,
                key=lambda s: s.confidence
            )
            patch = self.rdc.generate_patch_instruction(
                worst_signal,
                created_by=user_id
            )
            payload.patch_instruction = patch
            payload.scope = worst_signal.scope
        
        elif decision == OrchestratorDecision.RUN_SPEC:
            # Compute QCT for configuration selection
            qct_result = self.qct.select_configuration(
                rq=self.qct.compute_required_quality(segment_scores),
                er=self.qct.compute_expected_error_rate(segment_scores),
                budgets=budgets,
                available_specs=list(self.spec_catalog.keys())
            )
            payload.config_selected = qct_result.selected_config
            payload.specs_scheduled = qct_result.specs_to_run
            payload.reason = qct_result.rationale
        
        elif decision == OrchestratorDecision.ESCALATE:
            # Create escalation payload separately
            pass
        
        # Clear processed signals
        self.pending_signals.clear()
        
        logger.info(f"Decision made: {decision.value} - {reason}")
        return payload
    
    async def process_segment_batch(
        self,
        thread_id: str,
        content: Dict[str, Any],
        content_type: str,
        budgets: Budgets,
        user_id: str
    ) -> Dict[str, OrchDecisionPayload]:
        """
        Process a batch of segments using SES algorithm.
        
        Returns:
            Dict mapping segment_id to decision payload
        """
        # Segment the work
        segments = self.ses.segment_work(content, content_type)
        
        # Get per-segment configurations
        configs = self.ses.select_per_segment_config(
            segments,
            self.pending_signals,
            budgets
        )
        
        # Build decision payloads for each segment
        decisions = {}
        for segment in segments:
            qct_result = configs[segment.id]
            
            decisions[segment.id] = OrchDecisionPayload(
                decision=OrchestratorDecision.RUN_SPEC,
                reason=qct_result.rationale,
                budgets=budgets,
                signals=[s for s in self.pending_signals if s.scope and s.scope.segment_id == segment.id],
                scope=SignalScope(segment_id=segment.id),
                config_selected=qct_result.selected_config,
                specs_scheduled=qct_result.specs_to_run
            )
        
        return decisions
    
    def create_backlog_item(
        self,
        backlog_type: BacklogType,
        description: str,
        thread_id: str,
        severity: Optional[str] = None,
        references: Optional[Dict[str, Any]] = None
    ) -> BacklogItem:
        """
        Create a backlog item for learning.
        
        Used when:
        - Defect escapes early checks (error)
        - False positive detected (signal)
        - Decision outcome tracked (decision)
        - Cost spike detected (cost)
        """
        from ..schemas.governance_schemas import BacklogReferences
        
        return BacklogItem(
            backlog_type=backlog_type,
            severity=severity,
            description=description,
            references=BacklogReferences(
                thread_id=thread_id,
                **(references or {})
            )
        )


# ═══════════════════════════════════════════════════════════════════════════════
# DEFAULT SPEC CATALOG
# ═══════════════════════════════════════════════════════════════════════════════

def get_default_spec_catalog() -> List[Spec]:
    """Get the default specification catalog."""
    from ..schemas.governance_schemas import SpecTriggers
    
    return [
        Spec(
            id="CANON_GUARD",
            name="Canonical Thread Guard",
            category="safety",
            cost_level=1,
            latency_level=1,
            risk_coverage=["duplicate_memory", "append_only_violation", "permission_bypass"],
            triggers=SpecTriggers(always_on=True),
            cooldown=0,
            output="block",
            owner_agent="CanonGuardCEA"
        ),
        Spec(
            id="SCHEMA_GUARD",
            name="Schema Validator",
            category="correctness",
            cost_level=1,
            latency_level=1,
            risk_coverage=["json_schema_violation", "type_mismatch"],
            triggers=SpecTriggers(always_on=True),
            cooldown=0,
            output="signal",
            owner_agent="SchemaGuardCEA"
        ),
        Spec(
            id="SECURITY_GUARD",
            name="Security Invariant Checker",
            category="safety",
            cost_level=2,
            latency_level=2,
            risk_coverage=["injection", "unauthorized_access", "data_leak"],
            triggers=SpecTriggers(always_on=True),
            cooldown=0,
            output="block",
            owner_agent="SecurityGuardCEA"
        ),
        Spec(
            id="COHERENCE_GUARD",
            name="Coherence Detector",
            category="coherence",
            cost_level=2,
            latency_level=2,
            risk_coverage=["contradiction", "intent_drift", "context_loss"],
            triggers=SpecTriggers(
                on_event_types=["DECISION_RECORDED", "ACTION_CREATED"]
            ),
            cooldown=60,
            output="signal",
            owner_agent="CoherenceGuardCEA"
        ),
        Spec(
            id="STYLE_GUARD",
            name="Style & Clarity Checker",
            category="style",
            cost_level=1,
            latency_level=1,
            risk_coverage=["formatting", "clarity", "consistency"],
            triggers=SpecTriggers(on_event_types=["MESSAGE_POSTED"]),
            cooldown=30,
            output="signal",
            owner_agent="StyleGuardCEA"
        ),
        Spec(
            id="BUDGET_GUARD",
            name="Budget & Latency Monitor",
            category="cost",
            cost_level=1,
            latency_level=1,
            risk_coverage=["budget_exceeded", "latency_spike"],
            triggers=SpecTriggers(always_on=True),
            cooldown=0,
            output="signal",
            owner_agent="BudgetGuardCEA"
        ),
        Spec(
            id="DEEP_CRITIC",
            name="Deep Critic Review",
            category="correctness",
            cost_level=4,
            latency_level=4,
            risk_coverage=["logic_error", "subtle_bug", "edge_case"],
            triggers=SpecTriggers(on_segment_criticality_above=0.8),
            cooldown=300,
            output="signal",
            owner_agent="DeepCriticAgent"
        ),
        Spec(
            id="LEGAL_COMPLIANCE",
            name="Legal Compliance Check",
            category="compliance",
            cost_level=5,
            latency_level=5,
            risk_coverage=["legal_violation", "regulatory_breach"],
            triggers=SpecTriggers(on_cea_signal=GovernanceSignalLevel.ESCALATE),
            cooldown=600,
            output="block",
            owner_agent="LegalComplianceAgent"
        ),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    "QCTAlgorithm",
    "SESAlgorithm",
    "RDCAlgorithm",
    "Segment",
    "OrchestratorService",
    "get_default_spec_catalog",
    "CONFIG_COSTS",
    "CONFIG_LATENCIES",
    "CONFIG_QUALITY",
]
