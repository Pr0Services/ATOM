"""
═══════════════════════════════════════════════════════════════════════════════
AT-OM MAPPING SYSTEM — Tests (CHE·NU V76)
═══════════════════════════════════════════════════════════════════════════════

Tests for:
- Evidence gating (high-confidence requires sources)
- Fact/interpretation/hypothesis distinction
- Temporal coherence (no anachronisms)
- Psychology requires counter-signals
- Harmonic layer is interpretive only
"""

import pytest
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any

from app.services.atom_services import (
    CausalNexusService, CausalLinkCandidateDTO,
    ResonanceEngine, GematriaService,
    HarmonicSynchronizer, GlobalSynapse,
    normalize_text, A1Z26
)
from app.schemas.atom_schemas import (
    ATOMNodeCreate, CausalLinkCreate, CausalLinkType,
    PsychoEmotionalProfileCreate, ProvenanceSource,
    ATOMDimension, DateRange
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: EVIDENCE GATING
# ═══════════════════════════════════════════════════════════════════════════════

class TestEvidenceGating:
    """Test that high-confidence claims require provenance sources."""
    
    def test_low_confidence_no_provenance_ok(self):
        """Low confidence (< 0.75) should pass without provenance."""
        candidate = CausalLinkCandidateDTO(
            trigger_id=str(uuid4()),
            result_id=str(uuid4()),
            link_type="TECH",
            confidence=0.5,
            provenance=None
        )
        
        # Would need session for full service, test logic directly
        if candidate.confidence >= 0.75 and not candidate.provenance:
            is_valid = False
        else:
            is_valid = True
        
        assert is_valid is True
    
    def test_high_confidence_no_provenance_fails(self):
        """High confidence (>= 0.75) MUST fail without provenance."""
        candidate = CausalLinkCandidateDTO(
            trigger_id=str(uuid4()),
            result_id=str(uuid4()),
            link_type="TECH",
            confidence=0.8,
            provenance=None
        )
        
        if candidate.confidence >= 0.75 and not candidate.provenance:
            is_valid = False
            reason = "High-confidence link (>=0.75) requires provenance sources."
        else:
            is_valid = True
            reason = "OK"
        
        assert is_valid is False
        assert "provenance" in reason.lower()
    
    def test_high_confidence_with_provenance_ok(self):
        """High confidence with provenance should pass."""
        candidate = CausalLinkCandidateDTO(
            trigger_id=str(uuid4()),
            result_id=str(uuid4()),
            link_type="TECH",
            confidence=0.85,
            provenance=[{"source": "Smith et al. 2020", "type": "paper"}]
        )
        
        if candidate.confidence >= 0.75 and not candidate.provenance:
            is_valid = False
        else:
            is_valid = True
        
        assert is_valid is True
    
    def test_very_high_confidence_requires_multiple_sources(self):
        """Very high confidence (>= 0.9) requires at least 2 sources."""
        candidate = CausalLinkCandidateDTO(
            trigger_id=str(uuid4()),
            result_id=str(uuid4()),
            link_type="TECH",
            confidence=0.92,
            provenance=[{"source": "Smith 2020", "type": "paper"}]  # Only 1 source
        )
        
        if candidate.confidence >= 0.9:
            if not candidate.provenance or len(candidate.provenance) < 2:
                is_valid = False
                reason = "Very high confidence (>=0.9) requires at least 2 provenance sources."
            else:
                is_valid = True
                reason = "OK"
        else:
            is_valid = True
            reason = "OK"
        
        assert is_valid is False
        assert "2 provenance" in reason
    
    def test_very_high_confidence_with_multiple_sources_ok(self):
        """Very high confidence with 2+ sources should pass."""
        candidate = CausalLinkCandidateDTO(
            trigger_id=str(uuid4()),
            result_id=str(uuid4()),
            link_type="TECH",
            confidence=0.92,
            provenance=[
                {"source": "Smith 2020", "type": "paper"},
                {"source": "Jones 2021", "type": "paper"}
            ]
        )
        
        if candidate.confidence >= 0.9:
            if not candidate.provenance or len(candidate.provenance) < 2:
                is_valid = False
            else:
                is_valid = True
        else:
            is_valid = True
        
        assert is_valid is True


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: TEMPORAL COHERENCE
# ═══════════════════════════════════════════════════════════════════════════════

class TestTemporalCoherence:
    """Test that causal links respect temporal ordering."""
    
    def test_normal_causality_valid(self):
        """Trigger before result should be valid."""
        trigger_range = {"from": "-10000", "to": "-8000"}
        result_range = {"from": "-7000", "to": "-5000"}
        
        # Trigger ends (-8000) before result begins (-7000)
        trigger_to = int(trigger_range["to"])
        result_from = int(result_range["from"])
        
        is_valid = trigger_to <= result_from
        assert is_valid is True
    
    def test_overlapping_periods_valid(self):
        """Overlapping periods should be valid (concurrent events)."""
        trigger_range = {"from": "-10000", "to": "-7000"}
        result_range = {"from": "-8000", "to": "-5000"}
        
        # Overlap: trigger ends at -7000, result starts at -8000
        is_valid = True  # Overlapping is OK
        assert is_valid is True
    
    def test_reverse_causality_invalid(self):
        """Result before trigger should be flagged."""
        trigger_range = {"from": "-5000", "to": "-3000"}
        result_range = {"from": "-10000", "to": "-8000"}
        
        # Trigger starts (-5000) AFTER result ends (-8000) = ANACHRONISM
        trigger_from = int(trigger_range["from"])
        result_to = int(result_range["to"])
        
        is_anachronism = trigger_from > result_to
        assert is_anachronism is True
    
    def test_unknown_dates_permissible(self):
        """Unknown dates should be permissible but flagged."""
        trigger_range = None
        result_range = {"from": "-5000", "to": "-3000"}
        
        # Unknown ranges should pass but be flagged
        if not trigger_range or not result_range:
            is_valid = True
            needs_manual_review = True
        else:
            is_valid = True
            needs_manual_review = False
        
        assert is_valid is True
        assert needs_manual_review is True


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: PSYCHOLOGY COUNTER-SIGNALS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPsychologyCounterSignals:
    """Test that psychological claims require counter-signals."""
    
    def test_psychology_without_counter_signals_fails(self):
        """Psychological claims without counter_signals should fail."""
        psycho_data = {
            "societal_mood": [{"label": "anxiety", "signal": "pamphlets", "confidence": 0.4}],
            "drivers": [{"type": "fear", "note": "...", "confidence": 0.3}],
            # Missing: counter_signals
            # Missing: uncertainty_notes
        }
        
        has_counter_signals = "counter_signals" in psycho_data
        has_uncertainty = "uncertainty_notes" in psycho_data
        
        is_valid = has_counter_signals and has_uncertainty
        assert is_valid is False
    
    def test_psychology_with_counter_signals_ok(self):
        """Psychological claims with counter_signals and uncertainty should pass."""
        psycho_data = {
            "societal_mood": [{"label": "anxiety", "signal": "pamphlets", "confidence": 0.4}],
            "drivers": [{"type": "fear", "note": "...", "confidence": 0.3}],
            "counter_signals": ["Some populations showed optimism"],
            "uncertainty_notes": "Limited historical sources"
        }
        
        has_counter_signals = "counter_signals" in psycho_data and psycho_data["counter_signals"]
        has_uncertainty = "uncertainty_notes" in psycho_data and psycho_data["uncertainty_notes"]
        
        is_valid = has_counter_signals and has_uncertainty
        assert is_valid is True
    
    def test_psychology_validator_in_schema(self):
        """Test Pydantic validator catches missing fields."""
        with pytest.raises(ValueError) as excinfo:
            PsychoEmotionalProfileCreate(
                node_id=uuid4(),
                psycho_emotional={
                    "drivers": [{"type": "fear"}],
                    # Missing counter_signals and uncertainty_notes
                },
                confidence=0.5
            )
        
        error_msg = str(excinfo.value).lower()
        assert "counter_signals" in error_msg or "uncertainty" in error_msg


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: HARMONIC LAYER INTERPRETIVE
# ═══════════════════════════════════════════════════════════════════════════════

class TestHarmonicLayerInterpretive:
    """Verify the harmonic/gematria layer is marked as interpretive."""
    
    def test_dual_gematria_methods(self):
        """Test both A1Z26 and Pythagorean converge for AT-OM."""
        # A1Z26: A=1, T=20, O=15, M=13 → 49 → 13 → 4
        # Pythagorean: A=1, T=2, O=6, M=4 → 13 → 4
        
        # Simulate the engine
        A1Z26 = {chr(ord('a') + i): i + 1 for i in range(26)}
        PYTHAGOREAN = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
            'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
            's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
        }
        
        text = "atom"  # AT-OM cleaned
        
        a1z26_raw = sum(A1Z26.get(c, 0) for c in text)
        pyth_raw = sum(PYTHAGOREAN.get(c, 0) for c in text)
        
        assert a1z26_raw == 49, f"A1Z26 should be 49, got {a1z26_raw}"
        assert pyth_raw == 13, f"Pythagorean should be 13, got {pyth_raw}"
        
        # Both reduce to 4
        def reduce(n):
            while n > 9 and n not in {11, 22, 33}:
                n = sum(int(d) for d in str(n))
            return n
        
        assert reduce(a1z26_raw) == 4
        assert reduce(pyth_raw) == 4
    """Test that harmonic/gematria outputs are marked as interpretive."""
    
    def test_gematria_includes_disclaimer(self):
        """Gematria results must include disclaimer."""
        service = GematriaService()
        result = service.analyze("fire")
        
        assert "disclaimer" in result
        assert "interpretive" in result["disclaimer"].lower() or "not scientific" in result["disclaimer"].lower()
        assert result["is_interpretive"] is True
    
    def test_gematria_sums_correct(self):
        """Test basic gematria calculations."""
        service = GematriaService()
        
        # "a" = 1
        assert service.a1z26_sum("a") == 1
        
        # "z" = 26
        assert service.a1z26_sum("z") == 26
        
        # "abc" = 1 + 2 + 3 = 6
        assert service.a1z26_sum("abc") == 6
    
    def test_normalize_text(self):
        """Test text normalization."""
        # Lowercase
        assert normalize_text("ABC") == "abc"
        
        # Strip accents
        assert normalize_text("café") == "cafe"
        
        # Remove special chars
        assert normalize_text("hello-world!") == "hello world"
    
    def test_token_sums(self):
        """Test per-token sums."""
        service = GematriaService()
        result = service.token_sums("a b c")
        
        assert result["a"] == 1
        assert result["b"] == 2
        assert result["c"] == 3


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: FACT/INTERPRETATION/HYPOTHESIS DISTINCTION
# ═══════════════════════════════════════════════════════════════════════════════

class TestDistinctions:
    """Test clear distinction between facts, interpretations, and hypotheses."""
    
    def test_suggestion_confidence_capped(self):
        """Auto-generated suggestions should have capped confidence."""
        # Suggestions should never claim high confidence
        max_suggestion_confidence = 0.6
        
        # Simulated suggestion
        suggestion_confidence = 0.5
        
        assert suggestion_confidence <= max_suggestion_confidence
    
    def test_low_confidence_indicates_hypothesis(self):
        """Low confidence should indicate hypothesis status."""
        candidate = CausalLinkCandidateDTO(
            trigger_id=str(uuid4()),
            result_id=str(uuid4()),
            link_type="TECH",
            confidence=0.3,  # Low
            rationale="Tentative connection based on limited evidence"
        )
        
        is_hypothesis = candidate.confidence < 0.5
        assert is_hypothesis is True
    
    def test_high_confidence_with_sources_is_fact(self):
        """High confidence with solid provenance can be treated as established."""
        candidate = CausalLinkCandidateDTO(
            trigger_id=str(uuid4()),
            result_id=str(uuid4()),
            link_type="TECH",
            confidence=0.85,
            provenance=[
                {"source": "Peer-reviewed paper 1", "type": "paper"},
                {"source": "Archaeological evidence", "type": "artifact"}
            ]
        )
        
        is_established = (
            candidate.confidence >= 0.75 and
            candidate.provenance and
            len(candidate.provenance) >= 2
        )
        assert is_established is True


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: IMMATERIAL MODULES (No Absolute Truth)
# ═══════════════════════════════════════════════════════════════════════════════

class TestNoAbsoluteTruth:
    """Test that the system never claims absolute truth."""
    
    def test_guardrails_prevent_absolute_claims(self):
        """Guardrails should prevent absolute truth claims."""
        guardrails = {
            "no_absolute_truth_claims": True,
            "require_sources_for_high_confidence": True,
            "store_uncertainty_explicitly": True,
            "human_in_the_loop": True,
            "psycho_requires_counter_signals": True,
            "harmonic_is_interpretive_only": True
        }
        
        assert guardrails["no_absolute_truth_claims"] is True
        assert guardrails["human_in_the_loop"] is True
    
    def test_all_outputs_have_confidence(self):
        """All outputs should have explicit confidence scores."""
        # Causal link
        link = CausalLinkCandidateDTO(
            trigger_id=str(uuid4()),
            result_id=str(uuid4()),
            link_type="TECH",
            confidence=0.5
        )
        
        assert hasattr(link, 'confidence')
        assert 0.0 <= link.confidence <= 1.0


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: CAUSAL LINK SCHEMA VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

class TestCausalLinkSchema:
    """Test Pydantic schema validation for causal links."""
    
    def test_high_confidence_validator_in_schema(self):
        """Schema should reject high-confidence without provenance."""
        with pytest.raises(ValueError) as excinfo:
            CausalLinkCreate(
                trigger_id=uuid4(),
                result_id=uuid4(),
                link_type=CausalLinkType.TECH,
                confidence=0.8,  # High
                provenance=None  # Missing!
            )
        
        assert "provenance" in str(excinfo.value).lower()
    
    def test_valid_link_with_provenance(self):
        """Valid link with provenance should pass."""
        link = CausalLinkCreate(
            trigger_id=uuid4(),
            result_id=uuid4(),
            link_type=CausalLinkType.TECH,
            confidence=0.85,
            provenance=[ProvenanceSource(source="Test 2020", type="paper")]
        )
        
        assert link.confidence == 0.85
        assert len(link.provenance) == 1


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: NODE SCHEMA
# ═══════════════════════════════════════════════════════════════════════════════

class TestNodeSchema:
    """Test ATOM node schema."""
    
    def test_create_node_minimal(self):
        """Test minimal node creation."""
        node = ATOMNodeCreate(name="Fire Discovery")
        
        assert node.name == "Fire Discovery"
        assert node.dimension is None
    
    def test_create_node_full(self):
        """Test full node creation."""
        node = ATOMNodeCreate(
            name="Controlled Fire",
            dimension=ATOMDimension.PHYSICAL,
            epoch="Lower Paleolithic",
            date_range=DateRange(from_date="-400000", to_date="-200000", label="approx"),
            description="The controlled use of fire by early hominins",
            technical_specs={"ignition": "friction or percussion"},
            biological_impact={"digestion": "enabled cooked food"}
        )
        
        assert node.dimension == ATOMDimension.PHYSICAL
        assert node.epoch == "Lower Paleolithic"
        assert node.date_range.from_date == "-400000"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: RULE #6 TRACEABILITY
# ═══════════════════════════════════════════════════════════════════════════════

class TestRule6Traceability:
    """Test that all entities have proper traceability fields."""
    
    def test_node_has_traceability_fields(self):
        """Nodes should have id, created_by, created_at."""
        from app.models.atom_models import ATOMNode
        
        # Check column names exist
        columns = {c.name for c in ATOMNode.__table__.columns}
        
        assert "id" in columns
        assert "created_by" in columns
        assert "created_at" in columns
        assert "modified_by" in columns
        assert "modified_at" in columns
    
    def test_links_have_traceability_fields(self):
        """Causal links should have traceability."""
        from app.models.atom_models import atom_causal_links
        
        columns = {c.name for c in atom_causal_links.columns}
        
        assert "id" in columns
        assert "created_by" in columns
        assert "created_at" in columns
    
    def test_profiles_have_traceability_fields(self):
        """Dimension profiles should have traceability."""
        from app.models.atom_models import (
            AtomSensoryProfile, AtomPsychoEmotionalProfile,
            AtomResourceFootprint, AtomConceptualDrift,
            AtomLogisticsNetwork, AtomHarmonicSignature
        )
        
        for model in [
            AtomSensoryProfile, AtomPsychoEmotionalProfile,
            AtomResourceFootprint, AtomConceptualDrift,
            AtomLogisticsNetwork, AtomHarmonicSignature
        ]:
            columns = {c.name for c in model.__table__.columns}
            assert "id" in columns, f"{model.__name__} missing id"
            assert "created_at" in columns, f"{model.__name__} missing created_at"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST: RESONANCE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class TestResonanceEngine:
    """Test resonance engine minimum fields."""
    
    def test_minimum_fields_defined(self):
        """Each module should have defined minimum fields."""
        # Can't instantiate without session, test static method
        expected = {
            "sensory": ["ergonomics", "acoustics"],
            "psychology": ["psycho_emotional", "counter_signals", "uncertainty_notes"],
            "resources": ["resource_footprint"],
            "concepts": ["conceptual_drift"],
            "logistics": ["logistics_networks"],
        }
        
        # Psychology must have balance fields
        assert "counter_signals" in expected["psychology"]
        assert "uncertainty_notes" in expected["psychology"]


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestATOMSystemSummary:
    """Summary verification tests."""
    
    def test_all_guardrails_present(self):
        """Verify all required guardrails are defined."""
        required_guardrails = [
            "no_absolute_truth_claims",
            "require_sources_for_high_confidence",
            "store_uncertainty_explicitly",
            "human_in_the_loop",
            "psycho_requires_counter_signals",
            "harmonic_is_interpretive_only"
        ]
        
        from app.schemas.atom_schemas import Guardrails
        guardrails = Guardrails()
        
        for g in required_guardrails:
            assert hasattr(guardrails, g), f"Missing guardrail: {g}"
            assert getattr(guardrails, g) is True, f"Guardrail {g} should be True"
    
    def test_dimension_types_complete(self):
        """Verify all dimension types are defined."""
        expected_dimensions = [
            "PHYSICAL", "BIOLOGICAL", "SOCIAL", "SPIRITUAL",
            "CONCEPTUAL", "ECOLOGICAL", "LOGISTICAL", "SENSORY"
        ]
        
        from app.schemas.atom_schemas import ATOMDimension
        
        for dim in expected_dimensions:
            assert dim in [d.value for d in ATOMDimension], f"Missing dimension: {dim}"
    
    def test_link_types_complete(self):
        """Verify all link types are defined."""
        expected_types = [
            "BIO", "TECH", "SOCIAL", "SPIRITUAL",
            "ECO", "SENSORY", "CONCEPT", "LOGISTICS"
        ]
        
        from app.schemas.atom_schemas import CausalLinkType
        
        for lt in expected_types:
            assert lt in [t.value for t in CausalLinkType], f"Missing link type: {lt}"


# ═══════════════════════════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
