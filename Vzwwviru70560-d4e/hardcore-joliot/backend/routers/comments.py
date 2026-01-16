"""
CHE·NU™ V75 - Comments Router
Comments & Annotations API.

Comments = Discussions, annotations, feedback across resources

GOUVERNANCE > EXÉCUTION

@version 75.0.0
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class CommentCreate(BaseModel):
    """Create comment."""
    resource_type: str
    resource_id: str
    content: str = Field(..., min_length=1, max_length=5000)
    parent_id: Optional[str] = None
    mentions: List[str] = []
    attachments: List[str] = []


class CommentUpdate(BaseModel):
    """Update comment."""
    content: Optional[str] = Field(None, min_length=1, max_length=5000)


class ReactionCreate(BaseModel):
    """Add reaction."""
    reaction_type: str  # thumbs_up, thumbs_down, heart, fire, check, question


# ============================================================================
# MOCK DATA
# ============================================================================

RESOURCE_TYPES = ["dataspace", "document", "task", "meeting", "file", "thread"]
REACTION_TYPES = ["thumbs_up", "thumbs_down", "heart", "fire", "check", "question"]

MOCK_COMMENTS = [
    {
        "id": "comment_001",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "resource_type": "document",
        "resource_id": "doc_001",
        "parent_id": None,
        "content": "Le devis a été approuvé par le client. On peut passer à la commande des matériaux.",
        "mentions": [],
        "attachments": [],
        "reactions": {
            "thumbs_up": ["user_002"],
            "check": ["user_001"],
        },
        "replies_count": 2,
        "is_resolved": False,
        "is_edited": False,
        "created_at": "2026-01-05T14:30:00Z",
        "updated_at": "2026-01-05T14:30:00Z",
    },
    {
        "id": "comment_002",
        "user_id": "user_002",
        "identity_id": "identity_001",
        "resource_type": "document",
        "resource_id": "doc_001",
        "parent_id": "comment_001",
        "content": "Super! J'ai noté la liste des matériaux à commander.",
        "mentions": [],
        "attachments": [],
        "reactions": {},
        "replies_count": 0,
        "is_resolved": False,
        "is_edited": False,
        "created_at": "2026-01-05T15:00:00Z",
        "updated_at": "2026-01-05T15:00:00Z",
    },
    {
        "id": "comment_003",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "resource_type": "document",
        "resource_id": "doc_001",
        "parent_id": "comment_001",
        "content": "N'oublie pas de vérifier les délais de livraison pour les armoires.",
        "mentions": ["user_002"],
        "attachments": [],
        "reactions": {
            "check": ["user_002"],
        },
        "replies_count": 0,
        "is_resolved": False,
        "is_edited": False,
        "created_at": "2026-01-05T15:30:00Z",
        "updated_at": "2026-01-05T15:30:00Z",
    },
    {
        "id": "comment_004",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "resource_type": "task",
        "resource_id": "task_001",
        "parent_id": None,
        "content": "Commander les armoires chez Cuisines Pro - voir catalogue page 45.",
        "mentions": [],
        "attachments": ["file_005"],
        "reactions": {},
        "replies_count": 0,
        "is_resolved": False,
        "is_edited": False,
        "created_at": "2026-01-06T09:00:00Z",
        "updated_at": "2026-01-06T09:00:00Z",
    },
]


# ============================================================================
# COMMENTS
# ============================================================================

@router.get("", response_model=dict)
async def list_comments(
    resource_type: str,
    resource_id: str,
    parent_id: Optional[str] = None,
    include_replies: bool = True,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
):
    """
    List comments for a resource.
    """
    comments = [
        c for c in MOCK_COMMENTS
        if c["resource_type"] == resource_type and c["resource_id"] == resource_id
    ]
    
    if parent_id is not None:
        comments = [c for c in comments if c["parent_id"] == parent_id]
    elif not include_replies:
        comments = [c for c in comments if c["parent_id"] is None]
    
    # Sort by created_at
    comments.sort(key=lambda x: x["created_at"])
    
    total = len(comments)
    
    return {
        "success": True,
        "data": {
            "comments": comments,
            "total": total,
            "page": page,
        },
    }


@router.get("/{comment_id}", response_model=dict)
async def get_comment(comment_id: str):
    """
    Get comment details.
    """
    comment = next((c for c in MOCK_COMMENTS if c["id"] == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return {
        "success": True,
        "data": comment,
    }


@router.get("/{comment_id}/replies", response_model=dict)
async def list_replies(comment_id: str):
    """
    List replies to a comment.
    """
    replies = [c for c in MOCK_COMMENTS if c["parent_id"] == comment_id]
    replies.sort(key=lambda x: x["created_at"])
    
    return {
        "success": True,
        "data": {
            "replies": replies,
            "total": len(replies),
        },
    }


@router.post("", response_model=dict)
async def create_comment(data: CommentCreate):
    """
    Create comment.
    """
    if data.resource_type not in RESOURCE_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid resource type. Must be one of: {RESOURCE_TYPES}")
    
    comment = {
        "id": f"comment_{len(MOCK_COMMENTS) + 1:03d}",
        "user_id": "user_001",
        "identity_id": "identity_001",
        "resource_type": data.resource_type,
        "resource_id": data.resource_id,
        "parent_id": data.parent_id,
        "content": data.content,
        "mentions": data.mentions,
        "attachments": data.attachments,
        "reactions": {},
        "replies_count": 0,
        "is_resolved": False,
        "is_edited": False,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    # Increment parent's reply count
    if data.parent_id:
        parent = next((c for c in MOCK_COMMENTS if c["id"] == data.parent_id), None)
        if parent:
            parent["replies_count"] += 1
    
    MOCK_COMMENTS.append(comment)
    
    return {
        "success": True,
        "data": comment,
        "message": "Commentaire ajouté",
    }


@router.patch("/{comment_id}", response_model=dict)
async def update_comment(comment_id: str, data: CommentUpdate):
    """
    Update comment.
    """
    comment = next((c for c in MOCK_COMMENTS if c["id"] == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment["user_id"] != "user_001":
        raise HTTPException(status_code=403, detail="Cannot edit other's comment")
    
    if data.content:
        comment["content"] = data.content
        comment["is_edited"] = True
    
    comment["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": comment,
    }


@router.delete("/{comment_id}", response_model=dict)
async def delete_comment(comment_id: str):
    """
    Delete comment.
    """
    comment = next((c for c in MOCK_COMMENTS if c["id"] == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment["user_id"] != "user_001":
        raise HTTPException(status_code=403, detail="Cannot delete other's comment")
    
    MOCK_COMMENTS.remove(comment)
    
    return {
        "success": True,
        "message": "Commentaire supprimé",
    }


@router.post("/{comment_id}/resolve", response_model=dict)
async def resolve_comment(comment_id: str):
    """
    Mark comment as resolved.
    """
    comment = next((c for c in MOCK_COMMENTS if c["id"] == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    comment["is_resolved"] = True
    comment["updated_at"] = datetime.utcnow().isoformat()
    
    return {
        "success": True,
        "data": comment,
        "message": "Commentaire résolu",
    }


# ============================================================================
# REACTIONS
# ============================================================================

@router.post("/{comment_id}/reactions", response_model=dict)
async def add_reaction(comment_id: str, data: ReactionCreate):
    """
    Add reaction to comment.
    """
    if data.reaction_type not in REACTION_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid reaction. Must be one of: {REACTION_TYPES}")
    
    comment = next((c for c in MOCK_COMMENTS if c["id"] == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if data.reaction_type not in comment["reactions"]:
        comment["reactions"][data.reaction_type] = []
    
    if "user_001" not in comment["reactions"][data.reaction_type]:
        comment["reactions"][data.reaction_type].append("user_001")
    
    return {
        "success": True,
        "data": comment,
    }


@router.delete("/{comment_id}/reactions/{reaction_type}", response_model=dict)
async def remove_reaction(comment_id: str, reaction_type: str):
    """
    Remove reaction from comment.
    """
    comment = next((c for c in MOCK_COMMENTS if c["id"] == comment_id), None)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if reaction_type in comment["reactions"] and "user_001" in comment["reactions"][reaction_type]:
        comment["reactions"][reaction_type].remove("user_001")
        if not comment["reactions"][reaction_type]:
            del comment["reactions"][reaction_type]
    
    return {
        "success": True,
        "data": comment,
    }
