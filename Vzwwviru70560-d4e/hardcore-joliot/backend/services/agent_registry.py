"""
CHE·NU™ Agent Registry Service
==============================

Registry of all specialized agents across 9 spheres + Thread Agents.

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - agents with sensitive capabilities have human gates
- Rule #4: My Team Restrictions - NO AI-to-AI orchestration
- Rule #6: Traceability - all agents versioned and documented

AGENT TYPES:
1. SPHERE AGENTS (predefined, ~310 total):
   - Personal: 32 (+4 new)
   - Business: 50 (+7 new)
   - Government: 22 (+4 new)
   - Creative Studio: 45 (+3 new)
   - Community: 15 (+3 new)
   - Social Media: 18 (+3 new)
   - Entertainment: 10 (+2 new)
   - My Team: 38 (+3 new)
   - Scholar: 30 (+5 new)
   - Immobilier: 20 (NEW DOMAIN)
   - Core: 30 (cross-sphere)

2. THREAD AGENTS (dynamic):
   - Created automatically with each Thread
   - One agent per Thread
   - Inherits capabilities from Thread's sphere
   - Governed by Thread's identity boundary
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import NotFoundError, ValidationError, ConflictError
from backend.models.agent import (
    Agent,
    AgentStatus,
    AgentCapabilityType,
    SphereType,
    UserAgentConfig,
)
from backend.schemas.agent_schemas import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentSummary,
    AgentListResponse,
    SphereAgentSummary,
    AllSpheresAgentSummary,
    UserAgentConfigCreate,
    UserAgentConfigUpdate,
    UserAgentConfigResponse,
    AGENT_DISTRIBUTION,
    TOTAL_AGENTS,
)

logger = logging.getLogger(__name__)


# =============================================================================
# PREDEFINED AGENTS (226 total)
# =============================================================================

def _get_personal_agents() -> List[Dict[str, Any]]:
    """28 Personal sphere agents."""
    return [
        {"name": "personal_note_assistant", "display_name": "Note Assistant", "capabilities": ["text_generation", "summarization"], "requires_human_gate": False},
        {"name": "personal_task_manager", "display_name": "Task Manager", "capabilities": ["prioritization", "recommendation"], "requires_human_gate": False},
        {"name": "personal_calendar_assistant", "display_name": "Calendar Assistant", "capabilities": ["scheduling", "recommendation"], "requires_human_gate": False},
        {"name": "personal_habit_tracker", "display_name": "Habit Tracker", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "personal_goal_coach", "display_name": "Goal Coach", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "personal_journal_assistant", "display_name": "Journal Assistant", "capabilities": ["text_generation", "analysis"], "requires_human_gate": False},
        {"name": "personal_memory_keeper", "display_name": "Memory Keeper", "capabilities": ["summarization", "extraction"], "requires_human_gate": False},
        {"name": "personal_wellness_advisor", "display_name": "Wellness Advisor", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "personal_finance_tracker", "display_name": "Finance Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "personal_budget_planner", "display_name": "Budget Planner", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "personal_reminder_bot", "display_name": "Reminder Bot", "capabilities": ["notification_draft"], "requires_human_gate": True, "human_gate_capabilities": ["notification_draft"]},
        {"name": "personal_email_assistant", "display_name": "Email Assistant", "capabilities": ["email_draft", "summarization"], "requires_human_gate": True, "human_gate_capabilities": ["email_draft"]},
        {"name": "personal_reading_curator", "display_name": "Reading Curator", "capabilities": ["recommendation", "summarization"], "requires_human_gate": False},
        {"name": "personal_learning_path", "display_name": "Learning Path Advisor", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
        {"name": "personal_decision_helper", "display_name": "Decision Helper", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "personal_life_organizer", "display_name": "Life Organizer", "capabilities": ["prioritization", "recommendation"], "requires_human_gate": False},
        {"name": "personal_gratitude_journal", "display_name": "Gratitude Journal", "capabilities": ["text_generation"], "requires_human_gate": False},
        {"name": "personal_mood_tracker", "display_name": "Mood Tracker", "capabilities": ["analysis", "classification"], "requires_human_gate": False},
        {"name": "personal_sleep_analyzer", "display_name": "Sleep Analyzer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "personal_exercise_planner", "display_name": "Exercise Planner", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
        {"name": "personal_meal_planner", "display_name": "Meal Planner", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
        {"name": "personal_travel_assistant", "display_name": "Travel Assistant", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
        {"name": "personal_event_planner", "display_name": "Event Planner", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "personal_gift_suggester", "display_name": "Gift Suggester", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
        {"name": "personal_contact_manager", "display_name": "Contact Manager", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
        {"name": "personal_photo_organizer", "display_name": "Photo Organizer", "capabilities": ["classification", "data_processing"], "requires_human_gate": False},
        {"name": "personal_document_filer", "display_name": "Document Filer", "capabilities": ["classification", "document_processing"], "requires_human_gate": False},
        {"name": "personal_password_helper", "display_name": "Password Helper", "capabilities": ["recommendation"], "requires_human_gate": False},
    ]


def _get_business_agents() -> List[Dict[str, Any]]:
    """43 Business sphere agents."""
    return [
        {"name": "business_crm_assistant", "display_name": "CRM Assistant", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
        {"name": "business_lead_scorer", "display_name": "Lead Scorer", "capabilities": ["scoring", "analysis"], "requires_human_gate": False},
        {"name": "business_sales_forecaster", "display_name": "Sales Forecaster", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "business_proposal_writer", "display_name": "Proposal Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True, "human_gate_capabilities": ["text_generation"]},
        {"name": "business_contract_analyzer", "display_name": "Contract Analyzer", "capabilities": ["analysis", "extraction"], "requires_human_gate": False},
        {"name": "business_invoice_generator", "display_name": "Invoice Generator", "capabilities": ["document_processing", "data_processing"], "requires_human_gate": True},
        {"name": "business_expense_tracker", "display_name": "Expense Tracker", "capabilities": ["data_processing", "classification"], "requires_human_gate": False},
        {"name": "business_report_generator", "display_name": "Report Generator", "capabilities": ["text_generation", "analysis"], "requires_human_gate": False},
        {"name": "business_meeting_scheduler", "display_name": "Meeting Scheduler", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "business_email_composer", "display_name": "Business Email Composer", "capabilities": ["email_draft", "text_generation"], "requires_human_gate": True, "human_gate_capabilities": ["email_draft"]},
        {"name": "business_competitor_analyst", "display_name": "Competitor Analyst", "capabilities": ["research", "analysis"], "requires_human_gate": False},
        {"name": "business_market_researcher", "display_name": "Market Researcher", "capabilities": ["research", "analysis"], "requires_human_gate": False},
        {"name": "business_pricing_optimizer", "display_name": "Pricing Optimizer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "business_inventory_manager", "display_name": "Inventory Manager", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
        {"name": "business_supplier_evaluator", "display_name": "Supplier Evaluator", "capabilities": ["scoring", "analysis"], "requires_human_gate": False},
        {"name": "business_project_estimator", "display_name": "Project Estimator", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "business_risk_assessor", "display_name": "Risk Assessor", "capabilities": ["analysis", "scoring"], "requires_human_gate": False},
        {"name": "business_customer_insights", "display_name": "Customer Insights", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
        {"name": "business_churn_predictor", "display_name": "Churn Predictor", "capabilities": ["analysis", "scoring"], "requires_human_gate": False},
        {"name": "business_upsell_suggester", "display_name": "Upsell Suggester", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "business_quote_builder", "display_name": "Quote Builder", "capabilities": ["document_processing", "data_processing"], "requires_human_gate": True},
        {"name": "business_order_processor", "display_name": "Order Processor", "capabilities": ["data_processing"], "requires_human_gate": True},
        {"name": "business_shipping_optimizer", "display_name": "Shipping Optimizer", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "business_return_handler", "display_name": "Return Handler", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": True},
        {"name": "business_review_analyzer", "display_name": "Review Analyzer", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
        {"name": "business_kpi_tracker", "display_name": "KPI Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "business_cash_flow_analyst", "display_name": "Cash Flow Analyst", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "business_tax_helper", "display_name": "Tax Helper", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "business_payroll_assistant", "display_name": "Payroll Assistant", "capabilities": ["data_processing"], "requires_human_gate": True},
        {"name": "business_compliance_checker", "display_name": "Compliance Checker", "capabilities": ["analysis", "fact_check"], "requires_human_gate": False},
        {"name": "business_policy_writer", "display_name": "Policy Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
        {"name": "business_sop_generator", "display_name": "SOP Generator", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": False},
        {"name": "business_training_creator", "display_name": "Training Creator", "capabilities": ["content_planning", "text_generation"], "requires_human_gate": False},
        {"name": "business_knowledge_base", "display_name": "Knowledge Base Manager", "capabilities": ["summarization", "classification"], "requires_human_gate": False},
        {"name": "business_faq_generator", "display_name": "FAQ Generator", "capabilities": ["text_generation", "extraction"], "requires_human_gate": False},
        {"name": "business_customer_support", "display_name": "Customer Support Assistant", "capabilities": ["text_generation", "recommendation"], "requires_human_gate": True, "human_gate_capabilities": ["text_generation"]},
        {"name": "business_ticket_router", "display_name": "Ticket Router", "capabilities": ["classification", "prioritization"], "requires_human_gate": False},
        {"name": "business_sentiment_analyzer", "display_name": "Sentiment Analyzer", "capabilities": ["analysis", "classification"], "requires_human_gate": False},
        {"name": "business_feedback_processor", "display_name": "Feedback Processor", "capabilities": ["summarization", "classification"], "requires_human_gate": False},
        {"name": "business_nps_analyzer", "display_name": "NPS Analyzer", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
        {"name": "business_partnership_scout", "display_name": "Partnership Scout", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
        {"name": "business_negotiation_prep", "display_name": "Negotiation Prep", "capabilities": ["research", "analysis"], "requires_human_gate": False},
        {"name": "business_presentation_builder", "display_name": "Presentation Builder", "capabilities": ["content_planning", "text_generation"], "requires_human_gate": False},
    ]


def _get_government_agents() -> List[Dict[str, Any]]:
    """18 Government sphere agents."""
    return [
        {"name": "gov_document_preparer", "display_name": "Document Preparer", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": True},
        {"name": "gov_compliance_tracker", "display_name": "Compliance Tracker", "capabilities": ["analysis", "fact_check"], "requires_human_gate": False},
        {"name": "gov_deadline_monitor", "display_name": "Deadline Monitor", "capabilities": ["notification_draft", "analysis"], "requires_human_gate": True, "human_gate_capabilities": ["notification_draft"]},
        {"name": "gov_form_filler", "display_name": "Form Filler", "capabilities": ["document_processing", "extraction"], "requires_human_gate": True},
        {"name": "gov_regulation_analyst", "display_name": "Regulation Analyst", "capabilities": ["research", "analysis"], "requires_human_gate": False},
        {"name": "gov_permit_tracker", "display_name": "Permit Tracker", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
        {"name": "gov_tax_calculator", "display_name": "Tax Calculator", "capabilities": ["data_processing", "analysis"], "requires_human_gate": False},
        {"name": "gov_grant_finder", "display_name": "Grant Finder", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
        {"name": "gov_grant_writer", "display_name": "Grant Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
        {"name": "gov_license_manager", "display_name": "License Manager", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
        {"name": "gov_audit_preparer", "display_name": "Audit Preparer", "capabilities": ["document_processing", "analysis"], "requires_human_gate": True},
        {"name": "gov_policy_analyzer", "display_name": "Policy Analyzer", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
        {"name": "gov_public_records", "display_name": "Public Records Assistant", "capabilities": ["research", "extraction"], "requires_human_gate": False},
        {"name": "gov_citizen_service", "display_name": "Citizen Service Guide", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
        {"name": "gov_voting_info", "display_name": "Voting Information", "capabilities": ["research", "fact_check"], "requires_human_gate": False},
        {"name": "gov_benefits_advisor", "display_name": "Benefits Advisor", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "gov_legal_reference", "display_name": "Legal Reference", "capabilities": ["research", "analysis"], "requires_human_gate": False},
        {"name": "gov_freedom_info", "display_name": "Freedom of Information Helper", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": True},
    ]


def _get_creative_studio_agents() -> List[Dict[str, Any]]:
    """42 Creative Studio sphere agents."""
    return [
        {"name": "creative_image_generator", "display_name": "Image Generator", "capabilities": ["image_generation"], "requires_human_gate": False},
        {"name": "creative_image_editor", "display_name": "Image Editor", "capabilities": ["image_generation", "recommendation"], "requires_human_gate": False},
        {"name": "creative_style_transfer", "display_name": "Style Transfer", "capabilities": ["image_generation"], "requires_human_gate": False},
        {"name": "creative_logo_designer", "display_name": "Logo Designer", "capabilities": ["image_generation", "brainstorm"], "requires_human_gate": False},
        {"name": "creative_icon_maker", "display_name": "Icon Maker", "capabilities": ["image_generation"], "requires_human_gate": False},
        {"name": "creative_thumbnail_creator", "display_name": "Thumbnail Creator", "capabilities": ["image_generation", "recommendation"], "requires_human_gate": False},
        {"name": "creative_banner_designer", "display_name": "Banner Designer", "capabilities": ["image_generation", "design_assist"], "requires_human_gate": False},
        {"name": "creative_social_graphics", "display_name": "Social Graphics", "capabilities": ["image_generation", "design_assist"], "requires_human_gate": False},
        {"name": "creative_presentation_designer", "display_name": "Presentation Designer", "capabilities": ["design_assist", "content_planning"], "requires_human_gate": False},
        {"name": "creative_infographic_maker", "display_name": "Infographic Maker", "capabilities": ["design_assist", "data_processing"], "requires_human_gate": False},
        {"name": "creative_video_scriptwriter", "display_name": "Video Scriptwriter", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": False},
        {"name": "creative_video_editor", "display_name": "Video Editor Assistant", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "creative_subtitle_generator", "display_name": "Subtitle Generator", "capabilities": ["text_generation", "extraction"], "requires_human_gate": False},
        {"name": "creative_storyboard_creator", "display_name": "Storyboard Creator", "capabilities": ["content_planning", "image_generation"], "requires_human_gate": False},
        {"name": "creative_animation_assistant", "display_name": "Animation Assistant", "capabilities": ["recommendation", "design_assist"], "requires_human_gate": False},
        {"name": "creative_voice_generator", "display_name": "Voice Generator", "capabilities": ["audio_generation"], "requires_human_gate": False},
        {"name": "creative_voice_cloner", "display_name": "Voice Cloner", "capabilities": ["audio_generation"], "requires_human_gate": True},
        {"name": "creative_music_composer", "display_name": "Music Composer", "capabilities": ["audio_generation", "brainstorm"], "requires_human_gate": False},
        {"name": "creative_sound_designer", "display_name": "Sound Designer", "capabilities": ["audio_generation", "recommendation"], "requires_human_gate": False},
        {"name": "creative_podcast_editor", "display_name": "Podcast Editor", "capabilities": ["audio_generation", "summarization"], "requires_human_gate": False},
        {"name": "creative_copywriter", "display_name": "Copywriter", "capabilities": ["text_generation", "brainstorm"], "requires_human_gate": False},
        {"name": "creative_headline_generator", "display_name": "Headline Generator", "capabilities": ["text_generation", "brainstorm"], "requires_human_gate": False},
        {"name": "creative_tagline_creator", "display_name": "Tagline Creator", "capabilities": ["text_generation", "brainstorm"], "requires_human_gate": False},
        {"name": "creative_ad_writer", "display_name": "Ad Writer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True, "human_gate_capabilities": ["text_generation"]},
        {"name": "creative_blog_writer", "display_name": "Blog Writer", "capabilities": ["text_generation", "research"], "requires_human_gate": False},
        {"name": "creative_article_spinner", "display_name": "Article Rephraser", "capabilities": ["text_generation"], "requires_human_gate": False},
        {"name": "creative_story_generator", "display_name": "Story Generator", "capabilities": ["text_generation", "brainstorm"], "requires_human_gate": False},
        {"name": "creative_poetry_writer", "display_name": "Poetry Writer", "capabilities": ["text_generation"], "requires_human_gate": False},
        {"name": "creative_dialogue_writer", "display_name": "Dialogue Writer", "capabilities": ["text_generation"], "requires_human_gate": False},
        {"name": "creative_character_creator", "display_name": "Character Creator", "capabilities": ["brainstorm", "text_generation"], "requires_human_gate": False},
        {"name": "creative_world_builder", "display_name": "World Builder", "capabilities": ["brainstorm", "text_generation"], "requires_human_gate": False},
        {"name": "creative_plot_generator", "display_name": "Plot Generator", "capabilities": ["brainstorm", "content_planning"], "requires_human_gate": False},
        {"name": "creative_name_generator", "display_name": "Name Generator", "capabilities": ["brainstorm"], "requires_human_gate": False},
        {"name": "creative_brand_identity", "display_name": "Brand Identity", "capabilities": ["brainstorm", "design_assist"], "requires_human_gate": False},
        {"name": "creative_color_palette", "display_name": "Color Palette Generator", "capabilities": ["design_assist", "recommendation"], "requires_human_gate": False},
        {"name": "creative_font_selector", "display_name": "Font Selector", "capabilities": ["recommendation", "design_assist"], "requires_human_gate": False},
        {"name": "creative_mockup_generator", "display_name": "Mockup Generator", "capabilities": ["image_generation", "design_assist"], "requires_human_gate": False},
        {"name": "creative_ui_assistant", "display_name": "UI Assistant", "capabilities": ["design_assist", "recommendation"], "requires_human_gate": False},
        {"name": "creative_ux_reviewer", "display_name": "UX Reviewer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "creative_code_generator", "display_name": "Code Generator", "capabilities": ["code_generation"], "requires_human_gate": False},
        {"name": "creative_code_reviewer", "display_name": "Code Reviewer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "creative_documentation", "display_name": "Documentation Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": False},
    ]


def _get_community_agents() -> List[Dict[str, Any]]:
    """12 Community sphere agents."""
    return [
        {"name": "community_event_organizer", "display_name": "Event Organizer", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "community_volunteer_coordinator", "display_name": "Volunteer Coordinator", "capabilities": ["recommendation", "data_processing"], "requires_human_gate": False},
        {"name": "community_announcement_drafter", "display_name": "Announcement Drafter", "capabilities": ["text_generation", "notification_draft"], "requires_human_gate": True, "human_gate_capabilities": ["notification_draft"]},
        {"name": "community_discussion_moderator", "display_name": "Discussion Moderator", "capabilities": ["classification", "summarization"], "requires_human_gate": False},
        {"name": "community_poll_creator", "display_name": "Poll Creator", "capabilities": ["content_planning"], "requires_human_gate": False},
        {"name": "community_resource_curator", "display_name": "Resource Curator", "capabilities": ["recommendation", "classification"], "requires_human_gate": False},
        {"name": "community_newsletter_writer", "display_name": "Newsletter Writer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True, "human_gate_capabilities": ["text_generation"]},
        {"name": "community_member_welcomer", "display_name": "Member Welcomer", "capabilities": ["text_generation", "message_draft"], "requires_human_gate": True, "human_gate_capabilities": ["message_draft"]},
        {"name": "community_feedback_collector", "display_name": "Feedback Collector", "capabilities": ["summarization", "classification"], "requires_human_gate": False},
        {"name": "community_conflict_resolver", "display_name": "Conflict Resolver", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "community_milestone_tracker", "display_name": "Milestone Tracker", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
        {"name": "community_impact_reporter", "display_name": "Impact Reporter", "capabilities": ["analysis", "text_generation"], "requires_human_gate": False},
    ]


def _get_social_media_agents() -> List[Dict[str, Any]]:
    """15 Social Media sphere agents - NO RANKING (Rule #5)."""
    return [
        {"name": "social_post_composer", "display_name": "Post Composer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True, "human_gate_capabilities": ["text_generation"]},
        {"name": "social_hashtag_suggester", "display_name": "Hashtag Suggester", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "social_caption_writer", "display_name": "Caption Writer", "capabilities": ["text_generation"], "requires_human_gate": True, "human_gate_capabilities": ["text_generation"]},
        {"name": "social_thread_writer", "display_name": "Thread Writer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True},
        {"name": "social_reply_assistant", "display_name": "Reply Assistant", "capabilities": ["text_generation", "message_draft"], "requires_human_gate": True, "human_gate_capabilities": ["message_draft"]},
        {"name": "social_dm_assistant", "display_name": "DM Assistant", "capabilities": ["message_draft", "text_generation"], "requires_human_gate": True, "human_gate_capabilities": ["message_draft"]},
        {"name": "social_bio_writer", "display_name": "Bio Writer", "capabilities": ["text_generation"], "requires_human_gate": False},
        {"name": "social_content_calendar", "display_name": "Content Calendar", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "social_analytics_reporter", "display_name": "Analytics Reporter", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
        {"name": "social_trend_spotter", "display_name": "Trend Spotter", "capabilities": ["research", "analysis"], "requires_human_gate": False},
        {"name": "social_audience_analyzer", "display_name": "Audience Analyzer", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
        {"name": "social_competitor_tracker", "display_name": "Competitor Tracker", "capabilities": ["research", "analysis"], "requires_human_gate": False},
        {"name": "social_cross_poster", "display_name": "Cross-Poster", "capabilities": ["content_planning"], "requires_human_gate": True},
        {"name": "social_scheduling_assistant", "display_name": "Scheduling Assistant", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "social_engagement_analyzer", "display_name": "Engagement Analyzer", "capabilities": ["analysis"], "requires_human_gate": False},
        # NOTE: NO engagement_bot, NO ranking_optimizer - Rule #5 compliance
    ]


def _get_entertainment_agents() -> List[Dict[str, Any]]:
    """8 Entertainment sphere agents."""
    return [
        {"name": "entertainment_recommendation", "display_name": "Entertainment Recommender", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "entertainment_playlist_curator", "display_name": "Playlist Curator", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
        {"name": "entertainment_movie_finder", "display_name": "Movie Finder", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
        {"name": "entertainment_game_suggester", "display_name": "Game Suggester", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "entertainment_book_recommender", "display_name": "Book Recommender", "capabilities": ["recommendation", "summarization"], "requires_human_gate": False},
        {"name": "entertainment_podcast_finder", "display_name": "Podcast Finder", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
        {"name": "entertainment_event_finder", "display_name": "Event Finder", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
        {"name": "entertainment_trivia_master", "display_name": "Trivia Master", "capabilities": ["brainstorm", "fact_check"], "requires_human_gate": False},
    ]


def _get_my_team_agents() -> List[Dict[str, Any]]:
    """35 My Team sphere agents - NO AI-to-AI orchestration (Rule #4)."""
    return [
        {"name": "team_meeting_scheduler", "display_name": "Meeting Scheduler", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "team_agenda_creator", "display_name": "Agenda Creator", "capabilities": ["content_planning", "text_generation"], "requires_human_gate": False},
        {"name": "team_minutes_taker", "display_name": "Minutes Taker", "capabilities": ["summarization", "extraction"], "requires_human_gate": False},
        {"name": "team_action_tracker", "display_name": "Action Tracker", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
        {"name": "team_standup_assistant", "display_name": "Standup Assistant", "capabilities": ["summarization", "content_planning"], "requires_human_gate": False},
        {"name": "team_retrospective_helper", "display_name": "Retrospective Helper", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
        {"name": "team_performance_tracker", "display_name": "Performance Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "team_feedback_assistant", "display_name": "Feedback Assistant", "capabilities": ["text_generation", "analysis"], "requires_human_gate": True, "human_gate_capabilities": ["text_generation"]},
        {"name": "team_onboarding_guide", "display_name": "Onboarding Guide", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
        {"name": "team_training_planner", "display_name": "Training Planner", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "team_skill_mapper", "display_name": "Skill Mapper", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "team_resource_allocator", "display_name": "Resource Allocator", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "team_workload_analyzer", "display_name": "Workload Analyzer", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "team_capacity_planner", "display_name": "Capacity Planner", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "team_hiring_assistant", "display_name": "Hiring Assistant", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "team_interview_scheduler", "display_name": "Interview Scheduler", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "team_resume_screener", "display_name": "Resume Screener", "capabilities": ["analysis", "scoring"], "requires_human_gate": False},
        {"name": "team_job_description", "display_name": "Job Description Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
        {"name": "team_offer_letter", "display_name": "Offer Letter Generator", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": True},
        {"name": "team_policy_writer", "display_name": "Team Policy Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
        {"name": "team_handbook_updater", "display_name": "Handbook Updater", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
        {"name": "team_benefits_advisor", "display_name": "Benefits Advisor", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
        {"name": "team_leave_tracker", "display_name": "Leave Tracker", "capabilities": ["data_processing"], "requires_human_gate": False},
        {"name": "team_timesheet_helper", "display_name": "Timesheet Helper", "capabilities": ["data_processing", "analysis"], "requires_human_gate": False},
        {"name": "team_expense_reviewer", "display_name": "Expense Reviewer", "capabilities": ["analysis", "classification"], "requires_human_gate": False},
        {"name": "team_project_status", "display_name": "Project Status Reporter", "capabilities": ["summarization", "analysis"], "requires_human_gate": False},
        {"name": "team_risk_identifier", "display_name": "Risk Identifier", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "team_blocker_resolver", "display_name": "Blocker Resolver", "capabilities": ["recommendation", "analysis"], "requires_human_gate": False},
        {"name": "team_dependency_tracker", "display_name": "Dependency Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "team_milestone_planner", "display_name": "Milestone Planner", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "team_communication_helper", "display_name": "Communication Helper", "capabilities": ["text_generation", "recommendation"], "requires_human_gate": False},
        {"name": "team_conflict_mediator", "display_name": "Conflict Mediator", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "team_morale_tracker", "display_name": "Morale Tracker", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "team_recognition_suggester", "display_name": "Recognition Suggester", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "team_culture_guardian", "display_name": "Culture Guardian", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        # NOTE: NO orchestrator agent - Rule #4 compliance
    ]


def _get_scholar_agents() -> List[Dict[str, Any]]:
    """25 Scholar sphere agents."""
    return [
        {"name": "scholar_literature_search", "display_name": "Literature Search", "capabilities": ["research", "search"], "requires_human_gate": False},
        {"name": "scholar_paper_summarizer", "display_name": "Paper Summarizer", "capabilities": ["summarization", "extraction"], "requires_human_gate": False},
        {"name": "scholar_citation_manager", "display_name": "Citation Manager", "capabilities": ["data_processing", "document_processing"], "requires_human_gate": False},
        {"name": "scholar_bibliography_builder", "display_name": "Bibliography Builder", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": False},
        {"name": "scholar_research_noter", "display_name": "Research Noter", "capabilities": ["text_generation", "summarization"], "requires_human_gate": False},
        {"name": "scholar_hypothesis_generator", "display_name": "Hypothesis Generator", "capabilities": ["brainstorm", "analysis"], "requires_human_gate": False},
        {"name": "scholar_methodology_advisor", "display_name": "Methodology Advisor", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
        {"name": "scholar_data_analyzer", "display_name": "Data Analyzer", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "scholar_statistics_helper", "display_name": "Statistics Helper", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "scholar_visualization_creator", "display_name": "Visualization Creator", "capabilities": ["design_assist", "data_processing"], "requires_human_gate": False},
        {"name": "scholar_manuscript_editor", "display_name": "Manuscript Editor", "capabilities": ["text_generation", "analysis"], "requires_human_gate": False},
        {"name": "scholar_abstract_writer", "display_name": "Abstract Writer", "capabilities": ["text_generation", "summarization"], "requires_human_gate": False},
        {"name": "scholar_peer_review_helper", "display_name": "Peer Review Helper", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "scholar_journal_finder", "display_name": "Journal Finder", "capabilities": ["recommendation", "research"], "requires_human_gate": False},
        {"name": "scholar_grant_scout", "display_name": "Grant Scout", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
        {"name": "scholar_proposal_writer", "display_name": "Proposal Writer", "capabilities": ["text_generation", "document_processing"], "requires_human_gate": True},
        {"name": "scholar_presentation_builder", "display_name": "Presentation Builder", "capabilities": ["content_planning", "design_assist"], "requires_human_gate": False},
        {"name": "scholar_poster_creator", "display_name": "Poster Creator", "capabilities": ["design_assist", "content_planning"], "requires_human_gate": False},
        {"name": "scholar_conference_finder", "display_name": "Conference Finder", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
        {"name": "scholar_collaboration_finder", "display_name": "Collaboration Finder", "capabilities": ["research", "recommendation"], "requires_human_gate": False},
        {"name": "scholar_fact_checker", "display_name": "Fact Checker", "capabilities": ["fact_check", "research"], "requires_human_gate": False},
        {"name": "scholar_plagiarism_checker", "display_name": "Plagiarism Checker", "capabilities": ["analysis"], "requires_human_gate": False},
        {"name": "scholar_reference_validator", "display_name": "Reference Validator", "capabilities": ["fact_check", "analysis"], "requires_human_gate": False},
        {"name": "scholar_teaching_assistant", "display_name": "Teaching Assistant", "capabilities": ["text_generation", "recommendation"], "requires_human_gate": False},
        {"name": "scholar_quiz_generator", "display_name": "Quiz Generator", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": False},
    ]


def get_all_predefined_agents() -> List[Dict[str, Any]]:
    """
    Get all 226 predefined agents.
    
    Returns list of agent definitions ready for database seeding.
    """
    agents = []
    
    sphere_generators = {
        SphereType.PERSONAL: _get_personal_agents,
        SphereType.BUSINESS: _get_business_agents,
        SphereType.GOVERNMENT: _get_government_agents,
        SphereType.CREATIVE_STUDIO: _get_creative_studio_agents,
        SphereType.COMMUNITY: _get_community_agents,
        SphereType.SOCIAL_MEDIA: _get_social_media_agents,
        SphereType.ENTERTAINMENT: _get_entertainment_agents,
        SphereType.MY_TEAM: _get_my_team_agents,
        SphereType.SCHOLAR: _get_scholar_agents,
    }
    
    for sphere_type, generator in sphere_generators.items():
        sphere_agents = generator()
        for agent_def in sphere_agents:
            agent_def["sphere_type"] = sphere_type
            agent_def["id"] = uuid4()
            agent_def["status"] = AgentStatus.ACTIVE
            agent_def.setdefault("requires_human_gate", False)
            agent_def.setdefault("human_gate_capabilities", [])
            agent_def.setdefault("description", f"{agent_def['display_name']} for {sphere_type.value} sphere")
            agents.append(agent_def)
    
    # Verify count
    assert len(agents) == TOTAL_AGENTS, f"Expected {TOTAL_AGENTS} agents, got {len(agents)}"
    
    return agents


# =============================================================================
# AGENT REGISTRY SERVICE
# =============================================================================

class AgentRegistryService:
    """
    Service for managing the agent registry.
    
    R&D COMPLIANCE:
    - Rule #1: Tracks which agents require human gates
    - Rule #4: NO AI-to-AI orchestration capabilities
    - Rule #6: All agents versioned and documented
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # -------------------------------------------------------------------------
    # AGENT QUERIES
    # -------------------------------------------------------------------------
    
    async def get_agent(self, agent_id: UUID) -> Agent:
        """Get agent by ID."""
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            raise NotFoundError(f"Agent not found: {agent_id}")
        
        return agent
    
    async def get_agent_by_name(self, name: str) -> Agent:
        """Get agent by unique name."""
        result = await self.db.execute(
            select(Agent).where(Agent.name == name)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            raise NotFoundError(f"Agent not found: {name}")
        
        return agent
    
    async def list_agents(
        self,
        sphere_type: Optional[SphereType] = None,
        status: Optional[AgentStatus] = None,
        capability: Optional[AgentCapabilityType] = None,
        requires_human_gate: Optional[bool] = None,
    ) -> List[Agent]:
        """List agents with optional filters."""
        query = select(Agent)
        
        conditions = []
        if sphere_type:
            conditions.append(Agent.sphere_type == sphere_type)
        if status:
            conditions.append(Agent.status == status)
        if requires_human_gate is not None:
            conditions.append(Agent.requires_human_gate == requires_human_gate)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        result = await self.db.execute(query.order_by(Agent.sphere_type, Agent.name))
        agents = list(result.scalars().all())
        
        # Filter by capability if specified
        if capability:
            agents = [a for a in agents if capability.value in a.capabilities]
        
        return agents
    
    async def get_agents_by_sphere(self, sphere_type: SphereType) -> List[Agent]:
        """Get all agents for a specific sphere."""
        return await self.list_agents(sphere_type=sphere_type, status=AgentStatus.ACTIVE)
    
    async def get_all_spheres_summary(self) -> AllSpheresAgentSummary:
        """Get summary of agents across all 9 spheres."""
        all_agents = await self.list_agents()
        
        by_sphere: Dict[str, SphereAgentSummary] = {}
        
        for sphere_type in SphereType:
            sphere_agents = [a for a in all_agents if a.sphere_type == sphere_type]
            active_agents = [a for a in sphere_agents if a.status == AgentStatus.ACTIVE]
            
            by_sphere[sphere_type.value] = SphereAgentSummary(
                sphere_type=sphere_type,
                total_agents=len(sphere_agents),
                active_agents=len(active_agents),
                agents=[
                    AgentSummary(
                        id=a.id,
                        name=a.name,
                        display_name=a.display_name,
                        sphere_type=a.sphere_type,
                        status=a.status,
                        capabilities=a.capabilities,
                        requires_human_gate=a.requires_human_gate,
                    )
                    for a in active_agents
                ]
            )
        
        return AllSpheresAgentSummary(
            total_agents=len(all_agents),
            by_sphere=by_sphere
        )
    
    async def count_agents(self) -> Dict[str, int]:
        """Count agents by sphere."""
        result = await self.db.execute(
            select(
                Agent.sphere_type,
                func.count(Agent.id)
            )
            .group_by(Agent.sphere_type)
        )
        
        return {row[0].value: row[1] for row in result.all()}
    
    # -------------------------------------------------------------------------
    # USER AGENT CONFIG
    # -------------------------------------------------------------------------
    
    async def get_user_agent_config(
        self,
        identity_id: UUID,
        agent_id: UUID,
    ) -> Optional[UserAgentConfig]:
        """Get user's configuration for an agent."""
        result = await self.db.execute(
            select(UserAgentConfig)
            .where(
                and_(
                    UserAgentConfig.identity_id == identity_id,
                    UserAgentConfig.agent_id == agent_id,
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_or_create_user_agent_config(
        self,
        identity_id: UUID,
        agent_id: UUID,
    ) -> UserAgentConfig:
        """Get or create user's configuration for an agent."""
        config = await self.get_user_agent_config(identity_id, agent_id)
        
        if not config:
            # Verify agent exists
            await self.get_agent(agent_id)
            
            config = UserAgentConfig(
                id=uuid4(),
                identity_id=identity_id,
                agent_id=agent_id,
                enabled=True,
            )
            self.db.add(config)
            await self.db.flush()
        
        return config
    
    async def update_user_agent_config(
        self,
        identity_id: UUID,
        agent_id: UUID,
        update_data: UserAgentConfigUpdate,
    ) -> UserAgentConfig:
        """Update user's agent configuration."""
        config = await self.get_or_create_user_agent_config(identity_id, agent_id)
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(config, key, value)
        
        await self.db.flush()
        return config
    
    async def list_user_agent_configs(
        self,
        identity_id: UUID,
        sphere_type: Optional[SphereType] = None,
    ) -> List[UserAgentConfig]:
        """List all agent configs for a user."""
        query = select(UserAgentConfig).where(
            UserAgentConfig.identity_id == identity_id
        )
        
        if sphere_type:
            query = query.join(Agent).where(Agent.sphere_type == sphere_type)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    # -------------------------------------------------------------------------
    # SEEDING
    # -------------------------------------------------------------------------
    
    async def seed_agents(self) -> int:
        """
        Seed the database with all 226 predefined agents.
        
        Returns number of agents created.
        """
        # Check if already seeded
        existing_count = await self.db.scalar(select(func.count(Agent.id)))
        if existing_count >= TOTAL_AGENTS:
            logger.info(f"Agents already seeded: {existing_count}")
            return 0
        
        agents_data = get_all_predefined_agents()
        created = 0
        
        for agent_data in agents_data:
            # Check if agent exists by name
            existing = await self.db.execute(
                select(Agent).where(Agent.name == agent_data["name"])
            )
            if existing.scalar_one_or_none():
                continue
            
            agent = Agent(
                id=agent_data["id"],
                name=agent_data["name"],
                display_name=agent_data["display_name"],
                description=agent_data["description"],
                sphere_type=agent_data["sphere_type"],
                status=agent_data["status"],
                capabilities=agent_data["capabilities"],
                scope=agent_data.get("scope", {}),
                default_token_budget=10000,
                max_token_budget=50000,
                cost_per_1k_tokens=0.01,
                requires_human_gate=agent_data["requires_human_gate"],
                human_gate_capabilities=agent_data["human_gate_capabilities"],
            )
            self.db.add(agent)
            created += 1
        
        await self.db.flush()
        logger.info(f"Seeded {created} agents")
        
        return created


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "AgentRegistryService",
    "get_all_predefined_agents",
    "AGENT_DISTRIBUTION",
    "TOTAL_AGENTS",
]
