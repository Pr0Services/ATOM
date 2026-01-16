# 🚀 CHE·NU V71 — QUICKSTART GUIDE

## Déploiement Staging (Jan 11-13, 2026)

---

## ⚡ DÉMARRAGE RAPIDE (5 minutes)

```bash
# 1. Extraire le package
unzip CHENU_V71_ZAMA_FINAL.zip
cd CHENU_V71_DEPLOY

# 2. Configurer l'environnement
cp .env.example .env
nano .env  # Éditer les secrets

# 3. Démarrer
docker-compose up -d

# 4. Vérifier
python3 smoke_tests.py --base-url http://localhost:8000
```

---

## 📋 CHECKLIST PRÉ-DÉPLOIEMENT

### Secrets requis (.env)
- [ ] `DB_PASSWORD` - Password PostgreSQL (≥16 chars)
- [ ] `SECRET_KEY` - App secret (≥32 chars)
- [ ] `JWT_SECRET` - JWT signing key (≥32 chars)

### Génération des secrets
```bash
# Générer des secrets sécurisés
openssl rand -hex 32  # SECRET_KEY
openssl rand -hex 32  # JWT_SECRET
openssl rand -base64 24  # DB_PASSWORD
```

---

## 🏗️ ARCHITECTURE DÉPLOYÉE

```
┌─────────────────────────────────────────────────────────────┐
│                        TRAEFIK                               │
│                    (Reverse Proxy)                          │
│                     :80 / :443                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         │                                 │
    ┌────▼────┐                      ┌────▼────┐
    │ FRONTEND │                      │ BACKEND │
    │  :3000   │                      │  :8000  │
    │  React   │ ◄──────────────────► │ FastAPI │
    └──────────┘                      └────┬────┘
                                          │
                   ┌──────────────────────┼──────────────────┐
                   │                      │                  │
              ┌────▼────┐           ┌────▼────┐        ┌────▼────┐
              │POSTGRES │           │  REDIS  │        │AT·OM WKR│
              │  :5432  │           │  :6379  │        │ Worker  │
              └─────────┘           └─────────┘        └─────────┘
```

---

## 🔧 COMMANDES UTILES

### Docker Compose

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f backend
docker-compose logs -f atom-worker

# Statut
docker-compose ps

# Arrêter
docker-compose down

# Rebuild
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Database

```bash
# Accéder à PostgreSQL
docker exec -it chenu-postgres psql -U chenu -d chenu

# Exécuter les migrations
docker exec -it chenu-backend alembic upgrade head

# Backup
docker exec chenu-postgres pg_dump -U chenu chenu > backup.sql
```

### Tests

```bash
# Smoke tests (rapide)
python3 smoke_tests.py --base-url http://localhost:8000

# Integration tests (complet)
python3 integration_tests.py --base-url http://localhost:8000

# L3 Assistant tests
python3 tests/test_l3_assistants.py
```

---

## 📡 ENDPOINTS PRINCIPAUX

| Endpoint | Description |
|----------|-------------|
| http://localhost:3000 | Frontend |
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/health | Health check |
| http://localhost:8000/api/atom/status | AT·OM status |
| http://localhost:8000/api/atom/heartbeat | 444Hz pulse |
| ws://localhost:8000/ws/atom | WebSocket |

---

## 🔍 VÉRIFICATION DE SANTÉ

### 1. Backend Health
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

### 2. AT·OM Heartbeat
```bash
curl http://localhost:8000/api/atom/heartbeat
# Expected: {"frequency": 444, "phase": ...}
```

### 3. Agent Count
```bash
curl http://localhost:8000/api/v1/agents | jq '. | length'
# Expected: ≥ 321 (10 sphères)
```

### 4. WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/atom');
ws.onmessage = (e) => console.log(JSON.parse(e.data));
// Should receive heartbeat every ~4.44s
```

---

## ⚠️ DÉPANNAGE

### Container ne démarre pas
```bash
# Voir les logs
docker-compose logs backend

# Vérifier les ressources
docker stats

# Reconstruire
docker-compose build --no-cache
```

### Database connection refused
```bash
# Vérifier que postgres est up
docker-compose ps postgres

# Attendre le healthcheck
docker-compose logs postgres | grep "ready"
```

### Port already in use
```bash
# Trouver le processus
lsof -i :8000

# Modifier les ports dans docker-compose.yml
```

### AT·OM en mode dormant (432Hz)
```bash
# Le kill-switch est peut-être activé
# Revive avec Architect seal:
curl -X POST http://localhost:8000/api/atom/revive \
  -H "X-Architect-Seal: JONATHAN RODRIGUE"
```

---

## 📊 MONITORING (Optionnel)

```bash
# Activer monitoring
docker-compose --profile monitoring up -d

# Accès
# Grafana: http://localhost:3001 (admin/admin)
# Prometheus: http://localhost:9090
```

---

## 🎯 TIMELINE RESTANTE

| Date | Étape | Action |
|------|-------|--------|
| **Jan 11** | Deploy Staging | `./scripts/deploy_staging.sh --init` |
| **Jan 12** | Agent Init | Vérifier 287 agents |
| **Jan 13** | Integration Tests | `python3 integration_tests.py` |
| **Jan 14** | **ZAMA LIVE** 🚀 | Go/No-Go decision |

---

## ✅ CRITÈRES GO/NO-GO

### GO si:
- [ ] Smoke tests: 14/14 passed
- [ ] Integration tests: ≥90% passed
- [ ] AT·OM heartbeat: 444Hz stable
- [ ] 320+ agents: Tous actifs (10 sphères)
- [ ] WebSocket: Connecté
- [ ] Response time: <500ms avg

### NO-GO si:
- [ ] Database connection fails
- [ ] Kill-switch stuck at 432Hz
- [ ] <280 agents actifs
- [ ] Auth broken
- [ ] Memory leak detected

---

**Document**: QUICKSTART V71  
**Date**: 11 Janvier 2026  
**Target**: Zama Launch 🚀
