# 🤖 CHE·NU™ V75 — AGENT PARALLÈLE BRIEFING

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    MISSION: CONNECTER V75 AU BACKEND                                ║
║                                                                                      ║
║                    Agent Parallèle | Janvier 2026                                   ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

**CE DOCUMENT EST AUTONOME.** Tu n'as pas besoin du code complet pour commencer.

---

## 🎯 TA MISSION

**Transformer V75 de MAQUETTE → APPLICATION PRODUCTION**

### Problème Actuel
- 8 pages UI magnifiques
- **MAIS** 0% connectées au backend
- Toutes les données sont MOCK (fausses)
- Aucun test

### Ton Objectif
- Connecter TOUTES les pages aux APIs réelles
- Supprimer TOUS les MOCK_DATA
- Créer les hooks API avec TanStack Query
- S'assurer que l'auth fonctionne E2E

---

## 📋 CONTEXTE RAPIDE CHE·NU

### C'est quoi CHE·NU?
Un **Governed Intelligence Operating System** — système d'exploitation pour intelligence gouvernée.

### Principes CANON (NE JAMAIS VIOLER)
```
1. GOUVERNANCE > EXÉCUTION
2. Les HUMAINS prennent TOUTES les décisions
3. L'AI ILLUMINE, ne décide jamais
4. Thread = Source de vérité unique
5. 9 Sphères (Personal, Business, Government, Studio, Community, Social, Entertainment, My Team, Scholar)
```

### Stack Technique
```yaml
Frontend:
  - React 18 + TypeScript
  - TanStack Query (pour API)
  - Zustand (state management)
  - Vite (build)
  - Framer Motion (animations)

Backend:
  - Python 3.11 + FastAPI
  - PostgreSQL + Redis
  - JWT Auth
  - WebSocket

API:
  - Base URL: http://localhost:8000/api/v1
  - Auth: Bearer token JWT
```

---

## 📁 STRUCTURE V75 (CE QUI EXISTE)

```
CHENU_V75/
├── frontend/
│   ├── src/
│   │   ├── AppV72Enhanced.tsx      # Point d'entrée (routes)
│   │   ├── layouts/
│   │   │   └── LayoutV72.tsx       # Layout principal
│   │   ├── pages/
│   │   │   ├── DashboardV72.tsx    # 🔴 MOCK - À connecter
│   │   │   ├── ThreadsPageV72.tsx  # 🔴 MOCK - À connecter
│   │   │   ├── AgentsPageV72.tsx   # 🔴 MOCK - À connecter
│   │   │   ├── NovaPageV72.tsx     # 🔴 MOCK - À connecter
│   │   │   ├── GovernancePageV72.tsx # 🔴 MOCK - À connecter
│   │   │   ├── DecisionPointsPageV72.tsx # 🔴 MOCK - À connecter
│   │   │   ├── SpherePageV72.tsx   # 🔴 MOCK - À connecter
│   │   │   └── XRPageV72.tsx       # 🔴 MOCK - À connecter
│   │   ├── components/
│   │   │   ├── sphere/             # SphereGrid
│   │   │   ├── dashboard/          # DashboardStatsWidget
│   │   │   ├── agents/             # AgentCard, AgentGrid
│   │   │   ├── notifications/      # NotificationCenter
│   │   │   └── search/             # GlobalSearchV72
│   │   ├── stores/
│   │   │   ├── auth.store.ts       # ✅ Existe
│   │   │   ├── thread.store.ts     # ✅ Existe
│   │   │   ├── agent.store.ts      # ✅ Existe
│   │   │   └── ... (15 stores)
│   │   ├── services/
│   │   │   ├── api.ts              # ⚠️ URL incorrecte
│   │   │   ├── api-client.ts       # ⚠️ URL incorrecte
│   │   │   └── api.client.ts       # ⚠️ URL incorrecte
│   │   ├── hooks/
│   │   │   └── ... (64 hooks)
│   │   └── types/
│   │       └── ... (36 fichiers)
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── api/v1/routes/
│   │   │   ├── auth_routes.py      # ✅ Existe
│   │   │   ├── thread_routes.py    # ✅ Existe
│   │   │   ├── agent_routes.py     # ✅ Existe
│   │   │   ├── governance_routes.py # ✅ Existe
│   │   │   ├── nova_routes.py      # ✅ Existe
│   │   │   ├── sphere_routes.py    # ✅ Existe
│   │   │   └── xr_routes.py        # ✅ Existe
│   │   ├── services/               # 21 services
│   │   ├── models/                 # 7 models
│   │   └── core/
│   │       ├── config.py
│   │       ├── database.py
│   │       ├── security.py
│   │       └── redis.py
│   └── requirements.txt
│
└── docs/
```

---

## 🔴 PROBLÈME #1: URLs API INCOHÉRENTES

### État Actuel (3 URLs différentes!)
```typescript
// frontend/src/services/api-client.ts
baseUrl: 'http://localhost:3000/api'  // ❌ FAUX

// frontend/src/services/api.client.ts
baseUrl: 'http://localhost:8000/api/v1'  // ✅ CORRECT

// frontend/src/services/api.ts
API_BASE = 'http://localhost:8080/api/v1'  // ❌ FAUX
```

### Solution À Implémenter
```typescript
// CRÉER: frontend/src/config/api.config.ts
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  VERSION: 'v1',
  get FULL_URL() {
    return `${this.BASE_URL}/api/${this.VERSION}`;
  },
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/auth/login',
      REGISTER: '/auth/register',
      REFRESH: '/auth/refresh',
      LOGOUT: '/auth/logout',
    },
    THREADS: '/threads',
    AGENTS: '/agents',
    SPHERES: '/spheres',
    GOVERNANCE: '/governance',
    NOVA: '/nova',
    XR: '/xr',
    DASHBOARD: '/dashboard',
  }
};
```

---

## 🔴 PROBLÈME #2: PAGES EN MOCK

### Exemple: DashboardV72.tsx (AVANT)
```typescript
// frontend/src/pages/DashboardV72.tsx - ÉTAT ACTUEL

// Ligne ~50 - DONNÉES FAKE
const MOCK_STATS: DashboardStats = {
  decisions: {
    total: 12,
    byAging: { GREEN: 5, YELLOW: 4, RED: 2, BLINK: 1 },
  },
  threads: {
    active: 7,
    total: 23,
  },
  // ... etc
};

// Ligne ~150 - UTILISATION DU MOCK
<DashboardStatsWidget
  stats={MOCK_STATS}  // ❌ DONNÉES FAKE!
  onStatClick={handleStatClick}
/>
```

### Solution À Implémenter (APRÈS)
```typescript
// frontend/src/pages/DashboardV72.tsx - À MODIFIER

// 1. Importer le hook API
import { useDashboardStats } from '../hooks/api/useDashboardStats';

// 2. Utiliser le hook
function DashboardV72() {
  const { data: stats, isLoading, error } = useDashboardStats();
  
  // 3. Gérer loading
  if (isLoading) {
    return <DashboardSkeleton />;
  }
  
  // 4. Gérer erreur
  if (error) {
    return <DashboardError error={error} onRetry={() => refetch()} />;
  }
  
  // 5. Afficher données réelles
  return (
    <DashboardStatsWidget
      stats={stats}  // ✅ DONNÉES RÉELLES!
      onStatClick={handleStatClick}
    />
  );
}
```

---

## 📝 TÂCHES À FAIRE

### PHASE 1: Configuration API (Jour 1)

```markdown
□ Créer frontend/src/config/api.config.ts
□ Créer frontend/src/services/apiClient.ts (client unifié)
□ Supprimer/archiver les 3 anciens fichiers API
□ Mettre à jour .env.example avec VITE_API_URL
```

### PHASE 2: Créer Hooks API (Jours 2-3)

```markdown
□ Créer frontend/src/hooks/api/useDashboardStats.ts
□ Créer frontend/src/hooks/api/useThreads.ts
□ Créer frontend/src/hooks/api/useAgents.ts
□ Créer frontend/src/hooks/api/useGovernance.ts
□ Créer frontend/src/hooks/api/useNova.ts
□ Créer frontend/src/hooks/api/useSpheres.ts
□ Créer frontend/src/hooks/api/useXR.ts
□ Créer frontend/src/hooks/api/index.ts (barrel export)
```

### PHASE 3: Connecter Pages (Jours 3-5)

```markdown
□ Modifier DashboardV72.tsx - Supprimer MOCK_STATS
□ Modifier ThreadsPageV72.tsx - Supprimer MOCK
□ Modifier AgentsPageV72.tsx - Supprimer MOCK
□ Modifier GovernancePageV72.tsx - Supprimer 18 MOCK
□ Modifier DecisionPointsPageV72.tsx - Supprimer MOCK
□ Modifier NovaPageV72.tsx - Connecter API
□ Modifier SpherePageV72.tsx - Connecter API
□ Modifier XRPageV72.tsx - Connecter API
```

### PHASE 4: Error Handling (Jour 5)

```markdown
□ Créer ErrorBoundary component
□ Créer Skeleton components pour loading
□ Créer Toast notifications
□ Ajouter retry logic sur erreurs
```

---

## 🛠️ CODE À CRÉER

### 1. API Client Unifié

```typescript
// frontend/src/services/apiClient.ts
import { API_CONFIG } from '../config/api.config';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

class ApiClient {
  private baseUrl = API_CONFIG.FULL_URL;

  private getToken(): string | null {
    // Récupérer token depuis localStorage ou store
    return localStorage.getItem('chenu_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new ApiError(response.status, errorText);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  // GET
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  // POST
  async post<T>(endpoint: string, data?: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // PUT
  async put<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // PATCH
  async patch<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // DELETE
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();
export { ApiError };
```

### 2. Hook Dashboard Stats

```typescript
// frontend/src/hooks/api/useDashboardStats.ts
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../services/apiClient';

export interface DashboardStats {
  decisions: {
    total: number;
    byAging: {
      GREEN: number;
      YELLOW: number;
      RED: number;
      BLINK: number;
    };
  };
  threads: {
    active: number;
    total: number;
  };
  agents: {
    hired: number;
    available: number;
  };
  tokens: {
    used: number;
    budget: number;
  };
  checkpoints: {
    pending: number;
    approved: number;
  };
  memory: {
    items: number;
    sizeKb: number;
  };
}

export function useDashboardStats() {
  return useQuery<DashboardStats>({
    queryKey: ['dashboard', 'stats'],
    queryFn: () => apiClient.get('/dashboard/stats'),
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Refetch every minute
  });
}
```

### 3. Hook Threads

```typescript
// frontend/src/hooks/api/useThreads.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../services/apiClient';

export interface Thread {
  id: string;
  title: string;
  founding_intent: string;
  sphere_id: string;
  status: 'active' | 'paused' | 'archived' | 'completed';
  created_at: string;
  updated_at: string;
  event_count: number;
}

export interface CreateThreadInput {
  title: string;
  founding_intent: string;
  sphere_id: string;
}

// Liste des threads
export function useThreads(sphereId?: string) {
  return useQuery<Thread[]>({
    queryKey: ['threads', { sphereId }],
    queryFn: () => {
      const params = sphereId ? `?sphere_id=${sphereId}` : '';
      return apiClient.get(`/threads${params}`);
    },
  });
}

// Thread unique
export function useThread(threadId: string) {
  return useQuery<Thread>({
    queryKey: ['threads', threadId],
    queryFn: () => apiClient.get(`/threads/${threadId}`),
    enabled: !!threadId,
  });
}

// Créer thread
export function useCreateThread() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateThreadInput) => 
      apiClient.post<Thread>('/threads', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threads'] });
    },
  });
}

// Mettre à jour thread
export function useUpdateThread() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Thread> }) =>
      apiClient.patch<Thread>(`/threads/${id}`, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['threads'] });
      queryClient.invalidateQueries({ queryKey: ['threads', id] });
    },
  });
}

// Archiver thread
export function useArchiveThread() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id: string) =>
      apiClient.post(`/threads/${id}/archive`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threads'] });
    },
  });
}
```

### 4. Hook Agents

```typescript
// frontend/src/hooks/api/useAgents.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../services/apiClient';

export interface Agent {
  id: string;
  name: string;
  name_fr: string;
  level: 'L0' | 'L1' | 'L2' | 'L3';
  domain: string;
  sphere_id?: string;
  description: string;
  description_fr: string;
  avatar: string;
  capabilities: string[];
  base_cost: number;
  is_system: boolean;
  is_hireable: boolean;
  is_hired?: boolean;
}

// Liste des agents
export function useAgents(filters?: { sphereId?: string; level?: string }) {
  return useQuery<Agent[]>({
    queryKey: ['agents', filters],
    queryFn: () => {
      const params = new URLSearchParams();
      if (filters?.sphereId) params.append('sphere_id', filters.sphereId);
      if (filters?.level) params.append('level', filters.level);
      const queryString = params.toString();
      return apiClient.get(`/agents${queryString ? `?${queryString}` : ''}`);
    },
  });
}

// Agents engagés
export function useHiredAgents() {
  return useQuery<Agent[]>({
    queryKey: ['agents', 'hired'],
    queryFn: () => apiClient.get('/agents/hired'),
  });
}

// Engager un agent
export function useHireAgent() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (agentId: string) =>
      apiClient.post(`/agents/${agentId}/hire`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
  });
}

// Libérer un agent
export function useFireAgent() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (agentId: string) =>
      apiClient.post(`/agents/${agentId}/fire`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['agents'] });
    },
  });
}
```

### 5. Hook Governance

```typescript
// frontend/src/hooks/api/useGovernance.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../services/apiClient';

export interface Checkpoint {
  id: string;
  type: 'governance' | 'cost' | 'identity' | 'sensitive';
  status: 'pending' | 'approved' | 'rejected';
  title: string;
  description: string;
  thread_id?: string;
  agent_id?: string;
  created_at: string;
  resolved_at?: string;
  resolved_by?: string;
}

// Liste des checkpoints
export function useCheckpoints(status?: 'pending' | 'approved' | 'rejected') {
  return useQuery<Checkpoint[]>({
    queryKey: ['governance', 'checkpoints', { status }],
    queryFn: () => {
      const params = status ? `?status=${status}` : '';
      return apiClient.get(`/governance/checkpoints${params}`);
    },
  });
}

// Checkpoints en attente
export function usePendingCheckpoints() {
  return useCheckpoints('pending');
}

// Approuver checkpoint
export function useApproveCheckpoint() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (checkpointId: string) =>
      apiClient.post(`/governance/checkpoints/${checkpointId}/approve`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['governance', 'checkpoints'] });
    },
  });
}

// Rejeter checkpoint
export function useRejectCheckpoint() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, reason }: { id: string; reason: string }) =>
      apiClient.post(`/governance/checkpoints/${id}/reject`, { reason }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['governance', 'checkpoints'] });
    },
  });
}
```

---

## 📌 CONVENTIONS À RESPECTER

### Nommage
```typescript
// Hooks API: use{Resource}{Action}
useThreads()
useCreateThread()
useThread(id)

// Query Keys: [resource, filters | id]
['threads']
['threads', { sphereId: '123' }]
['threads', '456']

// Fichiers: camelCase.ts
useDashboardStats.ts
useThreads.ts
```

### Structure Hook
```typescript
// Toujours exporter l'interface des données
export interface ResourceData { ... }

// Toujours retourner le résultat de useQuery/useMutation
export function useResource() {
  return useQuery<ResourceData>({ ... });
}
```

### Error Handling
```typescript
// Dans les pages, toujours gérer:
const { data, isLoading, error, refetch } = useResource();

if (isLoading) return <Skeleton />;
if (error) return <Error onRetry={refetch} />;
return <Component data={data} />;
```

---

## ⚠️ RÈGLES ABSOLUES

```
1. NE JAMAIS laisser de MOCK_DATA en production
2. NE JAMAIS hardcoder une URL API
3. TOUJOURS utiliser le token JWT pour les routes protégées
4. TOUJOURS gérer loading + error states
5. TOUJOURS invalider les queries après mutations
6. NE JAMAIS faire d'appels API dans les composants (utiliser hooks)
```

---

## 🔗 ENDPOINTS BACKEND (EXISTANTS)

```yaml
Auth:
  POST /api/v1/auth/login
  POST /api/v1/auth/register
  POST /api/v1/auth/refresh
  POST /api/v1/auth/logout

Threads:
  GET    /api/v1/threads
  GET    /api/v1/threads/:id
  POST   /api/v1/threads
  PATCH  /api/v1/threads/:id
  POST   /api/v1/threads/:id/archive

Agents:
  GET    /api/v1/agents
  GET    /api/v1/agents/hired
  POST   /api/v1/agents/:id/hire
  POST   /api/v1/agents/:id/fire

Governance:
  GET    /api/v1/governance/checkpoints
  POST   /api/v1/governance/checkpoints/:id/approve
  POST   /api/v1/governance/checkpoints/:id/reject

Spheres:
  GET    /api/v1/spheres
  GET    /api/v1/spheres/:id

Nova:
  GET    /api/v1/nova/status
  POST   /api/v1/nova/query

XR:
  GET    /api/v1/xr/environments
  POST   /api/v1/xr/generate

Dashboard:
  GET    /api/v1/dashboard/stats
```

---

## 📊 CHECKLIST DE VÉRIFICATION

### Avant de commit
```markdown
□ Aucun MOCK_DATA dans le code
□ Tous les useQuery ont queryKey unique
□ Toutes les mutations invalident les queries appropriées
□ Loading states implémentés
□ Error states implémentés
□ Types TypeScript corrects
□ Pas de console.log restants
```

### Test manuel
```markdown
□ Login fonctionne
□ Dashboard charge des données
□ Navigation entre pages sans erreur
□ Créer un thread fonctionne
□ Engager un agent fonctionne
□ Approuver un checkpoint fonctionne
```

---

## 💬 COMMUNICATION

**Si tu as besoin du code source:**
- Demande le ZIP CHENU_V75_FINAL.zip (82 MB)
- Ou demande des fichiers spécifiques

**Si tu bloques:**
- Note le problème précisément
- Continue sur une autre tâche
- On synchronisera

**Quand tu termines une tâche:**
- Documente ce qui a été fait
- Liste les fichiers modifiés/créés
- Note les problèmes rencontrés

---

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    MISSION: MOCK → API RÉELLE                                       ║
║                                                                                      ║
║                    8 pages à connecter                                              ║
║                    7 hooks API à créer                                              ║
║                    1 client API unifié                                              ║
║                                                                                      ║
║                    "ON LÂCHE PAS!" 💪                                               ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

---

**Dernière mise à jour:** 8 Janvier 2026  
**Version:** V75  
**Status:** EN COURS DE CONNEXION

© 2026 CHE·NU™ — All Rights Reserved
