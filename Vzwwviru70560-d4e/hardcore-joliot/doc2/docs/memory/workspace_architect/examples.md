# WORKSPACE ARCHITECT — Reference Examples

## Example 1: Dashboard Layout

```json
{
  "workspace": {
    "id": "WS_DASHBOARD_001",
    "name": "Project Dashboard",
    "grid": {"columns": 12, "rows": "auto"},
    "panels": [
      {"id": "PANEL_HEADER", "span": 12, "row": 1},
      {"id": "PANEL_SIDEBAR", "span": 3, "row": 2},
      {"id": "PANEL_MAIN", "span": 9, "row": 2}
    ],
    "safe": true
  }
}
```

---
Status: SAFE • NON-AUTONOMOUS
