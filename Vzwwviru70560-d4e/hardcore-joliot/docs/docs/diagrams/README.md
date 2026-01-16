# CHE·NU — System Diagrams

## Overview

This directory contains the 6 canonical diagrams for the CHE·NU system.
All diagrams use Mermaid syntax and can be rendered in GitHub, VS Code, or any Mermaid viewer.

## Diagrams

| # | Diagram | Description |
|---|---------|-------------|
| 1 | [System Hierarchy](01-system-hierarchy.md) | Authority flow: User → Nova → Orchestrator → Agents → System |
| 2 | [Action Flow](02-action-flow.md) | Intent → Proposal → Explanation → Confirmation → Execution → Report |
| 3 | [Interaction Zones](03-interaction-zones.md) | 3 zones: Interaction · Navigation · Conception |
| 4 | [Budget Flow](04-budget-flow.md) | Preset → Sphere → Project → Meeting → Ledger |
| 5 | [Meeting Lifecycle](05-meeting-lifecycle.md) | Create → Work → Optional AI → End → Optional Summary |
| 6 | [XR Mapping](06-xr-mapping.md) | 2D Zones ↔ Spatial Zones (same governance) |

## Key Principles

All diagrams reflect:

- **Human authority is final**
- **No execution without confirmation**
- **No silent automation**
- **Budgets enforced before action**
- **XR is interface-only (same rules)**

## Rendering

### GitHub
Diagrams render automatically in GitHub markdown.

### VS Code
Install "Markdown Preview Mermaid Support" extension.

### CLI
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.md -o diagram.png
```

---

**CHE·NU™ — Governed Intelligence OS**
