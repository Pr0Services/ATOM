"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              CHE·NU™ CREATIVE STUDIO — BACKEND TESTS                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

# Import the modules
import sys
sys.path.insert(0, '/home/claude/CREATIVE_STUDIO_V68/backend/spheres/studio/agents')

from image_generator import (
    ImageGeneratorAgent,
    ImageGenerationRequest,
    ImageEngine,
    ImageSize,
    ImageStyle,
    PromptEnhancer,
    GeneratedImage,
    get_image_generator,
)

from voice_generator import (
    VoiceGeneratorAgent,
    VoiceGenerationRequest,
    VoiceEngine,
    VoiceStyle,
    OutputFormat,
    GeneratedAudio,
    get_voice_generator,
)


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE GENERATOR TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestPromptEnhancer:
    """Test prompt enhancement."""
    
    def test_enhance_with_style(self):
        """Test prompt enhancement with style."""
        prompt = "a cat"
        enhanced = PromptEnhancer.enhance(prompt, ImageStyle.PHOTOREALISTIC)
        
        assert "a cat" in enhanced
        assert "professional photography" in enhanced.lower() or "photorealistic" in enhanced.lower()
    
    def test_enhance_without_style(self):
        """Test prompt without style returns original."""
        prompt = "a dog running"
        enhanced = PromptEnhancer.enhance(prompt, None)
        
        assert enhanced == prompt
    
    def test_get_negative_prompt(self):
        """Test negative prompt generation."""
        neg = PromptEnhancer.get_negative_prompt(ImageStyle.PHOTOREALISTIC)
        
        assert "cartoon" in neg or "anime" in neg
    
    def test_get_default_negative_prompt(self):
        """Test default negative prompt."""
        neg = PromptEnhancer.get_negative_prompt(None)
        
        assert "blurry" in neg or "low quality" in neg


class TestImageGenerationRequest:
    """Test image generation request."""
    
    def test_default_values(self):
        """Test default values."""
        request = ImageGenerationRequest(prompt="test")
        
        assert request.engine == ImageEngine.DALLE_3
        assert request.size == ImageSize.SQUARE_1024
        assert request.num_images == 1
    
    def test_num_images_clamping(self):
        """Test num_images is clamped."""
        request = ImageGenerationRequest(prompt="test", num_images=10)
        assert request.num_images == 4
        
        request = ImageGenerationRequest(prompt="test", num_images=0)
        assert request.num_images == 1


class TestImageGeneratorAgent:
    """Test image generator agent."""
    
    def test_agent_initialization(self):
        """Test agent initializes with engines."""
        agent = ImageGeneratorAgent()
        
        assert "dalle-3" in agent.engines
        assert "stable-diffusion" in agent.engines
        assert "flux" in agent.engines
    
    def test_get_available_engines(self):
        """Test getting available engines."""
        agent = ImageGeneratorAgent()
        engines = agent.get_available_engines()
        
        assert len(engines) >= 4
        assert any(e["id"] == "dalle-3" for e in engines)
        assert all("cost_per_image" in e for e in engines)
    
    def test_get_styles(self):
        """Test getting styles."""
        agent = ImageGeneratorAgent()
        styles = agent.get_styles()
        
        assert len(styles) > 0
        assert any(s["id"] == "photorealistic" for s in styles)
    
    def test_get_sizes(self):
        """Test getting sizes."""
        agent = ImageGeneratorAgent()
        sizes = agent.get_sizes()
        
        assert len(sizes) > 0
        assert any(s["id"] == "1024x1024" for s in sizes)
        assert all("aspect" in s for s in sizes)
    
    def test_get_empty_gallery(self):
        """Test empty gallery."""
        agent = ImageGeneratorAgent()
        gallery = agent.get_gallery("new_user")
        
        assert gallery == []
    
    def test_get_empty_usage(self):
        """Test empty usage."""
        agent = ImageGeneratorAgent()
        usage = agent.get_usage("new_user")
        
        assert usage["total_images"] == 0
        assert usage["total_tokens"] == 0
        assert usage["total_cost_usd"] == 0.0
    
    def test_track_usage(self):
        """Test usage tracking."""
        agent = ImageGeneratorAgent()
        
        # Create mock image
        image = GeneratedImage(
            id="test-id",
            url="http://test.com/image.png",
            prompt="test",
            engine="dalle-3",
            size="1024x1024",
            style=None,
            created_at=datetime.utcnow(),
            tokens_used=1500,
            cost_usd=0.04,
            user_id="test_user",
            identity_id="test_identity",
        )
        
        agent._track_usage("test_user", [image])
        
        usage = agent.get_usage("test_user")
        assert usage["total_images"] == 1
        assert usage["total_tokens"] == 1500
        assert usage["total_cost_usd"] == 0.04


class TestImageGeneratorSingleton:
    """Test singleton pattern."""
    
    def test_singleton(self):
        """Test singleton returns same instance."""
        agent1 = get_image_generator()
        agent2 = get_image_generator()
        
        assert agent1 is agent2


# ═══════════════════════════════════════════════════════════════════════════════
# VOICE GENERATOR TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestVoiceGenerationRequest:
    """Test voice generation request."""
    
    def test_default_values(self):
        """Test default values."""
        request = VoiceGenerationRequest(text="test")
        
        assert request.engine == VoiceEngine.OPENAI_TTS
        assert request.voice_id == "alloy"
        assert request.speed == 1.0
        assert request.output_format == OutputFormat.MP3


class TestVoiceGeneratorAgent:
    """Test voice generator agent."""
    
    def test_agent_initialization(self):
        """Test agent initializes with engines."""
        agent = VoiceGeneratorAgent()
        
        assert "elevenlabs" in agent.engines
        assert "openai-tts" in agent.engines
    
    def test_get_available_voices(self):
        """Test getting available voices."""
        agent = VoiceGeneratorAgent()
        voices = agent.get_available_voices()
        
        assert "elevenlabs" in voices
        assert "openai-tts" in voices
        assert len(voices["elevenlabs"]) > 0
        assert len(voices["openai-tts"]) > 0
    
    def test_get_voices_by_engine(self):
        """Test getting voices for specific engine."""
        agent = VoiceGeneratorAgent()
        voices = agent.get_available_voices("openai-tts")
        
        assert "openai-tts" in voices
        assert "elevenlabs" not in voices
    
    def test_get_styles(self):
        """Test getting voice styles."""
        agent = VoiceGeneratorAgent()
        styles = agent.get_styles()
        
        assert len(styles) > 0
        assert any(s["id"] == "professional" for s in styles)
    
    def test_get_empty_library(self):
        """Test empty library."""
        agent = VoiceGeneratorAgent()
        library = agent.get_library("new_user")
        
        assert library == []
    
    def test_get_empty_usage(self):
        """Test empty usage."""
        agent = VoiceGeneratorAgent()
        usage = agent.get_usage("new_user")
        
        assert usage["total_audio_seconds"] == 0
        assert usage["total_tokens"] == 0
        assert usage["total_cost_usd"] == 0.0
    
    def test_track_usage(self):
        """Test usage tracking."""
        agent = VoiceGeneratorAgent()
        
        # Create mock audio
        audio = GeneratedAudio(
            id="test-id",
            url="data:audio/mpeg;base64,test",
            text="Hello world",
            engine="openai-tts",
            voice_id="alloy",
            duration_seconds=1.5,
            created_at=datetime.utcnow(),
            tokens_used=50,
            cost_usd=0.015,
            user_id="test_user",
            identity_id="test_identity",
            format="mp3",
        )
        
        agent._track_usage("test_user", audio)
        
        usage = agent.get_usage("test_user")
        assert usage["total_audio_seconds"] == 1.5
        assert usage["total_tokens"] == 50
        assert usage["total_cost_usd"] == 0.015


class TestVoiceGeneratorSingleton:
    """Test singleton pattern."""
    
    def test_singleton(self):
        """Test singleton returns same instance."""
        agent1 = get_voice_generator()
        agent2 = get_voice_generator()
        
        assert agent1 is agent2


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS (Mocked)
# ═══════════════════════════════════════════════════════════════════════════════

class TestImageGenerationIntegration:
    """Integration tests for image generation."""
    
    @pytest.mark.asyncio
    async def test_generate_with_mock(self):
        """Test image generation with mocked API."""
        agent = ImageGeneratorAgent()
        
        # Mock the DALL-E engine's generate method
        mock_image = GeneratedImage(
            id="test-id",
            url="http://test.com/image.png",
            prompt="test prompt",
            engine="dalle-3",
            size="1024x1024",
            style=None,
            created_at=datetime.utcnow(),
            tokens_used=1500,
            cost_usd=0.04,
            user_id="test_user",
            identity_id="test_identity",
        )
        
        with patch.object(agent.engines["dalle-3"], 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = [mock_image]
            
            request = ImageGenerationRequest(
                prompt="test prompt",
                engine=ImageEngine.DALLE_3,
                user_id="test_user",
            )
            
            images = await agent.generate(request)
            
            assert len(images) == 1
            assert images[0].prompt == "test prompt"
            assert images[0].engine == "dalle-3"


class TestVoiceGenerationIntegration:
    """Integration tests for voice generation."""
    
    @pytest.mark.asyncio
    async def test_generate_with_mock(self):
        """Test voice generation with mocked API."""
        agent = VoiceGeneratorAgent()
        
        # Mock audio result
        mock_audio = GeneratedAudio(
            id="test-id",
            url="data:audio/mpeg;base64,test",
            text="Hello world",
            engine="openai-tts",
            voice_id="alloy",
            duration_seconds=1.0,
            created_at=datetime.utcnow(),
            tokens_used=50,
            cost_usd=0.015,
            user_id="test_user",
            identity_id="test_identity",
            format="mp3",
        )
        
        with patch.object(agent.engines["openai-tts"], 'generate', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = mock_audio
            
            request = VoiceGenerationRequest(
                text="Hello world",
                engine=VoiceEngine.OPENAI_TTS,
                user_id="test_user",
            )
            
            audio = await agent.generate(request)
            
            assert audio.text == "Hello world"
            assert audio.engine == "openai-tts"


# ═══════════════════════════════════════════════════════════════════════════════
# RUN TESTS
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🧪 Running Creative Studio Tests...")
    print("=" * 60)
    
    # Run prompt enhancer tests
    print("\n📝 Testing PromptEnhancer...")
    test_enhancer = TestPromptEnhancer()
    test_enhancer.test_enhance_with_style()
    test_enhancer.test_enhance_without_style()
    test_enhancer.test_get_negative_prompt()
    test_enhancer.test_get_default_negative_prompt()
    print("  ✅ All PromptEnhancer tests passed")
    
    # Run image request tests
    print("\n🖼️ Testing ImageGenerationRequest...")
    test_request = TestImageGenerationRequest()
    test_request.test_default_values()
    test_request.test_num_images_clamping()
    print("  ✅ All ImageGenerationRequest tests passed")
    
    # Run image agent tests
    print("\n🤖 Testing ImageGeneratorAgent...")
    test_agent = TestImageGeneratorAgent()
    test_agent.test_agent_initialization()
    test_agent.test_get_available_engines()
    test_agent.test_get_styles()
    test_agent.test_get_sizes()
    test_agent.test_get_empty_gallery()
    test_agent.test_get_empty_usage()
    test_agent.test_track_usage()
    print("  ✅ All ImageGeneratorAgent tests passed")
    
    # Run voice request tests
    print("\n🎙️ Testing VoiceGenerationRequest...")
    test_voice_req = TestVoiceGenerationRequest()
    test_voice_req.test_default_values()
    print("  ✅ All VoiceGenerationRequest tests passed")
    
    # Run voice agent tests
    print("\n🤖 Testing VoiceGeneratorAgent...")
    test_voice_agent = TestVoiceGeneratorAgent()
    test_voice_agent.test_agent_initialization()
    test_voice_agent.test_get_available_voices()
    test_voice_agent.test_get_voices_by_engine()
    test_voice_agent.test_get_styles()
    test_voice_agent.test_get_empty_library()
    test_voice_agent.test_get_empty_usage()
    test_voice_agent.test_track_usage()
    print("  ✅ All VoiceGeneratorAgent tests passed")
    
    # Run singleton tests
    print("\n🔧 Testing Singletons...")
    TestImageGeneratorSingleton().test_singleton()
    TestVoiceGeneratorSingleton().test_singleton()
    print("  ✅ All Singleton tests passed")
    
    print("\n" + "=" * 60)
    print("✅ ALL CREATIVE STUDIO TESTS PASSED!")
    print("=" * 60)
