# 🚀 CHE·NU™ PRODUCTION DEPLOYMENT PLAYBOOK
## Complete Production Deployment Guide

**Version:** 1.0.0  
**Last Updated:** December 20, 2025  
**For:** CHE·NU v41.6+  
**Target:** Production Deployment Excellence

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                CHE·NU™ PRODUCTION DEPLOYMENT PLAYBOOK                         ║
║                                                                               ║
║   Zero-Downtime Deployments • High Availability • Auto-Scaling               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Infrastructure Setup](#infrastructure-setup)
3. [Database Deployment](#database-deployment)
4. [Application Deployment](#application-deployment)
5. [Post-Deployment Verification](#post-deployment-verification)
6. [Rollback Procedures](#rollback-procedures)
7. [Monitoring Setup](#monitoring-setup)
8. [Scaling Configuration](#scaling-configuration)

---

## Pre-Deployment Checklist

### 1. Code Readiness ✅

```bash
# Run all tests
npm run test:all
pytest --cov=. --cov-report=html

# Check coverage (must be 95%+)
cat coverage/index.html | grep "95%"

# Security scan
npm audit --production
pip-audit

# Lint check
npm run lint
black . --check
flake8 .

# Build check
npm run build
docker build -t chenu:latest .
```

**Requirements:**
- ✅ All tests passing (100%)
- ✅ Coverage ≥ 95%
- ✅ 0 security vulnerabilities
- ✅ 0 lint errors
- ✅ Build successful

### 2. Environment Configuration ✅

```bash
# Create production .env
cat > .env.production << 'EOF'
# Application
NODE_ENV=production
DEBUG=False
SECRET_KEY=<generate-with-openssl-rand>
ALLOWED_HOSTS=chenu.com,api.chenu.com

# Database
DATABASE_URL=postgresql://chenu:PASSWORD@db.internal:5432/chenu_prod
DB_POOL_MIN=10
DB_POOL_MAX=100
DB_SSL=require

# Redis
REDIS_URL=redis://:PASSWORD@redis.internal:6379/0
REDIS_SSL=true

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
S3_BUCKET=chenu-production

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG...
FROM_EMAIL=noreply@chenu.com

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
DATADOG_API_KEY=...
NEW_RELIC_LICENSE_KEY=...

# Security
MFA_REQUIRED=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true
SECURE_SSL_REDIRECT=true

# Performance
CACHE_TTL=3600
API_RATE_LIMIT=1000
COMPRESSION_ENABLED=true
EOF

# Validate all required vars are set
./scripts/validate-env.sh .env.production
```

**Requirements:**
- ✅ All secrets generated (use `openssl rand -hex 32`)
- ✅ AWS credentials configured
- ✅ Email SMTP working
- ✅ Monitoring keys valid
- ✅ No plaintext passwords

### 3. Infrastructure Readiness ✅

```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify VPC setup
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=chenu-prod"

# Check RDS instance
aws rds describe-db-instances --db-instance-identifier chenu-prod

# Verify Redis cluster
aws elasticache describe-cache-clusters --cache-cluster-id chenu-prod

# Check S3 bucket
aws s3 ls s3://chenu-production/

# Verify SSL certificates
aws acm describe-certificate --certificate-arn arn:aws:acm:...
```

**Requirements:**
- ✅ VPC configured (public + private subnets)
- ✅ RDS PostgreSQL 15 running
- ✅ ElastiCache Redis running
- ✅ S3 bucket with encryption
- ✅ SSL certificates valid
- ✅ Load balancer configured

### 4. DNS Configuration ✅

```bash
# Check DNS records
dig chenu.com
dig api.chenu.com
dig www.chenu.com

# Expected:
# chenu.com      → A record → Load Balancer IP
# api.chenu.com  → A record → API Load Balancer IP
# www.chenu.com  → CNAME   → chenu.com

# Verify SSL
curl -I https://chenu.com
curl -I https://api.chenu.com
```

**Requirements:**
- ✅ DNS records pointing to load balancers
- ✅ SSL certificates installed
- ✅ HTTPS working
- ✅ HTTP redirects to HTTPS

---

## Infrastructure Setup

### 1. Terraform Infrastructure as Code

```hcl
# infrastructure/main.tf
terraform {
  required_version = ">= 1.0"
  
  backend "s3" {
    bucket = "chenu-terraform-state"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr = "10.0.0.0/16"
  azs      = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.10.0/24", "10.0.20.0/24", "10.0.30.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Environment = "production"
    Project     = "chenu"
  }
}

# RDS PostgreSQL
module "rds" {
  source = "./modules/rds"
  
  identifier     = "chenu-prod"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.r6g.xlarge"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_encrypted     = true
  
  db_name  = "chenu"
  username = "chenu"
  password = var.db_password  # From secrets
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  multi_az               = true
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  
  tags = {
    Environment = "production"
  }
}

# ElastiCache Redis
module "redis" {
  source = "./modules/redis"
  
  cluster_id           = "chenu-prod"
  engine              = "redis"
  engine_version      = "7.0"
  node_type           = "cache.r6g.large"
  num_cache_nodes     = 3
  
  subnet_group_name   = aws_elasticache_subnet_group.main.name
  security_group_ids  = [aws_security_group.redis.id]
  
  automatic_failover_enabled = true
  multi_az_enabled          = true
  
  snapshot_retention_limit = 7
  snapshot_window         = "03:00-05:00"
  
  tags = {
    Environment = "production"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "chenu-prod"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Environment = "production"
  }
}

# Application Load Balancer
module "alb" {
  source = "./modules/alb"
  
  name               = "chenu-prod"
  load_balancer_type = "application"
  
  vpc_id          = module.vpc.vpc_id
  subnets         = module.vpc.public_subnets
  security_groups = [aws_security_group.alb.id]
  
  access_logs = {
    bucket  = "chenu-alb-logs"
    enabled = true
  }
  
  tags = {
    Environment = "production"
  }
}

# Auto Scaling
resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 20
  min_capacity       = 3
  resource_id        = "service/chenu-prod/api"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "ecs_policy_cpu" {
  name               = "cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace
  
  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0
  }
}
```

**Deploy Infrastructure:**

```bash
# Initialize Terraform
cd infrastructure
terraform init

# Plan deployment
terraform plan -out=tfplan

# Review plan carefully
terraform show tfplan

# Apply (requires confirmation)
terraform apply tfplan

# Verify outputs
terraform output -json > outputs.json
```

### 2. Docker Images

```dockerfile
# Dockerfile.production
FROM node:18-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --production
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim AS backend-builder
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY --from=backend-builder /app /app
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy frontend build
COPY --from=frontend-builder /app/dist /app/static

# Create non-root user
RUN useradd -m -u 1000 chenu && \
    chown -R chenu:chenu /app
USER chenu

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "app:app", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
```

**Build and Push:**

```bash
# Build image
docker build -f Dockerfile.production -t chenu:v41.6 .

# Tag for ECR
docker tag chenu:v41.6 123456789.dkr.ecr.us-east-1.amazonaws.com/chenu:v41.6
docker tag chenu:v41.6 123456789.dkr.ecr.us-east-1.amazonaws.com/chenu:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/chenu:v41.6
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/chenu:latest
```

---

## Database Deployment

### 1. Database Migration

```bash
# Create database backup FIRST
pg_dump -h db.internal -U chenu chenu_prod > backup_pre_migration.sql

# Upload to S3
aws s3 cp backup_pre_migration.sql s3://chenu-backups/migrations/$(date +%Y%m%d)/

# Run migrations
docker run --rm \
  -e DATABASE_URL=$DATABASE_URL \
  chenu:v41.6 \
  python manage.py migrate --check

# If check passes, run migration
docker run --rm \
  -e DATABASE_URL=$DATABASE_URL \
  chenu:v41.6 \
  python manage.py migrate

# Verify migration
docker run --rm \
  -e DATABASE_URL=$DATABASE_URL \
  chenu:v41.6 \
  python manage.py showmigrations
```

### 2. Database Optimization

```sql
-- Run after migration
-- Create indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_threads_user_updated 
ON threads(user_id, updated_at DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_messages_thread_created 
ON messages(thread_id, created_at DESC);

-- Analyze tables
ANALYZE threads;
ANALYZE messages;
ANALYZE users;

-- Update statistics
VACUUM ANALYZE;

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, tablename;
```

---

## Application Deployment

### 1. ECS Task Definition

```json
{
  "family": "chenu-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::123456789:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789:role/chenuTaskRole",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/chenu:v41.6",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "NODE_ENV", "value": "production"},
        {"name": "DEBUG", "value": "false"}
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:chenu/db-url"
        },
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:chenu/secret-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/chenu-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "api"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

### 2. Deployment Script

```bash
#!/bin/bash
# deploy.sh - Blue/Green Deployment Script

set -e

VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Usage: ./deploy.sh <version>"
  exit 1
fi

echo "🚀 Starting deployment of CHE·NU v$VERSION"

# 1. Build and push image
echo "📦 Building Docker image..."
docker build -f Dockerfile.production -t chenu:$VERSION .
docker tag chenu:$VERSION 123456789.dkr.ecr.us-east-1.amazonaws.com/chenu:$VERSION
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/chenu:$VERSION

# 2. Update task definition
echo "📝 Updating ECS task definition..."
TASK_DEF=$(cat task-definition.json | \
  jq ".containerDefinitions[0].image = \"123456789.dkr.ecr.us-east-1.amazonaws.com/chenu:$VERSION\"")
echo $TASK_DEF > task-definition-$VERSION.json

aws ecs register-task-definition \
  --cli-input-json file://task-definition-$VERSION.json

# 3. Update service (blue/green)
echo "🔄 Updating ECS service..."
aws ecs update-service \
  --cluster chenu-prod \
  --service api \
  --task-definition chenu-api:$VERSION \
  --force-new-deployment

# 4. Wait for deployment
echo "⏳ Waiting for deployment to complete..."
aws ecs wait services-stable \
  --cluster chenu-prod \
  --services api

# 5. Health check
echo "🏥 Running health checks..."
for i in {1..30}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.chenu.com/health)
  if [ "$STATUS" == "200" ]; then
    echo "✅ Health check passed!"
    break
  fi
  echo "Attempt $i/30: Status $STATUS"
  sleep 10
done

# 6. Smoke tests
echo "🧪 Running smoke tests..."
./scripts/smoke-tests.sh

echo "🎉 Deployment complete!"
```

### 3. Zero-Downtime Deployment

```yaml
# docker-compose.blue-green.yml
version: '3.8'

services:
  # Blue environment (current)
  api-blue:
    image: chenu:current
    environment:
      - COLOR=blue
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 30s
        failure_action: rollback
      rollback_config:
        parallelism: 1
        delay: 30s
  
  # Green environment (new)
  api-green:
    image: chenu:v41.6
    environment:
      - COLOR=green
    deploy:
      replicas: 3
  
  # Load balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api-blue
      - api-green
```

**Deployment Steps:**

1. Deploy green (new version) alongside blue
2. Run health checks on green
3. Switch 10% traffic to green
4. Monitor metrics for 5 minutes
5. Gradually shift traffic: 25%, 50%, 75%, 100%
6. Decommission blue after 24 hours

---

## Post-Deployment Verification

### 1. Automated Tests

```bash
#!/bin/bash
# smoke-tests.sh

BASE_URL="https://api.chenu.com"

echo "🧪 Running smoke tests..."

# Health check
echo "1. Health check..."
curl -f $BASE_URL/health || exit 1

# Auth flow
echo "2. Auth flow..."
TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@chenu.com","password":"TestPass123!"}' \
  | jq -r '.access_token')

if [ -z "$TOKEN" ]; then
  echo "❌ Auth failed"
  exit 1
fi

# API endpoint
echo "3. API endpoints..."
curl -f -H "Authorization: Bearer $TOKEN" \
  $BASE_URL/users/me || exit 1

# Create thread
echo "4. Create thread..."
THREAD=$(curl -s -X POST $BASE_URL/threads \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Smoke Test","sphere":"personal"}' \
  | jq -r '.id')

if [ -z "$THREAD" ]; then
  echo "❌ Thread creation failed"
  exit 1
fi

# Performance check
echo "5. Performance check..."
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' $BASE_URL/health)
if (( $(echo "$RESPONSE_TIME > 0.2" | bc -l) )); then
  echo "⚠️  Warning: Response time ${RESPONSE_TIME}s (>200ms)"
fi

echo "✅ All smoke tests passed!"
```

### 2. Metrics Verification

```bash
# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=chenu-api \
  --start-time $(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average

# Check response times (p95 should be <200ms)
aws cloudwatch get-metric-statistics \
  --namespace CHEnu \
  --metric-name ResponseTime \
  --start-time $(date -u -d '10 minutes ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics p95
```

---

## Rollback Procedures

### Quick Rollback (< 5 minutes)

```bash
#!/bin/bash
# rollback.sh - Emergency rollback

PREVIOUS_VERSION=$1

echo "⚠️  ROLLING BACK to version $PREVIOUS_VERSION"

# Update service to previous task definition
aws ecs update-service \
  --cluster chenu-prod \
  --service api \
  --task-definition chenu-api:$PREVIOUS_VERSION \
  --force-new-deployment

# Wait for rollback
aws ecs wait services-stable \
  --cluster chenu-prod \
  --services api

# Verify health
curl -f https://api.chenu.com/health

echo "✅ Rollback complete"
```

### Database Rollback

```bash
# Restore from backup
aws s3 cp s3://chenu-backups/migrations/20251220/backup_pre_migration.sql .

# Restore database
psql -h db.internal -U chenu chenu_prod < backup_pre_migration.sql

# Verify
psql -h db.internal -U chenu chenu_prod -c "SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1;"
```

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    DEPLOYMENT CHECKLIST                                       ║
║                                                                               ║
║   Pre-Deployment:                                                            ║
║   ✅ Tests passing (100%)                                                    ║
║   ✅ Coverage ≥ 95%                                                           ║
║   ✅ Security scan clean                                                      ║
║   ✅ Infrastructure ready                                                     ║
║   ✅ DNS configured                                                           ║
║                                                                               ║
║   Deployment:                                                                ║
║   ✅ Database migrated                                                        ║
║   ✅ Blue/green deployment                                                    ║
║   ✅ Health checks passed                                                     ║
║   ✅ Smoke tests passed                                                       ║
║   ✅ Metrics validated                                                        ║
║                                                                               ║
║   Post-Deployment:                                                           ║
║   ✅ Monitoring active                                                        ║
║   ✅ Alerts configured                                                        ║
║   ✅ Rollback plan ready                                                      ║
║   ✅ Team notified                                                            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Your production deployment is READY!** 🚀✨
