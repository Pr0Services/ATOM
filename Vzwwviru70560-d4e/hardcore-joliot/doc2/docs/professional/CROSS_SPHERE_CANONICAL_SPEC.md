# 🌐 CROSS-SPHERE CANONICAL — COMMUNITY + SCHOLAR → SOCIAL

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         CROSS-SPHERE INTEGRATION (VERSION CANONIQUE)         ║
║                                                               ║
║   ✅ Toutes fonctionnalités préservées                      ║
║   ✅ 100% conforme architecture freeze                      ║
║   ✅ Human sovereignty garantie                             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Version:** 1.0 CANONICAL  
**Date:** 21 December 2025  
**Status:** OFFICIAL — NON-NEGOTIABLE  
**Sphères:** Community (5), Scholar (9), Social & Media (6)

---

## 🎯 VISION JO (PRÉSERVÉE)

### Concept Original

**Chaque sphère garde son identité, MAIS peut se projeter sur Social:**

```
SPHÈRE COMMUNITY (5)
├── Groupe interne privé
├── Collaboration membres
├── Projets communautaires
└── 📱 PAGE SOCIALE PUBLIQUE (via Request)
    ├── Visible par tous
    ├── Posts publics VALIDÉS
    ├── Événements publics APPROUVÉS
    └── Recrutement nouveaux membres

SPHÈRE SCHOLAR (9)
├── Recherches privées
├── Notes académiques
├── Collaboration chercheurs
└── 📱 PROFIL ACADÉMIQUE PUBLIC (via Request)
    ├── Publications scientifiques PARTAGÉES
    ├── Projets de recherche VALIDÉS
    ├── CV académique
    └── Networking chercheurs
```

**DIFFÉRENCE CANONIQUE:**
- ❌ PAS "auto-publish"
- ✅ "PROPOSE → HUMAN VALIDATES → PUBLISH"

---

## 🔒 PRINCIPES CANONIQUES (NON-NÉGOCIABLES)

### 1. Connection Type: REQUEST

**Toute interaction cross-sphere = REQUEST:**

```python
ConnectionType = "Request"  # One of 4 allowed types
# Request = Action requiring human approval per-action
```

**Caractéristiques:**
- ✅ Human approval REQUIRED
- ✅ Per-action (not batch)
- ✅ Logged with user_id
- ✅ Reversible with undo_patch

### 2. Staging Area (Quarantine)

**Aucun contenu n'est publié directement:**

```
Community Event created
    ↓
STAGING AREA (quarantined)
    ↓
Human reviews
    ↓
Human approves (explicit click)
    ↓
VERIFIED ZONE (published)
```

### 3. Human Validation Gate

**Chaque action cross-sphere:**

```python
requires_human_validation: bool = True  # ALWAYS
validation_method: str = "explicit_click"
validated_by: str  # user_id (MANDATORY)
validated_at: datetime  # MANDATORY
```

### 4. Reversibility

**Toute action peut être annulée:**

```python
is_reversible: bool = True
undo_patch: Dict  # Generated automatically
undo_available_until: datetime  # Configurable period
```

### 5. Audit Trail Complet

**Chaque action loggée:**

```python
performed_by: str  # user_id
timestamp: datetime
action_type: str
source_sphere: str
target_sphere: str
reasoning: Optional[str]  # User can add note
```

---

## 🏗️ ARCHITECTURE TECHNIQUE

### 1. CORE MODELS

#### A) CrossSphereRequest (Human-Gated)

```python
from enum import Enum
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field

class Sphere(str, Enum):
    """9 frozen spheres"""
    PERSONAL = "Personal"
    BUSINESS = "Business"
    GOVERNMENT = "Government & Institutions"
    CREATIVE_STUDIO = "Creative Studio"
    COMMUNITY = "Community"
    SOCIAL_MEDIA = "Social & Media"
    ENTERTAINMENT = "Entertainment"
    MY_TEAM = "My Team"
    SCHOLAR = "Scholar"


class ConnectionType(str, Enum):
    """4 allowed connection types"""
    PROJECTION = "Projection"
    REQUEST = "Request"
    REFERENCE = "Reference"
    DELEGATION = "Delegation"


class RequestStatus(str, Enum):
    """Request lifecycle"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    UNDONE = "undone"


class CrossSphereRequest(BaseModel):
    """
    REQUEST connection type for cross-sphere interactions.
    
    CANONICAL RULE: Every cross-sphere action is a REQUEST.
    No auto-execution. Human approval required per-action.
    """
    id: str
    
    # CONNECTION TYPE (always Request for cross-sphere)
    connection_type: ConnectionType = ConnectionType.REQUEST
    
    # SOURCE & TARGET
    source_sphere: Sphere
    source_entity_id: str
    source_entity_type: str  # "community_group", "scholar_project", etc.
    
    target_sphere: Sphere
    target_entity_id: Optional[str] = None  # Created after approval
    target_entity_type: str  # "social_page", "social_profile", etc.
    
    # REQUEST DETAILS
    action_type: str  # "create_social_page", "share_event", "publish_research"
    action_details: Dict  # Specific to action type
    
    # HUMAN VALIDATION GATE (MANDATORY)
    status: RequestStatus = RequestStatus.PENDING
    requires_human_validation: bool = True
    
    requested_by: str  # user_id who initiated
    requested_at: datetime = Field(default_factory=datetime.now)
    
    reviewed_by: Optional[str] = None  # user_id who reviewed
    reviewed_at: Optional[datetime] = None
    
    approved_by: Optional[str] = None  # user_id who approved
    approved_at: Optional[datetime] = None
    
    # REASONING
    request_reasoning: Optional[str] = None  # Why user wants this
    rejection_reasoning: Optional[str] = None  # Why rejected
    
    # REVERSIBILITY
    is_reversible: bool = True
    undo_patch: Optional[Dict] = None  # Generated on execution
    undone_by: Optional[str] = None
    undone_at: Optional[datetime] = None
    
    # AUDIT
    audit_trail: List[Dict] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "req_abc123",
                "connection_type": "Request",
                "source_sphere": "Community",
                "source_entity_id": "group_xyz",
                "source_entity_type": "community_group",
                "target_sphere": "Social & Media",
                "target_entity_type": "social_page",
                "action_type": "create_social_page",
                "action_details": {
                    "page_name": "Vélo MTL",
                    "page_description": "Club de cyclisme à Montréal"
                },
                "status": "pending",
                "requested_by": "user_123",
                "requested_at": "2025-12-21T10:00:00Z"
            }
        }
```

#### B) StagedCrossSphereContent (Quarantine)

```python
class ContentStatus(str, Enum):
    """Content lifecycle in staging"""
    QUARANTINED = "quarantined"  # Just prepared
    READY_FOR_REVIEW = "ready_for_review"
    VALIDATED = "validated"  # Human approved
    PUBLISHED = "published"  # Applied to target
    REJECTED = "rejected"
    UNDONE = "undone"


class StagedCrossSphereContent(BaseModel):
    """
    Staging area for cross-sphere content.
    
    CANONICAL RULE: Nothing published directly.
    All content goes through staging → validation → publish.
    """
    id: str
    
    # STATUS
    status: ContentStatus = ContentStatus.QUARANTINED
    
    # SOURCE
    source_sphere: Sphere
    source_entity_id: str
    source_entity_type: str
    source_content_id: str  # ID of event/publication/etc in source
    
    # TARGET
    target_sphere: Sphere
    target_page_id: str  # Social page/profile to post on
    
    # PREPARED CONTENT (not yet published)
    content_type: str  # "post", "event", "publication"
    prepared_content: Dict  # Title, body, media, etc.
    preview_url: Optional[str] = None  # Preview for human review
    
    # HUMAN VALIDATION GATE
    requires_validation: bool = True
    
    prepared_by: str  # user_id or "system"
    prepared_at: datetime = Field(default_factory=datetime.now)
    
    validated_by: Optional[str] = None
    validated_at: Optional[datetime] = None
    validation_decision: Optional[str] = None  # approve, reject, modify
    validation_notes: Optional[str] = None
    
    # PUBLISHING
    published: bool = False
    published_by: Optional[str] = None
    published_at: Optional[datetime] = None
    published_post_id: Optional[str] = None  # ID in target sphere
    
    # REVERSIBILITY
    is_reversible: bool = True
    undo_patch: Optional[Dict] = None
    
    # MODIFICATIONS
    modification_history: List[Dict] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "staged_xyz",
                "status": "quarantined",
                "source_sphere": "Community",
                "source_entity_id": "group_123",
                "source_content_id": "event_456",
                "target_sphere": "Social & Media",
                "target_page_id": "page_789",
                "content_type": "event",
                "prepared_content": {
                    "title": "Sortie vélo dimanche",
                    "description": "Rendez-vous 10h au Mont-Royal",
                    "date": "2025-12-28T10:00:00Z",
                    "image_url": "https://..."
                },
                "prepared_by": "user_123",
                "requires_validation": True
            }
        }
```

#### C) CrossSphereAction (Audit Trail)

```python
class CrossSphereAction(BaseModel):
    """
    Complete audit trail for every cross-sphere action.
    
    CANONICAL RULE: Every action logged with who/what/when/why/how.
    """
    id: str
    
    # WHO
    performed_by: str  # user_id (MANDATORY)
    on_behalf_of: Optional[str] = None  # If delegated
    
    # WHAT
    action_type: str  # create_page, share_event, publish_research, undo
    source_sphere: Sphere
    source_entity_id: str
    target_sphere: Sphere
    target_entity_id: Optional[str]
    
    # WHEN
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # WHY
    reasoning: Optional[str] = None  # User explanation
    
    # HOW
    method: str  # "explicit_click", "api_call_with_header"
    request_id: Optional[str] = None  # Link to CrossSphereRequest
    staged_content_id: Optional[str] = None  # Link to StagedContent
    
    # VALIDATION
    required_validation: bool
    validated_by: Optional[str] = None
    validated_at: Optional[datetime] = None
    validation_decision: str  # approve, reject
    
    # REVERSIBILITY
    is_reversible: bool
    undo_patch: Optional[Dict] = None
    undo_performed: bool = False
    undo_by: Optional[str] = None
    undo_at: Optional[datetime] = None
    undo_reasoning: Optional[str] = None
    
    # METADATA
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
```

---

### 2. COMMUNITY → SOCIAL PAGES (CANONICAL)

#### A) Community Group Model

```python
class CommunityGroupType(str, Enum):
    """Types of community groups"""
    CLUB = "club"  # Sports, hobbies
    ORGANIZATION = "organization"  # Local organizations
    INTEREST_GROUP = "interest_group"  # Shared interests
    PROJECT = "project"  # Collaborative projects
    NGO = "ngo"  # Non-profits


class SocialPageSettings(BaseModel):
    """Settings for social page (if created)"""
    page_name: str
    page_description: str
    page_category: str
    page_visibility: str = "public"
    
    # CANONICAL: No auto-publishing
    propose_event_sharing: bool = True  # Propose, not auto
    propose_achievement_sharing: bool = True
    propose_update_sharing: bool = False
    
    # PUBLISHING RULES
    who_can_propose_posts: str = "admins_only"  # admins_only, all_members
    all_posts_require_approval: bool = True  # MANDATORY
    
    # FEATURES
    allow_public_comments: bool = True
    allow_public_messages: bool = True
    show_member_count: bool = True
    show_events: bool = True


class CommunityGroup(BaseModel):
    """
    Group in Community Sphere.
    
    CAN have social page, but creation requires human approval.
    """
    id: str
    name: str
    description: str
    type: CommunityGroupType
    
    # MEMBERS
    creator_id: str
    admins: List[str]
    members: List[str]
    member_count: int
    
    # PRIVACY
    is_private: bool = False
    requires_approval_to_join: bool = True
    
    # SOCIAL MEDIA PRESENCE (CANONICAL)
    has_social_page: bool = False
    social_page_id: Optional[str] = None
    social_page_request_id: Optional[str] = None  # Link to Request
    social_page_settings: Optional[SocialPageSettings] = None
    
    # CANONICAL: Propose, not auto
    social_page_creation_proposed: bool = False
    social_page_creation_approved_by: Optional[str] = None
    social_page_creation_approved_at: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

#### B) Community Event Model

```python
class CommunityEvent(BaseModel):
    """
    Event in Community Sphere.
    
    CAN be shared on social page, but requires per-event approval.
    """
    id: str
    group_id: str
    
    # EVENT DETAILS
    name: str
    description: str
    event_date: datetime
    location: Optional[str]
    is_online: bool = False
    max_participants: Optional[int] = None
    
    # ORGANIZER
    created_by: str
    organizers: List[str]
    
    # VISIBILITY
    is_public: bool = False
    visible_to_non_members: bool = False
    
    # CROSS-SPHERE SHARING (CANONICAL - per event)
    share_on_social_proposed: bool = False
    share_on_social_status: str = "not_proposed"
    # States: not_proposed, staged, pending_validation, approved, rejected, published
    
    staged_content_id: Optional[str] = None  # Link to StagedContent
    share_request_id: Optional[str] = None  # Link to CrossSphereRequest
    
    share_approved_by: Optional[str] = None
    share_approved_at: Optional[datetime] = None
    
    social_post_id: Optional[str] = None  # If published
    social_post_undo_patch: Optional[Dict] = None
    
    created_at: datetime = Field(default_factory=datetime.now)
```

---

### 3. SCHOLAR → SOCIAL PROFILES (CANONICAL)

#### A) Scholar Profile Model

```python
class ScholarProfile(BaseModel):
    """
    Academic profile (can project on Social).
    
    Publications/projects can be shared, but require approval.
    """
    id: str
    user_id: str
    
    # IDENTITY
    academic_name: str
    title: str  # "PhD Student", "Professor", "Researcher"
    institution: str
    department: str
    
    # RESEARCH
    research_interests: List[str]
    h_index: Optional[int] = None
    total_citations: int = 0
    
    # SOCIAL ACADEMIC PRESENCE (CANONICAL)
    has_public_social_profile: bool = False
    social_profile_id: Optional[str] = None
    social_profile_request_id: Optional[str] = None
    
    # CANONICAL: Propose sharing, not auto
    propose_publication_sharing: bool = True
    propose_project_sharing: bool = True
    propose_achievement_sharing: bool = True
    
    # All shares require per-action approval
    all_shares_require_approval: bool = True  # MANDATORY
    
    created_at: datetime = Field(default_factory=datetime.now)


class Publication(BaseModel):
    """
    Scientific publication in Scholar Sphere.
    
    CAN be shared on social profile, requires approval per publication.
    """
    id: str
    scholar_profile_id: str
    
    # PUBLICATION DETAILS
    title: str
    authors: List[str]
    journal: str
    publication_date: datetime
    doi: Optional[str] = None
    abstract: str
    pdf_url: Optional[str] = None
    citations: int = 0
    
    # CROSS-SPHERE SHARING (CANONICAL - per publication)
    share_on_social_proposed: bool = False
    share_on_social_status: str = "not_proposed"
    
    staged_content_id: Optional[str] = None
    share_request_id: Optional[str] = None
    
    share_approved_by: Optional[str] = None
    share_approved_at: Optional[datetime] = None
    
    social_post_id: Optional[str] = None
    social_post_undo_patch: Optional[Dict] = None
    
    created_at: datetime = Field(default_factory=datetime.now)


class ResearchProject(BaseModel):
    """
    Research project in Scholar Sphere.
    
    CAN have social page, requires approval.
    """
    id: str
    name: str
    description: str
    field: str
    status: str  # ongoing, completed, published
    
    lead_researchers: List[str]
    collaborators: List[str]
    funding: Optional[str] = None
    
    # PUBLIC PRESENCE (CANONICAL)
    has_social_page: bool = False
    social_page_id: Optional[str] = None
    social_page_request_id: Optional[str] = None
    
    allow_public_updates: bool = False
    public_updates_require_approval: bool = True  # MANDATORY
    
    created_at: datetime = Field(default_factory=datetime.now)
```

---

## 📋 WORKFLOWS CANONIQUES

### WORKFLOW 1: Create Social Page for Community Group

```
┌────────────────────────────────────────────────────────────┐
│ 1. USER CREATES COMMUNITY GROUP                           │
│    - In Community Sphere                                   │
│    - Group stored in community_groups table                │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 2. SYSTEM PROPOSES (UI Dialog)                            │
│    "Create public social page for this group?"            │
│    - Shows preview of page                                 │
│    - Shows settings                                        │
│    - Explains what will be shared                          │
│    - Shows undo option                                     │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 3. USER REVIEWS & DECIDES                                  │
│    Option A: Click "Create Page" (explicit)               │
│    Option B: Click "No Thanks"                             │
└────────────────────────────────────────────────────────────┘
                          ↓ (if Option A)
┌────────────────────────────────────────────────────────────┐
│ 4. CREATE CROSS-SPHERE REQUEST                            │
│    POST /api/cross-sphere/requests                        │
│    {                                                       │
│      connection_type: "Request",                           │
│      source_sphere: "Community",                           │
│      target_sphere: "Social & Media",                      │
│      action_type: "create_social_page",                    │
│      requested_by: user_id                                 │
│    }                                                       │
│    → Stored in cross_sphere_requests (PENDING)            │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 5. VALIDATION GATE (can be immediate or delayed)          │
│    - For own groups: often immediate                       │
│    - For organizational: may require admin review          │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 6. EXECUTE REQUEST                                         │
│    - Create social_page in Social Sphere                  │
│    - Link bidirectionally (with audit)                     │
│    - Generate undo_patch                                   │
│    - Log action in cross_sphere_actions                   │
│    - Update request status: EXECUTED                       │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 7. CONFIRMATION                                            │
│    "Social page created! View page →"                     │
│    "Undo this action ↩"                                   │
└────────────────────────────────────────────────────────────┘
```

---

### WORKFLOW 2: Share Community Event on Social Page

```
┌────────────────────────────────────────────────────────────┐
│ 1. USER CREATES EVENT IN COMMUNITY GROUP                  │
│    - Event stored in community_events table                │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 2. SYSTEM PREPARES CONTENT (Staging)                      │
│    - Extract event details                                 │
│    - Format for social post                                │
│    - Create StagedCrossSphereContent                       │
│    - Status: QUARANTINED                                   │
│    → staged_cross_sphere_content table                    │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 3. SYSTEM PROPOSES (UI)                                    │
│    "Share this event on social page?"                      │
│    - Shows prepared post preview                           │
│    - Shows target page                                     │
│    - Option to edit before sharing                         │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 4. USER REVIEWS PREPARED CONTENT                           │
│    - Sees preview exactly as it will appear                │
│    - Can edit title/description                            │
│    - Can add/remove images                                 │
│    - Can schedule publication                              │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 5. USER CLICKS "SHARE" (Explicit Action)                  │
│    POST /api/cross-sphere/staged-content/{id}/publish     │
│    Headers: {                                              │
│      x-user-id: "user_123",                                │
│      x-user-approval: "explicit"                           │
│    }                                                       │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 6. VALIDATION GATE                                         │
│    - Verify user has permission                            │
│    - Log validation (user_id, timestamp)                   │
│    - Update staged content: VALIDATED                      │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 7. PUBLISH TO SOCIAL SPHERE                                │
│    - Create post in social_posts table                    │
│    - Generate undo_patch (contains post_id, original data) │
│    - Log in cross_sphere_actions                          │
│    - Update staged content: PUBLISHED                      │
│    - Link event → social_post                              │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 8. CONFIRMATION WITH UNDO                                  │
│    "Event shared! View post →"                            │
│    "Undo share ↩" (deletes post, logs undo)              │
└────────────────────────────────────────────────────────────┘
```

---

### WORKFLOW 3: Share Scholar Publication on Social Profile

```
┌────────────────────────────────────────────────────────────┐
│ 1. RESEARCHER ADDS PUBLICATION IN SCHOLAR SPHERE          │
│    - Publication stored in scholar_publications            │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 2. SYSTEM PREPARES ACADEMIC POST                          │
│    - Extract: title, abstract, authors, DOI               │
│    - Format for social                                     │
│    - Add relevant hashtags (#neuroscience #research)       │
│    - Create StagedCrossSphereContent                       │
│    - Status: QUARANTINED                                   │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 3. SYSTEM PROPOSES                                         │
│    "Share this publication on your academic profile?"      │
│    - Preview of social post                                │
│    - Option to tag co-authors                              │
│    - Option to add context/commentary                      │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 4. RESEARCHER REVIEWS & CUSTOMIZES                         │
│    - Reviews prepared post                                 │
│    - Adds personal note (optional)                         │
│    - Tags co-authors (with their approval)                 │
│    - Selects visibility (public/followers)                 │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 5. RESEARCHER CLICKS "SHARE PUBLICATION"                   │
│    - Explicit per-publication approval                     │
│    - Logged with user_id + timestamp                       │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 6. VALIDATION & PUBLISH                                    │
│    - Validate researcher permission                        │
│    - Create social post                                    │
│    - Generate undo_patch                                   │
│    - Log action                                            │
└────────────────────────────────────────────────────────────┘
                          ↓
┌────────────────────────────────────────────────────────────┐
│ 7. CONFIRMATION                                            │
│    "Publication shared! View post →"                      │
│    "Undo ↩"                                               │
└────────────────────────────────────────────────────────────┘
```

---

## 🔐 GARANTIES CANONIQUES

### ✅ Ce qui est GARANTI

1. **Human Sovereignty**
   - ✅ Chaque action cross-sphere = human approval
   - ✅ Per-action (not batch)
   - ✅ Explicit click required

2. **No Silent Action**
   - ✅ Rien n'est publié automatiquement
   - ✅ Tout passe par staging → validation → publish
   - ✅ User voit preview avant publication

3. **Reversibility**
   - ✅ Chaque action génère undo_patch
   - ✅ Undo disponible via UI
   - ✅ Undo logged avec user_id

4. **Auditability**
   - ✅ Chaque action dans cross_sphere_actions
   - ✅ Logs: who, what, when, why, how
   - ✅ Full trail: request → staging → validation → execution

5. **Connection Type**
   - ✅ Toujours "Request" (one of 4 allowed)
   - ✅ Bidirectional links logged
   - ✅ Clear source/target spheres

---

## 🎯 EXEMPLES CONCRETS

### Exemple 1: Club Vélo MTL

```
COMMUNITY SPHERE (privé):
├── Groupe: "Vélo MTL"
├── Type: Club sportif
├── Membres: 45
├── Événements, discussions internes
└── [Propose social page] ← USER CLICKS

    ↓ Human approves

SOCIAL PAGE (public):
├── @VeloMTL
├── Page créée avec human approval
├── Followers: 890
└── Chaque event proposé:
    ├── "Sortie dimanche?" ← STAGED
    ├── Admin reviews ← VALIDATES
    ├── Admin clicks "Share" ← PUBLISHES
    └── Post visible ← CAN UNDO
```

### Exemple 2: Dr. Marie Tremblay

```
SCHOLAR SPHERE (privé):
├── Publications
├── Projets de recherche
└── [New publication added]

    ↓ System prepares post (quarantined)

UI PROPOSES:
├── "Share on academic profile?"
├── Preview shown
└── [Marie reviews & clicks "Share"]

    ↓ Validation gate (logged)

SOCIAL PROFILE (public):
├── @DrMarieTremblay
├── Post: "New paper published! 🧠"
├── DOI link, abstract, co-authors
└── [Undo button available]
```

---

## 📊 COMPARAISON AVANT/APRÈS

| Feature | AVANT (non-conforme) | APRÈS (canonique) |
|---------|---------------------|-------------------|
| Create social page | `auto: true` | Propose → Human clicks → Creates |
| Share event | Auto if `auto_share: true` | Prepare → Review → Approve → Publish |
| Share publication | Auto-post | Prepare → Customize → Approve → Share |
| Validation | Optional/batch | Mandatory per-action |
| Reversibility | ❌ Missing | ✅ Every action |
| Audit | ❌ Incomplete | ✅ Complete trail |
| Connection type | ❌ Undefined | ✅ Request |

---

## ✅ STATUS: 100% CONFORME

**Toutes fonctionnalités préservées:**
- ✅ Community groups can have social pages
- ✅ Events can be shared publicly
- ✅ Scholar publications can be shared
- ✅ Academic profiles visible
- ✅ Public discovery enabled

**Toutes règles respectées:**
- ✅ Human sovereignty (every action)
- ✅ No silent action (staging + approval)
- ✅ Reversibility (undo patches)
- ✅ Auditability (complete logs)
- ✅ Connection type (Request)
- ✅ Separation cognition/execution

**Prêt pour intégration!** 🚀

---

**Version:** 1.0 CANONICAL  
**Date:** 21 December 2025  
**Status:** PRODUCTION READY
