"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ BUSINESS CRM — CRM AGENT                          ║
║                                                                              ║
║  AI-powered CRM with intelligent lead scoring and sales automation.          ║
║                                                                              ║
║  Features:                                                                   ║
║  - Contact & Company management                                              ║
║  - AI Lead Scoring (multi-dimensional)                                       ║
║  - Deal Pipeline tracking                                                    ║
║  - Activity logging                                                          ║
║  - Email draft generation                                                    ║
║                                                                              ║
║  COS: 93/100 — Salesforce Competitor ($29/mo vs $300/mo)                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import uuid
import asyncio
import logging
import httpx
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from decimal import Decimal

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class LeadSource(str, Enum):
    WEBSITE = "website"
    REFERRAL = "referral"
    LINKEDIN = "linkedin"
    COLD_OUTREACH = "cold_outreach"
    EVENT = "event"
    PARTNER = "partner"
    OTHER = "other"


class DealStage(str, Enum):
    DISCOVERY = "discovery"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class ActivityType(str, Enum):
    EMAIL = "email"
    CALL = "call"
    MEETING = "meeting"
    NOTE = "note"
    TASK = "task"


class ContactType(str, Enum):
    LEAD = "lead"
    CUSTOMER = "customer"
    PARTNER = "partner"
    VENDOR = "vendor"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA MODELS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Company:
    """A company/organization."""
    id: str
    name: str
    domain: Optional[str]
    industry: Optional[str]
    size: Optional[str]  # 1-10, 11-50, 51-200, 201-500, 500+
    annual_revenue: Optional[Decimal]
    website: Optional[str]
    linkedin_url: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: str
    contact_count: int = 0
    deal_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Contact:
    """A contact/lead."""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    title: Optional[str]
    company_id: Optional[str]
    company_name: Optional[str]
    contact_type: ContactType
    lead_status: LeadStatus
    lead_source: LeadSource
    lead_score: int  # 0-100
    lead_score_breakdown: Dict[str, int]
    last_contacted: Optional[datetime]
    last_activity: Optional[datetime]
    linkedin_url: Optional[str]
    tags: List[str]
    owner_id: str
    created_at: datetime
    updated_at: datetime
    user_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Deal:
    """A sales deal/opportunity."""
    id: str
    name: str
    contact_id: str
    company_id: Optional[str]
    stage: DealStage
    amount: Decimal
    currency: str
    probability: int  # 0-100
    expected_close_date: Optional[datetime]
    actual_close_date: Optional[datetime]
    lost_reason: Optional[str]
    notes: Optional[str]
    owner_id: str
    created_at: datetime
    updated_at: datetime
    user_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Activity:
    """An activity/interaction."""
    id: str
    activity_type: ActivityType
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
    user_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LeadScoreResult:
    """Result of AI lead scoring."""
    total_score: int
    grade: str  # A, B, C, D, F
    breakdown: Dict[str, int]
    insights: List[str]
    next_actions: List[str]
    probability_to_close: int


@dataclass
class EmailDraft:
    """AI-generated email draft."""
    subject: str
    body: str
    tone: str
    cta: str
    personalization_points: List[str]


# ═══════════════════════════════════════════════════════════════════════════════
# AI ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class CRMAIEngine:
    """AI engine for CRM intelligence."""
    
    def __init__(self):
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.openai_key = os.environ.get("OPENAI_API_KEY", "")
    
    async def score_lead(self, contact: Contact, company: Optional[Company] = None) -> LeadScoreResult:
        """Score a lead using AI."""
        
        if self.anthropic_key:
            return await self._score_with_claude(contact, company)
        else:
            return self._local_scoring(contact, company)
    
    async def _score_with_claude(self, contact: Contact, company: Optional[Company]) -> LeadScoreResult:
        """Score with Claude."""
        
        company_info = ""
        if company:
            company_info = f"""
Company: {company.name}
Industry: {company.industry or 'Unknown'}
Size: {company.size or 'Unknown'}
Annual Revenue: ${company.annual_revenue or 'Unknown'}"""
        
        prompt = f"""Score this sales lead on a scale of 0-100. Analyze multiple dimensions.

LEAD INFORMATION:
Name: {contact.first_name} {contact.last_name}
Email: {contact.email}
Title: {contact.title or 'Unknown'}
Source: {contact.lead_source.value}
Current Status: {contact.lead_status.value}
{company_info}

Respond ONLY with valid JSON:
{{
    "total_score": 0-100,
    "breakdown": {{
        "fit": 0-25,           // How well they match ideal customer profile
        "engagement": 0-25,    // Activity and responsiveness
        "timing": 0-25,        // Buying signals and urgency
        "budget": 0-25         // Estimated budget/authority
    }},
    "insights": ["insight1", "insight2"],
    "next_actions": ["action1", "action2"],
    "probability_to_close": 0-100
}}"""

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 512,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    text = data["content"][0]["text"]
                    
                    json_start = text.find("{")
                    json_end = text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        result = json.loads(text[json_start:json_end])
                        
                        total = result.get("total_score", 50)
                        grade = "A" if total >= 80 else "B" if total >= 60 else "C" if total >= 40 else "D" if total >= 20 else "F"
                        
                        return LeadScoreResult(
                            total_score=total,
                            grade=grade,
                            breakdown=result.get("breakdown", {}),
                            insights=result.get("insights", []),
                            next_actions=result.get("next_actions", []),
                            probability_to_close=result.get("probability_to_close", total),
                        )
            except Exception as e:
                logger.error(f"Claude scoring failed: {e}")
        
        return self._local_scoring(contact, company)
    
    def _local_scoring(self, contact: Contact, company: Optional[Company]) -> LeadScoreResult:
        """Local fallback scoring."""
        
        breakdown = {"fit": 0, "engagement": 0, "timing": 0, "budget": 0}
        insights = []
        next_actions = []
        
        # Fit score (0-25)
        if contact.title:
            title_lower = contact.title.lower()
            if any(t in title_lower for t in ["ceo", "cto", "cfo", "vp", "director", "head"]):
                breakdown["fit"] = 25
                insights.append("Decision maker title detected")
            elif any(t in title_lower for t in ["manager", "lead", "senior"]):
                breakdown["fit"] = 18
            else:
                breakdown["fit"] = 10
        else:
            breakdown["fit"] = 5
        
        if company:
            if company.size in ["201-500", "500+"]:
                breakdown["fit"] += 5
                insights.append("Enterprise-size company")
        
        # Engagement score (0-25)
        if contact.lead_status == LeadStatus.QUALIFIED:
            breakdown["engagement"] = 25
        elif contact.lead_status == LeadStatus.CONTACTED:
            breakdown["engagement"] = 15
        elif contact.lead_status == LeadStatus.NEW:
            breakdown["engagement"] = 8
            next_actions.append("Make initial contact")
        
        # Timing score (0-25)
        status_timing = {
            LeadStatus.NEGOTIATION: 25,
            LeadStatus.PROPOSAL: 20,
            LeadStatus.QUALIFIED: 15,
            LeadStatus.CONTACTED: 10,
            LeadStatus.NEW: 5,
        }
        breakdown["timing"] = status_timing.get(contact.lead_status, 5)
        
        # Budget score (0-25)
        if company and company.annual_revenue:
            if company.annual_revenue >= 10000000:
                breakdown["budget"] = 25
            elif company.annual_revenue >= 1000000:
                breakdown["budget"] = 18
            else:
                breakdown["budget"] = 10
        else:
            breakdown["budget"] = 12  # Unknown = medium
        
        total = sum(breakdown.values())
        grade = "A" if total >= 80 else "B" if total >= 60 else "C" if total >= 40 else "D" if total >= 20 else "F"
        
        if not next_actions:
            if total >= 70:
                next_actions.append("Schedule demo call")
            elif total >= 50:
                next_actions.append("Send case study email")
            else:
                next_actions.append("Add to nurture campaign")
        
        return LeadScoreResult(
            total_score=total,
            grade=grade,
            breakdown=breakdown,
            insights=insights,
            next_actions=next_actions,
            probability_to_close=min(total + 10, 100),
        )
    
    async def generate_email_draft(
        self, 
        contact: Contact, 
        purpose: str = "follow_up",
        company: Optional[Company] = None
    ) -> EmailDraft:
        """Generate email draft."""
        
        if self.anthropic_key:
            return await self._generate_email_claude(contact, purpose, company)
        return self._local_email_draft(contact, purpose, company)
    
    async def _generate_email_claude(
        self, 
        contact: Contact, 
        purpose: str,
        company: Optional[Company]
    ) -> EmailDraft:
        """Generate with Claude."""
        
        prompt = f"""Write a professional sales email.

CONTACT:
Name: {contact.first_name} {contact.last_name}
Title: {contact.title or 'Professional'}
Company: {company.name if company else contact.company_name or 'their company'}

PURPOSE: {purpose}

Respond ONLY with valid JSON:
{{
    "subject": "email subject line",
    "body": "full email body with greeting and signature placeholder",
    "tone": "professional/friendly/urgent",
    "cta": "the call to action",
    "personalization_points": ["point1", "point2"]
}}"""

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.anthropic_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-3-haiku-20240307",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    text = data["content"][0]["text"]
                    
                    json_start = text.find("{")
                    json_end = text.rfind("}") + 1
                    if json_start >= 0 and json_end > json_start:
                        result = json.loads(text[json_start:json_end])
                        return EmailDraft(
                            subject=result.get("subject", "Following up"),
                            body=result.get("body", ""),
                            tone=result.get("tone", "professional"),
                            cta=result.get("cta", ""),
                            personalization_points=result.get("personalization_points", []),
                        )
            except Exception as e:
                logger.error(f"Claude email failed: {e}")
        
        return self._local_email_draft(contact, purpose, company)
    
    def _local_email_draft(
        self, 
        contact: Contact, 
        purpose: str,
        company: Optional[Company]
    ) -> EmailDraft:
        """Local email draft fallback."""
        
        company_name = company.name if company else contact.company_name or "your company"
        
        templates = {
            "follow_up": {
                "subject": f"Following up - {company_name}",
                "body": f"""Hi {contact.first_name},

I wanted to follow up on our previous conversation and see if you had any questions about how we can help {company_name}.

Would you have 15 minutes this week for a quick call?

Best regards,
[Your Name]""",
                "cta": "Schedule a call",
            },
            "introduction": {
                "subject": f"Quick introduction - helping {company_name}",
                "body": f"""Hi {contact.first_name},

I came across {company_name} and thought our solution might be a great fit for what you're building.

We help companies like yours [specific value prop]. Would you be open to a brief conversation?

Best regards,
[Your Name]""",
                "cta": "Learn more",
            },
            "demo": {
                "subject": f"Demo request - {company_name}",
                "body": f"""Hi {contact.first_name},

Thank you for your interest in our solution. I'd love to show you how we can help {company_name} achieve [specific goal].

When would be a good time for a 30-minute demo?

Best regards,
[Your Name]""",
                "cta": "Book demo",
            },
        }
        
        template = templates.get(purpose, templates["follow_up"])
        
        return EmailDraft(
            subject=template["subject"],
            body=template["body"],
            tone="professional",
            cta=template["cta"],
            personalization_points=[f"Personalized for {contact.first_name}", f"Company: {company_name}"],
        )


# ═══════════════════════════════════════════════════════════════════════════════
# CRM AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class CRMAgent:
    """
    CHE·NU Business CRM Agent.
    
    Features:
    - Contact & Company management
    - AI Lead Scoring
    - Deal Pipeline
    - Activity Tracking
    - Email Generation
    """
    
    def __init__(self):
        self.ai_engine = CRMAIEngine()
        
        # In-memory storage
        self._contacts: Dict[str, Dict[str, Contact]] = {}
        self._companies: Dict[str, Dict[str, Company]] = {}
        self._deals: Dict[str, Dict[str, Deal]] = {}
        self._activities: Dict[str, Dict[str, Activity]] = {}
        
        logger.info("CRMAgent initialized")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # COMPANY OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_company(
        self,
        name: str,
        user_id: str,
        domain: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        annual_revenue: Optional[Decimal] = None,
        website: Optional[str] = None,
        **kwargs
    ) -> Company:
        """Create a company."""
        
        now = datetime.now(timezone.utc)
        
        company = Company(
            id=str(uuid.uuid4()),
            name=name,
            domain=domain,
            industry=industry,
            size=size,
            annual_revenue=annual_revenue,
            website=website,
            linkedin_url=kwargs.get("linkedin_url"),
            address=kwargs.get("address"),
            city=kwargs.get("city"),
            country=kwargs.get("country"),
            created_at=now,
            updated_at=now,
            user_id=user_id,
        )
        
        if user_id not in self._companies:
            self._companies[user_id] = {}
        self._companies[user_id][company.id] = company
        
        logger.info(f"Created company {company.id}: {name}")
        return company
    
    def get_company(self, company_id: str, user_id: str) -> Optional[Company]:
        """Get a company by ID."""
        return self._companies.get(user_id, {}).get(company_id)
    
    def list_companies(
        self,
        user_id: str,
        industry: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
    ) -> List[Company]:
        """List companies."""
        companies = list(self._companies.get(user_id, {}).values())
        
        if industry:
            companies = [c for c in companies if c.industry == industry]
        if search:
            search_lower = search.lower()
            companies = [c for c in companies if search_lower in c.name.lower()]
        
        return sorted(companies, key=lambda c: c.name)[:limit]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CONTACT OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def create_contact(
        self,
        first_name: str,
        last_name: str,
        email: str,
        user_id: str,
        phone: Optional[str] = None,
        title: Optional[str] = None,
        company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        lead_source: LeadSource = LeadSource.OTHER,
        tags: Optional[List[str]] = None,
        auto_score: bool = True,
        **kwargs
    ) -> Contact:
        """Create a contact with optional AI scoring."""
        
        now = datetime.now(timezone.utc)
        
        contact = Contact(
            id=str(uuid.uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            title=title,
            company_id=company_id,
            company_name=company_name,
            contact_type=ContactType.LEAD,
            lead_status=LeadStatus.NEW,
            lead_source=lead_source,
            lead_score=0,
            lead_score_breakdown={},
            last_contacted=None,
            last_activity=None,
            linkedin_url=kwargs.get("linkedin_url"),
            tags=tags or [],
            owner_id=user_id,
            created_at=now,
            updated_at=now,
            user_id=user_id,
        )
        
        # AI Scoring
        if auto_score:
            company = self.get_company(company_id, user_id) if company_id else None
            score_result = await self.ai_engine.score_lead(contact, company)
            contact.lead_score = score_result.total_score
            contact.lead_score_breakdown = score_result.breakdown
        
        if user_id not in self._contacts:
            self._contacts[user_id] = {}
        self._contacts[user_id][contact.id] = contact
        
        # Update company contact count
        if company_id:
            company = self.get_company(company_id, user_id)
            if company:
                company.contact_count += 1
        
        logger.info(f"Created contact {contact.id}: {first_name} {last_name}")
        return contact
    
    def get_contact(self, contact_id: str, user_id: str) -> Optional[Contact]:
        """Get a contact by ID."""
        return self._contacts.get(user_id, {}).get(contact_id)
    
    async def update_contact(
        self,
        contact_id: str,
        user_id: str,
        rescore: bool = False,
        **updates
    ) -> Optional[Contact]:
        """Update a contact."""
        
        contact = self.get_contact(contact_id, user_id)
        if not contact:
            return None
        
        for key, value in updates.items():
            if hasattr(contact, key) and value is not None:
                setattr(contact, key, value)
        
        contact.updated_at = datetime.now(timezone.utc)
        
        if rescore:
            company = self.get_company(contact.company_id, user_id) if contact.company_id else None
            score_result = await self.ai_engine.score_lead(contact, company)
            contact.lead_score = score_result.total_score
            contact.lead_score_breakdown = score_result.breakdown
        
        return contact
    
    def delete_contact(self, contact_id: str, user_id: str) -> bool:
        """Delete a contact."""
        contact = self.get_contact(contact_id, user_id)
        if not contact:
            return False
        
        del self._contacts[user_id][contact_id]
        logger.info(f"Deleted contact {contact_id}")
        return True
    
    def list_contacts(
        self,
        user_id: str,
        company_id: Optional[str] = None,
        lead_status: Optional[LeadStatus] = None,
        lead_source: Optional[LeadSource] = None,
        min_score: Optional[int] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: str = "lead_score",
        limit: int = 50,
    ) -> List[Contact]:
        """List contacts with filtering."""
        
        contacts = list(self._contacts.get(user_id, {}).values())
        
        if company_id:
            contacts = [c for c in contacts if c.company_id == company_id]
        if lead_status:
            contacts = [c for c in contacts if c.lead_status == lead_status]
        if lead_source:
            contacts = [c for c in contacts if c.lead_source == lead_source]
        if min_score is not None:
            contacts = [c for c in contacts if c.lead_score >= min_score]
        if tag:
            contacts = [c for c in contacts if tag in c.tags]
        if search:
            search_lower = search.lower()
            contacts = [c for c in contacts if 
                        search_lower in c.first_name.lower() or
                        search_lower in c.last_name.lower() or
                        search_lower in c.email.lower()]
        
        if sort_by == "lead_score":
            contacts = sorted(contacts, key=lambda c: c.lead_score, reverse=True)
        elif sort_by == "created_at":
            contacts = sorted(contacts, key=lambda c: c.created_at, reverse=True)
        elif sort_by == "name":
            contacts = sorted(contacts, key=lambda c: f"{c.first_name} {c.last_name}")
        
        return contacts[:limit]
    
    async def score_contact(self, contact_id: str, user_id: str) -> Optional[LeadScoreResult]:
        """Score a contact with AI."""
        
        contact = self.get_contact(contact_id, user_id)
        if not contact:
            return None
        
        company = self.get_company(contact.company_id, user_id) if contact.company_id else None
        result = await self.ai_engine.score_lead(contact, company)
        
        contact.lead_score = result.total_score
        contact.lead_score_breakdown = result.breakdown
        contact.updated_at = datetime.now(timezone.utc)
        
        return result
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DEAL OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def create_deal(
        self,
        name: str,
        contact_id: str,
        amount: Decimal,
        user_id: str,
        company_id: Optional[str] = None,
        stage: DealStage = DealStage.DISCOVERY,
        currency: str = "USD",
        expected_close_date: Optional[datetime] = None,
        **kwargs
    ) -> Deal:
        """Create a deal."""
        
        now = datetime.now(timezone.utc)
        
        # Calculate probability based on stage
        stage_probabilities = {
            DealStage.DISCOVERY: 10,
            DealStage.QUALIFICATION: 25,
            DealStage.PROPOSAL: 50,
            DealStage.NEGOTIATION: 75,
            DealStage.CLOSED_WON: 100,
            DealStage.CLOSED_LOST: 0,
        }
        
        deal = Deal(
            id=str(uuid.uuid4()),
            name=name,
            contact_id=contact_id,
            company_id=company_id,
            stage=stage,
            amount=amount,
            currency=currency,
            probability=stage_probabilities.get(stage, 25),
            expected_close_date=expected_close_date,
            actual_close_date=None,
            lost_reason=None,
            notes=kwargs.get("notes"),
            owner_id=user_id,
            created_at=now,
            updated_at=now,
            user_id=user_id,
        )
        
        if user_id not in self._deals:
            self._deals[user_id] = {}
        self._deals[user_id][deal.id] = deal
        
        # Update company deal count
        if company_id:
            company = self.get_company(company_id, user_id)
            if company:
                company.deal_count += 1
        
        logger.info(f"Created deal {deal.id}: {name} - ${amount}")
        return deal
    
    def get_deal(self, deal_id: str, user_id: str) -> Optional[Deal]:
        """Get a deal by ID."""
        return self._deals.get(user_id, {}).get(deal_id)
    
    def update_deal_stage(
        self,
        deal_id: str,
        user_id: str,
        stage: DealStage,
        lost_reason: Optional[str] = None,
    ) -> Optional[Deal]:
        """Update deal stage."""
        
        deal = self.get_deal(deal_id, user_id)
        if not deal:
            return None
        
        deal.stage = stage
        deal.updated_at = datetime.now(timezone.utc)
        
        # Update probability
        stage_probabilities = {
            DealStage.DISCOVERY: 10,
            DealStage.QUALIFICATION: 25,
            DealStage.PROPOSAL: 50,
            DealStage.NEGOTIATION: 75,
            DealStage.CLOSED_WON: 100,
            DealStage.CLOSED_LOST: 0,
        }
        deal.probability = stage_probabilities.get(stage, deal.probability)
        
        if stage in [DealStage.CLOSED_WON, DealStage.CLOSED_LOST]:
            deal.actual_close_date = datetime.now(timezone.utc)
            if stage == DealStage.CLOSED_LOST:
                deal.lost_reason = lost_reason
        
        return deal
    
    def list_deals(
        self,
        user_id: str,
        stage: Optional[DealStage] = None,
        contact_id: Optional[str] = None,
        company_id: Optional[str] = None,
        min_amount: Optional[Decimal] = None,
        limit: int = 50,
    ) -> List[Deal]:
        """List deals."""
        
        deals = list(self._deals.get(user_id, {}).values())
        
        if stage:
            deals = [d for d in deals if d.stage == stage]
        if contact_id:
            deals = [d for d in deals if d.contact_id == contact_id]
        if company_id:
            deals = [d for d in deals if d.company_id == company_id]
        if min_amount:
            deals = [d for d in deals if d.amount >= min_amount]
        
        return sorted(deals, key=lambda d: d.amount, reverse=True)[:limit]
    
    def get_pipeline_summary(self, user_id: str) -> Dict[str, Any]:
        """Get pipeline summary."""
        
        deals = list(self._deals.get(user_id, {}).values())
        
        by_stage = {}
        total_value = Decimal(0)
        weighted_value = Decimal(0)
        
        for deal in deals:
            if deal.stage not in [DealStage.CLOSED_WON, DealStage.CLOSED_LOST]:
                stage_name = deal.stage.value
                if stage_name not in by_stage:
                    by_stage[stage_name] = {"count": 0, "value": Decimal(0)}
                by_stage[stage_name]["count"] += 1
                by_stage[stage_name]["value"] += deal.amount
                total_value += deal.amount
                weighted_value += deal.amount * Decimal(deal.probability / 100)
        
        won_deals = [d for d in deals if d.stage == DealStage.CLOSED_WON]
        lost_deals = [d for d in deals if d.stage == DealStage.CLOSED_LOST]
        
        return {
            "by_stage": {k: {"count": v["count"], "value": float(v["value"])} for k, v in by_stage.items()},
            "total_pipeline_value": float(total_value),
            "weighted_pipeline_value": float(weighted_value),
            "open_deals": len(deals) - len(won_deals) - len(lost_deals),
            "won_deals": len(won_deals),
            "won_value": float(sum(d.amount for d in won_deals)),
            "lost_deals": len(lost_deals),
            "win_rate": round(len(won_deals) / max(1, len(won_deals) + len(lost_deals)) * 100, 1),
        }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ACTIVITY OPERATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def log_activity(
        self,
        activity_type: ActivityType,
        subject: str,
        user_id: str,
        contact_id: Optional[str] = None,
        company_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        description: Optional[str] = None,
        scheduled_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        duration_minutes: Optional[int] = None,
        outcome: Optional[str] = None,
    ) -> Activity:
        """Log an activity."""
        
        activity = Activity(
            id=str(uuid.uuid4()),
            activity_type=activity_type,
            subject=subject,
            description=description,
            contact_id=contact_id,
            company_id=company_id,
            deal_id=deal_id,
            scheduled_at=scheduled_at,
            completed_at=completed_at,
            duration_minutes=duration_minutes,
            outcome=outcome,
            created_at=datetime.now(timezone.utc),
            user_id=user_id,
        )
        
        if user_id not in self._activities:
            self._activities[user_id] = {}
        self._activities[user_id][activity.id] = activity
        
        # Update contact last activity
        if contact_id:
            contact = self.get_contact(contact_id, user_id)
            if contact:
                contact.last_activity = datetime.now(timezone.utc)
                if activity_type in [ActivityType.EMAIL, ActivityType.CALL]:
                    contact.last_contacted = datetime.now(timezone.utc)
        
        logger.info(f"Logged activity {activity.id}: {activity_type.value} - {subject}")
        return activity
    
    def list_activities(
        self,
        user_id: str,
        contact_id: Optional[str] = None,
        company_id: Optional[str] = None,
        deal_id: Optional[str] = None,
        activity_type: Optional[ActivityType] = None,
        limit: int = 50,
    ) -> List[Activity]:
        """List activities."""
        
        activities = list(self._activities.get(user_id, {}).values())
        
        if contact_id:
            activities = [a for a in activities if a.contact_id == contact_id]
        if company_id:
            activities = [a for a in activities if a.company_id == company_id]
        if deal_id:
            activities = [a for a in activities if a.deal_id == deal_id]
        if activity_type:
            activities = [a for a in activities if a.activity_type == activity_type]
        
        return sorted(activities, key=lambda a: a.created_at, reverse=True)[:limit]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EMAIL GENERATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    async def generate_email(
        self,
        contact_id: str,
        user_id: str,
        purpose: str = "follow_up",
    ) -> Optional[EmailDraft]:
        """Generate email draft for a contact."""
        
        contact = self.get_contact(contact_id, user_id)
        if not contact:
            return None
        
        company = self.get_company(contact.company_id, user_id) if contact.company_id else None
        
        return await self.ai_engine.generate_email_draft(contact, purpose, company)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STATISTICS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_stats(self, user_id: str) -> Dict[str, Any]:
        """Get CRM statistics."""
        
        contacts = list(self._contacts.get(user_id, {}).values())
        companies = list(self._companies.get(user_id, {}).values())
        deals = list(self._deals.get(user_id, {}).values())
        activities = list(self._activities.get(user_id, {}).values())
        
        # Lead score distribution
        hot_leads = [c for c in contacts if c.lead_score >= 70]
        warm_leads = [c for c in contacts if 40 <= c.lead_score < 70]
        cold_leads = [c for c in contacts if c.lead_score < 40]
        
        return {
            "contacts": {
                "total": len(contacts),
                "hot_leads": len(hot_leads),
                "warm_leads": len(warm_leads),
                "cold_leads": len(cold_leads),
                "avg_lead_score": round(sum(c.lead_score for c in contacts) / max(1, len(contacts)), 1),
            },
            "companies": {
                "total": len(companies),
            },
            "deals": self.get_pipeline_summary(user_id),
            "activities": {
                "total": len(activities),
                "this_week": len([a for a in activities if a.created_at > datetime.now(timezone.utc) - timedelta(days=7)]),
            },
        }


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_crm_agent: Optional[CRMAgent] = None


def get_crm_agent() -> CRMAgent:
    """Get or create the CRM agent."""
    global _crm_agent
    if _crm_agent is None:
        _crm_agent = CRMAgent()
    return _crm_agent


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import asyncio
    
    print("✅ CHE·NU Business CRM Agent")
    print("=" * 60)
    
    agent = get_crm_agent()
    
    async def test():
        # Create company
        company = agent.create_company(
            name="TechCorp Inc",
            user_id="test_user",
            industry="Technology",
            size="51-200",
            annual_revenue=Decimal("5000000"),
        )
        print(f"\n✅ Created company: {company.name}")
        
        # Create contact
        contact = await agent.create_contact(
            first_name="John",
            last_name="Smith",
            email="john@techcorp.com",
            user_id="test_user",
            title="VP of Engineering",
            company_id=company.id,
            lead_source=LeadSource.LINKEDIN,
        )
        print(f"✅ Created contact: {contact.first_name} {contact.last_name}")
        print(f"   Lead Score: {contact.lead_score}/100")
        
        # Create deal
        deal = agent.create_deal(
            name="TechCorp Enterprise License",
            contact_id=contact.id,
            company_id=company.id,
            amount=Decimal("50000"),
            user_id="test_user",
            stage=DealStage.PROPOSAL,
        )
        print(f"✅ Created deal: {deal.name} - ${deal.amount}")
        
        # Log activity
        activity = agent.log_activity(
            activity_type=ActivityType.CALL,
            subject="Discovery call",
            user_id="test_user",
            contact_id=contact.id,
            duration_minutes=30,
            outcome="Positive - scheduled demo",
        )
        print(f"✅ Logged activity: {activity.subject}")
        
        # Stats
        stats = agent.get_stats("test_user")
        print(f"\n📊 Stats:")
        print(f"   Contacts: {stats['contacts']['total']}")
        print(f"   Hot Leads: {stats['contacts']['hot_leads']}")
        print(f"   Pipeline Value: ${stats['deals']['total_pipeline_value']}")
    
    asyncio.run(test())
    
    print("\n✅ CRM Agent ready!")
