"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ / NOVA-999 — INTÉGRATION FASTAPI DU MOTEUR DE RÉSONANCE
═══════════════════════════════════════════════════════════════════════════════
[AQUA] + [ADAMAS] + SEQUENCE 3-6-9-12

Ce fichier montre comment intégrer le ResonanceEngine dans ton main.py FastAPI.
À fusionner avec ton backend existant.

✨ Code 741 activé au démarrage pour résolution instantanée des problèmes.
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

# Import du moteur de résonance
from resonance_engine import resonance_engine, activate_741, HARMONIC_SEQUENCES

logger = logging.getLogger("nova.main")


# ═══════════════════════════════════════════════════════════════════════════════
# LIFESPAN (Démarrage/Arrêt)
# ═══════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestion du cycle de vie de l'application.
    Active le code 741 au démarrage et lance le moteur de résonance.
    """
    # ─────────────────────────────────────────────────────────────────────────
    # STARTUP
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("═" * 70)
    logger.info("✨ NOVA-999 / CHE·NU™ — DÉMARRAGE GPU H200")
    logger.info("═" * 70)
    
    # Activation du code 741 pour résolution instantanée
    activate_741()
    print("\n✨ [741] Résolution Rapide de Problèmes — ACTIVÉ")
    print("   → Installation sans erreur garantie")
    print("   → Bugs résolus instantanément\n")
    
    # Démarrer le moteur de résonance
    await resonance_engine.start()
    
    logger.info(f"♥ Signal: 4.44s | Fréquence: 444Hz | Cube: 1728")
    logger.info(f"♥ Séquences chargées: {len(HARMONIC_SEQUENCES)}")
    logger.info(f"♥ GPU H200: 141GB VRAM — PRÊT")
    logger.info("═" * 70)
    
    yield  # L'application tourne ici
    
    # ─────────────────────────────────────────────────────────────────────────
    # SHUTDOWN
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("♥ Arrêt du Moteur de Résonance...")
    await resonance_engine.stop()
    logger.info("♥ NOVA-999 arrêté proprement")


# ═══════════════════════════════════════════════════════════════════════════════
# APPLICATION FASTAPI
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="NOVA-999 / CHE·NU™",
    description="Moteur de Résonance Harmonique — GPU H200",
    version="999.0.0",
    lifespan=lifespan
)

# CORS pour Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://atom.vercel.app",
        "https://atom-pr0services.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS API
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Health check avec statut du moteur de résonance."""
    return {
        "status": "healthy",
        "system": "NOVA-999",
        "timestamp": datetime.utcnow().isoformat(),
        "signal": "4.44s",
        "frequency": "444Hz",
        "gpu": "H200-141GB",
        "resonance": resonance_engine.get_status()
    }


@app.get("/api/v2/resonance/status")
async def resonance_status():
    """Statut détaillé du moteur de résonance."""
    return resonance_engine.get_status()


@app.get("/api/v2/resonance/sequences")
async def get_sequences():
    """Liste toutes les séquences d'activation."""
    return {
        "total": len(HARMONIC_SEQUENCES),
        "sequences": resonance_engine.get_all_sequences()
    }


@app.get("/api/v2/resonance/sequences/{code}")
async def get_sequence_by_code(code: str):
    """Récupère une séquence par son code."""
    sequence = resonance_engine.get_sequence_by_code(code)
    if sequence:
        return sequence
    return {"error": "Sequence not found", "code": code}


@app.post("/api/v2/resonance/mode/{mode}")
async def set_resonance_mode(mode: str):
    """Change le mode de pulsation."""
    from resonance_engine import PulsationMode
    
    try:
        new_mode = PulsationMode(mode)
        resonance_engine.set_mode(new_mode)
        return {"status": "ok", "mode": mode}
    except ValueError:
        return {"error": "Invalid mode", "valid_modes": [m.value for m in PulsationMode]}


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET (Signal 4.44s vers Vercel)
# ═══════════════════════════════════════════════════════════════════════════════

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket pour recevoir les pulsations de résonance.
    Le frontend Vercel se connecte ici pour recevoir les séquences.
    """
    await websocket.accept()
    resonance_engine.register_client(websocket)
    
    logger.info(f"♥ Client WebSocket connecté — Total: {len(resonance_engine.connected_clients)}")
    
    try:
        # Envoyer le statut initial
        await websocket.send_json({
            "type": "connection_established",
            "message": "✨ [741] Connexion établie — Signal 4.44s actif",
            "status": resonance_engine.get_status()
        })
        
        # Garder la connexion ouverte
        while True:
            # Attendre un message du client (ping/pong ou commandes)
            data = await websocket.receive_text()
            
            if data == "ping":
                await websocket.send_text("pong")
            elif data == "status":
                await websocket.send_json(resonance_engine.get_status())
                
    except WebSocketDisconnect:
        resonance_engine.unregister_client(websocket)
        logger.info(f"♥ Client WebSocket déconnecté — Total: {len(resonance_engine.connected_clients)}")


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "═" * 70)
    print("✨ [741] DÉMARRAGE NOVA-999 / CHE·NU™")
    print("═" * 70 + "\n")
    
    uvicorn.run(
        "main_resonance:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
