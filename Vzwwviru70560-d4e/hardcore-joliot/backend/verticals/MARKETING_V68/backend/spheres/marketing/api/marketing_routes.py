"""
CHE·NU™ V68 - Marketing Automation API Routes
50+ endpoints for complete marketing automation
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr

from ..agents.marketing_agent import (
    MarketingAutomationService,
    CampaignStatus, CampaignType, ContactStatus,
    AutomationTrigger, AutomationAction
)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ContactCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


class TagsUpdate(BaseModel):
    tags: List[str]


class SegmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    conditions: Optional[List[Dict[str, Any]]] = None


class TemplateCreate(BaseModel):
    name: str
    subject: str = ""
    html_content: str = ""
    text_content: str = ""
    category: str = "general"


class CampaignCreate(BaseModel):
    name: str
    campaign_type: str = "email"
    subject: str = ""
    preview_text: str = ""
    from_name: str = ""
    from_email: str = ""
    reply_to: Optional[str] = None
    html_content: str = ""
    text_content: str = ""
    template_id: Optional[str] = None
    segment_ids: Optional[List[str]] = None


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    preview_text: Optional[str] = None
    from_name: Optional[str] = None
    from_email: Optional[str] = None
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    segment_ids: Optional[List[str]] = None


class CampaignSchedule(BaseModel):
    scheduled_at: datetime


class ABTestCreate(BaseModel):
    test_type: str = "subject"
    variants: List[Dict[str, Any]]
    test_size_percent: int = 20


class AutomationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    trigger: str
    trigger_config: Optional[Dict[str, Any]] = None


class AutomationStepAdd(BaseModel):
    action: str
    config: Optional[Dict[str, Any]] = None
    position: Optional[int] = None


class LandingPageCreate(BaseModel):
    name: str
    slug: str
    html_content: str = ""
    css_content: str = ""
    meta_title: str = ""
    meta_description: str = ""


class FormCreate(BaseModel):
    name: str
    fields: Optional[List[Dict[str, Any]]] = None
    submit_button_text: str = "Submit"
    success_message: str = "Thank you!"
    redirect_url: Optional[str] = None
    tags_to_add: Optional[List[str]] = None
    automation_id: Optional[str] = None


class FormSubmissionData(BaseModel):
    data: Dict[str, Any]
    ip_address: Optional[str] = None
    page_url: Optional[str] = None


class SubjectOptimization(BaseModel):
    subject: str
    audience_data: Optional[Dict[str, Any]] = None


class ContentSuggestion(BaseModel):
    topic: str
    tone: str = "professional"


# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter()
service = MarketingAutomationService()


# ============================================================================
# CONTACTS
# ============================================================================

@router.post("/contacts")
async def create_contact(
    contact: ContactCreate,
    user_id: str = Query(..., description="User ID")
):
    """Create a new contact"""
    try:
        result = service.create_contact(
            email=contact.email,
            created_by=user_id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            phone=contact.phone,
            company=contact.company,
            tags=contact.tags,
            source=contact.source,
            custom_fields=contact.custom_fields
        )
        return {"contact": _contact_to_dict(result)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/contacts")
async def list_contacts(
    workspace_id: str = Query(...),
    status: Optional[str] = None,
    tag: Optional[str] = None,
    segment_id: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(50, le=100),
    offset: int = 0
):
    """List contacts with filters"""
    status_enum = ContactStatus(status) if status else None
    contacts = service.list_contacts(
        workspace_id=workspace_id,
        status=status_enum,
        tag=tag,
        segment_id=segment_id,
        search=search,
        limit=limit,
        offset=offset
    )
    return {
        "contacts": [_contact_to_dict(c) for c in contacts],
        "count": len(contacts)
    }


@router.get("/contacts/{contact_id}")
async def get_contact(contact_id: str):
    """Get contact by ID"""
    contact = service.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"contact": _contact_to_dict(contact)}


@router.put("/contacts/{contact_id}")
async def update_contact(
    contact_id: str,
    updates: ContactUpdate,
    user_id: str = Query(...)
):
    """Update contact"""
    contact = service.update_contact(
        contact_id,
        updates.dict(exclude_unset=True),
        user_id
    )
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"contact": _contact_to_dict(contact)}


@router.post("/contacts/{contact_id}/tags")
async def add_contact_tags(contact_id: str, tags: TagsUpdate):
    """Add tags to contact"""
    contact = service.add_tags(contact_id, tags.tags)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"contact": _contact_to_dict(contact)}


@router.delete("/contacts/{contact_id}/tags")
async def remove_contact_tags(contact_id: str, tags: TagsUpdate):
    """Remove tags from contact"""
    contact = service.remove_tags(contact_id, tags.tags)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"contact": _contact_to_dict(contact)}


@router.post("/contacts/{contact_id}/unsubscribe")
async def unsubscribe_contact(contact_id: str, reason: Optional[str] = None):
    """Unsubscribe contact"""
    contact = service.unsubscribe_contact(contact_id, reason)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"contact": _contact_to_dict(contact)}


@router.get("/contacts/{contact_id}/lead-score")
async def get_lead_score(contact_id: str):
    """Get AI-calculated lead score"""
    score = service.calculate_lead_score(contact_id)
    if not score:
        raise HTTPException(status_code=404, detail="Contact not found")
    return score


# ============================================================================
# SEGMENTS
# ============================================================================

@router.post("/workspaces/{workspace_id}/segments")
async def create_segment(
    workspace_id: str,
    segment: SegmentCreate,
    user_id: str = Query(...)
):
    """Create a contact segment"""
    result = service.create_segment(
        name=segment.name,
        workspace_id=workspace_id,
        created_by=user_id,
        conditions=segment.conditions,
        description=segment.description
    )
    return {"segment": _segment_to_dict(result)}


@router.get("/workspaces/{workspace_id}/segments")
async def list_segments(workspace_id: str):
    """List all segments"""
    segments = service.list_segments(workspace_id)
    return {"segments": [_segment_to_dict(s) for s in segments]}


@router.get("/segments/{segment_id}")
async def get_segment(segment_id: str):
    """Get segment by ID"""
    segment = service.get_segment(segment_id)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")
    return {"segment": _segment_to_dict(segment)}


# ============================================================================
# TEMPLATES
# ============================================================================

@router.post("/workspaces/{workspace_id}/templates")
async def create_template(
    workspace_id: str,
    template: TemplateCreate,
    user_id: str = Query(...)
):
    """Create email template"""
    result = service.create_template(
        name=template.name,
        workspace_id=workspace_id,
        created_by=user_id,
        subject=template.subject,
        html_content=template.html_content,
        text_content=template.text_content,
        category=template.category
    )
    return {"template": _template_to_dict(result)}


@router.get("/workspaces/{workspace_id}/templates")
async def list_templates(
    workspace_id: str,
    category: Optional[str] = None
):
    """List email templates"""
    templates = service.list_templates(workspace_id, category)
    return {"templates": [_template_to_dict(t) for t in templates]}


@router.get("/templates/{template_id}")
async def get_template(template_id: str):
    """Get template by ID"""
    template = service.get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"template": _template_to_dict(template)}


# ============================================================================
# CAMPAIGNS
# ============================================================================

@router.post("/workspaces/{workspace_id}/campaigns")
async def create_campaign(
    workspace_id: str,
    campaign: CampaignCreate,
    user_id: str = Query(...)
):
    """Create a new campaign"""
    result = service.create_campaign(
        name=campaign.name,
        workspace_id=workspace_id,
        created_by=user_id,
        campaign_type=CampaignType(campaign.campaign_type),
        subject=campaign.subject,
        from_name=campaign.from_name,
        from_email=campaign.from_email,
        html_content=campaign.html_content,
        segment_ids=campaign.segment_ids
    )
    return {"campaign": _campaign_to_dict(result)}


@router.get("/workspaces/{workspace_id}/campaigns")
async def list_campaigns(
    workspace_id: str,
    status: Optional[str] = None,
    campaign_type: Optional[str] = None
):
    """List campaigns"""
    status_enum = CampaignStatus(status) if status else None
    type_enum = CampaignType(campaign_type) if campaign_type else None
    
    campaigns = service.list_campaigns(workspace_id, status_enum, type_enum)
    return {"campaigns": [_campaign_to_dict(c) for c in campaigns]}


@router.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str):
    """Get campaign by ID"""
    campaign = service.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"campaign": _campaign_to_dict(campaign)}


@router.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: str, updates: CampaignUpdate):
    """Update campaign"""
    try:
        campaign = service.update_campaign(
            campaign_id,
            updates.dict(exclude_unset=True)
        )
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return {"campaign": _campaign_to_dict(campaign)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/campaigns/{campaign_id}/schedule")
async def schedule_campaign(
    campaign_id: str,
    schedule: CampaignSchedule,
    user_id: str = Query(...)
):
    """Schedule campaign for sending"""
    try:
        campaign = service.schedule_campaign(
            campaign_id,
            schedule.scheduled_at,
            user_id
        )
        return {"campaign": _campaign_to_dict(campaign)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/campaigns/{campaign_id}/send")
async def send_campaign(campaign_id: str, user_id: str = Query(...)):
    """Send campaign immediately"""
    try:
        campaign = service.send_campaign(campaign_id, user_id)
        return {"campaign": _campaign_to_dict(campaign)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/campaigns/{campaign_id}/pause")
async def pause_campaign(campaign_id: str):
    """Pause scheduled campaign"""
    campaign = service.pause_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"campaign": _campaign_to_dict(campaign)}


@router.get("/campaigns/{campaign_id}/stats")
async def get_campaign_stats(campaign_id: str):
    """Get detailed campaign statistics"""
    stats = service.get_campaign_stats(campaign_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return stats


# ============================================================================
# A/B TESTING
# ============================================================================

@router.post("/campaigns/{campaign_id}/ab-test")
async def create_ab_test(
    campaign_id: str,
    ab_test: ABTestCreate,
    user_id: str = Query(...)
):
    """Create A/B test for campaign"""
    try:
        result = service.create_ab_test(
            campaign_id=campaign_id,
            created_by=user_id,
            test_type=ab_test.test_type,
            variants=ab_test.variants,
            test_size_percent=ab_test.test_size_percent
        )
        return {"ab_test": _ab_test_to_dict(result)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/ab-tests/{test_id}/results")
async def get_ab_test_results(test_id: str):
    """Get A/B test results"""
    results = service.get_ab_test_results(test_id)
    if not results:
        raise HTTPException(status_code=404, detail="A/B test not found")
    return results


# ============================================================================
# AUTOMATIONS
# ============================================================================

@router.post("/workspaces/{workspace_id}/automations")
async def create_automation(
    workspace_id: str,
    automation: AutomationCreate,
    user_id: str = Query(...)
):
    """Create automation workflow"""
    result = service.create_automation(
        name=automation.name,
        workspace_id=workspace_id,
        created_by=user_id,
        trigger=AutomationTrigger(automation.trigger),
        trigger_config=automation.trigger_config,
        description=automation.description
    )
    return {"automation": _automation_to_dict(result)}


@router.get("/workspaces/{workspace_id}/automations")
async def list_automations(
    workspace_id: str,
    active_only: bool = False
):
    """List automations"""
    automations = service.list_automations(workspace_id, active_only)
    return {"automations": [_automation_to_dict(a) for a in automations]}


@router.get("/automations/{automation_id}")
async def get_automation(automation_id: str):
    """Get automation by ID"""
    automation = service.get_automation(automation_id)
    if not automation:
        raise HTTPException(status_code=404, detail="Automation not found")
    return {"automation": _automation_to_dict(automation)}


@router.post("/automations/{automation_id}/steps")
async def add_automation_step(automation_id: str, step: AutomationStepAdd):
    """Add step to automation"""
    automation = service.add_automation_step(
        automation_id,
        AutomationAction(step.action),
        step.config,
        step.position
    )
    if not automation:
        raise HTTPException(status_code=404, detail="Automation not found")
    return {"automation": _automation_to_dict(automation)}


@router.post("/automations/{automation_id}/activate")
async def activate_automation(automation_id: str):
    """Activate automation"""
    automation = service.activate_automation(automation_id)
    if not automation:
        raise HTTPException(status_code=404, detail="Automation not found")
    return {"automation": _automation_to_dict(automation)}


@router.post("/automations/{automation_id}/deactivate")
async def deactivate_automation(automation_id: str):
    """Deactivate automation"""
    automation = service.deactivate_automation(automation_id)
    if not automation:
        raise HTTPException(status_code=404, detail="Automation not found")
    return {"automation": _automation_to_dict(automation)}


@router.post("/automations/{automation_id}/trigger")
async def trigger_automation(automation_id: str, contact_id: str = Query(...)):
    """Manually trigger automation for contact"""
    enrollment = service.trigger_automation(automation_id, contact_id)
    if not enrollment:
        raise HTTPException(status_code=400, detail="Could not enroll contact")
    return {"enrollment_id": enrollment.id, "status": enrollment.status}


# ============================================================================
# LANDING PAGES
# ============================================================================

@router.post("/workspaces/{workspace_id}/landing-pages")
async def create_landing_page(
    workspace_id: str,
    page: LandingPageCreate,
    user_id: str = Query(...)
):
    """Create landing page"""
    try:
        result = service.create_landing_page(
            name=page.name,
            workspace_id=workspace_id,
            created_by=user_id,
            slug=page.slug,
            html_content=page.html_content,
            meta_title=page.meta_title,
            meta_description=page.meta_description
        )
        return {"landing_page": _landing_page_to_dict(result)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/workspaces/{workspace_id}/landing-pages")
async def list_landing_pages(workspace_id: str):
    """List landing pages"""
    pages = [p for p in service.landing_pages.values() 
             if p.workspace_id == workspace_id]
    return {"landing_pages": [_landing_page_to_dict(p) for p in pages]}


@router.post("/landing-pages/{page_id}/publish")
async def publish_landing_page(page_id: str):
    """Publish landing page"""
    page = service.publish_landing_page(page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    return {"landing_page": _landing_page_to_dict(page)}


@router.post("/landing-pages/{page_id}/unpublish")
async def unpublish_landing_page(page_id: str):
    """Unpublish landing page"""
    page = service.unpublish_landing_page(page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Landing page not found")
    return {"landing_page": _landing_page_to_dict(page)}


@router.post("/landing-pages/{page_id}/view")
async def record_page_view(page_id: str, is_unique: bool = True):
    """Record page view"""
    service.record_page_view(page_id, is_unique)
    return {"success": True}


# ============================================================================
# FORMS
# ============================================================================

@router.post("/workspaces/{workspace_id}/forms")
async def create_form(
    workspace_id: str,
    form: FormCreate,
    user_id: str = Query(...)
):
    """Create lead capture form"""
    result = service.create_form(
        name=form.name,
        workspace_id=workspace_id,
        created_by=user_id,
        fields=form.fields,
        submit_button_text=form.submit_button_text,
        tags_to_add=form.tags_to_add,
        automation_id=form.automation_id
    )
    return {"form": _form_to_dict(result)}


@router.get("/workspaces/{workspace_id}/forms")
async def list_forms(workspace_id: str):
    """List forms"""
    forms = service.list_forms(workspace_id)
    return {"forms": [_form_to_dict(f) for f in forms]}


@router.get("/forms/{form_id}")
async def get_form(form_id: str):
    """Get form by ID"""
    form = service.get_form(form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    return {"form": _form_to_dict(form)}


@router.post("/forms/{form_id}/submit")
async def submit_form(form_id: str, submission: FormSubmissionData):
    """Submit form"""
    try:
        result = service.submit_form(
            form_id=form_id,
            data=submission.data,
            ip_address=submission.ip_address,
            page_url=submission.page_url
        )
        return {
            "submission_id": result.id,
            "contact_id": result.contact_id,
            "success": True
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# AI FEATURES
# ============================================================================

@router.post("/ai/optimize-subject")
async def optimize_subject_line(request: SubjectOptimization):
    """Get AI-optimized subject line suggestions"""
    result = service.optimize_subject(request.subject, request.audience_data)
    return result


@router.get("/ai/send-time")
async def get_send_time_recommendation():
    """Get AI-recommended send time"""
    return service.get_send_time_recommendation()


@router.post("/ai/content-suggestions")
async def get_content_suggestions(request: ContentSuggestion):
    """Get AI content suggestions"""
    return service.get_content_suggestions(request.topic, request.tone)


@router.get("/ai/auto-segment")
async def auto_segment_contacts(workspace_id: str = Query(...)):
    """Auto-segment contacts using AI"""
    return service.auto_segment_contacts(workspace_id)


# ============================================================================
# DASHBOARD
# ============================================================================

@router.get("/workspaces/{workspace_id}/dashboard")
async def get_dashboard(workspace_id: str):
    """Get marketing dashboard statistics"""
    return service.get_dashboard_stats(workspace_id)


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "marketing_automation",
        "version": "1.0.0"
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _contact_to_dict(contact) -> Dict[str, Any]:
    return {
        "id": contact.id,
        "email": contact.email,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "phone": contact.phone,
        "company": contact.company,
        "job_title": contact.job_title,
        "status": contact.status.value,
        "tags": contact.tags,
        "segments": contact.segments,
        "lead_score": contact.lead_score,
        "source": contact.source,
        "custom_fields": contact.custom_fields,
        "email_stats": contact.email_stats,
        "created_at": contact.created_at.isoformat(),
        "last_activity": contact.last_activity.isoformat() if contact.last_activity else None
    }


def _segment_to_dict(segment) -> Dict[str, Any]:
    return {
        "id": segment.id,
        "name": segment.name,
        "description": segment.description,
        "conditions": segment.conditions,
        "contact_count": segment.contact_count,
        "is_dynamic": segment.is_dynamic,
        "created_at": segment.created_at.isoformat()
    }


def _template_to_dict(template) -> Dict[str, Any]:
    return {
        "id": template.id,
        "name": template.name,
        "subject": template.subject,
        "preview_text": template.preview_text,
        "html_content": template.html_content,
        "text_content": template.text_content,
        "category": template.category,
        "variables": template.variables,
        "created_at": template.created_at.isoformat()
    }


def _campaign_to_dict(campaign) -> Dict[str, Any]:
    return {
        "id": campaign.id,
        "name": campaign.name,
        "campaign_type": campaign.campaign_type.value,
        "status": campaign.status.value,
        "subject": campaign.subject,
        "preview_text": campaign.preview_text,
        "from_name": campaign.from_name,
        "from_email": campaign.from_email,
        "html_content": campaign.html_content,
        "segment_ids": campaign.segment_ids,
        "scheduled_at": campaign.scheduled_at.isoformat() if campaign.scheduled_at else None,
        "sent_at": campaign.sent_at.isoformat() if campaign.sent_at else None,
        "stats": campaign.stats,
        "ab_test": campaign.ab_test,
        "created_at": campaign.created_at.isoformat()
    }


def _ab_test_to_dict(ab_test) -> Dict[str, Any]:
    return {
        "id": ab_test.id,
        "campaign_id": ab_test.campaign_id,
        "test_type": ab_test.test_type,
        "variants": ab_test.variants,
        "winner_criteria": ab_test.winner_criteria,
        "test_size_percent": ab_test.test_size_percent,
        "status": ab_test.status,
        "winner_id": ab_test.winner_id,
        "created_at": ab_test.created_at.isoformat()
    }


def _automation_to_dict(automation) -> Dict[str, Any]:
    return {
        "id": automation.id,
        "name": automation.name,
        "description": automation.description,
        "trigger": automation.trigger.value,
        "trigger_config": automation.trigger_config,
        "steps": automation.steps,
        "is_active": automation.is_active,
        "stats": automation.stats,
        "created_at": automation.created_at.isoformat()
    }


def _landing_page_to_dict(page) -> Dict[str, Any]:
    return {
        "id": page.id,
        "name": page.name,
        "slug": page.slug,
        "html_content": page.html_content,
        "css_content": page.css_content,
        "meta_title": page.meta_title,
        "meta_description": page.meta_description,
        "is_published": page.is_published,
        "published_at": page.published_at.isoformat() if page.published_at else None,
        "form_id": page.form_id,
        "stats": page.stats,
        "created_at": page.created_at.isoformat()
    }


def _form_to_dict(form) -> Dict[str, Any]:
    return {
        "id": form.id,
        "name": form.name,
        "fields": form.fields,
        "submit_button_text": form.submit_button_text,
        "success_message": form.success_message,
        "redirect_url": form.redirect_url,
        "tags_to_add": form.tags_to_add,
        "automation_id": form.automation_id,
        "submissions_count": form.submissions_count,
        "created_at": form.created_at.isoformat()
    }
