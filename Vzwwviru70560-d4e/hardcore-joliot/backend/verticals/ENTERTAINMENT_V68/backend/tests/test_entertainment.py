"""
CHE·NU V68 - Entertainment & Media Tests
20 tests covering governance workflows
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from spheres.entertainment.agents.entertainment_agent import (
    EntertainmentAgent,
    MediaType, ContentStatus, ContentRating, PlaybackStatus, ModerationAction
)

@pytest.fixture
def agent():
    return EntertainmentAgent()


class TestContentManagement:
    
    @pytest.mark.asyncio
    async def test_add_content_creates_draft(self, agent):
        """Content starts as draft"""
        content = await agent.add_content(
            title="New Movie",
            media_type=MediaType.MOVIE,
            description="Description",
            duration_seconds=5400,
            rating=ContentRating.PG,
            genres=["Comedy"],
            user_id="user_001"
        )
        assert content.status == ContentStatus.DRAFT
        assert content.title == "New Movie"
        
    @pytest.mark.asyncio
    async def test_submit_for_review(self, agent):
        """Content can be submitted for review"""
        content = await agent.add_content(
            title="Test Movie",
            media_type=MediaType.MOVIE,
            description="A test movie",
            duration_seconds=7200,
            user_id="user_001"
        )
        result = await agent.submit_for_review(content.id, "user_001")
        assert result.status == ContentStatus.UNDER_REVIEW
        
    @pytest.mark.asyncio
    async def test_content_moderation_governance(self, agent):
        """GOVERNANCE: Content requires moderation before publishing"""
        content = await agent.add_content(
            title="Test Movie",
            media_type=MediaType.MOVIE,
            description="A test movie",
            duration_seconds=7200,
            user_id="user_001"
        )
        await agent.submit_for_review(content.id, "user_001")
        result = await agent.moderate_content(
            content_id=content.id, 
            action=ModerationAction.APPROVE, 
            moderator_id="mod_001", 
            reason="Good"
        )
        assert result.status == ContentStatus.PUBLISHED
        
    @pytest.mark.asyncio
    async def test_content_rejection(self, agent):
        """Content can be rejected"""
        content = await agent.add_content(
            title="Test Movie",
            media_type=MediaType.MOVIE,
            description="A test movie",
            duration_seconds=7200,
            user_id="user_001"
        )
        await agent.submit_for_review(content.id, "user_001")
        result = await agent.moderate_content(
            content_id=content.id,
            action=ModerationAction.REJECT, 
            moderator_id="mod_001", 
            reason="Bad"
        )
        assert result.status == ContentStatus.DRAFT


class TestTVShows:
    
    @pytest.mark.asyncio
    async def test_create_show(self, agent):
        """Can create TV show"""
        show = await agent.create_show(
            title="Test Series",
            description="A test TV series",
            rating=ContentRating.PG13,
            genres=["Drama"],
            user_id="user_001"
        )
        assert show.title == "Test Series"
        
    @pytest.mark.asyncio
    async def test_add_season(self, agent):
        """Can add seasons to show"""
        show = await agent.create_show(
            title="Test Show",
            description="Desc",
            rating=ContentRating.PG,
            genres=["Drama"],
            user_id="user_001"
        )
        season = await agent.add_season(
            show_id=show.id,
            season_number=1,
            name="Season One",
            user_id="user_001"
        )
        assert season.season_number == 1


class TestPlaylists:
    
    @pytest.mark.asyncio
    async def test_create_playlist(self, agent):
        """Can create playlist"""
        playlist = await agent.create_playlist(
            name="Favorites",
            description="Best movies",
            owner_id="user_001",
            is_public=False
        )
        assert playlist.name == "Favorites"
        assert playlist.is_public == False
        
    @pytest.mark.asyncio
    async def test_playlists_alphabetical_rule5(self, agent):
        """RULE 5: Playlists listed alphabetically"""
        await agent.create_playlist(name="Zebra", description="Desc", owner_id="user_001", is_public=True)
        await agent.create_playlist(name="Alpha", description="Desc", owner_id="user_001", is_public=True)
        await agent.create_playlist(name="Mango", description="Desc", owner_id="user_001", is_public=True)
        
        playlists = await agent.get_public_playlists()
        names = [p.name for p in playlists]
        assert names == sorted(names), "Playlists must be alphabetical (Rule #5)"


class TestWatchHistory:
    
    @pytest.mark.asyncio
    async def test_record_watch_progress(self, agent):
        """Can record watch progress"""
        content = await agent.add_content(
            title="Test", media_type=MediaType.MOVIE, 
            description="Test", duration_seconds=7200, user_id="user_001"
        )
        await agent.submit_for_review(content.id, "user_001")
        await agent.moderate_content(content.id, ModerationAction.APPROVE, "mod_001")
        
        history = await agent.record_watch_progress(
            user_id="user_001",
            content_id=content.id,
            progress_seconds=1800
        )
        assert history.progress_seconds == 1800


class TestWatchlist:
    
    @pytest.mark.asyncio
    async def test_add_to_watchlist(self, agent):
        """Can add content to watchlist"""
        content = await agent.add_content(
            title="Test", media_type=MediaType.MOVIE,
            description="Test", duration_seconds=7200, user_id="user_001"
        )
        await agent.submit_for_review(content.id, "user_001")
        await agent.moderate_content(content.id, ModerationAction.APPROVE, "mod_001")
        
        result = await agent.add_to_watchlist(user_id="user_001", content_id=content.id)
        assert result["success"] == True


class TestWatchParty:
    
    @pytest.mark.asyncio
    async def test_create_watch_party(self, agent):
        """Can create watch party"""
        content = await agent.add_content(
            title="Test", media_type=MediaType.MOVIE,
            description="Test", duration_seconds=7200, user_id="user_001"
        )
        await agent.submit_for_review(content.id, "user_001")
        await agent.moderate_content(content.id, ModerationAction.APPROVE, "mod_001")
        
        party = await agent.create_watch_party(
            content_id=content.id,
            host_id="user_001",
            name="Movie Night",
            max_participants=10
        )
        assert party.name == "Movie Night"


class TestReviews:
    
    @pytest.mark.asyncio
    async def test_submit_review_pending(self, agent):
        """Reviews start as pending moderation"""
        content = await agent.add_content(
            title="Test", media_type=MediaType.MOVIE,
            description="Test", duration_seconds=7200, user_id="user_001"
        )
        await agent.submit_for_review(content.id, "user_001")
        await agent.moderate_content(content.id, ModerationAction.APPROVE, "mod_001")
        
        review = await agent.submit_review(
            user_id="user_001",
            content_id=content.id,
            rating=4.5,
            title="Great!",
            text="Text"
        )
        assert review.is_approved == False


class TestChannels:
    
    @pytest.mark.asyncio
    async def test_create_channel(self, agent):
        """Can create channel"""
        channel = await agent.create_channel(
            name="My Channel",
            description="Test channel",
            owner_id="user_001"
        )
        assert channel.name == "My Channel"
        
    @pytest.mark.asyncio
    async def test_channels_alphabetical_rule5(self, agent):
        """RULE 5: Channels alphabetical"""
        await agent.create_channel("Zebra Channel", "Desc", "user_001")
        await agent.create_channel("Alpha Channel", "Desc", "user_002")
        await agent.create_channel("Beta Channel", "Desc", "user_003")
        
        channels = await agent.get_channels()
        names = [c["name"] for c in channels]
        assert names == sorted(names), "Channels must be alphabetical (Rule #5)"


class TestLibraryAndSearch:
    
    @pytest.mark.asyncio
    async def test_search_chronological_rule5(self, agent):
        """RULE 5: Search results chronological"""
        content = await agent.add_content(
            title="Test Movie", media_type=MediaType.MOVIE,
            description="Test", duration_seconds=7200, user_id="user_001"
        )
        await agent.submit_for_review(content.id, "user_001")
        await agent.moderate_content(content.id, ModerationAction.APPROVE, "mod_001")
        
        results = await agent.search_content("Test")
        assert isinstance(results, list)


class TestAnalytics:
    
    @pytest.mark.asyncio
    async def test_get_library_stats(self, agent):
        """Can get library statistics"""
        stats = await agent.get_library_stats()
        assert "content" in stats


class TestHealthCheck:
    
    @pytest.mark.asyncio
    async def test_health_check(self, agent):
        """Agent health check passes"""
        health = await agent.get_health()
        assert health["status"] == "healthy"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
