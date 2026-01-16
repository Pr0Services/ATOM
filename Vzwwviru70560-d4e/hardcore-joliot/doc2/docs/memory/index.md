# CHE·NU Memory Index

============================================================
OFFICIAL MEMORY SYSTEM — DOCUMENTARY ONLY
SAFE • NON-AUTONOMOUS • NO INTERNAL STORAGE
============================================================

## Overview

This directory contains externally stored **DOCUMENTS ONLY**.
- NO persistence or internal model memory
- NO autonomous updates
- NO state tracking
- Manually or user-updated through ADD_TO_MEMORY commands

## Roles Included

| Folder | Purpose |
|--------|---------|
| `/orchestrator/` | CHE·NU orchestrator logic & routing rules |
| `/xr_scene_builder/` | XR Scene generation JSON schema + examples |
| `/workspace_architect/` | Workspace layouts, panels, dashboards |
| `/hyperfabric_designer/` | Multi-axis topology nodes, links, slices |
| `/cartography_designer/` | UC_MAP structures, maps, diagrams |
| `/depth_lens_system/` | Surface/structure/logic/depth/lens outputs |
| `/projection_engine/` | Projection styles (2D, axono, layered) |
| `/morphology_designer/` | Symbolic forms, morphotypes, materials |
| `/schemas/` | Global schemas (XR_SCENE, MAP_SCENE, HF_SCENE…) |
| `/global/` | General notes, versioning, FREEZE copies |

## File Structure Per Role

Each role folder contains:
```
role.md          → Identity & purpose
rules.md         → Operational rules
style.md         → Output style guide
examples.md      → Reference examples
forbidden.md     → Disallowed actions
notes.md         → Developer notes
integration.md   → Module connections
todo.md          → Task list
index.json       → Structural index
```

## Safety Declaration

This memory system:
- ✅ Stores files EXTERNALLY only
- ✅ Does NOT persist inside the model
- ✅ Does NOT learn or adapt
- ✅ Does NOT run autonomously
- ✅ Requires explicit user command

## Usage

To add content to memory:
```
ADD_TO_MEMORY: [your content] → [target role]
```

---
Version: 2.0
Status: SAFE • STATIC • NON-AUTONOMOUS
