"""
ROUTES: waitlist_routes.py
PREFIX: /api/v1/waitlist
VERSION: 1.0.0

PURPOSE: API endpoints for Waitlist Management
- Submit email to waitlist
- Check if email exists
- Admin statistics

COMPLIANCE:
- GDPR: Consent tracking with timestamps
- Deduplication: Prevent duplicate entries
- Source Tracking: Track signup origin
"""

from fastapi import APIRouter, HTTPException, Depends, Query, Body, Header
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime, timezone
import logging

from app.schemas.waitlist_schemas import (
    WaitlistSource,
    WaitlistSubmitRequest,
    WaitlistResponse,
    WaitlistCheckResponse,
    WaitlistStatsResponse,
    WaitlistEntry,
    WaitlistBulkInviteRequest,
    WaitlistBulkInviteResponse,
)
from app.services.waitlist_service import WaitlistService, get_waitlist_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/waitlist", tags=["Waitlist"])


# =============================================================================
# DEPENDENCY INJECTION
# =============================================================================

def get_service() -> WaitlistService:
    """Get waitlist service instance."""
    return get_waitlist_service()


def verify_admin_access(x_admin_token: Optional[str] = Header(None)) -> bool:
    """
    Verify admin access for protected endpoints.

    In production, replace with proper auth check.
    """
    # TODO: Implement proper admin authentication
    # For now, check for a simple header token
    admin_tokens = ["admin-secret-token", "dev-admin-access"]

    if x_admin_token and x_admin_token in admin_tokens:
        return True

    # In development, allow access without token
    import os
    if os.getenv("ENVIRONMENT", "development") == "development":
        return True

    raise HTTPException(
        status_code=403,
        detail="Admin access required"
    )


# =============================================================================
# PUBLIC ENDPOINTS
# =============================================================================

@router.post("", response_model=WaitlistResponse)
async def submit_to_waitlist(
    request: WaitlistSubmitRequest,
    service: WaitlistService = Depends(get_service)
):
    """
    Submit email to waitlist.

    - Validates email format
    - Checks for disposable emails
    - Tracks source, campaign, and referrer
    - Records consent with timestamp
    - Returns queue position

    **Sources:**
    - `landing`: Main landing page
    - `auth`: During auth flow
    - `essaim`: Essaim signup flow
    - `module`: From specific module
    - `referral`: Referral link
    - `partner`: Partner integration
    """
    try:
        response = await service.submit(request)

        # Log for analytics
        logger.info(
            f"Waitlist submission | success={response.success} | "
            f"email_hash={hash(request.email) % 10000} | "
            f"source={request.source} | campaign={request.campaign}"
        )

        return response

    except Exception as e:
        logger.error(f"Waitlist submission error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process waitlist submission"
        )


@router.get("/check", response_model=WaitlistCheckResponse)
async def check_waitlist_status(
    email: str = Query(..., description="Email to check"),
    service: WaitlistService = Depends(get_service)
):
    """
    Check if email exists on waitlist.

    Returns current status and queue position if pending.
    """
    try:
        response = await service.check_email(email)
        return response

    except Exception as e:
        logger.error(f"Waitlist check error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to check waitlist status"
        )


@router.get("/position")
async def get_position(
    email: str = Query(..., description="Email to check position for"),
    service: WaitlistService = Depends(get_service)
):
    """
    Get queue position for email.

    Simpler endpoint for checking position only.
    """
    try:
        response = await service.check_email(email)

        if not response.exists:
            raise HTTPException(
                status_code=404,
                detail="Email not found on waitlist"
            )

        return {
            "email": email,
            "position": response.position,
            "status": response.status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Position check error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to check position"
        )


# =============================================================================
# ADMIN ENDPOINTS
# =============================================================================

@router.get("/stats", response_model=WaitlistStatsResponse)
async def get_waitlist_stats(
    is_admin: bool = Depends(verify_admin_access),
    service: WaitlistService = Depends(get_service)
):
    """
    Get waitlist statistics (admin only).

    Returns:
    - Total entries and breakdown by status
    - Counts by source
    - Time-based statistics (today, week, month)
    - Conversion rates
    - Recent signups
    """
    try:
        stats = await service.get_stats()

        return WaitlistStatsResponse(
            success=True,
            stats=stats
        )

    except Exception as e:
        logger.error(f"Stats retrieval error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve statistics"
        )


@router.get("/entries/{entry_id}", response_model=WaitlistEntry)
async def get_entry(
    entry_id: str,
    is_admin: bool = Depends(verify_admin_access),
    service: WaitlistService = Depends(get_service)
):
    """
    Get single waitlist entry by ID (admin only).
    """
    entry = await service.get_entry(entry_id)

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Entry not found"
        )

    return entry


@router.post("/invite", response_model=WaitlistBulkInviteResponse)
async def send_bulk_invites(
    request: WaitlistBulkInviteRequest,
    is_admin: bool = Depends(verify_admin_access),
    service: WaitlistService = Depends(get_service)
):
    """
    Send batch invitations (admin only).

    Marks oldest pending entries as invited.
    Optionally filter by source.
    """
    try:
        invited_ids = await service.invite_batch(
            count=request.count,
            source_filter=request.source_filter
        )

        return WaitlistBulkInviteResponse(
            success=True,
            invited_count=len(invited_ids),
            message=f"Successfully invited {len(invited_ids)} users",
            entry_ids=invited_ids
        )

    except Exception as e:
        logger.error(f"Bulk invite error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process invitations"
        )


@router.post("/mark-registered")
async def mark_as_registered(
    email: str = Body(..., embed=True),
    is_admin: bool = Depends(verify_admin_access),
    service: WaitlistService = Depends(get_service)
):
    """
    Mark waitlist entry as registered (admin only).

    Called when a waitlisted user completes registration.
    """
    try:
        success = await service.mark_registered(email)

        if not success:
            raise HTTPException(
                status_code=404,
                detail="Email not found on waitlist"
            )

        return {
            "success": True,
            "message": f"Marked {email} as registered",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Mark registered error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update status"
        )


@router.delete("/entries/{entry_id}")
async def delete_entry(
    entry_id: str,
    is_admin: bool = Depends(verify_admin_access),
    service: WaitlistService = Depends(get_service)
):
    """
    Delete waitlist entry (admin only).

    Use for GDPR deletion requests.
    """
    try:
        success = await service.delete_entry(entry_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail="Entry not found"
            )

        return {
            "success": True,
            "message": "Entry deleted successfully",
            "entry_id": entry_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete entry error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete entry"
        )


# =============================================================================
# HEALTH CHECK
# =============================================================================

@router.get("/health")
async def waitlist_health():
    """Health check for waitlist service."""
    return {
        "status": "healthy",
        "service": "waitlist",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
