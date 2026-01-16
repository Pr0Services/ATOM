# ============================================================================
# CHE·NU™ V69 — L0 AGENT POLICY (NOVA - System Intelligence)
# ============================================================================
# Package: che_nu.agents.l0
# Version: 2.0.0
# Role: Nova - Central system intelligence
# Autonomy: INFORMATIONAL ONLY
# Can: Discuss, analyze, coordinate
# Cannot: Execute, mutate, write
# ============================================================================

package che_nu.agents.l0

# L0 (Nova) is informational only - no execution or mutation
deny_reason[msg] {
    input.request.agent.level == "L0"
    input.request.action.type == "execute"
    msg := "L0_NOVA_NO_EXECUTION"
}

deny_reason[msg] {
    input.request.agent.level == "L0"
    input.request.action.type == "write"
    msg := "L0_NOVA_NO_WRITE"
}

deny_reason[msg] {
    input.request.agent.level == "L0"
    input.request.action.type == "delete"
    msg := "L0_NOVA_NO_DELETE"
}

deny_reason[msg] {
    input.request.agent.level == "L0"
    input.request.action.type == "export"
    msg := "L0_NOVA_NO_EXPORT"
}

deny_reason[msg] {
    input.request.agent.level == "L0"
    input.request.action.type == "connect"
    msg := "L0_NOVA_NO_CONNECT"
}

# L0 allowed actions
l0_allowed_actions := ["discuss", "propose", "plan"]

allow {
    input.request.agent.level == "L0"
    input.request.action.type == l0_allowed_actions[_]
}

# L0 capabilities
capabilities := {
    "level": "L0",
    "name": "Nova",
    "role": "System Intelligence",
    "autonomy": "informational",
    "allowed_actions": l0_allowed_actions,
    "denied_actions": ["execute", "write", "delete", "export", "connect"],
    "description": "Central coordination and analysis. Never executes."
}
