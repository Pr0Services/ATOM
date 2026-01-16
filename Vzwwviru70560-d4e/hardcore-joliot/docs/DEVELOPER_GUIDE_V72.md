# CHE·NU™ V72 — Documentation Développeur

<div align="center">

**Governed Intelligence Operating System**

*Architecture Technique & Guide d'Intégration*

</div>

---

## Table des Matières

1. [Architecture](#architecture)
2. [Stack Technique](#stack-technique)
3. [Structure du Projet](#structure-du-projet)
4. [Installation](#installation)
5. [API Reference](#api-reference)
6. [Composants V72](#composants-v72)
7. [Hooks](#hooks)
8. [State Management](#state-management)
9. [Tests](#tests)
10. [Déploiement](#déploiement)
11. [Conventions](#conventions)

---

## Architecture

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                        CHE·NU™ V72                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │  Frontend   │  │   Backend   │  │     Infrastructure      │ │
│  │  (React)    │◄─┤  (FastAPI)  │◄─┤  (Docker/PostgreSQL)    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│         │               │                    │                 │
│         ▼               ▼                    ▼                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Zustand   │  │    OPA      │  │    Redis / WebSocket    │ │
│  │   (State)   │  │ (Governance)│  │    (Real-time)          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Principes Architecturaux

1. **GOUVERNANCE > EXÉCUTION** — OPA valide toutes les actions sensibles
2. **READ-ONLY XR** — Interface XR séparée, lecture seule
3. **9 Sphères, 6 Sections** — Architecture fixe, non extensible
4. **Human-in-the-Loop** — Checkpoints pour actions critiques

---

## Stack Technique

### Frontend

| Technologie | Version | Usage |
|-------------|---------|-------|
| React | 18.x | UI Framework |
| TypeScript | 5.x | Type Safety |
| Vite | 5.x | Build Tool |
| React Router | 6.x | Routing |
| Zustand | 4.x | State Management |
| TanStack Query | 5.x | Server State |

### Backend

| Technologie | Version | Usage |
|-------------|---------|-------|
| Python | 3.11+ | Runtime |
| FastAPI | 0.100+ | API Framework |
| SQLAlchemy | 2.x | ORM |
| Alembic | 1.x | Migrations |
| OPA | Latest | Policy Governance |
| Redis | 7.x | Cache/PubSub |

### Infrastructure

| Technologie | Usage |
|-------------|-------|
| Docker | Containerization |
| PostgreSQL | Database |
| Nginx | Reverse Proxy |
| Terraform | IaC |

---

## Structure du Projet

```
AT-OM-main/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── v72/                 # Composants V72
│   │   │   │   ├── DashboardStatsWidget.tsx
│   │   │   │   ├── SphereGrid.tsx
│   │   │   │   ├── ThreadMaturityBadge.tsx
│   │   │   │   └── ...
│   │   │   ├── agents/
│   │   │   ├── actions/
│   │   │   ├── notifications/
│   │   │   └── search/
│   │   ├── pages/
│   │   │   ├── DashboardV72.tsx
│   │   │   ├── ThreadsPageV72.tsx
│   │   │   ├── NovaPageV72.tsx
│   │   │   ├── AgentsPageV72.tsx
│   │   │   ├── DecisionPointsPageV72.tsx
│   │   │   ├── GovernancePageV72.tsx
│   │   │   ├── SpherePageV72.tsx
│   │   │   └── XRPageV72.tsx
│   │   ├── hooks/
│   │   │   ├── useApiV72.ts
│   │   │   ├── useKeyboardShortcuts.ts
│   │   │   └── useSpheres.ts
│   │   ├── stores/
│   │   │   ├── auth.store.ts
│   │   │   └── app.store.ts
│   │   ├── styles/
│   │   │   ├── globalV72.css
│   │   │   ├── responsive.ts
│   │   │   └── animationsV72.ts
│   │   ├── data/
│   │   │   └── agents-catalog.ts    # 226 agents
│   │   └── services/
│   │       └── api.ts
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── governance/              # OPA policies
│   ├── requirements.txt
│   └── alembic/
├── scripts/
│   └── deploy-v72.sh
├── docs/
│   ├── USER_MANUAL_V72.md
│   └── DEVELOPER_GUIDE_V72.md
└── docker-compose.yml
```

---

## Installation

### Prérequis

- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+ (ou via Docker)

### Installation Locale

```bash
# Clone
git clone https://github.com/your-org/chenu.git
cd chenu

# Frontend
cd frontend
npm install
cp .env.example .env.local
npm run dev

# Backend (dans un autre terminal)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

# Ou avec Docker
docker-compose up -d
```

### Variables d'Environnement

#### Frontend (.env.local)

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/ws
VITE_DEV_AUTH_BYPASS=true
```

#### Backend (.env)

```env
DATABASE_URL=postgresql://chenu:chenu@localhost:5432/chenu
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
OPA_URL=http://localhost:8181
```

---

## API Reference

### Endpoints Principaux

#### Auth

```
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

#### Spheres

```
GET  /api/v1/spheres
GET  /api/v1/spheres/:id
GET  /api/v1/spheres/:id/stats
```

#### Threads

```
GET    /api/v1/threads
POST   /api/v1/threads
GET    /api/v1/threads/:id
PATCH  /api/v1/threads/:id
POST   /api/v1/threads/:id/archive
GET    /api/v1/threads/:id/events
```

#### Decisions

```
GET  /api/v1/decisions
GET  /api/v1/decisions/:id
POST /api/v1/decisions/make
POST /api/v1/decisions/:id/defer
GET  /api/v1/decisions/stats
```

#### Agents

```
GET  /api/v1/agents
GET  /api/v1/agents/:id
POST /api/v1/agents/hire
POST /api/v1/agents/:id/dismiss
POST /api/v1/agents/suggestions
GET  /api/v1/agents/stats
```

#### Checkpoints (Governance)

```
GET  /api/v1/checkpoints
GET  /api/v1/checkpoints/pending
POST /api/v1/checkpoints/resolve
```

#### Nova

```
POST /api/v1/nova/chat
GET  /api/v1/nova/history
```

### WebSocket Events

```typescript
// Connect
ws://localhost:8000/ws?token=<jwt>

// Events
{ type: 'checkpoint_update', data: Checkpoint }
{ type: 'decision_update', data: Decision }
{ type: 'notification', data: Notification }
{ type: 'agent_action', data: AgentAction }
```

---

## Composants V72

### DashboardStatsWidget

```tsx
import { DashboardStatsWidget } from '@/components/v72';

<DashboardStatsWidget
  decisions={5}
  threads={12}
  agents={4}
  checkpoints={2}
  governanceScore={95}
  onStatClick={(type) => navigate(`/${type}`)}
/>
```

### SphereGrid

```tsx
import { SphereGrid } from '@/components/v72';

<SphereGrid
  spheres={SPHERES}
  onSphereClick={(id) => navigate(`/sphere/${id}`)}
/>
```

### ThreadMaturityBadge

```tsx
import { ThreadMaturityBadge } from '@/components/v72';

<ThreadMaturityBadge
  level="GROWING"
  score={65}
  showProgress
/>
```

### AgentCardV72

```tsx
import { AgentCardV72 } from '@/components/agents';

<AgentCardV72
  agent={agent}
  onHire={() => hireAgent(agent.id)}
  isHired={agent.is_hired}
/>
```

### CheckpointCard

```tsx
import { CheckpointCard } from '@/components/governance';

<CheckpointCard
  checkpoint={checkpoint}
  onApprove={() => resolveCheckpoint(id, 'approve')}
  onReject={() => resolveCheckpoint(id, 'reject')}
/>
```

---

## Hooks

### useApiV72

```tsx
import { useApi, useMutation } from '@/hooks/useApiV72';

// GET request with caching
const { data, isLoading, error, refetch } = useApi<Thread[]>('/threads', {
  cacheKey: 'threads',
  refetchInterval: 30000,
});

// POST/PUT/DELETE mutation
const { mutate, isLoading } = useMutation<Thread, CreateThreadRequest>(
  '/threads',
  'POST',
  { invalidateCache: ['threads'] }
);
```

### Specific Hooks

```tsx
// Dashboard
const { data: stats } = useDashboardStats();

// Threads
const { data: threads } = useThreads({ sphere_id: 'business' });
const { mutate: createThread } = useCreateThread();

// Decisions
const { data: decisions } = useDecisions({ aging_level: 'BLINK' });
const { mutate: makeDecision } = useMakeDecision();

// Agents
const { data: agents } = useAgents({ level: 2 });
const { mutate: hireAgent } = useHireAgent();

// Governance
const { data: metrics } = useGovernanceMetrics();
const { data: signals } = useGovernanceSignals(false); // unresolved only

// Nova
const { messages, send, isLoading } = useNovaChat();
```

### useKeyboardShortcuts

```tsx
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

useKeyboardShortcuts({
  onAction: (action) => {
    switch (action) {
      case 'search': setSearchOpen(true); break;
      case 'nova': navigate('/nova'); break;
      case 'new-thread': setModalOpen(true); break;
    }
  },
});
```

### useBreakpoint (Responsive)

```tsx
import { useBreakpoint, useIsMobile } from '@/styles/responsive';

const breakpoint = useBreakpoint(); // 'xs' | 'sm' | 'md' | 'lg' | 'xl'
const isMobile = useIsMobile(); // boolean
```

---

## State Management

### Auth Store (Zustand)

```tsx
import { useAuthStore } from '@/stores/auth.store';

// Usage
const { user, isAuthenticated, login, logout } = useAuthStore();

// Store definition
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}
```

### App Store

```tsx
import { useAppStore } from '@/stores/app.store';

const { 
  activeSphere,
  setActiveSphere,
  notifications,
  addNotification,
  dismissNotification,
} = useAppStore();
```

---

## Tests

### Exécuter les Tests

```bash
# Unit tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Specific file
npm test -- v72.pages.test.tsx
```

### Structure des Tests

```tsx
// v72.pages.test.tsx
describe('DashboardV72', () => {
  test('renders dashboard with greeting', async () => {
    renderWithRouter(<DashboardV72 />);
    await waitFor(() => {
      expect(screen.getByText(/Bonjour|Bon après-midi/i)).toBeInTheDocument();
    });
  });

  test('navigates to sphere on click', async () => {
    renderWithRouter(<DashboardV72 />);
    fireEvent.click(screen.getByText('Personnel'));
    expect(mockNavigate).toHaveBeenCalledWith('/sphere/personal');
  });
});
```

### Mocking

```tsx
// Mock API
jest.mock('@/hooks/useApiV72', () => ({
  useDashboardStats: () => ({
    data: { decisions_pending: 5, threads_active: 12 },
    isLoading: false,
  }),
}));

// Mock Router
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));
```

---

## Déploiement

### Script de Déploiement

```bash
# Production
./scripts/deploy-v72.sh --env production

# Staging
./scripts/deploy-v72.sh --env staging

# Skip build (images already built)
./scripts/deploy-v72.sh --skip-build

# Rollback
./scripts/deploy-v72.sh --rollback
```

### Docker Compose

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d

# Logs
docker-compose logs -f api

# Scale
docker-compose up -d --scale api=3
```

### Health Checks

```bash
# API
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000

# Database
docker-compose exec db pg_isready -U chenu
```

---

## Conventions

### Code Style

```typescript
// Composants: PascalCase
export const MyComponent: React.FC<Props> = () => {};

// Hooks: camelCase avec préfixe "use"
export function useMyHook() {}

// Types: PascalCase
interface MyComponentProps {}
type MyType = 'a' | 'b';

// Constants: SCREAMING_SNAKE_CASE
const MAX_ITEMS = 100;
const API_BASE_URL = '';

// Files: kebab-case ou PascalCase pour composants
my-utils.ts
MyComponent.tsx
```

### Commits

```
feat(v72): add dashboard stats widget
fix(agents): correct level badge color
docs: update user manual
refactor(api): simplify hooks
test: add decision page tests
chore: update dependencies
```

### Pull Requests

1. Une PR = une fonctionnalité ou fix
2. Tests obligatoires pour nouvelles fonctionnalités
3. Documentation mise à jour si nécessaire
4. Review obligatoire avant merge

---

## Ressources

- [React Documentation](https://react.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [OPA Documentation](https://www.openpolicyagent.org/docs)
- [Zustand Documentation](https://docs.pmnd.rs/zustand)

---

<div align="center">

**CHE·NU™ V72 — Developer Guide**

*GOUVERNANCE > EXÉCUTION*

</div>
