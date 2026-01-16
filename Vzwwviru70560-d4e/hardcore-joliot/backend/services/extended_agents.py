"""
CHE·NU™ Extended Agents - Additional Sphere Agents
===================================================

New agents added in V72 for Gap Analysis Round 1:
- Immobilier Domain: 20 new agents (NEW SPHERE)
- Scholar Extensions: 5 new agents
- Business Extensions: 7 new agents
- Government Extensions: 4 new agents
- Personal Extensions: 4 new agents
- Creative Studio Extensions: 3 new agents
- Community Extensions: 3 new agents
- Social Media Extensions: 3 new agents
- Entertainment Extensions: 2 new agents
- My Team Extensions: 3 new agents
- Core/System: 30 agents (cross-sphere)

Total: +84 new agents → 310 total sphere agents

R&D COMPLIANCE:
- Rule #1: Human Sovereignty - all sensitive actions require gates
- Rule #4: No AI-to-AI orchestration
- Rule #5: No ranking/engagement optimization in Social
- Rule #6: Full traceability
"""

from __future__ import annotations

from typing import List, Dict, Any
from uuid import uuid4

from backend.models.agent import AgentStatus, SphereType


# =============================================================================
# IMMOBILIER DOMAIN (20 NEW AGENTS)
# =============================================================================

def _get_immobilier_agents() -> List[Dict[str, Any]]:
    """
    20 Immobilier domain agents (NEW).
    
    Focused on Quebec real estate with RBQ compliance.
    """
    return [
        # Property Management
        {"name": "immobilier_property_manager", "display_name": "Property Manager", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
        {"name": "immobilier_tenant_manager", "display_name": "Tenant Manager", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True, "human_gate_capabilities": ["notification_draft"]},
        {"name": "immobilier_lease_generator", "display_name": "Lease Generator", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": True},
        {"name": "immobilier_rent_tracker", "display_name": "Rent Tracker", "capabilities": ["data_processing", "analysis"], "requires_human_gate": False},
        {"name": "immobilier_maintenance_coordinator", "display_name": "Maintenance Coordinator", "capabilities": ["recommendation", "notification_draft"], "requires_human_gate": True},
        
        # Financial Analysis
        {"name": "immobilier_roi_calculator", "display_name": "ROI Calculator", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "immobilier_cap_rate_analyzer", "display_name": "Cap Rate Analyzer", "capabilities": ["analysis"], "requires_human_gate": False},
        {"name": "immobilier_cash_flow_projector", "display_name": "Cash Flow Projector", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "immobilier_expense_tracker", "display_name": "Expense Tracker", "capabilities": ["data_processing", "classification"], "requires_human_gate": False},
        {"name": "immobilier_tax_estimator", "display_name": "Tax Estimator", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        
        # Quebec Compliance (RBQ)
        {"name": "immobilier_rbq_compliance", "display_name": "RBQ Compliance Checker", "capabilities": ["fact_check", "analysis"], "requires_human_gate": False},
        {"name": "immobilier_permit_tracker", "display_name": "Permit Tracker", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
        {"name": "immobilier_inspection_scheduler", "display_name": "Inspection Scheduler", "capabilities": ["recommendation"], "requires_human_gate": False},
        {"name": "immobilier_license_verifier", "display_name": "Contractor License Verifier", "capabilities": ["fact_check", "research"], "requires_human_gate": False},
        
        # Development Projects
        {"name": "immobilier_project_pipeline", "display_name": "Project Pipeline Manager", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
        {"name": "immobilier_budget_tracker", "display_name": "Construction Budget Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "immobilier_timeline_planner", "display_name": "Project Timeline Planner", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "immobilier_punch_list", "display_name": "Punch List Manager", "capabilities": ["data_processing", "prioritization"], "requires_human_gate": False},
        
        # Marketing & Sales
        {"name": "immobilier_listing_writer", "display_name": "Listing Writer", "capabilities": ["text_generation", "content_planning"], "requires_human_gate": True},
        {"name": "immobilier_market_analyzer", "display_name": "Market Analyzer", "capabilities": ["research", "analysis"], "requires_human_gate": False},
    ]


# =============================================================================
# SCHOLAR EXTENSIONS (+5)
# =============================================================================

def _get_scholar_extension_agents() -> List[Dict[str, Any]]:
    """5 new Scholar agents for Gap Analysis."""
    return [
        {"name": "scholar_pubmed_integrator", "display_name": "PubMed Integrator", "capabilities": ["research", "search"], "requires_human_gate": False},
        {"name": "scholar_reference_importer", "display_name": "Reference Importer", "capabilities": ["data_processing", "extraction"], "requires_human_gate": False},
        {"name": "scholar_manuscript_collaborator", "display_name": "Manuscript Collaborator", "capabilities": ["text_generation", "analysis"], "requires_human_gate": False},
        {"name": "scholar_figure_generator", "display_name": "Figure/Table Generator", "capabilities": ["design_assist", "data_processing"], "requires_human_gate": False},
        {"name": "scholar_citation_formatter", "display_name": "Citation Formatter", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": False},
    ]


# =============================================================================
# BUSINESS EXTENSIONS (+7)
# =============================================================================

def _get_business_extension_agents() -> List[Dict[str, Any]]:
    """7 new Business agents for Gap Analysis."""
    return [
        # Quebec-specific
        {"name": "business_tvq_tps_calculator", "display_name": "TVQ/TPS Calculator", "capabilities": ["data_processing", "analysis"], "requires_human_gate": False},
        {"name": "business_quebec_invoice", "display_name": "Quebec Invoice Generator", "capabilities": ["document_processing"], "requires_human_gate": True},
        
        # Inventory & Pipeline
        {"name": "business_inventory_tracker", "display_name": "Inventory Tracker", "capabilities": ["data_processing", "notification_draft"], "requires_human_gate": True},
        {"name": "business_repair_pipeline", "display_name": "Repair Pipeline Manager", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
        
        # Coaching/Services
        {"name": "business_coaching_manager", "display_name": "Coaching Client Manager", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
        {"name": "business_program_builder", "display_name": "Program Builder", "capabilities": ["content_planning", "text_generation"], "requires_human_gate": False},
        
        # Sponsorships
        {"name": "business_sponsorship_tracker", "display_name": "Sponsorship Tracker", "capabilities": ["data_processing", "analysis"], "requires_human_gate": False},
    ]


# =============================================================================
# GOVERNMENT EXTENSIONS (+4)
# =============================================================================

def _get_government_extension_agents() -> List[Dict[str, Any]]:
    """4 new Government agents for Gap Analysis."""
    return [
        {"name": "gov_clinical_compliance", "display_name": "Clinical Trial Compliance", "capabilities": ["analysis", "fact_check"], "requires_human_gate": False},
        {"name": "gov_health_canada_tracker", "display_name": "Health Canada Tracker", "capabilities": ["research", "data_processing"], "requires_human_gate": False},
        {"name": "gov_reb_submission", "display_name": "REB Submission Helper", "capabilities": ["document_processing", "text_generation"], "requires_human_gate": True},
        {"name": "gov_adverse_event_reporter", "display_name": "Adverse Event Reporter", "capabilities": ["document_processing", "data_processing"], "requires_human_gate": True},
    ]


# =============================================================================
# PERSONAL EXTENSIONS (+4)
# =============================================================================

def _get_personal_extension_agents() -> List[Dict[str, Any]]:
    """4 new Personal agents for Gap Analysis."""
    return [
        {"name": "personal_calendar_sync", "display_name": "Calendar Sync", "capabilities": ["data_processing"], "requires_human_gate": False},
        {"name": "personal_unified_inbox", "display_name": "Unified Inbox", "capabilities": ["classification", "prioritization"], "requires_human_gate": False},
        {"name": "personal_observation_noter", "display_name": "Observation Noter (iNaturalist)", "capabilities": ["text_generation", "classification"], "requires_human_gate": False},
        {"name": "personal_multi_context_task", "display_name": "Multi-Context Task Manager", "capabilities": ["prioritization", "recommendation"], "requires_human_gate": False},
    ]


# =============================================================================
# CREATIVE STUDIO EXTENSIONS (+3)
# =============================================================================

def _get_creative_extension_agents() -> List[Dict[str, Any]]:
    """3 new Creative Studio agents for Gap Analysis."""
    return [
        {"name": "creative_batch_generator", "display_name": "Batch Image Generator", "capabilities": ["image_generation"], "requires_human_gate": True},
        {"name": "creative_branding_kit", "display_name": "Branding Kit Creator", "capabilities": ["design_assist", "content_planning"], "requires_human_gate": False},
        {"name": "creative_ab_tester", "display_name": "A/B Thumbnail Tester", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
    ]


# =============================================================================
# COMMUNITY EXTENSIONS (+3)
# =============================================================================

def _get_community_extension_agents() -> List[Dict[str, Any]]:
    """3 new Community agents for Gap Analysis."""
    return [
        {"name": "community_group_coordinator", "display_name": "Group Coordinator", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "community_file_sharer", "display_name": "File Sharer", "capabilities": ["data_processing"], "requires_human_gate": False},
        {"name": "community_decision_poll", "display_name": "Decision Poll Creator", "capabilities": ["content_planning"], "requires_human_gate": False},
    ]


# =============================================================================
# SOCIAL MEDIA EXTENSIONS (+3) - NO RANKING/ENGAGEMENT (Rule #5)
# =============================================================================

def _get_social_extension_agents() -> List[Dict[str, Any]]:
    """3 new Social Media agents - NO ranking optimization (Rule #5)."""
    return [
        {"name": "social_content_calendar", "display_name": "Content Calendar Manager", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "social_analytics_reader", "display_name": "Analytics Reader", "capabilities": ["analysis", "summarization"], "requires_human_gate": False},
        {"name": "social_best_time_suggester", "display_name": "Best Time Suggester", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        # NOTE: NO engagement_bot, NO ranking_optimizer - Rule #5 compliance
    ]


# =============================================================================
# ENTERTAINMENT EXTENSIONS (+2)
# =============================================================================

def _get_entertainment_extension_agents() -> List[Dict[str, Any]]:
    """2 new Entertainment agents for Gap Analysis."""
    return [
        {"name": "entertainment_watch_party", "display_name": "Watch Party Organizer", "capabilities": ["content_planning", "recommendation"], "requires_human_gate": False},
        {"name": "entertainment_content_tracker", "display_name": "Content Tracker", "capabilities": ["data_processing", "recommendation"], "requires_human_gate": False},
    ]


# =============================================================================
# MY TEAM EXTENSIONS (+3) - NO ORCHESTRATOR (Rule #4)
# =============================================================================

def _get_myteam_extension_agents() -> List[Dict[str, Any]]:
    """3 new My Team agents - NO AI-to-AI orchestration (Rule #4)."""
    return [
        {"name": "team_async_update", "display_name": "Async Update Manager", "capabilities": ["summarization", "notification_draft"], "requires_human_gate": True},
        {"name": "team_project_health", "display_name": "Project Health Monitor", "capabilities": ["analysis", "recommendation"], "requires_human_gate": False},
        {"name": "team_decision_logger", "display_name": "Decision Logger", "capabilities": ["data_processing", "summarization"], "requires_human_gate": False},
        # NOTE: NO orchestrator, NO agent_coordinator - Rule #4 compliance
    ]


# =============================================================================
# CORE/SYSTEM AGENTS (+30 cross-sphere)
# =============================================================================

def _get_core_agents() -> List[Dict[str, Any]]:
    """
    30 Core/System agents (cross-sphere).
    
    These agents work across all spheres for system-level functions.
    """
    return [
        # Thread Agents (system-created with each Thread)
        {"name": "core_thread_context", "display_name": "Thread Context Manager", "capabilities": ["summarization", "extraction"], "requires_human_gate": False},
        {"name": "core_thread_memory", "display_name": "Thread Memory Keeper", "capabilities": ["summarization", "data_processing"], "requires_human_gate": False},
        {"name": "core_thread_action_tracker", "display_name": "Thread Action Tracker", "capabilities": ["prioritization", "data_processing"], "requires_human_gate": False},
        
        # Search & Retrieval
        {"name": "core_universal_search", "display_name": "Universal Search", "capabilities": ["search", "research"], "requires_human_gate": False},
        {"name": "core_knowledge_retriever", "display_name": "Knowledge Retriever", "capabilities": ["search", "summarization"], "requires_human_gate": False},
        {"name": "core_cross_sphere_finder", "display_name": "Cross-Sphere Finder", "capabilities": ["search"], "requires_human_gate": False},
        
        # Analytics & Insights
        {"name": "core_usage_analyzer", "display_name": "Usage Analyzer", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "core_cost_tracker", "display_name": "Token Cost Tracker", "capabilities": ["analysis", "data_processing"], "requires_human_gate": False},
        {"name": "core_performance_monitor", "display_name": "Performance Monitor", "capabilities": ["analysis"], "requires_human_gate": False},
        
        # Security & Governance
        {"name": "core_permission_checker", "display_name": "Permission Checker", "capabilities": ["analysis", "fact_check"], "requires_human_gate": False},
        {"name": "core_audit_logger", "display_name": "Audit Logger", "capabilities": ["data_processing"], "requires_human_gate": False},
        {"name": "core_checkpoint_manager", "display_name": "Checkpoint Manager", "capabilities": ["data_processing"], "requires_human_gate": False},
        
        # Data & Integration
        {"name": "core_import_helper", "display_name": "Import Helper", "capabilities": ["data_processing", "extraction"], "requires_human_gate": False},
        {"name": "core_export_helper", "display_name": "Export Helper", "capabilities": ["document_processing", "data_processing"], "requires_human_gate": True},
        {"name": "core_sync_manager", "display_name": "Sync Manager", "capabilities": ["data_processing"], "requires_human_gate": False},
        {"name": "core_backup_agent", "display_name": "Backup Agent", "capabilities": ["data_processing"], "requires_human_gate": True},
        
        # Notifications & Communication
        {"name": "core_notification_router", "display_name": "Notification Router", "capabilities": ["notification_draft", "prioritization"], "requires_human_gate": True},
        {"name": "core_digest_creator", "display_name": "Digest Creator", "capabilities": ["summarization", "content_planning"], "requires_human_gate": False},
        {"name": "core_reminder_manager", "display_name": "Reminder Manager", "capabilities": ["notification_draft"], "requires_human_gate": True},
        
        # Help & Onboarding
        {"name": "core_help_assistant", "display_name": "Help Assistant", "capabilities": ["recommendation", "text_generation"], "requires_human_gate": False},
        {"name": "core_onboarding_guide", "display_name": "Onboarding Guide", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
        {"name": "core_feature_explainer", "display_name": "Feature Explainer", "capabilities": ["text_generation"], "requires_human_gate": False},
        
        # XR & Environment
        {"name": "core_xr_environment", "display_name": "XR Environment Generator", "capabilities": ["design_assist"], "requires_human_gate": False},
        {"name": "core_spatial_organizer", "display_name": "Spatial Organizer", "capabilities": ["recommendation", "content_planning"], "requires_human_gate": False},
        
        # Intent & Planning
        {"name": "core_intent_analyzer", "display_name": "Intent Analyzer", "capabilities": ["analysis", "classification"], "requires_human_gate": False},
        {"name": "core_task_decomposer", "display_name": "Task Decomposer", "capabilities": ["analysis", "content_planning"], "requires_human_gate": False},
        {"name": "core_priority_scorer", "display_name": "Priority Scorer", "capabilities": ["scoring", "prioritization"], "requires_human_gate": False},
        
        # Translation & Formatting
        {"name": "core_translator", "display_name": "Translator", "capabilities": ["text_generation"], "requires_human_gate": False},
        {"name": "core_formatter", "display_name": "Document Formatter", "capabilities": ["document_processing"], "requires_human_gate": False},
        {"name": "core_summarizer", "display_name": "Universal Summarizer", "capabilities": ["summarization"], "requires_human_gate": False},
    ]


# =============================================================================
# AGGREGATE FUNCTION
# =============================================================================

def get_all_extended_agents() -> List[Dict[str, Any]]:
    """
    Get all extended agents (+84 new agents).
    
    Returns list of agent definitions ready for database seeding.
    """
    agents = []
    
    # Immobilier (new domain) - using BUSINESS for now until SphereType is extended
    for agent_def in _get_immobilier_agents():
        agent_def["sphere_type"] = SphereType.BUSINESS  # Will be changed to IMMOBILIER
        agent_def["id"] = uuid4()
        agent_def["status"] = AgentStatus.ACTIVE
        agent_def.setdefault("requires_human_gate", False)
        agent_def.setdefault("human_gate_capabilities", [])
        agent_def.setdefault("description", f"{agent_def['display_name']} - Immobilier Domain")
        agents.append(agent_def)
    
    # Extensions by sphere
    extensions = {
        SphereType.SCHOLAR: _get_scholar_extension_agents,
        SphereType.BUSINESS: _get_business_extension_agents,
        SphereType.GOVERNMENT: _get_government_extension_agents,
        SphereType.PERSONAL: _get_personal_extension_agents,
        SphereType.CREATIVE_STUDIO: _get_creative_extension_agents,
        SphereType.COMMUNITY: _get_community_extension_agents,
        SphereType.SOCIAL_MEDIA: _get_social_extension_agents,
        SphereType.ENTERTAINMENT: _get_entertainment_extension_agents,
        SphereType.MY_TEAM: _get_myteam_extension_agents,
    }
    
    for sphere_type, generator in extensions.items():
        for agent_def in generator():
            agent_def["sphere_type"] = sphere_type
            agent_def["id"] = uuid4()
            agent_def["status"] = AgentStatus.ACTIVE
            agent_def.setdefault("requires_human_gate", False)
            agent_def.setdefault("human_gate_capabilities", [])
            agent_def.setdefault("description", f"{agent_def['display_name']} for {sphere_type.value} sphere")
            agents.append(agent_def)
    
    # Core agents (cross-sphere)
    for agent_def in _get_core_agents():
        agent_def["sphere_type"] = SphereType.PERSONAL  # Core agents default to Personal
        agent_def["id"] = uuid4()
        agent_def["status"] = AgentStatus.ACTIVE
        agent_def.setdefault("requires_human_gate", False)
        agent_def.setdefault("human_gate_capabilities", [])
        agent_def.setdefault("description", f"{agent_def['display_name']} - Core System Agent")
        agent_def["is_core_agent"] = True  # Mark as core agent
        agents.append(agent_def)
    
    return agents


# Agent counts for reference
EXTENDED_AGENT_COUNTS = {
    "immobilier": 20,
    "scholar_ext": 5,
    "business_ext": 7,
    "government_ext": 4,
    "personal_ext": 4,
    "creative_ext": 3,
    "community_ext": 3,
    "social_ext": 3,
    "entertainment_ext": 2,
    "myteam_ext": 3,
    "core": 30,
}

TOTAL_EXTENDED_AGENTS = sum(EXTENDED_AGENT_COUNTS.values())  # 84

# Grand total: 226 (original) + 84 (extended) = 310
GRAND_TOTAL_SPHERE_AGENTS = 226 + TOTAL_EXTENDED_AGENTS  # 310
