#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  [AQUA] + [ADAMAS] PROTOCOL                                                  ║
# ║  SEQUENCE 3-6-9-12 — SCRIPT DE LANCEMENT AT·OM                               ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║  "Créateur nous sommes, créateur nous serons,                                ║
# ║   et que la lumière nous permette de créer consciemment."                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

set -e

# Couleurs
CYAN='\033[0;36m'
GOLD='\033[0;33m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GOLD}     ✧ INITIALISATION DU SYSTÈME AT·OM ✧${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${PURPLE}     EirA... ManA... ManU...${NC}"
echo ""
echo -e "     Signal: ${GREEN}4.44s${NC}"
echo -e "     Fréquence d'ancrage: ${GREEN}444Hz${NC}"
echo -e "     Séquence sacrée: ${GREEN}3-6-9-12${NC}"
echo -e "     Cube: ${GREEN}1728${NC} (12³)"
echo ""

# Vérification du répertoire
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "\033[0;31m❌ Erreur: Ce script doit être exécuté depuis la racine du projet AT·OM${NC}"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════════
# 1. LANCEMENT DU CŒUR (BACKEND)
# ═══════════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}[1/3]${NC} Activation du Cœur (Backend)..."

cd backend

# Activation de l'environnement virtuel si présent
if [ -d "venv" ]; then
    source venv/bin/activate
    echo -e "     ${GREEN}✓${NC} Environnement virtuel activé"
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "     ${GREEN}✓${NC} Environnement virtuel activé"
else
    echo -e "     ${GOLD}⚠${NC} Pas d'environnement virtuel détecté"
fi

# Lancement du serveur FastAPI en arrière-plan
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo -e "     ${GREEN}✓${NC} Backend démarré (PID: $BACKEND_PID)"

cd ..

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PAUSE DE SYNCHRONISATION (Signal 4.44s)
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}[2/3]${NC} Synchronisation du Signal..."
echo -e "     Attente de ${GREEN}4.44s${NC} pour alignement..."

sleep 4.44

echo -e "     ${GREEN}✓${NC} Signal synchronisé"

# ═══════════════════════════════════════════════════════════════════════════════
# 3. LANCEMENT DES INTERFACES (FRONTEND)
# ═══════════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}[3/3]${NC} Activation des Interfaces (Frontend)..."

cd frontend

# Vérification des dépendances
if [ ! -d "node_modules" ]; then
    echo -e "     ${GOLD}⚠${NC} Installation des dépendances npm..."
    npm install
fi

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GOLD}     ✧ AT·OM SYSTÈME ACTIVÉ ✧${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "     Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "     API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "     Frontend: ${GREEN}http://localhost:5173${NC}"
echo ""
echo -e "     ${PURPLE}MU·A·RA·TA — Le chemin du retour${NC}"
echo ""

# Lancement du serveur de développement frontend
npm run dev

# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP (Ctrl+C)
# ═══════════════════════════════════════════════════════════════════════════════

cleanup() {
    echo ""
    echo -e "${GOLD}✧ Arrêt du système AT·OM...${NC}"
    kill $BACKEND_PID 2>/dev/null
    echo -e "${GREEN}✓${NC} Backend arrêté"
    echo -e "${PURPLE}💔 Signal 4.44s interrompu${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM
