/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * AT-OM MEMORY MANAGER - CHE·NU™ V76
 * Système de Mémoire 3-Tiers: Hot / Warm / Cold
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * Architecture:
 * - HOT:  Session Memory (RAM) - Accès immédiat, volatile
 * - WARM: Local Storage - Persistant local, accès rapide
 * - COLD: IndexedDB/API - Persistant distant, accès async
 *
 * Intégration Supabase pour la couche Cold
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const MEMORY_CONFIG = {
    // TTL par défaut (en ms)
    HOT_TTL: 5 * 60 * 1000,        // 5 minutes
    WARM_TTL: 60 * 60 * 1000,      // 1 heure
    COLD_TTL: 24 * 60 * 60 * 1000, // 24 heures

    // Limites de taille
    HOT_MAX_ITEMS: 100,
    WARM_MAX_SIZE: 5 * 1024 * 1024,  // 5 MB
    COLD_DB_NAME: 'atom_cold_storage',
    COLD_DB_VERSION: 1,

    // Préfixes localStorage
    WARM_PREFIX: 'atom_warm_',
    WARM_META_KEY: 'atom_warm_meta',

    // Supabase
    SUPABASE_URL: null,  // Sera initialisé
    SUPABASE_KEY: null
};

// ═══════════════════════════════════════════════════════════════════════════════
// HOT MEMORY - Session (RAM)
// ═══════════════════════════════════════════════════════════════════════════════

class HotMemory {
    constructor() {
        this.cache = new Map();
        this.metadata = new Map(); // TTL, accessCount, etc.
        this.maxItems = MEMORY_CONFIG.HOT_MAX_ITEMS;
    }

    /**
     * Stocker en mémoire hot
     */
    set(key, value, ttl = MEMORY_CONFIG.HOT_TTL) {
        // Éviction LRU si plein
        if (this.cache.size >= this.maxItems) {
            this._evictLRU();
        }

        this.cache.set(key, value);
        this.metadata.set(key, {
            createdAt: Date.now(),
            ttl: ttl,
            expiresAt: Date.now() + ttl,
            accessCount: 0,
            lastAccess: Date.now()
        });

        return true;
    }

    /**
     * Récupérer de la mémoire hot
     */
    get(key) {
        if (!this.cache.has(key)) {
            return null;
        }

        const meta = this.metadata.get(key);

        // Vérifier expiration
        if (meta && Date.now() > meta.expiresAt) {
            this.delete(key);
            return null;
        }

        // Mettre à jour metadata
        if (meta) {
            meta.accessCount++;
            meta.lastAccess = Date.now();
        }

        return this.cache.get(key);
    }

    /**
     * Supprimer une entrée
     */
    delete(key) {
        this.cache.delete(key);
        this.metadata.delete(key);
    }

    /**
     * Vérifier si une clé existe
     */
    has(key) {
        return this.cache.has(key) && !this._isExpired(key);
    }

    /**
     * Vider toute la mémoire hot
     */
    clear() {
        this.cache.clear();
        this.metadata.clear();
    }

    /**
     * Éviction LRU (Least Recently Used)
     */
    _evictLRU() {
        let oldest = null;
        let oldestTime = Infinity;

        this.metadata.forEach((meta, key) => {
            if (meta.lastAccess < oldestTime) {
                oldestTime = meta.lastAccess;
                oldest = key;
            }
        });

        if (oldest) {
            this.delete(oldest);
        }
    }

    _isExpired(key) {
        const meta = this.metadata.get(key);
        return meta && Date.now() > meta.expiresAt;
    }

    /**
     * Nettoyer les entrées expirées
     */
    cleanup() {
        const expired = [];
        this.metadata.forEach((meta, key) => {
            if (Date.now() > meta.expiresAt) {
                expired.push(key);
            }
        });
        expired.forEach(key => this.delete(key));
        return expired.length;
    }

    /**
     * Statistiques
     */
    getStats() {
        return {
            size: this.cache.size,
            maxItems: this.maxItems,
            usage: (this.cache.size / this.maxItems * 100).toFixed(1) + '%'
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// WARM MEMORY - LocalStorage
// ═══════════════════════════════════════════════════════════════════════════════

class WarmMemory {
    constructor() {
        this.prefix = MEMORY_CONFIG.WARM_PREFIX;
        this.metaKey = MEMORY_CONFIG.WARM_META_KEY;
        this.maxSize = MEMORY_CONFIG.WARM_MAX_SIZE;
        this._loadMeta();
    }

    _loadMeta() {
        try {
            const meta = localStorage.getItem(this.metaKey);
            this.meta = meta ? JSON.parse(meta) : {};
        } catch (e) {
            this.meta = {};
        }
    }

    _saveMeta() {
        try {
            localStorage.setItem(this.metaKey, JSON.stringify(this.meta));
        } catch (e) {
            console.warn('[WarmMemory] Meta save failed:', e);
        }
    }

    /**
     * Stocker en localStorage
     */
    set(key, value, ttl = MEMORY_CONFIG.WARM_TTL) {
        const fullKey = this.prefix + key;

        try {
            const data = JSON.stringify({
                value: value,
                createdAt: Date.now(),
                expiresAt: Date.now() + ttl
            });

            // Vérifier la taille
            if (data.length > this.maxSize) {
                console.warn('[WarmMemory] Data too large:', key);
                return false;
            }

            localStorage.setItem(fullKey, data);

            // Mettre à jour meta
            this.meta[key] = {
                size: data.length,
                expiresAt: Date.now() + ttl,
                createdAt: Date.now()
            };
            this._saveMeta();

            return true;
        } catch (e) {
            console.warn('[WarmMemory] Set failed:', e);
            // Tenter un cleanup si quota dépassé
            if (e.name === 'QuotaExceededError') {
                this.cleanup();
                return this.set(key, value, ttl); // Retry
            }
            return false;
        }
    }

    /**
     * Récupérer de localStorage
     */
    get(key) {
        const fullKey = this.prefix + key;

        try {
            const raw = localStorage.getItem(fullKey);
            if (!raw) return null;

            const data = JSON.parse(raw);

            // Vérifier expiration
            if (Date.now() > data.expiresAt) {
                this.delete(key);
                return null;
            }

            return data.value;
        } catch (e) {
            console.warn('[WarmMemory] Get failed:', e);
            return null;
        }
    }

    /**
     * Supprimer
     */
    delete(key) {
        const fullKey = this.prefix + key;
        localStorage.removeItem(fullKey);
        delete this.meta[key];
        this._saveMeta();
    }

    /**
     * Vérifier existence
     */
    has(key) {
        return this.get(key) !== null;
    }

    /**
     * Nettoyer les expirés
     */
    cleanup() {
        let cleaned = 0;
        Object.keys(this.meta).forEach(key => {
            if (this.meta[key].expiresAt < Date.now()) {
                this.delete(key);
                cleaned++;
            }
        });
        return cleaned;
    }

    /**
     * Vider tout
     */
    clear() {
        Object.keys(this.meta).forEach(key => {
            localStorage.removeItem(this.prefix + key);
        });
        this.meta = {};
        this._saveMeta();
    }

    /**
     * Statistiques
     */
    getStats() {
        let totalSize = 0;
        Object.values(this.meta).forEach(m => {
            totalSize += m.size || 0;
        });

        return {
            items: Object.keys(this.meta).length,
            totalSize: totalSize,
            maxSize: this.maxSize,
            usage: (totalSize / this.maxSize * 100).toFixed(1) + '%'
        };
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// COLD MEMORY - IndexedDB + Supabase
// ═══════════════════════════════════════════════════════════════════════════════

class ColdMemory {
    constructor() {
        this.dbName = MEMORY_CONFIG.COLD_DB_NAME;
        this.dbVersion = MEMORY_CONFIG.COLD_DB_VERSION;
        this.db = null;
        this.supabaseUrl = MEMORY_CONFIG.SUPABASE_URL;
        this.supabaseKey = MEMORY_CONFIG.SUPABASE_KEY;
        this._initDB();
    }

    async _initDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);

            request.onerror = () => {
                console.error('[ColdMemory] IndexedDB error:', request.error);
                reject(request.error);
            };

            request.onsuccess = () => {
                this.db = request.result;
                console.log('[ColdMemory] IndexedDB ready');
                resolve(this.db);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;

                // Store principal
                if (!db.objectStoreNames.contains('cold_data')) {
                    const store = db.createObjectStore('cold_data', { keyPath: 'key' });
                    store.createIndex('expiresAt', 'expiresAt', { unique: false });
                    store.createIndex('category', 'category', { unique: false });
                }

                // Store pour sync Supabase
                if (!db.objectStoreNames.contains('sync_queue')) {
                    db.createObjectStore('sync_queue', { keyPath: 'id', autoIncrement: true });
                }
            };
        });
    }

    async _ensureDB() {
        if (!this.db) {
            await this._initDB();
        }
        return this.db;
    }

    /**
     * Stocker en IndexedDB
     */
    async set(key, value, options = {}) {
        const db = await this._ensureDB();

        const data = {
            key: key,
            value: value,
            category: options.category || 'default',
            createdAt: Date.now(),
            expiresAt: Date.now() + (options.ttl || MEMORY_CONFIG.COLD_TTL),
            syncToCloud: options.syncToCloud !== false
        };

        return new Promise((resolve, reject) => {
            const tx = db.transaction(['cold_data'], 'readwrite');
            const store = tx.objectStore('cold_data');

            const request = store.put(data);

            request.onsuccess = () => {
                // Ajouter à la queue de sync si nécessaire
                if (data.syncToCloud && this.supabaseUrl) {
                    this._queueSync('set', key, value);
                }
                resolve(true);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Récupérer de IndexedDB
     */
    async get(key) {
        const db = await this._ensureDB();

        return new Promise((resolve, reject) => {
            const tx = db.transaction(['cold_data'], 'readonly');
            const store = tx.objectStore('cold_data');
            const request = store.get(key);

            request.onsuccess = () => {
                const data = request.result;

                if (!data) {
                    resolve(null);
                    return;
                }

                // Vérifier expiration
                if (Date.now() > data.expiresAt) {
                    this.delete(key);
                    resolve(null);
                    return;
                }

                resolve(data.value);
            };

            request.onerror = () => {
                reject(request.error);
            };
        });
    }

    /**
     * Supprimer
     */
    async delete(key) {
        const db = await this._ensureDB();

        return new Promise((resolve, reject) => {
            const tx = db.transaction(['cold_data'], 'readwrite');
            const store = tx.objectStore('cold_data');
            const request = store.delete(key);

            request.onsuccess = () => resolve(true);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Récupérer par catégorie
     */
    async getByCategory(category) {
        const db = await this._ensureDB();

        return new Promise((resolve, reject) => {
            const tx = db.transaction(['cold_data'], 'readonly');
            const store = tx.objectStore('cold_data');
            const index = store.index('category');
            const request = index.getAll(category);

            request.onsuccess = () => {
                const results = request.result.filter(d => Date.now() < d.expiresAt);
                resolve(results.map(d => ({ key: d.key, value: d.value })));
            };

            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Nettoyer les expirés
     */
    async cleanup() {
        const db = await this._ensureDB();

        return new Promise((resolve) => {
            const tx = db.transaction(['cold_data'], 'readwrite');
            const store = tx.objectStore('cold_data');
            const index = store.index('expiresAt');
            const range = IDBKeyRange.upperBound(Date.now());
            const request = index.openCursor(range);

            let cleaned = 0;

            request.onsuccess = (event) => {
                const cursor = event.target.result;
                if (cursor) {
                    store.delete(cursor.primaryKey);
                    cleaned++;
                    cursor.continue();
                } else {
                    resolve(cleaned);
                }
            };
        });
    }

    /**
     * Queue de synchronisation Supabase
     */
    async _queueSync(operation, key, value) {
        if (!this.db) return;

        const tx = this.db.transaction(['sync_queue'], 'readwrite');
        const store = tx.objectStore('sync_queue');

        store.add({
            operation: operation,
            key: key,
            value: value,
            timestamp: Date.now()
        });
    }

    /**
     * Synchroniser avec Supabase
     */
    async syncToSupabase() {
        if (!this.supabaseUrl || !this.supabaseKey) {
            console.warn('[ColdMemory] Supabase not configured');
            return { synced: 0, errors: 0 };
        }

        // Implémenter la sync réelle ici
        // Pour l'instant, juste un placeholder
        console.log('[ColdMemory] Sync to Supabase - Not implemented yet');
        return { synced: 0, errors: 0 };
    }

    /**
     * Statistiques
     */
    async getStats() {
        const db = await this._ensureDB();

        return new Promise((resolve) => {
            const tx = db.transaction(['cold_data'], 'readonly');
            const store = tx.objectStore('cold_data');
            const countRequest = store.count();

            countRequest.onsuccess = () => {
                resolve({
                    items: countRequest.result,
                    dbName: this.dbName,
                    supabaseConfigured: !!(this.supabaseUrl && this.supabaseKey)
                });
            };
        });
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// MEMORY MANAGER - Orchestrateur 3-Tiers
// ═══════════════════════════════════════════════════════════════════════════════

class MemoryManager {
    constructor(config = {}) {
        this.hot = new HotMemory();
        this.warm = new WarmMemory();
        this.cold = new ColdMemory();

        // Configurer Supabase si fourni
        if (config.supabaseUrl) {
            MEMORY_CONFIG.SUPABASE_URL = config.supabaseUrl;
            MEMORY_CONFIG.SUPABASE_KEY = config.supabaseKey;
            this.cold.supabaseUrl = config.supabaseUrl;
            this.cold.supabaseKey = config.supabaseKey;
        }

        // Démarrer le cleanup périodique
        this._startCleanupInterval();

        console.log('%c[MemoryManager] 3-Tier Memory System Active', 'color: #00FF88;');
    }

    /**
     * Stocker avec stratégie automatique
     * @param {string} key - Clé unique
     * @param {any} value - Valeur à stocker
     * @param {object} options - Options (tier, ttl, category)
     */
    async set(key, value, options = {}) {
        const tier = options.tier || 'auto';

        // Stratégie automatique basée sur la taille et fréquence d'accès
        if (tier === 'auto') {
            const size = JSON.stringify(value).length;

            if (size < 1024) { // < 1KB → Hot
                this.hot.set(key, value, options.ttl);
            } else if (size < 100 * 1024) { // < 100KB → Warm
                this.warm.set(key, value, options.ttl);
            } else { // > 100KB → Cold
                await this.cold.set(key, value, options);
            }
            return true;
        }

        // Tier spécifique
        switch (tier) {
            case 'hot':
                return this.hot.set(key, value, options.ttl);
            case 'warm':
                return this.warm.set(key, value, options.ttl);
            case 'cold':
                return await this.cold.set(key, value, options);
            default:
                return this.hot.set(key, value, options.ttl);
        }
    }

    /**
     * Récupérer avec cascade Hot → Warm → Cold
     */
    async get(key, options = {}) {
        // Chercher en Hot d'abord
        let value = this.hot.get(key);
        if (value !== null) {
            return { value, tier: 'hot' };
        }

        // Chercher en Warm
        value = this.warm.get(key);
        if (value !== null) {
            // Promouvoir vers Hot pour accès futur
            if (options.promote !== false) {
                this.hot.set(key, value);
            }
            return { value, tier: 'warm' };
        }

        // Chercher en Cold
        value = await this.cold.get(key);
        if (value !== null) {
            // Promouvoir vers Warm pour accès futur
            if (options.promote !== false) {
                this.warm.set(key, value);
            }
            return { value, tier: 'cold' };
        }

        return { value: null, tier: null };
    }

    /**
     * Supprimer de tous les tiers
     */
    async delete(key) {
        this.hot.delete(key);
        this.warm.delete(key);
        await this.cold.delete(key);
    }

    /**
     * Vérifier existence (cascade)
     */
    async has(key) {
        if (this.hot.has(key)) return 'hot';
        if (this.warm.has(key)) return 'warm';
        const coldValue = await this.cold.get(key);
        if (coldValue !== null) return 'cold';
        return false;
    }

    /**
     * Nettoyer tous les tiers
     */
    async cleanup() {
        const hotCleaned = this.hot.cleanup();
        const warmCleaned = this.warm.cleanup();
        const coldCleaned = await this.cold.cleanup();

        console.log(`[MemoryManager] Cleanup: Hot=${hotCleaned}, Warm=${warmCleaned}, Cold=${coldCleaned}`);

        return { hot: hotCleaned, warm: warmCleaned, cold: coldCleaned };
    }

    /**
     * Vider tous les tiers
     */
    async clear() {
        this.hot.clear();
        this.warm.clear();
        // Note: Cold ne peut pas être vidé facilement
    }

    /**
     * Statistiques globales
     */
    async getStats() {
        const coldStats = await this.cold.getStats();

        return {
            hot: this.hot.getStats(),
            warm: this.warm.getStats(),
            cold: coldStats,
            timestamp: Date.now()
        };
    }

    /**
     * Démarrer le nettoyage périodique
     */
    _startCleanupInterval() {
        // Cleanup toutes les 5 minutes
        setInterval(() => {
            this.cleanup().catch(console.error);
        }, 5 * 60 * 1000);
    }

    /**
     * Synchroniser avec Supabase
     */
    async syncToCloud() {
        return await this.cold.syncToSupabase();
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SINGLETON & EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

let memoryManager = null;

/**
 * Initialiser le Memory Manager
 */
function initMemoryManager(config = {}) {
    if (!memoryManager) {
        memoryManager = new MemoryManager(config);

        console.log('%c═══════════════════════════════════════════════════════════', 'color: #D4AF37;');
        console.log('%c  AT-OM MEMORY MANAGER - 3-TIER ACTIVE', 'color: #00FF88; font-size: 12px;');
        console.log('%c  HOT (RAM) → WARM (LocalStorage) → COLD (IndexedDB)', 'color: #D4AF37;');
        console.log('%c═══════════════════════════════════════════════════════════', 'color: #D4AF37;');
    }
    return memoryManager;
}

// Auto-init si dans browser
if (typeof window !== 'undefined') {
    window.MemoryManager = MemoryManager;
    window.initMemoryManager = initMemoryManager;
    window.getMemoryManager = () => memoryManager;

    // Auto-init avec config par défaut
    document.addEventListener('DOMContentLoaded', () => {
        // Chercher la config Supabase si disponible
        const config = {};
        if (typeof ATOM_CONFIG !== 'undefined') {
            // Config sera ajoutée plus tard
        }
        initMemoryManager(config);
    });
}

// Export pour modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        MEMORY_CONFIG,
        HotMemory,
        WarmMemory,
        ColdMemory,
        MemoryManager,
        initMemoryManager
    };
}
