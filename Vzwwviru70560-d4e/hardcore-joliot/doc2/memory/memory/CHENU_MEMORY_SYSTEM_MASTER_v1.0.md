############################################################
#  CHE·NU MEMORY SYSTEM — MASTER MODULE (SAFE • DOCUMENTARY ONLY)
#  VERSION: 1.0
#  THIS MODULE IS FULLY NON-AUTONOMOUS AND REPRESENTATIONAL
############################################################

============================================================
[SECTION 1] — PURPOSE OF THE MEMORY SYSTEM
============================================================

The CHE·NU Memory System is a SAFE, NON-AUTONOMOUS framework
designed to store external documentation for each CHE·NU role.

It does NOT:
- store internal model memory
- evolve or modify itself automatically
- learn, adapt, or remember across sessions
- act as an agent
- create autonomous processes

It ONLY:
- creates structured memory folders
- organizes notes on user command
- consolidates role documentation
- outputs Markdown/JSON files for external storage
- assists in documentation workflows

Everything is explicit, static, user-driven.


============================================================
[SECTION 2] — CORE COMMANDS (OFFICIAL, SAFE)
============================================================

-----------------------------
COMMAND: ADD_TO_MEMORY
-----------------------------
Purpose:
Transform user-provided text into a structured external memory file.

This command:
✔ organizes text  
✔ formats it (Markdown/JSON)  
✔ saves it into the designated role's folder  
✔ creates summaries or merges existing memory  

ADD_TO_MEMORY NEVER:
❌ stores anything inside the model  
❌ creates persistent memory  
❌ updates itself autonomously  
❌ retains information between sessions  

Usage examples:
ADD_TO_MEMORY(role:xr_scene_builder, content:"rules for mesh placement")
ADD_TO_MEMORY(role:hyperfabric_designer, content:"new axis concept")
ADD_TO_MEMORY(role:orchestrator, content:"routing guidelines")


-----------------------------
COMMAND: READ_MEMORY
-----------------------------
Purpose:
Retrieve or reconstruct a file from the CHE·NU memory folder.

READ_MEMORY NEVER:
❌ implies internal memory  
❌ retrieves from a persistent store  
❌ maintains context automatically  

It ONLY:
✔ reformats documents  
✔ reconstructs files the user provides  
✔ summarizes external stored data  

Usage examples:
READ_MEMORY(role:morphology_designer, file:"rules.md")
READ_MEMORY(role:xr_scene_builder, summary:true)


============================================================
[SECTION 3] — OFFICIAL MEMORY DIRECTORY STRUCTURE
============================================================

/memory/
   /orchestrator/
   /xr_scene_builder/
   /workspace_architect/
   /hyperfabric_designer/
   /cartography_designer/
   /depth_lens_system/
   /projection_engine/
   /morphology_designer/
   /schemas/
   /global/
   index.md
   CHENU_MEMORY_SYSTEM_MASTER_v1.0.md


============================================================
[SECTION 4] — UNIVERSAL ROLE MEMORY TEMPLATE
============================================================

Each role folder contains:

1. role.md          → Identity & Purpose  
2. rules.md         → Operational rules  
3. style.md         → Formatting style  
4. examples.md      → Valid representative samples  
5. forbidden.md     → Disallowed actions  
6. notes.md         → User/developer notes  
7. integration.md   → How the role connects to others  
8. todo.md          → Tasks for refining role  
9. index.json       → Structural reference index  


============================================================
[SECTION 5] — ROLE REGISTRY
============================================================

| # | Role | Folder | Purpose |
|---|------|--------|---------|
| 1 | Orchestrator | /orchestrator/ | Intent routing & coordination |
| 2 | XR Scene Builder | /xr_scene_builder/ | XR_SCENE JSON generation |
| 3 | Workspace Architect | /workspace_architect/ | Layout & panel design |
| 4 | HyperFabric Designer | /hyperfabric_designer/ | Multi-axis topology |
| 5 | Cartography Designer | /cartography_designer/ | UC_MAP structures |
| 6 | Depth & Lens System | /depth_lens_system/ | Cognitive depth layers |
| 7 | Projection Engine | /projection_engine/ | 2D/3D projections |
| 8 | Morphology Designer | /morphology_designer/ | Abstract symbols |
| 9 | Schemas | /schemas/ | JSON Schema definitions |
| 10 | Global | /global/ | System-wide config |


============================================================
[SECTION 6] — MEMORY OPERATIONS API
============================================================

## ADD_TO_MEMORY

```
ADD_TO_MEMORY(
  role: string,           // Target role folder
  content: string,        // Content to add
  file?: string,          // Target file (default: notes.md)
  format?: "md" | "json", // Output format
  merge?: boolean         // Merge with existing
)
```

## READ_MEMORY

```
READ_MEMORY(
  role: string,           // Source role folder
  file?: string,          // Specific file to read
  summary?: boolean,      // Return summary only
  format?: "md" | "json"  // Output format
)
```

## LIST_MEMORY

```
LIST_MEMORY(
  role?: string,          // Specific role (optional)
  tree?: boolean          // Show full tree structure
)
```


============================================================
[SECTION 7] — SAFETY CONSTRAINTS
============================================================

## This System IS:
- ✅ Static — No dynamic updates
- ✅ External — Files stored outside model
- ✅ User-controlled — Only acts on explicit command
- ✅ Representational — Outputs blueprints only

## This System HAS:
- ❌ NO internal memory
- ❌ NO autonomous updates
- ❌ NO evolution or learning
- ❌ NO cross-session persistence
- ❌ NO agent behavior


============================================================
[SECTION 8] — FREEZE BLOCK COMPLIANCE
============================================================

All memory operations respect CHE·NU FREEZE BLOCK:

1. No self-modification
2. No autonomous behavior
3. No persistent storage in model
4. No emotional simulation
5. No humanoid content
6. User approval required for all operations


============================================================
[SECTION 9] — INTEGRATION WITH CHE·NU MODULES
============================================================

## Memory → Orchestrator
- Provides routing documentation
- Stores decision patterns (static)

## Memory → XR Pack
- Stores scene templates
- Defines visual standards

## Memory → HyperFabric
- Documents topology rules
- Stores axis definitions

## Memory → Projection
- Contains view presets
- Stores projection configs


============================================================
[SECTION 10] — VERSION HISTORY
============================================================

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-11 | Initial release |
| - | - | Full structure with 10 roles |
| - | - | ADD_TO_MEMORY command |
| - | - | READ_MEMORY command |
| - | - | Safety constraints defined |


============================================================
END OF CHE·NU MEMORY SYSTEM — MASTER MODULE
============================================================
