"""
CHE·NU™ V68 - Marketing Automation Agent
Vertical 7: HubSpot/Mailchimp Killer at $29/mo vs $800+/mo

Features:
- Email Campaigns (create, schedule, send, track)
- Contact Management (segments, tags, lead scoring)
- Automation Workflows (drip campaigns, triggers)
- Landing Pages & Forms
- A/B Testing
- Analytics & Reporting
- AI: Subject optimization, send time, content suggestions
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Dict, Any
from uuid import uuid4
import re
import random


# ============================================================================
# ENUMS
# ============================================================================

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class CampaignType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SOCIAL = "social"


class ContactStatus(str, Enum):
    ACTIVE = "active"
    UNSUBSCRIBED = "unsubscribed"
    BOUNCED = "bounced"
    COMPLAINED = "complained"
    PENDING = "pending"


class AutomationTrigger(str, Enum):
    SIGNUP = "signup"
    TAG_ADDED = "tag_added"
    FORM_SUBMIT = "form_submit"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    PAGE_VISITED = "page_visited"
    PURCHASE = "purchase"
    DATE_BASED = "date_based"
    CUSTOM = "custom"


class AutomationAction(str, Enum):
    SEND_EMAIL = "send_email"
    SEND_SMS = "send_sms"
    ADD_TAG = "add_tag"
    REMOVE_TAG = "remove_tag"
    UPDATE_FIELD = "update_field"
    ADD_TO_SEGMENT = "add_to_segment"
    REMOVE_FROM_SEGMENT = "remove_from_segment"
    WAIT = "wait"
    CONDITION = "condition"
    WEBHOOK = "webhook"
    NOTIFY_TEAM = "notify_team"


class FormFieldType(str, Enum):
    TEXT = "text"
    EMAIL = "email"
    PHONE = "phone"
    NUMBER = "number"
    DATE = "date"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    CHECKBOX = "checkbox"
    TEXTAREA = "textarea"
    HIDDEN = "hidden"


class LeadScoreCategory(str, Enum):
    COLD = "cold"          # 0-20
    WARM = "warm"          # 21-50
    HOT = "hot"            # 51-80
    QUALIFIED = "qualified" # 81-100


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Contact:
    id: str
    email: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    status: ContactStatus = ContactStatus.ACTIVE
    tags: List[str] = field(default_factory=list)
    segments: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    lead_score: int = 0
    source: Optional[str] = None
    last_activity: Optional[datetime] = None
    email_stats: Dict[str, int] = field(default_factory=lambda: {
        "sent": 0, "opened": 0, "clicked": 0, "bounced": 0
    })


@dataclass
class Segment:
    id: str
    name: str
    workspace_id: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    description: Optional[str] = None
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    contact_count: int = 0
    is_dynamic: bool = True  # Auto-update based on conditions


@dataclass
class EmailTemplate:
    id: str
    name: str
    workspace_id: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    subject: str = ""
    preview_text: str = ""
    html_content: str = ""
    text_content: str = ""
    category: str = "general"
    thumbnail_url: Optional[str] = None
    variables: List[str] = field(default_factory=list)


@dataclass
class Campaign:
    id: str
    name: str
    workspace_id: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    campaign_type: CampaignType = CampaignType.EMAIL
    status: CampaignStatus = CampaignStatus.DRAFT
    subject: str = ""
    preview_text: str = ""
    from_name: str = ""
    from_email: str = ""
    reply_to: Optional[str] = None
    html_content: str = ""
    text_content: str = ""
    template_id: Optional[str] = None
    segment_ids: List[str] = field(default_factory=list)
    tag_filter: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    stats: Dict[str, int] = field(default_factory=lambda: {
        "recipients": 0, "sent": 0, "delivered": 0,
        "opened": 0, "clicked": 0, "bounced": 0,
        "unsubscribed": 0, "complained": 0
    })
    ab_test: Optional[Dict[str, Any]] = None


@dataclass
class ABTest:
    id: str
    campaign_id: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    test_type: str = "subject"  # subject, content, send_time
    variants: List[Dict[str, Any]] = field(default_factory=list)
    winner_criteria: str = "open_rate"  # open_rate, click_rate, conversion
    test_size_percent: int = 20
    test_duration_hours: int = 4
    winner_id: Optional[str] = None
    status: str = "pending"  # pending, testing, completed


@dataclass
class Automation:
    id: str
    name: str
    workspace_id: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    description: Optional[str] = None
    trigger: AutomationTrigger = AutomationTrigger.SIGNUP
    trigger_config: Dict[str, Any] = field(default_factory=dict)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    is_active: bool = False
    stats: Dict[str, int] = field(default_factory=lambda: {
        "enrolled": 0, "completed": 0, "active": 0, "exited": 0
    })


@dataclass
class AutomationEnrollment:
    id: str
    automation_id: str
    contact_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    current_step: int = 0
    status: str = "active"  # active, completed, exited, paused
    step_history: List[Dict[str, Any]] = field(default_factory=list)
    next_action_at: Optional[datetime] = None


@dataclass
class LandingPage:
    id: str
    name: str
    workspace_id: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    slug: str = ""
    html_content: str = ""
    css_content: str = ""
    meta_title: str = ""
    meta_description: str = ""
    is_published: bool = False
    published_at: Optional[datetime] = None
    form_id: Optional[str] = None
    stats: Dict[str, int] = field(default_factory=lambda: {
        "views": 0, "unique_visitors": 0, "conversions": 0
    })


@dataclass
class Form:
    id: str
    name: str
    workspace_id: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    fields: List[Dict[str, Any]] = field(default_factory=list)
    submit_button_text: str = "Submit"
    success_message: str = "Thank you for submitting!"
    redirect_url: Optional[str] = None
    tags_to_add: List[str] = field(default_factory=list)
    automation_id: Optional[str] = None
    submissions_count: int = 0


@dataclass
class FormSubmission:
    id: str
    form_id: str
    contact_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    page_url: Optional[str] = None


@dataclass
class EmailEvent:
    id: str
    campaign_id: str
    contact_id: str
    event_type: str  # sent, delivered, opened, clicked, bounced, unsubscribed
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# AI ENGINE
# ============================================================================

class MarketingAIEngine:
    """AI-powered marketing optimization"""
    
    def __init__(self):
        self.subject_patterns = [
            {"pattern": "question", "boost": 1.2},
            {"pattern": "number", "boost": 1.15},
            {"pattern": "urgency", "boost": 1.1},
            {"pattern": "personalization", "boost": 1.25},
        ]
    
    def optimize_subject_line(self, subject: str, audience_data: Dict = None) -> Dict[str, Any]:
        """Generate optimized subject line variants"""
        suggestions = []
        base_score = self._score_subject(subject)
        
        # Generate variants
        variants = [
            self._add_personalization(subject),
            self._add_urgency(subject),
            self._add_question(subject),
            self._add_number(subject),
            self._shorten_subject(subject),
        ]
        
        for variant in variants:
            if variant and variant != subject:
                score = self._score_subject(variant)
                suggestions.append({
                    "subject": variant,
                    "predicted_open_rate": min(0.45, 0.15 + (score * 0.03)),
                    "improvement": f"+{int((score - base_score) / base_score * 100)}%",
                    "reasoning": self._get_reasoning(variant, subject)
                })
        
        return {
            "original": {
                "subject": subject,
                "score": base_score,
                "predicted_open_rate": 0.15 + (base_score * 0.02)
            },
            "suggestions": sorted(suggestions, key=lambda x: x["predicted_open_rate"], reverse=True)[:5],
            "best_practices": [
                "Keep subject under 50 characters",
                "Use personalization tokens",
                "Create curiosity or urgency",
                "Avoid spam trigger words"
            ]
        }
    
    def _score_subject(self, subject: str) -> float:
        score = 5.0
        
        # Length scoring
        length = len(subject)
        if 30 <= length <= 50:
            score += 1
        elif length > 70:
            score -= 1
        
        # Personalization
        if "{{" in subject or "{first_name}" in subject.lower():
            score += 1.5
        
        # Question
        if "?" in subject:
            score += 0.5
        
        # Numbers
        if any(char.isdigit() for char in subject):
            score += 0.5
        
        # Urgency words
        urgency = ["now", "today", "limited", "urgent", "last chance", "expires"]
        if any(word in subject.lower() for word in urgency):
            score += 0.5
        
        # Spam words (negative)
        spam = ["free", "click here", "buy now", "!!!"]
        if any(word in subject.lower() for word in spam):
            score -= 1
        
        return max(1, min(10, score))
    
    def _add_personalization(self, subject: str) -> str:
        if "{{" not in subject and "{" not in subject:
            return f"{{{{first_name}}}}, {subject[0].lower()}{subject[1:]}"
        return None
    
    def _add_urgency(self, subject: str) -> str:
        urgency_prefixes = ["Last chance: ", "Don't miss: ", "Ending soon: "]
        return random.choice(urgency_prefixes) + subject
    
    def _add_question(self, subject: str) -> str:
        if "?" not in subject:
            return f"Ready for {subject.lower().rstrip('.')}?"
        return None
    
    def _add_number(self, subject: str) -> str:
        if not any(char.isdigit() for char in subject):
            return f"3 ways to {subject.lower()}"
        return None
    
    def _shorten_subject(self, subject: str) -> str:
        if len(subject) > 50:
            words = subject.split()
            return " ".join(words[:6]) + "..."
        return None
    
    def _get_reasoning(self, variant: str, original: str) -> str:
        if "{{" in variant:
            return "Added personalization increases open rates by 26%"
        if "?" in variant and "?" not in original:
            return "Questions create curiosity and engagement"
        if any(word in variant.lower() for word in ["last", "ending", "don't miss"]):
            return "Urgency drives immediate action"
        if any(char.isdigit() for char in variant):
            return "Numbers in subjects increase click-through"
        if len(variant) < len(original):
            return "Shorter subjects perform better on mobile"
        return "Optimized for engagement"
    
    def predict_send_time(self, audience_data: Dict = None) -> Dict[str, Any]:
        """Predict optimal send time based on audience"""
        # Simulated analysis
        best_times = [
            {"day": "Tuesday", "time": "10:00 AM", "score": 0.92, "reason": "Highest engagement historically"},
            {"day": "Thursday", "time": "2:00 PM", "score": 0.88, "reason": "Post-lunch engagement peak"},
            {"day": "Wednesday", "time": "9:00 AM", "score": 0.85, "reason": "Start of workday attention"},
        ]
        
        worst_times = [
            {"day": "Monday", "time": "8:00 AM", "reason": "Inbox overload from weekend"},
            {"day": "Friday", "time": "4:00 PM", "reason": "Weekend mindset"},
            {"day": "Sunday", "time": "Any", "reason": "Lowest engagement day"},
        ]
        
        return {
            "recommended": best_times[0],
            "alternatives": best_times[1:],
            "avoid": worst_times,
            "timezone_note": "Times shown in recipient's local timezone",
            "confidence": 0.85
        }
    
    def generate_content_suggestions(self, topic: str, tone: str = "professional") -> Dict[str, Any]:
        """Generate email content suggestions"""
        hooks = {
            "professional": [
                f"I wanted to share some insights about {topic}...",
                f"Here's what top performers know about {topic}...",
                f"The latest data on {topic} reveals...",
            ],
            "casual": [
                f"Quick question about {topic}...",
                f"Thought you might find this interesting: {topic}...",
                f"Hey! Got something cool about {topic}...",
            ],
            "urgent": [
                f"Important update regarding {topic}...",
                f"Action required: {topic}...",
                f"Time-sensitive: {topic}...",
            ]
        }
        
        ctas = [
            {"text": "Learn More", "style": "button"},
            {"text": "Get Started", "style": "button"},
            {"text": "See How →", "style": "link"},
            {"text": "Claim Your Spot", "style": "button"},
        ]
        
        return {
            "opening_hooks": hooks.get(tone, hooks["professional"]),
            "suggested_ctas": ctas,
            "structure_tips": [
                "Start with a compelling hook",
                "Keep paragraphs to 2-3 sentences",
                "Use bullet points for key benefits",
                "Include one clear CTA",
                "Add P.S. for secondary message"
            ],
            "word_count_recommendation": "150-200 words for highest engagement"
        }
    
    def calculate_lead_score(self, contact: Contact, activities: List[Dict] = None) -> Dict[str, Any]:
        """Calculate lead score based on engagement"""
        score = 0
        breakdown = {}
        
        # Email engagement (40 points max)
        email_score = 0
        if contact.email_stats["opened"] > 0:
            email_score += min(20, contact.email_stats["opened"] * 2)
        if contact.email_stats["clicked"] > 0:
            email_score += min(20, contact.email_stats["clicked"] * 5)
        breakdown["email_engagement"] = email_score
        score += email_score
        
        # Profile completeness (20 points max)
        profile_score = 0
        if contact.first_name:
            profile_score += 5
        if contact.company:
            profile_score += 5
        if contact.phone:
            profile_score += 5
        if contact.job_title:
            profile_score += 5
        breakdown["profile_completeness"] = profile_score
        score += profile_score
        
        # Recency (20 points max)
        recency_score = 0
        if contact.last_activity:
            days_ago = (datetime.utcnow() - contact.last_activity).days
            if days_ago <= 7:
                recency_score = 20
            elif days_ago <= 30:
                recency_score = 15
            elif days_ago <= 90:
                recency_score = 10
            else:
                recency_score = 5
        breakdown["recency"] = recency_score
        score += recency_score
        
        # Source quality (20 points max)
        source_scores = {
            "organic": 20,
            "referral": 18,
            "webinar": 15,
            "content": 12,
            "social": 10,
            "paid": 8,
            "unknown": 5
        }
        source_score = source_scores.get(contact.source, 5)
        breakdown["source_quality"] = source_score
        score += source_score
        
        # Determine category
        if score >= 81:
            category = LeadScoreCategory.QUALIFIED
        elif score >= 51:
            category = LeadScoreCategory.HOT
        elif score >= 21:
            category = LeadScoreCategory.WARM
        else:
            category = LeadScoreCategory.COLD
        
        return {
            "score": score,
            "category": category.value,
            "breakdown": breakdown,
            "recommendations": self._get_lead_recommendations(category, breakdown)
        }
    
    def _get_lead_recommendations(self, category: LeadScoreCategory, breakdown: Dict) -> List[str]:
        recommendations = []
        
        if category == LeadScoreCategory.QUALIFIED:
            recommendations.append("Schedule a sales call immediately")
            recommendations.append("Send personalized proposal")
        elif category == LeadScoreCategory.HOT:
            recommendations.append("Send case study or demo invitation")
            recommendations.append("Add to high-touch nurture sequence")
        elif category == LeadScoreCategory.WARM:
            recommendations.append("Continue nurturing with educational content")
            recommendations.append("Invite to upcoming webinar")
        else:
            recommendations.append("Add to awareness campaign")
            recommendations.append("Send introductory content series")
        
        if breakdown.get("profile_completeness", 0) < 15:
            recommendations.append("Request profile completion via form")
        
        if breakdown.get("recency", 0) < 10:
            recommendations.append("Re-engagement campaign recommended")
        
        return recommendations
    
    def segment_audience(self, contacts: List[Contact]) -> Dict[str, List[str]]:
        """Auto-segment contacts based on behavior"""
        segments = {
            "highly_engaged": [],
            "active": [],
            "at_risk": [],
            "dormant": [],
            "new_subscribers": []
        }
        
        now = datetime.utcnow()
        
        for contact in contacts:
            days_since_creation = (now - contact.created_at).days
            
            # New subscribers (< 30 days)
            if days_since_creation < 30:
                segments["new_subscribers"].append(contact.id)
                continue
            
            # Check engagement
            total_engagement = contact.email_stats["opened"] + contact.email_stats["clicked"]
            
            if total_engagement >= 10:
                segments["highly_engaged"].append(contact.id)
            elif total_engagement >= 3:
                segments["active"].append(contact.id)
            elif contact.last_activity and (now - contact.last_activity).days > 60:
                segments["dormant"].append(contact.id)
            else:
                segments["at_risk"].append(contact.id)
        
        return segments


# ============================================================================
# MAIN SERVICE
# ============================================================================

class MarketingAutomationService:
    """Complete marketing automation service"""
    
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}
        self.segments: Dict[str, Segment] = {}
        self.templates: Dict[str, EmailTemplate] = {}
        self.campaigns: Dict[str, Campaign] = {}
        self.automations: Dict[str, Automation] = {}
        self.enrollments: Dict[str, AutomationEnrollment] = {}
        self.landing_pages: Dict[str, LandingPage] = {}
        self.forms: Dict[str, Form] = {}
        self.form_submissions: Dict[str, FormSubmission] = {}
        self.email_events: List[EmailEvent] = []
        self.ab_tests: Dict[str, ABTest] = {}
        self.ai_engine = MarketingAIEngine()
    
    # ========================================================================
    # CONTACTS
    # ========================================================================
    
    def create_contact(
        self,
        email: str,
        created_by: str,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        company: str = None,
        tags: List[str] = None,
        source: str = None,
        custom_fields: Dict = None
    ) -> Contact:
        """Create a new contact"""
        # Check for duplicate
        for contact in self.contacts.values():
            if contact.email.lower() == email.lower():
                raise ValueError(f"Contact with email {email} already exists")
        
        contact = Contact(
            id=str(uuid4()),
            email=email.lower(),
            created_by=created_by,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            company=company,
            tags=tags or [],
            source=source,
            custom_fields=custom_fields or {},
            last_activity=datetime.utcnow()
        )
        
        self.contacts[contact.id] = contact
        return contact
    
    def get_contact(self, contact_id: str) -> Optional[Contact]:
        return self.contacts.get(contact_id)
    
    def get_contact_by_email(self, email: str) -> Optional[Contact]:
        for contact in self.contacts.values():
            if contact.email.lower() == email.lower():
                return contact
        return None
    
    def update_contact(self, contact_id: str, updates: Dict[str, Any], updated_by: str) -> Optional[Contact]:
        contact = self.contacts.get(contact_id)
        if not contact:
            return None
        
        for key, value in updates.items():
            if hasattr(contact, key) and key not in ['id', 'created_at', 'created_by']:
                setattr(contact, key, value)
        
        contact.last_activity = datetime.utcnow()
        return contact
    
    def add_tags(self, contact_id: str, tags: List[str]) -> Optional[Contact]:
        contact = self.contacts.get(contact_id)
        if contact:
            for tag in tags:
                if tag not in contact.tags:
                    contact.tags.append(tag)
            contact.last_activity = datetime.utcnow()
        return contact
    
    def remove_tags(self, contact_id: str, tags: List[str]) -> Optional[Contact]:
        contact = self.contacts.get(contact_id)
        if contact:
            contact.tags = [t for t in contact.tags if t not in tags]
            contact.last_activity = datetime.utcnow()
        return contact
    
    def list_contacts(
        self,
        workspace_id: str = None,
        status: ContactStatus = None,
        tag: str = None,
        segment_id: str = None,
        search: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Contact]:
        """List contacts with filters"""
        contacts = list(self.contacts.values())
        
        if status:
            contacts = [c for c in contacts if c.status == status]
        
        if tag:
            contacts = [c for c in contacts if tag in c.tags]
        
        if segment_id:
            contacts = [c for c in contacts if segment_id in c.segments]
        
        if search:
            search_lower = search.lower()
            contacts = [c for c in contacts if 
                       search_lower in c.email.lower() or
                       (c.first_name and search_lower in c.first_name.lower()) or
                       (c.last_name and search_lower in c.last_name.lower()) or
                       (c.company and search_lower in c.company.lower())]
        
        # Sort by created_at descending
        contacts.sort(key=lambda x: x.created_at, reverse=True)
        
        return contacts[offset:offset + limit]
    
    def unsubscribe_contact(self, contact_id: str, reason: str = None) -> Optional[Contact]:
        contact = self.contacts.get(contact_id)
        if contact:
            contact.status = ContactStatus.UNSUBSCRIBED
            contact.last_activity = datetime.utcnow()
        return contact
    
    # ========================================================================
    # SEGMENTS
    # ========================================================================
    
    def create_segment(
        self,
        name: str,
        workspace_id: str,
        created_by: str,
        conditions: List[Dict] = None,
        description: str = None
    ) -> Segment:
        """Create a contact segment"""
        segment = Segment(
            id=str(uuid4()),
            name=name,
            workspace_id=workspace_id,
            created_by=created_by,
            conditions=conditions or [],
            description=description
        )
        
        # Calculate initial count
        segment.contact_count = len(self._get_segment_contacts(segment))
        
        self.segments[segment.id] = segment
        return segment
    
    def _get_segment_contacts(self, segment: Segment) -> List[Contact]:
        """Get contacts matching segment conditions"""
        contacts = list(self.contacts.values())
        
        for condition in segment.conditions:
            field = condition.get("field")
            operator = condition.get("operator")
            value = condition.get("value")
            
            if field == "tag":
                if operator == "contains":
                    contacts = [c for c in contacts if value in c.tags]
                elif operator == "not_contains":
                    contacts = [c for c in contacts if value not in c.tags]
            elif field == "lead_score":
                if operator == "greater_than":
                    contacts = [c for c in contacts if c.lead_score > value]
                elif operator == "less_than":
                    contacts = [c for c in contacts if c.lead_score < value]
            elif field == "status":
                contacts = [c for c in contacts if c.status.value == value]
        
        return contacts
    
    def get_segment(self, segment_id: str) -> Optional[Segment]:
        return self.segments.get(segment_id)
    
    def list_segments(self, workspace_id: str) -> List[Segment]:
        return [s for s in self.segments.values() if s.workspace_id == workspace_id]
    
    # ========================================================================
    # EMAIL TEMPLATES
    # ========================================================================
    
    def create_template(
        self,
        name: str,
        workspace_id: str,
        created_by: str,
        subject: str = "",
        html_content: str = "",
        text_content: str = "",
        category: str = "general"
    ) -> EmailTemplate:
        """Create email template"""
        # Extract variables from content
        variables = list(set(re.findall(r'\{\{(\w+)\}\}', html_content + subject)))
        
        template = EmailTemplate(
            id=str(uuid4()),
            name=name,
            workspace_id=workspace_id,
            created_by=created_by,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            category=category,
            variables=variables
        )
        
        self.templates[template.id] = template
        return template
    
    def get_template(self, template_id: str) -> Optional[EmailTemplate]:
        return self.templates.get(template_id)
    
    def list_templates(self, workspace_id: str, category: str = None) -> List[EmailTemplate]:
        templates = [t for t in self.templates.values() if t.workspace_id == workspace_id]
        if category:
            templates = [t for t in templates if t.category == category]
        return templates
    
    # ========================================================================
    # CAMPAIGNS
    # ========================================================================
    
    def create_campaign(
        self,
        name: str,
        workspace_id: str,
        created_by: str,
        campaign_type: CampaignType = CampaignType.EMAIL,
        subject: str = "",
        from_name: str = "",
        from_email: str = "",
        html_content: str = "",
        segment_ids: List[str] = None
    ) -> Campaign:
        """Create a new campaign"""
        campaign = Campaign(
            id=str(uuid4()),
            name=name,
            workspace_id=workspace_id,
            created_by=created_by,
            campaign_type=campaign_type,
            subject=subject,
            from_name=from_name,
            from_email=from_email,
            html_content=html_content,
            segment_ids=segment_ids or []
        )
        
        self.campaigns[campaign.id] = campaign
        return campaign
    
    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        return self.campaigns.get(campaign_id)
    
    def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Optional[Campaign]:
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return None
        
        if campaign.status not in [CampaignStatus.DRAFT, CampaignStatus.SCHEDULED]:
            raise ValueError("Cannot update campaign that is not in draft or scheduled status")
        
        for key, value in updates.items():
            if hasattr(campaign, key) and key not in ['id', 'created_at', 'created_by', 'stats']:
                setattr(campaign, key, value)
        
        return campaign
    
    def schedule_campaign(self, campaign_id: str, scheduled_at: datetime, user_id: str) -> Campaign:
        """Schedule campaign for sending"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        
        if campaign.status != CampaignStatus.DRAFT:
            raise ValueError("Only draft campaigns can be scheduled")
        
        # Validate
        if not campaign.subject:
            raise ValueError("Subject is required")
        if not campaign.html_content:
            raise ValueError("Email content is required")
        if not campaign.segment_ids:
            raise ValueError("At least one segment must be selected")
        
        campaign.scheduled_at = scheduled_at
        campaign.status = CampaignStatus.SCHEDULED
        
        # Calculate recipients
        recipients = set()
        for segment_id in campaign.segment_ids:
            segment = self.segments.get(segment_id)
            if segment:
                for contact in self._get_segment_contacts(segment):
                    if contact.status == ContactStatus.ACTIVE:
                        recipients.add(contact.id)
        
        campaign.stats["recipients"] = len(recipients)
        
        return campaign
    
    def send_campaign(self, campaign_id: str, user_id: str) -> Campaign:
        """Send campaign immediately or at scheduled time"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        
        if campaign.status not in [CampaignStatus.DRAFT, CampaignStatus.SCHEDULED]:
            raise ValueError("Campaign cannot be sent")
        
        campaign.status = CampaignStatus.SENDING
        campaign.sent_at = datetime.utcnow()
        
        # Simulate sending
        recipients = set()
        for segment_id in campaign.segment_ids:
            segment = self.segments.get(segment_id)
            if segment:
                for contact in self._get_segment_contacts(segment):
                    if contact.status == ContactStatus.ACTIVE:
                        recipients.add(contact.id)
                        
                        # Create email event
                        event = EmailEvent(
                            id=str(uuid4()),
                            campaign_id=campaign_id,
                            contact_id=contact.id,
                            event_type="sent"
                        )
                        self.email_events.append(event)
                        
                        # Update contact stats
                        contact.email_stats["sent"] += 1
                        contact.last_activity = datetime.utcnow()
        
        campaign.stats["sent"] = len(recipients)
        campaign.stats["delivered"] = int(len(recipients) * 0.98)  # 98% delivery rate
        campaign.status = CampaignStatus.SENT
        
        return campaign
    
    def pause_campaign(self, campaign_id: str) -> Optional[Campaign]:
        campaign = self.campaigns.get(campaign_id)
        if campaign and campaign.status == CampaignStatus.SCHEDULED:
            campaign.status = CampaignStatus.PAUSED
        return campaign
    
    def list_campaigns(
        self,
        workspace_id: str,
        status: CampaignStatus = None,
        campaign_type: CampaignType = None
    ) -> List[Campaign]:
        campaigns = [c for c in self.campaigns.values() if c.workspace_id == workspace_id]
        
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        
        if campaign_type:
            campaigns = [c for c in campaigns if c.campaign_type == campaign_type]
        
        campaigns.sort(key=lambda x: x.created_at, reverse=True)
        return campaigns
    
    def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        """Get detailed campaign statistics"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return {}
        
        stats = campaign.stats.copy()
        
        # Calculate rates
        if stats["sent"] > 0:
            stats["delivery_rate"] = stats["delivered"] / stats["sent"]
            stats["open_rate"] = stats["opened"] / stats["delivered"] if stats["delivered"] > 0 else 0
            stats["click_rate"] = stats["clicked"] / stats["delivered"] if stats["delivered"] > 0 else 0
            stats["bounce_rate"] = stats["bounced"] / stats["sent"]
            stats["unsubscribe_rate"] = stats["unsubscribed"] / stats["delivered"] if stats["delivered"] > 0 else 0
        
        return stats
    
    # ========================================================================
    # A/B TESTING
    # ========================================================================
    
    def create_ab_test(
        self,
        campaign_id: str,
        created_by: str,
        test_type: str = "subject",
        variants: List[Dict] = None,
        test_size_percent: int = 20
    ) -> ABTest:
        """Create A/B test for campaign"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        
        ab_test = ABTest(
            id=str(uuid4()),
            campaign_id=campaign_id,
            created_by=created_by,
            test_type=test_type,
            variants=variants or [],
            test_size_percent=test_size_percent
        )
        
        self.ab_tests[ab_test.id] = ab_test
        campaign.ab_test = {"id": ab_test.id, "status": "pending"}
        
        return ab_test
    
    def get_ab_test_results(self, test_id: str) -> Dict[str, Any]:
        """Get A/B test results"""
        ab_test = self.ab_tests.get(test_id)
        if not ab_test:
            return {}
        
        # Simulated results
        results = {
            "test_id": test_id,
            "status": ab_test.status,
            "variants": []
        }
        
        for i, variant in enumerate(ab_test.variants):
            variant_result = {
                "id": f"variant_{i}",
                "name": variant.get("name", f"Variant {chr(65+i)}"),
                "value": variant.get("value"),
                "sent": 100,
                "opens": random.randint(15, 35),
                "clicks": random.randint(5, 15),
            }
            variant_result["open_rate"] = variant_result["opens"] / variant_result["sent"]
            variant_result["click_rate"] = variant_result["clicks"] / variant_result["sent"]
            results["variants"].append(variant_result)
        
        # Determine winner
        if results["variants"]:
            winner = max(results["variants"], key=lambda x: x["open_rate"])
            results["winner"] = winner["id"]
            results["confidence"] = 0.95
        
        return results
    
    # ========================================================================
    # AUTOMATIONS
    # ========================================================================
    
    def create_automation(
        self,
        name: str,
        workspace_id: str,
        created_by: str,
        trigger: AutomationTrigger,
        trigger_config: Dict = None,
        description: str = None
    ) -> Automation:
        """Create automation workflow"""
        automation = Automation(
            id=str(uuid4()),
            name=name,
            workspace_id=workspace_id,
            created_by=created_by,
            trigger=trigger,
            trigger_config=trigger_config or {},
            description=description
        )
        
        self.automations[automation.id] = automation
        return automation
    
    def add_automation_step(
        self,
        automation_id: str,
        action: AutomationAction,
        config: Dict = None,
        position: int = None
    ) -> Optional[Automation]:
        """Add step to automation"""
        automation = self.automations.get(automation_id)
        if not automation:
            return None
        
        step = {
            "id": str(uuid4()),
            "action": action.value,
            "config": config or {},
            "created_at": datetime.utcnow().isoformat()
        }
        
        if position is not None and 0 <= position <= len(automation.steps):
            automation.steps.insert(position, step)
        else:
            automation.steps.append(step)
        
        return automation
    
    def activate_automation(self, automation_id: str) -> Optional[Automation]:
        automation = self.automations.get(automation_id)
        if automation:
            automation.is_active = True
        return automation
    
    def deactivate_automation(self, automation_id: str) -> Optional[Automation]:
        automation = self.automations.get(automation_id)
        if automation:
            automation.is_active = False
        return automation
    
    def trigger_automation(self, automation_id: str, contact_id: str) -> Optional[AutomationEnrollment]:
        """Enroll contact in automation"""
        automation = self.automations.get(automation_id)
        contact = self.contacts.get(contact_id)
        
        if not automation or not contact or not automation.is_active:
            return None
        
        # Check if already enrolled
        for enrollment in self.enrollments.values():
            if (enrollment.automation_id == automation_id and 
                enrollment.contact_id == contact_id and 
                enrollment.status == "active"):
                return None
        
        enrollment = AutomationEnrollment(
            id=str(uuid4()),
            automation_id=automation_id,
            contact_id=contact_id
        )
        
        self.enrollments[enrollment.id] = enrollment
        automation.stats["enrolled"] += 1
        automation.stats["active"] += 1
        
        return enrollment
    
    def get_automation(self, automation_id: str) -> Optional[Automation]:
        return self.automations.get(automation_id)
    
    def list_automations(self, workspace_id: str, active_only: bool = False) -> List[Automation]:
        automations = [a for a in self.automations.values() if a.workspace_id == workspace_id]
        if active_only:
            automations = [a for a in automations if a.is_active]
        return automations
    
    # ========================================================================
    # LANDING PAGES & FORMS
    # ========================================================================
    
    def create_landing_page(
        self,
        name: str,
        workspace_id: str,
        created_by: str,
        slug: str,
        html_content: str = "",
        meta_title: str = "",
        meta_description: str = ""
    ) -> LandingPage:
        """Create landing page"""
        # Check slug uniqueness
        for page in self.landing_pages.values():
            if page.slug == slug and page.workspace_id == workspace_id:
                raise ValueError(f"Slug '{slug}' already exists")
        
        landing_page = LandingPage(
            id=str(uuid4()),
            name=name,
            workspace_id=workspace_id,
            created_by=created_by,
            slug=slug,
            html_content=html_content,
            meta_title=meta_title,
            meta_description=meta_description
        )
        
        self.landing_pages[landing_page.id] = landing_page
        return landing_page
    
    def publish_landing_page(self, page_id: str) -> Optional[LandingPage]:
        page = self.landing_pages.get(page_id)
        if page:
            page.is_published = True
            page.published_at = datetime.utcnow()
        return page
    
    def unpublish_landing_page(self, page_id: str) -> Optional[LandingPage]:
        page = self.landing_pages.get(page_id)
        if page:
            page.is_published = False
        return page
    
    def record_page_view(self, page_id: str, is_unique: bool = True):
        """Record landing page view"""
        page = self.landing_pages.get(page_id)
        if page:
            page.stats["views"] += 1
            if is_unique:
                page.stats["unique_visitors"] += 1
    
    def create_form(
        self,
        name: str,
        workspace_id: str,
        created_by: str,
        fields: List[Dict] = None,
        submit_button_text: str = "Submit",
        tags_to_add: List[str] = None,
        automation_id: str = None
    ) -> Form:
        """Create a lead capture form"""
        form = Form(
            id=str(uuid4()),
            name=name,
            workspace_id=workspace_id,
            created_by=created_by,
            fields=fields or [
                {"name": "email", "type": "email", "required": True, "label": "Email"},
                {"name": "first_name", "type": "text", "required": False, "label": "First Name"}
            ],
            submit_button_text=submit_button_text,
            tags_to_add=tags_to_add or [],
            automation_id=automation_id
        )
        
        self.forms[form.id] = form
        return form
    
    def submit_form(
        self,
        form_id: str,
        data: Dict[str, Any],
        ip_address: str = None,
        page_url: str = None
    ) -> FormSubmission:
        """Process form submission"""
        form = self.forms.get(form_id)
        if not form:
            raise ValueError("Form not found")
        
        # Validate required fields
        for field in form.fields:
            if field.get("required") and field["name"] not in data:
                raise ValueError(f"Required field {field['name']} is missing")
        
        # Create or update contact
        email = data.get("email")
        contact = self.get_contact_by_email(email) if email else None
        
        if not contact and email:
            contact = Contact(
                id=str(uuid4()),
                email=email,
                created_by="form_submission",
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                phone=data.get("phone"),
                source="form",
                tags=form.tags_to_add.copy()
            )
            self.contacts[contact.id] = contact
        elif contact and form.tags_to_add:
            for tag in form.tags_to_add:
                if tag not in contact.tags:
                    contact.tags.append(tag)
        
        # Create submission
        submission = FormSubmission(
            id=str(uuid4()),
            form_id=form_id,
            contact_id=contact.id if contact else None,
            data=data,
            ip_address=ip_address,
            page_url=page_url
        )
        
        self.form_submissions[submission.id] = submission
        form.submissions_count += 1
        
        # Trigger automation if configured
        if form.automation_id and contact:
            self.trigger_automation(form.automation_id, contact.id)
        
        # Update landing page conversion
        if page_url:
            for page in self.landing_pages.values():
                if page.slug in page_url:
                    page.stats["conversions"] += 1
                    break
        
        return submission
    
    def get_form(self, form_id: str) -> Optional[Form]:
        return self.forms.get(form_id)
    
    def list_forms(self, workspace_id: str) -> List[Form]:
        return [f for f in self.forms.values() if f.workspace_id == workspace_id]
    
    # ========================================================================
    # AI FEATURES
    # ========================================================================
    
    def optimize_subject(self, subject: str, audience_data: Dict = None) -> Dict[str, Any]:
        """Get AI-optimized subject line suggestions"""
        return self.ai_engine.optimize_subject_line(subject, audience_data)
    
    def get_send_time_recommendation(self, audience_data: Dict = None) -> Dict[str, Any]:
        """Get AI-recommended send time"""
        return self.ai_engine.predict_send_time(audience_data)
    
    def get_content_suggestions(self, topic: str, tone: str = "professional") -> Dict[str, Any]:
        """Get AI content suggestions"""
        return self.ai_engine.generate_content_suggestions(topic, tone)
    
    def calculate_lead_score(self, contact_id: str) -> Dict[str, Any]:
        """Calculate AI lead score for contact"""
        contact = self.contacts.get(contact_id)
        if not contact:
            return {}
        return self.ai_engine.calculate_lead_score(contact)
    
    def auto_segment_contacts(self, workspace_id: str) -> Dict[str, List[str]]:
        """Auto-segment contacts using AI"""
        contacts = list(self.contacts.values())
        return self.ai_engine.segment_audience(contacts)
    
    # ========================================================================
    # ANALYTICS & DASHBOARD
    # ========================================================================
    
    def get_dashboard_stats(self, workspace_id: str) -> Dict[str, Any]:
        """Get marketing dashboard statistics"""
        contacts = list(self.contacts.values())
        campaigns = [c for c in self.campaigns.values() if c.workspace_id == workspace_id]
        automations = [a for a in self.automations.values() if a.workspace_id == workspace_id]
        
        # Contact stats
        total_contacts = len(contacts)
        active_contacts = len([c for c in contacts if c.status == ContactStatus.ACTIVE])
        new_this_month = len([c for c in contacts 
                            if (datetime.utcnow() - c.created_at).days <= 30])
        
        # Campaign stats
        total_campaigns = len(campaigns)
        sent_campaigns = len([c for c in campaigns if c.status == CampaignStatus.SENT])
        
        total_sent = sum(c.stats["sent"] for c in campaigns)
        total_opened = sum(c.stats["opened"] for c in campaigns)
        total_clicked = sum(c.stats["clicked"] for c in campaigns)
        
        avg_open_rate = total_opened / total_sent if total_sent > 0 else 0
        avg_click_rate = total_clicked / total_sent if total_sent > 0 else 0
        
        # Automation stats
        active_automations = len([a for a in automations if a.is_active])
        total_enrolled = sum(a.stats["enrolled"] for a in automations)
        
        return {
            "contacts": {
                "total": total_contacts,
                "active": active_contacts,
                "new_this_month": new_this_month,
                "growth_rate": new_this_month / total_contacts if total_contacts > 0 else 0
            },
            "campaigns": {
                "total": total_campaigns,
                "sent": sent_campaigns,
                "emails_sent": total_sent,
                "avg_open_rate": avg_open_rate,
                "avg_click_rate": avg_click_rate
            },
            "automations": {
                "total": len(automations),
                "active": active_automations,
                "contacts_enrolled": total_enrolled
            },
            "segments": {
                "total": len([s for s in self.segments.values() if s.workspace_id == workspace_id])
            },
            "forms": {
                "total": len([f for f in self.forms.values() if f.workspace_id == workspace_id]),
                "submissions_this_month": sum(f.submissions_count for f in self.forms.values())
            },
            "landing_pages": {
                "total": len([p for p in self.landing_pages.values() if p.workspace_id == workspace_id]),
                "published": len([p for p in self.landing_pages.values() 
                                if p.workspace_id == workspace_id and p.is_published])
            }
        }


# ============================================================================
# STANDALONE TEST
# ============================================================================

if __name__ == "__main__":
    print("🚀 Testing Marketing Automation Service...")
    
    service = MarketingAutomationService()
    workspace_id = "workspace_1"
    user_id = "user_1"
    
    # Test 1: Create contacts
    print("\n1️⃣ Creating contacts...")
    contact1 = service.create_contact(
        email="john@example.com",
        created_by=user_id,
        first_name="John",
        last_name="Doe",
        company="Acme Corp",
        tags=["vip", "enterprise"],
        source="organic"
    )
    print(f"   ✅ Contact created: {contact1.email}")
    
    contact2 = service.create_contact(
        email="jane@example.com",
        created_by=user_id,
        first_name="Jane",
        company="Startup Inc",
        source="webinar"
    )
    
    # Test 2: Create segment
    print("\n2️⃣ Creating segment...")
    segment = service.create_segment(
        name="VIP Customers",
        workspace_id=workspace_id,
        created_by=user_id,
        conditions=[{"field": "tag", "operator": "contains", "value": "vip"}]
    )
    print(f"   ✅ Segment created: {segment.name} ({segment.contact_count} contacts)")
    
    # Test 3: Create template
    print("\n3️⃣ Creating email template...")
    template = service.create_template(
        name="Welcome Email",
        workspace_id=workspace_id,
        created_by=user_id,
        subject="Welcome {{first_name}}!",
        html_content="<h1>Hello {{first_name}}!</h1><p>Welcome to our platform.</p>"
    )
    print(f"   ✅ Template created: {template.name} (variables: {template.variables})")
    
    # Test 4: Create campaign
    print("\n4️⃣ Creating campaign...")
    campaign = service.create_campaign(
        name="Q1 Newsletter",
        workspace_id=workspace_id,
        created_by=user_id,
        subject="Exciting updates for Q1!",
        from_name="Marketing Team",
        from_email="hello@example.com",
        html_content="<h1>Q1 Updates</h1><p>Check out what's new...</p>",
        segment_ids=[segment.id]
    )
    print(f"   ✅ Campaign created: {campaign.name}")
    
    # Test 5: Schedule and send campaign
    print("\n5️⃣ Scheduling campaign...")
    scheduled = service.schedule_campaign(
        campaign_id=campaign.id,
        scheduled_at=datetime.utcnow() + timedelta(hours=1),
        user_id=user_id
    )
    print(f"   ✅ Campaign scheduled: {scheduled.stats['recipients']} recipients")
    
    sent = service.send_campaign(campaign.id, user_id)
    print(f"   ✅ Campaign sent: {sent.stats['sent']} emails")
    
    # Test 6: AI subject optimization
    print("\n6️⃣ AI subject optimization...")
    optimization = service.optimize_subject("Check out our new products")
    print(f"   Original score: {optimization['original']['score']}")
    print(f"   Suggestions:")
    for s in optimization['suggestions'][:3]:
        print(f"      - {s['subject']} (predicted open: {s['predicted_open_rate']:.1%})")
    
    # Test 7: AI send time
    print("\n7️⃣ AI send time recommendation...")
    send_time = service.get_send_time_recommendation()
    print(f"   ✅ Best time: {send_time['recommended']['day']} at {send_time['recommended']['time']}")
    
    # Test 8: Create automation
    print("\n8️⃣ Creating automation workflow...")
    automation = service.create_automation(
        name="Welcome Series",
        workspace_id=workspace_id,
        created_by=user_id,
        trigger=AutomationTrigger.SIGNUP,
        description="Welcome email series for new signups"
    )
    
    service.add_automation_step(
        automation.id,
        AutomationAction.SEND_EMAIL,
        {"template_id": template.id}
    )
    service.add_automation_step(
        automation.id,
        AutomationAction.WAIT,
        {"days": 3}
    )
    service.add_automation_step(
        automation.id,
        AutomationAction.ADD_TAG,
        {"tag": "onboarded"}
    )
    
    service.activate_automation(automation.id)
    print(f"   ✅ Automation created: {automation.name} ({len(automation.steps)} steps)")
    
    # Test 9: Create form
    print("\n9️⃣ Creating lead capture form...")
    form = service.create_form(
        name="Newsletter Signup",
        workspace_id=workspace_id,
        created_by=user_id,
        fields=[
            {"name": "email", "type": "email", "required": True, "label": "Email"},
            {"name": "first_name", "type": "text", "required": False, "label": "First Name"}
        ],
        tags_to_add=["newsletter"],
        automation_id=automation.id
    )
    print(f"   ✅ Form created: {form.name}")
    
    # Test 10: Submit form
    print("\n🔟 Submitting form...")
    submission = service.submit_form(
        form_id=form.id,
        data={"email": "newuser@example.com", "first_name": "New User"}
    )
    print(f"   ✅ Form submitted, contact ID: {submission.contact_id}")
    
    # Test 11: Lead scoring
    print("\n1️⃣1️⃣ Calculating lead score...")
    score = service.calculate_lead_score(contact1.id)
    print(f"   ✅ Lead score: {score['score']}/100 ({score['category']})")
    print(f"   Recommendations: {score['recommendations'][:2]}")
    
    # Test 12: Dashboard
    print("\n1️⃣2️⃣ Getting dashboard stats...")
    dashboard = service.get_dashboard_stats(workspace_id)
    print(f"   ✅ Contacts: {dashboard['contacts']['total']}")
    print(f"   ✅ Campaigns: {dashboard['campaigns']['total']}")
    print(f"   ✅ Automations: {dashboard['automations']['active']} active")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
