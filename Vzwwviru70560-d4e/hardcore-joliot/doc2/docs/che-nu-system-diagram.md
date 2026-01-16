# CHE·NU System Diagram

```mermaid
flowchart TD

    %% Spheres / Domains Layer
    subgraph S[UniverseOS v3]
        SPH[10 Spheres<br/>Personal, Business, Creative, Scholar,<br/>SocialMedia, Community, XR, MyTeam, AILab, Entertainment]
        DOM[Domains<br/>incl. Architecture, Architecture & Construction]
        ENG[Engines<br/>ArchitectEngine, BlueprintEngine, SpatialLayoutEngine, etc.]
    end

    SPH --> DOM
    DOM --> ENG

    %% Orchestrator
    ORCH[Orchestrator v3<br/>classifie input → sphere/domain/engines]
    ORCH --> CTX

    %% Context Layer
    subgraph C[ContextLayer v3]
        CTX[ContextSnapshot<br/>tools, processes, memory, templates]
    end

    %% Core Layers (Tools, Process, Template, Memory, Project)
    subgraph CORE[Core Layers]
        TL[ToolLayer v3]
        PL[ProcessLayer v3]
        TM[TemplateLayer v3]
        MEM[MemoryThreads v3]
        PROJ[ProjectLayer v3<br/>Projects → Missions → Phases]
    end

    CTX --> TL
    CTX --> PL
    CTX --> TM
    CTX --> MEM
    CTX --> PROJ

    %% Workspace & DataSpace
    subgraph WS[Workspace Ecosystem]
        UWL[Universal Workspace Layer v1<br/>buildAdaptiveWorkspace]
        DS[DataSpace Layer v1<br/>notes/resources/archive/config/log]
        WSF[Unified WorkSurface v1<br/>modes: text, table, blocks, diagram,<br/> xr_layout, summary, final]
        WSA[WorkSurface Adaptation Engine<br/>classify + suggest mode]
    end

    ORCH --> UWL
    UWL --> DS
    UWL --> WSF
    WSF --> WSA
    DS --> MEM

    %% XR Layer
    subgraph XR[XR Layer v3]
        XRS[XRScene]
        XRU[XRUniverse]
        XRT[XR Presets<br/>architectureRoom,<br/> floorGridRoom, structuralVolumeRoom]
        XRN[XR Navigation / Portals]
    end

    UWL --> XRS
    XRS --> XRU
    XRU --> XRN
    XRT --> XRS

    %% Chat & Vocal
    subgraph CV[Chat & Vocal System]
        CHAT[Chat Interface<br/>Source of Truth]
        VOICE[Voice Input<br/>Transcribe → Confirm → Send]
        INBOX[Agent Inboxes<br/>Messages, Tasks, Context]
    end

    CHAT --> INBOX
    VOICE --> CHAT

    %% UI Layer
    subgraph UI[UI Layer]
        WSD[WorkspaceDashboard]
        WSU[WorkSurface UI<br/>toolbar + mode switcher + views]
        XRM[XRUniverseMapView]
        DEMO[Demo Pages<br/>Architecture Universe,<br/> Business+Architecture]
    end

    UWL --> WSD
    WSF --> WSU
    XRU --> XRM
    XRM --> DEMO
    WSD --> DEMO
    INBOX --> WSD

    %% Demo Suite
    subgraph DEMOS[Demo Suite]
        D1[Demo Architecture Universe v2]
        D2[Demo Business + Architecture]
        DSU[Demo Suite Script<br/>run all demos]
    end

    UWL --> D1
    DS --> D1
    XRU --> D1

    UWL --> D2
    DS --> D2
    XRS --> D2

    DEMO --> D1
    DEMO --> D2
    DSU --> D1
    DSU --> D2
```

## Layer Descriptions

### UniverseOS v3
- **10 Spheres**: Personal, Business, Creative, Scholar, SocialMedia, Community, XR, MyTeam, AILab, Entertainment
- **Domains**: Specialized areas within spheres (e.g., Architecture in Creative)
- **Engines**: Processing engines for each domain

### Core Layers
- **ContextLayer**: Snapshot of current context (tools, processes, memory, templates)
- **ToolLayer**: Available tools and toolchains
- **ProcessLayer**: Process models and workflows
- **TemplateLayer**: Document and structure templates
- **MemoryThreads**: Conceptual memory threads
- **ProjectLayer**: Projects → Missions → Phases hierarchy

### Workspace Ecosystem
- **Universal Workspace Layer**: Adaptive workspace generation
- **DataSpace Layer**: Data storage (notes, resources, archives, config, logs)
- **Unified WorkSurface**: Multi-mode editor (text, table, blocks, diagram, xr_layout, summary, final)
- **Adaptation Engine**: Auto-suggests modes based on input

### XR Layer
- **XRScene**: Individual XR scenes/rooms
- **XRUniverse**: Collection of connected scenes
- **XR Presets**: Pre-configured scene templates
- **Navigation/Portals**: Scene-to-scene connections

### Chat & Vocal System
- **Chat Interface**: Source of truth for all communications
- **Voice Input**: Speech-to-text with confirmation
- **Agent Inboxes**: Per-agent message and task queues

### UI Layer
- **WorkspaceDashboard**: Main workspace view
- **WorkSurface UI**: Editor interface with mode switching
- **XRUniverseMapView**: Visual map of XR universe
- **Demo Pages**: Interactive demonstrations
