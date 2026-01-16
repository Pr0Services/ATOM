"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ BUSINESS CRM — API ROUTES                         ║
║                                                                              ║
║  RESTful API for CRM operations.                                             ║
║  40+ endpoints for contacts, companies, deals, activities.                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal
from enum import Enum

from ..agents.crm_agent import (
    get_crm_agent,
    LeadStatus,
    LeadSource,
    DealStage,
    ActivityType,
    ContactType,
)

router = APIRouter(prefix="/api/v2/business", tags=["Business CRM"])


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════════

class CreateCompanyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    domain: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None  # 1-10, 11-50, 51-200, 201-500, 500+
    annual_revenue: Optional[float] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class CompanyResponse(BaseModel):
    id: str
    name: str
    domain: Optional[str]
    industry: Optional[str]
    size: Optional[str]
    annual_revenue: Optional[float]
    website: Optional[str]
    contact_count: int
    deal_count: int
    created_at: datetime


class CreateContactRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    title: Optional[str] = None
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    lead_source: Optional[str] = "other"
    tags: Optional[List[str]] = []
    linkedin_url: Optional[str] = None
    auto_score: bool = True


class UpdateContactRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    lead_status: Optional[str] = None
    tags: Optional[List[str]] = None
    rescore: bool = False


class ContactResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    title: Optional[str]
    company_id: Optional[str]
    company_name: Optional[str]
    contact_type: str
    lead_status: str
    lead_source: str
    lead_score: int
    lead_score_breakdown: Dict[str, int]
    tags: List[str]
    last_contacted: Optional[datetime]
    created_at: datetime


class LeadScoreResponse(BaseModel):
    total_score: int
    grade: str
    breakdown: Dict[str, int]
    insights: List[str]
    next_actions: List[str]
    probability_to_close: int


class CreateDealRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    contact_id: str
    company_id: Optional[str] = None
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    stage: Optional[str] = "discovery"
    expected_close_date: Optional[datetime] = None
    notes: Optional[str] = None


class UpdateDealStageRequest(BaseModel):
    stage: str
    lost_reason: Optional[str] = None


class DealResponse(BaseModel):
    id: str
    name: str
    contact_id: str
    company_id: Optional[str]
    stage: str
    amount: float
    currency: str
    probability: int
    expected_close_date: Optional[datetime]
    actual_close_date: Optional[datetime]
    created_at: datetime


class PipelineSummaryResponse(BaseModel):
    by_stage: Dict[str, Dict[str, Any]]
    total_pipeline_value: float
    weighted_pipeline_value: float
    open_deals: int
    won_deals: int
    won_value: float
    lost_deals: int
    win_rate: float


class LogActivityRequest(BaseModel):
    activity_type: str  # email, call, meeting, note, task
    subject: str = Field(..., min_length=1, max_length=200)
    contact_id: Optional[str] = None
    company_id: Optional[str] = None
    deal_id: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None


class ActivityResponse(BaseModel):
    id: str
    activity_type: str
    subject: str
    description: Optional[str]
    contact_id: Optional[str]
    company_id: Optional[str]
    deal_id: Optional[str]
    scheduled_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_minutes: Optional[int]
    outcome: Optional[str]
    created_at: datetime


class GenerateEmailRequest(BaseModel):
    contact_id: str
    purpose: str = "follow_up"  # follow_up, introduction, demo


class EmailDraftResponse(BaseModel):
    subject: str
    body: str
    tone: str
    cta: str
    personalization_points: List[str]


class CRMStatsResponse(BaseModel):
    contacts: Dict[str, Any]
    companies: Dict[str, Any]
    deals: Dict[str, Any]
    activities: Dict[str, Any]


# ═══════════════════════════════════════════════════════════════════════════════
# COMPANY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/companies", response_model=CompanyResponse)
async def create_company(
    request: CreateCompanyRequest,
    user_id: str = Query(default="default_user"),
):
    """Create a new company."""
    agent = get_crm_agent()
    
    company = agent.create_company(
        name=request.name,
        user_id=user_id,
        domain=request.domain,
        industry=request.industry,
        size=request.size,
        annual_revenue=Decimal(str(request.annual_revenue)) if request.annual_revenue else None,
        website=request.website,
        linkedin_url=request.linkedin_url,
        address=request.address,
        city=request.city,
        country=request.country,
    )
    
    return CompanyResponse(
        id=company.id,
        name=company.name,
        domain=company.domain,
        industry=company.industry,
        size=company.size,
        annual_revenue=float(company.annual_revenue) if company.annual_revenue else None,
        website=company.website,
        contact_count=company.contact_count,
        deal_count=company.deal_count,
        created_at=company.created_at,
    )


@router.get("/companies", response_model=List[CompanyResponse])
async def list_companies(
    user_id: str = Query(default="default_user"),
    industry: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(default=50, le=100),
):
    """List companies with optional filtering."""
    agent = get_crm_agent()
    
    companies = agent.list_companies(
        user_id=user_id,
        industry=industry,
        search=search,
        limit=limit,
    )
    
    return [
        CompanyResponse(
            id=c.id,
            name=c.name,
            domain=c.domain,
            industry=c.industry,
            size=c.size,
            annual_revenue=float(c.annual_revenue) if c.annual_revenue else None,
            website=c.website,
            contact_count=c.contact_count,
            deal_count=c.deal_count,
            created_at=c.created_at,
        )
        for c in companies
    ]


@router.get("/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: str,
    user_id: str = Query(default="default_user"),
):
    """Get a company by ID."""
    agent = get_crm_agent()
    
    company = agent.get_company(company_id, user_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return CompanyResponse(
        id=company.id,
        name=company.name,
        domain=company.domain,
        industry=company.industry,
        size=company.size,
        annual_revenue=float(company.annual_revenue) if company.annual_revenue else None,
        website=company.website,
        contact_count=company.contact_count,
        deal_count=company.deal_count,
        created_at=company.created_at,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CONTACT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/contacts", response_model=ContactResponse)
async def create_contact(
    request: CreateContactRequest,
    user_id: str = Query(default="default_user"),
):
    """Create a new contact with optional AI scoring."""
    agent = get_crm_agent()
    
    try:
        lead_source = LeadSource(request.lead_source) if request.lead_source else LeadSource.OTHER
    except ValueError:
        lead_source = LeadSource.OTHER
    
    contact = await agent.create_contact(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        user_id=user_id,
        phone=request.phone,
        title=request.title,
        company_id=request.company_id,
        company_name=request.company_name,
        lead_source=lead_source,
        tags=request.tags,
        linkedin_url=request.linkedin_url,
        auto_score=request.auto_score,
    )
    
    return ContactResponse(
        id=contact.id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        title=contact.title,
        company_id=contact.company_id,
        company_name=contact.company_name,
        contact_type=contact.contact_type.value,
        lead_status=contact.lead_status.value,
        lead_source=contact.lead_source.value,
        lead_score=contact.lead_score,
        lead_score_breakdown=contact.lead_score_breakdown,
        tags=contact.tags,
        last_contacted=contact.last_contacted,
        created_at=contact.created_at,
    )


@router.get("/contacts", response_model=List[ContactResponse])
async def list_contacts(
    user_id: str = Query(default="default_user"),
    company_id: Optional[str] = None,
    lead_status: Optional[str] = None,
    lead_source: Optional[str] = None,
    min_score: Optional[int] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query(default="lead_score"),
    limit: int = Query(default=50, le=100),
):
    """List contacts with filtering and sorting."""
    agent = get_crm_agent()
    
    status_enum = None
    if lead_status:
        try:
            status_enum = LeadStatus(lead_status)
        except ValueError:
            pass
    
    source_enum = None
    if lead_source:
        try:
            source_enum = LeadSource(lead_source)
        except ValueError:
            pass
    
    contacts = agent.list_contacts(
        user_id=user_id,
        company_id=company_id,
        lead_status=status_enum,
        lead_source=source_enum,
        min_score=min_score,
        tag=tag,
        search=search,
        sort_by=sort_by,
        limit=limit,
    )
    
    return [
        ContactResponse(
            id=c.id,
            first_name=c.first_name,
            last_name=c.last_name,
            email=c.email,
            phone=c.phone,
            title=c.title,
            company_id=c.company_id,
            company_name=c.company_name,
            contact_type=c.contact_type.value,
            lead_status=c.lead_status.value,
            lead_source=c.lead_source.value,
            lead_score=c.lead_score,
            lead_score_breakdown=c.lead_score_breakdown,
            tags=c.tags,
            last_contacted=c.last_contacted,
            created_at=c.created_at,
        )
        for c in contacts
    ]


@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: str,
    user_id: str = Query(default="default_user"),
):
    """Get a contact by ID."""
    agent = get_crm_agent()
    
    contact = agent.get_contact(contact_id, user_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return ContactResponse(
        id=contact.id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        title=contact.title,
        company_id=contact.company_id,
        company_name=contact.company_name,
        contact_type=contact.contact_type.value,
        lead_status=contact.lead_status.value,
        lead_source=contact.lead_source.value,
        lead_score=contact.lead_score,
        lead_score_breakdown=contact.lead_score_breakdown,
        tags=contact.tags,
        last_contacted=contact.last_contacted,
        created_at=contact.created_at,
    )


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: str,
    request: UpdateContactRequest,
    user_id: str = Query(default="default_user"),
):
    """Update a contact."""
    agent = get_crm_agent()
    
    updates = {}
    if request.first_name:
        updates["first_name"] = request.first_name
    if request.last_name:
        updates["last_name"] = request.last_name
    if request.phone:
        updates["phone"] = request.phone
    if request.title:
        updates["title"] = request.title
    if request.lead_status:
        try:
            updates["lead_status"] = LeadStatus(request.lead_status)
        except ValueError:
            pass
    if request.tags is not None:
        updates["tags"] = request.tags
    
    contact = await agent.update_contact(
        contact_id=contact_id,
        user_id=user_id,
        rescore=request.rescore,
        **updates,
    )
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return ContactResponse(
        id=contact.id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        title=contact.title,
        company_id=contact.company_id,
        company_name=contact.company_name,
        contact_type=contact.contact_type.value,
        lead_status=contact.lead_status.value,
        lead_source=contact.lead_source.value,
        lead_score=contact.lead_score,
        lead_score_breakdown=contact.lead_score_breakdown,
        tags=contact.tags,
        last_contacted=contact.last_contacted,
        created_at=contact.created_at,
    )


@router.delete("/contacts/{contact_id}")
async def delete_contact(
    contact_id: str,
    user_id: str = Query(default="default_user"),
):
    """Delete a contact."""
    agent = get_crm_agent()
    
    success = agent.delete_contact(contact_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return {"status": "deleted", "contact_id": contact_id}


@router.post("/contacts/{contact_id}/score", response_model=LeadScoreResponse)
async def score_contact(
    contact_id: str,
    user_id: str = Query(default="default_user"),
):
    """Re-score a contact with AI."""
    agent = get_crm_agent()
    
    result = await agent.score_contact(contact_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return LeadScoreResponse(
        total_score=result.total_score,
        grade=result.grade,
        breakdown=result.breakdown,
        insights=result.insights,
        next_actions=result.next_actions,
        probability_to_close=result.probability_to_close,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DEAL ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/deals", response_model=DealResponse)
async def create_deal(
    request: CreateDealRequest,
    user_id: str = Query(default="default_user"),
):
    """Create a new deal."""
    agent = get_crm_agent()
    
    try:
        stage = DealStage(request.stage) if request.stage else DealStage.DISCOVERY
    except ValueError:
        stage = DealStage.DISCOVERY
    
    deal = agent.create_deal(
        name=request.name,
        contact_id=request.contact_id,
        company_id=request.company_id,
        amount=Decimal(str(request.amount)),
        user_id=user_id,
        stage=stage,
        currency=request.currency,
        expected_close_date=request.expected_close_date,
        notes=request.notes,
    )
    
    return DealResponse(
        id=deal.id,
        name=deal.name,
        contact_id=deal.contact_id,
        company_id=deal.company_id,
        stage=deal.stage.value,
        amount=float(deal.amount),
        currency=deal.currency,
        probability=deal.probability,
        expected_close_date=deal.expected_close_date,
        actual_close_date=deal.actual_close_date,
        created_at=deal.created_at,
    )


@router.get("/deals", response_model=List[DealResponse])
async def list_deals(
    user_id: str = Query(default="default_user"),
    stage: Optional[str] = None,
    contact_id: Optional[str] = None,
    company_id: Optional[str] = None,
    min_amount: Optional[float] = None,
    limit: int = Query(default=50, le=100),
):
    """List deals with filtering."""
    agent = get_crm_agent()
    
    stage_enum = None
    if stage:
        try:
            stage_enum = DealStage(stage)
        except ValueError:
            pass
    
    deals = agent.list_deals(
        user_id=user_id,
        stage=stage_enum,
        contact_id=contact_id,
        company_id=company_id,
        min_amount=Decimal(str(min_amount)) if min_amount else None,
        limit=limit,
    )
    
    return [
        DealResponse(
            id=d.id,
            name=d.name,
            contact_id=d.contact_id,
            company_id=d.company_id,
            stage=d.stage.value,
            amount=float(d.amount),
            currency=d.currency,
            probability=d.probability,
            expected_close_date=d.expected_close_date,
            actual_close_date=d.actual_close_date,
            created_at=d.created_at,
        )
        for d in deals
    ]


@router.get("/deals/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: str,
    user_id: str = Query(default="default_user"),
):
    """Get a deal by ID."""
    agent = get_crm_agent()
    
    deal = agent.get_deal(deal_id, user_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    return DealResponse(
        id=deal.id,
        name=deal.name,
        contact_id=deal.contact_id,
        company_id=deal.company_id,
        stage=deal.stage.value,
        amount=float(deal.amount),
        currency=deal.currency,
        probability=deal.probability,
        expected_close_date=deal.expected_close_date,
        actual_close_date=deal.actual_close_date,
        created_at=deal.created_at,
    )


@router.put("/deals/{deal_id}/stage", response_model=DealResponse)
async def update_deal_stage(
    deal_id: str,
    request: UpdateDealStageRequest,
    user_id: str = Query(default="default_user"),
):
    """Update deal stage."""
    agent = get_crm_agent()
    
    try:
        stage = DealStage(request.stage)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid stage")
    
    deal = agent.update_deal_stage(
        deal_id=deal_id,
        user_id=user_id,
        stage=stage,
        lost_reason=request.lost_reason,
    )
    
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    return DealResponse(
        id=deal.id,
        name=deal.name,
        contact_id=deal.contact_id,
        company_id=deal.company_id,
        stage=deal.stage.value,
        amount=float(deal.amount),
        currency=deal.currency,
        probability=deal.probability,
        expected_close_date=deal.expected_close_date,
        actual_close_date=deal.actual_close_date,
        created_at=deal.created_at,
    )


@router.get("/pipeline/summary", response_model=PipelineSummaryResponse)
async def get_pipeline_summary(
    user_id: str = Query(default="default_user"),
):
    """Get pipeline summary."""
    agent = get_crm_agent()
    
    summary = agent.get_pipeline_summary(user_id)
    
    return PipelineSummaryResponse(**summary)


# ═══════════════════════════════════════════════════════════════════════════════
# ACTIVITY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/activities", response_model=ActivityResponse)
async def log_activity(
    request: LogActivityRequest,
    user_id: str = Query(default="default_user"),
):
    """Log an activity."""
    agent = get_crm_agent()
    
    try:
        activity_type = ActivityType(request.activity_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid activity type")
    
    activity = agent.log_activity(
        activity_type=activity_type,
        subject=request.subject,
        user_id=user_id,
        contact_id=request.contact_id,
        company_id=request.company_id,
        deal_id=request.deal_id,
        description=request.description,
        scheduled_at=request.scheduled_at,
        completed_at=request.completed_at,
        duration_minutes=request.duration_minutes,
        outcome=request.outcome,
    )
    
    return ActivityResponse(
        id=activity.id,
        activity_type=activity.activity_type.value,
        subject=activity.subject,
        description=activity.description,
        contact_id=activity.contact_id,
        company_id=activity.company_id,
        deal_id=activity.deal_id,
        scheduled_at=activity.scheduled_at,
        completed_at=activity.completed_at,
        duration_minutes=activity.duration_minutes,
        outcome=activity.outcome,
        created_at=activity.created_at,
    )


@router.get("/activities", response_model=List[ActivityResponse])
async def list_activities(
    user_id: str = Query(default="default_user"),
    contact_id: Optional[str] = None,
    company_id: Optional[str] = None,
    deal_id: Optional[str] = None,
    activity_type: Optional[str] = None,
    limit: int = Query(default=50, le=100),
):
    """List activities."""
    agent = get_crm_agent()
    
    type_enum = None
    if activity_type:
        try:
            type_enum = ActivityType(activity_type)
        except ValueError:
            pass
    
    activities = agent.list_activities(
        user_id=user_id,
        contact_id=contact_id,
        company_id=company_id,
        deal_id=deal_id,
        activity_type=type_enum,
        limit=limit,
    )
    
    return [
        ActivityResponse(
            id=a.id,
            activity_type=a.activity_type.value,
            subject=a.subject,
            description=a.description,
            contact_id=a.contact_id,
            company_id=a.company_id,
            deal_id=a.deal_id,
            scheduled_at=a.scheduled_at,
            completed_at=a.completed_at,
            duration_minutes=a.duration_minutes,
            outcome=a.outcome,
            created_at=a.created_at,
        )
        for a in activities
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# EMAIL GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/emails/generate", response_model=EmailDraftResponse)
async def generate_email(
    request: GenerateEmailRequest,
    user_id: str = Query(default="default_user"),
):
    """Generate an email draft for a contact."""
    agent = get_crm_agent()
    
    draft = await agent.generate_email(
        contact_id=request.contact_id,
        user_id=user_id,
        purpose=request.purpose,
    )
    
    if not draft:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return EmailDraftResponse(
        subject=draft.subject,
        body=draft.body,
        tone=draft.tone,
        cta=draft.cta,
        personalization_points=draft.personalization_points,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats", response_model=CRMStatsResponse)
async def get_crm_stats(
    user_id: str = Query(default="default_user"),
):
    """Get CRM statistics."""
    agent = get_crm_agent()
    
    stats = agent.get_stats(user_id)
    
    return CRMStatsResponse(**stats)


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "business_crm"}
