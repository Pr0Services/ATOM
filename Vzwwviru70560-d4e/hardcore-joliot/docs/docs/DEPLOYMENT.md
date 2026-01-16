# CHE·NU™ Deployment Guide

> Complete guide for deploying CHE·NU to production environments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Cloud Providers](#cloud-providers)
6. [Environment Variables](#environment-variables)
7. [Database Setup](#database-setup)
8. [SSL/TLS Configuration](#ssltls-configuration)
9. [Monitoring](#monitoring)
10. [Backup & Recovery](#backup--recovery)

---

## Prerequisites

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Storage | 20 GB | 50+ GB SSD |
| OS | Ubuntu 20.04+ | Ubuntu 22.04 LTS |

### Software Requirements

- **Node.js** 20.x LTS
- **Python** 3.11+
- **PostgreSQL** 15+
- **Redis** 7+
- **Docker** 24+
- **Docker Compose** 2.x

---

## Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/chenu/chenu.git
cd chenu

# Copy environment files
cp .env.example .env

# Start with Docker Compose
docker-compose up -d

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## Docker Deployment

### Build Images

```bash
# Build all images
docker-compose build

# Or build individually
docker build -t chenu/frontend:latest ./frontend
docker build -t chenu/backend:latest ./backend
```

### Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  frontend:
    image: chenu/frontend:latest
    restart: always
    environment:
      - VITE_API_URL=https://api.chenu.io
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  backend:
    image: chenu/backend:latest
    restart: always
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
```

### Run Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Kubernetes Deployment

### Namespace

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: chenu
```

### Deployment

```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chenu-backend
  namespace: chenu
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chenu-backend
  template:
    metadata:
      labels:
        app: chenu-backend
    spec:
      containers:
      - name: backend
        image: ghcr.io/chenu/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: chenu-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: chenu-secrets
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service

```yaml
# k8s/backend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: chenu-backend
  namespace: chenu
spec:
  selector:
    app: chenu-backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

### Ingress

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: chenu-ingress
  namespace: chenu
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - api.chenu.io
    - app.chenu.io
    secretName: chenu-tls
  rules:
  - host: api.chenu.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: chenu-backend
            port:
              number: 8000
  - host: app.chenu.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: chenu-frontend
            port:
              number: 3000
```

### Deploy to Kubernetes

```bash
# Apply configurations
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/

# Check status
kubectl get pods -n chenu
kubectl get services -n chenu
```

---

## Cloud Providers

### AWS (ECS + RDS + ElastiCache)

```bash
# Using AWS CDK or CloudFormation
# See infrastructure/aws/ directory
```

### Google Cloud (GKE + Cloud SQL)

```bash
# Create GKE cluster
gcloud container clusters create chenu-cluster \
  --num-nodes=3 \
  --machine-type=e2-standard-2 \
  --region=us-central1

# Deploy
kubectl apply -f k8s/
```

### Azure (AKS + Azure Database)

```bash
# Create AKS cluster
az aks create \
  --resource-group chenu-rg \
  --name chenu-cluster \
  --node-count 3 \
  --generate-ssh-keys
```

---

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/chenu
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis
REDIS_URL=redis://host:6379/0

# Security
SECRET_KEY=your-super-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=https://app.chenu.io,https://www.chenu.io

# AI (Optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Frontend (.env)

```bash
VITE_API_URL=https://api.chenu.io
VITE_WS_URL=wss://api.chenu.io
VITE_ENVIRONMENT=production
```

---

## Database Setup

### PostgreSQL

```sql
-- Create database
CREATE DATABASE chenu;

-- Create user
CREATE USER chenu_user WITH ENCRYPTED PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE chenu TO chenu_user;

-- Enable extensions
\c chenu
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

### Run Migrations

```bash
cd backend
alembic upgrade head
```

### Seed Data

```bash
python -m app.db.seed
```

---

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d api.chenu.io -d app.chenu.io

# Auto-renewal
sudo crontab -e
# Add: 0 0 * * * /usr/bin/certbot renew --quiet
```

### Nginx Configuration

```nginx
# /etc/nginx/sites-available/chenu
server {
    listen 80;
    server_name api.chenu.io app.chenu.io;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.chenu.io;

    ssl_certificate /etc/letsencrypt/live/api.chenu.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.chenu.io/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Monitoring

### Prometheus + Grafana

```yaml
# docker-compose.monitoring.yml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Health Endpoints

- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check
- `GET /health/live` - Liveness check
- `GET /metrics` - Prometheus metrics

---

## Backup & Recovery

### Database Backup

```bash
# Manual backup
pg_dump -U chenu_user -h localhost chenu > backup_$(date +%Y%m%d).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR=/backups
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U chenu_user chenu | gzip > $BACKUP_DIR/chenu_$DATE.sql.gz

# Keep last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
```

### Recovery

```bash
# Restore from backup
psql -U chenu_user -d chenu < backup_20240101.sql

# Or compressed
gunzip -c backup_20240101.sql.gz | psql -U chenu_user -d chenu
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Database connection failed | Check DATABASE_URL and network |
| WebSocket not connecting | Verify proxy WebSocket headers |
| 502 Bad Gateway | Check if backend is running |
| Slow queries | Add database indexes |
| High memory usage | Adjust container limits |

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Kubernetes logs
kubectl logs -f deployment/chenu-backend -n chenu
```

---

## Security Checklist

- [ ] Use HTTPS everywhere
- [ ] Set strong SECRET_KEY
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Enable database encryption
- [ ] Implement backup strategy
- [ ] Set up monitoring alerts
- [ ] Review access permissions

---

*CHE·NU™ - Governed Intelligence Operating System*
