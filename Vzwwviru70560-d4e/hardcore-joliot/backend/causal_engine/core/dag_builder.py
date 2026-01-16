"""
============================================================================
CHE·NU™ V69 — CAUSAL DAG BUILDER
============================================================================
Version: 1.0.0
Purpose: Build and manage causal DAGs from WorldEngine data
Principle: GOUVERNANCE > EXÉCUTION
============================================================================
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import logging
import hashlib
import json

from .models import (
    CausalDAG,
    CausalNode,
    CausalEdge,
    NodeType,
    EdgeType,
    ConfidenceLevel,
    ValidationStatus,
)

logger = logging.getLogger(__name__)


# ============================================================================
# DAG BUILDER
# ============================================================================

class DAGBuilder:
    """
    Builder pattern for constructing causal DAGs.
    
    Usage:
        dag = (DAGBuilder("Supply Chain Model")
            .add_slot_node("price", "Product Price", domain=[0, 100])
            .add_slot_node("demand", "Customer Demand", domain=[0, 1000])
            .add_slot_node("revenue", "Total Revenue", node_type=NodeType.OUTCOME)
            .add_causal_edge("price", "demand", coefficient=-0.5)
            .add_causal_edge("demand", "revenue", coefficient=10.0)
            .set_simulation_id("sim-001")
            .build())
    """
    
    def __init__(
        self,
        name: str,
        tenant_id: Optional[str] = None,
        sphere: Optional[str] = None,
    ):
        self._dag = CausalDAG(
            name=name,
            tenant_id=tenant_id,
            sphere=sphere,
            synthetic=True,  # Always synthetic!
        )
        self._node_name_to_id: Dict[str, str] = {}
    
    def add_node(self, node: CausalNode) -> "DAGBuilder":
        """Add a pre-built node"""
        self._dag.add_node(node)
        self._node_name_to_id[node.name] = node.id
        return self
    
    def add_slot_node(
        self,
        name: str,
        description: Optional[str] = None,
        node_type: NodeType = NodeType.SLOT,
        domain: Optional[List[float]] = None,
        unit: Optional[str] = None,
        slot_id: Optional[str] = None,
        is_manipulable: bool = True,
        observed_value: Optional[float] = None,
    ) -> "DAGBuilder":
        """Add a slot-based node"""
        node = CausalNode(
            name=name,
            description=description or name,
            node_type=node_type,
            domain=domain,
            unit=unit,
            slot_id=slot_id,
            sphere=self._dag.sphere,
            is_manipulable=is_manipulable,
            observed_value=observed_value,
        )
        return self.add_node(node)
    
    def add_outcome_node(
        self,
        name: str,
        description: Optional[str] = None,
        unit: Optional[str] = None,
    ) -> "DAGBuilder":
        """Add an outcome (target) node"""
        return self.add_slot_node(
            name=name,
            description=description,
            node_type=NodeType.OUTCOME,
            unit=unit,
            is_manipulable=False,
        )
    
    def add_intervention_node(
        self,
        name: str,
        description: Optional[str] = None,
        domain: Optional[List[float]] = None,
    ) -> "DAGBuilder":
        """Add an intervention point node"""
        return self.add_slot_node(
            name=name,
            description=description,
            node_type=NodeType.INTERVENTION,
            domain=domain,
            is_manipulable=True,
        )
    
    def add_confounder_node(
        self,
        name: str,
        description: Optional[str] = None,
        is_observable: bool = True,
    ) -> "DAGBuilder":
        """Add a confounder (common cause) node"""
        node = CausalNode(
            name=name,
            description=description,
            node_type=NodeType.CONFOUNDER,
            is_observable=is_observable,
            sphere=self._dag.sphere,
        )
        return self.add_node(node)
    
    def add_latent_node(
        self,
        name: str,
        description: Optional[str] = None,
    ) -> "DAGBuilder":
        """Add an unobserved (latent) node"""
        node = CausalNode(
            name=name,
            description=description,
            node_type=NodeType.LATENT,
            is_observable=False,
            is_manipulable=False,
            sphere=self._dag.sphere,
        )
        return self.add_node(node)
    
    def add_causal_edge(
        self,
        source_name: str,
        target_name: str,
        coefficient: Optional[float] = None,
        confidence: ConfidenceLevel = ConfidenceLevel.HYPOTHETICAL,
        p_value: Optional[float] = None,
        lag: Optional[int] = None,
        description: Optional[str] = None,
    ) -> "DAGBuilder":
        """Add a causal edge by node names"""
        source_id = self._resolve_node_id(source_name)
        target_id = self._resolve_node_id(target_name)
        
        edge = CausalEdge(
            source_id=source_id,
            target_id=target_id,
            edge_type=EdgeType.CAUSAL,
            coefficient=coefficient,
            confidence=confidence,
            p_value=p_value,
            lag=lag,
            description=description,
        )
        
        self._dag.add_edge(edge)
        return self
    
    def add_confounded_edge(
        self,
        node1_name: str,
        node2_name: str,
        description: Optional[str] = None,
    ) -> "DAGBuilder":
        """Add a bidirectional (confounded) edge"""
        node1_id = self._resolve_node_id(node1_name)
        node2_id = self._resolve_node_id(node2_name)
        
        edge = CausalEdge(
            source_id=node1_id,
            target_id=node2_id,
            edge_type=EdgeType.CONFOUNDED,
            description=description,
        )
        
        self._dag.edges.append(edge)  # Don't use add_edge to skip cycle check
        return self
    
    def _resolve_node_id(self, name_or_id: str) -> str:
        """Resolve node name to ID"""
        # Check if it's already an ID
        if name_or_id in self._dag.nodes:
            return name_or_id
        
        # Check name mapping
        if name_or_id in self._node_name_to_id:
            return self._node_name_to_id[name_or_id]
        
        raise ValueError(f"Node not found: {name_or_id}")
    
    def set_simulation_id(self, simulation_id: str) -> "DAGBuilder":
        """Set source simulation ID"""
        self._dag.simulation_id = simulation_id
        return self
    
    def set_created_by(self, user_id: str) -> "DAGBuilder":
        """Set creator"""
        self._dag.created_by = user_id
        return self
    
    def set_version(self, version: str) -> "DAGBuilder":
        """Set version"""
        self._dag.version = version
        return self
    
    def set_description(self, description: str) -> "DAGBuilder":
        """Set description"""
        self._dag.description = description
        return self
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the DAG before building"""
        errors = []
        
        # Check for empty DAG
        if len(self._dag.nodes) == 0:
            errors.append("DAG has no nodes")
        
        # Check for valid DAG (no cycles)
        if not self._dag.is_valid_dag():
            errors.append("DAG contains cycles")
        
        # Check for at least one outcome
        outcomes = [n for n in self._dag.nodes.values() if n.node_type == NodeType.OUTCOME]
        if len(outcomes) == 0:
            errors.append("DAG has no outcome nodes")
        
        # Check for isolated nodes
        connected = set()
        for edge in self._dag.edges:
            connected.add(edge.source_id)
            connected.add(edge.target_id)
        
        isolated = set(self._dag.nodes.keys()) - connected
        if isolated and len(self._dag.nodes) > 1:
            errors.append(f"Isolated nodes: {isolated}")
        
        # Check synthetic flag
        if not self._dag.synthetic:
            errors.append("DAG must be synthetic=True (CHE·NU rule)")
        
        return len(errors) == 0, errors
    
    def build(self, validate: bool = True) -> CausalDAG:
        """Build the final DAG"""
        if validate:
            is_valid, errors = self.validate()
            if not is_valid:
                raise ValueError(f"Invalid DAG: {errors}")
        
        self._dag.updated_at = datetime.utcnow()
        return self._dag


# ============================================================================
# DAG MANAGER
# ============================================================================

class DAGManager:
    """
    Manage causal DAG lifecycle: storage, versioning, approval.
    
    NOTE: This is a mock in-memory implementation.
    Production would use persistent storage with signatures.
    """
    
    def __init__(self):
        self._dags: Dict[str, CausalDAG] = {}
        self._dag_versions: Dict[str, List[str]] = {}  # dag_id -> [version_ids]
    
    def store(self, dag: CausalDAG) -> str:
        """Store a DAG"""
        self._dags[dag.id] = dag
        
        # Track versions
        base_id = dag.id.split("_v")[0]
        if base_id not in self._dag_versions:
            self._dag_versions[base_id] = []
        self._dag_versions[base_id].append(dag.id)
        
        logger.info(f"Stored DAG {dag.id}: {dag.name} (v{dag.version})")
        return dag.id
    
    def get(self, dag_id: str) -> Optional[CausalDAG]:
        """Retrieve a DAG by ID"""
        return self._dags.get(dag_id)
    
    def get_latest(self, base_id: str) -> Optional[CausalDAG]:
        """Get latest version of a DAG"""
        versions = self._dag_versions.get(base_id, [])
        if not versions:
            return None
        return self._dags.get(versions[-1])
    
    def list_by_simulation(self, simulation_id: str) -> List[CausalDAG]:
        """List DAGs for a simulation"""
        return [
            dag for dag in self._dags.values()
            if dag.simulation_id == simulation_id
        ]
    
    def list_by_tenant(self, tenant_id: str) -> List[CausalDAG]:
        """List DAGs for a tenant"""
        return [
            dag for dag in self._dags.values()
            if dag.tenant_id == tenant_id
        ]
    
    def submit_for_approval(
        self,
        dag_id: str,
        submitted_by: str,
    ) -> bool:
        """Submit DAG for human approval"""
        dag = self.get(dag_id)
        if dag is None:
            return False
        
        if dag.status != ValidationStatus.DRAFT:
            logger.warning(f"DAG {dag_id} is not in DRAFT status")
            return False
        
        dag.status = ValidationStatus.PENDING_REVIEW
        dag.updated_at = datetime.utcnow()
        
        logger.info(f"DAG {dag_id} submitted for approval by {submitted_by}")
        return True
    
    def approve(
        self,
        dag_id: str,
        approver_id: str,
        notes: Optional[str] = None,
    ) -> bool:
        """Human approval of DAG (HITL)"""
        dag = self.get(dag_id)
        if dag is None:
            return False
        
        if dag.status != ValidationStatus.PENDING_REVIEW:
            logger.warning(f"DAG {dag_id} is not pending review")
            return False
        
        dag.status = ValidationStatus.APPROVED
        dag.approved_by = approver_id
        dag.approved_at = datetime.utcnow()
        dag.updated_at = datetime.utcnow()
        
        logger.info(f"DAG {dag_id} APPROVED by {approver_id}")
        return True
    
    def reject(
        self,
        dag_id: str,
        rejector_id: str,
        reason: str,
    ) -> bool:
        """Human rejection of DAG"""
        dag = self.get(dag_id)
        if dag is None:
            return False
        
        dag.status = ValidationStatus.REJECTED
        dag.updated_at = datetime.utcnow()
        
        logger.info(f"DAG {dag_id} REJECTED by {rejector_id}: {reason}")
        return True
    
    def archive(self, dag_id: str) -> bool:
        """Archive a DAG"""
        dag = self.get(dag_id)
        if dag is None:
            return False
        
        dag.status = ValidationStatus.ARCHIVED
        dag.updated_at = datetime.utcnow()
        
        logger.info(f"DAG {dag_id} archived")
        return True
    
    def verify_integrity(self, dag_id: str) -> Tuple[bool, Optional[str]]:
        """Verify DAG integrity via hash"""
        dag = self.get(dag_id)
        if dag is None:
            return False, "DAG not found"
        
        # Recompute hash and compare
        expected_hash = dag.hash
        # In production, compare against stored hash
        
        return True, expected_hash


# ============================================================================
# STRUCTURE LEARNING (MOCK)
# ============================================================================

class StructureLearner:
    """
    Learn causal structure from data.
    
    NOTE: This is a simplified mock. Production would use:
    - CausalNex for structure learning
    - DoWhy for causal inference
    - PC, FCI, GES algorithms
    """
    
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha  # Significance level
    
    def learn_from_data(
        self,
        data: Dict[str, List[float]],
        prior_edges: Optional[List[Tuple[str, str]]] = None,
    ) -> CausalDAG:
        """
        Learn DAG structure from observational data.
        
        Args:
            data: Dict of variable_name -> values
            prior_edges: Known edges to include
            
        Returns:
            CausalDAG with learned structure
        """
        builder = DAGBuilder("Learned DAG")
        
        # Add nodes for each variable
        for var_name, values in data.items():
            builder.add_slot_node(
                name=var_name,
                observed_value=sum(values) / len(values) if values else None,
            )
        
        # Add prior edges if provided
        if prior_edges:
            for source, target in prior_edges:
                builder.add_causal_edge(
                    source,
                    target,
                    confidence=ConfidenceLevel.STRONG,
                )
        
        # MOCK: Add some learned edges based on correlation
        # In production, use proper structure learning algorithms
        variables = list(data.keys())
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                # Mock correlation check
                corr = self._mock_correlation(data.get(var1, []), data.get(var2, []))
                if abs(corr) > 0.3:  # Threshold
                    # Direction heuristic (alphabetical as mock)
                    if var1 < var2:
                        builder.add_causal_edge(var1, var2, coefficient=corr)
                    else:
                        builder.add_causal_edge(var2, var1, coefficient=corr)
        
        return builder.build(validate=False)  # May have issues, needs human review
    
    def _mock_correlation(self, x: List[float], y: List[float]) -> float:
        """Mock correlation calculation"""
        if not x or not y or len(x) != len(y):
            return 0.0
        
        n = len(x)
        if n < 3:
            return 0.0
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = (sum((xi - mean_x) ** 2 for xi in x) / n) ** 0.5
        std_y = (sum((yi - mean_y) ** 2 for yi in y) / n) ** 0.5
        
        if std_x == 0 or std_y == 0:
            return 0.0
        
        return cov / (std_x * std_y)


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_dag_manager: Optional[DAGManager] = None


def get_dag_manager() -> DAGManager:
    """Get singleton DAG manager"""
    global _dag_manager
    if _dag_manager is None:
        _dag_manager = DAGManager()
    return _dag_manager
