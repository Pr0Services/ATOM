/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM CONFIGURATION CENTRALE - CHE·NU™ V76
 * Source de Vérité Canonique pour la Plateforme
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Architecte: Jonathan Emmanuel Rodrigue
 * Version: CHE·NU™ V76 | 9 Domaines | 400+ Agents
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES PLATEFORME - AT·OM
// ═══════════════════════════════════════════════════════════════════════════════

const ATOM_CONSTANTS = {
    DOMAINS: 9,           // 9 domaines d'expertise
    AGENTS_TARGET: 400,   // Objectif d'agents
    VERSION_NUM: 76,      // Version CHE·NU
    PHI: 1.618033988749895  // Nombre d'or (design ratio)
};

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION BACKEND - SOURCE DE VÉRITÉ
// ═══════════════════════════════════════════════════════════════════════════════

const ATOM_CONFIG = {
    // API REST - Source canonique
    API_BASE: 'https://atom-2autu.ondigitalocean.app',

    // WebSocket - Source canonique
    WS_URL: 'wss://atom-2autu.ondigitalocean.app/ws',

    // Timeouts
    FETCH_TIMEOUT: 5000,      // 5 secondes
    WS_TIMEOUT: 8000,         // 8 secondes
    WS_RECONNECT_INTERVAL: 2000,  // 2 secondes
    WS_MAX_RECONNECT: 10,
    WS_HEARTBEAT_INTERVAL: 30000, // 30 secondes

    // Cache
    CACHE_KEY: 'atom_agents_cache',
    CACHE_TIME_KEY: 'atom_cache_time',
    CACHE_MAX_AGE: 3600000,   // 1 heure

    // Version
    VERSION: 'CHE·NU™ V76',
    APP_NAME: 'AT-OM | Plateforme d\'Intelligence Collective'
};

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES DE FALLBACK - Agents par défaut si API indisponible
// ═══════════════════════════════════════════════════════════════════════════════

const FALLBACK_AGENTS = [
    { id: 1, name: "Nova", sphere: "Personnel", level: "Expert", status: "active" },
    { id: 2, name: "Atlas", sphere: "Entreprise", level: "Expert", status: "active" },
    { id: 3, name: "Harmony", sphere: "Communication", level: "Avancé", status: "active" },
    { id: 4, name: "Phoenix", sphere: "Création", level: "Expert", status: "active" },
    { id: 5, name: "Guardian", sphere: "Institutions", level: "Expert", status: "active" },
    { id: 6, name: "Aria", sphere: "Personnel", level: "Expert", status: "active" },
    { id: 7, name: "Orion", sphere: "Entreprise", level: "Expert", status: "active" },
    { id: 8, name: "Catalyst", sphere: "Logistique", level: "Avancé", status: "active" },
    { id: 9, name: "Sentinel", sphere: "Institutions", level: "Avancé", status: "active" },
    { id: 10, name: "Architect", sphere: "Entreprise", level: "Avancé", status: "active" },
    { id: 11, name: "Messenger", sphere: "Communication", level: "Confirmé", status: "active" },
    { id: 12, name: "Analyst", sphere: "Formation", level: "Avancé", status: "active" }
];

// ═══════════════════════════════════════════════════════════════════════════════
// UTILITAIRES API
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Fetch avec timeout - Ne bloque jamais indéfiniment
 */
async function atomFetch(endpoint, timeout = ATOM_CONFIG.FETCH_TIMEOUT) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const url = endpoint.startsWith('http') ? endpoint : `${ATOM_CONFIG.API_BASE}${endpoint}`;
        const response = await fetch(url, {
            signal: controller.signal,
            headers: { 'Accept': 'application/json' }
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout');
        }
        throw error;
    }
}

/**
 * POST avec timeout - Pour envoyer des données au backend
 */
async function atomPost(endpoint, body, timeout = ATOM_CONFIG.FETCH_TIMEOUT * 3) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const url = endpoint.startsWith('http') ? endpoint : `${ATOM_CONFIG.API_BASE}${endpoint}`;
        const response = await fetch(url, {
            method: 'POST',
            signal: controller.signal,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout');
        }
        throw error;
    }
}

/**
 * Récupère les agents avec fallback automatique
 * @returns {Promise<{agents: Array, source: string, error: string|null}>}
 */
async function getAgents() {
    let result = { agents: [], source: 'fallback', error: null };

    // Essayer l'API d'abord
    try {
        const response = await atomFetch('/agents');

        if (response.ok) {
            const data = await response.json();
            result.agents = Array.isArray(data) ? data : [];
            result.source = 'api';

            // Mettre en cache
            saveToCache(result.agents);

            console.log(`%c[AT-OM] ✅ ${result.agents.length} agents chargés depuis l'API`, 'color: #00FF88;');
            return result;
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        result.error = error.message;
        console.warn(`[AT-OM] ⚠️ API indisponible: ${error.message}`);
    }

    // Essayer le cache
    const cached = getFromCache();
    if (cached && cached.length > 0) {
        result.agents = cached;
        result.source = 'cache';
        console.log(`%c[AT-OM] 📦 ${result.agents.length} agents chargés depuis le cache`, 'color: #D8B26A;');
        return result;
    }

    // Utiliser le fallback
    result.agents = FALLBACK_AGENTS;
    result.source = 'fallback';
    console.log(`%c[AT-OM] 🔄 ${result.agents.length} agents fallback utilisés`, 'color: #FF6B6B;');
    return result;
}

/**
 * Sauvegarde dans le cache localStorage
 */
function saveToCache(agents) {
    try {
        localStorage.setItem(ATOM_CONFIG.CACHE_KEY, JSON.stringify(agents));
        localStorage.setItem(ATOM_CONFIG.CACHE_TIME_KEY, Date.now().toString());
    } catch (e) {
        console.warn('[AT-OM] Cache save failed:', e);
    }
}

/**
 * Récupère depuis le cache localStorage (si non expiré)
 */
function getFromCache() {
    try {
        const cached = localStorage.getItem(ATOM_CONFIG.CACHE_KEY);
        const cacheTime = localStorage.getItem(ATOM_CONFIG.CACHE_TIME_KEY);

        if (cached && cacheTime) {
            const age = Date.now() - parseInt(cacheTime);
            if (age < ATOM_CONFIG.CACHE_MAX_AGE) {
                return JSON.parse(cached);
            }
        }
    } catch (e) {
        console.warn('[AT-OM] Cache read failed:', e);
    }
    return null;
}

// ═══════════════════════════════════════════════════════════════════════════════
// LOGGER - Affichage des constantes plateforme
// ═══════════════════════════════════════════════════════════════════════════════

function logATOMBanner() {
    console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D8B26A;');
    console.log('%c    AT·OM | Plateforme d\'Intelligence Collective - CHE·NU™ V76', 'color: #D8B26A; font-size: 16px; font-weight: bold;');
    console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D8B26A;');
    console.log('%c    Domaines    = ' + ATOM_CONSTANTS.DOMAINS, 'color: #00FF88;');
    console.log('%c    Agents      = ' + ATOM_CONSTANTS.AGENTS_TARGET + '+', 'color: #00FF88;');
    console.log('%c    Version     = V' + ATOM_CONSTANTS.VERSION_NUM, 'color: #00FF88;');
    console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D8B26A;');
    console.log('%c    Architecte: Jonathan Emmanuel Rodrigue', 'color: #888;');
    console.log('%c    API: ' + ATOM_CONFIG.API_BASE, 'color: #888;');
    console.log('%c    WS:  ' + ATOM_CONFIG.WS_URL, 'color: #888;');
    console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D8B26A;');
}

// Auto-log au chargement
if (typeof window !== 'undefined') {
    logATOMBanner();
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ATOM_CONFIG,
        ATOM_CONSTANTS,
        FALLBACK_AGENTS,
        atomFetch,
        atomPost,
        getAgents,
        saveToCache,
        getFromCache,
        logATOMBanner
    };
}
