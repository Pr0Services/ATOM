# 🔌 CHE·NU™ THEME SYSTEM — COMPLETE API ROUTES
## FastAPI Backend Implementation

---

# 📁 STRUCTURE DES FICHIERS

```
backend/
├── api/
│   ├── __init__.py
│   ├── main.py
│   └── routes/
│       ├── __init__.py
│       ├── theme.py
│       ├── environment_3d.py
│       ├── assets.py
│       └── webhooks.py
├── services/
│   ├── __init__.py
│   ├── theme_service.py
│   ├── theme_resolver.py
│   ├── environment_3d_service.py
│   ├── asset_preloader.py
│   └── providers/
│       ├── __init__.py
│       ├── blockade_labs.py
│       ├── skybox_ai.py
│       └── custom_pipeline.py
├── models/
│   ├── __init__.py
│   ├── theme.py
│   ├── user_preferences.py
│   └── generation_job.py
├── schemas/
│   ├── __init__.py
│   ├── theme_schemas.py
│   └── generation_schemas.py
└── config/
    ├── __init__.py
    ├── settings.py
    └── providers.py
```

---

# 🚀 MAIN APPLICATION

```python
# backend/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.routes import theme, environment_3d, assets, webhooks
from config.settings import settings
from services.asset_preloader import AssetPreloader

# Lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize preloader
    app.state.asset_preloader = AssetPreloader()
    await app.state.asset_preloader.initialize()
    yield
    # Shutdown: Cleanup
    await app.state.asset_preloader.cleanup()

app = FastAPI(
    title="CHE·NU Theme API",
    description="API for theme management, 3D environment generation, and asset delivery",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(theme.router, prefix="/api/theme", tags=["Theme"])
app.include_router(environment_3d.router, prefix="/api/3d-gen", tags=["3D Generation"])
app.include_router(assets.router, prefix="/api/assets", tags=["Assets"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chenu-theme-api"}
```

---

# 🎨 THEME ROUTES

```python
# backend/api/routes/theme.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from database import get_db
from schemas.theme_schemas import (
    ThemeResponse,
    ThemeListResponse,
    UserThemeConfigResponse,
    SphereThemeConfigCreate,
    SphereThemeConfigUpdate,
    EntityThemeConfigCreate,
    ResolvedThemeResponse,
    PreloadManifestResponse
)
from services.theme_service import ThemeService
from services.theme_resolver import ThemeResolver

router = APIRouter()

# ═══════════════════════════════════════════════════════════════════
# THEME ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@router.get("/themes", response_model=ThemeListResponse)
async def get_all_themes(db: AsyncSession = Depends(get_db)):
    """
    Récupère tous les thèmes disponibles avec leurs assets
    """
    service = ThemeService(db)
    themes = await service.get_all_themes()
    return ThemeListResponse(
        themes=themes,
        count=len(themes)
    )

@router.get("/themes/{theme_id}", response_model=ThemeResponse)
async def get_theme(
    theme_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère un thème spécifique avec tous ses détails
    """
    service = ThemeService(db)
    theme = await service.get_theme(theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme

@router.get("/themes/{theme_id}/rooms")
async def get_theme_rooms(
    theme_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère toutes les pièces disponibles pour un thème
    """
    service = ThemeService(db)
    rooms = await service.get_theme_rooms(theme_id)
    return {"theme_id": theme_id, "rooms": rooms, "count": len(rooms)}

@router.get("/themes/{theme_id}/logos")
async def get_theme_logos(
    theme_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère toutes les variantes de logo pour un thème
    """
    service = ThemeService(db)
    logos = await service.get_theme_logos(theme_id)
    return {"theme_id": theme_id, "logos": logos}

# ═══════════════════════════════════════════════════════════════════
# USER CONFIGURATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@router.get("/user/{user_id}/config", response_model=UserThemeConfigResponse)
async def get_user_theme_config(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère la configuration complète des thèmes pour un utilisateur
    """
    service = ThemeService(db)
    config = await service.get_user_config(user_id)
    return config

@router.put("/user/{user_id}/default")
async def set_user_default_theme(
    user_id: UUID,
    theme_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Définit le thème par défaut de l'utilisateur
    """
    service = ThemeService(db)
    await service.set_default_theme(user_id, theme_id)
    return {"status": "ok", "default_theme_id": theme_id}

@router.put("/user/{user_id}/preferences")
async def update_user_preferences(
    user_id: UUID,
    enable_animations: Optional[bool] = None,
    enable_3d_environments: Optional[bool] = None,
    enable_ambient_sounds: Optional[bool] = None,
    reduce_motion: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour les préférences visuelles de l'utilisateur
    """
    service = ThemeService(db)
    await service.update_preferences(
        user_id,
        enable_animations=enable_animations,
        enable_3d_environments=enable_3d_environments,
        enable_ambient_sounds=enable_ambient_sounds,
        reduce_motion=reduce_motion
    )
    return {"status": "ok"}

# ═══════════════════════════════════════════════════════════════════
# SPHERE THEME CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

@router.get("/user/{user_id}/sphere/{sphere_id}")
async def get_sphere_theme_config(
    user_id: UUID,
    sphere_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère la configuration de thème pour une sphère spécifique
    """
    service = ThemeService(db)
    config = await service.get_sphere_config(user_id, sphere_id)
    return config

@router.put("/user/{user_id}/sphere/{sphere_id}")
async def set_sphere_theme_config(
    user_id: UUID,
    sphere_id: str,
    config: SphereThemeConfigUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Configure le thème pour une sphère spécifique
    """
    service = ThemeService(db)
    await service.set_sphere_config(user_id, sphere_id, config)
    return {"status": "ok", "sphere_id": sphere_id}

@router.delete("/user/{user_id}/sphere/{sphere_id}")
async def reset_sphere_theme_config(
    user_id: UUID,
    sphere_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Réinitialise la configuration d'une sphère (retour à l'héritage)
    """
    service = ThemeService(db)
    await service.reset_sphere_config(user_id, sphere_id)
    return {"status": "ok", "message": "Sphere config reset to inherit"}

# ═══════════════════════════════════════════════════════════════════
# ENTITY THEME CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

@router.get("/user/{user_id}/entity/{entity_id}")
async def get_entity_theme_config(
    user_id: UUID,
    entity_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère la configuration de thème pour une entité
    """
    service = ThemeService(db)
    config = await service.get_entity_config(user_id, entity_id)
    return config

@router.put("/user/{user_id}/entity/{entity_id}")
async def set_entity_theme_config(
    user_id: UUID,
    entity_id: UUID,
    config: EntityThemeConfigCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Configure le thème pour une entité spécifique
    """
    service = ThemeService(db)
    await service.set_entity_config(user_id, entity_id, config)
    return {"status": "ok", "entity_id": str(entity_id)}

# ═══════════════════════════════════════════════════════════════════
# THEME RESOLUTION
# ═══════════════════════════════════════════════════════════════════

@router.get("/resolve/{user_id}/{sphere_id}", response_model=ResolvedThemeResponse)
async def resolve_theme(
    user_id: UUID,
    sphere_id: str,
    entity_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Résout le thème effectif pour une sphère/entité
    Suit la chaîne d'héritage: Entity → Sphere → Default
    
    Retourne toutes les informations nécessaires pour l'affichage:
    - Thème et palette
    - URL de la pièce (2D et 3D)
    - URL du logo
    - Configuration du symbole
    """
    resolver = ThemeResolver(db, user_id)
    resolved = await resolver.resolve(sphere_id, entity_id)
    return resolved

@router.get("/resolve-batch/{user_id}")
async def resolve_themes_batch(
    user_id: UUID,
    sphere_ids: List[str] = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Résout les thèmes pour plusieurs sphères en une seule requête
    Optimisé pour le chargement initial
    """
    resolver = ThemeResolver(db, user_id)
    results = {}
    for sphere_id in sphere_ids:
        results[sphere_id] = await resolver.resolve(sphere_id)
    return {"user_id": str(user_id), "resolved": results}

# ═══════════════════════════════════════════════════════════════════
# PRELOAD MANIFEST
# ═══════════════════════════════════════════════════════════════════

@router.get("/preload-manifest/{user_id}", response_model=PreloadManifestResponse)
async def get_preload_manifest(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Génère le manifeste de préchargement pour optimiser les performances
    
    Retourne les assets à charger par priorité:
    - critical: Logos et assets de la sphère active
    - high: Logos de tous les thèmes
    - normal: Pièces des sphères configurées
    - low: Assets optionnels (3D, sons)
    """
    service = ThemeService(db)
    manifest = await service.generate_preload_manifest(user_id)
    return manifest

# ═══════════════════════════════════════════════════════════════════
# SPHERE SYMBOLS
# ═══════════════════════════════════════════════════════════════════

@router.get("/symbols")
async def get_all_sphere_symbols(db: AsyncSession = Depends(get_db)):
    """
    Récupère tous les symboles de sphères
    """
    service = ThemeService(db)
    symbols = await service.get_all_symbols()
    return {"symbols": symbols}

@router.get("/symbols/{sphere_id}")
async def get_sphere_symbol(
    sphere_id: str,
    theme_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère le symbole d'une sphère, optionnellement stylisé par thème
    """
    service = ThemeService(db)
    symbol = await service.get_symbol(sphere_id, theme_id)
    return symbol
```

---

# 🎮 3D GENERATION ROUTES

```python
# backend/api/routes/environment_3d.py

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID
from enum import Enum

from database import get_db
from schemas.generation_schemas import (
    GenerateEnvironmentRequest,
    GenerationJobResponse,
    JobStatusResponse,
    BatchGenerateRequest,
    BatchGenerateResponse
)
from services.environment_3d_service import Environment3DService

router = APIRouter()

class Provider(str, Enum):
    BLOCKADE_LABS = "blockade_labs"
    SKYBOX_AI = "skybox_ai"
    CUSTOM = "custom"

class Quality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"

# ═══════════════════════════════════════════════════════════════════
# GENERATION ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@router.post("/generate", response_model=GenerationJobResponse)
async def generate_environment(
    request: GenerateEnvironmentRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Démarre la génération d'un environnement 3D à partir d'une image 2D
    
    Providers supportés:
    - blockade_labs: Skybox AI de Blockade Labs
    - skybox_ai: Alternative Skybox
    - custom: Pipeline personnalisé (depth + panorama)
    
    Retourne un job_id pour suivre la progression
    """
    service = Environment3DService(db)
    job = await service.create_generation_job(request)
    
    # Lance la génération en arrière-plan
    background_tasks.add_task(
        service.process_job,
        job.id
    )
    
    return GenerationJobResponse(
        job_id=str(job.id),
        status="queued",
        provider=request.provider,
        estimated_time_seconds=service.estimate_time(request.quality)
    )

@router.get("/job/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère le statut d'un job de génération
    """
    service = Environment3DService(db)
    job = await service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(
        job_id=str(job.id),
        status=job.status,
        provider=job.provider,
        progress=job.progress if hasattr(job, 'progress') else None,
        result_url=job.result_url,
        error_message=job.error_message,
        created_at=job.created_at,
        completed_at=job.completed_at
    )

@router.delete("/job/{job_id}")
async def cancel_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Annule un job de génération en cours
    """
    service = Environment3DService(db)
    success = await service.cancel_job(job_id)
    
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel job")
    
    return {"status": "cancelled", "job_id": str(job_id)}

# ═══════════════════════════════════════════════════════════════════
# BATCH GENERATION
# ═══════════════════════════════════════════════════════════════════

@router.post("/batch-generate", response_model=BatchGenerateResponse)
async def batch_generate_theme_rooms(
    request: BatchGenerateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Génère les environnements 3D pour toutes les pièces d'un thème
    """
    service = Environment3DService(db)
    jobs = await service.batch_generate(
        theme_id=request.theme_id,
        quality=request.quality,
        provider=request.provider
    )
    
    for job in jobs:
        background_tasks.add_task(service.process_job, job.id)
    
    return BatchGenerateResponse(
        theme_id=request.theme_id,
        jobs_created=len(jobs),
        job_ids=[str(j.id) for j in jobs]
    )

@router.get("/theme/{theme_id}/status")
async def get_theme_generation_status(
    theme_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère le statut de génération 3D pour toutes les pièces d'un thème
    """
    service = Environment3DService(db)
    status = await service.get_theme_status(theme_id)
    return status

# ═══════════════════════════════════════════════════════════════════
# PROVIDERS INFO
# ═══════════════════════════════════════════════════════════════════

@router.get("/providers")
async def get_available_providers():
    """
    Liste les providers de génération 3D disponibles
    """
    return {
        "providers": [
            {
                "id": "blockade_labs",
                "name": "Blockade Labs Skybox",
                "description": "AI-powered 360° skybox generation",
                "formats": ["hdr", "jpg"],
                "quality_options": ["low", "medium", "high", "ultra"],
                "estimated_times": {"low": 30, "medium": 60, "high": 120, "ultra": 300}
            },
            {
                "id": "skybox_ai",
                "name": "Skybox AI",
                "description": "Alternative skybox generator",
                "formats": ["hdr", "exr"],
                "quality_options": ["medium", "high"],
                "estimated_times": {"medium": 45, "high": 90}
            },
            {
                "id": "custom",
                "name": "Custom Pipeline",
                "description": "Depth estimation + panorama generation",
                "formats": ["glb", "gltf"],
                "quality_options": ["medium", "high"],
                "estimated_times": {"medium": 120, "high": 240}
            }
        ]
    }

@router.get("/providers/{provider_id}/styles")
async def get_provider_styles(
    provider_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère les styles disponibles pour un provider
    """
    service = Environment3DService(db)
    styles = await service.get_provider_styles(provider_id)
    return {"provider": provider_id, "styles": styles}
```

---

# 📦 ASSETS ROUTES

```python
# backend/api/routes/assets.py

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
import aiofiles

from database import get_db
from services.asset_preloader import AssetPreloader
from config.settings import settings

router = APIRouter()

# ═══════════════════════════════════════════════════════════════════
# ASSET DELIVERY
# ═══════════════════════════════════════════════════════════════════

@router.get("/logo/{theme_id}")
async def get_theme_logo(
    theme_id: str,
    variant: str = "primary",
    format: str = "svg"
):
    """
    Récupère le logo pour un thème spécifique
    
    Variants: primary, icon, wordmark, animated
    Formats: svg, png, webp, lottie
    """
    # Redirect to CDN or serve from storage
    logo_url = f"{settings.CDN_URL}/logos/{theme_id}/{variant}.{format}"
    return RedirectResponse(url=logo_url, status_code=302)

@router.get("/room/{theme_id}/{variant_index}")
async def get_room_image(
    theme_id: str,
    variant_index: int,
    quality: str = "high"
):
    """
    Récupère l'image d'une pièce
    
    Quality: thumb, medium, high, original
    """
    room_url = f"{settings.CDN_URL}/rooms/{theme_id}/room_{variant_index:02d}_{quality}.jpg"
    return RedirectResponse(url=room_url, status_code=302)

@router.get("/environment/{theme_id}/{variant_index}")
async def get_3d_environment(
    theme_id: str,
    variant_index: int,
    format: str = "hdr"
):
    """
    Récupère l'environnement 3D d'une pièce
    
    Formats: hdr, exr, glb
    """
    env_url = f"{settings.CDN_URL}/environments/{theme_id}/env_{variant_index:02d}.{format}"
    return RedirectResponse(url=env_url, status_code=302)

@router.get("/symbol/{sphere_id}")
async def get_sphere_symbol(
    sphere_id: str,
    theme_id: Optional[str] = None,
    format: str = "svg"
):
    """
    Récupère le symbole d'une sphère
    """
    if theme_id:
        symbol_url = f"{settings.CDN_URL}/symbols/{sphere_id}/{theme_id}.{format}"
    else:
        symbol_url = f"{settings.CDN_URL}/symbols/{sphere_id}/default.{format}"
    return RedirectResponse(url=symbol_url, status_code=302)

@router.get("/map/{theme_id}")
async def get_theme_map(
    theme_id: str,
    quality: str = "high"
):
    """
    Récupère la map globale d'un thème
    """
    map_url = f"{settings.CDN_URL}/maps/{theme_id}/map_{quality}.jpg"
    return RedirectResponse(url=map_url, status_code=302)

# ═══════════════════════════════════════════════════════════════════
# CACHE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════

@router.get("/cache/status/{user_id}")
async def get_cache_status(
    user_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère le statut du cache d'assets pour un utilisateur
    """
    preloader: AssetPreloader = request.app.state.asset_preloader
    status = await preloader.get_user_cache_status(user_id)
    return status

@router.post("/cache/preload/{user_id}")
async def trigger_preload(
    user_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Déclenche le préchargement des assets pour un utilisateur
    """
    preloader: AssetPreloader = request.app.state.asset_preloader
    await preloader.preload_for_user(user_id)
    return {"status": "preloading", "user_id": str(user_id)}

@router.delete("/cache/{user_id}")
async def clear_user_cache(
    user_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Vide le cache d'assets pour un utilisateur
    """
    preloader: AssetPreloader = request.app.state.asset_preloader
    await preloader.clear_user_cache(user_id)
    return {"status": "cleared", "user_id": str(user_id)}
```

---

# 🔔 WEBHOOKS

```python
# backend/api/routes/webhooks.py

from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
import hmac
import hashlib

from database import get_db
from services.environment_3d_service import Environment3DService
from config.settings import settings

router = APIRouter()

# ═══════════════════════════════════════════════════════════════════
# PROVIDER WEBHOOKS
# ═══════════════════════════════════════════════════════════════════

@router.post("/blockade")
async def blockade_labs_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_webhook_signature: str = Header(None)
):
    """
    Webhook receiver pour Blockade Labs
    Appelé quand une génération de skybox est terminée
    """
    # Verify signature
    body = await request.body()
    if x_webhook_signature:
        expected_signature = hmac.new(
            settings.BLOCKADE_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(x_webhook_signature, expected_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    payload = await request.json()
    
    service = Environment3DService(db)
    await service.handle_blockade_webhook(payload)
    
    return {"status": "ok"}

@router.post("/skybox")
async def skybox_ai_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Webhook receiver pour Skybox AI
    """
    payload = await request.json()
    
    service = Environment3DService(db)
    await service.handle_skybox_webhook(payload)
    
    return {"status": "ok"}

@router.post("/custom-pipeline")
async def custom_pipeline_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_api_key: str = Header(...)
):
    """
    Webhook receiver pour le pipeline personnalisé
    """
    if x_api_key != settings.CUSTOM_PIPELINE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    payload = await request.json()
    
    service = Environment3DService(db)
    await service.handle_custom_webhook(payload)
    
    return {"status": "ok"}
```

---

# 📋 SCHEMAS

```python
# backend/schemas/theme_schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════
# THEME SCHEMAS
# ═══════════════════════════════════════════════════════════════════

class ThemePalette(BaseModel):
    primary: str
    secondary: str
    accent: str
    background: str
    surface: str
    text: str

class ThemeResponse(BaseModel):
    id: str
    name: str
    name_fr: str
    icon: str
    description: Optional[str]
    palette: ThemePalette
    logo_url: str
    logo_animated_url: Optional[str]
    map_image_url: str
    
    class Config:
        from_attributes = True

class ThemeListResponse(BaseModel):
    themes: List[ThemeResponse]
    count: int

# ═══════════════════════════════════════════════════════════════════
# USER CONFIG SCHEMAS
# ═══════════════════════════════════════════════════════════════════

class SymbolConfig(BaseModel):
    position: str = "top-right"
    size: str = "small"
    opacity: float = Field(default=0.7, ge=0.3, le=1.0)
    custom_symbol: Optional[str] = None

class SphereThemeConfigCreate(BaseModel):
    theme_id: Optional[str] = None  # null = inherit
    room_variant: int = 0
    symbol_config: SymbolConfig = SymbolConfig()

class SphereThemeConfigUpdate(BaseModel):
    theme_id: Optional[str] = None
    room_variant: Optional[int] = None
    symbol_config: Optional[SymbolConfig] = None

class EntityThemeConfigCreate(BaseModel):
    parent_sphere_id: str
    entity_name: str
    theme_id: Optional[str] = None
    room_variant: int = 0
    symbol_config: SymbolConfig = SymbolConfig()

class SphereConfigResponse(BaseModel):
    sphere_id: str
    theme_id: Optional[str]
    effective_theme_id: str  # After inheritance resolution
    room_variant: int
    symbol_position: str
    symbol_size: str
    symbol_opacity: float

class UserThemeConfigResponse(BaseModel):
    user_id: str
    default_theme_id: str
    enable_animations: bool
    enable_3d_environments: bool
    enable_ambient_sounds: bool
    reduce_motion: bool
    sphere_configs: Dict[str, SphereConfigResponse]
    entity_configs: Dict[str, Any]

# ═══════════════════════════════════════════════════════════════════
# RESOLVED THEME
# ═══════════════════════════════════════════════════════════════════

class ResolvedSymbol(BaseModel):
    char: str
    color: str
    effect: str
    position: str
    size: str
    opacity: float
    icon_url: Optional[str]

class ResolvedThemeResponse(BaseModel):
    theme_id: str
    theme: ThemeResponse
    room_image_url: str
    room_3d_url: Optional[str]
    logo_url: str
    symbol: ResolvedSymbol
    palette: ThemePalette

# ═══════════════════════════════════════════════════════════════════
# PRELOAD MANIFEST
# ═══════════════════════════════════════════════════════════════════

class PreloadAsset(BaseModel):
    type: str  # logo, room_2d, room_3d, symbol, map, sound
    url: str
    theme_id: Optional[str]
    sphere_id: Optional[str]
    size_bytes: Optional[int]

class PreloadManifestResponse(BaseModel):
    user_id: str
    generated_at: datetime
    critical: List[PreloadAsset]  # Load immediately
    high: List[PreloadAsset]      # Load after critical
    normal: List[PreloadAsset]    # Load in background
    low: List[PreloadAsset]       # Load on demand
    total_size_bytes: int
```

---

# ✅ RÉSUMÉ API COMPLÈTE

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                       CHE·NU THEME API - ENDPOINTS                            ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   🎨 THEME MANAGEMENT                                                        ║
║   GET    /api/theme/themes                    → Liste tous les thèmes        ║
║   GET    /api/theme/themes/{id}               → Détails d'un thème           ║
║   GET    /api/theme/themes/{id}/rooms         → Pièces du thème              ║
║   GET    /api/theme/themes/{id}/logos         → Logos du thème               ║
║                                                                               ║
║   👤 USER CONFIGURATION                                                       ║
║   GET    /api/theme/user/{id}/config          → Config complète              ║
║   PUT    /api/theme/user/{id}/default         → Définir thème par défaut     ║
║   PUT    /api/theme/user/{id}/preferences     → Préférences visuelles        ║
║                                                                               ║
║   🔵 SPHERE CONFIGURATION                                                     ║
║   GET    /api/theme/user/{id}/sphere/{sid}    → Config sphère                ║
║   PUT    /api/theme/user/{id}/sphere/{sid}    → Modifier config sphère       ║
║   DELETE /api/theme/user/{id}/sphere/{sid}    → Reset config sphère          ║
║                                                                               ║
║   📦 ENTITY CONFIGURATION                                                     ║
║   GET    /api/theme/user/{id}/entity/{eid}    → Config entité                ║
║   PUT    /api/theme/user/{id}/entity/{eid}    → Modifier config entité       ║
║                                                                               ║
║   🎯 THEME RESOLUTION                                                         ║
║   GET    /api/theme/resolve/{uid}/{sid}       → Résoudre thème effectif      ║
║   GET    /api/theme/resolve-batch/{uid}       → Résoudre plusieurs           ║
║   GET    /api/theme/preload-manifest/{uid}    → Manifest préchargement       ║
║                                                                               ║
║   🔷 SYMBOLS                                                                  ║
║   GET    /api/theme/symbols                   → Tous les symboles            ║
║   GET    /api/theme/symbols/{sid}             → Symbole d'une sphère         ║
║                                                                               ║
║   🎮 3D GENERATION                                                            ║
║   POST   /api/3d-gen/generate                 → Démarrer génération          ║
║   GET    /api/3d-gen/job/{id}                 → Status d'un job              ║
║   DELETE /api/3d-gen/job/{id}                 → Annuler un job               ║
║   POST   /api/3d-gen/batch-generate           → Génération batch             ║
║   GET    /api/3d-gen/providers                → Liste providers              ║
║                                                                               ║
║   📦 ASSETS                                                                   ║
║   GET    /api/assets/logo/{theme}             → Logo d'un thème              ║
║   GET    /api/assets/room/{theme}/{variant}   → Image pièce                  ║
║   GET    /api/assets/environment/{t}/{v}      → Environnement 3D             ║
║   GET    /api/assets/symbol/{sphere}          → Symbole sphère               ║
║   GET    /api/assets/map/{theme}              → Map du thème                 ║
║                                                                               ║
║   🔔 WEBHOOKS                                                                 ║
║   POST   /api/webhooks/blockade               → Blockade Labs callback       ║
║   POST   /api/webhooks/skybox                 → Skybox AI callback           ║
║   POST   /api/webhooks/custom-pipeline        → Custom pipeline callback     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

*CHE·NU™ Theme API v1.0*
*Complete Backend Implementation*
