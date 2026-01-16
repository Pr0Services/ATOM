/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ — NAVIGATION E2E TESTS                            ║
 * ║                    Test sphere navigation (9 Sphères, 6 Sections)            ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

describe('Navigation Flow', () => {
  beforeEach(() => {
    // Mock authentication
    cy.intercept('GET', '**/users/me', {
      statusCode: 200,
      body: {
        id: 'test-id',
        email: 'test@example.com',
        display_name: 'Test User',
      },
    })

    cy.intercept('GET', '**/spheres', {
      statusCode: 200,
      body: [
        { id: 'personal', code: 'PER', name_fr: 'Personnel', name_en: 'Personal', icon: '👤', order: 1 },
        { id: 'business', code: 'BUS', name_fr: 'Affaires', name_en: 'Business', icon: '💼', order: 2 },
        { id: 'government', code: 'GOV', name_fr: 'Gouvernement', name_en: 'Government', icon: '🏛️', order: 3 },
        { id: 'studio', code: 'STU', name_fr: 'Studio Créatif', name_en: 'Creative Studio', icon: '🎨', order: 4 },
        { id: 'community', code: 'COM', name_fr: 'Communauté', name_en: 'Community', icon: '👥', order: 5 },
        { id: 'social', code: 'SOC', name_fr: 'Social & Médias', name_en: 'Social & Media', icon: '📱', order: 6 },
        { id: 'entertainment', code: 'ENT', name_fr: 'Divertissement', name_en: 'Entertainment', icon: '🎬', order: 7 },
        { id: 'team', code: 'TEA', name_fr: 'Mon Équipe', name_en: 'My Team', icon: '🤝', order: 8 },
        { id: 'scholar', code: 'SCH', name_fr: 'Académique', name_en: 'Scholar', icon: '📚', order: 9 },
      ],
    }).as('getSpheres')

    cy.intercept('GET', '**/bureau/sections', {
      statusCode: 200,
      body: [
        { id: 'quick_capture', key: 'quick_capture', name_fr: 'Capture Rapide', name_en: 'Quick Capture', order: 1 },
        { id: 'resume_workspace', key: 'resume_workspace', name_fr: 'Reprendre', name_en: 'Resume Workspace', order: 2 },
        { id: 'threads', key: 'threads', name_fr: 'Threads', name_en: 'Threads', order: 3 },
        { id: 'data_files', key: 'data_files', name_fr: 'Données & Fichiers', name_en: 'Data & Files', order: 4 },
        { id: 'active_agents', key: 'active_agents', name_fr: 'Agents Actifs', name_en: 'Active Agents', order: 5 },
        { id: 'meetings', key: 'meetings', name_fr: 'Réunions', name_en: 'Meetings', order: 6 },
      ],
    }).as('getBureauSections')

    cy.intercept('GET', '**/nova/status', {
      statusCode: 200,
      body: {
        status: 'active',
        level: 'L0',
        description: 'Nova is active and monitoring',
      },
    })

    // Set authenticated state
    cy.window().then((win) => {
      win.localStorage.setItem('chenu-auth', JSON.stringify({
        state: {
          user: {
            id: 'test-id',
            email: 'test@example.com',
            display_name: 'Test User',
          },
          isAuthenticated: true,
        },
        version: 0,
      }))
    })
  })

  describe('Dashboard', () => {
    it('should display all 9 spheres', () => {
      cy.visit('/')
      cy.wait('@getSpheres')
      
      // Check all 9 spheres are displayed
      cy.contains('Personnel').should('be.visible')
      cy.contains('Affaires').should('be.visible')
      cy.contains('Gouvernement').should('be.visible')
      cy.contains('Studio Créatif').should('be.visible')
      cy.contains('Communauté').should('be.visible')
      cy.contains('Social & Médias').should('be.visible')
      cy.contains('Divertissement').should('be.visible')
      cy.contains('Mon Équipe').should('be.visible')
      cy.contains('Académique').should('be.visible')
    })

    it('should display Nova status', () => {
      cy.visit('/')
      
      cy.contains('Nova').should('be.visible')
      cy.contains('L0').should('be.visible')
    })

    it('should display governance info', () => {
      cy.visit('/')
      
      cy.contains('Gouvernance Active').should('be.visible')
    })
  })

  describe('Sphere Navigation', () => {
    it('should navigate to sphere page', () => {
      cy.visit('/')
      cy.wait('@getSpheres')
      
      cy.contains('Personnel').click()
      cy.url().should('include', '/sphere/personal')
      cy.get('h1').should('contain', 'Personnel')
    })

    it('should display 6 bureau sections in sphere', () => {
      cy.visit('/sphere/personal')
      cy.wait('@getBureauSections')
      
      cy.contains('Capture Rapide').should('be.visible')
      cy.contains('Reprendre').should('be.visible')
      cy.contains('Threads').should('be.visible')
      cy.contains('Données & Fichiers').should('be.visible')
      cy.contains('Agents Actifs').should('be.visible')
      cy.contains('Réunions').should('be.visible')
    })

    it('should navigate between spheres via sidebar', () => {
      cy.visit('/sphere/personal')
      cy.wait('@getSpheres')
      
      // Click on Business sphere in sidebar
      cy.get('nav').contains('Affaires').click()
      cy.url().should('include', '/sphere/business')
      cy.get('h1').should('contain', 'Affaires')
    })

    it('should return to dashboard via home link', () => {
      cy.visit('/sphere/personal')
      
      cy.contains('Accueil').click()
      cy.url().should('eq', Cypress.config().baseUrl + '/')
    })
  })

  describe('Bureau Sections', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads*', {
        statusCode: 200,
        body: [],
      })
    })

    it('should select bureau section', () => {
      cy.visit('/sphere/personal')
      cy.wait('@getBureauSections')
      
      cy.contains('Threads').click()
      cy.url().should('include', '/sphere/personal/threads')
    })

    it('should show empty state for threads', () => {
      cy.visit('/sphere/personal/threads')
      
      cy.contains('Aucun thread').should('be.visible')
    })

    it('should show quick capture input', () => {
      cy.visit('/sphere/personal/quick_capture')
      
      cy.get('input[placeholder*="idée"]').should('be.visible')
    })

    it('should show empty state for agents', () => {
      cy.visit('/sphere/personal/active_agents')
      
      cy.contains('Aucun agent actif').should('be.visible')
    })
  })

  describe('Settings Navigation', () => {
    it('should navigate to settings', () => {
      cy.visit('/')
      
      cy.contains('Paramètres').click()
      cy.url().should('include', '/settings')
      cy.get('h1').should('contain', 'Paramètres')
    })

    it('should display settings tabs', () => {
      cy.visit('/settings')
      
      cy.contains('Profil').should('be.visible')
      cy.contains('Apparence').should('be.visible')
      cy.contains('Langue').should('be.visible')
      cy.contains('Notifications').should('be.visible')
      cy.contains('Sécurité').should('be.visible')
    })

    it('should switch between settings tabs', () => {
      cy.visit('/settings')
      
      cy.contains('Apparence').click()
      cy.contains('Thème').should('be.visible')
      
      cy.contains('Langue').click()
      cy.contains('Français').should('be.visible')
      cy.contains('English').should('be.visible')
    })
  })

  describe('Responsive Navigation', () => {
    it('should show mobile menu button on small screens', () => {
      cy.viewport(375, 667) // iPhone size
      cy.visit('/')
      
      // Should see menu button
      cy.get('button').find('svg').should('be.visible')
    })

    it('should open mobile navigation drawer', () => {
      cy.viewport(375, 667)
      cy.visit('/')
      
      // Click menu button
      cy.get('header button').last().click()
      
      // Should see spheres in drawer
      cy.contains('Personnel').should('be.visible')
    })
  })

  describe('Logout', () => {
    it('should logout and redirect to login', () => {
      cy.intercept('POST', '**/auth/logout', {
        statusCode: 200,
        body: { success: true },
      })

      cy.visit('/')
      
      cy.contains('Déconnexion').click()
      cy.url().should('include', '/login')
    })
  })
})
