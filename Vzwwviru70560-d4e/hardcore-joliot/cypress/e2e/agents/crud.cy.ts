/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ — AGENTS CRUD E2E TESTS                           ║
 * ║                    Sprint B1.4: Agent Hire/Fire/Manage                       ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

describe('Agents Management', () => {
  beforeEach(() => {
    cy.loginWithMock()
    cy.mockSpheres()
    cy.mockBureauSections()
  })

  describe('Agent List', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/agents*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'agent-1',
              code: 'WRITER',
              name: 'Content Writer',
              description: 'Expert en rédaction de contenu',
              level: 'L1',
              sphere_id: 'personal',
              status: 'available',
              capabilities: ['writing', 'editing', 'summarizing'],
              token_cost_per_hour: 100,
              icon: '✍️',
            },
            {
              id: 'agent-2',
              code: 'ANALYST',
              name: 'Data Analyst',
              description: 'Analyse de données et rapports',
              level: 'L2',
              sphere_id: 'business',
              status: 'available',
              capabilities: ['analysis', 'reporting', 'visualization'],
              token_cost_per_hour: 200,
              icon: '📊',
            },
            {
              id: 'agent-3',
              code: 'CODER',
              name: 'Code Assistant',
              description: 'Aide au développement',
              level: 'L2',
              sphere_id: null,
              status: 'hired',
              capabilities: ['coding', 'debugging', 'reviewing'],
              token_cost_per_hour: 250,
              icon: '💻',
              hired_at: '2026-01-01T10:00:00Z',
              hired_scope: 'global',
            },
          ],
          total: 3,
        },
      }).as('getAgents')

      cy.intercept('GET', '**/agents/hired', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'agent-3',
              code: 'CODER',
              name: 'Code Assistant',
              status: 'hired',
              hired_at: '2026-01-01T10:00:00Z',
              hired_scope: 'global',
              token_spent: 1500,
              token_budget: 10000,
            },
          ],
          total: 1,
        },
      }).as('getHiredAgents')
    })

    it('should display available agents', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').should('be.visible')
      cy.contains('Data Analyst').should('be.visible')
      cy.contains('Code Assistant').should('be.visible')
    })

    it('should show agent details', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()

      cy.contains('Expert en rédaction').should('be.visible')
      cy.contains('L1').should('be.visible')
      cy.contains('100 tokens/h').should('be.visible')
    })

    it('should filter by level', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.getByTestId('level-filter').click()
      cy.contains('L2').click()

      cy.contains('Data Analyst').should('be.visible')
      cy.contains('Code Assistant').should('be.visible')
      cy.contains('Content Writer').should('not.exist')
    })

    it('should filter by status', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.getByTestId('status-filter').click()
      cy.contains('Engagés').click()

      cy.contains('Code Assistant').should('be.visible')
      cy.contains('Content Writer').should('not.exist')
    })

    it('should search agents', () => {
      cy.intercept('GET', '**/agents*search=writer*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'agent-1',
              code: 'WRITER',
              name: 'Content Writer',
              status: 'available',
            },
          ],
          total: 1,
        },
      }).as('searchAgents')

      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.getByTestId('agent-search').type('writer')
      cy.wait('@searchAgents')

      cy.contains('Content Writer').should('be.visible')
    })

    it('should display hired agents section', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getHiredAgents')

      cy.contains('Agents Engagés').should('be.visible')
      cy.contains('Code Assistant').should('be.visible')
      cy.contains('1500 / 10000 tokens').should('be.visible')
    })

    it('should show empty state when no agents', () => {
      cy.intercept('GET', '**/agents*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.intercept('GET', '**/agents/hired', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.visit('/sphere/personal/active_agents')

      cy.contains('Aucun agent').should('be.visible')
    })
  })

  describe('Hire Agent', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/agents*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'agent-1',
              code: 'WRITER',
              name: 'Content Writer',
              description: 'Expert en rédaction',
              level: 'L1',
              status: 'available',
              token_cost_per_hour: 100,
            },
          ],
          total: 1,
        },
      }).as('getAgents')

      cy.intercept('GET', '**/agents/hired', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.intercept('GET', '**/users/me/tokens', {
        statusCode: 200,
        body: {
          balance: 50000,
          spent_today: 1000,
          daily_limit: 100000,
        },
      }).as('getTokenBalance')
    })

    it('should open hire modal', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      cy.getByTestId('hire-modal').should('be.visible')
      cy.contains('Engager Content Writer').should('be.visible')
    })

    it('should select hire scope', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      // Select scope
      cy.getByTestId('scope-thread').click()
      cy.getByTestId('scope-thread').should('have.class', 'selected')

      cy.getByTestId('scope-sphere').click()
      cy.getByTestId('scope-sphere').should('have.class', 'selected')

      cy.getByTestId('scope-global').click()
      cy.getByTestId('scope-global').should('have.class', 'selected')
    })

    it('should select hire duration', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      cy.getByTestId('duration-session').click()
      cy.getByTestId('duration-session').should('have.class', 'selected')

      cy.getByTestId('duration-day').click()
      cy.getByTestId('duration-day').should('have.class', 'selected')
    })

    it('should set token budget', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      cy.getByTestId('token-budget-slider').invoke('val', 5000).trigger('change')
      cy.contains('5,000 tokens').should('be.visible')
    })

    it('should show cost estimation', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      cy.getByTestId('scope-sphere').click()
      cy.getByTestId('duration-day').click()

      cy.contains('Coût estimé').should('be.visible')
      cy.contains('2,400 tokens').should('be.visible') // 100 tokens/h * 24h
    })

    it('should hire agent successfully', () => {
      cy.intercept('POST', '**/agents/agent-1/hire', {
        statusCode: 201,
        body: {
          id: 'hire-1',
          agent_id: 'agent-1',
          scope: 'sphere',
          duration: 'day',
          token_budget: 5000,
          hired_at: '2026-01-03T10:00:00Z',
          expires_at: '2026-01-04T10:00:00Z',
        },
      }).as('hireAgent')

      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      cy.getByTestId('scope-sphere').click()
      cy.getByTestId('duration-day').click()
      cy.getByTestId('token-budget-slider').invoke('val', 5000).trigger('change')

      cy.getByTestId('confirm-hire').click()

      cy.wait('@hireAgent')
      cy.contains('Agent engagé').should('be.visible')
    })

    it('should show governance notice', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      cy.contains('Règles de Gouvernance').should('be.visible')
      cy.contains('Human Sovereignty').should('be.visible')
    })

    it('should warn on high budget', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      cy.getByTestId('token-budget-slider').invoke('val', 40000).trigger('change')

      cy.contains('Budget élevé').should('be.visible')
    })

    it('should prevent hire if insufficient tokens', () => {
      cy.intercept('GET', '**/users/me/tokens', {
        statusCode: 200,
        body: {
          balance: 100,
          spent_today: 99900,
          daily_limit: 100000,
        },
      })

      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('hire-button').click()

      cy.getByTestId('confirm-hire').should('be.disabled')
      cy.contains('Solde insuffisant').should('be.visible')
    })
  })

  describe('Fire Agent', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/agents*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.intercept('GET', '**/agents/hired', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'agent-1',
              code: 'WRITER',
              name: 'Content Writer',
              status: 'hired',
              hired_at: '2026-01-01T10:00:00Z',
              hired_scope: 'global',
              token_spent: 1500,
              token_budget: 10000,
            },
          ],
          total: 1,
        },
      }).as('getHiredAgents')
    })

    it('should show fire confirmation', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getHiredAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('fire-button').click()

      cy.getByTestId('confirm-dialog').should('be.visible')
      cy.contains('Résilier le contrat').should('be.visible')
    })

    it('should fire agent on confirm', () => {
      cy.intercept('DELETE', '**/agents/agent-1/hire', {
        statusCode: 204,
      }).as('fireAgent')

      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getHiredAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('fire-button').click()
      cy.getByTestId('confirm-fire').click()

      cy.wait('@fireAgent')
      cy.contains('Contrat résilié').should('be.visible')
    })

    it('should cancel fire', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getHiredAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('fire-button').click()
      cy.getByTestId('cancel-fire').click()

      cy.getByTestId('confirm-dialog').should('not.exist')
    })

    it('should show token refund info', () => {
      cy.visit('/sphere/personal/active_agents')
      cy.wait('@getHiredAgents')

      cy.contains('Content Writer').click()
      cy.getByTestId('fire-button').click()

      cy.contains('8,500 tokens remboursés').should('be.visible') // 10000 - 1500
    })
  })

  describe('Agent Interaction', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads/thread-1', {
        statusCode: 200,
        body: {
          id: 'thread-1',
          title: 'Test Thread',
          sphere_id: 'personal',
        },
      })

      cy.intercept('GET', '**/threads/thread-1/messages*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.intercept('GET', '**/threads/thread-1/agents', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'agent-1',
              code: 'WRITER',
              name: 'Content Writer',
              status: 'active',
            },
          ],
          total: 1,
        },
      }).as('getThreadAgents')
    })

    it('should show active agents in thread', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getThreadAgents')

      cy.getByTestId('active-agents-panel').should('be.visible')
      cy.contains('Content Writer').should('be.visible')
    })

    it('should mention agent with @', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getThreadAgents')

      cy.getByTestId('message-input').type('@')
      cy.getByTestId('agent-mention-dropdown').should('be.visible')
      cy.contains('Content Writer').should('be.visible')
    })

    it('should insert agent mention', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getThreadAgents')

      cy.getByTestId('message-input').type('@')
      cy.contains('Content Writer').click()

      cy.getByTestId('message-input').should('contain.value', '@WRITER')
    })

    it('should quick engage agent from thread', () => {
      cy.intercept('POST', '**/agents/agent-1/hire', {
        statusCode: 201,
        body: {
          id: 'hire-1',
          agent_id: 'agent-1',
          scope: 'thread',
          thread_id: 'thread-1',
        },
      }).as('quickHire')

      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('quick-engage-button').click()
      cy.getByTestId('agent-suggestions').should('be.visible')
      cy.contains('Content Writer').click()

      cy.wait('@quickHire')
      cy.contains('Agent engagé pour ce thread').should('be.visible')
    })
  })

  describe('Agent Console', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/agents/agent-1', {
        statusCode: 200,
        body: {
          id: 'agent-1',
          code: 'WRITER',
          name: 'Content Writer',
          description: 'Expert en rédaction',
          level: 'L1',
          status: 'hired',
          capabilities: ['writing', 'editing'],
          token_spent: 1500,
          token_budget: 10000,
        },
      }).as('getAgent')

      cy.intercept('GET', '**/agents/agent-1/tasks*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'task-1',
              description: 'Rédiger article',
              status: 'completed',
              tokens_used: 500,
              created_at: '2026-01-02T10:00:00Z',
              completed_at: '2026-01-02T10:30:00Z',
            },
            {
              id: 'task-2',
              description: 'Résumer document',
              status: 'in_progress',
              tokens_used: 200,
              created_at: '2026-01-02T11:00:00Z',
            },
          ],
          total: 2,
        },
      }).as('getAgentTasks')
    })

    it('should open agent console', () => {
      cy.visit('/sphere/personal/active_agents')

      cy.intercept('GET', '**/agents/hired', {
        statusCode: 200,
        body: {
          items: [
            { id: 'agent-1', code: 'WRITER', name: 'Content Writer', status: 'hired' },
          ],
          total: 1,
        },
      })

      cy.contains('Content Writer').click()
      cy.getByTestId('open-console').click()

      cy.wait('@getAgent')
      cy.getByTestId('agent-console').should('be.visible')
    })

    it('should display agent tasks', () => {
      cy.visit('/agents/agent-1/console')
      cy.wait('@getAgent')
      cy.wait('@getAgentTasks')

      cy.contains('Rédiger article').should('be.visible')
      cy.contains('Résumer document').should('be.visible')
    })

    it('should show task status', () => {
      cy.visit('/agents/agent-1/console')
      cy.wait('@getAgentTasks')

      cy.contains('Rédiger article')
        .parent()
        .should('contain', 'Terminé')

      cy.contains('Résumer document')
        .parent()
        .should('contain', 'En cours')
    })

    it('should show token usage', () => {
      cy.visit('/agents/agent-1/console')
      cy.wait('@getAgent')

      cy.contains('1,500 / 10,000 tokens').should('be.visible')
      cy.getByTestId('token-progress').should('have.attr', 'style').and('contain', '15%')
    })

    it('should pause agent', () => {
      cy.intercept('POST', '**/agents/agent-1/pause', {
        statusCode: 200,
        body: { status: 'paused' },
      }).as('pauseAgent')

      cy.visit('/agents/agent-1/console')
      cy.wait('@getAgent')

      cy.getByTestId('pause-agent').click()
      cy.wait('@pauseAgent')

      cy.contains('Agent en pause').should('be.visible')
    })

    it('should resume agent', () => {
      cy.intercept('GET', '**/agents/agent-1', {
        statusCode: 200,
        body: {
          id: 'agent-1',
          code: 'WRITER',
          name: 'Content Writer',
          status: 'paused',
        },
      })

      cy.intercept('POST', '**/agents/agent-1/resume', {
        statusCode: 200,
        body: { status: 'hired' },
      }).as('resumeAgent')

      cy.visit('/agents/agent-1/console')

      cy.getByTestId('resume-agent').click()
      cy.wait('@resumeAgent')

      cy.contains('Agent actif').should('be.visible')
    })
  })

  describe('Agent Levels (L0-L3)', () => {
    it('should display agent level badge', () => {
      cy.intercept('GET', '**/agents*', {
        statusCode: 200,
        body: {
          items: [
            { id: 'a1', name: 'Agent L0', level: 'L0', status: 'available' },
            { id: 'a2', name: 'Agent L1', level: 'L1', status: 'available' },
            { id: 'a3', name: 'Agent L2', level: 'L2', status: 'available' },
            { id: 'a4', name: 'Agent L3', level: 'L3', status: 'available' },
          ],
          total: 4,
        },
      })

      cy.intercept('GET', '**/agents/hired', { body: { items: [], total: 0 } })

      cy.visit('/sphere/personal/active_agents')

      cy.getByTestId('level-badge-L0').should('have.class', 'bg-gray')
      cy.getByTestId('level-badge-L1').should('have.class', 'bg-blue')
      cy.getByTestId('level-badge-L2').should('have.class', 'bg-purple')
      cy.getByTestId('level-badge-L3').should('have.class', 'bg-gold')
    })

    it('should show level restrictions info', () => {
      cy.intercept('GET', '**/agents*', {
        statusCode: 200,
        body: {
          items: [
            { id: 'a1', name: 'Agent L3', level: 'L3', status: 'available' },
          ],
          total: 1,
        },
      })

      cy.intercept('GET', '**/agents/hired', { body: { items: [], total: 0 } })

      cy.visit('/sphere/personal/active_agents')
      cy.contains('Agent L3').click()

      cy.contains('Niveau L3').should('be.visible')
      cy.contains('Approbation humaine requise').should('be.visible')
    })
  })

  describe('Error Handling', () => {
    it('should handle hire error', () => {
      cy.intercept('GET', '**/agents*', {
        statusCode: 200,
        body: {
          items: [{ id: 'a1', name: 'Agent', level: 'L1', status: 'available' }],
          total: 1,
        },
      })

      cy.intercept('GET', '**/agents/hired', { body: { items: [], total: 0 } })

      cy.intercept('POST', '**/agents/a1/hire', {
        statusCode: 409,
        body: { detail: 'Agent already hired by another user' },
      }).as('hireError')

      cy.visit('/sphere/personal/active_agents')
      cy.contains('Agent').click()
      cy.getByTestId('hire-button').click()
      cy.getByTestId('confirm-hire').click()

      cy.wait('@hireError')
      cy.contains('Agent déjà engagé').should('be.visible')
    })

    it('should handle agent not found', () => {
      cy.intercept('GET', '**/agents/nonexistent', {
        statusCode: 404,
        body: { detail: 'Agent not found' },
      })

      cy.visit('/agents/nonexistent/console')

      cy.contains('Agent non trouvé').should('be.visible')
    })
  })
})
