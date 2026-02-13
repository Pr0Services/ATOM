/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM AGENT HIERARCHY - CHE·NU™ V76
 * Hiérarchie des Agents L0-L3 avec Permissions et Escalation
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Niveaux d'Agents:
 * - L0: System Agents (Nova, Aria, Orion) - Accès total
 * - L1: Orchestrators - Coordination et délégation
 * - L2: Specialists - Expertise domaine
 * - L3: Assistants - Exécution tâches
 *
 * Principe: GOUVERNANCE > EXECUTION
 * Les agents recommandent, jamais ne décident seuls
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// NIVEAUX D'AGENTS
// ═══════════════════════════════════════════════════════════════════════════════

const AGENT_LEVELS = {
    L0_SYSTEM: 0,      // System Overseer (Nova 999Hz)
    L1_ORCHESTRATOR: 1, // Orchestrators (Orion 741Hz)
    L2_SPECIALIST: 2,   // Domain Specialists
    L3_ASSISTANT: 3     // Task Assistants
};

const LEVEL_NAMES = {
    0: 'System',
    1: 'Orchestrator',
    2: 'Specialist',
    3: 'Assistant'
};

// ═══════════════════════════════════════════════════════════════════════════════
// PERMISSIONS PAR NIVEAU
// ═══════════════════════════════════════════════════════════════════════════════

const LEVEL_PERMISSIONS = {
    [AGENT_LEVELS.L0_SYSTEM]: {
        canCommand: true,          // Peut envoyer des COMMAND
        canEscalate: true,         // Peut escalader
        canApprove: true,          // Peut approuver checkpoints
        canModifySystem: true,     // Peut modifier config système
        canAccessAllData: true,    // Accès données complètes
        canDelegateToAll: true,    // Peut déléguer à tous niveaux
        requiresHITL: false,       // Pas besoin approbation humaine
        maxImpactScore: 1.0        // Impact max autorisé
    },
    [AGENT_LEVELS.L1_ORCHESTRATOR]: {
        canCommand: true,
        canEscalate: true,
        canApprove: false,         // Doit escalader pour approbation
        canModifySystem: false,
        canAccessAllData: true,
        canDelegateToAll: false,   // Seulement L2-L3
        requiresHITL: true,        // Pour actions à impact > 0.5
        maxImpactScore: 0.7
    },
    [AGENT_LEVELS.L2_SPECIALIST]: {
        canCommand: false,         // Seulement REQUEST
        canEscalate: true,
        canApprove: false,
        canModifySystem: false,
        canAccessAllData: false,
        canDelegateToAll: false,   // Seulement L3
        requiresHITL: true,        // Pour actions à impact > 0.3
        maxImpactScore: 0.5
    },
    [AGENT_LEVELS.L3_ASSISTANT]: {
        canCommand: false,
        canEscalate: true,         // Peut escalader vers L2+
        canApprove: false,
        canModifySystem: false,
        canAccessAllData: false,
        canDelegateToAll: false,
        requiresHITL: true,        // Pour toute action à impact > 0.1
        maxImpactScore: 0.3
    }
};

// ═══════════════════════════════════════════════════════════════════════════════
// AGENTS CORE L0
// ═══════════════════════════════════════════════════════════════════════════════

const CORE_AGENTS_L0 = {
    nova: {
        id: 'nova',
        name: 'Nova',
        level: AGENT_LEVELS.L0_SYSTEM,
        icon: '🔱',
        role: 'System Overseer',
        color: '#9333EA',
        capabilities: ['system_control', 'governance', 'emergency', 'audit'],
        description: 'Superviseur système et coordinateur des agents'
    },
    aria: {
        id: 'aria',
        name: 'Aria',
        level: AGENT_LEVELS.L0_SYSTEM,
        icon: '✨',
        role: 'Onboarding Guide',
        color: '#00FF88',
        capabilities: ['onboarding', 'guidance', 'support', 'education'],
        description: 'Guide d\'accueil et accompagnement utilisateur'
    },
    orion: {
        id: 'orion',
        name: 'Orion',
        level: AGENT_LEVELS.L1_ORCHESTRATOR, // L1, pas L0
        icon: '🏛️',
        role: 'User Orchestrator',
        color: '#FF6B35',
        capabilities: ['orchestration', 'planning', 'coordination', 'delegation'],
        description: 'Orchestrateur personnel coordonnant les 400+ agents'
    }
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE AGENT
// ═══════════════════════════════════════════════════════════════════════════════

class Agent {
    constructor(config) {
        this.id = config.id;
        this.name = config.name;
        this.level = config.level ?? AGENT_LEVELS.L3_ASSISTANT;
        this.frequency = config.frequency ?? 444;
        this.icon = config.icon ?? '🤖';
        this.role = config.role ?? 'Assistant';
        this.color = config.color ?? '#D4AF37';
        this.capabilities = config.capabilities ?? [];
        this.description = config.description ?? '';
        this.sphere = config.sphere ?? 'general';
        this.status = 'idle'; // idle, working, waiting, error
        this.currentTask = null;
        this.taskHistory = [];
        this.createdAt = Date.now();
    }

    /**
     * Obtenir les permissions de cet agent
     */
    getPermissions() {
        return LEVEL_PERMISSIONS[this.level] || LEVEL_PERMISSIONS[AGENT_LEVELS.L3_ASSISTANT];
    }

    /**
     * Vérifier si l'agent peut effectuer une action
     */
    canPerformAction(action) {
        const permissions = this.getPermissions();
        const impact = action.estimatedImpact ?? 0;

        // Vérifier impact max
        if (impact > permissions.maxImpactScore) {
            return {
                allowed: false,
                reason: `Impact ${impact} exceeds max ${permissions.maxImpactScore} for ${LEVEL_NAMES[this.level]}`,
                suggestion: 'escalate'
            };
        }

        // Vérifier type d'action
        if (action.type === 'command' && !permissions.canCommand) {
            return {
                allowed: false,
                reason: `${LEVEL_NAMES[this.level]} agents cannot send COMMAND`,
                suggestion: 'use_request'
            };
        }

        if (action.requiresApproval && !permissions.canApprove) {
            return {
                allowed: false,
                reason: `${LEVEL_NAMES[this.level]} agents cannot approve`,
                suggestion: 'escalate'
            };
        }

        // Vérifier si HITL requis
        if (permissions.requiresHITL && impact > 0.3) {
            return {
                allowed: true,
                requiresHITL: true,
                reason: `Action requires human approval (impact: ${impact})`
            };
        }

        return { allowed: true, requiresHITL: false };
    }

    /**
     * Vérifier si l'agent peut déléguer à un autre
     */
    canDelegateTo(targetAgent) {
        const permissions = this.getPermissions();

        if (permissions.canDelegateToAll) {
            return true;
        }

        // L1 peut déléguer à L2-L3
        if (this.level === AGENT_LEVELS.L1_ORCHESTRATOR) {
            return targetAgent.level >= AGENT_LEVELS.L2_SPECIALIST;
        }

        // L2 peut déléguer à L3 seulement
        if (this.level === AGENT_LEVELS.L2_SPECIALIST) {
            return targetAgent.level === AGENT_LEVELS.L3_ASSISTANT;
        }

        return false;
    }

    /**
     * Mettre à jour le statut
     */
    setStatus(status, task = null) {
        this.status = status;
        this.currentTask = task;
        if (task && status === 'working') {
            this.taskHistory.push({
                task: task,
                startedAt: Date.now()
            });
        }
    }

    /**
     * Sérialiser l'agent
     */
    toJSON() {
        return {
            id: this.id,
            name: this.name,
            level: this.level,
            levelName: LEVEL_NAMES[this.level],
            frequency: this.frequency,
            icon: this.icon,
            role: this.role,
            color: this.color,
            capabilities: this.capabilities,
            sphere: this.sphere,
            status: this.status,
            permissions: this.getPermissions()
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// REGISTRE DES AGENTS
// ═══════════════════════════════════════════════════════════════════════════════

class AgentRegistry {
    constructor() {
        this.agents = new Map();
        this.byLevel = new Map();
        this.bySphere = new Map();

        // Initialiser les maps par niveau
        Object.values(AGENT_LEVELS).forEach(level => {
            this.byLevel.set(level, new Set());
        });

        // Enregistrer les agents L0 core
        Object.values(CORE_AGENTS_L0).forEach(config => {
            this.register(new Agent(config));
        });
    }

    /**
     * Enregistrer un agent
     */
    register(agent) {
        if (!(agent instanceof Agent)) {
            agent = new Agent(agent);
        }

        this.agents.set(agent.id, agent);

        // Indexer par niveau
        if (!this.byLevel.has(agent.level)) {
            this.byLevel.set(agent.level, new Set());
        }
        this.byLevel.get(agent.level).add(agent.id);

        // Indexer par sphère
        if (!this.bySphere.has(agent.sphere)) {
            this.bySphere.set(agent.sphere, new Set());
        }
        this.bySphere.get(agent.sphere).add(agent.id);

        console.log(`[AgentRegistry] Registered: ${agent.name} (L${agent.level})`);
        return agent;
    }

    /**
     * Obtenir un agent par ID
     */
    get(agentId) {
        return this.agents.get(agentId);
    }

    /**
     * Obtenir tous les agents d'un niveau
     */
    getByLevel(level) {
        const ids = this.byLevel.get(level) || new Set();
        return Array.from(ids).map(id => this.agents.get(id));
    }

    /**
     * Obtenir tous les agents d'une sphère
     */
    getBySphere(sphere) {
        const ids = this.bySphere.get(sphere) || new Set();
        return Array.from(ids).map(id => this.agents.get(id));
    }

    /**
     * Trouver un agent capable de gérer une action
     */
    findCapableAgent(action, preferredLevel = null) {
        const requiredCapabilities = action.capabilities || [];

        // Chercher par niveau préféré d'abord
        if (preferredLevel !== null) {
            const agents = this.getByLevel(preferredLevel);
            for (const agent of agents) {
                if (this._hasCapabilities(agent, requiredCapabilities)) {
                    const check = agent.canPerformAction(action);
                    if (check.allowed) {
                        return agent;
                    }
                }
            }
        }

        // Chercher dans tous les niveaux (du plus bas au plus haut)
        for (let level = AGENT_LEVELS.L3_ASSISTANT; level >= AGENT_LEVELS.L0_SYSTEM; level--) {
            const agents = this.getByLevel(level);
            for (const agent of agents) {
                if (this._hasCapabilities(agent, requiredCapabilities)) {
                    const check = agent.canPerformAction(action);
                    if (check.allowed) {
                        return agent;
                    }
                }
            }
        }

        return null;
    }

    _hasCapabilities(agent, required) {
        if (required.length === 0) return true;
        return required.every(cap => agent.capabilities.includes(cap));
    }

    /**
     * Statistiques du registre
     */
    getStats() {
        const stats = {
            total: this.agents.size,
            byLevel: {},
            bySphere: {}
        };

        this.byLevel.forEach((ids, level) => {
            stats.byLevel[LEVEL_NAMES[level]] = ids.size;
        });

        this.bySphere.forEach((ids, sphere) => {
            stats.bySphere[sphere] = ids.size;
        });

        return stats;
    }

    /**
     * Lister tous les agents
     */
    listAll() {
        return Array.from(this.agents.values()).map(a => a.toJSON());
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// ESCALATION MANAGER
// ═══════════════════════════════════════════════════════════════════════════════

class EscalationManager {
    constructor(registry) {
        this.registry = registry;
        this.escalationChain = new Map(); // agentId -> parentAgentId
        this.escalationHistory = [];
    }

    /**
     * Définir la chaîne d'escalation pour un agent
     */
    setEscalationPath(agentId, parentAgentId) {
        this.escalationChain.set(agentId, parentAgentId);
    }

    /**
     * Escalader une action vers le niveau supérieur
     */
    escalate(fromAgent, action, reason) {
        const escalation = {
            id: `ESC-${Date.now()}`,
            fromAgent: fromAgent.id,
            fromLevel: fromAgent.level,
            action: action,
            reason: reason,
            timestamp: Date.now(),
            status: 'pending'
        };

        // Trouver l'agent cible
        let targetAgent = null;

        // D'abord chercher dans la chaîne définie
        const parentId = this.escalationChain.get(fromAgent.id);
        if (parentId) {
            targetAgent = this.registry.get(parentId);
        }

        // Sinon, chercher au niveau supérieur
        if (!targetAgent && fromAgent.level > AGENT_LEVELS.L0_SYSTEM) {
            const higherLevel = fromAgent.level - 1;
            const candidates = this.registry.getByLevel(higherLevel);

            // Préférer un agent de la même sphère
            targetAgent = candidates.find(a => a.sphere === fromAgent.sphere);

            // Sinon prendre le premier disponible
            if (!targetAgent && candidates.length > 0) {
                targetAgent = candidates[0];
            }
        }

        // Si niveau L0 ou pas de cible, escalader vers HITL
        if (!targetAgent) {
            escalation.toAgent = 'HITL';
            escalation.toLevel = -1; // Human level
            escalation.status = 'awaiting_human';

            // Déclencher l'interface HITL si disponible
            if (typeof window !== 'undefined' && window.atomGovernance) {
                window.atomGovernance.requestHITL(action, escalation);
            }
        } else {
            escalation.toAgent = targetAgent.id;
            escalation.toLevel = targetAgent.level;

            // Vérifier si l'agent cible peut gérer
            const check = targetAgent.canPerformAction(action);
            if (check.allowed && !check.requiresHITL) {
                escalation.status = 'delegated';
            } else if (check.requiresHITL) {
                escalation.status = 'awaiting_human';
            } else {
                // Escalader encore plus haut
                return this.escalate(targetAgent, action, check.reason);
            }
        }

        this.escalationHistory.push(escalation);

        console.log(`[Escalation] ${fromAgent.name} → ${escalation.toAgent}: ${reason}`);

        return escalation;
    }

    /**
     * Obtenir l'historique d'escalation
     */
    getHistory(limit = 50) {
        return this.escalationHistory.slice(-limit);
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON & EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

let agentRegistry = null;
let escalationManager = null;

/**
 * Initialiser le système de hiérarchie des agents
 */
function initAgentHierarchy() {
    if (!agentRegistry) {
        agentRegistry = new AgentRegistry();
        escalationManager = new EscalationManager(agentRegistry);

        console.log('%c═══════════════════════════════════════════════════════════', 'color: #9333EA;');
        console.log('%c  AT-OM AGENT HIERARCHY - ACTIVE', 'color: #00FF88; font-size: 12px;');
        console.log('%c  L0: System | L1: Orchestrator | L2: Specialist | L3: Assistant', 'color: #D4AF37;');
        console.log('%c═══════════════════════════════════════════════════════════', 'color: #9333EA;');
    }

    return {
        registry: agentRegistry,
        escalation: escalationManager
    };
}

// Auto-init si dans browser
if (typeof window !== 'undefined') {
    window.AGENT_LEVELS = AGENT_LEVELS;
    window.LEVEL_NAMES = LEVEL_NAMES;
    window.Agent = Agent;
    window.AgentRegistry = AgentRegistry;
    window.EscalationManager = EscalationManager;
    window.initAgentHierarchy = initAgentHierarchy;
    window.getAgentRegistry = () => agentRegistry;
    window.getEscalationManager = () => escalationManager;

    // Auto-init
    document.addEventListener('DOMContentLoaded', () => {
        initAgentHierarchy();
    });
}

// Export pour modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AGENT_LEVELS,
        LEVEL_NAMES,
        LEVEL_PERMISSIONS,
        CORE_AGENTS_L0,
        Agent,
        AgentRegistry,
        EscalationManager,
        initAgentHierarchy
    };
}
