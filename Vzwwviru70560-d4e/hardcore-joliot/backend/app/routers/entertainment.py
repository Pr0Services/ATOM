"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ V77 — Entertainment Sphere Router
═══════════════════════════════════════════════════════════════════════════════

Version: 77.0
Sphere: Entertainment
Endpoints: 18
Status: PRODUCTION READY

R&D Rules Enforced:
- Rule #1: HTTP 423 on stream deletion, content moderation
- Rule #5: CHRONOLOGICAL ONLY - NO ranking algorithms, NO recommendations
- Rule #6: Full traceability (id, created_by, created_at)
- Rule #7: Frozen architecture (6 bureau sections)

⚠️ CRITICAL: This sphere does NOT use algorithmic recommendations.
   All content is displayed in chronological order (created_at DESC).
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

router = APIRouter()


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS & CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

class StreamStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    LIVE = "live"
    ENDED = "ended"
    ARCHIVED = "archived"


class ContentType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    PODCAST = "podcast"
    LIVESTREAM = "livestream"
    PLAYLIST = "playlist"


class MediaCategory(str, Enum):
    MUSIC = "music"
    FILM = "film"
    DOCUMENTARY = "documentary"
    EDUCATION = "education"
    GAMING = "gaming"
    SPORTS = "sports"
    NEWS = "news"
    OTHER = "other"


# R&D Rule #5: NO ranking - order by created_at only
SORT_ORDER = "created_at DESC"


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class StreamBase(BaseModel):
    """Base stream schema."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=5000)
    content_type: ContentType = ContentType.VIDEO
    category: MediaCategory = MediaCategory.OTHER
    duration_seconds: Optional[int] = Field(None, ge=0)
    thumbnail_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class StreamCreate(StreamBase):
    """Create stream request - always starts as draft."""
    scheduled_at: Optional[datetime] = None


class StreamResponse(StreamBase):
    """Stream response with traceability."""
    id: UUID
    status: StreamStatus
    view_count: int = 0
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PlaylistBase(BaseModel):
    """Playlist base schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    is_public: bool = False
    category: MediaCategory = MediaCategory.OTHER


class PlaylistCreate(PlaylistBase):
    """Create playlist request."""
    media_ids: List[UUID] = Field(default_factory=list)


class PlaylistResponse(PlaylistBase):
    """Playlist response with traceability."""
    id: UUID
    media_count: int = 0
    total_duration_seconds: int = 0
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MediaItem(BaseModel):
    """Media library item."""
    id: UUID
    title: str
    content_type: ContentType
    category: MediaCategory
    duration_seconds: Optional[int] = None
    thumbnail_url: Optional[str] = None
    file_url: Optional[str] = None
    file_size_bytes: Optional[int] = None
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID


class WatchHistoryEntry(BaseModel):
    """Watch history entry."""
    id: UUID
    media_id: UUID
    media_title: str
    content_type: ContentType
    watched_at: datetime
    progress_seconds: int = 0
    completed: bool = False
    
    # R&D Rule #6: Traceability
    created_at: datetime
    created_by: UUID


class CheckpointPending(BaseModel):
    """Response when checkpoint required."""
    status: str = "checkpoint_required"
    checkpoint_id: UUID
    action: str
    resource_id: UUID
    message: str
    requires_approval: bool = True
    created_at: datetime


# ═══════════════════════════════════════════════════════════════════════════════
# MOCK DATA STORE (In production: PostgreSQL)
# ═══════════════════════════════════════════════════════════════════════════════

_streams_db: Dict[UUID, dict] = {}
_playlists_db: Dict[UUID, dict] = {}
_media_library_db: Dict[UUID, dict] = {}
_watch_history_db: Dict[UUID, list] = {}
_checkpoints_db: Dict[UUID, dict] = {}

# Mock user for development
MOCK_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_current_user_id() -> UUID:
    """Get current user ID. In production: from JWT token."""
    return MOCK_USER_ID


def create_checkpoint(action: str, resource_id: UUID, user_id: UUID) -> UUID:
    """Create governance checkpoint for sensitive actions."""
    checkpoint_id = uuid4()
    _checkpoints_db[checkpoint_id] = {
        "id": checkpoint_id,
        "action": action,
        "resource_id": resource_id,
        "user_id": user_id,
        "status": "pending",
        "created_at": datetime.utcnow(),
    }
    return checkpoint_id


# ═══════════════════════════════════════════════════════════════════════════════
# STREAM ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health", tags=["Health"])
async def entertainment_health():
    """Health check for entertainment sphere."""
    return {
        "status": "healthy",
        "sphere": "entertainment",
        "version": "77.0",
        "rd_rules": {
            "rule_5": "CHRONOLOGICAL_ONLY - No ranking algorithms",
            "rule_6": "Full traceability enabled"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/streams", response_model=List[StreamResponse], tags=["Streams"])
async def list_streams(
    status: Optional[StreamStatus] = None,
    category: Optional[MediaCategory] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    List user's streams.
    
    ⚠️ R&D Rule #5: Results are ALWAYS in chronological order (created_at DESC).
    NO ranking algorithms, NO recommendations, NO engagement-based sorting.
    """
    user_id = get_current_user_id()
    
    # Filter streams for user
    streams = [
        s for s in _streams_db.values()
        if s["created_by"] == user_id
    ]
    
    # Apply filters
    if status:
        streams = [s for s in streams if s["status"] == status]
    if category:
        streams = [s for s in streams if s["category"] == category]
    
    # R&D Rule #5: CHRONOLOGICAL ORDER ONLY
    streams.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Pagination
    streams = streams[offset:offset + limit]
    
    return [StreamResponse(**s) for s in streams]


@router.post("/streams/create", response_model=StreamResponse, status_code=201, tags=["Streams"])
async def create_stream(stream: StreamCreate):
    """
    Create a new stream.
    
    Streams always start in DRAFT status and require explicit publishing.
    This ensures human review before content goes live.
    """
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    stream_id = uuid4()
    stream_data = {
        "id": stream_id,
        **stream.model_dump(),
        "status": StreamStatus.DRAFT,
        "view_count": 0,
        "started_at": None,
        "ended_at": None,
        "created_at": now,
        "created_by": user_id,
        "updated_at": now,
    }
    
    _streams_db[stream_id] = stream_data
    
    return StreamResponse(**stream_data)


@router.get("/streams/{stream_id}", response_model=StreamResponse, tags=["Streams"])
async def get_stream(stream_id: UUID = Path(...)):
    """Get stream details by ID."""
    user_id = get_current_user_id()
    
    if stream_id not in _streams_db:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    stream = _streams_db[stream_id]
    
    # Check ownership
    if stream["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return StreamResponse(**stream)


@router.put("/streams/{stream_id}", response_model=StreamResponse, tags=["Streams"])
async def update_stream(
    stream_id: UUID = Path(...),
    update: StreamCreate = Body(...),
):
    """Update stream details. Only allowed in DRAFT status."""
    user_id = get_current_user_id()
    
    if stream_id not in _streams_db:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    stream = _streams_db[stream_id]
    
    if stream["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if stream["status"] != StreamStatus.DRAFT:
        raise HTTPException(
            status_code=400, 
            detail="Cannot update stream after it has been scheduled or published"
        )
    
    # Update fields
    stream.update(update.model_dump())
    stream["updated_at"] = datetime.utcnow()
    
    _streams_db[stream_id] = stream
    
    return StreamResponse(**stream)


@router.post("/streams/{stream_id}/schedule", response_model=StreamResponse, tags=["Streams"])
async def schedule_stream(
    stream_id: UUID = Path(...),
    scheduled_at: datetime = Body(..., embed=True),
):
    """Schedule a draft stream for future broadcast."""
    user_id = get_current_user_id()
    
    if stream_id not in _streams_db:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    stream = _streams_db[stream_id]
    
    if stream["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if stream["status"] != StreamStatus.DRAFT:
        raise HTTPException(status_code=400, detail="Only draft streams can be scheduled")
    
    if scheduled_at <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Schedule time must be in the future")
    
    stream["status"] = StreamStatus.SCHEDULED
    stream["scheduled_at"] = scheduled_at
    stream["updated_at"] = datetime.utcnow()
    
    _streams_db[stream_id] = stream
    
    return StreamResponse(**stream)


@router.post("/streams/{stream_id}/go-live", response_model=StreamResponse, tags=["Streams"])
async def go_live(stream_id: UUID = Path(...)):
    """Start a live stream. Only for scheduled or draft streams."""
    user_id = get_current_user_id()
    
    if stream_id not in _streams_db:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    stream = _streams_db[stream_id]
    
    if stream["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if stream["status"] not in [StreamStatus.DRAFT, StreamStatus.SCHEDULED]:
        raise HTTPException(status_code=400, detail="Stream cannot go live from current status")
    
    now = datetime.utcnow()
    stream["status"] = StreamStatus.LIVE
    stream["started_at"] = now
    stream["updated_at"] = now
    
    _streams_db[stream_id] = stream
    
    return StreamResponse(**stream)


@router.post("/streams/{stream_id}/end", response_model=StreamResponse, tags=["Streams"])
async def end_stream(stream_id: UUID = Path(...)):
    """End a live stream."""
    user_id = get_current_user_id()
    
    if stream_id not in _streams_db:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    stream = _streams_db[stream_id]
    
    if stream["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if stream["status"] != StreamStatus.LIVE:
        raise HTTPException(status_code=400, detail="Only live streams can be ended")
    
    now = datetime.utcnow()
    stream["status"] = StreamStatus.ENDED
    stream["ended_at"] = now
    stream["updated_at"] = now
    
    # Calculate duration
    if stream["started_at"]:
        stream["duration_seconds"] = int((now - stream["started_at"]).total_seconds())
    
    _streams_db[stream_id] = stream
    
    return StreamResponse(**stream)


@router.delete("/streams/{stream_id}", tags=["Streams"])
async def delete_stream(stream_id: UUID = Path(...)):
    """
    Delete a stream.
    
    ⚠️ R&D Rule #1: Requires human approval checkpoint.
    Returns HTTP 423 LOCKED until approved.
    """
    user_id = get_current_user_id()
    
    if stream_id not in _streams_db:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    stream = _streams_db[stream_id]
    
    if stream["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # R&D Rule #1: Create checkpoint for deletion
    checkpoint_id = create_checkpoint("DELETE_STREAM", stream_id, user_id)
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint_id": str(checkpoint_id),
            "action": "DELETE_STREAM",
            "resource_id": str(stream_id),
            "message": "Stream deletion requires human approval",
            "rule": "R&D Rule #1: Human Sovereignty"
        }
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MEDIA LIBRARY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/media-library", response_model=List[MediaItem], tags=["Media Library"])
async def list_media(
    content_type: Optional[ContentType] = None,
    category: Optional[MediaCategory] = None,
    search: Optional[str] = Query(None, min_length=1, max_length=200),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    List media library items.
    
    ⚠️ R&D Rule #5: CHRONOLOGICAL ORDER ONLY.
    No popularity ranking, no recommendation algorithms.
    """
    user_id = get_current_user_id()
    
    # Filter media for user
    media = [
        m for m in _media_library_db.values()
        if m["created_by"] == user_id
    ]
    
    # Apply filters
    if content_type:
        media = [m for m in media if m["content_type"] == content_type]
    if category:
        media = [m for m in media if m["category"] == category]
    if search:
        search_lower = search.lower()
        media = [m for m in media if search_lower in m["title"].lower()]
    
    # R&D Rule #5: CHRONOLOGICAL ORDER ONLY
    media.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Pagination
    media = media[offset:offset + limit]
    
    return [MediaItem(**m) for m in media]


@router.post("/media-library/upload", response_model=MediaItem, status_code=201, tags=["Media Library"])
async def upload_media(
    title: str = Body(..., min_length=1, max_length=500),
    content_type: ContentType = Body(...),
    category: MediaCategory = Body(default=MediaCategory.OTHER),
    file_url: Optional[str] = Body(None),
    thumbnail_url: Optional[str] = Body(None),
    duration_seconds: Optional[int] = Body(None),
    file_size_bytes: Optional[int] = Body(None),
):
    """Upload media to library."""
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    media_id = uuid4()
    media_data = {
        "id": media_id,
        "title": title,
        "content_type": content_type,
        "category": category,
        "file_url": file_url,
        "thumbnail_url": thumbnail_url,
        "duration_seconds": duration_seconds,
        "file_size_bytes": file_size_bytes,
        "created_at": now,
        "created_by": user_id,
    }
    
    _media_library_db[media_id] = media_data
    
    return MediaItem(**media_data)


@router.get("/media-library/{media_id}", response_model=MediaItem, tags=["Media Library"])
async def get_media(media_id: UUID = Path(...)):
    """Get media item details."""
    user_id = get_current_user_id()
    
    if media_id not in _media_library_db:
        raise HTTPException(status_code=404, detail="Media not found")
    
    media = _media_library_db[media_id]
    
    if media["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return MediaItem(**media)


@router.delete("/media-library/{media_id}", tags=["Media Library"])
async def delete_media(media_id: UUID = Path(...)):
    """
    Delete media from library.
    
    ⚠️ R&D Rule #1: Requires checkpoint approval.
    """
    user_id = get_current_user_id()
    
    if media_id not in _media_library_db:
        raise HTTPException(status_code=404, detail="Media not found")
    
    media = _media_library_db[media_id]
    
    if media["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    checkpoint_id = create_checkpoint("DELETE_MEDIA", media_id, user_id)
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint_id": str(checkpoint_id),
            "action": "DELETE_MEDIA",
            "resource_id": str(media_id),
            "message": "Media deletion requires human approval",
            "rule": "R&D Rule #1: Human Sovereignty"
        }
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PLAYLIST ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/playlists", response_model=List[PlaylistResponse], tags=["Playlists"])
async def list_playlists(
    is_public: Optional[bool] = None,
    category: Optional[MediaCategory] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    """
    List user's playlists.
    
    ⚠️ R&D Rule #5: CHRONOLOGICAL ORDER ONLY.
    """
    user_id = get_current_user_id()
    
    playlists = [
        p for p in _playlists_db.values()
        if p["created_by"] == user_id
    ]
    
    if is_public is not None:
        playlists = [p for p in playlists if p["is_public"] == is_public]
    if category:
        playlists = [p for p in playlists if p["category"] == category]
    
    # R&D Rule #5: CHRONOLOGICAL ORDER ONLY
    playlists.sort(key=lambda x: x["created_at"], reverse=True)
    
    playlists = playlists[offset:offset + limit]
    
    return [PlaylistResponse(**p) for p in playlists]


@router.post("/playlists", response_model=PlaylistResponse, status_code=201, tags=["Playlists"])
async def create_playlist(playlist: PlaylistCreate):
    """Create a new playlist."""
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    playlist_id = uuid4()
    playlist_data = {
        "id": playlist_id,
        **playlist.model_dump(exclude={"media_ids"}),
        "media_ids": [str(mid) for mid in playlist.media_ids],
        "media_count": len(playlist.media_ids),
        "total_duration_seconds": 0,  # Calculate from media
        "created_at": now,
        "created_by": user_id,
        "updated_at": now,
    }
    
    _playlists_db[playlist_id] = playlist_data
    
    return PlaylistResponse(**playlist_data)


@router.get("/playlists/{playlist_id}", response_model=PlaylistResponse, tags=["Playlists"])
async def get_playlist(playlist_id: UUID = Path(...)):
    """Get playlist details."""
    user_id = get_current_user_id()
    
    if playlist_id not in _playlists_db:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    playlist = _playlists_db[playlist_id]
    
    if playlist["created_by"] != user_id and not playlist["is_public"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return PlaylistResponse(**playlist)


@router.post("/playlists/{playlist_id}/add-media", response_model=PlaylistResponse, tags=["Playlists"])
async def add_media_to_playlist(
    playlist_id: UUID = Path(...),
    media_id: UUID = Body(..., embed=True),
):
    """Add media item to playlist."""
    user_id = get_current_user_id()
    
    if playlist_id not in _playlists_db:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    playlist = _playlists_db[playlist_id]
    
    if playlist["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if str(media_id) not in playlist.get("media_ids", []):
        playlist.setdefault("media_ids", []).append(str(media_id))
        playlist["media_count"] = len(playlist["media_ids"])
        playlist["updated_at"] = datetime.utcnow()
    
    _playlists_db[playlist_id] = playlist
    
    return PlaylistResponse(**playlist)


@router.delete("/playlists/{playlist_id}", tags=["Playlists"])
async def delete_playlist(playlist_id: UUID = Path(...)):
    """Delete a playlist. Requires checkpoint."""
    user_id = get_current_user_id()
    
    if playlist_id not in _playlists_db:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    playlist = _playlists_db[playlist_id]
    
    if playlist["created_by"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    checkpoint_id = create_checkpoint("DELETE_PLAYLIST", playlist_id, user_id)
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint_id": str(checkpoint_id),
            "action": "DELETE_PLAYLIST",
            "resource_id": str(playlist_id),
            "message": "Playlist deletion requires human approval"
        }
    )


# ═══════════════════════════════════════════════════════════════════════════════
# WATCH HISTORY ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/watch-history", response_model=List[WatchHistoryEntry], tags=["Watch History"])
async def get_watch_history(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """
    Get user's watch history.
    
    ⚠️ R&D Rule #5: CHRONOLOGICAL ORDER ONLY (most recent first).
    No "continue watching" recommendations based on engagement.
    """
    user_id = get_current_user_id()
    
    history = _watch_history_db.get(user_id, [])
    
    # R&D Rule #5: CHRONOLOGICAL ORDER ONLY
    history.sort(key=lambda x: x["watched_at"], reverse=True)
    
    history = history[offset:offset + limit]
    
    return [WatchHistoryEntry(**h) for h in history]


@router.post("/watch-history", response_model=WatchHistoryEntry, status_code=201, tags=["Watch History"])
async def add_watch_history(
    media_id: UUID = Body(...),
    media_title: str = Body(...),
    content_type: ContentType = Body(...),
    progress_seconds: int = Body(default=0),
    completed: bool = Body(default=False),
):
    """Record a watch history entry."""
    user_id = get_current_user_id()
    now = datetime.utcnow()
    
    entry_id = uuid4()
    entry_data = {
        "id": entry_id,
        "media_id": media_id,
        "media_title": media_title,
        "content_type": content_type,
        "watched_at": now,
        "progress_seconds": progress_seconds,
        "completed": completed,
        "created_at": now,
        "created_by": user_id,
    }
    
    if user_id not in _watch_history_db:
        _watch_history_db[user_id] = []
    
    _watch_history_db[user_id].append(entry_data)
    
    return WatchHistoryEntry(**entry_data)


@router.delete("/watch-history", tags=["Watch History"])
async def clear_watch_history():
    """
    Clear all watch history.
    
    ⚠️ R&D Rule #1: Requires checkpoint approval.
    """
    user_id = get_current_user_id()
    
    checkpoint_id = create_checkpoint("CLEAR_WATCH_HISTORY", user_id, user_id)
    
    raise HTTPException(
        status_code=423,
        detail={
            "status": "checkpoint_required",
            "checkpoint_id": str(checkpoint_id),
            "action": "CLEAR_WATCH_HISTORY",
            "resource_id": str(user_id),
            "message": "Clearing watch history requires human approval"
        }
    )


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICS ENDPOINTS (READ-ONLY)
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/stats", tags=["Statistics"])
async def get_entertainment_stats():
    """
    Get entertainment statistics (read-only).
    
    No engagement metrics that could influence algorithmic recommendations.
    """
    user_id = get_current_user_id()
    
    user_streams = [s for s in _streams_db.values() if s["created_by"] == user_id]
    user_media = [m for m in _media_library_db.values() if m["created_by"] == user_id]
    user_playlists = [p for p in _playlists_db.values() if p["created_by"] == user_id]
    user_history = _watch_history_db.get(user_id, [])
    
    return {
        "user_id": str(user_id),
        "streams": {
            "total": len(user_streams),
            "by_status": {
                status.value: len([s for s in user_streams if s["status"] == status])
                for status in StreamStatus
            }
        },
        "media_library": {
            "total": len(user_media),
            "by_type": {
                ct.value: len([m for m in user_media if m["content_type"] == ct])
                for ct in ContentType
            }
        },
        "playlists": {
            "total": len(user_playlists),
            "public": len([p for p in user_playlists if p.get("is_public", False)])
        },
        "watch_history": {
            "total_entries": len(user_history),
            "completed": len([h for h in user_history if h.get("completed", False)])
        },
        "timestamp": datetime.utcnow().isoformat(),
        "rd_rule_5_notice": "Statistics are for informational purposes only. No ranking algorithms applied."
    }


@router.get("/stats/categories", tags=["Statistics"])
async def get_category_stats():
    """Get media by category statistics."""
    user_id = get_current_user_id()
    
    user_media = [m for m in _media_library_db.values() if m["created_by"] == user_id]
    
    category_stats = {}
    for category in MediaCategory:
        items = [m for m in user_media if m["category"] == category]
        category_stats[category.value] = {
            "count": len(items),
            "total_duration_seconds": sum(m.get("duration_seconds", 0) or 0 for m in items)
        }
    
    return {
        "user_id": str(user_id),
        "categories": category_stats,
        "timestamp": datetime.utcnow().isoformat()
    }
