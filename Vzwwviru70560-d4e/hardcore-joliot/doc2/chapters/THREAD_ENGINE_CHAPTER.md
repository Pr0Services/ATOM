# CHE·NU™ — THREAD ENGINE CHAPTER
## Governed Intelligence Operating System

**Version:** 1.0.0  
**Status:** 🔒 CANONICAL  
**Module:** Core Engine  

---

## 📋 Overview

The Thread Engine is a **first-class object system** in CHE·NU that manages persistent lines of thought, conversations, and AI interactions. Threads (.chenu) are fundamental to the platform's memory and governance architecture.

---

## 🎯 Core Principles

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Threads are FIRST-CLASS OBJECTS in CHE·NU.               │
│   Every AI interaction exists within a Thread.              │
│   Threads have owners, scopes, budgets, and history.       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Thread Characteristics

| Property | Description |
|----------|-------------|
| **Owner** | User who created the thread |
| **Scope** | Sphere/Bureau context |
| **Budget** | Token allocation for AI operations |
| **Encoding** | Rules for message compression |
| **History** | Complete audit trail |
| **Auditable** | All decisions recorded |

---

## 🏗️ Architecture

### Thread Types

```python
class ThreadType(str, enum.Enum):
    CHAT = "chat"          # Standard conversation
    AGENT = "agent"        # Agent-driven thread
    TASK = "task"          # Task-focused thread
    WORKFLOW = "workflow"  # Multi-agent workflow
```

### Thread Status

```python
class ThreadStatus(str, enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
```

### Message Roles

```python
class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
```

---

## 📊 Data Model

### Thread Entity

```python
class Thread(Base):
    __tablename__ = "threads"
    
    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    
    # Identity
    title = Column(String(255), default="Nouvelle conversation")
    description = Column(Text, nullable=True)
    
    # Type & Status
    type = Column(Enum(ThreadType), default=ThreadType.CHAT)
    status = Column(Enum(ThreadStatus), default=ThreadStatus.ACTIVE)
    
    # Context (SPHERE INTEGRATION)
    sphere_id = Column(String(50), nullable=True)
    agent_id = Column(String(100), nullable=True)
    
    # AI Settings
    model = Column(String(100), default="claude-3-5-sonnet")
    temperature = Column(Float, default=0.7)
    system_prompt = Column(Text, nullable=True)
    
    # Metadata
    metadata = Column(JSON, default={})
    tags = Column(JSON, default=[])
    
    # Stats (GOVERNANCE)
    message_count = Column(Integer, default=0)
    token_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    last_message_at = Column(DateTime)
```

### Message Entity

```python
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID, primary_key=True)
    thread_id = Column(UUID, ForeignKey("threads.id"))
    
    # Content
    role = Column(Enum(MessageRole))
    content = Column(Text)
    content_type = Column(String(50))  # text, markdown, code, image
    
    # AI Metadata (GOVERNANCE)
    ai_metadata = Column(JSON)  # model, tokens, latency
    
    # Attachments
    attachments = Column(JSON, default=[])
    
    # Tool Integration
    tool_calls = Column(JSON)
    tool_results = Column(JSON)
    
    # Feedback (QUALITY)
    feedback_rating = Column(String(20))
    feedback_comment = Column(Text)
```

---

## 🔄 Service Layer

### ThreadService

```python
class ThreadService:
    """
    SAFE · NON-AUTONOMOUS · GOVERNED
    
    Service for managing threads and messages.
    All operations are auditable and reversible.
    """
    
    async def create_thread(self, user_id: str, data: ThreadCreate) -> Thread:
        """Create a new thread with optional initial message"""
        
    async def get_thread(self, thread_id: str, user_id: str) -> Thread:
        """Retrieve a thread (ownership verified)"""
        
    async def list_threads(
        self,
        user_id: str,
        sphere_id: Optional[str] = None,
        is_archived: bool = False,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[List[Thread], int]:
        """List threads with filtering and pagination"""
        
    async def chat(self, thread_id: str, user_id: str, data: ChatRequest) -> Message:
        """Send message and get AI response (GOVERNED)"""
        
    async def stream_chat(
        self,
        thread_id: str,
        user_id: str,
        data: ChatRequest
    ) -> AsyncGenerator[str, None]:
        """Stream AI response (GOVERNED)"""
        
    async def add_feedback(
        self,
        message_id: str,
        user_id: str,
        rating: str,
        comment: Optional[str] = None
    ) -> MessageFeedback:
        """Add feedback to a message (QUALITY TRACKING)"""
```

---

## 🌐 API Routes

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/threads/models` | List available LLM models |
| `POST` | `/api/threads` | Create new thread |
| `GET` | `/api/threads` | List user's threads |
| `GET` | `/api/threads/{id}` | Get thread with messages |
| `PATCH` | `/api/threads/{id}` | Update thread |
| `DELETE` | `/api/threads/{id}` | Delete thread |
| `POST` | `/api/threads/{id}/chat` | Send message, get response |
| `POST` | `/api/threads/{id}/chat/stream` | Stream response (SSE) |
| `POST` | `/api/threads/{id}/messages/{msg_id}/feedback` | Add feedback |

### Request Examples

```typescript
// Create Thread
POST /api/threads
{
  "sphere_id": "business",
  "title": "Project Planning",
  "model": "claude-3-5-sonnet",
  "initial_message": "Help me plan the Q1 roadmap"
}

// Chat
POST /api/threads/{id}/chat
{
  "message": "What are the key milestones?",
  "attachments": []
}

// Stream Chat
POST /api/threads/{id}/chat/stream
{
  "message": "Analyze this document",
  "attachments": [{ "type": "file", "id": "doc-123" }]
}
```

---

## 🔐 Governance Integration

### Token Budget

Every thread has a token budget managed by the Governance Engine:

```typescript
interface ThreadBudget {
  threadId: string;
  allocatedTokens: number;
  usedTokens: number;
  remainingTokens: number;
  warningThreshold: number;  // 80% default
}
```

### Audit Trail

All thread operations are logged:

```typescript
interface ThreadAuditEntry {
  threadId: string;
  userId: string;
  action: "create" | "message" | "archive" | "delete";
  timestamp: string;
  details: {
    tokensUsed?: number;
    modelUsed?: string;
    responseTime?: number;
  };
}
```

---

## 🔗 Sphere Integration

Threads exist within Spheres and follow the Bureau structure:

```
┌─────────────────────────────────────────────────────────────┐
│ SPHERE                                                      │
│   └── BUREAU                                                │
│         └── Section 5: Threads (.chenu)                     │
│               ├── Thread A (Chat)                           │
│               ├── Thread B (Agent)                          │
│               └── Thread C (Workflow)                       │
└─────────────────────────────────────────────────────────────┘
```

### Cross-Sphere Threads

Threads can reference data from multiple spheres but maintain their primary sphere assignment:

```typescript
interface ThreadContext {
  primarySphere: SphereKey;
  referencedSpheres: SphereKey[];
  crossSpherePermissions: Permission[];
}
```

---

## 📝 Encoding System

The Thread Engine integrates with CHE·NU's encoding layer for token optimization:

```typescript
interface ThreadEncoding {
  enabled: boolean;
  compressionLevel: "none" | "light" | "aggressive";
  preserveKeys: string[];  // Important terms to preserve
  qualityScore: number;    // 0-1 encoding quality
}
```

---

## 🔒 SAFE Compliance

```typescript
const THREAD_ENGINE_SAFE = {
  isRepresentational: true,
  noAutonomy: true,
  userOwnership: true,
  governedExecution: true,
  auditableHistory: true,
  reversibleActions: true
} as const;
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Files | 3 |
| Lines of Code | ~500 |
| API Endpoints | 9 |
| Thread Types | 4 |
| Message Roles | 4 |

---

## 🎯 Key Features

1. **First-Class Object**: Threads are not just containers but governed entities
2. **Sphere Scoping**: Every thread belongs to a sphere context
3. **Token Governance**: Built-in budget management
4. **Audit Trail**: Complete history of all operations
5. **Multi-Model**: Support for multiple LLM providers
6. **Streaming**: Real-time response streaming
7. **Feedback Loop**: Quality tracking via user feedback

---

*CHE·NU™ — Governed Intelligence Operating System*  
*Thread Engine v1.0.0*  
*© 2024-2025 PR0 Services Inc.*
