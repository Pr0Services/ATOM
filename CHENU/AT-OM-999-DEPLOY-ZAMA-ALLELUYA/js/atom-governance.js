/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM GOVERNANCE ORCHESTRATOR - CHE·NU™ V76
 * Point d'Entree Unifie pour le Systeme de Gouvernance
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Ce fichier orchestre:
 * - MessageBus (communication inter-agents)
 * - CheckpointManager (HITL/gouvernance)
 * - HITL UI (interface approbation)
 * - Integration avec config.js existant
 *
 * PRINCIPE: GOUVERNANCE > EXECUTION
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// GOVERNANCE ORCHESTRATOR
// ═══════════════════════════════════════════════════════════════════════════════

class ATOMGovernance {
    constructor(options = {}) {
        this.initialized = false;
        this.options = options;

        // Composants
        this.messageBus = null;
        this.checkpointManager = null;
        this.hitlUI = null;

        // Agents enregistres
        this.agents = new Map();

        // Stats
        this.stats = {
            actionsEvaluated: 0,
            checkpointsTriggered: 0,
            messagesRouted: 0
        };
    }

    /**
     * Initialise le systeme de gouvernance
     */
    async init() {
        if (this.initialized) {
            console.warn('[ATOMGovernance] Already initialized');
            return this;
        }

        console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D4AF37;');
        console.log('%c    AT-OM GOVERNANCE SYSTEM - CHE·NU™ V76', 'color: #D4AF37; font-size: 14px; font-weight: bold;');
        console.log('%c    GOUVERNANCE > EXECUTION', 'color: #9333EA; font-weight: bold;');
        console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D4AF37;');

        // 1. Initialize MessageBus
        if (typeof getATOMMessageBus !== 'undefined') {
            this.messageBus = getATOMMessageBus();
            console.log('[ATOMGovernance] ✅ MessageBus initialized');
        } else {
            console.warn('[ATOMGovernance] ⚠️ MessageBus not available');
        }

        // 2. Initialize CheckpointManager
        if (typeof getATOMCheckpointManager !== 'undefined') {
            this.checkpointManager = getATOMCheckpointManager({
                onCheckpointCreated: (cp) => this._onCheckpointCreated(cp),
                onCheckpointResolved: (cp, res) => this._onCheckpointResolved(cp, res)
            });
            console.log('[ATOMGovernance] ✅ CheckpointManager initialized');
        } else {
            console.warn('[ATOMGovernance] ⚠️ CheckpointManager not available');
        }

        // 3. Initialize HITL UI
        if (typeof initHITLUI !== 'undefined' && this.checkpointManager) {
            this.hitlUI = initHITLUI(this.checkpointManager);
            console.log('[ATOMGovernance] ✅ HITL UI initialized');
        } else {
            console.warn('[ATOMGovernance] ⚠️ HITL UI not available');
        }

        // 4. Register core agents (Nova, Aria, Orion)
        this._registerCoreAgents();

        // 5. Setup global message handler
        this._setupGlobalHandler();

        this.initialized = true;
        console.log('%c[ATOMGovernance] ✅ System ready', 'color: #00FF88; font-weight: bold;');

        return this;
    }

    /**
     * Enregistre les agents L0 core
     */
    _registerCoreAgents() {
        const coreAgents = [
            {
                id: 'nova',
                name: 'Nova',
                level: 'L0',
                frequency: 999,
                capabilities: ['system', 'monitor', 'orchestrate']
            },
            {
                id: 'aria',
                name: 'Aria',
                level: 'L1',
                frequency: 528,
                capabilities: ['onboard', 'guide', 'educate']
            },
            {
                id: 'orion',
                name: 'Orion',
                level: 'L1',
                frequency: 741,
                capabilities: ['orchestrate', 'coordinate', 'delegate']
            }
        ];

        coreAgents.forEach(agent => {
            this.registerAgent(agent.id, agent);
        });
    }

    /**
     * Configure le handler global de messages
     */
    _setupGlobalHandler() {
        if (!this.messageBus) return;

        // Subscribe to system events
        this.messageBus.subscribe('system', 'atom.governance');
        this.messageBus.subscribe('atom.checkpoints', 'atom.governance');
        this.messageBus.subscribe('atom.agents', 'atom.governance');
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // AGENT MANAGEMENT
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Enregistre un agent
     */
    registerAgent(agentId, config = {}) {
        const agent = {
            id: agentId,
            name: config.name || agentId,
            level: config.level || 'L3',
            frequency: config.frequency || 444,
            capabilities: config.capabilities || [],
            registeredAt: Date.now(),
            active: true
        };

        this.agents.set(agentId, agent);

        // Register in MessageBus
        if (this.messageBus) {
            this.messageBus.registerAgent(agentId, (message) => {
                this._handleAgentMessage(agentId, message);
            });
        }

        console.log(`[ATOMGovernance] Agent registered: ${agentId} (${agent.level})`);
        return agent;
    }

    /**
     * Desenregistre un agent
     */
    unregisterAgent(agentId) {
        this.agents.delete(agentId);
        if (this.messageBus) {
            this.messageBus.unregisterAgent(agentId);
        }
        return true;
    }

    /**
     * Recupere un agent
     */
    getAgent(agentId) {
        return this.agents.get(agentId);
    }

    /**
     * Liste tous les agents
     */
    listAgents() {
        return [...this.agents.values()];
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // ACTION EXECUTION WITH GOVERNANCE
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Execute une action avec verification HITL
     * C'est LA methode principale pour executer des actions gouvernees
     */
    async executeAction(action, callback) {
        this.stats.actionsEvaluated++;

        // Normalise l'action
        const normalizedAction = {
            id: action.id || 'action_' + Date.now(),
            name: action.name || 'Unknown Action',
            type: action.type || 'read',
            agentId: action.agentId || 'unknown',
            estimatedImpact: action.estimatedImpact ?? action.impact ?? 0.5,
            params: action.params || {},
            callback: callback
        };

        console.log(`[ATOMGovernance] Evaluating action: ${normalizedAction.name}`);

        // Evalue avec CheckpointManager
        if (this.checkpointManager) {
            const evaluation = this.checkpointManager.evaluateAction(normalizedAction);

            if (evaluation.needsCheckpoint) {
                this.stats.checkpointsTriggered++;
                console.log(`[ATOMGovernance] Checkpoint triggered: ${evaluation.checkpoint.type}`);

                // Retourne une promesse qui se resout quand le checkpoint est resolu
                return new Promise((resolve, reject) => {
                    evaluation.checkpoint._resolve = resolve;
                    evaluation.checkpoint._reject = reject;
                    evaluation.checkpoint._callback = callback;
                });
            }

            // Auto-approved
            console.log(`[ATOMGovernance] Action auto-approved`);
        }

        // Execute directement
        if (callback && typeof callback === 'function') {
            return callback();
        }

        return { success: true, autoApproved: true };
    }

    /**
     * Callback quand un checkpoint est cree
     */
    _onCheckpointCreated(checkpoint) {
        // Envoie un message sur le bus
        if (this.messageBus && typeof ATOMMessageFactory !== 'undefined') {
            const msg = ATOMMessageFactory.createEvent(
                'atom.governance',
                'checkpoint_created',
                { checkpointId: checkpoint.id, type: checkpoint.type },
                'atom.checkpoints'
            );
            this.messageBus.send(msg);
        }
    }

    /**
     * Callback quand un checkpoint est resolu
     */
    _onCheckpointResolved(checkpoint, resolution) {
        // Execute ou rejette l'action originale
        if (resolution === 'approved' && checkpoint._callback) {
            const result = checkpoint._callback();
            if (checkpoint._resolve) {
                checkpoint._resolve(result);
            }
        } else if (resolution === 'rejected' || resolution === 'timeout') {
            if (checkpoint._reject) {
                checkpoint._reject(new Error(`Action ${resolution}: ${checkpoint.resolutionNotes || 'No reason provided'}`));
            }
        }

        // Envoie un message sur le bus
        if (this.messageBus && typeof ATOMMessageFactory !== 'undefined') {
            const msg = ATOMMessageFactory.createEvent(
                'atom.governance',
                'checkpoint_resolved',
                { checkpointId: checkpoint.id, resolution },
                'atom.checkpoints'
            );
            this.messageBus.send(msg);
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // MESSAGING
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Envoie un message entre agents
     */
    sendMessage(from, to, type, payload) {
        if (!this.messageBus) {
            console.warn('[ATOMGovernance] MessageBus not available');
            return { success: false, error: 'MessageBus not available' };
        }

        if (typeof ATOMMessageFactory === 'undefined') {
            console.warn('[ATOMGovernance] MessageFactory not available');
            return { success: false, error: 'MessageFactory not available' };
        }

        const message = ATOMMessageFactory.create(type, from, to, payload);
        this.stats.messagesRouted++;

        return this.messageBus.send(message);
    }

    /**
     * Handler de messages pour un agent
     */
    _handleAgentMessage(agentId, message) {
        const agent = this.agents.get(agentId);
        if (!agent) return;

        console.log(`[ATOMGovernance] Message received by ${agentId}: ${message.type}`);

        // Gestion selon le type
        switch (message.type) {
            case 'task_delegate':
                this._handleTaskDelegation(agent, message);
                break;
            case 'escalate':
                this._handleEscalation(agent, message);
                break;
            case 'checkpoint':
                this._handleCheckpointMessage(agent, message);
                break;
            default:
            // Log seulement
        }
    }

    /**
     * Gere une delegation de tache
     */
    _handleTaskDelegation(agent, message) {
        // Verifie les capabilities
        const task = message.payload?.task;
        if (!task) return;

        const canHandle = agent.capabilities.some(cap =>
            task.requiredCapabilities?.includes(cap)
        );

        if (canHandle) {
            // Accept
            if (typeof ATOMMessageFactory !== 'undefined') {
                const accept = ATOMMessageFactory.createTaskAccept(
                    agent.id,
                    message.from,
                    message.id
                );
                this.messageBus.send(accept);
            }
        } else {
            // Reject et escalade
            if (typeof ATOMMessageFactory !== 'undefined') {
                const reject = ATOMMessageFactory.createTaskReject(
                    agent.id,
                    message.from,
                    message.id,
                    'Missing required capabilities'
                );
                this.messageBus.send(reject);
            }
        }
    }

    /**
     * Gere une escalade
     */
    _handleEscalation(agent, message) {
        console.log(`[ATOMGovernance] Escalation received by ${agent.id}`);
        // L'agent de niveau superieur recoit l'escalade
        // Implementation specifique selon le contexte
    }

    /**
     * Gere un message de checkpoint
     */
    _handleCheckpointMessage(agent, message) {
        // HITL controller reçoit les checkpoints
        if (agent.id === 'nova') {
            console.log('[ATOMGovernance] Nova received checkpoint for review');
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // UTILITIES
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Recupere les stats
     */
    getStats() {
        return {
            ...this.stats,
            agents: this.agents.size,
            messageBusStats: this.messageBus?.getStats() || null,
            checkpointStats: this.checkpointManager?.getStats() || null
        };
    }

    /**
     * Status global
     */
    getStatus() {
        return {
            initialized: this.initialized,
            messageBus: !!this.messageBus,
            checkpointManager: !!this.checkpointManager,
            hitlUI: !!this.hitlUI,
            agents: this.listAgents().map(a => ({
                id: a.id,
                level: a.level,
                active: a.active
            }))
        };
    }

    /**
     * Destruction propre
     */
    destroy() {
        if (this.messageBus) this.messageBus.destroy();
        if (this.checkpointManager) this.checkpointManager.destroy();
        this.agents.clear();
        this.initialized = false;
        console.log('[ATOMGovernance] Destroyed');
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON & AUTO-INIT
// ═══════════════════════════════════════════════════════════════════════════════

let governanceInstance = null;

function getATOMGovernance() {
    if (!governanceInstance) {
        governanceInstance = new ATOMGovernance();
    }
    return governanceInstance;
}

/**
 * Initialise automatiquement le systeme de gouvernance
 */
async function initATOMGovernance(options = {}) {
    const governance = getATOMGovernance();
    await governance.init();
    return governance;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ATOMGovernance,
        getATOMGovernance,
        initATOMGovernance
    };
}

if (typeof window !== 'undefined') {
    window.ATOMGovernance = ATOMGovernance;
    window.getATOMGovernance = getATOMGovernance;
    window.initATOMGovernance = initATOMGovernance;

    // Expose pour debug
    window.atomGovernanceStatus = () => {
        const gov = getATOMGovernance();
        console.table(gov.getStatus());
        return gov.getStats();
    };
}

console.log('%c[AT-OM] Governance Orchestrator loaded', 'color: #D4AF37;');
console.log('%c[AT-OM] Call initATOMGovernance() to start', 'color: #888;');
