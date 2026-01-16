"""
CHE·NU™ V68 - Team Collaboration API Routes
Complete REST API for Slack/Teams killer

Endpoints:
- Workspaces: CRUD, settings
- Channels: CRUD, join/leave, invite, archive
- Messages: CRUD, search, pin
- Threads: replies, participants
- Reactions: add/remove
- DMs: create, list
- Members: CRUD, status
- Notifications: list, mark read
- Polls: create, vote, results
- AI: analysis, summaries, smart replies
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

from ..agents.collaboration_agent import (
    TeamCollaborationService,
    ChannelType,
    MessageType,
    MemberRole,
    UserStatus,
    NotificationType
)

router = APIRouter(prefix="/api/v2/collaboration", tags=["Team Collaboration"])

# Initialize service
service = TeamCollaborationService()


# ============================================================
# REQUEST/RESPONSE MODELS
# ============================================================

class CreateWorkspaceRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = ""
    owner_id: str


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: str
    icon_url: Optional[str]
    owner_id: str
    created_at: datetime


class CreateChannelRequest(BaseModel):
    workspace_id: str
    name: str = Field(..., min_length=1, max_length=80)
    description: str = ""
    channel_type: str = "public"
    created_by: str


class ChannelResponse(BaseModel):
    id: str
    workspace_id: str
    name: str
    description: str
    channel_type: str
    topic: str
    icon_emoji: str
    is_default: bool
    member_count: int
    created_at: datetime


class SendMessageRequest(BaseModel):
    workspace_id: str
    sender_id: str
    content: str = Field(..., min_length=1)
    channel_id: Optional[str] = None
    conversation_id: Optional[str] = None
    thread_id: Optional[str] = None
    message_type: str = "text"
    attachments: List[Dict[str, Any]] = []


class MessageResponse(BaseModel):
    id: str
    workspace_id: str
    channel_id: Optional[str]
    conversation_id: Optional[str]
    thread_id: Optional[str]
    sender_id: str
    message_type: str
    content: str
    mentions: List[str]
    reactions: Dict[str, List[str]]
    is_edited: bool
    is_pinned: bool
    reply_count: int
    created_at: datetime


class EditMessageRequest(BaseModel):
    content: str = Field(..., min_length=1)
    edited_by: str


class CreateDMRequest(BaseModel):
    workspace_id: str
    participant_ids: List[str] = Field(..., min_items=2)


class DMResponse(BaseModel):
    id: str
    workspace_id: str
    participant_ids: List[str]
    conversation_type: str
    name: Optional[str]
    created_at: datetime
    last_message_at: Optional[datetime]


class AddMemberRequest(BaseModel):
    workspace_id: str
    user_id: str
    added_by: str
    display_name: str = ""
    role: str = "member"


class MemberResponse(BaseModel):
    id: str
    workspace_id: str
    user_id: str
    display_name: str
    avatar_url: Optional[str]
    role: str
    status: str
    status_text: str
    status_emoji: str
    joined_at: datetime


class UpdateStatusRequest(BaseModel):
    status: str
    status_text: str = ""
    status_emoji: str = ""


class ReactionRequest(BaseModel):
    user_id: str
    emoji: str


class CreatePollRequest(BaseModel):
    message_id: str
    question: str
    options: List[str] = Field(..., min_items=2, max_items=10)
    is_anonymous: bool = False
    is_multiple_choice: bool = False
    ends_at: Optional[datetime] = None


class VotePollRequest(BaseModel):
    user_id: str
    option: str


class InviteRequest(BaseModel):
    user_id: str
    invited_by: str


class SetTopicRequest(BaseModel):
    topic: str
    set_by: str


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    workspace_id: str
    channel_id: Optional[str]
    message_id: Optional[str]
    notification_type: str
    title: str
    body: str
    is_read: bool
    created_at: datetime


# ============================================================
# WORKSPACE ENDPOINTS
# ============================================================

@router.post("/workspaces", response_model=WorkspaceResponse)
async def create_workspace(request: CreateWorkspaceRequest):
    """Create a new workspace"""
    workspace = service.create_workspace(
        name=request.name,
        owner_id=request.owner_id,
        description=request.description
    )
    return WorkspaceResponse(
        id=workspace.id,
        name=workspace.name,
        description=workspace.description,
        icon_url=workspace.icon_url,
        owner_id=workspace.owner_id,
        created_at=workspace.created_at
    )


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(workspace_id: str):
    """Get workspace by ID"""
    workspace = service.get_workspace(workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    return WorkspaceResponse(
        id=workspace.id,
        name=workspace.name,
        description=workspace.description,
        icon_url=workspace.icon_url,
        owner_id=workspace.owner_id,
        created_at=workspace.created_at
    )


@router.get("/workspaces", response_model=List[WorkspaceResponse])
async def list_workspaces(user_id: str = Query(...)):
    """List workspaces for user"""
    workspaces = service.list_workspaces(user_id)
    return [
        WorkspaceResponse(
            id=ws.id,
            name=ws.name,
            description=ws.description,
            icon_url=ws.icon_url,
            owner_id=ws.owner_id,
            created_at=ws.created_at
        )
        for ws in workspaces
    ]


# ============================================================
# CHANNEL ENDPOINTS
# ============================================================

@router.post("/channels", response_model=ChannelResponse)
async def create_channel(request: CreateChannelRequest):
    """Create a new channel"""
    channel_type = ChannelType(request.channel_type)
    
    channel = service.create_channel(
        workspace_id=request.workspace_id,
        name=request.name,
        created_by=request.created_by,
        description=request.description,
        channel_type=channel_type
    )
    
    return ChannelResponse(
        id=channel.id,
        workspace_id=channel.workspace_id,
        name=channel.name,
        description=channel.description,
        channel_type=channel.channel_type.value,
        topic=channel.topic,
        icon_emoji=channel.icon_emoji,
        is_default=channel.is_default,
        member_count=len(channel.member_ids),
        created_at=channel.created_at
    )


@router.get("/channels/{channel_id}", response_model=ChannelResponse)
async def get_channel(channel_id: str):
    """Get channel by ID"""
    channel = service.get_channel(channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    return ChannelResponse(
        id=channel.id,
        workspace_id=channel.workspace_id,
        name=channel.name,
        description=channel.description,
        channel_type=channel.channel_type.value,
        topic=channel.topic,
        icon_emoji=channel.icon_emoji,
        is_default=channel.is_default,
        member_count=len(channel.member_ids),
        created_at=channel.created_at
    )


@router.get("/channels", response_model=List[ChannelResponse])
async def list_channels(
    workspace_id: str = Query(...),
    user_id: str = Query(...)
):
    """List channels in workspace"""
    channels = service.list_channels(workspace_id, user_id)
    return [
        ChannelResponse(
            id=ch.id,
            workspace_id=ch.workspace_id,
            name=ch.name,
            description=ch.description,
            channel_type=ch.channel_type.value,
            topic=ch.topic,
            icon_emoji=ch.icon_emoji,
            is_default=ch.is_default,
            member_count=len(ch.member_ids),
            created_at=ch.created_at
        )
        for ch in channels
    ]


@router.post("/channels/{channel_id}/join")
async def join_channel(channel_id: str, user_id: str = Query(...)):
    """Join a channel"""
    success = service.join_channel(channel_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot join channel")
    return {"status": "joined", "channel_id": channel_id}


@router.post("/channels/{channel_id}/leave")
async def leave_channel(channel_id: str, user_id: str = Query(...)):
    """Leave a channel"""
    success = service.leave_channel(channel_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot leave channel")
    return {"status": "left", "channel_id": channel_id}


@router.post("/channels/{channel_id}/invite")
async def invite_to_channel(channel_id: str, request: InviteRequest):
    """Invite user to channel"""
    success = service.invite_to_channel(channel_id, request.user_id, request.invited_by)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot invite to channel")
    return {"status": "invited", "channel_id": channel_id, "user_id": request.user_id}


@router.post("/channels/{channel_id}/archive")
async def archive_channel(channel_id: str, archived_by: str = Query(...)):
    """Archive a channel"""
    success = service.archive_channel(channel_id, archived_by)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot archive channel")
    return {"status": "archived", "channel_id": channel_id}


@router.put("/channels/{channel_id}/topic")
async def set_channel_topic(channel_id: str, request: SetTopicRequest):
    """Set channel topic"""
    success = service.set_channel_topic(channel_id, request.topic, request.set_by)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot set topic")
    return {"status": "updated", "topic": request.topic}


@router.get("/channels/{channel_id}/members")
async def get_channel_members(channel_id: str):
    """Get channel members"""
    channel = service.get_channel(channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    return {"channel_id": channel_id, "member_ids": channel.member_ids}


# ============================================================
# MESSAGE ENDPOINTS
# ============================================================

@router.post("/messages", response_model=MessageResponse)
async def send_message(request: SendMessageRequest):
    """Send a message"""
    if not request.channel_id and not request.conversation_id:
        raise HTTPException(status_code=400, detail="Must specify channel_id or conversation_id")
    
    message = service.send_message(
        workspace_id=request.workspace_id,
        sender_id=request.sender_id,
        content=request.content,
        channel_id=request.channel_id,
        conversation_id=request.conversation_id,
        thread_id=request.thread_id,
        message_type=MessageType(request.message_type),
        attachments=request.attachments
    )
    
    return MessageResponse(
        id=message.id,
        workspace_id=message.workspace_id,
        channel_id=message.channel_id,
        conversation_id=message.conversation_id,
        thread_id=message.thread_id,
        sender_id=message.sender_id,
        message_type=message.message_type.value,
        content=message.content,
        mentions=message.mentions,
        reactions=message.reactions,
        is_edited=message.is_edited,
        is_pinned=message.is_pinned,
        reply_count=message.reply_count,
        created_at=message.created_at
    )


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: str):
    """Get message by ID"""
    message = service.get_message(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return MessageResponse(
        id=message.id,
        workspace_id=message.workspace_id,
        channel_id=message.channel_id,
        conversation_id=message.conversation_id,
        thread_id=message.thread_id,
        sender_id=message.sender_id,
        message_type=message.message_type.value,
        content=message.content,
        mentions=message.mentions,
        reactions=message.reactions,
        is_edited=message.is_edited,
        is_pinned=message.is_pinned,
        reply_count=message.reply_count,
        created_at=message.created_at
    )


@router.put("/messages/{message_id}", response_model=MessageResponse)
async def edit_message(message_id: str, request: EditMessageRequest):
    """Edit a message"""
    message = service.edit_message(message_id, request.content, request.edited_by)
    if not message:
        raise HTTPException(status_code=400, detail="Cannot edit message")
    
    return MessageResponse(
        id=message.id,
        workspace_id=message.workspace_id,
        channel_id=message.channel_id,
        conversation_id=message.conversation_id,
        thread_id=message.thread_id,
        sender_id=message.sender_id,
        message_type=message.message_type.value,
        content=message.content,
        mentions=message.mentions,
        reactions=message.reactions,
        is_edited=message.is_edited,
        is_pinned=message.is_pinned,
        reply_count=message.reply_count,
        created_at=message.created_at
    )


@router.delete("/messages/{message_id}")
async def delete_message(message_id: str, deleted_by: str = Query(...)):
    """Delete a message"""
    success = service.delete_message(message_id, deleted_by)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete message")
    return {"status": "deleted", "message_id": message_id}


@router.get("/messages", response_model=List[MessageResponse])
async def list_messages(
    channel_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    thread_id: Optional[str] = None,
    limit: int = Query(50, le=100)
):
    """List messages"""
    if not channel_id and not conversation_id and not thread_id:
        raise HTTPException(status_code=400, detail="Must specify channel_id, conversation_id, or thread_id")
    
    messages = service.list_messages(
        channel_id=channel_id,
        conversation_id=conversation_id,
        thread_id=thread_id,
        limit=limit
    )
    
    return [
        MessageResponse(
            id=msg.id,
            workspace_id=msg.workspace_id,
            channel_id=msg.channel_id,
            conversation_id=msg.conversation_id,
            thread_id=msg.thread_id,
            sender_id=msg.sender_id,
            message_type=msg.message_type.value,
            content=msg.content,
            mentions=msg.mentions,
            reactions=msg.reactions,
            is_edited=msg.is_edited,
            is_pinned=msg.is_pinned,
            reply_count=msg.reply_count,
            created_at=msg.created_at
        )
        for msg in messages
    ]


@router.get("/messages/search")
async def search_messages(
    workspace_id: str = Query(...),
    query: str = Query(..., min_length=1),
    user_id: str = Query(...),
    channel_id: Optional[str] = None,
    from_user_id: Optional[str] = None,
    limit: int = Query(20, le=50)
):
    """Search messages"""
    results = service.search_messages(
        workspace_id=workspace_id,
        query=query,
        user_id=user_id,
        channel_id=channel_id,
        from_user_id=from_user_id,
        limit=limit
    )
    
    return {
        "query": query,
        "count": len(results),
        "messages": [
            {
                "id": msg.id,
                "channel_id": msg.channel_id,
                "sender_id": msg.sender_id,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in results
        ]
    }


@router.post("/messages/{message_id}/pin")
async def pin_message(message_id: str, pinned_by: str = Query(...)):
    """Pin a message"""
    success = service.pin_message(message_id, pinned_by)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot pin message")
    return {"status": "pinned", "message_id": message_id}


@router.post("/messages/{message_id}/unpin")
async def unpin_message(message_id: str):
    """Unpin a message"""
    success = service.unpin_message(message_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot unpin message")
    return {"status": "unpinned", "message_id": message_id}


# ============================================================
# REACTION ENDPOINTS
# ============================================================

@router.post("/messages/{message_id}/reactions")
async def add_reaction(message_id: str, request: ReactionRequest):
    """Add reaction to message"""
    success = service.add_reaction(message_id, request.user_id, request.emoji)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot add reaction")
    return {"status": "added", "emoji": request.emoji}


@router.delete("/messages/{message_id}/reactions")
async def remove_reaction(
    message_id: str,
    user_id: str = Query(...),
    emoji: str = Query(...)
):
    """Remove reaction from message"""
    success = service.remove_reaction(message_id, user_id, emoji)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot remove reaction")
    return {"status": "removed", "emoji": emoji}


# ============================================================
# THREAD ENDPOINTS
# ============================================================

@router.get("/threads/{parent_message_id}")
async def get_thread(parent_message_id: str):
    """Get thread info"""
    thread = service.get_thread(parent_message_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    return {
        "id": thread.id,
        "parent_message_id": thread.parent_message_id,
        "channel_id": thread.channel_id,
        "participant_ids": thread.participant_ids,
        "reply_count": thread.reply_count,
        "last_reply_at": thread.last_reply_at.isoformat() if thread.last_reply_at else None,
        "created_at": thread.created_at.isoformat()
    }


@router.get("/threads/{parent_message_id}/replies", response_model=List[MessageResponse])
async def get_thread_replies(
    parent_message_id: str,
    limit: int = Query(50, le=100)
):
    """Get thread replies"""
    replies = service.get_thread_replies(parent_message_id, limit)
    
    return [
        MessageResponse(
            id=msg.id,
            workspace_id=msg.workspace_id,
            channel_id=msg.channel_id,
            conversation_id=msg.conversation_id,
            thread_id=msg.thread_id,
            sender_id=msg.sender_id,
            message_type=msg.message_type.value,
            content=msg.content,
            mentions=msg.mentions,
            reactions=msg.reactions,
            is_edited=msg.is_edited,
            is_pinned=msg.is_pinned,
            reply_count=msg.reply_count,
            created_at=msg.created_at
        )
        for msg in replies
    ]


# ============================================================
# DM ENDPOINTS
# ============================================================

@router.post("/dms", response_model=DMResponse)
async def create_dm(request: CreateDMRequest):
    """Create or get DM conversation"""
    dm = service.create_dm(request.workspace_id, request.participant_ids)
    
    return DMResponse(
        id=dm.id,
        workspace_id=dm.workspace_id,
        participant_ids=dm.participant_ids,
        conversation_type=dm.conversation_type.value,
        name=dm.name,
        created_at=dm.created_at,
        last_message_at=dm.last_message_at
    )


@router.get("/dms/{conversation_id}", response_model=DMResponse)
async def get_dm(conversation_id: str):
    """Get DM conversation"""
    dm = service.get_conversation(conversation_id)
    if not dm:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return DMResponse(
        id=dm.id,
        workspace_id=dm.workspace_id,
        participant_ids=dm.participant_ids,
        conversation_type=dm.conversation_type.value,
        name=dm.name,
        created_at=dm.created_at,
        last_message_at=dm.last_message_at
    )


@router.get("/dms", response_model=List[DMResponse])
async def list_dms(
    workspace_id: str = Query(...),
    user_id: str = Query(...)
):
    """List user's DM conversations"""
    dms = service.list_conversations(workspace_id, user_id)
    
    return [
        DMResponse(
            id=dm.id,
            workspace_id=dm.workspace_id,
            participant_ids=dm.participant_ids,
            conversation_type=dm.conversation_type.value,
            name=dm.name,
            created_at=dm.created_at,
            last_message_at=dm.last_message_at
        )
        for dm in dms
    ]


# ============================================================
# MEMBER ENDPOINTS
# ============================================================

@router.post("/members", response_model=MemberResponse)
async def add_member(request: AddMemberRequest):
    """Add member to workspace"""
    member = service.add_member(
        workspace_id=request.workspace_id,
        user_id=request.user_id,
        added_by=request.added_by,
        display_name=request.display_name,
        role=MemberRole(request.role)
    )
    
    return MemberResponse(
        id=member.id,
        workspace_id=member.workspace_id,
        user_id=member.user_id,
        display_name=member.display_name,
        avatar_url=member.avatar_url,
        role=member.role.value,
        status=member.status.value,
        status_text=member.status_text,
        status_emoji=member.status_emoji,
        joined_at=member.joined_at
    )


@router.get("/members/{workspace_id}/{user_id}", response_model=MemberResponse)
async def get_member(workspace_id: str, user_id: str):
    """Get workspace member"""
    member = service.get_member(workspace_id, user_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return MemberResponse(
        id=member.id,
        workspace_id=member.workspace_id,
        user_id=member.user_id,
        display_name=member.display_name,
        avatar_url=member.avatar_url,
        role=member.role.value,
        status=member.status.value,
        status_text=member.status_text,
        status_emoji=member.status_emoji,
        joined_at=member.joined_at
    )


@router.get("/members", response_model=List[MemberResponse])
async def list_members(workspace_id: str = Query(...)):
    """List workspace members"""
    members = service.list_members(workspace_id)
    
    return [
        MemberResponse(
            id=m.id,
            workspace_id=m.workspace_id,
            user_id=m.user_id,
            display_name=m.display_name,
            avatar_url=m.avatar_url,
            role=m.role.value,
            status=m.status.value,
            status_text=m.status_text,
            status_emoji=m.status_emoji,
            joined_at=m.joined_at
        )
        for m in members
    ]


@router.put("/members/{workspace_id}/{user_id}/status")
async def update_member_status(
    workspace_id: str,
    user_id: str,
    request: UpdateStatusRequest
):
    """Update member status"""
    member = service.update_member_status(
        workspace_id=workspace_id,
        user_id=user_id,
        status=UserStatus(request.status),
        status_text=request.status_text,
        status_emoji=request.status_emoji
    )
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    return {
        "status": "updated",
        "user_status": member.status.value,
        "status_text": member.status_text
    }


@router.delete("/members/{workspace_id}/{user_id}")
async def remove_member(
    workspace_id: str,
    user_id: str,
    removed_by: str = Query(...)
):
    """Remove member from workspace"""
    success = service.remove_member(workspace_id, user_id, removed_by)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot remove member")
    return {"status": "removed", "user_id": user_id}


# ============================================================
# NOTIFICATION ENDPOINTS
# ============================================================

@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    user_id: str = Query(...),
    unread_only: bool = Query(False)
):
    """Get user notifications"""
    notifications = service.get_notifications(user_id, unread_only)
    
    return [
        NotificationResponse(
            id=n.id,
            user_id=n.user_id,
            workspace_id=n.workspace_id,
            channel_id=n.channel_id,
            message_id=n.message_id,
            notification_type=n.notification_type,
            title=n.title,
            body=n.body,
            is_read=n.is_read,
            created_at=n.created_at
        )
        for n in notifications
    ]


@router.post("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: str, user_id: str = Query(...)):
    """Mark notification as read"""
    success = service.mark_notification_read(notification_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot mark notification")
    return {"status": "read", "notification_id": notification_id}


@router.post("/notifications/read-all")
async def mark_all_notifications_read(user_id: str = Query(...)):
    """Mark all notifications as read"""
    count = service.mark_all_notifications_read(user_id)
    return {"status": "read", "count": count}


# ============================================================
# POLL ENDPOINTS
# ============================================================

@router.post("/polls")
async def create_poll(request: CreatePollRequest):
    """Create a poll"""
    poll = service.create_poll(
        message_id=request.message_id,
        question=request.question,
        options=request.options,
        is_anonymous=request.is_anonymous,
        is_multiple_choice=request.is_multiple_choice,
        ends_at=request.ends_at
    )
    
    return {
        "id": poll.id,
        "message_id": poll.message_id,
        "question": poll.question,
        "options": poll.options,
        "is_anonymous": poll.is_anonymous,
        "is_multiple_choice": poll.is_multiple_choice,
        "ends_at": poll.ends_at.isoformat() if poll.ends_at else None
    }


@router.post("/polls/{poll_id}/vote")
async def vote_poll(poll_id: str, request: VotePollRequest):
    """Vote in poll"""
    success = service.vote_poll(poll_id, request.user_id, request.option)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot vote")
    return {"status": "voted", "option": request.option}


@router.get("/polls/{poll_id}/results")
async def get_poll_results(poll_id: str):
    """Get poll results"""
    results = service.get_poll_results(poll_id)
    if not results:
        raise HTTPException(status_code=404, detail="Poll not found")
    return results


# ============================================================
# AI ENDPOINTS
# ============================================================

@router.get("/ai/analyze/{message_id}")
async def analyze_message(message_id: str):
    """AI analysis of a message"""
    analysis = service.analyze_message(message_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return {
        "message_id": analysis.message_id,
        "priority": analysis.priority.value,
        "sentiment": analysis.sentiment.value,
        "topics": analysis.topics,
        "action_items": analysis.action_items,
        "questions": analysis.questions,
        "key_points": analysis.key_points,
        "requires_response": analysis.requires_response,
        "confidence": analysis.confidence
    }


@router.get("/ai/channel-summary/{channel_id}")
async def get_channel_summary(
    channel_id: str,
    period_hours: int = Query(24, ge=1, le=168)
):
    """AI summary of channel activity"""
    summary = service.get_channel_summary(channel_id, period_hours)
    if not summary:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    return {
        "channel_id": summary.channel_id,
        "period_start": summary.period_start.isoformat(),
        "period_end": summary.period_end.isoformat(),
        "message_count": summary.message_count,
        "participant_count": summary.participant_count,
        "key_topics": summary.key_topics,
        "decisions_made": summary.decisions_made,
        "action_items": summary.action_items,
        "unresolved_questions": summary.unresolved_questions,
        "sentiment_breakdown": summary.sentiment_breakdown,
        "most_active_members": summary.most_active_members,
        "summary_text": summary.summary_text,
        "generated_at": summary.generated_at.isoformat()
    }


@router.get("/ai/smart-replies/{message_id}")
async def get_smart_replies(message_id: str):
    """Get AI-suggested replies"""
    replies = service.get_smart_replies(message_id)
    
    return {
        "message_id": message_id,
        "suggestions": [
            {
                "suggestion": r.suggestion,
                "tone": r.tone,
                "confidence": r.confidence
            }
            for r in replies
        ]
    }


@router.get("/ai/important-messages/{channel_id}")
async def get_important_messages(
    channel_id: str,
    limit: int = Query(10, le=20)
):
    """Get important messages needing attention"""
    messages = service.get_important_messages(channel_id, limit)
    
    return {
        "channel_id": channel_id,
        "count": len(messages),
        "messages": [
            {
                "id": msg.id,
                "sender_id": msg.sender_id,
                "content": msg.content[:200],
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }


# ============================================================
# DASHBOARD ENDPOINT
# ============================================================

@router.get("/dashboard/{workspace_id}")
async def get_dashboard(workspace_id: str, user_id: str = Query(...)):
    """Get collaboration dashboard data"""
    dashboard = service.get_dashboard(workspace_id, user_id)
    return dashboard


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "team-collaboration",
        "version": "V68",
        "workspaces_count": len(service.workspaces),
        "channels_count": len(service.channels),
        "messages_count": len(service.messages)
    }
