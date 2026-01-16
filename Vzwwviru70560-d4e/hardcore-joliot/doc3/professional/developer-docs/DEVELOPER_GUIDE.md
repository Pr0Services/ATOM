# CHE·NU™ DEVELOPER DOCUMENTATION
## Complete Guide for Developers

**Version:** 1.0.0  
**Last Updated:** December 20, 2025  
**For:** CHE·NU v41.6+

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                  CHE·NU™ DEVELOPER DOCUMENTATION                              ║
║                                                                               ║
║        Build, Integrate, Extend — Welcome to the Platform                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Development Setup](#development-setup)
4. [API Reference](#api-reference)
5. [SDK & Libraries](#sdk--libraries)
6. [Building Integrations](#building-integrations)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Contributing](#contributing)

---

## Quick Start

### 5-Minute Integration

**Goal:** Make your first API call in 5 minutes.

**Step 1: Get API Key**
```bash
1. Login to https://chenu.com
2. Go to Settings → API Keys
3. Click "Generate New Key"
4. Copy key (starts with sk_...)
```

**Step 2: Make First Request**
```bash
curl https://api.chenu.com/v1/users/me \
  -H "Authorization: Bearer sk_live_abc123xyz789"

# Response:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "you@example.com",
  "name": "Your Name",
  "role": "user"
}
```

**Step 3: Create a Thread**
```bash
curl -X POST https://api.chenu.com/v1/threads \
  -H "Authorization: Bearer sk_live_abc123xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Thread",
    "sphere": "personal"
  }'
```

**🎉 Done!** You've made your first API calls.

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  React 18 + TypeScript + Vite + TailwindCSS                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Spheres │  │ Threads  │  │  Agents  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTPS (REST + GraphQL + WebSocket)
┌─────────────────────────────────────────────────────────────┐
│                        API LAYER                             │
│  FastAPI (Python 3.11) + GraphQL (Strawberry)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │   Auth   │  │  Threads │  │  Agents  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────┐  ┌──────────┐  ┌──────────┐             │
│  │ PostgreSQL   │  │  Redis   │  │   S3    │             │
│  │   (Data)     │  │ (Cache)  │  │ (Files) │             │
│  └──────────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- React 18 (UI framework)
- TypeScript (type safety)
- Vite (build tool)
- TailwindCSS (styling)
- TanStack Query (data fetching)
- Zustand (state management)

**Backend:**
- Python 3.11 (language)
- FastAPI (web framework)
- Strawberry (GraphQL)
- SQLAlchemy (ORM)
- Pydantic (validation)
- Celery (async tasks)

**Infrastructure:**
- PostgreSQL 15 (database)
- Redis 7 (cache)
- AWS S3 (file storage)
- CloudFront (CDN)
- Nginx (reverse proxy)

**DevOps:**
- Docker (containers)
- Kubernetes (orchestration)
- GitHub Actions (CI/CD)
- Terraform (infrastructure as code)

---

## Development Setup

### Prerequisites

```bash
# Required
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Git

# Recommended
- Docker & Docker Compose
- VS Code with extensions
- Postman or similar
```

### Local Setup (Docker)

**Fastest way to get started:**

```bash
# Clone repository
git clone https://github.com/chenu/chenu.git
cd chenu

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec api python manage.py migrate

# Create admin user
docker-compose exec api python manage.py createsuperuser

# Access application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Admin: http://localhost:8000/admin
```

**Services started:**
- ✅ Frontend (port 3000)
- ✅ API (port 8000)
- ✅ PostgreSQL (port 5432)
- ✅ Redis (port 6379)
- ✅ Celery worker
- ✅ Celery beat (scheduler)

### Manual Setup (Without Docker)

**Backend:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb chenu_dev
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# In another terminal, start Celery
celery -A chenu worker -l info
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Open browser
open http://localhost:3000
```

### Environment Variables

**Required variables in `.env`:**

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/chenu_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here-change-in-production
MFA_ENCRYPTION_KEY=your-mfa-encryption-key-here

# API Keys (for integrations)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# AWS (for file storage)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=chenu-dev

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG...

# Environment
DEBUG=True
ENVIRONMENT=development
```

---

## API Reference

### Authentication

**All API requests require authentication via:**

**Method 1: Bearer Token (Recommended)**
```bash
curl https://api.chenu.com/v1/threads \
  -H "Authorization: Bearer sk_live_abc123..."
```

**Method 2: API Key Header**
```bash
curl https://api.chenu.com/v1/threads \
  -H "X-API-Key: sk_live_abc123..."
```

### REST Endpoints

**Base URL:** `https://api.chenu.com/v1`

**Common Headers:**
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
Accept: application/json
```

**Response Format:**
```json
{
  "data": { ... },        // Success response
  "error": "...",         // Error message (if failed)
  "meta": {               // Metadata
    "timestamp": "...",
    "request_id": "..."
  }
}
```

**Pagination:**
```bash
GET /api/v1/threads?limit=20&offset=0

Response:
{
  "data": [...],
  "meta": {
    "total": 145,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

### GraphQL API

**Endpoint:** `https://api.chenu.com/graphql`

**Example Query:**
```graphql
query GetUser {
  user {
    id
    email
    threads(limit: 10) {
      id
      title
      sphere
      createdAt
    }
  }
}
```

**Example Mutation:**
```graphql
mutation CreateThread($input: CreateThreadInput!) {
  createThread(input: $input) {
    thread {
      id
      title
      sphere
    }
    errors
  }
}

# Variables:
{
  "input": {
    "title": "My Thread",
    "sphere": "PERSONAL"
  }
}
```

**Introspection:**
```bash
# Get full schema
curl -X POST https://api.chenu.com/graphql \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{__schema{types{name}}}"}'
```

### WebSocket API

**Connect to real-time updates:**

```javascript
const ws = new WebSocket('wss://api.chenu.com/ws')

ws.onopen = () => {
  // Authenticate
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'Bearer YOUR_TOKEN'
  }))
  
  // Subscribe to thread updates
  ws.send(JSON.stringify({
    type: 'subscribe',
    channel: 'thread.123'
  }))
}

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  console.log('Received:', data)
  // { type: 'message.created', data: {...} }
}
```

**Supported Events:**
- `thread.created`
- `thread.updated`
- `message.created`
- `message.updated`
- `agent.status_changed`

---

## SDK & Libraries

### Official SDKs

**JavaScript/TypeScript**
```bash
npm install @chenu/sdk

# Usage:
import { ChenuClient } from '@chenu/sdk'

const client = new ChenuClient({
  apiKey: 'sk_live_...',
  baseUrl: 'https://api.chenu.com/v1'
})

// Get current user
const user = await client.users.me()

// Create thread
const thread = await client.threads.create({
  title: 'My Thread',
  sphere: 'personal'
})

// List threads
const threads = await client.threads.list({
  sphere: 'business',
  limit: 20
})
```

**Python**
```bash
pip install chenu

# Usage:
from chenu import ChenuClient

client = ChenuClient(api_key='sk_live_...')

# Get current user
user = client.users.me()

# Create thread
thread = client.threads.create(
    title='My Thread',
    sphere='personal'
)

# List threads
threads = client.threads.list(
    sphere='business',
    limit=20
)
```

**Ruby**
```bash
gem install chenu

# Usage:
require 'chenu'

Chenu.api_key = 'sk_live_...'

# Get current user
user = Chenu::User.me

# Create thread
thread = Chenu::Thread.create(
  title: 'My Thread',
  sphere: 'personal'
)
```

### Community Libraries

- **Go:** github.com/chenu/go-chenu
- **Java:** com.chenu:chenu-java
- **PHP:** composer require chenu/chenu-php
- **.NET:** NuGet Install-Package Chenu.SDK

---

## Building Integrations

### Webhook Integration

**1. Register Webhook:**
```bash
POST /api/v1/webhooks

{
  "url": "https://your-app.com/webhook",
  "events": ["thread.created", "message.created"],
  "secret": "your_webhook_secret"
}
```

**2. Receive Webhook:**
```javascript
// Express.js example
app.post('/webhook', (req, res) => {
  const signature = req.headers['x-chenu-signature']
  const payload = req.body
  
  // Verify signature
  const expected = crypto
    .createHmac('sha256', 'your_webhook_secret')
    .update(JSON.stringify(payload))
    .digest('hex')
  
  if (signature !== expected) {
    return res.status(401).send('Invalid signature')
  }
  
  // Process event
  switch (payload.event) {
    case 'thread.created':
      handleThreadCreated(payload.data)
      break
    case 'message.created':
      handleMessageCreated(payload.data)
      break
  }
  
  res.status(200).send('OK')
})
```

### OAuth Integration

**1. Register OAuth App:**
```
Admin → Integrations → OAuth Apps → New

Name: Your App
Redirect URIs: https://your-app.com/oauth/callback
Scopes: read_threads, write_threads
```

**2. Authorization Flow:**
```javascript
// Step 1: Redirect user to authorization URL
const authUrl = 'https://chenu.com/oauth/authorize?' + 
  'client_id=YOUR_CLIENT_ID&' +
  'redirect_uri=https://your-app.com/oauth/callback&' +
  'scope=read_threads write_threads&' +
  'state=RANDOM_STATE'

window.location.href = authUrl

// Step 2: Handle callback
app.get('/oauth/callback', async (req, res) => {
  const { code, state } = req.query
  
  // Exchange code for token
  const response = await fetch('https://api.chenu.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'authorization_code',
      code,
      client_id: 'YOUR_CLIENT_ID',
      client_secret: 'YOUR_CLIENT_SECRET',
      redirect_uri: 'https://your-app.com/oauth/callback'
    })
  })
  
  const { access_token } = await response.json()
  
  // Store token and use for API calls
  // ...
})
```

### Custom Agent

**Create custom agent:**

```python
from chenu.agents import BaseAgent

class CustomAgent(BaseAgent):
    name = "Custom Agent"
    description = "My custom AI agent"
    level = "L2"
    
    async def execute(self, task: str, context: dict) -> dict:
        """
        Execute the task and return results.
        """
        # Your custom logic here
        result = self.process_task(task, context)
        
        return {
            'result': result,
            'tokens_used': self.count_tokens(result),
            'execution_time': self.elapsed_time()
        }
    
    def process_task(self, task, context):
        # Implement your agent's logic
        # Call external APIs, run ML models, etc.
        return "Task completed!"

# Register agent
ChenuClient.register_agent(CustomAgent)
```

---

## Testing

### Unit Tests

**Backend (pytest):**
```python
# tests/test_threads.py
import pytest
from app.models import Thread

@pytest.fixture
def user(db):
    return User.objects.create(
        email='test@example.com',
        name='Test User'
    )

def test_create_thread(client, user):
    response = client.post('/api/v1/threads', json={
        'title': 'Test Thread',
        'sphere': 'personal'
    }, headers={'Authorization': f'Bearer {user.token}'})
    
    assert response.status_code == 201
    assert response.json()['title'] == 'Test Thread'

def test_list_threads(client, user):
    # Create test data
    Thread.objects.create(title='Thread 1', user=user, sphere='personal')
    Thread.objects.create(title='Thread 2', user=user, sphere='business')
    
    response = client.get('/api/v1/threads', 
        headers={'Authorization': f'Bearer {user.token}'})
    
    assert response.status_code == 200
    assert len(response.json()['threads']) == 2
```

**Frontend (Vitest):**
```typescript
// tests/components/ThreadList.test.tsx
import { render, screen } from '@testing-library/react'
import { ThreadList } from '@/components/ThreadList'

describe('ThreadList', () => {
  it('renders threads', () => {
    const threads = [
      { id: '1', title: 'Thread 1' },
      { id: '2', title: 'Thread 2' }
    ]
    
    render(<ThreadList threads={threads} />)
    
    expect(screen.getByText('Thread 1')).toBeInTheDocument()
    expect(screen.getByText('Thread 2')).toBeInTheDocument()
  })
})
```

### Integration Tests

```python
# tests/integration/test_api.py
import pytest
from chenu import ChenuClient

@pytest.fixture
def client():
    return ChenuClient(api_key=os.getenv('TEST_API_KEY'))

def test_end_to_end_flow(client):
    # Create thread
    thread = client.threads.create(
        title='Integration Test',
        sphere='personal'
    )
    assert thread.id
    
    # Send message
    message = client.messages.create(
        thread_id=thread.id,
        content='Test message'
    )
    assert message.id
    
    # List messages
    messages = client.messages.list(thread_id=thread.id)
    assert len(messages) == 1
    
    # Delete thread
    client.threads.delete(thread.id)
```

### Load Testing

```javascript
// k6 load test
import http from 'k6/http'
import { check } from 'k6'

export const options = {
  vus: 100,
  duration: '5m'
}

export default function() {
  const res = http.get('https://api.chenu.com/v1/threads', {
    headers: {
      'Authorization': 'Bearer sk_test_...'
    }
  })
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200
  })
}
```

---

## Deployment

### Production Checklist

**Before deploying to production:**

- [ ] Environment variables set
- [ ] Database migrations run
- [ ] Static files collected
- [ ] SSL certificate configured
- [ ] Security headers enabled
- [ ] Rate limiting configured
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Error tracking enabled
- [ ] Documentation updated

### Deploy to Production

**Using Docker Compose:**
```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Run migrations
docker-compose -f docker-compose.prod.yml run api python manage.py migrate

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

**Using Kubernetes:**
```bash
# Apply configurations
kubectl apply -f k8s/

# Check deployment
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/chenu-api
```

### CI/CD Pipeline

**GitHub Actions example:**
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Your deployment script
          ./deploy.sh production
```

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                      DEVELOPER RESOURCES                                      ║
║                                                                               ║
║   📚 API Docs: https://docs.chenu.com/api                                    ║
║   💬 Discord: https://discord.gg/chenu                                       ║
║   📖 Examples: https://github.com/chenu/examples                             ║
║   🐛 Issues: https://github.com/chenu/chenu/issues                           ║
║                                                                               ║
║   Happy coding! 💻                                                           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Build amazing things with CHE·NU!** 🚀
