# 🚀 CHE·NU Deployment Guide

**Version:** 2.7.0  
**Platform:** AI Operating System

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Configuration](#configuration)
6. [Monitoring](#monitoring)

---

## 📦 Prerequisites

### Required Software

```bash
# Core
Python 3.11+
Node.js 20+
Docker & Docker Compose

# Databases
PostgreSQL 15+
Redis 7+

# Optional
Ollama (for local LLMs)
```

### System Requirements

| Environment | CPU | RAM | Storage |
|-------------|-----|-----|---------|
| Development | 4 cores | 8 GB | 50 GB |
| Staging | 8 cores | 16 GB | 100 GB |
| Production | 16+ cores | 32+ GB | 500+ GB |

---

## 💻 Local Development

### 1. Clone Repository

```bash
git clone https://github.com/your-org/chenu.git
cd chenu
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env.example .env
# Edit .env with your API keys

# Run database migrations
alembic upgrade head

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access Points

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Frontend | http://localhost:3000 |

---

## 🐳 Docker Deployment

### Quick Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/chenu
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    depends_on:
      - api

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=chenu
      - POSTGRES_PASSWORD=secure_password
      - POSTGRES_DB=chenu_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  postgres_data:
  redis_data:
  ollama_data:
```

### Backend Dockerfile

```dockerfile
# docker/Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/ .

# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## ☁️ Cloud Deployment

### AWS (Recommended)

#### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AWS ca-central-1                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Route 53 → CloudFront → ALB → ECS Fargate              │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ RDS         │  │ ElastiCache │  │ S3          │     │
│  │ PostgreSQL  │  │ Redis       │  │ Storage     │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### Terraform Deployment

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ca-central-1"
}

module "chenu" {
  source = "./modules/chenu"
  
  environment     = "production"
  domain          = "chenu.app"
  db_instance     = "db.r6g.large"
  redis_node_type = "cache.r6g.large"
}
```

### Google Cloud

```bash
# Deploy to Cloud Run
gcloud run deploy chenu-api \
  --image gcr.io/your-project/chenu-api:latest \
  --region northamerica-northeast1 \
  --platform managed \
  --allow-unauthenticated
```

### Kubernetes

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chenu-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chenu-api
  template:
    metadata:
      labels:
        app: chenu-api
    spec:
      containers:
      - name: api
        image: chenu/api:2.7.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: chenu-secrets
              key: database-url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

---

## ⚙️ Configuration

### Environment Variables

See `.env.example` for complete list. Key variables:

```bash
# Required
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
JWT_SECRET_KEY=your-secret-key

# LLM Providers (at least one required)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Optional but recommended
SENTRY_DSN=https://...
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 📊 Monitoring

### Health Check Endpoints

| Endpoint | Description |
|----------|-------------|
| `/health` | Basic health check |
| `/health/ready` | Readiness probe |
| `/health/live` | Liveness probe |

### Prometheus Metrics

```
# Available at /metrics
chenu_requests_total
chenu_request_duration_seconds
chenu_llm_tokens_total
chenu_agent_tasks_total
```

### Logging

```python
# Structured JSON logging
{
    "timestamp": "2024-12-14T10:30:00Z",
    "level": "INFO",
    "service": "chenu-api",
    "trace_id": "abc123",
    "message": "Agent task completed",
    "agent_id": "scheduler_l3",
    "duration_ms": 1234
}
```

---

## 🔒 Security Checklist

- [ ] Change all default passwords
- [ ] Set strong JWT_SECRET_KEY (32+ characters)
- [ ] Configure CORS origins properly
- [ ] Enable HTTPS/TLS
- [ ] Set up firewall rules
- [ ] Configure rate limiting
- [ ] Enable audit logging
- [ ] Regular security updates

---

## 📞 Support

- **Documentation**: https://docs.chenu.app
- **Issues**: https://github.com/your-org/chenu/issues
- **Email**: support@chenu.app

---

**© 2024 CHE·NU - AI Operating System**
