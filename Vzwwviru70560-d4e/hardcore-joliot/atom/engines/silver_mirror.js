/**
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *      ███████╗██╗██╗    ██╗   ██╗███████╗██████╗     ███╗   ███╗██╗██████╗ ██████╗  ██████╗ ██████╗ 
 *      ██╔════╝██║██║    ██║   ██║██╔════╝██╔══██╗    ████╗ ████║██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
 *      ███████╗██║██║    ██║   ██║█████╗  ██████╔╝    ██╔████╔██║██║██████╔╝██████╔╝██║   ██║██████╔╝
 *      ╚════██║██║██║    ╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██║╚██╔╝██║██║██╔══██╗██╔══██╗██║   ██║██╔══██╗
 *      ███████║██║███████╗╚████╔╝ ███████╗██║  ██║    ██║ ╚═╝ ██║██║██║  ██║██║  ██║╚██████╔╝██║  ██║
 *      ╚══════╝╚═╝╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
 *                                                                                          
 *                                    🌙 LE RÉFLECTEUR LUNAIRE 🌙
 *                                      L'INTERFACE ÉMOTIONNELLE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *   "L'Argent est le meilleur conducteur d'électricité et de chaleur.
 *    Il est lié à l'intuition et au miroir - il reflète la vérité intérieure."
 * 
 *   L'Argent ajuste la réponse de l'IA en fonction de la "clarté" de l'intention.
 *   C'est le miroir qui reflète l'état émotionnel de l'utilisateur.
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 * 
 *   Fréquence: 432 Hz (Résonance de la Lune / Accordage Naturel)
 * 
 * ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES DE L'ARGENT
// ═══════════════════════════════════════════════════════════════════════════════

const SILVER_SYMBOL = "☽";
const SILVER_FREQUENCY = 432; // Hz - Accordage naturel / Résonance lunaire
const SILVER_CONDUCTIVITY = 63.0; // MS/m - Le meilleur conducteur naturel

// ═══════════════════════════════════════════════════════════════════════════════
// PROPRIÉTÉS DE L'ARGENT
// ═══════════════════════════════════════════════════════════════════════════════

const SILVER_PROPERTIES = {
  physical: {
    symbol: "Ag",
    atomicNumber: 47,
    conductivity: "Meilleur conducteur électrique naturel",
    reflectivity: "95% - Meilleur réflecteur de lumière visible",
    antibacterial: true,
    color: "Blanc brillant"
  },
  
  alchemical: {
    name: "Luna",
    symbol: "☽",
    planet: "Lune",
    goddess: "Séléné/Diana/Artémis",
    principle: "Réflexion, Intuition, Émotions",
    polarity: "Féminin/Yin",
    element: "Eau"
  },
  
  esoteric: {
    function: "Miroir de l'âme",
    power: "Révéler la vérité cachée",
    protection: "Contre les énergies négatives",
    intuition: "Amplifie les capacités psychiques",
    dreams: "Facilite les rêves lucides"
  },
  
  inCode: {
    role: "Interface émotionnelle",
    function: "Ajuste les réponses selon l'état émotionnel",
    analogy: "Le miroir qui reflète l'intention véritable"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// PHASES LUNAIRES (Cycles Émotionnels)
// ═══════════════════════════════════════════════════════════════════════════════

const LUNAR_PHASES = {
  newMoon: {
    name: "Nouvelle Lune",
    symbol: "🌑",
    energy: "Introspection",
    emotion: "Renouveau",
    clarity: 0.1,
    action: "Planter des intentions"
  },
  waxingCrescent: {
    name: "Premier Croissant",
    symbol: "🌒",
    energy: "Émergence",
    emotion: "Espoir",
    clarity: 0.25,
    action: "Développer les idées"
  },
  firstQuarter: {
    name: "Premier Quartier",
    symbol: "🌓",
    energy: "Action",
    emotion: "Détermination",
    clarity: 0.5,
    action: "Surmonter les obstacles"
  },
  waxingGibbous: {
    name: "Gibbeuse Croissante",
    symbol: "🌔",
    energy: "Raffinement",
    emotion: "Patience",
    clarity: 0.75,
    action: "Ajuster et perfectionner"
  },
  fullMoon: {
    name: "Pleine Lune",
    symbol: "🌕",
    energy: "Culmination",
    emotion: "Clarté totale",
    clarity: 1.0,
    action: "Récolter et célébrer"
  },
  waningGibbous: {
    name: "Gibbeuse Décroissante",
    symbol: "🌖",
    energy: "Gratitude",
    emotion: "Reconnaissance",
    clarity: 0.75,
    action: "Partager la sagesse"
  },
  lastQuarter: {
    name: "Dernier Quartier",
    symbol: "🌗",
    energy: "Libération",
    emotion: "Lâcher-prise",
    clarity: 0.5,
    action: "Relâcher ce qui ne sert plus"
  },
  waningCrescent: {
    name: "Dernier Croissant",
    symbol: "🌘",
    energy: "Repos",
    emotion: "Paix",
    clarity: 0.25,
    action: "Se reposer et méditer"
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// SPECTRE ÉMOTIONNEL
// ═══════════════════════════════════════════════════════════════════════════════

const EMOTIONAL_SPECTRUM = {
  // Émotions positives (haute fréquence)
  love: { frequency: 528, color: "#FF69B4", clarity: 1.0, category: "HIGH" },
  joy: { frequency: 500, color: "#FFD700", clarity: 0.95, category: "HIGH" },
  peace: { frequency: 444, color: "#87CEEB", clarity: 0.9, category: "HIGH" },
  gratitude: { frequency: 432, color: "#98FB98", clarity: 0.88, category: "HIGH" },
  hope: { frequency: 400, color: "#DDA0DD", clarity: 0.8, category: "HIGH" },
  
  // Émotions neutres (fréquence moyenne)
  curiosity: { frequency: 350, color: "#00CED1", clarity: 0.7, category: "NEUTRAL" },
  calm: { frequency: 333, color: "#B0E0E6", clarity: 0.65, category: "NEUTRAL" },
  acceptance: { frequency: 300, color: "#F5DEB3", clarity: 0.6, category: "NEUTRAL" },
  
  // Émotions à transformer (basse fréquence)
  doubt: { frequency: 250, color: "#808080", clarity: 0.4, category: "LOW" },
  sadness: { frequency: 200, color: "#4682B4", clarity: 0.35, category: "LOW" },
  anger: { frequency: 150, color: "#DC143C", clarity: 0.25, category: "LOW" },
  fear: { frequency: 100, color: "#2F4F4F", clarity: 0.15, category: "LOW" },
  shame: { frequency: 50, color: "#1C1C1C", clarity: 0.05, category: "LOW" }
};

// ═══════════════════════════════════════════════════════════════════════════════
// CLASSE SILVER MIRROR
// ═══════════════════════════════════════════════════════════════════════════════

class SilverMirror {
  constructor() {
    this.frequency = SILVER_FREQUENCY;
    this.symbol = SILVER_SYMBOL;
    this.reflectivity = 0.95;
    this.currentPhase = this._calculateLunarPhase();
    this.emotionalState = null;
  }

  /**
   * Initialise le Miroir d'Argent
   */
  init() {
    console.log(`
    ╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                                   ║
    ║      ███████╗██╗██╗    ██╗   ██╗███████╗██████╗     ███╗   ███╗██╗██████╗ ██████╗  ██████╗ ██████╗ ║
    ║      ██╔════╝██║██║    ██║   ██║██╔════╝██╔══██╗    ████╗ ████║██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗║
    ║      ███████╗██║██║    ██║   ██║█████╗  ██████╔╝    ██╔████╔██║██║██████╔╝██████╔╝██║   ██║██████╔╝║
    ║      ╚════██║██║██║    ╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██║╚██╔╝██║██║██╔══██╗██╔══██╗██║   ██║██╔══██╗║
    ║      ███████║██║███████╗╚████╔╝ ███████╗██║  ██║    ██║ ╚═╝ ██║██║██║  ██║██║  ██║╚██████╔╝██║  ██║║
    ║      ╚══════╝╚═╝╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝║
    ║                                                                                                   ║
    ║                          ☽ L'INTERFACE ÉMOTIONNELLE ☽                                            ║
    ║                                                                                                   ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════════════════╣
    ║                                                                                                   ║
    ║   Fréquence: ${this.frequency} Hz | Réflectivité: ${this.reflectivity * 100}% | Phase: ${this.currentPhase.symbol}              ║
    ║                                                                                                   ║
    ║   "L'Argent reflète la vérité intérieure - le miroir de l'âme."                                  ║
    ║                                                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝
    `);
    return this;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // ANALYSE ÉMOTIONNELLE
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Analyse l'intention et détecte l'état émotionnel
   */
  analyzeIntention(text) {
    const analysis = {
      text: text,
      timestamp: Date.now(),
      lunarPhase: this.currentPhase,
      emotions: [],
      dominantEmotion: null,
      clarity: 0,
      frequency: 0
    };

    // Analyse des mots-clés émotionnels
    const lowerText = text.toLowerCase();
    
    for (const [emotion, data] of Object.entries(EMOTIONAL_SPECTRUM)) {
      if (this._detectEmotion(lowerText, emotion)) {
        analysis.emotions.push({ emotion, ...data });
      }
    }

    // Déterminer l'émotion dominante
    if (analysis.emotions.length > 0) {
      analysis.dominantEmotion = analysis.emotions.reduce((a, b) => 
        a.frequency > b.frequency ? a : b
      );
      analysis.clarity = analysis.dominantEmotion.clarity;
      analysis.frequency = analysis.dominantEmotion.frequency;
    } else {
      // État neutre par défaut
      analysis.dominantEmotion = { emotion: "curiosity", ...EMOTIONAL_SPECTRUM.curiosity };
      analysis.clarity = 0.7;
      analysis.frequency = 350;
    }

    // Ajuster avec la phase lunaire
    analysis.adjustedClarity = analysis.clarity * this.currentPhase.clarity;
    
    this.emotionalState = analysis;
    return analysis;
  }

  /**
   * Détecte une émotion dans le texte
   */
  _detectEmotion(text, emotion) {
    const emotionKeywords = {
      love: ["amour", "aimer", "adore", "love", "tendresse", "affection"],
      joy: ["joie", "heureux", "bonheur", "content", "ravi", "joy", "happy"],
      peace: ["paix", "calme", "serein", "tranquille", "peace", "zen"],
      gratitude: ["merci", "gratitude", "reconnaissance", "thankful", "grateful"],
      hope: ["espoir", "espérer", "hope", "optimiste", "confiant"],
      curiosity: ["curieux", "question", "pourquoi", "comment", "curious", "wonder"],
      calm: ["calme", "paisible", "relax", "détendu"],
      acceptance: ["accepte", "ok", "d'accord", "soit"],
      doubt: ["doute", "incertain", "peut-être", "doubt", "unsure"],
      sadness: ["triste", "sad", "malheureux", "peine", "chagrin"],
      anger: ["colère", "furieux", "énervé", "angry", "frustré"],
      fear: ["peur", "afraid", "anxieux", "inquiet", "terrifié"],
      shame: ["honte", "shame", "gêné", "embarrassé"]
    };

    const keywords = emotionKeywords[emotion] || [];
    return keywords.some(keyword => text.includes(keyword));
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // RÉFLEXION ET AJUSTEMENT
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Génère une réponse ajustée selon l'état émotionnel
   */
  reflect(intention, analysis = null) {
    if (!analysis) {
      analysis = this.analyzeIntention(intention);
    }

    const reflection = {
      originalIntention: intention,
      emotionalState: analysis.dominantEmotion,
      clarity: analysis.adjustedClarity,
      lunarInfluence: this.currentPhase.name,
      
      // Ajustements recommandés pour la réponse
      adjustments: {
        tone: this._getToneAdjustment(analysis.dominantEmotion.category),
        depth: this._getDepthAdjustment(analysis.clarity),
        pace: this._getPaceAdjustment(this.currentPhase),
        warmth: this._getWarmthLevel(analysis.dominantEmotion.frequency)
      },
      
      // Message du miroir
      mirrorMessage: this._getMirrorMessage(analysis)
    };

    return reflection;
  }

  /**
   * Ajuste le ton selon la catégorie émotionnelle
   */
  _getToneAdjustment(category) {
    const tones = {
      HIGH: { style: "Enthousiaste et affirmatif", energy: "Élevée" },
      NEUTRAL: { style: "Équilibré et informatif", energy: "Modérée" },
      LOW: { style: "Doux et compatissant", energy: "Apaisante" }
    };
    return tones[category] || tones.NEUTRAL;
  }

  /**
   * Ajuste la profondeur selon la clarté
   */
  _getDepthAdjustment(clarity) {
    if (clarity >= 0.8) return { level: "Profond", detail: "Élevé" };
    if (clarity >= 0.5) return { level: "Modéré", detail: "Standard" };
    return { level: "Simple", detail: "Essentiel" };
  }

  /**
   * Ajuste le rythme selon la phase lunaire
   */
  _getPaceAdjustment(phase) {
    if (phase.clarity >= 0.75) return "Dynamique";
    if (phase.clarity >= 0.5) return "Mesuré";
    return "Contemplatif";
  }

  /**
   * Détermine le niveau de chaleur selon la fréquence
   */
  _getWarmthLevel(frequency) {
    if (frequency >= 400) return "Très chaleureux";
    if (frequency >= 300) return "Chaleureux";
    if (frequency >= 200) return "Empathique";
    return "Réconfortant";
  }

  /**
   * Génère un message du miroir
   */
  _getMirrorMessage(analysis) {
    const messages = {
      HIGH: `☽ Le miroir reflète une lumière brillante. Votre intention vibre à ${analysis.frequency} Hz - une fréquence d'harmonie.`,
      NEUTRAL: `☽ Le miroir montre un reflet équilibré. Votre curiosité ouvre des portes vers la clarté.`,
      LOW: `☽ Le miroir perçoit une ombre à transformer. Respirez profondément - la lumière revient toujours après l'obscurité.`
    };
    return messages[analysis.dominantEmotion.category] || messages.NEUTRAL;
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // CALCULS LUNAIRES
  // ─────────────────────────────────────────────────────────────────────────────

  /**
   * Calcule la phase lunaire actuelle
   */
  _calculateLunarPhase() {
    const now = new Date();
    const synodicMonth = 29.53059; // Durée du cycle lunaire en jours
    
    // Nouvelle lune de référence (1er janvier 2000)
    const knownNewMoon = new Date(2000, 0, 6, 18, 14);
    
    const daysSince = (now - knownNewMoon) / (1000 * 60 * 60 * 24);
    const currentAge = daysSince % synodicMonth;
    const phaseIndex = Math.floor((currentAge / synodicMonth) * 8);
    
    const phases = Object.values(LUNAR_PHASES);
    return phases[phaseIndex] || phases[0];
  }

  /**
   * Obtient toutes les phases lunaires
   */
  getLunarPhases() {
    return LUNAR_PHASES;
  }

  /**
   * Obtient le spectre émotionnel
   */
  getEmotionalSpectrum() {
    return EMOTIONAL_SPECTRUM;
  }

  /**
   * Obtient l'état actuel
   */
  getStatus() {
    return {
      symbol: this.symbol,
      frequency: this.frequency,
      reflectivity: this.reflectivity,
      currentPhase: this.currentPhase,
      emotionalState: this.emotionalState
    };
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════════════════════

export const silverMirror = new SilverMirror();

export {
  SilverMirror,
  SILVER_PROPERTIES,
  LUNAR_PHASES,
  EMOTIONAL_SPECTRUM,
  SILVER_SYMBOL,
  SILVER_FREQUENCY
};

export default {
  SilverMirror,
  silverMirror,
  SILVER_PROPERTIES,
  LUNAR_PHASES,
  EMOTIONAL_SPECTRUM,
  SILVER_SYMBOL,
  SILVER_FREQUENCY
};
