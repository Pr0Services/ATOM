# SCHEMAS — Reference Examples

## Example 1: Basic Structure

```json
{
  "_meta": {
    "type": "schemas",
    "version": "1.0",
    "safe": true
  },
  "id": "SCHEMAS_001",
  "name": "Example Structure",
  "description": "A basic example of Schemas output"
}
```

## Example 2: With References

```json
{
  "_meta": {
    "type": "schemas",
    "version": "1.0"
  },
  "id": "SCHEMAS_002",
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
