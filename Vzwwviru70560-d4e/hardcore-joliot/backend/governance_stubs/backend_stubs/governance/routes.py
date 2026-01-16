"""FastAPI routes — governance pipeline stubs."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from .models import GovernanceSignal, OrchestratorDecision
from .orchestrator import Orchestrator
from .event_store import ThreadEventStore

router = APIRouter(prefix="/threads/{thread_id}/governance", tags=["governance"])

# Instantiate these via dependency injection in real app
orch = Orchestrator()
store = ThreadEventStore()

@router.post("/signal", response_model=Dict[str, Any])
def post_signal(thread_id: str, signal: GovernanceSignal):
    # Auth: must have permission to submit signal (agents/system)
    # Log signal as event
    try:
        store.append_system(thread_id=thread_id, event_type="GOVERNANCE_SIGNAL", payload=signal.model_dump())
    except NotImplementedError:
        pass
    return {"status":"ok"}

@router.post("/run", response_model=Dict[str, Any])
def run_governance(thread_id: str, body: Dict[str, Any]):
    """Run governance cycle for a given context window.
    body = { context: {...}, signals: [...] }
    """
    context = body.get("context", {})
    signals_raw = body.get("signals", [])
    signals: List[GovernanceSignal] = [GovernanceSignal(**s) for s in signals_raw]

    decisions: List[OrchestratorDecision] = orch.decide_from_signals(thread_id=thread_id, signals=signals, context=context)

    # Log decisions
    for d in decisions:
        try:
            store.append_system(thread_id=thread_id, event_type="ORCH_DECISION_MADE", payload=d.model_dump())
        except NotImplementedError:
            pass

    return {"decisions":[d.model_dump() for d in decisions]}

@router.post("/backlog", response_model=Dict[str, Any])
def create_backlog_item(thread_id: str, body: Dict[str, Any]):
    """Create backlog item linked to events. Analytics/learning store, not canonical truth."""
    # You may store into backlog_items table AND emit BACKLOG_ITEM_CREATED event
    try:
        store.append_system(thread_id=thread_id, event_type="BACKLOG_ITEM_CREATED", payload=body)
    except NotImplementedError:
        pass
    return {"status":"created"}
