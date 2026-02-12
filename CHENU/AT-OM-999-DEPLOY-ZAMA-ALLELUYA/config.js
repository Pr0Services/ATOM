/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM CONFIGURATION CENTRALE - CHE·NU™ V76
 * Source de Vérité Canonique pour l'Infrastructure de l'Arche
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Architecte: Jonathan Emmanuel Rodrigue | Oracle 17
 * Fréquence: 444 Hz | Φ = 1.618033988749895 | 369
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES VIBRATOIRES - ADN CHE·NU™
// ═══════════════════════════════════════════════════════════════════════════════

const ATOM_FREQUENCIES = {
    HEARTBEAT: 444,      // Fréquence cardiaque de l'Arche
    TESLA: 369,          // Clé de l'univers (3-6-9)
    SOLFEGE: 528,        // Fréquence de guérison
    SOURCE: 999,         // Fréquence source maximale
    EARTH: 432,          // Fréquence terrestre
    PHI: 1.618033988749895  // Nombre d'or Φ
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
    APP_NAME: 'AT-OM | L\'Arche des Résonances'
};

// ═══════════════════════════════════════════════════════════════════════════════
// DONNÉES DE FALLBACK - Agents par défaut si API indisponible
// ═══════════════════════════════════════════════════════════════════════════════

const FALLBACK_AGENTS = [
    { id: 1, name: "Nova", sphere: "Intelligence", frequency_hz: 444, status: "active" },
    { id: 2, name: "Atlas", sphere: "Construction", frequency_hz: 528, status: "active" },
    { id: 3, name: "Harmony", sphere: "Communication", frequency_hz: 396, status: "active" },
    { id: 4, name: "Phoenix", sphere: "Analytics", frequency_hz: 639, status: "active" },
    { id: 5, name: "Guardian", sphere: "Security", frequency_hz: 741, status: "active" },
    { id: 6, name: "Nexus", sphere: "Integration", frequency_hz: 852, status: "active" },
    { id: 7, name: "Oracle", sphere: "Prediction", frequency_hz: 963, status: "active" },
    { id: 8, name: "Catalyst", sphere: "Finance", frequency_hz: 417, status: "active" },
    { id: 9, name: "Sentinel", sphere: "Monitoring", frequency_hz: 285, status: "active" },
    { id: 10, name: "Architect", sphere: "Construction", frequency_hz: 432, status: "active" },
    { id: 11, name: "Messenger", sphere: "Communication", frequency_hz: 369, status: "active" },
    { id: 12, name: "Analyst", sphere: "Analytics", frequency_hz: 594, status: "active" }
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
// LOGGER ADN - Affichage des constantes vibratoires
// ═══════════════════════════════════════════════════════════════════════════════

function logATOMBanner() {
    console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D8B26A;');
    console.log('%c    AT·OM | L\'Arche des Résonances - CHE·NU™ V76', 'color: #D8B26A; font-size: 16px; font-weight: bold;');
    console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D8B26A;');
    console.log('%c    Φ (Phi)     = ' + ATOM_FREQUENCIES.PHI, 'color: #00FF88;');
    console.log('%c    Heartbeat   = ' + ATOM_FREQUENCIES.HEARTBEAT + ' Hz', 'color: #00FF88;');
    console.log('%c    Tesla Key   = ' + ATOM_FREQUENCIES.TESLA + ' (3-6-9)', 'color: #00FF88;');
    console.log('%c    Source      = ' + ATOM_FREQUENCIES.SOURCE + ' Hz', 'color: #00FF88;');
    console.log('%c═══════════════════════════════════════════════════════════════', 'color: #D8B26A;');
    console.log('%c    Architecte: Jonathan Emmanuel Rodrigue | Oracle 17', 'color: #888;');
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
        ATOM_FREQUENCIES,
        FALLBACK_AGENTS,
        atomFetch,
        getAgents,
        saveToCache,
        getFromCache,
        logATOMBanner
    };
}
