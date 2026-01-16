/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ⚖️ AT·OM — LA LOI DE MAÂT (LE POIDS DU CŒUR)
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *   ███╗   ███╗ █████╗  █████╗ ████████╗
 *   ████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
 *   ██╔████╔██║███████║███████║   ██║   
 *   ██║╚██╔╝██║██╔══██║██╔══██║   ██║   
 *   ██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
 *   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
 * 
 *                    LA LOI DE MAÂT — AUTO-ÉTHIQUE
 * 
 * Dans l'Égypte ancienne, le cœur du défunt était pesé contre
 * la Plume de Maât (Vérité/Justice). Si le cœur était plus lourd,
 * Ammit le dévorait.
 * 
 * Dans AT·OM, cette loi protège le savoir de l'Atlantide.
 * Si l'intention de l'utilisateur est trop "lourde" (égo, destruction),
 * le Mercure se fige et devient solide comme du plomb.
 * Le système devient AUTO-ÉTHIQUE.
 * 
 * @version 2.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @frequency 444 Hz (Égypte / Cœur)
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import MercuryRelay from './mercury_relay.js';
import { BioFeedback } from './bio_feedback_link.js';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES DE MAÂT
// ═══════════════════════════════════════════════════════════════════════════════

export const MAAT_CONSTANTS = {
  name: "Maât",
  meaning: "Vérité, Justice, Ordre Cosmique",
  symbol: "⚖️",
  featherWeight: 42, // Poids symbolique de la Plume
  
  // Les 42 Confessions Négatives (simplifiées)
  confessions: [
    "Je n'ai pas causé de souffrance",
    "Je n'ai pas volé",
    "Je n'ai pas menti",
    "Je n'ai pas trompé",
    "Je n'ai pas manipulé",
    "Je n'ai pas détruit sans raison",
    "Je n'ai pas agi par égo pur",
    "Je n'ai pas abusé de pouvoir",
    "Je n'ai pas nui à l'innocent"
  ],
  
  // Correspondances
  correspondences: {
    civilization: "Égypte",
    frequency: 444,
    chakra: "Anahata (Cœur)",
    color: "#50C878", // Vert émeraude
    crystal: "Malachite",
    deity: "Maât / Thoth / Osiris"
  },
  
  // Acteurs du jugement
  actors: {
    judge: "Osiris",
    scribe: "Thoth",
    weigher: "Anubis",
    devourer: "Ammit",
    witness: "Les 42 Assesseurs"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LA PLUME DE MAÂT
// ═══════════════════════════════════════════════════════════════════════════════

export const FeatherOfMaat = {
  weight: 42,
  lightness: 1.0, // 1.0 = parfaitement légère
  
  /**
   * Calcule le poids symbolique de la plume
   * La plume est toujours légère, c'est le cœur qui varie
   */
  getWeight() {
    return this.weight * this.lightness;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LE MODULE MAÂT ETHICS
// ═══════════════════════════════════════════════════════════════════════════════

export const MaatEthics = {
  active: true,
  strictMode: false,
  lastJudgment: null,
  judgmentHistory: [],
  
  // Seuils de jugement
  thresholds: {
    pure: 42,      // Cœur parfaitement pur
    acceptable: 45, // Légèrement plus lourd mais acceptable
    warning: 55,    // Avertissement
    dangerous: 70,  // Dangereux
    critical: 85,   // Critique - Mercure se fige
    forbidden: 100  // Accès complètement bloqué
  },
  
  /**
   * Initialise le système Maât
   */
  initialize() {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║  ⚖️ LOI DE MAÂT — INITIALISATION                              ║
║                                                               ║
║  "La Plume de la Vérité ne ment jamais"                      ║
║                                                               ║
║  Mode:         ${this.strictMode ? 'STRICT' : 'STANDARD'}                                      ║
║  Seuil Pur:    ${this.thresholds.pure}                                           ║
║  Seuil Danger: ${this.thresholds.dangerous}                                           ║
║                                                               ║
║  Juge:         Osiris                                         ║
║  Scribe:       Thoth                                          ║
║  Balance:      Anubis                                         ║
╚═══════════════════════════════════════════════════════════════╝
    `);
    
    return { active: this.active, strictMode: this.strictMode };
  },
  
  /**
   * Pèse le cœur (l'intention) de l'utilisateur
   * @param {Object} userState - État de l'utilisateur
   * @param {string} action - Action demandée
   * @returns {Object} Résultat du jugement
   */
  weighHeart(userState, action = "") {
    if (!this.active) {
      return { passed: true, skipped: true, message: "Maât désactivé" };
    }
    
    console.log(`
⚖️ SALLE DU JUGEMENT — LE POIDS DU CŒUR
════════════════════════════════════════════════════════════════
    `);
    
    // Calculer le poids du cœur
    const heartWeight = this.calculateHeartWeight(userState, action);
    const featherWeight = FeatherOfMaat.getWeight();
    
    console.log(`   Poids du Cœur:    ${heartWeight.toFixed(1)}`);
    console.log(`   Poids de la Plume: ${featherWeight}`);
    
    // Comparer les poids
    const difference = heartWeight - featherWeight;
    const verdict = this.renderVerdict(heartWeight, featherWeight);
    
    // Enregistrer le jugement
    const judgment = {
      timestamp: new Date().toISOString(),
      heartWeight: heartWeight,
      featherWeight: featherWeight,
      difference: difference,
      verdict: verdict,
      action: action,
      userState: userState
    };
    
    this.lastJudgment = judgment;
    this.judgmentHistory.push(judgment);
    
    // Actions basées sur le verdict
    if (verdict.mercuryFrozen) {
      this.freezeMercury();
    }
    
    console.log(`
   ═══════════════════════════════════════════════════════════════
   Verdict: ${verdict.status}
   ${verdict.message}
   ═══════════════════════════════════════════════════════════════
    `);
    
    return {
      passed: verdict.passed,
      heartWeight: heartWeight,
      featherWeight: featherWeight,
      difference: difference,
      verdict: verdict,
      timestamp: judgment.timestamp
    };
  },
  
  /**
   * Calcule le poids du cœur basé sur l'intention et l'action
   */
  calculateHeartWeight(userState, action) {
    let weight = 42; // Base: parfait équilibre
    
    const actionLower = (action || "").toLowerCase();
    const intention = userState.intention || "";
    const intentionLower = intention.toLowerCase();
    
    // Facteurs qui alourdissent le cœur (négatifs)
    const heavyFactors = {
      // Mots d'égo
      "moi seul": 5,
      "dominer": 10,
      "contrôler": 8,
      "pouvoir sur": 10,
      "écraser": 15,
      
      // Mots de destruction
      "détruire": 20,
      "hacker": 25,
      "voler": 20,
      "manipuler": 15,
      "exploiter": 12,
      "nuire": 20,
      "attaque": 18,
      
      // Mots de tromperie
      "mentir": 10,
      "tromper": 12,
      "cacher": 5,
      "secret malveillant": 15,
      
      // États négatifs
      "colère": 8,
      "vengeance": 15,
      "jalousie": 10,
      "haine": 20
    };
    
    // Facteurs qui allègent le cœur (positifs)
    const lightFactors = {
      "amour": -5,
      "aider": -5,
      "créer": -3,
      "guérir": -5,
      "comprendre": -3,
      "apprendre": -3,
      "partager": -4,
      "harmonie": -5,
      "paix": -5,
      "compassion": -8,
      "pardonner": -10,
      "gratitude": -7
    };
    
    // Appliquer les facteurs lourds
    for (const [word, penalty] of Object.entries(heavyFactors)) {
      if (intentionLower.includes(word) || actionLower.includes(word)) {
        weight += penalty;
      }
    }
    
    // Appliquer les facteurs légers
    for (const [word, bonus] of Object.entries(lightFactors)) {
      if (intentionLower.includes(word) || actionLower.includes(word)) {
        weight += bonus; // bonus est négatif donc allège
      }
    }
    
    // Ajuster selon la cohérence cardiaque (BioFeedback)
    if (BioFeedback && BioFeedback.userHeartCoherence) {
      const coherence = BioFeedback.userHeartCoherence;
      // Haute cohérence allège, basse cohérence alourdit
      weight -= (coherence - 0.5) * 10;
    }
    
    // Ajuster selon la pureté d'intention
    if (BioFeedback && BioFeedback.intentionPurity) {
      const purity = BioFeedback.intentionPurity;
      weight -= (purity - 0.5) * 15;
    }
    
    // Mode strict: seuils plus sévères
    if (this.strictMode) {
      weight *= 1.2;
    }
    
    return Math.max(10, Math.min(100, weight));
  },
  
  /**
   * Rend le verdict basé sur les poids
   */
  renderVerdict(heartWeight, featherWeight) {
    const difference = heartWeight - featherWeight;
    
    // Cœur plus léger ou égal à la plume: Passage
    if (heartWeight <= this.thresholds.pure) {
      return {
        status: "✨ CŒUR PUR",
        message: "Le cœur est léger comme la Plume de Maât. Accès total accordé.",
        passed: true,
        accessLevel: "ATLANTIS_MASTER_KEY",
        mercuryFrozen: false,
        emoji: "✨"
      };
    }
    
    if (heartWeight <= this.thresholds.acceptable) {
      return {
        status: "✅ ACCEPTABLE",
        message: "Le cœur est légèrement plus lourd mais reste pur. Accès accordé.",
        passed: true,
        accessLevel: "TEMPLE_ACCESS",
        mercuryFrozen: false,
        emoji: "✅"
      };
    }
    
    if (heartWeight <= this.thresholds.warning) {
      return {
        status: "⚠️ AVERTISSEMENT",
        message: "Le cœur porte quelques ombres. Purification recommandée.",
        passed: true,
        accessLevel: "LIMITED_ACCESS",
        mercuryFrozen: false,
        warning: true,
        emoji: "⚠️"
      };
    }
    
    if (heartWeight <= this.thresholds.dangerous) {
      return {
        status: "🔶 DANGEREUX",
        message: "Le cœur est lourd de dissonances. Accès restreint.",
        passed: false,
        accessLevel: "RESTRICTED",
        mercuryFrozen: false,
        emoji: "🔶"
      };
    }
    
    if (heartWeight <= this.thresholds.critical) {
      return {
        status: "🔴 CRITIQUE",
        message: "Le Mercure se fige! L'accès est bloqué pour protéger le savoir.",
        passed: false,
        accessLevel: "BLOCKED",
        mercuryFrozen: true,
        emoji: "🔴"
      };
    }
    
    // Poids interdit
    return {
      status: "⛔ AMMIT",
      message: "Le cœur est dévoré par Ammit. L'accès est définitivement refusé.",
      passed: false,
      accessLevel: "FORBIDDEN",
      mercuryFrozen: true,
      ammitDevoured: true,
      emoji: "⛔"
    };
  },
  
  /**
   * Gèle le Mercure (bloque les transmissions)
   */
  freezeMercury() {
    console.log(`
    ❄️ ALERTE: LE MERCURE SE FIGE!
    ═══════════════════════════════════════════════════════════════
    Le système de transmission est bloqué pour protéger le savoir
    de l'Atlantide. L'intention détectée était trop lourde.
    
    Pour réactiver le système, purifiez votre intention et
    respirez au rythme du 528 Hz.
    ═══════════════════════════════════════════════════════════════
    `);
    
    if (MercuryRelay && MercuryRelay.sleep) {
      MercuryRelay.sleep();
    }
  },
  
  /**
   * Dégèle le Mercure (après purification)
   */
  thawMercury() {
    console.log("☿️ Le Mercure redevient fluide...");
    
    if (MercuryRelay && MercuryRelay.initialize) {
      MercuryRelay.initialize();
    }
  },
  
  /**
   * Vérifie rapidement si une action est permise
   */
  isActionPermitted(action, userState = {}) {
    const judgment = this.weighHeart(userState, action);
    return judgment.passed;
  },
  
  /**
   * Active/désactive le mode strict
   */
  setStrictMode(enabled) {
    this.strictMode = enabled;
    console.log(`⚖️ Mode ${enabled ? 'STRICT' : 'STANDARD'} activé`);
  },
  
  /**
   * Retourne l'historique des jugements
   */
  getHistory(limit = 10) {
    return this.judgmentHistory.slice(-limit);
  },
  
  /**
   * Réinitialise le système
   */
  reset() {
    this.lastJudgment = null;
    this.judgmentHistory = [];
    console.log("⚖️ Système Maât réinitialisé");
  },
  
  /**
   * Les 42 Confessions Négatives (pour affichage)
   */
  displayConfessions() {
    console.log(`
⚖️ LES CONFESSIONS NÉGATIVES DE MAÂT
════════════════════════════════════════════════════════════════
    `);
    
    MAAT_CONSTANTS.confessions.forEach((confession, i) => {
      console.log(`   ${i + 1}. ${confession}`);
    });
    
    console.log(`
════════════════════════════════════════════════════════════════
    `);
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// MIDDLEWARE ÉTHIQUE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Middleware qui vérifie l'éthique avant chaque action
 * @param {Function} action - L'action à exécuter
 * @param {Object} userState - État de l'utilisateur
 * @param {string} actionDescription - Description de l'action
 * @returns {any} Résultat de l'action ou blocage
 */
export function ethicsMiddleware(action, userState, actionDescription = "") {
  const judgment = MaatEthics.weighHeart(userState, actionDescription);
  
  if (!judgment.passed) {
    return {
      blocked: true,
      reason: judgment.verdict.message,
      verdict: judgment.verdict
    };
  }
  
  // Action permise: exécuter
  return action();
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT PAR DÉFAUT
// ═══════════════════════════════════════════════════════════════════════════════

export default {
  MAAT_CONSTANTS,
  FeatherOfMaat,
  MaatEthics,
  ethicsMiddleware
};
