"""Governance models (pydantic) — stubs.
Adapt to your auth + thread event store.
"""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Any, Dict, Literal, Optional

SignalLevel = Literal["WARN","CORRECT","PAUSE","BLOCK","ESCALATE"]

class Scope(BaseModel):
    segment_id: Optional[str] = None
    region: Optional[str] = None
    zone_id: Optional[str] = None
    item_id: Optional[str] = None

class GovernanceSignal(BaseModel):
    level: SignalLevel
    criterion: str
    message: str
    scope: Scope = Field(default_factory=Scope)
    confidence: float = 0.5
    references: Dict[str, Any] = Field(default_factory=dict)

class PatchInstruction(BaseModel):
    scope: Scope
    constraint: str
    correction: str
    rationale: str
    verification_spec_id: Optional[str] = None

class OrchestratorDecision(BaseModel):
    decision_id: str
    action: Literal["RUN_SPEC","DEFER_SPEC","ESCALATE","PATCH","BLOCK","NOOP"]
    reason: str
    scope: Scope = Field(default_factory=Scope)
    required_quality: float = 0.5
    budgets: Dict[str, Any] = Field(default_factory=dict)
    payload: Dict[str, Any] = Field(default_factory=dict)
"""
