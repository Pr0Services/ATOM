"""Criterion Enforcement Agent (CEA) interface — stubs."""
from __future__ import annotations
from typing import Protocol, List, Any, Dict
from .models import GovernanceSignal

class CEA(Protocol):
    id: str
    criterion: str

    def observe(self, *, thread_id: str, window: Dict[str, Any]) -> List[GovernanceSignal]:
        """Inspect a window of derived state/output and emit governance signals."""
        ...
