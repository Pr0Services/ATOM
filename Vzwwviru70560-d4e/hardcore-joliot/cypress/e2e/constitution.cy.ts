/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                                                                              ║
 * ║              CHE·NU™ — E2E CONSTITUTION COMPLIANCE TESTS                     ║
 * ║                                                                              ║
 * ║              Cypress tests for LAW #1, #2, #3                                ║
 * ║                                                                              ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

describe('Constitution Compliance E2E', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.login('test@chenu.io', 'testpassword');
  });

  // ════════════════════════════════════════════════════════════════════════════
  // LAW #1 — SILENT BUDGET MANAGEMENT
  // ════════════════════════════════════════════════════════════════════════════

  describe('LAW #1 — Silent Budget Management', () => {
    const FORBIDDEN_TERMS = ['$', '€', 'token', 'cost', 'budget', 'prix', 'coût', '%'];

    it('should never display cost information in Nova responses', () => {
      cy.visit('/nova');
      
      // Send a query
      cy.get('[data-testid="nova-input"]').type('Analyze my data{enter}');
      
      // Wait for response
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
      
      // Check response doesn't contain forbidden terms
      cy.get('[data-testid="nova-response"]').then(($el) => {
        const text = $el.text().toLowerCase();
        FORBIDDEN_TERMS.forEach((term) => {
          expect(text).not.to.include(term.toLowerCase());
        });
      });
    });

    it('should never display budget in governance dashboard', () => {
      cy.visit('/governance');
      
      // Check entire page
      cy.get('body').then(($body) => {
        const text = $body.text().toLowerCase();
        FORBIDDEN_TERMS.forEach((term) => {
          expect(text).not.to.include(term.toLowerCase());
        });
      });
    });

    it('should sanitize API responses with forbidden fields', () => {
      cy.intercept('POST', '/api/v1/nova/query', (req) => {
        req.continue((res) => {
          // Verify response doesn't have forbidden fields
          expect(res.body).not.to.have.property('tokensUsed');
          expect(res.body).not.to.have.property('cost');
          expect(res.body).not.to.have.property('budgetRemaining');
        });
      });

      cy.visit('/nova');
      cy.get('[data-testid="nova-input"]').type('Test query{enter}');
    });

    it('should not show token counts anywhere in the UI', () => {
      // Check various pages
      const pages = ['/dashboard', '/nova', '/governance', '/agents'];
      
      pages.forEach((page) => {
        cy.visit(page);
        cy.get('body').should('not.contain.text', 'token');
        cy.get('body').should('not.contain.text', 'Token');
      });
    });
  });

  // ════════════════════════════════════════════════════════════════════════════
  // LAW #2 — ANALYSIS FIRST, GOVERNANCE LATER
  // ════════════════════════════════════════════════════════════════════════════

  describe('LAW #2 — Analysis First, Governance Later', () => {
    it('should complete analysis without interruption', () => {
      cy.visit('/nova');
      
      // Send analysis request
      cy.get('[data-testid="nova-input"]').type('Analyze sales trends{enter}');
      
      // Should show processing indicator
      cy.get('[data-testid="nova-processing"]').should('exist');
      
      // Should NOT show checkpoint during analysis
      cy.get('[data-testid="checkpoint-modal"]').should('not.exist');
      
      // Wait for analysis to complete
      cy.get('[data-testid="nova-response"]', { timeout: 15000 }).should('exist');
      
      // Analysis should be complete
      cy.get('[data-testid="analysis-result"]').should('exist');
    });

    it('should only show checkpoint after requesting deepen', () => {
      cy.visit('/nova');
      
      // Complete initial analysis
      cy.get('[data-testid="nova-input"]').type('Analyze data{enter}');
      cy.get('[data-testid="nova-response"]', { timeout: 10000 }).should('exist');
      
      // Check for depth suggestion
      cy.get('[data-testid="depth-suggestion"]').should('exist');
      
      // Click deepen
      cy.get('[data-testid="deepen-button"]').click();
      
      // NOW checkpoint should appear
      cy.get('[data-testid="checkpoint-modal"]').should('be.visible');
    });

    it('should allow rejecting deepen without penalty', () => {
      cy.visit('/nova');
      
      // Complete analysis and trigger deepen
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      
      // Reject at checkpoint
      cy.get('[data-testid="checkpoint-reject"]').click();
      
      // Modal should close
      cy.get('[data-testid="checkpoint-modal"]').should('not.exist');
      
      // Original analysis should still be visible
      cy.get('[data-testid="analysis-result"]').should('exist');
    });
  });

  // ════════════════════════════════════════════════════════════════════════════
  // LAW #3 — DEPTH IS INTELLECTUAL, NOT FINANCIAL
  // ════════════════════════════════════════════════════════════════════════════

  describe('LAW #3 — Depth is Intellectual', () => {
    const APPROVED_PATTERNS = [
      /approfondir/i,
      /insights/i,
      /explorer/i,
      /détail/i,
      /analyse plus/i,
    ];

    const FORBIDDEN_PATTERNS = [
      /\$/,
      /€/,
      /token/i,
      /cost/i,
      /budget/i,
      /\d+%/,
    ];

    it('should use intellectual framing in depth suggestions', () => {
      cy.visit('/nova');
      
      // Trigger depth suggestion
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      
      // Get suggestion text
      cy.get('[data-testid="depth-suggestion"]').then(($el) => {
        const text = $el.text();
        
        // Should contain intellectual terms
        const hasApproved = APPROVED_PATTERNS.some((pattern) => pattern.test(text));
        expect(hasApproved).to.be.true;
        
        // Should NOT contain financial terms
        FORBIDDEN_PATTERNS.forEach((pattern) => {
          expect(text).not.to.match(pattern);
        });
      });
    });

    it('should use intellectual framing in checkpoint messages', () => {
      cy.visit('/nova');
      
      // Get to checkpoint
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      
      // Check checkpoint message
      cy.get('[data-testid="checkpoint-modal"]').should('be.visible');
      cy.get('[data-testid="checkpoint-message"]').then(($el) => {
        const text = $el.text();
        
        // Should NOT contain financial terms
        FORBIDDEN_PATTERNS.forEach((pattern) => {
          expect(text).not.to.match(pattern);
        });
      });
    });

    it('should have approve/reject buttons with intellectual labels', () => {
      cy.visit('/nova');
      
      // Get to checkpoint
      cy.get('[data-testid="nova-input"]').type('Analyze{enter}');
      cy.get('[data-testid="depth-suggestion"]', { timeout: 10000 }).should('exist');
      cy.get('[data-testid="deepen-button"]').click();
      
      // Check button labels
      cy.get('[data-testid="checkpoint-approve"]')
        .should('contain.text', 'Approfondir')
        .and('not.contain.text', 'cost')
        .and('not.contain.text', 'token');
      
      cy.get('[data-testid="checkpoint-reject"]')
        .should('not.contain.text', 'cost')
        .and('not.contain.text', 'token');
    });
  });

  // ════════════════════════════════════════════════════════════════════════════
  // INTEGRATION TESTS
  // ════════════════════════════════════════════════════════════════════════════

  describe('Constitution Integration', () => {
    it('should maintain compliance through full analysis workflow', () => {
      cy.visit('/nova');
      
      // Step 1: Initial query
      cy.get('[data-testid="nova-input"]').type('Full analysis of Q4 data{enter}');
      
      // Step 2: Wait for response (no interruption - LAW #2)
      cy.get('[data-testid="checkpoint-modal"]').should('not.exist');
      cy.get('[data-testid="nova-response"]', { timeout: 15000 }).should('exist');
      
      // Step 3: Check response for forbidden content (LAW #1)
      cy.get('[data-testid="nova-response"]').then(($el) => {
        const text = $el.text().toLowerCase();
        expect(text).not.to.include('token');
        expect(text).not.to.include('cost');
        expect(text).not.to.include('budget');
      });
      
      // Step 4: Check depth suggestion framing (LAW #3)
      cy.get('[data-testid="depth-suggestion"]').should('exist');
      cy.get('[data-testid="depth-suggestion"]').then(($el) => {
        const text = $el.text().toLowerCase();
        expect(text).not.to.include('$');
        expect(text).not.to.include('token');
      });
      
      // Step 5: Request deepen (checkpoint appears - LAW #2)
      cy.get('[data-testid="deepen-button"]').click();
      cy.get('[data-testid="checkpoint-modal"]').should('be.visible');
      
      // Step 6: Check checkpoint message (LAW #3)
      cy.get('[data-testid="checkpoint-message"]').then(($el) => {
        const text = $el.text().toLowerCase();
        expect(text).not.to.include('cost');
        expect(text).not.to.include('token');
      });
      
      // Step 7: Approve and verify continued compliance
      cy.get('[data-testid="checkpoint-approve"]').click();
      cy.get('[data-testid="checkpoint-modal"]').should('not.exist');
    });

    it('should never expose budget even in error states', () => {
      // Intercept to force error
      cy.intercept('POST', '/api/v1/nova/query', {
        statusCode: 500,
        body: { error: 'Server error' },
      });

      cy.visit('/nova');
      cy.get('[data-testid="nova-input"]').type('Test{enter}');
      
      // Error message should not mention budget
      cy.get('[data-testid="error-message"]', { timeout: 5000 }).then(($el) => {
        const text = $el.text().toLowerCase();
        expect(text).not.to.include('budget');
        expect(text).not.to.include('token');
        expect(text).not.to.include('cost');
      });
    });
  });
});

// ════════════════════════════════════════════════════════════════════════════
// CUSTOM COMMANDS
// ════════════════════════════════════════════════════════════════════════════

Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-testid="email-input"]').type(email);
    cy.get('[data-testid="password-input"]').type(password);
    cy.get('[data-testid="login-button"]').click();
    cy.url().should('not.include', '/login');
  });
});

Cypress.Commands.add('checkConstitutionCompliance', () => {
  const FORBIDDEN = ['$', '€', 'token', 'cost', 'budget'];
  cy.get('body').then(($body) => {
    const text = $body.text().toLowerCase();
    FORBIDDEN.forEach((term) => {
      expect(text).not.to.include(term);
    });
  });
});

// Type declarations
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      checkConstitutionCompliance(): Chainable<void>;
    }
  }
}
