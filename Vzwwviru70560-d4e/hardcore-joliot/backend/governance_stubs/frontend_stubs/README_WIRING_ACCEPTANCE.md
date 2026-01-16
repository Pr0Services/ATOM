# Wiring Acceptance Tests (Quick)

1) Post a GOVERNANCE_SIGNAL and verify it is appended as a ThreadEvent.
2) Run governance cycle and verify ORCH_DECISION_MADE events appended.
3) For a CORRECT signal in live mode, orchestrator returns PATCH decision.
4) applyGovernanceDecisions posts PATCH_INSTRUCTION event.
5) Create backlog item and verify BACKLOG_ITEM_CREATED event appended.
