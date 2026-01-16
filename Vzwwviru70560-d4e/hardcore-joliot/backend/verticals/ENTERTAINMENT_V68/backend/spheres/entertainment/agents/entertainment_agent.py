"""
CHE·NU™ V68 - Entertainment & Media Agent
Vertical 12: Media Platform (Plex/Netflix Killer)

GOVERNANCE:
- Content moderation requires human review
- Publishing requires approval
- NO engagement-based recommendations (Rule #5)

RULE #5 COMPLIANCE:
- Content listed CHRONOLOGICALLY (by added date)
- Playlists listed ALPHABETICALLY
- NO "trending" or popularity-based sorting
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from uuid import UUID, uuid4
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class MediaType(Enum):
    MOVIE = "movie"
    TV_SHOW = "tv_show"
    EPISODE = "episode"
    MUSIC = "music"
    PODCAST = "podcast"
    AUDIOBOOK = "audiobook"
    LIVE_STREAM = "live_stream"


class ContentStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    PUBLISHED = "published"
    RESTRICTED = "restricted"
    ARCHIVED = "archived"


class ContentRating(Enum):
    G = "G"
    PG = "PG"
    PG13 = "PG-13"
    R = "R"
    NC17 = "NC-17"
    UNRATED = "Unrated"


class PlaybackStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class WatchPartyStatus(Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    ENDED = "ended"
    CANCELLED = "cancelled"


class ModerationAction(Enum):
    APPROVE = "approve"
    REJECT = "reject"
    FLAG = "flag"
    RESTRICT = "restrict"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class MediaContent:
    """Media content item."""
    id: UUID
    title: str
    media_type: MediaType
    description: str
    duration_seconds: int
    status: ContentStatus
    rating: ContentRating
    genres: List[str]
    tags: List[str]
    thumbnail_url: Optional[str]
    stream_url: Optional[str]
    release_date: Optional[datetime]
    created_at: datetime
    created_by: str
    published_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    view_count: int = 0


@dataclass
class TVShow:
    """TV show with seasons/episodes."""
    id: UUID
    title: str
    description: str
    status: ContentStatus
    rating: ContentRating
    genres: List[str]
    thumbnail_url: Optional[str]
    created_at: datetime
    created_by: str
    seasons_count: int = 0


@dataclass
class Season:
    """Season of a TV show."""
    id: UUID
    show_id: UUID
    season_number: int
    title: str
    description: str
    episode_count: int
    created_at: datetime


@dataclass
class Episode:
    """Episode of a season."""
    id: UUID
    show_id: UUID
    season_id: UUID
    episode_number: int
    title: str
    description: str
    duration_seconds: int
    stream_url: Optional[str]
    thumbnail_url: Optional[str]
    created_at: datetime


@dataclass
class Playlist:
    """User playlist."""
    id: UUID
    name: str
    description: str
    owner_id: str
    is_public: bool
    items: List[UUID]  # Content IDs in order
    created_at: datetime
    updated_at: datetime


@dataclass
class WatchHistory:
    """User watch history."""
    id: UUID
    user_id: str
    content_id: UUID
    content_title: str
    playback_status: PlaybackStatus
    progress_seconds: int
    duration_seconds: int
    started_at: datetime
    last_watched: datetime
    completed_at: Optional[datetime] = None


@dataclass
class Watchlist:
    """User's watchlist (to watch later)."""
    id: UUID
    user_id: str
    content_ids: List[UUID]
    updated_at: datetime


@dataclass
class WatchParty:
    """Watch party for synchronized viewing."""
    id: UUID
    host_id: str
    content_id: UUID
    content_title: str
    status: WatchPartyStatus
    scheduled_for: Optional[datetime]
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    participants: List[str]
    max_participants: int
    current_position_seconds: int
    is_playing: bool
    created_at: datetime


@dataclass
class Review:
    """User review of content."""
    id: UUID
    content_id: UUID
    user_id: str
    user_name: str
    rating: int  # 1-5 stars
    title: str
    text: str
    status: ContentStatus  # Requires moderation
    created_at: datetime
    moderated_by: Optional[str] = None
    moderated_at: Optional[datetime] = None


@dataclass
class ModerationRequest:
    """Content moderation request."""
    id: UUID
    content_type: str  # "media", "review", etc.
    content_id: UUID
    reason: str
    reported_by: Optional[str]
    status: str  # "pending", "approved", "rejected"
    action: Optional[ModerationAction]
    moderator_id: Optional[str]
    moderated_at: Optional[datetime]
    created_at: datetime


@dataclass
class MediaLibrary:
    """User's media library."""
    id: UUID
    user_id: str
    name: str
    content_ids: Set[UUID]
    created_at: datetime
    updated_at: datetime


@dataclass
class Subscription:
    """User subscription."""
    id: UUID
    user_id: str
    plan_name: str
    price_monthly: Decimal
    features: List[str]
    started_at: datetime
    expires_at: Optional[datetime]
    is_active: bool


@dataclass
class Channel:
    """Content channel/creator."""
    id: UUID
    name: str
    description: str
    owner_id: str
    thumbnail_url: Optional[str]
    subscriber_count: int
    content_count: int
    created_at: datetime


# ============================================================================
# ENTERTAINMENT AGENT
# ============================================================================

class EntertainmentAgent:
    """
    Entertainment & Media Agent for CHE·NU V68.
    
    Competes with: Plex, Netflix, Spotify, YouTube
    
    GOVERNANCE:
    - Content requires moderation before publishing
    - Reviews require moderation
    
    RULE #5:
    - Content listed CHRONOLOGICALLY (by added date)
    - NO trending/popularity sorting
    - Playlists alphabetical
    """
    
    def __init__(self):
        self.content: Dict[UUID, MediaContent] = {}
        self.shows: Dict[UUID, TVShow] = {}
        self.seasons: Dict[UUID, Season] = {}
        self.episodes: Dict[UUID, Episode] = {}
        self.playlists: Dict[UUID, Playlist] = {}
        self.watch_history: Dict[UUID, WatchHistory] = {}
        self.watchlists: Dict[str, Watchlist] = {}  # user_id -> watchlist
        self.watch_parties: Dict[UUID, WatchParty] = {}
        self.reviews: Dict[UUID, Review] = {}
        self.moderation_requests: Dict[UUID, ModerationRequest] = {}
        self.libraries: Dict[UUID, MediaLibrary] = {}
        self.subscriptions: Dict[UUID, Subscription] = {}
        self.channels: Dict[UUID, Channel] = {}
    
    # ========================================================================
    # CONTENT MANAGEMENT
    # ========================================================================
    
    async def add_content(
        self,
        title: str,
        media_type: MediaType,
        description: str,
        duration_seconds: int,
        rating: ContentRating = ContentRating.UNRATED,
        genres: List[str] = None,
        tags: List[str] = None,
        thumbnail_url: Optional[str] = None,
        stream_url: Optional[str] = None,
        release_date: Optional[datetime] = None,
        user_id: str = None
    ) -> MediaContent:
        """
        Add new content (starts as DRAFT - requires review).
        
        GOVERNANCE: All content requires moderation before publishing.
        """
        content = MediaContent(
            id=uuid4(),
            title=title,
            media_type=media_type,
            description=description,
            duration_seconds=duration_seconds,
            status=ContentStatus.DRAFT,  # Requires review
            rating=rating,
            genres=sorted(genres or []),  # Alphabetical
            tags=sorted(tags or []),  # Alphabetical
            thumbnail_url=thumbnail_url,
            stream_url=stream_url,
            release_date=release_date,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.content[content.id] = content
        logger.info(f"Content added (draft): {title}")
        return content
    
    async def submit_for_review(
        self,
        content_id: UUID,
        user_id: str
    ) -> MediaContent:
        """Submit content for moderation review."""
        content = self.content.get(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")
        
        if content.status != ContentStatus.DRAFT:
            raise ValueError("Only draft content can be submitted for review")
        
        content.status = ContentStatus.UNDER_REVIEW
        
        # Create moderation request
        mod_request = ModerationRequest(
            id=uuid4(),
            content_type="media",
            content_id=content_id,
            reason="New content submission",
            reported_by=user_id,
            status="pending",
            action=None,
            moderator_id=None,
            moderated_at=None,
            created_at=datetime.utcnow()
        )
        self.moderation_requests[mod_request.id] = mod_request
        
        return content
    
    async def moderate_content(
        self,
        content_id: UUID,
        action: ModerationAction,
        moderator_id: str,
        reason: Optional[str] = None
    ) -> MediaContent:
        """
        Moderate content (GOVERNANCE: human approval required).
        """
        content = self.content.get(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")
        
        if content.status != ContentStatus.UNDER_REVIEW:
            raise ValueError("Content must be under review to moderate")
        
        if action == ModerationAction.APPROVE:
            content.status = ContentStatus.PUBLISHED
            content.published_at = datetime.utcnow()
            content.reviewed_by = moderator_id
            logger.info(f"Content approved: {content.title}")
        elif action == ModerationAction.REJECT:
            content.status = ContentStatus.DRAFT
            logger.info(f"Content rejected: {content.title}")
        elif action == ModerationAction.RESTRICT:
            content.status = ContentStatus.RESTRICTED
            logger.info(f"Content restricted: {content.title}")
        
        # Update moderation request
        for req in self.moderation_requests.values():
            if req.content_id == content_id and req.status == "pending":
                req.status = "completed"
                req.action = action
                req.moderator_id = moderator_id
                req.moderated_at = datetime.utcnow()
                break
        
        return content
    
    async def get_content_library(
        self,
        media_type: Optional[MediaType] = None,
        genre: Optional[str] = None,
        status: Optional[ContentStatus] = None
    ) -> List[MediaContent]:
        """
        Get content library - CHRONOLOGICAL by added date.
        
        RULE #5: NO popularity/trending sorting.
        """
        items = list(self.content.values())
        
        # Only show published by default
        if status:
            items = [c for c in items if c.status == status]
        else:
            items = [c for c in items if c.status == ContentStatus.PUBLISHED]
        
        if media_type:
            items = [c for c in items if c.media_type == media_type]
        
        if genre:
            items = [c for c in items if genre.lower() in [g.lower() for g in c.genres]]
        
        # RULE #5: CHRONOLOGICAL by created_at (NOT by view_count/popularity)
        return sorted(items, key=lambda c: c.created_at, reverse=True)
    
    async def search_content(
        self,
        query: str,
        media_type: Optional[MediaType] = None
    ) -> List[MediaContent]:
        """
        Search content - results CHRONOLOGICAL.
        
        RULE #5: NO relevance scoring or popularity ranking.
        """
        query_lower = query.lower()
        results = []
        
        for content in self.content.values():
            if content.status != ContentStatus.PUBLISHED:
                continue
            
            if (query_lower in content.title.lower() or 
                query_lower in content.description.lower() or
                any(query_lower in tag.lower() for tag in content.tags)):
                if media_type is None or content.media_type == media_type:
                    results.append(content)
        
        # RULE #5: Return chronologically (NOT by relevance score)
        return sorted(results, key=lambda c: c.created_at, reverse=True)
    
    async def get_content(self, content_id: UUID) -> Optional[MediaContent]:
        """Get single content item."""
        return self.content.get(content_id)
    
    # ========================================================================
    # TV SHOWS
    # ========================================================================
    
    async def create_show(
        self,
        title: str,
        description: str,
        rating: ContentRating,
        genres: List[str],
        thumbnail_url: Optional[str] = None,
        user_id: str = None
    ) -> TVShow:
        """Create a TV show."""
        show = TVShow(
            id=uuid4(),
            title=title,
            description=description,
            status=ContentStatus.DRAFT,
            rating=rating,
            genres=sorted(genres),
            thumbnail_url=thumbnail_url,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.shows[show.id] = show
        return show
    
    async def add_season(
        self,
        show_id: UUID,
        season_number: int,
        title: str,
        description: str = ""
    ) -> Season:
        """Add season to show."""
        show = self.shows.get(show_id)
        if not show:
            raise ValueError(f"Show {show_id} not found")
        
        season = Season(
            id=uuid4(),
            show_id=show_id,
            season_number=season_number,
            title=title,
            description=description,
            episode_count=0,
            created_at=datetime.utcnow()
        )
        
        self.seasons[season.id] = season
        show.seasons_count += 1
        return season
    
    async def add_episode(
        self,
        show_id: UUID,
        season_id: UUID,
        episode_number: int,
        title: str,
        description: str,
        duration_seconds: int,
        stream_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None
    ) -> Episode:
        """Add episode to season."""
        season = self.seasons.get(season_id)
        if not season or season.show_id != show_id:
            raise ValueError("Invalid show or season")
        
        episode = Episode(
            id=uuid4(),
            show_id=show_id,
            season_id=season_id,
            episode_number=episode_number,
            title=title,
            description=description,
            duration_seconds=duration_seconds,
            stream_url=stream_url,
            thumbnail_url=thumbnail_url,
            created_at=datetime.utcnow()
        )
        
        self.episodes[episode.id] = episode
        season.episode_count += 1
        return episode
    
    async def get_show_episodes(
        self,
        show_id: UUID,
        season_id: Optional[UUID] = None
    ) -> List[Episode]:
        """Get episodes - ordered by season/episode number."""
        episodes = [e for e in self.episodes.values() if e.show_id == show_id]
        
        if season_id:
            episodes = [e for e in episodes if e.season_id == season_id]
        
        return sorted(episodes, key=lambda e: (
            self.seasons[e.season_id].season_number, 
            e.episode_number
        ))
    
    # ========================================================================
    # PLAYLIST MANAGEMENT
    # ========================================================================
    
    async def create_playlist(
        self,
        name: str,
        description: str,
        owner_id: str,
        is_public: bool = False
    ) -> Playlist:
        """Create a playlist."""
        playlist = Playlist(
            id=uuid4(),
            name=name,
            description=description,
            owner_id=owner_id,
            is_public=is_public,
            items=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.playlists[playlist.id] = playlist
        return playlist
    
    async def add_to_playlist(
        self,
        playlist_id: UUID,
        content_id: UUID,
        user_id: str
    ) -> Playlist:
        """Add content to playlist."""
        playlist = self.playlists.get(playlist_id)
        if not playlist:
            raise ValueError(f"Playlist {playlist_id} not found")
        
        if playlist.owner_id != user_id:
            raise ValueError("Only owner can modify playlist")
        
        if content_id not in playlist.items:
            playlist.items.append(content_id)
            playlist.updated_at = datetime.utcnow()
        
        return playlist
    
    async def remove_from_playlist(
        self,
        playlist_id: UUID,
        content_id: UUID,
        user_id: str
    ) -> Playlist:
        """Remove content from playlist."""
        playlist = self.playlists.get(playlist_id)
        if not playlist:
            raise ValueError(f"Playlist {playlist_id} not found")
        
        if playlist.owner_id != user_id:
            raise ValueError("Only owner can modify playlist")
        
        if content_id in playlist.items:
            playlist.items.remove(content_id)
            playlist.updated_at = datetime.utcnow()
        
        return playlist
    
    async def get_user_playlists(self, user_id: str) -> List[Playlist]:
        """
        Get user's playlists - ALPHABETICAL.
        
        RULE #5: Alphabetical, NOT by usage/popularity.
        """
        playlists = [p for p in self.playlists.values() if p.owner_id == user_id]
        return sorted(playlists, key=lambda p: p.name.lower())
    
    async def get_public_playlists(self) -> List[Playlist]:
        """Get public playlists - ALPHABETICAL."""
        playlists = [p for p in self.playlists.values() if p.is_public]
        return sorted(playlists, key=lambda p: p.name.lower())
    
    # ========================================================================
    # WATCH HISTORY
    # ========================================================================
    
    async def record_watch_progress(
        self,
        user_id: str,
        content_id: UUID,
        progress_seconds: int
    ) -> WatchHistory:
        """Record watch progress."""
        content = self.content.get(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")
        
        # Find existing history
        history = None
        for h in self.watch_history.values():
            if h.user_id == user_id and h.content_id == content_id:
                history = h
                break
        
        if history:
            # Update existing
            history.progress_seconds = progress_seconds
            history.last_watched = datetime.utcnow()
            
            # Check if completed (90% watched)
            if progress_seconds >= content.duration_seconds * 0.9:
                history.playback_status = PlaybackStatus.COMPLETED
                history.completed_at = datetime.utcnow()
            else:
                history.playback_status = PlaybackStatus.IN_PROGRESS
        else:
            # Create new
            status = PlaybackStatus.IN_PROGRESS
            completed_at = None
            if progress_seconds >= content.duration_seconds * 0.9:
                status = PlaybackStatus.COMPLETED
                completed_at = datetime.utcnow()
            
            history = WatchHistory(
                id=uuid4(),
                user_id=user_id,
                content_id=content_id,
                content_title=content.title,
                playback_status=status,
                progress_seconds=progress_seconds,
                duration_seconds=content.duration_seconds,
                started_at=datetime.utcnow(),
                last_watched=datetime.utcnow(),
                completed_at=completed_at
            )
            self.watch_history[history.id] = history
        
        # Increment view count
        content.view_count += 1
        
        return history
    
    async def get_watch_history(self, user_id: str) -> List[WatchHistory]:
        """
        Get user's watch history - CHRONOLOGICAL.
        
        RULE #5: By last watched time, NOT by frequency.
        """
        history = [h for h in self.watch_history.values() if h.user_id == user_id]
        return sorted(history, key=lambda h: h.last_watched, reverse=True)
    
    async def get_continue_watching(self, user_id: str) -> List[WatchHistory]:
        """
        Get in-progress content - CHRONOLOGICAL.
        """
        history = [h for h in self.watch_history.values() 
                  if h.user_id == user_id 
                  and h.playback_status == PlaybackStatus.IN_PROGRESS]
        return sorted(history, key=lambda h: h.last_watched, reverse=True)
    
    # ========================================================================
    # WATCHLIST
    # ========================================================================
    
    async def add_to_watchlist(
        self,
        user_id: str,
        content_id: UUID
    ) -> Watchlist:
        """Add content to user's watchlist."""
        if content_id not in self.content:
            raise ValueError(f"Content {content_id} not found")
        
        if user_id not in self.watchlists:
            self.watchlists[user_id] = Watchlist(
                id=uuid4(),
                user_id=user_id,
                content_ids=[],
                updated_at=datetime.utcnow()
            )
        
        watchlist = self.watchlists[user_id]
        if content_id not in watchlist.content_ids:
            watchlist.content_ids.append(content_id)
            watchlist.updated_at = datetime.utcnow()
        
        return watchlist
    
    async def remove_from_watchlist(
        self,
        user_id: str,
        content_id: UUID
    ) -> Watchlist:
        """Remove from watchlist."""
        if user_id not in self.watchlists:
            raise ValueError("Watchlist not found")
        
        watchlist = self.watchlists[user_id]
        if content_id in watchlist.content_ids:
            watchlist.content_ids.remove(content_id)
            watchlist.updated_at = datetime.utcnow()
        
        return watchlist
    
    async def get_watchlist(self, user_id: str) -> List[MediaContent]:
        """
        Get user's watchlist - CHRONOLOGICAL by added order.
        """
        if user_id not in self.watchlists:
            return []
        
        watchlist = self.watchlists[user_id]
        items = []
        for cid in watchlist.content_ids:
            if cid in self.content:
                items.append(self.content[cid])
        
        return items  # Maintain added order
    
    # ========================================================================
    # WATCH PARTIES
    # ========================================================================
    
    async def create_watch_party(
        self,
        host_id: str,
        content_id: UUID,
        scheduled_for: Optional[datetime] = None,
        max_participants: int = 10
    ) -> WatchParty:
        """Create a watch party."""
        content = self.content.get(content_id)
        if not content:
            raise ValueError(f"Content {content_id} not found")
        
        party = WatchParty(
            id=uuid4(),
            host_id=host_id,
            content_id=content_id,
            content_title=content.title,
            status=WatchPartyStatus.SCHEDULED if scheduled_for else WatchPartyStatus.LIVE,
            scheduled_for=scheduled_for,
            started_at=None if scheduled_for else datetime.utcnow(),
            ended_at=None,
            participants=[host_id],
            max_participants=max_participants,
            current_position_seconds=0,
            is_playing=False,
            created_at=datetime.utcnow()
        )
        
        self.watch_parties[party.id] = party
        return party
    
    async def join_watch_party(
        self,
        party_id: UUID,
        user_id: str
    ) -> WatchParty:
        """Join a watch party."""
        party = self.watch_parties.get(party_id)
        if not party:
            raise ValueError(f"Watch party {party_id} not found")
        
        if party.status not in [WatchPartyStatus.SCHEDULED, WatchPartyStatus.LIVE]:
            raise ValueError("Cannot join ended or cancelled party")
        
        if len(party.participants) >= party.max_participants:
            raise ValueError("Watch party is full")
        
        if user_id not in party.participants:
            party.participants.append(user_id)
        
        return party
    
    async def leave_watch_party(
        self,
        party_id: UUID,
        user_id: str
    ) -> WatchParty:
        """Leave watch party."""
        party = self.watch_parties.get(party_id)
        if not party:
            raise ValueError(f"Watch party {party_id} not found")
        
        if user_id in party.participants and user_id != party.host_id:
            party.participants.remove(user_id)
        
        return party
    
    async def control_watch_party(
        self,
        party_id: UUID,
        host_id: str,
        action: str,  # "play", "pause", "seek", "end"
        position_seconds: Optional[int] = None
    ) -> WatchParty:
        """Control watch party playback (host only)."""
        party = self.watch_parties.get(party_id)
        if not party:
            raise ValueError(f"Watch party {party_id} not found")
        
        if party.host_id != host_id:
            raise ValueError("Only host can control playback")
        
        if action == "play":
            party.is_playing = True
            if party.status == WatchPartyStatus.SCHEDULED:
                party.status = WatchPartyStatus.LIVE
                party.started_at = datetime.utcnow()
        elif action == "pause":
            party.is_playing = False
        elif action == "seek" and position_seconds is not None:
            party.current_position_seconds = position_seconds
        elif action == "end":
            party.status = WatchPartyStatus.ENDED
            party.ended_at = datetime.utcnow()
            party.is_playing = False
        
        return party
    
    async def get_active_watch_parties(self) -> List[WatchParty]:
        """Get active watch parties - CHRONOLOGICAL."""
        parties = [p for p in self.watch_parties.values() 
                  if p.status in [WatchPartyStatus.SCHEDULED, WatchPartyStatus.LIVE]]
        return sorted(parties, key=lambda p: p.created_at, reverse=True)
    
    # ========================================================================
    # REVIEWS & MODERATION
    # ========================================================================
    
    async def submit_review(
        self,
        content_id: UUID,
        user_id: str,
        user_name: str,
        rating: int,
        title: str,
        text: str
    ) -> Review:
        """
        Submit a review (requires moderation).
        
        GOVERNANCE: Reviews require moderation before publishing.
        """
        if content_id not in self.content:
            raise ValueError(f"Content {content_id} not found")
        
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be 1-5")
        
        review = Review(
            id=uuid4(),
            content_id=content_id,
            user_id=user_id,
            user_name=user_name,
            rating=rating,
            title=title,
            text=text,
            status=ContentStatus.UNDER_REVIEW,  # Requires moderation
            created_at=datetime.utcnow()
        )
        
        self.reviews[review.id] = review
        
        # Create moderation request
        mod_request = ModerationRequest(
            id=uuid4(),
            content_type="review",
            content_id=review.id,
            reason="New review submission",
            reported_by=user_id,
            status="pending",
            action=None,
            moderator_id=None,
            moderated_at=None,
            created_at=datetime.utcnow()
        )
        self.moderation_requests[mod_request.id] = mod_request
        
        return review
    
    async def moderate_review(
        self,
        review_id: UUID,
        action: ModerationAction,
        moderator_id: str
    ) -> Review:
        """
        Moderate a review.
        
        GOVERNANCE: Human approval required.
        """
        review = self.reviews.get(review_id)
        if not review:
            raise ValueError(f"Review {review_id} not found")
        
        if action == ModerationAction.APPROVE:
            review.status = ContentStatus.PUBLISHED
        elif action == ModerationAction.REJECT:
            review.status = ContentStatus.ARCHIVED
        elif action == ModerationAction.RESTRICT:
            review.status = ContentStatus.RESTRICTED
        
        review.moderated_by = moderator_id
        review.moderated_at = datetime.utcnow()
        
        return review
    
    async def get_content_reviews(
        self,
        content_id: UUID
    ) -> List[Review]:
        """
        Get reviews for content - CHRONOLOGICAL.
        
        RULE #5: NO sorting by helpfulness/upvotes.
        """
        reviews = [r for r in self.reviews.values() 
                  if r.content_id == content_id 
                  and r.status == ContentStatus.PUBLISHED]
        return sorted(reviews, key=lambda r: r.created_at, reverse=True)
    
    async def get_pending_moderation(self) -> List[ModerationRequest]:
        """Get pending moderation requests - CHRONOLOGICAL."""
        pending = [m for m in self.moderation_requests.values() 
                  if m.status == "pending"]
        return sorted(pending, key=lambda m: m.created_at)
    
    # ========================================================================
    # CHANNELS
    # ========================================================================
    
    async def create_channel(
        self,
        name: str,
        description: str,
        owner_id: str,
        thumbnail_url: Optional[str] = None
    ) -> Channel:
        """Create a content channel."""
        channel = Channel(
            id=uuid4(),
            name=name,
            description=description,
            owner_id=owner_id,
            thumbnail_url=thumbnail_url,
            subscriber_count=0,
            content_count=0,
            created_at=datetime.utcnow()
        )
        
        self.channels[channel.id] = channel
        return channel
    
    async def get_channels(self) -> List[Channel]:
        """
        Get channels - ALPHABETICAL.
        
        RULE #5: NOT by subscriber count.
        """
        return sorted(self.channels.values(), key=lambda c: c.name.lower())
    
    # ========================================================================
    # RECOMMENDATIONS (RULE #5 COMPLIANT)
    # ========================================================================
    
    async def get_recommendations(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[MediaContent]:
        """
        Get content recommendations - CHRONOLOGICAL (newest first).
        
        RULE #5: NO personalized engagement-based recommendations.
        Simply returns newest published content.
        """
        # Just return newest content - NO personalization
        published = [c for c in self.content.values() 
                    if c.status == ContentStatus.PUBLISHED]
        
        # CHRONOLOGICAL - newest first
        sorted_content = sorted(published, key=lambda c: c.created_at, reverse=True)
        return sorted_content[:limit]
    
    async def get_new_releases(
        self,
        media_type: Optional[MediaType] = None,
        limit: int = 20
    ) -> List[MediaContent]:
        """Get new releases - CHRONOLOGICAL by release date."""
        published = [c for c in self.content.values() 
                    if c.status == ContentStatus.PUBLISHED and c.release_date]
        
        if media_type:
            published = [c for c in published if c.media_type == media_type]
        
        # By release date
        sorted_content = sorted(published, key=lambda c: c.release_date, reverse=True)
        return sorted_content[:limit]
    
    async def get_genre_content(
        self,
        genre: str,
        limit: int = 20
    ) -> List[MediaContent]:
        """Get content by genre - CHRONOLOGICAL."""
        genre_lower = genre.lower()
        matching = [c for c in self.content.values() 
                   if c.status == ContentStatus.PUBLISHED
                   and any(g.lower() == genre_lower for g in c.genres)]
        
        # CHRONOLOGICAL
        return sorted(matching, key=lambda c: c.created_at, reverse=True)[:limit]
    
    # ========================================================================
    # ANALYTICS
    # ========================================================================
    
    async def get_library_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get library statistics."""
        published = [c for c in self.content.values() 
                    if c.status == ContentStatus.PUBLISHED]
        
        by_type = {}
        for content in published:
            t = content.media_type.value
            by_type[t] = by_type.get(t, 0) + 1
        
        genres = set()
        for content in published:
            genres.update(content.genres)
        
        return {
            "total_content": len(published),
            "by_type": by_type,
            "genres": sorted(list(genres)),  # Alphabetical
            "shows": len(self.shows),
            "episodes": len(self.episodes),
            "playlists": len(self.playlists),
            "channels": len(self.channels)
        }
    
    async def get_health(self) -> Dict[str, Any]:
        """Health check."""
        return {
            "status": "healthy",
            "service": "entertainment_agent",
            "version": "V68",
            "stats": {
                "content": len(self.content),
                "shows": len(self.shows),
                "playlists": len(self.playlists),
                "watch_parties": len([p for p in self.watch_parties.values() 
                                     if p.status == WatchPartyStatus.LIVE]),
                "pending_moderation": len([m for m in self.moderation_requests.values()
                                          if m.status == "pending"])
            },
            "timestamp": datetime.utcnow().isoformat()
        }


# Singleton
_agent_instance: Optional[EntertainmentAgent] = None


def get_entertainment_agent() -> EntertainmentAgent:
    """Get entertainment agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = EntertainmentAgent()
    return _agent_instance
