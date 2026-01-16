# CHEÂ·NU ARCHITECTURE DIAGRAMS v29
## Complete Mermaid Diagrams Collection

---

## 1. COMPLETE ENGINE STACK OVERVIEW

```mermaid
graph TB
    subgraph "USER LAYER"
        UI[User Interface]
        OCW[OCW - Operational Cognitive Workspace]
        WS[Workspace Engine]
    end
    
    subgraph "ACTION LAYER"
        OC[1-Click Assistant Engine]
        AO[Agent Orchestrator]
    end
    
    subgraph "INTELLIGENCE LAYER"
        BI[Backstage Intelligence]
        AG[168+ Agents]
    end
    
    subgraph "SAFETY LAYER"
        MG[Memory & Governance Engine]
        AUDIT[Audit System]
    end
    
    subgraph "DATA LAYER"
        DS[DataSpace Engine]
        TH[Thread Engine]
        FT[File Transform Engine]
    end
    
    subgraph "DOMAIN LAYER"
        IMM[Immobilier]
        CON[Construction]
        FIN[Finance]
        ARC[Architecture]
    end
    
    subgraph "EXPERIENCE LAYER"
        MT[Meeting System]
        XR[XR Spatial Engine]
    end
    
    UI --> OCW
    UI --> WS
    OCW --> OC
    WS --> OC
    OC --> BI
    OC --> AO
    AO --> AG
    BI --> AG
    AG --> MG
    MG --> DS
    MG --> TH
    DS --> IMM
    DS --> CON
    DS --> FIN
    DS --> ARC
    MT --> DS
    XR --> DS
    MG --> AUDIT
```

---

## 2. IDENTITY & SPHERE HIERARCHY

```mermaid
graph TB
    subgraph "USER"
        U[User Account]
    end
    
    subgraph "IDENTITIES"
        IP[Personal Identity]
        IE[Enterprise Identity]
        IC[Creative Identity]
        ID[Design Identity]
        IA[Architecture Identity]
        ICO[Construction Identity]
    end
    
    subgraph "SPHERES"
        SM[Maison Sphere]
        SE[Entreprise Sphere]
        SC[Creative Sphere]
        SS[Scholar Sphere]
        ST[Team Sphere]
    end
    
    subgraph "DOMAINS"
        DF[Finance Domain]
        DI[Immobilier Domain]
        DCO[Construction Domain]
        DAR[Architecture Domain]
        DHR[HR Domain]
        DOP[Operations Domain]
    end
    
    U --> IP
    U --> IE
    U --> IC
    U --> ID
    U --> IA
    U --> ICO
    
    IP --> SM
    IE --> SE
    IC --> SC
    ID --> SC
    IA --> SE
    ICO --> SE
    
    SM --> DF
    SM --> DI
    SE --> DCO
    SE --> DAR
    SE --> DHR
    SE --> DOP
```

---

## 3. 1-CLICK ASSISTANT WORKFLOW

```mermaid
flowchart TB
    subgraph "INPUT"
        A[User Command]
        B[File Upload]
        C[Context]
        D[DataSpace]
    end
    
    subgraph "INTENT INTERPRETER"
        E[Parse Intent]
        F[Detect Domain]
        G[Identify Sphere]
        H[Find Gaps]
    end
    
    subgraph "WORKFLOW CONSTRUCTOR"
        I[Build Pipeline]
        J[Assign Tasks]
        K[Map Dependencies]
        L[Add Checkpoints]
    end
    
    subgraph "AGENT ORCHESTRATOR"
        M[Select Agents]
        N[Coordinate Actions]
        O[Monitor Compliance]
        P[Quality Check]
    end
    
    subgraph "OUTPUT SYNTHESIZER"
        Q[Assemble Results]
        R[Format Output]
        S[Generate Dashboard]
        T[Store in DataSpace]
    end
    
    subgraph "GOVERNANCE"
        U[Verify Permissions]
        V[Log Actions]
        W[Enable Undo]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F --> G --> H
    H --> I --> J --> K --> L
    L --> M --> N --> O --> P
    P --> Q --> R --> S --> T
    
    M --> U
    T --> V
    V --> W
```

---

## 4. MEMORY & GOVERNANCE FLOW

```mermaid
flowchart TB
    subgraph "MEMORY TYPES"
        ST[Short-Term Memory]
        MT[Mid-Term Memory]
        LT[Long-Term Memory]
        IM[Institutional Memory]
        AM[Agent Memory]
    end
    
    subgraph "STORAGE"
        DS[DataSpaces]
        TH[Threads]
        IP[Identity Profiles]
        DL[Domain Libraries]
        AC[Agent Configs]
    end
    
    subgraph "GOVERNANCE CHECKS"
        IC[Identity Check]
        PC[Permission Check]
        DC[Domain Check]
        SC[Sphere Check]
    end
    
    subgraph "ACTIONS"
        APP[Approve]
        BLK[Block]
        ELV[Elevate]
        LOG[Log]
    end
    
    ST --> DS
    MT --> DS
    MT --> TH
    LT --> IP
    LT --> DL
    IM --> DL
    AM --> AC
    
    DS --> IC
    IC --> PC
    PC --> DC
    DC --> SC
    
    SC --> APP
    SC --> BLK
    SC --> ELV
    
    APP --> LOG
    BLK --> LOG
    ELV --> LOG
```

---

## 5. WORKSPACE ENGINE MODES

```mermaid
flowchart LR
    subgraph "WORKSPACE MODES"
        DOC[Document Mode]
        BRD[Board Mode]
        TML[Timeline Mode]
        SPR[Spreadsheet Mode]
        DSH[Dashboard Mode]
        DGM[Diagram Mode]
        WBD[Whiteboard Mode]
        XRM[XR Mode]
        HYB[Hybrid Mode]
    end
    
    subgraph "TRANSFORMATIONS"
        T1[Data Preserved]
        T2[Layout Adapted]
        T3[Reversible]
    end
    
    DOC <--> T1
    BRD <--> T1
    TML <--> T1
    SPR <--> T1
    DSH <--> T1
    DGM <--> T1
    WBD <--> T1
    XRM <--> T1
    
    T1 <--> T2
    T2 <--> T3
```

---

## 6. BACKSTAGE INTELLIGENCE PIPELINE

```mermaid
sequenceDiagram
    participant U as User
    participant WS as Workspace
    participant BI as Backstage Intelligence
    participant CL as Classifier
    participant PR as Pre-Processor
    participant AG as Agents
    participant DS as DataSpace
    
    U->>WS: User Action
    WS->>BI: Context Signal
    BI->>CL: Classify Input
    CL->>BI: Classification
    BI->>PR: Pre-process
    PR->>BI: Prepared Data
    BI->>AG: Suggest Agents
    BI->>DS: Fetch Relevant Data
    DS->>BI: Context Data
    BI->>WS: Ready State
    WS->>U: Instant Response
```

---

## 7. AGENT HIERARCHY (L0-L3)

```mermaid
graph TB
    subgraph "L0 - MASTER ORCHESTRATOR"
        L0A[ARIA - Master AI]
    end
    
    subgraph "L1 - DEPARTMENT HEADS"
        L1A[Construction Chief]
        L1B[Finance Chief]
        L1C[HR Chief]
        L1D[Operations Chief]
        L1E[Immobilier Chief]
    end
    
    subgraph "L2 - SPECIALISTS"
        L2A[Estimator]
        L2B[Materials Expert]
        L2C[Safety Inspector]
        L2D[Accountant]
        L2E[Property Manager]
        L2F[Lease Analyst]
    end
    
    subgraph "L3 - SUPPORT"
        L3A[Data Entry]
        L3B[Document Processor]
        L3C[Calculator]
        L3D[Report Generator]
    end
    
    L0A --> L1A
    L0A --> L1B
    L0A --> L1C
    L0A --> L1D
    L0A --> L1E
    
    L1A --> L2A
    L1A --> L2B
    L1A --> L2C
    L1B --> L2D
    L1E --> L2E
    L1E --> L2F
    
    L2A --> L3A
    L2A --> L3B
    L2D --> L3C
    L2E --> L3D
```

---

## 8. DATASPACE RELATIONSHIPS

```mermaid
erDiagram
    DATASPACE ||--o{ DATASPACE_ITEM : contains
    DATASPACE ||--o{ DATASPACE_LINK : links
    DATASPACE }o--|| IDENTITY : belongs_to
    DATASPACE }o--o| SPHERE : scoped_to
    DATASPACE }o--o| DOMAIN : typed_by
    DATASPACE ||--o{ THREAD : has
    DATASPACE ||--o{ FILE : stores
    
    DATASPACE {
        uuid id
        string name
        string type
        uuid identity_id
        uuid sphere_id
        uuid domain_id
        jsonb metadata
    }
    
    DATASPACE_ITEM {
        uuid id
        uuid dataspace_id
        string type
        text content
    }
    
    DATASPACE_LINK {
        uuid id
        uuid source_id
        uuid target_id
        string link_type
    }
```

---

## 9. MEETING SYSTEM FLOW

```mermaid
stateDiagram-v2
    [*] --> Scheduled
    Scheduled --> Active: Start Meeting
    Active --> Active: Add Notes
    Active --> Active: Record Decisions
    Active --> Active: Create Tasks
    Active --> Completed: End Meeting
    Completed --> [*]
    
    state Active {
        [*] --> Running
        Running --> Paused: Pause
        Paused --> Running: Resume
        Running --> XR_Mode: Enter XR
        XR_Mode --> Running: Exit XR
    }
    
    state Completed {
        [*] --> Processing
        Processing --> Summary_Generated
        Summary_Generated --> Tasks_Routed
        Tasks_Routed --> [*]
    }
```

---

## 10. IMMOBILIER DOMAIN MODEL

```mermaid
erDiagram
    PROPERTY ||--o{ UNIT : has
    PROPERTY ||--o{ TENANT : leases_to
    PROPERTY ||--o{ MAINTENANCE : requires
    TENANT ||--o{ PAYMENT : makes
    PROPERTY }o--|| DATASPACE : stored_in
    
    PROPERTY {
        uuid id
        string type
        string address
        decimal value
        string status
    }
    
    UNIT {
        uuid id
        string number
        decimal rent
        string status
    }
    
    TENANT {
        uuid id
        string name
        date lease_start
        date lease_end
        decimal monthly_rent
    }
    
    PAYMENT {
        uuid id
        date payment_date
        decimal amount
        string status
    }
    
    MAINTENANCE {
        uuid id
        string title
        string category
        string priority
        string status
    }
```

---

## 11. CONSTRUCTION PROJECT WORKFLOW

```mermaid
flowchart TB
    subgraph "PLANNING"
        A[Project Created]
        B[Requirements Gathered]
        C[Estimate Created]
    end
    
    subgraph "ESTIMATION"
        D[Materials Listed]
        E[Labor Calculated]
        F[Equipment Added]
        G[Total Generated]
    end
    
    subgraph "APPROVAL"
        H[Estimate Submitted]
        I{Approved?}
        J[Revision Required]
    end
    
    subgraph "EXECUTION"
        K[Permits Obtained]
        L[Work Started]
        M[Progress Tracked]
        N[Inspections]
    end
    
    subgraph "COMPLETION"
        O[Final Inspection]
        P[Project Closed]
        Q[Documentation Filed]
    end
    
    A --> B --> C
    C --> D --> E --> F --> G
    G --> H --> I
    I -->|Yes| K
    I -->|No| J
    J --> C
    K --> L --> M --> N
    N --> O --> P --> Q
```

---

## 12. OCW SESSION ARCHITECTURE

```mermaid
flowchart TB
    subgraph "HOST"
        H[Host User]
        HC[Host Controls]
    end
    
    subgraph "PARTICIPANTS"
        P1[Editor 1]
        P2[Editor 2]
        P3[Viewer]
        P4[Agent Spectator]
    end
    
    subgraph "CANVAS"
        OBJ[Canvas Objects]
        ANN[Annotations]
        DRW[Drawings]
    end
    
    subgraph "SYNC"
        WS[WebSocket Server]
        ST[State Manager]
        CF[Conflict Resolver]
    end
    
    H --> HC
    HC --> WS
    
    P1 --> WS
    P2 --> WS
    P3 --> WS
    P4 --> WS
    
    WS --> ST
    ST --> CF
    CF --> OBJ
    CF --> ANN
    CF --> DRW
    
    OBJ --> WS
    ANN --> WS
    DRW --> WS
```

---

## 13. XR SPATIAL ENGINE

```mermaid
flowchart TB
    subgraph "INPUT SOURCES"
        BP[Blueprints]
        MD[3D Models]
        DS[DataSpaces]
        MT[Meetings]
    end
    
    subgraph "XR ENGINE"
        SP[Spatial Parser]
        RG[Room Generator]
        OB[Object Manager]
        AV[Avatar System]
    end
    
    subgraph "XR ROOM"
        SC[Scene]
        OBJ[Objects]
        USR[Users]
        INT[Interactions]
    end
    
    subgraph "OUTPUT"
        VR[VR Experience]
        AR[AR Overlay]
        DT[Desktop 3D]
        MB[Mobile View]
    end
    
    BP --> SP
    MD --> SP
    DS --> RG
    MT --> RG
    
    SP --> RG
    RG --> SC
    OB --> OBJ
    AV --> USR
    
    SC --> VR
    SC --> AR
    SC --> DT
    SC --> MB
```

---

## 14. GOVERNANCE AUDIT TRAIL

```mermaid
sequenceDiagram
    participant U as User
    participant A as Action
    participant G as Governance
    participant P as Permission
    participant L as Audit Log
    participant R as Reversibility
    
    U->>A: Request Action
    A->>G: Check Governance
    G->>P: Verify Permission
    
    alt Permission Granted
        P->>A: Approved
        A->>L: Log Action
        L->>R: Save State
        A->>U: Action Complete
    else Permission Denied
        P->>G: Denied
        G->>U: Explain Denial
    else Elevation Required
        P->>G: Needs Elevation
        G->>U: Request Approval
        U->>G: Approve/Deny
        G->>L: Log Decision
    end
```

---

## 15. COMPLETE DATA FLOW

```mermaid
flowchart TB
    subgraph "USER INPUT"
        CMD[Command]
        FILE[File]
        CTX[Context]
    end
    
    subgraph "PROCESSING"
        BI[Backstage Intelligence]
        OC[1-Click Engine]
        AG[Agents]
    end
    
    subgraph "GOVERNANCE"
        MG[Memory & Governance]
        ID[Identity Check]
        PM[Permission Check]
    end
    
    subgraph "STORAGE"
        DS[DataSpaces]
        TH[Threads]
        FL[Files]
    end
    
    subgraph "OUTPUT"
        DOC[Documents]
        DSH[Dashboards]
        XRS[XR Scenes]
        RPT[Reports]
    end
    
    CMD --> BI
    FILE --> BI
    CTX --> BI
    
    BI --> OC
    OC --> AG
    AG --> MG
    
    MG --> ID
    ID --> PM
    
    PM --> DS
    PM --> TH
    PM --> FL
    
    DS --> DOC
    DS --> DSH
    DS --> XRS
    DS --> RPT
```

---

## 16. MULTI-LLM INTEGRATION

```mermaid
flowchart TB
    subgraph "ROUTER"
        R[LLM Router]
    end
    
    subgraph "PROVIDERS"
        CL[Claude - Anthropic]
        GP[GPT-4 - OpenAI]
        GM[Gemini - Google]
        OL[Ollama - Local]
    end
    
    subgraph "TASKS"
        AN[Analysis]
        CR[Creative]
        CD[Code]
        VS[Vision]
    end
    
    R --> CL
    R --> GP
    R --> GM
    R --> OL
    
    AN --> R
    CR --> R
    CD --> R
    VS --> R
    
    CL --> |Primary|AN
    CL --> |Primary|CR
    GP --> |Fallback|AN
    GM --> |Vision|VS
    OL --> |Local/Private|CD
```

---

*CHEÂ·NU Architecture Diagrams v29 - December 2024*
