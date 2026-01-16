# PR Plan — Governance Pipeline Stubs

## PR Title
feat(governance): add CEAs->Orchestrator->Patch pipeline + backlog capture (stubs)

## Steps
1) Add shared types (events, signals, patch instructions)
2) Add CEA interface + sample guards (CanonGuard, SchemaGuard, CoherenceGuard, BudgetGuard)
3) Add Orchestrator skeleton (QCT+SES+RDC hooks)
4) Add FastAPI routes:
   - POST /threads/{id}/governance/signal
   - POST /threads/{id}/governance/run
   - POST /threads/{id}/governance/backlog
5) Add TS client helpers + hook style adapters
6) Add acceptance tests checklist for wiring
