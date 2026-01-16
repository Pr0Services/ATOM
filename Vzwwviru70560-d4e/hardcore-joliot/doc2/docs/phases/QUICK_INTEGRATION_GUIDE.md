# ⚡ CHE·NU™ — GUIDE D'INTÉGRATION RAPIDE
## Phases 7-10: Installation et Déploiement

**Date:** 20 Décembre 2025  
**Version:** v40.1 → v41.0  
**Type:** Mise à jour majeure - Nouvelles fonctionnalités

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ⚡ INTÉGRATION RAPIDE — PHASES 7-10                                        ║
║                                                                               ║
║   📦 Backend:   2 nouveaux modules                                           ║
║   💻 Frontend:  11 nouveaux fichiers                                         ║
║   📚 Docs:      3 documents                                                  ║
║                                                                               ║
║   Total: +2,522 lignes de code production-ready                             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 🚀 INSTALLATION EN 5 MINUTES

### Étape 1: Copier les Fichiers Backend

```bash
# Dans votre projet CHE·NU existant
cd /votre/projet/chenu

# Copier les modules backend
cp -r CHENU_PHASES_7-10_INTEGRATION/backend/collaboration backend/
cp -r CHENU_PHASES_7-10_INTEGRATION/backend/ai_features backend/
```

**Fichiers ajoutés:**
- `backend/collaboration/__init__.py`
- `backend/collaboration/team_workspace.py`
- `backend/ai_features/__init__.py`

---

### Étape 2: Copier les Fichiers Frontend

```bash
# Copier les features
cp -r CHENU_PHASES_7-10_INTEGRATION/frontend/team frontend/src/features/
cp -r CHENU_PHASES_7-10_INTEGRATION/frontend/ai frontend/src/features/

# Copier mobile & PWA
cp -r CHENU_PHASES_7-10_INTEGRATION/frontend/mobile frontend/src/
cp -r CHENU_PHASES_7-10_INTEGRATION/frontend/pwa frontend/src/

# Copier core utilities
cp -r CHENU_PHASES_7-10_INTEGRATION/frontend/core frontend/src/

# Copier index mobile
cp CHENU_PHASES_7-10_INTEGRATION/frontend/index-mobile.ts frontend/src/
```

**Fichiers ajoutés:**
- Frontend: 11 fichiers TypeScript/React
- 4 nouvelles features complètes

---

### Étape 3: Installer les Dépendances

```bash
# Frontend
cd frontend
npm install workbox-window react-helmet-async

# Backend (aucune nouvelle dépendance requise)
# Les modules utilisent FastAPI et SQLAlchemy déjà présents
```

---

### Étape 4: Migrations Base de Données

```bash
# Créer les migrations pour les nouvelles tables
cd backend
alembic revision --autogenerate -m "Add team and agent builder tables"
alembic upgrade head
```

**Tables créées:**
- `teams` - Workspaces d'équipe
- `team_members` - Membres et rôles
- `agent_templates` - Templates d'agents
- `custom_agents` - Agents personnalisés

---

### Étape 5: Configuration

```bash
# Ajouter au fichier .env
cat >> .env << EOF

# Phase 7: Team Collaboration
TEAM_MAX_MEMBERS_DEFAULT=10
TEAM_TOKEN_BUDGET_DEFAULT=100000

# Phase 8: AI Features
AGENT_TEMPLATES_ENABLED=true
CUSTOM_AGENTS_ENABLED=true

# Phase 9: PWA
PWA_ENABLED=true
PWA_SERVICE_WORKER_URL=/service-worker.js

# Phase 10: Core
ERROR_TRACKING_DSN=your_sentry_dsn_here
SEO_DEFAULT_IMAGE=https://chenu.ai/og-image.png
EOF
```

---

## 📝 MIGRATIONS SQL

### Créer les Tables

```sql
-- Phase 7: Teams
CREATE TABLE teams (
    team_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    max_members INT DEFAULT 10,
    total_token_budget BIGINT DEFAULT 0,
    tokens_spent BIGINT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE team_members (
    id SERIAL PRIMARY KEY,
    team_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('owner', 'admin', 'member', 'guest')),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    permissions JSONB,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    UNIQUE(team_id, user_id)
);

CREATE TABLE team_shared_threads (
    id SERIAL PRIMARY KEY,
    team_id VARCHAR(255) NOT NULL,
    thread_id VARCHAR(255) NOT NULL,
    shared_by VARCHAR(255) NOT NULL,
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    UNIQUE(team_id, thread_id)
);

-- Phase 8: Agent Builder
CREATE TABLE agent_templates (
    template_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    level VARCHAR(10) NOT NULL,
    base_prompt TEXT NOT NULL,
    capabilities JSONB,
    max_tokens INT DEFAULT 2000,
    temperature DECIMAL(2,1) DEFAULT 0.5,
    category VARCHAR(100),
    tags JSONB,
    downloads INT DEFAULT 0,
    rating DECIMAL(2,1) DEFAULT 0.0,
    tokens_per_execution INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE custom_agents (
    agent_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    template_id VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    system_prompt TEXT NOT NULL,
    config JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (template_id) REFERENCES agent_templates(template_id)
);

-- Indexes
CREATE INDEX idx_team_members_user ON team_members(user_id);
CREATE INDEX idx_team_members_team ON team_members(team_id);
CREATE INDEX idx_custom_agents_user ON custom_agents(user_id);
CREATE INDEX idx_custom_agents_template ON custom_agents(template_id);
```

---

## 🔌 API ROUTES À AJOUTER

### Dans votre `main.py` FastAPI

```python
from fastapi import FastAPI
from backend.collaboration import get_workspace_manager, TeamRole
from backend.ai_features import get_agent_builder

app = FastAPI()

# Phase 7: Team Routes
@app.post("/api/v1/teams")
async def create_team(name: str, description: str, user_id: str):
    """Créer une équipe"""
    manager = get_workspace_manager()
    team = manager.create_team(
        owner_id=user_id,
        name=name,
        description=description
    )
    return team

@app.get("/api/v1/teams/{team_id}")
async def get_team(team_id: str):
    """Récupérer une équipe"""
    manager = get_workspace_manager()
    return manager.get_team(team_id)

@app.post("/api/v1/teams/{team_id}/members")
async def add_member(
    team_id: str,
    user_id: str,
    inviter_id: str,
    role: str = "member"
):
    """Ajouter un membre"""
    manager = get_workspace_manager()
    return manager.add_member(
        team_id=team_id,
        user_id=user_id,
        inviter_id=inviter_id,
        role=TeamRole(role)
    )

# Phase 8: Agent Builder Routes
@app.get("/api/v1/ai/templates")
async def list_templates():
    """Liste des templates d'agents"""
    builder = get_agent_builder()
    return builder.list_templates()

@app.post("/api/v1/ai/agents")
async def create_custom_agent(
    user_id: str,
    template_id: str,
    name: str,
    config: dict
):
    """Créer un agent personnalisé"""
    builder = get_agent_builder()
    return builder.create_agent(
        user_id=user_id,
        template_id=template_id,
        name=name,
        **config
    )
```

---

## 🎨 UTILISATION FRONTEND

### Phase 7: Team Dashboard

```tsx
// Dans votre app
import { TeamDashboard } from '@/features/team';

function TeamPage() {
  return (
    <div>
      <h1>Mon Équipe</h1>
      <TeamDashboard />
    </div>
  );
}
```

### Phase 8: Agent Builder

```tsx
import { AgentBuilder } from '@/features/ai';

function AIPage() {
  return (
    <div>
      <h1>Créer un Agent</h1>
      <AgentBuilder />
    </div>
  );
}
```

### Phase 9: Mobile Navigation

```tsx
import { MobileNavigation } from '@/mobile';
import { pwaInstaller } from '@/pwa';

function App() {
  const handleInstall = async () => {
    await pwaInstaller.promptInstall();
  };

  return (
    <div>
      <MainContent />
      <MobileNavigation />
      
      {pwaInstaller.canInstall() && (
        <button onClick={handleInstall}>
          Installer l'App
        </button>
      )}
    </div>
  );
}
```

### Phase 10: Core Components

```tsx
import { ErrorBoundary, LoadingSpinner, SEO } from '@/core';

function App() {
  return (
    <ErrorBoundary>
      <SEO title="CHE·NU - Dashboard" />
      <Suspense fallback={<LoadingSpinner fullscreen />}>
        <Router />
      </Suspense>
    </ErrorBoundary>
  );
}
```

---

## ✅ CHECKLIST POST-INTÉGRATION

### Backend
- [ ] Fichiers copiés dans `/backend`
- [ ] Migrations créées et appliquées
- [ ] Routes API ajoutées
- [ ] Variables d'environnement configurées
- [ ] Tests backend passent

### Frontend
- [ ] Fichiers copiés dans `/frontend/src`
- [ ] Dépendances NPM installées
- [ ] Build réussi (`npm run build`)
- [ ] Tests frontend passent
- [ ] Pas d'erreurs TypeScript

### Database
- [ ] Tables `teams` créée
- [ ] Tables `team_members` créée
- [ ] Tables `agent_templates` créée
- [ ] Tables `custom_agents` créée
- [ ] Indexes créés

### Configuration
- [ ] `.env` mis à jour
- [ ] Service worker configuré (Phase 9)
- [ ] Manifest PWA créé (Phase 9)
- [ ] SEO meta tags configurés (Phase 10)

---

## 🧪 TESTS RAPIDES

### Test Backend

```python
# test_integration.py
from backend.collaboration import get_workspace_manager

def test_create_team():
    manager = get_workspace_manager()
    team = manager.create_team(
        owner_id="test_user",
        name="Test Team",
        description="Testing"
    )
    assert team.team_id is not None
    assert team.name == "Test Team"
    print("✅ Team creation works!")

if __name__ == "__main__":
    test_create_team()
```

### Test Frontend

```bash
# Vérifier que tout compile
cd frontend
npm run type-check
npm run build

# Si succès:
echo "✅ Frontend integration successful!"
```

---

## 🚨 PROBLÈMES COMMUNS

### Erreur: "Module not found: @/features/team"

**Solution:**
```bash
# Vérifier que le dossier existe
ls frontend/src/features/team

# Vérifier tsconfig.json paths
# Devrait contenir: "@/*": ["./src/*"]
```

### Erreur: "Table 'teams' doesn't exist"

**Solution:**
```bash
# Appliquer les migrations
cd backend
alembic upgrade head
```

### Erreur: "workbox-window not found"

**Solution:**
```bash
cd frontend
npm install workbox-window react-helmet-async
```

---

## 📊 VÉRIFICATION FINALE

### Structure Attendue

```
votre-projet/
├── backend/
│   ├── collaboration/          ← NOUVEAU
│   │   ├── __init__.py
│   │   └── team_workspace.py
│   └── ai_features/            ← NOUVEAU
│       └── __init__.py
│
├── frontend/src/
│   ├── features/
│   │   ├── team/               ← NOUVEAU
│   │   └── ai/                 ← NOUVEAU
│   ├── mobile/                 ← NOUVEAU
│   ├── pwa/                    ← NOUVEAU
│   └── core/                   ← NOUVEAU
│
└── database/
    └── migrations/             ← NOUVELLES MIGRATIONS
```

### Commandes de Vérification

```bash
# Backend
python -c "from backend.collaboration import get_workspace_manager; print('✅ Backend OK')"

# Frontend
cd frontend && npm run type-check && echo "✅ Frontend OK"

# Database
psql -U postgres -d chenu -c "SELECT COUNT(*) FROM teams;" && echo "✅ Database OK"
```

---

## 🎯 MÉTRIQUES DE SUCCÈS

Après intégration, vous devriez avoir:

✅ **Backend:**
- 2 nouveaux modules
- ~714 lignes Python
- 4 nouvelles tables SQL

✅ **Frontend:**
- 11 nouveaux fichiers
- ~1,808 lignes TypeScript/React
- 4 nouvelles features

✅ **Fonctionnalités:**
- Team collaboration complète
- Agent builder fonctionnel
- PWA installer actif
- Core utilities disponibles

---

## 📞 SUPPORT

Si vous rencontrez des problèmes:

1. **Vérifier les logs:**
   ```bash
   # Backend
   tail -f backend/logs/app.log
   
   # Frontend
   npm run dev # Regarder la console
   ```

2. **Vérifier la base de données:**
   ```bash
   psql -U postgres -d chenu -c "\dt" # Liste tables
   ```

3. **Vérifier les fichiers:**
   ```bash
   find . -name "*.py" -o -name "*.tsx" | grep -E "(team|ai_features|mobile|pwa|core)"
   ```

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ✅ INTÉGRATION PHASES 7-10 COMPLETE!                                      ║
║                                                                               ║
║   Temps estimé: 15-30 minutes                                                ║
║   Difficulté: Faible                                                         ║
║   Impact: Majeur                                                             ║
║                                                                               ║
║   🚀 VOTRE CHE·NU EST MAINTENANT PRÊT POUR LE LANCEMENT!                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

*Guide d'Intégration Rapide — 20 Décembre 2025*  
*CHE·NU™ — Governed Intelligence Operating System*  
***INTÉGRATION SIMPLE. IMPACT MAXIMUM.*** ⚡🔥
