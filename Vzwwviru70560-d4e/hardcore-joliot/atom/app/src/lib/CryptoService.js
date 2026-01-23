/**
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 *       ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗
 *      ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
 *      ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
 *      ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
 *      ╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
 *       ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝
 *
 *                    SERVICE DE CHIFFREMENT AT·OM
 *              Chiffrement AES-GCM pour données sensibles
 *
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES DE CHIFFREMENT
// ═══════════════════════════════════════════════════════════════════════════════

const ALGORITHM = 'AES-GCM';
const KEY_LENGTH = 256;
const IV_LENGTH = 12;
const SALT_LENGTH = 16;
const ITERATIONS = 100000;
const STORAGE_KEY_PREFIX = 'atom_encrypted_';
const MASTER_KEY_NAME = 'atom_master_key';

// ═══════════════════════════════════════════════════════════════════════════════
// UTILITAIRES DE CONVERSION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Convertit un ArrayBuffer en chaîne Base64
 */
function arrayBufferToBase64(buffer) {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

/**
 * Convertit une chaîne Base64 en ArrayBuffer
 */
function base64ToArrayBuffer(base64) {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
}

/**
 * Génère un sel aléatoire
 */
function generateSalt() {
  return crypto.getRandomValues(new Uint8Array(SALT_LENGTH));
}

/**
 * Génère un vecteur d'initialisation (IV) aléatoire
 */
function generateIV() {
  return crypto.getRandomValues(new Uint8Array(IV_LENGTH));
}

// ═══════════════════════════════════════════════════════════════════════════════
// GESTION DES CLÉS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Dérive une clé à partir d'un mot de passe et d'un sel
 */
async function deriveKey(password, salt) {
  const encoder = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    encoder.encode(password),
    'PBKDF2',
    false,
    ['deriveBits', 'deriveKey']
  );

  return crypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt: salt,
      iterations: ITERATIONS,
      hash: 'SHA-256'
    },
    keyMaterial,
    { name: ALGORITHM, length: KEY_LENGTH },
    false,
    ['encrypt', 'decrypt']
  );
}

/**
 * Génère une clé maître unique pour cette session/navigateur
 */
async function getOrCreateMasterKey() {
  // Utilise un identifiant unique basé sur le navigateur
  const browserFingerprint = [
    navigator.userAgent,
    navigator.language,
    screen.colorDepth,
    new Date().getTimezoneOffset()
  ].join('|');

  // Crée une clé déterministe mais unique à ce navigateur
  const encoder = new TextEncoder();
  const data = encoder.encode(browserFingerprint + '_atom_v76_secure');
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const masterPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

  return masterPassword;
}

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS DE CHIFFREMENT/DÉCHIFFREMENT
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Chiffre des données avec AES-GCM
 * @param {any} data - Données à chiffrer (sera converti en JSON)
 * @param {string} password - Mot de passe optionnel (utilise la clé maître par défaut)
 * @returns {Promise<string>} - Données chiffrées en Base64
 */
async function encrypt(data, password = null) {
  try {
    const masterPassword = password || await getOrCreateMasterKey();
    const salt = generateSalt();
    const iv = generateIV();
    const key = await deriveKey(masterPassword, salt);

    const encoder = new TextEncoder();
    const encodedData = encoder.encode(JSON.stringify(data));

    const encryptedBuffer = await crypto.subtle.encrypt(
      { name: ALGORITHM, iv: iv },
      key,
      encodedData
    );

    // Combine salt + iv + encrypted data
    const combined = new Uint8Array(salt.length + iv.length + encryptedBuffer.byteLength);
    combined.set(salt, 0);
    combined.set(iv, salt.length);
    combined.set(new Uint8Array(encryptedBuffer), salt.length + iv.length);

    return arrayBufferToBase64(combined.buffer);
  } catch (error) {
    console.error('[CRYPTO] Erreur chiffrement:', error);
    throw new Error('Échec du chiffrement des données');
  }
}

/**
 * Déchiffre des données avec AES-GCM
 * @param {string} encryptedData - Données chiffrées en Base64
 * @param {string} password - Mot de passe optionnel (utilise la clé maître par défaut)
 * @returns {Promise<any>} - Données déchiffrées
 */
async function decrypt(encryptedData, password = null) {
  try {
    const masterPassword = password || await getOrCreateMasterKey();
    const combined = new Uint8Array(base64ToArrayBuffer(encryptedData));

    // Extract salt, iv, and encrypted data
    const salt = combined.slice(0, SALT_LENGTH);
    const iv = combined.slice(SALT_LENGTH, SALT_LENGTH + IV_LENGTH);
    const data = combined.slice(SALT_LENGTH + IV_LENGTH);

    const key = await deriveKey(masterPassword, salt);

    const decryptedBuffer = await crypto.subtle.decrypt(
      { name: ALGORITHM, iv: iv },
      key,
      data
    );

    const decoder = new TextDecoder();
    return JSON.parse(decoder.decode(decryptedBuffer));
  } catch (error) {
    console.error('[CRYPTO] Erreur déchiffrement:', error);
    throw new Error('Échec du déchiffrement des données');
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SECURE STORAGE - localStorage CHIFFRÉ
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Service de stockage sécurisé avec chiffrement automatique
 */
class SecureStorage {
  constructor() {
    this.prefix = STORAGE_KEY_PREFIX;
    this.cache = new Map(); // Cache en mémoire pour performance
  }

  /**
   * Stocke des données de manière sécurisée
   * @param {string} key - Clé de stockage
   * @param {any} value - Valeur à stocker
   * @param {object} options - Options { encrypt: true, ttl: null }
   */
  async setItem(key, value, options = { encrypt: true, ttl: null }) {
    try {
      const storageKey = this.prefix + key;
      const storageData = {
        value: options.encrypt ? await encrypt(value) : value,
        encrypted: options.encrypt,
        timestamp: Date.now(),
        ttl: options.ttl
      };

      localStorage.setItem(storageKey, JSON.stringify(storageData));
      this.cache.set(key, { value, timestamp: Date.now() });

      return true;
    } catch (error) {
      console.error('[SECURE_STORAGE] Erreur setItem:', error);
      return false;
    }
  }

  /**
   * Récupère des données stockées de manière sécurisée
   * @param {string} key - Clé de stockage
   * @param {any} defaultValue - Valeur par défaut si non trouvé
   * @returns {Promise<any>}
   */
  async getItem(key, defaultValue = null) {
    try {
      // Vérifie le cache d'abord
      if (this.cache.has(key)) {
        return this.cache.get(key).value;
      }

      const storageKey = this.prefix + key;
      const stored = localStorage.getItem(storageKey);

      if (!stored) return defaultValue;

      const storageData = JSON.parse(stored);

      // Vérifie le TTL
      if (storageData.ttl && Date.now() - storageData.timestamp > storageData.ttl) {
        await this.removeItem(key);
        return defaultValue;
      }

      const value = storageData.encrypted
        ? await decrypt(storageData.value)
        : storageData.value;

      this.cache.set(key, { value, timestamp: Date.now() });
      return value;
    } catch (error) {
      console.error('[SECURE_STORAGE] Erreur getItem:', error);
      return defaultValue;
    }
  }

  /**
   * Supprime des données stockées
   * @param {string} key - Clé de stockage
   */
  async removeItem(key) {
    const storageKey = this.prefix + key;
    localStorage.removeItem(storageKey);
    this.cache.delete(key);
    return true;
  }

  /**
   * Vérifie si une clé existe
   * @param {string} key - Clé de stockage
   */
  hasItem(key) {
    return localStorage.getItem(this.prefix + key) !== null;
  }

  /**
   * Nettoie toutes les données expirées
   */
  async cleanup() {
    const keys = Object.keys(localStorage).filter(k => k.startsWith(this.prefix));

    for (const storageKey of keys) {
      try {
        const stored = JSON.parse(localStorage.getItem(storageKey));
        if (stored.ttl && Date.now() - stored.timestamp > stored.ttl) {
          localStorage.removeItem(storageKey);
        }
      } catch (e) {
        // Ignore les erreurs de parsing
      }
    }
  }

  /**
   * Efface toutes les données sécurisées
   */
  clear() {
    const keys = Object.keys(localStorage).filter(k => k.startsWith(this.prefix));
    keys.forEach(k => localStorage.removeItem(k));
    this.cache.clear();
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SECURE SESSION STORAGE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Service de stockage de session sécurisé (données sensibles à durée de vie courte)
 */
class SecureSessionStorage {
  constructor() {
    this.prefix = 'atom_session_';
  }

  async setItem(key, value) {
    try {
      const encrypted = await encrypt(value);
      sessionStorage.setItem(this.prefix + key, encrypted);
      return true;
    } catch (error) {
      console.error('[SECURE_SESSION] Erreur setItem:', error);
      return false;
    }
  }

  async getItem(key, defaultValue = null) {
    try {
      const stored = sessionStorage.getItem(this.prefix + key);
      if (!stored) return defaultValue;
      return await decrypt(stored);
    } catch (error) {
      console.error('[SECURE_SESSION] Erreur getItem:', error);
      return defaultValue;
    }
  }

  removeItem(key) {
    sessionStorage.removeItem(this.prefix + key);
  }

  clear() {
    const keys = Object.keys(sessionStorage).filter(k => k.startsWith(this.prefix));
    keys.forEach(k => sessionStorage.removeItem(k));
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// UTILITAIRES DE HACHAGE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Génère un hash SHA-256 d'une chaîne
 * @param {string} data - Données à hacher
 * @returns {Promise<string>} - Hash en hexadécimal
 */
async function hash(data) {
  const encoder = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest('SHA-256', encoder.encode(data));
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

/**
 * Génère un identifiant unique sécurisé
 * @param {number} length - Longueur de l'identifiant
 * @returns {string}
 */
function generateSecureId(length = 32) {
  const array = new Uint8Array(length / 2);
  crypto.getRandomValues(array);
  return Array.from(array, b => b.toString(16).padStart(2, '0')).join('');
}

// ═══════════════════════════════════════════════════════════════════════════════
// SANITIZATION DES DONNÉES SENSIBLES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Masque une clé API pour affichage
 * @param {string} key - Clé à masquer
 * @returns {string}
 */
function maskApiKey(key) {
  if (!key || key.length < 8) return '****';
  return key.substring(0, 4) + '****' + key.substring(key.length - 4);
}

/**
 * Nettoie les données sensibles d'un objet d'erreur
 * @param {Error} error - Erreur à nettoyer
 * @returns {object}
 */
function sanitizeError(error) {
  const sanitized = {
    message: error.message || 'Une erreur est survenue',
    timestamp: new Date().toISOString()
  };

  // En production, ne pas inclure le stack trace
  if (process.env.NODE_ENV !== 'production' && error.stack) {
    // Nettoie les chemins de fichiers du stack trace
    sanitized.stack = error.stack
      .replace(/file:\/\/\/[^\s]+/g, '[path]')
      .replace(/at\s+[^\s]+\s+\([^)]+\)/g, 'at [location]')
      .replace(/\/Users\/[^\/]+/g, '/[user]')
      .replace(/C:\\Users\\[^\\]+/g, 'C:\\[user]');
  }

  return sanitized;
}

/**
 * Nettoie les données PII d'un objet
 * @param {object} data - Données à nettoyer
 * @returns {object}
 */
function sanitizePII(data) {
  const piiFields = ['email', 'password', 'phone', 'ssn', 'creditCard', 'apiKey', 'token', 'secret'];
  const sanitized = { ...data };

  for (const field of piiFields) {
    if (sanitized[field]) {
      sanitized[field] = '[REDACTED]';
    }
  }

  // Nettoie récursivement les objets imbriqués
  for (const key in sanitized) {
    if (typeof sanitized[key] === 'object' && sanitized[key] !== null) {
      sanitized[key] = sanitizePII(sanitized[key]);
    }
  }

  return sanitized;
}

// ═══════════════════════════════════════════════════════════════════════════════
// INSTANCES SINGLETON
// ═══════════════════════════════════════════════════════════════════════════════

export const secureStorage = new SecureStorage();
export const secureSession = new SecureSessionStorage();

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export {
  encrypt,
  decrypt,
  hash,
  generateSecureId,
  maskApiKey,
  sanitizeError,
  sanitizePII,
  SecureStorage,
  SecureSessionStorage
};

export default {
  encrypt,
  decrypt,
  hash,
  generateSecureId,
  maskApiKey,
  sanitizeError,
  sanitizePII,
  secureStorage,
  secureSession
};
