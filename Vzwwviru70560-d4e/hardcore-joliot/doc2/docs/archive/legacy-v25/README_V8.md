# 🚀 CHENU Unified v8.0

**Plateforme de Gestion de Construction avec Agents IA Hiérarchiques**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)

---

## 📋 Table des Matières

- [Vue d'Ensemble](#-vue-densemble)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [API Reference](#-api-reference)
- [Intégrations](#-intégrations-60)

---

## 🎯 Vue d'Ensemble

CHENU combine:
- **🤖 Agents IA Hiérarchiques** - Nova → MasterMind → Directors → Specialists
- **🧠 Multi-LLM** - Claude, GPT-4, Gemini, DeepSeek, Ollama
- **🔌 60+ Intégrations** - Comptabilité, CRM, Marketing, E-commerce, PM...

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        👤 UTILISATEUR                           │
│              🏠 Maison | 🏢 Bureau | 🌍 Extérieur               │
├─────────────────────────────────────────────────────────────────┤
│  🎯 NOVA (L-1) ─ Agent Personnel Universel                     │
│                           │                                     │
│  🧠 MASTER MIND (L0) ─ Orchestrateur Central                   │
│     ├── 🔀 RoutingEngine    ├── 📊 TaskDecomposer              │
│     ├── 📋 ExecutionPlanner └── 🔄 ResultAssembler             │
│                           │                                     │
│  👔 DIRECTORS (L1)                                              │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐     │
│  │Pierre 🏗️ │Victoria💰│Clara 👥  │Sophie 📢 │Alex 🎨   │     │
│  │Construct.│Finance   │RH        │Marketing │Creative  │     │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘     │
│  🛠️ SPECIALISTS (L2) ─ 50+ agents spécialisés                  │
├─────────────────────────────────────────────────────────────────┤
│  🔌 INTEGRATIONS (60+)                                         │
│  💰 Compta │📊 CRM │📋 PM │🛒 E-Com │💬 Comm │🏗️ Construct.   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation

```bash
# 1. Cloner
git clone https://github.com/your-org/chenu.git && cd chenu

# 2. Environnement
python -m venv venv && source venv/bin/activate

# 3. Dépendances
pip install -r requirements.txt

# 4. Configuration
cp .env.example .env  # Éditer avec vos clés

# 5. Lancer
uvicorn backend.api.main:app --reload --port 8000
```

### Variables d'Environnement

```env
CHENU_DB_URL=postgresql://user:pass@localhost:5432/chenu
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx
GOOGLE_API_KEY=xxx
```

---

## 📡 API Reference

### Base URL: `http://localhost:8000/api/v1`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Chat avec Nova |
| `/tasks` | POST | Créer une tâche |
| `/tasks/active` | GET | Tâches actives |
| `/routing/analyze` | POST | Analyser le routage |
| `/agents` | GET | Liste des agents |
| `/agents/map` | GET | Carte hiérarchique |
| `/integrations` | GET | Intégrations disponibles |
| `/llm/providers` | GET | Providers LLM |

### Exemple Chat

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Crée une estimation pour le projet ABC", "user_id": "demo"}'
```

### Documentation Interactive

- **Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 Intégrations (60+)

### Comptabilité
| Provider | Features |
|----------|----------|
| **QuickBooks** | Factures, Dépenses, Rapports |
| **Xero** | Contacts, Invoices, Bank |
| **Stripe** | Paiements, Subscriptions |
| **Wave** | Free accounting |

### CRM
| Provider | Features |
|----------|----------|
| **Salesforce** | Leads, Opportunities, Accounts |
| **Pipedrive** | Deals, Persons, Activities |
| **Zoho CRM** | Leads, Deals, Campaigns |

### Project Management
| Provider | Features |
|----------|----------|
| **Asana** | Projects, Tasks, Subtasks |
| **Monday** | Boards, Items, Updates |
| **Jira** | Issues, Sprints, Workflows |
| **ClickUp** | Spaces, Lists, Tasks |

### E-Commerce
| Provider | Features |
|----------|----------|
| **Shopify** | Products, Orders, Customers |
| **WooCommerce** | Full store management |
| **Square** | POS, Inventory, Payments |

### Communication
| Provider | Features |
|----------|----------|
| **Slack** | Messages, Channels |
| **Discord** | Servers, Webhooks |
| **Teams** | Messages, Meetings |
| **Zoom** | Meetings, Webinars |

### Construction & RH
| Provider | Features |
|----------|----------|
| **Procore** | Projects, RFIs, Submittals |
| **Autodesk** | BIM, Design |
| **BambooHR** | Employees, Time off |
| **Gusto** | Payroll, Benefits |

### Administration
| Provider | Features |
|----------|----------|
| **DocuSign** | E-signatures |
| **Calendly** | Scheduling |
| **Notion** | Docs, Databases |
| **Airtable** | Bases, Records |
| **Trello** | Boards, Cards |

---

## 📊 Structure

```
chenu_unified/
├── backend/
│   ├── core/           # MasterMind, Routing, LLM Router
│   ├── agents/         # Nova, Directors, Specialists
│   ├── services/
│   │   └── integrations/   # 60+ integrations
│   ├── schemas/        # Pydantic models
│   └── api/            # FastAPI
├── sql/                # Migrations
├── requirements.txt
└── README.md
```

---

## 🧠 Multi-LLM Support

```yaml
Providers:
  anthropic: claude-sonnet-4-20250514, claude-opus-4-20250514, claude-haiku-4-20250514
  openai: gpt-4o, gpt-4o-mini, o1, o1-mini
  google: gemini-1.5-pro, gemini-1.5-flash, gemini-2.0-flash
  deepseek: deepseek-chat, deepseek-coder
  ollama: llama3.1:70b, qwen2.5:72b
```

**Fallback automatique** si un provider échoue.

---

**🚀 CHENU v8.0 Unified - Construction Intelligence, Simplified.**

*Développé avec ❤️ par l'équipe CHENU*
