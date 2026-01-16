# 🏛️ CHE·NU™ V69 — GOVERNANCE MODULE

> **GOUVERNANCE > EXÉCUTION**

## Overview

This module implements the **7 Core Governance Rules** for CHE·NU™ using Open Policy Agent (OPA).

## The 7 Rules

| # | Rule | Description |
|---|------|-------------|
| 1 | **AutoGen Sandbox** | AutoGen agents only in LABS |
| 2 | **PROD Allowlist** | PROD access requires explicit allowlist |
| 3 | **Sensitive Data HITL** | Sensitive data requires human approval |
| 4 | **High-Impact HITL** | High-risk actions require human approval |
| 5 | **Explainability** | All decisions must be explainable |
| 6 | **XR Read-Only** | XR is read-only, never write/execute |
| 7 | **Audit Logging** | All decisions must be audited |

## Architecture

```
governance/
├── opa/
│   ├── bundles/
│   │   └── che_nu_v2/
│   │       ├── manifest.json
│   │       ├── data.json
│   │       └── policies/
│   │           ├── core.rego          # 7 rules
│   │           ├── base.rego          # Helpers
│   │           ├── simulation.rego    # Simulation rules
│   │           ├── artifacts.rego     # Artifact rules
│   │           ├── exports.rego       # Export rules
│   │           ├── env/               # Environment policies
│   │           ├── agents/            # Agent level policies
│   │           └── spheres/           # Sphere policies
│   ├── tests/
│   │   └── core_test.rego
│   └── docker/
│       └── docker-compose.opa.yml
└── python/
    ├── __init__.py
    ├── models.py              # Pydantic models
    ├── opa_client.py          # OPA client
    ├── middleware.py          # FastAPI middleware
    └── requirements.txt
```

## Quick Start

### 1. Start OPA

```bash
cd governance/opa/docker
docker compose -f docker-compose.opa.yml up -d
```

### 2. Test Policy

```bash
curl -X POST http://localhost:8181/v1/data/che_nu/core/result \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "request": {
        "environment": "labs",
        "tenant": {"id": "t1", "plan": "pro"},
        "actor": {"type": "user", "id": "u1"},
        "agent": {
          "blueprint_id": "bp1",
          "level": "L1",
          "sphere": "business",
          "risk_level": "low",
          "is_autogen": false
        },
        "action": {
          "type": "discuss",
          "target": "system",
          "data_classification": "internal"
        },
        "hitl": {"approved": false},
        "explainability": {"required": true, "provided": true},
        "controls": {"audit_logging": true},
        "resource": {"synthetic": true}
      }
    }
  }'
```

### 3. Python Integration

```python
from governance import (
    OPAClient,
    create_simulation_request,
    setup_governance,
)

# Direct client usage
client = OPAClient()
request = create_simulation_request(
    tenant_id="tenant-001",
    user_id="user-001",
    agent_blueprint="bp-simulator",
    steps=100,
)
decision = await client.decide(request)

if decision.allow:
    # Proceed with simulation
    pass
else:
    # Handle denial
    print(f"Denied: {decision.deny_reasons}")

# FastAPI middleware
from fastapi import FastAPI
app = FastAPI()
setup_governance(app)
```

## Configuration

### data.json

```json
{
  "che_nu": {
    "config": {
      "allow_prod": false,
      "allow_autogen_in_pilot": false,
      "max_simulation_steps": 5000,
      "exports_require_human": true,
      "synthetic_only": true,
      "xr_read_only": true
    },
    "prod_allowlist": {
      "tenants": [],
      "agent_blueprints": []
    }
  }
}
```

## Testing

```bash
# Run OPA tests
docker exec chenu-opa opa test /bundles -v

# Run Python tests
pytest governance/python -v
```

## Key Principles

1. **Default Deny** - Everything is denied unless explicitly allowed
2. **Human Sovereignty** - Critical decisions require human approval
3. **Synthetic Only** - Only synthetic data, never real
4. **XR Read-Only** - XR visualizes, never executes
5. **Auditability** - Every decision is logged

---

**CHE·NU™ — GOUVERNANCE > EXÉCUTION**
