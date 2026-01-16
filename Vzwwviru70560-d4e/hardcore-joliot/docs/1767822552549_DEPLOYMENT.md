# 🚀 CHE·NU™ Deployment Guide

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                      CHE·NU™ — GOVERNED INTELLIGENCE OPERATING SYSTEM               ║
║                                                                                      ║
║                              DEPLOYMENT DOCUMENTATION                                ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Database Migrations](#database-migrations)
7. [Monitoring & Logging](#monitoring--logging)
8. [Security Considerations](#security-considerations)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools

```bash
# Docker & Docker Compose
docker --version  # >= 24.0
docker-compose --version  # >= 2.20

# Kubernetes (for K8s deployment)
kubectl version  # >= 1.28
kustomize version  # >= 5.0

# Node.js (for frontend development)
node --version  # >= 20.0
npm --version  # >= 10.0

# Python (for backend development)
python --version  # >= 3.11
```

### Clone Repository

```bash
git clone https://github.com/che-nu/chenu-platform.git
cd chenu-platform
```

---

## Local Development

### Quick Start

```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env with your configuration
nano .env

# 3. Start all services with dev tools
docker-compose --profile dev up -d

# 4. View logs
docker-compose logs -f

# 5. Access services
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Adminer (DB): http://localhost:8080
# Redis Commander: http://localhost:8081
```

### Development Workflow

```bash
# Start services
docker-compose up -d

# Run backend tests
docker-compose exec backend pytest

# Run migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Stop services
docker-compose down

# Stop and remove volumes (clean start)
docker-compose down -v
```

### Frontend Development (Hot Reload)

```bash
cd frontend
npm install
npm run dev  # Starts Vite dev server on port 5173
```

### Backend Development (Hot Reload)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Docker Deployment

### Build Images

```bash
# Build backend
docker build -f Dockerfile.backend -t chenu/backend:latest .

# Build frontend
cd frontend
docker build -t chenu/frontend:latest .
```

### Production Deployment

```bash
# Using production override
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale backend=3
```

### Health Checks

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend health
curl http://localhost:3000/health

# View container health
docker-compose ps
```

---

## Kubernetes Deployment

### Staging Deployment

```bash
# Create namespace
kubectl create namespace chenu-staging

# Apply staging configuration
kubectl apply -k k8s/overlays/staging

# Verify deployment
kubectl -n chenu-staging get all

# Check pod logs
kubectl -n chenu-staging logs -f deployment/staging-backend

# Port forward for local testing
kubectl -n chenu-staging port-forward svc/staging-backend 8000:8000
```

### Production Deployment

```bash
# Create namespace
kubectl create namespace chenu-production

# Create secrets (use sealed-secrets in production)
kubectl -n chenu-production create secret generic chenu-secrets \
  --from-literal=POSTGRES_PASSWORD=your_password \
  --from-literal=REDIS_PASSWORD=your_password \
  --from-literal=JWT_SECRET_KEY=your_secret \
  --from-literal=ANTHROPIC_API_KEY=your_key

# Apply production configuration
kubectl apply -k k8s/overlays/production

# Verify deployment
kubectl -n chenu-production get all

# Check rollout status
kubectl -n chenu-production rollout status deployment/prod-backend
```

### Scaling

```bash
# Manual scaling
kubectl -n chenu-production scale deployment/prod-backend --replicas=5

# View HPA status
kubectl -n chenu-production get hpa

# View pod distribution
kubectl -n chenu-production get pods -o wide
```

### Rolling Updates

```bash
# Update backend image
kubectl -n chenu-production set image deployment/prod-backend \
  backend=chenu/backend:v1.2.3

# Watch rollout
kubectl -n chenu-production rollout status deployment/prod-backend

# Rollback if needed
kubectl -n chenu-production rollout undo deployment/prod-backend
```

---

## Environment Configuration

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection string | `redis://:password@host:6379/0` |
| `JWT_SECRET_KEY` | 256-bit secret for JWT | `openssl rand -hex 32` |
| `ANTHROPIC_API_KEY` | Claude API key | `sk-ant-...` |

### R&D Compliance Flags

```bash
# These MUST be true in production (Rule #1, #5, #6)
CHENU_ENFORCE_HUMAN_GATES=true
CHENU_AUDIT_ALL_ACTIONS=true
CHENU_DISABLE_RANKING_ALGORITHMS=true
```

---

## Database Migrations

### Run Migrations

```bash
# Docker
docker-compose exec backend alembic upgrade head

# Kubernetes
kubectl -n chenu-production exec -it deployment/prod-backend -- alembic upgrade head
```

### Create New Migration

```bash
# Auto-generate from model changes
alembic revision --autogenerate -m "Add new table"

# Manual migration
alembic revision -m "Custom migration"
```

### Rollback

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123
```

---

## Monitoring & Logging

### Prometheus Metrics

Backend exposes metrics at `/metrics`:

```bash
# View metrics
curl http://localhost:8000/metrics
```

### Log Aggregation

```bash
# Docker logs
docker-compose logs -f backend

# Kubernetes logs
kubectl -n chenu-production logs -f -l app=backend --all-containers

# Structured logging (JSON)
kubectl -n chenu-production logs deployment/prod-backend | jq .
```

### Health Endpoints

| Endpoint | Description |
|----------|-------------|
| `/health` | Liveness check |
| `/health/ready` | Readiness check (includes DB/Redis) |
| `/metrics` | Prometheus metrics |

---

## Security Considerations

### Network Security

- All internal traffic uses Kubernetes NetworkPolicies
- Database/Redis only accessible from backend
- TLS enforced at ingress

### Container Security

- Non-root containers
- Read-only filesystem where possible
- Minimal base images (Alpine)
- No privilege escalation

### Secrets Management

```bash
# Use sealed-secrets for GitOps
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Or use external-secrets with Vault/AWS Secrets Manager
kubectl apply -f external-secret.yaml
```

### R&D Compliance Verification

The CI/CD pipeline automatically checks:
- No autonomous execution patterns (Rule #1)
- No bypass workflow patterns (Rule #3)
- No ranking algorithms in Social sphere (Rule #5)

---

## Troubleshooting

### Pod Not Starting

```bash
# Check pod events
kubectl -n chenu-production describe pod <pod-name>

# Check init container logs
kubectl -n chenu-production logs <pod-name> -c wait-for-postgres

# Check container logs
kubectl -n chenu-production logs <pod-name> -c backend
```

### Database Connection Issues

```bash
# Test database connectivity
kubectl -n chenu-production exec -it deployment/prod-backend -- \
  python -c "import asyncpg; print('OK')"

# Check database pod
kubectl -n chenu-production logs statefulset/prod-postgres
```

### Redis Connection Issues

```bash
# Test Redis connectivity
kubectl -n chenu-production exec -it deployment/prod-backend -- \
  redis-cli -h redis -a $REDIS_PASSWORD ping
```

### Common Issues

| Issue | Solution |
|-------|----------|
| `ImagePullBackOff` | Check image name and registry credentials |
| `CrashLoopBackOff` | Check logs for application errors |
| `Pending` pods | Check resource quotas and node capacity |
| `Connection refused` | Check NetworkPolicies and service endpoints |

---

## Quick Reference

### Docker Commands

```bash
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose logs -f        # Logs
docker-compose ps             # Status
docker-compose exec backend bash  # Shell
```

### Kubernetes Commands

```bash
kubectl apply -k k8s/overlays/production  # Deploy
kubectl get all -n chenu-production       # Status
kubectl logs -f deployment/prod-backend   # Logs
kubectl exec -it pod/xxx -- bash          # Shell
kubectl rollout restart deployment/xxx    # Restart
```

---

## Support

- **Documentation**: https://docs.che-nu.com
- **Issues**: https://github.com/che-nu/chenu-platform/issues
- **Email**: support@che-nu.com

---

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║              "GOVERNANCE > EXECUTION • HUMANS > AUTOMATION"                         ║
║                                                                                      ║
║                     CHE·NU™ — Built for Decades                                     ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

© 2026 CHE·NU™ — All Rights Reserved
