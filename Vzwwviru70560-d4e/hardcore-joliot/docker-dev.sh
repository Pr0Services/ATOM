#!/bin/bash
# CHE·NU™ V75 — Docker Development Script
# =========================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║              CHE·NU™ V75 — Docker Development               ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

COMMAND=${1:-start}

case $COMMAND in
  start)
    echo -e "${YELLOW}Starting services...${NC}"
    
    # Start PostgreSQL and Redis
    docker-compose -f docker-compose.dev.yml up -d
    
    echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
    until docker exec chenu-postgres-dev pg_isready -U chenu > /dev/null 2>&1; do
      sleep 1
    done
    echo -e "${GREEN}✓ PostgreSQL ready${NC}"
    
    echo -e "${YELLOW}Waiting for Redis to be ready...${NC}"
    until docker exec chenu-redis-dev redis-cli ping > /dev/null 2>&1; do
      sleep 1
    done
    echo -e "${GREEN}✓ Redis ready${NC}"
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}Services started!${NC}"
    echo ""
    echo -e "PostgreSQL: ${BLUE}localhost:5432${NC}"
    echo -e "  Database: chenu_dev"
    echo -e "  User: chenu"
    echo -e "  Password: chenu_dev_password"
    echo ""
    echo -e "Redis: ${BLUE}localhost:6379${NC}"
    echo ""
    echo -e "${YELLOW}Now start backend and frontend:${NC}"
    echo ""
    echo "  # Terminal 1 - Backend"
    echo "  cd backend"
    echo "  export DATABASE_URL=postgresql://chenu:chenu_dev_password@localhost:5432/chenu_dev"
    echo "  export REDIS_URL=redis://localhost:6379/0"
    echo "  python -m uvicorn app.main:app --port 8000 --reload"
    echo ""
    echo "  # Terminal 2 - Frontend"
    echo "  cd frontend"
    echo "  npm run dev"
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    ;;
    
  stop)
    echo -e "${YELLOW}Stopping services...${NC}"
    docker-compose -f docker-compose.dev.yml down
    echo -e "${GREEN}✓ Services stopped${NC}"
    ;;
    
  restart)
    echo -e "${YELLOW}Restarting services...${NC}"
    docker-compose -f docker-compose.dev.yml restart
    echo -e "${GREEN}✓ Services restarted${NC}"
    ;;
    
  logs)
    docker-compose -f docker-compose.dev.yml logs -f
    ;;
    
  clean)
    echo -e "${RED}Stopping and removing all data...${NC}"
    docker-compose -f docker-compose.dev.yml down -v
    echo -e "${GREEN}✓ Cleaned${NC}"
    ;;
    
  status)
    docker-compose -f docker-compose.dev.yml ps
    ;;
    
  db)
    echo -e "${YELLOW}Connecting to PostgreSQL...${NC}"
    docker exec -it chenu-postgres-dev psql -U chenu -d chenu_dev
    ;;
    
  redis)
    echo -e "${YELLOW}Connecting to Redis...${NC}"
    docker exec -it chenu-redis-dev redis-cli
    ;;
    
  *)
    echo "Usage: $0 {start|stop|restart|logs|clean|status|db|redis}"
    echo ""
    echo "Commands:"
    echo "  start   - Start PostgreSQL and Redis containers"
    echo "  stop    - Stop containers"
    echo "  restart - Restart containers"
    echo "  logs    - View container logs"
    echo "  clean   - Stop and remove all data (volumes)"
    echo "  status  - Show container status"
    echo "  db      - Connect to PostgreSQL CLI"
    echo "  redis   - Connect to Redis CLI"
    exit 1
    ;;
esac
