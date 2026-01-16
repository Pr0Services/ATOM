// ═══════════════════════════════════════════════════════════════════════════════
// CHE·NU™ — E2E NAVIGATION TESTS
// Sprint 2: End-to-end tests for sphere and bureau navigation
// Architecture: 9 Spheres + 6 Bureau Sections
// ═══════════════════════════════════════════════════════════════════════════════

import { test, expect, type Page } from '@playwright/test';

// ═══════════════════════════════════════════════════════════════════════════════
// TEST DATA - 9 SPHERES (FROZEN)
// ═══════════════════════════════════════════════════════════════════════════════

const SPHERES = [
  { id: 'personal', name: 'Personal', icon: '🏠', route: '/personal' },
  { id: 'business', name: 'Business', icon: '💼', route: '/business' },
  { id: 'government', name: 'Government', icon: '🏛️', route: '/government' },
  { id: 'creative', name: 'Creative Studio', icon: '🎨', route: '/creative' },
  { id: 'community', name: 'Community', icon: '👥', route: '/community' },
  { id: 'social', name: 'Social & Media', icon: '📱', route: '/social' },
  { id: 'entertainment', name: 'Entertainment', icon: '🎬', route: '/entertainment' },
  { id: 'team', name: 'My Team', icon: '🤝', route: '/team' },
  { id: 'scholar', name: 'Scholar', icon: '📚', route: '/scholar' },
];

// 6 BUREAU SECTIONS (HARD LIMIT)
const BUREAU_SECTIONS = [
  { id: 'quick_capture', name: 'Quick Capture', icon: '📝', testId: 'bureau-section-quick-capture' },
  { id: 'resume_workspace', name: 'Resume Workspace', icon: '▶️', testId: 'bureau-section-resume-workspace' },
  { id: 'threads', name: 'Threads', icon: '💬', testId: 'bureau-section-threads' },
  { id: 'data_files', name: 'Data Files', icon: '📁', testId: 'bureau-section-data-files' },
  { id: 'active_agents', name: 'Active Agents', icon: '🤖', testId: 'bureau-section-active-agents' },
  { id: 'meetings', name: 'Meetings', icon: '📅', testId: 'bureau-section-meetings' },
];

// ═══════════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════

async function navigateToSphere(page: Page, sphereId: string) {
  await page.getByTestId(`sphere-${sphereId}`).click();
  await page.waitForURL(`**/${sphereId}**`);
}

async function navigateToSection(page: Page, sectionId: string) {
  await page.getByTestId(`bureau-section-${sectionId}`).click();
}

async function getCurrentSphere(page: Page): Promise<string | null> {
  const activeElement = page.locator('[data-active="true"][data-testid^="sphere-"]');
  const testId = await activeElement.getAttribute('data-testid');
  return testId?.replace('sphere-', '') || null;
}

async function getCurrentSection(page: Page): Promise<string | null> {
  const activeElement = page.locator('[data-active="true"][data-testid^="bureau-section-"]');
  const testId = await activeElement.getAttribute('data-testid');
  return testId?.replace('bureau-section-', '') || null;
}

// ═══════════════════════════════════════════════════════════════════════════════
// APP LOAD TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('App Loading', () => {
  test('should load the application', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/CHE·NU/i);
  });

  test('should show main navigation', async ({ page }) => {
    await page.goto('/');
    
    // Should have sphere navigation
    const sphereNav = page.getByTestId('sphere-navigation');
    await expect(sphereNav).toBeVisible();
  });

  test('should default to Personal sphere', async ({ page }) => {
    await page.goto('/');
    
    const currentSphere = await getCurrentSphere(page);
    expect(currentSphere).toBe('personal');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 9 SPHERES NAVIGATION TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('9 Spheres Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display all 9 spheres', async ({ page }) => {
    for (const sphere of SPHERES) {
      const sphereElement = page.getByTestId(`sphere-${sphere.id}`);
      await expect(sphereElement).toBeVisible();
    }
  });

  test('should display Scholar sphere (9th sphere)', async ({ page }) => {
    const scholarSphere = page.getByTestId('sphere-scholar');
    await expect(scholarSphere).toBeVisible();
    await expect(scholarSphere).toContainText('📚');
  });

  test('should navigate to each sphere', async ({ page }) => {
    for (const sphere of SPHERES) {
      await navigateToSphere(page, sphere.id);
      
      const currentSphere = await getCurrentSphere(page);
      expect(currentSphere).toBe(sphere.id);
    }
  });

  test('sphere navigation should update URL', async ({ page }) => {
    await navigateToSphere(page, 'business');
    await expect(page).toHaveURL(/.*business.*/);
    
    await navigateToSphere(page, 'scholar');
    await expect(page).toHaveURL(/.*scholar.*/);
  });

  test('should only show one active sphere at a time', async ({ page }) => {
    await navigateToSphere(page, 'business');
    
    const activeSpheres = page.locator('[data-active="true"][data-testid^="sphere-"]');
    await expect(activeSpheres).toHaveCount(1);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// 6 BUREAU SECTIONS TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('6 Bureau Sections', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display all 6 bureau sections', async ({ page }) => {
    for (const section of BUREAU_SECTIONS) {
      const sectionElement = page.getByTestId(section.testId);
      await expect(sectionElement).toBeVisible();
    }
  });

  test('should have exactly 6 sections (HARD LIMIT)', async ({ page }) => {
    const sections = page.locator('[data-testid^="bureau-section-"]');
    await expect(sections).toHaveCount(6);
  });

  test('should navigate to each section', async ({ page }) => {
    for (const section of BUREAU_SECTIONS) {
      await navigateToSection(page, section.id);
      
      const currentSection = await getCurrentSection(page);
      expect(currentSection).toBe(section.id);
    }
  });

  test('Quick Capture should be first section', async ({ page }) => {
    const firstSection = page.locator('[data-testid^="bureau-section-"]').first();
    await expect(firstSection).toHaveAttribute('data-testid', 'bureau-section-quick-capture');
  });

  test('Meetings should be last section', async ({ page }) => {
    const lastSection = page.locator('[data-testid^="bureau-section-"]').last();
    await expect(lastSection).toHaveAttribute('data-testid', 'bureau-section-meetings');
  });

  test('should reset to Quick Capture when changing sphere', async ({ page }) => {
    // Navigate to threads section
    await navigateToSection(page, 'threads');
    
    // Change sphere
    await navigateToSphere(page, 'business');
    
    // Should reset to quick_capture
    const currentSection = await getCurrentSection(page);
    expect(currentSection).toBe('quick_capture');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// BUREAU PER SPHERE TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Bureau per Sphere', () => {
  test('each sphere should have same bureau structure', async ({ page }) => {
    for (const sphere of SPHERES) {
      await page.goto('/');
      await navigateToSphere(page, sphere.id);
      
      // Verify all 6 sections exist
      for (const section of BUREAU_SECTIONS) {
        const sectionElement = page.getByTestId(section.testId);
        await expect(sectionElement).toBeVisible();
      }
    }
  });

  test('Scholar sphere should have 6 sections', async ({ page }) => {
    await page.goto('/');
    await navigateToSphere(page, 'scholar');
    
    const sections = page.locator('[data-testid^="bureau-section-"]');
    await expect(sections).toHaveCount(6);
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// NAVIGATION HISTORY TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Navigation History', () => {
  test('should support browser back button', async ({ page }) => {
    await page.goto('/');
    
    // Navigate through spheres
    await navigateToSphere(page, 'business');
    await navigateToSphere(page, 'creative');
    
    // Go back
    await page.goBack();
    
    const currentSphere = await getCurrentSphere(page);
    expect(currentSphere).toBe('business');
  });

  test('should support browser forward button', async ({ page }) => {
    await page.goto('/');
    
    await navigateToSphere(page, 'business');
    await navigateToSphere(page, 'creative');
    
    await page.goBack();
    await page.goForward();
    
    const currentSphere = await getCurrentSphere(page);
    expect(currentSphere).toBe('creative');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// NOVA PRESENCE TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Nova Presence', () => {
  test('Nova should be accessible from all spheres', async ({ page }) => {
    for (const sphere of SPHERES) {
      await page.goto('/');
      await navigateToSphere(page, sphere.id);
      
      const novaButton = page.getByTestId('nova-toggle');
      await expect(novaButton).toBeVisible();
    }
  });

  test('should toggle Nova panel', async ({ page }) => {
    await page.goto('/');
    
    // Open Nova
    await page.getByTestId('nova-toggle').click();
    
    const novaPanel = page.getByTestId('nova-panel');
    await expect(novaPanel).toBeVisible();
    
    // Close Nova
    await page.getByTestId('nova-toggle').click();
    await expect(novaPanel).not.toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// RESPONSIVE TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Responsive Design', () => {
  test('should work on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Should still show spheres (possibly in menu)
    const mobileMenu = page.getByTestId('mobile-menu');
    if (await mobileMenu.isVisible()) {
      await mobileMenu.click();
    }
    
    // Personal sphere should be accessible
    const personalSphere = page.getByTestId('sphere-personal');
    await expect(personalSphere).toBeVisible();
  });

  test('should work on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    
    // Navigation should be visible
    const sphereNav = page.getByTestId('sphere-navigation');
    await expect(sphereNav).toBeVisible();
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// ACCESSIBILITY TESTS
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Accessibility', () => {
  test('should have proper focus management', async ({ page }) => {
    await page.goto('/');
    
    // Tab through spheres
    await page.keyboard.press('Tab');
    
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
  });

  test('sphere navigation should be keyboard accessible', async ({ page }) => {
    await page.goto('/');
    
    // Focus on sphere navigation
    await page.getByTestId('sphere-personal').focus();
    
    // Navigate with arrow keys
    await page.keyboard.press('ArrowRight');
    
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toHaveAttribute('data-testid', 'sphere-business');
  });

  test('sections should have ARIA labels', async ({ page }) => {
    await page.goto('/');
    
    for (const section of BUREAU_SECTIONS) {
      const sectionElement = page.getByTestId(section.testId);
      const ariaLabel = await sectionElement.getAttribute('aria-label');
      expect(ariaLabel).toBeTruthy();
    }
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// MEMORY PROMPT COMPLIANCE E2E
// ═══════════════════════════════════════════════════════════════════════════════

test.describe('Memory Prompt Compliance', () => {
  test('should have exactly 9 spheres (FROZEN architecture)', async ({ page }) => {
    await page.goto('/');
    
    const spheres = page.locator('[data-testid^="sphere-"]');
    await expect(spheres).toHaveCount(9);
  });

  test('should have exactly 6 bureau sections (HARD LIMIT)', async ({ page }) => {
    await page.goto('/');
    
    const sections = page.locator('[data-testid^="bureau-section-"]');
    await expect(sections).toHaveCount(6);
  });

  test('only one sphere active at a time', async ({ page }) => {
    await page.goto('/');
    
    const activeSpheres = page.locator('[data-active="true"][data-testid^="sphere-"]');
    await expect(activeSpheres).toHaveCount(1);
  });

  test('one bureau visible at a time', async ({ page }) => {
    await page.goto('/');
    
    const visibleBureaus = page.locator('[data-testid="bureau-content"]:visible');
    await expect(visibleBureaus).toHaveCount(1);
  });
});
