# EXHIBIT B: SOVEREIGN DATABASE ARCHITECTURE

**Patent Application:** CHENU-2026-001-PROV
**Document Type:** Database Schema Description
**Classification:** PUBLIC - Safe for Patent Disclosure

---

## 1. OVERVIEW

The system implements a sovereign database architecture where each qualifying member receives isolated data storage with centralized orchestration.

---

## 2. TABLE STRUCTURE

### 2.1 Member Registry

```
TABLE: members_grid
├── id (unique identifier)
├── user_id (authentication reference)
├── role_id (access tier)
├── full_name
├── email
├── energy_signature (frequency assignment)
├── resonance_score (qualification metric)
├── is_active (activation status)
├── activation_date
└── timestamps (created, updated)
```

**Purpose:** Stores member information with their assigned energy signature and calculated resonance score.

### 2.2 Database Provisioning

```
TABLE: sovereign_databases
├── id (unique identifier)
├── member_id (reference to member)
├── db_name (unique database identifier)
├── db_region (geographic location)
├── db_status (provisioning state)
├── connection_credentials (encrypted)
├── allocated_tokens (resource quota)
├── used_tokens (consumption tracking)
├── storage_metrics
└── timestamps
```

**Purpose:** Tracks provisioned database instances for each member with their resource allocation.

### 2.3 Distribution Configuration

```
TABLE: resource_relays
├── id (unique identifier)
├── provider_name
├── provider_type (categorization)
├── payment_account_id
├── distribution_percentage
├── total_distributed (cumulative)
├── last_distribution (timestamp)
├── is_active
└── timestamps
```

**Purpose:** Configures automated payment distribution to multiple recipients.

### 2.4 System Configuration

```
TABLE: admin_setup_status
├── id (singleton constraint)
├── api_connection_states (multiple)
├── database_initialization_state
├── grid_configuration_state
├── financial_configuration_state
├── completion_metrics
└── last_updated
```

**Purpose:** Singleton table tracking system configuration progress.

---

## 3. SECURITY MODEL

### 3.1 Row-Level Security

The system implements PostgreSQL Row-Level Security (RLS) with the following policy structure:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACCESS CONTROL MATRIX                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Role          │ Own Data │ Other Members │ System Config      │
│  ─────────────────────────────────────────────────────────────  │
│  Member        │   R/W    │      -        │      -             │
│  Sovereign     │   R/W    │     R/W       │     R/W            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Policy Principles

1. **Self-Access**: Members can only access their own data
2. **Sovereign Override**: System administrators can access all data
3. **Isolation Guarantee**: No cross-member data leakage possible

---

## 4. STORED FUNCTIONS

### 4.1 Connection Status Management

```
FUNCTION: update_api_connection_status
├── INPUT: api_name, connection_state, metadata
├── PROCESS: Update configuration, recalculate completion
└── OUTPUT: Success status with updated metrics
```

### 4.2 Configuration Retrieval

```
FUNCTION: get_setup_status
├── INPUT: (authenticated user context)
├── PROCESS: Aggregate configuration states
└── OUTPUT: Complete system status object
```

### 4.3 Database Provisioning

```
FUNCTION: provision_member_database
├── INPUT: member_id, database_name, region
├── PROCESS: Create provisioning record
└── OUTPUT: Provisioning status and credentials
```

### 4.4 Distribution Management

```
FUNCTION: add_resource_relay
├── INPUT: provider_info, payment_account, percentage
├── PROCESS: Validate percentages, create relay
└── OUTPUT: Relay configuration confirmation
```

### 4.5 Resonance Calculation

```
FUNCTION: calculate_member_resonance
├── INPUT: user_id
├── PROCESS: Evaluate qualification factors
└── OUTPUT: Updated resonance score with breakdown
```

---

## 5. DATA FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA ISOLATION FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    [User Request]                                               │
│          │                                                      │
│          ▼                                                      │
│    ┌───────────┐                                               │
│    │   Auth    │ ◄─── Verify user identity                     │
│    └─────┬─────┘                                               │
│          │                                                      │
│          ▼                                                      │
│    ┌───────────┐                                               │
│    │   RLS     │ ◄─── Apply row-level policies                 │
│    └─────┬─────┘                                               │
│          │                                                      │
│          ▼                                                      │
│    ┌───────────┐                                               │
│    │  Member   │ ◄─── Access only own data                     │
│    │   Data    │                                               │
│    └───────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. PROVISIONING STATES

```
PENDING ──► PROVISIONING ──► ACTIVE
                │               │
                │               ▼
                │          SUSPENDED
                │               │
                ▼               ▼
            [Error]        ARCHIVED
```

---

## 7. KEY FEATURES

1. **Complete Isolation**: Each member's data is completely isolated through RLS
2. **Centralized Orchestration**: Sovereign can manage all members while respecting isolation
3. **Quota Management**: Resource allocation tracked per member
4. **Automated Distribution**: Payment splitting configured via relays
5. **Configuration Tracking**: Singleton table tracks system setup progress

---

**END OF EXHIBIT B**

*This document describes the database structure without revealing specific algorithms, threshold values, or configuration parameters.*
