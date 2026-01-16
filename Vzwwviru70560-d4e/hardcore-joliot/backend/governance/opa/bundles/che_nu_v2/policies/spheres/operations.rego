# ============================================================================
# CHE·NU™ V69 — OPERATIONS SPHERE POLICY
# ============================================================================
package che_nu.spheres.operations

default allow := true

# External connections require HITL (security)
deny_reason[msg] {
    input.request.agent.sphere == "operations"
    input.request.action.type == "connect"
    not input.request.hitl.approved
    msg := "OPERATIONS_CONNECT_REQUIRES_HITL"
}

# System modifications require HITL
deny_reason[msg] {
    input.request.agent.sphere == "operations"
    input.request.action.type == "execute"
    input.request.action.target == "system"
    not input.request.hitl.approved
    msg := "OPERATIONS_SYSTEM_EXEC_REQUIRES_HITL"
}
