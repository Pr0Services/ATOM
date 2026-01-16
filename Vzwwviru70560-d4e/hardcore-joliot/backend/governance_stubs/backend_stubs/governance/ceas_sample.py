"""Sample CEAs — minimal examples.
They are intentionally light and cheap.
"""
from __future__ import annotations
from typing import List, Any, Dict
from .models import GovernanceSignal, Scope

class CanonGuardCEA:
    id = "CANON_GUARD"
    criterion = "canon"

    def observe(self, *, thread_id: str, window: Dict[str, Any]) -> List[GovernanceSignal]:
        # Example checks (adapt):
        # - ensure no attempt to delete/overwrite events
        # - ensure XR state isn't written as truth
        signals: List[GovernanceSignal] = []
        if window.get("attempts", {}).get("event_delete"):
            signals.append(GovernanceSignal(
                level="BLOCK",
                criterion=self.criterion,
                message="Append-only violation: attempted event deletion.",
                scope=Scope(segment_id=window.get("segment_id")),
                confidence=0.95,
            ))
        return signals

class SchemaGuardCEA:
    id = "SCHEMA_GUARD"
    criterion = "schema"

    def observe(self, *, thread_id: str, window: Dict[str, Any]) -> List[GovernanceSignal]:
        # Validate structured outputs (json schema) if present
        signals: List[GovernanceSignal] = []
        schema_ok = window.get("schema_ok", True)
        if not schema_ok:
            signals.append(GovernanceSignal(
                level="CORRECT",
                criterion=self.criterion,
                message="Schema mismatch detected; patch output to match schema.",
                scope=Scope(segment_id=window.get("segment_id")),
                confidence=0.8,
            ))
        return signals

class CoherenceGuardCEA:
    id = "COHERENCE_GUARD"
    criterion = "coherence"

    def observe(self, *, thread_id: str, window: Dict[str, Any]) -> List[GovernanceSignal]:
        signals: List[GovernanceSignal] = []
        if window.get("intent_drift", False):
            signals.append(GovernanceSignal(
                level="CORRECT",
                criterion=self.criterion,
                message="Detected drift from founding intent; realign segment.",
                scope=Scope(segment_id=window.get("segment_id"), region=window.get("region")),
                confidence=0.75,
            ))
        return signals

class BudgetGuardCEA:
    id = "BUDGET_GUARD"
    criterion = "budget"

    def observe(self, *, thread_id: str, window: Dict[str, Any]) -> List[GovernanceSignal]:
        signals: List[GovernanceSignal] = []
        latency_ms = window.get("latency_ms", 0)
        latency_budget = window.get("budgets", {}).get("latency_ms", 999999)
        if latency_ms > latency_budget:
            signals.append(GovernanceSignal(
                level="WARN",
                criterion=self.criterion,
                message=f"Latency exceeded budget: {latency_ms}ms > {latency_budget}ms",
                scope=Scope(segment_id=window.get("segment_id")),
                confidence=0.7,
            ))
        return signals
