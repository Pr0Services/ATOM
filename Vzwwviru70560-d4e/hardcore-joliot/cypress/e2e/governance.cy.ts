/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                                                                              ║
 * ║              CHE·NU™ — E2E GOVERNANCE TESTS                                  ║
 * ║                                                                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

describe('Governance System', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.login('test@chenu.io', 'testpassword');
  });

  describe('Governance Dashboard', () => {
    it('should display governance overview', () => {
      cy.visit('/governance');
      
      cy.get('[data-testid="governance-header"]').should('contain.text', 'Gouvernance');
      cy.get('[data-testid="constitution-badge"]').should('be.visible');
    });

    it('should show Constitution status', () => {
      cy.visit('/governance');
      
      cy.get('[data-testid="constitution-status"]')
        .should('contain.text', 'Active')
        .and('contain.text', 'v1.0');
    });

    it('should display the three laws', () => {
      cy.visit('/governance');
      
      cy.get('[data-testid="law-item"]').should('have.length', 3);
      
      // Law #1
      cy.get('[data-testid="law-1"]').should('contain.text', 'Silent Budget');
      
      // Law #2
      cy.get('[data-testid="law-2"]').should('contain.text', 'Analysis First');
      
      // Law #3
      cy.get('[data-testid="law-3"]').should('contain.text', 'Depth is Intellectual');
    });

    it('should show checkpoint statistics', () => {
      cy.visit('/governance');
      
      cy.get('[data-testid="checkpoint-stats"]').should('exist');
      cy.get('[data-testid="stat-approved"]').should('exist');
      cy.get('[data-testid="stat-rejected"]').should('exist');
    });
  });

  describe('Checkpoint System', () => {
    it('should display checkpoint modal when triggered', () => {
      cy.visit('/nova');
      
      // Trigger checkpoint via deepen
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      
      // Modal should appear
      cy.get('[data-testid="checkpoint-modal"]').should('be.visible');
      cy.get('[data-testid="checkpoint-message"]').should('exist');
      cy.get('[data-testid="checkpoint-approve"]').should('exist');
      cy.get('[data-testid="checkpoint-reject"]').should('exist');
    });

    it('should approve checkpoint', () => {
      cy.visit('/nova');
      
      // Get to checkpoint
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      cy.get('[data-testid="checkpoint-modal"]').should('be.visible');
      
      // Approve
      cy.get('[data-testid="checkpoint-approve"]').click();
      
      // Modal should close
      cy.get('[data-testid="checkpoint-modal"]').should('not.exist');
      
      // Deeper analysis should proceed
      cy.get('[data-testid="nova-processing"]').should('exist');
    });

    it('should reject checkpoint', () => {
      cy.visit('/nova');
      
      // Get to checkpoint
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      cy.get('[data-testid="checkpoint-modal"]').should('be.visible');
      
      // Reject
      cy.get('[data-testid="checkpoint-reject"]').click();
      
      // Modal should close
      cy.get('[data-testid="checkpoint-modal"]').should('not.exist');
      
      // Should stay at current level
      cy.get('[data-testid="nova-processing"]').should('not.exist');
    });

    it('should show checkpoint in history after resolution', () => {
      cy.visit('/nova');
      
      // Process a checkpoint
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      cy.get('[data-testid="checkpoint-approve"]').click();
      
      // Go to governance
      cy.visit('/governance');
      
      // Should see in history
      cy.get('[data-testid="checkpoint-history"]').should('exist');
      cy.get('[data-testid="history-item"]').should('have.length.at.least', 1);
    });
  });

  describe('Depth Suggestions', () => {
    it('should display depth suggestion after analysis', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]').type('Analyze sales data{enter}');
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
      
      cy.get('[data-testid="depth-suggestion"]').should('be.visible');
    });

    it('should show examples in depth suggestion', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      
      cy.get('[data-testid="depth-examples"]').should('exist');
    });

    it('should dismiss depth suggestion', () => {
      cy.visit('/nova');
      
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      
      cy.get('[data-testid="dismiss-depth"]').click();
      
      cy.get('[data-testid="depth-suggestion"]').should('not.exist');
    });
  });

  describe('Constitution Axiom', () => {
    it('should display the axiom', () => {
      cy.visit('/governance');
      
      cy.get('[data-testid="constitution-axiom"]')
        .should('contain.text', 'GOVERNANCE IS SILENT BY DEFAULT');
    });
  });

  describe('Accessibility', () => {
    it('should navigate checkpoint modal with keyboard', () => {
      cy.visit('/nova');
      
      // Get to checkpoint
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      cy.get('[data-testid="checkpoint-modal"]').should('be.visible');
      
      // Tab to buttons
      cy.get('[data-testid="checkpoint-approve"]').focus();
      cy.focused().should('have.attr', 'data-testid', 'checkpoint-approve');
      
      // Tab to reject
      cy.focused().tab();
      cy.focused().should('have.attr', 'data-testid', 'checkpoint-reject');
      
      // Enter to activate
      cy.focused().type('{enter}');
      cy.get('[data-testid="checkpoint-modal"]').should('not.exist');
    });

    it('should close modal with Escape', () => {
      cy.visit('/nova');
      
      // Get to checkpoint
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      cy.get('[data-testid="checkpoint-modal"]').should('be.visible');
      
      // Press Escape
      cy.get('body').type('{esc}');
      
      // Modal should close (rejected)
      cy.get('[data-testid="checkpoint-modal"]').should('not.exist');
    });
  });
});
