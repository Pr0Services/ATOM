"""
CHE·NU™ V68 - Entertainment & Media API Routes
Vertical 12: Media Platform

50+ endpoints for complete entertainment functionality.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field

from ..agents.entertainment_agent import (
    get_entertainment_agent,
    MediaType, ContentStatus, ContentRating, PlaybackStatus,
    WatchPartyStatus, ModerationAction
)

router = APIRouter(prefix="/api/v2/entertainment", tags=["Entertainment & Media"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class AddContentRequest(BaseModel):
    title: str
    media_type: MediaType
    description: str
    duration_seconds: int
    rating: ContentRating = ContentRating.UNRATED
    genres: List[str] = []
    tags: List[str] = []
    thumbnail_url: Optional[str] = None
    stream_url: Optional[str] = None
    release_date: Optional[datetime] = None


class ModerateContentRequest(BaseModel):
    action: ModerationAction
    reason: Optional[str] = None


class CreateShowRequest(BaseModel):
    title: str
    description: str
    rating: ContentRating
    genres: List[str]
    thumbnail_url: Optional[str] = None


class AddSeasonRequest(BaseModel):
    season_number: int
    title: str
    description: str = ""


class AddEpisodeRequest(BaseModel):
    episode_number: int
    title: str
    description: str
    duration_seconds: int
    stream_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class CreatePlaylistRequest(BaseModel):
    name: str
    description: str = ""
    is_public: bool = False


class RecordProgressRequest(BaseModel):
    progress_seconds: int


class CreateWatchPartyRequest(BaseModel):
    content_id: UUID
    scheduled_for: Optional[datetime] = None
    max_participants: int = 10


class ControlWatchPartyRequest(BaseModel):
    action: str  # play, pause, seek, end
    position_seconds: Optional[int] = None


class SubmitReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    title: str
    text: str


class CreateChannelRequest(BaseModel):
    name: str
    description: str
    thumbnail_url: Optional[str] = None


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    agent = get_entertainment_agent()
    return await agent.get_health()


# ============================================================================
# CONTENT MANAGEMENT
# ============================================================================

@router.post("/content")
async def add_content(
    request: AddContentRequest,
    user_id: str = Query(...)
):
    """Add new content (starts as draft - requires moderation)."""
    agent = get_entertainment_agent()
    content = await agent.add_content(
        title=request.title,
        media_type=request.media_type,
        description=request.description,
        duration_seconds=request.duration_seconds,
        rating=request.rating,
        genres=request.genres,
        tags=request.tags,
        thumbnail_url=request.thumbnail_url,
        stream_url=request.stream_url,
        release_date=request.release_date,
        user_id=user_id
    )
    return {
        "content": _serialize_content(content),
        "message": "Content added as draft - requires moderation"
    }


@router.post("/content/{content_id}/submit-for-review")
async def submit_for_review(
    content_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Submit content for moderation review."""
    agent = get_entertainment_agent()
    try:
        content = await agent.submit_for_review(content_id, user_id)
        return {"content": _serialize_content(content), "message": "Submitted for review"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/content/{content_id}/moderate")
async def moderate_content(
    request: ModerateContentRequest,
    content_id: UUID = Path(...),
    moderator_id: str = Query(...)
):
    """Moderate content (GOVERNANCE: human approval required)."""
    agent = get_entertainment_agent()
    try:
        content = await agent.moderate_content(
            content_id, request.action, moderator_id, request.reason
        )
        return {"content": _serialize_content(content), "message": f"Content {request.action.value}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/content")
async def get_content_library(
    media_type: Optional[MediaType] = None,
    genre: Optional[str] = None,
    status: Optional[ContentStatus] = None
):
    """Get content library - CHRONOLOGICAL (Rule #5)."""
    agent = get_entertainment_agent()
    content = await agent.get_content_library(media_type, genre, status)
    return {
        "content": [_serialize_content(c) for c in content],
        "total": len(content),
        "sort_order": "chronological_by_added_date"
    }


@router.get("/content/search")
async def search_content(
    query: str = Query(...),
    media_type: Optional[MediaType] = None
):
    """Search content - results CHRONOLOGICAL (Rule #5)."""
    agent = get_entertainment_agent()
    results = await agent.search_content(query, media_type)
    return {
        "results": [_serialize_content(c) for c in results],
        "total": len(results),
        "sort_order": "chronological"
    }


@router.get("/content/{content_id}")
async def get_content(content_id: UUID = Path(...)):
    """Get single content item."""
    agent = get_entertainment_agent()
    content = await agent.get_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"content": _serialize_content(content)}


@router.get("/content/recommendations")
async def get_recommendations(
    user_id: str = Query(...),
    limit: int = Query(20, ge=1, le=100)
):
    """Get recommendations - CHRONOLOGICAL newest first (Rule #5)."""
    agent = get_entertainment_agent()
    content = await agent.get_recommendations(user_id, limit)
    return {
        "recommendations": [_serialize_content(c) for c in content],
        "total": len(content),
        "sort_order": "chronological_newest_first",
        "note": "NO personalized engagement-based sorting (Rule #5)"
    }


@router.get("/content/new-releases")
async def get_new_releases(
    media_type: Optional[MediaType] = None,
    limit: int = Query(20, ge=1, le=100)
):
    """Get new releases - by release date."""
    agent = get_entertainment_agent()
    content = await agent.get_new_releases(media_type, limit)
    return {"new_releases": [_serialize_content(c) for c in content], "total": len(content)}


@router.get("/content/genre/{genre}")
async def get_genre_content(
    genre: str = Path(...),
    limit: int = Query(20, ge=1, le=100)
):
    """Get content by genre - CHRONOLOGICAL."""
    agent = get_entertainment_agent()
    content = await agent.get_genre_content(genre, limit)
    return {"content": [_serialize_content(c) for c in content], "total": len(content)}


# ============================================================================
# TV SHOWS
# ============================================================================

@router.post("/shows")
async def create_show(
    request: CreateShowRequest,
    user_id: str = Query(...)
):
    """Create a TV show."""
    agent = get_entertainment_agent()
    show = await agent.create_show(
        title=request.title,
        description=request.description,
        rating=request.rating,
        genres=request.genres,
        thumbnail_url=request.thumbnail_url,
        user_id=user_id
    )
    return {"show": _serialize_show(show)}


@router.post("/shows/{show_id}/seasons")
async def add_season(
    request: AddSeasonRequest,
    show_id: UUID = Path(...)
):
    """Add a season to show."""
    agent = get_entertainment_agent()
    try:
        season = await agent.add_season(
            show_id=show_id,
            season_number=request.season_number,
            title=request.title,
            description=request.description
        )
        return {"season": _serialize_season(season)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/shows/{show_id}/seasons/{season_id}/episodes")
async def add_episode(
    request: AddEpisodeRequest,
    show_id: UUID = Path(...),
    season_id: UUID = Path(...)
):
    """Add an episode."""
    agent = get_entertainment_agent()
    try:
        episode = await agent.add_episode(
            show_id=show_id,
            season_id=season_id,
            episode_number=request.episode_number,
            title=request.title,
            description=request.description,
            duration_seconds=request.duration_seconds,
            stream_url=request.stream_url,
            thumbnail_url=request.thumbnail_url
        )
        return {"episode": _serialize_episode(episode)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/shows/{show_id}/episodes")
async def get_show_episodes(
    show_id: UUID = Path(...),
    season_id: Optional[UUID] = None
):
    """Get episodes - ordered by season/episode number."""
    agent = get_entertainment_agent()
    episodes = await agent.get_show_episodes(show_id, season_id)
    return {"episodes": [_serialize_episode(e) for e in episodes], "total": len(episodes)}


# ============================================================================
# PLAYLISTS
# ============================================================================

@router.post("/playlists")
async def create_playlist(
    request: CreatePlaylistRequest,
    user_id: str = Query(...)
):
    """Create a playlist."""
    agent = get_entertainment_agent()
    playlist = await agent.create_playlist(
        name=request.name,
        description=request.description,
        owner_id=user_id,
        is_public=request.is_public
    )
    return {"playlist": _serialize_playlist(playlist)}


@router.post("/playlists/{playlist_id}/items")
async def add_to_playlist(
    playlist_id: UUID = Path(...),
    content_id: UUID = Query(...),
    user_id: str = Query(...)
):
    """Add content to playlist."""
    agent = get_entertainment_agent()
    try:
        playlist = await agent.add_to_playlist(playlist_id, content_id, user_id)
        return {"playlist": _serialize_playlist(playlist)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/playlists/{playlist_id}/items/{content_id}")
async def remove_from_playlist(
    playlist_id: UUID = Path(...),
    content_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Remove content from playlist."""
    agent = get_entertainment_agent()
    try:
        playlist = await agent.remove_from_playlist(playlist_id, content_id, user_id)
        return {"playlist": _serialize_playlist(playlist)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/playlists/mine")
async def get_my_playlists(user_id: str = Query(...)):
    """Get user's playlists - ALPHABETICAL (Rule #5)."""
    agent = get_entertainment_agent()
    playlists = await agent.get_user_playlists(user_id)
    return {
        "playlists": [_serialize_playlist(p) for p in playlists],
        "total": len(playlists),
        "sort_order": "alphabetical"
    }


@router.get("/playlists/public")
async def get_public_playlists():
    """Get public playlists - ALPHABETICAL."""
    agent = get_entertainment_agent()
    playlists = await agent.get_public_playlists()
    return {"playlists": [_serialize_playlist(p) for p in playlists], "total": len(playlists)}


# ============================================================================
# WATCH HISTORY
# ============================================================================

@router.post("/watch-progress")
async def record_watch_progress(
    request: RecordProgressRequest,
    content_id: UUID = Query(...),
    user_id: str = Query(...)
):
    """Record watch progress."""
    agent = get_entertainment_agent()
    try:
        history = await agent.record_watch_progress(
            user_id, content_id, request.progress_seconds
        )
        return {"history": _serialize_history(history)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/watch-history")
async def get_watch_history(user_id: str = Query(...)):
    """Get watch history - CHRONOLOGICAL by last watched."""
    agent = get_entertainment_agent()
    history = await agent.get_watch_history(user_id)
    return {"history": [_serialize_history(h) for h in history], "total": len(history)}


@router.get("/continue-watching")
async def get_continue_watching(user_id: str = Query(...)):
    """Get in-progress content - CHRONOLOGICAL."""
    agent = get_entertainment_agent()
    history = await agent.get_continue_watching(user_id)
    return {"items": [_serialize_history(h) for h in history], "total": len(history)}


# ============================================================================
# WATCHLIST
# ============================================================================

@router.post("/watchlist")
async def add_to_watchlist(
    content_id: UUID = Query(...),
    user_id: str = Query(...)
):
    """Add to watchlist."""
    agent = get_entertainment_agent()
    try:
        watchlist = await agent.add_to_watchlist(user_id, content_id)
        return {"watchlist_size": len(watchlist.content_ids)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/watchlist/{content_id}")
async def remove_from_watchlist(
    content_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Remove from watchlist."""
    agent = get_entertainment_agent()
    try:
        watchlist = await agent.remove_from_watchlist(user_id, content_id)
        return {"watchlist_size": len(watchlist.content_ids)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/watchlist")
async def get_watchlist(user_id: str = Query(...)):
    """Get watchlist - in added order."""
    agent = get_entertainment_agent()
    items = await agent.get_watchlist(user_id)
    return {"items": [_serialize_content(c) for c in items], "total": len(items)}


# ============================================================================
# WATCH PARTIES
# ============================================================================

@router.post("/watch-parties")
async def create_watch_party(
    request: CreateWatchPartyRequest,
    host_id: str = Query(...)
):
    """Create a watch party."""
    agent = get_entertainment_agent()
    try:
        party = await agent.create_watch_party(
            host_id=host_id,
            content_id=request.content_id,
            scheduled_for=request.scheduled_for,
            max_participants=request.max_participants
        )
        return {"watch_party": _serialize_party(party)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/watch-parties/{party_id}/join")
async def join_watch_party(
    party_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Join a watch party."""
    agent = get_entertainment_agent()
    try:
        party = await agent.join_watch_party(party_id, user_id)
        return {"watch_party": _serialize_party(party)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/watch-parties/{party_id}/leave")
async def leave_watch_party(
    party_id: UUID = Path(...),
    user_id: str = Query(...)
):
    """Leave a watch party."""
    agent = get_entertainment_agent()
    try:
        party = await agent.leave_watch_party(party_id, user_id)
        return {"watch_party": _serialize_party(party)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/watch-parties/{party_id}/control")
async def control_watch_party(
    request: ControlWatchPartyRequest,
    party_id: UUID = Path(...),
    host_id: str = Query(...)
):
    """Control watch party playback (host only)."""
    agent = get_entertainment_agent()
    try:
        party = await agent.control_watch_party(
            party_id, host_id, request.action, request.position_seconds
        )
        return {"watch_party": _serialize_party(party)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/watch-parties/active")
async def get_active_watch_parties():
    """Get active watch parties - CHRONOLOGICAL."""
    agent = get_entertainment_agent()
    parties = await agent.get_active_watch_parties()
    return {"watch_parties": [_serialize_party(p) for p in parties], "total": len(parties)}


# ============================================================================
# REVIEWS & MODERATION
# ============================================================================

@router.post("/content/{content_id}/reviews")
async def submit_review(
    request: SubmitReviewRequest,
    content_id: UUID = Path(...),
    user_id: str = Query(...),
    user_name: str = Query(...)
):
    """Submit a review (requires moderation)."""
    agent = get_entertainment_agent()
    try:
        review = await agent.submit_review(
            content_id=content_id,
            user_id=user_id,
            user_name=user_name,
            rating=request.rating,
            title=request.title,
            text=request.text
        )
        return {
            "review": _serialize_review(review),
            "message": "Review submitted - pending moderation"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reviews/{review_id}/moderate")
async def moderate_review(
    review_id: UUID = Path(...),
    action: ModerationAction = Query(...),
    moderator_id: str = Query(...)
):
    """Moderate a review (GOVERNANCE: human approval)."""
    agent = get_entertainment_agent()
    try:
        review = await agent.moderate_review(review_id, action, moderator_id)
        return {"review": _serialize_review(review), "message": f"Review {action.value}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/content/{content_id}/reviews")
async def get_content_reviews(content_id: UUID = Path(...)):
    """Get reviews - CHRONOLOGICAL (Rule #5)."""
    agent = get_entertainment_agent()
    reviews = await agent.get_content_reviews(content_id)
    return {
        "reviews": [_serialize_review(r) for r in reviews],
        "total": len(reviews),
        "sort_order": "chronological"
    }


@router.get("/moderation/pending")
async def get_pending_moderation():
    """Get pending moderation requests."""
    agent = get_entertainment_agent()
    requests = await agent.get_pending_moderation()
    return {"requests": [_serialize_moderation(r) for r in requests], "total": len(requests)}


# ============================================================================
# CHANNELS
# ============================================================================

@router.post("/channels")
async def create_channel(
    request: CreateChannelRequest,
    owner_id: str = Query(...)
):
    """Create a channel."""
    agent = get_entertainment_agent()
    channel = await agent.create_channel(
        name=request.name,
        description=request.description,
        owner_id=owner_id,
        thumbnail_url=request.thumbnail_url
    )
    return {"channel": _serialize_channel(channel)}


@router.get("/channels")
async def get_channels():
    """Get channels - ALPHABETICAL (Rule #5)."""
    agent = get_entertainment_agent()
    channels = await agent.get_channels()
    return {
        "channels": [_serialize_channel(c) for c in channels],
        "total": len(channels),
        "sort_order": "alphabetical"
    }


# ============================================================================
# ANALYTICS
# ============================================================================

@router.get("/stats")
async def get_library_stats(user_id: Optional[str] = None):
    """Get library statistics."""
    agent = get_entertainment_agent()
    stats = await agent.get_library_stats(user_id)
    return stats


# ============================================================================
# SERIALIZERS
# ============================================================================

def _serialize_content(content) -> Dict[str, Any]:
    return {
        "id": str(content.id),
        "title": content.title,
        "media_type": content.media_type.value,
        "description": content.description,
        "duration_seconds": content.duration_seconds,
        "status": content.status.value,
        "rating": content.rating.value,
        "genres": content.genres,
        "tags": content.tags,
        "thumbnail_url": content.thumbnail_url,
        "stream_url": content.stream_url,
        "release_date": content.release_date.isoformat() if content.release_date else None,
        "created_at": content.created_at.isoformat(),
        "created_by": content.created_by,
        "published_at": content.published_at.isoformat() if content.published_at else None,
        "view_count": content.view_count
    }


def _serialize_show(show) -> Dict[str, Any]:
    return {
        "id": str(show.id),
        "title": show.title,
        "description": show.description,
        "status": show.status.value,
        "rating": show.rating.value,
        "genres": show.genres,
        "thumbnail_url": show.thumbnail_url,
        "seasons_count": show.seasons_count,
        "created_at": show.created_at.isoformat()
    }


def _serialize_season(season) -> Dict[str, Any]:
    return {
        "id": str(season.id),
        "show_id": str(season.show_id),
        "season_number": season.season_number,
        "title": season.title,
        "description": season.description,
        "episode_count": season.episode_count
    }


def _serialize_episode(episode) -> Dict[str, Any]:
    return {
        "id": str(episode.id),
        "show_id": str(episode.show_id),
        "season_id": str(episode.season_id),
        "episode_number": episode.episode_number,
        "title": episode.title,
        "description": episode.description,
        "duration_seconds": episode.duration_seconds,
        "stream_url": episode.stream_url,
        "thumbnail_url": episode.thumbnail_url
    }


def _serialize_playlist(playlist) -> Dict[str, Any]:
    return {
        "id": str(playlist.id),
        "name": playlist.name,
        "description": playlist.description,
        "owner_id": playlist.owner_id,
        "is_public": playlist.is_public,
        "items": [str(i) for i in playlist.items],
        "item_count": len(playlist.items),
        "created_at": playlist.created_at.isoformat(),
        "updated_at": playlist.updated_at.isoformat()
    }


def _serialize_history(history) -> Dict[str, Any]:
    return {
        "id": str(history.id),
        "content_id": str(history.content_id),
        "content_title": history.content_title,
        "playback_status": history.playback_status.value,
        "progress_seconds": history.progress_seconds,
        "duration_seconds": history.duration_seconds,
        "progress_percent": round(history.progress_seconds / history.duration_seconds * 100, 1) if history.duration_seconds > 0 else 0,
        "last_watched": history.last_watched.isoformat()
    }


def _serialize_party(party) -> Dict[str, Any]:
    return {
        "id": str(party.id),
        "host_id": party.host_id,
        "content_id": str(party.content_id),
        "content_title": party.content_title,
        "status": party.status.value,
        "scheduled_for": party.scheduled_for.isoformat() if party.scheduled_for else None,
        "participants": party.participants,
        "participant_count": len(party.participants),
        "max_participants": party.max_participants,
        "current_position_seconds": party.current_position_seconds,
        "is_playing": party.is_playing
    }


def _serialize_review(review) -> Dict[str, Any]:
    return {
        "id": str(review.id),
        "content_id": str(review.content_id),
        "user_id": review.user_id,
        "user_name": review.user_name,
        "rating": review.rating,
        "title": review.title,
        "text": review.text,
        "status": review.status.value,
        "created_at": review.created_at.isoformat()
    }


def _serialize_moderation(mod) -> Dict[str, Any]:
    return {
        "id": str(mod.id),
        "content_type": mod.content_type,
        "content_id": str(mod.content_id),
        "reason": mod.reason,
        "status": mod.status,
        "created_at": mod.created_at.isoformat()
    }


def _serialize_channel(channel) -> Dict[str, Any]:
    return {
        "id": str(channel.id),
        "name": channel.name,
        "description": channel.description,
        "owner_id": channel.owner_id,
        "thumbnail_url": channel.thumbnail_url,
        "subscriber_count": channel.subscriber_count,
        "content_count": channel.content_count,
        "created_at": channel.created_at.isoformat()
    }
