"""
AT-OM Mapping — Causal Nexus Service

Provides:
- candidate link generation (suggestions)
- basic graph integrity checks
- evidence gating helpers (no 'strong' links without provenance)

This service is intentionally conservative: it suggests, but does not assert.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

@dataclass
class CausalLinkCandidate:
    trigger_id: str
    result_id: str
    link_type: str
    strength: float = 1.0
    confidence: float = 0.5
    rationale: str = ""
    provenance: Optional[List[Dict[str, Any]]] = None


class CausalNexusService:
    def __init__(self, session):
        self.session = session

    def suggest_links(self, node_id: str) -> List[CausalLinkCandidate]:
        """Return conservative candidates based on existing module fields.
        Implementation intentionally left project-specific:
        - You may use embeddings, rules, or hybrid retrieval.
        """
        # Placeholder: return empty until wired to your retrieval layer.
        return []

    def validate_link_evidence(self, candidate: CausalLinkCandidate) -> Tuple[bool, str]:
        """Gate strong claims: if confidence is high, require provenance."""
        if candidate.confidence >= 0.75 and not candidate.provenance:
            return False, "High-confidence link requires provenance sources."
        return True, "OK"

    def prevent_temporal_anachronism(self, trigger_range: Optional[Dict[str, str]], result_range: Optional[Dict[str, str]]) -> Tuple[bool, str]:
        """Basic temporal ordering check using date_range {from,to} strings.
        Leaves parsing to caller; treat unknown as permissible but low confidence.
        """
        if not trigger_range or not result_range:
            return True, "No date_range; cannot enforce ordering (set low confidence)."
        try:
            t_to = float(trigger_range.get("to")) if trigger_range.get("to") is not None else None
            r_from = float(result_range.get("from")) if result_range.get("from") is not None else None
            if t_to is not None and r_from is not None and t_to > r_from:
                return False, "Temporal anachronism: trigger ends after result begins."
        except Exception:
            return True, "Unparseable date_range; cannot enforce ordering (set low confidence)."
        return True, "OK"
