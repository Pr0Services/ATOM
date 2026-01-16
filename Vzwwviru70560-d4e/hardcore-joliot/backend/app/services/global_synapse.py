"""
AT-OM Mapping — Global Synapse

The 'glue' service that ties together:
- core nodes + causal links
- sensory + psycho-emotional + resources + concepts + logistics
- encyclopedia outputs for film/book/game pipelines

This layer should remain orchestration-only: no heavy domain claims without evidence.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .causal_nexus import CausalNexusService, CausalLinkCandidate
from .resonance_engine import ResonanceEngine, ResonanceSuggestion


class GlobalSynapse:
    def __init__(self, session):
        self.session = session
        self.causal = CausalNexusService(session)
        self.resonance = ResonanceEngine(session)

    def build_unified_suggestions(self, node_id: str) -> Dict[str, Any]:
        """One call to get all candidates for review."""
        link_candidates = self.causal.suggest_links(node_id)
        resonance_candidates = self.resonance.suggest(node_id)

        # Gate evidence for link candidates
        gated = []
        for c in link_candidates:
            ok, reason = self.causal.validate_link_evidence(c)
            gated.append({"candidate": c.__dict__, "ok": ok, "gate_reason": reason})

        return {
            "node_id": node_id,
            "causal_links": gated,
            "resonance": [r.__dict__ for r in resonance_candidates],
        }

    def publish_guardrails(self) -> Dict[str, Any]:
        """Static guardrails for UI & agents."""
        return {
            "no_absolute_truth_claims": True,
            "require_sources_for_high_confidence": True,
            "store_uncertainty_explicitly": True,
            "human_in_the_loop": True,
        }
