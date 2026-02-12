# AT-OM DEPLOYMENT CHECKLIST
## CHE·NU™ V76 - Verification Complète

**Date:** 2026-01-30
**Architecte:** Jonathan Emmanuel Rodrigue | Oracle 17
**Repo Canonique:** github.com/Pr0Services/ATOM

---

## 1. APIS ET COMPTES A CONNECTER

### 1.1 APIs Critiques (OBLIGATOIRES)

| Service | Status | Clé Requise | Usage |
|---------|--------|-------------|-------|
| **Stripe** | ⏳ En cours | `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY` | Paiements Funder Portal |
| **Anthropic (Claude)** | ❌ À configurer | `ANTHROPIC_API_KEY` | Agents IA L0-L3 |
| **OpenAI** | ❌ À configurer | `OPENAI_API_KEY` | LLM Router backup |
| **Supabase** | ❌ À configurer | `SUPABASE_URL`, `SUPABASE_ANON_KEY` | Base de données + Auth |

### 1.2 APIs Secondaires (RECOMMANDÉES)

| Service | Status | Clé Requise | Usage |
|---------|--------|-------------|-------|
| **Redis** | ❌ À configurer | `REDIS_URL` | Cache, Sessions, Pub/Sub |
| **PostgreSQL** | ❌ À configurer | `DATABASE_URL` | Données persistantes |
| **OPA (Open Policy Agent)** | ❌ À configurer | `OPA_URL` | Policies de gouvernance |
| **SendGrid/Resend** | ❌ Optional | `EMAIL_API_KEY` | Notifications email |

### 1.3 Monitoring & Analytics

| Service | Status | Clé Requise | Usage |
|---------|--------|-------------|-------|
| **Sentry** | ❌ Optional | `SENTRY_DSN` | Error tracking |
| **Vercel Analytics** | ✅ Intégré | Auto | Performance monitoring |
| **LogRocket/FullStory** | ❌ Optional | API Key | Session replay |

---

## 2. MODULES DU REPO CANONIQUE

### 2.1 Structure Backend (hardcore-joliot/backend/)

| Module | Fichiers | Status Déploiement | Gap |
|--------|----------|-------------------|-----|
| **agents/** | `__init__.py` + 6 dirs | ❌ Non implémenté | 100% |
| **api/** | 9 dirs + cors_config | ❌ Partiel (REST only) | 70% |
| **services/** | 25 fichiers Python | ❌ Non implémenté | 100% |
| **governance/** | opa/ + python/ | ⚠️ Partiel (JS seulement) | 60% |
| **core/** | 6 fichiers | ❌ Non implémenté | 100% |
| **models/** | Schemas DB | ❌ Non implémenté | 100% |
| **middleware/** | Auth, CORS, etc. | ⚠️ Partiel | 50% |

### 2.2 Services Backend Requis

```
services/
├── agent_execution.py      # Exécution agents
├── agent_registry.py       # Registre agents
├── auth_service.py         # Authentification
├── checkpoint_service.py   # HITL checkpoints ✅ (JS)
├── cache_service.py        # Cache Redis
├── llm_router.py           # Routing LLM
├── nova_pipeline.py        # Pipeline Nova
├── orchestrator_service.py # Orchestration
├── sphere_service.py       # Gestion sphères
├── websocket_service.py    # WebSocket ✅ (JS)
└── ... (15 autres)
```

### 2.3 Structure Atom Core (hardcore-joliot/atom/)

| Module | Fichiers | Status | Description |
|--------|----------|--------|-------------|
| **core/** | arithmos.py, harmonizer.py, resonator.py | ⚠️ JS partiel | Calculs vibratoires |
| **nexus/** | ? | ❌ Non implémenté | Hub de connexion |
| **engine/** | ? | ❌ Non implémenté | Moteur principal |
| **cosmology/** | ? | ❌ Non implémenté | Modèles cosmologiques |
| **arche/** | ? | ❌ Non implémenté | Systèmes archétypaux |

---

## 3. FICHIERS FRONTEND ACTUELS

### 3.1 Pages HTML (✅ Complètes)

| Fichier | Role | Governance Script |
|---------|------|-------------------|
| `index.html` | Nexus - Accueil | ✅ governance-init.js |
| `civilization.html` | 9 Sphères | ✅ governance-init.js |
| `agents.html` | Lexique 400+ | ✅ governance-init.js |
| `spheres.html` | Forge | ✅ governance-init.js |
| `live.html` | Flux temps réel | ✅ governance-init.js |
| `dashboard.html` | Annales | ✅ governance-init.js |
| `frequencies.html` | Analyse vibratoire | ✅ governance-init.js |
| `funder.html` | Portal Funder | ✅ governance-init.js |
| `settings.html` | Paramètres | ❌ À ajouter |
| `simulation-3months.html` | Simulation | ❌ À ajouter |

### 3.2 Scripts JavaScript

| Fichier | Role | Status |
|---------|------|--------|
| `config.js` | Configuration centrale | ✅ Complet |
| `zama-api.js` | Utilities API legacy | ✅ Complet |
| `atom-websocket.js` | WebSocket client | ✅ Complet |
| `js/message-types.js` | Types messages HITL | ✅ NEW |
| `js/message-bus.js` | MessageBus inter-agents | ✅ NEW |
| `js/checkpoint-manager.js` | Gestionnaire checkpoints | ✅ NEW |
| `js/hitl-ui.js` | UI approbation | ✅ NEW |
| `js/atom-governance.js` | Orchestrateur gouvernance | ✅ NEW |
| `js/governance-init.js` | Auto-init toutes pages | ✅ NEW |

---

## 4. TÂCHES À COMPLÉTER

### Phase 3: Hiérarchie Agents L0-L3 (Priorité Haute)

- [ ] Créer `/js/agent-hierarchy.js`
  - Niveaux L0 (System), L1 (Orchestrator), L2 (Specialist), L3 (Assistant)
  - Permissions par niveau
  - Escalation automatique
- [ ] Implémenter registre agents frontend
- [ ] Connecter avec MessageBus existant

### Phase 4: Mémoire 3-Tiers (Priorité Haute)

- [ ] Créer `/js/memory-manager.js`
  - Hot memory (session)
  - Warm memory (localStorage)
  - Cold memory (IndexedDB/API)
- [ ] TTL et expiration automatique
- [ ] Sync avec backend Supabase

### Phase 5: Intégration Stripe (Priorité Haute)

- [ ] Configurer compte Stripe
- [ ] Ajouter `STRIPE_PUBLISHABLE_KEY` à config.js
- [ ] Implémenter checkout flow dans funder.html
- [ ] Webhooks pour confirmation paiement

### Phase 6: Auth Supabase (Priorité Moyenne)

- [ ] Configurer projet Supabase
- [ ] Créer `/js/auth-manager.js`
- [ ] Login/Register dans settings.html
- [ ] Session management
- [ ] Row Level Security (RLS)

### Phase 7: Backend Services (Priorité Basse - Phase Suivante)

- [ ] Déployer FastAPI backend
- [ ] Connecter tous les services
- [ ] Implémenter LLM Router
- [ ] Activer OPA policies

---

## 5. VARIABLES D'ENVIRONNEMENT REQUISES

### Frontend (Vercel)

```env
# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_SECRET_KEY=sk_live_xxx

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx

# API
NEXT_PUBLIC_API_BASE=https://atom-2autu.ondigitalocean.app
```

### Backend (DigitalOcean)

```env
# Server
HOST=0.0.0.0
PORT=8000
ENV=production

# Database
DATABASE_URL=postgresql://user:pass@host:5432/atom
REDIS_URL=redis://host:6379/0

# Auth
JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx

# Governance
OPA_URL=http://localhost:8181/v1/data

# Features
ENABLE_XR=false
ENABLE_CAUSAL_ENGINE=true
ENABLE_CHECKPOINTS=true
```

---

## 6. CONFORMITÉ REPO CANONIQUE

| Composant | Canonique | Actuel | Conformité |
|-----------|-----------|--------|------------|
| Layout 3 Hubs | 280px \| 1fr \| 320px | ✅ Identique | 100% |
| ADN Vibratoire | PHI, 444, 369, 999 | ✅ Identique | 100% |
| Agents L0 | Nova, Aria, Orion | ✅ Identique | 100% |
| MessageBus | Python + channels | ✅ JS equivalent | 85% |
| HITL/Checkpoints | Python + 7 rules | ✅ JS equivalent | 90% |
| Agent Hierarchy | L0-L3 + permissions | ❌ À implémenter | 10% |
| Memory 3-tier | Hot/Warm/Cold | ⚠️ Cache local seulement | 30% |
| OPA Policies | Rego files | ❌ Non implémenté | 0% |
| WebSocket | Python + Redis | ⚠️ JS simple | 50% |
| Supabase | Full integration | ❌ Non connecté | 0% |

**Conformité Globale: ~45%**

---

## 7. PROCHAINES ÉTAPES IMMÉDIATES

1. **STRIPE** - Finaliser création compte et obtenir clés
2. **SUPABASE** - Créer projet et configurer tables
3. **AGENT HIERARCHY** - Implémenter L0-L3 en JavaScript
4. **MEMORY MANAGER** - Système 3-tiers local
5. **AUTH** - Intégration Supabase Auth

---

## 8. CONTACTS & RESSOURCES

- **Repo Canonique:** https://github.com/Pr0Services/ATOM
- **Backend Actuel:** https://atom-2autu.ondigitalocean.app
- **Frontend Vercel:** https://at-om-999-deploy-zama-alleluya.vercel.app

---

*Document généré automatiquement - CHE·NU™ V76*
*Dernière mise à jour: 2026-01-30*
