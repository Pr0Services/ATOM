"""
CHENU - Tests Unitaires
========================
Suite de tests complète avec pytest
Usage: pytest tests/ -v --cov=app --cov-report=html
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from uuid import uuid4

# ============================================
# FIXTURES
# ============================================

@pytest.fixture
def sample_task():
    """Fixture pour une tâche de test."""
    from app.models import Task, TaskStatus, TaskPriority
    return Task(
        id=f"task_{uuid4().hex[:8]}",
        description="Créer un article de blog sur l'IA",
        priority=TaskPriority.MEDIUM,
        status=TaskStatus.PENDING,
        context={"intent": "content", "original_request": "Créer un article"}
    )

@pytest.fixture
def sample_agent():
    """Fixture pour un agent de test."""
    from app.models import Agent, AgentLevel
    return Agent(
        id="creative_director",
        name="Directeur Créatif",
        level=AgentLevel.L1_DIRECTOR,
        description="Supervise la production créative",
        system_prompt="Tu es le Directeur Créatif...",
        tools=["brief_analyzer", "quality_checker"],
        delegates_to=["content_lead", "visual_lead"]
    )

@pytest.fixture
def mock_anthropic_client():
    """Mock du client Anthropic."""
    mock = Mock()
    mock.messages.create = Mock(return_value=Mock(
        content=[Mock(text="Voici l'article généré...")]
    ))
    return mock

@pytest.fixture
def orchestrator(mock_anthropic_client):
    """Fixture pour le Core Orchestrator."""
    from app.core.orchestrator import CoreOrchestrator
    with patch('anthropic.Anthropic', return_value=mock_anthropic_client):
        return CoreOrchestrator(api_key="test-key")

# ============================================
# TESTS: TASK MODELS
# ============================================

class TestTaskModel:
    """Tests pour le modèle Task."""
    
    def test_task_creation(self, sample_task):
        """Test création d'une tâche."""
        assert sample_task.id is not None
        assert sample_task.status.value == "pending"
        assert sample_task.priority.value == 2  # MEDIUM
    
    def test_task_status_transition(self, sample_task):
        """Test transition de statut."""
        from app.models import TaskStatus
        
        sample_task.status = TaskStatus.IN_PROGRESS
        assert sample_task.status == TaskStatus.IN_PROGRESS
        
        sample_task.status = TaskStatus.COMPLETED
        assert sample_task.status == TaskStatus.COMPLETED
    
    def test_task_with_result(self, sample_task):
        """Test tâche avec résultat."""
        from app.models import TaskStatus
        
        sample_task.status = TaskStatus.COMPLETED
        sample_task.result = {"content": "Article généré", "tokens": 500}
        sample_task.completed_at = datetime.now()
        
        assert sample_task.result is not None
        assert sample_task.completed_at is not None

# ============================================
# TESTS: AGENT MODELS
# ============================================

class TestAgentModel:
    """Tests pour le modèle Agent."""
    
    def test_agent_creation(self, sample_agent):
        """Test création d'un agent."""
        assert sample_agent.id == "creative_director"
        assert sample_agent.level.value == "L1"
        assert len(sample_agent.tools) == 2
    
    def test_agent_delegation(self, sample_agent):
        """Test capacité de délégation."""
        assert "content_lead" in sample_agent.delegates_to
        assert "visual_lead" in sample_agent.delegates_to
    
    def test_agent_can_delegate(self, sample_agent):
        """Test si l'agent peut déléguer."""
        from app.models import AgentLevel
        
        # L1 et L2 peuvent déléguer
        assert sample_agent.level in [AgentLevel.L1_DIRECTOR, AgentLevel.L2_MANAGER]
        assert len(sample_agent.delegates_to) > 0

# ============================================
# TESTS: TOOL REGISTRY
# ============================================

class TestToolRegistry:
    """Tests pour le registre d'outils."""
    
    def test_register_tool(self):
        """Test enregistrement d'un outil."""
        from app.core.tools import ToolRegistry, Tool
        
        registry = ToolRegistry()
        tool = Tool(
            id="test_tool",
            name="Test Tool",
            description="Un outil de test",
            cost=100
        )
        
        registry.register(tool)
        assert registry.get("test_tool") is not None
    
    def test_execute_tool(self):
        """Test exécution d'un outil."""
        from app.core.tools import ToolRegistry, Tool
        
        registry = ToolRegistry()
        handler = Mock(return_value={"status": "success"})
        
        tool = Tool(
            id="test_tool",
            name="Test Tool",
            description="Test",
            cost=100,
            handler=handler
        )
        registry.register(tool)
        
        result = registry.execute("test_tool", {"param1": "value1"})
        assert result["status"] == "success"
        handler.assert_called_once_with(param1="value1")
    
    def test_tool_not_found(self):
        """Test outil non trouvé."""
        from app.core.tools import ToolRegistry
        
        registry = ToolRegistry()
        
        with pytest.raises(ValueError, match="Tool not found"):
            registry.execute("nonexistent_tool", {})

# ============================================
# TESTS: TASK QUEUE
# ============================================

class TestTaskQueue:
    """Tests pour la file de tâches."""
    
    def test_add_task(self, sample_task):
        """Test ajout d'une tâche."""
        from app.core.queue import TaskQueue
        
        queue = TaskQueue()
        queue.add(sample_task)
        
        assert queue.get_next() == sample_task
    
    def test_priority_ordering(self):
        """Test ordonnancement par priorité."""
        from app.core.queue import TaskQueue
        from app.models import Task, TaskPriority
        
        queue = TaskQueue()
        
        low_task = Task(id="low", description="Low", priority=TaskPriority.LOW)
        high_task = Task(id="high", description="High", priority=TaskPriority.HIGH)
        critical_task = Task(id="critical", description="Critical", priority=TaskPriority.CRITICAL)
        
        queue.add(low_task)
        queue.add(high_task)
        queue.add(critical_task)
        
        # Critical devrait être premier
        next_task = queue.get_next()
        assert next_task.id == "critical"
    
    def test_update_status(self, sample_task):
        """Test mise à jour du statut."""
        from app.core.queue import TaskQueue
        from app.models import TaskStatus
        
        queue = TaskQueue()
        queue.add(sample_task)
        
        queue.update_status(sample_task.id, TaskStatus.COMPLETED, {"result": "done"})
        
        assert queue._tasks[sample_task.id].status == TaskStatus.COMPLETED
        assert queue._tasks[sample_task.id].result == {"result": "done"}

# ============================================
# TESTS: LLM ROUTER
# ============================================

class TestLLMRouter:
    """Tests pour le routeur LLM."""
    
    def test_model_selection_critical(self, sample_task):
        """Test sélection modèle pour tâche critique."""
        from app.core.llm import LLMRouter
        from app.models import TaskPriority
        
        sample_task.priority = TaskPriority.CRITICAL
        
        with patch('anthropic.Anthropic'):
            router = LLMRouter(api_key="test")
            model = router.select_model(sample_task)
            
            assert "opus" in model
    
    def test_model_selection_low(self, sample_task):
        """Test sélection modèle pour tâche basse priorité."""
        from app.core.llm import LLMRouter
        from app.models import TaskPriority
        
        sample_task.priority = TaskPriority.LOW
        
        with patch('anthropic.Anthropic'):
            router = LLMRouter(api_key="test")
            model = router.select_model(sample_task)
            
            assert "haiku" in model

# ============================================
# TESTS: CORE ORCHESTRATOR
# ============================================

class TestCoreOrchestrator:
    """Tests pour le Core Orchestrator."""
    
    @pytest.mark.asyncio
    async def test_process_request(self, orchestrator):
        """Test traitement d'une requête."""
        result = await orchestrator.process_request(
            "Crée un article de blog sur l'IA"
        )
        
        assert result["status"] == "success"
        assert "task_id" in result
    
    @pytest.mark.asyncio
    async def test_analyze_intent(self, orchestrator):
        """Test analyse d'intention."""
        intent = await orchestrator._analyze_intent(
            "Crée une campagne marketing sur LinkedIn"
        )
        
        assert "category" in intent
        assert "complexity" in intent
        assert "required_skills" in intent
    
    def test_route_to_director(self, orchestrator):
        """Test routage vers directeur."""
        intent = {"category": "content", "complexity": "medium"}
        director = orchestrator._route_to_director(intent)
        
        assert director is not None
        assert director.level.value == "L1"
    
    def test_determine_priority(self, orchestrator):
        """Test détermination priorité."""
        from app.models import TaskPriority
        
        low_intent = {"complexity": "low"}
        high_intent = {"complexity": "high"}
        
        assert orchestrator._determine_priority(low_intent) == TaskPriority.LOW
        assert orchestrator._determine_priority(high_intent) == TaskPriority.HIGH

# ============================================
# TESTS: INTEGRATIONS
# ============================================

class TestClickUpIntegration:
    """Tests pour l'intégration ClickUp."""
    
    @pytest.mark.asyncio
    async def test_create_task(self):
        """Test création de tâche ClickUp."""
        from app.integrations.clickup import ClickUpIntegration, IntegrationConfig
        
        config = IntegrationConfig(
            name="ClickUp",
            api_key="test-key",
            base_url="https://api.clickup.com/api/v2",
            workspace_id="team123",
            extra={"default_list_id": "list123"}
        )
        
        integration = ClickUpIntegration(config)
        
        with patch.object(integration, '_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"id": "task123", "name": "Test"}
            
            integration.session = Mock()  # Mock session
            result = await integration.create_task(
                list_id="list123",
                name="Test Task",
                description="Description"
            )
            
            assert result["id"] == "task123"
            mock_request.assert_called_once()

class TestNotionIntegration:
    """Tests pour l'intégration Notion."""
    
    def test_text_block_creation(self):
        """Test création de bloc texte."""
        from app.integrations.notion import NotionIntegration
        
        block = NotionIntegration.text_block("Hello World")
        
        assert block["type"] == "paragraph"
        assert block["paragraph"]["rich_text"][0]["text"]["content"] == "Hello World"
    
    def test_heading_block_creation(self):
        """Test création de bloc heading."""
        from app.integrations.notion import NotionIntegration
        
        block = NotionIntegration.heading_block("Mon Titre", level=2)
        
        assert block["type"] == "heading_2"

# ============================================
# TESTS: WORKFLOWS
# ============================================

class TestWorkflowExecution:
    """Tests pour l'exécution des workflows."""
    
    @pytest.mark.asyncio
    async def test_workflow_step_execution(self):
        """Test exécution d'une étape de workflow."""
        from app.workflows.engine import WorkflowEngine
        
        engine = WorkflowEngine()
        
        step = {
            "agent": "copywriter",
            "action": "Rédiger le contenu",
            "expected_output": "Texte brut"
        }
        
        with patch.object(engine, '_execute_step', new_callable=AsyncMock) as mock_exec:
            mock_exec.return_value = {"content": "Article généré"}
            
            result = await engine._execute_step(step, {})
            
            assert result["content"] == "Article généré"
    
    def test_workflow_validation(self):
        """Test validation d'un workflow."""
        from app.workflows.validator import WorkflowValidator
        
        valid_workflow = {
            "name": "Content Creation",
            "steps": [
                {"agent": "writer", "action": "write"},
                {"agent": "editor", "action": "edit"}
            ]
        }
        
        validator = WorkflowValidator()
        assert validator.validate(valid_workflow) is True
    
    def test_invalid_workflow(self):
        """Test workflow invalide."""
        from app.workflows.validator import WorkflowValidator
        
        invalid_workflow = {
            "name": "Empty Workflow",
            "steps": []
        }
        
        validator = WorkflowValidator()
        assert validator.validate(invalid_workflow) is False

# ============================================
# TESTS: API ENDPOINTS
# ============================================

class TestAPIEndpoints:
    """Tests pour les endpoints API."""
    
    @pytest.fixture
    def client(self):
        """Client de test FastAPI."""
        from fastapi.testclient import TestClient
        from app.main import app
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test endpoint de santé."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_create_task_endpoint(self, client):
        """Test création de tâche via API."""
        response = client.post("/api/v1/tasks", json={
            "description": "Test task",
            "priority": "medium"
        })
        
        assert response.status_code in [200, 201]
        assert "id" in response.json()
    
    def test_get_agents_endpoint(self, client):
        """Test liste des agents."""
        response = client.get("/api/v1/agents")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)

# ============================================
# TESTS: PERFORMANCE
# ============================================

class TestPerformance:
    """Tests de performance."""
    
    @pytest.mark.asyncio
    async def test_concurrent_tasks(self, orchestrator):
        """Test exécution concurrente de tâches."""
        tasks = [
            orchestrator.process_request(f"Task {i}")
            for i in range(5)
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        assert all(r["status"] == "success" for r in results)
    
    def test_queue_performance(self):
        """Test performance de la queue."""
        from app.core.queue import TaskQueue
        from app.models import Task, TaskPriority
        import time
        
        queue = TaskQueue()
        
        start = time.time()
        for i in range(1000):
            task = Task(id=f"task_{i}", description=f"Task {i}")
            queue.add(task)
        elapsed = time.time() - start
        
        # Devrait prendre moins de 1 seconde pour 1000 tâches
        assert elapsed < 1.0

# ============================================
# CONFIGURATION PYTEST
# ============================================

# conftest.py content
"""
# pytest.ini or pyproject.toml:

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

# To run:
# pytest                          # All tests
# pytest -v                       # Verbose
# pytest --cov=app                # With coverage
# pytest -k "test_task"           # Filter by name
# pytest -m "not slow"            # Exclude slow tests
"""
