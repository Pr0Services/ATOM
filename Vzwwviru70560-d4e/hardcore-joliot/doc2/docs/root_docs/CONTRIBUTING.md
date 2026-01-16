# 🤝 Contributing to CHE·NU™

Thank you for your interest in contributing to CHE·NU! This document provides guidelines and instructions for contributing.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Memory Prompt Compliance](#memory-prompt-compliance)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Commit Messages](#commit-messages)

---

## 📜 Code of Conduct

By participating in this project, you agree to:

1. **Be respectful** — Treat everyone with respect and dignity
2. **Be constructive** — Provide helpful feedback and suggestions
3. **Be collaborative** — Work together towards shared goals
4. **Follow governance** — Respect the 10 Laws of Governance

---

## ⚠️ Memory Prompt Compliance

**CRITICAL**: All contributions MUST comply with the Memory Prompt.

### Non-Negotiable Rules

1. **EXACTLY 8 Spheres** — No additions, no removals, no merging
   - Personal 🏠
   - Business 💼
   - Government & Institutions 🏛️
   - Creative Studio 🎨
   - Community 👥
   - Social & Media 📱
   - Entertainment 🎬
   - My Team 🤝

2. **EXACTLY 10 Bureau Sections** — Same structure for every sphere
   - Dashboard, Notes, Tasks, Projects, Threads, Meetings, Data, Agents, Reports, Budget

3. **Token Disclaimer** — Tokens are NOT cryptocurrency

4. **Nova is System Intelligence** — Nova is NEVER a hired agent

5. **Governance Before Execution** — All actions must pass governance checks

### Compliance Checklist

Before submitting a PR, verify:

- [ ] No new spheres added
- [ ] No spheres removed or renamed
- [ ] No bureau sections added/removed
- [ ] Token disclaimer present where tokens are shown
- [ ] Nova is labeled as "System Intelligence"
- [ ] Governance checks implemented for all actions
- [ ] All 10 Laws respected

---

## 🚀 Getting Started

### Prerequisites

- Node.js 20+
- npm or pnpm
- Docker (optional but recommended)
- Git

### Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/chenu-app.git
cd chenu-app

# Install dependencies
cd frontend && npm install
cd ../backend && npm install

# Copy environment
cp .env.example .env

# Start development servers
npm run dev
```

### Running Tests

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Type checking
npm run type-check

# Linting
npm run lint
```

---

## 🔄 Development Workflow

### Branch Naming

```
feature/   — New features
fix/       — Bug fixes
docs/      — Documentation
refactor/  — Code refactoring
test/      — Test additions/changes
chore/     — Maintenance tasks
```

Examples:
- `feature/nova-insights-panel`
- `fix/token-budget-calculation`
- `docs/api-endpoints`

### Workflow

1. **Create branch** from `develop`
2. **Make changes** following code standards
3. **Write tests** for new functionality
4. **Verify compliance** with Memory Prompt
5. **Submit PR** to `develop`
6. **Address feedback** from reviewers
7. **Merge** after approval

---

## 📝 Code Standards

### TypeScript

```typescript
// ✅ Good: Explicit types, clear naming
interface ThreadCreateInput {
  title: string;
  description?: string;
  sphereCode: SphereCode;  // Type alias, not string
  tokenBudget: number;
  encodingEnabled: boolean;
}

async function createThread(input: ThreadCreateInput): Promise<Thread> {
  // Governance check FIRST (Memory Prompt)
  await governanceService.verifyBudget(input.sphereCode, input.tokenBudget);
  
  // Then proceed
  return threadRepository.create(input);
}

// ❌ Bad: Any types, unclear naming
async function create(data: any): Promise<any> {
  return db.insert(data);
}
```

### React Components

```tsx
// ✅ Good: Props interface, Memory Prompt compliance
interface SphereSelectorProps {
  activeCode: SphereCode;
  onSelect: (code: SphereCode) => void;
}

// 8 Spheres ONLY (FROZEN)
const SPHERES: readonly Sphere[] = [
  { code: 'personal', name: 'Personal', icon: '🏠' },
  // ... exactly 8
] as const;

export function SphereSelector({ activeCode, onSelect }: SphereSelectorProps) {
  return (
    <nav aria-label="Sphere navigation">
      {SPHERES.map((sphere) => (
        <button
          key={sphere.code}
          onClick={() => onSelect(sphere.code)}
          aria-current={activeCode === sphere.code ? 'page' : undefined}
        >
          {sphere.icon} {sphere.name}
        </button>
      ))}
    </nav>
  );
}
```

### File Organization

```
src/
├── components/
│   ├── [ComponentName]/
│   │   ├── index.ts           # Exports
│   │   ├── ComponentName.tsx  # Main component
│   │   ├── ComponentName.test.tsx
│   │   └── ComponentName.stories.tsx
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `SphereSelector` |
| Hooks | camelCase with `use` | `useTokenBudget` |
| Utils | camelCase | `formatTokens` |
| Constants | SCREAMING_SNAKE | `MAX_SPHERES` |
| Types | PascalCase | `ThreadStatus` |
| Files | kebab-case or PascalCase | `sphere-selector.tsx` |

---

## 🧪 Testing Requirements

### Minimum Coverage

- **Unit Tests**: 80% coverage
- **E2E Tests**: All critical paths
- **Memory Prompt Tests**: Required for any sphere/bureau changes

### Test Structure

```typescript
describe('SphereSelector', () => {
  // Memory Prompt compliance
  it('should render exactly 8 spheres', () => {
    render(<SphereSelector activeCode="personal" onSelect={() => {}} />);
    expect(screen.getAllByRole('button')).toHaveLength(8);
  });

  // Functionality
  it('should call onSelect when sphere clicked', () => {
    const onSelect = vi.fn();
    render(<SphereSelector activeCode="personal" onSelect={onSelect} />);
    fireEvent.click(screen.getByText('Business'));
    expect(onSelect).toHaveBeenCalledWith('business');
  });

  // Accessibility
  it('should have proper aria attributes', () => {
    render(<SphereSelector activeCode="personal" onSelect={() => {}} />);
    expect(screen.getByLabelText(/sphere navigation/i)).toBeInTheDocument();
  });
});
```

### E2E Test Requirements

All E2E tests must verify Memory Prompt compliance:

```typescript
test('should display exactly 8 spheres', async ({ page }) => {
  await page.goto('/dashboard');
  const spheres = page.locator('[data-testid^="sphere-"]');
  await expect(spheres).toHaveCount(8);
});

test('should display exactly 10 bureau sections', async ({ page }) => {
  await page.goto('/personal');
  const sections = page.locator('[data-testid^="bureau-section-"]');
  await expect(sections).toHaveCount(10);
});
```

---

## 🔀 Pull Request Process

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Memory Prompt Compliance
- [ ] No sphere changes (still exactly 8)
- [ ] No bureau section changes (still exactly 10)
- [ ] Token disclaimer present
- [ ] Nova labeled correctly
- [ ] Governance checks in place

## Testing
- [ ] Unit tests added/updated
- [ ] E2E tests added/updated
- [ ] All tests passing

## Screenshots
If applicable

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed
- [ ] Comments added where needed
- [ ] Documentation updated
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least 1 maintainer
3. **Memory Prompt audit** for structural changes
4. **Approval** required before merge

---

## 💬 Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting |
| `refactor` | Code restructuring |
| `test` | Tests |
| `chore` | Maintenance |

### Examples

```bash
feat(threads): add encoding toggle for token savings

Implements encoding functionality that reduces token usage
by up to 30%. Toggle is visible in thread header.

Closes #123

---

fix(governance): enforce budget check before agent execution

Agent execution was bypassing budget verification in some cases.
This fix ensures Law 8 (Budget Accountability) is always enforced.

Memory Prompt Compliance: Law 7 (Agent Non-Autonomy)
```

---

## 🎯 Priority Areas

We especially welcome contributions in:

1. **i18n Translations** — Complete translations for DE, IT, PT, ZH, JA, KO, AR
2. **Accessibility** — WCAG 2.1 AA compliance
3. **Performance** — Optimization and profiling
4. **Documentation** — API docs, guides, tutorials
5. **Testing** — Increase coverage, edge cases

---

## ❓ Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

---

<div align="center">

**Thank you for contributing to CHE·NU! 💪🔥🚀**

*"LAISSE TA MARQUE"*

</div>
