# ============================================================================
# CHE·NU™ V69 — PILOT ENVIRONMENT POLICY
# ============================================================================
# Package: che_nu.env.pilot
# Version: 2.0.0
# Purpose: Controlled testing before production
# ============================================================================

package che_nu.env.pilot

import data.che_nu.config

# Pilot is more restricted than Labs
default allow := true

# AutoGen restrictions in Pilot
deny_reason[msg] {
    input.request.agent.is_autogen == true
    not config.allow_autogen_in_pilot
    msg := "AUTOGEN_NOT_ALLOWED_IN_PILOT"
}

deny_reason[msg] {
    input.request.agent.is_autogen == true
    config.allow_autogen_in_pilot
    input.request.action.type == "execute"
    msg := "AUTOGEN_CANNOT_EXECUTE_IN_PILOT"
}

# High-risk actions require HITL in Pilot
deny_reason[msg] {
    input.request.agent.risk_level == "high"
    input.request.action.type == "execute"
    not input.request.hitl.approved
    msg := "PILOT_HIGH_RISK_EXEC_REQUIRES_HITL"
}

# Exports require HITL in Pilot
deny_reason[msg] {
    input.request.action.type == "export"
    not input.request.hitl.approved
    msg := "PILOT_EXPORT_REQUIRES_HITL"
}

# XR still read-only
deny_reason[msg] {
    input.request.action.target == "xr"
    input.request.action.type == "write"
    msg := "XR_WRITE_DENIED_IN_PILOT"
}

deny_reason[msg] {
    input.request.action.target == "xr"
    input.request.action.type == "execute"
    msg := "XR_EXECUTE_DENIED_IN_PILOT"
}

# Pilot must be synthetic
deny_reason[msg] {
    input.request.resource.synthetic == false
    msg := "PILOT_REQUIRES_SYNTHETIC_DATA"
}

# Pilot settings
max_concurrent_simulations := 5
max_users := 100
