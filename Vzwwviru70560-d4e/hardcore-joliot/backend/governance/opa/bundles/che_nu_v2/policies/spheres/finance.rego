# ============================================================================
# CHE·NU™ V69 — FINANCE SPHERE POLICY
# ============================================================================
package che_nu.spheres.finance

default allow := true

# Financial writes require HITL (critical for accuracy)
deny_reason[msg] {
    input.request.agent.sphere == "finance"
    input.request.action.type == "write"
    not input.request.hitl.approved
    msg := "FINANCE_WRITE_REQUIRES_HITL"
}

# Financial exports require HITL
deny_reason[msg] {
    input.request.agent.sphere == "finance"
    input.request.action.type == "export"
    not input.request.hitl.approved
    msg := "FINANCE_EXPORT_REQUIRES_HITL"
}

# Transaction execution requires HITL
deny_reason[msg] {
    input.request.agent.sphere == "finance"
    input.request.action.type == "execute"
    input.request.action.target == "transaction"
    not input.request.hitl.approved
    msg := "FINANCE_TRANSACTION_REQUIRES_HITL"
}

# Audit level is elevated for finance
audit_level := "elevated"
