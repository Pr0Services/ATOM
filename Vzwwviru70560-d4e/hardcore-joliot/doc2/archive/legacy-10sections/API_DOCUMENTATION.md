# CHE·NU™ API Documentation

> **Version:** 1.0.0  
> **Base URL:** `https://api.chenu.io/api/v1`  
> **Last Updated:** 2024

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Spheres](#spheres)
4. [Threads (.chenu)](#threads)
5. [Tokens](#tokens)
6. [Agents](#agents)
7. [DataSpaces](#dataspaces)
8. [Meetings](#meetings)
9. [Nova AI](#nova-ai)
10. [Governance](#governance)
11. [Reports](#reports)
12. [WebSocket](#websocket)
13. [Encoding](#encoding)
14. [Error Handling](#error-handling)

---

## Overview

CHE·NU™ is a **Governed Intelligence Operating System** that manages:
- Intelligence and AI agents
- Intent and context (Spheres)
- Data and dataspaces
- Token budgets (NOT cryptocurrency)
- Collaboration and ethics

### Core Principles

| Principle | Description |
|-----------|-------------|
| **8 Spheres** | Personal, Business, Government, Studio, Community, Social, Entertainment, Team |
| **10 Bureau Sections** | Dashboard, Notes, Tasks, Projects, Threads, Meetings, Data, Agents, Reports, Budget |
| **Threads (.chenu)** | First-class persistent conversation objects |
| **Tokens** | Internal utility credits for AI operations |
| **Governance** | All AI execution is governed and auditable |

---

## Authentication

### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "display_name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "display_name": "John Doe",
  "role": "user",
  "token_balance": 10000,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "johndoe"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "refresh-token-string",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Get Current User

```http
GET /auth/me
Authorization: Bearer {access_token}
```

---

## Spheres

CHE·NU has **exactly 8 spheres**. This is non-negotiable.

### List All Spheres

```http
GET /spheres
```

**Response (200):**
```json
[
  {
    "id": "personal",
    "name": "Personal",
    "icon": "🏠",
    "color": "#3F7249",
    "description": "Private life management",
    "bureau_sections": [
      {"id": "dashboard", "name": "Dashboard", "order": 1},
      {"id": "notes", "name": "Notes", "order": 2},
      // ... 10 sections total
    ]
  },
  // ... 8 spheres total
]
```

### Get Sphere Details

```http
GET /spheres/{sphere_id}
```

**Parameters:**
- `sphere_id`: One of `personal`, `business`, `government`, `studio`, `community`, `social`, `entertainment`, `team`

---

## Threads

Threads are **first-class objects** in CHE·NU representing persistent lines of thought.

### List Threads

```http
GET /threads
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `sphere_id` | string | Filter by sphere |
| `status` | string | Filter by status (active, paused, completed, archived) |
| `skip` | int | Pagination offset |
| `limit` | int | Max results (default: 50) |

### Create Thread

```http
POST /threads
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Q4 Marketing Strategy",
  "sphere_id": "business",
  "description": "Thread for planning Q4 marketing initiatives",
  "token_budget": 5000,
  "encoding_mode": "standard",
  "tags": ["marketing", "q4", "strategy"]
}
```

**Response (201):**
```json
{
  "id": "thread-uuid",
  "title": "Q4 Marketing Strategy",
  "sphere_id": "business",
  "owner_id": "user-uuid",
  "status": "active",
  "token_budget": 5000,
  "tokens_used": 0,
  "encoding_mode": "standard",
  "messages": [],
  "decisions": [],
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Send Message to Thread

```http
POST /threads/{thread_id}/messages
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "What are the key trends for Q4?",
  "encode": true
}
```

**Response (200):**
```json
{
  "id": "msg-uuid",
  "thread_id": "thread-uuid",
  "role": "user",
  "content": "What are the key trends for Q4?",
  "encoded_content": "Q:KEY-TRENDS-Q4",
  "tokens_used": 8,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Record Decision

```http
POST /threads/{thread_id}/decisions
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Focus on social media campaigns",
  "description": "Decided to allocate 60% of budget to social media",
  "impact": "high"
}
```

---

## Tokens

Tokens are **internal utility credits**, NOT cryptocurrency.

### List Token Budgets

```http
GET /tokens/budgets
Authorization: Bearer {token}
```

**Response (200):**
```json
[
  {
    "id": "budget-uuid",
    "name": "Business Operations",
    "sphere_id": "business",
    "total_allocated": 10000,
    "total_used": 3500,
    "remaining": 6500,
    "period": "monthly",
    "reset_at": "2024-02-01T00:00:00Z"
  }
]
```

### Create Token Budget

```http
POST /tokens/budgets
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Personal AI Assistant",
  "sphere_id": "personal",
  "total_allocated": 5000,
  "period": "monthly"
}
```

### Consume Tokens

```http
POST /tokens/consume
Authorization: Bearer {token}
Content-Type: application/json

{
  "budget_id": "budget-uuid",
  "amount": 150,
  "description": "Agent task execution",
  "thread_id": "thread-uuid",
  "agent_id": "agent-uuid"
}
```

### Get Transactions

```http
GET /tokens/transactions
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `budget_id` | string | Filter by budget |
| `type` | string | allocation, consumption, transfer, refund |
| `start_date` | datetime | Filter from date |
| `end_date` | datetime | Filter to date |

---

## Agents

### Nova (System Agent)

Nova is the **system intelligence** - always present, never hired.

```http
GET /agents/nova
```

**Response (200):**
```json
{
  "id": "nova",
  "name": "Nova",
  "type": "nova",
  "avatar": "✧",
  "description": "System intelligence - guidance, memory, governance",
  "capabilities": ["guidance", "memory", "governance", "supervision"],
  "sphere_scopes": ["all"],
  "is_system": true,
  "is_active": true
}
```

### List Available Agents

```http
GET /agents
```

### Hire Agent

```http
POST /agents/hire
Authorization: Bearer {token}
Content-Type: application/json

{
  "agent_id": "agent-uuid"
}
```

> ⚠️ **Note:** Nova cannot be hired. Attempting to hire Nova will return 403 Forbidden.

### List Hired Agents

```http
GET /agents/hired
Authorization: Bearer {token}
```

### Execute Agent Task

```http
POST /agents/{agent_id}/execute
Authorization: Bearer {token}
Content-Type: application/json

{
  "task": "Analyze quarterly report",
  "sphere_id": "business",
  "thread_id": "thread-uuid",
  "budget_id": "budget-uuid",
  "parameters": {
    "depth": "detailed",
    "format": "summary"
  }
}
```

---

## DataSpaces

### List DataSpaces

```http
GET /dataspaces
Authorization: Bearer {token}
```

### Create DataSpace

```http
POST /dataspaces
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Customer Contacts",
  "sphere_id": "business",
  "type": "table",
  "schema": {
    "columns": [
      {"name": "id", "type": "string", "primary": true},
      {"name": "name", "type": "string", "required": true},
      {"name": "email", "type": "string"},
      {"name": "company", "type": "string"}
    ]
  }
}
```

### Add Record

```http
POST /dataspaces/{dataspace_id}/records
Authorization: Bearer {token}
Content-Type: application/json

{
  "data": {
    "id": "contact-1",
    "name": "Jane Smith",
    "email": "jane@company.com",
    "company": "TechCorp"
  }
}
```

### Query Records

```http
GET /dataspaces/{dataspace_id}/records
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `filter` | JSON | Filter criteria |
| `sort` | string | Sort field |
| `order` | string | asc or desc |
| `skip` | int | Pagination offset |
| `limit` | int | Max results |

---

## Meetings

### List Meetings

```http
GET /meetings
Authorization: Bearer {token}
```

### Create Meeting

```http
POST /meetings
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Weekly Team Sync",
  "sphere_id": "business",
  "start_time": "2024-01-15T10:00:00Z",
  "end_time": "2024-01-15T11:00:00Z",
  "is_virtual": true,
  "virtual_link": "https://meet.chenu.io/abc123",
  "token_budget": 500,
  "attendees": [
    {"name": "John Doe", "email": "john@example.com", "role": "required"},
    {"name": "Jane Smith", "email": "jane@example.com", "role": "optional"}
  ],
  "linked_thread_id": "thread-uuid"
}
```

### Add Meeting Notes

```http
POST /meetings/{meeting_id}/notes
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "Discussed Q4 priorities. Action items assigned.",
  "is_private": false
}
```

---

## Nova AI

### Get Nova Status

```http
GET /nova/status
```

**Response (200):**
```json
{
  "status": "idle",
  "active_threads": 0,
  "last_activity": "2024-01-01T00:00:00Z"
}
```

### Chat with Nova

```http
POST /nova/chat
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "Help me plan my week",
  "sphere_id": "personal",
  "thread_id": "thread-uuid",
  "context": {
    "include_recent_activity": true
  }
}
```

**Response (200):**
```json
{
  "response": "Based on your calendar and tasks, here's a suggested plan...",
  "suggestions": [
    {"type": "task", "content": "Review Q4 report"},
    {"type": "meeting", "content": "Schedule team sync"}
  ],
  "tokens_used": 245,
  "thread_id": "thread-uuid"
}
```

### Get Nova Suggestions

```http
GET /nova/suggestions
Authorization: Bearer {token}
```

---

## Governance

### Validate Execution

```http
POST /governance/validate
Authorization: Bearer {token}
Content-Type: application/json

{
  "action_type": "agent_execution",
  "sphere_id": "business",
  "estimated_tokens": 500,
  "agent_id": "agent-uuid",
  "thread_id": "thread-uuid"
}
```

**Response (200):**
```json
{
  "valid": true,
  "checks": {
    "budget_available": true,
    "scope_allowed": true,
    "agent_authorized": true,
    "governance_rules_passed": true
  },
  "warnings": [],
  "estimated_cost": 500
}
```

### List Governance Rules

```http
GET /governance/rules
Authorization: Bearer {token}
```

### Create Governance Rule

```http
POST /governance/rules
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Daily Token Limit",
  "type": "limit",
  "sphere_id": "personal",
  "threshold": 1000,
  "action": "block"
}
```

---

## Reports

### Get Activity Log

```http
GET /reports/activity
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `sphere_id` | string | Filter by sphere |
| `type` | string | create, update, delete, view, execute |
| `start_date` | datetime | Filter from date |
| `end_date` | datetime | Filter to date |

### Get Summary Report

```http
GET /reports/summary
Authorization: Bearer {token}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `sphere_id` | string | Filter by sphere |
| `period` | string | day, week, month |

**Response (200):**
```json
{
  "period": "week",
  "sphere_id": "business",
  "threads": {
    "total": 15,
    "active": 8,
    "completed": 5,
    "archived": 2
  },
  "tokens": {
    "allocated": 10000,
    "used": 3500,
    "remaining": 6500
  },
  "agents": {
    "tasks_executed": 42,
    "success_rate": 0.95
  },
  "meetings": {
    "total": 8,
    "upcoming": 3
  }
}
```

---

## WebSocket

### Connect

```javascript
const ws = new WebSocket('wss://api.chenu.io/ws/{user_id}');
```

### Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `connect` | Server→Client | Connection confirmed |
| `ping` | Client→Server | Keep-alive |
| `pong` | Server→Client | Keep-alive response |
| `thread_message` | Server→Client | New thread message |
| `thread_typing` | Both | Typing indicator |
| `agent_status` | Server→Client | Agent status change |
| `agent_task_progress` | Server→Client | Task progress update |
| `token_update` | Server→Client | Budget update |
| `token_alert` | Server→Client | Budget warning |
| `nova_response` | Server→Client | Nova AI response |
| `notification` | Server→Client | General notification |

### Subscribe to Thread

```json
{
  "type": "subscribe_thread",
  "data": {"thread_id": "thread-uuid"},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Subscribe to Sphere

```json
{
  "type": "subscribe_sphere",
  "data": {"sphere_id": "business"},
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## Encoding

CHE·NU includes an **encoding layer** to reduce token usage.

### Encode Text

```http
POST /encoding/encode
Authorization: Bearer {token}
Content-Type: application/json

{
  "text": "Please analyze the quarterly financial report and provide recommendations",
  "mode": "aggressive",
  "custom_rules": [
    {"pattern": "quarterly report", "replacement": "QR"}
  ]
}
```

**Response (200):**
```json
{
  "encoded_text": "ANL:QR→PROV:RECS",
  "original_tokens": 12,
  "encoded_tokens": 4,
  "compression_ratio": 3.0,
  "quality_score": 92,
  "rules_applied": ["action_compression", "custom:QR"]
}
```

### Decode Text

```http
POST /encoding/decode
Authorization: Bearer {token}
Content-Type: application/json

{
  "encoded_text": "ANL:QR→PROV:RECS"
}
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Rate Limited |
| 500 | Internal Server Error |

### Error Codes

| Code | Description |
|------|-------------|
| `AUTH_INVALID_CREDENTIALS` | Wrong email or password |
| `AUTH_TOKEN_EXPIRED` | Access token expired |
| `SPHERE_NOT_FOUND` | Invalid sphere ID |
| `THREAD_NOT_FOUND` | Thread does not exist |
| `BUDGET_INSUFFICIENT` | Not enough tokens |
| `AGENT_NOT_AUTHORIZED` | Agent cannot access sphere |
| `GOVERNANCE_BLOCKED` | Action blocked by governance |

---

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Authentication | 10/minute |
| API (authenticated) | 100/minute |
| WebSocket | 50 messages/minute |
| Nova Chat | 20/minute |

---

## SDKs

Official SDKs are available:

- **JavaScript/TypeScript:** `npm install @chenu/sdk`
- **Python:** `pip install chenu-sdk`
- **Go:** `go get github.com/chenu/sdk-go`

---

*CHE·NU™ - Governed Intelligence Operating System*
