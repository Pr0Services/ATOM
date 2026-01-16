# Creative Studio Cross-Sphere Workflows
# Complete Implementation

from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from ...core.auth import get_current_user
from ...core.sphere_orchestrator import SphereOrchestrator
from ...agents.creative_studio import WorkflowOrchestrator

router = APIRouter(prefix="/api/creative-studio/workflows", tags=["Workflows"])

# WORKFLOW 3: VIDEO → SOCIAL → ANALYTICS (SUITE)
@router.post("/video-distribution")
async def video_distribution_workflow(
    video_project_id: str,
    current_user = Depends(get_current_user)
):
    """Complete video distribution workflow"""
    
    orchestrator = SphereOrchestrator()
    workflow_agent = WorkflowOrchestrator()
    
    # Get video project
    video_project = await workflow_agent.get_video_project(video_project_id)
    
    # Generate platform versions
    platform_versions = await workflow_agent.generate_platform_versions(video_project)
    
    # Schedule distribution
    distribution = await orchestrator.distribute_multi_platform(platform_versions)
    
    return {
        "success": True,
        "distributed_to": len(distribution),
        "analytics_url": distribution["analytics_url"]
    }

# WORKFLOW TEMPLATES
@router.get("/templates")
async def list_workflow_templates():
    """List all available workflow templates"""
    
    templates = [
        {
            "id": "arch_to_marketing",
            "name": "Architecture → Marketing",
            "spheres": ["creative_studio", "business", "social_media"]
        },
        {
            "id": "rebrand",
            "name": "Brand Redesign Workflow",
            "spheres": ["creative_studio", "business", "social_media"]
        },
        {
            "id": "video_distribution",
            "name": "Video Multi-Platform Distribution",
            "spheres": ["creative_studio", "social_media", "business"]
        }
    ]
    
    return {"templates": templates}
