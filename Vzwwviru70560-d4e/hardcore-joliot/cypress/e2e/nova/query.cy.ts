/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ — NOVA QUERY E2E TESTS                            ║
 * ║                    Sprint B1.5: Nova AI Interaction                          ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

describe('Nova AI Queries', () => {
  beforeEach(() => {
    cy.loginWithMock()
    cy.mockSpheres()
    cy.mockBureauSections()

    cy.intercept('GET', '**/nova/status', {
      statusCode: 200,
      body: {
        status: 'active',
        level: 'L0',
        description: 'Nova is active and monitoring',
        capabilities: ['query', 'analyze', 'recommend', 'orchestrate'],
      },
    }).as('getNovaStatus')
  })

  describe('Nova Status', () => {
    it('should display Nova status in header', () => {
      cy.visit('/')
      cy.wait('@getNovaStatus')

      cy.getByTestId('nova-status-indicator').should('be.visible')
      cy.contains('Nova').should('be.visible')
      cy.contains('L0').should('be.visible')
    })

    it('should show Nova as active', () => {
      cy.visit('/')
      cy.wait('@getNovaStatus')

      cy.getByTestId('nova-status-indicator')
        .should('have.class', 'active')
    })

    it('should show Nova as degraded when issues', () => {
      cy.intercept('GET', '**/nova/status', {
        statusCode: 200,
        body: {
          status: 'degraded',
          level: 'L0',
          description: 'Some services are slow',
        },
      })

      cy.visit('/')

      cy.getByTestId('nova-status-indicator')
        .should('have.class', 'degraded')
    })

    it('should show Nova as offline', () => {
      cy.intercept('GET', '**/nova/status', {
        statusCode: 503,
        body: { detail: 'Nova is currently unavailable' },
      })

      cy.visit('/')

      cy.getByTestId('nova-status-indicator')
        .should('have.class', 'offline')
    })
  })

  describe('Quick Nova Query', () => {
    beforeEach(() => {
      cy.intercept('POST', '**/nova/query', (req) => {
        req.reply({
          statusCode: 200,
          body: {
            id: 'query-1',
            response: 'Voici ma réponse à votre question...',
            tokens_used: 150,
            created_at: '2026-01-03T10:00:00Z',
            context: {
              sphere: 'personal',
              confidence: 0.95,
            },
          },
        })
      }).as('novaQuery')
    })

    it('should send query from dashboard', () => {
      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Quelles sont mes tâches aujourd\'hui?')
      cy.getByTestId('nova-submit').click()

      cy.wait('@novaQuery')
      cy.contains('Voici ma réponse').should('be.visible')
    })

    it('should send query with Enter key', () => {
      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question rapide{enter}')

      cy.wait('@novaQuery')
    })

    it('should show loading state during query', () => {
      cy.intercept('POST', '**/nova/query', {
        delay: 1000,
        statusCode: 200,
        body: {
          id: 'query-1',
          response: 'Réponse...',
          tokens_used: 100,
        },
      }).as('slowQuery')

      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Test')
      cy.getByTestId('nova-submit').click()

      cy.getByTestId('nova-loading').should('be.visible')
      cy.contains('Nova réfléchit').should('be.visible')

      cy.wait('@slowQuery')
      cy.getByTestId('nova-loading').should('not.exist')
    })

    it('should display tokens used', () => {
      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question')
      cy.getByTestId('nova-submit').click()

      cy.wait('@novaQuery')
      cy.contains('150 tokens').should('be.visible')
    })

    it('should show context sphere', () => {
      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question')
      cy.getByTestId('nova-submit').click()

      cy.wait('@novaQuery')
      cy.contains('Personnel').should('be.visible')
    })
  })

  describe('Nova in Thread', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads/thread-1', {
        statusCode: 200,
        body: {
          id: 'thread-1',
          title: 'Discussion avec Nova',
          sphere_id: 'personal',
          status: 'active',
        },
      }).as('getThread')

      cy.intercept('GET', '**/threads/thread-1/messages*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'msg-1',
              content: 'Bonjour Nova, peux-tu m\'aider?',
              role: 'user',
              created_at: '2026-01-01T10:00:00Z',
            },
            {
              id: 'msg-2',
              content: 'Bien sûr! Comment puis-je vous assister aujourd\'hui?',
              role: 'assistant',
              agent_id: 'nova',
              created_at: '2026-01-01T10:00:05Z',
              tokens_used: 50,
            },
          ],
          total: 2,
        },
      }).as('getMessages')

      cy.intercept('POST', '**/threads/thread-1/messages', {
        statusCode: 201,
        body: {
          id: 'msg-3',
          content: 'Nouvelle question',
          role: 'user',
          created_at: '2026-01-03T10:00:00Z',
        },
      }).as('sendMessage')

      cy.intercept('POST', '**/nova/stream', (req) => {
        // Simulate streaming response
        req.reply({
          statusCode: 200,
          headers: {
            'content-type': 'text/event-stream',
          },
          body: 'data: {"type": "start"}\n\ndata: {"type": "token", "content": "Voici "}\n\ndata: {"type": "token", "content": "ma réponse."}\n\ndata: {"type": "end", "tokens_used": 100}\n\n',
        })
      }).as('novaStream')
    })

    it('should show Nova avatar on assistant messages', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      cy.getByTestId('message-nova')
        .find('[data-testid="nova-avatar"]')
        .should('be.visible')
    })

    it('should display thinking indicator', () => {
      cy.intercept('POST', '**/threads/thread-1/messages', {
        delay: 2000,
        statusCode: 201,
        body: { id: 'msg-3', content: 'Test', role: 'user' },
      })

      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      cy.getByTestId('message-input').type('Test')
      cy.getByTestId('send-button').click()

      cy.getByTestId('nova-thinking').should('be.visible')
      cy.contains('Nova analyse').should('be.visible')
    })

    it('should stream Nova response', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      cy.getByTestId('message-input').type('Nouvelle question')
      cy.getByTestId('send-button').click()

      cy.wait('@sendMessage')

      // Should show streaming response
      cy.getByTestId('streaming-message').should('be.visible')
    })

    it('should use Cmd+Enter to enhance message', () => {
      cy.intercept('POST', '**/nova/enhance', {
        statusCode: 200,
        body: {
          enhanced: 'Message amélioré et plus clair',
          original: 'msg pas clair',
        },
      }).as('enhance')

      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      cy.getByTestId('message-input').type('msg pas clair')
      cy.getByTestId('message-input').type('{cmd}{enter}')

      cy.wait('@enhance')
      cy.getByTestId('message-input').should('have.value', 'Message amélioré et plus clair')
    })
  })

  describe('Nova Commands', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads/thread-1', {
        statusCode: 200,
        body: { id: 'thread-1', title: 'Test', sphere_id: 'personal' },
      })

      cy.intercept('GET', '**/threads/thread-1/messages*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })
    })

    it('should show command menu with /', () => {
      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('message-input').type('/')
      cy.getByTestId('command-menu').should('be.visible')
    })

    it('should list available commands', () => {
      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('message-input').type('/')

      cy.contains('/enhance').should('be.visible')
      cy.contains('/code').should('be.visible')
      cy.contains('/image').should('be.visible')
      cy.contains('/summarize').should('be.visible')
      cy.contains('/translate').should('be.visible')
    })

    it('should filter commands while typing', () => {
      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('message-input').type('/cod')

      cy.contains('/code').should('be.visible')
      cy.contains('/image').should('not.exist')
    })

    it('should execute /code command', () => {
      cy.intercept('POST', '**/nova/code', {
        statusCode: 200,
        body: {
          code: 'function hello() { console.log("Hello"); }',
          language: 'javascript',
          explanation: 'A simple hello function',
        },
      }).as('codeCommand')

      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('message-input').type('/code Write a hello function')
      cy.getByTestId('send-button').click()

      cy.wait('@codeCommand')
      cy.getByTestId('code-block').should('be.visible')
    })

    it('should execute /image command', () => {
      cy.intercept('POST', '**/nova/image', {
        statusCode: 200,
        body: {
          image_url: 'https://example.com/image.png',
          prompt: 'A beautiful sunset',
        },
      }).as('imageCommand')

      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('message-input').type('/image A beautiful sunset')
      cy.getByTestId('send-button').click()

      cy.wait('@imageCommand')
      cy.getByTestId('generated-image').should('be.visible')
    })

    it('should execute /summarize command', () => {
      cy.intercept('POST', '**/nova/summarize', {
        statusCode: 200,
        body: {
          summary: 'Résumé: Points clés de la conversation...',
          key_points: ['Point 1', 'Point 2', 'Point 3'],
        },
      }).as('summarize')

      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('message-input').type('/summarize')
      cy.getByTestId('send-button').click()

      cy.wait('@summarize')
      cy.contains('Points clés').should('be.visible')
    })
  })

  describe('Nova Context Awareness', () => {
    it('should use sphere context', () => {
      cy.intercept('POST', '**/nova/query', (req) => {
        expect(req.body.context.sphere).to.eq('business')
        req.reply({
          statusCode: 200,
          body: { id: 'q1', response: 'Réponse business', tokens_used: 100 },
        })
      }).as('queryWithContext')

      cy.visit('/sphere/business')

      cy.getByTestId('nova-quick-input').type('Question business')
      cy.getByTestId('nova-submit').click()

      cy.wait('@queryWithContext')
    })

    it('should use thread context', () => {
      cy.intercept('GET', '**/threads/thread-1', {
        statusCode: 200,
        body: { id: 'thread-1', title: 'Projet X', sphere_id: 'business' },
      })

      cy.intercept('GET', '**/threads/thread-1/messages*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.intercept('POST', '**/threads/thread-1/messages', (req) => {
        expect(req.body.context.thread_id).to.eq('thread-1')
        req.reply({
          statusCode: 201,
          body: { id: 'msg-1', content: 'Test', role: 'user' },
        })
      }).as('messageWithContext')

      cy.visit('/sphere/business/thread/thread-1')

      cy.getByTestId('message-input').type('Question')
      cy.getByTestId('send-button').click()

      cy.wait('@messageWithContext')
    })

    it('should remember conversation history', () => {
      cy.intercept('GET', '**/threads/thread-1', {
        statusCode: 200,
        body: { id: 'thread-1', title: 'Test', sphere_id: 'personal' },
      })

      cy.intercept('GET', '**/threads/thread-1/messages*', {
        statusCode: 200,
        body: {
          items: [
            { id: 'msg-1', content: 'Mon nom est Jean', role: 'user' },
            { id: 'msg-2', content: 'Bonjour Jean!', role: 'assistant' },
          ],
          total: 2,
        },
      })

      cy.intercept('POST', '**/threads/thread-1/messages', (req) => {
        // Should include message history
        expect(req.body.include_history).to.be.true
        req.reply({
          statusCode: 201,
          body: { id: 'msg-3', content: 'Oui Jean, bien sûr!', role: 'assistant' },
        })
      }).as('queryWithHistory')

      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('message-input').type('Tu te souviens de mon nom?')
      cy.getByTestId('send-button').click()

      cy.wait('@queryWithHistory')
    })
  })

  describe('Nova Token Management', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/users/me/tokens', {
        statusCode: 200,
        body: {
          balance: 50000,
          spent_today: 5000,
          daily_limit: 100000,
          nova_usage: {
            queries: 25,
            tokens: 4500,
          },
        },
      }).as('getTokens')
    })

    it('should display token usage after query', () => {
      cy.intercept('POST', '**/nova/query', {
        statusCode: 200,
        body: { id: 'q1', response: 'Réponse', tokens_used: 150 },
      }).as('query')

      cy.visit('/')
      cy.wait('@getTokens')

      cy.getByTestId('nova-quick-input').type('Question')
      cy.getByTestId('nova-submit').click()

      cy.wait('@query')
      cy.contains('150 tokens').should('be.visible')
    })

    it('should warn on low token balance', () => {
      cy.intercept('GET', '**/users/me/tokens', {
        statusCode: 200,
        body: {
          balance: 500,
          spent_today: 99500,
          daily_limit: 100000,
        },
      })

      cy.visit('/')

      cy.getByTestId('token-warning').should('be.visible')
      cy.contains('Solde faible').should('be.visible')
    })

    it('should prevent query when no tokens', () => {
      cy.intercept('GET', '**/users/me/tokens', {
        statusCode: 200,
        body: {
          balance: 0,
          spent_today: 100000,
          daily_limit: 100000,
        },
      })

      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question')
      cy.getByTestId('nova-submit').should('be.disabled')
      cy.contains('Limite atteinte').should('be.visible')
    })

    it('should show daily usage stats', () => {
      cy.visit('/')
      cy.wait('@getTokens')

      cy.getByTestId('nova-stats').click()

      cy.contains('25 requêtes').should('be.visible')
      cy.contains('4,500 tokens').should('be.visible')
    })
  })

  describe('Nova Error Handling', () => {
    it('should handle query timeout', () => {
      cy.intercept('POST', '**/nova/query', {
        delay: 31000, // 31 seconds
        statusCode: 408,
        body: { detail: 'Request timeout' },
      }).as('timeout')

      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question')
      cy.getByTestId('nova-submit').click()

      cy.contains('Délai dépassé', { timeout: 35000 }).should('be.visible')
    })

    it('should handle rate limit', () => {
      cy.intercept('POST', '**/nova/query', {
        statusCode: 429,
        body: { detail: 'Rate limit exceeded', retry_after: 60 },
      }).as('rateLimit')

      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question')
      cy.getByTestId('nova-submit').click()

      cy.wait('@rateLimit')
      cy.contains('Trop de requêtes').should('be.visible')
      cy.contains('60 secondes').should('be.visible')
    })

    it('should handle content filter', () => {
      cy.intercept('POST', '**/nova/query', {
        statusCode: 400,
        body: { detail: 'Content filtered for safety', code: 'CONTENT_FILTER' },
      }).as('filtered')

      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question inappropriée')
      cy.getByTestId('nova-submit').click()

      cy.wait('@filtered')
      cy.contains('contenu filtré').should('be.visible')
    })

    it('should retry on server error', () => {
      let attempts = 0
      cy.intercept('POST', '**/nova/query', (req) => {
        attempts++
        if (attempts < 3) {
          req.reply({ statusCode: 500 })
        } else {
          req.reply({
            statusCode: 200,
            body: { id: 'q1', response: 'Réponse après retry', tokens_used: 100 },
          })
        }
      }).as('retryQuery')

      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question')
      cy.getByTestId('nova-submit').click()

      cy.contains('Réponse après retry', { timeout: 10000 }).should('be.visible')
    })
  })

  describe('Nova Accessibility', () => {
    it('should be keyboard accessible', () => {
      cy.visit('/')

      cy.get('body').tab()
      // Should eventually focus on Nova input
      cy.focused().should('have.attr', 'data-testid', 'nova-quick-input')
    })

    it('should announce response to screen readers', () => {
      cy.intercept('POST', '**/nova/query', {
        statusCode: 200,
        body: { id: 'q1', response: 'Réponse de Nova', tokens_used: 100 },
      })

      cy.visit('/')

      cy.getByTestId('nova-quick-input').type('Question{enter}')

      cy.get('[role="status"]').should('contain', 'Réponse de Nova')
    })

    it('should have proper ARIA labels', () => {
      cy.visit('/')

      cy.getByTestId('nova-quick-input')
        .should('have.attr', 'aria-label', 'Demander à Nova')

      cy.getByTestId('nova-submit')
        .should('have.attr', 'aria-label', 'Envoyer la question')
    })
  })
})
