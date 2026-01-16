# 🔄 CHE·NU™ - CI/CD PIPELINE

**Version:** V45  
**Status:** POST-MVP ENHANCEMENTS – RECOMMENDED BY GROK  

---

## 🎯 PIPELINE OVERVIEW

```
┌─────────────┐
│ Git Push    │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────────┐
│ CI: Continuous Integration                      │
│  1. Lint (ESLint, Flake8)                       │
│  2. Type Check (TypeScript, mypy)               │
│  3. Unit Tests (Jest, pytest)                   │
│  4. Integration Tests                           │
│  5. E2E Tests (Playwright)                      │
│  6. Security Scan (Snyk, Trivy)                 │
│  7. Build (Vite, Docker)                        │
│  8. Coverage Report (>75%)                      │
└──────┬──────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────┐
│ CD: Continuous Deployment                       │
│  Staging (auto on develop)                      │
│    ↓                                             │
│  Production (manual on main + tag)              │
└──────────────────────────────────────────────────┘
```

---

## 🔧 GITHUB ACTIONS

### Workflow: CI
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Backend lint
      - name: Lint Python
        run: |
          pip install flake8 black mypy
          flake8 backend/
          black --check backend/
          mypy backend/
      
      # Frontend lint
      - name: Lint TypeScript
        run: |
          cd frontend
          npm ci
          npm run lint
          npm run type-check
  
  test-backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379
        run: |
          cd backend
          pytest --cov=. --cov-report=xml --cov-report=term
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          fail_ci_if_error: true
          flags: backend
          threshold: 75%
  
  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage --watchAll=false
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./frontend/coverage/coverage-final.json
          fail_ci_if_error: true
          flags: frontend
          threshold: 70%
  
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Playwright
        run: |
          cd frontend
          npm ci
          npx playwright install --with-deps
      
      - name: Run E2E tests
        run: |
          cd frontend
          npm run test:e2e
      
      - name: Upload Playwright report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: frontend/playwright-report/
  
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      
      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'
  
  build:
    needs: [lint, test-backend, test-frontend, e2e, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker images
        run: |
          docker build -f Dockerfile.backend -t chenu-backend .
          docker build -f Dockerfile.frontend -t chenu-frontend .
      
      - name: Push to registry
        if: github.ref == 'refs/heads/main'
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push chenu-backend:latest
          docker push chenu-frontend:latest
```

### Workflow: CD Staging
```yaml
# .github/workflows/cd-staging.yml
name: CD Staging

on:
  push:
    branches: [develop]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy Backend (Railway)
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_STAGING_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up --environment staging
      
      - name: Deploy Frontend (Vercel)
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: |
          npm install -g vercel
          cd frontend
          vercel --prod --token=$VERCEL_TOKEN --yes --env=staging
      
      - name: Run smoke tests
        run: |
          sleep 30  # Wait for deployment
          curl -f https://api-staging.chenu.com/health || exit 1
          curl -f https://staging.chenu.com || exit 1
      
      - name: Notify team
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Staging deployment ${{ job.status }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Workflow: CD Production
```yaml
# .github/workflows/cd-production.yml
name: CD Production

on:
  release:
    types: [published]

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Database backup
        run: |
          ./scripts/backup/backup-db.sh
      
      - name: Deploy Backend
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_PRODUCTION_TOKEN }}
        run: |
          railway up --environment production
      
      - name: Deploy Frontend
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: |
          cd frontend
          vercel --prod --token=$VERCEL_TOKEN --yes
      
      - name: Health checks
        run: |
          ./scripts/monitoring/check-health.sh
      
      - name: Sentry release
        run: |
          sentry-cli releases new ${{ github.ref_name }}
          sentry-cli releases finalize ${{ github.ref_name }}
      
      - name: Notify success
        uses: 8398a7/action-slack@v3
        with:
          status: success
          text: '🚀 Production deployment v${{ github.ref_name }} successful!'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 🧪 TESTS AUTOMATISÉS

### Test Pyramid
```
    ╱────────╲
   ╱ E2E (10%) ╲          ~60 tests   (Playwright)
  ╱──────────────╲
 ╱ Integration   ╲       ~80 tests   (FastAPI TestClient, React Testing Library)
╱────(30%)────────╲
────────────────────
│  Unit  (60%)     │     ~170 tests  (pytest, Jest)
────────────────────
```

### Coverage Requirements
```yaml
# .codecov.yml
coverage:
  status:
    project:
      backend:
        target: 80%
        threshold: 2%
      frontend:
        target: 70%
        threshold: 2%
    patch:
      default:
        target: 75%
```

---

## 📊 MONITORING PRODUCTION

### Sentry Integration
```python
# backend/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    integrations=[FastApiIntegration()],
    environment=settings.ENVIRONMENT,
    release=settings.VERSION,
    traces_sample_rate=0.1,  # 10% traces
    profiles_sample_rate=0.1  # 10% profiles
)
```

### Prometheus Metrics
```python
# Exposed at /metrics
http_requests_total
http_request_duration_seconds
agent_executions_total
agent_tokens_used_total
database_connections_active
cache_hits_total
cache_misses_total
```

---

## 🚨 ALERTING

### PagerDuty Integration
```yaml
# Alerts configuration
alerts:
  - name: High error rate
    condition: error_rate > 1%
    duration: 5min
    severity: critical
    
  - name: High latency
    condition: latency_p95 > 1s
    duration: 3min
    severity: warning
    
  - name: Low availability
    condition: availability < 99.9%
    duration: 5min
    severity: critical
```

---

## 🔐 SECRETS MANAGEMENT

### GitHub Secrets
```
DOCKER_USERNAME
DOCKER_PASSWORD
RAILWAY_STAGING_TOKEN
RAILWAY_PRODUCTION_TOKEN
VERCEL_TOKEN
SNYK_TOKEN
SENTRY_DSN
SLACK_WEBHOOK
DATABASE_URL (production)
JWT_SECRET
STRIPE_SECRET_KEY
```

---

## 📅 DEPLOYMENT SCHEDULE

### Staging
- **Auto-deploy** on push to `develop`
- **Frequency:** Multiple times/day

### Production
- **Manual deploy** on release tag
- **Frequency:** Weekly (Tuesdays 10h UTC)
- **Maintenance window:** Tuesdays 09h-11h UTC

---

## 🔄 ROLLBACK PROCEDURE

```bash
# Automated rollback on failure
if [ "$(curl -s -o /dev/null -w '%{http_code}' https://api.chenu.com/health)" != "200" ]; then
  echo "Health check failed, rolling back..."
  railway rollback --environment production
  vercel rollback --yes
  
  # Alert team
  curl -X POST $SLACK_WEBHOOK \
    -d '{"text":"🚨 Production rollback triggered!"}'
fi
```

---

## ✅ QUALITY GATES

```yaml
# Required for merge to main
quality_gates:
  - All tests passing
  - Coverage ≥75%
  - No critical vulnerabilities (Snyk)
  - Code review approved (2+ reviewers)
  - Linting passed
  - Type checking passed
  - E2E tests passed
  - Build successful
```

---

*CHE·NU™ CI/CD Pipeline*  
***AUTOMATE. VALIDATE. DEPLOY.*** 🔄
