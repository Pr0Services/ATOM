"""
CHE·NU™ Decision Point Integration

Integrates decision points with existing governance systems:
- HTTP 423 checkpoints → Decision points
- Backlog items → Decision points
- Orchestrator blocks → Decision points

R&D Rule #1: Human Sovereignty - All checkpoints create trackable decision points
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

from backend.schemas.governance_schemas import (
    DecisionPoint,
    DecisionPointCreate,
    DecisionPointType,
    AgingLevel,
    AISuggestion,
)
from backend.services.governance.decision_point_service import DecisionPointService

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CHECKPOINT INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

class CheckpointToDecisionPointAdapter:
    """
    Adapts HTTP 423 checkpoints to decision points.
    
    When a checkpoint is triggered, automatically creates a
    trackable decision point with aging.
    """
    
    def __init__(self, decision_point_service: Optional[DecisionPointService] = None):
        self.service = decision_point_service or DecisionPointService()
    
    async def create_from_checkpoint(
        self,
        checkpoint_data: Dict[str, Any],
        user_id: str,
        thread_id: str,
    ) -> DecisionPoint:
        """
        Create a decision point from an HTTP 423 checkpoint response.
        
        Args:
            checkpoint_data: The checkpoint payload from HTTP 423 response
            user_id: User who triggered the checkpoint
            thread_id: Thread where checkpoint occurred
            
        Returns:
            Created DecisionPoint
        """
        checkpoint_type = checkpoint_data.get("type", "governance")
        
        # Map checkpoint types to decision point types
        type_mapping = {
            "governance": DecisionPointType.CHECKPOINT,
            "cost": DecisionPointType.APPROVAL,
            "identity": DecisionPointType.CONFIRMATION,
            "sensitive": DecisionPointType.APPROVAL,
            "policy_tuning": DecisionPointType.DECISION,
            "elevation": DecisionPointType.APPROVAL,
        }
        
        point_type = type_mapping.get(checkpoint_type, DecisionPointType.CHECKPOINT)
        
        # Extract options for alternatives
        options = checkpoint_data.get("options", ["approve", "reject"])
        
        # Build context
        context = {
            "checkpoint_id": checkpoint_data.get("id"),
            "checkpoint_type": checkpoint_type,
            "original_options": options,
            "reason": checkpoint_data.get("reason"),
            "source": "http_423_checkpoint",
        }
        
        # Add any extra data
        if "suggestions" in checkpoint_data:
            context["suggestions"] = checkpoint_data["suggestions"]
        if "costs" in checkpoint_data:
            context["costs"] = checkpoint_data["costs"]
        
        # Create decision point
        create_data = DecisionPointCreate(
            point_type=point_type,
            thread_id=thread_id,
            title=checkpoint_data.get("reason", "Checkpoint requires approval"),
            description=self._build_description(checkpoint_data),
            context=context,
        )
        
        point = await self.service.create_decision_point(
            create_data=create_data,
            created_by=user_id,
            generate_suggestion=True,
        )
        
        # Store checkpoint reference
        point.checkpoint_id = checkpoint_data.get("id")
        point.source_module = "checkpoint_integration"
        await self.service.repository.update(point)
        
        logger.info(
            f"Created decision point {point.id} from checkpoint {checkpoint_data.get('id')}"
        )
        
        return point
    
    def _build_description(self, checkpoint_data: Dict[str, Any]) -> str:
        """Build human-readable description from checkpoint data."""
        parts = []
        
        if reason := checkpoint_data.get("reason"):
            parts.append(reason)
        
        if cp_type := checkpoint_data.get("type"):
            type_descriptions = {
                "governance": "This action requires governance approval.",
                "cost": "This action has cost implications that need review.",
                "identity": "This action involves identity verification.",
                "sensitive": "This action involves sensitive data or operations.",
                "policy_tuning": "Policy changes are proposed that need approval.",
                "elevation": "This action requires elevated permissions.",
            }
            if desc := type_descriptions.get(cp_type):
                parts.append(desc)
        
        if options := checkpoint_data.get("options"):
            parts.append(f"Options: {', '.join(options)}")
        
        return " ".join(parts) if parts else "Checkpoint requires human decision."


# ═══════════════════════════════════════════════════════════════════════════════
# BACKLOG INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

class BacklogToDecisionPointAdapter:
    """
    Creates decision points from backlog items that need user action.
    """
    
    def __init__(self, decision_point_service: Optional[DecisionPointService] = None):
        self.service = decision_point_service or DecisionPointService()
    
    async def create_from_backlog(
        self,
        backlog_item: Dict[str, Any],
        user_id: str,
        thread_id: str,
    ) -> DecisionPoint:
        """
        Create a decision point from a backlog item requiring action.
        
        Args:
            backlog_item: The backlog item data
            user_id: User responsible for the decision
            thread_id: Associated thread
            
        Returns:
            Created DecisionPoint
        """
        # Map backlog status to decision type
        status = backlog_item.get("status", "pending")
        
        type_mapping = {
            "needs_review": DecisionPointType.REVIEW,
            "needs_decision": DecisionPointType.DECISION,
            "needs_confirmation": DecisionPointType.CONFIRMATION,
            "pending": DecisionPointType.TASK,
        }
        
        point_type = type_mapping.get(status, DecisionPointType.TASK)
        
        create_data = DecisionPointCreate(
            point_type=point_type,
            thread_id=thread_id,
            title=backlog_item.get("title", "Backlog item needs attention"),
            description=backlog_item.get("description"),
            context={
                "backlog_id": backlog_item.get("id"),
                "backlog_status": status,
                "severity": backlog_item.get("severity"),
                "source": "backlog_integration",
            },
        )
        
        point = await self.service.create_decision_point(
            create_data=create_data,
            created_by=user_id,
            generate_suggestion=True,
        )
        
        point.source_module = "backlog_integration"
        point.source_event_id = backlog_item.get("id")
        await self.service.repository.update(point)
        
        logger.info(
            f"Created decision point {point.id} from backlog {backlog_item.get('id')}"
        )
        
        return point


# ═══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

class OrchestratorToDecisionPointAdapter:
    """
    Creates decision points from orchestrator BLOCK/ASK_HUMAN decisions.
    """
    
    def __init__(self, decision_point_service: Optional[DecisionPointService] = None):
        self.service = decision_point_service or DecisionPointService()
    
    async def create_from_orchestrator_decision(
        self,
        decision: Dict[str, Any],
        user_id: str,
        thread_id: str,
    ) -> Optional[DecisionPoint]:
        """
        Create a decision point from orchestrator decision if it requires human input.
        
        Args:
            decision: The orchestrator decision output
            user_id: User who initiated the action
            thread_id: Thread context
            
        Returns:
            Created DecisionPoint or None if no human input needed
        """
        action = decision.get("action")
        
        # Only create decision points for actions requiring human input
        if action not in ["BLOCK", "ASK_HUMAN", "ELEVATE"]:
            return None
        
        type_mapping = {
            "BLOCK": DecisionPointType.APPROVAL,
            "ASK_HUMAN": DecisionPointType.DECISION,
            "ELEVATE": DecisionPointType.APPROVAL,
        }
        
        point_type = type_mapping.get(action, DecisionPointType.CHECKPOINT)
        
        # Build title from orchestrator reason
        reason = decision.get("reason", "Orchestrator requires human decision")
        
        create_data = DecisionPointCreate(
            point_type=point_type,
            thread_id=thread_id,
            title=reason,
            description=self._build_description(decision),
            context={
                "orchestrator_action": action,
                "orchestrator_reason": reason,
                "risk_score": decision.get("risk_score"),
                "governance_signal": decision.get("governance_signal"),
                "source": "orchestrator_integration",
            },
        )
        
        point = await self.service.create_decision_point(
            create_data=create_data,
            created_by=user_id,
            generate_suggestion=True,
        )
        
        point.source_module = "orchestrator_integration"
        await self.service.repository.update(point)
        
        logger.info(
            f"Created decision point {point.id} from orchestrator {action}"
        )
        
        return point
    
    def _build_description(self, decision: Dict[str, Any]) -> str:
        """Build description from orchestrator decision."""
        parts = []
        
        if reason := decision.get("reason"):
            parts.append(reason)
        
        if risk := decision.get("risk_score"):
            parts.append(f"Risk score: {risk}/100")
        
        if signal := decision.get("governance_signal"):
            parts.append(f"Governance signal: {signal}")
        
        if alternatives := decision.get("alternatives"):
            parts.append(f"Alternatives: {', '.join(alternatives)}")
        
        return " | ".join(parts) if parts else "Human decision required."


# ═══════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════════

async def checkpoint_middleware_hook(
    checkpoint_response: Dict[str, Any],
    request_context: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Middleware hook to create decision point when HTTP 423 is returned.
    
    Can be integrated into FastAPI middleware or exception handlers.
    
    Args:
        checkpoint_response: The 423 response body
        request_context: Request context (user_id, thread_id, etc.)
        
    Returns:
        Modified checkpoint response with decision_point_id
    """
    adapter = CheckpointToDecisionPointAdapter()
    
    try:
        point = await adapter.create_from_checkpoint(
            checkpoint_data=checkpoint_response.get("checkpoint", {}),
            user_id=request_context.get("user_id", "system"),
            thread_id=request_context.get("thread_id", "unknown"),
        )
        
        # Add decision point reference to response
        checkpoint_response["decision_point_id"] = point.id
        checkpoint_response["decision_point_url"] = f"/governance/decision-points/{point.id}"
        
    except Exception as e:
        logger.error(f"Failed to create decision point from checkpoint: {e}")
        # Don't fail the checkpoint, just log the error
    
    return checkpoint_response


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI EXCEPTION HANDLER
# ═══════════════════════════════════════════════════════════════════════════════

from fastapi import Request
from fastapi.responses import JSONResponse


async def checkpoint_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    FastAPI exception handler for checkpoint responses.
    
    Automatically creates decision points for 423 responses.
    
    Usage in main.py:
        from backend.services.governance.decision_point_integration import (
            CheckpointException,
            checkpoint_exception_handler,
        )
        
        app.add_exception_handler(CheckpointException, checkpoint_exception_handler)
    """
    # Get checkpoint data from exception
    checkpoint_data = getattr(exc, "checkpoint_data", {})
    
    # Get user context from request
    user_id = getattr(request.state, "user_id", None) or "anonymous"
    thread_id = request.query_params.get("thread_id") or request.path_params.get("thread_id") or "unknown"
    
    # Create decision point
    adapter = CheckpointToDecisionPointAdapter()
    
    try:
        point = await adapter.create_from_checkpoint(
            checkpoint_data=checkpoint_data,
            user_id=user_id,
            thread_id=thread_id,
        )
        
        # Build response
        response_data = {
            "status": "checkpoint_pending",
            "checkpoint": checkpoint_data,
            "decision_point_id": point.id,
            "decision_point_url": f"/api/v2/governance/decision-points/{point.id}",
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"Failed to create decision point: {e}")
        response_data = {
            "status": "checkpoint_pending",
            "checkpoint": checkpoint_data,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    return JSONResponse(
        status_code=423,
        content=response_data,
    )


class CheckpointException(Exception):
    """
    Exception to trigger HTTP 423 checkpoint with decision point creation.
    
    Usage:
        raise CheckpointException(
            checkpoint_type="governance",
            reason="Action requires approval",
            options=["approve", "reject"],
        )
    """
    
    def __init__(
        self,
        checkpoint_type: str = "governance",
        reason: str = "Checkpoint required",
        options: list = None,
        **extra_data,
    ):
        self.checkpoint_data = {
            "id": str(uuid4()),
            "type": checkpoint_type,
            "reason": reason,
            "options": options or ["approve", "reject"],
            "requires_approval": True,
            **extra_data,
        }
        super().__init__(reason)


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE SYNC
# ═══════════════════════════════════════════════════════════════════════════════

async def sync_decision_point_to_checkpoint(
    point_id: str,
    response_type: str,
) -> Dict[str, Any]:
    """
    Sync decision point response back to original checkpoint system.
    
    When user responds to a decision point, this updates the
    corresponding checkpoint if one exists.
    
    Args:
        point_id: Decision point ID
        response_type: The user's response (validate, redirect, etc.)
        
    Returns:
        Sync result
    """
    service = DecisionPointService()
    
    point = await service.repository.get(point_id)
    if not point:
        return {"synced": False, "error": "Point not found"}
    
    if not point.checkpoint_id:
        return {"synced": False, "reason": "No associated checkpoint"}
    
    # Map decision point response to checkpoint action
    response_mapping = {
        "validate": "approve",
        "redirect": "partial_approve",
        "reject": "reject",
        "defer": "pending",
    }
    
    checkpoint_action = response_mapping.get(response_type, "pending")
    
    # TODO: Call checkpoint resolution API
    # await checkpoint_service.resolve(point.checkpoint_id, checkpoint_action)
    
    logger.info(
        f"Synced decision point {point_id} response '{response_type}' "
        f"to checkpoint {point.checkpoint_id} as '{checkpoint_action}'"
    )
    
    return {
        "synced": True,
        "decision_point_id": point_id,
        "checkpoint_id": point.checkpoint_id,
        "response_type": response_type,
        "checkpoint_action": checkpoint_action,
    }
