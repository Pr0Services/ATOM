# EXHIBIT F: MEMBER ONBOARDING SYSTEM

**Patent Application:** CHENU-2026-001-PROV
**Document Type:** Invitation and Onboarding Flow
**Classification:** PUBLIC - Safe for Patent Disclosure

---

## 1. OVERVIEW

The system implements a controlled invitation mechanism for onboarding founding members, with energy-based qualification and activation within a global coordination grid.

---

## 2. INVITATION MODEL

### 2.1 Invitation Structure

```
INVITATION RECORD:
+-- code (unique alphanumeric)
+-- invited_name
+-- invited_email (optional)
+-- personal_message
+-- founder_type (classification)
+-- contribution_note
+-- status (pending/accepted/expired/revoked)
+-- usage_limits
+-- expiration_date
+-- timestamps
```

### 2.2 Code Format

Codes follow pattern: `PREFIX-XXXX-XXXX`
- Alphanumeric characters
- Excludes ambiguous characters (0/O, 1/I/L)
- Human-readable format

---

## 3. FOUNDER CLASSIFICATION

```
+-------------------------------------------------------------------+
|  TYPE          | ROLE                                             |
+-------------------------------------------------------------------+
|  Light Point   | International community anchor                   |
|  Guardian      | System protection and stability                  |
|  Architect     | Structural design and planning                   |
|  Weaver        | Connection building between members              |
|  Carrier       | Mission propagation and expansion                |
+-------------------------------------------------------------------+
```

---

## 4. ONBOARDING FLOW

```
+-------------------------------------------------------------------+
|                    MEMBER ONBOARDING PROCESS                      |
+-------------------------------------------------------------------+
|                                                                   |
|    [Invitation Created]                                           |
|          |                                                        |
|          v                                                        |
|    +-------------+                                                |
|    | Code        | <-- Unique invitation sent                     |
|    | Distributed |                                                |
|    +------+------+                                                |
|           |                                                       |
|           v                                                       |
|    +-------------+                                                |
|    | Code        | <-- User enters code                           |
|    | Validation  |                                                |
|    +------+------+                                                |
|           |                                                       |
|           v                                                       |
|    +-------------+                                                |
|    | Account     | <-- Create or link account                     |
|    | Creation    |                                                |
|    +------+------+                                                |
|           |                                                       |
|           v                                                       |
|    +-------------+                                                |
|    | Founder     | <-- Assign number, type, initial status        |
|    | Profile     |                                                |
|    +------+------+                                                |
|           |                                                       |
|           v                                                       |
|    +-------------+                                                |
|    | Energy      | <-- Calibration period begins                  |
|    | Calibration |                                                |
|    +-------------+                                                |
|                                                                   |
+-------------------------------------------------------------------+
```

---

## 5. ENERGY GRID INTEGRATION

### 5.1 Founder Grid Profile

Each founder has grid coordinates and energy status:

```
FOUNDER GRID PROFILE:
+-- grid_coordinates (latitude/longitude)
+-- location_name
+-- energy_signature (frequency assignment)
+-- energy_status (calibrating/aligned/activated/dormant)
+-- contribution_type
+-- grid_activation_date
```

### 5.2 Energy Status Progression

```
CALIBRATING --> ALIGNED --> ACTIVATED
                              |
                              v
                          (DORMANT if paused)
```

- **Calibrating**: Initial period after joining
- **Aligned**: Energy verified, ready for activation
- **Activated**: Full Grid participation
- **Dormant**: Temporary pause

### 5.3 Energy Signatures

Founders receive frequency assignments from the spectrum (111-999 Hz range) that determine their resonance within the grid.

---

## 6. GLOBAL GRID STRUCTURE

### 6.1 Grid Points

```
GRID POINT TYPES:
+-- Anchor: Primary stability points
+-- Node: Connection intersections
+-- Portal: Energy transition zones
+-- Sanctuary: Protected spaces
```

### 6.2 Grid Point Record

```
GRID POINT:
+-- name
+-- coordinates
+-- point_type
+-- frequency
+-- guardian (optional founder)
+-- connected_count
+-- activation_status
```

---

## 7. FOUNDER CONNECTIONS

Members can establish connections with types:

- **Resonance**: Energy alignment
- **Collaboration**: Joint projects
- **Mentorship**: Guidance relationship
- **Friendship**: Personal connection

---

## 8. SECURITY MODEL

### 8.1 Invitation Security

- Only Sovereign can create invitations
- Codes have usage limits and expiration
- Single-use by default

### 8.2 Grid Access

- Grid visibility requires activated status
- Location data protected by RLS
- Connection requests require mutual acceptance

### 8.3 Role Elevation

Accepting invitation automatically upgrades user role to Founder level.

---

## 9. KEY FEATURES

1. **Controlled Onboarding**: Invitation-only access
2. **Founder Sequencing**: Numbered by arrival order
3. **Energy Calibration**: Qualification period before activation
4. **Global Coordination**: Geographic grid mapping
5. **Connection Network**: Inter-member relationship tracking

---

## 10. INITIAL ANCHOR POINT

System bootstraps with an initial anchor point at the origin location, establishing the grid center.

---

**END OF EXHIBIT F**

*This document describes the onboarding concepts and structure without revealing specific qualification thresholds, activation algorithms, or detailed implementation.*
