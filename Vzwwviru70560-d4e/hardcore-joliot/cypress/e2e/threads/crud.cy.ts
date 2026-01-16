/**
 * ╔══════════════════════════════════════════════════════════════════════════════╗
 * ║                    CHE·NU™ — THREADS CRUD E2E TESTS                          ║
 * ║                    Sprint B1.3: Full Thread Lifecycle                        ║
 * ╚══════════════════════════════════════════════════════════════════════════════╝
 */

describe('Threads CRUD Operations', () => {
  beforeEach(() => {
    // Setup authenticated state
    cy.loginWithMock()
    cy.mockSpheres()
    cy.mockBureauSections()
  })

  describe('Thread List', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'thread-1',
              title: 'Premier thread test',
              sphere_id: 'personal',
              status: 'active',
              created_at: '2026-01-01T10:00:00Z',
              updated_at: '2026-01-02T15:30:00Z',
              message_count: 5,
              last_message: {
                content: 'Dernier message...',
                role: 'assistant',
                created_at: '2026-01-02T15:30:00Z',
              },
            },
            {
              id: 'thread-2',
              title: 'Deuxième thread',
              sphere_id: 'personal',
              status: 'active',
              created_at: '2026-01-01T09:00:00Z',
              updated_at: '2026-01-01T12:00:00Z',
              message_count: 3,
              last_message: {
                content: 'Message précédent...',
                role: 'user',
                created_at: '2026-01-01T12:00:00Z',
              },
            },
          ],
          total: 2,
          page: 1,
          per_page: 20,
        },
      }).as('getThreads')
    })

    it('should display thread list', () => {
      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      cy.contains('Premier thread test').should('be.visible')
      cy.contains('Deuxième thread').should('be.visible')
    })

    it('should show thread metadata', () => {
      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      // Check message count
      cy.contains('5 messages').should('be.visible')
      cy.contains('3 messages').should('be.visible')
    })

    it('should show empty state when no threads', () => {
      cy.intercept('GET', '**/threads*', {
        statusCode: 200,
        body: { items: [], total: 0, page: 1, per_page: 20 },
      }).as('getEmptyThreads')

      cy.visit('/sphere/personal/threads')
      cy.wait('@getEmptyThreads')

      cy.contains('Aucun thread').should('be.visible')
    })

    it('should filter threads by status', () => {
      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      // Click filter
      cy.getByTestId('thread-filter').click()
      cy.contains('Archivés').click()

      cy.wait('@getThreads')
    })

    it('should search threads', () => {
      cy.intercept('GET', '**/threads*search=test*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'thread-1',
              title: 'Premier thread test',
              sphere_id: 'personal',
              status: 'active',
              created_at: '2026-01-01T10:00:00Z',
              message_count: 5,
            },
          ],
          total: 1,
        },
      }).as('searchThreads')

      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      cy.getByTestId('thread-search').type('test')
      cy.wait('@searchThreads')

      cy.contains('Premier thread test').should('be.visible')
    })
  })

  describe('Create Thread', () => {
    it('should open create thread modal', () => {
      cy.visit('/sphere/personal/threads')

      cy.getByTestId('create-thread-button').click()
      cy.getByTestId('create-thread-modal').should('be.visible')
      cy.contains('Nouveau Thread').should('be.visible')
    })

    it('should create a new thread', () => {
      cy.intercept('POST', '**/threads', {
        statusCode: 201,
        body: {
          id: 'new-thread-id',
          title: 'Mon nouveau thread',
          sphere_id: 'personal',
          status: 'active',
          created_at: '2026-01-03T10:00:00Z',
          message_count: 0,
        },
      }).as('createThread')

      cy.intercept('GET', '**/threads*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.visit('/sphere/personal/threads')

      cy.getByTestId('create-thread-button').click()
      cy.getByTestId('thread-title-input').type('Mon nouveau thread')
      cy.getByTestId('thread-submit').click()

      cy.wait('@createThread')
      cy.contains('Thread créé').should('be.visible')
    })

    it('should validate required title', () => {
      cy.visit('/sphere/personal/threads')

      cy.getByTestId('create-thread-button').click()
      cy.getByTestId('thread-submit').click()

      cy.contains('Le titre est requis').should('be.visible')
    })

    it('should close modal on cancel', () => {
      cy.visit('/sphere/personal/threads')

      cy.getByTestId('create-thread-button').click()
      cy.getByTestId('create-thread-modal').should('be.visible')

      cy.getByTestId('cancel-button').click()
      cy.getByTestId('create-thread-modal').should('not.exist')
    })

    it('should close modal on escape key', () => {
      cy.visit('/sphere/personal/threads')

      cy.getByTestId('create-thread-button').click()
      cy.getByTestId('create-thread-modal').should('be.visible')

      cy.get('body').type('{esc}')
      cy.getByTestId('create-thread-modal').should('not.exist')
    })
  })

  describe('Thread View & Messages', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads/thread-1', {
        statusCode: 200,
        body: {
          id: 'thread-1',
          title: 'Thread de test',
          sphere_id: 'personal',
          status: 'active',
          created_at: '2026-01-01T10:00:00Z',
          updated_at: '2026-01-02T15:30:00Z',
        },
      }).as('getThread')

      cy.intercept('GET', '**/threads/thread-1/messages*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'msg-1',
              content: 'Bonjour Nova!',
              role: 'user',
              created_at: '2026-01-01T10:00:00Z',
            },
            {
              id: 'msg-2',
              content: 'Bonjour! Comment puis-je vous aider?',
              role: 'assistant',
              created_at: '2026-01-01T10:00:05Z',
              agent_id: 'nova',
            },
          ],
          total: 2,
        },
      }).as('getMessages')
    })

    it('should display thread conversation', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getThread')
      cy.wait('@getMessages')

      cy.contains('Thread de test').should('be.visible')
      cy.contains('Bonjour Nova!').should('be.visible')
      cy.contains('Comment puis-je vous aider?').should('be.visible')
    })

    it('should distinguish user and assistant messages', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      // User message should be aligned right
      cy.contains('Bonjour Nova!')
        .parent()
        .should('have.class', 'justify-end')

      // Assistant message should be aligned left
      cy.contains('Comment puis-je vous aider?')
        .parent()
        .should('have.class', 'justify-start')
    })

    it('should send a new message', () => {
      cy.intercept('POST', '**/threads/thread-1/messages', {
        statusCode: 201,
        body: {
          id: 'msg-3',
          content: 'Mon nouveau message',
          role: 'user',
          created_at: '2026-01-03T10:00:00Z',
        },
      }).as('sendMessage')

      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      cy.getByTestId('message-input').type('Mon nouveau message')
      cy.getByTestId('send-button').click()

      cy.wait('@sendMessage')
      cy.contains('Mon nouveau message').should('be.visible')
    })

    it('should send message with Enter key', () => {
      cy.intercept('POST', '**/threads/thread-1/messages', {
        statusCode: 201,
        body: {
          id: 'msg-3',
          content: 'Message avec Enter',
          role: 'user',
          created_at: '2026-01-03T10:00:00Z',
        },
      }).as('sendMessage')

      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      cy.getByTestId('message-input').type('Message avec Enter{enter}')

      cy.wait('@sendMessage')
    })

    it('should not send empty message', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      cy.getByTestId('send-button').should('be.disabled')
    })

    it('should show loading state while sending', () => {
      cy.intercept('POST', '**/threads/thread-1/messages', {
        delay: 1000,
        statusCode: 201,
        body: {
          id: 'msg-3',
          content: 'Message',
          role: 'user',
        },
      }).as('sendMessage')

      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      cy.getByTestId('message-input').type('Message')
      cy.getByTestId('send-button').click()

      cy.getByTestId('send-button').should('be.disabled')
      cy.getByTestId('sending-indicator').should('be.visible')
    })

    it('should scroll to bottom on new message', () => {
      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getMessages')

      // Messages container should be scrolled to bottom
      cy.getByTestId('messages-container').then(($el) => {
        const scrollTop = $el[0].scrollTop
        const scrollHeight = $el[0].scrollHeight
        const clientHeight = $el[0].clientHeight
        expect(scrollTop + clientHeight).to.be.closeTo(scrollHeight, 10)
      })
    })
  })

  describe('Update Thread', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads/thread-1', {
        statusCode: 200,
        body: {
          id: 'thread-1',
          title: 'Ancien titre',
          sphere_id: 'personal',
          status: 'active',
        },
      }).as('getThread')

      cy.intercept('GET', '**/threads/thread-1/messages*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })
    })

    it('should edit thread title', () => {
      cy.intercept('PATCH', '**/threads/thread-1', {
        statusCode: 200,
        body: {
          id: 'thread-1',
          title: 'Nouveau titre',
          sphere_id: 'personal',
          status: 'active',
        },
      }).as('updateThread')

      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getThread')

      cy.getByTestId('thread-menu').click()
      cy.contains('Renommer').click()

      cy.getByTestId('thread-title-input').clear().type('Nouveau titre')
      cy.getByTestId('save-title').click()

      cy.wait('@updateThread')
      cy.contains('Nouveau titre').should('be.visible')
    })

    it('should archive thread', () => {
      cy.intercept('PATCH', '**/threads/thread-1', {
        statusCode: 200,
        body: {
          id: 'thread-1',
          title: 'Ancien titre',
          status: 'archived',
        },
      }).as('archiveThread')

      cy.visit('/sphere/personal/thread/thread-1')
      cy.wait('@getThread')

      cy.getByTestId('thread-menu').click()
      cy.contains('Archiver').click()

      cy.wait('@archiveThread')
      cy.contains('Thread archivé').should('be.visible')
    })
  })

  describe('Delete Thread', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads*', {
        statusCode: 200,
        body: {
          items: [
            {
              id: 'thread-1',
              title: 'Thread à supprimer',
              sphere_id: 'personal',
              status: 'active',
            },
          ],
          total: 1,
        },
      }).as('getThreads')
    })

    it('should show delete confirmation', () => {
      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      cy.contains('Thread à supprimer').rightclick()
      cy.contains('Supprimer').click()

      cy.getByTestId('confirm-dialog').should('be.visible')
      cy.contains('Êtes-vous sûr').should('be.visible')
    })

    it('should delete thread on confirm', () => {
      cy.intercept('DELETE', '**/threads/thread-1', {
        statusCode: 204,
      }).as('deleteThread')

      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      cy.contains('Thread à supprimer').rightclick()
      cy.contains('Supprimer').click()

      cy.getByTestId('confirm-delete').click()

      cy.wait('@deleteThread')
      cy.contains('Thread supprimé').should('be.visible')
    })

    it('should cancel delete', () => {
      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      cy.contains('Thread à supprimer').rightclick()
      cy.contains('Supprimer').click()

      cy.getByTestId('cancel-delete').click()
      cy.getByTestId('confirm-dialog').should('not.exist')
      cy.contains('Thread à supprimer').should('be.visible')
    })
  })

  describe('Thread Keyboard Navigation', () => {
    beforeEach(() => {
      cy.intercept('GET', '**/threads*', {
        statusCode: 200,
        body: {
          items: [
            { id: 'thread-1', title: 'Thread 1', sphere_id: 'personal', status: 'active' },
            { id: 'thread-2', title: 'Thread 2', sphere_id: 'personal', status: 'active' },
            { id: 'thread-3', title: 'Thread 3', sphere_id: 'personal', status: 'active' },
          ],
          total: 3,
        },
      }).as('getThreads')
    })

    it('should navigate threads with arrow keys', () => {
      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      cy.get('body').type('{downarrow}')
      cy.focused().should('contain', 'Thread 1')

      cy.get('body').type('{downarrow}')
      cy.focused().should('contain', 'Thread 2')

      cy.get('body').type('{uparrow}')
      cy.focused().should('contain', 'Thread 1')
    })

    it('should open thread with Enter', () => {
      cy.visit('/sphere/personal/threads')
      cy.wait('@getThreads')

      cy.get('body').type('{downarrow}')
      cy.get('body').type('{enter}')

      cy.url().should('include', '/thread/thread-1')
    })
  })

  describe('Error Handling', () => {
    it('should handle thread creation error', () => {
      cy.intercept('POST', '**/threads', {
        statusCode: 500,
        body: { detail: 'Internal server error' },
      }).as('createThreadError')

      cy.intercept('GET', '**/threads*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.visit('/sphere/personal/threads')

      cy.getByTestId('create-thread-button').click()
      cy.getByTestId('thread-title-input').type('Test')
      cy.getByTestId('thread-submit').click()

      cy.wait('@createThreadError')
      cy.contains('Erreur').should('be.visible')
    })

    it('should handle message send error', () => {
      cy.intercept('GET', '**/threads/thread-1', {
        statusCode: 200,
        body: { id: 'thread-1', title: 'Test', sphere_id: 'personal' },
      })

      cy.intercept('GET', '**/threads/thread-1/messages*', {
        statusCode: 200,
        body: { items: [], total: 0 },
      })

      cy.intercept('POST', '**/threads/thread-1/messages', {
        statusCode: 429,
        body: { detail: 'Rate limit exceeded' },
      }).as('sendMessageError')

      cy.visit('/sphere/personal/thread/thread-1')

      cy.getByTestId('message-input').type('Test message')
      cy.getByTestId('send-button').click()

      cy.wait('@sendMessageError')
      cy.contains('limite').should('be.visible')
    })

    it('should retry on network error', () => {
      let attempt = 0
      cy.intercept('GET', '**/threads*', (req) => {
        attempt++
        if (attempt < 3) {
          req.reply({ statusCode: 503 })
        } else {
          req.reply({
            statusCode: 200,
            body: { items: [], total: 0 },
          })
        }
      }).as('getThreadsRetry')

      cy.visit('/sphere/personal/threads')

      cy.getByTestId('retry-button').click()
      cy.wait('@getThreadsRetry')
    })
  })
})
