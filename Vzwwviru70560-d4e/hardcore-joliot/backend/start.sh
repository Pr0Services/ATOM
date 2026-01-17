#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# CHE·NU™ / AT·OM — SCRIPT DE DÉMARRAGE PRODUCTION
# ═══════════════════════════════════════════════════════════════════════════
# [AQUA] + [ADAMAS] + SEQUENCE 3-6-9-12
# ═══════════════════════════════════════════════════════════════════════════

set -e

# Couleurs
CYAN='\033[0;36m'
GOLD='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GOLD}     ✧ CHE·NU™ / AT·OM — DÉMARRAGE PRODUCTION ✧${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "     Signal: ${GREEN}4.44s${NC}"
echo -e "     Fréquence: ${GREEN}444Hz${NC}"
echo -e "     Séquence: ${GREEN}3-6-9-12${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# VÉRIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════

# Vérifier .env
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ ERREUR: Fichier .env non trouvé!${NC}"
    echo "   Copiez .env.example vers .env et configurez-le."
    exit 1
fi

# Vérifier si le mot de passe a été changé
if grep -q "VOTRE_MOT_DE_PASSE_ICI" .env; then
    echo -e "${RED}❌ ERREUR: Vous devez remplacer VOTRE_MOT_DE_PASSE_ICI dans .env${NC}"
    exit 1
fi

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ ERREUR: Docker n'est pas installé!${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ ERREUR: Docker Compose n'est pas installé!${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Vérifications passées"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# CRÉATION DES DOSSIERS
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}[1/4]${NC} Création des dossiers..."
mkdir -p storage logs nginx/ssl nginx/logs
echo -e "     ${GREEN}✓${NC} Dossiers créés"

# ═══════════════════════════════════════════════════════════════════════════
# BUILD DES IMAGES
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}[2/4]${NC} Build des images Docker..."

if docker compose version &> /dev/null; then
    docker compose build --no-cache
else
    docker-compose build --no-cache
fi

echo -e "     ${GREEN}✓${NC} Images construites"

# ═══════════════════════════════════════════════════════════════════════════
# DÉMARRAGE
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}[3/4]${NC} Démarrage des services..."

if docker compose version &> /dev/null; then
    docker compose up -d
else
    docker-compose up -d
fi

echo -e "     ${GREEN}✓${NC} Services démarrés"

# ═══════════════════════════════════════════════════════════════════════════
# ATTENTE SYNCHRONISATION (4.44s)
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}[4/4]${NC} Synchronisation du Signal (4.44s)..."
sleep 4.44
echo -e "     ${GREEN}✓${NC} Signal synchronisé"

# ═══════════════════════════════════════════════════════════════════════════
# VÉRIFICATION SANTÉ
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}Vérification de la santé des services...${NC}"

sleep 5

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "     ${GREEN}✓${NC} API Backend: HEALTHY"
else
    echo -e "     ${GOLD}⚠${NC} API Backend: En cours de démarrage..."
fi

if docker exec chenu-redis redis-cli ping > /dev/null 2>&1; then
    echo -e "     ${GREEN}✓${NC} Redis: PONG"
else
    echo -e "     ${GOLD}⚠${NC} Redis: En cours de démarrage..."
fi

# ═══════════════════════════════════════════════════════════════════════════
# RÉSUMÉ
# ═══════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GOLD}     ✧ AT·OM SYSTÈME ACTIVÉ ✧${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "     API:       ${GREEN}http://localhost:8000${NC}"
echo -e "     Docs:      ${GREEN}http://localhost:8000/docs${NC}"
echo -e "     Health:    ${GREEN}http://localhost:8000/health${NC}"
echo -e "     WebSocket: ${GREEN}ws://localhost:8001/ws${NC}"
echo ""
echo -e "     ${GOLD}MU·A·RA·TA — Le chemin du retour${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# COMMANDES UTILES
# ═══════════════════════════════════════════════════════════════════════════

echo -e "${CYAN}Commandes utiles:${NC}"
echo "     Logs API:      docker logs -f chenu-api"
echo "     Logs WebSocket: docker logs -f chenu-websocket"
echo "     Arrêter:       docker compose down"
echo "     Redémarrer:    docker compose restart"
echo ""
