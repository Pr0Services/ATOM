# AT-OM / CHE-NU — Governance Pipeline Code Stubs (PR-Ready)
Date: 2026-01-06

This package provides **plug-and-play stubs** for implementing:
- CEAs (Criterion Enforcement Agents) -> Governance Signals
- Orchestrator -> Decisions / Patch Instructions / Escalations
- ThreadEvent logging (append-only)
- Backlog capture (errors, noise, cost, decision outcomes)
- Minimal API routes (FastAPI) + TS client helpers

## Intended integration
Adapt folder placement to your repo:
- backend_stubs/* -> FastAPI services
- frontend_stubs/* -> TS app client + UI hooks

## Non-negotiables
- Thread is source of truth; all writes are ThreadEvents.
- CEAs do not directly modify outputs; they emit signals.
- Orchestrator is the single decision authority.
- Backlogs are learning/analytics linked to events.
