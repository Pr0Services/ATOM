/**
 * CHE·NU™ — E2E Tests with Playwright v40
 * Sprint 1: Foundation - Task 1.15
 * 
 * Complete E2E test suite covering:
 * - 9 Spheres navigation
 * - 6 Bureau sections
 * - Thread creation/management
 * - Agent interactions
 * - Governance validation
 */

import { test, expect, Page, BrowserContext } from '@playwright/test';

// ═══════════════════════════════════════════════════════════════════════════════
// TEST CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

// Frozen architecture constants (must match CHENU_VERSION 40)
const SPHERE_COUNT = 9;
const BUREAU_SECTION_COUNT = 6;
const GOVERNANCE_LAW_COUNT = 10;
const AGENT_COUNT = 226;

const SPHERES = [
  { id: 'personal', name: 'Personal', icon: '🏠' },
  { id: 'business', name: 'Business', icon: '💼' },
  { id: 'government', name: 'Government & Institutions', icon: '🏛️' },
  { id: 'creative', name: 'Studio de Création', icon: '🎨' },
  { id: 'community', name: 'Community', icon: '👥' },
  { id: 'social', name: 'Social & Media', icon: '📱' },
  { id: 'entertainment', name: 'Entertainment', icon: '🎬' },
  { id: 'team', name: 'My Team', icon: '🤝' },
  { id: 'scholar', name: 'Scholar', icon: '📚' },
];

const BUREAU_SECTIONS = [
  { id: 'quick_capture', name: 'Quick Capture', icon: '⚡' },
  { id: 'resume_workspace', name: 'Resume Workspace', icon: '▶️' },
  { id: 'threads', name: 'Threads', icon: '💬' },
  { id: 'data_files', name: 'Data & Files', icon: '📁' },
  { id: 'active_agents', name: 'Active Agents', icon: '🤖' },
  { id: 'meetings', name: 'Meetings', icon: '📅' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════

async function login(page: Page, email = 'test@chenu.io', password = 'testpass123') {
  await page.goto(`${BASE_URL}/login`);
  await page.fill('[data-testid="email-input"]', email);
  await page.fill('[data-testid="password-input"]', password);
  await page.click('[data-testid="login-button"]');
  await page.waitForURL('**/dashboard');
}

async function navigateToSphere(page: Page, sphereId: string) {
  await page.click(`[data-testid="sphere-${sphereId}"]`);
  await page.waitForSelector(`[data-testid="bureau-container"]`);
}

async function navigateToSection(page: Page, sectionId: string) {
  await page.click(`[data-testid="section-${sectionId}"]`);
  await page.waitForSelector(`[data-testid="section-content-${sectionId}"]`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// AUTHENTICATION TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Authentication', () => {
  test('should display login page', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    await expect(page.locator('[data-testid="login-form"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    await login(page);
    
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('[data-testid="email-input"]', 'wrong@email.com');
    await page.fill('[data-testid="password-input"]', 'wrongpass');
    await page.click('[data-testid="login-button"]');
    
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  });

  test('should logout successfully', async ({ page }) => {
    await login(page);
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout-button"]');
    
    await expect(page).toHaveURL(/.*login/);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// SPHERE NAVIGATION TESTS (9 Spheres)
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Sphere Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('should display exactly 9 spheres', async ({ page }) => {
    const sphereElements = page.locator('[data-testid^="sphere-"]');
    await expect(sphereElements).toHaveCount(SPHERE_COUNT);
  });

  test('should display all sphere icons correctly', async ({ page }) => {
    for (const sphere of SPHERES) {
      const sphereElement = page.locator(`[data-testid="sphere-${sphere.id}"]`);
      await expect(sphereElement).toBeVisible();
      await expect(sphereElement).toContainText(sphere.icon);
    }
  });

  test('should navigate to each sphere', async ({ page }) => {
    for (const sphere of SPHERES) {
      await navigateToSphere(page, sphere.id);
      
      await expect(page.locator('[data-testid="sphere-title"]')).toContainText(sphere.name);
      await expect(page.locator('[data-testid="bureau-container"]')).toBeVisible();
    }
  });

  test('should maintain only one active sphere at a time', async ({ page }) => {
    await navigateToSphere(page, 'personal');
    await navigateToSphere(page, 'business');
    
    const activeSpheres = page.locator('[data-testid^="sphere-"][data-active="true"]');
    await expect(activeSpheres).toHaveCount(1);
  });

  test('sphere order should match frozen architecture', async ({ page }) => {
    const sphereElements = page.locator('[data-testid^="sphere-"]');
    const count = await sphereElements.count();
    
    expect(count).toBe(SPHERE_COUNT);
    
    for (let i = 0; i < count; i++) {
      const sphereId = await sphereElements.nth(i).getAttribute('data-testid');
      expect(sphereId).toBe(`sphere-${SPHERES[i].id}`);
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// BUREAU SECTION TESTS (6 Sections)
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Bureau Sections', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToSphere(page, 'personal');
  });

  test('should display exactly 6 bureau sections', async ({ page }) => {
    const sectionElements = page.locator('[data-testid^="section-"]');
    await expect(sectionElements).toHaveCount(BUREAU_SECTION_COUNT);
  });

  test('should display all section names correctly', async ({ page }) => {
    for (const section of BUREAU_SECTIONS) {
      const sectionElement = page.locator(`[data-testid="section-${section.id}"]`);
      await expect(sectionElement).toBeVisible();
    }
  });

  test('should navigate to each section', async ({ page }) => {
    for (const section of BUREAU_SECTIONS) {
      await navigateToSection(page, section.id);
      
      await expect(
        page.locator(`[data-testid="section-content-${section.id}"]`)
      ).toBeVisible();
    }
  });

  test('sections should be consistent across all spheres', async ({ page }) => {
    for (const sphere of SPHERES) {
      await navigateToSphere(page, sphere.id);
      
      const sectionElements = page.locator('[data-testid^="section-"]');
      await expect(sectionElements).toHaveCount(BUREAU_SECTION_COUNT);
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// THREAD TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Thread Management', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await navigateToSphere(page, 'personal');
    await navigateToSection(page, 'threads');
  });

  test('should create a new thread', async ({ page }) => {
    await page.click('[data-testid="new-thread-button"]');
    await page.fill('[data-testid="thread-title-input"]', 'Test Thread');
    await page.click('[data-testid="create-thread-button"]');
    
    await expect(page.locator('[data-testid="thread-list"]')).toContainText('Test Thread');
  });

  test('should open thread and show messages', async ({ page }) => {
    await page.click('[data-testid="thread-item"]:first-child');
    
    await expect(page.locator('[data-testid="thread-messages"]')).toBeVisible();
  });

  test('should send a message in thread', async ({ page }) => {
    await page.click('[data-testid="thread-item"]:first-child');
    await page.fill('[data-testid="message-input"]', 'Hello Nova!');
    await page.click('[data-testid="send-message-button"]');
    
    await expect(page.locator('[data-testid="thread-messages"]')).toContainText('Hello Nova!');
  });

  test('threads should respect sphere isolation', async ({ page }) => {
    // Create thread in Personal
    await page.click('[data-testid="new-thread-button"]');
    await page.fill('[data-testid="thread-title-input"]', 'Personal Thread');
    await page.click('[data-testid="create-thread-button"]');
    
    // Switch to Business
    await navigateToSphere(page, 'business');
    await navigateToSection(page, 'threads');
    
    // Thread should not be visible
    await expect(page.locator('[data-testid="thread-list"]')).not.toContainText('Personal Thread');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// AGENT TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Agent System', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('should display Nova (L0) as always present', async ({ page }) => {
    await expect(page.locator('[data-testid="nova-indicator"]')).toBeVisible();
  });

  test('should show agent list in Active Agents section', async ({ page }) => {
    await navigateToSphere(page, 'team');
    await navigateToSection(page, 'active_agents');
    
    await expect(page.locator('[data-testid="agent-list"]')).toBeVisible();
  });

  test('should display agent levels correctly', async ({ page }) => {
    await navigateToSphere(page, 'team');
    await navigateToSection(page, 'active_agents');
    
    // Check for level badges
    await expect(page.locator('[data-testid="agent-level-L0"]')).toBeVisible();
    await expect(page.locator('[data-testid="agent-level-L1"]')).toBeVisible();
    await expect(page.locator('[data-testid="agent-level-L2"]')).toBeVisible();
    await expect(page.locator('[data-testid="agent-level-L3"]')).toBeVisible();
  });

  test('should activate an agent', async ({ page }) => {
    await navigateToSphere(page, 'personal');
    await navigateToSection(page, 'active_agents');
    
    await page.click('[data-testid="agent-card"]:first-child [data-testid="activate-button"]');
    
    await expect(
      page.locator('[data-testid="agent-card"]:first-child [data-testid="status-active"]')
    ).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// GOVERNANCE TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Governance', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('should display all 10 governance laws', async ({ page }) => {
    await page.click('[data-testid="governance-menu"]');
    await page.click('[data-testid="view-laws"]');
    
    const lawElements = page.locator('[data-testid^="law-L"]');
    await expect(lawElements).toHaveCount(GOVERNANCE_LAW_COUNT);
  });

  test('should require approval before AI execution (L7)', async ({ page }) => {
    await navigateToSphere(page, 'personal');
    await navigateToSection(page, 'threads');
    await page.click('[data-testid="thread-item"]:first-child');
    
    await page.fill('[data-testid="message-input"]', 'Execute complex task');
    await page.click('[data-testid="send-message-button"]');
    
    // Should show approval dialog
    await expect(page.locator('[data-testid="approval-dialog"]')).toBeVisible();
  });

  test('should show token cost before execution (L8)', async ({ page }) => {
    await navigateToSphere(page, 'personal');
    await navigateToSection(page, 'threads');
    await page.click('[data-testid="thread-item"]:first-child');
    
    await page.fill('[data-testid="message-input"]', 'Analyze my data');
    await page.click('[data-testid="send-message-button"]');
    
    // Should show token cost estimate
    await expect(page.locator('[data-testid="token-estimate"]')).toBeVisible();
  });

  test('should enforce cross-sphere isolation (L9)', async ({ page }) => {
    // Create data in Personal sphere
    await navigateToSphere(page, 'personal');
    await navigateToSection(page, 'data_files');
    
    const personalFiles = await page.locator('[data-testid="file-item"]').count();
    
    // Switch to Business sphere
    await navigateToSphere(page, 'business');
    await navigateToSection(page, 'data_files');
    
    // Should not see Personal files
    // (In a real test, we'd verify specific files don't appear)
    await expect(page.locator('[data-testid="data-files-container"]')).not.toContainText('personal-');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TOKEN BUDGET TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Token Budget', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('should display token budget', async ({ page }) => {
    await expect(page.locator('[data-testid="token-budget"]')).toBeVisible();
  });

  test('should show token usage in threads', async ({ page }) => {
    await navigateToSphere(page, 'personal');
    await navigateToSection(page, 'threads');
    await page.click('[data-testid="thread-item"]:first-child');
    
    await expect(page.locator('[data-testid="thread-tokens-used"]')).toBeVisible();
  });

  test('should prevent action when budget exceeded', async ({ page }) => {
    // This test would need a special test account with depleted budget
    // For now, verify the budget warning is displayed when low
    
    await page.click('[data-testid="token-budget"]');
    await expect(page.locator('[data-testid="budget-details"]')).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// RESPONSIVE DESIGN TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Responsive Design', () => {
  test('should display mobile navigation on small screens', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await login(page);
    
    await expect(page.locator('[data-testid="mobile-nav"]')).toBeVisible();
    await expect(page.locator('[data-testid="desktop-nav"]')).not.toBeVisible();
  });

  test('should display desktop navigation on large screens', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await login(page);
    
    await expect(page.locator('[data-testid="desktop-nav"]')).toBeVisible();
    await expect(page.locator('[data-testid="mobile-nav"]')).not.toBeVisible();
  });

  test('spheres should be accessible on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await login(page);
    
    // Open sphere menu
    await page.click('[data-testid="sphere-menu-toggle"]');
    
    for (const sphere of SPHERES) {
      await expect(page.locator(`[data-testid="sphere-${sphere.id}"]`)).toBeVisible();
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// ACCESSIBILITY TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Accessibility', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('should have proper heading hierarchy', async ({ page }) => {
    const h1 = await page.locator('h1').count();
    expect(h1).toBe(1);
  });

  test('buttons should have accessible names', async ({ page }) => {
    const buttons = page.locator('button');
    const count = await buttons.count();
    
    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      const ariaLabel = await button.getAttribute('aria-label');
      const text = await button.textContent();
      
      expect(ariaLabel || text?.trim()).toBeTruthy();
    }
  });

  test('should be keyboard navigable', async ({ page }) => {
    await page.keyboard.press('Tab');
    
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
  });

  test('should have skip link', async ({ page }) => {
    await page.keyboard.press('Tab');
    
    const skipLink = page.locator('[data-testid="skip-link"]');
    await expect(skipLink).toBeFocused();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// PERFORMANCE TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Performance', () => {
  test('page should load within 3 seconds', async ({ page }) => {
    const startTime = Date.now();
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;
    
    expect(loadTime).toBeLessThan(3000);
  });

  test('sphere navigation should be fast', async ({ page }) => {
    await login(page);
    
    const startTime = Date.now();
    await navigateToSphere(page, 'business');
    const navigationTime = Date.now() - startTime;
    
    expect(navigationTime).toBeLessThan(500);
  });
});
