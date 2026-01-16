/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * CHE·NU™ — TESTS DE CONFORMITÉ PLAYWRIGHT
 * Format: GIVEN / WHEN / THEN
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * ⚠️ DIRECTIVE: Ces tests valident la conformité à la state machine canonique
 * 
 * @version 2.0.0
 * @date 2024-12-19
 */

import { test, expect, Page } from '@playwright/test';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const STATES = {
  PRE_ACCOUNT: 'STATE_PRE_ACCOUNT',
  ONBOARDING_THEME: 'STATE_ONBOARDING_THEME',
  ONBOARDING_SPHERES: 'STATE_ONBOARDING_SPHERES',
  PERSONAL_INIT: 'STATE_PERSONAL_INIT',
  DASHBOARD_ACTIVATION: 'STATE_DASHBOARD_ACTIVATION',
  OPERATIONAL: 'STATE_OPERATIONAL',
  SPHERE_LOBBY: 'STATE_SPHERE_LOBBY',
  SPHERE_BUREAU: 'STATE_SPHERE_BUREAU',
  WORKSPACE_ACTIVE: 'STATE_WORKSPACE_ACTIVE',
  AGENT_EXECUTION: 'STATE_AGENT_EXECUTION',
  VERSION_REVIEW: 'STATE_VERSION_REVIEW',
} as const;

const SPHERES = [
  'PERSONAL',
  'BUSINESS',
  'GOVERNMENT_INSTITUTIONS',
  'CREATIVE_STUDIO',
  'ENTERTAINMENT',
  'COMMUNITY',
  'SOCIAL_MEDIA',
  'MY_TEAM',
] as const;

// ═══════════════════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

async function getCurrentState(page: Page): Promise<string> {
  return await page.evaluate(() => {
    return (window as any).store.getState().stateMachine.currentState;
  });
}

async function login(page: Page) {
  await page.click('[data-testid="create-account-btn"]');
  await page.fill('[data-testid="email-input"]', 'test@chenu.io');
  await page.fill('[data-testid="password-input"]', 'Test123!');
  await page.click('[data-testid="submit-btn"]');
}

async function completeOnboarding(page: Page) {
  // Select theme
  await page.click('[data-testid="theme-option-0"]');
  await page.click('[data-testid="continue-btn"]');
  
  // Wait for spheres tour
  await page.waitForTimeout(3500);
  await page.click('[data-testid="continue-btn"]');
  
  // Complete personal init
  await page.fill('[data-testid="personal-notes"]', 'Mes objectifs');
  await page.click('[data-testid="continue-btn"]');
  
  // Enter operational
  await page.click('[data-testid="start-operational-btn"]');
}

async function enterSphereAndBureau(page: Page, sphereId: string) {
  await page.click(`[data-testid="sphere-${sphereId.toLowerCase()}"]`);
  await page.click('[data-testid="enter-bureau-btn"]');
}

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 1 — STRUCTURE DES HUBS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST 1 — Structure des HUBS', () => {
  test('GIVEN application chargée WHEN navigation THEN HUB_C toujours actif', async ({ page }) => {
    await page.goto('/');
    
    // Login and complete onboarding
    await login(page);
    await completeOnboarding(page);
    
    // Check HUB_C always visible
    await expect(page.locator('[data-testid="hub-communication"]')).toBeVisible();
    await expect(page.locator('[data-testid="nova-avatar"]')).toBeVisible();
    
    // Navigate through spheres
    for (const sphere of SPHERES.slice(0, 3)) {
      await page.click(`[data-testid="sphere-${sphere.toLowerCase()}"]`);
      await expect(page.locator('[data-testid="hub-communication"]')).toBeVisible();
    }
  });

  test('GIVEN application chargée THEN maximum 2 hubs visibles', async ({ page }) => {
    await page.goto('/');
    await login(page);
    await completeOnboarding(page);
    
    const visibleHubs = await page.locator('[data-testid^="hub-"]:visible').count();
    expect(visibleHubs).toBeLessThanOrEqual(2);
  });

  test('GIVEN application chargée THEN aucun hub ne bloque un autre', async ({ page }) => {
    await page.goto('/');
    await login(page);
    await completeOnboarding(page);
    
    // Click navigation hub
    await page.click('[data-testid="hub-navigation"]');
    
    // Other hubs should not be disabled
    await expect(page.locator('[data-testid="hub-execution"]')).not.toBeDisabled();
    await expect(page.locator('[data-testid="hub-communication"]')).not.toBeDisabled();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 2 — STATE MACHINE
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST 2 — State Machine', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    await page.reload();
  });

  test('GIVEN état PRE_ACCOUNT WHEN tentative entrée sphère THEN refusée', async ({ page }) => {
    // Check initial state
    const state = await getCurrentState(page);
    expect(state).toBe(STATES.PRE_ACCOUNT);
    
    // Try to click sphere
    await page.click('[data-testid="sphere-personal"]', { force: true });
    
    // Should show error
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="error-message"]')).toContainText('Créez un compte');
  });

  test('GIVEN PRE_ACCOUNT WHEN CREATE_ACCOUNT THEN transition ONBOARDING_THEME', async ({ page }) => {
    // Initial state
    expect(await getCurrentState(page)).toBe(STATES.PRE_ACCOUNT);
    
    // Create account
    await login(page);
    
    // Check new state
    expect(await getCurrentState(page)).toBe(STATES.ONBOARDING_THEME);
    await expect(page.locator('[data-testid="theme-selector"]')).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 3 — ONBOARDING
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST 3 — Onboarding', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    await page.reload();
    await login(page);
  });

  test('GIVEN nouvel utilisateur WHEN termine PERSONNEL THEN dashboard apparaît', async ({ page }) => {
    // Complete theme
    await page.click('[data-testid="theme-option-0"]');
    await page.click('[data-testid="continue-btn"]');
    
    // Complete spheres tour
    await page.waitForTimeout(3500);
    await page.click('[data-testid="continue-btn"]');
    
    // Check personal init state
    expect(await getCurrentState(page)).toBe(STATES.PERSONAL_INIT);
    
    // Complete personal
    await page.fill('[data-testid="personal-notes"]', 'Mes objectifs');
    await page.click('[data-testid="continue-btn"]');
    
    // Dashboard should appear
    expect(await getCurrentState(page)).toBe(STATES.DASHBOARD_ACTIVATION);
    await expect(page.locator('[data-testid="dashboard"]')).toBeVisible();
  });

  test('GIVEN PERSONNEL complété THEN autres sphères verrouillées', async ({ page }) => {
    // Complete to dashboard
    await page.click('[data-testid="theme-option-0"]');
    await page.click('[data-testid="continue-btn"]');
    await page.waitForTimeout(3500);
    await page.click('[data-testid="continue-btn"]');
    await page.fill('[data-testid="personal-notes"]', 'Test');
    await page.click('[data-testid="continue-btn"]');
    
    // Check other spheres are locked
    for (const sphere of SPHERES.filter(s => s !== 'PERSONAL')) {
      const sphereEl = page.locator(`[data-testid="sphere-${sphere.toLowerCase()}"]`);
      await expect(sphereEl).toHaveAttribute('data-locked', 'true');
    }
    
    // Personal is active
    await expect(page.locator('[data-testid="sphere-personal"]')).toHaveAttribute('data-locked', 'false');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 4 — BUREAU
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST 4 — Bureau', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await login(page);
    await completeOnboarding(page);
    await enterSphereAndBureau(page, 'PERSONAL');
  });

  test('GIVEN sphère active WHEN entre bureau THEN max 8 objets', async ({ page }) => {
    expect(await getCurrentState(page)).toBe(STATES.SPHERE_BUREAU);
    
    const objectCount = await page.locator('[data-testid^="bureau-object-"]').count();
    expect(objectCount).toBeLessThanOrEqual(8);
  });

  test('GIVEN bureau affiché THEN aucun document directement', async ({ page }) => {
    expect(await getCurrentState(page)).toBe(STATES.SPHERE_BUREAU);
    
    await expect(page.locator('[data-testid="document-content"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="document-preview"]')).not.toBeVisible();
  });

  test('GIVEN bureau THEN tous objets cliquables', async ({ page }) => {
    const objects = page.locator('[data-testid^="bureau-object-"]');
    const count = await objects.count();
    
    for (let i = 0; i < count; i++) {
      await expect(objects.nth(i)).not.toBeDisabled();
      await expect(objects.nth(i)).toHaveCSS('cursor', 'pointer');
    }
  });

  test('GIVEN objet cliqué THEN transition WORKSPACE_ACTIVE', async ({ page }) => {
    await page.click('[data-testid="bureau-object-notes"]');
    
    expect(await getCurrentState(page)).toBe(STATES.WORKSPACE_ACTIVE);
    await expect(page.locator('[data-testid="workspace-container"]')).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 5 — WORKSPACE & VERSIONING
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST 5 — Workspace & Versioning', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await login(page);
    await completeOnboarding(page);
    await enterSphereAndBureau(page, 'PERSONAL');
    await page.click('[data-testid="bureau-object-notes"]');
  });

  test('GIVEN document modifié WHEN envoyé agent THEN version originale conservée', async ({ page }) => {
    // Create content
    await page.fill('[data-testid="workspace-editor"]', 'Contenu original');
    await page.click('[data-testid="save-btn"]');
    
    // Send to agent
    await page.click('[data-testid="send-to-agent-btn"]');
    await page.click('[data-testid="agent-option-content-enhancer"]');
    await page.click('[data-testid="confirm-send-btn"]');
    
    // Wait for completion
    await page.waitForSelector('[data-testid="agent-status"]:has-text("Complete")', { timeout: 30000 });
    
    // Original version preserved
    await expect(page.locator('[data-testid="version-original"]')).toContainText('Contenu original');
  });

  test('GIVEN agent terminé THEN version agent séparée', async ({ page }) => {
    await page.fill('[data-testid="workspace-editor"]', 'Test content');
    await page.click('[data-testid="save-btn"]');
    await page.click('[data-testid="send-to-agent-btn"]');
    await page.click('[data-testid="agent-option-content-enhancer"]');
    await page.click('[data-testid="confirm-send-btn"]');
    await page.waitForSelector('[data-testid="agent-status"]:has-text("Complete")', { timeout: 30000 });
    
    expect(await getCurrentState(page)).toBe(STATES.VERSION_REVIEW);
    await expect(page.locator('[data-testid="version-agent"]')).toBeVisible();
    await expect(page.locator('[data-testid="version-original"]')).toBeVisible();
  });

  test('GIVEN versions affichées THEN diff visuel disponible', async ({ page }) => {
    await page.fill('[data-testid="workspace-editor"]', 'Test');
    await page.click('[data-testid="save-btn"]');
    await page.click('[data-testid="send-to-agent-btn"]');
    await page.click('[data-testid="agent-option-content-enhancer"]');
    await page.click('[data-testid="confirm-send-btn"]');
    await page.waitForSelector('[data-testid="agent-status"]:has-text("Complete")', { timeout: 30000 });
    
    await expect(page.locator('[data-testid="diff-view"]')).toBeVisible();
    await expect(page.locator('[data-testid="diff-additions"]')).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 6 — AGENTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST 6 — Agents', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await login(page);
    await completeOnboarding(page);
    await enterSphereAndBureau(page, 'PERSONAL');
    await page.click('[data-testid="bureau-object-notes"]');
  });

  test('GIVEN agent actif THEN workspace isolé', async ({ page }) => {
    await page.fill('[data-testid="workspace-editor"]', 'Test');
    await page.click('[data-testid="send-to-agent-btn"]');
    await page.click('[data-testid="agent-option-content-enhancer"]');
    await page.click('[data-testid="confirm-send-btn"]');
    
    expect(await getCurrentState(page)).toBe(STATES.AGENT_EXECUTION);
    
    await expect(page.locator('[data-testid="agent-workspace"]')).toBeVisible();
    await expect(page.locator('[data-testid="agent-workspace"]')).toHaveAttribute('data-isolated', 'true');
  });

  test('GIVEN agent actif THEN logs visibles', async ({ page }) => {
    await page.fill('[data-testid="workspace-editor"]', 'Test');
    await page.click('[data-testid="send-to-agent-btn"]');
    await page.click('[data-testid="agent-option-content-enhancer"]');
    await page.click('[data-testid="confirm-send-btn"]');
    
    await expect(page.locator('[data-testid="agent-logs"]')).toBeVisible();
    await expect(page.locator('[data-testid="agent-progress"]')).toBeVisible();
  });

  test('GIVEN agent terminé THEN validation requise', async ({ page }) => {
    await page.fill('[data-testid="workspace-editor"]', 'Original');
    await page.click('[data-testid="save-btn"]');
    await page.click('[data-testid="send-to-agent-btn"]');
    await page.click('[data-testid="agent-option-content-enhancer"]');
    await page.click('[data-testid="confirm-send-btn"]');
    await page.waitForSelector('[data-testid="agent-status"]:has-text("Complete")', { timeout: 30000 });
    
    // Should be in VERSION_REVIEW (not auto-merged)
    expect(await getCurrentState(page)).toBe(STATES.VERSION_REVIEW);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 7 — DONNÉES
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST 7 — Données', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await login(page);
    await completeOnboarding(page);
    await enterSphereAndBureau(page, 'PERSONAL');
    await page.click('[data-testid="bureau-object-notes"]');
  });

  test('GIVEN utilisateur refuse THEN aucune fusion', async ({ page }) => {
    await page.fill('[data-testid="workspace-editor"]', 'Original content');
    await page.click('[data-testid="save-btn"]');
    await page.click('[data-testid="send-to-agent-btn"]');
    await page.click('[data-testid="agent-option-content-enhancer"]');
    await page.click('[data-testid="confirm-send-btn"]');
    await page.waitForSelector('[data-testid="agent-status"]:has-text("Complete")', { timeout: 30000 });
    
    // Reject
    await page.click('[data-testid="reject-btn"]');
    
    // Back to workspace with original
    expect(await getCurrentState(page)).toBe(STATES.WORKSPACE_ACTIVE);
    await expect(page.locator('[data-testid="workspace-editor"]')).toContainText('Original content');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 9 — RÉGRESSION STRUCTURELLE
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST 9 — Régression Structurelle', () => {
  test('GIVEN mise à jour THEN 3 hubs présents', async ({ page }) => {
    await page.goto('/');
    
    const hubs = await page.evaluate(() => {
      return Object.keys((window as any).CHENU_CONFIG.hubs);
    });
    
    expect(hubs).toHaveLength(3);
    expect(hubs).toContain('NAVIGATION');
    expect(hubs).toContain('EXECUTION');
    expect(hubs).toContain('COMMUNICATION');
  });

  test('GIVEN mise à jour THEN 8 sphères exactement', async ({ page }) => {
    await page.goto('/');
    
    const spheres = await page.evaluate(() => {
      return (window as any).CHENU_CONFIG.spheres.map((s: any) => s.id);
    });
    
    expect(spheres).toHaveLength(8);
    expect(spheres).toEqual(SPHERES);
  });

  test('GIVEN mise à jour THEN 10 lois fondamentales', async ({ page }) => {
    await page.goto('/');
    
    const laws = await page.evaluate(() => {
      return (window as any).CHENU_CONFIG.fundamental_laws;
    });
    
    expect(laws).toHaveLength(10);
    expect(laws[0].law).toContain('Nova');
    expect(laws[9].law).toContain('ne change jamais');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST FINAL
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('TEST FINAL — Acceptation', () => {
  test('Architecture validée', async ({ page }) => {
    await page.goto('/');
    
    // Verify complete structure
    const config = await page.evaluate(() => (window as any).CHENU_CONFIG);
    
    expect(Object.keys(config.hubs)).toHaveLength(3);
    expect(config.spheres).toHaveLength(8);
    expect(config.fundamental_laws).toHaveLength(10);
    expect(config.global_rules.immutable_structure).toBe(true);
    expect(config.global_rules.nova_role).toBe('GUIDE_ONLY');
    expect(config.global_rules.agent_execution_requires_validation).toBe(true);
  });
});
