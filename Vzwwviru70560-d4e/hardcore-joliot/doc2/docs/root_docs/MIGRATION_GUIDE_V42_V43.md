# 🔄 MIGRATION GUIDE v42 → v43

## Overview

CHE·NU v43.0 introduces breaking changes for performance optimization and code clarity.

**Migration Time:** ~2-4 hours for typical installation  
**Risk Level:** Medium (breaking API changes)  
**Rollback:** Possible (keep v42 backup)

---

## Breaking Changes Summary

| Change | Impact | Migration Effort |
|--------|--------|------------------|
| Master Mind API | HIGH | 1-2 hours |
| Integrations package | MEDIUM | 30-60 min |
| Project Management | LOW | 15-30 min |
| Module renames | LOW | 15 min |

---

## 1. Master Mind Orchestrator

### Change

**OLD (v42):**
```python
from backend.services.orchestrator_v8 import CheNuOrchestratorV8

orchestrator = CheNuOrchestratorV8()
result = await orchestrator.process(query)
```

**NEW (v43):**
```python
from backend.services.master_mind import MasterMind

# Option 1: From environment (recommended)
master_mind = MasterMind.from_env()

# Option 2: Custom config
from backend.services.master_mind import MasterMindConfig
config = MasterMindConfig(
    enable_fast_intent=True,
    intent_confidence_threshold=0.3
)
master_mind = MasterMind(config=config)

result = await master_mind.process(query)
```

### Migration Steps

1. **Update imports:**
   ```bash
   # Find and replace in all files
   find . -name "*.py" -exec sed -i 's/from backend.services.orchestrator_v8 import/from backend.services.master_mind import/g' {} \;
   find . -name "*.py" -exec sed -i 's/CheNuOrchestratorV8/MasterMind/g' {} \;
   ```

2. **Update initialization:**
   ```python
   # Before
   orchestrator = CheNuOrchestratorV8()
   
   # After
   master_mind = MasterMind.from_env()
   ```

3. **Add environment variables:**
   ```bash
   # .env
   CHE·NU_ENABLE_FAST_INTENT=true
   CHE·NU_MAX_PARALLEL_TASKS=10
   ```

4. **Test:**
   ```python
   # Verify fast intent works
   result = await master_mind.process("Create construction project")
   metrics = master_mind.get_metrics()
   assert metrics['fast_intent_rate_percent'] > 50
   ```

---

## 2. Integrations Package

### Change

**OLD (v42):**
```python
from backend.services.integrations import GitHubIntegration
from backend.services.integration_service import IntegrationManager

github = GitHubIntegration(config)
await github.connect()
repos = await github.list_repos()
```

**NEW (v43):**
```python
from backend.integrations.manager import IntegrationManager
from backend.integrations.base import IntegrationConfig, IntegrationProvider

manager = IntegrationManager()

await manager.add_integration("my_github", IntegrationConfig(
    provider=IntegrationProvider.GITHUB,
    api_key="ghp_xxx"
))

github = manager.get_integration("my_github")
repos = await github.list_repos()
```

### Migration Steps

1. **Update imports:**
   ```python
   # Before
   from backend.services.integrations import GitHubIntegration
   from backend.services.integration_service import IntegrationManager
   
   # After
   from backend.integrations.providers.github import GitHubIntegration
   from backend.integrations.manager import IntegrationManager
   from backend.integrations.base import IntegrationConfig, IntegrationProvider
   ```

2. **Update initialization:**
   ```python
   # Before
   github = GitHubIntegration(config)
   await github.connect()
   
   # After
   manager = IntegrationManager()
   await manager.add_integration("github", IntegrationConfig(
       provider=IntegrationProvider.GITHUB,
       api_key=config.api_key
   ))
   github = manager.get_integration("github")
   ```

3. **Test:**
   ```bash
   pytest backend/tests/integration/test_integrations.py -v
   ```

---

## 3. Project Management

### Change

**OLD (v42):**
```python
from backend.services.project_service import ProjectService

service = ProjectService(db)
project = await service.create_project(data, user_id)
projects = await service.list_projects(user_id)
```

**NEW (v43):**
```python
from backend.services.project_management import ProjectManagementService

service = ProjectManagementService(db)

# Basic API unchanged
project = await service.create_project(user_id, name, description)
projects, total = await service.list_projects(user_id)

# NEW features available
gantt = await service.generate_gantt_chart(project.id, format="html")
template = await service.create_template(user_id, "Template", source_project_id=project.id)
critical_path = await service._get_critical_path(project)
```

### Migration Steps

1. **Update imports:**
   ```python
   # Before
   from backend.services.project_service import ProjectService
   
   # After
   from backend.services.project_management import ProjectManagementService
   ```

2. **Update create_project calls:**
   ```python
   # Before
   project = await service.create_project(
       ProjectCreate(name="Test", description="Desc"),
       user_id
   )
   
   # After
   project = await service.create_project(
       user_id=user_id,
       name="Test",
       description="Desc"
   )
   ```

3. **Optional: Use new features:**
   ```python
   # Generate Gantt
   gantt_html = await service.generate_gantt_chart(project.id, format="html")
   
   # Use templates
   template = await service.create_template(user_id, "Standard Construction")
   new_project = await service.create_project(user_id, "New Project", template_id=template.id)
   ```

---

## 4. Module Renames

### Changes

| Old Name | New Name | Reason |
|----------|----------|--------|
| `social_media.py` | `social_platforms_service.py` | Clarity (external platforms) |
| `communication.py` | `team_chat_service.py` | Clarity (team chat) |

### Migration Steps

1. **Update imports:**
   ```python
   # Before
   from backend.services.social_media import SocialMediaService
   from backend.services.communication import CommunicationService
   
   # After
   from backend.services.social_platforms_service import SocialPlatformsService
   from backend.services.team_chat_service import TeamChatService
   ```

2. **Understand distinctions:**
   - `social_platforms_service` = External (Twitter, LinkedIn, etc.)
   - `chenu-b19-social` = Internal CHE·NU social network
   - `team_chat_service` = Team chat (Slack-like)
   - `notification_service` = System notifications
   - `email_service` = Transactional emails

---

## 5. Test System

### Change

Tests moved from `backend/services/` to proper `backend/tests/` structure.

**OLD:**
```
backend/services/chenu-b11-tests-pytest.py
```

**NEW:**
```
backend/tests/
├── conftest.py
├── unit/
├── integration/
├── e2e/
└── mocks/
```

### Migration Steps

1. **Update test imports:**
   ```python
   # Before
   from backend.services.chenu-b11-tests-pytest import fixtures
   
   # After
   from backend.tests.conftest import fixtures
   ```

2. **Run tests from new location:**
   ```bash
   pytest backend/tests/ -v
   ```

---

## Complete Migration Checklist

### Pre-Migration

- [ ] Backup v42 installation
- [ ] Review all breaking changes
- [ ] Plan migration timeline
- [ ] Prepare rollback plan

### Migration

- [ ] Update master_mind imports and initialization
- [ ] Update integrations imports and usage
- [ ] Update project_service to project_management
- [ ] Update renamed module imports
- [ ] Update test imports
- [ ] Add new environment variables
- [ ] Update documentation references

### Testing

- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Run E2E tests
- [ ] Test fast intent detection (≥70% hit rate)
- [ ] Test Gantt chart generation
- [ ] Test integration providers
- [ ] Performance validation (<500ms avg response)

### Deployment

- [ ] Deploy to staging
- [ ] Smoke tests on staging
- [ ] Performance monitoring
- [ ] Deploy to production
- [ ] Monitor for issues
- [ ] Rollback if critical issues

---

## Automated Migration Script

```bash
#!/bin/bash
# migrate_v42_to_v43.sh

echo "🔄 Migrating CHE·NU v42 → v43..."

# 1. Backup
cp -r backend backend_v42_backup
echo "✅ Backup created"

# 2. Update imports - Master Mind
find backend -name "*.py" -exec sed -i 's/from backend.services.orchestrator_v8 import/from backend.services.master_mind import/g' {} \;
find backend -name "*.py" -exec sed -i 's/CheNuOrchestratorV8/MasterMind/g' {} \;
echo "✅ Master Mind imports updated"

# 3. Update imports - Integrations
find backend -name "*.py" -exec sed -i 's/from backend.services.integrations import/from backend.integrations.providers./g' {} \;
echo "✅ Integrations imports updated"

# 4. Update imports - Project Management
find backend -name "*.py" -exec sed -i 's/from backend.services.project_service import ProjectService/from backend.services.project_management import ProjectManagementService/g' {} \;
echo "✅ Project Management imports updated"

# 5. Update imports - Renamed modules
find backend -name "*.py" -exec sed -i 's/from backend.services.social_media/from backend.services.social_platforms_service/g' {} \;
find backend -name "*.py" -exec sed -i 's/from backend.services.communication/from backend.services.team_chat_service/g' {} \;
echo "✅ Renamed modules updated"

# 6. Run tests
pytest backend/tests/ -v
if [ $? -eq 0 ]; then
    echo "✅ All tests passed"
else
    echo "❌ Tests failed - review changes"
    exit 1
fi

echo "✅ Migration complete!"
echo "📝 Next: Review changes, update .env, deploy to staging"
```

---

## Rollback Plan

If migration fails:

```bash
# 1. Stop services
systemctl stop chenu-backend chenu-frontend

# 2. Restore backup
rm -rf backend
mv backend_v42_backup backend

# 3. Restart services
systemctl start chenu-backend chenu-frontend

# 4. Verify
curl http://localhost:8000/health
```

---

## Support

Questions? Check:
- `docs/MODULE_REGISTRY_V2_0_FINAL.md`
- `docs/RAPPORT_FINAL_MERGE_V43.md`
- GitHub Issues

---

**Migration Time:** Allow 2-4 hours  
**Recommended:** Migrate on staging first  
**Success Rate:** >95% with proper testing
