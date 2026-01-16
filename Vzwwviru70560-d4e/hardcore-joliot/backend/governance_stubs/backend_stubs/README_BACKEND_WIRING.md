# Backend wiring notes

- Put these stubs under something like:
  backend/app/governance/
    models.py
    cea_interface.py
    ceas_sample.py
    orchestrator.py
    event_store.py
    routes.py

- Plug `ThreadEventStore.append` into your real DB (thread_events table).
- Route integration:
  include_router(governance.routes.router)

- Auth:
  - /signal should accept system/agent submissions, not random users (unless debugging)
  - /run should require governance permission
  - /backlog should require triage/admin or system

- Redaction/permissions:
  run_governance should not leak redacted content; only handle signals and patch instructions.
