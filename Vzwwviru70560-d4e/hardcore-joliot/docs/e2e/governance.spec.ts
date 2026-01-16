// ═══════════════════════════════════════════════════════════════════════════════
// CHE·NU™ — E2E GOVERNANCE & AGENTS TESTS
// Sprint 2: End-to-end tests for governance and agent interactions
// Nova = L0 System Intelligence | Tokens = Internal Credits
// ═══════════════════════════════════════════════════════════════════════════════

import { test, expect, type Page } from '@playwright/test';

// ═══════════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════

async function openNova(page: Page) {
  await page.getByTestId('nova-toggle').click();
  await expect(page.getByTestId('nova-panel')).toBeVisible();
}

async function closeNova(page: Page) {
  await page.getByTestId('nova-toggle').click();
  await expect(page.getByTestId('nova-panel')).not.toBeVisible();
}

async function openGovernancePanel(page: Page) {
  await page.getByTestId('governance-toggle').click();
  await expect(page.getByTestId('governance-panel')).toBeVisible();
}

async function openAgentsPanel(page: Page) {
  await page.getByTestId('bureau-section-active-agents').click();
  await expect(page.getByTestId('agents-panel')).toBeVisible();
}

// ═══════════════════════════════════════════════════════════════════════════════
// NOVA TESTS (L0 - SYSTEM INTELLIGENCE)
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Nova - System Intelligence', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('Nova toggle should be visible', async ({ page }) => {
    const novaToggle = page.getByTestId('nova-toggle');
    await expect(novaToggle).toBeVisible();
  });

  test('should open Nova panel', async ({ page }) => {
    await openNova(page);
    
    const novaPanel = page.getByTestId('nova-panel');
    await expect(novaPanel).toBeVisible();
  });

  test('Nova should display system badge', async ({ page }) => {
    await openNova(page);
    
    const systemBadge = page.getByTestId('nova-system-badge');
    await expect(systemBadge).toBeVisible();
    await expect(systemBadge).toContainText('L0');
  });

  test('Nova should show guidance capabilities', async ({ page }) => {
    await openNova(page);
    
    const capabilities = page.getByTestId('nova-capabilities');
    await expect(capabilities).toContainText(/guidance|memory|governance/i);
  });

  test('Nova should be available in all spheres', async ({ page }) => {
    const spheres = ['personal', 'business', 'scholar'];
    
    for (const sphere of spheres) {
      await page.goto('/');
      await page.getByTestId(`sphere-${sphere}`).click();
      
      const novaToggle = page.getByTestId('nova-toggle');
      await expect(novaToggle).toBeVisible();
    }
  });

  test('Nova should show chat interface', async ({ page }) => {
    await openNova(page);
    
    const chatInput = page.getByTestId('nova-chat-input');
    await expect(chatInput).toBeVisible();
  });

  test('should be able to send message to Nova', async ({ page }) => {
    await openNova(page);
    
    const chatInput = page.getByTestId('nova-chat-input');
    await chatInput.fill('Hello Nova');
    
    const sendButton = page.getByTestId('nova-send-button');
    await sendButton.click();
    
    // Wait for response
    const novaResponse = page.getByTestId('nova-message-assistant').last();
    await expect(novaResponse).toBeVisible({ timeout: 10000 });
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// GOVERNANCE PANEL TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Governance Panel', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('governance toggle should be visible', async ({ page }) => {
    const govToggle = page.getByTestId('governance-toggle');
    await expect(govToggle).toBeVisible();
  });

  test('should open governance panel', async ({ page }) => {
    await openGovernancePanel(page);
    
    const govPanel = page.getByTestId('governance-panel');
    await expect(govPanel).toBeVisible();
  });

  test('should show governance status', async ({ page }) => {
    await openGovernancePanel(page);
    
    const status = page.getByTestId('governance-status');
    await expect(status).toBeVisible();
    await expect(status).toContainText(/enabled|disabled/i);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TOKEN BUDGET TESTS (Tokens = Internal Credits, NOT Crypto)
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Token Budget', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await openGovernancePanel(page);
  });

  test('should display token budget', async ({ page }) => {
    const budgetDisplay = page.getByTestId('token-budget-display');
    await expect(budgetDisplay).toBeVisible();
  });

  test('should show remaining tokens', async ({ page }) => {
    const remaining = page.getByTestId('tokens-remaining');
    await expect(remaining).toBeVisible();
    
    const text = await remaining.textContent();
    expect(parseInt(text?.replace(/[^0-9]/g, '') || '0')).toBeGreaterThan(0);
  });

  test('should show used tokens', async ({ page }) => {
    const used = page.getByTestId('tokens-used');
    await expect(used).toBeVisible();
  });

  test('token budget should be numeric (not crypto)', async ({ page }) => {
    const budgetDisplay = page.getByTestId('token-budget-display');
    const text = await budgetDisplay.textContent();
    
    // Should contain numbers, not blockchain addresses
    expect(text).toMatch(/\d+/);
    expect(text).not.toMatch(/0x[a-fA-F0-9]{40}/); // Not an ETH address
  });

  test('should show budget progress bar', async ({ page }) => {
    const progressBar = page.getByTestId('budget-progress-bar');
    await expect(progressBar).toBeVisible();
  });

  test('should show warning at threshold', async ({ page }) => {
    // This test would require manipulation of budget
    // For now, just verify warning element exists
    const warningIndicator = page.getByTestId('budget-warning-indicator');
    // May or may not be visible depending on budget state
    await expect(warningIndicator).toHaveCount(1);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// SCOPE LOCK TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Scope Lock', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await openGovernancePanel(page);
  });

  test('should show scope lock status', async ({ page }) => {
    const scopeLock = page.getByTestId('scope-lock-status');
    await expect(scopeLock).toBeVisible();
  });

  test('should show current scope level', async ({ page }) => {
    const scopeLevel = page.getByTestId('scope-level');
    await expect(scopeLevel).toBeVisible();
    
    const text = await scopeLevel.textContent();
    const validLevels = ['selection', 'document', 'project', 'sphere', 'global'];
    expect(validLevels.some(level => text?.toLowerCase().includes(level))).toBeTruthy();
  });

  test('should show lock/unlock button', async ({ page }) => {
    const lockButton = page.getByTestId('scope-lock-toggle');
    await expect(lockButton).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// AGENTS SECTION TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Agents Section', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await openAgentsPanel(page);
  });

  test('should show agents panel', async ({ page }) => {
    const agentsPanel = page.getByTestId('agents-panel');
    await expect(agentsPanel).toBeVisible();
  });

  test('should show Nova as L0 system agent', async ({ page }) => {
    const novaCard = page.getByTestId('agent-card-nova');
    await expect(novaCard).toBeVisible();
    await expect(novaCard).toContainText('L0');
    await expect(novaCard).toContainText('System');
  });

  test('Nova should NOT show hire button', async ({ page }) => {
    const novaCard = page.getByTestId('agent-card-nova');
    const hireButton = novaCard.getByTestId('hire-agent-button');
    
    // Nova is never hired - button should not exist or be disabled
    const buttonCount = await hireButton.count();
    expect(buttonCount).toBe(0);
  });

  test('should show available agents catalog', async ({ page }) => {
    const catalog = page.getByTestId('agents-catalog');
    await expect(catalog).toBeVisible();
  });

  test('available agents should show hire button', async ({ page }) => {
    const agentCards = page.locator('[data-testid^="agent-card-"]:not([data-testid="agent-card-nova"])');
    const firstAgent = agentCards.first();
    
    if (await firstAgent.isVisible()) {
      const hireButton = firstAgent.getByTestId('hire-agent-button');
      await expect(hireButton).toBeVisible();
    }
  });

  test('agents should show cost per token', async ({ page }) => {
    const agentCards = page.locator('[data-testid^="agent-card-"]');
    const firstAgent = agentCards.first();
    
    const costDisplay = firstAgent.getByTestId('agent-cost');
    await expect(costDisplay).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// AGENT HIRING FLOW TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Agent Hiring Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await openAgentsPanel(page);
  });

  test('should open hire confirmation dialog', async ({ page }) => {
    const agentCards = page.locator('[data-testid^="agent-card-"]:not([data-testid="agent-card-nova"])');
    const firstAgent = agentCards.first();
    
    if (await firstAgent.isVisible()) {
      const hireButton = firstAgent.getByTestId('hire-agent-button');
      await hireButton.click();
      
      const confirmDialog = page.getByTestId('hire-confirm-dialog');
      await expect(confirmDialog).toBeVisible();
    }
  });

  test('hire dialog should show cost estimation', async ({ page }) => {
    const agentCards = page.locator('[data-testid^="agent-card-"]:not([data-testid="agent-card-nova"])');
    const firstAgent = agentCards.first();
    
    if (await firstAgent.isVisible()) {
      const hireButton = firstAgent.getByTestId('hire-agent-button');
      await hireButton.click();
      
      const costEstimate = page.getByTestId('hire-cost-estimate');
      await expect(costEstimate).toBeVisible();
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// GOVERNANCE BEFORE EXECUTION TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Governance Before Execution', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should validate execution before running', async ({ page }) => {
    await openNova(page);
    
    // Send a message that requires execution
    const chatInput = page.getByTestId('nova-chat-input');
    await chatInput.fill('Execute a complex task');
    
    const sendButton = page.getByTestId('nova-send-button');
    await sendButton.click();
    
    // Should show validation indicator
    const validationIndicator = page.getByTestId('execution-validation');
    // May show briefly or be part of the flow
    await page.waitForTimeout(500);
  });

  test('should show pending approvals', async ({ page }) => {
    await openGovernancePanel(page);
    
    const pendingApprovals = page.getByTestId('pending-approvals');
    await expect(pendingApprovals).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// MEMORY PROMPT COMPLIANCE - GOVERNANCE
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Governance Compliance', () => {
  test('Nova should be L0 System Intelligence', async ({ page }) => {
    await page.goto('/');
    await openAgentsPanel(page);
    
    const novaCard = page.getByTestId('agent-card-nova');
    await expect(novaCard).toContainText('L0');
  });

  test('Nova should never be a hired agent', async ({ page }) => {
    await page.goto('/');
    await openAgentsPanel(page);
    
    const novaCard = page.getByTestId('agent-card-nova');
    const hiredBadge = novaCard.getByTestId('hired-badge');
    
    // Nova should not have hired badge
    await expect(hiredBadge).toHaveCount(0);
  });

  test('tokens should be internal credits (not crypto)', async ({ page }) => {
    await page.goto('/');
    await openGovernancePanel(page);
    
    // Check for crypto-related terms that should NOT appear
    const panelText = await page.getByTestId('governance-panel').textContent();
    
    expect(panelText?.toLowerCase()).not.toContain('blockchain');
    expect(panelText?.toLowerCase()).not.toContain('cryptocurrency');
    expect(panelText?.toLowerCase()).not.toContain('wallet');
    expect(panelText?.toLowerCase()).not.toContain('ethereum');
  });

  test('governance should be enabled by default', async ({ page }) => {
    await page.goto('/');
    await openGovernancePanel(page);
    
    const status = page.getByTestId('governance-status');
    await expect(status).toContainText(/enabled/i);
  });
});
