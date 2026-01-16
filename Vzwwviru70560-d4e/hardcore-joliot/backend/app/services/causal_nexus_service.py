"""
═══════════════════════════════════════════════════════════════════════════════
ORIGIN — Causal Nexus Service (CHE·NU / AT·OM V76)
═══════════════════════════════════════════════════════════════════════════════

Purpose:
- Manage complex causal relationships between:
  - OriginNode (technology/practice)
  - HumanLegacy (belief/body/planet)
  - BioEvolution (mutation/env transformation/feedback)
  - CivilizationPillar + CustomEvolution (society & daily life)

Design Philosophy:
- Conservative: generates CANDIDATE links, not automatic truths
- Requires expert agent validation before persisting as facts
- Full traceability (Rule #6)

Integration:
- on node create/update => build candidate nexus map
- on expert validation => persist validated links
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID, uuid4
from enum import Enum

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.master_origin import (
    OriginNode,
    OriginMediaAsset,
    OriginCivilizationPillar,
    OriginCustomEvolution,
    OriginHumanLegacy,
    OriginBioEvolution,
    OriginExpertValidation,
    origin_causal_links,
    origin_universal_links,
)


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class LinkType(str, Enum):
    """Types of causal relationships"""
    ENABLES = "ENABLES"
    DERIVES_FROM = "DERIVES_FROM"
    CORRELATES_WITH = "CORRELATES_WITH"
    IMPACTS = "IMPACTS"
    FEEDBACKS = "FEEDBACKS"
    TRIGGERS = "TRIGGERS"


class FeedbackType(str, Enum):
    """Types of gene-culture feedback loops"""
    GENE_CULTURE = "GENE_CULTURE"
    BIOEVO_FEEDBACK = "BIOEVO_FEEDBACK"
    EPIGENETIC_ENV = "EPIGENETIC_ENV"
    NICHE_CONSTRUCTION = "NICHE_CONSTRUCTION"
    CULTURAL_SELECTION = "CULTURAL_SELECTION"


class ClaimStrength(str, Enum):
    """Evidence strength levels"""
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"
    ESTABLISHED = "established"


class ValidationStatus(str, Enum):
    """Validation lifecycle states"""
    PENDING = "pending"
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    VALIDATED = "validated"
    CONTESTED = "contested"
    ARCHIVED = "archived"


# Expert agents required for different domains
DOMAIN_EXPERTS = {
    "historical": ["ORIGIN_HISTORIAN", "ORIGIN_CHRONOS", "ORIGIN_SEARCHER"],
    "scientific": ["ORIGIN_SCIENTIST", "ORIGIN_TECH_ARCHITECT"],
    "genetic": ["GENOME_ARCHITECT", "BIO_ADAPT"],
    "environmental": ["ECO_SYSTEMIC_MAPPER", "GAIA_SENTINEL"],
    "civilization": ["EMPIRE_STRATEGIST", "LINGUIST_PHILOLOGIST", "ARCHI_TECT"],
    "anthropological": ["ETHNO_OBSERVER", "CRAFT_MASTER", "SOUL_CHRONICLER"],
    "media": ["SCENE_DIRECTOR", "VISUAL_ARCHIVIST", "GHOST_WRITER", "NARRATIVE_DESIGNER"],
}


# ═══════════════════════════════════════════════════════════════════════════════
# CAUSAL NEXUS SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

class CausalNexusService:
    """
    Service for managing complex causal relationships in the ORIGIN graph.
    
    Key Features:
    - Build candidate nexus maps from node metadata
    - Create/validate causal links with expert oversight
    - Manage gene-culture co-evolution relationships
    - Track environmental transformation feedback loops
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ═══════════════════════════════════════════════════════════════════════════
    # NODE OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_node(self, node_id: UUID) -> Optional[OriginNode]:
        """Get a node by ID with all relationships loaded."""
        result = await self.db.execute(
            select(OriginNode)
            .where(OriginNode.id == node_id)
            .options(
                selectinload(OriginNode.media_assets),
                selectinload(OriginNode.civilization_pillars),
                selectinload(OriginNode.customs),
                selectinload(OriginNode.legacies),
                selectinload(OriginNode.bio_evolutions),
            )
        )
        return result.scalar_one_or_none()
    
    async def create_node(
        self,
        name: str,
        created_by: UUID,
        epoch: Optional[str] = None,
        exact_date: Optional[str] = None,
        description: Optional[str] = None,
        metadata_json: Optional[Dict[str, Any]] = None,
        geopolitical_context: Optional[Dict[str, Any]] = None,
    ) -> OriginNode:
        """
        Create a new origin node with Rule #6 traceability.
        """
        node = OriginNode(
            id=uuid4(),
            name=name,
            epoch=epoch,
            exact_date=exact_date,
            description=description,
            metadata_json=metadata_json or {},
            geopolitical_context=geopolitical_context,
            created_by=created_by,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_validated=False,
            validation_status=ValidationStatus.PENDING.value,
        )
        
        self.db.add(node)
        await self.db.flush()
        
        return node
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CANDIDATE NEXUS BUILDER
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def build_nexus_candidates(self, node_id: UUID) -> Dict[str, Any]:
        """
        Build candidate causal connections based on node metadata.
        
        IMPORTANT: These are HYPOTHESES requiring expert validation.
        Do NOT auto-persist without human/agent review.
        
        Returns:
            Dict with node info, candidate links, and required experts
        """
        node = await self.get_node(node_id)
        if not node:
            raise ValueError(f"OriginNode {node_id} not found")
        
        meta = node.metadata_json or {}
        tags = set(meta.get("tags", []))
        name_lower = (node.name or "").lower()
        
        candidates: List[Dict[str, Any]] = []
        
        # ─────────────────────────────────────────────────────────────────────
        # FIRE & COOKING — Metabolic/Brain allocation hypothesis
        # ─────────────────────────────────────────────────────────────────────
        if "fire" in name_lower or "cooking" in tags or "cuisson" in tags:
            candidates.append({
                "candidate_id": str(uuid4()),
                "link_type": FeedbackType.BIOEVO_FEEDBACK.value,
                "hypothesis": (
                    "Cuisson des aliments → meilleure extraction énergétique → "
                    "potentielle réallocation énergétique (cerveau). Hypothèse à valider."
                ),
                "bio_fields": {
                    "genetic_mutation": None,
                    "biological_impact": "Hypothèse: changements métaboliques / énergie disponible",
                    "is_hypothesis": True,
                },
                "env_fields": {
                    "env_modification": "Fire management",
                    "biodiversity_shift": {"notes": "Impact écosystèmes locaux - à documenter"},
                },
                "evidence": {
                    "confidence": 0.4,
                    "claim_strength": ClaimStrength.WEAK.value,
                    "sources": [],
                    "peer_reviewed": False,
                },
                "requires_agents": ["GENOME_ARCHITECT", "ECO_SYSTEMIC_MAPPER", "ORIGIN_SCIENTIST"],
                "domain": "genetic",
            })
        
        # ─────────────────────────────────────────────────────────────────────
        # AGRICULTURE — Zoonoses & immune selection
        # ─────────────────────────────────────────────────────────────────────
        if "agriculture" in name_lower or "domestication" in tags or "farming" in tags:
            candidates.append({
                "candidate_id": str(uuid4()),
                "link_type": FeedbackType.GENE_CULTURE.value,
                "hypothesis": (
                    "Sédentarité + proximité animaux domestiques → pression pathogènes → "
                    "sélection immunitaire + épidémies récurrentes. Corrélation documentée."
                ),
                "bio_fields": {
                    "genetic_mutation": None,
                    "biological_impact": "Pression immunitaire accrue (à préciser par variants)",
                    "is_hypothesis": True,
                },
                "env_fields": {
                    "env_modification": "Irrigation / Deforestation / Settlements",
                    "biodiversity_shift": {
                        "domesticated": [],
                        "notes": "Liste d'espèces à compléter",
                    },
                },
                "evidence": {
                    "confidence": 0.5,
                    "claim_strength": ClaimStrength.MEDIUM.value,
                    "sources": [],
                    "peer_reviewed": False,
                },
                "requires_agents": ["GENOME_ARCHITECT", "GAIA_SENTINEL", "ORIGIN_HISTORIAN"],
                "domain": "genetic",
            })
        
        # ─────────────────────────────────────────────────────────────────────
        # DAIRY / CATTLE — Lactase persistence
        # ─────────────────────────────────────────────────────────────────────
        if any(kw in name_lower for kw in ["dairy", "milk", "cattle", "lait", "élevage"]) or \
           any(t in tags for t in ["dairy", "cattle", "milk", "pastoral"]):
            candidates.append({
                "candidate_id": str(uuid4()),
                "link_type": FeedbackType.GENE_CULTURE.value,
                "hypothesis": (
                    "Élevage laitier → avantage sélectif de la persistance de la lactase "
                    "dans certaines populations. Mutation LCT documentée."
                ),
                "bio_fields": {
                    "genetic_mutation": "Lactase persistence (LCT -13910*T)",
                    "biological_impact": "Digestion du lactose à l'âge adulte",
                    "is_hypothesis": False,  # Well-established
                },
                "env_fields": {
                    "env_modification": "Pastoralism / Grassland management",
                    "biodiversity_shift": {
                        "domesticated": ["cattle", "sheep", "goats"],
                        "notes": "Sélection animale pour production laitière",
                    },
                },
                "evidence": {
                    "confidence": 0.8,
                    "claim_strength": ClaimStrength.ESTABLISHED.value,
                    "sources": ["Burger et al. 2007", "Gerbault et al. 2011"],
                    "peer_reviewed": True,
                },
                "requires_agents": ["GENOME_ARCHITECT", "ORIGIN_SCIENTIST", "ORIGIN_COMPARATOR"],
                "domain": "genetic",
            })
        
        # ─────────────────────────────────────────────────────────────────────
        # DIGITAL / INTERNET — Epigenetic & behavioral effects
        # ─────────────────────────────────────────────────────────────────────
        if any(kw in name_lower for kw in ["digital", "internet", "smartphone", "numérique", "écran"]) or \
           any(t in tags for t in ["digital", "data", "screen", "tech"]):
            candidates.append({
                "candidate_id": str(uuid4()),
                "link_type": FeedbackType.EPIGENETIC_ENV.value,
                "hypothesis": (
                    "Environnement informationnel dense → stress/attention/sommeil → "
                    "modulation expression génique (épigénétique). Études préliminaires."
                ),
                "bio_fields": {
                    "genetic_mutation": None,
                    "biological_impact": "Stress, attention, rythmes circadiens (épigénétique potentielle)",
                    "is_hypothesis": True,
                },
                "env_fields": {
                    "env_modification": "Digital environment / Light pollution",
                    "biodiversity_shift": {"notes": "N/A - environnement anthropique"},
                },
                "evidence": {
                    "confidence": 0.3,
                    "claim_strength": ClaimStrength.WEAK.value,
                    "sources": [],
                    "peer_reviewed": False,
                },
                "requires_agents": ["GENOME_ARCHITECT", "BIO_ADAPT", "ETHNO_OBSERVER"],
                "domain": "genetic",
            })
        
        # ─────────────────────────────────────────────────────────────────────
        # WRITING / PRINTING — Civilization & cognitive effects
        # ─────────────────────────────────────────────────────────────────────
        if any(kw in name_lower for kw in ["writing", "printing", "écriture", "imprimerie", "alphabet"]):
            candidates.append({
                "candidate_id": str(uuid4()),
                "link_type": LinkType.IMPACTS.value,
                "hypothesis": (
                    "Écriture/Imprimerie → externalisation mémoire → changements cognitifs "
                    "et structures de pouvoir. Impact civilisationnel documenté."
                ),
                "civilization_impact": {
                    "category": "COMMUNICATION",
                    "migration_flow": None,
                    "tools_used": ["stylus", "papyrus", "printing press"],
                },
                "custom_impact": {
                    "custom_name": "Literacy practices",
                    "evolution_stage": "Mainstream",
                },
                "evidence": {
                    "confidence": 0.7,
                    "claim_strength": ClaimStrength.STRONG.value,
                    "sources": ["Goody 1977", "Ong 1982", "Eisenstein 1979"],
                    "peer_reviewed": True,
                },
                "requires_agents": ["LINGUIST_PHILOLOGIST", "ORIGIN_HISTORIAN", "ETHNO_OBSERVER"],
                "domain": "civilization",
            })
        
        # ─────────────────────────────────────────────────────────────────────
        # CLIMATE EVENTS — Planetary adaptation
        # ─────────────────────────────────────────────────────────────────────
        if any(kw in name_lower for kw in ["ice age", "dryas", "holocene", "climate", "glaciation"]):
            candidates.append({
                "candidate_id": str(uuid4()),
                "link_type": FeedbackType.NICHE_CONSTRUCTION.value,
                "hypothesis": (
                    "Événement climatique majeur → migrations / effondrements → "
                    "nouvelles stratégies adaptatives (technologiques & biologiques)."
                ),
                "legacy_impact": {
                    "planetary_event": node.name,
                    "adaptation_stage": "Biological → Technological → Cognitive",
                },
                "evidence": {
                    "confidence": 0.6,
                    "claim_strength": ClaimStrength.MEDIUM.value,
                    "sources": [],
                    "peer_reviewed": False,
                },
                "requires_agents": ["GAIA_SENTINEL", "ORIGIN_HISTORIAN", "BIO_ADAPT"],
                "domain": "environmental",
            })
        
        return {
            "node_id": str(node_id),
            "node_name": node.name,
            "epoch": node.epoch,
            "generated_at": datetime.utcnow().isoformat(),
            "candidates": candidates,
            "total_candidates": len(candidates),
            "note": (
                "CANDIDATS À VALIDER. Chaque hypothèse nécessite validation par "
                "experts avec sources avant insertion factuelle (Rule #6)."
            ),
            "validation_workflow": {
                "step_1": "Expert agents review candidates",
                "step_2": "Sources verification",
                "step_3": "Confidence scoring",
                "step_4": "Human approval checkpoint",
                "step_5": "Persist validated links",
            },
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LINK CREATION (After Validation)
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_causal_link(
        self,
        trigger_id: UUID,
        result_id: UUID,
        created_by: UUID,
        link_type: str = LinkType.ENABLES.value,
        link_strength: float = 1.0,
        description: Optional[str] = None,
        evidence: Optional[Dict[str, Any]] = None,
        validated_by_agent: Optional[str] = None,
    ) -> UUID:
        """
        Create a validated causal link between two nodes.
        
        IMPORTANT: Should only be called AFTER expert validation.
        """
        link_id = uuid4()
        
        await self.db.execute(
            origin_causal_links.insert().values(
                id=link_id,
                trigger_id=trigger_id,
                result_id=result_id,
                link_strength=link_strength,
                link_type=link_type,
                description=description,
                evidence=evidence or {},
                created_at=datetime.utcnow(),
                created_by=created_by,
                validated_by_agent=validated_by_agent,
                validation_timestamp=datetime.utcnow() if validated_by_agent else None,
            )
        )
        
        return link_id
    
    async def create_universal_link(
        self,
        from_type: str,
        from_id: UUID,
        to_type: str,
        to_id: UUID,
        relation: str,
        created_by: UUID,
        weight: float = 1.0,
        evidence: Optional[Dict[str, Any]] = None,
        validated_by_agent: Optional[str] = None,
    ) -> UUID:
        """
        Create a universal cross-entity link for graph visualization.
        """
        link_id = uuid4()
        
        await self.db.execute(
            origin_universal_links.insert().values(
                id=link_id,
                from_type=from_type,
                from_id=from_id,
                to_type=to_type,
                to_id=to_id,
                relation=relation,
                weight=weight,
                evidence=evidence or {},
                created_at=datetime.utcnow(),
                created_by=created_by,
                validated_by_agent=validated_by_agent,
            )
        )
        
        return link_id
    
    # ═══════════════════════════════════════════════════════════════════════════
    # BIO-EVOLUTION RECORDS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_bio_evolution(
        self,
        node_id: UUID,
        created_by: UUID,
        genetic_mutation: Optional[str] = None,
        biological_impact: Optional[str] = None,
        env_modification: Optional[str] = None,
        biodiversity_shift: Optional[Dict[str, Any]] = None,
        feedback_loop_description: Optional[str] = None,
        feedback_type: Optional[str] = None,
        evidence: Optional[Dict[str, Any]] = None,
        is_hypothesis: bool = True,
        confidence_level: float = 0.3,
        validated_by_agent: Optional[str] = None,
    ) -> OriginBioEvolution:
        """
        Create a bio-evolution record with mandatory evidence tracking.
        """
        bio_evo = OriginBioEvolution(
            id=uuid4(),
            node_id=node_id,
            genetic_mutation=genetic_mutation,
            biological_impact=biological_impact,
            env_modification=env_modification,
            biodiversity_shift=biodiversity_shift,
            feedback_loop_description=feedback_loop_description,
            feedback_type=feedback_type,
            evidence=evidence or {"sources": [], "confidence": confidence_level},
            is_hypothesis=is_hypothesis,
            confidence_level=confidence_level,
            created_at=datetime.utcnow(),
            created_by=created_by,
            validated_by_agent=validated_by_agent,
        )
        
        self.db.add(bio_evo)
        await self.db.flush()
        
        return bio_evo
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EXPERT VALIDATION (Rule #6)
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def record_expert_validation(
        self,
        entity_type: str,
        entity_id: UUID,
        agent_id: str,
        validation_type: str,  # approve | reject | request_revision | flag
        created_by: UUID,
        agent_role: Optional[str] = None,
        confidence: float = 0.5,
        notes: Optional[str] = None,
        sources_verified: Optional[List[Dict[str, Any]]] = None,
    ) -> OriginExpertValidation:
        """
        Record an expert agent's validation decision.
        
        This is the core of Rule #6 compliance: every validation
        is tracked with full traceability.
        """
        validation = OriginExpertValidation(
            id=uuid4(),
            entity_type=entity_type,
            entity_id=entity_id,
            agent_id=agent_id,
            agent_role=agent_role,
            validation_type=validation_type,
            confidence=confidence,
            notes=notes,
            sources_verified=sources_verified,
            created_at=datetime.utcnow(),
            created_by=created_by,
        )
        
        self.db.add(validation)
        await self.db.flush()
        
        # Update entity validation status if approved
        if validation_type == "approve":
            await self._update_entity_validation(entity_type, entity_id, agent_id)
        
        return validation
    
    async def _update_entity_validation(
        self,
        entity_type: str,
        entity_id: UUID,
        agent_id: str,
    ) -> None:
        """Update the entity's validation status after approval."""
        if entity_type == "node":
            node = await self.get_node(entity_id)
            if node:
                validated_by = node.validated_by or {"agent_ids": [], "timestamps": []}
                validated_by["agent_ids"].append(agent_id)
                validated_by["timestamps"].append(datetime.utcnow().isoformat())
                
                node.validated_by = validated_by
                node.is_validated = True
                node.validation_status = ValidationStatus.VALIDATED.value
                node.updated_at = datetime.utcnow()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GRAPH QUERIES
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def get_causal_chain(
        self,
        start_node_id: UUID,
        max_depth: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Traverse the causal graph from a starting node.
        Returns the chain of triggered effects up to max_depth.
        """
        chain = []
        visited = set()
        
        async def traverse(node_id: UUID, depth: int):
            if depth > max_depth or node_id in visited:
                return
            
            visited.add(node_id)
            node = await self.get_node(node_id)
            
            if node:
                # Get outgoing links
                result = await self.db.execute(
                    select(origin_causal_links).where(
                        origin_causal_links.c.trigger_id == node_id
                    )
                )
                links = result.fetchall()
                
                for link in links:
                    chain.append({
                        "depth": depth,
                        "trigger_id": str(node_id),
                        "trigger_name": node.name,
                        "result_id": str(link.result_id),
                        "link_type": link.link_type,
                        "link_strength": link.link_strength,
                    })
                    await traverse(link.result_id, depth + 1)
        
        await traverse(start_node_id, 0)
        return chain
    
    async def find_related_bio_evolutions(
        self,
        node_id: UUID,
    ) -> List[OriginBioEvolution]:
        """Find all bio-evolution records linked to a node."""
        result = await self.db.execute(
            select(OriginBioEvolution).where(
                OriginBioEvolution.node_id == node_id
            )
        )
        return list(result.scalars().all())
    
    async def get_node_full_context(
        self,
        node_id: UUID,
    ) -> Dict[str, Any]:
        """
        Get complete context for a node including all related entities.
        """
        node = await self.get_node(node_id)
        if not node:
            raise ValueError(f"OriginNode {node_id} not found")
        
        return {
            "node": {
                "id": str(node.id),
                "name": node.name,
                "epoch": node.epoch,
                "description": node.description,
                "metadata": node.metadata_json,
                "geopolitical_context": node.geopolitical_context,
                "validation_status": node.validation_status,
                "is_validated": node.is_validated,
                "validated_by": node.validated_by,
            },
            "media_assets": [
                {
                    "id": str(m.id),
                    "type": m.asset_type,
                    "title": m.title,
                    "status": m.production_status,
                }
                for m in node.media_assets
            ],
            "civilization_pillars": [
                {
                    "id": str(p.id),
                    "category": p.category,
                    "title": p.title,
                }
                for p in node.civilization_pillars
            ],
            "customs": [
                {
                    "id": str(c.id),
                    "name": c.custom_name,
                    "stage": c.evolution_stage,
                }
                for c in node.customs
            ],
            "legacies": [
                {
                    "id": str(l.id),
                    "belief_system": l.belief_system,
                    "planetary_event": l.planetary_event,
                }
                for l in node.legacies
            ],
            "bio_evolutions": [
                {
                    "id": str(b.id),
                    "genetic_mutation": b.genetic_mutation,
                    "env_modification": b.env_modification,
                    "is_hypothesis": b.is_hypothesis,
                    "confidence": b.confidence_level,
                }
                for b in node.bio_evolutions
            ],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    'CausalNexusService',
    'LinkType',
    'FeedbackType',
    'ClaimStrength',
    'ValidationStatus',
    'DOMAIN_EXPERTS',
]
