"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ CREATIVE STUDIO — API ROUTES                      ║
║                                                                              ║
║  RESTful API for Creative Studio vertical.                                   ║
║                                                                              ║
║  Endpoints:                                                                  ║
║  - Image Generation (DALL-E 3, SD, Flux)                                     ║
║  - Voice Synthesis (ElevenLabs, OpenAI TTS)                                  ║
║  - Gallery & Library management                                              ║
║  - Usage tracking                                                            ║
║                                                                              ║
║  COS: 94/100 — Adobe Creative Cloud Competitor                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from .agents.image_generator import (
    get_image_generator,
    ImageGenerationRequest,
    ImageEngine,
    ImageSize,
    ImageStyle,
)
from .agents.voice_generator import (
    get_voice_generator,
    VoiceGenerationRequest,
    VoiceEngine,
    VoiceStyle,
    OutputFormat,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2/studio", tags=["Creative Studio"])


# ═══════════════════════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════════════════

# Image Generation
class ImageGenerateRequest(BaseModel):
    """Request to generate images."""
    prompt: str = Field(..., min_length=1, max_length=4000)
    engine: str = Field(default="dalle-3")
    size: str = Field(default="1024x1024")
    style: Optional[str] = None
    num_images: int = Field(default=1, ge=1, le=4)
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None


class ImageResponse(BaseModel):
    """Single image response."""
    id: str
    url: str
    prompt: str
    engine: str
    size: str
    style: Optional[str]
    created_at: str
    tokens_used: int
    cost_usd: float


class ImageGenerateResponse(BaseModel):
    """Response from image generation."""
    success: bool
    images: List[ImageResponse]
    total_tokens: int
    total_cost: float
    engine: str


# Voice Generation
class VoiceGenerateRequest(BaseModel):
    """Request to generate voice."""
    text: str = Field(..., min_length=1, max_length=5000)
    engine: str = Field(default="openai-tts")
    voice_id: str = Field(default="alloy")
    style: Optional[str] = None
    speed: float = Field(default=1.0, ge=0.25, le=4.0)
    output_format: str = Field(default="mp3")


class VoiceResponse(BaseModel):
    """Voice generation response."""
    success: bool
    id: str
    url: str
    text_preview: str
    engine: str
    voice_id: str
    duration_seconds: float
    tokens_used: int
    cost_usd: float
    format: str


# Gallery/Library
class GalleryResponse(BaseModel):
    """Gallery response."""
    items: List[Dict[str, Any]]
    total: int
    page: int
    per_page: int


class UsageResponse(BaseModel):
    """Usage statistics response."""
    images: Dict[str, Any]
    voice: Dict[str, Any]
    total_tokens: int
    total_cost_usd: float


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH & INFO ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Check Creative Studio health."""
    return {
        "status": "healthy",
        "service": "creative-studio",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/info")
async def get_studio_info() -> Dict[str, Any]:
    """Get Creative Studio information."""
    image_agent = get_image_generator()
    voice_agent = get_voice_generator()
    
    return {
        "name": "CHE·NU Creative Studio",
        "version": "1.0.0",
        "cos_score": 94,
        "description": "Multi-engine AI creative tools with governance",
        "capabilities": {
            "image_generation": {
                "engines": [e["id"] for e in image_agent.get_available_engines()],
                "styles": [s["id"] for s in image_agent.get_styles()],
                "sizes": [s["id"] for s in image_agent.get_sizes()],
            },
            "voice_synthesis": {
                "engines": ["elevenlabs", "openai-tts"],
                "styles": [s["id"] for s in voice_agent.get_styles()],
                "voices_count": sum(len(v) for v in voice_agent.get_available_voices().values()),
            },
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE GENERATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate/image", response_model=ImageGenerateResponse)
async def generate_image(
    request: ImageGenerateRequest,
    user_id: str = Query(default="anonymous"),
    identity_id: str = Query(default=""),
) -> ImageGenerateResponse:
    """
    Generate images using AI.
    
    Supported engines:
    - dalle-3: OpenAI DALL-E 3 (best quality, $0.04/image)
    - stable-diffusion: Stable Diffusion (fast, $0.002/image)
    - sdxl: Stable Diffusion XL (high quality, $0.002/image)
    - flux: Flux Schnell (fast, $0.003/image)
    - flux-pro: Flux Pro (highest quality, $0.05/image)
    """
    agent = get_image_generator()
    
    try:
        # Map string values to enums
        engine = ImageEngine(request.engine) if request.engine else ImageEngine.DALLE_3
        size = ImageSize(request.size) if request.size else ImageSize.SQUARE_1024
        style = ImageStyle(request.style) if request.style else None
        
        gen_request = ImageGenerationRequest(
            prompt=request.prompt,
            engine=engine,
            size=size,
            style=style,
            num_images=request.num_images,
            negative_prompt=request.negative_prompt,
            seed=request.seed,
            user_id=user_id,
            identity_id=identity_id,
        )
        
        images = await agent.generate(gen_request)
        
        return ImageGenerateResponse(
            success=True,
            images=[
                ImageResponse(
                    id=img.id,
                    url=img.url,
                    prompt=img.prompt,
                    engine=img.engine,
                    size=img.size,
                    style=img.style,
                    created_at=img.created_at.isoformat(),
                    tokens_used=img.tokens_used,
                    cost_usd=img.cost_usd,
                )
                for img in images
            ],
            total_tokens=sum(img.tokens_used for img in images),
            total_cost=sum(img.cost_usd for img in images),
            engine=request.engine,
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/image/engines")
async def get_image_engines() -> List[Dict[str, Any]]:
    """Get available image generation engines."""
    agent = get_image_generator()
    return agent.get_available_engines()


@router.get("/image/styles")
async def get_image_styles() -> List[Dict[str, str]]:
    """Get available image styles."""
    agent = get_image_generator()
    return agent.get_styles()


@router.get("/image/sizes")
async def get_image_sizes() -> List[Dict[str, str]]:
    """Get available image sizes."""
    agent = get_image_generator()
    return agent.get_sizes()


@router.get("/image/gallery")
async def get_image_gallery(
    user_id: str = Query(...),
    limit: int = Query(default=50, ge=1, le=100),
    page: int = Query(default=1, ge=1),
) -> GalleryResponse:
    """Get user's image gallery."""
    agent = get_image_generator()
    
    all_images = agent.get_gallery(user_id, limit=limit * page)
    start = (page - 1) * limit
    images = all_images[start:start + limit]
    
    return GalleryResponse(
        items=images,
        total=len(all_images),
        page=page,
        per_page=limit,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# VOICE GENERATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/generate/voice", response_model=VoiceResponse)
async def generate_voice(
    request: VoiceGenerateRequest,
    user_id: str = Query(default="anonymous"),
    identity_id: str = Query(default=""),
) -> VoiceResponse:
    """
    Generate voice audio using AI.
    
    Supported engines:
    - elevenlabs: ElevenLabs (highest quality, voice cloning)
    - openai-tts: OpenAI TTS (fast, affordable)
    """
    agent = get_voice_generator()
    
    try:
        engine = VoiceEngine(request.engine) if request.engine else VoiceEngine.OPENAI_TTS
        style = VoiceStyle(request.style) if request.style else None
        output_format = OutputFormat(request.output_format) if request.output_format else OutputFormat.MP3
        
        gen_request = VoiceGenerationRequest(
            text=request.text,
            engine=engine,
            voice_id=request.voice_id,
            style=style,
            speed=request.speed,
            output_format=output_format,
            user_id=user_id,
            identity_id=identity_id,
        )
        
        audio = await agent.generate(gen_request)
        
        return VoiceResponse(
            success=True,
            id=audio.id,
            url=audio.url,
            text_preview=audio.text[:100] + "..." if len(audio.text) > 100 else audio.text,
            engine=audio.engine,
            voice_id=audio.voice_id,
            duration_seconds=audio.duration_seconds,
            tokens_used=audio.tokens_used,
            cost_usd=audio.cost_usd,
            format=audio.format,
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Voice generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.get("/voice/engines")
async def get_voice_engines() -> List[Dict[str, Any]]:
    """Get available voice engines."""
    return [
        {
            "id": "elevenlabs",
            "name": "ElevenLabs",
            "description": "Highest quality, voice cloning support",
            "cost_per_1k_chars": 0.30,
            "features": ["voice_cloning", "multilingual", "emotion_control"],
        },
        {
            "id": "openai-tts",
            "name": "OpenAI TTS",
            "description": "Fast and affordable",
            "cost_per_1k_chars": 0.015,
            "features": ["speed_control", "multiple_formats"],
        },
    ]


@router.get("/voice/voices")
async def get_voices(
    engine: Optional[str] = Query(default=None),
) -> Dict[str, List[Dict[str, str]]]:
    """Get available voices by engine."""
    agent = get_voice_generator()
    return agent.get_available_voices(engine)


@router.get("/voice/styles")
async def get_voice_styles() -> List[Dict[str, str]]:
    """Get available voice styles."""
    agent = get_voice_generator()
    return agent.get_styles()


@router.get("/voice/library")
async def get_voice_library(
    user_id: str = Query(...),
    limit: int = Query(default=50, ge=1, le=100),
    page: int = Query(default=1, ge=1),
) -> GalleryResponse:
    """Get user's voice library."""
    agent = get_voice_generator()
    
    all_audios = agent.get_library(user_id, limit=limit * page)
    start = (page - 1) * limit
    audios = all_audios[start:start + limit]
    
    return GalleryResponse(
        items=audios,
        total=len(all_audios),
        page=page,
        per_page=limit,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# USAGE & ANALYTICS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/usage")
async def get_usage(
    user_id: str = Query(...),
) -> UsageResponse:
    """Get user's usage statistics."""
    image_agent = get_image_generator()
    voice_agent = get_voice_generator()
    
    image_usage = image_agent.get_usage(user_id)
    voice_usage = voice_agent.get_usage(user_id)
    
    return UsageResponse(
        images=image_usage,
        voice=voice_usage,
        total_tokens=image_usage.get("total_tokens", 0) + voice_usage.get("total_tokens", 0),
        total_cost_usd=image_usage.get("total_cost_usd", 0) + voice_usage.get("total_cost_usd", 0),
    )


@router.get("/usage/breakdown")
async def get_usage_breakdown(
    user_id: str = Query(...),
) -> Dict[str, Any]:
    """Get detailed usage breakdown."""
    image_agent = get_image_generator()
    voice_agent = get_voice_generator()
    
    image_usage = image_agent.get_usage(user_id)
    voice_usage = voice_agent.get_usage(user_id)
    
    return {
        "user_id": user_id,
        "period": "all_time",
        "image_generation": {
            "total_images": image_usage.get("total_images", 0),
            "total_tokens": image_usage.get("total_tokens", 0),
            "total_cost_usd": image_usage.get("total_cost_usd", 0),
            "by_engine": image_usage.get("by_engine", {}),
        },
        "voice_synthesis": {
            "total_seconds": voice_usage.get("total_audio_seconds", 0),
            "total_tokens": voice_usage.get("total_tokens", 0),
            "total_cost_usd": voice_usage.get("total_cost_usd", 0),
            "by_engine": voice_usage.get("by_engine", {}),
        },
        "totals": {
            "tokens": image_usage.get("total_tokens", 0) + voice_usage.get("total_tokens", 0),
            "cost_usd": image_usage.get("total_cost_usd", 0) + voice_usage.get("total_cost_usd", 0),
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATES & PRESETS
# ═══════════════════════════════════════════════════════════════════════════════

PROMPT_TEMPLATES = [
    {
        "id": "product_photo",
        "name": "Product Photography",
        "category": "business",
        "prompt": "Professional product photography of {subject}, clean white background, studio lighting, high detail, commercial quality",
    },
    {
        "id": "social_media",
        "name": "Social Media Post",
        "category": "marketing",
        "prompt": "Eye-catching social media image of {subject}, vibrant colors, modern design, trending aesthetic",
    },
    {
        "id": "logo_concept",
        "name": "Logo Concept",
        "category": "branding",
        "prompt": "Minimalist logo design for {subject}, clean lines, professional, scalable, modern",
    },
    {
        "id": "portrait",
        "name": "Professional Portrait",
        "category": "photography",
        "prompt": "Professional portrait photograph, {subject}, studio lighting, shallow depth of field, high resolution",
    },
    {
        "id": "landscape",
        "name": "Scenic Landscape",
        "category": "art",
        "prompt": "Beautiful landscape photograph of {subject}, golden hour lighting, dramatic sky, high dynamic range",
    },
    {
        "id": "illustration",
        "name": "Digital Illustration",
        "category": "art",
        "prompt": "Digital illustration of {subject}, vibrant colors, detailed, trending on ArtStation",
    },
    {
        "id": "anime",
        "name": "Anime Style",
        "category": "art",
        "prompt": "Anime style illustration of {subject}, vibrant colors, detailed character design, studio quality",
    },
    {
        "id": "3d_render",
        "name": "3D Render",
        "category": "design",
        "prompt": "3D render of {subject}, Octane render, volumetric lighting, highly detailed, 8K",
    },
    {
        "id": "ui_mockup",
        "name": "UI Mockup",
        "category": "design",
        "prompt": "Modern UI design mockup for {subject}, clean interface, professional, Figma style",
    },
    {
        "id": "book_cover",
        "name": "Book Cover",
        "category": "publishing",
        "prompt": "Professional book cover design for {subject}, compelling, genre-appropriate, bestseller quality",
    },
]


@router.get("/templates")
async def get_templates(
    category: Optional[str] = Query(default=None),
) -> List[Dict[str, Any]]:
    """Get prompt templates."""
    templates = PROMPT_TEMPLATES
    
    if category:
        templates = [t for t in templates if t["category"] == category]
    
    return templates


@router.get("/templates/categories")
async def get_template_categories() -> List[str]:
    """Get template categories."""
    return list(set(t["category"] for t in PROMPT_TEMPLATES))


# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════════════════

__all__ = ["router"]
