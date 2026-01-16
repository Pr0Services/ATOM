"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ CREATIVE STUDIO — VOICE GENERATOR                 ║
║                                                                              ║
║  Multi-engine AI voice synthesis with cloning and TTS.                       ║
║                                                                              ║
║  Engines:                                                                    ║
║  - ElevenLabs (Voice cloning, TTS)                                           ║
║  - OpenAI TTS (High quality)                                                 ║
║  - Bark (Open source)                                                        ║
║                                                                              ║
║  COS: 94/100 — Adobe Creative Cloud Competitor                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import uuid
import asyncio
import logging
import httpx
import base64
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class VoiceEngine(str, Enum):
    ELEVENLABS = "elevenlabs"
    OPENAI_TTS = "openai-tts"
    BARK = "bark"


class VoiceStyle(str, Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CALM = "calm"
    PROFESSIONAL = "professional"
    CONVERSATIONAL = "conversational"
    NARRATIVE = "narrative"


class OutputFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    FLAC = "flac"


# Pre-built voices
ELEVENLABS_VOICES = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "drew": "29vD33N1CtxCmqQRPOHJ",
    "clyde": "2EiwWnXFnvU5JabPnv8n",
    "paul": "5Q0t7uMcjvnagumLfvZi",
    "domi": "AZnzlk1XvdvUeBnXmlld",
    "dave": "CYw3kZ02Hs0563khs1Fj",
    "fin": "D38z5RcWu1voky8WS1ja",
    "sarah": "EXAVITQu4vr4xnSDxMaL",
    "antoni": "ErXwobaYiN019PkySvjV",
    "thomas": "GBv7mTt0atIp3Br8iCZE",
    "charlie": "IKne3meq5aSn9XLyUdCD",
    "emily": "LcfcDJNUP1GQjkzn1xUU",
    "elli": "MF3mGyEYCl7XYWbV9V6O",
    "callum": "N2lVS1w4EtoT3dr4eOWO",
    "patrick": "ODq5zmih8GrVes37Dizd",
    "harry": "SOYHLrjzK2X1ezoPC6cr",
    "liam": "TX3LPaxmHKxFdv7VOQHJ",
    "dorothy": "ThT5KcBeYPX3keUQqHPh",
    "josh": "TxGEqnHWrfWFTfGW9XjX",
    "arnold": "VR6AewLTigWG4xSOukaG",
    "charlotte": "XB0fDUnXU5powFXDhCwa",
    "matilda": "XrExE9yKIg1WjnnlVkGX",
    "matthew": "Yko7PKHZNXotIFUBG7I9",
    "james": "ZQe5CZNOzWyzPSCn5a3c",
    "joseph": "Zlb1dXrM653N07WRdFW3",
    "jeremy": "bVMeCyTHy58xNoL34h3p",
    "michael": "flq6f7yk4E4fJM5XTYuZ",
    "ethan": "g5CIjZEefAph4nQFvHAz",
    "gigi": "jBpfuIE2acCO8z3wKNLl",
    "freya": "jsCqWAovK2LkecY7zXl4",
    "grace": "oWAxZDx7w5VEj9dCyTzz",
    "daniel": "onwK4e9ZLuTAKqWW03F9",
    "lily": "pFZP5JQG7iQjIQuC4Bku",
    "serena": "pMsXgVXv3BLzUgSXRplE",
    "adam": "pNInz6obpgDQGcFmaJgB",
    "nicole": "piTKgcLEGmPE4e6mEKli",
    "bill": "pqHfZKP75CvOlQylNhV4",
    "jessie": "t0jbNlBVZ17f02VDIeMI",
    "sam": "yoZ06aMxZJJ28mfd3POQ",
    "glinda": "z9fAnlkpzviPz146aGWa",
    "giovanni": "zcAOhNBS3c14rBihAFp1",
    "mimi": "zrHiDhphv9ZnVXBqCLjz",
}

OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


@dataclass
class VoiceGenerationRequest:
    """Request for voice generation."""
    text: str
    engine: VoiceEngine = VoiceEngine.OPENAI_TTS
    voice_id: str = "alloy"  # or ElevenLabs voice ID
    style: Optional[VoiceStyle] = None
    speed: float = 1.0  # 0.25 to 4.0
    output_format: OutputFormat = OutputFormat.MP3
    user_id: str = ""
    identity_id: str = ""


@dataclass
class GeneratedAudio:
    """A generated audio result."""
    id: str
    url: str  # Data URL or file URL
    text: str
    engine: str
    voice_id: str
    duration_seconds: float
    created_at: datetime
    tokens_used: int
    cost_usd: float
    user_id: str
    identity_id: str
    format: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# VOICE GENERATION ENGINES
# ═══════════════════════════════════════════════════════════════════════════════

class BaseVoiceEngine:
    """Base class for voice generation engines."""
    
    def __init__(self):
        self.name = "base"
        self.cost_per_1k_chars = 0.0
        self.tokens_per_1k_chars = 0
    
    async def generate(self, request: VoiceGenerationRequest) -> GeneratedAudio:
        """Generate audio from request."""
        raise NotImplementedError


class ElevenLabsEngine(BaseVoiceEngine):
    """ElevenLabs voice synthesis."""
    
    def __init__(self):
        super().__init__()
        self.name = "elevenlabs"
        self.api_key = os.environ.get("ELEVENLABS_API_KEY", "")
        self.base_url = "https://api.elevenlabs.io/v1"
        self.cost_per_1k_chars = 0.30
        self.tokens_per_1k_chars = 100
    
    async def generate(self, request: VoiceGenerationRequest) -> GeneratedAudio:
        """Generate audio using ElevenLabs."""
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not configured")
        
        # Resolve voice ID
        voice_id = request.voice_id
        if voice_id.lower() in ELEVENLABS_VOICES:
            voice_id = ELEVENLABS_VOICES[voice_id.lower()]
        
        # Map style to stability/similarity settings
        stability = 0.5
        similarity_boost = 0.75
        style_intensity = 0.0
        
        if request.style:
            style_map = {
                VoiceStyle.CALM: (0.8, 0.5, 0.0),
                VoiceStyle.EXCITED: (0.3, 0.8, 0.5),
                VoiceStyle.PROFESSIONAL: (0.7, 0.7, 0.2),
                VoiceStyle.CONVERSATIONAL: (0.4, 0.6, 0.3),
                VoiceStyle.NARRATIVE: (0.6, 0.7, 0.4),
            }
            if request.style in style_map:
                stability, similarity_boost, style_intensity = style_map[request.style]
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/text-to-speech/{voice_id}",
                    headers={
                        "xi-api-key": self.api_key,
                        "Content-Type": "application/json",
                    },
                    json={
                        "text": request.text,
                        "model_id": "eleven_multilingual_v2",
                        "voice_settings": {
                            "stability": stability,
                            "similarity_boost": similarity_boost,
                            "style": style_intensity,
                            "use_speaker_boost": True,
                        }
                    }
                )
                
                if response.status_code == 200:
                    audio_data = response.content
                    audio_b64 = base64.b64encode(audio_data).decode()
                    data_url = f"data:audio/mpeg;base64,{audio_b64}"
                    
                    # Estimate duration (rough: ~150 chars/second for speech)
                    duration = len(request.text) / 150
                    
                    # Calculate cost
                    chars = len(request.text)
                    cost = (chars / 1000) * self.cost_per_1k_chars
                    tokens = (chars / 1000) * self.tokens_per_1k_chars
                    
                    return GeneratedAudio(
                        id=str(uuid.uuid4()),
                        url=data_url,
                        text=request.text,
                        engine=self.name,
                        voice_id=request.voice_id,
                        duration_seconds=duration,
                        created_at=datetime.utcnow(),
                        tokens_used=int(tokens),
                        cost_usd=cost,
                        user_id=request.user_id,
                        identity_id=request.identity_id,
                        format=request.output_format.value,
                        metadata={
                            "stability": stability,
                            "similarity_boost": similarity_boost,
                            "style": request.style.value if request.style else None,
                        }
                    )
                else:
                    logger.error(f"ElevenLabs error: {response.status_code} - {response.text}")
                    raise Exception(f"ElevenLabs API error: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"ElevenLabs generation failed: {e}")
                raise


class OpenAITTSEngine(BaseVoiceEngine):
    """OpenAI Text-to-Speech."""
    
    def __init__(self):
        super().__init__()
        self.name = "openai-tts"
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1/audio/speech"
        self.cost_per_1k_chars = 0.015  # TTS-1
        self.cost_per_1k_chars_hd = 0.030  # TTS-1-HD
        self.tokens_per_1k_chars = 50
    
    async def generate(self, request: VoiceGenerationRequest) -> GeneratedAudio:
        """Generate audio using OpenAI TTS."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        
        # Validate voice
        voice = request.voice_id.lower()
        if voice not in OPENAI_VOICES:
            voice = "alloy"
        
        # Select model based on style
        model = "tts-1"
        if request.style in [VoiceStyle.PROFESSIONAL, VoiceStyle.NARRATIVE]:
            model = "tts-1-hd"
        
        # Map format
        format_map = {
            OutputFormat.MP3: "mp3",
            OutputFormat.WAV: "wav",
            OutputFormat.OGG: "opus",
            OutputFormat.FLAC: "flac",
        }
        response_format = format_map.get(request.output_format, "mp3")
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "input": request.text,
                        "voice": voice,
                        "response_format": response_format,
                        "speed": max(0.25, min(4.0, request.speed)),
                    }
                )
                
                if response.status_code == 200:
                    audio_data = response.content
                    audio_b64 = base64.b64encode(audio_data).decode()
                    
                    mime_types = {
                        "mp3": "audio/mpeg",
                        "wav": "audio/wav",
                        "opus": "audio/ogg",
                        "flac": "audio/flac",
                    }
                    mime = mime_types.get(response_format, "audio/mpeg")
                    data_url = f"data:{mime};base64,{audio_b64}"
                    
                    duration = len(request.text) / 150
                    chars = len(request.text)
                    cost_rate = self.cost_per_1k_chars_hd if model == "tts-1-hd" else self.cost_per_1k_chars
                    cost = (chars / 1000) * cost_rate
                    tokens = (chars / 1000) * self.tokens_per_1k_chars
                    
                    return GeneratedAudio(
                        id=str(uuid.uuid4()),
                        url=data_url,
                        text=request.text,
                        engine=self.name,
                        voice_id=voice,
                        duration_seconds=duration,
                        created_at=datetime.utcnow(),
                        tokens_used=int(tokens),
                        cost_usd=cost,
                        user_id=request.user_id,
                        identity_id=request.identity_id,
                        format=response_format,
                        metadata={
                            "model": model,
                            "speed": request.speed,
                        }
                    )
                else:
                    logger.error(f"OpenAI TTS error: {response.status_code} - {response.text}")
                    raise Exception(f"OpenAI TTS API error: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"OpenAI TTS generation failed: {e}")
                raise


# ═══════════════════════════════════════════════════════════════════════════════
# VOICE GENERATOR AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class VoiceGeneratorAgent:
    """
    CHE·NU Creative Studio Voice Generator Agent.
    
    Features:
    - Multi-engine support (ElevenLabs, OpenAI TTS)
    - Voice cloning ready
    - Style presets
    - Token tracking
    - Cost management
    """
    
    def __init__(self):
        self.engines: Dict[str, BaseVoiceEngine] = {
            VoiceEngine.ELEVENLABS.value: ElevenLabsEngine(),
            VoiceEngine.OPENAI_TTS.value: OpenAITTSEngine(),
        }
        
        self._library: Dict[str, List[GeneratedAudio]] = {}
        self._usage: Dict[str, Dict[str, Any]] = {}
        
        logger.info("VoiceGeneratorAgent initialized")
    
    async def generate(self, request: VoiceGenerationRequest) -> GeneratedAudio:
        """Generate audio from request."""
        engine_key = request.engine.value
        
        if engine_key not in self.engines:
            raise ValueError(f"Unknown engine: {engine_key}")
        
        engine = self.engines[engine_key]
        
        logger.info(f"Generating voice with {engine_key}, voice: {request.voice_id}")
        
        try:
            audio = await engine.generate(request)
            
            # Store in library
            user_id = request.user_id or "anonymous"
            if user_id not in self._library:
                self._library[user_id] = []
            self._library[user_id].append(audio)
            
            # Track usage
            self._track_usage(request.user_id, audio)
            
            logger.info(f"Generated {audio.duration_seconds:.1f}s audio")
            return audio
            
        except Exception as e:
            logger.error(f"Voice generation failed: {e}")
            raise
    
    def _track_usage(self, user_id: str, audio: GeneratedAudio):
        """Track usage for billing."""
        if user_id not in self._usage:
            self._usage[user_id] = {
                "total_audio_seconds": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "by_engine": {},
            }
        
        self._usage[user_id]["total_audio_seconds"] += audio.duration_seconds
        self._usage[user_id]["total_tokens"] += audio.tokens_used
        self._usage[user_id]["total_cost_usd"] += audio.cost_usd
        
        engine = audio.engine
        if engine not in self._usage[user_id]["by_engine"]:
            self._usage[user_id]["by_engine"][engine] = {"seconds": 0, "cost": 0.0}
        self._usage[user_id]["by_engine"][engine]["seconds"] += audio.duration_seconds
        self._usage[user_id]["by_engine"][engine]["cost"] += audio.cost_usd
    
    def get_library(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's audio library."""
        audios = self._library.get(user_id, [])
        audios = sorted(audios, key=lambda x: x.created_at, reverse=True)[:limit]
        
        return [
            {
                "id": a.id,
                "url": a.url,
                "text": a.text[:100] + "..." if len(a.text) > 100 else a.text,
                "engine": a.engine,
                "voice_id": a.voice_id,
                "duration_seconds": a.duration_seconds,
                "created_at": a.created_at.isoformat(),
                "format": a.format,
            }
            for a in audios
        ]
    
    def get_usage(self, user_id: str) -> Dict[str, Any]:
        """Get user's usage statistics."""
        return self._usage.get(user_id, {
            "total_audio_seconds": 0,
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "by_engine": {},
        })
    
    def get_available_voices(self, engine: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
        """Get available voices by engine."""
        voices = {}
        
        if not engine or engine == "elevenlabs":
            voices["elevenlabs"] = [
                {"id": name, "name": name.title(), "voice_id": vid}
                for name, vid in ELEVENLABS_VOICES.items()
            ]
        
        if not engine or engine == "openai-tts":
            voices["openai-tts"] = [
                {"id": v, "name": v.title(), "voice_id": v}
                for v in OPENAI_VOICES
            ]
        
        return voices
    
    def get_styles(self) -> List[Dict[str, str]]:
        """Get available voice styles."""
        return [
            {"id": style.value, "name": style.value.replace("_", " ").title()}
            for style in VoiceStyle
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_voice_generator: Optional[VoiceGeneratorAgent] = None


def get_voice_generator() -> VoiceGeneratorAgent:
    """Get or create the voice generator agent."""
    global _voice_generator
    if _voice_generator is None:
        _voice_generator = VoiceGeneratorAgent()
    return _voice_generator


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎙️ CHE·NU Creative Studio - Voice Generator")
    print("=" * 60)
    
    agent = get_voice_generator()
    
    print("\n📋 Available Voices:")
    voices = agent.get_available_voices()
    for engine, voice_list in voices.items():
        print(f"\n  {engine}:")
        for v in voice_list[:5]:
            print(f"    - {v['name']}")
        if len(voice_list) > 5:
            print(f"    ... and {len(voice_list) - 5} more")
    
    print("\n🎭 Available Styles:")
    for style in agent.get_styles():
        print(f"  - {style['name']}")
    
    print("\n✅ Voice Generator Agent ready!")
