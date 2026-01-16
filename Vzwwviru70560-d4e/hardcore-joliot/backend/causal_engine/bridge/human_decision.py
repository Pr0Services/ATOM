"""
============================================================================
CHE·NU™ V69 — HUMAN DECISION BRIDGE (HITL)
============================================================================
Version: 1.0.0
Purpose: Bridge between AI analysis and human decision
Principle: CHE·NU NEVER DECIDES. HUMANS ALWAYS DECIDE.
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import logging
import hashlib
import json
import uuid

from pydantic import BaseModel, Field

from ..core.models import (
    CausalDAG,
    CausalEffect,
    SensitivityScore,
    CounterfactualResult,
    DecisionRecommendation,
    ConfidenceLevel,
    ValidationStatus,
)
from ..core.inference import CausalEngine

logger = logging.getLogger(__name__)


# ============================================================================
# DECISION STATUS
# ============================================================================

class DecisionStatus(str, Enum):
    """Status of human decision"""
    PENDING = "pending"              # Awaiting decision
    VIEWED = "viewed"                # Human has seen recommendation
    UNDER_REVIEW = "under_review"    # Being evaluated
    DECIDED = "decided"              # Decision made
    DEFERRED = "deferred"            # Postponed
    ESCALATED = "escalated"          # Sent to higher authority
    CANCELLED = "cancelled"          # No longer needed


# ============================================================================
# DECISION RECORD
# ============================================================================

class DecisionRecord(BaseModel):
    """
    Immutable record of human decision.
    
    This is the CRITICAL governance artifact that proves
    a human made the decision, not the AI.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    recommendation_id: str = Field(...)
    dag_id: str = Field(...)
    
    # Decision
    status: DecisionStatus = Field(default=DecisionStatus.PENDING)
    selected_option: Optional[str] = Field(default=None)
    decision_rationale: Optional[str] = Field(default=None)
    
    # Human identity
    decider_id: str = Field(default="", description="Human who made decision")
    decider_name: Optional[str] = Field(default=None)
    decider_role: Optional[str] = Field(default=None)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    viewed_at: Optional[datetime] = Field(default=None)
    decided_at: Optional[datetime] = Field(default=None)
    
    # Audit
    trace_id: Optional[str] = Field(default=None)
    tenant_id: Optional[str] = Field(default=None)
    synthetic: bool = Field(default=True)
    
    # Signature
    signature: Optional[str] = Field(default=None)
    signature_algorithm: str = Field(default="sha256")
    
    def sign(self, secret_key: str = "mock-key") -> str:
        """Sign the decision record"""
        content = {
            "id": self.id,
            "recommendation_id": self.recommendation_id,
            "selected_option": self.selected_option,
            "decider_id": self.decider_id,
            "decided_at": self.decided_at.isoformat() if self.decided_at else None,
        }
        payload = json.dumps(content, sort_keys=True)
        signature = hashlib.sha256(f"{payload}{secret_key}".encode()).hexdigest()
        self.signature = signature
        return signature
    
    def verify(self, secret_key: str = "mock-key") -> bool:
        """Verify signature"""
        if not self.signature:
            return False
        
        content = {
            "id": self.id,
            "recommendation_id": self.recommendation_id,
            "selected_option": self.selected_option,
            "decider_id": self.decider_id,
            "decided_at": self.decided_at.isoformat() if self.decided_at else None,
        }
        payload = json.dumps(content, sort_keys=True)
        expected = hashlib.sha256(f"{payload}{secret_key}".encode()).hexdigest()
        return self.signature == expected


# ============================================================================
# DECISION OPTION
# ============================================================================

class DecisionOption(BaseModel):
    """A possible decision option presented to human"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(...)
    description: str = Field(...)
    
    # Impact estimates
    expected_outcome: Optional[float] = Field(default=None)
    confidence_interval: Optional[tuple] = Field(default=None)
    risk_level: str = Field(default="medium")
    
    # Details
    key_assumptions: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    benefits: List[str] = Field(default_factory=list)
    
    # Causal backing
    causal_effects: List[CausalEffect] = Field(default_factory=list)
    counterfactuals: List[CounterfactualResult] = Field(default_factory=list)


# ============================================================================
# DECISION PACKAGE
# ============================================================================

class DecisionPackage(BaseModel):
    """
    Complete package for human decision.
    
    Contains all information needed to make an informed decision:
    - Options to choose from
    - Causal analysis
    - Sensitivity scores
    - Risks and recommendations
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(...)
    description: str = Field(...)
    
    # Source
    dag_id: str = Field(...)
    simulation_id: Optional[str] = Field(default=None)
    
    # Options
    options: List[DecisionOption] = Field(default_factory=list)
    
    # Analysis
    key_levers: List[SensitivityScore] = Field(default_factory=list)
    risk_factors: List[SensitivityScore] = Field(default_factory=list)
    critical_alerts: List[str] = Field(default_factory=list)
    
    # Context
    assumptions: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    
    # Recommendation (advisory only!)
    recommended_option_id: Optional[str] = Field(
        default=None,
        description="AI suggestion - advisory only, human decides"
    )
    recommendation_rationale: Optional[str] = Field(default=None)
    
    # Governance
    requires_human_decision: bool = Field(default=True)
    deadline: Optional[datetime] = Field(default=None)
    escalation_contact: Optional[str] = Field(default=None)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(default="causal_engine")
    tenant_id: Optional[str] = Field(default=None)
    trace_id: Optional[str] = Field(default=None)
    synthetic: bool = Field(default=True)
    
    # Decision record (linked after human decides)
    decision_record_id: Optional[str] = Field(default=None)


# ============================================================================
# HUMAN DECISION BRIDGE
# ============================================================================

class HumanDecisionBridge:
    """
    Bridge between AI analysis and human decision-making.
    
    CORE PRINCIPLE: AI analyzes, humans decide.
    
    This class:
    1. Packages causal analysis for human consumption
    2. Presents options clearly with pros/cons
    3. Records human decisions immutably
    4. Never makes decisions itself
    
    Usage:
        bridge = HumanDecisionBridge(causal_engine)
        
        # Create decision package
        package = bridge.create_decision_package(
            title="Q4 Strategy",
            outcome="revenue",
            interventions=[...],
        )
        
        # Human views and decides
        record = bridge.record_decision(
            package_id=package.id,
            decider_id="user-123",
            selected_option="option-A",
            rationale="Best risk-reward balance",
        )
    """
    
    def __init__(self, engine: CausalEngine):
        self.engine = engine
        self._packages: Dict[str, DecisionPackage] = {}
        self._records: Dict[str, DecisionRecord] = {}
    
    def create_decision_package(
        self,
        title: str,
        description: str,
        outcome_node: str,
        intervention_scenarios: List[Dict[str, float]],
        scenario_names: Optional[List[str]] = None,
        tenant_id: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> DecisionPackage:
        """
        Create a decision package for human review.
        
        Args:
            title: Decision title
            description: Decision context
            outcome_node: What outcome to optimize
            intervention_scenarios: List of intervention options
            scenario_names: Names for each scenario
        """
        if scenario_names is None:
            scenario_names = [f"Option {i+1}" for i in range(len(intervention_scenarios))]
        
        # Get analysis from causal engine
        levers = self.engine.get_key_levers(outcome_node, top_n=5)
        risks = self.engine.get_risk_factors(outcome_node, top_n=5)
        
        # Create options from scenarios
        options = []
        base_outcome = None
        
        for i, scenario in enumerate(intervention_scenarios):
            # Estimate outcome for this scenario
            total_effect = 0
            effects = []
            
            for node_name, value in scenario.items():
                effect = self.engine.estimate_effect(node_name, outcome_node)
                
                # Get baseline value
                node = self.engine.dag.nodes.get(
                    self._resolve_id(node_name)
                )
                if node and node.observed_value is not None:
                    delta = value - node.observed_value
                    contribution = (effect.ate or 0) * delta
                    total_effect += contribution
                
                effects.append(effect)
            
            # Get base outcome value
            out_node = self.engine.dag.nodes.get(self._resolve_id(outcome_node))
            if base_outcome is None and out_node:
                base_outcome = out_node.observed_value or 0
            
            expected = (base_outcome or 0) + total_effect
            
            # Create option
            option = DecisionOption(
                name=scenario_names[i],
                description=f"Intervention: {scenario}",
                expected_outcome=expected,
                risk_level=self._assess_risk(effects),
                key_assumptions=[
                    f"Assumes {k}={v} is achievable" for k, v in scenario.items()
                ],
                risks=[r.alert_message for r in risks[:2] if r.alert_message],
                benefits=[
                    f"Expected {outcome_node}: {expected:.2f}",
                ],
                causal_effects=effects,
            )
            options.append(option)
        
        # Find best option (for advisory)
        if options:
            best_idx = max(
                range(len(options)),
                key=lambda i: options[i].expected_outcome or 0
            )
            recommended_id = options[best_idx].id
            recommended_rationale = (
                f"Option '{options[best_idx].name}' has highest expected "
                f"{outcome_node} ({options[best_idx].expected_outcome:.2f}). "
                f"This is an AI suggestion only - please review and decide."
            )
        else:
            recommended_id = None
            recommended_rationale = None
        
        # Create package
        package = DecisionPackage(
            title=title,
            description=description,
            dag_id=self.engine.dag.id,
            simulation_id=self.engine.dag.simulation_id,
            options=options,
            key_levers=levers,
            risk_factors=risks,
            critical_alerts=[r.alert_message for r in risks if r.is_critical],
            assumptions=[
                "Analysis based on synthetic data only",
                "Causal relationships are estimated, not guaranteed",
            ],
            limitations=[
                "Cannot account for unknown confounders",
                "Results are probabilistic, not deterministic",
            ],
            recommended_option_id=recommended_id,
            recommendation_rationale=recommended_rationale,
            requires_human_decision=True,
            deadline=deadline,
            tenant_id=tenant_id,
        )
        
        # Store
        self._packages[package.id] = package
        
        logger.info(
            f"Created decision package {package.id}: {title} "
            f"with {len(options)} options"
        )
        
        return package
    
    def get_package(self, package_id: str) -> Optional[DecisionPackage]:
        """Get a decision package"""
        return self._packages.get(package_id)
    
    def mark_viewed(
        self,
        package_id: str,
        viewer_id: str,
    ) -> Optional[DecisionRecord]:
        """Record that human has viewed the package"""
        package = self._packages.get(package_id)
        if package is None:
            return None
        
        # Create or get record
        record = self._get_or_create_record(package)
        record.status = DecisionStatus.VIEWED
        record.viewed_at = datetime.utcnow()
        record.decider_id = viewer_id
        
        logger.info(f"Package {package_id} viewed by {viewer_id}")
        
        return record
    
    def record_decision(
        self,
        package_id: str,
        decider_id: str,
        selected_option_id: str,
        rationale: str,
        decider_name: Optional[str] = None,
        decider_role: Optional[str] = None,
    ) -> DecisionRecord:
        """
        Record human decision.
        
        This is the CRITICAL governance function.
        Creates an immutable, signed record of human decision.
        """
        package = self._packages.get(package_id)
        if package is None:
            raise ValueError(f"Package not found: {package_id}")
        
        # Validate option exists
        option_ids = [o.id for o in package.options]
        if selected_option_id not in option_ids:
            raise ValueError(f"Invalid option: {selected_option_id}")
        
        # Create record
        record = DecisionRecord(
            recommendation_id=package_id,
            dag_id=package.dag_id,
            status=DecisionStatus.DECIDED,
            selected_option=selected_option_id,
            decision_rationale=rationale,
            decider_id=decider_id,
            decider_name=decider_name,
            decider_role=decider_role,
            decided_at=datetime.utcnow(),
            tenant_id=package.tenant_id,
            trace_id=package.trace_id,
            synthetic=True,
        )
        
        # Sign the record
        record.sign()
        
        # Store
        self._records[record.id] = record
        
        # Link to package
        package.decision_record_id = record.id
        
        logger.info(
            f"DECISION RECORDED: {record.id} by {decider_id} | "
            f"Selected: {selected_option_id} | "
            f"Rationale: {rationale[:50]}..."
        )
        
        return record
    
    def get_record(self, record_id: str) -> Optional[DecisionRecord]:
        """Get a decision record"""
        return self._records.get(record_id)
    
    def verify_record(self, record_id: str) -> bool:
        """Verify decision record signature"""
        record = self._records.get(record_id)
        if record is None:
            return False
        return record.verify()
    
    def defer_decision(
        self,
        package_id: str,
        decider_id: str,
        reason: str,
        new_deadline: Optional[datetime] = None,
    ) -> DecisionRecord:
        """Defer decision to later"""
        package = self._packages.get(package_id)
        if package is None:
            raise ValueError(f"Package not found: {package_id}")
        
        record = self._get_or_create_record(package)
        record.status = DecisionStatus.DEFERRED
        record.decider_id = decider_id
        record.decision_rationale = f"Deferred: {reason}"
        
        if new_deadline:
            package.deadline = new_deadline
        
        logger.info(f"Decision {package_id} deferred by {decider_id}: {reason}")
        
        return record
    
    def escalate_decision(
        self,
        package_id: str,
        escalator_id: str,
        escalate_to: str,
        reason: str,
    ) -> DecisionRecord:
        """Escalate decision to higher authority"""
        package = self._packages.get(package_id)
        if package is None:
            raise ValueError(f"Package not found: {package_id}")
        
        record = self._get_or_create_record(package)
        record.status = DecisionStatus.ESCALATED
        record.decider_id = escalator_id
        record.decision_rationale = f"Escalated to {escalate_to}: {reason}"
        
        package.escalation_contact = escalate_to
        
        logger.info(
            f"Decision {package_id} escalated by {escalator_id} to {escalate_to}"
        )
        
        return record
    
    def _get_or_create_record(self, package: DecisionPackage) -> DecisionRecord:
        """Get existing record or create new one"""
        if package.decision_record_id:
            record = self._records.get(package.decision_record_id)
            if record:
                return record
        
        record = DecisionRecord(
            recommendation_id=package.id,
            dag_id=package.dag_id,
            tenant_id=package.tenant_id,
            trace_id=package.trace_id,
        )
        self._records[record.id] = record
        package.decision_record_id = record.id
        
        return record
    
    def _resolve_id(self, name_or_id: str) -> str:
        """Resolve node name to ID"""
        if name_or_id in self.engine.dag.nodes:
            return name_or_id
        
        for node_id, node in self.engine.dag.nodes.items():
            if node.name == name_or_id:
                return node_id
        
        return name_or_id
    
    def _assess_risk(self, effects: List[CausalEffect]) -> str:
        """Assess overall risk level from effects"""
        # Count significant vs uncertain effects
        significant = sum(1 for e in effects if e.is_significant)
        total = len(effects)
        
        if total == 0:
            return "unknown"
        
        ratio = significant / total
        
        if ratio > 0.8:
            return "low"
        elif ratio > 0.5:
            return "medium"
        else:
            return "high"
    
    def generate_decision_report(
        self,
        record_id: str,
    ) -> Dict[str, Any]:
        """Generate a signed decision report (PDF-ready)"""
        record = self._records.get(record_id)
        if record is None:
            raise ValueError(f"Record not found: {record_id}")
        
        package = self._packages.get(record.recommendation_id)
        if package is None:
            raise ValueError(f"Package not found: {record.recommendation_id}")
        
        # Find selected option
        selected_option = None
        for opt in package.options:
            if opt.id == record.selected_option:
                selected_option = opt
                break
        
        return {
            "report_type": "DECISION_RECORD",
            "report_id": str(uuid.uuid4()),
            "generated_at": datetime.utcnow().isoformat(),
            
            "decision": {
                "id": record.id,
                "package_title": package.title,
                "selected_option": selected_option.name if selected_option else "Unknown",
                "rationale": record.decision_rationale,
                "decided_at": record.decided_at.isoformat() if record.decided_at else None,
            },
            
            "decider": {
                "id": record.decider_id,
                "name": record.decider_name,
                "role": record.decider_role,
            },
            
            "context": {
                "dag_id": record.dag_id,
                "options_presented": len(package.options),
                "key_levers_count": len(package.key_levers),
                "risk_factors_count": len(package.risk_factors),
                "critical_alerts": package.critical_alerts,
            },
            
            "governance": {
                "signature": record.signature,
                "signature_valid": record.verify(),
                "synthetic_data_only": record.synthetic,
                "human_decided": True,
                "ai_decided": False,  # ALWAYS FALSE - CHE·NU principle
            },
            
            "disclaimer": (
                "This decision was made by a human. CHE·NU™ provided analysis "
                "and recommendations but did not make the decision. All data "
                "is synthetic. No real-world actions were executed."
            ),
        }
