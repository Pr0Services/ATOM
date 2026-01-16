# 🚀 CHE·NU™ Deployment Guide

**Governed Intelligence Operating System**  
**Version:** 2.7.0

---

## Prerequisites

### Required Services
- **PostgreSQL** 15+
- **Redis** 7+
- **Python** 3.11+
- **Node.js** 20+ (frontend)

### Optional Services
- **Pinecone** (vector database)
- **AWS S3** (document storage)
- **Sentry** (error tracking)

---

## 🔧 Local Development

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
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r ../requirements.txt

# Copy environment file
cp ../.env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access Application

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

---

## 🐳 Docker Deployment

### 1. Build Images

```bash
# Build all services
docker-compose build

# Or build individually
docker build -f docker/Dockerfile.backend -t chenu-api .
docker build -f docker/Dockerfile.frontend -t chenu-web ./frontend
```

### 2. Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### docker-compose.yml

```yaml
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

  web:
    build:
      context: ./frontend
      dockerfile: ../docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    depends_on:
      - api

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: chenu
      POSTGRES_PASSWORD: secure_password
      POSTGRES_DB: chenu_db
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

## ☁️ AWS Deployment

### Architecture

```
                    ┌─────────────────┐
                    │   CloudFront    │
                    │     (CDN)       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │       ALB       │
                    │ (Load Balancer) │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────▼──────┐┌─────▼──────┐┌─────▼──────┐
       │ ECS Fargate ││ECS Fargate ││ECS Fargate │
       │  (API x3)   ││  (API x3)  ││  (Web x2)  │
       └──────┬──────┘└─────┬──────┘└────────────┘
              │             │
       ┌──────▼─────────────▼──────┐
       │         VPC               │
       │  ┌─────────┐ ┌─────────┐  │
       │  │   RDS   │ │ElastiC. │  │
       │  │Postgres │ │  Redis  │  │
       │  └─────────┘ └─────────┘  │
       └───────────────────────────┘
```

### 1. Infrastructure Setup (Terraform)

```hcl
# main.tf
provider "aws" {
  region = "ca-central-1"  # Montreal
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  name   = "chenu-vpc"
  cidr   = "10.0.0.0/16"
}

module "rds" {
  source           = "terraform-aws-modules/rds/aws"
  identifier       = "chenu-db"
  engine           = "postgres"
  engine_version   = "15"
  instance_class   = "db.t3.medium"
  allocated_storage = 50
}

module "elasticache" {
  source          = "terraform-aws-modules/elasticache/aws"
  cluster_id      = "chenu-redis"
  engine          = "redis"
  node_type       = "cache.t3.small"
}
```

### 2. ECS Task Definition

```json
{
  "family": "chenu-api",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "ghcr.io/your-org/chenu-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "ENVIRONMENT", "value": "production"}
      ],
      "secrets": [
        {"name": "DATABASE_URL", "valueFrom": "arn:aws:secretsmanager:..."}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/chenu-api",
          "awslogs-region": "ca-central-1"
        }
      }
    }
  ],
  "cpu": "1024",
  "memory": "2048"
}
```

### 3. Deploy with GitHub Actions

See `.github/workflows/ci-cd.yml` for automatic deployments.

---

## 🔐 Environment Variables

### Required

```bash
# Application
ENVIRONMENT=production
SECRET_KEY=your-256-bit-secret-key

# Database
DATABASE_URL=postgresql://user:pass@host:5432/chenu

# Redis
REDIS_URL=redis://host:6379/0

# JWT
JWT_SECRET_KEY=your-jwt-secret
```

### LLM Providers

```bash
# Pick the ones you need
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
XAI_API_KEY=xai-...
DEEPSEEK_API_KEY=sk-...
MISTRAL_API_KEY=...
GROQ_API_KEY=gsk_...
PERPLEXITY_API_KEY=pplx-...
```

### Optional Services

```bash
# Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
STORAGE_BUCKET=chenu-storage

# Vector DB
PINECONE_API_KEY=...
PINECONE_INDEX=chenu-embeddings

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
```

---

## 🔄 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# View migration history
alembic history
```

---

## 📊 Monitoring

### Health Checks

```bash
# API health
curl https://api.chenu.app/health

# Response
{
  "status": "healthy",
  "governance": {
    "encoding_layer": "active",
    "agent_orchestration": "active"
  }
}
```

### Logging

Logs are structured JSON:

```json
{
  "timestamp": "2024-12-14T10:30:00Z",
  "level": "INFO",
  "service": "chenu-api",
  "message": "Thread created",
  "thread_id": "thread_xyz",
  "user_id": "user_abc"
}
```

### Metrics (Prometheus)

```
chenu_threads_total
chenu_encodings_total
chenu_agent_executions_total
chenu_tokens_used_total
chenu_governance_checks_total
```

---

## 🔒 Security Checklist

- [ ] SSL/TLS enabled
- [ ] CORS configured
- [ ] Rate limiting enabled
- [ ] JWT secrets rotated
- [ ] Database encrypted at rest
- [ ] Secrets in Secrets Manager
- [ ] WAF rules configured
- [ ] Audit logging enabled

---

## 📞 Support

- **Documentation**: https://docs.chenu.app
- **Issues**: GitHub Issues
- **Email**: support@chenu.app

---

**© 2024 CHE·NU™ - Governed Intelligence Operating System**
