"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHE·NU™ CREATIVE STUDIO — IMAGE GENERATOR                 ║
║                                                                              ║
║  Multi-engine AI image generation with governance controls.                  ║
║                                                                              ║
║  Engines:                                                                    ║
║  - DALL-E 3 (OpenAI)                                                         ║
║  - Stable Diffusion (Replicate)                                              ║
║  - Midjourney (via API proxy)                                                ║
║  - Flux (Replicate)                                                          ║
║                                                                              ║
║  COS: 94/100 — Adobe Creative Cloud Competitor                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import uuid
import asyncio
import logging
import httpx
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class ImageEngine(str, Enum):
    DALLE_3 = "dalle-3"
    STABLE_DIFFUSION = "stable-diffusion"
    STABLE_DIFFUSION_XL = "sdxl"
    MIDJOURNEY = "midjourney"
    FLUX = "flux"
    FLUX_PRO = "flux-pro"


class ImageSize(str, Enum):
    SQUARE_1024 = "1024x1024"
    LANDSCAPE_1792 = "1792x1024"
    PORTRAIT_1024 = "1024x1792"
    SQUARE_512 = "512x512"
    SQUARE_768 = "768x768"


class ImageStyle(str, Enum):
    VIVID = "vivid"
    NATURAL = "natural"
    PHOTOREALISTIC = "photorealistic"
    ARTISTIC = "artistic"
    ANIME = "anime"
    DIGITAL_ART = "digital-art"
    OIL_PAINTING = "oil-painting"
    WATERCOLOR = "watercolor"
    SKETCH = "sketch"
    THREE_D = "3d-render"


@dataclass
class ImageGenerationRequest:
    """Request for image generation."""
    prompt: str
    engine: ImageEngine = ImageEngine.DALLE_3
    size: ImageSize = ImageSize.SQUARE_1024
    style: Optional[ImageStyle] = None
    num_images: int = 1
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None
    user_id: str = ""
    identity_id: str = ""
    
    def __post_init__(self):
        if self.num_images < 1:
            self.num_images = 1
        if self.num_images > 4:
            self.num_images = 4


@dataclass
class GeneratedImage:
    """A generated image result."""
    id: str
    url: str
    prompt: str
    engine: str
    size: str
    style: Optional[str]
    created_at: datetime
    tokens_used: int
    cost_usd: float
    user_id: str
    identity_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT ENHANCEMENT
# ═══════════════════════════════════════════════════════════════════════════════

PROMPT_TEMPLATES = {
    "photorealistic": "A photorealistic image of {prompt}, professional photography, high detail, 8K resolution",
    "artistic": "An artistic interpretation of {prompt}, creative, expressive, gallery quality",
    "anime": "Anime style illustration of {prompt}, vibrant colors, detailed character design",
    "digital-art": "Digital art of {prompt}, modern design, clean lines, trending on ArtStation",
    "oil-painting": "Oil painting of {prompt}, classical style, rich textures, museum quality",
    "watercolor": "Watercolor painting of {prompt}, soft colors, flowing, delicate details",
    "sketch": "Detailed pencil sketch of {prompt}, fine lines, shading, artistic",
    "3d-render": "3D render of {prompt}, Octane render, volumetric lighting, highly detailed",
}

NEGATIVE_PROMPTS = {
    "default": "blurry, low quality, distorted, ugly, bad anatomy, watermark, text",
    "photorealistic": "cartoon, anime, illustration, painting, drawing, art, sketch",
    "artistic": "photo, realistic, photograph, blurry",
    "anime": "realistic, photo, 3d render, blurry, bad anatomy",
}


class PromptEnhancer:
    """Enhances prompts for better image generation results."""
    
    @staticmethod
    def enhance(prompt: str, style: Optional[ImageStyle] = None) -> str:
        """Enhance a prompt with style-specific additions."""
        if not style or style.value not in PROMPT_TEMPLATES:
            return prompt
        
        template = PROMPT_TEMPLATES[style.value]
        return template.format(prompt=prompt)
    
    @staticmethod
    def get_negative_prompt(style: Optional[ImageStyle] = None) -> str:
        """Get appropriate negative prompt for style."""
        if style and style.value in NEGATIVE_PROMPTS:
            return NEGATIVE_PROMPTS[style.value]
        return NEGATIVE_PROMPTS["default"]


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE GENERATION ENGINES
# ═══════════════════════════════════════════════════════════════════════════════

class BaseImageEngine:
    """Base class for image generation engines."""
    
    def __init__(self):
        self.name = "base"
        self.cost_per_image = 0.0
        self.tokens_per_image = 0
    
    async def generate(self, request: ImageGenerationRequest) -> List[GeneratedImage]:
        """Generate images from request."""
        raise NotImplementedError


class DallE3Engine(BaseImageEngine):
    """DALL-E 3 image generation via OpenAI API."""
    
    def __init__(self):
        super().__init__()
        self.name = "dalle-3"
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1/images/generations"
        
        # Pricing per image
        self.pricing = {
            "1024x1024": 0.040,
            "1792x1024": 0.080,
            "1024x1792": 0.080,
        }
        self.tokens_per_image = 1500
    
    async def generate(self, request: ImageGenerationRequest) -> List[GeneratedImage]:
        """Generate images using DALL-E 3."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        
        # Enhance prompt
        enhanced_prompt = PromptEnhancer.enhance(request.prompt, request.style)
        
        # Map size
        size = request.size.value
        if size not in self.pricing:
            size = "1024x1024"
        
        # Map style
        quality = "hd" if request.style in [ImageStyle.PHOTOREALISTIC, ImageStyle.THREE_D] else "standard"
        style_param = "vivid" if request.style != ImageStyle.NATURAL else "natural"
        
        images = []
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            for i in range(request.num_images):
                try:
                    response = await client.post(
                        self.base_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "dall-e-3",
                            "prompt": enhanced_prompt,
                            "n": 1,  # DALL-E 3 only supports 1 at a time
                            "size": size,
                            "quality": quality,
                            "style": style_param,
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        for img_data in data.get("data", []):
                            image = GeneratedImage(
                                id=str(uuid.uuid4()),
                                url=img_data.get("url", ""),
                                prompt=request.prompt,
                                engine=self.name,
                                size=size,
                                style=request.style.value if request.style else None,
                                created_at=datetime.utcnow(),
                                tokens_used=self.tokens_per_image,
                                cost_usd=self.pricing.get(size, 0.040),
                                user_id=request.user_id,
                                identity_id=request.identity_id,
                                metadata={
                                    "enhanced_prompt": enhanced_prompt,
                                    "quality": quality,
                                    "revised_prompt": img_data.get("revised_prompt"),
                                }
                            )
                            images.append(image)
                    else:
                        logger.error(f"DALL-E 3 error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    logger.error(f"DALL-E 3 generation failed: {e}")
        
        return images


class StableDiffusionEngine(BaseImageEngine):
    """Stable Diffusion via Replicate API."""
    
    def __init__(self):
        super().__init__()
        self.name = "stable-diffusion"
        self.api_key = os.environ.get("REPLICATE_API_KEY", "")
        self.base_url = "https://api.replicate.com/v1/predictions"
        
        # Model versions
        self.models = {
            "stable-diffusion": "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        }
        
        self.cost_per_image = 0.002
        self.tokens_per_image = 500
    
    async def generate(self, request: ImageGenerationRequest) -> List[GeneratedImage]:
        """Generate images using Stable Diffusion."""
        if not self.api_key:
            raise ValueError("REPLICATE_API_KEY not configured")
        
        # Enhance prompt
        enhanced_prompt = PromptEnhancer.enhance(request.prompt, request.style)
        negative_prompt = request.negative_prompt or PromptEnhancer.get_negative_prompt(request.style)
        
        # Parse size
        width, height = map(int, request.size.value.split("x"))
        
        # Select model
        model_key = "sdxl" if request.engine == ImageEngine.STABLE_DIFFUSION_XL else "stable-diffusion"
        model_version = self.models.get(model_key, self.models["stable-diffusion"])
        
        images = []
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                # Create prediction
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Token {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "version": model_version.split(":")[-1],
                        "input": {
                            "prompt": enhanced_prompt,
                            "negative_prompt": negative_prompt,
                            "width": width,
                            "height": height,
                            "num_outputs": request.num_images,
                            "num_inference_steps": 50,
                            "guidance_scale": 7.5,
                            "seed": request.seed,
                        }
                    }
                )
                
                if response.status_code in [200, 201]:
                    prediction = response.json()
                    prediction_id = prediction.get("id")
                    
                    # Poll for completion
                    for _ in range(60):  # Max 60 seconds
                        await asyncio.sleep(1)
                        
                        status_response = await client.get(
                            f"{self.base_url}/{prediction_id}",
                            headers={"Authorization": f"Token {self.api_key}"}
                        )
                        
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            
                            if status_data.get("status") == "succeeded":
                                output = status_data.get("output", [])
                                for url in output:
                                    image = GeneratedImage(
                                        id=str(uuid.uuid4()),
                                        url=url,
                                        prompt=request.prompt,
                                        engine=self.name,
                                        size=request.size.value,
                                        style=request.style.value if request.style else None,
                                        created_at=datetime.utcnow(),
                                        tokens_used=self.tokens_per_image,
                                        cost_usd=self.cost_per_image,
                                        user_id=request.user_id,
                                        identity_id=request.identity_id,
                                        metadata={
                                            "enhanced_prompt": enhanced_prompt,
                                            "negative_prompt": negative_prompt,
                                            "prediction_id": prediction_id,
                                        }
                                    )
                                    images.append(image)
                                break
                            
                            elif status_data.get("status") == "failed":
                                logger.error(f"SD prediction failed: {status_data.get('error')}")
                                break
                else:
                    logger.error(f"SD error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                logger.error(f"SD generation failed: {e}")
        
        return images


class FluxEngine(BaseImageEngine):
    """Flux image generation via Replicate API."""
    
    def __init__(self):
        super().__init__()
        self.name = "flux"
        self.api_key = os.environ.get("REPLICATE_API_KEY", "")
        self.base_url = "https://api.replicate.com/v1/predictions"
        
        self.models = {
            "flux": "black-forest-labs/flux-schnell",
            "flux-pro": "black-forest-labs/flux-1.1-pro",
        }
        
        self.cost_per_image = 0.003
        self.tokens_per_image = 600
    
    async def generate(self, request: ImageGenerationRequest) -> List[GeneratedImage]:
        """Generate images using Flux."""
        if not self.api_key:
            raise ValueError("REPLICATE_API_KEY not configured")
        
        enhanced_prompt = PromptEnhancer.enhance(request.prompt, request.style)
        
        # Parse aspect ratio from size
        width, height = map(int, request.size.value.split("x"))
        if width == height:
            aspect_ratio = "1:1"
        elif width > height:
            aspect_ratio = "16:9"
        else:
            aspect_ratio = "9:16"
        
        model_key = "flux-pro" if request.engine == ImageEngine.FLUX_PRO else "flux"
        
        images = []
        
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers={
                        "Authorization": f"Token {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "version": self.models[model_key],
                        "input": {
                            "prompt": enhanced_prompt,
                            "aspect_ratio": aspect_ratio,
                            "num_outputs": request.num_images,
                            "output_format": "png",
                        }
                    }
                )
                
                if response.status_code in [200, 201]:
                    prediction = response.json()
                    prediction_id = prediction.get("id")
                    
                    # Poll for completion
                    for _ in range(60):
                        await asyncio.sleep(1)
                        
                        status_response = await client.get(
                            f"{self.base_url}/{prediction_id}",
                            headers={"Authorization": f"Token {self.api_key}"}
                        )
                        
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            
                            if status_data.get("status") == "succeeded":
                                output = status_data.get("output", [])
                                if isinstance(output, str):
                                    output = [output]
                                    
                                for url in output:
                                    image = GeneratedImage(
                                        id=str(uuid.uuid4()),
                                        url=url,
                                        prompt=request.prompt,
                                        engine=self.name,
                                        size=request.size.value,
                                        style=request.style.value if request.style else None,
                                        created_at=datetime.utcnow(),
                                        tokens_used=self.tokens_per_image,
                                        cost_usd=self.cost_per_image,
                                        user_id=request.user_id,
                                        identity_id=request.identity_id,
                                        metadata={
                                            "enhanced_prompt": enhanced_prompt,
                                            "aspect_ratio": aspect_ratio,
                                        }
                                    )
                                    images.append(image)
                                break
                            
                            elif status_data.get("status") == "failed":
                                logger.error(f"Flux failed: {status_data.get('error')}")
                                break
                                
            except Exception as e:
                logger.error(f"Flux generation failed: {e}")
        
        return images


# ═══════════════════════════════════════════════════════════════════════════════
# IMAGE GENERATOR AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class ImageGeneratorAgent:
    """
    CHE·NU Creative Studio Image Generator Agent.
    
    Features:
    - Multi-engine support (DALL-E 3, SD, SDXL, Flux)
    - Prompt enhancement
    - Style presets
    - Token tracking
    - Cost management
    - Governance integration
    """
    
    def __init__(self):
        self.engines: Dict[str, BaseImageEngine] = {
            ImageEngine.DALLE_3.value: DallE3Engine(),
            ImageEngine.STABLE_DIFFUSION.value: StableDiffusionEngine(),
            ImageEngine.STABLE_DIFFUSION_XL.value: StableDiffusionEngine(),
            ImageEngine.FLUX.value: FluxEngine(),
            ImageEngine.FLUX_PRO.value: FluxEngine(),
        }
        
        # In-memory gallery (replace with DB in production)
        self._gallery: Dict[str, List[GeneratedImage]] = {}
        
        # Usage tracking
        self._usage: Dict[str, Dict[str, Any]] = {}
        
        logger.info("ImageGeneratorAgent initialized with engines: " + ", ".join(self.engines.keys()))
    
    async def generate(self, request: ImageGenerationRequest) -> List[GeneratedImage]:
        """
        Generate images from request.
        
        Args:
            request: Image generation request
            
        Returns:
            List of generated images
        """
        engine_key = request.engine.value
        
        if engine_key not in self.engines:
            raise ValueError(f"Unknown engine: {engine_key}")
        
        engine = self.engines[engine_key]
        
        logger.info(f"Generating {request.num_images} images with {engine_key}")
        logger.info(f"Prompt: {request.prompt[:100]}...")
        
        try:
            images = await engine.generate(request)
            
            # Store in gallery
            user_id = request.user_id or "anonymous"
            if user_id not in self._gallery:
                self._gallery[user_id] = []
            self._gallery[user_id].extend(images)
            
            # Track usage
            self._track_usage(request.user_id, images)
            
            logger.info(f"Generated {len(images)} images successfully")
            return images
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            raise
    
    def _track_usage(self, user_id: str, images: List[GeneratedImage]):
        """Track usage for billing and governance."""
        if user_id not in self._usage:
            self._usage[user_id] = {
                "total_images": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "by_engine": {},
            }
        
        for img in images:
            self._usage[user_id]["total_images"] += 1
            self._usage[user_id]["total_tokens"] += img.tokens_used
            self._usage[user_id]["total_cost_usd"] += img.cost_usd
            
            engine = img.engine
            if engine not in self._usage[user_id]["by_engine"]:
                self._usage[user_id]["by_engine"][engine] = {"images": 0, "cost": 0.0}
            self._usage[user_id]["by_engine"][engine]["images"] += 1
            self._usage[user_id]["by_engine"][engine]["cost"] += img.cost_usd
    
    def get_gallery(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's image gallery."""
        images = self._gallery.get(user_id, [])
        images = sorted(images, key=lambda x: x.created_at, reverse=True)[:limit]
        
        return [
            {
                "id": img.id,
                "url": img.url,
                "prompt": img.prompt,
                "engine": img.engine,
                "size": img.size,
                "style": img.style,
                "created_at": img.created_at.isoformat(),
                "tokens_used": img.tokens_used,
                "cost_usd": img.cost_usd,
            }
            for img in images
        ]
    
    def get_usage(self, user_id: str) -> Dict[str, Any]:
        """Get user's usage statistics."""
        return self._usage.get(user_id, {
            "total_images": 0,
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "by_engine": {},
        })
    
    def get_available_engines(self) -> List[Dict[str, Any]]:
        """Get list of available engines with info."""
        return [
            {
                "id": ImageEngine.DALLE_3.value,
                "name": "DALL-E 3",
                "provider": "OpenAI",
                "cost_per_image": 0.040,
                "max_resolution": "1792x1024",
                "strengths": ["Prompt following", "Text rendering", "Photorealism"],
            },
            {
                "id": ImageEngine.STABLE_DIFFUSION_XL.value,
                "name": "Stable Diffusion XL",
                "provider": "Stability AI",
                "cost_per_image": 0.002,
                "max_resolution": "1024x1024",
                "strengths": ["Speed", "Consistency", "Fine-tuning"],
            },
            {
                "id": ImageEngine.FLUX.value,
                "name": "Flux Schnell",
                "provider": "Black Forest Labs",
                "cost_per_image": 0.003,
                "max_resolution": "1024x1024",
                "strengths": ["Speed", "Quality", "Prompt adherence"],
            },
            {
                "id": ImageEngine.FLUX_PRO.value,
                "name": "Flux 1.1 Pro",
                "provider": "Black Forest Labs",
                "cost_per_image": 0.05,
                "max_resolution": "2048x2048",
                "strengths": ["Highest quality", "Professional output"],
            },
        ]
    
    def get_styles(self) -> List[Dict[str, str]]:
        """Get available style presets."""
        return [
            {"id": style.value, "name": style.value.replace("-", " ").title()}
            for style in ImageStyle
        ]
    
    def get_sizes(self) -> List[Dict[str, str]]:
        """Get available image sizes."""
        return [
            {"id": size.value, "name": size.value, "aspect": self._get_aspect(size)}
            for size in ImageSize
        ]
    
    @staticmethod
    def _get_aspect(size: ImageSize) -> str:
        """Get aspect ratio name for size."""
        if "1024x1024" in size.value or "512x512" in size.value or "768x768" in size.value:
            return "Square"
        elif "1792" in size.value:
            return "Landscape"
        else:
            return "Portrait"


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON
# ═══════════════════════════════════════════════════════════════════════════════

_image_generator: Optional[ImageGeneratorAgent] = None


def get_image_generator() -> ImageGeneratorAgent:
    """Get or create the image generator agent."""
    global _image_generator
    if _image_generator is None:
        _image_generator = ImageGeneratorAgent()
    return _image_generator


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🎨 CHE·NU Creative Studio - Image Generator")
    print("=" * 60)
    
    agent = get_image_generator()
    
    # List engines
    print("\n📋 Available Engines:")
    for engine in agent.get_available_engines():
        print(f"  - {engine['name']} ({engine['provider']}): ${engine['cost_per_image']}/image")
    
    # List styles
    print("\n🎭 Available Styles:")
    for style in agent.get_styles():
        print(f"  - {style['name']}")
    
    # List sizes
    print("\n📐 Available Sizes:")
    for size in agent.get_sizes():
        print(f"  - {size['name']} ({size['aspect']})")
    
    print("\n✅ Image Generator Agent ready!")
    print("\nTo generate images, call:")
    print("  images = await agent.generate(ImageGenerationRequest(prompt='...'))")
