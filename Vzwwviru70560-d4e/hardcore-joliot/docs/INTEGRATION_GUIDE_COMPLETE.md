# 🔧 GUIDE D'INTÉGRATION — MY TEAM + ENTERTAINMENT V41

**Date:** 21 Décembre 2025  
**Version:** V41 Complete Integration  
**Projet:** CHE·NU ULTIMATE V41

---

## 📦 FICHIERS CRÉÉS

### Backend Python (4 fichiers - 1,592 lignes)

1. **backend_myteam_entertainment_migration.py** (628 lignes)
   - Migration Alembic complète
   - 20 tables SQL

2. **backend_models_myteam.py** (355 lignes)
   - 12 modèles SQLAlchemy My Team
   
3. **backend_models_entertainment.py** (241 lignes)
   - 8 modèles SQLAlchemy Entertainment

4. **backend_schemas_myteam.py** (368 lignes)
   - Schémas Pydantic validation

---

## 🗂️ STRUCTURE D'INTÉGRATION

### Où placer chaque fichier dans CHENU_ULTIMATE_PACKAGE:

```
CHENU_ULTIMATE_PACKAGE/
│
├── backend/
│   ├── alembic/versions/
│   │   └── v41_001_myteam_entertainment_complete.py ← backend_myteam_entertainment_migration.py
│   │
│   ├── models/
│   │   ├── myteam/
│   │   │   ├── __init__.py ← CRÉER
│   │   │   ├── employee.py ← EXTRAIRE de backend_models_myteam.py
│   │   │   ├── agent.py ← EXTRAIRE de backend_models_myteam.py
│   │   │   ├── skill.py ← EXTRAIRE de backend_models_myteam.py
│   │   │   ├── prompt.py ← EXTRAIRE de backend_models_myteam.py
│   │   │   ├── memory.py ← EXTRAIRE de backend_models_myteam.py
│   │   │   └── workflow.py ← EXTRAIRE de backend_models_myteam.py
│   │   │
│   │   └── entertainment/
│   │       ├── __init__.py ← CRÉER
│   │       ├── content.py ← EXTRAIRE de backend_models_entertainment.py
│   │       ├── wellbeing.py ← EXTRAIRE de backend_models_entertainment.py
│   │       ├── gaming.py ← EXTRAIRE de backend_models_entertainment.py
│   │       ├── travel.py ← EXTRAIRE de backend_models_entertainment.py
│   │       └── restaurants.py ← EXTRAIRE de backend_models_entertainment.py
│   │
│   ├── schemas/
│   │   ├── myteam/
│   │   │   ├── __init__.py ← CRÉER
│   │   │   ├── employee_schemas.py ← EXTRAIRE
│   │   │   ├── agent_schemas.py ← EXTRAIRE  
│   │   │   ├── skill_schemas.py ← EXTRAIRE
│   │   │   ├── prompt_schemas.py ← EXTRAIRE
│   │   │   └── memory_schemas.py ← EXTRAIRE
│   │   │
│   │   └── entertainment/
│   │       ├── __init__.py ← CRÉER
│   │       ├── content_schemas.py ← À CRÉER
│   │       ├── wellbeing_schemas.py ← À CRÉER
│   │       └── gaming_schemas.py ← À CRÉER
│   │
│   ├── api/
│   │   ├── myteam/
│   │   │   ├── __init__.py ← CRÉER
│   │   │   ├── employees.py ← À CRÉER
│   │   │   ├── agents.py ← À CRÉER
│   │   │   ├── skills.py ← À CRÉER
│   │   │   ├── prompts.py ← À CRÉER
│   │   │   └── memory.py ← À CRÉER
│   │   │
│   │   └── entertainment/
│   │       ├── __init__.py ← CRÉER
│   │       ├── content.py ← À CRÉER
│   │       ├── wellbeing.py ← À CRÉER (PRIORITÉ!)
│   │       └── gaming.py ← À CRÉER
│   │
│   └── services/
│       ├── myteam/
│       │   ├── __init__.py ← CRÉER
│       │   ├── agent_service.py ← À CRÉER
│       │   ├── skill_service.py ← À CRÉER
│       │   ├── prompt_service.py ← À CRÉER
│       │   └── memory_service.py ← À CRÉER
│       │
│       └── entertainment/
│           ├── __init__.py ← CRÉER
│           ├── content_service.py ← À CRÉER
│           └── wellbeing_service.py ← À CRÉER (PRIORITÉ!)
```

---

## ⚙️ ÉTAPES D'INTÉGRATION

### PHASE 1: Préparer le Backend (10 min)

#### 1.1 Créer la structure de dossiers

```bash
cd CHENU_ULTIMATE_PACKAGE/backend

# Créer dossiers My Team
mkdir -p models/myteam schemas/myteam api/myteam services/myteam

# Créer dossiers Entertainment
mkdir -p models/entertainment schemas/entertainment api/entertainment services/entertainment

# Créer fichiers __init__.py
touch models/myteam/__init__.py
touch models/entertainment/__init__.py
touch schemas/myteam/__init__.py
touch schemas/entertainment/__init__.py
touch api/myteam/__init__.py
touch api/entertainment/__init__.py
touch services/myteam/__init__.py
touch services/entertainment/__init__.py
```

#### 1.2 Copier la migration

```bash
cp backend_myteam_entertainment_migration.py \
   backend/alembic/versions/v41_001_myteam_entertainment_complete.py
```

#### 1.3 Séparer les modèles My Team

Depuis `backend_models_myteam.py`, extraire chaque classe dans son fichier:

**backend/models/myteam/employee.py:**
```python
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from backend.database import Base

class Employee(Base):
    # ... copier la classe Employee
```

**backend/models/myteam/agent.py:**
```python
# ... copier la classe Agent
```

**Répéter pour:**
- skill.py
- methodology.py
- template.py
- prompt.py
- memory.py
- workflow.py
- assignments.py
- analytics.py

#### 1.4 Séparer les modèles Entertainment

Depuis `backend_models_entertainment.py`, extraire:

**backend/models/entertainment/content.py:**
```python
# EntertainmentContent, EntertainmentWatchlist, EntertainmentUsage
```

**backend/models/entertainment/wellbeing.py:**
```python
# EntertainmentWellbeing (PRIORITÉ!)
```

**backend/models/entertainment/gaming.py:**
```python
# GamingLibrary
```

**backend/models/entertainment/travel.py:**
```python
# TravelTrip
```

**backend/models/entertainment/restaurants.py:**
```python
# RestaurantFavorite, HobbyTracking
```

### PHASE 2: Appliquer la Migration (5 min)

```bash
cd CHENU_ULTIMATE_PACKAGE/backend

# Générer la migration
alembic revision --autogenerate -m "my_team_entertainment_complete_v41"

# OU utiliser directement notre migration
# (Renommer v41_001_myteam_entertainment_complete.py avec bon revision ID)

# Appliquer
alembic upgrade head

# Vérifier
alembic current
psql -d chenu_db -c "\dt" # Lister toutes les tables
```

### PHASE 3: Créer les Schémas Pydantic (20 min)

Séparer `backend_schemas_myteam.py` en:

**backend/schemas/myteam/employee_schemas.py:**
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from enum import Enum

class EmployeeStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    on_leave = "on_leave"

class EmployeeBase(BaseModel):
    # ... copier les classes Employee*
```

**Répéter pour:**
- agent_schemas.py
- skill_schemas.py
- prompt_schemas.py
- memory_schemas.py

**Créer Entertainment schemas:**

**backend/schemas/entertainment/wellbeing_schemas.py:**
```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from uuid import UUID

class WellbeingSettings(BaseModel):
    daily_limit_minutes: int = Field(120, ge=0, le=1440)
    session_limit_minutes: int = Field(60, ge=0, le=480)
    enforce_mode: str = Field("soft", regex="^(soft|hard)$")
    pause_reminders_enabled: bool = True
    healthy_alternatives_enabled: bool = True

class WellbeingCreate(WellbeingSettings):
    pass

class WellbeingUpdate(BaseModel):
    daily_limit_minutes: Optional[int] = Field(None, ge=0, le=1440)
    session_limit_minutes: Optional[int] = Field(None, ge=0, le=480)
    enforce_mode: Optional[str] = None
    pause_reminders_enabled: Optional[bool] = None
    healthy_alternatives_enabled: Optional[bool] = None

class WellbeingResponse(WellbeingSettings):
    id: UUID
    user_id: UUID
    today_usage_minutes: int
    today_sessions: int
    last_warning_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UsageStatus(BaseModel):
    status: str  # ok, warning, limit_reached
    message: str
    remaining_minutes: Optional[int] = None
    suggestions: Optional[List[Dict[str, str]]] = None
```

### PHASE 4: Créer les API Routes (40 min)

#### 4.1 My Team - Agents API

**backend/api/myteam/agents.py:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.database import get_db
from backend.models.myteam.agent import Agent
from backend.schemas.myteam.agent_schemas import (
    AgentCreate, AgentUpdate, AgentResponse, AgentListResponse
)
from backend.services.myteam.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["My Team - Agents"])

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Créer un nouvel agent IA"""
    service = AgentService(db)
    return await service.create_agent(current_user_id, agent_data)

@router.get("/", response_model=AgentListResponse)
async def list_agents(
    sphere_id: Optional[str] = None,
    level: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Liste tous les agents avec filtres"""
    service = AgentService(db)
    return await service.list_agents(
        current_user_id, 
        sphere_id=sphere_id,
        level=level,
        status=status,
        page=page,
        page_size=page_size
    )

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Récupérer un agent par ID"""
    service = AgentService(db)
    agent = await service.get_agent(current_user_id, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Modifier un agent (utilisé depuis IA Labs)"""
    service = AgentService(db)
    return await service.update_agent(current_user_id, agent_id, agent_data)

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Supprimer un agent"""
    service = AgentService(db)
    await service.delete_agent(current_user_id, agent_id)

@router.get("/{agent_id}/memory", response_model=List[AgentMemoryResponse])
async def get_agent_memory(
    agent_id: UUID,
    memory_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Récupérer la mémoire contrôlée d'un agent"""
    service = AgentService(db)
    return await service.get_agent_memory(current_user_id, agent_id, memory_type)

@router.post("/{agent_id}/skills/{skill_id}")
async def assign_skill_to_agent(
    agent_id: UUID,
    skill_id: UUID,
    proficiency_level: str,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Assigner un skill à un agent"""
    service = AgentService(db)
    return await service.assign_skill(current_user_id, agent_id, skill_id, proficiency_level)
```

#### 4.2 My Team - Prompts API

**backend/api/myteam/prompts.py:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.database import get_db
from backend.models.myteam.prompt import Prompt
from backend.schemas.myteam.prompt_schemas import (
    PromptCreate, PromptUpdate, PromptResponse, PromptListResponse
)
from backend.services.myteam.prompt_service import PromptService

router = APIRouter(prefix="/prompts", tags=["My Team - Prompts"])

@router.post("/", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    prompt_data: PromptCreate,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Créer un nouveau prompt"""
    service = PromptService(db)
    return await service.create_prompt(current_user_id, prompt_data)

@router.get("/", response_model=PromptListResponse)
async def list_prompts(
    category: Optional[str] = None,
    is_template: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Liste tous les prompts"""
    service = PromptService(db)
    return await service.list_prompts(
        current_user_id,
        category=category,
        is_template=is_template,
        page=page,
        page_size=page_size
    )

@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Récupérer un prompt par ID"""
    service = PromptService(db)
    prompt = await service.get_prompt(current_user_id, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: UUID,
    prompt_data: PromptUpdate,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Modifier un prompt"""
    service = PromptService(db)
    return await service.update_prompt(current_user_id, prompt_id, prompt_data)

@router.post("/{prompt_id}/test")
async def test_prompt(
    prompt_id: UUID,
    variables: dict,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Tester un prompt dans le playground"""
    service = PromptService(db)
    return await service.test_prompt(current_user_id, prompt_id, variables)
```

#### 4.3 Entertainment - Wellbeing API (PRIORITÉ!)

**backend/api/entertainment/wellbeing.py:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from backend.database import get_db
from backend.schemas.entertainment.wellbeing_schemas import (
    WellbeingCreate, WellbeingUpdate, WellbeingResponse, UsageStatus
)
from backend.services.entertainment.wellbeing_service import WellbeingService

router = APIRouter(prefix="/wellbeing", tags=["Entertainment - Wellbeing"])

@router.get("/", response_model=WellbeingResponse)
async def get_wellbeing_settings(
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Récupérer les paramètres wellbeing de l'utilisateur"""
    service = WellbeingService(db)
    settings = await service.get_settings(current_user_id)
    if not settings:
        # Créer settings par défaut
        return await service.create_default_settings(current_user_id)
    return settings

@router.put("/", response_model=WellbeingResponse)
async def update_wellbeing_settings(
    settings_data: WellbeingUpdate,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Modifier les paramètres wellbeing"""
    service = WellbeingService(db)
    return await service.update_settings(current_user_id, settings_data)

@router.get("/status", response_model=UsageStatus)
async def check_usage_status(
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Vérifier le statut d'usage actuel (limite atteinte?)"""
    service = WellbeingService(db)
    return await service.check_usage_limit(current_user_id)

@router.post("/session/start")
async def start_session(
    content_id: UUID,
    content_type: str,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Démarrer une session de streaming"""
    service = WellbeingService(db)
    return await service.start_session(current_user_id, content_id, content_type)

@router.post("/session/end")
async def end_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Terminer une session (calcul durée, mise à jour usage)"""
    service = WellbeingService(db)
    return await service.end_session(current_user_id, session_id)

@router.get("/alternatives")
async def get_healthy_alternatives(
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id)
):
    """Suggérer des alternatives saines"""
    service = WellbeingService(db)
    return await service.suggest_alternatives(current_user_id)
```

### PHASE 5: Créer les Services (30 min)

#### 5.1 Agent Service

**backend/services/myteam/agent_service.py:**
```python
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.models.myteam.agent import Agent
from backend.models.myteam.memory import AgentMemory
from backend.schemas.myteam.agent_schemas import AgentCreate, AgentUpdate

class AgentService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_agent(self, user_id: UUID, agent_data: AgentCreate) -> Agent:
        """Créer un nouvel agent"""
        agent = Agent(
            user_id=user_id,
            **agent_data.dict()
        )
        self.db.add(agent)
        self.db.commit()
        self.db.refresh(agent)
        return agent
    
    async def get_agent(self, user_id: UUID, agent_id: UUID) -> Optional[Agent]:
        """Récupérer un agent"""
        return self.db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.user_id == user_id
        ).first()
    
    async def list_agents(
        self,
        user_id: UUID,
        sphere_id: Optional[str] = None,
        level: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        """Lister agents avec filtres"""
        query = self.db.query(Agent).filter(Agent.user_id == user_id)
        
        if level:
            query = query.filter(Agent.level == level)
        if status:
            query = query.filter(Agent.status == status)
        
        total = query.count()
        offset = (page - 1) * page_size
        agents = query.offset(offset).limit(page_size).all()
        
        return {
            "agents": agents,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    
    async def update_agent(
        self,
        user_id: UUID,
        agent_id: UUID,
        agent_data: AgentUpdate
    ) -> Agent:
        """Modifier un agent (IA Labs)"""
        agent = await self.get_agent(user_id, agent_id)
        if not agent:
            raise ValueError("Agent not found")
        
        for field, value in agent_data.dict(exclude_unset=True).items():
            setattr(agent, field, value)
        
        self.db.commit()
        self.db.refresh(agent)
        return agent
    
    async def delete_agent(self, user_id: UUID, agent_id: UUID):
        """Supprimer un agent"""
        agent = await self.get_agent(user_id, agent_id)
        if not agent:
            raise ValueError("Agent not found")
        
        self.db.delete(agent)
        self.db.commit()
    
    async def get_agent_memory(
        self,
        user_id: UUID,
        agent_id: UUID,
        memory_type: Optional[str] = None
    ) -> List[AgentMemory]:
        """Récupérer mémoire contrôlée"""
        query = self.db.query(AgentMemory).filter(
            AgentMemory.agent_id == agent_id
        )
        
        if memory_type:
            query = query.filter(AgentMemory.type == memory_type)
        
        return query.all()
```

#### 5.2 Wellbeing Service (PRIORITÉ!)

**backend/services/entertainment/wellbeing_service.py:**
```python
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional, List, Dict
from uuid import UUID

from backend.models.entertainment.wellbeing import EntertainmentWellbeing
from backend.models.entertainment.content import EntertainmentUsage
from backend.schemas.entertainment.wellbeing_schemas import (
    WellbeingUpdate, UsageStatus
)

class WellbeingService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_settings(self, user_id: UUID) -> Optional[EntertainmentWellbeing]:
        """Récupérer settings wellbeing"""
        return self.db.query(EntertainmentWellbeing).filter(
            EntertainmentWellbeing.user_id == user_id
        ).first()
    
    async def create_default_settings(self, user_id: UUID) -> EntertainmentWellbeing:
        """Créer settings par défaut"""
        settings = EntertainmentWellbeing(
            user_id=user_id,
            daily_limit_minutes=120,  # 2h default
            session_limit_minutes=60,  # 1h default
            enforce_mode='soft',
            pause_reminders_enabled=True,
            healthy_alternatives_enabled=True
        )
        self.db.add(settings)
        self.db.commit()
        self.db.refresh(settings)
        return settings
    
    async def check_usage_limit(self, user_id: UUID) -> UsageStatus:
        """Vérifier limite usage (ANTI-ADDICTION)"""
        settings = await self.get_settings(user_id)
        if not settings:
            settings = await self.create_default_settings(user_id)
        
        # Calculer usage aujourd'hui
        today = date.today()
        usage_today = self.db.query(EntertainmentUsage).filter(
            EntertainmentUsage.user_id == user_id,
            EntertainmentUsage.date == today
        ).all()
        
        total_minutes = sum(u.duration_minutes or 0 for u in usage_today)
        settings.today_usage_minutes = total_minutes
        
        # Vérifier limite
        percent_used = (total_minutes / settings.daily_limit_minutes) * 100
        
        if total_minutes >= settings.daily_limit_minutes:
            return UsageStatus(
                status="limit_reached",
                message="Tu as atteint ta limite quotidienne de streaming! 🚫",
                remaining_minutes=0,
                suggestions=await self.suggest_alternatives(user_id)
            )
        elif percent_used >= 90:
            return UsageStatus(
                status="warning",
                message=f"Plus que {settings.daily_limit_minutes - total_minutes} minutes aujourd'hui ⚠️",
                remaining_minutes=settings.daily_limit_minutes - total_minutes
            )
        else:
            return UsageStatus(
                status="ok",
                message="Usage normal ✅",
                remaining_minutes=settings.daily_limit_minutes - total_minutes
            )
    
    async def suggest_alternatives(self, user_id: UUID) -> List[Dict[str, str]]:
        """Suggérer alternatives saines (ANTI-ADDICTION)"""
        return [
            {"type": "exercise", "activity": "Marche 15 min dehors 🚶", "sphere": "personal"},
            {"type": "social", "activity": "Appelle un ami 📞", "sphere": "community"},
            {"type": "creative", "activity": "Dessine ou écris quelque chose ✏️", "sphere": "creative"},
            {"type": "learning", "activity": "Lis 10 pages d'un livre 📚", "sphere": "scholar"},
            {"type": "mindfulness", "activity": "Médite 5 minutes 🧘", "sphere": "personal"}
        ]
```

### PHASE 6: Enregistrer les Routes (5 min)

**backend/main.py ou backend/api/__init__.py:**
```python
from fastapi import FastAPI
from backend.api.myteam import agents, prompts, skills, memory
from backend.api.entertainment import wellbeing, content, gaming

app = FastAPI(title="CHE·NU API V41")

# My Team routes
app.include_router(agents.router, prefix="/api/v1/myteam")
app.include_router(prompts.router, prefix="/api/v1/myteam")
app.include_router(skills.router, prefix="/api/v1/myteam")
app.include_router(memory.router, prefix="/api/v1/myteam")

# Entertainment routes
app.include_router(wellbeing.router, prefix="/api/v1/entertainment")
app.include_router(content.router, prefix="/api/v1/entertainment")
app.include_router(gaming.router, prefix="/api/v1/entertainment")
```

---

## 🧪 TESTS

### Test Migration

```bash
# Test création tables
psql -d chenu_db -c "SELECT tablename FROM pg_tables WHERE schemaname='public';"

# Vérifier structure
psql -d chenu_db -c "\d agents"
psql -d chenu_db -c "\d prompts"
psql -d chenu_db -c "\d entertainment_wellbeing"
```

### Test API (avec curl)

```bash
# Test create agent
curl -X POST "http://localhost:8000/api/v1/myteam/agents" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Agent",
    "type": "specialist",
    "level": "L1",
    "llm_model": "gpt-4"
  }'

# Test wellbeing status
curl "http://localhost:8000/api/v1/entertainment/wellbeing/status"

# Test create prompt
curl -X POST "http://localhost:8000/api/v1/myteam/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Analysis Prompt",
    "category": "analysis",
    "system_prompt": "You are an expert analyst..."
  }'
```

---

## ✅ CHECKLIST FINALE

### Backend
- [ ] Migration appliquée (20 tables créées)
- [ ] Modèles SQLAlchemy importables
- [ ] Schémas Pydantic fonctionnels
- [ ] API routes enregistrées
- [ ] Services créés
- [ ] Tests passent

### Fonctionnalités Critiques
- [ ] Création agent fonctionne
- [ ] Modification agent (IA Labs) fonctionne
- [ ] Accès mémoire contrôlée fonctionne
- [ ] Création/modification prompts fonctionne
- [ ] Test prompt (playground) fonctionne
- [ ] **Wellbeing anti-addiction fonctionne** ⚠️
- [ ] Limites temps enforced
- [ ] Suggestions alternatives actives

### Frontend (À créer)
- [ ] Pages My Team
- [ ] IA Labs UI
- [ ] Agent card avec bouton "⚙️ IA Labs"
- [ ] Prompt editor
- [ ] Memory viewer
- [ ] Entertainment wellbeing UI

---

## 🎯 NEXT STEPS

1. **Appliquer migration** → Créer toutes les tables
2. **Tester API** → Vérifier endpoints
3. **Créer Frontend** → UI complète
4. **Intégrer Workflow Builder** → Ajouter agent nodes
5. **Tests E2E** → Tout fonctionne ensemble

---

**GUIDE CRÉÉ:** 21 Décembre 2025  
**READY TO INTEGRATE!** 🚀
