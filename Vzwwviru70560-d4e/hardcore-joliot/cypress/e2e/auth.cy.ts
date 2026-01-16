/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ — AUTH E2E TESTS                                  ║
 * ║                    Task B0.4: Setup Cypress                                   ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

describe('Authentication Flow', () => {
  beforeEach(() => {
    // Clear any existing session
    cy.clearLocalStorage()
    cy.clearCookies()
  })

  describe('Login Page', () => {
    it('should display login form', () => {
      cy.visit('/login')
      
      cy.get('h2').should('contain', 'Connexion')
      cy.get('input[type="email"]').should('be.visible')
      cy.get('input[type="password"]').should('be.visible')
      cy.get('button[type="submit"]').should('contain', 'Se connecter')
    })

    it('should have link to register page', () => {
      cy.visit('/login')
      
      cy.contains('Créer un compte').should('have.attr', 'href', '/register')
    })

    it('should show error for empty email', () => {
      cy.visit('/login')
      
      cy.get('button[type="submit"]').click()
      cy.contains("L'email est requis").should('be.visible')
    })

    it('should show error for empty password', () => {
      cy.visit('/login')
      
      cy.get('input[type="email"]').type('test@example.com')
      cy.get('button[type="submit"]').click()
      cy.contains('Le mot de passe est requis').should('be.visible')
    })

    it('should toggle password visibility', () => {
      cy.visit('/login')
      
      cy.get('input[type="password"]').as('passwordInput')
      cy.get('@passwordInput').should('have.attr', 'type', 'password')
      
      // Click the toggle button (find by svg icon)
      cy.get('@passwordInput').parent().find('button').click()
      cy.get('@passwordInput').should('have.attr', 'type', 'text')
      
      // Toggle back
      cy.get('@passwordInput').parent().find('button').click()
      cy.get('@passwordInput').should('have.attr', 'type', 'password')
    })

    it('should redirect to home after successful login', () => {
      // Mock successful login API
      cy.intercept('POST', '**/auth/login', {
        statusCode: 200,
        body: {
          user: {
            id: 'test-id',
            email: 'test@example.com',
            display_name: 'Test User',
          },
          tokens: {
            access_token: 'mock-token',
            refresh_token: 'mock-refresh',
            expires_in: 3600,
          },
        },
      }).as('loginRequest')

      cy.visit('/login')
      cy.get('input[type="email"]').type('test@example.com')
      cy.get('input[type="password"]').type('password123')
      cy.get('button[type="submit"]').click()

      cy.wait('@loginRequest')
      cy.url().should('eq', Cypress.config().baseUrl + '/')
    })

    it('should show error for invalid credentials', () => {
      cy.intercept('POST', '**/auth/login', {
        statusCode: 401,
        body: {
          detail: 'Invalid credentials',
        },
      }).as('loginRequest')

      cy.visit('/login')
      cy.get('input[type="email"]').type('test@example.com')
      cy.get('input[type="password"]').type('wrongpassword')
      cy.get('button[type="submit"]').click()

      cy.wait('@loginRequest')
      cy.get('[class*="red"]').should('be.visible')
    })
  })

  describe('Register Page', () => {
    it('should display register form', () => {
      cy.visit('/register')
      
      cy.get('h2').should('contain', 'Créer un compte')
      cy.get('input[type="email"]').should('be.visible')
      cy.get('input[type="password"]').should('have.length', 2) // password + confirm
      cy.get('button[type="submit"]').should('contain', 'Créer mon compte')
    })

    it('should have link to login page', () => {
      cy.visit('/register')
      
      cy.contains('Se connecter').should('have.attr', 'href', '/login')
    })

    it('should show password strength indicator', () => {
      cy.visit('/register')
      
      // Type a weak password
      cy.get('input#password').type('abc')
      
      // Should show strength indicators
      cy.contains('8+ caractères').should('be.visible')
      cy.contains('Majuscule').should('be.visible')
      cy.contains('Minuscule').should('be.visible')
      cy.contains('Chiffre').should('be.visible')
    })

    it('should show password mismatch error', () => {
      cy.visit('/register')
      
      cy.get('input#password').type('Password123')
      cy.get('input#confirmPassword').type('DifferentPassword')
      
      cy.contains('ne correspondent pas').should('be.visible')
    })

    it('should require terms acceptance', () => {
      cy.visit('/register')
      
      cy.get('input[type="email"]').type('new@example.com')
      cy.get('input#password').type('Password123')
      cy.get('input#confirmPassword').type('Password123')
      cy.get('button[type="submit"]').click()
      
      cy.contains('conditions').should('be.visible')
    })
  })

  describe('Protected Routes', () => {
    it('should redirect to login when not authenticated', () => {
      cy.visit('/')
      cy.url().should('include', '/login')
    })

    it('should redirect to login for sphere routes', () => {
      cy.visit('/sphere/personal')
      cy.url().should('include', '/login')
    })

    it('should redirect to login for settings', () => {
      cy.visit('/settings')
      cy.url().should('include', '/login')
    })
  })

  describe('Navigation after Auth', () => {
    beforeEach(() => {
      // Setup authenticated state
      cy.intercept('GET', '**/users/me', {
        statusCode: 200,
        body: {
          id: 'test-id',
          email: 'test@example.com',
          display_name: 'Test User',
        },
      }).as('getCurrentUser')

      // Set auth token in localStorage
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

    it('should show dashboard when authenticated', () => {
      cy.visit('/')
      cy.contains('Bienvenue').should('be.visible')
    })

    it('should redirect logged-in user from login to home', () => {
      cy.visit('/login')
      cy.url().should('eq', Cypress.config().baseUrl + '/')
    })
  })
})
