# CHE·NU™ V75 - OPA Governance Policy
# RÈGLE ABSOLUE: GOUVERNANCE > EXÉCUTION

package chenu.governance

import future.keywords.if
import future.keywords.in

# =============================================================================
# DEFAULT: DENY
# =============================================================================
# En cas de doute → DENY
default allow := false

# =============================================================================
# AGENT OPERATIONS
# =============================================================================

# Hiring agents requires valid user and non-system agent
allow if {
    input.operation == "agent.hire"
    valid_user
    not is_system_agent(input.resource.id)
}

# Cannot fire Nova (L0 system agent)
allow if {
    input.operation == "agent.fire"
    valid_user
    not is_nova(input.resource.id)
}

# Assigning tasks requires hired agent
allow if {
    input.operation == "agent.assign_task"
    valid_user
}

# =============================================================================
# GOVERNANCE OPERATIONS
# =============================================================================

# Approving checkpoints requires human (not agent)
allow if {
    input.operation == "governance.approve"
    valid_user
    input.user.type != "agent"
}

# Rejecting checkpoints requires human
allow if {
    input.operation == "governance.reject"
    valid_user
    input.user.type != "agent"
}

# =============================================================================
# DECISION OPERATIONS
# =============================================================================

# Resolving decisions requires human
allow if {
    input.operation == "decision.resolve"
    valid_user
    input.user.type != "agent"
}

# =============================================================================
# XR OPERATIONS
# =============================================================================

# XR generation only on backend
allow if {
    input.operation == "xr.generate"
    valid_user
    input.context.source == "backend"
}

# =============================================================================
# THREAD OPERATIONS
# =============================================================================

# Thread deletion requires owner or admin
allow if {
    input.operation == "thread.delete"
    valid_user
    is_admin_or_owner
}

# Thread archiving requires participant
allow if {
    input.operation == "thread.archive"
    valid_user
}

# =============================================================================
# DATASPACE OPERATIONS
# =============================================================================

# DataSpace deletion requires owner
allow if {
    input.operation == "dataspace.delete"
    valid_user
    is_admin_or_owner
}

# =============================================================================
# IDENTITY OPERATIONS
# =============================================================================

# Identity switching always allowed for valid user
allow if {
    input.operation == "identity.switch"
    valid_user
}

# =============================================================================
# NOVA OPERATIONS
# =============================================================================

# Nova execute may require checkpoint for certain actions
allow if {
    input.operation == "nova.execute"
    valid_user
    not requires_checkpoint
}

# Nova execute with checkpoint approval
allow if {
    input.operation == "nova.execute"
    valid_user
    requires_checkpoint
    checkpoint_approved
}

# =============================================================================
# HELPER RULES
# =============================================================================

valid_user if {
    input.user.id != null
    input.user.id != ""
}

is_system_agent(agent_id) if {
    agent_id == "nova"
}

is_nova(agent_id) if {
    agent_id == "nova"
}

is_admin_or_owner if {
    "admin" in input.user.roles
}

is_admin_or_owner if {
    input.resource.owner_id == input.user.id
}

# Determine if operation requires checkpoint
requires_checkpoint if {
    input.context.action_type == "external_api"
}

requires_checkpoint if {
    input.context.cost_amount > 1000
}

requires_checkpoint if {
    input.context.sensitivity == "high"
}

checkpoint_approved if {
    input.context.checkpoint_status == "approved"
}

# =============================================================================
# CHECKPOINT REQUIREMENTS
# =============================================================================

# Return whether this operation requires a checkpoint
checkpoint_required[operation] := true if {
    operation := input.operation
    requires_checkpoint_for_operation(operation)
}

requires_checkpoint_for_operation(op) if {
    op == "agent.hire"
}

requires_checkpoint_for_operation(op) if {
    op == "nova.execute"
    input.context.action_type == "external_api"
}

requires_checkpoint_for_operation(op) if {
    op in ["dataspace.delete", "thread.delete"]
}

# =============================================================================
# AUDIT LOGGING
# =============================================================================

# All decisions are logged
decision := {
    "allow": allow,
    "operation": input.operation,
    "user_id": input.user.id,
    "timestamp": input.context.timestamp,
    "requires_checkpoint": requires_checkpoint,
}
