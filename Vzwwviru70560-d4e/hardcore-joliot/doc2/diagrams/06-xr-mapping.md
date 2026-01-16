# XR Interface Mapping

```mermaid
flowchart TB
    subgraph TwoD["🖥️ 2D INTERFACE"]
        Z1_2D["Zone 1: Interaction"]
        Z2_2D["Zone 2: Navigation"]
        Z3_2D["Zone 3: Conception"]
    end
    
    subgraph XR["🥽 XR INTERFACE"]
        Z1_XR["Spatial: Nova Space"]
        Z2_XR["Spatial: Sphere Room"]
        Z3_XR["Spatial: Workspace"]
    end
    
    subgraph Core["⚙️ SHARED CORE"]
        GOV_CORE["Governance Layer"]
        BUDGET_CORE["Budget System"]
        API_CORE["Same APIs"]
    end

    Z1_2D <-->|"Same Logic"| Z1_XR
    Z2_2D <-->|"Same Logic"| Z2_XR
    Z3_2D <-->|"Same Logic"| Z3_XR
    
    Z1_2D --> Core
    Z1_XR --> Core
    Z2_2D --> Core
    Z2_XR --> Core
    Z3_2D --> Core
    Z3_XR --> Core

    style TwoD fill:#3b82f6,color:#fff
    style XR fill:#8b5cf6,color:#fff
    style Core fill:#10b981,color:#fff
```

## XR Rules

1. **XR is interface-only** — same backend
2. **Same governance in spatial**
3. **Same confirmation requirements**
4. **Same budget enforcement**
5. **No spatial shortcuts to bypass consent**
6. **No implicit recording in XR**
