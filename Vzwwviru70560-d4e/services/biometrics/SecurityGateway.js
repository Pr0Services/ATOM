/**
 * AT·OM Security Gateway v1.0
 * Passerelle de Sécurité Multi-Couches pour ZAMA IGNITION
 *
 * Gère les permissions d'affichage des modules d'armure
 * basées sur les couches de sécurité biométrique validées.
 *
 * @author AT·OM Collective
 * @version 1.0.0
 */

const crypto = require('crypto');

// ==================== CONSTANTES DE SÉCURITÉ ====================

/**
 * Couches de sécurité disponibles
 */
const SECURITY_LAYERS = {
  GEOMETRY: {
    level: 1,
    name: 'Géométrie Sacrée',
    description: 'Mesures M, P, I, Po basées sur le ratio Phi',
    visibility: 'public',
    required: true
  },
  OCULAR: {
    level: 2,
    name: 'Biométrie Oculaire',
    description: 'Scan de l\'iris pour déverrouillage Phase 3',
    visibility: 'private',
    required: false
  },
  FINGERPRINT: {
    level: 3,
    name: 'Empreinte Digitale',
    description: 'Signature des transactions Hedera',
    visibility: 'private',
    required: false
  },
  BIORESONANCE: {
    level: 4,
    name: 'Bio-Résonance',
    description: 'Synchronisation BPM pour animation temps réel',
    visibility: 'private',
    required: false
  }
};

/**
 * Modules de l'armure et leurs exigences de sécurité
 */
const ARMOR_MODULES = {
  CUBE_METATRON: {
    name: 'Cube de Métatron',
    phase: 1,
    requiredLayers: ['GEOMETRY'],
    visibility: 'public'
  },
  FLEUR_DE_VIE: {
    name: 'Fleur de Vie',
    phase: 1,
    requiredLayers: ['GEOMETRY'],
    visibility: 'public',
    animation: {
      requires: 'BIORESONANCE',
      fallback: 'static'
    }
  },
  TRISKEL: {
    name: 'Triskel',
    phase: 2,
    requiredLayers: ['GEOMETRY'],
    visibility: 'public'
  },
  SCEAU_PROTECTION: {
    name: 'Sceau de Protection',
    phase: 2,
    requiredLayers: ['GEOMETRY'],
    visibility: 'semi-private',
    verificationRequired: true
  },
  OEIL_HORUS: {
    name: 'Œil d\'Horus',
    phase: 3,
    requiredLayers: ['GEOMETRY', 'OCULAR'],
    visibility: 'private'
  }
};

// ==================== CLASSE PRINCIPALE ====================

/**
 * Gestionnaire de sécurité multi-couches
 */
class SecurityGateway {
  constructor(options = {}) {
    this.userId = options.userId || null;
    this.activatedLayers = new Set();
    this.validationProofs = {};
    this.sessionKey = null;
    this.createdAt = new Date();
    this.lastActivity = new Date();

    // Initialiser avec la couche de base
    if (options.geometryValidated) {
      this.activateLayer('GEOMETRY', options.geometryProof);
    }
  }

  // ==================== GESTION DES COUCHES ====================

  /**
   * Active une couche de sécurité avec preuve de validation
   *
   * @param {string} layerName - Nom de la couche
   * @param {Object} proof - Preuve de validation
   * @returns {Object} Résultat de l'activation
   */
  activateLayer(layerName, proof = {}) {
    const layer = SECURITY_LAYERS[layerName];

    if (!layer) {
      throw new Error(`Couche de sécurité inconnue: ${layerName}`);
    }

    // Vérifier les prérequis
    if (layerName !== 'GEOMETRY' && !this.activatedLayers.has('GEOMETRY')) {
      throw new Error('La couche GEOMETRY doit être activée en premier');
    }

    // Générer la preuve d'activation
    const activationProof = {
      layer: layerName,
      activatedAt: new Date().toISOString(),
      proofHash: this._generateProofHash(layerName, proof),
      ...proof
    };

    this.activatedLayers.add(layerName);
    this.validationProofs[layerName] = activationProof;
    this.lastActivity = new Date();

    // Générer une clé de session si c'est la première activation
    if (!this.sessionKey) {
      this.sessionKey = this._generateSessionKey();
    }

    return {
      success: true,
      layer: layer.name,
      level: layer.level,
      totalLayers: this.activatedLayers.size,
      unlockedModules: this.getUnlockedModules()
    };
  }

  /**
   * Désactive une couche de sécurité
   *
   * @param {string} layerName - Nom de la couche
   * @returns {boolean} Succès de la désactivation
   */
  deactivateLayer(layerName) {
    if (layerName === 'GEOMETRY') {
      throw new Error('La couche GEOMETRY ne peut pas être désactivée');
    }

    if (this.activatedLayers.has(layerName)) {
      this.activatedLayers.delete(layerName);
      delete this.validationProofs[layerName];
      return true;
    }

    return false;
  }

  /**
   * Vérifie si une couche est activée
   *
   * @param {string} layerName - Nom de la couche
   * @returns {boolean}
   */
  isLayerActive(layerName) {
    return this.activatedLayers.has(layerName);
  }

  // ==================== GESTION DES MODULES ====================

  /**
   * Vérifie si un module est déverrouillé
   *
   * @param {string} moduleName - Nom du module
   * @returns {Object} Statut du module
   */
  checkModuleAccess(moduleName) {
    const module = ARMOR_MODULES[moduleName];

    if (!module) {
      throw new Error(`Module inconnu: ${moduleName}`);
    }

    const requiredLayers = module.requiredLayers;
    const missingLayers = requiredLayers.filter(l => !this.activatedLayers.has(l));

    const unlocked = missingLayers.length === 0;

    return {
      module: module.name,
      phase: module.phase,
      unlocked,
      visibility: unlocked ? module.visibility : 'locked',
      missingLayers: missingLayers.map(l => SECURITY_LAYERS[l].name),
      animation: this._checkAnimationAccess(module)
    };
  }

  /**
   * Vérifie l'accès aux animations d'un module
   *
   * @param {Object} module - Configuration du module
   * @returns {Object} Statut de l'animation
   */
  _checkAnimationAccess(module) {
    if (!module.animation) {
      return { mode: 'static', available: true };
    }

    const animationLayer = module.animation.requires;
    const hasAccess = this.activatedLayers.has(animationLayer);

    return {
      mode: hasAccess ? 'dynamic' : module.animation.fallback,
      available: true,
      syncRequired: animationLayer
    };
  }

  /**
   * Retourne la liste des modules déverrouillés
   *
   * @returns {Array} Modules accessibles
   */
  getUnlockedModules() {
    const unlocked = [];

    for (const [name, module] of Object.entries(ARMOR_MODULES)) {
      const access = this.checkModuleAccess(name);
      if (access.unlocked) {
        unlocked.push({
          id: name,
          ...access
        });
      }
    }

    return unlocked;
  }

  /**
   * Retourne la liste des modules verrouillés
   *
   * @returns {Array} Modules inaccessibles avec instructions
   */
  getLockedModules() {
    const locked = [];

    for (const [name, module] of Object.entries(ARMOR_MODULES)) {
      const access = this.checkModuleAccess(name);
      if (!access.unlocked) {
        locked.push({
          id: name,
          ...access,
          unlockInstructions: this._getUnlockInstructions(access.missingLayers)
        });
      }
    }

    return locked;
  }

  /**
   * Génère les instructions pour débloquer les couches manquantes
   *
   * @param {Array} missingLayers - Couches manquantes
   * @returns {Array} Instructions
   */
  _getUnlockInstructions(missingLayers) {
    return missingLayers.map(layerName => {
      const layer = Object.values(SECURITY_LAYERS).find(l => l.name === layerName);
      return {
        layer: layerName,
        action: this._getLayerUnlockAction(layer)
      };
    });
  }

  /**
   * Retourne l'action requise pour débloquer une couche
   *
   * @param {Object} layer - Configuration de la couche
   * @returns {string} Action à effectuer
   */
  _getLayerUnlockAction(layer) {
    const actions = {
      'Géométrie Sacrée': 'Calibrez vos mesures biométriques (M, P, I, Po)',
      'Biométrie Oculaire': 'Effectuez un scan de votre iris',
      'Empreinte Digitale': 'Enregistrez votre empreinte digitale',
      'Bio-Résonance': 'Connectez un capteur de fréquence cardiaque'
    };

    return actions[layer?.name] || 'Action non définie';
  }

  // ==================== GÉNÉRATION DE PREUVES ====================

  /**
   * Génère un hash de preuve pour une couche
   *
   * @param {string} layerName - Nom de la couche
   * @param {Object} data - Données à hasher
   * @returns {string} Hash SHA-256
   */
  _generateProofHash(layerName, data) {
    const content = JSON.stringify({
      layer: layerName,
      userId: this.userId,
      data,
      timestamp: Date.now()
    });

    return crypto.createHash('sha256').update(content).digest('hex');
  }

  /**
   * Génère une clé de session unique
   *
   * @returns {string} Clé de session
   */
  _generateSessionKey() {
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Génère les métadonnées pour le token Hedera
   *
   * @returns {Object} Métadonnées de sécurité
   */
  generateHederaMetadata() {
    return {
      securityLayers: Array.from(this.activatedLayers),
      layerCount: this.activatedLayers.size,
      proofs: Object.entries(this.validationProofs).map(([layer, proof]) => ({
        layer,
        hash: proof.proofHash,
        activatedAt: proof.activatedAt
      })),
      unlockedModules: this.getUnlockedModules().map(m => m.id),
      sessionKey: this.sessionKey,
      createdAt: this.createdAt.toISOString()
    };
  }

  // ==================== VALIDATION HUMAN-IN-THE-LOOP ====================

  /**
   * Vérifie si une validation utilisateur est requise
   *
   * @param {string} action - Action à effectuer
   * @returns {Object} Exigences de validation
   */
  requiresHumanValidation(action) {
    const sensitiveActions = [
      'seal_measures',      // Sceller les mesures biométriques
      'mint_token',         // Créer le token NFT
      'unlock_phase3',      // Débloquer la phase 3
      'transfer_token'      // Transférer l'armure
    ];

    return {
      required: sensitiveActions.includes(action),
      action,
      prompt: this._getValidationPrompt(action)
    };
  }

  /**
   * Retourne le message de validation pour une action
   *
   * @param {string} action - Action concernée
   * @returns {string} Message de confirmation
   */
  _getValidationPrompt(action) {
    const prompts = {
      seal_measures: 'Confirmez-vous que les mesures affichées correspondent à votre corps ?',
      mint_token: 'Voulez-vous graver définitivement cette armure sur la blockchain Hedera ?',
      unlock_phase3: 'Activez-vous le déverrouillage des Senseurs (Œil d\'Horus) ?',
      transfer_token: 'Confirmez-vous le transfert de votre armure à un autre porteur ?'
    };

    return prompts[action] || 'Confirmez-vous cette action ?';
  }

  // ==================== ÉTAT DE LA GATEWAY ====================

  /**
   * Retourne l'état complet de la gateway
   *
   * @returns {Object} État actuel
   */
  getState() {
    return {
      userId: this.userId,
      sessionKey: this.sessionKey,
      activatedLayers: Array.from(this.activatedLayers),
      layerDetails: Array.from(this.activatedLayers).map(l => ({
        id: l,
        ...SECURITY_LAYERS[l],
        proof: this.validationProofs[l]?.proofHash
      })),
      unlockedModules: this.getUnlockedModules(),
      lockedModules: this.getLockedModules(),
      securityScore: this._calculateSecurityScore(),
      createdAt: this.createdAt.toISOString(),
      lastActivity: this.lastActivity.toISOString()
    };
  }

  /**
   * Calcule le score de sécurité global
   *
   * @returns {number} Score de 0 à 100
   */
  _calculateSecurityScore() {
    const maxLayers = Object.keys(SECURITY_LAYERS).length;
    const activeLayers = this.activatedLayers.size;

    return Math.round((activeLayers / maxLayers) * 100);
  }
}

// ==================== FACTORY FUNCTION ====================

/**
 * Crée une nouvelle instance de SecurityGateway
 *
 * @param {Object} options - Options de configuration
 * @returns {SecurityGateway}
 */
function createSecurityGateway(options = {}) {
  return new SecurityGateway(options);
}

// ==================== EXPORTS ====================

module.exports = {
  SecurityGateway,
  createSecurityGateway,
  SECURITY_LAYERS,
  ARMOR_MODULES
};

// ==================== EXEMPLE D'UTILISATION ====================

if (require.main === module) {
  console.log('\n═══════════════════════════════════════════════════════════════');
  console.log('           AT·OM SECURITY GATEWAY - DÉMONSTRATION               ');
  console.log('═══════════════════════════════════════════════════════════════\n');

  // Créer la gateway
  const gateway = new SecurityGateway({
    userId: 'user_123',
    geometryValidated: true,
    geometryProof: { M: 2.1, P: 8.5, I: 7.2, Po: 9.5 }
  });

  console.log('COUCHE 1 - GÉOMÉTRIE ACTIVÉE');
  console.log('────────────────────────────────────────────────────────────────');

  let state = gateway.getState();
  console.log(`  Couches actives: ${state.activatedLayers.join(', ')}`);
  console.log(`  Score sécurité: ${state.securityScore}%`);
  console.log(`  Modules déverrouillés: ${state.unlockedModules.length}`);

  // Activer la couche oculaire
  console.log('\nACTIVATION COUCHE 2 - BIOMÉTRIE OCULAIRE');
  console.log('────────────────────────────────────────────────────────────────');

  gateway.activateLayer('OCULAR', {
    irisHash: 'sha256_iris_sample_hash',
    scanDate: new Date().toISOString()
  });

  state = gateway.getState();
  console.log(`  Couches actives: ${state.activatedLayers.join(', ')}`);
  console.log(`  Score sécurité: ${state.securityScore}%`);

  // Vérifier l'accès à l'Œil d'Horus
  const oeilAccess = gateway.checkModuleAccess('OEIL_HORUS');
  console.log(`\n  Œil d'Horus déverrouillé: ${oeilAccess.unlocked ? 'OUI' : 'NON'}`);

  // Afficher les métadonnées Hedera
  console.log('\nMÉTADONNÉES HEDERA:');
  console.log('────────────────────────────────────────────────────────────────');
  const metadata = gateway.generateHederaMetadata();
  console.log(JSON.stringify(metadata, null, 2));

  console.log('\n═══════════════════════════════════════════════════════════════\n');
}
