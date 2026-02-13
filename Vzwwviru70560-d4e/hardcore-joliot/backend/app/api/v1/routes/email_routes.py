"""
EMAIL AUTOMATION API ROUTES
============================

Endpoints pour la gestion des emails automatiques:
- POST /process - Traiter les emails en attente
- POST /unsubscribe - Se désinscrire
- GET /stats - Statistiques d'envoi
- GET /history/{email} - Historique d'un email
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

from ....services.email_automation_service import email_automation_service, EmailType

router = APIRouter(prefix="/email", tags=["email"])


# =============================================================================
# SCHEMAS
# =============================================================================

class ProcessRequest(BaseModel):
    entries: List[Dict[str, Any]]


class UnsubscribeRequest(BaseModel):
    email: EmailStr


class SendEmailRequest(BaseModel):
    email: EmailStr
    email_type: str
    name: Optional[str] = None


# =============================================================================
# ROUTES
# =============================================================================

@router.post("/process")
async def process_pending_emails(request: ProcessRequest):
    """
    Process all pending emails for waitlist entries.
    This should be called by a cron job or scheduler.
    """
    try:
        stats = await email_automation_service.process_all_pending(request.entries)
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send")
async def send_single_email(request: SendEmailRequest):
    """Send a specific email to a user."""
    try:
        email_type = EmailType(request.email_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid email_type. Must be one of: {[e.value for e in EmailType]}"
        )

    success = await email_automation_service.send_email(
        to_email=request.email,
        email_type=email_type,
        name=request.name
    )

    return {
        "success": success,
        "email": request.email,
        "type": request.email_type
    }


@router.post("/unsubscribe")
async def unsubscribe(request: UnsubscribeRequest):
    """Unsubscribe an email from all communications."""
    success = email_automation_service.unsubscribe(request.email)
    return {
        "success": success,
        "email": request.email,
        "message": "Successfully unsubscribed" if success else "Failed to unsubscribe"
    }


@router.post("/resubscribe")
async def resubscribe(request: UnsubscribeRequest):
    """Re-subscribe an email."""
    success = email_automation_service.resubscribe(request.email)
    return {
        "success": success,
        "email": request.email,
        "message": "Successfully re-subscribed" if success else "Failed to re-subscribe"
    }


@router.get("/history/{email}")
async def get_email_history(email: str):
    """Get email history for a specific address."""
    history = email_automation_service.get_email_history(email)
    return {
        "email": email,
        "history": history
    }


@router.get("/stats")
async def get_email_stats():
    """Get email automation statistics."""
    stats = email_automation_service.get_stats()
    return {
        "success": True,
        "stats": stats
    }


@router.get("/templates")
async def get_available_templates():
    """Get list of available email templates."""
    return {
        "templates": [
            {
                "type": email_type.value,
                "delay_days": email_automation_service.TEMPLATES[email_type].delay_days
                if hasattr(email_automation_service, 'TEMPLATES') else
                {"welcome": 0, "discovery": 2, "engagement": 7}.get(email_type.value, 0)
            }
            for email_type in EmailType
        ]
    }
