"""
CHE·NU™ V75 — YELLOW PAGES MODULE
===================================

Agent directory and discovery service.

Version: 75.0
Status: PRODUCTION
R&D Compliance: ✅ Rule #1-7
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
import logging

logger = logging.getLogger("chenu.v75.yellow_pages")


class AgentCategory(str, Enum):
    """Agent categories"""
    ASSISTANT = "assistant"
    ANALYST = "analyst"
    CREATOR = "creator"
    MANAGER = "manager"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"


class AgentStatus(str, Enum):
    """Agent availability status"""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


@dataclass
class AgentProfile:
    """
    Complete agent profile for directory.
    
    R&D Compliance:
    - Rule #6: Complete traceability
    """
    id: str
    name: str
    description: str
    
    # Classification
    sphere: str
    category: AgentCategory
    
    # Capabilities
    capabilities: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    
    # Constraints
    scope: List[str] = field(default_factory=list)
    token_budget: int = 10000
    
    # Status
    status: AgentStatus = AgentStatus.AVAILABLE
    
    # Metrics
    tasks_completed: int = 0
    success_rate: float = 0.0
    average_response_time_ms: float = 0.0
    
    # Metadata
    version: str = "1.0"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class YellowPagesService:
    """
    Yellow Pages - Agent Directory Service.
    
    Provides agent discovery, search, and recommendation.
    
    R&D Compliance:
    - Rule #1: Human Sovereignty - recommendations only, human chooses
    - Rule #4: My Team - transparent agent listing
    """
    
    # Pre-registered CHE·NU agents (226 total)
    SPHERE_AGENTS = {
        "personal": {
            "count": 28,
            "agents": [
                "note_assistant", "task_manager", "habit_tracker",
                "calendar_sync", "goal_setter", "memory_companion",
                "focus_coach", "wellness_advisor", "finance_helper",
                "learning_guide"
            ]
        },
        "business": {
            "count": 43,
            "agents": [
                "crm_agent", "invoice_generator", "contract_manager",
                "proposal_builder", "lead_scorer", "sales_forecaster",
                "client_communicator", "meeting_scheduler", "report_builder",
                "market_analyst"
            ]
        },
        "government": {
            "count": 18,
            "agents": [
                "compliance_checker", "regulation_tracker", "permit_assistant",
                "tax_advisor", "grant_finder", "policy_analyzer"
            ]
        },
        "creative": {
            "count": 42,
            "agents": [
                "image_generator", "voice_synthesizer", "video_editor",
                "music_composer", "thumbnail_creator", "content_writer",
                "design_assistant", "brand_advisor", "social_creator",
                "animation_builder"
            ]
        },
        "community": {
            "count": 12,
            "agents": [
                "event_planner", "group_coordinator", "volunteer_manager",
                "communication_hub", "poll_creator", "resource_sharer"
            ]
        },
        "social": {
            "count": 15,
            "agents": [
                "content_scheduler", "analytics_tracker", "engagement_monitor",
                "hashtag_suggester", "audience_analyzer", "cross_poster"
            ]
        },
        "entertainment": {
            "count": 8,
            "agents": [
                "game_recommender", "media_curator", "playlist_builder",
                "watch_tracker", "review_collector"
            ]
        },
        "team": {
            "count": 35,
            "agents": [
                "project_coordinator", "task_assigner", "progress_tracker",
                "standup_facilitator", "resource_allocator", "timeline_manager",
                "quality_reviewer", "documentation_helper", "onboarding_guide",
                "feedback_collector"
            ]
        },
        "scholar": {
            "count": 25,
            "agents": [
                "literature_searcher", "reference_manager", "citation_formatter",
                "manuscript_assistant", "peer_review_helper", "data_analyzer",
                "visualization_creator", "methodology_advisor", "publishing_guide",
                "research_tracker"
            ]
        }
    }
    
    def __init__(self):
        self._agents: Dict[str, AgentProfile] = {}
        self._sphere_index: Dict[str, List[str]] = {}
        self._capability_index: Dict[str, List[str]] = {}
        self._initialize_agents()
        logger.info(f"YellowPagesService initialized with {len(self._agents)} agents")
    
    def _initialize_agents(self):
        """Initialize all CHE·NU agents"""
        for sphere, data in self.SPHERE_AGENTS.items():
            self._sphere_index[sphere] = []
            
            for agent_name in data["agents"]:
                agent_id = f"{sphere}_{agent_name}"
                
                profile = AgentProfile(
                    id=agent_id,
                    name=agent_name.replace("_", " ").title(),
                    description=f"{agent_name} for {sphere} sphere",
                    sphere=sphere,
                    category=AgentCategory.ASSISTANT,
                    capabilities=[agent_name],
                    scope=[sphere]
                )
                
                self._agents[agent_id] = profile
                self._sphere_index[sphere].append(agent_id)
                
                # Index by capability
                for cap in profile.capabilities:
                    if cap not in self._capability_index:
                        self._capability_index[cap] = []
                    self._capability_index[cap].append(agent_id)
    
    def search(
        self,
        query: Optional[str] = None,
        sphere: Optional[str] = None,
        category: Optional[AgentCategory] = None,
        capability: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search agents by various criteria.
        
        Args:
            query: Text search in name/description
            sphere: Filter by sphere
            category: Filter by category
            capability: Filter by capability
            limit: Max results
            
        Returns:
            List of matching agent profiles
        """
        results = list(self._agents.values())
        
        # Apply filters
        if sphere:
            results = [a for a in results if a.sphere == sphere]
        
        if category:
            results = [a for a in results if a.category == category]
        
        if capability:
            results = [a for a in results if capability in a.capabilities]
        
        if query:
            query_lower = query.lower()
            results = [
                a for a in results
                if query_lower in a.name.lower() or query_lower in a.description.lower()
            ]
        
        # Apply limit
        results = results[:limit]
        
        return [self._profile_to_dict(a) for a in results]
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        agent = self._agents.get(agent_id)
        if agent:
            return self._profile_to_dict(agent)
        return None
    
    def list_by_sphere(self, sphere: str) -> List[Dict[str, Any]]:
        """List all agents in a sphere"""
        agent_ids = self._sphere_index.get(sphere, [])
        return [
            self._profile_to_dict(self._agents[aid])
            for aid in agent_ids
        ]
    
    def recommend_agents(
        self,
        task_description: str,
        sphere: Optional[str] = None,
        max_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Recommend agents for a task.
        
        GOVERNANCE: These are RECOMMENDATIONS only.
        Human must select which agent(s) to use.
        
        Args:
            task_description: Description of the task
            sphere: Preferred sphere (optional)
            max_recommendations: Max agents to recommend
            
        Returns:
            List of recommended agents with scores
        """
        candidates = list(self._agents.values())
        
        if sphere:
            candidates = [a for a in candidates if a.sphere == sphere]
        
        # Simple keyword matching (in production: use embeddings)
        task_words = set(task_description.lower().split())
        
        scored = []
        for agent in candidates:
            agent_words = set(
                agent.name.lower().split() +
                agent.description.lower().split() +
                [c.lower() for c in agent.capabilities]
            )
            
            overlap = len(task_words & agent_words)
            if overlap > 0:
                scored.append((agent, overlap))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for agent, score in scored[:max_recommendations]:
            rec = self._profile_to_dict(agent)
            rec["recommendation_score"] = score
            rec["recommendation_note"] = "Based on task keyword matching"
            recommendations.append(rec)
        
        return recommendations
    
    def get_sphere_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics per sphere"""
        stats = {}
        
        for sphere, agent_ids in self._sphere_index.items():
            agents = [self._agents[aid] for aid in agent_ids]
            
            stats[sphere] = {
                "total_agents": len(agents),
                "available": sum(1 for a in agents if a.status == AgentStatus.AVAILABLE),
                "categories": list(set(a.category.value for a in agents))
            }
        
        return stats
    
    def get_total_count(self) -> int:
        """Get total agent count"""
        return len(self._agents)
    
    def _profile_to_dict(self, profile: AgentProfile) -> Dict[str, Any]:
        """Convert AgentProfile to dict"""
        return {
            "id": profile.id,
            "name": profile.name,
            "description": profile.description,
            "sphere": profile.sphere,
            "category": profile.category.value,
            "capabilities": profile.capabilities,
            "skills": profile.skills,
            "scope": profile.scope,
            "token_budget": profile.token_budget,
            "status": profile.status.value,
            "metrics": {
                "tasks_completed": profile.tasks_completed,
                "success_rate": profile.success_rate,
                "average_response_time_ms": profile.average_response_time_ms
            },
            "version": profile.version
        }


# Singleton
_service: Optional[YellowPagesService] = None


def get_yellow_pages() -> YellowPagesService:
    """Get or create YellowPagesService instance"""
    global _service
    if _service is None:
        _service = YellowPagesService()
    return _service


# Export
__all__ = [
    "YellowPagesService",
    "AgentProfile",
    "AgentCategory",
    "AgentStatus",
    "get_yellow_pages"
]
