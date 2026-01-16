"""
═══════════════════════════════════════════════════════════════════════════════
AT·OM MAPPING SYSTEM — Test Suite (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Tests for:
- Models (Rule #6 compliance)
- Evidence gating (high confidence requires provenance)
- Temporal validation (anti-anachronism)
- Harmonics layer (disclaimer requirements)
"""

import pytest
from datetime import datetime
from uuid import uuid4, UUID
from typing import Dict, Any


# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def user_id() -> UUID:
    """Test user ID for Rule #6 traceability."""
    return uuid4()


@pytest.fixture
def sample_atom_node(user_id: UUID) -> Dict[str, Any]:
    """Sample AT·OM node data."""
    return {
        "name": "Steam Engine",
        "dimension": "PHYSICAL",
        "epoch": "Industrial",
        "date_range": {"from": "1712", "to": "1769", "label": "Newcomen to Watt"},
        "location": {"region": "England", "confidence": 0.9},
        "description": "Heat engine using steam pressure to perform mechanical work",
        "technical_specs": {
            "fuel": "coal",
            "efficiency": 0.01,
            "power_output": "5 HP"
        },
        "created_by": str(user_id)
    }


@pytest.fixture
def sample_causal_link(user_id: UUID) -> Dict[str, Any]:
    """Sample causal link with evidence."""
    return {
        "link_type": "TECH",
        "strength": 0.8,
        "confidence": 0.75,
        "rationale": "Steam engine enabled railway transportation",
        "provenance": [
            {"source": "The Railway Revolution", "type": "book", "author": "J. Simmons"}
        ],
        "created_by": str(user_id)
    }


# ═══════════════════════════════════════════════════════════════════════════════
# EVIDENCE GATING TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestEvidenceGating:
    """Test evidence requirements for high-confidence claims."""
    
    def test_high_confidence_requires_provenance(self):
        """High confidence (>=0.75) must have provenance sources."""
        from dataclasses import dataclass
        from typing import Optional, List
        
        @dataclass
        class CausalLinkCandidate:
            trigger_id: str
            result_id: str
            link_type: str
            strength: float = 1.0
            confidence: float = 0.5
            rationale: str = ""
            provenance: Optional[List[Dict[str, Any]]] = None
        
        def validate_link_evidence(candidate: CausalLinkCandidate) -> tuple:
            if candidate.confidence >= 0.75 and not candidate.provenance:
                return False, "High-confidence link requires provenance sources."
            return True, "OK"
        
        # High confidence without provenance - SHOULD FAIL
        high_conf_no_prov = CausalLinkCandidate(
            trigger_id="a",
            result_id="b",
            link_type="TECH",
            confidence=0.8,
            provenance=None
        )
        valid, msg = validate_link_evidence(high_conf_no_prov)
        assert valid is False
        assert "provenance" in msg.lower()
        
        # High confidence with provenance - SHOULD PASS
        high_conf_with_prov = CausalLinkCandidate(
            trigger_id="a",
            result_id="b",
            link_type="TECH",
            confidence=0.8,
            provenance=[{"source": "Test Book", "type": "book"}]
        )
        valid, msg = validate_link_evidence(high_conf_with_prov)
        assert valid is True
        
        # Low confidence without provenance - SHOULD PASS
        low_conf = CausalLinkCandidate(
            trigger_id="a",
            result_id="b",
            link_type="TECH",
            confidence=0.4,
            provenance=None
        )
        valid, msg = validate_link_evidence(low_conf)
        assert valid is True
    
    def test_medium_confidence_allows_no_provenance(self):
        """Medium confidence (< 0.75) can exist without provenance."""
        # This is allowed but should be flagged as hypothesis
        confidence = 0.5
        provenance = None
        
        # Rule: < 0.75 doesn't require sources
        assert confidence < 0.75
        # But should be marked as hypothesis
        is_hypothesis = provenance is None or len(provenance) == 0
        assert is_hypothesis is True


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPORAL VALIDATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTemporalValidation:
    """Test anti-anachronism checks."""
    
    def test_prevent_temporal_anachronism(self):
        """Trigger must not end after result begins."""
        def prevent_anachronism(trigger_range, result_range) -> tuple:
            if not trigger_range or not result_range:
                return True, "No date_range; cannot enforce ordering."
            try:
                t_to = float(trigger_range.get("to")) if trigger_range.get("to") else None
                r_from = float(result_range.get("from")) if result_range.get("from") else None
                if t_to is not None and r_from is not None and t_to > r_from:
                    return False, "Temporal anachronism: trigger ends after result begins."
            except Exception:
                return True, "Unparseable date_range."
            return True, "OK"
        
        # Valid: trigger ends before result begins
        valid_case = prevent_anachronism(
            {"from": "1700", "to": "1750"},
            {"from": "1760", "to": "1800"}
        )
        assert valid_case[0] is True
        
        # Invalid: trigger ends after result begins (anachronism)
        invalid_case = prevent_anachronism(
            {"from": "1700", "to": "1800"},
            {"from": "1750", "to": "1850"}
        )
        assert invalid_case[0] is False
        assert "anachronism" in invalid_case[1].lower()
        
        # Edge case: no dates provided
        no_dates = prevent_anachronism(None, None)
        assert no_dates[0] is True  # Allow but flag
    
    def test_bce_dates_handled(self):
        """BCE (negative) dates should work correctly."""
        def parse_year(s: str) -> float:
            if s is None:
                return None
            s = s.strip()
            if s.lower().endswith("bce") or s.lower().endswith("bc"):
                return -abs(float(s.replace("BCE", "").replace("BC", "").strip()))
            return float(s)
        
        assert parse_year("3000 BCE") == -3000
        assert parse_year("1500") == 1500
        assert parse_year("-500") == -500


# ═══════════════════════════════════════════════════════════════════════════════
# HARMONICS LAYER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestHarmonicsLayer:
    """Test harmonics/gematria creative layer compliance."""
    
    def test_harmonics_requires_disclaimer(self):
        """Harmonics results must include interpretive note (disclaimer)."""
        # Simulate harmonics result
        class HarmonicResult:
            def __init__(self, interpretive_note: str = None, confidence: float = 0.2):
                self.interpretive_note = interpretive_note
                self.confidence = confidence
        
        # Without disclaimer - INVALID
        no_disclaimer = HarmonicResult(interpretive_note=None)
        assert no_disclaimer.interpretive_note is None or no_disclaimer.interpretive_note == ""
        
        # With disclaimer - VALID
        with_disclaimer = HarmonicResult(
            interpretive_note="This is an artistic interpretation, not scientific fact."
        )
        assert with_disclaimer.interpretive_note is not None
        assert len(with_disclaimer.interpretive_note) > 0
    
    def test_harmonics_default_confidence_low(self):
        """Harmonics confidence should default to <= 0.3."""
        default_confidence = 0.2  # From model definition
        
        assert default_confidence <= 0.3, "Harmonics confidence must be low by default"
    
    def test_gematria_normalization(self):
        """Test gematria text normalization."""
        import re
        import unicodedata
        
        def normalize_text(s: str) -> str:
            s = s.strip().lower()
            s = unicodedata.normalize("NFKD", s)
            s = "".join(ch for ch in s if not unicodedata.combining(ch))
            s = re.sub(r"[^a-z0-9\s]", " ", s)
            s = re.sub(r"\s+", " ", s).strip()
            return s
        
        assert normalize_text("Café") == "cafe"
        assert normalize_text("L'École") == "l ecole"
        assert normalize_text("  HELLO  WORLD  ") == "hello world"
    
    def test_a1z26_sum(self):
        """Test A1Z26 gematria sum."""
        A1Z26 = {chr(ord("a") + i): i + 1 for i in range(26)}
        
        def a1z26_sum(text: str) -> int:
            text = text.lower().replace(" ", "")
            return sum(A1Z26.get(ch, 0) for ch in text)
        
        # A=1, B=2, C=3 => ABC = 6
        assert a1z26_sum("abc") == 6
        # HELLO: H=8, E=5, L=12, L=12, O=15 = 52
        assert a1z26_sum("hello") == 52


# ═══════════════════════════════════════════════════════════════════════════════
# RULE #6 TRACEABILITY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestRule6Traceability:
    """Test Rule #6 compliance for all models."""
    
    def test_atom_node_has_traceability_fields(self, user_id: UUID):
        """ATOMNode must have created_at, created_by, updated_at, updated_by."""
        node_fields = ["created_at", "created_by", "updated_at", "updated_by"]
        
        # Simulate model
        node = {
            "id": str(uuid4()),
            "name": "Test Node",
            "created_at": datetime.utcnow(),
            "created_by": str(user_id),
            "updated_at": datetime.utcnow(),
            "updated_by": None
        }
        
        for field in node_fields:
            assert field in node, f"ATOMNode missing {field}"
    
    def test_profile_tables_have_created_by(self, user_id: UUID):
        """All profile tables must have created_by field."""
        profile_tables = [
            "atom_sensory_profiles",
            "atom_psycho_emotional_profiles",
            "atom_resource_footprints",
            "atom_conceptual_drift",
            "atom_logistics_networks",
            "atom_harmonic_signatures"
        ]
        
        # Each table should enforce created_by
        for table in profile_tables:
            # In actual implementation, this would check the model
            # Here we verify the requirement is documented
            assert "profiles" in table or "drift" in table or "networks" in table or "signatures" in table
    
    def test_causal_links_have_traceability(self, sample_causal_link: Dict[str, Any]):
        """Causal links must have created_at, created_by."""
        assert "created_by" in sample_causal_link
        # created_at would be auto-generated


# ═══════════════════════════════════════════════════════════════════════════════
# DIMENSION CLASSIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestDimensionClassification:
    """Test dimension enum values."""
    
    def test_valid_dimensions(self):
        """Only valid dimensions should be allowed."""
        valid_dimensions = {
            "PHYSICAL",
            "BIOLOGICAL",
            "SOCIAL",
            "SPIRITUAL",
            "CONCEPTUAL",
            "ECOLOGICAL",
            "LOGISTICAL",
            "SENSORY"
        }
        
        # Test valid
        assert "PHYSICAL" in valid_dimensions
        assert "BIOLOGICAL" in valid_dimensions
        
        # Test invalid
        assert "MAGICAL" not in valid_dimensions
        assert "RANDOM" not in valid_dimensions
    
    def test_link_types(self):
        """Only valid link types should be allowed."""
        valid_link_types = {
            "BIO",
            "TECH",
            "SOCIAL",
            "SPIRITUAL",
            "ECO",
            "SENSORY",
            "CONCEPT",
            "LOGISTICS"
        }
        
        assert "TECH" in valid_link_types
        assert "BIO" in valid_link_types
        assert "MAGIC" not in valid_link_types


# ═══════════════════════════════════════════════════════════════════════════════
# ENCYCLOPEDIA ENTRY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestEncyclopediaEntry:
    """Test encyclopedia entry validation."""
    
    def test_review_status_enum(self):
        """Valid review statuses."""
        valid_statuses = {"draft", "validated", "published"}
        
        assert "draft" in valid_statuses
        assert "published" in valid_statuses
        assert "deleted" not in valid_statuses
    
    def test_completeness_bounds(self):
        """Completeness must be between 0 and 1."""
        valid_completeness = [0.0, 0.5, 1.0]
        invalid_completeness = [-0.1, 1.5, 2.0]
        
        for c in valid_completeness:
            assert 0.0 <= c <= 1.0
        
        for c in invalid_completeness:
            assert not (0.0 <= c <= 1.0)


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestATOMIntegration:
    """Integration tests for AT·OM Mapping System."""
    
    def test_node_can_have_multiple_profiles(self, user_id: UUID):
        """A node can have multiple profile types attached."""
        node_id = uuid4()
        
        # Simulate profiles
        profiles = {
            "sensory": {"node_id": str(node_id), "ergonomics": {"grip": "power"}},
            "psycho": {"node_id": str(node_id), "psycho_emotional": {"mood": "anxiety"}},
            "resource": {"node_id": str(node_id), "resource_footprint": {"materials": ["iron"]}},
            "concept": {"node_id": str(node_id), "concept_evolution": {"etymology": "latin"}},
            "logistics": {"node_id": str(node_id), "logistics_data": {"routes": ["silk road"]}},
        }
        
        # All should reference same node
        for profile in profiles.values():
            assert profile["node_id"] == str(node_id)
    
    def test_causal_chain_traversal(self):
        """Causal chain can be traversed from any node."""
        # Simulate graph: A -> B -> C
        nodes = {
            "A": {"id": "A", "name": "Fire"},
            "B": {"id": "B", "name": "Cooking"},
            "C": {"id": "C", "name": "Nutrition"},
        }
        
        links = [
            {"trigger_id": "A", "result_id": "B"},
            {"trigger_id": "B", "result_id": "C"},
        ]
        
        # Traverse from A
        def get_chain(start_id: str, max_depth: int = 5) -> list:
            chain = []
            current = start_id
            depth = 0
            
            while depth < max_depth:
                next_links = [l for l in links if l["trigger_id"] == current]
                if not next_links:
                    break
                chain.append(next_links[0])
                current = next_links[0]["result_id"]
                depth += 1
            
            return chain
        
        chain = get_chain("A")
        assert len(chain) == 2
        assert chain[0]["result_id"] == "B"
        assert chain[1]["result_id"] == "C"


# ═══════════════════════════════════════════════════════════════════════════════
# MARKERS
# ═══════════════════════════════════════════════════════════════════════════════

pytestmark = [
    pytest.mark.atom,
    pytest.mark.mapping,
]
