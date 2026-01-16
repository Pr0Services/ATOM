# CARTOGRAPHY DESIGNER — Reference Examples

## Example: Project Map

```json
{
  "uc_map": {
    "id": "UC_MAP_PROJECT_001",
    "name": "Project Overview",
    "regions": [
      {"id": "REG_CORE", "name": "Core System", "bounds": {"x1":0,"y1":0,"x2":10,"y2":10}},
      {"id": "REG_EXT", "name": "Extensions", "bounds": {"x1":10,"y1":0,"x2":20,"y2":10}}
    ],
    "paths": [
      {"id": "PATH_001", "from": "REG_CORE", "to": "REG_EXT", "type": "dependency"}
    ],
    "safe": true
  }
}
```

---
Status: SAFE • NON-AUTONOMOUS
