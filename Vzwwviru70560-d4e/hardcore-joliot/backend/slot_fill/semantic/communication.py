"""
============================================================================
CHE·NU™ V69 — SEMANTIC AGENT COMMUNICATION
============================================================================
Spec: GPT1/CHE-NU_ENG_SEMANTIC_AGENT_COMMUNICATION.md

Objective: Replace verbose text/JSON exchanges with semantic messages:
- intention
- structure logique
- preuves minimales (truth sync)

All compatible with OPA governance.

Core Ontology (common language):
- Concept (ex: THERMAL_STRESS)
- State (ex: CRITICAL_THRESHOLD)
- Relation (ex: IMPACTS → STRUCTURAL_INTEGRITY)
- Scope (sphere / project / task)
- Confidence (calibrated + provenance)

Format: semantic_packet.v1.json
============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# CORE ONTOLOGY (per spec)
# ============================================================================

class ConceptCategory(str, Enum):
    """Categories of concepts in the ontology"""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    RISK = "risk"
    COMPLIANCE = "compliance"
    RESOURCE = "resource"
    TEMPORAL = "temporal"
    CAUSAL = "causal"
    QUALITY = "quality"


class RelationType(str, Enum):
    """Types of relations between concepts"""
    IMPACTS = "impacts"
    DEPENDS_ON = "depends_on"
    CAUSES = "causes"
    PREVENTS = "prevents"
    ENABLES = "enables"
    CORRELATES = "correlates"
    CONTAINS = "contains"
    DERIVED_FROM = "derived_from"


class StateType(str, Enum):
    """Types of states a concept can be in"""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
    THRESHOLD_EXCEEDED = "threshold_exceeded"
    IMPROVING = "improving"
    DEGRADING = "degrading"


# ============================================================================
# ONTOLOGY CONCEPTS
# ============================================================================

@dataclass
class Concept:
    """
    A concept in the ontology.
    
    Per spec: ex THERMAL_STRESS, STRUCTURAL_INTEGRITY
    """
    concept_id: str
    name: str
    category: ConceptCategory
    description: str = ""
    
    # Attributes
    attributes: Dict[str, Any] = field(default_factory=dict)
    
    # Validation
    allowed_states: Set[StateType] = field(default_factory=lambda: set(StateType))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "concept_id": self.concept_id,
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "attributes": self.attributes,
        }


@dataclass
class Relation:
    """
    A relation between concepts.
    
    Per spec: ex IMPACTS → STRUCTURAL_INTEGRITY
    """
    relation_id: str
    source_concept: str
    target_concept: str
    relation_type: RelationType
    strength: float = 1.0  # 0-1
    bidirectional: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "relation_id": self.relation_id,
            "source": self.source_concept,
            "target": self.target_concept,
            "type": self.relation_type.value,
            "strength": self.strength,
            "bidirectional": self.bidirectional,
        }


# ============================================================================
# SEMANTIC PACKET (per spec)
# ============================================================================

@dataclass
class SemanticPacket:
    """
    Semantic packet per spec: semantic_packet.v1.json
    
    Each message encodes:
    - Concept
    - State
    - Relation
    - Scope (sphere / project / task)
    - Confidence (calibrated + provenance)
    
    Also includes Truth-Sync (per spec section 3):
    - worldstate_hash
    - causal_graph_hash
    - opa_bundle_hash
    - evidence_refs
    """
    packet_id: str
    
    # Core semantic content
    concept: str
    state: StateType
    relations: List[Dict[str, Any]] = field(default_factory=list)
    
    # Scope
    scope: Dict[str, str] = field(default_factory=dict)  # sphere, project, task
    
    # Confidence (per spec)
    confidence: float = 0.0  # 0-1
    provenance: str = ""
    
    # Truth-Sync (per spec section 3)
    worldstate_hash: Optional[str] = None
    causal_graph_hash: Optional[str] = None
    opa_bundle_hash: Optional[str] = None
    evidence_refs: List[str] = field(default_factory=list)  # Signed artifact refs
    
    # Speculative flag (per spec rule)
    speculative: bool = False  # If true, must route to HITL
    
    # Metadata
    sender_id: str = ""
    recipient_id: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": "v1",
            "packet_id": self.packet_id,
            "concept": self.concept,
            "state": self.state.value,
            "relations": self.relations,
            "scope": self.scope,
            "confidence": self.confidence,
            "provenance": self.provenance,
            "truth_sync": {
                "worldstate_hash": self.worldstate_hash,
                "causal_graph_hash": self.causal_graph_hash,
                "opa_bundle_hash": self.opa_bundle_hash,
                "evidence_refs": self.evidence_refs,
            },
            "speculative": self.speculative,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "timestamp": self.timestamp.isoformat(),
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
    
    def requires_hitl(self) -> bool:
        """
        Per spec rule: agent that can't provide evidence must mark speculative=true
        and be routed to HITL.
        """
        return self.speculative or (
            not self.evidence_refs and self.confidence < 0.7
        )


# ============================================================================
# Z-LOGIC COMPRESSION (per spec section 2)
# ============================================================================

class ZLogicCompressor:
    """
    Z-Logic compression per spec.
    
    Objective: Pass from "1000 datapoints" to "1 semantic point"
    - extraction de patterns
    - quantification des relations
    - référence à un graphe causal (hash) plutôt que texte
    """
    
    def __init__(self):
        self._pattern_cache: Dict[str, str] = {}
    
    def compress(
        self,
        data: Dict[str, Any],
        causal_graph_hash: str = None,
    ) -> Dict[str, Any]:
        """
        Compress verbose data into semantic form.
        
        Returns compressed representation.
        """
        # Extract patterns
        patterns = self._extract_patterns(data)
        
        # Quantify relations
        relations = self._quantify_relations(data)
        
        # Create compressed packet
        return {
            "type": "z_compressed",
            "patterns": patterns,
            "relations": relations,
            "causal_ref": causal_graph_hash,
            "original_size": len(json.dumps(data)),
            "compressed_size": len(json.dumps(patterns)) + len(json.dumps(relations)),
        }
    
    def _extract_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract recurring patterns from data"""
        patterns = []
        
        # Simple pattern extraction (would be more sophisticated in production)
        if "values" in data and isinstance(data["values"], list):
            values = data["values"]
            if len(values) > 0:
                avg = sum(values) / len(values)
                trend = "increasing" if values[-1] > values[0] else "decreasing"
                
                patterns.append({
                    "type": "trend",
                    "direction": trend,
                    "mean": avg,
                    "samples": len(values),
                })
        
        return patterns
    
    def _quantify_relations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Quantify relations between variables"""
        relations = []
        
        if "correlations" in data:
            for key, value in data["correlations"].items():
                relations.append({
                    "type": "correlation",
                    "variables": key,
                    "strength": value,
                })
        
        return relations
    
    def decompress(self, compressed: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decompress (reconstruct approximate original).
        
        Note: Lossy - semantic compression discards details.
        """
        return {
            "reconstructed": True,
            "patterns": compressed.get("patterns", []),
            "note": "Decompressed from semantic representation (lossy)",
        }


# ============================================================================
# ONTOLOGY REGISTRY
# ============================================================================

class OntologyRegistry:
    """
    Registry for concepts and relations.
    
    Per spec: Define ontology v1 (100-300 concepts)
    """
    
    def __init__(self):
        self._concepts: Dict[str, Concept] = {}
        self._relations: Dict[str, Relation] = {}
        
        # Initialize base concepts
        self._init_base_concepts()
    
    def _init_base_concepts(self) -> None:
        """Initialize base ontology concepts"""
        base_concepts = [
            # Financial
            ("BUDGET", ConceptCategory.FINANCIAL, "Budget allocation"),
            ("COST", ConceptCategory.FINANCIAL, "Cost measurement"),
            ("REVENUE", ConceptCategory.FINANCIAL, "Revenue measurement"),
            ("PROFIT", ConceptCategory.FINANCIAL, "Profit calculation"),
            
            # Operational
            ("CAPACITY", ConceptCategory.OPERATIONAL, "System capacity"),
            ("THROUGHPUT", ConceptCategory.OPERATIONAL, "Processing throughput"),
            ("LATENCY", ConceptCategory.OPERATIONAL, "Response latency"),
            ("AVAILABILITY", ConceptCategory.OPERATIONAL, "System availability"),
            
            # Risk
            ("RISK_SCORE", ConceptCategory.RISK, "Overall risk score"),
            ("COMPLIANCE_RISK", ConceptCategory.RISK, "Compliance risk level"),
            ("FINANCIAL_RISK", ConceptCategory.RISK, "Financial risk level"),
            ("OPERATIONAL_RISK", ConceptCategory.RISK, "Operational risk level"),
            
            # Resource
            ("HUMAN_RESOURCE", ConceptCategory.RESOURCE, "Human resources"),
            ("COMPUTE_RESOURCE", ConceptCategory.RESOURCE, "Computing resources"),
            ("STORAGE_RESOURCE", ConceptCategory.RESOURCE, "Storage resources"),
            
            # Quality
            ("QUALITY_SCORE", ConceptCategory.QUALITY, "Quality measurement"),
            ("ACCURACY", ConceptCategory.QUALITY, "Accuracy level"),
            ("COMPLETENESS", ConceptCategory.QUALITY, "Completeness level"),
        ]
        
        for concept_id, category, description in base_concepts:
            self.register_concept(Concept(
                concept_id=concept_id,
                name=concept_id.replace("_", " ").title(),
                category=category,
                description=description,
            ))
    
    def register_concept(self, concept: Concept) -> None:
        """Register a concept"""
        self._concepts[concept.concept_id] = concept
    
    def register_relation(self, relation: Relation) -> None:
        """Register a relation"""
        self._relations[relation.relation_id] = relation
    
    def get_concept(self, concept_id: str) -> Optional[Concept]:
        """Get concept by ID"""
        return self._concepts.get(concept_id)
    
    def get_concepts_by_category(
        self,
        category: ConceptCategory,
    ) -> List[Concept]:
        """Get all concepts in a category"""
        return [
            c for c in self._concepts.values()
            if c.category == category
        ]
    
    def validate_concept(self, concept_id: str) -> bool:
        """Check if concept exists in ontology"""
        return concept_id in self._concepts
    
    def get_stats(self) -> Dict[str, int]:
        """Get ontology statistics"""
        return {
            "total_concepts": len(self._concepts),
            "total_relations": len(self._relations),
            "categories": len(set(c.category for c in self._concepts.values())),
        }


# ============================================================================
# SEMANTIC ENCODER/DECODER
# ============================================================================

class SemanticCodec:
    """
    Encode/decode semantic packets.
    
    Per spec: Add encode/decode libs
    """
    
    def __init__(self, ontology: OntologyRegistry = None):
        self.ontology = ontology or OntologyRegistry()
        self.compressor = ZLogicCompressor()
    
    def encode(
        self,
        concept: str,
        state: StateType,
        scope: Dict[str, str],
        confidence: float,
        sender_id: str,
        recipient_id: str,
        relations: List[Dict[str, Any]] = None,
        evidence_refs: List[str] = None,
        worldstate_hash: str = None,
    ) -> SemanticPacket:
        """Encode data into semantic packet"""
        import uuid
        
        # Validate concept
        if not self.ontology.validate_concept(concept):
            logger.warning(f"Unknown concept: {concept}")
        
        # Check if speculative (no evidence)
        speculative = not evidence_refs and confidence < 0.7
        
        return SemanticPacket(
            packet_id=str(uuid.uuid4()),
            concept=concept,
            state=state,
            relations=relations or [],
            scope=scope,
            confidence=confidence,
            provenance=sender_id,
            worldstate_hash=worldstate_hash,
            evidence_refs=evidence_refs or [],
            speculative=speculative,
            sender_id=sender_id,
            recipient_id=recipient_id,
        )
    
    def decode(self, packet: SemanticPacket) -> Dict[str, Any]:
        """Decode semantic packet to structured data"""
        concept = self.ontology.get_concept(packet.concept)
        
        return {
            "concept": packet.concept,
            "concept_details": concept.to_dict() if concept else None,
            "state": packet.state.value,
            "scope": packet.scope,
            "confidence": packet.confidence,
            "requires_hitl": packet.requires_hitl(),
            "has_evidence": len(packet.evidence_refs) > 0,
        }
    
    def compress_and_encode(
        self,
        verbose_data: Dict[str, Any],
        concept: str,
        state: StateType,
        sender_id: str,
        recipient_id: str,
    ) -> Tuple[SemanticPacket, Dict[str, Any]]:
        """Compress verbose data and create semantic packet"""
        # Compress
        compressed = self.compressor.compress(verbose_data)
        
        # Create packet
        packet = self.encode(
            concept=concept,
            state=state,
            scope={"source": "compressed"},
            confidence=0.8,
            sender_id=sender_id,
            recipient_id=recipient_id,
        )
        
        return packet, compressed


# ============================================================================
# GOVERNANCE HOOKS (per spec section 6)
# ============================================================================

class SemanticGovernance:
    """
    OPA governance hooks for semantic communication.
    
    Per spec policies:
    - allowed concepts per sphere
    - block disallowed relations (discrimination, unsafe)
    - require evidence on high-impact packets
    """
    
    def __init__(self):
        # Allowed concepts per sphere
        self._sphere_concepts: Dict[str, Set[str]] = {
            "personal": {"BUDGET", "QUALITY_SCORE"},
            "business": set(),  # All allowed
            "government": {"COMPLIANCE_RISK", "RISK_SCORE"},
        }
        
        # Blocked relations
        self._blocked_relations: Set[str] = {
            "discriminates",
            "harms",
            "violates",
        }
        
        # High-impact concepts requiring evidence
        self._evidence_required: Set[str] = {
            "FINANCIAL_RISK",
            "COMPLIANCE_RISK",
            "REVENUE",
            "PROFIT",
        }
    
    def validate_packet(
        self,
        packet: SemanticPacket,
        sphere: str = None,
    ) -> Tuple[bool, List[str]]:
        """
        Validate packet against governance rules.
        
        Returns (is_valid, errors).
        """
        errors = []
        
        # Check concept allowed in sphere
        if sphere and sphere in self._sphere_concepts:
            allowed = self._sphere_concepts[sphere]
            if allowed and packet.concept not in allowed:
                errors.append(
                    f"Concept {packet.concept} not allowed in sphere {sphere}"
                )
        
        # Check blocked relations
        for rel in packet.relations:
            rel_type = rel.get("type", "")
            if rel_type.lower() in self._blocked_relations:
                errors.append(f"Blocked relation type: {rel_type}")
        
        # Check evidence requirement
        if packet.concept in self._evidence_required:
            if not packet.evidence_refs:
                errors.append(
                    f"Concept {packet.concept} requires evidence"
                )
        
        return len(errors) == 0, errors
    
    def check_speculative(self, packet: SemanticPacket) -> bool:
        """
        Check if packet should be marked speculative.
        
        Per spec: agent without proof must mark speculative=true
        """
        return packet.requires_hitl()


# ============================================================================
# SEMANTIC COMMUNICATION CHANNEL
# ============================================================================

class SemanticChannel:
    """
    Communication channel for semantic packets.
    """
    
    def __init__(
        self,
        codec: SemanticCodec = None,
        governance: SemanticGovernance = None,
    ):
        self.codec = codec or SemanticCodec()
        self.governance = governance or SemanticGovernance()
        self._message_log: List[SemanticPacket] = []
    
    def send(
        self,
        packet: SemanticPacket,
        sphere: str = None,
    ) -> Tuple[bool, List[str]]:
        """Send a semantic packet"""
        # Validate
        is_valid, errors = self.governance.validate_packet(packet, sphere)
        
        if not is_valid:
            logger.warning(f"Packet validation failed: {errors}")
            return False, errors
        
        # Log
        self._message_log.append(packet)
        
        logger.debug(
            f"Sent semantic packet {packet.packet_id}: "
            f"{packet.concept} -> {packet.recipient_id}"
        )
        
        return True, []
    
    def get_messages(
        self,
        recipient_id: str = None,
        concept: str = None,
    ) -> List[SemanticPacket]:
        """Get messages with optional filters"""
        messages = self._message_log
        
        if recipient_id:
            messages = [m for m in messages if m.recipient_id == recipient_id]
        
        if concept:
            messages = [m for m in messages if m.concept == concept]
        
        return messages
    
    def get_stats(self) -> Dict[str, Any]:
        """Get channel statistics"""
        return {
            "total_messages": len(self._message_log),
            "speculative_count": sum(
                1 for m in self._message_log if m.speculative
            ),
            "hitl_required": sum(
                1 for m in self._message_log if m.requires_hitl()
            ),
        }


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_ontology() -> OntologyRegistry:
    """Create ontology registry"""
    return OntologyRegistry()


def create_codec(ontology: OntologyRegistry = None) -> SemanticCodec:
    """Create semantic codec"""
    return SemanticCodec(ontology)


def create_channel() -> SemanticChannel:
    """Create semantic communication channel"""
    return SemanticChannel()
