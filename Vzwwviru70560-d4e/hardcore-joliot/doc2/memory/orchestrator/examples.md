# ORCHESTRATOR — Reference Examples

## Example 1: Basic Structure

```json
{
  "_meta": {
    "type": "orchestrator",
    "version": "1.0",
    "safe": true
  },
  "id": "ORCHESTRATOR_001",
  "name": "Example Structure",
  "description": "A basic example of Orchestrator output"
}
```

## Example 2: With References

```json
{
  "_meta": {
    "type": "orchestrator",
    "version": "1.0"
  },
  "id": "ORCHESTRATOR_002",
  "references": [
    "@ref:SCHEMA_BASE",
    "@ref:GLOBAL_CONFIG"
  ]
}
```

## Example 3: Complete Output

<!-- Claude: Complete with role-specific examples -->

---
Status: SAFE • NON-AUTONOMOUS
