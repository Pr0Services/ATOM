/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * CHE·NU™ — TESTS DE CONFORMITÉ CYPRESS
 * Format: GIVEN / WHEN / THEN
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * ⚠️ DIRECTIVE: Ces tests valident la conformité à la state machine canonique
 * 
 * @version 2.0.0
 * @date 2024-12-19
 */

/// <reference types="cypress" />

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const STATES = {
  PRE_ACCOUNT: 'STATE_PRE_ACCOUNT',
  ONBOARDING_THEME: 'STATE_ONBOARDING_THEME',
  ONBOARDING_SPHERES: 'STATE_ONBOARDING_SPHERES',
  PERSONAL_INIT: 'STATE_PERSONAL_INIT',
  DASHBOARD_ACTIVATION: 'STATE_DASHBOARD_ACTIVATION',
  OPERATIONAL: 'STATE_OPERATIONAL',
  SPHERE_LOBBY: 'STATE_SPHERE_LOBBY',
  SPHERE_BUREAU: 'STATE_SPHERE_BUREAU',
  WORKSPACE_ACTIVE: 'STATE_WORKSPACE_ACTIVE',
  AGENT_EXECUTION: 'STATE_AGENT_EXECUTION',
  VERSION_REVIEW: 'STATE_VERSION_REVIEW',
};

const HUBS = {
  NAVIGATION: 'HUB_A',
  EXECUTION: 'HUB_B',
  COMMUNICATION: 'HUB_C',
};

const SPHERES = [
  'PERSONAL',
  'BUSINESS',
  'GOVERNMENT_INSTITUTIONS',
  'CREATIVE_STUDIO',
  'ENTERTAINMENT',
  'COMMUNITY',
  'SOCIAL_MEDIA',
  'MY_TEAM',
];

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 1 — STRUCTURE DES HUBS
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 1 — Structure des HUBS', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('GIVEN l\'application est chargée WHEN l\'utilisateur navigue THEN HUB_C est toujours actif', () => {
    // Given: Application chargée
    cy.get('[data-testid="app-container"]').should('exist');
    
    // When: Navigation dans différents états
    cy.login();
    cy.completeOnboarding();
    
    // Then: HUB_C toujours actif
    cy.get('[data-testid="hub-communication"]')
      .should('exist')
      .and('be.visible');
    
    // Naviguer vers différentes sphères
    SPHERES.slice(0, 3).forEach((sphere) => {
      cy.enterSphere(sphere);
      cy.get('[data-testid="hub-communication"]').should('be.visible');
      cy.get('[data-testid="nova-avatar"]').should('exist');
    });
  });

  it('GIVEN l\'application est chargée THEN maximum 2 hubs sont visibles simultanément', () => {
    // Given: Utilisateur connecté en mode opérationnel
    cy.login();
    cy.completeOnboarding();
    
    // Then: Compter les hubs visibles
    cy.get('[data-testid^="hub-"]')
      .filter(':visible')
      .should('have.length.at.most', 2);
  });

  it('GIVEN l\'application est chargée THEN aucun hub ne bloque un autre', () => {
    // Given: Utilisateur en mode opérationnel
    cy.login();
    cy.completeOnboarding();
    
    // When: Interactions avec les hubs
    cy.get('[data-testid="hub-navigation"]').click();
    
    // Then: Les autres hubs restent accessibles
    cy.get('[data-testid="hub-execution"]').should('not.be.disabled');
    cy.get('[data-testid="hub-communication"]').should('not.be.disabled');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 2 — STATE MACHINE
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 2 — State Machine', () => {
  beforeEach(() => {
    cy.clearLocalStorage();
    cy.visit('/');
  });

  it('GIVEN état = PRE_ACCOUNT WHEN tentative d\'entrer dans une sphère THEN action refusée', () => {
    // Given: État PRE_ACCOUNT (pas de compte)
    cy.getCurrentState().should('eq', STATES.PRE_ACCOUNT);
    
    // When: Tentative d'entrer dans une sphère
    cy.get('[data-testid="sphere-personal"]').click({ force: true });
    
    // Then: Action refusée
    cy.get('[data-testid="error-message"]')
      .should('be.visible')
      .and('contain', 'Créez un compte');
    
    // Et aucune donnée créée
    cy.window().its('store.getState().user').should('be.null');
  });

  it('GIVEN état = PRE_ACCOUNT WHEN CREATE_ACCOUNT THEN transition vers ONBOARDING_THEME', () => {
    // Given: État PRE_ACCOUNT
    cy.getCurrentState().should('eq', STATES.PRE_ACCOUNT);
    
    // When: Création de compte
    cy.get('[data-testid="create-account-btn"]').click();
    cy.fillAccountForm();
    
    // Then: Transition vers ONBOARDING_THEME
    cy.getCurrentState().should('eq', STATES.ONBOARDING_THEME);
    cy.get('[data-testid="theme-selector"]').should('be.visible');
  });

  it('GIVEN les transitions autorisées WHEN transition interdite THEN rejetée avec log', () => {
    // Given: État ONBOARDING_THEME
    cy.login();
    cy.getCurrentState().should('eq', STATES.ONBOARDING_THEME);
    
    // When: Tentative de skip vers OPERATIONAL (interdit)
    cy.dispatch({ type: 'ENTER_OPERATIONAL' });
    
    // Then: Transition rejetée
    cy.getCurrentState().should('eq', STATES.ONBOARDING_THEME);
    
    // Et log enregistré
    cy.getTransitionLogs().should('include', {
      action: 'ENTER_OPERATIONAL',
      result: 'REJECTED',
    });
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 3 — ONBOARDING
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 3 — Onboarding', () => {
  beforeEach(() => {
    cy.clearLocalStorage();
    cy.visit('/');
    cy.createAccount();
  });

  it('GIVEN nouvel utilisateur WHEN termine sphère PERSONNEL THEN dashboard apparaît', () => {
    // Given: Nouvel utilisateur qui a complété le thème et tour des sphères
    cy.selectTheme(0);
    cy.completeSpheresTour();
    
    // When: Termine l'initialisation Personnel
    cy.getCurrentState().should('eq', STATES.PERSONAL_INIT);
    cy.get('[data-testid="personal-notes"]').type('Mes objectifs');
    cy.get('[data-testid="continue-btn"]').click();
    
    // Then: Dashboard apparaît
    cy.getCurrentState().should('eq', STATES.DASHBOARD_ACTIVATION);
    cy.get('[data-testid="dashboard"]').should('be.visible');
  });

  it('GIVEN sphère PERSONNEL complétée THEN autres sphères restent verrouillées', () => {
    // Given: Onboarding complété jusqu'au dashboard
    cy.completeOnboardingTooDashboard();
    
    // Then: Sphères autres que PERSONAL sont verrouillées
    SPHERES.filter(s => s !== 'PERSONAL').forEach((sphere) => {
      cy.get(`[data-testid="sphere-${sphere.toLowerCase()}"]`)
        .should('have.attr', 'data-locked', 'true');
    });
    
    // Et PERSONAL est active
    cy.get('[data-testid="sphere-personal"]')
      .should('have.attr', 'data-locked', 'false');
  });

  it('GIVEN onboarding THEN aucune activation automatique des sphères', () => {
    // Given: Onboarding en cours
    cy.selectTheme(0);
    cy.completeSpheresTour();
    cy.completePersonalInit();
    
    // Then: Seule PERSONAL est active
    cy.getActiveSpheres().should('deep.equal', ['PERSONAL']);
    
    // Et les autres nécessitent une activation manuelle
    cy.get('[data-testid="activate-sphere-business"]').should('exist');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 4 — BUREAU
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 4 — Bureau', () => {
  beforeEach(() => {
    cy.loginAndComplete();
    cy.enterSphere('PERSONAL');
    cy.get('[data-testid="enter-bureau-btn"]').click();
  });

  it('GIVEN sphère active WHEN entre dans bureau THEN max 8 objets visibles', () => {
    // Given: Dans le bureau d'une sphère
    cy.getCurrentState().should('eq', STATES.SPHERE_BUREAU);
    
    // Then: Maximum 8 objets
    cy.get('[data-testid^="bureau-object-"]')
      .should('have.length.at.most', 8);
  });

  it('GIVEN bureau affiché THEN aucun document affiché directement', () => {
    // Given: Dans le bureau
    cy.getCurrentState().should('eq', STATES.SPHERE_BUREAU);
    
    // Then: Pas de contenu document visible
    cy.get('[data-testid="document-content"]').should('not.exist');
    cy.get('[data-testid="document-preview"]').should('not.exist');
    
    // Le bureau affiche seulement des objets cliquables
    cy.get('[data-testid^="bureau-object-"]').each(($obj) => {
      cy.wrap($obj).should('have.attr', 'data-type', 'control');
    });
  });

  it('GIVEN bureau affiché THEN tous les objets sont cliquables', () => {
    // Given: Dans le bureau
    cy.getCurrentState().should('eq', STATES.SPHERE_BUREAU);
    
    // Then: Tous les objets ont un handler click
    cy.get('[data-testid^="bureau-object-"]').each(($obj) => {
      cy.wrap($obj)
        .should('not.be.disabled')
        .and('have.css', 'cursor', 'pointer');
    });
  });

  it('GIVEN objet bureau cliqué THEN transition vers WORKSPACE_ACTIVE', () => {
    // When: Click sur un objet
    cy.get('[data-testid="bureau-object-notes"]').click();
    
    // Then: Transition vers workspace
    cy.getCurrentState().should('eq', STATES.WORKSPACE_ACTIVE);
    cy.get('[data-testid="workspace-container"]').should('be.visible');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 5 — WORKSPACE & VERSIONING
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 5 — Workspace & Versioning', () => {
  beforeEach(() => {
    cy.loginAndComplete();
    cy.enterSphere('PERSONAL');
    cy.enterBureau();
    cy.openObject('notes');
  });

  it('GIVEN document modifié WHEN envoyé à agent THEN version originale conservée', () => {
    // Given: Document avec contenu
    cy.get('[data-testid="workspace-editor"]').type('Contenu original');
    cy.get('[data-testid="save-btn"]').click();
    
    // When: Envoi à agent
    cy.get('[data-testid="send-to-agent-btn"]').click();
    cy.selectAgent('content-enhancer');
    cy.get('[data-testid="confirm-send-btn"]').click();
    
    // Wait for agent execution
    cy.waitForAgentComplete();
    
    // Then: Version originale conservée
    cy.get('[data-testid="version-original"]')
      .should('contain', 'Contenu original');
  });

  it('GIVEN agent terminé THEN version agent proposée séparément', () => {
    // Given: Document envoyé à agent
    cy.get('[data-testid="workspace-editor"]').type('Contenu test');
    cy.get('[data-testid="save-btn"]').click();
    cy.sendToAgent('content-enhancer');
    cy.waitForAgentComplete();
    
    // Then: État VERSION_REVIEW
    cy.getCurrentState().should('eq', STATES.VERSION_REVIEW);
    
    // Et version agent séparée
    cy.get('[data-testid="version-agent"]').should('exist');
    cy.get('[data-testid="version-original"]').should('exist');
    cy.get('[data-testid="version-agent"]')
      .should('not.equal', cy.get('[data-testid="version-original"]'));
  });

  it('GIVEN versions affichées THEN diff visuel disponible', () => {
    // Given: En mode VERSION_REVIEW
    cy.sendToAgent('content-enhancer');
    cy.waitForAgentComplete();
    
    // Then: Diff visuel visible
    cy.get('[data-testid="diff-view"]').should('be.visible');
    cy.get('[data-testid="diff-additions"]').should('exist');
    cy.get('[data-testid="diff-deletions"]').should('exist');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 6 — AGENTS
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 6 — Agents', () => {
  beforeEach(() => {
    cy.loginAndComplete();
    cy.enterSphereAndBureau('PERSONAL');
    cy.openObject('notes');
  });

  it('GIVEN agent actif WHEN exécute THEN travaille dans son workspace isolé', () => {
    // Given: Envoi à agent
    cy.get('[data-testid="workspace-editor"]').type('Test content');
    cy.sendToAgent('content-enhancer');
    
    // When: Agent en exécution
    cy.getCurrentState().should('eq', STATES.AGENT_EXECUTION);
    
    // Then: Workspace agent isolé visible
    cy.get('[data-testid="agent-workspace"]').should('exist');
    cy.get('[data-testid="agent-workspace"]')
      .should('have.attr', 'data-isolated', 'true');
  });

  it('GIVEN agent actif THEN utilisateur peut observer', () => {
    // Given: Agent en exécution
    cy.sendToAgent('content-enhancer');
    cy.getCurrentState().should('eq', STATES.AGENT_EXECUTION);
    
    // Then: Logs visibles
    cy.get('[data-testid="agent-logs"]').should('be.visible');
    cy.get('[data-testid="agent-progress"]').should('be.visible');
    cy.get('[data-testid="agent-steps"]').should('exist');
  });

  it('GIVEN agent terminé THEN aucune modification sans validation', () => {
    // Given: Agent terminé
    cy.sendToAgent('content-enhancer');
    cy.waitForAgentComplete();
    
    // Then: État VERSION_REVIEW (pas de merge auto)
    cy.getCurrentState().should('eq', STATES.VERSION_REVIEW);
    
    // Et données originales non modifiées
    cy.get('[data-testid="version-original"]')
      .invoke('text')
      .should('not.include', '[AGENT]');
  });

  it('GIVEN agent actif THEN actions disponibles: INTERRUPT, MODIFY, WAIT', () => {
    // Given: Agent en exécution
    cy.sendToAgent('content-enhancer');
    cy.getCurrentState().should('eq', STATES.AGENT_EXECUTION);
    
    // Then: Actions disponibles
    cy.get('[data-testid="interrupt-btn"]').should('exist').and('not.be.disabled');
    cy.get('[data-testid="modify-instructions-btn"]').should('exist').and('not.be.disabled');
    cy.get('[data-testid="cancel-btn"]').should('exist').and('not.be.disabled');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 7 — DONNÉES
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 7 — Données', () => {
  beforeEach(() => {
    cy.loginAndComplete();
    cy.enterSphereAndBureau('PERSONAL');
    cy.openObject('notes');
  });

  it('GIVEN donnée produite par agent WHEN utilisateur refuse THEN aucune donnée fusionnée', () => {
    // Given: Agent a produit une version
    cy.get('[data-testid="workspace-editor"]').type('Original content');
    cy.get('[data-testid="save-btn"]').click();
    cy.sendToAgent('content-enhancer');
    cy.waitForAgentComplete();
    
    // When: Utilisateur refuse
    cy.get('[data-testid="reject-btn"]').click();
    
    // Then: Retour au workspace avec données originales
    cy.getCurrentState().should('eq', STATES.WORKSPACE_ACTIVE);
    cy.get('[data-testid="workspace-editor"]')
      .should('contain', 'Original content');
  });

  it('GIVEN utilisateur refuse THEN version agent reste isolée', () => {
    // Given: Version agent rejetée
    cy.createContentAndSendToAgent();
    cy.waitForAgentComplete();
    
    // When: Rejet
    cy.get('[data-testid="reject-btn"]').click();
    
    // Then: Version agent toujours accessible dans historique
    cy.get('[data-testid="version-history-btn"]').click();
    cy.get('[data-testid="version-list"]')
      .should('contain', 'Agent proposal (rejected)');
  });

  it('GIVEN utilisateur accepte THEN merge contrôlé', () => {
    // Given: Version agent prête
    cy.get('[data-testid="workspace-editor"]').type('Original');
    cy.get('[data-testid="save-btn"]').click();
    cy.sendToAgent('content-enhancer');
    cy.waitForAgentComplete();
    
    // When: Acceptation
    cy.get('[data-testid="accept-btn"]').click();
    
    // Then: Merge effectué
    cy.getCurrentState().should('eq', STATES.WORKSPACE_ACTIVE);
    
    // Et log de validation
    cy.getAuditLogs().should('include', {
      action: 'ACCEPT_AGENT_VERSION',
      validated_by: 'user',
    });
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 8 — XR
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 8 — XR', () => {
  beforeEach(() => {
    cy.loginAndComplete();
  });

  it('GIVEN XR activé WHEN sphère affichée THEN correspond à un lieu', () => {
    // Given: XR mode activé (si disponible)
    cy.enableXRMode();
    
    // When: Entrer dans une sphère
    cy.enterSphere('PERSONAL');
    
    // Then: Représentation spatiale
    cy.get('[data-testid="xr-place"]').should('exist');
    cy.get('[data-testid="xr-place"]')
      .should('have.attr', 'data-sphere', 'PERSONAL');
  });

  it('GIVEN XR mode THEN données restent 2D en backend', () => {
    // Given: XR mode activé
    cy.enableXRMode();
    cy.enterSphereAndBureau('PERSONAL');
    
    // When: Modification de données
    cy.openObject('notes');
    cy.get('[data-testid="workspace-editor"]').type('XR test data');
    cy.get('[data-testid="save-btn"]').click();
    
    // Then: Données stockées en 2D standard
    cy.window().then((win) => {
      const savedData = win.store.getState().spheres.PERSONAL.notes;
      expect(savedData.format).to.equal('2D');
      expect(savedData).to.not.have.property('xr_position');
    });
  });

  it('GIVEN application standard THEN XR n\'est jamais requis', () => {
    // Given: Mode normal (pas XR)
    cy.disableXRMode();
    
    // Then: Toutes les fonctionnalités disponibles
    cy.enterSphere('PERSONAL');
    cy.enterBureau();
    cy.openObject('notes');
    cy.get('[data-testid="workspace-editor"]').should('be.visible');
    cy.get('[data-testid="save-btn"]').should('not.be.disabled');
    cy.get('[data-testid="send-to-agent-btn"]').should('not.be.disabled');
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST 9 — RÉGRESSION STRUCTURELLE
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST 9 — Régression Structurelle', () => {
  it('GIVEN mise à jour THEN aucun hub supprimé', () => {
    cy.visit('/');
    
    // Vérifier existence des 3 hubs
    cy.window().then((win) => {
      const hubs = win.CHENU_CONFIG.hubs;
      expect(Object.keys(hubs)).to.have.length(3);
      expect(hubs).to.have.property('NAVIGATION');
      expect(hubs).to.have.property('EXECUTION');
      expect(hubs).to.have.property('COMMUNICATION');
    });
  });

  it('GIVEN mise à jour THEN aucun état sauté dans onboarding', () => {
    cy.clearLocalStorage();
    cy.visit('/');
    
    // Vérifier séquence d'états
    const expectedSequence = [
      STATES.PRE_ACCOUNT,
      STATES.ONBOARDING_THEME,
      STATES.ONBOARDING_SPHERES,
      STATES.PERSONAL_INIT,
      STATES.DASHBOARD_ACTIVATION,
    ];
    
    expectedSequence.forEach((state, index) => {
      if (index > 0) {
        cy.progressOnboarding();
      }
      cy.getCurrentState().should('eq', state);
    });
  });

  it('GIVEN mise à jour THEN 8 sphères exactement', () => {
    cy.visit('/');
    
    cy.window().then((win) => {
      const spheres = win.CHENU_CONFIG.spheres;
      expect(spheres).to.have.length(8);
      expect(spheres.map(s => s.id)).to.deep.equal(SPHERES);
    });
  });

  it('GIVEN mise à jour THEN 10 lois fondamentales respectées', () => {
    cy.visit('/');
    
    cy.window().then((win) => {
      const laws = win.CHENU_CONFIG.fundamental_laws;
      expect(laws).to.have.length(10);
      
      // Vérifier chaque loi
      expect(laws[0].law).to.include('Nova');
      expect(laws[1].law).to.include('utilisateur valide');
      expect(laws[2].law).to.include('workspace séparé');
      expect(laws[3].law).to.include('sans retour');
      expect(laws[4].law).to.include('contextes étanches');
      expect(laws[5].law).to.include('dump de données');
      expect(laws[6].law).to.include('visible');
      expect(laws[7].law).to.include('originale');
      expect(laws[8].law).to.include('ne bloque jamais');
      expect(laws[9].law).to.include('ne change jamais');
    });
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// TEST FINAL — ACCEPTATION SYSTÈME
// ═══════════════════════════════════════════════════════════════════════════════

describe('TEST FINAL — Acceptation Système', () => {
  it('GIVEN tous les tests verts THEN CHE·NU conforme et déploiement autorisé', () => {
    // Ce test s'exécute après tous les autres
    // Il vérifie que le rapport de tests est vert
    
    cy.task('getTestResults').then((results) => {
      expect(results.failed).to.equal(0);
      expect(results.passed).to.be.greaterThan(0);
      
      // Générer badge de conformité
      cy.task('generateComplianceBadge', {
        status: 'PASSED',
        version: '2.0.0',
        date: new Date().toISOString(),
      });
    });
  });
});

// ═══════════════════════════════════════════════════════════════════════════════
// CUSTOM COMMANDS
// ═══════════════════════════════════════════════════════════════════════════════

Cypress.Commands.add('getCurrentState', () => {
  return cy.window().its('store.getState().stateMachine.currentState');
});

Cypress.Commands.add('dispatch', (action) => {
  return cy.window().then((win) => {
    win.store.dispatch(action);
  });
});

Cypress.Commands.add('getTransitionLogs', () => {
  return cy.window().its('store.getState().stateMachine.transitionLogs');
});

Cypress.Commands.add('getActiveSpheres', () => {
  return cy.window().its('store.getState().spheres.active');
});

Cypress.Commands.add('getAuditLogs', () => {
  return cy.window().its('store.getState().governance.auditLogs');
});

Cypress.Commands.add('login', () => {
  cy.get('[data-testid="create-account-btn"]').click();
  cy.get('[data-testid="email-input"]').type('test@chenu.io');
  cy.get('[data-testid="password-input"]').type('Test123!');
  cy.get('[data-testid="submit-btn"]').click();
});

Cypress.Commands.add('loginAndComplete', () => {
  cy.login();
  cy.completeOnboarding();
});

Cypress.Commands.add('createAccount', () => {
  cy.get('[data-testid="create-account-btn"]').click();
  cy.get('[data-testid="email-input"]').type('test@chenu.io');
  cy.get('[data-testid="password-input"]').type('Test123!');
  cy.get('[data-testid="submit-btn"]').click();
});

Cypress.Commands.add('selectTheme', (index) => {
  cy.get(`[data-testid="theme-option-${index}"]`).click();
  cy.get('[data-testid="continue-btn"]').click();
});

Cypress.Commands.add('completeSpheresTour', () => {
  cy.wait(3200); // 8 sphères * 400ms delay
  cy.get('[data-testid="continue-btn"]').click();
});

Cypress.Commands.add('completePersonalInit', () => {
  cy.get('[data-testid="personal-notes"]').type('Mes objectifs');
  cy.get('[data-testid="continue-btn"]').click();
});

Cypress.Commands.add('completeOnboarding', () => {
  cy.selectTheme(0);
  cy.completeSpheresTour();
  cy.completePersonalInit();
  cy.get('[data-testid="start-operational-btn"]').click();
});

Cypress.Commands.add('completeOnboardingTooDashboard', () => {
  cy.selectTheme(0);
  cy.completeSpheresTour();
  cy.completePersonalInit();
});

Cypress.Commands.add('enterSphere', (sphereId) => {
  cy.get(`[data-testid="sphere-${sphereId.toLowerCase()}"]`).click();
});

Cypress.Commands.add('enterBureau', () => {
  cy.get('[data-testid="enter-bureau-btn"]').click();
});

Cypress.Commands.add('enterSphereAndBureau', (sphereId) => {
  cy.enterSphere(sphereId);
  cy.enterBureau();
});

Cypress.Commands.add('openObject', (objectId) => {
  cy.get(`[data-testid="bureau-object-${objectId}"]`).click();
});

Cypress.Commands.add('sendToAgent', (agentId) => {
  cy.get('[data-testid="send-to-agent-btn"]').click();
  cy.get(`[data-testid="agent-option-${agentId}"]`).click();
  cy.get('[data-testid="confirm-send-btn"]').click();
});

Cypress.Commands.add('waitForAgentComplete', () => {
  cy.get('[data-testid="agent-status"]', { timeout: 30000 })
    .should('contain', 'Complete');
});

Cypress.Commands.add('createContentAndSendToAgent', () => {
  cy.get('[data-testid="workspace-editor"]').type('Test content');
  cy.get('[data-testid="save-btn"]').click();
  cy.sendToAgent('content-enhancer');
});

Cypress.Commands.add('enableXRMode', () => {
  cy.get('[data-testid="settings-btn"]').click();
  cy.get('[data-testid="xr-toggle"]').click();
  cy.get('[data-testid="close-settings"]').click();
});

Cypress.Commands.add('disableXRMode', () => {
  cy.get('[data-testid="settings-btn"]').click();
  cy.get('[data-testid="xr-toggle"]').uncheck();
  cy.get('[data-testid="close-settings"]').click();
});

Cypress.Commands.add('progressOnboarding', () => {
  cy.get('[data-testid="continue-btn"]').click();
});

Cypress.Commands.add('fillAccountForm', () => {
  cy.get('[data-testid="email-input"]').type('test@chenu.io');
  cy.get('[data-testid="password-input"]').type('Test123!');
  cy.get('[data-testid="submit-btn"]').click();
});
