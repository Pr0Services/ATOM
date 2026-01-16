"""
CHE·NU™ V75 Backend - Streaming Router

API endpoints for STREAMING sphere.

Content types: movies, series, podcasts, music, live streams, shorts

@version 75.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import uuid

from config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import require_auth
from services.streaming_service import StreamingService
from models.streaming import ContentType, ContentStatus


router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class ContentBase(BaseModel):
    """Base content schema."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    content_type: str  # movie, series, podcast, etc.
    
    class Config:
        from_attributes = True


class ContentCreate(ContentBase):
    """Create content request."""
    original_title: Optional[str] = None
    duration_seconds: Optional[int] = None
    release_year: Optional[int] = None
    thumbnail_url: Optional[str] = None
    poster_url: Optional[str] = None
    language: str = "fr"
    maturity_rating: Optional[str] = None
    genre_ids: List[str] = []
    
    # For episodes
    parent_id: Optional[str] = None
    season_number: Optional[int] = None
    episode_number: Optional[int] = None


class ContentResponse(ContentBase):
    """Content response."""
    id: str
    status: str
    duration_seconds: Optional[int]
    duration_formatted: str
    release_year: Optional[int]
    thumbnail_url: Optional[str]
    poster_url: Optional[str]
    rating: float
    rating_count: int
    view_count: int
    language: str
    maturity_rating: Optional[str]
    created_at: datetime


class StreamSourceResponse(BaseModel):
    """Stream source response."""
    id: str
    source_type: str
    quality: Optional[str]
    url: str
    bitrate: Optional[int]
    is_default: bool
    
    class Config:
        from_attributes = True


class ProgressUpdate(BaseModel):
    """Watch progress update."""
    position_seconds: int
    duration_seconds: Optional[int] = None


class ProgressResponse(BaseModel):
    """Watch progress response."""
    content_id: str
    position_seconds: int
    progress_percent: float
    is_completed: bool
    last_watched_at: datetime
    
    class Config:
        from_attributes = True


class PlaylistCreate(BaseModel):
    """Create playlist request."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    is_public: bool = False


class PlaylistResponse(BaseModel):
    """Playlist response."""
    id: str
    name: str
    description: Optional[str]
    playlist_type: str
    thumbnail_url: Optional[str]
    is_public: bool
    item_count: int
    total_duration: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChannelCreate(BaseModel):
    """Create channel request."""
    name: str = Field(..., min_length=1, max_length=100)
    handle: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    channel_type: str = "general"


class ChannelResponse(BaseModel):
    """Channel response."""
    id: str
    name: str
    handle: str
    description: Optional[str]
    avatar_url: Optional[str]
    banner_url: Optional[str]
    channel_type: str
    subscriber_count: int
    content_count: int
    is_verified: bool
    is_monetized: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    """Create rating request."""
    rating: float = Field(..., ge=0, le=10)
    review: Optional[str] = None
    is_spoiler: bool = False


class LiveStreamCreate(BaseModel):
    """Create live stream request."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    scheduled_start: Optional[datetime] = None


class LiveStreamResponse(BaseModel):
    """Live stream response."""
    id: str
    title: str
    description: Optional[str]
    status: str
    hls_url: Optional[str]
    thumbnail_url: Optional[str]
    scheduled_start: Optional[datetime]
    actual_start: Optional[datetime]
    current_viewers: int
    peak_viewers: int
    
    class Config:
        from_attributes = True


# ============================================================================
# CONTENT ENDPOINTS
# ============================================================================

@router.get("/content")
async def list_content(
    content_type: Optional[str] = None,
    genre: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """
    List media content with filters.
    
    Content types: movie, series, episode, podcast, podcast_episode,
                   music_album, music_track, live_stream, short, documentary
    """
    service = StreamingService(db)
    
    content = await service.list_content(
        content_type=content_type,
        genre_slug=genre,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )
    
    return {
        "success": True,
        "data": [
            {
                "id": str(c.id),
                "title": c.title,
                "content_type": c.content_type,
                "duration_formatted": c.duration_formatted,
                "thumbnail_url": c.thumbnail_url,
                "rating": c.rating,
                "view_count": c.view_count,
            }
            for c in content
        ],
        "pagination": {
            "limit": limit,
            "offset": offset,
            "has_more": len(content) == limit,
        }
    }


@router.get("/content/trending")
async def get_trending(
    content_type: Optional[str] = None,
    period: int = Query(7, ge=1, le=30),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get trending content."""
    service = StreamingService(db)
    
    content = await service.get_trending(
        content_type=content_type,
        period_days=period,
        limit=limit,
    )
    
    return {
        "success": True,
        "data": [
            {
                "id": str(c.id),
                "title": c.title,
                "content_type": c.content_type,
                "thumbnail_url": c.thumbnail_url,
                "view_count": c.view_count,
                "rating": c.rating,
            }
            for c in content
        ]
    }


@router.get("/content/recommendations")
async def get_recommendations(
    content_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get personalized recommendations."""
    service = StreamingService(db)
    
    content = await service.get_recommendations(
        user_id=user["id"],
        content_type=content_type,
        limit=limit,
    )
    
    return {
        "success": True,
        "data": [
            {
                "id": str(c.id),
                "title": c.title,
                "content_type": c.content_type,
                "thumbnail_url": c.thumbnail_url,
                "rating": c.rating,
            }
            for c in content
        ]
    }


@router.get("/content/{content_id}")
async def get_content(
    content_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get content details."""
    service = StreamingService(db)
    
    content = await service.get_content(content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Increment view
    await service.increment_view(content_id)
    
    # Get user's progress
    progress = await service.get_progress(user["id"], content_id)
    
    return {
        "success": True,
        "data": {
            "id": str(content.id),
            "title": content.title,
            "original_title": content.original_title,
            "description": content.description,
            "content_type": content.content_type,
            "status": content.status,
            "duration_seconds": content.duration_seconds,
            "duration_formatted": content.duration_formatted,
            "release_year": content.release_year,
            "thumbnail_url": content.thumbnail_url,
            "poster_url": content.poster_url,
            "banner_url": content.banner_url,
            "rating": content.rating,
            "rating_count": content.rating_count,
            "view_count": content.view_count,
            "language": content.language,
            "maturity_rating": content.maturity_rating,
            "genres": [{"id": str(g.id), "name": g.name} for g in content.genres],
            "streams": [
                {
                    "id": str(s.id),
                    "source_type": s.source_type,
                    "quality": s.quality,
                    "url": s.url,
                    "is_default": s.is_default,
                }
                for s in content.streams
            ],
            "progress": {
                "position_seconds": progress.position_seconds if progress else 0,
                "progress_percent": progress.progress_percent if progress else 0,
                "is_completed": progress.is_completed if progress else False,
            } if progress else None,
            "channel": {
                "id": str(content.channel.id),
                "name": content.channel.name,
                "handle": content.channel.handle,
            } if content.channel else None,
        }
    }


@router.get("/content/{content_id}/episodes")
async def get_episodes(
    content_id: str,
    season: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get episodes for a series/podcast."""
    service = StreamingService(db)
    
    episodes = await service.list_content(
        content_type=ContentType.EPISODE,
        limit=100,
    )
    
    # Filter by parent
    episodes = [e for e in episodes if str(e.parent_id) == content_id]
    
    if season:
        episodes = [e for e in episodes if e.season_number == season]
    
    return {
        "success": True,
        "data": [
            {
                "id": str(e.id),
                "title": e.title,
                "season_number": e.season_number,
                "episode_number": e.episode_number,
                "duration_formatted": e.duration_formatted,
                "thumbnail_url": e.thumbnail_url,
            }
            for e in sorted(episodes, key=lambda x: (x.season_number or 0, x.episode_number or 0))
        ]
    }


# ============================================================================
# WATCH PROGRESS
# ============================================================================

@router.post("/content/{content_id}/progress")
async def update_progress(
    content_id: str,
    data: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Update watch progress."""
    service = StreamingService(db)
    
    progress = await service.update_progress(
        user_id=user["id"],
        content_id=content_id,
        position_seconds=data.position_seconds,
        duration_seconds=data.duration_seconds,
    )
    
    return {
        "success": True,
        "data": {
            "position_seconds": progress.position_seconds,
            "progress_percent": progress.progress_percent,
            "is_completed": progress.is_completed,
        }
    }


@router.get("/continue-watching")
async def get_continue_watching(
    limit: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get content to continue watching."""
    service = StreamingService(db)
    
    items = await service.get_continue_watching(user["id"], limit)
    
    return {
        "success": True,
        "data": [
            {
                "content": {
                    "id": str(item["content"].id),
                    "title": item["content"].title,
                    "thumbnail_url": item["content"].thumbnail_url,
                    "content_type": item["content"].content_type,
                },
                "progress_percent": item["progress"],
                "position_seconds": item["position"],
                "last_watched": item["last_watched"].isoformat(),
            }
            for item in items
        ]
    }


@router.get("/history")
async def get_watch_history(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get watch history."""
    service = StreamingService(db)
    
    history = await service.get_watch_history(user["id"], limit, offset)
    
    return {
        "success": True,
        "data": [
            {
                "content_id": str(h.content_id),
                "content": {
                    "id": str(h.content.id),
                    "title": h.content.title,
                    "thumbnail_url": h.content.thumbnail_url,
                } if h.content else None,
                "progress_percent": h.progress_percent,
                "is_completed": h.is_completed,
                "last_watched": h.last_watched_at.isoformat(),
            }
            for h in history
        ],
        "pagination": {
            "limit": limit,
            "offset": offset,
        }
    }


# ============================================================================
# WATCHLIST & PLAYLISTS
# ============================================================================

@router.get("/watchlist")
async def get_watchlist(
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get user's watchlist."""
    service = StreamingService(db)
    
    watchlist = await service.get_or_create_watchlist(user["id"])
    
    return {
        "success": True,
        "data": {
            "id": str(watchlist.id),
            "name": watchlist.name,
            "item_count": watchlist.item_count,
            "items": [
                {
                    "id": str(item.id),
                    "title": item.title,
                    "content_type": item.content_type,
                    "thumbnail_url": item.thumbnail_url,
                }
                for item in watchlist.items
            ]
        }
    }


@router.post("/watchlist/{content_id}")
async def add_to_watchlist(
    content_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Add content to watchlist."""
    service = StreamingService(db)
    
    await service.add_to_watchlist(user["id"], content_id)
    
    return {"success": True, "message": "Added to watchlist"}


@router.delete("/watchlist/{content_id}")
async def remove_from_watchlist(
    content_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Remove content from watchlist."""
    service = StreamingService(db)
    
    await service.remove_from_watchlist(user["id"], content_id)
    
    return {"success": True, "message": "Removed from watchlist"}


@router.get("/playlists")
async def get_playlists(
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get user's playlists."""
    service = StreamingService(db)
    
    playlists = await service.get_user_playlists(user["id"])
    
    return {
        "success": True,
        "data": [
            {
                "id": str(p.id),
                "name": p.name,
                "playlist_type": p.playlist_type,
                "thumbnail_url": p.thumbnail_url,
                "item_count": p.item_count,
                "is_public": p.is_public,
            }
            for p in playlists
        ]
    }


@router.post("/playlists")
async def create_playlist(
    data: PlaylistCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Create a new playlist."""
    service = StreamingService(db)
    
    playlist = await service.create_playlist(
        user_id=user["id"],
        name=data.name,
        description=data.description,
        is_public=data.is_public,
    )
    
    return {
        "success": True,
        "data": {
            "id": str(playlist.id),
            "name": playlist.name,
        }
    }


# ============================================================================
# CHANNELS
# ============================================================================

@router.get("/channels")
async def list_channels(
    search: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """List channels."""
    # TODO: Implement channel listing
    return {
        "success": True,
        "data": []
    }


@router.get("/channels/{handle}")
async def get_channel(
    handle: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get channel by handle."""
    service = StreamingService(db)
    
    channel = await service.get_channel_by_handle(handle)
    
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    return {
        "success": True,
        "data": {
            "id": str(channel.id),
            "name": channel.name,
            "handle": channel.handle,
            "description": channel.description,
            "avatar_url": channel.avatar_url,
            "banner_url": channel.banner_url,
            "subscriber_count": channel.subscriber_count,
            "content_count": channel.content_count,
            "is_verified": channel.is_verified,
        }
    }


@router.post("/channels")
async def create_channel(
    data: ChannelCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Create a new channel."""
    service = StreamingService(db)
    
    # Check handle availability
    existing = await service.get_channel_by_handle(data.handle)
    if existing:
        raise HTTPException(status_code=400, detail="Handle already taken")
    
    channel = await service.create_channel(
        owner_id=user["id"],
        name=data.name,
        handle=data.handle,
        description=data.description,
        channel_type=data.channel_type,
    )
    
    return {
        "success": True,
        "data": {
            "id": str(channel.id),
            "handle": channel.handle,
        }
    }


@router.post("/channels/{channel_id}/subscribe")
async def subscribe_channel(
    channel_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Subscribe to a channel."""
    service = StreamingService(db)
    
    await service.subscribe_to_channel(user["id"], channel_id)
    
    return {"success": True, "message": "Subscribed"}


@router.delete("/channels/{channel_id}/subscribe")
async def unsubscribe_channel(
    channel_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Unsubscribe from a channel."""
    service = StreamingService(db)
    
    await service.unsubscribe_from_channel(user["id"], channel_id)
    
    return {"success": True, "message": "Unsubscribed"}


# ============================================================================
# RATINGS
# ============================================================================

@router.post("/content/{content_id}/rate")
async def rate_content(
    content_id: str,
    data: RatingCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Rate content."""
    service = StreamingService(db)
    
    rating = await service.rate_content(
        user_id=user["id"],
        content_id=content_id,
        rating=data.rating,
        review=data.review,
    )
    
    return {
        "success": True,
        "data": {
            "rating": rating.rating,
            "review": rating.review,
        }
    }


# ============================================================================
# GENRES
# ============================================================================

@router.get("/genres")
async def list_genres(
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """List all genres."""
    service = StreamingService(db)
    
    genres = await service.get_genres()
    
    return {
        "success": True,
        "data": [
            {
                "id": str(g.id),
                "name": g.name,
                "slug": g.slug,
                "icon": g.icon,
            }
            for g in genres
        ]
    }


@router.get("/genres/{slug}/content")
async def get_genre_content(
    slug: str,
    content_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get content by genre."""
    service = StreamingService(db)
    
    content = await service.get_content_by_genre(
        genre_slug=slug,
        content_type=content_type,
        limit=limit,
        offset=offset,
    )
    
    return {
        "success": True,
        "data": [
            {
                "id": str(c.id),
                "title": c.title,
                "content_type": c.content_type,
                "thumbnail_url": c.thumbnail_url,
                "rating": c.rating,
            }
            for c in content
        ]
    }


# ============================================================================
# LIVE STREAMING
# ============================================================================

@router.get("/live")
async def get_live_streams(
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Get active live streams."""
    service = StreamingService(db)
    
    streams = await service.get_live_streams(status="live", limit=limit)
    
    return {
        "success": True,
        "data": [
            {
                "id": str(s.id),
                "title": s.title,
                "thumbnail_url": s.thumbnail_url,
                "current_viewers": s.current_viewers,
                "channel_id": str(s.channel_id),
            }
            for s in streams
        ]
    }


@router.post("/live")
async def create_live_stream(
    data: LiveStreamCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_auth),
):
    """Create a live stream."""
    service = StreamingService(db)
    
    # Get user's channel
    # TODO: Get channel_id from user
    
    stream = await service.create_live_stream(
        channel_id="",  # TODO
        title=data.title,
        description=data.description,
        scheduled_start=data.scheduled_start,
    )
    
    return {
        "success": True,
        "data": {
            "id": str(stream.id),
            "stream_key": stream.stream_key,
            "rtmp_url": stream.rtmp_url,
        }
    }
