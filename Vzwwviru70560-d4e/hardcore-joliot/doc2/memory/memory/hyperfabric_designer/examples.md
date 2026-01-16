# HYPERFABRIC DESIGNER — Reference Examples

## Example 1: Basic Node Network

```json
{
  "hyperfabric": {
    "id": "HF_NETWORK_001",
    "nodes": [
      {"id": "HF_NODE_001", "coordinates": {"x":0,"y":0,"z":0,"t":"2025-01","s":"project","p":1}},
      {"id": "HF_NODE_002", "coordinates": {"x":1,"y":0,"z":0,"t":"2025-01","s":"task","p":0.8}}
    ],
    "links": [
      {"id": "HF_LINK_001_002", "from": "HF_NODE_001", "to": "HF_NODE_002", "type": "contains"}
    ],
    "safe": true
  }
}
```

---
Status: SAFE • NON-AUTONOMOUS
