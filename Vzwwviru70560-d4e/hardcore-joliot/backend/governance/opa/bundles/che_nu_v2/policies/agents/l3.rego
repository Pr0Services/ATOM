# ============================================================================
# CHE·NU™ V69 — L3 AGENT POLICY (System Agents)
# ============================================================================
# Package: che_nu.agents.l3
# Version: 2.0.0
# Role: Critical system agents (backup, recovery, audit)
# Autonomy: RESTRICTED
# Can: Execute critical ops (with strict HITL)
# Special: PROD disabled by default, requires explicit pinning
# ============================================================================

package che_nu.agents.l3

# L3 agents require HITL for everything beyond discuss
deny_reason[msg] {
    input.request.agent.level == "L3"
    input.request.action.type == "execute"
    not input.request.hitl.approved
    msg := "L3_EXEC_REQUIRES_HITL"
}

deny_reason[msg] {
    input.request.agent.level == "L3"
    input.request.action.type == "write"
    not input.request.hitl.approved
    msg := "L3_WRITE_REQUIRES_HITL"
}

deny_reason[msg] {
    input.request.agent.level == "L3"
    input.request.action.type == "delete"
    not input.request.hitl.approved
    msg := "L3_DELETE_REQUIRES_HITL"
}

# L3 DISABLED IN PROD by default
deny_reason[msg] {
    input.request.agent.level == "L3"
    input.request.environment == "prod"
    not l3_pinned_for_prod
    msg := "L3_PROD_DISABLED_UNLESS_PINNED"
}

# L3 can be pinned for PROD via explicit config
l3_pinned_for_prod {
    input.request.agent.prod_pinned == true
    input.request.agent.pin_approval_id != ""
}

# L3 free actions (informational only)
l3_free_actions := ["discuss"]

allow {
    input.request.agent.level == "L3"
    input.request.action.type == l3_free_actions[_]
}

# L3 with HITL in non-prod
allow {
    input.request.agent.level == "L3"
    input.request.action.type == "execute"
    input.request.hitl.approved == true
    input.request.environment != "prod"
}

allow {
    input.request.agent.level == "L3"
    input.request.action.type == "execute"
    input.request.hitl.approved == true
    input.request.environment == "prod"
    l3_pinned_for_prod
}

# L3 critical operations require multi-approval
deny_reason[msg] {
    input.request.agent.level == "L3"
    critical_operation
    not multi_approval
    msg := "L3_CRITICAL_OP_REQUIRES_MULTI_APPROVAL"
}

critical_operation {
    input.request.action.type == "delete"
    input.request.action.target == "system"
}

critical_operation {
    input.request.action.type == "execute"
    input.request.action.target == "recovery"
}

multi_approval {
    input.request.hitl.approved == true
    count(input.request.hitl.approvers) >= 2
}

# L3 audit level is always critical
audit_level := "critical" {
    input.request.agent.level == "L3"
}

# L3 capabilities
capabilities := {
    "level": "L3",
    "name": "System Agent",
    "role": "Critical Operations",
    "autonomy": "restricted",
    "allowed_actions": l3_free_actions,
    "hitl_required_actions": ["propose", "plan", "execute", "write", "delete", "export", "connect"],
    "prod_allowed": false,
    "multi_approval_operations": ["delete:system", "execute:recovery"],
    "description": "Critical system agents. Maximum restriction. PROD disabled by default."
}
