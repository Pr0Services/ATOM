/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ — GOVERNANCE E2E TESTS                            ║
 * ║                    Sprint B1.6: Checkpoints & Approvals                      ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 * 
 * Tests the 7 R&D Rules:
 * - Rule #1: Human Sovereignty
 * - Rule #2: Autonomy Isolation
 * - Rule #3: Sphere Integrity
 * - Rule #4: My Team Restrictions
 * - Rule #5: Social Restrictions
 * - Rule #6: Module Traceability
 * - Rule #7: R&D Continuity
 */

describe('Governance & Checkpoints', () => {
  beforeEach(() => {
    cy.loginWithMock()
    cy.mockSpheres()
    cy.mockBureauSections()

    cy.intercept('GET', '**/governance/status', {
      statusCode: 200,
      body: {
        active: true,
        rules_enforced: 7,
        pending_checkpoints: 3,
        last_audit: '2026-01-02T10:00:00Z',
      },
    }).as('getGovernanceStatus')
  })

  describe('Governance Dashboard', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/governance/checkpoints*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'cp-1',
              type: 'agent_action',
              agent_id: 'agent-1',
              agent_name: 'Content Writer',
              action: 'send_email',
              description: 'Envoyer email marketing',
              status: 'pending',
              created_at: '2026-01-03T09:00:00Z',
              requires_approval: true,
              risk_level: 'medium',
            },
            {
              id: 'cp-2',
              type: 'data_transfer',
              from_sphere: 'business',
              to_sphere: 'personal',
              description: 'Transférer rapport vers Personal',
              status: 'pending',
              created_at: '2026-01-03T08:30:00Z',
              requires_approval: true,
              risk_level: 'low',
            },
            {
              id: 'cp-3',
              type: 'token_budget',
              agent_id: 'agent-2',
              agent_name: 'Data Analyst',
              description: 'Dépassement budget tokens',
              status: 'pending',
              created_at: '2026-01-03T08:00:00Z',
              requires_approval: true,
              risk_level: 'high',
              token_amount: 5000,
            },
          ],
          total: 3,
        },
      }).as('getCheckpoints')

      cy.intercept('GET', '**/governance/audit-log*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'audit-1',
              type: 'checkpoint_approved',
              description: 'Checkpoint CP-001 approuvé',
              user_id: 'user-1',
              user_name: 'Test User',
              created_at: '2026-01-02T15:00:00Z',
            },
            {
              id: 'audit-2',
              type: 'agent_hired',
              description: 'Agent Content Writer engagé',
              user_id: 'user-1',
              user_name: 'Test User',
              created_at: '2026-01-02T10:00:00Z',
            },
          ],
          total: 2,
        },
      }).as('getAuditLog')
    })

    it('should display governance dashboard', () => {
      cy.visit('/governance')
      cy.wait('@getGovernanceStatus')

      cy.contains('Tableau de Gouvernance').should('be.visible')
      cy.contains('7 règles actives').should('be.visible')
    })

    it('should show pending checkpoints count', () => {
      cy.visit('/governance')
      cy.wait('@getCheckpoints')

      cy.getByTestId('pending-checkpoints-badge')
        .should('contain', '3')
    })

    it('should display checkpoint list', () => {
      cy.visit('/governance')
      cy.wait('@getCheckpoints')

      cy.contains('Envoyer email marketing').should('be.visible')
      cy.contains('Transférer rapport').should('be.visible')
      cy.contains('Dépassement budget').should('be.visible')
    })

    it('should show risk levels', () => {
      cy.visit('/governance')
      cy.wait('@getCheckpoints')

      cy.getByTestId('risk-badge-medium').should('be.visible')
      cy.getByTestId('risk-badge-low').should('be.visible')
      cy.getByTestId('risk-badge-high').should('be.visible')
    })

    it('should display audit log', () => {
      cy.visit('/governance')
      cy.wait('@getAuditLog')

      cy.getByTestId('audit-log-tab').click()

      cy.contains('Checkpoint CP-001 approuvé').should('be.visible')
      cy.contains('Agent Content Writer engagé').should('be.visible')
    })

    it('should filter checkpoints by type', () => {
      cy.visit('/governance')
      cy.wait('@getCheckpoints')

      cy.getByTestId('checkpoint-filter').click()
      cy.contains('Actions Agent').click()

      cy.contains('Envoyer email marketing').should('be.visible')
      cy.contains('Transférer rapport').should('not.exist')
    })

    it('should filter checkpoints by status', () => {
      cy.visit('/governance')
      cy.wait('@getCheckpoints')

      cy.getByTestId('status-filter').click()
      cy.contains('En attente').click()

      cy.getByTestId('checkpoint-item').should('have.length', 3)
    })
  })

  describe('Checkpoint Approval (Rule #1: Human Sovereignty)', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/governance/checkpoints/cp-1', {
        statusCode: 200,
        body: {
          id: 'cp-1',
          type: 'agent_action',
          agent_id: 'agent-1',
          agent_name: 'Content Writer',
          action: 'send_email',
          description: 'Envoyer email marketing à 500 contacts',
          status: 'pending',
          requires_approval: true,
          risk_level: 'medium',
          details: {
            recipients_count: 500,
            subject: 'Newsletter Janvier',
            preview: 'Bonjour, voici notre newsletter...',
          },
          created_at: '2026-01-03T09:00:00Z',
        },
      }).as('getCheckpoint')
    })

    it('should display checkpoint details', () => {
      cy.visit('/governance/checkpoints/cp-1')
      cy.wait('@getCheckpoint')

      cy.contains('Envoyer email marketing').should('be.visible')
      cy.contains('500 contacts').should('be.visible')
      cy.contains('Content Writer').should('be.visible')
    })

    it('should show email preview', () => {
      cy.visit('/governance/checkpoints/cp-1')
      cy.wait('@getCheckpoint')

      cy.getByTestId('preview-toggle').click()
      cy.contains('Newsletter Janvier').should('be.visible')
      cy.contains('Bonjour, voici notre newsletter').should('be.visible')
    })

    it('should approve checkpoint', () => {
      cy.intercept('POST', '**/governance/checkpoints/cp-1/approve', {
        statusCode: 200,
        body: {
          id: 'cp-1',
          status: 'approved',
          approved_by: 'user-1',
          approved_at: '2026-01-03T10:00:00Z',
        },
      }).as('approveCheckpoint')

      cy.visit('/governance/checkpoints/cp-1')
      cy.wait('@getCheckpoint')

      cy.getByTestId('approve-button').click()
      cy.getByTestId('confirm-approval').click()

      cy.wait('@approveCheckpoint')
      cy.contains('Checkpoint approuvé').should('be.visible')
    })

    it('should reject checkpoint with reason', () => {
      cy.intercept('POST', '**/governance/checkpoints/cp-1/reject', {
        statusCode: 200,
        body: {
          id: 'cp-1',
          status: 'rejected',
          rejected_by: 'user-1',
          rejection_reason: 'Contenu non validé',
        },
      }).as('rejectCheckpoint')

      cy.visit('/governance/checkpoints/cp-1')
      cy.wait('@getCheckpoint')

      cy.getByTestId('reject-button').click()
      cy.getByTestId('rejection-reason').type('Contenu non validé')
      cy.getByTestId('confirm-rejection').click()

      cy.wait('@rejectCheckpoint')
      cy.contains('Checkpoint rejeté').should('be.visible')
    })

    it('should require rejection reason', () => {
      cy.visit('/governance/checkpoints/cp-1')
      cy.wait('@getCheckpoint')

      cy.getByTestId('reject-button').click()
      cy.getByTestId('confirm-rejection').should('be.disabled')

      cy.getByTestId('rejection-reason').type('Raison')
      cy.getByTestId('confirm-rejection').should('not.be.disabled')
    })

    it('should show approval in audit log', () => {
      cy.intercept('POST', '**/governance/checkpoints/cp-1/approve', {
        statusCode: 200,
        body: { status: 'approved' },
      }).as('approve')

      cy.intercept('GET', '**/governance/audit-log*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'audit-new',
              type: 'checkpoint_approved',
              description: 'Email marketing approuvé',
              user_id: 'user-1',
              user_name: 'Test User',
              created_at: '2026-01-03T10:00:00Z',
            },
          ],
          total: 1,
        },
      }).as('getNewAuditLog')

      cy.visit('/governance/checkpoints/cp-1')
      cy.wait('@getCheckpoint')

      cy.getByTestId('approve-button').click()
      cy.getByTestId('confirm-approval').click()

      cy.wait('@approve')

      cy.visit('/governance')
      cy.getByTestId('audit-log-tab').click()
      cy.wait('@getNewAuditLog')

      cy.contains('Email marketing approuvé').should('be.visible')
    })
  })

  describe('Cross-Sphere Transfer (Rule #3: Sphere Integrity)', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/governance/checkpoints/cp-2', {
        statusCode: 200,
        body: {
          id: 'cp-2',
          type: 'data_transfer',
          from_sphere: 'business',
          from_sphere_name: 'Affaires',
          to_sphere: 'personal',
          to_sphere_name: 'Personnel',
          description: 'Transférer rapport financier vers Personal',
          status: 'pending',
          requires_approval: true,
          risk_level: 'low',
          data: {
            file_name: 'rapport_q4.pdf',
            file_size: '2.5 MB',
            data_type: 'document',
          },
          created_at: '2026-01-03T08:30:00Z',
        },
      }).as('getTransferCheckpoint')
    })

    it('should display transfer details', () => {
      cy.visit('/governance/checkpoints/cp-2')
      cy.wait('@getTransferCheckpoint')

      cy.contains('Affaires').should('be.visible')
      cy.contains('Personnel').should('be.visible')
      cy.contains('rapport_q4.pdf').should('be.visible')
    })

    it('should show sphere icons', () => {
      cy.visit('/governance/checkpoints/cp-2')
      cy.wait('@getTransferCheckpoint')

      cy.getByTestId('from-sphere-icon').should('contain', '💼')
      cy.getByTestId('to-sphere-icon').should('contain', '👤')
    })

    it('should show transfer direction arrow', () => {
      cy.visit('/governance/checkpoints/cp-2')
      cy.wait('@getTransferCheckpoint')

      cy.getByTestId('transfer-arrow').should('be.visible')
    })

    it('should approve cross-sphere transfer', () => {
      cy.intercept('POST', '**/governance/checkpoints/cp-2/approve', {
        statusCode: 200,
        body: {
          id: 'cp-2',
          status: 'approved',
          transfer_executed: true,
        },
      }).as('approveTransfer')

      cy.visit('/governance/checkpoints/cp-2')
      cy.wait('@getTransferCheckpoint')

      cy.getByTestId('approve-button').click()
      cy.getByTestId('confirm-approval').click()

      cy.wait('@approveTransfer')
      cy.contains('Transfert approuvé').should('be.visible')
    })
  })

  describe('Token Budget Approval (Governance)', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/governance/checkpoints/cp-3', {
        statusCode: 200,
        body: {
          id: 'cp-3',
          type: 'token_budget',
          agent_id: 'agent-2',
          agent_name: 'Data Analyst',
          description: 'Demande de dépassement budget tokens',
          status: 'pending',
          requires_approval: true,
          risk_level: 'high',
          current_budget: 10000,
          requested_amount: 5000,
          new_total: 15000,
          reason: 'Analyse complexe de données volumineuses',
          created_at: '2026-01-03T08:00:00Z',
        },
      }).as('getBudgetCheckpoint')
    })

    it('should display budget request details', () => {
      cy.visit('/governance/checkpoints/cp-3')
      cy.wait('@getBudgetCheckpoint')

      cy.contains('Data Analyst').should('be.visible')
      cy.contains('10,000 tokens').should('be.visible')
      cy.contains('+5,000 tokens').should('be.visible')
      cy.contains('15,000 tokens').should('be.visible')
    })

    it('should show high risk warning', () => {
      cy.visit('/governance/checkpoints/cp-3')
      cy.wait('@getBudgetCheckpoint')

      cy.getByTestId('high-risk-warning').should('be.visible')
      cy.contains('Risque élevé').should('be.visible')
    })

    it('should require confirmation for high-risk approval', () => {
      cy.visit('/governance/checkpoints/cp-3')
      cy.wait('@getBudgetCheckpoint')

      cy.getByTestId('approve-button').click()

      cy.getByTestId('high-risk-confirmation').should('be.visible')
      cy.contains('Êtes-vous sûr').should('be.visible')
      cy.getByTestId('confirm-checkbox').should('not.be.checked')

      cy.getByTestId('confirm-approval').should('be.disabled')

      cy.getByTestId('confirm-checkbox').click()
      cy.getByTestId('confirm-approval').should('not.be.disabled')
    })

    it('should approve with partial amount', () => {
      cy.intercept('POST', '**/governance/checkpoints/cp-3/approve', {
        statusCode: 200,
        body: {
          id: 'cp-3',
          status: 'approved',
          approved_amount: 3000,
        },
      }).as('partialApprove')

      cy.visit('/governance/checkpoints/cp-3')
      cy.wait('@getBudgetCheckpoint')

      cy.getByTestId('partial-approve-toggle').click()
      cy.getByTestId('approved-amount-input').clear().type('3000')
      cy.getByTestId('approve-button').click()
      cy.getByTestId('confirm-checkbox').click()
      cy.getByTestId('confirm-approval').click()

      cy.wait('@partialApprove')
      cy.contains('3,000 tokens approuvés').should('be.visible')
    })
  })

  describe('Token Budget Display', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/users/me/tokens', {
        statusCode: 200,
        body: {
          balance: 45000,
          spent_today: 5000,
          daily_limit: 100000,
          monthly_limit: 500000,
          monthly_spent: 150000,
        },
      }).as('getTokens')

      cy.intercept('GET', '**/governance/token-usage*', {
        statusCode: 200,
        body: {
          by_agent: [
            { agent_name: 'Nova', tokens: 3000 },
            { agent_name: 'Content Writer', tokens: 1500 },
            { agent_name: 'Data Analyst', tokens: 500 },
          ],
          by_sphere: [
            { sphere_name: 'Personal', tokens: 2500 },
            { sphere_name: 'Business', tokens: 2000 },
            { sphere_name: 'Studio', tokens: 500 },
          ],
        },
      }).as('getTokenUsage')
    })

    it('should display token balance in header', () => {
      cy.visit('/')
      cy.wait('@getTokens')

      cy.getByTestId('token-balance').should('contain', '45,000')
    })

    it('should show daily progress', () => {
      cy.visit('/')
      cy.wait('@getTokens')

      cy.getByTestId('token-balance').click()
      cy.getByTestId('daily-progress').should('be.visible')
      cy.contains('5,000 / 100,000').should('be.visible')
    })

    it('should show monthly progress', () => {
      cy.visit('/')
      cy.wait('@getTokens')

      cy.getByTestId('token-balance').click()
      cy.contains('150,000 / 500,000').should('be.visible')
    })

    it('should display usage by agent', () => {
      cy.visit('/governance')
      cy.getByTestId('token-usage-tab').click()
      cy.wait('@getTokenUsage')

      cy.contains('Nova').should('be.visible')
      cy.contains('3,000 tokens').should('be.visible')
    })

    it('should display usage by sphere', () => {
      cy.visit('/governance')
      cy.getByTestId('token-usage-tab').click()
      cy.wait('@getTokenUsage')

      cy.getByTestId('view-by-sphere').click()

      cy.contains('Personal').should('be.visible')
      cy.contains('2,500 tokens').should('be.visible')
    })

    it('should show warning at 80% daily limit', () => {
      cy.intercept('GET', '**/users/me/tokens', {
        statusCode: 200,
        body: {
          balance: 20000,
          spent_today: 85000,
          daily_limit: 100000,
        },
      })

      cy.visit('/')

      cy.getByTestId('token-warning').should('be.visible')
      cy.contains('85% du quota').should('be.visible')
    })

    it('should show critical warning at 95% daily limit', () => {
      cy.intercept('GET', '**/users/me/tokens', {
        statusCode: 200,
        body: {
          balance: 5000,
          spent_today: 98000,
          daily_limit: 100000,
        },
      })

      cy.visit('/')

      cy.getByTestId('token-critical').should('be.visible')
      cy.contains('Limite critique').should('be.visible')
    })
  })

  describe('Agent Level Restrictions (Rule #2: Autonomy Isolation)', () => {
    it('should show L0 agents can only observe', () => {
      cy.intercept('GET', '**/agents/nova', {
        statusCode: 200,
        body: {
          id: 'nova',
          name: 'Nova',
          level: 'L0',
          capabilities: ['observe', 'analyze', 'recommend'],
          restrictions: ['cannot_execute', 'cannot_modify'],
        },
      }).as('getNova')

      cy.visit('/agents/nova')
      cy.wait('@getNova')

      cy.contains('Niveau L0').should('be.visible')
      cy.contains('Observation uniquement').should('be.visible')
    })

    it('should show L1 agents require approval for actions', () => {
      cy.intercept('GET', '**/agents/agent-1', {
        statusCode: 200,
        body: {
          id: 'agent-1',
          name: 'Writer',
          level: 'L1',
          capabilities: ['write', 'edit', 'publish'],
          restrictions: ['requires_approval'],
        },
      }).as('getAgent')

      cy.visit('/agents/agent-1')
      cy.wait('@getAgent')

      cy.contains('Niveau L1').should('be.visible')
      cy.contains('Approbation requise').should('be.visible')
    })

    it('should show L2 agents have bounded autonomy', () => {
      cy.intercept('GET', '**/agents/agent-2', {
        statusCode: 200,
        body: {
          id: 'agent-2',
          name: 'Analyst',
          level: 'L2',
          capabilities: ['analyze', 'report', 'schedule'],
          restrictions: ['token_budget', 'scope_limited'],
        },
      }).as('getAgent')

      cy.visit('/agents/agent-2')
      cy.wait('@getAgent')

      cy.contains('Niveau L2').should('be.visible')
      cy.contains('Autonomie limitée').should('be.visible')
    })

    it('should block L3 agents without human supervision', () => {
      cy.intercept('GET', '**/agents/agent-3', {
        statusCode: 200,
        body: {
          id: 'agent-3',
          name: 'Orchestrator',
          level: 'L3',
          capabilities: ['orchestrate', 'coordinate'],
          restrictions: ['human_supervision_required'],
          status: 'requires_supervision',
        },
      }).as('getAgent')

      cy.visit('/agents/agent-3')
      cy.wait('@getAgent')

      cy.contains('Niveau L3').should('be.visible')
      cy.contains('Supervision humaine requise').should('be.visible')
      cy.getByTestId('activate-button').should('be.disabled')
    })
  })

  describe('My Team Restrictions (Rule #4)', () => {
    it('should prevent agent-to-agent orchestration', () => {
      cy.intercept('POST', '**/agents/agent-1/delegate', {
        statusCode: 403,
        body: {
          detail: 'Agent-to-agent delegation not allowed',
          rule: 'Rule #4: My Team Restrictions',
        },
      }).as('delegateError')

      // Simulate attempting delegation
      cy.visit('/sphere/team/agents')

      // Should show governance notice
      cy.contains('Règle #4').should('be.visible')
      cy.contains('orchestration entre agents').should('be.visible')
    })
  })

  describe('Social Restrictions (Rule #5)', () => {
    it('should show chronological-only in social sphere', () => {
      cy.visit('/sphere/social')

      cy.contains('Ordre chronologique').should('be.visible')
      cy.getByTestId('sort-select').should('not.exist')
    })

    it('should not show engagement metrics', () => {
      cy.visit('/sphere/social')

      cy.getByTestId('engagement-score').should('not.exist')
      cy.getByTestId('ranking-algorithm').should('not.exist')
    })
  })

  describe('Governance Notifications', () => {
    it('should show notification for pending checkpoints', () => {
      cy.intercept('GET', '**/governance/checkpoints*status=pending*', {
        statusCode: 200,
        body: {
          items: [{ id: 'cp-1', type: 'agent_action', status: 'pending' }],
          total: 1,
        },
      })

      cy.visit('/')

      cy.getByTestId('governance-notification').should('be.visible')
      cy.contains('1 checkpoint en attente').should('be.visible')
    })

    it('should navigate to checkpoint from notification', () => {
      cy.intercept('GET', '**/governance/checkpoints*', {
        statusCode: 200,
        body: {
          items: [{ id: 'cp-1', type: 'agent_action', status: 'pending' }],
          total: 1,
        },
      })

      cy.visit('/')

      cy.getByTestId('governance-notification').click()
      cy.url().should('include', '/governance')
    })

    it('should update notification badge in real-time', () => {
      cy.intercept('GET', '**/governance/checkpoints*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.visit('/')

      cy.getByTestId('pending-checkpoints-badge').should('not.exist')

      // Simulate WebSocket notification
      cy.window().then((win) => {
        win.dispatchEvent(new CustomEvent('governance:new-checkpoint', {
          detail: { id: 'cp-new', type: 'agent_action' },
        }))
      })

      cy.getByTestId('pending-checkpoints-badge').should('contain', '1')
    })
  })

  describe('Error Handling', () => {
    it('should handle approval error', () => {
      cy.intercept('GET', '**/governance/checkpoints/cp-1', {
        statusCode: 200,
        body: { id: 'cp-1', type: 'agent_action', status: 'pending' },
      })

      cy.intercept('POST', '**/governance/checkpoints/cp-1/approve', {
        statusCode: 409,
        body: { detail: 'Checkpoint already processed' },
      }).as('approveError')

      cy.visit('/governance/checkpoints/cp-1')

      cy.getByTestId('approve-button').click()
      cy.getByTestId('confirm-approval').click()

      cy.wait('@approveError')
      cy.contains('Déjà traité').should('be.visible')
    })

    it('should handle governance service unavailable', () => {
      cy.intercept('GET', '**/governance/status', {
        statusCode: 503,
        body: { detail: 'Governance service unavailable' },
      })

      cy.visit('/governance')

      cy.contains('Service indisponible').should('be.visible')
      cy.getByTestId('retry-button').should('be.visible')
    })
  })
})
