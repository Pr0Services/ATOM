/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                                                                              ║
 * ║              CHE·NU™ — E2E NOVA TESTS                                        ║
 * ║                                                                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

describe('Nova System Intelligence', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.login('test@chenu.io', 'testpassword');
  });

  describe('Chat Interface', () => {
    it('should display Nova chat panel', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-header"]').should('contain.text', 'Nova');
      cy.get('[data-testid="nova-status"]').should('exist');
      cy.get('[data-testid="nova-input"]').should('be.visible');
    });

    it('should send and receive messages', () => {
      cy.visit('/nova');
      
      const message = 'Hello Nova!';
      cy.get('[data-testid="nova-input"]').type(`${message}{enter}`);
      
      // User message should appear
      cy.get('[data-testid="user-message"]').should('contain.text', message);
      
      // Nova response should appear
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
    });

    it('should show processing indicator while waiting', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      
      // Processing should show
      cy.get('[data-testid="nova-processing"]').should('be.visible');
      
      // Then response appears
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
    });

    it('should display suggestions after response', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]').type('Help me with project planning{enter}');
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
      
      // Suggestions should be clickable
      cy.get('[data-testid="suggestion-chip"]').should('exist');
    });

    it('should handle empty input gracefully', () => {
      cy.visit('/nova');
      
      // Try to send empty message
      cy.get('[data-testid="send-button"]').should('be.disabled');
      
      // Type then clear
      cy.get('[data-testid="nova-input"]').type('test').clear();
      cy.get('[data-testid="send-button"]').should('be.disabled');
    });
  });

  describe('Analysis Mode', () => {
    it('should perform data analysis', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]').type('Analyze the following: [1, 2, 3, 4, 5]{enter}');
      
      cy.get('[data-testid="analysis-result"]', { timeout: 15000 }).should('exist');
      cy.get('[data-testid="analysis-insights"]').should('exist');
    });

    it('should offer depth suggestions after analysis', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]').type('Analyze trends{enter}');
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
      
      // Depth suggestion should appear (LAW #3 compliant)
      cy.get('[data-testid="depth-suggestion"]').should('exist');
      cy.get('[data-testid="depth-suggestion"]')
        .should('not.contain.text', 'token')
        .and('not.contain.text', 'cost');
    });
  });

  describe('Conversation History', () => {
    it('should maintain message history', () => {
      cy.visit('/nova');
      
      // Send multiple messages
      cy.get('[data-testid="nova-input"]').type('First message{enter}');
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
      
      cy.get('[data-testid="nova-input"]').type('Second message{enter}');
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('have.length.at.least', 2);
      
      // Both messages should be visible
      cy.get('[data-testid="user-message"]').should('have.length', 2);
    });

    it('should allow clearing conversation', () => {
      cy.visit('/nova');
      
      // Send a message
      cy.get('[data-testid="nova-input"]').type('Test{enter}');
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
      
      // Clear
      cy.get('[data-testid="clear-chat-button"]').click();
      cy.get('[data-testid="confirm-clear"]').click();
      
      // Messages should be gone
      cy.get('[data-testid="user-message"]').should('not.exist');
    });
  });

  describe('Nova Status', () => {
    it('should show online status', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-status"]').should('contain.text', 'En ligne');
      cy.get('[data-testid="status-indicator"]').should('have.class', 'online');
    });

    it('should handle offline gracefully', () => {
      // Simulate offline
      cy.intercept('GET', '/api/v1/nova/status', {
        statusCode: 503,
        body: { online: false },
      });

      cy.visit('/nova');
      
      cy.get('[data-testid="nova-status"]').should('contain.text', 'Hors ligne');
    });
  });

  describe('Keyboard Navigation', () => {
    it('should submit on Enter', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]').type('Test{enter}');
      cy.get('[data-testid="user-message"]').should('contain.text', 'Test');
    });

    it('should allow multiline with Shift+Enter', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]')
        .type('Line 1{shift+enter}Line 2');
      
      cy.get('[data-testid="nova-input"]').should('contain.value', 'Line 1\nLine 2');
    });
  });
});
