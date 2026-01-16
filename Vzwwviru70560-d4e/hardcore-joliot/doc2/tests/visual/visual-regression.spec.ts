"""
═══════════════════════════════════════════════════════════════════════════════
CHE·NU™ — VISUAL REGRESSION TESTING (PERCY + CHROMATIC)
Q1 2026 - Week 8: Testing Excellence
═══════════════════════════════════════════════════════════════════════════════

Suite complète de visual regression pour détecter changements UI.
Target: 100% coverage UI, 0 regressions non intentionnelles

Créé: 20 Décembre 2025
Version: v41.4
"""

// ═══════════════════════════════════════════════════════════════════════════
// PERCY CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

/*
// .percy.yml

version: 2
snapshot:
  widths:
    - 375   # Mobile
    - 768   # Tablet
    - 1280  # Desktop
    - 1920  # Large desktop
  
  min-height: 1024
  
  enable-javascript: true
  
  discovery:
    allowed-hostnames:
      - localhost
      - "*.chenu.test"
    
    disable-cache: false
    
    network-idle-timeout: 750

static:
  include: "**/*.html"
  exclude: "**/node_modules/**"

agent:
  asset-discovery:
    network-idle-timeout: 750
    allowed-hostnames:
      - cdn.chenu.com
      - fonts.googleapis.com
      - fonts.gstatic.com
*/

// ═══════════════════════════════════════════════════════════════════════════
// PERCY + PLAYWRIGHT INTEGRATION
// ═══════════════════════════════════════════════════════════════════════════

import { test } from '@playwright/test'
import percySnapshot from '@percy/playwright'

const BASE_URL = 'http://localhost:3000'

test.describe('Visual Regression Tests', () => {
  // ─────────────────────────────────────────────────────────────────────────
  // AUTHENTICATION SCREENS
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Login Page', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`)
    
    await percySnapshot(page, 'Login Page', {
      widths: [375, 768, 1280]
    })
  })
  
  test('Login Page - Error State', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`)
    
    // Fill invalid credentials
    await page.fill('input[name="email"]', 'wrong@email.com')
    await page.fill('input[name="password"]', 'wrong')
    await page.click('button[type="submit"]')
    
    // Wait for error
    await page.waitForSelector('text=Invalid credentials')
    
    await percySnapshot(page, 'Login Page - Error State')
  })
  
  test('Signup Page', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`)
    
    await percySnapshot(page, 'Signup Page', {
      widths: [375, 768, 1280]
    })
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // SPHERE VIEWS
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Personal Sphere - Empty State', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    await percySnapshot(page, 'Personal Sphere - Empty')
  })
  
  test('Personal Sphere - With Threads', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    // Wait for threads to load
    await page.waitForSelector('[data-component="thread-list"]')
    
    await percySnapshot(page, 'Personal Sphere - With Threads', {
      widths: [375, 768, 1280, 1920]
    })
  })
  
  test('Business Sphere', async ({ page }) => {
    await page.goto(`${BASE_URL}/business`)
    
    await percySnapshot(page, 'Business Sphere')
  })
  
  test('Studio Sphere', async ({ page }) => {
    await page.goto(`${BASE_URL}/studio`)
    
    await percySnapshot(page, 'Studio de création Sphere')
  })
  
  test('All Spheres Navigation', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    const spheres = [
      'Personal',
      'Business',
      'Government & Institutions',
      'Studio de création',
      'Community',
      'Social & Media',
      'Entertainment',
      'My Team',
      'Scholar'
    ]
    
    for (const sphere of spheres) {
      await page.click(`text=${sphere}`)
      await page.waitForSelector(`[data-sphere="${sphere}"][data-active="true"]`)
      
      await percySnapshot(page, `${sphere} Sphere`)
    }
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // THREAD VIEWS
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Thread List - Desktop', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    await percySnapshot(page, 'Thread List - Desktop', {
      widths: [1280, 1920]
    })
  })
  
  test('Thread List - Mobile', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    await percySnapshot(page, 'Thread List - Mobile', {
      widths: [375]
    })
  })
  
  test('Thread Detail - Empty', async ({ page }) => {
    await page.goto(`${BASE_URL}/threads/new`)
    
    await percySnapshot(page, 'Thread Detail - Empty')
  })
  
  test('Thread Detail - With Messages', async ({ page }) => {
    await page.goto(`${BASE_URL}/threads/test-thread`)
    
    // Wait for messages
    await page.waitForSelector('[data-component="message-list"]')
    
    await percySnapshot(page, 'Thread Detail - With Messages', {
      widths: [375, 768, 1280]
    })
  })
  
  test('Thread Composer', async ({ page }) => {
    await page.goto(`${BASE_URL}/threads/test-thread`)
    
    // Focus on composer
    await page.click('textarea[placeholder="Type a message"]')
    
    await percySnapshot(page, 'Thread Composer - Active')
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // AGENT VIEWS
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Agent List', async ({ page }) => {
    await page.goto(`${BASE_URL}/team`)
    
    await percySnapshot(page, 'Agent List')
  })
  
  test('Agent Detail - Nova', async ({ page }) => {
    await page.goto(`${BASE_URL}/agents/nova`)
    
    await percySnapshot(page, 'Agent Detail - Nova', {
      widths: [375, 1280]
    })
  })
  
  test('Agent Hire Modal', async ({ page }) => {
    await page.goto(`${BASE_URL}/team`)
    
    // Open hire modal
    await page.click('button:has-text("Hire Agent")')
    await page.waitForSelector('[role="dialog"]')
    
    await percySnapshot(page, 'Agent Hire Modal')
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // MODALS & DIALOGS
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Settings Modal', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    // Open settings
    await page.click('[aria-label="User menu"]')
    await page.click('text=Settings')
    
    await page.waitForSelector('[role="dialog"]')
    
    await percySnapshot(page, 'Settings Modal', {
      widths: [375, 768, 1280]
    })
  })
  
  test('Confirmation Dialog', async ({ page }) => {
    await page.goto(`${BASE_URL}/threads/test-thread`)
    
    // Trigger delete
    await page.click('[aria-label="Delete thread"]')
    await page.waitForSelector('[role="alertdialog"]')
    
    await percySnapshot(page, 'Confirmation Dialog')
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // THEME VARIATIONS
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Dark Mode', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    // Enable dark mode
    await page.evaluate(() => {
      document.documentElement.classList.add('dark')
    })
    
    await percySnapshot(page, 'Personal Sphere - Dark Mode')
  })
  
  test('Light Mode', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    // Ensure light mode
    await page.evaluate(() => {
      document.documentElement.classList.remove('dark')
    })
    
    await percySnapshot(page, 'Personal Sphere - Light Mode')
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // LOADING STATES
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Loading State - Skeleton', async ({ page }) => {
    // Intercept API to delay response
    await page.route('**/api/v1/threads', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 5000))
      await route.continue()
    })
    
    await page.goto(`${BASE_URL}/personal`)
    
    // Capture loading state
    await percySnapshot(page, 'Loading State - Skeleton')
  })
  
  test('Loading State - Spinner', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    // Trigger loading
    await page.click('button:has-text("Refresh")')
    
    await percySnapshot(page, 'Loading State - Spinner')
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // ERROR STATES
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Error State - 404', async ({ page }) => {
    await page.goto(`${BASE_URL}/not-found`)
    
    await percySnapshot(page, 'Error State - 404')
  })
  
  test('Error State - 500', async ({ page }) => {
    // Mock 500 error
    await page.route('**/api/v1/threads', (route) => {
      route.fulfill({
        status: 500,
        body: 'Internal Server Error'
      })
    })
    
    await page.goto(`${BASE_URL}/personal`)
    
    await percySnapshot(page, 'Error State - 500')
  })
  
  test('Error State - Network Offline', async ({ page, context }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    // Go offline
    await context.setOffline(true)
    
    // Trigger action that requires network
    await page.click('button:has-text("Refresh")')
    
    await percySnapshot(page, 'Error State - Offline')
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // RESPONSIVE VIEWS
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Mobile - Navigation Menu', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto(`${BASE_URL}/personal`)
    
    // Open mobile menu
    await page.click('[aria-label="Menu"]')
    
    await percySnapshot(page, 'Mobile - Navigation Menu')
  })
  
  test('Tablet - Split View', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.goto(`${BASE_URL}/personal`)
    
    await percySnapshot(page, 'Tablet - Split View')
  })
  
  // ─────────────────────────────────────────────────────────────────────────
  // ANIMATIONS & TRANSITIONS
  // ─────────────────────────────────────────────────────────────────────────
  
  test('Hover State - Sphere Card', async ({ page }) => {
    await page.goto(`${BASE_URL}/personal`)
    
    // Hover over sphere card
    await page.hover('[data-sphere-card="business"]')
    
    await percySnapshot(page, 'Hover State - Sphere Card')
  })
  
  test('Focus State - Input', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`)
    
    // Focus on email input
    await page.focus('input[name="email"]')
    
    await percySnapshot(page, 'Focus State - Email Input')
  })
})

// ═══════════════════════════════════════════════════════════════════════════
// CHROMATIC CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════

/*
// .storybook/main.js

module.exports = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
  ],
  framework: '@storybook/react',
}
*/

/*
// src/components/SphereCard.stories.tsx

import { Meta, StoryObj } from '@storybook/react'
import { SphereCard } from './SphereCard'

const meta: Meta<typeof SphereCard> = {
  title: 'Components/SphereCard',
  component: SphereCard,
  parameters: {
    chromatic: {
      // Delay to wait for animations
      delay: 300,
      
      // Pause animations
      pauseAnimationAtEnd: true,
      
      // Viewports to test
      viewports: [375, 768, 1280]
    }
  }
}

export default meta
type Story = StoryObj<typeof SphereCard>

export const Default: Story = {
  args: {
    sphere: {
      id: 'personal',
      name: 'Personal',
      icon: '🏠',
      color: '#D8B26A'
    }
  }
}

export const Active: Story = {
  args: {
    ...Default.args,
    active: true
  }
}

export const WithCount: Story = {
  args: {
    ...Default.args,
    count: 12
  }
}

export const Hover: Story = {
  args: Default.args,
  parameters: {
    pseudo: { hover: true }
  }
}

export const DarkMode: Story = {
  args: Default.args,
  parameters: {
    backgrounds: {
      default: 'dark'
    }
  },
  decorators: [
    (Story) => (
      <div className="dark">
        <Story />
      </div>
    )
  ]
}
*/

// ═══════════════════════════════════════════════════════════════════════════
// PACKAGE.JSON SCRIPTS
// ═══════════════════════════════════════════════════════════════════════════

/*
{
  "scripts": {
    // Percy
    "test:visual": "percy exec -- playwright test visual.spec.ts",
    "test:visual:update": "percy exec -- playwright test visual.spec.ts --update-snapshots",
    
    // Chromatic
    "chromatic": "chromatic --project-token=<token>",
    "chromatic:ci": "chromatic --exit-zero-on-changes",
    
    // Storybook
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  },
  "devDependencies": {
    "@percy/cli": "^1.27.0",
    "@percy/playwright": "^1.0.4",
    "chromatic": "^10.0.0",
    "@storybook/react": "^7.6.0"
  }
}
*/

// ═══════════════════════════════════════════════════════════════════════════
// GITHUB ACTIONS WORKFLOW
// ═══════════════════════════════════════════════════════════════════════════

/*
// .github/workflows/visual-regression.yml

name: Visual Regression Tests

on: [push, pull_request]

jobs:
  percy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Run Percy
        run: npm run test:visual
        env:
          PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}
  
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Publish to Chromatic
        uses: chromaui/action@v1
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          exitZeroOnChanges: true
*/

// ═══════════════════════════════════════════════════════════════════════════
// RUNNING TESTS
// ═══════════════════════════════════════════════════════════════════════════

/*
PERCY SETUP:
1. Sign up at percy.io
2. Create project
3. Get PERCY_TOKEN
4. export PERCY_TOKEN=<your-token>

RUN PERCY:
npm run test:visual

CHROMATIC SETUP:
1. Sign up at chromatic.com
2. Link repository
3. Get project token
4. npx chromatic --project-token=<token>

RUN CHROMATIC:
npm run chromatic

VIEW RESULTS:
- Percy: https://percy.io/your-org/chenu
- Chromatic: https://chromatic.com/builds?appId=<id>
*/

// ═══════════════════════════════════════════════════════════════════════════
// EXPECTED RESULTS
// ═══════════════════════════════════════════════════════════════════════════

/*
TARGETS:

Coverage:
✅ 100% UI components covered
✅ All spheres tested
✅ All states tested (loading, error, empty)

Viewports:
✅ Mobile (375px)
✅ Tablet (768px)
✅ Desktop (1280px)
✅ Large Desktop (1920px)

Themes:
✅ Light mode
✅ Dark mode

States:
✅ Default
✅ Hover
✅ Focus
✅ Active
✅ Loading
✅ Error
✅ Empty

Regressions:
✅ 0 unintentional changes
✅ 100% review coverage
✅ Approved changes only
*/

export {}
