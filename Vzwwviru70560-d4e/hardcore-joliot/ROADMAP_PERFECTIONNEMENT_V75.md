# 🚀 CHE·NU™ V75 → PRODUCTION — ROADMAP DE PERFECTIONNEMENT

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    ROADMAP: MAQUETTE → APPLICATION PRODUCTION                       ║
║                                                                                      ║
║                    Objectif: 500 Utilisateurs en 4 Semaines                         ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

---

## 📊 VUE D'ENSEMBLE

| Phase | Durée | Focus | Livrable |
|-------|-------|-------|----------|
| Phase 1 | 5 jours | Connexion API | Frontend connecté |
| Phase 2 | 5 jours | Tests & Auth | Tests E2E passent |
| Phase 3 | 4 jours | Stabilisation | Error handling |
| Phase 4 | 4 jours | Production | Deploy + Beta |
| **Total** | **18 jours** | - | **500 Users Ready** |

---

# 📅 PHASE 1: CONNEXION BACKEND (5 Jours)

## Objectif
Connecter TOUTES les pages aux APIs réelles et supprimer les MOCK.

---

## Jour 1: Configuration API Unifiée

### 1.1 Unifier les URLs API

**Problème actuel:**
```typescript
// 3 URLs différentes dans le code!
'http://localhost:3000/api'      // api-client.ts
'http://localhost:8000/api/v1'   // api.client.ts  
'http://localhost:8080/api/v1'   // api.ts
```

**Solution:**
```typescript
// src/config/api.config.ts
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  API_VERSION: 'v1',
  get FULL_URL() {
    return `${this.BASE_URL}/api/${this.API_VERSION}`;
  }
};
```

### 1.2 Créer API Client Unifié

```typescript
// src/services/apiClient.ts
import { API_CONFIG } from '../config/api.config';
import { useAuthStore } from '../stores/auth.store';

class ApiClient {
  private baseUrl = API_CONFIG.FULL_URL;

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = useAuthStore.getState().token;
    
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new ApiError(response.status, await response.text());
    }

    return response.json();
  }

  // GET
  get<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  // POST
  post<T>(endpoint: string, data: unknown) {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // PUT
  put<T>(endpoint: string, data: unknown) {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // DELETE
  delete<T>(endpoint: string) {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();
```

---

## Jour 2: Connecter DashboardV72

### 2.1 Créer Hooks API Dashboard

```typescript
// src/hooks/api/useDashboardStats.ts
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../services/apiClient';

interface DashboardStats {
  decisions: { total: number; byAging: Record<string, number> };
  threads: { active: number; total: number };
  agents: { hired: number; available: number };
  tokens: { used: number; budget: number };
  checkpoints: { pending: number; approved: number };
  memory: { items: number; sizeKb: number };
}

export function useDashboardStats() {
  return useQuery<DashboardStats>({
    queryKey: ['dashboard', 'stats'],
    queryFn: () => apiClient.get('/dashboard/stats'),
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // 1 minute
  });
}
```

### 2.2 Modifier DashboardV72.tsx

```typescript
// AVANT (MOCK)
const MOCK_STATS: DashboardStats = { ... };
// ...
<DashboardStatsWidget stats={MOCK_STATS} />

// APRÈS (API RÉELLE)
import { useDashboardStats } from '../hooks/api/useDashboardStats';

function DashboardV72() {
  const { data: stats, isLoading, error } = useDashboardStats();
  
  if (isLoading) return <DashboardSkeleton />;
  if (error) return <DashboardError error={error} />;
  
  return (
    <DashboardStatsWidget stats={stats} />
  );
}
```

---

## Jour 3: Connecter ThreadsPageV72 & AgentsPageV72

### 3.1 Hooks Threads

```typescript
// src/hooks/api/useThreads.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../../services/apiClient';

export function useThreads(filters?: ThreadFilters) {
  return useQuery({
    queryKey: ['threads', filters],
    queryFn: () => apiClient.get('/threads', { params: filters }),
  });
}

export function useCreateThread() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateThreadInput) => 
      apiClient.post('/threads', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['threads'] });
    },
  });
}
```

### 3.2 Hooks Agents

```typescript
// src/hooks/api/useAgents.ts
export function useAgents(sphereId?: string) {
  return useQuery({
    queryKey: ['agents', sphereId],
    queryFn: () => apiClient.get('/agents', { params: { sphereId } }),
  });
}

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
```

---

## Jour 4: Connecter Governance & Decisions

### 4.1 Hooks Governance

```typescript
// src/hooks/api/useGovernance.ts
export function useCheckpoints() {
  return useQuery({
    queryKey: ['governance', 'checkpoints'],
    queryFn: () => apiClient.get('/governance/checkpoints'),
  });
}

export function useApproveCheckpoint() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (checkpointId: string) => 
      apiClient.post(`/governance/checkpoints/${checkpointId}/approve`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['governance'] });
    },
  });
}
```

---

## Jour 5: Connecter Nova, Spheres, XR

### 5.1 Finaliser toutes les connexions

```typescript
// src/hooks/api/useNova.ts
export function useNovaStatus() { ... }
export function useNovaQuery() { ... }

// src/hooks/api/useSpheres.ts
export function useSpheres() { ... }
export function useSphereDetails(id: string) { ... }

// src/hooks/api/useXR.ts
export function useXREnvironments() { ... }
export function useGenerateXR() { ... }
```

### 5.2 Vérification Jour 5

```bash
# Checklist fin Phase 1
□ 0 occurrences MOCK_ dans les pages
□ Toutes pages utilisent useQuery
□ API Client unifié
□ Error states sur toutes pages
□ Loading states sur toutes pages
```

---

# 📅 PHASE 2: TESTS & AUTH (5 Jours)

## Jour 6-7: Auth E2E Complet

### 6.1 Implémenter Auth Complète

```typescript
// src/stores/auth.store.ts (amélioration)
interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterInput) => Promise<void>;
  logout: () => void;
  refreshAccessToken: () => Promise<void>;
  checkAuth: () => Promise<void>;
}
```

### 6.2 Tests Cypress Auth

```typescript
// cypress/e2e/auth.cy.ts
describe('Authentication', () => {
  it('should login successfully', () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type('test@chenu.com');
    cy.get('[data-cy=password]').type('password123');
    cy.get('[data-cy=submit]').click();
    cy.url().should('eq', Cypress.config().baseUrl + '/dashboard');
    cy.get('[data-cy=user-menu]').should('be.visible');
  });

  it('should show error on invalid credentials', () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type('wrong@email.com');
    cy.get('[data-cy=password]').type('wrongpassword');
    cy.get('[data-cy=submit]').click();
    cy.get('[data-cy=error-message]').should('be.visible');
  });

  it('should logout successfully', () => {
    cy.login(); // Custom command
    cy.get('[data-cy=user-menu]').click();
    cy.get('[data-cy=logout]').click();
    cy.url().should('include', '/login');
  });

  it('should redirect unauthenticated users', () => {
    cy.visit('/dashboard');
    cy.url().should('include', '/login');
  });
});
```

---

## Jour 8-9: Tests E2E Critiques

### 8.1 Tests Dashboard

```typescript
// cypress/e2e/dashboard.cy.ts
describe('Dashboard', () => {
  beforeEach(() => {
    cy.login();
    cy.visit('/dashboard');
  });

  it('should display stats widgets', () => {
    cy.get('[data-cy=stats-widget]').should('have.length', 6);
  });

  it('should display sphere grid', () => {
    cy.get('[data-cy=sphere-grid]').should('be.visible');
    cy.get('[data-cy=sphere-card]').should('have.length', 9);
  });

  it('should navigate to sphere on click', () => {
    cy.get('[data-cy=sphere-card]').first().click();
    cy.url().should('include', '/sphere/');
  });

  it('should open global search with Cmd+K', () => {
    cy.get('body').type('{cmd}k');
    cy.get('[data-cy=global-search]').should('be.visible');
  });
});
```

### 8.2 Tests Threads

```typescript
// cypress/e2e/threads.cy.ts
describe('Threads', () => {
  beforeEach(() => {
    cy.login();
    cy.visit('/threads');
  });

  it('should list threads', () => {
    cy.get('[data-cy=thread-list]').should('be.visible');
  });

  it('should create new thread', () => {
    cy.get('[data-cy=create-thread]').click();
    cy.get('[data-cy=thread-title]').type('Test Thread');
    cy.get('[data-cy=thread-intent]').type('Testing intent');
    cy.get('[data-cy=submit]').click();
    cy.get('[data-cy=thread-list]').should('contain', 'Test Thread');
  });

  it('should open thread detail', () => {
    cy.get('[data-cy=thread-item]').first().click();
    cy.url().should('include', '/thread/');
  });
});
```

---

## Jour 10: Tests Backend

### 10.1 Tests Python FastAPI

```python
# backend/tests/test_auth.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/login", json={
            "email": "test@chenu.com",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/auth/login", json={
            "email": "wrong@email.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_route_without_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/threads")
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_protected_route_with_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Login first
        login_response = await client.post("/api/v1/auth/login", json={
            "email": "test@chenu.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        # Access protected route
        response = await client.get(
            "/api/v1/threads",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
```

### 10.2 Tests Threads Backend

```python
# backend/tests/test_threads.py
@pytest.mark.asyncio
async def test_create_thread():
    async with AsyncClient(app=app, base_url="http://test") as client:
        token = await get_test_token(client)
        
        response = await client.post(
            "/api/v1/threads",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Test Thread",
                "founding_intent": "Testing",
                "sphere_id": "personal"
            }
        )
        assert response.status_code == 201
        assert response.json()["title"] == "Test Thread"

@pytest.mark.asyncio
async def test_list_threads():
    async with AsyncClient(app=app, base_url="http://test") as client:
        token = await get_test_token(client)
        
        response = await client.get(
            "/api/v1/threads",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
```

---

# 📅 PHASE 3: STABILISATION (4 Jours)

## Jour 11-12: Error Handling Global

### 11.1 Error Boundary

```typescript
// src/components/error/ErrorBoundary.tsx
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
    // Send to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

### 11.2 Toast Notifications

```typescript
// src/components/ui/Toast.tsx
import { create } from 'zustand';

interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
}

interface ToastStore {
  toasts: Toast[];
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
}

export const useToastStore = create<ToastStore>((set) => ({
  toasts: [],
  addToast: (toast) => {
    const id = crypto.randomUUID();
    set((state) => ({ toasts: [...state.toasts, { ...toast, id }] }));
    
    // Auto-remove after duration
    setTimeout(() => {
      set((state) => ({
        toasts: state.toasts.filter((t) => t.id !== id),
      }));
    }, toast.duration || 5000);
  },
  removeToast: (id) => {
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    }));
  },
}));
```

---

## Jour 13-14: Loading States & Skeletons

### 13.1 Skeleton Components

```typescript
// src/components/ui/Skeleton.tsx
export const Skeleton: React.FC<{ className?: string }> = ({ className }) => (
  <div
    className={`animate-pulse bg-white/5 rounded ${className}`}
    style={{ animationDuration: '1.5s' }}
  />
);

export const CardSkeleton = () => (
  <div className="p-4 border border-white/10 rounded-xl">
    <Skeleton className="h-6 w-3/4 mb-2" />
    <Skeleton className="h-4 w-full mb-2" />
    <Skeleton className="h-4 w-2/3" />
  </div>
);

export const DashboardSkeleton = () => (
  <div className="grid grid-cols-3 gap-4">
    {[...Array(6)].map((_, i) => (
      <CardSkeleton key={i} />
    ))}
  </div>
);
```

### 13.2 Retry Logic

```typescript
// src/hooks/useRetry.ts
import { useState, useCallback } from 'react';

export function useRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000
) {
  const [retryCount, setRetryCount] = useState(0);
  const [isRetrying, setIsRetrying] = useState(false);

  const execute = useCallback(async () => {
    setIsRetrying(true);
    
    for (let i = 0; i <= maxRetries; i++) {
      try {
        const result = await fn();
        setRetryCount(0);
        setIsRetrying(false);
        return result;
      } catch (error) {
        setRetryCount(i + 1);
        if (i < maxRetries) {
          await new Promise((r) => setTimeout(r, delay * (i + 1)));
        } else {
          setIsRetrying(false);
          throw error;
        }
      }
    }
  }, [fn, maxRetries, delay]);

  return { execute, retryCount, isRetrying };
}
```

---

# 📅 PHASE 4: PRODUCTION (4 Jours)

## Jour 15-16: Deployment Setup

### 15.1 Docker Production

```dockerfile
# Dockerfile.frontend
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 15.2 Docker Compose Production

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://chenu:${DB_PASSWORD}@db:5432/chenu
      - REDIS_URL=redis://redis:6379/0
      - JWT_SECRET_KEY=${JWT_SECRET}
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=chenu
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=chenu
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## Jour 17-18: Beta & Monitoring

### 17.1 Monitoring Setup

```typescript
// src/utils/monitoring.ts
export const monitoring = {
  trackError: (error: Error, context?: Record<string, unknown>) => {
    console.error('[ERROR]', error, context);
    // Send to Sentry/LogRocket
  },
  
  trackEvent: (event: string, data?: Record<string, unknown>) => {
    console.log('[EVENT]', event, data);
    // Send to analytics
  },
  
  trackPerformance: (metric: string, value: number) => {
    console.log('[PERF]', metric, value);
    // Send to monitoring
  },
};
```

### 17.2 Health Check Endpoint

```python
# backend/app/api/v1/routes/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.redis import redis_client

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Check database
    try:
        await db.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    # Check Redis
    try:
        await redis_client.ping()
        redis_status = "healthy"
    except Exception:
        redis_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded",
        "database": db_status,
        "redis": redis_status,
        "version": "75.0.0"
    }
```

---

# ✅ CHECKLIST FINALE

## Avant Beta (50 Users)

```
□ Auth E2E fonctionne
□ Dashboard charge données réelles
□ Navigation sans erreurs
□ 10 tests E2E passent
□ Error handling global
□ Loading states partout
□ Health check endpoint
```

## Avant 500 Users

```
□ Tous tests passent
□ Performance < 3s first load
□ Error rate < 1%
□ Uptime > 99%
□ Monitoring actif
□ Backup database
□ Documentation utilisateur
□ Support email configuré
```

---

# 📊 MÉTRIQUES DE SUCCÈS

| Métrique | Cible | Comment mesurer |
|----------|-------|-----------------|
| First Load | < 3s | Lighthouse |
| API Response | < 500ms | Backend logs |
| Error Rate | < 1% | Monitoring |
| Test Coverage | > 60% | Jest/Cypress |
| Uptime | > 99% | Health checks |
| User Satisfaction | > 4/5 | Feedback |

---

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    V75 → PRODUCTION EN 18 JOURS                                     ║
║                                                                                      ║
║    Phase 1: Connexion API ................ 5 jours                                  ║
║    Phase 2: Tests & Auth ................. 5 jours                                  ║
║    Phase 3: Stabilisation ................ 4 jours                                  ║
║    Phase 4: Production ................... 4 jours                                  ║
║                                                                                      ║
║    "DE MAQUETTE À APPLICATION PRODUCTION"                                           ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

---

**Généré:** 8 Janvier 2026  
**Agent:** Claude (Anthropic)  
**Objectif:** 500 Utilisateurs Ready

© 2026 CHE·NU™ — All Rights Reserved
