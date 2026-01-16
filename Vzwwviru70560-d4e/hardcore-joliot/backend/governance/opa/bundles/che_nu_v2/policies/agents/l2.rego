# ============================================================================
# CHE·NU™ V69 — L2 AGENT POLICY (Platform Agents)
# ============================================================================
# Package: che_nu.agents.l2
# Version: 2.0.0
# Role: Platform service agents
# Autonomy: GOVERNED
# Can: Discuss, propose, plan, execute (with HITL)
# Special: Execution requires human approval
# ============================================================================

package che_nu.agents.l2

# L2 agents can execute but require HITL approval
deny_reason[msg] {
    input.request.agent.level == "L2"
    input.request.action.type == "execute"
    not input.request.hitl.approved
    msg := "L2_EXEC_REQUIRES_HITL"
}

# L2 mutations also require HITL
deny_reason[msg] {
    input.request.agent.level == "L2"
    mutation_action
    not input.request.hitl.approved
    msg := "L2_MUTATION_REQUIRES_HITL"
}

mutation_action {
    input.request.action.type == "write"
}
mutation_action {
    input.request.action.type == "delete"
}
mutation_action {
    input.request.action.type == "export"
}
mutation_action {
    input.request.action.type == "connect"
}

# L2 allowed actions without HITL
l2_free_actions := ["discuss", "propose", "plan"]

allow {
    input.request.agent.level == "L2"
    input.request.action.type == l2_free_actions[_]
}

# L2 allowed with HITL
allow {
    input.request.agent.level == "L2"
    input.request.action.type == "execute"
    input.request.hitl.approved == true
}

allow {
    input.request.agent.level == "L2"
    mutation_action
    input.request.hitl.approved == true
}

# L2 rate limiting (platform protection)
deny_reason[msg] {
    input.request.agent.level == "L2"
    input.request.rate_limit_exceeded == true
    msg := "L2_RATE_LIMIT_EXCEEDED"
}

# L2 capabilities
capabilities := {
    "level": "L2",
    "name": "Platform Agent",
    "role": "Service Provider",
    "autonomy": "governed",
    "allowed_actions": l2_free_actions,
    "hitl_required_actions": ["execute", "write", "delete", "export", "connect"],
    "description": "Platform service agents. Can execute with human approval."
}
