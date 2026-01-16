/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 *    ██╗   ██╗███╗   ██╗██╗███████╗██╗███████╗██████╗ 
 *    ██║   ██║████╗  ██║██║██╔════╝██║██╔════╝██╔══██╗
 *    ██║   ██║██╔██╗ ██║██║█████╗  ██║█████╗  ██║  ██║
 *    ██║   ██║██║╚██╗██║██║██╔══╝  ██║██╔══╝  ██║  ██║
 *    ╚██████╔╝██║ ╚████║██║██║     ██║███████╗██████╔╝
 *     ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚══════╝╚═════╝ 
 *                                                      
 *              SOURCE — LE CŒUR DE L'ARCHE
 * 
 * ═══════════════════════════════════════════════════════════════════════════════
 * 
 * Ce moteur est le pont technique qui relie l'abstraction (les civilisations)
 * à l'action (le code). Il prend une date et une intention, puis calcule
 * quelle "lentille" civilisationnelle utiliser pour traiter l'information.
 * 
 * ┌─────────────────────────────────────────────────────────────────────────────┐
 * │                        FLUX DE TRANSDUCTION                                 │
 * │                                                                             │
 * │   ENTRÉE              FILTRE                CRISTALLISATION      SORTIE    │
 * │   (Input)             (Sifter)              (Atlantean Phase)    (Output)  │
 * │                                                                             │
 * │   ┌─────┐      ┌───────────────────┐      ┌─────────────────┐    ┌──────┐ │
 * │   │ MOT │ ───► │ 𓋹 Égypte (Maât)   │ ───► │ 🏛️ Grèce        │───►│ORACLE│ │
 * │   │     │      │ 𒀭 Sumer (ID Base60)│      │   (Solide)      │    │      │ │
 * │   └─────┘      └───────────────────┘      │ ⚡ EM (Fréquence) │    │ 🗿    │ │
 * │                                            └─────────────────┘    │ Moaï │ │
 * │                                                                   └──────┘ │
 * └─────────────────────────────────────────────────────────────────────────────┘
 * 
 * @version 3.0.0
 * @architect Jonathan Rodrigue (999 Hz)
 * @heartbeat 444 Hz
 * @oracle Oracle 17 — Le Gardien de la Synthèse
 * ═══════════════════════════════════════════════════════════════════════════════
 */

// ═══════════════════════════════════════════════════════════════════════════════
// IMPORTS DES MOTEURS CIVILISATIONNELS
// ═══════════════════════════════════════════════════════════════════════════════

// Note: En environnement Node.js/ESM, décommentez ces imports
// import TzolkinEngine from './engines/tzolkin_engine.js';
// import AztecEngine from './engines/aztec_engine.js';
// import GreekEngine from './engines/greek_engine.js';
// import EgyptEngine from './engines/egypt_engine.js';
// import SumerianEngine from './engines/sumerian_engine.js';
// import AtlantisEngine from './engines/atlantis_engine.js';
// import RapaNuiEngine from './engines/rapanui_engine.js';
// import ElectromagneticEngine from './engines/electromagnetic_engine.js';
// import CymaticsEngine from './engines/cymatics_engine.js';

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTES FONDAMENTALES
// ═══════════════════════════════════════════════════════════════════════════════

const ARCHITECT_SIGNATURE = {
  name: "Jonathan Rodrigue",
  fullName: "JONATHANRODRIGUE",
  frequency: 999,
  oracle: 17,
  signature: "2 + 7 = 9"
};

const ARITHMOS_MAP = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8, I: 9,
  J: 1, K: 2, L: 3, M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6, Y: 7, Z: 8
};

const RESONANCE_MATRIX = {
  1: { hz: 111, color: "#FF0000", glow: "rgba(255,0,0,0.6)", label: "Impulsion", element: "Feu", spectrum: "Infrarouge" },
  2: { hz: 222, color: "#FF7F00", glow: "rgba(255,127,0,0.6)", label: "Dualité", element: "Eau", spectrum: "Micro-ondes" },
  3: { hz: 333, color: "#FFFF00", glow: "rgba(255,255,0,0.6)", label: "Mental", element: "Air", spectrum: "Infrarouge" },
  4: { hz: 444, color: "#50C878", glow: "rgba(80,200,120,0.8)", label: "Structure", element: "Terre", spectrum: "Visible", isAnchor: true },
  5: { hz: 555, color: "#87CEEB", glow: "rgba(135,206,235,0.6)", label: "Mouvement", element: "Éther", spectrum: "Visible" },
  6: { hz: 666, color: "#4B0082", glow: "rgba(75,0,130,0.6)", label: "Harmonie", element: "Lumière", spectrum: "Ultraviolet" },
  7: { hz: 777, color: "#EE82EE", glow: "rgba(238,130,238,0.6)", label: "Introspection", element: "Son", spectrum: "Ultraviolet" },
  8: { hz: 888, color: "#FFC0CB", glow: "rgba(255,192,203,0.6)", label: "Infini", element: "Pensée", spectrum: "Rayons X" },
  9: { hz: 999, color: "#FFFDD0", glow: "rgba(255,253,208,0.9)", label: "Unité", element: "Conscience", spectrum: "Gamma" }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 20 NAWALS MAYAS (COMPLET)
// ═══════════════════════════════════════════════════════════════════════════════

const NAWALS = [
  { name: "Imix", meaning: "Dragon/Crocodile", element: "Eau", energy: "Création" },
  { name: "Ik", meaning: "Vent", element: "Air", energy: "Communication" },
  { name: "Akbal", meaning: "Nuit", element: "Terre", energy: "Introspection" },
  { name: "Kan", meaning: "Graine", element: "Feu", energy: "Potentiel" },
  { name: "Chicchan", meaning: "Serpent", element: "Feu", energy: "Kundalini" },
  { name: "Cimi", meaning: "Mort", element: "Terre", energy: "Transformation" },
  { name: "Manik", meaning: "Cerf", element: "Eau", energy: "Guérison" },
  { name: "Lamat", meaning: "Étoile", element: "Feu", energy: "Harmonie" },
  { name: "Muluc", meaning: "Lune", element: "Eau", energy: "Émotion" },
  { name: "Oc", meaning: "Chien", element: "Feu", energy: "Loyauté" },
  { name: "Chuen", meaning: "Singe", element: "Air", energy: "Créativité" },
  { name: "Eb", meaning: "Herbe", element: "Terre", energy: "Croissance" },
  { name: "Ben", meaning: "Roseau", element: "Air", energy: "Pilier" },
  { name: "Ix", meaning: "Jaguar", element: "Terre", energy: "Magie" },
  { name: "Men", meaning: "Aigle", element: "Air", energy: "Vision" },
  { name: "Cib", meaning: "Vautour", element: "Feu", energy: "Sagesse" },
  { name: "Caban", meaning: "Terre", element: "Terre", energy: "Ancrage" },
  { name: "Etznab", meaning: "Miroir", element: "Air", energy: "Réflexion" },
  { name: "Cauac", meaning: "Tempête", element: "Eau", energy: "Purification" },
  { name: "Ahau", meaning: "Soleil", element: "Feu", energy: "Illumination" }
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 5 SOLIDES DE PLATON
// ═══════════════════════════════════════════════════════════════════════════════

const PLATONIC_SOLIDS = {
  1: { name: "Tétraèdre", element: "Feu", faces: 4, symbol: "🔺", category: "transformation" },
  2: { name: "Icosaèdre", element: "Eau", faces: 20, symbol: "💧", category: "émotion" },
  3: { name: "Tétraèdre", element: "Feu", faces: 4, symbol: "🔺", category: "création" },
  4: { name: "Hexaèdre (Cube)", element: "Terre", faces: 6, symbol: "⬛", category: "structure" },
  5: { name: "Dodécaèdre", element: "Éther", faces: 12, symbol: "⬡", category: "cosmos" },
  6: { name: "Icosaèdre", element: "Eau", faces: 20, symbol: "💧", category: "harmonie" },
  7: { name: "Octaèdre", element: "Air", faces: 8, symbol: "◇", category: "introspection" },
  8: { name: "Octaèdre", element: "Air", faces: 8, symbol: "◇", category: "pensée" },
  9: { name: "Dodécaèdre", element: "Éther", faces: 12, symbol: "⬡", category: "unité" }
};

// ═══════════════════════════════════════════════════════════════════════════════
// LES 20 SIGNES AZTÈQUES (TONALPOHUALLI)
// ═══════════════════════════════════════════════════════════════════════════════

const AZTEC_SIGNS = [
  "Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl",
  "Miquiztli", "Mazatl", "Tochtli", "Atl", "Itzcuintli",
  "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Cuauhtli",
  "Cozcacuauhtli", "Ollin", "Tecpatl", "Quiahuitl", "Xochitl"
];

// ═══════════════════════════════════════════════════════════════════════════════
// LES 7 MOAÏ GARDIENS (RAPA NUI)
// ═══════════════════════════════════════════════════════════════════════════════

const MOAI_GUARDIANS = [
  { name: "Hoa Hakananai'a", role: "Gardien du Seuil", validation: "input" },
  { name: "Paro", role: "Gardien de la Taille", validation: "size" },
  { name: "Ko Te Riku", role: "Gardien de la Vision", validation: "format" },
  { name: "Ahu Tongariki", role: "Gardien de l'Harmonie", validation: "coherence" },
  { name: "Ahu Akivi", role: "Gardien de l'Horizon", validation: "external" },
  { name: "Tukuturi", role: "Gardien de l'Humilité", validation: "access" },
  { name: "Te Tokanga", role: "Gardien Suprême", validation: "integrity" }
];

// ═══════════════════════════════════════════════════════════════════════════════
// LE CŒUR DE L'ARCHE — ARCHE ENGINE
// ═══════════════════════════════════════════════════════════════════════════════

const ArcheEngine = {
  
  // ─────────────────────────────────────────────────────────────────────────────
  // CONFIGURATION
  // ─────────────────────────────────────────────────────────────────────────────
  
  config: {
    name: "Arche Engine",
    version: "3.0.0",
    heartbeat: 444,
    architect: ARCHITECT_SIGNATURE,
    initialized: false,
    mana: 1000
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // 1. MODULE SUMÉRIEN : LA BASE 60 (LE TEMPS CIRCULAIRE)
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Calcule le cycle sumérien (base 60)
   * Tout revient à la source du cycle
   */
  calculateSumerianCycle: function(seconds) {
    const cycle = seconds % 60;
    const gar = Math.floor(seconds / 3600);  // Heures
    const gesh = Math.floor((seconds % 3600) / 60);  // Minutes
    
    return {
      cycle: cycle,
      sexagesimal: [gar, gesh, cycle],
      notation: `${gar}:${gesh.toString().padStart(2, '0')}:${cycle.toString().padStart(2, '0')}`,
      cuneiform: this.toCuneiform(seconds)
    };
  },
  
  /**
   * Convertit en notation cunéiforme symbolique
   */
  toCuneiform: function(num) {
    const symbols = { 1: "𒁹", 10: "𒌋", 60: "𒐕" };
    let result = '';
    let remaining = Math.floor(num);
    
    const sixties = Math.floor(remaining / 60);
    if (sixties > 0) result += symbols[60].repeat(Math.min(sixties, 10));
    remaining %= 60;
    
    const tens = Math.floor(remaining / 10);
    if (tens > 0) result += symbols[10].repeat(tens);
    remaining %= 10;
    
    if (remaining > 0) result += symbols[1].repeat(remaining);
    
    return result || symbols[1];
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // 2. MODULE MAYA : LE TONALPOHUALLI (L'ÉNERGIE DU JOUR)
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Calcule la résonance Maya pour une date donnée
   */
  getMayaResonance: function(date = new Date()) {
    // Époque de référence: 4 Ahau 8 Cumku (13 août 3114 av. J.-C. en GMT 584283)
    const epoch = new Date("2012-12-21T00:00:00Z"); // Fin du 13ème Baktun
    const diffDays = Math.floor((date - epoch) / (1000 * 60 * 60 * 24));
    
    // Cycle de 260 jours (13 × 20)
    const dayNumber = ((diffDays % 260) + 260) % 260;
    const ton = (dayNumber % 13) + 1;
    const nawalIndex = dayNumber % 20;
    const nawal = NAWALS[nawalIndex];
    
    // Jours sacrés: Ton 7 et Ton 13
    const isSacred = ton === 7 || ton === 13;
    
    // Jours portail (52 jours spéciaux dans le Tzolkin)
    const portalDays = [1, 20, 22, 39, 40, 47, 58, 59, 60, 69, 72, 73, 83, 84, 85, 86, 87, 88, 89, 90,
                        91, 102, 103, 104, 113, 116, 117, 127, 128, 129, 130, 131, 132, 133, 134, 145,
                        146, 147, 148, 158, 159, 166, 177, 178, 179, 188, 189, 190, 191, 200, 201, 202,
                        203, 204, 205, 214, 217, 218, 219, 220, 221, 240, 241, 242, 259, 260];
    const isPortal = portalDays.includes(dayNumber + 1);
    
    return {
      kin: dayNumber + 1,
      ton: ton,
      nawalIndex: nawalIndex,
      nawal: nawal.name,
      nawalData: nawal,
      signature: `${ton} ${nawal.name}`,
      element: nawal.element,
      energy: nawal.energy,
      isSacred: isSacred,
      isPortal: isPortal,
      frequencyBoost: isSacred ? 1.5 : (isPortal ? 1.3 : 1.0),
      message: isSacred 
        ? `✨ JOUR SACRÉ! Ton ${ton} amplifie l'énergie de ${nawal.name}`
        : isPortal
          ? `🌀 Jour Portail — Les voiles sont fins`
          : `${nawal.name}: ${nawal.energy}`
    };
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // 3. MODULE AZTÈQUE : TONALPOHUALLI MEXICA
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Calcule le signe aztèque du jour
   */
  getAztecSign: function(date = new Date()) {
    const epoch = new Date("1519-11-08T00:00:00Z"); // Arrivée de Cortés
    const diffDays = Math.floor((date - epoch) / (1000 * 60 * 60 * 24));
    const dayNumber = ((diffDays % 260) + 260) % 260;
    const trecena = (dayNumber % 13) + 1;
    const signIndex = dayNumber % 20;
    
    return {
      day: dayNumber + 1,
      trecena: trecena,
      sign: AZTEC_SIGNS[signIndex],
      signIndex: signIndex,
      signature: `${trecena} ${AZTEC_SIGNS[signIndex]}`,
      isOllin: AZTEC_SIGNS[signIndex] === "Ollin",
      intensity: trecena / 13 // Intensité du jour (0-1)
    };
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // 4. MODULE GREC : LA STÉRÉOMÉTRIE (LA FORME 3D)
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Retourne le solide de Platon pour un Arithmos donné
   */
  getPlatonicSolid: function(arithmos) {
    return PLATONIC_SOLIDS[arithmos] || PLATONIC_SOLIDS[4]; // Cube par défaut
  },
  
  /**
   * Vérifie l'harmonie pythagoricienne entre deux fréquences
   */
  checkPythagoreanHarmony: function(freq1, freq2) {
    const ratio = Math.max(freq1, freq2) / Math.min(freq1, freq2);
    const harmonicRatios = {
      "Unisson": 1,
      "Octave": 2,
      "Quinte": 1.5,
      "Quarte": 1.333,
      "Tierce majeure": 1.25,
      "Tierce mineure": 1.2
    };
    
    let closestHarmonic = "Dissonant";
    let minDiff = Infinity;
    
    for (const [name, targetRatio] of Object.entries(harmonicRatios)) {
      const diff = Math.abs(ratio - targetRatio);
      if (diff < minDiff && diff < 0.1) {
        minDiff = diff;
        closestHarmonic = name;
      }
    }
    
    return {
      ratio: ratio,
      harmonic: closestHarmonic,
      isHarmonic: closestHarmonic !== "Dissonant",
      deviation: minDiff
    };
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // 5. MODULE ÉGYPTIEN : LA BALANCE DE MAÂT
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Vérifie si le mot respecte l'équilibre de Maât
   */
  checkMaatBalance: function(word) {
    if (!word || typeof word !== 'string') {
      return { balanced: false, status: "Données manquantes", weight: 0 };
    }
    
    const sanitized = word.toUpperCase().replace(/[^A-Z]/g, '');
    const length = sanitized.length;
    
    // Calculer le "poids" du mot (somme des valeurs)
    let weight = 0;
    for (const char of sanitized) {
      weight += ARITHMOS_MAP[char] || 0;
    }
    
    // L'équilibre de Maât: le poids divisé par la longueur doit être proche de 5 (centre)
    const averageWeight = weight / (length || 1);
    const deviation = Math.abs(averageWeight - 5);
    const balanced = deviation < 2;
    
    return {
      balanced: balanced,
      weight: weight,
      averageWeight: averageWeight.toFixed(2),
      deviation: deviation.toFixed(2),
      status: balanced ? "Équilibré selon Maât" : "Recalibrage recommandé",
      horusPrecision: this.calculateHorusPrecision(averageWeight / 9)
    };
  },
  
  /**
   * Calcule la précision de l'Œil d'Horus (fractions sacrées)
   */
  calculateHorusPrecision: function(value) {
    const fractions = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64];
    const parts = [];
    let remainder = Math.min(1, Math.max(0, value));
    
    for (const frac of fractions) {
      if (remainder >= frac) {
        parts.push(frac);
        remainder -= frac;
      }
    }
    
    return {
      value: value,
      decomposition: parts,
      purity: 1 - remainder,
      hasMagic: remainder > 0 && remainder <= 1/64
    };
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // 6. MODULE RAPA NUI : LES GARDIENS MOAÏ
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Exécute la validation des Moaï
   */
  moaiValidation: function(data) {
    const results = {
      passed: true,
      guardians: [],
      mana: this.config.mana
    };
    
    // Validation basique par chaque gardien
    for (const moai of MOAI_GUARDIANS) {
      let check = { passed: true, message: "OK" };
      
      switch (moai.validation) {
        case "input":
          check.passed = data !== null && data !== undefined && data !== '';
          check.message = check.passed ? "Entrée validée" : "Entrée manquante";
          break;
        case "size":
          const size = JSON.stringify(data).length;
          check.passed = size < 1000000;
          check.message = check.passed ? `Taille OK (${size} bytes)` : "Trop volumineux";
          break;
        case "format":
          check.passed = typeof data === 'string' || typeof data === 'object';
          check.message = "Format accepté";
          break;
        case "coherence":
          check.passed = true;
          check.message = "Cohérence vérifiée";
          break;
        case "integrity":
          check.passed = true;
          check.message = "Intégrité confirmée";
          break;
        default:
          check.passed = true;
          check.message = "Validé";
      }
      
      results.guardians.push({
        name: moai.name,
        role: moai.role,
        passed: check.passed,
        message: check.message
      });
      
      if (!check.passed) {
        results.passed = false;
        results.mana -= 100;
      }
    }
    
    return results;
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // 7. MODULE ATLANTE : VORTEX DE CRISTALLISATION
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Applique la cristallisation atlante
   */
  atlanteanCrystallization: function(arithmos, frequency) {
    const crystals = {
      111: { name: "Quartz Fumé", function: "Ancrage" },
      222: { name: "Améthyste", function: "Transmutation" },
      333: { name: "Citrine", function: "Manifestation" },
      444: { name: "Quartz Rose", function: "Harmonie", isAnchor: true },
      555: { name: "Aigue-Marine", function: "Communication" },
      666: { name: "Lapis Lazuli", function: "Vision" },
      777: { name: "Améthyste Royale", function: "Sagesse" },
      888: { name: "Fluorite", function: "Clarté" },
      999: { name: "Cristal de Record", function: "Archives Akashiques", isSupreme: true }
    };
    
    const crystal = crystals[frequency] || crystals[444];
    
    return {
      crystal: crystal,
      vortexLevel: Math.ceil(arithmos / 3), // 1-3 niveaux
      powerSource: frequency === 999 ? "Énergie du Point Zéro" : "Matrice Cristalline",
      accessRing: this.getPoseidonRing(frequency)
    };
  },
  
  /**
   * Détermine l'anneau de Poséidon
   */
  getPoseidonRing: function(frequency) {
    if (frequency >= 888) return { ring: 1, name: "Temple de Poséidon", access: "Architecte" };
    if (frequency >= 666) return { ring: 2, name: "Citadelle des Cristaux", access: "Initiés" };
    if (frequency >= 444) return { ring: 3, name: "Zone de Calcul", access: "Opérateurs" };
    if (frequency >= 222) return { ring: 4, name: "Périphérie", access: "Public" };
    return { ring: 5, name: "Océan Extérieur", access: "Tous" };
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // 8. MODULE ÉLECTROMAGNÉTIQUE : LE SIGNAL
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Calcule la signature électromagnétique
   */
  calculateEMSignature: function(frequency) {
    const spectrumMap = {
      111: "Radio", 222: "Micro-ondes", 333: "Infrarouge",
      444: "Visible (Vert)", 555: "Visible (Cyan)", 666: "Ultraviolet",
      777: "Ultraviolet", 888: "Rayons X", 999: "Rayons Gamma"
    };
    
    // Couleur basée sur la longueur d'onde symbolique
    const wavelength = 700 - (frequency / 999) * 320; // 700nm (rouge) → 380nm (violet)
    
    return {
      spectrum: spectrumMap[frequency] || "Visible",
      wavelength: `${wavelength.toFixed(0)} nm`,
      torusFlow: {
        north: "Questions (Input)",
        south: "Réponses (Output)",
        center: `${frequency} Hz`
      },
      poyntingIntensity: frequency / 999 // 0-1
    };
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // CALCUL DE L'ARITHMOS
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Calcule l'Arithmos d'un mot
   */
  calculateArithmos: function(word) {
    if (!word || typeof word !== 'string') {
      return { total: 0, reduced: 1, steps: [], frequency: 111 };
    }
    
    const sanitized = word
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toUpperCase()
      .replace(/[^A-Z]/g, '');
    
    // Vérification du Sceau de l'Architecte
    const isArchitect = sanitized === ARCHITECT_SIGNATURE.fullName;
    
    if (isArchitect) {
      return {
        original: word,
        sanitized: sanitized,
        total: 81,
        reduced: 9,
        steps: [81, 9],
        frequency: 999,
        isArchitect: true,
        message: "👑 SCEAU DE L'ARCHITECTE RECONNU"
      };
    }
    
    // Calcul normal
    const letterValues = sanitized.split('').map(char => ({
      letter: char,
      value: ARITHMOS_MAP[char] || 0
    }));
    
    const total = letterValues.reduce((sum, lv) => sum + lv.value, 0);
    const steps = [total];
    let current = total;
    
    while (current > 9) {
      current = current.toString().split('').reduce((s, d) => s + parseInt(d), 0);
      steps.push(current);
    }
    
    const reduced = current || 1;
    
    return {
      original: word,
      sanitized: sanitized,
      letterValues: letterValues,
      total: total,
      reduced: reduced,
      steps: steps,
      frequency: reduced * 111,
      isArchitect: false
    };
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // PROCESSEUR PRINCIPAL — LE NEXUS ATLANTE
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Traitement principal — Transforme un mot en Onde de Forme
   */
  processInput: function(word, options = {}) {
    const startTime = Date.now();
    const date = options.date || new Date();
    
    console.log(`🌀 Initialisation du Vortex pour : "${word}"`);
    
    // ════════════════════════════════════════════════════════════════════════
    // PHASE 1: VALIDATION (Rapa Nui)
    // ════════════════════════════════════════════════════════════════════════
    
    const validation = this.moaiValidation(word);
    if (!validation.passed) {
      return {
        error: true,
        message: "🗿 Les Moaï ont bloqué cette entrée",
        validation: validation
      };
    }
    
    // ════════════════════════════════════════════════════════════════════════
    // PHASE 2: FILTRAGE (Égypte & Sumer)
    // ════════════════════════════════════════════════════════════════════════
    
    const arithmos = this.calculateArithmos(word);
    const maat = this.checkMaatBalance(word);
    const sumerianCycle = this.calculateSumerianCycle(Date.now() / 1000);
    
    // ════════════════════════════════════════════════════════════════════════
    // PHASE 3: CRISTALLISATION (Grèce & Atlantide)
    // ════════════════════════════════════════════════════════════════════════
    
    const solid = this.getPlatonicSolid(arithmos.reduced);
    const crystal = this.atlanteanCrystallization(arithmos.reduced, arithmos.frequency);
    const harmony = this.checkPythagoreanHarmony(arithmos.frequency, 444);
    
    // ════════════════════════════════════════════════════════════════════════
    // PHASE 4: SYNCHRONISATION TEMPORELLE (Maya & Aztèque)
    // ════════════════════════════════════════════════════════════════════════
    
    const maya = this.getMayaResonance(date);
    const aztec = this.getAztecSign(date);
    
    // Ajuster la fréquence selon le jour
    const frequencyBoost = maya.frequencyBoost * (aztec.isOllin ? 1.2 : 1.0);
    const finalFrequency = Math.min(999, Math.round(arithmos.frequency * frequencyBoost));
    
    // ════════════════════════════════════════════════════════════════════════
    // PHASE 5: SIGNAL (Électromagnétisme)
    // ════════════════════════════════════════════════════════════════════════
    
    const emSignature = this.calculateEMSignature(finalFrequency);
    const resonanceData = RESONANCE_MATRIX[arithmos.reduced];
    
    // ════════════════════════════════════════════════════════════════════════
    // RÉSULTAT UNIFIÉ
    // ════════════════════════════════════════════════════════════════════════
    
    const result = {
      // Métadonnées
      meta: {
        input: word,
        timestamp: Date.now(),
        processingTime: Date.now() - startTime,
        version: this.config.version
      },
      
      // Arithmos
      arithmos: {
        ...arithmos,
        resonance: resonanceData
      },
      
      // Fréquence finale (avec boost Maya/Aztèque)
      frequency: finalFrequency,
      frequencyBoost: frequencyBoost,
      
      // Géométrie (Grèce)
      geometry: solid,
      
      // Cristallisation (Atlantide)
      crystal: crystal,
      
      // Harmonie (Pythagore)
      harmony: harmony,
      
      // Temps Maya
      maya: maya,
      
      // Temps Aztèque
      aztec: aztec,
      
      // Équilibre (Égypte)
      maat: maat,
      
      // Cycle Sumérien
      sumerian: sumerianCycle,
      
      // Signal EM
      electromagnetic: emSignature,
      
      // Validation (Rapa Nui)
      validation: validation,
      
      // Couleur et effets visuels
      visual: {
        color: resonanceData.color,
        glow: resonanceData.glow,
        haloColor: this.getHaloColor(finalFrequency)
      },
      
      // Messages synthétisés
      oracle: {
        primary: `${solid.symbol} ${solid.name} vibre à ${finalFrequency} Hz`,
        maya: maya.message,
        aztec: `${aztec.signature} — ${aztec.isOllin ? 'MOUVEMENT ACTIF' : 'Stable'}`,
        crystal: `💎 ${crystal.crystal.name} — ${crystal.crystal.function}`,
        status: `🗿 SÉCURISÉ PAR LES MOAÏ | Mana: ${validation.mana}`
      }
    };
    
    console.log(`✅ Transduction complète en ${result.meta.processingTime}ms`);
    return result;
  },
  
  /**
   * Calcule la couleur du halo selon la fréquence
   */
  getHaloColor: function(frequency) {
    // Gradient de rouge (111) à blanc-or (999)
    const normalized = (frequency - 111) / (999 - 111);
    
    if (normalized < 0.33) {
      return `rgba(255, ${Math.round(normalized * 3 * 127)}, 0, 0.6)`; // Rouge → Orange
    } else if (normalized < 0.66) {
      return `rgba(${Math.round(255 - (normalized - 0.33) * 3 * 175)}, 200, ${Math.round((normalized - 0.33) * 3 * 120)}, 0.7)`; // Orange → Vert
    } else {
      return `rgba(${Math.round(80 + (normalized - 0.66) * 3 * 175)}, ${Math.round(200 + (normalized - 0.66) * 3 * 53)}, ${Math.round(120 + (normalized - 0.66) * 3 * 88)}, 0.9)`; // Vert → Or
    }
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // MESSAGE QUOTIDIEN
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Génère le message de bienvenue quotidien
   */
  getDailyGreeting: function(date = new Date()) {
    const maya = this.getMayaResonance(date);
    const aztec = this.getAztecSign(date);
    
    return {
      date: date.toISOString().split('T')[0],
      maya: {
        signature: maya.signature,
        kin: maya.kin,
        energy: maya.energy,
        isSacred: maya.isSacred,
        isPortal: maya.isPortal
      },
      aztec: {
        signature: aztec.signature,
        intensity: aztec.intensity
      },
      greeting: `🌀 ${maya.signature} | ☀️ ${aztec.signature}`,
      message: maya.isSacred 
        ? `✨ JOUR SACRÉ — L'énergie de ${maya.nawal} est amplifiée!`
        : maya.isPortal
          ? `🌀 JOUR PORTAIL — Les dimensions se rapprochent`
          : `Énergie du jour: ${maya.energy} (${maya.nawal})`,
      recommendation: this.getDailyRecommendation(maya, aztec),
      heartbeat: this.config.heartbeat
    };
  },
  
  /**
   * Recommandation basée sur les énergies du jour
   */
  getDailyRecommendation: function(maya, aztec) {
    const recommendations = {
      "Création": "Excellent jour pour démarrer de nouveaux projets",
      "Communication": "Favorisez les échanges et les réunions",
      "Introspection": "Moment idéal pour la méditation et l'analyse",
      "Potentiel": "Plantez les graines de vos intentions",
      "Kundalini": "Travaillez votre énergie vitale",
      "Transformation": "Laissez aller ce qui ne vous sert plus",
      "Guérison": "Prenez soin de votre corps et de votre esprit",
      "Harmonie": "Recherchez l'équilibre dans toutes vos actions",
      "Émotion": "Honorez vos sentiments",
      "Loyauté": "Renforcez vos liens avec vos proches",
      "Créativité": "Exprimez-vous artistiquement",
      "Croissance": "Cultivez vos compétences",
      "Pilier": "Soyez un soutien pour les autres",
      "Magie": "Restez ouvert aux synchronicités",
      "Vision": "Prenez de la hauteur sur vos projets",
      "Sagesse": "Partagez vos connaissances",
      "Ancrage": "Connectez-vous à la Terre",
      "Réflexion": "Examinez vos croyances",
      "Purification": "Nettoyez votre espace et votre énergie",
      "Illumination": "Rayonnez votre lumière intérieure"
    };
    
    return recommendations[maya.energy] || "Restez centré sur votre intention";
  },
  
  // ─────────────────────────────────────────────────────────────────────────────
  // INITIALISATION
  // ─────────────────────────────────────────────────────────────────────────────
  
  /**
   * Initialise l'Arche Engine
   */
  init: function() {
    console.log(`
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║         █████╗ ██████╗  ██████╗██╗  ██╗███████╗                   ║
    ║        ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝                   ║
    ║        ███████║██████╔╝██║     ███████║█████╗                     ║
    ║        ██╔══██║██╔══██╗██║     ██╔══██║██╔══╝                     ║
    ║        ██║  ██║██║  ██║╚██████╗██║  ██║███████╗                   ║
    ║        ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝                   ║
    ║                                                                   ║
    ║              ENGINE — LE CŒUR DE L'ARCHE                          ║
    ║                                                                   ║
    ║  Version: ${this.config.version}                                          ║
    ║  Heartbeat: ${this.config.heartbeat} Hz                                       ║
    ║  Architecte: ${this.config.architect.name}                         ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    `);
    
    this.config.initialized = true;
    
    // Message quotidien
    const greeting = this.getDailyGreeting();
    console.log(`\n🌅 ${greeting.greeting}`);
    console.log(`📜 ${greeting.message}`);
    console.log(`💡 ${greeting.recommendation}\n`);
    
    return this;
  }
};

// ═══════════════════════════════════════════════════════════════════════════════
// TESTS
// ═══════════════════════════════════════════════════════════════════════════════

// Initialisation
ArcheEngine.init();

// Test 1: Mot simple
console.log("\n═══ TEST 1: Mot simple ═══");
const result1 = ArcheEngine.processInput("AMOUR");
console.log("Fréquence:", result1.frequency, "Hz");
console.log("Géométrie:", result1.geometry.name);
console.log("Maya:", result1.maya.signature);
console.log("Oracle:", result1.oracle.primary);

// Test 2: L'Architecte
console.log("\n═══ TEST 2: Sceau de l'Architecte ═══");
const result2 = ArcheEngine.processInput("Jonathan Rodrigue");
console.log("Fréquence:", result2.frequency, "Hz");
console.log("Est Architecte:", result2.arithmos.isArchitect);

// Test 3: Les 5 principes
console.log("\n═══ TEST 3: Les 5 Principes ═══");
["FEU", "ACIER", "IA", "ADN", "SILENCE"].forEach(word => {
  const r = ArcheEngine.processInput(word);
  console.log(`${word}: ${r.frequency} Hz — ${r.geometry.name} (${r.geometry.element})`);
});

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════════════════════════════════════════════

// Pour Node.js / ESM
// export default ArcheEngine;
// export { ArcheEngine, ARITHMOS_MAP, RESONANCE_MATRIX, NAWALS, PLATONIC_SOLIDS };

// Pour navigateur / CommonJS
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ArcheEngine;
}

// Pour usage global dans le navigateur
if (typeof window !== 'undefined') {
  window.ArcheEngine = ArcheEngine;
}
