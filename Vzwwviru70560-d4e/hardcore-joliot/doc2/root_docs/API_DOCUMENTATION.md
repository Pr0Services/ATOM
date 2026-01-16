# ═══════════════════════════════════════════════════════════════════════════════
# CHE·NU™ v40 — API DOCUMENTATION COMPLETE
# ═══════════════════════════════════════════════════════════════════════════════
# Version: 40.0.0
# Base URL: /api/v1
# Authentication: Bearer Token
# ═══════════════════════════════════════════════════════════════════════════════

## 📋 TABLE OF CONTENTS

1. [Personal Sphere API](#personal-sphere-api)
2. [Business Sphere API](#business-sphere-api)
3. [Government Sphere API](#government-sphere-api)
4. [Studio Sphere API](#studio-sphere-api)
5. [Community Sphere API](#community-sphere-api)
6. [Social Sphere API](#social-sphere-api)
7. [Entertainment Sphere API](#entertainment-sphere-api)
8. [My Team Sphere API](#my-team-sphere-api)
9. [Scholar Sphere API](#scholar-sphere-api)
10. [Agents API](#agents-api)

---

## 🔐 AUTHENTICATION

All API requests require authentication via Bearer token:

```http
Authorization: Bearer <your_token>
```

---

## 🏠 PERSONAL SPHERE API

Base: `/api/v1/personal`

### Goals

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/goals` | List all goals |
| POST | `/goals` | Create new goal |
| GET | `/goals/{id}` | Get goal details |
| PUT | `/goals/{id}` | Update goal |
| DELETE | `/goals/{id}` | Delete goal |
| POST | `/goals/{id}/progress` | Update progress |
| POST | `/goals/{id}/complete` | Mark complete |
| POST | `/goals/{id}/milestones` | Add milestone |

### Habits

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/habits` | List all habits |
| POST | `/habits` | Create new habit |
| GET | `/habits/{id}` | Get habit details |
| PUT | `/habits/{id}` | Update habit |
| DELETE | `/habits/{id}` | Delete habit |
| POST | `/habits/{id}/log` | Log completion |
| GET | `/habits/{id}/logs` | Get habit logs |
| GET | `/habits/{id}/stats` | Get statistics |

### Journal

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/journal` | List entries |
| POST | `/journal` | Create entry |
| GET | `/journal/{id}` | Get entry |
| PUT | `/journal/{id}` | Update entry |
| DELETE | `/journal/{id}` | Delete entry |
| POST | `/journal/{id}/favorite` | Toggle favorite |
| GET | `/journal/prompts` | Get prompts |
| GET | `/journal/stats` | Get statistics |

### Daily Planning

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/daily-plan` | Get today's plan |
| GET | `/daily-plan/{date}` | Get plan by date |
| POST | `/daily-plan` | Create plan |
| PUT | `/daily-plan/{date}/evening-review` | Complete review |

### Life Areas

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/life-areas` | List life areas |
| POST | `/life-areas` | Create area |
| PUT | `/life-areas/{id}/score` | Update score |
| POST | `/assessments` | Create assessment |
| GET | `/assessments` | Get history |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Get overview |

---

## 🏛️ GOVERNMENT SPHERE API

Base: `/api/v1/government`

### Documents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/documents` | List documents |
| POST | `/documents` | Create document |
| GET | `/documents/{id}` | Get document |
| PUT | `/documents/{id}` | Update document |
| DELETE | `/documents/{id}` | Delete document |
| POST | `/documents/{id}/upload` | Upload file |
| GET | `/documents/expiring` | Get expiring |

### Deadlines

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/deadlines` | List deadlines |
| POST | `/deadlines` | Create deadline |
| GET | `/deadlines/{id}` | Get deadline |
| PUT | `/deadlines/{id}` | Update deadline |
| DELETE | `/deadlines/{id}` | Delete deadline |
| POST | `/deadlines/{id}/complete` | Mark complete |
| GET | `/deadlines/upcoming` | Get upcoming |
| GET | `/deadlines/overdue` | Get overdue |

### Forms

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/forms` | List forms |
| POST | `/forms` | Create form |
| GET | `/forms/{id}` | Get form |
| PUT | `/forms/{id}` | Update form |
| DELETE | `/forms/{id}` | Delete form |
| PUT | `/forms/{id}/fields` | Update fields |
| POST | `/forms/{id}/submit` | Submit form |
| POST | `/forms/{id}/upload` | Upload file |

### Compliance

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/compliance` | List items |
| POST | `/compliance` | Create item |
| PUT | `/compliance/{id}` | Update item |
| PUT | `/compliance/{id}/requirements/{idx}` | Update requirement |
| POST | `/compliance/{id}/verify` | Verify compliance |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard` | Get overview |
| GET | `/calendar` | Get calendar |
| GET | `/reminders` | Get reminders |
| GET | `/activity` | Get activity log |

---

## 💼 BUSINESS SPHERE API

Base: `/api/v1/business`

### CRM

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| Contacts | 10 |
| Companies | 8 |
| Deals | 12 |
| Pipelines | 5 |

### Invoicing

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| Invoices | 12 |
| Payments | 6 |
| Templates | 4 |
| Reports | 3 |

### Time Tracking

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| Time Entries | 8 |
| Projects | 6 |
| Reports | 5 |

---

## 🎨 STUDIO SPHERE API

Base: `/api/v1/studio`

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| Projects | 15 |
| Assets | 12 |
| Canvases | 8 |
| Collaborators | 6 |
| Versions | 5 |
| Comments | 5 |

---

## 👥 COMMUNITY SPHERE API

Base: `/api/v1/community`

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| Groups | 12 |
| Posts | 10 |
| Events | 8 |
| Members | 8 |
| Connections | 7 |

---

## 📱 SOCIAL SPHERE API

Base: `/api/v1/social`

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| Profiles | 8 |
| Posts | 15 |
| Stories | 8 |
| Follows | 6 |
| Analytics | 8 |

---

## 🎬 ENTERTAINMENT SPHERE API

Base: `/api/v1/entertainment`

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| Media | 10 |
| Library | 8 |
| Playlists | 8 |
| Recommendations | 5 |
| Watch Parties | 5 |
| Integrations | 5 |

---

## 🤝 MY TEAM SPHERE API

Base: `/api/v1/myteam`

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| Teams | 10 |
| Members | 8 |
| Skills | 6 |
| Tools | 6 |
| Marketplace | 8 |
| Workflows | 4 |

---

## 📚 SCHOLAR SPHERE API

Base: `/api/v1/scholar`

| Endpoint Group | Endpoints Count |
|----------------|-----------------|
| References | 12 |
| Notes | 10 |
| Flashcards | 8 |
| Study Plans | 6 |
| Review Sessions | 6 |

---

## 🤖 AGENTS API

Base: `/api/v1/agents`

### Available Agents

| Agent ID | Sphere | Level | Capabilities |
|----------|--------|-------|--------------|
| `personal.assistant` | Personal 🏠 | L3 | 12 |
| `business.crm_assistant` | Business 💼 | L3 | 10 |
| `business.invoice_manager` | Business 💼 | L3 | 8 |
| `government.admin` | Government 🏛️ | L3 | 10 |
| `scholar.research_assistant` | Scholar 📚 | L3 | 12 |
| `studio.creative_assistant` | Studio 🎨 | L3 | 11 |
| `community.manager` | Community 👥 | L3 | 8 |
| `social.media_manager` | Social 📱 | L3 | 12 |
| `entertainment.curator` | Entertainment 🎬 | L3 | 12 |
| `myteam.orchestrator` | My Team 🤝 | L3 | 12 |

### Agent Invocation

```http
POST /api/v1/agents/{agent_id}/invoke
Content-Type: application/json

{
  "action": "capability_name",
  "params": {},
  "context": {}
}
```

### Response Format

```json
{
  "success": true,
  "action": "capability_name",
  "data": {},
  "message": "Action completed",
  "tokens_used": 100,
  "suggestions": []
}
```

---

## 📊 COMMON PATTERNS

### Pagination

```http
GET /api/v1/{resource}?page=1&page_size=20
```

### Filtering

```http
GET /api/v1/{resource}?status=active&category=work
```

### Sorting

```http
GET /api/v1/{resource}?sort_by=created_at&sort_order=desc
```

### Search

```http
GET /api/v1/{resource}?search=keyword
```

---

## ⚠️ ERROR RESPONSES

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Rate Limited |
| 500 | Server Error |

---

## 🔒 GOVERNANCE

All API operations respect CHE·NU™ governance:

1. **Sphere Isolation**: Data stays within sphere boundaries
2. **Token Budget**: Each operation costs tokens
3. **Agent Non-Autonomy**: Agents require user approval
4. **Audit Logging**: All actions are logged

---

*CHE·NU™ API Documentation v40.0.0*
*Generated: December 20, 2025*
