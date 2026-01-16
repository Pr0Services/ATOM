"""
═══════════════════════════════════════════════════════════════════════════════
AT-OM MAPPING SYSTEM — Services (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Contains:
- CausalNexusService: Link suggestions and evidence gating
- ResonanceEngine: Cross-dimension resonance suggestions
- GlobalSynapse: Orchestration layer
- GematriaService: Numeric signatures (CREATIVE LAYER)
- HarmonicSynchronizer: Gold node detection (CREATIVE LAYER)

Evidence-first design with human-in-the-loop validation.
"""

from __future__ import annotations

import re
import unicodedata
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.atom_models import (
    ATOMNode, EncyclopediaEntry, atom_causal_links,
    AtomSensoryProfile, AtomPsychoEmotionalProfile,
    AtomResourceFootprint, AtomConceptualDrift,
    AtomLogisticsNetwork, AtomHarmonicSignature
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CAUSAL NEXUS SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CausalLinkCandidateDTO:
    """Data transfer object for causal link candidate."""
    trigger_id: str
    result_id: str
    link_type: str
    strength: float = 1.0
    confidence: float = 0.5
    rationale: str = ""
    provenance: Optional[List[Dict[str, Any]]] = None


class CausalNexusService:
    """
    Provides:
    - Candidate link generation (suggestions)
    - Evidence gating helpers (no 'strong' links without provenance)
    - Temporal coherence checks
    
    This service is intentionally CONSERVATIVE: it suggests, but does not assert.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    # ─────────────────────────────────────────────────────────────────────────
    # LINK SUGGESTIONS
    # ─────────────────────────────────────────────────────────────────────────
    
    async def suggest_links(self, node_id: UUID) -> List[CausalLinkCandidateDTO]:
        """
        Return conservative candidates based on existing node data.
        
        Uses dimension matching and epoch proximity as heuristics.
        All candidates are SUGGESTIONS requiring human review.
        """
        candidates = []
        
        # Get the source node
        result = await self.session.execute(
            select(ATOMNode).where(ATOMNode.id == node_id)
        )
        source_node = result.scalar_one_or_none()
        
        if not source_node:
            return candidates
        
        # Find potentially related nodes
        query = select(ATOMNode).where(
            and_(
                ATOMNode.id != node_id,
                or_(
                    ATOMNode.dimension == source_node.dimension,
                    ATOMNode.epoch == source_node.epoch
                )
            )
        ).limit(20)
        
        result = await self.session.execute(query)
        related_nodes = result.scalars().all()
        
        for related in related_nodes:
            # Calculate basic similarity score
            confidence = 0.3  # Start conservative
            reasons = []
            
            if related.dimension == source_node.dimension:
                confidence += 0.1
                reasons.append(f"Same dimension: {source_node.dimension}")
            
            if related.epoch == source_node.epoch:
                confidence += 0.1
                reasons.append(f"Same epoch: {source_node.epoch}")
            
            # Check for keyword overlap in descriptions
            if source_node.description and related.description:
                overlap = self._keyword_overlap(
                    source_node.description, 
                    related.description
                )
                if overlap > 0.2:
                    confidence += 0.1
                    reasons.append("Keyword overlap in descriptions")
            
            if confidence > 0.3:
                candidates.append(CausalLinkCandidateDTO(
                    trigger_id=str(source_node.id),
                    result_id=str(related.id),
                    link_type=self._infer_link_type(source_node.dimension),
                    strength=1.0,
                    confidence=min(confidence, 0.6),  # Cap at 0.6 for suggestions
                    rationale="; ".join(reasons),
                    provenance=None  # Suggestions don't have provenance yet
                ))
        
        return candidates
    
    def _keyword_overlap(self, text1: str, text2: str) -> float:
        """Simple keyword overlap ratio."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def _infer_link_type(self, dimension: Optional[str]) -> str:
        """Infer link type from dimension."""
        mapping = {
            "PHYSICAL": "TECH",
            "BIOLOGICAL": "BIO",
            "SOCIAL": "SOCIAL",
            "SPIRITUAL": "SPIRITUAL",
            "CONCEPTUAL": "CONCEPT",
            "ECOLOGICAL": "ECO",
            "LOGISTICAL": "LOGISTICS",
            "SENSORY": "SENSORY",
        }
        return mapping.get(dimension, "TECH")
    
    # ─────────────────────────────────────────────────────────────────────────
    # EVIDENCE GATING
    # ─────────────────────────────────────────────────────────────────────────
    
    def validate_link_evidence(
        self, 
        candidate: CausalLinkCandidateDTO
    ) -> Tuple[bool, str]:
        """
        Gate strong claims: if confidence is high, require provenance.
        
        Returns:
            Tuple of (is_valid, reason)
        """
        if candidate.confidence >= 0.75 and not candidate.provenance:
            return False, "High-confidence link (>=0.75) requires provenance sources."
        
        if candidate.confidence >= 0.9:
            # Very high confidence requires multiple sources
            if not candidate.provenance or len(candidate.provenance) < 2:
                return False, "Very high confidence (>=0.9) requires at least 2 provenance sources."
        
        return True, "OK"
    
    # ─────────────────────────────────────────────────────────────────────────
    # TEMPORAL COHERENCE
    # ─────────────────────────────────────────────────────────────────────────
    
    def prevent_temporal_anachronism(
        self,
        trigger_range: Optional[Dict[str, str]],
        result_range: Optional[Dict[str, str]]
    ) -> Tuple[bool, str]:
        """
        Basic temporal ordering check.
        
        Cause must precede or overlap with effect.
        Unknown ranges are permissible but flagged.
        """
        if not trigger_range or not result_range:
            return True, "Unknown date ranges - manual verification recommended"
        
        try:
            trigger_to = int(trigger_range.get("to", "0"))
            result_from = int(result_range.get("from", "0"))
            
            if trigger_to < result_from:
                # Normal causality: trigger ends before effect begins
                return True, "OK - Temporal ordering valid"
            elif trigger_to > result_from:
                # Possible overlap or reverse causality
                trigger_from = int(trigger_range.get("from", trigger_to))
                if trigger_from <= result_from:
                    return True, "OK - Overlapping periods"
                else:
                    return False, f"Potential anachronism: trigger ({trigger_range}) appears after result ({result_range})"
            else:
                return True, "OK - Concurrent events"
                
        except (ValueError, TypeError):
            return True, "Unable to parse date ranges - manual verification recommended"
    
    # ─────────────────────────────────────────────────────────────────────────
    # CRUD OPERATIONS
    # ─────────────────────────────────────────────────────────────────────────
    
    async def create_link(
        self,
        trigger_id: UUID,
        result_id: UUID,
        link_type: str,
        strength: float = 1.0,
        confidence: float = 0.5,
        rationale: Optional[str] = None,
        provenance: Optional[List[Dict]] = None,
        created_by: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """Create a new causal link with validation."""
        
        # Validate evidence
        candidate = CausalLinkCandidateDTO(
            trigger_id=str(trigger_id),
            result_id=str(result_id),
            link_type=link_type,
            strength=strength,
            confidence=confidence,
            rationale=rationale or "",
            provenance=provenance
        )
        
        is_valid, reason = self.validate_link_evidence(candidate)
        if not is_valid:
            raise ValueError(reason)
        
        # Insert link
        link_id = uuid4()
        stmt = atom_causal_links.insert().values(
            id=link_id,
            trigger_id=trigger_id,
            result_id=result_id,
            link_type=link_type,
            strength=strength,
            confidence=confidence,
            rationale=rationale,
            provenance=provenance,
            created_by=created_by,
            created_at=datetime.utcnow()
        )
        
        await self.session.execute(stmt)
        await self.session.commit()
        
        return {
            "id": str(link_id),
            "trigger_id": str(trigger_id),
            "result_id": str(result_id),
            "link_type": link_type,
            "confidence": confidence,
            "created_at": datetime.utcnow().isoformat()
        }
    
    async def get_links_for_node(self, node_id: UUID) -> List[Dict[str, Any]]:
        """Get all causal links involving a node."""
        stmt = select(atom_causal_links).where(
            or_(
                atom_causal_links.c.trigger_id == node_id,
                atom_causal_links.c.result_id == node_id
            )
        )
        
        result = await self.session.execute(stmt)
        rows = result.fetchall()
        
        return [
            {
                "id": str(row.id),
                "trigger_id": str(row.trigger_id),
                "result_id": str(row.result_id),
                "link_type": row.link_type,
                "strength": row.strength,
                "confidence": row.confidence,
                "rationale": row.rationale,
                "provenance": row.provenance,
                "created_at": row.created_at.isoformat() if row.created_at else None
            }
            for row in rows
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# RESONANCE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ResonanceSuggestionDTO:
    """Data transfer object for resonance suggestion."""
    node_id: str
    module: str  # sensory | psychology | resources | concepts | logistics
    payload: Dict[str, Any]
    confidence: float = 0.5
    rationale: str = ""
    provenance: Optional[List[Dict[str, Any]]] = None


class ResonanceEngine:
    """
    Proposes cross-dimension resonance when a node is created/updated.
    
    Output is SUGGESTIONS ONLY, designed for human + expert agent review.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def suggest(self, node_id: UUID) -> List[ResonanceSuggestionDTO]:
        """
        Generate resonance suggestions for a node.
        
        Analyzes existing data and suggests missing dimension data.
        """
        suggestions = []
        
        # Get node with all profiles
        result = await self.session.execute(
            select(ATOMNode)
            .options(
                selectinload(ATOMNode.sensory_profile),
                selectinload(ATOMNode.psycho_profile),
                selectinload(ATOMNode.resource_footprint),
                selectinload(ATOMNode.conceptual_drift),
                selectinload(ATOMNode.logistics_network),
            )
            .where(ATOMNode.id == node_id)
        )
        node = result.scalar_one_or_none()
        
        if not node:
            return suggestions
        
        # Suggest missing dimensions based on node type
        if not node.sensory_profile and node.technical_specs:
            suggestions.append(ResonanceSuggestionDTO(
                node_id=str(node_id),
                module="sensory",
                payload={
                    "suggestion": "Add ergonomics/acoustics data",
                    "reason": "Technical specs present but no sensory profile"
                },
                confidence=0.4,
                rationale="Technology nodes often have sensory implications"
            ))
        
        if not node.resource_footprint and node.dimension == "PHYSICAL":
            suggestions.append(ResonanceSuggestionDTO(
                node_id=str(node_id),
                module="resources",
                payload={
                    "suggestion": "Add material/supply chain data",
                    "reason": "Physical dimension suggests resource requirements"
                },
                confidence=0.4,
                rationale="Physical entities typically have resource footprints"
            ))
        
        if not node.conceptual_drift and node.dimension == "CONCEPTUAL":
            suggestions.append(ResonanceSuggestionDTO(
                node_id=str(node_id),
                module="concepts",
                payload={
                    "suggestion": "Add etymological/semantic evolution data",
                    "reason": "Conceptual dimension should track meaning drift"
                },
                confidence=0.5,
                rationale="Concepts evolve over time"
            ))
        
        if not node.logistics_network and node.location:
            suggestions.append(ResonanceSuggestionDTO(
                node_id=str(node_id),
                module="logistics",
                payload={
                    "suggestion": "Add trade routes/network connections",
                    "reason": "Location data suggests logistical context"
                },
                confidence=0.3,
                rationale="Geographic entities often have logistical networks"
            ))
        
        return suggestions
    
    def minimum_fields(self) -> Dict[str, List[str]]:
        """Defines expected keys per module for consistency checks."""
        return {
            "sensory": ["ergonomics", "acoustics"],
            "psychology": ["psycho_emotional", "counter_signals", "uncertainty_notes"],
            "resources": ["resource_footprint"],
            "concepts": ["conceptual_drift"],
            "logistics": ["logistics_networks"],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# GEMATRIA SERVICE (CREATIVE LAYER)
# ═══════════════════════════════════════════════════════════════════════════════

def normalize_text(s: str) -> str:
    """Lowercase + strip accents + keep alphanumerics/spaces."""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# A1Z26 mapping (simple)
A1Z26: Dict[str, int] = {chr(ord("a") + i): i + 1 for i in range(26)}

# Pythagorean mapping (cycles 1-9)
PYTHAGOREAN: Dict[str, int] = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
    'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
    's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
}

# Master numbers (preserved in theosophical reduction)
MASTER_NUMBERS = {11, 22, 33}

# Golden ratio
PHI = (1 + 5**0.5) / 2


class NumerologyEngine:
    """
    Advanced Numerology Engine with dual mapping systems and Sacred Geometry.
    
    ⚠️ CRITICAL DISCLAIMER:
    - This is a CREATIVE/INTERPRETIVE tool for film/game/art projects.
    - It is NOT scientifically validated.
    - It makes NO factual claims about reality.
    - The "frequencies" and "coordinates" are symbolic, not physical.
    - Human review is REQUIRED before any public display.
    
    Methods:
    - calculate_gematria(): Both A1Z26 and Pythagorean with theosophical reduction
    - get_sacred_geometry_coords(): Phi-based spiral coordinates
    - analyze(): Full analysis with all methods
    
    Supported Systems:
    - A1Z26: Standard mapping (A=1, B=2, ... Z=26) → AT-OM = 49
    - Pythagorean: Cyclic mapping (1-9 cycles) → AT-OM = 13
    - Both reduce to same value via theosophical reduction
    """
    
    DISCLAIMER = (
        "⚠️ CREATIVE LAYER ONLY: This numerology engine is for artistic/narrative "
        "purposes (film, games, storytelling). It is NOT scientific and makes NO "
        "factual claims. All outputs are INTERPRETIVE and require human review."
    )
    
    def __init__(self):
        self.pythagorean_map = PYTHAGOREAN.copy()
        self.a1z26_map = A1Z26.copy()
    
    def calculate_gematria(self, text: str, method: str = "both") -> Dict[str, Any]:
        """
        Calculate gematria with theosophical reduction.
        
        Args:
            text: Input text to analyze
            method: "a1z26", "pythagorean", or "both" (default)
            
        Returns:
            Dict with raw sum(s) and reduced value (preserving master numbers)
            
        Examples:
            "AT-OM" with A1Z26: raw=49 → 13 → 4
            "AT-OM" with Pythagorean: raw=13 → 4
        """
        cleaned = text.lower().replace("-", "").replace(" ", "")
        
        result: Dict[str, Any] = {
            "text": text,
            "cleaned": cleaned,
            "is_interpretive": True
        }
        
        # A1Z26 calculation
        if method in ("a1z26", "both"):
            a1z26_raw = sum(self.a1z26_map.get(char, 0) for char in cleaned)
            a1z26_reduced, a1z26_path = self._reduce_with_path(a1z26_raw)
            result["a1z26"] = {
                "raw": a1z26_raw,
                "reduced": a1z26_reduced,
                "reduction_path": a1z26_path,
                "is_master_number": a1z26_reduced in MASTER_NUMBERS
            }
        
        # Pythagorean calculation
        if method in ("pythagorean", "both"):
            pyth_raw = sum(self.pythagorean_map.get(char, 0) for char in cleaned)
            pyth_reduced, pyth_path = self._reduce_with_path(pyth_raw)
            result["pythagorean"] = {
                "raw": pyth_raw,
                "reduced": pyth_reduced,
                "reduction_path": pyth_path,
                "is_master_number": pyth_reduced in MASTER_NUMBERS
            }
        
        # Final reduced value (both methods converge)
        if "a1z26" in result:
            result["reduced"] = result["a1z26"]["reduced"]
        elif "pythagorean" in result:
            result["reduced"] = result["pythagorean"]["reduced"]
        
        return result
    
    def _reduce_with_path(self, value: int) -> Tuple[int, List[int]]:
        """Theosophical reduction with path tracking."""
        path = [value]
        current = value
        while current > 9 and current not in MASTER_NUMBERS:
            current = sum(int(digit) for digit in str(current))
            path.append(current)
        return current, path
    
    def get_sacred_geometry_coords(self, value: int) -> Dict[str, float]:
        """
        Generate phi-based spiral coordinates for visualization.
        
        Args:
            value: Reduced numerology value (1-9 or master number)
            
        Returns:
            Dict with x, y coordinates and symbolic frequency
            
        ⚠️ These are SYMBOLIC positions for art/visualization, not physics.
        """
        import math
        
        # Position on the cycle of 9
        angle = value * (360 / 9)
        
        # Phi-based spiral expansion
        radius = math.pow(PHI, value / 3)
        
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        
        # Symbolic frequency (NOT physical Hz)
        frequency = value * 111.1
        
        return {
            "x": round(x, 4),
            "y": round(y, 4),
            "angle_degrees": angle,
            "radius": round(radius, 4),
            "frequency_symbolic": round(frequency, 1),
            "is_interpretive": True,
            "note": "Coordinates are symbolic for visualization, not physical positions"
        }
    
    def get_number_meaning(self, value: int) -> Dict[str, Any]:
        """
        Get symbolic meaning of a number (for creative narratives).
        
        ⚠️ These are traditional interpretations, not facts.
        """
        meanings = {
            1: {"archetype": "Beginning", "element": "Fire", "planet": "Sun"},
            2: {"archetype": "Duality", "element": "Water", "planet": "Moon"},
            3: {"archetype": "Creation", "element": "Fire", "planet": "Jupiter"},
            4: {"archetype": "Foundation", "element": "Earth", "planet": "Uranus"},
            5: {"archetype": "Change", "element": "Air", "planet": "Mercury"},
            6: {"archetype": "Harmony", "element": "Earth", "planet": "Venus"},
            7: {"archetype": "Mystery", "element": "Water", "planet": "Neptune"},
            8: {"archetype": "Power", "element": "Earth", "planet": "Saturn"},
            9: {"archetype": "Completion", "element": "Fire", "planet": "Mars"},
            11: {"archetype": "Illumination", "element": "Air", "planet": "Pluto", "is_master": True},
            22: {"archetype": "Master Builder", "element": "Earth", "planet": "Vulcan", "is_master": True},
            33: {"archetype": "Master Teacher", "element": "Water", "planet": "Neptune", "is_master": True},
        }
        
        meaning = meanings.get(value, {"archetype": "Unknown", "element": "Unknown", "planet": "Unknown"})
        meaning["is_interpretive"] = True
        meaning["note"] = "Traditional symbolic associations, not factual claims"
        
        return meaning


class GematriaService:
    """
    Unified Gematria / Numerology Service (CREATIVE LAYER).
    
    Combines:
    - Simple A1Z26 mapping
    - ASCII sums
    - Pythagorean numerology with theosophical reduction
    - Sacred geometry coordinates
    
    ⚠️ IMPORTANT:
    - This is NOT a scientific validation tool.
    - Treat outputs as INTERPRETIVE/CREATIVE metadata for film/game UX.
    - Never present results as factual causation or "truth".
    - Always provide disclaimers in UI.
    """
    
    DISCLAIMER = (
        "This is a creative/interpretive tool, not scientific analysis. "
        "All numeric patterns are coincidental and carry no causal meaning."
    )
    
    def __init__(self):
        self.numerology = NumerologyEngine()
    
    def a1z26_sum(self, text: str) -> int:
        """Simple A=1, Z=26 sum."""
        t = normalize_text(text).replace(" ", "")
        return sum(A1Z26.get(ch, 0) for ch in t)
    
    def ascii_sum(self, text: str) -> int:
        """Sum of ASCII values."""
        t = normalize_text(text)
        return sum(ord(ch) for ch in t)
    
    def token_sums(self, text: str) -> Dict[str, int]:
        """Return per-token A1Z26 sums."""
        tokens = normalize_text(text).split()
        return {token: self.a1z26_sum(token) for token in tokens}
    
    def pythagorean(self, text: str) -> Dict[str, Any]:
        """Pythagorean gematria with theosophical reduction."""
        return self.numerology.calculate_gematria(text, method="pythagorean")
    
    def full_gematria(self, text: str) -> Dict[str, Any]:
        """Both A1Z26 and Pythagorean systems."""
        return self.numerology.calculate_gematria(text, method="both")
    
    def sacred_geometry(self, value: int) -> Dict[str, float]:
        """Get phi-based coordinates for a numeric value."""
        return self.numerology.get_sacred_geometry_coords(value)
    
    def number_meaning(self, value: int) -> Dict[str, Any]:
        """Get symbolic meaning of a number."""
        return self.numerology.get_number_meaning(value)
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Full gematria analysis with all methods.
        
        Returns all computed signatures with mandatory disclaimer.
        """
        normalized = normalize_text(text)
        gematria = self.numerology.calculate_gematria(text, method="both")
        reduced = gematria.get("reduced", 4)
        
        return {
            "text": text,
            "normalized": normalized,
            # Simple methods
            "a1z26_sum": self.a1z26_sum(text),
            "ascii_sum": self.ascii_sum(text),
            "token_sums": self.token_sums(text),
            # Dual gematria systems
            "gematria": gematria,
            # Sacred geometry
            "sacred_geometry": self.sacred_geometry(reduced),
            # Symbolic meaning
            "meaning": self.number_meaning(reduced),
            # Mandatory flags
            "is_interpretive": True,
            "disclaimer": self.DISCLAIMER
        }


# ═══════════════════════════════════════════════════════════════════════════════
# HARMONIC SYNCHRONIZER (CREATIVE LAYER)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class GoldNodeCandidateDTO:
    """A node identified as potentially significant by harmonic patterns."""
    node_id: str
    score: float
    reasons: List[str] = field(default_factory=list)
    artifacts: Dict[str, Any] = field(default_factory=dict)


class HarmonicSynchronizer:
    """
    Scans nodes for "gold nodes" where multiple dimensions align.
    
    ⚠️ IMPORTANT:
    - This is NOT a scientific detector.
    - Treat outputs as CREATIVE PROMPTS / documentary storytelling hooks.
    - Must be gated behind human review and clearly labeled as INTERPRETIVE.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.gematria = GematriaService()
    
    async def scan(self, limit: int = 50) -> List[GoldNodeCandidateDTO]:
        """
        Find nodes with multi-dimensional alignment.
        
        Scoring heuristic:
        - Presence of conceptual drift data (+0.2)
        - Presence of technical_specs (+0.2)
        - Presence of multiple sources (+0.1 per source, max 0.3)
        - Presence of numeric signature patterns (+0.1)
        """
        candidates = []
        
        # Query nodes with concept data
        result = await self.session.execute(
            select(ATOMNode)
            .options(
                selectinload(ATOMNode.conceptual_drift),
                selectinload(ATOMNode.harmonic_signature),
            )
            .limit(limit)
        )
        nodes = result.scalars().all()
        
        for node in nodes:
            score = 0.0
            reasons = []
            artifacts = {}
            
            # Check conceptual drift
            if node.conceptual_drift and node.conceptual_drift.conceptual_drift:
                score += 0.2
                reasons.append("Has conceptual drift data")
                artifacts["conceptual_drift"] = True
            
            # Check technical specs
            if node.technical_specs:
                score += 0.2
                reasons.append("Has technical specifications")
                artifacts["technical_specs"] = True
            
            # Check harmonic signature
            if node.harmonic_signature and node.harmonic_signature.numeric_signatures:
                score += 0.1
                reasons.append("Has numeric signatures")
                artifacts["numeric_signatures"] = node.harmonic_signature.numeric_signatures
            
            # Compute gematria for node name
            gematria_result = self.gematria.analyze(node.name)
            artifacts["gematria"] = gematria_result
            
            # Bonus for "interesting" numeric patterns
            a1z26 = gematria_result["a1z26_sum"]
            if a1z26 % 9 == 0:  # Divisible by 9
                score += 0.05
                reasons.append(f"Name sum divisible by 9: {a1z26}")
            
            if score >= 0.3:
                candidates.append(GoldNodeCandidateDTO(
                    node_id=str(node.id),
                    score=min(score, 1.0),
                    reasons=reasons,
                    artifacts=artifacts
                ))
        
        # Sort by score
        candidates.sort(key=lambda x: x.score, reverse=True)
        
        return candidates


# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL SYNAPSE (Orchestration Layer)
# ═══════════════════════════════════════════════════════════════════════════════

class GlobalSynapse:
    """
    The 'glue' service that ties together:
    - Core nodes + causal links
    - Sensory + psycho-emotional + resources + concepts + logistics
    - Encyclopedia outputs for film/book/game pipelines
    
    This layer is ORCHESTRATION ONLY: no heavy domain claims without evidence.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.causal = CausalNexusService(session)
        self.resonance = ResonanceEngine(session)
        self.gematria = GematriaService()
        self.harmonic = HarmonicSynchronizer(session)
    
    async def build_unified_suggestions(self, node_id: UUID) -> Dict[str, Any]:
        """
        One call to get all candidates for review.
        
        Returns suggestions from causal nexus and resonance engine,
        with evidence gating applied.
        """
        link_candidates = await self.causal.suggest_links(node_id)
        resonance_candidates = await self.resonance.suggest(node_id)
        
        # Gate evidence for link candidates
        gated = []
        for c in link_candidates:
            ok, reason = self.causal.validate_link_evidence(c)
            gated.append({
                "candidate": {
                    "trigger_id": c.trigger_id,
                    "result_id": c.result_id,
                    "link_type": c.link_type,
                    "strength": c.strength,
                    "confidence": c.confidence,
                    "rationale": c.rationale,
                    "provenance": c.provenance
                },
                "ok": ok,
                "gate_reason": reason
            })
        
        return {
            "node_id": str(node_id),
            "causal_links": gated,
            "resonance": [
                {
                    "node_id": r.node_id,
                    "module": r.module,
                    "payload": r.payload,
                    "confidence": r.confidence,
                    "rationale": r.rationale
                }
                for r in resonance_candidates
            ],
            "guardrails": self.publish_guardrails()
        }
    
    def publish_guardrails(self) -> Dict[str, Any]:
        """Static guardrails for UI & agents."""
        return {
            "no_absolute_truth_claims": True,
            "require_sources_for_high_confidence": True,
            "store_uncertainty_explicitly": True,
            "human_in_the_loop": True,
            "psycho_requires_counter_signals": True,
            "harmonic_is_interpretive_only": True
        }
    
    async def get_full_node(self, node_id: UUID) -> Optional[Dict[str, Any]]:
        """Get a node with all its dimension profiles."""
        result = await self.session.execute(
            select(ATOMNode)
            .options(
                selectinload(ATOMNode.sensory_profile),
                selectinload(ATOMNode.psycho_profile),
                selectinload(ATOMNode.resource_footprint),
                selectinload(ATOMNode.conceptual_drift),
                selectinload(ATOMNode.logistics_network),
                selectinload(ATOMNode.harmonic_signature),
                selectinload(ATOMNode.encyclopedia_entries),
            )
            .where(ATOMNode.id == node_id)
        )
        node = result.scalar_one_or_none()
        
        if not node:
            return None
        
        return {
            "id": str(node.id),
            "name": node.name,
            "dimension": node.dimension,
            "epoch": node.epoch,
            "date_range": node.date_range,
            "location": node.location,
            "description": node.description,
            "technical_specs": node.technical_specs,
            "biological_impact": node.biological_impact,
            "social_customs": node.social_customs,
            "planetary_context": node.planetary_context,
            "psychology": node.psychology,
            "validation_status": node.validation_status,
            "created_at": node.created_at.isoformat() if node.created_at else None,
            "profiles": {
                "sensory": node.sensory_profile.__dict__ if node.sensory_profile else None,
                "psychology": node.psycho_profile.__dict__ if node.psycho_profile else None,
                "resources": node.resource_footprint.__dict__ if node.resource_footprint else None,
                "concepts": node.conceptual_drift.__dict__ if node.conceptual_drift else None,
                "logistics": node.logistics_network.__dict__ if node.logistics_network else None,
                "harmonics": node.harmonic_signature.__dict__ if node.harmonic_signature else None,
            },
            "encyclopedia_entries": [
                {"id": str(e.id), "title": e.title, "review_status": e.review_status}
                for e in node.encyclopedia_entries
            ]
        }


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = [
    # DTOs
    "CausalLinkCandidateDTO",
    "ResonanceSuggestionDTO",
    "GoldNodeCandidateDTO",
    # Services
    "CausalNexusService",
    "ResonanceEngine",
    "NumerologyEngine",
    "GematriaService",
    "HarmonicSynchronizer",
    "GlobalSynapse",
    # Utilities
    "normalize_text",
    "A1Z26",
    "PYTHAGOREAN",
    "PHI",
    "MASTER_NUMBERS",
]
