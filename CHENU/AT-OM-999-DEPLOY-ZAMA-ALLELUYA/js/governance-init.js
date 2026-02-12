/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM GOVERNANCE INIT - CHE·NU™ V76
 * Script d'initialisation unifie pour toutes les pages
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Ce script charge et initialise automatiquement:
 * - MessageBus (communication inter-agents)
 * - CheckpointManager (HITL/gouvernance)
 * - HITL UI (interface approbation)
 * - ATOMGovernance (orchestrateur)
 * - AgentHierarchy (niveaux L0-L3)
 * - MemoryManager (3-tier: Hot/Warm/Cold)
 *
 * Usage: Inclure ce script apres config.js dans toutes les pages
 * <script src="/js/governance-init.js"></script>
 */

'use strict';

(function() {
    // ═══════════════════════════════════════════════════════════════════════════
    // CONFIGURATION
    // ═══════════════════════════════════════════════════════════════════════════

    const GOVERNANCE_CONFIG = {
        enabled: true,
        autoInit: true,
        debug: false,
        scripts: [
            '/js/message-types.js',
            '/js/message-bus.js',
            '/js/checkpoint-manager.js',
            '/js/hitl-ui.js',
            '/js/atom-governance.js',
            '/js/agent-hierarchy.js',
            '/js/memory-manager.js'
        ]
    };

    // ═══════════════════════════════════════════════════════════════════════════
    // SCRIPT LOADER
    // ═══════════════════════════════════════════════════════════════════════════

    let scriptsLoaded = 0;
    let governanceReady = false;

    /**
     * Charge un script de maniere sequentielle
     */
    function loadScript(src) {
        return new Promise((resolve, reject) => {
            // Check if already loaded
            if (document.querySelector(`script[src="${src}"]`)) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = src;
            script.async = false;

            script.onload = () => {
                scriptsLoaded++;
                if (GOVERNANCE_CONFIG.debug) {
                    console.log(`[GovernanceInit] Loaded: ${src} (${scriptsLoaded}/${GOVERNANCE_CONFIG.scripts.length})`);
                }
                resolve();
            };

            script.onerror = () => {
                console.warn(`[GovernanceInit] Failed to load: ${src}`);
                reject(new Error(`Failed to load ${src}`));
            };

            document.head.appendChild(script);
        });
    }

    /**
     * Charge tous les scripts de gouvernance en sequence
     */
    async function loadGovernanceScripts() {
        if (!GOVERNANCE_CONFIG.enabled) {
            console.log('[GovernanceInit] Governance disabled');
            return false;
        }

        try {
            for (const src of GOVERNANCE_CONFIG.scripts) {
                await loadScript(src);
            }
            return true;
        } catch (err) {
            console.error('[GovernanceInit] Script loading failed:', err);
            return false;
        }
    }

    /**
     * Initialise le systeme de gouvernance
     */
    async function initGovernance() {
        if (governanceReady) {
            return window.atomGovernance;
        }

        const loaded = await loadGovernanceScripts();
        if (!loaded) {
            console.warn('[GovernanceInit] Scripts not loaded, skipping init');
            return null;
        }

        // Wait for DOM if needed
        if (document.readyState === 'loading') {
            await new Promise(resolve => {
                document.addEventListener('DOMContentLoaded', resolve);
            });
        }

        // Initialize governance system
        if (typeof initATOMGovernance === 'function') {
            try {
                const governance = await initATOMGovernance();
                window.atomGovernance = governance;
                governanceReady = true;

                // Initialize Agent Hierarchy
                if (typeof initAgentHierarchy === 'function') {
                    const hierarchy = initAgentHierarchy();
                    window.atomAgentRegistry = hierarchy.registry;
                    window.atomEscalation = hierarchy.escalation;
                }

                // Initialize Memory Manager
                if (typeof initMemoryManager === 'function') {
                    window.atomMemory = initMemoryManager();
                }

                console.log('%c═══════════════════════════════════════════════════════════', 'color: #D4AF37;');
                console.log('%c  AT-OM GOVERNANCE SYSTEM - FULLY ACTIVE', 'color: #00FF88; font-size: 12px; font-weight: bold;');
                console.log('%c  GOUVERNANCE > EXECUTION', 'color: #9333EA;');
                console.log('%c  Agents L0-L3 | Memory 3-Tier | HITL Checkpoints', 'color: #D4AF37;');
                console.log('%c═══════════════════════════════════════════════════════════', 'color: #D4AF37;');

                // Dispatch event for other modules
                window.dispatchEvent(new CustomEvent('atomGovernanceReady', {
                    detail: { governance }
                }));

                return governance;
            } catch (err) {
                console.error('[GovernanceInit] Initialization failed:', err);
                return null;
            }
        } else {
            console.warn('[GovernanceInit] initATOMGovernance not available');
            return null;
        }
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // GLOBAL API
    // ═══════════════════════════════════════════════════════════════════════════

    /**
     * Execute une action avec verification HITL
     * @param {Object} action - L'action a executer
     * @param {Function} callback - La fonction a appeler si approuve
     * @returns {Promise} Resultat de l'action
     */
    window.executeWithGovernance = async function(action, callback) {
        const governance = window.atomGovernance || await initGovernance();
        if (!governance) {
            // Fallback: execute directement si gouvernance non disponible
            console.warn('[Governance] Not available, executing directly');
            return callback ? callback() : { success: true };
        }
        return governance.executeAction(action, callback);
    };

    /**
     * Envoie un message entre agents via le MessageBus
     */
    window.sendAgentMessage = function(from, to, type, payload) {
        const governance = window.atomGovernance;
        if (!governance) {
            console.warn('[Governance] Not ready, message not sent');
            return { success: false, error: 'Governance not ready' };
        }
        return governance.sendMessage(from, to, type, payload);
    };

    /**
     * Verifie le statut de la gouvernance
     */
    window.getGovernanceStatus = function() {
        const governance = window.atomGovernance;
        if (!governance) {
            return {
                ready: false,
                message: 'Governance not initialized'
            };
        }
        return {
            ready: governanceReady,
            status: governance.getStatus(),
            stats: governance.getStats()
        };
    };

    // ═══════════════════════════════════════════════════════════════════════════
    // AUTO-INIT
    // ═══════════════════════════════════════════════════════════════════════════

    if (GOVERNANCE_CONFIG.autoInit) {
        // Start loading immediately
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initGovernance);
        } else {
            // DOM already loaded
            setTimeout(initGovernance, 100);
        }
    }

    // Expose init function for manual initialization
    window.initATOMGovernanceSystem = initGovernance;

    console.log('%c[AT-OM] Governance Init script loaded', 'color: #D4AF37;');
})();
