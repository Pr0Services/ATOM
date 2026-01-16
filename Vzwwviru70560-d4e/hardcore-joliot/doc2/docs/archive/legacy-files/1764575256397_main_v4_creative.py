"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🚀 CHENU V4.0 - CREATIVE STUDIO EDITION                                    ║
║   ═══════════════════════════════════════════                                ║
║                                                                              ║
║   Backend API avec:                                                          ║
║   • 60+ Agents Originaux                                                     ║
║   • 18 Agents Créatifs Spécialisés (NOUVEAU!)                               ║
║   • 50+ APIs Créatives (NOUVEAU!)                                           ║
║   • Système complet de gestion                                               ║
║                                                                              ║
║   "Une œuvre remplie de bonne volonté" 💜                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Import from models
from models import (
    SessionLocal, init_db, seed_agent_templates,
    User, Business, AgentTemplate, HiredAgent, 
    Project, Task, Database, DatabaseTable,
    Meeting, MeetingAgent, Message
)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎬 IMPORT CREATIVE STUDIO (NOUVEAU!)
# ═══════════════════════════════════════════════════════════════════════════════

from creative_studio_agents import (
    CREATIVE_AGENTS,
    CREATIVE_APIS,
    get_all_agents as get_creative_agents,
    get_agent as get_creative_agent,
    get_agents_by_department,
    get_all_apis,
    get_compatible_apis,
    get_studio_stats,
    FOLDER_STRUCTURE,
    PROJECT_INFO_TEMPLATE,
    Department
)

# ============================================================================
# APP SETUP
# ============================================================================

app = FastAPI(
    title="CHENU V4.0 - Creative Studio Edition",
    description="Multi-Agent Business Operating System avec Creative Studio intégré",
    version="4.0.0"
)

# CORS - Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATABASE DEPENDENCY
# ============================================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# PYDANTIC MODELS (Request/Response)
# ============================================================================

class UserCreate(BaseModel):
    email: str
    name: str

class BusinessCreate(BaseModel):
    name: str
    industry: Optional[str] = None

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "todo"

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class DatabaseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TableCreate(BaseModel):
    name: str

class MeetingCreate(BaseModel):
    name: str
    initial_agent_ids: Optional[List[str]] = []

class MessageCreate(BaseModel):
    content: str
    sender_type: Optional[str] = "user"
    sender_name: Optional[str] = "User"

class AgentHire(BaseModel):
    template_id: str
    name: Optional[str] = None
    api_keys: Optional[dict] = {}

class ConvokeAgent(BaseModel):
    agent_id: str
    briefing: Optional[dict] = {}

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database and Creative Studio on startup"""
    init_db()
    seed_agent_templates()
    
    # Seed Creative Studio agents into database
    db = SessionLocal()
    try:
        # Create demo user if not exists
        user = db.query(User).filter(User.id == "demo-user-123").first()
        if not user:
            user = User(
                id="demo-user-123",
                email="demo@chenu.ai",
                name="Demo User"
            )
            db.add(user)
            db.commit()
            print("✅ Demo user created!")
        
        # Add Creative Studio agents as templates
        for agent_id, agent_data in CREATIVE_AGENTS.items():
            existing = db.query(AgentTemplate).filter(AgentTemplate.id == agent_id).first()
            if not existing:
                template = AgentTemplate(
                    id=agent_id,
                    name=agent_data["name"],
                    role=agent_data["role"],
                    department=agent_data["department"],
                    icon=agent_data["avatar"],
                    description=agent_data["description"],
                    system_prompt=agent_data.get("catchphrase", ""),
                    skills=",".join(agent_data.get("skills", [])),
                    level=agent_data.get("level", 3),
                    cost_per_request=agent_data.get("cost_per_request", 0.05)
                )
                db.add(template)
        
        db.commit()
        print(f"✅ {len(CREATIVE_AGENTS)} Creative Studio agents loaded!")
        
    finally:
        db.close()
    
    # Print startup info
    stats = get_studio_stats()
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🚀 CHENU V4.0 - CREATIVE STUDIO EDITION - READY!                           ║
║                                                                              ║
║   📊 Creative Studio Stats:                                                  ║
║      • Creative Agents: {stats['total_agents']}                                              ║
║      • Creative APIs: {stats['total_apis']}                                               ║
║      • Departments: {stats['departments']}                                                 ║
║                                                                              ║
║   🌐 API Docs: http://localhost:8000/docs                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

# ============================================================================
# ROOT
# ============================================================================

@app.get("/")
async def root():
    stats = get_studio_stats()
    return {
        "name": "CHENU V4.0 - Creative Studio Edition",
        "status": "running",
        "creative_agents": stats["total_agents"],
        "creative_apis": stats["total_apis"],
        "docs": "/docs",
        "made_with": "💜 Love & Good Will"
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 🎬 CREATIVE STUDIO ENDPOINTS (NOUVEAU!)
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/creative-studio/stats")
async def creative_studio_stats():
    """Get Creative Studio statistics"""
    return get_studio_stats()

@app.get("/api/creative-studio/agents")
async def get_all_creative_agents():
    """Get all Creative Studio agents"""
    agents = []
    for agent_id, agent_data in CREATIVE_AGENTS.items():
        agents.append({
            "id": agent_id,
            "name": agent_data["name"],
            "role": agent_data["role"],
            "department": agent_data["department"],
            "avatar": agent_data["avatar"],
            "level": agent_data.get("level", 3),
            "personality": agent_data.get("personality", ""),
            "description": agent_data["description"],
            "catchphrase": agent_data.get("catchphrase", ""),
            "skills": agent_data.get("skills", []),
            "compatible_apis": agent_data.get("compatible_apis", []),
            "cost_per_request": agent_data.get("cost_per_request", 0.05)
        })
    
    return {
        "total": len(agents),
        "agents": agents
    }

@app.get("/api/creative-studio/agents/{agent_id}")
async def get_creative_agent_by_id(agent_id: str):
    """Get a specific Creative Studio agent"""
    agent = CREATIVE_AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Creative agent not found")
    
    return {
        "id": agent_id,
        **agent,
        "compatible_apis_details": [
            CREATIVE_APIS.get(api_id, {"name": api_id}) 
            for api_id in agent.get("compatible_apis", [])
        ]
    }

@app.get("/api/creative-studio/departments")
async def get_departments():
    """Get all departments with their agents"""
    departments = {}
    for dept in Department:
        dept_agents = get_agents_by_department(dept.value)
        departments[dept.name] = {
            "name": dept.value,
            "agent_count": len(dept_agents),
            "agents": list(dept_agents.keys())
        }
    
    return {"departments": departments}

@app.get("/api/creative-studio/departments/{department}")
async def get_department_agents(department: str):
    """Get all agents in a specific department"""
    # Find matching department
    matching_dept = None
    for dept in Department:
        if department.lower() in dept.value.lower() or department.lower() == dept.name.lower():
            matching_dept = dept
            break
    
    if not matching_dept:
        raise HTTPException(status_code=404, detail=f"Department '{department}' not found")
    
    agents = get_agents_by_department(matching_dept.value)
    
    return {
        "department": matching_dept.value,
        "agent_count": len(agents),
        "agents": [
            {
                "id": aid,
                "name": adata["name"],
                "role": adata["role"],
                "avatar": adata["avatar"],
                "catchphrase": adata.get("catchphrase", "")
            }
            for aid, adata in agents.items()
        ]
    }

@app.get("/api/creative-studio/apis")
async def get_all_creative_apis():
    """Get all Creative Studio APIs"""
    return {
        "total": len(CREATIVE_APIS),
        "apis": [
            {
                "id": api_id,
                **api_data
            }
            for api_id, api_data in CREATIVE_APIS.items()
        ]
    }

@app.get("/api/creative-studio/apis/{api_id}")
async def get_creative_api(api_id: str):
    """Get a specific API details"""
    api = CREATIVE_APIS.get(api_id)
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    
    # Find compatible agents
    compatible_agents = []
    for agent_id, agent_data in CREATIVE_AGENTS.items():
        if api_id in agent_data.get("compatible_apis", []):
            compatible_agents.append({
                "id": agent_id,
                "name": agent_data["name"],
                "avatar": agent_data["avatar"]
            })
    
    return {
        "id": api_id,
        **api,
        "compatible_agents": compatible_agents
    }

@app.get("/api/creative-studio/folder-structure")
async def get_folder_structure():
    """Get recommended folder structure for YouTube projects"""
    return {
        "structure": FOLDER_STRUCTURE,
        "template": PROJECT_INFO_TEMPLATE
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 👥 USERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.post("/api/users")
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        name=user_data.name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "name": user.name}

@app.get("/api/users/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email, "name": user.name}

# ═══════════════════════════════════════════════════════════════════════════════
# 🏢 BUSINESSES
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/users/{user_id}/businesses")
async def get_user_businesses(user_id: str, db: Session = Depends(get_db)):
    """Get all businesses for a user"""
    businesses = db.query(Business).filter(Business.owner_id == user_id).all()
    
    result = []
    for biz in businesses:
        agent_count = db.query(HiredAgent).filter(HiredAgent.business_id == biz.id).count()
        project_count = db.query(Project).filter(Project.business_id == biz.id).count()
        meeting_count = db.query(Meeting).filter(Meeting.business_id == biz.id).count()
        database_count = db.query(Database).filter(Database.business_id == biz.id).count()
        
        result.append({
            "id": biz.id,
            "name": biz.name,
            "industry": biz.industry,
            "is_primary": biz.is_primary,
            "agent_count": agent_count,
            "project_count": project_count,
            "meeting_count": meeting_count,
            "database_count": database_count
        })
    
    return {"businesses": result}

@app.post("/api/users/{user_id}/businesses")
async def create_business(user_id: str, business: BusinessCreate, db: Session = Depends(get_db)):
    """Create new business for user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_biz = Business(
        id=str(uuid.uuid4()),
        owner_id=user_id,
        name=business.name,
        industry=business.industry,
        is_primary=False
    )
    db.add(new_biz)
    db.commit()
    db.refresh(new_biz)
    
    return {
        "id": new_biz.id,
        "name": new_biz.name,
        "industry": new_biz.industry,
        "message": f"Business '{new_biz.name}' created!"
    }

@app.get("/api/businesses/{business_id}")
async def get_business(business_id: str, db: Session = Depends(get_db)):
    """Get business by ID"""
    biz = db.query(Business).filter(Business.id == business_id).first()
    if not biz:
        raise HTTPException(status_code=404, detail="Business not found")
    
    return {
        "id": biz.id,
        "name": biz.name,
        "industry": biz.industry,
        "is_primary": biz.is_primary
    }

@app.delete("/api/businesses/{business_id}")
async def delete_business(business_id: str, db: Session = Depends(get_db)):
    """Delete a business"""
    biz = db.query(Business).filter(Business.id == business_id).first()
    if not biz:
        raise HTTPException(status_code=404, detail="Business not found")
    
    db.delete(biz)
    db.commit()
    return {"message": "Business deleted"}

# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 AGENT TEMPLATES (Original + Creative)
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/agent-templates")
async def get_agent_templates(db: Session = Depends(get_db)):
    """Get all agent templates (original + creative)"""
    templates = db.query(AgentTemplate).all()
    
    result = []
    for t in templates:
        # Check if it's a creative agent
        is_creative = t.id in CREATIVE_AGENTS
        
        result.append({
            "id": t.id,
            "name": t.name,
            "role": t.role,
            "department": t.department,
            "icon": t.icon,
            "description": t.description,
            "level": t.level,
            "cost_per_request": t.cost_per_request,
            "skills": t.skills.split(",") if t.skills else [],
            "is_creative_studio": is_creative
        })
    
    return {"templates": result}

@app.get("/api/agent-templates/{template_id}")
async def get_agent_template(template_id: str, db: Session = Depends(get_db)):
    """Get a specific agent template"""
    template = db.query(AgentTemplate).filter(AgentTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # If creative agent, add extra info
    creative_data = CREATIVE_AGENTS.get(template_id, {})
    
    return {
        "id": template.id,
        "name": template.name,
        "role": template.role,
        "department": template.department,
        "icon": template.icon,
        "description": template.description,
        "system_prompt": template.system_prompt,
        "level": template.level,
        "cost_per_request": template.cost_per_request,
        "skills": template.skills.split(",") if template.skills else [],
        "is_creative_studio": template_id in CREATIVE_AGENTS,
        "personality": creative_data.get("personality", ""),
        "catchphrase": creative_data.get("catchphrase", ""),
        "compatible_apis": creative_data.get("compatible_apis", [])
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 HIRED AGENTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/businesses/{business_id}/agents")
async def get_business_agents(business_id: str, db: Session = Depends(get_db)):
    """Get all hired agents for a business"""
    agents = db.query(HiredAgent).filter(HiredAgent.business_id == business_id).all()
    
    result = []
    for agent in agents:
        template = db.query(AgentTemplate).filter(AgentTemplate.id == agent.template_id).first()
        creative_data = CREATIVE_AGENTS.get(agent.template_id, {})
        
        result.append({
            "id": agent.id,
            "name": agent.name,
            "template_id": agent.template_id,
            "status": agent.status,
            "template": {
                "name": template.name if template else "Unknown",
                "role": template.role if template else "",
                "department": template.department if template else "",
                "icon": template.icon if template else "🤖"
            } if template else None,
            "is_creative_studio": agent.template_id in CREATIVE_AGENTS,
            "catchphrase": creative_data.get("catchphrase", "")
        })
    
    return {"agents": result}

@app.post("/api/businesses/{business_id}/agents")
async def hire_agent(business_id: str, data: AgentHire, db: Session = Depends(get_db)):
    """Hire an agent for a business"""
    # Check business exists
    biz = db.query(Business).filter(Business.id == business_id).first()
    if not biz:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Check template exists
    template = db.query(AgentTemplate).filter(AgentTemplate.id == data.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Agent template not found")
    
    # Create hired agent
    agent = HiredAgent(
        id=str(uuid.uuid4()),
        business_id=business_id,
        template_id=data.template_id,
        name=data.name or template.name,
        status="available"
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    creative_data = CREATIVE_AGENTS.get(data.template_id, {})
    
    return {
        "id": agent.id,
        "name": agent.name,
        "template_id": agent.template_id,
        "status": agent.status,
        "is_creative_studio": data.template_id in CREATIVE_AGENTS,
        "welcome_message": creative_data.get("catchphrase", f"{agent.name} is ready to help!"),
        "message": f"Agent '{agent.name}' hired successfully!"
    }

@app.delete("/api/agents/{agent_id}")
async def fire_agent(agent_id: str, db: Session = Depends(get_db)):
    """Fire/remove an agent"""
    agent = db.query(HiredAgent).filter(HiredAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(agent)
    db.commit()
    return {"message": "Agent removed"}

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 PROJECTS & TASKS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/businesses/{business_id}/projects")
async def get_projects(business_id: str, db: Session = Depends(get_db)):
    """Get all projects for a business"""
    projects = db.query(Project).filter(Project.business_id == business_id).all()
    
    result = []
    for p in projects:
        task_count = db.query(Task).filter(Task.project_id == p.id).count()
        completed = db.query(Task).filter(Task.project_id == p.id, Task.status == "done").count()
        
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "status": p.status,
            "task_count": task_count,
            "completed_tasks": completed,
            "progress": (completed / task_count * 100) if task_count > 0 else 0
        })
    
    return {"projects": result}

@app.post("/api/businesses/{business_id}/projects")
async def create_project(business_id: str, data: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    project = Project(
        id=str(uuid.uuid4()),
        business_id=business_id,
        name=data.name,
        description=data.description,
        status="active"
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "id": project.id,
        "name": project.name,
        "message": f"Project '{project.name}' created!"
    }

@app.get("/api/projects/{project_id}/tasks")
async def get_tasks(project_id: str, db: Session = Depends(get_db)):
    """Get all tasks for a project"""
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    
    return {
        "tasks": [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "status": t.status,
                "priority": t.priority
            }
            for t in tasks
        ]
    }

@app.post("/api/projects/{project_id}/tasks")
async def create_task(project_id: str, data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    task = Task(
        id=str(uuid.uuid4()),
        project_id=project_id,
        name=data.name,
        description=data.description,
        status=data.status or "todo",
        priority=data.priority or "medium"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {
        "id": task.id,
        "name": task.name,
        "status": task.status,
        "message": f"Task '{task.name}' created!"
    }

# ═══════════════════════════════════════════════════════════════════════════════
# 💬 MEETINGS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/businesses/{business_id}/meetings")
async def get_meetings(business_id: str, db: Session = Depends(get_db)):
    """Get all meetings for a business"""
    meetings = db.query(Meeting).filter(Meeting.business_id == business_id).all()
    
    result = []
    for m in meetings:
        message_count = db.query(Message).filter(Message.meeting_id == m.id).count()
        active_agents = db.query(MeetingAgent).filter(
            MeetingAgent.meeting_id == m.id,
            MeetingAgent.status == "active"
        ).count()
        
        result.append({
            "id": m.id,
            "name": m.name,
            "status": m.status,
            "total_messages": message_count,
            "active_agent_count": active_agents,
            "total_tokens": m.total_tokens,
            "total_cost": m.total_cost
        })
    
    return {"meetings": result}

@app.post("/api/meetings")
async def create_meeting(data: MeetingCreate, business_id: str = None, db: Session = Depends(get_db)):
    """Create a new meeting"""
    meeting = Meeting(
        id=str(uuid.uuid4()),
        business_id=business_id or data.dict().get('business_id'),
        name=data.name,
        status="active",
        total_tokens=0,
        total_cost=0.0
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    
    return {
        "id": meeting.id,
        "name": meeting.name,
        "status": meeting.status,
        "message": f"Meeting '{meeting.name}' started!"
    }

@app.get("/api/meetings/{meeting_id}")
async def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    """Get meeting details with messages"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    messages = db.query(Message).filter(Message.meeting_id == meeting_id).order_by(Message.created_at).all()
    
    active_participations = db.query(MeetingAgent).filter(
        MeetingAgent.meeting_id == meeting_id,
        MeetingAgent.status == "active"
    ).all()
    
    active_agents = []
    for p in active_participations:
        agent = db.query(HiredAgent).filter(HiredAgent.id == p.agent_id).first()
        if agent:
            template = db.query(AgentTemplate).filter(AgentTemplate.id == agent.template_id).first()
            creative_data = CREATIVE_AGENTS.get(agent.template_id, {})
            active_agents.append({
                "id": agent.id,
                "name": agent.name,
                "icon": template.icon if template else "🤖",
                "is_creative": agent.template_id in CREATIVE_AGENTS,
                "catchphrase": creative_data.get("catchphrase", "")
            })
    
    return {
        "id": meeting.id,
        "name": meeting.name,
        "status": meeting.status,
        "total_tokens": meeting.total_tokens,
        "total_cost": meeting.total_cost,
        "active_agents": active_agents,
        "messages": [
            {
                "id": m.id,
                "content": m.content,
                "sender_type": m.sender_type,
                "sender_name": m.sender_name,
                "created_at": m.created_at.isoformat() if m.created_at else None,
                "tokens": m.tokens,
                "cost": m.cost
            }
            for m in messages
        ]
    }

@app.post("/api/meetings/{meeting_id}/messages")
async def send_message(meeting_id: str, data: MessageCreate, db: Session = Depends(get_db)):
    """Send a message in a meeting"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    message = Message(
        id=str(uuid.uuid4()),
        meeting_id=meeting_id,
        content=data.content,
        sender_type=data.sender_type or "user",
        sender_name=data.sender_name or "User",
        tokens=0,
        cost=0.0
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "id": message.id,
        "content": message.content,
        "sender_name": message.sender_name
    }

@app.post("/api/meetings/{meeting_id}/convoke")
async def convoke_agent(meeting_id: str, data: ConvokeAgent, db: Session = Depends(get_db)):
    """Add an agent to the meeting"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    agent = db.query(HiredAgent).filter(HiredAgent.id == data.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    existing = db.query(MeetingAgent).filter(
        MeetingAgent.meeting_id == meeting_id,
        MeetingAgent.agent_id == data.agent_id,
        MeetingAgent.status == "active"
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Agent already in meeting")
    
    ma = MeetingAgent(
        id=str(uuid.uuid4()),
        meeting_id=meeting_id,
        agent_id=data.agent_id,
        status="active"
    )
    db.add(ma)
    agent.status = "busy"
    
    # Get creative catchphrase
    creative_data = CREATIVE_AGENTS.get(agent.template_id, {})
    join_message = creative_data.get("catchphrase", f"{agent.name} has joined the meeting.")
    
    msg = Message(
        id=str(uuid.uuid4()),
        meeting_id=meeting_id,
        content=f"🎬 {agent.name} joined: \"{join_message}\"",
        sender_type="system",
        sender_name="System",
        tokens=0,
        cost=0.0
    )
    db.add(msg)
    db.commit()
    
    return {"message": f"{agent.name} joined the meeting", "catchphrase": join_message}

@app.post("/api/meetings/{meeting_id}/end")
async def end_meeting(meeting_id: str, db: Session = Depends(get_db)):
    """End a meeting"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting.status = "ended"
    meeting.ended_at = datetime.utcnow()
    
    participations = db.query(MeetingAgent).filter(
        MeetingAgent.meeting_id == meeting_id,
        MeetingAgent.status == "active"
    ).all()
    
    for p in participations:
        p.status = "released"
        agent = db.query(HiredAgent).filter(HiredAgent.id == p.agent_id).first()
        if agent:
            agent.status = "available"
    
    db.commit()
    
    return {"message": "Meeting ended"}

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 RUN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
