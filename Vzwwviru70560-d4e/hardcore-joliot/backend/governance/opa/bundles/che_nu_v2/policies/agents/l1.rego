# ============================================================================
# CHE·NU™ V69 — L1 AGENT POLICY (User-Hired Agents)
# ============================================================================
# Package: che_nu.agents.l1
# Version: 2.0.0
# Role: User-hired specialist agents (168+ types)
# Autonomy: ASSISTED
# Can: Discuss, propose, plan
# Cannot: Execute by default
# Special: User defines scope at hiring
# ============================================================================

package che_nu.agents.l1

# L1 agents cannot execute by default
deny_reason[msg] {
    input.request.agent.level == "L1"
    input.request.action.type == "execute"
    not execution_explicitly_allowed
    msg := "L1_NO_EXECUTION_BY_DEFAULT"
}

# Execution can be allowed with explicit scope grant
execution_explicitly_allowed {
    input.request.agent.scope_grants[_] == "execute"
    input.request.hitl.approved == true
}

# L1 allowed actions
l1_allowed_actions := ["discuss", "propose", "plan"]

allow {
    input.request.agent.level == "L1"
    input.request.action.type == l1_allowed_actions[_]
}

# L1 can write proposals (not actual data)
allow {
    input.request.agent.level == "L1"
    input.request.action.type == "write"
    input.request.action.target == "proposal"
}

# L1 sphere restriction - must match authorized sphere
deny_reason[msg] {
    input.request.agent.level == "L1"
    input.request.agent.sphere != ""
    input.request.action.target_sphere != ""
    input.request.agent.sphere != input.request.action.target_sphere
    msg := "L1_SPHERE_MISMATCH"
}

# L1 capabilities
capabilities := {
    "level": "L1",
    "name": "User-Hired Agent",
    "role": "Specialist",
    "autonomy": "assisted",
    "allowed_actions": l1_allowed_actions,
    "conditional_actions": ["write:proposal", "execute:with_hitl"],
    "description": "User-hired specialists. Propose and plan, but need approval to execute."
}
