"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ / NOVA-999 — BACKEND FASTAPI PRODUCTION
═══════════════════════════════════════════════════════════════════════════════
[AQUA] + [ADAMAS] + SEQUENCE 3-6-9-12
Signal: 4.44s | Fréquence: 444Hz | Cube: 1728

✨ Code 741 activé au démarrage — Résolution instantanée des problèmes
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import asyncio
import json
import logging
from datetime import datetime
from typing import List, Dict, Set, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, select, text


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION (Variables d'environnement)
# ═══════════════════════════════════════════════════════════════════════════════

class Settings(BaseSettings):
    # Database
    database_url: str = ""
    
    # Server
    port: int = 8000
    host: str = "0.0.0.0"
    env: str = "production"
    debug: bool = False
    
    # CORS
    cors_origins: str = '["http://localhost:3000"]'
    
    # Resonance AT·OM
    signal_interval: float = 4.44
    anchor_frequency: int = 444
    cube_volume: int = 1728
    
    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"


settings = Settings()


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING avec Code 741
# ═══════════════════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("nova.main")


def log_startup_741():
    """Active le code 741 au démarrage pour résolution instantanée."""
    logger.info("═" * 70)
    logger.info("✨ [741] NOVA-999 / CHE·NU™ — DÉMARRAGE")
    logger.info("═" * 70)
    logger.info("   Code 741: Résolution Rapide de Problèmes — ACTIVÉ")
    logger.info(f"   Signal: {settings.signal_interval}s")
    logger.info(f"   Fréquence: {settings.anchor_frequency}Hz")
    logger.info(f"   Cube: {settings.cube_volume}")
    logger.info(f"   Environment: {settings.env}")
    logger.info("═" * 70)


# ═══════════════════════════════════════════════════════════════════════════════
# SÉQUENCES D'ACTIVATION NOVA-999
# ═══════════════════════════════════════════════════════════════════════════════

HARMONIC_SEQUENCES = [
    {"code": "781901942", "intent": "J'Harmonise notre passé", "frequency": 111, "category": "temporal"},
    {"code": "71042", "intent": "J'harmonise notre présent", "frequency": 444, "category": "temporal"},
    {"code": "14872191", "intent": "J'harmonise notre futur", "frequency": 777, "category": "temporal"},
    {"code": "8888848888819751", "intent": "Pour notre rétablissement", "frequency": 999, "category": "temporal"},
    {"code": "5487489", "intent": "Stabilité Infrastructure", "frequency": 528, "category": "infrastructure"},
    {"code": "9187758981818", "intent": "Protection Cybernétique", "frequency": 639, "category": "infrastructure"},
    {"code": "741", "intent": "Résolution Rapide", "frequency": 741, "category": "resolution"},
    {"code": "212309909", "intent": "Succès Entreprise", "frequency": 852, "category": "expansion"},
    {"code": "318798", "intent": "Abondance & Flux", "frequency": 888, "category": "expansion"},
    {"code": "1231115025", "intent": "Souveraineté Technologique", "frequency": 963, "category": "expansion"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE (SQLAlchemy Async)
# ═══════════════════════════════════════════════════════════════════════════════

engine = None
async_session_maker = None


class Base(DeclarativeBase):
    pass


class Agent(Base):
    """Modèle pour les 6500+ agents."""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), unique=True, index=True)
    name = Column(String(255), nullable=False)
    sphere_id = Column(Integer, index=True)
    level = Column(String(10), default="L3")
    status = Column(String(50), default="active")
    capabilities = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


async def init_database():
    """Initialise la connexion à la base de données."""
    global engine, async_session_maker
    
    if not settings.database_url:
        logger.warning("⚠️ DATABASE_URL non configuré — Mode sans DB")
        return
    
    try:
        engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True,
        )
        
        async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Test de connexion
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            logger.info("✅ Connexion PostgreSQL établie")
            
            # Compter les agents
            try:
                count_result = await conn.execute(text("SELECT COUNT(*) FROM agents"))
                count = count_result.scalar()
                logger.info(f"✅ {count} agents trouvés dans la base")
            except Exception:
                logger.info("ℹ️ Table agents non trouvée — sera créée au premier usage")
                
    except Exception as e:
        logger.error(f"❌ Erreur connexion DB: {e}")
        raise


async def get_db() -> AsyncSession:
    """Dependency pour obtenir une session DB."""
    if async_session_maker is None:
        raise HTTPException(status_code=503, detail="Database not available")
    
    async with async_session_maker() as session:
        yield session


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET MANAGER (Moteur de Résonance)
# ═══════════════════════════════════════════════════════════════════════════════

class ResonanceManager:
    """Gère les connexions WebSocket et la diffusion des séquences."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.tick_count: int = 0
        self.current_sequence_index: int = 0
        self.is_running: bool = False
        self._task: Optional[asyncio.Task] = None

    async def connect(self, websocket: WebSocket):
        """Accepte une nouvelle connexion WebSocket."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"♥ Client connecté — Total: {len(self.active_connections)}")
        
        # Envoyer message de bienvenue
        await websocket.send_json({
            "type": "connection_established",
            "message": "✨ [741] Connexion établie",
            "signal_interval": settings.signal_interval,
            "frequency": settings.anchor_frequency
        })

    def disconnect(self, websocket: WebSocket):
        """Déconnecte un client WebSocket."""
        self.active_connections.discard(websocket)
        logger.info(f"♥ Client déconnecté — Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Diffuse un message à tous les clients connectés."""
        if not self.active_connections:
            return
            
        dead_connections = set()
        
        for connection in self.active_connections.copy():
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.add(connection)
        
        # Nettoyer les connexions mortes
        self.active_connections -= dead_connections

    def _get_current_sequence(self) -> dict:
        """Retourne la séquence actuelle."""
        return HARMONIC_SEQUENCES[self.current_sequence_index]

    def _advance_sequence(self):
        """Avance à la séquence suivante."""
        self.current_sequence_index = (self.current_sequence_index + 1) % len(HARMONIC_SEQUENCES)

    async def _resonance_loop(self):
        """Boucle principale de résonance — diffuse toutes les 4.44s."""
        logger.info(f"♥ Moteur de Résonance démarré — Intervalle: {settings.signal_interval}s")
        
        while self.is_running:
            try:
                sequence = self._get_current_sequence()
                
                payload = {
                    "type": "resonance_pulse",
                    "timestamp": datetime.utcnow().isoformat(),
                    "tick": self.tick_count,
                    "signal": {
                        "interval": settings.signal_interval,
                        "frequency": settings.anchor_frequency,
                        "cube": settings.cube_volume
                    },
                    "harmonic": sequence,
                    "cycle": {
                        "position": self.current_sequence_index + 1,
                        "total": len(HARMONIC_SEQUENCES)
                    }
                }
                
                await self.broadcast(payload)
                
                logger.debug(f"♥ Tick {self.tick_count} | {sequence['code']} | {sequence['intent']}")
                
                self.tick_count += 1
                self._advance_sequence()
                
                await asyncio.sleep(settings.signal_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"♥ Erreur résonance: {e}")
                await asyncio.sleep(1)

    async def start(self):
        """Démarre le moteur de résonance."""
        if self.is_running:
            return
        self.is_running = True
        self._task = asyncio.create_task(self._resonance_loop())
        logger.info("✨ Moteur de Résonance ACTIVÉ")

    async def stop(self):
        """Arrête le moteur de résonance."""
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("♥ Moteur de Résonance ARRÊTÉ")

    def get_status(self) -> dict:
        """Retourne le statut du moteur."""
        return {
            "running": self.is_running,
            "tick_count": self.tick_count,
            "connected_clients": len(self.active_connections),
            "current_sequence": self._get_current_sequence(),
            "interval": settings.signal_interval,
            "frequency": settings.anchor_frequency
        }


# Instance globale
resonance_manager = ResonanceManager()


# ═══════════════════════════════════════════════════════════════════════════════
# LIFESPAN (Startup / Shutdown)
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application."""
    # Startup
    log_startup_741()
    await init_database()
    await resonance_manager.start()
    
    yield
    
    # Shutdown
    await resonance_manager.stop()
    if engine:
        await engine.dispose()
    logger.info("♥ NOVA-999 arrêté proprement")


# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION FASTAPI
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="NOVA-999 / CHE·NU™",
    description="Moteur de Résonance Harmonique — 6500+ Agents",
    version="999.0.0",
    lifespan=lifespan
)

# CORS
cors_origins = json.loads(settings.cors_origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS API
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "system": "NOVA-999 / CHE·NU™",
        "status": "active",
        "code": "741",
        "message": "✨ Résolution Rapide de Problèmes"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "signal": f"{settings.signal_interval}s",
        "frequency": f"{settings.anchor_frequency}Hz",
        "resonance": resonance_manager.get_status()
    }


@app.get("/api/v2/resonance/status")
async def resonance_status():
    """Statut du moteur de résonance."""
    return resonance_manager.get_status()


@app.get("/api/v2/resonance/sequences")
async def get_sequences():
    """Liste toutes les séquences d'activation."""
    return {
        "total": len(HARMONIC_SEQUENCES),
        "sequences": HARMONIC_SEQUENCES
    }


@app.get("/api/v2/agents")
async def get_agents(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Liste les agents (pagination)."""
    try:
        result = await db.execute(
            select(Agent).offset(skip).limit(limit)
        )
        agents = result.scalars().all()
        
        return {
            "total": len(agents),
            "skip": skip,
            "limit": limit,
            "agents": [
                {
                    "id": a.id,
                    "agent_id": a.agent_id,
                    "name": a.name,
                    "sphere_id": a.sphere_id,
                    "level": a.level,
                    "status": a.status
                }
                for a in agents
            ]
        }
    except Exception as e:
        logger.error(f"Erreur récupération agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v2/agents/count")
async def count_agents(db: AsyncSession = Depends(get_db)):
    """Compte le nombre total d'agents."""
    try:
        result = await db.execute(text("SELECT COUNT(*) FROM agents"))
        count = result.scalar()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET ENDPOINT
# ═══════════════════════════════════════════════════════════════════════════════

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket pour recevoir les pulsations de résonance.
    Signal toutes les 4.44 secondes.
    """
    await resonance_manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            if data == "ping":
                await websocket.send_text("pong")
            elif data == "status":
                await websocket.send_json(resonance_manager.get_status())
                
    except WebSocketDisconnect:
        resonance_manager.disconnect(websocket)


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
