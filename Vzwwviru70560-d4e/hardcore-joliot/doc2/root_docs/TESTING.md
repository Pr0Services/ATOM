# CHE·NU™ Testing Guide

## 📊 Test Coverage Overview

| Category | Files | Tests | Coverage Target |
|----------|-------|-------|-----------------|
| **Backend API Routes** | 11 | 150+ | 80%+ |
| **Backend Agents** | 9 | 90+ | 75%+ |
| **Backend Infrastructure** | 5 | 40+ | 85%+ |
| **Frontend Components** | 10 | 80+ | 70%+ |
| **Frontend Stores** | 3 | 30+ | 80%+ |
| **Frontend Hooks** | 3 | 20+ | 75%+ |
| **E2E Tests** | 11 | 50+ | Critical flows |
| **TOTAL** | **52** | **460+** | **75%+** |

---

## 🚀 Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term

# Run specific test file
pytest tests/api/test_crm_routes.py -v

# Run specific test class
pytest tests/api/test_crm_routes.py::TestCRMContacts -v

# Run with markers
pytest tests/ -m "slow" -v
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- HubArchitecture.test.tsx

# Run in watch mode
npm test -- --watch

# Update snapshots
npm test -- -u
```

### E2E Tests

```bash
cd frontend

# Run all E2E tests
npx playwright test

# Run specific browser
npx playwright test --project=chromium

# Run specific test file
npx playwright test e2e/auth-flow.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed

# Run with UI
npx playwright test --ui

# Debug mode
npx playwright test --debug
```

---

## 📁 Test File Organization

```
backend/
├── tests/
│   ├── api/                    # API route tests
│   │   ├── test_crm_routes.py
│   │   ├── test_scholar_routes.py
│   │   ├── test_invoice_routes.py
│   │   └── ... (8 more)
│   │
│   ├── agents/                 # Agent tests
│   │   ├── test_business_agents.py
│   │   ├── test_scholar_agents.py
│   │   └── ... (7 more)
│   │
│   ├── test_auth.py           # Auth tests
│   ├── test_migrations.py     # Migration tests
│   ├── test_permissions.py    # RBAC tests
│   ├── test_rate_limiting.py  # Rate limit tests
│   └── test_caching.py        # Cache tests

frontend/
├── src/
│   └── __tests__/
│       ├── components/         # Component tests
│       │   └── HubArchitecture.test.tsx
│       │
│       ├── stores/             # Store tests
│       │   ├── sphereStore.test.ts
│       │   ├── threadStore.test.ts
│       │   └── agentStore.test.ts
│       │
│       ├── hooks/              # Hook tests
│       │   ├── useSphere.test.ts
│       │   ├── useThread.test.ts
│       │   └── useAgent.test.ts
│       │
│       └── integration/        # Integration tests
│           ├── SphereNavigation.test.tsx
│           └── ThreadWorkflow.test.tsx
│
└── e2e/                        # E2E tests
    ├── hub-navigation.spec.ts
    ├── auth-flow.spec.ts
    ├── thread-workflow.spec.ts
    ├── agent-execution.spec.ts
    ├── performance.spec.ts
    ├── accessibility.spec.ts
    └── responsive.spec.ts
```

---

## 🧪 Test Examples

### Backend API Test

```python
class TestCRMContacts:
    def test_create_contact(self, client, auth_headers):
        """Test creating a new contact"""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }
        resp = client.post(
            "/api/v1/crm/contacts",
            json=data,
            headers=auth_headers
        )
        assert resp.status_code == 201
        assert resp.json()["email"] == "john@example.com"
```

### Frontend Component Test

```typescript
describe('HubProvider', () => {
  it('workspace is always visible', () => {
    const TestComponent = () => {
      const { visibleHubs } = useHubs();
      return <div data-testid="hubs">{visibleHubs.join(',')}</div>;
    };
    
    render(
      <HubProvider>
        <TestComponent />
      </HubProvider>
    );
    
    expect(screen.getByTestId('hubs')).toHaveTextContent('workspace');
  });
});
```

### E2E Test

```typescript
test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@chenu.com');
  await page.fill('[name="password"]', 'test123');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
});
```

---

## 🎯 Coverage Goals

### Backend
- **API Routes**: 80%+ coverage
- **Agents**: 75%+ coverage
- **Core Logic**: 85%+ coverage

### Frontend
- **Components**: 70%+ coverage
- **Stores**: 80%+ coverage
- **Hooks**: 75%+ coverage

### E2E
- All critical user flows
- 3 browsers (Chrome, Firefox, Safari)
- Mobile + Desktop viewports

---

## 🔧 CI/CD Integration

Tests run automatically on:
- Every push to `develop` or `main`
- Every pull request
- Every release

### CI Pipeline

```yaml
# .github/workflows/ci.yml
jobs:
  test-backend:
    - Install dependencies
    - Run migrations
    - pytest --cov --cov-fail-under=75
  
  test-frontend:
    - Install dependencies
    - npm test -- --coverage
    - Check coverage > 70%
  
  test-e2e:
    - Run on 3 browsers
    - Upload artifacts (screenshots, videos)
```

---

## 📈 Viewing Coverage Reports

### Backend

```bash
# Generate HTML report
pytest --cov=. --cov-report=html

# Open report
open htmlcov/index.html
```

### Frontend

```bash
# Run with coverage
npm test -- --coverage

# Open report
open coverage/lcov-report/index.html
```

### CodeCov

Coverage reports automatically uploaded to CodeCov:
https://codecov.io/gh/chenu/chenu

---

## 🐛 Debugging Tests

### Backend

```bash
# Run with verbose output
pytest tests/ -vv

# Run with print statements
pytest tests/ -s

# Run with PDB debugger
pytest tests/ --pdb

# Run last failed tests only
pytest --lf
```

### Frontend

```bash
# Debug in VS Code
# Add breakpoint, press F5

# Run single test
npm test -- -t "test name"

# Show full error output
npm test -- --verbose
```

### E2E

```bash
# Debug mode (step through)
npx playwright test --debug

# Show browser
npx playwright test --headed

# Slow motion
npx playwright test --headed --slow-mo=1000

# Trace viewer (after failure)
npx playwright show-trace trace.zip
```

---

## ✅ Writing Good Tests

### Best Practices

1. **Descriptive Names**: `test_user_can_create_contact_with_valid_data()`
2. **Arrange-Act-Assert**: Clear test structure
3. **One Assertion Focus**: Test one thing at a time
4. **Use Fixtures**: Reusable test data
5. **Mock External Services**: Don't call real APIs
6. **Clean Up**: Reset state after tests

### Example

```python
def test_thread_budget_tracking(
    client, 
    auth_headers, 
    sample_thread
):
    """Test that thread budget is tracked correctly"""
    # Arrange
    thread_id = sample_thread["id"]
    initial_budget = sample_thread["budget"]
    
    # Act
    resp = client.post(
        f"/api/v1/threads/{thread_id}/execute-agent",
        json={"agent_id": "test", "cost": 50},
        headers=auth_headers
    )
    
    # Assert
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["budget_used"] == 50
    assert updated["budget_remaining"] == initial_budget - 50
```

---

## 🚨 Common Issues

### Issue: Tests fail locally but pass in CI

**Solution**: Check environment variables, database state, timing issues

### Issue: E2E tests flaky

**Solution**: Add explicit waits, increase timeouts, check for race conditions

### Issue: Coverage not reaching target

**Solution**: Identify uncovered code paths, add edge case tests

---

## 📚 Resources

- **Pytest Docs**: https://docs.pytest.org
- **React Testing Library**: https://testing-library.com/react
- **Playwright Docs**: https://playwright.dev
- **CHE·NU Testing Standards**: See `docs/testing-standards.md`

---

*Testing is not just about code coverage — it's about confidence in your code.*
