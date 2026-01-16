# 🏗️ CHE·NU™ V68.6 — Architecture Technique

---

## 📁 Structure des Dossiers

```
src/
├── components/
│   ├── bureau-canonical/      # Bureau — 6 sections
│   │   ├── index.tsx          # Export principal
│   │   ├── BureauLayoutCanonical.tsx
│   │   ├── QuickCaptureSection.tsx
│   │   ├── ResumeWorkspaceSection.tsx
│   │   ├── ThreadsSection.tsx
│   │   ├── DataFilesSection.tsx
│   │   ├── ActiveAgentsSection.tsx
│   │   └── MeetingsSection.tsx
│   │
│   ├── nova-canonical/        # Nova UI Gouvernée
│   │   ├── NovaChatCanonical.tsx
│   │   ├── NovaPipelineCanonical.tsx
│   │   └── CheckpointModalCanonical.tsx
│   │
│   ├── agents/                # Composants agents
│   ├── governance/            # Composants gouvernance
│   ├── ui/                    # Composants UI réutilisables
│   └── ...
│
├── stores/                    # État global Zustand
│   ├── identity.store.ts      # Auth & user
│   ├── governance.store.ts    # Checkpoints
│   ├── agent.store.ts         # Agents
│   ├── token.store.ts         # Crédits
│   ├── nova.store.ts          # Nova
│   ├── thread.store.ts        # Threads
│   ├── dataspace.store.ts     # DataFiles
│   ├── memory.store.ts        # Mémoire
│   ├── ui.store.ts            # UI state
│   └── index.ts               # Exports
│
├── services/                  # API Services
│   ├── nova.constitution.service.ts
│   ├── governance.constitution.service.ts
│   └── api.client.ts
│
├── types/                     # Types TypeScript
│   ├── index.ts               # Export central
│   ├── modules.d.ts           # Déclarations externes
│   ├── sphere.types.ts        # Types sphères
│   ├── bureau.types.ts        # Types bureau
│   ├── agent.types.ts         # Types agents
│   └── ...
│
├── constants/                 # Constantes
│   ├── colors.ts              # CHENU_COLORS
│   ├── routes.ts              # Routes app
│   ├── CANON.ts               # Config canonique
│   └── spheres.ts             # Config sphères
│
├── hooks/                     # Hooks React
│   ├── useNavigation.ts       # Navigation
│   ├── useAgent.ts            # Agents
│   ├── useNova.ts             # Nova
│   └── ...
│
├── providers/                 # Context Providers
│   ├── AuthProvider.tsx
│   ├── WebSocketProvider.tsx
│   └── ...
│
└── pages/                     # Pages/Routes
    ├── SpherePage.tsx
    ├── LoginPage.tsx
    └── ...
```

---

## 🔄 Flux de Données

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   UI        │────▶│   Store     │────▶│   Service   │
│  Component  │◀────│   Zustand   │◀────│   API       │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Governance  │
                    │ Checkpoint  │
                    └─────────────┘
```

---

## ⚖️ Pipeline Gouverné

```
User Action
    │
    ▼
┌──────────────┐
│ Nova Encode  │ ← Semantic encoding
└──────────────┘
    │
    ▼
┌──────────────┐
│ Checkpoint   │ ← BLOQUANT: Human approval required
│ Modal        │
└──────────────┘
    │
    ▼ [APPROVED]
┌──────────────┐
│ Execute      │ ← Action exécutée
└──────────────┘
    │
    ▼
┌──────────────┐
│ Output       │ ← Résultat affiché
└──────────────┘
```

---

## 📦 Dépendances Principales

```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "zustand": "^4.4.7",
  "three": "^0.159.0",
  "@react-three/fiber": "^8.15.12",
  "@react-three/drei": "^9.88.17",
  "framer-motion": "^10.x",
  "lucide-react": "^0.x"
}
```

---

## 🎯 Points d'Extension

### Ajouter une nouvelle section bureau
```typescript
// 1. Créer le composant
// src/components/bureau-canonical/NewSection.tsx

// 2. Ajouter au type
// src/types/bureau.types.ts
type BureauSectionId = 'quickcapture' | ... | 'newsection';

// 3. Enregistrer dans le router
// src/components/bureau-canonical/index.tsx
```

### Ajouter un nouveau store
```typescript
// 1. Créer le store
// src/stores/new.store.ts

// 2. Exporter depuis index
// src/stores/index.ts
export * from './new.store';
```

---

## 🔒 Sécurité

- **Pas de secrets dans le code**
- **Tokens stockés en mémoire uniquement**
- **Checkpoints obligatoires pour actions sensibles**
- **Audit trail de toutes les actions**

---

**CHE·NU™** — Governed Intelligence Operating System
