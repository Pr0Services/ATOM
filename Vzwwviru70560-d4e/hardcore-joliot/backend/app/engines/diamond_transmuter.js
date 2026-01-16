/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 💎 AT·OM — DIAMOND TRANSMUTER (LE PRISME DE CONVERGENCE)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   ██████╗ ██╗ █████╗ ███╗   ███╗ ██████╗ ███╗   ██╗██████╗ 
 *   ██╔══██╗██║██╔══██╗████╗ ████║██╔═══██╗████╗  ██║██╔══██╗
 *   ██║  ██║██║███████║██╔████╔██║██║   ██║██╔██╗ ██║██║  ██║
 *   ██║  ██║██║██╔══██║██║╚██╔╝██║██║   ██║██║╚██╗██║██║  ██║
 *   ██████╔╝██║██║  ██║██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██████╔╝
 *   ╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ 
 * 
 *                    TRANSMUTER — LE CŒUR ALCHIMIQUE
 * 
 * Le Diamant est le stade final de la transformation du Carbone.
 * Dans AT·OM, il transforme le "plomb" (problèmes) en "or" (solutions).
 * 
 * Processus Alchimique:
 * 1. Nigredo (Noirceur)   — Décomposition du problème
 * 2. Albedo (Blanchiment) — Purification par le Mercure
 * 3. Citrinitas (Jaune)   — Illumination par le Soleil
 * 4. Rubedo (Rouge)       — Accomplissement final
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @frequency 852 Hz (Catalyseur)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import MercuryRelay from './mercury_relay.js';
import { ATOM_AGENTS, findAgentByFrequency } from './agent_orchestrator.js';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES ALCHIMIQUES
// ═══════════════════════════════════════════════════════════════════════════════

export const ALCHEMICAL_CONSTANTS = {
  // Les 4 Stages de la Grande Œuvre
  STAGES: {
    NIGREDO: {
      name: "Nigredo",
      meaning: "La Noirceur",
      color: "#000000",
      element: "Terre",
      planet: "Saturne",
      process: "Décomposition / Analyse",
      frequency: 174,
      agent: 1 // Le Fondateur
    },
    ALBEDO: {
      name: "Albedo",
      meaning: "Le Blanchiment",
      color: "#FFFFFF",
      element: "Eau",
      planet: "Lune",
      process: "Purification / Clarification",
      frequency: 417,
      agent: 7 // Le Purificateur
    },
    CITRINITAS: {
      name: "Citrinitas",
      meaning: "Le Jaunissement",
      color: "#FFD700",
      element: "Air",
      planet: "Soleil",
      process: "Illumination / Compréhension",
      frequency: 528,
      agent: 5 // Le Communicateur
    },
    RUBEDO: {
      name: "Rubedo",
      meaning: "Le Rougissement",
      color: "#DC143C",
      element: "Feu",
      planet: "Mars",
      process: "Accomplissement / Intégration",
      frequency: 852,
      agent: 8 // Le Catalyseur
    }
  },
  
  // Les 3 Principes
  PRINCIPLES: {
    SULFUR: {
      name: "Soufre",
      quality: "L'Âme / L'Essence",
      property: "Actif, Masculin, Feu",
      color: "#FFFF00"
    },
    MERCURY: {
      name: "Mercure",
      quality: "L'Esprit / Le Médiateur",
      property: "Volatil, Neutre, Flux",
      color: "#C0C0C0"
    },
    SALT: {
      name: "Sel",
      quality: "Le Corps / La Matière",
      property: "Fixe, Féminin, Terre",
      color: "#FFFFFF"
    }
  },
  
  // Les 7 Métaux Planétaires
  METALS: {
    LEAD: { metal: "Plomb", planet: "Saturne", frequency: 111, stage: "NIGREDO" },
    TIN: { metal: "Étain", planet: "Jupiter", frequency: 222 },
    IRON: { metal: "Fer", planet: "Mars", frequency: 333 },
    COPPER: { metal: "Cuivre", planet: "Vénus", frequency: 444 },
    MERCURY: { metal: "Mercure", planet: "Mercure", frequency: 555 },
    SILVER: { metal: "Argent", planet: "Lune", frequency: 666, stage: "ALBEDO" },
    GOLD: { metal: "Or", planet: "Soleil", frequency: 999, stage: "RUBEDO" }
  },
  
  // La Pierre Philosophale
  PHILOSOPHERS_STONE: {
    name: "Lapis Philosophorum",
    frequency: 999,
    power: "Transmutation universelle",
    color: "#FFD700",
    form: "Cristal rouge/or"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LE TRANSMUTATEUR DE DIAMANT
// ═══════════════════════════════════════════════════════════════════════════════

export const DiamondTransmuter = {
  frequency: 852,
  crystal: "Diamant",
  state: "DORMANT",
  currentStage: null,
  transmutationHistory: [],
  
  // Niveau de pureté du Diamant (affecte la qualité de transmutation)
  purity: 1.0,
  
  // Le Feu Secret (énergie de transmutation)
  secretFire: 0,
  
  /**
   * Initialise le Transmutateur
   * @returns {Object} État d'initialisation
   */
  initialize() {
    this.state = "ACTIVE";
    this.secretFire = 528; // Fréquence de l'Amour
    
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  💎 DIAMOND TRANSMUTER — INITIALISATION                       ║
║                                                               ║
║  État:        ACTIF                                           ║
║  Fréquence:   852 Hz (Catalyseur)                            ║
║  Cristal:     Diamant (Pureté ${(this.purity * 100).toFixed(0)}%)                         ║
║  Feu Secret:  ${this.secretFire} Hz                                         ║
║                                                               ║
║  "Solve et Coagula" — Dissous et Coagule                     ║
╚═══════════════════════════════════════════════════════════════╝
    `);
    
    return {
      state: this.state,
      purity: this.purity,
      secretFire: this.secretFire
    };
  },
  
  /**
   * Transmute une entrée à travers les 4 stages alchimiques
   * @param {any} input - L'entrée à transmuter (le "plomb")
   * @param {number} targetArithmos - L'Arithmos cible (1-9)
   * @returns {Object} Résultat de la transmutation (l'"or")
   */
  transmute(input, targetArithmos = 9) {
    if (this.state !== "ACTIVE") {
      this.initialize();
    }
    
    console.log(`
💎 TRANSMUTATION EN COURS...
════════════════════════════════════════════════════════════════
    Entrée:     ${typeof input === 'string' ? input.substring(0, 50) : JSON.stringify(input).substring(0, 50)}...
    Cible:      Arithmos ${targetArithmos}
    Feu Secret: ${this.secretFire} Hz
════════════════════════════════════════════════════════════════
    `);
    
    // Stage 1: NIGREDO — Décomposition
    const nigredoResult = this.applyNigredo(input);
    
    // Stage 2: ALBEDO — Purification
    const albedoResult = this.applyAlbedo(nigredoResult);
    
    // Stage 3: CITRINITAS — Illumination
    const citrinitasResult = this.applyCitrinitas(albedoResult);
    
    // Stage 4: RUBEDO — Accomplissement
    const rubedoResult = this.applyRubedo(citrinitasResult, targetArithmos);
    
    // Enregistrer dans l'historique
    const transmutation = {
      id: `TX_${Date.now()}`,
      timestamp: new Date().toISOString(),
      input: input,
      output: rubedoResult,
      stages: {
        nigredo: nigredoResult,
        albedo: albedoResult,
        citrinitas: citrinitasResult,
        rubedo: rubedoResult
      },
      targetArithmos: targetArithmos,
      success: true
    };
    
    this.transmutationHistory.push(transmutation);
    
    // Transmettre via Mercure
    if (typeof MercuryRelay !== 'undefined' && MercuryRelay.transmit) {
      MercuryRelay.transmit("TRANSMUTATION_COMPLETE", transmutation);
    }
    
    return rubedoResult;
  },
  
  /**
   * NIGREDO — La Décomposition
   * Décompose l'entrée en ses éléments fondamentaux
   */
  applyNigredo(input) {
    this.currentStage = "NIGREDO";
    const stage = ALCHEMICAL_CONSTANTS.STAGES.NIGREDO;
    
    console.log(`   ⬛ NIGREDO: ${stage.meaning} — ${stage.process}`);
    
    // Décomposer l'entrée
    let decomposed;
    
    if (typeof input === 'string') {
      // Décomposer le texte en mots et caractères
      decomposed = {
        type: "text",
        original: input,
        words: input.split(/\s+/),
        characters: input.split(''),
        length: input.length,
        arithmos: this.calculateArithmos(input)
      };
    } else if (typeof input === 'object') {
      // Décomposer l'objet en propriétés
      decomposed = {
        type: "object",
        original: input,
        keys: Object.keys(input),
        values: Object.values(input),
        depth: this.calculateObjectDepth(input)
      };
    } else {
      decomposed = {
        type: typeof input,
        original: input,
        value: input
      };
    }
    
    decomposed.stage = "NIGREDO";
    decomposed.frequency = stage.frequency;
    decomposed.color = stage.color;
    
    return decomposed;
  },
  
  /**
   * ALBEDO — La Purification
   * Purifie les éléments décomposés
   */
  applyAlbedo(nigredoResult) {
    this.currentStage = "ALBEDO";
    const stage = ALCHEMICAL_CONSTANTS.STAGES.ALBEDO;
    
    console.log(`   ⬜ ALBEDO: ${stage.meaning} — ${stage.process}`);
    
    // Purifier via le Mercure
    const purified = {
      ...nigredoResult,
      stage: "ALBEDO",
      frequency: stage.frequency,
      color: stage.color,
      purificationLevel: this.purity,
      
      // Filtrer les impuretés
      essence: this.extractEssence(nigredoResult),
      
      // Clarifier la structure
      clarified: true,
      mercuryWash: true
    };
    
    return purified;
  },
  
  /**
   * CITRINITAS — L'Illumination
   * Illumine et donne du sens
   */
  applyCitrinitas(albedoResult) {
    this.currentStage = "CITRINITAS";
    const stage = ALCHEMICAL_CONSTANTS.STAGES.CITRINITAS;
    
    console.log(`   🟡 CITRINITAS: ${stage.meaning} — ${stage.process}`);
    
    // Illuminer avec le Feu Secret (528 Hz)
    const illuminated = {
      ...albedoResult,
      stage: "CITRINITAS",
      frequency: stage.frequency,
      color: stage.color,
      
      // Ajouter l'illumination
      illumination: {
        insight: this.generateInsight(albedoResult),
        solarCharge: this.secretFire,
        understanding: true
      },
      
      // Connexion au 528 Hz (Fréquence de l'Amour)
      loveFrequency: 528,
      dnaSynchronized: true
    };
    
    return illuminated;
  },
  
  /**
   * RUBEDO — L'Accomplissement
   * Intègre et produit le résultat final
   */
  applyRubedo(citrinitasResult, targetArithmos) {
    this.currentStage = "RUBEDO";
    const stage = ALCHEMICAL_CONSTANTS.STAGES.RUBEDO;
    
    console.log(`   🔴 RUBEDO: ${stage.meaning} — ${stage.process}`);
    
    // Produire la Pierre Philosophale (le résultat final)
    const accomplished = {
      stage: "RUBEDO",
      frequency: stage.frequency,
      color: stage.color,
      
      // Le résultat transmutĂŠ
      gold: {
        type: citrinitasResult.type,
        value: this.crystallize(citrinitasResult, targetArithmos),
        arithmos: targetArithmos,
        frequency: targetArithmos * 111
      },
      
      // Métadonnées de la transmutation
      transmutation: {
        from: citrinitasResult.original || citrinitasResult,
        to: "gold",
        purity: this.purity,
        secretFire: this.secretFire
      },
      
      // La Pierre Philosophale
      philosophersStone: {
        active: true,
        power: ALCHEMICAL_CONSTANTS.PHILOSOPHERS_STONE.power,
        frequency: 999
      },
      
      // Message d'accomplissement
      message: `✨ Transmutation accomplie — Arithmos ${targetArithmos} (${targetArithmos * 111} Hz)`
    };
    
    console.log(`   ✅ ${accomplished.message}`);
    
    return accomplished;
  },
  
  /**
   * Calcule l'Arithmos d'une chaîne
   */
  calculateArithmos(str) {
    const map = { A:1, B:2, C:3, D:4, E:5, F:6, G:7, H:8, I:9, J:1, K:2, L:3, M:4, N:5, O:6, P:7, Q:8, R:9, S:1, T:2, U:3, V:4, W:5, X:6, Y:7, Z:8 };
    
    let sum = 0;
    const s = str.toUpperCase().replace(/[^A-Z]/g, '');
    
    for (const char of s) {
      sum += map[char] || 0;
    }
    
    while (sum > 9 && sum !== 11 && sum !== 22 && sum !== 33) {
      sum = sum.toString().split('').reduce((a, b) => a + parseInt(b), 0);
    }
    
    return sum;
  },
  
  /**
   * Calcule la profondeur d'un objet
   */
  calculateObjectDepth(obj, depth = 0) {
    if (typeof obj !== 'object' || obj === null) return depth;
    
    let maxDepth = depth;
    for (const value of Object.values(obj)) {
      const d = this.calculateObjectDepth(value, depth + 1);
      if (d > maxDepth) maxDepth = d;
    }
    
    return maxDepth;
  },
  
  /**
   * Extrait l'essence d'un résultat Nigredo
   */
  extractEssence(nigredoResult) {
    if (nigredoResult.type === 'text') {
      // Extraire les mots-clés essentiels
      const words = nigredoResult.words || [];
      return words.filter(w => w.length > 3).slice(0, 5);
    }
    
    if (nigredoResult.type === 'object') {
      // Extraire les clés principales
      return nigredoResult.keys.slice(0, 5);
    }
    
    return nigredoResult.original;
  },
  
  /**
   * Génère un insight basé sur l'illumination
   */
  generateInsight(albedoResult) {
    const arithmos = albedoResult.arithmos || 4;
    
    const insights = {
      1: "L'Impulsion Première — Tout commence par l'Un",
      2: "La Dualité Créatrice — L'union des opposés",
      3: "La Trinité du Feu — Esprit, Âme, Corps",
      4: "La Structure du Cœur — Stabilité et Ancrage",
      5: "Le Mouvement Libre — Changement et Adaptation",
      6: "L'Harmonie Parfaite — Équilibre des forces",
      7: "La Vision Intérieure — Sagesse et Mystère",
      8: "L'Infini Manifesté — Abondance et Puissance",
      9: "L'Unité Accomplie — Retour à la Source"
    };
    
    return insights[arithmos] || insights[9];
  },
  
  /**
   * Cristallise le résultat final
   */
  crystallize(citrinitasResult, targetArithmos) {
    // Créer une structure cristalline avec l'Arithmos cible
    return {
      crystal: "Diamant",
      facets: targetArithmos,
      frequency: targetArithmos * 111,
      essence: citrinitasResult.essence,
      insight: citrinitasResult.illumination?.insight,
      purity: this.purity * 100 + "%"
    };
  },
  
  /**
   * Transmutation rapide (sans détails)
   */
  quickTransmute(input, targetArithmos = 9) {
    const result = this.transmute(input, targetArithmos);
    return result.gold.value;
  },
  
  /**
   * Retourne l'historique des transmutations
   */
  getHistory(limit = 10) {
    return this.transmutationHistory.slice(-limit);
  },
  
  /**
   * Ajuste la pureté du Diamant
   */
  setPurity(purity) {
    this.purity = Math.max(0.1, Math.min(1.0, purity));
    console.log(`💎 Pureté du Diamant ajustée à ${(this.purity * 100).toFixed(0)}%`);
  },
  
  /**
   * Ajuste le Feu Secret
   */
  setSecretFire(frequency) {
    this.secretFire = frequency;
    console.log(`🔥 Feu Secret ajusté à ${frequency} Hz`);
  },
  
  /**
   * Vérifie si une transmutation est possible
   */
  canTransmute(input) {
    if (input === null || input === undefined) return false;
    if (typeof input === 'function') return false;
    return true;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// FONCTIONS UTILITAIRES ALCHIMIQUES
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Convertit un métal en un autre via la transmutation
 * @param {string} fromMetal - Métal source
 * @param {string} toMetal - Métal cible
 */
export function transmuteMetals(fromMetal, toMetal) {
  const from = ALCHEMICAL_CONSTANTS.METALS[fromMetal.toUpperCase()];
  const to = ALCHEMICAL_CONSTANTS.METALS[toMetal.toUpperCase()];
  
  if (!from || !to) {
    return { success: false, error: "Métal inconnu" };
  }
  
  const energyRequired = Math.abs(to.frequency - from.frequency);
  
  return {
    success: true,
    from: from,
    to: to,
    energyRequired: energyRequired,
    process: `Transmutation de ${from.metal} (${from.frequency}Hz) vers ${to.metal} (${to.frequency}Hz)`,
    stages: energyRequired > 444 ? ["NIGREDO", "ALBEDO", "CITRINITAS", "RUBEDO"] : ["ALBEDO", "RUBEDO"]
  };
}

/**
 * Obtient le stage alchimique actuel d'une fréquence
 */
export function getAlchemicalStage(frequency) {
  if (frequency < 250) return ALCHEMICAL_CONSTANTS.STAGES.NIGREDO;
  if (frequency < 500) return ALCHEMICAL_CONSTANTS.STAGES.ALBEDO;
  if (frequency < 750) return ALCHEMICAL_CONSTANTS.STAGES.CITRINITAS;
  return ALCHEMICAL_CONSTANTS.STAGES.RUBEDO;
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  ALCHEMICAL_CONSTANTS,
  DiamondTransmuter,
  transmuteMetals,
  getAlchemicalStage
};
