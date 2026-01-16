# 🌐 CHE·NU Cross-Sphere Integration — CANONICAL v1.0

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              CROSS-SPHERE INTEGRATION (VERSION CANONIQUE)                    ║
║                                                                               ║
║   ✅ Toutes fonctionnalités préservées                                      ║
║   ✅ 100% conforme architecture freeze                                      ║
║   ✅ Human sovereignty garantie                                             ║
║   ✅ Production ready                                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Version:** 1.0 CANONICAL  
**Date:** 21 December 2025  
**Status:** PRODUCTION READY  
**License:** Proprietary — CHE·NU Project

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Principles](#core-principles)
4. [Package Contents](#package-contents)
5. [Installation](#installation)
6. [Quick Start](#quick-start)
7. [Complete Workflows](#complete-workflows)
8. [API Reference](#api-reference)
9. [UI Components](#ui-components)
10. [Database Schema](#database-schema)
11. [Testing](#testing)
12. [Production Deployment](#production-deployment)

---

## 🎯 OVERVIEW

Ce package implémente l'intégration cross-sphere entre **Community**, **Scholar** et **Social & Media** de manière **100% conforme** aux règles CHE·NU.

### Vision Originale (Préservée)

Chaque sphère garde son identité, MAIS peut se projeter sur Social:

- **Community groups** → Pages sociales publiques
- **Scholar publications** → Profils académiques publics
- **Research projects** → Pages sociales de recherche

### Différence Canonique

❌ **AVANT (non-conforme):**
- `auto_publish: true`
- Posts automatiques
- Création silencieuse

✅ **APRÈS (canonique):**
- `propose → HUMAN VALIDATES → publish`
- Staging area (quarantine)
- Validation per-action
- Full reversibility

---

## 🏗️ ARCHITECTURE

### Connection Type: REQUEST

Toutes les interactions cross-sphere utilisent le type **REQUEST**:

```
Community Event
    ↓ (STAGING)
Prepared Content (quarantined)
    ↓ (HUMAN VALIDATION GATE)
User Reviews & Approves
    ↓ (VERIFIED ZONE)
Published on Social Page
```

### 3-Table System

1. **`cross_sphere_requests`** — Demandes de connexion cross-sphere
2. **`staged_cross_sphere_content`** — Zone de staging (quarantine)
3. **`cross_sphere_actions`** — Audit trail complet

---

## 🔒 CORE PRINCIPLES (NON-NEGOTIABLE)

### 1. Human Sovereignty
✅ Chaque action cross-sphere = human approval  
✅ Per-action (not batch)  
✅ Explicit click required

### 2. No Silent Action
✅ Rien n'est publié automatiquement  
✅ Tout passe par staging → validation → publish  
✅ User voit preview avant publication

### 3. Reversibility
✅ Chaque action génère `undo_patch`  
✅ Undo disponible via UI  
✅ Undo logged avec user_id

### 4. Auditability
✅ Chaque action dans `cross_sphere_actions`  
✅ Logs: who, what, when, why, how  
✅ Full trail: request → staging → validation → execution

### 5. Connection Type
✅ Toujours "Request" (one of 4 allowed)  
✅ Bidirectional links logged  
✅ Clear source/target spheres

---

## 📦 PACKAGE CONTENTS

```
CROSS_SPHERE_CANONICAL/
│
├── docs/
│   ├── CROSS_SPHERE_CANONICAL_SPEC.md (50KB)
│   └── WORKFLOWS.md
│
├── backend/
│   ├── cross_sphere_canonical_models.py (15KB)
│   ├── cross_sphere_canonical_routes.py (25KB)
│   ├── community_canonical_models.py (12KB)
│   ├── scholar_canonical_models.py (13KB)
│   └── migrations/
│       └── cross_sphere_v1_canonical.py (8KB)
│
├── frontend/
│   └── CrossSphereComponents.tsx (22KB)
│
├── examples/
│   ├── community_to_social_workflow.py
│   ├── scholar_to_social_workflow.py
│   └── complete_integration_example.py
│
├── tests/
│   ├── test_cross_sphere_models.py
│   ├── test_cross_sphere_routes.py
│   └── test_workflows.py
│
└── README.md (this file)
```

**Total:** ~120KB code + 60KB documentation

---

## 🚀 INSTALLATION

### 1. Install Dependencies

```bash
# Backend
pip install fastapi sqlalchemy alembic pydantic

# Frontend
npm install lucide-react
```

### 2. Run Migration

```bash
# Apply database migration
alembic upgrade head

# Or specifically
alembic upgrade cross_sphere_v1_canonical
```

### 3. Import Modules

```python
# Backend
from backend.cross_sphere_canonical_models import (
    CrossSphereRequestDB,
    StagedCrossSphereContentDB,
    CrossSphereActionDB
)
from backend.cross_sphere_canonical_routes import router as cross_sphere_router

# Add to FastAPI app
app.include_router(cross_sphere_router)
```

```typescript
// Frontend
import {
  CreateSocialPageDialog,
  StagedContentReview,
  UndoActionButton,
  AuditTrailDisplay,
  PendingRequestsList
} from './CrossSphereComponents';
```

---

## ⚡ QUICK START

### Create Social Page for Community Group

```python
from backend.community_canonical_models import CommunityGroupCreate, ProposeSocialPageRequest
from backend.cross_sphere_canonical_routes import create_cross_sphere_request

# 1. Create community group
group = CommunityGroupCreate(
    name="Vélo MTL",
    description="Club de cyclisme à Montréal",
    type="club"
)

# 2. Propose social page (HUMAN DECISION)
propose = ProposeSocialPageRequest(
    group_id=str(group.id),
    settings={
        "page_name": "Vélo MTL",
        "page_description": "Club de cyclisme à Montréal",
        "page_category": "Sports & Recreation"
    },
    reasoning="Want to reach more cyclists in Montreal"
)

# 3. Create request (requires x-human-approval: explicit header)
request = await create_cross_sphere_request(
    request_data=propose,
    current_user=user,
    approval={"approved": True, "method": "explicit", "timestamp": "..."}
)

# 4. Request goes to validation queue
# 5. Human approves via UI
# 6. Social page created with full audit trail
```

### Share Event on Social Page

```python
from backend.community_canonical_models import ProposeEventShareRequest
from backend.cross_sphere_canonical_routes import create_staged_content

# 1. Event already exists in community group

# 2. Prepare content (STAGING)
staged = await create_staged_content(
    content_data={
        "source_sphere": "Community",
        "source_entity_id": event.group_id,
        "source_content_id": event.id,
        "target_sphere": "Social & Media",
        "target_page_id": group.social_page_id,
        "content_type": "event",
        "prepared_content": prepare_event_social_content(event)
    },
    current_user=user
)

# 3. Content in staging area (quarantined)
# Status: "quarantined"

# 4. Human reviews via UI
# Sees preview exactly as it will appear

# 5. Human clicks "Publish" (VALIDATION GATE)
# Requires: x-human-approval: explicit

# 6. Content published to social page
# Full audit trail + undo patch generated
```

### Share Scholar Publication

```python
from backend.scholar_canonical_models import ProposePublicationShareRequest

# 1. Publication exists in scholar sphere

# 2. Propose sharing (STAGING)
propose = ProposePublicationShareRequest(
    publication_id=str(publication.id),
    custom_commentary="Excited to share our latest findings! 🧠",
    tag_coauthors=[coauthor1_id, coauthor2_id],
    visibility="public"
)

# 3. Content prepared and staged
# Includes: title, abstract, DOI, authors, hashtags

# 4. Researcher reviews prepared post

# 5. Researcher approves (HUMAN VALIDATION GATE)

# 6. Published on academic social profile
# Undo available
```

---

## 📖 COMPLETE WORKFLOWS

### Workflow 1: Create Social Page for Community Group

```
┌─────────────────────────────────────────────────┐
│ 1. User creates Community group                │
│    Location: Community Sphere                   │
│    Action: Create group entity                  │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 2. System proposes (UI Dialog)                 │
│    "Create public social page?"                 │
│    Shows: Preview, settings, what will happen  │
│    User Decision: YES / NO                      │
└─────────────────────────────────────────────────┘
                    ↓ (if YES)
┌─────────────────────────────────────────────────┐
│ 3. Create Cross-Sphere Request                 │
│    POST /cross-sphere/requests                  │
│    Headers: x-human-approval: explicit          │
│    Status: PENDING                              │
│    Table: cross_sphere_requests                 │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 4. Validation Gate                              │
│    Human reviews request                        │
│    Human clicks "Approve"                       │
│    POST /cross-sphere/requests/{id}/approve     │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 5. Execute Request                              │
│    Create social_page in Social Sphere          │
│    Link: group.social_page_id = page_id         │
│    Generate undo_patch                          │
│    Log in cross_sphere_actions                  │
│    Status: EXECUTED                             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 6. Confirmation                                 │
│    "Social page created!"                       │
│    "View page →"                                │
│    "Undo ↩" (available)                        │
└─────────────────────────────────────────────────┘
```

### Workflow 2: Share Event on Social Page

```
┌─────────────────────────────────────────────────┐
│ 1. Event created in Community                  │
│    Table: community_events                      │
│    share_on_social_status: "not_proposed"       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 2. System prepares content (STAGING)           │
│    Extract event details                        │
│    Format for social post                       │
│    POST /cross-sphere/staged-content            │
│    Status: QUARANTINED                          │
│    Table: staged_cross_sphere_content           │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 3. System proposes (UI)                        │
│    "Share this event on social page?"           │
│    Shows prepared post preview                  │
│    User can edit before sharing                 │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 4. Human reviews & modifies (optional)         │
│    Sees exact preview                           │
│    Can edit title/description                   │
│    Can schedule publication                     │
│    PATCH /cross-sphere/staged-content/{id}      │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 5. Human clicks "Publish" (VALIDATION GATE)    │
│    POST /cross-sphere/staged-content/{id}/publish│
│    Headers: x-human-approval: explicit          │
│    Status: VALIDATED → PUBLISHED                │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 6. Publish to Social Sphere                    │
│    Create post in social_posts                  │
│    Generate undo_patch                          │
│    Log in cross_sphere_actions                  │
│    event.social_post_id = post_id               │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 7. Confirmation with Undo                      │
│    "Event shared!"                              │
│    "View post →"                                │
│    "Undo share ↩" (available)                  │
└─────────────────────────────────────────────────┘
```

---

## 🔌 API REFERENCE

### Cross-Sphere Requests

#### Create Request
```http
POST /api/v1/cross-sphere/requests
Headers:
  x-human-approval: explicit
  x-approval-timestamp: 2025-12-21T10:00:00Z

Body:
{
  "source_sphere": "Community",
  "source_entity_id": "group_123",
  "target_sphere": "Social & Media",
  "action_type": "create_social_page",
  "action_details": {...}
}

Response: 201 Created
{
  "id": "req_abc",
  "status": "pending",
  "requested_at": "..."
}
```

#### Approve Request
```http
POST /api/v1/cross-sphere/requests/{id}/approve
Headers:
  x-human-approval: explicit

Body:
{
  "approval_notes": "Approved for public outreach"
}

Response: 200 OK
{
  "id": "req_abc",
  "status": "executed",
  "approved_by": "user_123"
}
```

### Staged Content

#### Create Staged Content
```http
POST /api/v1/cross-sphere/staged-content

Body:
{
  "source_sphere": "Community",
  "source_content_id": "event_456",
  "target_page_id": "page_789",
  "content_type": "event",
  "prepared_content": {...}
}

Response: 201 Created
{
  "id": "staged_xyz",
  "status": "quarantined"
}
```

#### Publish Staged Content
```http
POST /api/v1/cross-sphere/staged-content/{id}/publish
Headers:
  x-human-approval: explicit

Body:
{
  "validation_notes": "Reviewed and approved"
}

Response: 200 OK
{
  "id": "staged_xyz",
  "status": "published",
  "published_post_id": "post_123"
}
```

### Audit & Undo

#### Get Actions
```http
GET /api/v1/cross-sphere/actions?source_sphere=Community&limit=50

Response: 200 OK
[
  {
    "id": "action_123",
    "action_type": "publish_content",
    "performed_by": "user_123",
    "timestamp": "...",
    "is_reversible": true
  }
]
```

#### Undo Action
```http
DELETE /api/v1/cross-sphere/actions/{id}/undo
Headers:
  x-human-approval: explicit

Body:
{
  "undo_reasoning": "Posted to wrong page by mistake"
}

Response: 200 OK
{
  "message": "Action undone successfully"
}
```

---

## 🎨 UI COMPONENTS

### CreateSocialPageDialog

```tsx
<CreateSocialPageDialog
  groupName="Vélo MTL"
  groupDescription="Club de cyclisme"
  onConfirm={async () => {
    // Create request with approval headers
  }}
  onCancel={() => setDialog(false)}
  isOpen={showDialog}
/>
```

### StagedContentReview

```tsx
<StagedContentReview
  staged={stagedContent}
  onPublish={async (notes) => {
    // Publish with approval headers
  }}
  onModify={async (newContent) => {
    // Save modifications
  }}
  onReject={async (reason) => {
    // Reject with reasoning
  }}
/>
```

### UndoActionButton

```tsx
<UndoActionButton
  action={crossSphereAction}
  onUndo={async (actionId, reasoning) => {
    // Undo with reasoning logged
  }}
/>
```

---

## 🗄️ DATABASE SCHEMA

### cross_sphere_requests

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| connection_type | String | Always "Request" |
| source_sphere | String | Source sphere name |
| target_sphere | String | Target sphere name |
| action_type | String | Action to perform |
| status | String | pending/approved/executed |
| requested_by | UUID FK | User who requested |
| approved_by | UUID FK | User who approved |
| undo_patch | JSONB | Reversibility data |

### staged_cross_sphere_content

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| status | String | quarantined/validated/published |
| source_content_id | String | Original content ID |
| prepared_content | JSONB | Prepared post data |
| validated_by | UUID FK | User who validated |
| published_post_id | String | ID in target sphere |
| undo_patch | JSONB | Reversibility data |

### cross_sphere_actions

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| performed_by | UUID FK | User who performed |
| action_type | String | Type of action |
| timestamp | DateTime | When performed |
| is_reversible | Boolean | Can be undone |
| undo_performed | Boolean | Already undone |
| undo_patch | JSONB | Undo instructions |

---

## ✅ PRODUCTION DEPLOYMENT

### Pre-Deployment Checklist

- [ ] Database migration applied
- [ ] API routes registered
- [ ] UI components integrated
- [ ] Human approval headers implemented
- [ ] Undo functionality tested
- [ ] Audit logs verified
- [ ] Permission checks in place

### Environment Variables

```bash
# Required
DATABASE_URL=postgresql://...
CHENU_CROSS_SPHERE_ENABLED=true

# Optional
CHENU_UNDO_WINDOW_DAYS=30
CHENU_AUDIT_RETENTION_DAYS=365
```

### Monitoring

Monitor these metrics:
- Cross-sphere requests created
- Approval rate (approved / total)
- Average time to approval
- Undo rate
- Audit trail completeness

---

## 📄 LICENSE

Proprietary — CHE·NU Project  
All rights reserved.

---

## 🤝 SUPPORT

For questions or issues:
- Email: support@chenu.ai
- Documentation: https://docs.chenu.ai/cross-sphere

---

**Created:** 21 December 2025  
**Version:** 1.0 CANONICAL  
**Status:** PRODUCTION READY ✅
