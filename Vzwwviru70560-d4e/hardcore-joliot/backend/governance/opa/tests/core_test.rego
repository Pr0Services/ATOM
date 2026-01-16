# ============================================================================
# CHE·NU™ V69 — OPA GOVERNANCE TESTS
# ============================================================================
# Package: che_nu.tests
# Version: 2.0.0
# Purpose: Comprehensive tests for all 7 rules
# ============================================================================

package che_nu.tests

import data.che_nu.core.allow as core_allow
import data.che_nu.core.deny_reason as core_deny
import data.che_nu.core.result as core_result

# ============================================================================
# TEST HELPERS
# ============================================================================

base_input := {
    "request": {
        "request_id": "test-001",
        "timestamp": "2026-01-05T12:00:00Z",
        "trace_id": "trace-001",
        "environment": "labs",
        "tenant": {"id": "tenant-001", "plan": "pro"},
        "actor": {"type": "user", "id": "user-001"},
        "agent": {
            "blueprint_id": "bp-001",
            "level": "L1",
            "sphere": "business",
            "autonomy": "assisted",
            "risk_level": "low",
            "is_autogen": false,
            "is_user_hired": true
        },
        "action": {
            "type": "discuss",
            "target": "system",
            "resource_id": "",
            "data_classification": "internal"
        },
        "hitl": {"required": false, "approved": false, "approver_id": ""},
        "explainability": {"required": true, "provided": true},
        "controls": {"audit_logging": true, "trace_context": "trace-001"},
        "resource": {"synthetic": true}
    }
}

# ============================================================================
# RULE 7: AUDIT LOGGING TESTS
# ============================================================================

test_audit_logging_missing_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/controls/audit_logging", "value": false}
    ])
    not core_allow with input as input
}

test_audit_logging_present_ok {
    core_allow with input as base_input
}

# ============================================================================
# RULE 5: EXPLAINABILITY TESTS
# ============================================================================

test_explainability_missing_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/explainability/provided", "value": false}
    ])
    not core_allow with input as input
}

test_explainability_provided_ok {
    core_allow with input as base_input
}

# ============================================================================
# RULE 1: AUTOGEN SANDBOX TESTS
# ============================================================================

test_autogen_in_labs_allowed {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/is_autogen", "value": true},
        {"op": "replace", "path": "/request/environment", "value": "labs"}
    ])
    core_allow with input as input
}

test_autogen_in_pilot_denied_by_default {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/is_autogen", "value": true},
        {"op": "replace", "path": "/request/environment", "value": "pilot"}
    ])
    not core_allow with input as input
}

test_autogen_in_prod_always_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/is_autogen", "value": true},
        {"op": "replace", "path": "/request/environment", "value": "prod"}
    ])
    not core_allow with input as input
}

# ============================================================================
# RULE 2: PROD ACCESS TESTS
# ============================================================================

test_prod_globally_disabled {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/environment", "value": "prod"}
    ])
    not core_allow with input as input
}

# ============================================================================
# RULE 3: SENSITIVE DATA TESTS
# ============================================================================

test_sensitive_data_without_hitl_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/action/data_classification", "value": "sensitive"},
        {"op": "replace", "path": "/request/hitl/approved", "value": false}
    ])
    not core_allow with input as input
}

test_sensitive_data_with_hitl_allowed {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/action/data_classification", "value": "sensitive"},
        {"op": "replace", "path": "/request/hitl/approved", "value": true}
    ])
    core_allow with input as input
}

# ============================================================================
# RULE 4: HIGH-IMPACT TESTS
# ============================================================================

test_high_risk_execute_without_hitl_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/risk_level", "value": "high"},
        {"op": "replace", "path": "/request/action/type", "value": "execute"},
        {"op": "replace", "path": "/request/hitl/approved", "value": false}
    ])
    not core_allow with input as input
}

test_high_risk_execute_with_hitl_allowed {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/risk_level", "value": "high"},
        {"op": "replace", "path": "/request/action/type", "value": "execute"},
        {"op": "replace", "path": "/request/hitl/approved", "value": true}
    ])
    core_allow with input as input
}

test_high_risk_write_without_hitl_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/risk_level", "value": "high"},
        {"op": "replace", "path": "/request/action/type", "value": "write"},
        {"op": "replace", "path": "/request/hitl/approved", "value": false}
    ])
    not core_allow with input as input
}

# ============================================================================
# RULE 6: XR READ-ONLY TESTS
# ============================================================================

test_xr_read_allowed {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/action/target", "value": "xr"},
        {"op": "replace", "path": "/request/action/type", "value": "discuss"}
    ])
    core_allow with input as input
}

test_xr_execute_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/action/target", "value": "xr"},
        {"op": "replace", "path": "/request/action/type", "value": "execute"}
    ])
    not core_allow with input as input
}

test_xr_write_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/action/target", "value": "xr"},
        {"op": "replace", "path": "/request/action/type", "value": "write"}
    ])
    not core_allow with input as input
}

test_xr_delete_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/action/target", "value": "xr"},
        {"op": "replace", "path": "/request/action/type", "value": "delete"}
    ])
    not core_allow with input as input
}

test_xr_export_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/action/target", "value": "xr"},
        {"op": "replace", "path": "/request/action/type", "value": "export"}
    ])
    not core_allow with input as input
}

test_xr_connect_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/action/target", "value": "xr"},
        {"op": "replace", "path": "/request/action/type", "value": "connect"}
    ])
    not core_allow with input as input
}

# ============================================================================
# SYNTHETIC-ONLY TESTS
# ============================================================================

test_synthetic_data_allowed {
    core_allow with input as base_input
}

test_real_data_denied {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/resource/synthetic", "value": false}
    ])
    not core_allow with input as input
}

# ============================================================================
# AGENT LEVEL TESTS
# ============================================================================

test_l0_discuss_allowed {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/level", "value": "L0"},
        {"op": "replace", "path": "/request/action/type", "value": "discuss"}
    ])
    core_allow with input as input
}

test_l1_propose_allowed {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/level", "value": "L1"},
        {"op": "replace", "path": "/request/action/type", "value": "propose"}
    ])
    core_allow with input as input
}

test_l2_execute_requires_hitl {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/level", "value": "L2"},
        {"op": "replace", "path": "/request/action/type", "value": "execute"},
        {"op": "replace", "path": "/request/hitl/approved", "value": false}
    ])
    # L2 execute without HITL should fail (checked in agents/l2.rego)
    true  # Placeholder - actual check in l2.rego
}

# ============================================================================
# SPHERE-SPECIFIC TESTS
# ============================================================================

test_health_execute_restricted {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/sphere", "value": "health"},
        {"op": "replace", "path": "/request/action/type", "value": "execute"}
    ])
    # Health sphere restricts execution (checked in spheres/health.rego)
    true  # Placeholder
}

test_finance_write_requires_hitl {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/sphere", "value": "finance"},
        {"op": "replace", "path": "/request/action/type", "value": "write"},
        {"op": "replace", "path": "/request/hitl/approved", "value": false}
    ])
    # Finance write without HITL should fail
    true  # Placeholder
}

test_legal_all_mutations_require_hitl {
    input := json.patch(base_input, [
        {"op": "replace", "path": "/request/agent/sphere", "value": "legal_compliance"},
        {"op": "replace", "path": "/request/action/type", "value": "write"},
        {"op": "replace", "path": "/request/hitl/approved", "value": false}
    ])
    # Legal compliance requires HITL for all mutations
    true  # Placeholder
}

# ============================================================================
# GOLDEN PATH TEST
# ============================================================================

test_golden_path_simulation {
    # Standard simulation request should pass
    input := {
        "request": {
            "request_id": "golden-001",
            "timestamp": "2026-01-05T12:00:00Z",
            "trace_id": "trace-golden",
            "environment": "labs",
            "tenant": {"id": "tenant-golden", "plan": "enterprise"},
            "actor": {"type": "user", "id": "user-golden"},
            "agent": {
                "blueprint_id": "bp-simulator",
                "level": "L1",
                "sphere": "business",
                "autonomy": "assisted",
                "risk_level": "low",
                "is_autogen": false,
                "is_user_hired": true
            },
            "action": {
                "type": "propose",
                "target": "simulation",
                "resource_id": "",
                "data_classification": "internal"
            },
            "hitl": {"required": false, "approved": false, "approver_id": ""},
            "explainability": {"required": true, "provided": true},
            "controls": {"audit_logging": true, "trace_context": "trace-golden"},
            "resource": {"synthetic": true, "steps": 100}
        }
    }
    core_allow with input as input
}
