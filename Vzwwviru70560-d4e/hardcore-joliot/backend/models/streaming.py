"""
CHE·NU™ V75 Backend - Streaming Models

STREAMING SPHERE - Media & Entertainment Platform

Content types:
- Movies, Series, Episodes
- Podcasts, Audio Episodes
- Music, Albums, Tracks
- Live Streams
- Shorts/Clips
- User-generated content

@version 75.0.0
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, BigInteger, Float, ForeignKey, ARRAY, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from config.database import Base


# ============================================================================
# CONTENT TYPE ENUM
# ============================================================================

class ContentType:
    """Media content types."""
    MOVIE = "movie"
    SERIES = "series"
    EPISODE = "episode"
    PODCAST = "podcast"
    PODCAST_EPISODE = "podcast_episode"
    MUSIC_ALBUM = "music_album"
    MUSIC_TRACK = "music_track"
    LIVE_STREAM = "live_stream"
    SHORT = "short"
    CLIP = "clip"
    DOCUMENTARY = "documentary"
    AUDIOBOOK = "audiobook"


class ContentStatus:
    """Content status."""
    DRAFT = "draft"
    PROCESSING = "processing"
    PUBLISHED = "published"
    SCHEDULED = "scheduled"
    ARCHIVED = "archived"
    BLOCKED = "blocked"


# ============================================================================
# ASSOCIATION TABLES
# ============================================================================

# Content <-> Genre many-to-many
content_genres = Table(
    'content_genres',
    Base.metadata,
    Column('content_id', UUID(as_uuid=True), ForeignKey('media_content.id'), primary_key=True),
    Column('genre_id', UUID(as_uuid=True), ForeignKey('genres.id'), primary_key=True),
)

# Content <-> Tag many-to-many
content_tags = Table(
    'content_tags',
    Base.metadata,
    Column('content_id', UUID(as_uuid=True), ForeignKey('media_content.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True),
)

# Playlist <-> Content many-to-many
playlist_items = Table(
    'playlist_items',
    Base.metadata,
    Column('playlist_id', UUID(as_uuid=True), ForeignKey('playlists.id'), primary_key=True),
    Column('content_id', UUID(as_uuid=True), ForeignKey('media_content.id'), primary_key=True),
    Column('position', Integer, default=0),
    Column('added_at', DateTime(timezone=True), default=datetime.utcnow),
)


# ============================================================================
# MEDIA CONTENT (Base for all content)
# ============================================================================

class MediaContent(Base):
    """
    Base media content entity.
    
    Supports all content types: movies, series, podcasts, music, etc.
    """
    
    __tablename__ = "media_content"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic info
    title = Column(String(500), nullable=False)
    original_title = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    
    content_type = Column(String(50), nullable=False)  # movie, series, podcast, etc.
    status = Column(String(20), default=ContentStatus.DRAFT)
    
    # Ownership
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"), nullable=True)
    
    # For episodes/tracks - parent reference
    parent_id = Column(UUID(as_uuid=True), ForeignKey("media_content.id"), nullable=True)
    season_number = Column(Integer, nullable=True)
    episode_number = Column(Integer, nullable=True)
    track_number = Column(Integer, nullable=True)
    
    # Media info
    duration_seconds = Column(Integer, nullable=True)
    release_date = Column(DateTime(timezone=True), nullable=True)
    release_year = Column(Integer, nullable=True)
    
    # Files & streaming
    thumbnail_url = Column(Text, nullable=True)
    poster_url = Column(Text, nullable=True)
    banner_url = Column(Text, nullable=True)
    
    # Ratings
    rating = Column(Float, default=0.0)  # 0-10
    rating_count = Column(Integer, default=0)
    maturity_rating = Column(String(10), nullable=True)  # G, PG, PG-13, R, NC-17
    
    # Engagement
    view_count = Column(BigInteger, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    
    # External references
    imdb_id = Column(String(20), nullable=True)
    tmdb_id = Column(String(20), nullable=True)
    spotify_id = Column(String(50), nullable=True)
    youtube_id = Column(String(20), nullable=True)
    
    # Metadata
    language = Column(String(10), default="fr")
    country = Column(String(10), nullable=True)
    metadata = Column(JSONB, default={})
    
    # Scheduling
    publish_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", foreign_keys=[creator_id])
    channel = relationship("Channel", back_populates="content")
    parent = relationship("MediaContent", remote_side=[id], backref="children")
    genres = relationship("Genre", secondary=content_genres, back_populates="content")
    tags = relationship("Tag", secondary=content_tags, back_populates="content")
    streams = relationship("StreamSource", back_populates="content", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MediaContent {self.title} ({self.content_type})>"
    
    @property
    def is_published(self) -> bool:
        return self.status == ContentStatus.PUBLISHED
    
    @property
    def duration_formatted(self) -> str:
        """Format duration as HH:MM:SS."""
        if not self.duration_seconds:
            return "00:00"
        hours, remainder = divmod(self.duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"


# ============================================================================
# STREAM SOURCES
# ============================================================================

class StreamSource(Base):
    """
    Streaming source for content.
    
    Each content can have multiple sources (qualities, formats).
    """
    
    __tablename__ = "stream_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id = Column(UUID(as_uuid=True), ForeignKey("media_content.id", ondelete="CASCADE"), nullable=False, index=True)
    
    source_type = Column(String(20), nullable=False)  # hls, dash, mp4, mp3, webm
    quality = Column(String(20), nullable=True)  # 4k, 1080p, 720p, 480p, audio_high, audio_low
    
    url = Column(Text, nullable=False)
    cdn_url = Column(Text, nullable=True)
    
    bitrate = Column(Integer, nullable=True)  # kbps
    file_size = Column(BigInteger, nullable=True)
    
    # For adaptive streaming
    manifest_url = Column(Text, nullable=True)
    
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    content = relationship("MediaContent", back_populates="streams")
    
    def __repr__(self):
        return f"<StreamSource {self.quality} ({self.source_type})>"


# ============================================================================
# CHANNELS (Creators)
# ============================================================================

class Channel(Base):
    """
    Creator channel for content publishing.
    """
    
    __tablename__ = "channels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    name = Column(String(100), nullable=False)
    handle = Column(String(50), unique=True, nullable=False)  # @handle
    description = Column(Text, nullable=True)
    
    avatar_url = Column(Text, nullable=True)
    banner_url = Column(Text, nullable=True)
    
    channel_type = Column(String(50), default="general")  # general, podcast, music, education
    
    # Stats
    subscriber_count = Column(Integer, default=0)
    total_views = Column(BigInteger, default=0)
    content_count = Column(Integer, default=0)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Monetization
    is_monetized = Column(Boolean, default=False)
    monetization_tier = Column(String(20), nullable=True)
    
    # Social links
    social_links = Column(JSONB, default={})
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", backref="channels")
    content = relationship("MediaContent", back_populates="channel")
    
    def __repr__(self):
        return f"<Channel @{self.handle}>"


# ============================================================================
# GENRES & TAGS
# ============================================================================

class Genre(Base):
    """Content genre."""
    
    __tablename__ = "genres"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    parent_id = Column(UUID(as_uuid=True), ForeignKey("genres.id"), nullable=True)
    
    icon = Column(String(10), nullable=True)
    color = Column(String(7), nullable=True)
    
    # Relationships
    content = relationship("MediaContent", secondary=content_genres, back_populates="genres")
    parent = relationship("Genre", remote_side=[id], backref="children")
    
    def __repr__(self):
        return f"<Genre {self.name}>"


class Tag(Base):
    """Content tag for discovery."""
    
    __tablename__ = "tags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    
    usage_count = Column(Integer, default=0)
    
    # Relationships
    content = relationship("MediaContent", secondary=content_tags, back_populates="tags")
    
    def __repr__(self):
        return f"<Tag #{self.name}>"


# ============================================================================
# PLAYLISTS & COLLECTIONS
# ============================================================================

class Playlist(Base):
    """
    User playlist/collection.
    
    Types: watchlist, favorites, custom, queue
    """
    
    __tablename__ = "playlists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    playlist_type = Column(String(50), default="custom")  # watchlist, favorites, history, queue, custom
    
    thumbnail_url = Column(Text, nullable=True)
    
    is_public = Column(Boolean, default=False)
    is_system = Column(Boolean, default=False)  # For watchlist, history, etc.
    
    item_count = Column(Integer, default=0)
    total_duration = Column(Integer, default=0)  # seconds
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="playlists")
    items = relationship("MediaContent", secondary=playlist_items, backref="in_playlists")
    
    def __repr__(self):
        return f"<Playlist {self.name}>"


# ============================================================================
# WATCH PROGRESS
# ============================================================================

class WatchProgress(Base):
    """
    User's watch/listen progress for content.
    """
    
    __tablename__ = "watch_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    content_id = Column(UUID(as_uuid=True), ForeignKey("media_content.id", ondelete="CASCADE"), nullable=False, index=True)
    
    position_seconds = Column(Integer, default=0)
    duration_seconds = Column(Integer, nullable=True)
    
    progress_percent = Column(Float, default=0.0)  # 0-100
    
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    watch_count = Column(Integer, default=1)
    total_watch_time = Column(Integer, default=0)  # Total seconds watched
    
    last_watched_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="watch_progress")
    content = relationship("MediaContent", backref="progress")
    
    def __repr__(self):
        return f"<WatchProgress {self.progress_percent:.1f}%>"
    
    def update_progress(self, position: int, duration: int = None):
        """Update watch progress."""
        self.position_seconds = position
        if duration:
            self.duration_seconds = duration
            self.progress_percent = (position / duration) * 100
        
        self.last_watched_at = datetime.utcnow()
        
        # Mark as completed if near end (95%)
        if self.progress_percent >= 95:
            self.is_completed = True
            self.completed_at = datetime.utcnow()


# ============================================================================
# SUBSCRIPTIONS
# ============================================================================

class ChannelSubscription(Base):
    """
    User subscription to a channel.
    """
    
    __tablename__ = "channel_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id", ondelete="CASCADE"), nullable=False, index=True)
    
    notifications_enabled = Column(Boolean, default=True)
    notification_level = Column(String(20), default="all")  # all, highlights, none
    
    subscribed_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="subscriptions")
    channel = relationship("Channel", backref="subscribers")
    
    def __repr__(self):
        return f"<Subscription user={self.user_id} channel={self.channel_id}>"


# ============================================================================
# RATINGS & REVIEWS
# ============================================================================

class ContentRating(Base):
    """
    User rating for content.
    """
    
    __tablename__ = "content_ratings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    content_id = Column(UUID(as_uuid=True), ForeignKey("media_content.id", ondelete="CASCADE"), nullable=False, index=True)
    
    rating = Column(Float, nullable=False)  # 0-10
    review = Column(Text, nullable=True)
    
    is_spoiler = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="ratings")
    content = relationship("MediaContent", backref="ratings")
    
    def __repr__(self):
        return f"<Rating {self.rating}/10>"


# ============================================================================
# LIVE STREAMING
# ============================================================================

class LiveStream(Base):
    """
    Live streaming session.
    """
    
    __tablename__ = "live_streams"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("channels.id"), nullable=False, index=True)
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    status = Column(String(20), default="scheduled")  # scheduled, live, ended, cancelled
    
    stream_key = Column(String(100), nullable=True)
    rtmp_url = Column(Text, nullable=True)
    hls_url = Column(Text, nullable=True)
    
    thumbnail_url = Column(Text, nullable=True)
    
    scheduled_start = Column(DateTime(timezone=True), nullable=True)
    actual_start = Column(DateTime(timezone=True), nullable=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    
    # Stats
    peak_viewers = Column(Integer, default=0)
    current_viewers = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    
    # Recording
    is_recorded = Column(Boolean, default=True)
    recording_content_id = Column(UUID(as_uuid=True), ForeignKey("media_content.id"), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    
    # Relationships
    channel = relationship("Channel", backref="live_streams")
    recording = relationship("MediaContent", foreign_keys=[recording_content_id])
    
    def __repr__(self):
        return f"<LiveStream {self.title} ({self.status})>"


# ============================================================================
# SEED DATA
# ============================================================================

GENRE_SEED_DATA = [
    # Video genres
    {"name": "Action", "slug": "action", "icon": "💥"},
    {"name": "Comédie", "slug": "comedy", "icon": "😂"},
    {"name": "Drame", "slug": "drama", "icon": "🎭"},
    {"name": "Science-Fiction", "slug": "sci-fi", "icon": "🚀"},
    {"name": "Horreur", "slug": "horror", "icon": "👻"},
    {"name": "Romance", "slug": "romance", "icon": "💕"},
    {"name": "Documentaire", "slug": "documentary", "icon": "📹"},
    {"name": "Animation", "slug": "animation", "icon": "🎨"},
    {"name": "Thriller", "slug": "thriller", "icon": "😱"},
    {"name": "Fantaisie", "slug": "fantasy", "icon": "🧙"},
    # Music genres
    {"name": "Pop", "slug": "pop", "icon": "🎤"},
    {"name": "Rock", "slug": "rock", "icon": "🎸"},
    {"name": "Hip-Hop", "slug": "hip-hop", "icon": "🎧"},
    {"name": "Jazz", "slug": "jazz", "icon": "🎺"},
    {"name": "Classique", "slug": "classical", "icon": "🎻"},
    {"name": "Électronique", "slug": "electronic", "icon": "🎹"},
    # Podcast genres
    {"name": "True Crime", "slug": "true-crime", "icon": "🔍"},
    {"name": "Business", "slug": "business", "icon": "💼"},
    {"name": "Technologie", "slug": "technology", "icon": "💻"},
    {"name": "Santé", "slug": "health", "icon": "🏥"},
    {"name": "Éducation", "slug": "education", "icon": "📚"},
]
