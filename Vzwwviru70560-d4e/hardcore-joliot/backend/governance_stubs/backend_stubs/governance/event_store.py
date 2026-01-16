"""ThreadEvent store integration points — stubs.
Replace with your DB + append-only enforcement.
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from pydantic import BaseModel
import uuid, datetime

class ThreadEvent(BaseModel):
    event_id: str
    thread_id: str
    event_type: str
    created_at: str
    actor_type: str
    actor_id: str
    payload: Dict[str, Any]

def now_iso() -> str:
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

class ThreadEventStore:
    def append(self, event: ThreadEvent) -> None:
        # TODO: insert into thread_events (append-only)
        # enforce: no updates/deletes
        raise NotImplementedError

    def append_system(self, *, thread_id: str, event_type: str, payload: Dict[str, Any]) -> None:
        evt = ThreadEvent(
            event_id=str(uuid.uuid4()),
            thread_id=thread_id,
            event_type=event_type,
            created_at=now_iso(),
            actor_type="system",
            actor_id="orchestrator",
            payload=payload,
        )
        self.append(evt)
