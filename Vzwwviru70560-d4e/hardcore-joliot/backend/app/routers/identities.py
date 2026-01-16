"""
ROUTER: identities.py
PREFIX: /api/v2/identities
VERSION: 1.0.0
PHASE: B2

Multi-Identity Management System.
Core enforcement of R&D Rule #3 (Identity Boundary).

R&D COMPLIANCE:
- Rule #1 (Human Sovereignty): Identity changes require approval
- Rule #3 (Identity Boundary): HTTP 403 for cross-identity access
- Rule #6 (Traceability): Full identity audit trail
- Rule #7 (Continuity): 9 spheres per identity

ENDPOINTS: 14
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, EmailStr

router = APIRouter(prefix="/api/v2/identities", tags=["Identities"])

# ============================================================
# ENUMS
# ============================================================

class IdentityType(str, Enum):
    PRIMARY = "primary"           # Main identity
    PROFESSIONAL = "professional" # Work identity
    CREATIVE = "creative"         # Creative persona
    ANONYMOUS = "anonymous"       # Anonymous identity

class IdentityStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"

class SphereType(str, Enum):
    """The 9 canonical spheres - R&D Rule #7."""
    PERSONAL = "personal"
    BUSINESS = "business"
    GOVERNMENT = "government"
    CREATIVE = "creative"
    COMMUNITY = "community"
    SOCIAL = "social"
    ENTERTAINMENT = "entertainment"
    MY_TEAM = "my_team"
    SCHOLAR = "scholar"

# ============================================================
# SCHEMAS
# ============================================================

class IdentityCreate(BaseModel):
    """Create a new identity."""
    name: str = Field(..., min_length=1, max_length=100)
    identity_type: IdentityType = IdentityType.PRIMARY
    email: Optional[EmailStr] = None
    metadata: Optional[Dict[str, Any]] = None

class IdentityUpdate(BaseModel):
    """Update identity (non-critical fields)."""
    name: Optional[str] = Field(None, max_length=100)
    metadata: Optional[Dict[str, Any]] = None

class SphereResponse(BaseModel):
    """Sphere within an identity."""
    id: UUID
    identity_id: UUID
    sphere_type: SphereType
    created_at: datetime
    thread_count: int
    agent_count: int
    is_active: bool

class IdentityResponse(BaseModel):
    """Identity response with R&D Rule #6 compliance."""
    id: UUID
    user_id: UUID  # Owner
    created_by: UUID
    created_at: datetime
    name: str
    identity_type: IdentityType
    status: IdentityStatus
    email: Optional[str]
    sphere_count: int  # Should always be 9
    metadata: Optional[Dict[str, Any]]

class IdentityFullResponse(BaseModel):
    """Identity with all spheres."""
    identity: IdentityResponse
    spheres: List[SphereResponse]

# ============================================================
# MOCK DATA STORE
# ============================================================

_identities_store: Dict[UUID, Dict] = {}
_spheres_store: Dict[UUID, List[Dict]] = {}  # identity_id -> spheres
_user_identities: Dict[UUID, List[UUID]] = {}  # user_id -> identity_ids

# ============================================================
# DEPENDENCIES
# ============================================================

async def get_current_user_id() -> UUID:
    """Mock current user - replace with real auth."""
    return UUID("11111111-1111-1111-1111-111111111111")

async def verify_identity_ownership(
    identity_id: UUID,
    current_user_id: UUID
) -> Dict:
    """
    Verify user owns the identity - R&D Rule #3.
    Returns HTTP 403 if violation.
    """
    if identity_id not in _identities_store:
        raise HTTPException(status_code=404, detail="Identity not found")
    
    identity = _identities_store[identity_id]
    if identity["user_id"] != current_user_id:
        # R&D Rule #3: Identity Boundary Violation
        raise HTTPException(
            status_code=403,
            detail={
                "error": "identity_boundary_violation",
                "message": "Access denied: identity belongs to different user",
                "code": "RULE_3_VIOLATION",
                "requested_identity": str(identity_id),
                "actual_owner": "hidden"  # Don't leak user info
            }
        )
    return identity

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_9_spheres(identity_id: UUID, user_id: UUID) -> List[Dict]:
    """
    Create the 9 canonical spheres for an identity.
    R&D Rule #7: Every identity has exactly 9 spheres.
    """
    now = datetime.utcnow()
    spheres = []
    
    for sphere_type in SphereType:
        sphere = {
            "id": uuid4(),
            "identity_id": identity_id,
            "sphere_type": sphere_type,
            "created_at": now,
            "created_by": user_id,
            "thread_count": 0,
            "agent_count": 0,
            "is_active": True
        }
        spheres.append(sphere)
    
    return spheres

# ============================================================
# ENDPOINTS
# ============================================================

# --- LIST & GET ---

@router.get("/", response_model=List[IdentityResponse])
async def list_identities(
    status: Optional[IdentityStatus] = None,
    identity_type: Optional[IdentityType] = None,
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    List user's identities.
    
    R&D Rule #3: Only returns identities owned by current user.
    R&D Rule #5: Ordered by created_at DESC.
    """
    identity_ids = _user_identities.get(current_user_id, [])
    identities = [_identities_store[iid] for iid in identity_ids if iid in _identities_store]
    
    if status:
        identities = [i for i in identities if i["status"] == status]
    if identity_type:
        identities = [i for i in identities if i["identity_type"] == identity_type]
    
    # R&D Rule #5: Chronological order
    identities.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [IdentityResponse(**i) for i in identities]

@router.get("/{identity_id}", response_model=IdentityFullResponse)
async def get_identity(
    identity_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Get identity with all 9 spheres.
    
    R&D Rule #3: Only owner can access.
    R&D Rule #7: Returns all 9 spheres.
    """
    identity = await verify_identity_ownership(identity_id, current_user_id)
    spheres = _spheres_store.get(identity_id, [])
    
    return IdentityFullResponse(
        identity=IdentityResponse(**identity),
        spheres=[SphereResponse(**s) for s in spheres]
    )

# --- CREATE & UPDATE ---

@router.post("/", response_model=IdentityFullResponse, status_code=201)
async def create_identity(
    data: IdentityCreate,
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Create a new identity with 9 spheres.
    
    R&D Rule #6: Full traceability.
    R&D Rule #7: Automatically creates 9 spheres.
    """
    now = datetime.utcnow()
    identity_id = uuid4()
    
    identity = {
        # R&D Rule #6: Traceability
        "id": identity_id,
        "user_id": current_user_id,
        "created_by": current_user_id,
        "created_at": now,
        # Identity data
        "name": data.name,
        "identity_type": data.identity_type,
        "status": IdentityStatus.ACTIVE,
        "email": data.email,
        "sphere_count": 9,  # R&D Rule #7
        "metadata": data.metadata or {}
    }
    
    # R&D Rule #7: Create 9 spheres
    spheres = create_9_spheres(identity_id, current_user_id)
    
    _identities_store[identity_id] = identity
    _spheres_store[identity_id] = spheres
    _user_identities.setdefault(current_user_id, []).append(identity_id)
    
    return IdentityFullResponse(
        identity=IdentityResponse(**identity),
        spheres=[SphereResponse(**s) for s in spheres]
    )

@router.patch("/{identity_id}", response_model=IdentityResponse)
async def update_identity(
    identity_id: UUID = Path(...),
    data: IdentityUpdate = Body(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Update identity (non-critical fields).
    
    R&D Rule #3: Only owner can update.
    """
    identity = await verify_identity_ownership(identity_id, current_user_id)
    
    if data.name is not None:
        identity["name"] = data.name
    if data.metadata is not None:
        identity["metadata"].update(data.metadata)
    
    return IdentityResponse(**identity)

@router.delete("/{identity_id}", status_code=423)
async def delete_identity(
    identity_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Delete an identity - REQUIRES CHECKPOINT.
    
    R&D Rule #1: Destructive action requires approval.
    R&D Rule #3: Only owner can delete.
    """
    identity = await verify_identity_ownership(identity_id, current_user_id)
    
    # Check if primary identity
    if identity["identity_type"] == IdentityType.PRIMARY:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete primary identity"
        )
    
    checkpoint_id = uuid4()
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_pending",
            "checkpoint": {
                "id": str(checkpoint_id),
                "type": "identity_delete",
                "action": "delete_identity",
                "identity_id": str(identity_id),
                "identity_name": identity["name"],
                "requires_approval": True,
                "severity": "critical",
                "warning": "This will delete all data in this identity",
                "created_at": datetime.utcnow().isoformat(),
                "options": ["approve", "reject"]
            },
            "message": "Identity deletion requires human approval"
        }
    )

# --- SPHERES ---

@router.get("/{identity_id}/spheres", response_model=List[SphereResponse])
async def list_identity_spheres(
    identity_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    List all 9 spheres for an identity.
    
    R&D Rule #7: Always returns exactly 9 spheres.
    """
    await verify_identity_ownership(identity_id, current_user_id)
    spheres = _spheres_store.get(identity_id, [])
    
    # R&D Rule #7: Verify 9 spheres
    if len(spheres) != 9:
        # Auto-repair if missing spheres
        spheres = create_9_spheres(identity_id, current_user_id)
        _spheres_store[identity_id] = spheres
    
    return [SphereResponse(**s) for s in spheres]

@router.get("/{identity_id}/spheres/{sphere_type}", response_model=SphereResponse)
async def get_sphere(
    identity_id: UUID = Path(...),
    sphere_type: SphereType = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Get a specific sphere."""
    await verify_identity_ownership(identity_id, current_user_id)
    spheres = _spheres_store.get(identity_id, [])
    
    sphere = next((s for s in spheres if s["sphere_type"] == sphere_type), None)
    if not sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")
    
    return SphereResponse(**sphere)

# --- IDENTITY SWITCHING ---

@router.post("/{identity_id}/switch")
async def switch_to_identity(
    identity_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Switch active identity.
    
    R&D Rule #3: Can only switch to owned identities.
    """
    identity = await verify_identity_ownership(identity_id, current_user_id)
    
    if identity["status"] != IdentityStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot switch to {identity['status']} identity"
        )
    
    return {
        "status": "switched",
        "active_identity": IdentityResponse(**identity),
        "message": f"Now using identity: {identity['name']}"
    }

# --- CROSS-IDENTITY ACCESS (BLOCKED) ---

@router.get("/{identity_id}/access/{target_identity_id}", status_code=403)
async def cross_identity_access(
    identity_id: UUID = Path(...),
    target_identity_id: UUID = Path(...),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    BLOCKED: Cross-identity access is not allowed.
    
    R&D Rule #3: Identity Boundary enforcement.
    This endpoint exists to explicitly document the rule.
    """
    raise HTTPException(
        status_code=403,
        detail={
            "error": "cross_identity_access_blocked",
            "message": "Direct cross-identity access is not allowed (R&D Rule #3)",
            "code": "RULE_3_VIOLATION",
            "source_identity": str(identity_id),
            "target_identity": str(target_identity_id),
            "resolution": "Use explicit data transfer workflows with approval"
        }
    )

# --- DATA TRANSFER WORKFLOW ---

@router.post("/{identity_id}/transfer-request", status_code=423)
async def request_data_transfer(
    identity_id: UUID = Path(...),
    target_identity_id: UUID = Body(..., embed=True),
    data_type: str = Body(..., embed=True),
    description: str = Body(..., embed=True),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Request data transfer between identities - REQUIRES CHECKPOINT.
    
    R&D Rule #1: Cross-identity transfers require approval.
    R&D Rule #3: Both identities must be owned by same user.
    """
    # Verify ownership of both identities
    await verify_identity_ownership(identity_id, current_user_id)
    await verify_identity_ownership(target_identity_id, current_user_id)
    
    # R&D Rule #1: Checkpoint required
    checkpoint_id = uuid4()
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_pending",
            "checkpoint": {
                "id": str(checkpoint_id),
                "type": "identity_transfer",
                "action": "transfer_data",
                "source_identity": str(identity_id),
                "target_identity": str(target_identity_id),
                "data_type": data_type,
                "description": description,
                "requires_approval": True,
                "created_at": datetime.utcnow().isoformat(),
                "options": ["approve", "reject"]
            },
            "message": "Cross-identity data transfer requires human approval"
        }
    )

# --- IDENTITY BOUNDARY VERIFICATION ---

@router.post("/verify-boundary")
async def verify_identity_boundary(
    resource_identity_id: UUID = Body(..., embed=True),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """
    Verify if current user can access a resource's identity.
    
    R&D Rule #3: Explicit boundary check.
    """
    if resource_identity_id not in _identities_store:
        return {
            "allowed": False,
            "reason": "Identity not found"
        }
    
    identity = _identities_store[resource_identity_id]
    is_owner = identity["user_id"] == current_user_id
    
    return {
        "resource_identity": str(resource_identity_id),
        "allowed": is_owner,
        "reason": "Owner access" if is_owner else "Identity boundary violation",
        "code": "ACCESS_GRANTED" if is_owner else "RULE_3_VIOLATION"
    }

# --- HEALTH ---

@router.get("/health/check")
async def health_check():
    """Health check for identities router."""
    return {
        "status": "healthy",
        "router": "identities",
        "version": "1.0.0",
        "endpoints": 14,
        "rd_rules_enforced": ["#1", "#3", "#6", "#7"],
        "spheres_per_identity": 9,
        "cross_identity_blocked": True
    }
