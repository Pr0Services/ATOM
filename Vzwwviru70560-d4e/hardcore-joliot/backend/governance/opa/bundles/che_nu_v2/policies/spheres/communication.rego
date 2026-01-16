# ============================================================================
# CHE·NU™ V69 — COMMUNICATION SPHERE POLICY
# ============================================================================
package che_nu.spheres.communication

default allow := true

# Outbound communication requires HITL (prevent spam/abuse)
deny_reason[msg] {
    input.request.agent.sphere == "communication"
    input.request.action.type == "execute"
    not input.request.hitl.approved
    msg := "COMMUNICATION_OUTBOUND_REQUIRES_HITL"
}

# External messaging requires HITL
deny_reason[msg] {
    input.request.agent.sphere == "communication"
    input.request.action.type == "connect"
    input.request.action.target == "external_messaging"
    not input.request.hitl.approved
    msg := "COMMUNICATION_EXTERNAL_MSG_REQUIRES_HITL"
}
