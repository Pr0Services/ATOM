#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# CHE·NU™ / AT·OM — DÉMARRAGE DIRECT (SANS DOCKER)
# ═══════════════════════════════════════════════════════════════════════════
# [AQUA] + [ADAMAS] + SEQUENCE 3-6-9-12
# ═══════════════════════════════════════════════════════════════════════════

set -e

CYAN='\033[0;36m'
GOLD='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GOLD}     ✧ CHE·NU™ — DÉMARRAGE DIRECT ✧${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# VÉRIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════

if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Fichier .env non trouvé!${NC}"
    exit 1
fi

if grep -q "VOTRE_MOT_DE_PASSE_ICI" .env; then
    echo -e "${RED}❌ Remplacez VOTRE_MOT_DE_PASSE_ICI dans .env${NC}"
    exit 1
fi

# ═══════════════════════════════════════════════════════════════════════════
# ENVIRONNEMENT VIRTUEL
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}[1/3]${NC} Configuration de l'environnement..."

if [ ! -d "venv" ]; then
    echo "     Création de l'environnement virtuel..."
    python3 -m venv venv
fi

source venv/bin/activate
echo -e "     ${GREEN}✓${NC} Environnement activé"

# ═══════════════════════════════════════════════════════════════════════════
# DÉPENDANCES
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}[2/3]${NC} Installation des dépendances..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "     ${GREEN}✓${NC} Dépendances installées"

# ═══════════════════════════════════════════════════════════════════════════
# DÉMARRAGE
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}[3/3]${NC} Démarrage du serveur..."
echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GOLD}     ✧ AT·OM BACKEND DÉMARRÉ ✧${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "     API:    ${GREEN}http://localhost:8000${NC}"
echo -e "     Docs:   ${GREEN}http://localhost:8000/docs${NC}"
echo ""

# Charger les variables d'environnement
export $(grep -v '^#' .env | xargs)

# Démarrer uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
