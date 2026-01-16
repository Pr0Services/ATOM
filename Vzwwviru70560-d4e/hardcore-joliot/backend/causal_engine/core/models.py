"""
============================================================================
CHE·NU™ V69 — CAUSAL ENGINE CORE MODELS
============================================================================
Version: 1.0.0
Purpose: Data models for causal reasoning (DAG, nodes, edges, interventions)
Principle: GOUVERNANCE > EXÉCUTION - Agents analyze, humans decide
============================================================================
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field, computed_field
import uuid
import hashlib
import json


# ============================================================================
# ENUMS
# ============================================================================

class NodeType(str, Enum):
    """Types of causal nodes"""
    SLOT = "slot"                    # WorldEngine slot variable
    INTERVENTION = "intervention"    # do(X) intervention point
    OUTCOME = "outcome"              # Target/goal variable
    CONFOUNDER = "confounder"        # Common cause
    MEDIATOR = "mediator"            # Intermediate variable
    COLLIDER = "collider"            # Common effect
    INSTRUMENT = "instrument"        # Instrumental variable
    LATENT = "latent"                # Unobserved variable


class EdgeType(str, Enum):
    """Types of causal edges"""
    CAUSAL = "causal"                # Direct causal relationship
    CONFOUNDED = "confounded"        # Bidirectional (shared cause)
    ASSOCIATION = "association"      # Statistical, not causal
    BLOCKED = "blocked"              # Blocked path (conditioned)


class ConfidenceLevel(str, Enum):
    """Confidence in causal relationship"""
    VERIFIED = "verified"            # Experimentally confirmed
    STRONG = "strong"                # Strong observational evidence
    MODERATE = "moderate"            # Moderate evidence
    WEAK = "weak"                    # Weak evidence
    HYPOTHETICAL = "hypothetical"    # Expert hypothesis only


class InterventionType(str, Enum):
    """Types of causal interventions"""
    DO = "do"                        # do(X=x) - set value
    SOFT = "soft"                    # Soft intervention (distribution shift)
    COUNTERFACTUAL = "counterfactual"  # What-if on past
    POLICY = "policy"                # Policy intervention


class ValidationStatus(str, Enum):
    """DAG validation status"""
    DRAFT = "draft"                  # Not validated
    PENDING_REVIEW = "pending_review"  # Awaiting human review
    APPROVED = "approved"            # Human approved
    REJECTED = "rejected"            # Human rejected
    ARCHIVED = "archived"            # No longer active


# ============================================================================
# CAUSAL NODE
# ============================================================================

class CausalNode(BaseModel):
    """A node in the causal DAG"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Node name (e.g., slot name)")
    node_type: NodeType = Field(default=NodeType.SLOT)
    
    # Value & distribution
    observed_value: Optional[float] = Field(default=None)
    distribution: Optional[str] = Field(default=None, description="e.g., 'normal(0,1)'")
    domain: Optional[List[float]] = Field(default=None, description="[min, max]")
    
    # Metadata
    description: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None, description="e.g., 'EUR', '%', 'units'")
    slot_id: Optional[str] = Field(default=None, description="WorldEngine slot reference")
    sphere: Optional[str] = Field(default=None, description="CHE·NU sphere")
    
    # Causal properties
    is_manipulable: bool = Field(default=True, description="Can be intervened upon")
    is_observable: bool = Field(default=True, description="Can be observed")
    
    # Statistics
    mean: Optional[float] = Field(default=None)
    std: Optional[float] = Field(default=None)
    sample_size: Optional[int] = Field(default=None)
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, CausalNode):
            return self.id == other.id
        return False


# ============================================================================
# CAUSAL EDGE
# ============================================================================

class CausalEdge(BaseModel):
    """An edge in the causal DAG (cause → effect)"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_id: str = Field(..., description="Source node ID (cause)")
    target_id: str = Field(..., description="Target node ID (effect)")
    edge_type: EdgeType = Field(default=EdgeType.CAUSAL)
    
    # Strength & confidence
    coefficient: Optional[float] = Field(default=None, description="Effect size")
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.HYPOTHETICAL)
    p_value: Optional[float] = Field(default=None)
    confidence_interval: Optional[Tuple[float, float]] = Field(default=None)
    
    # Metadata
    description: Optional[str] = Field(default=None)
    evidence_source: Optional[str] = Field(default=None, description="Study, expert, etc.")
    
    # Temporal
    lag: Optional[int] = Field(default=None, description="Time lag in steps")
    is_instantaneous: bool = Field(default=True)
    
    # Validation
    validated_by: Optional[str] = Field(default=None, description="Human validator ID")
    validated_at: Optional[datetime] = Field(default=None)
    
    def __hash__(self):
        return hash(self.id)


# ============================================================================
# CAUSAL DAG
# ============================================================================

class CausalDAG(BaseModel):
    """Directed Acyclic Graph for causal reasoning"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="DAG name")
    version: str = Field(default="1.0.0")
    
    # Graph structure
    nodes: Dict[str, CausalNode] = Field(default_factory=dict)
    edges: List[CausalEdge] = Field(default_factory=list)
    
    # Metadata
    description: Optional[str] = Field(default=None)
    simulation_id: Optional[str] = Field(default=None, description="Source simulation")
    tenant_id: Optional[str] = Field(default=None)
    sphere: Optional[str] = Field(default=None)
    
    # Validation & governance
    status: ValidationStatus = Field(default=ValidationStatus.DRAFT)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(default=None)
    approved_by: Optional[str] = Field(default=None)
    approved_at: Optional[datetime] = Field(default=None)
    
    # Audit
    synthetic: bool = Field(default=True, description="Must be True - CHE·NU rule")
    
    @computed_field
    @property
    def node_count(self) -> int:
        return len(self.nodes)
    
    @computed_field
    @property
    def edge_count(self) -> int:
        return len(self.edges)
    
    @computed_field
    @property
    def hash(self) -> str:
        """Compute DAG hash for integrity verification"""
        content = {
            "nodes": sorted([n.id for n in self.nodes.values()]),
            "edges": sorted([(e.source_id, e.target_id) for e in self.edges]),
            "version": self.version,
        }
        return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()[:16]
    
    def add_node(self, node: CausalNode) -> None:
        """Add a node to the DAG"""
        self.nodes[node.id] = node
        self.updated_at = datetime.utcnow()
    
    def add_edge(self, edge: CausalEdge) -> None:
        """Add an edge to the DAG"""
        if edge.source_id not in self.nodes:
            raise ValueError(f"Source node {edge.source_id} not in DAG")
        if edge.target_id not in self.nodes:
            raise ValueError(f"Target node {edge.target_id} not in DAG")
        
        # Check for cycles
        if self._creates_cycle(edge.source_id, edge.target_id):
            raise ValueError(f"Edge {edge.source_id} → {edge.target_id} would create a cycle")
        
        self.edges.append(edge)
        self.updated_at = datetime.utcnow()
    
    def _creates_cycle(self, source: str, target: str) -> bool:
        """Check if adding edge would create a cycle"""
        # DFS from target to see if we can reach source
        visited = set()
        stack = [target]
        
        while stack:
            node = stack.pop()
            if node == source:
                return True
            if node in visited:
                continue
            visited.add(node)
            
            # Add children of current node
            for edge in self.edges:
                if edge.source_id == node:
                    stack.append(edge.target_id)
        
        return False
    
    def get_parents(self, node_id: str) -> List[str]:
        """Get parent node IDs (direct causes)"""
        return [e.source_id for e in self.edges if e.target_id == node_id]
    
    def get_children(self, node_id: str) -> List[str]:
        """Get children node IDs (direct effects)"""
        return [e.target_id for e in self.edges if e.source_id == node_id]
    
    def get_ancestors(self, node_id: str) -> Set[str]:
        """Get all ancestor node IDs"""
        ancestors = set()
        stack = self.get_parents(node_id)
        
        while stack:
            parent = stack.pop()
            if parent not in ancestors:
                ancestors.add(parent)
                stack.extend(self.get_parents(parent))
        
        return ancestors
    
    def get_descendants(self, node_id: str) -> Set[str]:
        """Get all descendant node IDs"""
        descendants = set()
        stack = self.get_children(node_id)
        
        while stack:
            child = stack.pop()
            if child not in descendants:
                descendants.add(child)
                stack.extend(self.get_children(child))
        
        return descendants
    
    def topological_sort(self) -> List[str]:
        """Return nodes in topological order"""
        in_degree = {n: 0 for n in self.nodes}
        for edge in self.edges:
            in_degree[edge.target_id] += 1
        
        queue = [n for n, d in in_degree.items() if d == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            for edge in self.edges:
                if edge.source_id == node:
                    in_degree[edge.target_id] -= 1
                    if in_degree[edge.target_id] == 0:
                        queue.append(edge.target_id)
        
        return result
    
    def is_valid_dag(self) -> bool:
        """Check if graph is a valid DAG (no cycles)"""
        return len(self.topological_sort()) == len(self.nodes)


# ============================================================================
# INTERVENTION
# ============================================================================

class Intervention(BaseModel):
    """A causal intervention do(X=x)"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    node_id: str = Field(..., description="Node to intervene on")
    intervention_type: InterventionType = Field(default=InterventionType.DO)
    
    # Intervention value
    value: Optional[float] = Field(default=None, description="Set value for do()")
    value_change: Optional[float] = Field(default=None, description="Relative change")
    distribution: Optional[str] = Field(default=None, description="New distribution for soft")
    
    # Metadata
    description: Optional[str] = Field(default=None)
    rationale: Optional[str] = Field(default=None)
    
    # Governance
    requires_hitl: bool = Field(default=True)
    approved: bool = Field(default=False)
    approved_by: Optional[str] = Field(default=None)


# ============================================================================
# CAUSAL QUERY
# ============================================================================

class CausalQuery(BaseModel):
    """A query to the causal engine"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dag_id: str = Field(..., description="DAG to query")
    
    # Query type
    query_type: str = Field(..., description="effect, counterfactual, sensitivity, etc.")
    
    # Variables
    treatment: str = Field(..., description="Treatment/intervention variable")
    outcome: str = Field(..., description="Outcome variable")
    covariates: List[str] = Field(default_factory=list, description="Adjustment set")
    
    # Interventions
    interventions: List[Intervention] = Field(default_factory=list)
    
    # Context
    trace_id: Optional[str] = Field(default=None)
    tenant_id: Optional[str] = Field(default=None)
    synthetic: bool = Field(default=True)


# ============================================================================
# CAUSAL EFFECT
# ============================================================================

class CausalEffect(BaseModel):
    """Result of a causal effect estimation"""
    
    query_id: str = Field(...)
    
    # Effect estimate
    ate: Optional[float] = Field(default=None, description="Average Treatment Effect")
    att: Optional[float] = Field(default=None, description="ATT (on treated)")
    atc: Optional[float] = Field(default=None, description="ATC (on control)")
    
    # Confidence
    confidence_interval: Optional[Tuple[float, float]] = Field(default=None)
    p_value: Optional[float] = Field(default=None)
    standard_error: Optional[float] = Field(default=None)
    
    # Method used
    estimator: str = Field(default="unknown", description="Estimation method")
    
    # Robustness
    refutation_passed: bool = Field(default=False)
    refutation_results: Dict[str, Any] = Field(default_factory=dict)
    
    # Interpretation
    is_significant: bool = Field(default=False)
    effect_size_interpretation: Optional[str] = Field(default=None)
    
    @computed_field
    @property
    def summary(self) -> str:
        """Human-readable summary"""
        if self.ate is None:
            return "No effect estimated"
        
        direction = "increases" if self.ate > 0 else "decreases"
        sig = "significantly" if self.is_significant else "non-significantly"
        
        return f"Treatment {sig} {direction} outcome by {abs(self.ate):.3f}"


# ============================================================================
# SENSITIVITY SCORE
# ============================================================================

class SensitivityScore(BaseModel):
    """Impact/sensitivity score for a variable"""
    
    node_id: str = Field(...)
    node_name: str = Field(...)
    
    # Scores
    impact_score: float = Field(..., ge=0, le=1, description="0-1 impact on outcome")
    volatility: float = Field(default=0, ge=0, le=1, description="0-1 instability")
    controllability: float = Field(default=1, ge=0, le=1, description="0-1 ease of intervention")
    
    # Confidence
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MODERATE)
    confidence_interval: Optional[Tuple[float, float]] = Field(default=None)
    
    # Ranking
    rank: Optional[int] = Field(default=None, description="Rank among all variables")
    
    # Alert
    is_critical: bool = Field(default=False, description="High impact + high volatility")
    alert_message: Optional[str] = Field(default=None)
    
    @computed_field
    @property
    def risk_score(self) -> float:
        """Combined risk score (high impact + high volatility = high risk)"""
        return self.impact_score * self.volatility


# ============================================================================
# COUNTERFACTUAL RESULT
# ============================================================================

class CounterfactualResult(BaseModel):
    """Result of a counterfactual query"""
    
    query_id: str = Field(...)
    
    # Factual
    factual_outcome: float = Field(..., description="What actually happened")
    
    # Counterfactual
    counterfactual_outcome: float = Field(..., description="What would have happened")
    
    # Difference
    effect: float = Field(..., description="Counterfactual - Factual")
    relative_effect: Optional[float] = Field(default=None, description="% change")
    
    # Confidence
    confidence_interval: Optional[Tuple[float, float]] = Field(default=None)
    
    # Interpretation
    interpretation: Optional[str] = Field(default=None)
    
    @computed_field
    @property
    def summary(self) -> str:
        """Human-readable summary"""
        direction = "higher" if self.effect > 0 else "lower"
        return f"Without intervention, outcome would be {abs(self.effect):.3f} {direction}"


# ============================================================================
# DECISION RECOMMENDATION
# ============================================================================

class DecisionRecommendation(BaseModel):
    """A recommendation for human decision (not a decision itself!)"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dag_id: str = Field(...)
    
    # Content
    title: str = Field(...)
    description: str = Field(...)
    
    # Evidence
    causal_effects: List[CausalEffect] = Field(default_factory=list)
    sensitivity_scores: List[SensitivityScore] = Field(default_factory=list)
    counterfactuals: List[CounterfactualResult] = Field(default_factory=list)
    
    # Key insights
    key_levers: List[str] = Field(default_factory=list, description="Most impactful variables")
    risks: List[str] = Field(default_factory=list, description="Key risks identified")
    
    # Confidence
    overall_confidence: ConfidenceLevel = Field(default=ConfidenceLevel.MODERATE)
    
    # Governance - CRITICAL
    requires_human_decision: bool = Field(default=True, description="Always True!")
    human_decision_made: bool = Field(default=False)
    decision_maker_id: Optional[str] = Field(default=None)
    decision_timestamp: Optional[datetime] = Field(default=None)
    decision_notes: Optional[str] = Field(default=None)
    
    # Audit
    created_at: datetime = Field(default_factory=datetime.utcnow)
    trace_id: Optional[str] = Field(default=None)
    synthetic: bool = Field(default=True)
    
    @computed_field
    @property
    def is_actionable(self) -> bool:
        """Check if recommendation has human decision"""
        return self.human_decision_made and self.decision_maker_id is not None
