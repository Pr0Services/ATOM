# 🧠 CHE·NU™ Architecture Documentation

**Governed Intelligence Operating System**  
**Version:** 2.7.0  
**Last Updated:** December 2024  

> **"Putting humans back in control of AI"**

---

## ⚠️ What CHE·NU IS and IS NOT

### CHE·NU IS:
- ✅ A **Governed Intelligence Operating System**
- ✅ An **encoding layer** between humans and AI
- ✅ An **agent orchestration platform**
- ✅ A **governance-first** AI interface
- ✅ A **multi-sphere** contextual workspace

### CHE·NU IS NOT:
- ❌ NOT a chatbot
- ❌ NOT a prompt manager
- ❌ NOT a simple AI SaaS
- ❌ NOT a content generator
- ❌ NOT a task manager
- ❌ NOT an industry-specific app

---

## 🎯 Core Philosophy

> **No AI execution should happen before human intent is clarified, encoded, governed, and validated.**

Most AI systems execute first and let humans clean the mess.
**CHE·NU does the opposite.**

CHE·NU introduces an intermediate, governed layer between humans and AI models.

---

## 🔄 The CHE·NU Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THE CHE·NU PIPELINE                                   │
│                                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐│
│   │  INTENT  │───▶│ ENCODING │───▶│GOVERNANCE│───▶│  ORCH.   │───▶│ EXEC.  ││
│   │          │    │          │    │          │    │          │    │        ││
│   │ Clarify  │    │ Semantic │    │ Validate │    │  Agent   │    │Traced  ││
│   │  human   │    │  schema  │    │  scope   │    │ select   │    │output  ││
│   │  want    │    │ creation │    │  budget  │    │ prepare  │    │        ││
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘    └────────┘│
│                                                                              │
│   ❌ NO execution before this pipeline completes                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pipeline Stages:

| Stage | Purpose | Output |
|-------|---------|--------|
| **1. Intent** | Understand what the human wants | Clarified request |
| **2. Encoding** | Translate to governed instruction schema | `.chenu` encoding |
| **3. Governance** | Check scope, budget, permissions | Validation pass/fail |
| **4. Orchestration** | Select compatible agents | Agent assignment |
| **5. Execution** | Controlled, traced execution | Audited result |

---

## 🔐 CHE·NU Encoding Layer

The **key innovation** of CHE·NU.

The Encoding Layer translates human intent into a compact, structured, machine-readable semantic encoding.

### What the Encoding Does:
- ✅ Reduces ambiguity
- ✅ Reduces token usage
- ✅ Prevents hallucinations
- ✅ Enables governance BEFORE execution

### Encoding Schema

```json
{
  "encoding_version": "2.7",
  "intent_hash": "abc123...",
  
  "action": {
    "type": "ANALYZE | PREPARE | DRAFT | COMPARE | STRUCTURE",
    "verb": "specific action verb",
    "target": "what is being acted upon"
  },
  
  "source": {
    "type": "SEL | DOC | WS | EXT",
    "reference": "source identifier",
    "access_level": "read | write"
  },
  
  "scope": {
    "lock": "SEL | DOC | WS",
    "boundary": "strict | flexible",
    "expansion_allowed": false
  },
  
  "mode": {
    "type": "analysis | preparation | drafting | comparison | structuring",
    "depth": "surface | standard | deep",
    "format": "output format specification"
  },
  
  "focus": {
    "primary": "main focus area",
    "secondary": ["additional focuses"],
    "exclude": ["what to ignore"]
  },
  
  "permissions": {
    "rewrite_allowed": false,
    "create_new": false,
    "external_access": false,
    "human_approval_required": true
  },
  
  "governance": {
    "token_estimate": 1500,
    "budget_impact": 0.05,
    "sensitivity": "low | medium | high | critical",
    "audit_level": "standard | enhanced | full"
  },
  
  "traceability": {
    "thread_id": "thread_xxx",
    "parent_encoding": null,
    "version": 1,
    "created_at": "ISO timestamp"
  }
}
```

### Encoding is NOT a Prompt

| Prompt | CHE·NU Encoding |
|--------|-----------------|
| Free text | Structured schema |
| Ambiguous | Precise |
| Executed immediately | Validated first |
| No governance | Full governance |
| Unpredictable cost | Estimated cost |

---

## 📜 .chenu Threads

CHE·NU introduces a new primitive: the **`.chenu` thread**.

### What a Thread IS:
- ✅ A **governed interaction artifact**
- ✅ Contains intent, encoding, audit trail
- ✅ Universal (personal, enterprise, XR)
- ✅ Append-only version history

### What a Thread IS NOT:
- ❌ NOT a chat
- ❌ NOT a document
- ❌ NOT a task
- ❌ NOT a message

### Thread Structure

```
┌────────────────────────────────────────────────────────────┐
│                     .chenu THREAD                          │
├────────────────────────────────────────────────────────────┤
│  thread_id: "thread_xyz789"                                │
│  created_at: "2024-12-14T10:30:00Z"                       │
│  sphere: "enterprise"                                      │
│  owner: "user_abc123"                                      │
├────────────────────────────────────────────────────────────┤
│  INTENT                                                    │
│  ├── original_text: "..."                                  │
│  ├── clarified_intent: "..."                              │
│  └── intent_confidence: 0.95                              │
├────────────────────────────────────────────────────────────┤
│  ENCODING                                                  │
│  ├── raw_encoding: {...}                                  │
│  ├── optimized_encoding: {...}                            │
│  └── encoding_version: "2.7"                              │
├────────────────────────────────────────────────────────────┤
│  GOVERNANCE                                                │
│  ├── token_estimate: 1500                                 │
│  ├── budget_approved: true                                │
│  ├── scope_locked: "DOC"                                  │
│  └── permissions: {...}                                   │
├────────────────────────────────────────────────────────────┤
│  AGENT                                                     │
│  ├── compatible_agents: ["agent_a", "agent_b"]           │
│  ├── selected_agent: "agent_a"                            │
│  └── agent_confidence: 0.92                               │
├────────────────────────────────────────────────────────────┤
│  EXECUTION                                                 │
│  ├── status: "completed"                                  │
│  ├── result: {...}                                        │
│  ├── actual_tokens: 1423                                  │
│  └── duration_ms: 3456                                    │
├────────────────────────────────────────────────────────────┤
│  AUDIT TRAIL (append-only)                                │
│  ├── v1: {timestamp, action, actor}                       │
│  ├── v2: {timestamp, action, actor}                       │
│  └── ...                                                  │
└────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Orchestration

CHE·NU does NOT run "an AI". It orchestrates **specialized AI agents**.

### Before Execution Checklist

| Check | Description |
|-------|-------------|
| ☐ Intent clarified | Human intent understood |
| ☐ Encoding validated | Schema is complete and valid |
| ☐ Token estimated | Cost calculated |
| ☐ Scope locked | SEL/DOC/WS boundary set |
| ☐ Budget checked | Within allocation |
| ☐ Agent compatible | ACM verification passed |

Only then: **EXECUTE**

### Agent Categories (168+)

```
L0: Meta-Orchestrators (2)
L1: Sphere Directors (8)
L2: Domain Managers (32)
L3: Specialists (126+)
```

---

## 🌐 Spheres (NOT Apps)

### Available Spheres

| Sphere | Purpose |
|--------|---------|
| **Personal** | Tasks, finance, health, projects |
| **Enterprise** | Companies, teams, documents |
| **Creative Studio** | Design, content, media |
| **IA Labs** | Experiments, models, training |
| **Design Studio** | UI/UX, prototypes, assets |
| **Social Network** | Profiles, feeds, messages |
| **Community** | Marketplace, forums, events |
| **XR/Spatial** | AR/VR (future) |

Spheres are contextual containers, NOT silos.

---

## ✨ Nova

**Nova is NOT the main orchestrator.**

Nova is:
- ✅ The **guide**
- ✅ The **narrator**
- ✅ The **personal assistant**
- ✅ The **face of CHE·NU**

Users choose their own orchestrator agent separately.

---

## 🔀 Multi-LLM Router (15+ Providers)

| Provider | Models | Best For |
|----------|--------|----------|
| **Claude** | Opus, Sonnet, Haiku | Complex reasoning |
| **OpenAI** | GPT-4o, o1, o3 | General purpose |
| **Gemini** | Pro, Flash | Multimodal |
| **Grok** | Grok-2 | Real-time info |
| **DeepSeek** | V3, R1, Coder | Cost-effective |
| **Mistral** | Large, Codestral | European, Code |
| **Groq** | Llama 70B | Ultra-fast |
| **Perplexity** | Sonar | Search-augmented |
| **Ollama** | Local models | Privacy, Offline |

### BYOLLM Support
Users can bring their own LLM API keys.

---

## 🔒 Governance Mechanisms

### Scope Lock

| Scope | Description |
|-------|-------------|
| **SEL** | Selection only |
| **DOC** | Current document |
| **WS** | Workspace |

### Budget Control
- Token estimation before execution
- Per-sphere/project budgets
- Human approval for large requests

### Audit Trail
- Every action logged
- Append-only history
- Full traceability

---

## 💰 Monetization Philosophy

CHE·NU monetizes:
- ✅ **Governance**
- ✅ **Orchestration**
- ✅ **Efficiency**
- ✅ **Clarity**

CHE·NU does NOT monetize:
- ❌ Attention
- ❌ Volume
- ❌ Addiction

---

**© 2024 CHE·NU™ - Governed Intelligence Operating System**

*"No AI execution without human governance."*
