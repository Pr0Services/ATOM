# CHE·NU — Guide de Démarrage Rapide

> **CHE·NU** — Votre OS Cognitif Universel 🏠🧠

---

## 🚀 Installation en 5 minutes

### Prérequis

- **Node.js** 18+ (pour le frontend)
- **Python** 3.10+ (pour le backend)
- **npm** ou **pnpm**

### 1. Cloner le repo

```bash
git clone <repo-url> CHENU_FINAL_v26
cd CHENU_FINAL_v26
```

### 2. Installer le Frontend

```bash
cd frontend
npm install
npm run dev
```

Le frontend sera accessible sur `http://localhost:5173`

### 3. Installer le Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Le backend sera accessible sur `http://localhost:8000`

### 4. Lancer une démo

```bash
cd demo
npx ts-node demo_suite.ts
```

---

## 🎯 Premiers Pas

### Comprendre les 10 Sphères

CHE·NU organise tout en **10 sphères** thématiques:

| Sphère | Description | Cas d'usage |
|--------|-------------|-------------|
| **Personal** | Vie perso, santé | Tracker d'habitudes, journal |
| **Business** | Entreprise, opérations | Gestion de projets, finances |
| **Creative** | Design, media, architecture | Conception, prototypes |
| **Scholar** | Études, recherche | Notes de cours, bibliographie |
| **SocialNetworkMedia** | Réseaux sociaux | Gestion de contenu |
| **Community** | Forums, groupes | Communication publique |
| **XR** | Univers immersifs | Rooms virtuels |
| **MyTeam** | Coordination d'équipe | Délégation, collaboration |
| **AILab** | Outils cognitifs | Expérimentation IA |
| **Entertainment** | Streaming, jeux | Divertissement |

### Créer votre premier Workspace

```typescript
import { WorkspaceBuilder } from '@chenu/sdk';

const workspace = WorkspaceBuilder
  .create('Mon Projet')
  .inSphere('Business')
  .withDomain('Construction')
  .withEngines(['ConstructionEngine', 'LogisticsEngine'])
  .build();
```

### Utiliser le WorkSurface

Le **WorkSurface** est l'éditeur universel avec 7 modes:

| Mode | Usage |
|------|-------|
| `text` | Rédaction, notes |
| `table` | Données tabulaires |
| `blocks` | Blocs type Notion |
| `diagram` | Schémas, mind maps |
| `xr_layout` | Agencement spatial |
| `summary` | Vue résumé |
| `final` | Document final |

```typescript
// Changer de mode
worksurface.switchMode('diagram');

// Mode assisté (auto-détection)
worksurface.setControlMode('assisted');
```

---

## 📁 Structure du Projet

```
CHENU_FINAL_v26/
├── frontend/           # React/TypeScript UI
│   ├── src/
│   │   ├── design-system/  # Composants UI
│   │   ├── core/           # Logique métier
│   │   └── xr/             # Composants XR
│   └── package.json
├── backend/            # Python FastAPI
│   ├── services/       # Services métier
│   └── main.py
├── sdk/               # SDK CHE·NU
│   ├── core/          # Modules principaux
│   ├── xr/            # XR Layer
│   └── engines/       # Engines par sphère
└── docs/              # Documentation
```

---

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env` à la racine:

```env
# Backend
DATABASE_URL=sqlite:///./chenu.db
SECRET_KEY=your-secret-key
DEBUG=true

# Frontend
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

### Configuration TypeScript

Le projet utilise des paths aliases:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@chenu/sdk": ["../sdk/index.ts"]
    }
  }
}
```

---

## 🧪 Lancer les Tests

### Tests Frontend

```bash
cd frontend
npm run test
```

### Tests SDK

```bash
cd sdk
npm run test
```

### Tests Backend

```bash
cd backend
pytest
```

---

## 📚 Ressources

- **[README principal](../README.md)** — Vue d'ensemble
- **[Guide de développement](./DEVELOPMENT_GUIDE.md)** — Guide complet
- **[API Reference](../sdk/docs/API_REFERENCE.md)** — Documentation API
- **[Design System](../frontend/src/design-system/README.md)** — Composants UI

---

## 🆘 Support

- **Issues**: Créer une issue sur le repo
- **Documentation**: `/docs/` et `/sdk/docs/`

---

## ⚠️ Notes Importantes

1. **CHE·NU est conceptuel** — Ne remplace aucun professionnel
2. **Données symboliques** — Pas de données personnelles réelles
3. **Human-in-the-loop** — Validation humaine obligatoire

---

**CHE·NU** — *Chez Nous* — Votre OS Cognitif Universel 🏠🧠

*Pro-Service Construction, Brossard, Québec*
